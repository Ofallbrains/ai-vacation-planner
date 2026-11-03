
import pytest

from app.guardrails.output_guard import (
    OutputGuardError,
    validate_ai_output,
)


def test_valid_ai_output():
    response = {
        "days": [
            {"day": 1, "activities": ["Visit Nairobi National Park"]},
            {"day": 2, "activities": ["Explore Nairobi markets"]},
        ]
    }

    result = validate_ai_output(response)

    assert len(result.days) == 2


def test_reject_invalid_structure():
    response = {
        "days": "invalid"
    }

    with pytest.raises(OutputGuardError):
        validate_ai_output(response)


def test_reject_empty_itinerary():
    response = {
        "days": []
    }

    with pytest.raises(OutputGuardError):
        validate_ai_output(response)


def test_reject_day_without_activities():
    response = {
        "days": [
            {"day": 1, "activities": []}
        ]
    }

    with pytest.raises(OutputGuardError):
        validate_ai_output(response)


def test_reject_empty_activity():
    response = {
        "days": [
            {"day": 1, "activities": [""]}
        ]
    }

    with pytest.raises(OutputGuardError):
        validate_ai_output(response)


def test_reject_non_string_activity():
    response = {
        "days": [
            {"day": 1, "activities": [123]}
        ]
    }

    with pytest.raises(OutputGuardError):
        validate_ai_output(response)
