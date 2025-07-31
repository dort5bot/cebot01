##
#stop_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.orders import close_order_by_stop

async def stop_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text("❗ Kullanım: /stop <coin> <miktar> <zarar%>")
            return

        symbol = args[0].upper() + "USDT"
        amount = float(args[1])
        stop_percent = float(args[2])
        user_id = update.effective_user.id

        result = close_order_by_stop(user_id, symbol, amount, stop_percent)
        await update.message.reply_text(result)
    except Exception:
        await update.message.reply_text("❌ Stop işlemi başarısız oldu.")

def get_handler():
    return CommandHandler("stop", stop_command)
