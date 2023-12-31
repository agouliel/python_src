import os, pyodbc
from flask import Flask

server = 'localhost'
database = 'AlexDB'
user = 'dataminer'
passw = os.environ['SERVDBPASS']

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + user + ';PWD=' + passw)
cursor = cnxn.cursor()

app = Flask(__name__)

######## USING CURSOR DIRECTLY ##########
#cursor.execute(stmt) / list1 = list(cursor)      / print(len(list1))
#cursor.execute(stmt) / list2 = cursor.fetchall() / print(len(list2))

######## USING A CURSOR VARIABLE ##########
#result and cursor is the same: <pyodbc.Cursor object at 0x102d4cab0>
#result = cursor.execute(stmt) / list3 = list(result)      / print(len(list3))
#result = cursor.execute(stmt) / list4 = result.fetchall() / print(len(list4))

stmt = "select name, object_id from sys.objects where [type] = 'U'"
tables = cursor.execute(stmt)

##### ROUTES #####
"""
@app.route('/users')
def get_users():
    stmt = 'select name, column_id from sys.columns where object_id = 1029578706'
    cursor.execute(stmt)
    columns = cursor.fetchall()

    # construct query
    q = 'select '
    for c in columns:
        q += f'{c[0]},'
    q = q[:-1]
    q += ' from users'

    cursor.execute(q)
    rows = cursor.fetchall()
    return {'data': [{c[0]:row[c[1]-1] for c in columns} for row in rows],}
"""
for table_row in tables:
    table_name = table_row[0]
    table_id = table_row[1]

    func_str = f"""def get_{table_name}():
    stmt = 'select name, column_id from sys.columns where object_id = {table_id}'
    cursor.execute(stmt)
    columns = cursor.fetchall()

    # construct query
    q = 'select '
    for c in columns:
        q += f'{{c[0]}},'
    q = q[:-1]
    q += ' from {table_name}'

    cursor.execute(q)
    rows = cursor.fetchall()
    return {{'data': [{{c[0]:row[c[1]-1] for c in columns}} for row in rows],}}"""
    
    exec(func_str)

    url_str = f"app.add_url_rule('/{table_name}', view_func=get_{table_name})"
    exec(url_str)