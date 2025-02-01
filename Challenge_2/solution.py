import os
import pickle
import requests
import base64
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def getEmails():
    creds = None
    picklePath = os.path.dirname(os.path.realpath(__file__)) + '/token.pickle'
    credsPath = os.path.dirname(os.path.realpath(__file__)) + '/creds.json'

    if os.path.exists(picklePath):
        with open(picklePath, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credsPath, SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open(picklePath, 'wb') as token:
            pickle.dump(creds, token)

    gmail = build('gmail', 'v1', credentials=creds)
    res = gmail.users().messages().list(userId='me').execute()
    msgs = res.get('messages')
    for msg in msgs:
        text = gmail.users().messages().get(userId='me', id=msg['id']).execute()
        try:
            payload = text['payload']
            headers = payload['headers']

            for head in headers:
                if head['name'] == "Subject":
                    subject = head['value']
                if head['name'] == "From":
                    sender = head['value']

            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)

            soup = BeautifulSoup(decoded_data, "html.parser")
            body = soup.get_text()

            isPhishing = checkPhishing(sender, subject, body)
            if isPhishing:
                print("Phishing email detected!")
            else:
                print("Email is safe!")
        except:
            pass

phishingDomains = []
domains = requests.get("https://raw.githubusercontent.com/Phishing-Database/Phishing.Database/refs/heads/master/phishing-domains-ACTIVE.txt")
for domain in domains.text.splitlines():
    phishingDomains.append(domain)

def checkPhishing(sender, subject, body):
    for domain in phishingDomains:
        if domain in sender or domain in subject or domain in body:
            return True
    return False

getEmails()