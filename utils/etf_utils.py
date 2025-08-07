# utils/etf_utils.py farisi

import aiohttp
from bs4 import BeautifulSoup

async def fetch_farside_data(coin: str):
    url = f"https://farside.co.uk/{coin.lower()}/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise Exception(f"{coin} için Farside erişim hatası: {response.status}")
            html = await response.text()

    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    if not table:
        raise Exception(f"{coin} için Farside verisi alınamadı.")

    rows = table.find_all("tr")[1:]  # Başlık satırını atla
    data = []

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 2:
            continue
        date_str = cols[0].get_text(strip=True)
        try:
            netflow = float(cols[1].get_text(strip=True).replace(",", "").replace("$", ""))
        except ValueError:
            continue
        data.append((date_str, netflow))

    if len(data) < 2:
        raise Exception(f"{coin} için yeterli geçmiş veri yok.")

    today_value = data[0][1]
    yesterday_value = data[1][1]
    change = today_value - yesterday_value
    trend = "📈" if change > 0 else ("📉" if change < 0 else "➡️")
    
    return {
        "today": today_value,
        "change": change,
        "trend": trend,
        "raw": data[:3]
    }
    
