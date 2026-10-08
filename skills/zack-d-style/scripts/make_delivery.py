#!/usr/bin/env python3
"""Dossier de montage : make_delivery.py <run_dir>. Lit <run>/run.json {"vo": "...mp3", "script": "...txt"} et <run>/jobs/legs.json."""
import json, os, shutil, subprocess, sys
run = os.path.abspath(sys.argv[1]); os.chdir(run); cfg = json.load(open("run.json"))
D = "EXPORTS/MONTAGE"; os.makedirs(D+"/clips-bruts", exist_ok=True); os.makedirs(D+"/clips-recales-VO", exist_ok=True)
jobs = json.load(open("jobs/legs.json")); lines = [l.strip() for l in open(cfg["script"]) if l.strip()]
vodur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",cfg["vo"]],capture_output=True,text=True).stdout.strip())
fiche = [f"# {cfg.get('brand','')} — ZACK {cfg.get('recipe','')} — fiche de montage (VO = {os.path.basename(cfg['vo'])}, {vodur:.1f} s)", "", "Chaque clip couvre la phrase indiquée : poser à VO-début, finir à VO-fin. clips-recales-VO/ = déjà recalés.", ""]
missing = []
with open("tmp_list.txt", "w") as L:
    for i, j in enumerate(jobs, 1):
        src = f"jobs/OUT/{j['name']}.mp4"
        if not os.path.exists(src): missing.append(j["name"]); continue
        base = f"{i:02d}_{j['name']}_{j['vo_start']:.1f}-{j['vo_end']:.1f}s.mp4"; shutil.copy(src, f"{D}/clips-bruts/{base}")
        dur = float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",src],capture_output=True,text=True).stdout.strip())
        f = j["target_s"]/dur; out = f"{D}/clips-recales-VO/{base}"
        subprocess.run(["ffmpeg","-v","error","-y","-i",src,"-vf",f"setpts={f:.5f}*PTS,fps=30,scale=1080:1920,format=yuv420p","-an","-c:v","libx264","-crf","18","-preset","fast",out], check=True)
        L.write(f"file '{os.path.abspath(out)}'\n")
        txt = " / ".join(lines[x-1] for x in j.get("lines", [])) if j.get("lines") else "(pas de VO, outro pour la caption)"
        fiche.append(f"{i:02d}. {j['name']} · VO {j['vo_start']:.1f} → {j['vo_end']:.1f} s ({j['target_s']} s) · clip {j.get('duration','5')} s · vitesse x{1/f:.2f}\n    « {txt} »")
shutil.copy(cfg["vo"], D+"/"+os.path.basename(cfg["vo"])); open(D+"/FICHE-MONTAGE.txt","w").write("\n".join(fiche)+"\n")
subprocess.run(["ffmpeg","-v","error","-y","-f","concat","-safe","0","-i","tmp_list.txt","-i",cfg["vo"],"-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k",D+"/APERCU-recale-avec-VO.mp4"], check=True)
os.remove("tmp_list.txt"); print("manquants:", missing, "| aperçu:", D+"/APERCU-recale-avec-VO.mp4")
