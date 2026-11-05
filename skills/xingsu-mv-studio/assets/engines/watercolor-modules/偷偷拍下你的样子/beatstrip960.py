# beatstrip960.py video.mp4 outdir [per=4] : for every beat k: frame before / frame containing the beat / frame after, 960-wide cells
import sys, json, subprocess, numpy as np, os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
SB = json.load(open(os.path.join(HERE, '..', 'data', 'storyboard.json')))
B = SB['beats']
src, out = sys.argv[1], sys.argv[2]
per = int(sys.argv[3]) if len(sys.argv) > 3 else 4
os.makedirs(out, exist_ok=True)
w, h = 960, 540
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
ev = {}
for s in SB['shots']:
    for e in s['events']:
        ev[e['k']] = f"{s['id']} {e['what']}"
ks = [k for k in range(len(B)) if B[k] < SB['dur']]
for i in range(0, len(ks), per):
    grp = ks[i:i + per]
    S = Image.new('RGB', (3 * w, len(grp) * (h + 24)), 'black')
    d = ImageDraw.Draw(S)
    for r, k in enumerate(grp):
        fb = int(B[k] * 24)
        y = r * (h + 24)
        d.text((6, y + 5), f'k{k}  t={B[k]:.3f}s  beat frame f{fb}   EVENT: {ev.get(k, "-")}', fill='yellow')
        for c, f in enumerate((fb - 1, fb, fb + 1)):
            if 0 <= f < len(fr):
                S.paste(Image.fromarray(fr[f]), (c * w, y + 24))
            d.rectangle([c * w, y + 24, c * w + 150, y + 44], fill='red' if c == 1 else 'black')
            d.text((c * w + 4, y + 28), f'f{f}' + (' BEAT' if c == 1 else ''), fill='white')
    S.save(os.path.join(out, f'strip_k{grp[0]:02d}-k{grp[-1]:02d}.jpg'), quality=90)
print('ok', len(ks), 'beats')
