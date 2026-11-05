# mz.py: props and sets for 《幻昼+短发女孩+罗生门》串烧 (watercolour + ink). Engine files stay untouched.
# Her costume for this song: a short chocolate bob (齐耳短发) + a white jasmine flower (茉莉) on the hair.
# Day half: barber-shop street with a jasmine hedge, rooftop + moon, night plaza, winter bench, night market, rainy corner.
# Night half: his windowless bedroom, his phone chat, dream tape-measure, clover pot, heart cage, park bench + star river.
import math
from eng import *
import eng
import clawd as _cl
from clawd import *
from props import puff, sparkle, sparkles, floatHearts, bubble, stamp, sunburst, stripes, tree, bush, lamp, impactLines
from common import B, bt, pk, after, age, handXY, kt

WENKAI = 'LXGWWenKai-Regular.ttf'
HOT = '#E8476E'
PINK, PINKDK = '#EE9AAE', '#C0637B'
HAIR, HAIRDK, HAIRLT = '#4E3330', '#2E1D1E', '#8A5E52'
JAS = '#FFFDF4'
MOONC = '#FFF8E2'
NIGHT1, NIGHT2 = '#1B2152', '#3A3F7E'


# ------------------------------------------------------------------ her bob + jasmine (added by wrapping clawd.hat)
_hat0 = _cl.hat
JS = [1.0]          # jasmine size multiplier (S01 k4 bloom)


def jasmine(x, y, r, open_=1.0, key='jas', rot=0.0, col=JAS, a=1.0):
    """a jasmine blossom: 5 narrow pointed white petals around a pale-yellow eye"""
    if open_ <= .02:
        return
    k = backOut(clamp(open_))
    push()
    translate(x, y)
    rotate(rot)
    scale(k)
    boilSeed(key)
    for i in range(5):
        ang = i / 5 * TAU - math.pi / 2
        push()
        rotate(ang)
        paint([[0, -r * .18], [r * .34, -r * .62], [0, -r * 1.12], [-r * .34, -r * .62]], wash=col, washOp=int(255 * a), ink=INK, sw=.45 * min(1.6, r / 14), curv=.55)
        pop()
    paint(ellPts(0, 0, r * .26, r * .26, 10), wash='#F6E59A', washOp=int(255 * a), ink=INK, sw=.35)
    pop()


def _bobPts(u, view):
    """hair outline in hat space (front-view coordinates)"""
    P = lambda pts: [[a * u, b * u] for a, b in pts]
    if view == 'side':
        return P([[-3.5, -4.4], [-3.7, -7.6], [-2.6, -9.3], [0, -9.8], [2.4, -9.4], [3.6, -8.0], [3.5, -7.2], [2.4, -7.35],
                  [1.2, -7.1], [-.6, -7.3], [-1.6, -6.4], [-2.3, -4.6], [-2.9, -4.1]])
    return P([[-5.55, -4.3], [-5.75, -7.6], [-4.6, -9.25], [-2.2, -9.95], [0, -10.05], [2.2, -9.95], [4.6, -9.25], [5.75, -7.6], [5.55, -4.3],
              [5.0, -3.95], [4.35, -4.4], [4.35, -7.05], [3.3, -7.35], [2.4, -6.95], [1.3, -7.3], [.2, -6.95], [-.9, -7.3], [-2.0, -6.95],
              [-3.1, -7.35], [-4.35, -7.05], [-4.35, -4.4], [-5.0, -3.95]])


def _hat(u, h, sw, o=None):
    o = o or {}
    view = o.get('view') or 'front'
    if h == 'bob':
        if view in ('back', 'qback'):
            P = lambda pts: [[a * u, b * u] for a, b in pts]
            paint(P([[-5.6, -4.2], [-5.75, -7.6], [-4.6, -9.25], [0, -10.05], [4.6, -9.25], [5.75, -7.6], [5.6, -4.2], [4.6, -3.9], [0, -4.1],
                     [-4.6, -3.9]]), wash=HAIR, fill=HAIRDK, fillOp=70, ink=INK, sw=sw * .8, curv=.35)
            return
        pts = _bobPts(u, view)
        if view == 'q':
            # the face sits right of centre in the 3/4 view: shift the hair a little and squeeze the far (left) side
            pts = [[(x + .6 * u) * (1 if x > 0 else .92), y] for x, y in pts]
        paint(pts, wash=HAIR, fill=HAIRDK, fillOp=70, ink=INK, sw=sw * .8, curv=.35)
        # sheen arc
        inkLine([[-3.4 * u, -8.9 * u], [-1.4 * u, -9.55 * u], [1.0 * u, -9.6 * u]], sw * 1.1, HAIRLT, 'ink', .5)
        return
    if h == 'jasmine':
        fx = -3.5 * u if view != 'side' else -1.6 * u
        js = JS[0]
        jasmine(fx, -9.0 * u, 1.05 * u * js, key='hjas', rot=.2)
        jasmine(fx + 1.25 * u * js, -9.55 * u, .62 * u * js, key='hjas2', rot=-.3)
        paint(ellPts(fx + .5 * u, -8.35 * u, .55 * u, .26 * u, 10, 0, -.3), wash='#7CBF6A', ink=INK, sw=sw * .35)
        return
    return _hat0(u, h, sw, o)


