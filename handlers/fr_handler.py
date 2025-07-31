##2
#fr_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.fr_utils import get_fund_report  # Burada get_fund_report kullanıyoruz

async def fr_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        symbol = args[0].upper() if args else "BTCUSDT"  # İstersen sembol argümanı da ekleyebilirsin
        result = get_fund_report(symbol)
        await update.message.reply_text(result)
    except Exception:
        await update.message.reply_text("❌ /fr komutunda hata oluştu.")

def get_handler():
    return CommandHandler("fr", fr_command)
