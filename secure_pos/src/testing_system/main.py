import os
import sys
import time
import typing

import requests
from pandas import DataFrame, read_csv

import utility


def parse_dataset() -> typing.Tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    return (
        read_csv(os.path.join(utility.data_folder, 'commercial.csv')),
        read_csv(os.path.join(utility.data_folder, 'geo.csv')),
        read_csv(os.path.join(utility.data_folder, 'network.csv')),
        read_csv(os.path.join(utility.data_folder, 'label.csv')),
    )


def get_data_for_testing(commercial, geo, network, label,
                         start_index=0, window_size=10) -> typing.Tuple[list, list, list, dict]:
    return (
        commercial.iloc[start_index: start_index + window_size].to_dict(orient='records'),
        geo.iloc[start_index: start_index + window_size].to_dict(orient='records'),
        network.iloc[start_index: start_index + window_size].to_dict(orient='records'),
        label.iloc[start_index + window_size - 1].to_dict()
    )


def replace_broken_label(label):
    if label['label'] not in ["ATTACK", "NORMAL"]:
        label['label'] = "NORMAL"
    return label


def main():
    commercial, geo, network, label = parse_dataset()
    window_size = 10
    
    for i in range(100):
        # Get data from dataset
        commercial_data, geo_data, network_data, label_data = get_data_for_testing(
            commercial, geo, network, label,
            start_index=i * window_size,
            window_size=window_size
        )
        # Get session id
        session_id = label_data['event_id']
        label_data = replace_broken_label(label_data)  # todo
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
                response = requests.post("http://127.0.0.1:8000/", json=record)
            except Exception as ex:
                print(ex)
                print(f"FAIL session_id: {session_id}")
                break
        time.sleep(2)


if __name__ == "__main__":
    main()
