"""
OpenVoice V2 isteğe bağlı kurulum (ses klonlama / ton rengi dönüştürme).

Yapılanlar:
  1. myshell-ai/OpenVoice -> vendor/OpenVoice (git clone)
  2. pip install -e vendor/OpenVoice
  3. V2 checkpoint'leri (~120 MB) -> vendor/OpenVoice/checkpoints_v2/
  4. config/voice/ klasörü (reference.wav buraya konur)

MeloTTS kurulmaz: stüdyo Türkçe sesi Edge-TTS ile üretir, OpenVoice yalnızca tınıyı dönüştürür.

Kullanım:
  python scripts/install_openvoice.py
  python main.py ... --clone-voice
"""

import os
import shutil
import subprocess
import sys
import urllib.request
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VENDOR = os.path.join(ROOT, "vendor", "OpenVoice")
REPO = "https://github.com/myshell-ai/OpenVoice.git"
CKPT_URL = "https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip"
CKPT_DIR = os.path.join(VENDOR, "checkpoints_v2")


for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def run(cmd):
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> None:
    if not shutil.which("git"):
        sys.exit("git bulunamadı.")
    if not os.path.isdir(VENDOR):
        os.makedirs(os.path.dirname(VENDOR), exist_ok=True)
        run(["git", "clone", "--depth", "1", REPO, VENDOR])
    else:
        print(f"[=] Zaten var: {VENDOR}")

    run([sys.executable, "-m", "pip", "install", "-e", VENDOR])

    conv = os.path.join(CKPT_DIR, "converter", "checkpoint.pth")
    if not os.path.isfile(conv):
        zip_path = os.path.join(VENDOR, "checkpoints_v2.zip")
        print(f"[*] Checkpoint indiriliyor: {CKPT_URL}")
        urllib.request.urlretrieve(CKPT_URL, zip_path)
        with zipfile.ZipFile(zip_path) as z:
            z.extractall(VENDOR)  # zip içinde checkpoints_v2/ klasörü var
        os.remove(zip_path)
    if not os.path.isfile(conv):
        sys.exit(f"Checkpoint bulunamadı: {conv}")

    voice_dir = os.path.join(ROOT, "config", "voice")
    os.makedirs(voice_dir, exist_ok=True)
    print("\n[✓] OpenVoice V2 hazır.")
    print(f"    Referans sesi koy: {os.path.join(voice_dir, 'reference.wav')} (10–30 sn, tek konuşmacı, temiz;")
    print("    yalnızca izni alınmış bir ses).")
    print("    Sonra: python main.py ... --clone-voice")


if __name__ == "__main__":
    main()
