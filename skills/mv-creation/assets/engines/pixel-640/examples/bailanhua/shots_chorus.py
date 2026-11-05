# -*- coding: utf-8 -*-
"""S21–S29：副歌（回到现在的雨夜）—— 水洼倒影 / 白兰花→月份牌 / 香气丝带 / 整条街 / 橱窗倒影 / 海报被雨冲 / 长椅上的白兰花 /
出租车驶过、花落水洼 / 招牌翻回空白。"""
import numpy as np, math, functools
from core import *
from sprite import place
from chibi import HIM, HER, blink, unit_px
from props import umbrella, orchid_pair, shape, npc_girl, bubble, TAXI
from sh_street import render_street, GY, CIN, marquee_overlay
from fx import rain, splashes, ripples, splash_ring, draw_drop
from shots_intro import _bokeh_bg, SPC, FLIPS
from shots_verse import beat_pulse
from shots_pre import beat_idx, _place_world, _hat_sprite

BEATS = TIMING['beats']


# ---------------- S21 top-down puddle: the reflection breaks ----------------
_PUD = {}


def _puddle_reflection(kind):
    if kind in _PUD:
        return _PUD[kind]
    img = new((0, 0, 0))
    vgrad_bands(img, 0, H, C('#0e0d22'), C('#2a2244'), 6)
    stepped_glow(img, 120, 250, 90, (255, 110, 190), k=0.35, levels=4)
    stepped_glow(img, 540, 210, 70, (255, 190, 110), k=0.35, levels=4)
    k = 1.7
    if kind == 'past':
        for (x, kd) in ((230, 0), (410, 3)):
            npc_girl(img, x, 300, k * 0.95, view='front', kind=kd, light='warm', expr='laugh')
        spr, anc = HIM(view='front', s=k, light='warm', hat=False, eyes='happy', mouth='laugh', hand_r=(19.0, 46.0))
        place(img, spr, anc, 320, 300)
        hs = _hat_sprite(k)
        hx, hy = unit_px(anc, k, 320, 300, 21.0, 40.0)
        place(img, hs[0], hs[1], hx, hy)
    else:
        spr, anc = HIM(view='front', s=k, light='cold', eyes='down', mouth='sad', rim=None)
        place(img, spr, anc, 320, 300)
    out = img[::-1].copy()          # upside down: feet at the top (he stands at the puddle edge)
    _PUD[kind] = out
    return out


