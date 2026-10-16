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


client = Anthropic(api_key=settings.anthropic_api_key)


def generate_itinerary(
    destination: str,
    days: int,
    budget: float,
    travel_style: str,
) -> AIItineraryResponse:

    weather = get_weather(destination)

    state = AIState(
        destination=destination,
        days=days,
        budget=budget,
        travel_style=travel_style,
        weather=weather,
    )

    prompt = build_itinerary_prompt(
        destination=state.destination,
        days=state.days,
        budget=state.budget,
        travel_style=state.travel_style,
        weather=state.weather,
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