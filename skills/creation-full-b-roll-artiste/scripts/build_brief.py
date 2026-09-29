#!/usr/bin/env python3
"""
build_brief.py : génère la shot list interactive (brief.html) à partir d'un brief.json
CRÉATION FULL B-ROLL ARTISTE. Une seule page HTML autonome (CSS et JS inline, aucune dépendance
réseau), lisible hors ligne en double-cliquant sur le fichier.

Usage :
    python3 build_brief.py brief.json --out brief.html [--audio voix.mp3]
                          [--features work/features.json] [--words work/words.json]
                          [--profiles assets/profiles.json]

Sans --audio, le script cherche le fichier indiqué dans brief.audio.file à côté du brief.
Sans --features / --words, il cherche work/features.json et work/words.json à côté du brief.
L'audio de moins de 20 Mo est encodé en base64 dans la page ; sinon la page pointe vers
le fichier par un chemin relatif au HTML.

Bibliothèque standard uniquement (Python 3.11).
"""

import argparse
import base64
import datetime as dt
import html
import json
import os
import sys
from pathlib import Path

AUDIO_INLINE_MAX = 20 * 1024 * 1024  # 20 Mo
MIME_BY_EXT = {
    ".mp3": "audio/mpeg", ".wav": "audio/wav", ".m4a": "audio/mp4", ".aac": "audio/aac",
    ".ogg": "audio/ogg", ".oga": "audio/ogg", ".opus": "audio/ogg", ".flac": "audio/flac",
    ".webm": "audio/webm",
}


def json_for_html(obj):
    """Sérialise en JSON sûr pour un <script type=application/json> (pas de fermeture prématurée)."""
    s = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
    return s.replace("</", "<\\/").replace("<!--", "<\\!--")


def load_json(path, label):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print(f"[ERREUR] impossible de lire {label} {path} : {exc}", file=sys.stderr)
        return None


def resolve_audio(args, brief, brief_dir, out_dir):
    """Retourne (src, info) : src est une data URI ou un chemin relatif au HTML."""
    candidate = None
    if args.audio:
        candidate = Path(args.audio)
    else:
        name = (brief.get("audio") or {}).get("file")
        if name:
            candidate = brief_dir / name
    if candidate is None:
        return None, "aucun audio indiqué"
    if not candidate.exists():
        rel = os.path.relpath(candidate, out_dir).replace(os.sep, "/")
        return rel, f"audio introuvable ({candidate}), chemin relatif conservé : {rel}"
    size = candidate.stat().st_size
    mime = MIME_BY_EXT.get(candidate.suffix.lower(), "audio/mpeg")
    if size <= AUDIO_INLINE_MAX:
        data = base64.b64encode(candidate.read_bytes()).decode("ascii")
        return f"data:{mime};base64,{data}", f"audio encodé en base64 ({size / 1024 / 1024:.1f} Mo, {mime})"
    rel = os.path.relpath(candidate, out_dir).replace(os.sep, "/")
    return rel, f"audio trop lourd pour l'inclusion ({size / 1024 / 1024:.1f} Mo), chemin relatif : {rel}"


def default_profiles_path():
    return Path(__file__).resolve().parent.parent / "assets" / "profiles.json"


