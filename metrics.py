import json
import os


os.makedirs("logs/performance", exist_ok=True)
os.makedirs("logs/responses", exist_ok=True)


def log_performance(data):
    path = "logs/performance/performance.log"

    with open(path, "a", encoding="utf-8") as file:
        file.write(
            json.dumps(
                data,
                ensure_ascii=False
            ) + "\n"
        )


def log_response(data):
    path = "logs/responses/responses.log"

    with open(path, "a", encoding="utf-8") as file:
        file.write(
            json.dumps(
                data,
                ensure_ascii=False
            ) + "\n"
        )