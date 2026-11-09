"""
Visual Pipeline: stok (Pexels/Pixabay) → AI görsel (ComfyUI) → rembg cutout.

Kodla çizilen sahne türleri (stat_card, timeline, diagram, map, quote_card, code) Remotion'da üretilir;
bu modül fotoğraf/illüstrasyon gerektiren sahneler içindir.
Hiçbir kaynak sonuç vermezse VisualSourceError fırlatır — placeholder görsel üretmez.

Ortam değişkenleri: PEXELS_API_KEY, PIXABAY_API_KEY, COMFYUI_URL, COMFYUI_CHECKPOINT, COMFYUI_LORA
"""

import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional

import requests

STYLE_PRESETS = {
    "cartoon": {
        "positive": "flat 2d cartoon illustration, thick black outlines, flat colors, simple shading, "
                    "expressive characters, clean background, explainer video style",
        "negative": "photorealistic, 3d render, gradient mesh, text, watermark, signature, extra limbs, "
                    "deformed hands, blurry, lowres",
    },
    "cinematic": {
        "positive": "cinematic still, natural key light, soft shadows, 35mm lens, shallow depth of field, "
                    "muted color grade, historically accurate",
        "negative": "oversaturated, neon, cartoonish, text, watermark, extra limbs, deformed, blurry, lowres",
    },
}


class VisualSourceError(RuntimeError):
    pass


