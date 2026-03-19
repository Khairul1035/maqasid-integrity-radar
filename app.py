import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from streamlit_autorefresh import st_autorefresh

# =========================================================
# 1. PAGE CONFIG & AUTO-REFRESH
# =========================================================
st.set_page_config(
    page_title="Maqasid Strategic Radar | Researcher MKR",
    page_icon="⚖️",
    layout="wide"
)

# Refresh setiap 2 saat untuk pergerakan Globe & Jam
count = st_autorefresh(interval=2000, limit=None, key="fadzil_refresher")

# =========================================================
# 2. ADVANCED CORPORATE-TACTICAL CSS
# =========================================================
st.markdown("""
<style>
    .stApp {
        background: radial-gradient(circle at top right, #1e293b, #0f172a, #020617);
        color: #f8fafc;
    }
    .researcher-header {
        background: linear-gradient(90deg, #1e3a8a 0%, #1e40af 100%);
        padding: 30px;
        border-radius: 15px;
        border-bottom: 5px solid #fbbf24;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }
    .metric-container {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(56, 189, 248, 0.2);
        border-radius: 12px;
        padding: 20px;
    }
    [data-testid="stMetricValue"] {
        font-family: 'Courier New', monospace;
        color: #38bdf8 !important;
        text-shadow: 0 0 10px rgba(56, 189, 248, 0.5);
    }
    .terminal-text {
        font-family: 'Courier New', monospace;
        color: #10b981;
        background: #000;
        padding: 10px;
        border-radius: 5px;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)

# =========================================================
# 3. SIDEBAR: RESEARCHER PROFILE
# =========================================================
st.sidebar.markdown(f"""
<div style="text-align:center;">
    <img src="https://cdn-icons-png.flaticon.com/512/3306/3306613.png" width="90" style="filter: brightness(0) invert(1);">
    <h3 style="color:#38bdf8; margin-bottom:0;">LEAD RESEARCHER</h3>
    <p style="font-size:14px;">MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
with st.sidebar.expander("🎓 CORE EXPERTISE", expanded=True):
    st.write("⚖️ Financial Criminology")
    st.write("🌙 Islamic Studies")
    st.write("🌱 Corporate Sustainability")

with st.sidebar.expander("🚀 RESEARCH SPECIALIZATION (SELF-TAUGHT)", expanded=True):
    st.caption("• Human-Computer Interaction")
    st.caption("• Artificial Intelligence (AI)")
    st.caption("• Machine Learning (ML)")
    st.caption("• Global Geopolitics")

# =========================================================
# 4. STRATEGIC DATA ENGINE
# =========================================================
@st.cache_data(ttl=300)
def fetch_intelligence():
    # NewsAPI - Real-time Signals
    API_KEY = "8e257951f858454abe1ac4528f4a24ee"
    target_date = (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%d')
    url = f'https://newsapi.org/v2/everything?q=(Iran OR Israel OR Gaza OR Lebanon) AND (Conflict OR Sanctions)&sortBy=publishedAt&apiKey={API_KEY}'
    
    # Financial Pulse (Brent Crude)
    try:
        oil = yf.Ticker("BZ=F")
        oil_p = oil.history(period="1d")['Close'].iloc[-1]
    except:
        oil_p = 108.30

    articles = requests.get(url).json().get('articles', [])
    processed = []
    risk_stats = {"Iran": 0, "Israel": 0, "USA": 0, "Palestine": 0, "Lebanon": 0, "Yemen": 0}

    for art in articles[:40]:
        title = art.get('title', "")
        if not title: continue
        h = title.lower()
        score = 100
        if any(x in h for x in ['war', 'missile', 'strike', 'drone']): score -= 60
        if any(x in h for x in ['sanction', 'freeze', 'illegal']): score -= 30
        
        # Geopolitical Mapping
        for nation in risk_stats.keys():
            if nation.lower() in h: risk_stats[nation] += (100 - score)

        processed.append({
            "Source": art['source']['name'],
            "Headline": title,
            "Integrity_Score": max(score, 0),
            "Pillar": "Hifz al-Nafs" if score < 50 else "Hifz al-Mal" if score < 80 else "General"
        })
    
    return oil_p, pd.DataFrame(processed), risk_stats

oil_price, df_news, risk_map = fetch_intelligence()
avg_index = df_news['Integrity_Score'].mean() if not df_news.empty else 70.0

# =========================================================
# 5. HEADER (REAL-TIME CLOCK)
# =========================================================
now = datetime.now()
st.markdown(f"""
<div class="researcher-header">
    <div style="font-family:monospace; font-size:12px; color:#cbd5e1;">STRATEGIC RESEARCH UNIT // NODE: {now.year}</div>
    <h1 style="color:white; margin:0;">MAQASID STRATEGIC INTEGRITY RADAR</h1>
    <div style="font-size:18px; margin-top:10px;">
        Lead Researcher: <strong>MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL</strong>
    </div>
    <div style="color:#fbbf24; font-family:monospace; font-size:16px; margin-top:5px;">
        {now.strftime('%A, %d %B %Y | %H:%M:%S')}
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# 6. TACTICAL GLOBE & WORLD TENSION
# =========================================================
col_map, col_radar = st.columns([1.6, 1])

with col_map:
    st.subheader("🌐 Interactive Geopolitical Anomaly Globe")
    # Globe Rotation Logic
    lon_rotation = (count * 10) % 360
    
    fig_globe = go.Figure(go.Scattergeo(
        lon = [51.3, 34.8, -77.0, 35.2, 33.8, 44.0],
        lat = [35.6, 31.0, 38.9, 31.9, 32.4, 15.0],
        text = ["IRAN", "ISRAEL", "USA", "PALESTINE", "LEBANON", "YEMEN"],
        mode = 'markers+text',
        marker = dict(size=10, color='red', opacity=0.8, line=dict(width=1, color='white'))
    ))
    fig_globe.update_geos(
        projection_type="orthographic",
        showland=True, landcolor="#1e293b",
        showocean=True, oceancolor="#020617",
        showcountries=True, countrycolor="#475569",
        projection_rotation=dict(lon=lon_rotation, lat=20, roll=0)
    )
    fig_globe.update_layout(height=500, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_globe, use_container_width=True)

with col_radar:
    st.subheader("🤖 AI Escalation Forecast")
    risk_df = pd.DataFrame(list(risk_map.items()), columns=['Nation', 'Risk'])
    risk_df['Probability'] = (risk_df['Risk'] / risk_df['Risk'].max() * 100).fillna(20)
    
    fig_risk = px.bar(risk_df.sort_values('Probability', ascending=False), 
                     x='Nation', y='Probability', color='Probability',
                     color_continuous_scale='Reds', template="plotly_dark")
    fig_risk.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=380)
    st.plotly_chart(fig_risk, use_container_width=True)
    
    # Tension Gauge
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = 100 - avg_index,
        title = {'text': "World Tension Rating", 'font': {'size': 14}},
        gauge = {
            'axis': {'range': [0, 100]},
            'bar': {'color': "#ef4444"},
            'steps': [
                {'range': [0, 40], 'color': "#065f46"},
                {'range': [40, 70], 'color': "#92400e"},
                {'range': [70, 100], 'color': "#7f1d1d"}]
        }
    ))
    fig_gauge.update_layout(height=200, margin=dict(l=10,r=10,t=30,b=10), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_gauge, use_container_width=True)

# =========================================================
# 7. STRATEGIC METRICS & DATA FEED
# =========================================
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("BRENT OIL (LIVE)", f"${oil_price:.2f}", "USD/BBL")
m2.metric("MAQASID INTEGRITY INDEX", f"{avg_index:.1f}/100", "SIGNAL PULSE")
m3.metric("GLOBAL STATUS", "CRITICAL" if avg_index < 60 else "ELEVATED")

st.subheader("🔍 Strategic Intelligence Feed (Iran-US-Israel)")
def color_score(val):
    color = '#f87171' if val < 50 else '#fbbf24' if val < 80 else '#34d399'
    return f'color: {color}; font-weight: bold;'

if not df_news.empty:
    st.dataframe(df_news.style.applymap(color_score, subset=['Integrity_Score']), use_container_width=True)

# =========================================================
# 8. FOOTER
# =========================================================
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #94a3b8; font-family: monospace; font-size: 12px;">
    <strong>OFFICIAL STRATEGIC DOCUMENT</strong> | Node ID: MKR-INTEL-2026<br>
    Researcher: Mohd Khairul Ridhuan Bin Mohd Fadzil<br>
    Integrated: Financial Criminology • Maqasid-ESG • AI/ML Forecasting • HCI Visualization
</div>
""", unsafe_allow_html=True)