def S21(t, lt, d):
    img = new((32, 32, 46))
    for y in range(0, H, 10):
        for x in range((y // 10) % 2 * 12, W, 24):
            img[y:y + 1, x:x + 8] = (40, 40, 56)
    pud = m_poly([(70, 120), (120, 70), (260, 46), (420, 52), (560, 90), (600, 170), (560, 270), (430, 312), (250, 316), (110, 280), (60, 200)])
    hit = 67.40
    kind = 'past' if t < hit + 0.22 else 'now'
    refl = _puddle_reflection(kind).copy()
    if kind == 'past':
        refl = refl * 0.9 + np.array([30, 16, 0], np.float32)
    # ripple displacement after the hit
    if t >= hit:
        u = t - hit
        amp = 7 * math.exp(-u * 2.2)
        src = refl.copy()
        cx, cy = 320, 190
        yy, xx = np.mgrid[0:H, 0:W]
        dd = np.sqrt((xx - cx) ** 2 + ((yy - cy) * 1.4) ** 2)
        off = (amp * np.sin(dd * 0.12 - tq(t, 12) * 14)).astype(int)
        refl = src[np.clip(yy + off, 0, H - 1), np.clip(xx + off // 2, 0, W - 1)]
    img[pud] = refl[pud] * 0.82 + np.array([10, 12, 24], np.float32)
    img[outline_of(pud)] = (70, 74, 96)
    # his shoe tips at the top edge (standing at the edge of the puddle)
    for sg in (-1, 1):
        cxs = 320 + sg * 28
        leg = m_rect(cxs - 15, -4, cxs + 15, 14)
        shape(img, leg, (44, 44, 62), outline=(14, 12, 18))
        sh = m_ellipse(cxs, 26, 17, 16) | m_rect(cxs - 17, 12, cxs + 17, 26)
        shape(img, sh, (70, 46, 40), outline=(14, 12, 18))
        img[m_ellipse(cxs - 5, 28, 6, 4) & sh] = (98, 66, 56)
        img[outline_of(sh) & m_rect(0, 30, W, 44)] = (220, 216, 208)
    # rain ripples in the puddle
    ripples(img, t, pud & m_rect(0, 30, W, H), rate=14, flat=0.7, rmax=10)
    # the big drop
    if hit - 0.30 <= t < hit:
        u = (t - (hit - 0.30)) / 0.30
        img[m_ellipse(320, 190, 3 + 6 * (1 - u), 4 + 8 * (1 - u))] = (220, 232, 255)
    if t >= hit:
        u = t - hit
        if u < 0.3:
            splash_ring(img, 320, 190, 12, u / 0.3)
        for kk in range(3):
            r = (u - kk * 0.18) * 160
            if r > 4:
                ring = m_ellipse(320, 190, r, r * 0.72) & ~m_ellipse(320, 190, r - 2, r * 0.72 - 2) & pud
                a = max(0.0, 0.8 - u * 0.5)
                img[ring] = img[ring] * (1 - a) + np.array([200, 214, 240], np.float32) * a
    rain(img, t, layers=('near',), density=0.5)
    return img


# ---------------- S22 orchid in palm -> 月份牌 poster ----------------
@functools.lru_cache(maxsize=4)
def poster_art(w, h):
    img = np.zeros((h, w, 3), np.float32)
    vgrad_bands(img, 0, h, C('#3d6f78'), C('#e8d6b4'), 7)
    # moon behind her
    img[m_ellipse(w * 0.5, h * 0.34, w * 0.36, w * 0.36, w, h)] = (246, 236, 206)
    img[m_ellipse(w * 0.5, h * 0.34, w * 0.33, w * 0.33, w, h)] = (252, 244, 220)
    spr, anc = HER(view='front', s=w / 92.0, light='day', style='now', eyes='open', mouth='lips', lip=(150, 20, 46), look=0.0,
                   blush=True, rim=None)
    place(img, spr, anc, w * 0.5, h * 1.08)
    # orchid sprigs
    for (x, y, a, s) in ((0.13, 0.66, -0.5, 0.017), (0.87, 0.60, 0.6, 0.016), (0.18, 0.80, 0.2, 0.015), (0.82, 0.78, -0.3, 0.016),
                         (0.12, 0.26, 0.9, 0.013), (0.88, 0.30, -0.8, 0.013)):
        orchid_pair(img, w * x, h * y, s=w * s, angle=a)
    # art-deco frame
    gold = np.array((200, 164, 90), np.float32)
    for k, c in ((0, gold), (4, (60, 40, 30)), (6, gold)):
        img[outline_of(m_rect(k, k, w - k, h - k, w, h)) & m_rect(0, 0, w, h, w, h)] = c
    for (cx, cy) in ((10, 10), (w - 11, 10), (10, h - 11), (w - 11, h - 11)):
        img[m_ellipse(cx, cy, 5, 5, w, h)] = gold
    # title band
    img[m_rect(14, h - 54, w - 14, h - 16, w, h)] = (160, 32, 46)
    draw_text(img, '白兰花', w / 2, h - 52, (252, 236, 206), scale=2, anchor='mt')
    draw_text(img, '林俊杰', w - 60, 18, (60, 50, 50))
    return img


def S22(t, lt, d):
    if t < 70.42:
        # the orchid pair hanging from its little wire hook (held off-frame), swaying, glowing on “兰”
        img = _bokeh_bg('s22', [(110, 90, 90, (255, 190, 110), 0.3), (540, 80, 100, (255, 110, 190), 0.25), (500, 300, 70, (120, 200, 255), 0.2)])
        sway = 0.06 * math.sin(tq(t, 12) * 2.4)
        hx, hy = 320, 212
        top = (320 + 40 * math.sin(sway), -12)
        img[m_line([top, (hx, hy - 6)], 1)] = (170, 170, 160)
        img[m_line([(hx - 4, hy - 8), (hx, hy - 4), (hx + 4, hy - 8)], 1)] = (170, 170, 160)
        g = clamp((t - 69.52) / 0.3) if t >= 69.52 else 0.0
        orchid_pair(img, hx, hy, s=9.0, angle=sway, glow=0.4 * g + 0.12)
        rain(img, t, layers=('mid', 'near'), density=0.6)
        return img
    img = new((40, 28, 30))
    for y in range(0, H, 12):
        img[y, :] = (52, 36, 38)
    pw, ph = 280, 344
    art = poster_art(pw, ph)
    oy = 8 - int(round(10 * ease(seg(t, 70.42, 73.2))))
    x0, y0 = 320 - pw // 2, oy
    img[max(0, y0):y0 + ph, x0:x0 + pw] = art[max(0, -y0):H - y0 if y0 + ph > H else ph][:min(ph, H - max(0, y0))]
    # soft glow over her
    stepped_glow(img, 320, 120 + oy, 140, (255, 240, 210), k=0.10 * clamp((t - 70.42) / 0.4), levels=3)
    return img


# ---------------- scent ribbons ----------------
def scent(img, t, t0, rows, speed=120, lifetime=None, alpha=0.6):
    """rows: list of (y0, amp, k, phase). ribbons enter from the right edge at t0 and flow left."""
    T = tq(t, 12)
    if t < t0:
        return
    head = W - (t - t0) * speed * 2.4
    Hh, Ww = img.shape[:2]
    for i, (y0, amp, k, ph) in enumerate(rows):
        xs = np.arange(max(0, int(head)), Ww)
        if len(xs) == 0:
            continue
        ys = y0 + amp * np.sin(xs * k + T * 2.6 + ph) + 3 * np.sin(xs * k * 3.1 - T * 4 + ph)
        for dy, a in ((-1, alpha * 0.45), (0, alpha), (1, alpha * 0.45)):
            yy = np.round(ys + dy).astype(int)
            ok = (yy >= 0) & (yy < Hh)
            img[yy[ok], xs[ok]] = img[yy[ok], xs[ok]] * (1 - a) + np.array([252, 250, 236], np.float32) * a
        # petals drifting along
        for j in range(5):
            px = (Ww - ((T * 70 + j * 140 + i * 50) % (Ww + 60)))
            if px < head:
                continue
            py = y0 + amp * math.sin(px * k + T * 2.6 + ph) + 8 * math.sin(j + T * 3)
            img[m_ellipse(px, py, 2, 1.4, Ww, Hh)] = (252, 250, 236)


# ---------------- S23 wandering, the scent arrives ----------------
def S23(t, lt, d):
    z = 2.0
    stop = 76.30
    tt = min(t, stop)
    x = 560 + 30 * (tt - 73.20)
    cam_x = x - 0.38 * W / z
    cam_y = 268 - 300 / z
    img, info = render_street(cam_x, cam_y, z, 'night', t=t, state=dict(cinema=0.0, cafe=0, salon=0),
                              marquee=dict(flips=FLIPS, clock=60, lights=0.0, chase=False, board=0.0, bulbs_on=1.0, blade=0.0))
    T = info['T']
    k = SPC * z
    sx, sy = T(x, 268)
    lu = 0.9 * ease(seg(t, 76.02, 76.4))
    if t < stop:
        spr, anc = HIM(view='side', s=k, light='night', walk=(t * 1.1) % 1, eyes='down', mouth='sad', look_up=lu, rim=(1, 0))
    else:
        spr, anc = HIM(view='side', s=k, light='night', eyes='open', mouth='o', look_up=lu, rim=(1, 0))
    place(img, spr, anc, sx, sy)
    scent(img, t, 75.20, [(sy - 70 * k, 10, 0.02, 0.0), (sy - 96 * k, 14, 0.015, 2.0), (sy - 52 * k, 8, 0.025, 4.0)])
    rain(img, t, density=0.8)
    splashes(img, t, int(T(0, 264)[1]), H - 30, rate=30)
    return img


# ---------------- S24 the whole street, the ribbon winds along ----------------
def S24(t, lt, d):
    z = 0.62
    u = ease(seg(t, 77.06, 80.70))
    cam_x = 0 + (1700 - W / z) * u
    cam_y = 262 - 292 / z
    img, info = render_street(cam_x, cam_y, z, 'night', t=t, state=dict(cinema=0.0, cafe=0, salon=0),
                              marquee=dict(flips=FLIPS, clock=60, lights=0.0, chase=False, board=0.0, bulbs_on=1.0, blade=0.0))
    T = info['T']
    head = 120 + 1500 * ease(seg(t, 77.06, 80.30))
    xs = np.arange(120, head, 2.0)
    Tq = tq(t, 12)
    pts = [T(x, 205 + 34 * math.sin(x / 70 + Tq * 1.2) - 18 * math.sin(x / 230)) for x in xs]
    for (px, py) in pts:
        for dy, a in ((-1, 0.3), (0, 0.75), (1, 0.3)):
            X, Y = int(round(px)), int(round(py + dy))
            if 0 <= X < W and 0 <= Y < H:
                img[Y, X] = img[Y, X] * (1 - a) + np.array([252, 250, 236], np.float32) * a
    if pts:
        hx, hy = pts[-1]
        stepped_glow(img, hx, hy, 14, (255, 250, 220), k=0.6, levels=3)
    # him, small, following
    xh = 260 + 300 * u
    k = SPC * z
    spr, anc = HIM(view='side', s=k, light='night', walk=(t * 1.3) % 1, rim=(1, 0), mouth='flat')
    sx, sy = T(xh, 270)
    place(img, spr, anc, sx, sy)
    rain(img, t, density=0.7)
    return img


# ---------------- S25 the cafe window reflection ----------------
def S25(t, lt, d):
    z = 2.6
    cam_x, cam_y = 430 - 123, 268 - 300 / z
    img, info = render_street(cam_x, cam_y, z, 'night', t=t, state=dict(cafe=0, cinema=0.0, salon=0))
    T = info['T']
    k = SPC * z
    a0, b0 = T(396, 200); a1, b1 = T(524, 252)
    glass = m_rect(a0, b0, a1, b1)
    refl = img.copy()
    refl[:] = refl * 0.4 + np.array([10, 12, 26], np.float32)
    defend = t >= 82.30
    fade = clamp((t - 82.30) / 0.6)
    if not defend or fade < 1:
        al = 1 - fade
        tmp = refl.copy()
        for (x, kd) in ((a0 + 150, 0), (a0 + 230, 3)):
            npc_girl(tmp, x, b1 + 4, k * 0.86, view='front', kind=kd, light='warm', expr='laugh')
        spr, anc = HIM(view='side', s=k, light='warm', eyes='happy', mouth='laugh', rim=None)
        place(tmp, spr, anc, a0 + 70, b1 + 6, flip=True)
        refl = refl * (1 - al) + tmp * al
    if defend:
        tmp = refl.copy()
        spr, anc = HIM(view='side', s=k, light='cold', eyes='down', mouth='sad', rim=None)
        place(tmp, spr, anc, a0 + 70, b1 + 6, flip=True)
        refl = refl * (1 - fade) + tmp * fade
    img[glass] = img[glass] * 0.45 + refl[glass] * 0.55
    # glass sheen
    for kk in range(3):
        img[m_line([(a0 + 40 + kk * 110, b0), (a0 + 10 + kk * 110, b1)], 3) & glass] *= 1.12
    sx, sy = T(372, 268)
    if not defend:
        spr, anc = HIM(view='side', s=k, light='night', eyes='open', mouth='flat', rim=(1, 0))
        place(img, spr, anc, sx, sy)
    else:
        wig = 3 if int(tq(t, 12) * 12) % 2 else -3
        look = 2.0 if int(tq(t, 12) * 8) % 2 else -2.0
        spr, anc = HIM(view='front', s=k, light='night', eyes='closed', mouth='wavy', look=look,
                       hand_r=(15.0 + wig, 50.0), hand_l=(-15.0 + wig, 50.0), rim=(1, 0))
        place(img, spr, anc, sx, sy)
    rain(img, t, density=0.8)
    splashes(img, t, int(T(0, 264)[1]), H - 30, rate=30)
    return img


# ---------------- S26 the poster in the rain ----------------
def S26(t, lt, d):
    img = new((70, 44, 42))
    for y in range(0, H, 14):
        img[y:y + 1, :] = (54, 34, 34)
        off = 0 if (y // 14) % 2 else 20
        for x in range(off, W, 40):
            img[y:y + 14, x:x + 1] = (54, 34, 34)
    pw, ph = 250, 306
    art = poster_art(pw, ph).copy()
    wet = clamp((t - 86.20) / 1.4) if t >= 86.20 else 0.0
    # water streams (rivulets) smear the colours downward
    if wet > 0:
        for i in range(14):
            cx = int(10 + h01(i, 3) * (pw - 20))
            L = int(ph * min(1.0, wet * (0.6 + 0.6 * h01(i, 4))))
            wd = 3 + int(h01(i, 5) * 5)
            col = art[:, max(0, cx - wd):cx + wd].copy()
            sm = int(10 + 26 * wet)
            for y in range(L - 1, sm, -1):
                art[y, max(0, cx - wd):cx + wd] = col[y - sm] * 0.8 + art[y, max(0, cx - wd):cx + wd] * 0.2
            art[:L, cx:cx + 1] = np.minimum(255, art[:L, cx:cx + 1] * 1.2 + 20)
        art[:] = art * (1 - 0.18 * wet)
    x0, y0 = 320 - pw // 2, 22
    img[y0:y0 + ph, x0:x0 + pw] = art
    img[outline_of(m_rect(x0, y0, x0 + pw, y0 + ph))] = (30, 20, 20)
    # peeling top-right corner, flaps on beats
    p = beat_pulse(t, 0.35)
    fl = 26 + 10 * p
    corner = m_poly([(x0 + pw - fl, y0), (x0 + pw, y0), (x0 + pw, y0 + fl)])
    img[corner] = (70, 44, 42)
    flap = m_poly([(x0 + pw - fl, y0), (x0 + pw, y0 + fl), (x0 + pw - fl - 4 * p, y0 + fl + 6 + 4 * p)])
    shape(img, flap, (226, 214, 190), outline=(30, 20, 20))
    dens = 1.0 + 1.2 * wet
    rain(img, t, density=dens)
    return img


# ---------------- S27 the orchid on the bench ----------------
def S27(t, lt, d):
    z = 2.6
    cam_x, cam_y = 1130 - 123, 268 - 300 / z
    img, info = render_street(cam_x, cam_y, z, 'night', t=t, state=dict(cinema=0.0))
    T = info['T']
    k = SPC * z
    picked = t >= 89.30
    if not picked:
        bx, by = T(1140, 237)
        orchid_pair(img, bx, by, s=2.4, angle=0.1, light=0.9, glow=0.25)
    x = 1050 + 66 * ease_out(seg(t, 88.26, 89.0))
    sx, sy = T(x, 268)
    if t < 89.0:
        spr, anc = HIM(view='side', s=k, light='night', walk=(t * 1.6) % 1, eyes='down', mouth='flat', rim=(1, 0))
        place(img, spr, anc, sx, sy)
    elif t < 89.9:
        spr, anc = HIM(view='side', s=k, light='night', hand_r=(17.0, 56.0), eyes='down', mouth='o', rim=(1, 0))
        place(img, spr, anc, sx, sy)
        if picked:
            hx, hy = unit_px(anc, k, sx, sy, 17.0, 56.0)
            orchid_pair(img, hx + 2, hy, s=2.4, angle=-0.2, glow=0.3)
    else:
        chest = t >= 91.20
        hr = (4.0, 61.0) if chest else (10.0, 64.0)
        spr, anc = HIM(view='front', s=k, light='night', hand_r=hr, hand_l=(-5.0, 63.0) if chest else None,
                       eyes='closed' if chest else 'down', mouth='sad', rim=(1, 0))
        place(img, spr, anc, sx, sy)
        hx, hy = unit_px(anc, k, sx, sy, hr[0], hr[1])
        orchid_pair(img, hx, hy - 2, s=2.4, angle=0.0, glow=0.35 if chest else 0.2)
    rain(img, t, density=0.9)
    splashes(img, t, int(T(0, 264)[1]), H - 30, rate=30)
    return img


# ---------------- S28 the taxi passes; the orchid falls ----------------
def S28(t, lt, d):
    frozen = t >= 95.20
    tt = min(t, 95.20)
    z = round(1.6 + 0.3 * ease(seg(tt, 91.80, 95.20)), 3)          # slow push-in, holds on the freeze
    cam_x, cam_y = 900 - 360 / z, 270 - 236 / z
    img, info = render_street(cam_x, cam_y, z, 'night', t=tt, state=dict(cinema=0.0),
                              marquee=dict(flips=FLIPS, clock=60, lights=0.0, chase=False, board=0.0, bulbs_on=1.0, blade=0.0))
    T = info['T']
    k = SPC * z
    sx, sy = T(900, 270)
    dropped = tt >= 93.82
    eyes = 'down' if not dropped else ('wide' if tt < 94.4 else 'sad')
    spr, anc = HIM(view='front', s=k, light='night', hand_r=(4.0, 61.0) if not dropped else (8.0, 66.0), eyes=eyes, mouth='sad', rim=(1, 0))
    place(img, spr, anc, sx, sy)
    if not dropped:
        hx, hy = unit_px(anc, k, sx, sy, 4.0, 61.0)
        orchid_pair(img, hx, hy - 2, s=1.8, glow=0.2)
    else:
        u = clamp((tt - 93.82) / 0.18)
        hx, hy = unit_px(anc, k, sx, sy, 8.0, 66.0)
        gy = sy - 2
        y = hy + (gy - hy) * u * u
        if u < 1:
            orchid_pair(img, hx, y, s=1.8, angle=u * 1.2)
        else:
            orchid_pair(img, hx + 4, gy, s=1.8, angle=1.4, light=0.85)
            if tt < 94.30:
                splash_ring(img, hx + 4, gy, 6, (tt - 94.0) / 0.3)
            rr = m_ellipse(hx + 4, gy + 1, 22, 4)
            ripples(img, tt, rr, rate=6, flat=0.25, rmax=12, seed=7)
    # taxi from right to left on the road (passes in front of him), her silhouette in the rear window
    if 91.86 <= tt < 93.70:
        u = (tt - 91.86) / 1.84
        tx = W + 140 - (W + 380) * u
        spr, anc = TAXI(round(1.25 * z / 1.6 / 0.05) * 0.05, 'night', True)
        ty = T(0, 316)[1]
        stepped_glow(img, tx - 100, ty - 30, 70, (255, 240, 200), k=0.35, levels=3, sy=0.5)
        place(img, spr, anc, tx, ty, flip=True)
    rain(img, t, density=1.0, stop_at=95.20 if frozen else None)
    if not frozen:
        splashes(img, t, int(T(0, 264)[1]), H - 30, rate=34)
    else:
        g = img.mean(2, keepdims=True)
        img[:] = img * 0.5 + g * 0.5
        img[:] = img * np.array([0.9, 0.94, 1.04], np.float32)
    return img


# ---------------- S29 the title flips back to blank ----------------
def S29(t, lt, d):
    z = 2.4
    cam_x, cam_y = 855 - 320 / z, 141 - 180 / z
    mq = dict(flips=FLIPS, clock=60, lights=0.0, chase=False, board=0.0, bulbs_on=1.0, blade=0.0, flip_start=0.0,
              blank=[95.90, 96.22, 96.54])
    img, info = render_street(cam_x, cam_y, z, 'night', state=dict(cinema=0.0, dance=0, salon=0), t=t, marquee=mq, wet=False,
                              neon=dict(dance=0, salon=0, poster=0))
    img *= 0.8
    rain(img, t, layers=('mid', 'near'), density=0.6)
    if t >= 96.85:
        a = clamp((t - 96.85) / 0.25)
        draw_text(img, '白兰花  ·  林俊杰', 320, 300, (236, 228, 214), outline=(20, 16, 24), a=a, anchor='mt')
    return img
