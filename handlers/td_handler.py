# handlers/td_handler.py2
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.td_utils import get_trending_symbols

async def td_top_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = get_trending_symbols(limit=20)  # ilk 20
    if not result:
        await update.message.reply_text("Veri alınamadı.")
        return

    text = "📊 <b>Trend Coinler (Hacim + Fiyat Artışı)</b>\n\n"
    for i, coin in enumerate(result, 1):
        text += f"{i}. {coin['symbol']}: {coin['change']}% | Hacim: ${coin['volume']:,.0f}\n"

    await update.message.reply_text(text, parse_mode="HTML")

def register_td_handlers(app):
    app.add_handler(CommandHandler("td", td_top_handler))
    app.add_handler(CommandHandler("tdtop", td_top_handler))  # kısaltma
