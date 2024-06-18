import json

with open("flags.json") as f:
    data = json.load(f)


def get_flag(country_name: str):
    return next(
        (country["emoji"] for country in data if country["name"] == country_name), None
    )
