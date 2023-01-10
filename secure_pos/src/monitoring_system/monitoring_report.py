
class MonitoringReport:

    def __init__(self):
        self.conflicting_labels = 0
        self.compared_labels = 0
        self.max_consecutive_conflicting_labels = 0
        self.conflicting_labels_threshold = 10
        self.max_consecutive_conflicting_labels_threshold = 10

    def to_dict(self):
        return {
            'conflicting_labels': self.conflicting_labels,
            'compared_labels': self.compared_labels,
            'max_consecutive_conflicting_labels': self.max_consecutive_conflicting_labels,
            'conflicting_labels_threshold': self.conflicting_labels_threshold,
            'max_consecutive_conflicting_labels_threshold':
                self.max_consecutive_conflicting_labels_threshold
        }
