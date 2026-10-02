#!/usr/bin/env python3
"""Téléverse un fichier lourd (vidéo, audio, image) dans le Drive « Studio marketing » par l'API Google Drive.

L'outil Drive du chat est limité à quelques Mo ; ce script utilise l'envoi « resumable » de l'API (morceaux de 8 Mo),
sans limite pratique de taille.

Clés dans `.env` à la racine (jamais affichées) :
  GDRIVE_CLIENT_ID, GDRIVE_CLIENT_SECRET, GDRIVE_REFRESH_TOKEN   (client OAuth du compte Google de l'utilisateur, portée drive)

Usage (depuis la racine du studio) :
  python3 scripts/drive_upload.py <fichier> --dossier <ID dossier Drive> [--nom nom.mp4] [--remplacer]
  python3 scripts/drive_upload.py --test        # vérifie les clés (affiche seulement l'adresse du compte)

--remplacer : met à la corbeille les fichiers du même nom déjà présents dans le dossier (règle du studio : une seule version).
Affiche une ligne JSON : id, nom, taille, lien.
"""
import argparse, json, mimetypes, os, sys, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHUNK = 8 * 1024 * 1024


def env():
    vals = {k: v for k, v in os.environ.items() if k.startswith("GDRIVE_")}
    for line in (open(os.path.join(ROOT, ".env")) if os.path.exists(os.path.join(ROOT, ".env")) else []):
        if "=" in line and not line.startswith("#"):
            k, v = line.strip().split("=", 1)
            vals.setdefault(k, v.strip().strip('"'))
    try:
        return vals["GDRIVE_CLIENT_ID"], vals["GDRIVE_CLIENT_SECRET"], vals["GDRIVE_REFRESH_TOKEN"]
    except KeyError as e:
        sys.exit(f"clé absente de .env : {e.args[0]}")


def requete(url, data=None, headers=None, method=None):
    req = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def jeton():
    cid, secret, refresh = env()
    data = urllib.parse.urlencode({"client_id": cid, "client_secret": secret, "refresh_token": refresh,
                                   "grant_type": "refresh_token"}).encode()
    st, _, body = requete("https://oauth2.googleapis.com/token", data,
                          {"Content-Type": "application/x-www-form-urlencoded"})
    if st != 200:
        sys.exit(f"échec d'authentification Google ({st}) : {json.loads(body).get('error', '?')}")
    return json.loads(body)["access_token"]


def api(tok, url, method="GET", payload=None):
    h = {"Authorization": f"Bearer {tok}"}
    data = None
    if payload is not None:
        h["Content-Type"] = "application/json"
        data = json.dumps(payload).encode()
    st, _, body = requete(url, data, h, method)
    return st, json.loads(body or b"{}")


def envoyer(tok, chemin, dossier, nom):
    taille = os.path.getsize(chemin)
    mime = mimetypes.guess_type(nom)[0] or "application/octet-stream"
    st, hdr, body = requete(
        "https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable&supportsAllDrives=true&fields=id,name,size,webViewLink",
        json.dumps({"name": nom, "parents": [dossier]}).encode(),
        {"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
         "X-Upload-Content-Type": mime, "X-Upload-Content-Length": str(taille)}, "POST")
    if st != 200:
        sys.exit(f"ouverture de l'envoi refusée ({st}) : {body[:300]!r}")
    session = hdr.get("Location") or hdr.get("location")
    with open(chemin, "rb") as f:
        debut = 0
        while debut < taille:
            bloc = f.read(CHUNK)
            fin = debut + len(bloc) - 1
            st, hdr, body = requete(session, bloc, {"Content-Length": str(len(bloc)),
                                                     "Content-Range": f"bytes {debut}-{fin}/{taille}"}, "PUT")
            if st in (200, 201):
                return json.loads(body)
            if st != 308:
                sys.exit(f"envoi interrompu ({st}) : {body[:300]!r}")
            debut = fin + 1
            print(f"  {debut * 100 // taille} %", file=sys.stderr)
    sys.exit("envoi terminé sans réponse finale")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("fichier", nargs="?")
    ap.add_argument("--dossier")
    ap.add_argument("--nom")
    ap.add_argument("--remplacer", action="store_true")
    ap.add_argument("--test", action="store_true")
    a = ap.parse_args()
    tok = jeton()
    if a.test:
        st, me = api(tok, "https://www.googleapis.com/drive/v3/about?fields=user(emailAddress)")
        print("connexion OK :", me.get("user", {}).get("emailAddress") if st == 200 else f"erreur {st}")
        return
    if not (a.fichier and a.dossier):
        sys.exit("indiquer un fichier et --dossier")
    nom = a.nom or os.path.basename(a.fichier)
    if a.remplacer:
        q = urllib.parse.quote(f"name = '{nom}' and '{a.dossier}' in parents and trashed = false")
        st, res = api(tok, f"https://www.googleapis.com/drive/v3/files?q={q}&fields=files(id)&supportsAllDrives=true&includeItemsFromAllDrives=true")
        for f in res.get("files", []):
            api(tok, f"https://www.googleapis.com/drive/v3/files/{f['id']}?supportsAllDrives=true", "PATCH", {"trashed": True})
            print(f"  ancienne version mise à la corbeille : {f['id']}", file=sys.stderr)
    r = envoyer(tok, a.fichier, a.dossier, nom)
    print(json.dumps({"id": r.get("id"), "nom": r.get("name"), "taille": r.get("size"), "lien": r.get("webViewLink")}, ensure_ascii=False))


if __name__ == "__main__":
    main()
