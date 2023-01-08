from typing import List

from data_objects.attack_risk_label import AttackRiskLabel
from data_objects.transaction import Transaction


class RawSession:
    def __init__(self, session_id: str, label: AttackRiskLabel, transactions: List[Transaction]):
        self.session_id = session_id
        self.attack_risk_label = label
        self.transactions = transactions
