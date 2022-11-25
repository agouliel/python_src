# Usage:
# import myconnection as c
# c.select('database', '* from table')

import pyodbc, os


myserver = 'servsrv\mssql2016'

try:
  myusername = os.environ['SERVDBUSER']
  mypassword = os.environ['SERVDBPASS']
except:
  myusername = input('Username: ')
  mypassword = input('Password: ')

def select(mydb, stmt):
  cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + myserver + ';DATABASE=' + mydb + ';UID=' + myusername + ';PWD=' + mypassword)

  cursor = cnxn.cursor()

  cursor.execute(f"select {stmt}")
  records = cursor.fetchall()
  print(records)
  cnxn.close()