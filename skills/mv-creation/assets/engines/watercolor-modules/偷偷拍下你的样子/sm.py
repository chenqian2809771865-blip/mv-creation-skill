# sm.py: 《失眠》 props and sets — yarn, knitting, alarm clock, bedroom (front-facing bed), gift box, cardboard standee,
# rain cloud, apartment facade with switchable windows, windowsill ashtray and smoke. Logical canvas 1920x1080.
import math
from eng import *
import eng
from clawd import *
from props import *
from hl import (windowView, windowFrame, curtain, deskLamp, stars, rain, ripples, deerHatAlone, mug, WENKAI, NIGHT1, NIGHT2)
from sets2 import fairyLights, bookshelf, photoString, wallCalendar, parkBench, seat

YARN, YARNDK, YARNLT = '#E8506A', '#A8324A', '#F7A0AE'
SMOKE = '#C9CCDA'
QUILT, QUILTDK = '#8E86D8', '#6A60B8'


# ================================================================ soft strokes (smoke, glow lines)
def softLine(pts, w, col, a=1.0, blur=0.0, cap=True):
    if len(pts) < 2:
        return
    P = through(pts, 6) if len(pts) >= 3 else pts
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=skcol(col, clamp(a)),
                    StrokeCap=skia.Paint.kRound_Cap if cap else skia.Paint.kButt_Cap, StrokeJoin=skia.Paint.kRound_Join)
    if blur > 0:
        pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    G.c.drawPath(eng._path(P, False), pa)


def strand(pts, col=YARN, sw=2.0, key='str'):
    """a yarn thread: ink line in yarn colour with a lighter core"""
    boilSeed(key)
    inkLine(pts, sw * 1.25, mixCol(col, INK, .35), 'ink', .5)
    softLine(pts, sw * 3.2, col, .95)
    softLine(pts, sw * 1.1, mixCol(col, '#FFFFFF', .45), .7)


# ================================================================ yarn
def yarnBall(x, y, r, col=YARN, dk=YARNDK, key='yb', rot=0.0):
    boilSeed(key)
    paint(ellPts(x, y, r, r, 26), wash=col, fill=dk, fillOp=70, bleed=.06, ink=INK, sw=max(.6, r / 50))
    push()
    translate(x, y)
    rotate(rot)
    for i in range(5):
        a = -1.2 + i * .55
        ry = r * (.95 - .12 * i)
        pts = [[math.cos(a + s * 1.9) * r * .92 * math.cos(s * .9), math.sin(a + s * 1.9) * ry * .9] for s in [-1, -.6, -.2, .2, .6, 1]]
        inkLine(pts, max(.5, r / 70), dk, 'inkfine', .6)
    for i in range(4):
        y0 = -r * .7 + i * r * .45
        hw = math.sqrt(max(0, r * r - y0 * y0)) * .9
        inkLine([[-hw, y0 + r * .1], [0, y0 - r * .12], [hw, y0 + r * .08]], max(.5, r / 80), mixCol(dk, '#FFFFFF', .2), 'inkfine', .6)
    G.c.drawCircle(-r * .35, -r * .4, r * .18, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .35)))
    pop()


def tangle(cx, cy, rx, ry, k, seed=1, col=YARN, sw=2.0, loops=7, ring=False, avoid=None):
    """a scribble of yarn loops; k 0..1 = how much of it is drawn"""
    if k <= .01:
        return
    n = int(30 + 260 * k)
    pts = []
    a1, a2, a3 = 1.0 + hash1(seed) * .6, 1.7 + hash1(seed * 2) * .5, .37 + hash1(seed * 3) * .2
    for i in range(n):
        s = i / 290 * loops * TAU
        rr = (.78 + .22 * math.sin(s * a3 + seed)) if ring else (.55 + .45 * math.sin(s * a3 + seed))
        pts.append([cx + rx * rr * math.sin(s * a1 + seed), cy + ry * rr * math.cos(s * a2 + seed * .5)])
    boilSeed(f'tg{seed}')
    runs, cur = [], []
    for p in pts:
        inside = avoid is not None and ((p[0] - avoid[0]) / avoid[2]) ** 2 + ((p[1] - avoid[1]) / avoid[3]) ** 2 < 1
        if inside:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
        else:
            cur.append(p)
            if len(cur) >= 40:
                runs.append(cur)
                cur = [p]
    if len(cur) > 1:
        runs.append(cur)
    for j, r in enumerate(runs):
        strand(r, col, sw, key=f'tg{seed}_{j}')


