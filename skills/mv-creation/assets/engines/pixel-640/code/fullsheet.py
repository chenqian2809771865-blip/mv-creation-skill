import os as _os
_CODE = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__))))
_ROOT = _os.path.normpath(_os.path.join(_CODE, '..'))   # project root (fonts/, out/, assets/)
import sys; sys.path.insert(0,_CODE)
import render
from core import *
from PIL import Image, ImageDraw
t0,t1,step,out=float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
ts=[]; t=t0
while t<t1: ts.append(t); t+=step
cols=5; tw,th=384,216
rows=(len(ts)+cols-1)//cols
S=Image.new('RGB',(tw*cols,th*rows))
for i,t in enumerate(ts):
    f=render.frame(t); im=Image.fromarray(np.clip(f+0.5,0,255).astype(np.uint8)).resize((tw,th),Image.NEAREST)
    d=ImageDraw.Draw(im); d.rectangle([0,0,44,11],fill=(0,0,0)); d.text((2,0),f'{t:.1f}',fill=(255,255,0))
    S.paste(im,((i%cols)*tw,(i//cols)*th))
S.save(out); print(len(ts))
