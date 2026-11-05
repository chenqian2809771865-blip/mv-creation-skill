# props2.py: new sets and props for the Rolling in the Deep x 小苹果 mashup (watercolour + ink, same engine as 疑心病).
import math
from eng import *
from clawd import *
from props import *

APPLE, APPLE_DK, APPLE_LT = '#E0303F', '#A81F2E', '#FF8A8A'
LEAF, LEAF_DK = '#7CC36B', '#4E9A47'
FIRE, FIRE_IN, FIRE_DK = '#FF7A2E', '#FFD45C', '#D8452A'


# ---------------------------------------------------------------- apple
def applePts(x, y, r, n=44):
    pts = []
    for i in range(n):
        th = i / n * TAU                      # 0 = top, clockwise
        px = math.sin(th) * r * 1.06
        py = -math.cos(th) * r * (1.0 if math.cos(th) > 0 else .94)
        d = ((th + math.pi) % TAU) - math.pi  # distance from top
        py += .24 * r * math.exp(-(d / .42) ** 2)
        db = th - math.pi
        py -= .07 * r * math.exp(-(db / .35) ** 2)
        pts.append([x + px, y + py])
    return pts


def apple(x, y, r, key='apple', shine=0.0, rot=0.0, bow=False, a=1.0):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    if shine > 0:
        glow(0, 0, r * 3.2, '#FFE8A0', .7 * shine)
    inkLine([[0, -r * .7], [r * .05, -r * 1.05], [r * .16, -r * 1.25]], max(.8, r / 22), '#6B4A35', 'ink', .5)
    paint([[r * .12, -r * 1.0], [r * .45, -r * 1.25], [r * .8, -r * 1.12], [r * .5, -r * .9]], wash=LEAF, ink=INK, sw=max(.5, r / 40), curv=.6)
    paint(applePts(0, 0, r), wash=APPLE, washOp=255 * a, fill=APPLE_DK, fillOp=110, ink=INK, sw=max(.6, r / 30))
    paint(ellPts(-r * .42, -r * .38, r * .2, r * .3, 12, 0, -.5), wash='#FFFFFF', washOp=170, ink=None)
    if shine > 0:
        sparkle(r * .55, -r * .55, r * .35 * shine, '#FFFFFF')
    if bow:
        for s in (-1, 1):
            paint([[0, -r * .78], [s * r * .55, -r * 1.05], [s * r * .5, -r * .55]], wash='#FFD84A', ink=INK, sw=max(.5, r / 40), curv=.3)
        paint(ellPts(0, -r * .78, r * .13, r * .13, 10), wash='#F2C53D', ink=INK, sw=max(.4, r / 50))
    pop()


def appleHook(r=1.4, shine=0.0, bow=False, key='ah'):
    def h(u, sw):
        apple(r * u * .9, -r * u * .2, r * u, key=key, shine=shine, bow=bow)
    return h


def giftHook(s=1.0, key='gift'):
    def h(u, sw):
        w = 3.0 * u * s
        boilSeed(key)
        paint(rectPts(-.2 * u, -w * .55, w, w * .8, u * .05), wash='#7FB8E6', ink=INK, sw=sw * .8)
        paint(rectPts(-.2 * u + w * .42, -w * .55, w * .16, w * .8), wash='#E8476E', ink=None)
        for sgn in (-1, 1):
            paint([[w * .5 - .2 * u, -w * .55], [w * .5 - .2 * u + sgn * w * .3, -w * .8], [w * .5 - .2 * u + sgn * w * .28, -w * .5]],
                  wash='#E8476E', ink=INK, sw=sw * .6, curv=.3)
    return h


# ---------------------------------------------------------------- fire
def flame(x, y, s, t, key='fl', k=1.0, col=FIRE, inner=FIRE_IN):
    """a flickering flame standing on (x, y), about s wide and 2.2 s tall; boils at 12 fps"""
    if k <= .02:
        return
    tt = onTwos(t)
    s *= k
    for layer, (c, sc) in enumerate(((col, 1.0), (inner, .55))):
        pts = []
        for i in range(28):
            a = i / 28 * TAU
            px, py = math.sin(a) * s * .5 * sc, math.cos(a) * s * .5 * sc
            if py < 0:  # upper half stretched into a tongue
                up = -py / (s * .5 * sc)
                py *= 1 + 2.8 * up
                px *= 1 - .55 * up
                px += math.sin(tt * 13 + up * 4 + hash1(len(key)) * 5) * s * .12 * up
            pts.append([x + px, y - s * .5 * sc + py])
        boilSeed(f'{key}{layer}')
        paint(pts, wash=c, ink=INK if layer == 0 else None, sw=clamp(s / 60, .4, 1.2), curv=.3)


