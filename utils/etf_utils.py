# utils/etf_utils.py cg
# utils/etf_utils.py

import aiohttp
import datetime
from bs4 import BeautifulSoup

COINGLASS_URL = "https://www.coinglass.com/etf"

async def fetch_etf_html():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(COINGLASS_URL, headers=headers) as response:
            if response.status != 200:
                raise Exception(f"Coinglass sayfasına erişilemedi: {response.status}")
            return await response.text()

def parse_etf_data(html):
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not table:
        raise Exception("ETF verisi tablosu bulunamadı")

    rows = table.find_all("tr")[1:]  # Başlık satırını atla
    etf_data = {"BTC": [], "ETH": []}

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 5:
            continue

        symbol = cols[0].text.strip()
        netflow_str = cols[4].text.strip().replace(",", "").replace("$", "").replace("M", "")
        coin = "BTC" if "BTC" in symbol else "ETH" if "ETH" in symbol else None
        provider = symbol

        try:
            netflow = float(netflow_str)
        except ValueError:
            continue

        if coin:
            etf_data[coin].append((provider, netflow))

    return etf_data

async def get_etf_flow_report():
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    report_lines = [f"📊 Spot ETF Net Akış Raporu ({today})\n"]

    try:
        html = await fetch_etf_html()
        etf_data = parse_etf_data(html)
    except Exception as e:
        return f"❌ Coinglass verisi alınamadı: {e}"

    for coin, flows in etf_data.items():
        if not flows:
            report_lines.append(f"• {coin}: Veri bulunamadı\n")
            continue

        total_flow = sum(f for _, f in flows)
        emoji = "🟢" if total_flow >= 0 else "🔴"
        provider_lines = [f"{p}: {'+' if f >= 0 else ''}${f:.2f}M" for p, f in flows]
        total_line = f"• {coin}: {'+' if total_flow >= 0 else ''}${total_flow:.2f}M {emoji}\n  ({', '.join(provider_lines)})"
        report_lines.append(total_line)

    return "\n".join(report_lines)
