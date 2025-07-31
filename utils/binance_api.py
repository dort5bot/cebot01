# ==2====================================
# 📈 MegaBot Final - utils/binance_api.py
# Binance API işlemleri: fiyat alma, veri çekme
# ======================================
import requests

BASE_URL = "https://api.binance.com/api/v3"

# Genel fiyat alma fonksiyonu (USDT bazlı)
def get_current_price(symbol: str) -> float:
    symbol = symbol.upper().replace("/", "")
    if not symbol.endswith("USDT"):
        symbol += "USDT"
    try:
        response = requests.get(f"{BASE_URL}/ticker/price", params={"symbol": symbol}, timeout=5)
        response.raise_for_status()
        return float(response.json()["price"])
    except Exception as e:
        print(f"[BinanceAPI] Fiyat alınamadı: {symbol} - {e}")
        return None

def get_orderbook(symbol: str, limit: int = 100):
    symbol = symbol.upper().replace("/", "")
    if not symbol.endswith("USDT"):
        symbol += "USDT"
    try:
        response = requests.get(f"{BASE_URL}/depth", params={"symbol": symbol, "limit": limit}, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[BinanceAPI] Orderbook alınamadı: {symbol} - {e}")
        return None

def get_klines(symbol: str, interval: str = "1h", limit: int = 100):
    symbol = symbol.upper().replace("/", "")
    if not symbol.endswith("USDT"):
        symbol += "USDT"
    try:
        response = requests.get(f"{BASE_URL}/klines", params={"symbol": symbol, "interval": interval, "limit": limit}, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"[BinanceAPI] Klines alınamadı: {symbol} - {e}")
        return None
