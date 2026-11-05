# -*- coding: utf-8 -*-
"""《小酒窝》男女主，按 640x360 高清像素网格重画（Q 版约 2.3 头身）。
他：格纹礼帽（灰底红竖纹+浅横线）、黑发斜刘海、紫蓝格子衬衫、黑白红格纹马甲、紫白蓝条纹领结、深色裤、棕鞋白底。
她：栗色齐刘海、长睫毛、笑时小酒窝；回忆=及背长发+珊瑚红蝴蝶结+白衬衫粉背带裙+白袜红鞋；
    现在=下巴波波头、示例歌词、深梅色外套配白领、深色裤袜、红鞋。
单位：0=帽顶/发顶附近，100=脚底。任意缩放直接光栅（SB），按光照乘色+单侧轮廓光。"""
import numpy as np, math, functools
from core import *
from sprite import SB, ramp, place

# ---------------- base colours (daylight, from 小酒窝 sprite) ----------------
BASE = dict(
    skin=(244, 204, 172), skin_d=(214, 156, 128), blush=(240, 150, 142),
    hair=(40, 30, 34), hair_h=(84, 64, 62),
    hat=(124, 116, 110), hat_d=(86, 80, 78), band=(52, 44, 48), hat_r=(178, 62, 76), hat_l=(206, 200, 192),
    shirt=(78, 66, 150), shirt_m=(190, 72, 136), shirt_b=(110, 146, 230),
    vest=(46, 46, 58), vest_w=(150, 150, 168), vest_r=(196, 54, 70),
    bow1=(110, 70, 180), bow2=(240, 240, 250), bow3=(150, 206, 246),
    pants=(50, 50, 70), shoe=(78, 50, 42), sole=(232, 228, 220),
    # her
    hskin=(250, 214, 188), hblush=(244, 150, 150), dimple=(212, 104, 116),
    hhair=(104, 60, 46), hhair_h=(154, 96, 68),
    ribbon=(238, 80, 100),
    blouse=(250, 246, 240), dress=(242, 150, 180), sock=(250, 250, 252), hshoe=(208, 62, 76),
    coat=(96, 44, 70), tights=(52, 40, 52),
    lip=(196, 80, 96), lip_deep=(140, 22, 46),
    eye=(36, 28, 42), mouth=(150, 56, 70), white=(255, 255, 255),
    outline=(20, 14, 26),
)

# lighting: (mul, add, rim colour)
LIGHT = {
    'day': ((1.0, 1.0, 1.0), (0, 0, 0), (255, 244, 220)),
    'night': ((0.70, 0.72, 0.90), (8, 10, 24), (176, 192, 240)),
    'lamp': ((0.80, 0.70, 0.64), (14, 6, 0), (255, 200, 140)),
    'warm': ((1.04, 0.90, 0.76), (22, 10, 0), (255, 214, 160)),
    'neon': ((0.74, 0.62, 0.86), (16, 2, 18), (255, 140, 200)),
    'room': ((0.78, 0.76, 0.86), (10, 8, 14), (255, 210, 160)),
    'dim': ((0.50, 0.52, 0.70), (4, 6, 16), (130, 150, 210)),
    'corner': ((0.86, 0.76, 0.82), (14, 4, 10), (255, 140, 200)),
    'nightpink': ((0.72, 0.72, 0.90), (10, 8, 24), (255, 150, 206)),
    'dusk': ((0.92, 0.80, 0.86), (16, 6, 14), (255, 180, 170)),
    'cold': ((0.66, 0.74, 0.92), (6, 12, 26), (190, 220, 255)),
}


def _lit(c, light):
    m, a, _ = LIGHT[light]
    return np.clip(np.asarray(c, np.float32) * np.asarray(m, np.float32) + np.asarray(a, np.float32), 0, 255)


def _R(c, light, k_sh=0.70, k_li=1.16):
    b = _lit(c, light)
    return (b, b * k_sh, np.minimum(255, b * k_li + 8))


def ik(S, T, L1, L2, bend=1):
    sx, sy = S; tx, ty = T
    dx, dy = tx - sx, ty - sy
    d = math.hypot(dx, dy)
    d = min(max(d, 1e-3), L1 + L2 - 1e-3)
    a = math.atan2(dy, dx)
    c = (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d)
    b = math.acos(max(-1, min(1, c)))
    ang = a + b * bend
    E = (sx + L1 * math.cos(ang), sy + L1 * math.sin(ang))
    n = math.hypot(dx, dy)
    Tn = (sx + dx / n * d, sy + dy / n * d) if n > 0 else T
    return E, Tn


def _eye(b, ex, ey, kind, col, white, big=False, lash=0, s=1.0, side=False):
    """kind: open/closed/happy/down/wide/sad/wink"""
    if kind in ('closed', 'wink_c'):
        b.paint(b.m_line([(ex - 1.8, ey + 0.4), (ex + 1.8, ey + 0.4)], 0.9), col)
        if lash:
            b.paint(b.m_line([(ex + 1.6 * lash, ey + 0.4), (ex + 2.6 * lash, ey - 0.4)], 0.7), col)
        return
    if kind == 'happy':
        b.paint(b.m_line([(ex - 2.0, ey + 1.0), (ex, ey - 0.8), (ex + 2.0, ey + 1.0)], 0.9), col)
        if lash:
            b.paint(b.m_line([(ex + 2.0 * lash, ey + 1.0), (ex + 2.9 * lash, ey + 0.2)], 0.7), col)
        return
    if kind == 'down':
        b.paint(b.m_ell(ex, ey + 1.0, 1.7, 1.2), col)
        b.paint(b.m_line([(ex - 2.0, ey + 0.2), (ex + 2.0, ey + 0.2)], 0.8), col)
        if lash:
            b.paint(b.m_line([(ex + 1.9 * lash, ey + 0.4), (ex + 2.8 * lash, ey + 1.4)], 0.7), col)
        return
    ry = 2.7 if not big else 3.1
    if kind == 'wide':
        ry *= 1.18
    rx = 1.65 if not big else 2.0
    if side:
        rx *= 0.85
    b.paint(b.m_ell(ex, ey, rx, ry), col)
    if s >= 0.9:
        b.paint(b.m_ell(ex + 0.5, ey - 0.9, 0.62, 0.75), white)
        if big and s >= 1.6:
            b.paint(b.m_ell(ex - 0.5, ey + 1.3, 0.35, 0.35), white * 0.9 + col * 0.1)
    if kind == 'sad':
        b.paint(b.m_line([(ex - 2.0 * (1 if ex < 0 else -1), ey - ry - 1.6), (ex + 1.6 * (1 if ex < 0 else -1), ey - ry - 0.6)], 0.7), col)
    if lash:
        # upper lid line flicking outward (long lashes)
        b.paint(b.m_line([(ex - rx * 1.05 * lash, ey - ry * 0.45), (ex + rx * 1.3 * lash, ey - ry * 0.9), (ex + rx * 2.0 * lash, ey - ry * 0.55)], 0.85), col)
        b.paint(b.m_line([(ex + rx * 1.9 * lash, ey - ry * 0.6), (ex + rx * 2.6 * lash, ey - ry * 1.1)], 0.7), col)


