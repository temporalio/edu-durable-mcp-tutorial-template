from temporalio import workflow
from datetime import timedelta

NWS_API_BASE = "https://api.weather.gov"

# Import activities using Temporal's safe import pattern
with workflow.unsafe.imports_passed_through():
    from activities import make_nws_request

@workflow.defn
class GetForecast:
    @workflow.run
    async def run(self, latitude: float, longitude: float) -> str:
        """Get weather forecast for a location.

        Args:
            latitude: Latitude of the location
            longitude: Longitude of the location
        """
        # Step 1: Get the forecast grid endpoint
        points_url = f"{NWS_API_BASE}/points/{latitude},{longitude}"
        points_data = await workflow.execute_activity(
            make_nws_request,
            points_url,
            start_to_close_timeout=timedelta(seconds=40),
        )

        if not points_data:
            return "Unable to fetch forecast data for this location."

        # Optional: Add a delay between calls
        await workflow.sleep(10)

        # Step 2: Get the actual forecast
        forecast_url = points_data["properties"]["forecast"]
        forecast_data = await workflow.execute_activity(
            make_nws_request,
            forecast_url,
            start_to_close_timeout=timedelta(seconds=40),
        )

        if not forecast_data:
            return "Unable to fetch detailed forecast."

        # Format the periods into a readable forecast
        periods = forecast_data["properties"]["periods"]
        forecasts = []
        for period in periods[:5]:  # Only show next 5 periods
            forecast = f"""
{period['name']}:
Temperature: {period['temperature']}°{period['temperatureUnit']}
Wind: {period['windSpeed']} {period['windDirection']}
Forecast: {period['detailedForecast']}
"""
            forecasts.append(forecast)

        return "\n---\n".join(forecasts)