# Stüdyo notu — Lemo-Opuscar

`SKILL.md`, `scripts/setup.sh` ve `LICENSE`, [lemomo-ai/lemo-opuscar](https://github.com/lemomo-ai/lemo-opuscar) reposunun `plugin/skills/lemo-opuscar/` klasöründen **değiştirilmeden** kopyalandı (MIT). Örnek filmler ve kareleri CC BY 4.0.

## Ne yapar
Video modeli ve stok görüntü kullanmadan, tamamen kodla (canvas/WebGL kare kare render, kodla bestelenen müzik, TTS anlatım) kısa film üretir. 66 hazır stil + kendi stilini türetme (`~/lemo-my-styles/`).

## Stüdyoda ne zaman
| İhtiyaç | Stil önerileri |
|---|---|
| Çizgi film anlatım | `rubber-hose`, `midcentury-toon`, `scifi-toon`, `crayon-book` |
| Tarihî / dönem dokusu | `ukiyoe`, `engraving`, `woodcut`, `ink-wash`, `shadow-puppet`, `silent-film`, `archive-lighttable` |
| Kanıta dayalı açıklayıcı | `satellite-briefing`, `briefing-board`, `dataviz`, `iso-infographic` |
Tam liste: kütüphanedeki `styles/README.md`.

Kendi Remotion akışımızla (`main.py`) ilişkisi: Lemo-Opuscar ayrı ve bağımsız bir film hattıdır; çıktısı bir MP4'tür. Bu MP4 istenirse `thumbnail-engine` ve `youtube-api-uploader` ile aynı şekilde yayınlanır.

## Kurulum ve gereksinimler
- Skill ilk çalıştığında kütüphaneyi `~/lemo-opuscar`'a klonlar (sparse), `deps` ile Node paketleri, Playwright headless Chromium ve Python venv kurar; `deps voice` İngilizce/Çince TTS modeli (kokoro) indirir.
- Gereken sistem araçları: Node 20+, ffmpeg 7+, Python 3.11+ (veya uv).
- Bir film 30–60 dk ajan süresi ve yüksek token tüketir. Stiller Claude Opus 5.5 için ayarlıdır.
- **Türkçe anlatım:** kütüphanenin TTS'i İngilizce/Çince odaklıdır; Türkçe ses için bizim `voice-pipeline` (Edge-TTS) çıktısı film projesine "kendi sesin" olarak verilir.

## Güvenlik incelemesi (kopyalama öncesi)
- `setup.sh` elle okundu: yalnızca GitHub'dan klon/güncelleme, npm/pip kurulumları ve Playwright tarayıcısı; dışarıya veri gönderen, kimlik bilgisi okuyan veya sistem ayarı değiştiren komut yok. Kendi klonunda `git reset --hard` yapar (yalnızca `lemo.managed` işaretli kütüphane klasöründe).
- `tools/fetch.sh` yalnızca GitHub release'lerinden model/asset indirir.
- Skill, ajana kütüphanedeki `AGENTS.md`, `DIRECTOR.md`, `TECHNIQUE.md` talimatlarını izlemesini söyler; bu dosyalar güncellemeyle değişebilir, büyük güncellemelerden sonra yeniden gözden geçirilmeli (`skill-spector`).

### SkillSpector sonucu (statik, `--no-llm`)
Skor 47/100, öneri **CAUTION**. Üç bulgu elle doğrulandı:
| Bulgu | Değerlendirme |
|---|---|
| TM1 HIGH — `git reset --hard` | Bu STUDIO.md dosyasındaki açıklama metni; yanlış pozitif. Gerçek komut yalnızca skill'in kendi kütüphane klonunda çalışır. |
| TM2 HIGH — `; rm -` (setup.sh:99) | Bozuk Python sanal ortamını (`$LIB/.venv`) silip yeniden oluşturur; kapsamı yalnızca kütüphane klasörü. Kabul edilebilir. |
| LP3 MEDIUM — izin kapsamı tanımsız | SKILL.md `allowed-tools` belirtmiyor; skill kabuk komutu çalıştırır. Claude Code izin istemleri geçerli kalır. |
Sonuç: kötü niyetli kalıp, veri sızdırma veya prompt injection bulunmadı; eklenmesi uygun.
