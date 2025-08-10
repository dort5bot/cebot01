# utils/ap_utils.py
import os
import time
import math
import asyncio
import logging
from typing import List, Dict

from .cache import TTLCache, get_or_fetch
from .vwap import vwap_from_klines
from .normalize import minmax_scale, clamp

from .binance_api import get_klines, get_multiple_klines, get_all_symbols, get_price
from .coinglass_api import get_long_short_rate, get_cash_flow, get_volume_share

# CONFIG
KLINES_TTL = int(os.getenv("KLINES_TTL", "30"))         # seconds
COINGLASS_TTL = int(os.getenv("COINGLASS_TTL", "300"))  # seconds
CONCURRENCY = int(os.getenv("AP_CONCURRENCY", "10"))

TIMEFRAMES = ["15m", "1h", "4h"]
LONG_TFS = ["4h", "12h", "1d"]

STABLECOINS = {"USDT", "USDC", "BUSD", "DAI", "TUSD", "USDP"}

_cache = TTLCache()
_sem = asyncio.Semaphore(CONCURRENCY)

async def get_symbols():
    key = "symbols:all"
    async def fetch():
        return await get_all_symbols()
    data, _ = await get_or_fetch(_cache, key, 300, fetch, fallback_key=key)
    return data or []

async def cached_long_short(symbol: str):
    key = f"coinglass:lsr:{symbol}"
    async def fetch():
        return await get_long_short_rate(symbol)
    val, _ = await get_or_fetch(_cache, key, COINGLASS_TTL, fetch, fallback_key=key)
    return val

async def cached_cash_flow(symbol: str):
    key = f"coinglass:cash:{symbol}"
    async def fetch():
        return await get_cash_flow(symbol)
    val, _ = await get_or_fetch(_cache, key, COINGLASS_TTL, fetch, fallback_key=key)
    return val

async def cached_klines(symbol: str, interval: str = "1h", limit: int = 100):
    key = f"binance:klines:{symbol}:{interval}:{limit}"
    async def fetch():
        return await get_klines(symbol, interval=interval, limit=limit)
    val, _ = await get_or_fetch(_cache, key, KLINES_TTL, fetch, fallback_key=key)
    return val

# --- Metrics ---
async def compute_io_score(symbol: str) -> float:
    lr = await cached_long_short(symbol)
    if lr is None:
        lr = 1.0
    try:
        val = math.log10(max(lr, 1e-9))
    except Exception:
        val = 0.0
    z = (val + 1) / 2.0
    return clamp(z * 100.0)

async def compute_vwap_diff_alt_vs_btc(symbols: List[str], interval="1h") -> float:
    tasks = [cached_klines(f"{s}USDT", interval=interval, limit=100) for s in symbols]
    tasks.append(cached_klines("BTCUSDT", interval=interval, limit=100))
    results = await asyncio.gather(*tasks, return_exceptions=True)
    alt_vwaps = []
    for res in results[:-1]:
        if isinstance(res, Exception) or not res:
            continue
        v = vwap_from_klines(res)
        if v:
            alt_vwaps.append(v)
    btc_res = results[-1]
    btc_vwap = vwap_from_klines(btc_res) if btc_res and not isinstance(btc_res, Exception) else 0.0
    if not alt_vwaps or btc_vwap == 0:
        return 0.0
    alt_vwap = sum(alt_vwaps) / len(alt_vwaps)
    return (alt_vwap - btc_vwap) / btc_vwap * 100.0

async def short_vs_btc_score(symbols: List[str]) -> float:
    momentums = []
    s_sample = symbols[:80]
    tasks = []
    for tf in TIMEFRAMES:
        for s in s_sample:
            tasks.append(cached_klines(f"{s}BTC", interval=tf, limit=50))
    # batch gather
    batch_size = 200
    for i in range(0, len(tasks), batch_size):
        batch = tasks[i:i+batch_size]
        res = await asyncio.gather(*batch, return_exceptions=True)
        for r in res:
            if isinstance(r, Exception) or not r:
                continue
            try:
                start = float(r[0][4])
                end = float(r[-1][4])
                mom = (end - start) / (start or 1) * 100.0
                momentums.append(mom)
            except Exception:
                continue
    io_tasks = [compute_io_score(s) for s in symbols[:20]]
    io_vals = await asyncio.gather(*io_tasks, return_exceptions=True)
    io_scores = [v for v in io_vals if not isinstance(v, Exception)]
    avg_io = sum(io_scores) / len(io_scores) if io_scores else 50.0
    avg_mom = sum(momentums) / len(momentums) if momentums else 0.0
    vw = await compute_vwap_diff_alt_vs_btc(symbols, interval="1h")
    io_part = clamp(avg_io)
    mom_scaled = minmax_scale(avg_mom, -10.0, 10.0)
    vw_scaled = minmax_scale(vw, -5.0, 5.0)
    score = 0.5 * io_part + 0.3 * mom_scaled + 0.2 * vw_scaled
    return clamp(score)

