import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

server = 'localhost'
database = 'AlexDB'
user = 'dataminer'
passw = os.environ['SERVDBPASS']
conn_string = f"mssql+pyodbc://{user}:{passw}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

engine = create_engine(conn_string)
Session = sessionmaker(engine)
session = Session()
