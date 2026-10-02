from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def embed_text(text: str) -> list[float]:
    """
    Convert a piece of text into an embedding vector.
    """

    embedding = model.encode(text)

    return embedding.tolist()


def embed_documents(documents: list[str]) -> list[list[float]]:
    """
    Convert multiple documents into embedding vectors.
    """

    embeddings = model.encode(documents)

    return embeddings.tolist()