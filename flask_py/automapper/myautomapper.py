from flask import Flask
from sqlalchemy import inspect, select
from sqlalchemy.ext.automap import automap_base
from db import engine, session

app = Flask(__name__)

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

### ADD ANOTHER ROUTE WITH AN ADDITIONAL CLASS METHOD ###
def duplicate_username(cls):
    return cls.username + cls.username # the allowed calculations here are very limited
Users.duplicate_username = classmethod(duplicate_username)

@app.route('/users_duplicate_username')
def get_users_duplicate_username():
    q = select(Users.duplicate_username())
    result = session.execute(q)
    return {'data': [row[0] for row in result]}

### SAME AS ABOVE BUT WITH NORMAL METHOD ###
def id_and_username(self):
    return str(self.id) + ' ' + self.username # here calculations are allowed normally
Users.id_and_username = id_and_username

@app.route('/users_id_and_username')
def get_users_id_and_username():
    q = select(Users)
    result = session.execute(q)
    return {'data': [row[0].id_and_username() for row in result]}
