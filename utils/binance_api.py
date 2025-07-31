# ==2>3>4====================================
# 📈 MegaBot Final - utils/binance_api.py
# Binance API işlemleri: fiyat alma, veri çekme
# ======================================
import requests

BASE_URL = "https://api.binance.com/api/v3"

def get_price(symbol):
    try:
        response = requests.get(f"{BASE_URL}/ticker/price", params={"symbol": symbol})
        response.raise_for_status()
        return float(response.json()["price"])
    except Exception:
        return None

def get_order_book(symbol, limit=10):
    try:
        url = f"{BASE_URL}/depth"
        response = requests.get(url, params={"symbol": symbol, "limit": limit})
        response.raise_for_status()
        return response.json()
    except Exception:
        return None

def get_klines(symbol, interval="1h", limit=100):
    try:
        url = f"{BASE_URL}/klines"
        response = requests.get(url, params={"symbol": symbol, "interval": interval, "limit": limit})
        response.raise_for_status()
        return response.json()
    except Exception:
        return None

