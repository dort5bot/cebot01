# utils/p_utils.py

import requests
import pandas as pd
import numpy as np
from datetime import datetime

BINANCE_URL = "https://api.binance.com"

def get_price_summary(symbols):
    result = []
    for symbol in symbols:
        try:
            sym = symbol.upper() + "USDT"
            url = f"{BINANCE_URL}/api/v3/ticker/24hr?symbol={sym}"
            r = requests.get(url).json()

            price = float(r['lastPrice'])
            percent = float(r['priceChangePercent'])
            vol = float(r['quoteVolume']) / 1_000_000

            arrow = "🔺" if percent >= 0 else "🔻"
            result.append(f"{symbol.upper()}: {price:.5f} {arrow}{percent:.3f}% (Vol: {vol:.1f}M$)")

        except Exception:
            result.append(f"{symbol.upper()}: ❌ Veri alınamadı")

    return "\n".join(result)


def get_klines(symbol, interval="1h", limit=100):
    sym = symbol.upper() + "USDT"
    url = f"{BINANCE_URL}/api/v3/klines?symbol={sym}&interval={interval}&limit={limit}"
    r = requests.get(url).json()
    df = pd.DataFrame(r, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "num_trades",
        "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    return df


def calculate_indicators(df):
    close = df["close"]
    
    # RSI
    delta = close.diff()
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)
    avg_gain = pd.Series(gain).rolling(window=14).mean()
    avg_loss = pd.Series(loss).rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    
    # MACD
    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()

    return {
        "rsi": rsi.iloc[-1],
        "macd": macd.iloc[-1],
        "macd_signal": signal.iloc[-1]
    }

def get_detailed_analysis(symbols):
    result = []
    for symbol in symbols:
        try:
            df = get_klines(symbol, interval="1h", limit=100)
            indicators = calculate_indicators(df)

            rsi = indicators["rsi"]
            macd = indicators["macd"]
            signal = indicators["macd_signal"]
            trend = "📈 AL" if macd > signal and rsi > 50 else "📉 SAT" if macd < signal and rsi < 50 else "⏸ NÖTR"

            result.append(f"{symbol.upper()}: RSI={rsi:.1f}, MACD={macd:.3f}, Sinyal={signal:.3f} → {trend}")

        except Exception:
            result.append(f"{symbol.upper()}: ❌ Veri alınamadı")

    return "\n".join(result)
