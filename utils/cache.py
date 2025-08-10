##ap için 
# utils/cache.py
import time
import asyncio
from typing import Any, Callable, Optional, Tuple

class TTLCache:
    def __init__(self):
        self._store: dict[str, Tuple[float, Any]] = {}
        self._lock = asyncio.Lock()

    async def set(self, key: str, value: Any, ttl: int):
        expire = time.time() + ttl
        async with self._lock:
            self._store[key] = (expire, value)

    async def get(self, key: str) -> Optional[Any]:
        async with self._lock:
            e = self._store.get(key)
            if not e:
                return None
            expire, val = e
            if time.time() > expire:
                self._store.pop(key, None)
                return None
            return val

async def get_or_fetch(cache: TTLCache, key: str, ttl: int, fetcher: Callable[[], Any], fallback_key: Optional[str] = None):
    """
    Try cache -> if miss call fetcher() (async). On success store and return.
    On fetcher exception or None, try fallback_key (last cached) and return that if present.
    Returns: (value_or_None, from_cache:bool)
    """
    val = await cache.get(key)
    if val is not None:
        return val, True

    try:
        result = await fetcher()
        if result is not None:
            await cache.set(key, result, ttl)
            return result, False
    except Exception:
        # fetch failed; will attempt fallback if any
        pass

    if fallback_key:
        last = await cache.get(fallback_key)
        if last is not None:
            return last, True
    return None, False
