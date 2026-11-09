---
name: skill-spector
description: Repodaki skill dosyalarını NVIDIA SkillSpector ile güvenlik ve kötü niyetli kalıp taramasından geçirir. Dışarıdan skill kopyalarken veya yeni skill eklerken kullan.
---

# SkillSpector Denetimi

Kaynak: [NVIDIA/SkillSpector](https://github.com/NVIDIA/SkillSpector) (Apache-2.0). Bir skill'in kurulmasının güvenli olup olmadığını denetler (prompt injection, veri sızdırma, tehlikeli komutlar).

## Kurulum
```bash
uv tool install git+https://github.com/NVIDIA/skillspector.git
```

## Kullanım
```bash
skillspector scan ./skills/
skillspector scan ./skills/02-scriptwriting-&-lore/book-to-skill/ --no-llm --format json --output output/skillspector.json
```

## Kural
- Upstream'den kopyalanan her skill (book-to-skill, no-ai-slop, taste-skill, banner-design) eklenmeden önce taranır.
- Yüksek riskli bulgu varsa skill eklenmez ya da ilgili kısım çıkarılır.