def embers(t, seed, n, x0, y0, x1, y1, col='#FFB347'):
    tt = onTwos(t)
    for i in range(n):
        ph = frac(tt * (.4 + .4 * hash1(seed + i)) + hash1(i * 3.3 + seed))
        x = lerp(x0, x1, hash1(i * 7.1 + seed)) + math.sin(tt * 3 + i) * 18
        y = lerp(y1, y0, ph)
        r = 5 + 5 * hash1(i + seed * 2)
        paint(ellPts(x, y, r, r, 8), wash=col, washOp=255 * math.sin(ph * math.pi), ink=None)


# ---------------------------------------------------------------- phone close-up
def bigPhone(x, y, w, h, lit=1.0, key='bp'):
    boilSeed(key)
    paint(rrPts(x - w / 2, y - h / 2, w, h, w * .12, 1.5), wash='#2E2B3E', ink=INK, sw=1.6)
    scr = mixCol('#1E2235', '#BFE6FA', lit)
    paint(rrPts(x - w / 2 + w * .06, y - h / 2 + w * .1, w * .88, h - w * .2, w * .07), wash=scr, ink=None)
    if lit > .05:
        glow(x, y, w * 1.1, '#BDEBFF', .45 * lit)
    paint(rrPts(x - w * .12, y - h / 2 + w * .045, w * .24, w * .035, w * .02), wash='#11101A', ink=None)


def notifCard(x, y, w, k, who, msg, key='nc'):
    p = backOut(k)
    if p < .02:
        return
    h = w * .3
    push()
    translate(x, y)
    scale(p)
    boilSeed(key)
    paint(rrPts(-w / 2, -h / 2, w, h, h * .28, 1), wash='#FFFFFF', washOp=245, ink=INK, sw=1.0)
    apple(-w / 2 + h * .52, h * .06, h * .28, key=key + 'ap')
    text(who, -w / 2 + h * 1.05, -h * .2, h * .3, INK, align='left', shadow=False)
    text(msg, -w / 2 + h * 1.05, h * .2, h * .24, '#5A5468', align='left', shadow=False)
    paint(heartPts(w / 2 - h * .4, h * .18, h * .14, 18), wash=C['heart'], ink=None)
    pop()


# ---------------------------------------------------------------- house / window
def house(x, y, s, key='house', door=0.0, winLit=1.0):
    """little house, ground at y, centre x; s = unit (house ~ 9s wide). door 0 closed .. 1 open"""
    boilSeed(key)
    paint(rectPts(x - 4.5 * s, y - 6 * s, 9 * s, 6 * s, 2), wash='#F2C9A0', fill='#D9A577', fillOp=60, ink=INK, sw=1.2)
    paint([[x - 5.3 * s, y - 6 * s], [x, y - 9.4 * s], [x + 5.3 * s, y - 6 * s]], wash='#C8524F', fill='#8E2E35', fillOp=60, ink=INK, sw=1.2)
    # door (right)
    dx = x + 1.3 * s
    paint(rectPts(dx, y - 3.8 * s, 2.2 * s, 3.8 * s), wash='#3A2840', ink=INK, sw=1)
    if door < 1:
        w = 2.2 * s * (1 - door)
        paint(rectPts(dx, y - 3.8 * s, max(2, w), 3.8 * s), wash='#9B6B45', ink=INK, sw=1)
        paint(ellPts(dx + w - .4 * s, y - 1.9 * s, .16 * s, .16 * s, 8), wash='#F2C53D', ink=None)
    # window (left) with warm light
    wx, wy = x - 3.4 * s, y - 4.6 * s
    paint(rectPts(wx, wy, 2.6 * s, 2.2 * s), wash=mixCol('#3B3770', '#FFE3A0', winLit), ink=INK, sw=1)
    if winLit > .05:
        glow(wx + 1.3 * s, wy + 1.1 * s, 3 * s, '#FFD27A', .6 * winLit)
    return (wx, wy, 2.6 * s, 2.2 * s)


def curtain(wx, wy, ww, wh, open_=0.5, key='ct'):
    boilSeed(key)
    for sgn in (-1, 1):
        x0 = wx if sgn < 0 else wx + ww
        x1 = x0 - sgn * ww * .5 * (1 - open_)
        paint([[x0, wy], [x1, wy], [x1 + sgn * 6, wy + wh * .5], [x1, wy + wh], [x0, wy + wh]], wash='#E88FA8', fill='#B85C78', fillOp=60, ink=INK, sw=.8)


