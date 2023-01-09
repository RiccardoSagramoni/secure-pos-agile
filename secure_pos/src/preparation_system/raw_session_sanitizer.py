from preparation_system.prepared_session_generator import PreparedSessionGenerator


class RawSessionSanitizer:

    def __init__(self, raw_session):
        self.raw_session = raw_session

    def detect_outliers(self):
        pass

    def correct_outliers(self):
        pass

    def detect_missing_attributes(self):
        pass

    def correct_missing_attributes(self):
        pass
