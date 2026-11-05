import os as _os
_CODE = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__))))
_ROOT = _os.path.normpath(_os.path.join(_CODE, '..'))   # project root (fonts/, out/, assets/)
import sys; sys.path.insert(0,_CODE)
import render
from story import SHOTS
fs=set()
for r in SHOTS:
    a,b=int(round(r[1]*24)),int(round(r[2]*24))
    fs.update(range(a,min(a+4,b))); fs.update(range(max(a,b-4),b)); fs.update(range(a,b,9))
fs=sorted(f for f in fs if f < int(round(render.DUR*24)))
bad=0
for f in fs:
    try: render.frame(f/24)
    except Exception as e:
        print('FAIL',f,f/24,repr(e)); bad+=1
        if bad>5: break
print('checked',len(fs),'bad',bad)
