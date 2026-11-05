# bsc.py: props and sets for 《白山茶》 — night flower stall with the title sign, suitcase + luggage tag, paper islands,
# polaroid, desk with drawer, cork board + letters, paper-cup phone, rooftops, tear-off calendar, heart balloon, stage spotlight.
import math
from eng import *
import eng
from daw import line, rrect, _pa, camellia, rose, petal, icoHeart, pixelDust, splash
from hl import stars


def nightSky(x0=-300, y0=-300, w=W + 600, h=H + 600, cols=('#141A44', '#2A2F66', '#4A3F7A')):
    gradRect(x0, y0, w, h, list(cols))


def stringLights(pts, t, on=1.0, key='sl', col='#FFD98A', seed=0):
    P = through(pts, 8) if len(pts) > 2 else pts
    boilSeed(key)
    inkLine(pts, 1.0, '#2A2440', 'inkfine', .5)
    n = len(P)
    for i in range(0, n, 3):
        x, y = P[i]
        tw = .65 + .35 * math.sin(t * 5 + i * 1.7 + seed)
        a = on * tw
        G.c.drawCircle(x, y + 9, 11, _pa(mixCol('#4A4060', col, on), 1))
        G.c.drawCircle(x, y + 9, 11, _pa(INK, .8, 1.5))
        if a > .02:
            glow(x, y + 9, 46, col, .6 * a)


# ------------------------------------------------------------------ the flower stall + its title sign
def bucket(x, y, s, kind='cam', key='bk', n=4, wilt=0.0, empty=False):
    """metal bucket standing on (x, y); s = bucket height"""
    boilSeed(key)
    if not empty:
        for i in range(n):
            fx = x + (i - (n - 1) / 2) * s * .32
            fy = y - s * (1.25 + .18 * math.sin(i * 2.1))
            inkLine([[fx, fy], [x + (fx - x) * .3, y - s * .6]], 1.6, '#3F6E3A', 'ink', .3)
            if kind == 'cam':
                camellia(fx, fy, s * .26, 1.0, wilt=wilt, key=f'{key}c{i}')
            else:
                rose(fx, fy, s * .2, key=f'{key}r{i}')
    paint([[x - s * .42, y - s * .72], [x + s * .42, y - s * .72], [x + s * .34, y], [x - s * .34, y]], wash='#9AA6B8', fill='#6A7488',
          fillOp=80, ink=INK, sw=1.1)
    line(x - s * .4, y - s * .6, x + s * .4, y - s * .6, '#C8D0DC', .8, 2)


def titleSign(x, y, w, h, titleK=None, light=1.0, sway=0.0, key='sign', title='白山茶', posts=0):
    """wooden sign centred at (x, y): hangs on chains, or (posts > 0) stands on two posts of that length.
    titleK = per-char landing (None = shown)."""
    push()
    piv = y + h / 2 + posts if posts else y - h / 2 - 70
    translate(x, piv)
    rotate(sway)
    translate(-x, -piv)
    for s in (-1, 1):
        if posts:
            boilSeed(key + 'post%d' % s)
            paint(rectPts(x + s * w * .3 - 9, y + h / 2 - 4, 18, posts + 8), wash='#6A4A3A', ink=INK, sw=.9)
        else:
            line(x + s * w * .32, y - h / 2 - 70, x + s * w * .32, y - h / 2, '#3A3550', 1, 3)
    if light > .01:
        glow(x, y, w * .75, '#FFD98A', .45 * light)
    boilSeed(key)
    paint(rrPts(x - w / 2, y - h / 2, w, h, 18), wash='#E9D3A8', fill='#B98A55', fillOp=80, ink=INK, sw=1.6)
    paint(rrPts(x - w / 2 + 12, y - h / 2 + 12, w - 24, h - 24, 12), ink='#8A5E34', sw=1.0)
    camellia(x - w / 2 + h * .34, y + 2, h * .2, 1.0, key=key + 'cm')
    rose(x + w / 2 - h * .34, y - h * .06, h * .14, key=key + 'rs', stem=h * .2)
    chars = list(title)
    size = h * .56
    gap = size * 1.0
    x0 = x - gap * (len(chars) - 1) / 2
    for i, ch in enumerate(chars):
        k = 1 if titleK is None else titleK[i]
        if k <= .01:
            continue
        sc = backOut(clamp(k))
        text(ch, x0 + i * gap, y - 4 - 22 * (1 - clamp(k * 1.4)), size, '#5A2E1E', stroke='#FFF4DC', strokeW=size * .1, shadow=False,
             a=clamp(k * 2), sc=sc)
    text('花 坊', x, y + h * .36, h * .14, '#8A5E34', shadow=False, a=.9)
    pop()


