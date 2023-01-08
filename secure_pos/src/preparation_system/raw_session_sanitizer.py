from preparation_system.prepared_session_generator import PreparedSessionGenerator


class RawSessionSanitizer:

    def __init__(self, raw_session):
        self.raw_session = raw_session

    def detect_outliers(self):
        self.correct_outliers()

    def correct_outliers(self):
        prepared_session_generator = PreparedSessionGenerator(self.raw_session)
        prepared_session_dict = prepared_session_generator.extract_features()

    def detect_missing_attributes(self):
        self.correct_missing_attributes()

    def correct_missing_attributes(self):
        self.detect_outliers()
