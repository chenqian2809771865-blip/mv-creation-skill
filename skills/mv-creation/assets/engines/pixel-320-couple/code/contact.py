import os as _os
_CODE = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__))))
_ROOT = _os.path.normpath(_os.path.join(_CODE, '..'))   # project root (fonts/, out/, assets/)
# contact sheet: python3 contact.py T0 T1 STEP out.png [cols]
import sys, time; sys.path.insert(0, _CODE)
import numpy as np
from PIL import Image, ImageDraw
import render
t0, t1, step = float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3])
out = sys.argv[4]; cols = int(sys.argv[5]) if len(sys.argv) > 5 else 4
ts = list(np.arange(t0, t1, step))
tiles = []
tm = time.time()
for t in ts:
    a = render.frame_small(t)
    im = Image.fromarray(np.repeat(np.repeat(a, 2, 0), 2, 1))
    d = ImageDraw.Draw(im); d.rectangle([0, 0, 64, 12], fill=(0, 0, 0)); d.text((2, 0), '%.2f %s' % (t, render.SH[render.shot_at(t + render.LEAD)][0]), fill=(255, 255, 0))
    tiles.append(np.array(im))
print('avg %.3fs/frame' % ((time.time() - tm) / len(ts)))
rows = (len(tiles) + cols - 1) // cols
h, w = tiles[0].shape[:2]
g = np.zeros((rows * h, cols * w, 3), np.uint8)
for i, a in enumerate(tiles):
    g[(i // cols) * h:(i // cols + 1) * h, (i % cols) * w:(i % cols + 1) * w] = a
Image.fromarray(g).save(out)
