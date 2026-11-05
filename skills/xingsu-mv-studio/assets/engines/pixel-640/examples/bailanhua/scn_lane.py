# -*- coding: utf-8 -*-
"""弄堂（石库门里弄）立面：一排石库门（乌漆双门+石框+门楣花饰），二楼木窗，晾衣竿，路灯；
她家门上贴“此房出租”。世界 x 0..900，地面 y=262。右端是弄堂口过街楼拱门（外面是街）。"""
import numpy as np, math
from core import *
from sh_street import _put_text

GY = 262
HOUSE_W = 150
HER_X = 300          # her house centre
ARCH_X = 760         # lane mouth arch centre


class Lane:
    def __init__(self):
        self._cache = {}

    def strip(self, z, cam_y, variant='night', state=None, hh=None):
        hh = H if hh is None else hh
        st = dict(her_win=0, wins=0.5)
        if state:
            st.update(state)
        key = (round(z, 3), round(cam_y, 2), variant, tuple(sorted(st.items())), hh)
        if key in self._cache:
            return self._cache[key]
        if len(self._cache) > 6:
            self._cache.pop(next(iter(self._cache)))
        Wp = int(900 * z) + 2
        T = lambda x, y: (x * z, (y - cam_y) * z)
        img = np.zeros((hh, Wp, 3), np.float32)
        vgrad_bands(img, 0, hh, C('#0f0e22'), C('#2a2444'), 6)
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(im)
        lw = max(1, int(round(z)))

        def R(x0, y0, x1, y1, c):
            a, b = T(x0, y0); cc, dd = T(x1, y1)
            if round(cc) - 1 < round(a) or round(dd) - 1 < round(b):
                return
            d.rectangle([round(a), round(b), round(cc) - 1, round(dd) - 1], fill=tuple(int(v) for v in c))

        def PG(pts, c):
            d.polygon([tuple(round(v) for v in T(x, y)) for x, y in pts], fill=tuple(int(v) for v in c))

        def LN(pts, c, w=None):
            d.line([tuple(round(v) for v in T(x, y)) for x, y in pts], fill=tuple(int(v) for v in c), width=w or lw)

        def ELL(cx, cy, rx, ry, c):
            a, b = T(cx - rx, cy - ry); cc, dd = T(cx + rx, cy + ry)
            if round(cc) - 1 < round(a) or round(dd) - 1 < round(b):
                return
            d.ellipse([round(a), round(b), round(cc) - 1, round(dd) - 1], fill=tuple(int(v) for v in c))

        lit, emis, texts = [], [], []
        rng = np.random.default_rng(5)
        # far roofs (other lanes) silhouettes
        x = -10
        while x < 910:
            bw = int(rng.integers(30, 70)); top = int(rng.integers(-40, 20))
            R(x, top, x + bw, 60, (30, 28, 50))
            PG([(x - 4, top), (x + bw / 2, top - 14), (x + bw + 4, top)], (26, 24, 44))
            x += bw + 6
        brick = (78, 50, 50)
        for i in range(-1, 6):
            cx = HER_X + (i - 1) * HOUSE_W
            if cx - 75 > 690:
                break
            x0, x1 = cx - 75, cx + 75
            R(x0, 40, x1, GY, brick)
            if z >= 1.0:
                for yy in range(44, GY, 6):
                    LN([(x0, yy), (x1, yy)], (70, 44, 46))
            # pilaster between houses
            R(x0 - 4, 40, x0 + 4, GY, (110, 102, 98))
            # roof eave
            PG([(x0 - 8, 44), (x1 + 8, 44), (x1 + 2, 30), (x0 - 2, 30)], (44, 40, 54))
            for k in range(int((x1 - x0 + 16) / 7)):
                ELL(x0 - 6 + k * 7, 44, 3.4, 2.4, (58, 54, 70))
            # 2nd floor window (wooden lattice)
            wx0, wx1, wy0, wy1 = cx - 34, cx + 34, 80, 130
            R(wx0 - 4, wy0 - 4, wx1 + 4, wy1 + 6, (110, 100, 96))
            R(wx0, wy0, wx1, wy1, (32, 30, 46))
            on = (rng.random() < st['wins']) if cx != HER_X else st['her_win']
            if on:
                lit.append((wx0 + 2, wy0 + 2, wx1 - 2, wy1 - 2, (236, 180, 110)))
                emis.append((cx, (wy0 + wy1) / 2, 50, (255, 190, 120), 0.18))
            post = []
            for k in range(1, 4):
                post.append(([(wx0 + k * 17, wy0), (wx0 + k * 17, wy1)],))
            post.append(([(wx0, (wy0 + wy1) / 2), (wx1, (wy0 + wy1) / 2)],))
            for (pts,) in post:
                LN(pts, (70, 54, 48), w=max(1, int(1.6 * z)))
            R(wx0 - 6, wy1 + 4, wx1 + 6, wy1 + 8, (120, 110, 104))
            # flower pot on her sill
            if cx == HER_X:
                R(cx + 14, wy1 - 6, cx + 26, wy1 + 4, (150, 80, 60))
                ELL(cx + 20, wy1 - 9, 8, 6, (60, 100, 70))
            # stone gate frame + pediment
            gx0, gx1 = cx - 26, cx + 26
            R(gx0 - 8, 168, gx1 + 8, GY, (150, 142, 132))
            PG([(gx0 - 14, 168), (gx1 + 14, 168), (gx1 + 6, 154), (gx0 - 6, 154)], (156, 148, 138))
            PG([(cx - 20, 154), (cx + 20, 154), (cx, 142)], (150, 142, 132))
            ELL(cx, 160, 7, 4, (120, 112, 104))
            # black lacquer double door
            R(gx0, 176, gx1, GY, (26, 20, 24))
            LN([(cx, 176), (cx, GY)], (50, 40, 44), w=max(1, int(1.4 * z)))
            for sx in (-8, 8):
                ELL(cx + sx, 214, 2.2, 2.2, (170, 140, 80))
            R(gx0 - 6, GY - 4, gx1 + 6, GY, (120, 112, 106))
        # lane mouth arch (过街楼) at the right
        ax = ARCH_X
        R(ax - 70, 20, ax + 90, GY, (92, 70, 66))
        R(ax - 40, 120, ax + 60, GY, (20, 18, 28))
        ELL(ax + 10, 120, 50, 26, (20, 18, 28))
        R(ax - 40, 120, ax + 60, 122, (20, 18, 28))
        # street beyond the arch (distant, cool)
        R(ax - 40, 150, ax + 60, GY, (46, 50, 76))
        R(ax - 40, 210, ax + 60, GY, (60, 62, 86))
        lit.append((ax - 30, 160, ax - 16, 176, (200, 170, 120)))
        lit.append((ax + 30, 168, ax + 44, 182, (170, 190, 220)))
        R(ax - 60, 70, ax + 80, 84, (60, 44, 40))
        texts.append(('安和里', ax + 10, 70, (226, 200, 150)))
        # lamp on the arch (silhouette spot)
        LN([(ax + 52, 132), (ax + 40, 132)], (60, 60, 70), w=max(1, int(2 * z)))
        R(ax + 34, 130, ax + 44, 138, (50, 50, 60))
        lit.append((ax + 35, 137, ax + 43, 140, (255, 220, 160)))
        emis.append((ax + 39, 140, 40, (255, 196, 130), 0.5))
        # wall lamp on the left
        R(120, 150, 128, 162, (50, 50, 60))
        lit.append((121, 160, 127, 163, (255, 220, 160)))
        emis.append((124, 162, 40, (255, 190, 120), 0.4))
        # laundry pole across upper floors
        LN([(0, 70), (690, 66)], (90, 80, 70), w=max(1, int(1.5 * z)))
        for (lx, c) in ((70, (150, 160, 190)), (180, (190, 120, 120)), (450, (200, 200, 190)), (560, (120, 140, 120))):
            PG([(lx, 69), (lx + 18, 69), (lx + 16, 92), (lx + 2, 92)], c)
        # ground: stone slabs
        R(-10, GY, 910, 600, (44, 44, 60))
        for xx in range(0, 900, 30):
            LN([(xx, GY), (xx - 10, 360)], (38, 38, 52))
        for yy in (276, 296, 324):
            LN([(0, yy), (900, yy)], (38, 38, 52))
        img = np.asarray(im, np.float32).copy()
        for (x0, y0, x1, y1, c) in lit:
            a, b = T(x0, y0); cc, dd = T(x1, y1)
            a, b, cc, dd = int(round(a)), int(round(b)), int(round(cc)), int(round(dd))
            img[max(0, b):max(0, dd), max(0, a):max(0, cc)] = c
        for (s_, wx, wy, col) in texts:
            _put_text(img, s_, T, z, wx, wy, col, 1, None)
        res = dict(img=img, emis=emis)
        self._cache[key] = res
        return res


