# nn.py: props, looks and helpers for 《99》 (TizzyT). 疑心病 Clawd couple: him clay orange (no hat), her pink + white flower.
# Title device: a big tear-off day calendar 「在一起的第 99 天」 (S01), torn to 「100」 in the last shot (S25).
import math
from hb import *
import hb, nm, tp, wx, ch, sets, sets2, hl, props
from sets2 import seat
import clawd as _cl

RED = '#E0344E'
SKY = '#8FC7FF'


# ------------------------------------------------------------------ cast
def himN(x, y, u, o=None):
    him(x, y, u, o)


def herN(x, y, u, o=None):
    her(x, y, u, o)


_hatPrev = _cl.hat


def _hat99(u, h, sw, o=None):
    if h == 'straw':                       # summer straw hat (drawn before her flower so the flower sits on the band)
        boilSeed('straw')
        paint(ellPts(0, -7.95 * u, 6.4 * u, 1.05 * u, 26), wash='#F2D58A', fill='#C9A24E', fillOp=60, ink=INK, sw=sw * .7)
        d = []
        for i in range(15):
            a = math.pi + i / 14 * math.pi
            d.append([math.cos(a) * 3.4 * u, -8.2 * u + math.sin(a) * 2.5 * u])
        paint(d, wash='#F6DE98', fill='#C9A24E', fillOp=50, ink=INK, sw=sw * .7)
        paint(rectPts(-3.4 * u, -9.3 * u, 6.8 * u, .8 * u), wash='#E8476E', ink=INK, sw=sw * .5)
        flowerAt(-2.4 * u, -9.0 * u, u, sw, .8)
    else:
        _hatPrev(u, h, sw, o)


_cl.hat = _hat99


# ------------------------------------------------------------------ small timing helpers
def gone(t, k, lead=.04):
    return t >= B[k] - lead


def jumpAt(t, k, h=1.8, d=.42):
    """dy (in u) of a little hop that lands ON beat k"""
    a = t - (B[k] - d)
    if a < 0 or a > d:
        return 0.0
    f = a / d
    return -h * 4 * f * (1 - f)


def hopOn(t, k, h=1.2, d=.3):
    """dy of a hop that starts ON beat k (takes off on the beat)"""
    a = t - (B[k] - .02)
    if a < 0 or a > d:
        return 0.0
    f = a / d
    return -h * 4 * f * (1 - f)


# ------------------------------------------------------------------ walls / rooms (no windows)
def wallRoom(t, c1='#F7DCCF', c2='#F2C9BA', floor=840, floorCol='#C8905E', key='wr', lights=True, decor=True, dots='#E9B8A6'):
    gradRect(-400, -400, W + 800, floor + 400, [c1, c2])
    for i in range(-4, 40):
        for j in range(-4, 16):
            if (i + j) % 2 == 0:
                G.c.drawCircle(i * 64 + (32 if j % 2 else 0), j * 72, 4, skia.Paint(AntiAlias=True, Color=skcol(dots, .55)))
    flatRect(-400, floor, W + 800, 600, floorCol)
    for i in range(-4, 26):
        G.c.drawLine(i * 120, floor, i * 120 - 70, floor + 300, skia.Paint(AntiAlias=True, Color=skcol(mixCol(floorCol, INK, .35), .35), StrokeWidth=2))
    flatRect(-400, floor - 18, W + 800, 18, mixCol(c2, '#FFFFFF', .35))
    inkLine([[-400, floor], [W + 400, floor]], 1.0, INK, 'ink', 0)
    if lights:
        sets2.fairyLights(t, -60, W + 60, 70, sag=60, n=22, key=key + 'fl')


def plantPot(x, y, s, key='pl', col='#7CC36B'):
    boilSeed(key)
    for i, (a, L) in enumerate([(-.6, 1.6), (-.2, 2.0), (.25, 1.8), (.7, 1.4), (0, 2.3)]):
        tx, ty = x + math.sin(a) * L * s, y - 1.0 * s - math.cos(a) * L * s
        paint(ellPts(tx, ty, .38 * s, .75 * s, 14, 0, a), wash=col, fill=mixCol(col, INK, .25), fillOp=60, ink=INK, sw=.6)
        inkLine([[x, y - .9 * s], [tx, ty + .5 * s]], .6, mixCol(col, INK, .4), 'inkfine', .2)
    paint([[x - .7 * s, y - 1.1 * s], [x + .7 * s, y - 1.1 * s], [x + .5 * s, y], [x - .5 * s, y]], wash='#D9825A', fill='#A85A3A', fillOp=60, ink=INK, sw=.8)


# ------------------------------------------------------------------ the day calendar (title device)
def calPage(num, w, h, key, head='在一起的第', foot='天', heartK=0.0, sub=None, numCol=None):
    """page drawn in local coords, top centre at (0, 0)"""
    boilSeed(key + 'pg' + num)
    paint(rectPts(-w / 2, 0, w, h), wash='#FFFDF6', ink=INK, sw=1.0)
    flatRect(-w / 2 + 8, 8, w - 16, h * .17, '#F9CFDA')
    text(head, 0, h * .1, h * .074, '#B8324F', face=WENKAI, shadow=False)
    ns = h * (.47 if len(num) < 3 else .36)
    text(num, 0, h * (.5 if not sub else .47), ns, numCol or RED, stroke=INK, strokeW=ns * .035, shadow=False)
    text(foot, 0, h * (.78 if sub else .83), h * .095, '#6A5A70', face=WENKAI, shadow=False)
    if sub:
        text(sub, 0, h * .92, h * .1, '#B8324F', face=WENKAI, shadow=False)
    if heartK > .01:
        heart(w * .3, h * .83, h * .045 * backOut(heartK), HOT, key=key + 'ph')


