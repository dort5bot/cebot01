##
#etf_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.etf_utils import get_etf_info

async def etf_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        result = get_etf_info()
        await update.message.reply_text(result)
    except Exception:
        await update.message.reply_text("❌ /etf komutunda hata oluştu.")

def get_handler():
    return CommandHandler("etf", etf_command)
