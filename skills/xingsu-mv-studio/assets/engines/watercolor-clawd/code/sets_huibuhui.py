# sets_h.py: sets and props for 《会不会》 (autumn: ginkgo gold, a white daisy that is HER flower).
# Logical canvas 1920x1080. Present = dusk orange / night indigo; memory = warm gold; breakup memory = cold grey.
import math
from eng import *
import eng
import clawd as CL
from clawd import *
from props import *
from props_bingbian import P2, xmark, starsField
from hl import tint, desat, memoryGrade, deskLamp, mug, curtain, windowFrame, WENKAI, rain as rainH, ripples, stars, caption
from hl import vignette as softVig
from sets2 import bookshelf, photoString, wallClock, wallCalendar, fairyLights, parkBench, seat, bigTreeSide, shopFront2, SHOPS
from sets import heartBalloon
from props import lamp as streetLamp

GK = dict(leaf='#F2C14E', dk='#C98A1E', lt='#FBE08A', brown='#B97A2A', orange='#E8A33A')
DAISY, DAISY_DK, DAISY_C, DAISY_CDK = '#FFFDF6', '#D9D2C2', '#F2B63A', '#D9902A'
STEM = '#5E9E5A'
GOLD_TXT = '#F5C04A'      # 会
GREY_TXT = '#9DB2D6'      # 不会
RED = '#D8394E'


# ================================================================ small geometry
def rell(cx, cy, rx, ry, ang, n=16):
    ca, sa = math.cos(ang), math.sin(ang)
    out = []
    for i in range(n):
        a = i / n * TAU
        ex, ey = math.cos(a) * rx, math.sin(a) * ry
        out.append([cx + ex * ca - ey * sa, cy + ex * sa + ey * ca])
    return out


def handPos(x, y, u, o, side='R'):
    """world position of the end of a Clawd arm (front / q view), from the same numbers clawd() uses"""
    V = CL.VIEWS.get(o.get('view') or 'front')
    spec = [a for a in V['arms'] if a[2] == side]
    if not spec:
        return x, y - 4.5 * u
    px, dr, which, layer = spec[0]
    a = o.get('aL' if side == 'L' else 'aR', .2)
    if a is None:
        a = .2
    sq = (o.get('sq') or 0)
    fl = -1 if o.get('flip') else 1
    bx = x + (o.get('dx') or 0) * u
    by = y + (o.get('dy') or 0) * u
    ox = (px + dr * .55 * clamp((abs(a) - .7) / .9)) * u
    oy = -4.5 * u
    if dr == 0:
        return bx + fl * ox, by + oy
    ang = a if dr < 0 else -a
    ex = ox + dr * 2.2 * u * math.cos(ang)
    ey = oy + 2.2 * u * math.sin(ang) * (1 if dr > 0 else -1)
    return bx + fl * ex * (1 + sq * .6), by + ey * (1 - sq)


# ================================================================ ginkgo
def ginkgoLeaf(x, y, s, rot=0.0, col=None, key='gl', lite=False, a=1.0, ink=True, veins=True):
    """fan-shaped ginkgo leaf; (x, y) = end of the stalk, the fan opens 'up' (rot turns it around the stalk end); s = fan radius"""
    if a <= .01 or s < 1:
        return
    col = col or GK['leaf']
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    base = -.42 * s
    P = [[0, base]]
    for i in range(19):
        ang = math.radians(-152 + i * 124 / 18)
        rr = s * (1 - .18 * math.exp(-((i - 9) / 1.3) ** 2)) * (1 + .025 * math.sin(i * 2.3))
        P.append([math.cos(ang) * rr, base + math.sin(ang) * rr * .9])
    paint(P, wash=col, washOp=int(255 * a), fill=mixCol(col, GK['dk'], .55), fillOp=int(80 * a), bleed=.12,
          ink=(INK if ink else None), sw=clamp(s / 60, .35, 1.0), lite=lite)
    if veins and s > 14:
        pa = skia.Paint(AntiAlias=True, Color=skcol(mixCol(col, GK['dk'], .7), .45 * a), StrokeWidth=max(.8, s * .018))
        for i in range(9):
            ang = math.radians(-146 + i * 112 / 8)
            G.c.drawLine(0, base, math.cos(ang) * s * .86, base + math.sin(ang) * s * .8, pa)
    G.c.drawLine(0, base, 0, 0, skia.Paint(AntiAlias=True, Color=skcol(mixCol(GK['brown'], INK, .3), a), StrokeWidth=max(1.2, s * .05)))
    pop()


def leafCol(i):
    return mixCol(GK['leaf'], [GK['lt'], GK['dk'], GK['orange'], GK['leaf']][i % 4], .45)


