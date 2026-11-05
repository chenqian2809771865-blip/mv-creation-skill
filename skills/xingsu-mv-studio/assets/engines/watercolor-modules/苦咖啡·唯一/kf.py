# kf.py: props and sets for 《苦咖啡·唯一》 — his coffee cart on a street corner, the chalk A-board, cups, the music box,
# geese, the ice heart, the bedroom (no window), etc. World units = logical 1920x1080 canvas.
import math
from eng import *
import eng
from clawd import *
from props import puff, sparkle, sparkles, floatHearts, stamp, bubble, tree, bush, lamp, city, hills, impactLines, sunburst, stripes
from dx import awning, apronHook, deskBell, smallBird, calendar11
from bbset import stringLights, wallClock2, bedsideTable, wallFrames, plant, rug
from props_bingbian import wallpaper, woodFloor, bedBack, blanket
from props_zuitian import noteGlyph, cloche
from wx import _pa, line
from common import *

WENKAI = 'LXGWWenKai-Regular.ttf'
GY = 860                     # ground line of the full shots
WOOD, WOODDK, WOODLT = '#C98B5A', '#8E5A36', '#E3B07E'
COFFEE, CREMA, MILK = '#4A2C1E', '#C78B5A', '#FFF4E2'
CHALK = '#F4F1E6'
BOARD = '#2F4A3F'
PINK, PINKDK = '#EE9AAE', '#C0637B'
HOT = '#FF6F96'
NIGHT_SKY = ['#1F2550', '#2F3C7A', '#5A5A9A']
DUSK_SKY = ['#4E4A8E', '#B97AA8', '#F6B68A']
DAY_SKY = ['#9CD3F0', '#CFEAF7', '#FFF4DE']
DAWN_SKY = ['#8E8CC8', '#F2B3B8', '#FFE2B8']


# ------------------------------------------------------------------ small helpers
def em(t, keys, base, **kw):
    o = emotions(t, keys, base)
    o.update(kw)
    return o


def emH(t, keys, **kw):
    return em(t, keys, HER, **kw)


def emM(t, keys, **kw):
    return em(t, keys, ME, **kw)


def ek(k):
    """emotion key time: just before the beat so the new face is fully there on the beat frame"""
    return B[k] - .06


def hitK(t, k, d=.12):
    a = t - (B[k] - .04)
    return 0.0 if a < 0 else math.exp(-a / d)


def landK(t, k, d=.16):
    """0..1 progress that reaches 1 on beat k (motion that arrives on the beat)"""
    return clamp((t - (B[k] - d)) / d)


def popK(t, k, d=.14):
    """backOut pop that starts ~1 frame before beat k"""
    return backOut(clamp((t - (B[k] - .045)) / d))


def handDot(x, y, col, r=10):
    """a little hand nub (body colour + ink) over the bottom of a held prop so it reads as 'held'"""
    G.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=skcol(col)))
    G.c.drawCircle(x, y, r, _pa(INK, 1, 2.2))


def chalkText(txt, x, y, size, prog=1.0, col=CHALK, a=1.0, face=WENKAI, rot=0.0):
    """chalk lettering revealed left→right by prog (0..1); slightly doubled for a dusty chalk look"""
    if prog <= 0 or a <= 0:
        return
    w = textW(txt, size, face) + size * .2
    push()
    translate(x, y)
    rotate(rot)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(-w / 2, -size, w * clamp(prog), size * 2))
    text(txt, 1.5, 1.5, size, col, face=face, shadow=False, a=.35 * a)
    text(txt, 0, 0, size, col, face=face, shadow=False, a=.92 * a)
    G.c.restore()
    pop()


def chalkLine(pts, prog=1.0, col=CHALK, sw=1.0, a=.9):
    """chalk stroke along pts revealed by prog"""
    if prog <= 0 or len(pts) < 2:
        return
    L = [0]
    for i in range(1, len(pts)):
        L.append(L[-1] + math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]))
    target = L[-1] * clamp(prog)
    out = [pts[0]]
    for i in range(1, len(pts)):
        if L[i] <= target:
            out.append(pts[i])
        else:
            f = (target - L[i - 1]) / max(1e-6, L[i] - L[i - 1])
            out.append([lerp(pts[i - 1][0], pts[i][0], f), lerp(pts[i - 1][1], pts[i][1], f)])
            break
    if len(out) >= 2:
        pa = skia.Paint(AntiAlias=True, Color=skcol(col, a), Style=skia.Paint.kStroke_Style, StrokeWidth=5 * sw,
                        StrokeCap=skia.Paint.kRound_Cap, StrokeJoin=skia.Paint.kRound_Join)
        p = skia.Path()
        p.moveTo(*out[0])
        for q in out[1:]:
            p.lineTo(*q)
        G.c.drawPath(p, pa)


def bage(t, k):
    """age for props.stamp so a beat stamp is (almost) full size on the beat frame"""
    return t - B[k] + .1


def writeK(t, k, d=.3, lead=.24):
    """writing progress that is complete on the beat frame of k"""
    return clamp((t - (B[k] - lead)) / d)


# ------------------------------------------------------------------ backgrounds
def skyGrad(cols, y1=GY):
    gradRect(-500, -500, W + 1000, y1 + 500, cols)


def pavement(y=GY, night=0.0, key='pv'):
    col = mixCol('#D9C9B4', '#4A4868', night * .8)
    flatRect(-500, y, W + 1000, H - y + 600, col)
    boilSeed(key)
    for i in range(-6, 34):
        x = i * 120
        line(x, y + 4, x - 60, H + 40, mixCol(col, INK, .18), .7, 2)
    line(-500, y + 70, W + 500, y + 70, mixCol(col, INK, .15), .7, 2)
    inkLine([[-500, y], [W + 500, y]], 1.1, INK, 'ink', 0)


def skyline(night=1.0, key='sk'):
    col = mixCol('#B9A9C8', '#2E3366', night)
    x = -200
    i = 0
    while x < W + 200:
        w = 150 + 110 * hash1(i * 3.3)
        h = 120 + 200 * hash1(i * 7.1)
        flat(rectPts(x, GY - 120 - h, w, h + 130), mixCol(col, '#FFFFFF', .08 * hash1(i)), .9)
        if night > .3:
            for r in range(int(h / 60)):
                for c_ in range(int(w / 50)):
                    if hash1(i * 13 + r * 5 + c_) > .55:
                        flatRect(x + 18 + c_ * 50, GY - 100 - h + 26 + r * 60, 14, 18, '#FFD98A', .55 * night)
        x += w + 10
        i += 1


