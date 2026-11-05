# -*- coding: utf-8 -*-
"""The little cloud (from the album cover) + warm 'longing' drops."""
import numpy as np, math, functools
from core import *
from sprite import SB, ramp

CL_L = C('#f6f7ff'); CL_B = C('#d9ddf0'); CL_S = C('#aab2d4'); CL_D = C('#7f87b2'); CL_O = C('#3c3f63')
WARM = C('#ffcf7a'); WARM_HI = C('#fff2c8')


@functools.lru_cache(maxsize=256)
def cloud_sprite(s, mood=0.0, breath=0, lit=(-1, -1), tint=None):
    """s: px per unit (cloud ~44 units wide). mood 0 = fluffy, 1 = sad/droopy. breath: 0..3 puff phase."""
    b = SB(s, wu=56, hu=34, oxu=28, top_u=-20)
    br = [0, 0.6, 1.0, 0.6][breath % 4]
    sq = 1 - 0.18 * mood
    puffs = [(-11, 1, 8.2), (-2, -4.5, 10.5 + br * 0.4), (9, -1, 8.6), (16, 3.5, 6.0), (-18, 4.5, 5.6), (3, 2, 9)]
    m = np.zeros((b.H, b.W), bool)
    for (x, y, r) in puffs:
        m |= b.m_ell(x, y * sq + mood * 2.5, r + br * 0.25, r * sq + br * 0.2)
    m |= b.m_poly([(-21, 5 + mood * 2), (21, 5 + mood * 2), (19, 9.5 + mood * 1.5), (-19, 9.5 + mood * 1.5)])
    pal = (CL_B, CL_S, CL_L) if tint is None else tuple(np.asarray(c, np.float32) * np.asarray(tint, np.float32) for c in (CL_B, CL_S, CL_L))
    b.col[m] = pal[0]
    # light from top-left: each puff's top-left crescent
    for (x, y, r) in puffs:
        pm = b.m_ell(x, y * sq + mood * 2.5, r + br * 0.25, r * sq + br * 0.2)
        inner = b.m_ell(x + r * 0.22, y * sq + mood * 2.5 + r * 0.22, r * 0.95, r * sq * 0.95)
        b.col[pm & ~inner & m] = pal[2]
    # bottom shadow band
    bot = m & ~shift(m, 0, -max(2, int(3.2 * s)))
    b.col[bot] = pal[1]
    bot2 = m & ~shift(m, 0, -max(1, int(1.2 * s)))
    b.col[bot2] = CL_D if tint is None else CL_D * np.asarray(tint, np.float32)
    # puff separation lines (subtle)
    if s >= 1.5:
        for (x, y, r) in puffs[:3]:
            pm = b.m_ell(x, y * sq + mood * 2.5, r, r * sq)
            e = outline_of(pm) & m & ~bot
            b.col[e & (np.arange(b.H)[:, None] > b.Y(y * sq + mood * 2.5))] = pal[1]
    b.sil = m
    spr = b.finish(outline=CL_O * (1 if tint is None else np.asarray(tint, np.float32)))
    ax, ay = b.X(0), b.Y(0)
    return spr, (ax, ay), (b.X(-19) - ax, b.X(19) - ax, b.Y(9.5) - ay)


def draw_cloud(img, x, y, s, t=0.0, mood=0.0, bob=True, a=1.0, tint=None):
    br = int(tq(t, 4) * 4) % 4
    spr, (ax, ay), ext = cloud_sprite(round(s, 2), round(mood, 1), br, tint=tint)
    dy = int(round(math.sin(t * 2.2) * 1.2 * s)) if bob else 0
    blit(img, spr, int(round(x - ax)), int(round(y - ay + dy)), a)
    return (x + ext[0], x + ext[1], y + ext[2] + dy)


def cloud_rain(img, t, x0, x1, ytop, ybot, density=1.0, seed=7, color=(200, 212, 240), speed=420, length=7, heavier=1.0):
    """rain column under the little cloud (screen space)."""
    T = tq(t, 12)
    n = int((x1 - x0) * 0.35 * density * heavier)
    col = np.asarray(color, np.float32)
    span = max(1, ybot - ytop)
    for i in range(n):
        r1, r2 = h01(i, seed), h01(seed, i, 3)
        y = ytop + ((r2 * span + speed * T * (0.85 + 0.3 * h01(i, 9))) % span)
        x = x0 + r1 * (x1 - x0) + (y - ytop) * 0.05
        for k in range(length):
            yy, xx = int(y + k), int(x + k * 0.05)
            if 0 <= yy < img.shape[0] and 0 <= xx < img.shape[1] and yy < ybot:
                a = 0.75 if k > length // 3 else 0.4
                img[yy, xx] = img[yy, xx] * (1 - a) + col * a


def warm_drop(img, x, y, r=3.0, glow=1.0, a=1.0):
    """glowing teardrop of 'longing'"""
    x, y = int(round(x)), int(round(y))
    if glow > 0:
        stepped_glow(img, x, y, r * 6, (255, 190, 100), k=0.55 * glow * a, levels=4)
    m = m_ellipse(x, y, r, r * 1.05, img.shape[1], img.shape[0])
    tip = m_poly([(x - r * 0.75, y - r * 0.3), (x, y - r * 2.6), (x + r * 0.75, y - r * 0.3)], img.shape[1], img.shape[0])
    mm = m | tip
    fill(img, mm, WARM, a)
    fill(img, inner_edge(mm, 1, 1) & mm, C('#e89a4a'), a)
    hi = m_ellipse(x - r * 0.35, y - r * 0.3, max(1, r * 0.3), max(1, r * 0.35), img.shape[1], img.shape[0])
    fill(img, hi, WARM_HI, a)
