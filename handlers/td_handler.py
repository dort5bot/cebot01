# handlers/td_handler.py
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.td_utils import get_trending_symbols

async def td_top_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trending = get_trending_symbols(limit=20)
    
    if not trending:
        await update.message.reply_text("❌ Binance verisi alınamadı.")
        return

    text = "📈 <b>Trend Coinler (24s Değişim + Hacim)</b>\n\n"
    for i, coin in enumerate(trending, 1):
        text += (
            f"{i}. <b>{coin['symbol']}</b>: "
            f"{coin['change']}% | "
            f"Hacim: <code>${coin['volume']:,.0f}</code>\n"
        )

    await update.message.reply_text(text, parse_mode="HTML")

def register_td_handlers(app):
    app.add_handler(CommandHandler("td", td_top_handler))
    app.add_handler(CommandHandler("tdtop", td_top_handler))  # kısa komut
