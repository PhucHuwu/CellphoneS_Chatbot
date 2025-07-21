from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


def get_embeddings(texts):
    return normalize(model.encode(texts, show_progress_bar=True))
