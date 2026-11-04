import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from 'remotion';

interface WordItem {
  word: string;
  start: number;
  end: number;
}

interface SceneItem {
  scene_id: number;
  speech_text: string;
  visual_prompt: string;
  overlay_text?: string;
  pacing: string;
}

interface MainVideoProps {
  title: string;
  words: WordItem[];
  scenes: SceneItem[];
}

export const MainVideo: React.FC<MainVideoProps> = ({ title, words = [], scenes = [] }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const currentTime = frame / fps;

  // Arka plan Ken Burns slow zoom efekti
  const scale = interpolate(frame, [0, durationInFrames], [1, 1.08]);

  return (
    <AbsoluteFill style={{ backgroundColor: '#0f172a', color: '#f8fafc', fontFamily: 'sans-serif' }}>
      {/* Arka Plan Katmanı */}
      <AbsoluteFill
        style={{
          transform: `scale(${scale})`,
          background: 'radial-gradient(circle at 50% 30%, #1e293b 0%, #020617 100%)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center'
        }}
      >
        <div style={{ opacity: 0.1, fontSize: 120, fontWeight: 900, textTransform: 'uppercase' }}>
          {title}
        </div>
      </AbsoluteFill>

      {/* Sahne Başlığı ve Overlay Banner */}
      <AbsoluteFill style={{ padding: 80, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <div
          style={{
            background: 'linear-gradient(90deg, #38bdf8, #818cf8)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontSize: 48,
            fontWeight: 800,
            letterSpacing: 2
          }}
        >
          {title}
        </div>
      </AbsoluteFill>

      {/* Dinamik ADHD Altyazı Katmanı (Faster-Whisper Senkronizasyonu) */}
      <div
        style={{
          position: 'absolute',
          bottom: 120,
          width: '100%',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '0 60px'
        }}
      >
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'center',
            gap: 16,
            maxWidth: 1400
          }}
        >
          {words.map((w, idx) => {
            const isActive = currentTime >= w.start && currentTime <= w.end;
            return (
              <span
                key={idx}
                style={{
                  fontSize: isActive ? 68 : 56,
                  fontWeight: 900,
                  textTransform: 'uppercase',
                  color: isActive ? '#facc15' : 'rgba(255, 255, 255, 0.85)',
                  backgroundColor: isActive ? 'rgba(0, 0, 0, 0.75)' : 'transparent',
                  padding: '4px 12px',
                  borderRadius: 8,
                  transform: isActive ? 'scale(1.1)' : 'scale(1)',
                  transition: 'all 0.08s ease'
                }}
              >
                {w.word}
              </span>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
