# -*- coding: utf-8 -*-
"""Jay Chou fixed leads (pixel): 'he' (navy hoodie, black hair, guitar case) and 'she' (brown bob, cream sweater, red scarf).
Rebuilt from the project spec: ~33px chibi on the 320x180 grid, busts with head ~46px wide, plus emote icons."""
import math
from functools import lru_cache
import numpy as np
from px import Cv, hx, outline, OUT, mix

P = {
    'he': dict(hair=hx('#2c2536'), hair_hi=hx('#4b4060'), top=hx('#3b5b98'), top_dk=hx('#2a4375'), top_lt=hx('#5a80c2'),
               string=hx('#dcd6cc'), pants=hx('#343a52'), pants_dk=hx('#252a3d'), shoe=hx('#e8e4de'), sole=hx('#b6b0aa'),
               skin=hx('#f2c9a8'), skin_dk=hx('#d9a083')),
    'she': dict(hair=hx('#6b3d2b'), hair_hi=hx('#94573a'), top=hx('#efe4cb'), top_dk=hx('#cdbd9c'), top_lt=hx('#fbf4e4'),
                scarf=hx('#cc3b42'), scarf_dk=hx('#972a35'), skirt=hx('#4d4560'), skirt_dk=hx('#3a334a'),
                tights=hx('#3f3747'), boot=hx('#7b4a32'), boot_dk=hx('#57321f'),
                skin=hx('#f6d0b2'), skin_dk=hx('#dfa689')),
}
BLUSH = hx('#f19a92')
MOUTH = hx('#8c3b3e')
CASE, CASE_LT, STRAP = hx('#3a2b27'), hx('#56423a'), hx('#231b1c')
PICK = hx('#e84a5f')
PHONE, SCREEN = hx('#24202e'), hx('#bfe0f0')
EYE = hx('#241c2e')
WHITE = hx('#ffffff')
TEAR, TEAR_HI = hx('#9fd4f4'), hx('#f2fbff')


class Pt:
    def __init__(self, c, ox=0, oy=0):
        self.c, self.ox, self.oy = c, ox, oy

    def p(self, x, y, col):
        self.c.px(x + self.ox, y + self.oy, col)

    def r(self, x, y, w, h, col):
        self.c.rect(x + self.ox, y + self.oy, w, h, col)

    def h(self, x0, x1, y, col):
        self.c.hline(x0 + self.ox, x1 + self.ox, y + self.oy, col)

    def v(self, x, y0, y1, col):
        self.c.vline(x + self.ox, y0 + self.oy, y1 + self.oy, col)

    def ln(self, x0, y0, x1, y1, col, w=1):
        for k in range(w):
            self.c.line(x0 + self.ox + k, y0 + self.oy, x1 + self.ox + k, y1 + self.oy, col)


# ================================================================ chibi heads
def _face(pt, cx, view, eyes, mouth, who, blush=True, look=0):
    c = P[who]
    if view == 'back':
        return
    if view == 'front':
        ex = [cx - 3 + look, cx + 3 + look]
        ey = 8
        if eyes == 'open':
            for x in ex:
                pt.v(x, ey, ey + 1, EYE)
        elif eyes == 'down':
            for x in ex:
                pt.p(x, ey + 1, EYE)
                pt.p(x - 1, ey, c['skin_dk'])
        elif eyes == 'closed':
            for x in ex:
                pt.h(x - 1, x, ey + 1, EYE)
        elif eyes == 'smile':
            for x in ex:
                pt.p(x, ey, EYE); pt.p(x - 1, ey + 1, EYE); pt.p(x + 1, ey + 1, EYE)
        elif eyes == 'wide':
            for x in ex:
                pt.v(x, ey - 1, ey + 1, EYE)
        if blush:
            pt.h(cx - 5, cx - 4, 10, BLUSH)
            pt.h(cx + 4, cx + 5, 10, BLUSH)
        mx = cx + (1 if look > 0 else 0)
        if mouth == 'smile':
            pt.h(mx - 1, mx, 11, MOUTH)
        elif mouth == 'o':
            pt.p(mx, 11, MOUTH)
        elif mouth == 'big':
            pt.h(mx - 1, mx + 1, 11, MOUTH)
        else:
            pt.h(mx - 1, mx, 11, c['skin_dk'])
    else:  # side, facing right
        ex = cx + 3
        if eyes in ('open', 'wide'):
            pt.v(ex, 8, 9, EYE)
        elif eyes == 'down':
            pt.p(ex, 9, EYE); pt.p(ex - 1, 8, c['skin_dk'])
        elif eyes == 'closed':
            pt.h(ex - 1, ex, 9, EYE)
        elif eyes == 'smile':
            pt.p(ex, 8, EYE); pt.p(ex - 1, 9, EYE); pt.p(ex + 1, 9, EYE)
        if blush:
            pt.h(cx + 2, cx + 3, 10, BLUSH)
        if mouth in ('smile', 'big'):
            pt.h(cx + 5, cx + 6, 11, MOUTH)
        elif mouth == 'o':
            pt.p(cx + 6, 11, MOUTH)
        else:
            pt.p(cx + 5, 11, c['skin_dk'])


