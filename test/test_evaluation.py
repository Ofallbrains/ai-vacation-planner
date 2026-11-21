
from app.evaluation.evaluator import evaluate_itinerary


def test_valid_itinerary():
    response = {
        "days": [
            {"day": 1, "activities": ["Visit Paris museums"]},
            {"day": 2, "activities": ["Explore Paris city"]},
            {"day": 3, "activities": ["Visit Paris parks"]},
        ]
    }

    result = evaluate_itinerary(
        response,
        expected_days=3,
        destination="Paris",
    )

    assert result.accepted is True
    assert result.score == 100.0


def test_incomplete_itinerary():
    response = {
        "days": [
            {"day": 1, "activities": ["Visit Nairobi National Park"]},
            {"day": 2, "activities": ["Explore Nairobi markets"]},
        ]
    }

    result = evaluate_itinerary(
        response,
        expected_days=3,
        destination="Nairobi",
    )

    assert result.accepted is False
    assert result.score < 100


def test_invalid_day_sequence():
    response = {
        "days": [
            {"day": 1, "activities": ["Visit Kigali museums"]},
            {"day": 3, "activities": ["Explore Kigali city"]},
        ]
    }

    result = evaluate_itinerary(
        response,
        expected_days=2,
        destination="Kigali",
    )

    assert result.accepted is False
    assert result.checks["sequential_days"] is False


def test_empty_activities():
    response = {
        "days": [
            {"day": 1, "activities": []},
            {"day": 2, "activities": ["Explore Kigali city"]},
        ]
    }

    result = evaluate_itinerary(
        response,
        expected_days=2,
        destination="Kigali",
    )

    assert result.accepted is False
    assert result.checks["activities_present"] is False


def test_wrong_destination():
    response = {
        "days": [
            {"day": 1, "activities": ["Visit Kigali Genocide Memorial"]},
            {"day": 2, "activities": ["Explore Kigali markets"]},
        ]
    }

    result = evaluate_itinerary(
        response,
        expected_days=2,
        destination="Nairobi",
    )

    assert result.accepted is False
    assert result.checks["destination_relevance"] is False
