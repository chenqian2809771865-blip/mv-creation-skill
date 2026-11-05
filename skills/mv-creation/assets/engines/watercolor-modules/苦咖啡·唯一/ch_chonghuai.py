# ch.py: props and sets for 《宠坏》 (watercolour + ink). Engine files are untouched; the tiara is added by wrapping clawd.hat.
import math
from eng import *
import eng
import clawd as _cl
from clawd import *
from props import C, puff, sparkle, sparkles, floatHearts, bubble, stamp, sunburst, stripes, groundBand, tree, bush, lamp, bench

WENKAI = 'LXGWWenKai-Regular.ttf'
CREAM = '#FFF8EE'
PINK = '#EE9AAE'
PINKDK = '#C0637B'
HOT = '#E8476E'

# ------------------------------------------------------------------ her tiara (song costume; the flower stays on her)
_hat0 = _cl.hat


def _hat(u, h, sw, o=None):
    if h == 'tiara':
        P = lambda pts: [[a * u, b * u] for a, b in pts]
        pts = P([[-.6, -7.95], [-.7, -10.0], [.5, -9.0], [1.6, -10.8], [2.7, -9.0], [3.9, -10.0], [3.8, -7.95]])
        paint(pts, wash='#F6CF4E', fill='#E0A92C', fillOp=90, ink=INK, sw=sw * .75)
        inkLine(P([[-.55, -8.5], [3.75, -8.5]]), sw * .4, '#B07C1A', 'inkfine', 0)
        for gx, gc in ((-.6, '#7FD0E8'), (1.6, HOT), (3.9, '#7FD0E8')):
            paint(ellPts(gx * u, (-10.15 if gx != 1.6 else -10.95) * u, u * .32, u * .32, 10), wash=gc, ink=INK, sw=sw * .4)
        paint(ellPts(1.6 * u, -8.95 * u, u * .38, u * .32, 10), wash=HOT, ink=None)
        G.c.drawCircle(1.45 * u, -9.05 * u, u * .1, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .8)))
        return
    if h == 'flowerL':      # her flower, nudged left of the tiara
        _cl.flowerAt(-2.9 * u, -8.6 * u, u, sw)
        return
    return _hat0(u, h, sw, o)


_cl.hat = _hat
QUEEN = ['tiara', 'flowerL']      # her look in this MV


def herQ(x, y, u, o=None):
    o = dict(o or {})
    o.setdefault('hat', QUEEN)
    her(x, y, u, o)


def fo(base, **kw):
    d = dict(base)
    d.update(kw)
    return d


# ------------------------------------------------------------------ small shapes
def rr(x, y, w, h, r, wash, ink=INK, sw=1.0, fill=None, fillOp=60, key=None, washOp=255):
    if key:
        boilSeed(key)
    paint(rrPts(x, y, w, h, r), wash=wash, washOp=washOp, fill=fill, fillOp=fillOp, ink=ink, sw=sw)


def heart(x, y, r, col=HOT, key='ht', sw=.9, shine=True, a=1.0):
    boilSeed(key)
    paint(heartPts(x, y, r, 26), wash=col, washOp=255 * a, fill=mixCol(col, INK, .25), fillOp=50 * a, ink=INK if a > .5 else None, sw=sw, curv=.4)
    if shine:
        paint(ellPts(x - r * .38, y - r * .35, r * .18, r * .12, 10, 0, -.6), wash='#FFFFFF', washOp=170 * a, ink=None)


def popK(t, tb, d=.16, lead=.04):
    """0..1 pop progress for something that lands on time tb"""
    return clamp((t - (tb - lead)) / d)


def shakeAmt(t, tb, amp=10, dec=14):
    a = t - tb
    if a < 0 or a > .5:
        return 0, 0
    e = amp * math.exp(-a * dec)
    return e * math.sin(a * 90), e * math.cos(a * 70) * .6


# ------------------------------------------------------------------ phone + chat UI
def phoneBody(cx, cy, w, h, key='ph', col='#2E2B3E', case=None):
    boilSeed(key)
    if case:
        paint(rrPts(cx - w / 2 - 14, cy - h / 2 - 14, w + 28, h + 28, w * .15), wash=case, fill=mixCol(case, INK, .2), fillOp=60, ink=INK, sw=1.4)
    paint(rrPts(cx - w / 2, cy - h / 2, w, h, w * .12), wash=col, ink=INK, sw=1.4)


def screenClip(cx, cy, w, h):
    sx, sy, sw_, sh = cx - w / 2 + w * .05, cy - h / 2 + w * .05, w * .9, h - w * .1
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(sx, sy, sw_, sh), w * .08, w * .08))
    return p, (sx, sy, sw_, sh)


def chatHeader(sx, sy, sw_, name, avatar=None, sub=None, love=False):
    flatRect(sx, sy, sw_, 128, '#FFFFFF')
    inkLine([[sx, sy + 128], [sx + sw_, sy + 128]], .6, '#C9C1D6', 'inkfine', 0)
    inkLine([[sx + 44, sy + 62], [sx + 28, sy + 80], [sx + 44, sy + 98]], 2.4, '#7A6E88', 'ink', 0)
    if avatar:
        avatar(sx + 100, sy + 80, 30)
    w_ = text(name, sx + 150, sy + 70, 44, INK, align='left', shadow=False)
    if love:
        heart(sx + 150 + w_ + 26, sy + 70, 16, HOT, key='hdrh', sw=.5, shine=False)
    if sub:
        text(sub, sx + 150, sy + 108, 22, '#9A8FA8', align='left', shadow=False, face=WENKAI)
    G.c.drawCircle(sx + sw_ - 40, sy + 80, 5, skia.Paint(AntiAlias=True, Color=skcol('#7A6E88')))
    G.c.drawCircle(sx + sw_ - 58, sy + 80, 5, skia.Paint(AntiAlias=True, Color=skcol('#7A6E88')))
    G.c.drawCircle(sx + sw_ - 22, sy + 80, 5, skia.Paint(AntiAlias=True, Color=skcol('#7A6E88')))


def miniHead(x, y, r, col, dk, flower=False, face='happy', key='mh', tiara=False):
    """a tiny Clawd head (avatar / sticker)"""
    o = dict(col=col, dk=dk, lt=mixCol(col, '#FFFFFF', .5), view='front', noShadow=True, noLegs=True, boilKey=key, aL=-1.6, aR=-1.6)
    o.update(EMO_FACE.get(face, {}))
    if flower:
        o['hat'] = QUEEN if tiara else 'flower'
    G.c.save()
    clawd(x, y + r * .95, r / 5.2, o)
    G.c.restore()


EMO_FACE = dict(happy=dict(eyes='happy', mouth='smile', blush=.5), angry=dict(eyes='angry', mouth='teeth', tint='flush', tintK=.4),
                pout=dict(eyes='angry', mouth='pout', blush=.6), love=dict(eyes='heart', mouth='cat', blush=.8),
                smug=dict(eyes='narrow', mouth='smirk'), cry=dict(eyes='cry', mouth='wail'), wink=dict(eyes=['closed', 'normal'], mouth='tongue'),
                plain=dict(eyes='normal', mouth='smile'), shine=dict(eyes='shine', mouth='cat', blush=.4))