def streetLamp(x, y=GY, s=1.0, on=1.0, key='lp', dirn=1, icicles=0.0):
    """tall street lamp, (x, y) = foot; dirn = which way the arm points"""
    boilSeed(key)
    paint(rectPts(x - 9 * s, y - 520 * s, 18 * s, 520 * s, 3), wash='#4A4760', ink=INK, sw=.9)
    paint(rectPts(x - 26 * s, y - 24 * s, 52 * s, 24 * s, 4), wash='#4A4760', ink=INK, sw=.8)
    d = dirn
    inkLine([[x, y - 515 * s], [x + d * 60 * s, y - 548 * s], [x + d * 96 * s, y - 530 * s]], 2.2, '#4A4760', 'ink', .4)
    hx = x + d * 97 * s
    paint([[hx - 27 * s, y - 530 * s], [hx + 27 * s, y - 530 * s], [hx + 15 * s, y - 552 * s], [hx - 15 * s, y - 552 * s]], wash='#4A4760',
          ink=INK, sw=.8)
    paint(ellPts(hx, y - 526 * s, 22 * s, 9 * s, 12), wash=mixCol('#77738A', '#FFE7A0', on), ink=INK, sw=.6)
    if on > .02:
        glow(hx, y - 520 * s, 230 * s, '#FFD27A', .75 * on)
        p = skia.Path()
        p.moveTo(hx - 19 * s, y - 522 * s)
        p.lineTo(hx + 19 * s, y - 522 * s)
        p.lineTo(hx + 150 * s, y)
        p.lineTo(hx - 150 * s, y)
        p.close()
        G.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol('#FFE7A0', .13 * on)))
    if icicles > 0:
        for i in range(5):
            L = (24 + 30 * hash1(i * 2.1)) * s * clamp(icicles * 1.4 - i * .08)
            if L > 1:
                ix = hx - 24 * s + i * 12 * s
                paint([[ix - 5 * s, y - 524 * s], [ix + 5 * s, y - 524 * s], [ix, y - 524 * s + L]], wash='#DDF2FB', ink=INK, sw=.5)
    return hx, y - 526 * s


def apron(view='q', flip=False):
    """his café apron (waist panel + pocket with 「橙」 + straps), body-local; stays below the mouth"""
    def h(u, sw):
        V = VIEWS[view]
        L, R = V['L'] * u, V['R'] * u
        y0, y1 = -3.7 * u, -1.7 * u
        boilSeed('apron')
        paint(rectPts(L + .45 * u, y0, R - L - .9 * u, y1 - y0, u * .05), wash='#5A3A2A', fill='#3A2418', fillOp=60, ink=INK, sw=sw * .7)
        inkLine([[L + .25 * u, y0], [R - .25 * u, y0]], sw * 1.1, '#E8D9BE', 'ink', 0)
        cx = V['face']['cx'] * u if V.get('face') else 0
        paint(rectPts(cx - 1.2 * u, -3.1 * u, 2.4 * u, .95 * u), wash='#6E4A36', ink=INK, sw=sw * .45)
        push()
        translate(cx, -2.62 * u)
        if flip:
            scale(-1, 1)
        text('橙', 0, 0, u * .7, '#FFD9A8', shadow=False)
        pop()
        xs = [L + 1.15 * u, R - 1.15 * u] if view == 'front' else ([-1.9 * u] if view == 'q' else [])
        for x in xs:
            inkLine([[x, y0], [x, -7.95 * u]], sw * 1.0, '#5A3A2A', 'ink', 0)
    return h


def heO(t, keys, view='q', flip=False, apron_=True, **kw):
    """his options: emotions + the apron"""
    o = emotions(t, keys, ME)
    o.update(view=view, flip=flip)
    if apron_:
        o['draw'] = apron(view, flip)
    o.update(kw)
    return o


def sheO(t, keys, view='q', flip=True, **kw):
    o = emotions(t, keys, HER)
    o.update(view=view, flip=flip)
    o.update(kw)
    return o


def hands(x, y, u, o):
    return handXY(x, y, u, o, 'L'), handXY(x, y, u, o, 'R')


def nearHand(x, y, u, o, tx):
    a, b = hands(x, y, u, o)
    return a if abs(a[0] - tx) < abs(b[0] - tx) else b


def potPlant(x, y, s=1.0, key='pp', night=0.0):
    boilSeed(key)
    for i in range(5):
        a = -math.pi / 2 + (i - 2) * .42
        paint(ellPts(x + math.cos(a) * 30 * s, y - 70 * s + math.sin(a) * 34 * s, 16 * s, 34 * s, 12, 0, a + math.pi / 2),
              wash=mixCol('#7CC36B', '#2E4A5A', night * .5), ink=INK, sw=.6)
    paint([[x - 34 * s, y - 62 * s], [x + 34 * s, y - 62 * s], [x + 26 * s, y], [x - 26 * s, y]], wash=mixCol('#D9774E', '#5A4060', night * .4),
          ink=INK, sw=.8)


# ------------------------------------------------------------------ the coffee cart
CART = dict(x=960, w=460, top=GY - 262)


def cart(t, x=960, y=GY, s=1.0, night=0.0, key='cart', sign='小橙咖啡', machine=True, items=True, lit=1.0, drip=None):
    """his coffee cart: wheels, wooden body, counter slab, two poles, striped awning, name board.
    (x, y) = ground centre. Counter top at y − 262 s. Returns counter-top y."""
    boilSeed(key)
    wd = mixCol(WOOD, '#5A4A6A', night * .45)
    top = y - 262 * s
    # poles + awning + name board
    for px in (-205, 205):
        paint(rectPts(x + px * s - 7 * s, y - 610 * s, 14 * s, 360 * s), wash=mixCol('#6B5A50', '#3A3550', night * .5), ink=INK, sw=.7)
    awning(x - 262 * s, x + 262 * s, y - 640 * s, depth=78 * s, key=key + 'aw',
           cols=(mixCol('#C8643C', '#6A3C4A', night * .4), mixCol('#FFF5E2', '#B8B4D0', night * .4)))
    boilSeed(key + 'nb')
    paint(rrPts(x - 165 * s, y - 732 * s, 330 * s, 84 * s, 14 * s), wash=mixCol('#FFF5E2', '#D8D2E8', night * .3), fill='#E8D6BC', fillOp=50,
          ink=INK, sw=1.0)
    text(sign, x, y - 690 * s, 50 * s, '#B04A2E', shadow=False)
    if lit > .02 and night > .3:
        glow(x, y - 690 * s, 180 * s, '#FFE7A0', .35 * lit * night)
    # body
    boilSeed(key + 'bd')
    paint(rectPts(x - 210 * s, top + 12 * s, 420 * s, 180 * s, 3), wash=wd, fill=WOODDK, fillOp=55, ink=INK, sw=1.1)
    for i in range(1, 6):
        line(x - 210 * s + i * 70 * s, top + 22 * s, x - 210 * s + i * 70 * s, top + 186 * s, mixCol(WOODDK, INK, .2), .7, 2.5)
    # little front chalk menu
    paint(rrPts(x - 92 * s, top + 44 * s, 184 * s, 112 * s, 8 * s), wash=BOARD, ink=INK, sw=.8)
    text('MENU', x, top + 72 * s, 26 * s, CHALK, face=WENKAI, shadow=False, a=.9)
    line(x - 60 * s, top + 98 * s, x + 60 * s, top + 98 * s, CHALK, .5, 2)
    line(x - 60 * s, top + 122 * s, x + 40 * s, top + 122 * s, CHALK, .5, 2)
    # counter slab
    paint(rectPts(x - 235 * s, top, 470 * s, 18 * s, 2), wash=mixCol(WOODLT, '#7A6A8A', night * .4), fill=wd, fillOp=60, ink=INK, sw=1.0)
    # wheels
    for wx_ in (-140, 140):
        boilSeed(key + 'wh%d' % wx_)
        paint(ellPts(x + wx_ * s, y - 44 * s, 44 * s, 44 * s, 22), wash='#3D3A52', ink=INK, sw=1.0)
        paint(ellPts(x + wx_ * s, y - 44 * s, 16 * s, 16 * s, 12), wash='#B8B4C8', ink=INK, sw=.6)
    if machine:
        espresso(x - 120 * s, top, s * .9, lit=lit, key=key + 'es', drip=drip)
    if items:
        boilSeed(key + 'it')
        for i in range(3):
            cup(x + 150 * s, top - i * 22 * s, .62 * s, fill=0, key=f'{key}stk{i}', saucer=False)
        paint(rrPts(x + 40 * s, top - 74 * s, 56 * s, 74 * s, 10 * s), wash='#E8E1F0', washOp=200, ink=INK, sw=.7)   # sugar jar
        text('糖', x + 68 * s, top - 40 * s, 24 * s, INK, face=WENKAI, shadow=False, a=.8)
    return top


