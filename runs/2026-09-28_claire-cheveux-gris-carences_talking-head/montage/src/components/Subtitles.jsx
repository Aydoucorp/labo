import React, {useMemo} from 'react';
import {useCurrentFrame, useVideoConfig, spring} from 'remotion';
import {FONT} from '../lib';

// Regroupe les mots horodatés en lignes de 3 à 5 mots (coupure sur ponctuation, pause ou longueur).
export const chunkWords = (words, maxWords = 4, maxChars = 26, gap = 0.45) => {
  const chunks = [];
  let cur = [];
  const flush = () => {
    if (cur.length) chunks.push(cur);
    cur = [];
  };
  words.forEach((w, i) => {
    const prev = cur[cur.length - 1];
    const len = cur.reduce((a, x) => a + x.w.length + 1, 0) + w.w.length;
    if (prev && (w.s - prev.e > gap || cur.length >= maxWords || len > maxChars)) flush();
    cur.push(w);
    if (/[.!?;:,]$/.test(w.w) && cur.length >= 2) flush();
  });
  flush();
  return chunks.map((c, i) => ({
    words: c,
    start: c[0].s - 0.05,
    end: chunks[i + 1] ? Math.min(chunks[i + 1][0].s - 0.05, c[c.length - 1].e + 0.6) : c[c.length - 1].e + 0.6,
  }));
};

// Sous-titres karaoké : mots dits en plein, mots à venir atténués, une ligne, petite boîte.
// hide : intervalles [début, fin] (s) sans sous-titres ; yAt(t) : position verticale (fraction de la hauteur).
export const Subtitles = ({sub, th, hide = [], yAt}) => {
  const frame = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const t = frame / fps;
  const chunks = useMemo(() => chunkWords(sub.words || [], sub.maxWords || 4, sub.maxChars || 26), [sub]);
  if (hide.some(([a, b]) => t >= a && t < b)) return null;
  const c = chunks.find((x) => t >= x.start && t < x.end);
  if (!c) return null;
  const f0 = Math.round(c.start * fps);
  const s = spring({frame: frame - f0, fps, config: {damping: 14, mass: 0.4}});
  const y = yAt ? yAt(t) : (sub.y ?? 0.5);
  return (
    <div style={{position: 'absolute', left: 0, width, top: height * y, display: 'flex', justifyContent: 'center', transform: `translateY(-50%) scale(${0.92 + 0.08 * s})`}}>
      <div style={{background: th.subBox, borderRadius: 12, padding: '10px 22px', fontFamily: FONT, fontWeight: 700, fontSize: sub.size || 44,
        boxShadow: '0 6px 20px rgba(0,0,0,.25)', maxWidth: width * 0.86, textAlign: 'center', lineHeight: 1.2}}>
        {c.words.map((w, i) => {
          const said = t >= w.s - 0.02;
          const now = said && t < w.e;
          const col = !said ? th.subDim : now && th.subSpoken ? th.subSpoken : th.subText;
          return <span key={i} style={{color: col}}>{(i ? ' ' : '') + w.w}</span>;
        })}
      </div>
    </div>
  );
};
