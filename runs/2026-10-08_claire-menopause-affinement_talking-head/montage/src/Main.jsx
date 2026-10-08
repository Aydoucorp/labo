import React from 'react';
import {AbsoluteFill, Audio, Sequence} from 'remotion';
import {theme, src, fr} from './lib';
import {AvatarSeg, SplitSeg, CardSeg, LetterboxSeg, FullSeg, PlainSeg, CollageSeg, InfoListSeg, KineticSeg, CircleWipe} from './components/Segments';
import {BigNumber, DocCard, Chapter, Cutout, Counter, Label, TextPop, Follow, Flash, Inset} from './components/Overlays';
import {Subtitles} from './components/Subtitles';

const SEGMENTS = {
  avatar: AvatarSeg, split: SplitSeg, card: CardSeg, letterbox: LetterboxSeg, full: FullSeg, edu: FullSeg,
  image: FullSeg, plain: PlainSeg, collage: CollageSeg, infolist: InfoListSeg, kinetic: KineticSeg,
};
const OVERLAYS = {
  bignumber: BigNumber, doc: DocCard, chapter: Chapter, cutout: Cutout, counter: Counter, label: Label,
  text: TextPop, follow: Follow, flash: Flash, inset: Inset,
};
// Types sans sous-titres standards par défaut (ils ont leur propre texte à l'écran).
const NO_SUBS = new Set(['split', 'edu', 'kinetic', 'letterbox', 'infolist']);
const SUB_Y = {avatar: 0.5, card: 0.52, full: 0.5, image: 0.5, collage: 0.5, plain: 0.82};
// Surimpressions qui remplacent les sous-titres pendant leur présence (comme dans les vidéos de référence).
const OV_NO_SUBS = new Set(['bignumber', 'doc', 'chapter']);

export const Main = (props) => {
  const fps = props.fps || 30;
  const th = theme(props);
  const segs = props.segments || [];
  const ovs = props.overlays || [];

  const hide = segs.filter((s) => (s.subs === false) || (NO_SUBS.has(s.type) && s.subs !== true)).map((s) => [s.start, s.end]);
  (props.subtitles?.hide || []).forEach((h) => hide.push(h));
  ovs.filter((o) => o.hideSubs === true || (OV_NO_SUBS.has(o.type) && o.hideSubs !== false)).forEach((o) => hide.push([o.start, o.end]));
  const yAt = (t) => {
    const o = ovs.find((x) => x.subY != null && t >= x.start && t < x.end);
    if (o) return o.subY;
    const s = segs.find((x) => t >= x.start && t < x.end);
    return s ? (s.subY ?? SUB_Y[s.type] ?? props.subtitles?.y ?? 0.5) : 0.5;
  };

  return (
    <AbsoluteFill style={{backgroundColor: props.bg || '#000'}}>
      {segs.map((seg, i) => {
        const C = SEGMENTS[seg.type];
        if (!C) return null;
        const from = fr(seg.start, fps);
        const dur = Math.max(1, fr(seg.end, fps) - from);
        const inner = <C seg={seg} fps={fps} th={th} durFrames={dur} />;
        return (
          <Sequence key={`s${i}`} from={from} durationInFrames={dur} name={`${i} ${seg.type}`}>
            {seg.enter === 'circle' ? <CircleWipe cx={seg.wipeX || '70%'} cy={seg.wipeY || '15%'}>{inner}</CircleWipe> : inner}
          </Sequence>
        );
      })}

      {ovs.map((o, i) => {
        const C = OVERLAYS[o.type];
        if (!C) return null;
        const start = o.type === 'flash' ? o.t - (o.dur || 0.3) / 2 : o.start;
        const end = o.type === 'flash' ? o.t + (o.dur || 0.3) / 2 : o.end;
        const from = fr(start, fps);
        const dur = Math.max(1, fr(end, fps) - from);
        return (
          <Sequence key={`o${i}`} from={from} durationInFrames={dur} name={`ov ${o.type}`} layout="absolute-fill">
            <C o={{...o, start}} th={th} durFrames={dur} />
          </Sequence>
        );
      })}

      {props.subtitles ? <Subtitles sub={props.subtitles} th={th} hide={hide} yAt={yAt} /> : null}

      {props.audio ? <Audio src={src(props.audio)} volume={props.audioVolume ?? 1} /> : null}
      {props.music ? <Audio src={src(props.music.src)} volume={props.music.volume ?? 0.08} loop /> : null}
    </AbsoluteFill>
  );
};
