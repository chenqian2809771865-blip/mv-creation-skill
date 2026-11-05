# -*- coding: utf-8 -*-
"""Chorus 2 + ending: S18-S26"""
import numpy as np, math, functools
from core import *
from fx import rain, splashes, ripples, Glass, Drop, draw_drop, splash_ring
from sprite import place, layer
from chars import HIM, HER, UMB, hat_sprite
from street import render_street, GY, CURB0, CURB1
from skyline import render_sky, special_window, moon, MOON, HER_WIN, HIS_WIN
from cloud import draw_cloud, cloud_rain, warm_drop
from scn_window import his_window
from scn_her import room_bg
from bust import her_bust
from shots_c1 import his_window_cloud, _cloud_drops, to_units, _window_half, desat_keep_yellow


# ---------------- S18 the cloud searches the city ----------------
def S18(t, lt, d):
    z = 1.6
    stop = 106.5
    tm = min(t, stop) - 103.56
    cam_x = 560 + 78 * tm + (8 * ease(seg(t, stop, stop + 0.6)))
    cam_y = 560
    img, T = render_sky(cam_x, cam_y, z, t, 'clear', moon_on=False)
    stepped_glow(img, 80, -60, 260, (170, 186, 255), k=0.12, levels=5)
    cx = 300 + 20 * math.sin(tm * 1.3)
    cy = 120 + 10 * math.sin(tm * 2.0)
    if t > stop:
        # looking around: quick left/right darts
        u = t - stop
        cx = 320 + 34 * math.sin(u * 7.5) * math.exp(-0.2 * u)
        cy = 120 + 4 * math.sin(u * 15)
    x0, x1, yb = draw_cloud(img, cx, cy, 2.0, t=t, mood=0.1)
    cloud_rain(img, t, x0 + 8, x1 - 8, int(yb), H, density=1.6, seed=41, color=(206, 216, 246))
    return img


# ---------------- S19 the cloud comes back: can't find you ----------------
@functools.lru_cache(maxsize=1)
def _s19_drops():
    D = _cloud_drops(108.85, 116.5, 7, rate=7)
    D += [Drop(109.35, 440, 160, 9, slide_at=110.2, speed=22, seed=3), Drop(110.25, 500, 206, 8, slide_at=111.0, speed=20, seed=4)]
    # tears: heavier, sliding drops after 112.0
    for i in range(14):
        tt = 112.0 + i * 0.11
        D.append(Drop(tt, 392 + h01(i, 3) * 150, 118 + h01(i, 4) * 50, 4 + h01(i, 5) * 3, slide_at=tt + 0.2, speed=34 + h01(i, 6) * 20, seed=50 + i, splash=False))
    return D


def S19(t, lt, d):
    mood = ease(seg(t, 112.0, 113.0))
    cx = 450 + (1 - ease_out(seg(t, 108.85, 109.3))) * 260
    hand = None
    if t >= 113.2:
        u = ease_out(seg(t, 113.2, 113.6))
        hand = (13.0 + 3 * u, 46 - 26 * u)
    return his_window_cloud(t, _s19_drops(), cloud=(cx, 72 + mood * 6, 2.8), mood=mood, rain_heavy=1 + 1.6 * mood, hand=hand)


# ---------------- memory vignettes ----------------
def _mem_street(cam_x, z, t, st=None):
    cam_y = GY - 300 / z
    s0 = dict(flower=1, noodle=1, b4=1, shutter=0.0, lantern=1, oldshop=1)
    if st:
        s0.update(st)
    img, info = render_street(cam_x, cam_y, z, 'memory', s0, t=t, reflect_k=0.3)
    return img, info['T']


