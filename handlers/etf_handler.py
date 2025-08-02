# handlers/etf_handler.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.etf_utils import get_etf_data  # utils klasöründeki fonksiyon

async def etf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        result = await get_etf_data()
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text(f"ETF verisi alınamadı: {e}")

# main.py'de import edilecek handler fonksiyonu
def get_handler():
    return CommandHandler("etf", etf)
