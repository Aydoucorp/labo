#!/usr/bin/env python3
"""
validate_brief.py : vérifie un brief.json (schéma broll-director/brief/1)
contre les contraintes de CONTRACTS.md (section 4) et le profil de rythme
de assets/profiles.json.

Usage :
    python3 validate_brief.py brief.json [--profiles assets/profiles.json] [--fix-slugs] [--strict]

Code de sortie : 0 si aucune erreur bloquante, 1 sinon (2 si le fichier est illisible).
Bibliothèque standard uniquement (Python 3.11).
"""

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path

SCHEMA = "broll-director/brief/1"
TOL = 0.002  # tolérance en secondes pour les comparaisons de temps

PROFILES = {"ADS", "EDU"}
PLATFORMS = {"tiktok", "reels", "shorts", "youtube", "meta-feed"}
FUNCTIONS = {"HOOK", "PROMESSE", "PROBLEME", "AGITATION", "MECANISME", "PREUVE",
             "PRODUIT", "BENEFICE", "OBJECTION", "CTA", "CHUTE"}
SECTIONS = {"HOOK", "PROB", "MECA", "PREUVE", "PROD", "BENEF", "OBJ", "CTA", "CHUTE"}
ABSTRACTIONS = {"concret", "consequence", "mecanisme", "abstrait", "emotion"}
SHOT_TYPES = {"STOCK", "UGC", "PRODUIT", "3DSCI", "MOTION", "SCREEN", "SOCIAL", "IAGEN"}
VALUES = {"large", "moyen", "detail", "macro", "topdown", "pov"}
CAMERAS = {"static", "push", "pull", "pan", "handheld", "orbit", "tilt"}
ORIENTATIONS = {"vertical", "horizontal", "any"}

# Types de plans comptés comme "produit" pour la part minimale (product_share_min)
PRODUCT_TYPES = {"PRODUIT", "UGC"}
# Sections exclues du "corps" pour le calcul de la part produit
NON_BODY_SECTIONS = {"HOOK"}

SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FILENAME_RE = re.compile(r"^(?P<id>[^_]+)_(?P<section>[^_]+)_(?P<type>[^_]+)_(?P<slug>[^_]+)\.mp4$")

# Mots vides ignorés lors de la génération de slug
STOPWORDS = {
    "le", "la", "les", "un", "une", "des", "du", "de", "d", "l", "et", "ou", "a", "au", "aux",
    "en", "sur", "sous", "dans", "avec", "sans", "pour", "par", "qui", "que", "se", "sa", "son",
    "ses", "ce", "cette", "ces", "est", "c", "il", "elle", "on", "the", "of", "and", "plan",
    "vue", "gros", "tres", "puis", "vers", "pendant", "encore", "leger", "legere", "lentement",
}


def slugify(text, max_words=4):
    """Fabrique un slug ascii (a-z, 0-9, tirets) à partir d'une description."""
    if not text:
        return "plan"
    norm = unicodedata.normalize("NFKD", str(text))
    ascii_txt = "".join(ch for ch in norm if not unicodedata.combining(ch)).lower()
    ascii_txt = ascii_txt.replace("'", " ").replace("’", " ")
    words = re.findall(r"[a-z0-9]+", ascii_txt)
    kept = [w for w in words if w not in STOPWORDS and len(w) > 1]
    if not kept:
        kept = words
    slug = "-".join(kept[:max_words])
    return slug or "plan"


