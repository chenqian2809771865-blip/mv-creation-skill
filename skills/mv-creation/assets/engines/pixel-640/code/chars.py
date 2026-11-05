# -*- coding: utf-8 -*-
"""HIM (fedora + long black coat, eyes hidden under the brim) and HER (bob hair, cream cardigan, yellow umbrella).
Units: 0 = top, 100 = soles. All drawn at target scale; cached."""
import numpy as np, math, functools
from core import *
from sprite import SB, ramp, place

# ---------------- palettes ----------------
PAL = {
    'night': dict(  # cool street night, rim from lamps/window
        coat=ramp((40, 38, 52), (26, 25, 35), (62, 60, 80)), inner=ramp((18, 17, 24), (12, 11, 16), (30, 29, 38)),
        trou=ramp((30, 29, 40), (20, 19, 28), (46, 45, 60)), shoe=ramp((22, 20, 28), (14, 13, 18), (80, 78, 98)),
        hat=ramp((34, 31, 42), (22, 20, 28), (58, 54, 70)), band=ramp((78, 74, 92), (56, 52, 68), (104, 100, 120)),
        skin=ramp((206, 166, 156), (150, 112, 116), (236, 204, 188)), hair=ramp((24, 22, 30), (16, 14, 20), (48, 46, 62)),
        outline=(10, 9, 16), rim=(150, 164, 214), lip=(150, 100, 104),
        # her
        hhair=ramp((74, 46, 46), (50, 32, 36), (110, 72, 64)), hskin=ramp((240, 206, 188), (204, 160, 150), (255, 230, 214)),
        card=ramp((214, 204, 190), (168, 158, 150), (238, 230, 218)), dress=ramp((78, 98, 118), (56, 72, 92), (104, 128, 146)),
        legs=ramp((66, 56, 70), (48, 40, 54), (88, 76, 92)), boots=ramp((96, 64, 54), (66, 44, 40), (128, 88, 70)),
        blush=(232, 150, 150), eye=(40, 26, 34), houtline=(30, 20, 28), yellow=ramp((240, 192, 62), (196, 140, 40), (255, 226, 120)),
    ),
    'warm': dict(  # memory dusk: amber light
        coat=ramp((56, 42, 46), (38, 28, 34), (92, 66, 62)), inner=ramp((26, 20, 24), (18, 14, 18), (40, 30, 34)),
        trou=ramp((44, 34, 40), (30, 22, 28), (66, 50, 52)), shoe=ramp((30, 22, 26), (20, 14, 18), (100, 76, 70)),
        hat=ramp((46, 34, 40), (30, 22, 28), (80, 60, 60)), band=ramp((112, 90, 88), (84, 66, 66), (140, 116, 106)),
        skin=ramp((236, 186, 152), (190, 132, 112), (255, 220, 186)), hair=ramp((36, 26, 30), (24, 18, 22), (66, 50, 52)),
        outline=(26, 16, 20), rim=(255, 196, 140), lip=(176, 110, 96),
        hhair=ramp((92, 54, 44), (64, 36, 34), (136, 84, 62)), hskin=ramp((255, 214, 184), (222, 164, 140), (255, 236, 212)),
        card=ramp((240, 222, 194), (198, 172, 148), (255, 242, 222)), dress=ramp((104, 112, 120), (78, 82, 94), (134, 140, 142)),
        legs=ramp((88, 64, 66), (64, 46, 50), (112, 84, 82)), boots=ramp((120, 78, 58), (86, 54, 44), (156, 106, 76)),
        blush=(244, 150, 132), eye=(52, 30, 30), houtline=(48, 26, 28), yellow=ramp((255, 200, 70), (214, 148, 46), (255, 234, 140)),
    ),
}
PAL['room'] = dict(PAL['night'])  # her room: warm lamp; tweak later
PAL['room'].update(hskin=ramp((248, 210, 186), (212, 160, 146), (255, 234, 216)), rim=(255, 200, 150))


def ik(S, T, L1, L2, bend=1):
    sx, sy = S; tx, ty = T
    dx, dy = tx - sx, ty - sy
    d = math.hypot(dx, dy)
    d = min(d, L1 + L2 - 1e-3)
    if d < 1e-3:
        return (sx, sy + L1), (sx, sy + L1 + L2)
    a = math.atan2(dy, dx)
    c = (L1 * L1 + d * d - L2 * L2) / (2 * L1 * d)
    c = max(-1, min(1, c))
    b = math.acos(c)
    ang = a + b * bend
    E = (sx + L1 * math.cos(ang), sy + L1 * math.sin(ang))
    Tn = (sx + dx / math.hypot(dx, dy) * d, sy + dy / math.hypot(dx, dy) * d) if math.hypot(dx, dy) > 0 else T
    return E, Tn


def _kf(p, keys):
    """circular keyframe interpolation: keys list of (p, value)"""
    p = p % 1.0
    ks = keys + [(keys[0][0] + 1, keys[0][1])]
    for (a, va), (b, vb) in zip(ks[:-1], ks[1:]):
        if a <= p < b:
            u = (p - a) / (b - a)
            u = u * u * (3 - 2 * u)
            return va + (vb - va) * u
    return keys[0][1]


THIGH = [(0, 22), (0.125, 13), (0.25, 0), (0.375, -12), (0.5, -20), (0.625, -10), (0.75, 6), (0.875, 18)]
KNEE = [(0, 4), (0.125, 14), (0.25, 6), (0.375, 4), (0.5, 12), (0.625, 32), (0.75, 34), (0.875, 16)]
FOOT = [(0, -12), (0.125, 0), (0.25, 0), (0.375, 8), (0.5, 26), (0.625, 16), (0.75, 4), (0.875, -6)]


