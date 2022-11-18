import pyodbc, os
# pip install pyodbc==4.0.34
# 4.0.35 fails with ImportError: dlopen(lib/python3.10/site-packages/pyodbc.cpython-310-darwin.so, 0x0002): symbol not found in flat namespace '_SQLAllocHandle'

myserver = 'servsrv\mssql2016' 
mydb = 'Hephaestus'
myusername = os.environ['SERVDBUSER']
mypassword = os.environ['SERVDBPASS']

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + myserver + ';DATABASE=' + mydb + ';UID=' + myusername + ';PWD=' + mypassword)
cursor = cnxn.cursor()

myquery = f"select * from Vessels"
cursor.execute(myquery)
row = cursor.fetchone()
print(row)
