---
name: visual-pipeline
description: Sahne görsellerini toplar veya üretir. Öncelik sırası stok (Pexels/Pixabay) → kodla çizim (Remotion SVG) → AI görsel (ComfyUI/diffusers) → AnimateDiff. Hiçbir kaynak sonuç vermezse sahte görsel üretmez, durur.
---

# Visual Pipeline

## Kaynak seçimi (sahne başına)
`smart_montage.classify_broll` her cümleye bir tür atar; tür kaynağı belirler:

| Tür | Kaynak |
|---|---|
| `stat_card`, `timeline`, `diagram`, `quote_card`, `code` | **Kodla çizim** (Remotion SVG/CSS) — her zaman |
| `map` | Kodla çizim (SVG harita) veya stok harita görseli |
| `illustration` | Stok → yoksa AI görsel |

1. **Stok video/fotoğraf** — `PEXELS_API_KEY` / `PIXABAY_API_KEY` (ücretsiz). Somut nesne/mekân sahneleri. Kaynak ve lisans `assets/credits.json`'a yazılır, açıklamaya eklenir.
2. **Kodla çizim** — `remotion/src/` altında bileşen.
3. **AI görsel** — ComfyUI (`http://127.0.0.1:8188`) veya `diffusers`. Prompt formülü ve negatif prompt: `taste-design`.
   - 4 GB VRAM (GTX 1650 Ti): SD 1.5 + stil LoRA, 768×432 üret → 2× upscale.
   - Çizgi film / "explainer cartoon" stili: kalın kontur, düz renk LoRA'sı; stil promptu tüm sahnelerde sabit.
   - **Karakter tutarlılığı:** ana karakteri bir kez üret → `rembg` ile kes → sahnelerde cutout olarak yeniden kullan (ifade/poz varyantları ayrı üretilir).
4. **AnimateDiff** — kısa hareketli illüstrasyon (≥ 8 GB VRAM önerilir).

## Kurallar
- Tarihî videolarda anakronik stok görsel kullanılmaz (modern üniforma, modern şehir, yanlış yüzyıl mimarisi).
- Telifli eser, tanınabilir marka veya gerçek kişi portresi AI ile üretilmez.
- Her görsel ≤ 3.2 sn statik kalır; hareket planı `smart_montage.static_shot_plan`.
- Bir kaynak başarısız olursa sıradakine geçilir; hiçbiri olmazsa pipeline **durur** (placeholder görsel yok).
