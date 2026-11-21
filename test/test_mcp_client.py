import asyncio

from app.mcp.client import get_weather_from_mcp


def test_mcp_weather():
    result = asyncio.run(
        get_weather_from_mcp("Kigali")
    )

    print("\nMCP WEATHER RESULT:")
    print(result)

    assert result is not None