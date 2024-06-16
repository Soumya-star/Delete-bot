import os.path
import pickle
import base64
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these SCOPES, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']


def authenticate_gmail():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        return service
    except HttpError as error:
        print(f'An error occurred: {error}')
        return None

def delete_all_emails(service):
    try:
        # Get the list of message IDs
        results = service.users().messages().list(userId='me').execute()
        messages = results.get('messages', [])

        if not messages:
            print('No messages found.')
            return

        for message in messages:
            msg_id = message['id']
            try:
                # Move the message to trash
                service.users().messages().delete(userId='me', id=msg_id).execute()
                print(f'Message with id: {msg_id} deleted.')
            except HttpError as error:
                print(f'An error occurred: {error}')

    except HttpError as error:
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    service = authenticate_gmail()
    if service:
        delete_all_emails(service)
