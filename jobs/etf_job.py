# jobs/etf_job.py
from utils.etf_utils import fetch_etf_data, save_etf_data_to_csv

def etf_daily_job(context):
    data = fetch_etf_data()
    save_etf_data_to_csv(data)
