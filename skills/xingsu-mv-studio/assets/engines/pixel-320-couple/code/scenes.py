# -*- coding: utf-8 -*-
"""Backgrounds, weather and reusable scene pieces for 《半岛铁盒》 (320x180 grid)."""
import math
from functools import lru_cache
import numpy as np
from px import (Cv, hx, mix, mul, vgrad, bayer, outline, W, H, OUT, ease, seg, clamp, text, text_w)

# ---------------------------------------------------------------- particles (shared seeds)


@lru_cache(maxsize=64)
def _parts(seed, n):
    r = np.random.default_rng(seed)
    return dict(x=r.uniform(0, 1, n), y=r.uniform(0, 1, n), v=r.uniform(0.6, 1.4, n), amp=r.uniform(2, 9, n),
                fr=r.uniform(0.5, 1.6, n), ph=r.uniform(0, 6.28, n), rot=r.uniform(3, 7, n), col=r.integers(0, 8, n),
                big=r.random(n))


def stars(cv, t, n=60, seed=9, area=(0, 0, W, 90), col=(230, 230, 250)):
    p = _parts(seed, n)
    x0, y0, x1, y1 = area
    for i in range(n):
        x = x0 + p['x'][i] * (x1 - x0)
        y = y0 + p['y'][i] ** 1.5 * (y1 - y0)
        tw = math.sin(t * p['fr'][i] * 3 + p['ph'][i])
        if tw > -0.3:
            cv.px(x, y, col if tw > 0.5 else mix(col, (90, 90, 140), 0.5))


def rain(cv, t, n=120, seed=3, speed=300, wind=-70, length=7, col=(150, 170, 215), col2=None, area=(0, 0, W, H), alpha=1.0):
    """diagonal rain streaks. wind<0 leans left."""
    p = _parts(seed, n)
    x0, y0, x1, y1 = area
    ww, hh = x1 - x0 + 40, y1 - y0 + 20
    col2 = col2 or mix(col, (255, 255, 255), 0.35)
    dx = wind / speed * length
    for i in range(n):
        if alpha < 1.0 and p['big'][i] > alpha:
            continue
        v = 0.75 + 0.5 * p['v'][i]
        y = (p['y'][i] * hh + speed * v * t) % hh + y0 - 10
        x = (p['x'][i] * ww + wind * v * t) % ww + x0 - 20
        ln = length * (0.6 + 0.6 * p['v'][i])
        cv.line(x, y, x + dx * (ln / length), y + ln, col2 if p['big'][i] > 0.8 else col)


def splashes(cv, t, y0, y1, n=30, seed=7, col=(190, 205, 235), x0=0, x1=W, rate=2.5):
    """little splash crowns on the ground; each splash lives ~0.15s and respawns at a new spot."""
    p = _parts(seed, n)
    for i in range(n):
        ph = (t * rate * p['v'][i] + p['ph'][i]) % 1.0
        if ph > 0.22:
            continue
        k = int((t * rate * p['v'][i] + p['ph'][i]))
        r = np.random.default_rng(seed * 1000 + i * 37 + k)
        x = r.uniform(x0, x1); y = r.uniform(y0, y1)
        if ph < 0.08:
            cv.px(x, y, col)
        else:
            cv.px(x - 1, y - 1, col); cv.px(x + 1, y - 1, col)
            if ph < 0.15:
                cv.px(x - 2, y - 2, col); cv.px(x + 2, y - 2, col)


def ripples(cv, t, y0, y1, n=12, seed=11, col=(120, 140, 180), x0=0, x1=W, rate=1.2):
    p = _parts(seed, n)
    for i in range(n):
        ph = (t * rate * p['v'][i] + p['ph'][i]) % 1.0
        k = int(t * rate * p['v'][i] + p['ph'][i])
        r = np.random.default_rng(seed * 1000 + i * 13 + k)
        x = r.uniform(x0, x1); y = r.uniform(y0, y1)
        rx = 1 + ph * 7
        if ph < 0.8:
            for a in range(0, 360, 30):
                cv.px(x + rx * math.cos(math.radians(a)), y + rx * 0.35 * math.sin(math.radians(a)), col)


def glass_rain(cv, t, x0, y0, w, h, seed=21, n=14, col=(120, 140, 190), hi=(200, 215, 245), static=70):
    """water on a window pane: static beads + a few drops sliding down leaving trails."""
    r = np.random.default_rng(seed)
    for i in range(static):
        x = x0 + r.uniform(0, w); y = y0 + r.uniform(0, h)
        cv.px(x, y, col)
        if r.random() < 0.3:
            cv.px(x, y - 1, hi)
    p = _parts(seed + 1, n)
    for i in range(n):
        sp = 10 + 30 * p['v'][i]
        cyc = h + 30
        yy = (p['y'][i] * cyc + sp * t) % cyc - 10
        xx = x0 + p['x'][i] * w + math.sin(yy * 0.15 + p['ph'][i]) * 1.2
        top = max(0, yy - 14 - 10 * p['v'][i])
        for k in range(int(top), int(yy)):
            if 0 <= k < h:
                cv.px(xx + math.sin(k * 0.15 + p['ph'][i]) * 1.2, y0 + k, col)
        if 0 <= yy < h - 1:
            cv.rect(xx - 1, y0 + yy, 2, 2, col); cv.px(xx - 1, y0 + yy, hi)


