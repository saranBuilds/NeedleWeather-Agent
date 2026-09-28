import time
import requests

from cache import get_cached_city, add_city

def resolve_city(city):
    city = city.strip()

    cached = get_cached_city(city)

    if cached:
        return {
            "city": cached["city"],
            "latitude": cached["latitude"],
            "longitude": cached["longitude"],
            "cache_hit": True,
            "geocoding_latency": 0.0
        }

    start = time.perf_counter()

    response = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={
            "name": city,
            "count": 1,
            "language": "en",
            "format": "json"
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    geocoding_latency = time.perf_counter() - start

    if not data.get("results"):
        raise ValueError(f"City not found: {city}")

    location = data["results"][0]

    cached_city = add_city(
        location["name"],
        location["latitude"],
        location["longitude"]
    )

    return {
        "city": cached_city["city"],
        "latitude": cached_city["latitude"],
        "longitude": cached_city["longitude"],
        "cache_hit": False,
        "geocoding_latency": round(
            geocoding_latency,
            4
        )
    }

def get_temperature(city: str):
    location = resolve_city(city)

    start = time.perf_counter()

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "temperature_2m",
            "temperature_unit": "celsius",
            "timezone": "auto"
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    weather_api_latency = time.perf_counter() - start

    current = data["current"]

    return {
        "success": True,
        "tool": "get_temperature",
        "city": location["city"],
        "temperature": current["temperature_2m"],
        "unit": "°C",
        "timestamp": current["time"],
        "timezone": data["timezone"],
        "cache_hit": location["cache_hit"],
        "geocoding_latency": round(
            location["geocoding_latency"], 4
        ),
        "weather_api_latency": round(
            weather_api_latency, 4
        )
    }


def get_humidity(city: str):
    location = resolve_city(city)

    start = time.perf_counter()

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "relative_humidity_2m",
            "timezone": "auto"
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    weather_api_latency = time.perf_counter() - start

    current = data["current"]

    return {
        "success": True,
        "tool": "get_humidity",
        "city": location["city"],
        "humidity": current["relative_humidity_2m"],
        "unit": "%",
        "timestamp": current["time"],
        "timezone": data["timezone"],
        "cache_hit": location["cache_hit"],
        "geocoding_latency": round(
            location["geocoding_latency"], 4
        ),
        "weather_api_latency": round(
            weather_api_latency, 4
        )
    }


def get_wind(city: str):
    location = resolve_city(city)

    start = time.perf_counter()

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": "wind_speed_10m",
            "wind_speed_unit": "kmh",
            "timezone": "auto"
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    weather_api_latency = time.perf_counter() - start

    current = data["current"]

    return {
        "success": True,
        "tool": "get_wind",
        "city": location["city"],
        "wind_speed": current["wind_speed_10m"],
        "unit": "km/h",
        "timestamp": current["time"],
        "timezone": data["timezone"],
        "cache_hit": location["cache_hit"],
        "geocoding_latency": round(
            location["geocoding_latency"], 4
        ),
        "weather_api_latency": round(
            weather_api_latency, 4
        )
    }


def get_weather(city: str):
    location = resolve_city(city)

    start = time.perf_counter()

    response = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": location["latitude"],
            "longitude": location["longitude"],
            "current": (
                "temperature_2m,"
                "apparent_temperature,"
                "relative_humidity_2m,"
                "wind_speed_10m,"
                "precipitation,"
                "weather_code"
            ),
            "temperature_unit": "celsius",
            "wind_speed_unit": "kmh",
            "timezone": "auto"
        },
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    weather_api_latency = time.perf_counter() - start

    current = data["current"]

    return {
        "success": True,
        "tool": "get_weather",
        "city": location["city"],
        "temperature": current["temperature_2m"],
        "feels_like": current["apparent_temperature"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "precipitation": current["precipitation"],
        "weather_code": current["weather_code"],
        "timestamp": current["time"],
        "timezone": data["timezone"],
        "cache_hit": location["cache_hit"],
        "geocoding_latency": round(
            location["geocoding_latency"], 4
        ),
        "weather_api_latency": round(
            weather_api_latency, 4
        )
    }