import sys

import pandas as pd

from src.segregation_system.Classes.DataStatsExtractor import DataStatsExtractor
from src.communication import RestServer
from src.communication.api.file_transfer import ReceiveFileApi
from src.database import DBManager


class SegregationSystemController:
    """Class that manage all the logic inside the Segregation System"""

    def __init__(self):
        self.sessions_nr = 0
        self.database_exists = False
        self.prep_session_schema = "./../Json_schema/prep_session_schema.json"
        self.server_start()

    def handle_message(self, filename):
        """
        Function that handle the messages arrived from the preparation system
        """
        # Store the information inside the local database
        data_base_manager = DBManager.DBManager("../utility/segregationSystemDatabase.db")

        # If this is the first execution we have to create our table
        if not self.database_exists:
            data_base_manager.create_table(
                "CREATE TABLE ArrivedSessions "
                "(id TEXT PRIMARY KEY UNIQUE, time_mean FLOAT, time_std FLOAT, time_skew FLOAT,"
                "amount_1 FLOAT, amount_2 FLOAT, amount_3 FLOAT, amount_4 FLOAT, amount_5 FLOAT,"
                "amount_6 FLOAT, amount_7 FLOAT, amount_8 FLOAT, amount_9 FLOAT, amount_10 FLOAT,"
                "label INT, type INT)")

        # From now on the table creation is no longer needed
        self.database_exists = True

        # Insert the record inside the table
        data_frame = pd.read_json(filename)
        ret = data_base_manager.insert(
            data_frame, 'ArrivedSessions')
        # if we received 7 sessions the system can continue its execution,
        # otherwise it will terminate waiting for a new message
        if ret:
            self.sessions_nr += 1
            if self.sessions_nr == 7:
                self.sessions_nr = 0
                data = data_base_manager.read_sql("SELECT * FROM ArrivedSession WHERE type == -1")
                self.check_balancing(data)

    def server_start(self):
        """
        Function that create the server waiting for prepared sessions
        """
        # The first step is to manage all the sessions that the
        # Preparation system will send and wait until a sufficient amount of sessions are arrived
        filename = 'PreparedSession.json'

        # Instantiate server
        server = RestServer()
        server.api.add_resource(ReceiveFileApi,
                                "/",
                                resource_class_kwargs=dict(
                                    filename=filename,
                                    handler=lambda: self.handle_message(filename)))
        server.run(debug=True)

        sys.exit(0)

    def check_balancing(self, data):
        # TODO Create first the ExtractDataStats first
        data_extractor = DataStatsExtractor(data)


