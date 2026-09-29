// Types TypeScript miroir du contrat timeline.json (CONTRACTS.md section 8)
// et des props de la composition.
import type {Caption} from '@remotion/captions';

export type TransitionType =
  | 'cut'
  | 'whip'
  | 'zoomthrough'
  | 'flash'
  | 'dissolve'
  | 'wipe'
  | 'punchcut';

export type TransitionDir = 'left' | 'right' | 'up' | 'down' | null;

export type Transition = {
  type: TransitionType;
  frames: number;
  dir: TransitionDir;
};

export type KenBurns = {
  from: number;
  to: number;
  origin: [number, number];
};

export type Punch = {
  at_frame: number;
  scale: number;
  frames: number;
};

export type Clip = {
  shot_id: string;
  src: string;
  from_frame: number;
  duration_frames: number;
  trim_before_frames: number;
  speed: number;
  kenburns: KenBurns | null;
  punch: Punch | null;
  transition_in: Transition;
  ambience: boolean;
  ambience_db: number;
  // Champs d'extension (facultatifs, ignores par Remotion)
  section?: string;
  source_rush?: string | null;
};

export type Overlay = {
  type: 'text';
  text: string;
  from_frame: number;
  duration_frames: number;
  style: 'stat';
  anchor: 'center';
};

export type Sfx = {
  src: string;
  at_frame: number;
  db: number;
};

export type Timeline = {
  schema: string;
  fps: number;
  width: number;
  height: number;
  duration_frames: number;
  profile: 'ADS' | 'EDU';
  audio: {
    vo: string;
    music: string | null;
    music_db: number;
    ambience_db: number;
  };
  clips: Clip[];
  captions: {
    file: string;
    style: string;
    hook_style: string;
    hook_end_frame: number;
  };
  overlays: Overlay[];
  sfx: Sfx[];
  endcard: unknown;
  safe_zone?: {top: number; bottom: number; left: number; right: number};
};

export type MainProps = {
  // Chemin du timeline.json relatif a public/ (charge par calculateMetadata)
  timelinePath?: string | null;
  // Ou bien le timeline directement en prop
  timeline?: Timeline | null;
  // Captions chargees par calculateMetadata (sinon lues depuis timeline.captions.file)
  captions?: Caption[] | null;
  // Barre de progression fine en bas de la safe zone
  progressBar?: boolean;
  // Logo PNG dans public/ (chemin relatif), null pour aucun
  logo?: string | null;
};
