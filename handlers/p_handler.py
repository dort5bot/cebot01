##
##p_handler.py

# handlers/p_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from utils.p_utils import generate_price_delta_analysis

async def p_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Lütfen bir sembol girin. Örnek: /p BTCUSDT")
        return

    symbol = context.args[0].upper()
    try:
        result = generate_price_delta_analysis(symbol)
        await update.message.reply_text(result, parse_mode="HTML")
    except Exception as e:
        await update.message.reply_text(f"Hata: {e}")
