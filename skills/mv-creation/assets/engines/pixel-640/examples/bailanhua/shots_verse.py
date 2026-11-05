# -*- coding: utf-8 -*-
"""S06–S09：手机呼叫→弄堂“此房出租”→示例歌词→近景泪（全停定格）。"""
import numpy as np, math
from core import *
from sprite import place
from chibi import HIM, HER, blink, unit_px
from props import umbrella, orchid_pair, shape
from scn_lane import render_lane, HER_X, ARCH_X
from fx import rain, splashes, draw_drop
from shots_intro import _bokeh_bg, SPC

BEATS = TIMING['beats']


def beat_pulse(t, width=0.18):
    """1 at each beat, decaying"""
    best = 9
    for b in BEATS:
        if b <= t:
            best = min(best, t - b)
    return max(0.0, 1 - best / width) if best < width else 0.0


# ---------------- S06 phone ----------------
_AV = {}


def _avatar(r):
    if r in _AV:
        return _AV[r]
    spr, anc = HER(view='front', s=r / 22.0, light='day', style='memory', mouth='smile', dimple=True, rim=None)
    _AV[r] = (spr, anc)
    return _AV[r]


def S06(t, lt, d):
    img = _bokeh_bg('s06', [(80, 80, 80, (255, 190, 110), 0.3), (560, 70, 100, (255, 120, 190), 0.22), (520, 300, 70, (120, 200, 255), 0.2),
                            (120, 300, 60, (255, 210, 140), 0.25)])
    # the phone alone (no hand), centred, a little taller than before
    px0, py0, pw, ph = 226, 8, 188, 306
    body = m_rect(px0, py0, px0 + pw, py0 + ph)
    for (cx_, cy_) in ((px0, py0), (px0 + pw - 4, py0), (px0, py0 + ph - 4), (px0 + pw - 4, py0 + ph - 4)):
        body &= ~m_rect(cx_, cy_, cx_ + 4, cy_ + 4)
    img[m_rect(px0 + 6, py0 + 8, px0 + pw + 6, py0 + ph + 8)] *= 0.55
    shape(img, body, (22, 22, 30), outline=(8, 8, 12))
    img[m_rect(px0 + pw // 2 - 14, py0 + 4, px0 + pw // 2 + 14, py0 + 7)] = (46, 46, 58)      # speaker slot
    img[m_rect(px0 + pw, py0 + 70, px0 + pw + 2, py0 + 100)] = (40, 40, 52)                    # side button
    sx0, sy0, sx1, sy1 = px0 + 7, py0 + 12, px0 + pw - 7, py0 + ph - 12
    off = t >= 20.11
    scr = m_rect(sx0, sy0, sx1, sy1)
    vgrad_bands(img, sy0, sy1, C('#2b3a5c') if not off else C('#2e2e38'), C('#6a5a86') if not off else C('#4a4a54'), 6, sx0, sx1)
    draw_text(img, '00:01', sx0 + 6, sy0 + 3, (230, 230, 240))
    draw_text(img, '▮▮▮', sx1 - 30, sy0 + 3, (230, 230, 240))
    cx, cy, r = (sx0 + sx1) // 2, sy0 + 78, 36
    # pulse rings each beat
    if not off:
        for b in BEATS:
            if 0 <= t - b < 0.6:
                u = (t - b) / 0.6
                ring = m_ellipse(cx, cy, r + 4 + 26 * u, r + 4 + 26 * u) & ~m_ellipse(cx, cy, r + 2 + 26 * u, r + 2 + 26 * u) & scr
                img[ring] = img[ring] * (0.4 + 0.6 * u) + np.array([200, 220, 255], np.float32) * (0.6 - 0.6 * u)
    disc = m_ellipse(cx, cy, r, r)
    img[outline_of(disc)] = (240, 240, 248)
    img[disc] = (250, 214, 222)
    spr, anc = _avatar(r)
    tmp = img.copy()
    place(tmp, spr, anc, cx, cy + r * 3.3)
    if off:
        g = tmp[disc].mean(1, keepdims=True)
        tmp[disc] = tmp[disc] * 0.35 + g * 0.65 * 0.85
    img[disc] = tmp[disc]
    draw_text(img, '她', cx, cy + r + 10, (250, 250, 255), scale=2, anchor='mt')
    if not off:
        nd = int((t - 19.46) / 0.316) % 4
        draw_text(img, '正在呼叫' + '.' * nd, cx - 34, cy + r + 50, (220, 226, 246))
    else:
        draw_text(img, '通话结束', cx, cy + r + 50, (200, 200, 210), anchor='mt')
    # hang up button
    hb = m_ellipse(cx, sy1 - 34, 18, 18)
    img[hb] = (230, 70, 70) if not off else (120, 70, 70)
    img[m_rect(cx - 9, sy1 - 36, cx + 9, sy1 - 32)] = (250, 250, 250)
    # banner 对方已关机
    if off:
        u = min(1.0, (t - 20.11) / (2.0 / FPS))
        bw, bh = int(150 * (0.85 + 0.15 * u)), 34
        bx0, by0 = cx - bw // 2, cy + r + 72
        bn = m_rect(bx0, by0, bx0 + bw, by0 + bh)
        shape(img, bn, (40, 40, 48), outline=(200, 60, 70))
        draw_text(img, '对方已关机', cx, by0 + 9, (255, 120, 120), anchor='mt')
    # raindrops on the glass
    through = img.copy()
    for i in range(14):
        if h01(i, 4) < clamp((t - 19.46) / 1.2 + 0.4):
            x = sx0 + 6 + h01(i, 1) * (sx1 - sx0 - 12)
            y = sy0 + 10 + h01(i, 2) * (sy1 - sy0 - 20)
            draw_drop(img, through, x, y, 1.5 + 2.5 * h01(i, 3))
    rain(img, t, layers=('near',), density=0.6)
    return img


# ---------------- S07 lane: her dark window + 此房出租 ----------------
def S07(t, lt, d):
    z = 1.6
    cam_x, cam_y = HER_X - 200, 77
    flap = 0.0
    for b in BEATS:
        if 0 <= t - b < 0.3:
            flap = max(flap, (1 - (t - b) / 0.3) * (0.7 if int(b / 0.947) % 2 else 0.35))
    img, info = render_lane(cam_x, cam_y, z, t, state=dict(her_win=0, wins=0.4), sign_flap=flap)
    T = info['T']
    s = SPC * z
    # he runs in from the left, stops at 21.70, looks up at 21.9
    if t < 21.06:
        x = 60
    else:
        x = 150 + (262 - 150) * ease_out(seg(t, 21.06, 21.70))
    sx, sy = T(x, 272)
    if t < 21.70:
        spr, anc = HIM(view='side', s=s, light='night', walk=(t * 3.2) % 1, mouth='o', rim=(-1, 0))
    else:
        lu = ease(seg(t, 21.85, 22.2))
        spr, anc = HIM(view='side', s=s, light='night', look_up=lu * 1.0, mouth='o' if t < 22.5 else 'sad', rim=(-1, 0),
                       eyes='wide' if t < 22.5 else 'open')
    if t >= 21.06:
        place(img, spr, anc, sx, sy)
    rain(img, t, density=1.1)
    splashes(img, t, int(T(0, 264)[1]), H - 40, rate=40)
    return img


# ---------------- S08 walk away, glance back, silhouette under the arch ----------------
def S08(t, lt, d):
    z = 1.25
    cam_x, cam_y = 330, 22.4
    img, info = render_lane(cam_x, cam_y, z, t, state=dict(her_win=0, wins=0.4), sign=False)
    T = info['T']
    s = SPC * z
    # silhouette under the arch lamp (far: smaller, bluish) visible 24.6–25.56
    lamp_flick = 25.56 <= t < 25.56 + 2.0 / FPS
    if 24.3 <= t < 25.56:
        ss = s * 0.86
        spr, anc = HER(view='back', s=ss, light='lamp', style='now', rim=None)
        ax, ay = T(ARCH_X + 30, 258)
        a = 0.9 if t >= 24.45 else 0.9 * (t - 24.3) / 0.15
        place(img, spr, anc, ax, ay, a=a)
        umbrella(img, ax + 3, ay - 58 * ss, ss * 1.2, (40, 40, 52), 'lamp', a)
    if lamp_flick:
        lx, ly = T(ARCH_X + 39, 140)
        img[m_ellipse(lx, ly, 46, 30)] *= 0.5
    # him walking left, slow; glance back at 24.84
    x = 560 - 26 * (t - 23.25)
    sx, sy = T(x, 272)
    if t < 24.84:
        spr, anc = HIM(view='side', s=s, light='night', walk=(t * 1.4) % 1, mouth='sad', eyes='down', rim=(1, 0))
        place(img, spr, anc, sx, sy, flip=True)
    else:
        stop = t >= 24.95
        spr, anc = HIM(view='side', s=s, light='night', walk=None if stop else (t * 1.4) % 1, head_back=True,
                       mouth='o' if t < 25.7 else 'sad', eyes='wide' if t < 25.7 else 'open', rim=(1, 0))
        place(img, spr, anc, sx, sy, flip=True)
    dens = 0.8 + 0.9 * ease(seg(t, 23.25, 23.6))
    rain(img, t, density=dens)
    splashes(img, t, int(T(0, 264)[1]), H - 30, rate=60)
    return img


# ---------------- S09 bust close-up, tear, freeze ----------------
def S09(t, lt, d):
    img = _bokeh_bg('s09', [(70, 120, 90, (255, 190, 110), 0.28), (590, 90, 110, (255, 110, 190), 0.3), (540, 300, 80, (120, 200, 255), 0.2),
                            (180, 30, 60, (255, 220, 160), 0.2), (420, 200, 40, (255, 200, 140), 0.18)])
    frozen = t >= 30.70
    tt = min(t, 30.70)
    s = round(3.48 + 0.30 * ease(seg(tt, 26.38, 30.70)), 2)     # slow push-in, frozen with the rain
    tear = 0.0
    if tt >= 29.46:
        tear = min(1.0, (tt - 29.46) / 1.0)
    lu = 0.35 * ease(seg(tt, 28.4, 28.9))
    eyes = 'closed' if (blink(tt, 1.1) and tt < 29.3) else ('sad' if tt < 28.4 else 'open')
    spr, anc = HIM(view='front', s=s, light='nightpink', mouth='sad', eyes=eyes, look_up=lu, tear=tear, rim=(1, 0))
    fx, fy = 320, int(round(158 + 69 * s))
    # tiny breathing bob (integer)
    if not frozen:
        fy += int(round(math.sin(t * 2.2) * 1))
    place(img, spr, anc, fx, fy)
    # tear glint + falling drop in the freeze
    ex, ey = unit_px(anc, s, fx, fy, -7.2, 34.5 - lu * 1.4)
    if 29.46 <= t < 30.70:
        gy = ey + 3.5 * s + tear * 7 * s
        img[m_ellipse(ex - 1, gy - 2, 1, 1)] = (255, 255, 255)
    if frozen:
        u = clamp((t - 30.70) / 0.72)
        y0 = ey + 10.5 * s
        y = y0 + (H + 20 - y0) * (u ** 2.2)
        x = ex - 2 + 18 * u
        img[m_ellipse(x, y, 3, 4.6)] = (206, 232, 255)
        img[m_ellipse(x - 1, y - 2, 1, 1)] = (255, 255, 255)
        # cold, still
        img[:] = img * np.array([0.86, 0.92, 1.04], np.float32) + np.array([0, 4, 10], np.float32)
    rain(img, t, layers=('mid', 'near'), density=0.9, stop_at=30.70 if frozen else None)
    return img