def _head(pt, cx, view, who, eyes, mouth, blush=True, look=0, hood=False):
    c = P[who]
    H, HH, SK, SD = c['hair'], c['hair_hi'], c['skin'], c['skin_dk']
    if who == 'he':
        if view == 'front':
            pt.h(cx - 5, cx + 5, 0, H)
            pt.r(cx - 6, 1, 13, 5, H)
            pt.r(cx - 6, 6, 13, 6, SK)
            pt.h(cx - 5, cx + 5, 12, SK)
            # jagged bangs
            for x in range(cx - 5, cx + 6):
                if (x - cx) not in (-3, 0, 2):
                    pt.p(x, 6, H)
            for x in (cx - 4, cx - 1, cx + 3):
                pt.p(x, 7, H)
            pt.v(cx - 6, 6, 9, H); pt.v(cx + 6, 6, 9, H)
            pt.h(cx - 3, cx + 0, 2, HH); pt.p(cx + 1, 3, HH)
            pt.h(cx - 4, cx + 4, 12, SK)
            pt.p(cx - 6, 10, SD); pt.p(cx + 6, 10, SD)
        elif view == 'side':
            pt.h(cx - 5, cx + 4, 0, H)
            pt.r(cx - 6, 1, 12, 5, H)
            pt.r(cx - 1, 6, 8, 6, SK)
            pt.h(cx - 4, cx + 5, 12, SK)
            pt.r(cx - 6, 6, 5, 5, H)
            pt.h(cx - 5, cx - 2, 11, H)
            for x in range(cx + 1, cx + 7):
                if (x - cx) not in (4,):
                    pt.p(x, 6, H)
            pt.p(cx + 3, 7, H); pt.p(cx + 6, 7, H)
            pt.p(cx + 6, 1, H)
            pt.v(cx, 8, 9, SD)  # ear
            pt.p(cx + 7, 9, SK)  # nose
            pt.h(cx - 2, cx + 1, 2, HH)
        else:  # back
            pt.h(cx - 5, cx + 5, 0, H)
            pt.r(cx - 6, 1, 13, 10, H)
            pt.h(cx - 5, cx + 5, 11, H)
            pt.h(cx - 2, cx + 2, 12, SD)
            pt.h(cx - 3, cx + 1, 2, HH)
            pt.p(cx - 6, 8, SK); pt.p(cx + 6, 8, SK)
    else:  # she: bob + straight bangs
        if view == 'front':
            pt.h(cx - 5, cx + 5, 0, H)
            pt.r(cx - 6, 1, 13, 6, H)
            pt.r(cx - 4, 7, 9, 6, SK)
            pt.h(cx - 3, cx + 3, 12, SK)
            pt.r(cx - 7, 4, 3, 8, H); pt.r(cx + 5, 4, 3, 8, H)
            pt.h(cx - 6, cx - 5, 12, H); pt.h(cx + 5, cx + 6, 12, H)
            pt.h(cx - 3, cx + 1, 2, HH)
            pt.v(cx - 6, 6, 9, HH)
        elif view == 'side':
            pt.h(cx - 5, cx + 4, 0, H)
            pt.r(cx - 6, 1, 12, 6, H)
            pt.r(cx, 7, 7, 5, SK)
            pt.h(cx + 1, cx + 5, 12, SK)
            pt.r(cx - 7, 4, 7, 8, H)
            pt.h(cx - 6, cx - 1, 12, H)
            pt.r(cx, 6, 7, 1, H)
            pt.p(cx + 6, 1, H)
            pt.v(cx + 1, 8, 9, SD)
            pt.p(cx + 7, 9, SK)
            pt.h(cx - 3, cx + 1, 2, HH)
            pt.v(cx - 5, 6, 9, HH)
        else:
            pt.h(cx - 5, cx + 5, 0, H)
            pt.r(cx - 6, 1, 13, 11, H)
            pt.r(cx - 7, 4, 15, 8, H)
            pt.h(cx - 6, cx + 6, 12, H)
            pt.h(cx - 3, cx + 1, 2, HH)
    if view != 'back':
        if view == 'side' and who == 'he':
            pass
        _face(pt, cx, view, eyes, mouth, who, blush, look)
    if hood and who == 'he':
        HD, HDK = c['top'] if 'top' in c else P['he']['top'], P['he']['top_dk']
        HD = P['he']['top']
        if view == 'front':
            pt.h(cx - 5, cx + 5, -1, HD)
            pt.r(cx - 7, 0, 2, 13, HD); pt.r(cx + 6, 0, 2, 13, HD)
            pt.h(cx - 6, cx + 6, 0, HD); pt.h(cx - 6, cx + 6, 1, HD)
            pt.h(cx - 5, cx + 5, 2, HDK)
            pt.v(cx - 7, 2, 12, HDK); pt.v(cx + 7, 2, 12, HDK)
        elif view == 'side':
            pt.h(cx - 5, cx + 5, -1, HD)
            pt.r(cx - 7, 0, 7, 12, HD)
            pt.h(cx - 6, cx + 6, 0, HD); pt.h(cx - 6, cx + 6, 1, HD)
            pt.h(cx, cx + 6, 2, HDK)
            pt.v(cx, 2, 11, HDK)
        else:
            pt.h(cx - 5, cx + 5, -1, HD)
            pt.r(cx - 7, 0, 15, 13, HD)
            pt.v(cx, 3, 12, HDK)


# ================================================================ chibi bodies
def _arm_side(pt, sx, sy, ang, length, col, dk, skin, w=2):
    """arm from shoulder (sx,sy) at angle ang degrees (0=down, +=forward/right, 90=forward horizontal, 180=up)."""
    a = math.radians(ang)
    ex = sx + math.sin(a) * length
    ey = sy + math.cos(a) * length
    pt.ln(sx, sy, ex, ey, col, w)
    pt.ln(sx, sy, ex, ey, col, 1)
    hx_, hy_ = int(round(ex)), int(round(ey))
    pt.r(hx_, hy_, 2, 2, skin)
    return hx_, hy_


