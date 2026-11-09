"""
Thumbnail Engine — 1280x720 yüksek CTR kapak üreticisi (Pillow + rembg).

Kurallar (skills/06-thumbnail-designer/thumbnail-engine):
  - En fazla 3 öğe: odak figür (cutout) + zıt renk arka plan + <= 4 kelime dev metin
  - Sağ alt köşe (YouTube süre rozeti) boş
  - Metin yüksekliği >= görsel yüksekliğinin %18'i, tek vurgulu kelime
  - Figüre açık kontur + gölge

Kullanım:
  python pipeline/thumbnail_engine.py --bg kare.png --figure karakter.png --text "DÖRT KELİMELİK BAŞLIK" \
      --accent "BAŞLIK" --out output/konu/thumbnail
"""

import argparse
import os
from typing import List, Optional, Tuple

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

W, H = 1280, 720
SAFE_BR = (W - 200, H - 80)  # sağ alt süre rozeti alanı başlangıcı
FONT_CANDIDATES = [
    "C:/Windows/Fonts/impact.ttf", "C:/Windows/Fonts/arialbd.ttf", "C:/Windows/Fonts/segoeuib.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
PALETTES = {  # (arka plan koyulaştırma rengi, vurgu rengi)
    "a": ((20, 14, 10), (230, 170, 40)),
    "b": ((12, 22, 40), (255, 90, 60)),
    "c": ((30, 10, 10), (255, 220, 80)),
}


def _font(size: int) -> ImageFont.FreeTypeFont:
    for p in FONT_CANDIDATES:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    raise FileNotFoundError("Kalın bir TTF font bulunamadı (FONT_CANDIDATES).")


def _cover(img: Image.Image) -> Image.Image:
    return ImageOps.fit(img.convert("RGB"), (W, H), Image.LANCZOS)


def _background(bg_path: Optional[str], tint: Tuple[int, int, int]) -> Image.Image:
    if bg_path:
        bg = _cover(Image.open(bg_path)).filter(ImageFilter.GaussianBlur(6))
        bg = ImageEnhance.Brightness(bg).enhance(0.55)
        overlay = Image.new("RGB", (W, H), tint)
        return Image.blend(bg, overlay, 0.35)
    # düz renk + radyal parlama
    bg = Image.new("RGB", (W, H), tint)
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((W * 0.35, -H * 0.3, W * 1.3, H * 1.1), fill=90)
    return Image.composite(Image.new("RGB", (W, H), tuple(min(255, c + 60) for c in tint)), bg,
                           glow.filter(ImageFilter.GaussianBlur(120)))


def _figure(fig_path: str, cutout: bool) -> Image.Image:
    fig = Image.open(fig_path).convert("RGBA")
    if cutout and (fig.getextrema()[3][0] == 255):  # alfa yoksa rembg ile kes
        from rembg import remove
        fig = remove(fig)
    # yüksekliği %95'e ölçekle
    s = (H * 0.95) / fig.height
    fig = fig.resize((int(fig.width * s), int(fig.height * s)), Image.LANCZOS)
    # açık kontur + gölge
    alpha = fig.split()[3]
    stroke = alpha.filter(ImageFilter.MaxFilter(17))
    out = Image.new("RGBA", fig.size, (0, 0, 0, 0))
    shadow = Image.new("RGBA", fig.size, (0, 0, 0, 160))
    out.paste(shadow, (12, 12), stroke.filter(ImageFilter.GaussianBlur(10)))
    out.paste(Image.new("RGBA", fig.size, (255, 255, 255, 255)), (0, 0), stroke)
    out.alpha_composite(fig)
    return out


def _text_block(draw: ImageDraw.ImageDraw, words: List[str], accent: str, color_accent, box_w: int,
                x0: int, y0: int) -> None:
    lines = [" ".join(words[:2]), " ".join(words[2:4])] if len(words) > 2 else [" ".join(words)]
    size = int(H * 0.2)
    font = _font(size)
    while max(draw.textlength(l, font=font) for l in lines) > box_w and size > 40:
        size -= 4
        font = _font(size)
    y = y0
    for line in lines:
        x = x0
        for wd in line.split():
            col = color_accent if wd.upper() == accent.upper() else (255, 255, 255)
            draw.text((x, y), wd, font=font, fill=col, stroke_width=max(4, size // 14), stroke_fill=(0, 0, 0))
            x += draw.textlength(wd + " ", font=font)
        y += int(size * 1.05)
    if y > SAFE_BR[1] and x0 + box_w > SAFE_BR[0]:
        raise ValueError("Metin sağ alt süre rozeti alanına taşıyor.")


def make_thumbnail(text: str, out_path: str, bg: Optional[str] = None, figure: Optional[str] = None,
                   accent: Optional[str] = None, palette: str = "a", cutout: bool = True) -> str:
    words = text.upper().split()
    if len(words) > 4:
        raise ValueError("Kapak metni en fazla 4 kelime olmalı.")
    tint, acc = PALETTES[palette]
    canvas = _background(bg, tint).convert("RGBA")
    text_w = int(W * 0.58)
    if figure:
        fig = _figure(figure, cutout)
        canvas.alpha_composite(fig, (W - fig.width + int(fig.width * 0.08), H - fig.height))
    else:
        text_w = int(W * 0.85)
    draw = ImageDraw.Draw(canvas)
    _text_block(draw, words, (accent or words[-1]), acc, text_w, 48, 70)
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    canvas.convert("RGB").save(out_path, "JPEG", quality=90, optimize=True)
    if os.path.getsize(out_path) > 2 * 1024 * 1024:
        raise ValueError("Kapak 2 MB sınırını aşıyor.")
    return out_path


def make_variants(text: str, out_prefix: str, **kw) -> List[str]:
    return [make_thumbnail(text, f"{out_prefix}_{p}.jpg", palette=p, **kw) for p in PALETTES]


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", required=True)
    ap.add_argument("--out", required=True, help="çıktı öneki, ör. output/slug/thumbnail")
    ap.add_argument("--bg")
    ap.add_argument("--figure")
    ap.add_argument("--accent")
    ap.add_argument("--no-cutout", action="store_true")
    a = ap.parse_args()
    for p in make_variants(a.text, a.out, bg=a.bg, figure=a.figure, accent=a.accent, cutout=not a.no_cutout):
        print(p)
