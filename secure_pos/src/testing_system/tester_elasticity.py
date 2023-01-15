import os
import threading
import time
import typing
from datetime import datetime

import pandas as pd
import requests
from pandas import read_csv

import utility
from communication import RestServer
from communication.api.json_transfer import ReceiveJsonApi

"""
TODO: ottenere uno timestamp per ogni classificatore
"""


#################################################
###                 UTILITY
#################################################
def replace_broken_label(label):
    if label['label'] not in ["ATTACK", "NORMAL"]:
        label['label'] = "ATTACK"
    return label


#################################################
###             TESTING SYSTEM
#################################################
class ElasticityTester:
    WINDOW_SIZE = 10
    NUM_SESSIONS_PER_CLASSIFIER = 100
    
    # [COMMUNICATION] Testing -> toolchain
    ingestion_system_url = "http://25.34.31.202:8000"
    
    # [COMMUNICATION] toolchain -> Testing
    semaphore = threading.Semaphore(0)

    received_response_list = []
    received_response_lock = threading.Lock()

    diff_timestamp_list = []
    diff_timestamp_lock = threading.RLock()  # lock for diff_timestamp_list
    
    # Constructor
    def __init__(self):
        # Parse dataset
        self.commercial = read_csv(os.path.join(utility.data_folder, 'commercial.csv'))
        self.geo = read_csv(os.path.join(utility.data_folder, 'geo.csv'))
        self.network = read_csv(os.path.join(utility.data_folder, 'network.csv'))
        self.label = read_csv(os.path.join(utility.data_folder, 'label.csv'))
        # Compute total number of available unique sessions
        self.TOTAL_NUM_SESSIONS = int(len(self.commercial) / self.WINDOW_SIZE)

    def __get_raw_session(self, start_index=0, window_size=10) -> typing.Tuple[list, list, list, dict]:
        return (
            self.commercial.iloc[start_index: start_index + window_size].to_dict(orient='records'),
            self.geo.iloc[start_index: start_index + window_size].to_dict(orient='records'),
            self.network.iloc[start_index: start_index + window_size].to_dict(orient='records'),
            self.label.iloc[start_index + window_size - 1].to_dict()
        )
    
    #################################################
    ###             COMMUNICATION
    #################################################
    def __handle_message(self, message: dict):
        with self.received_response_lock:
            self.received_response_list.append(message)
        self.semaphore.release()
        print("Received result")
    
    def __start_rest_server(self):
        server = RestServer()
        server.api.add_resource(
            ReceiveJsonApi,
            "/",
            resource_class_kwargs={
                'handler':
                    lambda message: self.__handle_message(message)
            }
        )
        server.run(port=1234)
    
    #################################################
    ###             DEVELOPMENT
    #################################################
    def __development_send_raw_sessions(self, how_many_classifiers, iteration):
        # for i in range(how_many_classifiers * self.NUM_SESSIONS_PER_CLASSIFIER):
        i = 0
        while True:
            session_index = i % self.TOTAL_NUM_SESSIONS

            i += 1
            
            # Get data from dataset
            commercial_data, geo_data, network_data, label_data = self.__get_raw_session(
                start_index=session_index * self.WINDOW_SIZE,
                window_size=self.WINDOW_SIZE
            )
            # Get session id
            session_id = label_data['event_id']
            label_data = replace_broken_label(label_data)
            print(f"iteration: {iteration}, {session_index + 1}) {label_data}")
            
            # Prepare data to send
            data = [
                {
                    'session_id': session_id,
                    'type': 'commercial',
                    'data': commercial_data
                },
                {
                    'session_id': session_id,
                    'type': 'geo',
                    'data': geo_data
                },
                {
                    'session_id': session_id,
                    'type': 'network',
                    'data': network_data
                },
                {
                    'session_id': session_id,
                    'type': 'label',
                    'data': label_data
                }
            ]
            
            # Send data to ingestion system
            for record in data:
                try:
                    requests.post(self.ingestion_system_url, json=record)
                except Exception as ex:
                    print(ex)
                    print(f"FAIL session_id: {session_id}")
                    break
            time.sleep(0.05)

            if len(self.received_response_list) == how_many_classifiers:
                break

    def __run_development_testing(self, iteration_num, how_many_classifiers):
        # Get timestamp
        start_timestamp = datetime.now()
        
        # Send raw sessions
        self.__development_send_raw_sessions(how_many_classifiers, iteration_num)

        for i in range(how_many_classifiers):
            # Wait for HTTP message
            self.semaphore.acquire()

            # Get difference between start and end timestamp
            end_timestamp_str = self.received_response_list[i]["timestamp"]
            end_timestamp = datetime.strptime(end_timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
            diff_timestamp = end_timestamp - start_timestamp
            diff = diff_timestamp.total_seconds()

            # Write performance on csv
            # id dello scenario | diff
            scenario_id = self.received_response_list[i]["scenario_id"]
            result_dict = {
                "iteration": iteration_num,
                "scenario_id": scenario_id,
                "diff": diff
            }
            print(f"iteration: {iteration_num}, Insert result" + str(diff) + " into csv")
            result_df = pd.DataFrame(result_dict, index=[0])
            result_df.to_csv("development.csv", sep=',', encoding="UTF-8", mode='a', header=False, index=False)

    def start_development_testing(self, how_many_classifiers_list: list) -> None:
        # Create development.csv file
        with open("development.csv", "w", encoding="UTF-8") as file:
            file.write("iteration,scenario_id,diff\n")
        
        # Start REST server
        flask_thread = threading.Thread(target=self.__start_rest_server, daemon=True)
        flask_thread.start()
        time.sleep(5)
        
        for i, num in enumerate(how_many_classifiers_list):
            self.__run_development_testing(i, num)
            while True:
                if len(self.received_response_list) == num:
                    break
            self.received_response_list = []
        
        # todo do stuff here?
        return
