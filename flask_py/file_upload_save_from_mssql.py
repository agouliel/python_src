import pyodbc, os

myserver = 'servsrv\mssql2016' 
mydb = 'AttendanceV1'

try:
  myusername = os.environ['SERVDBUSER']
  mypassword = os.environ['SERVDBPASS']
except:
  myusername = input('Username: ')
  mypassword = input('Password: ')

cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=' + myserver + ';DATABASE=' + mydb + ';UID=' + myusername + ';PWD=' + mypassword)

cursor = cnxn.cursor()

def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

sql_fetch_blob_query = "select commentFile from Vetting where vetid = 1500"
cursor.execute(sql_fetch_blob_query)
record = cursor.fetchall()
for row in record:
    print("Storing image on disk \n")
    photoPath = "alex.jpg"
    writeTofile(row[0], photoPath)

cursor.close()
cnxn.close()