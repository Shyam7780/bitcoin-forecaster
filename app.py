import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import time
from src.data_loader import get_btc_data
from src.features import add_features
from src.model import run_model

# 1. Page Config (इसे सबसे ऊपर ही रखना है)
st.set_page_config(page_title="BTC Oracle | Institutional Forecast", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

# 2. Advanced & Bulletproof CSS
st.markdown("""
<style>
    /* 1. पेज के ऊपर की फालतू जगह (Padding) हटाना ताकि टाइटल ऊपर जाए */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1rem !important;
        max-width: 95% !important;
    }
    
    /* 2. डार्क प्रीमियम बैकग्राउंड */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #050505 0%, #1a0f00 100%) !important;
        color: #ffffff !important;
    }
    
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    /* 3. छिपे हुए डेटा (Metrics) को फिक्स करना */
    div[data-testid="metric-container"] {
        background: rgba(20, 20, 20, 0.95) !important;
        border: 1px solid #4a2b0f !important;
        padding: 20px !important;
        border-radius: 12px !important;
        border-left: 5px solid #F7931A !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.8) !important;
    }
    
    /* मेट्रिक्स के टेक्स्ट का कलर फिक्स करना (Visibility) */
    [data-testid="stMetricLabel"] {
        color: #aaaaaa !important;
        font-size: 1.1rem !important;
        font-weight: bold !important;
    }
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2.2rem !important;
    }
    
    /* 4. अल्ट्रा-प्रीमियम सेंटर बटन */
    div.stButton > button {
        background: linear-gradient(90deg, #F7931A 0%, #cc7a00 100%) !important;
        color: #ffffff !important;
        font-size: 22px !important;
        font-weight: 900 !important;
        padding: 18px 30px !important;
        border-radius: 12px !important;
        border: 2px solid #ffaa42 !important;
        box-shadow: 0px 0px 30px rgba(247, 147, 26, 0.4) !important;
        transition: 0.3s !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        width: 100% !important;
    }
    div.stButton > button:hover {
        box-shadow: 0px 0px 50px rgba(247, 147, 26, 0.8) !important;
        border: 2px solid #ffffff !important;
        transform: scale(1.02) !important;
    }
    
    /* 5. टाइटल्स और रिजल्ट बॉक्स लेआउट */
    .title-box {
        text-align: center;
        background: linear-gradient(180deg, rgba(20,20,20,0.8) 0%, rgba(0,0,0,0) 100%);
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    .result-box {
        text-align: center;
        background: rgba(15, 15, 15, 0.95);
        padding: 30px;
        border-radius: 15px;
        border: 2px solid #F7931A;
        box-shadow: 0px 0px 40px rgba(247, 147, 26, 0.3);
        margin-top: 20px;
    }
    
    /* सभी सामान्य टेक्स्ट को सफेद करना */
    p, h1, h2, h3, h4, h5, h6, span {
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# 3. Header (अब पेज के बिल्कुल ऊपर आएगा)
st.markdown("""
    <div class="title-box">
        <h1 style='color: #F7931A; font-family: monospace; font-size: 3.5rem; margin-bottom: 0;'>⚡ INSTITUTIONAL BTC ORACLE ⚡</h1>
        <p style='color: #a3a3a3; font-size: 1.2rem; font-family: monospace; margin-top: 5px;'>[ QUANTITATIVE TIME-SERIES FORECASTING ENGINE ]</p>
    </div>
""", unsafe_allow_html=True)

# 4. Centered Engine Button
col_left, col_mid, col_right = st.columns([1, 2, 1])
with col_mid:
    start_engine = st.button("🚀 INITIALIZE FORECAST ENGINE", use_container_width=True)

# 5. Execution Logic & UI
if start_engine:
    # लोडिंग एनीमेशन
    with st.spinner("🔄 CONNECTING TO MARKET DATA & RUNNING NEURAL ALGORITHMS..."):
        time.sleep(1.5)
        raw_df = get_btc_data()
        processed_df = add_features(raw_df)
        preds, actual, mape, dates = run_model(processed_df)
        time.sleep(1)
        
    latest_actual = actual.iloc[-1]
    latest_pred = preds[-1]
    price_diff = latest_pred - latest_actual
    accuracy_rate = 100 - (mape * 100)

    # 6. Trend Decision
    if price_diff > 0:
        trend_status = "BULLISH TREND IDENTIFIED"
        trend_color = "#00FF41" # Neon Green
    else:
        trend_status = "BEARISH TREND IDENTIFIED"
        trend_color = "#FF003C" # Red

    st.markdown("<br>", unsafe_allow_html=True)

    # 7. Metrics Layout (अब टेक्स्ट बिल्कुल चमकीला सफेद दिखेगा)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric(label="LAST KNOWN CLOSE PRICE", value=f"${latest_actual:,.2f}")
    with m2:
        st.metric(label="ENGINE ACCURACY TARGET", value=f"{accuracy_rate:.2f}%", delta="Optimized")
    with m3:
        st.metric(label="MARKET MOMENTUM", value=trend_status, delta=f"{'+' if price_diff > 0 else ''}{(price_diff/latest_actual)*100:.2f}%")

    st.markdown("---")

    # 8. Enhanced Chart Visualization
    st.markdown("<h3 style='color: #F7931A; font-family: monospace; text-align: center;'>📊 FORECAST TRAJECTORY & MARKET VOLATILITY</h3>", unsafe_allow_html=True)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates, y=actual, mode='lines', name='Actual Market Price',
        line=dict(color='#ffffff', width=2)
    ))
    fig.add_trace(go.Scatter(
        x=dates, y=preds, mode='lines', name='AI Predicted Trajectory',
        line=dict(color='#F7931A', width=2, dash='dot')
    ))
    
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0.3)',
        paper_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, title="Timeline"),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', title="USD Price"),
        hovermode="x unified",
        height=450,
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01, bgcolor="rgba(0,0,0,0.8)")
    )
    st.plotly_chart(fig, use_container_width=True)

    # 9. Bottom Prominent Result (बिल्कुल साफ और बड़ा रिजल्ट)
    st.markdown(f"""
        <div class="result-box">
            <h4 style="color: {trend_color}; letter-spacing: 2px; margin-bottom: 10px;">{trend_status}</h4>
            <h1 style="color: white; font-size: 3rem; margin: 0;">PROJECTED PRICE TOMORROW</h1>
            <h1 style="color: #F7931A; font-size: 4rem; margin: 10px 0 0 0;">${latest_pred:,.2f}</h1>
        </div>
    """, unsafe_allow_html=True)