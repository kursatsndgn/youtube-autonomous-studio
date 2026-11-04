---
name: motion-canvas
description: Generates programmatic vector animations, modern code-syntax visualizers, and procedural tech diagrams using motion-canvas/motion-canvas.
tools: [read_file, write_file, run_command]
---

# Motion Canvas Vector & Code Animation Skill

Bu beceri, **motion-canvas/motion-canvas** motorunu kullanarak özellikle yazılım, algoritma, mimari diyagramlar ve modern teknoloji anlatımları için pürüzsüz vektörel animasyonlar üretir.

## 1. Ne Zaman Kullanılır?

- Bir kod bloğunun satır satır yazılmasını ve kritik satırın aydınlatılmasını (syntax highlight) göstermek için.
- İki sistem veya API arasındaki veri akışını (Node A -> Node B veri paketi) canlandırmak için.
- 3Blue1Brown benzeri ama modern web/TypeScript estetiğinde diyagramlar için.

## 2. Motion Canvas Sahne Örneği (TypeScript)

```typescript
import { makeScene2D } from '@motion-canvas/2d';
import { all, createRef } from '@motion-canvas/core';
import { Rect, Txt, Code } from '@motion-canvas/2d/lib/components';

export default makeScene2D(function* (view) {
  const codeRef = createRef<Code>();
  const cardRef = createRef<Rect>();

  view.add(
    <Rect
      ref={cardRef}
      width={1200}
      height={600}
      radius={24}
      fill={'#0f172a'}
      stroke={'#38bdf8'}
      lineWidth={4}
    >
      <Code
        ref={codeRef}
        fontSize={36}
        code={`// Autonomous Agent Loop\nwhile (task.isRunning()) {\n  const plan = await agent.think();\n  await agent.execute(plan);\n}`}
      />
    </Rect>
  );

  // Animasyon adımları
  yield* cardRef().scale(1.1, 0.6);
  yield* codeRef().selection([[[1, 0], [1, 20]]], 0.8);
});
```

## 3. Remotion Entegrasyonu

Motion Canvas çıktısı saydam arka planlı video (ProRes 4444 veya WebM) veya MP4 olarak render edilerek Remotion projesine dahil edilir.
