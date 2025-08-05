# 📂 utils/stats.py
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests, coint
from statsmodels.tsa.api import VAR
from utils.binance_api import get_klines


# 🔹 Log getiri hesapla
def get_log_returns(symbol, limit=200):
    klines = get_klines(symbol, interval="1h", limit=limit)
    if not klines:
        return None
    prices = [float(k[4]) for k in klines]  # Kapanış fiyatları
    df = pd.DataFrame(prices, columns=["close"])
    df["log_return"] = np.log(df["close"] / df["close"].shift(1))
    df.dropna(inplace=True)
    return df["log_return"]


# 🔹 Coin log getirilerini hizala
def align_data(coins):
    data = {}
    for coin in coins:
        ret = get_log_returns(coin)
        if ret is not None:
            data[coin] = ret
    df = pd.DataFrame(data).dropna()
    return df if len(df.columns) >= 2 else None


# 1️⃣ Korelasyon Matrisi
def correlation_matrix(coins):
    df = align_data(coins)
    if df is None:
        return "Yeterli veri yok."
    corr = df.corr()
    return f"Korelasyon Matrisi:\n{corr.round(2).to_string()}"


# 2️⃣ Granger Nedensellik (tek yön)
# coin1 → coin2 nedenselliği test edilir
def granger_test(coin1, coin2, maxlag=5):
    df = align_data([coin1, coin2])
    if df is None:
        return "Yeterli veri yok."
    try:
        test_result = grangercausalitytests(df[[coin2, coin1]], maxlag=maxlag, verbose=False)
        p_values = [round(test_result[i + 1][0]['ssr_chi2test'][1], 4) for i in range(maxlag)]
        min_p = min(p_values)
        conclusion = f"{coin1} → {coin2} için en düşük p-değeri: {min_p}"
        if min_p < 0.05:
            conclusion += "\n📊 Granger Nedensellik VAR."
        else:
            conclusion += "\nℹ️ Nedensellik bulunamadı."
        return conclusion
    except Exception as e:
        return f"Hata (Granger): {str(e)}"


# 3️⃣ Granger Nedensellik Matrisi
def granger_matrix(coins, maxlag=5):
    df = align_data(coins)
    if df is None:
        return "Yeterli veri yok."
    results = {}
    for cause in coins:
        row = {}
        for effect in coins:
            if cause == effect:
                row[effect] = "-"
                continue
            try:
                test_result = grangercausalitytests(df[[effect, cause]], maxlag=maxlag, verbose=False)
                p_values = [test_result[i + 1][0]['ssr_chi2test'][1] for i in range(maxlag)]
                row[effect] = round(min(p_values), 3)
            except Exception:
                row[effect] = "ERR"
        results[cause] = row
    matrix = pd.DataFrame(results).T
    return f"Granger Nedensellik Matrisi (p-değerleri):\n{matrix.to_string()}"


# 4️⃣ Cointegration Matrisi
def cointegration_matrix(coins):
    df = align_data(coins)
    if df is None:
        return "Yeterli veri yok."
    matrix = pd.DataFrame(index=coins, columns=coins)
    for i in coins:
        for j in coins:
            if i == j:
                matrix.loc[i, j] = "-"
            else:
                try:
                    score, pval, _ = coint(df[i], df[j])
                    matrix.loc[i, j] = round(pval, 3)
                except Exception:
                    matrix.loc[i, j] = "ERR"
    return f"Cointegration Matrisi (p-değerleri):\n{matrix.to_string()}"


# 5️⃣ VAR Tahmin Matrisi
def var_matrix(coins):
    df = align_data(coins)
    if df is None:
        return "Yeterli veri yok."
    try:
        if df.shape[0] < 30:
            return "VAR modeli için yeterli veri yok (min 30 satır önerilir)."
        model = VAR(df)
        results = model.fit(maxlags=5, ic='aic')
        forecast = results.forecast(df.values[-results.k_ar:], steps=1)
        pred = pd.DataFrame(forecast, columns=df.columns)
        return f"VAR Modeli Tahmini (1 adım sonrası):\n{pred.round(4).to_string(index=False)}"
    except Exception as e:
        return f"Hata (VAR Modeli kurulamadı): {str(e)}"


# 6️⃣ Liderlik Skoru Matrisi
def leader_matrix(coins):
    df = align_data(coins)
    if df is None:
        return "Yeterli veri yok."
    lead_scores = {}
    for lead in coins:
        score = 0
        for lag in coins:
            if lead == lag:
                continue
            shifted = df[lead].shift(1).corr(df[lag])
            score += shifted if pd.notna(shifted) else 0
        lead_scores[lead] = round(score, 3)
    lead_sorted = dict(sorted(lead_scores.items(), key=lambda x: x[1], reverse=True))
    msg = "\n".join([f"{k}: {v}" for k, v in lead_sorted.items()])
    return f"Liderlik Skorları (yüksek = lider olma olasılığı):\n{msg}"
    
