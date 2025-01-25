class Ttps:
    def __init__(self, text):
        self.text = text

    def get_info(self):
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
            if tactic in self.text:
                ttps.append({known_tactics[tactic]: tactic})
        return ttps
