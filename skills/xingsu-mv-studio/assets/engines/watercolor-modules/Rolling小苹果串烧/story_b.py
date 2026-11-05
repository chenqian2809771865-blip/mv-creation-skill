# story_b.py: S09–S16 — 小苹果 「春夏秋冬」: the evidence photos turn out to be sweet memories (the summer one is at 老地方).
import math
from eng import *
from clawd import *
from props import *
from props_chuanshao import *
from props3 import *
from sets_huibuhui import ginkgoAvenue, ginkgoLeaf, leafCol, GK
from common import *


# ===================================================================== the four "evidence" photos (tiny versions of S10/S11/S13/S15)
def mini(kind):
    def sc(cx, cy, w, h):
        x0, y0 = cx - w / 2, cy - h / 2
        if kind == 'spring':
            gradRect(x0, y0, w, h, ['#CDEBFA', '#FBE0EA'])
            flat([[x0, cy + h * .12], [x0 + w, cy + h * .02], [x0 + w, y0 + h], [x0, y0 + h]], '#9ED27A')
            for i in range(9):
                G.c.drawCircle(x0 + w * (.06 + i * .11), cy + h * .28 + (i % 2) * 10, w * .03, skia.Paint(AntiAlias=True, Color=skcol(PETALS[i % 6])))
            boilSeed(f'mt{kind}')
            paint(ellPts(x0 + w * .85, cy - h * .05, w * .16, h * .2, 14), wash='#7CC36B', ink=INK, sw=.4, lite=True)
        elif kind == 'summer':
            gradRect(x0, y0, w, h, ['#1C2A6E', '#3E3B8E'])
            for i in range(10):
                sparkle(x0 + w * hash1(i * 3), y0 + h * .55 * hash1(i * 7), w * .03, '#FFF3B0')
            flat([[x0, cy + h * .22], [x0 + w, cy + h * .14], [x0 + w, y0 + h], [x0, y0 + h]], '#2F5A4A')
            G.c.drawRect(skia.Rect.MakeXYWH(x0 + w * .2, cy + h * .26, w * .6, h * .04), skia.Paint(AntiAlias=True, Color=skcol('#B9784E')))
        elif kind == 'autumn':
            gradRect(x0, y0, w, h, ['#F6C97E', '#FCEBC6'])
            flat([[x0, cy + h * .1], [x0 + w, cy + h * .1], [x0 + w, y0 + h], [x0, y0 + h]], '#E9DCC4')
            for s_ in (-1, 1):
                paint(ellPts(cx + s_ * w * .4, cy - h * .15, w * .16, h * .28, 14), wash=GK['leaf'], ink=INK, sw=.4, lite=True)
        else:
            gradRect(x0, y0, w, h, ['#9FB0D8', '#EEF4FA'])
            flat([[x0, cy + h * .2], [x0 + w, cy + h * .1], [x0 + w, y0 + h], [x0, y0 + h]], '#FFFFFF')
            for i in range(10):
                G.c.drawCircle(x0 + w * hash1(i * 2.1), y0 + h * hash1(i * 5.3), 3, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF')))
        u = w / 30
        him(cx - w * .18, cy + h * .38, u, dict(view='q', eyes='happy', mouth='smile', noShadow=True, lite=True, swMul=.7))
        her(cx + w * .18, cy + h * .38, u, dict(view='q', flip=True, eyes='happy', mouth='smile', noShadow=True, lite=True, swMul=.7))
    return sc


POLS = [(470, 380, -.07, 'spring', '春'), (840, 330, .05, 'summer', '夏'), (1200, 400, -.04, 'autumn', '秋'), (1540, 340, .07, 'winter', '冬')]


def holdHands(x1, x2, y, u):
    """a little clasped-hands blob between two walkers (bodies ≥ 12u apart)"""
    boilSeed('hh')
    paint(ellPts((x1 + x2) / 2, y - 4.5 * u, .55 * u, .5 * u, 12), wash='#F2A283', ink=INK, sw=.7)


# ===================================================================== S09 the evidence board
def s09(t, lt, dur):
    BB = beatsOf(9)
    n = nOn(t, BB)
    lean = ease(seg(t, BB[3] - .08, BB[3] + .1)) if t > BB[3] - .08 else 0
    cam(t, lerp(960, 1250, lean), lerp(520, 560, lean), lerp(1.0, 1.28, lean))
    evidenceWall(t)
    pts = [[x, y - 160] for i, (x, y, r, kind, lab) in enumerate(POLS) if i < n]
    if len(pts) >= 2:
        pinThread(pts)
    for i, (x, y, r, kind, lab) in enumerate(POLS):
        if i < n:
            polaroid(x, y, 290, r, pk(t, BB[i], .14), mini(kind), key=f'bd9p{i}', label=lab)
            if t - BB[i] < .25:
                impactLines(x, y - 160, 30, 70, 8, t, '#FFF5E2', key=f'pin9{i}', sw=1)
    o = fo(feel('suspicious' if lean < .5 else 'surprised', t), view='q', flip=True, aR=1.3, armR=magnifierHook(1.4), rot=-.08 * lean,
           dy=-1.6 * lean)
    her(lerp(1660, 1590, lean), 1010, 36, o, detective=True)
    camEnd()


# ===================================================================== S10 spring: the photo comes alive
def s10(t, lt, dur):
    BB = beatsOf(10)
    n = nOn(t, BB)
    cam(t, 960, 540, 1.0)
    springField(t)
    u = 30
    x = lerp(560, 980, lt / dur)
    x2 = x + 12 * u
    mv = move('walk', t)
    him(x, 880, u, fo(feel('happy', t), view='q', walk=mv['walk'], dy=mv['dy'], aR=0.0, aL=.3))
    her(x2, 880, u, fo(feel('happy', t), view='q', walk=mv['walk'] + .5, dy=mv['dy'], aL=0.0, aR=.3, hat='flower'))
    holdHands(x + 5 * u, x2 - 5 * u, 880 + mv['dy'] * u, u)
    spots = [(180, 980, 74), (1630, 1000, 64), (390, 1010, 58), (1820, 860, 74)]
    for i, (bx, by, s) in enumerate(spots):
        k = clamp((t - BB[i] + .06) / .1) if t > BB[i] - .06 else 0
        bloom(bx, by, s, k, PETALS[(i + 1) % 5], key=f'bb10{i}')
    bfly(700 + 220 * math.sin(t * 1.3), 420 + 60 * math.cos(t * 2), 22, t, key='bf10')
    bfly(1250 + 160 * math.sin(t * 1.1 + 2), 360 + 50 * math.cos(t * 1.7), 18, t + .3, key='bf10b', col='#F59BB0')
    if n >= 4:
        petalsFly(t, 10, 28, 0, -50, W, 1000, 13)
    camEnd()


BENCH_W = 820


def benchProps(t, st):
    """a slice of watermelon and a little radio at the two ends of the 老地方 bench (S11, S12)"""
    boilSeed('wm11')
    x0 = 960 - BENCH_W / 2 + 14
    paint([[x0, st], [x0 + 86, st], [x0 + 43, st - 50]], wash='#E8574E', ink=INK, sw=.7)
    paint([[x0, st], [x0 + 86, st], [x0 + 80, st - 8], [x0 + 6, st - 8]], wash='#7CC36B', ink=None)
    x1 = 960 + BENCH_W / 2 - 88
    paint(rrPts(x1, st - 54, 74, 54, 10), wash='#5B7FC4', ink=INK, sw=.7)
    G.c.drawCircle(x1 + 20, st - 26, 12, skia.Paint(AntiAlias=True, Color=skcol('#2A2440')))
    emote('music', x1 + 50, st - 90, 18, 1, t)


# ===================================================================== S11 summer night at 老地方: stars come out one per beat
def s11(t, lt, dur):
    BB = beatsOf(11)
    n = nOn(t, BB)
    cam(t, 960, 560, 1.0)
    oldPlace(t, 1.0, decor=0.0, bench=False, signX=1500, key='op11', lanterns=False)
    if n >= 4:
        a = ease(seg(t, BB[3] - .04, BB[3] + .3))
        glow(1100, 200, 700, '#B9C6FF', .3 * a)
        sparkles(t, 111, 30, 300, 40, 1800, 460, 7, '#FFF5E2')
    SP = [(760, 170, 46), (1060, 110, 58), (1360, 230, 50)]
    for i, (x, y, r) in enumerate(SP):
        if i < n:
            k = backOut(clamp((t - BB[i] + .04) / .14))
            starFace(x, y, r * k, 0, key=f'st11{i}')
    u = 28
    st = parkBench(960, oldGround(960) + 40, BENCH_W, 110, 130, key='bn11', night=1.0)
    seat(him, 960 - 5.4 * u, st, u, fo(feel('happy', t), view='front', lookY=-1, lookX=.4, aL=.2, aR=.2, dy=0))
    seat(her, 960 + 5.4 * u, st, u, fo(feel('love' if n >= 4 else 'happy', t), view='front', lookY=-1, lookX=-.2, aL=.2, aR=.2, dy=0, hat='flower'))
    benchProps(t, st)
    fireflies(t, 11, 14, 100, 560, 1800, 900, 1.0)
    camEnd()


# ===================================================================== S12 the stars wink; she leans on him
def s12(t, lt, dur):
    BB = beatsOf(12)
    n = nOn(t, BB)
    cam(t, 960, 420, 1.0 + .02 * lt)
    oldPlace(t, 1.0, decor=0.0, bench=False, signX=1500, key='op11', lanterns=False)
    SP = [(830, 130, 70), (1080, 70, 84), (1330, 210, 74), (1790, 330, 64), (980, 380, 54)]
    for i, (x, y, r) in enumerate(SP):
        w = 0
        if i < 3 and n > i:
            a = t - BB[i]
            w = 1 if -.04 <= a < .3 else 0
        starFace(x, y + 8 * math.sin(t * 2 + i), r, w, key=f'st12{i}')
    if n >= 4:
        a = clamp((t - BB[3] + .04) / .45)
        sx, sy = lerp(1900, 300, a), lerp(40, 460, a)
        flat([[sx, sy], [sx + 380, sy - 110], [sx + 380, sy - 92], [sx, sy + 8]], '#FFF8D0', .7 * (1 - a * .5))
        sparkle(sx, sy, 26, '#FFFFFF')
        stamp('许愿！', 520, 480, 80, '#FFE36E', t - BB[3], rot=-.1)
    u = 28
    st = parkBench(960, oldGround(960) + 40, BENCH_W, 110, 130, key='bn11', night=1.0)
    benchProps(t, st)
    lean = ease(seg(t, BB[2] - .1, BB[2] + .06)) if t > BB[2] - .1 else 0
    seat(him, 960 - 5.4 * u, st, u, fo(feel('happy', t), view='front', lookY=-1, aL=.2, aR=.2, dy=0))
    seat(her, 960 + 5.4 * u - 14 * lean, st, u, fo(feel('love' if lean > .5 else 'happy', t), view='front', lookY=-1, rot=-.12 * lean, aL=.2, aR=.2, dy=0, hat='flower'))
    fireflies(t, 12, 14, 100, 560, 1800, 900, 1.0)
    camEnd()


# ===================================================================== S13 autumn: the ginkgo avenue, leaves land on the beats
def s13(t, lt, dur):
    BB = beatsOf(13)
    n = nOn(t, BB)
    cam(t, 960, 540, 1.0)
    ginkgoAvenue(t, 'gold', key='ga13', leavesK=.6)
    u = 32
    x = lerp(560, 900, lt / dur)
    x2 = x + 12 * u
    mv = move('walk', t)
    him(x, 900, u, fo(feel('happy', t), view='q', walk=mv['walk'], dy=mv['dy'], aR=0.0, aL=.3))
    her(x2, 900, u, fo(feel('happy', t), view='q', walk=mv['walk'] + .5, dy=mv['dy'], aL=0.0, aR=.3, hat='flower'))
    holdHands(x + 5 * u, x2 - 5 * u, 900 + mv['dy'] * u, u)
    land = [(300, 980), (1520, 1000), (1100, 1010)]
    for i in range(min(3, n)):
        a = t - BB[i]
        lx, ly = land[i]
        y = ly if a >= 0 else lerp(-60, ly, clamp((a + .5) / .5))
        sq = 1 + .25 * math.exp(-max(0, a) * 10) * (1 if a >= 0 else 0)
        ginkgoLeaf(lx, y, 56 * sq, rot=(a * 3 + i) if a < 0 else .4 + i * .7, col=leafCol(i), key=f'gl13{i}')
        if 0 <= a < .22:
            impactLines(lx, ly - 20, 40, 90, 10, t, '#FFF5E2', key=f'gi13{i}', sw=1.0)
    hx, hy = x2 + 1.6 * u, 900 - 8.6 * u + mv['dy'] * u
    a = t - BB[3]
    if a > -.5:
        y = lerp(-60, hy, clamp((a + .5) / .46)) if a < -.04 else hy
        ginkgoLeaf(hx, y, 52, rot=a * 4 if a < 0 else -.3, col=leafCol(5), key='glhat')
        if 0 <= a < .3:
            sparkles(t, 13, 6, hx - 90, hy - 90, hx + 90, hy + 30, 16, '#FFFFFF')
    camEnd()


# ===================================================================== S14 waves over the wheat field
def s14(t, lt, dur):
    BB = beatsOf(14)
    n = nOn(t, BB)
    cam(t, 960, 540, 1.0)
    wx = -400
    if n:
        wx = lerp(-300, W + 300, clamp((t - BB[n - 1] + .04) / .45))
    wheatScene(t, wx, 1.0 if n else 0.0)
    u = 20
    him(915, 760, u, fo(feel('happy', t), view='qback', aL=.2, aR=.2))
    her(915 + 12.5 * u, 760, u, fo(feel('happy', t), view='qback', aL=.2, aR=.2, hat='flower'))
    if n >= 4:
        a = t - BB[3]
        for i in range(9):
            bx = 600 + i * 90 + a * 600
            by = 520 - a * 500 - (i % 3) * 30
            boilSeed(f'bird{i}')
            inkLine([[bx - 22, by - 8], [bx, by + 2], [bx + 22, by - 8]], 1.4, INK, 'ink', .6)
    camEnd()


# ===================================================================== S15 winter: the snowman, the red scarf
def s15(t, lt, dur):
    BB = beatsOf(15)
    n = nOn(t, BB)
    cam(t, 960, 540, 1.0)
    winterCorner(t)
    ages = [t - BB[i] for i in range(4)]
    snowman(1260, 900, 50, min(4, n), t, key='sm15', ages=ages)
    for i in range(min(3, n)):
        a = t - BB[i]
        if a < .3:
            for j in range(6):
                ang = j / 6 * TAU
                paint(ellPts(1260 + math.cos(ang) * (80 + 200 * a), 860 - [0, 125, 215][i] + math.sin(ang) * 60 * a - 100 * a, 9, 9, 8),
                      wash='#FFFFFF', washOp=255 * (1 - a / .3), ink=None)
    u = 32
    him(480, 920, u, fo(feel('happy', t), view='q', aR=1.1 if n >= 4 else .3))
    her(480 + 11 * u, 920, u, fo(feel('shy' if n >= 4 else 'happy', t), view='q', flip=True, hat='flower'))
    if n >= 4:
        a = clamp((t - BB[3] + .04) / .2)
        boilSeed('scarf')
        hx = 480 + 11 * u
        y = 920 - 3.0 * u
        paint(ribbon([[hx - 5 * u, y], [hx, y + 10], [hx + 5 * u * a, y]], 28, 28), wash='#E03A4E', ink=INK, sw=1)
        paint(rectPts(hx + 2.0 * u, y + 6, 26, 90 * a), wash='#E03A4E', ink=INK, sw=.8)
        floatHearts(t, 15, 5, 500, 380, 1000, 700, 14)
    snowflakes(t, 15, 70, -40, -60, W + 40, H)
    camEnd()


# ===================================================================== S16 back at her desk: blush, then "still suspicious!"
def s16(t, lt, dur):
    BB = beatsOf(16)
    n = nOn(t, BB)
    sh = shake(t, BB[3], 16, .35) if n >= 4 else (0, 0)
    cam(t, 960 + sh[0], 520 + sh[1], 1.04)
    herRoom(t)
    rot = 0
    if n == 3:
        a = t - BB[2]
        rot = .18 * math.sin(a * 30) * math.exp(-a * 4)
    emo = ['shy', 'shy', 'love', 'shy', 'determined'][n]
    o = fo(feel(emo, t), view='front', blush=.5 + .2 * n if n < 4 else .2, aL=-.3, rot=rot, aR=.55 if n < 4 else 1.6)
    if n == 3:
        o.update(eyes='closed', mouth='wobble', emote='sweat')
    if n < 4:
        o['armR'] = lambda u, sw: polaroid(2.6 * u, -1.6 * u, 4.6 * u, .12, 1, mini('winter'), key='hold16')
    her(820, 812, 42, o, detective=True)
    jump = 0
    if n >= 4:
        a = t - BB[3]
        jump = -14 * math.exp(-a * 8) * abs(math.cos(a * 20))
    push()
    translate(0, jump)
    herDesk(t)
    pop()
    if n >= 4:
        a = t - BB[3]
        impactLines(1400, 400, 140, 420, 18, t, '#FFF5E2', key='imp16', sw=1.6)
        stamp('疑！', 1400, 400, 220, C['red'], a, rot=.12)
    camEnd()
