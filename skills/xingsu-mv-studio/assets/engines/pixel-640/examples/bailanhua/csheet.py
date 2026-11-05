import sys, time, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render
from core import *
from PIL import Image, ImageDraw
out=sys.argv[1]; ts=[float(x) for x in sys.argv[2:]]
tiles=[]
for t in ts:
    t0=time.time(); f=render.frame(t); dt=time.time()-t0
    im=Image.fromarray(upscale(f,1)); d=ImageDraw.Draw(im); d.rectangle([0,0,96,12],fill=(0,0,0)); d.text((2,1),f'{t:.2f} {dt*1000:.0f}ms',fill=(255,255,0)); tiles.append(im)
cols=3 if len(tiles)>4 else 2; rows=(len(tiles)+cols-1)//cols
S=Image.new('RGB',(640*cols,360*rows))
for i,im in enumerate(tiles): S.paste(im,((i%cols)*640,(i//cols)*360))
S.save(out); print('ok')
