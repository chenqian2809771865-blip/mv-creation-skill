import os as _os
_CODE = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), '..'))
_ROOT = _os.path.normpath(_os.path.join(_CODE, '..'))   # project root (fonts/, out/, assets/)
# verify final mp4: compare decoded frames (8x8 block centers) with render.frame_small(t)
import sys, subprocess, json
sys.path.insert(0, _CODE)
import numpy as np
import render
mp4 = sys.argv[1]
pr = json.loads(subprocess.run(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', mp4], capture_output=True, text=True).stdout)
for s in pr['streams']:
    print(s['codec_type'], s.get('width'), s.get('height'), s.get('r_frame_rate'), s.get('nb_frames'), s.get('duration'))
print('format duration', pr['format']['duration'], 'size MB %.1f' % (int(pr['format']['size']) / 1e6))
for fi in [0, 2, 100, 300, 700, 1200, 1500, 2000, 2500, 2900, 3200, 3325]:
    t = fi / 24
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', mp4, '-vf', 'select=eq(n\\,%d)' % fi, '-vframes', '1', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'],
                         capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8).reshape(1440, 2560, 3)[4::8, 4::8].astype(int)
    b = render.frame_small(t).astype(int)
    print('frame %d t=%.2f mean abs diff %.2f' % (fi, t, np.abs(a - b).mean()))
