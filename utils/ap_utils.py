# ==3========
# == ✅ MegaBot Final - utils/ap_utils.py ==
# /ap komutu - Gelişmiş Altcoin Güç Endeksi Analizi
# ===============================================

from .binance_api import get_price, get_klines
import numpy as np

def calculate_rsi(prices, period=14):
    if len(prices) < period + 1:
        return None
    deltas = np.diff(prices)
    seed = deltas[:period]
    up = seed[seed > 0].sum() / period
    down = -seed[seed < 0].sum() / period
    rs = up / down if down != 0 else 0
    rsi = 100 - (100 / (1 + rs))
    return round(rsi, 2)

def calculate_trend(prices):
    if len(prices) < 2:
        return "yetersiz veri"
    return "yukarı" if prices[-1] > prices[0] else "aşağı"

def calculate_momentum(prices):
    if len(prices) < 4:
        return "yetersiz veri"
    diff = prices[-1] - prices[-4]
    return "güçlü" if diff > 0 else "zayıf"

def detect_volume_spike(volumes):
    if len(volumes) < 4:
        return "yetersiz veri"
    avg_vol = np.mean(volumes[:-1])
    return "yüksek" if volumes[-1] > 1.5 * avg_vol else "normal"

def generate_ap_report(symbol="BTCUSDT", interval="1h"):
    try:
        klines = get_klines(symbol, interval=interval, limit=100)
        closes = [float(k[4]) for k in klines]
        volumes = [float(k[5]) for k in klines]

        if not closes or not volumes:
            raise ValueError("Veri eksik")

        price = closes[-1]
        rsi = calculate_rsi(closes)
        trend = calculate_trend(closes)
        momentum = calculate_momentum(closes)
        volume_status = detect_volume_spike(volumes)

        recommendation = "AL"
        if rsi and rsi > 70:
            recommendation = "SAT"
        elif rsi and rsi < 30:
            recommendation = "AL"
        elif trend == "aşağı":
            recommendation = "BEKLE"

        return {
            "symbol": symbol,
            "interval": interval,
            "price": round(price, 4),
            "trend": trend,
            "momentum": momentum,
            "rsi": rsi,
            "volume": volume_status,
            "recommendation": recommendation
        }

    except Exception as e:
        return {
            "symbol": symbol,
            "interval": interval,
            "error": f"Veri çekilemedi: {str(e)}"
        }
