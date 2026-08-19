from mcp.server.fastmcp import FastMCP
import os
import requests
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.environ.get("PORT", 8000))
mcp_app = FastMCP(name="WeatherBot", host="0.0.0.0", port=PORT, stateless_http=True)


OPENWEATHER_API = os.getenv("OPENWEATHER_API_KEY")

@mcp_app.tool() # to make it tool of the server, no more just python function
def get_current_weather(city: str):
    """
    This function fetches the current weather data for a given city using the OpenWeatherMap API. It returns a dictionary containing the city name, temperature in Celsius, feels like temperature, humidity, weather condition description, and wind speed.
    """
    if not OPENWEATHER_API:
        return {"error": "OPENWEATHER_API_KEY is not configured."}

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API}&units=metric"
    response = requests.get(url, timeout=10)

    data = response.json()
    if response.status_code != 200:
        return data
    
    return {
        "city": data["name"],
        "temperature_C": data["main"]["temp"],
        "feels_like_C": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"],
        "wind_speed": data["wind"]["speed"]
    }

@mcp_app.tool()
def get_weather_forecast(city: str):
    """
    This function fetches the weather forecast for a given city using the OpenWeatherMap API. It returns the first 5 forecast entries, including the date and time, temperature, and weather description.
    """
    if not OPENWEATHER_API:
        return {"error": "OPENWEATHER_API_KEY is not configured."}

    url = ("https://api.openweathermap.org/data/2.5/forecast")
    params = {
        "q": city,
        "appid": OPENWEATHER_API,
        "units": "metric"
    }

    response = requests.get(
        url=url,
        params=params,
        timeout=10
    )

    data = response.json()
    if response.status_code != 200:
        return data

    forecast = []

    # Return first 5 forecast entries
    for item in data["list"][:5]:
        forecast.append({
            "datetime": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "weather": item["weather"][0]["description"]
        })
    
    return {
        "city": city,
        "forecast": forecast
    }


if __name__ == "__main__":
    mcp_app.run(transport="streamable-http")  # or "sse", "websocket", "http"
