# lsm3.py: 《罗生门》 detail pass (user 2026-11-04: 「后面就开始变得敷衍了」「城市 火车 房间都可以多加点细节 太单调 可以多加点烟火气息」).
# Overrides doorScene / rainStreet / cityWide / trainOutside / stationNorth from lsm2 with denser, lived-in versions, and adds the
# green-train four-seat booth (trainBooth), tiny passers-by, food stalls with steam, lit windows with silhouettes, laundry, lanterns,
# AC units, bikes, cats, neon. Import AFTER lsm2 so these names win.
import math
from eng import *
import eng
from couple import jhim, jher, HIM, HER
from lsm import *
import lsm2 as _L2
from lsm2 import umbDown, umbLean, OLDHIM, OLDHER

WK = 'LXGWWenKai-Regular.ttf'


def P_(c, a=1.0, sw=None):
    p = skia.Paint(AntiAlias=True, Color=skcol(c, a))
    if sw:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(sw)
        p.setStrokeCap(skia.Paint.kRound_Cap)
    return p


# ================================================================ small life props
def steam(t, x, y, n=3, a=.45, w=1.0, h=150, seed=0):
    for i in range(n):
        ph = frac(t * .45 + i / n + hash1(seed + i) * .3)
        xx = x + math.sin(ph * 5 + i + seed) * 16 * w + (i - n / 2) * 10 * w
        yy = y - ph * h
        G.c.drawCircle(xx, yy, (8 + ph * 22) * w, P_('#FFFFFF', a * math.sin(ph * math.pi) * .8))


def smoke(t, x, y, a=.35, s=1.0, seed=0, col='#C9C9D4'):
    for i in range(5):
        ph = frac(t * .22 + i / 5 + hash1(seed) * .2)
        G.c.drawCircle(x + ph * 60 * s + math.sin(ph * 4 + i) * 10 * s, y - ph * 200 * s, (10 + ph * 30) * s, P_(col, a * (1 - ph)))


def tinyPerson(x, y, s, coat, t=0.0, walk=True, umb=None, hat=None, d=1, hair='#2E2A36', seed=0, bag=None):
    """a small passer-by (about 70*s px tall): (x, y) = feet"""
    ph = t * 2.2 + seed
    sw_ = math.sin(ph * math.pi) if walk else 0
    lg = P_(INK, 1, 3.0 * s)
    G.c.drawLine(x - 4 * s, y - 22 * s, x - 4 * s + 6 * s * sw_, y, lg)
    G.c.drawLine(x + 4 * s, y - 22 * s, x + 4 * s - 6 * s * sw_, y, lg)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x - 11 * s, y - 50 * s, 22 * s, 32 * s), 8 * s, 8 * s, P_(coat))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x - 11 * s, y - 50 * s, 22 * s, 32 * s), 8 * s, 8 * s, P_(INK, .8, 1.6 * s))
    G.c.drawCircle(x, y - 60 * s, 10 * s, P_('#F2C9A8'))
    G.c.drawArc(skia.Rect.MakeXYWH(x - 10.5 * s, y - 71 * s, 21 * s, 18 * s), 180, 180, True, P_(hair))
    G.c.drawCircle(x, y - 60 * s, 10 * s, P_(INK, .8, 1.4 * s))
    if hat:
        G.c.drawRoundRect(skia.Rect.MakeXYWH(x - 11 * s, y - 74 * s, 22 * s, 10 * s), 5 * s, 5 * s, P_(hat))
        G.c.drawCircle(x, y - 76 * s, 4 * s, P_(hat))
    if bag:
        G.c.drawRoundRect(skia.Rect.MakeXYWH(x + 9 * s * d, y - 40 * s, 12 * s, 14 * s), 3 * s, 3 * s, P_(bag))
    if umb:
        G.c.drawLine(x + 6 * s * d, y - 40 * s, x + 6 * s * d, y - 92 * s, P_(INK, 1, 2 * s))
        G.c.drawArc(skia.Rect.MakeXYWH(x + 6 * s * d - 34 * s, y - 112 * s, 68 * s, 44 * s), 180, 180, True, P_(umb))
        G.c.drawArc(skia.Rect.MakeXYWH(x + 6 * s * d - 34 * s, y - 112 * s, 68 * s, 44 * s), 180, 180, True, P_(INK, .8, 1.5 * s))


def crowd(t, x0, x1, y, n, s, north, seed=0, a=1.0, umbrellas=True):
    coats = ['#7A6A4E', '#4E6A7A', '#8A5A3C', '#5E7A5A', '#9A8A5A', '#4A4E66', '#B0604A']
    umbs = ['#5D8FC9', '#3F7F6A', '#E9A23B', '#7A7F8E', '#B0403E', '#2E2A38']
    for i in range(n):
        d = 1 if hash1(seed + i * 3) > .5 else -1
        sp = 26 + 24 * hash1(seed + i * 7)
        xx = x0 + ((hash1(seed + i * 11) * (x1 - x0) + d * t * sp) % (x1 - x0))
        G.c.saveLayerAlpha(None, int(255 * a))
        tinyPerson(xx, y + 6 * hash1(i + seed), s * (.9 + .2 * hash1(i * 5 + seed)), coats[i % len(coats)], t, True,
                   umb=(umbs[i % len(umbs)] if (umbrellas and not north) else None), hat=('#C94A4A' if north and i % 3 == 0 else ('#5E5A72' if north else None)),
                   d=d, seed=i * 1.7 + seed, bag=('#E9E2D2' if i % 4 == 1 else None))
        G.c.restore()


def acUnit(x, y, s=1.0):
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x, y, 70 * s, 46 * s), 4, 4, P_('#E6E2DA'))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x, y, 70 * s, 46 * s), 4, 4, P_(INK, .7, 1.5))
    G.c.drawCircle(x + 22 * s, y + 23 * s, 15 * s, P_('#9A968E', 1, 1.5))
    for k in range(3):
        G.c.drawLine(x + 44 * s, y + 10 * s + k * 12 * s, x + 64 * s, y + 10 * s + k * 12 * s, P_('#9A968E', 1, 1.5))


def laundry(x0, x1, y, t, seed=0, frozen=False):
    G.c.drawLine(x0, y, x1, y + 6, P_('#5E5A66', 1, 1.6))
    cols = ['#E9585E', '#5D8FC9', '#FFFDF6', '#E9A23B', '#7FB08A', '#C9A0D0', '#FFFDF6']
    n = int((x1 - x0) / 34)
    for i in range(n):
        if hash1(seed + i) < .3:
            continue
        xx = x0 + 12 + i * 34
        sway = 0 if frozen else math.sin(t * 2 + i) * 2
        c = cols[(i + seed) % len(cols)]
        if i % 3 == 0:
            G.c.drawRect(skia.Rect.MakeXYWH(xx - 12 + sway, y + 2, 24, 30), P_(c))           # shirt
            G.c.drawRect(skia.Rect.MakeXYWH(xx - 18 + sway, y + 2, 36, 9), P_(c))
        elif i % 3 == 1:
            G.c.drawRect(skia.Rect.MakeXYWH(xx - 9 + sway, y + 2, 18, 34), P_(c))            # towel / trousers
        else:
            G.c.drawRect(skia.Rect.MakeXYWH(xx - 5 + sway, y + 2, 10, 18), P_(c))            # sock
        if frozen:
            G.c.drawRect(skia.Rect.MakeXYWH(xx - 12, y + 1, 24, 4), P_('#FFFFFF', .9))


def lantern(x, y, s=1.0, t=0.0, lit=True):
    G.c.drawLine(x, y - 30 * s, x, y - 18 * s, P_(INK, 1, 1.5))
    if lit:
        glow(x, y, 46 * s, '#FF8A6A', .35)
    G.c.drawOval(skia.Rect.MakeXYWH(x - 16 * s, y - 18 * s, 32 * s, 36 * s), P_('#D9393E'))
    G.c.drawOval(skia.Rect.MakeXYWH(x - 16 * s, y - 18 * s, 32 * s, 36 * s), P_(INK, .8, 1.4))
    G.c.drawRect(skia.Rect.MakeXYWH(x - 8 * s, y - 21 * s, 16 * s, 5 * s), P_('#E9C84A'))
    G.c.drawRect(skia.Rect.MakeXYWH(x - 8 * s, y + 16 * s, 16 * s, 5 * s), P_('#E9C84A'))
    G.c.drawLine(x, y + 21 * s, x + math.sin(t * 2) * 2, y + 34 * s, P_('#E9C84A', 1, 2))


