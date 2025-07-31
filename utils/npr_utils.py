
# ==2====================================
# ✅ MegaBot Final - utils/npr_utils.py
# /npr komutu - Nakit Piyasa Raporu hesaplama
# ======================================


from .binance_api import get_klines

def calculate_npr(symbol="BTCUSDT"):
    klines = get_klines(symbol, interval="15m", limit=4)
    volumes = [float(k[5]) for k in klines]
    trend = round((volumes[-1] - volumes[0]) / (volumes[0] + 1e-9) * 100, 2)
    return {
        "symbol": symbol,
        "volumes": volumes,
        "trend": trend
    }

def check_npr(symbol="BTCUSDT"):
    result = calculate_npr(symbol)
    text = (
        f"{result['symbol']} - NPR Trend: %{result['trend']}\n"
        f"Volüm Değerleri (Son 4 x 15dk):\n"
        f"{result['volumes']}"
    )
    return text
