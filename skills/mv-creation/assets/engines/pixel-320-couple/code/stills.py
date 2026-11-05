# python3 stills.py out.png t1 t2 ... (2x, labeled)
import sys, time
import numpy as np
from PIL import Image, ImageDraw
import render
ts = [float(x) for x in sys.argv[2:]]
tiles = []
tm = time.time()
for t in ts:
    a = render.frame_small(t)
    im = Image.fromarray(np.repeat(np.repeat(a, 2, 0), 2, 1))
    d = ImageDraw.Draw(im); d.rectangle([0, 0, 70, 12], fill=(0, 0, 0)); d.text((2, 0), '%.2f %s' % (t, render.SH[render.shot_at(t + render.LEAD)][0]), fill=(255, 255, 0))
    tiles.append(np.array(im))
print('avg %.3fs/frame' % ((time.time() - tm) / len(ts)))
cols = 3 if len(tiles) > 2 else len(tiles)
rows = (len(tiles) + cols - 1) // cols
h, w = tiles[0].shape[:2]
g = np.zeros((rows * h, cols * w, 3), np.uint8)
for i, a in enumerate(tiles):
    g[(i // cols) * h:(i // cols + 1) * h, (i % cols) * w:(i % cols + 1) * w] = a
Image.fromarray(g).save(sys.argv[1])
