# ======================================
# ✅ MegaBot Final - utils/init_files.py
# CSV dosyalarını ve orders.json'u başlatır
# ======================================
import os
import csv
import json

DATA_DIR = "data"

def ensure_dir_exists():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def create_csv_file(filename, headers):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        with open(path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

def create_json_file(filename, default_data):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, indent=2)

def init_data_files():
    ensure_dir_exists()
    
    create_csv_file("order_history.csv", [
        "user_id", "symbol", "amount", "entry_price", "exit_price", "pnl_percent", "result", "timestamp"
    ])

    create_csv_file("daily_report.csv", [
        "user_id", "date", "total_orders", "total_profit_percent", "total_loss_percent"
    ])

    create_csv_file("portfolio_snapshot.csv", [
        "user_id", "date", "total_value_usdt", "total_open_orders", "total_realized_pnl"
    ])

    create_csv_file("fr_log.csv", [
        "symbol", "funding_rate", "timestamp"
    ])

    create_csv_file("error_logs.csv", [
        "timestamp", "error", "details"
    ])

    create_json_file("orders.json", {})