def flowerStall(t, x, y, w, lights=1.0, key='fs', titleK=None, signSway=0.0, emptyBuckets=False):
    """front view stall; (x, y) = ground centre. returns sign centre."""
    top = y - 560
    # posts
    for s in (-1, 1):
        boilSeed(key + 'p%d' % s)
        paint(rectPts(x + s * w / 2 - 14, top + 70, 28, 490), wash='#6A4A3A', ink=INK, sw=1.0)
    # back wall shelves with pots
    flatRect(x - w / 2 + 14, top + 150, w - 28, 260, '#2E2A50', .9)
    for j in range(2):
        yy = top + 260 + j * 120
        line(x - w / 2 + 14, yy, x + w / 2 - 14, yy, '#6A4A3A', 1, 6)
        for i in range(7):
            px = x - w / 2 + 70 + i * (w - 140) / 6
            boilSeed(f'{key}pot{j}{i}')
            paint([[px - 22, yy - 40], [px + 22, yy - 40], [px + 16, yy], [px - 16, yy]], wash='#C8704E', ink=INK, sw=.8)
            if (i + j) % 3 == 0:
                rose(px, yy - 62, 14, key=f'{key}pr{j}{i}')
            elif (i + j) % 3 == 1:
                camellia(px, yy - 62, 18, 1.0, key=f'{key}pc{j}{i}')
            else:
                paint(ellPts(px, yy - 58, 26, 20, 14), wash='#6E9F58', ink=INK, sw=.7)
    # awning (scalloped stripes)
    boilSeed(key + 'aw')
    aw = [[x - w / 2 - 60, top + 150], [x - w / 2 + 20, top], [x + w / 2 - 20, top], [x + w / 2 + 60, top + 150]]
    paint(aw, wash='#F4F0E8', ink=INK, sw=1.4)
    n = 10
    for i in range(n):
        if i % 2:
            continue
        a0, a1 = i / n, (i + 1) / n
        P = [[lerp(x - w / 2 + 20, x + w / 2 - 20, a0), top], [lerp(x - w / 2 + 20, x + w / 2 - 20, a1), top],
             [lerp(x - w / 2 - 60, x + w / 2 + 60, a1), top + 150], [lerp(x - w / 2 - 60, x + w / 2 + 60, a0), top + 150]]
        paint(P, wash='#5FA88A', ink=None)
    paint(aw, ink=INK, sw=1.4)
    for i in range(n):
        cx = lerp(x - w / 2 - 60, x + w / 2 + 60, (i + .5) / n)
        r = (w + 120) / n / 2
        boilSeed(f'{key}sc{i}')
        paint(ellPts(cx, top + 150, r, r * .55, 16), wash='#5FA88A' if i % 2 == 0 else '#F4F0E8', ink=INK, sw=1.0)
    # counter
    boilSeed(key + 'ct')
    paint(rectPts(x - w / 2 + 10, y - 190, w - 20, 190), wash='#8A5E44', fill='#5A3A2A', fillOp=70, ink=INK, sw=1.3)
    paint(rectPts(x - w / 2 - 10, y - 214, w + 20, 30), wash='#B07A54', ink=INK, sw=1.2)
    for i in range(5):
        bucket(x - w / 2 + 110 + i * (w - 220) / 4, y - 214, 120, 'cam' if i % 2 == 0 else 'rose', key=f'{key}b{i}',
               empty=emptyBuckets and i != 2)
    stringLights([[x - w / 2 - 50, top + 175], [x, top + 215], [x + w / 2 + 50, top + 175]], t, lights, key=key + 'sl')
    sx, sy = x, top - 125
    titleSign(sx, sy, 500, 170, titleK=titleK, light=lights, sway=signSway, key=key + 'sign', posts=46)
    return sx, sy


