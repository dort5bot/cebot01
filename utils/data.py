
# ==2====================================
# ✅ MegaBot Final - utils/data.py
# Kullanıcı verisi, emir işlemleri JSON dosyası
# ======================================
import json
import os

DATA_DIR = "data"
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
API_KEYS_FILE = os.path.join(DATA_DIR, "api_keys.json")

# Emir kayıt sistemleri
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


# ✅ API KEY yönetimi
def save_api_key(user_id, api_key, secret_key):
    os.makedirs(DATA_DIR, exist_ok=True)
    data = {}

    if os.path.exists(API_KEYS_FILE):
        with open(API_KEYS_FILE, "r") as f:
            data = json.load(f)

    data[str(user_id)] = {
        "api_key": api_key,
        "secret_key": secret_key
    }

    with open(API_KEYS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def load_api_key(user_id):
    if not os.path.exists(API_KEYS_FILE):
        return None, None

    with open(API_KEYS_FILE, "r") as f:
        data = json.load(f)

    user_data = data.get(str(user_id))
    if user_data:
        return user_data.get("api_key"), user_data.get("secret_key")
    return None, None

