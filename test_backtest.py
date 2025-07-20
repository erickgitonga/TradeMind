# test_backtest.py

import pandas as pd
import matplotlib.pyplot as plt
from modules.signal_generator import add_indicators, generate_signal

# Load your historical data (CSV or from DB)
df = pd.read_csv("data/btc_15min.csv")  # Replace with your actual source

# Add indicators and signals
df = add_indicators(df)
df['Signal'] = df.apply(generate_signal, axis=1)

# Backtesting setup
initial_balance = 1000
balance = initial_balance
in_position = False
entry_price = 0
position_size = 1  # Assume 1 unit per trade
wins = 0
losses = 0
trade_log = []

for i, row in df.iterrows():
    signal = row['Signal']
    price = row['Close']

    if signal == 'BUY' and not in_position:
        entry_price = price
        in_position = True
        trade_log.append({'Type': 'BUY', 'Price': price, 'Time': i})

    elif signal == 'SELL' and in_position:
        pnl = (price - entry_price) * position_size
        balance += pnl
        result = 'WIN' if pnl > 0 else 'LOSS'
        if pnl > 0:
            wins += 1
        else:
            losses += 1
        trade_log.append({
            'Type': 'SELL', 'Price': price, 'Time': i,
            'PnL': pnl, 'Result': result
        })
        in_position = False

# Summary
total_trades = wins + losses
win_rate = (wins / total_trades) * 100 if total_trades > 0 else 0
total_pnl = balance - initial_balance

print("📈 Backtest Summary:")
print(f"Total Trades: {total_trades}")
print(f"Wins: {wins} ({win_rate:.2f}%)")
print(f"Losses: {losses} ({100 - win_rate:.2f}%)")
print(f"Final Balance: ${balance:.2f}")
print(f"Total PnL: ${total_pnl:.2f}")

# Optional: plot signal entries on price chart
plt.figure(figsize=(12, 6))
plt.plot(df['Close'], label='Close Price')
buy_signals = df[df['Signal'] == 'BUY']
sell_signals = df[df['Signal'] == 'SELL']
plt.scatter(buy_signals.index, buy_signals['Close'], marker='^', color='green', label='Buy Signal')
plt.scatter(sell_signals.index, sell_signals['Close'], marker='v', color='red', label='Sell Signal')
plt.title("📈 TradeMind Signal Chart")
plt.xlabel("Time")
plt.ylabel("Price")
plt.legend()
plt.tight_layout()
plt.show()
