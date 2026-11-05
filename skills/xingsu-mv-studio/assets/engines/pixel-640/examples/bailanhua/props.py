# -*- coding: utf-8 -*-
"""Props: umbrella, white-orchid pair (Shanghai 白兰花 on a wire), phone, taxi, tickets; NPC walkers; helpers."""
import numpy as np, math, functools
from core import *
from sprite import SB, ramp, place
from chibi import HIM, HER, LIGHT, _lit

ORCHID = (250, 248, 232)
ORCHID_SH = (214, 210, 184)
LEAF = (86, 136, 92)


def shape(img, m, color, outline=None, a=1.0):
    if outline is not None:
        fill(img, outline_of(m) & ~m, outline, a)
    fill(img, m, color, a)


@functools.lru_cache(maxsize=64)
def UMB(s, col=(60, 64, 96), light='night', open_=1.0):
    c = _lit(col, light)
    b = SB(s, wu=60, hu=62, oxu=30, top_u=0)
    b.part('shaft', b.m_line([(0, 4), (0, 50)], 0.9), ramp((70, 60, 60)), shade='flat')
    b.part('handle', b.m_line([(0, 48), (0, 52), (1.6, 54.4), (3.6, 54), (3.8, 52.4)], 1.6), ramp((110, 70, 50)), shade='flat')
    R = 24 * (0.4 + 0.6 * open_)
    hgt = 12
    pts = []
    n = 6
    for i in range(n + 1):
        x = -R + 2 * R * i / n
        pts.append((x, 4 + hgt))
        if i < n:
            pts.append((x + R / n, 4 + hgt - 2.0))
    top = [(R * math.cos(a), 4 + hgt - hgt * math.sin(a)) for a in np.linspace(0, math.pi, 24)]
    canopy = b.m_poly(top + list(reversed(pts)))
    b.part('canopy', canopy, (c, c * 0.7, np.minimum(255, c * 1.25 + 8)), hl=0.18, sh=0.3, light=-1)
    for i in range(1, n):
        x = -R + 2 * R * i / n
        b.paint(b.m_line([(0, 4), (x * 0.95, 4 + hgt - 1.4)]) & canopy, c * 0.7)
    b.part('tip', b.m_line([(0, 4), (0, 1.5)], 0.9), ramp((80, 70, 70)), shade='flat')
    spr = b.finish(outline=(16, 14, 22))
    return spr, (b.X(0), b.Y(50))


def umbrella(img, x, y, s, col=(60, 64, 96), light='night', a=1.0):
    """(x,y) = handle grip point on screen"""
    spr, anc = UMB(round(s, 3), col, light)
    blit(img, spr, int(round(x - anc[0])), int(round(y - anc[1])), a)