def vignette(k, t):
    """full-frame memory image (640x360) centred on the subject at screen (320,180)"""
    z = 1.0
    s = 0.82 * z
    hs = s * 0.86
    if k == 0:   # sharing her yellow umbrella, walking
        wx = 300 + 30 * (t - 116)
        img, T = _mem_street(wx - 320 / z, z, t)
        fx, fy = T(wx, GY + 12)
        ph = ((t - 116) / 1.33) % 1
        place(img, *HIM(view='side', s=s, pal='warm', walk=ph, hat=True, rim=(1, 0), rim_col=(255, 200, 140)), fx - 10, fy)
        hspr, hanc = HER(view='side', s=hs, pal='warm', walk=(ph + 0.5) % 1, hand_r=(7.0, 30.0), rim=(1, 0), rim_col=(255, 200, 140), expr='smile')
        place(img, hspr, hanc, fx + 12, fy + 2)
        u, ax, ay = UMB(round(hs * 1.5, 2), 'warm', 1.0)
        blit(img, u, int(fx + 12 + 7 * hs - ax), int(fy + 2 - 70 * hs - ay))
    elif k == 1:  # she hops over a puddle
        wx = 760
        img, T = _mem_street(wx - 320 / z, z, t)
        fx, fy = T(wx, GY + 14)
        pm = m_ellipse(fx, fy + 2, 30, 4)
        img[pm] = img[pm] * 0.6 + np.array([255, 190, 140]) * 0.4
        hop = math.sin(clamp((t - 117.79) / 0.8) * math.pi)
        hspr, hanc = HER(view='side', s=hs, pal='warm', walk=0.0, hand_r=(9.0, 32.0), hand_l=(-8.0, 34.0), rim=(1, 0), rim_col=(255, 200, 140), expr='smile')
        place(img, hspr, hanc, fx - 10 + 20 * clamp((t - 117.79) / 0.8), fy - 22 * hop)
    elif k == 2:  # laughing under the eave
        wx = 1090
        img, T = _mem_street(wx - 320 / z, z, t)
        fx, fy = T(wx, GY + 14)
        place(img, *HIM(view='front', s=s, pal='warm', smile=1, rim=(1, 0), rim_col=(255, 200, 140)), fx - 14, fy)
        place(img, *HER(view='front', s=hs, pal='warm', expr='smile', rim=(1, 0), rim_col=(255, 200, 140)), fx + 14, fy)
    else:  # he lifts his hat toward her
        wx = 560
        img, T = _mem_street(wx - 320 / z, z, t)
        fx, fy = T(wx, GY + 14)
        place(img, *HIM(view='side', s=s, pal='warm', hat=False, hand_r=(10.0, 4.0), rim=(1, 0), rim_col=(255, 200, 140)), fx - 16, fy)
        hsp, hanc = hat_sprite(round(s, 2), 'warm', 'side')
        place(img, hsp, hanc, fx - 16 + 10 * s, fy - 96 * s)
        place(img, *HER(view='side', s=hs, pal='warm', expr='soft', rim=(-1, 0), rim_col=(255, 200, 140)), fx + 16, fy, flip=True)
    rain(img, t, density=0.8, color=(255, 214, 180), slant=0.14, seed=81 + k)
    return img, (fx, fy - 46 * s)


def S20(t, lt, d):
    S = his_window()
    from shots_c1 import _his_glass_base
    S, A = _his_glass_base()
    out = S['clear'].copy()
    g = Glass(S['pane'], A * 0.8, fog_color=S['fog'], soft=S['soft'] * 0.6)
    g.drops = []
    img = g.render(out, S['clear'], t)
    centers = [(140, 148), (262, 212), (382, 140), (500, 206)]
    times = (116.55, 117.79, 118.95, 120.25)
    R = 52
    for i, ((cx, cy), tt) in enumerate(zip(centers, times)):
        circ = m_ellipse(cx, cy, R, R * 1.04)
        if t >= tt - 0.04:
            v, (vx, vy) = vignette(i, t)
            vx, vy = int(round(vx)), int(round(vy))
            vp = np.pad(v, ((80, 80), (80, 80), (0, 0)), mode='edge')
            sub = vp[80 + vy - int(R * 1.04):80 + vy + int(R * 1.04) + 1, 80 + vx - R:80 + vx + R + 1]
            ys, xs = np.nonzero(circ)
            img[ys, xs] = sub[np.clip(ys - int(cy - R * 1.04), 0, sub.shape[0] - 1), np.clip(xs - int(cx - R), 0, sub.shape[1] - 1)]
            if t - tt < 0.3:
                stepped_glow(img, cx, cy, R * 1.8, (255, 214, 150), k=0.5 * (1 - (t - tt) / 0.3), levels=3)
        else:
            draw_drop(img, S['clear'], cx, cy, R)
            continue
        # glassy rim + highlight
        e = outline_of(circ)
        img[e] = (255, 240, 214)
        img[inner_edge(circ, -1, -1, 2)] = img[inner_edge(circ, -1, -1, 2)] * 0.7
        img[inner_edge(circ, 1, 1, 2)] = np.minimum(255, img[inner_edge(circ, 1, 1, 2)] * 0.6 + 100)
        fill(img, m_ellipse(cx - R * 0.45, cy - R * 0.5, 4, 3), (255, 255, 255))
    fr = S['frame']
    a = fr[..., 3:4]
    img = img * (1 - a) + fr[..., :3] * a
    return img


