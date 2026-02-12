import streamlit as st
import requests
import os

OPENROUTER_KEY = st.secrets["OPENROUTER_KEY"]
OPENWEATHER_KEY = os.getenv("OPENWEATHER_API_KEY")

def ask_llm(prompt):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3.1-8b-instruct",
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )

    data = response.json()
    return data['choices'][0]['message']['content']

def get_weather(city):
    if not OPENWEATHER_KEY:
        return "Weather API key not found"

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_KEY}&units=metric"
    r = requests.get(url).json()

    if "main" in r:
        return f"{r['main']['temp']}°C, {r['weather'][0]['description']}"

    return "Weather data not available"

st.title("Trip Planner Agent ✈️")

user_input = st.text_input("Enter your trip request")

if st.button("Plan Trip"):

    if not user_input:
        st.warning("Please enter a prompt")
    else:
        city = user_input.split("to")[-1].strip().split(" ")[0]

        weather = get_weather(city)

        prompt = f"""
        Plan a trip based on: {user_input}

        Include:
        - Cultural & historical overview
        - Suggested itinerary
        - Sample flight options
        - Sample hotel options
        """

        answer = ask_llm(prompt)

        st.subheader("Trip Plan")
        st.write(answer)

        st.subheader("Current Weather")
        st.write(weather)
