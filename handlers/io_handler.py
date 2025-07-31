##2
#io_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.io_utils import get_io_analysis

async def io_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper() if context.args else "BTCUSDT"
        # timeframe parametresi io_utils'da kullanılmıyor, kaldırdım
        result = get_io_analysis(symbol)
        await update.message.reply_text(result)
    except Exception:
        await update.message.reply_text("❌ /io komutunda bir hata oluştu.")

def get_handler():
    return CommandHandler("io", io_command)