_cl.hat = _hat
LOOK = ['bob', 'jasmine']


def herM(x, y, u, o=None):
    """her in this MV: pink Clawd, short bob, jasmine on the hair"""
    o = dict(o or {})
    o.setdefault('hat', LOOK)
    her(x, y, u, o)


def emH(t, keys, **kw):
    o = emotions(t, keys, HER)
    o.update(kw)
    return o


def emM(t, keys, **kw):
    o = emotions(t, keys, ME)
    o.update(kw)
    return o


def ek(k):
    """emotion key time: the new face is fully there on the beat frame"""
    return B[k] - .06


def hitK(t, k, d=.12):
    a = t - (B[k] - .04)
    return 0.0 if a < 0 else math.exp(-a / d)


def popB(t, k, d=.16):
    """0..1 pop that is 1 by the beat frame (starts ~1 frame early)"""
    return clamp((t - (B[k] - .05)) / d)


def landK(t, k, d=.16):
    """0..1 progress that reaches 1 exactly on beat k"""
    return clamp((t - (B[k] - d)) / d)


def line(x0, y0, x1, y1, col, a=1.0, w=2.0):
    G.c.drawLine(x0, y0, x1, y1, skia.Paint(AntiAlias=True, Color=skcol(col, a), StrokeWidth=w, Style=skia.Paint.kStroke_Style,
                                            StrokeCap=skia.Paint.kRound_Cap))


def circ(x, y, r, col, a=1.0):
    G.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=skcol(col, a)))


def ring(x, y, r, col, a=1.0, w=3.0):
    G.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=skcol(col, a), StrokeWidth=w, Style=skia.Paint.kStroke_Style))


def heart(x, y, r, col=HOT, key='ht', sw=.9, shine=True, a=1.0, crack=0.0, rot=0.0):
    if r <= .5:
        return
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(heartPts(0, 0, r, 22), wash=col, washOp=int(255 * a), fill=mixCol(col, INK, .25), fillOp=int(60 * a), ink=INK, sw=sw)
    if shine:
        paint(ellPts(-r * .45, -r * .35, r * .2, r * .13, 10, 0, -.6), wash='#FFFFFF', washOp=int(170 * a), ink=None)
    if crack > .02:
        k = clamp(crack)
        pts = [[0, -r * .55], [-r * .16, -r * .25], [r * .14, 0], [-r * .12, r * .3], [0, r * .62]]
        n = max(2, int(2 + k * 3))
        inkLine(pts[:n], sw * 2.2, INK, 'ink', 0)
    pop()


def labelTag(txt, x, y, size, col='#FFFDF6', tcol=INK, rot=0.0, k=1.0, key='lt', face=None, pad=.55):
    if k <= .02:
        return
    push()
    translate(x, y)
    rotate(rot)
    scale(backOut(clamp(k)))
    w = textW(txt, size, face or KUAILE) + size * pad * 2
    h = size * 1.45
    boilSeed(key)
    paint(rrPts(-w / 2, -h / 2, w, h, h * .28), wash=col, ink=INK, sw=1.0)
    text(txt, 0, 0, size, tcol, face=face or KUAILE, shadow=False)
    pop()


def dots3(x, y, s, k, col=INK, key='d3'):
    """a '……' speech cloud"""
    if k <= .02:
        return
    push()
    translate(x, y)
    scale(backOut(clamp(k)))
    puff(0, 0, s, '#FFFFFF', key=key)
    for i in range(3):
        circ((i - 1) * s * .42, 0, s * .1, col)
    pop()


# ------------------------------------------------------------------ day street: barber shop, jasmine hedge
def barberPole(x, y, h, t, key='bp'):
    w = h * .22
    boilSeed(key)
    paint(rrPts(x - w / 2 - 6, y - h / 2 - 22, w + 12, 26, 10), wash='#D9D4CC', ink=INK, sw=.8)
    paint(rrPts(x - w / 2 - 6, y + h / 2 - 4, w + 12, 26, 10), wash='#D9D4CC', ink=INK, sw=.8)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(x - w / 2, y - h / 2, w, h), skia.ClipOp.kIntersect, True)
    flatRect(x - w / 2, y - h / 2, w, h, '#FFFFFF')
    off = (t * 90) % (w * 1.4)
    for i in range(-3, int(h / (w * .7)) + 4):
        y0 = y - h / 2 + i * w * .7 - off
        col = '#E0344E' if i % 2 == 0 else '#3D6FD8'
        flat([[x - w / 2, y0], [x + w / 2, y0 - w * .6], [x + w / 2, y0 - w * .6 + w * .3], [x - w / 2, y0 + w * .3]], col, .92)
    G.c.restore()
    paint(rectPts(x - w / 2, y - h / 2, w, h), ink=INK, sw=1.0)
    glow(x, y, h * .5, '#FFFFFF', .25)


