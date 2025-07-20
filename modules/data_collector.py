import yfinance as yf
import pandas as pd

def get_market_data(symbol='BTC-USD', interval='15m', period='5d'):
    try:
        data = yf.download(symbol, interval=interval, period=period, progress=False)
        data.dropna(inplace=True)
        return data
    except Exception as e:
        print(f"❌ Error fetching market data: {e}")
        return pd.DataFrame()

def save_data_to_csv(data, filename='data/market_data.csv'):
    try:
        data.to_csv(filename)
        print(f"✅ Data saved to {filename}")
    except Exception as e:
        print(f"❌ Error saving data: {e}")
