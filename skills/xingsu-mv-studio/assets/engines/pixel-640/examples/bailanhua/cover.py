# 3:4 title keyframe: 240x320 logical grid, x6 = 1440x1920. Redrawn (not a frame grab).
import sys, os; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *
from sprite import place
from chibi import HIM, unit_px
from props import orchid_pair, shape, npc_walker
from sh_street import render_street
from fx import rain, splashes
from PIL import Image
OW, OH = 240, 320
z = 1.6
cam_x, cam_y = 855 - (OW / 2) / z, 98.25
t = 6.3
mq = dict(flips=[0, 0, 0], clock=59, lights=1.0, chase=True, board=1.0, bulbs_on=1.0, flip_start=0.0,
          msg='午夜场 · 她没有来', kt=2)
img, info = render_street(cam_x, cam_y, z, 'night', state=dict(cinema=1.0), t=t, marquee=mq, ow=OW, oh=OH)
T = info['T']
k = 0.44 * z
# a passer-by with umbrella in the rain (right)
sx, sy = T(905, 272)
npc_walker(img, sx, sy, k, 0.3, kind=1, facing=-1, light='night')
# him under the canopy, looking up at the marquee, tickets + orchid
sx, sy = T(855, 262)
spr, anc = HIM(view='front', s=k, light='lamp', hand_r=(9.5, 70.0), hand_l=(-9.5, 70.0), look_up=0.9, mouth='flat', rim=(0, -1))
place(img, spr, anc, sx, sy)
hx, hy = unit_px(anc, k, sx, sy, 9.5, 71.0)
shape(img, m_rect(hx - 2, hy - 6, hx + 3, hy + 1, OW, OH), (240, 226, 196), outline=(40, 30, 30))
lx, ly = unit_px(anc, k, sx, sy, -9.5, 70.0)
orchid_pair(img, lx, ly + 1, s=0.9, angle=0.4, glow=0.3)
rain(img, t, density=0.9)
# signage text in-world: singer line on the canopy edge
draw_text(img, '林俊杰 · 学不会', OW // 2, int(T(0, 181)[1]), (250, 236, 210), outline=(30, 20, 26), anchor='mt')
# 像素MV tag
tag = m_rect(4, 4, 62, 24, OW, OH)
shape(img, tag, (255, 212, 110), outline=(30, 20, 26))
draw_text(img, '像素MV', 8, 7, (40, 26, 30))
big = upscale(img, 6)
Image.fromarray(big).save(os.path.join(ROOT, 'out', '白兰花_标题关键帧_3x4.png'))
Image.fromarray(upscale(img, 2)).save(os.path.join(ROOT, 'out', 'cover_preview.png'))
print(big.shape)
