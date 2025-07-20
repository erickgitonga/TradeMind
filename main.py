# main.py

from modules.data_collector import get_market_data, save_data_to_csv
from modules.data_manager import load_data_from_csv
from modules.signal_generator import add_indicators
from modules.strategy_engine import combined_strategy  # ✅ Your strategy function
from modules.risk_manager import calculate_position_size, apply_risk_management
from modules.position_sizer import calculate_position_size
from modules.db_manager import connect_db, create_signals_table, save_signal
from modules.backtester import backtest
import pandas as pd

def run():
    print("📥 Collecting BTC-USD 15min market data...")

    # Step 1: Get market data
    data = get_market_data(symbol='BTC-USD', interval='15m', period='5d')

    if not data.empty:
        # Step 2: Save it
        save_data_to_csv(data, 'data/btc_15min.csv')

        # Step 3: Load it back
        df = load_data_from_csv('data/btc_15min.csv')

        # Step 4: Add indicators like RSI, MACD, BBands
        df = add_indicators(df)

        # Step 5: Apply strategy to each row
        signals = []
        for index, row in df.iterrows():
            signal = combined_strategy(row)
            signals.append(signal)

        df['Signal'] = signals  # Store decisions in the dataframe

        # Step 6: Print results
        print("\n📈 Market Data with Indicators:")
        print(df.tail())
        print("✅ Last Signal:", df['Signal'].iloc[-1])

        conn = connect_db()
        if conn:
            create_signals_table(conn)
            latest = df.iloc[-1]
            save_signal(conn,
        timestamp=latest.name,
        close_price=float(latest["Close"]),
        signal=latest["Signal"],
        open_price=float(latest["Open"]),
        high_price=float(latest["High"]),
        low_price=float(latest["Low"]),
        rsi=latest.get("RSI"),
        ema=latest.get("EMA"),
        bb_upper=latest.get("bb_upper"),
        bb_lower=latest.get("bb_lower")
    )


            conn.close()

    
        # Step 8: Simulate a trade
        latest_row = df.iloc[-1]
        signal = latest_row['Signal']
        current_price = latest_row['Close']
        entry_price = current_price  # for simulation

        # Simulate risk management decision
        risk_decision = apply_risk_management(
            signal=signal,
            entry_price=entry_price,
            current_price=current_price,
            stop_loss_pct=2,
            take_profit_pct=3
        )

        # Step 9: Calculate position size with fixed capital
        capital = 100  # dollars
        risk_percent = 2  # 2% per trade

        position_size = calculate_position_size(
            capital=capital,
            risk_percent=risk_percent,
            entry_price=entry_price,
            stop_loss_price=entry_price * (1 - 0.02)
        )

        # Show trade simulation output
        print("💼 Entry Price:", round(entry_price, 2))
        print("📌 Signal:", signal)
        print("📊 Risk Decision:", risk_decision)
        print("📐 Position Size (units):", position_size)

    else:
        print("❌ No market data received.")

if __name__ == "__main__":
    run()
