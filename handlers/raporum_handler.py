##
#handlers/raporum_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.orders import generate_report

async def raporum_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.effective_user.id
        result, file_path = generate_report(user_id)
        await update.message.reply_text(result)
        if file_path:
            await update.message.reply_document(document=open(file_path, 'rb'))
    except Exception:
        await update.message.reply_text("❌ Rapor oluşturulamadı.")

def get_handler():
    return CommandHandler("raporum", raporum_command)
