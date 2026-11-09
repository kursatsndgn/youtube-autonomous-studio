---
name: voice-pipeline
description: Senaryoyu seslendirir. Türkçe metin Edge-TTS ile üretilir, isteğe bağlı olarak OpenVoice V2 ton rengi dönüştürücüsüyle kanalın kendi sesine klonlanır; kelime zamanları Edge-TTS WordBoundary veya faster-whisper ile çıkarılır. Kod pipeline/voice_engine.py.
---

# Voice Pipeline (Edge-TTS + OpenVoice + faster-whisper)

## Mimari
```
metin ──▶ Edge-TTS (tr-TR-AhmetNeural / EmelNeural) ──▶ base.wav + kelime zamanları (WordBoundary)
                                                         │
                         referans ses (10–30 sn, temiz) ─┤
                                                         ▼
                              OpenVoice V2 ToneColorConverter ──▶ voiceover.wav (kanalın sesi)
```

### Neden bu sıra?
**OpenVoice V2 Türkçe konuşma üretmez** (yerel diller: EN, ES, FR, ZH, JA, KO; temel TTS'i MeloTTS'te Türkçe yok).
Ancak **ton rengi dönüştürücüsü dilden bağımsızdır**: Edge-TTS'in ürettiği Türkçe sesi, referans kaydın tınısına dönüştürür. Böylece doğal Türkçe telaffuz + kanala özgü, tutarlı ses elde edilir.
Dönüştürme süreyi değiştirmez, bu yüzden Edge-TTS'ten alınan kelime zamanları geçerli kalır.

## OpenVoice kurulumu (bir kez)
Kaynak: [myshell-ai/OpenVoice](https://github.com/myshell-ai/OpenVoice) (MIT, V1 ve V2 ticari kullanıma açık).
```bash
git clone https://github.com/myshell-ai/OpenVoice vendor/OpenVoice
pip install -e vendor/OpenVoice
# V2 checkpoint'leri: upstream README'deki "checkpoints_v2" zip'i → vendor/OpenVoice/checkpoints_v2/
```
- `config/voice/reference.wav`: kanalın sesi. 10–30 sn, tek konuşmacı, müziksiz, gürültüsüz. **Yalnızca izni alınmış bir sesi klonla.**
- GPU (GTX 1650 Ti, 4 GB) yeterli; CPU'da da çalışır, daha yavaş.

## Kullanım
```python
engine = VoiceEngine(voice="tr-TR-AhmetNeural", rate="-4%")
await engine.generate_tts(text, "output/base.mp3")            # + output/word_alignment.json
engine.clone_tone("output/base.mp3", "output/voiceover.wav")  # OpenVoice; kurulu değilse hata verir
```
`main.py --clone-voice` bayrağı dönüştürmeyi açar. Kurulum veya referans ses yoksa pipeline **durur**; sessizce sahte ses üretmez.

## Seslendirme kuralları
- Belgesel tempo: Edge-TTS `rate` −4% ile +5% arası, hedef 140–155 kelime/dk.
- Cümle sonu doğal duraklama; dramatik anlarda paragraf arası boşluk bırakılır (jump-cut kapalıysa korunur).
- Yabancı ve eski Türkçe terimler (ulufe, Vaka-i Hayriye) seslendirmeden önce dinlenerek kontrol edilir; gerekirse fonetik yazımla düzeltilir.

## Kelime zamanları
- **Edge-TTS sesi:** `boundary="WordBoundary"` → birebir doğru, Whisper gerekmez.
- **Dış kayıt / insan sesi:** `faster-whisper`, Türkçe için en az `small` model, `word_timestamps=True`.
- Çıktı biçimi `{"w","s","e"}` (subtitle-engine ve smart_montage ile ortak).
