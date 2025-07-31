##
#nls_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.nls_utils import analyze_nls

async def nls_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper() if context.args else "BTCUSDT"
        result = analyze_nls(symbol)
        await update.message.reply_text(result)
    except Exception:
        await update.message.reply_text("❌ /nls komutunda hata oluştu.")

def get_handler():
    return CommandHandler("nls", nls_command)
