##
###etf için dosya 
import pandas as pd
import os

FILE = "data/etf_history.csv"

def load_etf_data():
    if not os.path.exists(FILE):
        return pd.DataFrame()
    return pd.read_csv(FILE)

def save_etf_entry(entry: dict):
    df = load_etf_data()
    df = df.append(entry, ignore_index=True)

    # Sadece son 60 kayıt tut
    if len(df) > 60:
        df = df.iloc[-60:]

    df.to_csv(FILE, index=False)