def _leg_pts(hip, p, L1=23.0, L2=22.6, stand=False):
    if stand:
        th, kn, ft = 0, 4, 0
    else:
        th, kn, ft = _kf(p, THIGH), _kf(p, KNEE), _kf(p, FOOT)
    a1 = math.radians(th)
    knee = (hip[0] + L1 * math.sin(a1), hip[1] + L1 * math.cos(a1))
    a2 = math.radians(th - kn)
    ank = (knee[0] + L2 * math.sin(a2), knee[1] + L2 * math.cos(a2))
    return knee, ank, ft


# ======================= HIM =======================

def _hat(b, view, pal, tilt=0.0, dx=0.0, dy=0.0, onher=False):
    """tilt: look-up amount 0..1 (front: shows underside of brim)"""
    P = lambda L: [(x + dx, y + dy) for x, y in L]
    if view in ('front', 'back'):
        crown = b.m_poly(P([(-7, 1.6), (-2.6, 0.3), (0, 1.3), (2.6, 0.3), (7, 1.6), (7.7, 10.2), (-7.7, 10.2)]))
        ry = 1.9 + tilt * 1.6
        brim = b.m_ell(0 + dx, 10.9 + dy - tilt * 0.6, 17.2, ry)
        b.part('brim', brim, pal['hat'], shade='cyl', hl=0.12, sh=0.3)
        if tilt > 0.05 and view == 'front':
            under = b.m_ell(0 + dx, 11.3 + dy - tilt * 0.4, 15.5, ry * 0.75) & brim
            b.paint(under & ~shift(brim, 0, 1), pal['hat'][1] * 0.8)
        b.part('crown', crown, pal['hat'], shade='cyl', hl=0.2, sh=0.32)
        band = b.m_poly(P([(-7.6, 7.6), (7.6, 7.6), (7.7, 10.2), (-7.7, 10.2)])) & crown
        b.part('band', band, pal['band'], shade='cyl', hl=0.15, sh=0.3)
        # crease line on top
        b.paint(b.m_line(P([(0, 1.4), (0, 4.5)])) & crown, pal['hat'][1])
    else:  # side, facing right
        crown = b.m_poly(P([(-6.2, 2.0), (3.5, 0.6), (6.4, 1.8), (7.4, 10.2), (-6.8, 10.2)]))
        brim = b.m_poly(P([(-12, 10.2), (-6, 9.4), (8, 9.4), (14.4, 9.8), (15.4, 10.8), (14, 11.9), (2, 11.7), (-10.5, 11.6), (-12.8, 10.9)]))
        b.part('brim', brim, pal['hat'], shade='top')
        b.part('crown', crown, pal['hat'], shade='cyl', hl=0.18, sh=0.3, light=1)
        band = b.m_poly(P([(-6.7, 7.6), (7.2, 7.6), (7.4, 10.2), (-6.8, 10.2)])) & crown
        b.part('band', band, pal['band'], shade='cyl', light=1)
        b.paint(b.m_line(P([(-2, 1.4), (2.5, 2.2)])) & crown, pal['hat'][1])


