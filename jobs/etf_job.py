# jobs/etf_job.py
import os
import csv
from datetime import datetime
from telegram import Bot
from utils.etf_utils import get_etf_data

# Ortam değişkeninden admin ID alın (isteğe bağlı bildirim için)
ADMIN_ID = os.getenv("ADMIN_ID")

# 📌 ETF geçmiş verisini CSV'ye yaz
def save_etf_history(data: str):
    os.makedirs("data", exist_ok=True)
    csv_file = "data/etf_history.csv"
    with open(csv_file, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([now, data])

# 🕒 JobQueue üzerinden çağrılan görev
async def etf_daily_job(context):
    try:
        result = await get_etf_data()
        save_etf_history(result)

        # Eğer admin varsa mesaj gönder
        if ADMIN_ID:
            bot: Bot = context.bot
            await bot.send_message(chat_id=int(ADMIN_ID), text=f"[ETF Günlük Rapor]\n{result}")

    except Exception as e:
        if ADMIN_ID:
            await context.bot.send_message(chat_id=int(ADMIN_ID), text=f"[ETF JOB HATASI] {e}")
            
