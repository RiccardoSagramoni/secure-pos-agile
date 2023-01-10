import os
import sys
import json
import pandas as pd

from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi
from database.DBManager import DBManager


class CommunicationController:
    """
    Class that manage all the communication with other systems
    """

    def __init__(self, db_semaphore, path_db, url, segregation_system_controller):
        self.db_semaphore = db_semaphore
        self.filename = './database/PreparedSession.json'
        self.path_db = path_db
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
                                    'filename': self.filename
                                })
        server.run()

    def handle_message(self):
        """
        Method that handle the incoming messages (preparation system)
        """
        # If our system is involved with data balancing and quality I cannot
        # accept more prepared sessions so the system discards them
        if self.mode == 1:
            os.remove(self.filename)
            sys.exit(0)

        # Store the information inside the local database
        data_base_manager = DBManager(self.path_db)

        # To avoid concurrency
        self.db_semaphore.acquire()
        # If this is the first execution we have to create our table
        data_base_manager.create_table(
            "CREATE TABLE IF NOT EXISTS ArrivedSessions"
            "(id VARCHAR(80) PRIMARY KEY, time_mean FLOAT, time_std FLOAT, time_skew FLOAT,"
            "amount_1 FLOAT, amount_2 FLOAT, amount_3 FLOAT, amount_4 FLOAT, amount_5 FLOAT,"
            "amount_6 FLOAT, amount_7 FLOAT, amount_8 FLOAT, amount_9 FLOAT, amount_10 FLOAT,"
            "type INT, label VARCHAR(20))")
        self.db_semaphore.release()

        # Insert the record inside the table
        with open(self.filename, 'r', encoding='utf-8') as opened_file:
            data = json.load(opened_file)

        # Error checking
        if not data:
            print("Error during message receiving, data not found.")
            sys.exit(-1)

        # Instantiate a data frame
        data_frame = pd.DataFrame(data,
                                  columns=['id', 'time_mean', 'time_std', 'time_skew',
                                           'amount_1', 'amount_2', 'amount_3', 'amount_4',
                                           'amount_5', 'amount_6', 'amount_7', 'amount_8',
                                           'amount_9', 'amount_10', 'type', 'label'])

        self.db_semaphore.acquire()
        ret = data_base_manager.insert(data_frame, 'ArrivedSessions')
        self.db_semaphore.release()

        # os.remove(self.filename) TODO remove comment

        # if we received 7 sessions the system can continue its execution,
        # otherwise it will terminate waiting for a new message
        if ret:
            self.sessions_nr += 7
            if self.sessions_nr == 7:
                self.sessions_nr = 0
                self.mode = 1
                print('ciao')
                self.segregation_system_controller.check_balancing(self)

    def send_datasets(self, json_to_send, url):
        # TODO
        return
