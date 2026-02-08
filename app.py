import streamlit as st
import google.generativeai as genai
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import os
import time
import pandas as pd
from datetime import datetime

# ========================================
# 🎨 UI/UX EXECUTIVE MINIMALIST DESIGN
# ========================================
st.set_page_config(page_title="Cocoa Intel | Vitor Pozza", layout="wide", page_icon="🍫")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp { background: #0a0a0a; color: #e0e0e0; font-family: 'Inter', sans-serif; }
    
    /* Sidebar Fix & Design */
    [data-testid="stSidebar"] { 
        background: #0f0f0f !important; 
        border-right: 1px solid #2a2a2a;
    }
    
    .sidebar-brand { padding: 30px 20px; border-bottom: 1px solid #2a2a2a; text-align: left; }
    .sidebar-logo { color: #ffffff; font-size: 22px; font-weight: 700; margin-bottom: 5px; }
    .sidebar-title { color: #d4af37; font-size: 10px; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; }
    
    .sb-label { font-size: 11px; color: #555; text-transform: uppercase; letter-spacing: 1px; margin-top: 20px; font-weight: 500; }
    .sb-data { 
        font-size: 19px; color: #ffffff; font-weight: 700; margin-bottom: 12px;
        background: #161616; padding: 10px 15px; border-radius: 6px; border-left: 3px solid #d4af37;
    }
    
    /* Metrics Area */
    div[data-testid="stMetric"] { 
        background: #161616; border: 1px solid #333; border-radius: 12px; padding: 20px;
    }
    
    .sidebar-footer { padding: 25px 20px; font-size: 10px; color: #444; border-top: 1px solid #2a2a2a; margin-top: 40px; }
    .update-tag { color: #00ff88; font-family: monospace; font-size: 9px; margin-top: 5px; opacity: 0.8; }
</style>
""", unsafe_allow_html=True)

# ========================================
# 🔍 DATA ENGINE
# ========================================
@st.cache_data(ttl=3600)
def fetch_physical_price():
    data = {"Bahia": 235.0}
    try:
        url = "https://mercadodocacau.com.br/cotacoes/"
        headers = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, 'html.parser')
        cells = soup.find_all('td')
        for i, cell in enumerate(cells):
            if "ILHÉUS" in cell.get_text().upper():
                val = cells[i+1].get_text().replace('R$', '').replace('.', '').replace(',', '.').strip()
                data["Bahia"] = float(val)
                break
    except: pass
    return data

@st.cache_data(ttl=3600)
def get_historical_data():
    cocoa = yf.Ticker("CC=F")
    df = cocoa.history(period="3y")
    return df

@st.cache_data(ttl=900)
def fetch_global():
    try:
        ticker = yf.Ticker("CC=F").history(period="1mo")
        usd = yf.Ticker("USDBRL=X").history(period="1d")['Close'].iloc[-1]
        return ticker['Close'].iloc[-1], ticker['Close'].iloc[-2], usd
    except: return 0.0, 0.0, 5.0

# Ingestão e Processamento
prices = fetch_physical_price()
ny_now, ny_prev, dollar = fetch_global()
df_hist = get_historical_data()
parity = (ny_now / 66.67) * dollar if ny_now > 0 else 0
basis = prices['Bahia'] - parity
current_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# ========================================
# 🧭 EXECUTIVE SIDEBAR
# ========================================
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand">
        <p class="sidebar-logo">🍫 Cocoa Intel</p>
        <p class="sidebar-title">Market Intelligence Lead</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="padding: 20px;">', unsafe_allow_html=True)
    st.markdown('<p class="sb-label">📍 BAHIA (R$/@)</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sb-data">R$ {prices["Bahia"]:.2f}</p>', unsafe_allow_html=True)
    
    st.markdown('<p class="sb-label">📈 PARIDADE NY (R$/@)</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sb-data">R$ {parity:.2f}</p>', unsafe_allow_html=True)
    
    st.markdown('<p class="sb-label">💱 CÂMBIO USD/BRL</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sb-data">R$ {dollar:.2f}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Sidebar Footer com Sinalização de Update
    st.markdown(f"""
    <div class="sidebar-footer">
        <p style="font-size: 13px; color: #ddd; margin-bottom: 2px;">© {datetime.now().year} Vitor Pozza</p>
        <p style="color: #666; font-size: 11px;">Commodities Analytics Platform</p>
        <p class="update-tag">● SYNCED: {current_time}</p>
    </div>
    """, unsafe_allow_html=True)

# ========================================
# 🖥️ MAIN DASHBOARD
# ========================================
st.title("🍫 Cocoa Strategic Intelligence")
st.markdown(f"#### Global Market Monitoring & Arbitrage Intelligence | <span style='color:#00ff88; font-size:12px;'>● LIVE UPDATE: {current_time}</span>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.metric("NY Futures (USD/t)", f"${ny_now:,.2f}", f"{ny_now - ny_prev:+.2f}")
col2.metric("Market Basis (BRL)", f"R$ {basis:+.2f}", f"{'Premium' if basis > 0 else 'Discount'}")
col3.metric("Physical Price", f"R$ {prices['Bahia']:.2f}")
col4.metric("Market Status", "ACTIVE", delta=datetime.now().strftime("%H:%M"), delta_color="off")

st.divider()

# ========================================
# 📈 CHART SECTION (36 MONTHS)
# ========================================
st.subheader("📊 NY Cocoa Futures - 36 Month Performance")

if not df_hist.empty:
    max_val = df_hist['Close'].max()
    min_val = df_hist['Close'].min()
    last_val = df_hist['Close'].iloc[-1]
    
    chart_col1, chart_col2 = st.columns([3, 1])
    
    with chart_col1:
        st.area_chart(df_hist['Close'], color="#d4af37")
        
    with chart_col2:
        st.markdown(f"""
        **Period Statistics (USD/t)**
        - 🚀 **Max Peak:** `${max_val:,.2f}`
        - 📉 **Period Min:** `${min_val:,.2f}`
        - 🎯 **Current:** `${last_val:,.2f}`
        ---
        *Analysis:* The 36-month trend shows significant volatility. 
        Current levels are at `{((last_val - min_val)/(max_val - min_val)*100):.1f}%` of the historical range.
        """)

st.divider()

# ========================================
# 💬 AI ANALYST
# ========================================
st.subheader("🤖 AI Market Strategic Analyst")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about market trends or arbitrage..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(f"**You:** {prompt}")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        st.error("API Key missing.")
    else:
        # Fallback list for stability
        models = ["gemini-1.5-flash", "gemini-pro"]
        genai.configure(api_key=api_key)
        
        with st.spinner("🧠 Analyzing global dynamics..."):
            res_text = ""
            for m_name in models:
                try:
                    model = genai.GenerativeModel(m_name)
                    ctx = f"Senior Analyst. NY: ${ny_now}. Bahia: R${prices['Bahia']}. Parity: R${parity}."
                    response = model.generate_content([ctx, prompt])
                    res_text = response.text
                    break
                except: continue
            
            if not res_text:
                res_text = "AI Service temporarily unavailable. Please try again."
                
            st.session_state.messages.append({"role": "assistant", "content": res_text})
            with st.chat_message("assistant"):
                st.markdown(res_text)

st.divider()
st.markdown(f"<div style='text-align: center; color: #333; font-size: 10px;'>Data Sync: {current_time} • NYSE & Mercado do Cacau • Developed by Vitor Pozza</div>", unsafe_allow_html=True)