def him(view='front', s=1.0, pal='night', walk=None, look_up=0.0, hand_r=None, hand_l=None, hat=True, smile=0,
        rim=(1, 0), rim_col=None, head_turn=0.0, mouth_open=0.0):
    """view: front/side/back. walk: phase 0..1 (side view) or None (stand).
    hand_r/hand_l: target (x,y) units for IK (front/back: r = viewer's right). side: hand_r = near arm."""
    P_ = PAL[pal]
    b = SB(s, wu=96, hu=114, oxu=48, top_u=-8)
    bob = 0.9 * math.sin(4 * math.pi * walk) if walk is not None else 0.0
    oy = bob
    O = lambda L: [(x, y + oy) for x, y in L]
    sk = P_['skin']
    if view in ('front', 'back'):
        # legs + shoes
        for sg in (-1, 1):
            leg = b.m_poly([(sg * 7.4, 79), (sg * 1.0, 79), (sg * 1.3, 96.6), (sg * 6.9, 96.6)])
            b.part('leg%d' % sg, leg, P_['trou'], hl=0.2, sh=0.35)
            shoe = b.m_ell(sg * 4.3, 98.2, 4.1, 2.0) | b.m_poly([(sg * 0.6, 98.2), (sg * 8.3, 98.2), (sg * 8.2, 100), (sg * 0.6, 100)])
            b.part('shoe%d' % sg, shoe, P_['shoe'], shade='top')
        # arms behind body when hanging
        arms = []
        for sg, tgt in ((1, hand_r), (-1, hand_l)):
            Sh = (sg * 11.6, 27.6 + oy)
            T = tgt if tgt is not None else (sg * 13.4, 61.5 + oy)
            E, Tn = ik(Sh, T, 17.5, 16.5, bend=(-1 if sg > 0 else 1))
            arms.append((sg, Sh, E, Tn, tgt is not None))
        for sg, Sh, E, Tn, raised in arms:
            if not raised:
                m = b.m_cap(Sh, E, 3.1, 2.9) | b.m_cap(E, Tn, 2.9, 2.6)
                b.part('arm%d' % sg, m, P_['coat'], hl=0.22, sh=0.4, light=-1)
        coat = b.m_poly(O([(-5, 23.6), (5, 23.6), (12.8, 26), (13.7, 30), (12.4, 40), (11.6, 52), (13.6, 80.5), (-13.6, 80.5),
                          (-11.6, 52), (-12.4, 40), (-13.7, 30), (-12.8, 26)]))
        b.part('coat', coat, P_['coat'], hl=0.16, sh=0.32)
        if view == 'front':
            inner = b.m_poly(O([(-4.2, 23.8), (4.2, 23.8), (2.4, 44), (0.2, 52), (-2.4, 44)]))
            b.part('inner', inner, P_['inner'], shade='flat')
            for sg in (-1, 1):
                lap = b.m_poly(O([(sg * 4.4, 24), (sg * 7.8, 26.4), (sg * 6.0, 29.6), (sg * 7.4, 31), (sg * 4.0, 41), (sg * 2.3, 44.5)]))
                b.part('lap%d' % sg, lap, ramp(P_['coat'][2], P_['coat'][0], P_['coat'][2] * 1.15), shade='flat')
                b.paint(outline_of(lap) & coat & ~inner, P_['coat'][1])
            b.paint(b.m_line(O([(0.3, 52), (0.9, 80.5)])) & coat, P_['coat'][1])
            if s >= 1.2:
                b.paint(b.m_ell(1.6, 52.5 + oy, 0.75, 0.75), P_['coat'][2] * 1.2)
                for sg in (-1, 1):
                    b.paint(b.m_line(O([(sg * 9.4, 59), (sg * 5.6, 59.6)])) & coat, P_['coat'][1])
        else:
            b.paint(b.m_line(O([(0, 52), (0, 80.5)])) & coat, P_['coat'][1])
            b.paint(b.m_line(O([(-3, 25), (3, 25)])) & coat, P_['coat'][2])
        for sg, Sh, E, Tn, raised in arms:
            if raised:
                m = b.m_cap(Sh, E, 3.1, 2.9) | b.m_cap(E, Tn, 2.9, 2.6)
                b.part('arm%d' % sg, m, P_['coat'], hl=0.22, sh=0.4, light=-1)
        for sg, Sh, E, Tn, raised in arms:
            hx, hy = Tn
            hand = b.m_ell(hx, hy + (1.6 if not raised else -1.2), 2.2, 3.1)
            b.part('hand%d' % sg, hand, sk if view == 'front' or raised else ramp(sk[1], sk[1] * 0.8, sk[0]), hl=0.25, sh=0.4)
        # neck + head
        neck = b.m_poly(O([(-2.4, 20.5), (2.4, 20.5), (2.3, 25), (-2.3, 25)]))
        b.part('neck', neck, ramp(sk[1], sk[1] * 0.85, sk[0]), shade='flat')
        hx = head_turn * 1.2
        head = b.m_ell(hx, 16.2 + oy - look_up * 0.6, 5.7, 6.7)
        if view == 'front':
            b.part('head', head, sk, hl=0.18, sh=0.3, light=-1)
            for sg in (-1, 1):
                b.part('ear%d' % sg, b.m_ell(sg * 5.7 + hx, 15.6 + oy, 1.2, 1.7), sk, shade='flat')
            # brim shadow over the eyes (the album-cover look)
            sh_y = 15.0 - look_up * 2.4
            shadow = head & b.m_poly(O([(-8, 9), (8, 9), (8, sh_y), (-8, sh_y)]))
            b.paint(shadow, sk[1] * 0.82)
            b.paint(shadow & ~shift(shadow, 0, 1), sk[1] * 0.68)
            if look_up > 0.4 and s >= 1.0:
                for sg in (-1, 1):
                    b.paint(b.m_ell(sg * 2.3 + hx, 14.4 + oy - look_up * 0.4, 0.9, 0.5), P_['outline'])
            if s >= 1.0:
                b.paint(b.m_line(O([(0.5 + hx, 16.6), (0.9 + hx, 17.6)])), sk[1])          # nose shade
                mw = 1.7
                if smile:
                    b.paint(b.m_line(O([(-mw + hx, 19.0), (hx, 19.6), (mw + hx, 19.0)])), P_['lip'])
                else:
                    b.paint(b.m_line(O([(-mw * 0.8 + hx, 19.5), (mw * 0.8 + hx, 19.5)])), P_['lip'])
        else:
            b.part('head', head, P_['hair'], hl=0.15, sh=0.3)
            b.part('nape', b.m_ell(0, 20.5 + oy, 3.4, 2.0), ramp(sk[1], sk[1] * 0.8, sk[0]), shade='flat')
        if hat:
            _hat(b, view, P_, tilt=look_up, dy=oy - look_up * 0.6)
        else:
            hair = b.m_poly(O([(-6.2, 15), (-6.4, 10), (-4.6, 7.2), (0, 6.2), (4.6, 7.2), (6.4, 10), (6.2, 15), (4.8, 11.5), (2, 12.4), (-1.5, 11.3), (-4.6, 12.2)]))
            if view == 'back':
                hair = hair | b.m_ell(0, 14 + oy, 6.2, 6.4)
            b.part('hair', hair, P_['hair'], hl=0.18, sh=0.3)
    else:
        # ---------------- side (facing right) ----------------
        p = walk if walk is not None else 0.0
        stand = walk is None
        hip = (0.4, 52.0 + oy)
        legs = []
        for ph, nm in ((p + 0.5, 'far'), (p, 'near')):
            kn, an, ft = _leg_pts(hip, ph, stand=stand)
            legs.append((nm, kn, an, ft))
        for nm, kn, an, ft in legs:
            dark = nm == 'far'
            rp = P_['trou'] if not dark else ramp(P_['trou'][1], P_['trou'][1] * 0.8, P_['trou'][0])
            m = b.m_cap(hip, kn, 3.4, 3.1) | b.m_cap(kn, an, 3.0, 2.5)
            b.part('leg_' + nm, m, rp, hl=0.2, sh=0.35, light=1)
            fa = math.radians(ft)
            ca, sa = math.cos(fa), math.sin(fa)
            shoe_pts = [(-2.0, -1.4), (1.5, -1.8), (4.4, -0.8), (6.3, 0.6), (6.4, 1.6), (-2.3, 1.7)]
            sp = [(an[0] + x * ca - y * sa, an[1] + 1.2 + x * sa + y * ca) for x, y in shoe_pts]
            srp = P_['shoe'] if not dark else ramp(P_['shoe'][1], P_['shoe'][1], P_['shoe'][0])
            b.part('shoe_' + nm, b.m_poly(sp), srp, shade='top')
        # far arm (behind coat)
        swing = 0 if stand else 24 * math.sin(2 * math.pi * p)
        Sh = (0.6, 27.6 + oy)

        def arm_pts(sw, tgt):
            if tgt is not None:
                E, Tn = ik(Sh, tgt, 17.5, 16.5, bend=-1)
                return E, Tn
            a = math.radians(sw)
            E = (Sh[0] + 17.5 * math.sin(a), Sh[1] + 17.5 * math.cos(a))
            a2 = math.radians(sw + 12 + max(0, sw) * 0.5)
            Tn = (E[0] + 16.5 * math.sin(a2), E[1] + 16.5 * math.cos(a2))
            return E, Tn
        Ef, Tf = arm_pts(-swing, hand_l)
        mfar = b.m_cap(Sh, Ef, 3.0, 2.8) | b.m_cap(Ef, Tf, 2.8, 2.5)
        b.part('arm_far', mfar, ramp(P_['coat'][1], P_['coat'][1] * 0.85, P_['coat'][0]), shade='flat')
        b.part('hand_far', b.m_ell(Tf[0], Tf[1] + 1.4, 2.0, 2.8), ramp(sk[1], sk[1] * 0.8, sk[0]), shade='flat')
        # coat (side)
        sw_h = 0 if stand else 1.6 * math.sin(2 * math.pi * p)
        coat = b.m_poly(O([(-2.5, 23.4), (3.6, 23.4), (5.6, 27), (6.3, 33), (5.4, 44), (4.8, 52), (7.6 + sw_h, 80.5),
                          (-9.0 + sw_h * 0.6, 80.5), (-6.6, 52), (-6.4, 40), (-6.8, 30), (-5.4, 25.2)]))
        b.part('coat', coat, P_['coat'], hl=0.14, sh=0.3, light=1)
        b.paint(b.m_line(O([(3.8, 25), (5.4, 33), (4.6, 42)])) & coat, P_['coat'][2])  # lapel edge
        b.paint(b.m_line(O([(4.6, 52), (7.0 + sw_h, 80)])) & coat, P_['coat'][1])      # front opening
        if s >= 1.2:
            b.paint(b.m_line(O([(-1.6, 58), (2.6, 58.6)])) & coat, P_['coat'][1])
        # near arm
        En, Tn = arm_pts(swing, hand_r)
        mnear = b.m_cap(Sh, En, 3.1, 2.9) | b.m_cap(En, Tn, 2.9, 2.6)
        b.part('arm_near', mnear, P_['coat'], hl=0.22, sh=0.36, light=1)
        b.part('hand_near', b.m_ell(Tn[0], Tn[1] + 1.4, 2.1, 2.9), sk, hl=0.25, sh=0.3, light=1)
        # neck & head profile
        b.part('neck', b.m_poly(O([(-1.8, 20), (2.6, 20), (2.8, 25), (-2.2, 25)])), ramp(sk[1], sk[1] * 0.85, sk[0]), shade='flat')
        lu = look_up
        hy = oy - lu * 0.8
        face = b.m_poly([(x, y + hy) for x, y in [(-5.6, 12), (-5.2, 19), (-3, 22.4), (2.8, 22.8), (5.0, 21.6), (5.6, 20.2), (6.2, 19.4),
                                                  (5.9, 18.4), (7.6, 17.0), (6.6, 15.6), (6.4, 12.4), (4, 10.6), (-4, 10.6)]])
        b.part('head', face, sk, hl=0.2, sh=0.25, light=1)
        if hat:
            hairb = b.m_poly([(x, y + hy) for x, y in [(-5.9, 10.8), (-3.2, 10.8), (-2.6, 16), (-3.6, 21), (-5.6, 19.4), (-6.2, 14)]])
        else:
            hairb = b.m_poly([(x, y + hy) for x, y in [(-6.2, 15.5), (-6.5, 9.5), (-4.5, 6.6), (0.5, 5.8), (4.6, 6.8), (6.9, 9.6), (6.6, 12.4), (4.6, 11.0), (2.0, 12.0), (-0.6, 11.4), (-2.4, 14.6), (-3.6, 19.4), (-5.6, 19.4)]])
        b.part('hair', hairb, P_['hair'], hl=0.15, sh=0.3, light=1)
        if s >= 0.9:
            b.part('ear', b.m_ell(-1.0, 16.2 + hy, 1.2, 1.7), ramp(sk[1], sk[1] * 0.8, sk[0]), shade='flat')
        if hat:
            sh_y = 15.2 - lu * 2.6
            shadow = face & b.m_poly([(-8, 8 + hy), (9, 8 + hy), (9, sh_y + hy), (-8, sh_y + hy)])
            b.paint(shadow, sk[1] * 0.8)
            if lu > 0.4 and s >= 1.0:
                b.paint(b.m_ell(4.6, 14.3 + hy, 0.8, 0.5), P_['outline'])
        else:
            if s >= 1.0:
                b.paint(b.m_ell(4.4, 14.6 + hy, 0.7, 0.9 if not smile else 0.45), P_['outline'])
                b.paint(b.m_line([(3.2, 12.8 + hy), (5.4, 12.6 + hy)]), P_['hair'][0])
        if s >= 1.0:
            if smile:
                b.paint(b.m_line([(4.6, 19.6 + hy), (5.6, 19.9 + hy)]), P_['lip'])
            else:
                b.paint(b.m_line([(4.8, 19.9 + hy), (5.8, 19.9 + hy)]), P_['lip'])
        if hat:
            _hat(b, 'side', P_, dy=hy, tilt=lu)
            if lu > 0:
                pass
    rc = P_['rim'] if rim_col is None else rim_col
    spr = b.finish(outline=P_['outline'], rim=(rim[0], rim[1], rc, max(1, int(s * 0.9))) if rim else None)
    return spr, b.anchor(), b


