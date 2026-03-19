import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime

# --- 1. RESEARCHER CONFIGURATION ---
st.set_page_config(page_title="Strategic Maqasid Radar | Mohd Khairul Ridhuan", layout="wide")

# Professional Corporate CSS
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .researcher-header {
        background-color: #1a2a6c;
        padding: 30px;
        color: white;
        border-radius: 10px;
        margin-bottom: 25px;
        border-bottom: 5px solid #f2a900;
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. LEAD RESEARCHER PROFILE (SIDEBAR) ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3306/3306613.png", width=100)
st.sidebar.markdown("### **LEAD STRATEGIC RESEARCHER**")
st.sidebar.markdown("#### MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL")
st.sidebar.write("Accredited Financial Criminologist & Geopolitical Risk Strategist")
st.sidebar.markdown("---")
st.sidebar.write("📂 **Research Focus:**")
st.sidebar.caption("- Islamic Financial Integrity\n- Maqasid-ESG Framework\n- Trade-Based Money Laundering (TBML)\n- Geopolitical Supply Chain Risk")

# --- 3. REAL-TIME DATA ENGINE (DYNAMIC DATE) ---
@st.cache_data(ttl=60) # Data refresh setiap 60 saat
def fetch_global_data():
    current_date = datetime.now().strftime('%Y-%m-%d')
    
    # Financial Market Data (Oil)
    oil = yf.Ticker("BZ=F")
    oil_price = oil.history(period="1d")['Close'].iloc[-1]
    
    # News Signals (Today's Data)
    API_KEY = "8e257951f858454abe1ac4528f4a24ee"
    # Query dinamik mengikut tarikh hari ini
    url = f'https://newsapi.org/v2/everything?q=(Iran AND US) OR (Iran AND Israel)&from={current_date}&sortBy=publishedAt&apiKey={API_KEY}'
    
    try:
        articles = requests.get(url).json().get('articles', [])
    except:
        articles = []

    processed = []
    for art in articles[:25]:
        h = art['title'].lower()
        score = 100
        # Expert Analysis Logic
        if any(x in h for x in ['sanction', 'illegal', 'laundering', 'freeze']): score -= 40
        if any(x in h for x in ['war', 'missile', 'strike', 'drone', 'attack']): score -= 60
        
        processed.append({
            "Time": art['publishedAt'][11:16],
            "Headline": art['title'],
            "Source": art['source']['name'],
            "Integrity_Score": max(score, 0)
        })
    return oil_price, pd.DataFrame(processed)

# --- 4. DATA PROCESSING ---
oil_price, df = fetch_global_data()
avg_score = df['Integrity_Score'].mean() if not df.empty else 0

# --- 5. VISUALS: RESEARCH HEADER ---
st.markdown(f"""
    <div class="researcher-header">
        <span style="letter-spacing: 2px; font-size: 14px;">GEOPOLITICAL INTEGRITY RESEARCH UNIT // REAL-TIME MONITOR</span>
        <h1 style="margin: 10px 0;">MAQASID-INTEGRITY STRATEGIC RADAR</h1>
        <p>Lead Researcher: <strong>MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL</strong> | Current Node: 2026-03-19 {datetime.now().strftime('%H:%M:%S')}</p>
    </div>
    """, unsafe_allow_html=True)

# --- 6. TOP ROW: GLOBAL RISK PULSE & GLOBE ---
col_a, col_b = st.columns([1, 1.5])

with col_a:
    st.subheader("🌐 Global Strategic Position")
    # Plotly Globe (Rotating Effect Setup)
    fig_globe = go.Figure(go.Scattergeo(
        lon = [51.3, -77.0, 34.7], # Tehran, DC, Tel Aviv
        lat = [35.6, 38.8, 32.0],
        text = ['Tehran (Conflict Zone)', 'Washington (Sanction Source)', 'Tel Aviv (Tactical Point)'],
        mode = 'markers+text',
        marker = dict(size = 10, color = 'red', symbol = 'circle', line=dict(width=2, color='white'))
    ))
    fig_globe.update_geos(
        projection_type="orthographic",
        showcountries=True, countrycolor="LightGrey",
        showocean=True, oceancolor="AliceBlue",
        center=dict(lat=30, lon=40), # Focus on Middle East
        projection_rotation=dict(lon=datetime.now().second * 6) # Simulasi putaran setiap saat
    )
    fig_globe.update_layout(height=400, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_globe, use_container_width=True)

with col_b:
    st.subheader("📊 Strategic Integrity Metrics")
    k1, k2, k3 = st.columns(3)
    k1.metric("BRENT OIL (USD)", f"${oil_price:.2f}", "LIVE")
    k2.metric("MAQASID RATING", f"{avg_score:.1f}/100")
    k3.metric("WORLD TENSION", "ELEVATED" if avg_score < 75 else "STABLE")

    # Radar Chart: Maqasid 5 Pillars
    categories = ['Life (Nafs)', 'Wealth (Mal)', 'Faith (Din)', 'Intellect (Aql)', 'Lineage (Nasl)']
    # Simulasi data berasaskan skor berita
    values = [avg_score-10, avg_score-20, avg_score, avg_score-5, avg_score-15] 
    
    fig_radar = go.Figure(data=go.Scatterpolar(
      r=values + [values[0]],
      theta=categories + [categories[0]],
      fill='toself',
      line_color='#1a2a6c'
    ))
    fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100])), showlegend=False, height=300, margin=dict(l=40,r=40,t=20,b=20))
    st.plotly_chart(fig_radar, use_container_width=True)

# --- 7. BOTTOM ROW: LIVE RESEARCH FEED ---
st.divider()
st.subheader("📁 Live Research Feed: Anomaly Detection (Iran-US-Israel)")

# Mewarnakan baris table
def color_research(val):
    if val < 50: return 'background-color: #f8d7da; color: #721c24; font-weight: bold;'
    elif val < 80: return 'background-color: #fff3cd; color: #856404;'
    else: return 'background-color: #d4edda; color: #155724;'

if not df.empty:
    st.dataframe(df.style.applymap(color_research, subset=['Integrity_Score']), use_container_width=True)
else:
    st.info("Searching for latest strategic signals...")

# --- FOOTER ---
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; color: #666; font-size: 12px;">
        OFFICIAL RESEARCH DOCUMENT | LEAD RESEARCHER: MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL<br>
        Framework: Financial Criminology (TBML Detection) • Islamic Jurisprudence (Maqasid al-Shariah) • Corporate Sustainability (ESG)
    </div>
    """, unsafe_allow_html=True)