def awning(x, y, w, h, c1, c2, key='aw', n=7):
    boilSeed(key)
    sw_ = w / n
    for i in range(n):
        col = c1 if i % 2 == 0 else c2
        paint([[x + i * sw_, y], [x + (i + 1) * sw_, y], [x + (i + 1) * sw_ + 6, y + h], [x + i * sw_ + 6, y + h]], wash=col, ink=None)
        paint(ellPts(x + (i + .5) * sw_ + 6, y + h, sw_ / 2, h * .22, 12), wash=col, ink=INK, sw=.6)
    paint(rectPts(x - 6, y - 14, w + 18, 16), wash=mixCol(c2, INK, .3), ink=INK, sw=.8)
    inkLine([[x, y], [x + w + 6, y]], 1.0, INK, 'ink', 0)


def doorCurtain(x0, x1, top, bot, sway=0.0, open_=0.0, key='dc', col='#FFF3E0', pat='#E89AAE'):
    """a cloth door curtain (暖帘) in a doorway: two panels that swing / part"""
    w = (x1 - x0) / 2
    for s, xs in ((-1, x0), (1, x0 + w)):
        push()
        piv = xs if s < 0 else xs + w
        translate(piv, top)
        k = open_
        ww = w * (1 - .7 * k)
        dx = s * sway * 18
        boilSeed(key + str(s))
        if s < 0:
            pts = [[0, 0], [ww, 0], [ww + dx, (bot - top) * .62], [0 + dx * .4, (bot - top) * .62]]
        else:
            pts = [[-ww, 0], [0, 0], [0 + dx * .4, (bot - top) * .62], [-ww + dx, (bot - top) * .62]]
        paint(pts, wash=col, fill=mixCol(col, INK, .1), fillOp=50, ink=INK, sw=.9)
        cx = (pts[0][0] + pts[1][0]) / 2
        jasmine(cx, (bot - top) * .3, 22, key=key + 'j' + str(s), col='#FFFFFF')
        pop()


def barberShop(x, y, w, t, curtainOpen=0.0, sway=0.0, key='bs', sign='理发'):
    """shop front on ground y (no glass): brick wall, striped awning, cloth door curtain, sign + barber pole"""
    h = 560
    boilSeed(key)
    paint(rectPts(x, y - h, w, h), wash='#F3D9C2', fill='#E2B99A', fillOp=60, ink=INK, sw=1.0)
    for r in range(9):
        for c in range(int(w / 90) + 1):
            bx_ = x + c * 90 + (45 if r % 2 else 0)
            if bx_ + 80 > x + w:
                continue
            G.c.drawRect(skia.Rect.MakeXYWH(bx_ + 4, y - h + 20 + r * 58, 80, 48), skia.Paint(AntiAlias=True, Color=skcol('#E7BFA4', .55)))
    # sign board
    paint(rrPts(x + w * .16, y - h + 30, w * .68, 96, 18), wash='#3E4C8E', fill='#2C3870', fillOp=60, ink=INK, sw=1.1)
    text(sign, x + w / 2, y - h + 78, 64, '#FFF3E0', stroke=INK, strokeW=8)
    awning(x - 10, y - h + 150, w + 4, 70, '#E8476E', '#FFF3E0', key=key + 'aw', n=9)
    # doorway (dark interior + cloth curtain)
    dx0, dx1, dtop = x + w * .3, x + w * .7, y - 330
    paint(rectPts(dx0, dtop, dx1 - dx0, y - dtop), wash='#4A3A48', ink=INK, sw=1.0)
    doorCurtain(dx0, dx1, dtop, y, sway, curtainOpen, key=key + 'dc')
    paint(rectPts(dx0 - 14, dtop - 14, dx1 - dx0 + 28, 18), wash='#8A5A3C', ink=INK, sw=.8)
    barberPole(x + w * .14, y - 210, 230, t, key=key + 'pole')
    # little potted plant by the door
    boilSeed(key + 'pot')
    paint(rectPts(x + w * .78, y - 70, 70, 70), wash='#C9774E', ink=INK, sw=.8)
    bush(x + w * .78 + 35, y - 70, 60, key=key + 'pb', col='#86C96E')
    return dx0, dx1, dtop


def jasmineHedge(x0, x1, y, h, t, bloom=1.0, key='jh', seed=3, night=0.0, wave=None):
    """a clipped green hedge with white jasmine stars; bloom 0..1 (or wave=(tb, speed) to pop left->right)"""
    col = mixCol('#6FB35E', '#2E4A5A', night * .6)
    dk = mixCol('#3F7A3E', '#1B2A3E', night * .6)
    boilSeed(key)
    pts = [[x0, y]]
    n = int((x1 - x0) / 70) + 1
    for i in range(n + 1):
        xx = x0 + i * (x1 - x0) / n
        pts.append([xx, y - h + 16 * math.sin(i * 1.7 + seed)])
    pts.append([x1, y])
    paint(pts, wash=col, fill=dk, fillOp=80, ink=INK, sw=1.0, curv=.6)
    m = int((x1 - x0) / 46)
    for i in range(m):
        fx = x0 + 20 + (x1 - x0 - 40) * hash1(i * 3.1 + seed)
        fy = y - h * .15 - (h * .75) * hash1(i * 7.7 + seed)
        if wave is not None:
            tb, sp = wave
            k = clamp((t - tb - (fx - x0) / sp) / .14)
        else:
            k = bloom
        jasmine(fx, fy, 13 + 5 * hash1(i * 1.3), k, key=f'{key}{i}', rot=hash1(i) * 3, col=mixCol(JAS, '#C8CCE8', night * .4))


