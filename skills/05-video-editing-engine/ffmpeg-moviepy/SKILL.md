---
name: ffmpeg-moviepy
description: FFmpeg ile hızlı kurgu ve Smart Montage — sessizlik kırpma (jump-cut), kelime zamanlarını yeniden eşleme, cümle→B-roll türü eşleme, 3.2 sn ritim planı ve donuk sahne denetimi. Kod pipeline/smart_montage.py.
---

# FFmpeg / Smart Montage

calesthio/openmontage (AGPL-3.0) **fikirlerinden esinlenilerek sıfırdan yazıldı**; lisans nedeniyle kod kopyalanmadı.

## Komutlar
```bash
python pipeline/smart_montage.py silences output/voiceover.mp3         # sessiz aralıklar
python pipeline/smart_montage.py jumpcut  output/voiceover.mp3 out.mp3  # kırpılmış ses + rapor
python pipeline/smart_montage.py broll    output/script.txt            # cümle → B-roll türü
python pipeline/smart_montage.py static   output/final.mp4 --max 4     # donuk kalan bölümler
```

## Kurallar
- Sessizlik: −35 dB altı, ≥ 0.35 sn. Kırpmada her uçta 0.12 sn nefes payı.
- **Jump-cut sonrası kelime zamanları `remap_words(words, segments)` ile yeniden hesaplanır**, yoksa altyazı kayar.
- Belgesel anlatımda jump-cut opsiyoneldir (`main.py --jumpcut`); dramatik duraklamalar bilinçli olabilir.
- B-roll türleri: `timeline`, `stat_card`, `map`, `diagram`, `code`, `quote_card`, `illustration` (visual-pipeline kaynak seçimini buna göre yapar).
- Ritim: hiçbir plan 3.2 sn'den uzun statik kalmaz → `cut`, `punch_in`, `pan`, `overlay`.
- Yayın öncesi `detect_static` ile 4 sn'den uzun donuk bölüm kalmadığı doğrulanır.
- MoviePy yalnızca Python içinden basit birleştirme için; ağır işler FFmpeg CLI ile.
