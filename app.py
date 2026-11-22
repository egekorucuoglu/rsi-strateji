import streamlit as st
from strateji import veri_cek, backtest_yap, grafik_ciz

st.set_page_config(page_title="RSI Strateji Testi", layout="wide")
st.title("RSI Strateji Backtest Aracı")
st.caption("Eğitim/prototip amaçlıdır, yatırım tavsiyesi değildir.")

st.sidebar.header("Ayarlar")
sembol = st.sidebar.selectbox("Varlık", ["BTC-USD", "ETH-USD", "THYAO.IS", "AAPL", "EURUSD=X"])
baslangic = st.sidebar.date_input("Başlangıç tarihi", value=None) or "2021-01-01"
periyot = st.sidebar.slider("RSI periyodu", 5, 30, 14)
alt_esik = st.sidebar.slider("AL eşiği (RSI altına inerse)", 10, 50, 30)
ust_esik = st.sidebar.slider("SAT eşiği (RSI üstüne çıkarsa)", 50, 90, 70)
komisyon = st.sidebar.number_input("Komisyon (işlem başına, %)", 0.0, 2.0, 0.1) / 100


@st.cache_data
def veri_getir(sembol, baslangic):
    return veri_cek(sembol, str(baslangic))


if st.sidebar.button("Backtest çalıştır", type="primary"):
    df = veri_getir(sembol, baslangic)
    if df.empty:
        st.error("Veri çekilemedi. Sembolü veya tarihi kontrol edin.")
    else:
        sonuc, ozet = backtest_yap(df, periyot, alt_esik, ust_esik, komisyon)

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Al-Bekle getirisi", f"%{ozet['buyhold_getiri'] * 100:.1f}")
        k2.metric("Strateji getirisi", f"%{ozet['strateji_getiri'] * 100:.1f}")
        k3.metric("Al-Bekle max düşüş", f"%{ozet['buyhold_dusus'] * 100:.1f}")
        k4.metric("Strateji max düşüş", f"%{ozet['strateji_dusus'] * 100:.1f}")
        st.write(f"Toplam işlem sayısı: **{ozet['islem_sayisi']}**")

        st.pyplot(grafik_ciz(sonuc, sembol))
else:
    st.info("Soldaki ayarları seçip **Backtest çalıştır** butonuna basın.")