def bike(x, y, s=1.0, col='#3F7F6A', snowK=0.0):
    pa = P_(INK, 1, 3 * s)
    for wx in (x - 34 * s, x + 34 * s):
        G.c.drawCircle(wx, y - 22 * s, 22 * s, pa)
    G.c.drawLine(x - 34 * s, y - 22 * s, x, y - 22 * s, P_(col, 1, 5 * s))
    G.c.drawLine(x, y - 22 * s, x + 14 * s, y - 52 * s, P_(col, 1, 5 * s))
    G.c.drawLine(x - 34 * s, y - 22 * s, x - 10 * s, y - 50 * s, P_(col, 1, 5 * s))
    G.c.drawLine(x - 10 * s, y - 50 * s, x + 14 * s, y - 52 * s, P_(col, 1, 5 * s))
    G.c.drawLine(x + 14 * s, y - 52 * s, x + 34 * s, y - 22 * s, P_(col, 1, 5 * s))
    G.c.drawRect(skia.Rect.MakeXYWH(x - 22 * s, y - 56 * s, 22 * s, 6 * s), P_(INK))
    G.c.drawLine(x + 14 * s, y - 52 * s, x + 18 * s, y - 64 * s, P_(INK, 1, 3 * s))
    G.c.drawLine(x + 8 * s, y - 64 * s, x + 28 * s, y - 64 * s, P_(INK, 1, 3 * s))
    G.c.drawRect(skia.Rect.MakeXYWH(x + 22 * s, y - 62 * s, 22 * s, 16 * s), P_('#C9A27A'))            # basket
    if snowK > 0:
        G.c.drawRect(skia.Rect.MakeXYWH(x - 24 * s, y - 60 * s, 26 * s, 5 * s), P_('#FFFFFF', snowK))
        G.c.drawRect(skia.Rect.MakeXYWH(x + 20 * s, y - 66 * s, 26 * s, 5 * s), P_('#FFFFFF', snowK))


def scooter(x, y, s=1.0, col='#E9585E'):
    for wx in (x - 40 * s, x + 40 * s):
        G.c.drawCircle(wx, y - 16 * s, 16 * s, P_(INK))
        G.c.drawCircle(wx, y - 16 * s, 7 * s, P_('#9A968E'))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x - 50 * s, y - 46 * s, 70 * s, 26 * s), 12 * s, 12 * s, P_(col))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x - 46 * s, y - 60 * s, 46 * s, 14 * s), 7 * s, 7 * s, P_('#2E2A38'))
    G.c.drawLine(x + 30 * s, y - 30 * s, x + 40 * s, y - 84 * s, P_(col, 1, 7 * s))
    G.c.drawLine(x + 26 * s, y - 86 * s, x + 54 * s, y - 84 * s, P_(INK, 1, 4 * s))
    G.c.drawCircle(x + 44 * s, y - 72 * s, 6 * s, P_('#FFE7A8'))


def cat(x, y, s=1.0, col='#E9A23B', t=0.0, sit=True):
    G.c.drawOval(skia.Rect.MakeXYWH(x - 18 * s, y - 34 * s, 36 * s, 34 * s), P_(col))
    G.c.drawCircle(x, y - 42 * s, 13 * s, P_(col))
    for d in (-1, 1):
        G.c.drawPath(_tri(x + d * 9 * s, y - 52 * s, d), P_(col))
        G.c.drawCircle(x + d * 5 * s, y - 43 * s, 1.8 * s, P_(INK))
    tail = math.sin(t * 2.5) * 8 * s
    G.c.drawLine(x + 16 * s, y - 6 * s, x + 30 * s + tail, y - 26 * s, P_(col, 1, 6 * s))
    G.c.drawOval(skia.Rect.MakeXYWH(x - 18 * s, y - 34 * s, 36 * s, 34 * s), P_(INK, .7, 1.4))


def _tri(x, y, d):
    p = skia.Path()
    p.moveTo(x - 6, y + 4)
    p.lineTo(x + 2 * d, y - 8)
    p.lineTo(x + 7, y + 5)
    p.close()
    return p


def neon(x, y, txt, col, t, size=34, flick=0):
    on = 1.0 if not flick or frac(t * .7 + flick) > .06 else .3
    glow(x, y, size * 2.4, col, .35 * on)
    text(txt, x, y, size, '#FFFDF6' if on > .5 else '#B0A8B0', face=WK, stroke=col, strokeW=size * .22, shadow=False, a=.95)


def litWindow(x, y, w, h, kind, t, north=False, seed=0):
    """an apartment window with life inside: 'cook' (someone at the stove, steam), 'tv' (blue flicker, sofa heads), 'family'
    (two heads at a table), 'study' (desk lamp + head), 'plant', 'dark'"""
    if kind == 'dark':
        G.c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), P_('#2A2E48', .9))
    else:
        base = {'tv': '#9FC4F0', 'cook': '#FFD9A0', 'family': '#FFE3B0', 'study': '#FFF1C8', 'plant': '#FFE7A8'}[kind]
        if kind == 'tv':
            base = mixCol('#9FC4F0', '#C9E0FA', .5 + .5 * math.sin(t * 9 + seed))
        G.c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), P_(base, .95))
        hb = P_('#3A3346', .85)
        if kind == 'cook':
            G.c.drawCircle(x + w * .35, y + h * .42, h * .14, hb)
            G.c.drawRect(skia.Rect.MakeXYWH(x + w * .25, y + h * .55, w * .2, h * .45), hb)
            steam(t, x + w * .68, y + h * .6, 2, .5, w / 120, h * .5, seed)
        elif kind == 'tv':
            for k in range(2):
                G.c.drawCircle(x + w * (.35 + k * .25), y + h * .72, h * .13, hb)
        elif kind == 'family':
            for k in range(3):
                G.c.drawCircle(x + w * (.25 + k * .25), y + h * .5, h * .12, hb)
            G.c.drawRect(skia.Rect.MakeXYWH(x + w * .1, y + h * .68, w * .8, h * .08), P_('#8A5A3C', .8))
        elif kind == 'study':
            G.c.drawCircle(x + w * .45, y + h * .55, h * .13, hb)
            glow(x + w * .75, y + h * .5, h * .4, '#FFE7A8', .4)
        elif kind == 'plant':
            for k in range(3):
                G.c.drawOval(skia.Rect.MakeXYWH(x + w * (.2 + k * .2), y + h * .5, w * .16, h * .3), P_('#5E8A50', .9))
    G.c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), P_(INK, .7, 1.6))
    G.c.drawLine(x + w / 2, y, x + w / 2, y + h, P_(INK, .5, 1.4))
    if north:
        G.c.drawRect(skia.Rect.MakeXYWH(x - 3, y + h - 4, w + 6, 6), P_('#FFFFFF', .95))
        for k in range(3):
            G.c.drawCircle(x + 8 + k * 9, y + 8, 4, P_('#FFFFFF', .5))