def msgBubble(x, y, txt, size, side, k, col=None, key='mb', tcol=INK, maxw=None):
    """chat bubble; side 'L' (incoming) or 'R' (outgoing); (x, y) = the bubble's outer edge anchor (left or right), top"""
    if k <= .02:
        return 0
    p = backOut(k)
    w = textW(txt, size) + size * 1.2
    h = size * 1.7
    col = col or ('#FFFFFF' if side == 'L' else '#FFC2D3')
    bx = x if side == 'L' else x - w
    push()
    ox = bx if side == 'L' else bx + w
    translate(ox, y + h)
    scale(p)
    translate(-ox, -(y + h))
    boilSeed(key)
    paint(rrPts(bx, y, w, h, h * .42), wash=col, ink=INK, sw=.9)
    tx = bx + (10 if side == 'L' else w - 10)
    paint([[tx - 12, y + h - 22], [tx + (-18 if side == 'L' else 18), y + h + 6], [tx + 12, y + h - 10]], wash=col, ink=None)
    text(txt, bx + w / 2, y + h / 2, size, tcol, shadow=False)
    pop()
    return h


def typingDots(x, y, t, k=1.0):
    if k < 1:
        return
    boilSeed('typ')
    paint(rrPts(x, y, 120, 64, 30), wash='#FFFFFF', washOp=255 * k, ink=INK, sw=.8)
    for i in range(3):
        a = .35 + .65 * (.5 + .5 * math.sin(t * 12 - i * 1.1))
        G.c.drawCircle(x + 32 + i * 28, y + 32, 8, skia.Paint(AntiAlias=True, Color=skcol('#9A8FA8', a * k)))


def sticker(x, y, s, k, face='angry', key='stk', col=PINK, dk=PINKDK, label=None, tiara=True):
    """a big face sticker message (her angry Clawd head with a steam puff)"""
    if k <= .02:
        return
    p = backOut(k)
    push()
    translate(x, y)
    scale(p)
    rotate(-.06)
    boilSeed(key)
    paint(rrPts(-s, -s, 2 * s, 2 * s, s * .3), wash='#FFFFFF', ink=INK, sw=1.0)
    miniHead(0, s * .12, s * .62, col, dk, flower=True, face=face, key=key + 'h', tiara=tiara)
    if label:
        text(label, 0, s * .78, s * .26, HOT, stroke='#FFFFFF', strokeW=6, shadow=False)
    pop()


# ------------------------------------------------------------------ suitcase
def suitcase(x, y, s, col='#7FC6E8', key='suit', tilt=0.0, handle=1.0):
    """(x, y) = bottom centre; about 3s wide, 4s tall"""
    push()
    translate(x, y)
    rotate(tilt)
    boilSeed(key)
    for sx_ in (-1, 1):
        G.c.drawCircle(sx_ * 1.0 * s, -.12 * s, .28 * s, skia.Paint(AntiAlias=True, Color=skcol(INK)))
    hy = -4.0 * s - 1.4 * s * handle
    inkLine([[-.7 * s, -4.0 * s], [-.7 * s, hy]], 2.0, '#6A6478', 'ink', 0)
    inkLine([[.7 * s, -4.0 * s], [.7 * s, hy]], 2.0, '#6A6478', 'ink', 0)
    paint(rrPts(-.9 * s, hy - .35 * s, 1.8 * s, .45 * s, .2 * s), wash='#4A4560', ink=INK, sw=.8)
    paint(rrPts(-1.5 * s, -4.1 * s, 3.0 * s, 3.85 * s, .45 * s), wash=col, fill=mixCol(col, INK, .25), fillOp=60, ink=INK, sw=1.1)
    for i in (-1, 0, 1):
        inkLine([[i * .8 * s, -3.8 * s], [i * .8 * s, -.55 * s]], .6, mixCol(col, INK, .35), 'inkfine', 0)
    heart(-.55 * s, -2.9 * s, .38 * s, '#FF8FB0', key=key + 'h', sw=.6)
    paint(starPts(.6 * s, -1.4 * s, .42 * s, .45, 5), wash='#FFE07A', ink=INK, sw=.5)
    pop()


