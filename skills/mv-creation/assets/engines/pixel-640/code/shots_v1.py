# -*- coding: utf-8 -*-
"""Verse 1: S02-S08"""
import numpy as np, math, functools
from core import *
from fx import rain, splashes, ripples, reflect
from sprite import place
from chars import HIM, HER, UMB, pedestrian
from street import render_street, GY, CURB0, CURB1, LAMPS
from skyline import render_sky, special_window, MOON
from cloud import draw_cloud, cloud_rain

L = {l['text']: l for l in TIMING['lyrics']}


# ---------------- S02 sky -> his window ----------------
def S02(t, lt, d):
    z = 1.0
    cam_x = 130
    u = ease(seg(t, 26.52, 29.16))
    cam_y = 470 * u
    # clouds: one slides over the moon on "示例歌词内"
    cover = ease(seg(t, 24.6, 26.15))
    dt = t - 19.8
    clouds = [
        (40 + dt * 7, 300, 1.5, 11),
        (980 - dt * 5, 210, 1.15, 12),
        (720 - 205 * cover, 160, 1.25, 3),               # the moon-hider
        (180 + dt * 4, 86, 1.0, 5),
        (900 + dt * 3, 270, 1.3, 8),
        (330 - dt * 2.5, 345, 1.1, 9),
        (620 + dt * 9, 40, 0.8, 13),
    ]
    img, T = render_sky(cam_x, cam_y, z, t, 'rain', clouds=clouds)
    # dim moonlight once covered
    special_window(img, T, z, 'his', t)
    dens = 0.25 + 0.75 * seg(t, 19.8, 22.9)
    rain(img, t, density=dens, color=(176, 180, 220), slant=0.16, seed=21, oy=cam_y)
    return img


# ---------------- S03 overhead crosswalk ----------------
@functools.lru_cache(maxsize=1)
def _crosswalk_base():
    img = new((34, 36, 52))
    # asphalt speckle (static, sparse)
    rng = np.random.default_rng(2)
    for i in range(900):
        x, y = rng.integers(0, W), rng.integers(0, H)
        img[y, x] = (40, 42, 58)
    # zebra: horizontal bars across the crossing (x 196-444)
    for k in range(0, H + 30, 30):
        img[k:k + 16, 196:444] = (150, 154, 170)
        img[k + 15:k + 16, 196:444] = (110, 114, 130)
    # stop lines / lane dashes
    img[:, 176:180] = (130, 132, 146)
    img[:, 460:464] = (130, 132, 146)
    for y in range(0, H, 40):
        img[y:y + 20, 90:94] = (120, 122, 136)
        img[y:y + 20, 548:552] = (120, 122, 136)
    # manhole
    m = m_ellipse(560, 70, 16, 16)
    img[m] = (44, 46, 60)
    img[outline_of(m)] = (60, 62, 78)
    for k in range(-12, 13, 4):
        img[70 + k, 548:572][m[70 + k, 548:572]] = (52, 54, 70)
    # lamp light pools (stepped, warm) at both edges
    stepped_glow(img, 40, 40, 170, (255, 180, 110), k=0.2, levels=5)
    stepped_glow(img, 610, 320, 180, (255, 180, 110), k=0.2, levels=5)
    # wet sheen on stripes near lights
    return img