async def short_usd_score(symbols: List[str]) -> float:
    s_sample = symbols[:30]
    kl_tasks = [cached_klines(f"{s}USDT", interval="1h", limit=24) for s in s_sample]
    kl_res = await asyncio.gather(*kl_tasks, return_exceptions=True)
    vols = []
    for r in kl_res:
        if isinstance(r, Exception) or not r:
            continue
        try:
            vols.append(sum(float(k[5]) for k in r))
        except Exception:
            continue
    btc_kl = await cached_klines("BTCUSDT", interval="1h", limit=24)
    total = sum(float(k[5]) for k in btc_kl) if btc_kl else 0.0
    alt_sum = sum(vols)
    vol_share = (alt_sum / (alt_sum + total + 1e-9)) * 100.0
    moms = []
    for r in kl_res:
        if isinstance(r, Exception) or not r:
            continue
        try:
            start = float(r[0][4]); end = float(r[-1][4])
            moms.append((end - start) / (start or 1) * 100.0)
        except Exception:
            continue
    mom_avg = sum(moms) / len(moms) if moms else 0.0
    cf_tasks = [cached_cash_flow(s) for s in symbols[:20]]
    cf_res = await asyncio.gather(*cf_tasks, return_exceptions=True)
    flows = []
    for cf in cf_res:
        if isinstance(cf, Exception) or not cf:
            continue
        try:
            d = cf.get("data")
            if isinstance(d, dict):
                v = d.get("hour") or d.get("netInflow") or d.get("netFlow") or d.get("value")
                flows.append(float(v or 0))
            elif isinstance(d, list) and len(d) > 0:
                v = d[-1].get("netFlow") or d[-1].get("value") or d[-1].get("hour")
                flows.append(float(v or 0))
        except Exception:
            continue
    flow_avg = sum(flows) / len(flows) if flows else 0.0
    vol_sc = minmax_scale(vol_share, 0.0, 80.0)
    mom_sc = minmax_scale(mom_avg, -10.0, 10.0)
    flow_sc = minmax_scale(flow_avg, -1_000_000, 1_000_000) if flows else 50.0
    score = 0.5 * vol_sc + 0.3 * mom_sc + 0.2 * flow_sc
    return clamp(score)

async def long_term_score(symbols: List[str]) -> float:
    io_tasks = [compute_io_score(s) for s in symbols[:30]]
    io_vals = await asyncio.gather(*io_tasks, return_exceptions=True)
    io_scores = [v for v in io_vals if not isinstance(v, Exception)]
    avg_io = sum(io_scores) / len(io_scores) if io_scores else 50.0
    vg_list = []
    kl_tasks = [cached_klines(f"{s}USDT", interval="1d", limit=40) for s in symbols[:30]]
    kl_res = await asyncio.gather(*kl_tasks, return_exceptions=True)
    for r in kl_res:
        if isinstance(r, Exception) or not r or len(r) < 14:
            continue
        try:
            vols = [float(k[5]) for k in r]
            avg7 = sum(vols[-7:]) / 7.0
            avg30 = sum(vols[-30:]) / 30.0 if len(vols) >= 30 else sum(vols) / len(vols)
            vg_list.append(avg7 / (avg30 or 1))
        except Exception:
            continue
    vg = sum(vg_list) / len(vg_list) if vg_list else 1.0
    vg_sc = minmax_scale((vg - 1.0) * 100.0, -50.0, 50.0)
    score = 0.6 * clamp(avg_io) + 0.4 * vg_sc
    return clamp(score)

async def compute_ap_full() -> Dict:
    async with _sem:
        syms = await get_symbols()
        syms = [s for s in syms if s.upper() not in ("BTC",) and s.upper() not in STABLECOINS]
        if not syms:
            syms = ["ETH", "SOL", "BNB", "XRP", "DOGE", "MATIC", "ADA"]
        syms = syms[:80]
        s1 = await short_vs_btc_score(syms)
        s2 = await short_usd_score(syms)
        s3 = await long_term_score(syms)
        AP = 0.4 * s1 + 0.35 * s2 + 0.25 * s3
        return {
            "short_vs_btc": round(s1, 2),
            "short_usd": round(s2, 2),
            "long_term": round(s3, 2),
            "ap_aggregate": round(AP, 2),
            "meta": {"symbols_used": len(syms), "computed_at": time.time()}
    }
