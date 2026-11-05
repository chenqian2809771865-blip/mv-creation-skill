# preview.py WxH F0 F1 out.mp4 : quick review render (crf 18, veryfast)
import os, sys, subprocess, time
os.environ['MV_OUT'] = sys.argv[1]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render
f0, f1, out = int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
W, H = (int(v) for v in sys.argv[1].split('x'))
cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'bgra', '-s', f'{W}x{H}', '-r', '24', '-i', '-',
       '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-threads', '2', out]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
R = render.Renderer()
t0 = time.time()
for f in range(f0, f1):
    p.stdin.write(R.frame(f / 24).tobytes())
p.stdin.close(); p.wait()
print('DONE', out, f'{time.time() - t0:.0f}s', flush=True)