# ------------------------------------------------------------------ the front door (S02)
def hallway(t, doorOpen=0.0, slam=0.0, key='hw', outside=None):
    """wall, door at x 1180-1520 (floor y 860), coat hooks with the deerstalker, shoe rack, mat, plant"""
    gradRect(-200, -200, W + 400, 1100, ['#FFF1E4', '#F8DCCB'])
    for i in range(-4, 40):
        G.c.drawRect(skia.Rect.MakeXYWH(i * 60, -200, 4, 1300), skia.Paint(AntiAlias=True, Color=skcol('#E9B9A6', .35)))
    flatRect(-200, 860, W + 400, 400, '#C99A73')
    for i in range(-2, 30):
        inkLine([[i * 120, 860], [i * 120 - 80, 1100]], .5, '#A97A55', 'inkfine', 0)
    inkLine([[-200, 860], [W + 200, 860]], 1.2, INK, 'ink', 0)
    flatRect(-200, 820, W + 400, 40, '#E7C3AA')
    inkLine([[-200, 820], [W + 200, 820]], .7, INK, 'inkfine', 0)
    # door opening (outside light) and frame
    dx, dy, dw, dh = 1180, 300, 340, 560
    boilSeed(key + 'out')
    gradRect(dx, dy, dw, dh, ['#BFE6F7', '#FFF2C9'])
    for i in range(3):
        puff(dx + 80 + i * 110, dy + 120 + (i % 2) * 60, 16, '#FFFFFF', key=f'{key}pf{i}', ink=False, a=.9)
    flat([[dx, dy + dh - 120], [dx + dw, dy + dh - 160], [dx + dw, dy + dh], [dx, dy + dh]], '#9ED27A')
    if outside:
        G.c.save()
        G.c.clipRect(skia.Rect.MakeXYWH(dx, dy, dw, dh), skia.ClipOp.kIntersect, True)
        outside()
        G.c.restore()
    paint(rectPts(dx - 26, dy - 26, dw + 52, dh + 26), wash=None, ink=INK, sw=1.2)
    paint([[dx - 26, dy - 26], [dx + dw + 26, dy - 26], [dx + dw + 26, dy + dh], [dx + dw, dy + dh], [dx + dw, dy], [dx, dy], [dx, dy + dh], [dx - 26, dy + dh]],
          wash='#FFFFFF', ink=INK, sw=1.0)
    # the door leaf: hinged on the right edge, swings in toward camera (open 0 = shut)
    dk = doorOpen
    lw = dw * (1 - .78 * dk)
    sxs, sys_ = shakeAmt(t, slam, 6) if slam else (0, 0)
    lx0 = dx + dw - lw
    push()
    translate(sxs, 0)
    boilSeed(key + 'door')
    skew = 40 * dk
    leaf = [[lx0, dy - skew * .3], [dx + dw, dy], [dx + dw, dy + dh], [lx0, dy + dh + skew * .3]]
    if dk > .5:
        leaf = [[dx + dw, dy], [dx + dw + lw * .9, dy - skew], [dx + dw + lw * .9, dy + dh + skew], [dx + dw, dy + dh]]
    paint(leaf, wash='#F59AB0', fill='#D8708E', fillOp=60, ink=INK, sw=1.2)
    if dk < .5:
        paint(rrPts(lx0 + lw * .15, dy + 60, lw * .7, 170, 14), wash=None, fill='#D8708E', fillOp=90, ink=INK, sw=.7)
        paint(rrPts(lx0 + lw * .15, dy + 290, lw * .7, 220, 14), wash=None, fill='#D8708E', fillOp=90, ink=INK, sw=.7)
        G.c.drawCircle(lx0 + lw * .12, dy + 300, 14, skia.Paint(AntiAlias=True, Color=skcol('#F2C53D')))
        heart(lx0 + lw / 2, dy + 145, 34, '#FFFFFF', key=key + 'dh', sw=.6, shine=False)
    pop()
    # coat hooks with the deerstalker (疑心病 easter egg) and her pink coat
    boilSeed(key + 'hook')
    paint(rrPts(560, 360, 420, 34, 10), wash='#B98552', ink=INK, sw=.9)
    for hx in (620, 760, 900):
        inkLine([[hx, 394], [hx, 420], [hx + 16, 428]], 2.2, '#5A4A42', 'ink', .3)
    from hl import deerHatAlone
    deerHatAlone(620, 500, 19, key=key + 'deer')
    boilSeed(key + 'coat')
    paint([[760, 420], [700, 470], [690, 640], [830, 640], [820, 470]], wash='#B8AEEA', fill='#8E84CC', fillOp=60, ink=INK, sw=.9, curv=.2)
    for i in range(3):
        G.c.drawCircle(760, 490 + i * 45, 7, skia.Paint(AntiAlias=True, Color=skcol('#6E64B0')))
    # a framed photo of the two of them
    from sets2 import coupleSnap
    push()
    translate(1010, 520)
    rotate(.05)
    boilSeed(key + 'pf')
    paint(rectPts(-80, -90, 160, 170), wash='#FFFDF6', ink=INK, sw=.9)
    coupleSnap(-68, -78, 136, 120)
    pop()
    # shoe rack + shoes, mat, plant, mirror
    boilSeed(key + 'rack')
    paint(rectPts(220, 700, 380, 160), wash='#E8D3B8', fill='#C9A57E', fillOp=60, ink=INK, sw=1.0)
    inkLine([[220, 780], [600, 780]], .8, INK, 'inkfine', 0)
    for i, (sx_, col) in enumerate([(270, HOT), (360, HOT), (460, '#5B7FC4'), (540, '#5B7FC4')]):
        paint(ellPts(sx_, 768, 36, 14, 12), wash=col, ink=INK, sw=.6)
        paint(ellPts(sx_ + 6, 846, 34, 13, 12), wash='#F2C14E' if i < 2 else '#6E9F58', ink=INK, sw=.6)
    boilSeed(key + 'mat')
    paint([[1130, 905], [1580, 905], [1620, 960], [1090, 960]], wash='#F7D36E', fill='#E0A92C', fillOp=60, ink=INK, sw=.9)
    text('HOME', 1355, 932, 30, '#B07C1A', shadow=False)
    boilSeed(key + 'pot')
    paint([[1640, 860], [1760, 860], [1740, 760], [1660, 760]], wash='#E8836B', ink=INK, sw=.9)
    for i in range(6):
        a = -math.pi / 2 + (i - 2.5) * .35
        paint(ellPts(1700 + math.cos(a) * 90, 700 + math.sin(a) * 70 + 40, 26, 62, 12, 0, a + math.pi / 2), wash='#7CC36B', ink=INK, sw=.6)


# ------------------------------------------------------------------ cake slice / strawberry
def strawberry(x, y, s, key='sb'):
    boilSeed(key)
    paint([[x - s, y - s * .3], [x + s, y - s * .3], [x, y + s * 1.2]], wash='#E8394E', fill='#B8243A', fillOp=60, ink=INK, sw=.6, curv=.5)
    for i in range(5):
        G.c.drawCircle(x + (hash1(i * 3.1) - .5) * s, y + hash1(i * 5.7) * s * .6, s * .07, skia.Paint(AntiAlias=True, Color=skcol('#FFE07A')))
    paint([[x - s * .7, y - s * .35], [x, y - s * .7], [x + s * .7, y - s * .35], [x, y - s * .15]], wash='#6E9F58', ink=INK, sw=.5)


def cakeSlice(x, y, s, key='cs', bite=0.0):
    """a wedge of strawberry shortcake; (x, y) = centre of its base"""
    boilSeed(key)
    w, h = 2.4 * s, 1.3 * s
    bt = bite * w * .45
    paint([[x - w / 2 + bt, y], [x + w / 2, y], [x + w / 2, y - h], [x - w / 2 + bt, y - h * .55]], wash='#FFF4D6', fill='#F2D7A0', fillOp=60, ink=INK, sw=.9)
    inkLine([[x - w / 2 + bt, y - h * .3], [x + w / 2, y - h * .5]], 3.2, '#F59AB0', 'ink', .2)
    paint([[x - w / 2 + bt, y - h * .55], [x + w / 2, y - h], [x + w / 2 - .2 * s, y - h - .25 * s], [x - w / 2 + bt - .1 * s, y - h * .62 - .1 * s]],
          wash='#FFFFFF', ink=INK, sw=.8)
    strawberry(x + w * .3, y - h - .45 * s, .42 * s, key=key + 'st')


def rodHook(L=7.0):
    """fishing rod held in the hand: a line along the arm; returns nothing (draws in arm space)"""
    def f(u, sw):
        inkLine([[0, 0], [L * .5 * u, -.15 * u], [L * u, -.5 * u]], sw * 2.0, '#7A5232', 'ink', .4)
        G.c.drawCircle(.6 * u, .1 * u, .5 * u, skia.Paint(AntiAlias=True, Color=skcol('#5A4A42')))
    return f


def fishLine(p0, p1, sag=60, a=1.0):
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + sag
    pts = [p0, [mx, my], p1]
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.0, Color=skcol('#5A5468', .85 * a))
    path = skia.Path()
    path.moveTo(*p0)
    path.quadTo(2 * mx - (p0[0] + p1[0]) / 2, 2 * my - (p0[1] + p1[1]) / 2, *p1)
    G.c.drawPath(path, pa)


