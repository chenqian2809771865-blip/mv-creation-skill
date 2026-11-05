# -*- coding: utf-8 -*-
"""Close-up hands in pixel style: capsule fingers/thumb with nail, joint crease, 3-tone shading and a soft brown outline.
All shapes are built in a local frame (u along the digit from base to tip, v across; +v = shadow side) then rotated."""
import numpy as np, math
from core import *

SKIN = dict(base=(236, 192, 162), shade=(204, 152, 128), deep=(172, 120, 102), light=(250, 216, 190),
            line=(84, 48, 44), nail=(248, 220, 206), nail_sh=(222, 172, 160))


def _pal(light=1.0, warm=(1.0, 1.0, 1.0)):
    w = np.asarray(warm, np.float32)
    return {k: np.clip(np.asarray(v, np.float32) * light * w, 0, 255) for k, v in SKIN.items()}


def _xf(base, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    bx, by = base
    return lambda u, v: (bx + u * ca - v * sa, by + u * sa + v * ca)


def digit_mask(base, ang, L, w0, w1, n=10):
    """capsule from base (width w0) to tip (width w1) with a round tip"""
    P = _xf(base, ang)
    pts = [P(0, -w0 / 2), P(L - w1 / 2, -w1 / 2)]
    for i in range(1, n):
        a = -math.pi / 2 + math.pi * i / n
        pts.append(P(L - w1 / 2 + math.cos(a) * w1 / 2, math.sin(a) * w1 / 2))
    pts += [P(L - w1 / 2, w1 / 2), P(0, w0 / 2)]
    return m_poly(pts)


def draw_digit(img, base, ang, L, w0, w1, pal=None, nail=True, crease=(0.5,), outline=True, clip=None, soft=None, cap=0.0):
    """one finger / thumb. ang: radians (0 = pointing right, -pi/2 = up).
    soft: mask where the outline becomes a soft crease (e.g. over the palm); cap: no outline for the first `cap` px (base blends in)."""
    pal = pal or _pal()
    P = _xf(base, ang)
    m = digit_mask(base, ang, L, w0, w1)
    if clip is not None:
        m &= clip
    if outline:
        ol = outline_of(m) & ~m
        if cap > 0:
            wm = max(w0, w1)
            ol &= ~m_poly([P(-wm, -wm), P(cap, -wm), P(cap, wm), P(-wm, wm)])
        if soft is not None:
            fill(img, ol & soft, pal['shade'])
            ol &= ~soft
        fill(img, ol, pal['line'])
    fill(img, m, pal['base'])
    # shadow side (+v) and lit edge (-v)
    wm = max(w0, w1)
    sh = m_poly([P(-2, wm * 0.14), P(L + 4, wm * 0.10), P(L + 4, wm), P(-2, wm)]) & m
    fill(img, sh, pal['shade'])
    deep = m_poly([P(-2, wm * 0.36), P(L + 4, wm * 0.30), P(L + 4, wm), P(-2, wm)]) & m
    fill(img, deep, pal['deep'])
    lit = m_poly([P(2, -wm), P(L - w1 * 0.4, -wm), P(L - w1 * 0.4, -wm * 0.36), P(2, -wm * 0.40)]) & m
    fill(img, lit & ~shift(lit, 0, 1) & ~shift(lit, 1, 0), pal['light'])
    for cu in crease:
        u = L * cu
        wc = w0 + (w1 - w0) * cu
        img[m_line([P(u - 1.5, -wc * 0.30), P(u + 1.0, -wc * 0.02), P(u - 0.5, wc * 0.26)], 1) & m] = pal['deep']
    if nail:
        u0, u1 = L - w1 * 1.25, L - w1 * 0.16
        nm = m_poly([P(u0, -w1 * 0.30), P(u1 - w1 * 0.12, -w1 * 0.30), P(u1, -w1 * 0.14), P(u1, w1 * 0.10),
                     P(u1 - w1 * 0.12, w1 * 0.24), P(u0, w1 * 0.24)]) & m
        fill(img, nm, pal['nail'])
        fill(img, outline_of(nm) & m, pal['nail_sh'])
        hl = m_line([P(u0 + 2, -w1 * 0.16), P(u1 - 3, -w1 * 0.16)], 1) & nm
        fill(img, hl, np.minimum(255, pal['nail'] * 1.04 + 8))
    return m


def draw_blob(img, pts, pal=None, shade_dir=(0.6, 0.8), outline=True, behind=None):
    """palm / back of hand: polygon with an inner shadow band on the shade_dir side.
    behind: mask of digits drawn earlier — the blob covers their bases and its outline skips them."""
    pal = pal or _pal()
    m = m_poly(pts)
    if outline:
        ol = outline_of(m) & ~m
        if behind is not None:
            ol &= ~behind
        fill(img, ol, pal['line'])
    fill(img, m, pal['base'])
    dx, dy = shade_dir
    k = 6
    inner = m.copy()
    for _ in range(k):
        inner = inner & shift(inner, int(round(-dx)), int(round(-dy)))
    fill(img, m & ~inner, pal['shade'])
    return m
