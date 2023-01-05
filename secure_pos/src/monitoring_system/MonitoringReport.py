
class MonitoringReport:

    conflicting_labels = 0
    compared_labels = 0
    max_consecutive_conflicting_labels = 0
    conflicting_labels_threshold = 10
    max_consecutive_conflicting_labels_threshold = 10

    def __int__(self):
        self.conflicting_labels = 0
        self.compared_labels = 0
        self.max_consecutive_conflicting_labels = 0
        self.conflicting_labels_threshold = 10
        self.max_consecutive_conflicting_labels_threshold = 10

    def set_conflicting_labels(self, tot):
        self.conflicting_labels = tot

    def set_compared_labels(self, tot):
        self.compared_labels = tot

    def set_max_consecutive_conflicting_labels(self, tot):
        self.max_consecutive_conflicting_labels = tot

    def to_dict(self):
        return {
            'conflicting_labels': self.conflicting_labels,
            'compared_labels': self.compared_labels,
            'max_consecutive_conflicting_labels': self.max_consecutive_conflicting_labels,
            'conflicting_labels_threshold': self.conflicting_labels_threshold,
            'max_consecutive_conflicting_labels_threshold': self.max_consecutive_conflicting_labels_threshold
        }
