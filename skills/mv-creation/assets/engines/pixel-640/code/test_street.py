import sys; sys.path.insert(0,'.')
from core import *
from street import render_street
from PIL import Image
tiles=[]
for (cx,cy,z,v) in ((0,0,1,'night'),(620,0,1,'night'),(1000,0,1,'night'),(900,0,1,'moon'),(900,0,1,'memory'),(960,112,2.2,'night')):
    img,_=render_street(cx,cy,z,v,t=1.0)
    tiles.append(Image.fromarray(upscale(img,1)))
S=Image.new('RGB',(1280,1080))
for i,im in enumerate(tiles): S.paste(im,((i%2)*640,(i//2)*360))
S.save('../out/check/street_a.png')
