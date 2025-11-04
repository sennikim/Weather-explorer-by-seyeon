# app.py
# Arts & Advanced Big Data - Week 10
# Open API Project: "Weather Explorer by Seyeon (Final)"
# Author: Kim Seyeon

import streamlit as st
import requests
import datetime
import random

# -------------------------------
# 🌈 Page Config
# -------------------------------
st.set_page_config(page_title="Weather Explorer by Seyeon", page_icon="🌦️", layout="centered")

st.markdown("""
<style>
h1, h2, h3, h4 {font-family: 'Didot', serif;}
body {background-color: #f5f3f0; font-family: 'Helvetica'; color: #333;}
hr {border: none; border-top: 2px solid #e3d6c4;}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# 🖼️ Title Section
# -------------------------------
st.title("🌦️ *Weather Explorer by Seyeon*")
st.markdown("### Where data meets emotion — explore the poetry of the atmosphere ☁️")
st.write("This app transforms real-time weather data into an artistic, color-based poster experience.")

st.divider()

# -------------------------------
# 🔑 API Key Input (직접 입력 가능)
# -------------------------------
st.subheader("🔑 Enter your OpenWeatherMap API Key")
api_input = st.text_input("Paste your API Key here (https://openweathermap.org/api)", type="password")

# -------------------------------
# 🌍 City Input
# -------------------------------
st.subheader("🏙️ Enter a City")
CITY = st.text_input("City name (e.g., Seoul, Paris, New York)", "Seoul")

# -------------------------------
# 🌤️ Fetch Weather
# -------------------------------
if st.button("Show Weather Poster 🎨"):
    if not api_input:
        st.error("⚠️ Please enter your OpenWeatherMap API key first!")
    else:
        try:
            URL = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={api_input}&units=metric"
            response = requests.get(URL)
            if response.status_code == 200:
                data = response.json()
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                weather = data["weather"][0]["main"]
                time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

                # 🎨 색상 및 무드 매핑
                if "Rain" in weather:
                    bg_color = "#6CA6CD"; mood = "melancholy & calm"
                elif "Cloud" in weather:
                    bg_color = "#B0C4DE"; mood = "serene & thoughtful"
                elif "Clear" in weather:
                    bg_color = "#FFD700"; mood = "bright & inspiring"
                elif "Snow" in weather:
                    bg_color = "#E0FFFF"; mood = "pure & tranquil"
                else:
                    bg_color = "#87CEFA"; mood = "open & refreshing"

                # 🌈 비주얼 포스터
                st.markdown(
                    f"""
                    <div style="background-color:{bg_color};
                                padding:50px;
                                border-radius:25px;
                                text-align:center;
                                color:white;
                                box-shadow:0 4px 20px rgba(0,0,0,0.2);">
                        <h1 style="font-size:42px;">{CITY.title()}</h1>
                        <h2 style="font-size:30px;">{weather}</h2>
                        <p style="font-size:24px;">🌡️ {temp:.1f}°C | 💧 {humidity}%</p>
                        <hr>
                        <p style="font-size:18px;">Mood: <b>{mood}</b></p>
                        <p style="font-size:14px;">Updated at {time_now}</p>
                    </div>
                    """, unsafe_allow_html=True
                )

                # ✨ 예술적 문구
                phrases = [
                    "“Every weather carries its own poetry.”",
                    "“The sky whispers in colors.”",
                    "“Let the wind paint your thoughts.”",
                    "“Some days, the air hums in gold.”"
                ]
                st.markdown(
                    f"<p style='text-align:center; color:#666; font-style:italic;'>{random.choice(phrases)}</p>",
                    unsafe_allow_html=True,
                )

            else:
                st.error("⚠️ Could not find that city. Please check the spelling or API key.")
        except Exception as e:
            st.error(f"⚠️ An error occurred: {e}")
