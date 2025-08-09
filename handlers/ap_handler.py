##ap komutu
# handlers/ap_handler.py
from telegram import Update
from telegram.ext import ContextTypes
from utils.ap_utils import compute_ap_full

async def ap_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.effective_message.reply_text("AP hesaplanıyor... (binance + coinglass)")
    try:
        report = compute_ap_full()
    except Exception as e:
        await msg.edit_text(f"AP hesaplanırken hata: {e}")
        return

    agg = report["ap_aggregate"]
    emoji = "🟢" if agg >= 60 else ("🟡" if agg >= 40 else "🔴")
    text = (
        f"📊 /ap — Altların Güç Endeksi\n\n"
        f"🔹 Kısa v. BTC gücü: {report['short_vs_btc']} \n"
        f"🔹 Kısa v. USD gücü: {report['short_usd']} \n"
        f"🔹 Uzun v. güç: {report['long_term']} \n\n"
        f"⭐ AP (aggregate): {agg} {emoji}\n\n"
        f"Meta: sembol sayısı: {report['meta']['symbols_used']}"
    )
    await msg.edit_text(text)
