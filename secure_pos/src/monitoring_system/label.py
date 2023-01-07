import json


class Label:

    def __init__(self, session_id, value, source):
        self.session_id = session_id
        self.source = source
        self.value = value

    def to_dict(self):
        return {
            'session_id': self.session_id,
            'source': self.source,
            'value': self.value
        }

    def load_from_file(self, label_file_path):
        with open(label_file_path, "r", encoding="UTF-8") as file:
            label_json = json.load(file)

        self.session_id = label_json['session_id']
        self.source = label_json['source']
        self.value = label_json['value']
