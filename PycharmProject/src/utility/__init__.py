import os


def get_project_folder() -> str:
    return os.path.realpath(__file__ + "/../../../")


def get_source_folder() -> str:
    return os.path.realpath(get_project_folder() + "/src")

def get_received_data_folder() -> str:
    return os.path.realpath(get_project_folder() + "/received_data")


def get_tests_folder() -> str:
    return os.path.realpath(get_project_folder() + "/test")
