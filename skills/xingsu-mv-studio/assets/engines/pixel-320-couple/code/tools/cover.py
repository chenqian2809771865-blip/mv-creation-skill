# 3:4 cover: 240x320 logical grid, x6 -> 1440x1920.  python3 tools/cover.py out.png preview.png
import sys, os, math
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from PIL import Image
from px import Cv, hx, mix, vgrad, bayer, text, text_w, upscale, OUT
from chars import chibi, blit_chibi
from scenes import rain, splashes, umbrella, RED_UMB, glow, lamp, buildings
from scenes_qt import forecast_screen, shade
from shots import lit

W, H = 240, 320
c = Cv(W, H)
# dark classroom wall (power cut), the TV still shows the sunny forecast
vgrad(c, 0, 150, [hx('#141626'), hx('#1a1c30'), hx('#20243a')])
c.rect(0, 0, W, 6, hx('#262a40')); c.rect(0, 6, W, 1, hx('#10121e'))
c.rect(116, 0, 8, 12, hx('#3a3a46'))
glow(c, 120, 74, 120, hx('#7cb6ec'), k=0.32, dens=0.55, sy=0.75)
c.rect(13, 11, 214, 130, OUT)
c.rect(14, 12, 212, 128, hx('#3c3a46')); c.rect(14, 12, 212, 2, hx('#5a5866')); c.rect(14, 137, 212, 3, hx('#2a2832'))
c.rect(26, 18, 188, 110, hx('#24222a'))
g = forecast_screen(1.0, 0, 1.0, 0.7, True)
c.paste(g, 32, 23)
c.rect(196, 131, 3, 2, hx('#5aff7a'))
# red alert ticker across the middle (the hook)
c.rect(0, 146, W, 15, hx('#c8141e')); c.rect(0, 146, W, 1, hx('#ffd23a')); c.rect(0, 160, W, 1, hx('#7a0a12'))
c.rect(0, 147, 36, 13, hx('#ffd23a'))
text(c, 4, 147, '紧急', hx('#a8141e'), font='w')
text(c, 42, 147, '暴雨红色预警 · 请师生尽快回家', hx('#ffffff'), font='w')
# the school gate in the storm below
vgrad(c, 161, 268, [hx('#161a2c'), hx('#20263c'), hx('#2c3450'), hx('#3a4462')])
buildings(c, 262, 61, hx('#1c2034'), win=hx('#d8b060'), lit=0.2, x1=W, hmin=20, hmax=70)
c.rect(8, 186, 10, 82, hx('#6a6e84')); c.rect(222, 186, 10, 82, hx('#6a6e84'))
c.rect(0, 178, W, 9, hx('#4a2e30')); c.rect(0, 178, W, 2, hx('#6a4044'))
for x in range(18, 222, 7):
    c.rect(x, 226, 2, 42, hx('#3a3e52'))
c.rect(18, 226, 204, 3, hx('#3a3e52'))
c.rect(0, 268, W, 52, hx('#1c2032'))
for y in range(272, 320, 8):
    c.rect(0, y, W, 1, hx('#242a40'))
lamp(c, 196, 268, h=78, on=True, glow_col=hx('#ffd68a'), post=hx('#121220'), glow_r=34)
for y in range(272, 320, 2):  # lamp reflection on the wet ground
    if (y // 2) % 3:
        w_ = 2 + (y - 272) // 9
        c.rect(196 - w_ // 2 + int(math.sin(y * 0.5) * 2), y, w_, 1, hx('#8a7048'))
# the couple under the red umbrella, half-res layer x2
Lr = Cv(120, 60, alpha=True)
fx, fy = 52, 57
he = chibi('he', 'side', 'stand', case=True, eyes='open', mouth='line', arm=150, arm2=70)
she = chibi('she', 'side', 'stand', eyes='open', mouth='smile', arm=70)
blit_chibi(Lr, lit(he, 'rain'), fx, fy)
blit_chibi(Lr, lit(she, 'lamp'), fx + 22, fy, flip=True)
a = math.radians(150)
hx_, hy_ = fx - 1 + 7 * math.sin(a), fy - 18 + 7 * math.cos(a)
umbrella(Lr, hx_, hy_, *RED_UMB, open_=1.0, w=44, tilt=6, shaft=16)
Lr.rect(fx + 9, fy - 18, 4, 3, (244, 203, 170, 255))
L2 = upscale(Lr.a, 2)
m = L2[..., 3] > 127
reg = c.a[160:280, 0:240]
reg[m] = L2[..., :3][m]
rain(c, 3.0, 170, 5, speed=380, wind=-120, length=9, col=hx('#7a8ab0'), area=(0, 162, W, 320))
splashes(c, 3.0, 270, 318, n=40, seed=6, col=hx('#9aaad0'))
# small tag
c.rect(182, 0, 56, 12, hx('#fbf6ea')); c.rect(182, 12, 56, 1, OUT)
text(c, 186, 0, '像素 MV', hx('#c8141e'), font='w')
Image.fromarray(upscale(c.a, 6)).save(sys.argv[1])
Image.fromarray(upscale(c.a, 2)).save(sys.argv[2])
print('ok')