def stall(x, y, kind, t, s=1.0, north=False, seed=0):
    """food stall with a vendor; (x, y) = ground under the cart. kinds: 红薯 (oil-drum stove), 栗子 (big wok), 包子 (steamers), 烧烤 (grill)"""
    vx = x - 60 * s
    tinyPerson(vx, y, 1.15 * s, '#5E7A5A' if kind != '烧烤' else '#8A5A3C', t, False, hat=('#C94A4A' if north else None), seed=seed)
    boilSeed(f'stall{kind}{seed}')
    if kind == '红薯':
        paint(rrPts(x - 34 * s, y - 92 * s, 68 * s, 92 * s, 8 * s), wash='#5A5E6E', ink=INK, sw=.6)
        glow(x, y - 80 * s, 60 * s, '#FF8A3C', .5)
        for k in range(4):
            G.c.drawOval(skia.Rect.MakeXYWH(x - 30 * s + k * 15 * s, y - 102 * s, 16 * s, 10 * s), P_('#B0604A'))
        smoke(t, x + 10 * s, y - 110 * s, .35, .8 * s, seed)
        sign = '烤红薯'
    elif kind == '栗子':
        paint(rrPts(x - 60 * s, y - 70 * s, 120 * s, 70 * s, 6 * s), wash='#B0403E', ink=INK, sw=.6)
        G.c.drawOval(skia.Rect.MakeXYWH(x - 50 * s, y - 92 * s, 100 * s, 30 * s), P_('#2E2A36'))
        for k in range(9):
            G.c.drawCircle(x - 34 * s + (k % 5) * 17 * s, y - 80 * s + (k // 5) * 7 * s, 5 * s, P_('#7A4A2A'))
        steam(t, x, y - 95 * s, 3, .5, .9 * s, 120 * s, seed)
        sign = '糖炒栗子'
    elif kind == '包子':
        for k in range(3):
            paint(ellPts(x, y - 30 * s - k * 26 * s, 50 * s, 14 * s, 18), wash='#D9B77A', ink=INK, sw=.5)
            G.c.drawRect(skia.Rect.MakeXYWH(x - 50 * s, y - 30 * s - k * 26 * s, 100 * s, 18 * s), P_('#C9A262'))
        steam(t, x, y - 110 * s, 4, .6, 1.1 * s, 160 * s, seed)
        sign = '热包子'
    else:
        paint(rectPts(x - 64 * s, y - 64 * s, 128 * s, 20 * s), wash='#3A3346', ink=INK, sw=.6)
        glow(x, y - 60 * s, 70 * s, '#FF6A3C', .5)
        for k in range(6):
            G.c.drawLine(x - 50 * s + k * 20 * s, y - 70 * s, x - 44 * s + k * 20 * s, y - 92 * s, P_('#8A4A2A', 1, 4 * s))
        smoke(t, x, y - 96 * s, .4, .9 * s, seed)
        G.c.drawLine(x - 50 * s, y - 44 * s, x - 50 * s, y, P_(INK, 1, 3 * s))
        G.c.drawLine(x + 50 * s, y - 44 * s, x + 50 * s, y, P_(INK, 1, 3 * s))
        sign = '烧烤'
    paint(rrPts(x - 52 * s, y - 150 * s, 104 * s, 36 * s, 6 * s), wash='#FFF1C8', ink=INK, sw=.5)
    text(sign, x, y - 132 * s, 24 * s, '#B0403E', face=WK, shadow=False)


def powerLines(y0, t, n=3, birds=False):
    for k in range(n):
        pts = [[x, y0 + k * 18 + math.sin(x / W * math.pi) * 40] for x in range(-60, W + 80, 40)]
        boilSeed(f'pl{k}')
        inkLine(pts, .45, '#2E2A38', 'inkfine', .3)
    if birds:
        for i in range(4):
            bx = 200 + i * 70
            G.c.drawCircle(bx, y0 + 30 + math.sin(bx / W * math.pi) * 40 - 8, 8, P_('#2E2A38'))


# ================================================================ apartment door landing (dense): 北方 302 / 南方 502, neighbour 301 on the side wall
def doorScene(t, city='north', light='night', sill=0.0, note=0.0, noteTxt=('示例歌词占位文字？', '我在门口。'), doorOpen=0.0, clear=False,
              neighbor=0.0, cat_=0.0, flyers=True, prints=1.0):
    north = city == 'north'
    night = light == 'night'
    wallU = ('#E7E0D2' if north else '#E2E6DA') if not night else ('#5E5C72' if north else '#55615E')
    gradRect(-400, -400, W + 800, H + 800, [wallU, mixCol(wallU, '#000000', .08)])
    flatRect(-400, -400, W + 800, 470, mixCol(wallU, '#000000', .12))
    for i in range(7):                                                        # stains and patched plaster
        boilSeed(f'stain{i}{city}')
        paint(ellPts(260 + hash1(i * 3) * 800, 140 + hash1(i * 7) * 700, 30 + 50 * hash1(i), 18 + 30 * hash1(i * 5), 14),
              wash=mixCol(wallU, '#7A6A54', .25), washOp=60, ink=None)
    boilSeed('crack' + city)
    inkLine([[700, 90], [690, 160], [712, 210], [700, 280]], .3, mixCol(wallU, INK, .5), 'inkfine', .4)
    # gas pipe along the top + conduit
    G.c.drawRect(skia.Rect.MakeXYWH(-40, 88, W + 80, 14), P_('#E9C84A'))
    G.c.drawRect(skia.Rect.MakeXYWH(-40, 88, W + 80, 14), P_(INK, .6, 1.4))
    for bx in (300, 640, 980):
        G.c.drawRect(skia.Rect.MakeXYWH(bx, 84, 10, 22), P_('#8A8478'))
    G.c.drawLine(470, 102, 470, 600, P_('#BDB6AA', 1, 7))
    lowc = '#8A6A54' if north else '#6E8A70'
    flatRect(230, 900, W + 400, 320, lowc, .92)
    flatRect(230, 896, W + 400, 8, INK, .45)
    for i in range(6):                                                        # scuffs on the lower wall
        G.c.drawLine(260 + i * 140, 960 + 40 * hash1(i), 300 + i * 140, 965 + 40 * hash1(i), P_(mixCol(lowc, INK, .4), .6, 3))
    # left side wall in perspective with the neighbour's door 301
    sidec = mixCol(wallU, '#000000', .14)
    boilSeed('side' + city)
    paint([[-80, -60], [230, 40], [230, 1215], [-80, 1330]], wash=sidec, ink=INK, sw=.8)
    paint([[-80, 920], [230, 900], [230, 1215], [-80, 1330]], wash=mixCol(lowc, '#000000', .12), ink=None)
    nd = [[40, 330], [196, 372], [196, 1150], [40, 1200]]
    if neighbor > .01:
        glow(196, 760, 260, '#FFC890', .55 * neighbor)
        paint([[196, 372], [196 - 34 * neighbor, 380], [196 - 34 * neighbor, 1160], [196, 1150]], wash='#FFD9A0', ink=None)
    paint(nd, wash='#4E6A5A' if north else '#8A4A3A', fill='#3A5446' if north else '#6E3428', fillOp=90, ink=INK, sw=.7)
    paint([[60, 520], [100, 530], [100, 600], [60, 590]], wash='#D9393E', ink=None)                    # 福 square on 301 (seen at an angle)
    paint([[18, 380], [30, 383], [30, 1150], [18, 1154]], wash='#C9393E', ink=None)                    # couplet strip
    paint([[150, 440], [166, 444], [166, 470], [150, 466]], wash='#C9A24A', ink=INK, sw=.3)             # 301 plate
    text('301', 158, 456, 12, INK, face=WK, shadow=False)
    if cat_ > .01:
        cat(150, 1150, 1.0, '#E9A23B', t)
    # 301's shoe rack + umbrella bucket on the floor in front of it
    boilSeed('rack301')
    paint([[0, 1150], [150, 1130], [150, 1210], [0, 1240]], wash='#8A6A44', ink=INK, sw=.6)
    for k in range(3):
        G.c.drawOval(skia.Rect.MakeXYWH(14 + k * 44, 1120 - k * 6, 36, 16), P_(['#3A3346', '#E9585E', '#5D8FC9'][k]))
    paint(rrPts(-10, 1040, 46, 120, 8), wash='#5D8FC9', ink=INK, sw=.5)
    G.c.drawLine(10, 1040, 0, 980, P_(INK, 1, 3))
    G.c.drawLine(24, 1040, 34, 990, P_(INK, 1, 3))
    # stairwell window on the back wall (weather outside, the opposite block's windows)
    wx0, wy0, ww, wh = 262, 190, 200, 300
    boilSeed('swin' + city)
    paint(rectPts(wx0 - 14, wy0 - 14, ww + 28, wh + 28), wash='#BDB6AA', ink=INK, sw=.8)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(wx0, wy0, ww, wh))
    sky = ('#2F3A5A' if night else ('#B9C9DE' if north else '#8C9AB0'))
    if clear:
        sky = '#9FC4F0'
    gradRect(wx0, wy0, ww, wh, [sky, mixCol(sky, '#FFFFFF', .25)])
    paint(rectPts(wx0 + 20, wy0 + 60, 120, 260), wash=mixCol(sky, '#3A3346', .5), ink=None)              # the block across the yard
    for r in range(4):
        for c in range(2):
            litWindow(wx0 + 34 + c * 52, wy0 + 80 + r * 56, 34, 34, ['cook', 'tv', 'study', 'dark', 'family', 'plant'][(r * 2 + c + (0 if north else 3)) % 6],
                      t, north, r * 7 + c)
    if clear:
        G.c.drawCircle(wx0 + 160, wy0 + 60, 32, P_('#FFE7A8'))
    elif north:
        snow(t, wx0, wy0 - 20, wx0 + ww, wy0 + wh, 26, .95, 60, 13, 2.5, 6)
    else:
        rain(t, wx0, wy0 - 20, wx0 + ww, wy0 + wh, 30, .55, .15, 1400, 17)
    G.c.restore()
    G.c.drawLine(wx0 + ww / 2, wy0, wx0 + ww / 2, wy0 + wh, P_(INK, 1, 5))
    if north:
        for k in range(10):                                                  # frost on the glass edges
            G.c.drawCircle(wx0 + hash1(k) * ww, wy0 + wh - 6 - hash1(k * 3) * 30, 6 + 10 * hash1(k * 5), P_('#FFFFFF', .55))
        if sill > .01:
            paint([[wx0 - 16, wy0 + wh + 14], [wx0 + ww + 16, wy0 + wh + 14], [wx0 + ww + 10, wy0 + wh + 14 - 26 * sill], [wx0 + ww / 2, wy0 + wh + 14 - 40 * sill],
                   [wx0 - 10, wy0 + wh + 14 - 24 * sill]], wash='#FFFFFF', ink=INK, sw=.5)
    else:
        boilSeed('spider')
        paint(rrPts(wx0 + 60, wy0 + wh - 4, 70, 40, 6), wash='#B0604A', ink=INK, sw=.4)
        for k in range(7):
            an = -2.6 + k * .35
            inkLine([[wx0 + 95, wy0 + wh - 2], [wx0 + 95 + math.cos(an) * 60, wy0 + wh - 2 + math.sin(an) * 50]], .7, '#5E8A50', 'ink', .5)
    # cobweb in the corner
    for k in range(5):
        G.c.drawLine(232, 104, 232 + k * 14, 104 + (5 - k) * 12, P_('#FFFFFF', .35, 1))
    # meter box with a little dial and tangled wires, stickers
    boilSeed('meter')
    paint(rectPts(282, 590, 150, 160), wash='#A8ACA8', ink=INK, sw=.7)
    paint(rectPts(300, 610, 114, 60), wash='#E6EAE2', ink=INK, sw=.4)
    text('0312.7', 357, 640, 24, INK, face=WK, shadow=False)
    for k in range(3):
        inkLine([[320 + k * 30, 590], [330 + k * 26, 520], [460 + k * 4, 420 - k * 20]], .45, ['#2E2A38', '#B0403E', '#3F6A8A'][k], 'inkfine', .5)
    for (ax, ay, at, rot) in ((300, 780, '开锁 138****0520', -.05), (330, 960, '通下水道', .06), (270, 1040, '搬家 · 空调维修', -.03), (420, 1100, '收旧家电', .04)):
        push()
        translate(ax, ay)
        rotate(rot)
        tw = textW(at, 22, WK)
        G.c.drawRect(skia.Rect.MakeXYWH(-8, -16, tw + 16, 32), P_('#F3F0E6', .9))
        text(at, tw / 2, 0, 22, '#C0392B', face=WK, shadow=False, a=.85)
        pop()
    paint(rrPts(478, 800, 30, 44, 4), wash='#F3F0E6', ink=INK, sw=.4)                                      # light switch
    # milk box on the wall right of the door
    paint(rectPts(912, 560, 86, 96), wash='#3F7F6A', ink=INK, sw=.5)
    text('奶箱', 955, 600, 22, '#FFFDF6', face=WK, shadow=False)
    # ceiling bulb
    G.c.drawLine(640, -20, 640, 132, P_(INK, 1, 3))
    glow(640, 160, 330 if night else 140, '#FFE7A8', .62 if night else .22)
    paint(ellPts(640, 155, 24, 28, 14), wash='#FFF1C8', ink=INK, sw=.5)
    # the door + couplets + 横批 + 福
    dx0, dy0, dw, dh = 520, 380, 360, 820
    boilSeed('door' + city)
    fade = .55 if north else 1.0
    paint(rectPts(dx0 - 26, dy0 - 26, dw + 52, dh + 26), wash='#5E5A5A', ink=INK, sw=.8)
    for cxs in (dx0 - 66, dx0 + dw + 30):
        paint(rectPts(cxs, dy0 + 20, 36, 700), wash=mixCol('#D9393E', wallU, 1 - fade), ink=None)
        for k in range(7):
            G.c.drawRect(skia.Rect.MakeXYWH(cxs + 9, dy0 + 60 + k * 96, 18, 18), P_('#E9C84A', .5 * fade))
    paint(rectPts(dx0 + 40, dy0 - 76, dw - 80, 40), wash=mixCol('#D9393E', wallU, 1 - fade), ink=None)
    text('出入平安' if north else '万事如意', dx0 + dw / 2, dy0 - 56, 26, '#E9C84A', face=WK, shadow=False, a=.8 * fade + .1)
    if doorOpen > .01:
        flatRect(dx0, dy0, dw, dh, '#2A2420', 1.0)
        glow(dx0 + dw / 2, dy0 + dh / 2, 300, '#FFD9A0', .4 * doorOpen)
    dcol = '#8E3A34' if north else '#4E6A86'
    paint(rectPts(dx0, dy0, dw * (1 - .7 * doorOpen), dh), wash=dcol, fill=mixCol(dcol, INK, .3), fillOp=90, ink=INK, sw=.8)
    if doorOpen < .3:
        for (py, ph) in ((dy0 + 60, 300), (dy0 + 420, 330)):
            paint(rectPts(dx0 + 40, py, dw - 80, ph), wash=None, ink=mixCol(dcol, INK, .5), sw=.5)
        paint(rrPts(dx0 + dw - 70, dy0 + 420, 26, 80, 8), wash='#C9A24A', ink=INK, sw=.5)
        G.c.drawCircle(dx0 + dw / 2, dy0 + 250, 8, P_('#C9A24A'))                                       # peephole
        paint(rrPts(dx0 + dw / 2 - 60, dy0 + 10, 120, 54, 6), wash='#E9E2D2', ink=INK, sw=.5)
        text('302' if north else '502', dx0 + dw / 2, dy0 + 37, 36, INK, face=WK, shadow=False)
        push()
        translate(dx0 + dw / 2, dy0 + 150)
        rotate(math.pi / 4)
        paint(rectPts(-52, -52, 104, 104), wash=mixCol('#D9393E', dcol, 1 - fade), ink=INK, sw=.4)
        pop()
        text('福', dx0 + dw / 2, dy0 + 150, 66, mixCol('#FFE08A', dcol, .3 if north else 0), face=WK, shadow=False, rot=math.pi)
        if north:
            for (ux, uy) in ((dx0 + 70, dy0 + 610),):                                                     # a little snowman sticker
                paint(ellPts(ux, uy, 20, 20, 12), wash='#FFFFFF', ink=INK, sw=.4)
                paint(ellPts(ux, uy - 30, 14, 14, 12), wash='#FFFFFF', ink=INK, sw=.4)
                paint(rectPts(ux - 13, uy - 21, 26, 6), wash='#CC3B42', ink=None)
    if note > .01:
        push()
        translate(dx0 + dw / 2 - 20, dy0 + 330)
        rotate(-.05)
        G.c.saveLayerAlpha(None, int(255 * clamp(note * 3)))
        paint(rectPts(-150, -80, 300, 160), wash='#FFE58A', ink=INK, sw=.5)
        n = len(noteTxt[0]) + len(noteTxt[1])
        shown = int(n * clamp(note))
        text(noteTxt[0][:shown], -130, -22, 34, INK, face=WK, align='left', shadow=False)
        text(noteTxt[1][:max(0, shown - len(noteTxt[0]))], -130, 34, 34, INK, face=WK, align='left', shadow=False)
        G.c.restore()
        pop()
    # floor tiles, doormat, flyers / parcel (north: nobody home), footprints, shoe rack, plant
    flatRect(230, 1200, W + 400, 800, '#9A9284' if north else '#8E8A7C', 1.0)
    flatRect(-400, 1215, 640, 800, '#8E877A' if north else '#83806F', 1.0)
    for k in range(8):
        G.c.drawLine(-200, 1240 + k * 50, W + 200, 1240 + k * 50, P_(INK, .18, 2))
    for k in range(12):
        G.c.drawLine(-100 + k * 110, 1200, -260 + k * 130, H + 60, P_(INK, .14, 2))
    paint(rrPts(dx0 + 20, 1196, dw - 40, 46, 6), wash='#7E5C46' if north else '#5E6E5A', ink=INK, sw=.5)
    text('出入平安', dx0 + dw / 2, 1219, 22, '#E9C84A', face=WK, shadow=False, a=.7)
    if north and flyers:
        for k, (fx, fr, fc) in enumerate(((600, .3, '#FFFDF6'), (660, -.2, '#FFE58A'), (720, .5, '#BFE3F2'))):
            push()
            translate(fx, 1214)
            rotate(fr)
            G.c.drawRect(skia.Rect.MakeXYWH(-34, -10, 68, 22), P_(fc))
            G.c.drawRect(skia.Rect.MakeXYWH(-34, -10, 68, 22), P_(INK, .6, 1.2))
            pop()
        paint(rrPts(800, 1130, 110, 76, 6), wash='#C9A27A', ink=INK, sw=.6)                                # a parcel waiting for her
        G.c.drawLine(800, 1168, 910, 1168, P_('#8A6A44', 1, 4))
        G.c.drawRect(skia.Rect.MakeXYWH(820, 1140, 40, 20), P_('#FFFDF6'))
    if prints > .01:
        for k in range(7):
            fx, fy = 120 + k * 60, 1300 + (k % 2) * 26 - k * 8
            G.c.drawOval(skia.Rect.MakeXYWH(fx, fy, 22, 12), P_('#5E5A66' if north else '#4E5A66', .28 * prints))
    boilSeed('rack' + city)
    paint(rectPts(920, 1110, 150, 96), wash='#8A6A44', ink=INK, sw=.6)
    for k in range(3):
        G.c.drawOval(skia.Rect.MakeXYWH(930 + k * 46, 1100, 40, 16), P_(['#E9A23B', '#3A3346', '#F19A92'][k] if north else ['#3A3346', '#5D8FC9', '#E8E4DE'][k]))
    boilSeed('plant' + city)
    paint(rrPts(1000, 1010, 60, 90, 8), wash='#B0604A', ink=INK, sw=.5)
    for k in range(6):
        an = -2.4 + k * .3
        col = '#8A7A5A' if north else '#5E8A50'
        inkLine([[1030, 1012], [1030 + math.cos(an) * 70, 1012 + math.sin(an) * 90]], .9, col, 'ink', .5)
    # light: morning / noon shaft from the stair window, dusk orange, night dim
    if light in ('day', 'noon', 'dawn', 'dusk'):
        col = {'day': '#FFF6DE', 'noon': '#FFF9E6', 'dawn': '#DDE8FF', 'dusk': '#FFB070'}[light]
        sh = {'day': 0, 'noon': 60, 'dawn': -40, 'dusk': 160}[light]
        pth = skia.Path()
        pth.moveTo(wx0, wy0 + 40)
        pth.lineTo(wx0 + ww, wy0 + 40)
        pth.lineTo(wx0 + ww + 420 + sh, 1420)
        pth.lineTo(wx0 + 140 + sh, 1420)
        pth.close()
        pa = P_(col, .16 if light != 'dusk' else .22)
        pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 30))
        G.c.drawPath(pth, pa)
        for i in range(18):                                                   # dust motes in the beam
            ph = frac(t * .05 + hash1(i))
            mx = wx0 + 80 + hash1(i * 3) * 380 + ph * 60
            my = wy0 + 120 + hash1(i * 7) * 900 - ph * 40
            G.c.drawCircle(mx, my, 2.2, P_('#FFFFFF', .5 * math.sin(ph * math.pi)))
    if night:
        G.c.drawRect(skia.Rect.MakeXYWH(-400, -400, W + 800, H + 800), P_('#0E1128', .18))