LANE = Lane()


def render_lane(cam_x, cam_y, z, t=0.0, state=None, sign=True, sign_flap=0.0):
    S = LANE.strip(z, cam_y, 'night', state)
    x0 = int(round(cam_x * z))
    x0 = max(0, min(S['img'].shape[1] - W, x0))
    img = S['img'][:, x0:x0 + W].copy()
    T = lambda x, y: (x * z - x0, (y - cam_y) * z)
    for (wx, wy, r, c, s) in S['emis']:
        sx, sy = T(wx, wy)
        if -r * z < sx < W + r * z:
            stepped_glow(img, sx, sy, r * min(z, 1.6), c, k=s / max(1.0, z) ** 0.6, levels=4)
    if sign:
        # red paper “此房出租” on her door (right leaf), corner flaps
        cx = HER_X + 13
        a, b = T(cx - 11, 184); cc, dd = T(cx + 11, 216)
        flap = sign_flap
        pts = [(a, b), (cc, b), (cc - flap * (cc - a) * 0.35, dd - flap * (dd - b) * 0.25), (a, dd)]
        m = m_poly(pts)
        img[outline_of(m) & ~m] = (60, 10, 16)
        img[m] = (200, 40, 44)
        if z >= 1.4:
            _put_text(img, '此房', lambda x, y: (x, y), 1, (a + cc) / 2, b + (dd - b) * 0.1, (250, 220, 120), 1)
            _put_text(img, '出租', lambda x, y: (x, y), 1, (a + cc) / 2, b + (dd - b) * 0.52, (250, 220, 120), 1)
        else:
            for k in range(3):
                img[m_rect(a + 3, b + 4 + k * (dd - b) / 3.5, cc - 3, b + 6 + k * (dd - b) / 3.5)] = (250, 220, 120)
    return img, dict(T=T, z=z, x0=x0)
