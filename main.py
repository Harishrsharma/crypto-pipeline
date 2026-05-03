import time
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from extract import fetch_crypto_data
from transform import clean_and_analyze

load_dotenv()
engine = create_engine(os.getenv("DB_URL"))

def run_pipeline():
    print("🚀 Starting Pipeline Cycle...")
    
    # Task 1: Extract
    coins = ["bitcoin", "ethereum", "solana"]
    df_raw = fetch_crypto_data(coins)
    df_raw.to_sql("crypto_prices", engine, if_exists="append", index=False)
    print("✅ Extraction Complete")

    # Task 2: Transform
    status = clean_and_analyze(engine)
    print(f"✅ Transformation Complete: {status}")

if __name__ == "__main__":
    while True:
        try:
            run_pipeline()
        except Exception as e:
            print(f"❌ Pipeline Error: {e}")
        
        print("⏳ Waiting 5 minutes...")
        time.sleep(300)