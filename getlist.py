#https://martinnoah.com/sharepoint-rest-api-with-python.html

#https://docs.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-lists-and-list-items-with-rest
#GET https://{site_url}/_api/web/lists/GetByTitle('List Title')
#Authorization: "Bearer " + accessToken
#Accept: "application/json;odata=verbose"

#https://stackoverflow.com/questions/22462352/sharepoint-rest-get-user-title-in-a-single-rest-query/22483105#22483105
#/_api/web/lists/getbytitle('Pages')/items(1)?$select=Author/Name,Author/Title&$expand=Author/Id

#https://ioniamangr.sharepoint.com/sites/IT/_layouts/15/settings.aspx
#https://ioniamangr.sharepoint.com/sites/IT/_layouts/15/viewlsts.aspx?view=14
#https://ioniamangr.sharepoint.com/sites/Technical/_api/web/siteusers
#https://ioniamangr.sharepoint.com/sites/Technical/_api/web/GetUserById(17) - Mousouraki


import requests
import json

app_id = '442e3155-f174-4f40-8d18-1b02baef7eec'
client_secret = 'oHUhJPWPnWwj+r+JA3mRN82HjpVTexYseWleH+pOg9I='

tenant =  'ioniamangr'
tenant_id = '06b26b33-98e4-47d8-8731-23f49f477e8b'  

client_id = app_id + '@' + tenant_id

data1 = { 'grant_type':'client_credentials', 'resource': "00000003-0000-0ff1-ce00-000000000000/" + tenant + ".sharepoint.com@" + tenant_id, 'client_id': client_id, 'client_secret': client_secret}

headers1 = {'Content-Type':'application/x-www-form-urlencoded'}

url1 = f"https://accounts.accesscontrol.windows.net/{tenant_id}/tokens/OAuth/2"
r1 = requests.post(url1, data=data1, headers=headers1)
json_data = json.loads(r1.text)

#print(json_data)

#{'token_type': 'Bearer', 'expires_in': '86399', 'not_before': '1619609303', 'expires_on': '1619696003', 
#'resource': '00000003-0000-0ff1-ce00-000000000000/ioniamangr.sharepoint.com@06b26b33-98e4-47d8-8731-23f49f477e8b', 'access_token': 'eyJ0...'

###################################################

headers2 = {'Authorization': "Bearer " + json_data['access_token'], 'Accept':'application/json;odata=verbose', 'Content-Type': 'application/json;odata=verbose'}

url2 = f"https://{tenant}.sharepoint.com/sites/IT/_api/web/lists/getbytitle('alex_list')/items"
r2 = requests.get(url2, headers=headers2)

print(r2.text)

#{"error":"invalid_request","error_description":"Token type is not allowed."}

###################################################


data3 = '''{ "__metadata": {"type": "SP.Data.alex_listListItem"},
    "Title": "PythonAPI", 
    "Name": "Mr Snake", 
    "Message": "Hello from Python"
}'''

r3 = requests.post(url2, headers=headers2, data=data3)

print(r3)
