import re

class Iocs:
    def __init__(self, text):
        self.text = text

    def get_info(self):
        iocs = {
            "IP addresses": re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', self.text),
            "Domains": re.findall(r'\b[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b', self.text),
            "File hashes": re.findall(r'\b([a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64})\b', self.text),
            "Email addresses": re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b', self.text)
        }
        return iocs
