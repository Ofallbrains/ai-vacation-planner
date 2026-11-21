import logging
import time

from app.agents.travel_agent import run_agent
from app.evaluation.evaluator import evaluate_itinerary
from app.schemas.ai_response import AIItineraryResponse
from app.guardrails.input_guard import validate_trip_input
from app.guardrails.output_guard import validate_ai_output

logger = logging.getLogger(__name__)


def generate_itinerary(
    destination: str,
    days: int,
    budget: float,
    travel_style: str,
) -> AIItineraryResponse:

    start_time = time.perf_counter()

    logger.info(
        "Itinerary generation started | destination=%s | days=%s",
        destination,
        days,
    )

    try:
        validate_trip_input(
            destination=destination,
            days=days,
            budget=budget,
            travel_style=travel_style,
        )

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

        response = run_agent(user_request)

        itinerary = validate_ai_output(response)

        evaluation = evaluate_itinerary(
            response=itinerary,
            expected_days=days,
            destination=destination,
        )

        if not evaluation.accepted:
            raise ValueError(
                f"Itinerary evaluation failed: {evaluation.issues}"
            )

        duration = time.perf_counter() - start_time

        logger.info(
            "Itinerary generation completed | "
            "destination=%s | duration=%.2fs | score=%s",
            destination,
            duration,
            evaluation.score,
        )

        return itinerary

    except Exception:
        duration = time.perf_counter() - start_time

        logger.exception(
            "Itinerary generation failed | destination=%s | duration=%.2fs",
            destination,
            duration,
        )

        raise