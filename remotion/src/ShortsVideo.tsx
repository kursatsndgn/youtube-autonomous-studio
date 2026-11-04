import React from 'react';
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from 'remotion';

interface WordItem {
  word: string;
  start: number;
  end: number;
}

interface ShortsVideoProps {
  title: string;
  words: WordItem[];
}

export const ShortsVideo: React.FC<ShortsVideoProps> = ({ title, words = [] }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const currentTime = frame / fps;

  // Arka plan Ken Burns zoom
  const scale = interpolate(frame, [0, durationInFrames], [1, 1.15]);

  return (
    <AbsoluteFill style={{ backgroundColor: '#020617', color: '#f8fafc', fontFamily: 'sans-serif' }}>
      {/* Sinematik Dikey Arka Plan */}
      <AbsoluteFill
        style={{
          transform: `scale(${scale})`,
          background: 'radial-gradient(circle at 50% 40%, #1e1b4b 0%, #020617 100%)',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center'
        }}
      />

      {/* Üst Kanca Başlığı (Viral Header) */}
      <div
        style={{
          position: 'absolute',
          top: 140,
          width: '100%',
          display: 'flex',
          justifyContent: 'center',
          padding: '0 40px',
          textAlign: 'center'
        }}
      >
        <span
          style={{
            background: 'linear-gradient(135deg, #ef4444, #f59e0b)',
            color: '#fff',
            fontSize: 48,
            fontWeight: 900,
            textTransform: 'uppercase',
            padding: '12px 24px',
            borderRadius: 16,
            letterSpacing: 2,
            boxShadow: '0 20px 40px rgba(0,0,0,0.6)'
          }}
        >
          {title}
        </span>
      </div>

      {/* Ortada ADHD Tarzı Devasa Kelime Altyazısı */}
      <div
        style={{
          position: 'absolute',
          top: '45%',
          width: '100%',
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '0 50px'
        }}
      >
        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'center', gap: 16 }}>
          {words.map((w, idx) => {
            const isActive = currentTime >= w.start && currentTime <= w.end;
            return (
              <span
                key={idx}
                style={{
                  fontSize: isActive ? 72 : 54,
                  fontWeight: 900,
                  textTransform: 'uppercase',
                  color: isActive ? '#facc15' : 'rgba(255,255,255,0.7)',
                  backgroundColor: isActive ? 'rgba(0,0,0,0.9)' : 'transparent',
                  padding: '6px 16px',
                  borderRadius: 12,
                  transform: isActive ? 'scale(1.15)' : 'scale(1)',
                  transition: 'all 0.06s ease'
                }}
              >
                {w.word}
              </span>
            );
          })}
        </div>
      </div>

      {/* Alt Kanal Filigranı */}
      <div
        style={{
          position: 'absolute',
          bottom: 120,
          width: '100%',
          textAlign: 'center',
          fontSize: 28,
          color: 'rgba(255,255,255,0.5)',
          letterSpacing: 3,
          fontWeight: 700
        }}
      >
        TARİHİN KIRILMA NOKTALARI
      </div>
    </AbsoluteFill>
  );
};