def leafFall(t, seed, n, x0, y0, x1, y1, s=18, fall=110, a=1.0, sway=50, wind=0.0, lite=True, ink=True, shift=0.0):
    """drifting ginkgo leaves; positions only from t"""
    for i in range(n):
        h1, h2, h3 = hash1(seed + i * 3.7), hash1(seed * 1.3 + i * 5.1), hash1(seed * 2.1 + i * 1.7)
        span = (y1 - y0) + 200
        yy = y0 - 100 + (h2 * span + t * fall * (.6 + .6 * h3)) % span
        xx = lerp(x0, x1, h1) + math.sin(t * (.8 + h3) + i) * sway + t * wind * (.5 + h3) + shift * (.6 + .6 * h3)
        xx = x0 + (xx - x0) % max(1, (x1 - x0))
        rot = math.sin(t * (1.4 + h1) + i * 1.7) * 1.2 + i
        ginkgoLeaf(xx, yy, s * (.7 + .5 * h2), rot, leafCol(i), key=f'lf{seed}_{i}', lite=lite, a=a, ink=ink, veins=False)


def leafCarpet(x0, y0, x1, y1, n, seed=3, s=14, a=1.0, persp=True):
    """leaves lying on the ground (static)"""
    for i in range(n):
        h1, h2, h3 = hash1(seed + i * 2.9), hash1(seed * 1.7 + i * 4.3), hash1(seed * 3.1 + i * 1.3)
        yy = lerp(y0, y1, h2 ** (.7 if persp else 1))
        sc = lerp(.6, 1.4, (yy - y0) / max(1, y1 - y0)) if persp else 1
        ginkgoLeaf(lerp(x0, x1, h1), yy, s * sc * (.7 + .5 * h3), h3 * TAU, leafCol(i), key=f'lc{seed}_{i}', lite=True, a=a, ink=False, veins=False)


def ginkgoTree(x, y, s, t, key='gt', night=0.0, memory=0.0):
    bigTreeSide(x, y, s, t, key=key, col=mixCol(mixCol(GK['leaf'], '#F7D36E', memory * .3), '#5A5A8A', night * .55),
                dk=mixCol(GK['dk'], '#3A3A6A', night * .55), night=0.0)


# ================================================================ the daisy (her flower)
DAISY_ORDER = [0, 6, 3, 9, 1, 7, 4, 10, 2, 8, 5, 11]


def daisyHead(x, y, r, gone=0, rot=0.0, key='dz', n=12, tilt=1.0, a=1.0, lite=None, col=DAISY):
    """flower head centred at (x, y); r = petal-tip radius; `gone` petals (in DAISY_ORDER) already plucked"""
    if r < 1:
        return
    goneSet = set(DAISY_ORDER[:int(gone)]) if n == 12 else set(range(int(gone)))
    lite = (r < 50) if lite is None else lite
    sw = clamp(r / 90, .35, 1.3)
    for i in range(n):
        if i in goneSet:
            continue
        ang = rot + i / n * TAU
        cx, cy = x + math.cos(ang) * r * .58, y + math.sin(ang) * r * .58 * tilt
        boilSeed(f'{key}p{i}')
        aa = math.atan2(math.sin(ang) * tilt, math.cos(ang))
        paint(rell(cx, cy, r * .43, r * .15 * (.75 + .25 * tilt), aa, 14), wash=col, washOp=int(255 * a), fill=DAISY_DK, fillOp=int(55 * a),
              ink=INK, sw=sw * .7, lite=lite)
    boilSeed(key + 'c')
    paint(ellPts(x, y, r * .26, r * .26 * (.55 + .45 * tilt), 16), wash=DAISY_C, fill=DAISY_CDK, fillOp=90, ink=INK, sw=sw * .8, lite=lite)
    if r > 30:
        for j in range(7):
            aj = j / 7 * TAU + .4
            G.c.drawCircle(x + math.cos(aj) * r * .13, y + math.sin(aj) * r * .13 * tilt, max(1, r * .025),
                           skia.Paint(AntiAlias=True, Color=skcol(DAISY_CDK, .8)))


def daisyStem(x, y, L, bend=0.0, w=3.0, key='ds', leaf=True):
    """stem from the head (x, y) going down L px (bend = horizontal offset of the bottom)"""
    boilSeed(key)
    pts = [[x, y], [x + bend * .35, y + L * .5], [x + bend, y + L]]
    inkLine(pts, w / 2.2, STEM, 'ink', .5)
    if leaf and L > 60:
        lx, ly = x + bend * .4, y + L * .55
        paint(rell(lx + 16, ly - 6, 22, 7, -.5, 12), wash='#7FB86A', ink=INK, sw=.5, lite=True)


def daisy(x, y, r, L, gone=0, rot=0.0, bend=0.0, key='dzf', tilt=1.0):
    daisyStem(x, y, L, bend, max(2.5, r / 14), key=key + 's')
    daisyHead(x, y, r, gone, rot, key=key, tilt=tilt)


