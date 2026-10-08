#!/usr/bin/env python3
"""SRT calé sur l'audio du montage : make_srt.py <montage.mp4> <script.txt> <out.srt> [lang=en]. Whisper mots -> réalignés sur le VRAI script -> blocs courts style Zack."""
import re, json, difflib, sys
from faster_whisper import WhisperModel
import subprocess, tempfile
wav=tempfile.mktemp(suffix=".wav"); subprocess.run(["ffmpeg","-v","error","-y","-i",sys.argv[1],"-vn","-ac","1","-ar","16000",wav],check=True)
LANG=sys.argv[4] if len(sys.argv)>4 else "en"
mdl=WhisperModel("small.en" if LANG=="en" else "small", compute_type="int8")
segs,_=mdl.transcribe(wav, language=LANG, word_timestamps=True)
heard=[{"w":w.word.strip(),"s":w.start,"e":w.end} for s in segs for w in (s.words or []) if w.word.strip()]
script=" ".join(l.strip() for l in open(sys.argv[2]) if l.strip())
tokens=script.split()  # mots du vrai script avec ponctuation
norm=lambda t: re.sub(r"[^a-z0-9àâäéèêëîïôöùûüç']","",t.lower())
A=[norm(t) for t in tokens]; B=[norm(h["w"]) for h in heard]
sm=difflib.SequenceMatcher(None,A,B,autojunk=False)
times=[None]*len(tokens)
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag=="equal":
        for k in range(i2-i1): times[i1+k]=(heard[j1+k]["s"],heard[j1+k]["e"])
    elif tag=="replace":
        # répartit linéairement les mots entendus sur les mots du script
        n=i2-i1; m=j2-j1
        for k in range(n):
            j=j1+min(m-1,int(k*m/n)); times[i1+k]=(heard[j]["s"],heard[j]["e"])
# interpolation des mots sans timing (insert dans script / delete côté audio)
for i,t in enumerate(times):
    if t is None:
        prev=next((times[k] for k in range(i-1,-1,-1) if times[k]),None); nxt=next((times[k] for k in range(i+1,len(times)) if times[k]),None)
        if prev and nxt: times[i]=(prev[1],nxt[0])
        elif prev: times[i]=(prev[1],prev[1]+0.3)
        else: times[i]=(nxt[0]-0.3,nxt[0])
# blocs : phrase -> clauses (virgules, deux-points) -> si > 5 mots, découpe équilibrée en morceaux <= 4 ; puis fusion des blocs < 0,45 s avec le voisin
words=list(zip(tokens,times)); clauses=[]; cur=[]
for w in words:
    cur.append(w)
    if re.search(r"[.!?,:]$",w[0]): clauses.append(cur); cur=[]
if cur: clauses.append(cur)
def split_bal(c):
    n=len(c)
    if n<=5: return [c]
    k=-(-n//4); base,extra=divmod(n,k); out=[]; i=0
    for x in range(k):
        j=i+base+(1 if x<extra else 0); out.append(c[i:j]); i=j
    return out
blocks=[b for c in clauses for b in split_bal(c)]
dur=lambda b: b[-1][1][1]-b[0][1][0]
out=[]
for b in blocks:
    if out and (dur(b)<0.45 or len(b)==1) and len(out[-1])+len(b)<=6 and not re.search(r"[.!?]$",out[-1][-1][0]): out[-1]=out[-1]+b
    elif out and (dur(out[-1])<0.45) and len(out[-1])+len(b)<=6: out[-1]=out[-1]+b
    else: out.append(b)
def ts(x): x=max(0,x); h=int(x//3600); m=int(x%3600//60); s=x%60; return f"{h:02d}:{m:02d}:{s:06.3f}".replace(".",",")
lines=[]
for i,b in enumerate(out,1):
    s=b[0][1][0]; e=b[-1][1][1]
    if i<len(out): e=min(e+0.08, out[i][0][1][0]-0.02)  # petit maintien, sans chevaucher
    lines.append(f"{i}\n{ts(s)} --> {ts(e)}\n{' '.join(t for t,_ in b)}\n")
open(sys.argv[3],"w",encoding="utf-8").write("\n".join(lines))
print(len(out),"blocs · premier mot",round(heard[0]["s"],2),"s · dernier",round(heard[-1]["e"],2),"s · non alignés:",sum(1 for tag,*_ in sm.get_opcodes() if tag!="equal"),"zones")