def dayCal(cx, top, w, h, num, t, key='dc', heartK=0.0, tear=None, curl=0.0, under=None, glint=0.0, sub=None):
    """tear-off calendar hanging on a nail: (cx, top) = top centre of the pad. tear = (num, k 0..1) page flying off on top.
    curl = 0..1 the current page's lower-right corner lifting (about to be torn). under = page num shown under a lifting page."""
    boilSeed(key)
    inkLine([[cx - w * .22, top - 6], [cx, top - 70], [cx + w * .22, top - 6]], .9, '#7A6A80', 'inkfine', .2)
    G.c.drawCircle(cx, top - 72, 7, skia.Paint(AntiAlias=True, Color=skcol(INK)))
    paint(rectPts(cx - w / 2 + 14, top + 16, w, h), wash=INK, washOp=50, ink=None)
    paint(rectPts(cx - w / 2 - 12, top - 14, w + 24, h + 28), wash='#E8476E', fill='#B8324F', fillOp=50, ink=INK, sw=1.1)
    for i in range(3):              # page edges below (a thick pad)
        flatRect(cx - w / 2 + 4, top + h + 2 + i * 5, w - 8, 3, '#E9DCCB')
    push()
    translate(cx, top)
    if under is not None and curl > .01:
        calPage(under, w, h, key + 'u', sub='未完待续' if under == '100' else None)
    if curl > .01:
        # the current page, with its lower right corner peeled up
        G.c.save()
        cut = skia.Path()
        cw = w * .55 * curl
        cut.moveTo(-w / 2 - 2, -2)
        cut.lineTo(w / 2 + 2, -2)
        cut.lineTo(w / 2 + 2, h - cw)
        cut.lineTo(w / 2 - cw, h + 2)
        cut.lineTo(-w / 2 - 2, h + 2)
        cut.close()
        G.c.clipPath(cut, skia.ClipOp.kIntersect, True)
        calPage(num, w, h, key, heartK=heartK)
        G.c.restore()
        boilSeed(key + 'curl')
        paint([[w / 2, h - cw], [w / 2 - cw, h], [w / 2 - cw * 1.05, h - cw * 1.05]], wash='#F3EBDC', fill='#D9CBB6', fillOp=90, ink=INK, sw=.8)
    else:
        calPage(num, w, h, key, heartK=heartK, sub=sub)
    if glint > .01:
        for i in range(8):
            a = i / 8 * TAU + .3
            r = w * .62 + 40 * (1 - glint)
            sparkle(math.cos(a) * r, h * .5 + math.sin(a) * r * .9, 26 * glint, '#FFC93D', glint)
    pop()
    for i in range(5):              # binding rings
        rx = cx - w / 2 + 40 + i * (w - 80) / 4
        paint(rrPts(rx - 9, top - 34, 18, 50, 9), wash='#C9C1D6', ink=INK, sw=.6)
    if tear:
        pg, k = tear
        if 0 <= k < 1:
            push()
            ang = .65 * easeIn(k) + .1 * k
            translate(cx + 260 * k, top - 40 * math.sin(k * 3) - 900 * easeIn(k))
            rotate(ang)
            calPage(pg, w, h, key + 't')
            pop()


# ------------------------------------------------------------------ S02 · ego balloon
def egoBalloon(x, y, r, txt, key='eg', col='#FFC93D', sq=0.0, anchor=None, a=1.0):
    """balloon centred (x, y), radius r; string to anchor"""
    if r < 2:
        return
    boilSeed(key)
    if anchor:
        ax, ay = anchor
        inkLine([[x, y + r * 1.08], [lerp(x, ax, .5) + r * .2, lerp(y + r, ay, .5)], [ax, ay]], .8, INK, 'inkfine', .5)
    paint([[x - r * .14, y + r * .96], [x + r * .14, y + r * .96], [x, y + r * 1.12]], wash=mixCol(col, INK, .2), ink=INK, sw=.7)
    paint(ellPts(x, y, r * (1 + sq), r * 1.05 * (1 - sq * .6), 34), wash=col, fill=mixCol(col, INK, .2), fillOp=60, ink=INK, sw=1.1)
    paint(ellPts(x - r * .4, y - r * .45, r * .2, r * .12, 12, 0, -.7), wash='#FFFFFF', washOp=190, ink=None)
    if txt:
        text(txt, x, y + r * .06, r * .62, '#FFFFFF', stroke=INK, strokeW=r * .08, shadow=False)


# ------------------------------------------------------------------ S03 · emo cloud, steam, little sun
def emoCloud(x, y, s, t, rain=1.0, a=1.0, key='ec', label='emo'):
    if a <= .01:
        return
    G.c.saveLayerAlpha(None, int(255 * a))
    if rain > .01:
        for i in range(9):
            ph = frac(t * 2.2 + hash1(i * 7.1))
            rx = x + (i - 4) * s * .28
            ry = y + s * .35 + ph * s * 1.5
            inkLine([[rx, ry], [rx - s * .04, ry + s * .2]], 1.1, '#7EA4D8', 'ink', 0)
    boilSeed(key)
    pts = []
    for i in range(44):
        q = i / 44 * TAU
        up = math.sin(q) < 0
        rr_ = 1 + .3 * abs(math.sin(q * 3)) ** .6 if up else 1
        pts.append([x + math.cos(q) * s * 1.05 * rr_, y + math.sin(q) * (.55 if up else .32) * s * rr_])
    paint(pts, wash='#9EA4BE', fill='#6E7698', fillOp=70, ink=INK, sw=1.0, curv=.4)
    if label:
        text(label, x, y + s * .02, s * .42, '#FFFFFF', stroke=INK, strokeW=s * .06, shadow=False)
    G.c.restore()


def steamPuff(x, y, s, age, dirx=1, key='stm'):
    """little puffs shooting out of the head (angry steam)"""
    if age < 0:
        return
    for i in range(3):
        f = clamp((age - i * .05) / .45)
        if f <= 0:
            continue
        px = x + dirx * (i - 1) * s * .6 + dirx * f * s * .4
        py = y - f * s * 1.6
        r = s * (.3 + .35 * f)
        paint(ellPts(px, py, r, r * .85, 14), wash='#FFFFFF', washOp=int(235 * (1 - f * .6)), ink=INK if f < .8 else None, sw=.6)