# ------------------------------------------------------------------ dusk park (S03 / S04)
def parkDusk(t, key='pk', horizon=760):
    gradRect(-400, -400, W + 800, horizon + 400, ['#F4B8C8', '#FBD9B0', '#FCE9C4'])
    glow(1500, horizon - 120, 520, '#FFE2A0', .55)
    boilSeed(key + 'sun')
    paint(ellPts(1500, horizon - 110, 90, 90, 32), wash='#FFD98A', ink=None)
    for i, (cx, cy, s) in enumerate([(300, 160, 26), (820, 110, 20), (1250, 210, 22), (1780, 130, 18)]):
        puff(cx + 12 * math.sin(t * .3 + i), cy, s, '#FFF1EA', key=f'{key}cl{i}', ink=False, a=.85)
    # distant houses with warm windows
    for i in range(9):
        hx = -120 + i * 250 + (i % 2) * 40
        hh = 150 + 70 * hash1(i * 2.7)
        boilSeed(f'{key}h{i}')
        col = ['#C9A0C0', '#B58CB0', '#D4AFC4'][i % 3]
        paint([[hx, horizon], [hx, horizon - hh], [hx + 90, horizon - hh - 70], [hx + 180, horizon - hh], [hx + 180, horizon]], wash=col, ink=INK, sw=.6, lite=True)
        for r_ in range(2):
            for c_ in range(2):
                on = hash1(i * 5 + r_ * 2 + c_) > .35
                paint(rectPts(hx + 32 + c_ * 74, horizon - hh + 30 + r_ * 56, 40, 34), wash='#FFE3A0' if on else '#8E7298', ink=None)
    # grass ground
    boilSeed(key + 'g')
    pts = [[-400, H + 400], [-400, horizon]]
    for i in range(30):
        x = -400 + i * (W + 800) / 29
        pts.append([x, horizon - 12 * math.sin(i * .7) ** 2])
    pts.append([W + 400, H + 400])
    paint(pts, wash='#A7D88A', fill='#7FB866', fillOp=60, ink=INK, sw=1.0, curv=.3)
    for i in range(40):
        gx = -300 + hash1(i * 1.7) * (W + 600)
        gy = horizon + 30 + hash1(i * 3.3) * 280
        inkLine([[gx, gy], [gx + 6, gy - 16]], .6, '#5E9E4A', 'inkfine', 0)
    for i in range(12):
        fx = -200 + hash1(i * 4.1) * (W + 400)
        fy = horizon + 60 + hash1(i * 6.2) * 240
        for j in range(5):
            a = j / 5 * TAU
            G.c.drawCircle(fx + math.cos(a) * 7, fy + math.sin(a) * 7, 6, skia.Paint(AntiAlias=True, Color=skcol(['#FFFFFF', '#FFD1DC', '#FFF09A'][i % 3])))
        G.c.drawCircle(fx, fy, 4, skia.Paint(AntiAlias=True, Color=skcol('#F2B33D')))


# ------------------------------------------------------------------ jack-in-the-box (S06)
def boxBack(x, y, s, col, key='bx', lid=0.0):
    boilSeed(key + 'b')
    w, h, d = 4 * s, 3 * s, 1.0 * s
    if lid >= .5:
        ly = y - h - d
        paint([[x - w / 2, ly], [x + w / 2, ly], [x + w / 2 + .1 * s, ly - 1.0 * s], [x - w / 2 - .1 * s, ly - 1.0 * s]], wash=mixCol(col, '#FFFFFF', .15), ink=INK, sw=1.0)
    paint([[x - w / 2, y - h], [x + w / 2, y - h], [x + w / 2 - .3 * s, y - h - d], [x - w / 2 + .3 * s, y - h - d]], wash=mixCol(col, '#1C1A2C', .5), ink=INK, sw=1.0)


def boxFront(x, y, s, col, rib, lid=0.0, key='bx'):
    """lid 0 = closed, 1 = flipped open behind the box"""
    boilSeed(key + 'f')
    w, h, d = 4 * s, 3 * s, 1.0 * s
    dk = mixCol(col, INK, .3)
    paint(rectPts(x - w / 2, y - h, w, h), wash=col, fill=dk, fillOp=60, ink=INK, sw=1.2)
    paint(rectPts(x - .3 * s, y - h, .6 * s, h), wash=rib, ink=INK, sw=.8)
    for i in range(5):
        G.c.drawCircle(x - w / 2 + .5 * s + i * .75 * s, y - h * .3 - (i % 2) * .6 * s, .14 * s, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .7)))
    if lid < .5:
        ly = y - h - lid * 2.5 * s
        paint(rectPts(x - w / 2 - .25 * s, ly - .7 * s, w + .5 * s, .8 * s), wash=col, fill=dk, fillOp=50, ink=INK, sw=1.1)
        paint(rectPts(x - .3 * s, ly - .7 * s, .6 * s, .8 * s), wash=rib, ink=None)
        for sg in (-1, 1):
            paint(ellPts(x + sg * .7 * s, ly - 1.0 * s, .7 * s, .4 * s, 12, 0, sg * .3), wash=rib, ink=INK, sw=.7)


def spring(x, y0, y1, w, key='spr'):
    boilSeed(key)
    n = 7
    pts = []
    for i in range(n * 8 + 1):
        k = i / (n * 8)
        pts.append([x + math.sin(k * n * TAU) * w, lerp(y0, y1, k)])
    inkLine(pts, 2.0, '#8C8AA0', 'ink', .3)


# ------------------------------------------------------------------ fairy wings and wand (S07 / S08)
def wings(x, y, u, flap=0.0, a=.85, key='wg'):
    """drawn before her; (x, y) = her ground point"""
    cx, cy = x, y - 6.2 * u
    for sg in (-1, 1):
        for j, (rx, ry, ang, oy) in enumerate([(4.2, 2.6, -.55, -1.0), (3.0, 1.8, .45, 1.3)]):
            boilSeed(f'{key}{sg}{j}')
            fa = ang - .25 * flap * (1 if j == 0 else .6)
            P = ellPts(cx + sg * (4.8 + rx * .7) * u, cy + oy * u, rx * u, ry * u, 28, 0, sg * fa)
            paint(P, wash='#C9ECFF', washOp=235 * a, fill='#8FD0F2', fillOp=110 * a, ink=INK, sw=.8)
            sparkle(cx + sg * (5.6 + rx * .5) * u, cy + oy * u - .6 * u, .5 * u, '#FFFFFF', a)


def wandHook(glowK=1.0):
    def f(u, sw):
        inkLine([[0, 0], [3.4 * u, 0]], sw * 1.6, '#F6CF4E', 'ink', 0)
        if glowK > 0:
            glow(4.0 * u, 0, 3 * u, '#FFF2A8', .6 * glowK)
        paint(starPts(4.0 * u, 0, 1.1 * u, .45, 5), wash='#FFE36E', fill='#F2B33D', fillOp=70, ink=INK, sw=sw * .7)
    return f


def wandTip(x, y, u, o):
    """world position of the star at the end of her right-hand wand (front/q views)"""
    from common import handXY
    hx, hy = handXY(x, y, u, o, 'R')
    a = o.get('aR', .2)
    f = -1 if o.get('flip') else 1
    return hx + f * 4.0 * u * math.cos(a), hy - 4.0 * u * math.sin(a)


def lightBeam(x, top, bottom, w0, w1, a=.45, col='#FFF6C8'):
    flat([[x - w0 / 2, top], [x + w0 / 2, top], [x + w1 / 2, bottom], [x - w1 / 2, bottom]], col, a)
    flat([[x - w0 / 4, top], [x + w0 / 4, top], [x + w1 / 4, bottom], [x - w1 / 4, bottom]], '#FFFFFF', a * .5)


