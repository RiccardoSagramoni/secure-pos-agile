class TopClassifier:

    def __init__(self, id_classifier, classifier):

        self.classifier_id = id_classifier
        self._mlp = classifier.mlp
        self.hyper_parameters = classifier.hyper_parameters
        self.validation_error = classifier.validation_error
        self.training_error = classifier.training_error

    def print(self):
        print("*********************************")
        print(f"id_classifier:{self.classifier_id}")
        print("self.hyper_parameters")
        print(self.hyper_parameters)
        print(f"validation_error:{self.validation_error}")
        print(f"training_error:{self.training_error}")
        print("*********************************")
