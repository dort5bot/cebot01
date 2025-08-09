## ap ana motor
# utils/ap_utils.py
import time
from typing import List, Dict
from datetime import datetime, timedelta

from .binance_api import get_multiple_klines, get_klines, get_price, get_order_book, get_all_symbols as base_symbols
from .coinglass_api import get_long_short_rate, get_cash_flow
from .vwap import vwap_from_klines, aggregate_vwap_many
from .normalize import minmax_scale, clamp

# CONFIG
TIMEFRAMES = ["15m", "1h", "4h"]      # kısa vadeli ağırlıklı
LONG_TFS = ["4h", "12h", "1d"]       # uzun vadeli bileşen
WEIGHTS = {"15m": 0.5, "1h": 0.3, "4h": 0.2}  # örnek kısa-vade ağırlıkları

STABLECOINS = {"USDT", "USDC", "BUSD", "DAI", "TUSD", "USDP"}

def get_symbols():
    # temel semboller listesinden BTC ve stablecoinleri çıkar
    syms = base_symbols()
    return [s for s in syms if s.upper() not in ("BTC",) and s.upper() not in STABLECOINS]

# --- Helper metric calculators ---
def compute_volume_growth(symbol: str, interval: str = "1h") -> float:
    """
    Hacim büyümesi: son interval hacmi / ortalama önceki N interval hacmi
    Dönüş: ratio (ör. 1.5 => +50%)
    """
    klines = get_klines(f"{symbol}USDT", interval=interval, limit=50)
    if not klines or len(klines) < 10:
        return 1.0
    vols = [float(k[5]) for k in klines]
    recent = vols[-1]
    avg_prev = sum(vols[:-1]) / (len(vols)-1) if len(vols) > 1 else recent
    if avg_prev == 0:
        return 1.0
    return recent / avg_prev

def compute_io_score(symbol: str) -> float:
    """
    IO proxy: Coinglass longShortRate kullan, >1 -> long baskısı, <1 short baskısı
    map -> 0..100
    """
    lr = get_long_short_rate(symbol) or 1.0
    # normalize longShortRate: typical range 0.1 - 10; map to 0-100 with log scale
    import math
    val = math.log10(lr + 1e-9)  # center near 0 (lr=1)
    # map [-1..+1] -> [0..100]
    z = (val + 1) / 2.0
    return clamp(z * 100.0)

def compute_vwap_diff_alt_vs_btc(symbols: List[str], interval="1h") -> float:
    """
    Compute VWAP difference between aggregated alts and BTC.
    Positive -> alts trading higher relative to BTC.
    """
    # aggregate alt VWAP by averaging VWAPs
    alt_vwaps = []
    for s in symbols:
        kl = get_klines(f"{s}USDT", interval=interval, limit=100)
        if kl:
            alt_vwaps.append(vwap_from_klines(kl))
    btc_kl = get_klines("BTCUSDT", interval=interval, limit=100)
    btc_vwap = vwap_from_klines(btc_kl) if btc_kl else 0.0
    if not alt_vwaps or btc_vwap == 0:
        return 0.0
    alt_vwap = sum(alt_vwaps) / len(alt_vwaps)
    # relative diff percent
    return (alt_vwap - btc_vwap) / btc_vwap * 100.0

# --- Score building blocks ---
def short_vs_btc_score(symbols: List[str]) -> float:
    """
    1) Kısa vadede BTC'ye karşı güç:
      - volume growth aggregated
      - price momentum aggregated (15m-4h)
      - IO score aggregated
      - VWAP diff
    Returns 0..100
    """
    # aggregate volume growth across symbols (median)
    vols = []
    io_scores = []
    momentums = []
    for tf in TIMEFRAMES:
        for s in symbols:
            try:
                klines = get_klines(f"{s}BTC", interval=tf, limit=50)
                if not klines:
                    continue
                # momentum = percent change last candle close vs 1st
                start = float(klines[0][4])
                end = float(klines[-1][4])
                mom = (end - start) / (start or 1) * 100.0
                momentums.append(mom)
            except Exception:
                continue
    # use IO from coinglass across top coins (use average)
    for s in symbols[:20]:
        io = compute_io_score(s) or 50.0
        io_scores.append(io)
    # aggregate metrics
    avg_io = sum(io_scores) / len(io_scores) if io_scores else 50.0
    avg_mom = sum(momentums) / len(momentums) if momentums else 0.0

    # VWAP diff (percent)
    vw = compute_vwap_diff_alt_vs_btc(symbols, interval="1h")
    # map metrics to 0..100
    io_part = clamp(avg_io)
    # momentum mapping: -10% -> 0, 0% ->50, +10% ->100 (clip)
    mom_scaled = minmax_scale(avg_mom, -10.0, 10.0)
    vw_scaled = minmax_scale(vw, -5.0, 5.0)  # +/-5% range
    # combine with weights
    score = 0.5 * io_part + 0.3 * mom_scaled + 0.2 * vw_scaled
    return clamp(score)

