import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage

SCOPES = ["https://www.googleapis.com/auth/gmail.send"] # readonly

creds = None
token_file = '.venv/token_gmail.json'
cred_file = '.venv/cred_gmail.json'

if os.path.exists(token_file):
  creds = Credentials.from_authorized_user_file(token_file, SCOPES)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
  if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
  else:
    flow = InstalledAppFlow.from_client_secrets_file(cred_file, SCOPES)
    creds = flow.run_local_server(port=0)

# creds, _ = google.auth.default()

# Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=777809651108-12g28i4jh6cthpbncfoh7dieo40jl3bq.apps.googleusercontent.com&redirect_uri=http%3A%2F%2Flocalhost%3A64659%2F&scope=https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fgmail.readonly&state=1sFXyH2ClwfksxV3mxEmh7bTo3JZFH&code_challenge=bDfc2oGcqG8iUK4L_ZR0DDBPbmfsINuWi2KcmQWz_zI&code_challenge_method=S256&access_type=offline

with open(token_file, 'w') as token:
    token.write(creds.to_json())

try:
  service = build("gmail", "v1", credentials=creds)

  message = EmailMessage()
  message.set_content("This is automated draft mail")

  message["From"] = "nikoskorompos80@gmail.com"

  message["To"] = "agoulielmos@digitech.marketing"
  encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
  create_message = {"raw": encoded_message}
  send_message = (
          service.users()
          .messages()
          .send(userId="me", body=create_message)
          .execute()
  )
  print('Sent')
except HttpError as error:
  print(f"An error occurred: {error}")