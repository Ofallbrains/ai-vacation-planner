from langchain_core.tools import tool
from app.rag.rag_service import retrieve_context

@tool
def search_travel_knowledge(query: str) -> str:
    """
    Search the travel knowledge base for relebant destination informatiton.
    Use this tool when you need information about attractions,
    neighborhoods, food recommendations, local tips, or other
    destination-specific travel knowledge.
    """
    
    return retrieve_context(
        query=query,
        n_results=3,
    )
    