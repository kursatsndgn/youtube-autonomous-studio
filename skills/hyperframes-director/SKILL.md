---
name: hyperframes-director
description: Generates rich HTML, Tailwind CSS, and GSAP animated video frames and deterministic MP4 scenes using the heygen-com/hyperframes framework.
tools: [read_file, write_file, run_command]
---

# Hyperframes Scene Director Skill

Bu beceri, **heygen-com/hyperframes** mimarisini kullanarak LLM'in React kodlarıyla boğuşmak zorunda kalmadan, doğrudan **HTML, Tailwind CSS ve GSAP (GreenSock) animasyonları** ile modern, akıcı ve deterministik video sahneleri ve hareketli kartlar (motion cards) üretmesini sağlar.

## 1. Ne Zaman Kullanılır?

- Karmaşık React bileşeni yazmak yerine, hızlıca şık bir bildirim kartı, istatistik grafiği, tweet kutusu veya karşılaştırma tablosu eklemek gerektiğinde.
- HeyGen tarzı temiz, modern kurumsal veya YouTube explainer görselleştirmelerinde.

## 2. Hyperframes Şablon Mimarisi

Bir Hyperframes sahnesi standart HTML5 + CSS animasyonu olarak tanımlanır:

```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.2/gsap.min.js"></script>
  <style>
    body { background: transparent; overflow: hidden; width: 1920px; height: 1080px; }
  </style>
</head>
<body class="flex items-center justify-center">
  <div id="card" class="bg-slate-900/90 border border-cyan-500/40 p-12 rounded-3xl shadow-2xl backdrop-blur-xl flex flex-col gap-6 max-w-3xl transform scale-75 opacity-0">
    <div class="flex items-center gap-4">
      <div class="w-6 h-6 rounded-full bg-cyan-400 animate-ping"></div>
      <span class="text-cyan-400 font-mono tracking-widest text-2xl uppercase">CANLI METRİK</span>
    </div>
    <h1 class="text-6xl font-black text-white">Yapay Zeka Hız Çarpanı</h1>
    <p class="text-3xl text-slate-300 leading-relaxed">Geleneksel geliştirme süresi 14 günden 4 saate indi.</p>
  </div>

  <script>
    // GSAP deterministik zamanlama
    gsap.to("#card", {
      opacity: 1,
      scale: 1,
      duration: 0.8,
      ease: "back.out(1.7)"
    });
  </script>
</body>
</html>
```

## 3. Remotion & B-Roll Entegrasyonu

Üretilen HTML dosyası HyperFrames CLI veya headless browser ile şeffaf WebM / MP4 video olarak render edilir ve Remotion kompozisyonuna Z-Index katmanı olarak bindirilir.