# ------------------------------------------------------------------ suitcase + tag
def suitcase(x, y, w, h, lid=0.0, key='suit', col='#C86A6A', dk='#8E3E48', inside=None):
    """front view; (x, y) = bottom centre. lid 0 = closed, 1 = fully open (lid flips up behind)."""
    boilSeed(key)
    if lid > .01:
        lh = h * .9 * lid
        paint(rrPts(x - w / 2, y - h - lh, w, lh + 10, 14), wash=mixCol(col, '#FFFFFF', .1), fill=dk, fillOp=60, ink=INK, sw=1.3)
        flatRect(x - w / 2 + 14, y - h - lh + 14, w - 28, lh - 14, '#F4D8D8', .9)
    paint(rrPts(x - w / 2, y - h, w, h, 16), wash=col, fill=dk, fillOp=70, ink=INK, sw=1.4)
    if lid > .01:
        flatRect(x - w / 2 + 14, y - h + 10, w - 28, h * .35, '#E8C0C0', 1)
        if inside:
            inside()
    for s in (-1, 1):
        paint(rectPts(x + s * w * .3 - 10, y - h, 20, h), wash=dk, ink=INK, sw=.8)
    if lid < .3:
        inkLine([[x - w * .14, y - h], [x - w * .12, y - h - 34], [x + w * .12, y - h - 34], [x + w * .14, y - h]], 6, INK, 'ink', .4)
    for s in (-1, 1):
        G.c.drawCircle(x + s * w * .4, y + 6, 10, _pa(INK, 1))


def luggageTag(x, y, txt, swing=0.0, key='tag', s=1.0):
    push()
    translate(x, y)
    rotate(swing)
    line(0, 0, 0, 50 * s, INK, 1, 3)
    boilSeed(key)
    paint([[-60 * s, 50 * s], [60 * s, 50 * s], [60 * s, 150 * s], [-60 * s, 150 * s]], wash='#F2E2BC', ink=INK, sw=1.1)
    G.c.drawCircle(0, 64 * s, 7 * s, _pa(INK, 1))
    text(txt, 0, 108 * s, 44 * s, '#8A3A2A', shadow=False)
    pop()


# ------------------------------------------------------------------ paper islands at sea
def island(x, y, w, kind='tree', key='isl', pin=0.0):
    """paper-cutout island; (x, y) = top-centre surface"""
    boilSeed(key)
    P = [[x - w / 2, y + 120], [x - w * .42, y + 12], [x - w * .2, y - 6], [x + w * .25, y - 4], [x + w * .45, y + 14], [x + w / 2, y + 120]]
    paint(P, wash='#E8C890', fill='#B8925A', fillOp=70, ink=INK, sw=1.2, curv=.4)
    paint([[x - w * .44, y + 10], [x - w * .2, y - 8], [x + w * .25, y - 6], [x + w * .46, y + 12], [x + w * .3, y + 26], [x - w * .3, y + 26]],
          wash='#86C96E', ink=INK, sw=1.0, curv=.4)
    lx = x + w * .26
    if kind == 'tree':
        inkLine([[lx, y + 4], [lx + 6, y - 90]], 5, '#7A4E33', 'ink', .3)
        for i in range(5):
            a = -math.pi / 2 + (i - 2) * .55
            paint([[lx + 6, y - 92], [lx + 6 + math.cos(a) * 70, y - 92 + math.sin(a) * 40 + 24], [lx + 6 + math.cos(a) * 30, y - 80]],
                  wash='#5FA058', ink=INK, sw=.8)
    elif kind == 'light':
        paint([[lx - 18, y], [lx + 18, y], [lx + 12, y - 120], [lx - 12, y - 120]], wash='#F4F0E8', ink=INK, sw=1.0)
        for j in range(3):
            flatRect(lx - 16 + j * 1.5, y - 30 - j * 36, 32 - j * 3, 14, '#D8504E', 1)
        paint(rectPts(lx - 16, y - 150, 32, 30), wash='#FFE7A0', ink=INK, sw=.9)
        glow(lx, y - 135, 70, '#FFE7A0', .6)
    elif kind == 'hut':
        paint(rectPts(lx - 40, y - 60, 80, 60), wash='#E8D4B0', ink=INK, sw=1.0)
        paint([[lx - 56, y - 56], [lx, y - 110], [lx + 56, y - 56]], wash='#C8704E', ink=INK, sw=1.0)
        paint(rectPts(lx - 12, y - 34, 24, 34), wash='#6A4A3A', ink=INK, sw=.8)
    elif kind == 'mill':
        paint([[lx - 24, y], [lx + 24, y], [lx + 14, y - 110], [lx - 14, y - 110]], wash='#F2E2BC', ink=INK, sw=1.0)
        for i in range(4):
            a = i * TAU / 4 + G.T * 1.5
            paint([[lx, y - 110], [lx + math.cos(a) * 70, y - 110 + math.sin(a) * 70], [lx + math.cos(a + .25) * 66, y - 110 + math.sin(a + .25) * 66]],
                  wash='#F4F0E8', ink=INK, sw=.8)
    if pin > 0:
        mapPin(x - w * .36, y + 8, pin, key + 'pin')