def scentRibbon(x0, y0, x1, y1, k, t, key='sc', col='#FFFFFF'):
    """wavy scent streamers carrying tiny jasmine petals from (x0,y0) toward (x1,y1); k 0..1 = how far they've reached"""
    if k <= .02:
        return
    for j in range(3):
        pts = []
        n = 18
        for i in range(n + 1):
            f = i / n * k
            x = lerp(x0, x1, f)
            y = lerp(y0, y1, f) + math.sin(f * 9 + t * 6 + j * 2) * 26 + (j - 1) * 34
            pts.append([x, y])
        boilSeed(key + str(j))
        inkLine(pts, 2.6, mixCol(col, '#F7C6D2', j * .3), 'ink', .6)
        jasmine(pts[-1][0], pts[-1][1], 12, 1, key=key + 'p' + str(j), rot=t * 3 + j)


def bigMoon(x, y, r, k=1.0, glowA=.7, key='moon'):
    if k <= .02:
        return
    rr = r * backOut(clamp(k))
    glow(x, y, rr * 2.4, '#FFF4C8', glowA * clamp(k))
    boilSeed(key)
    paint(ellPts(x, y, rr, rr, 40), wash=MOONC, fill='#F2E2B0', fillOp=60, ink=INK, sw=1.1)
    for i, (dx, dy, cr) in enumerate([(-.3, -.2, .16), (.25, .15, .11), (.05, .4, .08), (.38, -.3, .07)]):
        paint(ellPts(x + dx * rr, y + dy * rr, cr * rr, cr * rr, 14), wash='#EFE0B8', ink=None)


def nightSky(c1=NIGHT1, c2=NIGHT2):
    gradRect(-400, -400, W + 800, H + 800, [c1, c2])


def starsBg(t, seed, n, x0, y0, x1, y1, a=1.0, r=3.0):
    for i in range(n):
        x = x0 + (x1 - x0) * hash1(i * 2.3 + seed)
        y = y0 + (y1 - y0) * hash1(i * 5.1 + seed)
        tw = .55 + .45 * math.sin(t * 3 + i * 1.9)
        circ(x, y, r * (.6 + .8 * hash1(i * 9.7 + seed)), '#FFF6D8', a * tw)


def frostCorners(k, t, key='fr'):
    """ice ferns growing in from the four corners of the frame (screen space at the camera's frame)"""
    if k <= .02:
        return
    for ci, (cx, cy) in enumerate([(0, 0), (W, 0), (0, H), (W, H)]):
        sx = 1 if cx == 0 else -1
        sy = 1 if cy == 0 else -1
        for j in range(5):
            ang = (j / 4) * math.pi / 2
            L = (180 + 90 * hash1(ci * 7 + j)) * k
            ex, ey = cx + sx * math.cos(ang) * L, cy + sy * math.sin(ang) * L
            boilSeed(f'{key}{ci}{j}')
            inkLine([[cx, cy], [ex, ey]], 3.2, '#E8F6FF', 'ink', 0)
            for b in range(1, 4):
                f = b / 4
                px, py = lerp(cx, ex, f), lerp(cy, ey, f)
                bl = L * .22 * (1 - f * .5)
                for s in (-1, 1):
                    a2 = ang + s * .7
                    inkLine([[px, py], [px + sx * math.cos(a2) * bl, py + sy * math.sin(a2) * bl]], 2.0, '#E8F6FF', 'ink', 0)
        glow(cx, cy, 330 * k, '#DDF2FF', .55 * k)


def snow(t, seed, n, x0, y0, x1, y1, a=1.0, r=5.0, sp=120):
    for i in range(n):
        x = x0 + (x1 - x0) * hash1(i * 2.3 + seed) + 20 * math.sin(t * 1.5 + i)
        y = y0 + ((hash1(i * 5.1 + seed) * (y1 - y0) + t * sp * (.6 + .5 * hash1(i * 3.3))) % (y1 - y0))
        circ(x, y, r * (.6 + .7 * hash1(i * 9.7 + seed)), '#FFFFFF', a * .9)


def snowflake(x, y, r, a=1.0, rot=0.0, col='#FFFFFF'):
    for i in range(6):
        ang = i / 6 * TAU + rot
        ex, ey = x + math.cos(ang) * r, y + math.sin(ang) * r
        line(x, y, ex, ey, col, a, max(2, r * .12))
        for f in (.55,):
            px, py = x + math.cos(ang) * r * f, y + math.sin(ang) * r * f
            for s in (-1, 1):
                line(px, py, px + math.cos(ang + s * .8) * r * .3, py + math.sin(ang + s * .8) * r * .3, col, a, max(1.5, r * .09))


