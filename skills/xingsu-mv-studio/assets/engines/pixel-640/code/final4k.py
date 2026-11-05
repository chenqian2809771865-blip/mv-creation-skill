import os as _os
_CODE = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__))))
_ROOT = _os.path.normpath(_os.path.join(_CODE, '..'))   # project root (fonts/, out/, assets/)
import sys, os, subprocess, time
sys.path.insert(0, _CODE)
import render
from core import *
OUT = _os.path.join(_ROOT, 'out/下雨了_像素MV_4K_抖音上传版.mp4')
AUD = os.path.join(ASSETS, 'audio_cut.wav')
cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '3840x2160', '-r', '24', '-i', '-', '-i', AUD,
       '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-tune', 'animation', '-profile:v', 'high', '-level:v', '5.1', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
       '-profile:v', 'high', '-x264-params', 'keyint=48:min-keyint=24:ref=4', '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', OUT + '.tmp.mp4']
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
N = int(round(render.DUR * 24))
for f in range(N):
    a = np.clip(render.frame(f / 24) + 0.5, 0, 255).astype(np.uint8)
    p.stdin.write(np.repeat(np.repeat(a, 6, 0), 6, 1).tobytes())
p.stdin.close(); p.wait()
os.replace(OUT + '.tmp.mp4', OUT)
print('DONE', os.path.getsize(OUT))
