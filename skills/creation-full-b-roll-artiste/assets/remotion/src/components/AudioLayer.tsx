// Mixage audio : voix off a volume 1, musique optionnelle a music_db (en boucle),
// effets sonores aux frames prevus. Les ambiances sont portees par chaque clip.
import React from 'react';
import {Audio, Sequence} from 'remotion';
import type {Timeline} from '../types';
import {dbToGain} from '../lib/audio';
import {resolveSrc} from '../lib/load';

// Duree maximale allouee a un sfx (les fichiers sont courts, la sequence coupe au besoin)
const SFX_MAX_FRAMES = 45;

export const AudioLayer: React.FC<{timeline: Timeline}> = ({timeline}) => {
  const {audio, sfx, duration_frames: total} = timeline;
  return (
    <>
      {audio.vo ? <Audio src={resolveSrc(audio.vo)} volume={1} name="voix off" /> : null}
      {audio.music ? <Audio src={resolveSrc(audio.music)} volume={dbToGain(audio.music_db)} loop name="musique" /> : null}
      {sfx.map((s, i) => {
        const from = Math.max(0, Math.min(s.at_frame, total - 1));
        const dur = Math.max(1, Math.min(SFX_MAX_FRAMES, total - from));
        return (
          <Sequence key={i} name={`sfx ${i}`} from={from} durationInFrames={dur} layout="none">
            <Audio src={resolveSrc(s.src)} volume={dbToGain(s.db)} />
          </Sequence>
        );
      })}
    </>
  );
};
