import React from 'react';
import { Composition } from 'remotion';
import { MainVideo, MainVideoProps } from './MainVideo';
import { Yeniceri, totalFrames } from './Yeniceri';

export const Root: React.FC = () => {
  return (
    <>
      <Composition id="Yeniceri" component={Yeniceri} durationInFrames={totalFrames} fps={30} width={1920} height={1080} />
      <Composition
        id="MainVideo"
        component={MainVideo}
        durationInFrames={300}
        fps={30}
        width={1920}
        height={1080}
        defaultProps={{ title: '', words: [], scenes: [] } as MainVideoProps}
        calculateMetadata={({ props }) => ({
          durationInFrames: Math.max(30, Math.ceil((props.durationSec ?? 10) * 30)),
        })}
      />
    </>
  );
};
