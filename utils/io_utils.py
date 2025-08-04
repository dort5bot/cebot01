#
##io_utils.py
##
import requests
from utils.binance_api import get_ticker, get_klines
from datetime import datetime
import numpy as np

# Binance API endpoint
BASE_URL = "https://api.binance.com"

def get_all_symbols():
    url = f"{BASE_URL}/api/v3/ticker/24hr"
    data = requests.get(url).json()
    return [x['symbol'] for x in data if x['symbol'].endswith("USDT") and not any(i in x['symbol'] for i in ['UP', 'DOWN', 'BULL', 'BEAR'])]

def get_volume_share():
    url = f"{BASE_URL}/api/v3/ticker/24hr"
    data = requests.get(url).json()
    total_volume = sum([float(x['quoteVolume']) for x in data if x['symbol'].endswith("USDT")])
    vol_dict = {x['symbol']: float(x['quoteVolume']) for x in data if x['symbol'].endswith("USDT")}
    volume_share = {sym: (vol / total_volume) for sym, vol in vol_dict.items()}
    return volume_share

def get_recent_cash_flow(symbol, interval="15m", limit=20):
    klines = get_klines(symbol, interval, limit)
    volumes = [float(k[7]) for k in klines]  # quote asset volume
    changes = np.diff(volumes)
    percent_change = (changes[-1] / volumes[-2]) * 100 if volumes[-2] != 0 else 0
    return round(percent_change, 1)

def get_mts_score(symbol):
    trend = ""
    total_score = 0
    timeframes = ["15m", "1h", "4h", "12h", "1d"]
    arrows = []
    for tf in timeframes:
        change = get_recent_cash_flow(symbol, tf)
        arrows.append("🔼" if change >= 50 else "🔻")
        total_score += 1 if change >= 50 else 0
    score = round(total_score / len(timeframes), 2)
    return score, "".join(arrows)

def get_market_insight_report():
    symbols = get_all_symbols()[:50]
    vol_share = get_volume_share()
    total_market_cash = sum(vol_share.values())
    sorted_vol = sorted(vol_share.items(), key=lambda x: x[1], reverse=True)

    short_term_power = round(sum([v for k, v in sorted_vol[:10]]), 2)
    report = "✅Bölüm-1: Market Bilgisi\n"
    report += f"Kısa Vadeli Market Alım Gücü: {short_term_power:.2f}X\n"
    report += f"Marketteki Hacim Payı: %{round(total_market_cash * 100, 1)}\n"

    report += "\n✅Bölüm-2: Zaman Bazlı Nakit Girişi\n"
    for tf in ["15m", "1h", "4h", "12h", "1d"]:
        changes = [get_recent_cash_flow(sym, tf) for sym in symbols]
        avg_change = round(np.mean(changes), 1)
        arrow = "🔼" if avg_change >= 50 else "🔻"
        report += f"{tf} => %{avg_change} {arrow}\n"

    report += "\n✅Bölüm-3: En Çok Nakit Girişi Olanlar\n"
    report += "Coin Nakit: % Market | 15m:% | Mts | Trend\n"
    for sym, share in sorted_vol[:30]:
        pct15 = get_recent_cash_flow(sym)
        mts, trend = get_mts_score(sym)
        report += f"{sym} Nakit: %{round(share*100,1)} 15m:%{pct15} Mts:{mts} {trend}\n"

    report += "\n✅Bölüm-4: Piyasa Yorum\n"
    report += "Piyasa ciddi anlamda risk barındırıyor. Alım yapma!\n"
    report += "1d nakit girişi %50 üzerine çıkarsa risk azalır.\n"

    return report

def get_coin_insight_report(symbol):
    try:
        pct15 = get_recent_cash_flow(symbol)
        mts, trend = get_mts_score(symbol)
        report = f"✅{symbol} Coin Analizi\n"
        report += f"15 dakikalık Nakit Girişi: %{pct15}\n"
        report += f"MTS Skoru: {mts} {trend}\n"
        report += "Yorum: "
        if mts >= 0.6:
            report += "Güçlü nakit akışı. İlgi yüksek.\n"
        elif mts >= 0.4:
            report += "Kararsız piyasa, dikkatli ol.\n"
        else:
            report += "Zayıf nakit akışı, yatırım için uygun değil.\n"
        return report
    except:
        return f"❌ {symbol} için veri alınamadı."