def espresso(x, y, s, lit=1.0, key='es', drip=None):
    """espresso machine, (x, y) = bottom centre"""
    boilSeed(key)
    paint(rrPts(x - 62 * s, y - 150 * s, 124 * s, 150 * s, 12 * s), wash='#D8D2E0', fill='#9A93AA', fillOp=60, ink=INK, sw=1.0)
    paint(rrPts(x - 50 * s, y - 140 * s, 100 * s, 34 * s, 6 * s), wash='#3D3A52', ink=INK, sw=.6)
    G.c.drawCircle(x - 28 * s, y - 123 * s, 6 * s, skia.Paint(AntiAlias=True, Color=skcol(mixCol('#5A3038', '#FF5A6E', lit))))
    G.c.drawCircle(x + 28 * s, y - 123 * s, 6 * s, skia.Paint(AntiAlias=True, Color=skcol(mixCol('#2E4A3A', '#7CF29A', lit))))
    if lit > .3:
        glow(x - 28 * s, y - 123 * s, 22 * s, '#FF5A6E', .6 * lit)
    paint(rectPts(x - 26 * s, y - 100 * s, 52 * s, 22 * s, 2), wash='#4A4760', ink=INK, sw=.7)       # group head
    paint(rectPts(x - 6 * s, y - 80 * s, 12 * s, 14 * s), wash='#4A4760', ink=INK, sw=.5)            # spout
    paint(rectPts(x - 52 * s, y - 16 * s, 104 * s, 16 * s, 2), wash='#9A93AA', ink=INK, sw=.6)        # drip tray


# ------------------------------------------------------------------ cups & coffee things
def cup(x, y, s=1.0, fill=1.0, key='cup', saucer=True, steam=0.0, t=0.0, col='#FFFDF6', coffee=COFFEE, label=None, heartSteam=0.0,
        steamCol=None, rot=0.0):
    """white ceramic cup, side view. (x, y) = bottom centre (saucer bottom). s=1 -> 84 px wide."""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    if saucer:
        paint(ellPts(0, -6 * s, 70 * s, 12 * s, 18), wash=col, fill='#E2DDEA', fillOp=60, ink=INK, sw=.8)
    body = [[-42 * s, -78 * s], [42 * s, -78 * s], [34 * s, -18 * s], [22 * s, -8 * s], [-22 * s, -8 * s], [-34 * s, -18 * s]]
    inkLine([[38 * s, -66 * s], [62 * s, -62 * s], [60 * s, -36 * s], [34 * s, -30 * s]], 2.6 * s, INK, 'ink', .5)
    paint(body, wash=col, fill='#E2DDEA', fillOp=60, ink=INK, sw=1.0)
    paint(ellPts(0, -78 * s, 42 * s, 9 * s, 18), wash=mixCol(col, coffee, clamp(fill)), ink=INK, sw=.7)
    if label:
        text(label, 0, -44 * s, 24 * s, '#B04A2E', face=WENKAI, shadow=False)
    pop()
    sc = steamCol or mixCol('#FFFFFF', INK, .15)
    if steam > 0:
        for i in range(2):
            ph = frac(t * .5 + i * .5)
            yy = y - 92 * s - ph * 80 * s
            pa = skia.Paint(AntiAlias=True, Color=skcol(sc, .8 * steam * math.sin(ph * math.pi)), Style=skia.Paint.kStroke_Style,
                            StrokeWidth=4 * s, StrokeCap=skia.Paint.kRound_Cap)
            p = skia.Path()
            p.moveTo(x - 12 * s + i * 24 * s, y - 88 * s)
            p.quadTo(x - 26 * s + i * 24 * s + math.sin(t * 3 + i) * 10 * s, yy + 30 * s, x - 8 * s + i * 24 * s, yy)
            G.c.drawPath(p, pa)
    if heartSteam > 0:
        k = heartSteam
        hp = heartPts(x, y - 150 * s - 20 * s * k, 78 * s * backOut(clamp(k * 1.4)), 22)
        p = eng._path(hp)
        G.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol('#FFD6E4', .55 * clamp(k * 2))))
        G.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol('#FF6F96', clamp(k * 2)), Style=skia.Paint.kStroke_Style, StrokeWidth=6))


def cupTop(x, y, r, art=None, artK=1.0, key='ct', t=0.0):
    """top-down cup on a saucer; art(x, y, r, k) paints the latte art on the crema"""
    boilSeed(key)
    G.c.drawCircle(x + 10, y + 12, r * 1.55, skia.Paint(AntiAlias=True, Color=skcol(INK, .16)))
    paint(ellPts(x, y, r * 1.55, r * 1.55, 30), wash='#FFFDF6', fill='#E2DDEA', fillOp=50, ink=INK, sw=.9)
    paint(rrPts(x + r * 1.0, y - r * .2, r * .62, r * .4, r * .18), wash='#FFFDF6', ink=INK, sw=.7)
    paint(ellPts(x, y, r * 1.08, r * 1.08, 28), wash='#FFFDF6', ink=INK, sw=.9)
    paint(ellPts(x, y, r * .95, r * .95, 28), wash=CREMA, fill='#A8683E', fillOp=60, ink=None)
    if art and artK > 0:
        G.c.save()
        cp = skia.Path()
        cp.addCircle(x, y, r * .95)
        G.c.clipPath(cp, skia.ClipOp.kIntersect, True)
        art(x, y, r, artK)
        G.c.restore()


def milkFill(pts, k=1.0):
    paint(pts, wash=MILK, washOp=int(255 * clamp(k)), ink=None)