# ---------------------------------------------------------------------------
# Gabarit HTML. Les marqueurs __XXX__ sont remplacés par le script.
# ---------------------------------------------------------------------------
TEMPLATE = r'''<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITLE__</title>
<style>
:root{
  --bg:#f4f6f9;--panel:#ffffff;--ink:#1c2330;--muted:#5b6474;--line:#dfe4ec;--soft:#eef1f6;
  --accent:#1f5eff;--accent-ink:#ffffff;--ok:#16a34a;--warn:#d97706;--bad:#dc2626;
  --t-STOCK:#3b82f6;--t-UGC:#f59e0b;--t-PRODUIT:#10b981;--t-3DSCI:#8b5cf6;--t-MOTION:#ec4899;
  --t-SCREEN:#06b6d4;--t-SOCIAL:#f43f5e;--t-IAGEN:#64748b;
  --s-HOOK:#ef4444;--s-PROB:#f97316;--s-MECA:#8b5cf6;--s-PREUVE:#0ea5e9;--s-PROD:#10b981;
  --s-BENEF:#84cc16;--s-OBJ:#eab308;--s-CTA:#ec4899;--s-CHUTE:#6366f1;
  --radius:12px;--shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.08);
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1200px;margin:0 auto;padding:20px 16px 80px}
h1,h2,h3{margin:0 0 .4em;line-height:1.2}
h1{font-size:26px;letter-spacing:-.01em}
h2{font-size:18px}
h3{font-size:15px}
p{margin:.3em 0}
code,pre,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace}
code{font-size:.92em}
pre{background:var(--soft);border:1px solid var(--line);border-radius:8px;padding:12px;overflow:auto;font-size:13px;line-height:1.45;margin:0}
button,.btn{font:inherit;font-size:13px;border:1px solid var(--line);background:var(--panel);color:var(--ink);border-radius:8px;padding:6px 10px;cursor:pointer;line-height:1.2}
button:hover,.btn:hover{border-color:#b9c3d3;background:#fafbfd}
button.primary{background:var(--accent);color:var(--accent-ink);border-color:var(--accent)}
button.primary:hover{background:#1750e0}
button.small{padding:3px 8px;font-size:12px}
button[disabled]{opacity:.5;cursor:default}
button.copied{border-color:var(--ok);color:var(--ok)}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:16px}
.row{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.muted{color:var(--muted)}
.pill{display:inline-flex;align-items:center;gap:6px;border-radius:999px;padding:2px 10px;font-size:12px;font-weight:600;border:1px solid var(--line);background:var(--soft);white-space:nowrap}
.pill .dot{width:9px;height:9px;border-radius:50%;display:inline-block}
.pill.type{color:#fff;border-color:transparent}
.pill.sec{color:#fff;border-color:transparent}
.badge{display:inline-block;border-radius:6px;padding:2px 8px;font-size:12px;background:var(--soft);border:1px solid var(--line);white-space:nowrap}
.badge b{font-weight:600}
.hero{display:grid;gap:16px}
.hero .meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:8px}
.grid{display:grid;gap:16px;grid-template-columns:1fr}
@media (min-width:760px){.grid{grid-template-columns:1fr 1fr}}
.kv{display:grid;grid-template-columns:auto 1fr;gap:4px 12px;font-size:14px}
.kv dt{color:var(--muted);white-space:nowrap}
.kv dd{margin:0;word-break:break-word}
.stat{display:flex;flex-direction:column;gap:2px}
.stat .n{font-size:22px;font-weight:700;line-height:1.1}
.stat .l{font-size:12px;color:var(--muted)}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:12px}
table{border-collapse:collapse;width:100%;font-size:13px}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:600;color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.03em}
.diag ul{margin:6px 0 0;padding-left:18px}
.diag .ok{color:var(--ok);font-weight:600}
.diag .ko{color:var(--bad);font-weight:600}
/* lecteur */
.player .controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin-bottom:10px}
.player .time{font-variant-numeric:tabular-nums;font-size:14px;min-width:120px}
.player .loopinfo{font-size:13px;color:var(--muted)}
.player .loopinfo b{color:var(--ink)}
.wave-wrap{position:relative;width:100%;height:130px;border:1px solid var(--line);border-radius:8px;overflow:hidden;background:#fbfcfe}
.wave-wrap canvas{display:block;width:100%;height:100%;cursor:pointer}
.player .note{font-size:12px;color:var(--muted);margin-top:6px}
/* timeline */
.tl-scroll{overflow-x:auto;padding-bottom:4px}
.tl{min-width:760px}
.tl .band{display:flex;height:26px;border-radius:6px;overflow:hidden;margin-bottom:4px}
.tl .band .seg{display:flex;align-items:center;justify-content:center;color:#fff;font-size:11px;font-weight:700;overflow:hidden;white-space:nowrap;border-right:1px solid rgba(255,255,255,.6)}
.tl .band .seg:last-child{border-right:0}
.tl .shots{display:flex;height:36px;border-radius:6px;overflow:hidden}
.tl .shots .shot{display:flex;align-items:center;justify-content:center;color:#fff;font-size:12px;font-weight:700;cursor:pointer;border-right:1px solid rgba(255,255,255,.7);overflow:hidden;white-space:nowrap;position:relative;transition:filter .15s}
.tl .shots .shot:hover{filter:brightness(1.12)}
.tl .shots .shot.playing{outline:3px solid var(--ink);outline-offset:-3px}
.tl .shots .shot.found::after{content:"";position:absolute;right:3px;top:3px;width:7px;height:7px;border-radius:50%;background:#fff}
.tl .shots .shot:last-child{border-right:0}
.tl .ticks{display:flex;justify-content:space-between;font-size:11px;color:var(--muted);margin-top:4px;font-variant-numeric:tabular-nums}
.legend{display:flex;flex-wrap:wrap;gap:6px 12px;font-size:12px;margin-top:10px}
.legend span{display:inline-flex;align-items:center;gap:5px}
.legend i{width:10px;height:10px;border-radius:3px;display:inline-block}
/* énergie */
.energy svg{max-width:100%;height:auto;display:block}
/* onglets */
.tabs{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:20px 0 12px}
.tabs .tab{border-radius:999px;padding:7px 14px;font-weight:600}
.tabs .tab.active{background:var(--ink);color:#fff;border-color:var(--ink)}
.tabs .spacer{flex:1}
.view{display:none}
.view.active{display:block}
/* filtres */
.filters{display:grid;gap:10px}
.filters .chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{border-radius:999px;padding:4px 11px;font-size:12px;font-weight:600;border:1px solid var(--line);background:var(--panel);cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.chip.on{color:#fff;border-color:transparent}
.chip .dot{width:8px;height:8px;border-radius:50%;display:inline-block;background:currentColor}
.chip.on .dot{background:#fff}
.filters input[type=search]{font:inherit;padding:7px 10px;border:1px solid var(--line);border-radius:8px;min-width:200px;flex:1}
.filters label{font-size:13px;display:inline-flex;align-items:center;gap:6px}
.counter{font-size:14px;margin:12px 0;color:var(--muted)}
.counter b{color:var(--ink)}
/* cartes */
.cards{display:grid;gap:14px;grid-template-columns:repeat(auto-fill,minmax(min(100%,460px),1fr))}
.card{background:var(--panel);border:1px solid var(--line);border-radius:var(--radius);box-shadow:var(--shadow);padding:14px;border-top:5px solid var(--card-color,#999);display:flex;flex-direction:column;gap:10px;min-width:0}
.card.found{background:#f2fbf5;border-color:#bfe8cc}
.card.hidden{display:none}
.card .head{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.card .id{font-size:20px;font-weight:800;letter-spacing:-.02em}
.card .tc{font-variant-numeric:tabular-nums;font-size:13px;color:var(--muted)}
.card .head .right{margin-left:auto;display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.card .found-label{display:inline-flex;align-items:center;gap:5px;font-size:13px;border:1px solid var(--line);border-radius:8px;padding:4px 8px;cursor:pointer;background:var(--panel)}
.card .found-label input{margin:0}
.card .file{display:flex;gap:6px;align-items:center;flex-wrap:wrap}
.card .file code{background:var(--soft);padding:3px 7px;border-radius:6px;word-break:break-all;font-size:12.5px}
.card .voice{margin:0;padding:8px 12px;border-left:3px solid var(--line);background:#fafbfd;font-style:italic;font-size:14px}
.card .voice mark{background:#fde68a;font-style:normal;font-weight:700;padding:0 2px;border-radius:3px}
.card .voice .w{opacity:.55}
.card .voice .w.in{opacity:1}
.card .desc{font-size:14.5px}
.card .badges{display:flex;flex-wrap:wrap;gap:5px}
.card .q{display:grid;grid-template-columns:auto 1fr auto;gap:6px;align-items:start;font-size:13px}
.card .q .lab{font-weight:700;color:var(--muted);font-size:11px;padding-top:4px;min-width:22px}
.card .q .txt{background:var(--soft);border-radius:6px;padding:4px 8px;word-break:break-word}
.card .links{display:flex;flex-wrap:wrap;gap:5px}
.card .links a{font-size:12px;text-decoration:none;border:1px solid var(--line);border-radius:6px;padding:3px 8px;color:var(--accent);background:var(--panel)}
.card .links a:hover{border-color:var(--accent)}
.card .ai-box{border:1px solid var(--line);border-radius:8px;padding:0}
.card .ai-box .toggle{display:block;width:100%;text-align:left;border:0;background:none;cursor:pointer;padding:6px 10px;font-size:13px;font-weight:600;color:var(--muted)}
.card .ai-box .toggle::before{content:"+ ";font-weight:700}
.card .ai-box.open .toggle::before{content:"\2212  "}
.card .ai-box .ai{display:none;padding:4px 10px 10px;gap:8px}
.card .ai-box.open .ai{display:grid}
.card .specs{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;font-size:13px;margin:0}
.card .specs dt{color:var(--muted);white-space:nowrap}
.card .specs dd{margin:0;word-break:break-word}
.card textarea{font:inherit;font-size:13px;width:100%;min-height:52px;border:1px solid var(--line);border-radius:8px;padding:6px 8px;resize:vertical}
.card .listen.active{background:var(--ink);color:#fff;border-color:var(--ink)}
.card .fb{font-size:13px}
.empty{padding:30px;text-align:center;color:var(--muted)}
/* plan de tournage */
.loc{margin-bottom:16px}
.loc h3{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline}
.loc h3 .muted{font-weight:400;font-size:13px}
.loc table td:first-child{width:28px}
.loc .vals{display:flex;flex-wrap:wrap;gap:4px}
.loc .vals span{border-radius:5px;padding:1px 7px;font-size:12px;background:var(--soft);border:1px solid var(--line)}
.loc .vals span.main{background:var(--ink);color:#fff;border-color:var(--ink);font-weight:700}
.loc tr.found td{color:var(--muted);text-decoration:line-through}
.loc tr.found td:first-child,.loc tr.found td.nostrike{text-decoration:none}
/* nomenclature */
.nomen .rule{font-size:16px;background:var(--soft);padding:10px 12px;border-radius:8px;display:inline-block}
.nomen ol{padding-left:20px}
footer{margin-top:30px;font-size:12px;color:var(--muted)}
@media (max-width:640px){
  .wrap{padding:14px 12px 60px}
  h1{font-size:22px}
  .card .q{grid-template-columns:auto 1fr}
  .card .q button{grid-column:2;justify-self:start}
  .tabs .tab{padding:6px 10px;font-size:13px}
  th,td{padding:5px 6px}
  .loc table thead{display:none}
  .loc table tr{display:flex;flex-wrap:wrap;gap:4px 10px;padding:8px 0;border-bottom:1px solid var(--line);align-items:center}
  .loc table td{display:block;border:0;padding:0}
  .loc table td:first-child{width:auto}
  .loc table td.plan{flex:1;min-width:160px}
  .loc table td.vals-cell,.loc table td.desc{flex-basis:100%}
  .loc table td[data-label]::before{content:attr(data-label) " : ";color:var(--muted)}
}
@media print{
  body{background:#fff;font-size:12px}
  .wrap{max-width:none;padding:0}
  .no-print,.player,.filters,.tabs,.tl-scroll,.energy,footer,.card textarea,.card .listen,button.copy{display:none !important}
  .view{display:none}
  .view.active{display:block}
  .panel,.card{box-shadow:none;border:1px solid #bbb;break-inside:avoid;page-break-inside:avoid}
  .cards{display:block}
  .card{margin:0 0 10px;display:block}
  .card.hidden{display:none}
  .card > *{margin-bottom:6px}
  .card .ai-box{border:0}
  .card .ai-box .toggle{display:none}
  .card .ai-box .ai{display:grid;padding:0}
  .card .q{grid-template-columns:auto 1fr}
  a{color:inherit;text-decoration:none}
  .card .links a::after{content:""}
  .loc{break-inside:avoid}
  .hero .grid{display:block}
  .hero .panel{margin-bottom:8px}
}
</style>
</head>
<body>
<div class="wrap">

<header class="hero">
  <div>
    <h1 id="h-title"></h1>
    <div class="muted" id="h-sub"></div>
    <div class="meta" id="h-meta"></div>
  </div>
  <div class="grid">
    <section class="panel">
      <h2>Répartition des plans</h2>
      <div class="stats" id="h-stats"></div>
      <div class="row" id="h-types" style="margin-top:12px"></div>
    </section>
    <section class="panel">
      <h2>Cadence par section</h2>
      <table id="h-cadence"><thead><tr><th>Section</th><th>Durée</th><th>Plans</th><th>Moy.</th><th>Cible</th></tr></thead><tbody></tbody></table>
    </section>
    <section class="panel diag">
      <h2>Diagnostic du script</h2>
      <div id="h-diag"></div>
    </section>
    <section class="panel">
      <h2>Look book</h2>
      <dl class="kv" id="h-look"></dl>
    </section>
  </div>
</header>

<section class="panel player" style="margin-top:16px">
  <h2>Voix off</h2>
  <div class="controls">
    <button class="primary" id="btn-play">Lecture</button>
    <button id="btn-stop">Stop</button>
    <span class="time" id="p-time">00:00.0 / 00:00.0</span>
    <span class="loopinfo" id="p-loop">Cliquez sur un plan de la timeline ou sur "écouter" dans une carte pour boucler son segment.</span>
  </div>
  <div class="wave-wrap"><canvas id="wave"></canvas></div>
  <div class="note" id="p-note"></div>
  <audio id="audio" preload="auto"></audio>
</section>

<section class="panel" style="margin-top:16px">
  <h2>Timeline</h2>
  <div class="tl-scroll"><div class="tl" id="timeline"></div></div>
  <div class="legend" id="legend"></div>
</section>

<section class="panel energy" style="margin-top:16px">
  <h2>Énergie des beats</h2>
  <div id="energy"></div>
</section>

<nav class="tabs no-print">
  <button class="tab active" data-view="plans">Plans</button>
  <button class="tab" data-view="tournage">Plan de tournage</button>
  <button class="tab" data-view="nomenclature">Nomenclature</button>
  <span class="spacer"></span>
  <button id="btn-csv">Exporter CSV</button>
  <button id="btn-json">Exporter JSON</button>
  <button id="btn-print">Imprimer</button>
</nav>

<section class="view active" id="view-plans">
  <div class="panel filters no-print">
    <div class="row">
      <input type="search" id="f-search" placeholder="Rechercher (ID, description, requête, texte, fichier)">
      <label><input type="checkbox" id="f-missing"> à trouver seulement</label>
      <button class="small" id="f-reset">Réinitialiser</button>
    </div>
    <div class="chips" id="f-types"></div>
    <div class="chips" id="f-sections"></div>
  </div>
  <div class="counter" id="counter"></div>
  <div class="cards" id="cards"></div>
</section>

<section class="view" id="view-tournage">
  <div class="panel">
    <h2>Plan de tournage</h2>
    <p class="muted">Plans UGC et PRODUIT regroupés par lieu. Pour chaque prise, la valeur demandée est en noir ; les deux autres valeurs de la séquence (large, moyen, détail) sont à couvrir en bonus pour laisser du choix au montage. Durée mini = durée de rush à enregistrer, marges comprises.</p>
    <div id="tournage"></div>
  </div>
</section>

<section class="view nomen" id="view-nomenclature">
  <div class="panel">
    <h2>Nomenclature des rushes</h2>
    <p>Règle de nommage :</p>
    <p><code class="rule">{id}_{section}_{type}_{slug}.mp4</code></p>
    <ol>
      <li><b>id</b> : identifiant du plan (numéro du beat + lettre), exemple <code>03a</code>.</li>
      <li><b>section</b> : HOOK, PROB, MECA, PREUVE, PROD, BENEF, OBJ, CTA ou CHUTE.</li>
      <li><b>type</b> : STOCK, UGC, PRODUIT, 3DSCI, MOTION, SCREEN, SOCIAL ou IAGEN.</li>
      <li><b>slug</b> : quelques mots en minuscules sans accent, séparés par des tirets simples.</li>
    </ol>
    <p>Le nom exact est recommandé. Un fichier dont le nom commence par l'identifiant suivi d'un underscore (par exemple <code>03a_main.mp4</code>) est aussi reconnu par correspondance de préfixe. Formats acceptés : mp4 ou mov, de préférence vertical 1080x1920, durée au moins égale à la durée mini indiquée sur la carte.</p>
    <h3>Structure attendue du dossier</h3>
    <pre id="tree"></pre>
    <h3 style="margin-top:14px">Liste complète des fichiers <button class="small" id="btn-copy-names">copier la liste</button></h3>
    <pre id="names"></pre>
  </div>
</section>

<footer>Généré par CRÉATION FULL B-ROLL ARTISTE (build_brief.py) le <span id="gen-date"></span>. Les cases "trouvé" et les notes sont enregistrées dans ce navigateur uniquement (localStorage).</footer>
</div>

<script type="application/json" id="brief-data">__BRIEF_JSON__</script>
<script type="application/json" id="features-data">__FEATURES_JSON__</script>
<script type="application/json" id="words-data">__WORDS_JSON__</script>
<script type="application/json" id="profile-data">__PROFILE_JSON__</script>
<script type="application/json" id="audio-src">__AUDIO_JSON__</script>
<script>
(function(){
"use strict";
/* ---------- données ---------- */
function readJson(id){ try{ return JSON.parse(document.getElementById(id).textContent); }catch(e){ return null; } }
const BRIEF = readJson("brief-data") || {};
const FEATURES = readJson("features-data");
const WORDS = readJson("words-data");
const PROFILE = readJson("profile-data");
const AUDIO_SRC = readJson("audio-src");
const GEN_DATE = "__GEN_DATE__";

const TYPES = ["STOCK","UGC","PRODUIT","3DSCI","MOTION","SCREEN","SOCIAL","IAGEN"];
const SECTION_ORDER = ["HOOK","PROB","MECA","PREUVE","PROD","BENEF","OBJ","CTA","CHUTE"];
const SECTION_LABEL = {HOOK:"Hook",PROB:"Problème",MECA:"Mécanisme",PREUVE:"Preuve",PROD:"Produit",BENEF:"Bénéfice",OBJ:"Objection",CTA:"Appel à l'action",CHUTE:"Chute"};
const VALUE_LABEL = {large:"large",moyen:"moyen",detail:"détail",macro:"macro",topdown:"vue du dessus",pov:"POV"};
const CAMERA_LABEL = {static:"fixe",push:"avancée",pull:"recul",pan:"panoramique",handheld:"à l'épaule",orbit:"orbite",tilt:"bascule"};
const ORIENT_LABEL = {vertical:"vertical",horizontal:"horizontal",any:"toute orientation"};
const SEQ3 = ["large","moyen","detail"];
const SEARCH_SITES = [
  ["Pexels", (q,o)=>"https://www.pexels.com/search/videos/"+encodeURIComponent(q)+"/"+(o==="horizontal"?"?orientation=landscape":(o==="any"?"":"?orientation=portrait"))],
  ["Pixabay", q=>"https://pixabay.com/videos/search/"+encodeURIComponent(q)+"/"],
  ["Mixkit", q=>"https://mixkit.co/free-stock-video/"+encodeURIComponent(q.replace(/\s+/g,"-"))+"/"],
  ["Coverr", q=>"https://coverr.co/s?q="+encodeURIComponent(q)],
  ["Storyblocks", q=>"https://www.storyblocks.com/video/search/"+encodeURIComponent(q)],
  ["Artgrid", q=>"https://artgrid.io/clips?search="+encodeURIComponent(q)],
  ["Envato Elements", q=>"https://elements.envato.com/stock-video/"+encodeURIComponent(q.replace(/\s+/g,"-"))]
];

const project = BRIEF.project || {};
const duration = (BRIEF.audio && BRIEF.audio.duration_s) || 0;
const sections = (BRIEF.sections || []).slice().sort((a,b)=>a.start-b.start);
const beats = (BRIEF.beats || []).slice().sort((a,b)=>a.start-b.start);
const shots = [];
beats.forEach(b => (b.shots||[]).forEach(s => shots.push(Object.assign({}, s, {_beat:b, _section:b.section, _dur:(s.end-s.start)}))));
shots.sort((a,b)=>a.start-b.start);
const shotById = {}; shots.forEach(s => shotById[s.id] = s);

function typeColor(t){ return TYPES.includes(t) ? "var(--t-"+t+")" : "#999"; }
function secColor(s){ return SECTION_ORDER.includes(s) ? "var(--s-"+s+")" : "#999"; }
function esc(s){ return String(s==null?"":s).replace(/[&<>"']/g, c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c])); }
function tc(t){ t = Math.max(0, +t||0); const m = Math.floor(t/60); const s = (t - m*60).toFixed(1); return String(m).padStart(2,"0")+":"+ (s.length<4?"0"+s:s); }
function fmtS(t){ return (Math.round(t*10)/10).toFixed(1).replace(".",",")+" s"; }
function el(tag, cls, html){ const e=document.createElement(tag); if(cls) e.className=cls; if(html!=null) e.innerHTML=html; return e; }

/* ---------- persistance ---------- */
const STORE_KEY = "broll-director:" + (project.name || "projet");
let state = {shots:{}};
function loadState(){ try{ const raw = localStorage.getItem(STORE_KEY); if(raw){ const o = JSON.parse(raw); if(o && o.shots) state = o; } }catch(e){} }
function saveState(){ try{ localStorage.setItem(STORE_KEY, JSON.stringify(state)); }catch(e){} }
function shotState(id){ if(!state.shots[id]) state.shots[id] = {found:false, notes:""}; return state.shots[id]; }
loadState();

/* ---------- presse-papiers ---------- */
function copyText(text, btn){
  const done = ()=>{ if(btn){ const old = btn.textContent; btn.textContent = "copié"; btn.classList.add("copied"); setTimeout(()=>{ btn.textContent = old; btn.classList.remove("copied"); }, 1200); } };
  const fallback = ()=>{ try{ const ta = document.createElement("textarea"); ta.value = text; ta.style.position="fixed"; ta.style.opacity="0"; document.body.appendChild(ta); ta.select(); document.execCommand("copy"); document.body.removeChild(ta); done(); }catch(e){} };
  if(navigator.clipboard && navigator.clipboard.writeText){ navigator.clipboard.writeText(text).then(done, fallback); } else fallback();
}
function copyBtn(text, label, cls){ const b = el("button", "small copy"+(cls?" "+cls:""), esc(label||"copier")); b.type="button"; b.addEventListener("click", ()=>copyText(text, b)); return b; }

/* ---------- en-tête ---------- */
(function header(){
  document.getElementById("h-title").textContent = project.name || "Shot list";
  document.getElementById("h-sub").textContent = (project.brand ? "Marque " + project.brand + ". " : "") + "Shot list B-roll, " + shots.length + " plans sur " + fmtS(duration) + ".";
  const meta = document.getElementById("h-meta");
  const badges = [["Profil", project.profile], ["Plateforme", project.platform], ["Ratio", project.ratio], ["Format", project.width && project.height ? project.width+"x"+project.height+" à "+(project.fps||"?")+" i/s" : null], ["Langue", project.language], ["Audio", BRIEF.audio && BRIEF.audio.file]];
  badges.forEach(([k,v])=>{ if(v) meta.appendChild(el("span","badge", esc(k)+" : <b>"+esc(v)+"</b>")); });

  const stats = document.getElementById("h-stats");
  const avg = shots.length ? shots.reduce((a,s)=>a+s._dur,0)/shots.length : 0;
  const body = shots.filter(s=>s._section!=="HOOK"); const bodyDur = body.reduce((a,s)=>a+s._dur,0);
  const prodDur = body.filter(s=>s.type==="UGC"||s.type==="PRODUIT").reduce((a,s)=>a+s._dur,0);
  [[fmtS(duration),"durée totale"],[shots.length,"plans"],[beats.length,"beats"],[fmtS(avg),"plan moyen"],[bodyDur?Math.round(100*prodDur/bodyDur)+" %":"n/a","UGC + PRODUIT (corps)"]].forEach(([n,l])=>{
    const d = el("div","stat"); d.appendChild(el("span","n",esc(n))); d.appendChild(el("span","l",esc(l))); stats.appendChild(d);
  });
  const types = document.getElementById("h-types");
  TYPES.forEach(t=>{ const n = shots.filter(s=>s.type===t).length; const p = el("span","pill", "<span class='dot' style='background:"+typeColor(t)+"'></span>"+t+" <span class='muted'>"+n+"</span>"); if(!n) p.style.opacity=".45"; types.appendChild(p); });

  const tb = document.querySelector("#h-cadence tbody");
  sections.forEach(sec=>{
    const ss = shots.filter(s=>s._section===sec.id); const d = sec.end-sec.start; const m = ss.length ? ss.reduce((a,s)=>a+s._dur,0)/ss.length : 0;
    const spec = PROFILE && PROFILE.shot && (PROFILE.shot[sec.id] || PROFILE.shot.default);
    const target = spec ? fmtS(spec.target)+" ("+String(spec.min).replace(".",",")+" à "+String(spec.max).replace(".",",")+")" : "";
    const tr = el("tr","", "<td><span class='pill sec' style='background:"+secColor(sec.id)+"'>"+esc(sec.id)+"</span></td><td>"+fmtS(d)+"</td><td>"+ss.length+"</td><td>"+(ss.length?fmtS(m):"")+"</td><td class='muted'>"+esc(target)+"</td>");
    tb.appendChild(tr);
  });

  const diag = BRIEF.script_diagnostic || {}; const dg = document.getElementById("h-diag");
  const yn = v => v===true ? "<span class='ok'>oui</span>" : (v===false ? "<span class='ko'>non</span>" : "<span class='muted'>?</span>");
  const dl = el("dl","kv");
  dl.innerHTML = "<dt>Hook efficace</dt><dd>"+yn(diag.hook_ok)+"</dd>"
    + "<dt>Promesse validée à</dt><dd>"+(diag.promise_validated_by_s!=null? esc(fmtS(diag.promise_validated_by_s)) : "<span class='muted'>?</span>")+"</dd>"
    + "<dt>Position du CTA</dt><dd>"+(diag.cta_position_pct!=null? esc(diag.cta_position_pct)+" % de la durée" : "<span class='muted'>?</span>")+"</dd>"
    + "<dt>Boucle fermée</dt><dd>"+yn(diag.loop_closed)+"</dd>";
  dg.appendChild(dl);
  if(diag.notes && diag.notes.length){ const ul = el("ul"); diag.notes.forEach(n=>ul.appendChild(el("li","",esc(n)))); dg.appendChild(ul); }

  const look = project.lookbook || {}; const lk = document.getElementById("h-look");
  [["Lumière","light"],["Palette","palette"],["Décor","setting"],["Personnes","people"],["Suffixe de style (EN)","style_suffix_en"]].forEach(([l,k])=>{
    if(!look[k]) return; const dt = el("dt","",esc(l)); const dd = el("dd","",esc(look[k])+" ");
    if(k==="style_suffix_en") dd.appendChild(copyBtn(look[k],"copier"));
    lk.appendChild(dt); lk.appendChild(dd);
  });
  if(!lk.children.length) lk.innerHTML = "<dd class='muted'>Aucun look book dans le brief.</dd>";
  document.getElementById("gen-date").textContent = GEN_DATE;
})();

/* ---------- lecteur audio et forme d'onde ---------- */
const audio = document.getElementById("audio");
const canvas = document.getElementById("wave");
const ctx = canvas.getContext("2d");
let loop = null;          // {id,start,end}
let audioReady = false;
const pNote = document.getElementById("p-note");
if(AUDIO_SRC){ audio.src = AUDIO_SRC; pNote.textContent = AUDIO_SRC.startsWith("data:") ? "Audio intégré dans la page." : "Audio lu depuis le fichier : " + AUDIO_SRC; }
else { pNote.textContent = "Aucun fichier audio fourni : la timeline reste consultable, la lecture est désactivée."; document.getElementById("btn-play").disabled = true; }
audio.addEventListener("loadedmetadata", ()=>{ audioReady = true; updateTime(); });
audio.addEventListener("error", ()=>{ pNote.textContent = "Impossible de charger l'audio (" + (AUDIO_SRC && !AUDIO_SRC.startsWith("data:") ? AUDIO_SRC : "données intégrées") + "). Vérifiez le chemin ou régénérez la page avec --audio."; });
audio.addEventListener("play", updatePlayUi); audio.addEventListener("pause", updatePlayUi); audio.addEventListener("ended", ()=>{ if(loop){ audio.currentTime = loop.start; audio.play().catch(()=>{}); } });

function updateTime(){ document.getElementById("p-time").textContent = tc(audio.currentTime||0) + " / " + tc(duration || audio.duration || 0); }
function updatePlayUi(){
  document.getElementById("btn-play").textContent = audio.paused ? "Lecture" : "Pause";
  document.body.dataset.playing = audio.paused ? "0" : "1";
  const li = document.getElementById("p-loop");
  if(loop){ const s = shotById[loop.id]; li.innerHTML = "Boucle sur le plan <b>"+esc(loop.id)+"</b> ("+tc(loop.start)+" à "+tc(loop.end)+")" + (s ? ", " + esc(s.type) : "") + ". Cliquez sur Stop pour sortir de la boucle."; }
  else li.textContent = "Cliquez sur un plan de la timeline ou sur \"écouter\" dans une carte pour boucler son segment.";
  document.querySelectorAll(".listen").forEach(b=>{ const on = loop && loop.id===b.dataset.id && !audio.paused; b.classList.toggle("active", !!on); b.textContent = on ? "stop" : "écouter"; });
  document.querySelectorAll(".tl .shot").forEach(d=>d.classList.toggle("playing", !!(loop && loop.id===d.dataset.id && !audio.paused)));
  document.body.dataset.loop = loop ? loop.id : "";
}
function playShot(id){
  const s = shotById[id]; if(!s) return;
  if(loop && loop.id===id && !audio.paused){ stopLoop(); return; }
  loop = {id:id, start:s.start, end:s.end};
  try{ audio.currentTime = s.start; }catch(e){}
  const p = audio.play(); if(p && p.catch) p.catch(()=>{});
  updatePlayUi(); drawWave();
}
function stopLoop(){ loop = null; audio.pause(); updatePlayUi(); drawWave(); }
document.getElementById("btn-play").addEventListener("click", ()=>{ if(audio.paused){ const p = audio.play(); if(p&&p.catch) p.catch(()=>{}); } else audio.pause(); });
document.getElementById("btn-stop").addEventListener("click", ()=>{ stopLoop(); try{ audio.currentTime = loop ? loop.start : 0; }catch(e){} drawWave(); updateTime(); });

function tick(){
  if(!audio.paused){
    if(loop && (audio.currentTime >= loop.end - 0.03 || audio.currentTime < loop.start - 0.2)){ try{ audio.currentTime = loop.start; }catch(e){} }
    updateTime(); drawWave();
  }
  requestAnimationFrame(tick);
}
requestAnimationFrame(tick);

canvas.addEventListener("click", ev=>{
  if(!duration) return;
  const r = canvas.getBoundingClientRect(); const t = Math.max(0, Math.min(duration, (ev.clientX - r.left)/r.width*duration));
  const s = shots.find(x=>t>=x.start && t<x.end);
  if(s){ playShot(s.id); } else { loop=null; try{ audio.currentTime = t; }catch(e){} updatePlayUi(); }
  drawWave();
});

function drawWave(){
  const W = canvas.clientWidth || 600, H = canvas.clientHeight || 130, dpr = window.devicePixelRatio || 1;
  if(canvas.width !== Math.round(W*dpr) || canvas.height !== Math.round(H*dpr)){ canvas.width = Math.round(W*dpr); canvas.height = Math.round(H*dpr); }
  ctx.setTransform(dpr,0,0,dpr,0,0);
  ctx.clearRect(0,0,W,H);
  const x = t => duration ? t/duration*W : 0;
  const top = 18, bottom = H-30, mid = (top+bottom)/2, half = (bottom-top)/2;
  /* bandes de sections */
  ctx.font = "600 11px system-ui, sans-serif"; ctx.textBaseline = "top";
  sections.forEach(sec=>{ const col = getComputedStyle(document.documentElement).getPropertyValue("--s-"+sec.id).trim() || "#999"; ctx.fillStyle = col; ctx.globalAlpha = .10; ctx.fillRect(x(sec.start), 0, x(sec.end)-x(sec.start), H); ctx.globalAlpha = 1; const w = x(sec.end)-x(sec.start); if(w > ctx.measureText(sec.id).width + 8){ ctx.fillStyle = "#333"; ctx.fillText(sec.id, x(sec.start)+4, 3); } });
  /* pauses */
  if(FEATURES && FEATURES.pauses){ ctx.fillStyle = "rgba(0,0,0,.06)"; FEATURES.pauses.forEach(p=>ctx.fillRect(x(p.start), top, Math.max(1, x(p.end)-x(p.start)), bottom-top)); }
  /* enveloppe : un polygone symétrique, une valeur (max) par colonne de pixels */
  const rms = FEATURES && FEATURES.energy && FEATURES.energy.rms_db;
  if(rms && rms.length){
    const hop = FEATURES.energy.hop_s || (duration/rms.length);
    const cols = Math.max(1, Math.floor(W)); const amp = new Array(cols).fill(0);
    /* normalisation : le maximum de l'enveloppe fait toute la hauteur, 40 dB plus bas c'est le silence */
    let peak = -120; for(let i=0;i<rms.length;i++){ const d = +rms[i]; if(isFinite(d) && d>peak) peak = d; }
    if(peak < -100) peak = 0; const floor = peak - 40;
    for(let i=0;i<rms.length;i++){ const d = +rms[i]; if(!isFinite(d)) continue; const c = Math.min(cols-1, Math.floor(x(i*hop))); const a = Math.max(0, Math.min(1, (d-floor)/(peak-floor))); if(a>amp[c]) amp[c]=a; }
    for(let c=0;c<cols;c++){ if(amp[c]===0 && c>0) amp[c] = amp[c-1]; }
    /* léger lissage sur 3 colonnes */
    const sm = amp.map((v,c)=>((amp[c-1]||v)+v+(amp[c+1]||v))/3);
    const path = ()=>{ ctx.beginPath(); ctx.moveTo(0, mid); for(let c=0;c<cols;c++) ctx.lineTo(c, mid - Math.max(1, sm[c]*half)); for(let c=cols-1;c>=0;c--) ctx.lineTo(c, mid + Math.max(1, sm[c]*half)); ctx.closePath(); };
    path(); ctx.fillStyle = loop ? "#b8c0cf" : "#3f4c63"; ctx.fill();
    if(loop){ ctx.save(); ctx.beginPath(); ctx.rect(x(loop.start), 0, x(loop.end)-x(loop.start), H); ctx.clip(); path(); ctx.fillStyle = "#1f5eff"; ctx.fill(); ctx.restore(); }
  } else {
    ctx.strokeStyle = "#c3cad6"; ctx.beginPath(); ctx.moveTo(0, mid); ctx.lineTo(W, mid); ctx.stroke();
    ctx.fillStyle = "#8a93a3"; ctx.font = "12px system-ui, sans-serif"; ctx.textBaseline = "middle"; ctx.fillText("forme d'onde indisponible (features.json absent)", 8, mid-14);
  }
  /* emphases */
  if(FEATURES && FEATURES.emphasis){ ctx.fillStyle = "#d97706"; FEATURES.emphasis.forEach(e=>{ ctx.beginPath(); ctx.arc(x(e.t), H-6, 2.5, 0, Math.PI*2); ctx.fill(); }); }
  /* repères de plans */
  ctx.strokeStyle = "rgba(28,35,48,.35)"; ctx.lineWidth = 1;
  shots.forEach(s=>{ const px = Math.round(x(s.start))+.5; ctx.beginPath(); ctx.moveTo(px, top-4); ctx.lineTo(px, bottom+12); ctx.stroke(); });
  ctx.fillStyle = "#5b6474"; ctx.font = "10px ui-monospace, monospace"; ctx.textBaseline = "bottom";
  shots.forEach(s=>{ const w = x(s.end)-x(s.start); if(w>22) ctx.fillText(s.id, x(s.start)+3, bottom+13); });
  /* frontières de sections */
  ctx.strokeStyle = "rgba(28,35,48,.7)"; sections.forEach(sec=>{ const px = Math.round(x(sec.start))+.5; ctx.beginPath(); ctx.moveTo(px,0); ctx.lineTo(px,H); ctx.stroke(); });
  /* curseur */
  if(AUDIO_SRC){ const px = x(audio.currentTime||0); ctx.strokeStyle = "#dc2626"; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(px,0); ctx.lineTo(px,H); ctx.stroke(); ctx.lineWidth = 1; }
}
window.addEventListener("resize", drawWave);

/* ---------- timeline ---------- */
(function timeline(){
  const tl = document.getElementById("timeline");
  const band = el("div","band"); sections.forEach(sec=>{ const d = el("div","seg", esc(sec.id)); d.style.flex = (sec.end-sec.start)+" 0 0"; d.style.background = secColor(sec.id); d.title = SECTION_LABEL[sec.id]+" ("+tc(sec.start)+" à "+tc(sec.end)+")"; band.appendChild(d); });
  const row = el("div","shots"); shots.forEach(s=>{ const d = el("div","shot", esc(s.id)); d.dataset.id = s.id; d.style.flex = s._dur+" 0 0"; d.style.minWidth = "22px"; d.style.background = typeColor(s.type); d.title = s.id+" "+s.type+" ("+tc(s.start)+" à "+tc(s.end)+", "+fmtS(s._dur)+")"; d.addEventListener("click", ()=>playShot(s.id)); row.appendChild(d); });
  const ticks = el("div","ticks"); const n = 6; for(let i=0;i<=n;i++) ticks.appendChild(el("span","",tc(duration*i/n)));
  tl.appendChild(band); tl.appendChild(row); tl.appendChild(ticks);
  /* masque les étiquettes qui ne tiennent pas dans leur segment (le titre reste au survol) */
  const meas = document.createElement("canvas").getContext("2d");
  const fit = ()=>tl.querySelectorAll(".seg, .shot").forEach(d=>{ const label = d.dataset.label || (d.dataset.label = d.textContent); meas.font = getComputedStyle(d).font; d.textContent = (meas.measureText(label).width + 6 > d.clientWidth) ? "" : label; });
  fit(); window.addEventListener("resize", fit);
  const lg = document.getElementById("legend"); TYPES.forEach(t=>{ if(shots.some(s=>s.type===t)) lg.appendChild(el("span","", "<i style='background:"+typeColor(t)+"'></i>"+t)); });
})();

/* ---------- courbe d'énergie ---------- */
function drawEnergy(){
  const box = document.getElementById("energy");
  const W = Math.max(320, box.clientWidth || 1000), H = 120, padL = 30, padR = 10, padT = 12, padB = 24;
  const x = t => duration ? padL + t/duration*(W-padL-padR) : padL;
  const y = e => padT + (5-e)/4*(H-padT-padB);
  let svg = "<svg viewBox='0 0 "+W+" "+H+"' width='"+W+"' height='"+H+"' xmlns='http://www.w3.org/2000/svg' role='img' aria-label='Énergie des beats'>";
  sections.forEach(sec=>{ svg += "<rect x='"+x(sec.start)+"' y='"+padT+"' width='"+(x(sec.end)-x(sec.start))+"' height='"+(H-padT-padB)+"' fill='"+secColor(sec.id)+"' opacity='.08'/>"; });
  for(let e=1;e<=5;e++) svg += "<line x1='"+padL+"' x2='"+(W-padR)+"' y1='"+y(e)+"' y2='"+y(e)+"' stroke='#e3e7ee'/><text x='"+(padL-6)+"' y='"+(y(e)+4)+"' font-size='11' text-anchor='end' fill='#5b6474'>"+e+"</text>";
  const pts = beats.map(b=>{ const mx = (b.start+b.end)/2; return [x(mx), y(+b.energy||1), b]; });
  if(pts.length){
    let d = ""; pts.forEach((p,i)=>{ d += (i?" L":"M")+p[0]+" "+p[1]; });
    const area = "M"+x(beats[0].start)+" "+y(1)+" L"+pts.map(p=>p[0]+" "+p[1]).join(" L")+" L"+x(beats[beats.length-1].end)+" "+y(1)+" Z";
    svg += "<path d='"+area+"' fill='#1f5eff' opacity='.10'/>";
    svg += "<path d='"+d+"' fill='none' stroke='#1f5eff' stroke-width='2.5' stroke-linejoin='round'/>";
    pts.forEach(p=>{ svg += "<circle cx='"+p[0]+"' cy='"+p[1]+"' r='4' fill='#fff' stroke='#1f5eff' stroke-width='2'/><text x='"+p[0]+"' y='"+(H-8)+"' font-size='11' text-anchor='middle' fill='#5b6474'>"+esc(p[2].id)+"</text>"; });
  }
  svg += "</svg>";
  box.innerHTML = svg;
}
drawEnergy();
window.addEventListener("resize", drawEnergy);

/* ---------- texte de la voix ---------- */
function voiceHtml(shot){
  const b = shot._beat; const pivot = (b.pivot_word||"").toLowerCase();
  if(WORDS && WORDS.words && WORDS.words.length){
    const ws = WORDS.words.filter(w => w.end > b.start + 0.01 && w.start < b.end - 0.01);
    if(ws.length){
      /* un seul mot pivot : d'abord par le texte (première occurrence), sinon par le temps */
      const norm = s => String(s||"").toLowerCase().replace(/[^\p{L}\p{N}]/gu,"");
      let pivotIdx = pivot ? ws.findIndex(w => norm(w.w) === norm(pivot)) : -1;
      if(pivotIdx < 0 && b.pivot_t != null) pivotIdx = ws.findIndex(w => w.start - 0.05 <= b.pivot_t && b.pivot_t <= w.end + 0.05);
      return ws.map((w,i)=>{
        const inShot = w.end > shot.start + 0.02 && w.start < shot.end - 0.02;
        const t = esc(w.w)+esc(w.punct_after||"");
        return "<span class='w"+(inShot?" in":"")+"'>"+(i===pivotIdx?"<mark>"+t+"</mark>":t)+"</span>";
      }).join(" ");
    }
  }
  const text = b.text || "";
  if(pivot){ const i = text.toLowerCase().indexOf(pivot); if(i>=0) return esc(text.slice(0,i))+"<mark>"+esc(text.slice(i,i+pivot.length))+"</mark>"+esc(text.slice(i+pivot.length)); }
  return esc(text);
}

/* ---------- cartes ---------- */
const cardsEl = document.getElementById("cards");
function buildCard(s){
  const st = shotState(s.id);
  const card = el("article","card"+(st.found?" found":"")); card.dataset.id = s.id; card.dataset.type = s.type; card.dataset.section = s._section; card.style.setProperty("--card-color", typeColor(s.type));
  const head = el("div","head");
  head.appendChild(el("span","id", esc(s.id)));
  head.appendChild(el("span","tc", tc(s.start)+" → "+tc(s.end)+" ("+fmtS(s._dur)+")"));
  head.appendChild(el("span","pill sec", esc(s._section))).style.background = secColor(s._section);
  const right = el("div","right");
  if(AUDIO_SRC){ const lb = el("button","small listen","écouter"); lb.type="button"; lb.dataset.id = s.id; lb.addEventListener("click", ()=>playShot(s.id)); right.appendChild(lb); }
  const fl = el("label","found-label"); const cb = document.createElement("input"); cb.type="checkbox"; cb.checked = !!st.found; cb.addEventListener("change", ()=>{ st.found = cb.checked; saveState(); card.classList.toggle("found", cb.checked); syncFound(s.id, cb.checked); applyFilters(); });
  fl.appendChild(cb); fl.appendChild(document.createTextNode(" trouvé")); right.appendChild(fl);
  head.appendChild(right); card.appendChild(head);

  const file = el("div","file"); file.appendChild(el("code","", esc(s.filename||"(nom de fichier manquant)"))); if(s.filename) file.appendChild(copyBtn(s.filename,"copier")); card.appendChild(file);

  const bq = el("blockquote","voice", voiceHtml(s)); bq.title = "Beat "+s._beat.id+" ("+esc(s._beat.function||"")+"), mot pivot : "+(s._beat.pivot_word||"")+" à "+tc(s._beat.pivot_t||0); card.appendChild(bq);
  card.appendChild(el("p","desc", "<b>Ce qu'on voit :</b> "+esc(s.description||"")));

  const bd = el("div","badges");
  bd.appendChild(el("span","pill type", esc(s.type))).style.background = typeColor(s.type);
  bd.appendChild(el("span","badge", "valeur : <b>"+esc(VALUE_LABEL[s.value]||s.value||"?")+"</b>"));
  bd.appendChild(el("span","badge", "caméra : <b>"+esc(CAMERA_LABEL[s.camera]||s.camera||"?")+"</b>"));
  bd.appendChild(el("span","badge", "<b>"+esc(ORIENT_LABEL[s.orientation]||s.orientation||"?")+"</b>"));
  bd.appendChild(el("span","badge", "énergie : <b>"+esc(s._beat.energy!=null?s._beat.energy+"/5":"?")+"</b>"));
  bd.appendChild(el("span","badge", "fonction : <b>"+esc(s._beat.function||"?")+"</b>"));
  card.appendChild(bd);

  if(s.query_en || s.query_fr){
    const q = el("div","q");
    if(s.query_en){ q.appendChild(el("span","lab","EN")); q.appendChild(el("span","txt", esc(s.query_en))); q.appendChild(copyBtn(s.query_en,"copier")); }
    if(s.query_fr){ q.appendChild(el("span","lab","FR")); q.appendChild(el("span","txt", esc(s.query_fr))); q.appendChild(copyBtn(s.query_fr,"copier")); }
    card.appendChild(q);
  }
  if(s.query_en){
    const links = el("div","links");
    const cleanQ = s.query_en.replace(/[^\p{L}\p{N}\s-]/gu," ").replace(/\s+/g," ").trim();
    SEARCH_SITES.forEach(([name,fn])=>{ const a = document.createElement("a"); a.href = fn(cleanQ, s.orientation); a.target = "_blank"; a.rel = "noopener"; a.textContent = name; links.appendChild(a); });
    card.appendChild(links);
  } else if(s.type==="MOTION"){
    card.appendChild(el("p","muted fb","Plan à fabriquer en motion design, pas de recherche de stock."));
  }

  const ai = s.ai_prompt || {};
  if(ai.image || ai.motion){
    const det = el("div","ai-box"); const tg = el("button","toggle","Prompt IA (image et mouvement)"); tg.type="button"; tg.addEventListener("click", ()=>det.classList.toggle("open")); det.appendChild(tg);
    const box = el("div","ai");
    if(ai.image){ const q = el("div","q"); q.appendChild(el("span","lab","IMG")); q.appendChild(el("span","txt", esc(ai.image))); q.appendChild(copyBtn(ai.image,"copier")); box.appendChild(q); }
    if(ai.motion){ const q = el("div","q"); q.appendChild(el("span","lab","MVT")); q.appendChild(el("span","txt", esc(ai.motion))); q.appendChild(copyBtn(ai.motion,"copier")); box.appendChild(q); }
    if(ai.image && ai.motion){ const r = el("div","row"); r.appendChild(copyBtn(ai.image+"\n\n"+ai.motion,"copier les deux")); box.appendChild(r); }
    det.appendChild(box); card.appendChild(det);
  }

  const dl = el("dl","specs");
  const add = (k,v)=>{ if(v==null || v==="" || (Array.isArray(v)&&!v.length)) return; dl.appendChild(el("dt","",esc(k))); dl.appendChild(el("dd","",v)); };
  add("Rush minimum", s.min_rush_s!=null ? esc(fmtS(s.min_rush_s)) : null);
  add("Doit montrer", Array.isArray(s.must_show) ? s.must_show.map(m=>"<span class='badge'>"+esc(m)+"</span>").join(" ") : esc(s.must_show));
  add("Texte à l'écran", s.overlay_text ? "<b>"+esc(s.overlay_text)+"</b>" : null);
  add("SFX", s.sfx ? esc(s.sfx) : null);
  if(s.fallback && s.fallback.type){ add("Repli", "<span class='pill type' style='background:"+typeColor(s.fallback.type)+"'>"+esc(s.fallback.type)+"</span> "+(s.fallback.query_en?"<span class='mono'>"+esc(s.fallback.query_en)+"</span>":"")); }
  card.appendChild(dl);

  const ta = document.createElement("textarea"); ta.placeholder = "Notes (source trouvée, lien, remarque de tournage)"; ta.value = st.notes||""; ta.addEventListener("input", ()=>{ st.notes = ta.value; saveState(); });
  card.appendChild(ta);
  return card;
}
shots.forEach(s=>cardsEl.appendChild(buildCard(s)));
function syncFound(id, found){
  document.querySelectorAll(".tl .shot[data-id='"+id+"']").forEach(d=>d.classList.toggle("found", found));
  document.querySelectorAll("#tournage tr[data-id='"+id+"']").forEach(tr=>{ tr.classList.toggle("found", found); const c = tr.querySelector("input"); if(c) c.checked = found; });
  document.querySelectorAll(".card[data-id='"+id+"']").forEach(c=>{ c.classList.toggle("found", found); const cb = c.querySelector(".found-label input"); if(cb) cb.checked = found; });
}

/* ---------- filtres ---------- */
const filter = {types:new Set(), sections:new Set(), missing:false, q:""};
(function filters(){
  const ft = document.getElementById("f-types"); TYPES.forEach(t=>{ if(!shots.some(s=>s.type===t)) return; const c = el("button","chip", "<span class='dot'></span>"+t); c.type="button"; c.style.color = typeColor(t); c.dataset.t = t; c.addEventListener("click", ()=>{ if(filter.types.has(t)) filter.types.delete(t); else filter.types.add(t); c.classList.toggle("on"); c.style.background = c.classList.contains("on") ? typeColor(t) : ""; applyFilters(); }); ft.appendChild(c); });
  const fs = document.getElementById("f-sections"); sections.forEach(sec=>{ const c = el("button","chip", "<span class='dot'></span>"+sec.id); c.type="button"; c.style.color = secColor(sec.id); c.addEventListener("click", ()=>{ if(filter.sections.has(sec.id)) filter.sections.delete(sec.id); else filter.sections.add(sec.id); c.classList.toggle("on"); c.style.background = c.classList.contains("on") ? secColor(sec.id) : ""; applyFilters(); }); fs.appendChild(c); });
  document.getElementById("f-missing").addEventListener("change", e=>{ filter.missing = e.target.checked; applyFilters(); });
  document.getElementById("f-search").addEventListener("input", e=>{ filter.q = e.target.value.trim().toLowerCase(); applyFilters(); });
  document.getElementById("f-reset").addEventListener("click", ()=>{ filter.types.clear(); filter.sections.clear(); filter.missing=false; filter.q=""; document.getElementById("f-missing").checked=false; document.getElementById("f-search").value=""; document.querySelectorAll(".chip.on").forEach(c=>{ c.classList.remove("on"); c.style.background=""; }); applyFilters(); });
})();
function applyFilters(){
  let shown = 0, found = 0;
  shots.forEach(s=>{
    const st = shotState(s.id); if(st.found) found++;
    let ok = true;
    if(filter.types.size && !filter.types.has(s.type)) ok = false;
    if(filter.sections.size && !filter.sections.has(s._section)) ok = false;
    if(filter.missing && st.found) ok = false;
    if(filter.q){ const hay = [s.id, s.filename, s.description, s.query_en, s.query_fr, s._beat.text, s.overlay_text, s.type, s._section, (s.must_show||[]).join(" "), st.notes].join(" ").toLowerCase(); if(!hay.includes(filter.q)) ok = false; }
    const c = cardsEl.querySelector(".card[data-id='"+s.id+"']"); if(c) c.classList.toggle("hidden", !ok);
    if(ok) shown++;
  });
  document.getElementById("counter").innerHTML = "<b>"+found+"</b> plan"+(found>1?"s":"")+" trouvé"+(found>1?"s":"")+" sur <b>"+shots.length+"</b>, "+shown+" affiché"+(shown>1?"s":"")+ (shots.length-found>0 ? ", "+(shots.length-found)+" à trouver" : ", tout est trouvé");
  let empty = cardsEl.querySelector(".empty"); if(!shown){ if(!empty){ empty = el("div","empty","Aucun plan ne correspond aux filtres."); cardsEl.appendChild(empty); } } else if(empty) empty.remove();
}
applyFilters();

/* ---------- plan de tournage ---------- */
(function tournage(){
  const box = document.getElementById("tournage");
  const shootable = shots.filter(s=>s.type==="UGC"||s.type==="PRODUIT");
  const groups = []; const placed = new Set();
  (BRIEF.shooting_plan||[]).forEach(g=>{ if(!g || !g.location) return; const ids = (g.shots||[]).filter(id=>shotById[id]); ids.forEach(id=>placed.add(id)); groups.push({location:g.location, ids:ids, source:"brief"}); });
  const KEYS = [["salle de bain",/salle de bain|douche|lavabo|baignoire|toilettes|wc\b/i],["cuisine",/cuisine|plan de travail|évier|evier|frigo|placard/i],["salon",/salon|canapé|canape|télé|tele|tapis/i],["chambre",/chambre|lit\b|oreiller/i],["extérieur",/extérieur|exterieur|jardin|terrasse|rue|balcon/i],["bureau",/bureau|ordinateur|écran|ecran/i],["table produit, fond neutre",/packshot|fond blanc|fond neutre|table produit|pack\b|packaging|logo|produit posé/i]];
  const heur = {}; shootable.forEach(s=>{ if(placed.has(s.id)) return; const txt = (s.description||"")+" "+(s.query_fr||""); let loc = "lieu à définir"; for(const [name,re] of KEYS){ if(re.test(txt)){ loc = name; break; } } (heur[loc] = heur[loc]||[]).push(s.id); });
  Object.keys(heur).forEach(loc=>groups.push({location:loc, ids:heur[loc], source:"auto"}));
  if(!groups.length){ box.appendChild(el("p","muted","Aucun plan UGC ou PRODUIT à tourner : tout vient de stock, de motion ou d'IA.")); return; }
  groups.forEach(g=>{
    const ids = g.ids.filter(id=>shotById[id]); if(!ids.length) return;
    const total = ids.reduce((a,id)=>a+(+shotById[id].min_rush_s||shotById[id]._dur),0);
    const sec = el("section","loc");
    sec.appendChild(el("h3","", esc(g.location)+" <span class='muted'>"+ids.length+" prise"+(ids.length>1?"s":"")+", environ "+fmtS(total)+" de rushes"+(g.source==="auto"?", regroupement automatique":"")+"</span>"));
    const tbl = el("table"); tbl.innerHTML = "<thead><tr><th></th><th>Plan</th><th>Type</th><th>Valeurs à tourner</th><th>Caméra</th><th>Mini</th><th>Ce qu'on voit</th></tr></thead>";
    const tb = el("tbody");
    ids.forEach(id=>{ const s = shotById[id]; const st = shotState(id);
      const vals = [s.value].concat(SEQ3.filter(v=>v!==s.value).slice(0,2)).map((v,i)=>"<span class='"+(i?"":"main")+"'>"+esc(VALUE_LABEL[v]||v)+"</span>").join("");
      const tr = el("tr", st.found?"found":""); tr.dataset.id = id;
      tr.innerHTML = "<td class='nostrike'><input type='checkbox'"+(st.found?" checked":"")+"></td><td class='plan'><b>"+esc(id)+"</b><br><code style='font-size:11px'>"+esc(s.filename||"")+"</code></td><td><span class='pill type' style='background:"+typeColor(s.type)+"'>"+esc(s.type)+"</span></td><td class='nostrike vals-cell'><div class='vals'>"+vals+"</div></td><td data-label='caméra'>"+esc(CAMERA_LABEL[s.camera]||s.camera||"")+"</td><td data-label='mini'>"+esc(s.min_rush_s!=null?fmtS(s.min_rush_s):fmtS(s._dur))+"</td><td class='desc'>"+esc(s.description||"")+(s.must_show&&s.must_show.length?"<br><span class='muted'>doit montrer : "+esc(s.must_show.join(", "))+"</span>":"")+(s.overlay_text?"<br><span class='muted'>texte : "+esc(s.overlay_text)+"</span>":"")+"</td>";
      tr.querySelector("input").addEventListener("change", e=>{ st.found = e.target.checked; saveState(); syncFound(id, st.found); applyFilters(); });
      tb.appendChild(tr);
    });
    tbl.appendChild(tb); sec.appendChild(tbl); box.appendChild(sec);
  });
})();

/* ---------- nomenclature ---------- */
(function nomen(){
  const names = shots.map(s=>s.filename).filter(Boolean);
  const proj = project.name || "projet";
  let tree = proj + "/\n  " + ((BRIEF.audio&&BRIEF.audio.file)||"voix.mp3") + "\n  script.txt\n  brief.json\n  brief.html\n  rushes/\n";
  names.forEach((n,i)=>{ tree += "    " + n + "\n"; });
  tree += "  work/   (intermédiaires, gérés par le skill)\n  out/    (final_9x16.mp4, final.srt, qc_report.md)";
  document.getElementById("tree").textContent = tree;
  document.getElementById("names").textContent = names.join("\n");
  document.getElementById("btn-copy-names").addEventListener("click", e=>copyText(names.join("\n"), e.target));
})();

/* ---------- onglets ---------- */
document.querySelectorAll(".tabs .tab").forEach(b=>b.addEventListener("click", ()=>{
  document.querySelectorAll(".tabs .tab").forEach(x=>x.classList.toggle("active", x===b));
  document.querySelectorAll(".view").forEach(v=>v.classList.toggle("active", v.id==="view-"+b.dataset.view));
  try{ localStorage.setItem(STORE_KEY+":view", b.dataset.view); }catch(e){}
}));
try{ const v = localStorage.getItem(STORE_KEY+":view"); if(v){ const b = document.querySelector(".tabs .tab[data-view='"+v+"']"); if(b) b.click(); } }catch(e){}

/* ---------- export ---------- */
function download(name, mime, content){ const blob = new Blob([content], {type:mime}); const url = URL.createObjectURL(blob); const a = document.createElement("a"); a.href = url; a.download = name; document.body.appendChild(a); a.click(); document.body.removeChild(a); setTimeout(()=>URL.revokeObjectURL(url), 2000); }
function csvCell(v){ if(v==null) v=""; if(Array.isArray(v)) v = v.join(" | "); v = String(v); return '"'+v.replace(/"/g,'""').replace(/\r?\n/g," ")+'"'; }
document.getElementById("btn-csv").addEventListener("click", ()=>{
  const cols = ["id","section","fonction","beat","start","end","duree_s","type","valeur","camera","orientation","energie","filename","description","query_en","query_fr","min_rush_s","must_show","overlay_text","sfx","fallback_type","fallback_query_en","ai_image","ai_motion","trouve","notes"];
  const rows = [cols.join(";")];
  shots.forEach(s=>{ const st = shotState(s.id); const b = s._beat; rows.push([s.id, s._section, b.function, b.id, s.start.toFixed(3), s.end.toFixed(3), s._dur.toFixed(3), s.type, s.value, s.camera, s.orientation, b.energy, s.filename, s.description, s.query_en, s.query_fr, s.min_rush_s, s.must_show, s.overlay_text, s.sfx, s.fallback&&s.fallback.type, s.fallback&&s.fallback.query_en, s.ai_prompt&&s.ai_prompt.image, s.ai_prompt&&s.ai_prompt.motion, st.found?"oui":"non", st.notes].map(csvCell).join(";")); });
  download((project.name||"brief")+"_shotlist.csv", "text/csv;charset=utf-8", "﻿"+rows.join("\r\n"));
});
document.getElementById("btn-json").addEventListener("click", ()=>{
  const out = {schema:"broll-director/brief-export/1", exported_at:new Date().toISOString(), brief:BRIEF, state:{}};
  shots.forEach(s=>{ const st = shotState(s.id); out.state[s.id] = {found:!!st.found, notes:st.notes||""}; });
  download((project.name||"brief")+"_export.json", "application/json", JSON.stringify(out, null, 2));
});
document.getElementById("btn-print").addEventListener("click", ()=>window.print());

updatePlayUi(); updateTime(); drawWave();
window.BROLL = {shots:shots, playShot:playShot, stopLoop:stopLoop, state:()=>state, applyFilters:applyFilters};
})();
</script>
</body>
</html>
'''