def _umb_top(img, x, y, r, col, phase, clear=False):
    """umbrella seen from above: 8 panels alternating shade, tip, edge drops"""
    m = m_ellipse(x, y, r, r)
    yy, xx = np.mgrid[0:H, 0:W]
    ang = (np.arctan2(yy - y, xx - x) + phase) % (2 * math.pi)
    pan = (ang // (math.pi / 4)).astype(int) % 2 == 0
    c = np.asarray(col, np.float32)
    if clear:
        img[m] = img[m] * 0.7 + np.array([200, 210, 230], np.float32) * 0.3
        img[m & pan] = img[m & pan] * 0.9 + 12
    else:
        img[m] = c
        img[m & pan] = c * 0.8
        # light from top-left lamp
        lit = m & ~shift(m, 2, 2)
        img[lit] = np.minimum(255, c * 1.35 + 14)
    img[outline_of(m)] = (20, 20, 30)
    # spokes tips
    for k in range(8):
        a = k * math.pi / 4 - phase
        px, py = int(round(x + (r - 1) * math.cos(a))), int(round(y + (r - 1) * math.sin(a)))
        if 0 <= px < W and 0 <= py < H:
            img[py, px] = (210, 214, 230)
    fill(img, m_ellipse(x, y, 1.6, 1.6), (220, 220, 230))


def S03(t, lt, d):
    img = _crosswalk_base().copy()
    # rain on the ground: ripples everywhere (top-down = round)
    ripples(img, t, m_rect(0, 0, W, H), rate=60, flat=1.0, rmax=6, seed=4, color=(150, 160, 200))
    # walkers: everyone is already crossing at the cut, nobody new arrives -> the crowd thins out
    cols = [(60, 64, 96), (40, 40, 48), (110, 60, 70), (70, 100, 84), (150, 140, 120), (84, 84, 104), (130, 90, 60)]
    n = 24
    for i in range(n):
        dirn = 1 if h01(i, 2) < 0.5 else -1
        sp = 34 + h01(i, 3) * 40
        lane_x = 214 + h01(i, 4) * 212
        y_at0 = 20 + h01(i, 7) * 320
        y = y_at0 + dirn * sp * (t - 30.66) * (1 + 0.25 * (t - 30.66))
        if not (-40 < y < H + 40):
            continue
        x = lane_x + math.sin((t - 30.66) * 2.4 + i) * 1.5
        r = 15 + int(h01(i, 5) * 6)
        ph = (t - 30.66) * 1.6 + h01(i, 6)
        for sgn in (-1, 1):
            fy = y + dirn * (r - 2) + sgn * 3 * math.sin(ph * 2 * math.pi)
            fill(img, m_ellipse(x + sgn * 4, fy, 2.5, 3.5), (24, 22, 30))
        _umb_top(img, x, y, r, cols[i % len(cols)], phase=i * 0.3, clear=(i % 9 == 4))
    return img


# ---------------- S04 street lights go off; he walks out ----------------
def S04(t, lt, d):
    st = dict(flower=int(t < 35.42), noodle=int(t < 36.15), b4=int(t < 37.14), shutter=ease(seg(t, 36.52, 37.14)),
              apt=1)
    img, info = render_street(60, 0, 1.0, 'night', st, t=t)
    T = info['T']
    # pedestrians leaving
    for i, (x0, sp, kind) in enumerate(((260, -38, 0), (430, 34, 1), (520, -30, 2), (150, 30, 3))):
        x = x0 + sp * (t - 35.34)
        sx, sy = T(x, GY + 14 + (i % 2) * 4)
        if -40 < sx < W + 40:
            pedestrian(img, sx, sy, 0.8, (t - 35.34) * 1.2 + i * 0.3, kind=kind, facing=1 if sp > 0 else -1)
    # door opens at 39.83, he steps out
    if t >= 39.6:
        dx, dy = T(70, 198)
        ex, ey = T(110, GY)
        if t >= 39.83:
            img[int(dy):int(ey), int(dx):int(ex)] = (250, 200, 130)
            stepped_glow(img, (dx + ex) / 2, ey - 10, 50, (255, 190, 120), k=0.25, levels=3)
        if t >= 39.95:
            u = ease_out(seg(t, 39.95, 40.6))
            hx, hy = T(90, GY + 6 + 10 * u)
            lu = ease(seg(t, 40.45, 40.95))
            spr, anc = HIM(view='front', s=0.82, look_up=lu, rim=(1, 0), rim_col=(255, 190, 130))
            place(img, spr, anc, hx, hy)
    rain(img, t, density=0.9, color=(176, 184, 220), slant=0.16, seed=31)
    splashes(img, t, GY * 1.0 + 2, CURB0, rate=30, seed=3)
    splashes(img, t, CURB1 + 4, H, rate=40, seed=5, scale=(0.9, 1.6))
    return img


# ---------------- S05 tracking walk ----------------
def S05(t, lt, d):
    z = 1.4
    hxw = 172 + 52 * (t - 41.15)
    cam_x = hxw - 230 / z
    cam_y = GY - 300 / z
    st = dict(flower=0, noodle=0, b4=0, shutter=1.0)
    img, info = render_street(cam_x, cam_y, z, 'night', st, t=t)
    T = info['T']
    sx, sy = T(hxw, GY + 12)
    phase = (t - 41.15) / 1.33
    spr, anc = HIM(view='side', s=0.82 * z, walk=phase % 1.0, rim=(-1, 0), rim_col=(255, 188, 130))
    place(img, spr, anc, sx, sy)
    # rain hitting hat & shoulders
    for k in range(3):
        s_ = math.floor(t * 12) - k
        if h01(s_, 77) < 0.55:
            px = sx + (h01(s_, 3) - 0.3) * 30
            py = sy - 100 * 0.82 * z + 6 + h01(s_, 9) * 4
            a = (0.9, 0.6, 0.3)[k]
            for (ddx, ddy) in ((0, 0), (-1, -1), (1, -1), (-2, -2), (2, -2)):
                X, Y = int(px + ddx * (k + 1)), int(py + ddy)
                if 0 <= X < W and 0 <= Y < H:
                    img[Y, X] = img[Y, X] * (1 - a) + np.array([210, 220, 245]) * a
    rain(img, t, density=1.0, color=(176, 184, 220), slant=0.16, seed=41, ox=cam_x * z)
    gy0 = T(0, GY)[1]
    splashes(img, t, gy0 + 2, T(0, CURB0)[1], rate=36, seed=6)
    splashes(img, t, T(0, CURB1)[1] + 4, H, rate=44, seed=7, scale=(1.0, 1.8))
    return img


# ---------------- S06 cafe window: reflection walks with her ----------------
def S06(t, lt, d):
    from sprite import layer
    z = 2.0
    cam_x, cam_y = 648, GY - 330 / z
    st = dict(flower=0, noodle=0, b4=0, shutter=1.0)
    img, info = render_street(cam_x, cam_y, z, 'night', st, t=t, reflect_k=0.32)
    T = info['T']
    stop_t = 48.56
    tw = min(t, stop_t)
    hxw = 708 + 26 * (tw - 45.83)
    sx, sy = T(hxw, GY + 16)
    s = 0.82 * z
    walking = t < stop_t
    phase = ((tw - 45.83) / 1.33) % 1.0
    gx0, gy0 = T(712, 176); gx1, gy1 = T(888, 256)
    glass = m_rect(int(gx0), int(gy0), int(gx1), int(gy1))
    # reflections (inside the glass only): him + her with the yellow umbrella (memory)
    off = (10, -16)
    her_a = 1.0 if t < 49.45 else [0.66, 0.33, 0.0][min(2, int((t - 49.45) / 0.3))]
    rgb, msk = None, None
    rgb, msk = layer(*HIM(view='side', s=s, walk=phase if walking else None, rim=None), sx + off[0], sy + off[1])
    k_ = 0.45
    sel = msk & glass
    img[sel] = img[sel] * (1 - k_) + (rgb[sel] * 0.8 + np.array([24, 28, 46]) * 0.2) * k_
    if her_a > 0:
        hs = s * 0.86
        hsx, hsy = T(hxw + 21, GY + 10)
        hspr, hanc = HER(view='side', s=hs, pal='warm', walk=phase if walking else None, hand_r=(7.0, 38.0), rim=None)
        rgb2, m2 = layer(hspr, hanc, hsx + off[0], hsy + off[1])
        u, ux, uy = UMB(round(hs * 1.3, 2), 'warm', 1.0)
        hx_, hy_ = hsx + off[0] + 7.0 * hs, hsy + off[1] - (100 - 38.0) * hs
        rgb2, m2 = layer(u, (ux, uy), hx_, hy_ + 2 * hs, out=rgb2, mask=m2)
        kk = 0.42 * her_a
        sel = m2 & glass
        img[sel] = img[sel] * (1 - kk) + rgb2[sel] * kk
    if t > 49.2:
        spr, anc = HIM(view='front', s=s, head_turn=1.0, rim=(1, 0), rim_col=(255, 186, 130))
    else:
        spr, anc = HIM(view='side', s=s, walk=phase if walking else None, rim=(-1, 0), rim_col=(255, 186, 130))
    place(img, spr, anc, sx, sy)
    rain(img, t, density=0.9, color=(176, 184, 220), slant=0.16, seed=51)
    splashes(img, t, T(0, GY)[1] + 3, T(0, CURB0)[1], rate=30, seed=8, scale=(1.2, 2.0))
    return img


# ---------------- S07 under the eave: rain stops on 停 ----------------
def S07(t, lt, d):
    z = 2.2
    cam_x, cam_y = 932, GY - 330 / z
    st = dict(flower=0, noodle=0, b4=0, shutter=1.0, lantern=1)
    img, info = render_street(cam_x, cam_y, z, 'night', st, t=t, reflect_k=0.3)
    T = info['T']
    stop = ease(seg(t, 53.72, 54.35))
    # him under the eave, front, looking out
    sx, sy = T(1124, GY + 14)
    lu = 0.0 if t < 53.77 else ease(seg(t, 53.77, 54.4)) * 0.8
    spr, anc = HIM(view='front', s=0.82 * z, look_up=lu, rim=(1, 0), rim_col=(255, 150, 110))
    place(img, spr, anc, sx, sy)
    # eave drips: from tile ends every 8 world px, fall to ground
    ex0, ey = T(944, 176)
    gy = T(0, GY + 10)[1]
    for k in range(30):
        wx = 948 + k * 8
        px, _ = T(wx, 0)
        if not (0 <= px < W):
            continue
        per = 0.9 + h01(k, 3) * 0.8 + stop * 2.5
        ph = (t + h01(k, 5) * per) % per
        if t > 54.9 and h01(k, 8) > 0.15:
            continue
        fall = ph / 0.42
        if fall < 1:
            yy = ey + (gy - ey) * fall * fall
            for q in range(3):
                Y = int(yy) - q * 2
                if 0 <= Y < H:
                    img[Y, int(px)] = img[Y, int(px)] * 0.3 + np.array([210, 222, 250]) * 0.7
        elif fall < 1.3:
            for ddx in (-2, -1, 1, 2):
                X, Y = int(px + ddx), int(gy - (1 if abs(ddx) == 1 else 2))
                if 0 <= X < W and 0 <= Y < H:
                    img[Y, X] = img[Y, X] * 0.4 + np.array([210, 222, 250]) * 0.6
    if stop < 1:
        rain(img, t, density=1.0 * (1 - stop), color=(176, 184, 220), slant=0.16, seed=61, stop_at=None)
        splashes(img, t, gy - 6, H, rate=int(40 * (1 - stop)) + 1, seed=9, scale=(1.4, 2.2))
    return img


# ---------------- S08 moon street: he steps out; the little cloud arrives ----------------
def S08(t, lt, d):
    z = 1.0
    cam_x, cam_y = 860, 0
    st = dict(flower=0, noodle=0, b4=0, shutter=1.0, lantern=1, signal='green' if t > 57.38 else 'red')
    img, info = render_street(cam_x, cam_y, z, 'moon', st, t=t, reflect_k=0.34)
    T = info['T']
    # moon in the gap of sky above the old shop + clouds parting
    part = ease(seg(t, 55.2, 57.6))
    mx, my = 250, 34
    from skyline import moon, night_cloud
    moon(img, mx, my, 11, glow=0.4 + 0.6 * part)
    night_cloud(img, 250 - 70 - 160 * part, 30, 0.7, seed=2, col=(40, 48, 84), rim=(120, 140, 200))
    night_cloud(img, 250 + 80 + 170 * part, 40, 0.65, seed=6, col=(40, 48, 84), rim=(120, 140, 200))
    # puddle with the moon
    pm = m_ellipse(*T(1180, 276), 34, 4)
    img[pm] = img[pm] * 0.55 + np.array([60, 80, 130]) * 0.45
    mmx, mmy = T(1178, 276)
    fill(img, m_ellipse(mmx - 6, mmy, 4, 1.5) & pm, (230, 232, 220))
    # him: under the eave until 55.84, walks out to 1150, stops, looks up 57.38
    if t < 55.84:
        hx = 1080
        spr, anc = HIM(view='front', s=0.82, rim=(1, 0), rim_col=(200, 214, 255))
    elif t < 57.0:
        u = (t - 55.84) / (57.0 - 55.84)
        hx = 1080 + 120 * u
        spr, anc = HIM(view='side', s=0.82, walk=((t - 55.84) / 1.33) % 1, rim=(1, 0), rim_col=(200, 214, 255))
    else:
        hx = 1200
        lu = ease(seg(t, 57.3, 57.8))
        spr, anc = HIM(view='front', s=0.82, look_up=lu, rim=(1, 0), rim_col=(200, 214, 255))
    sx, sy = T(hx, GY + 16)
    place(img, spr, anc, sx, sy)
    # the little cloud drifts down
    if t >= 58.7:
        u = ease(seg(t, 59.03, 60.32))
        cy = -30 + (sy - 82 * 1.0 - 34 + 30) * u
        cx = sx + 40 * (1 - u)
        draw_cloud(img, cx, cy, 0.85, t=t)
    # last drips from eave
    ex, ey = T(1000, 176)
    for k in range(4):
        per = 2.2 + k * 0.7
        ph = (t + k * 0.9) % per
        if ph < 0.4:
            px = T(960 + k * 56, 0)[0]
            yy = ey + (T(0, GY)[1] - ey) * (ph / 0.4) ** 2
            if 0 <= px < W:
                img[int(yy):int(yy) + 2, int(px)] = (200, 214, 250)
    return img
