import spacy
import json
from helpers.iocs import Iocs
from helpers.ttps import Ttps
from helpers.malware_detect import Malware
from helpers.threat_actors import ThreatActors
from helpers.targeted_entities import TargetedEntities

nlp = spacy.load("en_core_web_sm")

report_text = ''' 
The APT33 group, suspected to be from Iran, has launched a new campaign targeting the energy sector organizations. 
The attack utilizes Shamoon malware, known for its destructive capabilities. The threat actor exploited a vulnerability in the network perimeter to gain initial access. 
The malware was delivered via spear-phishing emails containing a malicious attachment. The malware's behavior was observed communicating with IP address 192.168.1.1 and domain example.com. The attack also involved lateral movement using PowerShell scripts. 
''' 

iocs = Iocs(report_text)
ttps = Ttps(report_text)
threat_actors = ThreatActors(report_text, nlp)
malware = Malware(report_text)
targeted_entities = TargetedEntities(report_text, nlp)

data = {
    "IoCs": iocs.get_info(),
    "TTPs": ttps.get_info(),
    "Threat Actor(s)": threat_actors.get_info(),
    "Malware": malware.get_info(),
    "Targeted Entities": targeted_entities.get_info(),
}

print(json.dumps(data, indent=4))
