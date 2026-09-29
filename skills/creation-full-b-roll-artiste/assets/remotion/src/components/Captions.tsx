// Sous-titres karaoke : pages de 3 a 4 mots, mot en cours mis en avant.
// Style "default" : Montserrat 800, 68 px, blanc, contour noir, a 60 % de la hauteur.
// Style "red-box" (hook) : texte blanc 76 px sur boite rouge arrondie au centre.
import React, {useMemo} from 'react';
import {AbsoluteFill, Sequence, interpolate, spring, useCurrentFrame, useVideoConfig} from 'remotion';
import type {Caption, TikTokToken} from '@remotion/captions';
import {buildPages, type CaptionPageData} from '../lib/pages';

type Props = {
  captions: Caption[];
  hookEndFrame: number;
  style: string;
  hookStyle: string;
  // Dimensions de reference du montage (1080x1920)
  width: number;
  height: number;
  safeZone: {top: number; bottom: number; left: number; right: number};
};

const FONT = 'Montserrat, "Montserrat ExtraBold", Arial, sans-serif';

// Contour noir : paint-order stroke + ombre douce
const strokeStyle = (px: number): React.CSSProperties => ({
  WebkitTextStroke: `${px}px #000`,
  paintOrder: 'stroke fill',
  textShadow: '0 6px 18px rgba(0,0,0,0.55)',
});

type WordProps = {
  token: TikTokToken;
  absMs: number;
  fps: number;
  frame: number;
  pageStartMs: number;
  activeScale: number;
};

// Un mot : pop 1.15 -> activeScale a son apparition, activeScale tant qu'il est
// en cours, 1.0 une fois passe. Les mots a venir sont blancs a 0.85 d'opacite.
const Word: React.FC<WordProps> = ({token, absMs, fps, frame, pageStartMs, activeScale}) => {
  const isPast = token.toMs <= absMs;
  const isActive = token.fromMs <= absMs && !isPast;
  const isFuture = token.fromMs > absMs;

  // Frame locale (dans la page) a laquelle le mot devient actif
  const activeAtFrame = ((token.fromMs - pageStartMs) / 1000) * fps;
  const pop = spring({
    frame: frame - activeAtFrame,
    fps,
    config: {damping: 200},
    durationInFrames: 4,
  });
  let scale = 1;
  if (isActive) {
    scale = interpolate(pop, [0, 1], [1.15, activeScale]);
  }

  return (
    <span
      style={{
        display: 'inline-block',
        whiteSpace: 'pre',
        color: '#fff',
        opacity: isFuture ? 0.85 : 1,
        scale: String(scale),
        transformOrigin: '50% 60%',
      }}
    >
      {token.text}
    </span>
  );
};

const DefaultPage: React.FC<{page: CaptionPageData; width: number; height: number; safe: Props['safeZone']}> = ({
  page,
  width,
  height,
  safe,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const absMs = page.startMs + (frame / fps) * 1000;
  // Centre du bloc a 60 % de la hauteur, borne dans la safe zone
  const centerY = Math.min(height - safe.bottom - 120, Math.max(safe.top + 120, height * 0.6));
  return (
    <AbsoluteFill style={{justifyContent: 'flex-start', alignItems: 'center'}}>
      <div
        style={{
          position: 'absolute',
          top: centerY,
          left: 0,
          width,
          translate: '0 -50%',
          padding: `0 ${Math.max(safe.left, safe.right)}px`,
          boxSizing: 'border-box',
          textAlign: 'center',
          fontFamily: FONT,
          fontWeight: 800,
          fontSize: 68,
          lineHeight: 1.15,
          wordSpacing: '0.22em',
          ...strokeStyle(6),
        }}
      >
        {page.tokens.map((t, i) => (
          <Word key={`${t.fromMs}-${i}`} token={t} absMs={absMs} fps={fps} frame={frame} pageStartMs={page.startMs} activeScale={1.08} />
        ))}
      </div>
    </AbsoluteFill>
  );
};

const RedBoxPage: React.FC<{page: CaptionPageData; width: number; height: number; safe: Props['safeZone']}> = ({
  page,
  width,
  height,
  safe,
}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const absMs = page.startMs + (frame / fps) * 1000;
  const pop = spring({frame, fps, config: {damping: 200}, durationInFrames: 5});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center'}}>
      <div
        style={{
          position: 'absolute',
          top: height * 0.5,
          left: 0,
          width,
          translate: '0 -50%',
          // La boite est au centre vertical, hors de la colonne d'icones : marge laterale reduite
          padding: `0 ${safe.left + 20}px`,
          boxSizing: 'border-box',
          display: 'flex',
          justifyContent: 'center',
        }}
      >
        <div
          style={{
            display: 'inline-block',
            backgroundColor: '#E0202A',
            borderRadius: 18,
            padding: '18px 28px',
            boxShadow: '0 10px 30px rgba(0,0,0,0.35)',
            fontFamily: FONT,
            fontWeight: 800,
            fontSize: 76,
            lineHeight: 1.12,
            wordSpacing: '0.18em',
            color: '#fff',
            textAlign: 'center',
            scale: String(interpolate(pop, [0, 1], [0.86, 1])),
            opacity: interpolate(pop, [0, 1], [0.4, 1]),
          }}
        >
          {page.tokens.map((t, i) => (
            <Word key={`${t.fromMs}-${i}`} token={t} absMs={absMs} fps={fps} frame={frame} pageStartMs={page.startMs} activeScale={1.06} />
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const Captions: React.FC<Props> = ({captions, hookEndFrame, hookStyle, width, height, safeZone}) => {
  const {fps} = useVideoConfig();
  const pages = useMemo(() => buildPages(captions), [captions]);
  const hookEndMs = (hookEndFrame / fps) * 1000;

  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      {pages.map((page, i) => {
        // Une page dont le premier mot est dans le HOOK prend le style hook et s'arrete a la fin du hook
        const inHook = hookStyle === 'red-box' && page.startMs < hookEndMs - 1;
        const from = Math.round((page.startMs / 1000) * fps);
        const to = inHook ? Math.min(hookEndFrame, Math.round((page.endMs / 1000) * fps)) : Math.round((page.endMs / 1000) * fps);
        const dur = to - from;
        if (dur <= 0) {
          return null;
        }
        return (
          <Sequence key={i} name={`caption ${i}`} from={from} durationInFrames={dur} layout="none">
            {inHook ? (
              <RedBoxPage page={page} width={width} height={height} safe={safeZone} />
            ) : (
              <DefaultPage page={page} width={width} height={height} safe={safeZone} />
            )}
          </Sequence>
        );
      })}
    </AbsoluteFill>
  );
};
