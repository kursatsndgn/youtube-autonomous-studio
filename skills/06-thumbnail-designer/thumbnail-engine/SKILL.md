---
name: thumbnail-engine
description: Yüksek CTR'lı YouTube kapağı (1280×720) üretir — rembg ile figür kesme, Pillow/opencv ile kontrast, kontur ve metin yerleşimi; 2–3 varyant.
---

# Thumbnail Engine

## Kompozisyon
- En fazla **3 öğe**: odak figür (rembg cutout) + zıt renkli grafik + ≤ 4 kelimelik dev metin.
- Sağ alt köşe (~180×60 px) boş — YouTube süre rozeti.
- %15 boyutta (~190 px genişlik) okunabilir olmalı: metin yüksekliği ≥ görsel yüksekliğinin %18'i.
- Figüre 6–10 px açık kontur + hafif dış gölge.
- Başlıkla aynı cümleyi tekrarlama; kapak, başlığın eksik bıraktığı merakı tamamlar.

## Akış
1. Kaynak: video karesi, stok veya AI görsel (visual-pipeline).
2. `rembg` ile odak figürü kes.
3. Arka plan: bulanıklaştır + koyulaştır, ya da düz vurgu rengi (taste-design 60-30-10 paleti).
4. Metin: kalın sans-serif, beyaz + tek vurgulu kelime, sol üçte ikide.
5. `output/<slug>/thumbnail_{a,b,c}.jpg`, 1280×720, < 2 MB.
6. Seçim: kanal hafızasındaki CTR geçmişine göre; YouTube "Test & Compare" ile A/B.

Banner güvenli alanları ve stil kataloğu: `ui-ux-graphics/references/banner-sizes-and-styles.md`.
