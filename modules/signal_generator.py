# modules/signal_generator.py

import pandas as pd
import ta

def add_indicators(df):
    """
    Add RSI and EMA indicators to the DataFrame.
    """
    # Calculate 14-period Relative Strength Index (RSI)
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()

    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # Calculate 20-period Exponential Moving Average (EMA)
    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()

    return df


def generate_signal(df):
    """
    Generate a basic signal using RSI and EMA.
    """
    if df.empty or 'RSI' not in df.columns:
        return "hold"

    latest = df.iloc[-1]

    # Example strategy rules:
    # - Buy if RSI < 30 and price is above EMA
    # - Sell if RSI > 70 and price drops below EMA
    # - Hold otherwise

    if latest['RSI'] < 30 and latest['Close'] > latest['EMA20']:
        return "buy"
    elif latest['RSI'] > 70 and latest['Close'] < latest['EMA20']:
        return "sell"
    else:
        return "hold"
        
def add_indicators(df):
    # Convert price columns to numeric
    df['Close'] = pd.to_numeric(df['Close'], errors='coerce')
    
    # SMA
    df['SMA_20'] = df['Close'].rolling(window=20).mean()

    # RSI
    df['RSI'] = ta.momentum.RSIIndicator(close=df['Close'], window=14).rsi()

    # MACD
    macd = ta.trend.MACD(close=df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()

    # Bollinger Bands
    bb = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()

    return df
