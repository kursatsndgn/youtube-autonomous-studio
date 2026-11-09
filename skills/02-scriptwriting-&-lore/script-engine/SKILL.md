---
name: script-engine
description: Writes natural, human-sounding, punchy YouTube video scripts by strictly eliminating AI cliches, buzzwords, generic transitions, and robotic fluff.
---

# Anti-Slop YouTube Scriptwriting Skill

Bu beceri, **petergyang/no-ai-slop** manifestosu, **jwynia/agent-skills/creative** prensipleri ve **fabric** senaryo kalıplarını harmanlayarak izleyiciyi sıkmayan, asla "yapay zeka yazmış" hissi vermeyen, doğal ve vurucu senaryolar üretir.

## 1. Kesinlikle Yasaklı "AI Slop" İfadeleri (Banned List)

Senaryoda aşağıdaki kalıpların veya türevlerinin geçmesi KESİNLİKLE YASAKTIR:
- ❌ *"In today's fast-paced digital world..."* (Günümüzün hızla değişen dünyasında...)
- ❌ *"Let's dive right in..."* / *"Let's delve into..."* (Hemen derinlemesine dalalım...)
- ❌ *"Game-changer"* / *"Revolutionary"* / *"Tapestry"* / *"Testament to"*
- ❌ *"Whether you are a beginner or an expert..."* (İster yeni başlayan ister uzman olun...)
- ❌ *"It is important to remember that..."* (Unutmamak gerekir ki...)
- ❌ *"Without further ado..."* (Lafı daha fazla uzatmadan...)
- ❌ *"In conclusion..."* / *"To sum up..."* (Sonuç olarak...)
- ❌ Cümleye sürekli *"Moreover"*, *"Furthermore"*, *"Additionally"* ile başlama.

## 2. Doğal Konuşma Dili Kuralları (Human Voice Engine)

1. **Giriş (First Sentence):**
   - Asla selamla ("Herkese merhaba kanalıma hoş geldiniz") başlama!
   - İlk cümle doğrudan aksiyona, probleme ya da şaşırtıcı bir iddiaya girmelidir.
   - Örnek İyi: *"Eğer son 6 ayda kod yazdıysanız, fark etmişsinizdir: Bir şeyler kökünden değişti."*
   - Örnek Kötü: *"Merhaba arkadaşlar bugün yapay zekanın yazılımdaki önemini inceleyeceğiz."*

2. **Cümle Ritim Varyasyonu (Burstiness & Cadence):**
   - Arka arkaya 3 tane uzun bileşik cümle kurma.
   - Kısa cümleler kullan. Vur. Dur. Sonra biraz açıkla. Tek kelimelik vurgular yap.
   - *"Mantıklı mı? Değil. Ama herkes bunu yapıyor."*

3. **Soyut değil, Somut Örnekler:**
   - "Verimlilik artar" deme. "Günde 3 saatinizi alan pull request incelemesini 15 dakikaya düşürür" de.
   - Karakterler, anektodlar ve somut senaryolar ekle.

4. **Kişisel ve Samimi Ton:**
   - Bir akademisyen gibi değil; kahve içerken karşındaki zeki bir arkadaşına anlatıyormuş gibi konuş.
   - Dürüst ol: Bir şey kötüyse veya henüz mükemmel değilse açıkça söyle ("Dürüst olalım, hâlâ bazen saçmalıyor").

## 3. Sahne Bazlı Çıktı Formatı

Senaryo bir sonraki ses ve video montaj aşaması için sahne sahne ayrıştırılmış `output/script_{topic_id}.json` olarak kaydedilmelidir:

```json
{
  "scenes": [
    {
      "scene_id": 1,
      "speech_text": "Bunu ilk gördüğümde gözlerime inanamadım. Çünkü yıllardır bildiğimiz kurallar tamamen çöpe gitti.",
      "visual_prompt": "Cinematic close-up of a programmer staring at a glowing screen with shock, neon cyan and amber lighting, modern office, 8k",
      "pacing": "fast",
      "overlay_text": "EZBERLER BOZULDU"
    }
  ]
}
```

## Stüdyo akışı (02-scriptwriting-&-lore)
1. **Girdi:** `research/<slug>/brief.md` + `facts.md` (trend-researcher + open-notebook).
2. **Yapı:** `creative-fiction` ile anlatı omurgası (karakter yayı, anahtar anlar, final).
3. **Taslak:** bu dosyadaki anti-slop kuralları + `retention-pacing.md` (3 sn kancası, open-loop, tempo).
   Bilgi damıtma için `fabric/extract_wisdom.md`; açıklama bölümleri için `fabric/create_video_chapters.md` (danielmiessler/fabric, MIT).
4. **Türkçe doktor:** `turkish-literary-script-doctor` (TDK imla, edebî sanatlar, ritim).
5. **Slop denetimi:** `skills/08-qa-security-audit/no-ai-slop/` (`SKILL.md` + `turkish-patterns.md`); kod tarafı `pipeline/scriptwriter.py` → `BANNED_CLICHES`.
6. **Çıktı:** `output/<slug>/senaryo.md` — sahne başına `**Ses:**` ve `**Görsel:**` blokları (`scriptwriter.load_script_md` bunu okur).
