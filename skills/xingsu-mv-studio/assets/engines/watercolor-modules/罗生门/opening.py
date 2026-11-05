# opening.py: 《罗生门》 opening credit. B-style prologue: the title card is S03 (the gate, 「罗生门 / Follow」 drawn in the shot,
# K36 = 16.88, the hats come in). 「★你的署名」 + the artists sit right under the title, fading in with the card (slow song: 0.4 s) and
# gone before the cut at K44 = 20.64 (hard rule 8). Screen space.
from eng import *

WENKAI = 'LXGWWenKai-Regular.ttf'
from mv_config import load_signature


def signature(x, y, size=44, a=.92, rot=-.06, col='#FFFFFF'):
    SIGN = load_signature().lstrip('★')
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
    a = clamp(k_in) * clamp(k_out)
    if a <= .01:
        return
    signature(W / 2 + 20, 462, 50, a=.95 * a)
    text('梨冻紧 / Wiz_H张子豪', W / 2, 522, 32, '#FFF3E2', face=WENKAI, stroke=INK, strokeW=5, shadow=False, a=a)