def bucketTears(x, y, s, fill, frozen=0.0, key='bt', label='眼泪'):
    """small tin pail on the ground at (x,y) (bottom centre), s = height; fill 0..1.2 (overflow), frozen 0..1"""
    w0, w1 = s * .78, s * .62
    boilSeed(key)
    paint([[x - w0 / 2, y - s], [x + w0 / 2, y - s], [x + w1 / 2, y], [x - w1 / 2, y]], wash='#B9C4D6', fill='#8492AA', fillOp=70, ink=INK, sw=1.0)
    f = clamp(fill)
    water = mixCol('#7FC8F0', '#E4F6FF', frozen)
    if f > .02:
        top = y - s * f * .92
        wt = lerp(w1, w0, f * .92)
        paint([[x - wt / 2 + 4, top], [x + wt / 2 - 4, top], [x + w1 / 2 - 4, y - 4], [x - w1 / 2 + 4, y - 4]], wash=water, washOp=210, ink=None)
        paint(ellPts(x, top, wt / 2 - 4, s * .07, 18), wash=mixCol(water, '#FFFFFF', .4), ink=INK, sw=.6)
    if fill > 1.0:
        o = clamp((fill - 1) / .2)
        for s_ in (-1, 1):
            paint([[x + s_ * w0 / 2, y - s], [x + s_ * (w0 / 2 + 18), y - s * .55], [x + s_ * (w0 / 2 + 30), y], [x + s_ * (w0 / 2 + 6), y]],
                  wash=water, washOp=int(200 * o), ink=INK, sw=.5)
        paint(ellPts(x, y + 6, w0 * .95, s * .1, 20), wash=water, washOp=int(160 * o), ink=None)
    if frozen > .1:
        for i in range(4):
            ix = x - w0 / 2 + 10 + i * (w0 - 20) / 3
            L = s * .28 * frozen * (.6 + .5 * hash1(i))
            paint([[ix - 7, y - s * .82], [ix + 7, y - s * .82], [ix, y - s * .82 + L]], wash='#E8F7FF', ink=INK, sw=.5)
    paint(ellPts(x, y - s, w0 / 2, s * .09, 18), ink=INK, sw=1.0)
    labelTag(label, x, y - s * .45, s * .2, '#FFFDF6', INK, -.05, 1, key=key + 'lb')


# ------------------------------------------------------------------ night market
def lantern(x, y, s, t, key='ln', col='#E8423E'):
    sw_ = math.sin(t * 2 + x) * .05
    push()
    translate(x, y)
    rotate(sw_)
    line(0, -s * .9, 0, -s * .55, INK, 1, 2)
    boilSeed(key)
    paint(ellPts(0, 0, s * .45, s * .55, 22), wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=.9)
    for i in (-1, 0, 1):
        inkLine([[i * s * .2, -s * .52], [i * s * .26, 0], [i * s * .2, s * .52]], .6, mixCol(col, INK, .4), 'inkfine', .5)
    paint(rectPts(-s * .2, -s * .62, s * .4, s * .12), wash='#F2C53D', ink=INK, sw=.6)
    paint(rectPts(-s * .2, s * .5, s * .4, s * .12), wash='#F2C53D', ink=INK, sw=.6)
    for i in range(3):
        line(-s * .1 + i * s * .1, s * .62, -s * .1 + i * s * .1, s * .9, '#F2C53D', 1, 2)
    pop()
    glow(x, y, s * 1.4, '#FFB36E', .35)


def beerMug(x, y, s, foam=1.0, key='bm', tilt=0.0):
    push()
    translate(x, y)
    rotate(tilt)
    boilSeed(key)
    paint(rrPts(-s * .38, -s, s * .76, s, s * .1), wash='#F6C24A', fill='#E09A2A', fillOp=70, ink=INK, sw=1.0)
    inkLine([[s * .38, -s * .78], [s * .62, -s * .72], [s * .62, -s * .3], [s * .38, -s * .24]], 2.2, INK, 'ink', .5)
    for i in range(3):
        circ(-s * .2 + i * s * .2, -s * .4 - i * s * .15, s * .04, '#FFF3C8', .8)
    if foam > .02:
        for i in range(4):
            paint(ellPts(-s * .3 + i * s * .2, -s - s * .05, s * .16 * foam, s * .14 * foam, 12), wash='#FFFDF6', ink=INK, sw=.6)
    pop()


