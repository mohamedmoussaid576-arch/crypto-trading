# ================================
# CRYPTO TRADING APP - PROFESSIONAL
# Python - Streamlit + Plotly
# ================================

import requests
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# ----------------
# PAGE CONFIG
# ----------------
st.set_page_config(
    page_title="Crypto Trading Pro", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------
# THEME TOGGLE
# ----------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True

# ----------------
# DYNAMIC CSS BASED ON THEME
# ----------------
if st.session_state.dark_mode:
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #0a0a0a 0%, #1a1a2e 100%) !important;
        }
        
        .main .block-container {
            background-color: transparent !important;
            padding-top: 2rem;
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #16213e 0%, #0f3460 100%) !important;
            border-right: 1px solid #2a4365;
        }
        
        header[data-testid="stHeader"] {
            background: rgba(10, 10, 10, 0.8) !important;
            backdrop-filter: blur(10px);
        }
        
        h1, h2, h3, h4, h5, h6, p, span, label, div, li, a {
            color: #ffffff !important;
        }
        
        .stMetric {
            background: linear-gradient(135deg, #1e3a5f 0%, #2a4365 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #3a5a7f;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: #4fd1c5 !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: #a0aec0 !important;
            font-size: 0.9rem !important;
            font-weight: 500 !important;
        }
        
        .stSelectbox > div > div {
            background: linear-gradient(135deg, #1e3a5f 0%, #2a4365 100%) !important;
            border: 1px solid #3a5a7f !important;
            border-radius: 8px;
            color: #ffffff !important;
        }
        
        .stNumberInput input {
            background: linear-gradient(135deg, #1e3a5f 0%, #2a4365 100%) !important;
            color: #ffffff !important;
            border: 1px solid #3a5a7f !important;
            border-radius: 8px;
            font-weight: 500;
        }
        
        .stButton button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: rgba(30, 58, 95, 0.5);
            padding: 0.5rem;
            border-radius: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background: transparent;
            color: #a0aec0 !important;
            border-radius: 6px;
            padding: 0.5rem 1rem;
        }
        
        .stTabs [aria-selected="true"] {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #ffffff !important;
        }
        
        .trade-card {
            background: linear-gradient(135deg, #1e3a5f 0%, #2a4365 100%);
            padding: 2rem;
            border-radius: 16px;
            border: 1px solid #3a5a7f;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        }
        
        .success-box {
            background: linear-gradient(135deg, #0ea5e9 0%, #06b6d4 100%);
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        
        .dataframe {
            background: rgba(30, 58, 95, 0.5) !important;
            border-radius: 8px;
        }
        </style>
    """, unsafe_allow_html=True)
    plot_template = "plotly_dark"
    paper_bg = "rgba(10, 10, 10, 0)"
    plot_bg = "rgba(10, 10, 10, 0)"
else:
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
        }
        
        .main .block-container {
            background-color: transparent !important;
            padding-top: 2rem;
        }
        
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #ffffff 0%, #f0f4f8 100%) !important;
            border-right: 1px solid #cbd5e0;
        }
        
        h1, h2, h3, h4, h5, h6, p, span, label, div, li, a {
            color: #2d3748 !important;
        }
        
        .stMetric {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        [data-testid="stMetricValue"] {
            font-size: 1.8rem !important;
            font-weight: 700 !important;
            color: #2b6cb0 !important;
        }
        
        .stButton button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px;
            font-weight: 600;
            padding: 0.5rem 1rem;
        }
        </style>
    """, unsafe_allow_html=True)
    plot_template = "plotly_white"
    paper_bg = "rgba(255, 255, 255, 0)"
    plot_bg = "rgba(255, 255, 255, 0)"

# ----------------
# HEADER
# ----------------
col_title, col_theme = st.columns([5, 1])

with col_title:
    st.markdown("# 📊 Crypto Trading Pro")
    st.markdown("*Advanced Trading Dashboard & Portfolio Management*")

with col_theme:
    st.write("")
    st.write("")
    if st.button("☀️ Light" if st.session_state.dark_mode else "🌙 Dark", use_container_width=True):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

st.markdown("---")

# ----------------
# DATA COLLECTION
# ----------------
@st.cache_data(ttl=60)
def get_prices(symbol="BTCUSDT", interval="1h", limit=200):
    url = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    data = requests.get(url, params=params).json()

    df = pd.DataFrame(data, columns=[
        "Open time", "Open", "High", "Low", "Close",
        "Volume", "Close time", "Quote asset volume", "Trades",
        "Taker base", "Taker quote", "Ignore"
    ])

    df["Open time"] = pd.to_datetime(df["Open time"], unit="ms")
    for col in ["Close", "Open", "High", "Low", "Volume"]:
        df[col] = df[col].astype(float)

    return df

# ----------------
# TECHNICAL INDICATORS
# ----------------
def add_indicators(df, ma_period=20, ema_period=20, rsi_period=14, bb_period=20):
    # Moving Averages
    df["MA_20"] = df["Close"].rolling(ma_period).mean()
    df["EMA_20"] = df["Close"].ewm(span=ema_period, adjust=False).mean()
    df["MA_50"] = df["Close"].rolling(50).mean()
    
    # Volatility
    df["Volatility"] = df["Close"].rolling(ma_period).std()
    
    # RSI
    delta = df["Close"].diff()
    gain = (delta.where(delta > 0, 0)).rolling(rsi_period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(rsi_period).mean()
    rs = gain / loss
    df["RSI"] = 100 - (100 / (1 + rs))
    
    # Bollinger Bands
    df["BB_Middle"] = df["Close"].rolling(bb_period).mean()
    bb_std = df["Close"].rolling(bb_period).std()
    df["BB_Upper"] = df["BB_Middle"] + (2 * bb_std)
    df["BB_Lower"] = df["BB_Middle"] - (2 * bb_std)
    
    # MACD
    exp1 = df["Close"].ewm(span=12, adjust=False).mean()
    exp2 = df["Close"].ewm(span=26, adjust=False).mean()
    df["MACD"] = exp1 - exp2
    df["MACD_Signal"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["MACD_Hist"] = df["MACD"] - df["MACD_Signal"]
    
    # Linear Regression
    x = np.arange(len(df))
    y = df["Close"].values
    a, b = np.polyfit(x, y, 1)
    df["LR_Prediction"] = a * x + b
    
    return df

def trading_signal(df):
    df["Signal"] = np.where(
        (df["Close"] > df["MA_20"]) & (df["RSI"] < 70) & (df["MACD"] > df["MACD_Signal"]),
        "BUY",
        np.where(
            (df["Close"] < df["MA_20"]) & (df["RSI"] > 30) & (df["MACD"] < df["MACD_Signal"]),
            "SELL",
            "HOLD"
        )
    )
    return df

# ----------------
# SIDEBAR CONTROLS
# ----------------
with st.sidebar:
    st.markdown("## ⚙️ Trading Parameters")
    
    symbol = st.selectbox(
        "📈 Select Symbol",
        ["BTCUSDT", "ETHUSDT", "BNBUSDT", "ADAUSDT", "SOLUSDT"],
        index=0
    )

    interval = st.selectbox(
        "⏰ Time Interval",
        ["1m", "5m", "15m", "1h", "4h", "1d"],
        index=3
    )
    
    chart_type = st.selectbox(
        "📊 Chart Type",
        ["Candlestick", "Line", "Area"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("## 💰 Wallet Management")
    
    # Initialize states
    if "balance" not in st.session_state:
        st.session_state.balance = 10000.00
    if "portfolio" not in st.session_state:
        st.session_state.portfolio = {}
    if "transactions" not in st.session_state:
        st.session_state.transactions = []
    
    st.metric("💵 Cash Balance", f"${st.session_state.balance:,.2f}")
    
    with st.expander("💳 Deposit / Withdraw"):
        deposit_amount = st.number_input("Deposit ($)", min_value=0.0, value=0.0, step=100.0, key="dep")
        if st.button("➕ Deposit", use_container_width=True):
            if deposit_amount > 0:
                st.session_state.balance += deposit_amount
                st.success(f"✅ +${deposit_amount:,.2f}")
                st.rerun()
        
        withdraw_amount = st.number_input("Withdraw ($)", min_value=0.0, value=0.0, step=100.0, key="with")
        if st.button("➖ Withdraw", use_container_width=True):
            if 0 < withdraw_amount <= st.session_state.balance:
                st.session_state.balance -= withdraw_amount
                st.success(f"✅ -${withdraw_amount:,.2f}")
                st.rerun()
            elif withdraw_amount > st.session_state.balance:
                st.error("⚠️ Insufficient funds")

# ----------------
# DATA PROCESSING
# ----------------
df = get_prices(symbol, interval, limit=500)
df = add_indicators(df)
df = trading_signal(df)

current_price = df['Close'].iloc[-1]
price_change = df['Close'].iloc[-1] - df['Close'].iloc[-2]
price_change_pct = (price_change / df['Close'].iloc[-2]) * 100

# ----------------
# MAIN METRICS
# ----------------
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        "💰 Current Price", 
        f"${current_price:,.2f}",
        f"{price_change_pct:+.2f}%"
    )

with col2:
    st.metric("📊 RSI", f"{df['RSI'].iloc[-1]:.2f}")

with col3:
    st.metric("📈 MA 20", f"${df['MA_20'].iloc[-1]:,.2f}")

with col4:
    st.metric("📉 Volatility", f"{df['Volatility'].iloc[-1]:.4f}")

with col5:
    signal_color = "🟢" if df["Signal"].iloc[-1] == "BUY" else "🔴" if df["Signal"].iloc[-1] == "SELL" else "🟡"
    st.metric("🎯 Signal", f"{signal_color} {df['Signal'].iloc[-1]}")

with col6:
    vol_24h = df['Volume'].iloc[-24:].sum() if len(df) >= 24 else df['Volume'].sum()
    st.metric("📊 Volume 24h", f"{vol_24h:,.0f}")

st.markdown("---")

# ----------------
# TABS INTERFACE
# ----------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Advanced Chart",
    "💼 Trading",
    "📊 Portfolio",
    "📜 History",
    "📚 Analysis"
])

# ==================
# TAB 1: ADVANCED CHART
# ==================
with tab1:
    # Create subplots
    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.05,
        row_heights=[0.6, 0.2, 0.2],
        subplot_titles=(f"{symbol} Price Chart", "MACD", "RSI")
    )
    
    # Main price chart
    if chart_type == "Candlestick":
        fig.add_trace(go.Candlestick(
            x=df["Open time"],
            open=df["Open"],
            high=df["High"],
            low=df["Low"],
            close=df["Close"],
            name="Price"
        ), row=1, col=1)
    elif chart_type == "Line":
        fig.add_trace(go.Scatter(
            x=df["Open time"],
            y=df["Close"],
            mode="lines",
            name="Price",
            line=dict(color="#667eea", width=2)
        ), row=1, col=1)
    else:  # Area
        fig.add_trace(go.Scatter(
            x=df["Open time"],
            y=df["Close"],
            fill='tozeroy',
            name="Price",
            line=dict(color="#667eea")
        ), row=1, col=1)
    
    # Bollinger Bands
    fig.add_trace(go.Scatter(
        x=df["Open time"],
        y=df["BB_Upper"],
        mode="lines",
        name="BB Upper",
        line=dict(color="rgba(250, 128, 114, 0.5)", dash="dash")
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df["Open time"],
        y=df["BB_Lower"],
        mode="lines",
        name="BB Lower",
        line=dict(color="rgba(100, 200, 255, 0.5)", dash="dash"),
        fill='tonexty',
        fillcolor='rgba(150, 150, 255, 0.1)'
    ), row=1, col=1)
    
    # Moving Averages
    fig.add_trace(go.Scatter(
        x=df["Open time"],
        y=df["MA_20"],
        mode="lines",
        name="MA 20",
        line=dict(color="#4fd1c5", width=2)
    ), row=1, col=1)
    
    fig.add_trace(go.Scatter(
        x=df["Open time"],
        y=df["MA_50"],
        mode="lines",
        name="MA 50",
        line=dict(color="#f6ad55", width=2)
    ), row=1, col=1)
    
    # MACD
    fig.add_trace(go.Scatter(
        x=df["Open time"],
        y=df["MACD"],
        mode="lines",
        name="MACD",
        line=dict(color="#667eea")
    ), row=2, col=1)
    
    fig.add_trace(go.Scatter(
        x=df["Open time"],
        y=df["MACD_Signal"],
        mode="lines",
        name="Signal",
        line=dict(color="#f6ad55")
    ), row=2, col=1)
    
    # MACD Histogram
    colors = ['green' if val >= 0 else 'red' for val in df["MACD_Hist"]]
    fig.add_trace(go.Bar(
        x=df["Open time"],
        y=df["MACD_Hist"],
        name="MACD Hist",
        marker_color=colors
    ), row=2, col=1)
    
    # RSI
    fig.add_trace(go.Scatter(
        x=df["Open time"],
        y=df["RSI"],
        mode="lines",
        name="RSI",
        line=dict(color="#9f7aea")
    ), row=3, col=1)
    
    # RSI levels
    fig.add_hline(y=70, line_dash="dash", line_color="red", opacity=0.5, row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", opacity=0.5, row=3, col=1)
    
    fig.update_layout(
        height=800,
        template=plot_template,
        xaxis_rangeslider_visible=False,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ==================
# TAB 2: TRADING
# ==================
with tab2:
    col_buy, col_sell = st.columns(2)
    
    with col_buy:
        st.markdown("### 🟢 BUY ORDER")
        st.markdown("---")
        
        order_type_buy = st.radio("Order Type", ["Market", "Limit"], key="buy_type", horizontal=True)
        
        if order_type_buy == "Market":
            buy_amount_usd = st.number_input(
                "💵 Amount (USD)",
                min_value=1.0,
                value=100.0,
                step=10.0,
                key="buy_market"
            )
            buy_price = current_price
            crypto_amount = buy_amount_usd / current_price
        else:
            buy_price = st.number_input(
                "💰 Limit Price (USD)",
                min_value=0.01,
                value=float(current_price),
                step=0.01,
                key="buy_limit_price"
            )
            buy_amount_usd = st.number_input(
                "💵 Amount (USD)",
                min_value=1.0,
                value=100.0,
                step=10.0,
                key="buy_limit_amount"
            )
            crypto_amount = buy_amount_usd / buy_price
        
        st.info(f"📦 You will receive: **{crypto_amount:.8f}** {symbol[:-4]}")
        st.info(f"💰 At price: **${buy_price:.2f}**")
        st.info(f"💵 Total cost: **${buy_amount_usd:.2f}**")
        
        if st.button("🛒 EXECUTE BUY ORDER", use_container_width=True, type="primary"):
            if buy_amount_usd <= st.session_state.balance:
                st.session_state.balance -= buy_amount_usd
                
                if symbol not in st.session_state.portfolio:
                    st.session_state.portfolio[symbol] = 0.0
                st.session_state.portfolio[symbol] += crypto_amount
                
                st.session_state.transactions.append({
                    "Type": "BUY",
                    "Symbol": symbol,
                    "Amount": crypto_amount,
                    "Price": buy_price,
                    "Total": buy_amount_usd,
                    "Order Type": order_type_buy,
                    "Timestamp": datetime.now()
                })
                
                st.success(f"✅ Successfully bought {crypto_amount:.8f} {symbol[:-4]}")
                st.balloons()
                st.rerun()
            else:
                st.error("⚠️ Insufficient balance!")
    
    with col_sell:
        st.markdown("### 🔴 SELL ORDER")
        st.markdown("---")
        
        current_holdings = st.session_state.portfolio.get(symbol, 0.0)
        
        order_type_sell = st.radio("Order Type", ["Market", "Limit"], key="sell_type", horizontal=True)
        
        if order_type_sell == "Market":
            sell_amount_crypto = st.number_input(
                f"🪙 Amount ({symbol[:-4]})",
                min_value=0.0,
                max_value=float(current_holdings),
                value=min(0.01, float(current_holdings)),
                step=0.001,
                key="sell_market",
                format="%.8f"
            )
            sell_price = current_price
            usd_amount = sell_amount_crypto * current_price
        else:
            sell_price = st.number_input(
                "💰 Limit Price (USD)",
                min_value=0.01,
                value=float(current_price),
                step=0.01,
                key="sell_limit_price"
            )
            sell_amount_crypto = st.number_input(
                f"🪙 Amount ({symbol[:-4]})",
                min_value=0.0,
                max_value=float(current_holdings),
                value=min(0.01, float(current_holdings)),
                step=0.001,
                key="sell_limit_amount",
                format="%.8f"
            )
            usd_amount = sell_amount_crypto * sell_price
        
        st.info(f"💵 You will receive: **${usd_amount:.2f}** USD")
        st.info(f"💰 At price: **${sell_price:.2f}**")
        st.info(f"📊 Holdings: **{current_holdings:.8f}** {symbol[:-4]}")
        
        if st.button("💰 EXECUTE SELL ORDER", use_container_width=True, type="secondary"):
            if sell_amount_crypto <= current_holdings:
                st.session_state.balance += usd_amount
                st.session_state.portfolio[symbol] -= sell_amount_crypto
                
                st.session_state.transactions.append({
                    "Type": "SELL",
                    "Symbol": symbol,
                    "Amount": sell_amount_crypto,
                    "Price": sell_price,
                    "Total": usd_amount,
                    "Order Type": order_type_sell,
                    "Timestamp": datetime.now()
                })
                
                st.success(f"✅ Successfully sold {sell_amount_crypto:.8f} {symbol[:-4]}")
                st.rerun()
            else:
                st.error(f"⚠️ Insufficient {symbol[:-4]} balance!")

# ==================
# TAB 3: PORTFOLIO
# ==================
with tab3:
    st.markdown("## 💼 Portfolio Overview")
    
    if st.session_state.portfolio:
        portfolio_data = []
        total_value = 0.0
        
        for sym, amount in st.session_state.portfolio.items():
            if amount > 0:
                if sym == symbol:
                    price = current_price
                else:
                    temp_df = get_prices(sym, interval, limit=2)
                    price = temp_df['Close'].iloc[-1]
                    prev_price = temp_df['Close'].iloc[-2]
                    change = ((price - prev_price) / prev_price) * 100
                
                value = amount * price
                total_value += value
                
                portfolio_data.append({
                    "Symbol": sym[:-4],
                    "Amount": f"{amount:.8f}",
                    "Price": f"${price:.2f}",
                    "Value": f"${value:.2f}",
                    "Change 24h": f"{change:+.2f}%" if sym != symbol else f"{price_change_pct:+.2f}%"
                })
        
        if portfolio_data:
            # Portfolio Summary Cards
            col1, col2, col3, col4 = st.columns(4)
            
            total_account = st.session_state.balance + total_value
            
            with col1:
                st.metric("💵 Cash Balance", f"${st.session_state.balance:,.2f}")
            with col2:
                st.metric("🪙 Crypto Value", f"${total_value:,.2f}")
            with col3:
                st.metric("💼 Total Account", f"${total_account:,.2f}")
            with col4:
                profit = total_account - 10000
                profit_pct = (profit / 10000) * 100
                st.metric("📈 Total P&L", f"${profit:,.2f}", f"{profit_pct:+.2f}%")
            
            st.markdown("---")
            
            # Portfolio Table
            portfolio_df = pd.DataFrame(portfolio_data)
            st.dataframe(
                portfolio_df,
                use_container_width=True,
                hide_index=True
            )
            
            # Pie Chart
            st.markdown("### 📊 Asset Allocation")
            values = [float(d["Value"].replace("$", "").replace(",", "")) for d in portfolio_data]
            labels = [d["Symbol"] for d in portfolio_data]
            
            fig_pie = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.4,
                marker_colors=['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b']
            )])
            
            fig_pie.update_layout(
                template=plot_template,
                paper_bgcolor=paper_bg,
                height=400
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("📭 Your portfolio is empty. Start trading to build your portfolio!")
    else:
        st.info("📭 Your portfolio is empty. Start trading to build your portfolio!")

# ==================
# TAB 4: HISTORY
# ==================
with tab4:
    st.markdown("## 📜 Transaction History")
    
    if st.session_state.transactions:
        transactions_df = pd.DataFrame(st.session_state.transactions)
        transactions_df = transactions_df.sort_values("Timestamp", ascending=False)
        
        # Filters
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            filter_type = st.multiselect(
                "Filter by Type",
                ["BUY", "SELL"],
                default=["BUY", "SELL"]
            )
        
        with col_f2:
            filter_symbol = st.multiselect(
                "Filter by Symbol",
                transactions_df["Symbol"].unique(),
                default=transactions_df["Symbol"].unique().tolist()
            )
        
        # Apply filters
        filtered_df = transactions_df[
            (transactions_df["Type"].isin(filter_type)) &
            (transactions_df["Symbol"].isin(filter_symbol))
        ]
        
        # Statistics
        col_s1, col_s2, col_s3, col_s4 = st.columns(4)
        
        total_buys = filtered_df[filtered_df["Type"] == "BUY"]["Total"].sum()
        total_sells = filtered_df[filtered_df["Type"] == "SELL"]["Total"].sum()
        total_trades = len(filtered_df)
        
        with col_s1:
            st.metric("📊 Total Trades", total_trades)
        with col_s2:
            st.metric("🟢 Total Buys", f"${total_buys:,.2f}")
        with col_s3:
            st.metric("🔴 Total Sells", f"${total_sells:,.2f}")
        with col_s4:
            net = total_sells - total_buys
            st.metric("💰 Net Flow", f"${net:,.2f}")
        
        st.markdown("---")
        
        # Display transactions
        display_df = filtered_df.copy()
        display_df["Amount"] = display_df["Amount"].apply(lambda x: f"{x:.8f}")
        display_df["Price"] = display_df["Price"].apply(lambda x: f"${x:.2f}")
        display_df["Total"] = display_df["Total"].apply(lambda x: f"${x:.2f}")
        display_df["Timestamp"] = display_df["Timestamp"].apply(lambda x: x.strftime("%Y-%m-%d %H:%M:%S"))
        
        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True
        )
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"transactions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    else:
        st.info("📭 No transactions yet. Start trading to see your history!")

# ==================
# TAB 5: ANALYSIS
# ==================
with tab5:
    st.markdown("## 📚 Market Analysis & Insights")
    
    col_a1, col_a2 = st.columns(2)
    
    with col_a1:
        st.markdown("### 📊 Technical Analysis Summary")
        
        # Signal strength
        rsi_val = df['RSI'].iloc[-1]
        if rsi_val > 70:
            rsi_signal = "🔴 Overbought"
            rsi_color = "red"
        elif rsi_val < 30:
            rsi_signal = "🟢 Oversold"
            rsi_color = "green"
        else:
            rsi_signal = "🟡 Neutral"
            rsi_color = "orange"
        
        st.markdown(f"**RSI Status:** {rsi_signal}")
        
        # MACD
        macd_val = df['MACD'].iloc[-1]
        macd_signal = df['MACD_Signal'].iloc[-1]
        if macd_val > macd_signal:
            st.markdown("**MACD:** 🟢 Bullish Crossover")
        else:
            st.markdown("**MACD:** 🔴 Bearish Crossover")
        
        # Trend
        if df['Close'].iloc[-1] > df['MA_50'].iloc[-1]:
            st.markdown("**Trend (MA50):** 🟢 Uptrend")
        else:
            st.markdown("**Trend (MA50):** 🔴 Downtrend")
        
        # Bollinger Bands
        if df['Close'].iloc[-1] > df['BB_Upper'].iloc[-1]:
            st.markdown("**BB Position:** 🔴 Above Upper Band (Overbought)")
        elif df['Close'].iloc[-1] < df['BB_Lower'].iloc[-1]:
            st.markdown("**BB Position:** 🟢 Below Lower Band (Oversold)")
        else:
            st.markdown("**BB Position:** 🟡 Within Bands (Normal)")
        
        st.markdown("---")
        
        # Price Statistics
        st.markdown("### 📈 Price Statistics")
        high_24h = df['High'].iloc[-24:].max() if len(df) >= 24 else df['High'].max()
        low_24h = df['Low'].iloc[-24:].min() if len(df) >= 24 else df['Low'].min()
        avg_24h = df['Close'].iloc[-24:].mean() if len(df) >= 24 else df['Close'].mean()
        
        st.markdown(f"**24h High:** ${high_24h:,.2f}")
        st.markdown(f"**24h Low:** ${low_24h:,.2f}")
        st.markdown(f"**24h Average:** ${avg_24h:,.2f}")
        st.markdown(f"**24h Range:** ${high_24h - low_24h:,.2f}")
    
    with col_a2:
        st.markdown("### 🎯 Trading Recommendation")
        
        # Calculate recommendation score
        score = 0
        
        # RSI check
        if 30 < rsi_val < 70:
            score += 1
        elif rsi_val < 30:
            score += 2
        
        # MACD check
        if macd_val > macd_signal:
            score += 1
        
        # Trend check
        if df['Close'].iloc[-1] > df['MA_20'].iloc[-1]:
            score += 1
        
        # Overall recommendation
        if score >= 4:
            st.success("🟢 **STRONG BUY**")
            st.markdown("Multiple indicators suggest bullish momentum.")
        elif score >= 3:
            st.info("🟢 **BUY**")
            st.markdown("Indicators lean towards a buying opportunity.")
        elif score >= 2:
            st.warning("🟡 **HOLD**")
            st.markdown("Mixed signals. Consider waiting for clearer direction.")
        else:
            st.error("🔴 **CAUTION**")
            st.markdown("Bearish indicators detected. Consider reducing exposure.")
        
        st.markdown("---")
        
        st.markdown("### ⚠️ Risk Assessment")
        
        volatility = df['Volatility'].iloc[-1]
        avg_volatility = df['Volatility'].mean()
        
        if volatility > avg_volatility * 1.5:
            st.error("🔴 **High Volatility Risk**")
        elif volatility > avg_volatility:
            st.warning("🟡 **Moderate Volatility**")
        else:
            st.success("🟢 **Low Volatility**")
        
        st.markdown(f"Current Volatility: **{volatility:.4f}**")
        st.markdown(f"Average Volatility: **{avg_volatility:.4f}**")
    
    # Volume Analysis Chart
    st.markdown("---")
    st.markdown("### 📊 Volume Analysis")
    
    fig_vol = go.Figure()
    
    fig_vol.add_trace(go.Bar(
        x=df["Open time"],
        y=df["Volume"],
        name="Volume",
        marker_color='rgba(102, 126, 234, 0.7)'
    ))
    
    fig_vol.update_layout(
        title="Trading Volume Over Time",
        xaxis_title="Time",
        yaxis_title="Volume",
        template=plot_template,
        paper_bgcolor=paper_bg,
        plot_bgcolor=plot_bg,
        height=300
    )
    
    st.plotly_chart(fig_vol, use_container_width=True)

# ----------------
# FOOTER
# ----------------
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #a0aec0; padding: 2rem;'>
        <p>📊 <strong>Crypto Trading </strong> | Advanced Trading Dashboard</p>
        <p style='font-size: 0.95rem; margin-top: 0.5rem;'>💻 <strong>Created by Boughadi Mouad</strong></p>
    </div>
    """,
   unsafe_allow_html=True
)