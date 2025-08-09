# utils/coinglass_api.py
#ap için 

import os
import requests
from typing import Optional, Dict

BASE = "https://open-api.coinglass.com/api"

HEADERS = {"coinglassSecret": os.getenv("COINGLASS_API_KEY", "")}

def safe_get(url, params=None):
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        # production: logging.warn(e)
        return None

def get_long_short_rate(symbol: str) -> Optional[float]:
    """Long/Short ratio (recent). symbol like 'BTC' or 'ETH'"""
    url = f"{BASE}/futures/longShortRate"
    params = {"symbol": f"{symbol}USDT", "interval": 0}
    data = safe_get(url, params)
    try:
        return float(data["data"][0]["longShortRate"])
    except Exception:
        return None

def get_cash_flow(symbol: str) -> Optional[Dict]:
    """Returns cash flow / net inflow data (hourly/day structures)"""
    url = f"{BASE}/futures/cash_flow"
    params = {"symbol": f"{symbol}USDT"}
    return safe_get(url, params)

def get_volume_share(symbol: str) -> Optional[float]:
    """Volume share helper (if available)"""
    url = f"{BASE}/futures/volume_share"
    params = {"symbol": f"{symbol}USDT"}
    data = safe_get(url, params)
    try:
        # response shapes vary; guard robustly
        return float(data.get("data", {}).get(symbol.upper(), 0))
    except Exception:
        return None
