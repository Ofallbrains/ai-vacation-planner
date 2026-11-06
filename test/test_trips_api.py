
def test_create_trip(client, auth_headers):
    response = client.post(
        "/trips/",
        headers=auth_headers,
        json={
            "destination": "Kenya",
            "days": 5,
            "budget": 1500,
            "trip_style": "Adventure",
        },
    )

    assert response.status_code == 200
    assert response.json()["destination"] == "Kenya"


def test_get_user_trips(client, auth_headers):
    client.post(
        "/trips/",
        headers=auth_headers,
        json={
            "destination": "Rwanda",
            "days": 3,
            "budget": 500,
            "trip_style": "Relaxation",
        },
    )

    response = client.get("/trips/", headers=auth_headers)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_single_trip(client, auth_headers):
    created = client.post(
        "/trips/",
        headers=auth_headers,
        json={
            "destination": "Kenya",
            "days": 5,
            "budget": 1500,
            "trip_style": "Adventure",
        },
    )

    trip_id = created.json()["id"]

    response = client.get(
        f"/trips/{trip_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200
    assert response.json()["destination"] == "Kenya"


def test_update_trip(client, auth_headers):
    created = client.post(
        "/trips/",
        headers=auth_headers,
        json={
            "destination": "Kenya",
            "days": 5,
            "budget": 1500,
            "trip_style": "Adventure",
        },
    )

    trip_id = created.json()["id"]

    response = client.put(
        f"/trips/{trip_id}",
        headers=auth_headers,
        json={"destination": "Tanzania"},
    )

    assert response.status_code == 200
    assert response.json()["destination"] == "Tanzania"


def test_delete_trip(client, auth_headers):
    created = client.post(
        "/trips/",
        headers=auth_headers,
        json={
            "destination": "Kenya",
            "days": 5,
            "budget": 1500,
            "trip_style": "Adventure",
        },
    )

    trip_id = created.json()["id"]

    response = client.delete(
        f"/trips/{trip_id}",
        headers=auth_headers,
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/trips/{trip_id}",
        headers=auth_headers,
    )

    assert get_response.status_code == 404


def test_trips_require_authentication(client):
    response = client.get("/trips/")

    assert response.status_code == 403


def test_create_trip_invalid_days(client, auth_headers):
    response = client.post(
        "/trips/",
        headers=auth_headers,
        json={
            "destination": "Kenya",
            "days": 0,
            "budget": 1500,
            "trip_style": "Adventure",
        },
    )

    assert response.status_code == 422
