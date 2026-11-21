from app.rag.embeddings import embed_text
from app.rag.vector_store import search


def retrieve_context(
    query: str,
    n_results: int = 3,
) -> str:
    """
    Retrieve relevant travel knowledge for a query.
    """

    query_embedding = embed_text(query)

    results = search(
        query_embedding=query_embedding,
        n_results=n_results,
    )

    documents = results.get("documents", [[]])[0]

    if not documents:
        return ""

    context = "\n\n".join(documents)

    return context