# ------------------------------------------------------------------ flip board (S08)
def flipBoard(x, y, cw, chh, txt, locks, t, key='fb', scr='0123456789', stand=0):
    """tiles centred at (x, y); locks[i] = time tile i locks (scrambles every 3 frames before)"""
    n = len(txt)
    gap = cw * .12
    tw = n * cw + (n - 1) * gap
    boilSeed(key)
    if stand:
        for sg in (-1, 1):
            paint(rectPts(x + sg * tw * .32 - 10, y + chh / 2, 20, stand), wash='#5A5468', ink=INK, sw=.8)
        inkLine([[x - tw * .32, y + chh / 2 + stand * .5], [x + tw * .32, y + chh / 2 + stand * .5]], 1.2, '#5A5468', 'ink', 0)
    paint(rrPts(x - tw / 2 - 30, y - chh / 2 - 30, tw + 60, chh + 60, 18), wash='#3A3550', fill='#2A2640', fillOp=60, ink=INK, sw=1.2)
    for i, ch_ in enumerate(txt):
        tx = x - tw / 2 + i * (cw + gap)
        lk = locks[i]
        if t >= lk - .04:
            c_ = ch_
            pk_ = clamp((t - (lk - .04)) / .12)
        else:
            fi = int(t * 24 / 3)
            pool = scr.replace(ch_, '')
            c_ = pool[int(hash1(fi * 7.3 + i * 3.1) * len(pool)) % len(pool)]
            pk_ = 0
        sc = 1 + .12 * math.sin(pk_ * math.pi) if 0 < pk_ < 1 else 1
        push()
        translate(tx + cw / 2, y)
        scale(sc)
        boilSeed(f'{key}t{i}')
        paint(rrPts(-cw / 2, -chh / 2, cw, chh, 10), wash='#FFF8EE' if pk_ > 0 else '#E4DDEA', ink=INK, sw=.9)
        G.c.drawRect(skia.Rect.MakeXYWH(-cw / 2, -1.5, cw, 3), skia.Paint(AntiAlias=True, Color=skcol('#3A3550', .8)))
        text(c_, 0, 4, chh * .74, HOT if pk_ > 0 else '#5A5468', shadow=False)
        pop()


# ------------------------------------------------------------------ daytime street (S08)
SHOPS = [('奶茶', '#F7A1B6', '#E8476E'), ('花店', '#B8E3C8', '#3FA37A'), ('蛋糕', '#FBE7A1', '#E0A92C'), ('书店', '#BFD8F5', '#5B7FC4')]


def dayStreet(t, key='ds', ground=860):
    gradRect(-400, -400, W + 800, ground + 400, ['#A9DBF5', '#DDF2FB', '#FFF6E2'])
    for i, (cx, cy, s) in enumerate([(220, 120, 24), (760, 80, 18), (1420, 140, 26), (1840, 90, 16)]):
        puff(cx + 10 * math.sin(t * .4 + i), cy, s, '#FFFFFF', key=f'{key}cl{i}', ink=True, a=.95)
    xs = [-140, 330, 800, 1270, 1740]
    for i in range(4):
        x0, x1 = xs[i] + 10, xs[i + 1] - 10
        hgt = [470, 560, 600, 500][i]
        name, col, sign = SHOPS[i]
        boilSeed(f'{key}b{i}')
        paint(rectPts(x0, ground - hgt, x1 - x0, hgt), wash=col, fill=mixCol(col, INK, .2), fillOp=50, ink=INK, sw=1.0)
        for r_ in range(2):
            for c_ in range(3):
                wx = x0 + 40 + c_ * (x1 - x0 - 80) / 3
                wy = ground - hgt + 40 + r_ * 110
                if wy < ground - 300:
                    paint(rectPts(wx, wy, (x1 - x0 - 80) / 3 - 30, 70), wash='#E9F6FF', ink=INK, sw=.6)
                    inkLine([[wx + 12, wy + 50], [wx + 30, wy + 16]], 1.2, '#FFFFFF', 'inkfine', 0)
        # awning
        ay = ground - 290
        n = 8
        aw = (x1 - x0 + 40) / n
        for j in range(n):
            boilSeed(f'{key}aw{i}{j}')
            ax = x0 - 20 + j * aw
            paint([[ax, ay], [ax + aw, ay], [ax + aw, ay + 60], [ax + aw / 2, ay + 80], [ax, ay + 60]], wash=sign if j % 2 == 0 else '#FFFFFF', ink=INK, sw=.6)
        # sign board + shop window
        paint(rrPts(x0 + 40, ay - 90, x1 - x0 - 80, 70, 14), wash='#FFFDF6', ink=INK, sw=.9)
        text(name, (x0 + x1) / 2, ay - 55, 46, sign, shadow=False)
        paint(rectPts(x0 + 30, ay + 100, x1 - x0 - 60, ground - ay - 110), wash='#DDF0FA', fill='#B6DCEF', fillOp=40, ink=INK, sw=.9)
        # things in the window
        if i == 0:
            for j in range(3):
                bobaCup(x0 + 110 + j * 110, ground - 20, 22, key=f'{key}bc{j}')
        elif i == 1:
            for j in range(4):
                bouquet(x0 + 90 + j * 100, ground - 30, 16, key=f'{key}bq{j}', cols=[[['#F59AB0', '#FFD1DC'], ['#FFF09A', '#F7D36E']][j % 2]])
        elif i == 2:
            for j in range(2):
                cakeWhole(x0 + 140 + j * 190, ground - 20, 30, key=f'{key}ck{j}')
        else:
            for j in range(7):
                paint(rectPts(x0 + 70 + j * 46, ground - 150 - (j % 3) * 10, 36, 130 + (j % 3) * 10), wash=['#E8836B', '#7FB8E6', '#F2C14E', '#9ED27A'][j % 4], ink=INK, sw=.6)
    # sidewalk + road
    flatRect(-400, ground, W + 800, 90, '#E9DCCB')
    for i in range(-3, 24):
        inkLine([[i * 100, ground], [i * 100 - 30, ground + 90]], .5, '#C9B8A2', 'inkfine', 0)
    inkLine([[-400, ground], [W + 400, ground]], 1.2, INK, 'ink', 0)
    flatRect(-400, ground + 90, W + 800, 400, '#8A8EA0')
    inkLine([[-400, ground + 90], [W + 400, ground + 90]], 1.0, INK, 'ink', 0)
    for i in range(-2, 12):
        flatRect(i * 260 + 40, ground + 170, 140, 14, '#FFFFFF', .8)
    for i, px in enumerate((300, 790, 1250, 1720)):
        boilSeed(f'{key}pp{i}')
        paint([[px - 34, ground], [px + 34, ground], [px + 44, ground - 60], [px - 44, ground - 60]], wash='#E8836B', ink=INK, sw=.7)
        for j in range(5):
            a = -math.pi / 2 + (j - 2) * .45
            paint(ellPts(px + math.cos(a) * 40, ground - 90 + math.sin(a) * 30, 16, 34, 10, 0, a + math.pi / 2), wash='#7CC36B', ink=INK, sw=.5)