def kettle(x, y, s, tilt=0.0, key='ket'):
    """gooseneck kettle; (x, y) = the handle grip (put it on the hand). Spout tip returned (world)."""
    push()
    translate(x, y)
    rotate(tilt)
    boilSeed(key)
    paint(rrPts(-10 * s, -18 * s, 82 * s, 70 * s, 18 * s), wash='#D8D2E0', fill='#9A93AA', fillOp=60, ink=INK, sw=1.0)
    paint(rrPts(14 * s, -28 * s, 34 * s, 12 * s, 5 * s), wash='#4A4760', ink=INK, sw=.6)
    inkLine([[72 * s, 30 * s], [104 * s, 20 * s], [118 * s, -14 * s], [134 * s, -26 * s]], 3.4 * s, INK, 'ink', .5)
    inkLine([[72 * s, 30 * s], [104 * s, 20 * s], [118 * s, -14 * s], [134 * s, -26 * s]], 2.0 * s, '#D8D2E0', 'ink', .5)
    inkLine([[-10 * s, -8 * s], [-30 * s, 2 * s], [-28 * s, 34 * s], [-10 * s, 40 * s]], 2.4 * s, INK, 'ink', .5)
    pop()
    c, sn = math.cos(tilt), math.sin(tilt)
    return x + 134 * s * c + 26 * s * sn, y + 134 * s * sn - 26 * s * c


def dripper(x, y, s, key='dr'):
    """pour-over cone sitting on a cup rim; (x, y) = bottom of the cone"""
    boilSeed(key)
    paint([[x - 46 * s, y - 60 * s], [x + 46 * s, y - 60 * s], [x + 12 * s, y], [x - 12 * s, y]], wash='#F2E6D6', fill='#D8C8B0', fillOp=50,
          ink=INK, sw=.9)
    paint(ellPts(x, y - 60 * s, 46 * s, 8 * s, 16), wash='#C8A07A', ink=INK, sw=.6)


