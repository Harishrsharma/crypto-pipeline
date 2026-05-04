import pandas as pd
from sqlalchemy import text

def get_start_point(engine):
    """Checks the Silver table for the last processed timestamp."""
    try:
        # We try to find the last record we processed
        query = text("SELECT MAX(extracted_at) FROM crypto_silver")
        with engine.connect() as conn:
            result = conn.execute(query).scalar()
            return result if result else "1900-01-01"
    except Exception:
        # If the table doesn't exist yet, we start from the beginning
        return "1900-01-01"

def clean_and_analyze(engine, start_point):
    # 1. Fetch data
    query_date = str(start_point)
    query = f"SELECT * FROM crypto_prices WHERE extracted_at >= '{query_date}'"
    df = pd.read_sql(query, engine)
    
    if df.empty:
        return "No data found in Bronze to process."

    # 🚨 THE MAGIC FIX: Convert the entire column to Timestamps!
    df['extracted_at'] = pd.to_datetime(df['extracted_at'], format='mixed')

    # 2. Sorting and Grouping
    df = df.sort_values(['coin_name', 'extracted_at'])
    df['price_diff'] = df.groupby('coin_name')['price'].diff()
    
    # 3. The Comparison
    start_dt = pd.to_datetime(start_point)
    
    if query_date == "1900-01-01":
        df_to_save = df
    else:
        # Now it's Timestamp vs Timestamp! 
        df_to_save = df[df['extracted_at'] > start_dt]

    if not df_to_save.empty:
        df_to_save.to_sql("crypto_silver", engine, if_exists="append", index=False)
        return f"Created/Updated Silver with {len(df_to_save)} rows"
    
    return "No new records to append."