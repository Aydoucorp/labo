// Overlays texte style "stat" : gros chiffre ou mot cle centre a 42 % de la hauteur.
// Entree : scale 0.8 -> 1 + fondu sur 6 frames. Sortie : fondu 4 frames.
import React from 'react';
import {AbsoluteFill, Sequence, interpolate, useCurrentFrame} from 'remotion';
import type {Overlay} from '../types';
import {easeOut} from '../lib/easing';

const FONT = 'Montserrat, "Montserrat ExtraBold", Arial, sans-serif';

// Taille de police adaptee a la longueur du texte (max 120 px)
const fontSizeFor = (text: string): number => {
  const n = text.length;
  if (n <= 6) return 120;
  if (n <= 10) return 104;
  if (n <= 16) return 84;
  if (n <= 24) return 68;
  return 56;
};

const StatOverlay: React.FC<{overlay: Overlay; width: number; height: number; sidePad: number}> = ({
  overlay,
  width,
  height,
  sidePad,
}) => {
  const frame = useCurrentFrame();
  const dur = overlay.duration_frames;
  const enter = interpolate(frame, [0, 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: easeOut});
  const exit = interpolate(frame, [dur - 4, dur], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <div
        style={{
          position: 'absolute',
          top: height * 0.42,
          left: 0,
          width,
          translate: '0 -50%',
          padding: `0 ${sidePad}px`,
          boxSizing: 'border-box',
          textAlign: 'center',
          fontFamily: FONT,
          fontWeight: 800,
          fontSize: fontSizeFor(overlay.text),
          lineHeight: 1.05,
          color: '#fff',
          WebkitTextStroke: '8px #000',
          paintOrder: 'stroke fill',
          textShadow: '0 8px 24px rgba(0,0,0,0.6)',
          opacity: enter * exit,
          scale: String(interpolate(enter, [0, 1], [0.8, 1])),
          transformOrigin: '50% 50%',
        }}
      >
        {overlay.text}
      </div>
    </AbsoluteFill>
  );
};

export const Overlays: React.FC<{overlays: Overlay[]; width: number; height: number; sidePad: number}> = ({
  overlays,
  width,
  height,
  sidePad,
}) => {
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {overlays.map((o, i) =>
        o.duration_frames > 0 ? (
          <Sequence key={i} name={`overlay ${o.text}`} from={o.from_frame} durationInFrames={o.duration_frames} layout="none">
            <StatOverlay overlay={o} width={width} height={height} sidePad={sidePad} />
          </Sequence>
        ) : null,
      )}
    </AbsoluteFill>
  );
};
