import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render
from core import *
from PIL import Image, ImageDraw
t0,t1,step,out=float(sys.argv[1]),float(sys.argv[2]),float(sys.argv[3]),sys.argv[4]
ts=[]; t=t0
while t<t1: ts.append(t); t+=step
cols=6; tw,th=320,180
rows=(len(ts)+cols-1)//cols
S=Image.new('RGB',(tw*cols,th*rows))
for i,t in enumerate(ts):
    f=render.frame(t); im=Image.fromarray(np.clip(f+0.5,0,255).astype(np.uint8)).resize((tw,th),Image.NEAREST)
    d=ImageDraw.Draw(im); d.rectangle([0,0,40,11],fill=(0,0,0)); d.text((2,0),f'{t:.1f}',fill=(255,255,0))
    S.paste(im,((i%cols)*tw,(i//cols)*th))
S.save(out); print(len(ts))