def _mouth(b, mx, my, kind, colm, side=False, lip=None, tongue=(236, 112, 122)):
    w = 1.0 if side else 1.0
    if kind == 'none':
        return
    if kind == 'smile':
        if side:
            b.paint(b.m_line([(mx - 1.2, my - 0.2), (mx + 0.3, my + 0.5)], 0.8), colm)
        else:
            b.paint(b.m_line([(mx - 2.2, my - 0.4), (mx, my + 0.9), (mx + 2.2, my - 0.4)], 0.85), colm)
    elif kind in ('open', 'laugh'):
        if side:
            b.paint(b.m_poly([(mx - 1.5, my - 0.6), (mx + 0.6, my - 0.8), (mx + 0.2, my + 1.4), (mx - 1.2, my + 1.0)]), colm)
        else:
            m = b.m_poly([(mx - 2.6, my - 0.7), (mx + 2.6, my - 0.7), (mx + 1.4, my + 1.9), (mx - 1.4, my + 1.9)])
            b.paint(m, colm)
            b.paint(m & b.m_ell(mx, my + 2.0, 1.6, 1.0), tongue)
    elif kind == 'o':
        b.paint(b.m_ell(mx - (0.4 if side else 0), my + 0.4, 1.0, 1.3), colm)
    elif kind == 'sad':
        if side:
            b.paint(b.m_line([(mx - 1.2, my + 0.5), (mx + 0.2, my - 0.1)], 0.8), colm)
        else:
            b.paint(b.m_line([(mx - 2.0, my + 0.8), (mx, my - 0.3), (mx + 2.0, my + 0.8)], 0.85), colm)
    elif kind == 'wavy':
        b.paint(b.m_line([(mx - 2.2, my + 0.4), (mx - 1.1, my - 0.3), (mx, my + 0.4), (mx + 1.1, my - 0.3), (mx + 2.2, my + 0.4)], 0.8), colm)
    elif kind == 'lips':   # closed, coloured lips (her, present)
        c = colm if lip is None else lip
        if side:
            b.paint(b.m_poly([(mx - 1.4, my - 0.5), (mx + 0.4, my - 0.7), (mx + 0.6, my + 0.6), (mx - 1.2, my + 0.7)]), c)
        else:
            b.paint(b.m_poly([(mx - 2.0, my - 0.3), (mx - 0.6, my - 0.9), (mx, my - 0.5), (mx + 0.6, my - 0.9), (mx + 2.0, my - 0.3),
                              (mx + 1.0, my + 0.9), (mx - 1.0, my + 0.9)]), c)
    else:  # flat
        if side:
            b.paint(b.m_line([(mx - 1.0, my), (mx + 0.4, my)], 0.8), colm)
        else:
            b.paint(b.m_line([(mx - 1.6, my), (mx + 1.6, my)], 0.85), colm)


# ============================== HIM ==============================

def _hat(b, view, P, dx=0.0, dy=0.0, tilt=0.0, s=1.0):
    O = lambda L: [(x + dx, y + dy) for x, y in L]
    hat, hd, band, hr, hl = P['hat'], P['hat_d'], P['band'], P['hat_r'], P['hat_l']
    if view in ('front', 'back'):
        crown = b.m_poly(O([(-13.5, 2.6), (-6, 0.6), (0, 2.2), (6, 0.6), (13.5, 2.6), (15.4, 13.6), (-15.4, 13.6)]))
        brim = b.m_ell(dx, 14.2 + dy, 25.5, 3.0 + tilt * 1.4)
        b.part('brim', brim, (hd, hd * 0.7, np.minimum(255, hd * 1.2)), shade='cyl', hl=0.1, sh=0.28)
        if tilt > 0.1 and view == 'front':
            b.paint(brim & b.m_ell(dx, 15.0 + dy, 23, 2.2) & ~shift(brim, 0, 1), hd * 0.6)
        b.part('crown', crown, (hat, hat * 0.74, np.minimum(255, hat * 1.15)), shade='cyl', hl=0.16, sh=0.3)
        if s >= 0.5:
            for x in (-9.5, -3.2, 3.2, 9.5):
                b.paint(b.m_line(O([(x * 0.98, 3.0), (x * 1.04, 13.4)]), 0.9) & crown, hr)
            b.paint(b.m_line(O([(-15, 7.2), (15, 7.2)]), 0.8) & crown, hl)
        bandm = b.m_poly(O([(-15.0, 9.8), (15.0, 9.8), (15.4, 13.6), (-15.4, 13.6)])) & crown
        b.part('band', bandm, (band, band * 0.8, band * 1.3), shade='cyl', hl=0.12, sh=0.3)
        b.paint(b.m_line(O([(0, 2.4), (0, 5.4)]), 0.8) & crown, hat * 0.62)
    else:  # side facing right
        crown = b.m_poly(O([(-12.6, 3.4), (2, 0.8), (11.6, 2.2), (13.8, 13.6), (-13.8, 13.6)]))
        brim = b.m_poly(O([(-23, 13.2), (-12, 12.4), (14, 12.4), (25, 13.0), (26.4, 14.4), (24, 15.8), (2, 15.6), (-20, 15.6), (-23.8, 14.6)]))
        b.part('brim', brim, (hd, hd * 0.7, np.minimum(255, hd * 1.25)), shade='top')
        b.part('crown', crown, (hat, hat * 0.74, np.minimum(255, hat * 1.15)), shade='cyl', hl=0.16, sh=0.3, light=1)
        if s >= 0.5:
            for x in (-8, -1.5, 5.5):
                b.paint(b.m_line(O([(x, 2.6), (x + 0.6, 13.4)]), 0.9) & crown, hr)
            b.paint(b.m_line(O([(-14, 7.2), (14, 7.2)]), 0.8) & crown, hl)
        bandm = b.m_poly(O([(-13.4, 9.8), (13.2, 9.8), (13.8, 13.6), (-13.8, 13.6)])) & crown
        b.part('band', bandm, (band, band * 0.8, band * 1.3), shade='cyl', light=1)


def _plaid(b, m, cols, step=4.0, w=0.7, s=1.0, ox=0.0, oy=0.0, x0=-20, x1=20, y0=40, y1=100):
    """thin plaid lines clipped to m. cols = (vertical colour, horizontal colour)"""
    if s < 0.55:
        return
    cv, ch = cols
    x = x0 + (ox % step)
    while x < x1:
        b.paint(b.m_line([(x, y0), (x, y1)], w) & m, cv)
        x += step
    y = y0 + (oy % step)
    while y < y1:
        b.paint(b.m_line([(x0, y), (x1, y)], w) & m, ch)
        y += step


