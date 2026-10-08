import React from 'react';
import {Composition} from 'remotion';
import {Main} from './Main';

const defaultProps = {fps: 30, width: 1080, height: 1920, durationSec: 5, segments: [], overlays: []};

export const RemotionRoot = () => (
  <Composition
    id="Main"
    component={Main}
    defaultProps={defaultProps}
    fps={30}
    width={1080}
    height={1920}
    durationInFrames={150}
    calculateMetadata={({props}) => {
      const fps = props.fps || 30;
      return {
        fps,
        width: props.width || 1080,
        height: props.height || 1920,
        durationInFrames: Math.round((props.durationSec || 5) * fps),
      };
    }}
  />
);
