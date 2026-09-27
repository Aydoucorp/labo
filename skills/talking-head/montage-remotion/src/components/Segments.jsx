import React from 'react';
import {AbsoluteFill, OffthreadVideo, Sequence, useCurrentFrame, useVideoConfig, interpolate, spring} from 'remotion';
import {Media} from './Media';
import {Kinetic} from './Kinetic';
import {FONT, SERIF, src, fr, absT} from '../lib';

const ZOOM = {A: 1.0, B: 1.15, C: 1.3};

// Clip avatar (scène Seedance 2.5 générée depuis l'image de départ). Le clip est calé sur la voix maître :
// clipStart = temps absolu (s) de la voix auquel correspond l'image 0 du clip.
const AvatarVideo = ({seg, fps, zoom = 'A', faceY = 0.3, drift = true, durFrames}) => {
  const frame = useCurrentFrame();
  const base = ZOOM[zoom] || Number(zoom) || 1;
  const d = drift ? interpolate(frame, [0, durFrames], [0, 0.025], {extrapolateRight: 'clamp'}) : 0;
  const trim = Math.max(0, Math.round((seg.start - (seg.clipStart ?? seg.start)) * fps));
  return (
    <OffthreadVideo
      src={src(seg.src)}
      muted
      trimBefore={trim}
      style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: seg.pos || '50% 50%',
        transform: `scale(${base + d})`, transformOrigin: `50% ${faceY * 100}%`}}
    />
  );
};

export const AvatarSeg = ({seg, fps, durFrames}) => (
  <AbsoluteFill style={{backgroundColor: '#000'}}>
    <AvatarVideo seg={seg} fps={fps} zoom={seg.zoom || 'A'} faceY={seg.faceY ?? 0.3} drift={seg.drift !== false} durFrames={durFrames} />
  </AbsoluteFill>
);

// Écran partagé : avatar en haut, b-roll(s) en bas, bandeau titre sur la couture.
export const SplitSeg = ({seg, fps, th, durFrames}) => {
  const {width, height} = useVideoConfig();
  const half = height / 2;
  const brolls = seg.broll || [];
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <div style={{position: 'absolute', top: 0, left: 0, width, height: half, overflow: 'hidden'}}>
        <AvatarVideo seg={{...seg, pos: seg.avatarPos || '50% 50%'}} fps={fps} zoom={seg.zoom || 'A'} faceY={0.35} drift={false} durFrames={durFrames} />
      </div>
      <div style={{position: 'absolute', top: half, left: 0, width, height: half, overflow: 'hidden'}}>
        {brolls.map((b, i) => {
          const from = fr(b.start, fps) - fr(seg.start, fps);
          const dur = fr(b.end, fps) - fr(b.start, fps);
          return (
            <Sequence key={i} from={from} durationInFrames={dur} layout="none">
              <div style={{position: 'absolute', inset: 0}}>
                <Media file={b.src} from={b.from || 0} rate={b.rate || 1} pos={b.pos || '50% 50%'} kb={b.kb || null} durFrames={dur} />
              </div>
            </Sequence>
          );
        })}
      </div>
      {seg.banner ? <Banner text={seg.banner} th={th} y={half} /> : null}
    </AbsoluteFill>
  );
};

export const Banner = ({text, th, y}) => {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 14, mass: 0.6}});
  return (
    <div style={{position: 'absolute', left: 0, width, top: y, transform: `translateY(-50%) scale(${0.85 + 0.15 * s})`, display: 'flex', justifyContent: 'center', opacity: s}}>
      <div style={{maxWidth: width * 0.9, background: th.bannerBg, color: th.bannerText, fontFamily: FONT, fontWeight: 800,
        fontSize: 44, lineHeight: 1.15, textAlign: 'center', padding: '12px 26px', borderRadius: 14, boxShadow: '0 6px 24px rgba(0,0,0,.35)'}}>
        {text}
      </div>
    </div>
  );
};

