# utils/vwap.py
##⚠️ap icin

# utils/vwap.py
from typing import List

def vwap_from_klines(klines: List[List]) -> float:
    num = 0.0
    den = 0.0
    for k in klines:
        try:
            close = float(k[4])
            vol = float(k[5])
        except Exception:
            continue
        num += close * vol
        den += vol
    if den == 0:
        return 0.0
    return num / den

def aggregate_vwap_many(symbol_klines: dict) -> float:
    vals = []
    for k in symbol_klines.values():
        v = vwap_from_klines(k) if k else 0.0
        if v:
            vals.append(v)
    return sum(vals) / len(vals) if vals else 0.0
