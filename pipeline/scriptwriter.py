"""
Script Engine — senaryo dosyasını okur, AI slop denetiminden geçirir, sahne listesine çevirir.

Senaryo yazımı ajan tarafından skill'lerle yapılır (skills/02-scriptwriting-&-lore):
creative-fiction → script-engine → turkish-literary-script-doctor → no-ai-slop.
Bu modül sabit şablon üretmez; senaryo yoksa hata verir.

Senaryo biçimi (Markdown):
  ## Sahne 1 — Başlık
  **Ses:**
  anlatım metni...
  **Görsel:** görsel tarifi
"""

import json
import os
import re
from typing import Any, Dict, List

BANNED_CLICHES = [
    # İngilizce (petergyang/no-ai-slop kapsamındaki yaygın kalıplar)
    r"in today's (fast-paced|digital) world", r"let's dive (right )?in", r"game[- ]changer",
    r"without further ado", r"testament to", r"tapestry", r"in conclusion", r"to sum up", r"delve into",
    # Türkçe (skills/08-qa-security-audit/no-ai-slop/turkish-patterns.md)
    r"gelin (birlikte )?yakından bakalım", r"hadi başlayalım", r"günümüz dünyasında", r"dijital çağ",
    r"şüphesiz ki", r"unutmamak gerekir ki", r"özetle söylemek gerekirse", r"sonuç olarak",
    r"bir yolculuğa çıkıyoruz", r"oyunun kurallarını değiştir", r"bir kanıtıdır", r"dünyasına dalalım",
]


def find_slop(text: str) -> List[str]:
    return [p for p in BANNED_CLICHES if re.search(p, text, re.IGNORECASE)]


def load_script_md(path: str) -> List[Dict[str, Any]]:
    """`## Sahne` başlıklı Markdown senaryoyu sahne listesine çevirir."""
    with open(path, encoding="utf-8") as f:
        txt = f.read()
    scenes = []
    for block in re.split(r"^## ", txt, flags=re.M)[1:]:
        title = block.splitlines()[0].strip()
        speech = re.search(r"\*\*Ses:\*\*\s*(.*?)(?=\*\*Görsel|\Z)", block, re.S)
        visual = re.search(r"\*\*Görsel:\*\*\s*(.*?)(?=\n## |\Z)", block, re.S)
        if not speech:
            continue
        scenes.append({
            "scene_id": len(scenes) + 1,
            "title": title,
            "speech_text": re.sub(r"\s+", " ", speech.group(1)).strip(),
            "visual_prompt": re.sub(r"\s+", " ", visual.group(1)).strip() if visual else "",
        })
    if not scenes:
        raise ValueError(f"Senaryoda '## Sahne' + '**Ses:**' bloğu bulunamadı: {path}")
    return scenes


class AntiSlopScriptwriter:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def validate_anti_slop(self, text: str) -> List[str]:
        return find_slop(text)

    def build_script(self, topic: str, script_path: str) -> Dict[str, Any]:
        """Senaryo dosyasını okur, slop denetler, script.json yazar."""
        if not script_path or not os.path.isfile(script_path):
            raise FileNotFoundError(
                f"Senaryo dosyası yok: {script_path}. Önce senaryoyu yaz (skills/02-scriptwriting-&-lore).")
        scenes = load_script_md(script_path)
        violations = self.validate_anti_slop(" ".join(s["speech_text"] for s in scenes))
        if violations:
            raise ValueError(f"AI slop tespit edildi, senaryoyu düzelt: {violations}")
        words = sum(len(s["speech_text"].split()) for s in scenes)
        data = {"topic": topic, "total_scenes": len(scenes), "word_count": words, "scenes": scenes}
        out = os.path.join(self.output_dir, "script.json")
        with open(out, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"[+] Senaryo onaylandı: {len(scenes)} sahne, {words} kelime -> {out}")
        return data
