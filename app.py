import streamlit as st
import pandas as pd
import requests
import yfinance as yf
import plotly.express as px
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Maqasid Geopolitical Intelligence", layout="wide")

# CSS untuk gaya professional & branding (HCI)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    [data-testid="stMetricValue"] { font-size: 28px; color: #1f77b4; }
    .researcher-box {
        background-color: #e1f5fe;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #0288d1;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR: OWNER & RESEARCHER PROFILE ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
st.sidebar.title("👤 Project Owner")
st.sidebar.markdown("### **MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL**")
st.sidebar.write("Lead Researcher & Financial Intelligence Analyst")
st.sidebar.markdown("---")
st.sidebar.info("""
**Expertise Integration:**
- ⚖️ Financial Criminology
- 🌙 Islamic Studies (Maqasid)
- 🌱 Corporate Sustainability
- 💻 Human-Computer Interaction
""")

# --- DATA FUNCTIONS ---
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

def get_news():
    API_KEY = "8e257951f858454abe1ac4528f4a24ee"
    try:
        url = f'https://newsapi.org/v2/everything?q=Iran+US+Sanctions&sortBy=publishedAt&apiKey={API_KEY}'
        response = requests.get(url).json()
        articles = response.get('articles', [])
        processed = []
        for art in articles[:20]:
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

# --- MAIN UI ---
st.title("⚖️ Maqasid-Integrity Geopolitical Radar")

# Researcher Branding Box
st.markdown(f"""
    <div class="researcher-box">
        <strong>Developed & Analyzed by:</strong><br>
        <span style="font-size: 20px; font-weight: bold;">MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL</span><br>
        <em>Lead Researcher in Financial Criminology & Geopolitical Risk</em>
    </div>
    """, unsafe_allow_html=True)

st.write(f"📅 **System Live Update:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

oil_p, oil_c = get_oil_price()
df = get_news()

if not df.empty:
    # Row 1: Metrics
    c1, c2, c3 = st.columns(3)
    c1.metric("Brent Crude Oil", f"${oil_p:.2f}", f"{oil_c:.2f}")
    c2.metric("Maqasid Index (Global)", f"{df['Score'].mean():.1f}/100")
    c3.metric("High Risk Alerts", len(df[df['Score'] < 70]))

    # Row 2: Charts
    st.divider()
    st.subheader("📊 Trend Integriti Geopolitik")
    fig = px.area(df, x='Time', y='Score', title="Real-Time Maqasid Pulse", 
                  color_discrete_sequence=['#1f77b4'])
    st.plotly_chart(fig, use_container_width=True)

    # Row 3: Intelligence Feed
    st.subheader("🔍 Financial Intelligence Feed (Iran-US)")
    def color_risk(val):
        color = '#ffcccc' if val < 50 else '#fff4cc' if val < 80 else '#ccffcc'
        return f'background-color: {color}'

    st.dataframe(df.style.applymap(color_risk, subset=['Score']), use_container_width=True)

st.markdown("---")
# Footer Branding
st.markdown(f"""
    <div style="text-align: center; color: gray; font-size: 12px;">
        © 2026 | <strong>Researcher: MOHD KHAIRUL RIDHUAN BIN MOHD FADZIL</strong> | 
        Expertise: Financial Criminology | Islamic Studies | HCI | Corporate Sustainability
    </div>
    """, unsafe_allow_html=True)