def orchid_pair(img, cx, cy, s=1.0, glow=0.0, light=1.0, angle=0.0, n=2):
    """Shanghai 白兰花: two slim ivory buds tied on a thin wire with a green leaf. ~ (16*s) px long. (cx,cy)=wire centre."""
    Hh, Ww = img.shape[:2]
    ca, sa = math.cos(angle), math.sin(angle)
    P = lambda x, y: (cx + (x * ca - y * sa) * s, cy + (x * sa + y * ca) * s)
    col = np.minimum(255, np.asarray(ORCHID, np.float32) * light)
    shc = np.minimum(255, np.asarray(ORCHID_SH, np.float32) * light)
    olc = np.asarray((70, 74, 52), np.float32) * light
    if glow > 0:
        stepped_glow(img, cx, cy - 3 * s, 16 * s, (255, 250, 220), k=0.5 * glow, levels=3)
    img[m_line([P(-7.5, 0.6), P(7.5, 0.6)], max(1, int(round(0.45 * s))), Ww, Hh)] = (150, 150, 140)
    xs = (-3.4, 3.4) if n == 2 else (0.0,)
    for k, sx in enumerate(xs):
        tilt = -0.18 if sx < 0 else 0.18
        Q = lambda x, y: P(sx + x + y * tilt * -0.3, y)
        bud = m_poly([Q(-1.3, 0.2), Q(-1.6, -2.6), Q(-1.3, -5.4), Q(-0.5, -7.6), Q(0.0, -8.6), Q(0.5, -7.6), Q(1.3, -5.4), Q(1.6, -2.6), Q(1.3, 0.2)], Ww, Hh)
        if s >= 1.0:
            fill(img, outline_of(bud) & ~bud, olc)
        fill(img, bud, col)
        # shaded half + petal seam + split tip
        half = bud & m_poly([Q(0.15, 0.4), Q(0.3, -8.8), Q(3, -8.8), Q(3, 0.4)], Ww, Hh)
        fill(img, half, shc)
        if s >= 1.8:
            fill(img, m_line([Q(-0.4, -0.8), Q(-0.2, -6.6)], 1, Ww, Hh) & bud, shc * 0.96)
            fill(img, m_line([Q(-0.9, -6.8), Q(-0.3, -8.2)], 1, Ww, Hh), olc * 1.4)
        calyx = m_poly([Q(-1.2, -0.2), Q(1.2, -0.2), Q(0.8, 1.4), Q(-0.8, 1.4)], Ww, Hh)
        fill(img, calyx, np.asarray((96, 140, 84), np.float32) * light)
    leaf = m_poly([P(-1.2, 1.2), P(2.4, 4.2), P(6.6, 4.4), P(3.2, 1.4)], Ww, Hh)
    if s >= 1.0:
        fill(img, outline_of(leaf) & ~leaf, np.asarray((30, 50, 34), np.float32) * light)
    fill(img, leaf, np.asarray(LEAF, np.float32) * light)
    if s >= 1.8:
        fill(img, m_line([P(-0.6, 1.6), P(5.6, 4.0)], 1, Ww, Hh) & leaf, np.asarray((64, 110, 72), np.float32) * light)


def phone_sprite(img, x, y, w, h, screen=(150, 200, 240), a=1.0):
    m = m_rect(x, y, x + w, y + h)
    shape(img, m, (24, 24, 32), outline=(10, 10, 14), a=a)
    fill(img, m_rect(x + 1, y + 2, x + w - 1, y + h - 2), screen, a)


# ---------------- NPC ----------------
NPC_M = [dict(shirt=(110, 100, 86), vest=(80, 72, 62), pants=(54, 52, 64), hair=(46, 36, 34)),
         dict(shirt=(52, 62, 96), vest=(40, 48, 74), pants=(40, 40, 52), hair=(30, 26, 30)),
         dict(shirt=(120, 120, 128), vest=(88, 90, 100), pants=(34, 34, 44), hair=(60, 50, 44)),
         dict(shirt=(130, 70, 70), vest=(100, 54, 56), pants=(40, 36, 48), hair=(24, 22, 28))]
NPC_F = [dict(dress=(140, 190, 230), blouse=(240, 240, 240), hhair=(40, 30, 32)),
         dict(dress=(250, 210, 120), blouse=(250, 246, 236), hhair=(120, 70, 50)),
         dict(dress=(170, 220, 170), blouse=(240, 240, 240), hhair=(60, 40, 40)),
         dict(dress=(220, 120, 140), blouse=(250, 240, 240), hhair=(30, 24, 30))]
UMB_COLS = [(60, 64, 96), (40, 40, 48), (96, 60, 70), (70, 96, 84), (150, 140, 120), (84, 84, 104)]


def _no_vest(o):
    d = dict(o)
    d.update(vest_w=d['vest'], vest_r=d['vest'], bow1=d['shirt'], bow2=d['shirt'], bow3=d['shirt'], shirt_m=d['shirt'], shirt_b=d['shirt'])
    return d


def npc_walker(img, x, y, s, phase, kind=0, facing=1, light='night', umb=True, a=1.0):
    """side-view walker with umbrella; (x,y) feet."""
    o = tuple(sorted(_no_vest(NPC_M[kind % 4]).items()))
    spr, anc = HIM(view='side', s=s, light=light, walk=phase, hat=False, hand_r=(7.5, 58.0), over=o, rim=(1 if facing > 0 else -1, 0),
                   mouth='flat')
    place(img, spr, anc, x, y, a, flip=facing < 0)
    if umb:
        hx = x + facing * 7.5 * s
        hy = y - (100 - 59) * s
        umbrella(img, hx, hy, s * 1.25, UMB_COLS[kind % len(UMB_COLS)], light, a)


