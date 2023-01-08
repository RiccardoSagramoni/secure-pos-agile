import pandas

from data_objects.attack_risk_label import AttackRiskLabel
from data_objects.raw_session import RawSession
from factory.transaction_factory import TransactionFactory


class RawSessionFactory:
    @staticmethod
    def generate_raw_session_from_dict(session_dict: dict) -> RawSession:
        # Generate list of transaction objects
        transactions = []
        for doc in session_dict['transactions']:
            transactions.append(
                TransactionFactory.generate_from_dict(doc)
            )
        # Generate raw session object
        return RawSession(
            session_dict['session_id'],
            session_dict['attack_risk_label'],
            transactions
        )
    
    @staticmethod
    def generate_raw_session_from_dataframe(session_id: str,
                                            session_df: pandas.DataFrame,
                                            label: str) -> RawSession:
        # Extract list of transactions
        transactions = []
        for _, row in session_df.iterrows():
            transactions.append(
                TransactionFactory.generate_from_series(row)
            )
        # Generate a RawSession object
        return RawSession(session_id, AttackRiskLabel(label), transactions)
