# -*- coding: utf-8 -*-
"""S01–S05：前奏 A1（影院翻牌招牌）→ 下摇到街面 → 票的近景 → 午夜招牌熄灭。"""
import numpy as np, math
from core import *
from sprite import place
from chibi import HIM, HER, blink, unit_px
from props import umbrella, orchid_pair, npc_walker, shape
from sh_street import render_street, GY, CIN
from fx import rain, splashes, splash_ring, draw_drop

FLIPS = [3.07, 4.01, 4.96]
SPC = 0.44          # chibi px-per-unit per unit of zoom (world height 44)


def mq_state(t, lights=1.0):
    st = dict(flips=FLIPS, clock=58.0, lights=lights, chase=True, board=1.0, bulbs_on=1.0, flip_start=1.17,
              land=4.96, msg_at=5.91)
    if t < 1.17:
        st.update(bulbs_on=clamp((t - 0.24) / 0.93) if t >= 0.24 else 0.0, chase=False, board=0.0, flips=[None, None, None])
    return st


def _flash(img, t, t0, k=0.45, n=2):
    if t0 <= t < t0 + n / FPS:
        img[:] = img * (1 - k) + np.array([255, 244, 220], np.float32) * k


def S01(t, lt, d):
    # close-up on the marquee: bulbs light from the top centre, title flips and locks on the beat,
    # then the complete 白兰花 holds for two beats (4.96–6.86) before cutting wider
    z = 2.4
    cam_x, cam_y = 855 - 320 / z, 139 - 180 / z
    lit = 1.0 if t >= 1.17 else 0.0
    st = dict(cinema=lit, dance=0, salon=0, apt=0.3)
    img, info = render_street(cam_x, cam_y, z, 'night', state=st, t=t, marquee=mq_state(t), glow=t >= 1.17, wet=False,
                              neon=dict(dance=0, salon=0, poster=0))
    if t < 1.17:
        # darkness: only the bulbs being switched on (keep the rest dim)
        img *= 0.42 + 0.3 * clamp((t - 0.24) / 0.93)
        mq = mq_state(t)
        from sh_street import marquee_overlay
        marquee_overlay(img, info['T'], z, t, mq)
    rain(img, t, layers=('mid', 'near'), density=0.6, color=(206, 214, 236))
    _flash(img, t, 1.17, 0.5)
    return img


S02_Z, S02_C = 0.9, (855, -18)


def S02(t, lt, d):
    # whole facade (static, centred): tower, blade neon flickers on at the cut, clock ticks to 23:59 on the snare
    z = S02_Z
    cam_x, cam_y = S02_C[0] - 320 / z, S02_C[1] - 180 / z
    mins = 58.0 if t < 7.80 else 59.0
    if 7.80 <= t < 7.80 + 0.12:
        mins = 59.25
    blade = 0.0 if t < 6.90 else (1.0 if (6.90 <= t < 6.94 or t >= 7.00) else 0.0)
    mq = dict(flips=FLIPS, clock=mins, lights=1.0, chase=True, board=1.0, bulbs_on=1.0, flip_start=1.17, blade=blade)
    img, info = render_street(cam_x, cam_y, z, 'night', state=dict(cinema=1.0), t=t, marquee=mq, wet=False)
    rain(img, t, density=0.9)
    return img


def _him_waiting(img, t, T, z, x, y, phase='wait'):
    s = SPC * z
    sx, sy = T(x, y)
    if t < 11.59:
        look = 1.6 if (int((t - 8.75) / 1.895) % 2 == 0) else -1.6
        spr, anc = HIM(view='front', s=s, light='lamp', hand_r=(9.5, 70.0), hand_l=(-9.5, 70.0), look=look,
                       eyes='closed' if blink(t, 0.3) else 'open', mouth='flat', rim=(0, -1))
    else:
        spr, anc = HIM(view='front', s=s, light='lamp', hand_r=(9.5, 70.0), hand_l=(-3.5, 61.0), look=-1.2, eyes='down', mouth='flat', rim=(0, -1))
    place(img, spr, anc, sx, sy)
    # tickets in right hand (viewer right), orchid in left
    hx, hy = unit_px(anc, s, sx, sy, 9.5, 71.0)
    shape(img, m_rect(hx - 1.5 * z, hy - 4.5 * z, hx + 2.5 * z, hy + 1 * z), (240, 226, 196), outline=(40, 30, 30))
    if t < 11.59:
        lx, ly = unit_px(anc, s, sx, sy, -9.5, 70.0)
        orchid_pair(img, lx, ly + 1, s=max(0.6, z * 0.5), light=0.95, angle=0.4)
    else:
        lx, ly = unit_px(anc, s, sx, sy, -3.5, 61.0)
        orchid_pair(img, lx - 2 * z, ly + 4 * z, s=max(0.6, z * 0.5), light=0.95, angle=0.9)


