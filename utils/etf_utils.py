# utils/etf_utils.py cg
import aiohttp
import datetime
import json

COINGLASS_API = "https://api.coinglass.com/api/pro/v1/futures/etf/history?type=2"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "accept": "application/json, text/plain, */*"
}

PROVIDER_MAPPING = {
    "IBIT": "BlackRock",
    "FBTC": "Fidelity",
    "BITB": "Bitwise",
    "ARKB": "Ark",
    "GBTC": "Grayscale",
    "ETHE": "Grayscale",
    "HODL": "VanEck",
    "BTCO": "Invesco",
    "EZBC": "Franklin",
    "BRRR": "Valkyrie",
}

def get_coin_from_symbol(symbol: str) -> str:
    if symbol.endswith("E") or symbol.startswith("ETH"):
        return "ETH"
    return "BTC"

async def get_etf_flow_report():
    today = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    report_lines = [f"📊 Spot ETF Net Akış 2Raporu ({today})\n"]

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(COINGLASS_API, headers=HEADERS) as resp:
                if resp.status != 200:
                    return f"❌ Coinglass API durumu: {resp.status}"
                text_data = await resp.text()
                if not text_data.strip():
                    return "❌ Coinglass boş içerik döndürdü (IP engeli veya koruma olabilir)"
                try:
                    data = json.loads(text_data)
                except json.JSONDecodeError as je:
                    return f"❌ JSON ayrıştırma hatası: {je}.\nYanıt: {text_data[:200]}"
    except Exception as e:
        return f"❌ Coinglass verisi alınamadı: {e}"

    try:
        etf_list = data["data"]["etfList"]
    except Exception:
        return "❌ Veri yapısı çözümlenemedi"

    coin_data = {"BTC": [], "ETH": []}

    for item in etf_list:
        symbol = item.get("symbol", "")
        flow_str = item.get("lastNetInflow", "")
        try:
            flow = float(flow_str)
        except:
            continue

        coin = get_coin_from_symbol(symbol)
        provider = PROVIDER_MAPPING.get(symbol, symbol)
        coin_data[coin].append((provider, flow))

    for coin, flows in coin_data.items():
        if not flows:
            report_lines.append(f"• {coin}: Veri yok\n")
            continue

        total = sum([f for _, f in flows])
        emoji = "🟢" if total >= 0 else "🔴"
        flow_lines = [f"{p}: {'+' if f >= 0 else ''}${f:.2f}M" for p, f in flows]
        report_lines.append(f"• {coin}: {'+' if total >= 0 else ''}${total:.2f}M {emoji}\n  ({', '.join(flow_lines)})")

    return "\n".join(report_lines)
