# ===============================
# ✅ Revize Edilmiş: etf_handler.py
# Komut: /etf
# ===============================

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.etf_utils import generate_etf_report

async def etf_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if args:
            arg = args[0].lower()
            result = generate_etf_report(arg)
        else:
            result = generate_etf_report()
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"❌ /etf komutunda hata oluştu: {e}")

def get_handler():
    return CommandHandler("etf", etf_command)
    
