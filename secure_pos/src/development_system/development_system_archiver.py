import glob
import os

import utility

PATH_DIRECTORY_CLASSIFIER = os.path.join(utility.data_folder, 'development_system/classifiers')


class DevelopmentSystemArchiver:

    @staticmethod
    def return_path_best_classifier(best_classifier_id) -> str:
        for classifier_filename in os.listdir(PATH_DIRECTORY_CLASSIFIER):
            # scan all the classifier and delete the one who are not the best
            if str(best_classifier_id) in classifier_filename:
                return os.path.join(PATH_DIRECTORY_CLASSIFIER, classifier_filename)

    @staticmethod
    def delete_remaining_classifiers(best_classifier_id):
        # scan the directory
        for classifier_filename in os.listdir(PATH_DIRECTORY_CLASSIFIER):
            # scan all the classifier and delete the one who are not the best
            if str(best_classifier_id) not in classifier_filename and 'readme' not in classifier_filename:
                if os.path.isfile(os.path.join(PATH_DIRECTORY_CLASSIFIER, classifier_filename)):
                    os.remove(os.path.join(PATH_DIRECTORY_CLASSIFIER, classifier_filename))

    @staticmethod
    def delete_all_file_in_the_directory(path):

        types = ('**/*.json', '**/*.sav', '**/*.png')
        for files in types:
            pattern = os.path.join(path, files)
            for item in glob.iglob(pattern, recursive=True):
                if 'configuration' not in item and 'status' not in item:
                    os.remove(item)