def hairDaisy(fx, fy, u, sw, k=1.0):
    """replaces clawd.flowerAt: her hair flower is a small daisy"""
    inkLine([[fx, fy], [fx + .3 * u, fy + .7 * u]], sw * .6, STEM, 'ink', 0)
    daisyHead(fx, fy, 1.35 * u * k, 0, .2, key='hair', lite=True)


CL.flowerAt = hairDaisy


def petalShape(x, y, r, ang, key='pt', a=1.0):
    boilSeed(key)
    paint(rell(x, y, r * .43, r * .15, ang, 14), wash=DAISY, washOp=int(255 * a), fill=DAISY_DK, fillOp=int(50 * a), ink=INK,
          sw=clamp(r / 90, .35, 1.3) * .7, lite=True)


def pluck(t, tb, x, y, r, idx, dirx=1, label=None, lx=None, ly=None, lsize=96, lcol=None, key='pk', rot=0.0, dist=620, life=1.3,
          head_from_t=None):
    """petal `idx` (index into DAISY_ORDER) leaves the head at beat tb, flies off with a spin; its label stamps in"""
    age = t - tb
    if age < 0:
        return
    i = DAISY_ORDER[idx]
    ang = rot + i / 12 * TAU
    sx, sy = x + math.cos(ang) * r * .58, y + math.sin(ang) * r * .58
    k = easeOut(clamp(age / .7))
    px = sx + dirx * dist * k + 30 * math.sin(age * 7) * (1 - k)
    py = sy - 220 * math.sin(clamp(age / .7) * math.pi * .7) + 500 * max(0, age - .45) ** 2
    if age < life:
        petalShape(px, py, r * (1 - .25 * k), ang + age * 9 * dirx, key=f'{key}{idx}', a=1 - seg(age, life - .3, life))
    if label:
        lx = lx if lx is not None else sx + dirx * 160
        ly = ly if ly is not None else sy - 170
        col = lcol or (GOLD_TXT if label == '会' else GREY_TXT)
        stamp(label, lx, ly, lsize, col, age, rot=(-.12 if dirx > 0 else .12), life=.95)


# ================================================================ title leaves (opening and ending)
def titleLeaf(t, tb, x, y, s, ch, rot, col, key, fall=520, tcol=INK):
    """a leaf that lands at (x, y) on beat tb, with a character brushed on it"""
    age = t - tb
    if age < -.42:
        return
    if age < 0:
        k = 1 - (-age / .42)
        k2 = easeIn(k)
        lx = x + 140 * math.sin((1 - k) * 4.2) * (1 - k)
        ly = y - fall * (1 - k2)
        r_ = rot + (1 - k) * 2.2
        sq = 1
    else:
        lx, ly = x, y
        r_ = rot + .06 * math.sin(age * 18) * math.exp(-age * 6)
        sq = 1 - .08 * math.exp(-age * 9) * math.cos(age * 30)
    push()
    translate(lx, ly)
    scale(1, sq)
    translate(-lx, -ly)
    ginkgoLeaf(lx, ly, s, r_, col, key=key)
    push()
    translate(lx, ly)
    rotate(r_)
    text(ch, 0, -s * .9, s * .5, tcol, face=WENKAI, shadow=False)
    pop()
    pop()


# ================================================================ glass bottle, pots, desk things
def bottle(x, y, s, key='btl', light='#FFE3B0'):
    """small glass bottle standing on (x, y); returns the neck top point"""
    boilSeed(key)
    bw, bh, nw, nh = 1.15 * s, 1.55 * s, .46 * s, .8 * s
    P = rrPts(x - bw / 2, y - bh, bw, bh, .3 * s) + []
    paint(P, wash='#CFE6EA', washOp=120, ink=INK, sw=.8, lite=True)
    paint(rectPts(x - bw / 2 + 6, y - bh * .55, bw - 12, bh * .55 - 6), wash='#BFE0E8', washOp=110, ink=None, lite=True)
    paint(rectPts(x - nw / 2, y - bh - nh, nw, nh + 6), wash='#D8EEF1', washOp=130, ink=INK, sw=.7, lite=True)
    G.c.drawLine(x - bw / 2 + 10, y - bh + 12, x - bw / 2 + 10, y - 20, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .7), StrokeWidth=max(2, s * .06)))
    glow(x, y - bh * .5, s * 1.2, light, .25)
    return x, y - bh - nh


