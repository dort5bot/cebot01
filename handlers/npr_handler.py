##2
# /npr_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.npr_utils import check_npr

async def npr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper() if context.args else "BTCUSDT"
        result = check_npr(symbol)
        await update.message.reply_text(result)
    except Exception:
        await update.message.reply_text("❌ /npr komutunda hata oluştu.")

def get_handler():
    return CommandHandler("npr", npr_command)
