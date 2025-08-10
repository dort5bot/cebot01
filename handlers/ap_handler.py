# handlers/ap_handler.py
from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
import logging
from utils.ap_utils import compute_ap_full

async def _ap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.effective_message.reply_text("AP hesaplanıyor... (binance + coinglass, cache ile)")
    try:
        report = await compute_ap_full()
    except Exception as e:
        logging.exception("compute_ap_full error")
        await msg.edit_text(f"AP hesaplanırken hata: {e}")
        return

    agg = report.get("ap_aggregate", 0.0)
    emoji = "🟢" if agg >= 60 else ("🟡" if agg >= 40 else "🔴")
    text = (
        f"📊 /ap — Altların Güç Endeksi\n\n"
        f"🔹 Kısa v. BTC gücü: {report.get('short_vs_btc')} \n"
        f"🔹 Kısa v. USD gücü: {report.get('short_usd')} \n"
        f"🔹 Uzun v. güç: {report.get('long_term')} \n\n"
        f"⭐ AP (aggregate): {agg} {emoji}\n\n"
        f"Meta: sembol sayısı: {report.get('meta', {}).get('symbols_used')}"
    )
    await msg.edit_text(text)

def get_handler():
    """
    Returns a CommandHandler instance. main.py expects to import get_handler and call it.
    """
    return CommandHandler("ap", _ap_command)
