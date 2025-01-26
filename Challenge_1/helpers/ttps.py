import re
import requests

response = requests.get('https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json')
attack_data = response.json()

class Ttps:
    def __init__(self, text, nlp):
        self.text = text
        self.nlp = nlp

    def get_info(self):
        techniques = []
        tactics = []

        for obj in attack_data.get('objects', []):
            if obj.get('type') == 'attack-pattern':
                techniques.append((obj['name'], obj['external_references'][0]['external_id']))
            elif obj.get('type') == 'x-mitre-tactic':
                tactics.append((obj['name'], obj['external_references'][0]['external_id']))

        text = re.sub('[^A-Za-z\s]+', '', self.text)
        text = text.lower()

        doc = self.nlp(text)
        keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]

        matched_techniques = [(tech, code) for tech, code in techniques if any(kw in tech.lower() for kw in keywords)]
        matched_tactics = [(tact, code) for tact, code in tactics if any(kw in tact.lower() for kw in keywords)]
    
        return {
            "Tactics": {tactic[1]: tactic[0] for tactic in matched_tactics},
            "Techniques": {technique[1]: technique[0] for technique in matched_techniques}
        }
