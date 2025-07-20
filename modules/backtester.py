# modules/backtester.py

def backtest(df, strategy_fn, capital=1000, risk_per_trade=0.02):
    df = df.copy()
    df['Signal'] = df.apply(strategy_fn, axis=1)
    
    trades = []
    balance = capital

    for i in range(1, len(df)):
        row = df.iloc[i]
        prev_row = df.iloc[i - 1]

        signal = prev_row['Signal']
        price = row['Close']

        if signal == 'BUY':
            risk_amount = balance * risk_per_trade
            entry_price = price
            stop_loss = entry_price * 0.98
            take_profit = entry_price * 1.03
            outcome_price = row['Close']

            if outcome_price >= take_profit:
                pnl = risk_amount * 1.5  # Win 1.5R
            elif outcome_price <= stop_loss:
                pnl = -risk_amount       # Lose 1R
            else:
                pnl = 0  # No hit

            balance += pnl
            trades.append({'Date': row.name, 'Signal': signal, 'PnL': pnl, 'Balance': balance})

    return trades
