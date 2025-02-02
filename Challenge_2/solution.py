import os
import torch
import pickle
import base64
import requests
from flask import Flask
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from transformers import BertTokenizer, BertForSequenceClassification

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

frontend_text = []

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
    res = gmail.users().messages().list(userId='me', maxResults=50).execute()
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
                frontend_text.append("""
                <div style="background-color: #ff0000; color: #ffffff; padding: 10px; margin: 10px;">
                    <h3>Phishing Email</h3>
                    <p>Sender: """ + sender + """</p>
                    <p>Subject: """ + subject + """</p>
                    <p>Body: """ + body + """</p>
                </div>
            """)
        except:
            pass

phishingDomains = []
domains = requests.get("https://raw.githubusercontent.com/Phishing-Database/Phishing.Database/refs/heads/master/phishing-domains-ACTIVE.txt")
for domain in domains.text.splitlines():
    phishingDomains.append(domain)

model_name = 'ealvaradob/bert-finetuned-phishing'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

def checkPhishing(sender, subject, body):
    for domain in phishingDomains:
        if domain in sender or domain in subject or domain in body:
            return True

    inputs = tokenizer(body, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1).item()
    if predicted_class == 1:
        return True

    return False

app = Flask(__name__)
@app.route('/')
def FrontEnd():
    getEmails()
    return "<br>".join(frontend_text)

app.run()
