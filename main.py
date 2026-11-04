"""
YouTube Autonomous Studio - Main Orchestrator CLI
Integrates all skills, AI engines, programmatic renderers, and publish pipelines.
"""

import argparse
import asyncio
import os
import sys

# Windows konsol UTF-8 çıktı desteği
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(PROJECT_DIR)

from pipeline.researcher import TrendResearcher
from pipeline.scriptwriter import AntiSlopScriptwriter
from pipeline.voice_engine import VoiceEngine
from pipeline.visual_engine import VisualEngine
from pipeline.remotion_render import RemotionRenderer
from pipeline.youtube_uploader import YouTubeUploader


async def run_pipeline(topic: str, auto_upload: bool = False, privacy: str = "unlisted"):
    print("=" * 65)
    print("🚀 YOUTUBE AUTONOMOUS STUDIO: OTONOM VİDEO ÜRETİM HATTI")
    print(f"🎯 Hedef Konu: {topic}")
    print("=" * 65)

    # Adım 1: Trend ve Rakip Araştırması (yt-dlp, open-notebook, fabric)
    print("\n[Aşama 1/6] 🔍 Trend ve Rakip Analizi Başlatılıyor...")
    researcher = TrendResearcher()
    brief = researcher.generate_topic_brief(topic)
    competitors = researcher.search_competitor_videos(topic, max_results=3)
    print(f"   Bulunan rakip video sayısı: {len(competitors)}")

    # Adım 2: Anti-Slop & ADHD Pacing Senaryo Üretimi
    print("\n[Aşama 2/6] ✍️ Anti-Slop & ADHD Pacing ile Senaryo Yazılıyor...")
    writer = AntiSlopScriptwriter()
    script = writer.build_script(topic)
    print(f"   Toplam Sahne Sayısı: {script['total_scenes']}")

    # Adım 3: Görsel ve Sticker Varlıklarının Üretimi (ComfyUI + rembg)
    print("\n[Aşama 3/6] 🎨 Görsel ve Cutout Varlıklar Hazırlanıyor...")
    visuals = VisualEngine()
    for scene in script["scenes"]:
        img_path = visuals.generate_scene_image(scene["scene_id"], scene["visual_prompt"])

    # Adım 4: Seslendirme ve Kelime Bazlı Senkronizasyon (OpenVoice + Faster-Whisper)
    print("\n[Aşama 4/6] 🎙️ Seslendirme ve Kelime Zamanlaması (Faster-Whisper)...")
    voice = VoiceEngine()
    full_text = " ".join([s["speech_text"] for s in script["scenes"]])
    audio_path = os.path.join("output", "voiceover.wav")
    await voice.generate_tts(full_text, audio_path)
    word_alignment = voice.align_words_faster_whisper(audio_path)

    # Adım 5: Programatik Video Kurgu & Montaj (Remotion)
    print("\n[Aşama 5/6] 🎬 Remotion ile Video Kurgusu ve Render Ediliyor...")
    renderer = RemotionRenderer()
    renderer.prepare_props(script, word_alignment, audio_path)
    final_video = renderer.render_video("output/final_video.mp4")

    # Adım 6: Kalite Denetimi & YouTube Yükleme
    print("\n[Aşama 6/6] 📡 YouTube Dağıtım & Yayınlama Aşaması...")
    if auto_upload:
        uploader = YouTubeUploader()
        res = uploader.upload_video(
            video_path=final_video,
            title=f"{topic} (Detaylı Rehber)",
            description=f"Bu videoda {topic} konusunu uçtan uca inceliyoruz.\n\n#teknoloji #yapayzeka",
            privacy_status=privacy
        )
        print(f"✅ Video başarıyla yüklendi! Link: {res.get('url')}")
    else:
        print("ℹ️ Otomatik yükleme kapalı. Video yerel olarak hazırlandı:")
        print(f"   📂 Çıktı: {final_video}")

    print("\n🎉 Tüm süreç başarıyla tamamlandı!")


def main():
    parser = argparse.ArgumentParser(description="Autonomous YouTube Video Generation Studio")
    parser.add_argument("--topic", type=str, default="Yapay Zeka ile Kod Yazmanın Yeni Çağı", help="Video konusu")
    parser.add_argument("--auto-upload", action="store_true", help="Render sonrası YouTube'a otomatik yükle")
    parser.add_argument("--privacy", type=str, default="unlisted", choices=["public", "unlisted", "private"])

    args = parser.parse_args()
    asyncio.run(run_pipeline(args.topic, args.auto_upload, args.privacy))


if __name__ == "__main__":
    main()
