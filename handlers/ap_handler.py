# == ✅ MegaBot Final - handlers/ap_handler.py ==
# /ap komutu - Gelişmiş Altcoin Güç Endeksi

from utils.ap_calc import alt_vs_btc_strength, alt_usdt_strength, long_term_strength
from utils.ap_utils import generate_ap_report

def ap_command(update, context):
    chat_id = update.effective_chat.id
    try:
        btc_report = generate_ap_report("BTCUSDT")
        eth_report = generate_ap_report("ETHUSDT")

        msg = "📊 **Altcoin Güç Endeksi**\n"
        msg += f"\n🔹 **Alt vs BTC Gücü:** {alt_vs_btc_strength()} / 100"
        msg += f"\n🔹 **Alt vs USDT Gücü:** {alt_usdt_strength()} / 100"
        msg += f"\n🔹 **Uzun Vadeli Güç:** {long_term_strength()} / 100"

        msg += "\n\n📈 **BTC Teknik Analizi**"
        msg += f"\nFiyat: {btc_report['price']} | RSI: {btc_report['rsi']} | Trend: {btc_report['trend']} | Momentum: {btc_report['momentum']} | Hacim: {btc_report['volume']} | Tavsiye: {btc_report['recommendation']}"

        msg += "\n\n📈 **ETH Teknik Analizi**"
        msg += f"\nFiyat: {eth_report['price']} | RSI: {eth_report['rsi']} | Trend: {eth_report['trend']} | Momentum: {eth_report['momentum']} | Hacim: {eth_report['volume']} | Tavsiye: {eth_report['recommendation']}"

        context.bot.send_message(chat_id=chat_id, text=msg, parse_mode="Markdown")
    except Exception as e:
        context.bot.send_message(chat_id=chat_id, text=f"❌ Hata: {str(e)}")
