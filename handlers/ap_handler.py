# ==2 ✅ MegaBot Final - handlers/ap_handler.py ==
# /ap komutu - Gelişmiş analiz çıktısı üretir
# ============================================

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.ap_utils import generate_ap_report

async def ap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        symbol = args[0].upper() + "USDT" if args else "BTCUSDT"
        interval = args[1] if len(args) > 1 else "1h"

        result = generate_ap_report(symbol, interval)

        if "error" in result:
            await update.message.reply_text(f"⚠️ Hata: {result['error']}")
            return

        msg = (
            f"📊 <b>{result['symbol']} ({result['interval']})</b>\n"
            f"💰 Fiyat: <code>{result['price']}</code>\n"
            f"📈 Trend: <b>{result['trend']}</b>\n"
            f"⚡ Momentum: <b>{result['momentum']}</b>\n"
            f"📊 RSI: <b>{result['rsi']}</b>\n"
            f"📦 Hacim Durumu: <b>{result['volume']}</b>\n"
            f"🧭 Tavsiye: <b>{result['recommendation']}</b>"
        )

        await update.message.reply_text(msg, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text("❌ Komut çalıştırılamadı.")
        print(f"[AP KOMUTU HATASI] {e}")

def get_handler():
    return CommandHandler("ap", ap_command)
