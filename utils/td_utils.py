# utils/td_utils.py
import requests

def get_trending_symbols(limit=20):
    try:
        response = requests.get("https://api.binance.com/api/v3/ticker/24hr", timeout=10)
        response.raise_for_status()
        all_data = response.json()
    except Exception as e:
        print("Binance API hatası:", e)
        return []

    usdt_pairs = [
        item for item in all_data
        if item["symbol"].endswith("USDT")
        and "DOWN" not in item["symbol"]
        and "UP" not in item["symbol"]
        and "BULL" not in item["symbol"]
        and "BEAR" not in item["symbol"]
        and float(item.get("quoteVolume", 0)) > 1000000
    ]

    sorted_data = sorted(
        usdt_pairs,
        key=lambda x: (float(x["priceChangePercent"]), float(x["quoteVolume"])),
        reverse=True
    )

    return [
        {
            "symbol": item["symbol"].replace("USDT", ""),
            "change": round(float(item["priceChangePercent"]), 2),
            "volume": float(item["quoteVolume"])
        }
        for item in sorted_data[:limit]
    ]
    
