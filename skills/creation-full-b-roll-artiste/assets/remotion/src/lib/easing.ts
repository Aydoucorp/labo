// Fonctions d'easing utilisees par les transitions et les animations.
import {Easing} from 'remotion';

export const easeInOut = Easing.inOut(Easing.cubic);
export const easeOut = Easing.out(Easing.cubic);
export const easeIn = Easing.in(Easing.quad);

// Bosse symetrique 0 -> 1 -> 0 (pour le flou au milieu d'une transition)
export const bump = (p: number): number => Math.sin(Math.PI * Math.min(1, Math.max(0, p)));

// Borne une valeur dans [0, 1]
export const clamp01 = (v: number): number => Math.min(1, Math.max(0, v));
