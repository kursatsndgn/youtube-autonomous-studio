"""
Smart Montage (FFmpeg) — OpenMontage fikirlerinden esinlenilerek sıfırdan yazıldı (kod kopyalanmadı).

Yetenekler:
  1. detect_silences   : ffmpeg silencedetect ile sessiz aralıkları bulur.
  2. jump_cut_audio    : Uzun sessizlikleri kırpar (nefes payı bırakarak), yeni ses dosyası yazar.
  3. remap_words       : Kırpma sonrası kelime zaman damgalarını yeni zaman çizelgesine taşır.
  4. classify_broll    : Her cümleyi B-roll türüne eşler (istatistik kartı, diyagram, harita, illüstrasyon...).
  5. static_shot_plan  : "Hiçbir plan 3.2 sn'den uzun durmaz" kuralına göre görsel değişim noktaları üretir.
  6. detect_static     : Render edilmiş videoda uzun süre donuk kalan bölümleri (freezedetect) bulur.

Kelime formatı: hem {"w","s","e"} hem {"word","start","end"} kabul edilir.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, asdict
from typing import Iterable, List, Dict, Any, Tuple


def _run(cmd: List[str]) -> str:
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise RuntimeError(f"Komut başarısız ({r.returncode}): {' '.join(cmd)}\n{r.stderr[-800:]}")
    return r.stderr + r.stdout


def media_duration(path: str) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
        capture_output=True, text=True, check=True,
    ).stdout.strip()
    return float(out)


# ---------------------------------------------------------------- 1. sessizlik
def detect_silences(audio: str, noise_db: float = -35.0, min_dur: float = 0.35) -> List[Tuple[float, float]]:
    log = _run(["ffmpeg", "-hide_banner", "-nostats", "-i", audio,
                "-af", f"silencedetect=noise={noise_db}dB:d={min_dur}", "-f", "null", "-"])
    starts = [float(x) for x in re.findall(r"silence_start: (-?[\d.]+)", log)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]
    if len(ends) < len(starts):  # dosya sessizlikle bitiyor
        ends.append(media_duration(audio))
    return [(max(0.0, s), e) for s, e in zip(starts, ends)]


# ---------------------------------------------------------------- 2. jump-cut
def keep_segments(silences: List[Tuple[float, float]], total: float, pad: float = 0.12) -> List[Tuple[float, float]]:
    """Sessizliklerin her iki ucunda `pad` kadar nefes payı bırakarak tutulacak aralıkları döndürür."""
    keep, cur = [], 0.0
    for s, e in silences:
        cut_s, cut_e = s + pad, e - pad
        if cut_e - cut_s <= 0.05:
            continue
        if cut_s > cur:
            keep.append((cur, cut_s))
        cur = cut_e
    if cur < total:
        keep.append((cur, total))
    return keep


def jump_cut_audio(audio: str, out_path: str, noise_db: float = -35.0, min_dur: float = 0.35,
                   pad: float = 0.12) -> Dict[str, Any]:
    total = media_duration(audio)
    sil = detect_silences(audio, noise_db, min_dur)
    keep = keep_segments(sil, total, pad)
    expr = "+".join(f"between(t,{a:.3f},{b:.3f})" for a, b in keep) or "1"
    _run(["ffmpeg", "-y", "-hide_banner", "-i", audio,
          "-af", f"aselect='{expr}',asetpts=N/SR/TB", out_path])
    new_total = sum(b - a for a, b in keep)
    return {"input": audio, "output": out_path, "segments": keep,
            "removed_seconds": round(total - new_total, 2), "new_duration": round(new_total, 2)}


def _w(word: Dict[str, Any]) -> Tuple[str, float, float]:
    return (word.get("w") or word.get("word", ""), float(word.get("s", word.get("start", 0))),
            float(word.get("e", word.get("end", 0))))


def remap_time(t: float, keep: List[Tuple[float, float]]) -> float:
    acc = 0.0
    for a, b in keep:
        if t < a:
            return acc
        if t <= b:
            return acc + (t - a)
        acc += b - a
    return acc


def remap_words(words: Iterable[Dict[str, Any]], keep: List[Tuple[float, float]]) -> List[Dict[str, Any]]:
    out = []
    for w in words:
        text, s, e = _w(w)
        out.append({"w": text, "s": round(remap_time(s, keep), 3), "e": round(remap_time(e, keep), 3)})
    return out


# ---------------------------------------------------------------- 4. B-roll eşleme
BROLL_RULES = [
    ("timeline",    r"\b(1[0-9]{3}\b|yüzyıl|yılında|tarih(te|inde))"),
    ("stat_card",   r"\d|yüzde|%|milyon|bin\b|sayı|oran|kat\b|maaş|akçe|ulufe"),
    ("map",         r"\b(rumeli|anadolu|balkan|istanbul|edirne|bosna|sınır|bölge|harita|yol)\w*"),
    ("diagram",     r"\b(rütbe|basamak|hiyerarşi|sistem|süreç|adım|aşama|merdiven|piramit|orta)\w*"),
    ("code",        r"\b(kod|yazılım|api|fonksiyon|algoritma|script)\w*"),
    ("quote_card",  r"[\"“”«»]"),
]


@dataclass
class BrollCue:
    sentence: str
    kind: str
    start: float | None = None
    end: float | None = None


def split_sentences(text: str) -> List[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?…])\s+", text) if s.strip()]


def classify_broll(text: str, words: List[Dict[str, Any]] | None = None) -> List[Dict[str, Any]]:
    """Her cümle için bir B-roll türü önerir; kelime zamanları verilirse cümleye zaman atar."""
    cues: List[BrollCue] = []
    for sent in split_sentences(text):
        low = sent.lower()
        kind = next((k for k, pat in BROLL_RULES if re.search(pat, low)), "illustration")
        cues.append(BrollCue(sent, kind))
    if words:
        idx = 0
        flat = [_w(w) for w in words]
        for cue in cues:
            n = len(cue.sentence.split())
            if idx >= len(flat):
                break
            seg = flat[idx: idx + n]
            cue.start, cue.end = seg[0][1], seg[-1][2]
            idx += n
    return [asdict(c) for c in cues]


# ---------------------------------------------------------------- 5. ritim
def static_shot_plan(duration: float, max_static: float = 3.2,
                     anchor_times: Iterable[float] = ()) -> List[Dict[str, Any]]:
    """Önemli anlara (anchor) ve en fazla `max_static` aralıklara görsel değişim noktası koyar.
    Değişim türleri sırayla döner: punch-in zoom, pan, overlay."""
    anchors = sorted(t for t in anchor_times if 0 < t < duration)
    points, t, i = [], 0.0, 0
    kinds = ["punch_in", "pan", "overlay"]
    for a in anchors + [duration]:
        while a - t > max_static:
            t += max_static
            points.append({"t": round(t, 2), "kind": kinds[i % 3]}); i += 1
        if a < duration:
            t = a
            points.append({"t": round(a, 2), "kind": "cut"})
    return points


# ---------------------------------------------------------------- 6. donuk sahne denetimi
def detect_static(video: str, max_static: float = 4.0, noise: float = 0.001) -> List[Tuple[float, float]]:
    log = _run(["ffmpeg", "-hide_banner", "-nostats", "-i", video,
                "-vf", f"freezedetect=n={noise}:d={max_static}", "-map", "0:v:0", "-f", "null", "-"])
    s = [float(x) for x in re.findall(r"freeze_start: ([\d.]+)", log)]
    e = [float(x) for x in re.findall(r"freeze_end: ([\d.]+)", log)]
    if len(e) < len(s):
        e.append(media_duration(video))
    return list(zip(s, e))


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Smart Montage araçları")
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("silences"); a.add_argument("audio")
    b = sub.add_parser("jumpcut"); b.add_argument("audio"); b.add_argument("out")
    c = sub.add_parser("broll"); c.add_argument("text_file")
    d = sub.add_parser("static"); d.add_argument("video"); d.add_argument("--max", type=float, default=4.0)
    args = p.parse_args()
    if args.cmd == "silences":
        res = detect_silences(args.audio)
    elif args.cmd == "jumpcut":
        res = jump_cut_audio(args.audio, args.out)
    elif args.cmd == "broll":
        res = classify_broll(open(args.text_file, encoding="utf-8").read())
    else:
        res = detect_static(args.video, args.max)
    print(json.dumps(res, ensure_ascii=False, indent=2))
