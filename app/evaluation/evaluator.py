
from pydantic import BaseModel, ValidationError

from app.schemas.ai_response import AIItineraryResponse


class EvaluationResult(BaseModel):
    accepted: bool
    score: float
    checks: dict[str, bool]
    issues: list[str]


def evaluate_itinerary(
    response: AIItineraryResponse | dict,
    expected_days: int,
    destination: str,
) -> EvaluationResult:

    checks = {
        "valid_structure": False,
        "correct_day_count": False,
        "sequential_days": False,
        "activities_present": False,
        "destination_relevance": False,
    }

    issues = []

    try:
        itinerary = AIItineraryResponse.model_validate(response)
        checks["valid_structure"] = True

    except (ValidationError, TypeError, ValueError) as error:
        issues.append(f"Invalid itinerary structure: {error}")

        return EvaluationResult(
            accepted=False,
            score=0.0,
            checks=checks,
            issues=issues,
        )

    checks["correct_day_count"] = (
        len(itinerary.days) == expected_days
    )

    if not checks["correct_day_count"]:
        issues.append(
            f"Expected {expected_days} days, "
            f"but received {len(itinerary.days)}."
        )

    actual_days = [day.day for day in itinerary.days]
    expected_sequence = list(range(1, expected_days + 1))

    checks["sequential_days"] = (
        actual_days == expected_sequence
    )

    if not checks["sequential_days"]:
        issues.append(
            f"Invalid day sequence. Expected "
            f"{expected_sequence}, received {actual_days}."
        )

    checks["activities_present"] = all(
        day.activities
        and all(
            isinstance(activity, str) and activity.strip()
            for activity in day.activities
        )
        for day in itinerary.days
    )

    if not checks["activities_present"]:
        issues.append(
            "One or more days have missing or empty activities."
        )

    all_activities = " ".join(
        activity
        for day in itinerary.days
        for activity in day.activities
    ).lower()

    checks["destination_relevance"] = (
        destination.strip().lower() in all_activities
    )

    if not checks["destination_relevance"]:
        issues.append(
            f"The destination '{destination}' "
            "was not mentioned in the itinerary activities."
        )

    passed_checks = sum(checks.values())
    total_checks = len(checks)

    score = (passed_checks / total_checks) * 100

    accepted = all(checks.values())

    return EvaluationResult(
        accepted=accepted,
        score=score,
        checks=checks,
        issues=issues,
    )