from hl import tint as _tint


# ================================================================ rainy old street (dense): AC units, laundry, neon, stall, passers-by, bikes, cat
def rainStreet(t, frozen=False, rainA=.55, lampK=1.0):
    tt = t if not frozen else 0.0
    _L2.rainStreet(t, frozen, rainA, lampK)
    # upper floors: balconies with laundry, AC units, lanterns, lit windows with life
    for i, (bx, by) in enumerate(((40, 380), (300, 330), (580, 400), (820, 350))):
        litWindow(bx + 20, by + 40, 90, 70, ['cook', 'tv', 'family', 'study'][i], tt, False, i)
        litWindow(bx + 130, by + 40, 90, 70, ['dark', 'plant', 'tv', 'cook'][i], tt, False, i + 9)
        G.c.drawLine(bx, by + 130, bx + 230, by + 130, P_('#5E5A66', 1, 3))
        for k in range(8):
            G.c.drawLine(bx + 5 + k * 30, by + 130, bx + 5 + k * 30, by + 160, P_('#5E5A66', 1, 2))
        laundry(bx + 4, bx + 226, by + 22, tt, i * 3, False)
        acUnit(bx + 160, by + 168, .9)
    for k in range(5):
        lantern(80 + k * 230, 640 - 20 * (k % 2), .9, tt)
    powerLines(240, tt, 3)
    neon(470, 560, '奶茶', '#E9585E', tt, 34, .3)
    neon(160, 600, '旅馆', '#5D8FC9', tt, 30, .7)
    # street life in front of the shops (far plane), the chestnut stall in the alley gap, steam from the noodle shop
    stall(520, 1068, '栗子', tt, .95, False, 3)
    steam(tt, 900, 860, 4, .5, 1.3, 220, 5)
    crowd(tt if not frozen else .3, -40, W + 40, 1092, 6, 1.05, False, 11, .95)
    cat(400, 1072, .9, '#3A3346', tt)
    boilSeed('menu')
    paint([[860, 1180], [960, 1180], [948, 1060], [872, 1060]], wash='#2E2A38', ink=INK, sw=.6)
    text('今日', 910, 1090, 20, '#FFFDF6', face=WK, shadow=False)
    text('牛肉面18', 910, 1122, 20, '#FFE58A', face=WK, shadow=False)
    scooter(1010, 1240, .9, '#E9585E')
    bike(60, 1250, .95, '#3F7F6A')


