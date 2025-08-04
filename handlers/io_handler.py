##2
#io_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.io_utils import get_market_insight_report, get_coin_insight_report

async def io_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if args:
            symbol = args[0].upper()
            result = get_coin_insight_report(symbol)
        else:
            result = get_market_insight_report()
        await update.message.reply_text(result, disable_web_page_preview=True)
    except Exception as e:
        await update.message.reply_text("❌ /io komutunda bir hata oluştu.")
        print(f"[IO HATA] {e}")

def get_handler():
    return CommandHandler("io", io_command)