def mapPin(x, y, k, key='pin'):
    p = backOut(clamp(k))
    if p < .02:
        return
    yy = y - 80 * (1 - clamp(k * 1.5))
    push()
    translate(x, yy)
    scale(p)
    line(0, 0, 0, -60, INK, 1, 4)
    boilSeed(key)
    paint(ellPts(0, -72, 22, 22, 18), wash='#E0344E', ink=INK, sw=1.1)
    G.c.drawCircle(-7, -79, 6, _pa('#FFFFFF', .8))
    pop()


def seaBands(t, x0, x1, y, rows=4, cols=('#7FB8E0', '#5A98CC', '#3F7AB4', '#2C5E98')):
    for r in range(rows):
        yy = y + r * 60
        P = [[x0, yy + 400]]
        n = int((x1 - x0) / 40)
        for i in range(n + 1):
            xx = x0 + i * 40
            P.append([xx, yy + 14 * math.sin(xx / 90 + t * (1.4 + r * .3) + r)])
        P.append([x1, yy + 400])
        boilSeed('sea%d' % r)
        paint(P, wash=cols[r % len(cols)], ink=INK, sw=1.0)


def polaroid(x, y, s, rot=0.0, key='pol', night=False):
    from sets2 import coupleSnap
    push()
    translate(x, y)
    rotate(rot)
    scale(s)
    boilSeed(key)
    paint(rectPts(-110, -120, 220, 250), wash='#FFFDF6', ink=INK, sw=1.0)
    coupleSnap(-92, -102, 184, 170, night=night)
    camellia(60, 100, 14, 1.0, key=key + 'c')
    pop()


# ------------------------------------------------------------------ desk with a drawer, cork board, letters
def desk(x, y, w, h, drawer=0.0, key='desk', col='#B07A54', inside=None):
    """front view; (x, y) = ground centre; returns (drawer x, y, w, h)"""
    top = y - h
    boilSeed(key)
    for s in (-1, 1):
        paint(rectPts(x + s * (w / 2 - 30) - 16, top, 32, h), wash=mixCol(col, INK, .2), ink=INK, sw=1.0)
    paint(rectPts(x - w / 2, top - 30, w, 34), wash=col, fill=mixCol(col, INK, .25), fillOp=60, ink=INK, sw=1.3)
    dw, dh = w * .62, h * .3
    dx, dy = x - dw / 2, top + 10
    paint(rectPts(x - w / 2 + 20, top + 4, w - 40, dh + 20), wash=mixCol(col, INK, .12), ink=INK, sw=1.0)
    if drawer > .01:
        # pulled out towards the viewer: draw the box below the front
        ext = dh * .9 * drawer
        paint(rectPts(dx - 10, dy - ext * .35, dw + 20, ext * .5 + 6), wash='#5A3A2A', ink=INK, sw=1.0)
        if inside:
            inside(dx, dy - ext * .35, dw, ext * .5)
    paint(rectPts(dx, dy + (dh * .25 * drawer), dw, dh), wash=mixCol(col, '#FFFFFF', .1), fill=mixCol(col, INK, .2), fillOp=60, ink=INK, sw=1.2)
    paint(rrPts(x - 40, dy + dh * .42 + dh * .25 * drawer, 80, 16, 8), wash='#E8C890', ink=INK, sw=.9)
    return dx, dy, dw, dh


