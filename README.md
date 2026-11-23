# RSI Strateji Backtest Aracı

Python ve Streamlit ile yazılmış, RSI (Relative Strength Index) göstergesine dayalı bir al-sat stratejisini geçmiş fiyat verisi üzerinde test eden basit bir prototiptir.

> **Uyarı:** Bu proje eğitim ve araştırma amaçlıdır. Yatırım tavsiyesi değildir.

## Ne yapar?

- Yahoo Finance'ten günlük kapanış fiyatlarını çeker (kripto, hisse, döviz)
- RSI hesaplar
- Kural: RSI alt eşiğin altına inerse AL, üst eşiğin üstüne çıkarsa SAT
- Stratejiyi "al ve bekle" ile karşılaştırır
- Toplam getiri, maksimum düşüş (drawdown) ve işlem sayısını gösterir
- Fiyat grafiği üzerinde AL/SAT noktalarını çizer

## Ayarlanabilir parametreler

- Varlık (BTC-USD, ETH-USD, THYAO.IS, AAPL, EURUSD=X)
- Başlangıç tarihi
- RSI periyodu
- AL / SAT eşikleri
- İşlem başına komisyon

## Kurulum

```
git clone https://github.com/egekorucuoglu/rsi-strateji.git
cd rsi-strateji
pip install -r requirements.txt
python -m streamlit run app.py
```
