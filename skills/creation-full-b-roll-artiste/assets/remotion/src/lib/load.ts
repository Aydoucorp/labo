// Chargement de ressources : JSON depuis public/ (staticFile) et polices locales,
// en retenant le rendu avec delayRender tant que ce n'est pas pret.
import {useEffect, useState} from 'react';
import {cancelRender, continueRender, delayRender, staticFile} from 'remotion';

// Resout un chemin de ressource : URL absolue telle quelle, sinon staticFile()
export const resolveSrc = (src: string): string => {
  if (/^(https?:)?\/\//.test(src) || src.startsWith('data:') || src.startsWith('blob:')) {
    return src;
  }
  return staticFile(src);
};

export const fetchJson = async <T,>(path: string): Promise<T> => {
  const res = await fetch(resolveSrc(path));
  if (!res.ok) {
    throw new Error(`Impossible de charger ${path} (HTTP ${res.status})`);
  }
  return (await res.json()) as T;
};

// Hook : charge un JSON via staticFile et bloque le rendu jusqu'a reception.
export const useJson = <T,>(path: string | null | undefined, initial: T | null): T | null => {
  const [data, setData] = useState<T | null>(initial);
  const [handle] = useState(() => (path && !initial ? delayRender(`chargement ${path}`) : null));

  useEffect(() => {
    if (!path || initial || handle === null) {
      return;
    }
    fetchJson<T>(path)
      .then((d) => {
        setData(d);
        continueRender(handle);
      })
      .catch((e) => cancelRender(e));
  }, [path, initial, handle]);

  return data;
};

// Polices Montserrat locales (public/fonts/), chargees par l'API FontFace.
const FONTS: Array<{file: string; weight: string}> = [
  {file: 'fonts/Montserrat-ExtraBold.ttf', weight: '800'},
  {file: 'fonts/Montserrat-Bold.ttf', weight: '700'},
];

let fontsPromise: Promise<void> | null = null;

export const loadMontserrat = (): Promise<void> => {
  if (fontsPromise) {
    return fontsPromise;
  }
  fontsPromise = (async () => {
    if (typeof document === 'undefined' || !('fonts' in document)) {
      return;
    }
    await Promise.all(
      FONTS.map(async ({file, weight}) => {
        const face = new FontFace('Montserrat', `url(${staticFile(file)}) format('truetype')`, {
          weight,
          style: 'normal',
          display: 'block',
        });
        const loaded = await face.load();
        (document.fonts as unknown as {add: (f: FontFace) => void}).add(loaded);
      }),
    );
    await document.fonts.ready;
  })();
  return fontsPromise;
};

// Hook : retient le rendu jusqu'au chargement des polices.
export const useMontserrat = (): boolean => {
  const [ready, setReady] = useState(false);
  const [handle] = useState(() => delayRender('chargement des polices Montserrat'));
  useEffect(() => {
    loadMontserrat()
      .then(() => {
        setReady(true);
        continueRender(handle);
      })
      .catch((e) => cancelRender(e));
  }, [handle]);
  return ready;
};
