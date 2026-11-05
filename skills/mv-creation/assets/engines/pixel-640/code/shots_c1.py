# -*- coding: utf-8 -*-
"""Chorus 1: S09-S17"""
import numpy as np, math, functools
from core import *
from fx import rain, splashes, ripples, Glass, Drop, draw_drop, splash_ring
from sprite import place, layer
from chars import HIM, HER, UMB
from street import render_street, GY, CURB0, CURB1
from skyline import render_sky, special_window, moon, MOON, HER_WIN
from cloud import draw_cloud, cloud_rain, warm_drop
from scn_window import his_window
from scn_her import room_bg, desk_bg
from bust import her_bust


def to_units(sx, sy, fx, fy, s):
    """screen point -> character units given feet (fx,fy) and scale s"""
    return ((sx - fx) / s, 100 - (fy - sy) / s)


# ---------------- S09 only his cloud rains ----------------
def S09(t, lt, d):
    z = 2.2
    cam_x, cam_y = 1200 - 320 / z, GY - 330 / z
    st = dict(flower=0, noodle=0, b4=0, shutter=1.0, lantern=1, signal='green')
    img, info = render_street(cam_x, cam_y, z, 'moon', st, t=t, reflect_k=0.3)
    T = info['T']
    sx, sy = T(1200, GY + 14)
    s = 0.82 * z
    lu = 0.25 * ease(seg(t, 61.0, 61.6)) + 0.65 * ease(seg(t, 62.3, 63.1))
    spr, anc = HIM(view='front', s=s, look_up=lu, rim=(1, 0), rim_col=(200, 214, 255))
    place(img, spr, anc, sx, sy)
    hat_top = sy - 100 * s
    cx, cy = sx + 4, hat_top - 52
    rain_on = t >= 60.96
    if rain_on:
        x0, x1, yb = draw_cloud(img, cx, cy, 1.9, t=t, mood=0.2, tint=(0.84, 0.88, 0.96))
        cloud_rain(img, t, x0 + 8, x1 - 8, int(yb), H, density=4.0, seed=9, color=(214, 224, 250), length=10)
        # splashes on the brim + shoulders
        brim_y = hat_top + 10.5 * s
        for k in range(3):
            s_ = math.floor(t * 12) - k
            for j in range(2):
                if h01(s_, j, 5) < 0.7:
                    px = sx + (h01(s_, j, 8) - 0.5) * 30 * s
                    py = brim_y - 1 if abs(px - sx) < 17 * s else sy - 74 * s
                    a = (0.9, 0.6, 0.3)[k]
                    for (dx_, dy_) in ((0, 0), (-1, -1), (1, -1), (-2, -2), (2, -2)):
                        X, Y = int(px + dx_ * (k + 1)), int(py + dy_ * (1 + k))
                        if 0 <= X < W and 0 <= Y < H:
                            img[Y, X] = img[Y, X] * (1 - a) + np.array([220, 230, 255]) * a
        # four big bounces on 64.18 64.32 64.82 65.28
        for i, tt in enumerate((64.18, 64.32, 64.82, 65.28)):
            u = (t - tt) / 0.35
            if 0 <= u < 1:
                px = sx + (-14 + i * 9) * s * 0.9
                py = brim_y - 2 - math.sin(u * math.pi) * 18
                splash_ring(img, px, brim_y - 1, 3.0, min(1, u * 1.6))
                fill(img, m_ellipse(px + u * 6 * (1 if i % 2 else -1), py, 2.2, 2.6), (230, 238, 255))
    else:
        # cloud waiting (from S08)
        draw_cloud(img, cx, cy, 1.9, t=t)
    return img


# ---------------- his window with the cloud outside ----------------
@functools.lru_cache(maxsize=1)
def _his_glass_base():
    from shot_intro import setup
    S = his_window()
    _, _, wr, _ = setup()
    m_title, _, _ = wr.state(12.95)
    A = S['A'].copy()
    A[m_title] *= 0.42
    return S, A


