import streamlit as st
import requests
import yfinance as yf

# Load secrets (works locally + Streamlit Cloud)
OPENROUTER_KEY = st.secrets["OPENROUTER_KEY"]
EXCHANGE_KEY = st.secrets["EXCHANGE_API_KEY"]

# ---------- LLM CALL ----------
def ask_llm(prompt):
    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "meta-llama/llama-3.1-8b-instruct",
            "messages": [{"role": "user", "content": prompt}]
        }
    )

    try:
        data = response.json()
    except Exception:
        return None

    if "choices" not in data:
        return None

    return data['choices'][0]['message']['content']


# ---------- EXCHANGE RATES ----------
def get_exchange_rates(currency_code):
    url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_KEY}/latest/{currency_code}"
    response = requests.get(url)

    try:
        r = response.json()
    except Exception:
        return None

    if "conversion_rates" not in r:
        return None

    rates = r["conversion_rates"]

    return {
        "USD": rates.get("USD"),
        "INR": rates.get("INR"),
        "GBP": rates.get("GBP"),
        "EUR": rates.get("EUR")
    }


# ---------- STOCK INDICES ----------
def get_stock_index(country):
    mapping = {
        "japan": "^N225",
        "india": "^BSESN",
        "us": "^GSPC",
        "united states": "^GSPC",
        "uk": "^FTSE",
        "united kingdom": "^FTSE",
        "china": "000001.SS",
        "south korea": "^KS11"
    }

    ticker = mapping.get(country.lower())

    if not ticker:
        return "Stock index not mapped"

    data = yf.Ticker(ticker).history(period="1d")

    if data.empty:
        return "No market data available"

    return f"{ticker} Latest Close: {round(data['Close'].iloc[-1], 2)}"


# ---------- UI ----------
st.set_page_config(page_title="Currency & Stock Agent", page_icon="💱")

st.title("💱 Currency & Stock Market Agent")

st.write("Enter a country to get its currency, exchange rates, and stock market details.")

country = st.text_input("🌍 Enter Country Name")

if st.button("Get Details"):

    if not country:
        st.warning("Please enter a country name")
    else:
        with st.spinner("Fetching financial data..."):

            currency_info = ask_llm(
                f"What is the official currency of {country}? "
                f"Return in format: Currency Name (CODE)"
            )

            if not currency_info:
                st.error("Failed to fetch currency information")
            else:
                st.subheader(f"🏦 Official Currency of {country}")
                st.success(currency_info)

                currency_code = "USD"
                if "(" in currency_info and ")" in currency_info:
                    currency_code = currency_info.split("(")[-1].split(")")[0].strip()

                rates = get_exchange_rates(currency_code)

                st.subheader("💱 Exchange Rates")

                if rates:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.info(f"1 {currency_code} → USD: {rates['USD']}")
                        st.info(f"1 {currency_code} → INR: {rates['INR']}")

                    with col2:
                        st.info(f"1 {currency_code} → GBP: {rates['GBP']}")
                        st.info(f"1 {currency_code} → EUR: {rates['EUR']}")
                else:
                    st.error("Exchange rate data unavailable")

                st.subheader("📈 Major Stock Market Index")
                st.success(get_stock_index(country))

                st.subheader("📍 Stock Exchange HQ (Google Maps)")
                st.write(f"https://www.google.com/maps/search/{country}+stock+exchange")
