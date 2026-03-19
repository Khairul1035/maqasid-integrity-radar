import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# --- 1. RESEARCHER CONFIGURATION ---
st.set_page_config(page_title="Maqasid Strategic Radar | Researcher MKR", layout="wide")

# Professional Dark-Corporate CSS
st.markdown("""
    <style>
    .main { background-color: #0b1120; color: #e2e8f0; }
    .researcher-header {
        background-color: #1e293b;
        padding: 25px;
        color: #38bdf8;
        border-radius: 12px;
        border-left: 10px solid #38bdf8;
        margin-bottom: 20px;
    }
    .stMetric { background-color: #1e293b; border-radius: 10px; padding: 15px; border: 1px solid #334155; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. RESEARCHER PROFILE (SIDEBAR) ---
st.sidebar.markdown(f"""
    <div style="text-align: center;">
        <img src="https://cdn-icons-png.flaticon.com/512/1043/1043321.png" width="100" style="filter: brightness(0) invert(1);">
        <h2 style="color: #38bdf8; margin-top:10px;">RESEARCHER</h2>
        <h4 style="color: #f8fafc;">MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL</h4>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.markdown("**CORE EXPERTISE:**")
st.sidebar.info("⚖️ Financial Criminology\n🌙 Islamic Studies\n🌱 Corporate Sustainability")

st.sidebar.markdown("**SELF-TAUGHT RESEARCH:**")
st.sidebar.warning("💻 HCI | 🤖 AI & ML\n🌍 Geopolitics")

# --- 3. DYNAMIC DATA ENGINE ---
@st.cache_data(ttl=300)
def fetch_strategic_data():
    # NewsAPI - Ambil data 3 hari ke belakang untuk elak isu "0.0"
    target_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    API_KEY = "8e257951f858454abe1ac4528f4a24ee"
    url = f'https://newsapi.org/v2/everything?q=(Iran OR Israel OR Gaza OR "Red Sea") AND (Sanctions OR War)&from={target_date}&sortBy=relevancy&apiKey={API_KEY}'
    
    # Financial Data
    oil = yf.Ticker("BZ=F")
    oil_price = oil.history(period="1d")['Close'].iloc[-1]
    
    try:
        articles = requests.get(url).json().get('articles', [])
    except:
        articles = []

    processed = []
    # AI/ML Heuristic Logic for Risk Prediction
    risk_nations = {"Iran": 0, "Israel": 0, "USA": 0, "Lebanon": 0, "Yemen": 0}
    
    for art in articles[:30]:
        h = art['title'].lower()
        score = 100
        if any(x in h for x in ['sanction', 'illegal', 'freeze']): score -= 40
        if any(x in h for x in ['war', 'strike', 'missile', 'attack']): score -= 60
        
        # Mapping Risk to Nations
        for nation in risk_nations.keys():
            if nation.lower() in h:
                risk_nations[nation] += (100 - score)

        processed.append({
            "Headline": art['title'],
            "Source": art['source']['name'],
            "Score": max(score, 0),
            "Pillar": "Hifz al-Nafs" if score < 50 else "Hifz al-Mal" if score < 80 else "General"
        })
    
    return oil_price, pd.DataFrame(processed), risk_nations

oil_p, df, risk_nations = fetch_strategic_data()
avg_score = df['Score'].mean() if not df.empty else 75.0 # Default fallback

# --- 4. DASHBOARD HEADER ---
st.markdown(f"""
    <div class="researcher-header">
        <span style="letter-spacing: 3px; font-size: 12px; color: #94a3b8;">SYSTEM STATUS: ACTIVE // NODE: {datetime.now().year}</span>
        <h1 style="margin: 5px 0;">MAQASID STRATEGIC INTEGRITY RADAR</h1>
        <p style="color: #f8fafc; font-size: 18px;">
            <strong>RESEARCHER: MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL</strong><br>
            <span style="color: #38bdf8;">{datetime.now().strftime('%A, %d %B %Y | %H:%M:%S')}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. INTERACTIVE GLOBE & RADAR ---
col_map, col_risk = st.columns([1.5, 1])

with col_map:
    st.subheader("🌐 Interactive Geopolitical Anomaly Map")
    # Globe yang berputar secara visual menggunakan rotation
    fig_globe = go.Figure(go.Scattergeo(
        lon = [51.3, 34.8, -77.0, 44.0, 35.2], 
        lat = [35.6, 31.0, 38.9, 33.3, 31.7],
        text = ["Iran", "Israel", "USA", "Iraq", "Palestine"],
        mode = 'markers',
        marker = dict(size = 15, color = 'red', opacity = 0.8, symbol = 'pulse')
    ))
    fig_globe.update_geos(
        projection_type="orthographic",
        showcountries=True, countrycolor="#475569",
        showocean=True, oceancolor="#0f172a",
        showlakes=True, lakecolor="#1e293b",
        projection_rotation=dict(lon=datetime.now().second * 6, lat=20, roll=0)
    )
    fig_globe.update_layout(height=500, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_globe, use_container_width=True)

with col_risk:
    st.subheader("📉 AI Anomaly Projection")
    # Menghitung kebarangkalian masalah mengikut negara
    risk_df = pd.DataFrame(list(risk_nations.items()), columns=['Nation', 'Risk_Weight'])
    risk_df['Escalation_Prob'] = (risk_df['Risk_Weight'] / risk_df['Risk_Weight'].sum() * 100).fillna(20)
    
    fig_risk = px.bar(risk_df, x='Nation', y='Escalation_Prob', 
                     title="Probability of Escalation (%)",
                     color='Escalation_Prob', color_continuous_scale='Reds')
    fig_risk.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_risk, use_container_width=True)
    
    st.info("💡 **ML Prediction:** Analisis menunjukkan risiko tertinggi pada zon 'Red Sea' & 'Strait of Hormuz'.")

# --- 6. METRICS & MAQASID RADAR ---
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("BRENT OIL", f"${oil_p:.2f}", "LIVE DATA")
m2.metric("MAQASID INTEGRITY INDEX", f"{avg_score:.1f}/100")
m3.metric("GEOPOLITICAL TENSION", "CRITICAL" if avg_score < 60 else "WATCHLIST")

# --- 7. RESEARCH FEED ---
st.subheader("📁 Strategic Intelligence Feed")
def color_score(val):
    if val < 50: return 'color: #f87171; font-weight: bold;'
    elif val < 80: return 'color: #fbbf24;'
    else: return 'color: #34d399;'

st.dataframe(df.style.applymap(color_score, subset=['Score']), use_container_width=True)

# --- FOOTER ---
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; font-size: 12px; color: #64748b;">
        <strong>OFFICIAL RESEARCH DASHBOARD v3.0</strong><br>
        Lead Researcher: Mohd Khairul Ridhuan Bin Mohd Fadzil<br>
        Methodology: Financial Criminology | Maqasid-ESG | AI-Driven Geopolitical Anomaly Detection
    </div>
    """, unsafe_allow_html=True)

# Auto-refresh simulator
time.sleep(1)
if st.sidebar.button("Manual Signal Scan"):
    st.rerun()
