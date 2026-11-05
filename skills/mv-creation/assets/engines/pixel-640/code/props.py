# -*- coding: utf-8 -*-
"""Hand sprite (writing finger / open palm) drawn directly at target scale (no resampling)."""
import numpy as np, math
from core import *

SKIN_D = C('#5a3e48'); SKIN_M = C('#7a525a'); SKIN_L = C('#d39478'); NAIL = C('#a07f86'); SKIN_RIM = C('#c3c4ea')
SLEEVE = C('#17161f'); SLEEVE_L = C('#2a2a3a'); RIM = C('#a9b4dc'); OUT = C('#0c0b12')


def _rot(pts, a, S, ox, oy):
    ca, sa = math.cos(a), math.sin(a)
    return [(ox + (x * ca - y * sa) * S, oy + (x * sa + y * ca) * S) for x, y in pts]


def _capsule(p0, p1, r, n=10):
    (x0, y0), (x1, y1) = p0, p1
    a = math.atan2(y1 - y0, x1 - x0)
    pts = []
    for i in range(n + 1):
        th = a + math.pi / 2 + math.pi * i / n
        pts.append((x0 + r * math.cos(th), y0 + r * math.sin(th)))
    for i in range(n + 1):
        th = a - math.pi / 2 + math.pi * i / n
        pts.append((x1 + r * math.cos(th), y1 + r * math.sin(th)))
    return pts


def pointing_hand(img, fx, fy, angle=-0.5, S=1.5, rim_dir=(-1, -1), skin=(SKIN_D, SKIN_M, SKIN_L), sleeve=(SLEEVE, SLEEVE_L)):
    """fingertip at (fx,fy); hand extends toward +local y rotated by angle (radians). back of hand to camera."""
    R = lambda pts: _rot(pts, angle, S, fx, fy)
    finger = m_poly(R(_capsule((0, 2.5), (0, 36), 4.6)))
    # curled fingers sit to the right of the index finger, thumb clearly out on the left -> reads as a writing index finger
    fist = m_poly(R([(-3, 36), (2, 32), (8, 34), (13, 33), (18, 36), (22, 42), (23, 56), (19, 64), (4, 66), (-4, 60), (-5, 46)]))
    thumb = m_poly(R(_capsule((-4, 58), (-15, 38), 4.4)))
    wrist = m_poly(R([(-2, 58), (24, 56), (30, 84), (2, 90)]))
    sleeve = m_poly(R([(-6, 80), (34, 72), (60, 160), (70, 260), (-30, 280), (-26, 160)]))
    cuff = m_poly(R([(-6, 80), (34, 72), (37, 82), (-4, 91)]))
    hand = finger | fist | thumb | wrist
    sil = hand | sleeve
    # outline
    fill(img, outline_of(sil, diag=True), OUT)
    # sleeve
    fill(img, sleeve, sleeve[0] if False else SLEEVE)
    fill(img, sleeve & ~shift(sleeve, 3, 3), SLEEVE_L)
    fill(img, cuff, C('#22212e'))
    fill(img, inner_edge(cuff, 0, -1) & cuff, C('#34344a'))
    # skin
    fill(img, hand, skin[1])
    fill(img, hand & ~shift(hand, -3, -1), skin[0])  # far side in shadow
    # finger separation lines on fist (curled fingers)
    for k in range(3):
        ln = m_line(R([(7 + k * 5, 35), (8 + k * 5, 45)]), 1)
        fill(img, ln & fist & ~finger, skin[0])
    fill(img, outline_of(finger) & fist, skin[0])
    fill(img, outline_of(thumb) & fist, skin[0])
    # nail on finger tip (back of finger)
    nail = m_poly(R(_capsule((0, 4.5), (0, 9), 2.4))) & finger
    fill(img, nail, NAIL)
    # rim light from window side
    # warm lamp from the left, cool window rim on the upper edges
    fill(img, inner_edge(hand, -1, 0, 2) & ~inner_edge(hand, 0, -1, 1), skin[2])
    fill(img, inner_edge(hand, 0, -1, 1), SKIN_RIM)
    fill(img, inner_edge(sleeve, -1, 0, 1), C('#6a4a4a'))
    fill(img, inner_edge(sleeve, 0, -1, 1), RIM * 0.6)
    return sil
