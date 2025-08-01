# utils/etf_utils.py

import os, csv, requests
import yfinance as yf
from datetime import datetime

CSV_FILE = "data/etf_history.csv"

def get_etf_data(coins=["btc", "eth"]):
    url = "https://api.sosovalue.com/api/v1/fund/etf/spot"
    headers = {"User-Agent": "Mozilla/5.0", "accept": "application/json"}
    result = {}
    try:
        res = requests.get(url, headers=headers, timeout=10).json()
        data = res.get("data", [])
        for c in coins:
            for item in data:
                if item["symbol"].lower() == c.lower():
                    total = round(float(item.get("totalNetInflow", 0)), 2)
                    funds_dict = {f["name"]: round(float(f["netInflow"]), 2) for f in item.get("etfList", [])}
                    result[c.upper()] = {"total": total, "funds": funds_dict}
        return result
    except Exception as e:
        print("ETF veri hatası:", e)
        return {}

def get_us_markets():
    symbols = {
        "Microstrategy": "MSTR", "Coinbase": "COIN", "Nvidia": "NVDA", "Tesla": "TSLA",
        "Altın": "GC=F", "Gümüş": "SI=F", "Petrol": "CL=F", "US10Y": "^TNX"
    }
    results = {}
    for name, ticker in symbols.items():
        try:
            info = yf.Ticker(ticker).info
            results[name] = round(info["regularMarketChangePercent"], 2)
        except:
            results[name] = None
    return results

def save_etf_to_csv(etf_data):
    rows = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8") as f:
            rows = list(csv.reader(f))

    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    btc = etf_data.get("BTC", {}).get("total", 0)
    eth = etf_data.get("ETH", {}).get("total", 0)
    btc_br = etf_data.get("BTC", {}).get("funds", {}).get("BlackRock", 0)
    btc_gr = etf_data.get("BTC", {}).get("funds", {}).get("Grayscale", 0)
    eth_br = etf_data.get("ETH", {}).get("funds", {}).get("BlackRock", 0)
    eth_gr = etf_data.get("ETH", {}).get("funds", {}).get("Grayscale", 0)

    rows.append([date_str, btc, eth, btc_br, btc_gr, eth_br, eth_gr])

    if len(rows) > 60:
        rows = rows[-60:]

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(rows)

def load_csv_last():
    if not os.path.exists(CSV_FILE): return None
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))
        return rows[-1] if rows else None

def load_csv_avg(n=15):
    if not os.path.exists(CSV_FILE): return None
    with open(CSV_FILE, "r", encoding="utf-8") as f:
        rows = list(csv.reader(f))[-n:]
        if not rows: return None
        btc_avg = sum(float(r[1]) for r in rows) / len(rows)
        eth_avg = sum(float(r[2]) for r in rows) / len(rows)
        btc_br_avg = sum(float(r[3]) for r in rows) / len(rows)
        btc_gr_avg = sum(float(r[4]) for r in rows) / len(rows)
        eth_br_avg = sum(float(r[5]) for r in rows) / len(rows)
        eth_gr_avg = sum(float(r[6]) for r in rows) / len(rows)
        return btc_avg, eth_avg, btc_br_avg, btc_gr_avg, eth_br_avg, eth_gr_avg

def trend_arrow(current, past):
    if past == 0: return "➖ 0%"
    change = ((current - past) / abs(past)) * 100
    arrow = "📈" if change > 0 else "📉" if change < 0 else "➖"
    return f"{arrow} {change:.2f}%"

def trend_percent(current, past):
    if past == 0: return "➖ %0"
    change = ((current - past) / abs(past)) * 100
    icon = "📈" if change > 0 else "🔻" if change < 0 else "➖"
    return f"{icon} %{abs(change):.0f}"
