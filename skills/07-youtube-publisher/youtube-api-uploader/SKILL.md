---
name: youtube-api-uploader
description: Final MP4'ü, kapağı ve altyazıyı YouTube Data API v3 ile yükler veya zamanlar. Kod pipeline/youtube_uploader.py. Kimlik doğrulama veya yükleme başarısız olursa hata verir; sahte link döndürmez.
---

# YouTube API Uploader

## Önkoşullar
- `config/client_secrets.json` (Google Cloud OAuth istemcisi, YouTube Data API v3 açık). İlk çalıştırmada tarayıcıda izin → `config/token.pickle`. İkisi de `.gitignore`'da.
- Video 08-qa-security-audit denetiminden geçmiş olmalı.

## Metadata
- **Başlık:** ≤ 60 karakter, merak boşluğu, anahtar kelime başta.
- **Açıklama:** ilk 2 satır özet + bölümler (`0:00 …`, fabric `create_video_chapters` kalıbı) + kaynakça (open-notebook `sources.md`) + stok görsel künyeleri (`assets/credits.json`).
- **Etiketler:** 10–15 hedefli kelime.
- **Gizlilik:** varsayılan `unlisted`; `public` yalnızca kullanıcı açıkça isterse.
- **Kapak:** `thumbnails().set` ayrı çağrı (kanal doğrulanmış olmalı).
- **Altyazı:** subtitle-engine `.srt` → `captions().insert`.
- **Zamanlama:** `status.publishAt` (ISO 8601) + `privacyStatus=private`.

Yükleme sonrası video kimliği ve metadata `global/channel-memory` hafızasına eklenir.
