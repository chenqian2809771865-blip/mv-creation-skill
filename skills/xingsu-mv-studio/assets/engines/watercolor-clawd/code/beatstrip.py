# beatstrip.py video.mp4 K0 K1 out.png : for each beat k, the frame before, the frame containing the beat, and the next frame
import sys, json, subprocess, numpy as np, os
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
B = json.load(open(os.path.join(HERE, '..', 'data', 'beats.json')))['beats']
src, k0, k1, out = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
w, h = 320, 180
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-vf', f'scale={w}:{h}', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], capture_output=True).stdout
fr = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
ks = list(range(k0, min(k1, len(B))))
S = Image.new('RGB', (3 * w, len(ks) * h), 'black'); d = ImageDraw.Draw(S)
for r, k in enumerate(ks):
    fb = int(B[k] * 24)          # frame whose interval contains the beat
    for c, f in enumerate((fb - 1, fb, fb + 1)):
        if 0 <= f < len(fr):
            S.paste(Image.fromarray(fr[f]), (c * w, r * h))
        lab = f'k{k} f{f}' + (' BEAT' if c == 1 else '')
        d.rectangle([c * w, r * h, c * w + 110, r * h + 14], fill='red' if c == 1 else 'black'); d.text((c * w + 2, r * h + 2), lab, fill='white')
S.save(out)
