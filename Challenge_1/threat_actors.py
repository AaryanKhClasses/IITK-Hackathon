class ThreatActors:
  def __init__(self, text, nlp):
    self.text = text
    self.nlp = nlp

  def get_info(self):
    threat_actors = []
    for ent in self.nlp(self.text).ents:
        if ent.label_ == "ORG":
            threat_actors.append(ent.text)
    return threat_actors
