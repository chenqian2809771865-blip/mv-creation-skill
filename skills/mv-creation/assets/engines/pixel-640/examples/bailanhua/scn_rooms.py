# -*- coding: utf-8 -*-
"""Interiors drawn in a 640x360 'world' (z=1) and re-rasterized at any zoom: cafe, salon mirror, dance hall,
dining room (night), bedroom. Each returns (img, T) where T maps world->screen."""
import numpy as np, math, functools
from core import *


class Canvas:
    """PIL drawing in world coords with zoom z and camera centre (cx, cy)."""

    def __init__(self, z=1.0, cx=320, cy=180, w=W, h=H):
        self.z, self.cx, self.cy = z, cx, cy
        self.w, self.h = w, h
        self.im = Image.new('RGB', (w, h), (0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def T(self, x, y):
        return ((x - self.cx) * self.z + self.w / 2, (y - self.cy) * self.z + self.h / 2)

    def R(self, x0, y0, x1, y1, c):
        a, b = self.T(x0, y0); cc, dd = self.T(x1, y1)
        if round(cc) - 1 < round(a) or round(dd) - 1 < round(b):
            return
        self.d.rectangle([round(a), round(b), round(cc) - 1, round(dd) - 1], fill=tuple(int(v) for v in c))

    def PG(self, pts, c):
        self.d.polygon([tuple(round(v) for v in self.T(x, y)) for x, y in pts], fill=tuple(int(v) for v in c))

    def LN(self, pts, c, w=1.0):
        self.d.line([tuple(round(v) for v in self.T(x, y)) for x, y in pts], fill=tuple(int(v) for v in c), width=max(1, int(round(w * self.z))))

    def ELL(self, cx, cy, rx, ry, c):
        a, b = self.T(cx - rx, cy - ry); cc, dd = self.T(cx + rx, cy + ry)
        if round(cc) - 1 < round(a) or round(dd) - 1 < round(b):
            return
        self.d.ellipse([round(a), round(b), round(cc) - 1, round(dd) - 1], fill=tuple(int(v) for v in c))

    def arr(self):
        return np.asarray(self.im, np.float32).copy()


_cache = {}


def cached(key, fn):
    if key in _cache:
        return _cache[key][0].copy(), _cache[key][1]
    if len(_cache) > 24:
        _cache.pop(next(iter(_cache)))
    img, T = fn()
    _cache[key] = (img, T)
    return img.copy(), T


# ---------------- cafe (memory, warm afternoon) ----------------
def cafe(z=1.0, cx=320, cy=180):
    def build():
        from sh_street import render_street
        cv = Canvas(z, cx, cy)
        R, PG, LN, ELL = cv.R, cv.PG, cv.LN, cv.ELL
        R(-400, -200, 1040, 262, (236, 214, 182))
        for x in range(-400, 1040, 18):
            R(x, -200, x + 6, 210, (226, 202, 168))
        R(-400, 206, 1040, 262, (124, 80, 58))
        R(-400, 206, 1040, 210, (150, 100, 70))
        for x in range(-400, 1040, 60):
            R(x + 8, 216, x + 52, 256, (110, 70, 52))
        R(-400, 262, 1040, 600, (176, 140, 110))
        for i, x in enumerate(range(-400, 1040, 32)):
            for j, y in enumerate(range(262, 600, 16)):
                if (i + j) % 2 == 0:
                    R(x, y, x + 32, y + 16, (150, 110, 88))
        # big window
        R(120, 34, 520, 204, (110, 70, 50))
        img = cv.arr()
        # outside: dusk street (memory)
        ox0, oy0 = cv.T(128, 42); ox1, oy1 = cv.T(512, 196)
        ow, oh = int(round(ox1 - ox0)), int(round(oy1 - oy0))
        if ow > 4 and oh > 4:
            sz = 0.62 * z
            out, _ = render_street(1330 - (ow / 2) / sz, 150 - (oh * 0.62) / sz, sz, 'memory', t=0.0, wet=False, glow=False, ow=ow, oh=oh,
                                   state=dict(cinema=0.0, shops=1))
            out = out * 0.75 + np.array([255, 210, 160], np.float32) * 0.25
            X0, Y0 = int(round(ox0)), int(round(oy0))
            xs0, ys0 = max(0, X0), max(0, Y0)
            xs1, ys1 = min(W, X0 + ow), min(H, Y0 + oh)
            if xs1 > xs0 and ys1 > ys0:
                img[ys0:ys1, xs0:xs1] = out[ys0 - Y0:ys1 - Y0, xs0 - X0:xs1 - X0]
        cv.im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
        cv.d = ImageDraw.Draw(cv.im)
        for x in (252, 386):
            cv.R(x, 42, x + 8, 196, (110, 70, 50))
        cv.R(128, 116, 512, 122, (110, 70, 50))
        cv.R(112, 200, 528, 210, (140, 92, 64))
        # pendant lamp
        cv.LN([(320, -40), (320, 40)], (60, 44, 40), 1.4)
        cv.PG([(300, 58), (340, 58), (330, 40), (310, 40)], (60, 92, 74))
        cv.R(304, 58, 336, 61, (255, 230, 170))
        # plant, menu board
        cv.R(40, 150, 76, 206, (70, 56, 50))
        cv.R(44, 156, 72, 200, (40, 52, 44))
        cv.d.text(cv.T(46, 158), '', fill=(0, 0, 0))
        cv.R(560, 196, 590, 262, (160, 90, 70)); cv.ELL(575, 186, 24, 22, (80, 130, 84)); cv.ELL(560, 172, 14, 12, (96, 150, 96))
        img = cv.arr()
        # chalk menu text
        from sh_street import _put_text
        _put_text(img, '咖啡', cv.T, z, 58, 160, (230, 230, 220), 0.6)
        _put_text(img, '蛋糕', cv.T, z, 58, 178, (230, 230, 220), 0.6)
        lx, ly = cv.T(320, 62)
        stepped_glow(img, lx, ly, 120 * z, (255, 210, 150), k=0.22, levels=4)
        wx, wy = cv.T(320, 120)
        stepped_glow(img, wx, wy, 230 * z, (255, 220, 170), k=0.12, levels=3, sy=0.6)
        return img, cv.T
    return cached(('cafe', round(z, 3), cx, cy), build)


def cafe_table(img, T, z, cups=True):
    """round cafe table (side view) top at y=268, pedestal; two cups."""
    def r(x0, y0, x1, y1, c):
        a, b = T(x0, y0); cc, dd = T(x1, y1)
        img[m_rect(a, b, cc, dd)] = c
    r(272, 266, 368, 271, (120, 76, 52))
    r(272, 266, 368, 267, (160, 108, 74))
    r(316, 271, 324, 300, (80, 52, 40))
    r(298, 298, 342, 302, (80, 52, 40))
    if cups:
        for (x, c) in ((294, (250, 246, 240)), (346, (250, 246, 240))):
            r(x - 9, 264, x + 9, 266, (230, 226, 220))
            cup = m_rect(*T(x - 6, 255), *T(x + 6, 264))
            img[outline_of(cup)] = (90, 60, 50)
            img[cup] = c
            a, b = T(x - 5, 255); cc, dd = T(x + 5, 257)
            img[m_rect(a, b, cc, dd)] = (110, 60, 36)


def bentwood_chair(img, T, x, facing=1):
    def ln(p0, p1, w):
        img[m_line([T(*p0), T(*p1)], max(1, int(w)))] = (90, 56, 40)
    bx = x - facing * 18
    ln((bx, 230), (bx, 300), 2)
    ln((bx, 232), (bx + facing * 6, 226), 2)
    ln((x - 18, 278), (x + 18, 278), 3)
    ln((x + facing * 14, 278), (x + facing * 16, 300), 2)


# ---------------- salon mirror ----------------
def salon(z=1.0):
    def build():
        cv = Canvas(z)
        R, PG, LN, ELL = cv.R, cv.PG, cv.LN, cv.ELL
        R(-10, -10, 650, 370, (150, 186, 170))
        for x in range(0, 650, 22):
            LN([(x, 0), (x, 360)], (136, 172, 156), 1)
        for y in range(0, 360, 22):
            LN([(0, y), (640, y)], (136, 172, 156), 1)
        # mirror frame (round top)
        R(150, 70, 490, 300, (196, 160, 90))
        ELL(320, 80, 170, 64, (196, 160, 90))
        R(162, 82, 478, 300, (70, 86, 92))
        ELL(320, 88, 158, 56, (70, 86, 92))
        # reflected room inside mirror: back wall + window + chair back
        R(162, 82, 478, 300, (110, 128, 130))
        ELL(320, 88, 158, 56, (110, 128, 130))
        R(380, 110, 460, 200, (170, 196, 210))
        LN([(420, 110), (420, 200)], (120, 140, 150), 2)
        R(162, 236, 478, 300, (90, 104, 110))
        # counter
        R(0, 296, 640, 360, (236, 232, 226))
        R(0, 296, 640, 302, (210, 204, 196))
        for (x, c, hgt) in ((70, (120, 180, 220), 34), (96, (230, 120, 140), 26), (540, (200, 170, 90), 30), (572, (140, 200, 150), 22)):
            R(x - 7, 296 - hgt, x + 7, 296, c)
            R(x - 3, 296 - hgt - 6, x + 3, 296 - hgt, (60, 60, 70))
        img = cv.arr()
        # bulbs around the mirror
        for k in range(9):
            a = math.pi * (k / 8)
            bx, by = 320 - math.cos(a) * 176, 82 - math.sin(a) * 70
            p = cv.T(bx, by)
            img[m_ellipse(p[0], p[1], 5 * z, 5 * z)] = (255, 240, 200)
            stepped_glow(img, p[0], p[1], 22 * z, (255, 230, 170), k=0.3, levels=3)
        for side in (144, 496):
            for k in range(4):
                p = cv.T(side, 120 + k * 46)
                img[m_ellipse(p[0], p[1], 5 * z, 5 * z)] = (255, 240, 200)
                stepped_glow(img, p[0], p[1], 22 * z, (255, 230, 170), k=0.3, levels=3)
        return img, cv.T
    return cached(('salon', round(z, 3)), build)


def salon_mirror_mask(T):
    a, b = T(162, 82); cc, dd = T(478, 300)
    m = m_rect(a, b, cc, dd)
    c = T(320, 88)
    m |= m_ellipse(c[0], c[1], 158 * (cc - a) / 316, 56 * (cc - a) / 316)
    m &= m_rect(0, 0, W, T(0, 296)[1])
    return m


# ---------------- dance hall (warm neon) ----------------
def dancehall(z=1.0, cx=320, cy=180):
    def build():
        cv = Canvas(z, cx, cy)
        R, PG, LN, ELL = cv.R, cv.PG, cv.LN, cv.ELL
        R(-200, -200, 840, 560, (92, 26, 40))
        for i, x in enumerate(range(-200, 840, 120)):
            R(x + 20, 30, x + 100, 250, (120, 36, 52))
            ELL(x + 60, 30, 40, 30, (120, 36, 52))
            R(x + 30, 40, x + 90, 250, (70, 18, 32))
            ELL(x + 60, 40, 30, 22, (70, 18, 32))
            for k in range(4):
                LN([(x + 60 - 26 + k * 17, 46), (x + 60 - 26 + k * 17, 248)], (150, 110, 60), 1)
        R(-200, 250, 840, 262, (150, 110, 60))
        R(-200, 262, 840, 560, (60, 30, 36))
        for x in range(-200, 840, 40):
            LN([(x, 262), (x - 30, 360)], (74, 38, 44), 1)
        # small stage + band silhouettes (right)
        R(470, 210, 640, 262, (50, 20, 30))
        for (bx, hgt) in ((500, 48), (560, 56), (610, 44)):
            ELL(bx, 210 - hgt, 8, 9, (30, 10, 18))
            R(bx - 9, 210 - hgt + 8, bx + 9, 210, (30, 10, 18))
        LN([(560, 170), (574, 196), (566, 204)], (200, 160, 80), 3)   # sax
        img = cv.arr()
        from sh_street import _put_text
        sub = _put_text(img, '夜上海', cv.T, z, 320, 6, (255, 150, 210), 1.6)
        ys, xs = np.nonzero(sub)
        if len(xs):
            stepped_glow(img, xs.mean(), ys.mean(), 90 * z, (255, 110, 190), k=0.3, levels=3, sy=0.5)
        p = cv.T(320, 60)
        stepped_glow(img, p[0], p[1], 260 * z, (255, 190, 140), k=0.12, levels=4, sy=0.7)
        return img, cv.T
    return cached(('dance', round(z, 3), cx, cy), build)


def disco(img, T, z, t):
    cx, cy = T(320, 66)
    r = 14 * z
    img[m_ellipse(cx, cy, r, r)] = (200, 200, 210)
    ph = tq(t, 12)
    for i in range(14):
        a = i / 14 * 2 * math.pi + ph * 1.4
        x = cx + math.cos(a) * r * 0.7
        y = cy + math.sin(a * 2) * r * 0.5
        img[m_rect(x - 1, y - 1, x + 2, y + 2)] = (255, 255, 255) if (i + int(ph * 12)) % 3 else (180, 180, 200)
    for i in range(10):
        a = h01(i, 2) * 2 * math.pi + ph * 0.8
        x = cx + math.cos(a) * (120 + 160 * h01(i, 5)) * z
        y = cy + abs(math.sin(a)) * (60 + 150 * h01(i, 7)) * z
        if 0 <= x < W and 0 <= y < H:
            img[m_rect(x - 1, y - 1, x + 2, y + 2)] = (255, 240, 220)


# ---------------- dining room (night, waiting) ----------------
def dining(z=1.0):
    def build():
        cv = Canvas(z)
        R, PG, LN, ELL = cv.R, cv.PG, cv.LN, cv.ELL
        R(-10, -10, 650, 370, (70, 80, 108))
        for x in range(0, 650, 26):
            R(x, 0, x + 2, 250, (62, 72, 98))
        R(0, 236, 640, 262, (60, 50, 56))
        R(0, 262, 640, 360, (52, 44, 50))
        # window with rain (left)
        R(40, 60, 170, 200, (90, 80, 70))
        R(48, 68, 162, 192, (22, 26, 46))
        LN([(105, 68), (105, 192)], (90, 80, 70), 3); LN([(48, 130), (162, 130)], (90, 80, 70), 3)
        # sideboard (right) with photo frame
        R(500, 190, 620, 262, (90, 64, 52))
        R(530, 160, 560, 190, (200, 180, 150)); R(534, 164, 556, 186, (240, 200, 210))
        img = cv.arr()
        # hanging lamp cone
        lx, ly = cv.T(330, 120)
        stepped_glow(img, lx, ly, 200 * z, (255, 200, 140), k=0.22, levels=4, sy=0.8)
        cv2 = cv
        return img, cv.T
    return cached(('dining', round(z, 3)), build)


def wall_clock(img, T, z, x, y, r, hh, mm, ss=None):
    c = T(x, y)
    R = r * z
    img[m_ellipse(c[0], c[1], R + 2 * z, R + 2 * z)] = (90, 64, 50)
    img[m_ellipse(c[0], c[1], R, R)] = (236, 228, 210)
    for k in range(12):
        a = k / 12 * 2 * math.pi
        p0 = (c[0] + math.sin(a) * R * 0.86, c[1] - math.cos(a) * R * 0.86)
        img[m_ellipse(p0[0], p0[1], max(1, z * 0.8), max(1, z * 0.8))] = (60, 50, 50)
    ah = ((hh % 12) + mm / 60) / 12 * 2 * math.pi
    am = mm / 60 * 2 * math.pi
    for ang, L, w in ((ah, 0.5, 2.0), (am, 0.78, 1.4)):
        img[m_line([c, (c[0] + math.sin(ang) * R * L, c[1] - math.cos(ang) * R * L)], max(1, int(w * z)))] = (40, 30, 30)
    if ss is not None:
        a = ss / 60 * 2 * math.pi
        img[m_line([c, (c[0] + math.sin(a) * R * 0.84, c[1] - math.cos(a) * R * 0.84)], 1)] = (200, 40, 50)


# ---------------- bedroom (packing) ----------------
def bedroom(z=1.0, cx=320, cy=180, w=W):
    def build():
        cv = Canvas(z, cx, cy, w=w)
        R, PG, LN, ELL = cv.R, cv.PG, cv.LN, cv.ELL
        R(-200, -200, 840, 560, (96, 82, 110))
        for x in range(-200, 840, 30):
            R(x, -200, x + 3, 250, (88, 74, 102))
        R(-200, 250, 840, 560, (70, 56, 62))
        # bed
        R(80, 210, 560, 262, (210, 200, 220))
        R(80, 200, 560, 214, (240, 236, 244))
        R(70, 150, 90, 262, (110, 76, 60))
        R(80, 160, 180, 200, (250, 246, 250))
        # lamp
        R(580, 200, 620, 262, (90, 64, 52))
        PG([(588, 168), (612, 168), (618, 196), (582, 196)], (240, 210, 160))
        img = cv.arr()
        p = cv.T(600, 182)
        stepped_glow(img, p[0], p[1], 160 * z, (255, 200, 140), k=0.25, levels=4)
        return img, cv.T
    return cached(('bed', round(z, 3), cx, cy, w), build)
