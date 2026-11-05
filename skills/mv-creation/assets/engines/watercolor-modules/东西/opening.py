# opening.py: the opening title tag + the user's signature watermark 「★你的署名」 (hard rule 8), screen space.
# S01 is a top-down shop counter with the phone right of centre, so the title is a kraft price tag in the free counter space on
# the left (x 90–560); nothing over the phone UI, nothing in the lyric strip, nothing in the bottom-right corner.
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


def titleTag(k):
    """a kraft price tag on a string: 「东西」 + 林俊呈"""
    if k <= .01:
        return
    push()
    translate(330, 470 - 24 * (1 - k))
    scale(k)
    rotate(-.07)
    # string to the top-left
    boilSeed('tagstr')
    inkLine([[-205, -40], [-260, -120], [-300, -150]], 1.4, '#8E6A3E', 'ink', .5)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-215 + 12, -125 + 16, 450, 250), 26, 26, skia.Paint(AntiAlias=True, Color=skcol(INK, .22)))
    boilSeed('optag')
    tag = [[-170, -125], [225, -125], [225, 125], [-170, 125], [-225, 40], [-225, -40]]
    paint(tag, wash='#E9CC92', fill='#C9A062', fillOp=60, ink=INK, sw=1.5, curv=.08)
    G.c.drawCircle(-182, 0, 15, skia.Paint(AntiAlias=True, Color=skcol('#8E6A3E')))
    G.c.drawCircle(-182, 0, 9, skia.Paint(AntiAlias=True, Color=skcol('#F6E9CF')))
    # dashed inner border
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skcol('#9E7A48', .8),
                    PathEffect=skia.DashPathEffect.Make([14, 9], 0))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-140, -103, 342, 206), 14, 14, pa)
    text('东西', 32, -12, 128, '#D9573E', stroke=INK, strokeW=12, shadow=False)
    text('林俊呈', 32, 76, 34, '#5A4330', face=WENKAI, shadow=False)
    # a tiny compass doodle in the corner
    boilSeed('tagcmp')
    paint(ellPts(180, -84, 20, 20, 16), wash='#FFF5E2', ink=INK, sw=.6)
    paint([[180, -100], [186, -84], [180, -68], [174, -84]], wash='#E8476E', ink=None)
    pop()


def openingTitle(k_in, k_out):
    """title tag + the user's watermark (你的署名). k_in drives the tag's scale; the layer alpha is k_out."""
    push()
    G.c.saveLayerAlpha(None, int(255 * clamp(k_out)))
    titleTag(k_in)
    a = clamp(k_in)
    signature(345, 690, 50, a=.95 * a)
    G.c.restore()
    pop()
