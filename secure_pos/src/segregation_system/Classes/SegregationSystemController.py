import os
import sys
import json
import pandas as pd

from src.segregation_system.Classes.DataStatsExtractor import DataStatsExtractor
from src.communication import RestServer
from src.communication.api.file_transfer import ReceiveFileApi
from src.database import DBManager
from src.segregation_system.Classes.Plotter import Plotter


class SegregationSystemController:
    """Class that manage all the logic inside the Segregation System"""

    def __init__(self):
        self.sessions_nr = 0
        self.path_db = "./database/segregationSystemDatabase.db"
        #self.handle_message('database/PreparedSession.json')
        self.check_balancing()
        sys.exit(0)

    def handle_message(self, filename):
        """
        Function that handle the messages arrived from the preparation system
        """
        # Store the information inside the local database
        data_base_manager = DBManager.DBManager(self.path_db)

        # If this is the first execution we have to create our table
        data_base_manager.create_table(
            "CREATE TABLE IF NOT EXISTS ArrivedSessions"
            "(id INT PRIMARY KEY UNIQUE, time_mean FLOAT, time_std FLOAT, time_skew FLOAT,"
            "amount_1 FLOAT, amount_2 FLOAT, amount_3 FLOAT, amount_4 FLOAT, amount_5 FLOAT,"
            "amount_6 FLOAT, amount_7 FLOAT, amount_8 FLOAT, amount_9 FLOAT, amount_10 FLOAT,"
            "type INT, label INT)")

        # Insert the record inside the table
        with open(filename, 'r') as f:
            data = json.load(f)

        df = pd.DataFrame(data, columns=['id', 'time_mean', 'time_std', 'time_skew', 'amount_1', 'amount_2',
                                         'amount_3', 'amount_4', 'amount_5', 'amount_6', 'amount_7', 'amount_8',
                                         'amount_9', 'amount_10', 'type', 'label'])

        num_rows = len(df.index)

        ret = data_base_manager.insert(df, 'ArrivedSessions')
        # os.remove(filename)

        # if we received 7 sessions the system can continue its execution,
        # otherwise it will terminate waiting for a new message
        if ret:
            self.sessions_nr += num_rows
            if self.sessions_nr == 7:
                self.sessions_nr = 0
                self.check_balancing()
        return

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

    def check_balancing(self):
        """
        Function that calls the API that extracts the data
        and plot them in order to evaluate the data balancing
        :return: Null
        """
        data_extractor = DataStatsExtractor(self.path_db)
        labels = data_extractor.count_labels()
        value_0 = labels.pop(0).values[0][0]
        value_1 = labels.pop(0).values[0][0]

        print(value_0)
        print(value_1)

        plotter = Plotter()
        plotter.plot_data_balancing([value_0, value_1])
        return
