import {staticFile} from 'remotion';
import {loadFont} from '@remotion/fonts';

// Polices locales (public/fonts, licence OFL) : aucun accès réseau nécessaire au rendu.
// Montserrat (texte principal, graisses 500 à 900) et Playfair Display italique (mots mis en valeur).
loadFont({family: 'Montserrat', url: staticFile('fonts/Montserrat.woff2'), weight: '500 900', format: 'woff2'});
loadFont({family: 'Playfair Display', url: staticFile('fonts/PlayfairDisplay-Italic.woff2'), style: 'italic', weight: '600 700', format: 'woff2'});
export const FONT = 'Montserrat, Arial, sans-serif';
export const SERIF = '"Playfair Display", Georgia, serif';

export const DEFAULT_THEME = {
  accent: '#E3262F', // couleur principale (bandeau, mots clés, chiffres)
  accent2: '#FFD400', // surligneur, chiffres de chapitre
  subBox: '#FFFFFF', // fond de la boîte de sous-titres
  subText: '#141414', // mot déjà prononcé
  subDim: '#A3A3A3', // mot à venir
  subSpoken: null, // couleur du mot en cours (null = subText)
  bannerBg: '#D7141A',
  bannerText: '#FFFFFF',
  eduBg: '#1531C9',
  infoBg: '#FFF1EA',
  infoText: '#4A2A1A',
  cardBg: '#000000',
  followBlue: '#1D8CF8',
};

export const theme = (props) => ({...DEFAULT_THEME, ...(props.theme || {})});

// Chemin média : relatif au dossier public/ ou URL complète.
export const src = (p) => (!p ? null : /^https?:\/\//.test(p) ? p : staticFile(p));

// Conversion secondes → images, toujours à partir des temps ABSOLUS (pas de cumul d'arrondis).
export const fr = (sec, fps) => Math.round(sec * fps);

export const isVideo = (p) => /\.(mp4|mov|webm|m4v)$/i.test(p || '');

// Temps absolu (secondes) de l'image courante, à partir de l'image relative d'une Sequence.
export const absT = (frame, fromSec, fps) => fromSec + frame / fps;

export const fmtNumber = (n, locale = 'fr-FR') => Math.round(n).toLocaleString(locale).replace(/ /g, ' ');
