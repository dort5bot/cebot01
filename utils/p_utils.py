##p_utils.py
##
# utils/p_utils.py
from utils.binance_api import get_klines
import numpy as np

def generate_price_delta_analysis(symbol: str) -> str:
    klines = get_klines(symbol, interval="1m", limit=15)
    if not klines or len(klines) < 2:
        return "Yeterli veri alınamadı."

    closes = [float(k[4]) for k in klines]
    volumes = [float(k[5]) for k in klines]

    deltas = np.diff(closes)
    momentum = np.sum(deltas[-5:])  # son 5 dakikalık değişim toplamı
    avg_delta = np.mean(deltas)
    max_delta = np.max(np.abs(deltas))
    volatility = np.std(closes)
    vol_change = volumes[-1] / max(volumes[:-1]) if max(volumes[:-1]) > 0 else 0

    trend = "🔼 Yükseliş" if momentum > 0 else "🔽 Düşüş" if momentum < 0 else "➡️ Yatay"

    text = f"""📊 <b>Fiyat Delta-Momentum Analizi</b> ({symbol})

• Son 5dk Momentum: <b>{momentum:.4f}</b>
• Ortalama Delta: <b>{avg_delta:.5f}</b>
• Maksimum Delta: <b>{max_delta:.5f}</b>
• Fiyat Volatilitesi: <b>{volatility:.5f}</b>
• Hacim Değişimi (son): <b>{vol_change:.2f}x</b>
• Trend: <b>{trend}</b>
"""
    return text
