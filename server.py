from typing import Any
import os
import json
import httpx
from fastmcp import FastMCP
from starlette.responses import JSONResponse

print("Starting weather service...")

# Optional auth via env var (recommended for remote)
AUTH_TOKEN = os.environ.get("MCP_AUTH_TOKEN")

mcp = FastMCP("weather")

api_base = "https://api.open-meteo.com/v1"
user_agent = "weather-app/1.0"


async def make_openmeteo_request(url: str) -> dict[str, Any] | None:
    headers = {
        "User-Agent": user_agent,
        "Accept": "application/json",
    }
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error {e.response.status_code}")
        return None
    except Exception as e:
        print(f"Request failed: {e}")
        return None


@mcp.tool
async def get_current_weather(latitude: float, longitude: float) -> str:
    """
    Get current weather for a location.

    Args:
      latitude: Latitude of the location
      longitude: Longitude of the location

    Returns:
      str: JSON string with current weather data
    """
    url = (
        f"{api_base}/forecast?latitude={latitude}&longitude={longitude}"
        "&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code"
    )
    data = await make_openmeteo_request(url)
    if not data:
        return "Unable to fetch weather data."
    return json.dumps(data, indent=2)


@mcp.tool
async def get_forecast(latitude: float, longitude: float) -> str:
    """
    Get weather forecast for a location.

    Args:
      latitude: Latitude of the location
      longitude: Longitude of the location

    Returns:
      str: Formatted weather forecast
    """
    url = (
        f"{api_base}/forecast?latitude={latitude}&longitude={longitude}"
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,weather_code&timezone=auto"
    )
    data = await make_openmeteo_request(url)
    if not data:
        return "Unable to fetch forecast data."

    daily = data.get("daily", {}) or {}
    days = len(daily.get("time", []))
    parts = []
    for i in range(days):
        parts.append(
            f"Date: {daily['time'][i]}\n"
            f"Max Temperature: {daily['temperature_2m_max'][i]}°C\n"
            f"Min Temperature: {daily['temperature_2m_min'][i]}°C\n"
            f"Precipitation: {daily['precipitation_sum'][i]} mm"
        )
    return "\n---\n".join(parts)


# Simple health endpoint for Docker/GCP checks
@mcp.custom_route("/health", methods=["GET"])
async def health_check(_request):
    return JSONResponse({"status": "healthy", "service": "weather-mcp"})


# Run as HTTP (remote MCP) instead of stdio
if __name__ == "__main__":
    # Expose on 0.0.0.0 so Docker/GCP can reach it, default port 8000
    # MCP endpoint will be served at http://<host>:8000/mcp/
    mcp.run(transport="http", host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