def him(view='front', s=1.0, light='night', walk=None, hand_r=None, hand_l=None, eyes='open', mouth='smile', blush=False,
        hat=True, look=0.0, look_up=0.0, sit=False, head_back=False, rim=(1, 0), sweat=False, bob=0.0, tear=0.0, over=None):
    """view: front/side/back (side faces right). walk: phase 0..1. hand_r/l: IK targets in units
    (front: r = viewer's right; side: r = near arm). head_back: side body, head turned back to look behind (faces left)."""
    base = dict(BASE)
    if over:
        base.update(dict(over))
    P = {k: _lit(v, light) for k, v in base.items() if not isinstance(v, str)}
    b = SB(s, wu=64, hu=110, oxu=32, top_u=-6)
    ph = walk if walk is not None else 0.0
    wb = abs(math.sin(2 * math.pi * ph)) * 1.0 if walk is not None else 0.0
    oy = -wb + bob + (9.0 if sit else 0.0)
    O = lambda L: [(x, y + oy) for x, y in L]
    R = lambda key, ks=0.7, kl=1.16: (P[key], P[key] * ks, np.minimum(255, P[key] * kl + 8))
    sk = R('skin', 0.84, 1.08)
    side = view == 'side'
    # ---------------- legs ----------------
    if view in ('front', 'back'):
        if sit:
            for sg in (-1, 1):
                b.part('leg%d' % sg, b.m_poly([(sg * 8, 84), (sg * 1.0, 84), (sg * 1.4, 95.5), (sg * 7.2, 95.5)]), R('pants'), hl=0.2, sh=0.35)
                b.part('shoe%d' % sg, b.m_poly([(sg * 0.6, 94.5), (sg * 8.6, 94.5), (sg * 9.0, 100), (sg * 0.4, 100)]), R('shoe', 0.7, 1.3), shade='top')
                b.paint(b.m_line([(sg * 0.6, 99.4), (sg * 8.8, 99.4)], 0.8), P['sole'])
        else:
            for sg in (-1, 1):
                lift = 0
                if walk is not None:
                    lift = max(0, math.sin(2 * math.pi * (ph + (0 if sg > 0 else 0.5)))) * 2.2
                b.part('leg%d' % sg, b.m_poly([(sg * 8.4, 76), (sg * 1.0, 76), (sg * 1.4, 95.5 - lift), (sg * 7.6, 95.5 - lift)]), R('pants'), hl=0.2, sh=0.35)
                b.part('shoe%d' % sg, b.m_poly([(sg * 0.6, 94.3 - lift), (sg * 8.4, 94.3 - lift), (sg * 9.2, 98 - lift), (sg * 9.0, 100 - lift), (sg * 0.4, 100 - lift)]),
                       R('shoe', 0.7, 1.3), shade='top')
                b.paint(b.m_line([(sg * 0.6, 99.3 - lift), (sg * 9.0, 99.3 - lift)], 0.8), P['sole'])
    else:
        hip = (0.0, 77.0 + oy)
        if sit:
            for nm, dk in (('far', True), ('near', False)):
                xo = -1.2 if dk else 0.6
                rp = R('pants') if not dk else (P['pants'] * 0.72, P['pants'] * 0.6, P['pants'])
                b.part('thigh_' + nm, b.m_cap((xo, 83.5), (12 + xo, 84.5), 4.0, 3.6), rp, hl=0.2, sh=0.35, light=1, axis=0)
                b.part('shin_' + nm, b.m_cap((12 + xo, 84.5), (12.6 + xo, 95.0), 3.5, 3.0), rp, hl=0.2, sh=0.35, light=1)
                b.part('shoe_' + nm, b.m_poly([(9.6 + xo, 94.0), (16.4 + xo, 94.6), (18.2 + xo, 97.6), (18 + xo, 100), (9.4 + xo, 100)]),
                       R('shoe', 0.7, 1.3) if not dk else (P['shoe'] * 0.7, P['shoe'] * 0.6, P['shoe']), shade='top')
                b.paint(b.m_line([(9.6 + xo, 99.4), (18.0 + xo, 99.4)], 0.8), P['sole'] * (0.75 if dk else 1))
        else:
            for nm, off in (('far', 0.5), ('near', 0.0)):
                dk = nm == 'far'
                p = (ph + off) % 1.0 if walk is not None else 0.0
                th = 26 * math.sin(2 * math.pi * p) if walk is not None else 0.0
                kn = max(0.0, 30 * math.sin(2 * math.pi * p + 1.4)) if walk is not None else 0.0
                a1 = math.radians(th)
                knee = (hip[0] + 9.6 * math.sin(a1), hip[1] + 9.6 * math.cos(a1))
                a2 = math.radians(th - kn)
                ank = (knee[0] + 9.2 * math.sin(a2), knee[1] + 9.2 * math.cos(a2))
                rp = R('pants') if not dk else (P['pants'] * 0.72, P['pants'] * 0.6, P['pants'])
                b.part('leg_' + nm, b.m_cap(hip, knee, 4.2, 3.9) | b.m_cap(knee, ank, 3.9, 3.4), rp, hl=0.2, sh=0.35, light=1)
                fa = math.radians(-kn * 0.4 if walk is not None else 0)
                ca, sa = math.cos(fa), math.sin(fa)
                pts = [(-3.6, -1.6), (3.2, -1.8), (6.6, 0.2), (7.0, 2.4), (-3.8, 2.4)]
                sp = [(ank[0] + x * ca - y * sa, ank[1] + 2.2 + x * sa + y * ca) for x, y in pts]
                srp = R('shoe', 0.7, 1.3) if not dk else (P['shoe'] * 0.7, P['shoe'] * 0.6, P['shoe'])
                b.part('shoe_' + nm, b.m_poly(sp), srp, shade='top')
                sole = [(ank[0] + x * ca - y * sa, ank[1] + 2.2 + x * sa + y * ca) for x, y in [(-3.8, 2.0), (7.0, 2.0)]]
                b.paint(b.m_line(sole, 0.8), P['sole'] * (0.75 if dk else 1))
    # ---------------- arms (behind) ----------------
    sh_y = 53.0 + oy
    arms = []
    if not side:
        for sg, tgt in ((1, hand_r), (-1, hand_l)):
            S_ = (sg * 11.6, sh_y)
            T_ = tgt if tgt is not None else (sg * 14.4 + (math.sin(2 * math.pi * ph) * 1.5 * sg if walk is not None else 0), 72.5 + oy)
            E, Tn = ik(S_, T_, 10.6, 10.0, bend=(-1 if sg > 0 else 1))
            arms.append((sg, S_, E, Tn, tgt is not None))
    else:
        S_ = (0.5, sh_y)
        sw = 28 * math.sin(2 * math.pi * ph) if walk is not None else 0.0

        def arm_pts(swing, tgt):
            if tgt is not None:
                return ik(S_, tgt, 10.6, 10.0, bend=-1)
            a = math.radians(swing)
            E = (S_[0] + 10.6 * math.sin(a), S_[1] + 10.6 * math.cos(a))
            a2 = math.radians(swing + 14 + max(0, swing) * 0.4)
            return E, (E[0] + 10 * math.sin(a2), E[1] + 10 * math.cos(a2))
        Ef, Tf = arm_pts(-sw, hand_l)
        mfar = b.m_cap(S_, Ef, 3.4, 3.2) | b.m_cap(Ef, Tf, 3.2, 3.0)
        b.part('arm_far', mfar, (P['shirt'] * 0.72, P['shirt'] * 0.6, P['shirt']), shade='flat')
        b.part('hand_far', b.m_ell(Tf[0], Tf[1] + 1.2, 2.9, 3.0), (sk[1], sk[1] * 0.9, sk[0]), shade='flat')
    for sg, S_, E, Tn, raised in arms:
        if not raised:
            m = b.m_cap(S_, E, 3.5, 3.3) | b.m_cap(E, Tn, 3.3, 3.0)
            b.part('arm%d' % sg, m, R('shirt'), hl=0.22, sh=0.4)
            _plaid(b, m, (P['shirt_b'] * 0.9, P['shirt_m'] * 0.9), step=3.4, w=0.6, s=s, x0=-22, x1=22, y0=48, y1=80)
    # ---------------- torso ----------------
    if not side:
        shirt = b.m_poly(O([(-6, 49), (6, 49), (11.6, 51), (12.6, 56), (11.8, 77), (-11.8, 77), (-12.6, 56), (-11.6, 51)]))
        b.part('shirt', shirt, R('shirt'), hl=0.16, sh=0.3)
        vest = b.m_poly(O([(-12.2, 54), (-6.6, 50.4), (-1.6, 61.5), (0, 63.5), (1.6, 61.5), (6.6, 50.4), (12.2, 54), (11.6, 75.6), (0.6, 78.6), (0, 77.4),
                           (-0.6, 78.6), (-11.6, 75.6)])) if view == 'front' else \
            b.m_poly(O([(-12.2, 52), (12.2, 52), (11.8, 76.5), (-11.8, 76.5)]))
        b.part('vest', vest, R('vest', 0.7, 1.35), hl=0.16, sh=0.3)
        if s >= 0.55:
            # plaid on vest: white + red thin lines
            _plaid(b, vest, (P['vest_w'] * 0.85, P['vest_w'] * 0.85), step=8.5, w=0.6, s=s, x0=-12.75, x1=14, y0=50, y1=80, oy=oy + 3.0)
            _plaid(b, vest, (P['vest_r'] * 0.9, P['vest_r'] * 0.9), step=8.5, w=0.6, s=s * 0.8, x0=-8.5, x1=17, y0=54, y1=80, oy=oy + 7.2)
            if view == 'front':
                for k in range(3):
                    b.paint(b.m_ell(0.0, 66 + k * 3.8 + oy, 0.75, 0.75), P['vest_w'] * 1.15)
        if view == 'front':
            # shirt plaid in V
            _plaid(b, shirt & ~vest, (P['shirt_b'], P['shirt_m']), step=3.2, w=0.6, s=s, x0=-8, x1=8, y0=48, y1=66)
            # bow tie
            bw = b.m_poly(O([(-6.4, 48.2), (-0.6, 50.6), (-6.4, 53.4)])) | b.m_poly(O([(6.4, 48.2), (0.6, 50.6), (6.4, 53.4)]))
            b.part('bow', bw, R('bow1'), shade='flat')
            if s >= 0.6:
                b.paint(b.m_line(O([(-5.6, 49.6), (-5.6, 52.0)]), 0.8) & bw, P['bow2'])
                b.paint(b.m_line(O([(5.6, 49.6), (5.6, 52.0)]), 0.8) & bw, P['bow2'])
                b.paint(b.m_line(O([(-3.8, 49.8), (-3.8, 51.6)]), 0.7) & bw, P['bow3'])
                b.paint(b.m_line(O([(3.8, 49.8), (3.8, 51.6)]), 0.7) & bw, P['bow3'])
            b.part('knot', b.m_ell(0, 50.8 + oy, 1.5, 1.6), R('bow3'), shade='flat')
        else:
            b.paint(b.m_line(O([(0, 53), (0, 76)]), 0.8) & vest, P['vest'] * 0.7)
    else:
        shirt = b.m_poly(O([(-4.6, 49), (4.0, 49), (6.8, 52), (7.4, 60), (6.8, 77), (-7.4, 77), (-7.6, 60), (-6.6, 52)]))
        b.part('shirt', shirt, R('shirt'), hl=0.16, sh=0.3, light=1)
        vest = b.m_poly(O([(-7.2, 51.6), (2.8, 51.0), (5.4, 60), (6.4, 66), (6.2, 76.4), (-7.2, 76.4), (-7.6, 60)]))
        b.part('vest', vest, R('vest', 0.7, 1.35), hl=0.14, sh=0.3, light=1)
        _plaid(b, vest, (P['vest_w'] * 0.85, P['vest_w'] * 0.85), step=8.5, w=0.6, s=s, x0=-12.75, x1=10, y0=50, y1=80, oy=oy + 3.0)
        _plaid(b, vest, (P['vest_r'] * 0.9, P['vest_r'] * 0.9), step=8.5, w=0.6, s=s * 0.8, x0=-8.5, x1=13, y0=54, y1=80, oy=oy + 7.2)
        bw = b.m_poly(O([(3.2, 48.6), (7.4, 48.4), (7.0, 52.6), (3.4, 52.2)]))
        b.part('bow', bw, R('bow1'), shade='flat')
        if s >= 0.6:
            b.paint(b.m_line(O([(5.6, 48.8), (5.4, 52.2)]), 0.7) & bw, P['bow2'])
    # raised arms / near arm
    if side:
        En, Tn = arm_pts(sw, hand_r)
        mnear = b.m_cap(S_, En, 3.5, 3.3) | b.m_cap(En, Tn, 3.3, 3.0)
        b.part('arm_near', mnear, R('shirt'), hl=0.22, sh=0.36, light=1)
        _plaid(b, mnear, (P['shirt_b'] * 0.9, P['shirt_m'] * 0.9), step=3.4, w=0.6, s=s, x0=-22, x1=22, y0=48, y1=80)
        b.part('hand_near', b.m_ell(Tn[0], Tn[1] + 1.2, 3.0, 3.1), sk, hl=0.25, sh=0.3, light=1)
    else:
        for sg, S_, E, Tn, raised in arms:
            if raised:
                m = b.m_cap(S_, E, 3.5, 3.3) | b.m_cap(E, Tn, 3.3, 3.0)
                b.part('arm%d' % sg, m, R('shirt'), hl=0.22, sh=0.4)
                _plaid(b, m, (P['shirt_b'] * 0.9, P['shirt_m'] * 0.9), step=3.4, w=0.6, s=s, x0=-22, x1=22, y0=40, y1=80)
        for sg, S_, E, Tn, raised in arms:
            b.part('hand%d' % sg, b.m_ell(Tn[0], Tn[1] + (1.2 if not raised else -0.4), 3.0, 3.1), sk, hl=0.25, sh=0.4)
    # ---------------- head ----------------
    hy = oy - look_up * 0.8
    hview = view
    if side and head_back:
        hview = 'side_l'
    cx = look * 1.2
    head = b.m_ell(cx * 0.4, 31.0 + hy, 20.0, 19.0)
    hair = P['hair']
    hr = (hair, hair * 0.75, np.minimum(255, hair * 1.6 + 16))
    if hview == 'back':
        b.part('head', head, hr, hl=0.14, sh=0.3)
        b.part('nape', b.m_ell(0, 49.0 + hy, 5.0, 2.4), (sk[1], sk[1] * 0.85, sk[0]), shade='flat')
    else:
        fx = 1 if hview != 'side_l' else -1
        if hview == 'front':
            b.part('head', head, sk, hl=0.16, sh=0.26)
            for sg in (-1, 1):
                b.part('ear%d' % sg, b.m_ell(sg * 19.6, 33 + hy, 2.4, 3.2), sk, shade='flat')
            # hair: sides + side-swept bangs (from viewer's left to right)
            hm = b.m_poly([(x, y + hy) for x, y in [(-20.4, 30), (-20.6, 20), (-17, 14), (0, 12), (17, 14), (20.6, 20), (20.4, 30), (18.6, 27), (17.4, 22),
                                                     (12, 25.5), (5, 23.5), (-1, 26.5), (-6, 24.6), (-10.6, 27.4), (-15.6, 25.6), (-18.6, 28)]])
            b.part('hair', hm, hr, hl=0.18, sh=0.3)
            b.part('burn_l', b.m_poly([(x, y + hy) for x, y in [(-20.4, 26), (-18.4, 26), (-18.0, 35.5), (-19.8, 34)]]), hr, shade='flat')
            b.part('burn_r', b.m_poly([(x, y + hy) for x, y in [(20.4, 26), (18.4, 26), (18.0, 35.5), (19.8, 34)]]), hr, shade='flat')
            if s >= 0.7:
                b.paint(b.m_line([(-9, 17.5 + hy), (-3, 15.8 + hy)], 0.8), hr[2])
            ex, ey = 7.2, 34.5 + hy - look_up * 0.6
            for sg in (-1, 1):
                k = eyes
                if eyes == 'wink' and sg > 0:
                    k = 'closed'
                elif eyes == 'wink':
                    k = 'open'
                _eye(b, sg * ex + look, ey, k, P['eye'], P['white'], s=s)
            if blush or mouth in ('laugh',):
                for sg in (-1, 1):
                    b.paint(b.m_ell(sg * 11.5, 40.0 + hy, 2.4, 1.1), P['blush'])
            _mouth(b, look * 0.8, 42.2 + hy, mouth, P['mouth'])
            if tear > 0 and s >= 0.9:
                ty = ey + 3.5 + tear * 7
                b.paint(b.m_ell(-ex + look - 0.4, ty, 0.9, 1.4), (200, 228, 255))
        else:
            # side profile (fx=1 faces right, -1 faces left)
            F = lambda L: [(x * fx, y + hy) for x, y in L]
            face = b.m_poly(F([(-17, 22), (-19.4, 30), (-17.4, 41), (-11, 48.6), (0, 50.2), (9, 48.6), (15.4, 44), (18.4, 38.4), (19.4, 35.6),
                               (20.6, 33.4), (19.2, 31.8), (19.4, 24), (14, 15), (0, 12), (-12, 14.6)]))
            b.part('head', face, sk, hl=0.18, sh=0.24, light=fx)
            hm = b.m_poly(F([(-19.6, 33), (-20.2, 22), (-15, 14.4), (0, 11.6), (14, 14.6), (19.2, 22), (19.6, 26.4), (14.4, 25.2), (10, 27.6), (6, 24.6),
                             (2.6, 26.4), (-1.6, 25.4), (-4.4, 33.8), (-6.4, 40.6), (-12.6, 45.4), (-17.2, 41)]))
            b.part('hair', hm, hr, hl=0.16, sh=0.3, light=fx)
            b.part('ear', b.m_ell(-2.6 * fx, 34.6 + hy, 2.3, 3.0), (sk[1], sk[1] * 0.85, sk[0]), shade='flat')
            ex, ey = 11.0 * fx, 34.6 + hy - look_up * 0.6
            k = 'open' if eyes == 'wink' else eyes
            _eye(b, ex, ey, k, P['eye'], P['white'], s=s, side=True)
            if blush or mouth in ('laugh',):
                b.paint(b.m_ell(12.6 * fx, 40.4 + hy, 2.0, 1.0), P['blush'])
            _mouth(b, 16.2 * fx, 43.0 + hy, mouth, P['mouth'], side=True)
            if tear > 0 and s >= 0.9:
                b.paint(b.m_ell(ex - 0.2 * fx, ey + 3.5 + tear * 7, 0.9, 1.4), (200, 228, 255))
    if hat:
        hv = 'front' if hview in ('front', 'back') else 'side'
        if hview == 'side_l':
            # draw a mirrored side hat: build on temp and paste flipped into b
            tb = SB(s, wu=64, hu=110, oxu=32, top_u=-6)
            _hat(tb, 'side', P, dy=hy + 2.4 - look_up * 0.6, tilt=look_up, s=s)
            m = tb.sil[:, ::-1]
            b.col[m] = tb.col[:, ::-1][m]
            b.sil |= m
        else:
            _hat(b, hv, P, dy=hy + 2.4 - look_up * 0.6, tilt=look_up, s=s)
    elif hview != 'back':
        # crown hair (no hat)
        top = b.m_ell(cx * 0.4, 24.0 + hy, 19.6, 12.6) & head
        b.part('hairtop', top & ~b.m_poly([(-30, 26 + hy), (30, 26 + hy), (30, 60), (-30, 60)]), hr, hl=0.2, sh=0.3)
    if sweat and s >= 0.6:
        b.paint(b.m_ell(-21 if view != 'side' else -18, 26 + hy, 1.3, 2.2), (160, 210, 255))
    _, _, rc = LIGHT[light]
    spr = b.finish(outline=_lit(BASE['outline'], 'day'), rim=(rim[0], rim[1], np.asarray(rc, np.float32), max(1, int(s * 0.9))) if rim else None)
    return spr, b.anchor(), b


