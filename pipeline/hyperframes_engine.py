"""
Hyperframes HTML/CSS/GSAP Motion Engine
Generates dynamic HTML/CSS overlays inspired by heygen-com/hyperframes.
"""

import os
from typing import Dict, Any


class HyperframesEngine:
    def __init__(self, output_dir: str = "assets/hyperframes"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_metric_card(self, title: str, subtitle: str, metric_value: str, filename: str = "card_1.html") -> str:
        """HTML + Tailwind + GSAP animasyonlu kart üretir."""
        html_content = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <style>
    body {{ background: transparent; overflow: hidden; width: 1920px; height: 1080px; }}
  </style>
</head>
<body class="flex items-center justify-center">
  <div id="statCard" class="bg-slate-900/95 border-2 border-cyan-400 p-12 rounded-3xl shadow-2xl backdrop-blur-md flex flex-col items-center gap-6 max-w-2xl transform scale-50 opacity-0">
    <span class="text-cyan-400 font-mono tracking-widest text-2xl uppercase font-bold">{title}</span>
    <div class="text-8xl font-black text-white">{metric_value}</div>
    <p class="text-2xl text-slate-300 text-center">{subtitle}</p>
  </div>
  <script>
    gsap.to("#statCard", {{
      opacity: 1,
      scale: 1,
      duration: 0.9,
      ease: "back.out(1.5)"
    }});
  </script>
</body>
</html>"""
        file_path = os.path.join(self.output_dir, filename)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[+] Hyperframes kartı oluşturuldu: {file_path}")
        return file_path
