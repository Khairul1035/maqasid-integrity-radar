import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time

# --- 1. RESEARCHER CONFIGURATION (HCI OPTIMIZED) ---
st.set_page_config(page_title="Strategic Maqasid Radar | Researcher MKR", layout="wide")

# Professional Dark-Corporate CSS
st.markdown("""
    <style>
    .main { background-color: #0b1120; color: #e2e8f0; }
    .researcher-header {
        background-color: #1e293b;
        padding: 25px;
        color: #38bdf8;
        border-radius: 12px;
        border-left: 10px solid #fbbf24;
        margin-bottom: 20px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.4);
    }
    .stMetric { background-color: #1e293b; border-radius: 10px; padding: 15px; border: 1px solid #334155; }
    [data-testid="stMetricValue"] { color: #38bdf8; font-family: 'Courier New', monospace; }
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
st.sidebar.markdown("🎯 **CORE EXPERTISE:**")
st.sidebar.info("• Financial Criminology\n• Islamic Studies\n• Corporate Sustainability")

st.sidebar.markdown("🚀 **SELF-TAUGHT RESEARCH:**")
st.sidebar.warning("• Human-Computer Interaction (HCI)\n• Artificial Intelligence & Machine Learning\n• Geopolitics")

# --- 3. DYNAMIC DATA ENGINE (AI-DRIVEN) ---
@st.cache_data(ttl=300)
def fetch_strategic_data():
    # Ambil data 3 hari ke belakang untuk elak isu API delay
    target_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    API_KEY = "8e257951f858454abe1ac4528f4a24ee"
    
    # Global Conflict Query
    url = f'https://newsapi.org/v2/everything?q=(Iran OR Israel OR Gaza OR "Red Sea") AND (Sanctions OR Conflict)&from={target_date}&sortBy=publishedAt&apiKey={API_KEY}'
    
    # Financial Data: Brent Crude
    try:
        oil = yf.Ticker("BZ=F")
        oil_price = oil.history(period="1d")['Close'].iloc[-1]
    except:
        oil_price = 108.30 # Fallback

    try:
        response = requests.get(url).json()
        articles = response.get('articles', [])
    except:
        articles = []

    processed = []
    # AI Heuristic: Analyze Risk per Nation
    risk_nations = {"Iran": 0, "Israel": 0, "USA": 0, "Lebanon": 0, "Yemen": 0, "Palestine": 0}
    
    for art in articles[:40]:
        title = art.get('title')
        if not title: continue # SAFETY CHECK: Elak AttributeError NoneType
        
        h = title.lower()
        score = 100
        
        # Financial Criminology & Maqasid Logic
        if any(x in h for x in ['sanction', 'illegal', 'laundering', 'freeze']): score -= 40
        if any(x in h for x in ['war', 'strike', 'missile', 'attack', 'bomb']): score -= 60
        
        # AI Logic: Risk Mapping
        for nation in risk_nations.keys():
            if nation.lower() in h:
                risk_nations[nation] += (101 - score)

        processed.append({
            "Headline": title,
            "Source": art['source']['name'],
            "Score": max(score, 0),
            "Pillar": "Hifz al-Nafs (Life)" if score < 50 else "Hifz al-Mal (Wealth)" if score < 80 else "General"
        })
    
    return oil_price, pd.DataFrame(processed), risk_nations

oil_p, df, risk_nations = fetch_strategic_data()
avg_score = df['Score'].mean() if not df.empty else 75.0

# --- 4. DASHBOARD HEADER ---
st.markdown(f"""
    <div class="researcher-header">
        <span style="letter-spacing: 3px; font-size: 11px; color: #94a3b8;">GEOPOLITICAL INTELLIGENCE UNIT // SYSTEM YEAR: {datetime.now().year}</span>
        <h1 style="margin: 5px 0;">MAQASID STRATEGIC INTEGRITY RADAR</h1>
        <p style="color: #f8fafc; font-size: 18px;">
            <strong>RESEARCHER: MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL</strong><br>
            <span style="color: #38bdf8; font-family: monospace;">{datetime.now().strftime('%A, %d %B %Y | %H:%M:%S')}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. INTERACTIVE GLOBE & AI RISK ---
col_map, col_risk = st.columns([1.5, 1])

with col_map:
    st.subheader("🌐 Global Strategic Anomaly Globe")
    # Globe berputar mengikut saat (Radar Simulation)
    rotation = datetime.now().second * 6
    
    fig_globe = go.Figure(go.Scattergeo(
        lon = [51.3, 34.8, -77.0, 44.3, 35.2, 44.0], 
        lat = [35.6, 31.0, 38.9, 33.3, 31.9, 15.0],
        text = ["IRN", "ISR", "USA", "IRQ", "PSE", "YEM"],
        mode = 'markers+text',
        marker = dict(size = 12, color = '#f87171', opacity = 0.8, symbol = 'circle', 
                      line=dict(width=1, color='white')),
        textfont=dict(color="white", size=9)
    ))
    fig_globe.update_geos(
        projection_type="orthographic",
        showcountries=True, countrycolor="#475569",
        showocean=True, oceancolor="#0f172a",
        projection_rotation=dict(lon=rotation, lat=20, roll=0)
    )
    fig_globe.update_layout(height=450, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_globe, use_container_width=True)

with col_risk:
    st.subheader("🤖 AI-Driven Escalation Forecast")
    risk_df = pd.DataFrame(list(risk_nations.items()), columns=['Nation', 'Val'])
    risk_df['Probability'] = (risk_df['Val'] / (risk_df['Val'].max() if risk_df['Val'].max() > 0 else 1) * 100)
    
    fig_risk = px.bar(risk_df.sort_values('Probability', ascending=False), 
                     x='Nation', y='Probability', 
                     color='Probability', color_continuous_scale='Reds',
                     labels={'Probability': 'Risk %'})
    fig_risk.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white", height=350)
    st.plotly_chart(fig_risk, use_container_width=True)
    
    top_nation = risk_df.iloc[risk_df['Probability'].idxmax()]['Nation'] if not risk_df.empty else "None"
    st.markdown(f"""
        <div style="background-color:rgba(248, 113, 113, 0.1); padding:10px; border-radius:5px; border-left: 4px solid #f87171;">
            <strong>AI ANALYSIS:</strong> Risiko eskalasi dikesan pada zon <strong>{top_nation}</strong>.
        </div>
    """, unsafe_allow_html=True)

# --- 6. METRICS & RESEARCH FEED ---
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("BRENT CRUDE OIL", f"${oil_p:.2f}", "LIVE FEED")
m2.metric("MAQASID INTEGRITY INDEX", f"{avg_score:.1f}/100")
m3.metric("GEOPOLITICAL TENSION", "CRITICAL" if avg_score < 60 else "ELEVATED")

st.subheader("🔍 Strategic Intelligence Feed (Real-Time)")
def style_score(val):
    color = '#f87171' if val < 50 else '#fbbf24' if val < 80 else '#34d399'
    return f'color: {color}; font-weight: bold;'

if not df.empty:
    st.dataframe(df.style.applymap(style_score, subset=['Score']), use_container_width=True)
else:
    st.info("Scanning geopolitical signals...")

# --- FOOTER ---
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; font-size: 11px; color: #64748b; font-family: monospace;">
        STRATEGIC RESEARCH NODE: MKR-INTEL-2026<br>
        <strong>RESEARCHER: MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL</strong><br>
        Integrated Expertise: Financial Criminology • Islamic Studies • Sustainability • AI/ML • HCI
    </div>
    """, unsafe_allow_html=True)