def noSign(x, y, r, k, t, key='ns'):
    """「禁止烟酒」 placard: red ring + slash over a cigarette and a mug"""
    if k <= .02:
        return
    push()
    translate(x, y)
    scale(backOut(clamp(k)))
    boilSeed(key)
    paint(rrPts(-r * 1.2, -r * 1.25, r * 2.4, r * 2.9, r * .2), wash='#FFFDF6', ink=INK, sw=1.2)
    # cigarette
    paint(rectPts(-r * .75, -r * .2, r * 1.0, r * .2), wash='#FFFFFF', ink=INK, sw=.7)
    paint(rectPts(-r * .75, -r * .2, r * .25, r * .2), wash='#E8A35A', ink=None)
    paint(rectPts(r * .25, -r * .2, r * .1, r * .2), wash='#E8423E', ink=None)
    beerMug(r * .45, r * .55, r * .6, key=key + 'm')
    G.c.drawCircle(0, 0, r * .95, skia.Paint(AntiAlias=True, Color=skcol('#E0344E'), StrokeWidth=r * .16, Style=skia.Paint.kStroke_Style))
    line(-r * .67, -r * .67, r * .67, r * .67, '#E0344E', 1, r * .16)
    text('禁止烟酒', 0, r * 1.32, r * .32, '#E0344E', shadow=False)
    pop()


def smoke(x, y, s, t, k=1.0, key='smk', col='#D8D4E2'):
    for i in range(5):
        ph = t * 1.4 + i * 1.3
        xx = x + math.sin(ph) * s * .4 + i * s * .3
        yy = y - i * s * .45
        r = s * (.35 + .1 * i)
        boilSeed(f'{key}{i}')
        paint(ellPts(xx, yy, r, r * .78, 16), wash=col, washOp=int(150 * k), ink=INK, sw=.4)


# ------------------------------------------------------------------ his room (no window)
def tissuePack(x, y, s, rot=0.0, key='tp'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rrPts(-s * .6, -s * .35, s * 1.2, s * .7, s * .12), wash='#BFE6F5', fill='#8CC8E2', fillOp=60, ink=INK, sw=.8)
    paint([[-s * .3, -s * .35], [-s * .1, -s * .75], [s * .15, -s * .5], [s * .3, -s * .35]], wash='#FFFFFF', ink=INK, sw=.6, curv=.5)
    paint(heartPts(s * .32, s * .08, s * .13, 14), wash='#FF8FB0', ink=None)
    pop()


def flipSign(x, y, w, h, flip, txtA, colA, txtB, colB, key='fs', k=1.0):
    """a two-sided card on a stick that flips horizontally; flip 0..1"""
    if k <= .02:
        return
    push()
    translate(x, y)
    scale(backOut(clamp(k)))
    line(0, h * .5, 0, h * 1.1, '#8A5A3C', 1, 8)
    sx = abs(math.cos(flip * math.pi))
    front = flip < .5
    push()
    scale(max(.04, sx), 1)
    boilSeed(key + ('a' if front else 'b'))
    col = colA if front else colB
    paint(rrPts(-w / 2, -h / 2, w, h, h * .2), wash=col, fill=mixCol(col, INK, .2), fillOp=50, ink=INK, sw=1.2)
    text(txtA if front else txtB, 0, 0, h * .5, '#FFFFFF', stroke=INK, strokeW=h * .09)
    pop()
    pop()


def thermometer(x, y, h, level, key='th', t=0.0):
    """standing thermometer, bulb at (x, y); level 0..1"""
    w = h * .14
    boilSeed(key)
    paint(rrPts(x - w * .9, y - h - w * .4, w * 1.8, h + w * .4, w * .9), wash='#FFFDF6', ink=INK, sw=1.0)
    for i in range(6):
        yy = y - h * .2 - i * h * .14
        line(x + w * .3, yy, x + w * .75, yy, INK, .7, 2)
    lv = clamp(level)
    col = mixCol('#E8476E', '#FF2A2A', lv)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x - w * .25, y - h * .1 - (h * .8) * lv, w * .5, (h * .8) * lv + h * .1), w * .25, w * .25,
                      skia.Paint(AntiAlias=True, Color=skcol(col)))
    paint(ellPts(x, y, w * .9, w * .9, 18), wash=col, ink=INK, sw=1.0)
    if lv > .95:
        glow(x, y - h * .9, h * .4, '#FF6A5A', .5)


def icePack(x, y, s, melt=0.0, key='ip', rot=0.0):
    if melt >= 1:
        return
    push()
    translate(x, y)
    rotate(rot)
    k = 1 - melt * .5
    scale(1 + melt * .2, k)
    boilSeed(key)
    paint(rrPts(-s * .7, -s * .35, s * 1.4, s * .7, s * .25), wash='#BFE8FF', washOp=int(240 * (1 - melt * .6)), fill='#7FC8F0', fillOp=60,
          ink=INK, sw=1.0)
    text('冷静', 0, 0, s * .36, '#2C6FA8', shadow=False, a=1 - melt)
    pop()


def steamPuffs(x, y, s, t, k, key='st'):
    if k <= .02:
        return
    for i in range(4):
        ph = (t * 1.6 + i * .25) % 1
        xx = x + (i - 1.5) * s * .5 + math.sin(t * 5 + i) * s * .1
        yy = y - ph * s * 1.6
        r = s * (.25 + .3 * ph)
        boilSeed(f'{key}{i}')
        paint(ellPts(xx, yy, r, r * .8, 14), wash='#FFFFFF', washOp=int(200 * k * (1 - ph)), ink=None)