def beanBag(x, y, s, key='bb', label='苦', rot=0.0):
    """burlap coffee-bean sack; (x, y) = bottom centre"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    pts = [[-48 * s, 0], [-54 * s, -60 * s], [-36 * s, -110 * s], [-20 * s, -122 * s], [0, -114 * s], [20 * s, -122 * s], [36 * s, -110 * s],
           [54 * s, -60 * s], [48 * s, 0]]
    paint(pts, wash='#C9A77A', fill='#9A7A52', fillOp=70, ink=INK, sw=1.0, curv=.3)
    inkLine([[-30 * s, -104 * s], [30 * s, -104 * s]], 1.2, '#7A5A3A', 'ink', .3)
    text(label, 0, -50 * s, 50 * s, '#5A3A22', face=WENKAI, shadow=False)
    pop()


def bean(x, y, s, rot=0.0):
    paint(ellPts(x, y, 9 * s, 6 * s, 10, 0, rot), wash='#5A3622', ink=INK, sw=.4)
    inkLine([[x - 6 * s * math.cos(rot), y - 6 * s * math.sin(rot)], [x + 6 * s * math.cos(rot), y + 6 * s * math.sin(rot)]], .4, '#2A1A10', 'inkfine', 0)


def sugarCube(x, y, s, rot=0.0, key='sc'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rrPts(-s, -s, 2 * s, 2 * s, s * .2), wash='#FFFFFF', fill='#E6E2EE', fillOp=60, ink=INK, sw=.8)
    for i in range(5):
        G.c.drawCircle((hash1(i * 3.3) - .5) * 1.4 * s, (hash1(i * 7.1) - .5) * 1.4 * s, s * .08, _pa('#D0CCDA'))
    pop()


def chili(x, y, s, rot=0.0):
    push()
    translate(x, y)
    rotate(rot)
    paint([[-s, 0], [-.4 * s, -.5 * s], [.8 * s, -.3 * s], [1.3 * s, .3 * s], [.4 * s, .3 * s]], wash='#E8392E', ink=INK, sw=.6, curv=.4)
    inkLine([[-s, 0], [-1.4 * s, -.4 * s]], .9, '#4E8A3A', 'ink', .3)
    pop()


def lemon(x, y, s, rot=0.0):
    paint(ellPts(x, y, s, s, 20), wash='#FFE36E', ink=INK, sw=.7)
    paint(ellPts(x, y, .78 * s, .78 * s, 20), wash='#FFF4B0', ink=None)
    for i in range(6):
        a = rot + i / 6 * TAU
        inkLine([[x, y], [x + math.cos(a) * .7 * s, y + math.sin(a) * .7 * s]], .5, '#E8C43A', 'inkfine', 0)


def marshmallow(x, y, s, rot=0.0):
    push()
    translate(x, y)
    rotate(rot)
    paint(rrPts(-s, -.8 * s, 2 * s, 1.6 * s, .5 * s), wash='#FFD6E4', ink=INK, sw=.6)
    pop()


def splash(x, y, age, s=1.0, col=COFFEE, n=7):
    if age < 0 or age > .45:
        return
    k = age / .45
    for i in range(n):
        a = -math.pi / 2 + (i - (n - 1) / 2) * .38
        r = 60 * s * easeOut(k)
        G.c.drawCircle(x + math.cos(a) * r, y + math.sin(a) * r * 1.2 + 120 * s * k * k, 7 * s * (1 - k * .6),
                       skia.Paint(AntiAlias=True, Color=skcol(col, 1 - k)))


# ------------------------------------------------------------------ the chalk A-board
def aBoard(x, y, s=1.0, key='ab', night=0.0, inner=None):
    """A-frame chalkboard sign. (x, y) = ground centre. Board area is returned (bx, by, bw, bh); inner(bx, by, bw, bh) draws on it."""
    boilSeed(key)
    wd = mixCol(WOOD, '#5A4A6A', night * .45)
    bw, bh = 300 * s, 360 * s
    bx, by = x - bw / 2, y - 60 * s - bh
    for sx in (-1, 1):
        inkLine([[x + sx * (bw / 2 + 4 * s), by - 20 * s], [x + sx * (bw / 2 + 30 * s), y]], 6 * s, INK, 'ink', 0)
        inkLine([[x + sx * (bw / 2 + 4 * s), by - 20 * s], [x + sx * (bw / 2 + 30 * s), y]], 4 * s, wd, 'ink', 0)
    paint(rrPts(bx - 22 * s, by - 26 * s, bw + 44 * s, bh + 52 * s, 10 * s), wash=wd, fill=WOODDK, fillOp=60, ink=INK, sw=1.1)
    paint(rectPts(bx, by, bw, bh, 2), wash=mixCol(BOARD, '#1E2A3A', night * .4), ink=INK, sw=.8)
    # chalk dust smudges
    for i in range(6):
        G.c.drawCircle(bx + bw * hash1(i * 4.1), by + bh * hash1(i * 2.3), 30 * s * (.5 + hash1(i)),
                       skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .035)))
    paint(rectPts(bx + 30 * s, by + bh - 8 * s, 70 * s, 10 * s), wash='#FFFDF6', ink=None)      # chalk stick on the ledge
    if inner:
        G.c.save()
        G.c.clipRect(skia.Rect.MakeXYWH(bx, by, bw, bh))
        inner(bx, by, bw, bh)
        G.c.restore()
    return bx, by, bw, bh


def chalkCouple(cx, cy, s, himK=1.0, herK=1.0, heartK=1.0, smear=0.0, t=0.0):
    """chalk doodle: little him (left) + her (right) with a heart between; smear washes HIM away (streaks run down)"""
    def boxFig(x, y, col, flower, k, sm):
        if k <= 0:
            return
        a = 1 - sm
        pts = [[x - 40 * s, y], [x - 40 * s, y - 70 * s], [x + 40 * s, y - 70 * s], [x + 40 * s, y], [x - 40 * s, y]]
        chalkLine(pts, k, col, 1.1 * s, .9 * a)
        for lx in (-24, -8, 8, 24):
            chalkLine([[x + lx * s, y], [x + lx * s, y + 18 * s]], k, col, .9 * s, .9 * a)
        chalkLine([[x - 40 * s, y - 40 * s], [x - 58 * s, y - 30 * s]], k, col, .9 * s, .9 * a)
        chalkLine([[x + 40 * s, y - 40 * s], [x + 58 * s, y - 30 * s]], k, col, .9 * s, .9 * a)
        if k > .6:
            for ex in (-14, 14):
                G.c.drawCircle(x + ex * s, y - 44 * s, 4 * s, skia.Paint(AntiAlias=True, Color=skcol(col, .9 * a)))
        if flower and k > .8:
            for i in range(5):
                ang = i / 5 * TAU
                G.c.drawCircle(x + 20 * s + math.cos(ang) * 9 * s, y - 80 * s + math.sin(ang) * 9 * s, 6 * s,
                               skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .9 * a)))
        if sm > 0:     # rain streaks running down from the figure
            for i in range(9):
                sx = x + (i - 4) * 10 * s
                L = (40 + 120 * hash1(i * 3.7)) * s * sm
                pa = skia.Paint(AntiAlias=True, Color=skcol(col, .55 * (1 - sm * .5)), StrokeWidth=4 * s, StrokeCap=skia.Paint.kRound_Cap)
                G.c.drawLine(sx, y - 60 * s + 30 * s * hash1(i), sx, y - 60 * s + L + 30 * s * hash1(i), pa)
    boxFig(cx - 80 * s, cy, '#FFB27A', False, himK, smear)
    boxFig(cx + 80 * s, cy, '#FFB3C6', True, herK, 0)
    if heartK > 0:
        hp = heartPts(cx, cy - 110 * s, 30 * s, 20)
        chalkLine(hp + [hp[0]], heartK, '#FF8FB0', 1.0 * s)


# ------------------------------------------------------------------ furniture
def stool(x, y, s=1.0, cushion=PINK, key='st', night=0.0):
    """bar stool, (x, y) = floor centre; seat top at y − 190 s (returned)"""
    boilSeed(key)
    top = y - 190 * s
    for sx in (-1, 1):
        inkLine([[x + sx * 20 * s, top + 10 * s], [x + sx * 40 * s, y]], 3.4 * s, mixCol('#4A4760', '#2A2840', night * .4), 'ink', 0)
    line(x - 30 * s, y - 70 * s, x + 30 * s, y - 70 * s, '#4A4760', 1, 4 * s)
    paint(ellPts(x, top, 60 * s, 14 * s, 18), wash=mixCol(WOODLT, '#7A6A8A', night * .4), ink=INK, sw=.8)
    if cushion:
        paint(ellPts(x, top - 9 * s, 52 * s, 13 * s, 18), wash=mixCol(cushion, '#6A5A8A', night * .35), ink=INK, sw=.7)
    return top - (12 * s if cushion else 0)


def highTable(x, y, s=1.0, key='ht', night=0.0, cloth=None):
    """small round standing table; (x, y) = floor centre. Top surface at y − 300 s (returned)."""
    boilSeed(key)
    top = y - 300 * s
    paint(rectPts(x - 8 * s, top + 10 * s, 16 * s, y - top - 20 * s), wash=mixCol('#4A4760', '#2A2840', night * .4), ink=INK, sw=.7)
    paint(ellPts(x, y - 6 * s, 56 * s, 12 * s, 16), wash='#4A4760', ink=INK, sw=.6)
    paint(ellPts(x, top, 96 * s, 18 * s, 22), wash=mixCol(cloth or WOODLT, '#7A6A8A', night * .4), fill=WOOD, fillOp=50, ink=INK, sw=.9)
    paint(rectPts(x - 96 * s, top, 192 * s, 10 * s), wash=mixCol(WOOD, '#5A4A6A', night * .4), ink=INK, sw=.6)
    return top


# ------------------------------------------------------------------ the corner (full shot) — the main set
LAY = dict(he=560, cart=960, table=1250, she=1520, stool=1750, lamp=1860, board=250, cs=.85, ts=.7, ss=.8)


def corner(t, mode='night', lights=1.0, lamp_=1.0, cartLit=1.0, key='cn', board=None, stoolCushion=True,
           table=True, extra=None, boardX=None, boardS=.95, drip=None, machine=True, items=True, cartX=None, lights2=None,
           stool_=True, tableX=None):
    """mode: 'night' | 'day' | 'dawn' | 'dusk'. Layout (LAY): he ~x 560, cart x 960 (s .85, counter top GY−223), table x 1300 (top GY−210),
    she ~x 1490, stool x 1700, lamp x 1860 (arm to the left). board = inner callback for the A-board (x 250).
    Returns dict(top=counter y, table=table-top y, stool=seat y)."""
    night = 1.0 if mode == 'night' else 0.0
    if mode == 'night':
        skyGrad(NIGHT_SKY)
        from sets import starField
        starField(t, 7, 50, 0, 0, W, 420, r=2.6)
        skyline(1.0, key + 'sk')
    elif mode == 'dusk':
        skyGrad(DUSK_SKY)
        skyline(.55, key + 'sk')
    elif mode == 'dawn':
        skyGrad(DAWN_SKY)
        glow(1500, 700, 500, '#FFE2B8', .6)
        skyline(.4, key + 'sk')
    else:
        skyGrad(DAY_SKY)
        for i, (cx, cy, s) in enumerate([(240, 140, 26), (900, 90, 20), (1540, 150, 28)]):
            puff(cx + 12 * math.sin(t * .4 + i), cy, s, '#FFFFFF', key=f'{key}cl{i}', a=.95)
        skyline(0.0, key + 'sk')
        tree(90, GY, 70, key=key + 'tr1')
    pavement(GY, night * .9 + (.25 if mode == 'dusk' else 0), key + 'pv')
    lampHead = streetLamp(LAY['lamp'], GY, 1.0, lamp_ * (1 if mode != 'day' else 0), key + 'lp', dirn=-1)
    cx_ = cartX if cartX is not None else LAY['cart']
    top = cart(t, cx_, GY, LAY['cs'], night * .9, key=key + 'cart', lit=cartLit, drip=drip, machine=machine, items=items)
    if mode != 'day':
        stringLights(t, cx_ + 205 * LAY['cs'], lampHead[0], GY - 520, sag=50, n=10, key=key + 'sl', on=lights)
        stringLights(t, -40, cx_ - 205 * LAY['cs'], GY - 600, sag=60, n=10, key=key + 'sl2', on=lights if lights2 is None else lights2)
    st = stool(LAY['stool'], GY, LAY['ss'], cushion=PINK if stoolCushion else None, key=key + 'stool', night=night * .8) if stool_ else None
    tt = highTable(tableX or LAY['table'], GY, LAY['ts'], key=key + 'tab', night=night * .8) if table else None
    if board is not None:
        aBoard(boardX or LAY['board'], GY + 20, boardS, key + 'ab', night * .8, inner=board)
    if extra:
        extra()
    return dict(top=top, table=tt, stool=st)


# ------------------------------------------------------------------ the bedroom (no window)
def bedroom(t, hh=1, mm=0, key='bd', lights=1.0, digital=None, dshake=0.0):
    """his bedroom at night: dotted wallpaper, wall clock, string lights, calendar, frames, floor, rug, plant, bedside table.
    Returns the bed's mattress line y (bedBack at x 1060, y 900, w 1000, s 30)."""
    wallpaper('#2F3358', '#383E68', key=key + 'wp')
    wallClock2(1060, 230, 60, hh, mm, night=1, key=key + 'wc')
    calendar11(1560, 200, .9, key=key + 'cal')
    wallFrames(420, 260, .8, night=1, key=key + 'wfr')
    stringLights(t, 560, 1560, 360, sag=44, n=16, key=key + 'sl', on=lights)
    woodFloor(840, col='#5A4E66', dk='#3E3550', key=key + 'fl')
    rug(1000, 1010, 760, 80, night=1, key=key + 'rug')
    plant(1760, 905, .95, night=1, key=key + 'plant')
    bedsideTable(330, 905, 26, night=1, key=key + 'bst', lampOn=lights, clock=None, frame='up')
    if digital:
        from sm import alarmClock
        alarmClock(330, 905 - 26 * 6.85, .42, txt=digital, key=key + 'ac', shake=dshake)
    bedBack(1060, 900, 1000, 30, key=key + 'bed', night=1)
    return 900


