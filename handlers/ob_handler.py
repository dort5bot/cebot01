##ob_handler.py
# /ob komutu - Emir defteri analizi
##
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.ob_utils import analyze_order_book

async def ob_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        args = context.args
        symbol = args[0].upper() + "USDT" if args else "BTCUSDT"

        result = analyze_order_book(symbol)

        if "error" in result:
            await update.message.reply_text(f"⚠️ Hata: {result['error']}")
            return

        msg = (
            f"📘 <b>{symbol} Emir Defteri Özeti</b>\n\n"
            f"🔄 <b>Spread:</b> <code>{result['spread']:.2f} USDT</code>\n"
            f"📉 <b>Alım Baskısı:</b> <code>{result['buy_pressure']}%</code>\n"
            f"📈 <b>Satım Baskısı:</b> <code>{result['sell_pressure']}%</code>\n"
            f"📦 <b>Likidite Derinliği:</b>\n"
            f"• Alım: <code>{result['buy_volume']} {symbol[:-4]}</code>\n"
            f"• Satım: <code>{result['sell_volume']} {symbol[:-4]}</code>\n\n"
            f"🧭 <b>Yorum:</b> {result['comment']}"
        )

        await update.message.reply_text(msg, parse_mode="HTML")

    except Exception as e:
        await update.message.reply_text("❌ /ob komutu çalıştırılamadı.")
        print(f"[OB HATA] {e}")

def get_handler():
    return CommandHandler("ob", ob_command)
