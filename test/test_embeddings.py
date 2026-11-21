from app.rag.embeddings import embed_text


text = "Canal Saint-Martin is a quieter area in Paris."

embedding = embed_text(text)

print("Embedding length:", len(embedding))
print("First 10 values:", embedding[:10])