# ---------------------------------------------------------------- thermometer
def thermometer(x, y, h, lvl, key='th', burst=0.0):
    """stands on (x, y); lvl 0..1 (1 = top); burst > 0 cracks the bulb"""
    boilSeed(key)
    w = h * .11
    r = w * 1.05
    paint(rrPts(x - w / 2, y - h, w, h - r, w / 2), wash='#F4FBFF', washOp=230, ink=INK, sw=1.4)
    for i in range(9):
        yy = y - r * 1.6 - i * (h - r * 2.6) / 8
        inkLine([[x + w * .55, yy], [x + w * .95 if i % 2 == 0 else x + w * .8, yy]], .9, INK, 'inkfine', 0)
    top = y - r * 1.2 - (h - r * 2.4) * clamp(lvl, 0, 1.05)
    paint(rrPts(x - w * .22, top, w * .44, y - r * .8 - top, w * .2), wash=C['red'], ink=None)
    paint(ellPts(x, y - r * .9, r, r, 24), wash=C['red'], fill='#9E1F30', fillOp=80, ink=INK, sw=1.4)
    paint(ellPts(x - r * .35, y - r * 1.2, r * .22, r * .3, 10), wash='#FFFFFF', washOp=160, ink=None)
    if burst > 0:
        a = burst
        for i in range(10):
            ang = i / 10 * TAU + .2
            d = r * (1.2 + 3.5 * easeOut(clamp(a / .3)))
            paint(starPts(x + math.cos(ang) * d, y - h - r + math.sin(ang) * d * .7, 14 * (1 - clamp(a / .5) * .6), .4, 4), wash='#DDF2FF', ink=INK, sw=.6)


# ---------------------------------------------------------------- spotlight
def spotBeam(x, top, bottom_y, w0, w1, col='#FFF2C4', a=.35):
    flat([[x - w0 / 2, top], [x + w0 / 2, top], [x + w1 / 2, bottom_y], [x - w1 / 2, bottom_y]], col, a)
    boilSeed(f'pool{x}')
    paint(ellPts(x, bottom_y, w1 * .55, w1 * .12, 30), wash=col, washOp=110, ink=None)


def spotLamp(x, y, on, key='sl'):
    boilSeed(key)
    paint(rrPts(x - 34, y - 26, 68, 52, 12), wash='#3A3550', ink=INK, sw=1)
    paint(ellPts(x, y + 24, 30, 12, 16), wash=mixCol('#5A566E', '#FFF6CC', on), ink=INK, sw=.8)
    if on > .05:
        glow(x, y + 24, 120, '#FFF0B0', on)


# ---------------------------------------------------------------- crystal ball
def crystalBall(x, y, r, k=1.0, key='cb', inside=None):
    boilSeed(key)
    paint([[x - r * .9, y + r * .95], [x + r * .9, y + r * .95], [x + r * .6, y + r * .6], [x - r * .6, y + r * .6]], wash='#8E6A3E', ink=INK, sw=1.2)
    paint(rrPts(x - r * 1.05, y + r * .92, r * 2.1, r * .22, r * .08), wash='#6B4A35', ink=INK, sw=1)
    glow(x, y, r * 2.4, '#B9E6FF', .5 + .5 * k)
    paint(ellPts(x, y, r, r, 40), wash=mixCol('#C9B8EC', '#E6F7FF', k), washOp=235, ink=None)
    if inside:
        c = G.c
        c.save()
        c.clipPath(skia.Path().addCircle(x, y, r * .96), skia.ClipOp.kIntersect, True)
        inside()
        c.restore()
    paint(ellPts(x - r * .38, y - r * .42, r * .2, r * .32, 14, 0, -.6), wash='#FFFFFF', washOp=190, ink=None)
    paint(ellPts(x, y, r, r, 40), ink=INK, sw=1.4)


def tableCloth(y, col='#5B3F8E', key='tc'):
    boilSeed(key)
    pts = [[-80, y]]
    for i in range(13):
        pts.append([-80 + i * (W + 160) / 12, y + jit(3)])
    pts += [[W + 80, H + 80], [-80, H + 80]]
    paint(pts, wash=col, ink=None)
    inkLine(pts[1:14], 1.2, INK, 'ink', .3)
    for i in range(14):
        x = i * 150 + 40
        paint(starPts(x, y + 60 + (i % 2) * 70, 10, .4, 5), wash='#F2C53D', ink=None)


