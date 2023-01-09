class TopClassifier:

    def __init__(self, id_classifier, mlp, validation_error, **selected_hyper_parameters):

        self.id_classifier = id_classifier
        self.mlp = mlp
        self.hyper_parameters = selected_hyper_parameters
        self.validation_error = validation_error

    def print(self):
        print("*********************************")
        print(f"id_classifier:{self.id_classifier}")
        print("self.hyper_parameters")
        print(self.hyper_parameters)
        print(f"Validation Error:{self.validation_error}")
        print("*********************************")
