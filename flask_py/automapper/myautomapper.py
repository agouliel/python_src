import os
from flask import Flask
from sqlalchemy import create_engine, select, MetaData, inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

server = 'localhost'
database = 'AlexDB'
user = 'dataminer'
passw = os.environ['SERVDBPASS']
conn_string = f"mssql+pyodbc://{user}:{passw}@{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

app = Flask(__name__)

### DB ENGINE & SESSION ###
engine = create_engine(conn_string)
Session = sessionmaker(engine)
session = Session()

### AUTOMAP & REFLECTION ###
Base = automap_base()
Base.prepare(autoload_with=engine)
# https://docs.sqlalchemy.org/en/20/core/reflection.html#reflecting-database-objects
metadata_obj = MetaData()
metadata_obj.reflect(bind=engine)

insp = inspect(engine)
tables = insp.get_table_names()

##### MODELS #####
for table in tables:
    #User = Base.classes.users
    globals()[table.title()] = getattr(Base.classes, table)

    # https://stackoverflow.com/questions/24959589/get-table-columns-from-sqlalchemy-table-model
    #user_columns = [column.key for column in metadata_obj.tables['users'].c]
    globals()[f'{table}_columns'] = [column.key for column in metadata_obj.tables[table].c]

##### ROUTES #####
for table in tables:
    func_str = f"""def get_{table}():
    q = select({table.title()})
    query = session.execute(q)
    return {{'data': [{{column:getattr(row[0],column) for column in {table}_columns}} for row in query],}}"""
    #return {'data': [{'id':row[0].id,'username':row[0].username} for row in query],}
    exec(func_str)
    url_str = f"app.add_url_rule('/{table}', view_func=get_{table})"
    exec(url_str)
