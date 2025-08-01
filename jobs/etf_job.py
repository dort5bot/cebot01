# jobs/etf_job.py
from utils.etf_utils import get_etf_snapshot
from store.etf_store import load_etf_data, save_etf_data
import datetime

def etf_update_job(context):
    data = load_etf_data()
    snapshot = get_etf_snapshot()

    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    data[now] = snapshot

    save_etf_data(data)
