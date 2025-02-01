import re

class Iocs:
  def __init__(self, text, nlp):
    self.text = text
    self.nlp = nlp
    self.data = self.nlp(self.text)
    self.ip_pat = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')

  def get_ip_addresses(self):
    addresses = []
    for token in self.data:
      if (token.like_url and self.ip_pat.match(token.text)):
        addresses.append(self.ip_pat.findall(token.text)[0])
    return addresses

  def allow_domain(self, text):
    for i in [".exe", ".dll", ".sys", ".dat"]:
      if i in text:
        return False
    return True

  def get_domains(self):
    domains = []
    for token in self.data:
      if (token.like_url and not self.ip_pat.match(token.text) and self.allow_domain(token.text)):
        domains.append(token.text)
    return domains

  def get_file_hashes(self):
    return list(set(re.findall(r'\b([a-fA-F0-9]{32}|[a-fA-F0-9]{40}|[a-fA-F0-9]{64})\b', self.text)))

  def get_emails(self):
    return list(set(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,6}\b', self.text)))

  def get_info(self):
    iocs = {
      "IP addresses": self.get_ip_addresses(),
      "Domains": self.get_domains(),
      "File hashes": self.get_file_hashes(),
      "Email addresses": self.get_emails()
    }
    return iocs
