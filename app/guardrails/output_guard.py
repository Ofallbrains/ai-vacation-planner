
from pydantic import ValidationError

from app.schemas.ai_response import AIItineraryResponse


class OutputGuardError(ValueError):
    """Raised when an AI response fails output validation."""


def validate_ai_output(response) -> AIItineraryResponse:
    """
    Validate AI-generated itinerary before returning or saving it.
    """

    # 1. Validate the response against our Pydantic schema
    try:
        itinerary = AIItineraryResponse.model_validate(response)

    except (ValidationError, TypeError, ValueError) as error:
        raise OutputGuardError(
            f"AI generated an invalid itinerary: {error}"
        ) from error

    # 2. Ensure the itinerary contains days
    if not itinerary.days:
        raise OutputGuardError(
            "AI generated an itinerary without any days."
        )

    # 3. Ensure every day has activities
    for day in itinerary.days:

        if not day.activities:
            raise OutputGuardError(
                f"Day {day.day} contains no activities."
            )

        # 4. Reject empty activity descriptions
        for activity in day.activities:

            if not activity.strip():
                raise OutputGuardError(
                    f"Day {day.day} contains an empty activity."
                )

    return itinerary
