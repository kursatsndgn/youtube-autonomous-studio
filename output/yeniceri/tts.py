"""Senaryodan sahne bazlı TTS + kelime zamanlaması üretir -> remotion/public/yeniceri/"""
import asyncio, json, re, subprocess, sys
from pathlib import Path
import edge_tts

HERE = Path(__file__).parent
OUT = HERE.parents[1] / "remotion" / "public" / "yeniceri"
OUT.mkdir(parents=True, exist_ok=True)
VOICE, RATE = "tr-TR-AhmetNeural", "-4%"

def scenes():
    txt = (HERE / "senaryo.md").read_text(encoding="utf-8")
    out = []
    for block in re.split(r"^## ", txt, flags=re.M)[1:]:
        title = block.splitlines()[0]
        m = re.search(r"\*\*Ses:\*\*\s*(.*?)\s*\*\*Görsel", block, re.S)
        if m:
            out.append({"title": title, "text": re.sub(r"\s+", " ", m.group(1)).strip()})
    return out

def dur(p):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True)
    return float(r.stdout.strip())

async def main():
    data = []
    for i, s in enumerate(scenes(), 1):
        mp3 = OUT / f"s{i}.mp3"
        words = []
        com = edge_tts.Communicate(s["text"], VOICE, rate=RATE, boundary="WordBoundary")
        with open(mp3, "wb") as f:
            async for ch in com.stream():
                if ch["type"] == "audio":
                    f.write(ch["data"])
                elif ch["type"] == "WordBoundary":
                    words.append({"w": ch["text"], "s": ch["offset"] / 1e7, "e": (ch["offset"] + ch["duration"]) / 1e7})
        d = dur(mp3)
        data.append({"id": i, "title": s["title"], "audio": f"yeniceri/s{i}.mp3", "duration": d, "words": words})
        print(f"s{i} {d:6.1f}s  {s['title']}")
    (OUT / "timeline.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    print("TOPLAM", round(sum(x["duration"] for x in data) / 60, 2), "dk")

asyncio.run(main())