# ------------------------------------------------------------------ dream tape measure, clover pot, heart cage
def tapeMeasure(x0, x1, y, k, key='tm', t=0.0):
    """long yellow tape from x0 to x0+(x1-x0)*k with tick marks; case at x0"""
    xe = lerp(x0, x1, clamp(k))
    boilSeed(key)
    paint(rectPts(x0, y - 22, xe - x0, 44), wash='#F6D04D', fill='#E2B02A', fillOp=60, ink=INK, sw=1.0)
    i = 0
    xx = x0 + 20
    while xx < xe - 6:
        L = 20 if i % 5 == 0 else 10
        line(xx, y - 22, xx, y - 22 + L, INK, .8, 2)
        xx += 26
        i += 1
    paint(rrPts(x0 - 90, y - 70, 120, 120, 26), wash='#E8476E', fill='#B8324F', fillOp=60, ink=INK, sw=1.2)
    paint(ellPts(x0 - 30, y - 10, 28, 28, 18), wash='#FFFDF6', ink=INK, sw=.8)
    paint(rectPts(xe - 8, y - 30, 16, 60), wash='#B9C4D6', ink=INK, sw=.8)
    return xe


def cloverPot(x, y, s, leaves, falls, t, key='cp', label='侥幸'):
    """heart-shaped pot at ground (x,y); four-leaf clover with `leaves` (list of 4 bools still on); falls = list of (i, age) falling"""
    boilSeed(key)
    # stem
    inkLine([[x, y - s * .55], [x + s * .05, y - s * 1.1], [x, y - s * 1.45]], 3.2, '#4E8A3E', 'ink', .5)
    cx, cy = x, y - s * 1.5
    for i in range(4):
        ang = i / 4 * TAU + math.pi / 4
        if leaves[i]:
            push()
            translate(cx, cy)
            rotate(ang + math.pi / 2)
            paint(heartPts(0, -s * .32, s * .3, 18), wash='#7CC36B', fill='#4E8A3E', fillOp=60, ink=INK, sw=.9)
            pop()
    for (i, ag) in falls:
        if ag < 0 or ag > 1.6:
            continue
        ang = i / 4 * TAU + math.pi / 4
        fx = cx + math.cos(ang) * s * (.32 + 1.2 * ag) + math.sin(ag * 6 + i) * s * .25
        fy = cy + math.sin(ang) * s * .32 + ag * ag * s * 2.2 + ag * s * .9
        push()
        translate(fx, fy)
        rotate(ang + math.pi / 2 + ag * 4)
        paint(heartPts(0, -s * .32, s * .3, 18), wash='#9CD08A', fill='#4E8A3E', fillOp=40, ink=INK, sw=.8)
        pop()
    paint(heartPts(x, y - s * .28, s * .6, 22), wash='#E8476E', fill='#B8324F', fillOp=60, ink=INK, sw=1.1)
    paint(ellPts(x, y - s * .62, s * .48, s * .1, 18), wash='#6B4A3A', ink=INK, sw=.7)
    labelTag(label, x, y - s * .2, s * .2, '#FFFDF6', INK, -.06, 1, key=key + 'lb')


def heartCage(x, y, s, door=0.0, key='hc', a=1.0, glint=0.0):
    """a golden heart-shaped birdcage standing on (x, y) (base centre); s = half width. door 0..1 opens (right side)"""
    hp = heartPts(x, y - s * 1.05, s, 40)
    top = min(p[1] for p in hp)
    # bars: vertical lines clipped to the heart
    pth = eng._path(hp)
    G.c.save()
    G.c.clipPath(pth, skia.ClipOp.kIntersect, True)
    n = 11
    for i in range(n):
        xx = x - s * 1.1 + i * (s * 2.2) / (n - 1)
        if door > .02 and xx > x + s * .2 and xx < x + s * .8:
            continue
        line(xx, top - 10, xx, y + 10, '#C99A2E', a, 7)
        line(xx - 2, top - 10, xx - 2, y + 10, '#F6D27A', a * .8, 2.5)
    for j in range(4):
        yy = top + (y - top) * (j + 1) / 5
        line(x - s * 1.2, yy, x + s * 1.2, yy, '#C99A2E', a * .9, 5)
    G.c.restore()
    boilSeed(key)
    paint(hp, ink=INK, sw=1.6)
    inkLine(hp + [hp[0]], 6.0, '#C99A2E', 'ink', 0)
    # base + hook
    paint(rrPts(x - s * .9, y - 26, s * 1.8, 40, 14), wash='#C99A2E', fill='#8E6A1E', fillOp=60, ink=INK, sw=1.1)
    ring(x, top - 40, 34, '#C99A2E', a, 8)
    # door (right lower)
    if door > .02:
        push()
        translate(x + s * .8, y - s * .9)
        sx = math.cos(door * math.pi * .8)
        scale(sx, 1)
        boilSeed(key + 'door')
        paint(rectPts(-s * .6, -s * .55, s * .6, s * .9), wash=None, ink=INK, sw=1.0)
        for i in range(4):
            line(-s * .6 + i * s * .2, -s * .55, -s * .6 + i * s * .2, s * .35, '#C99A2E', a, 6)
        pop()
    if glint > .02:
        sparkle(x - s * .5, top + s * .4, 30 * glint, '#FFF6C8', glint)
    return top


