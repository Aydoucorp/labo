// Elements optionnels : barre de progression fine et logo.
import React from 'react';
import {AbsoluteFill, Img, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {resolveSrc} from '../lib/load';

type Safe = {top: number; bottom: number; left: number; right: number};

export const ProgressBar: React.FC<{width: number; height: number; safe: Safe}> = ({width, height, safe}) => {
  const frame = useCurrentFrame();
  const {durationInFrames} = useVideoConfig();
  const trackW = width - safe.left - safe.right;
  const y = height - safe.bottom - 14;
  const p = interpolate(frame, [0, Math.max(1, durationInFrames - 1)], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div style={{position: 'absolute', left: safe.left, top: y, width: trackW, height: 6, borderRadius: 3, backgroundColor: 'rgba(255,255,255,0.25)'}} />
      <div style={{position: 'absolute', left: safe.left, top: y, width: trackW * p, height: 6, borderRadius: 3, backgroundColor: 'rgba(255,255,255,0.95)'}} />
    </AbsoluteFill>
  );
};

export const Logo: React.FC<{src: string; safe: Safe}> = ({src, safe}) => {
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <Img
        src={resolveSrc(src)}
        style={{
          position: 'absolute',
          top: safe.top + 10,
          right: safe.right,
          width: 160,
          height: 'auto',
          opacity: 0.92,
          filter: 'drop-shadow(0 4px 12px rgba(0,0,0,0.5))',
        }}
      />
    </AbsoluteFill>
  );
};