# ---------------- S21 his hat on her head ----------------
def S21(t, lt, d):
    z = 2.4
    wx = 790
    cam_x, cam_y = wx - 320 / z, GY - 336 / z
    img, info = render_street(cam_x, cam_y, z, 'memory', dict(flower=1, noodle=1, b4=1, shutter=0.0, cafe=0), t=t, reflect_k=0.28)
    T = info['T']
    s = 0.82 * z
    hs = s * 0.86
    mx, my = T(wx - 22, GY + 14)
    fx, fy = T(wx + 18, GY + 14)
    # hat path: on his head -> lifted -> over to her head (lands 121.4)
    u = ease(seg(t, 121.0, 121.4))
    hat_his = (mx + 0.5 * s, my - 89.6 * s)
    hat_her = (fx - 0.5 * hs, fy - (100 - 3.6) * hs)
    lift = math.sin(u * math.pi) * 16
    hx = hat_his[0] + (hat_her[0] - hat_his[0]) * u
    hy = hat_his[1] + (hat_her[1] - hat_his[1]) * u - lift
    # his arm reaches the hat brim
    tgt = to_units(hx + 6 * s, hy + 6, mx, my, s)
    if t < 121.0:
        tgt_ = None
        hat_on = True
    elif t < 121.65:
        tgt_ = tgt
        hat_on = False
    else:
        tgt_ = None
        hat_on = False
    place(img, *HIM(view='side', s=s, pal='warm', hat=hat_on, smile=int(t > 121.6), hand_r=tgt_, rim=(1, 0), rim_col=(255, 200, 140)), mx, my)
    expr = 'soft' if t < 121.5 else 'smile'
    lu = 0.0 if t < 121.45 else 0.6
    place(img, *HER(view='side', s=hs, pal='warm', expr=expr, look_up=lu, rim=(-1, 0), rim_col=(255, 200, 140)), fx, fy, flip=True)
    if t >= 121.0:
        hsp, hanc = hat_sprite(round(s, 2), 'warm', 'side')
        hsp = hsp[:, ::-1]
        hanc = (hsp.shape[1] - 1 - hanc[0], hanc[1])
        place(img, hsp, hanc, hx, hy)
    rain(img, t, density=0.9, color=(255, 214, 180), slant=0.14, seed=91)
    splashes(img, t, T(0, GY + 6)[1], H, rate=30, seed=13, color=(255, 220, 190), scale=(1.4, 2.4))
    return img


# ---------------- S22 he lets the cloud go ----------------
def S22(t, lt, d):
    S, A = (None, None)
    from shots_c1 import _his_glass_base
    S, A = _his_glass_base()
    opn = ease(seg(t, 124.95, 125.7))
    out = S['clear'].copy()
    sP = 3.3
    fxP, fyP = 150, 360 + 100 * sP * 0.58
    palm_x, palm_y = fxP + 44 * sP, fyP - (100 - 34) * sP
    if t < 127.38:
        u = ease(seg(t, 125.6, 127.38))
        cx, cy, cs = 470 + (palm_x + 6 - 470) * u, 90 + (palm_y - 34 - 90) * u, 2.6 - 0.9 * u
    elif t < 129.36:
        cx, cy, cs = palm_x + 6, palm_y - 34 + math.sin(t * 3) * 2, 1.7
    else:
        u = ease_in(seg(t, 129.36, 129.98))
        cx, cy, cs = palm_x + 6 + 260 * u, palm_y - 34 - 300 * u, 1.7
    pane = S['pane'].copy()
    sash_x = int(596 - (596 - 330) * opn)
    open_area = m_rect(sash_x, 0, 596, 300) & S['pane']
    g = Glass(pane, A * 0.65 * (~open_area), fog_color=S['fog'], soft=S['soft'] * 0.5)
    img = g.render(out, S['clear'], t)
    img[open_area] = out[open_area]
    fr = S['frame'].copy()
    a = fr[..., 3:4]
    img = img * (1 - a) + fr[..., :3] * a
    # sliding sash frame edge
    if opn > 0:
        img[23:291, sash_x - 5:sash_x] = (74, 52, 50)
        img[23:291, sash_x - 5:sash_x - 4] = (130, 90, 70)
    # foreground: him, arm reaching out
    s = 3.3
    fx, fy = 150, 360 + 100 * s * 0.58
    reach = ease(seg(t, 126.4, 127.3))
    lift = ease(seg(t, 129.2, 129.6))
    hand = None
    if reach > 0:
        hand = (14 + 30 * reach, 46 - 12 * reach - 8 * lift)
    spr, anc = HIM(view='back', s=s, hand_r=hand, rim=(-1, 0), rim_col=(255, 176, 120))
    place(img, spr, anc, fx, fy)
    # the cloud in front of the open window (drawn after him so it sits above his palm)
    x0, x1, yb = draw_cloud(img, cx, cy, cs, t=t)
    cloud_rain(img, t, x0 + 6, x1 - 6, int(yb), int(yb) + 22, density=0.8, seed=51, color=(206, 216, 246))
    return img


