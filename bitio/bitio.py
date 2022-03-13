# brew install postgresql
# pip install pandas psycopg2 sqlalchemy

import csv, os, time
from io import StringIO

import pandas as pd
from sqlalchemy import create_engine

PG_USER = os.getenv('PG_USER')
PG_STRING = f"postgresql://{os.getenv('PG_USERNAME')}:{os.getenv('PG_PASSWORD')}@db.bit.io?sslmode=prefer"

# Create SQLAlchemy engine to manage database connection
engine = create_engine(PG_STRING)

# SQL for querying an entire table
sql = f'''SELECT * FROM "{PG_USER}/demo_repo"."atl_home_sales";'''

# Return SQL query as a pandas dataframe
with engine.connect() as conn:
    # Set 1 minute statement timeout (units are milliseconds)
  conn.execute("SET statement_timeout = 60000;")
  df = pd.read_sql(sql, conn)
print(df.head())