def S03(t, lt, d):
    u = ease(seg(t, 8.75, 11.59))
    z = S02_Z + (1.85 - S02_Z) * u
    # camera centre continues from the S02 framing down to the entrance (one continuous tilt)
    cx = S02_C[0] + (855 - S02_C[0]) * u
    cy = S02_C[1] + (222 - S02_C[1]) * u
    cam_x, cam_y = cx - 320 / z, cy - 180 / z
    mq = dict(flips=FLIPS, clock=59.0, lights=1.0, chase=True, board=1.0, bulbs_on=1.0, flip_start=1.17)
    img, info = render_street(cam_x, cam_y, z, 'night', state=dict(cinema=1.0), t=t, marquee=mq)
    T = info['T']
    # pedestrians with umbrellas on the sidewalk
    for k, (t0, x0, sp, fac, kind) in enumerate(((8.4, 640, 30, 1, 0), (9.8, 1060, 26, -1, 1), (10.9, 600, 34, 1, 2))):
        if t >= t0:
            x = x0 + fac * sp * (t - t0)
            sx, sy = T(x, 278)
            if -40 < sx < W + 40:
                npc_walker(img, sx, sy, SPC * z, (t - t0) * 1.6, kind=kind, facing=fac, light='night')
    _him_waiting(img, t, T, z, 855, 270)
    rain(img, t, density=0.9, ox=cam_x * z * 0.2, oy=cam_y * z * 0.2)
    _, gy = T(0, 280)
    splashes(img, t, int(T(0, 264)[1]), int(T(0, 284)[1]), rate=30)
    return img


# ---------------- S04 tickets close-up ----------------
_BG04 = {}


def _bokeh_bg(key, cols):
    if key in _BG04:
        return _BG04[key].copy()
    img = new((14, 14, 28))
    vgrad_bands(img, 0, H, C('#141228'), C('#2a2040'), 6)
    for (x, y, r, c, k) in cols:
        stepped_glow(img, x, y, r, c, k=k, levels=4)
    _BG04[key] = img
    return img.copy()


TK_W, TK_H, TK_PERF = 480, 214, 372


def _ticket(seat, no, date='10月28日 周三'):
    """detailed midnight-show cinema ticket (RGBA float, alpha 0 = punched holes)."""
    w, h = TK_W, TK_H
    tk = np.zeros((h, w, 4), np.float32)
    tk[..., 3] = 1
    paper = np.array((244, 233, 206), np.float32)
    rgb = np.empty((h, w, 3), np.float32)
    rgb[:] = paper
    # guilloche security waves (main part only)
    for k in range(7):
        xs = np.arange(10, TK_PERF - 6)
        ys = (56 + k * 21 + 4 * np.sin(xs / 13.0 + k * 0.9)).astype(int)
        ok = (ys >= 0) & (ys < h)
        rgb[ys[ok], xs[ok]] = (232, 218, 188)
        ys2 = (60 + k * 21 + 4 * np.sin(xs / 13.0 + k * 0.9 + 2.2)).astype(int)
        ok = (ys2 >= 0) & (ys2 < h)
        rgb[ys2[ok], xs[ok]] = (236, 222, 194)
    # header band + gold rule
    rgb[:40] = (176, 40, 52)
    rgb[40:42] = (214, 170, 92)
    draw_text(rgb, '午夜场', 16, 12, (252, 240, 220))
    draw_text(rgb, '★', 74, 12, (240, 200, 110))
    draw_text(rgb, no, TK_PERF - 86, 12, (252, 226, 200))
    # decorative double frame + red corner marks
    for ins, col in ((6, (206, 176, 136)), (9, (226, 204, 168))):
        rgb[46:h - ins, ins] = col; rgb[46:h - ins, w - 1 - ins] = col
        rgb[h - 1 - ins, ins:w - ins] = col
    for (cx, cy, sx, sy) in ((12, 48, 1, 1), (TK_PERF - 10, 48, -1, 1), (12, h - 12, 1, -1), (TK_PERF - 10, h - 12, -1, -1)):
        rgb[cy, min(cx, cx + 7 * sx):max(cx, cx + 7 * sx) + 1] = (180, 50, 60)
        rgb[min(cy, cy + 7 * sy):max(cy, cy + 7 * sy) + 1, cx] = (180, 50, 60)
    # title, pinyin, orchid icon
    draw_text(rgb, '白兰花', 24, 52, (150, 26, 40), scale=3)
    draw_text(rgb, 'B A I   L A N   H U A', 26, 106, (160, 128, 104))
    from props import orchid_pair
    orchid_pair(rgb, 268, 86, s=2.8, angle=-0.35)
    # info lines
    lab, val = (150, 126, 106), (70, 46, 44)
    draw_text(rgb, '日期', 24, 132, lab); draw_text(rgb, date, 62, 132, val)
    draw_text(rgb, '开映', 214, 132, lab); draw_text(rgb, '00:00', 252, 132, (150, 26, 40))
    draw_text(rgb, '座位', 24, 158, lab); draw_text(rgb, seat, 62, 158, val)
    draw_text(rgb, '票价', 214, 158, lab); draw_text(rgb, '40元', 252, 158, val)
    draw_text(rgb, '当日当场有效 · 请提前入场', 24, 186, (170, 150, 128))
    # stub: 副券, red seal, vertical serial, barcode
    sx0 = TK_PERF + 8
    draw_text(rgb, '副', sx0 + 34, 50, val); draw_text(rgb, '券', sx0 + 34, 68, val)
    yy, xx = np.mgrid[0:h, 0:w]
    dd = np.hypot(xx - (sx0 + 42), yy - 120)
    rgb[(dd > 18) & (dd < 21)] = (196, 64, 76)
    draw_text(rgb, '午夜', sx0 + 26, 113, (196, 64, 76))
    for i, ch in enumerate(no[-4:]):
        draw_text(rgb, ch, w - 20, 48 + i * 15, (176, 40, 52))
    x = sx0 + 6
    i = 0
    while x < w - 14:
        bw = 1 + int(h01(i, 17) * 3)
        if h01(i, 29) < 0.62:
            rgb[160:196, x:x + bw] = (46, 36, 36)
        x += bw + 1
        i += 1
    # perforation: dashed line + punched holes
    for y in range(46, h - 4, 9):
        rgb[y:y + 4, TK_PERF] = (176, 156, 128)
        tk[(np.hypot(xx - TK_PERF, yy - (y + 6)) <= 1.8), 3] = 0
    tk[..., :3] = rgb
    return tk