# ================================================================ city wide (dense): life in every window, street level with stalls, cars, lamps
def cityWide(t, city='north', tod='dawn', fig=None, fx=540, fy=1260, fu=6):
    north = city == 'north'
    night = tod == 'night'
    if north:
        sky = ['#8E9CC0', '#C9D2E6', '#F2D9C8'] if not night else ['#1E2444', '#34406A', '#4E5A80']
    else:
        sky = ['#4A5470', '#6E7690', '#8A8EA2'] if not night else ['#1E2238', '#2E3450', '#3E4460']
    gradRect(-400, -400, W + 800, H + 800, sky)
    # far skyline
    for i in range(9):
        bx, bh = -80 + i * 140, 200 + hash1(i * 13 + 5) * 300
        paint(rectPts(bx, 760 - bh, 130, bh + 300), wash=mixCol(sky[1], '#3A3346', .35), ink=None)
        for r in range(int(bh / 50)):
            for c in range(3):
                if hash1(i * 7 + r * 3 + c) > .6:
                    G.c.drawRect(skia.Rect.MakeXYWH(bx + 14 + c * 38, 760 - bh + 18 + r * 50, 16, 18), P_('#FFD27A', .45))
        if north and i % 3 == 0:
            G.c.drawRect(skia.Rect.MakeXYWH(bx + 90, 760 - bh - 40, 14, 40), P_('#5A5E6E'))
            smoke(t, bx + 97, 760 - bh - 44, .35, 1.0, i)
    # mid residential blocks with balconies: laundry, plants, AC, lanterns, people at the stove / TV / table
    kinds = ['cook', 'tv', 'family', 'study', 'dark', 'plant']
    for b in range(3):
        bx = -40 + b * 380
        top = 380 + 60 * (b % 2)
        col = ('#C9B8A0' if north else '#B8A898') if b != 1 else ('#B0A8B8' if north else '#A8B0A0')
        if night:
            col = mixCol(col, '#2E3450', .55)
        boilSeed(f'blk{b}{city}')
        paint(rectPts(bx, top, 340, 1000), wash=col, ink=INK, sw=.8)
        if north:
            paint(rectPts(bx - 8, top - 14, 356, 20), wash='#FFFFFF', ink=INK, sw=.5)
        for r in range(4):
            yy = top + 40 + r * 140
            for c in range(2):
                xx = bx + 30 + c * 160
                kind = kinds[(b * 5 + r * 2 + c) % 6] if (night or (b + r + c) % 3) else 'dark'
                litWindow(xx, yy, 120, 76, kind, t, north, b * 20 + r * 3 + c)
                G.c.drawLine(xx - 6, yy + 92, xx + 126, yy + 92, P_('#5E5A66', 1, 3))
                if (r + c + b) % 2 == 0:
                    laundry(xx - 4, xx + 124, yy - 6, t, b + r + c, frozen=north)
                elif (r + c) % 3 == 1:
                    acUnit(xx + 70, yy + 96, .7)
                else:
                    for k in range(3):
                        G.c.drawOval(skia.Rect.MakeXYWH(xx + k * 40, yy + 76, 26, 18), P_('#5E8A50' if not north else '#8A7A5A'))
                if north and r == 0 and c == 1:
                    lantern(xx + 110, yy + 112, .8, t)
    # street level: shopfronts with signs and warm interiors
    shops = [('热包子', '#B0403E'), ('超市', '#3F7F6A'), ('药房', '#4E6A9A'), ('奶茶', '#E9585E'), ('面馆', '#8A5A3C'), ('花店', '#7FB08A')]
    for i, (nm, sc) in enumerate(shops):
        sx = -30 + i * 190
        boilSeed(f'shop{i}{city}')
        paint(rectPts(sx, 930, 182, 170), wash='#FFE9B8' if (night or not north) else '#F7EBD2', fill='#FFD98A', fillOp=60, ink=INK, sw=.6)
        glow(sx + 91, 1020, 120, '#FFD98A', .35 if night else .18)
        paint(rectPts(sx, 900, 182, 40), wash=sc, ink=INK, sw=.6)
        text(nm, sx + 91, 920, 26, '#FFFDF6', face=WK, shadow=False)
        for k in range(3):
            G.c.drawRect(skia.Rect.MakeXYWH(sx + 16 + k * 54, 960, 40, 50), P_(['#E9585E', '#E9A23B', '#5D8FC9', '#7FB08A'][(i + k) % 4], .6))
        if north:
            paint(rectPts(sx - 4, 892, 190, 12), wash='#FFFFFF', ink=None)
    steam(t, 60, 900, 4, .55, 1.2, 200, 1)
    # road with cars and a bus, street lamps, trees, stalls
    roadc = '#E6ECF4' if north else '#3E4660'
    flatRect(-400, 1100, W + 800, 100, mixCol(roadc, '#5A5E6E', .5 if north else 0), 1.0)
    for k in range(9):
        G.c.drawRect(skia.Rect.MakeXYWH(-40 + k * 140, 1148, 70, 6), P_('#FFFDF6', .7))
    for i in range(4):
        d = 1 if i % 2 else -1
        cx_ = (hash1(i * 9) * 1500 + d * t * (180 + 60 * i)) % 1500 - 200
        cy_ = 1130 if d > 0 else 1170
        ccol = ['#E9585E', '#5D8FC9', '#E9E2D2', '#3A3346'][i]
        if i == 3:
            paint(rrPts(cx_ - 120, cy_ - 70, 240, 80, 12), wash='#3F7F6A', ink=INK, sw=.6)          # bus
            for k in range(5):
                G.c.drawRect(skia.Rect.MakeXYWH(cx_ - 108 + k * 44, cy_ - 60, 34, 26), P_('#FFE7A8', .9))
        else:
            paint(rrPts(cx_ - 50, cy_ - 34, 100, 34, 10), wash=ccol, ink=INK, sw=.5)
            paint(rrPts(cx_ - 30, cy_ - 52, 60, 22, 8), wash=mixCol(ccol, '#FFFFFF', .3), ink=INK, sw=.4)
        G.c.drawCircle(cx_ + 52 * d, cy_ - 16, 7, P_('#FFF3C0'))
        glow(cx_ + 70 * d, cy_ - 16, 50, '#FFF3C0', .45 if night else .2)
        G.c.drawCircle(cx_ - 52 * d, cy_ - 16, 5, P_('#FF4A4A'))
        if north:
            paint(rrPts(cx_ - 40, cy_ - 56, 80, 8, 4), wash='#FFFFFF', ink=None)
    for lx in (120, 520, 920):
        G.c.drawLine(lx, 1196, lx, 870, P_('#3A3346', 1, 6))
        G.c.drawLine(lx, 870, lx + 40, 860, P_('#3A3346', 1, 5))
        glow(lx + 44, 866, 90, '#FFE7A8', .55 if night else .2)
        G.c.drawCircle(lx + 44, 866, 9, P_('#FFE7A8'))
    for tx in (330, 760):
        boilSeed(f'tree{tx}{city}')
        G.c.drawLine(tx, 1196, tx, 1030, P_('#5A4234', 1, 10))
        if north:
            for k in range(5):
                an = -2.6 + k * .4
                inkLine([[tx, 1060], [tx + math.cos(an) * 90, 1060 + math.sin(an) * 110]], .9, '#5A4234', 'ink', .5)
                G.c.drawCircle(tx + math.cos(an) * 80, 1060 + math.sin(an) * 100, 9, P_('#FFFFFF'))
        else:
            paint(ellPts(tx, 990, 110, 80, 24), wash='#3E6A4A', fill='#2E5038', fillOp=80, ink=INK, sw=.6)
    flatRect(-400, 1196, W + 800, 800, '#F3F6FB' if north else '#4A5270', 1.0)
    if north:
        stall(220, 1196, '红薯', t, 1.0, True, 2)
        paint(ellPts(980, 1190, 28, 26, 14), wash='#FFFFFF', ink=INK, sw=.5)                               # a snowman by the kerb
        paint(ellPts(980, 1150, 19, 18, 14), wash='#FFFFFF', ink=INK, sw=.5)
        paint(rectPts(964, 1158, 32, 6), wash='#CC3B42', ink=None)
    else:
        stall(840, 1196, '烧烤', t, 1.0, False, 4)
        for k in range(6):
            G.c.drawRect(skia.Rect.MakeXYWH(-40 + k * 200 + 40 * hash1(k), 1230, 120, 8), P_('#FFD27A', .18))
    crowd(t, -40, W + 40, 1194, 7, 1.0, north, 21)
    if north:
        snow(t, -60, -60, W + 60, H, 150, .9, 80, 51, 2.5, 7)
    else:
        rain(t, -60, -60, W + 60, H, 170, .5, .18, 1600, 53)
    if fig:
        fig(fx, fy, fu)


