# beatstrip.py video.mp4 outdir [--w 960] [--per 8] [--even] [--k0 K --k1 K] [--cols 3|2]
# For each beat k: the frame before, the frame that contains the beat (red label), and the frame after.
# Cells default to 960 wide (the 《宠坏》 spec); --even keeps only felt beats (76 BPM: even k); --cols 2 drops the after-frame.
import sys, json, subprocess, os
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
B = json.load(open(os.path.join(HERE, '..', 'data', 'beats.json')))['beats']
args = sys.argv[1:]
src, outdir = args[0], args[1]


def opt(name, d):
    return type(d)(args[args.index(name) + 1]) if name in args else d


w = opt('--w', 960)
per = opt('--per', 8)
cols = opt('--cols', 3)
k0, k1 = opt('--k0', 0), opt('--k1', len(B))
h = w * 9 // 16
os.makedirs(outdir, exist_ok=True)
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                     capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
ks = [k for k in range(k0, min(k1, len(B))) if ('--even' not in args or k % 2 == 0)]
for s in range(0, len(ks), per):
    grp = ks[s:s + per]
    S = Image.new('RGB', (cols * w, len(grp) * h), 'black')
    d = ImageDraw.Draw(S)
    for r, k in enumerate(grp):
        fb = int(B[k] * 24)          # frame whose interval [f/24, (f+1)/24) contains the beat
        offs = (-1, 0, 1)[:cols]
        for c, o in enumerate(offs):
            f = fb + o
            if 0 <= f < len(fr):
                S.paste(Image.fromarray(fr[f]), (c * w, r * h))
            lab = f'k{k} f{f} {B[k]:.2f}s' + (' BEAT' if o == 0 else '')
            d.rectangle([c * w, r * h, c * w + 170, r * h + 16], fill='red' if o == 0 else 'black')
            d.text((c * w + 3, r * h + 3), lab, fill='white')
    S.save(os.path.join(outdir, f'strip_k{grp[0]:03d}-k{grp[-1]:03d}.png'))
print('wrote', (len(ks) + per - 1) // per, 'sheets ->', outdir)
