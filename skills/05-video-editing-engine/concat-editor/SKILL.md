---
name: concat-editor
description: Concat masaüstü video editörünü MCP üzerinden kullanarak render edilmiş videolara son kurgu yapar — çok kanallı timeline, kesme/birleştirme, başlık ve stilize altyazı, keyframe, efekt/geçiş, arka plan silme, ses temizleme, kare önizleme ve 4K dışa aktarım. Remotion veya Lemo-Opuscar çıktısını birleştirmek, elle düzeltmek veya insanla birlikte düzenlenebilir bir proje dosyası bırakmak gerektiğinde kullan.
---

# Concat Editor (MCP)

Kaynak: [jub0t/concat](https://github.com/jub0t/concat) — ücretsiz, açık kaynak, yerel çalışan, çapraz platform video editörü (Rust, GPU compositor).
**Lisans AGPL-3.0:** kodu bu repoya kopyalanmaz; Concat ayrı bir uygulama olarak kurulur ve yalnızca MCP/JSON-RPC ile konuşulur (bu, repomuzun lisansını etkilemez).

## Stüdyodaki yeri
```
main.py (Remotion) ──┐
Lemo-Opuscar filmi ──┼──▶ concat-editor: birleştir, son rötuş, altyazı, ses temizleme ──▶ final.mp4 ──▶ thumbnail-engine / youtube-api-uploader
stok / kayıt ────────┘
```
Ne zaman Concat, ne zaman FFmpeg:
| İş | Araç |
|---|---|
| Otomatik, toplu, kesin tekrar edilebilir işlem (jump-cut, donuk sahne kontrolü) | `ffmpeg-moviepy` |
| Kodla üretilen sahneler | `remotion-engine`, `lemo-opuscar` |
| Birden çok parçayı timeline'da birleştirme, geçiş, başlık, keyframe, ses temizleme, kullanıcının sonra elle açıp düzenleyebileceği proje | **concat-editor** |

## Kurulum (kullanıcı yapar)
1. Uygulamayı indir: https://concat.standalones.org/#download veya GitHub Releases.
2. Claude Code'a MCP olarak ekle (Windows, kullanıcıya kurulum):
   ```bash
   claude mcp add concat -- "%LOCALAPPDATA%\Programs\Concat\concat.exe" --mcp
   ```
   Tüm kullanıcılar için kurulduysa: `"C:\Program Files\Concat\concat.exe"`. macOS: `/Applications/Concat.app/Contents/MacOS/concat`.
3. İsteğe bağlı: altyazı (Whisper), ses ve arka plan silme modelleri uygulamada **Settings** içinden bir kez indirilir; sonra çevrimdışı çalışır.

## Çalışma modları
- `--mcp headless`: pencere açık olmadan motoru kendi çalıştırır. Otomasyon için varsayılan tercih.
- `--mcp window`: Concat açık ve **Settings > Automation > Scripts and apps** açıksa pencere üzerinden çalışır; ajan, kullanıcının ekranda açık projesinin üzerine yazamaz.
- Ajan dosyaları yalnızca kullanıcının ev klasörü altına yazar. Repo başka yerdeyse `CONCAT_MCP_ROOTS` ile izin verilir.

## İş akışı (MCP araçları)
1. `concat_version` → mod ve sürüm kontrolü.
2. `project_create` (`output/<slug>/concat/` altında) → `project_set_video` (1920×1080, 30 fps).
3. `media_probe` + `media_import` → Remotion/Lemo çıktıları, ses, müzik.
4. `clips_add_sequence` ile sahneleri sırala; `clip_trim`, `clips_split`, `clips_move` ile ince ayar.
5. Başlık/altyazı: `title_add`, `title_style_words` (vurgu kelimesi rengi), gerekiyorsa `captions_add` (yerel Whisper). Bizim kelime zamanlı altyazımız varsa çift altyazı ekleme.
6. Hareket: `keyframe_set` (punch-in %110–120, pan) — 3.2 sn ritim kuralı (`smart_montage.static_shot_plan`).
7. Efekt/geçiş: `effects_list` → `effect_layer_add`; tarihî videolarda abartılı geçişten kaçın (taste-design).
8. Kontrol: `preview_frame` ile kritik saniyelerden kare al ve gözle doğrula.
9. `project_save` → `export_start` (H.264, 1080p) → `export_wait`.
10. Çıktıyı `smart_montage.py static` ile donuk sahne denetiminden geçir.

## Kurallar
- Düzenlemeler `project_save`'e kadar bellekte; her büyük adımdan sonra kaydet.
- Toplu değişiklikleri tek geri alma adımı için `edit_apply` (batch) ile yap.
- Kullanıcının açık projesine dokunma; ajan her zaman kendi projesini oluşturur.
- Concat'in TTS/ses klonlama özelliği Türkçe için doğrulanmadı; Türkçe anlatım `voice-pipeline`'dan gelir.
- Proje ve dışa aktarımlar `output/` altında kalır (git dışı).
