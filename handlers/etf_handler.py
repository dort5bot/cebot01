# handlers/etf_handler.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.etf_utils import generate_etf_report

async def etf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        report = await generate_etf_report()
        await update.message.reply_text(report, parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"ETF verisi alınamadı: {e}")

def get_handler():
    return CommandHandler("etf", etf)