def littleSun(x, y, r, k, t, key='lsun'):
    if k <= .01:
        return
    p = backOut(k)
    glow(x, y, r * 3.2 * p, '#FFE38A', .8)
    for i in range(10):
        a = i / 10 * TAU + t * .8
        inkLine([[x + math.cos(a) * r * 1.25 * p, y + math.sin(a) * r * 1.25 * p], [x + math.cos(a) * r * 1.7 * p, y + math.sin(a) * r * 1.7 * p]],
                1.6, '#F2A65A', 'ink', 0)
    boilSeed(key)
    paint(ellPts(x, y, r * p, r * p, 26), wash='#FFD34D', fill='#F2A65A', fillOp=60, ink=INK, sw=1.0)
    G.c.drawCircle(x - r * .3 * p, y - r * .1 * p, r * .08, skia.Paint(AntiAlias=True, Color=skcol(INK)))
    G.c.drawCircle(x + r * .3 * p, y - r * .1 * p, r * .08, skia.Paint(AntiAlias=True, Color=skcol(INK)))
    inkLine([[x - r * .25 * p, y + r * .2 * p], [x, y + r * .38 * p], [x + r * .25 * p, y + r * .2 * p]], .9, INK, 'ink', .6)


# ------------------------------------------------------------------ S04 · grudge book, eraser
def grudgeBook(x, y, s, open_=1.0, erased=0.0, rot=0.0, key='gb', t=0.0):
    """(x, y) centre; s ~ half width of the open spread"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    if open_ < .5:
        paint(rrPts(-s * .55, -s * .7, s * 1.1, s * 1.4, s * .06), wash='#5B4A7A', fill='#3A2F55', fillOp=60, ink=INK, sw=1.0)
        paint(rectPts(-s * .38, -s * .38, s * .76, s * .36), wash='#FFFDF6', ink=INK, sw=.6)
        text('记仇本', 0, -s * .2, s * .2, '#B8324F', face=WENKAI, shadow=False)
    else:
        paint(rrPts(-s * 1.05, -s * .72, s * 2.1, s * 1.44, s * .06), wash='#5B4A7A', ink=INK, sw=1.0)
        for sd in (-1, 1):
            paint(rectPts(-s * 1.0 if sd < 0 else 0, -s * .66, s, s * 1.32), wash='#FFFDF6', ink=INK, sw=.6, lite=True)
        text('记仇本', -s * .5, -s * .5, s * .17, '#B8324F', face=WENKAI, shadow=False)
        lines = ['他又忘了回消息', '他吃了我的布丁', '他说我胖了', '他打游戏不理我', '他踩到我的小花']
        for i, ln in enumerate(lines):
            yy = -s * .3 + i * s * .2
            if yy > s * .55:
                break
            sd = -1 if i < 3 else 1
            yy = -s * .3 + (i if i < 3 else i - 3) * s * .2 + (0 if i < 3 else -s * .15)
            xx = -s * .5 if sd < 0 else s * .5
            a = 1 - erased
            if a > .02:
                text(ln, xx, yy, s * .095, '#5A4A6A', face=WENKAI, shadow=False, a=a)
                inkLine([[xx - s * .38, yy + s * .07], [xx + s * .38, yy + s * .07]], .5, '#E8476E', 'inkfine', 0) if i % 2 == 0 and a > .3 else None
        if erased > .95:
            doodleHeart(s * .5, s * .15, s * .16, HOT, 1.0, key=key + 'dh')
        inkLine([[0, -s * .66], [0, s * .66]], .7, INK, 'inkfine', 0)
    pop()


def eraser(x, y, s, rot=0.0, key='er'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rrPts(-s, -s * .45, s * 2, s * .9, s * .15), wash='#FFFFFF', ink=INK, sw=.8)
    paint(rrPts(-s, -s * .45, s * .9, s * .9, s * .15), wash='#7FC6E8', ink=INK, sw=.8)
    pop()


def crumbs(x, y, t, age, n=8, key='cr'):
    if age < 0 or age > .8:
        return
    for i in range(n):
        a = -math.pi / 2 + (hash1(i * 3.3) - .5) * 2.4
        d = 30 + 140 * easeOut(clamp(age / .5))
        px = x + math.cos(a) * d
        py = y + math.sin(a) * d + 300 * age * age
        paint(ellPts(px, py, 6, 4, 8), wash='#D9D3DC', washOp=int(255 * (1 - age / .8)), ink=None)


# ------------------------------------------------------------------ S07 · kitchen
def kitchenBack(t, key='kb'):
    gradRect(-400, -400, W + 800, 1240, ['#FFF4E2', '#F6E2C8'])
    for i in range(-6, 40):              # tiles (upper wall)
        for j in range(0, 7):
            x0, y0 = i * 90 + (45 if j % 2 else 0) - 300, 380 + j * 64
            G.c.drawRect(skia.Rect.MakeXYWH(x0, y0, 88, 62), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2, Color=skcol('#E2CDB0', .8)))
    flatRect(-400, 840, W + 800, 500, '#C8905E')
    inkLine([[-400, 840], [W + 400, 840]], 1.0, INK, 'ink', 0)
    # a small pot and a kettle on a low wall shelf at the far right
    boilSeed(key + 'pot')
    paint(rectPts(1690, 330, 250, 18), wash='#B98552', ink=INK, sw=.8)
    paint(ellPts(1750, 292, 52, 40, 20), wash='#E8476E', fill='#B8324F', fillOp=60, ink=INK, sw=.8)
    paint(rrPts(1820, 262, 70, 68, 12), wash='#F2C53D', ink=INK, sw=.7)
    sets2.fairyLights(t, -60, W + 60, 60, sag=40, n=20, key=key + 'fl')
    hb.calendar11(830, 130, key=key + 'cal')


def shelfBoard(x0, x1, y, key='sh'):
    boilSeed(key)
    paint(rectPts(x0, y, x1 - x0, 22), wash='#B98552', fill='#8E5E3A', fillOp=60, ink=INK, sw=.9)
    for x in (x0 + 40, x1 - 40):
        paint([[x - 12, y + 22], [x + 12, y + 22], [x - 12, y + 80]], wash='#8E5E3A', ink=INK, sw=.7)


def pantry(kind, x, y, s, k=1.0, key='pt'):
    """柴 / 米 / 油 / 盐 jars standing on a shelf; (x, y) = bottom centre"""
    if k <= .01:
        return
    p = backOut(k)
    push()
    translate(x, y)
    scale(p)
    boilSeed(key + kind)
    if kind == '柴':
        for i in range(5):
            paint(rrPts(-s * .9 + i * s * .36, -s * 1.5, s * .34, s * 1.5, s * .1), wash=['#B98552', '#A8714A', '#C99A62'][i % 3], ink=INK, sw=.7)
        paint(rectPts(-s * .95, -s * .95, s * 1.9, s * .22), wash='#E8476E', ink=INK, sw=.6)
        lab, ly = '柴', -s * 1.9
    elif kind == '米':
        paint([[-s * .8, 0], [s * .8, 0], [s * .7, -s * 1.5], [s * .3, -s * 1.8], [-s * .3, -s * 1.8], [-s * .7, -s * 1.5]], wash='#F3EBDC', fill='#D9CBB6', fillOp=70, ink=INK, sw=.8)
        inkLine([[-s * .35, -s * 1.62], [s * .35, -s * 1.62]], 1.2, '#E8476E', 'ink', 0)
        lab, ly = '米', -s * .8
    elif kind == '油':
        paint(rrPts(-s * .45, -s * 1.7, s * .9, s * 1.7, s * .2), wash='#F7D36E', fill='#E0A93A', fillOp=70, ink=INK, sw=.8)
        paint(rectPts(-s * .18, -s * 2.05, s * .36, s * .4), wash='#E8476E', ink=INK, sw=.6)
        lab, ly = '油', -s * .8
    else:
        paint(rrPts(-s * .6, -s * 1.3, s * 1.2, s * 1.3, s * .25), wash='#DDEFFB', fill='#A9CBE6', fillOp=60, ink=INK, sw=.8)
        paint(rrPts(-s * .65, -s * 1.5, s * 1.3, s * .3, s * .1), wash='#7FC6E8', ink=INK, sw=.6)
        lab, ly = '盐', -s * .62
    if kind != '柴':
        paint(ellPts(0, ly, s * .42, s * .36, 16), wash='#FFFDF6', ink=INK, sw=.5)
        text(lab, 0, ly, s * .5, INK, face=WENKAI, shadow=False)
    else:
        bubble(0, ly, lab, s * .5, None, 1.0, key=key + 'lb')
    pop()


def houseIcon(x, y, s, k=1.0, key='hs'):
    if k <= .01:
        return
    p = backOut(k)
    push()
    translate(x, y)
    scale(p)
    boilSeed(key)
    paint(rectPts(-s, -s * .2, s * 2, s * 1.2), wash='#FFF3E2', ink=INK, sw=.9)
    paint([[-s * 1.3, -s * .15], [0, -s * 1.2], [s * 1.3, -s * .15]], wash='#E8476E', fill='#B8324F', fillOp=60, ink=INK, sw=.9)
    paint(rectPts(-s * .25, s * .35, s * .5, s * .65), wash='#B98552', ink=INK, sw=.7)
    heart(0, -s * .5, s * .26, '#FFFFFF', key=key + 'h', sw=.6)
    plantPot(s * .7, s * 1.0, s * .2, key=key + 'pp')
    pop()


# ------------------------------------------------------------------ S08 · cork board
def corkBoard(x, y, w, h, key='cb'):
    boilSeed(key)
    paint(rectPts(x - 16, y - 16, w + 32, h + 32), wash='#8E5E3A', ink=INK, sw=1.1)
    paint(rectPts(x, y, w, h), wash='#D3A46E', fill='#B5824C', fillOp=70, tex=.8, ink=INK, sw=.8)
    for i in range(70):
        G.c.drawCircle(x + hash1(i * 1.3) * w, y + hash1(i * 2.7) * h, 2.2, skia.Paint(AntiAlias=True, Color=skcol('#9A6A3A', .5)))


def pin(x, y, col=HOT):
    G.c.drawCircle(x + 2, y + 3, 9, skia.Paint(AntiAlias=True, Color=skcol(INK, .3)))
    G.c.drawCircle(x, y, 9, skia.Paint(AntiAlias=True, Color=skcol(col)))
    G.c.drawCircle(x - 3, y - 3, 3, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .8)))


def stickyNote(x, y, w, txt, rot, k, col='#FBE7A1', key='sn', size=None, icon=None):
    if k <= .01:
        return
    p = backOut(k)
    push()
    translate(x, y)
    rotate(rot + (1 - clamp(k)) * .3)
    scale(p)
    boilSeed(key)
    paint(rectPts(-w / 2 + 8, -w / 2 + 10, w, w), wash=INK, washOp=40, ink=None)
    paint(rectPts(-w / 2, -w / 2, w, w), wash=col, ink=INK, sw=.8)
    text(txt, 0, -w * .08, size or w * .26, '#5A4A6A', face=WENKAI, shadow=False)
    if icon:
        icon(0, w * .26, w * .16)
    pop()
    pin(x + math.sin(rot) * w * .45, y - w * .42, HOT)


def planeIcon(x, y, s, rot=-.2, col='#5B7FC4', key='pli'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint([[-s, 0], [s * 1.1, -s * .1], [s * 1.25, 0], [s * 1.1, s * .1]], wash='#FFFFFF', ink=INK, sw=.7)
    paint([[-s * .1, -s * .05], [s * .25, -s * .05], [-s * .3, -s * .8]], wash=col, ink=INK, sw=.6)
    paint([[-s * .1, s * .05], [s * .25, s * .05], [-s * .3, s * .8]], wash=col, ink=INK, sw=.6)
    paint([[-s * .9, 0], [-s * .7, 0], [-s * 1.05, -s * .4]], wash=col, ink=INK, sw=.5)
    pop()


def movieTicket(x, y, w, rot, k, key='mt', col='#F7B2C6'):
    if k <= .01:
        return
    p = backOut(k)
    push()
    translate(x, y)
    rotate(rot)
    scale(p)
    boilSeed(key)
    h = w * .45
    paint(rectPts(-w / 2, -h / 2, w, h), wash=col, ink=INK, sw=.8)
    for i in range(6):
        G.c.drawCircle(w * .22, -h / 2 + 8 + i * (h - 16) / 5, 3, skia.Paint(AntiAlias=True, Color=skcol('#FFFDF6')))
    text('电影票', -w * .1, -h * .12, w * .14, INK, face=WENKAI, shadow=False)
    text('2人', -w * .1, h * .2, w * .11, '#B8324F', face=WENKAI, shadow=False)
    heart(w * .36, 0, w * .07, HOT, key=key + 'h', sw=.5)
    pop()
    pin(x, y - h * .38, '#5B7FC4')


def redString(pts, k=1.0):
    if k <= .01:
        return
    n = len(pts)
    m = max(2, int(2 + (n - 2) * k))
    inkLine(pts[:m], .8, '#D8394E', 'inkfine', .2)


# ------------------------------------------------------------------ S09 · cardboard rocket
def rocketBox(x, y, s, t, flame=0.0, key='rk', label='99号', front=True, back=True):
    """open-top cardboard rocket; (x, y) = bottom centre of the hull; ~4s tall body (+nose). front/back split for seated riders."""
    boilSeed(key)
    if back:
        # a cardboard flag on a stick behind the riders (the open-top box rocket has no nose cone)
        inkLine([[x + 1.6 * s, y - 2.9 * s], [x + 1.6 * s, y - 4.7 * s]], 1.6, '#8A5A3C', 'ink', 0)
        fl_ = .08 * math.sin(t * 9)
        paint([[x + 1.6 * s, y - 4.7 * s], [x + 2.5 * s, y - (4.45 + fl_) * s], [x + 1.6 * s, y - 4.15 * s]], wash='#E8476E', ink=INK, sw=.7)
    if front:
        if flame > .01:
            fl = flame * (1 + .15 * math.sin(t * 40))
            glow(x, y + .7 * s * fl, 2.0 * s * fl, '#FFB347', .9)
            paint([[x - 1.1 * s, y], [x + 1.1 * s, y], [x + .5 * s, y + .9 * s * fl], [x, y + 1.5 * s * fl], [x - .5 * s, y + .9 * s * fl]],
                  wash='#FFB347', fill='#E8476E', fillOp=60, ink=INK, sw=.8)
            paint([[x - .5 * s, y], [x + .5 * s, y], [x, y + .85 * s * fl]], wash='#FFF3A8', ink=None)
        for sd in (-1, 1):
            paint([[x + sd * 1.8 * s, y - 1.6 * s], [x + sd * 2.9 * s, y - .2 * s], [x + sd * 2.9 * s, y + .5 * s], [x + sd * 1.8 * s, y]],
                  wash='#5B7FC4', fill='#3C5A9A', fillOp=60, ink=INK, sw=.9)
        paint(rectPts(x - 2.0 * s, y - 2.85 * s, 4 * s, 2.85 * s), wash='#D9AE72', fill='#B5824C', fillOp=70, ink=INK, sw=1.1)
        inkLine([[x - 2.0 * s, y - 1.4 * s], [x + 2.0 * s, y - 1.4 * s]], .6, '#8E6A3E', 'inkfine', 0)
        paint(ellPts(x, y - 1.55 * s, .95 * s, .62 * s, 20), wash='#FFFDF6', ink=INK, sw=.7)
        text(label, x, y - 1.55 * s, .5 * s, RED, face=WENKAI, shadow=False)
        paint(rectPts(x - 2.05 * s, y - 2.95 * s, 4.1 * s, .3 * s), wash='#C9A06A', ink=INK, sw=.8)


def earthBall(x, y, r, key='earth'):
    boilSeed(key)
    glow(x, y, r * 1.6, '#8FD3FF', .5)
    paint(ellPts(x, y, r, r, 40), wash='#5BA8E0', fill='#3C7AB8', fillOp=60, ink=INK, sw=1.0)
    for (dx, dy, rx, ry) in [(-.35, -.3, .32, .2), (.25, .15, .4, .25), (-.1, .45, .25, .14), (.45, -.45, .18, .12)]:
        paint(ellPts(x + dx * r, y + dy * r, rx * r, ry * r, 16), wash='#7CC36B', ink=INK, sw=.5)


def countdown(txt, x, y, size, age):
    if age < -.04 or age > .5:
        return
    stamp(txt, x, y, size, '#FFE36E', age, rot=-.08, life=.5)


# ------------------------------------------------------------------ S10 · scribble cloud
def scribble(x, y, s, k, t, key='scr', col=INK):
    if k <= .01:
        return
    p = backOut(k)
    pts = []
    n = 40
    for i in range(n + 1):
        f = i / n
        a = f * TAU * 4.3 + t * 3
        r = s * p * (.55 + .45 * math.sin(f * 17 + t * 2))
        pts.append([x + math.cos(a) * r * 1.3, y + math.sin(a) * r * .6])
    boilSeed(key)
    inkLine(pts, 1.1, col, 'ink', .6)


# ------------------------------------------------------------------ S13 · wish strip, shooting star
def wishStrip(x, y, s, txt, rot=0.0, key='ws', col='#F7C6D2'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-s * .32, -s * 1.5, s * .64, s * 3), wash=col, ink=INK, sw=.8)
    G.c.drawCircle(0, -s * 1.3, s * .07, skia.Paint(AntiAlias=True, Color=skcol(INK)))
    inkLine([[0, -s * 1.37], [s * .15, -s * 1.75], [-s * .1, -s * 2.05]], .6, '#D8394E', 'inkfine', .4)
    for i, c in enumerate(txt):
        text(c, 0, -s * .95 + i * s * .5, s * .38, '#5A4A6A', face=WENKAI, shadow=False)
    pop()


def shootingStar(x0, y0, x1, y1, k, key='ss'):
    if k <= 0 or k >= 1.3:
        return
    kk = clamp(k)
    hx, hy = lerp(x0, x1, easeOut(kk)), lerp(y0, y1, easeOut(kk))
    a = 1 - seg(k, 1.0, 1.3)
    tl = .35
    tx, ty = lerp(x0, x1, easeOut(max(0, kk - tl))), lerp(y0, y1, easeOut(max(0, kk - tl)))
    p = skia.Paint(AntiAlias=True, StrokeWidth=18, StrokeCap=skia.Paint.kRound_Cap,
                   Shader=skia.GradientShader.MakeLinear([skia.Point(tx, ty), skia.Point(hx, hy)], [skcol('#FFF6C8', 0), skcol('#FFF6C8', .9 * a)]))
    G.c.drawLine(tx, ty, hx, hy, p)
    glow(hx, hy, 120, '#FFF6C8', a)
    paint(starPts(hx, hy, 40, .42, 5), wash='#FFF3A8', washOp=int(255 * a), ink=INK if a > .5 else None, sw=.6)


# ------------------------------------------------------------------ S14 · chat bubbles
def lockIcon(x, y, s, shut=1.0, key='lki'):
    boilSeed(key)
    sh = (1 - shut) * s * .35
    inkLine([[x - s * .35, y - s * .1], [x - s * .35, y - s * .55 - sh], [x, y - s * .85 - sh], [x + s * .35, y - s * .55 - sh], [x + s * .35, y - s * .1 - sh * 1.6]],
            1.4, '#7A6A80', 'ink', .7)
    paint(rrPts(x - s * .55, y - s * .2, s * 1.1, s * .85, s * .12), wash='#F2C53D', fill='#C9A24E', fillOp=60, ink=INK, sw=.8)
    G.c.drawCircle(x, y + s * .15, s * .1, skia.Paint(AntiAlias=True, Color=skcol(INK)))


# ------------------------------------------------------------------ S15 · plan board + props in hand
def dumbbell(x, y, s, rot=0.0, key='db'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-s, -s * .1, s * 2, s * .2), wash='#9AA3B8', ink=INK, sw=.6)
    for sd in (-1, 1):
        paint(rrPts(sd * s - s * .25, -s * .45, s * .5, s * .9, s * .12), wash='#3D3A52', ink=INK, sw=.7)
    pop()


def bookOpen(x, y, s, rot=0.0, key='bko', col='#5B7FC4'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rrPts(-s * 1.05, -s * .7, s * 2.1, s * 1.4, s * .08), wash=col, ink=INK, sw=.8)
    for sd in (-1, 1):
        paint([[0, -s * .62], [sd * s * .98, -s * .7], [sd * s * .98, s * .62], [0, s * .66]], wash='#FFFDF6', ink=INK, sw=.6, lite=True)
        for i in range(4):
            inkLine([[sd * s * .2, -s * .35 + i * s * .25], [sd * s * .8, -s * .37 + i * s * .25]], .4, '#9A8AA0', 'inkfine', 0)
    pop()


def spatula(x, y, s, rot=0.0, key='spt'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-s * .07, -s * 1.2, s * .14, s * 1.3), wash='#8A5A3C', ink=INK, sw=.6)
    paint(rrPts(-s * .32, -s * 1.85, s * .64, s * .7, s * .1), wash='#C9C1D6', ink=INK, sw=.7)
    pop()


def soupBowl(x, y, s, t, key='sb', steam=1.0):
    boilSeed(key)
    if steam > .01:
        for i in range(3):
            ph = frac(t * .9 + i / 3)
            sx = x + (i - 1) * s * .45
            inkLine([[sx, y - s * .6 - ph * s * 1.2], [sx + s * .15 * math.sin(t * 4 + i), y - s * .9 - ph * s * 1.2],
                     [sx, y - s * 1.2 - ph * s * 1.2]], .9, '#FFFFFF', 'ink', .7)
    paint([[x - s, y - s * .55], [x + s, y - s * .55], [x + s * .7, y + s * .2], [x - s * .7, y + s * .2]], wash='#FFFDF6', fill='#D9CBB6', fillOp=60, ink=INK, sw=.9)
    paint(ellPts(x, y - s * .55, s, s * .22, 20), wash='#F2A65A', ink=INK, sw=.7)
    paint(rectPts(x - s * .65, y - s * .35, s * 1.3, s * .12), wash='#E8476E', ink=None)


def chalkBoard(x, y, w, h, key='cbd'):
    boilSeed(key)
    paint(rectPts(x - 14, y - 14, w + 28, h + 28), wash='#B98552', ink=INK, sw=1.0)
    paint(rectPts(x, y, w, h), wash='#2F5A4A', fill='#24463A', fillOp=60, ink=INK, sw=.7)


# ------------------------------------------------------------------ S16 · stone blocks
def stoneBlock(x, y, w, h, txt, rot=0.0, key='stb', col='#8E93A8'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rrPts(-w / 2, -h, w, h, h * .12, 2), wash=col, fill=mixCol(col, INK, .3), fillOp=70, ink=INK, sw=1.1)
    for i in range(3):
        inkLine([[-w * .3 + i * w * .22, -h * .8], [-w * .26 + i * w * .22, -h * .62]], .6, mixCol(col, INK, .5), 'inkfine', .3)
    text(txt, 0, -h * .45, h * .4, '#FFFFFF', stroke=INK, strokeW=h * .05, shadow=False)
    pop()


# ------------------------------------------------------------------ S17 · snow night
def snowNight(t, warm=0.0, key='sn'):
    top = mixCol('#1E2654', '#3A2A4A', warm)
    gradRect(-400, -400, W + 800, 1300, [top, mixCol('#3A4880', '#7A5060', warm), mixCol('#6A7AB0', '#C8907A', warm)])
    hl.stars(t, 21, 50, -100, -100, W + 100, 520, a=.7)
    tp.skyline(760, mixCol('#2A3366', '#4A3050', warm), '#FFD98A', .5, key=key + 'sky')
    flatRect(-400, 840, W + 800, 500, mixCol('#E6ECF8', '#F6E6DA', warm))
    boilSeed(key + 'gnd')
    paint([[-400, 850], [W + 400, 830], [W + 400, 1300], [-400, 1300]], wash=mixCol('#E8EEFA', '#FBEFE4', warm), ink=None)
    inkLine([[-400, 848], [600, 838], [1300, 846], [W + 400, 832]], .9, INK, 'ink', .4)


def cocoaCup(x, y, s, t, key='cc', col='#F7C6D2'):
    hl.mug(x, y, s, key=key, col=col, steam=1.0, t=t)


# ------------------------------------------------------------------ S18 · honey, lemon, tea
def honeyJar(x, y, s, key='hj', drip=0.0):
    boilSeed(key)
    paint(rrPts(x - s * .9, y - s * 1.9, s * 1.8, s * 1.9, s * .45), wash='#F7C24A', fill='#E0952A', fillOp=70, ink=INK, sw=1.0)
    paint(rrPts(x - s * .75, y - s * 2.25, s * 1.5, s * .42, s * .12), wash='#E8476E', ink=INK, sw=.8)
    paint([[x - s * .9, y - s * 1.55], [x + s * .9, y - s * 1.55], [x + s * .6, y - s * 1.3], [x + s * .2, y - s * 1.45], [x - s * .3, y - s * 1.2], [x - s * .9, y - s * 1.45]],
          wash='#FFE38A', ink=None)
    paint(ellPts(x, y - s * .85, s * .5, s * .36, 16), wash='#FFFDF6', ink=INK, sw=.5)
    text('蜂蜜', x, y - s * .85, s * .3, '#B8724A', face=WENKAI, shadow=False)
    # a little bee
    bx, by = x + s * 1.2, y - s * 2.4
    paint(ellPts(bx, by, s * .26, s * .2, 12), wash='#FFD34D', ink=INK, sw=.5)
    for i in (-1, 1):
        paint(ellPts(bx + i * s * .1, by - s * .22, s * .14, s * .1, 10), wash='#FFFFFF', washOp=200, ink=INK, sw=.4)


def lemonProp(x, y, s, key='lm', rot=0.0):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(ellPts(0, 0, s * 1.25, s * .9, 28), wash='#FFE24A', fill='#E8C42A', fillOp=70, ink=INK, sw=1.0)
    paint([[s * 1.15, -s * .12], [s * 1.5, 0], [s * 1.15, s * .12]], wash='#E8C42A', ink=INK, sw=.7)
    paint(ellPts(-s * .3, -s * .9, s * .45, s * .2, 12, 0, -.4), wash='#7CC36B', ink=INK, sw=.6)
    paint(ellPts(-s * .45, -s * .35, s * .25, s * .12, 10, 0, -.4), wash='#FFFFFF', washOp=150, ink=None)
    pop()


def teaGlass(x, y, s, t, key='tg'):
    """a mug of honey lemon tea (opaque ceramic mug, not glass)"""
    boilSeed(key)
    for i in range(3):
        ph = frac(t * .9 + i / 3)
        sx = x + (i - 1) * s * .35
        inkLine([[sx, y - s * 2.1 - ph * s], [sx + s * .12 * math.sin(t * 4 + i), y - s * 2.4 - ph * s], [sx, y - s * 2.7 - ph * s]], .9, '#FFFFFF', 'ink', .7)
    paint(rrPts(x - s, y - s * 2, s * 2, s * 2, s * .3), wash='#FFFDF6', fill='#E9DCCB', fillOp=60, ink=INK, sw=1.0)
    inkLine([[x + s, y - s * 1.6], [x + s * 1.5, y - s * 1.4], [x + s * 1.45, y - s * .7], [x + s, y - s * .5]], 1.6, INK, 'ink', .5)
    paint(ellPts(x, y - s * 1.95, s * .92, s * .2, 18), wash='#F7C24A', ink=INK, sw=.5)
    paint(ellPts(x + s * .35, y - s * 2.05, s * .32, s * .26, 14), wash='#FFE24A', ink=INK, sw=.5)
    text('蜂蜜', x, y - s * 1.12, s * .46, '#B8724A', face=WENKAI, shadow=False)
    text('柠檬', x, y - s * .58, s * .46, '#7AA02A', face=WENKAI, shadow=False)


# ------------------------------------------------------------------ S20 · big flower
def bigBloom(x, y, r, k, key='bbl', col='#F59AB0', t=0.0):
    if k <= .01:
        return
    p = backOut(k)
    boilSeed(key)
    for i in range(7):
        a = i / 7 * TAU + .3 + .05 * math.sin(t * 2)
        paint(ellPts(x + math.cos(a) * r * .62 * p, y + math.sin(a) * r * .62 * p, r * .46 * p, r * .3 * p, 16, 0, a),
              wash=col, fill=mixCol(col, INK, .2), fillOp=60, ink=INK, sw=.8)
    paint(ellPts(x, y, r * .32 * p, r * .32 * p, 18), wash='#FFD34D', ink=INK, sw=.7)


def petal(x, y, s, rot, col='#F59AB0', a=1.0, key='pt'):
    boilSeed(key)
    paint(ellPts(x, y, s, s * .55, 12, 0, rot), wash=col, washOp=int(255 * a), ink=INK if a > .5 else None, sw=.5)


# ------------------------------------------------------------------ S22 · race track
def track(t, key='trk', finishX=1560):
    gradRect(-400, -400, W + 800, 900, ['#9ED3F2', '#D8EEF8', '#F2F8EC'])
    puff(300, 140, 30, key=key + 'c1')
    puff(1420, 120, 24, key=key + 'c2')
    # stands with a grey crowd silhouette
    boilSeed(key + 'st')
    paint(rectPts(-400, 420, W + 800, 220), wash='#B8B6BE', fill='#9A98A4', fillOp=60, ink=INK, sw=.8)
    for i in range(30):
        G.c.drawCircle(-100 + i * 75, 470 + 30 * (i % 2), 26, skia.Paint(AntiAlias=True, Color=skcol('#A9A7B0')))
    flatRect(-400, 640, W + 800, 700, '#D9604A')
    for j in range(5):
        y = 690 + j * 60
        inkLine([[-400, y], [W + 400, y]], .7, '#FFFFFF', 'inkfine', 0)
    flatRect(-400, 640, W + 800, 18, '#7CC36B')
    # finish line: checkered post + tape
    for i in range(10):
        for j in range(2):
            flatRect(finishX - 20 + j * 20, 650 + i * 30, 20, 30, INK if (i + j) % 2 == 0 else '#FFFFFF')


def dustCloud(x, y, s, age, key='dust'):
    if age < 0 or age > 1.6:
        return
    a = 1 - seg(age, .9, 1.6)
    for i in range(7):
        f = clamp(age / .4)
        px = x - i * s * .55 * (.6 + .4 * f)
        py = y - (hash1(i * 3.3) * .8) * s
        r = s * (.35 + .35 * f) * (1 + .2 * hash1(i))
        paint(ellPts(px, py, r, r * .8, 16), wash='#E6D2B0', washOp=int(230 * a), fill='#C9A97A', fillOp=int(60 * a), ink=INK if a > .6 else None, sw=.6)


# ------------------------------------------------------------------ S24 · jasmine
def jasmine(x, y, r, k=1.0, key='js', glowK=0.0):
    if k <= .01:
        return
    p = backOut(k)
    if glowK > .01:
        glow(x, y, r * 3, '#FFFBE0', glowK)
    boilSeed(key)
    for i in range(5):
        a = i / 5 * TAU - math.pi / 2
        paint(ellPts(x + math.cos(a) * r * .55 * p, y + math.sin(a) * r * .55 * p, r * .5 * p, r * .3 * p, 12, 0, a),
              wash='#FFFFFF', fill='#E8F2E0', fillOp=60, ink=INK, sw=.5)
    paint(ellPts(x, y, r * .2 * p, r * .2 * p, 10), wash='#F7E38A', ink=None)


def jasmineWall(t, key='jw', open_=None):
    gradRect(-400, -400, W + 800, 1300, ['#CDEFE0', '#E8F7EE', '#FFFBEF'])
    flatRect(-400, 840, W + 800, 500, '#A9DA8A')
    inkLine([[-400, 840], [W + 400, 840]], .9, INK, 'ink', 0)
    # a long hedge with jasmine flowers
    boilSeed(key + 'hd')
    pts = [[-400, 840]]
    for i in range(31):
        x = -400 + i * (W + 800) / 30
        pts.append([x, 420 + 40 * math.sin(i * 1.7) + 25 * hash1(i)])
    pts.append([W + 400, 840])
    paint(pts, wash='#4E9A5A', fill='#2F6440', fillOp=60, ink=INK, sw=1.0)
    for i in range(60):
        x = -300 + hash1(i * 2.3) * (W + 600)
        y = 470 + hash1(i * 4.1) * 330
        paint(ellPts(x, y, 40, 22, 10, 0, hash1(i) * 3), wash='#6FB36A', ink=None)
    for i in range(30):
        x = -200 + hash1(i * 5.7) * (W + 400)
        y = 480 + hash1(i * 1.9) * 300
        jasmine(x, y, 18, 1.0, key=f'{key}j{i}')


def jasmineBunch(x, y, s, key='jb', rot=0.0):
    """a small bouquet: (x, y) = where the stems are held"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    for i in range(5):
        a = -.5 + i * .25
        inkLine([[0, 0], [math.sin(a) * s * 1.2, -s * 1.5 - math.cos(a) * s * .3]], 1.4, '#4E9A5A', 'ink', .3)
    for i in range(6):
        a = -.9 + i * .36
        paint(ellPts(math.sin(a) * s * 1.2, -s * 1.6 - math.cos(a) * s * .5, s * .3, s * .16, 10, 0, a), wash='#6FB36A', ink=INK, sw=.5)
    for i, (dx, dy) in enumerate([(0, -2.2), (-.75, -1.95), (.75, -1.95), (-.4, -2.6), (.4, -2.6), (-1.1, -2.4), (1.1, -2.4), (0, -1.75)]):
        jasmine(dx * s, dy * s, s * .42, 1.0, key=f'{key}{i}')
    paint([[-s * .45, -s * .6], [s * .45, -s * .6], [s * .2, s * .3], [-s * .2, s * .3]], wash='#F7C6D2', ink=INK, sw=.7)
    pop()


