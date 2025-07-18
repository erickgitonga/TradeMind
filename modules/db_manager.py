import psycopg2
import pandas as pd

def connect_db():
    try:
        conn = psycopg2.connect(
            dbname="trademind",
            user="trademind_user",     # change if needed
            password="ERICK_FUTURE%",  # replace with actual password
            host="localhost",
            port="5432"
        )
        print("✅ Connected to PostgreSQL!")
        return conn
    except Exception as e:
        print("❌ Database connection failed:", e)
        return None

def create_signals_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS trade_signals (
                id SERIAL PRIMARY KEY,
                timestamp TIMESTAMPTZ,
                close_price NUMERIC,
                signal VARCHAR(10)
                
            );
        """)
        conn.commit()
        print("📦 Table 'trade_signals' ready.")

def save_signal(conn, timestamp, close_price, signal,
                open_price=None, high_price=None, low_price=None,
                rsi=None, ema=None, bb_upper=None, bb_lower=None):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO trade_signals (
                timestamp, close_price, signal,
                open_price, high_price, low_price,
                rsi, ema, bb_upper, bb_lower
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            timestamp, float(close_price), signal,
            float(open_price) if open_price else None,
            float(high_price) if high_price else None,
            float(low_price) if low_price else None,
            float(rsi) if rsi else None,
            float(ema) if ema else None,
            float(bb_upper) if bb_upper else None,
            float(bb_lower) if bb_lower else None
        ))
        conn.commit()
        print(f"💾 Saved signal {signal} at {timestamp}")

def load_signals_from_db():
    conn = connect_db()
    if conn is None:
        return pd.DataFrame()  # Return empty if no connection

    try:
        query = "SELECT * FROM trade_signals ORDER BY timestamp DESC"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        print("❌ Failed to load signals:", e)
        return pd.DataFrame()
    finally:
        conn.close()

