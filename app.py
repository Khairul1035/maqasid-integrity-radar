import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 1. RESEARCHER CONFIGURATION ---
st.set_page_config(page_title="Maqasid Strategic Radar | Researcher MKR", layout="wide")

# Professional Dark-Corporate CSS (HCI Optimization)
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
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
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
st.sidebar.markdown("🎯 **CORE EXPERTISE:**")
st.sidebar.write("- ⚖️ Financial Criminology")
st.sidebar.write("- 🌙 Islamic Studies")
st.sidebar.write("- 🌱 Corporate Sustainability")

st.sidebar.markdown("---")
st.sidebar.markdown("🚀 **SELF-TAUGHT RESEARCH:**")
st.sidebar.caption("- Human-Computer Interaction (HCI)")
st.sidebar.caption("- Artificial Intelligence & Machine Learning")
st.sidebar.caption("- Geopolitics")

# --- 3. DYNAMIC DATA ENGINE ---
@st.cache_data(ttl=300)
def fetch_strategic_data():
    # Menarik data berita 3 hari ke belakang untuk mengelakkan isu "Empty Data" pada waktu pagi
    target_date = (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    API_KEY = "8e257951f858454abe1ac4528f4a24ee"
    
    # Query untuk konflik Global
    url = f'https://newsapi.org/v2/everything?q=(Iran OR Israel OR Gaza OR "Red Sea") AND (Sanctions OR Conflict)&from={target_date}&sortBy=publishedAt&apiKey={API_KEY}'
    
    # Data Minyak (Energy Sustainability)
    oil = yf.Ticker("BZ=F")
    oil_price = oil.history(period="1d")['Close'].iloc[-1]
    
    try:
        articles = requests.get(url).json().get('articles', [])
    except:
        articles = []

    processed = []
    # AI Heuristic: Menghitung risiko berdasarkan kekerapan nama negara
    risk_nations = {"Iran": 0, "Israel": 0, "USA": 0, "Lebanon": 0, "Yemen": 0, "Palestine": 0}
    
    for art in articles[:40]:
        h = art['title'].lower()
        score = 100
        if any(x in h for x in ['sanction', 'illegal', 'laundering', 'freeze']): score -= 40
        if any(x in h for x in ['war', 'strike', 'missile', 'attack', 'bomb']): score -= 60
        
        # ML Logic: Detect risk area
        for nation in risk_nations.keys():
            if nation.lower() in h:
                risk_nations[nation] += (101 - score)

        processed.append({
            "Headline": art['title'],
            "Source": art['source']['name'],
            "Integrity_Score": max(score, 0),
            "Nation_Ref": next((n for n in risk_nations if n.lower() in h), "Global")
        })
    
    return oil_price, pd.DataFrame(processed), risk_nations

oil_p, df, risk_nations = fetch_strategic_data()
avg_score = df['Integrity_Score'].mean() if not df.empty else 75.0

# --- 4. DASHBOARD HEADER (LIVE DATE/TIME) ---
st.markdown(f"""
    <div class="researcher-header">
        <span style="letter-spacing: 3px; font-size: 12px; color: #94a3b8;">DATA NODE: ACTIVE // ESTABLISHED {datetime.now().year}</span>
        <h1 style="margin: 5px 0;">MAQASID STRATEGIC INTEGRITY RADAR</h1>
        <p style="color: #f8fafc; font-size: 18px;">
            <strong>RESEARCHER: MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL</strong><br>
            <span style="color: #38bdf8;">Current Analysis: {datetime.now().strftime('%A, %d %B %Y | %H:%M:%S')}</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

# --- 5. INTERACTIVE GLOBE & AI RISK (HCI SECTION) ---
col_map, col_risk = st.columns([1.5, 1])

with col_map:
    st.subheader("🌐 Interactive Geopolitical Anomaly Globe")
    # Globe berputar mengikut saat semasa (Simulasi Radar)
    rotation_speed = datetime.now().second * 6
    
    fig_globe = go.Figure(go.Scattergeo(
        lon = [51.3, 34.8, -77.0, 44.3, 35.2, 44.0], 
        lat = [35.6, 31.0, 38.9, 33.3, 31.9, 15.0],
        text = ["Iran", "Israel", "USA", "Iraq", "Palestine", "Yemen"],
        mode = 'markers+text',
        marker = dict(size = 12, color = 'red', opacity = 0.8, symbol = 'circle', 
                      line=dict(width=1, color='white'))
    ))
    fig_globe.update_geos(
        projection_type="orthographic",
        showcountries=True, countrycolor="#475569",
        showocean=True, oceancolor="#0f172a",
        showlakes=False,
        projection_rotation=dict(lon=rotation_speed, lat=20, roll=0)
    )
    fig_globe.update_layout(height=500, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_globe, use_container_width=True)

with col_risk:
    st.subheader("🤖 AI-Driven Escalation Projection")
    # Menukar data risiko kepada DataFrame untuk visualisasi
    risk_df = pd.DataFrame(list(risk_nations.items()), columns=['Nation', 'Risk_Value'])
    risk_df['Probability'] = (risk_df['Risk_Value'] / risk_df['Risk_Value'].max() * 100).fillna(0)
    
    fig_risk = px.bar(risk_df.sort_values('Probability', ascending=False), 
                     x='Nation', y='Probability', 
                     color='Probability', color_continuous_scale='Reds',
                     labels={'Probability': 'Escalation Probability (%)'})
    fig_risk.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_risk, use_container_width=True)
    
    st.warning(f"💡 **Researcher Insight:** Trend terkini menunjukkan kebarangkalian konflik tertinggi di zon **{risk_df.iloc[risk_df['Probability'].idxmax()]['Nation']}**.")

# --- 6. METRICS & FEED ---
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("BRENT OIL PRICE", f"${oil_p:.2f}", "LIVE ENERGY FEED")
m2.metric("MAQASID INTEGRITY INDEX", f"{avg_score:.1f}/100")
m3.metric("WORLD TENSION STATUS", "CRITICAL" if avg_score < 60 else "ELEVATED" if avg_score < 85 else "STABLE")

st.subheader("🔍 Strategic Research Feed (Anomaly Detection)")
def style_score(val):
    color = '#f87171' if val < 50 else '#fbbf24' if val < 80 else '#34d399'
    return f'color: {color}; font-weight: bold;'

if not df.empty:
    st.dataframe(df.style.applymap(style_score, subset=['Score']), use_container_width=True)
else:
    st.info("System scanning for geopolitical signals...")

# --- FOOTER ---
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; font-size: 12px; color: #64748b; font-family: monospace;">
        OFFICIAL RESEARCH DATA SOURCE | NODE ID: MKR-2026<br>
        <strong>MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL</strong><br>
        Methodology: Financial Criminology • Islamic Studies • AI-ML Geopolitical Forecasting • HCI Design
    </div>
    """, unsafe_allow_html=True)