# ======================= HER =======================

def her(view='front', s=1.0, pal='night', walk=None, hand_r=None, hand_l=None, expr='calm', blink=False, hat_on=False,
        rim=(1, 0), rim_col=None, look_up=0.0):
    """her units: she is 0.86 of his height -> caller uses s*0.86. expr: calm/smile/soft/sad/teary/surprise"""
    P_ = PAL[pal]
    b = SB(s, wu=96, hu=114, oxu=48, top_u=-10)
    bob = 0.8 * math.sin(4 * math.pi * walk) if walk is not None else 0.0
    oy = bob
    O = lambda L: [(x, y + oy) for x, y in L]
    sk = P_['hskin']
    hr = P_['hhair']
    eyec = P_['eye']
    if view in ('front', 'back'):
        for sg in (-1, 1):
            leg = b.m_poly([(sg * 5.8, 74), (sg * 1.4, 74), (sg * 1.8, 95.5), (sg * 5.0, 95.5)])
            b.part('leg%d' % sg, leg, P_['legs'], hl=0.2, sh=0.35)
            boot = b.m_poly([(sg * 1.2, 92), (sg * 5.6, 92), (sg * 6.6, 98), (sg * 6.6, 100), (sg * 0.8, 100), (sg * 1.0, 96)])
            b.part('boot%d' % sg, boot, P_['boots'], shade='top')
        arms = []
        for sg, tgt in ((1, hand_r), (-1, hand_l)):
            Sh = (sg * 9.2, 26.5 + oy)
            T = tgt if tgt is not None else (sg * 11.0, 54 + oy)
            E, Tn = ik(Sh, T, 14.6, 14.0, bend=(-1 if sg > 0 else 1))
            arms.append((sg, Sh, E, Tn, tgt is not None))
        dress = b.m_poly(O([(-4.5, 23.5), (4.5, 23.5), (8, 27), (8.4, 44), (11.2, 76), (-11.2, 76), (-8.4, 44), (-8, 27)]))
        b.part('dress', dress, P_['dress'], hl=0.16, sh=0.3)
        b.paint(b.m_line(O([(-10.5, 74.5), (10.5, 74.5)])) & dress, P_['dress'][1])
        for sg, Sh, E, Tn, raised in arms:
            if not raised:
                m = b.m_cap(Sh, E, 2.8, 2.6) | b.m_cap(E, Tn, 2.6, 2.3)
                b.part('arm%d' % sg, m, P_['card'], hl=0.2, sh=0.4, light=-1)
        if view == 'front':
            for sg in (-1, 1):
                cd = b.m_poly(O([(sg * 3.6, 23.2), (sg * 9.6, 25.4), (sg * 10.6, 30), (sg * 10.0, 44), (sg * 12.6, 66), (sg * 4.4, 66), (sg * 3.2, 44), (sg * 2.4, 30)]))
                b.part('card%d' % sg, cd, P_['card'], hl=0.2, sh=0.3, light=-1)
                b.paint(inner_edge(cd, -sg, 0, 1), P_['card'][1])
            if s >= 1.2:
                for k in range(3):
                    b.paint(b.m_ell(3.0, 34 + k * 6 + oy, 0.6, 0.6), P_['card'][1])
        else:
            cd = b.m_poly(O([(-9.6, 25.4), (9.6, 25.4), (10.6, 30), (10.0, 44), (12.6, 66), (-12.6, 66), (-10.0, 44), (-10.6, 30)]))
            b.part('card', cd, P_['card'], hl=0.16, sh=0.3)
        for sg, Sh, E, Tn, raised in arms:
            if raised:
                m = b.m_cap(Sh, E, 2.8, 2.6) | b.m_cap(E, Tn, 2.6, 2.3)
                b.part('arm%d' % sg, m, P_['card'], hl=0.2, sh=0.4, light=-1)
        for sg, Sh, E, Tn, raised in arms:
            b.part('hand%d' % sg, b.m_ell(Tn[0], Tn[1] + (1.2 if not raised else -1.0), 1.8, 2.5), sk, hl=0.25, sh=0.4)
        b.part('neck', b.m_poly(O([(-1.8, 18.5), (1.8, 18.5), (1.8, 23.8), (-1.8, 23.8)])), ramp(sk[1], sk[1] * 0.9, sk[0]), shade='flat')
        # hair back mass
        hb = b.m_poly(O([(-8.4, 8), (-9.2, 16), (-9.4, 24.5), (-6.5, 25.6), (6.5, 25.6), (9.4, 24.5), (9.2, 16), (8.4, 8)]))
        b.part('hairback', hb, ramp(hr[1], hr[1] * 0.85, hr[0]), shade='flat')
        head = b.m_ell(0, 11.6 + oy - look_up * 0.4, 7.2, 8.4)
        if view == 'front':
            b.part('head', head, sk, hl=0.2, sh=0.28, light=-1)
            # hair top + side locks + bangs
            top = b.m_poly(O([(-7.8, 9.5), (-7.2, 4.6), (-4.8, 2.0), (0, 1.0), (4.8, 2.0), (7.2, 4.6), (7.8, 9.5), (6, 7.6), (4.5, 9.6), (3, 7.8), (1.2, 9.8),
                              (-0.6, 7.8), (-2.4, 9.8), (-4.0, 7.8), (-5.6, 9.6), (-6.4, 7.8)]))
            b.part('hairtop', top, hr, hl=0.25, sh=0.3, light=-1)
            for sg in (-1, 1):
                lock = b.m_poly(O([(sg * 7.9, 7), (sg * 8.9, 14), (sg * 9.2, 22), (sg * 8.0, 25.4), (sg * 6.6, 22.8), (sg * 6.6, 14), (sg * 6.8, 9.5)]))
                b.part('lock%d' % sg, lock, hr, hl=0.3, sh=0.3, light=-1)
            if s >= 1.0:
                b.paint(b.m_line(O([(-4.6, 3.6), (-1.6, 2.5)])), hr[2])  # hair sheen
            clip = b.m_poly(O([(3.6, 4.6), (6.4, 3.8), (6.8, 5.4), (4.0, 6.2)]))
            b.part('clip', clip, P_['yellow'], shade='flat')
            # face
            ey = 12.6 + oy - look_up * 0.6
            if s >= 0.8:
                for sg in (-1, 1):
                    ex = sg * 3.1
                    if blink or expr in ('smile',):
                        b.paint(b.m_line([(ex - 1.1, ey + 0.4), (ex, ey - 0.3), (ex + 1.1, ey + 0.4)]), eyec)
                    else:
                        eh = 1.5 if expr != 'surprise' else 1.9
                        b.paint(b.m_ell(ex, ey, 0.95, eh), eyec)
                        if s >= 1.6:
                            b.paint(b.m_ell(ex - 0.3, ey - 0.6, 0.35, 0.35), (250, 245, 245))
                        if expr == 'teary' and s >= 1.4:
                            b.paint(b.m_ell(ex, ey + 1.6, 0.9, 0.4), (200, 230, 255))
                    if s >= 1.2:
                        b.paint(b.m_ell(sg * 4.6, ey + 2.6, 1.2, 0.55), P_['blush'])
                my = 16.6 + oy - look_up * 0.6
                if expr in ('smile', 'soft'):
                    b.paint(b.m_line([(-1.0, my - 0.2), (0, my + 0.4), (1.0, my - 0.2)]), (170, 92, 92))
                elif expr == 'surprise':
                    b.paint(b.m_ell(0, my + 0.2, 0.6, 0.7), (150, 80, 84))
                elif expr in ('sad', 'teary'):
                    b.paint(b.m_line([(-0.9, my + 0.3), (0, my - 0.1), (0.9, my + 0.3)]), (160, 92, 96))
                else:
                    b.paint(b.m_line([(-0.7, my), (0.7, my)]), (170, 100, 100))
        else:
            b.part('head', head | b.m_poly(O([(-8.6, 8), (8.6, 8), (9.4, 24.8), (-9.4, 24.8)])), hr, hl=0.2, sh=0.3)
            clip = b.m_poly(O([(3.6, 4.6), (6.4, 3.8), (6.8, 5.4), (4.0, 6.2)]))
            b.part('clip', clip, P_['yellow'], shade='flat')
    else:
        # side, facing right
        p = walk if walk is not None else 0.0
        stand = walk is None
        hip = (0.0, 50.0 + oy)
        for ph, nm in ((p + 0.5, 'far'), (p, 'near')):
            kn, an, ft = _leg_pts(hip, ph, L1=21.6, L2=22.4, stand=stand)
            dark = nm == 'far'
            rp = P_['legs'] if not dark else ramp(P_['legs'][1], P_['legs'][1] * 0.85, P_['legs'][0])
            b.part('leg_' + nm, b.m_cap(hip, kn, 2.6, 2.3) | b.m_cap(kn, an, 2.2, 1.9), rp, hl=0.2, sh=0.3, light=1)
            fa = math.radians(ft)
            ca, sa = math.cos(fa), math.sin(fa)
            pts = [(-1.6, -3.2), (1.6, -3.2), (2.2, -0.6), (4.8, 0.4), (5.0, 1.6), (-1.8, 1.6)]
            sp = [(an[0] + x * ca - y * sa, an[1] + 1.0 + x * sa + y * ca) for x, y in pts]
            brp = P_['boots'] if not dark else ramp(P_['boots'][1], P_['boots'][1], P_['boots'][0])
            b.part('boot_' + nm, b.m_poly(sp), brp, shade='top')
        swing = 0 if stand else 20 * math.sin(2 * math.pi * p)
        Sh = (0.4, 26.5 + oy)

        def arm_pts(sw, tgt):
            if tgt is not None:
                return ik(Sh, tgt, 14.6, 14.0, bend=-1)
            a = math.radians(sw)
            E = (Sh[0] + 14.6 * math.sin(a), Sh[1] + 14.6 * math.cos(a))
            a2 = math.radians(sw + 14)
            return E, (E[0] + 14 * math.sin(a2), E[1] + 14 * math.cos(a2))
        Ef, Tf = arm_pts(-swing, hand_l)
        b.part('arm_far', b.m_cap(Sh, Ef, 2.6, 2.4) | b.m_cap(Ef, Tf, 2.4, 2.1), ramp(P_['card'][1], P_['card'][1] * 0.9, P_['card'][0]), shade='flat')
        b.part('hand_far', b.m_ell(Tf[0], Tf[1] + 1, 1.7, 2.2), ramp(sk[1], sk[1] * 0.9, sk[0]), shade='flat')
        sk_h = 0 if stand else 1.4 * math.sin(2 * math.pi * p)
        dress = b.m_poly(O([(-3.6, 23.5), (3.4, 23.5), (5.2, 30), (4.6, 44), (8.4 + sk_h, 76), (-9.0 + sk_h, 76), (-5.4, 44), (-5.0, 30)]))
        b.part('dress', dress, P_['dress'], hl=0.16, sh=0.3, light=1)
        card = b.m_poly(O([(-3.6, 23.0), (2.8, 23.0), (5.0, 27), (5.0, 40), (5.6 + sk_h * 0.7, 66), (-8.6 + sk_h * 0.5, 66), (-6.0, 44), (-5.6, 30)]))
        b.part('card', card, P_['card'], hl=0.2, sh=0.3, light=1)
        b.paint(b.m_line(O([(3.0, 25), (4.6, 40), (5.2, 65)])) & card, P_['card'][1])
        En, Tn = arm_pts(swing, hand_r)
        b.part('arm_near', b.m_cap(Sh, En, 2.8, 2.6) | b.m_cap(En, Tn, 2.6, 2.3), P_['card'], hl=0.22, sh=0.36, light=1)
        b.part('hand_near', b.m_ell(Tn[0], Tn[1] + 1, 1.8, 2.4), sk, hl=0.25, sh=0.3, light=1)
        b.part('neck', b.m_poly(O([(-1.6, 18.5), (2.0, 18.5), (2.0, 24), (-1.8, 24)])), ramp(sk[1], sk[1] * 0.9, sk[0]), shade='flat')
        hy = oy - look_up * 0.6
        hb = b.m_poly([(x, y + hy) for x, y in [(-8.2, 8), (-8.8, 16), (-8.2, 24.6), (-3.0, 25.2), (-1.4, 21), (-2.0, 12)]])
        b.part('hairback', hb, ramp(hr[1], hr[1] * 0.85, hr[0]), shade='flat')
        face = b.m_poly([(x, y + hy) for x, y in [(-6.8, 9), (-6.6, 16), (-3.4, 20.4), (2.6, 20.6), (4.8, 18.6), (5.6, 17.0), (5.4, 16.2),
                                                  (6.8, 14.6), (6.2, 13.2), (6.6, 10.2), (4.6, 4.6), (-4, 3.4)]])
        b.part('head', face, sk, hl=0.2, sh=0.25, light=1)
        top = b.m_poly([(x, y + hy) for x, y in [(-7.8, 14), (-7.6, 6.4), (-4.4, 2.4), (0.6, 1.4), (5.0, 3.0), (7.0, 6.6), (6.6, 9.4), (5.0, 7.8), (3.8, 9.8),
                                                 (2.2, 8.2), (0.8, 10.6), (-0.6, 9.4), (-1.6, 14), (-2.6, 20), (-4.0, 24.6), (-7.6, 24.6)]])
        b.part('hairtop', top, hr, hl=0.2, sh=0.3, light=1)
        clip = b.m_poly([(x, y + hy) for x, y in [(-1.0, 3.4), (1.8, 2.6), (2.2, 4.2), (-0.6, 5.0)]])
        b.part('clip', clip, P_['yellow'], shade='flat')
        if s >= 0.8:
            ey = 12.6 + hy
            if blink or expr == 'smile':
                b.paint(b.m_line([(3.0, ey + 0.2), (4.0, ey - 0.3), (4.8, ey + 0.1)]), eyec)
            else:
                b.paint(b.m_ell(4.0, ey, 0.7, 1.4), eyec)
            if s >= 1.2:
                b.paint(b.m_ell(3.4, ey + 2.6, 1.0, 0.5), P_['blush'])
            my = 17.2 + hy
            b.paint(b.m_line([(4.2, my), (5.0, my + (0.2 if expr in ('smile', 'soft') else 0))]), (168, 96, 96))
    rc = P_['rim'] if rim_col is None else rim_col
    spr = b.finish(outline=P_['houtline'], rim=(rim[0], rim[1], rc, max(1, int(s * 0.9))) if rim else None)
    return spr, b.anchor(), b


