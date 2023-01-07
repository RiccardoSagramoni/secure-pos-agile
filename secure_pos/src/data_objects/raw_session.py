import pandas

from data_objects.attack_risk_label import AttackRiskLabel
from data_objects.transaction import Transaction
from ingestion_system.configuration import Configuration


class RawSession:
    transactions = []
    
    def __init__(self, session_id: str,session_df: pandas.DataFrame,
                 label: str, conf: Configuration):
        self.configuration = conf
        self.session_id = session_id
        self.attack_risk_label = AttackRiskLabel(label)
        
        for _, row in session_df.iterrows():
            self.transactions.append(
                Transaction(row, conf)
            )
