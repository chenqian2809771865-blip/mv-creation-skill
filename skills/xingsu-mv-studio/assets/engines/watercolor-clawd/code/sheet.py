# sheet.py out.png T1 T2 ... [--w 640 --cols 4] : contact sheet of frames at clip times (MV_OUT default 960x540)
import os, sys, time
os.environ.setdefault('MV_OUT', '960x540')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render
from PIL import Image, ImageDraw
args = sys.argv[1:]
out = args.pop(0)
w, cols = 640, 4
if '--w' in args:
    i = args.index('--w'); w = int(args[i + 1]); del args[i:i + 2]
if '--cols' in args:
    i = args.index('--cols'); cols = int(args[i + 1]); del args[i:i + 2]
ts = [float(a) for a in args]
R = render.Renderer()
h = int(w * 9 / 16)
rows = (len(ts) + cols - 1) // cols
S = Image.new('RGB', (cols * w, rows * h), 'black')
d = ImageDraw.Draw(S)
t0 = time.time()
for k, t in enumerate(ts):
    a = R.frame(t - 1.0 / 24)
    im = Image.fromarray(a[..., [2, 1, 0]]).resize((w, h), Image.LANCZOS)
    x, y = (k % cols) * w, (k // cols) * h
    S.paste(im, (x, y))
    d.rectangle([x, y, x + 64, y + 18], fill='black')
    d.text((x + 4, y + 3), '%.2f' % t, fill='white')
print('%.2f s/frame' % ((time.time() - t0) / max(1, len(ts))))
S.save(out)
