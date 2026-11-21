from pathlib import Path

from app.rag.chunker import chunk_text
from app.rag.embeddings import embed_documents
from app.rag.vector_store import add_documents


KNOWLEDGE_DIR = Path("knowledge")


def ingest_knowledge_base():
    documents = []
    metadatas = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        chunks = chunk_text(text)

        destination = file_path.stem.replace(
            "_guide",
            ""
        ).title()

        for chunk in chunks:
            documents.append(chunk)

            metadatas.append(
                {
                    "destination": destination,
                    "source": file_path.name,
                }
            )

    if not documents:
        print("No knowledge documents found.")
        return

    print(f"Found {len(documents)} chunks.")

    embeddings = embed_documents(documents)

    add_documents(
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print("Knowledge base successfully ingested.")


if __name__ == "__main__":
    ingest_knowledge_base()