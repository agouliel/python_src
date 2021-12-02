# https://github.com/googleworkspace/python-samples/tree/master/calendar/quickstart
# pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib

from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

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