@lru_cache(maxsize=32)
def cloud_sprite(w, h, seed, c1, c2, c3):
    r = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:h, 0:w]
    m = np.zeros((h, w), bool)
    for i in range(7):
        cx = r.uniform(w * 0.15, w * 0.85)
        cy = r.uniform(h * 0.45, h * 0.75)
        rx = r.uniform(w * 0.12, w * 0.25)
        ry = r.uniform(h * 0.25, h * 0.45)
        m |= ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1
    m[int(h * 0.82):, :] = False
    c = Cv(w, h, alpha=True)
    c.a[m] = (*c1, 255)
    top = m & ~np.vstack([np.zeros((2, w), bool), m[:-2]])
    c.a[top] = (*c2, 255)
    bot = m & ~np.vstack([m[1:], np.zeros((1, w), bool)])
    c.a[bot] = (*c3, 255)
    return c


def dust(cv, t, n=40, seed=31, area=(0, 0, W, H), col=(236, 226, 200), col2=None, speed=3, swirl=None, beam=None):
    """floating dust motes. swirl=(cx, cy, r, w) orbits motes around a center. beam=mask HxW bool: only lit motes drawn bright."""
    p = _parts(seed, n)
    x0, y0, x1, y1 = area
    col2 = col2 or mix(col, (60, 60, 80), 0.55)
    pts = []
    for i in range(n):
        if swirl is not None:
            cx, cy, rr, wsp = swirl
            a = p['ph'][i] + t * wsp * (0.6 + 0.6 * p['v'][i])
            rad = rr * (0.35 + 0.75 * p['x'][i]) + math.sin(t * 2 + i) * 2
            x = cx + math.cos(a) * rad
            y = cy + math.sin(a) * rad * 0.55 + math.sin(t * 1.3 + i) * 2
        else:
            x = x0 + (p['x'][i] * (x1 - x0) + math.sin(t * 0.5 * p['fr'][i] + p['ph'][i]) * 6 * p['amp'][i] / 5) % (x1 - x0)
            y = y0 + (p['y'][i] * (y1 - y0) - speed * p['v'][i] * t + math.cos(t * 0.4 * p['fr'][i] + p['ph'][i]) * 4) % (y1 - y0)
        lit_ = True
        if beam is not None:
            xi, yi = int(x), int(y)
            lit_ = 0 <= yi < beam.shape[0] and 0 <= xi < beam.shape[1] and beam[yi, xi]
        c = col if lit_ else col2
        if p['big'][i] > 0.86 and lit_:
            cv.rect(x, y, 2, 1, c)
        else:
            cv.px(x, y, c)
        pts.append((x, y))
    return pts


# ---------------------------------------------------------------- trees (green canopy)
CANOPY = {
    'day': [hx('#2f5a3a'), hx('#3e7a44'), hx('#5a9a4c'), hx('#86c062')],
    'warm': [hx('#5a5a30'), hx('#7a8a3c'), hx('#a6b04e'), hx('#d8c86a')],
    'night': [hx('#0e1a20'), hx('#14262c'), hx('#1c3436'), hx('#264440')],
    'dusk': [hx('#2a2a3a'), hx('#3a4048'), hx('#4e5a54'), hx('#6a7460')],
}


