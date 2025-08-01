##etf_job##
from utils.etf_utils import fetch_and_store_etf_data

def etf_daily_job(context):
    fetch_and_store_etf_data()
