# ======================================
# ✅ MegaBot Final - utils/init_files.py
# CSV ve JSON dosyalarını başlatır (data, store, history)
# ======================================

import os
import csv
import json
import pandas as pd

DATA_DIR = "data"
STORE_DIR = "store"
HISTORY_DIR = "history"

def ensure_dirs():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(STORE_DIR, exist_ok=True)
    os.makedirs(HISTORY_DIR, exist_ok=True)

def create_csv_file(path, headers):
    if not os.path.exists(path):
        with open(path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

def create_json_file(path, default_data):
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=2)

def init_data_files():
    ensure_dirs()

    # === data klasörü CSV ===
    create_csv_file(f"{DATA_DIR}/order_history.csv", [
        "user_id", "symbol", "amount", "entry_price", "exit_price", "pnl_percent", "result", "timestamp"
    ])
    create_csv_file(f"{DATA_DIR}/daily_report.csv", [
        "user_id", "date", "total_orders", "total_profit_percent", "total_loss_percent"
    ])
    create_csv_file(f"{DATA_DIR}/portfolio_snapshot.csv", [
        "user_id", "date", "total_value_usdt", "total_open_orders", "total_realized_pnl"
    ])
    create_csv_file(f"{DATA_DIR}/fr_log.csv", [
        "symbol", "funding_rate", "timestamp"
    ])
    create_csv_file(f"{DATA_DIR}/error_logs.csv", [
        "timestamp", "error", "details"
    ])

    # === ETF için klasörler ===
    etf_history_path = f"{HISTORY_DIR}/etf_history.csv"
    if not os.path.exists(etf_history_path):
        df = pd.DataFrame(columns=["timestamp", "BTC", "ETH", "SOL", "BNB", "XRP"])
        df.to_csv(etf_history_path, index=False)

    etf_store_path = f"{STORE_DIR}/etf_store.json"
    if not os.path.exists(etf_store_path):
        create_json_file(etf_store_path, {})

    # === JSON ===
    create_json_file(f"{DATA_DIR}/orders.json", {})
