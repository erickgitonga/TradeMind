import pandas as pd
import ta

import pandas as pd
import ta

def add_indicators(df):
    # Ensure Close is numeric
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')

    # ✅ EMA
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()

    # ✅ RSI (from ta)
    df['RSI'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()

    # ✅ MACD
    macd = ta.trend.MACD(close=df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()

    # ✅ SMA
    df['SMA_20'] = df['Close'].rolling(window=20).mean()

    # ✅ Bollinger Bands (from ta)
    bb = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['BB_upper'] = bb.bollinger_hband()
    df['BB_lower'] = bb.bollinger_lband()

    return df


    print(df.columns)

def generate_signal(row):
    if (
        row['EMA20'] > row['EMA50'] and
        row['RSI'] < 30 and
        row['Close'] < row['bb_lower']
    ):
        return 'BUY'
    elif (
        row['EMA20'] < row['EMA50'] and
        row['RSI'] > 70 and
        row['Close'] > row['bb_upper']
    ):
        return 'SELL'
    else:
        return 'HOLD'


 
    print(df['Signal'].value_counts())
    print(df[['EMA20', 'EMA50', 'RSI', 'BB_upper', 'BB_lower']].isnull().sum())