def his_window_cloud(t, drops, cloud=(450, 70, 2.8), mood=0.0, fog_k=0.65, rain_heavy=1.0, foreground=True, look_up=0.0,
                     hand=None, cloud_t=None, open_=0.0, palm=None):
    S, A = _his_glass_base()
    out = S['clear'].copy()
    cx, cy, cs = cloud
    if cs > 0:
        x0, x1, yb = draw_cloud(out, cx, cy, cs, t=t if cloud_t is None else cloud_t, mood=mood)
        cloud_rain(out, t, x0 + 8, x1 - 8, int(yb), S['sill_y'], density=1.2 * rain_heavy, seed=12, color=(200, 210, 240))
    g = Glass(S['pane'], A * fog_k, fog_color=S['fog'], soft=S['soft'] * 0.6)
    g.drops = drops
    img = g.render(out, S['clear'], t)
    fr = S['frame']
    a = fr[..., 3:4]
    img = img * (1 - a) + fr[..., :3] * a
    if foreground:
        s = 3.3
        spr, anc = HIM(view='back', s=s, look_up=look_up, hand_r=hand, rim=(-1, 0), rim_col=(255, 176, 120))
        place(img, spr, anc, 150, 360 + 100 * s * 0.58)
    return img


def _cloud_drops(t0, t1, seed, region=(380, 540, 100, 260), rate=7):
    """small drops hitting the glass under the cloud"""
    D = []
    n = int((t1 - t0) * rate)
    for i in range(n):
        tt = t0 + (i + h01(i, seed)) / rate
        x = region[0] + h01(i, seed, 1) * (region[1] - region[0])
        y = region[2] + h01(i, seed, 2) * (region[3] - region[2])
        r = 1.6 + h01(i, seed, 3) * 2.2
        sl = tt + 0.8 + h01(i, seed, 4) * 1.5 if h01(i, seed, 5) < 0.4 else None
        D.append(Drop(tt, x, y, r, slide_at=sl, speed=30, seed=i + seed, splash=r > 2.6, beads=False))
    return D


@functools.lru_cache(maxsize=1)
def _s10_drops():
    big = [Drop(66.6, 430, 150, 9, slide_at=67.8, speed=24, seed=1), Drop(67.41, 488, 196, 8, slide_at=68.6, speed=20, seed=2)]
    for i, tt in enumerate((69.65, 70.02, 70.32, 70.95)):
        big.append(Drop(tt, 312 + i * 62, 236 - i * 16, 6 + i * 0.8, seed=10 + i, slide_at=tt + 1.4 + i * 0.3, speed=22))
    return _cloud_drops(66.0, 73.8, 3) + big


def S10(t, lt, d):
    return his_window_cloud(t, _s10_drops())


# ---------------- memory under the eave ----------------
def _memory_eave(t, phase):
    z = 2.2
    cam_x, cam_y = 932, GY - 330 / z
    st = dict(flower=0, noodle=0, b4=0, shutter=1.0, lantern=1, oldshop=1)
    img, info = render_street(cam_x, cam_y, z, 'memory', st, t=t, reflect_k=0.3)
    T = info['T']
    s = 0.82 * z
    hs = s * 0.86
    mx, my = T(1080, GY + 14)
    fx, fy = T(1116, GY + 12)
    him_spr = HIM(view='front', s=s, pal='warm', rim=(1, 0), rim_col=(255, 200, 140))
    if phase == 'hold':
        # her hand on his sleeve until 77.93
        rel = ease(seg(t, 77.93, 78.15))
        tx, ty = mx + 13.4 * s, my - (100 - 58) * s
        ux, uy = to_units(tx, ty, fx, fy, hs)
        dux, duy = -11.0, 54
        hl = (ux + (dux - ux) * rel, uy + (duy - uy) * rel)
        place(img, *him_spr, mx, my)
        hspr, hanc = HER(view='front', s=hs, pal='warm', hand_l=hl, rim=(1, 0), rim_col=(255, 200, 140), expr='calm')
        place(img, hspr, hanc, fx, fy)
        # closed umbrella in her right hand
        u, ax, ay = UMB(round(hs * 1.1, 2), 'warm', 0.0)
        hx, hy = fx + 11.0 * hs, fy - (100 - 55.5) * hs
        blit(img, u, int(round(hx - ax)), int(round(hy - ay + 6 * hs)))
    else:
        place(img, *him_spr, mx, my)
        if t < 78.9:
            op = ease(seg(t, 78.34, 78.6))
            hspr, hanc = HER(view='front', s=hs, pal='warm', hand_r=(8.0, 26.0 + 20 * (1 - op)), rim=(1, 0), rim_col=(255, 200, 140), expr='sad')
            place(img, hspr, hanc, fx, fy)
            u, ax, ay = UMB(round(hs * 1.3, 2), 'warm', round(op, 2))
            hx, hy = fx + 8.0 * hs, fy - (100 - 26.0 - 20 * (1 - op)) * hs
            blit(img, u, int(round(hx - ax)), int(round(hy - ay)))
        else:
            wx = 1116 + 44 * (t - 78.9)
            fx, fy = T(wx, GY + 12)
            hspr, hanc = HER(view='side', s=hs, pal='warm', walk=((t - 78.9) / 1.2) % 1, hand_r=(7.0, 30.0), rim=(-1, 0), rim_col=(255, 200, 140))
            place(img, hspr, hanc, fx, fy)
            u, ax, ay = UMB(round(hs * 1.3, 2), 'warm', 1.0)
            hx, hy = fx + 7.0 * hs, fy - (100 - 30.0) * hs
            blit(img, u, int(round(hx - ax)), int(round(hy - ay + 2 * hs)))
    rain(img, t, density=1.0, color=(255, 214, 180), slant=0.14, seed=71)
    splashes(img, t, T(0, GY + 6)[1], H, rate=36, seed=10, color=(255, 220, 190), scale=(1.4, 2.2))
    return img