# ---------------- S23 across the city to her window ----------------
def _wide(t, z=0.64, cam=(230, 339)):
    img, T = render_sky(cam[0], cam[1], z, t, 'clear', moon_on=False)
    moon(img, 70, 30, 12, glow=0.7)
    special_window(img, T, z, 'his', t)
    special_window(img, T, z, 'her', t)
    return img, T


PATH0 = (HIS_WIN[0] + 10, HIS_WIN[1] - 34)
PATH1 = (HER_WIN[0], HER_WIN[1] - 40)


def _path(u):
    x = PATH0[0] + (PATH1[0] - PATH0[0]) * u
    y = PATH0[1] + (PATH1[1] - PATH0[1]) * u - math.sin(u * math.pi) * 150
    return x, y


def S23(t, lt, d):
    img, T = _wide(t)
    u = ease(seg(t, 130.0, 136.5))
    # trail of warm drops (spawned every 0.25s), four bright pops on the 4 characters
    pops = (133.66, 134.03, 134.38, 135.01)
    k = 0
    tt = 130.2
    while tt < t:
        uu = ease(seg(tt, 130.0, 136.5))
        x, y = _path(uu)
        age = t - tt
        px, py = T(x, y + 18 + min(age, 3) * 6)
        warm_drop(img, px, py, 2.2, glow=0.7 * max(0.3, 1 - age / 4))
        tt += 0.25
    for i, tp in enumerate(pops):
        if t >= tp:
            uu = ease(seg(tp, 130.0, 136.5))
            x, y = _path(uu)
            px, py = T(x, y + 22)
            a = max(0.4, 1 - (t - tp) / 1.2)
            warm_drop(img, px, py, 3.6, glow=1.4 * a)
            if t - tp < 0.2:
                stepped_glow(img, px, py, 30, (255, 236, 180), k=0.9, levels=3)
    x, y = _path(u)
    sx, sy = T(x, y)
    draw_cloud(img, sx, sy, 0.95, t=t)
    return img