def daisyPot(x, y, s, t, heads=((-.55, -2.6, .0), (.35, -3.1, .4), (.85, -2.2, 1.1)), gone=None, key='dpot', hide=()):
    """terracotta pot of daisies standing on (x, y); s = pot height. returns head positions"""
    boilSeed(key)
    paint([[x - .62 * s, y - s], [x + .62 * s, y - s], [x + .48 * s, y], [x - .48 * s, y]], wash='#C9774E', fill='#9A5434', fillOp=60, ink=INK, sw=.8, lite=True)
    paint(rectPts(x - .7 * s, y - s - .22 * s, 1.4 * s, .26 * s), wash='#D98A5E', ink=INK, sw=.7, lite=True)
    out = []
    for j, (hx, hy, ph) in enumerate(heads):
        if j in hide:
            out.append(None)
            continue
        sway = math.sin(t * 1.3 + ph) * .06 * s
        X, Y = x + hx * s * .6 + sway, y + hy * s * .55 - .2 * s
        daisyStem(X, Y, (y - s) - Y + 6, x + hx * s * .25 - X, 2.2, key=f'{key}s{j}', leaf=j == 1)
        daisyHead(X, Y, .42 * s, (gone[j] if gone else 0), ph, key=f'{key}h{j}', lite=True)
        out.append((X, Y))
    return out


def battery(x, y, s, level, blink=0.0, a=1.0):
    """battery icon centred at (x, y); level 0..3 bars"""
    boilSeed('bat')
    w, h = 2.0 * s, 1.0 * s
    paint(rrPts(x - w / 2, y - h / 2, w, h, .18 * s), wash='#FFFDF6', washOp=int(235 * a), ink=INK, sw=1.0)
    paint(rectPts(x + w / 2, y - h * .22, .18 * s, h * .44), wash=INK, ink=None)
    cols = {3: '#7CC36B', 2: '#F2C14E', 1: '#E8574E', 0: '#E8574E'}
    on = 1 - blink
    for i in range(int(level)):
        bx = x - w / 2 + .14 * s + i * (w - .28 * s) / 3
        paint(rectPts(bx + 3, y - h / 2 + .14 * s, (w - .28 * s) / 3 - 8, h - .28 * s), wash=cols[int(level)], washOp=int(255 * a * on), ink=None)
    if level == 0 and blink > 0:
        text('!', x, y, s * .8, '#E8574E', a=a * blink, shadow=False)


def pedSignal(x, y, s, state, key='psg', glowK=1.0, wet=0.0):
    """pedestrian signal on a pole; (x, y) = pole foot; state 'red' / 'green'"""
    boilSeed(key)
    paint(rectPts(x - .09 * s, y - 5.2 * s, .18 * s, 5.2 * s), wash='#5A5A70', ink=INK, sw=.8, lite=True)
    bx, by = x - .55 * s, y - 7.6 * s
    paint(rrPts(bx, by, 1.1 * s, 2.4 * s, .14 * s), wash='#2A2A38', ink=INK, sw=.9)
    for j, (st, col, cy) in enumerate((('red', '#FF4A4A', by + .62 * s), ('green', '#3CE08A', by + 1.78 * s))):
        lit = state == st
        paint(rrPts(x - .42 * s, cy - .48 * s, .84 * s, .96 * s, .1 * s), wash=col if lit else '#3A3A4A', washOp=255 if lit else 255, ink=None)
        pc = '#FFFFFF' if lit else '#55556A'
        # pictogram
        G.c.drawCircle(x, cy - .26 * s, .09 * s, skia.Paint(AntiAlias=True, Color=skcol(pc)))
        pa = skia.Paint(AntiAlias=True, Color=skcol(pc), StrokeWidth=.07 * s, StrokeCap=skia.Paint.kRound_Cap, Style=skia.Paint.kStroke_Style)
        if st == 'red':
            G.c.drawLine(x, cy - .16 * s, x, cy + .14 * s, pa)
            G.c.drawLine(x - .12 * s, cy - .08 * s, x + .12 * s, cy - .08 * s, pa)
            G.c.drawLine(x, cy + .14 * s, x - .07 * s, cy + .34 * s, pa)
            G.c.drawLine(x, cy + .14 * s, x + .07 * s, cy + .34 * s, pa)
        else:
            G.c.drawLine(x + .02 * s, cy - .16 * s, x - .03 * s, cy + .12 * s, pa)
            G.c.drawLine(x - .03 * s, cy + .12 * s, x - .16 * s, cy + .34 * s, pa)
            G.c.drawLine(x - .03 * s, cy + .12 * s, x + .14 * s, cy + .3 * s, pa)
            G.c.drawLine(x - .12 * s, cy - .02 * s, x + .14 * s, cy - .1 * s, pa)
        if lit and glowK > 0:
            glow(x, cy, 2.2 * s, col, .8 * glowK)
    if wet > 0 and state:
        col = '#FF4A4A' if state == 'red' else '#3CE08A'
        sh = skia.GradientShader.MakeLinear([skia.Point(0, y + 10), skia.Point(0, y + 4 * s)], [skcol(col, .35 * wet), skcol(col, 0)])
        G.c.drawRect(skia.Rect.MakeXYWH(x - .5 * s, y + 10, s, 4 * s), skia.Paint(Shader=sh))
    return bx, by