def desat_keep_yellow(img, k):
    if k <= 0:
        return img
    r, g, b_ = img[..., 0], img[..., 1], img[..., 2]
    yellow = (r > 150) & (g > 110) & (b_ < g * 0.62) & (r - b_ > 90)
    lum = (0.3 * r + 0.59 * g + 0.11 * b_)[..., None]
    grey = lum * np.array([0.92, 0.95, 1.05]) * 0.85
    out = img * (1 - k) + grey * k
    out[yellow] = img[yellow]
    return out


def S11(t, lt, d):
    mem = _memory_eave(t, 'hold')
    if t < 74.36:
        base = his_window_cloud(t, _s10_drops())
        u = ease_in(seg(t, 73.80, 74.36))
        cx, cy = 430, 176
        r = 14 + u * 420
        circ = m_ellipse(cx, cy, r, r)
        base[circ] = mem[circ]
        e = outline_of(circ)
        base[e] = (255, 236, 200)
        e2 = outline_of(circ | e)
        base[e2] = base[e2] * 0.5 + np.array([255, 220, 170]) * 0.5
        if u < 0.2:
            hi = m_ellipse(cx - r * 0.4, cy - r * 0.45, max(1, r * 0.12), max(1, r * 0.12))
            base[hi] = (255, 255, 255)
        return base
    return mem


def S12(t, lt, d):
    img = _memory_eave(t, 'go')
    k = [0, 0.35, 0.65, 0.88][min(3, int(seg(t, 80.0, 82.0) * 3 + 1e-6) + (1 if t >= 80.0 else 0))]
    return desat_keep_yellow(img, k)