def bedFrontCover(key='bd', lump=0.0):
    blanket(1060, 900, 1000, 30, key=key + 'blk', night=1, lump=lump)


# ------------------------------------------------------------------ geese, ice, music box, film, misc
def goose(x, y, s, flap, dirn=1, key='gs', scarf=None, flower=False, col='#9A8E86', flowerS=9):
    """flying goose seen from the side; dirn=1 flies right. (x, y) = body centre."""
    push()
    translate(x, y)
    scale(dirn, 1)
    boilSeed(key)
    wa = math.sin(flap)
    paint(ellPts(0, 0, 46 * s, 18 * s, 18), wash=col, fill=mixCol(col, INK, .3), fillOp=50, ink=INK, sw=.8)
    paint([[34 * s, -6 * s], [62 * s, -22 * s], [70 * s, -26 * s], [74 * s, -18 * s], [40 * s, 6 * s]], wash='#3D3A52', ink=INK, sw=.6)
    paint(ellPts(78 * s, -22 * s, 12 * s, 9 * s, 12), wash='#3D3A52', ink=INK, sw=.6)
    paint([[88 * s, -22 * s], [100 * s, -18 * s], [88 * s, -15 * s]], wash='#F2A65A', ink=INK, sw=.5)
    G.c.drawCircle(80 * s, -24 * s, 2.4 * s, _pa('#FFFFFF'))
    paint(ellPts(68 * s, -14 * s, 9 * s, 4 * s, 10), wash='#FFFFFF', ink=None)
    paint([[-42 * s, -4 * s], [-62 * s, -12 * s], [-58 * s, 6 * s]], wash=mixCol(col, INK, .25), ink=INK, sw=.5)
    wing = [[-14 * s, -6 * s], [24 * s, -6 * s], [-6 * s, -6 * s - 58 * s * wa], [-30 * s, -6 * s - 46 * s * wa]]
    paint(wing, wash=mixCol(col, '#FFFFFF', .2), fill=mixCol(col, INK, .25), fillOp=40, ink=INK, sw=.7)
    if scarf:
        paint(ellPts(56 * s, -12 * s, 10 * s, 7 * s, 10, 0, -.6), wash=scarf, ink=INK, sw=.5)
        paint([[50 * s, -8 * s], [30 * s, 6 * s + 6 * s * math.sin(flap * 2)], [24 * s, -2 * s + 6 * s * math.sin(flap * 2)], [46 * s, -14 * s]],
              wash=scarf, ink=INK, sw=.5)
    pop()
    if flower:
        flowerAt(x + dirn * 78 * s, y - 34 * s - flowerS * .6 * s, flowerS * s, 1.0, .7)


def iceHeart(x, y, r, cracks=0.0, glowK=0.0, key='ih', t=0.0, shards=0.0):
    """a heart of ice; cracks 0..1 spreads crack lines, glowK = pink light inside"""
    boilSeed(key)
    if glowK > 0:
        glow(x, y, r * 2.2, '#FF8FB0', .7 * glowK)
    hp = heartPts(x, y, r, 30)
    paint(hp, wash='#CFEFFF', washOp=220, fill='#8FC8E8', fillOp=80, ink=INK, sw=1.3)
    if glowK > 0:
        paint(heartPts(x, y + r * .05, r * .55 * glowK, 24), wash='#FF8FB0', washOp=int(200 * glowK), ink=None)
    paint(ellPts(x - r * .45, y - r * .55, r * .18, r * .32, 12, 0, .5), wash='#FFFFFF', washOp=200, ink=None)
    paint(ellPts(x + r * .5, y - r * .6, r * .1, r * .16, 10, 0, -.4), wash='#FFFFFF', washOp=160, ink=None)
    if cracks > 0:
        n = int(2 + 10 * cracks)
        for i in range(n):
            a = hash1(i * 3.3) * TAU
            L = r * (.3 + .6 * hash1(i * 5.7)) * clamp(cracks * 1.5 - i * .05)
            if L <= 0:
                continue
            pts = [[x + (hash1(i) - .5) * r * .3, y]]
            for j in range(3):
                a += (hash1(i * 7 + j) - .5) * 1.2
                pts.append([pts[-1][0] + math.cos(a) * L / 3, pts[-1][1] + math.sin(a) * L / 3])
            inkLine(pts, 1.1, '#FFFFFF', 'ink', 0)
            inkLine(pts, .5, '#4A7AA8', 'inkfine', 0)


