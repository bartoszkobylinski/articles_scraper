from __future__ import print_function
# import pickle
# import os.path
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request

# I have to added that
import base64
from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# import mimetypes


class EmailSender:

    def __init__(self, service):
        self.service = service

    def create_message(self, sender, to, subject, message_text):
        print(message_text)
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(
            message.as_bytes()).decode('ascii')}

    def send_message(self, message, user_id='me'):
        try:
            message = (self.service.users().messages().send(
                userId=user_id, body=message).execute())
            return message
        except errors.HttpError as error:
            print(f"An error occured: {error}")
