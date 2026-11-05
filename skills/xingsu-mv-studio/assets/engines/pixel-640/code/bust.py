# -*- coding: utf-8 -*-
"""HER close-up bust, drawn directly on the pixel grid with finer features (eyes w/ iris + highlights, brows, lashes)."""
import numpy as np, math, functools
from core import *
from sprite import SB, ramp
from chars import PAL


def her_bust(s=4.0, pal='room', expr='calm', look=(0.0, 0.0), blink=0.0, tear=0.0, hat=False, hand_chest=False,
             glow_hand=0.0, mouth=0.0, tilt=0.0, palm_out=0.0):
    """units: head ~ 0..20 tall; canvas covers shoulders. look=(dx,dy) pupils offset -1..1. blink 0..1"""
    P_ = PAL[pal]
    sk, hr = P_['hskin'], P_['hhair']
    b = SB(s, wu=60, hu=56, oxu=30, top_u=-8)
    # shoulders / cardigan / dress collar
    body = b.m_poly([(-19, 46), (-17, 34), (-11, 29.0), (-4, 26.8), (4, 26.8), (11, 29.0), (17, 34), (19, 46)])
    b.part('body', body, P_['card'], hl=0.2, sh=0.3, light=-1)
    for sg in (-1, 1):
        b.paint(b.m_line([(sg * 13.5, 34), (sg * 14.5, 44)], 0.3) & body, P_['card'][1])
    neckv = b.m_poly([(-4.2, 26.4), (4.2, 26.4), (2.6, 33), (0, 35.5), (-2.6, 33)])
    b.part('dressv', neckv, P_['dress'], shade='flat')
    for sg in (-1, 1):
        col = b.m_poly([(sg * 4.4, 26.2), (sg * 9.6, 28.0), (sg * 7.0, 31.5), (sg * 3.0, 35.0)])
        b.paint(col, P_['card'][2])
        b.paint(outline_of(col) & body, P_['card'][1])
    b.part('neck', b.m_poly([(-2.6, 20), (2.6, 20), (2.8, 27.4), (-2.8, 27.4)]), ramp(sk[1], sk[1] * 0.9, sk[0]), shade='flat')
    b.paint(b.m_poly([(-2.8, 20), (2.8, 20), (2.8, 22.4), (-2.8, 22.4)]), sk[1] * 0.85)
    # hair back mass
    hb = b.m_poly([(-10.6, 4), (-11.6, 14), (-11.8, 25), (-9, 27.8), (-5.5, 26), (5.5, 26), (9, 27.8), (11.8, 25), (11.6, 14), (10.6, 4)])
    b.part('hairback', hb, ramp(hr[1], hr[1] * 0.85, hr[0]), shade='flat')
    # face
    face = b.m_poly([(-8.6, 6), (-8.8, 11), (-8.0, 15.4), (-5.6, 19.0), (-2.4, 21.0), (0, 21.4), (2.4, 21.0), (5.6, 19.0), (8.0, 15.4), (8.8, 11), (8.6, 6), (6, 1.2), (-6, 1.2)])
    b.part('face', face, sk, hl=0.16, sh=0.22, light=-1)
    # cheek shadow under hair on right
    b.paint(face & b.m_poly([(5.2, 4), (9, 4), (9, 18), (6.4, 17.6)]), sk[1])
    # eyes
    ey = 11.6
    for sg in (-1, 1):
        ex = sg * 3.9
        if blink >= 0.85 or expr == 'smile':
            # closed / smiling arcs
            if expr == 'smile' and blink < 0.85:
                b.paint(b.m_line([(ex - 1.8, ey + 0.6), (ex - 0.6, ey - 0.5), (ex + 0.6, ey - 0.5), (ex + 1.8, ey + 0.6)], 0.5), P_['eye'])
            else:
                b.paint(b.m_line([(ex - 1.8, ey + 0.3), (ex, ey + 0.8), (ex + 1.8, ey + 0.3)], 0.5), P_['eye'])
        else:
            hgt = 2.4 * (1 - blink * 0.8)
            if expr == 'surprise':
                hgt *= 1.15
            white = b.m_ell(ex, ey, 1.9, hgt)
            b.paint(white, (250, 246, 244))
            ix = ex + look[0] * 0.5
            iy = ey + look[1] * 0.4 + 0.2
            iris = b.m_ell(ix, iy, 1.45, min(hgt, 2.0)) & white
            b.paint(iris, (96, 60, 56))
            b.paint(b.m_ell(ix, iy + 0.5, 1.45, min(hgt, 2.0) * 0.55) & iris, (130, 84, 70))
            b.paint(b.m_ell(ix, iy - 0.1, 0.7, 1.0) & iris, (36, 22, 26))
            b.paint(b.m_ell(ix - 0.55, iy - 0.75, 0.42, 0.42) & white, (255, 255, 255))
            b.paint(b.m_ell(ix + 0.6, iy + 0.7, 0.25, 0.25) & white, (240, 232, 240))
            # upper lash line (thicker), outer flick
            up = white & ~shift(white, 0, max(1, int(s * 0.35)))
            b.paint(up, P_['eye'])
            b.paint(b.m_line([(ex + sg * 1.6, ey - 1.4), (ex + sg * 2.4, ey - 1.9)], 0.35), P_['eye'])
            if tear > 0:
                ty = ey + hgt + 0.2 + tear * 4.2
                b.paint(b.m_ell(ex + sg * 0.6, ey + hgt - 0.1, 1.6, 0.5), (200, 230, 255))
                if tear > 0.2:
                    b.paint(b.m_ell(ex + sg * 1.2, ty, 0.45, 0.75), (190, 226, 255))
                    b.paint(b.m_ell(ex + sg * 1.1, ty - 0.2, 0.18, 0.18), (255, 255, 255))
        # brows
        by = ey - 3.6 - (0.5 if expr == 'surprise' else 0)
        if expr in ('sad', 'teary'):
            b.paint(b.m_line([(ex - sg * 1.6, by + 0.2), (ex + sg * 1.4, by + 0.9)], 0.45), hr[1])
        else:
            b.paint(b.m_line([(ex - sg * 1.6, by + 0.5), (ex, by), (ex + sg * 1.6, by + 0.4)], 0.45), hr[1])
        # blush
        b.paint(b.m_ell(sg * 5.6, ey + 3.8, 1.7, 0.75), P_['blush'])
        if s >= 3:
            for k in (-1, 0, 1):
                b.paint(b.m_line([(sg * 5.6 + k * 0.9 - 0.3, ey + 3.5), (sg * 5.6 + k * 0.9 + 0.3, ey + 4.0)], 0.2), np.asarray(P_['blush'], np.float32) * 0.85)
    # nose
    b.paint(b.m_line([(0.4, 15.1), (0.9, 15.6)], 0.3), sk[1] * 0.92)
    # mouth
    my = 17.6
    if expr in ('smile', 'soft'):
        b.paint(b.m_line([(-1.6, my - 0.3), (-0.5, my + 0.4), (0.5, my + 0.4), (1.6, my - 0.3)], 0.4), (176, 92, 96))
        if mouth > 0:
            b.paint(b.m_ell(0, my + 0.6, 1.1, 0.6 * mouth), (200, 110, 112))
    elif expr == 'surprise':
        b.paint(b.m_ell(0, my + 0.3, 0.8, 0.95), (160, 80, 86))
    elif expr in ('sad', 'teary'):
        b.paint(b.m_line([(-1.3, my + 0.4), (0, my), (1.3, my + 0.4)], 0.4), (170, 96, 100))
    else:
        b.paint(b.m_line([(-1.0, my), (1.0, my)], 0.4), (176, 104, 106))
    # hair: top + bangs + side locks, strand lines
    top = b.m_poly([(-10, 11), (-10.4, 5), (-8.2, 0.4), (-4.2, -2.2), (0, -2.8), (4.2, -2.2), (8.2, 0.4), (10.4, 5), (10, 11), (8.6, 7.4),
                    (7.6, 8.2), (6.4, 6.9), (5.0, 7.8), (3.6, 6.6), (2.2, 7.7), (0.8, 6.5), (-0.6, 7.7), (-2.0, 6.6), (-3.4, 7.7), (-4.8, 6.6),
                    (-6.2, 7.8), (-7.4, 6.8), (-8.6, 7.6)])
    b.part('hairtop', top, hr, hl=0.22, sh=0.28, light=-1)
    for sg in (-1, 1):
        lock = b.m_poly([(sg * 9.4, 4), (sg * 11.0, 10), (sg * 11.6, 18), (sg * 11.2, 25.6), (sg * 9.2, 27.6), (sg * 8.0, 24), (sg * 8.4, 17),
                         (sg * 8.6, 10), (sg * 8.2, 6.5)])
        b.part('lock%d' % sg, lock, hr, hl=0.25, sh=0.3, light=-1)
        b.paint(b.m_line([(sg * 9.8, 9), (sg * 10.4, 18), (sg * 9.8, 24)], 0.3) & lock, hr[1])
    for (x0, y0, x1, y1) in ((-6, -1.0, -7.6, 4.6), (-2.6, -2.0, -3.2, 4.4), (1.8, -2.2, 2.6, 4.0), (5.4, -1.2, 6.8, 4.4)):
        b.paint(b.m_line([(x0, y0), (x1, y1)], 0.3) & top, hr[1])
    # sheen band
    sheen = b.m_line([(-6.6, 0.6), (-3, -0.9), (1, -1.3)], 0.6) & top
    b.paint(sheen, hr[2] * 1.12)
    # yellow clip
    clip = b.m_poly([(4.4, 1.0), (8.4, -0.4), (9.0, 1.4), (5.0, 2.8)])
    b.part('clip', clip, P_['yellow'], shade='flat')
    b.paint(inner_edge(clip, 0, -1), P_['yellow'][2])
    if hat:
        # his fedora on her head (too big, cute)
        crown = b.m_poly([(-9.2, -3.0), (-3.4, -7.4), (0, -6.2), (3.4, -7.4), (9.2, -3.0), (10, 3.4), (-10, 3.4)])
        brim = b.m_ell(0, 3.8, 18, 2.6)
        b.part('brim', brim, P_['hat'], shade='cyl', hl=0.12, sh=0.3)
        b.part('crown', crown, P_['hat'], hl=0.2, sh=0.3)
        b.part('band', crown & b.m_poly([(-10, 0.6), (10, 0.6), (10, 3.4), (-10, 3.4)]), P_['band'], shade='flat')
    if hand_chest:
        hand = b.m_poly([(-6, 36), (-1, 33.6), (3.6, 34.4), (5.6, 37), (4, 40.4), (-3, 41.2), (-6.4, 39.4)])
        b.part('hand', hand, P_['hskin'], hl=0.25, sh=0.3)
        for k in range(3):
            b.paint(b.m_line([(-2.4 + k * 2.0, 34.6), (-1.8 + k * 2.0, 37.6)], 0.25) & hand, P_['hskin'][1])
        b.part('sleeve', b.m_poly([(-14, 46), (-11, 38), (-6, 36.6), (-6.4, 41.4), (-9, 46)]), P_['card'], hl=0.2, sh=0.3)
    if palm_out > 0:
        # right forearm reaching forward/down to an open palm (palm up)
        k = palm_out
        wx, wy = 12 + 3 * k, 34 + 4 * k
        sleeve = b.m_cap((11.5, 31), (wx, wy), 3.2, 2.6)
        b.part('rsleeve', sleeve, P_['card'], hl=0.2, sh=0.35, light=-1)
        palm = b.m_ell(wx + 0.6, wy + 2.4, 3.6, 1.7)
        b.part('palm', palm, P_['hskin'], shade='top')
        for q in range(4):
            b.paint(b.m_line([(wx - 1.8 + q * 1.3, wy + 1.6), (wx - 2.2 + q * 1.4, wy + 0.6)], 0.25), P_['hskin'][1])
        b.part('thumbp', b.m_cap((wx - 2.6, wy + 2.4), (wx - 4.0, wy + 1.0), 0.8), P_['hskin'], shade='flat')
    b.sil |= body
    spr = b.finish(outline=P_['houtline'], rim=(1, 0, P_['rim'], max(1, int(s * 0.5))))
    return spr, (b.X(0), b.Y(0)), b
