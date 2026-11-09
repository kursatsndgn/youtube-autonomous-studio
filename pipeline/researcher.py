"""
Trend and Competitor Research Engine
Powered by yt-dlp and Fabric pattern principles.
"""

import json
import os
import subprocess
from typing import Dict, List, Any


class TrendResearcher:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def search_competitor_videos(self, query: str, max_results: int = 5) -> List[Dict[str, Any]]:
        """yt-dlp kullanarak YouTube'da en popüler videoları arar."""
        cmd = [
            "yt-dlp",
            f"ytsearch{max_results}:{query}",
            "--dump-json",
            "--flat-playlist"
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            videos = []
            for line in result.stdout.strip().split("\n"):
                if line:
                    data = json.loads(line)
                    videos.append({
                        "id": data.get("id"),
                        "title": data.get("title"),
                        "url": data.get("url") or f"https://www.youtube.com/watch?v={data.get('id')}",
                        "view_count": data.get("view_count", 0)
                    })
            return videos
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise RuntimeError(f"yt-dlp araması başarısız: {e}") from e

    def download_transcript(self, video_url: str) -> str:
        """yt-dlp ile videonun altyazı/transkriptini çeker."""
        cmd = [
            "yt-dlp",
            "--write-auto-sub",
            "--sub-lang", "en,tr",
            "--skip-download",
            "-o", os.path.join(self.output_dir, "%(id)s.%(ext)s"),
            video_url
        ]
        try:
            subprocess.run(cmd, check=True, capture_output=True)
            return "Transkript başarıyla indirildi."
        except Exception as e:
            return f"Transkript indirilemedi: {e}"

    def generate_topic_brief(self, topic: str, target_audience: str = "Genel Teknoloji Takipçileri") -> Dict[str, Any]:
        """Video üretim brief'i hazırlar."""
        brief = {
            "topic": topic,
            "target_audience": target_audience,
            "core_promise": f"{topic} konusunu sıfırdan zirveye, sıkıcı olmadan anlatan rehber.",
            "hook_thesis": f"Herkes {topic} hakkında konuşuyor ama asıl can alıcı noktayı kimse fark etmedi.",
            "estimated_length_minutes": 5,
            "recommended_wpm": 160
        }
        brief_path = os.path.join(self.output_dir, "topic_brief.json")
        with open(brief_path, "w", encoding="utf-8") as f:
            json.dump(brief, f, indent=2, ensure_ascii=False)
        print(f"[+] Brief kaydedildi: {brief_path}")
        return brief
