from temporalio.client import Client
from fastmcp import FastMCP
from workflow import GetForecast

# Initialize FastMCP server
mcp = FastMCP("weather")

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get weather forecast for a location.

    Args:
        latitude: Latitude of the location
        longitude: Longitude of the location
    """
    client = await Client.connect("localhost:7233")
    handle = await client.start_workflow(
        GetForecast,
        args=[latitude, longitude],
        id=f"forecast-{latitude}-{longitude}",
        task_queue="weather-task-queue",
    )
    return await handle.result()

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')