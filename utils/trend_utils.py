# utils/trend_utils.py

import requests
from statistics import mean

def format_price(price):
    try:
        price = float(price)
        return f"{price:.2f}" if price >= 1 else f"{price:.8f}"
    except:
        return "-"

def analyze_coin(symbol):
    try:
        base_url = "https://api.binance.com/api/v3"
        klines = requests.get(f"{base_url}/klines", params={
            "symbol": symbol.upper() + "USDT",
            "interval": "15m",
            "limit": 30
        }).json()

        closes = [float(k[4]) for k in klines]
        volumes = [float(k[5]) for k in klines]

        if len(closes) < 10:
            return None

        price_now = closes[-1]
        price_prev = closes[0]
        vol_now = volumes[-1]
        vol_avg = mean(volumes)

        delta = (price_now - price_prev) / price_prev * 100
        vol_delta = (vol_now - vol_avg) / vol_avg * 100

        ts = delta + (vol_delta * 0.6)

        if ts > 5:
            signal = "🔼 AL"
        elif ts < -3:
            signal = "🔽 SAT"
        else:
            signal = "⏸️ DUR"

        return {
            "symbol": symbol.upper(),
            "price": format_price(price_now),
            "score": f"{ts:.2f}",
            "signal": signal
        }
    except Exception as e:
        return None

def get_top_trending_coins(limit=30):
    coin_list = [
        "BTC", "ETH", "BNB", "XRP", "SOL", "DOGE", "ADA", "AVAX", "DOT", "MATIC",
        "SHIB", "LINK", "LTC", "BCH", "OP", "ARB", "PEPE", "FLOKI", "GALA", "1000SATS",
        "JASMY", "TIA", "SEI", "WIF", "INJ", "RNDR", "BLUR", "FTM", "CAKE", "TRX"
    ]
    all_results = []
    for coin in coin_list:
        data = analyze_coin(coin)
        if data:
            all_results.append(data)
    all_results.sort(key=lambda x: float(x['score']), reverse=True)
    return all_results[:limit]
