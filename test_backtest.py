from modules.data_manager import load_data_from_csv
from modules.signal_generator import add_indicators
from modules.strategy_engine import combined_strategy
from modules.backtester import backtest

import matplotlib.pyplot as plt

# Load and prepare data
df = load_data_from_csv('data/btc_15min.csv')
df = add_indicators(df)

# Run backtest
results = backtest(df, combined_strategy)

print("📊 Recent Backtest Results:")
for trade in results[-5:]:
    print(trade)

# Summary Stats
if results:
    wins = sum(1 for t in results if t['PnL'] > 0)
    losses = sum(1 for t in results if t['PnL'] < 0)
    total = len(results)
    final_balance = results[-1]['Balance']
    total_pnl = sum(t['PnL'] for t in results)

    print("\n📈 Backtest Summary:")
    print(f"Total Trades: {total}")
    print(f"Wins: {wins} ({(wins / total) * 100:.2f}%)")
    print(f"Losses: {losses} ({(losses / total) * 100:.2f}%)")
    print(f"Final Balance: ${final_balance:.2f}")
    print(f"Total PnL: ${total_pnl:.2f}")
else:
    print("❌ No trades executed.")

# Optional: Plot Equity Curve
try:
    equity = [t['Balance'] for t in results]
    dates = [t['Date'] for t in results]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, equity, label='Equity Curve', color='green')
    plt.title("📈 Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Balance ($)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()
except Exception as e:
    print(f"⚠️ Couldn't plot equity curve: {e}")
