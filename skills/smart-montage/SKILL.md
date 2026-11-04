---
name: smart-montage
description: Automates intelligent video editing, silence removal (jump-cuts), semantic B-roll placement, and agentic multi-stage video workflows based on calesthio/openmontage.
tools: [read_file, write_file, run_command]
---

# Smart Montage & Agentic Workflow Skill

Bu beceri, **calesthio/openmontage** felsefesini referans alarak ses kaydındaki nefes ve duraklama boşluklarını milisaniye düzeyinde kırpar (Jump-Cut), senaryo metninin duygu ve konusuna göre otomatik B-roll video eşleştirmesi yapar.

## 1. Sessizlik Kırpma (Silence Removal & Jump-Cut)

Monotonluğu engellemek ve izleyicinin dikkatini sürekli tutmak için:
- 350 milisaniyeden uzun tüm sessizlikler tespit edilir.
- Ses seviyesi -35 dB altına düşen aralıklar FFmpeg `silencedetect` filtresi ile kesilerek video dinamik hale getirilir:
  ```bash
  ffmpeg -i voiceover.wav -af "silencedetect=noise=-35dB:d=0.35" -f null -
  ```

## 2. Semantik B-Roll ve Katman Eşleştirme Kuralları

Senaryodaki her cümle için şu sınıflandırma yapılır:
- **Konuşan / Ana Sahne (A-Roll):** Doğrudan kameraya anlatım veya yapay zeka sunucu sahnesi (en fazla 4 saniye).
- **Destekleyici Görsel (B-Roll):**
  - Kod / Yazılım bahsediliyorsa -> `motion-canvas` animasyonu.
  - İstatistik / Metrik bahsediliyorsa -> `hyperframes` HTML/CSS infografik kartı.
  - Formül / Veri akışı bahsediliyorsa -> `manim` matematik grafiği.
  - Dramatik anlatım -> ComfyUI sinematik görseli + Ken Burns zoom.

## 3. Pacing ve Ritim Denetimi

OpenMontage kuralına göre video içerisinde hiçbir statik plan (b-roll veya slayt) 3.2 saniyeden uzun kesintisiz kalamaz. Her 3.2 saniyede bir kamera açısı, zoom oranı (%110 -> %120) veya overlay grafiği değişmelidir.
