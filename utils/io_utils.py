# ==2====================================
# ✅ MegaBot Final - utils/io_utils.py
# /io komutu - Alış/Satış baskı oranları hesaplama
# ======================================

from .binance_api import get_orderbook

def calculate_io(symbol):
    book = get_orderbook(symbol)
    bids = sum(float(bid[1]) for bid in book["bids"])
    asks = sum(float(ask[1]) for ask in book["asks"])
    total = bids + asks
    if total == 0:
        return {"buy_ratio": 0, "sell_ratio": 0}
    return {
        "buy_ratio": round(100 * bids / total, 2),
        "sell_ratio": round(100 * asks / total, 2)
    }

def get_io_analysis(symbol):
    ratios = calculate_io(symbol)
    buy_ratio = ratios["buy_ratio"]
    sell_ratio = ratios["sell_ratio"]

    trend = "NÖTR"
    if buy_ratio > 60:
        trend = "AL"
    elif sell_ratio > 60:
        trend = "SAT"

    return {
        "symbol": symbol,
        "buy_ratio": buy_ratio,
        "sell_ratio": sell_ratio,
        "trend": trend
    }