def corkBoard(x, y, w, h, key='cork'):
    boilSeed(key)
    paint(rectPts(x - 18, y - 18, w + 36, h + 36), wash='#7A4E33', ink=INK, sw=1.4)
    paint(rectPts(x, y, w, h), wash='#C89A63', fill='#A87A48', fillOp=60, ink=INK, sw=1.0)
    for i in range(140):
        G.c.drawCircle(x + hash1(i * 1.3) * w, y + hash1(i * 2.9) * h, 2 + 2 * hash1(i), _pa('#8E6438', .5))


def letter(x, y, w, h, title, body='示例歌词', key='let', rot=0.0, pinCol='#E0344E', a=1.0):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-w / 2, -h / 2, w, h), wash='#FFFBF0', washOp=int(255 * a), ink=INK, sw=1.0)
    text(title, -w / 2 + 24, -h / 2 + 40, 30, '#5A3A2A', align='left', shadow=False, a=a)
    for j in range(4):
        yy = -h / 2 + 90 + j * 44
        line(-w / 2 + 24, yy + 18, w / 2 - 24, yy + 18, '#C8B8A0', .8 * a, 1.5)
    text(body, 0, -h / 2 + 120, 40, '#C0304A', shadow=False, a=a)
    icoHeart(w / 2 - 50, h / 2 - 46, 26, '#E0344E', a, ink=True, key=key + 'h')
    G.c.drawCircle(0, -h / 2 + 8, 12, _pa(pinCol, a))
    G.c.drawCircle(-3, -h / 2 + 4, 4, _pa('#FFFFFF', .8 * a))
    pop()


