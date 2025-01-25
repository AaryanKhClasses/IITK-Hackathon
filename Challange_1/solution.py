import re
import requests
import spacy

nlp = spacy.load("en_core_web_sm")

report_text = ''' 
The APT33 group, suspected to be from Iran, has launched a new campaign targeting the energy sector organizations. 
The attack utilizes Shamoon malware, known for its destructive capabilities. The threat actor exploited a vulnerability in the network perimeter to gain initial access. 
The malware was delivered via spear-phishing emails containing a malicious attachment. The malware's behavior was observed communicating with IP address 192.168.1.1 and domain example.com. The attack also involved lateral movement using PowerShell scripts. 
''' 

def get_iocs(text):
    iocs = {
        "ip_addresses": re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', text),
        "domains": re.findall(r'\b[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b', text),
        "file_hashes": re.findall(r'\b([a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64})\b', text),
        "email_addresses": re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b', text)
    }
    return iocs

print(get_iocs(report_text))