from unittest.mock import patch

import pytest

from app.services.ai_itinerary_service import generate_itinerary


def test_generation_rejects_incomplete_itinerary():

    fake_response = {
        "days": [
            {
                "day": 1,
                "activities": ["Visit Nairobi National Park"],
            }
        ]
    }

    with patch(
        "app.services.ai_itinerary_service.run_agent",
        return_value=fake_response,
    ):
        with pytest.raises(ValueError, match="evaluation failed"):
            generate_itinerary(
                destination="Nairobi",
                days=3,
                budget=500,
                travel_style="Adventure",
            )