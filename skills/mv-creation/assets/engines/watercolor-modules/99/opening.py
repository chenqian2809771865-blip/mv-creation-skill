# opening.py: 《99》 opening credit (hard rule 8, A1 title device). The title 「99」 is the page of the wall day calendar in S01
# (「在一起的第 99 天」), so there is no extra title card: only the user's signature 「★你的署名」 + the artist, beside the calendar,
# appearing on the beat the 「98」 page is torn away (k1) and gone before the cut to S02 (k4).
from eng import *

WENKAI = 'LXGWWenKai-Regular.ttf'
from mv_config import load_signature


def signature(x, y, size=44, a=.92, rot=-.06, col='#FFFFFF'):
    SIGN = load_signature().lstrip('★')
    """small hand-lettered signature with a little star (same as 《偷偷拍下你的样子》 tp.signature)"""
    if a <= .01:
        return
    push()
    translate(x, y)
    rotate(rot)
    w = textW(SIGN, size, WENKAI)
    boilSeed('signstar')
    paint(starPts(-w / 2 - size * .55, -size * .05, size * .38, .45, 5), wash='#FFE36E', washOp=int(255 * a), ink=INK, sw=.5)
    text(SIGN, 0, 0, size, col, face=WENKAI, stroke=INK, strokeW=size * .14, shadow=False, a=a)
    pop()


def openingTitle(k_in, k_out):
    """signature + artist beside the calendar page 「99」 (S01, A1 title device; screen space, S01's camera barely moves)"""
    push()
    G.c.saveLayerAlpha(None, int(255 * clamp(k_out)))
    a = clamp(k_in)
    s = .7 + .3 * k_in
    push()
    translate(1340, 420)
    scale(s)
    signature(0, 0, 50, a=.95 * a)
    text('TizzyT', 10, 72, 38, '#FFF3E2', stroke=INK, strokeW=7, shadow=False, a=a)
    pop()
    G.c.restore()
    pop()
