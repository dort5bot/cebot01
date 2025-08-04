##3
#nls_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.io_utils import get_io_analysis, get_io_market_analysis

async def io_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if context.args:
            symbol = context.args[0].upper() + "USDT"
            result = get_io_analysis(symbol)
        else:
            result = get_io_market_analysis()
        await update.message.reply_text(result)
    except Exception:
        await update.message.reply_text("❌ /io komutunda bir hata oluştu.")

def get_handler():
    return CommandHandler("io", io_command)
