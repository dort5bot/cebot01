# utils/td_utils.py2
import requests

def get_trending_symbols(limit=20):
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        response = requests.get(url, timeout=10)
        data = response.json()
    except Exception as e:
        print("API hatası:", e)
        return []

    # Sadece USDT pariteleri ve spot işlemler
    usdt_pairs = [
        item for item in data
        if item["symbol"].endswith("USDT")
        and not item["symbol"].endswith("BULLUSDT")
        and not item["symbol"].endswith("BEARUSDT")
        and float(item["quoteVolume"]) > 1000000  # min hacim filtresi
    ]

    # Hacim ve fiyat artışına göre sıralama
    sorted_list = sorted(
        usdt_pairs,
        key=lambda x: (float(x["priceChangePercent"]), float(x["quoteVolume"])),
        reverse=True
    )

    result = []
    for item in sorted_list[:limit]:
        result.append({
            "symbol": item["symbol"].replace("USDT", ""),
            "change": round(float(item["priceChangePercent"]), 2),
            "volume": float(item["quoteVolume"])
        })

    return result
    