class Report:
    """Collecte les erreurs bloquantes et les avertissements."""

    def __init__(self):
        self.errors = []
        self.warnings = []
        self.infos = []

    def error(self, where, msg):
        self.errors.append((where, msg))

    def warn(self, where, msg):
        self.warnings.append((where, msg))

    def info(self, msg):
        self.infos.append(msg)

    def print(self, strict=False):
        print("=" * 72)
        print("RAPPORT DE VALIDATION DU BRIEF")
        print("=" * 72)
        if self.infos:
            print("\nInformations :")
            for m in self.infos:
                print(f"  . {m}")
        if self.errors:
            print(f"\nErreurs bloquantes ({len(self.errors)}) :")
            for where, msg in self.errors:
                print(f"  [ERREUR] {where} : {msg}")
        if self.warnings:
            label = "Avertissements (traités comme erreurs, mode strict)" if strict else "Avertissements"
            print(f"\n{label} ({len(self.warnings)}) :")
            for where, msg in self.warnings:
                print(f"  [AVERT.] {where} : {msg}")
        print()
        if self.errors or (strict and self.warnings):
            print(f"RESULTAT : ECHEC ({len(self.errors)} erreur(s), {len(self.warnings)} avertissement(s))")
        else:
            print(f"RESULTAT : OK ({len(self.warnings)} avertissement(s))")
        print("=" * 72)

    @property
    def failed(self):
        return bool(self.errors)


def fmt(t):
    return f"{t:.3f}s"


def is_num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def check_closed(rep, where, field, value, allowed, required=True):
    """Vérifie qu'un champ fermé prend une valeur autorisée."""
    if value is None:
        if required:
            rep.error(where, f"champ '{field}' manquant")
        return False
    if value not in allowed:
        rep.error(where, f"'{field}' = {value!r} hors des valeurs autorisées {sorted(allowed)}")
        return False
    return True


def shot_bounds(profile, section):
    """Bornes de durée d'un plan selon la section et le profil (HOOK : min 0,6 s selon le contrat)."""
    table = profile.get("shot", {})
    spec = table.get(section) or table.get("default") or {"min": 1.0, "max": 4.0, "target": 2.0}
    lo, hi, target = spec.get("min", 1.0), spec.get("max", 4.0), spec.get("target")
    if section == "HOOK":
        lo = 0.6
    return lo, hi, target


