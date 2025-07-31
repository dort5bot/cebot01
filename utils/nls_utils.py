
# ======================================
# ✅ MegaBot Final - utils/nls_utils.py
# /nls komutu - Net Likidite Skoru hesaplama
# ======================================
from .binance_api import get_orderbook

def calculate_nls(symbol):
    ob = get_orderbook(symbol)
    buy = sum(float(bid[0]) * float(bid[1]) for bid in ob["bids"])
    sell = sum(float(ask[0]) * float(ask[1]) for ask in ob["asks"])
    net = buy - sell
    score = round(net / (buy + sell + 1e-9) * 100, 2)
    return {"nls_score": score, "buy_value": buy, "sell_value": sell}