# ---------------- S13 split screen ----------------
def _facade(w, h, base, seed):
    img = new(base, w, h)
    for y in range(0, h, 6):
        img[y] = np.asarray(base) * 0.92
    rng = np.random.default_rng(seed)
    for y in range(3, h, 12):
        off = 0 if (y // 12) % 2 else 6
        for x in range(off, w, 12):
            img[y:y + 3, x] = np.asarray(base) * 0.9
    return img


def _window_half(t, which):
    w = 320
    if which == 'his':
        img = _facade(w, H, (56, 60, 84), 1)
    else:
        img = _facade(w, H, (70, 64, 86), 2)
    X0, Y0, X1, Y1 = 66, 92, 254, 300
    # sky strip at top
    sky = [C('#141a34'), C('#18203c'), C('#1d2644'), C('#222c4c')]
    vgrad_bands(img, 0, 60, sky[0], sky[-1], 4)
    img[56:62] = (40, 42, 62)
    # interior
    inter = np.zeros((H, w, 3), np.float32)
    warm = np.array([238, 176, 110] if which == 'his' else [250, 200, 140], np.float32)
    inter[:] = warm
    for i, c in enumerate((1.0, 0.94, 0.88, 0.82)):
        inter[:, X0 + i * 47:X0 + (i + 1) * 47] = warm * c
    if which == 'his':
        inter[:, X0:X0 + 40] = warm * 0.7
        s = 1.7
        hand = None
        if t >= 84.86:
            hand = (11.0, 18.0)
        spr, anc = HIM(view='front', s=s, hand_r=hand, rim=(1, 0), rim_col=(200, 214, 255))
        place(inter, spr, anc, 168, Y1 + 100 * s * 0.42)
        if hand is not None:
            hx, hy = 168 + 11.0 * s, Y1 + 100 * s * 0.42 - (100 - 18.0) * s - 1.2 * s
            fill(inter, m_ellipse(hx, hy, 3.4 * s * 0.8, 4 * s * 0.8, w, H), (232, 196, 178))
    else:
        inter[:, X0:X0 + 34] = (236, 186, 70)
        inter[:, X1 - 34:X1] = (236, 186, 70)
        for k in range(X0 + 4, X0 + 34, 9):
            inter[:, k:k + 2] = (200, 150, 50)
        for k in range(X1 - 30, X1, 9):
            inter[:, k:k + 2] = (200, 150, 50)
        look = (0.0, 1.0)
        blink = 0.55
        if 86.65 <= t < 87.25:
            look, blink = (0.2, -0.8), 0.0
        spr, (ax, ay), _ = her_bust(s=2.3, pal='room', look=look, blink=blink, expr='calm')
        blit(inter, spr, int(160 - ax), int(186 - ay))
        # desk + book + lamp
        inter[262:Y1] = (150, 100, 72)
        inter[262:264] = (184, 130, 96)
        bk = m_poly([(120, 266), (200, 266), (206, 284), (114, 284)], w, H)
        inter[bk] = (242, 234, 220)
        inter[m_line([(160, 266), (160, 284)], 1, w, H)] = (200, 190, 176)
        stepped_glow(inter, 230, 250, 70, (255, 214, 150), k=0.3, levels=3)
    img[Y0:Y1, X0:X1] = inter[Y0:Y1, X0:X1]
    # glass sheen
    for k in range(2):
        sh = m_poly([(X0 + 20 + k * 70, Y0), (X0 + 44 + k * 70, Y0), (X0 + 4 + k * 70, Y1), (X0 - 20 + k * 70, Y1)], w, H) & m_rect(X0, Y0, X1, Y1, w, H)
        img[sh] = np.minimum(255, img[sh] * 1.08 + 8)
    # frame
    fr = (130, 130, 146) if which == 'his' else (196, 190, 200)
    for (a, b_, c_, d_) in ((X0 - 8, Y0 - 8, X1 + 8, Y0), (X0 - 8, Y1, X1 + 8, Y1 + 8), (X0 - 8, Y0, X0, Y1), (X1, Y0, X1 + 8, Y1)):
        img[b_:d_, a:c_] = fr
    img[Y0:Y1, (X0 + X1) // 2 - 2:(X0 + X1) // 2 + 2] = fr
    img[Y1 + 8:Y1 + 14, X0 - 16:X1 + 16] = np.asarray(fr) * 1.1
    img[Y1 + 14:Y1 + 16, X0 - 16:X1 + 16] = np.asarray(fr) * 0.6
    stepped_glow(img, (X0 + X1) / 2, (Y0 + Y1) / 2, 170, warm, k=0.12, levels=3)
    if which == 'his':
        x0, x1, yb = draw_cloud(img, 160, 46, 2.0, t=t, mood=0.3)
        cloud_rain(img, t, x0 + 8, x1 - 8, int(yb), Y1 + 8, density=1.6, seed=31, color=(206, 216, 246))
        splashes(img, t, Y1 + 6, Y1 + 12, x0=int(x0), x1=int(x1), rate=40, seed=12)
    else:
        moon(img, 270, 28, 13, glow=0.8)
        rng = np.random.default_rng(6)
        for i in range(20):
            img[rng.integers(2, 52), rng.integers(0, w)] = (220, 224, 246)
    return img


def S13(t, lt, d):
    img = np.zeros((H, W, 3), np.float32)
    img[:, :320] = _window_half(t, 'his')
    img[:, 320:] = _window_half(t, 'her')
    img[:, 318:322] = (14, 12, 22)
    img[:, 320:321] = (90, 90, 120)
    return img


# ---------------- S14/S15 the cloud and four warm drops ----------------
CLOUD_W = (1141, 380)
DROP_X = (-38, -13, 13, 38)
DROP_FORM = (87.42, 87.73, 88.27, 88.69)
DROP_FALL = (90.95, 91.33, 91.68, 92.32)


def _drop4_wy(t):
    tl = DROP_FALL[3]
    if t < tl:
        return CLOUD_W[1] + 26
    k = seg(t, tl, 95.15)
    return CLOUD_W[1] + 26 + (HER_WIN[1] - 6 - CLOUD_W[1] - 26) * (k * k * (3 - 2 * k) * 0.7 + k * 0.3)


def _sky_cam(t):
    wy = _drop4_wy(t)
    return 981, min(596, max(300, wy - 92))


def S14(t, lt, d):
    return _cloud_drops_shot(t)


def S15(t, lt, d):
    return _cloud_drops_shot(t)


def _cloud_drops_shot(t):
    z = 2.0
    cx_, cy_ = _sky_cam(t)
    img, T = render_sky(cx_, cy_, z, t, 'clear', moon_on=False)
    stepped_glow(img, 660, -40, 300, (170, 186, 255), k=0.12, levels=6)
    if cy_ > 520:
        special_window(img, T, z, 'her', t)
    sx, sy = T(*CLOUD_W)
    x0, x1, yb = draw_cloud(img, sx, sy, 4.6, t=t)
    for i in range(4):
        tf, tl = DROP_FORM[i], DROP_FALL[i]
        if t < tf:
            continue
        r = 6.0 * ease(seg(t, tf, tf + 0.5))
        wx = CLOUD_W[0] + DROP_X[i] * 1.0
        if i == 3 and t >= tl:
            wx = wx + (HER_WIN[0] - wx) * ease(seg(t, tl, 95.0))
        if t < tl:
            wy = CLOUD_W[1] + 26 + math.sin(t * 3 + i) * 0.5
            px, py = T(wx, wy)
            warm_drop(img, px, py, r, glow=0.6 + 0.4 * math.sin(t * 4 + i) ** 2)
        else:
            u = t - tl
            if i < 3:
                wy = CLOUD_W[1] + 26 + 60 * u * u + 30 * u
            else:
                wy = _drop4_wy(t)
            px, py = T(wx, wy)
            if py < H + 20:
                for q in range(1, 6):
                    _, py2 = T(wx, wy - q * 5)
                    fill(img, m_rect(px - 1, py2 - 3, px + 2, py2 + 2), (255, 210, 130), 0.55 * (1 - q / 6))
                warm_drop(img, px, py, 6.0, glow=1.0)
                if u < 0.12:
                    stepped_glow(img, px, py, 40, (255, 230, 170), k=0.8, levels=3)
    return img


# ---------------- S16 tea ----------------
def S16(t, lt, d):
    base, (mx, my, rr) = desk_bg()
    img = base.copy()
    hit = 96.81
    if t < hit:
        u = seg(t, 96.1, hit)
        if u > 0:
            r = 9 - 7 * u
            stepped_glow(img, mx, my, r * 5, (255, 200, 110), k=0.6, levels=4)
            fill(img, m_ellipse(mx, my, r, r), (255, 222, 150))
    else:
        u = t - hit
        tea = m_ellipse(mx, my, rr, rr)
        gr = min(rr, 6 + u * 26)
        gm = m_ellipse(mx, my, gr, gr) & tea
        img[gm] = img[gm] * 0.4 + np.array([255, 176, 80]) * 0.6
        stepped_glow(img, mx, my, 40 + min(60, u * 50), (255, 190, 110), k=0.5 * max(0.4, 1 - u / 2), levels=4)
        for k in range(4):
            rk = (u - k * 0.22) * 34
            if 2 < rk < rr:
                ring = outline_of(m_ellipse(mx, my, rk, rk)) & tea
                img[ring] = np.minimum(255, img[ring] * 0.6 + np.array([255, 236, 190]) * 0.5)
        if u < 0.25:
            splash_ring(img, mx, my, 5, u / 0.25, color=(255, 230, 170))
    # steam wisps (on 6 fps)
    T6 = tq(t, 6)
    for k in range(3):
        ph = (T6 * 0.8 + k / 3) % 1
        yy = my - 20 - ph * 50
        xx = mx - 10 + k * 10 + math.sin(ph * 6 + k) * 4
        a = 0.35 * (1 - ph)
        fill(img, m_ellipse(xx, yy, 3, 6), (255, 244, 230), a)
    return img


# ---------------- S17 her close-up ----------------
def S17(t, lt, d):
    img = room_bg().copy()
    if t < 98.62:
        kw = dict(look=(0.0, 1.0), blink=0.5, expr='calm')
    elif t < 99.59:
        kw = dict(look=(0.4, -0.7), blink=0.0, expr='surprise')
    else:
        kw = dict(look=(0.5, -0.4), blink=0.0, expr='soft', tear=0.12)
    if 101.7 <= t < 101.83:
        kw['blink'] = 1.0
    spr, (ax, ay), _ = her_bust(s=4.4, pal='room', **kw)
    blit(img, spr, int(210 - ax), int(118 - ay))
    return img
