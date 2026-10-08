import React from 'react';
import {AbsoluteFill, Img, useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';
import {Media} from './Media';
import {FONT, SERIF, src, fmtNumber} from '../lib';

const pop = (frame, fps, delay = 0) => spring({frame: frame - delay, fps, config: {damping: 12, mass: 0.55}});

// Sortie douce sur les 6 dernières images de la surimpression.
const useExit = (durFrames, n = 6) => {
  const frame = useCurrentFrame();
  return interpolate(frame, [durFrames - n, durFrames], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
};

// Gros chiffre sur l'avatar (ex : "30 %") avec étiquette.
export const BigNumber = ({o, th, durFrames}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const s = pop(frame, fps);
  const out = useExit(durFrames);
  return (
    <div style={{position: 'absolute', left: 0, width, top: height * (o.y ?? 0.52), display: 'flex', justifyContent: 'center'}}>
      <div style={{textAlign: 'center', opacity: s * out, filter: `blur(${(1 - s) * 18 + (1 - out) * 12}px)`, transform: `scale(${0.7 + 0.3 * s})`}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontSize: o.size || 300, lineHeight: 0.9, color: o.color || '#EAF6FF',
          textShadow: '0 0 40px rgba(168,85,58,.65), 0 8px 30px rgba(0,0,0,.5)', letterSpacing: -6}}>{o.text}</div>
        {o.label ? <div style={{fontFamily: FONT, fontWeight: 700, fontSize: 60, color: '#FFFFFF', marginTop: 6, textShadow: '0 4px 18px rgba(0,0,0,.6)'}}>{o.label}</div> : null}
      </div>
    </div>
  );
};

// Capture de source (étude, communiqué, étiquette) dans une carte + surligneur synchronisé.
// highlights[] : {t, x, y, w, h} en fractions de l'image (0 à 1), couleur optionnelle.
export const DocCard = ({o, th, durFrames}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const s = pop(frame, fps);
  const out = useExit(durFrames);
  const w = width * (o.w || 0.86);
  const start = o.start;
  return (
    <AbsoluteFill style={{alignItems: 'center', justifyContent: o.full ? 'center' : 'flex-start', paddingTop: o.full ? 0 : height * (o.y ?? 0.5)}}>
      <div style={{position: 'relative', width: w, borderRadius: 22, overflow: 'hidden', background: '#fff', boxShadow: '0 20px 60px rgba(0,0,0,.45)',
        opacity: s * out, transform: `translateY(${(1 - s) * 120}px)`, filter: `blur(${(1 - s) * 10}px)`}}>
        <Img src={src(o.src)} style={{width: '100%', display: 'block'}} />
        {(o.highlights || []).map((h, i) => {
          const f0 = Math.round((h.t - start) * fps);
          const p = interpolate(frame, [f0, f0 + Math.round((h.dur || 0.5) * fps)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
          return <div key={i} style={{position: 'absolute', left: `${h.x * 100}%`, top: `${h.y * 100}%`, width: `${h.w * 100 * p}%`, height: `${h.h * 100}%`,
            background: h.color || th.accent2, mixBlendMode: 'multiply', opacity: 0.85, borderRadius: 4}} />;
        })}
      </div>
    </AbsoluteFill>
  );
};

// Titre de chapitre (liste numérotée) : gros numéro + titre + média dans une carte lumineuse.
export const Chapter = ({o, th, durFrames}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const s = pop(frame, fps);
  const out = useExit(durFrames);
  const chars = Math.floor(interpolate(frame, [3, 3 + (o.title || '').length * 1.2], [0, (o.title || '').length], {extrapolateRight: 'clamp'}));
  return (
    <AbsoluteFill style={{opacity: out}}>
      <div style={{position: 'absolute', left: width * 0.14, top: height * (o.y ?? 0.44), display: 'flex', alignItems: 'center', gap: 14}}>
        <div style={{fontFamily: FONT, fontWeight: 900, fontStyle: 'italic', fontSize: 190, color: o.numColor || th.accent2, lineHeight: 0.85,
          transform: `scale(${s})`, textShadow: '0 6px 24px rgba(0,0,0,.5)'}}>{o.number}</div>
        <div style={{fontFamily: FONT, fontStyle: 'italic', fontWeight: 500, fontSize: 64, color: '#FFF', lineHeight: 1.0, maxWidth: width * 0.55,
          textShadow: '0 4px 18px rgba(0,0,0,.6)'}}>{(o.title || '').slice(0, chars)}</div>
      </div>
      {o.media ? (
        <div style={{position: 'absolute', left: width * 0.2, width: width * 0.6, top: height * ((o.y ?? 0.44) + 0.1), height: height * 0.2, borderRadius: 20, overflow: 'hidden',
          boxShadow: '0 0 0 3px rgba(255,255,255,.85), 0 0 40px rgba(255,255,255,.35)', opacity: s, transform: `translateY(${(1 - s) * 60}px)`}}>
          <Media file={o.media} from={o.mediaFrom || 0} kb="in" durFrames={durFrames} />
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// Objet détouré (PNG transparent) qui "pope" près des mains, texte optionnel écrit dessus.
export const Cutout = ({o, th, durFrames}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const s = pop(frame, fps);
  const out = useExit(durFrames);
  const tf = o.textT != null ? Math.round((o.textT - o.start) * fps) : 0;
  const ts = o.text ? pop(frame, fps, tf) : 0;
  return (
    <div style={{position: 'absolute', left: width * o.x, top: height * o.y, width: width * (o.w || 0.3), transform: `translate(-50%,-50%) scale(${s * out}) rotate(${o.rotate || 0}deg)`}}>
      <Img src={src(o.src)} style={{width: '100%', display: 'block', filter: 'drop-shadow(0 12px 22px rgba(0,0,0,.45))'}} />
      {o.text ? <div style={{position: 'absolute', inset: 0, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: FONT, fontWeight: 900,
        fontSize: o.textSize || 56, color: o.textColor || '#7A0A12', transform: `rotate(${o.textRotate || -12}deg) scale(${ts})`}}>{o.text}</div> : null}
    </div>
  );
};

// Compteur animé (ex : 0 → 11 878) qui s'arrête pile quand le nombre est prononcé.
export const Counter = ({o, th, durFrames}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const a = Math.round(((o.countStart ?? o.start) - o.start) * fps);
  const b = Math.round(((o.countEnd ?? o.start + 1.5) - o.start) * fps);
  const v = interpolate(frame, [a, b], [o.from || 0, o.to], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: (x) => 1 - Math.pow(1 - x, 3)});
  const s = pop(frame, fps);
  return (
    <div style={{position: 'absolute', left: 0, width, top: height * (o.y ?? 0.4), textAlign: 'center', fontFamily: FONT, transform: `scale(${0.8 + 0.2 * s})`, opacity: s}}>
      <div style={{fontSize: o.size || 170, fontWeight: 900, color: o.color || th.accent, letterSpacing: -3}}>{o.prefix || ''}{fmtNumber(v)}{o.suffix || ''}</div>
      {o.label ? <div style={{fontSize: 52, fontWeight: 700, color: o.labelColor || th.accent}}>{o.label}</div> : null}
    </div>
  );
};

// Étiquette qui apparaît sur son mot (annotations d'animation éducative, schémas).
export const Label = ({o, th, durFrames}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const s = pop(frame, fps);
  const out = useExit(durFrames);
  const lineLen = interpolate(frame, [0, 8], [0, o.line || 0], {extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: width * o.x, top: height * o.y, transform: `translate(${o.align === 'right' ? '-100%' : o.align === 'center' ? '-50%' : '0'}, -50%)`, opacity: s * out}}>
      {o.line ? <div style={{position: 'absolute', top: '50%', [o.align === 'right' ? 'left' : 'right']: '100%', width: lineLen, height: 3, background: o.color || th.accent}} /> : null}
      <div style={{fontFamily: FONT, fontWeight: 800, fontSize: o.size || 46, color: o.color || th.accent, background: o.box ? (o.boxColor || '#FFFFFF') : 'transparent',
        padding: o.box ? '6px 16px' : 0, borderRadius: 10, whiteSpace: 'nowrap', textShadow: o.box ? 'none' : (o.shadow || '0 2px 10px rgba(0,0,0,.25)')}}>{o.text}</div>
      {o.sub ? <div style={{fontFamily: FONT, fontWeight: 500, fontSize: (o.size || 46) * 0.55, color: o.subColor || o.color || th.accent, maxWidth: 420, marginTop: 4}}>{o.sub}</div> : null}
    </div>
  );
};

// Texte libre (titre d'animation tapé mot à mot : utiliser plutôt Kinetic ; ici bloc simple).
export const TextPop = ({o, th, durFrames}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const s = pop(frame, fps);
  const out = useExit(durFrames);
  return (
    <div style={{position: 'absolute', left: width * (o.x ?? 0.5), top: height * (o.y ?? 0.5), transform: `translate(-50%,-50%) scale(${0.85 + 0.15 * s})`, opacity: s * out,
      fontFamily: o.serif ? SERIF : FONT, fontStyle: o.serif ? 'italic' : 'normal', fontWeight: o.weight || 800, fontSize: o.size || 64, color: o.color || '#FFF',
      background: o.bg || 'transparent', padding: o.bg ? '10px 22px' : 0, borderRadius: 12, textAlign: 'center', maxWidth: width * 0.9}}>{o.text}</div>
  );
};

// Bouton "S'abonner" animé (fin de vidéo) : clic simulé puis "Abonné".
export const Follow = ({o, th, durFrames}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const s = pop(frame, fps);
  const click = Math.round((o.clickAfter ?? 0.8) * fps);
  const clicked = frame >= click;
  const cursor = interpolate(frame, [click - 10, click], [60, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'absolute', left: width / 2, top: height * (o.y ?? 0.45), transform: `translate(-50%,-50%) scale(${s})`}}>
      <div style={{display: 'flex', alignItems: 'center', gap: 16, background: 'rgba(20,20,20,.72)', border: '2px solid rgba(255,255,255,.5)', borderRadius: 60, padding: '10px 14px 10px 10px'}}>
        {o.avatar ? <Img src={src(o.avatar)} style={{width: 64, height: 64, borderRadius: '50%', objectFit: 'cover'}} /> : <div style={{width: 64, height: 64, borderRadius: '50%', background: '#555'}} />}
        <div style={{fontFamily: FONT, fontWeight: 700, fontSize: 34, color: '#FFF'}}>{o.handle}</div>
        <div style={{fontFamily: FONT, fontWeight: 800, fontSize: 28, padding: '10px 26px', borderRadius: 40,
          background: clicked ? th.followBlue : '#FFFFFF', color: clicked ? '#FFFFFF' : '#111', transform: `scale(${clicked ? 1 : 1 - 0.08 * (1 - cursor / 60)})`}}>
          {clicked ? (o.doneText || 'Abonné') : (o.text || "S'abonner")}
        </div>
      </div>
      {frame < click + 12 ? <div style={{position: 'absolute', right: 30 - cursor * 0.2, top: 60 + cursor, width: 34, height: 34, borderRadius: '50%', background: th.followBlue, opacity: 0.9}} /> : null}
    </div>
  );
};

// Flash lumineux de transition (light leak) centré sur la coupe.
export const Flash = ({o, durFrames}) => {
  const frame = useCurrentFrame();
  const mid = durFrames / 2;
  const a = interpolate(frame, [0, mid, durFrames], [0, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const c = o.color || '#FF4D8D';
  return <AbsoluteFill style={{background: `radial-gradient(circle at ${o.at || '30% 20%'}, #FFFFFF 0%, ${c} 35%, rgba(0,0,0,0) 75%)`, opacity: a * (o.strength ?? 0.9), mixBlendMode: 'screen'}} />;
};

// Média incrusté (image ou vidéo) dans une carte, sur l'avatar (comparatif, photo produit).
export const Inset = ({o, th, durFrames}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const s = pop(frame, fps);
  const out = useExit(durFrames);
  return (
    <div style={{position: 'absolute', left: width * (o.x ?? 0.5), top: height * (o.y ?? 0.72), width: width * (o.w || 0.8), height: height * (o.h || 0.22),
      transform: `translate(-50%,-50%) translateY(${(1 - s) * 80}px)`, opacity: s * out, borderRadius: o.round ?? 18, overflow: 'hidden',
      boxShadow: o.glow ? '0 0 0 3px rgba(255,255,255,.85), 0 0 40px rgba(255,255,255,.35)' : '0 16px 40px rgba(0,0,0,.5)'}}>
      <Media file={o.src} from={o.from || 0} fit={o.fit || 'cover'} durFrames={durFrames} />
    </div>
  );
};
