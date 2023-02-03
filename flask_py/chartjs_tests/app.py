#https://www.mssqltips.com/sqlservertip/6597/flask-python-reporting-for-sql-server/

from flask import Flask, render_template, request, send_from_directory, url_for
import pandas as pd
import json
import sqlalchemy
import pyodbc
import os
from sqlalchemy import text # https://stackoverflow.com/questions/69490450/sqlalchemy-v1-4-objectnotexecutableerror-when-executing-any-sql-query-using-asyn

app = Flask(__name__ )

app.config['TEMPLATES_AUTO_RELOAD'] = True

def fetch_from_db():
    ServerName = 'servsrv' #Change to Your Server
    InstanceName = 'mssql2016' #Change to your Instance Name
    DatabaseName = 'AttendanceV1Dev'
    user = os.environ['SERVDBUSER']
    passw = os.environ['SERVDBPASS']

    MSSQLengine = sqlalchemy.create_engine('mssql+pyodbc://' + user + ':' + passw + '@' + ServerName + "\\" + InstanceName + '/' + DatabaseName + '?driver=ODBC+Driver+17+for+SQL+Server')
    print(str(MSSQLengine))

    ProductA = []
    ProductB = []
    ProductC = []
    ProductD = []

    with MSSQLengine.connect() as con:
        rs = con.execute(text("""SELECT YEAR(SALEDATE) AS [Year],SUM(SALESAMOUNT) AS SalesAmount,ProductName
FROM SalesData
GROUP BY YEAR(SALEDATE),ProductName
ORDER BY PRODUCTNAME,[YEAR]"""))
        for row in rs:
            if (row[2] == 'Product A'):
                ProductA.append(int(row[1]))
            if (row[2] == 'Product B'):
                ProductB.append(int(row[1]))
            if (row[2] == 'Product C'):
                ProductC.append(int(row[1]))
            if (row[2] == 'Product D'):
                ProductD.append(int(row[1]))


    nestDict = {
        'Product A': {'SalesData': ProductA},
        'Product B': {'SalesData': ProductB},
        'Product C': {'SalesData': ProductC},
        'Product D': {'SalesData': ProductD}
    }

    data = pd.DataFrame(nestDict)
    print(data)
    return data

@app.route('/')
def show_index():
    return render_template('chart.html')

@app.route('/report')
def show_chart():
    dbdata = fetch_from_db()
    return render_template('chartjs.html', data=dbdata)

@app.route('/reportnew')
def show_chartnew():
    dbdata = fetch_from_db()
    return render_template('chartnew.html', data=dbdata)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081)
