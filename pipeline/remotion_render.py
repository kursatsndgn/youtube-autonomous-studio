"""
Remotion render motoru: sesi remotion/public/_pipeline/ altına kopyalar, props yazar, kompozisyonu render eder.
Render başarısız olursa hata verir (sahte MP4 yazmaz).
"""

import json
import os
import shutil
import subprocess
from typing import Any, Dict, List


class RemotionRenderer:
    def __init__(self, remotion_dir: str = "remotion", output_dir: str = "output"):
        self.remotion_dir = remotion_dir
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def prepare_props(self, script_data: Dict[str, Any], word_alignment: List[Dict[str, Any]],
                      audio_file: str) -> str:
        pub = os.path.join(self.remotion_dir, "public", "_pipeline")
        os.makedirs(pub, exist_ok=True)
        audio_name = "voiceover" + os.path.splitext(audio_file)[1]
        shutil.copyfile(audio_file, os.path.join(pub, audio_name))
        words = [{"word": w.get("w", w.get("word")), "start": w.get("s", w.get("start")),
                  "end": w.get("e", w.get("end"))} for w in word_alignment]
        props = {
            "title": script_data.get("topic", ""),
            "audio": f"_pipeline/{audio_name}",
            "durationSec": (words[-1]["end"] + 1.5) if words else 10,
            "scenes": script_data.get("scenes", []),
            "words": words,
        }
        path = os.path.join(self.output_dir, "render_props.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(props, f, indent=2, ensure_ascii=False)
        return path

    def render_video(self, output_mp4: str, composition: str = "MainVideo") -> str:
        props = os.path.abspath(os.path.join(self.output_dir, "render_props.json"))
        target = os.path.abspath(output_mp4)
        npx = "npx.cmd" if os.name == "nt" else "npx"
        cmd = [npx, "remotion", "render", "src/index.ts", composition, target, f"--props={props}"]
        print(f"[*] Remotion render: {composition} -> {target}")
        try:
            subprocess.run(cmd, cwd=self.remotion_dir, check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Remotion render başarısız: {e}") from e
        return target
