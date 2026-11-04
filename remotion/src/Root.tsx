import React from 'react';
import { Composition } from 'remotion';
import { MainVideo } from './MainVideo';

export const Root: React.FC = () => {
  return (
    <Composition
      id="MainVideo"
      component={MainVideo}
      durationInFrames={300}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{
        title: 'Autonomous AI Video',
        words: [],
        scenes: []
      }}
    />
  );
};
