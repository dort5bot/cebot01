##
#sat_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.orders import close_order_by_target

async def sat_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text("❗ Kullanım: /sat <coin> <miktar> <hedef%>")
            return

        symbol = args[0].upper() + "USDT"
        amount = float(args[1])
        target_percent = float(args[2])
        user_id = update.effective_user.id

        result = close_order_by_target(user_id, symbol, amount, target_percent)
        await update.message.reply_text(result)
    except Exception:
        await update.message.reply_text("❌ Satış işlemi başarısız oldu.")

def get_handler():
    return CommandHandler("sat", sat_command)
