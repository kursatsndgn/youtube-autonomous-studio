# Retention & Pacing (script-engine referansı)

> Eski `adhd-pacing-hook` skill'inden taşındı. Ölçüm kodu: `pipeline/smart_montage.py` (ritim planı, donuk sahne).


Bu beceri, izleyici tutma prensiplerini uygulayarak YouTube algoritmasının en çok ödüllendirdiği metrik olan **Average View Duration (İzlenme Süresi)** ve **Audience Retention** grafiğini maksimize eder.

## 1. 3 Saniye Kancası (The 3-Second Hook Rule)

İzleyicinin parmağını kaydırmasını (veya videodan çıkmasını) engellemek için ilk 3 saniyede 3 unsur aynı anda devreye girmelidir:
1. **Görsel Şok / Pattern Interrupt:** Beklenmeyen bir hareket, hızlı zoom veya çarpıcı bir zıtlık.
2. **Kelimeler (Auditory Trigger):** Yüksek enerji, ilk kelimeden itibaren soru işareti veya çelişki.
3. **Ekranda Büyük Metin (Kinetic Hook):** Maksimum 3-4 kelimelik, merak uyandıran büyük altyazı.

*Kural:* İlk 10 saniyede intro jeneriği, kanal logosu, abone ol çağrısı KESİNLİKLE YASAKTIR.

## 2. Dopamin & Pacing Döngüsü (ADHD Timing Architecture)

İzleyicinin beyni her 4-6 saniyede bir yeni bir uyarana ihtiyaç duyar:
- **Görsel Değişim Sıklığı:** Statik bir görsel asla 3.5 saniyeden uzun ekranda kalamaz!
- **Kurgu Teknikleri:**
  - **Punch-in Zoom:** Önemli bir kelime söylendiğinde kameranın %115 yaklaşması.
  - **B-Roll / Sticker Geçişi:** rembg ile çıkarılmış şeffaf PNG ikonlarının veya illüstrasyonların pop-up sesiyle belirmesi.
  - **Sound Effects (SFX):** Whoosh, pop, daktilo, glitch sesleriyle görsel hareketlerin senkronize edilmesi.
  - **Open Loops (Merak Döngüleri):** Bir konuyu anlatırken "birazdan göreceğiniz sürpriz hata hariç..." diyerek cevabı 2 dakika sonraya erteleme.

## 3. Replica Engine (Rakip Stilini Klonlama)

Hedef kanal stili (örneğin Ali Abdaal, MrBeast, Veritasium veya fireship tarzı):
- **Tempo Ölçümü:** Dakikadaki kelime sayısı (WPM: Words Per Minute) hedef kitleye göre ayarlanır:
  - Bilgi yoğun / Tutorial: 140 - 155 WPM
  - Hızlı tempolu / Shorts / Tech-news: 165 - 185 WPM
- **Duygu Grafiği:** Senaryoyu monotonluktan kurtarmak için gerilim dalgalanmaları (Sorun -> Hayal kırıklığı -> Keşif -> Zafer) oluşturulur.
