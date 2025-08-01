# jobs/etf_job.py

from telegram.ext import ContextTypes
from datetime import time
from utils.etf_utils import get_etf_data, save_etf_to_csv

async def save_daily(context: ContextTypes.DEFAULT_TYPE):
    etf_data = get_etf_data(["btc", "eth"])
    save_etf_to_csv(etf_data)
    print("ETF verisi CSV'ye kaydedildi.")

def add_etf_job(job_queue):
    job_queue.run_daily(save_daily, time(hour=18, minute=0))
