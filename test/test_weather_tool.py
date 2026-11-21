from app.tools.weather_tool import get_weather


def test_paris_weather():
    result = get_weather.invoke({
        "destination": "Paris"
    })

    print("\nPARIS WEATHER:")
    print(result)

    assert result["status"] == "success"
    assert result["temperature"] is not None


def test_musanze_weather():
    result = get_weather.invoke({
        "destination": "Musanze"
    })

    print("\nMUSANZE WEATHER:")
    print(result)

    assert result["status"] == "success"
    assert result["temperature"] is not None


def test_dubai_weather():
    result = get_weather.invoke({
        "destination": "Dubai"
    })

    print("\nDUBAI WEATHER:")
    print(result)

    assert result["status"] == "success"
    assert result["temperature"] is not None


def test_maldives_weather():
    result = get_weather.invoke({
        "destination": "Maldives"
    })

    print("\nMALDIVES WEATHER:")
    print(result)

    assert result["status"] == "success"
    assert result["temperature"] is not None