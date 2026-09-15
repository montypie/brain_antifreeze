import requests

# import streamlit as st


def fetch_weather_data(latitude, longitude, past_days=7):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,surface_pressure_mean",
        "past_days": past_days,
        "forecast_days": 0,
        "timezone": "auto",
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    data = fetch_weather_data(latitude=50.88, longitude=4.70)
    print(data.keys())
    print(data["daily"])
