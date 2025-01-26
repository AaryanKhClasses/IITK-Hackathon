from .threat_actors import ThreatActors

class TargetedEntities:
    def __init__(self, text, nlp):
        self.text = text
        self.nlp = nlp

    def get_info(self):
        unwanted_terms = ["IP", "PowerShell"]
        threat_actors = ThreatActors(self.text, self.nlp).get_info()
        entities = []
        for ent in self.nlp(self.text).ents:
            if ent.label_ in ["ORG", "GPE"] and ent.text not in threat_actors and ent.text not in unwanted_terms:
                entities.append(ent.text)
        
        sector_keywords = ["sector", "organization", "industry"]
        for chunk in self.nlp(self.text).noun_chunks:
            if any(keyword in chunk.text.lower() for keyword in sector_keywords):
                entities.append(chunk.text)
        entities = list(set(entities)) 
        return entities
