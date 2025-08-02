# handlers/p_handler.py

from telegram import Update
from telegram.ext import ContextTypes
from utils.p_utils import get_price_summary, get_detailed_analysis

async def price_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coins = context.args
    if not coins:
        await update.message.reply_text("Lütfen en az bir coin girin. Örnek: /p BTC ETH")
        return

    response = get_price_summary(coins)
    await update.message.reply_text(response)

async def price_detailed_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coins = context.args
    if not coins:
        await update.message.reply_text("Lütfen en az bir coin girin. Örnek: /pd BTC ETH")
        return

    response = get_detailed_analysis(coins)
    await update.message.reply_text(response)
