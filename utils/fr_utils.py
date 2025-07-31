
# ==2====================================
# ✅ MegaBot Final - utils/fr_utils.py
# /fr komutu - Fon Raporu
# ======================================


import requests

def get_fr_info(symbol="BTCUSDT"):
    url = f"https://fapi.binance.com/fapi/v1/fundingRate?symbol={symbol}&limit=7"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        if not data or isinstance(data, dict) and "code" in data:
            return "❌ Fonlama verisi alınamadı."

        rates = [float(i["fundingRate"]) * 100 for i in data]
        avg_rate = round(sum(rates) / len(rates), 4)
        last_rate = round(rates[-1], 4)

        text = f"📈 {symbol} Fonlama Raporu (7 Günlük)\n"
        text += f"• Ortalama: {avg_rate}%\n"
        text += f"• Son Oran: {last_rate}%\n"
        text += "• Günlük Oranlar:\n"
        for i, rate in enumerate(rates, 1):
            text += f"   - Gün {i}: {round(rate, 4)}%\n"

        return text

    except Exception as e:
        return f"❌ Hata oluştu: {e}"
