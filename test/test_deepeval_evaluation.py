import json
import os
from pathlib import Path

import pytest
from deepeval import assert_test
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase, LLMTestCaseParams

from app.services.ai_itinerary_service import generate_itinerary


# Locate the golden dataset from the project root.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "datasets" / "travel_golden_dataset.json"


def load_golden_dataset():
    with DATASET_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)["cases"]


GOLDEN_CASES = load_golden_dataset()

VALID_CASES = [
    case for case in GOLDEN_CASES
    if not case["expected"].get("must_reject_input")
]


@pytest.mark.parametrize(
    "case",
    VALID_CASES,
    ids=lambda case: case["id"],
)
def test_itinerary_quality_with_deepeval(case):
    # Prevent accidental API calls during ordinary pytest runs.
    if os.getenv("RUN_LIVE_DEEPEVAL") != "1":
        pytest.skip(
            "Set RUN_LIVE_DEEPEVAL=1 to run live DeepEval tests."
        )

    request = case["input"]
    expected = case["expected"]

    # Generate a real itinerary using the project's service.
    itinerary = generate_itinerary(
        destination=request["destination"],
        days=request["days"],
        budget=request["budget"],
        travel_style=request["travel_style"],
    )

    actual_output = itinerary.model_dump_json(indent=2)

    expected_output = (
        f"The itinerary must contain exactly {expected['day_count']} days, "
        f"numbered sequentially from 1. Every day must contain meaningful "
        f"activities for {request['destination']}. The activities should "
        f"respect the {request['travel_style']} travel style and consider "
        f"the budget of {request['budget']}."
    )

    test_case = LLMTestCase(
        input=(
            f"Plan a {request['days']}-day trip to "
            f"{request['destination']}. "
            f"Budget: {request['budget']}. "
            f"Travel style: {request['travel_style']}."
        ),
        actual_output=actual_output,
        expected_output=expected_output,
    )

    itinerary_quality = GEval(
        name="Travel Itinerary Quality",
        criteria=(
            "Evaluate the generated travel itinerary against the user's "
            "request and expected output. Assess destination relevance, "
            "completeness, useful activities, requested duration, budget "
            "awareness, and travel-style alignment. Penalize irrelevant, "
            "vague, or unsupported recommendations. Do not require the "
            "destination's full name to appear verbatim in every activity."
        ),
        evaluation_params=[
            LLMTestCaseParams.INPUT,
            LLMTestCaseParams.ACTUAL_OUTPUT,
            LLMTestCaseParams.EXPECTED_OUTPUT,
        ],
        threshold=0.7,
    )

    assert_test(test_case, [itinerary_quality])