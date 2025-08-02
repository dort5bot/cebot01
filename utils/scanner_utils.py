# 📊 MegaBot - utils/scanner_utils.py
# Gelişmiş tarama (RSI, MACD, Hacim, Trend Skoru) + Zaman dilimi ve filtre desteği
# ===============================================================
import re
import numpy as np
from utils.binance_api import get_klines
from utils.indicators import calculate_rsi, calculate_macd
from utils.trend_score import calculate_trend_score

DEFAULT_INTERVAL = "1h"
DEFAULT_LIMIT = 50

def parse_scanner_command(args):
    filters = {
        "rsi": None,
        "macd": None,
        "volume": None,
        "ts": None,
        "interval": DEFAULT_INTERVAL,
        "limit": DEFAULT_LIMIT
    }

    for arg in args:
        arg = arg.lower()
        if re.match(r"rsi[<>]=?\d+", arg):
            filters["rsi"] = arg
        elif re.match(r"macd[<>]=?-?\d+\.?\d*", arg):
            filters["macd"] = arg
        elif re.match(r"vol(ume)?[<>]=?\d+", arg):
            filters["volume"] = arg
        elif re.match(r"ts[<>]=?\d+", arg):
            filters["ts"] = arg
        elif arg in ["1m", "5m", "15m", "30m", "1h", "4h", "1d", "1w"]:
            filters["interval"] = arg

    return filters

def evaluate_condition(value, condition_str):
    match = re.match(r"(<=|>=|<|>|=)?(-?\d+\.?\d*)", condition_str)
    if not match:
        return True
    operator, target = match.groups()
    target = float(target)

    if operator == "<":
        return value < target
    elif operator == "<=":
        return value <= target
    elif operator == ">":
        return value > target
    elif operator == ">=":
        return value >= target
    elif operator == "=" or operator is None:
        return value == target
    return True

def scan_coins(coins, filters):
    results = []

    interval = filters.get("interval", DEFAULT_INTERVAL)
    limit = filters.get("limit", DEFAULT_LIMIT)

    for coin in coins:
        try:
            df = get_klines(coin, interval=interval, limit=limit)
            if df is None or df.empty:
                continue

            close = df["close"].astype(float)
            volume = df["volume"].astype(float)
            rsi = calculate_rsi(close)[-1]
            macd_line, signal_line, _ = calculate_macd(close)
            macd = macd_line[-1] - signal_line[-1]
            vol_avg = np.mean(volume[-10:])
            ts = calculate_trend_score(df)

            if filters["rsi"] and not evaluate_condition(rsi, filters["rsi"][3:] if filters["rsi"].startswith("rsi") else filters["rsi"]):
                continue
            if filters["macd"] and not evaluate_condition(macd, filters["macd"][4:] if filters["macd"].startswith("macd") else filters["macd"]):
                continue
            if filters["volume"] and not evaluate_condition(vol_avg, filters["volume"].replace("volume", "").replace("vol", "")):
                continue
            if filters["ts"] and not evaluate_condition(ts, filters["ts"][2:] if filters["ts"].startswith("ts") else filters["ts"]):
                continue

            signal = "⚠️ BEKLE"
            if rsi < 35 and macd > 0 and ts > 60:
                signal = "🟢 AL"
            elif rsi > 70 and macd < 0:
                signal = "🔴 SAT"

            results.append({
                "coin": coin,
                "rsi": round(rsi, 1),
                "macd": round(macd, 3),
                "volume": round(vol_avg, 2),
                "ts": round(ts, 1),
                "signal": signal
            })

        except Exception as e:
            print(f"[HATA - scan_coins]: {coin} -> {e}")
            continue

    return sorted(results, key=lambda x: x["ts"], reverse=True)
