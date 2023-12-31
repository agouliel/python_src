import os
from flask import Flask
from sqlalchemy import create_engine, inspect, select
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

### AUTOMAP & INSPECTION ###
Base = automap_base()
Base.prepare(autoload_with=engine)

insp = inspect(engine)
tables = insp.get_table_names()
# the above can also be done by looping the classes:
# tables = []
# for c in Base.classes:
#   tables.append(c.__name__)

##### MODELS #####
for table in tables:
    #User = Base.classes.users
    globals()[table.title()] = getattr(Base.classes, table)

##### ROUTES #####
for table in tables:
    func_str = f"""def get_{table}():
    q = select({table.title()})
    query = session.execute(q)
    return {{'data': [{{column.key:getattr(row[0],column.key) for column in inspect(Base.classes.{table}).c}} for row in query],}}    
    """
    # simple case (use it as reference, in order to build the above):
    #return {'data': [{'id':row[0].id, 'username':row[0].username, 'homeaddress':row[0].homeaddress} for row in query],}

    # other way (using reflection instead of inspection):
    # https://docs.sqlalchemy.org/en/20/core/reflection.html#reflecting-database-objects
    #metadata_obj = MetaData()
    #metadata_obj.reflect(bind=engine)
    # https://stackoverflow.com/questions/24959589/get-table-columns-from-sqlalchemy-table-model
    #return {{'data': [{{column.key:getattr(row[0],column.key) for column in metadata_obj.tables[{table}].c}} for row in query],}}

    exec(func_str)
    
    url_str = f"app.add_url_rule('/{table}', view_func=get_{table})"
    exec(url_str)
