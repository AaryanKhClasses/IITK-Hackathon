import re
import requests
import spacy
from bs4 import BeautifulSoup
import json

nlp = spacy.load("en_core_web_sm")

report_text = ''' 
The APT33 group, suspected to be from Iran, has launched a new campaign targeting the energy sector organizations. 
The attack utilizes Shamoon malware, known for its destructive capabilities. The threat actor exploited a vulnerability in the network perimeter to gain initial access. 
The malware was delivered via spear-phishing emails containing a malicious attachment. The malware's behavior was observed communicating with IP address 192.168.1.1 and domain example.com. The attack also involved lateral movement using PowerShell scripts. 
''' 

def get_iocs(text):
    iocs = {
        "IP addresses": re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text),
        "Domains": re.findall(r'\b[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b', text),
        "File hashes": re.findall(r'\b([a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64})\b', text),
        "Email addresses": re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b', text)
    }
    return iocs

def get_ttps(text):
    known_tactics = {
        "Initial Access": "TA0001",
        "Execution": "TA0002",
        "Persistence": "TA0003",
        "Privilege Escalation": "TA0004",
        "Defense Evasion": "TA0005",
        "Credential Access": "TA0006",
        "Discovery": "TA0007",
        "Lateral Movement": "TA0008",
        "Collection": "TA0009",
        "Exfiltration": "TA0010",
        "Command and Control": "TA0011",
        "Impact": "TA0040",
        "Resource Development": "TA0042",
        "Reconnaissance": "TA0043",
    }
    ttps = []
    for tactic in known_tactics:
        if tactic in text:
            ttps.append({known_tactics[tactic]: tactic})
    return ttps

def get_threat_actors(text):
    threat_actors = []
    for ent in nlp(text).ents:
        if ent.label_ == "ORG":
            threat_actors.append(ent.text)
    return threat_actors

def extract_malware_details(text):
    malware_details = []
    file_hashes = re.findall(r'\b([a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64})\b', text)
    for file_hash in file_hashes:
        response = requests.get(f'https://www.virustotal.com/gui/file/{file_hash}')
        soup = BeautifulSoup(response.content, 'html.parser')
        malware_name = soup.find('title').text
        malware_details.append({"name": malware_name, "hash": file_hash})
    return malware_details

def get_targeted_entities(text):
    entities = []
    for ent in nlp(text).ents:
        if ent.label_ in ["ORG", "GPE"]:
            entities.append(ent.text)
    return entities

data = {
    "IoCs": get_iocs(report_text),
    "TTPs": get_ttps(report_text),
    "Threat Actor(s)": get_threat_actors(report_text),
    "Malware": extract_malware_details(report_text),
    "Targeted Entities": get_targeted_entities(report_text),
}

print(json.dumps(data, indent=4))