#3 fr_scheduler.py
from telegram.ext import ContextTypes, Application
from utils.fr_utils import get_fund_report

async def fr_scheduler_job(context: ContextTypes.DEFAULT_TYPE):
    job_data = context.job.data
    user_id = job_data["user_id"]
    coin = job_data["coin"]

    try:
        report = get_fund_report(coin)
        await context.bot.send_message(chat_id=user_id, text=f"📊 Haftalık Fon Raporu ({coin}):\n\n{report}")
    except Exception as e:
        await context.bot.send_message(chat_id=user_id, text=f"⚠️ Rapor alınamadı: {e}")

def schedule_fr_check(application: Application, user_id: int, coin: str):
    application.job_queue.run_repeating(
        fr_scheduler_job,
        interval=86400,  # 24 saatte bir
        first=10,
        data={"user_id": user_id, "coin": coin.upper()}
    )