def build(brief, features, words, profile, audio_src, gen_date):
    title = f"{brief.get('project', {}).get('name', 'brief')} : shot list B-roll"
    page = TEMPLATE
    page = page.replace("__TITLE__", html.escape(title))
    page = page.replace("__BRIEF_JSON__", json_for_html(brief))
    page = page.replace("__FEATURES_JSON__", json_for_html(features) if features else "null")
    page = page.replace("__WORDS_JSON__", json_for_html(words) if words else "null")
    page = page.replace("__PROFILE_JSON__", json_for_html(profile) if profile else "null")
    page = page.replace("__AUDIO_JSON__", json_for_html(audio_src) if audio_src else "null")
    page = page.replace("__GEN_DATE__", gen_date)
    return page


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="build_brief.py",
        description="Génère brief.html, la shot list interactive CRÉATION FULL B-ROLL ARTISTE, à partir d'un brief.json validé. "
                    "Page autonome : lecteur audio avec forme d'onde, timeline, cartes par plan avec liens de recherche, "
                    "plan de tournage, nomenclature, export CSV et JSON, cases 'trouvé' et notes persistées dans le navigateur.",
        epilog="Exemple : python3 build_brief.py brief.json --out brief.html --audio voix.mp3 --features work/features.json",
    )
    parser.add_argument("brief", help="chemin du brief.json (schéma broll-director/brief/1)")
    parser.add_argument("--out", required=True, help="chemin du fichier HTML à produire")
    parser.add_argument("--audio", default=None,
                        help="fichier audio de la voix off (défaut : brief.audio.file à côté du brief). "
                             "Inclus en base64 s'il pèse moins de 20 Mo, sinon référencé par chemin relatif")
    parser.add_argument("--features", default=None,
                        help="features.json (enveloppe RMS, pauses, emphases) pour la forme d'onde "
                             "(défaut : work/features.json à côté du brief s'il existe)")
    parser.add_argument("--words", default=None,
                        help="words.json (alignement mot à mot) pour surligner les mots de chaque plan "
                             "(défaut : work/words.json à côté du brief s'il existe)")
    parser.add_argument("--profiles", default=None,
                        help="profiles.json pour afficher les cibles de durée par section "
                             "(défaut : assets/profiles.json à côté du dossier scripts)")
    parser.add_argument("--no-audio", action="store_true", help="ne pas inclure ni référencer l'audio")
    args = parser.parse_args(argv)

    brief_path = Path(args.brief)
    out_path = Path(args.out)
    brief = load_json(brief_path, "le brief")
    if brief is None:
        return 2
    brief_dir = brief_path.resolve().parent
    out_dir = out_path.resolve().parent

    brief_dur = (brief.get("audio") or {}).get("duration_s")

    def check_duration(obj, path, explicit, label):
        """Ignore un fichier découvert automatiquement dont la durée ne correspond pas à l'audio du brief."""
        d = obj.get("duration_s") if isinstance(obj, dict) else None
        if isinstance(d, (int, float)) and isinstance(brief_dur, (int, float)) and abs(d - brief_dur) > 0.5:
            msg = f"[AVERT.] {label} {path} : durée {d}s différente de l'audio du brief ({brief_dur}s)"
            if explicit:
                print(msg + ", fichier utilisé quand même", file=sys.stderr)
                return obj
            print(msg + f", fichier ignoré (passez --{label} pour forcer)", file=sys.stderr)
            return None
        return obj

    features = None
    fpath = Path(args.features) if args.features else brief_dir / "work" / "features.json"
    if fpath.exists():
        features = check_duration(load_json(fpath, "features"), fpath, bool(args.features), "features")
        if features is not None:
            # on ne garde que ce qui sert à la page
            features = {k: features.get(k) for k in ("duration_s", "pauses", "emphasis", "energy", "speech_rate_wps") if k in features}
    elif args.features:
        print(f"[AVERT.] features introuvable : {fpath}", file=sys.stderr)

    words = None
    wpath = Path(args.words) if args.words else brief_dir / "work" / "words.json"
    if wpath.exists():
        words = check_duration(load_json(wpath, "words"), wpath, bool(args.words), "words")
    elif args.words:
        print(f"[AVERT.] words introuvable : {wpath}", file=sys.stderr)

    profile = None
    ppath = Path(args.profiles) if args.profiles else default_profiles_path()
    if ppath.exists():
        profiles = load_json(ppath, "profiles")
        if profiles:
            name = (brief.get("project") or {}).get("profile")
            if name in profiles:
                profile = {"name": name, "shot": profiles[name].get("shot"),
                           "relance_max_s": profiles[name].get("relance_max_s"),
                           "product_share_min": profiles[name].get("product_share_min")}

    audio_src, audio_info = (None, "audio désactivé (--no-audio)") if args.no_audio else resolve_audio(args, brief, brief_dir, out_dir)

    gen_date = dt.datetime.now().strftime("%d/%m/%Y à %H:%M")
    page = build(brief, features, words, profile, audio_src, gen_date)
    try:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(page, encoding="utf-8")
    except OSError as exc:
        print(f"[ERREUR] impossible d'écrire {out_path} : {exc}", file=sys.stderr)
        return 2

    n_shots = sum(len(b.get("shots") or []) for b in brief.get("beats") or [])
    size = out_path.stat().st_size
    print(f"brief.html généré : {out_path} ({size / 1024:.0f} Ko, {n_shots} plans)")
    print(f"  audio    : {audio_info}")
    features_info = f"oui ({fpath})" if features else "non, forme d'onde remplacée par les repères seuls"
    words_info = f"oui ({wpath})" if words else "non, mot pivot surligné par recherche de texte"
    profile_info = f"oui ({ppath})" if profile else "non, cibles de durée non affichées"
    print(f"  features : {features_info}")
    print(f"  words    : {words_info}")
    print(f"  profil   : {profile_info}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
