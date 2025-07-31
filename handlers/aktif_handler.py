##
#aktif_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.orders import list_active_orders

async def aktif_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        result = list_active_orders(user_id)
        await update.message.reply_text(result)
    except Exception:
        await update.message.reply_text("❌ Açık işlemler listelenemedi.")

def get_handler():
    return CommandHandler("aktif", aktif_command)
