import React from 'react';
import {Img, OffthreadVideo, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {src, isVideo} from '../lib';

// Média générique (vidéo ou image) qui remplit son conteneur.
// from   : seconde du fichier source à laquelle commencer (vidéo)
// rate   : vitesse de lecture (vidéo)
// kb     : "in" | "out" | null  (lent zoom façon Ken Burns sur images et vidéos)
// fit    : "cover" | "contain"
// pos    : object-position, ex "50% 30%"
export const Media = ({file, from = 0, rate = 1, kb = null, fit = 'cover', pos = '50% 50%', durFrames = 90, style = {}}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const scale = kb === 'in'
    ? interpolate(frame, [0, durFrames], [1.0, 1.08], {extrapolateRight: 'clamp'})
    : kb === 'out'
      ? interpolate(frame, [0, durFrames], [1.08, 1.0], {extrapolateRight: 'clamp'})
      : 1;
  const common = {width: '100%', height: '100%', objectFit: fit, objectPosition: pos, transform: `scale(${scale})`, ...style};
  if (!file) return null;
  if (isVideo(file)) {
    return <OffthreadVideo src={src(file)} muted trimBefore={Math.round(from * fps)} playbackRate={rate} style={common} />;
  }
  return <Img src={src(file)} style={common} />;
};
