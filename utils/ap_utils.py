# ==2====================================
# ✅ MegaBot Final - utils/ap_utils.py
# /ap komutu - Altcoin Güç Endeksi hesaplama ve analiz üretimi
# ======================================
from .binance_api import get_price

def calculate_ap(symbols):
    results = {}
    for sym in symbols:
        try:
            price = get_price(sym)
            results[sym] = price
        except:
            results[sym] = None
    return results

def generate_ap_report(symbol, interval="1h"):
    # Bu örnek analiz fonksiyonu basit bir yapıdadır.
    # Daha gelişmiş hesaplamalar eklenebilir.

    price = get_price(symbol)
    if price is None:
        return {
            "symbol": symbol,
            "interval": interval,
            "error": "Veri alınamadı"
        }

    analysis = {
        "symbol": symbol,
        "interval": interval,
        "trend": "yukarı",  # örnek değer
        "momentum": "güçlü",  # örnek değer
        "volume": "yüksek",   # örnek değer
        "recommendation": "AL",  # örnek değer
        "price": price
    }
    return analysis
