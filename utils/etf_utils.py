# utils/etf_utils.py

import aiohttp
from datetime import datetime
import pytz

# ETF simgeleri ve açıklamaları
ETF_CONFIG = {
    "BTC": {
        "IBIT": "BlackRock",
        "GBTC": "Grayscale"
    },
    "ETH": {
        "ETHB": "BlackRock",
        "ETHE": "Grayscale"
    }
}

# Yahoo Finance API URL şablonu
YAHOO_URL_TEMPLATE = "https://query1.finance.yahoo.com/v8/finance/chart/{}?interval=1d&range=5d"

async def fetch_last_two_closes(symbol):
    url = YAHOO_URL_TEMPLATE.format(symbol)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            data = await response.json()
            result = data["chart"]["result"][0]
            closes = result["indicators"]["adjclose"][0]["adjclose"]
            return closes[-2:]  # [önceki, son]

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
                    continue
                flow = closes[1] - closes[0]
                total_flow += flow
                sign = "+" if flow >= 0 else "-"
                flow_lines.append(f"{sign}${abs(flow):,.0f} M$ {issuer}")
            except Exception as e:
                flow_lines.append(f"{issuer}: veri alınamadı")

        emoji = "🟢" if total_flow >= 0 else "🔴"
        total_str = f"+${total_flow:,.0f} M$" if total_flow >= 0 else f"-${abs(total_flow):,.0f} M$"
        detail_str = ", ".join(flow_lines)
        report += f"• {asset}: {total_str} {emoji}\n  ({detail_str})\n"

    return report
                       
