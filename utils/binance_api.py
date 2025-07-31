# ==2>3====================================
# 📈 MegaBot Final - utils/binance_api.py
# Binance API işlemleri: fiyat alma, veri çekme
# ======================================

import requests

BASE_URL = "https://api.binance.com/api/v3"

def get_price(symbol="BTCUSDT"):
    try:
        url = f"{BASE_URL}/ticker/price"
        params = {"symbol": symbol}
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"[get_price HATASI] {e}")
        return None

def get_klines(symbol="BTCUSDT", interval="1h", limit=100):
    try:
        url = f"{BASE_URL}/klines"
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": limit
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[get_klines HATASI] {e}")
        return []

def get_current_price(symbol="BTCUSDT"):
    # check_orders için gereklidir
    return get_price(symbol)
