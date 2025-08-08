# == ✅ MegaBot Final - utils/ap_calc.py ==
# Altcoin Güç Skorları Hesaplama

import statistics
from utils.io_utils import get_all_symbols, get_volume_share, get_recent_cash_flow, get_mts_score, get_io_ratio
from utils.binance_api import get_price_change

def normalize(value, min_val=-1, max_val=1):
    """Veriyi 0-100 arası normalize eder."""
    try:
        return round(((value - min_val) / (max_val - min_val)) * 100, 2)
    except:
        return 50.0

def alt_vs_btc_strength():
    """Altların kısa vadede BTC’ye karşı gücü"""
    symbols = get_all_symbols()
    alt_symbols = [s for s in symbols if s not in ["BTC", "ETH"]]

    btc_vol_share = get_volume_share("BTC")
    alt_vol_share = sum(get_volume_share(s) for s in alt_symbols) / len(alt_symbols)

    btc_change = get_price_change("BTC", "1h")
    alt_change = statistics.mean(get_price_change(s, "1h") for s in alt_symbols)

    btc_io = get_io_ratio("BTC")
    alt_io = statistics.mean(get_io_ratio(s) for s in alt_symbols)

    score = (alt_vol_share - btc_vol_share) + (alt_change - btc_change) + ((alt_io - btc_io) / 100)
    return normalize(score, -0.5, 0.5)

def alt_usdt_strength():
    """Altların kısa vadede gücü (USD bazlı)"""
    symbols = get_all_symbols()
    alt_symbols = [s for s in symbols if s not in ["BTC"]]

    alt_vol_share = statistics.mean(get_volume_share(s) for s in alt_symbols)
    alt_change = statistics.mean(get_price_change(s, "1h") for s in alt_symbols)
    alt_io = statistics.mean(get_io_ratio(s) for s in alt_symbols)

    score = alt_vol_share + alt_change + (alt_io / 100)
    return normalize(score, 0, 2)

def long_term_strength():
    """Coinlerin uzun vadede gücü"""
    symbols = get_all_symbols()

    mts_scores = statistics.mean(get_mts_score(s) for s in symbols)
    price_change_24h = statistics.mean(get_price_change(s, "24h") for s in symbols)
    avg_io = statistics.mean(get_io_ratio(s) for s in symbols)

    score = mts_scores + price_change_24h + (avg_io / 100)
    return normalize(score, 0, 2)
