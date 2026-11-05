# -*- coding: utf-8 -*-
"""Night city seen from above the rooftops: sky, moon, big night clouds, rows of buildings, HIS window and HER window.
World: 1500 x 1000. His window centre (300, 690); her window centre (1172, 664)."""
import numpy as np, math, functools
from core import *

WW, WH = 1500, 1000
MOON = (520, 150, 24)
HIS_WIN = (307, 714, 34, 40)
HER_WIN = (1141, 692, 34, 40)

SKY_BANDS = {
    'rain': [C('#121226'), C('#16162c'), C('#1b1a34'), C('#211f3c'), C('#282444'), C('#30294c'), C('#3a3054'), C('#46375c')],
    'clear': [C('#0f1630'), C('#121b38'), C('#162141'), C('#1a284a'), C('#203054'), C('#27395e'), C('#304368'), C('#3b4d70')],
}


class Skyline:
    def __init__(self):
        self.cache = {}

    def base(self, z, variant='rain', hiswin=1, herwin=1):
        key = (round(z, 3), variant, hiswin, herwin)
        if key in self.cache:
            return self.cache[key]
        if len(self.cache) > 4:
            self.cache.pop(next(iter(self.cache)))
        Wp, Hp = int(WW * z) + 2, int(WH * z) + 2
        img = np.zeros((Hp, Wp, 3), np.float32)
        bands = SKY_BANDS[variant]
        vgrad_bands(img, 0, int(720 * z), bands[0], bands[-1], len(bands))
        img[int(720 * z):] = bands[-1]
        if variant == 'clear':
            rng = np.random.default_rng(1)
            for i in range(160):
                x, y = rng.integers(0, Wp), rng.integers(0, int(520 * z))
                img[y, x] = (200, 210, 240) if rng.random() < 0.7 else (255, 240, 200)
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(im)
        lw = max(1, int(round(z)))
        T = lambda x, y: (x * z, y * z)

        def R(x0, y0, x1, y1, c):
            a, b = T(x0, y0); cc, dd = T(x1, y1)
            if round(cc) - 1 < round(a) or round(dd) - 1 < round(b):
                return
            d.rectangle([round(a), round(b), round(cc) - 1, round(dd) - 1], fill=tuple(int(v) for v in c))

        def PG(pts, c):
            d.polygon([tuple(round(v) for v in T(x, y)) for x, y in pts], fill=tuple(int(v) for v in c))
        lit = []
        sil = []
        rng = np.random.default_rng(7)
        # far skyline
        x = -20
        while x < WW + 20:
            bw = int(rng.integers(30, 90)); top = int(rng.integers(520, 620))
            R(x, top, x + bw, WH, (48, 40, 76))
            if rng.random() < 0.3:
                R(x + bw // 2 - 1, top - 30, x + bw // 2 + 1, top, (48, 40, 76))
                R(x + bw // 2 - 1, top - 31, x + bw // 2 + 1, top - 29, (255, 80, 80))
            for yy in range(top + 8, WH, 13):
                for xx in range(x + 5, x + bw - 5, 9):
                    if rng.random() < 0.1:
                        R(xx, yy, xx + 3, yy + 4, (130, 104, 92))
            x += bw + int(rng.integers(-4, 8))
        # mid row
        x = -30
        while x < WW + 30:
            bw = int(rng.integers(70, 150)); top = int(rng.integers(600, 680))
            R(x, top, x + bw, WH, (34, 30, 56))
            R(x, top, x + bw, top + 3, (52, 46, 80))
            for yy in range(top + 10, WH, 18):
                for xx in range(x + 8, x + bw - 10, 14):
                    if rng.random() < 0.18:
                        R(xx, yy, xx + 6, yy + 8, (236, 176, 104) if rng.random() < 0.7 else (140, 180, 210))
                    else:
                        R(xx, yy, xx + 6, yy + 8, (28, 26, 44))
            # roof props
            if rng.random() < 0.5:
                tx = x + bw * 0.3
                R(tx, top - 16, tx + 18, top, (44, 40, 64)); R(tx - 2, top - 18, tx + 20, top - 15, (60, 54, 84))
            if rng.random() < 0.5:
                ax_ = x + bw * 0.75
                d.line([T(ax_, top), T(ax_, top - 26)], fill=(60, 54, 84), width=lw)
                d.line([T(ax_ - 6, top - 20), T(ax_ + 6, top - 20)], fill=(60, 54, 84), width=lw)
            x += bw + int(rng.integers(6, 30))

        def block(x0, x1, top, base, seed, special=None):
            r = np.random.default_rng(seed)
            R(x0, top, x1, WH, base)
            R(x0 - 4, top - 6, x1 + 4, top, tuple(int(v * 1.25) for v in base))
            R(x0 - 4, top, x1 + 4, top + 2, tuple(int(v * 0.7) for v in base))
            if z >= 0.9:
                for yy in range(int(top) + 4, WH, 6):
                    d.line([T(x0, yy), T(x1, yy)], fill=tuple(int(v * 0.93) for v in base), width=1)
            for yy in range(int(top) + 22, WH - 20, 60):
                for xx in range(int(x0) + 18, int(x1) - 30, 56):
                    cx, cy = xx + 17, yy + 20
                    if special and any(abs(cx - sx) < 30 and abs(cy - sy) < 30 for (sx, sy, _, _, _) in special):
                        continue
                    R(xx - 3, yy - 3, xx + 37, yy + 43, tuple(int(v * 0.6) for v in base))
                    on = r.random() < 0.35
                    if on:
                        tv = r.random() < 0.25
                        c = (236, 178, 108) if not tv else (140, 176, 220)
                        lit.append((xx, yy, xx + 34, yy + 40, c))
                        kind = r.random()
                        if kind < 0.22:
                            sil.append(('cat', xx, yy))
                        elif kind < 0.5:
                            sil.append(('person', xx, yy))
                        elif kind < 0.62:
                            sil.append(('couple', xx, yy))
                        elif kind < 0.75:
                            sil.append(('plant', xx, yy))
                    else:
                        R(xx, yy, xx + 34, yy + 40, (30, 30, 48)); R(xx, yy, xx + 15, yy + 40, (38, 40, 60))
                    R(xx - 4, yy + 40, xx + 38, yy + 44, tuple(int(v * 1.3) for v in base))
                    if r.random() < 0.3:
                        R(xx + 40, yy + 26, xx + 54, yy + 40, (96, 98, 116))
            # rooftop tank
            R(x0 + 20, top - 34, x0 + 52, top - 6, tuple(int(v * 0.9) for v in base))
            R(x0 + 18, top - 38, x0 + 54, top - 32, tuple(int(v * 1.2) for v in base))
        hw = (HIS_WIN[0], HIS_WIN[1], HIS_WIN[2], HIS_WIN[3], 'his')
        rw = (HER_WIN[0], HER_WIN[1], HER_WIN[2], HER_WIN[3], 'her')
        block(160, 440, 612, (56, 60, 84), 11, special=[hw])
        block(470, 640, 700, (64, 58, 78), 12)
        block(700, 900, 730, (58, 62, 80), 13)
        block(930, 1020, 690, (66, 60, 84), 14)
        block(1050, 1310, 590, (70, 64, 86), 15, special=[rw])
        block(1340, 1520, 650, (54, 58, 80), 16)
        img = np.asarray(im, np.float32).copy()
        for (x0, y0, x1, y1, c) in lit:
            a, b = T(x0, y0); cc, dd = T(x1, y1)
            img[max(0, int(round(b))):max(0, int(round(dd))), max(0, int(round(a))):max(0, int(round(cc)))] = c
        im3 = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
        d3 = ImageDraw.Draw(im3)
        sc_ = (60, 40, 46)

        def P3(L, ox, oy):
            d3.polygon([tuple(round(v) for v in T(ox + x, oy + y)) for x, y in L], fill=sc_)
        for (k, ox, oy) in sil:
            if k == 'cat':
                P3([(20, 40), (20, 31), (21, 28), (23, 30), (25, 30), (27, 28), (28, 31), (28, 40)], ox, oy)
                P3([(28, 39), (32, 36), (33, 37), (29, 40)], ox, oy)
            elif k == 'person':
                P3([(8, 40), (9, 30), (12, 27), (11, 24), (11, 20), (14, 17), (18, 18), (19, 22), (18, 26), (21, 28), (24, 40)], ox, oy)
            elif k == 'couple':
                P3([(4, 40), (5, 31), (8, 28), (7, 23), (10, 19), (14, 21), (14, 26), (16, 29), (18, 26), (18, 21), (22, 19), (25, 23), (24, 28), (27, 31), (28, 40)], ox, oy)
            elif k == 'plant':
                P3([(24, 40), (25, 34), (31, 34), (32, 40)], ox, oy)
                P3([(22, 34), (26, 24), (28, 30), (30, 22), (31, 30), (34, 26), (33, 34)], ox, oy)
        img = np.asarray(im3, np.float32).copy()
        res = dict(img=img, z=z)
        self.cache[key] = res
        return res


SKYL = Skyline()


def moon(img, sx, sy, r, glow=1.0, cover=None):
    stepped_glow(img, sx, sy, r * 4.2, (170, 186, 255), k=0.35 * glow, levels=4)
    m = m_ellipse(sx, sy, r, r, img.shape[1], img.shape[0])
    fill(img, m, (240, 238, 220))
    fill(img, inner_edge(m, 1, 1, max(1, int(r / 8))), (214, 212, 200))
    for (dx, dy, rr) in ((-0.3, -0.2, 0.22), (0.25, 0.25, 0.16), (0.1, -0.45, 0.1), (-0.1, 0.4, 0.12)):
        fill(img, m_ellipse(sx + dx * r, sy + dy * r, rr * r, rr * r, img.shape[1], img.shape[0]) & m, (220, 218, 204))


def night_cloud(img, cx, cy, sc, seed=0, col=(50, 50, 84), rim=(120, 130, 190), a=1.0, moonlit=None):
    """large rain cloud: bumpy lit top, puff contours, dark flat underside."""
    rng = np.random.default_rng(seed)
    Hh, Ww = img.shape[:2]
    n = 7
    puffs = []
    for i in range(n):
        x = cx + (i - (n - 1) / 2) * 20 * sc + rng.uniform(-5, 5) * sc
        hump = math.sin((i + 0.5) / n * math.pi)
        r = (14 + 14 * hump + rng.uniform(-3, 3)) * sc
        y = cy - hump * 10 * sc + rng.uniform(-3, 3) * sc
        puffs.append((x, y, r))
    m = np.zeros((Hh, Ww), bool)
    for (x, y, r) in puffs:
        m |= m_ellipse(x, y, r, r * 0.78, Ww, Hh)
    bottom = cy + 8 * sc
    m &= m_rect(0, 0, Ww, bottom, Ww, Hh)
    if not m.any():
        return m
    c0 = np.asarray(col, np.float32)
    fill(img, m, c0, a)
    # puff contours: the upper arc of each puff that lies inside the union -> lighter step
    for (x, y, r) in puffs:
        pm = m_ellipse(x, y, r, r * 0.78, Ww, Hh) & m
        top = pm & ~shift(pm, 0, max(1, int(3 * sc)))
        fill(img, top, c0 * 1.18 + 6, a)
    # dark underside
    fill(img, m & ~shift(m, 0, -max(2, int(5 * sc))), c0 * 0.78, a)
    # silver rim on the top edge
    rimm = inner_edge(m, 0, -1, max(1, int(1.5 * sc)))
    fill(img, rimm, rim, a * 0.85)
    if moonlit is not None:
        mx, my = moonlit
        ys, xs = np.nonzero(rimm)
        near = np.hypot(xs - mx, ys - my) < 110 * sc
        img[ys[near], xs[near]] = img[ys[near], xs[near]] * (1 - a) + np.array([224, 230, 252], np.float32) * a
    return m


def render_sky(cam_x, cam_y, z, t, variant='rain', hiswin=1, herwin=1, clouds=None, moon_on=True, moon_cover=0.0):
    """clouds: list of (wx, wy, scale, seed). Returns img and T."""
    B = SKYL.base(z, variant, hiswin, herwin)
    x0, y0 = int(round(cam_x * z)), int(round(cam_y * z))
    img = B['img'][y0:y0 + H, x0:x0 + W].copy()
    if img.shape[0] < H or img.shape[1] < W:
        pad = np.zeros((H, W, 3), np.float32); pad[:img.shape[0], :img.shape[1]] = img; img = pad
    T = lambda x, y: (x * z - x0, y * z - y0)
    if moon_on:
        mx, my = T(MOON[0], MOON[1])
        if -200 < my < H + 200:
            moon(img, mx, my, MOON[2] * z)
    for (wx, wy, sc, sd) in (clouds or []):
        sx, sy = T(wx, wy)
        if -300 < sx < W + 300 and -200 < sy < H + 200:
            night_cloud(img, sx, sy, sc * z, seed=sd, moonlit=T(MOON[0], MOON[1]) if moon_on else None)
    return img, T


def special_window(img, T, z, which='his', t=0.0, lit=1.0, occupant=True, curtain=True, open_=0.0):
    """exterior view of HIS or HER window at world position, drawn at zoom z (screen space)."""
    cx, cy, w, h = HIS_WIN if which == 'his' else HER_WIN
    x0, y0 = T(cx - w / 2, cy - h / 2)
    x1, y1 = T(cx + w / 2, cy + h / 2)
    x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
    fw = max(1, int(round(3 * z)))
    Hh, Ww = img.shape[:2]
    def RR(a, b, c, d, col):
        a, b, c, d = max(0, a), max(0, b), min(Ww, c), min(Hh, d)
        if c > a and d > b:
            img[b:d, a:c] = col
    RR(x0 - fw, y0 - fw, x1 + fw, y1 + fw, (150, 146, 160) if which == 'her' else (120, 120, 136))
    warm = np.array([246, 186, 112], np.float32) if which == 'his' else np.array([255, 204, 136], np.float32)
    dark = np.array([34, 34, 52], np.float32)
    RR(x0, y0, x1, y1, tuple(dark + (warm - dark) * lit))
    if lit > 0.3:
        stepped_glow(img, (x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) * 1.5, warm, k=0.22 * lit, levels=3)
    wpx = x1 - x0
    if which == 'his':
        if curtain:
            RR(x0, y0, x0 + int(wpx * 0.22), y1, tuple(warm * 0.72))
        if occupant:
            # fedora silhouette, standing, slightly right of centre
            sx = x0 + wpx * 0.58
            s = wpx / 34.0
            P = lambda L: [(sx + a * s, y1 + b * s) for a, b in L]
            sil = m_poly(P([(-11, 0), (-10, -16), (-6, -21), (-4, -26), (-3.5, -31), (-9, -31.5), (-9, -33), (-4, -33.5), (-3.6, -38), (3.6, -38), (4, -33.5), (9, -33), (9, -31.5), (3.5, -31), (4, -26), (6, -21), (10, -16), (11, 0)]), Ww, Hh)
            sil &= m_rect(x0, y0, x1, y1, Ww, Hh)
            fill(img, sil, (44, 30, 38))
    else:
        if curtain:
            RR(x0, y0, x0 + int(wpx * 0.2), y1, (236, 186, 70))
            RR(x1 - int(wpx * 0.2), y0, x1, y1, (236, 186, 70))
            RR(x0, y0, x0 + int(wpx * 0.2), y0 + max(1, int(z * 2)), (255, 220, 120))
        if occupant:
            sx = x0 + wpx * 0.45
            s = wpx / 36.0
            P = lambda L: [(sx + a * s, y1 + b * s) for a, b in L]
            sil = m_poly(P([(-10, 0), (-9, -10), (-6, -13), (-7, -18), (-7.5, -24), (-5, -28), (0, -29.5), (5, -28), (7.5, -24), (7, -18), (6, -13), (9, -10), (10, 0)]), Ww, Hh)
            fill(img, sil, (60, 40, 46))
        # plant on sill
        px = x1 - int(wpx * 0.32)
        RR(px - int(3 * z), y1 - int(6 * z), px + int(3 * z), y1, (150, 80, 60))
        fill(img, m_ellipse(px, y1 - 9 * z, 5 * z, 4 * z, Ww, Hh), (70, 120, 80))
    RR(x0 - fw * 2, y1 + fw, x1 + fw * 2, y1 + fw * 2 + max(1, int(z)), (170, 168, 186))
    if open_ > 0:
        # casement opened outward on the right
        ow = int(wpx * 0.5 * open_)
        RR(x1, y0 - fw, x1 + ow, y1 + fw, (60, 62, 84))
        RR(x1 + 1, y0, x1 + ow - 1, y1, (90, 96, 130))
    return (x0, y0, x1, y1)
