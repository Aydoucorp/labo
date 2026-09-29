// Un clip B-roll : OffthreadVideo prepare (1080x1920) sur lequel on applique
// uniquement des transformations : Ken Burns, punch, transition entrante (la
// sienne) et transition sortante (celle du clip suivant, pendant le chevauchement).
import React from 'react';
import {AbsoluteFill, OffthreadVideo, interpolate, useCurrentFrame} from 'remotion';
import type {Clip, Transition} from '../types';
import {dbToGain} from '../lib/audio';
import {bump, clamp01, easeInOut, easeOut} from '../lib/easing';
import {resolveSrc} from '../lib/load';

type Props = {
  clip: Clip;
  // Transition du clip suivant (le clip courant est alors le sortant)
  nextTransition: Transition | null;
};

type Xf = {
  tx: number; // en % de la largeur
  ty: number; // en % de la hauteur
  scale: number;
  blur: number;
  opacity: number;
  clipPath: string | null;
};

const identity = (): Xf => ({tx: 0, ty: 0, scale: 1, blur: 0, opacity: 1, clipPath: null});

// Signe horizontal de la direction : left = le contenu file vers la gauche
const dirSign = (dir: Transition['dir']): number => (dir === 'right' || dir === 'down' ? 1 : -1);
const isVertical = (dir: Transition['dir']): boolean => dir === 'up' || dir === 'down';

// Transformations du clip ENTRANT en fonction de la progression p (0 -> 1)
const incoming = (t: Transition, p: number): Xf => {
  const x = identity();
  const e = easeInOut(clamp01(p));
  switch (t.type) {
    case 'whip': {
      // Entrant : arrive depuis le cote oppose au sens de fuite du sortant
      const s = dirSign(t.dir);
      const amount = 40 * (1 - e) * -s;
      if (isVertical(t.dir)) {
        x.ty = amount;
      } else {
        x.tx = amount;
      }
      x.blur = 8 * bump(p);
      return x;
    }
    case 'zoomthrough':
      x.scale = interpolate(e, [0, 1], [0.7, 1]);
      x.opacity = interpolate(p, [0, 0.55], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
      x.blur = 6 * (1 - e);
      return x;
    case 'dissolve':
      x.opacity = clamp01(p);
      return x;
    case 'wipe': {
      const rest = (1 - e) * 100;
      // inset(top right bottom left) : la partie masquee se retire selon la direction
      if (t.dir === 'right') {
        x.clipPath = `inset(0 ${rest}% 0 0)`;
      } else if (t.dir === 'up') {
        x.clipPath = `inset(${rest}% 0 0 0)`;
      } else if (t.dir === 'down') {
        x.clipPath = `inset(0 0 ${rest}% 0)`;
      } else {
        x.clipPath = `inset(0 0 0 ${rest}%)`;
      }
      return x;
    }
    case 'punchcut':
      x.scale = interpolate(easeOut(clamp01(p)), [0, 1], [1.1, 1]);
      return x;
    case 'flash':
    case 'cut':
    default:
      return x;
  }
};

// Transformations du clip SORTANT en fonction de la progression q (0 -> 1)
const outgoing = (t: Transition, q: number): Xf => {
  const x = identity();
  const e = easeInOut(clamp01(q));
  switch (t.type) {
    case 'whip': {
      const s = dirSign(t.dir);
      const amount = 40 * e * s;
      if (isVertical(t.dir)) {
        x.ty = amount;
      } else {
        x.tx = amount;
      }
      x.blur = 8 * bump(q);
      return x;
    }
    case 'zoomthrough':
      x.scale = interpolate(e, [0, 1], [1, 1.6]);
      x.blur = 10 * e;
      return x;
    default:
      return x;
  }
};

export const ClipView: React.FC<Props> = ({clip, nextTransition}) => {
  const frame = useCurrentFrame(); // local au Sequence du clip
  const dur = clip.duration_frames;

  // Ken Burns : zoom lent sur toute la duree du clip
  const kb = clip.kenburns;
  const kbScale = kb
    ? interpolate(frame, [0, Math.max(1, dur - 1)], [kb.from, kb.to], {
        extrapolateLeft: 'clamp',
        extrapolateRight: 'clamp',
      })
    : 1;
  const origin = kb ? `${kb.origin[0] * 100}% ${kb.origin[1] * 100}%` : '50% 42%';

  // Punch : saut a punch.scale puis retour a 1 en punch.frames
  let punchScale = 1;
  if (clip.punch) {
    const p0 = clip.punch.at_frame - clip.from_frame;
    punchScale = interpolate(frame, [p0, p0 + clip.punch.frames], [clip.punch.scale, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
      easing: easeOut,
    });
    if (frame < p0) {
      punchScale = 1;
    }
  }

  // Transition entrante (la mienne)
  const tin = clip.transition_in;
  let xf = identity();
  if (tin && tin.type !== 'cut' && tin.type !== 'flash' && tin.frames > 0 && frame < tin.frames) {
    xf = incoming(tin, frame / tin.frames);
  }
  // Transition sortante (celle du suivant) : demarre a la fin de ma duree nominale
  if (nextTransition && nextTransition.frames > 0 && frame >= dur) {
    const q = (frame - dur) / nextTransition.frames;
    xf = outgoing(nextTransition, q);
  }

  const gain = clip.ambience ? dbToGain(clip.ambience_db) : 0;

  return (
    <AbsoluteFill
      style={{
        translate: `${xf.tx}% ${xf.ty}%`,
        scale: String(xf.scale),
        opacity: xf.opacity,
        filter: xf.blur > 0.05 ? `blur(${xf.blur.toFixed(2)}px)` : undefined,
        clipPath: xf.clipPath ?? undefined,
        backgroundColor: 'black',
      }}
    >
      <AbsoluteFill
        style={{
          scale: String(kbScale * punchScale),
          transformOrigin: origin,
        }}
      >
        <OffthreadVideo
          src={resolveSrc(clip.src)}
          trimBefore={clip.trim_before_frames}
          playbackRate={clip.speed}
          muted={!clip.ambience || gain <= 0}
          volume={gain}
          delayRenderTimeoutInMilliseconds={120000}
          style={{width: '100%', height: '100%', objectFit: 'cover'}}
        />
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
