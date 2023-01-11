import os
import sys
import json
import pandas as pd

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi


class CommunicationController:
    """
    Class that manage all the communication with other systems
    """

    def __init__(self, db_handler, url, segregation_system_controller):
        self.filename = './database/PreparedSession.json'
        self.db_handler = db_handler
        self.mode = 0
        self.sessions_nr = 0
        self.dev_system_url = url
        self.segregation_system_controller = segregation_system_controller

    def init_rest_server(self):
        """
        Method that create the server waiting for prepared sessions
        """
        server = RestServer()
        server.api.add_resource(ReceiveJsonApi,
                                "/",
                                resource_class_kwargs={
                                    'handler': self.handle_message,
                                })
        server.run()

    def handle_message(self, file_json):
        """
        Method that handle the incoming messages (preparation system)
        """
        # If our system is involved with data balancing and quality I cannot
        # accept more prepared sessions so the system discards them
        if self.mode == 1:
            sys.exit(0)

        self.db_handler.create_arrived_session_table()
        print(file_json)
        # Instantiate a data frame
        data_frame = pd.DataFrame(file_json,
                                  columns=['time_mean', 'time_median', 'time_std',
                                           'time_kurtosis', 'time_skewness', 'amount_mean',
                                           'amount_median', 'amount_std', 'amount_kurtosis',
                                           'amount_skewness', 'type', 'label'])

        ret = self.db_handler.insert_session(data_frame)

        # if we received 7 sessions the system can continue its execution,
        # otherwise it will terminate waiting for a new message
        if ret:
            self.sessions_nr += 1
            if self.sessions_nr == self.segregation_system_controller.\
                                        config_file.session_nr_threshold:
                self.sessions_nr = 0
                self.mode = 1
                self.db_handler.normalize_current_data()
                self.segregation_system_controller.check_balancing()

    def send_datasets(self, json_to_send):
        # TODO
        return


