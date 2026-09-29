// Composition principale : dessine le montage a sa taille native (timeline.width x
// timeline.height) puis le met a l'echelle de la composition (utile pour Preview 540x960).
import React from 'react';
import {AbsoluteFill, useVideoConfig} from 'remotion';
import type {Caption} from '@remotion/captions';
import type {MainProps, Timeline} from './types';
import {useJson, useMontserrat} from './lib/load';
import {ClipLayer} from './components/ClipLayer';
import {Captions} from './components/Captions';
import {Overlays} from './components/Overlays';
import {AudioLayer} from './components/AudioLayer';
import {Logo, ProgressBar} from './components/Chrome';

// Safe zone TikTok par defaut (profiles.json platform_safe_zone.tiktok)
const DEFAULT_SAFE = {top: 220, bottom: 420, left: 60, right: 130};

export const Main: React.FC<MainProps> = ({timelinePath, timeline: tlProp, captions: capProp, progressBar, logo}) => {
  const {width, height} = useVideoConfig();
  const timeline = useJson<Timeline>(timelinePath ?? null, tlProp ?? null);
  const captions = useJson<{captions: Caption[]}>(
    timeline && !capProp ? timeline.captions.file : null,
    capProp ? {captions: capProp} : null,
  );
  const fontsReady = useMontserrat();

  if (!timeline || !fontsReady) {
    return <AbsoluteFill style={{backgroundColor: 'black'}} />;
  }

  const safe = timeline.safe_zone ?? DEFAULT_SAFE;
  const s = width / timeline.width;
  const caps = captions?.captions ?? [];

  return (
    <AbsoluteFill style={{backgroundColor: 'black', overflow: 'hidden'}}>
      <div
        style={{
          position: 'absolute',
          left: 0,
          top: 0,
          width: timeline.width,
          height: timeline.height,
          transformOrigin: 'top left',
          scale: String(s),
          overflow: 'hidden',
        }}
      >
        <ClipLayer clips={timeline.clips} totalFrames={timeline.duration_frames} />
        <Overlays overlays={timeline.overlays ?? []} width={timeline.width} height={timeline.height} sidePad={Math.max(safe.left, safe.right)} />
        <Captions
          captions={caps}
          hookEndFrame={timeline.captions.hook_end_frame}
          style={timeline.captions.style}
          hookStyle={timeline.captions.hook_style}
          width={timeline.width}
          height={timeline.height}
          safeZone={safe}
        />
        {progressBar ? <ProgressBar width={timeline.width} height={timeline.height} safe={safe} /> : null}
        {logo ? <Logo src={logo} safe={safe} /> : null}
      </div>
      <AudioLayer timeline={timeline} />
    </AbsoluteFill>
  );
};
