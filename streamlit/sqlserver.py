import streamlit as st
import pandas as pd
import numpy as np
import pymssql #pyodbc
import os

st.title('Crew List')

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

df = pd.read_sql_query("""select v.VSL_NAME, c.LASTNAME, c.FIRSTNAME, /*s.vsl_name*/ n.descr nationality, r.DESCR crewrank, r.aa
from cwcrew c, cwcrewserv s, vsl v, cwpnation n, cwprank r
where c.id = s.cwcrew_id
and s.vsl_id = v.id
and c.cwpnation_id = n.id
and c.cwprank_id = r.id
and c.FL_ONBOARD = 1
and s.dated is null
order by 1,6""", con)

df.drop('aa', axis=1, inplace=True)

vessels = df['VSL_NAME'].drop_duplicates()
allv = pd.Series('All vessels')
vessels_all = vessels.append(allv)

vsl_choice = st.sidebar.selectbox('Vessel', vessels_all)

if vsl_choice=='All vessels':
  st.dataframe(df)
else:
  df_vsl = df.loc[df['VSL_NAME']==vsl_choice]
  df_vsl.drop('VSL_NAME', axis=1, inplace=True)
  df_vsl = df_vsl.reset_index(drop=True)
  st.dataframe(df_vsl)
