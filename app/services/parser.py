import json

from pydantic import ValidationError

from app.schemas.ai_response import AIItineraryResponse


def parse_ai_response(response: str) -> AIItineraryResponse:
    """
    Parse Claude response and validate it with Pydantic.
    """

    response = response.strip()

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    try:
        parsed = json.loads(response)

    except json.JSONDecodeError as e:
        raise Exception(
            f"Claude returned invalid JSON.\n\n{e}\n\nResponse:\n{response}"
        )

    try:
        return AIItineraryResponse.model_validate(parsed)

    except ValidationError as e:
        raise Exception(
            f"Claude returned an invalid itinerary.\n\n{e}"
        )