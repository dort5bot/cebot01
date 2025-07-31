##
#al_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.orders import add_order

async def al_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) < 3:
            await update.message.reply_text("❗ Kullanım: /al <coin> <miktar> <hedef%> [zarar%]")
            return

        symbol = args[0].upper() + "USDT"
        amount = float(args[1])
        target_percent = float(args[2])
        stop_percent = float(args[3]) if len(args) > 3 else 2.0
        user_id = update.effective_user.id

        result = add_order(user_id, symbol, amount, target_percent, stop_percent)
        await update.message.reply_text(result)
    except Exception as e:
        await update.message.reply_text("❌ Emir eklenemedi.")
        print(e)

def get_handler():
    return CommandHandler("al", al_command)
