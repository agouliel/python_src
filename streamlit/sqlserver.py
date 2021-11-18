import streamlit as st
import pandas as pd
import numpy as np
import pymssql #pyodbc
import os

st.title('SQL Server App')

#con = pyodbc.connect(
#            driver="SQL Server",
#            Server="sqlsrv03",
#            DATABASE="BIONIA",
#            UID="",
#            PWD="",
#)

#cursor = con.cursor()

myserver = 'sqlsrv03' #'servsrv\mssql2016' 
mydb = 'BIONIA'
myusername = os.environ['SERVDBUSER']
mypassword = os.environ['BNFTDBPASS']

con = pymssql.connect(server=myserver, user=myusername, password=mypassword, database=mydb)

df = pd.read_sql_query('select * from VSL', con)

st.dataframe(df)