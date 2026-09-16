import requests
from langchain_core.tools import tool


GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


def weather_code_to_description(code: int) -> str:
    """
    Convert Open-Meteo weather codes into readable descriptions.
    """

    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        56: "Light freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        66: "Light freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Moderate snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail",
    }

    return weather_codes.get(code, "Unknown weather condition")


@tool
def get_weather(destination: str) -> dict:
    """
    Get current weather information for any travel destination.

    Use this tool when weather information is relevant to planning
    a trip or choosing travel activities.

    The destination can be a city, region, or country.
    """

    try:
       
        geocoding_response = requests.get(
            GEOCODING_URL,
            params={
                "name": destination,
                "count": 1,
                "language": "en",
                "format": "json",
            },
            timeout=10,
        )

        geocoding_response.raise_for_status()

        location_data = geocoding_response.json()
        locations = location_data.get("results", [])

        if not locations:
            return {
                "destination": destination,
                "status": "unavailable",
                "reason": "Location could not be found.",
            }

        location = locations[0]

        latitude = location["latitude"]
        longitude = location["longitude"]


        weather_response = requests.get(
            WEATHER_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,weather_code",
                "timezone": "auto",
            },
            timeout=10,
        )

        weather_response.raise_for_status()

        weather_data = weather_response.json()
        current = weather_data.get("current", {})

        weather_code = current.get("weather_code")

        return {
            "destination": location.get("name", destination),
            "country": location.get("country"),
            "temperature": current.get("temperature_2m"),
            "temperature_unit": "°C",
            "condition": weather_code_to_description(weather_code),
            "weather_code": weather_code,
            "timezone": weather_data.get("timezone"),
            "status": "success",
            "source": "Open-Meteo",
        }

    except requests.RequestException as exc:
        return {
            "destination": destination,
            "status": "unavailable",
            "reason": f"Weather service request failed: {str(exc)}",
        }

    except Exception as exc:
        return {
            "destination": destination,
            "status": "unavailable",
            "reason": f"Unexpected weather error: {str(exc)}",
        }