def _legs_side(pt, cx, top, s, cols, lift=0, run=False):
    """two legs side view. s in [-1,1] stride. top=hip row."""
    k = 4 if run else 3
    fx, bx = int(round(s * k)), int(round(-s * k))
    L = 7
    lw, ldk, shoe, sole = cols
    # back leg first (darker)
    for leg, off, col in ((1, bx, ldk), (0, fx, lw)):
        hx0 = cx - 1
        x1 = hx0 + off
        lift_ = lift if leg == 0 and run else 0
        for yy in range(L):
            fr = yy / (L - 1)
            xx = int(round(hx0 + (x1 - hx0) * fr))
            pt.r(xx - 1, top + yy - (lift_ if yy > 3 else 0), 3, 1, col)
        fy = top + L - lift_
        pt.r(x1 - 1, fy, 4, 1, shoe)
        pt.r(x1 - 1, fy + 1, 4, 1, sole)


@lru_cache(maxsize=4096)
def chibi(who, view='front', pose='stand', phase=0.0, eyes='open', mouth='line', arm=None, arm2=None,
          case=False, hood=False, prop=None, blush=True, look=0, wind=0, out=True, bag=False):
    """returns outlined Cv (alpha). Anchor: feet center = (w//2, h-2) of returned sprite (after outline pad).
    view: front/side/back (side faces right; flip at blit for left). pose: stand/walk/run/sit/floor/crouch.
    phase: walk cycle 0..1. arm/arm2: near/far arm angle (side view) degrees. prop: 'phone','candle','pick','leaf'."""
    Wd, Hd = 30, 40
    c = Cv(Wd, Hd, alpha=True)
    cx = 15
    base = 4  # rows of headroom so head row 0 maps to y=4
    pt = Pt(c, 0, base)
    col = P[who]
    TOP, TDK, TLT = col['top'], col['top_dk'], col['top_lt']
    SK, SD = col['skin'], col['skin_dk']
    bob = 0
    s = 0.0
    if pose in ('walk', 'run'):
        s = math.sin(phase * 2 * math.pi)
        bob = -1 if abs(math.cos(phase * 2 * math.pi)) > 0.7 else 0
        if pose == 'run':
            bob = -1 if abs(s) < 0.5 else 0
    dy = {'stand': 0, 'walk': 0, 'run': 0, 'sit': 2, 'floor': 9, 'crouch': 7}[pose]
    body = Pt(c, 0, base + dy + bob)

    # guitar case behind
    if case and who == 'he':
        if view == 'side':
            cp = Pt(c, 0, base + dy + bob)
            # neck sticking above the shoulder, body behind the back (seen edge-on), lighter rim + buckle
            cp.r(cx - 8, -2, 3, 15, CASE); cp.v(cx - 8, -2, 12, CASE_LT); cp.h(cx - 8, cx - 6, -2, CASE_LT)
            cp.r(cx - 10, 13, 6, 14, CASE); cp.v(cx - 10, 14, 25, CASE_LT); cp.h(cx - 9, cx - 5, 26, CASE_LT)
            cp.r(cx - 9, 19, 4, 1, hx('#8a6a4a'))
        elif view == 'back':
            pass
        else:
            cp = Pt(c, 0, base + dy + bob)
            cp.r(cx + 6, -2, 3, 15, CASE); cp.v(cx + 6, -2, 12, CASE_LT); cp.h(cx + 6, cx + 8, -2, CASE_LT)

    if view in ('front', 'back') and pose in ('stand', 'walk', 'run', 'sit'):
        # ---------------- legs
        if who == 'he':
            if pose == 'sit':
                body.r(cx - 5, 24, 11, 2, col['pants']); body.h(cx - 5, cx + 5, 25, col['pants_dk'])
                body.r(cx - 4, 26, 3, 3, col['pants']); body.r(cx + 2, 26, 3, 3, col['pants'])
                body.r(cx - 5, 29, 4, 1, col['shoe']); body.r(cx + 2, 29, 4, 1, col['shoe'])
                body.r(cx - 5, 30, 4, 1, col['sole']); body.r(cx + 2, 30, 4, 1, col['sole'])
            else:
                l1 = int(round(s * 1.5)) if pose != 'stand' else 0
                body.r(cx - 4, 24, 9, 1, col['pants'])
                body.r(cx - 4, 25, 4, 6 - max(0, l1), col['pants']); body.v(cx - 1, 25, 30 - max(0, l1), col['pants_dk'])
                body.r(cx + 1, 25, 4, 6 - max(0, -l1), col['pants']); body.v(cx + 4, 25, 30 - max(0, -l1), col['pants_dk'])
                body.r(cx - 5, 31 - max(0, l1), 5, 1, col['shoe']); body.r(cx - 5, 32 - max(0, l1), 5, 1, col['sole'])
                body.r(cx + 1, 31 - max(0, -l1), 5, 1, col['shoe']); body.r(cx + 1, 32 - max(0, -l1), 5, 1, col['sole'])
        else:
            if pose == 'sit':
                body.r(cx - 6, 23, 13, 3, col['skirt']); body.h(cx - 6, cx + 6, 25, col['skirt_dk'])
                body.r(cx - 3, 26, 2, 3, col['tights']); body.r(cx + 2, 26, 2, 3, col['tights'])
                body.r(cx - 4, 29, 3, 2, col['boot']); body.r(cx + 2, 29, 3, 2, col['boot'])
                body.h(cx - 4, cx - 2, 30, col['boot_dk']); body.h(cx + 2, cx + 4, 30, col['boot_dk'])
            else:
                l1 = int(round(s * 1.5)) if pose != 'stand' else 0
                body.r(cx - 3, 26, 2, 4 - max(0, l1), col['tights']); body.r(cx + 2, 26, 2, 4 - max(0, -l1), col['tights'])
                body.r(cx - 4, 30 - max(0, l1), 4, 2, col['boot']); body.h(cx - 4, cx - 1, 32 - max(0, l1), col['boot_dk'])
                body.r(cx + 1, 30 - max(0, -l1), 4, 2, col['boot']); body.h(cx + 1, cx + 4, 32 - max(0, -l1), col['boot_dk'])
                body.h(cx - 5, cx + 5, 23, col['skirt'])
                body.r(cx - 6, 24, 13, 2, col['skirt'])
                for x in (cx - 3, cx, cx + 3):
                    body.v(x, 24, 25, col['skirt_dk'])
        # ---------------- torso
        if who == 'he':
            body.r(cx - 5, 13, 11, 11, TOP)
            body.v(cx + 5, 14, 22, TDK); body.v(cx - 5, 14, 17, TLT)
            body.h(cx - 5, cx + 5, 23, TDK)
            if view == 'front':
                body.h(cx - 4, cx + 4, 13, TDK); body.h(cx - 1, cx + 1, 13, SD)
                body.v(cx - 2, 14, 17, col['string']); body.v(cx + 2, 14, 17, col['string'])
                body.h(cx - 3, cx + 3, 19, TDK); body.v(cx - 3, 19, 21, TDK); body.v(cx + 3, 19, 21, TDK)
                if case:
                    body.v(cx - 4, 13, 19, STRAP); body.v(cx + 4, 13, 19, STRAP)
            else:
                body.r(cx - 4, 13, 9, 4, TDK)
                body.v(cx, 14, 16, TOP)
                if case:
                    body.r(cx + 5, -2, 3, 16, CASE); body.v(cx + 5, -2, 13, CASE_LT); body.h(cx + 5, cx + 7, -2, CASE_LT)
                    body.r(cx - 4, 14, 9, 7, CASE); body.r(cx - 3, 21, 7, 2, CASE); body.r(cx - 5, 23, 11, 7, CASE)
                    body.r(cx - 4, 30, 9, 1, CASE)
                    body.v(cx - 4, 14, 20, CASE_LT); body.v(cx - 5, 23, 29, CASE_LT); body.h(cx - 3, cx + 3, 14, CASE_LT)
                    body.r(cx - 1, 25, 3, 2, hx('#8a6a4a'))
                    body.v(cx - 6, 13, 18, STRAP); body.v(cx + 6, 13, 18, STRAP)
        else:
            body.r(cx - 5, 15, 11, 8, TOP)
            body.v(cx + 5, 15, 22, TDK); body.h(cx - 5, cx + 5, 22, TDK)
            body.v(cx - 5, 15, 18, TLT)
            body.r(cx - 5, 13, 11, 2, col['scarf']); body.h(cx - 5, cx + 5, 14, col['scarf_dk'])
            if view == 'front':
                body.r(cx - 3, 15, 2, 4, col['scarf']); body.v(cx - 2, 15, 18, col['scarf_dk'])
                body.p(cx - 3, 19, col['scarf']); body.p(cx - 1, 19, col['scarf_dk'])
                for x in range(cx - 4, cx + 5, 2):
                    body.p(x, 13, col['scarf_dk'])
            else:
                body.r(cx + 1, 15, 2, 3, col['scarf']); body.v(cx + 2, 15, 17, col['scarf_dk'])
        # ---------------- arms (front/back) - arm param: 'phone' or None or ('up', side)
        ac = (TOP, TDK)
        if prop == 'phone' and view == 'front':
            body.r(cx - 7, 14, 2, 4, ac[0]); body.v(cx - 7, 14, 17, ac[1])
            body.r(cx + 6, 14, 2, 4, ac[0]); body.v(cx + 7, 14, 17, ac[1])
            body.r(cx - 6, 18, 4, 2, ac[0]); body.r(cx + 3, 18, 4, 2, ac[0])
            body.r(cx - 2, 15, 5, 6, PHONE); body.r(cx - 1, 16, 3, 3, SCREEN)
            body.r(cx - 3, 18, 2, 2, SK); body.r(cx + 2, 18, 2, 2, SK)
        elif arm == 'up' and view == 'front':
            body.r(cx - 7, 14, 2, 8, ac[0]); body.v(cx - 7, 14, 21, ac[1]); body.r(cx - 7, 22, 2, 2, SK)
            body.r(cx + 6, 6, 2, 9, ac[0]); body.v(cx + 7, 6, 14, ac[1]); body.r(cx + 6, 4, 2, 2, SK)
        elif arm == 'cup' and view == 'front':  # both hands together in front (holding something)
            body.r(cx - 7, 14, 2, 5, ac[0]); body.r(cx + 6, 14, 2, 5, ac[0])
            body.r(cx - 6, 19, 4, 2, ac[0]); body.r(cx + 3, 19, 4, 2, ac[0])
            body.r(cx - 2, 19, 5, 2, SK)
            if prop == 'pick':
                body.r(cx - 1, 18, 3, 2, PICK)
        else:
            if pose == 'sit':
                body.r(cx - 7, 14, 2, 7, ac[0]); body.v(cx - 7, 14, 20, ac[1]); body.r(cx - 7, 21, 2, 2, SK)
                body.r(cx + 6, 14, 2, 7, ac[0]); body.v(cx + 7, 14, 20, ac[1]); body.r(cx + 6, 21, 2, 2, SK)
            else:
                sw = int(round(s)) if pose != 'stand' else 0
                body.r(cx - 7, 14 + max(0, sw), 2, 8, ac[0]); body.v(cx - 7, 14, 21, ac[1]); body.r(cx - 7, 22, 2, 2, SK)
                body.r(cx + 6, 14 + max(0, -sw), 2, 8, ac[0]); body.v(cx + 7, 14, 21, ac[1]); body.r(cx + 6, 22, 2, 2, SK)
        if view == 'back' and who == 'she':
            body.r(cx - 1, 13, 3, 3, col['scarf_dk'])
        _head(body, cx, view, who, eyes, mouth, blush, look, hood)

    elif view == 'side' and pose in ('stand', 'walk', 'run', 'sit'):
        lean = 1 if pose == 'run' else 0
        up = Pt(c, lean, base + dy + bob)
        # far arm (behind body)
        far = arm2 if arm2 is not None else (-s * 30 if pose in ('walk', 'run') else 4)
        if pose == 'run' and arm2 is None:
            far = -s * 55
        _arm_side(up, cx - 1, 14, far, 7, TDK, TDK, SD)
        # legs
        if pose == 'sit':
            if who == 'he':
                body.r(cx - 3, 24, 9, 2, col['pants']); body.h(cx - 3, cx + 5, 25, col['pants_dk'])
                body.r(cx + 3, 26, 3, 3, col['pants'])
                body.r(cx + 3, 29, 5, 1, col['shoe']); body.r(cx + 3, 30, 5, 1, col['sole'])
            else:
                body.r(cx - 4, 23, 10, 3, col['skirt']); body.h(cx - 4, cx + 5, 25, col['skirt_dk'])
                body.r(cx + 3, 26, 2, 3, col['tights'])
                body.r(cx + 3, 29, 4, 2, col['boot']); body.h(cx + 3, cx + 6, 30, col['boot_dk'])
        else:
            if who == 'he':
                _legs_side(body, cx, 24, s, (col['pants'], col['pants_dk'], col['shoe'], col['sole']), lift=2, run=pose == 'run')
            else:
                _legs_side(body, cx, 25, s * 0.9, (col['tights'], hx('#2e2838'), col['boot'], col['boot_dk']), lift=2, run=pose == 'run')
        # torso
        if who == 'he':
            up.r(cx - 4, 13, 8, 11, TOP); up.v(cx - 4, 14, 22, TDK); up.h(cx - 4, cx + 3, 23, TDK)
            up.r(cx - 5, 13, 2, 4, TDK)
            up.h(cx - 3, cx + 3, 13, TDK)
            up.v(cx + 2, 14, 17, col['string'])
            up.h(cx, cx + 3, 19, TDK); up.v(cx, 19, 21, TDK)
            if case:
                up.ln(cx + 2, 13, cx - 3, 22, STRAP)
        else:
            up.r(cx - 4, 15, 8, 8, TOP); up.v(cx - 4, 15, 22, TDK); up.h(cx - 4, cx + 3, 22, TDK)
            up.r(cx - 4, 13, 9, 2, col['scarf']); up.h(cx - 4, cx + 4, 14, col['scarf_dk'])
            # skirt
            if pose != 'sit':
                up.r(cx - 5, 23, 10, 2, col['skirt']); up.h(cx - 5, cx + 4, 24, col['skirt_dk'])
            if wind:
                up.r(cx - 7, 13 + 0, 3, 2, col['scarf']); up.p(cx - 8, 14, col['scarf_dk']); up.p(cx - 9, 13 + (1 if wind > 1 else 0), col['scarf'])
            else:
                up.r(cx + 2, 15, 2, 3, col['scarf']); up.p(cx + 3, 17, col['scarf_dk'])
        _head(up, cx, 'side', who, eyes, mouth, blush, look, hood)
        # near arm
        near = arm if arm is not None else (s * 30 if pose in ('walk', 'run') else 0)
        if pose == 'run' and arm is None:
            near = s * 55
        if pose == 'sit' and arm is None:
            near = 25
        hxp, hyp = _arm_side(up, cx - 1, 14, near, 7, TOP, TDK, SK)
        if prop == 'phone':
            up.r(hxp, hyp - 3, 2, 4, PHONE); up.p(hxp + 1, hyp - 2, SCREEN)
        elif prop == 'candle':
            up.r(hxp, hyp - 4, 2, 4, hx('#f4ead8')); up.p(hxp, hyp - 5, hx('#ffd36a'))
        elif prop == 'pick':
            up.r(hxp, hyp - 1, 2, 2, PICK)
        elif prop == 'leaf':
            up.p(hxp + 1, hyp - 1, hx('#d8402c')); up.p(hxp + 2, hyp - 2, hx('#d8402c'))

    elif pose == 'floor':  # sitting on the floor hugging knees, side view facing right; abs rows, feet bottom = 36
        b = Pt(c, 0, 0)
        if who == 'he':
            pc, pdk = col['pants'], col['pants_dk']
        else:
            pc, pdk = col['tights'], hx('#2e2838')
        # torso (leaning forward a little)
        b.r(cx - 6, 24, 7, 11, TOP); b.v(cx - 6, 25, 34, TDK); b.r(cx - 7, 24, 2, 4, TDK)
        if who == 'she':
            b.r(cx - 7, 31, 9, 4, col['skirt']); b.h(cx - 7, cx + 1, 34, col['skirt_dk'])
        else:
            b.r(cx - 7, 32, 8, 3, pc); b.h(cx - 7, cx, 34, pdk)
        b.h(cx - 7, cx + 1, 35, pdk)
        # thigh from hip to knee, shin down to the floor
        b.ln(cx - 1, 33, cx + 3, 27, pc, 3)
        b.r(cx + 3, 26, 3, 3, pc)
        b.r(cx + 4, 28, 3, 6, pc); b.v(cx + 6, 28, 33, pdk)
        if who == 'he':
            b.r(cx + 4, 34, 5, 1, col['shoe']); b.r(cx + 4, 35, 5, 1, col['sole'])
        else:
            b.r(cx + 4, 33, 4, 2, col['boot']); b.h(cx + 4, cx + 7, 35, col['boot_dk'])
        # head resting forward on the knees (rows 13..25)
        hp = Pt(c, 0, 13)
        _head(hp, cx, 'side', who, eyes, mouth, blush, look, hood)
        if who == 'she':
            b.r(cx - 5, 24, 8, 2, col['scarf']); b.h(cx - 5, cx + 2, 25, col['scarf_dk'])
        # near arm wrapped around the shins
        b.ln(cx - 3, 26, cx + 3, 29, TOP, 2)
        b.r(cx + 4, 29, 3, 2, TOP)
        b.r(cx + 7, 29, 2, 2, SK)
    elif pose == 'crouch':  # kneel facing right, arms forward
        b = Pt(c, 0, base + 6)
        hp = Pt(c, 1, base + 6)
        if who == 'he':
            b.r(cx - 4, 13, 8, 10, TOP); b.v(cx - 4, 14, 22, TDK); b.h(cx - 3, cx + 3, 13, TDK)
            b.r(cx - 5, 13, 2, 4, TDK)
            b.r(cx - 4, 23, 10, 3, col['pants']); b.h(cx - 4, cx + 5, 25, col['pants_dk'])
            b.r(cx + 3, 23, 3, 4, col['pants'])
            b.r(cx - 6, 25, 4, 1, col['shoe']); b.r(cx - 6, 26, 4, 1, col['sole'])
        _head(hp, cx, 'side', who, eyes, mouth, blush, look, hood)
        a = arm if arm is not None else 60
        hxp, hyp = _arm_side(b, cx - 1, 14, a, 7, TOP, TDK, SK)
        if prop == 'phone':
            b.r(hxp, hyp - 3, 2, 4, PHONE); b.p(hxp + 1, hyp - 2, SCREEN)
    if bag and pose in ('stand', 'walk', 'run', 'sit'):
        _bag(c, view, cx, base + dy + bob, pose)
    res = outline(c) if out else c
    return res