def validate(brief, profiles, rep, fix_slugs=False):
    """Applique toutes les vérifications. Retourne True si des slugs ont été modifiés."""
    changed = False

    if not isinstance(brief, dict):
        rep.error("racine", "le brief doit être un objet JSON")
        return changed

    if brief.get("schema") != SCHEMA:
        rep.error("schema", f"attendu {SCHEMA!r}, trouvé {brief.get('schema')!r}")

    # ---- projet ----
    project = brief.get("project")
    if not isinstance(project, dict):
        rep.error("project", "objet 'project' manquant")
        project = {}
    if not project.get("name"):
        rep.error("project.name", "nom de projet manquant")
    check_closed(rep, "project", "profile", project.get("profile"), PROFILES)
    check_closed(rep, "project", "platform", project.get("platform"), PLATFORMS)
    for key in ("ratio", "width", "height", "fps"):
        if project.get(key) is None:
            rep.warn("project", f"champ '{key}' absent")
    lookbook = project.get("lookbook")
    if not isinstance(lookbook, dict):
        rep.warn("project.lookbook", "look book absent (light, palette, setting, people, style_suffix_en)")
    else:
        for key in ("light", "palette", "setting", "people", "style_suffix_en"):
            if not lookbook.get(key):
                rep.warn("project.lookbook", f"champ '{key}' vide")

    profile_name = project.get("profile")
    profile = profiles.get(profile_name) if profile_name in PROFILES else None
    if profile is None:
        rep.error("profiles", f"profil {profile_name!r} introuvable dans le fichier de profils")
        profile = {"shot": {"default": {"min": 1.0, "max": 4.0, "target": 2.0}},
                   "relance_max_s": 5.0, "product_share_min": 0.0}

    # ---- audio ----
    audio = brief.get("audio")
    duration = None
    if not isinstance(audio, dict):
        rep.error("audio", "objet 'audio' manquant")
    else:
        if not audio.get("file"):
            rep.warn("audio", "champ 'file' vide")
        duration = audio.get("duration_s")
        if not is_num(duration) or duration <= 0:
            rep.error("audio", f"'duration_s' invalide : {duration!r}")
            duration = None

    # ---- diagnostic de script ----
    diag = brief.get("script_diagnostic")
    if not isinstance(diag, dict):
        rep.warn("script_diagnostic", "diagnostic de structure absent")
    else:
        for key in ("hook_ok", "promise_validated_by_s", "cta_position_pct", "loop_closed"):
            if key not in diag:
                rep.warn("script_diagnostic", f"champ '{key}' absent")

    # ---- sections ----
    sections = brief.get("sections")
    section_by_id = {}
    if not isinstance(sections, list) or not sections:
        rep.error("sections", "liste 'sections' manquante ou vide")
        sections = []
    prev_end = 0.0
    for i, sec in enumerate(sections):
        where = f"section[{i}]"
        if not isinstance(sec, dict):
            rep.error(where, "doit être un objet")
            continue
        sid = sec.get("id")
        if not check_closed(rep, where, "id", sid, SECTIONS):
            continue
        if sid in section_by_id:
            rep.error(where, f"section {sid} en double")
        s, e = sec.get("start"), sec.get("end")
        if not (is_num(s) and is_num(e)) or e <= s:
            rep.error(where, f"bornes invalides start={s!r} end={e!r}")
            continue
        section_by_id[sid] = (s, e)
        if abs(s - prev_end) > TOL:
            rep.warn(where, f"la section {sid} commence à {fmt(s)} alors que la précédente finit à {fmt(prev_end)}")
        prev_end = e
    if sections and duration is not None and abs(prev_end - duration) > TOL:
        rep.warn("sections", f"la dernière section finit à {fmt(prev_end)}, l'audio dure {fmt(duration)}")
    if section_by_id:
        if "HOOK" not in section_by_id:
            rep.error("sections", "la section HOOK est obligatoire")
        if not ({"CTA", "CHUTE"} & set(section_by_id)):
            rep.error("sections", "il faut au moins une section CTA ou CHUTE")

    # ---- beats et plans ----
    beats = brief.get("beats")
    if not isinstance(beats, list) or not beats:
        rep.error("beats", "liste 'beats' manquante ou vide")
        beats = []

    all_shots = []       # (shot, beat, where) dans l'ordre chronologique du fichier
    beat_ids = set()
    prev_beat_end = None

    for bi, beat in enumerate(beats):
        bwhere = f"beat {beat.get('id', bi) if isinstance(beat, dict) else bi}"
        if not isinstance(beat, dict):
            rep.error(bwhere, "doit être un objet")
            continue
        bid = beat.get("id")
        if not bid or not isinstance(bid, str):
            rep.error(bwhere, "identifiant 'id' manquant (chaîne)")
        elif bid in beat_ids:
            rep.error(bwhere, f"identifiant de beat {bid!r} en double")
        else:
            beat_ids.add(bid)

        section_ok = check_closed(rep, bwhere, "section", beat.get("section"), SECTIONS)
        check_closed(rep, bwhere, "function", beat.get("function"), FUNCTIONS)
        check_closed(rep, bwhere, "abstraction", beat.get("abstraction"), ABSTRACTIONS)
        energy = beat.get("energy")
        if not (isinstance(energy, int) and not isinstance(energy, bool) and 1 <= energy <= 5):
            rep.error(bwhere, f"'energy' doit être un entier de 1 à 5 (trouvé {energy!r})")

        bs, be = beat.get("start"), beat.get("end")
        if not (is_num(bs) and is_num(be)) or be <= bs:
            rep.error(bwhere, f"bornes invalides start={bs!r} end={be!r}")
            bs = be = None
        else:
            if prev_beat_end is not None and bs < prev_beat_end - TOL:
                rep.error(bwhere, f"le beat commence à {fmt(bs)} avant la fin du précédent ({fmt(prev_beat_end)})")
            prev_beat_end = be
            if section_ok and beat.get("section") in section_by_id:
                ss, se = section_by_id[beat["section"]]
                if bs < ss - TOL or be > se + TOL:
                    rep.error(bwhere, f"le beat [{fmt(bs)}, {fmt(be)}] déborde de sa section "
                                      f"{beat['section']} [{fmt(ss)}, {fmt(se)}]")
            if section_ok and beat.get("section") not in section_by_id:
                rep.error(bwhere, f"section {beat.get('section')!r} absente de la liste 'sections'")

        if not beat.get("text"):
            rep.warn(bwhere, "texte de voix vide")
        pivot_t = beat.get("pivot_t")
        if pivot_t is None:
            rep.warn(bwhere, "'pivot_t' absent")
        elif not is_num(pivot_t):
            rep.error(bwhere, f"'pivot_t' doit être un nombre (trouvé {pivot_t!r})")
        elif bs is not None and not (bs - TOL <= pivot_t <= be + TOL):
            rep.error(bwhere, f"'pivot_t' = {fmt(pivot_t)} hors du beat [{fmt(bs)}, {fmt(be)}]")
        if beat.get("pivot_word") and beat.get("text"):
            if str(beat["pivot_word"]).lower() not in str(beat["text"]).lower():
                rep.warn(bwhere, f"le mot pivot {beat['pivot_word']!r} n'apparaît pas dans le texte du beat")

        shots = beat.get("shots")
        if not isinstance(shots, list) or not shots:
            rep.error(bwhere, "aucun plan ('shots') dans ce beat")
            continue

        prev_shot_end = bs
        for si, shot in enumerate(shots):
            swhere = f"plan {shot.get('id', f'{bid}?{si}') if isinstance(shot, dict) else si}"
            if not isinstance(shot, dict):
                rep.error(swhere, "doit être un objet")
                continue
            sid = shot.get("id")
            if not sid or not isinstance(sid, str):
                rep.error(swhere, "identifiant 'id' manquant (chaîne)")
            elif bid and not sid.startswith(bid):
                rep.warn(swhere, f"l'identifiant du plan devrait commencer par celui du beat ({bid})")

            st, en = shot.get("start"), shot.get("end")
            if not (is_num(st) and is_num(en)) or en <= st:
                rep.error(swhere, f"bornes invalides start={st!r} end={en!r}")
                st = en = None
            else:
                if bs is not None and (st < bs - TOL or en > be + TOL):
                    rep.error(swhere, f"le plan [{fmt(st)}, {fmt(en)}] déborde de son beat [{fmt(bs)}, {fmt(be)}]")
                if prev_shot_end is not None and abs(st - prev_shot_end) > TOL:
                    if st > prev_shot_end:
                        rep.error(swhere, f"trou de {st - prev_shot_end:.3f}s avant ce plan (attendu {fmt(prev_shot_end)})")
                    else:
                        rep.error(swhere, f"chevauchement de {prev_shot_end - st:.3f}s avec le plan précédent")
                prev_shot_end = en

            check_closed(rep, swhere, "type", shot.get("type"), SHOT_TYPES)
            check_closed(rep, swhere, "value", shot.get("value"), VALUES)
            check_closed(rep, swhere, "camera", shot.get("camera"), CAMERAS)
            check_closed(rep, swhere, "orientation", shot.get("orientation"), ORIENTATIONS)

            stype = shot.get("type")
            if stype == "MOTION":
                if not (shot.get("overlay_text") or shot.get("description")):
                    rep.error(swhere, "un plan MOTION doit avoir 'overlay_text' ou 'description'")
            else:
                if not shot.get("query_en"):
                    rep.error(swhere, f"'query_en' obligatoire pour un plan {stype}")
                if not shot.get("query_fr"):
                    rep.warn(swhere, "'query_fr' vide")
            if not shot.get("description"):
                rep.warn(swhere, "'description' vide")
            ai = shot.get("ai_prompt")
            if not isinstance(ai, dict) or not (ai.get("image") or ai.get("motion")):
                rep.warn(swhere, "prompt IA absent (ai_prompt.image / ai_prompt.motion)")
            mr = shot.get("min_rush_s")
            if mr is None:
                rep.warn(swhere, "'min_rush_s' absent")
            elif not is_num(mr):
                rep.error(swhere, f"'min_rush_s' doit être un nombre (trouvé {mr!r})")
            elif st is not None and mr < (en - st) - TOL:
                rep.warn(swhere, f"'min_rush_s' ({mr}) plus court que le plan ({en - st:.2f}s)")
            ms = shot.get("must_show")
            if ms is not None and not isinstance(ms, list):
                rep.error(swhere, "'must_show' doit être une liste")
            fb = shot.get("fallback")
            if isinstance(fb, dict):
                if fb.get("type") not in SHOT_TYPES:
                    rep.error(swhere, f"fallback.type {fb.get('type')!r} hors des valeurs autorisées")
                elif fb.get("type") != "MOTION" and not fb.get("query_en"):
                    rep.warn(swhere, f"fallback {fb.get('type')} sans 'query_en'")
            elif fb is not None:
                rep.error(swhere, "'fallback' doit être un objet ou null")

            # ---- nom de fichier ----
            fname = shot.get("filename")
            expected_prefix = f"{sid}_{beat.get('section')}_{stype}_"
            valid_name = False
            if isinstance(fname, str) and fname:
                m = FILENAME_RE.match(fname)
                if not m:
                    rep.error(swhere, f"'filename' {fname!r} ne respecte pas {{id}}_{{section}}_{{type}}_{{slug}}.mp4")
                else:
                    if m.group("id") != sid or m.group("section") != beat.get("section") or m.group("type") != stype:
                        rep.error(swhere, f"'filename' {fname!r} devrait commencer par {expected_prefix!r}")
                    elif not SLUG_RE.match(m.group("slug")):
                        rep.error(swhere, f"slug {m.group('slug')!r} invalide (minuscules ascii, chiffres, tirets)")
                    else:
                        valid_name = True
            if not valid_name:
                if fix_slugs and sid and stype in SHOT_TYPES and beat.get("section") in SECTIONS:
                    new_name = expected_prefix + slugify(shot.get("description") or shot.get("overlay_text")) + ".mp4"
                    shot["filename"] = new_name
                    changed = True
                    rep.info(f"plan {sid} : filename régénéré -> {new_name}")
                    # on retire l'erreur associée pour ce plan
                    rep.errors = [(w, m_) for (w, m_) in rep.errors if not (w == swhere and "'filename'" in m_)]
                    rep.errors = [(w, m_) for (w, m_) in rep.errors if not (w == swhere and m_.startswith("slug "))]
                elif fname is None:
                    rep.error(swhere, "'filename' manquant (utiliser --fix-slugs pour le générer)")

            all_shots.append((shot, beat, swhere, st, en))

        if bs is not None and prev_shot_end is not None and abs(prev_shot_end - be) > TOL:
            rep.error(bwhere, f"les plans finissent à {fmt(prev_shot_end)} mais le beat finit à {fmt(be)}")

    # ---- couverture globale, unicité, alternances ----
    ordered = [s for s in all_shots if s[3] is not None]
    ordered.sort(key=lambda s: s[3])

    if ordered and duration is not None:
        first_start = ordered[0][3]
        if abs(first_start) > TOL:
            rep.error("couverture", f"le premier plan commence à {fmt(first_start)} au lieu de 0.000s")
        last_end = max(s[4] for s in ordered)
        if abs(last_end - duration) > TOL:
            rep.error("couverture", f"le dernier plan finit à {fmt(last_end)} mais l'audio dure {fmt(duration)}")
        for a, b in zip(ordered, ordered[1:]):
            if abs(b[3] - a[4]) > TOL and a[1] is not b[1]:
                # les trous à l'intérieur d'un beat sont déjà signalés, ici on couvre les frontières de beats
                if b[3] > a[4]:
                    rep.error("couverture", f"trou entre {a[0].get('id')} et {b[0].get('id')} "
                                            f"({a[4]:.3f}s à {b[3]:.3f}s)")
                else:
                    rep.error("couverture", f"chevauchement entre {a[0].get('id')} et {b[0].get('id')} "
                                            f"({a[4] - b[3]:.3f}s)")

    seen_ids = {}
    seen_files = {}
    for shot, beat, swhere, st, en in all_shots:
        sid = shot.get("id")
        if sid:
            if sid in seen_ids:
                rep.error(swhere, f"identifiant de plan {sid!r} en double")
            seen_ids[sid] = shot
        fname = shot.get("filename")
        if isinstance(fname, str) and fname:
            if fname in seen_files:
                rep.error(swhere, f"'filename' {fname!r} déjà utilisé par le plan {seen_files[fname]}")
            seen_files[fname] = sid

    # durées selon le profil
    for shot, beat, swhere, st, en in ordered:
        sec = beat.get("section")
        lo, hi, target = shot_bounds(profile, sec)
        d = en - st
        if d < lo - TOL:
            rep.error(swhere, f"durée {d:.2f}s < minimum {lo}s pour la section {sec} (profil {profile_name})")
        elif d > hi + TOL:
            rep.error(swhere, f"durée {d:.2f}s > maximum {hi}s pour la section {sec} (profil {profile_name})")

    # alternance de valeurs et de caméras
    for a, b in zip(ordered, ordered[1:]):
        sa, sb = a[0], b[0]
        if sa.get("value") and sa.get("value") == sb.get("value"):
            rep.error(b[2], f"même valeur de plan ({sb['value']}) que le plan précédent {sa.get('id')}")
        if sa.get("camera") and sa.get("camera") == sb.get("camera"):
            rep.error(b[2], f"même caméra ({sb['camera']}) que le plan précédent {sa.get('id')}")

    # relance visuelle : aucune fenêtre de relance_max_s sans changement de plan
    relance = profile.get("relance_max_s")
    if is_num(relance):
        for shot, beat, swhere, st, en in ordered:
            if en - st > relance + TOL:
                rep.error(swhere, f"plan de {en - st:.2f}s sans coupe, dépasse la relance max de {relance}s")

    # part produit dans le corps
    share_min = profile.get("product_share_min")
    if is_num(share_min) and ordered:
        body = [s for s in ordered if s[1].get("section") not in NON_BODY_SECTIONS]
        body_total = sum(s[4] - s[3] for s in body)
        prod_total = sum(s[4] - s[3] for s in body if s[0].get("type") in PRODUCT_TYPES)
        if body_total > 0:
            share = prod_total / body_total
            rep.info(f"part PRODUIT+UGC dans le corps (hors {', '.join(sorted(NON_BODY_SECTIONS))}) : "
                     f"{share:.0%} (minimum {share_min:.0%})")
            if share < share_min - 1e-9:
                rep.error("part produit", f"{share:.0%} de plans PRODUIT+UGC dans le corps, minimum {share_min:.0%}")

    # réutilisation : deux plans identiques (même filename) trop proches
    # (le filename est unique, on regarde donc les requêtes identiques)
    reuse_gap = profile.get("reuse_min_gap_s")
    if is_num(reuse_gap):
        last_by_query = {}
        for shot, beat, swhere, st, en in ordered:
            q = (shot.get("query_en") or "").strip().lower()
            if not q:
                continue
            if q in last_by_query and st - last_by_query[q] < reuse_gap:
                rep.warn(swhere, f"même 'query_en' qu'un plan à moins de {reuse_gap}s (réutilisation visible)")
            last_by_query[q] = en

    # ---- plan de tournage ----
    plan = brief.get("shooting_plan")
    if plan is not None:
        if not isinstance(plan, list):
            rep.error("shooting_plan", "doit être une liste")
        else:
            planned = set()
            for i, loc in enumerate(plan):
                where = f"shooting_plan[{i}]"
                if not isinstance(loc, dict) or not loc.get("location") or not isinstance(loc.get("shots"), list):
                    rep.error(where, "attendu {'location': str, 'shots': [ids]}")
                    continue
                for ref in loc["shots"]:
                    if ref not in seen_ids:
                        rep.error(where, f"plan {ref!r} inconnu")
                    elif ref in planned:
                        rep.warn(where, f"plan {ref!r} présent dans plusieurs lieux")
                    planned.add(ref)
            for sid, shot in seen_ids.items():
                if shot.get("type") in PRODUCT_TYPES and sid not in planned:
                    rep.warn("shooting_plan", f"plan {sid} ({shot.get('type')}) absent du plan de tournage")
    else:
        rep.warn("shooting_plan", "absent, build_brief.py regroupera les plans par mots-clés")

    # ---- résumé ----
    if ordered:
        counts = {}
        for shot, *_ in ordered:
            counts[shot.get("type")] = counts.get(shot.get("type"), 0) + 1
        dist = ", ".join(f"{k} {v}" for k, v in sorted(counts.items(), key=lambda kv: -kv[1]))
        rep.info(f"{len(ordered)} plans, {len(beats)} beats, {len(sections)} sections, "
                 f"durée {duration if duration is not None else '?'}s, profil {profile_name}")
        rep.info(f"répartition par type : {dist}")
        avg = sum(s[4] - s[3] for s in ordered) / len(ordered)
        rep.info(f"durée moyenne d'un plan : {avg:.2f}s")

    return changed


