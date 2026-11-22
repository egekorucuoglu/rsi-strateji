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

## Proje yapısı

| Dosya | Görevi |
|---|---|
| `strateji.py` | Veri çekme, RSI hesabı, pozisyon üretimi, backtest, grafik |
| `app.py` | Streamlit arayüzü |
| `requirements.txt` | Gerekli kütüphaneler |

## Örnek sonuç (BTC-USD, 2021'den bugüne, RSI 14, eşikler 30/70, komisyon %0,1)

| | Al-Bekle | RSI Stratejisi |
|---|---|---|
| Getiri | %106,4 | %-41,3 |
| Maksimum düşüş | %-76,6 | %-64,5 |

Bu sonuç, tek göstergeli basit bir RSI stratejisinin güçlü trend dönemlerinde işe yaramadığını gösteriyor.

## Sınırlamalar

- Sadece tek gösterge ve tek varlık
- Kayma (slippage) hesaba katılmıyor
- Eğitim/test ayrımı yok, aşırı uyum (overfitting) riski kontrol edilmedi
- Geçmiş performans geleceği garanti etmez

## Yol haritası

- [ ] Trend filtresi (200 günlük hareketli ortalama)
- [ ] Eğitim/test veri ayrımı
- [ ] Birden fazla gösterge (MACD, Bollinger)
- [ ] Makine öğrenmesi tabanlı sinyal modeli
- [ ] Streamlit Community Cloud ile yayınlama