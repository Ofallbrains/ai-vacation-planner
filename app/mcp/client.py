from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

server_params = StdioServerParameters(
    command="python",
    args=["-m", "app.mcp.travel_server"],
    )

async def get_weather_from_mcp(destination: str):  
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            await session.initialize()
            
            result = await session.call_tool(
                "get_destination_weather",
                {
                    "destination": destination
                }
            )
            
            return result
        
async def get_route_from_mcp(origin: str, destination: str):
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            
            await session.initialize()
            
            result = await session.call_tool(
                "get_route",
                {
                    "origin": origin,
                    "destination": destination,
                },
            )
            
            return result