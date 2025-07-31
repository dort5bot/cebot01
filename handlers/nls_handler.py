##2
#nls_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.nls_utils import analyze_nls

async def nls_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper() if context.args else "BTCUSDT"
        result = analyze_nls(symbol)
        text = (
            f"{result['symbol']} - NLS Skoru: {result['nls_score']}%\n"
            f"Alış Değeri: {result['buy_value']}\n"
            f"Satış Değeri: {result['sell_value']}\n"
            f"Trend: {result['trend']}"
        )
        await update.message.reply_text(text)
    except Exception:
        await update.message.reply_text("❌ /nls komutunda hata oluştu.")

def get_handler():
    return CommandHandler("nls", nls_command)