def npc_girl(img, x, y, s, phase=None, kind=0, facing=1, light='warm', view='side', expr='laugh', a=1.0, hand_r=None, hand_l=None):
    o = tuple(sorted(NPC_F[kind % 4].items()))
    spr, anc = HER(view=view, s=s, light=light, walk=phase, style='long', ribbon=False, over=o, mouth=expr,
                   eyes='happy' if expr == 'laugh' else 'open', hand_r=hand_r, hand_l=hand_l, rim=(1 if facing > 0 else -1, 0))
    place(img, spr, anc, x, y, a, flip=facing < 0)


# ---------------- taxi ----------------
@functools.lru_cache(maxsize=16)
def TAXI(s, light='night', passenger=True):
    b = SB(s, wu=150, hu=70, oxu=75, top_u=0)
    body_c = _lit((92, 140, 210), light) if light != 'day' else np.array((92, 140, 210), np.float32)
    body = b.m_poly([(-70, 44), (-68, 34), (-50, 30), (-34, 14), (26, 14), (44, 30), (66, 33), (70, 44), (68, 54), (-68, 54)])
    b.part('body', body, (body_c, body_c * 0.7, np.minimum(255, body_c * 1.2)), shade='top')
    win = b.m_poly([(-31, 17), (-4, 17), (-4, 30), (-45, 30)]) | b.m_poly([(0, 17), (24, 17), (40, 30), (0, 30)])
    b.paint(win, _lit((40, 46, 70), light))
    if passenger:
        # bob-haired silhouette in the back window (left window = rear when moving left)
        b.paint(b.m_ell(-18, 24, 7.0, 6.6) & win, _lit((70, 40, 36), light))
        b.paint(b.m_ell(-14.6, 25.4, 3.8, 4.4) & win, _lit((240, 200, 176), light))
        b.paint(b.m_ell(-11.6, 27.6, 0.9, 0.5) & win, _lit((140, 22, 46), light))
    b.paint(b.m_line([(-2, 14), (-2, 54)], 0.8) & body, body_c * 0.6)
    b.part('sign', b.m_poly([(-8, 9), (8, 9), (9, 14), (-9, 14)]), ramp((240, 200, 90)), shade='flat')
    for wx in (-46, 44):
        b.part('wheel', b.m_ell(wx, 54, 9, 9), ramp((30, 30, 36)), shade='flat')
        b.paint(b.m_ell(wx, 54, 4, 4), (110, 110, 120))
    b.paint(b.m_poly([(64, 38), (70, 38), (70, 44), (64, 44)]), (255, 240, 200))   # head light (front=right)
    b.paint(b.m_poly([(-70, 38), (-66, 38), (-66, 46), (-70, 46)]), (240, 40, 50))  # tail light
    spr = b.finish(outline=(14, 14, 20))
    return spr, (b.X(0), b.Y(63))


def bubble(img, x, y, text_, col=(250, 250, 252), tcol=(40, 36, 50), scale=1, a=1.0):
    """speech/thought bubble centred at x, bottom tip at y."""
    m = text_mask(text_, 16)
    if scale > 1:
        m = np.repeat(np.repeat(m, scale, 0), scale, 1)
    w, h = m.shape[1] + 8, m.shape[0] + 6
    x0, y0 = int(x - w / 2), int(y - h - 4)
    body = m_rect(x0, y0, x0 + w, y0 + h)
    body &= ~(m_rect(x0, y0, x0 + 1, y0 + 1) | m_rect(x0 + w - 1, y0, x0 + w, y0 + 1) | m_rect(x0, y0 + h - 1, x0 + 1, y0 + h) | m_rect(x0 + w - 1, y0 + h - 1, x0 + w, y0 + h))
    tip = m_poly([(x - 3, y0 + h - 1), (x + 3, y0 + h - 1), (x, y)])
    shape(img, body | tip, col, outline=(30, 26, 40), a=a)
    draw_text(img, text_, x0 + 4, y0 + 3, tcol, a=a, scale=scale)
