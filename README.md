# 🎬 YouTube Autonomous Studio

Araştırmadan senaryoya, seslendirmeden programatik montaja, kapak tasarımından YouTube'a yüklemeye kadar video üretim hattı.
Mimari: [ARCHITECTURE.md](ARCHITECTURE.md). Her departman `skills/` altında bir klasördür; çalışan kod `pipeline/` altındadır.

> **İlke:** Bir adım başarısız olursa hat durur. Sahte ses, görsel, video veya YouTube linki üretilmez.

## Departmanlar ve skill'ler

| Departman | Skill | Kaynak | Kod |
|---|---|---|---|
| 01 Araştırma | `trend-researcher` | fabric `youtube_summary` (MIT, kopya) | `pipeline/researcher.py` |
|  | `open-notebook` | lfnovo/open-notebook (opsiyonel sunucu) | `research/<slug>/` kasası |
| 02 Senaryo | `script-engine` | fabric `extract_wisdom`, `create_video_chapters` (MIT, kopya) | `pipeline/scriptwriter.py` |
|  | `creative-fiction` | jwynia/agent-skills (lisanssız → yönlendirme) | — |
|  | `book-to-skill` | virgiliojr94/book-to-skill (MIT, kopya) | upstream script |
|  | `turkish-literary-script-doctor` | stüdyoya özgü | — |
| 03 Ses | `voice-pipeline` | Edge-TTS + myshell-ai/OpenVoice V2 (MIT) | `pipeline/voice_engine.py` |
| 04 Görsel | `visual-pipeline` | Pexels / Pixabay / ComfyUI / rembg | `pipeline/visual_engine.py` |
|  | `lemo-opuscar` | lemomo-ai/lemo-opuscar (MIT, kopya): kodla film, 66 stil | upstream kütüphane (`~/lemo-opuscar`) |
| 05 Kurgu | `remotion-engine` | Remotion (+ remotion-dev/skills yönlendirme) | `remotion/`, `pipeline/remotion_render.py` |
|  | `ffmpeg-moviepy` (Smart Montage) | OpenMontage fikirleri, sıfırdan yazıldı | `pipeline/smart_montage.py` |
|  | `concat-editor` | jub0t/concat (AGPL, ayrı uygulama, MCP ile) | `concat --mcp` |
|  | `subtitle-engine` | Edge-TTS WordBoundary / faster-whisper | Remotion `Captions` |
| 06 Kapak | `thumbnail-engine` | stüdyoya özgü | `pipeline/thumbnail_engine.py` |
|  | `taste-design` | leonxlnx/taste-skill (MIT, kopya) | — |
|  | `mcptoon-graphics` | ui-ux-pro-max banner-design (MIT, kopya) + çizgi film stil rehberi | — |
| 07 Yayın | `youtube-api-uploader` | YouTube Data API v3 | `pipeline/youtube_uploader.py` |
| 08 QA & Güvenlik | `no-ai-slop` | petergyang/no-ai-slop (MIT, kopya) + Türkçe kalıplar | `scriptwriter.BANNED_CLICHES` |
|  | `skill-spector` | NVIDIA/SkillSpector (araç) | CLI |
|  | `strix-audit` | usestrix/strix (araç) | CLI |

Kopyalanan upstream dosyalar değiştirilmeden, kendi LICENSE dosyalarıyla birlikte tutulur.
Lisans dosyası olmayan repolar (jwynia/agent-skills, remotion-dev/skills) kopyalanmaz; skill yalnızca yönlendirir.

## Kurulum
```bash
pip install -r requirements.txt
cd remotion && npm install && cd ..
python scripts/install_skills.py          # skill'leri .claude/skills/ altına kurar (--user: ~/.claude/skills)
```
Opsiyonel:
- **OpenVoice (ses klonlama):** `python scripts/install_openvoice.py`, sonra `config/voice/reference.wav` ekle ve `--clone-voice` kullan.
- **Stok görsel:** `PEXELS_API_KEY`, `PIXABAY_API_KEY` (ikisi de ücretsiz hesapla alınır).
- **AI görsel:** `COMFYUI_URL`, `COMFYUI_CHECKPOINT`, `COMFYUI_LORA`.
- **Yükleme:** YouTube OAuth (`config/client_secrets.json`).

## Kullanım
Senaryo ajan tarafından skill'lerle yazılır (`## Sahne N — Başlık` / `**Ses:**` / `**Görsel:**`), sonra:
```bash
python main.py --topic "Konu" --script output/konu/senaryo.md \
    --out-dir output/konu --thumbnail-text "DÖRT KELİMELİK BAŞLIK"
```
Bayraklar: `--clone-voice` (OpenVoice), `--jumpcut`, `--composition <id>`, `--auto-upload --privacy unlisted`.

Smart Montage araçları tek başına:
```bash
python pipeline/smart_montage.py silences ses.mp3
python pipeline/smart_montage.py static final.mp4 --max 4
```

## Kişisel çıktılar
`output/`, `remotion/public/` ve kişisel video kompozisyonları git'e girmez (`.gitignore`). Kendi kompozisyonunu `remotion/src/local/` altında tutup `Root.tsx`'e yerelde ekleyebilirsin.