# ------------------------------------------------------------------ gifts and sweets
def bobaCup(x, y, s, key='boba', rot=0.0):
    """(x, y) = bottom centre; ~2s wide, 4s tall"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    inkLine([[.3 * s, -3.6 * s], [.6 * s, -5.0 * s]], 3.4 * s / 20, HOT, 'ink', 0)
    paint([[-1.1 * s, -3.6 * s], [1.1 * s, -3.6 * s], [.85 * s, 0], [-.85 * s, 0]], wash='#E8C9A8', fill='#C9A07A', fillOp=70, ink=INK, sw=.9)
    for i in range(9):
        G.c.drawCircle((-.6 + (i % 4) * .4) * s, (-.35 - (i // 4) * .32) * s, .17 * s, skia.Paint(AntiAlias=True, Color=skcol('#3A2B2B')))
    paint(ellPts(0, -3.6 * s, 1.15 * s, .3 * s, 16), wash='#FFFFFF', ink=INK, sw=.7)
    heart(0, -2.0 * s, .45 * s, '#FFFFFF', key=key + 'h', sw=.5, shine=False)
    pop()


def bouquet(x, y, s, key='bq', cols=None, rot=0.0):
    """(x, y) = bottom of the stems; ~4s tall"""
    cols = cols or [['#F59AB0', '#FFD1DC'], ['#FFF09A', '#F7D36E'], ['#FFFFFF', '#F3EBDC']]
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    for i in range(5):
        a = -math.pi / 2 + (i - 2) * .32
        inkLine([[0, 0], [math.cos(a) * 3.2 * s, -2.2 * s + math.sin(a) * 1.2 * s]], 1.0, '#5E9E4A', 'inkfine', .3)
    for i in range(6):
        a = -math.pi / 2 + (i - 2.5) * .45
        fx, fy = math.cos(a) * 1.7 * s, -3.0 * s + math.sin(a) * .9 * s
        c1, c2 = cols[i % len(cols)]
        for j in range(5):
            b = j / 5 * TAU
            G.c.drawCircle(fx + math.cos(b) * .5 * s, fy + math.sin(b) * .5 * s, .48 * s, skia.Paint(AntiAlias=True, Color=skcol(c1)))
        G.c.drawCircle(fx, fy, .35 * s, skia.Paint(AntiAlias=True, Color=skcol(c2)))
    paint([[-1.2 * s, -1.8 * s], [1.2 * s, -1.8 * s], [.4 * s, .3 * s], [-.4 * s, .3 * s]], wash='#F7C6D2', fill='#E8A0B6', fillOp=60, ink=INK, sw=.8)
    paint(ellPts(0, -.8 * s, .45 * s, .3 * s, 10), wash=HOT, ink=INK, sw=.5)
    pop()


def cakeWhole(x, y, s, key='ck', candle=False):
    """round strawberry cake on a stand; (x, y) = bottom centre"""
    boilSeed(key)
    paint(ellPts(x, y - .1 * s, 3.2 * s, .5 * s, 20), wash='#FFFFFF', ink=INK, sw=.7)
    paint([[x - 2.6 * s, y - .4 * s], [x - 2.6 * s, y - 2.6 * s], [x + 2.6 * s, y - 2.6 * s], [x + 2.6 * s, y - .4 * s]], wash='#FFF4E6', fill='#F2D7C0', fillOp=40, ink=INK, sw=.9)
    inkLine([[x - 2.6 * s, y - 1.5 * s], [x + 2.6 * s, y - 1.5 * s]], 2.6, '#F59AB0', 'ink', 0)
    paint(ellPts(x, y - 2.6 * s, 2.6 * s, .6 * s, 24), wash='#FFFFFF', ink=INK, sw=.8)
    for i in range(5):
        strawberry(x + (i - 2) * 1.0 * s, y - 2.9 * s - (i % 2) * .15 * s, .38 * s, key=f'{key}s{i}')


def friesBox(x, y, s, n=7, key='fr', taken=0):
    """(x, y) = bottom centre; ~3s wide; fries left = n - taken"""
    boilSeed(key)
    left = max(0, n - taken)
    for i in range(n):
        if i >= left:
            continue
        fx = x + (i - (n - 1) / 2) * .38 * s
        ht = (2.2 + .6 * hash1(i * 2.3)) * s
        ang = (i - (n - 1) / 2) * .05
        paint(rectPts(fx - .16 * s, y - 2.0 * s - ht + 1.6 * s, .32 * s, ht), wash='#F7D36E', fill='#E0A92C', fillOp=60, ink=INK, sw=.6)
    paint([[x - 1.5 * s, y - 2.6 * s], [x + 1.5 * s, y - 2.6 * s], [x + 1.1 * s, y], [x - 1.1 * s, y]], wash='#E8394E', fill='#B8243A', fillOp=60, ink=INK, sw=1.0)
    paint([[x - 1.5 * s, y - 2.6 * s], [x, y - 2.1 * s], [x + 1.5 * s, y - 2.6 * s], [x + 1.4 * s, y - 2.2 * s], [x, y - 1.7 * s], [x - 1.4 * s, y - 2.2 * s]], wash='#C82A40', ink=INK, sw=.6)
    heart(x, y - 1.0 * s, .5 * s, '#FFE07A', key=key + 'h', sw=.5, shine=False)


def fry(x, y, s, ang, key='fy'):
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    paint(rectPts(-.16 * s, -1.2 * s, .32 * s, 2.4 * s), wash='#F7D36E', fill='#E0A92C', fillOp=60, ink=INK, sw=.6)
    pop()


def teddy(x, y, s, key='td'):
    """a small plush bear sitting; (x, y) = bottom centre; ~3s wide"""
    boilSeed(key)
    col, dk = '#C99A6B', '#9B6B45'
    for sg in (-1, 1):
        G.c.drawCircle(x + sg * 1.0 * s, y - .35 * s, .55 * s, skia.Paint(AntiAlias=True, Color=skcol(dk)))
    paint(ellPts(x, y - 1.2 * s, 1.3 * s, 1.1 * s, 20), wash=col, fill=dk, fillOp=40, ink=INK, sw=.8)
    for sg in (-1, 1):
        paint(ellPts(x + sg * 1.0 * s, y - 3.6 * s, .5 * s, .5 * s, 12), wash=col, ink=INK, sw=.7)
    paint(ellPts(x, y - 2.8 * s, 1.25 * s, 1.05 * s, 20), wash=col, fill=dk, fillOp=30, ink=INK, sw=.8)
    paint(ellPts(x, y - 2.5 * s, .55 * s, .4 * s, 12), wash='#F2DCC0', ink=None)
    for sg in (-1, 1):
        G.c.drawCircle(x + sg * .45 * s, y - 3.0 * s, .13 * s, skia.Paint(AntiAlias=True, Color=skcol(INK)))
    G.c.drawCircle(x, y - 2.6 * s, .14 * s, skia.Paint(AntiAlias=True, Color=skcol(INK)))
    paint([[x - .5 * s, y - 2.0 * s], [x + .5 * s, y - 2.0 * s], [x, y - 1.7 * s]], wash=HOT, ink=None)


# ------------------------------------------------------------------ paperwork (S10)
def form(x, y, w, h, rot=0.0, crumple=0.0, key='fm', title='改正清单', items=('不许乱发脾气', '不许说拜拜', '少吃一点甜')):
    """a sheet centred at (x, y); crumple 0..1 folds it into a paper ball"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    if crumple < .5:
        k = crumple * 2
        sx_, sy_ = 1 - .5 * k, 1 - .6 * k
        scale(sx_, sy_)
        P = [[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2, h / 2]]
        if k > 0:
            P = [[px + jit(18 * k), py + jit(18 * k)] for px, py in P]
        paint(P, wash='#FFFDF6', ink=INK, sw=1.0)
        if k < .5:
            text(title, 0, -h / 2 + 62, 52, INK, shadow=False, face=WENKAI)
            inkLine([[-w / 2 + 40, -h / 2 + 105], [w / 2 - 40, -h / 2 + 105]], .8, '#C9A0B0', 'inkfine', 0)
            for i, it in enumerate(items):
                yy = -h / 2 + 170 + i * 82
                paint(rectPts(-w / 2 + 44, yy - 18, 34, 34), wash=None, ink=INK, sw=.7)
                text(it, -w / 2 + 100, yy, 36, '#4A4058', align='left', shadow=False, face=WENKAI)
    else:
        r = lerp(w * .35, w * .22, (crumple - .5) * 2)
        P = []
        for i in range(18):
            a = i / 18 * TAU
            rr_ = r * (1 + .12 * math.sin(a * 5 + 1) + .06 * hash1(i))
            P.append([math.cos(a) * rr_, math.sin(a) * rr_])
        paint(P, wash='#FFFDF6', fill='#E0D6C4', fillOp=60, ink=INK, sw=1.0)
        for i in range(5):
            a = hash1(i * 3.3) * TAU
            inkLine([[0, 0], [math.cos(a) * r * .8, math.sin(a) * r * .8]], .6, '#B8AC98', 'inkfine', .3)
    pop()


