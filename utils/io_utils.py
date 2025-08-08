##io api yardımcı fonksiyonlari


import requests
import os

def get_all_symbols():
    """Analizde kullanılacak semboller listesi"""
    return ["BTC", "ETH", "SOL", "BNB", "XRP", "DOGE", "AVAX", "MATIC", "ADA"]

def get_volume_share(symbol):
    """Coin'in piyasa hacim yüzdesini döndürür"""
    try:
        url = f"https://open-api.coinglass.com/api/futures/volume_share?symbol={symbol}USDT"
        headers = {"coinglassSecret": os.getenv("COINGLASS_API_KEY")}
        r = requests.get(url, headers=headers)
        data = r.json()
        return float(data.get("data", {}).get(symbol.upper(), 0))
    except:
        return 0.0

def get_recent_cash_flow(symbol):
    """Son saatlik net giriş/çıkış verisi"""
    try:
        url = f"https://open-api.coinglass.com/api/futures/cash_flow?symbol={symbol}USDT"
        headers = {"coinglassSecret": os.getenv("COINGLASS_API_KEY")}
        r = requests.get(url, headers=headers)
        return r.json()
    except:
        return None

def get_mts_score(symbol):
    """MTS skorunu döndürür (örnek placeholder)"""
    return 50.0

def get_io_ratio(symbol):
    """Long/Short Open Interest Ratio"""
    try:
        url = f"https://open-api.coinglass.com/api/futures/longShortRate?symbol={symbol}USDT&interval=0"
        headers = {"coinglassSecret": os.getenv("COINGLASS_API_KEY")}
        r = requests.get(url, headers=headers)
        data = r.json()
        return float(data["data"][0]["longShortRate"])
    except:
        return 0.0
