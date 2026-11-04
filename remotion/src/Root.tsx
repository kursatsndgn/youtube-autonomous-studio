import React from 'react';
import { Composition } from 'remotion';
import { MainVideo } from './MainVideo';
import { ShortsVideo } from './ShortsVideo';

export const Root: React.FC = () => {
  return (
    <>
      {/* 12-15 Dakikalık Ana Yatay Video (1920x1080) */}
      <Composition
        id="MainVideo"
        component={MainVideo}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{
          title: 'Bir Futbol Maçı Gerçek Bir Savaşı Nasıl Başlattı?',
          words: [],
          scenes: []
        }}
      />

      {/* 45-60 Saniyelik Dikey YouTube Shorts (1080x1920) */}
      <Composition
        id="ShortsVideo"
        component={ShortsVideo}
        durationInFrames={900} // 30 saniye
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          title: '3000 KİŞİYİ ÖLDÜREN 90 DAKİKA',
          words: [],
          scenes: []
        }}
      />
    </>
  );
};
