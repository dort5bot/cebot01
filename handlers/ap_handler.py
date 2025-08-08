###handlers/ap_handler.py → Komut yönlendirme
#


from telegram import Update
from telegram.ext import CallbackContext
from utils.ap_calc import alt_vs_btc_strength, alt_usdt_strength, long_term_strength
from utils.binance_api import get_price_change, get_rsi, get_trend, get_momentum, get_volume_status

def ap_command(update: Update, context: CallbackContext):
    args = context.args

    if not args:
        # Piyasa genel rapor
        score1 = alt_vs_btc_strength()
        score2 = alt_usdt_strength()
        score3 = long_term_strength()

        msg = (
            "📊 *Piyasa Güç Endeksi*\n"
            f"Altların Kısa Vadede BTC’ye Karşı Gücü (0-100): *{score1}*\n"
            f"Altların Kısa Vadede Gücü (0-100): *{score2}*\n"
            f"Coinlerin Uzun Vadede Gücü (0-100): *{score3}*"
        )
        update.message.reply_text(msg, parse_mode="Markdown")

    else:
        symbol = args[0].upper()
        price = get_price_change(symbol, "current")
        trend = get_trend(symbol)
        momentum = get_momentum(symbol)
        rsi = get_rsi(symbol)
        volume = get_volume_status(symbol)

        msg = (
            f"📊 *{symbol} Analiz*\n"
            f"Fiyat: *{price}*\n"
            f"Trend: *{trend}*\n"
            f"Momentum: *{momentum}*\n"
            f"RSI: *{rsi}*\n"
            f"Hacim: *{volume}*\n"
        )
        update.message.reply_text(msg, parse_mode="Markdown")
