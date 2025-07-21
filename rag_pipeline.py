import faiss
import pickle
from utils.chunking import chunk_faq, chunk_policy, chunk_products
from utils.embedding import get_embeddings


def build_index():
    import json

    faq = json.load(open("data/faq.json", encoding="utf-8"))
    policy = json.load(open("data/policy_dataset.json", encoding="utf-8"))
    products = json.load(open("data/product_details.json", encoding="utf-8"))

    docs = chunk_faq(faq) + chunk_policy(policy) + chunk_products(products)
    texts = [d["text"] for d in docs]
    metadatas = [d["metadata"] for d in docs]

    embeddings = get_embeddings(texts)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    faiss.write_index(index, "embeddings/faiss_index.bin")
    with open("embeddings/metadata.pkl", "wb") as f:
        pickle.dump(metadatas, f)
