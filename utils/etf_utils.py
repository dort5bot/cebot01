# utils/etf_utils.py
import os
import pandas as pd
from datetime import datetime
from utils.binance_api import get_price

ETF_LIST = {
    "BTC": "BTCUSDT",
    "ETH": "ETHUSDT",
    "SOL": "SOLUSDT",
    "BNB": "BNBUSDT",
    "XRP": "XRPUSDT"
}

HISTORY_FILE = "history/etf_history.csv"

def get_etf_summary():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    prices = {symbol: get_price(pair) for symbol, pair in ETF_LIST.items()}
    
    save_etf_data(now, prices)

    summary = f"📊 <b>ETF Fiyat Özeti</b>\n🕒 {now} UTC\n\n"
    for coin, price in prices.items():
        summary += f"• {coin}: ${price:.2f}\n"
    return summary

def save_etf_data(timestamp, prices):
    os.makedirs("history", exist_ok=True)
    df = pd.DataFrame([{"timestamp": timestamp, **prices}])
    if not os.path.exists(HISTORY_FILE):
        df.to_csv(HISTORY_FILE, index=False)
    else:
        df.to_csv(HISTORY_FILE, mode='a', header=False, index=False)