def _paste_rot(img, spr, cx, cy, ang):
    from PIL import Image
    a = np.clip(spr, 0, 255)
    rgba = np.concatenate([a[..., :3], a[..., 3:4] * 255], -1).astype(np.uint8)
    im = Image.fromarray(rgba, 'RGBA').rotate(ang, resample=Image.NEAREST, expand=True)
    arr = np.asarray(im).astype(np.float32)
    h, w = arr.shape[:2]
    x0, y0 = int(round(cx - w / 2)), int(round(cy - h / 2))
    al = (arr[..., 3] > 127)
    ys, xs = np.nonzero(al)
    X, Y = xs + x0, ys + y0
    ok = (X >= 0) & (X < W) & (Y >= 0) & (Y < H)
    img[Y[ok], X[ok]] = arr[ys[ok], xs[ok], :3]
    m = np.zeros((H, W), bool)
    m[Y[ok], X[ok]] = True
    img[outline_of(m)] = (40, 28, 30)
    return m, (x0, y0, w, h)


_TK = {}


def S04(t, lt, d):
    """the two midnight-show tickets, no hands: the front one crisp and straight, the second one behind;
    13.48 a raindrop hits “8座”, the ink bleeds, 14.43 the drop runs down and drips off the edge."""
    drift = int(round(6 * seg(t, 12.45, 15.30)))
    img = _bokeh_bg('s04', [(90, 70, 70, (255, 190, 110), 0.35), (560, 50, 90, (255, 210, 140), 0.3), (470, 300, 60, (255, 90, 170), 0.25),
                            (40, 300, 50, (120, 200, 255), 0.2), (320, 20, 120, (255, 220, 160), 0.18)])
    img = np.roll(img, -drift, axis=1)
    if 'f' not in _TK:
        _TK['f'] = _ticket('7排8座', 'NO.0082')
        _TK['b'] = _ticket('7排9座', 'NO.0083')
    X0, Y0 = 70, 108
    # back ticket peeking out (rotated), then the front ticket's shadow and the ticket itself
    _paste_rot(img, _TK['b'], X0 + TK_W / 2 + 34, Y0 + TK_H / 2 - 30, 5)
    sh = m_rect(X0 + 6, Y0 + 8, X0 + TK_W + 6, Y0 + TK_H + 8)
    img[sh] = img[sh] * 0.55
    tk = _TK['f']
    reg = img[Y0:Y0 + TK_H, X0:X0 + TK_W]
    al = tk[..., 3:4]
    reg[:] = reg * (1 - al) + tk[..., :3] * al
    m1 = np.zeros((H, W), bool)
    m1[Y0:Y0 + TK_H, X0:X0 + TK_W] = tk[..., 3] > 0.5
    img[outline_of(m1) & ~m_rect(X0 - 1, Y0 - 1, X0 + TK_W + 1, Y0 + TK_H + 1) | (outline_of(m1) & ~m1 & m_rect(0, 0, W, H))] = (60, 40, 40)
    # orchid pair tied to the top-left corner with a red thread
    img[m_line([(X0 + 14, Y0 + 54), (X0 - 2, Y0 + 30), (X0 + 8, Y0 + 6)], 1)] = (200, 50, 60)
    img[m_ellipse(X0 + 14, Y0 + 54, 2, 2)] = (40, 30, 34)
    orchid_pair(img, X0 + 8, Y0 + 2, s=4.4, angle=-0.55, glow=0.2)
    # small beads collecting on the paper
    through = img.copy()
    for (tb, bx, by, br) in ((12.62, X0 + 420, Y0 + 70, 2.4), (13.05, X0 + 300, Y0 + 116, 2.0), (13.86, X0 + 150, Y0 + 92, 2.6),
                             (14.70, X0 + 330, Y0 + 176, 2.2)):
        if t >= tb:
            draw_drop(img, through, bx, by, br)
    # the drop on “8座”
    wx, wy = X0 + 106, Y0 + 165
    if 12.9 <= t < 13.48:
        u = (t - 12.9) / 0.58
        img[m_ellipse(wx, -40 + (wy + 40) * u * u, 2.5, 4)] = (210, 226, 250)
    if t >= 13.48:
        r = 5 + 8 * clamp((t - 13.48) / 0.35)
        slide = 0.0
        L = Y0 + TK_H - wy - 2
        if t >= 14.43:
            v = t - 14.43
            slide = min(L, 34 * (v + 0.18 * math.sin(2 * math.pi * 1.4 * v) / (2 * math.pi * 1.4)))
        if slide > 0:
            tr = m_line([(wx, wy), (wx + 1, wy + slide)], 6) & m1
            src = img.copy()
            ys, xs = np.nonzero(tr)
            img[ys, xs] = src[np.maximum(0, ys - 2), xs] * 0.8 + np.array([70, 64, 84], np.float32) * 0.2
        spot = m_ellipse(wx, wy, r, r * 0.8) & m1
        img[spot] = img[spot] * 0.84 + np.array([60, 50, 70], np.float32) * 0.16
        img[outline_of(spot) & m1] = img[outline_of(spot) & m1] * 0.7 + np.array([120, 90, 100], np.float32) * 0.3
        if t < 13.78:
            splash_ring(img, wx, wy, 9, (t - 13.48) / 0.3)
        by = wy + slide
        if slide < L - 0.5:
            img[m_ellipse(wx + 1, by, 3, 3.6)] = (214, 228, 250)
            img[m_rect(wx, by - 2, wx + 1, by - 1)] = (255, 255, 255)
        else:
            t_end = 14.43 + 1.4
            u = clamp((t - t_end) / 0.3)
            if u < 1:
                img[m_ellipse(wx + 1, by + 4 + 70 * u * u, 2.4, 3.2)] = (214, 228, 250)
    rain(img, t, layers=('near',), density=0.8, color=(200, 214, 240))
    return img