// B-roll dans une carte à coins arrondis sur fond noir (uniformise des sources hétérogènes).
export const CardSeg = ({seg, durFrames, th}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const s = spring({frame, fps, config: {damping: 18, mass: 0.5}});
  const w = width * (seg.cardW || 0.86);
  const h = height * (seg.cardH || 0.64);
  const clips = seg.clips || [{src: seg.src, start: seg.start, end: seg.end, from: seg.from || 0, rate: seg.rate || 1}];
  return (
    <AbsoluteFill style={{backgroundColor: th.cardBg}}>
      <div style={{position: 'absolute', left: (width - w) / 2, top: (height - h) / 2 - height * 0.02, width: w, height: h,
        borderRadius: 38, overflow: 'hidden', boxShadow: '0 0 0 2px rgba(255,255,255,.18), 0 20px 60px rgba(0,0,0,.6)',
        transform: `scale(${0.96 + 0.04 * s})`}}>
        {clips.map((c, i) => {
          const from = fr(c.start, fps) - fr(seg.start, fps);
          const dur = fr(c.end, fps) - fr(c.start, fps);
          return (
            <Sequence key={i} from={from} durationInFrames={dur} layout="none">
              <div style={{position: 'absolute', inset: 0}}>
                <Media file={c.src} from={c.from || 0} rate={c.rate || 1} pos={c.pos || '50% 50%'} kb={c.kb || null} durFrames={dur} />
              </div>
            </Sequence>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// Vidéo horizontale en bandeau 16:9, mots clés écrits au-dessus un par un.
export const LetterboxSeg = ({seg, durFrames, th, fps}) => {
  const {width, height} = useVideoConfig();
  const h = width * 9 / 16;
  const top = (height - h) / 2;
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      <div style={{position: 'absolute', left: 0, top, width, height: h, overflow: 'hidden'}}>
        <Media file={seg.src} from={seg.from || 0} rate={seg.rate || 1} kb={seg.kb || null} durFrames={durFrames} />
      </div>
      {seg.words ? (
        <div style={{position: 'absolute', left: 60, right: 60, top: top - 260, height: 240, display: 'flex', alignItems: 'flex-end'}}>
          <Kinetic words={seg.words} segStart={seg.start} th={th} size={58} align="left" />
        </div>
      ) : null}
      {seg.wordsBelow ? (
        <div style={{position: 'absolute', left: 60, right: 60, top: top + h + 30, height: 200}}>
          <Kinetic words={seg.wordsBelow} segStart={seg.start} th={th} size={46} align="right" />
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

// Plein écran : vidéo ou image (b-roll vertical, image IA, animation éducative, capture).
export const FullSeg = ({seg, durFrames}) => (
  <AbsoluteFill style={{backgroundColor: seg.bg || '#000'}}>
    <Media file={seg.src} from={seg.from || 0} rate={seg.rate || 1} kb={seg.kb ?? null} fit={seg.fit || 'cover'} pos={seg.pos || '50% 50%'} durFrames={durFrames} />
  </AbsoluteFill>
);

// Fond uni ou dégradé (pour compteurs, étiquettes, infographies construites en surimpression).
export const PlainSeg = ({seg}) => (
  <AbsoluteFill style={{background: seg.bg || '#FFFFFF'}} />
);

// Collage vertical de 2 à 4 images ou vidéos, apparition simultanée ou échelonnée (items[].t).
export const CollageSeg = ({seg, fps, durFrames}) => {
  const frame = useCurrentFrame();
  const items = seg.items || [];
  const n = items.length || 1;
  return (
    <AbsoluteFill style={{backgroundColor: '#000', display: 'flex', flexDirection: 'column'}}>
      {items.map((it, i) => {
        const appear = it.t != null ? fr(it.t, fps) - fr(seg.start, fps) : 0;
        const s = spring({frame: frame - appear, fps, config: {damping: 16, mass: 0.5}});
        return (
          <div key={i} style={{flex: 1, overflow: 'hidden', opacity: frame >= appear ? 1 : 0, transform: `translateY(${(1 - s) * 40}px)`}}>
            <Media file={it.src} from={it.from || 0} kb="in" durFrames={durFrames} />
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// Infographie en lignes (ex : nutriment + phrase + image ronde), chaque ligne apparaît sur son mot.
// rows[] : {t, title, parts:[{s, mark?}], img}
export const InfoListSeg = ({seg, fps, th}) => {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const rows = seg.rows || [];
  const rowH = (height * 0.8) / Math.max(rows.length, 3);
  return (
    <AbsoluteFill style={{background: seg.bg || `linear-gradient(180deg, #FFFFFF 0%, ${th.infoBg} 100%)`}}>
      {rows.map((r, i) => {
        const appear = fr(r.t, fps) - fr(seg.start, fps);
        const s = spring({frame: frame - appear, fps, config: {damping: 15, mass: 0.6}});
        const tNow = absT(frame, seg.start, fps);
        return (
          <div key={i} style={{position: 'absolute', left: 60, width: width - 120, top: height * 0.1 + i * rowH, height: rowH,
            display: 'flex', alignItems: 'center', opacity: frame >= appear ? s : 0, transform: `translateY(${(1 - s) * 30}px)`, filter: `blur(${(1 - s) * 6}px)`}}>
            <div style={{flex: 1, color: th.infoText, fontFamily: FONT}}>
              <div style={{fontSize: 120, fontWeight: 800, lineHeight: 1}}>{r.title}</div>
              <div style={{fontSize: 34, fontWeight: 500, marginTop: 10, lineHeight: 1.3, maxWidth: width * 0.5}}>
                {(r.parts || []).map((p, k) => {
                  const marked = p.mark != null && tNow >= p.mark;
                  return <span key={k} style={{fontWeight: p.bold ? 800 : 500, background: marked ? th.accent2 : 'transparent', transition: 'none'}}>{p.s}</span>;
                })}
              </div>
            </div>
            {r.img ? (
              <div style={{width: rowH * 0.8, height: rowH * 0.8, borderRadius: '50%', overflow: 'hidden', transform: `scale(${s})`}}>
                <Media file={r.img} kb="in" durFrames={300} />
              </div>
            ) : null}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

// Image ou vidéo dramatique + typographie cinétique mot à mot (chiffre géant, mot en serif).
export const KineticSeg = ({seg, durFrames, th}) => {
  const {width, height} = useVideoConfig();
  return (
    <AbsoluteFill style={{backgroundColor: '#000'}}>
      {seg.src ? <Media file={seg.src} from={seg.from || 0} kb={seg.kb ?? 'in'} durFrames={durFrames} pos={seg.pos || '50% 60%'} /> : null}
      <div style={{position: 'absolute', left: 70, right: 70, top: height * (seg.textY ?? 0.08)}}>
        <Kinetic words={seg.words || []} segStart={seg.start} th={th} size={seg.size || 72} align={seg.align || 'left'} />
      </div>
    </AbsoluteFill>
  );
};

// Entrée par cercle qui s'ouvre (changement de partie, ex : vers l'animation éducative).
export const CircleWipe = ({children, frames = 10, cx = '70%', cy = '15%'}) => {
  const frame = useCurrentFrame();
  const r = interpolate(frame, [0, frames], [0, 160], {extrapolateRight: 'clamp'});
  return <AbsoluteFill style={{clipPath: `circle(${r}% at ${cx} ${cy})`}}>{children}</AbsoluteFill>;
};

export {SERIF};
