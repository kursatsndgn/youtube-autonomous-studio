---
name: voice-and-sync
description: Orchestrates high-fidelity voice generation via OpenVoice/Edge-TTS and extracts millisecond-accurate word-level timestamps using Faster-Whisper for dynamic subtitles.
tools: [run_command, read_file, write_file]
---

# Voice Generation & Millisecond Alignment Skill

Bu beceri, **myshell-ai/OpenVoice** ses klonlama / TTS motorunu ve **SYSTRAN/faster-whisper** transkripsiyon motorunu kullanarak insan doğallığında seslendirme ve kelime kelime senkronize altyazı verisi üretir.

## 1. Seslendirme Prensipleri (OpenVoice TTS)

1. **Ses Tonu ve Enerji Uyumu:**
   - Script'in duygu durumuna göre tonlama (Heyecanlı, ciddi, meraklı, samimi).
   - Sabit tekdüze (monotone) robot sesinden kaçınmak için cümle aralarında doğal duraklamalar (`[pause: 200ms]`) bırakılır.
2. **Telaffuz Kontrolü:**
   - İngilizce teknik terimler (API, Framework, Python, Docker) için fonetik düzeltmeler yapılır.

## 2. Faster-Whisper ile Kelime Bazlı Hizalama (Word-Level Timestamps)

Ses dosyası (`audio.wav`) oluşturulduktan sonra, Faster-Whisper modeli çalıştırılarak her kelimenin tam başlama ve bitiş anı saniye cinsinden çıkarılır:

```python
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cuda", compute_type="float16")
segments, info = model.transcribe("output/voiceover.wav", word_timestamps=True)

words_data = []
for segment in segments:
    for word in segment.words:
        words_data.append({
            "word": word.word.strip(),
            "start": round(word.start, 2),
            "end": round(word.end, 2),
            "probability": round(word.probability, 2)
        })
```

## 3. Remotion İçin Senkronizasyon Verisi

Çıkan `words_data` JSON dosyası doğrudan Remotion kurgu motoruna aktarılır. Böylece ekranda konuşulan kelime parladığında (karaoke efekti) ya da ekrana fırladığında %100 dudak/ses senkronizasyonu sağlanır.
