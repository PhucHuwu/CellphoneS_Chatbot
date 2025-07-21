from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize

model = SentenceTransformer("keepitreal/vietnamese-sbert")


def get_embeddings(texts):
    return normalize(model.encode(texts, show_progress_bar=True))