# ---------------------------------------------------------------- cork board + polaroids
def corkBoard(x, y, w, h, key='cork'):
    boilSeed(key)
    paint(rectPts(x - 18, y - 18, w + 36, h + 36, 2), wash='#9B6B45', ink=INK, sw=1.4)
    paint(rectPts(x, y, w, h, 2), wash='#D7A86E', fill='#B8864E', fillOp=70, ink=INK, sw=1)
    for i in range(140):
        px, py = x + hash1(i * 3.7) * w, y + hash1(i * 9.1) * h
        flatRect(px, py, 4, 3, '#A97A45', .5)


def polaroid(x, y, w, rot, k, scene, key='pol', label=None):
    """polaroid photo centred at (x, y); scene(cx, cy, iw, ih) paints the picture; k = pop-in"""
    p = backOut(k)
    if p < .02:
        return
    push()
    translate(x, y)
    rotate(rot)
    scale(p)
    boilSeed(key)
    h = w * 1.18
    paint(rectPts(-w / 2 + 8, -h / 2 + 10, w, h), wash=INK, washOp=60, ink=None)
    paint(rectPts(-w / 2, -h / 2, w, h, 1), wash='#FFFDF6', ink=INK, sw=1)
    iw, ih = w * .86, w * .8
    ix, iy = -iw / 2, -h / 2 + w * .07
    c = G.c
    c.save()
    c.clipRect(skia.Rect.MakeXYWH(ix, iy, iw, ih), skia.ClipOp.kIntersect, True)
    scene(0, iy + ih / 2, iw, ih)
    c.restore()
    inkStroke(rectPts(ix, iy, iw, ih), True, .5, INK, 'inkfine')
    if label:
        text(label, 0, h / 2 - w * .14, w * .13, INK, shadow=False)
    # push pin
    paint(ellPts(0, -h / 2 + 6, w * .055, w * .055, 12), wash=C['red'], ink=INK, sw=.7)
    pop()


def pinThread(pts):
    inkLine(pts, 1.6, '#E03A4E', 'ink', .2)


# ---------------------------------------------------------------- flowers / nature
PETALS = ['#F59AB0', '#FFE36E', '#FFFFFF', '#C9B8EC', '#FF9E7A', '#9FD8F0']


def bloom(x, y, s, k, col='#F59AB0', key='bl', centre='#FFD45C', stem=True):
    p = backOut(k) if k < 1 else 1
    boilSeed(key)
    if stem:
        inkLine([[x, y], [x + s * .1, y + s * 1.6], [x, y + s * 3]], max(.6, s / 28), LEAF_DK, 'ink', .5)
        paint([[x + s * .05, y + s * 1.8], [x + s * .9, y + s * 1.3], [x + s * .2, y + s * 2.2]], wash=LEAF, ink=INK, sw=.6, curv=.5)
    if p < .02:
        paint(ellPts(x, y, s * .25, s * .35, 10), wash=LEAF, ink=INK, sw=.6)
        return
    for i in range(5):
        a = i / 5 * TAU - math.pi / 2 + k * .3
        paint(ellPts(x + math.cos(a) * s * .55 * p, y + math.sin(a) * s * .55 * p, s * .42 * p, s * .42 * p, 12), wash=col, ink=INK, sw=max(.4, s / 50))
    paint(ellPts(x, y, s * .3 * p, s * .3 * p, 12), wash=centre, ink=INK, sw=max(.4, s / 50))


def petalsFly(t, seed, n, x0, y0, x1, y1, s=12, cols=None):
    cols = cols or ['#F59AB0', '#FFFFFF', '#FBD0DA']
    tt = onTwos(t)
    for i in range(n):
        ph = frac(tt * (.25 + .2 * hash1(i + seed)) + hash1(seed * 3 + i * 1.7))
        x = lerp(x0, x1, frac(hash1(seed + i * 5.3) + ph * .4))
        y = lerp(y0, y1, ph) + math.sin(tt * 2 + i) * 30
        boilSeed(f'pf{seed}{i}')
        paint(ellPts(x, y, s, s * .55, 10, 0, tt * 2 + i), wash=cols[i % len(cols)], ink=INK, sw=.4)


