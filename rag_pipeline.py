import os
from dotenv import load_dotenv
from groq import Groq
import faiss
import pickle
from utils.chunking import chunk_faq, chunk_policy, chunk_products
from utils.embedding import get_embeddings

load_dotenv()
api = os.getenv("API_KEY")

client = Groq(api_key=api)

GROQ_MODEL_ID = "openai/gpt-oss-120b"


def build_index():
    import json

    faq = json.load(open("data/faq.json", encoding="utf-8"))
    policy = json.load(open("data/policy_dataset.json", encoding="utf-8"))
    products = json.load(open("data/product_details.json", encoding="utf-8"))

    docs = chunk_faq(faq) + chunk_policy(policy) + chunk_products(products)
    texts = [d["text"] for d in docs]
    metadatas = [{"text": d["text"], **d["metadata"]} for d in docs]

    embeddings = get_embeddings(texts)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, "embeddings/faiss_index.bin")
    with open("embeddings/metadata.pkl", "wb") as f:
        pickle.dump(metadatas, f)


def search_rag(query, k=3):
    import pickle
    import faiss
    from utils.embedding import get_embeddings

    query = query.strip().lower()

    index = faiss.read_index("embeddings/faiss_index.bin")
    metadata = pickle.load(open("embeddings/metadata.pkl", "rb"))

    q_emb = get_embeddings([query])
    D, I = index.search(q_emb, k)

    threshold = 1.2
    contexts = []
    for dist, idx in zip(D[0], I[0]):
        if dist < threshold:
            contexts.append(metadata[idx])
    if not contexts:
        contexts = [metadata[i] for i in I[0]]
    return contexts


def generate_answer(query, contexts, temperature=0.7, max_tokens=2048):
    prompt = "Dưới đây là các thông tin liên quan đến câu hỏi của bạn:\n\n"
    for i, context in enumerate(contexts, 1):
        info_type = context.get("type", "")
        if info_type == "faq":
            prompt += f"[FAQ] Thông tin {i}:\n{context.get('text', '')}\n\n"
        elif info_type == "policy":
            prompt += f"[Chính sách] Thông tin {i} (Danh mục: {context.get('category', '')}):\n{context.get('text', '')}\n\n"
        elif info_type == "product":
            url = context.get('url', '')
            prompt += f"[Sản phẩm] Thông tin {i} (Tên: {context.get('name', '')}, url: {url}):\n{context.get('text', '')}\n\n"
        else:
            prompt += f"Thông tin {i}:\n{context.get('text', '')}\n\n"

    prompt += f"Câu hỏi của khách hàng: {query}\n\n"
    prompt += "Vui lòng trả lời dựa trên các thông tin trên."
    prompt += "Nếu không đủ thông tin, hãy nói rõ bạn không thể trả lời chính xác."
    prompt += "Trả lời đầy đủ, rõ ý, dễ hiểu bằng tiếng Việt."
    prompt += "Nếu người dùng hỏi về thông tin sản phẩm, hãy cung cấp thông tin chi tiết về sản phẩm đó và đính kèm url."
    prompt += "Hãy nhấn mạnh những lưu ý."

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL_ID,
            messages=[
                {"role": "system",
                 "content": """Bạn là trợ lý AI của CellphoneS, một cửa hàng bán điện thoại và thiết bị điện tử.
                               Bạn giúp khách hàng trả lời các câu hỏi về sản phẩm, chính sách và các vấn đề liên quan đến CellphoneS.
                               Trả lời bằng tiếng Việt, ngắn gọn, chính xác, nêu rõ nguồn thông tin nếu có thể."""},
                {"role": "user",
                 "content": prompt}
            ],
            temperature=temperature,
            max_completion_tokens=max_tokens,
            top_p=1,
            reasoning_effort="medium",
            stream=True,
            stop=None
        )

        full_response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content

        return full_response
    except Exception as e:
        return f"Đã xảy ra lỗi khi tạo câu trả lời: {str(e)}"


def get_answer_from_query(query, k=3, temperature=0.7, max_tokens=2048):
    contexts = search_rag(query, k)

    answer = generate_answer(query, contexts, temperature, max_tokens)

    return {
        "query": query,
        "contexts": contexts,
        "answer": answer
    }
