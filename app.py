import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Maqasid Geopolitical Intelligence", layout="wide")

# CSS untuk gaya professional (HCI)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_stdio=True)

# --- SIDEBAR & API SETUP ---
st.sidebar.title("🛡️ Intelligence Control")
API_KEY = "8e257951f858454abe1ac4528f4a24ee" # NewsAPI Key anda
st.sidebar.info("Projek ini menggabungkan Financial Criminology, Maqasid al-Shariah, & ESG.")

# --- 1. DATA REAL-TIME: PASARAN MINYAK (Sustainability & Geopolitics) ---
def get_oil_price():
    # Brent Crude Oil (Penunjuk utama krisis Iran-US)
    oil = yf.Ticker("BZ=F")
    data = oil.history(period="1d")
    return data['Close'].iloc[-1], data['Close'].iloc[-1] - data['Open'].iloc[-1]

# --- 2. LOGIK PAKAR: ANALISIS MAQASID & JENAYAH KEWANGAN ---
def analyze_integrity(headline):
    h = headline.lower()
    # Skor bermula 100 (Integriti Tinggi)
    score = 100
    risk_label = "Low"
    maqasid_focus = "General"
    
    # Financial Criminology Keywords (Sanctions, Laundering)
    if any(x in h for x in ['sanction', 'freeze', 'blacklist', 'illegal', 'laundering']):
        score -= 40
        risk_label = "HIGH (Financial Crime)"
        maqasid_focus = "Hifz al-Mal (Protection of Wealth)"
        
    # Geopolitical & Social Sustainability (Life/Peace)
    if any(x in h for x in ['war', 'strike', 'attack', 'military', 'conflict', 'nuclear']):
        score -= 50
        risk_label = "CRITICAL (Conflict)"
        maqasid_focus = "Hifz al-Nafs (Protection of Life)"
        
    return score, risk_label, maqasid_focus

# --- 3. DATA REAL-TIME: BERITA GEOPOLITIK ---
def get_geopolitical_news():
    url = f'https://newsapi.org/v2/everything?q=Iran+US+Sanctions+Oil&sortBy=publishedAt&apiKey={API_KEY}'
    response = requests.get(url).json()
    articles = response.get('articles', [])
    
    processed = []
    for art in articles[:15]:
        score, risk, maqasid = analyze_integrity(art['title'])
        processed.append({
            "Time": art['publishedAt'],
            "Source": art['source']['name'],
            "Headline": art['title'],
            "Score": score,
            "Risk_Status": risk,
            "Maqasid_Pillar": maqasid
        })
    return pd.DataFrame(processed)

# --- DASHBOARD UI (HCI) ---
st.title("⚖️ Maqasid-Integrity Geopolitical Radar")
st.write(f"**Live Update:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# Barisan Atas: Metrics
col1, col2, col3 = st.columns(3)
oil_price, oil_change = get_oil_price()

with col1:
    st.metric("Brent Crude Oil (Live)", f"${oil_price:.2f}", f"{oil_change:.2f}")
    st.caption("Penunjuk kestabilan tenaga & ekonomi global")

try:
    df = get_geopolitical_news()
    avg_maqasid = df['Score'].mean()

    with col2:
        st.metric("Global Maqasid Index", f"{avg_maqasid:.1f}/100")
        st.caption("Skor Integriti (Hifz al-Nafs & Hifz al-Mal)")
        
    with col3:
        high_risk_count = len(df[df['Score'] < 70])
        st.metric("Active Risk Alerts", high_risk_count)
        st.caption("Berita berisiko tinggi dikesan")

    # Barisan Kedua: Visualisasi Trend
    st.divider()
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("📈 Geopolitical Integrity Trend")
        fig = px.area(df, x='Time', y='Score', color_discrete_sequence=['#1f77b4'],
                      title="Maqasid Integrity Pulse (Real-Time)")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("📊 ESG & Maqasid Pillar")
        fig_pie = px.pie(df, names='Maqasid_Pillar', hole=0.4,
                         color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Barisan Ketiga: Intelligence Feed (Real Data Table)
    st.subheader("🔍 Financial Intelligence Feed")
    
    # Mewarnakan jadual (HCI)
    def color_risk(val):
        if val < 50: return 'background-color: #ffcccc; color: black'
        elif val < 80: return 'background-color: #fff4cc; color: black'
        else: return 'background-color: #ccffcc; color: black'

    st.dataframe(df.style.applymap(color_risk, subset=['Score']), use_container_width=True)

except Exception as e:
    st.error(f"Gagal menarik data real-time. Sila semak API Key anda. Error: {e}")

# Footer
st.markdown("---")
st.caption("Expert System by [Nama Anda] | Framework: Financial Criminology - Maqasid al-Shariah - HCI - ESG")
