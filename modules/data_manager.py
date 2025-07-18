# modules/data_manager.py

import pandas as pd


def load_data_from_csv(filepath='data/btc_15min.csv'):
    """
    Load yfinance-style CSV with multi-index header and convert to flat dataframe.
    """
    try:
        # Load multi-index columns (two header rows)
        df = pd.read_csv(filepath, header=[0, 1], index_col=0, parse_dates=True)

        # Flatten the multi-level columns
        df.columns = [col[0] for col in df.columns]

        # Rename columns to standard format
        df.rename(columns={
            "Close": "Close",
            "Open": "Open",
            "High": "High",
            "Low": "Low",
            "Volume": "Volume"
        }, inplace=True)

        # Ensure numeric conversion
        for col in ["Open", "High", "Low", "Close", "Volume"]:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df.dropna(inplace=True)

        return df

    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return pd.DataFrame()

def get_latest_candle(df):
    """
    Return the most recent OHLCV candle (last row of the DataFrame).
    """
    if not df.empty:
        return df.iloc[-1]
    return None
