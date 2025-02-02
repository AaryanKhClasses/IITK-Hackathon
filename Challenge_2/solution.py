# import libraries
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

# define scopes of Gmail API
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

frontend_text = []
maxRes = 50

def getEmails():
    creds = None

    # get the path of the token.pickle and creds.json
    picklePath = os.path.dirname(os.path.realpath(__file__)) + '/token.pickle'
    credsPath = os.path.dirname(os.path.realpath(__file__)) + '/creds.json'

    # if the token.pickle exists, load the credentials
    if os.path.exists(picklePath):
        with open(picklePath, 'rb') as token:
            creds = pickle.load(token)
    
    # if there are no valid credentials, get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credsPath, SCOPES)
            creds = flow.run_local_server(port=0)
        
        # save the credentials for future use
        with open(picklePath, 'wb') as token:
            pickle.dump(creds, token)

    # build the Gmail API and get the messages
    gmail = build('gmail', 'v1', credentials=creds)
    res = gmail.users().messages().list(userId='me', maxResults=maxRes).execute()
    msgs = res.get('messages')
    for msg in msgs:
        # for each message get the text
        text = gmail.users().messages().get(userId='me', id=msg['id']).execute()
        try:
            # get the payload headers of the message
            payload = text['payload']
            headers = payload['headers']

            # get the sender and subject of the message
            for head in headers:
                if head['name'] == "Subject":
                    subject = head['value']
                if head['name'] == "From":
                    sender = head['value']

            # get the body of the message
            parts = payload.get('parts')[0]
            data = parts['body']['data']
            data = data.replace("-","+").replace("_","/")
            decoded_data = base64.b64decode(data)

            soup = BeautifulSoup(decoded_data, "html.parser")
            body = soup.get_text()

            # check if the email is phishing using the checkPhishing() function
            isPhishing = checkPhishing(sender, subject, body)
            if isPhishing:
                # append the phishing email to the frontend_text list
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

# get the phishing domains using the Phishing.Database
phishingDomains = []
domains = requests.get("https://raw.githubusercontent.com/Phishing-Database/Phishing.Database/refs/heads/master/phishing-domains-ACTIVE.txt")
for domain in domains.text.splitlines():
    phishingDomains.append(domain)

# get the pre-loaded BERT phishign model and tokenizer
model_name = 'ealvaradob/bert-finetuned-phishing'
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name, num_labels=2)

def checkPhishing(sender, subject, body):
    for domain in phishingDomains:
        # if the domain is in the sender, subject or body, return True
        if domain in sender or domain in subject or domain in body:
            return True

    # check if the email is phishing using the BERT model
    inputs = tokenizer(body, return_tensors='pt', max_length=512, truncation=True, padding='max_length')
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=1)
    predicted_class = torch.argmax(probabilities, dim=1).item()
    if predicted_class == 1:
        return True

    return False

# create a Flask app
app = Flask(__name__)
@app.route('/')
def FrontEnd():
    # on loading the flask page, execute the getEmails() function and display them
    getEmails()
    return "<center><h1>Phishing Emails</h1></center>" + "<br>".join(frontend_text)

# run the Flask app on script execution
app.run()
