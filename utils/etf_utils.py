# utils/etf_utils.py farisi

import aiohttp
from bs4 import BeautifulSoup

FARSIDE_URLS = {
    "BTC": "https://farside.co.uk/btc/",
    "ETH": "https://farside.co.uk/eth/"
}

PROVIDERS = ["BlackRock", "Fidelity", "Grayscale"]

def interpret_trend(today, yesterday):
    try:
        today = float(today)
        yesterday = float(yesterday)
    except:
        return "Trend belirlenemedi ❓"

    if today > 0 and yesterday > 0:
        if today > yesterday:
            return "Düne göre artış 📈"
        elif today < yesterday:
            return "Düne göre azalış ↘️"
        else:
            return "Aynı seviye ➖"
    elif today < 0 and yesterday < 0:
        if today < yesterday:
            return "Çıkış artışı 🔻"
        elif today > yesterday:
            return "Çıkış azaldı ↗️"
        else:
            return "Aynı seviye ➖"
    elif today > 0 and yesterday < 0:
        return "Pozitife döndü 🟢"
    elif today < 0 and yesterday > 0:
        return "Negatife döndü 🔴"
    else:
        return "Trend belirlenemedi ❓"

async def fetch_coin_etf_data(coin):
    url = FARSIDE_URLS[coin]
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status != 200:
                raise Exception(f"{coin} için 2❗Farside verisi alınamadı.")
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not table:
        raise Exception(f"{coin} için tablo bulunamadı.")

    rows = table.find_all("tr")[1:]
    if len(rows) < 2:
        raise Exception(f"{coin} için yeterli geçmiş veri yok.")

    today_row = [td.text.strip().replace("$", "") for td in rows[0].find_all("td")]
    yesterday_row = [td.text.strip().replace("$", "") for td in rows[1].find_all("td")]

    date = today_row[0]
    today_values = today_row[1:]
    yesterday_values = yesterday_row[1:]

    if len(today_values) != len(PROVIDERS) + 1:
        raise Exception(f"{coin} veri formatı beklenen gibi değil.")

    provider_today = list(map(lambda v: float(v.replace(",", "")), today_values[:-1]))
    provider_yesterday = list(map(lambda v: float(v.replace(",", "")), yesterday_values[:-1]))

    total_today = float(today_values[-1].replace(",", ""))
    total_yesterday = float(yesterday_values[-1].replace(",", ""))

    trend = interpret_trend(total_today, total_yesterday)
    emoji = "🟢" if total_today >= 0 else "🔴"
    total_str = f"{'+' if total_today >= 0 else ''}${total_today:.2f} M$"

    provider_lines = []
    for name, val in zip(PROVIDERS, provider_today):
        p_str = f"{'+' if val >= 0 else ''}${val:.2f} M$"
        provider_lines.append(f"  {name}: {p_str}")

    coin_report = f"• {coin}: {total_str} {emoji}   ({trend})\n" + "\n".join(provider_lines)
    return date, coin_report

async def get_full_etf_report():
    btc_date, btc_report = await fetch_coin_etf_data("BTC")
    eth_date, eth_report = await fetch_coin_etf_data("ETH")

    # En güncel tarihi üstte göstermek için
    report_date = btc_date if btc_date >= eth_date else eth_date
    return f"📊 Spot ETF Net Akış Raporu ({report_date})\n\n{btc_report}\n\n{eth_report}"
        

