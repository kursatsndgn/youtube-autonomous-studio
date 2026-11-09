---
name: trend-researcher
description: Researches trending YouTube topics, scrapes competitor video transcripts using yt-dlp, extracts wisdom and curiosity gaps, and builds high-potential content briefs.
---

# YouTube Trend & Intelligence Research Skill

Bu beceri, **yt-dlp**, **fabric (extract_wisdom / analyze_claims)** ve **open-notebook** metodolojisini birleştirerek rakiplerin en çok izlenen içeriklerini analiz eder, yorumlardaki soru işaretlerini bulur ve viral potansiyeli yüksek video brief'i üretir.

## 1. Veri Toplama Adımları (yt-dlp & Web Search)

1. **Niş ve Trend Tespiti:**
   - Hedef nişteki son 30 günün en çok izlenen videolarını ve Google/YouTube arama trendlerini belirle.
   - `search_web` veya `yt-dlp` komutlarıyla hedef kanalların en popüler videolarının metaverilerini topla:
     ```bash
     yt-dlp --flat-playlist --print "%(title)s | %(view_count)s | %(id)s" "https://www.youtube.com/@channel/videos"
     ```

2. **Transkript ve İçerik Madenciliği (Fabric Pattern):**
   - Rakip videonun transkriptini indir:
     ```bash
     yt-dlp --write-auto-sub --sub-lang en,tr --skip-download "https://www.youtube.com/watch?v=VIDEO_ID"
     ```
   - Transkriptten şu bilgileri ayrıştır:
     - **Core Thesis (Ana Fikir):** Videonun 1 cümlelik vaadi.
     - **Pain Points & Frustrations:** İzleyicinin çözemediği sorunlar.
     - **Missing Angles (Eksik Bırakılanlar):** Yorumlarda izleyicilerin "bunu anlatmamışsın", "şunu nasıl yaparız" dediği noktalar.

3. **Yorum Analizi (Sentiment & Question Mining):**
   - Yorumlardaki en çok beğeni alan soruları listele. Videonun ana çatısı bu yanıtsız kalan sorular üzerine kurulmalıdır.

## 2. Topic Brief Çıktı Şablonu

Araştırma sonucunda `output/brief_{topic_id}.json` dosyasında şu yapı üretilmelidir:

```json
{
  "topic": "Yapay Zeka ile Kod Yazmanın Yeni Çağı: 2026 Trendleri",
  "target_audience": "Geliştiriciler, meraklılar, teknoloji takipçileri",
  "core_promise": "İzleyiciye 10 dakikada sadece prompt değil, tam otonom ajanlarla nasıl yazılım geliştirildiğini öğretmek.",
  "viral_angle": "Geleneksel yazılımcılık bitiyor mu yoksa süper-güç mü kazanıyoruz? (Dramatik ama dürüst kanca)",
  "competitor_weakness": "Rakipler sadece basit chatbot gösterdi; biz çalışan mimari ve canlı ajan akışı göstereceğiz.",
  "recommended_duration_seconds": 480,
  "key_milestones": [
    {"sec": 0, "event": "ADHD Kancası: 3 saniyede şok edici veri"},
    {"sec": 45, "event": "Problem Tanımı ve Neden Önemli Olduğu"},
    {"sec": 180, "event": "Çözüm ve Canlı Uygulama"},
    {"sec": 380, "event": "Gelecek Öngörüsü & Aksiyon Çağrısı (CTA)"}
  ]
}
```

## open-notebook ile iş birliği
Bu skill'in tüm çıktıları `research/<slug>/` kasasına yazılır (bkz. `open-notebook`):
- Rakip videolar ve kapsadıkları/atladıkları noktalar → `competitors.md`
- Transkript özetleri → `fabric/youtube_summary.md` kalıbıyla (MIT, danielmiessler/fabric) özetlenir, kelimesi kelimesine kopyalanmaz.
- İzleyici yorumlarındaki cevapsız sorular ve "kimsenin anlatmadığı açı" → `brief.md`
open-notebook bu boşlukları kaynaklarla doldurur; script-engine ikisini birlikte okur.
