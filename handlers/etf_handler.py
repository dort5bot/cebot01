# handlers/etf_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from utils.etf_utils import fetch_etf_data, format_etf_summary

async def etf_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = fetch_etf_data()
    text = format_etf_summary(data)
    await update.message.reply_html(text)