def scissors(x, y, s, ang, open_, key='sc', col='#C8564F'):
    """scissors with the pivot at (x, y), blades pointing along ang; open_ 0..1"""
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    da = .32 * open_
    for sgn in (-1, 1):
        push()
        rotate(sgn * da)
        paint([[0, -.07 * s * sgn], [1.25 * s, 0], [0, .09 * s * sgn]], wash='#D7DCE6', fill='#9AA3B5', fillOp=80, ink=INK, sw=.7)
        paint(rell(-.55 * s, .2 * s * sgn, .3 * s, .2 * s, .2 * sgn, 16), wash=col, ink=INK, sw=.7)
        paint(rell(-.55 * s, .2 * s * sgn, .17 * s, .09 * s, .2 * sgn, 14), wash=PAL['paper'], ink=None)
        pop()
    G.c.drawCircle(0, 0, .06 * s, skia.Paint(AntiAlias=True, Color=skcol(INK)))
    pop()


def car(x, y, s, col='#5B7FC4', key='car', night=1.0, flip=False):
    """little side-view car, (x, y) = bottom centre, about 4s long"""
    push()
    translate(x, y)
    if flip:
        scale(-1, 1)
    boilSeed(key)
    paint([[-2 * s, -.35 * s], [-2 * s, -1.0 * s], [-1.1 * s, -1.1 * s], [-.7 * s, -1.75 * s], [.8 * s, -1.75 * s], [1.3 * s, -1.1 * s],
           [2.05 * s, -.95 * s], [2.05 * s, -.35 * s]], wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=1.0, curv=.15)
    paint([[-.55 * s, -1.12 * s], [-.35 * s, -1.6 * s], [.25 * s, -1.6 * s], [.25 * s, -1.12 * s]], wash='#BFE0F0', ink=INK, sw=.6, lite=True)
    paint([[.4 * s, -1.12 * s], [.4 * s, -1.6 * s], [.72 * s, -1.6 * s], [1.05 * s, -1.12 * s]], wash='#BFE0F0', ink=INK, sw=.6, lite=True)
    for wx in (-1.2 * s, 1.25 * s):
        paint(ellPts(wx, -.35 * s, .42 * s, .42 * s, 16), wash='#2A2438', ink=INK, sw=.8)
        G.c.drawCircle(wx, -.35 * s, .16 * s, skia.Paint(AntiAlias=True, Color=skcol('#9AA3B5')))
    paint(ellPts(1.95 * s, -.78 * s, .12 * s, .1 * s, 10), wash='#FFF3B0', ink=None)
    if night > 0:
        p = [[2.0 * s, -.78 * s], [5.5 * s, -1.3 * s], [5.5 * s, -.1 * s]]
        flat(p, '#FFF3B0', .18 * night)
    pop()


def splashDrops(x, y, age, n=14, s=1.0, col='#BFD3EE', key='spd'):
    if not (0 <= age < .7):
        return
    for i in range(n):
        h1, h2 = hash1(i * 3.1 + 2), hash1(i * 7.3 + 5)
        ang = -math.pi * (.15 + .7 * h1)
        v = (500 + 700 * h2) * s
        px = x + math.cos(ang) * v * age
        py = y + math.sin(ang) * v * age + 1400 * age * age
        r = (10 + 12 * h2) * s * (1 - age / .7)
        boilSeed(f'{key}{i}')
        paint(ellPts(px, py, r, r * 1.2, 10), wash=col, washOp=220, ink=INK, sw=.5, lite=True)


def tearDrop(x, y, s, a=1.0, key='td'):
    boilSeed(key)
    paint([[x, y - 1.3 * s], [x + .75 * s, y + .1 * s], [x, y + .85 * s], [x - .75 * s, y + .1 * s]], wash=PAL['sky'], washOp=int(235 * a), ink=INK, sw=.7, curv=.7)
    paint(ellPts(x - .25 * s, y - .1 * s, .18 * s, .26 * s, 8), wash='#FFFFFF', washOp=int(200 * a), ink=None)


# ================================================================ windows and rooms
SKY = dict(dusk=('#F2A464', '#F9D59A'), night=('#1E2457', '#3A3F7E'), day=('#9FD0EE', '#F3E6C8'), gold=('#F7C77A', '#FBE6B8'))


