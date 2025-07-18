import streamlit as st
import pandas as pd
import plotly.express as px
from modules.data_manager import load_data_from_csv
from modules.db_manager import load_signals_from_db



from modules.signal_generator import add_indicators
from modules.strategy_engine import combined_strategy
from modules.backtester import backtest

st.set_page_config(page_title="📊 TradeMind Dashboard", layout="wide")
st.title("📊 TradeMind BTC Signal Dashboard")

# 🔄 Load latest data from DB
df = load_signals_from_db()


# ✅ Show latest signal
if not df.empty:
    latest_signal = df.iloc[-1]["signal"]
    st.success(f"✅ Latest Signal: {latest_signal}")
else:
    st.warning("No signal data available.")

# 📉 Price Chart
if not df.empty:
    fig = px.line(df.sort_values("timestamp"), x="timestamp", y="close_price", title="📈 BTC Price Over Time")
    st.plotly_chart(fig, use_container_width=True)

# 🧾 Table View of Signals
columns_to_show = ['timestamp', 'close_price', 'signal']
extra_cols = ['open_price', 'high_price', 'low_price', 'rsi', 'ema', 'bb_upper', 'bb_lower']

for col in extra_cols:
    if col in df.columns:
        columns_to_show.append(col)

st.dataframe(df[columns_to_show].sort_values(by="timestamp", ascending=False).head(25))

# 🧪 Backtest Historical Data
st.header("🧪 Strategy Backtest")

try:
    hist_df = load_data_from_csv("data/btc_15min.csv")
    hist_df = add_indicators(hist_df)
    results = backtest(hist_df, combined_strategy)

    if results:
        result_df = pd.DataFrame(results)

        # 📊 Show last 10 trades
        st.subheader("📄 Recent Trades")
        st.dataframe(result_df.tail(10))

        # 📈 Plot equity curve
        st.subheader("💰 Equity Curve")
        fig_eq = px.line(result_df, x="Date", y="Balance", title="Equity Curve")
        st.plotly_chart(fig_eq, use_container_width=True)

        # 📋 Show performance summary
        total_return = result_df['Balance'].iloc[-1] - result_df['Balance'].iloc[0]
        wins = sum(1 for t in results if t['PnL'] > 0)
        losses = sum(1 for t in results if t['PnL'] < 0)
        win_rate = 100 * wins / (wins + losses) if (wins + losses) > 0 else 0

        st.markdown(f"**📈 Total Return:** `${total_return:.2f}`")
        st.markdown(f"**✅ Win Rate:** `{win_rate:.2f}%`")
        st.markdown(f"**🔢 Total Trades:** `{len(results)}`")

    else:
        st.warning("Backtest produced no trades.")

except Exception as e:
    st.error(f"Backtest failed: {e}")
