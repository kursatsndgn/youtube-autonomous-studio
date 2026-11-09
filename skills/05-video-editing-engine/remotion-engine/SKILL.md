---
name: remotion-engine
description: Programmatic video composition and editing using Remotion (React), integrating cutout assets (rembg), dynamic word-level subtitles, kinetic typography, and audio ducking.
tools: [run_command, read_file, write_file]
---

# Remotion Programmatic Video Director Skill

Bu beceri, **remotion-dev/remotion** motorunu kullanarak geleneksel video editörlerine (Premiere, CapCut) ihtiyaç duymadan, saf kod ve React komponentleriyle profesyonel video kurgusu yapar. **rembg** ile arka planı temizlenmiş PNG ögelerini dinamik animasyonlarla birleştirir.

## 1. Kompozisyon Katman Mimarisi (Z-Index Hierarchy)

Her sahnede katmanlar şu sırada yerleşir:
1. **Z-0: Arka Plan (Background Layer):** ComfyUI tarafından üretilen sinematik görsel veya yavaşça zoom yapan video loop'u (`interpolate` ile Ken Burns efekti).
2. **Z-1: Ambiyans & Parçacıklar (VFX Layer):** Hafif duman, ışık sızıntısı veya grid ızgara overlay'i.
3. **Z-2: Cutout Varlıklar (Foreground Stickers):** `rembg` ile arka planı silinmiş nesneler, infografikler veya karakterler (Spring animasyonu ile fırlayarak girer).
4. **Z-3: Dinamik Altyazı & Tipografi (Subtitles Layer):** Faster-Whisper'dan gelen kelime zamanlamalarına göre o anda telaffuz edilen kelimeyi sarı/yeşil renkle aydınlatan kinetic metin.
5. **Z-4: Ses Katmanı (Audio Engine):**
   - Ana Ses (Voiceover): 0 dB
   - Arka Plan Müziği (BGM): -24 dB (Konuşma başladığında otomatik ducking ile kısılır).
   - SFX: Pop, whoosh, click efektleri.

## 2. Remotion Bileşen Örneği (Dinamik Altyazı)

```tsx
import { useCurrentFrame, useVideoConfig } from 'remotion';

export const KineticSubtitle = ({ words }: { words: Array<{ word: string, start: number, end: number }> }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  return (
    <div className="absolute bottom-24 w-full flex justify-center items-center px-8">
      <div className="flex flex-wrap gap-3 text-5xl font-black text-center uppercase tracking-wide">
        {words.map((w, i) => {
          const isActive = currentTime >= w.start && currentTime <= w.end;
          return (
            <span
              key={i}
              className={`transition-all duration-75 px-2 py-1 rounded-lg ${
                isActive ? 'text-yellow-400 scale-110 bg-black/60 shadow-lg' : 'text-white/90'
              }`}
            >
              {w.word}
            </span>
          );
        })}
      </div>
    </div>
  );
};
```

## 3. Render Komutu

```bash
npx remotion render src/index.ts MainVideo output/final_video.mp4 --props=./output/render_props.json
```

## Resmî Remotion skill'leri
[remotion-dev/skills](https://github.com/remotion-dev/skills) (best-practices, captions, create, docs) Remotion ekibinin resmî agent skill'leridir. Reponun lisans dosyası olmadığı için buraya kopyalanmadı; ajan ortamına doğrudan kurulur:
```bash
npx skills add remotion-dev/skills
```
Örnek kompozisyon: `remotion/src/Yeniceri.tsx` (kelime zamanlı altyazı, sahne bazlı ses, SVG infografik).