def butterfly(x, y, s, t, col='#FFB3C6', key='bf'):
    f = abs(math.sin(onTwos(t) * 18))
    boilSeed(key)
    for sgn in (-1, 1):
        paint(ellPts(x + sgn * s * .5 * f, y, s * .5 * f + 2, s * .6, 12), wash=col, ink=INK, sw=.5)
    inkLine([[x, y - s * .5], [x, y + s * .5]], .7, INK, 'ink', 0)


def starFace(x, y, r, wink=0.0, key='sf', col='#FFE36E'):
    boilSeed(key)
    glow(x, y, r * 2.4, '#FFF3B0', .5 + .5 * wink)
    paint(starPts(x, y, r * (1 + .15 * wink), .5, 5), wash=col, ink=INK, sw=max(.5, r / 40), curv=.15)
    ex = r * .2
    for sgn in (-1, 1):
        if wink > .5 and sgn > 0:
            inkLine([[x + sgn * ex - r * .1, y - r * .02], [x + sgn * ex, y - r * .1], [x + sgn * ex + r * .1, y - r * .02]], max(.5, r / 40), INK, 'ink', .4)
        else:
            paint(ellPts(x + sgn * ex, y - r * .05, r * .05, r * .08, 8), wash=INK, ink=None)
    inkLine([[x - r * .1, y + r * .12], [x, y + r * .18], [x + r * .1, y + r * .12]], max(.5, r / 45), INK, 'ink', .5)


def firefly(t, seed, n, x0, y0, x1, y1):
    tt = onTwos(t)
    for i in range(n):
        x = lerp(x0, x1, hash1(seed + i * 2.3)) + math.sin(tt * .9 + i * 1.3) * 40
        y = lerp(y0, y1, hash1(seed + i * 5.9)) + math.cos(tt * 1.1 + i) * 25
        on = .5 + .5 * math.sin(tt * 4 + i * 2)
        glow(x, y, 26, '#FFF29A', on)
        paint(ellPts(x, y, 4, 4, 8), wash='#FFF8C0', ink=None)


def wheat(x, y, h, sway, key='wh', col='#E9B44C'):
    boilSeed(key)
    tip = [x + sway * h * .3, y - h]
    inkLine([[x, y], [x + sway * h * .12, y - h * .5], tip], max(.5, h / 160), '#B98A45', 'ink', .5)
    for i in range(5):
        k = i / 5
        px, py = lerp(x + sway * h * .2, tip[0], k), lerp(y - h * .72, tip[1], k)
        for sgn in (-1, 1):
            paint(ellPts(px + sgn * h * .035, py, h * .03, h * .055, 8, 0, sgn * .5), wash=col, ink=None)


