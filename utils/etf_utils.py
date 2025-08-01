# revize utils/etf_utils.py
# ETF verisi + ABD borsa + Trend analiz + BlackRock/Grayscale

import csv
from datetime import datetime
from utils.binance_api import get_etf_flows
from utils.market_data import get_us_stock_data
from pathlib import Path

ETF_CSV = Path("data/etf_history.csv")
MAX_RECORDS = 60

def format_number(n):
    return f"{n:,.2f}".replace(",", ".") if isinstance(n, float) else str(n)

def trend_emoji(change):
    return "📈" if change > 0 else ("📉" if change < 0 else "➖")

def percent_diff(new, old):
    if old == 0:
        return 0.0
    return ((new - old) / old) * 100

def read_etf_history():
    if not ETF_CSV.exists():
        return []
    with open(ETF_CSV, newline="") as f:
        return list(csv.DictReader(f))

def write_etf_history(data):
    history = read_etf_history()
    history.append(data)
    if len(history) > MAX_RECORDS:
        history = history[-MAX_RECORDS:]
    with open(ETF_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=data.keys())
        writer.writeheader()
        writer.writerows(history)

def calculate_avg(data_list, key):
    values = [float(row[key]) for row in data_list if row.get(key)]
    return sum(values) / len(values) if values else 0.0

def generate_etf_report(args):
    etf_data = get_etf_flows()  # API'den anlık veri al
    if not etf_data:
        return "❌ ETF verisi alınamadı."

    # Tarih
    today_str = datetime.now().strftime("%d %B %Y")
    date_title = f"\ud83d\udcca ETF Ak\u0131\u015f\u0131 ({today_str})"

    # CSV kayıt işlemi
    record = {
        "date": today_str,
        "btc": etf_data["BTC"],
        "eth": etf_data["ETH"],
        "br_btc": etf_data["BR_BTC"],
        "br_eth": etf_data["BR_ETH"],
        "gr_btc": etf_data["GR_BTC"],
        "gr_eth": etf_data["GR_ETH"],
    }
    write_etf_history(record)

    history = read_etf_history()

    def build_coin_line(coin):
        val = float(etf_data[coin])
        last_val = float(history[-2][coin]) if len(history) >= 2 else val
        change_pct = percent_diff(val, last_val)
        emoji = trend_emoji(change_pct)

        br_val = float(etf_data[f"BR_{coin}"])
        gr_val = float(etf_data[f"GR_{coin}"])

        return f"{coin}: {format_number(val)}$ (Son: {format_number(last_val)}$) {emoji} {change_pct:+.2f}%\n" \
               f"(+{format_number(br_val)}M$ BlackRock, –{format_number(gr_val)}M$ Grayscale)"

    def build_avg_line(coin, days):
        recent = history[-days:] if len(history) >= days else history
        avg = calculate_avg(recent, coin)
        val = float(etf_data[coin])
        change_pct = percent_diff(val, avg)
        emoji = trend_emoji(change_pct)

        br_vals = [float(row[f"br_{coin.lower()}"]) for row in recent if row.get(f"br_{coin.lower()}")]
        gr_vals = [float(row[f"gr_{coin.lower()}"]) for row in recent if row.get(f"gr_{coin.lower()}")]
        br_avg = sum(br_vals)/len(br_vals) if br_vals else 0
        gr_avg = sum(gr_vals)/len(gr_vals) if gr_vals else 0

        br_pct = percent_diff(float(etf_data[f"BR_{coin}"]), br_avg)
        gr_pct = percent_diff(float(etf_data[f"GR_{coin}"]), gr_avg)

        return f"{coin}: {format_number(val)}$ (Ort.: {format_number(avg)}$) {emoji} {change_pct:+.2f}%\n" \
               f"(ort: +{format_number(br_avg)}M$ BlackRock {trend_emoji(br_pct)} %{abs(br_pct):.0f} ," \
               f"ort: –{format_number(gr_avg)}M$ Grayscale {trend_emoji(gr_pct)} %{abs(gr_pct):.0f})"

    if len(args) == 1 and args[0].isdigit():
        days = int(args[0])
        title = f"\ud83d\udcca Son {days} G\u00fcnl\u00fck Ortalama Kar\u015f\u0131la\u015ft\u0131rma"
        btc_line = build_avg_line("BTC", days)
        eth_line = build_avg_line("ETH", days)
        return f"{title}\n\n{btc_line}\n\n{eth_line}"

    elif len(args) == 1 and args[0] == "abd":
        us_data = get_us_stock_data()
        if not us_data:
            return "❌ ABD verileri al\u0131namad\u0131."
        lines = [f"{name}: {change}" for name, change in us_data.items()]
        return "\ud83c\udf10 ABD Borsas\u0131\n" + "\n".join(lines)

    else:
        btc_line = build_coin_line("BTC")
        eth_line = build_coin_line("ETH")
        return f"{date_title}\n\n{btc_line}\n\n{eth_line)
    
