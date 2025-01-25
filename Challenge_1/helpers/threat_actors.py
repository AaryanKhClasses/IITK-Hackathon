import re

class ThreatActors:
    def __init__(self, text, nlp):
        self.text = text
        self.nlp = nlp

    def get_info(self):
        unwanted_terms = ["IP", "PowerShell"]
        threat_actors = []
        for ent in self.nlp(self.text).ents:
            if ent.label_ in ["ORG", "GPE", "NORP"] and ent.text not in unwanted_terms:
                threat_actors.append(ent.text)
        pattern = re.compile(r'\bAPT\d+\b', re.IGNORECASE)
        threat_actors.extend(pattern.findall(self.text))
        
        return threat_actors
