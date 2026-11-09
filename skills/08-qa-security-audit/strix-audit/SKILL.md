---
name: strix-audit
description: Repo genelinde (API anahtarları, OAuth token dosyaları, yükleyici kodu) usestrix/strix ile güvenlik taraması yapar.
---

# Strix Güvenlik Taraması

Kaynak: [usestrix/strix](https://github.com/usestrix/strix) (Apache-2.0). Yerelde Docker ile çalışan, LLM destekli güvenlik test aracı.

## Önkoşullar
- Docker çalışıyor olmalı.
- LLM anahtarı: `STRIX_LLM` ve `LLM_API_KEY` ortam değişkenleri (anahtar repoya yazılmaz).

## Kurulum ve kullanım
```bash
pipx install strix-agent
strix --target ./
```

## Stüdyoya özel kontrol listesi
- `config/client_secrets.json`, `config/token.pickle`, `.env` git geçmişine girmemiş mi.
- Kodda gömülü API anahtarı yok mu (Pexels, Pixabay, OpenAI vb.).
- `youtube_uploader.py` token veya kimlik bilgisini loglamıyor mu.
- Rapor `output/strix/`; kritik bulgu varsa yayın durur.