def keyProp(x, y, s, rot=0.0, key='key'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(heartPts(-s * .55, 0, s * .32, 18), wash='#F2C53D', fill='#C99A2E', fillOp=70, ink=INK, sw=.8)
    paint(rectPts(-s * .3, -s * .07, s * .9, s * .14), wash='#F2C53D', ink=INK, sw=.7)
    paint(rectPts(s * .4, 0, s * .1, s * .22), wash='#F2C53D', ink=INK, sw=.6)
    paint(rectPts(s * .2, 0, s * .1, s * .16), wash='#F2C53D', ink=INK, sw=.6)
    pop()


def zipperMouth(x, y, w, k, key='zp'):
    """a zipper pulled shut across a mouth at (x, y); k 0..1 = how far it's zipped (left -> right)"""
    if k <= .02:
        return
    boilSeed(key)
    xe = x - w / 2 + w * clamp(k)
    paint(rrPts(x - w / 2, y - w * .09, xe - (x - w / 2), w * .18, w * .05), wash='#9AA3B8', ink=INK, sw=.7)
    n = int((xe - (x - w / 2)) / (w * .1))
    for i in range(n):
        xx = x - w / 2 + (i + .5) * w * .1
        line(xx, y - w * .09, xx, y + w * .09, INK, .8, 1.5)
    paint(rrPts(xe - w * .06, y - w * .05, w * .2, w * .26, w * .04), wash='#C9CDD8', ink=INK, sw=.7)


def starRiver(t, x0, x1, ytop, ybot, k, key='sr'):
    """a glittering river of stars filling a gap (trapezoid narrower at the top)"""
    if k <= .02:
        return
    w = (x1 - x0) * k
    cx = (x0 + x1) / 2
    pts = [[cx - w * .35, ytop], [cx + w * .35, ytop], [cx + w * .5, ybot], [cx - w * .5, ybot]]
    boilSeed(key)
    paint(pts, wash='#1E2A6E', fill='#3A4AA0', fillOp=90, ink=INK, sw=1.0)
    G.c.save()
    G.c.clipPath(eng._path(pts), skia.ClipOp.kIntersect, True)
    for i in range(70):
        f = hash1(i * 2.7)
        yy = ytop + (ybot - ytop) * hash1(i * 5.3)
        ww = lerp(w * .35, w * .5, (yy - ytop) / max(1, ybot - ytop))
        xx = cx + (f - .5) * 2 * ww + ((t * 30 * (1 + hash1(i))) % 60) - 30
        tw = .5 + .5 * math.sin(t * 4 + i * 1.7)
        circ(xx, yy, 2.5 + 3 * hash1(i * 7.1), '#FFF2B0', .5 + .5 * tw)
    glow(cx, (ytop + ybot) / 2, w * .6, '#8FA8FF', .35)
    G.c.restore()


def crackLine(x, y0, y1, k, key='crk', w=6.0):
    if k <= .02:
        return
    pts = []
    n = 9
    for i in range(n + 1):
        f = i / n
        if f > k:
            break
        pts.append([x + (18 if i % 2 else -18) * (1 if i else 0), lerp(y0, y1, f)])
    if len(pts) >= 2:
        boilSeed(key)
        inkLine(pts, w, INK, 'ink', 0)


def ghostG(x, y, u, aL=-.6, aR=-.6, key='gh', flip=False):
    """the grey fedora man (his rival): grey Clawd, a big ? for a face, a fedora; arms settable (nm.ghost fixes them)"""
    import nm
    o = dict(col='#8E8AA0', dk='#5E5A74', lt='#B8B4C8', eyes='blank', mouth=None, view='front', aL=aL, aR=aR, boilKey=key, flip=flip)
    clawd(x, y, u, o)
    paint(rectPts(x - 3.6 * u, y - 7.4 * u, 7.2 * u, 3.0 * u), wash='#8E8AA0', ink=None)
    text('?', x, y - 5.6 * u, 4.6 * u, '#F3EBDC', stroke=INK, strokeW=u * .5, shadow=False)
    nm.fedora(x, y - 8.0 * u, 4.0 * u, -.06, key=key + 'f')
    return o


def mugGuy(x, y, u, i, raise_=1.0, key='mg', flip=False):
    """a grey passer-by raising a beer mug (the mug sits in the hand)"""
    shade = ['#B8B6BE', '#A9A7B0', '#C4C2CA'][i % 3]
    o = dict(col=shade, dk=mixCol(shade, INK, .25), lt=mixCol(shade, '#FFFFFF', .4), view='q', flip=flip, eyes='blank', mouth=None,
             boilKey=f'{key}{i}', aL=.1, aR=lerp(.3, 1.3, raise_))
    clawd(x, y, u, o)
    hx, hy = handXY(x, y, u, o, 'R')
    beerMug(hx + (-1 if flip else 1) * .3 * u, hy + .9 * u, 2.4 * u, key=f'{key}m{i}', tilt=(-.25 if flip else .25) * raise_)
