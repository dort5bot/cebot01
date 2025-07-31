
# ======================================
# ✅ MegaBot Final - utils/ap_utils.py
# /ap komutu - Altcoin Güç Endeksi hesaplama
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
