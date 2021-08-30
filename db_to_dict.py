import pymssql
import os

myserver = 'sqlsrv03'
mydb = 'BIONIA'
myusername = os.environ['SERVDBUSER']
mypassword = os.environ['BNFTDBPASS']

conn = pymssql.connect(server=myserver, user=myusername, password=mypassword, database=mydb)
cursor = conn.cursor()

select_query = """select v.VSL_NAME, v.VSL_DWT, f.loanamount
from vsl v, djangovessels_financialdets f
where v.id = f.vessel_id;"""

cursor.execute(select_query)

Fleet = {}

out = cursor.fetchall() # this returns a list of tuples
for row in out:

  GeneralInfoDict = {}
  loanDict = {}
  financialDict = {}

  GeneralInfoDict['Name'] = str(row[0])
  GeneralInfoDict['DWT'] = int(row[1])

  loanDict['loanamount'] = int(row[2])

  Fleet[str(row[0]).title()+'Data'] = {'GeneralInfo':GeneralInfoDict, 'loan':loanDict}
