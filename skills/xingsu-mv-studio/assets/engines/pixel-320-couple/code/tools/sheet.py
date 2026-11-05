import os as _os
_CODE = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
_ROOT = _os.path.normpath(_os.path.join(_CODE, '..'))   # project root (fonts/, out/, assets/)
import sys; sys.path.insert(0,_CODE)
from px import *
from chars import *
from PIL import Image
c=Cv(320,180,(120,128,150))
c.rect(0,120,320,60,(90,96,118))
x=14
for who in ('he','she'):
    for view,pose,kw in [('front','stand',{}),('side','stand',{}),('back','stand',{}),('side','walk',{'phase':0.0}),('side','walk',{'phase':0.25}),('side','walk',{'phase':0.5}),('side','run',{'phase':0.2}),('front','sit',{}),('side','sit',{}),('side','floor',{'eyes':'closed'})]:
        k=dict(kw)
        if who=='he' and view!='back': k['case']= view=='side' and pose in('walk','run')
        if who=='he' and view=='back': k['case']=True
        s=chibi(who,view,pose,**k)
        blit_chibi(c,s,x,60 if who=='he' else 118)
        x+=31
    x=14
blit_chibi(c,chibi('he','front','stand',prop='phone',eyes='down'),300,60)
blit_chibi(c,chibi('she','front','stand',arm='up',mouth='smile',eyes='smile'),300,118)
c.blit(bust('he','open','line'),0,108-8)
c.blit(bust('she','smile','bigsmile'),70,100)
c.blit(bust('he','wet','sad','sad',tear=10),140,100)
c.blit(bust('she','closed','sad','sad',tear=6,wind=1),210,100)
c.blit(emote('heart',(230,70,90)),290,140); c.blit(emote('note',(60,60,90)),300,160)
text(c,4,2,'角色对照 他/她',(255,255,255),font='w')
Image.fromarray(upscale(c.a,4)).save(_os.path.join(_ROOT, 'out/check/chars.png'))
