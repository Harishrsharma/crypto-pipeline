import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# 1. Load the secrets and build the bridge
load_dotenv()
engine = create_engine(os.getenv("DB_URL"))

# 2. Write the SQL query
query = "SELECT * FROM bitcoin_prices;"

# 3. Read the data from Postgres into a new DataFrame
verification_df = pd.read_sql(query, engine)
print(verification_df)