# ==2-3====================================
# ✅ MegaBot Final - utils/io_utils.py
# /io komutu - Alış/Satış baskı oranları hesaplama
# ======================================
from .binance_api import get_order_book

def get_io_analysis(symbol="BTCUSDT", limit=10):
    orderbook = get_order_book(symbol, limit=limit)
    if not orderbook:
        return "⚠️ Emir defteri verisi alınamadı."

    try:
        bids = orderbook.get("bids", [])
        asks = orderbook.get("asks", [])

        buy_volume = sum(float(bid[1]) for bid in bids)
        sell_volume = sum(float(ask[1]) for ask in asks)

        total_volume = buy_volume + sell_volume
        if total_volume == 0:
            return "⚠️ Emir defterinde işlem hacmi yok."

        buy_pressure = (buy_volume / total_volume) * 100
        sell_pressure = (sell_volume / total_volume) * 100

        comment = ""
        if buy_pressure > sell_pressure + 10:
            comment = "Alım baskısı güçlü görünüyor."
        elif sell_pressure > buy_pressure + 10:
            comment = "Satım baskısı güçlü görünüyor."
        else:
            comment = "Piyasa dengede."

        result = (
            f"📊 {symbol} Emir Defteri Analizi:\n"
            f"• Alım Hacmi: {buy_volume:.2f}\n"
            f"• Satım Hacmi: {sell_volume:.2f}\n"
            f"• Alım Baskısı: %{buy_pressure:.2f}\n"
            f"• Satım Baskısı: %{sell_pressure:.2f}\n"
            f"📝 Yorum: {comment}"
        )

        return result

    except Exception as e:
        return f"⚠️ Analiz hatası: {e}"
