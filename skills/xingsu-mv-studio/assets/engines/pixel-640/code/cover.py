# -*- coding: utf-8 -*-
import os as _os
_CODE = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__))))
_ROOT = _os.path.normpath(_os.path.join(_CODE, '..'))   # project root (fonts/, out/, assets/)
"""3:4 title keyframe: 240x320 logical grid x6 -> 1440x1920. Only his cloud is raining on a dry moonlit street."""
import sys; sys.path.insert(0, _CODE)
import numpy as np, math
from core import *
from street import render_street, GY
from sprite import place
from chars import HIM
from cloud import draw_cloud, cloud_rain
from skyline import moon, night_cloud
from fx import splashes
from PIL import Image

CW, CH = 240, 320
z = 1.5
hx_world = 1196
cam_x = hx_world - 120 / z
cam_y = GY + 14 - 262 / z
t = 63.0
st = dict(flower=0, noodle=0, b4=0, shutter=1.0, lantern=1, signal='green')
img, info = render_street(cam_x, cam_y, z, 'moon', st, t=t, reflect_k=0.32, ow=CW, oh=CH)
T = info['T']
# sky above the roofs: deeper, with moon + parting clouds
sky_h = int(T(0, 118)[1])
moon(img, 196, 34, 12, glow=1.0)
night_cloud(img, 40, 30, 0.55, seed=2, col=(40, 48, 84), rim=(130, 150, 210))
rng = np.random.default_rng(3)
for i in range(30):
    x, y = rng.integers(0, CW), rng.integers(0, max(10, sky_h - 30))
    if img[y, x].sum() < 260:
        img[y, x] = (210, 216, 244)
# him, front, looking up at his cloud
s = 1.08
fx, fy = T(hx_world, GY + 14)
fy = 266
spr, anc = HIM(view='front', s=round(s, 3), look_up=0.85, rim=(1, 0), rim_col=(200, 214, 255))
place(img, spr, anc, fx, fy)
hat_top = fy - 100 * s
cx, cy = fx + 2, hat_top - 34
x0, x1, yb = draw_cloud(img, cx, cy, 1.45, t=t, mood=0.15, tint=(0.86, 0.9, 0.97))
cloud_rain(img, t, x0 + 6, x1 - 6, int(yb), int(fy) + 2, density=4.5, seed=9, color=(214, 224, 250), length=9)
splashes(img, t, fy - 2, fy + 3, x0=int(x0) + 4, x1=int(x1) - 4, rate=90, seed=3, scale=(1.0, 1.4))
# puddle at his feet with the moon in it
pm = m_ellipse(fx + 4, fy + 4, 30, 4, CW, CH)
img[pm] = img[pm] * 0.5 + np.array([70, 90, 140]) * 0.5
fill(img, m_ellipse(fx - 10, fy + 4, 4, 1.5, CW, CH) & pm, (232, 234, 222))

# ---- title block ----
for i, a in enumerate((0.62, 0.55, 0.45, 0.34, 0.22, 0.1)):
    y0, y1 = i * 19, (i + 1) * 19
    img[y0:y1] = img[y0:y1] * (1 - a) + np.array([14, 14, 30]) * a
def text(s_, x, y, col, scale=1, ol=(18, 16, 32), sh=True):
    m = text_mask(s_, 16)
    if scale > 1:
        m = np.repeat(np.repeat(m, scale, 0), scale, 1)
    h, w = m.shape
    x = int(x - w / 2)
    full = np.zeros((CH, CW), bool)
    full[y:y + h, x:x + w] = m
    if sh:
        sh_m = np.zeros_like(full); sh_m[y + scale:y + h + scale, x + scale:x + w + scale] = m
        img[sh_m & ~full] = ol
    img[outline_of(full, diag=True)] = ol
    img[full] = col
    return full

title = text('下雨了', 120, 12, (248, 246, 240), scale=3)
# rain drips hanging from the title strokes
ys, xs = np.nonzero(title)
bottom = title & ~shift(title, 0, -1)
by, bx = np.nonzero(bottom)
for i in range(0, len(bx), 9):
    L = 2 + int(h01(i, 4) * 5)
    for k in range(1, L + 1):
        yy = by[i] + k
        if yy < CH:
            img[yy, bx[i]] = (176, 206, 246) if k < L else (236, 246, 255)
text('薛之谦 · 绅士', 120, 66, (230, 222, 226))
# hook line (small, warm)
text('雨停了，只剩他头顶在下', 120, 88, (255, 212, 110))
# pixel tag
tag = m_rect(6, 6, 74, 24, CW, CH)
img[tag] = (255, 212, 110)
img[outline_of(tag)] = (18, 16, 32)
m = text_mask('像素MV', 12 if False else 16)
# small tag text in 16px unifont fits 4 chars? use 3 glyph widths
tm = text_mask('像素', 16)
yy, xx = 7, 8
img[yy:yy + tm.shape[0], xx:xx + tm.shape[1]][tm] = (30, 24, 40)
tm2 = text_mask('MV', 16)
img[yy:yy + tm2.shape[0], xx + tm.shape[1] + 2:xx + tm.shape[1] + 2 + tm2.shape[1]][tm2] = (30, 24, 40)

out = upscale(img, 6)
Image.fromarray(out).save(_os.path.join(_ROOT, 'out/下雨了_标题关键帧_3x4.png'))
Image.fromarray(upscale(img, 2)).save(_os.path.join(_ROOT, 'out/check/cover_preview.png'))
print(out.shape)