def autumnView(x, y, w, h, t, mode='dusk', key='av', leaves=True, moonXY=None):
    """what is seen through a window: sky, roofs, ginkgo crowns, a few drifting leaves (clipped to the opening)"""
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(x, y, w, h))
    s1, s2 = SKY[mode]
    gradRect(x, y, w, h, [s1, s2])
    night = 1.0 if mode == 'night' else 0.0
    if mode == 'dusk':
        glow(x + w * .3, y + h * .78, w * .45, '#FFE2A0', .8)
        boilSeed(key + 'sun')
        paint(ellPts(x + w * .3, y + h * .78, 46, 46, 22), wash='#FFF3D2', ink=None)
    if night:
        stars(t, 17, 30, x, y, x + w, y + h * .55, 1.0, 2.4)
        mx, my = moonXY or (x + w * .76, y + h * .22)
        glow(mx, my, 140, '#E8E4FF', .5)
        boilSeed(key + 'm')
        paint(ellPts(mx, my, 30, 30, 22), wash='#FFF8E4', ink=None)
    # roofs
    rx = x - 20
    i = 0
    while rx < x + w + 20:
        boilSeed(f'{key}r{i}')
        bw = 90 + 70 * hash1(i * 3.3)
        bh = 80 + 90 * hash1(i * 5.1)
        top = y + h - bh
        col = mixCol(mixCol('#9A6E6A', '#2C2F66', night), s1, .35)
        paint([[rx, y + h + 10], [rx, top + 20], [rx + bw / 2, top - 10], [rx + bw, top + 20], [rx + bw, y + h + 10]], wash=col, ink=INK, sw=.6, lite=True)
        for r_ in range(2):
            on = hash1(i * 13 + r_) < (.7 if night else .25)
            flatRect(rx + bw * .3, top + 40 + r_ * 34, 16, 20, '#FFD98A' if on else mixCol(col, INK, .2), .9)
        rx += bw + 10
        i += 1
    # ginkgo crowns at both sides of the window
    for j, (cx, cy, r) in enumerate([(x + 40, y + h * .35, 170), (x + w - 30, y + h * .28, 190), (x + w * .5, y - 40, 120)]):
        boilSeed(f'{key}c{j}')
        P = []
        for k in range(30):
            a = k / 30 * TAU
            rr = r * (1 + .14 * abs(math.sin(a * 3.5 + j))) + 5 * math.sin(t * 1.2 + k)
            P.append([cx + math.cos(a) * rr, cy + math.sin(a) * rr * .8])
        paint(P, wash=mixCol(GK['leaf'], '#4A4A80', night * .6), fill=mixCol(GK['dk'], '#2A2A5A', night * .6), fillOp=80, ink=INK, sw=.7, curv=.3, lite=True)
    if leaves:
        leafFall(t, 7 + len(key), 6, x, y, x + w, y + h, s=12, fall=90, a=1.0 - .3 * night, sway=40, wind=30)
    G.c.restore()


WALLS = {('him', 'dusk'): ('#7C5E6E', '#A27C72'), ('her', 'dusk'): ('#82607E', '#A88090'),
         ('her', 'night'): ('#2B3168', '#3E4482'), ('him', 'night'): ('#22394F', '#355068')}


def roomBackH(t, who='him', mode='dusk', curtainSway=0.0, window=(600, 70, 720, 430), extraBack=None):
    """front-facing room behind the sitter (his = mirror of hers)"""
    mirror = who == 'him'
    c1, c2 = WALLS[(who, mode)]
    gradRect(-400, -400, W + 800, H + 800, [c1, c2])
    for i in range(-6, 40):
        G.c.drawRect(skia.Rect.MakeXYWH(i * 56, -400, 22, 1100), skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .025)))
    flatRect(-400, 600, W + 800, 200, mixCol(c2, INK, .25))
    G.c.drawLine(-400, 600, W + 400, 600, skia.Paint(AntiAlias=True, Color=skcol(mixCol(c2, '#FFFFFF', .2), .6), StrokeWidth=4))
    push()
    if mirror:
        translate(W, 0)
        scale(-1, 1)
    wx, wy, ww, wh = window
    autumnView(wx, wy, ww, wh, t, mode, key='wb' + who)
    windowFrame(wx, wy, ww, wh, '#6B4A3E' if not mirror else '#5A4A42', key='wbf' + who)
    if mode == 'dusk':
        flat([[wx, wy + wh], [wx + ww, wy + wh], [wx + ww + 260, 1100], [wx - 160, 1100]], '#FFD9A0', .10)
    curtain(wx - 40, wy - 30, wh + 90, -1, curtainSway, '#C98A6A' if not mirror else '#8C9A7A', key='cl' + who)
    curtain(wx + ww + 40, wy - 30, wh + 90, 1, curtainSway, '#C98A6A' if not mirror else '#8C9A7A', key='cr' + who)
    fairyLights(t, wx - 60, wx + ww + 60, wy - 46, 34, 16, key='fl' + who, a=.8 if mode == 'dusk' else 1.0)
    bookshelf(70, 150, 360, 450, key='bs' + who, who=who)
    photoString(t, 1440, 1840, 170, who, key='ps' + who)
    wallClock(1520, 330, 46, t, key='clk' + who)
    if extraBack:
        extraBack()
    pop()
    wallCalendar(1680 if not mirror else W - 1680 - 190, 300, key='cal' + who)
    boilSeed('chb' + who)
    paint(rrPts(800, 560, 320, 230, 30), wash='#6B4A3E', fill='#4A2E22', fillOp=60, ink=INK, sw=1.0, lite=True)
    paint(rrPts(830, 590, 260, 170, 20), wash='#86593F', ink=INK, sw=.7, lite=True)