# ======================= props =======================

def umbrella(s=1.0, pal='night', open_=1.0, view='side', tint=None):
    """yellow umbrella. units: canopy radius 22. anchor = handle bottom. open_: 0 closed .. 1 open"""
    P_ = PAL[pal]
    yl = P_['yellow'] if tint is None else ramp(tint)
    b = SB(s, wu=60, hu=60, oxu=30, top_u=0)
    shaft_top = (0, 4)
    hb = (0, 52)
    b.part('shaft', b.m_line([shaft_top, hb], 0.9), ramp((70, 60, 60)), shade='flat')
    b.part('handle', b.m_line([(0, 50), (0, 53.5), (1.5, 55.5), (3.4, 55), (3.6, 53.5)], 1.6), ramp((110, 70, 50), (80, 50, 40), (150, 100, 70)), shade='flat')
    if open_ > 0.15:
        R = 22 * (0.35 + 0.65 * open_)
        hgt = 12 * (0.6 + 0.4 * open_) + (1 - open_) * 14
        pts = []
        n = 6
        for i in range(n + 1):
            x = -R + 2 * R * i / n
            # scallop bottom edge
            pts.append((x, 4 + hgt))
            if i < n:
                xm = x + R / n
                pts.append((xm, 4 + hgt - 2.0 * open_))
        top = [(R * math.cos(a), 4 + hgt - (hgt) * math.sin(a)) for a in np.linspace(0, math.pi, 24)]
        canopy = b.m_poly(top + pts[::-1] if False else top + list(reversed(pts)))
        b.part('canopy', canopy, yl, hl=0.18, sh=0.3, light=-1)
        for i in range(1, n):
            x = -R + 2 * R * i / n
            b.paint(b.m_line([(0, 4), (x * 0.95, 4 + hgt - 1.4)]) & canopy, yl[1])
        b.paint(inner_edge(canopy, 0, 1, max(1, int(s * 0.8))), yl[1] * 0.9)
        b.part('tip', b.m_line([(0, 4), (0, 1.5)], 0.9), ramp((80, 70, 70)), shade='flat')
    else:
        rolled = b.m_poly([(0, 2), (2.2, 12), (2.6, 30), (0.8, 46), (-0.8, 46), (-2.6, 30), (-2.2, 12)])
        b.part('rolled', rolled, yl, hl=0.25, sh=0.35, light=-1)
        b.paint(b.m_line([(-2.0, 24), (2.0, 26)]) & rolled, (120, 90, 60))
    spr = b.finish(outline=P_['houtline'])
    return spr, b.X(0), b.Y(52)


