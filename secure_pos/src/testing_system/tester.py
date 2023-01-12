import os
import time
import typing
from datetime import datetime

import requests
from pandas import DataFrame, read_csv

import utility


def replace_broken_label(label):
    if label['label'] not in ["ATTACK", "NORMAL"]:
        label['label'] = "NORMAL"
    return label


class TestingSystem:
    ingestion_system_url = "http://127.0.0.1:8000"
    
    def __init__(self):
        # Parse dataset
        self.commercial = read_csv(os.path.join(utility.data_folder, 'commercial.csv'))
        self.geo = read_csv(os.path.join(utility.data_folder, 'geo.csv'))
        self.network = read_csv(os.path.join(utility.data_folder, 'network.csv'))
        self.label = read_csv(os.path.join(utility.data_folder, 'label.csv'))
    
    def get_raw_session(self, start_index=0, window_size=10) -> typing.Tuple[list, list, list, dict]:
        return (
            self.commercial.iloc[start_index: start_index + window_size].to_dict(orient='records'),
            self.geo.iloc[start_index: start_index + window_size].to_dict(orient='records'),
            self.network.iloc[start_index: start_index + window_size].to_dict(orient='records'),
            self.label.iloc[start_index + window_size - 1].to_dict()
        )
    
    def development_send_raw_sessions(self, num_sessions=100, window_size=10):
        for i in range(num_sessions):
            # Get data from dataset
            commercial_data, geo_data, network_data, label_data = self.get_raw_session(
                start_index=i * window_size,
                window_size=window_size
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
            print(f"{i}) {label_data}")
            # Send data to ingestion system
            for record in data:
                try:
                    requests.post(self.ingestion_system_url, json=record)
                except Exception as ex:
                    print(ex)
                    print(f"FAIL session_id: {session_id}")
                    break
            time.sleep(2)
        
    
    def run_development(self):
        # Get timestamp
        start_timestamp = datetime.now()
        
        # Send raw sessions
        
        # Wait for HTTP message
        
        # Get difference between start and end timestamp
        end_timestamp = datetime.now()
        diff_timestamp = end_timestamp - start_timestamp
        diff = diff_timestamp.total_seconds()
        
        # Write performance on csv
        
        pass
