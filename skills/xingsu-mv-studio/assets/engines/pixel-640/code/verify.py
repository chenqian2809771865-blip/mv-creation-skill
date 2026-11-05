import os as _os
_CODE = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__))))
_ROOT = _os.path.normpath(_os.path.join(_CODE, '..'))   # project root (fonts/, out/, assets/)
import sys, subprocess, json; sys.path.insert(0,_CODE)
import numpy as np, render
from core import *
path, k = sys.argv[1], int(sys.argv[2])
info = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries','stream=codec_type,width,height,r_frame_rate,nb_frames,duration','-show_entries','format=duration,size','-of','json',path]))
print(json.dumps(info, ensure_ascii=False))
for t in (0.5, 19.0, 47.0, 70.5, 96.9, 121.5, 139.9, 146.0):
    f = int(round(t*FPS)); tt = f/FPS
    raw = subprocess.check_output(['ffmpeg','-v','error','-ss','%.4f'%(tt+0.001),'-i',path,'-frames:v','1','-f','rawvideo','-pix_fmt','rgb24','-'])
    a = np.frombuffer(raw, np.uint8).reshape(H*k, W*k, 3).astype(np.float32)
    g = a[k//2::k, k//2::k]
    ref = np.clip(render.frame(tt)+0.5,0,255).astype(np.uint8).astype(np.float32)
    print('t=%.2f mean abs diff %.2f' % (tt, np.abs(g-ref).mean()))
