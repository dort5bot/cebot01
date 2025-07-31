
# ======================================
# ✅ MegaBot Final - utils/fr_utils.py
# /fr komutu - Fon Raporu
# ======================================
from .binance_api import get_klines

def calculate_fr(symbol):
    klines = get_klines(symbol, interval="1d", limit=7)
    closes = [float(k[4]) for k in klines]
    change = round((closes[-1] - closes[0]) / closes[0] * 100, 2)
    return {"closes": closes, "7d_change": change}
