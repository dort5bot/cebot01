# 📂 handlers/granger_handler.py 
from telegram import Update
from telegram.ext import ContextTypes
from utils.stats import (
    granger_test,
    granger_matrix,
    correlation_matrix,
    cointegration_matrix,
    var_matrix,
    leader_matrix
)

# Tekli Granger testi
async def granger_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 2:
        await update.message.reply_text("Kullanım: /g BTC ETH")
        return
    coin1, coin2 = context.args[0].upper(), context.args[1].upper()
    result = granger_test(coin1, coin2)
    await update.message.reply_text(result)

# Korelasyon matrisi
async def correlation_matrix_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coins = [c.upper() for c in context.args]
    result = correlation_matrix(coins)
    await update.message.reply_text(result)

# Granger matrisi
async def granger_matrix_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coins = [c.upper() for c in context.args]
    result = granger_matrix(coins)
    await update.message.reply_text(result)

# Cointegration matrisi
async def cointegration_matrix_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coins = [c.upper() for c in context.args]
    result = cointegration_matrix(coins)
    await update.message.reply_text(result)

# VAR matrisi
async def var_matrix_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coins = [c.upper() for c in context.args]
    result = var_matrix(coins)
    await update.message.reply_text(result)

# Liderlik matrisi
async def leader_matrix_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coins = [c.upper() for c in context.args]
    result = leader_matrix(coins)
    await update.message.reply_text(result)

# Genel matrix yönlendirici
async def matrix_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Kullanım: /m [c|g|ct|v|l] coin1 coin2 ...")
        return

    mode = context.args[0].lower()
    coins = [c.upper() for c in context.args[1:]]

    if mode == "c":
        result = correlation_matrix(coins)
    elif mode == "g":
        result = granger_matrix(coins)
    elif mode == "ct":
        result = cointegration_matrix(coins)
    elif mode == "v":
        result = var_matrix(coins)
    elif mode == "l":
        result = leader_matrix(coins)
    else:
        result = "Geçersiz mod. Kullanım: /m [c|g|ct|v|l] coin1 coin2 ..."

    await update.message.reply_text(result)
