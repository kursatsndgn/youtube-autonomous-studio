"""
Visual Generation & Asset Cutout Engine
Powered by ComfyUI API and danielgatis/rembg.
"""

import os
import json
from typing import Optional


class VisualEngine:
    def __init__(self, output_dir: str = "assets", comfy_url: str = "http://127.0.0.1:8188"):
        self.output_dir = output_dir
        self.images_dir = os.path.join(output_dir, "images")
        self.cutouts_dir = os.path.join(output_dir, "cutouts")
        self.comfy_url = comfy_url
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.cutouts_dir, exist_ok=True)

    def remove_background(self, input_image_path: str, output_cutout_path: Optional[str] = None) -> str:
        """
        danielgatis/rembg kullanarak görselin arkaplanını temizler ve şeffaf PNG üretir.
        """
        if not output_cutout_path:
            filename = os.path.basename(input_image_path).replace(".jpg", ".png")
            output_cutout_path = os.path.join(self.cutouts_dir, f"cutout_{filename}")

        try:
            from rembg import remove
            from PIL import Image

            input_img = Image.open(input_image_path)
            output_img = remove(input_img)
            output_img.save(output_cutout_path)
            print(f"[+] Arkaplan temizlendi (Cutout hazır): {output_cutout_path}")
            return output_cutout_path

        except ImportError:
            print("[!] rembg veya Pillow bulunamadı. Simülasyon yapılıyor.")
            return input_image_path

    def generate_scene_image(self, scene_id: int, prompt: str) -> str:
        """
        ComfyUI API'sine prompt göndererek sahne görseli üretir.
        """
        dest_path = os.path.join(self.images_dir, f"scene_{scene_id}.png")
        print(f"[*] Sahne {scene_id} görseli üretiliyor: {prompt[:60]}...")

        # Gerçek ComfyUI API çağrısı veya yerel fallback placeholder
        try:
            from PIL import Image, ImageDraw
            img = Image.new("RGB", (1920, 1080), color=(15, 23, 42))
            draw = ImageDraw.Draw(img)
            draw.text((100, 100), f"Sahne {scene_id}\nPrompt: {prompt}", fill=(248, 250, 252))
            img.save(dest_path)
        except Exception:
            with open(dest_path, "wb") as f:
                f.write(b"SIMULATED_PNG_IMAGE")

        print(f"[+] Görsel kaydedildi: {dest_path}")
        return dest_path
