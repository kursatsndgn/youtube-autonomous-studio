---
name: creative-fiction
description: Belgesel ve video-deneme senaryolarına derin hikâye yapısı kazandırır — kişileştirilmiş anlatıcı/karakter yayı, dramatik anlar, dünya (kurum, inanç, ekonomi) anlatımı, klişe kırma ve güçlü final. jwynia/agent-skills creative paketini video senaryosu için yönlendirir.
---

# Creative Fiction — Belgeselde Hikâye Gücü

Kaynak: [jwynia/agent-skills](https://github.com/jwynia/agent-skills) → `skills/creative/`. Reponun **lisans dosyası olmadığı için** içerik buraya kopyalanmadı; skill'ler kullanıcı ortamında (`~/.claude/skills`) kurulu ve buradan çağrılır.

## Neden önemli
Ansiklopedik anlatım izleyiciyi 2. dakikada kaybeder. Bilgi bir **insanın yolculuğuna** asıldığında izlenme süresi artar. Örnek: "Yeniçeri rütbeleri" yerine "bir köy çocuğunun kazandan ağalığa merdiveni".

## Senaryo akışında kullanım
| Aşama | İhtiyaç | Skill |
|---|---|---|
| Fikir | Konuyu bir kişinin/grubun dönüşümüne bağlamak | `character-arc`, `identity-denial` |
| Yapı | 6–9 duygusal "anahtar an" belirlemek | `key-moments`, `scene-sequencing` |
| Dünya | Kurum, inanç ve ekonomiyi canlı anlatmak | `governance-systems`, `belief-systems`, `economic-systems`, `settlement-design` |
| Derinlik | Az sözle yüzyıllık doku hissi | `memetic-depth`, `oblique-worldbuilding` |
| Tazelik | Bilinen konuya yeni açı | `cliche-transcendence`, `story-idea-generator` |
| Final | Kazanılmış, döngüyü kapatan son | `endings`, `positional-revelation` |
| Uyarlama | Kitap/kaynaktan iskelet çıkarmak | `dna-extraction`, `adaptation-synthesis` |
| Hassasiyet | Din, etnik köken, şiddet | `sensitivity-check` |

## Belgesel için sınırlar
- Kurgu **çerçeve** içindir, olgu değildir: uydurulan karakter "temsilî" olarak sunulur, olgular `open-notebook/facts.md`'ye bağlı kalır.
- Diyalog uydurulmaz; tarihî alıntı yalnızca kaynaklıysa kullanılır.
- Final, açılış görüntüsüne geri döner (döngü kapanışı) ve bir sonraki videoya köprü kurar.

Kurulu değilse: `git clone https://github.com/jwynia/agent-skills` → `skills/creative/` altındakileri `~/.claude/skills/` içine kopyala.
