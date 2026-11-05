# usage: python3 final.py SCALE OUTNAME   -> full-length video-only master with the upload params
import sys, os, subprocess, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render
from core import *
OUT = os.path.join(ROOT, 'out')
k, name = int(sys.argv[1]), sys.argv[2]
Wd, Hd = W * k, H * k
cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (Wd, Hd), '-r', str(FPS), '-i', '-',
       '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', '14',
       '-tune', 'animation', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
       '-profile:v', 'high', '-level:v', '5.1',
       '-x264-params', 'ref=4:vbv-maxrate=50000:vbv-bufsize=100000:keyint=48:min-keyint=24:rc-lookahead=30',
       '-threads', '2', os.path.join(OUT, name)]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
N = int(round(render.DUR * FPS))
ts = time.time()
for f in range(N):
    a = np.clip(render.frame(f / FPS) + 0.5, 0, 255).astype(np.uint8)
    p.stdin.write(np.repeat(np.repeat(a, k, 0), k, 1).tobytes())
    if f % 120 == 0:
        print('x%d frame %d/%d %.0fs' % (k, f, N, time.time() - ts), flush=True)
p.stdin.close(); p.wait()
print('DONE x%d %.0fs rc=%s' % (k, time.time() - ts, p.returncode), flush=True)
