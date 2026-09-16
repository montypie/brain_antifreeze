import pandas as pd
import plotly.graph_objects as go
import requests
from plotly.subplots import make_subplots

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


def to_dataframe(data):
    df = pd.DataFrame(data["daily"])
    df["time"] = pd.to_datetime(df["time"])
    df = df.rename(
        columns={
            "time": "date",
            "temperature_2m_max": "temp_max",
            "temperature_2m_min": "temp_min",
            "precipitation_sum": "precipitation",
            "surface_pressure_mean": "pressure",
        }
    )
    return df


def create_figure(df):
    df = df.copy()
    df["pressure_kpa"] = df["pressure"] / 10  # hPa -> kPa

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.07,
        row_heights=[0.4, 0.3, 0.3],
        subplot_titles=("Temperature (°C)", "Precipitation (mm)", "Pressure (kPa)"),
    )

    # Temperature band (max line invisible, min line fills up to it)
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["temp_max"],
            mode="lines",
            line=dict(color="red", width=2),
            showlegend=False,
            name="Max",
        ),
        row=1,
        col=1,
    )
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["temp_min"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(255,127,14,0.3)",
            showlegend=False,
            name="Min",
        ),
        row=1,
        col=1,
    )

    # Precipitation bars
    fig.add_trace(
        go.Bar(
            x=df["date"],
            y=df["precipitation"],
            marker_color="steelblue",
            showlegend=False,
            name="Precipitation",
        ),
        row=2,
        col=1,
    )

    # Pressure line
    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["pressure_kpa"],
            mode="lines+markers",
            line=dict(color="purple", width=2),
            showlegend=False,
            name="Pressure",
        ),
        row=3,
        col=1,
    )

    fig.update_yaxes(title_text="°C", row=1, col=1)
    fig.update_yaxes(title_text="mm", row=2, col=1)
    fig.update_yaxes(title_text="kPa", row=3, col=1)

    fig.update_xaxes(showticklabels=True, row=1, col=1)
    fig.update_xaxes(showticklabels=True, row=2, col=1)
    fig.update_xaxes(showticklabels=True, row=3, col=1)

    fig.update_layout(height=800, margin=dict(t=40, b=40))
    return fig


if __name__ == "__main__":
    data = fetch_weather_data(latitude=50.88, longitude=4.70)
    df = to_dataframe(data)
    fig = create_figure(df)
    fig.show()
