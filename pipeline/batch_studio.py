"""
Batch Studio Automation Engine
Produces 5 Full Long-form Videos (12-15 min) + 2 Shorts each (Total 15 Videos)
and automatically uploads them to YouTube without manual intervention.
"""

import asyncio
import os
import sys
import json
from typing import List, Dict, Any

from pipeline.researcher import TrendResearcher
from pipeline.scriptwriter import AntiSlopScriptwriter
from pipeline.voice_engine import VoiceEngine
from pipeline.visual_engine import VisualEngine
from pipeline.remotion_render import RemotionRenderer
from pipeline.shorts_generator import ShortsGenerator
from pipeline.youtube_uploader import YouTubeUploader

# 5 Belgesel Konusu (12-15 Dakikalık Kurgular)
BATCH_PROJECTS = [
    {
        "id": 1,
        "topic": "Bir Futbol Maçı Gerçek Bir Savaşı Nasıl Başlattı? (1969 Futbol Savaşı)",
        "target_minutes": 14,
        "description": "1969 yılında El Salvador ve Honduras arasında oynanan 90 dakikalık futbol maçı, nasıl 3000 insanın hayatına mal olan 100 saatlik bir savaşa dönüştü?",
        "tags": ["futbol savaşı", "el salvador", "honduras", "tarih belgeseli", "ilginç olaylar"]
    },
    {
        "id": 2,
        "topic": "Futbol Tarihinin En Utanç Verici 90 Dakikası: 1982 Gijon Skandalı",
        "target_minutes": 13,
        "description": "Almanya ve Avusturya'nın Cezayir'i kupadan elemek için sahada paslaşarak zaman geçirdiği, taraftarların para sallayarak protesto ettiği o kara gün.",
        "tags": ["gijon skandalı", "1982 dünya kupası", "futbol tarihi", "cezayir", "almanya"]
    },
    {
        "id": 3,
        "topic": "Didier Drogba Bir Ülkedeki İç Savaşı Nasıl Durdurdu?",
        "target_minutes": 13,
        "description": "Fildişi Sahili'nde 5 yıldır süren kanlı iç savaş, Didier Drogba'nın soyunma odasında canlı yayında diz çöküp ulusa seslenmesiyle nasıl bitti?",
        "tags": ["drogba", "fildişi sahili", "iç savaş", "futbol mucizesi", "chelsea"]
    },
    {
        "id": 4,
        "topic": "Tarihi Değiştiren Tek Bir Hata: 1. Dünya Savaşını Başlatan Yanlış Dönüş",
        "target_minutes": 14,
        "description": "Franz Ferdinand'ın şoförü Saraybosna'da o yanlış sokağa girmeseydi, 20 milyon insanın öldüğü 1. Dünya Savaşı gerçekten başlar mıydı?",
        "tags": ["1. dünya savaşı", "franz ferdinand", "saraybosna", "tarihi hatalar", "kelebek etkisi"]
    },
    {
        "id": 5,
        "topic": "Diktatörlerin Sahadaki Savaşı: Mussolini ve 'Kazan ya da Öl' Emri",
        "target_minutes": 15,
        "description": "1934 Dünya Kupası'nda Benito Mussolini'nin İtalyan milli takımına gönderdiği tek cümlelik telgraf: 'Vincere o Morire' (Kazan ya da Öl).",
        "tags": ["mussolini", "1934 dünya kupası", "italya", "faşizm ve spor", "tarih"]
    }
]


async def run_batch_automation(auto_upload: bool = True, privacy: str = "unlisted"):
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=" * 70)
    print("🎬 YOUTUBE TAM OTONOM FABRİKA (BATCH STUDIO)")
    print("📦 Üretim Hedefi: 5 Ana Video (12-15 dk) + 10 YouTube Shorts")
    print(f"📡 Otomatik YouTube Yükleme: {'AÇIK (' + privacy + ')' if auto_upload else 'KAPALI'}")
    print("=" * 70)

    researcher = TrendResearcher()
    writer = AntiSlopScriptwriter()
    voice = VoiceEngine()
    visuals = VisualEngine()
    renderer = RemotionRenderer()
    shorts_gen = ShortsGenerator()
    uploader = YouTubeUploader() if auto_upload else None

    summary_results = []

    for idx, project in enumerate(BATCH_PROJECTS, 1):
        topic = project["topic"]
        print(f"\n[{idx}/5] 🚀 PROJE BAŞLATILIYOR: {topic}")
        print("-" * 65)

        # 1. Trend & Brief
        brief = researcher.generate_topic_brief(topic)

        # 2. 12-15 Dakikalık Anti-Slop Bölüm Senaryosu
        script = writer.build_script(topic)

        # 3. Görsellerin Hazırlanması
        for scene in script["scenes"]:
            visuals.generate_scene_image(scene["scene_id"], scene["visual_prompt"])

        # 4. Seslendirme (TTS) & Kelime Hizalama
        audio_file = os.path.join("output", f"voiceover_ep_{idx}.wav")
        full_text = " ".join([s["speech_text"] for s in script["scenes"]])
        await voice.generate_tts(full_text, audio_file)
        words_data = voice.align_words_faster_whisper(audio_file)

        # 5. Ana Video (1920x1080) Render
        main_video_path = os.path.join("output", f"main_ep_{idx}.mp4")
        renderer.prepare_props(script, words_data, audio_file)
        rendered_main = renderer.render_video(main_video_path)

        # 6. Otomatik 2 Shorts Render (1080x1920 Dikey)
        shorts_meta = shorts_gen.generate_two_shorts_scripts(topic, script["scenes"])
        rendered_shorts = []
        for s_idx, s_item in enumerate(shorts_meta, 1):
            s_path = shorts_gen.render_shorts(f"ep_{idx}_{s_idx}", s_item["title"], words_data)
            rendered_shorts.append({"title": s_item["title"], "path": s_path})

        # 7. YouTube Sıfır Dokunuşla Otomatik Yükleme
        uploaded_main_url = None
        uploaded_shorts_urls = []

        if auto_upload and uploader:
            # Ana Videoyu Yükle
            res_main = uploader.upload_video(
                video_path=rendered_main,
                title=f"{topic} (Tarih Belgeseli)",
                description=f"{project['description']}\n\nAbone olmayı ve bildirimleri açmayı unutmayın!\n\n#tarih #futbol #belgesel",
                tags=project["tags"],
                privacy_status=privacy,
                is_shorts=False
            )
            uploaded_main_url = res_main.get("url")

            # 2 Shorts'u Yükle
            for s in rendered_shorts:
                res_s = uploader.upload_video(
                    video_path=s["path"],
                    title=s["title"],
                    description=f"{s['title']} - Detaylar kanaldaki ana videoda!\n\n#Shorts #Tarih #Futbol",
                    privacy_status=privacy,
                    is_shorts=True
                )
                uploaded_shorts_urls.append(res_s.get("url"))

        summary_results.append({
            "topic": topic,
            "main_video": rendered_main,
            "main_url": uploaded_main_url,
            "shorts": rendered_shorts,
            "shorts_urls": uploaded_shorts_urls
        })

        print(f"✅ Proje {idx}/5 Tamamlandı! (1 Ana Video + 2 Shorts Hazır)")

    print("\n" + "=" * 70)
    print("🎉 BATCH OTOMASYON BAŞARIYLA TAMAMLANDI!")
    print(f"📊 Toplam Üretilen: 5 Ana Video + 10 YouTube Shorts = 15 Video")
    print("=" * 70)
    return summary_results


if __name__ == "__main__":
    asyncio.run(run_batch_automation(auto_upload=True, privacy="unlisted"))
