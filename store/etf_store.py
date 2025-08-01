# store/etf_store.py
import json
import os

ETF_DATA_FILE = "data/etf_data.json"

def load_etf_data():
    if not os.path.exists(ETF_DATA_FILE):
        return {}
    with open(ETF_DATA_FILE, "r") as f:
        return json.load(f)

def save_etf_data(data):
    with open(ETF_DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)