def short_usd_score(symbols: List[str]) -> float:
    """
    2) Altların kısa vadede USD bazlı gücü:
      - toplam altcoin USD hacim payı (proxy: sum vol of top alts / total vol)
      - fiyat momentum (USDT pairs)
      - kısa vade nakit göçü (Coinglass cash flow)
    """
    # volume share: approximate using klines volume sum for top N
    vols = []
    total = 0.0
    for s in symbols[:30]:
        kl = get_klines(f"{s}USDT", interval="1h", limit=24)
        if kl:
            vols.append(sum(float(k[5]) for k in kl))
    btc_kl = get_klines("BTCUSDT", interval="1h", limit=24)
    if btc_kl:
        total = sum(float(k[5]) for k in btc_kl)
    alt_sum = sum(vols)
    vol_share = (alt_sum / (alt_sum + total + 1e-9)) * 100.0

    # momentum USDT:
    moms = []
    for s in symbols[:30]:
        kl = get_klines(f"{s}USDT", interval="1h", limit=24)
        if kl:
            start = float(kl[0][4])
            end = float(kl[-1][4])
            moms.append((end - start) / (start or 1) * 100.0)
    mom_avg = sum(moms) / len(moms) if moms else 0.0

    # cash flow proxy: average net inflow (if API provides)
    flows = []
    for s in symbols[:20]:
        cf = get_cash_flow(s)
        if cf and "data" in cf:
            # shape varies; try robust extraction
            try:
                # some returns: data -> list of flows; sum recent
                flows.append(float(cf["data"].get("hour", 0)))
            except Exception:
                continue
    flow_avg = sum(flows) / len(flows) if flows else 0.0

    # scale and combine
    vol_sc = minmax_scale(vol_share, 0.0, 80.0)  # if alts >80% -> high
    mom_sc = minmax_scale(mom_avg, -10.0, 10.0)
    flow_sc = minmax_scale(flow_avg, -1000000, 1000000) if flows else 50.0

    score = 0.5 * vol_sc + 0.3 * mom_sc + 0.2 * flow_sc
    return clamp(score)

def long_term_score(symbols: List[str]) -> float:
    """
    3) Uzun vadeli coinlerin gücü (günlük/haftalık)
     - 4h/12h/1d IO ortalaması
     - uzun vadeli MTS / net cash
     - balina hareketleri (proxy: high volume spikes)
    """
    # IO across long timeframes
    io_vals = []
    for s in symbols[:30]:
        io_vals.append(compute_io_score(s))
    avg_io = sum(io_vals) / len(io_vals) if io_vals else 50.0

    # volume growth long-term: compare 7d avg to 30d avg (approx via klines)
    vg_list = []
    for s in symbols[:30]:
        try:
            kl_1d = get_klines(f"{s}USDT", interval="1d", limit=40)
            if not kl_1d or len(kl_1d) < 14:
                continue
            vols = [float(k[5]) for k in kl_1d]
            avg7 = sum(vols[-7:]) / 7.0
            avg30 = sum(vols[-30:]) / 30.0 if len(vols) >= 30 else sum(vols) / len(vols)
            vg_list.append(avg7 / (avg30 or 1))
        except Exception:
            continue
    vg = sum(vg_list) / len(vg_list) if vg_list else 1.0
    vg_sc = minmax_scale((vg-1.0)*100.0, -50.0, 50.0)

    # combine avg_io and vg_sc
    score = 0.6 * clamp(avg_io) + 0.4 * vg_sc
    return clamp(score)

# --- Main orchestrator ---
def compute_ap_full() -> Dict:
    """
    Returns:
      {
        "short_vs_btc": float,
        "short_usd": float,
        "long_term": float,
        "ap_aggregate": float,
        "meta": { ... }
      }
    """
    symbols = get_symbols()
    # to limit calls, pick top N
    symbols = symbols[:80]

    s1 = short_vs_btc_score(symbols)
    s2 = short_usd_score(symbols)
    s3 = long_term_score(symbols)

    # aggregate AP: ağırlık önerisi
    AP = 0.4 * s1 + 0.35 * s2 + 0.25 * s3
    return {
        "short_vs_btc": round(s1, 2),
        "short_usd": round(s2, 2),
        "long_term": round(s3, 2),
        "ap_aggregate": round(AP, 2),
        "meta": {
            "symbols_used": len(symbols),
            "computed_at": time.time()
        }
                          }
