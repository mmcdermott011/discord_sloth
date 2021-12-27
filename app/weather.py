import requests

from auth import WEATHER_KEY
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import pprint
import json
import datetime

base_url = 'https://api.openweathermap.org/data/2.5/'
parameters = {
  'start': '1',
  'limit': '5000',
  'convert': 'USD'
}
headers = {
  'Accepts': 'application/json',
}


CITY_CODES = {

    "San Jose": {
            "id": 5392171,
            "name": "San Jose",
            "state": "CA",
            "country": "US",
            "coord": {
                "lon": -121.894958,
                "lat": 37.33939
            }
    },
    "Long Beach": {
        "id": 5367929,
        "name": "Long Beach",
        "state": "CA",
        "country": "US",
        "coord": {
            "lon": -118.189232,
            "lat": 33.76696
        }
    },
    "Oceanside": {
        "id": 5378771,
        "name": "Oceanside",
        "state": "CA",
        "country": "US",
        "coord": {
            "lon": -117.379478,
            "lat": 33.195869
        }
    },
    "Garden Grove": {
        "id": 5351515,
        "name": "Garden Grove",
        "state": "CA",
        "country": "US",
        "coord": {
            "lon": -117.941452,
            "lat": 33.773911
        }
    }
}


DEFAULT_CITY = "San Jose"
DEFAULT_STATE = "CA"

def _get_city_code(city, state):
    print(f"Getting city code for {city}, {state}")
    retrieved_city = CITY_CODES.get(city)
    if not retrieved_city:
        print("City not in cache, have to look it up")
        with open("../city.list.json") as f:
            cities = json.load(f)
            for item in cities:
                if item.get("name", "") == city and item.get("state", "") == state:
                    print(f"Found city we were looking for: {item}")
                    print("Will cache this city")
                    CITY_CODES[city] = item
                    print(f"Updated cached city code map: {CITY_CODES}")
    if CITY_CODES.get(city):
        return CITY_CODES.get(city).get("id")
    else:
        return None


def get_weather_forecast(**kwargs):
    """gets todays weather forecast for given city"""
    city = kwargs.get("city", DEFAULT_CITY)
    state = kwargs.get("state", DEFAULT_STATE)
    code = _get_city_code(city, state)
    if not code:
        return f"Sorry! Wasn't able to find weather info for {city}, {code}\n"
    url = base_url + f"weather?id={code}&units=imperial&appid={WEATHER_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        json = response.json()
        low_temp = f"{json['main']['temp_min']}F"
        high_temp = f"{json['main']['temp_max']}F"
        humidity = f"{json['main']['humidity']}%"
        desc = json['weather'][0]['description']
        if int(json['main']['humidity']) > 30:
            humidity += " ☂️"
        if int(json['main']['humidity']) >= 60 or "rain" in desc:
            humidity += "🌧️"
        forecast = f"--------- Todays Weather for {city}, {state} ---------\nHigh: {high_temp}\t Low: {low_temp}\tHumidity: {humidity}\n{desc}\n"
        return forecast


if __name__ == "__main__":
    print(get_weather_forecast(city="Escondido", state="CA"))