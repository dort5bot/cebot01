##
#fr_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.fr_utils import get_fr_info

async def fr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        result = get_fr_info()
        await update.message.reply_text(result)
    except Exception:
        await update.message.reply_text("❌ /fr komutunda hata oluştu.")

def get_handler():
    return CommandHandler("fr", fr_command)
