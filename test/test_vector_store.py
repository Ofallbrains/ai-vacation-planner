from pathlib import Path

from app.rag.chunker import chunk_text
from app.rag.embeddings import (
    embed_documents,
    embed_text,
)
from app.rag.vector_store import (
    add_documents,
    search,
)

knowledge_file = Path("knowledge/paris_guide.txt")

text = knowledge_file.read_text(
    encoding="utf-8"
)

print("Knowledge document loaded.")
print(f"Document length: {len(text)} characters")
chunks = chunk_text(text)
print(f"Created {len(chunks)} chunks.")
embeddings = embed_documents(chunks)
print("Created embeddings.")

metadatas = [
    {
        "destination": "Paris",
        "source": "paris_guide.txt",
    }
    for _ in chunks
]

add_documents(
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadatas,
)

print("Documents added to ChromaDB.")

query = "What are some quiet places in Paris?"
print("\nSearch query:")
print(query)
query_embedding = embed_text(query)

print("Query embedding created.")

results = search(
    query_embedding=query_embedding,
    n_results=3,
)
print("\n--- RETRIEVED RESULTS ---")

for index, document in enumerate(
    results["documents"][0],
    start=1,
):
    print(f"\n--- RESULT {index} ---")
    print(document)

print("\n--- METADATA ---")

for metadata in results["metadatas"][0]:
    print(metadata)