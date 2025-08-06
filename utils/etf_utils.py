# utils/etf_utils.py2
import aiohttp
import datetime

ETF_CONFIG = {
    "BTC": {
        "BlackRock": "IBIT",
        "Grayscale": "GBTC"
    },
    "ETH": {
        "BlackRock": "FBTC",
        "Grayscale": "ETHE"
    }
}

async def fetch_last_two_closes(symbol):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=5d"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as response:
            if response.status != 200:
                raise Exception(f"{symbol} için API hatası: {response.status}")
            data = await response.json()

    try:
        result = data["chart"]["result"][0]
        closes = result["indicators"]["adjclose"][0]["adjclose"]
        volumes = result["indicators"]["quote"][0]["volume"]

        # None olmayan kapanış ve hacimleri eşleştir
        cleaned = [(c, v) for c, v in zip(closes, volumes) if c is not None and v is not None]

        if len(cleaned) < 2:
            raise Exception(f"{symbol} için yeterli geçerli veri yok.")

        (prev_close, _), (last_close, volume) = cleaned[-2], cleaned[-1]
        price_diff = last_close - prev_close
        net_flow = round(price_diff * volume / 1_000_000, 2)  # Milyon dolar cinsinden
        return net_flow
    except Exception as e:
        raise Exception(f"{symbol} için veri çözümlenemedi: {e}")

async def get_etf_flow_report():
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    report_lines = [f"📊 Spot ETF Net Akış Raporu ({today})\n"]

    for coin, providers in ETF_CONFIG.items():
        total_flow = 0
        provider_lines = []
        for provider_name, symbol in providers.items():
            try:
                flow = await fetch_last_two_closes(symbol)
                total_flow += flow
                flow_str = f"{'+' if flow >= 0 else ''}${flow} M$"
                provider_lines.append(f"{provider_name}: {flow_str}")
            except Exception as e:
                provider_lines.append(f"{provider_name}: veri alınamadı")

        total_str = f"{'+' if total_flow >= 0 else ''}${total_flow:.2f} M$"
        emoji = "🟢" if total_flow >= 0 else "🔴"
        provider_text = ", ".join(provider_lines)
        report_lines.append(f"• {coin}: {total_str} {emoji}\n  ({provider_text})")

    return "\n".join(report_lines)
