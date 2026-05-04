import time
import os
from sqlalchemy import create_engine, text
from extract import fetch_crypto_data
from transform import clean_and_analyze

from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

engine = create_engine(os.getenv("DB_URL"))

def get_last_silver_date():
    try:
        with engine.connect() as conn:
            res = conn.execute(text("SELECT MAX(extracted_at) FROM crypto_silver")).scalar()
            return res if res else "1900-01-01"
    except:
        return "1900-01-01"

if __name__ == "__main__":
    while True:
        try:
            # 1. Extract
            raw_df = fetch_crypto_data(["bitcoin", "ethereum"])
            raw_df.to_sql("crypto_prices", engine, if_exists="append", index=False)
            
            # 2. Transform
            last_date = get_last_silver_date()
            result = clean_and_analyze(engine, last_date)
            print(f"Cycle Complete: {result}")
            
        except Exception as e:
            print(f"Error: {e}")
            
        time.sleep(300) # 5 minute heartbeat