BAG, BAG_DK, BAG_LT, BAG_ST = hx('#c98a3e'), hx('#9a6428'), hx('#e2aa5e'), hx('#5a3a1c')


def _bag(c, view, cx, oy, pose):
    """school backpack (tan) drawn over the finished body. oy = row offset of the body."""
    b = Pt(c, 0, oy)
    if view == 'side':  # facing right: pack sits on the back (left)
        b.r(cx - 10, 14, 5, 9, BAG); b.v(cx - 10, 15, 21, BAG_DK); b.h(cx - 10, cx - 6, 22, BAG_DK)
        b.h(cx - 9, cx - 6, 14, BAG_LT); b.r(cx - 10, 18, 4, 1, BAG_DK)
        b.ln(cx - 5, 14, cx + 1, 17, BAG_ST)
    elif view == 'back':
        b.r(cx - 5, 14, 11, 10, BAG); b.v(cx - 5, 15, 22, BAG_LT); b.v(cx + 5, 15, 23, BAG_DK)
        b.h(cx - 5, cx + 5, 23, BAG_DK); b.h(cx - 4, cx + 4, 14, BAG_LT)
        b.r(cx - 3, 18, 7, 3, BAG_DK); b.r(cx - 2, 19, 5, 1, BAG_LT)
        b.v(cx - 4, 12, 13, BAG_ST); b.v(cx + 4, 12, 13, BAG_ST)
    else:
        b.v(cx - 4, 13, 19, BAG_ST); b.v(cx + 4, 13, 19, BAG_ST)
        b.p(cx - 6, 14, BAG); b.p(cx + 6, 14, BAG)


