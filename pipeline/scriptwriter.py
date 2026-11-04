"""
Anti-Slop & ADHD Pacing Scriptwriter Engine
Enforces No-AI-Slop, High-Retention Hooks, and Scene-by-Scene structure.
"""

import json
import os
import re
from typing import Dict, List, Any

BANNED_CLICHES = [
    r"in today's (fast-paced|digital) world",
    r"let's dive (right )?in",
    r"game-changer",
    r"revolutionary",
    r"without further ado",
    r"testament to",
    r"tapestry",
    r"in conclusion",
    r"to sum up",
    r"delve into"
]


class AntiSlopScriptwriter:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def validate_anti_slop(self, text: str) -> List[str]:
        """Senaryodaki yapay zeka klişelerini tespit eder."""
        violations = []
        for pattern in BANNED_CLICHES:
            if re.search(pattern, text, re.IGNORECASE):
                violations.append(pattern)
        return violations

    def build_script(self, topic: str, raw_scenes: List[Dict[str, str]] = None) -> Dict[str, Any]:
        """
        Anti-slop kurallarına uygun, dinamik sahneler oluşturur.
        """
        if not raw_scenes:
            # Örnek yüksek kancalı senaryo şablonu
            raw_scenes = [
                {
                    "scene_id": 1,
                    "speech_text": f"Son bir ayda {topic} hakkında duyduğunuz neredeyse her şey yanıltıcıydı. Çünkü arka plandaki gerçek oyun bambaşka.",
                    "visual_prompt": f"Dramatic cinematic shot representing {topic}, dark moody neon cyan atmosphere, 8k resolution",
                    "overlay_text": "BÜYÜK YANILGI",
                    "pacing": "fast"
                },
                {
                    "scene_id": 2,
                    "speech_text": "Birçoğumuz eski yöntemlerle saatlerce vakit kaybediyoruz. Oysa yeni nesil otonom araçlar süreci dakikalara indirdi.",
                    "visual_prompt": "Split screen comparison: slow vintage computer vs ultra high-speed modern digital pipeline",
                    "overlay_text": "10X HIZ FARKI",
                    "pacing": "medium"
                },
                {
                    "scene_id": 3,
                    "speech_text": "İşte tam olarak bu yüzden şimdi göreceğiniz 3 adımı hemen iş akışınıza eklemeniz gerekiyor. İlk adımla başlayalım.",
                    "visual_prompt": "Step 1 holographic glowing banner in a high-tech modern studio, clean minimalism",
                    "overlay_text": "ADIM 1: BAŞLANGIÇ",
                    "pacing": "fast"
                }
            ]

        # Slop denetimi
        all_speech = " ".join([s["speech_text"] for s in raw_scenes])
        violations = self.validate_anti_slop(all_speech)
        if violations:
            raise ValueError(f"AI Slop tespit edildi: {violations}")

        script_data = {
            "topic": topic,
            "total_scenes": len(raw_scenes),
            "scenes": raw_scenes
        }

        output_path = os.path.join(self.output_dir, "script.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(script_data, f, indent=2, ensure_ascii=False)

        print(f"[+] Anti-Slop Senaryo onaylandı ve kaydedildi: {output_path}")
        return script_data