def stampTool(x, y, s, key='st', col='#D8394E'):
    """a rubber stamp standing on (x, y) = bottom of the rubber"""
    boilSeed(key)
    paint(rectPts(x - 1.3 * s, y - .5 * s, 2.6 * s, .5 * s), wash=col, ink=INK, sw=.8)
    paint(rectPts(x - 1.1 * s, y - 1.1 * s, 2.2 * s, .6 * s), wash='#B98552', ink=INK, sw=.8)
    paint(rectPts(x - .3 * s, y - 2.6 * s, .6 * s, 1.5 * s), wash='#9B6B45', ink=INK, sw=.8)
    paint(ellPts(x, y - 2.9 * s, .75 * s, .55 * s, 14), wash='#B98552', ink=INK, sw=.8)


# ------------------------------------------------------------------ sticker (S11)
def heartSticker(x, y, r, txt, k, rot=-.12, key='hs'):
    if k <= .02:
        return
    p = backOut(k)
    sc = lerp(1.7, 1.0, easeOut(clamp(k * 1.4))) if k < 1 else 1
    push()
    translate(x, y)
    rotate(rot)
    scale(p * sc)
    boilSeed(key)
    paint(heartPts(0, 0, r * 1.08, 26), wash='#FFFFFF', ink=None, curv=.4)
    paint(heartPts(0, 0, r, 26), wash='#FF7FA3', fill=HOT, fillOp=50, ink=INK, sw=1.0, curv=.4)
    text(txt, 0, -r * .05, r * .5, '#FFFFFF', stroke=HOT, strokeW=6, shadow=False)
    pop()


# ------------------------------------------------------------------ cake title (S12)
def cakeTop(cx, cy, r, key='ct'):
    """a big round cake seen from above"""
    boilSeed(key + 'pl')
    paint(ellPts(cx + 14, cy + 22, r * 1.22, r * 1.22, 48), wash=INK, washOp=40, ink=None)
    paint(ellPts(cx, cy, r * 1.2, r * 1.2, 48), wash='#FFFFFF', ink=INK, sw=1.0)
    boilSeed(key)
    paint(ellPts(cx, cy, r, r, 48), wash='#FFF7EC', fill='#F7E3CF', fillOp=50, ink=INK, sw=1.0)
    for i in range(28):
        a = i / 28 * TAU
        paint(ellPts(cx + math.cos(a) * r * .9, cy + math.sin(a) * r * .9, r * .075, r * .075, 10), wash='#FFFFFF', fill='#F3D9DF', fillOp=60, ink=INK, sw=.5)
    for i in range(10):
        a = i / 10 * TAU + .3
        strawberry(cx + math.cos(a) * r * .74, cy + math.sin(a) * r * .74, r * .07, key=f'{key}s{i}')


def pipingBag(x, y, s, ang=-.6, key='pb'):
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    paint([[0, 0], [-1.0 * s, -3.6 * s], [1.0 * s, -3.6 * s]], wash='#FFFFFF', fill='#F3D9DF', fillOp=60, ink=INK, sw=.9)
    paint(rectPts(-1.05 * s, -4.2 * s, 2.1 * s, .7 * s), wash='#F59AB0', ink=INK, sw=.8)
    paint([[-.2 * s, 0], [.2 * s, 0], [0, .5 * s]], wash='#C0C0CC', ink=INK, sw=.6)
    pop()


def credit(x, y, k, lines, key='cr'):
    if k <= .02:
        return
    p = backOut(k)
    push()
    translate(x, y)
    rotate(.06)
    scale(1, p)
    boilSeed(key)
    paint(rrPts(-170, -70, 340, 140, 12), wash='#FFFDF6', ink=INK, sw=.9)
    heart(-130, -40, 16, HOT, key=key + 'h', sw=.4, shine=False)
    for i, ln in enumerate(lines):
        text(ln, 0, -18 + i * 50, 38 if i == 0 else 30, '#C9587E' if i == 0 else '#6A5A70', shadow=False, face=WENKAI)
    pop()


