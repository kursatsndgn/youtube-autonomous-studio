---
name: open-notebook
description: Araştırma kasası. trend-researcher'ın bulduğu rakip videoları, transkript özetlerini, kaynakları ve olgu-kaynak eşleşmesini video başına Markdown olarak saklar; isteğe bağlı lfnovo/open-notebook sunucusuna aktarır. Senaryo yazımı bu kasadan beslenir.
---

# Open Notebook — Araştırma Kasası

## trend-researcher ile iş birliği
```
trend-researcher ──(rakip listesi, transkript, youtube_summary)──▶ research/<slug>/competitors.md
                 ──(boşluklar, izleyici soruları)───────────────▶ research/<slug>/brief.md
open-notebook    ──(kaynak okuma, book-to-skill özetleri)────────▶ sources.md + facts.md
script-engine    ◀──(brief + facts)── senaryo; her olgu facts.md'deki bir kaynağa bağlı
```
1. **trend-researcher** konuyu tarar, rakiplerin neyi anlatıp neyi atladığını `competitors.md`'ye yazar (fabric `youtube_summary` kalıbıyla, kelimesi kelimesine kopya yok).
2. **open-notebook** bu boşlukları kaynaklarla doldurur: kitap/makale (`book-to-skill`), ansiklopedi, akademik çalışma.
3. `brief.md`'deki "kimsenin anlatmadığı açı" senaryonun kancası olur.

## Kasa yapısı
```
research/<video-slug>/
  brief.md        # hedef kitle, vaat, kanca tezi, süre, rakiplerden farkımız
  competitors.md  # rakip videolar: başlık, izlenme, kapsadığı / atladığı noktalar
  sources.md      # her kaynak: künye, link, güvenilirlik (A/B/C)
  facts.md        # senaryodaki her olgu → kaynak
  ideas.md        # seri / sonraki video fikirleri (open-loop bağlantıları)
```

## Kurallar
- Senaryodaki **her sayı, tarih ve isim** `facts.md` içinde bir kaynağa bağlanır. Kaynaksız olgu senaryoya girmez.
- Tartışmalı bilgiler "kaynaklarda farklı geçer" diye işaretlenir; senaryoda "genellikle / klasik dönemde" gibi yumuşatma kullanılır.
- `ideas.md`, videonun kapanışındaki "bir sonraki video" kancasının kaynağıdır.

## Open Notebook sunucusu (opsiyonel)
[lfnovo/open-notebook](https://github.com/lfnovo/open-notebook) (MIT) NotebookLM benzeri kendi barındırılan uygulamadır (Docker). Kurulursa `research/<slug>/` bir notebook olarak içe aktarılır; uygulamanın soru-cevap ve özet çıktıları `sources.md`'ye eklenir. Kurulum: upstream README'deki Docker Compose adımları.
