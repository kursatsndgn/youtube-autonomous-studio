"""
Stüdyo skill'lerini Claude Code'un bulabileceği yere kurar.

Claude Code skill'leri `<kök>/<skill-adı>/SKILL.md` biçiminde (tek seviye) arar; repodaki departman
klasörleri (skills/01-…/<skill>/) bu yüzden doğrudan görünmez. Bu script her skill klasörünü kopyalar.

  python scripts/install_skills.py            # proje: ./.claude/skills/ (git dışı)
  python scripts/install_skills.py --user     # kullanıcı: ~/.claude/skills/
  python scripts/install_skills.py --check    # sadece listele ve doğrula

Aynı adlı başka bir skill varsa (stüdyoya ait değilse) üzerine yazmaz, uyarır.
"""

import argparse
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(ROOT, "skills")
MARK = ".studio-skill"


for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except Exception:
        pass


def find_skills():
    out = []
    for dirpath, _, files in os.walk(SKILLS):
        if "SKILL.md" in files:
            with open(os.path.join(dirpath, "SKILL.md"), encoding="utf-8") as f:
                head = f.read(4000)
            m = re.match(r"---\n(.*?)\n---", head, re.S)
            name = re.search(r"^name:\s*(.+)$", m.group(1), re.M) if m else None
            desc = re.search(r"^description:\s*\S", m.group(1), re.M) if m else None
            out.append((dirpath, name.group(1).strip().strip('"') if name else None, bool(desc)))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user", action="store_true", help="~/.claude/skills altına kur")
    ap.add_argument("--check", action="store_true", help="yalnızca doğrula")
    a = ap.parse_args()

    skills = find_skills()
    bad = [(d, n) for d, n, ok in skills if not n or not ok or n != os.path.basename(d)]
    for d, n in bad:
        print(f"✗ geçersiz frontmatter / ad uyuşmazlığı: {os.path.relpath(d, ROOT)} (name={n})")
    if a.check or bad:
        print(f"{len(skills)} skill bulundu, {len(bad)} sorunlu.")
        sys.exit(1 if bad else 0)

    target = os.path.expanduser("~/.claude/skills") if a.user else os.path.join(ROOT, ".claude", "skills")
    os.makedirs(target, exist_ok=True)
    for src, name, _ in skills:
        dst = os.path.join(target, name)
        if os.path.exists(dst) and not os.path.exists(os.path.join(dst, MARK)):
            print(f"! atlandı (aynı adda başka skill var): {dst}")
            continue
        shutil.rmtree(dst, ignore_errors=True)
        shutil.copytree(src, dst)
        open(os.path.join(dst, MARK), "w").close()
        print(f"✓ {name}")
    print(f"\n{len(skills)} skill -> {target}. Claude Code'u yeniden başlat.")


if __name__ == "__main__":
    main()
