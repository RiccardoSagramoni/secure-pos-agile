import os

import utility

PATH_DIRECTORY_CLASSIFIER = os.path.join(utility.data_folder, 'development_system/classifiers')

class ClassifierArchiver:

    def __init__(self, best_classifier_id):

        self.best_classifier_id = best_classifier_id

    def return_path_best_classifier(self) -> str:

        for classifier_filename in os.listdir(PATH_DIRECTORY_CLASSIFIER):
            # scan all the classifier and delete the one who are not the best
            if str(self.best_classifier_id) in classifier_filename:
                return os.path.join(PATH_DIRECTORY_CLASSIFIER, classifier_filename)


    def delete_remaining_classifiers(self):

        # scan the directory
        for classifier_filename in os.listdir(PATH_DIRECTORY_CLASSIFIER):
            # scan all the classifier and delete the one who are not the best
            if str(self.best_classifier_id) not in classifier_filename:
                if os.path.isfile(os.path.join(PATH_DIRECTORY_CLASSIFIER, classifier_filename)):
                    os.remove(os.path.join(PATH_DIRECTORY_CLASSIFIER, classifier_filename))


