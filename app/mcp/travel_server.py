import json

from mcp.server import MCPServer
from app.tools.weather_tool import get_weather
from urllib.parse import quote
from urllib.request import Request, urlopen

mcp = MCPServer("Vacation Planner Travel Server")


@mcp.tool()
def get_destination_weather(destination: str) -> dict:
    """Get current weather information for a travel destination."""
    return get_weather.invoke({
        "destination": destination
    })

@mcp.tool()
def get_route(origin: str, destination: str) -> dict:
    """Get driving route information between two places."""

    def geocode(place: str):
        url = (
            "https://nominatim.openstreetmap.org/search"
            f"?q={quote(place)}&format=json&limit=1"
        )

        request = Request(
            url,
            headers={"User-Agent": "AI-Vacation-Planner"},
        )

        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode())

        if not data:
            raise ValueError(f"Could not find location: {place}")

        return float(data[0]["lon"]), float(data[0]["lat"])

    origin_lon, origin_lat = geocode(origin)
    destination_lon, destination_lat = geocode(destination)

    route_url = (
        "https://router.project-osrm.org/route/v1/driving/"
        f"{origin_lon},{origin_lat};"
        f"{destination_lon},{destination_lat}"
        "?overview=false"
    )

    request = Request(
        route_url,
        headers={"User-Agent": "AI-Vacation-Planner"},
    )

    with urlopen(request, timeout=10) as response:
        data = json.loads(response.read().decode())

    if data.get("code") != "Ok":
        raise ValueError("Could not calculate route")

    route = data["routes"][0]

    return {
        "origin": origin,
        "destination": destination,
        "distance_km": round(route["distance"] / 1000, 2),
        "duration_minutes": round(route["duration"] / 60, 1),
        "status": "success",
    }

if __name__ == "__main__":
    mcp.run()