DESK_Y = 760
U_ROOM = 46
SIT_Y = DESK_Y + 102


def deskTopH(t, who='him', lampK=1.0, bottleDaisy=None, pot=None, polaroidK=0.0, papers=False, mugSteam=1.0, leafOn=True, after=None,
             inBottle=None):
    """the desk in the foreground (drawn after the sitter). bottleDaisy = gone-count or None (bottle empty / absent)"""
    y = DESK_Y
    boilSeed('dsk' + who)
    paint([[-100, y], [W + 100, y], [W + 100, y + 46], [-100, y + 46]], wash='#B98A60', fill='#8A5A3C', fillOp=50, ink=INK, sw=1.0)
    gradRect(-100, y + 46, W + 200, 400, ['#8A5A3C', '#5A3828'])
    inkLine([[-100, y + 46], [W + 100, y + 46]], 1.0, INK, 'ink', 0)
    for k in range(3):
        dx = 120 + k * 620
        paint(rectPts(dx, y + 80, 480, 120), wash='#7A5038', ink=INK, sw=.8, lite=True)
        paint(rrPts(dx + 210, y + 128, 60, 16, 8), wash='#D9B45A', ink=INK, sw=.6, lite=True)
    lampX = 1760 if who == 'him' else 160
    if lampK > 0:
        sh = skia.GradientShader.MakeRadial(skia.Point(lampX - (380 if who == 'him' else -380), y + 20), 560, [skcol('#FFD48A', .32 * lampK), skcol('#FFD48A', 0)])
        G.c.drawRect(skia.Rect.MakeXYWH(-100, y - 10, W + 200, 70), skia.Paint(Shader=sh))
    # book stack on the lamp side's opposite end
    bx0 = 1500 if who == 'him' else 1430
    for i, (bw, col) in enumerate([(230, '#5B7FC4'), (210, '#C8564F'), (220, '#E8B04A')]):
        boilSeed(f'stk{who}{i}')
        paint(rectPts(bx0 + i * 6 - 120, y + 24 - (i + 1) * 30, bw, 30), wash=col, ink=INK, sw=.7, lite=True)
    if papers:
        for i in range(5):
            boilSeed(f'ppr{i}')
            paint(rectPts(1180 + i * 4 - 20 * (i % 2), y + 18 - i * 10, 230, 14), wash='#FFFDF6', ink=INK, sw=.5, lite=True)
    if leafOn:
        ginkgoLeaf(1240 if who == 'him' else 700, y + 30, 34, 1.9, GK['leaf'], key='dleaf' + who)
    if polaroidK > 0:
        push()
        translate(1250 if who == 'him' else 670, y + 22)
        rotate(-.08)
        boilSeed('dpol' + who)
        paint([[-70, 0], [70, 0], [62, -26], [-62, -26]], wash='#FFFDF6', ink=INK, sw=.6, lite=True)
        pop()
    mx = 1330 if who == 'him' else 1290
    mug(mx, y + 22, .85, key='mg' + who, steam=mugSteam, t=t)
    deskLamp(lampX, y + 26, 1.3, lampK, key='lp' + who, flip=(who == 'him'))
    neck = None
    if bottleDaisy is not None:
        if inBottle:
            inBottle(560, y + 30 - 2.35 * 46)
        neck = bottle(560, y + 30, 46, key='btl' + who)
    potHeads = None
    if pot is not None:
        potHeads = daisyPot(560 if who == 'her' else 1360, y + 30, 92, t, gone=pot.get('gone'), hide=pot.get('hide', ()), key='dpot' + who)
    if after:
        after()
    return neck, potHeads