class VisualEngine:
    def __init__(self, output_dir: str = "assets", style: str = "cartoon"):
        self.output_dir = output_dir
        self.images_dir = os.path.join(output_dir, "images")
        self.cutouts_dir = os.path.join(output_dir, "cutouts")
        self.credits_path = os.path.join(output_dir, "credits.json")
        self.style = style
        self.comfy_url = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188")
        self.checkpoint = os.environ.get("COMFYUI_CHECKPOINT", "v1-5-pruned-emaonly.safetensors")
        self.lora = os.environ.get("COMFYUI_LORA")  # örn. "flat_cartoon_style.safetensors"
        os.makedirs(self.images_dir, exist_ok=True)
        os.makedirs(self.cutouts_dir, exist_ok=True)

    # ------------------------------------------------------------------ ana giriş
    def generate_scene_image(self, scene_id: int, prompt: str, stock_query: Optional[str] = None,
                             sources: List[str] = ("pexels", "pixabay", "comfyui")) -> str:
        """Sırayla kaynakları dener; ilk başarılı görselin yolunu döndürür."""
        errors = []
        for src in sources:
            try:
                if src in ("pexels", "pixabay"):
                    q = stock_query or prompt
                    path = getattr(self, f"_{src}")(scene_id, q)
                else:
                    path = self.comfyui_txt2img(scene_id, prompt)
                print(f"[+] Sahne {scene_id} görseli ({src}): {path}")
                return path
            except Exception as e:  # sıradaki kaynağa geç
                errors.append(f"{src}: {e}")
        raise VisualSourceError(f"Sahne {scene_id} için görsel bulunamadı/üretilemedi -> " + " | ".join(errors))

    # ------------------------------------------------------------------ stok
    def _download(self, url: str, dest: str, headers: Optional[Dict[str, str]] = None) -> str:
        r = requests.get(url, headers=headers or {}, timeout=60)
        r.raise_for_status()
        with open(dest, "wb") as f:
            f.write(r.content)
        return dest

    def _credit(self, scene_id: int, entry: Dict[str, Any]) -> None:
        data = {}
        if os.path.exists(self.credits_path):
            with open(self.credits_path, encoding="utf-8") as f:
                data = json.load(f)
        data[str(scene_id)] = entry
        with open(self.credits_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _pexels(self, scene_id: int, query: str) -> str:
        key = os.environ.get("PEXELS_API_KEY")
        if not key:
            raise VisualSourceError("PEXELS_API_KEY yok")
        r = requests.get("https://api.pexels.com/v1/search", headers={"Authorization": key},
                         params={"query": query, "per_page": 1, "orientation": "landscape"}, timeout=30)
        r.raise_for_status()
        photos = r.json().get("photos", [])
        if not photos:
            raise VisualSourceError("sonuç yok")
        p = photos[0]
        dest = self._download(p["src"]["large2x"], os.path.join(self.images_dir, f"scene_{scene_id}.jpg"))
        self._credit(scene_id, {"source": "Pexels", "author": p.get("photographer"), "url": p.get("url")})
        return dest

    def _pixabay(self, scene_id: int, query: str) -> str:
        key = os.environ.get("PIXABAY_API_KEY")
        if not key:
            raise VisualSourceError("PIXABAY_API_KEY yok")
        r = requests.get("https://pixabay.com/api/", params={
            "key": key, "q": query[:100], "image_type": "photo", "orientation": "horizontal",
            "per_page": 3, "safesearch": "true"}, timeout=30)
        r.raise_for_status()
        hits = r.json().get("hits", [])
        if not hits:
            raise VisualSourceError("sonuç yok")
        h = hits[0]
        dest = self._download(h["largeImageURL"], os.path.join(self.images_dir, f"scene_{scene_id}.jpg"))
        self._credit(scene_id, {"source": "Pixabay", "author": h.get("user"), "url": h.get("pageURL")})
        return dest

    # ------------------------------------------------------------------ ComfyUI
    def _workflow(self, prompt: str, seed: int, width: int, height: int) -> Dict[str, Any]:
        style = STYLE_PRESETS[self.style]
        model_src, clip_src = ["1", 0], ["1", 1]
        wf: Dict[str, Any] = {
            "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": self.checkpoint}},
        }
        if self.lora:
            wf["8"] = {"class_type": "LoraLoader", "inputs": {
                "model": ["1", 0], "clip": ["1", 1], "lora_name": self.lora,
                "strength_model": 0.8, "strength_clip": 0.8}}
            model_src, clip_src = ["8", 0], ["8", 1]
        wf.update({
            "2": {"class_type": "CLIPTextEncode", "inputs": {"clip": clip_src, "text": f"{prompt}, {style['positive']}"}},
            "3": {"class_type": "CLIPTextEncode", "inputs": {"clip": clip_src, "text": style["negative"]}},
            "4": {"class_type": "EmptyLatentImage", "inputs": {"width": width, "height": height, "batch_size": 1}},
            "5": {"class_type": "KSampler", "inputs": {
                "model": model_src, "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0],
                "seed": seed, "steps": 25, "cfg": 7.0, "sampler_name": "dpmpp_2m", "scheduler": "karras",
                "denoise": 1.0}},
            "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
            "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": "studio"}},
        })
        return wf

    def comfyui_txt2img(self, scene_id: int, prompt: str, seed: Optional[int] = None,
                        width: int = 768, height: int = 432, timeout: int = 600) -> str:
        """4 GB VRAM için varsayılan 768x432 (SD 1.5). Upscale Remotion/ffmpeg tarafında yapılır."""
        try:
            requests.get(self.comfy_url, timeout=3)
        except requests.RequestException as e:
            raise VisualSourceError(f"ComfyUI erişilemiyor ({self.comfy_url})") from e
        seed = seed if seed is not None else 1000 + scene_id
        r = requests.post(f"{self.comfy_url}/prompt", json={
            "prompt": self._workflow(prompt, seed, width, height), "client_id": str(uuid.uuid4())}, timeout=30)
        r.raise_for_status()
        pid = r.json()["prompt_id"]
        t0 = time.time()
        while time.time() - t0 < timeout:
            hist = requests.get(f"{self.comfy_url}/history/{pid}", timeout=30).json()
            if pid in hist:
                for out in hist[pid]["outputs"].values():
                    for img in out.get("images", []):
                        dest = os.path.join(self.images_dir, f"scene_{scene_id}.png")
                        self._download(f"{self.comfy_url}/view?filename={img['filename']}"
                                       f"&subfolder={img.get('subfolder', '')}&type={img.get('type', 'output')}", dest)
                        self._credit(scene_id, {"source": "ComfyUI", "checkpoint": self.checkpoint,
                                                "lora": self.lora, "seed": seed, "prompt": prompt})
                        return dest
                raise VisualSourceError("ComfyUI çıktı görseli döndürmedi")
            time.sleep(2)
        raise VisualSourceError("ComfyUI zaman aşımı")

    # ------------------------------------------------------------------ rembg
    def remove_background(self, input_image_path: str, output_cutout_path: Optional[str] = None) -> str:
        """rembg ile şeffaf PNG cutout (karakter tutarlılığı ve thumbnail için)."""
        from rembg import remove  # yoksa ImportError -> çağıran karar verir
        from PIL import Image

        if not output_cutout_path:
            base = os.path.splitext(os.path.basename(input_image_path))[0]
            output_cutout_path = os.path.join(self.cutouts_dir, f"cutout_{base}.png")
        remove(Image.open(input_image_path)).save(output_cutout_path)
        print(f"[+] Cutout hazır: {output_cutout_path}")
        return output_cutout_path
