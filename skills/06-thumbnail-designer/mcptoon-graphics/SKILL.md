---
name: mcptoon-graphics
description: Kapak ve video içi 2D çizgi film / illüstrasyon grafikleri — "explainer cartoon" stili (kalın kontur, düz renk, ifadeli karakterler), karakter sayfası ve tutarlılığı, sahne kompozisyonu; banner/kapak güvenli alanları için ui-ux-pro-max banner-design kılavuzu.
---

# mcptoon-graphics — 2D Çizgi Film ve İllüstrasyon Grafikleri

> **İsim notu:** Mimari belgesinde bu departman `mcptoon` aracıyla eşleştirilmişti. Ancak [activeing123/mcptoon](https://github.com/activeing123/mcptoon) bir MCP araç geçidi (token sıkıştırma CLI'ı) ve grafik üretmiyor. Departman adı korunmuştur; içerik çizgi film / illüstrasyon üretimi için yazılmıştır.
> Banner ve kapak boyutları/güvenli alanları: `upstream-banner-design.md` + `references/` ([nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill), MIT, değiştirilmeden kopyalandı).

## Hedef stil: "Explainer Cartoon"
- **Çizgi:** 4–6 px siyah kontur, hafif el çizimi titreşimi; iç detay çizgileri 2–3 px.
- **Renk:** düz dolgu + tek kademeli gölge; doygunluk orta. Gökyüzü açık mavi, zemin zeytin yeşili/toprak tonları.
- **Karakter:** büyük kafa (boy ≈ 4–5 kafa), iri göz, net ağız ifadesi; kostüm dönemine uygun ve sade.
- **Arka plan:** az detaylı, karakterlerden daha soluk; derinlik için 2–3 katman (zemin, orta plan, gökyüzü).
- **Anlatım öğeleri:** oklar, vurgu çizgileri, küçük ikonlar (anahtar, kese, sancak) hikâyeyi taşır.

## Üretim yolları (kalite sırasıyla)
1. **AI görsel + stil LoRA** (visual-pipeline 3. adım). Sabit stil promptu:
   `flat 2d cartoon illustration, thick black outlines, flat colors, simple shading, expressive characters, clean background, explainer video style`
   Negatif: `photorealistic, 3d render, gradient mesh, text, watermark, extra limbs, deformed hands`
2. **Kodla SVG çizim** (Remotion): aynı kontur/renk kurallarıyla; hızlı, tamamen tutarlı ama daha basit.
3. **Blender toon shader + Freestyle kontur**: 3D sahneyi çizgi film görünümünde render etmek (kamera hareketi gerekiyorsa).

## Karakter tutarlılığı (zorunlu)
1. Her ana karakter için **karakter sayfası**: ön / üç çeyrek / yan, 4 ifade (nötr, şaşkın, öfkeli, gülen) → `assets/characters/<ad>/`.
2. Pozlar `rembg` ile kesilir; sahneler bu cutout'larla kurulur (karakter her sahnede yeniden üretilmez).
3. Kostüm renkleri karakter başına sabittir (ör. acemi oğlanı: kırmızı kaftan; yeniçeri: beyaz börk + lacivert dolama).
4. Yaşlanma/terfi gibi değişimler aynı yüz üzerinde yeni kostümle gösterilir.

## Video içinde kullanım
- Sahne = arka plan katmanı + 1–3 karakter cutout + 1 anlatım öğesi (ok, ikon).
- Hareket: karakterlere hafif nefes/bob animasyonu, konuşma anında küçük ölçek vurgusu; kamera parallax.
- Her 3.2 sn'de bir değişim (smart_montage ritim planı).

## Kapakta kullanım
thumbnail-engine kurallarıyla: tek büyük ifadeli karakter + zıt renk arka plan + ≤ 4 kelime.
