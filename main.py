"""
YouTube Autonomous Studio — orkestrasyon CLI.

Akış (ARCHITECTURE.md departmanlarıyla):
  02 senaryo (Markdown, ajan + skill'lerle yazılmış)  -> slop denetimi
  03 seslendirme (Edge-TTS [+ OpenVoice ton klonlama]) + kelime zamanları
  05 smart montage (opsiyonel jump-cut) + Remotion render
  08 donuk sahne denetimi
  06 kapak (opsiyonel)
  07 YouTube yükleme (opsiyonel, varsayılan unlisted)

Herhangi bir adım başarısız olursa akış durur; sahte çıktı üretilmez.

Örnek:
  python main.py --topic "Konu" --script output/konu/senaryo.md \
      --out-dir output/konu --thumbnail-text "DÖRT KELİMELİK BAŞLIK"
"""

import argparse
import asyncio
import json
import os
import sys

if sys.platform == "win32":
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except Exception:
            pass

from pipeline.scriptwriter import AntiSlopScriptwriter
from pipeline.voice_engine import VoiceEngine
from pipeline.remotion_render import RemotionRenderer
from pipeline import smart_montage


async def run(a: argparse.Namespace) -> None:
    os.makedirs(a.out_dir, exist_ok=True)
    print(f"=== {a.topic} ===")

    # 02 — senaryo
    script = AntiSlopScriptwriter(a.out_dir).build_script(a.topic, a.script)
    text = " ".join(s["speech_text"] for s in script["scenes"])

    # 03 — ses
    voice = VoiceEngine(a.out_dir, voice=a.voice, rate=a.rate)
    base_audio = os.path.join(a.out_dir, "voice_base.mp3")
    await voice.generate_tts(text, base_audio)
    words = voice.last_words
    audio = base_audio
    if a.clone_voice:
        audio = voice.clone_tone(base_audio, os.path.join(a.out_dir, "voiceover.wav"))

    # 05 — smart montage
    if a.jumpcut:
        jc = smart_montage.jump_cut_audio(audio, os.path.join(a.out_dir, "voiceover_cut.wav"))
        words = smart_montage.remap_words(words, jc["segments"])
        audio = jc["output"]
        print(f"[+] Jump-cut: {jc['removed_seconds']} sn sessizlik kırpıldı")
    cues = smart_montage.classify_broll(text, words)
    with open(os.path.join(a.out_dir, "broll_plan.json"), "w", encoding="utf-8") as f:
        json.dump(cues, f, indent=2, ensure_ascii=False)

    renderer = RemotionRenderer(output_dir=a.out_dir)
    renderer.prepare_props(script, words, audio)
    video = renderer.render_video(os.path.join(a.out_dir, "final.mp4"), composition=a.composition)

    # 08 — donuk sahne denetimi
    frozen = smart_montage.detect_static(video, max_static=4.0)
    if frozen:
        print(f"[!] 4 sn'den uzun donuk bölümler: {frozen}")

    # 06 — kapak
    thumb = None
    if a.thumbnail_text:
        from pipeline.thumbnail_engine import make_variants
        thumbs = make_variants(a.thumbnail_text, os.path.join(a.out_dir, "thumbnail"),
                               bg=a.thumbnail_bg, figure=a.thumbnail_figure)
        thumb = thumbs[0]
        print(f"[+] Kapak varyantları: {thumbs}")

    # 07 — yükleme
    if a.auto_upload:
        if frozen and not a.force:
            raise SystemExit("Donuk sahne bulguları var; yükleme durduruldu (--force ile geç).")
        from pipeline.youtube_uploader import YouTubeUploader
        up = YouTubeUploader()
        up.authenticate()
        res = up.upload_video(video_path=video, title=a.title or a.topic, description=a.description or "",
                              privacy_status=a.privacy, thumbnail_path=thumb)
        print(f"[+] Yüklendi: {res['url']}")
    print(f"[✓] Bitti: {video}")


def main() -> None:
    p = argparse.ArgumentParser(description="YouTube Autonomous Studio")
    p.add_argument("--topic", required=True)
    p.add_argument("--script", required=True, help="Markdown senaryo (## Sahne / **Ses:** / **Görsel:**)")
    p.add_argument("--out-dir", default="output")
    p.add_argument("--composition", default="MainVideo", help="Remotion kompozisyon kimliği")
    p.add_argument("--voice", default="tr-TR-AhmetNeural")
    p.add_argument("--rate", default="-4%")
    p.add_argument("--clone-voice", action="store_true", help="OpenVoice V2 ile config/voice/reference.wav tınısına dönüştür")
    p.add_argument("--jumpcut", action="store_true", help="Sessizlikleri kırp (belgeselde varsayılan kapalı)")
    p.add_argument("--thumbnail-text")
    p.add_argument("--thumbnail-bg")
    p.add_argument("--thumbnail-figure")
    p.add_argument("--auto-upload", action="store_true")
    p.add_argument("--title")
    p.add_argument("--description")
    p.add_argument("--privacy", default="unlisted", choices=["public", "unlisted", "private"])
    p.add_argument("--force", action="store_true")
    asyncio.run(run(p.parse_args()))


if __name__ == "__main__":
    main()
