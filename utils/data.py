
# ======================================
# ✅ MegaBot Final - utils/data.py
# Kullanıcı verisi, emir işlemleri JSON dosyası
# ======================================
import json
import os

ORDERS_FILE = "data/orders.json"

def load_orders():
    if not os.path.exists(ORDERS_FILE):
        return {}
    with open(ORDERS_FILE, "r") as f:
        return json.load(f)

def save_orders(data):
    with open(ORDERS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def add_order(user_id, order):
    data = load_orders()
    uid = str(user_id)
    if uid not in data:
        data[uid] = []
    data[uid].append(order)
    save_orders(data)

def get_orders(user_id):
    return load_orders().get(str(user_id), [])

def update_orders(user_id, orders):
    data = load_orders()
    data[str(user_id)] = orders
    save_orders(data)
