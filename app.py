# app.py
# Arts & Advanced Big Data - Week 10
# Open API Project: Weather Explorer by Seyeon (No API Key, Open-Meteo)
# Author: Kim Seyeon

import streamlit as st
import requests
import datetime
import random
import pandas as pd

# ---------------------------------
# 🌈 Page Config & Styles
# ---------------------------------
st.set_page_config(page_title="Weather Explorer by Seyeon", page_icon="🌦️", layout="wide")
st.markdown("""
<style>
body {background-color: #faf8f5; font-family: 'Helvetica'; color: #333;}
h1 {font-family: 'Didot'; font-size: 42px;}
hr {border: none; border-top: 2px solid #e3d6c4;}
.city-card {background-color: #fff6e6; border-radius: 18px; padding: 24px; box-shadow: 0 6px 24px rgba(0,0,0,0.08);}
</style>
""", unsafe_allow_html=True)

# ---------------------------------
# 🖼️ Title
# ---------------------------------
st.title("🌦️ *Weather Explorer by Seyeon*")
st.markdown("### Key-free weather art using the Open‑Meteo API (no API key required)")
st.write("Select a city or type any city name. The app fetches current weather and renders an artistic poster.")

st.divider()

# ---------------------------------
# 🗺️ City selection + custom search
# ---------------------------------
col1, col2 = st.columns([1, 2])
with col1:
    st.subheader("🏙️ Choose a City")
    cities = {
        "Seoul": (37.5665, 126.9780),
        "Paris": (48.8566, 2.3522),
        "New York": (40.7128, -74.0060),
        "Tokyo": (35.6895, 139.6917),
        "London": (51.5072, -0.1276),
        "Los Angeles": (34.0522, -118.2437),
        "Dubai": (25.276987, 55.296249)
    }
    city_choice = st.selectbox("Select a city:", list(cities.keys()))
    custom_city = st.text_input("…or type another city (press Enter)", "")

    if custom_city.strip():
        # Geocode with Open-Meteo (no key)
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={custom_city.strip()}&count=1&language=en&format=json"
        geo_res = requests.get(geo_url, timeout=10)
        if geo_res.status_code == 200 and geo_res.json().get("results"):
            lat = geo_res.json()["results"][0]["latitude"]
            lon = geo_res.json()["results"][0]["longitude"]
            city_label = geo_res.json()["results"][0]["name"]
        else:
            st.error("Could not find that city. Try another name or use the dropdown.")
            lat, lon = cities[city_choice]
            city_label = city_choice
    else:
        lat, lon = cities[city_choice]
        city_label = city_choice

    df = pd.DataFrame([[lat, lon]], columns=["lat", "lon"])
    st.map(df, zoom=3, use_container_width=True)

with col2:
    st.subheader(f"🌍 Current Weather: {city_label}")
    # Open-Meteo current weather (no API key)
    meteo_url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current=temperature_2m,relative_humidity_2m,precipitation,weather_code,wind_speed_10m"
        "&timezone=auto"
    )
    res = requests.get(meteo_url, timeout=15)
    if res.status_code != 200:
        st.error("⚠️ Failed to retrieve weather data.")
    else:
        j = res.json()
        current = j.get("current", {})
        temp = current.get("temperature_2m", None)
        humidity = current.get("relative_humidity_2m", None)
        precip = current.get("precipitation", None)
        wcode = current.get("weather_code", None)
        wind = current.get("wind_speed_10m", None)
        time_now = current.get("time", datetime.datetime.now().isoformat())

        # Map Open-Meteo WMO weather codes to text
        code_map = {
            0: "Clear sky",
            1: "Mainly clear",
            2: "Partly cloudy",
            3: "Overcast",
            45: "Fog",
            48: "Depositing rime fog",
            51: "Light drizzle",
            53: "Moderate drizzle",
            55: "Dense drizzle",
            56: "Freezing drizzle (light)",
            57: "Freezing drizzle (dense)",
            61: "Slight rain",
            63: "Moderate rain",
            65: "Heavy rain",
            66: "Freezing rain (light)",
            67: "Freezing rain (heavy)",
            71: "Slight snow fall",
            73: "Moderate snow fall",
            75: "Heavy snow fall",
            77: "Snow grains",
            80: "Rain showers (slight)",
            81: "Rain showers (moderate)",
            82: "Rain showers (violent)",
            85: "Snow showers (slight)",
            86: "Snow showers (heavy)",
            95: "Thunderstorm (slight or moderate)",
            96: "Thunderstorm with slight hail",
            99: "Thunderstorm with heavy hail"
        }
        weather_text = code_map.get(wcode, "Unknown")

        # Mood & color mapping
        if wcode in [61,63,65,80,81,82]:
            color = "#6CA6CD"; mood = "Melancholy & calm"
        elif wcode in [1,2,3,45,48]:
            color = "#B0C4DE"; mood = "Serene & reflective"
        elif wcode in [0]:
            color = "#FFD700"; mood = "Bright & uplifting"
        elif wcode in [71,73,75,77,85,86]:
            color = "#E0FFFF"; mood = "Pure & tranquil"
        elif wcode in [95,96,99]:
            color = "#7b68ee"; mood = "Dramatic & electric"
        else:
            color = "#87CEFA"; mood = "Open & refreshing"

        st.markdown(
            f"""
            <div class="city-card" style="background-color:{color}; text-align:center; color:white;">
                <h2>{city_label}</h2>
                <h3>{weather_text}</h3>
                <p>🌡️ {temp if temp is not None else '—'}°C |
                   💧 {humidity if humidity is not None else '—'}% |
                   🌧 {precip if precip is not None else '—'} mm |
                   💨 {wind if wind is not None else '—'} m/s</p>
                <hr>
                <p><b>Mood:</b> {mood}</p>
                <p style="font-size:12px;">Updated at {time_now}</p>
            </div>
            """, unsafe_allow_html=True
        )

        quotes = [
            "“The sky paints emotions we cannot name.”",
            "“Each breeze carries a story untold.”",
            "“Every shade of sunlight is a memory.”",
            "“Rain falls, and the earth listens.”"
        ]
        st.markdown(f"<p style='text-align:center; color:#555; font-style:italic;'>{random.choice(quotes)}</p>", unsafe_allow_html=True)