# ================================================================ green-train four-seat booth (dense)
def trainBooth(t, outside='rain', mix=0.0, night=True, mainSide='right', others=(), refl=None, clock=None, clockSpeed=0.0, items=True, main=None):
    """booth seen across the table: window centre back (x 330–750), seats left (x<480) and right (x>600), luggage rack, ceiling fan;
    others = list of (side, draw(x, ground, u)) passengers; the main character is drawn by the shot (right seat x≈800 / left x≈280)"""
    gradRect(-400, -400, W + 800, H + 800, ['#E9E4D4', '#DCD6C2'] if not night else ['#B8B4A6', '#A8A496'])
    flatRect(-400, 760, W + 800, 900, '#5E8A70' if not night else '#4A6E5A', 1.0)
    flatRect(-400, 754, W + 800, 10, '#C9C2A8', 1.0)
    # ceiling: light strip and a fan
    flatRect(-400, -400, W + 800, 470, '#CFC8B2' if not night else '#9A9686', 1.0)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(300, 40, 480, 18), 9, 9, P_('#FFF8E0'))
    glow(540, 60, 260, '#FFF8E0', .35 if night else .15)
    G.c.drawLine(540, 58, 540, 96, P_(INK, 1, 4))
    for k in range(3):
        an = t * 9 + k * TAU / 3
        G.c.drawOval(skia.Rect.MakeXYWH(540 + math.cos(an) * 44 - 40, 96 + math.sin(an) * 6 - 6, 80, 12), P_('#8A8478', .8))
    G.c.drawCircle(540, 98, 12, P_('#5A5E6E'))
    # luggage racks with bags (woven bag, suitcase, box with rope, backpack)
    for (x0, x1) in ((-40, 470), (610, 1120)):
        G.c.drawLine(x0, 210, x1, 210, P_('#BDB6AA', 1, 6))
        G.c.drawLine(x0, 238, x1, 238, P_('#BDB6AA', 1, 6))
    boilSeed('bags')
    paint(rrPts(20, 120, 190, 96, 14), wash='#F3F0E6', fill='#D9D2C2', fillOp=80, ink=INK, sw=.6)
    for k in range(4):
        G.c.drawLine(20, 140 + k * 22, 210, 140 + k * 22, P_(['#D9393E', '#3B5B98', '#D9393E', '#3B5B98'][k], 1, 5))
    paint(rrPts(230, 130, 150, 86, 10), wash='#8A5A3C', ink=INK, sw=.6)
    G.c.drawLine(305, 130, 305, 216, P_('#C9A27A', 1, 4))
    paint(rrPts(640, 110, 160, 106, 10), wash='#3F6A8A', ink=INK, sw=.6)
    paint(rrPts(820, 140, 120, 76, 8), wash='#C9A27A', ink=INK, sw=.6)
    G.c.drawLine(820, 178, 940, 178, P_('#8A6A44', 1, 4))
    G.c.drawLine(880, 140, 880, 216, P_('#8A6A44', 1, 4))
    paint(rrPts(960, 124, 110, 92, 20), wash='#E9A23B', ink=INK, sw=.6)
    # the window between the two seats
    wx, wy, ww, wh = 330, 330, 420, 600
    boilSeed('twinB')
    paint(rrPts(wx - 20, wy - 20, ww + 40, wh + 40, 36), wash='#C9C4B4', ink=INK, sw=.8)
    G.c.save()
    G.c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(wx, wy, ww, wh), 28, 28), True)
    m = mix if outside == 'mix' else (1.0 if outside == 'snow' else 0.0)
    skyc = [mixCol('#1E2440', '#5A6890', m), mixCol('#2E3658', '#8EA0C0', m)] if night else [mixCol('#7A88A8', '#C8D4E6', m), mixCol('#9AA6BE', '#E6ECF4', m)]
    gradRect(wx, wy, ww, wh, skyc)
    for i in range(5):                                                            # villages flowing past: houses, lit windows, smoke
        hx = wx + ((i * 170 - t * 120) % (ww + 340)) - 170
        hy = wy + wh - 210
        paint(rectPts(hx, hy, 90, 60), wash=mixCol('#5A4E5E', '#B8C2D4', m), ink=None)
        paint([[hx - 10, hy], [hx + 45, hy - 34], [hx + 100, hy]], wash=mixCol('#7A3E34', '#FFFFFF', m), ink=None)
        G.c.drawRect(skia.Rect.MakeXYWH(hx + 18, hy + 18, 18, 18), P_('#FFD27A', .9 if night else .5))
        G.c.drawRect(skia.Rect.MakeXYWH(hx + 56, hy + 18, 18, 18), P_('#FFD27A', .6 if night else .3))
        smoke(t, hx + 70, hy - 30, .3, .5, i)
    paint(rectPts(wx, wy + wh - 150, ww, 150), wash=mixCol('#3A4A3A', '#EEF2F8', m), ink=None)
    for i in range(3):
        px = wx + ((i * 200 - t * 700) % (ww + 200)) - 100
        G.c.drawRect(skia.Rect.MakeXYWH(px, wy + 100, 9, wh), P_('#1A1E2C', .8))
        G.c.drawLine(px - 200, wy + 120, px + 200, wy + 150, P_('#1A1E2C', .5, 2))
    if m < .98:
        rain(t, wx, wy, wx + ww, wy + wh, 46, .5 * (1 - m), .9, 900, 23, ln=60)
    if m > .02:
        snow(t * 1.6, wx, wy, wx + ww, wy + wh, 36, .95 * m, 180, 27, 3, 7, drift=60)
    if refl:
        G.c.saveLayerAlpha(None, 70)
        refl()
        G.c.restore()
    G.c.restore()
    paint(rrPts(wx, wy, ww, wh, 28), wash=None, ink=INK, sw=.7)
    flatRect(wx, wy + wh * .42, ww, 6, '#9A958A', .7)
    paint(rrPts(wx + 70, wy - 92, ww - 140, 56, 8), wash='#2F4A7A', ink=INK, sw=.6)                  # route plate above the window
    text('K1314  南方 ⇄ 北方' if False else 'K1314  南方 — 北方', wx + ww / 2, wy - 64, 28, '#FFFDF6', face=WK, shadow=False)
    for (cx0, d) in ((wx - 40, 1), (wx + ww - 30, -1)):                              # curtains with tiebacks
        boilSeed(f'cur{cx0}')
        paint([[cx0, wy - 30], [cx0 + 70, wy - 30], [cx0 + 50 + 10 * d, wy + 380], [cx0 + 60, wy + wh + 30], [cx0 - 10, wy + wh + 30], [cx0 + 10, wy + 380]],
              wash='#3F7F8A', fill='#2E6070', fillOp=90, ink=INK, sw=.6)
        G.c.drawLine(cx0 + 4, wy + 380, cx0 + 64, wy + 384, P_('#E9C84A', 1, 5))
    if clock is not None:
        cx_, cy_ = 540, 290
        paint(ellPts(cx_, cy_, 46, 46, 24), wash='#FFFDF6', ink=INK, sw=.7)
        mn = clock + t * clockSpeed
        for (ln_, an, wd) in ((24, (mn / 720) * TAU - math.pi / 2, 5), (36, (mn / 60) * TAU - math.pi / 2, 3)):
            G.c.drawLine(cx_, cy_, cx_ + math.cos(an) * ln_, cy_ + math.sin(an) * ln_, P_(INK, 1, wd))
    # seat backs (blue vinyl benches)
    for (sx0, sx1) in ((-60, 450), (630, 1140)):
        boilSeed(f'seat{sx0}')
        paint(rrPts(sx0, 700, sx1 - sx0, 540, 30), wash='#3E5A8A', fill='#2E4670', fillOp=80, ink=INK, sw=.8)
        paint(rrPts(sx0 + 40, 720, sx1 - sx0 - 80, 64, 14), wash='#F3F0E6', ink=INK, sw=.5)
        paint(rrPts(sx0 - 10, 1180, sx1 - sx0 + 20, 50, 12), wash='#4A6698', ink=INK, sw=.6)
    boilSeed('jacket')                                                                  # a jacket hanging on the right wall hook
    G.c.drawCircle(1060, 300, 8, P_('#BDB6AA'))
    paint([[1030, 310], [1090, 310], [1110, 560], [1010, 560]], wash='#8A5A3C', ink=INK, sw=.6)
    for (side, draw) in others:
        draw(280 if side == 'left' else 800, 1300, 26)
    if main:
        main()
    # the table under the window with life on it
    boilSeed('tblB')
    paint(rrPts(300, 1140, 480, 28, 8), wash='#D9D2C2', fill='#BDB6AA', fillOp=80, ink=INK, sw=.7)
    paint(rectPts(520, 1168, 40, 140), wash='#9A958A', ink=INK, sw=.5)
    if items:
        paint(rrPts(330, 1044, 40, 98, 10), wash='#D9393E', ink=INK, sw=.6)                          # thermos with flowers
        for k in range(3):
            G.c.drawCircle(342 + k * 8, 1080 + k * 14, 5, P_('#FFFDF6'))
        paint([[392, 1060], [452, 1060], [446, 1140], [398, 1140]], wash='#FFFDF6', ink=INK, sw=.5)      # cup noodles
        paint([[394, 1080], [450, 1080], [448, 1100], [396, 1100]], wash='#E9585E', ink=None)
        steam(t, 422, 1050, 3, .45, .7, 100, 2)
        for k in range(3):
            G.c.drawCircle(600 + k * 30, 1126, 15, P_('#F29A3C'))                                       # oranges
            G.c.drawCircle(600 + k * 30, 1126, 15, P_(INK, .6, 1.3))
        for k in range(8):
            G.c.drawOval(skia.Rect.MakeXYWH(680 + hash1(k) * 70, 1128 + hash1(k * 3) * 8, 10, 6), P_('#C9A27A'))   # peanut shells
        ticket(500, 1126, 110, .15, 'K1314', '', key='tblticket')


