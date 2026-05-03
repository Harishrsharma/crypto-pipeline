import pandas as pd

def clean_and_analyze(engine):
    # 1. Pull Raw Data
    df = pd.read_sql("SELECT * FROM crypto_prices", engine)
    
    if df.empty:
        return "No data to transform"

    # 2. Clean & Sort
    df = df.dropna(subset=['price'])
    df = df.sort_values(['coin_name', 'extracted_at'])

    # 3. Calculate Change (The Silver Logic)
    df['price_diff'] = df.groupby('coin_name')['price'].diff()
    
    # 4. Remove the first-row NaNs so our Silver table is clean
    df = df.dropna(subset=['price_diff'])

    # 5. Save to Silver Table
    df.to_sql("crypto_silver", engine, if_exists="replace", index=False)
    return f"Processed {len(df)} rows into Silver layer"