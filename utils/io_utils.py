# ==2-3=4===================================
# ✅ MegaBot Final - utils/io_utils.py
# /io komutu - Alış/Satış baskı oranları hesaplama
# ======================================
from .binance_api import get_order_book, get_klines
from utils.symbols import get_all_usdt_symbols  # tüm coinleri çekmek için
import numpy as np

def calculate_mts(trend_list):
    # Basit MTS puanı (geliştirilebilir)
    score = 0
    for t in trend_list:
        if t == "🔼":
            score += 1
        elif t == "🔻":
            score -= 1
    return round(score / len(trend_list), 2)

def detect_trend(pct):
    return "🔼" if pct >= 50 else "🔻"

def get_io_market_analysis():
    symbols = get_all_usdt_symbols()
    coin_data = []
    total_market_cash = 0
    volume_share_acc = 0

    # Zamansal aralıklar
    intervals = ["15m", "1h", "4h", "12h", "1d"]
    interval_map = {"15m": "15m", "1h": "1h", "4h": "4h", "12h": "12h", "1d": "1d"}

    # Bölüm 1: genel market verisi
    for sym in symbols:
        klines = get_multiple_klines(sym, intervals=interval_map.values(), limit=2)
        if not klines or "1h" not in klines:
            continue

        last_price = float(klines["1h"][-1][4])
        volume_1h = float(klines["1h"][-1][5])
        coin_cash = last_price * volume_1h
        total_market_cash += coin_cash

        coin_entry = {"symbol": sym, "cash": coin_cash, "trend_data": {}, "trend_texts": [], "volume_1h": volume_1h}
        
        for key in interval_map:
            kline_data = klines.get(key)
            if kline_data and len(kline_data) >= 2:
                prev_close = float(kline_data[-2][4])
                curr_close = float(kline_data[-1][4])
                pct = (curr_close - prev_close) / prev_close * 100
                coin_entry["trend_data"][key] = round(pct, 2)
                coin_entry["trend_texts"].append(detect_trend(pct))
        
        coin_data.append(coin_entry)

    # Sıralama ve filtreleme
    sorted_coins = sorted(coin_data, key=lambda x: x["cash"], reverse=True)[:30]
    
    market_share = sum([c["volume_1h"] for c in sorted_coins]) / sum([c["volume_1h"] for c in coin_data]) * 100
    market_power = round(np.mean([abs(c["trend_data"].get("1h", 0)) for c in sorted_coins]) / 100, 2)

    # Bölüm 2: zaman bazlı market değişimleri
    time_analysis = {}
    for interval in interval_map:
        pct_list = [c["trend_data"].get(interval, 0) for c in sorted_coins if interval in c["trend_data"]]
        avg_pct = np.mean(pct_list)
        time_analysis[interval] = f"%{round(avg_pct, 1)} {detect_trend(avg_pct)}"

    # Bölüm 3: nakit akışı listesi
    flow_lines = []
    for coin in sorted_coins:
        cash_pct = round(coin["cash"] / total_market_cash * 100, 1)
        mts_score = calculate_mts(coin["trend_texts"])
        line = f"{coin['symbol']} Nakit: %{cash_pct} 15m:%{coin['trend_data'].get('15m', 0)} Mts: {mts_score} {' '.join(coin['trend_texts'])}"
        flow_lines.append(line)

    # Bölüm 4: yorum
    d1_value = float(time_analysis['1d'].split('%')[1].split(' ')[0])
    if d1_value > 50:
        comment = "✅ Günlük nakit girişi %50'nin üstünde. Risk azalmış görünüyor."
    else:
        comment = (
            "❗ Piyasa ciddi anlamda risk barındırıyor. Alım Yapma!\n"
            "Günlük nakit giriş oranı %50 üzerine çıkarsa risk azalacaktır."
        )

    result = (
        "✅ Bölüm 1: Market Hakkında Bilgi\n"
        f"Kısa Vadeli Market Alım Gücü: {market_power}X\n"
        f"Marketteki Hacim Payı: %{round(market_share, 1)}\n\n"

        "✅ Bölüm 2: Zamansal Nakit Girişi\n" +
        "\n".join([f"{k} => {v}" for k, v in time_analysis.items()]) + "\n\n"

        "✅ Bölüm 3: Nakit Göçü Raporu (En çok para girenler)\n" +
        "\n".join(flow_lines) + "\n\n"

        "✅ Bölüm 4: Yorum\n" + comment
    )

    return result
def get_io_analysis(symbol="BTCUSDT", limit=10):
    orderbook = get_order_book(symbol, limit=limit)
    if not orderbook:
        return "⚠️ Emir defteri verisi alınamadı."

    try:
        bids = orderbook.get("bids", [])
        asks = orderbook.get("asks", [])

        buy_volume = sum(float(bid[1]) for bid in bids)
        sell_volume = sum(float(ask[1]) for ask in asks)

        total_volume = buy_volume + sell_volume
        if total_volume == 0:
            return "⚠️ Emir defterinde işlem hacmi yok."

        buy_pressure = (buy_volume / total_volume) * 100
        sell_pressure = (sell_volume / total_volume) * 100

        comment = ""
        if buy_pressure > sell_pressure + 10:
            comment = "Alım baskısı güçlü görünüyor."
        elif sell_pressure > buy_pressure + 10:
            comment = "Satım baskısı güçlü görünüyor."
        else:
            comment = "Piyasa dengede."

        result = (
            f"📊 {symbol} Emir Defteri Analizi:\n"
            f"• Alım Hacmi: {buy_volume:.2f}\n"
            f"• Satım Hacmi: {sell_volume:.2f}\n"
            f"• Alım Baskısı: %{buy_pressure:.2f}\n"
            f"• Satım Baskısı: %{sell_pressure:.2f}\n"
            f"📝 Yorum: {comment}"
        )

        return result

    except Exception as e:
        return f"⚠️ Analiz hatası: {e}"
