# handlers/etf_handler.py2
from telegram import Update
from telegram.ext import ContextTypes
from utils.etf_utils import get_full_etf_report

async def etf_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        report = await get_full_etf_report()
    except Exception as e:
        report = f"Hata oluştu: {e}"
    await update.message.reply_text(report)
    
