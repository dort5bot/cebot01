# handlers/trend_handler.py

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from utils.trend_utils import analyze_coin, get_top_trending_coins

async def td_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await update.message.reply_text("Lütfen coin sembolleri girin. Örnek: /td btc eth sol\nTüm piyasa için: /td top")
        return

    if args[0].lower() == "top":
        top_data = get_top_trending_coins(limit=30)
        if not top_data:
            await update.message.reply_text("Veri alınamadı.")
            return

        message = "📈 En Trend 30 Coin:\n\n"
        for i, coin in enumerate(top_data, 1):
            price = coin['price']
            score = coin['score']
            signal = coin['signal']
            message += f"{i}. {coin['symbol']} - {price} | TS: {score} | {signal}\n"
        await update.message.reply_text(message)
        return

    results = []
    for symbol in args:
        result = analyze_coin(symbol)
        if result:
            results.append(result)

    if not results:
        await update.message.reply_text("Geçerli veri bulunamadı.")
        return

    message = ""
    for coin in results:
        message += f"🔹 {coin['symbol']} - {coin['price']}\nTS: {coin['score']} | {coin['signal']}\n\n"
    await update.message.reply_text(message)

def register_td_handler(application):
    application.add_handler(CommandHandler("td", td_command))