def iceBlock(x, y, w, h, k=1.0, key='ib'):
    if k <= 0:
        return
    boilSeed(key)
    G.c.saveLayerAlpha(None, int(255 * clamp(k)))
    paint(rrPts(x - w / 2, y - h, w, h, 18), wash='#CFEFFF', washOp=150, fill='#8FC8E8', fillOp=60, ink=INK, sw=1.2)
    paint(ellPts(x - w * .3, y - h * .78, w * .08, h * .14, 12, 0, .4), wash='#FFFFFF', washOp=200, ink=None)
    inkLine([[x + w * .2, y - h * .9], [x + w * .35, y - h * .7]], 1.0, '#FFFFFF', 'ink', 0)
    G.c.restore()


def musicBox(x, y, s, lid=0.0, glowK=0.0, lock=0.0, key='mb', figure=None, t=0.0):
    """wooden music box, (x, y) = bottom centre; lid 0 closed .. 1 open (hinged at the back); figure(fx, fy, k) draws the dancer"""
    boilSeed(key)
    if glowK > 0:
        glow(x, y - 70 * s, 200 * s, '#FFE7A0', .8 * glowK)
    if figure and lid > .3:
        figure(x, y - 76 * s, lid)
    paint(rrPts(x - 90 * s, y - 76 * s, 180 * s, 76 * s, 8 * s), wash='#C8564F', fill='#8E3A36', fillOp=60, ink=INK, sw=1.0)
    paint(rectPts(x - 90 * s, y - 50 * s, 180 * s, 10 * s), wash='#F2C53D', ink=INK, sw=.5)
    for i in range(3):
        G.c.drawCircle(x - 50 * s + i * 50 * s, y - 24 * s, 6 * s, _pa('#F2C53D'))
    # crank on the side
    inkLine([[x + 90 * s, y - 40 * s], [x + 112 * s, y - 40 * s], [x + 112 * s, y - 56 * s]], 1.4, INK, 'ink', 0)
    # lid hinged at the top back edge: open lid = a thin slab rotating up
    push()
    translate(x - 90 * s, y - 76 * s)
    rotate(-1.9 * clamp(lid))
    paint(rrPts(0, -22 * s, 180 * s, 22 * s, 6 * s), wash='#D9675F', fill='#8E3A36', fillOp=60, ink=INK, sw=.9)
    paint(heartPts(90 * s, -11 * s, 8 * s, 14), wash='#F2C53D', ink=None)
    pop()
    if lock > 0:
        k = backOut(clamp(lock))
        push()
        translate(x, y - 50 * s)
        scale(k)
        inkLine([[-12 * s, -16 * s], [-12 * s, -28 * s], [12 * s, -28 * s], [12 * s, -16 * s]], 2.0, '#B88A2A', 'ink', .5)
        paint(heartPts(0, -2 * s, 20 * s, 18), wash='#F2C53D', fill='#C99A2A', fillOp=60, ink=INK, sw=.8)
        G.c.drawCircle(0, -4 * s, 3 * s, _pa(INK))
        pop()


def notes(t, seed, pts, s=26, cols=('#FF6F96', '#FFB347', '#7FB8E6', '#8FD18A'), a=1.0):
    """music notes at given points (list of (x, y)); colours cycle"""
    for i, (x, y) in enumerate(pts):
        G.c.saveLayerAlpha(None, int(255 * clamp(a)))
        noteGlyph(x, y + 6 * math.sin(t * 5 + i), s, cols[i % len(cols)], rot=.15 * math.sin(t * 3 + i), key=f'nt{seed}{i}', double=i % 3 == 1)
        G.c.restore()


def clapper(x, y, s, openA=0.0, key='clp', txt='第 99 场'):
    """film clapperboard; (x, y) = bottom-left of the slate; openA = stick angle (0 closed)"""
    boilSeed(key)
    paint(rectPts(x, y - 150 * s, 240 * s, 150 * s, 2), wash='#2B2233', ink=INK, sw=1.0)
    for i in range(3):
        line(x + 12 * s, y - 105 * s + i * 40 * s, x + 228 * s, y - 105 * s + i * 40 * s, '#FFFFFF', .7, 2)
    text(txt, x + 120 * s, y - 84 * s, 30 * s, '#FFFFFF', face=WENKAI, shadow=False)
    text('苦咖啡', x + 120 * s, y - 42 * s, 26 * s, '#FFFFFF', face=WENKAI, shadow=False, a=.8)
    push()
    translate(x, y - 150 * s)
    rotate(-openA)
    paint(rectPts(0, -34 * s, 244 * s, 34 * s), wash='#FFFFFF', ink=INK, sw=1.0)
    for i in range(6):
        paint([[i * 42 * s + 6 * s, 0], [i * 42 * s + 26 * s, 0], [i * 42 * s + 44 * s, -34 * s], [i * 42 * s + 24 * s, -34 * s]], wash='#2B2233',
              ink=None)
    pop()
    paint(rectPts(x, y - 160 * s, 240 * s, 12 * s), wash='#FFFFFF', ink=INK, sw=.6)


def filmBorder(k=1.0, burn=0.0):
    """film strip frame around the screen: black side bands with sprocket holes; burn darkens the edges"""
    off = (1 - easeOut(k)) * 240
    for side in (-1, 1):
        x0 = (-20 - off) if side < 0 else (W - 120 + off)
        flatRect(x0, -60, 140, H + 120, '#16131C')
        for j in range(12):
            G.c.drawRoundRect(skia.Rect.MakeXYWH(x0 + 46, j * 96 + 10, 48, 60), 8, 8, _pa('#F3EBDC', .85))
    if burn > 0:
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), W * .62,
                                             [skcol('#2A1408', 0), skcol('#2A1408', 0), skcol('#120804', burn)], [0, .5 + .3 * (1 - burn), 1])
        G.c.drawRect(skia.Rect.MakeXYWH(-200, -200, W + 400, H + 400), skia.Paint(Shader=sh))


def micStand(x, y, s=1.0, key='mic', head=1.0):
    boilSeed(key)
    inkLine([[x - 40 * s, y], [x, y - 10 * s], [x + 40 * s, y]], 2.0, INK, 'ink', 0)
    paint(rectPts(x - 4 * s, y - 330 * s, 8 * s, 322 * s), wash='#4A4760', ink=INK, sw=.6)
    h = head * s
    paint(rrPts(x - 14 * h, y - 330 * s - 50 * h, 28 * h, 54 * h, 13 * h), wash='#3D3A52', ink=INK, sw=.8)
    for i in range(3):
        line(x - 10 * h, y - 330 * s - 38 * h + i * 12 * h, x + 10 * h, y - 330 * s - 38 * h + i * 12 * h, '#8A86A0', .8, 2)


def spotlight(x, top, y, w, a=1.0, col='#FFF2C8'):
    if a <= 0:
        return
    p = skia.Path()
    p.moveTo(x - 40, top)
    p.lineTo(x + 40, top)
    p.lineTo(x + w / 2, y)
    p.lineTo(x - w / 2, y)
    p.close()
    G.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol(col, .3 * a)))
    paint(ellPts(x, y, w / 2, 40, 28), wash=col, washOp=int(120 * a), ink=None)


