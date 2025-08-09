# utils/vwap.py
##⚠️ap icin
from typing import List, Tuple

def vwap_from_klines(klines: List[List]) -> float:
    """
    klines: list of Binance kline rows: [openTime, open, high, low, close, volume, ...]
    VWAP = sum(price * volume) / sum(volume), use typical price (high+low+close)/3 or close.
    """
    num = 0.0
    den = 0.0
    for k in klines:
        close = float(k[4])
        vol = float(k[5])
        num += close * vol
        den += vol
    if den == 0:
        return 0.0
    return num / den

def aggregate_vwap_many(symbol_klines: dict) -> float:
    """
    symbol_klines: {interval: klines}
    compute weighted VWAP across intervals using simple avg
    """
    vals = []
    for k in symbol_klines.values():
        v = vwap_from_klines(k)
        if v:
            vals.append(v)
    return sum(vals) / len(vals) if vals else 0.0
