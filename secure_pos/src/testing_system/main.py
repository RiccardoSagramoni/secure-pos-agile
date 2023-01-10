import os
import threading
import time
from typing import Tuple

import requests

from pandas import read_csv, DataFrame

from utility import get_project_folder

data_folder = os.path.join(get_project_folder(), 'data')


def parse_dataset() -> Tuple[DataFrame, DataFrame, DataFrame, DataFrame]:
    return (
        read_csv(os.path.join(data_folder, 'commercial.csv')),
        read_csv(os.path.join(data_folder, 'geo.csv')),
        read_csv(os.path.join(data_folder, 'network.csv')),
        read_csv(os.path.join(data_folder, 'label.csv')),
    )


def get_data_for_testing(window_size) -> Tuple[list, list, list, dict]:
    commercial, geo, network, label = parse_dataset()
    return (
        commercial.head(window_size).to_dict(orient='records'),
        geo.head(window_size).to_dict(orient='records'),
        network.head(window_size).to_dict(orient='records'),
        label.iloc[window_size - 1].to_dict()
    )


def main():
    # Get data from dataset
    commercial, geo, network, label = get_data_for_testing(window_size=10)
    # Get session id
    session_id = label['event_id']
    # Prepare data to send
    data = [
        {
            'session_id': session_id,
            'type': 'commercial',
            'data': commercial
        },
        {
            'session_id': session_id,
            'type': 'geo',
            'data': geo
        },
        {
            'session_id': session_id,
            'type': 'network',
            'data': network
        },
        {
            'session_id': session_id,
            'type': 'label',
            'data': label
        }
    ]
    print("Invio!")
    # Send data to ingestion system
    for d in data:
        response = requests.post("http://127.0.0.1:8000/", json=d)
        print(response.text)
        time.sleep(1)
    return


if __name__ == "__main__":
    main()
