##
#io_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.io_utils import get_io_analysis

async def io_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper() if context.args else "BTCUSDT"
        timeframe = context.args[1] if len(context.args) > 1 else "1h"
        result = get_io_analysis(symbol, timeframe)
        await update.message.reply_text(result)
    except Exception:
        await update.message.reply_text("❌ /io komutunda bir hata oluştu.")

def get_handler():
    return CommandHandler("io", io_command)