# ---------------- S24 her window: a warm drop into her palm ----------------
def _her_window_front(t, palm=0.0, drop_t=None, rain_soft=0.0, expr='calm', look=(0, -0.6)):
    img = new((70, 64, 86))
    for y in range(0, H, 6):
        img[y] = (64, 58, 80)
    for y in range(3, H, 12):
        off = 0 if (y // 12) % 2 else 6
        img[y:y + 3, off::12] = (62, 56, 78)
    sky = [C('#141a34'), C('#18203c'), C('#1d2644'), C('#222c4c')]
    vgrad_bands(img, 0, 44, sky[0], sky[-1], 4)
    img[42:48] = (90, 82, 108)
    X0, Y0, X1, Y1 = 196, 96, 444, 300
    inter = np.zeros((H, W, 3), np.float32)
    warm = np.array([250, 200, 140], np.float32)
    inter[:] = warm
    for i, c in enumerate((1.0, 0.95, 0.9, 0.86, 0.82)):
        inter[:, X0 + i * 50:X0 + (i + 1) * 50] = warm * c
    inter[:, X0:X0 + 40] = (236, 186, 70)
    inter[:, X1 - 40:X1] = (236, 186, 70)
    for k in range(X0 + 4, X0 + 40, 9):
        inter[:, k:k + 2] = (200, 150, 50)
    for k in range(X1 - 36, X1, 9):
        inter[:, k:k + 2] = (200, 150, 50)
    spr, (ax, ay), _ = her_bust(s=3.2, pal='room', look=look, expr=expr, palm_out=palm)
    blit(inter, spr, int(320 - ax), int(160 - ay))
    img[Y0:Y1, X0:X1] = inter[Y0:Y1, X0:X1]
    # window opened outward: both casements swung to the sides
    fr = (200, 194, 206)
    for (a, b_, c_, d_) in ((X0 - 9, Y0 - 9, X1 + 9, Y0), (X0 - 9, Y1, X1 + 9, Y1 + 9), (X0 - 9, Y0, X0, Y1), (X1, Y0, X1 + 9, Y1)):
        img[b_:d_, a:c_] = fr
    img[Y0 - 4:Y1 + 4, X0 - 40:X0 - 9] = (120, 130, 160)
    img[Y0 - 4:Y1 + 4, X0 - 40:X0 - 37] = fr
    img[Y0 - 4:Y1 + 4, X1 + 9:X1 + 40] = (120, 130, 160)
    img[Y0 - 4:Y1 + 4, X1 + 37:X1 + 40] = fr
    img[Y1 + 9:Y1 + 18, X0 - 20:X1 + 20] = (226, 220, 230)
    img[Y1 + 18:Y1 + 21, X0 - 20:X1 + 20] = (120, 112, 130)
    stepped_glow(img, 320, 200, 230, warm, k=0.12, levels=4)
    return img


PALM = (320 + 15.6 * 3.2, 160 + 40.4 * 3.2)


def S24(t, lt, d):
    palm = ease(seg(t, 137.9, 138.5))
    expr = 'calm' if t < 139.51 else 'soft'
    look = (0.2, -0.8) if t < 139.51 else (0.2, 0.6)
    img = _her_window_front(t, palm=palm, expr=expr, look=look)
    x0, x1, yb = draw_cloud(img, PALM[0], 40, 2.2, t=t)
    cloud_rain(img, t, x0 + 8, x1 - 8, int(yb), 290, density=0.6, seed=61, color=(206, 216, 246))
    # the warm drop
    if t < 139.51:
        u = seg(t, 138.75, 139.51)
        if u > 0:
            px, py = PALM[0], yb + (PALM[1] - 4 - yb) * u * u
            warm_drop(img, px, py, 4.0, glow=1.0)
    else:
        u = t - 139.51
        stepped_glow(img, PALM[0], PALM[1], 60 + min(40, u * 40), (255, 200, 120), k=0.7 * max(0.45, 1 - u / 1.5), levels=4)
        warm_drop(img, PALM[0], PALM[1] - 3, 3.0, glow=0.8)
        if u < 0.25:
            splash_ring(img, PALM[0], PALM[1] - 3, 5, u / 0.25, color=(255, 230, 170))
    return img


# ---------------- S25 her close-up ----------------
def S25(t, lt, d):
    img = room_bg().copy()
    # soft rain + the cloud in her window
    win = m_rect(366, 34, 600, 252)
    rain(img, t, layers=('far', 'mid'), density=0.9, color=(190, 200, 236), slant=0.1, seed=71, region=win)
    sub = np.zeros_like(img)
    x0, x1, yb = draw_cloud(img, 540, 74, 1.6, t=t)
    img[m_rect(481, 34, 487, 252)] = C('#e6dccf')
    tear = 0.3 + 0.5 * seg(t, 141.6, 143.0)
    expr = 'soft' if t < 142.0 else 'smile'
    spr, (ax, ay), _ = her_bust(s=4.4, pal='room', look=(0.6, -0.7), expr=expr, tear=tear if expr != 'smile' else 0.0, hand_chest=True)
    blit(img, spr, int(210 - ax), int(118 - ay))
    hx, hy = 210 + 0 * 4.4, 118 + 37 * 4.4
    stepped_glow(img, 210 - 4, 118 + 37.5 * 4.4, 70, (255, 190, 110), k=0.55, levels=4)
    return img


# ---------------- S26 ending ----------------
def S26(t, lt, d):
    img, T = _wide(t, z=0.64, cam=(230, 339))
    x, y = (HIS_WIN[0] + HER_WIN[0]) / 2, 560
    sx, sy = T(x, y)
    x0, x1, yb = draw_cloud(img, sx, sy, 1.1, t=t)
    cloud_rain(img, t, x0 + 6, x1 - 6, int(yb), H, density=0.7, seed=81, color=(206, 216, 246))
    rain(img, t, layers=('far',), density=0.5, color=(190, 196, 230), seed=82)
    if t >= 145.35:
        a = [0.33, 0.66, 1.0][min(2, int((t - 145.35) / 0.12))]
        draw_text(img, '下雨了', 320, 284, (246, 242, 236), outline=(26, 22, 40), shadow=(26, 22, 40), a=a, scale=2, anchor='mm')
        draw_text(img, '薛之谦', 320, 318, (222, 214, 220), outline=(26, 22, 40), a=a, anchor='mm')
    return img
