---
name: manim-explainer
description: Produces mathematical formulas, neural network architectures, geometric visualizations, and scientific charts using manimCommunity/manim.
tools: [read_file, write_file, run_command]
---

# Manim Mathematical & Scientific Explainer Skill

Bu beceri, **manimCommunity/manim** kütüphanesini kullanarak yapay zeka modellerinin iç işleyişini, matris çarpımlarını, öğrenme eğrilerini ve bilimsel grafikleri Python kodu ile doğrudan animasyona dönüştürür.

## 1. Ne Zaman Kullanılır?

- Bir yapay zeka algoritmasının (örneğin Transformer attention mekanizması, Loss fonksiyonu) açıklanmasında.
- Büyüme oranları, benchmark grafikleri ve istatistiksel karşılaştırmalarda.

## 2. Manim Python Sahne Örneği

```python
from manim import *

class AIModelPerformance(Scene):
    def construct(self):
        title = Text("Model Başarımı ve Ölçeklenme", font_size=40).to_edge(UP)
        axes = Axes(
            x_range=[0, 10, 2],
            y_range=[0, 100, 20],
            axis_config={"color": BLUE},
        )
        graph = axes.plot(lambda x: 10 * np.log2(x + 1) * 8, color=YELLOW)
        label = axes.get_graph_label(graph, label="Verimlilik Artışı")

        self.play(Write(title))
        self.play(Create(axes), Create(graph), run_time=2)
        self.play(FadeIn(label))
        self.wait(1)
```

## 3. Render Komutu

```bash
manim -pqh scene.py AIModelPerformance -o ai_chart.mp4
```
Üretilen klip `assets/broll/` klasörüne taşınır ve ana videonun ilgili sahnesine yerleştirilir.
