import os as _os
_CODE = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__))))
_ROOT = _os.path.normpath(_os.path.join(_CODE, '..'))   # project root (fonts/, out/, assets/)
import sys, os, subprocess, time
sys.path.insert(0, _CODE)
import render
from core import *
DUR = render.DUR
OUT = _os.path.join(_ROOT, 'out')
AUD = os.path.join(ASSETS, 'audio_cut.wav')

def enc(path, k, crf):
    Wd, Hd = W * k, H * k
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (Wd, Hd), '-r', str(FPS), '-i', '-',
           '-i', AUD, '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', str(crf), '-tune', 'animation', '-profile:v', 'high', '-level:v', '5.1',
           '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-profile:v', 'high', '-x264-params', 'keyint=48:min-keyint=24:ref=4', '-threads', '1',
           '-c:a', 'aac', '-b:a', '320k', '-shortest', '-movflags', '+faststart', path]
    return subprocess.Popen(cmd, stdin=subprocess.PIPE)

p2 = enc(os.path.join(OUT, '下雨了_像素MV_2K.mp4'), 4, 14)
p4 = enc(os.path.join(OUT, '下雨了_像素MV_4K_抖音上传版.mp4'), 6, 14)
N = int(round(DUR * FPS))
ts = time.time()
for f in range(N):
    img = render.frame(f / FPS)
    a = np.clip(img + 0.5, 0, 255).astype(np.uint8)
    p2.stdin.write(np.repeat(np.repeat(a, 4, 0), 4, 1).tobytes())
    p4.stdin.write(np.repeat(np.repeat(a, 6, 0), 6, 1).tobytes())
    if f % 240 == 0:
        print('frame %d/%d %.0fs' % (f, N, time.time() - ts), flush=True)
for p in (p2, p4):
    p.stdin.close(); p.wait()
print('ALL DONE %.0fs' % (time.time() - ts), flush=True)
