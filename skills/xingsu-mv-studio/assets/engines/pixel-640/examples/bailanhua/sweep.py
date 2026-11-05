import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render
from story import SHOTS
fs=set()
for r in SHOTS:
    a,b=int(round(r[1]*24)),int(round(r[2]*24))
    fs.update(range(a,min(a+3,b))); fs.update(range(max(a,b-3),b)); fs.update(range(a,b,11))
fs=sorted(f for f in fs if f < int(round(render.DUR*24)))
bad=0
for f in fs:
    try: render.frame(f/24)
    except Exception as e:
        import traceback; print('FAIL',f,f/24,repr(e)); traceback.print_exc(limit=3); bad+=1
        if bad>5: break
print('checked',len(fs),'bad',bad)
