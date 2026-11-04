---
name: quality-inspector
description: Evaluates and audits generated video scripts, audio quality, visual composition, and retention score before publishing, inspired by NVIDIA/SkillSpector and Strix.
tools: [read_file, write_file]
---

# Pre-Flight Quality Inspector Skill

Bu beceri, **NVIDIA/SkillSpector** ve **usestrix/strix** güvenlik ve kalite standartlarını kullanarak, bir video YouTube'a yüklenmeden önce tüm adımları denetler ve kalite skoru 90/100'ün altındaysa pipeline'ı durdurarak düzeltme ister.

## 1. Denetim Kontrol Listesi (Audit Checklist)

### A. Senaryo Kalite Testi (Script Inspection)
- [ ] **AI Slop Taraması:** Yasaklı kelimelerden herhangi biri geçiyor mu? (Geçiyorsa REJECT).
- [ ] **İlk 3 Saniye Kancası:** İlk 15 kelimede net bir merak unsuru veya şok edici bilgi var mı?
- [ ] **WPM (Words Per Minute):** Konuşma hızı 140 - 180 kelime/dakika aralığında mı?

### B. Ses Kalite Testi (Audio Inspection)
- [ ] **Kırpılma / Bozulma (Clipping):** Ses pik seviyesi -1 dBFS'yi aşıyor mu?
- [ ] **Arka Plan Gürültüsü / Hallucination:** Whisper transkriptinde konuşulmayan hayali tekrarlar var mı?
- [ ] **Müzik Dengesi:** Arka plan müziği konuşmanın -20 dB altında mı?

### C. Görsel & Kurgu Testi (Visual & Edit Inspection)
- [ ] **Statik Süre Limiti:** Herhangi bir görsel 4 saniyeden uzun hareketsiz kalmış mı?
- [ ] **Çözünürlük & Format:** Yatay video için tam 1920x1080, Shorts için 1080x1920 mi?
- [ ] **Metin Okunabilirliği:** Altyazılar ekran sınırlarının dışına taşıyor mu?

### D. Thumbnail & Metadata Testi
- [ ] Başlık 60 karakterden kısa ve merak uyandırıcı mı?
- [ ] Thumbnail'da sağ alt köşe (süre alanı) boş bırakılmış mı?
- [ ] Açıklamada zaman damgaları (timestamps / chapters) ve kaynak linkleri var mı?

## 2. Denetim Raporu Formatı

Rapor `output/audit_report_{topic_id}.json` olarak üretilir:
```json
{
  "overall_score": 94,
  "status": "APPROVED",
  "breakdown": {
    "script_retention": 95,
    "audio_clarity": 98,
    "visual_pacing": 90,
    "thumbnail_ctr_potential": 93
  },
  "flags": []
}
```
Eğer `status == "REJECTED"` ise, ilgili pipeline adımı bildirilen hata ile yeniden çalıştırılır.
