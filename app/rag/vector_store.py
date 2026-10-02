import chromadb


CHROMA_PATH = "./chroma_db"

client = chromadb.PersistentClient(
    path=CHROMA_PATH
)

collection = client.get_or_create_collection(
    name="travel_knowledge"
)


def add_documents(
    documents: list[str],
    embeddings: list[list[float]],
    metadatas: list[dict],
):
    """
    Store documents, embeddings, and metadata in ChromaDB.
    """

    ids = [
        f"document_{index}"
        for index in range(len(documents))
    ]

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def search(
    query_embedding: list[float],
    n_results: int = 3,
):
    """
    Search the knowledge base using an embedding.
    """

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
    )

    return results