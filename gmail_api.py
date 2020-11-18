import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from email.message import EmailMessage
import base64

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
          'https://www.googleapis.com/auth/gmail.send']


def create_message(sender, to, subject, msg):
    message = EmailMessage()
    message.set_content(msg)
    message['To'] = to
    message['From'] = sender
    message['Subject'] = subject

    # Base 64 encode
    b64_bytes = base64.urlsafe_b64encode(message.as_bytes())
    b64_string = b64_bytes.decode()
    return {'raw': b64_string}


def send_message(service, user_id, message):
    message = (service.users().messages().send(userId=user_id,
                                               body=message).execute())
    print('Message Id: %s' % message['id'])
    return message


def send_twitter_email(tw_msg, today):
    """
    Send an email to myself containing tw_msg.

    :param tw_msg: Text-form message to send
    :param today: Date today
    :return: None
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
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('gmail', 'v1', credentials=creds)

    # Example send mail


    msg = create_message("charlesjgallagher15@gmail.com",
                         "charlesjgallagher15@gmail.com",
                         f"Twitter update: {today}", tw_msg)
    send_message(service, 'me', msg)