# ============================== HER ==============================

def her(view='front', s=1.0, light='night', walk=None, hand_r=None, hand_l=None, eyes='open', mouth='smile', blush=True,
        style='memory', ribbon=None, dimple=False, look=0.0, look_up=0.0, sit=False, rim=(1, 0), tear=0.0, lip=None, over=None):
    """style: memory (long hair, ribbon, pink pinafore) / now (bob, deep lips, plum coat) / cut (bob + memory clothes)."""
    base = dict(BASE)
    if over:
        base.update(dict(over))
    P = {k: _lit(v, light) for k, v in base.items() if not isinstance(v, str)}
    b = SB(s, wu=64, hu=110, oxu=32, top_u=-6)
    longhair = style in ('memory', 'long')
    if ribbon is None:
        ribbon = style in ('memory', 'cut')
    ph = walk if walk is not None else 0.0
    wb = abs(math.sin(2 * math.pi * ph)) * 0.9 if walk is not None else 0.0
    oy = -wb + (9.0 if sit else 0.0)
    O = lambda L: [(x, y + oy) for x, y in L]
    R = lambda key, ks=0.7, kl=1.16: (P[key], P[key] * ks, np.minimum(255, P[key] * kl + 8))
    sk = R('hskin', 0.86, 1.06)
    side = view == 'side'
    legc = 'hskin' if style != 'now' else 'tights'
    dresskey = 'dress' if style != 'now' else 'coat'
    topkey = 'blouse' if style != 'now' else 'coat'
    hair = P['hhair']
    hr = (hair, hair * 0.74, np.minimum(255, P['hhair_h'] * 1.05))
    hy = oy - look_up * 0.7
    # ---- hair back mass (behind everything) ----
    if view != 'back':
        if longhair:
            hb = b.m_poly([(x, y + hy) for x, y in ([(-21, 22), (-23, 36), (-22.6, 58), (-19, 66), (19, 66), (22.6, 58), (23, 36), (21, 22)] if not side else
                                                    [(-22, 22), (-23.6, 38), (-22.4, 58), (-17, 66), (-4, 64), (-2, 48), (6, 30), (8, 20)])])
            b.part('hairback', hb, (hr[1], hr[1] * 0.85, hr[0]), shade='flat')
        else:
            hb = b.m_poly([(x, y + hy) for x, y in ([(-21.6, 22), (-23.0, 38), (-21.4, 49), (-16, 51.4), (16, 51.4), (21.4, 49), (23.0, 38), (21.6, 22)] if not side else
                                                    [(-22, 22), (-23.4, 38), (-21.2, 49), (-12, 51.6), (-4, 50), (4, 30), (8, 20)])])
            b.part('hairback', hb, (hr[1], hr[1] * 0.85, hr[0]), shade='flat')
    # ---- legs ----
    if view in ('front', 'back'):
        if sit:
            for sg in (-1, 1):
                b.part('leg%d' % sg, b.m_poly([(sg * 6.2, 85), (sg * 1.4, 85), (sg * 1.8, 96), (sg * 5.6, 96)]), R(legc, 0.84, 1.06), hl=0.2, sh=0.35)
                if style != 'now':
                    b.paint(b.m_poly([(sg * 1.4, 91.5), (sg * 6.0, 91.5), (sg * 6.0, 96), (sg * 1.6, 96)]), P['sock'])
                b.part('shoe%d' % sg, b.m_poly([(sg * 1.0, 95.5), (sg * 6.4, 95.5), (sg * 7.4, 98.4), (sg * 7.2, 100), (sg * 0.8, 100)]), R('hshoe', 0.7, 1.25), shade='top')
        else:
            for sg in (-1, 1):
                lift = max(0, math.sin(2 * math.pi * (ph + (0 if sg > 0 else 0.5)))) * 2.0 if walk is not None else 0
                b.part('leg%d' % sg, b.m_poly([(sg * 6.0, 78), (sg * 1.4, 78), (sg * 1.8, 96 - lift), (sg * 5.6, 96 - lift)]), R(legc, 0.84, 1.06), hl=0.2, sh=0.35)
                if style != 'now':
                    b.paint(b.m_poly([(sg * 1.4, 91.0 - lift), (sg * 6.0, 91.0 - lift), (sg * 6.0, 96 - lift), (sg * 1.6, 96 - lift)]), P['sock'])
                b.part('shoe%d' % sg, b.m_poly([(sg * 1.0, 95.4 - lift), (sg * 6.4, 95.4 - lift), (sg * 7.6, 98.2 - lift), (sg * 7.4, 100 - lift), (sg * 0.8, 100 - lift)]),
                       R('hshoe', 0.7, 1.25), shade='top')
    else:
        hip = (0.0, 78.0 + oy)
        if sit:
            for nm, dk in (('far', True), ('near', False)):
                xo = -1.0 if dk else 0.6
                base = R(legc, 0.84, 1.06)
                rp = base if not dk else (base[1], base[1] * 0.9, base[0])
                b.part('thigh_' + nm, b.m_cap((xo, 84.5), (11 + xo, 85.5), 3.4, 3.0), rp, hl=0.2, sh=0.35, light=1, axis=0)
                b.part('shin_' + nm, b.m_cap((11 + xo, 85.5), (11.4 + xo, 95.5), 2.8, 2.5), rp, hl=0.2, sh=0.35, light=1)
                if style != 'now':
                    b.paint(b.m_cap((11 + xo, 91.0), (11.4 + xo, 95.5), 2.9, 2.6), P['sock'] * (0.8 if dk else 1))
                b.part('shoe_' + nm, b.m_poly([(8.8 + xo, 95.0), (14.2 + xo, 95.4), (15.8 + xo, 98.4), (15.6 + xo, 100), (8.6 + xo, 100)]),
                       R('hshoe', 0.7, 1.25) if not dk else (P['hshoe'] * 0.72, P['hshoe'] * 0.6, P['hshoe']), shade='top')
        else:
            for nm, off in (('far', 0.5), ('near', 0.0)):
                dk = nm == 'far'
                p = (ph + off) % 1.0 if walk is not None else 0.0
                th = 24 * math.sin(2 * math.pi * p) if walk is not None else 0.0
                kn = max(0.0, 28 * math.sin(2 * math.pi * p + 1.4)) if walk is not None else 0.0
                a1 = math.radians(th)
                knee = (hip[0] + 9.2 * math.sin(a1), hip[1] + 9.2 * math.cos(a1))
                a2 = math.radians(th - kn)
                ank = (knee[0] + 8.8 * math.sin(a2), knee[1] + 8.8 * math.cos(a2))
                base = R(legc, 0.84, 1.06)
                rp = base if not dk else (base[1], base[1] * 0.9, base[0])
                lm = b.m_cap(hip, knee, 3.0, 2.8) | b.m_cap(knee, ank, 2.8, 2.4)
                b.part('leg_' + nm, lm, rp, hl=0.2, sh=0.35, light=1)
                if style != 'now':
                    b.paint(b.m_cap(((knee[0] + ank[0]) / 2, (knee[1] + ank[1]) / 2 + 1.4), ank, 2.9, 2.5), P['sock'] * (0.8 if dk else 1))
                fa = math.radians(-kn * 0.4 if walk is not None else 0)
                ca, sa = math.cos(fa), math.sin(fa)
                pts = [(-2.8, -1.4), (2.6, -1.6), (5.8, 0.4), (6.0, 2.2), (-3.0, 2.2)]
                sp = [(ank[0] + x * ca - y * sa, ank[1] + 2.0 + x * sa + y * ca) for x, y in pts]
                b.part('shoe_' + nm, b.m_poly(sp), R('hshoe', 0.7, 1.25) if not dk else (P['hshoe'] * 0.72, P['hshoe'] * 0.6, P['hshoe']), shade='top')
    # ---- arms behind ----
    sh_y = 52.5 + oy
    arms = []
    if not side:
        for sg, tgt in ((1, hand_r), (-1, hand_l)):
            S_ = (sg * 9.6, sh_y)
            T_ = tgt if tgt is not None else (sg * 12.6, 70.5 + oy)
            E, Tn = ik(S_, T_, 9.6, 9.0, bend=(-1 if sg > 0 else 1))
            arms.append((sg, S_, E, Tn, tgt is not None))
    else:
        S_ = (0.4, sh_y)
        sw = 24 * math.sin(2 * math.pi * ph) if walk is not None else 0.0

        def arm_pts(swing, tgt):
            if tgt is not None:
                return ik(S_, tgt, 9.6, 9.0, bend=-1)
            a = math.radians(swing)
            E = (S_[0] + 9.6 * math.sin(a), S_[1] + 9.6 * math.cos(a))
            a2 = math.radians(swing + 14)
            return E, (E[0] + 9 * math.sin(a2), E[1] + 9 * math.cos(a2))
        Ef, Tf = arm_pts(-sw, hand_l)
        base = R(topkey)
        b.part('arm_far', b.m_cap(S_, Ef, 2.9, 2.7) | b.m_cap(Ef, Tf, 2.7, 2.5), (base[1], base[1] * 0.9, base[0]), shade='flat')
        b.part('hand_far', b.m_ell(Tf[0], Tf[1] + 1.0, 2.5, 2.6), (sk[1], sk[1] * 0.9, sk[0]), shade='flat')
    for sg, S_, E, Tn, raised in arms:
        if not raised:
            b.part('arm%d' % sg, b.m_cap(S_, E, 3.0, 2.8) | b.m_cap(E, Tn, 2.8, 2.5), R(topkey), hl=0.2, sh=0.4)
    # ---- torso: blouse + pinafore / coat ----
    if not side:
        top = b.m_poly(O([(-5, 48.5), (5, 48.5), (9.6, 50.4), (10.6, 55), (10.0, 64), (-10.0, 64), (-10.6, 55), (-9.6, 50.4)]))
        b.part('top', top, R(topkey), hl=0.16, sh=0.3)
        skirt = b.m_poly(O([(-10.2, 61), (10.2, 61), (12.6, 70), (15.4, 80.5), (-15.4, 80.5), (-12.6, 70)]))
        b.part('skirt', skirt, R(dresskey), hl=0.16, sh=0.3)
        if style != 'now' and view == 'front':
            bib = b.m_poly(O([(-6.4, 55.6), (6.4, 55.6), (7.0, 62), (-7.0, 62)]))
            b.part('bib', bib, R('dress'), shade='flat')
            for sg in (-1, 1):
                b.paint(b.m_line(O([(sg * 5.8, 55.6), (sg * 7.6, 50.0)]), 1.4), P['dress'])
            if s >= 0.7:
                b.paint(b.m_line(O([(-12.6, 79.4), (12.6, 79.4)]), 0.8) & skirt, P['dress'] * 0.78)
                b.paint(b.m_ell(-0.2, 58.6 + oy, 1.6, 1.0), np.minimum(255, P['dress'] * 1.15))
        if style == 'now' and view == 'front':
            b.paint(b.m_line(O([(0, 52), (0, 80)]), 0.8) & (top | skirt), P['coat'] * 0.66)
            for k in range(3):
                b.paint(b.m_ell(-2.0, 57 + k * 6 + oy, 0.7, 0.7), np.minimum(255, P['coat'] * 1.5))
        if view == 'front':
            col = b.m_poly(O([(-6.4, 48.0), (0, 51.6), (6.4, 48.0), (7.4, 50.6), (2.0, 54.0), (0, 53.0), (-2.0, 54.0), (-7.4, 50.6)]))
            b.part('collar', col, R('blouse', 0.82, 1.04), shade='flat')
            if style != 'now' and s >= 0.6:
                b.paint(b.m_ell(-1.2, 52.0 + oy, 1.1, 0.9) | b.m_ell(1.2, 52.0 + oy, 1.1, 0.9), P['ribbon'])
    else:
        top = b.m_poly(O([(-4.4, 48.6), (3.6, 48.6), (5.8, 52), (6.2, 60), (5.6, 64), (-6.4, 64), (-6.6, 56), (-5.6, 51.6)]))
        b.part('top', top, R(topkey), hl=0.16, sh=0.3, light=1)
        skirt = b.m_poly(O([(-6.6, 61), (5.8, 61), (8.6, 70), (11.6, 80.5), (-11.0, 80.5), (-8.6, 70)]))
        b.part('skirt', skirt, R(dresskey), hl=0.16, sh=0.3, light=1)
        if style != 'now':
            b.part('bib', b.m_poly(O([(-1.6, 55.4), (5.8, 55.4), (6.2, 62), (-1.8, 62)])), R('dress'), shade='flat')
            b.paint(b.m_line(O([(0.6, 55.4), (-2.0, 50.0)]), 1.4), P['dress'])
        col = b.m_poly(O([(-1.2, 47.8), (5.8, 48.2), (6.6, 50.8), (1.4, 51.6)]))
        b.part('collar', col, R('blouse', 0.82, 1.04), shade='flat')
    if side:
        En, Tn = arm_pts(sw, hand_r)
        b.part('arm_near', b.m_cap(S_, En, 3.0, 2.8) | b.m_cap(En, Tn, 2.8, 2.5), R(topkey), hl=0.22, sh=0.36, light=1)
        b.part('hand_near', b.m_ell(Tn[0], Tn[1] + 1.0, 2.6, 2.7), sk, hl=0.25, sh=0.3, light=1)
    else:
        for sg, S_, E, Tn, raised in arms:
            if raised:
                b.part('arm%d' % sg, b.m_cap(S_, E, 3.0, 2.8) | b.m_cap(E, Tn, 2.8, 2.5), R(topkey), hl=0.2, sh=0.4)
        for sg, S_, E, Tn, raised in arms:
            b.part('hand%d' % sg, b.m_ell(Tn[0], Tn[1] + (1.0 if not raised else -0.4), 2.6, 2.7), sk, hl=0.25, sh=0.4)
    # ---- head ----
    lipc = P['lip'] if style != 'now' else P['lip_deep']
    if lip is not None:
        lipc = _lit(lip, light)
    if view == 'back':
        if longhair:
            hm = b.m_poly([(x, y + hy) for x, y in [(-20, 18), (-23, 36), (-22.6, 58), (-19, 66), (19, 66), (22.6, 58), (23, 36), (20, 18), (12, 13.6), (0, 12.4), (-12, 13.6)]])
        else:
            hm = b.m_poly([(x, y + hy) for x, y in [(-20, 18), (-23, 36), (-21.4, 49), (-16, 51.4), (16, 51.4), (21.4, 49), (23, 36), (20, 18), (12, 13.6), (0, 12.4), (-12, 13.6)]])
        b.part('hair', hm | b.m_ell(0, 32 + hy, 20.4, 19.6), hr, hl=0.14, sh=0.3)
        if s >= 0.7:
            for x in (-9, -2, 6):
                b.paint(b.m_line([(x, 20 + hy), (x * 1.15, (60 if longhair else 47) + hy)], 0.7) & hm, hr[2])
        if ribbon:
            _ribbon(b, P, -13.0, 21.0 + hy, s)
    elif not side:
        head = b.m_ell(look * 0.5, 33.0 + hy, 20.0, 19.0)
        b.part('head', head, sk, hl=0.16, sh=0.24)
        top = b.m_poly([(x, y + hy) for x, y in [(-21.0, 34), (-21.4, 22), (-16.6, 15.4), (0, 12.6), (16.6, 15.4), (21.4, 22), (21.0, 34), (18.6, 30.0), (17.6, 27.4),
                                                  (13, 28.6), (8, 27.2), (3.5, 28.8), (-1.5, 27.4), (-6, 28.8), (-10.6, 27.4), (-15, 28.6), (-18.4, 27.2), (-19.0, 30.4)]])
        b.part('hairtop', top, hr, hl=0.22, sh=0.3)
        for sg in (-1, 1):
            if longhair:
                lock = b.m_poly([(x * sg, y + hy) for x, y in [(19.4, 26), (22.0, 36), (22.6, 52), (20.4, 62), (17.4, 56), (16.8, 42), (17.4, 30)]])
            else:
                lock = b.m_poly([(x * sg, y + hy) for x, y in [(19.4, 26), (22.2, 36), (21.8, 46), (18.6, 50.6), (15.0, 49.0), (16.6, 42), (17.2, 30)]])
            b.part('lock%d' % sg, lock, hr, hl=0.3, sh=0.3, light=-sg)
        if s >= 0.7:
            b.paint(b.m_line([(-11, 17.6 + hy), (-4, 15.2 + hy)], 0.9), hr[2])
        if ribbon:
            _ribbon(b, P, 13.6, 18.6 + hy, s)
        ex, ey = 7.6, 36.0 + hy - look_up * 0.5
        for sg in (-1, 1):
            k = eyes
            if eyes == 'wink':
                k = 'closed' if sg > 0 else 'open'
            _eye(b, sg * ex + look, ey, k, P['eye'], P['white'], big=True, lash=sg, s=s)
        if blush:
            for sg in (-1, 1):
                b.paint(b.m_ell(sg * 12.2, 41.6 + hy, 2.6, 1.2), P['hblush'])
        mk = mouth
        if style == 'now' and mouth in ('smile', 'flat'):
            mk = 'lips'
        _mouth(b, look * 0.8, 44.0 + hy, mk, P['mouth'], lip=lipc)
        if mk in ('smile', 'laugh', 'open') and style == 'now':
            pass
        if dimple and s >= 0.7:
            for sg in (-1, 1):
                b.paint(b.m_ell(sg * 4.6 + look * 0.8, 43.6 + hy, 0.6, 0.6), P['dimple'])
        if tear > 0 and s >= 0.9:
            b.paint(b.m_ell(-ex + look, ey + 4.0 + tear * 7, 1.0, 1.5), (204, 230, 255))
            b.paint(b.m_ell(ex + look, ey + 4.0 + tear * 6, 1.0, 1.5), (204, 230, 255))
    else:
        F = lambda L: [(x, y + hy) for x, y in L]
        face = b.m_poly(F([(-17, 24), (-19.4, 32), (-17.4, 43), (-11, 50.4), (0, 52), (8, 50.6), (14.4, 46.4), (17.6, 41.4), (18.6, 38.6), (19.8, 36.8),
                           (18.6, 35.0), (18.8, 26), (13.4, 17), (0, 14), (-12, 16.6)]))
        b.part('head', face, sk, hl=0.18, sh=0.24, light=1)
        top = b.m_poly(F([(-21.6, 38), (-21.6, 24), (-16, 15.4), (0, 12.4), (13, 15), (19.4, 22), (20.2, 29.8), (16.4, 29.2), (13.6, 30.4), (11.0, 28.6),
                          (8.0, 30.2), (5.0, 29.0), (1.0, 30.6), (-2.0, 36.0), (-3.4, 44.0), (-6.0, (60 if longhair else 49)), (-12, (64 if longhair else 50.6)),
                          (-20.0, (60 if longhair else 48))]))
        b.part('hairtop', top, hr, hl=0.2, sh=0.3, light=1)
        if s >= 0.7:
            b.paint(b.m_line(F([(-10, 18), (-2, 15.4)]), 0.9), hr[2])
        if ribbon:
            _ribbon(b, P, -11.0, 18.0 + hy, s, side=True)
        ex, ey = 11.0, 36.0 + hy - look_up * 0.5
        k = 'open' if eyes == 'wink' else eyes
        _eye(b, ex, ey, k, P['eye'], P['white'], big=True, lash=1, s=s, side=True)
        if blush:
            b.paint(b.m_ell(12.6, 42.0 + hy, 2.2, 1.0), P['hblush'])
        mk = mouth
        if style == 'now' and mouth in ('smile', 'flat'):
            mk = 'lips'
        _mouth(b, 16.0, 44.6 + hy, mk, P['mouth'], side=True, lip=lipc)
        if dimple and s >= 0.7:
            b.paint(b.m_ell(13.2, 44.6 + hy, 0.6, 0.6), P['dimple'])
        if tear > 0 and s >= 0.9:
            b.paint(b.m_ell(ex - 0.4, ey + 4.0 + tear * 7, 1.0, 1.5), (204, 230, 255))
    _, _, rc = LIGHT[light]
    spr = b.finish(outline=_lit(BASE['outline'], 'day'), rim=(rim[0], rim[1], np.asarray(rc, np.float32), max(1, int(s * 0.9))) if rim else None)
    return spr, b.anchor(), b