# ------------------------------------------------------------------ S25 · love card
def loveCard(x, y, w, prog, rot=0.0, key='lc', k=1.0):
    """an opened card; prog 0..1 = handwriting progress of 「每一天」 / 「示例歌词」"""
    if k <= .01:
        return
    p = backOut(k)
    h = w * .72
    push()
    translate(x, y)
    rotate(rot)
    scale(p)
    boilSeed(key)
    paint(rectPts(-w / 2 + 8, -h / 2 + 10, w, h), wash=INK, washOp=40, ink=None)
    paint(rrPts(-w / 2, -h / 2, w, h, 10), wash='#FFFDF6', fill='#F9E3EA', fillOp=50, ink=INK, sw=.9)
    inkLine([[0, -h / 2], [0, h / 2]], .5, '#E2C6CC', 'inkfine', 0)
    heart(-w * .25, 0, w * .12, HOT, key=key + 'h', sw=.6)
    l1, l2 = '每一天', '示例歌词'
    p1 = clamp(prog * 2)
    p2 = clamp(prog * 2 - 1)
    hb.handText(l1, w * .25, -h * .17, w * .13, p1, '#5A4A6A', WENKAI, 'center', pen=False)
    hb.handText(l2, w * .25, h * .17, w * .1, p2, '#B8324F', WENKAI, 'center', pen=False)
    pop()
