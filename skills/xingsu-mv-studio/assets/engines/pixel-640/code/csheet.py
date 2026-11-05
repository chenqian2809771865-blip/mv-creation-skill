import os as _os
_CODE = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__))))
_ROOT = _os.path.normpath(_os.path.join(_CODE, '..'))   # project root (fonts/, out/, assets/)
import sys, time; sys.path.insert(0,_CODE)
import render
from core import *
from PIL import Image, ImageDraw
out=sys.argv[1]; ts=[float(x) for x in sys.argv[2:]]
tiles=[]
for t in ts:
    t0=time.time(); f=render.frame(t); dt=time.time()-t0
    im=Image.fromarray(upscale(f,1)); d=ImageDraw.Draw(im); d.rectangle([0,0,90,12],fill=(0,0,0)); d.text((2,1),f'{t:.2f} {dt*1000:.0f}ms',fill=(255,255,0)); tiles.append(im)
cols=3; rows=(len(tiles)+cols-1)//cols
S=Image.new('RGB',(640*cols,360*rows))
for i,im in enumerate(tiles): S.paste(im,((i%cols)*640,(i//cols)*360))
S.save(out); print('ok')