def mapleLeaf(x, y, s, rot=0, col='#E8743B', key='ml'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i / 10 * TAU
        r = s if i % 2 == 0 else s * .45
        if i in (4, 6):
            r *= .75
        pts.append([math.cos(a) * r, math.sin(a) * r])
    paint(pts, wash=col, fill=mixCol(col, '#8E2E35', .4), fillOp=60, ink=INK, sw=.6)
    inkLine([[0, s * .2], [0, s * 1.0]], .6, '#6B4A35', 'ink', 0)
    pop()


def snowflakes(t, seed, n, x0, y0, x1, y1, r=6):
    tt = onTwos(t)
    for i in range(n):
        ph = frac(tt * (.12 + .12 * hash1(i + seed)) + hash1(seed + i * 4.1))
        x = lerp(x0, x1, hash1(seed + i * 2.9)) + math.sin(tt * 1.5 + i) * 26
        y = lerp(y0, y1, ph)
        rr = r * (.6 + .8 * hash1(i * 3 + seed))
        paint(ellPts(x, y, rr, rr, 10), wash='#FFFFFF', ink=None)


def snowman(x, y, s, n, t, key='sm', ages=None):
    """n = how many parts are on (0..4: base, body, head, flower+scarf). ages = seconds since each part landed"""
    ages = ages or [9] * 4
    parts = [(0, 1.6), (-2.5, 1.15), (-4.3, .8)]
    for i, (dy, r) in enumerate(parts):
        if i >= n:
            continue
        a = ages[i]
        sq = .18 * math.exp(-a * 9) * math.cos(a * 30)
        boilSeed(f'{key}{i}')
        cy = y + dy * s - r * s
        paint(ellPts(x, cy + r * s * sq * .5, r * s * (1 + sq * .6), r * s * (1 - sq), 30), wash='#FFFFFF', fill='#C9D6E3', fillOp=70, ink=INK, sw=1)
        if i == 2:
            for sgn in (-1, 1):
                paint(ellPts(x + sgn * .28 * s, cy - .12 * s, .08 * s, .1 * s, 8), wash=INK, ink=None)
            paint([[x, cy + .02 * s], [x + .6 * s, cy + .12 * s], [x, cy + .2 * s]], wash='#FF9E3D', ink=INK, sw=.6)
        if i == 1:
            for b in range(3):
                paint(ellPts(x, cy - .4 * s + b * .4 * s, .08 * s, .08 * s, 8), wash=INK, ink=None)
    if n >= 4:
        flowerAt(x - .45 * s, y - 5.8 * s, s * .55, 1.0)


# ---------------------------------------------------------------- night street
def sign(x, y, txt, s=1.0, key='sign', col='#B98552'):
    boilSeed(key)
    paint(rectPts(x - 8 * s, y - 160 * s, 16 * s, 160 * s), wash='#7F5A3A', ink=INK, sw=1)
    w = textW(txt, 54 * s) + 70 * s
    paint([[x - w / 2, y - 250 * s], [x + w / 2, y - 250 * s], [x + w / 2 + 30 * s, y - 205 * s], [x + w / 2, y - 160 * s], [x - w / 2, y - 160 * s]],
          wash=col, fill='#8E6A3E', fillOp=60, ink=INK, sw=1.2)
    text(txt, x + 10 * s, y - 205 * s, 54 * s, INK, shadow=False)


def lightning(x0, y0, x1, y1, key='lt', w=3.0, col='#FFFDE0'):
    boilSeed(key)
    pts = [[x0, y0]]
    n = 7
    for i in range(1, n):
        k = i / n
        pts.append([lerp(x0, x1, k) + jit(60), lerp(y0, y1, k)])
    pts.append([x1, y1])
    glow((x0 + x1) / 2, (y0 + y1) / 2, 380, '#E6E0FF', .8)
    inkLine(pts, w * 2.2, '#8E79BC', 'ink', 0)
    inkLine(pts, w, col, 'ink', 0)


def heldPhoto(x, y, w, rot, scene, key='hp'):
    polaroid(x, y, w, rot, 1, scene, key=key)


def seal(x, y, txt, size, col, age, rot=-.15):
    """rubber stamp imprint: slams down (scale 1.6 -> 1) with a ring"""
    if age < 0:
        return
    k = clamp(age / .1)
    s = lerp(1.6, 1.0, easeOut(k))
    push()
    translate(x, y)
    rotate(rot)
    scale(s)
    boilSeed(f'seal{txt}')
    w = textW(txt, size) + size * .7
    h = size * 1.45
    paint(rrPts(-w / 2, -h / 2, w, h, size * .2, 2), ink=col, sw=2.2)
    text(txt, 0, 0, size, col, shadow=False, a=.92)
    pop()


# ---------------------------------------------------------------- underwater
def seaBg(t, depth=0.0):
    gradRect(-80, -80, W + 160, H + 160, [mixCol('#4FA7D8', '#1D3E78', depth), mixCol('#1D3E78', '#0E1B44', depth)])
    tt = onTwos(t)
    for i in range(6):
        x = 200 + i * 320 + math.sin(tt * .7 + i) * 40
        flat([[x - 40, -80], [x + 40, -80], [x + 220, H + 80], [x + 60, H + 80]], '#BFE9FF', .07 * (1 - depth * .6))


def bubbles(t, seed, n, x0, y0, x1, y1, r=10, speed=.5):
    tt = onTwos(t)
    for i in range(n):
        ph = frac(tt * speed * (.6 + .6 * hash1(i + seed)) + hash1(seed * 7 + i * 1.3))
        x = lerp(x0, x1, hash1(seed + i * 3.7)) + math.sin(tt * 3 + i * 2) * 14
        y = lerp(y1, y0, ph)
        rr = r * (.5 + hash1(i * 5 + seed))
        bubble1(x, y, rr)


def bubble1(x, y, r, a=1.0):
    paint(ellPts(x, y, r, r, 14), wash='#DDF6FF', washOp=70 * a, ink='#E8F8FF', sw=max(.3, r / 30))
    paint(ellPts(x - r * .35, y - r * .35, r * .22, r * .16, 8), wash='#FFFFFF', washOp=220 * a, ink=None)


def fish(x, y, s, d=1, col='#F7C65C', key='fish'):
    push()
    translate(x, y)
    scale(d, 1)
    boilSeed(key)
    paint([[-s * .9, 0], [-s * 1.5, -s * .5], [-s * 1.4, 0], [-s * 1.5, s * .5]], wash=mixCol(col, '#E8743B', .3), ink=INK, sw=.6)
    paint(ellPts(0, 0, s, s * .55, 18), wash=col, ink=INK, sw=.7)
    paint(ellPts(s * .5, -s * .1, s * .1, s * .1, 8), wash=INK, ink=None)
    pop()


def seaweed(x, y, h, t, key='sw', col='#3FA37A'):
    tt = onTwos(t)
    pts = []
    for i in range(7):
        k = i / 6
        pts.append([x + math.sin(tt * 2 + k * 3 + x) * 30 * k, y - h * k])
    boilSeed(key)
    paint(ribbon(pts, h * .12, h * .03), wash=col, ink=INK, sw=.8)


def anglerfish(x, y, s, lit, key='af'):
    boilSeed(key)
    inkLine([[x + s * .3, y - s * .5], [x + s * .9, y - s * 1.3], [x + s * 1.4, y - s * 1.0]], 1.2, '#2B2233', 'ink', .6)
    glow(x + s * 1.4, y - s * .95, s * 2.2, '#FFF3B0', lit)
    paint(ellPts(x + s * 1.4, y - s * .95, s * .18, s * .18, 10), wash=mixCol('#8C8A70', '#FFF8C0', lit), ink=INK, sw=.6)
    paint(ellPts(x, y, s, s * .8, 24), wash='#4A4A78', fill='#2E2E55', fillOp=80, ink=INK, sw=1)
    paint(ellPts(x + s * .35, y - s * .25, s * .14, s * .14, 8), wash='#FFFFFF', ink=INK, sw=.5)
    for i in range(5):
        tx = x + s * (.1 + i * .17)
        paint([[tx, y + s * .2], [tx + s * .07, y + s * .38], [tx + s * .14, y + s * .2]], wash='#FFFFFF', ink=None)


# ---------------------------------------------------------------- masks / sky
def binoMask(cx, cy, r, gap, col=INK):
    p = skia.Path()
    p.setFillType(skia.PathFillType.kEvenOdd)
    p.addRect(skia.Rect.MakeXYWH(-200, -200, W + 400, H + 400))
    q = skia.Path()
    q.addCircle(cx - gap, cy, r)
    q2 = skia.Path()
    q2.addCircle(cx + gap, cy, r)
    u = skia.Op(q, q2, skia.PathOp.kUnion_PathOp)
    full = skia.Path()
    full.addRect(skia.Rect.MakeXYWH(-200, -200, W + 400, H + 400))
    m = skia.Op(full, u, skia.PathOp.kDifference_PathOp)
    G.c.drawPath(m, skia.Paint(AntiAlias=True, Color=skcol(col)))
    boilSeed('bino')
    paint(ellPts(cx - gap, cy, r, r, 48), ink=INK, sw=2.2)
    paint(ellPts(cx + gap, cy, r, r, 48), ink=INK, sw=2.2)


def moon(x, y, r, key='moon'):
    glow(x, y, r * 3.5, '#FFF3C4', .9)
    boilSeed(key)
    paint(ellPts(x, y, r, r, 32), wash='#FFF6D5', fill='#F2DFA0', fillOp=60, ink=INK, sw=1)
    for i, (dx, dy, rr) in enumerate([(-.3, -.2, .18), (.25, .3, .12), (.35, -.35, .08)]):
        paint(ellPts(x + dx * r, y + dy * r, rr * r, rr * r, 12), wash='#EBD592', ink=None)


def starsField(t, seed, n, x0, y0, x1, y1, r=5, col='#FFF5E2'):
    for i in range(n):
        x, y = lerp(x0, x1, hash1(seed + i * 1.9)), lerp(y0, y1, hash1(seed * 2 + i * 3.3))
        k = .6 + .4 * math.sin(onTwos(t) * 3 + i)
        sparkle(x, y, r * k * (.6 + hash1(i)), col, k)


def appleLight(x, y, r, on, key='al'):
    if on > .05:
        glow(x, y, r * 3, '#FF8A8A', on)
    apple(x, y, r, key=key, shine=0)
    if on < .9:
        paint(applePts(x, y, r), wash='#2A2440', washOp=170 * (1 - on), ink=None)


# ---------------------------------------------------------------- garden
def mound(x, y, s, key='mound'):
    boilSeed(key)
    pts = []
    for i in range(17):
        a = math.pi + i / 16 * math.pi
        pts.append([x + math.cos(a) * s * 2.6, y + math.sin(a) * s * .8])
    paint(pts, wash='#9B6B45', fill='#6B4A35', fillOp=70, ink=INK, sw=1)


def sprout(x, y, s, k, key='spr'):
    if k <= .02:
        return
    p = backOut(k)
    boilSeed(key)
    inkLine([[x, y], [x, y - s * 1.6 * p]], max(.8, s / 14), LEAF_DK, 'ink', 0)
    for sgn in (-1, 1):
        paint([[x, y - s * 1.5 * p], [x + sgn * s * 1.0 * p, y - s * 2.1 * p], [x + sgn * s * .25 * p, y - s * 1.2 * p]], wash=LEAF, ink=INK, sw=.7, curv=.5)


def appleTree(x, y, s, grow, napples, t, key='at', blossom=0.0, ages=None):
    """grow 0..1: trunk height and crown size; napples apples pop in (ages = seconds since each popped)"""
    g = clamp(grow)
    if g <= .01:
        return
    boilSeed(key)
    th = s * 6 * g
    paint([[x - s * .5 * g, y], [x + s * .5 * g, y], [x + s * .3 * g, y - th], [x - s * .3 * g, y - th]], wash='#9B6B45', fill='#6B4A35', fillOp=70, ink=INK, sw=1.1)
    for sgn in (-1, 1):
        inkLine([[x, y - th * .7], [x + sgn * s * 1.4 * g, y - th * 1.05]], max(1, s * .12 * g), '#7F5A3A', 'ink', .3)
    cr = s * 3.4 * g
    cy = y - th - cr * .45
    pts = []
    for i in range(36):
        a = i / 36 * TAU
        r = 1 + .13 * abs(math.sin(a * 4))
        pts.append([x + math.cos(a) * cr * 1.25 * r, cy + math.sin(a) * cr * .9 * r])
    paint(pts, wash=LEAF, fill=LEAF_DK, fillOp=80, ink=INK, sw=1.2, curv=.3)
    if blossom > 0:
        for i in range(12):
            bx = x + (hash1(i * 4.1) - .5) * cr * 2.0
            by = cy + (hash1(i * 6.3) - .5) * cr * 1.3
            bloom(bx, by, s * .28 * blossom, 1, '#FFFFFF', key=f'{key}b{i}', centre='#F59AB0', stem=False)
    ages = ages or [9] * napples
    spots = [(-.55, .05), (.5, -.15), (.05, .35), (-.2, -.4), (.7, .3), (-.8, -.25), (.3, -.5), (-.45, .45)]
    for i in range(min(napples, len(spots))):
        a = ages[i]
        k = backOut(clamp(a / .14))
        ax, ay = x + spots[i][0] * cr * 1.15, cy + spots[i][1] * cr * .9
        apple(ax, ay, s * .42 * k + .1, key=f'{key}a{i}', shine=max(0, 1 - a * 3))


def wateringCanHook(tilt=0.0):
    def h(u, sw):
        push()
        rotate(tilt)
        boilSeed('wcan')
        paint(rrPts(0, -1.4 * u, 2.6 * u, 2.0 * u, .4 * u), wash='#7FB8E6', ink=INK, sw=sw * .8)
        paint([[2.5 * u, -.8 * u], [4.2 * u, -2.0 * u], [4.4 * u, -1.7 * u], [2.6 * u, -.3 * u]], wash='#7FB8E6', ink=INK, sw=sw * .7)
        inkLine([[.3 * u, -1.4 * u], [1.3 * u, -2.6 * u], [2.3 * u, -1.4 * u]], sw * 1.2, INK, 'ink', .6)
        pop()
    return h


def shovelHook(dig=0.0):
    def h(u, sw):
        push()
        rotate(.9 + dig)
        boilSeed('shovel')
        inkLine([[0, 0], [4.2 * u, 0]], sw * 1.6, '#9B6B45', 'ink', 0)
        paint([[4.0 * u, -.8 * u], [5.6 * u, -.6 * u], [6.0 * u, 0], [5.6 * u, .6 * u], [4.0 * u, .8 * u]], wash='#B9C2CC', ink=INK, sw=sw * .7)
        pop()
    return h


def detectiveHatAlone(x, y, u, rot=0.0):
    push()
    translate(x, y)
    rotate(rot)
    translate(0, 9 * u)
    hat(u, 'deer', clamp(u / 15, .45, 2.4))
    pop()
