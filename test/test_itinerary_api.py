
from unittest.mock import patch


def test_get_missing_itinerary(client, auth_headers):
    response = client.get(
        "/itineraries/9999",
        headers=auth_headers,
    )

    assert response.status_code == 404


def test_itinerary_requires_authentication(client):
    response = client.get("/itineraries/1")

    assert response.status_code == 403


def test_generate_itinerary_endpoint(client, auth_headers):
    fake_result = {
        "trip_id": 1,
        "itinerary": [
            {
                "day": 1,
                "activities": ["Visit Nairobi National Park"],
            }
        ],
        "message": "Itinerary generated successfully",
    }

    with patch(
        "app.routes.itinerary.generate_itinerary_for_trip",
        return_value=fake_result,
    ):
        response = client.post(
            "/itineraries/generate/1",
            headers=auth_headers,
        )

    assert response.status_code == 200
    assert response.json()["trip_id"] == 1
    assert len(response.json()["itinerary"]) == 1
