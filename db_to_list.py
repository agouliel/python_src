from office365.runtime.auth.user_credential import UserCredential
from office365.sharepoint.client_context import ClientContext
import os, pymssql
from datetime import datetime

site_url = "https://ioniamangr.sharepoint.com/"
ctx = ClientContext(site_url).with_credentials(UserCredential(os.environ['SPUSER'], os.environ['SPUSERPASS']))
sp_lists = ctx.web.lists
s_list = sp_lists.get_by_title("Ports")

conn = pymssql.connect(server='sqlsrv03', user=os.environ['SERVDBUSER'], password=os.environ['BNFTDBPASS'], database='BIONIA')
cursor = conn.cursor()
cursor.execute("""select c.CNTRY_NAME, p.id pid, p.PRT_NAME,
c.id cid,
CASE
    WHEN p.lat is not null and p.lat1 is not null and p.lat2 is not null THEN
        CONCAT(p.lat,'°',p.LAT1,'''',p.LAT2,'''''',p.LAT_FL)
    WHEN p.lat is not null and p.lat1 is not null THEN
        CONCAT(p.lat,'°',p.LAT1,'''',p.LAT_FL)
    WHEN p.lat is not null THEN 
        CONCAT(p.lat,'°',p.LAT_FL)
    ELSE null 
END lat,
CASE
    WHEN p.lon is not null and p.lon1 is not null and p.lon2 is not null THEN
        CONCAT(p.LON,'°',p.LON1,'''',p.LON2,'''''',p.LON_FL)
    WHEN p.lon is not null and p.lon1 is not null THEN
        CONCAT(p.LON,'°',p.LON1,'''',p.LON_FL)
    WHEN p.lon is not null THEN 
        CONCAT(p.LON,'°',p.LON_FL)
    ELSE null 
END long
from ports p, CNTRY c
where p.CNTR_ID = c.ID;
""")

for row in cursor:
    
      port_properties = {
            'Title': str(row[0]),
            'Port': str(row[2]),
            'Latidute': str(row[4]),
            'Longidute': str(row[5]),
            'CountryCode': str(row[3]),
            'PortCode': str(row[1])
      }
      port_item = s_list.add_item(port_properties).execute_query()
