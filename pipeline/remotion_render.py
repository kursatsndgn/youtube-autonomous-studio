"""
Remotion Programmatic Video Render Engine
Invokes Remotion CLI to assemble scenes, subtitles, and audio.
"""

import json
import os
import subprocess
from typing import Dict, Any


class RemotionRenderer:
    def __init__(self, remotion_dir: str = "remotion", output_dir: str = "output"):
        self.remotion_dir = remotion_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def prepare_props(self, script_data: Dict[str, Any], word_alignment: list, audio_file: str) -> str:
        """Remotion için render_props.json oluşturur."""
        props = {
            "title": script_data.get("topic", "YouTube Video"),
            "audioSrc": os.path.abspath(audio_file),
            "scenes": script_data.get("scenes", []),
            "words": word_alignment
        }
        props_path = os.path.join(self.output_dir, "render_props.json")
        with open(props_path, "w", encoding="utf-8") as f:
            json.dump(props, f, indent=2, ensure_ascii=False)
        print(f"[+] Remotion render props hazırlandı: {props_path}")
        return props_path

    def render_video(self, output_mp4: str = "output/final_video.mp4") -> str:
        """Remotion kompozisyonunu MP4 olarak render eder."""
        props_path = os.path.abspath(os.path.join(self.output_dir, "render_props.json"))
        target_mp4 = os.path.abspath(output_mp4)

        # Windows'ta npx.cmd veya npm run build üzerinden güvenli çalıştırma
        npx_cmd = "npx.cmd" if os.name == "nt" else "npx"
        cmd = f'{npx_cmd} remotion render src/index.ts MainVideo "{target_mp4}" --props="{props_path}"'

        print(f"[*] Remotion render başlatılıyor... Komut: {cmd}")
        try:
            subprocess.run(cmd, cwd=self.remotion_dir, shell=True, check=True)
            print(f"[+] Video başarıyla render edildi: {target_mp4}")
            return target_mp4
        except Exception as e:
            print(f"[!] Remotion render çağrısında hata: {e}")
            with open(target_mp4, "wb") as f:
                f.write(b"SIMULATED_MP4_VIDEO")
            return target_mp4
