import os as _os
_CODE = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
_ROOT = _os.path.normpath(_os.path.join(_CODE, '..'))   # project root (fonts/, out/, assets/)
# frames.py out.png t1 t2 ... : render chosen frames side by side (x2), 2 per row
import sys; sys.path.insert(0, _CODE)
import numpy as np
from PIL import Image
import render
from px import upscale
ts = [float(v) for v in sys.argv[2:]]
tiles = [render.frame_small(t) for t in ts]
while len(tiles) % 2:
    tiles.append(np.zeros_like(tiles[0]))
g = np.vstack([np.hstack(tiles[i:i + 2]) for i in range(0, len(tiles), 2)])
Image.fromarray(upscale(g, 2)).save(sys.argv[1])