def knitPiece(x, y, w, h, col=YARN, dk=YARNDK, key='kp', rot=0.0, title=None, titleK=None, rib=True, titleSize=None):
    """knitted fabric: rounded strip with rows of V stitches; (x, y) = top-left. title = stitched letters (cream)"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    P = rrPts(0, 0, w, h, min(w, h) * .12)
    paint(P, wash=col, fill=dk, fillOp=50, bleed=.04, ink=INK, sw=1.0)
    G.c.save()
    G.c.clipPath(eng._path(P), skia.ClipOp.kIntersect, True)
    cw = 22.0
    rows = int(h / 18) + 1
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2, Color=skcol(dk, .55), StrokeCap=skia.Paint.kRound_Cap)
    pl = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=skcol(YARNLT, .55), StrokeCap=skia.Paint.kRound_Cap)
    for r in range(rows):
        yy = 6 + r * 18
        for c in range(int(w / cw) + 1):
            xx = 4 + c * cw + (cw / 2 if r % 2 else 0) * 0
            G.c.drawLine(xx, yy, xx + cw / 2, yy + 12, pa)
            G.c.drawLine(xx + cw / 2, yy + 12, xx + cw, yy, pa)
            G.c.drawLine(xx + 3, yy + 2, xx + cw / 2, yy + 9, pl)
    G.c.restore()
    if rib:
        for side in (0, 1):
            for i in range(int(w / 16)):
                xx = 8 + i * 16
                yy = 0 if side == 0 else h
                G.c.drawLine(xx, yy - 6, xx + 4, yy + 6, skia.Paint(AntiAlias=True, Color=skcol(dk, .7), StrokeWidth=2))
    if title:
        size = titleSize or h * .62
        chars = list(title)
        widths = [textW(c, size) for c in chars]
        tot = sum(widths) + size * .1 * (len(chars) - 1)
        xx = w / 2 - tot / 2
        for i, (c, cw_) in enumerate(zip(chars, widths)):
            kk = 1 if titleK is None else clamp(titleK[i])
            if kk > .01:
                sc = backOut(kk)
                text(c, xx + cw_ / 2, h / 2, size, '#FFF6EC', stroke=dk, strokeW=size * .11, shadow=False, sc=sc)
                # little stitch dashes over the letter
                boilSeed(f'{key}st{i}')
                for j in range(5):
                    px = xx + cw_ * (.2 + .6 * hash1(i * 7 + j))
                    py = h / 2 + size * (hash1(i * 5 + j * 3) - .5) * .6
                    G.c.drawLine(px - 4, py - 3, px + 4, py + 3, skia.Paint(AntiAlias=True, Color=skcol(dk, .35 * kk), StrokeWidth=1.6))
            xx += cw_ + size * .1
    pop()


def scarfRibbon(C, width, key='sr', col=YARN, dk=YARNDK, fringe=(False, True), sway=0.0):
    """knitted scarf along a centreline C (list of points): V-stitch texture and fringe at the chosen ends"""
    n = len(C) - 1
    L, R = [], []
    for i, (x, y) in enumerate(C):
        j0, j1 = max(0, i - 1), min(n, i + 1)
        dx, dy = C[j1][0] - C[j0][0], C[j1][1] - C[j0][1]
        d = math.hypot(dx, dy) or 1
        nx, ny = -dy / d, dx / d
        L.append([x + nx * width / 2, y + ny * width / 2])
        R.append([x - nx * width / 2, y - ny * width / 2])
    P = L + R[::-1]
    boilSeed(key)
    paint(P, wash=col, fill=dk, fillOp=50, bleed=.04, ink=INK, sw=1.0)
    G.c.save()
    G.c.clipPath(eng._path(P), skia.ClipOp.kIntersect, True)
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.2, Color=skcol(dk, .55), StrokeCap=skia.Paint.kRound_Cap)
    for i in range(1, n):
        x, y = C[i]
        dx, dy = C[i + 1][0] - C[i - 1][0], C[i + 1][1] - C[i - 1][1]
        d = math.hypot(dx, dy) or 1
        tx, ty = dx / d, dy / d
        nx, ny = -ty, tx
        for c in (-1, 0, 1):
            xx, yy = x + nx * c * width * .3, y + ny * c * width * .3
            G.c.drawLine(xx - nx * 8 - tx * 6, yy - ny * 8 - ty * 6, xx, yy + 0, pa)
            G.c.drawLine(xx, yy, xx + nx * 8 - tx * 6, yy + ny * 8 - ty * 6, pa)
    G.c.restore()
    for e, on in ((0, fringe[0]), (n, fringe[1])):
        if not on:
            continue
        a, b = L[e], R[e]
        j = 1 if e == 0 else n - 1
        ox, oy = C[e][0] - C[j][0], C[e][1] - C[j][1]
        d = math.hypot(ox, oy) or 1
        ox, oy = ox / d, oy / d
        for k in range(7):
            fx, fy = lerp(a[0], b[0], (k + .5) / 7), lerp(a[1], b[1], (k + .5) / 7)
            inkLine([[fx, fy], [fx + ox * 26 + math.sin(sway + k) * 4, fy + oy * 26]], 1.6, dk, 'ink', 0)


def scarfHang(px, py, length, width, sway=0.0, key='sh', col=YARN, dk=YARNDK, curl=0.0):
    """a knitted scarf hanging from a point (held), with a soft S-curve and fringe at the bottom"""
    n = 14
    C = [[px + math.sin(i / n * 2.6 + sway) * 26 * (i / n) + curl * (i / n) ** 2 * 120, py + (i / n) * length] for i in range(n + 1)]
    scarfRibbon(C, width, key, col, dk, (False, True), sway)
    return C[-1]


def scarfBand(p0, p1, sag, width, drop0=90, drop1=90, key='sb', col=YARN, dk=YARNDK, sway=0.0):
    """a scarf held between two hands: hangs down a little at each hand, droops between them"""
    C = []
    n = 16
    for i in range(4):
        C.append([p0[0] - 6 + math.sin(sway + i) * 2, p0[1] + drop0 * (1 - i / 3)])
    for i in range(1, n):
        k = i / n
        C.append([lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k) + sag * 4 * k * (1 - k)])
    for i in range(4):
        C.append([p1[0] + 6 + math.sin(sway + i) * 2, p1[1] + drop1 * i / 3])
    scarfRibbon(C, width, key, col, dk, (True, True), sway)


def needle(x0, y0, x1, y1, col='#E8D3A8', knob='#E8574E', sw=1.0):
    inkLine([[x0, y0], [x1, y1]], 3.2 * sw, mixCol(col, INK, .5), 'ink', 0)
    softLine([[x0, y0], [x1, y1]], 6 * sw, col, 1)
    G.c.drawCircle(x0, y0, 8 * sw, skia.Paint(AntiAlias=True, Color=skcol(knob)))
    G.c.drawCircle(x0, y0, 8 * sw, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=skcol(INK, .8)))


def basket(x, y, w, h, key='bk', col='#C9965E'):
    """wicker basket, (x, y) = bottom centre"""
    boilSeed(key)
    P = [[x - w / 2, y - h], [x + w / 2, y - h], [x + w * .42, y], [x - w * .42, y]]
    paint(P, wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=1.0)
    for i in range(1, 7):
        yy = y - h + i * h / 7
        k = i / 7
        hw = lerp(w / 2, w * .42, k)
        inkLine([[x - hw, yy], [x + hw, yy]], .7, mixCol(col, INK, .45), 'inkfine', 0)
    for i in range(1, 10):
        k = i / 10
        inkLine([[lerp(x - w / 2, x + w / 2, k), y - h], [lerp(x - w * .42, x + w * .42, k), y]], .5, mixCol(col, INK, .35), 'inkfine', 0)
    paint(rrPts(x - w / 2 - 8, y - h - 12, w + 16, 22, 10), wash=mixCol(col, '#FFFFFF', .15), ink=INK, sw=.9)


# ================================================================ seven-segment alarm clock
SEG = {'0': 'abcdef', '1': 'bc', '2': 'abged', '3': 'abgcd', '4': 'fgbc', '5': 'afgcd', '6': 'afgedc', '7': 'abc', '8': 'abcdefg', '9': 'abcdfg'}


def segDigit(x, y, w, h, ch, col, a=1.0, th=None):
    th = th or w * .2
    segs = SEG.get(ch, '')
    g = th * .18
    S = dict(a=(x + g, y, x + w - g, y), d=(x + g, y + h, x + w - g, y + h), g=(x + g, y + h / 2, x + w - g, y + h / 2),
             f=(x, y + g, x, y + h / 2 - g), b=(x + w, y + g, x + w, y + h / 2 - g), e=(x, y + h / 2 + g, x, y + h - g), c=(x + w, y + h / 2 + g, x + w, y + h - g))
    off = skia.Paint(AntiAlias=True, Color=skcol(col, .08 * a), StrokeWidth=th, StrokeCap=skia.Paint.kRound_Cap)
    on = skia.Paint(AntiAlias=True, Color=skcol(col, a), StrokeWidth=th, StrokeCap=skia.Paint.kRound_Cap)
    for k, (x0, y0, x1, y1) in S.items():
        G.c.drawLine(x0, y0, x1, y1, on if k in segs else off)


def alarmClock(x, y, s, txt='03:00', key='ac', col='#FF6B5E', colonOn=True, glowK=1.0, shake=0.0, body='#E8E1D2'):
    """(x, y) = bottom centre; s = scale (1 => 300 px wide)"""
    push()
    translate(x, y)
    if shake:
        rotate(shake)
    scale(s)
    boilSeed(key)
    # bells
    for sx in (-1, 1):
        paint(ellPts(sx * 95, -205, 46, 34, 16, 0, sx * .5), wash='#D9B45A', fill='#A8833A', fillOp=60, ink=INK, sw=1.0)
    inkLine([[-60, -232], [0, -250], [60, -232]], 2.2, '#3A3550', 'ink', .5)
    # body
    paint(rrPts(-150, -190, 300, 190, 46), wash=body, fill=mixCol(body, INK, .25), fillOp=60, ink=INK, sw=1.2)
    for sx in (-1, 1):
        paint(rectPts(sx * 100 - 12, -6, 24, 16), wash='#3A3550', ink=INK, sw=.8)
    # screen
    paint(rrPts(-118, -160, 236, 120, 18), wash='#1C1A2C', ink=INK, sw=1.0)
    glow(0, -100, 180, col, .28 * glowK)
    dw, dh = 34, 70
    xs = [-104, -58, None, 24, 70]
    for i, ch in enumerate(txt[:5]):
        if ch == ':':
            if colonOn:
                for yy in (-118, -82):
                    G.c.drawCircle(0, yy, 6, skia.Paint(AntiAlias=True, Color=skcol(col, glowK)))
            continue
        segDigit(xs[i], -135, dw, dh, ch, col, glowK, 10)
    pop()


def nightstand(x, y, w, h, key='ns', col='#7A5A8A'):
    """(x, y) = top-left of the table top"""
    boilSeed(key)
    paint([[x - 12, y], [x + w + 12, y], [x + w + 12, y + 30], [x - 12, y + 30]], wash=mixCol(col, '#FFFFFF', .15), ink=INK, sw=1.0)
    paint(rectPts(x, y + 30, w, h), wash=col, fill=mixCol(col, INK, .35), fillOp=60, ink=INK, sw=1.0)
    for i in range(2):
        paint(rectPts(x + 22, y + 52 + i * (h / 2 - 6), w - 44, h / 2 - 34), wash=mixCol(col, '#FFFFFF', .08), ink=INK, sw=.7, lite=True)
        paint(rrPts(x + w / 2 - 26, y + 52 + i * (h / 2 - 6) + (h / 2 - 34) / 2 - 7, 52, 14, 7), wash='#D9B45A', ink=INK, sw=.5, lite=True)


# ================================================================ the bedroom (front-facing: window behind her, quilt in front)
BED_Y = 820            # top edge of the quilt


def bedBack(t, lampK=1.0, starsK=1.0, moonXY=None, cityK=1.0, wall=('#2B3168', '#3E4482')):
    c1, c2 = wall
    gradRect(-400, -400, W + 800, H + 800, [c1, c2])
    for i in range(-6, 40):
        G.c.drawRect(skia.Rect.MakeXYWH(i * 56, -400, 22, 1100), skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .025)))
    flatRect(-400, 640, W + 800, 200, mixCol(c2, INK, .25))
    G.c.drawLine(-400, 640, W + 400, 640, skia.Paint(AntiAlias=True, Color=skcol(mixCol(c2, '#FFFFFF', .2), .6), StrokeWidth=4))
    wx, wy, ww, wh = 600, 60, 720, 400
    windowView(wx, wy, ww, wh, t, cityK=cityK, starsK=starsK, key='bwv', moonXY=moonXY or (wx + ww * .78, wy + wh * .24))
    windowFrame(wx, wy, ww, wh, '#6B4A3E', key='bwf')
    curtain(wx - 40, wy - 30, wh + 90, -1, 0, '#8C7AA8', key='bcl')
    curtain(wx + ww + 40, wy - 30, wh + 90, 1, 0, '#8C7AA8', key='bcr')
    fairyLights(t, wx - 60, wx + ww + 60, wy - 44, 34, 16, key='bfl')
    bookshelf(70, 150, 360, 450, key='bbs', who='her')
    photoString(t, 1440, 1840, 150, 'her', key='bps')
    wallCalendar(1650, 300, key='bcal')
    # lamp light on the wall
    if lampK > 0:
        glow(1640, 640, 700, '#FFB867', .35 * lampK)
    # headboard + pillow
    boilSeed('hb')
    paint(rrPts(560, 470, 800, 420, 90), wash='#B98AA6', fill='#8A5A7A', fillOp=70, ink=INK, sw=1.2)
    paint(rrPts(600, 510, 720, 340, 70), wash='#CFA2BC', ink=INK, sw=.8, lite=True)
    for i in range(3):
        for j in range(2):
            G.c.drawCircle(700 + i * 260, 590 + j * 120, 7, skia.Paint(AntiAlias=True, Color=skcol('#8A5A7A', .8)))
    boilSeed('pil')
    paint(rrPts(640, 620, 640, 170, 60), wash='#F4EEF8', fill='#C9C0DA', fillOp=60, ink=INK, sw=1.0)


def quilt(t, y=BED_Y, key='q', lump=None, pattern=True):
    """the quilt in front of her, drawn after the sitter. lump = (x, w): a bump where something lies under it"""
    boilSeed(key)
    pts = [[380, y + 30]]
    for i in range(13):
        xx = 380 + i * (1160 / 12)
        yy = y + 10 * math.sin(i * 1.3 + 1) + (14 if i in (0, 12) else 0)
        pts.append([xx, yy])
    pts += [[1560, y + 40], [1600, H + 60], [340, H + 60]]
    paint(pts, wash=QUILT, fill=QUILTDK, fillOp=70, bleed=.05, ink=INK, sw=1.2, curv=.15)
    # folded top band
    band = [[400, y + 6], [1520, y + 6], [1520, y + 84], [400, y + 84]]
    paint([[400 + jit(3), y + 2], [960, y - 6], [1520, y + 2], [1524, y + 80], [960, y + 90], [396, y + 80]], wash='#F4EEF8', fill='#C9C0DA', fillOp=60, ink=INK, sw=1.0, curv=.2)
    if pattern:
        for r in range(3):
            for c in range(9):
                px = 470 + c * 125 + (60 if r % 2 else 0)
                py = y + 150 + r * 95
                if px > 1520:
                    continue
                boilSeed(f'{key}p{r}{c}')
                if (r + c) % 2:
                    paint(starPts(px, py, 16, .45, 5), wash='#FFE9A8', ink=None, lite=True)
                else:
                    paint(ellPts(px, py, 13, 13, 12), wash='#FFE9A8', ink=None, lite=True)
                    paint(ellPts(px + 6, py - 4, 11, 11, 12), wash=QUILT, ink=None, lite=True)
    # side drape shading
    for sx in (390, 1530):
        inkLine([[sx, y + 60], [sx + (-20 if sx < 900 else 20), H]], .8, mixCol(QUILTDK, INK, .3), 'inkfine', .3)


def bedFront(t, clockTxt='03:00', clockS=.62, clockShake=0.0, lampK=1.0, colon=True, basketYarn=True, extra=None):
    """nightstand with lamp and clock on the right"""
    nightstand(1560, 760, 300, 330, key='nst')
    deskLamp(1800, 776, 1.0, lampK, key='nlp', flip=True)
    alarmClock(1660, 778, clockS, clockTxt, key='nclk', colonOn=colon, shake=clockShake)
    if extra:
        extra()


# ================================================================ gift box (front view, a little from above)
def giftBox(x, y, s, lidK=1.0, ribbonK=1.0, bowK=1.0, tagK=0.0, key='gb', col='#7FB8E6', rib='#E8476E', open_=0.0, scarf=False):
    """(x, y) = bottom centre; box 4s wide, 3s tall"""
    push()
    translate(x, y)
    boilSeed(key)
    w, h, d = 4 * s, 3 * s, 1.1 * s
    dk = mixCol(col, INK, .3)
    # back top face (interior visible if lid off)
    top = [[-w / 2, -h], [w / 2, -h], [w / 2 - .25 * s, -h - d], [-w / 2 + .25 * s, -h - d]]
    paint(top, wash=mixCol(col, '#1C1A2C', .45), ink=INK, sw=1.0)
    if scarf:
        knitPiece(-w / 2 + .35 * s, -h - d + .15 * s, w - .7 * s, d * .9, key=key + 'sc', rib=False)
    paint(rectPts(-w / 2, -h, w, h), wash=col, fill=dk, fillOp=60, ink=INK, sw=1.2)
    if ribbonK > 0:
        rh = h * ribbonK
        paint(rectPts(-.3 * s, -rh, .6 * s, rh), wash=rib, ink=INK, sw=.8)
    if lidK > 0:
        ly = lerp(-h - 3.5 * s, -h, easeOut(lidK)) - open_ * 2 * s
        a = clamp(lidK * 3)
        lid = [[-w / 2 - .25 * s, ly + .15 * s], [w / 2 + .25 * s, ly + .15 * s], [w / 2 + .25 * s, ly - .65 * s], [-w / 2 - .25 * s, ly - .65 * s]]
        paint([[-w / 2 - .25 * s, ly - .65 * s], [w / 2 + .25 * s, ly - .65 * s], [w / 2, ly - .65 * s - d], [-w / 2, ly - .65 * s - d]],
              wash=mixCol(col, '#FFFFFF', .2), washOp=int(255 * a), ink=INK, sw=1.0)
        paint(lid, wash=col, washOp=int(255 * a), fill=dk, fillOp=40, ink=INK, sw=1.0)
        if ribbonK > 0:
            paint(rectPts(-.3 * s, ly - .65 * s, .6 * s, .8 * s), wash=rib, ink=INK, sw=.7)
            paint([[-.3 * s, ly - .65 * s], [.3 * s, ly - .65 * s], [.22 * s, ly - .65 * s - d], [-.22 * s, ly - .65 * s - d]], wash=rib, ink=INK, sw=.6)
        if bowK > 0:
            b = backOut(bowK)
            by = ly - .65 * s - d * .5
            for sx in (-1, 1):
                paint([[0, by], [sx * 1.2 * s * b, by - .9 * s * b], [sx * 1.4 * s * b, by - .1 * s * b]], wash=rib, fill=mixCol(rib, INK, .3), fillOp=60, ink=INK, sw=.9, curv=.35)
                paint([[0, by], [sx * .5 * s * b, by + .9 * s * b], [sx * .9 * s * b, by + .7 * s * b]], wash=rib, ink=INK, sw=.8, curv=.2)
            paint(ellPts(0, by, .28 * s * b, .24 * s * b, 12), wash=mixCol(rib, INK, .15), ink=INK, sw=.8)
    if tagK > 0:
        k = backOut(tagK)
        push()
        translate(w / 2 - .2 * s, -h * .55)
        rotate(.25 * math.sin(G.T * 3) * .3 + .15)
        scale(k)
        inkLine([[0, 0], [.4 * s, .5 * s]], 1.0, INK, 'inkfine', 0)
        paint([[.2 * s, .5 * s], [2.4 * s, .5 * s], [2.4 * s, 1.6 * s], [.2 * s, 1.6 * s], [-.15 * s, 1.05 * s]], wash='#FFF6E2', ink=INK, sw=.9)
        text('给你♥', 1.3 * s, 1.05 * s, .55 * s, '#C9587E', face=WENKAI, shadow=False)
        pop()
    pop()


# ================================================================ cardboard standee of him
def standee(x, y, u, flip=0.0, o=None, key='sd'):
    """flat cardboard him on a wooden strut. flip 0..1 turns it round (0 = front, 1 = back)."""
    ang = flip * math.pi
    cs = math.cos(ang)
    push()
    translate(x, y)
    scale(max(.02, abs(cs)), 1)
    boilSeed(key)
    outline = rrPts(-6.0 * u, -9.0 * u, 12.0 * u, 9.1 * u, 1.6 * u)
    if cs > 0:
        paint(outline, wash='#FFFDF6', ink=INK, sw=1.1)
        d = dict(o or {})
        d.setdefault('noShadow', True)
        d.setdefault('lite', True)
        him(0, -.4 * u, u * .98, d)
        G.c.drawLine(-5.6 * u, -1.0 * u, 5.6 * u, -1.0 * u, skia.Paint(AntiAlias=True, Color=skcol('#C9B08F', .5), StrokeWidth=2))
    else:
        paint(outline, wash='#C9A27A', fill='#9A7350', fillOp=70, ink=INK, sw=1.1)
        for i in range(5):
            yy = -8 * u + i * 1.7 * u
            G.c.drawLine(-5.6 * u, yy, 5.6 * u, yy, skia.Paint(AntiAlias=True, Color=skcol('#8A6448', .35), StrokeWidth=2))
        paint(rectPts(-.4 * u, -7 * u, .8 * u, 7 * u), wash='#8A6448', ink=INK, sw=.8)
        text('纸板', 0, -4.6 * u, 1.3 * u, '#6B4A33', face=WENKAI, shadow=False)
    pop()
    # base
    boilSeed(key + 'b')
    paint(rectPts(x - 2.6 * u, y - .3 * u, 5.2 * u, .5 * u), wash='#9A7350', ink=INK, sw=.8)


# ================================================================ a personal rain cloud
def rainCloud(x, y, s, t, key='rc', zap=0.0, rainA=.8, w=None):
    w = w or 2.6 * s
    # rain under it
    step = math.floor(t * 12) / 12
    p = skia.Paint(AntiAlias=True, Color=skcol('#4F64A0', rainA), StrokeWidth=3.4, StrokeCap=skia.Paint.kRound_Cap)
    for i in range(18):
        h1 = hash1(i * 1.7 + 3)
        yy = (h1 * 400 + step * 900) % 420
        xx = x - w * .8 + (i / 17) * w * 1.6
        G.c.drawLine(xx, y + .3 * s + yy, xx - 8, y + .3 * s + yy + 52, p)
    c = []
    for i in range(44):
        a = i / 44 * TAU
        up = math.sin(a) < 0
        r = 1 + .32 * abs(math.sin(a * 3)) ** .6 if up else 1
        c.append([x + math.cos(a) * w * (r * .92 if up else 1), y - .1 * s + math.sin(a) * (1.0 if up else .5) * s * r])
    boilSeed(key)
    paint(c, wash='#8F93A8', fill='#5E6280', fillOp=80, bleed=.08, ink=INK, sw=1.1, curv=.4)
    # sulky face
    for sx in (-1, 1):
        inkLine([[x + sx * .55 * s - .18 * s, y - .25 * s], [x + sx * .55 * s + .18 * s, y - .22 * s]], 1.2, INK, 'ink', 0)
    if zap > .01:
        k = zap
        zz = [[x + .3 * s, y + .4 * s], [x - .1 * s, y + 1.1 * s], [x + .25 * s, y + 1.1 * s], [x - .2 * s, y + 1.9 * s]]
        glow(x, y + 1.2 * s, 2.4 * s, '#FFF2A0', .6 * k)
        inkLine(zz, 4 * k, '#FFE24A', 'ink', 0)


# ================================================================ apartment facade with switchable windows
def facade2(t, lit, herLit=1.0, key='fac2', winX=960, winY=520, winW=300, winH=330, inside=None, moonXY=(1500, -900), moonVeil=0.0, eyesK=0.0, eyesBlink=0.0, roofY=-300):
    """lit(r, c) -> 0..1 for each other window. her window at (r, c) = (0, 2)."""
    gradRect(-1400, -1600, W + 2800, 1700 + roofY, ['#0B0E2E', '#161B48', '#283070'])
    stars(t, 23, 140, -1200, -1500, W + 1200, roofY - 20, .9, 2.8)
    mx, my = moonXY
    glow(mx, my, 260, '#E8E4FF', .55 * (1 - .6 * moonVeil))
    boilSeed(key + 'moon')
    paint(ellPts(mx, my, 48, 48, 24), wash='#FFF8E4', ink=None)
    boilSeed(key)
    gradRect(-1400, roofY, W + 2800, 2400, ['#363E7C', '#232960'])
    flatRect(-1400, roofY - 26, W + 2800, 30, '#2A3068')
    inkLine([[-1400, roofY - 26], [W + 1400, roofY - 26]], 1.2, INK, 'ink', 0)
    rows = [r for r in range(-3, 4) if winY - winH / 2 + r * (winH + 110) > roofY + 30]
    for r in rows:
        yslab = winY - winH / 2 + r * (winH + 110) - 55
        flatRect(-1400, yslab - 8, W + 2800, 16, '#252A5E')
    cols = ['#FFCF85', '#FFB98A', '#FFE2A0']
    for r in rows:
        for c in range(-6, 11):
            x = winX - winW / 2 + (c - 2) * (winW + 120)
            y = winY - winH / 2 + r * (winH + 110)
            if c == 2 and r == 0:
                continue
            on = clamp(lit(r, c))
            boilSeed(f'{key}w{r}{c}')
            col = cols[(c + r) % 3]
            paint(rectPts(x, y, winW, winH), wash=mixCol('#171B48', col, on), washOp=235, ink=INK, sw=.8, lite=True)
            if on > .02:
                glow(x + winW / 2, y + winH / 2, winW * .75, col, .22 * on)
                for s_ in (-1, 1):
                    cx_ = x + winW / 2 + s_ * winW * .36
                    paint(rectPts(cx_ - winW * .14, y + 6, winW * .28, winH - 12), wash='#C98A7A' if (c + r) % 2 else '#8A9AC8', washOp=int(200 * on), ink=None, lite=True)
            G.c.drawLine(x + winW / 2, y, x + winW / 2, y + winH, skia.Paint(AntiAlias=True, Color=skcol('#0E1030', .85), StrokeWidth=5))
            G.c.drawLine(x, y + winH * .4, x + winW, y + winH * .4, skia.Paint(AntiAlias=True, Color=skcol('#0E1030', .85), StrokeWidth=5))
            paint(rectPts(x - 16, y + winH, winW + 32, 16), wash='#454C88', ink=INK, sw=.6, lite=True)
            if hash1(c * 3.3 + r * 1.7) < .22:
                paint(rectPts(x + winW - 90, y + winH + 16, 80, 54), wash='#6E76A8', ink=INK, sw=.6, lite=True)
    x, y = winX - winW / 2, winY - winH / 2
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(x, y, winW, winH))
    gradRect(x, y, winW, winH, [mixCol('#0E1030', '#FFD594', herLit), mixCol('#0E1030', '#F2A96A', herLit)])
    if inside:
        inside(x, y, winW, winH)
    for s_ in (-1, 1):
        cx_ = x + winW / 2 + s_ * winW * .42
        paint(rectPts(cx_ - winW * .1, y, winW * .2, winH), wash=mixCol('#2A2448', '#E8B6A8', herLit), washOp=220, ink=None, lite=True)
    if eyesK > .01:
        for sx in (-1, 1):
            hgt = 16 * (1 - eyesBlink)
            G.c.drawRoundRect(skia.Rect.MakeXYWH(x + winW / 2 + sx * 26 - 6, y + winH * .55 - hgt / 2, 12, max(2, hgt)), 6, 6,
                              skia.Paint(AntiAlias=True, Color=skcol('#FFFDF6', eyesK)))
            glow(x + winW / 2 + sx * 26, y + winH * .55, 30, '#FFFDF6', .5 * eyesK)
    G.c.restore()
    glow(winX, winY, winW * 1.1, '#FFC976', .35 * herLit)
    windowFrame(x, y, winW, winH, '#7A5A4E', bars=False, key=key + 'f')


# ================================================================ windowsill (interior) with ashtray and smoke
def ashtray(x, y, s, key='at', ember=1.0, t=0.0):
    """(x, y) = centre of the dish rim on the sill"""
    boilSeed(key)
    paint(ellPts(x, y + .25 * s, 2.3 * s, .75 * s, 24), wash='#7E8AA8', fill='#4E5878', fillOp=70, ink=INK, sw=1.0)
    paint(ellPts(x, y, 2.3 * s, .6 * s, 24), wash='#AEB8D0', ink=INK, sw=1.0)
    paint(ellPts(x, y + .05 * s, 1.6 * s, .38 * s, 20), wash='#4A4E66', ink=None)
    for sx in (-1, 1):
        paint(ellPts(x + sx * 2.1 * s, y - .02 * s, .32 * s, .16 * s, 10), wash='#6A7392', ink=None)
    # the cigarette resting on the rim
    x0, y0 = x + .4 * s, y - .05 * s
    x1, y1 = x + 2.7 * s, y - .55 * s
    softLine([[x0, y0], [x1, y1]], .34 * s, '#F6F2EA', 1)
    fx, fy = lerp(x0, x1, .72), lerp(y0, y1, .72)
    softLine([[fx, fy], [x1, y1]], .36 * s, '#E3A25E', 1)
    inkLine([[x0, y0 - .17 * s], [x1, y1 - .17 * s]], .7, INK, 'inkfine', 0)
    inkLine([[x0, y0 + .17 * s], [x1, y1 + .17 * s]], .7, INK, 'inkfine', 0)
    if ember > 0:
        fl = .8 + .2 * math.sin(t * 13)
        glow(x0, y0, .9 * s, '#FF7A3A', .9 * ember * fl)
        G.c.drawCircle(x0, y0, .18 * s, skia.Paint(AntiAlias=True, Color=skcol('#FF8A4A', ember)))
    G.c.drawCircle(x0 - .05 * s, y0, .2 * s, skia.Paint(AntiAlias=True, Color=skcol('#8E8E96', .9)))
    return x0, y0


def lighter(x, y, s, key='lt', col='#4E9AD8'):
    boilSeed(key)
    paint(rrPts(x - .5 * s, y - 1.7 * s, 1.0 * s, 1.7 * s, .2 * s), wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=.9)
    paint(rectPts(x - .45 * s, y - 2.1 * s, .9 * s, .45 * s), wash='#C9CCD6', ink=INK, sw=.8)


def smokeCurl(t, x0, y0, seed, age, rise=320, sway=60, w=10, a=.55, life=3.0, col=SMOKE):
    """one rising wisp, born `age` seconds ago at (x0, y0)"""
    if age < 0 or age > life:
        return
    k = age / life
    n = 18
    head = rise * (.25 + .75 * easeOut(k))
    pts = []
    for i in range(n + 1):
        s = i / n
        yy = y0 - head * s
        ph = seed * 2.1 + s * 4.2 - t * 1.6
        xx = x0 + math.sin(ph) * sway * s * (.4 + k) + math.sin(seed * 5 + s * 9 - t * 2.3) * 10 * s
        pts.append([xx, yy])
    fade = (1 - k) ** 1.3 * clamp(age / .15)
    softLine(pts, w * (1 + 1.8 * k), col, a * fade, blur=w * .6)
    softLine(pts, w * .45, '#F2F3F8', a * .6 * fade, blur=2)


def smokeRing(t, x, y, age, r=40, a=.6, life=1.6):
    if age < 0 or age > life:
        return
    k = age / life
    rr = r * (1 + 1.6 * easeOut(k))
    yy = y - 240 * easeOut(k)
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=10 * (1 + k), Color=skcol(SMOKE, a * (1 - k)))
    pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6 + 6 * k))
    G.c.drawOval(skia.Rect.MakeXYWH(x - rr, yy - rr * .45, 2 * rr, rr * .9), pa)


def smokeHim(t, x, y, u, form=1.0, spread=0.0, blink=0.0, a=.75, seed=3):
    """his outline drawn in smoke. form 0..1 = how much of the outline is there; spread 0..1 = drifting apart"""
    if form <= .01 or a <= .01:
        return

    def wob(p, i):
        s = spread
        ph = seed + i * .37
        return [p[0] + math.sin(t * 2.0 + ph) * (4 + 70 * s) + (hash1(i * 3.3) - .5) * 160 * s,
                p[1] + math.cos(t * 1.7 + ph) * (4 + 40 * s) - 260 * s * (.4 + hash1(i * 1.9))]
    # body outline (rounded rectangle path)
    P = []
    L, R, T, Bt = -5 * u, 5 * u, -8 * u, -2 * u
    for i in range(48):
        k = i / 48
        if k < .25:
            p = [lerp(L, R, k / .25), T]
        elif k < .5:
            p = [R, lerp(T, Bt, (k - .25) / .25)]
        elif k < .75:
            p = [lerp(R, L, (k - .5) / .25), Bt]
        else:
            p = [L, lerp(Bt, T, (k - .75) / .25)]
        P.append([x + p[0], y + p[1]])
    m = int(len(P) * clamp(form))
    Q = [wob(p, i) for i, p in enumerate(P[:m + 1])]
    if form >= .999:
        Q.append(Q[0])
    softLine(Q, 26, SMOKE, a * .45, blur=14)
    softLine(Q, 9, '#E6E8F0', a * .7, blur=3)
    # legs and arms
    if form > .6:
        ka = (form - .6) / .4
        for i, lx in enumerate((-4, -2, 1.5, 3.5)):
            L_ = [wob([x + lx * u, y - 2 * u], 60 + i), wob([x + lx * u, y - .2 * u], 70 + i)]
            softLine(L_, 12, SMOKE, a * .55 * ka, blur=6)
        for sx in (-1, 1):
            A_ = [wob([x + sx * 5 * u, y - 4.6 * u], 80 + sx), wob([x + sx * 7 * u, y - 4.2 * u], 90 + sx)]
            softLine(A_, 12, SMOKE, a * .55 * ka, blur=6)
    # eyes
    if form > .8:
        ke = (form - .8) / .2 * (1 - spread)
        for sx in (-1, 1):
            hh = 1.3 * u * (1 - blink) + 2
            ex, ey = wob([x + sx * 2.3 * u, y - 5.6 * u], 100 + sx)
            G.c.drawRoundRect(skia.Rect.MakeXYWH(ex - .3 * u, ey - hh / 2, .6 * u, hh), .3 * u, .3 * u,
                              skia.Paint(AntiAlias=True, Color=skcol('#F2F3F8', a * ke)))


# ================================================================ night park background
def nightPark(t, key='np', lampOn=1.0, horizon=700):
    gradRect(-600, -600, W + 1200, horizon + 600, ['#10143A', '#1E2457', '#3E3F86'])
    stars(t, 31, 60, -500, -500, W + 500, horizon - 250, .9, 2.6)
    glow(1580, 170, 200, '#E8E4FF', .55)
    boilSeed(key + 'm')
    paint(ellPts(1580, 170, 42, 42, 24), wash='#FFF8E4', ink=None)
    push()
    translate(0, horizon - 640 + 40)
    scale(1, .55)
    city(t, .9, key=key + 'c', col='#2A2D66', win='#FFD98A')
    pop()
    boilSeed(key + 'g')
    paint([[-600, horizon], [W + 600, horizon - 10], [W + 600, H + 600], [-600, H + 600]], wash='#2E4A4E', fill='#22383E', fillOp=60, ink=INK, sw=1.0)
    for i in range(30):
        gx = -300 + hash1(i * 2.7) * (W + 600)
        gy = horizon + 30 + hash1(i * 5.1) * 330
        inkLine([[gx, gy], [gx - 6, gy - 18]], .7, '#4E7A6A', 'inkfine', 0)
        inkLine([[gx + 8, gy], [gx + 10, gy - 14]], .7, '#4E7A6A', 'inkfine', 0)
