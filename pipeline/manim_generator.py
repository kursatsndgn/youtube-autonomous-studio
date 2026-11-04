"""
Manim Scientific & Mathematical Animation Generator
Powered by manimCommunity/manim.
"""

import os
import subprocess
from typing import Optional


class ManimGenerator:
    def __init__(self, output_dir: str = "assets/manim"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_chart_scene(self, title: str = "Performans Artışı") -> str:
        """Manim sahne Python kodu oluşturur ve render komutunu hazırlar."""
        script_path = os.path.join(self.output_dir, "scene.py")
        code = f'''from manim import *

class ChartScene(Scene):
    def construct(self):
        title = Text("{title}", font_size=42, color=YELLOW).to_edge(UP)
        axes = Axes(x_range=[0, 5, 1], y_range=[0, 10, 2], axis_config={{"color": BLUE}})
        curve = axes.plot(lambda x: 0.4 * x**2, color=GREEN)
        self.play(Write(title))
        self.play(Create(axes), Create(curve), run_time=1.5)
        self.wait(1)
'''
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(code)

        print(f"[+] Manim sahnesi hazırlandı: {script_path}")
        return script_path