def S05(t, lt, d):
    # slow push-in on him while the lights die (feet stay at the same screen spot)
    z = round(1.25 + 0.27 * ease(seg(t, 15.30, 19.46)), 3)
    cam_x, cam_y = 855 - 320 / z, 270 - 310 / z
    mins = 59.0 if t < 16.32 else 60.0
    if 15.9 <= t < 16.32:
        mins = 59.0 + 0.6 * ease(seg(t, 15.9, 16.32))
    lights = 1.0 - clamp((t - 16.32) / 0.95)
    st_c = 1.0 if t < 17.27 else 0.0
    blade = 1.0 if t < 17.27 else (1.0 if (17.36 <= t < 17.44 or 17.52 <= t < 17.58) else 0.0)
    mq = dict(flips=FLIPS, clock=mins, lights=lights, chase=lights > 0.99, board=1.0, bulbs_on=1.0, flip_start=1.17,
              blade=blade, off_chars=0)
    img, info = render_street(cam_x, cam_y, z, 'night', state=dict(cinema=st_c), t=t, marquee=mq)
    if lights < 1.0:
        # the board itself dims with the bulbs
        pass
    T = info['T']
    sx, sy = T(855, 270)
    s = SPC * z * 1.0
    lu = 0.8 * ease(seg(t, 16.5, 16.9)) * (1 - ease(seg(t, 18.2, 18.6)))
    spr, anc = HIM(view='front', s=s, light='lamp' if st_c else 'night', hand_r=(9.5, 70.0), hand_l=(-9.5, 70.0), look_up=lu,
                   mouth='flat', eyes='closed' if blink(t, 0.6) else 'open', rim=(0, -1))
    place(img, spr, anc, sx, sy)
    _flash(img, t, 16.32, 0.35)
    rain(img, t, density=1.0)
    splashes(img, t, int(T(0, 264)[1]), int(T(0, 284)[1]), rate=40)
    return img
