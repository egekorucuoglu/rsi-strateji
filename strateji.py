import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def veri_cek(sembol, baslangic):
    """Yahoo Finance'ten kapanış fiyatlarını çeker."""
    df = yf.download(sembol, start=baslangic, auto_adjust=True, progress=False)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df[["Close"]].dropna()


def rsi_hesapla(fiyat, periyot=14):
    """RSI hesaplar (0-100 arası bir seri döndürür)."""
    fark = fiyat.diff()
    kazanc = fark.clip(lower=0)
    kayip = -fark.clip(upper=0)
    ort_kazanc = kazanc.ewm(alpha=1 / periyot, adjust=False).mean()
    ort_kayip = kayip.ewm(alpha=1 / periyot, adjust=False).mean()
    rs = ort_kazanc / ort_kayip
    return 100 - (100 / (1 + rs))


def pozisyon_uret(rsi, alt_esik, ust_esik):
    """RSI < alt_esik ise AL (1), RSI > ust_esik ise SAT (0), arada eski durum korunur."""
    pozisyon = []
    icerde = 0
    for deger in rsi:
        if deger < alt_esik:
            icerde = 1
        elif deger > ust_esik:
            icerde = 0
        pozisyon.append(icerde)
    return pd.Series(pozisyon, index=rsi.index)


def max_dusus(egri):
    """Zirveden en dip noktaya en büyük düşüş oranı."""
    return (egri / egri.cummax() - 1).min()


def backtest_yap(df, periyot=14, alt_esik=30, ust_esik=70, komisyon=0.001):
    """Stratejiyi geçmiş veride çalıştırır, sonuç tablosunu ve özet metrikleri döndürür."""
    df = df.copy()
    df["RSI"] = rsi_hesapla(df["Close"], periyot)
    df["Pozisyon"] = pozisyon_uret(df["RSI"], alt_esik, ust_esik)

    df["Getiri"] = df["Close"].pct_change().fillna(0)
    poz = df["Pozisyon"].shift(1).fillna(0)       # dünkü karar bugün uygulanır
    islem = poz.diff().abs().fillna(0)            # pozisyon değiştiyse işlem yapılmış demektir
    df["Strateji"] = df["Getiri"] * poz - islem * komisyon

    df["BuyHold_Egri"] = (1 + df["Getiri"]).cumprod()
    df["Strateji_Egri"] = (1 + df["Strateji"]).cumprod()

    ozet = {
        "buyhold_getiri": df["BuyHold_Egri"].iloc[-1] - 1,
        "strateji_getiri": df["Strateji_Egri"].iloc[-1] - 1,
        "buyhold_dusus": max_dusus(df["BuyHold_Egri"]),
        "strateji_dusus": max_dusus(df["Strateji_Egri"]),
        "islem_sayisi": int(islem.sum()),
    }
    return df, ozet


def grafik_ciz(df, sembol):
    """Fiyat + AL/SAT noktaları ve büyüme eğrilerini çizer."""
    fig, (ust, alt) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)

    ust.plot(df.index, df["Close"], label="Fiyat", color="gray")
    al = df[df["Pozisyon"].diff() == 1]
    sat = df[df["Pozisyon"].diff() == -1]
    ust.scatter(al.index, al["Close"], marker="^", color="green", s=100, label="AL")
    ust.scatter(sat.index, sat["Close"], marker="v", color="red", s=100, label="SAT")
    ust.set_title(f"{sembol} RSI Stratejisi")
    ust.legend()

    alt.plot(df.index, df["BuyHold_Egri"], label="Al-Bekle")
    alt.plot(df.index, df["Strateji_Egri"], label="RSI Stratejisi")
    alt.set_title("Büyüme Eğrisi (1 birim ile başlangıç)")
    alt.legend()

    plt.tight_layout()
    return fig