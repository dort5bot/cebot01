##
#handlers/apikey_handler.py
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.data import save_api_key

async def apikey_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        if len(args) != 2:
            await update.message.reply_text("❗ Kullanım: /apikey <API_KEY> <SECRET_KEY>")
            return

        api_key, secret_key = args
        user_id = update.effective_user.id
        save_api_key(user_id, api_key, secret_key)
        await update.message.reply_text("✅ API anahtarları kaydedildi.")
    except Exception:
        await update.message.reply_text("❌ API anahtarları kaydedilemedi.")

def get_handler():
    return CommandHandler("apikey", apikey_command)
