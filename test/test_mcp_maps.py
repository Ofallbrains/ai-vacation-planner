import asyncio
from app.mcp.client import get_route_from_mcp

def test_mcp_maps():
    result = asyncio.run(
        get_route_from_mcp(
            "Kigali, Rwanda",
            "Musanze, Rwanda",
        )
    )
    
    print("\nMCP MAPS RESULT:")
    print(result)
    
    assert result is not None