# handlers/etf_handler.py
from telegram.ext import CommandHandler
from utils.etf_utils import get_etf_summary

def etf_command(update, context):
    try:
        summary = get_etf_summary()
        update.message.reply_text(summary)
    except Exception as e:
        update.message.reply_text("❌ ETF verisi alınırken hata oluştu.")
        print(f"ETF Handler Error: {e}")

def get_handler():
    return CommandHandler("etf", etf_command)
