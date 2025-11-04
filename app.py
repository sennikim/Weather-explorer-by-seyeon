# app.py
# Arts & Advanced Big Data - Week 10
# Open API Project: Weather Explorer by Seyeon (Interactive Map Ver.)
# Author: Kim Seyeon

import streamlit as st
import requests
import datetime
import random
import pandas as pd

# -------------------------------
# 🌈 Page Config
# -------------------------------
st.set_page_config(page_title="Weather Explorer by Seyeon", page_icon="🌦️", layout="wide")

st.markdown("""
<style>
body {background-color: #faf8f5; font-family: 'Helvetica'; color: #333;}
h1 {font-family: 'Didot'; font-size: 42px;}
hr {border: none; border-top: 2px solid #e3d6c4;}
.city-card {background-color: #fff6e6; border-radius: 15px; padding: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🖼️ Title
# -------------------------------
st.title("🌦️ *Weather Explorer by Seyeon*")
st.markdown("### Experience the atmosphere — visually, emotionally, artistically ☁️")
st.write("Select a city or tap on the map to explore its weather mood and artistic palette.")

st.divider()

# -------------------------------
# 🌍 City Selector & Map
# -------------------------------
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
    city = st.selectbox("Select a city:", list(cities.keys()))
    lat, lon = cities[city]

    # 지도 표시
    df = pd.DataFrame([[lat, lon]], columns=["lat", "lon"])
    st.map(df, zoom=3, use_container_width=True)

with col2:
    st.subheader(f"🌍 Current Weather: {city}")
    API_KEY = st.secrets["OPENWEATHER_KEY"]
    URL = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    res = requests.get(URL)
    data = res.json()

    if res.status_code == 200:
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        weather = data["weather"][0]["main"]
        desc = data["weather"][0]["description"].capitalize()
        time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # 🎨 색상 매핑
        if "Rain" in weather:
            color = "#6CA6CD"; mood = "Melancholy & calm"
        elif "Cloud" in weather:
            color = "#B0C4DE"; mood = "Serene & reflective"
        elif "Clear" in weather:
            color = "#FFD700"; mood = "Bright & uplifting"
        elif "Snow" in weather:
            color = "#E0FFFF"; mood = "Pure & tranquil"
        else:
            color = "#87CEFA"; mood = "Open & refreshing"

        # 🌈 Poster Layout
        st.markdown(
            f"""
            <div class="city-card" style="background-color:{color}; text-align:center; color:white;">
                <h2>{city}</h2>
                <h3>{weather} ({desc})</h3>
                <p>🌡️ {temp:.1f}°C | 💧 {humidity}%</p>
                <hr>
                <p><b>Mood:</b> {mood}</p>
                <p style="font-size:12px;">Updated at {time_now}</p>
            </div>
            """, unsafe_allow_html=True,
        )

        # 🌸 감성 문구
        quotes = [
            "“The sky paints emotions we cannot name.”",
            "“Each breeze carries a story untold.”",
            "“Every shade of sunlight is a memory.”",
            "“Rain falls, and the earth listens.”"
        ]
        st.markdown(f"<p style='text-align:center; color:#555; font-style:italic;'>{random.choice(quotes)}</p>", unsafe_allow_html=True)
    else:
        st.error("⚠️ Failed to retrieve weather data.")
