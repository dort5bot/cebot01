# utils/coinglass_api.py
#ap için 

# utils/coinglass_api.py
import os
import asyncio
import httpx
import logging
from typing import Optional, Dict, Any

BASE = "https://open-api.coinglass.com/api"
API_KEY = os.getenv("COINGLASS_API_KEY", "")
HEADERS = {"coinglassSecret": API_KEY} if API_KEY else {}

CONCURRENCY = int(os.getenv("COINGLASS_CONCURRENCY", "6"))
_semaphore = asyncio.Semaphore(CONCURRENCY)
_client: Optional[httpx.AsyncClient] = None

def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(timeout=12.0, headers=HEADERS)
    return _client

async def _get(path: str, params: dict = None) -> Optional[Dict[str, Any]]:
    url = f"{BASE}{path}"
    client = get_client()
    async with _semaphore:
        try:
            r = await client.get(url, params=params)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            logging.warning("coinglass._get %s failed: %s", path, e)
            return None

async def get_long_short_rate(symbol: str) -> Optional[float]:
    try:
        data = await _get("/futures/longShortRate", params={"symbol": f"{symbol}USDT", "interval": 0})
        if not data:
            return None
        d = data.get("data")
        if isinstance(d, list) and len(d) > 0:
            v = d[0].get("longShortRate") or d[0].get("ratio")
            return float(v) if v is not None else None
        if isinstance(d, dict):
            v = d.get(symbol.upper()) or d.get("longShortRate")
            return float(v) if v is not None else None
    except Exception as e:
        logging.warning("coinglass.get_long_short_rate %s failed: %s", symbol, e)
    return None

async def get_cash_flow(symbol: str) -> Optional[Dict]:
    try:
        return await _get("/futures/cash_flow", params={"symbol": f"{symbol}USDT"})
    except Exception as e:
        logging.warning("coinglass.get_cash_flow %s failed: %s", symbol, e)
        return None

async def get_volume_share(symbol: str) -> Optional[float]:
    try:
        data = await _get("/futures/volume_share", params={"symbol": f"{symbol}USDT"})
        if not data:
            return None
        d = data.get("data", {})
        val = d.get(symbol.upper()) or d.get("volumeShare")
        return float(val) if val is not None else None
    except Exception as e:
        logging.warning("coinglass.get_volume_share %s failed: %s", symbol, e)
    return None
