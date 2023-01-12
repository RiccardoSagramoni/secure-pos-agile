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
class TestingSystem:
    WINDOW_SIZE = 10
    
    # [COMMUNICATION] Testing -> toolchain
    ingestion_system_url = "http://127.0.0.1:8000"
    
    # [COMMUNICATION] toolchain -> Testing
    semaphore = threading.Semaphore(0)
    received_response = None
    
    # Constructor
    def __init__(self):
        # Parse dataset
        self.commercial = read_csv(os.path.join(utility.data_folder, 'commercial.csv'))
        self.geo = read_csv(os.path.join(utility.data_folder, 'geo.csv'))
        self.network = read_csv(os.path.join(utility.data_folder, 'network.csv'))
        self.label = read_csv(os.path.join(utility.data_folder, 'label.csv'))
        
        self.TOTAL_NUM_SESSIONS = int(len(self.commercial) / self.WINDOW_SIZE)
    
    #
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
        self.received_response = message
        self.semaphore.release()

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
    def __development_send_raw_sessions(self, num_sessions=100):
        for i in range(num_sessions):
            session_index = i % self.TOTAL_NUM_SESSIONS
            
            # Get data from dataset
            commercial_data, geo_data, network_data, label_data = self.__get_raw_session(
                start_index=session_index * self.WINDOW_SIZE,
                window_size=self.WINDOW_SIZE
            )
            # Get session id
            session_id = label_data['event_id']
            label_data = replace_broken_label(label_data)
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
            print(f"{session_index}) {label_data}")
            # Send data to ingestion system
            for record in data:
                try:
                    requests.post(self.ingestion_system_url, json=record)
                except Exception as ex:
                    print(ex)
                    print(f"FAIL session_id: {session_id}")
                    break
            time.sleep(2)
    
    
    
    #
    def __run_development_testing(self, num_sessions=100):
        # Get timestamp
        start_timestamp = datetime.now()
        
        # Send raw sessions
        self.__development_send_raw_sessions(num_sessions)
        
        # Wait for HTTP message
        self.semaphore.acquire()
        
        # Get difference between start and end timestamp
        end_timestamp_str = self.received_response["timestamp"]
        end_timestamp = datetime.strptime(end_timestamp_str, '%hh:%mm:%ss:%ms')
        diff_timestamp = end_timestamp - start_timestamp
        diff = diff_timestamp.total_seconds()
        
        # Write performance on csv
        # id dello scenario | diff
        scenario_id = self.received_response["scenario_id"]
        result_dict = {
            "scenario_id": scenario_id,
            "diff": diff
        }
        result_df = pd.DataFrame(result_dict, index=[0])
        result_df.to_csv("development.csv", sep=',', encoding="UTF-8", mode='a')
    
    #
    def start_development_testing(self, num_session_list: list) -> None:
        # Start REST server
        flask_thread = threading.Thread(target=self.__start_rest_server, daemon=True)
        flask_thread.start()
    
        for num in num_session_list:
            self.__run_development_testing(num)
    
        # todo do stuff here?
        return



    #################################################
    ###                EXECUTION
    #################################################
    def __execution_send_raw_sessions(self,
                                      num_sessions,
                                      execution_length,
                                      monitoring_length):
        for i in range(num_sessions):
            session_index = i % self.TOTAL_NUM_SESSIONS
            
            # Get data from dataset
            commercial_data, geo_data, network_data, label_data = self.__get_raw_session(
                start_index=session_index * self.WINDOW_SIZE,
                window_size=self.WINDOW_SIZE
            )
            
            # Get session id
            session_id = label_data['event_id']
            label_data = replace_broken_label(label_data)
            print(f"{session_index}) {label_data}")
            
            # Prepare data to send
            data_to_send = [
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
                }
            ]
            label_to_send = {
                'session_id': session_id,
                'type': 'label',
                'data': label_data
            }
            
            # Send data to ingestion system
            for record in data_to_send:
                try:
                    requests.post(self.ingestion_system_url, json=record)
                except Exception as ex:
                    print(ex)
                    print(f"FAIL session_id: {session_id}")
                    break
            
            # Check if we must send the label
            if (session_index % (execution_length + monitoring_length)) >= execution_length:
                print(f"MONITORING {session_index}")
                try:
                    requests.post(self.ingestion_system_url, json=label_to_send)
                except Exception as ex:
                    print(ex)
                    print(f"FAIL label session_id: {session_id}")
                    break
            time.sleep(2)
    
    
    def __run_execution_testing(self, num_sessions, execution_len, monitoring_len):
        # Get timestamp
        start_timestamp = datetime.now()
    
        # Send raw sessions
        self.__execution_send_raw_sessions(num_sessions, execution_len, monitoring_len)
    
        # Wait for HTTP message
        self.semaphore.acquire()
    
        # Get difference between start and end timestamp
        end_timestamp_str = self.received_response["timestamp"]
        end_timestamp = datetime.strptime(end_timestamp_str, '%hh:%mm:%ss:%ms')
        diff_timestamp = end_timestamp - start_timestamp
        diff = diff_timestamp.total_seconds()
    
        # Write performance on csv
        # id dello scenario | diff
        scenario_id = self.received_response["scenario_id"]
        result_dict = {
            "scenario_id": scenario_id,
            "diff": diff
        }
        result_df = pd.DataFrame(result_dict, index=[0])
        result_df.to_csv("execution.csv", sep=',', encoding="UTF-8", mode='a')

    #
    def start_execution_testing(self, num_session_list: list, execution_len, monitoring_len) -> None:
        # Start REST server
        flask_thread = threading.Thread(target=self.__start_rest_server, daemon=True)
        flask_thread.start()
    
        for num in num_session_list:
            self.__run_execution_testing(num, execution_len, monitoring_len)
    
        # todo do stuff here?
        return


