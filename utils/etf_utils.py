# utils/etf_utils.py

import aiohttp
from datetime import datetime
import pytz

async def get_etf_data():
    url = "https://api.sosovalue.com/data/etf/fund-trend?symbol=USBTC"  # örnek endpoint
    headers = {
        "User-Agent": "Mozilla/5.0",
        "accept": "application/json"
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as resp:
                if resp.status != 200:
                    return f"API hatası: {resp.status}"
                data = await resp.json()
    except Exception as e:
        return f"API bağlantı hatası: {e}"

    # Veriyi çözümle
    try:
        rows = data.get("data", {}).get("rows", [])
        if not rows:
            return "Veri bulunamadı."

        # Son 1-2 günün verisi
        latest = rows[-1]
        prev = rows[-2] if len(rows) > 1 else None

        date = latest.get("date")
        value = latest.get("value")
        diff = None
        if prev:
            diff = value - prev.get("value")

        tz = pytz.timezone("Europe/Istanbul")
        now = datetime.now(tz).strftime("%Y-%m-%d %H:%M")

        msg = f"📊 *BTC Spot ETF Net Akışı* ({now})\n"
        msg += f"🟢 Tarih: {date}\n"
        msg += f"💰 Akış: ${value:,.0f}"
        if diff:
            delta = f"(+${diff:,.0f})" if diff > 0 else f"(-${abs(diff):,.0f})"
            msg += f" {delta}"

        return msg
    except Exception as e:
        return f"Veri çözümleme hatası: {e}"
