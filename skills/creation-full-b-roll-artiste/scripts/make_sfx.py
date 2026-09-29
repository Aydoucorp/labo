#!/usr/bin/env python3
"""make_sfx.py : genere les trois effets sonores synthetiques du skill (aucun fichier tiers).

  whoosh_soft.wav : bruit blanc filtre passe-bande balaye 200 Hz -> 4 kHz sur 350 ms, enveloppe
  tick_soft.wav   : clic de 30 ms
  impact_low.wav  : sinus 60 Hz avec decroissance sur 400 ms

Ecrits en WAV 48 kHz mono 16 bits dans assets/sfx/ (ou --out). Appele
automatiquement par build_timeline.py si les fichiers manquent.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy import signal
from scipy.io import wavfile

from montage_common import SFX_DIR, log

SR = 48000


def _norm(x: np.ndarray, peak: float = 0.9) -> np.ndarray:
    m = float(np.max(np.abs(x))) or 1.0
    return (x / m * peak).astype(np.float32)


def whoosh(dur: float = 0.35) -> np.ndarray:
    n = int(SR * dur)
    rng = np.random.default_rng(7)
    noise = rng.standard_normal(n).astype(np.float32)
    # Balayage passe-bande 200 Hz -> 4 kHz par blocs courts
    block = 512
    out = np.zeros(n, dtype=np.float32)
    zi = None
    for i in range(0, n, block):
        p = i / n
        fc = 200.0 * (4000.0 / 200.0) ** p
        low = max(40.0, fc / 1.6)
        high = min(SR / 2 - 100.0, fc * 1.6)
        sos = signal.butter(2, [low, high], btype="band", fs=SR, output="sos")
        seg = noise[i:i + block]
        if zi is None:
            zi = signal.sosfilt_zi(sos) * seg[0]
        y, zi = signal.sosfilt(sos, seg, zi=zi)
        out[i:i + block] = y
    t = np.linspace(0, 1, n)
    env = np.sin(np.pi * t) ** 1.5
    return _norm(out * env, 0.8)


def tick(dur: float = 0.03) -> np.ndarray:
    n = int(SR * dur)
    t = np.arange(n) / SR
    click = np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 180) + 0.4 * np.sin(2 * np.pi * 3600 * t) * np.exp(-t * 300)
    rng = np.random.default_rng(3)
    click += 0.15 * rng.standard_normal(n) * np.exp(-t * 400)
    return _norm(click, 0.7)


def impact(dur: float = 0.4) -> np.ndarray:
    n = int(SR * dur)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * 60 * t) * np.exp(-t * 7)
    # Petite attaque pour la lisibilite sur enceintes de telephone
    attack = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 60) * 0.35
    x = body + attack
    fade = np.minimum(1.0, (n - np.arange(n)) / (0.02 * SR))
    return _norm(x * fade, 0.95)


def write(path: Path, x: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    wavfile.write(str(path), SR, (np.clip(x, -1, 1) * 32767).astype(np.int16))


def ensure_sfx(out_dir: Path = SFX_DIR, force: bool = False) -> dict[str, Path]:
    files = {"whoosh": out_dir / "whoosh_soft.wav", "tick": out_dir / "tick_soft.wav", "impact": out_dir / "impact_low.wav"}
    gens = {"whoosh": whoosh, "tick": tick, "impact": impact}
    for key, path in files.items():
        if force or not path.exists():
            write(path, gens[key]())
            log(f"sfx genere : {path}")
    return files


def main() -> None:
    ap = argparse.ArgumentParser(description="Genere les sfx synthetiques (whoosh, tick, impact).",
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--out", default=str(SFX_DIR), help="dossier de sortie (defaut : assets/sfx du skill)")
    ap.add_argument("--force", action="store_true", help="regenere meme si present")
    args = ap.parse_args()
    ensure_sfx(Path(args.out), args.force)


if __name__ == "__main__":
    main()
