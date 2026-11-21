from app.agents.travel_agent import run_agent
from app.schemas.ai_response import AIItineraryResponse


def generate_itinerary(
    destination: str,
    days: int,
    budget: float,
    travel_style: str,
) -> AIItineraryResponse:
    
    user_request = f"""
    Create a {days}-day travel itinerary for {destination}.

    Trip details:
    - Destination: {destination}
    - Number of days: {days}
    - Budget: {budget}
    - Travel style: {travel_style}

    Use the available travel tools to improve the itinerary.

    In particular:
    - Use weather information when it is relevant.
    - Use the travel knowledge base for destination-specific
      attractions, neighborhoods, food recommendations, and local tips.
    - Consider the weather when selecting activities.
    - Consider the budget and travel style.

    Return an itinerary for exactly {days} days.
    """

    return run_agent(user_request)