# ================================================================ outdoor sets
def ginkgoAvenue(t, mode='gold', key='ga', horizon=600, wind=0.0, leavesK=1.0, trees=True, lamps=True, shift=0.0):
    """golden ginkgo avenue in perspective: sky, far trees, path with leaf carpet, big trees both sides"""
    skies = dict(gold=('#F6C97E', '#FCEBC6'), dusk=('#E99A6A', '#F7CF9C'), memory=('#EBC98E', '#F7E7C4'), bright=('#9FD3F0', '#FCEBC6'))
    s1, s2 = skies[mode]
    gradRect(-400, -400, W + 800, horizon + 400, [s1, s2])
    glow(960, horizon - 40, 900, '#FFF2C8', .55)
    if mode in ('gold', 'bright'):
        puff(380, 160, 34, '#FFF8EA', key=key + 'pf1', a=.9)
        puff(1500, 120, 26, '#FFF8EA', key=key + 'pf2', a=.9)
    # far tree line
    for i in range(14):
        boilSeed(f'{key}far{i}')
        fx = -60 + i * 150
        r = 80 + 30 * hash1(i * 2.3)
        paint(ellPts(fx, horizon - 40, r, r * .75, 18), wash=mixCol(GK['leaf'], s2, .35), ink=INK, sw=.5, lite=True)
    flatRect(-400, horizon, W + 800, H - horizon + 400, '#D9B784')
    # path (perspective)
    vx = 960
    paint([[vx - 70, horizon], [vx + 70, horizon], [vx + 1100, H + 60], [vx - 1100, H + 60]], wash='#E9DCC4', ink=INK, sw=.8)
    for i in range(10):
        yy = horizon + (H - horizon) * (i / 10) ** 1.6
        hw = lerp(70, 1100, (yy - horizon) / (H - horizon))
        G.c.drawLine(vx - hw, yy, vx + hw, yy, skia.Paint(AntiAlias=True, Color=skcol('#C9B898', .5), StrokeWidth=2))
    leafCarpet(-200, horizon + 10, W + 200, H + 40, 70, seed=len(key) + 3, s=16)
    if lamps:
        for s_ in (-1, 1):
            for j, d in enumerate((.35, .75)):
                lx = vx + s_ * lerp(120, 900, d)
                ly = horizon + (H - horizon) * d ** 1.1
                streetLamp(lx, ly, lerp(14, 40, d), 1.0 if mode == 'dusk' else 0.0, key=f'{key}lm{s_}{j}')
    if trees:
        for j, (tx, ty, ts) in enumerate([(200, horizon + 70, 60), (1720, horizon + 70, 60), (-60, H + 30, 150), (1990, H + 30, 150)]):
            ginkgoTree(tx, ty, ts, t, key=f'{key}t{j}', memory=1.0 if mode == 'memory' else 0.0)
    if leavesK > 0:
        leafFall(t, len(key) * 7 + 1, int(22 * leavesK), -100, -100, W + 100, H, s=16, fall=120, sway=60, wind=40 + wind, shift=shift)


def autumnStreet(t, key='as', rainK=0.0, zebraK=1.0, trees=True, wet=1.0):
    """night shop street (from 《后来》) with ginkgo trees on the pavement and a zebra crossing on the road"""
    import sets2
    sets2.streetTall2(t, key, rainK)
    if zebraK > 0:
        for i in range(-2, 12):
            xf = 960 + (i - 4.5) * 150
            xn = 960 + (i - 4.5) * 330
            paint([[xf, 700], [xf + 80, 700], [xn + 180, H + 40], [xn, H + 40]], wash='#E9E4F2', washOp=int(170 * zebraK), ink=None, lite=True)
    if trees:
        for j, tx in enumerate((150, 1790)):
            ginkgoTree(tx, 668, 64, t, key=f'{key}gt{j}', night=.55)
    leafCarpet(-200, 690, W + 200, H + 40, 26, seed=len(key) + 11, s=14, a=.85)


def vhs(t, date, k=1.0, lt=0.0):
    """rewind overlay: blue tint, scan lines, a tracking band, ◀◀ x8 and a date stamp"""
    if k <= 0:
        return
    tint('#3A5AA8', .22 * k, skia.BlendMode.kScreen)
    pa = skia.Paint(AntiAlias=False, Color=skcol('#000000', .12 * k))
    for y in range(0, H, 6):
        G.c.drawRect(skia.Rect.MakeXYWH(-50, y, W + 100, 2), pa)
    by = (t * 900) % (H + 200) - 100
    flatRect(-50, by, W + 100, 34, '#FFFFFF', .18 * k)
    for i in range(8):
        h1 = hash1(math.floor(t * 24) * 3.1 + i)
        flatRect(h1 * W, by + 6 + i * 3, 60 + 200 * hash1(i * 7.7), 2, '#FFFFFF', .35 * k)
    # ◀◀ x8
    x0, y0 = 120, 110
    for j in range(2):
        flat([[x0 + j * 46 + 46, y0 - 26], [x0 + j * 46 + 46, y0 + 26], [x0 + j * 46, y0]], '#FFFFFF', .95 * k)
    text('x8', x0 + 150, y0 + 2, 52, '#FFFFFF', shadow=True, a=k)
    if frac(t * 2) < .6:
        text('REW', x0 + 270, y0 + 2, 40, '#FFFFFF', shadow=True, a=.9 * k)
    text(date, W - 330, H - 190, 54, '#FFE07A', face=WENKAI, shadow=True, a=k)
