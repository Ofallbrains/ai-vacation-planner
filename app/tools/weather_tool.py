WEATHER = {
    "Paris": {
        "temperature": 25,
        "condition": "Sunny"
    },
    "Dubai": {
        "temperature": 39,
        "condition": "Hot"
    },
    "London": {
        "temperature": 18,
        "condition": "Rainy"
    }
}


def get_weather(destination: str):
    weather = WEATHER.get(
        destination,
        {
            "temperature": 22,
            "condition": "Unknown"
        }
    )
    
    return weather.copy()