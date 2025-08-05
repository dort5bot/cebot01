# ==2====================================
# ✅ MegaBot Final - utils/nls_utils.py
# /nls komutu - Net Likidite Skoru hesaplama
# ======================================

import pandas as pd
import os
from datetime import datetime
from utils.io_utils import get_mts_score

CSV_PATH = "data/signals.csv"
TIMEFRAMES = ["15m", "1h", "4h", "12h", "1d"]

def init_csv():
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(CSV_PATH):
        df = pd.DataFrame(columns=["symbol"] + TIMEFRAMES + ["timestamp"])
        df.to_csv(CSV_PATH, index=False)

def append_signal(symbol):
    init_csv()
    df = pd.read_csv(CSV_PATH)

    score, trends = get_mts_score(symbol)
    if len(trends) != len(TIMEFRAMES):
        return False

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    row = {"symbol": symbol, "timestamp": now}
    row.update(dict(zip(TIMEFRAMES, list(trends))))
    df = pd.concat([df, pd.DataFrame([row])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)
    return True

def read_signals():
    init_csv()
    try:
        return pd.read_csv(CSV_PATH)
    except:
        return pd.DataFrame()

def remove_signal(symbol):
    df = read_signals()
    df = df[df['symbol'] != symbol]
    df.to_csv(CSV_PATH, index=False)

def check_signals():
    df = read_signals()
    report = "⏰ Alarm Taraması Sonucu:\n"
    if df.empty:
        return "🚫 Aktif alarm yok."

    for _, row in df.iterrows():
        symbol = row['symbol']
        trend_data = " ".join([f"{tf}:{row[tf]}" for tf in TIMEFRAMES])
        report += f"🚨 {symbol} → {trend_data}\n"
        remove_signal(symbol)  # Alarm sonrası sil
    return report
