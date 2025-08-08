# utils/indicators.py
#kimle ilgilidir not almamışım 

import numpy as np

def calculate_rsi(prices, period=14):
    deltas = np.diff(prices)
    ups = deltas[deltas > 0].sum() / period
    downs = -deltas[deltas < 0].sum() / period if any(deltas < 0) else 0.01
    rs = ups / downs
    return 100 - (100 / (1 + rs))

def calculate_macd(prices, short=12, long=26, signal=9):
    ema_short = np.mean(prices[-short:])
    ema_long = np.mean(prices[-long:])
    macd = ema_short - ema_long
    return macd

def calculate_volume(volumes):
    return sum(volumes[-5:])

def calculate_TS(prices):
    if len(prices) < 2:
        return 0
    delta = prices[-1] - prices[-2]
    percent = (delta / prices[-2]) * 100
    return percent

def calculate_indicators(klines):
    close_prices = [float(k[4]) for k in klines]
    volumes = [float(k[5]) for k in klines]

    return {
        "RSI": round(calculate_rsi(close_prices), 2),
        "MACD": round(calculate_macd(close_prices), 4),
        "VOL": round(calculate_volume(volumes), 2),
        "TS": round(calculate_TS(close_prices), 2),
    }
