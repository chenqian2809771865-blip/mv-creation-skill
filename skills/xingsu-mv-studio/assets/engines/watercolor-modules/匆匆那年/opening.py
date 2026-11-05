# opening.py: 《匆匆那年》 opening credit (the chalk title on the blackboard, S02); was 《我好想你》 (hard rule 8, A1 title device). The title is the yellow note in S01 on which the pen writes
# 「我好想你」 (complete on K16); so there is no title card — only 「★你的署名」 + the artist, beside the note, fading in on K16 and
# gone by K24 (slow song: 0.4 s fades, no bounce). Screen space; S01's camera holds still from K16 to K24.
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
    """signature + artist at the lower right of the chalk title (S02: title spans screen x ~345–1455, y ~360–520)"""
    a = clamp(k_in) * clamp(k_out)
    if a <= .01:
        return
    push()
    translate(1600, 572)
    signature(0, 0, 50, a=.95 * a)
    text('王菲', 14, 72, 38, '#FFF3E2', face=WENKAI, stroke=INK, strokeW=6, shadow=False, a=a)
    pop()
