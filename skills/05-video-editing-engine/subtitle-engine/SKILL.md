---
name: subtitle-engine
description: Kelime bazlı zamanlamayla dinamik (karaoke) altyazı üretir. Edge-TTS WordBoundary veya faster-whisper zaman damgalarını kullanır; Remotion bileşeni ve .srt çıktısı.
---

# Subtitle Engine

## Zamanlama kaynağı
- **Edge-TTS sesi:** `boundary="WordBoundary"` birebir doğrudur (`voice_engine.generate_tts`). OpenVoice dönüştürmesi süreyi değiştirmez.
- **Dış kayıt:** `faster-whisper`, Türkçe için en az `small` model.
- Jump-cut yapıldıysa zamanlar `smart_montage.remap_words` ile güncellenir.

## Gruplama
- Satır başına 3–8 kelime; noktalama veya > 0.35 sn boşlukta kırılır.
- Konuşulan kelime vurgu rengiyle, henüz söylenmeyenler %55 opaklık.
- Güvenli alan: alttan ≥ 70 px, yanlardan ≥ 160 px; satır ≤ 42 karakter (Türkçe uzun kelimeler).
- Altyazı ekran grafiğiyle çakışmaz: grafikler alt %20'ye inmez.

## Çıktılar
- Remotion altyazı bileşeni (`MainVideo.tsx` kelime vurgusu).
- `.srt` — YouTube'a ayrı altyazı parçası olarak yüklenir (erişilebilirlik + SEO).
