#🎯api yeni yapi, coklu api desteği var
# utils/binance_api.py
import os
import asyncio
import httpx
import logging
from typing import List, Optional, Dict, Any

BASE = "https://api.binance.com/api/v3"
CONCURRENCY = int(os.getenv("BINANCE_CONCURRENCY", "10"))
_semaphore = asyncio.Semaphore(CONCURRENCY)
_client: Optional[httpx.AsyncClient] = None

def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient(timeout=10.0)
    return _client

async def _get(path: str, params: dict = None) -> Any:
    url = f"{BASE}{path}"
    client = get_client()
    async with _semaphore:
        for attempt in range(2):
            try:
                r = await client.get(url, params=params)
                r.raise_for_status()
                return r.json()
            except Exception as e:
                if attempt == 1:
                    raise
                await asyncio.sleep(0.2)

async def get_all_symbols() -> List[str]:
    try:
        data = await _get("/exchangeInfo")
        syms = []
        for s in data.get("symbols", []):
            if s.get("status") == "TRADING":
                syms.append(s.get("baseAsset"))
        return sorted(list(set(syms)))
    except Exception as e:
        logging.warning("binance.get_all_symbols failed: %s", e)
        return []

async def get_klines(symbol: str, interval: str = "1h", limit: int = 500) -> Optional[List[List]]:
    try:
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        return await _get("/klines", params=params)
    except Exception as e:
        logging.warning("binance.get_klines(%s) failed: %s", symbol, e)
        return None

async def get_multiple_klines(symbols: List[str], interval: str = "1h", limit: int = 100) -> Dict[str, Optional[List[List]]]:
    tasks = [get_klines(s, interval=interval, limit=limit) for s in symbols]
    res = await asyncio.gather(*tasks, return_exceptions=True)
    out: Dict[str, Optional[List[List]]] = {}
    for s, r in zip(symbols, res):
        if isinstance(r, Exception):
            out[s] = None
        else:
            out[s] = r
    return out

async def get_price(symbol: str) -> Optional[float]:
    try:
        data = await _get("/ticker/price", params={"symbol": symbol})
        return float(data.get("price"))
    except Exception as e:
        logging.warning("binance.get_price %s failed: %s", symbol, e)
        return None

async def get_order_book(symbol: str, limit: int = 100) -> Optional[dict]:
    try:
        return await _get("/depth", params={"symbol": symbol, "limit": limit})
    except Exception as e:
        logging.warning("binance.get_order_book %s failed: %s", symbol, e)
        return None
