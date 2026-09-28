import time
from datetime import datetime

import needle

from weather import (
    get_temperature,
    get_humidity,
    get_wind,
    get_weather
)

from metrics import (
    log_performance,
    log_response
)


agent = needle.Needle(
    tools=[
        get_temperature,
        get_humidity,
        get_wind,
        get_weather
    ]
)


def extract_weather_result(result):
    results = result.get("results")

    if not results:
        return None

    if isinstance(results, list):
        for item in results:
            if isinstance(item, dict):
                if item.get("success") is True:
                    return item

    return None


def format_response(result):
    weather = extract_weather_result(result)

    if not weather:
        return str(result)

    if not weather.get("success"):
        return (
            f"Weather error: "
            f"{weather.get('error', 'Unknown error')}"
        )

    tool = weather.get("tool")

    if tool == "get_temperature":
        return (
            f"\nWeather in {weather['city']}\n"
            f"Temperature: {weather['temperature']}°C\n"
            f"Time: {weather['timestamp']}\n"
            f"Timezone: {weather['timezone']}"
        )

    if tool == "get_humidity":
        return (
            f"\nWeather in {weather['city']}\n"
            f"Humidity: {weather['humidity']}%\n"
            f"Time: {weather['timestamp']}\n"
            f"Timezone: {weather['timezone']}"
        )

    if tool == "get_wind":
        return (
            f"\nWeather in {weather['city']}\n"
            f"Wind speed: {weather['wind_speed']} km/h\n"
            f"Time: {weather['timestamp']}\n"
            f"Timezone: {weather['timezone']}"
        )

    if tool == "get_weather":
        return (
            f"\nWeather in {weather['city']}\n"
            f"Temperature: {weather['temperature']}°C\n"
            f"Feels like: {weather['feels_like']}°C\n"
            f"Humidity: {weather['humidity']}%\n"
            f"Wind: {weather['wind_speed']} km/h\n"
            f"Precipitation: {weather['precipitation']} mm\n"
            f"Weather code: {weather['weather_code']}\n"
            f"Time: {weather['timestamp']}\n"
            f"Timezone: {weather['timezone']}"
        )

    return str(weather)


def main():
    print("Needle 3 Weather Agent")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        query = input("\nYou: ").strip()

        if query.lower() in ["exit", "quit"]:
            break

        if not query:
            continue

        request_start = time.perf_counter()

        try:
            result = agent.run(query)

            total_latency = (
                time.perf_counter() - request_start
            )

            timestamp = datetime.now().isoformat()

            weather_result = extract_weather_result(result)

            response_text = format_response(result)

            print(response_text)

            print("\nPerformance")
            print(
                f"Total latency: "
                f"{total_latency:.4f} s"
            )

            print(
                f"Confidence: "
                f"{result.get('confidence')}"
            )

            print(
                f"Prefill TPS: "
                f"{result.get('prefill_tps')}"
            )

            print(
                f"Decode TPS: "
                f"{result.get('decode_tps')}"
            )

            print(
                f"Peak RAM: "
                f"{result.get('peak_ram_mb')} MB"
            )

            if weather_result:
                print(
                    f"Cache hit: "
                    f"{weather_result.get('cache_hit')}"
                )

                print(
                    f"Geocoding latency: "
                    f"{weather_result.get('geocoding_latency')} s"
                )

                print(
                    f"Weather API latency: "
                    f"{weather_result.get('weather_api_latency')} s"
                )

            performance_log = {
                "timestamp": timestamp,
                "query": query,
                "total_latency": round(
                    total_latency,
                    4
                ),
                "confidence": result.get(
                    "confidence"
                ),
                "prefill_tps": result.get(
                    "prefill_tps"
                ),
                "decode_tps": result.get(
                    "decode_tps"
                ),
                "peak_ram_mb": result.get(
                    "peak_ram_mb"
                )
            }

            if weather_result:
                performance_log.update({
                    "tool": weather_result.get(
                        "tool"
                    ),
                    "city": weather_result.get(
                        "city"
                    ),
                    "cache_hit": weather_result.get(
                        "cache_hit"
                    ),
                    "geocoding_latency": weather_result.get(
                        "geocoding_latency"
                    ),
                    "weather_api_latency": weather_result.get(
                        "weather_api_latency"
                    )
                })

            log_performance(
                performance_log
            )

            response_log = {
                "timestamp": timestamp,
                "query": query,
                "response": response_text,
                "success": result.get(
                    "success"
                )
            }

            if weather_result:
                response_log.update({
                    "city": weather_result.get(
                        "city"
                    ),
                    "tool": weather_result.get(
                        "tool"
                    ),
                    "temperature": weather_result.get(
                        "temperature"
                    ),
                    "feels_like": weather_result.get(
                        "feels_like"
                    ),
                    "humidity": weather_result.get(
                        "humidity"
                    ),
                    "wind_speed": weather_result.get(
                        "wind_speed"
                    ),
                    "precipitation": weather_result.get(
                        "precipitation"
                    ),
                    "weather_code": weather_result.get(
                        "weather_code"
                    ),
                    "weather_timestamp": weather_result.get(
                        "timestamp"
                    ),
                    "timezone": weather_result.get(
                        "timezone"
                    )
                })

            log_response(
                response_log
            )

        except Exception as error:
            total_latency = (
                time.perf_counter() - request_start
            )

            timestamp = datetime.now().isoformat()

            print(
                f"\nError: {error}"
            )

            log_performance({
                "timestamp": timestamp,
                "query": query,
                "total_latency": round(
                    total_latency,
                    4
                ),
                "success": False,
                "error": str(error)
            })

            log_response({
                "timestamp": timestamp,
                "query": query,
                "success": False,
                "error": str(error)
            })


if __name__ == "__main__":
    main()