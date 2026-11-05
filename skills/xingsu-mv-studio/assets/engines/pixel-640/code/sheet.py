# -*- coding: utf-8 -*-
import os as _os
_CODE = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__))))
_ROOT = _os.path.normpath(_os.path.join(_CODE, '..'))   # project root (fonts/, out/, assets/)
"""contact sheet: python3 sheet.py module out.png t1 t2 ... [--k 1] [--cols 3]"""
import sys, importlib, time, numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, _CODE)
from core import upscale

args = sys.argv[1:]
k = 1; cols = 3
if '--k' in args:
    i = args.index('--k'); k = int(args[i + 1]); del args[i:i + 2]
if '--cols' in args:
    i = args.index('--cols'); cols = int(args[i + 1]); del args[i:i + 2]
mod = importlib.import_module(args[0])
out = args[1]
ts = [float(x) for x in args[2:]]
tiles = []
for t in ts:
    t0 = time.time()
    f = mod.frame(t)
    dt = time.time() - t0
    im = Image.fromarray(upscale(f, k))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 120, 14], fill=(0, 0, 0))
    d.text((3, 1), f't={t:.2f} {dt*1000:.0f}ms', fill=(255, 255, 0))
    tiles.append(im)
w, h = tiles[0].size
rows = (len(tiles) + cols - 1) // cols
S = Image.new('RGB', (w * cols, h * rows), (0, 0, 0))
for i, im in enumerate(tiles):
    S.paste(im, ((i % cols) * w, (i // cols) * h))
S.save(out)
print('saved', out, S.size)
