import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# --- 1. TACTICAL CONFIGURATION (HCI SPY-GRADE) ---
st.set_page_config(page_title="MAQASID INTEL | GEO-RISK", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for "Spy-Intelligence" UI
st.markdown("""
    <style>
    /* Dark Theme Background */
    .stApp { background-color: #0e1117; color: #00f2ff; }
    
    /* Metrics Styling */
    [data-testid="stMetricValue"] { font-family: 'Courier New', monospace; color: #00f2ff; font-size: 32px; text-shadow: 0 0 10px #00f2ff; }
    [data-testid="stMetricLabel"] { color: #808495; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Researcher Branding Box */
    .intel-header {
        border: 1px solid #00f2ff;
        padding: 20px;
        border-radius: 5px;
        background-color: rgba(0, 242, 255, 0.05);
        margin-bottom: 25px;
        font-family: 'Courier New', monospace;
    }
    
    /* Terminal Style Log */
    .terminal-log {
        background-color: #000000;
        border: 1px solid #333;
        padding: 10px;
        color: #00ff00;
        font-family: 'Courier New', monospace;
        font-size: 12px;
        height: 150px;
        overflow-y: scroll;
    }
    
    /* Dataframe Styling */
    .stDataFrame { border: 1px solid #333; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: OPERATIONAL PROFILE ---
st.sidebar.markdown(f"""
    <div style="text-align: center;">
        <img src="https://cdn-icons-png.flaticon.com/512/552/552408.png" width="80" style="filter: invert(1);">
        <h3 style="color: #00f2ff;">OPERATIONAL PROFILE</h3>
        <p style="font-size: 12px; color: #808495;">SECURITY CLEARANCE: LEVEL 5 (TOP SECRET)</p>
    </div>
    """, unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.subheader("CHIEF INTELLIGENCE RESEARCHER")
st.sidebar.markdown(f"**MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL**")
st.sidebar.caption("Financial Criminology • Maqasid Analyst • ESG Strategy")

st.sidebar.markdown("---")
st.sidebar.subheader("MISSION PARAMETERS")
st.sidebar.checkbox("Live News Feed", value=True)
st.sidebar.checkbox("Financial Anomaly Detection", value=True)
st.sidebar.checkbox("Maqasid ESG Audit", value=True)

# --- DATA ENGINE ---
@st.cache_data(ttl=300)
def fetch_spy_data():
    # Oil Data (Energy Surveillance)
    oil = yf.Ticker("BZ=F")
    oil_data = oil.history(period="2d")
    price = oil_data['Close'].iloc[-1]
    change = price - oil_data['Close'].iloc[-2]
    
    # News Data (Signal Intelligence)
    API_KEY = "8e257951f858454abe1ac4528f4a24ee"
    url = f'https://newsapi.org/v2/everything?q=Iran+US+Sanctions+Conflict&sortBy=publishedAt&apiKey={API_KEY}'
    articles = requests.get(url).json().get('articles', [])
    
    processed = []
    for art in articles[:20]:
        h = art['title'].lower()
        # Intelligence Logic
        score = 100
        threat = "STABLE"
        pillar = "General"
        if any(x in h for x in ['sanction', 'freeze', 'blacklist', 'laundering']):
            score -= 40; threat = "FINANCIAL ANOMALY"; pillar = "Hifz al-Mal"
        if any(x in h for x in ['war', 'strike', 'attack', 'military', 'nuclear']):
            score -= 50; threat = "SECURITY THREAT"; pillar = "Hifz al-Nafs"
            
        processed.append({
            "Timestamp": art['publishedAt'][:16].replace('T', ' '),
            "Source": art['source']['name'].upper(),
            "Signal": art['title'],
            "Integrity_Index": score,
            "Classification": threat,
            "Maqasid_Pillar": pillar
        })
    return price, change, pd.DataFrame(processed)

# --- MAIN INTERFACE ---
oil_price, oil_change, df = fetch_spy_data()

# Intelligence Header
st.markdown(f"""
    <div class="intel-header">
        <span style="color: #808495;">// CLASSIFIED DOCUMENT // GEOPOLITICAL INTELLIGENCE RADAR</span><br>
        <span style="font-size: 24px; font-weight: bold; letter-spacing: 3px;">MAQASID-INTEGRITY COMMAND CENTRE</span><br>
        <span style="color: #00f2ff;">RESEARCHER ID: KHAIRUL_RIDHUAN_FADZIL_035</span>
    </div>
    """, unsafe_allow_html=True)

# Tactical Metrics
m1, m2, m3, m4 = st.columns(4)
m1.metric("BRENT CRUDE (USD)", f"${oil_price:.2f}", f"{oil_change:.2f}")
m2.metric("MAQASID INDEX", f"{df['Integrity_Index'].mean():.1f}")
m3.metric("THREAT ALERTS", len(df[df['Integrity_Index'] < 70]))
m4.metric("SYSTEM STATUS", "ACTIVE", delta_color="normal")

# Intelligence Timeline Chart
st.divider()
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("📡 SIGNAL STRENGTH OVER TIME (INTEGRITY PULSE)")
    fig = px.line(df, x='Timestamp', y='Integrity_Index', template="plotly_dark")
    fig.update_traces(line_color='#00f2ff', line_width=3)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="#808495")
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("📝 LIVE INTELLIGENCE LOG")
    log_content = ""
    for _, row in df.head(10).iterrows():
        log_content += f"[{row['Timestamp']}] ALERT: {row['Classification']} DETECTED FROM {row['Source']}\n"
    st.markdown(f'<div class="terminal-log">{log_content}</div>', unsafe_allow_html=True)

# Data Table
st.subheader("📑 SIGNAL CLASSIFICATION DATA")
def style_risk(val):
    if val < 60: return 'color: #ff4b4b; font-weight: bold;'
    elif val < 80: return 'color: #ffa500;'
    else: return 'color: #00ff00;'

st.dataframe(df.style.applymap(style_risk, subset=['Integrity_Index']), use_container_width=True)

# Footer
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; font-family: 'Courier New', monospace; font-size: 10px; color: #444;">
        SYSTEM OWNER: MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL | 
        LOCATION: [ENCRYPTED] | 
        METHODOLOGY: FINANCIAL CRIMINOLOGY & MAQASID FRAMEWORK v2.0
    </div>
    """, unsafe_allow_html=True)
