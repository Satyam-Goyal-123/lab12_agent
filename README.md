# 🤖 Lab 12 – LLM Agent Development (Streamlit)

This repository contains two Streamlit-based LLM agents.

---

## ✈ Trip Planner Agent
LLM-powered assistant for trip planning.

**Run**
```bash
streamlit run app.py
```

---

## 💱 Currency & Stock Market Agent
Provides currency + exchange rates + stock index data.

**Run**
```bash
streamlit run finance_agent.py
```

---

## 🛠 Tech Stack
Python • Streamlit • OpenRouter • ExchangeRate API • yfinance

---

## 📦 Setup

```bash
git clone https://github.com/Satyam-Goyal-123/lab12_agent.git
cd lab12_agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🔑 API Keys

Create `.streamlit/secrets.toml`

```toml
OPENROUTER_KEY = "your_key"
EXCHANGE_RATE_KEY = "your_key"
```

---

## ▶ Run Apps

```bash
streamlit run app.py
streamlit run finance_agent.py
```
