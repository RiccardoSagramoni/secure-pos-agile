import json


class Label:
    sessionId = None
    source = None
    value = None

    def __int__(self, session_id, value, source):
        self.sessionId = session_id
        self.source = source
        self.value = value

    def to_dict(self):
        return {
            'sessionId': self.sessionId,
            'source': self.source,
            'value': self.value
        }

    def load_from_file(self, label_file_path):
        with open(label_file_path, "r", encoding="UTF-8") as file:
            label_json = json.load(file)

        self.sessionId = label_json['sessionId']
        self.source = label_json['source']
        self.value = label_json['value']
