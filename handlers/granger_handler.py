# 📂 handlers/granger_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from utils.stats import (
    granger_test, granger_matrix,
    correlation_matrix, cointegration_matrix,
    var_matrix, leader_matrix
)

async def granger_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Kullanım: /g BTC ETH")
        return

    coin1, coin2 = context.args[0].upper(), context.args[1].upper()
    result = granger_test(coin1, coin2)
    await update.message.reply_text(result)

async def granger_matrix_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Kullanım: /GM BTC ETH BNB")
        return

    coins = [c.upper() for c in context.args]
    result = granger_matrix(coins)
    await update.message.reply_text(result)

async def matrix_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Kullanım: /m [c|g|ct|v|l] coin1 coin2 ...")
        return

    mode = context.args[0].lower()
    coins = [c.upper() for c in context.args[1:]]

    if mode == "g":
        result = granger_matrix(coins)
    elif mode == "c":
        result = correlation_matrix(coins)
    elif mode == "ct":
        result = cointegration_matrix(coins)
    elif mode == "v":
        result = var_matrix(coins)
    elif mode == "l":
        result = leader_matrix(coins)
    else:
        result = "Geçersiz analiz türü. Kullanım: /m [c|g|ct|v|l] coin1 coin2 ..."

    await update.message.reply_text(result)