def stationNorth(t, tx, train=True):
    _L2.stationNorth(t, tx, train)
    for k in range(3):
        lantern(300 + k * 240, 230, 1.0, t)
    crowd(t, -40, W + 40, 1060, 6, 1.25, True, 31)
    for k, (lx, col) in enumerate(((120, '#3F6A8A'), (980, '#B0403E'))):
        paint(rrPts(lx - 30, 1010, 60, 60, 8), wash=col, ink=INK, sw=.5)                                   # suitcases
        G.c.drawLine(lx, 1010, lx, 980, P_(INK, 1, 4))
    boilSeed('hotcart')
    paint(rrPts(780, 960, 180, 110, 12), wash='#E9E2D2', ink=INK, sw=.6)
    paint(rrPts(790, 920, 160, 46, 8), wash='#B0403E', ink=INK, sw=.5)
    text('热饮 · 茶叶蛋', 870, 943, 22, '#FFFDF6', face=WK, shadow=False)
    steam(t, 840, 950, 4, .6, 1.0, 160, 7)
    tinyPerson(760, 1070, 1.25, '#5E7A5A', t, False, hat='#C94A4A', seed=3)


def trainOutside(t, mix=0.0, night=False, x=0.0, dawn=0.0):
    _L2.trainOutside(t, mix, night, x, dawn)
    # the fields below the bridge: rows of paddies turning into snowy furrows, fences, bare trees, a cyclist on the farm road
    for k in range(9):
        yy = 1240 + k * 44
        G.c.drawLine(-60, yy, W + 60, yy + 20, P_(mixCol('#6E8A50', '#FFFFFF', mix), .8, 6))
        G.c.drawLine(-60, yy + 12, W + 60, yy + 32, P_(mixCol('#4A6A3A', '#C9D3E3', mix), .5, 3))
    for k in range(12):
        fx = -20 + k * 100
        G.c.drawLine(fx, 1200, fx, 1250, P_('#5A4234', 1, 5))
    G.c.drawLine(-20, 1214, W + 20, 1214, P_('#5A4234', 1, 3))
    for tx in (140, 620, 960):
        boilSeed(f'ftree{tx}')
        G.c.drawLine(tx, 1200, tx, 1090, P_('#4A3A2E', 1, 8))
        for k in range(4):
            an = -2.5 + k * .45
            inkLine([[tx, 1120], [tx + math.cos(an) * 70, 1120 + math.sin(an) * 80]], .7, '#4A3A2E', 'ink', .5)
            if mix > .4:
                G.c.drawCircle(tx + math.cos(an) * 60, 1120 + math.sin(an) * 70, 7, P_('#FFFFFF', mix))
    flatRect(-60, 1420, W + 120, 40, '#8A7A64', .9)
    bxp = (t * 60) % 1300 - 120
    tinyPerson(bxp, 1430, 1.2, '#B0604A', t, False, umb=(None if mix > .5 else '#3F7F6A'), hat=('#C94A4A' if mix > .5 else None), seed=4)
    G.c.drawCircle(bxp - 22, 1424, 14, P_(INK, 1, 3))
    G.c.drawCircle(bxp + 22, 1424, 14, P_(INK, 1, 3))
    # a village on the far bank: houses, lit windows, chimney smoke; a level crossing with people waiting
    for i in range(6):
        hx = (i * 210 - t * 30) % 1400 - 200
        hy = 970
        paint(rectPts(hx, hy - 60, 110, 60), wash=mixCol('#7A6A5A', '#C8D2E0', mix), ink=None)
        paint([[hx - 12, hy - 60], [hx + 55, hy - 100], [hx + 122, hy - 60]], wash=mixCol('#8E3A34', '#FFFFFF', mix), ink=None)
        G.c.drawRect(skia.Rect.MakeXYWH(hx + 20, hy - 44, 20, 20), P_('#FFD27A', .9 if (night or dawn > .3) else .45))
        smoke(t, hx + 90, hy - 104, .3, .6, i)
    for k in range(3):
        tinyPerson(860 + k * 40, 1180, .9, ['#7A6A4E', '#B0604A', '#4E6A7A'][k], t, False, umb=(None if mix > .5 else ['#5D8FC9', '#E9A23B', '#3F7F6A'][k]),
                   hat=('#C94A4A' if mix > .5 else None), seed=k)
    G.c.drawLine(820, 1180, 820, 1080, P_(INK, 1, 5))
    G.c.drawLine(820, 1090, 1000, 1080, P_('#E9585E', 1, 8))
    G.c.drawCircle(820, 1074, 10, P_('#FF4A4A' if frac(t * 1.5) < .5 else '#7A2A2A'))


