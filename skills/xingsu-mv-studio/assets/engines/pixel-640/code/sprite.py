# -*- coding: utf-8 -*-
"""Sprite builder: parts drawn in 'units' (0..100 = hat-top..feet) at any pixel scale, aliased;
cylinder shading per part, selective outline, rim light. Output RGBA float sprite + anchor (feet)."""
import numpy as np, math
from core import *


def ramp(base, sh=None, li=None):
    b = np.asarray(base, np.float32)
    sh = b * 0.68 if sh is None else np.asarray(sh, np.float32)
    li = np.minimum(255, b * 1.22 + 10) if li is None else np.asarray(li, np.float32)
    return (b, sh, li)


def _runs_u(m, axis=1):
    """normalized position across runs along axis (0..1), -1 outside"""
    mm = m if axis == 1 else m.T
    h, w = mm.shape
    u = np.full((h, w), -1.0, np.float32)
    for y in range(h):
        row = mm[y]
        if not row.any():
            continue
        d = np.diff(np.r_[0, row.astype(np.int8), 0])
        st = np.where(d == 1)[0]
        en = np.where(d == -1)[0]
        for a, b in zip(st, en):
            n = b - a
            u[y, a:b] = (np.arange(n) + 0.5) / n
    return u if axis == 1 else u.T


class SB:
    def __init__(self, s, wu=90, hu=112, oxu=45, top_u=-6):
        """s: px per unit. canvas covers x in [-oxu, wu-oxu] units, y in [top_u, top_u+hu] units"""
        self.s = s
        self.oxu, self.top_u = oxu, top_u
        self.W = int(math.ceil(wu * s)) + 6
        self.H = int(math.ceil(hu * s)) + 6
        self.col = np.zeros((self.H, self.W, 3), np.float32)
        self.sil = np.zeros((self.H, self.W), bool)
        self.parts = {}
        self.outline_col = {}

    def X(self, x):
        return 3 + (x + self.oxu) * self.s

    def Y(self, y):
        return 3 + (y - self.top_u) * self.s

    def pts(self, P):
        return [(self.X(x), self.Y(y)) for x, y in P]

    def anchor(self):
        """pixel of unit (0,100) - feet centre"""
        return self.X(0), self.Y(100)

    # ---- shapes -> masks ----
    def m_poly(self, P):
        return m_poly(self.pts(P), self.W, self.H)

    def m_ell(self, cx, cy, rx, ry):
        return m_ellipse(self.X(cx), self.Y(cy), rx * self.s, ry * self.s, self.W, self.H)

    def m_cap(self, p0, p1, r0, r1=None, n=8):
        r1 = r0 if r1 is None else r1
        (x0, y0), (x1, y1) = p0, p1
        a = math.atan2(y1 - y0, x1 - x0)
        P = []
        for i in range(n + 1):
            th = a + math.pi / 2 + math.pi * i / n
            P.append((x0 + r0 * math.cos(th), y0 + r0 * math.sin(th)))
        for i in range(n + 1):
            th = a - math.pi / 2 + math.pi * i / n
            P.append((x1 + r1 * math.cos(th), y1 + r1 * math.sin(th)))
        return self.m_poly(P)

    def m_line(self, P, wu=0.0):
        wpx = max(1, int(round(wu * self.s)))
        return m_line(self.pts(P), wpx, self.W, self.H)

    # ---- painting ----
    def part(self, name, m, rp, shade='cyl', light=-1, hl=0.22, sh=0.36, axis=1, clip=None, outline=None):
        if clip is not None:
            m = m & clip
        if not m.any():
            return m
        b, s_, l = rp
        self.col[m] = b
        if shade == 'cyl':
            u = _runs_u(m, axis)
            if light < 0:
                self.col[m & (u < hl) & (u >= 0)] = l
                self.col[m & (u > 1 - sh)] = s_
            else:
                self.col[m & (u > 1 - hl)] = l
                self.col[m & (u < sh) & (u >= 0)] = s_
        elif shade == 'top':
            self.col[inner_edge(m, 0, -1, max(1, int(self.s * 0.9)))] = l
            self.col[inner_edge(m, 0, 1, max(1, int(self.s * 1.2)))] = s_
        elif shade == 'shadow':
            self.col[m] = s_
        self.sil |= m
        self.parts[name] = m
        if outline is not None:
            self.outline_col[name] = outline
        return m

    def paint(self, m, color, clip=None):
        if clip is not None:
            m = m & clip
        self.col[m] = color
        return m

    def sep(self, a, b, color):
        """separation line where part b borders part a (drawn on b)"""
        if a in self.parts and b in self.parts:
            e = outline_of(self.parts[a]) & self.parts[b]
            self.col[e] = color

    def finish(self, outline=(14, 12, 20), rim=None, rim2=None, out_w=1):
        """rim=(dx,dy,color,width) on silhouette inner edge"""
        if rim is not None:
            dx, dy, c, w = rim
            e = inner_edge(self.sil, dx, dy, w)
            self.col[e] = mix(self.col[e], c, 0.85)
        if rim2 is not None:
            dx, dy, c, w = rim2
            e = inner_edge(self.sil, dx, dy, w)
            self.col[e] = mix(self.col[e], c, 0.6)
        o = outline_of(self.sil)
        spr = np.zeros((self.H, self.W, 4), np.float32)
        spr[..., :3] = self.col
        spr[..., 3] = self.sil
        if outline is not None:
            spr[o, :3] = outline
            spr[o, 3] = 1.0
        return spr


def place(img, spr, anchor, x, y, a=1.0, flip=False):
    """blit sprite so that its anchor lands on (x,y)"""
    ax, ay = anchor
    if flip:
        spr = spr[:, ::-1]
        ax = spr.shape[1] - 1 - ax
    blit(img, spr, int(round(x - ax)), int(round(y - ay)), a)


def tint_sprite(spr, mul=(1, 1, 1), add_=(0, 0, 0)):
    out = spr.copy()
    out[..., :3] = np.clip(out[..., :3] * np.asarray(mul, np.float32) + np.asarray(add_, np.float32), 0, 255)
    return out


def layer(spr, anc, x, y, flip=False, w=None, h=None, out=None, mask=None):
    """render sprite into full-frame (rgb, mask) buffers"""
    from core import W as _W, H as _H
    w = _W if w is None else w
    h = _H if h is None else h
    if out is None:
        out = np.zeros((h, w, 3), np.float32)
    if mask is None:
        mask = np.zeros((h, w), bool)
    ax, ay = anc
    if flip:
        spr = spr[:, ::-1]
        ax = spr.shape[1] - 1 - ax
    X, Y = int(round(x - ax)), int(round(y - ay))
    sh, sw = spr.shape[:2]
    x0, y0, x1, y1 = max(0, X), max(0, Y), min(w, X + sw), min(h, Y + sh)
    if x1 > x0 and y1 > y0:
        s = spr[y0 - Y:y1 - Y, x0 - X:x1 - X]
        m = s[..., 3] > 0.5
        reg = out[y0:y1, x0:x1]
        reg[m] = s[..., :3][m]
        mask[y0:y1, x0:x1] |= m
    return out, mask