def default_profiles_path():
    """assets/profiles.json relatif au dossier du skill (scripts/../assets)."""
    return Path(__file__).resolve().parent.parent / "assets" / "profiles.json"


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="validate_brief.py",
        description="Vérifie un brief.json CRÉATION FULL B-ROLL ARTISTE : couverture audio, durées par section selon le profil, "
                    "noms de fichiers, alternance des valeurs et des caméras, mots pivots, champs fermés, "
                    "part de plans produit, relance visuelle.",
        epilog="Code de sortie 1 si au moins une erreur bloquante (2 si le fichier est illisible).",
    )
    parser.add_argument("brief", help="chemin du brief.json à vérifier")
    parser.add_argument("--profiles", default=None,
                        help="chemin de profiles.json (défaut : assets/profiles.json à côté du dossier scripts)")
    parser.add_argument("--fix-slugs", action="store_true",
                        help="régénère les 'filename' absents ou invalides à partir de la description et réécrit le brief")
    parser.add_argument("--strict", action="store_true",
                        help="traite les avertissements comme des erreurs (code de sortie 1)")
    parser.add_argument("--quiet", action="store_true", help="n'affiche que le résultat final")
    args = parser.parse_args(argv)

    brief_path = Path(args.brief)
    profiles_path = Path(args.profiles) if args.profiles else default_profiles_path()

    try:
        brief = json.loads(brief_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"[ERREUR] impossible de lire {brief_path} : {exc}", file=sys.stderr)
        return 2
    try:
        profiles = json.loads(profiles_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"[ERREUR] impossible de lire les profils {profiles_path} : {exc}", file=sys.stderr)
        return 2

    rep = Report()
    changed = validate(brief, profiles, rep, fix_slugs=args.fix_slugs)

    if changed:
        try:
            brief_path.write_text(json.dumps(brief, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            rep.info(f"brief réécrit avec les nouveaux noms de fichiers : {brief_path}")
        except OSError as exc:
            rep.error("fichier", f"impossible de réécrire le brief : {exc}")

    if args.quiet:
        status = "ECHEC" if (rep.failed or (args.strict and rep.warnings)) else "OK"
        print(f"{status} : {len(rep.errors)} erreur(s), {len(rep.warnings)} avertissement(s)")
    else:
        rep.print(strict=args.strict)

    if rep.failed or (args.strict and rep.warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
