##2
#fr_scheduler.py
#
import requests

def get_fund_report(symbol):
    try:
        url = f"https://fapi.binance.com/futures/data/fundingRate"
        params = {
            "symbol": symbol.upper(),
            "limit": 7
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        report_lines = []
        for entry in data:
            time_str = entry["fundingTime"]
            rate = float(entry["fundingRate"]) * 100
            report_lines.append(f"{time_str}: {rate:.4f}%")

        return "\n".join(report_lines)
    except Exception as e:
        return f"Rapor alınamadı: {e}"
