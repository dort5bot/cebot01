##
#jobs/check_orders.py
##



import logging
from utils.data import load_orders, save_orders
from utils.binance_api import get_current_price
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

async def check_orders_job(context: ContextTypes.DEFAULT_TYPE):
    orders_data = load_orders()
    changes = []

    for user_id, orders in orders_data.items():
        for order in orders:
            if order["status"] != "open":
                continue

            symbol = order["symbol"]
            entry_price = order["entry_price"]
            amount = order["amount"]
            target_pct = order["target_profit_percent"]
            stop_pct = order["stop_loss_percent"]

            current_price = get_current_price(symbol)
            if not current_price:
                continue

            target_price = entry_price * (1 + target_pct / 100)
            stop_price = entry_price * (1 - stop_pct / 100)

            if current_price >= target_price:
                order["status"] = "closed"
                profit = (current_price - entry_price) * amount
                changes.append((user_id, f"✅ Hedef gerçekleşti: {symbol} ({amount})\nFiyat: {entry_price} → {current_price}\nKar: {profit:.2f} USDT"))

            elif current_price <= stop_price:
                order["status"] = "closed"
                loss = (entry_price - current_price) * amount
                changes.append((user_id, f"🛑 Zarar durdur tetiklendi: {symbol} ({amount})\nFiyat: {entry_price} → {current_price}\nZarar: {loss:.2f} USDT"))

    if changes:
        save_orders(orders_data)
        for user_id, message in changes:
            try:
                await context.bot.send_message(chat_id=int(user_id), text=message)
            except Exception as e:
                logger.warning(f"Mesaj gönderilemedi ({user_id}): {e}")
