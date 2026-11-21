
def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "newuser@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 201
    assert response.json()["message"] == "User registered successfully"


def test_register_duplicate_user(client):
    user = {
        "email": "duplicate@example.com",
        "password": "Password123!",
    }

    client.post("/auth/register", json=user)

    response = client.post("/auth/register", json=user)

    assert response.status_code == 400


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "email": "login@example.com",
            "password": "Password123!",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "login@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_login_invalid_password(client):
    client.post(
        "/auth/register",
        json={
            "email": "wrong@example.com",
            "password": "Password123!",
        },
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "wrong@example.com",
            "password": "WrongPassword!",
        },
    )

    assert response.status_code == 401


def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "not-an-email",
            "password": "Password123!",
        },
    )

    assert response.status_code == 422
