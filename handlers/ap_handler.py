##
#ap_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.ap_utils import generate_ap_report
import logging

logger = logging.getLogger(__name__)

async def ap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        symbol = context.args[0].upper() if context.args else "BTCUSDT"
        timeframe = context.args[1] if len(context.args) > 1 else "1h"
        message = await update.message.reply_text(f"🔍 AP analizi başlatılıyor...\n\nSembol: {symbol}\nZaman dilimi: {timeframe}")
        result_text = generate_ap_report(symbol, timeframe)
        await message.edit_text(result_text)
    except Exception as e:
        logger.error(f"/ap komutu hatası: {e}")
        await update.message.reply_text("❌ AP analizi sırasında bir hata oluştu.")

def get_handler():
    return CommandHandler("ap", ap_command)
