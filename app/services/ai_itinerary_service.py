from anthropic import Anthropic

from app.config import settings
from app.schemas.ai_response import AIItineraryResponse
from app.prompts.itinerary_prompt import (
    SYSTEM_PROMPT,
    build_itinerary_prompt,
)
from app.tools.weather_tool import get_weather
from app.services.state import AIState
from app.services.retry import retry
from app.rag.rag_service import retrieve_context


client = Anthropic(api_key=settings.anthropic_api_key)


def generate_itinerary(
    destination: str,
    days: int,
    budget: float,
    travel_style: str,
) -> AIItineraryResponse:

    weather = get_weather(destination)
    
    query = f"""
    Create a travel itinerary for {destination}.
    The trip is {days} days long.
    The traveler's budget is {budget}.
    The traveler's style is {travel_style}.

    Find relevant attractions, neighborhoods,
    local tips, food recommendations, and
    useful travel information.
    """

    context = retrieve_context(
        query=query,
        n_results=3,
    )

    state = AIState(
        destination=destination,
        days=days,
        budget=budget,
        travel_style=travel_style,
        weather=weather,
        context=context,
    )

    prompt = build_itinerary_prompt(
        destination=state.destination,
        days=state.days,
        budget=state.budget,
        travel_style=state.travel_style,
        weather=state.weather,
        context=state.context,
    )

    response = retry(
        lambda: client.messages.parse(
            model=settings.anthropic_model,
            system=SYSTEM_PROMPT,
            max_tokens=2000,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            output_format=AIItineraryResponse,
        )
    )

    return response.parsed_output