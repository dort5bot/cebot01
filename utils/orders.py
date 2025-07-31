# 3✅ MegaBot Final - utils/orders.py
# Emir yönetim sistemi: /al /sat /stop /raporum komutları için

import os
import csv
from datetime import datetime
from utils.binance_api import get_price

DATA_DIR = "data"


def get_order_file(user_id):
    return os.path.join(DATA_DIR, f"{user_id}_orders.csv")


def add_order(user_id, symbol, amount, target_percent, stop_percent):
    price = get_price(symbol)
    if price is None:
        return f"❌ Fiyat alınamadı: {symbol}"

    entry_price = round(price, 4)
    target_price = round(entry_price * (1 + target_percent / 100), 4)
    stop_price = round(entry_price * (1 - stop_percent / 100), 4)

    file_path = get_order_file(user_id)
    os.makedirs(DATA_DIR, exist_ok=True)

    is_new = not os.path.exists(file_path)
    with open(file_path, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["symbol", "amount", "entry", "target", "stop", "datetime"])
        writer.writerow([symbol, amount, entry_price, target_price, stop_price, datetime.now().isoformat()])

    return (
        f"✅ Emir eklendi:\n"
        f"• Coin: {symbol}\n"
        f"• Miktar: {amount}\n"
        f"• Giriş: {entry_price}\n"
        f"• Hedef (%{target_percent}): {target_price}\n"
        f"• Zarar (%{stop_percent}): {stop_price}"
    )


def close_order_by_target(user_id, symbol, amount, target_percent):
    price = get_price(symbol)
    if price is None:
        return f"❌ Fiyat alınamadı: {symbol}"

    file_path = get_order_file(user_id)
    if not os.path.exists(file_path):
        return "❌ Açık emir bulunamadı."

    orders = []
    found = False
    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["symbol"] == symbol and float(row["amount"]) == amount:
                entry = float(row["entry"])
                target_price = round(entry * (1 + target_percent / 100), 4)
                if price >= target_price:
                    found = True
                    continue  # Emri kaldır (satıldı)
            orders.append(row)

    if found:
        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["symbol", "amount", "entry", "target", "stop", "datetime"])
            writer.writeheader()
            writer.writerows(orders)
        return f"✅ Satış tamamlandı: {symbol} {amount} adet (Fiyat {price})"
    else:
        return "ℹ️ Hedefe ulaşan emir bulunamadı."


def close_order_by_stop(user_id, symbol, amount, stop_percent):
    price = get_price(symbol)
    if price is None:
        return f"❌ Fiyat alınamadı: {symbol}"

    file_path = get_order_file(user_id)
    if not os.path.exists(file_path):
        return "❌ Açık emir bulunamadı."

    orders = []
    found = False
    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["symbol"] == symbol and float(row["amount"]) == amount:
                entry = float(row["entry"])
                stop_price = round(entry * (1 - stop_percent / 100), 4)
                if price <= stop_price:
                    found = True
                    continue  # Emri kaldır (zararına çık)
            orders.append(row)

    if found:
        with open(file_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["symbol", "amount", "entry", "target", "stop", "datetime"])
            writer.writeheader()
            writer.writerows(orders)
        return f"🛑 Stop-loss işlemi uygulandı: {symbol} {amount} adet (Fiyat {price})"
    else:
        return "ℹ️ Zarar seviyesine ulaşan emir bulunamadı."


def list_active_orders(user_id):
    file_path = get_order_file(user_id)
    if not os.path.exists(file_path):
        return "🔎 Açık emir bulunamadı."

    result = "📋 Açık Emirler:\n"
    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)
        orders = list(reader)

        if not orders:
            return "🔎 Açık emir bulunamadı."

        for row in orders:
            result += (
                f"• Coin: {row['symbol']} | Miktar: {row['amount']}\n"
                f"  Giriş: {row['entry']} | Hedef: {row['target']} | Stop: {row['stop']}\n"
                f"  📅 {row['datetime']}\n"
                "------------------------\n"
            )

    return result


def generate_report(user_id):
    file_path = get_order_file(user_id)
    if not os.path.exists(file_path):
        return "🔎 Hiç işlem kaydı yok.", None

    result = "📊 İşlem Raporu:\n"
    with open(file_path, newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        if not rows:
            return "🔎 Hiç işlem bulunamadı.", None

        for row in rows:
            result += (
                f"• {row['symbol']} | Miktar: {row['amount']} | Giriş: {row['entry']} | 🎯 {row['target']} | 🛑 {row['stop']}\n"
                f"  📅 {row['datetime']}\n"
                "------------------------\n"
            )

    return result, file_path
