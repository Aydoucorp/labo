// Couche des clips : chaque clip est monte dans un Sequence premonte. Le clip
// sortant reste monte pendant les frames de la transition du clip suivant
// (chevauchement), et le clip entrant est dessine au dessus (ordre DOM).
import React from 'react';
import {AbsoluteFill, Sequence, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Clip} from '../types';
import {ClipView} from './ClipView';

// Calque blanc pour la transition "flash" : opacite 1 -> 0
const Flash: React.FC<{frames: number}> = ({frames}) => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        backgroundColor: 'white',
        opacity: interpolate(frame, [0, Math.max(1, frames)], [1, 0], {
          extrapolateLeft: 'clamp',
          extrapolateRight: 'clamp',
        }),
        pointerEvents: 'none',
      }}
    />
  );
};

export const ClipLayer: React.FC<{clips: Clip[]; totalFrames: number}> = ({clips, totalFrames}) => {
  const {fps} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: 'black'}}>
      {clips.map((clip, i) => {
        const next = clips[i + 1] ?? null;
        const nextT = next && next.transition_in.type !== 'cut' && next.transition_in.type !== 'flash' ? next.transition_in : null;
        // Le sortant reste monte pendant la transition du suivant
        const extra = nextT ? nextT.frames : 0;
        const duration = Math.max(1, Math.min(clip.duration_frames + extra, totalFrames - clip.from_frame));
        return (
          <Sequence
            key={`${clip.shot_id}-${i}`}
            name={`clip ${clip.shot_id}`}
            from={clip.from_frame}
            durationInFrames={duration}
            premountFor={fps}
            layout="absolute-fill"
          >
            <ClipView clip={clip} nextTransition={nextT} />
          </Sequence>
        );
      })}
      {clips.map((clip, i) =>
        clip.transition_in.type === 'flash' && clip.transition_in.frames > 0 ? (
          <Sequence
            key={`flash-${clip.shot_id}-${i}`}
            name={`flash ${clip.shot_id}`}
            from={clip.from_frame}
            durationInFrames={clip.transition_in.frames}
            layout="none"
          >
            <Flash frames={clip.transition_in.frames} />
          </Sequence>
        ) : null,
      )}
    </AbsoluteFill>
  );
};
