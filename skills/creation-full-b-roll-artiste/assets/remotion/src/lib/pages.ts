// Pagination des sous-titres karaoke : pages de 3 a 4 mots construites avec
// createTikTokStyleCaptions, puis decoupees pour ne jamais depasser maxTokens.
// La coupe forcee sur ponctuation forte vient de pageBreakAfter (make_captions.py).
import {createTikTokStyleCaptions} from '@remotion/captions';
import type {Caption, TikTokToken} from '@remotion/captions';

export type CaptionPageData = {
  startMs: number;
  endMs: number;
  tokens: TikTokToken[];
};

export const COMBINE_MS = 900;
export const MAX_TOKENS = 4;
// Maintien d'une page apres son dernier mot (avant la page suivante)
const HOLD_AFTER_MS = 700;

export const buildPages = (captions: Caption[], maxTokens: number = MAX_TOKENS): CaptionPageData[] => {
  if (!captions || captions.length === 0) {
    return [];
  }
  const {pages} = createTikTokStyleCaptions({
    captions,
    combineTokensWithinMilliseconds: COMBINE_MS,
  });

  // Decoupe des pages trop longues en morceaux de maxTokens (equilibres)
  const chunks: TikTokToken[][] = [];
  for (const page of pages) {
    const toks = page.tokens;
    if (toks.length <= maxTokens) {
      chunks.push(toks);
      continue;
    }
    const n = Math.ceil(toks.length / maxTokens);
    const size = Math.ceil(toks.length / n);
    for (let i = 0; i < toks.length; i += size) {
      chunks.push(toks.slice(i, i + size));
    }
  }

  const out: CaptionPageData[] = [];
  for (let i = 0; i < chunks.length; i++) {
    const toks = chunks[i].map((t, j) => ({
      ...t,
      // Premier mot d'une page : pas d'espace devant (convention Remotion)
      text: j === 0 ? t.text.replace(/^\s+/, '') : t.text,
    }));
    const startMs = toks[0].fromMs;
    const lastTo = toks[toks.length - 1].toMs;
    const next = chunks[i + 1];
    const nextStart = next ? next[0].fromMs : Infinity;
    const endMs = Math.min(nextStart, lastTo + HOLD_AFTER_MS);
    out.push({startMs, endMs, tokens: toks});
  }
  return out;
};
