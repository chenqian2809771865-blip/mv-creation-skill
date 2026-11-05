# opening.py: the opening title card + the user's signature watermark 「★你的署名」 (hard rule 8), screen space, 0–2 s.
# signature() is taken from 《偷偷拍下你的样子》 tp.signature; the layout is re-done for this film: the phone fills the centre
# of S01, so the card sits in the free gingham area on the left (no UI button or face covered, nothing in the lyric strip).
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


def titleCard(k):
    """a rounded green title tag (stays left of the phone: x 70–530)"""
    if k <= .01:
        return
    push()
    translate(300, 565 - 30 * (1 - k))
    scale(k)
    rotate(-.05)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-230 + 10, -100 + 14, 460, 200), 36, 36, skia.Paint(AntiAlias=True, Color=skcol(INK, .25)))
    boilSeed('optag')
    paint(rrPts(-230, -100, 460, 200, 36), wash='#43B873', fill='#2F8C55', fillOp=40, ink=INK, sw=1.4)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-214, -84, 428, 168), 26, 26,
                      skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skcol('#FFFFFF', .7)))
    text('可不可以', 0, -38, 70, '#FFFFFF', stroke=INK, strokeW=10)
    text('给我你的微信', 0, 40, 70, '#FFFFFF', stroke=INK, strokeW=10)
    boilSeed('optagh')
    paint(heartPts(205, -88, 26, 22), wash='#FF6F96', ink=INK, sw=.8)
    pop()


def openingTitle(k_in, k_out):
    """title banner + artist credit + the user's watermark (你的署名)"""
    push()
    G.c.saveLayerAlpha(None, int(255 * clamp(k_out)))
    titleCard(k_in)
    a = clamp(k_in)
    signature(250, 735, 50, a=.95 * a)
    text('MOONBOI', 470, 737, 38, '#FFF3E2', stroke=INK, strokeW=7, shadow=False, a=a)
    G.c.restore()
    pop()
