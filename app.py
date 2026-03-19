import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Maqasid Geopolitical Intelligence", layout="wide")

# CSS untuk gaya professional (HCI) - FIX: unsafe_allow_html
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    [data-testid="stMetricValue"] { font-size: 28px; }
    </style>
    """, unsafe_allow_html=True)

# --- 1. DATA REAL-TIME: PASARAN MINYAK (Sustainability) ---
def get_oil_price():
    try:
        oil = yf.Ticker("BZ=F")
        data = oil.history(period="2d")
        if len(data) >= 2:
            current_price = data['Close'].iloc[-1]
            change = current_price - data['Close'].iloc[-2]
            return current_price, change
        return 0, 0
    except:
        return 0, 0

# --- 2. LOGIK PAKAR: MAQASID & FINANCIAL CRIME ---
def analyze_integrity(headline):
    h = headline.lower()
    score = 100
    risk = "Low"
    pillar = "General"
    
    if any(x in h for x in ['sanction', 'freeze', 'blacklist', 'illegal', 'laundering']):
        score -= 40
        risk = "HIGH (Financial Crime)"
        pillar = "Hifz al-Mal"
        
    if any(x in h for x in ['war', 'strike', 'attack', 'military', 'conflict', 'nuclear']):
        score -= 50
        risk = "CRITICAL (Conflict)"
        pillar = "Hifz al-Nafs"
        
    return score, risk, pillar

# --- 3. DATA REAL-TIME: NEWS ---
def get_news():
    API_KEY = "8e257951f858454abe1ac4528f4a24ee"
    try:
        url = f'https://newsapi.org/v2/everything?q=Iran+US+Sanctions&sortBy=publishedAt&apiKey={API_KEY}'
        response = requests.get(url).json()
        articles = response.get('articles', [])
        processed = []
        for art in articles[:15]:
            s, r, p = analyze_integrity(art['title'])
            processed.append({
                "Time": art['publishedAt'][:10], 
                "Source": art['source']['name'], 
                "Headline": art['title'], 
                "Score": s, 
                "Risk": r, 
                "Pillar": p
            })
        return pd.DataFrame(processed)
    except:
        return pd.DataFrame()

# --- UI STREAMLIT (HCI) ---
st.title("⚖️ Maqasid-Integrity Geopolitical Radar")
st.write(f"**Live Update:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

oil_p, oil_c = get_oil_price()
df = get_news()

if not df.empty:
    c1, c2, c3 = st.columns(3)
    c1.metric("Brent Crude Oil", f"${oil_p:.2f}", f"{oil_c:.2f}")
    c2.metric("Maqasid Index", f"{df['Score'].mean():.1f}")
    c3.metric("High Risk Alerts", len(df[df['Score'] < 70]))

    st.subheader("📈 Trend Integriti Geopolitik")
    fig = px.area(df, x='Time', y='Score', title="Maqasid Integrity Pulse", 
                  color_discrete_sequence=['#1f77b4'])
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔍 Financial Intelligence Feed")
    # Mewarnakan baris mengikut risiko
    def color_risk(val):
        color = '#ffcccc' if val < 50 else '#fff4cc' if val < 80 else '#ccffcc'
        return f'background-color: {color}'

    st.dataframe(df.style.applymap(color_risk, subset=['Score']), use_container_width=True)
else:
    st.warning("Data sedang dikemaskini. Sila tunggu sebentar atau muat semula halaman.")

st.markdown("---")
st.caption("Expertise: Financial Criminology | Islamic Studies | HCI | Corporate Sustainability")
