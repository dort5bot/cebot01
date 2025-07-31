# ✅ MegaBot Final - utils/etf_utils.py
# Binance borsasındaki ETF tokenları listeler ve analiz eder

import requests

def get_etf_info():
    url = "https://api.binance.com/sapi/v1/bswap/pools"
    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        etf_list = []
        for pool in data:
            name = pool.get("name", "")
            if any(x in name.upper() for x in ["UP", "DOWN", "BULL", "BEAR"]):
                etf_list.append(name)

        if not etf_list:
            return "❗ Binance üzerinde aktif ETF tokenı bulunamadı."

        text = "📊 Binance ETF Tokenları:\n"
        text += "\n".join(f"• {etf}" for etf in sorted(etf_list))
        return text

    except Exception as e:
        return f"❌ ETF verisi alınırken hata oluştu: {e}"
