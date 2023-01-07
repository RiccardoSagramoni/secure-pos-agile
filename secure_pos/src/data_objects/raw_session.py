import pandas

from data_objects.attack_risk_label import AttackRiskLabel
from data_objects.transaction import Transaction


class RawSession:
    transactions = []
    
    def __init__(self, session_id: str,
                 session_df: pandas.DataFrame, label: str):
        self.session_id = session_id
        self.attack_risk_label = AttackRiskLabel(label)
        
        for _, row in session_df.iterrows():
            self.transactions.append(
                Transaction(row)
            )
