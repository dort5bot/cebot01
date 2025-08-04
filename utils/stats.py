# 📂 utils/stats.py
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import grangercausalitytests, coint
from statsmodels.tsa.api import VAR
from utils.binance_api import get_klines

def get_price_series(symbol, limit=100):
    klines = get_klines(symbol, interval="1h", limit=limit)
    if not klines:
        return None
    closes = [float(k[4]) for k in klines]
    return pd.Series(closes, name=symbol)

def align_data(coins):
    data = {}
    for coin in coins:
        series = get_price_series(f"{coin}USDT")
        if series is not None:
            data[coin] = series.reset_index(drop=True)
    return pd.DataFrame(data).dropna()

# Korelasyon Matrisi
def correlation_matrix(coins):
    df = align_data(coins)
    if df.empty:
        return "Veri alınamadı."
    corr = df.corr().round(3)
    return f"📊 Korelasyon Matrisi:\n{corr.to_string()}"

# Granger Nedensellik
def granger_test(coin1, coin2, maxlag=5):
    df = align_data([coin1, coin2])
    if df.shape[1] != 2:
        return "Veriler eksik."
    try:
        test = grangercausalitytests(df[[coin2, coin1]], maxlag=maxlag, verbose=False)
        pvals = [round(test[i+1][0]['ssr_ftest'][1], 4) for i in range(maxlag)]
        return f"📈 Granger Testi ({coin1} -> {coin2}):\nP-değerleri: {pvals}"
    except Exception as e:
        return f"Hata: {e}"

def granger_matrix(coins, maxlag=5):
    df = align_data(coins)
    if df.empty:
        return "Veri alınamadı."
    result = "📈 Granger Nedensellik Matrisi (P-Değeri):\n"
    matrix = pd.DataFrame(index=coins, columns=coins)

    for c1 in coins:
        for c2 in coins:
            if c1 == c2:
                matrix.loc[c1, c2] = "-"
            else:
                try:
                    test = grangercausalitytests(df[[c2, c1]], maxlag=maxlag, verbose=False)
                    pval = test[maxlag][0]['ssr_ftest'][1]
                    matrix.loc[c1, c2] = round(pval, 3)
                except:
                    matrix.loc[c1, c2] = "err"

    return result + matrix.to_string()

# Cointegration Matrisi
def cointegration_matrix(coins):
    df = align_data(coins)
    result = "🔗 Cointegration Matrisi:\n"
    matrix = pd.DataFrame(index=coins, columns=coins)
    for i in coins:
        for j in coins:
            if i == j:
                matrix.loc[i, j] = "-"
            else:
                try:
                    score, pval, _ = coint(df[i], df[j])
                    matrix.loc[i, j] = round(pval, 3)
                except:
                    matrix.loc[i, j] = "err"
    return result + matrix.to_string()

# VAR Matrisi
def var_matrix(coins):
    df = align_data(coins)
    if df.empty:
        return "Veri alınamadı."
    model = VAR(df)
    try:
        result = model.fit(maxlags=5, ic='aic')
        summary = result.summary()
        return f"🧠 VAR Model Özeti:\n{summary}"
    except Exception as e:
        return f"VAR Modeli kurulamadı: {e}"

# Lider/Takipçi
def leader_matrix(coins):
    df = align_data(coins)
    if df.empty:
        return "Veri alınamadı."
    lags = {}
    for coin in coins:
        others = df.drop(columns=[coin])
        try:
            model = VAR(pd.concat([df[coin], others], axis=1))
            res = model.fit(maxlags=5, ic='aic')
            lag = res.k_ar
            lags[coin] = lag
        except:
            lags[coin] = "err"
    return "🚩 Liderlik Skoru (lag sayısı):\n" + "\n".join(f"{k}: {v}" for k, v in lags.items())