# ---------------- cached wrappers + pedestrians ----------------
for _k, _coat, _tr, _hair in (('ped_a', (120, 104, 86), (54, 52, 64), (46, 36, 34)), ('ped_b', (52, 62, 96), (40, 40, 52), (30, 26, 30)),
                              ('ped_c', (88, 90, 100), (34, 34, 44), (60, 50, 44)), ('ped_d', (110, 60, 64), (40, 36, 48), (24, 22, 28))):
    _p = dict(PAL['night'])
    _p.update(coat=ramp(_coat), inner=ramp(np.asarray(_coat) * 0.6), trou=ramp(_tr), hair=ramp(_hair), rim=(170, 176, 210))
    PAL[_k] = _p


def _r(v):
    if isinstance(v, float):
        return round(v, 3)
    if isinstance(v, tuple):
        return tuple(_r(x) for x in v)
    return v


@functools.lru_cache(maxsize=512)
def _him_c(key):
    kw = dict(key)
    spr, anc, _ = him(**kw)
    return spr, anc


@functools.lru_cache(maxsize=512)
def _her_c(key):
    kw = dict(key)
    spr, anc, _ = her(**kw)
    return spr, anc


def HIM(**kw):
    if kw.get('walk') is not None:
        kw['walk'] = (math.floor(kw['walk'] * 8) % 8) / 8.0
    return _him_c(tuple(sorted((k, _r(v)) for k, v in kw.items())))


