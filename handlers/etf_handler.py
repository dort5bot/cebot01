# handlers/etf_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from history.etf_history import generate_etf_history_csv
from utils.etf_utils import get_etf_snapshot

async def etf_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    snapshot = get_etf_snapshot()

    msg = "📊 <b>ETF Piyasa Özeti</b>\n\n"
    for key, value in snapshot.items():
        msg += f"• <b>{key}</b>: {value}\n"

    await update.message.reply_text(msg, parse_mode="HTML")

    file_path = generate_etf_history_csv()
    if file_path:
        await update.message.reply_document(document=open(file_path, "rb"))
