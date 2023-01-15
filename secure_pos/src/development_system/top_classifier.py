class TopClassifier:

    def __init__(self, id_classifier, classifier, hyper_parameters):

        self.classifier_id = id_classifier
        self.classifier_filename = "classifier_number_" + str(id_classifier) + ".sav"
        self.hyper_parameters = hyper_parameters
        self.validation_error = classifier.validation_error
        self.training_error = classifier.training_error