def HER(**kw):
    if kw.get('walk') is not None:
        kw['walk'] = (math.floor(kw['walk'] * 8) % 8) / 8.0
    return _her_c(tuple(sorted((k, _r(v)) for k, v in kw.items())))


@functools.lru_cache(maxsize=64)
def UMB(s, pal='night', open_=1.0, tint=None):
    return umbrella(s=s, pal=pal, open_=open_, tint=tint)


UMB_COLS = [(60, 64, 96), (40, 40, 48), (96, 60, 70), (70, 96, 84), (150, 140, 120), (84, 84, 104)]


def pedestrian(img, x, y, s, phase, kind=0, facing=1, a=1.0):
    """side-view walker with umbrella. (x,y) = feet on screen."""
    from sprite import place
    pal = ['ped_a', 'ped_b', 'ped_c', 'ped_d'][kind % 4]
    spr, anc = HIM(view='side', s=s, pal=pal, walk=phase, hat=False, hand_r=(9.0, 30.0), rim=(1 if facing > 0 else -1, 0))
    u, ux, uy = UMB(round(s * 1.15, 2), 'night', 1.0, UMB_COLS[kind % len(UMB_COLS)])
    place(img, spr, anc, x, y, a, flip=facing < 0)
    hx = x + facing * 9.0 * s
    hy = y - (100 - 30.0) * s
    blit(img, u, int(round(hx - ux)), int(round(hy - uy + 2 * s)), a)


@functools.lru_cache(maxsize=32)
def hat_sprite(s, pal='night', view='side'):
    P_ = PAL[pal]
    b = SB(s, wu=40, hu=18, oxu=20, top_u=-2)
    _hat(b, view, P_)
    spr = b.finish(outline=P_['outline'])
    return spr, (b.X(0), b.Y(10.6))