# ------------------------------------------------------------------ palace (S13)
def palace(t, key='pal'):
    gradRect(-400, -400, W + 800, H + 800, ['#FCD3DF', '#F7B8CB'])
    for i in range(-4, 30):
        flatRect(i * 90, -400, 30, 1300, '#FFFFFF', .12)
    for sg in (-1, 1):
        boilSeed(f'{key}dr{sg}')
        x0 = W / 2 + sg * 1100
        x1 = W / 2 + sg * 640
        pts = [[x0, -100], [x1, -100]]
        for i in range(10):
            yy = -100 + i * 100
            pts.append([x1 + sg * (math.sin(i * 1.3) * 14 + (max(0, yy) / H) ** 1.5 * 160), yy])
        pts += [[x0, 1000]]
        paint(pts, wash='#F59AB0', fill='#E06F92', fillOp=60, ink=INK, sw=1.1)
        paint(ellPts(x1 + sg * 120, 520, 30, 18, 12), wash='#F6CF4E', ink=INK, sw=.7)
    from sets2 import fairyLights
    fairyLights(t, 120, W - 120, 70, 60, 18, key=key + 'fl')
    flatRect(-400, 860, W + 800, 400, '#E8A0B6')
    for i in range(-3, 22):
        flatRect(i * 110, 860, 55, 400, '#F2B4C6', .6)
    inkLine([[-400, 860], [W + 400, 860]], 1.2, INK, 'ink', 0)
    boilSeed(key + 'rug')
    paint(ellPts(W / 2, 900, 640, 70, 40), wash='#C8324A', fill='#8E1E35', fillOp=50, ink=INK, sw=1.0)
    paint(ellPts(W / 2, 900, 600, 56, 40), wash=None, ink='#F6CF4E', sw=1.0)


def throneBack(x, y, s, key='thr'):
    """(x, y) = floor point under the seat centre; draw before the sitter"""
    boilSeed(key + 'b')
    pts = [[x - 3.2 * s, y - 2.6 * s], [x - 3.4 * s, y - 8.0 * s], [x - 2.0 * s, y - 9.8 * s], [x, y - 10.6 * s], [x + 2.0 * s, y - 9.8 * s],
           [x + 3.4 * s, y - 8.0 * s], [x + 3.2 * s, y - 2.6 * s]]
    paint(pts, wash='#F6CF4E', fill='#E0A92C', fillOp=70, ink=INK, sw=1.2, curv=.3)
    pts2 = [[px + (x - px) * .12, py + (y - 6 * s - py) * .1] for px, py in pts]
    paint(pts2, wash='#FF7FA3', fill=HOT, fillOp=50, ink=INK, sw=.9, curv=.3)
    heart(x, y - 10.6 * s, .7 * s, HOT, key=key + 'ht', sw=.7)
    for i in range(3):
        for j in range(2):
            G.c.drawCircle(x + (i - 1) * 1.6 * s, y - (5.0 + j * 2.2) * s, .16 * s, skia.Paint(AntiAlias=True, Color=skcol('#FFE07A')))


def throneSeat(x, y, s, key='thr'):
    """the cushion; the sitter's ground point = (x, y - 2.4 s)"""
    boilSeed(key + 's')
    for sg in (-1, 1):
        paint(rectPts(x + sg * 2.9 * s - .3 * s, y - 1.2 * s, .6 * s, 1.2 * s), wash='#E0A92C', ink=INK, sw=.8)
    paint(rrPts(x - 3.6 * s, y - 2.6 * s, 7.2 * s, 1.5 * s, .6 * s), wash='#FF9FBA', fill=HOT, fillOp=50, ink=INK, sw=1.1)
    for sg in (-1, 1):
        paint(rrPts(x + sg * 3.8 * s - .7 * s, y - 4.6 * s, 1.4 * s, 3.4 * s, .6 * s), wash='#F6CF4E', fill='#E0A92C', fillOp=60, ink=INK, sw=1.0)


def placardSign(x, y, w, h, txt, size, rot=0.0, key='ps', col='#FFFDF6', tcol=HOT, stick=True):
    """a hand-held sign, (x, y) = sign centre; stick hangs below"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    if stick:
        paint(rectPts(-10, h / 2 - 6, 20, h * .9), wash='#B98552', ink=INK, sw=.7)
    paint(rrPts(-w / 2, -h / 2, w, h, 16), wash=col, ink=INK, sw=1.1)
    text(txt, 0, 0, size, tcol, shadow=False)
    pop()


# ------------------------------------------------------------------ battery + charging cable (S16)
def batteryPct(x, y, s, frac, blink=0.0, key='bat'):
    boilSeed(key)
    w, h = 2.2 * s, 1.1 * s
    paint(rrPts(x - w / 2, y - h / 2, w, h, .2 * s), wash='#FFFDF6', ink=INK, sw=1.1)
    paint(rrPts(x + w / 2, y - h * .22, .2 * s, h * .44, .06 * s), wash=INK, ink=None)
    col = '#E8574E' if frac < .25 else ('#F2C14E' if frac < .6 else '#7CC36B')
    fw = max(.16 * s, (w - .3 * s) * clamp(frac))
    if blink < .5:
        paint(rrPts(x - w / 2 + .15 * s, y - h / 2 + .15 * s, fw, h - .3 * s, .1 * s), wash=col, ink=None)
    pct = max(1, min(100, int(round(frac * 100))))
    text(f'{pct}%', x - w / 2 - .3 * s, y, s * .62, col if frac < .25 else INK, align='right', stroke='#FFFFFF', strokeW=8, shadow=False)


def cable(p0, p1, sag=120, col=HOT, k=1.0):
    """charging cable from p0 to p1 (drawn up to fraction k)"""
    pts = []
    for i in range(41):
        u_ = i / 40 * k
        x = lerp(p0[0], p1[0], u_)
        y = lerp(p0[1], p1[1], u_) + sag * math.sin(u_ * math.pi)
        pts.append([x, y])
    inkLine(pts, 3.0, col, 'ink', .2)
    return pts[-1]


def plug(x, y, s, ang=0.0, key='plg'):
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    paint(rrPts(-1.2 * s, -.6 * s, 1.4 * s, 1.2 * s, .25 * s), wash='#FFFFFF', ink=INK, sw=.8)
    heart(-.5 * s, 0, .35 * s, HOT, key=key + 'h', sw=.4, shine=False)
    for sg in (-1, 1):
        paint(rectPts(.2 * s, sg * .3 * s - .08 * s, .5 * s, .16 * s), wash='#C0C0CC', ink=INK, sw=.4)
    pop()


# ------------------------------------------------------------------ notifications (S18)
def notif(x, y, w, k, who, msg, avatarFn, off=0.0, key='nt', alpha=1.0):
    """banner card centred at (x + off, y); k = pop-in 0..1"""
    if k <= .02 or alpha <= .02:
        return
    p = backOut(k)
    h = 140
    push()
    translate(x + off, y)
    scale(p)
    rotate(off * .0004)
    boilSeed(key)
    if off > 20:
        for j in range(4):
            inkLine([[-w / 2 - 40 - j * 30, -h / 2 + 20 + j * 30], [-w / 2 - 140 - j * 30 - off * .2, -h / 2 + 20 + j * 30]], 2, '#9A8FA8', 'ink', 0)
    paint(rrPts(-w / 2, -h / 2, w, h, 30), wash='#FFFFFF', washOp=250 * alpha, ink=INK, sw=1.0)
    avatarFn(-w / 2 + 64, 0, 36)
    text(who, -w / 2 + 122, -28, 32, INK, align='left', shadow=False, a=alpha)
    text(msg, -w / 2 + 122, 26, 42, '#4A4058', align='left', shadow=False, a=alpha)
    text('刚刚', w / 2 - 50, -26, 22, '#9A8FA8', shadow=False, a=alpha, face=WENKAI)
    pop()
