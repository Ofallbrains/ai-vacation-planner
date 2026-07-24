import json
from anthropic import Anthropic
from pydantic import ValidationError
from app.services.parser import parse_ai_response
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
        lambda : client.messages.create(        
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
        )
    )
    
    result = response.content[0].text
    return parse_ai_response(result)