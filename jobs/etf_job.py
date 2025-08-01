# jobs/etf_job.py
from datetime import time
from utils.etf_utils import get_etf_summary

def etf_job(context):
    chat_id = context.job.chat_id
    try:
        summary = get_etf_summary()
        context.bot.send_message(chat_id=chat_id, text=summary, parse_mode="HTML")
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text="❌ ETF job hatası oluştu.")
        print(f"ETF Job Error: {e}")

def schedule_etf_job(job_queue):
    # Sabit kullanıcı ve zaman örneği
    chat_id = 123456789  # Değiştir
    job_queue.run_daily(etf_job, time=time(hour=11, minute=0), chat_id=chat_id)
