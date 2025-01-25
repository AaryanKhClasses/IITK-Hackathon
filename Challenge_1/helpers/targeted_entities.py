class TargetedEntities:
    def __init__(self, text, nlp):
        self.text = text
        self.nlp = nlp

    def get_info(self):
        entities = []
        for ent in self.nlp(self.text).ents:
            if ent.label_ in ["ORG", "GPE"]:
                entities.append(ent.text)
        return entities
