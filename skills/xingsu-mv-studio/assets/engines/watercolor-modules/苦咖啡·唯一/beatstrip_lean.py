# beatstrip_lean.py video.mp4 outdir [--w 960] [--per 4] [--k0 K --k1 K]
# Same sheets as beatstrip.py (frame before / beat frame (red label) / frame after, one row per beat) but memory-light:
# frames are dumped once to outdir/_frames as JPEG instead of holding the whole decoded video in RAM.
import sys, json, subprocess, os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
B = json.load(open(os.path.join(HERE, '..', 'data', 'beats.json')))['beats']
args = sys.argv[1:]
src, outdir = args[0], args[1]


def opt(name, d):
    return type(d)(args[args.index(name) + 1]) if name in args else d


w = opt('--w', 960)
per = opt('--per', 4)
k0, k1 = opt('--k0', 0), opt('--k1', len(B))
h = w * 9 // 16
fd = os.path.join(outdir, '_frames')
os.makedirs(fd, exist_ok=True)
if not os.path.exists(os.path.join(fd, 'f00001.jpg')):
    subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'scale={w}:{h}', '-q:v', '3', '-start_number', '0',
                    os.path.join(fd, 'f%05d.jpg')], check=True)
n = len([f for f in os.listdir(fd) if f.endswith('.jpg')])
ks = list(range(k0, min(k1, len(B))))
for s in range(0, len(ks), per):
    grp = ks[s:s + per]
    S = Image.new('RGB', (3 * w, len(grp) * h), 'black')
    d = ImageDraw.Draw(S)
    for r, k in enumerate(grp):
        fb = int(B[k] * 24)
        for c, o in enumerate((-1, 0, 1)):
            f = fb + o
            if 0 <= f < n:
                S.paste(Image.open(os.path.join(fd, f'f{f:05d}.jpg')), (c * w, r * h))
            d.rectangle([c * w, r * h, c * w + 190, r * h + 18], fill='red' if o == 0 else 'black')
            d.text((c * w + 3, r * h + 3), f'k{k} f{f} {B[k]:.2f}s' + (' BEAT' if o == 0 else ''), fill='white')
    S.save(os.path.join(outdir, f'strip_k{grp[0]:03d}-k{grp[-1]:03d}.jpg'), quality=88)
print('wrote', (len(ks) + per - 1) // per, 'sheets ->', outdir)
