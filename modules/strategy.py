def generate_trade_signal(row):
    if (
        row['RSI'] < 30 and
        row['MACD'] > row['MACD_signal'] and
        row['Close'] < row['bb_lower']
    ):
        return 'BUY'

    elif (
        row['RSI'] > 70 and
        row['MACD'] < row['MACD_signal'] and
        row['Close'] > row['bb_upper']
    ):
        return 'SELL'

    else:
        return 'HOLD'