# ================================================================ passengers, the guitar held properly
UNCLE = dict(HIM, name='uncle', hair='#3A3A40', hairLt='#5A5A62', coat='#7A6A4E', coatDk='#5A4E38', coatLt='#A08E6E', pants='#4E4A44', pantsDk='#363330')
STUDENT = dict(HIM, name='student', hair='#3A3346', coat='#5E8A6A', coatDk='#456A50', coatLt='#8AB896', pants='#3A3E58', pantsDk='#282B40')
AUNTIE = dict(HER, name='auntie', hair='#3A2A2A', hairLt='#5A4040', coat='#8A5A6E', coatDk='#6A4054', coatLt='#B08498', skirt='#4E4A44', skirtDk='#363330', scarf=None)


def passengerUncle(t, x, y, u, paper=True):
    jhim(x, y, u, dict(C=UNCLE, legs='sit', rot=.05, hands=dict(L=[-1.6, -7.8], R=[1.6, -7.8]), ex=dict(eyes='closed', mouth='o', blush=.3), key=71))
    if paper:
        boilSeed('paper')
        paint([[x - 2.6 * u, y - 9.6 * u], [x + 2.6 * u, y - 9.4 * u], [x + 2.4 * u, y - 6.0 * u], [x - 2.4 * u, y - 6.2 * u]], wash='#F3F0E6', ink=INK, sw=.5)
        for k in range(4):
            G.c.drawLine(x - 2.0 * u, y - 9.0 * u + k * .8 * u, x + 1.8 * u, y - 8.9 * u + k * .8 * u, P_('#8A8478', .8, 2))
        text('晚报', x - 1.2 * u, y - 9.0 * u, u * .9, INK, face=WK, shadow=False)
    for i in range(3):
        ph = frac(t * .5 + i / 3)
        text('z', x + 2.4 * u + ph * 40, y - 19 * u - ph * 70, 26 + 12 * ph, '#5E5A66', face=WK, shadow=False, a=math.sin(ph * math.pi))


def passengerStudent(t, x, y, u):
    jhim(x, y, u, dict(C=STUDENT, legs='sit', rot=-.05, hands=dict(L=[-1.4, -7.4], R=[1.4, -7.4]), ex=dict(eyes='closed', mouth='small'), key=72))
    G.c.drawArc(skia.Rect.MakeXYWH(x - 5.2 * u, y - 21.0 * u + 1.5 * u, 10.4 * u, 9 * u), 180, 180, False, P_('#2E2A38', 1, .7 * u))
    for d in (-1, 1):
        G.c.drawRoundRect(skia.Rect.MakeXYWH(x + d * 5.0 * u - .8 * u, y - 15.4 * u + 1.5 * u, 1.6 * u, 2.4 * u), 6, 6, P_('#E9585E'))


def guitarMid(t, strum=True):
    """mid layer for a sitting front-view player (body coords): body on the right thigh (screen left), neck out to the fretting hand
    (screen right). Pair with GUITAR_HANDS(t)."""
    def mid(u, sw):
        push()
        translate(-1.6 * u, -4.9 * u)
        rotate(1.2)
        boilSeed('gmid')
        bodyP = [[-.2, -2.6], [1.4, -2.2], [1.9, -1.0], [1.3, -.2], [2.1, .9], [1.8, 2.4], [0, 3.0], [-1.8, 2.4], [-2.1, .9], [-1.3, -.2], [-1.9, -1.0], [-1.4, -2.2]]
        paint(throughClosed([[a * u, b * u] for a, b in bodyP], 3), wash='#C98A4E', fill='#A86A36', fillOp=110, ink=INK, sw=.8)
        paint(ellPts(0, .2 * u, .7 * u, .7 * u, 16), wash='#3A2A22', ink=INK, sw=.4)
        paint(rectPts(-.9 * u, 1.5 * u, 1.8 * u, .35 * u), wash='#3A2A22', ink=None)
        paint(rectPts(-.32 * u, -8.6 * u, .64 * u, 6.2 * u), wash='#6E4A30', ink=INK, sw=.5)
        for k in range(5):
            G.c.drawLine(-.32 * u, (-3.4 - k * 1.0) * u, .32 * u, (-3.4 - k * 1.0) * u, P_('#D9D2C2', .8, 1.2))
        paint(rrPts(-.55 * u, -9.9 * u, 1.1 * u, 1.5 * u, 6), wash='#4A3226', ink=INK, sw=.5)
        wob = math.sin(t * 40) * .6 if strum else 0
        for i in range(3):
            xx = (-.18 + i * .18) * u
            G.c.drawLine(xx, -9.0 * u, xx + wob, 1.6 * u, P_('#EDE6D6', .75, 1.2))
        paint(heartPts(1.0 * u, -1.2 * u, .35 * u), wash='#E84A5F', ink=INK, sw=.3)
        pop()
    return mid


def GUITAR_HANDS(t, strum=True):
    return dict(L=[-.9, -5.6 + (.3 * math.sin(t * 10) if strum else 0)], R=[4.6, -7.5])
