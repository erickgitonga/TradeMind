# modules/strategy_engine.py

"""
This module contains all trading logic (signal strategies).
Each function returns a BUY, SELL, or HOLD signal.
"""

def simple_rsi_macd_strategy(row):
    """
    Strategy: Buy when RSI < 30 and MACD > MACD_signal.
              Sell when RSI > 70 and MACD < MACD_signal.
              Otherwise, Hold.
    """
    if row['RSI'] < 30 and row['MACD'] > row['MACD_signal']:
        return "BUY"
    elif row['RSI'] > 70 and row['MACD'] < row['MACD_signal']:
        return "SELL"
    else:
        return "HOLD"


def bollinger_band_strategy(row):
    """
    Strategy: Buy when price touches lower Bollinger Band.
              Sell when price touches upper Bollinger Band.
    """
    if row['Close'] <= row['bb_lower']:
        return "BUY"
    elif row['Close'] >= row['bb_upper']:
        return "SELL"
    else:
        return "HOLD"


def combined_strategy(row):
    if row['RSI'] < 50:
        return 'BUY'
    elif row['RSI'] > 50:
        return 'SELL'
    else:
        return 'HOLD'