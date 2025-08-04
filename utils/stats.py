##stats.py (granler)

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests, coint
from statsmodels.tsa.api import VAR
from utils.binance_api import get_ohlcv_multiple

def granger_test(coin1, coin2, lag=2):
    df = get_ohlcv_multiple([coin1, coin2])
    data = df[[coin1, coin2]].dropna()
    try:
        test = grangercausalitytests(data[[coin1, coin2]], maxlag=lag, verbose=False)
        p_value = test[lag][0]['ssr_ftest'][1]
        result = f"{coin1} -> {coin2} Granger Nedensellik p-değeri: {p_value:.4f}"
        if p_value < 0.05:
            result += " ✅ Nedensellik VAR"
        else:
            result += " ❌ Nedensellik YOK"
        return result
    except Exception as e:
        return f"Hata: {str(e)}"

def granger_matrix(coins):
    df = get_ohlcv_multiple(coins)
    matrix = ""
    for i in coins:
        row = []
        for j in coins:
            if i == j:
                row.append(" - ")
            else:
                try:
                    p = grangercausalitytests(df[[i, j]].dropna(), maxlag=2, verbose=False)[2][0]['ssr_ftest'][1]
                    row.append(f"{p:.2f}")
                except:
                    row.append("Err")
        matrix += f"{i}: {' | '.join(row)}\n"
    return f"📊 Granger Nedensellik Matrisi:\n{matrix}"

def correlation_matrix(coins):
    df = get_ohlcv_multiple(coins)
    corr = df.corr().round(2)
    return f"📈 Korelasyon Matrisi:\n{corr.to_string()}"

def cointegration_matrix(coins):
    df = get_ohlcv_multiple(coins)
    result = "🔗 Cointegration Matrisi:\n"
    for i in range(len(coins)):
        for j in range(i+1, len(coins)):
            try:
                score, pvalue, _ = coint(df[coins[i]], df[coins[j]])
                result += f"{coins[i]} - {coins[j]}: p={pvalue:.4f} {'✅' if pvalue < 0.05 else '❌'}\n"
            except:
                result += f"{coins[i]} - {coins[j]}: Hata\n"
    return result

def var_matrix(coins):
    df = get_ohlcv_multiple(coins)
    model = VAR(df.dropna())
    try:
        result = model.fit(maxlags=2)
        forecast = result.forecast(df.values[-result.k_ar:], steps=1)
        out = pd.DataFrame(forecast, columns=df.columns)
        return f"📉 VAR Tahmini (1 adım):\n{out.round(3).to_string(index=False)}"
    except Exception as e:
        return f"VAR modeli hatası: {str(e)}"

def leader_matrix(coins):
    df = get_ohlcv_multiple(coins)
    leaders = []
    for i in coins:
        row = []
        for j in coins:
            if i == j:
                row.append(" - ")
            else:
                try:
                    p = grangercausalitytests(df[[i, j]].dropna(), maxlag=2, verbose=False)[2][0]['ssr_ftest'][1]
                    row.append("✔" if p < 0.05 else "✖")
                except:
                    row.append("?")
        leaders.append(f"{i}: {' '.join(row)}")
    return "📍 Lider/Takipçi Matrisi:\n" + "\n".join(leaders)
