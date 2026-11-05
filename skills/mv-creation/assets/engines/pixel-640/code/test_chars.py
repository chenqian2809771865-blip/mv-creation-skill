import sys; sys.path.insert(0,'.')
from core import *
from chars import *
from sprite import place
img = new((52,58,84), 640, 360)
img[250:] = (40,44,64)
x = 30
for (v, w, lu) in (('front',None,0),('front',None,1.0),('side',None,0),('side',0.0,0),('side',0.25,0),('side',0.5,0),('side',0.75,0),('back',None,0)):
    spr, anc, _ = him(v, s=0.82, walk=w, look_up=lu)
    place(img, spr, anc, x, 140)
    x += 40
spr,anc,_ = him('front', s=1.9, look_up=0.0); place(img, spr, anc, 380, 250)
spr,anc,_ = him('side', s=1.9, walk=0.1); place(img, spr, anc, 460, 250)
spr,anc,_ = him('front', s=1.9, hat=False, smile=1); place(img, spr, anc, 560, 250)
x=30
for (v,w,e) in (('front',None,'calm'),('front',None,'smile'),('side',None,'calm'),('side',0.0,'calm'),('side',0.5,'calm'),('back',None,'calm')):
    spr,anc,_ = her(v, s=0.82*0.86, walk=w, expr=e)
    place(img, spr, anc, x, 300); x+=40
spr,anc,_ = her('front', s=2.4*0.86, expr='smile'); place(img, spr, anc, 300, 355)
spr,ax,ay = umbrella(s=1.4); blit(img, spr, int(260-ax), int(300-ay))
spr,ax,ay = umbrella(s=1.4, open_=0); blit(img, spr, int(330-ax), int(240-ay))
save_png(img, '../out/check/chars_a.png', 2)
