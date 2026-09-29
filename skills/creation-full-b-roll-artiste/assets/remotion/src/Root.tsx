// Racine : compositions "Main" (taille native du timeline) et "Preview" (540x960).
// durationInFrames, fps, width et height viennent du timeline.json passe en props
// (prop `timeline`) ou charge depuis public/ (prop `timelinePath`).
import React from 'react';
import {Composition, type CalculateMetadataFunction} from 'remotion';
import type {Caption} from '@remotion/captions';
import {Main} from './Main';
import type {MainProps, Timeline} from './types';
import {fetchJson} from './lib/load';

const loadTimeline = async (props: MainProps): Promise<Timeline> => {
  if (props.timeline) {
    return props.timeline;
  }
  if (props.timelinePath) {
    return fetchJson<Timeline>(props.timelinePath);
  }
  throw new Error('Aucun timeline : passez la prop `timeline` (objet) ou `timelinePath` (fichier dans public/)');
};

const makeCalculateMetadata = (scale: number): CalculateMetadataFunction<MainProps> => {
  return async ({props}) => {
    const timeline = await loadTimeline(props);
    let captions: Caption[] | null = props.captions ?? null;
    if (!captions && timeline.captions?.file) {
      const c = await fetchJson<{captions: Caption[]}>(timeline.captions.file);
      captions = c.captions;
    }
    return {
      durationInFrames: Math.max(1, timeline.duration_frames),
      fps: timeline.fps,
      width: Math.round(timeline.width * scale),
      height: Math.round(timeline.height * scale),
      props: {...props, timeline, captions},
    };
  };
};

const defaultProps: MainProps = {
  timelinePath: 'render/timeline.json',
  timeline: null,
  captions: null,
  progressBar: false,
  logo: null,
};

export const Root: React.FC = () => {
  return (
    <>
      <Composition
        id="Main"
        component={Main}
        durationInFrames={300}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={defaultProps}
        calculateMetadata={makeCalculateMetadata(1)}
      />
      <Composition
        id="Preview"
        component={Main}
        durationInFrames={300}
        fps={30}
        width={540}
        height={960}
        defaultProps={defaultProps}
        calculateMetadata={makeCalculateMetadata(0.5)}
      />
    </>
  );
};
