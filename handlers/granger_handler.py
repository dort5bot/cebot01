# 📂 handlers/granger_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from utils.stats import (
    granger_test, granger_matrix, cointegration_matrix,
    correlation_matrix, var_matrix, leader_matrix
)

async def granger_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Kullanım:\n/g COIN1 COIN2\n/g matrix COIN1 COIN2 ...")
        return

    cmd = args[0].lower()
    coins = [arg.upper() for arg in args if arg.upper().isalpha()]

    if cmd == "matrix":
        await update.message.reply_text(granger_matrix(coins))
    elif cmd == "cointegration":
        await update.message.reply_text(cointegration_matrix(coins))
    elif cmd == "correlation":
        await update.message.reply_text(correlation_matrix(coins))
    elif cmd == "var":
        await update.message.reply_text(var_matrix(coins))
    elif cmd == "leader":
        await update.message.reply_text(leader_matrix(coins))
    elif len(coins) == 2:
        await update.message.reply_text(granger_test(coins[0], coins[1]))
    else:
        await update.message.reply_text("Geçersiz komut. Lütfen en az 2 coin belirtin.")