def blit_chibi(cv, spr, x, y, flip=False, alpha_mul=1.0):
    """x,y = feet center on canvas."""
    w, h = spr.a.shape[1], spr.a.shape[0]
    # sprite feet row: base(4)+32 (+1 pad from outline) -> 37
    cv.blit(spr, x - w // 2, y - 37, flip=flip, alpha_mul=alpha_mul)


def blink(t, seed=0.0):
    return ((t + seed * 1.37) % 3.7) < 0.11


# ================================================================ busts (close-ups on the same grid)
@lru_cache(maxsize=1024)
def bust(who, eyes='open', mouth='line', brow='calm', look=0, tear=0, hood=False, wind=0, blush=True):
    """front bust. returns outlined Cv ~ 70x78. tear: 0 none, 1..12 progress steps of a tear running down left eye (and right)."""
    Wd, Hd = 72, 80
    c = Cv(Wd, Hd, alpha=True)
    pt = Pt(c)
    col = P[who]
    H, HH, SK, SD = col['hair'], col['hair_hi'], col['skin'], col['skin_dk']
    cx = 36
    # ---- shoulders / clothes
    if who == 'he':
        T, TD, TL = col['top'], col['top_dk'], col['top_lt']
        c.ellipse(cx, 84, 34, 22, T)
        pt.r(cx - 8, 56, 17, 6, SD)
        c.ellipse(cx, 64, 15, 6, TD)
        c.ellipse(cx, 63, 11, 4, SD)
        pt.v(cx - 6, 66, 74, col['string']); pt.v(cx + 6, 66, 74, col['string'])
        pt.r(cx - 7, 74, 2, 2, col['string']); pt.r(cx + 5, 74, 2, 2, col['string'])
        for x in range(cx + 18, cx + 34):
            pt.v(x, 70 + (x - cx - 18) // 3, 79, TD)
        pt.h(cx - 28, cx - 18, 70, TL)
    else:
        T, TD = col['top'], col['top_dk']
        c.ellipse(cx, 86, 34, 22, T)
        for x in range(cx + 18, cx + 34):
            pt.v(x, 72 + (x - cx - 18) // 3, 79, TD)
        pt.r(cx - 8, 54, 17, 6, SD)
        # scarf thick with knit stripes
        c.ellipse(cx, 62, 22, 8, col['scarf'])
        for x in range(cx - 20, cx + 21, 3):
            for y in range(56, 70):
                if c.a[y, x, 3] and tuple(c.a[y, x, :3]) == col['scarf']:
                    c.a[y, x, :3] = col['scarf_dk']
        pt.r(cx - 14, 64, 8, 14, col['scarf'])
        for x in range(cx - 14, cx - 6, 3):
            pt.v(x, 64, 77, col['scarf_dk'])
        for x in range(cx - 14, cx - 6, 2):
            pt.p(x, 78, col['scarf_dk'])
        pt.h(cx - 18, cx + 18, 69, col['scarf_dk'])
    # ---- head shape
    if who == 'he':
        c.ellipse(cx, 25, 25, 19, H)
        if hood:
            c.ellipse(cx, 22, 31, 23, col['top'])
            c.ellipse(cx, 25, 27, 20, col['top_dk'])
            c.ellipse(cx, 26, 25, 18, H)
            pt.r(cx - 31, 26, 6, 32, col['top']); pt.r(cx + 26, 26, 6, 32, col['top'])
        pt.r(cx - 24, 22, 5, 16, H); pt.r(cx + 20, 22, 5, 16, H)
    else:
        c.ellipse(cx, 26, 27, 20, H)
        pt.r(cx - 27, 24, 9, 28, H); pt.r(cx + 19, 24, 9, 28, H)
        c.ellipse(cx - 22, 51, 6, 4, H); c.ellipse(cx + 23, 51, 6, 4, H)
        if wind:
            pt.r(cx + 27, 28, 4, 8, H); pt.r(cx + 30, 33, 3, 5, H)
    # ears
    c.ellipse(cx - 21, 38, 3, 4, SK); c.ellipse(cx + 21, 38, 3, 4, SK)
    pt.v(cx - 21, 36, 39, SD); pt.v(cx + 21, 36, 39, SD)
    if who == 'she':
        pt.r(cx - 27, 30, 6, 22, H); pt.r(cx + 22, 30, 6, 22, H)
    # face
    c.ellipse(cx, 38, 20, 19, SK)
    pt.r(cx - 20, 30, 41, 9, SK)
    pt.h(cx - 9, cx + 9, 57, SD)
    if who == 'he':
        jag = [1, 3, 0, 4, 2, 0, 3, 1, 4, 0, 2, 3, 1, 0, 4, 2, 1, 3, 0, 2, 4, 1, 0]
        for i, x in enumerate(range(cx - 22, cx + 23, 2)):
            d = jag[i % len(jag)]
            pt.r(x, 12, 2, 10 + d, H)
        for x in (cx - 21, cx - 1, cx + 19):
            pt.r(x, 20, 2, 7, H)
        pt.h(cx - 12, cx - 2, 9, HH); pt.h(cx - 14, cx - 9, 10, HH); pt.h(cx + 4, cx + 9, 8, HH)
        pt.r(cx - 6, 12, 2, 6, HH); pt.r(cx + 8, 11, 2, 5, HH)
    else:
        pt.r(cx - 22, 12, 45, 13, H)
        for x in range(cx - 20, cx + 21, 5):
            pt.v(x, 20, 24, hx('#5a3223'))
        pt.h(cx - 12, cx + 2, 9, HH); pt.h(cx - 14, cx - 8, 10, HH)
        pt.v(cx - 25, 28, 46, HH); pt.v(cx - 26, 32, 42, HH)
    # ---- brows
    by = 26 if who == 'he' else 27
    bcol = H
    if brow == 'sad':
        pt.h(cx - 15, cx - 10, by + 1, bcol); pt.h(cx - 11, cx - 8, by, bcol)
        pt.h(cx + 10, cx + 15, by + 1, bcol); pt.h(cx + 8, cx + 11, by, bcol)
    elif brow == 'up':
        pt.h(cx - 15, cx - 9, by - 1, bcol); pt.h(cx + 9, cx + 15, by - 1, bcol)
    elif brow == 'knit':
        pt.h(cx - 15, cx - 10, by, bcol); pt.p(cx - 9, by + 1, bcol)
        pt.h(cx + 10, cx + 15, by, bcol); pt.p(cx + 9, by + 1, bcol)
    else:
        pt.h(cx - 15, cx - 9, by, bcol); pt.h(cx + 9, cx + 15, by, bcol)
    # ---- eyes
    ey = 30
    for sx in (-1, 1):
        ex = cx + sx * 12 - 2 + look
        if eyes == 'open' or eyes == 'wide':
            hh = 7 if eyes == 'wide' else 6
            pt.r(ex, ey, 4, hh, EYE)
            pt.r(ex, ey, 2, 2, WHITE)
            pt.p(ex + 3, ey + hh - 2, hx('#6a5a7a'))
            pt.h(ex - 1, ex + 4, ey - 1, EYE)
        elif eyes == 'down':
            pt.r(ex, ey + 3, 4, 3, EYE)
            pt.h(ex - 1, ex + 4, ey + 2, EYE)
            pt.p(ex, ey + 3, WHITE)
        elif eyes == 'closed':
            pt.h(ex - 1, ex + 4, ey + 4, EYE)
            pt.p(ex - 1, ey + 3, EYE); pt.p(ex + 4, ey + 3, EYE)
        elif eyes == 'smile':
            pt.h(ex, ex + 3, ey + 2, EYE)
            pt.p(ex - 1, ey + 3, EYE); pt.p(ex + 4, ey + 3, EYE)
        elif eyes == 'wet':
            pt.r(ex, ey, 4, 6, EYE)
            pt.r(ex, ey, 2, 2, WHITE); pt.r(ex + 2, ey + 3, 2, 1, hx('#a6d6f6'))
            pt.h(ex - 1, ex + 4, ey + 6, TEAR)
            pt.h(ex - 1, ex + 4, ey - 1, EYE)
    # ---- nose
    pt.h(cx - 1, cx, 40, SD); pt.p(cx + 1, 39, SD)
    # ---- blush (dithered dots)
    if blush:
        for (bx, byy) in ((cx - 17, 41), (cx + 12, 41)):
            for yy in range(3):
                for xx in range(6):
                    if (xx + yy) % 2 == 0:
                        pt.p(bx + xx, byy + yy, BLUSH)
    # ---- mouth
    my = 46
    if mouth == 'line':
        pt.h(cx - 2, cx + 2, my, SD)
    elif mouth == 'smile':
        pt.h(cx - 2, cx + 2, my + 1, MOUTH); pt.p(cx - 3, my, MOUTH); pt.p(cx + 3, my, MOUTH)
    elif mouth == 'bigsmile':
        pt.h(cx - 4, cx + 4, my - 1, MOUTH)
        pt.r(cx - 3, my, 7, 2, MOUTH); pt.h(cx - 2, cx + 2, my + 2, MOUTH)
        pt.h(cx - 3, cx + 3, my, WHITE)
        pt.h(cx - 1, cx + 1, my + 2, hx('#e2747a'))
    elif mouth == 'sad':
        pt.h(cx - 2, cx + 2, my, MOUTH); pt.p(cx - 3, my + 1, MOUTH); pt.p(cx + 3, my + 1, MOUTH)
    elif mouth == 'bite':
        pt.h(cx - 3, cx + 3, my, MOUTH); pt.h(cx - 1, cx + 1, my - 1, WHITE)
    elif mouth == 'o':
        pt.r(cx - 1, my - 1, 3, 3, MOUTH)
    # ---- tears
    if tear:
        for sx in (-1, 1):
            ex = cx + sx * 12 - 1
            n = min(tear, 14)
            for k in range(n):
                y = ey + 6 + k
                xx = ex + (1 if k > 6 else 0) * sx
                pt.p(xx, y, TEAR)
            # droplet head
            y = ey + 6 + n
            pt.r(ex - 1 + (sx if n > 6 else 0), y, 2, 2, TEAR); pt.p(ex - 1 + (sx if n > 6 else 0), y, TEAR_HI)
    return outline(c)


# ================================================================ emotes
EMOTES = {
    'note': ["..##", "..#.#", "..#..", "..#..", "###..", "###..", ],
    'heart': [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."],
    'dots': ["#.#.#"],
    'excl': ["#", "#", "#", ".", "#"],
    'q': [".##.", "#..#", "...#", "..#.", "....", "..#."],
}


def emote(kind, col=(255, 255, 255), bubble=True):
    rows = EMOTES[kind]
    h, w = len(rows), max(len(r) for r in rows)
    pad = 3 if bubble else 0
    c = Cv(w + 2 * pad, h + 2 * pad + (2 if bubble else 0), alpha=True)
    if bubble:
        c.rect(1, 0, w + 2 * pad - 2, h + 2 * pad, (255, 250, 244))
        c.rect(0, 1, w + 2 * pad, h + 2 * pad - 2, (255, 250, 244))
        c.rect(pad, h + 2 * pad, 2, 1, (255, 250, 244)); c.px(pad, h + 2 * pad + 1, (255, 250, 244))
    for y, r in enumerate(rows):
        for x, ch in enumerate(r):
            if ch == '#':
                c.px(x + pad, y + pad, col)
    return outline(c) if bubble else c
