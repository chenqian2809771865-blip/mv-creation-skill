# opening.py: 《苦咖啡·唯一》 A1 opening — the chalk A-board in S01 IS the title (written one character a beat, complete on k4).
# Screen layer adds only the user's signature 「★你的署名」 + the artist credit, beside the board title (hard rule 8), k4 -> k8.
# signature() is the shared one from 《偷偷拍下你的样子》 / 《可不可以给我你的微信》.
from eng import *

WENKAI = 'LXGWWenKai-Regular.ttf'
from mv_config import load_signature


def signature(x, y, size=44, a=.92, rot=-.06, col='#FFFFFF'):
    SIGN = load_signature().lstrip('★')
    """small hand-lettered signature with a little star, placed beside the song title"""
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
    """A1: no title card — only the signature + artist, right of the chalk board (sky, no face, out of the lyric strip)"""
    push()
    G.c.saveLayerAlpha(None, int(255 * clamp(k_out)))
    a = clamp(k_in)
    s = lerp(.85, 1.0, clamp(k_in))
    translate(1345, 320)
    scale(s)
    signature(0, 0, 50, a=.95 * a)
    text('那奇沃夫 / KKECHO', 10, 70, 36, '#FFF3E2', face=WENKAI, stroke=INK, strokeW=6, shadow=False, a=a)
    G.c.restore()
    pop()
