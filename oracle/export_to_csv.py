# https://www.oracle.com/database/technologies/appdev/python/quickstartpython.html

import cx_Oracle
import pandas as pd

passw = input('Password: ')
conn = cx_Oracle.connect(user="admin", password=passw, dsn="db202109301512_high")

#cursor = conn.cursor()

sql_query = pd.read_sql_query('''
                              select * from tblsong
                              '''
                              ,conn)

df = pd.DataFrame(sql_query)
df.to_csv('data.csv', index = False)