def _ribbon(b, P, x, y, s, side=False):
    rc = P['ribbon']
    rp = (rc, rc * 0.72, np.minimum(255, rc * 1.15))
    if side:
        m = b.m_poly([(x - 4.6, y - 3.4), (x, y - 0.4), (x - 4.6, y + 3.4)]) | b.m_poly([(x + 4.6, y - 3.4), (x, y - 0.4), (x + 4.6, y + 3.4)])
    else:
        m = b.m_poly([(x - 6.0, y - 3.8), (x, y), (x - 6.0, y + 3.8)]) | b.m_poly([(x + 6.0, y - 3.8), (x, y), (x + 6.0, y + 3.8)])
    b.part('ribbon', m, rp, shade='flat')
    b.part('rknot', b.m_ell(x, y, 1.6, 1.8), (rc * 0.8, rc * 0.7, rc), shade='flat')
    if s >= 0.8:
        b.paint(b.m_line([(x - 4.4, y - 2.0), (x - 2.2, y - 0.6)], 0.6) & m, rc * 0.7)


# ---------------- cached wrappers ----------------
def _r(v):
    if isinstance(v, float):
        return round(v, 3)
    if isinstance(v, (tuple, list)):
        return tuple(_r(x) for x in v)
    return v


@functools.lru_cache(maxsize=768)
def _him_c(key):
    spr, anc, b = him(**dict(key))
    return spr, anc


@functools.lru_cache(maxsize=768)
def _her_c(key):
    spr, anc, b = her(**dict(key))
    return spr, anc


def HIM(**kw):
    if kw.get('walk') is not None:
        kw['walk'] = (math.floor(kw['walk'] * 8) % 8) / 8.0
    return _him_c(tuple(sorted((k, _r(v)) for k, v in kw.items())))


def HER(**kw):
    if kw.get('walk') is not None:
        kw['walk'] = (math.floor(kw['walk'] * 8) % 8) / 8.0
    return _her_c(tuple(sorted((k, _r(v)) for k, v in kw.items())))


def unit_px(anc, s, x0, y0, ux, uy, flip=False):
    """screen position of unit point (ux,uy) for a sprite placed with feet at (x0,y0)."""
    if flip:
        ux = -ux
    return x0 + ux * s, y0 + (uy - 100) * s


def blink(t, seed=0.0, period=3.7):
    return ((t + seed * 1.37) % period) < 0.11
