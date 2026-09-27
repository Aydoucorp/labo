import React from 'react';
import {useCurrentFrame, useVideoConfig, spring} from 'remotion';
import {FONT, SERIF} from '../lib';

// Typographie cinétique : chaque mot apparaît à son temps absolu t (secondes de la voix maître).
// words[] : {t, text, style?: "normal"|"giant"|"serif"|"accent"|"light", color?, br?: true (retour à la ligne avant)}
export const Kinetic = ({words, segStart, th, size = 64, align = 'left', color = '#FFFFFF'}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const lines = [];
  let cur = [];
  words.forEach((w) => {
    if (w.br && cur.length) {
      lines.push(cur);
      cur = [];
    }
    cur.push(w);
  });
  if (cur.length) lines.push(cur);
  return (
    <div style={{width: '100%', textAlign: align, fontFamily: FONT}}>
      {lines.map((ln, li) => (
        <div key={li} style={{display: 'flex', flexWrap: 'wrap', alignItems: 'baseline', gap: size * 0.25, justifyContent: align === 'right' ? 'flex-end' : align === 'center' ? 'center' : 'flex-start'}}>
          {ln.map((w, i) => {
            const appear = Math.round((w.t - segStart) * fps) - 1;
            if (frame < appear) return <span key={i} style={{opacity: 0}}>{w.text}</span>;
            const s = spring({frame: frame - appear, fps, config: {damping: 13, mass: 0.5}});
            const st = w.style || 'normal';
            const base = {display: 'inline-block', opacity: Math.min(1, s * 1.4), transform: `translateY(${(1 - s) * size * 0.4}px) scale(${0.9 + 0.1 * s})`, lineHeight: 1.05};
            const styles = {
              normal: {fontSize: size, fontWeight: 800, color: w.color || color},
              light: {fontSize: size * 0.8, fontWeight: 600, color: w.color || color},
              accent: {fontSize: size, fontWeight: 800, color: w.color || th.accent},
              serif: {fontSize: size * 1.15, fontFamily: SERIF, fontStyle: 'italic', fontWeight: 700, color: w.color || color},
              giant: {fontSize: size * 3.2, fontWeight: 900, color: w.color || th.accent2, lineHeight: 0.9, letterSpacing: -4},
            };
            return <span key={i} style={{...base, ...(styles[st] || styles.normal)}}>{w.text}</span>;
          })}
        </div>
      ))}
    </div>
  );
};
