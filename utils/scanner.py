# utils/scanner.py

from utils.indicators import calculate_indicators
from utils.binance_api import get_klines

import re

COINS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "DOGEUSDT", "AVAXUSDT", "MATICUSDT"]

def parse_filter(filter_str):
    match = re.match(r'([a-zA-Z]+)([<>]=?|=)([0-9.]+)', filter_str)
    if not match:
        return None
    indicator, operator, value = match.groups()
    return indicator.upper(), operator, float(value)

def check_condition(indicator_value, operator, threshold):
    if operator == "<":
        return indicator_value < threshold
    elif operator == "<=":
        return indicator_value <= threshold
    elif operator == ">":
        return indicator_value > threshold
    elif operator == ">=":
        return indicator_value >= threshold
    elif operator == "=":
        return abs(indicator_value - threshold) < 0.01
    return False

def run_screener(filters_str, interval="1h", limit=50):
    filters = filters_str.split()
    parsed_filters = [parse_filter(f) for f in filters if parse_filter(f)]

    result = ""
    for coin in COINS:
        klines = get_klines(coin, interval=interval, limit=limit)
        if not klines:
            continue
        indicators = calculate_indicators(klines)

        if all(
            check_condition(indicators.get(ind, 0), op, val)
            for ind, op, val in parsed_filters
        ):
            result += f"✅ {coin}\n"

    return result.strip()
