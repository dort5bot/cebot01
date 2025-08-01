# handlers/etf_handler.py

from telegram.ext import CommandHandler, ContextTypes
from telegram import Update
from utils.etf_utils import get_etf_data, get_us_markets, load_csv_last, load_csv_avg, trend_arrow, trend_percent
from datetime import datetime

async def etf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = [a.lower() for a in context.args]
    msg = ""

    if "abd" in args and len(args) == 1:
        us = get_us_markets()
        msg += "📈 ABD Piyasaları\n"
        for n, c in us.items():
            if c is not None:
                emoji = "🟢" if c >= 0 else "🔴"
                msg += f"{emoji} {n} {c:+.2f}%\n"
        await update.message.reply_text(msg)
        return

    if args and args[0].isdigit():
        n = int(args[0])
        etf_data = get_etf_data(["btc", "eth"])
        avg = load_csv_avg(n)
        msg += f"📊 Son {n} Günlük Ortalama Karşılaştırma\n\n"

        if avg:
            msg += f"BTC: {etf_data['BTC']['total']}M$ (Ort.: {avg[0]:.2f}M$) {trend_arrow(etf_data['BTC']['total'], avg[0])}\n"
            msg += f"(ort: {avg[2]:+.0f} M$ BlackRock {trend_percent(etf_data['BTC']['funds'].get('BlackRock',0), avg[2])} , "
            msg += f"ort: {avg[3]:+.0f} M$ Grayscale {trend_percent(etf_data['BTC']['funds'].get('Grayscale',0), avg[3])})\n\n"

            msg += f"ETH: {etf_data['ETH']['total']}M$ (Ort.: {avg[1]:.2f}M$) {trend_arrow(etf_data['ETH']['total'], avg[1])}\n"
            msg += f"(ort: {avg[4]:+.0f} M$ BlackRock {trend_percent(etf_data['ETH']['funds'].get('BlackRock',0), avg[4])} , "
            msg += f"ort: {avg[5]:+.0f} M$ Grayscale {trend_percent(etf_data['ETH']['funds'].get('Grayscale',0), avg[5])})\n"
        else:
            msg += "📌 Yeterli kayıt yok.\n"

        await update.message.reply_text(msg)
        return

    today_str = datetime.now().strftime("%d %B %Y")
    coins = ["btc", "eth"] if not args else [a for a in args if a in ["btc", "eth"]]
    etf_data = get_etf_data(coins)
    last = load_csv_last()

    msg += f"📊 ETF Akışı ({today_str})\n\n"
    for c in coins:
        name = c.upper()
        total = etf_data[name]["total"]
        msg += f"{name}: {total}M$"
        if last:
            if name == "BTC":
                msg += f" (Son Kayıt: {last[1]}M$) {trend_arrow(total, float(last[1]))}\n"
            if name == "ETH":
                msg += f" (Son Kayıt: {last[2]}M$) {trend_arrow(total, float(last[2]))}\n"
        else:
            msg += "\n"

        funds = etf_data[name]["funds"]
        details = []
        for f, val in funds.items():
            sign = "+" if val >= 0 else "–"
            details.append(f"{sign}{abs(val):.0f} M$ {f}")
        msg += f"({', '.join(details)})\n\n"

    if not args or "abd" in args:
        us = get_us_markets()
        msg += "📈 ABD Piyasaları\n"
        for n, c in us.items():
            if c is not None:
                emoji = "🟢" if c >= 0 else "🔴"
                msg += f"{emoji} {n} {c:+.2f}%\n"

    await update.message.reply_text(msg)

def add_etf_handler(application, job_queue):
    application.add_handler(CommandHandler("etf", etf))
