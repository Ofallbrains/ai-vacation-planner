from app.rag.rag_service import retrieve_context


query = "What are some quiet places in Paris?"

context = retrieve_context(query)

print("\n--- RETRIEVED CONTEXT ---")
print(context)