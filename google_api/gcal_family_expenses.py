# https://github.com/googleworkspace/python-samples/tree/master/calendar/quickstart

from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    token_file = '.venv/token.json'
    cred_file = '.venv/cred.json'
    creds = None

    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_file, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # 'Z' indicates UTC time
    # 2021-11-29T13:31:42.108271Z
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    month_start = datetime.datetime.today().date().replace(day=1).isoformat() + 'T00:00:00.000000Z'

    events_result = service.events().list(calendarId='primary',
                                        timeMin=month_start,
                                        timeMax=now,
                                        #maxResults=10, 
                                        singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])
    mydict = {}
    for event in events:
      if event['summary'].startswith('*'): # family expenses start with asterisk
        start = event['start'].get('dateTime', event['start'].get('date'))
        startdt = start[:10]
        event_summary = event['summary'][2:] # remove asterisk
        summary_numbers = [int(s) for s in event_summary.split() if s.isdigit()]
        event_amnt = summary_numbers[0]

        if startdt in mydict: # this date already exists, so add the new data
          mydict[startdt] = [mydict[startdt][0]+event_amnt, mydict[startdt][1]+' + '+event_summary]
        else:
          mydict[startdt] = [event_amnt, event_summary]

    # add missing dates
    for i in range(1, 32):
      mydt = start[:8] + f'{i:02}'
      if mydt not in mydict:
        mydict[mydt] = []

    mysorteddict = {k: v for k, v in sorted(mydict.items(), key=lambda item: item[0])}

    for mykey in mysorteddict:
      if mysorteddict[mykey]:
        print(mykey+';'+mysorteddict[mykey][1]+';'+str(mysorteddict[mykey][0]))
      else:
        print(mykey+';'+';')

if __name__ == '__main__':
    main()
