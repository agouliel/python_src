import os, pyodbc, re

def clean_file(filedata):
    filedata = re.sub('<div(.*?)>', '', filedata)
    filedata = re.sub('<span(.*?)>', '', filedata)
    filedata = re.sub('<font(.*?)>', '', filedata)
    filedata = re.sub('<strong(.*?)>', '', filedata)
    filedata = re.sub('<ol(.*?)>', '', filedata)
    filedata = re.sub('<li(.*?)>', '', filedata)
    filedata = re.sub('<ul(.*?)>', '', filedata)
    filedata = re.sub('<p(.*?)>', '', filedata)

    filedata = filedata.replace('</div>', '')
    filedata = filedata.replace('</span>', '')
    filedata = filedata.replace('</font>', '')
    filedata = filedata.replace('</strong>', '')
    filedata = filedata.replace('</ol>', '')
    filedata = filedata.replace('</li>', '')
    filedata = filedata.replace('</ul>', '')
    filedata = filedata.replace('</p>', '')

    return filedata

#db = 'AttendanceV1'
db = 'Hephaestus'
cnxn = pyodbc.connect(f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER=servsrv\mssql2016;DATABASE={db};UID={os.environ['SERVDBUSER']};PWD={os.environ['SERVDBPASS']}")
cursor = cnxn.cursor()
#stmt = "select ObjectId, comments from Vetting where vetid=6158 and comments is not null and comments<>''"
stmt = "select ProblemResolutionStepId, Remarks from ProblemResolutionSteps where QualitySafetyEventId = '1B17C58D-12AD-4C16-93B0-C6140D7F05F8'"
cursor.execute(stmt)
results = cursor.fetchall()

for row in results:
  #upd_stmt = f"""update vetting set comments='{clean_file(row[1]).replace("'", '')}' where vetid=6158 and objectid='{row[0]}'"""
  upd_stmt = f"""update ProblemResolutionSteps
  set Remarks = '{clean_file(row[1]).replace("'", '')}'
  where ProblemResolutionStepId = '{row[0]}'"""
  #print(upd_stmt)
  #print('------------')
  cursor.execute(upd_stmt)
  cnxn.commit()
cnxn.close()