def tinCan(x, y, s, rot=0.0, key='tc', col='#FFFDF6'):
    """paper-cup phone; (x, y) = centre of the cup's bottom (where the string ties)"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint([[0, -22 * s], [56 * s, -32 * s], [56 * s, 32 * s], [0, 22 * s]], wash=col, fill='#E2DDEA', fillOp=50, ink=INK, sw=.9)
    paint(ellPts(56 * s, 0, 8 * s, 32 * s, 14), wash='#E8E1D2', ink=INK, sw=.7)
    line(14 * s, -20 * s, 14 * s, 20 * s, HOT, .8, 3 * s)
    pop()


def soundWaves(x, y, ang, n, r0, dr, a=1.0, col=INK, sw=1.0, spread=.6):
    for i in range(n):
        r = r0 + i * dr
        p = skia.Path()
        p.addArc(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), math.degrees(ang - spread), math.degrees(2 * spread))
        G.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol(col, a * (1 - i / (n + 1))), Style=skia.Paint.kStroke_Style, StrokeWidth=5 * sw,
                                   StrokeCap=skia.Paint.kRound_Cap))


def jar(x, y, s, glowK=0.0, bloom=0.0, key='jar', t=0.0):
    """glass jar with her little white flower inside; (x, y) = bottom centre (≈ 120 s tall)"""
    boilSeed(key)
    if glowK > 0:
        glow(x, y - 60 * s, 170 * s, '#FFF2C8', .8 * glowK)
    inkLine([[x, y - 6 * s], [x, y - 54 * s]], 1.2, '#4E8A3A', 'ink', .3)
    paint(ellPts(x - 12 * s, y - 30 * s, 10 * s, 5 * s, 10, 0, -.5), wash='#7CC36B', ink=INK, sw=.4)
    flowerAt(x, y - 62 * s, (11 + 6 * bloom) * s, 1.0, .8)
    paint(rrPts(x - 46 * s, y - 120 * s, 92 * s, 120 * s, 22 * s), wash='#DDF2FB', washOp=90, ink=INK, sw=1.0)
    paint(rrPts(x - 40 * s, y - 134 * s, 80 * s, 16 * s, 5 * s), wash='#C9A77A', ink=INK, sw=.8)
    paint(ellPts(x - 26 * s, y - 80 * s, 6 * s, 26 * s, 10), wash='#FFFFFF', washOp=170, ink=None)


def mapBoard(x, y, w, h, key='map'):
    """a kraft-paper map pinned to a wall; (x, y) = top-left"""
    boilSeed(key)
    paint(rectPts(x + 10, y + 12, w, h), wash=INK, washOp=40, ink=None)
    paint(rectPts(x, y, w, h, 3), wash='#E8D3A8', fill='#C9A77A', fillOp=50, ink=INK, sw=1.0)
    boilSeed(key + 'land')
    paint([[x + w * .12, y + h * .2], [x + w * .45, y + h * .12], [x + w * .6, y + h * .35], [x + w * .5, y + h * .6], [x + w * .2, y + h * .55]],
          wash='#C8DDA0', ink=INK, sw=.6, curv=.4)
    paint([[x + w * .62, y + h * .5], [x + w * .88, y + h * .42], [x + w * .9, y + h * .8], [x + w * .66, y + h * .86]],
          wash='#C8DDA0', ink=INK, sw=.6, curv=.4)
    for i in range(6):
        inkLine([[x + w * (.1 + .13 * i), y + h * .9], [x + w * (.18 + .13 * i), y + h * .7]], .4, '#8A6A4A', 'inkfine', .3)
    text('南', x + w * .5, y + h - 30, 34, '#8A5A3A', face=WENKAI, shadow=False)


def mapPin(x, y, k, crossK=0.0, key='pin', sc=1.0):
    if k <= 0:
        return
    s = backOut(clamp(k)) * sc
    boilSeed(key)
    inkLine([[x, y], [x, y - 40 * s]], 1.2, '#6B6880', 'ink', 0)
    paint(ellPts(x, y - 46 * s, 13 * s, 13 * s, 12), wash='#E8392E', ink=INK, sw=.7)
    if crossK > 0:
        c = backOut(clamp(crossK))
        for sx in (-1, 1):
            G.c.drawLine(x - 30 * c * sc, y + 4 - 30 * c * sx * sc, x + 30 * c * sc, y + 4 + 30 * c * sx * sc,
                         skia.Paint(AntiAlias=True, Color=skcol('#D8394E'), StrokeWidth=9 * sc, StrokeCap=skia.Paint.kRound_Cap))


def miniHer(x, y, u, t, i=0, o=None):
    d = dict(view='front', eyes='happy', mouth='smile', blush=.6, boilKey=f'mh{i}', noShadow=True, aL=.6 + .4 * math.sin(t * 6 + i),
             aR=.6 - .4 * math.sin(t * 6 + i))
    d.update(o or {})
    her(x, y, u, d)


def thoughtCloud(x, y, w, h, k=1.0, key='tcl', col='#FFFFFF', tail=None):
    """big thought cloud centred at (x, y); tail = (tx, ty) where the little dots lead to"""
    if k <= 0:
        return
    s = backOut(clamp(k))
    push()
    translate(x, y)
    scale(s)
    boilSeed(key)
    pts = []
    for i in range(40):
        a = i / 40 * TAU
        r = 1 + .1 * abs(math.sin(a * 5))
        pts.append([math.cos(a) * w / 2 * r, math.sin(a) * h / 2 * r])
    paint(pts, wash=col, ink=INK, sw=1.2, curv=.3)
    pop()
    if tail:
        for j in range(3):
            f = (j + 1) / 4
            px, py = lerp(x, tail[0], .55 + f * .45), lerp(y + h / 2 * s, tail[1], .3 + f * .7)
            paint(ellPts(px, py, (16 - j * 4) * s, (12 - j * 3) * s, 12), wash=col, ink=INK, sw=.8)


def glassBell(x, y, r, key='gb'):
    """a clear glass bell jar; (x, y) = centre of its rim, r = radius"""
    boilSeed(key)
    d = [[-r, 0]]
    for i in range(1, 24):
        a = math.pi + i / 24 * math.pi
        d.append([x + math.cos(a) * r, y + math.sin(a) * r * 1.25])
    d = [[x - r, y]] + d[1:] + [[x + r, y]]
    paint(d, wash='#DDF2FB', washOp=60, ink=INK, sw=1.1)
    paint(ellPts(x, y - r * 1.3, r * .14, r * .1, 10), wash='#DDF2FB', washOp=200, ink=INK, sw=.7)
    paint(ellPts(x - r * .45, y - r * .7, r * .1, r * .32, 12, 0, .4), wash='#FFFFFF', washOp=170, ink=None)
    inkLine([[x - r - 8, y], [x + r + 8, y]], 1.4, INK, 'ink', 0)
