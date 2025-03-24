import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']

def authenticate(token_path='./creds/token.pickle', credentials_path='./creds/credentials.json'):
    print("🔐 Authenticating with Google...")
    creds = None
    if os.path.exists(token_path):
        print("🔄 Loading saved credentials...")
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("♻️ Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            print("🌐 Starting OAuth2 flow. A browser window will open...")
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    print("✅ Authenticated successfully.")
    return creds
