---
name: channel-memory
description: Maintains persistent YouTube channel memory, tracking past video metrics, audience feedback loops, brand identity, and managing automated YouTube API publishing.
tools: [run_command, read_file, write_file]
---

# Channel Memory & Automated Publishing Skill

Bu beceri, **thedotmack/claude-mem** hafıza mimarisini ve **darkzOGx/youtube-automation-agent** dağıtım altyapısını kullanarak kanalın zaman içinde akıllanmasını sağlar. Önceki videoların performansını hatırlar ve YouTube Data API v3 ile videoyu otomatik yükler.

## 1. Kanal Hafıza Dosyası (`config/channel_memory.json`)

Kanalın geçmişi, kitle tercihleri ve başarılı şablonlar bu dosyada kümülatif olarak saklanır:

```json
{
  "channel_name": "Tech Unveiled",
  "brand_voice": "Zeki, samimi, gereksiz laf kalabalığından uzak, kod ve sistem odaklı.",
  "top_performing_hooks": [
    "İki ay önce herkesin yanlış bildiği...",
    "Bunu ilk gördüğümde saçmalık olduğunu düşünmüştüm..."
  ],
  "underperforming_topics": [
    "Çok genel felsefi tartışmalar izlenmedi; somut araç ve rehber videoları %40 daha çok retention aldı."
  ],
  "published_videos_history": [
    {
      "video_id": "dQw4w9WgXcQ",
      "title": "Ajanik Kodlama Rehberi",
      "views_day_7": 14200,
      "ctr": 7.8,
      "average_retention_percent": 62
    }
  ]
}
```

## 2. YouTube Data API v3 Yükleme Akışı

Video render edildikten ve kalite denetiminden onay aldıktan sonra:
1. `pipeline/youtube_uploader.py` devreye girer.
2. `google-api-python-client` ve OAuth2 token ile YouTube'a bağlanır.
3. Parametreler:
   - **Title:** Yüksek CTR potansiyelli, 60 karakter altı başlık.
   - **Description:** SEO uyumlu açıklama, bölüm zaman damgaları (Chapters), kaynaklar ve sosyal linkler.
   - **Tags:** Niş ile ilgili hedeflenmiş 10-15 anahtar kelime.
   - **Privacy Status:** Varsayılan olarak `unlisted` (gizli) veya doğrudan `public`.
   - **Thumbnail:** Üretilen yüksek kaliteli kapak resmi yüklenir.
