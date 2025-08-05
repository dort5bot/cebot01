# utils/etf_utils.py

import aiohttp
from datetime import datetime
import pytz

# Kullanılabilir ETF'ler ve açıklamaları
ETF_CONFIG = {
    "BTC": {
        "IBIT": "BlackRock",
        "GBTC": "Grayscale"
    },
    "ETH": {
        "ETHE": "Grayscale"
    }
}

# Yahoo Finance URL şablonu
YAHOO_URL_TEMPLATE = "https://query1.finance.yahoo.com/v8/finance/chart/{}?interval=1d&range=5d"

# 2 günlük kapanış verisi al
async def fetch_last_two_closes(symbol):
    url = YAHOO_URL_TEMPLATE.format(symbol)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            if response.status != 200:
                raise Exception(f"{symbol} için API hatası: {response.status}")
            data = await response.json()

    try:
        result = data["chart"]["result"][0]
        closes = result["indicators"]["adjclose"][0]["adjclose"]
        closes = [round(c, 2) if c is not None else None for c in closes]
        return closes[-2:]  # son 2 gün
    except Exception:
        raise Exception(f"{symbol} için veri çözümlenemedi")

# Rapor üret
async def generate_etf_report():
    tz = pytz.timezone("Europe/Istanbul")
    now = datetime.now(tz)
    date_str = now.strftime("%Y-%m-%d")

    report = f"📊 *Spot ETF Net Akış Raporu* ({date_str})\n\n"

    for asset, etfs in ETF_CONFIG.items():
        total_flow = 0
        flow_lines = []

        for symbol, issuer in etfs.items():
            try:
                closes = await fetch_last_two_closes(symbol)
                if None in closes:
                    raise Exception("Eksik veri")
                flow = closes[1] - closes[0]
                total_flow += flow
                sign = "+" if flow >= 0 else "-"
                flow_lines.append(f"{issuer}: {sign}${abs(flow):,.2f} M$")
            except Exception as e:
                flow_lines.append(f"{issuer}: veri alınamadı")

        emoji = "🟢" if total_flow >= 0 else "🔴"
        total_str = f"+${total_flow:,.2f} M$" if total_flow >= 0 else f"-${abs(total_flow):,.2f} M$"
        flow_details = ", ".join(flow_lines)

        report += f"• {asset}: {total_str} {emoji}\n  ({flow_details})\n"

    return report
    
