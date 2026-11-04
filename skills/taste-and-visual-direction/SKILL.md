---
name: taste-and-visual-direction
description: Provides visual taste standards, color palettes, thumbnail composition rules, and ComfyUI / Stable Diffusion prompt crafting guidelines.
tools: [read_file, write_file]
---

# Visual Taste & Design Direction Skill

Bu beceri, **leonxlnx/taste-skill**, **ui-ux-pro-max-skill** ve **awesome-design-md** standartlarını temel alarak ucuz yapay zeka görselleri yerine sinematik, estetik ve tutarlı sahneler ve yüksek CTR'lı thumbnail'lar üretir.

## 1. Estetik Standartlar ("Good Taste" Principles)

- **Aşırı Doygunluktan Kaçın (No Neon Slop):** Yapay zeka görsellerinin en büyük belirtisi aşırı yapay parlaklık ve anlamsız neon ışıklardır. Doğal ışık kaynakları (key light, rim light), sinematik gölgeler ve temiz renk paletleri tercih edilmelidir.
- **Renk Hiyerarşisi (60-30-10 Kuralı):**
  - %60 Dominant Arka Plan (Derin lacivert, mat antrasit, yumuşak sıcak gri)
  - %30 Tamamlayıcı Ton (Temiz beyaz, açık füme, pastel destek)
  - %10 Vurgu Rengi (Elektrik sarısı, canlı mercan veya zümrüt yeşili - sadece odak noktasında!)
- **Tipografi Hiyerarşisi:**
  - Modern sans-serif, kalın, okunaklı fontlar (Inter, Montserrat, Bebas Neue, Clash Display).
  - Yüksek kontrast (koyu arka planda beyaz metin + renkli kelime vurgusu).

## 2. ComfyUI / Image Prompt Mühendisliği

Her sahne için prompt üretirken şu katmanlı formül uygulanır:
1. **Subject (Özne):** Net tanımlanmış odak noktası.
2. **Environment & Context (Ortam):** Minimalist veya amaca uygun arkaplan.
3. **Lighting & Atmosphere (Işık):** Cinematic diffused lighting, subtle volumetric rays, soft shadows.
4. **Camera & Lens (Kamera):** 35mm lens, f/1.8 aperture, shallow depth of field, sharp focus.
5. **Style Negative Prompts:** `blurry, distorted hands, oversaturated, cartoonish, lowres, text watermarks, extra limbs, deformed`.

## 3. Thumbnail (Küçük Resim) Tasarım Kuralları (High-CTR Architecture)

1. **3 Eleman Kuralı:** Bir thumbnail'da en fazla 3 odak noktası olmalıdır (Örn: Şaşırmış insan yüzü / ikonik nesne + Zıt renkli büyük grafik + 3 kelimelik dev metin).
2. **Kör Nokta Güvenliği:** YouTube süre sayacının geldiği sağ alt köşeye asla metin veya kritik öge koyma!
3. **Küçük Ekranda Okunabilirlik:** Tasarım %15 boyutuna küçültüldüğünde (mobil ekranda gezinirken) bile anında anlaşılmalıdır.