# ------------------------------------------------------------------ paper-cup phone, rooftops
def paperCup(x, y, s, rot=0.0, key='cup', col='#F4F0E8'):
    """cup centre at (x, y); open end points along +x (before rotation)"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint([[-s * .5, -s * .3], [s * .5, -s * .5], [s * .5, s * .5], [-s * .5, s * .3]], wash=col, fill='#C8BCA8', fillOp=60, ink=INK, sw=1.0)
    paint(ellPts(s * .5, 0, s * .12, s * .5, 14), wash='#D8D0C0', ink=INK, sw=.9)
    line(-s * .2, -s * .38, -s * .2, s * .38, '#E07A92', .9, s * .1)
    pop()


def rooftop(x, y, w, key='roof', col='#5A4A7A', h=600):
    """building top at y (flat roof surface), x = centre"""
    boilSeed(key)
    paint(rectPts(x - w / 2, y, w, h), wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=1.2)
    paint(rectPts(x - w / 2 - 16, y - 18, w + 32, 26), wash=mixCol(col, '#FFFFFF', .2), ink=INK, sw=1.1)
    for i in range(3):
        for j in range(2):
            wx, wy = x - w / 2 + 40 + i * (w - 80) / 2.5, y + 60 + j * 110
            flatRect(wx, wy, 50, 60, '#FFD98A', .85 if (i + j) % 2 == 0 else .25)


# ------------------------------------------------------------------ calendar, balloon, stage
def calendar(x, y, s, num, tear=0.0, nextNum=None, key='cal', month='十月'):
    """tear-off calendar centred at (x, y). tear 0..1 peels the top page away to reveal nextNum."""
    boilSeed(key)
    G.c.drawCircle(x, y - s * .66, s * .04, _pa(INK, 1))
    paint(rectPts(x - s * .4, y - s * .58, s * .8, s * 1.1), wash='#F4F0E8', ink=INK, sw=1.1)
    flatRect(x - s * .4, y - s * .58, s * .8, s * .2, '#E0344E', 1)
    text(month, x, y - s * .48, s * .12, '#FFFFFF', shadow=False)
    if nextNum is not None and tear > 0:
        text(str(nextNum), x, y + s * .1, s * .5, INK, shadow=False)
    if tear < 1:
        push()
        px, py = x + s * .4, y - s * .38
        translate(px, py)
        rotate(-tear * 1.4)
        translate(tear * s * .8, tear * tear * s * 1.2)
        translate(-px, -py)
        paint(rectPts(x - s * .4, y - s * .38, s * .8, s * .9), wash='#FFFDF6', ink=INK, sw=1.0)
        text(str(num), x, y + s * .1, s * .5, INK if tear == 0 else '#5A4A4A', shadow=False)
        pop()


def tornPage(x, y, s, num, k, key='tp'):
    """a calendar page peeling off (k 0..1) and then falling away and fading (k > 1)"""
    a = 1 - clamp((k - 1) / 2.2)
    if a <= .01:
        return
    push()
    px, py = x + s * .4, y - s * .38
    translate(px, py)
    rotate(-min(k, 1) * 1.4 - max(0, k - 1) * .8)
    translate(k * s * .8, k * k * s * .45)
    translate(-px, -py)
    boilSeed(key)
    paint(rectPts(x - s * .4, y - s * .38, s * .8, s * .9), wash='#FFFDF6', washOp=int(255 * a), ink=INK if a > .5 else None, sw=1.0)
    text(str(num), x, y + s * .1, s * .5, '#5A4A4A', shadow=False, a=a)
    pop()


def heartBalloon(x, y, r, key='hb', col='#FF6F96', a=1.0, sq=0.0):
    """heart balloon centred at (x, y); string goes down from the knot"""
    boilSeed(key)
    P = heartPts(x, y, r, 40)
    if sq:
        P = [[x + (px - x) * (1 + sq), y + (py - y) * (1 - sq)] for px, py in P]
    glow(x, y, r * 1.6, col, .25 * a)
    paint(P, wash=col, washOp=int(255 * a), fill=mixCol(col, INK, .25), fillOp=int(60 * a), ink=INK, sw=1.3)
    paint(ellPts(x - r * .45, y - r * .35, r * .2, r * .12, 12, 0, -.6), wash='#FFFFFF', washOp=int(170 * a), ink=None)
    paint([[x - r * .1, y + r * .98], [x + r * .1, y + r * .98], [x, y + r * .86]], wash=col, ink=INK, sw=.8)


def spotlight(x, yTop, yFloor, w, a=1.0, col='#FFF2C8'):
    if a <= .01:
        return
    flat([[x - w * .12, yTop], [x + w * .12, yTop], [x + w / 2, yFloor], [x - w / 2, yFloor]], col, .22 * a)
    G.c.save()
    G.c.translate(x, yFloor)
    G.c.scale(1, .22)
    G.c.drawCircle(0, 0, w / 2, _pa(col, .35 * a))
    G.c.restore()


def confetti(t, cx, cy, k, seed=0, n=60, spread=600):
    if k <= 0 or k >= 1.6:
        return
    cols = ['#FF6F96', '#FFD36A', '#8FD3FF', '#FFFFFF', '#B8F0A0']
    for i in range(n):
        h1, h2, h3 = hash1(seed + i * 1.3), hash1(seed + i * 2.7), hash1(seed + i * 4.1)
        a = h1 * TAU
        d = spread * (.3 + .7 * h2) * easeOut(clamp(k * 1.6))
        x = cx + math.cos(a) * d
        y = cy + math.sin(a) * d * .7 + 260 * k * k * (.5 + h3)
        al = 1 - clamp((k - .9) / .7)
        push()
        translate(x, y)
        rotate(k * 10 * (h3 - .5) + a)
        flatRect(-9, -4, 18, 8, cols[i % len(cols)], al)
        pop()


def smokePuff(x, y, s, k, key='smk'):
    if k <= 0 or k >= 1:
        return
    for i in range(7):
        a = i / 7 * TAU + .3
        d = s * (.2 + .8 * easeOut(k))
        r = s * (.35 + .2 * hash1(i)) * (1 - .3 * k)
        boilSeed(f'{key}{i}')
        paint(ellPts(x + math.cos(a) * d, y + math.sin(a) * d * .6, r, r * .8, 16), wash='#E8E4F0', washOp=int(230 * (1 - k)), ink=None)