@lru_cache(maxsize=64)
def canopy(w, h, seed, pal):
    r = np.random.default_rng(seed)
    cols = CANOPY[pal]
    m = np.zeros((h, w), bool)
    yy, xx = np.mgrid[0:h, 0:w]
    blobs = []
    for i in range(12):
        cx = r.uniform(w * 0.18, w * 0.82)
        cy = r.uniform(h * 0.25, h * 0.7)
        rx = r.uniform(w * 0.14, w * 0.28)
        ry = rx * r.uniform(0.6, 0.85)
        blobs.append((cx, cy, rx, ry))
        m |= ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2 <= 1
    L = np.zeros((h, w), np.float32)
    for (cx, cy, rx, ry) in blobs:
        d = ((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2
        v = 0.65 - 0.55 * ((yy - cy) / ry) - 0.25 * ((xx - cx) / rx) - 0.2 * d
        L = np.where(d <= 1, np.maximum(L, v), L)
    L += (yy / h) * -0.25
    by = np.tile(np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16.0, (h // 4 + 1, w // 4 + 1))[:h, :w]
    q = np.clip(np.floor(L * 3.2 + by * 0.6 + 0.3), 0, 3).astype(int)
    c = Cv(w, h, alpha=True)
    pal_a = np.array(cols, np.uint8)
    c.a[m, :3] = pal_a[q[m]]
    c.a[m, 3] = 255
    edge = np.zeros_like(m)
    edge[1:, :] |= m[:-1, :]; edge[:-1, :] |= m[1:, :]; edge[:, 1:] |= m[:, :-1]; edge[:, :-1] |= m[:, 1:]
    edge &= ~m
    pick = edge & (r.random(m.shape) < 0.45)
    c.a[pick, :3] = pal_a[1]
    c.a[pick, 3] = 255
    return c


def buildings(cv, y_base, seed, col, win=None, x0=0, x1=W, hmin=20, hmax=50, lit=0.3, roofcol=None, wet=None):
    r = np.random.default_rng(seed)
    x = x0 - r.integers(0, 10)
    while x < x1:
        bw = int(r.integers(14, 34)); bh = int(r.integers(hmin, hmax))
        cv.rect(x, y_base - bh, bw, bh, col)
        if roofcol:
            cv.rect(x, y_base - bh, bw, 1, roofcol)
        if win is not None:
            for wy in range(y_base - bh + 4, y_base - 4, 6):
                for wx in range(x + 3, x + bw - 3, 5):
                    if r.random() < lit:
                        cv.rect(wx, wy, 2, 3, win)
        x += bw + int(r.integers(0, 4))


def lamp(cv, x, base_y, h=58, on=True, glow_col=(255, 214, 138), post=(40, 36, 52), glow_r=26, k=0.45):
    if on:
        cy = base_y - h + 3
        for rr, f in ((glow_r, 0.18), (glow_r * 0.65, 0.33), (glow_r * 0.38, 0.55)):
            yy, xx = np.mgrid[int(cy - rr):int(cy + rr) + 1, int(x - rr):int(x + rr) + 1]
            m = (xx - x) ** 2 + (yy - cy) ** 2 <= rr * rr
            bm = bayer(m.shape[0], m.shape[1], int(x - rr), int(cy - rr)) < f
            ys, xs = np.nonzero(m & bm)
            ys = ys + int(cy - rr); xs = xs + int(x - rr)
            ok = (ys >= 0) & (ys < cv.h) & (xs >= 0) & (xs < cv.w)
            ys, xs = ys[ok], xs[ok]
            cur = cv.a[ys, xs, :3].astype(np.float32)
            cv.a[ys, xs, :3] = np.clip(cur * (1 - k) + np.array(glow_col) * k, 0, 255).astype(np.uint8)
    cv.rect(x, base_y - h, 2, h, post)
    cv.rect(x - 2, base_y - 2, 6, 2, post)
    cv.rect(x - 3, base_y - h, 8, 2, post)
    cv.rect(x - 2, base_y - h + 2, 6, 3, glow_col if on else (80, 80, 96))


def light_cone(cv, x, y_top, y_bot, w_top, w_bot, col, k=0.25, dens=0.5):
    """additive-ish dithered light cone (e.g. lamp light falling through rain)."""
    m = Cv(W, H, alpha=True)
    m.poly([(x - w_top / 2, y_top), (x + w_top / 2, y_top), (x + w_bot / 2, y_bot), (x - w_bot / 2, y_bot)], (255, 255, 255))
    mm = (m.a[..., 3] > 0) & (bayer() < dens)
    cur = cv.a[mm].astype(np.float32)
    cv.a[mm] = np.clip(cur * (1 - k) + np.array(col) * k, 0, 255).astype(np.uint8)


def glow(cv, x, y, r, col, k=0.4, dens=0.6, sy=1.0):
    yy, xx = np.mgrid[0:cv.h, 0:cv.w]
    d = np.sqrt((xx - x) ** 2 + ((yy - y) / sy) ** 2) / max(r, 1)
    mm = (bayer(cv.h, cv.w) < np.clip(1 - d, 0, 1) * dens * 1.6)
    cur = cv.a[mm, :3].astype(np.float32)
    cv.a[mm, :3] = np.clip(cur * (1 - k) + np.array(col) * k, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- umbrella
def umbrella(cv, hx_, hy_, col, dk, open_=1.0, w=34, tilt=0.0, shaft=18, rib=None, handle=hx('#2a2026')):
    """hand at (hx_, hy_) holds the shaft; canopy sits shaft px above the hand. tilt in degrees (+ = canopy leans right)."""
    a = math.radians(tilt)
    ca, sa = math.cos(a), math.sin(a)

    def P(px_, py_):  # local (x right, y up) -> canvas
        return (hx_ + px_ * ca + py_ * sa, hy_ - (py_ * ca - px_ * sa))
    rib = rib or mix(dk, (0, 0, 0), 0.25)
    # shaft + handle
    x0, y0 = P(0, 0); x1, y1 = P(0, shaft + 2)
    cv.line(x0, y0, x1, y1, hx('#3a3440'))
    hk = [P(0, 0), P(0, -2), P(-1, -3), P(-2, -3), P(-3, -2)]
    for i in range(len(hk) - 1):
        cv.line(hk[i][0], hk[i][1], hk[i + 1][0], hk[i + 1][1], handle)
    o = clamp(open_)
    half = 3 + (w / 2 - 3) * o
    ry = (w * 0.30) * (0.55 + 0.45 * o)
    base = shaft - (1 - o) * 8
    n = 6
    if o < 0.15:  # furled
        pts = [P(-2, base - 9), P(2, base - 9), P(1, base + 3), P(0, base + 5), P(-1, base + 3)]
        cv.poly(pts, col)
        cv.line(*P(-1, base - 8), *P(0, base + 3), dk)
        return
    arc = []
    for i in range(21):
        th = math.pi * i / 20
        arc.append((-half * math.cos(th), base + ry * math.sin(th) * (0.75 + 0.25 * o)))
    bottom = []
    for j in range(n, -1, -1):
        xx = -half + 2 * half * j / n
        bottom.append((xx, base - (1.5 if o > 0.5 else 0.5)))
        if j > 0:
            xm = -half + 2 * half * (j - 0.5) / n
            bottom.append((xm, base + (1.6 * o)))
    pts = [P(*q) for q in arc] + [P(*q) for q in bottom]
    cv.poly(pts, col)
    # shading: right half darker band + ribs
    for j in range(1, n):
        xx = -half + 2 * half * j / n
        cv.line(*P(0, base + ry * 0.95), *P(xx, base - 0.5), rib)
    sh = [P(half * 0.25 * math.cos(math.pi * i / 10), base + ry * 0.9 * math.sin(math.pi * i / 10)) for i in range(0, 6)]
    for (sx, sy) in sh:
        cv.px(sx, sy, mix(col, (255, 255, 255), 0.35))
    for q in arc[:8]:
        X, Y = P(q[0] * 0.92, q[1] - 1)
        cv.px(X, Y, mix(col, (255, 255, 255), 0.25))
    # outline
    for i in range(len(pts) - 1):
        cv.line(pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1], dk)
    tx, ty = P(0, base + ry + 2)
    cv.rect(tx, ty, 1, 2, hx('#3a3440'))


RED_UMB = (hx('#cc3b42'), hx('#972a35'))
BLK_UMB = (hx('#2a2a36'), hx('#16161e'))


# ---------------------------------------------------------------- the room (his childhood room)
ROOM = {
    'night': dict(wall=hx('#1f2340'), wall2=hx('#262a4c'), wall_dk=hx('#181a32'), floor=hx('#2a2236'), floor_dk=hx('#211a2c'),
                  frame=hx('#3a3050'), bed=hx('#3a4a78'), bed_dk=hx('#2c3860'), sheet=hx('#c8c4d8'), desk=hx('#4a3430'),
                  desk_dk=hx('#33241f'), shelf=hx('#3e2e2c'), curtain=hx('#5a3a5a'), curtain_dk=hx('#4a2e4a')),
    'day': dict(wall=hx('#e8d2a8'), wall2=hx('#dcc294'), wall_dk=hx('#c8a878'), floor=hx('#b8865a'), floor_dk=hx('#9c6e48'),
                frame=hx('#f4ead6'), bed=hx('#6a8ac8'), bed_dk=hx('#4e6aa6'), sheet=hx('#fbf4e4'), desk=hx('#9a6a44'),
                desk_dk=hx('#7a5034'), shelf=hx('#8a5a3a'), curtain=hx('#e0a070'), curtain_dk=hx('#c8845a')),
}
WIN = (40, 22, 100, 82)  # window rect x0,y0,w,h


def book_spines(c, x, y, n, seed, h=12, palette=None, lean_last=False):
    r = np.random.default_rng(seed)
    pal = palette or [hx('#c84a3a'), hx('#3a7a8a'), hx('#e0b050'), hx('#5a6aa8'), hx('#7a9a5a'), hx('#d8d0c0'), hx('#8a4a6a')]
    xx = x
    for i in range(n):
        bw = int(r.integers(2, 4)); bh = int(h - r.integers(0, 4))
        col = pal[int(r.integers(0, len(pal)))]
        c.rect(xx, y + h - bh, bw, bh, col)
        c.px(xx, y + h - bh + 2, mix(col, (255, 255, 255), 0.4))
        xx += bw
    return xx


@lru_cache(maxsize=8)
def room_static(mode='night'):
    R = ROOM[mode]
    c = Cv(W, H, R['wall'])
    for x in range(0, W, 12):
        c.rect(x, 0, 1, 128, R['wall2'])
    c.rect(0, 126, W, 2, R['wall_dk'])
    c.rect(0, 128, W, 52, R['floor'])
    for y in range(134, 180, 7):
        c.rect(0, y, W, 1, R['floor_dk'])
    for i, y in enumerate(range(128, 180, 7)):
        for x in range((i * 23) % 40, W, 40):
            c.rect(x, y, 1, 7, R['floor_dk'])
    x0, y0, w, h = WIN
    c.rect(x0 - 2, y0 - 2, w + 4, h + 4, R['frame'])
    c.rect(x0 - 4, y0 + h + 2, w + 8, 4, mix(R['frame'], (0, 0, 0), 0.15))  # sill
    # bed (right)
    c.rect(214, 100, 106, 30, R['bed']); c.rect(214, 126, 106, 4, R['bed_dk'])
    c.rect(214, 96, 106, 6, R['sheet']); c.rect(222, 88, 34, 10, R['sheet']); c.rect(222, 96, 34, 2, mix(R['sheet'], (0, 0, 0), 0.15))
    c.rect(210, 84, 6, 48, R['desk_dk'])
    c.rect(214, 130, 106, 2, mix(R['floor'], (0, 0, 0), 0.35))  # shadow under bed
    # bookshelf on the wall above the bed
    c.rect(232, 54, 70, 3, R['shelf']); c.rect(232, 57, 70, 1, mix(R['shelf'], (0, 0, 0), 0.3))
    book_spines(c, 236, 42, 22, 5)
    c.rect(286, 46, 10, 8, hx('#a8b8c8') if mode == 'day' else hx('#4a5468'))  # little box on shelf
    # wall clock
    c.ellipse(176, 36, 9, 9, hx('#d8d0c0') if mode == 'day' else hx('#9a96a8')); c.ellipse(176, 36, 7, 7, hx('#f2ece0') if mode == 'day' else hx('#c8c4d0'))
    # photo frame on the wall (the two under the red umbrella)
    c.rect(166, 62, 22, 18, hx('#6a4a3a')); c.rect(168, 64, 18, 14, hx('#2a3050'))
    c.rect(172, 69, 10, 3, hx('#cc3b42')); c.rect(176, 72, 1, 5, hx('#3a3440'))
    c.rect(173, 73, 2, 4, hx('#3b5b98')); c.rect(178, 73, 2, 4, hx('#efe4cb'))
    # desk (left) with lamp + candy jar
    c.rect(0, 108, 34, 4, R['desk']); c.rect(2, 112, 3, 16, R['desk_dk']); c.rect(28, 112, 3, 16, R['desk_dk'])
    c.rect(4, 100, 2, 8, hx('#6a6070')); c.rect(1, 96, 9, 4, hx('#8a8090'))
    # calendar under the clock
    c.rect(190, 58, 14, 16, hx('#f2ece0') if mode == 'day' else hx('#9a96a8')); c.rect(190, 58, 14, 4, hx('#c83a36'))
    return c


def candy_jar_small(c, x, y, t=0.0, full=True, key_glint=0.0):
    """tiny jar on the desk; (x,y)= bottom-left."""
    c.rect(x + 1, y - 9, 8, 9, hx('#a8c8d8')); c.rect(x + 2, y - 8, 6, 7, hx('#c8e0ea'))
    c.rect(x, y - 11, 10, 2, hx('#e0b050'))
    if full:
        cols = [hx('#e84a5f'), hx('#f6c040'), hx('#5ab0e0'), hx('#7ac060'), hx('#f08ac0')]
        for i in range(8):
            c.px(x + 2 + (i * 3) % 6, y - 2 - (i // 3) * 2, cols[i % 5])
    if key_glint > 0:
        c.px(x + 4, y - 3, hx('#f6d070')); c.px(x + 5, y - 3, hx('#d8a838'))
        if key_glint > 0.5:
            c.px(x + 4, y - 5, (255, 255, 240)); c.px(x + 3, y - 4, (255, 255, 240)); c.px(x + 5, y - 4, (255, 255, 240))


def window_view(c, t, mode='night', x0=None, y0=None, w=None, h=None, rain_k=1.0, open_=0.0, sun=None, panes=True):
    """outside view in the window: night city in rain / sunny day with a tree / dawn after rain."""
    if x0 is None:
        x0, y0, w, h = WIN
    sub = Cv(w, h)
    if mode == 'night':
        vgrad(sub, 0, h, [hx('#0b0d20'), hx('#11143a'), hx('#1a1d44'), hx('#262650')])
        buildings(sub, h, 21, hx('#0f1024'), win=hx('#e8b868'), lit=0.25, x1=w, hmin=12, hmax=40)
        buildings(sub, h, 22, hx('#161834'), win=hx('#d8a058'), lit=0.2, x1=w, hmin=6, hmax=22)
        if rain_k > 0:
            rain(sub, t, int(40 * rain_k), 41, speed=220, wind=-40, length=5, col=hx('#4a5a8a'), area=(0, 0, w, h))
    elif mode == 'day':
        vgrad(sub, 0, h, [hx('#7cc0e8'), hx('#9ad0ee'), hx('#c4e4f0'), hx('#f4ecd0')])
        cs = cloud_sprite(50, 18, 4, hx('#ffffff'), hx('#ffffff'), hx('#d8e8f2'))
        sub.blit(cs, int(10 + t * 2) % (w + 50) - 25, 8)
        buildings(sub, h, 23, hx('#c8bfcc'), win=hx('#eef2f6'), lit=0.35, x1=w, hmin=10, hmax=30)
        sub.blit(canopy(60, 34, 77, 'day'), 52, -6); sub.blit(canopy(40, 22, 78, 'day'), 70, 18)
        sub.line(w, 4, 62, 14, hx('#4a3a2c')); sub.line(w, 5, 64, 15, hx('#4a3a2c'))
    elif mode == 'dawn':
        vgrad(sub, 0, h, [hx('#3a4a7a'), hx('#6a6a9a'), hx('#c08aa0'), hx('#f0b48a'), hx('#fde0b0')])
        if sun is not None:
            sub.ellipse(sun[0], sun[1], 8, 8, hx('#fff0c8'))
        buildings(sub, h, 21, hx('#4a3e5e'), win=hx('#f6d090'), lit=0.08, x1=w, hmin=12, hmax=40)
        buildings(sub, h, 22, hx('#5e4e6a'), win=None, x1=w, hmin=6, hmax=22)
    c.paste(sub, x0, y0)
    if panes:
        R = ROOM['day' if mode == 'day' else 'night']
        c.rect(x0 + w // 2 - 1, y0, 3, h, R['frame'])
        c.rect(x0, y0 + h // 2 - 1, w, 2, R['frame'])
    if mode == 'night' and rain_k > 0:
        glass_rain(c, t, x0, y0, w, h, seed=21, n=int(12 * rain_k), static=int(60 * rain_k))
    R = ROOM['day' if mode == 'day' else 'night']
    c.rect(x0 - 12, y0 - 6, 10, h + 12, R['curtain']); c.rect(x0 + w + 2, y0 - 6, 10, h + 12, R['curtain'])
    for k in range(0, 10, 3):
        c.rect(x0 - 12 + k, y0 - 6, 1, h + 12, R['curtain_dk']); c.rect(x0 + w + 2 + k, y0 - 6, 1, h + 12, R['curtain_dk'])
    c.rect(x0 - 16, y0 - 8, w + 32, 2, hx('#6a6070'))


def window_light(c, col=(110, 130, 200), k=0.22, floor_y=128):
    x0, y0, w, h = WIN
    pts = [(x0 + 10, floor_y), (x0 + w - 10, floor_y), (x0 + w + 30, H), (x0 + 20, H)]
    m_c = Cv(W, H, alpha=True)
    m_c.poly(pts, (255, 255, 255))
    m = (m_c.a[..., 3] > 0) & (bayer() < 0.5)
    cur = c.a[m].astype(np.float32)
    c.a[m] = np.clip(cur * (1 - k) + np.array(col) * k, 0, 255).astype(np.uint8)


def clock_hands(c, t, cx=176, cy=36, speed=1.0, col=hx('#2a2236')):
    a1 = (t * speed / 60.0) * 2 * math.pi
    a2 = 2 * math.pi * (11 / 12 + t * speed / 43200.0)
    a3 = 2 * math.pi * (t * speed / 3600.0) + 1.3
    c.line(cx, cy, cx + 5 * math.sin(a1), cy - 5 * math.cos(a1), hx('#c83a36'))
    c.line(cx, cy, cx + 3 * math.sin(a2), cy - 3 * math.cos(a2), col)
    c.line(cx, cy, cx + 5 * math.sin(a3), cy - 5 * math.cos(a3), col)
    c.px(cx, cy, col)


def room(t, mode='night', rain_k=1.0, win_mode=None, clock_speed=1.0):
    c = room_static(mode).copy()
    window_view(c, t, win_mode or mode, rain_k=rain_k)
    if mode == 'night':
        window_light(c)
    clock_hands(c, t + 3000, speed=clock_speed)
    return c


# ---------------------------------------------------------------- corridor (old apartment, side view)
@lru_cache(maxsize=4)
def corridor_static(lit=True):
    wall = hx('#5a6478') if lit else hx('#1a1e2e')
    wall2 = hx('#4e5868') if lit else hx('#161a28')
    c = Cv(W, H, wall)
    c.rect(0, 0, W, 18, hx('#7a8290') if lit else hx('#202436'))  # ceiling
    c.rect(0, 18, W, 2, hx('#3a4252') if lit else hx('#10121e'))
    c.rect(0, 96, W, 30, wall2)  # dado
    c.rect(0, 96, W, 2, hx('#3e4656') if lit else hx('#12141f'))
    c.rect(0, 126, W, 54, hx('#6a6a70') if lit else hx('#1c1c26'))  # floor
    for x in range(0, W, 16):
        c.rect(x, 126, 1, 54, hx('#5a5a62') if lit else hx('#16161e'))
    for y in range(140, 180, 12):
        c.rect(0, y, W, 1, hx('#5a5a62') if lit else hx('#16161e'))
    # doors
    for i, dx in enumerate((24, 128, 236)):
        dc = hx('#7a4a34') if lit else hx('#2a1a1a')
        c.rect(dx - 2, 50, 46, 78, hx('#3a3238') if lit else hx('#101014'))
        c.rect(dx, 52, 42, 76, dc)
        c.rect(dx + 4, 56, 34, 30, mix(dc, (0, 0, 0), 0.15)); c.rect(dx + 4, 92, 34, 30, mix(dc, (0, 0, 0), 0.15))
        c.rect(dx + 34, 88, 4, 3, hx('#d8b048') if lit else hx('#4a4030'))
        c.rect(dx + 14, 40, 14, 8, hx('#2a3048') if lit else hx('#0e1018'))
        text(c, dx + 15, 38, ['301', '302', '303'][i], hx('#e8e8f0') if lit else hx('#3a3e50'), font='w')
    for lx in (70, 180, 290):
        c.rect(lx - 8, 18, 16, 3, hx('#f4f0e0') if lit else hx('#2a2c3a'))
        c.rect(lx - 6, 21, 12, 1, hx('#d8d4c8') if lit else hx('#22242e'))
    if lit:
        for lx in (70, 180, 290):
            light_cone(c, lx, 22, 126, 14, 90, hx('#fff4d8'), k=0.12, dens=0.45)
    return c


# ---------------------------------------------------------------- school gate (side-ish front view) for the rain memory
@lru_cache(maxsize=4)
def gate_static():
    c = Cv(W, H)
    D = 24
    vgrad(c, 0, 120 + D, [hx('#1a2038'), hx('#26304e'), hx('#3a4566'), hx('#56607e'), hx('#6a7490')])
    buildings(c, 112 + D, 61, hx('#2a3048'), win=hx('#e8c070'), lit=0.25, hmin=20, hmax=66)
    buildings(c, 116 + D, 62, hx('#343a56'), win=hx('#e8c070'), lit=0.2, hmin=8, hmax=30)
    c.rect(0, 116 + D, W, 22, hx('#3a3e54'))
    for x in range(0, W, 14):
        c.rect(x, 116 + D, 1, 22, hx('#30344a'))
    c.rect(0, 138 + D, W, 2, hx('#5a5e74'))
    c.rect(0, 140 + D, W, 40, hx('#24263a'))
    for x in range(10, W, 44):
        c.rect(x, 172, 20, 1, hx('#4a4c62'))
    c.rect(0, 82 + D, 120, 34, hx('#8a8ea2')); c.rect(0, 82 + D, 120, 3, hx('#a8acbc'))
    for x in range(4, 120, 10):
        c.rect(x, 70 + D, 2, 12, hx('#4a4e62'))
    c.rect(0, 70 + D, 120, 2, hx('#4a4e62'))
    c.rect(18, 46 + D, 10, 70, hx('#9a9eb0')); c.rect(110, 46 + D, 10, 70, hx('#9a9eb0'))
    c.rect(18, 46 + D, 1, 70, hx('#b8bccc')); c.rect(110, 46 + D, 1, 70, hx('#b8bccc'))
    c.rect(8, 38 + D, 124, 8, hx('#5a3a3a')); c.rect(8, 44 + D, 124, 2, hx('#3a2424')); c.rect(8, 38 + D, 124, 1, hx('#7a5050'))
    c.rect(44, 28 + D, 50, 12, hx('#e8e4d8')); c.rect(44, 28 + D, 50, 1, hx('#ffffff'))
    text(c, 48, 28 + D, '半岛中学', hx('#2a2a3a'), font='w')
    c.rect(10, 112 + D, 120, 4, hx('#4a4e64'))
    return c


GATE_Y = 138  # feet line under the awning
STREET_Y = 172  # feet line on the road side


def gate(t, rain_k=1.0):
    c = gate_static().copy()
    lamp(c, 200, 164, h=64, on=True, glow_col=hx('#ffd68a'), post=hx('#2a2636'), glow_r=24)
    lamp(c, 300, 164, h=64, on=True, glow_col=hx('#ffd68a'), post=hx('#2a2636'), glow_r=24)
    if rain_k > 0:
        rain(c, t, int(150 * rain_k), 3, speed=320, wind=-60, length=8, col=hx('#7a8ab0'))
        splashes(c, t, 142, 178, n=int(40 * rain_k), seed=5)
        ripples(c, t, 166, 178, n=8, seed=6, col=hx('#3e4260'))
        for x in range(10, 132, 6):
            ph = (t * 3 + x * 0.37) % 1
            c.px(x, 71 + ph * 64, hx('#9aaad0'))
    return c


# ---------------------------------------------------------------- perspective street (rain) for walking away
@lru_cache(maxsize=4)
def street_static(mode='rain'):
    c = Cv(W, H)
    vx, vy = 160, 70
    vgrad(c, 0, 90, [hx('#141a30'), hx('#1e2642'), hx('#2c3456'), hx('#3e4668')])
    # far glow at the vanishing point
    yy, xx = np.mgrid[0:H, 0:W]
    for rr, f in ((70, 0.2), (40, 0.35)):
        m = ((xx - vx) ** 2 + ((yy - vy) * 1.6) ** 2 < rr * rr) & (bayer() < f)
        c.a[m] = np.clip(c.a[m].astype(np.float32) * 0.6 + np.array([110, 100, 130]) * 0.4, 0, 255).astype(np.uint8)
    c.rect(0, vy, W, H - vy, hx('#3a3c52'))
    # road
    c.poly([(vx - 6, vy), (vx + 6, vy), (W + 80, H), (-80, H)], hx('#262838'))
    # sidewalks
    c.poly([(vx - 6, vy), (vx - 14, vy), (-200, H), (-80, H)], hx('#3a3c52'))
    c.poly([(vx + 6, vy), (vx + 14, vy), (W + 200, H), (W + 80, H)], hx('#3a3c52'))
    # lane dashes
    for k in range(8):
        f0 = (k / 8) ** 2; f1 = ((k + 0.45) / 8) ** 2
        y0_ = vy + (H - vy) * f0; y1_ = vy + (H - vy) * f1
        wd = 0.5 + 3 * f1
        c.poly([(vx - wd * 0.3, y0_), (vx + wd * 0.3, y0_), (vx + wd, y1_), (vx - wd, y1_)], hx('#4a4c60'))
    # buildings on both sides (perspective slabs)
    for side in (-1, 1):
        for k in range(7):
            f0 = ((k) / 7) ** 1.6; f1 = ((k + 0.85) / 7) ** 1.6
            xa = vx + side * (14 + (W) * f0); xb = vx + side * (14 + (W) * f1)
            ya = vy - 6 - 90 * f0; yb = vy - 6 - 90 * f1
            ga = vy + (H - vy) * f0 * 0.4; gb = vy + (H - vy) * f1 * 0.4
            col = hx('#1c2036') if k % 2 else hx('#22263e')
            c.poly([(xa, ya), (xb, yb), (xb, gb + vy * 0), (xa, ga)], col)
            # windows
            rr = np.random.default_rng(k * 7 + (side > 0))
            for j in range(4):
                fx = rr.uniform(0.15, 0.85)
                xx = xa + (xb - xa) * fx; yy = ya + (yb - ya) * fx + (ga - ya) * rr.uniform(0.2, 0.7)
                if rr.random() < 0.55:
                    sz = max(1, int(1 + 3 * f1))
                    c.rect(xx, yy, sz, sz + 1, hx('#e8b868'))
    return c


def street_lamps(c, t, on=True):
    vx, vy = 160, 70
    for side in (-1, 1):
        for k in range(1, 6):
            f = (k / 6) ** 2
            x = vx + side * (18 + 200 * f); base = vy + (H - vy) * f * 0.5 + 4
            h = 6 + 90 * f
            post = hx('#14141e')
            if x < -10 or x > W + 10:
                continue
            c.rect(x, base - h, max(1, int(1 + 2 * f)), h, post)
            gx = x - side * (2 + 10 * f)
            c.rect(min(x, gx), base - h, abs(gx - x) + 1, 1, post)
            if on:
                rr = 3 + 22 * f
                glow(c, gx, base - h + 2, rr, hx('#ffd68a'), k=0.35, dens=0.5)
                c.rect(gx - 1, base - h + 1, 2 + int(2 * f), 1 + int(f), hx('#ffe6a8'))


def street(t, rain_k=1.0, lamps_on=True):
    c = street_static().copy()
    street_lamps(c, t, lamps_on)
    if rain_k > 0:
        rain(c, t, int(140 * rain_k), 13, speed=300, wind=-30, length=8, col=hx('#6a7aa4'))
        splashes(c, t, 120, 178, n=int(34 * rain_k), seed=15, col=hx('#a8b8d8'))
        ripples(c, t, 130, 178, n=8, seed=16, col=hx('#3a3c54'))
    return c
