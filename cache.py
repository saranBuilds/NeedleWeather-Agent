import json
import os


CACHE_FILE = "city_cache.json"


def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(cache):
    with open(CACHE_FILE, "w", encoding="utf-8") as file:
        json.dump(
            cache,
            file,
            indent=4,
            ensure_ascii=False
        )


def normalize_city(city):
    return city.strip().lower()


def get_cached_city(city):
    cache = load_cache()

    city_key = normalize_city(city)

    return cache.get(city_key)


def add_city(city, latitude, longitude):
    cache = load_cache()

    city_key = normalize_city(city)

    cache[city_key] = {
        "city": city.title(),
        "latitude": latitude,
        "longitude": longitude
    }

    save_cache(cache)

    return cache[city_key]