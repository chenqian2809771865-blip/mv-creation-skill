# story3.py: 《苦咖啡·唯一》 shots S28–S38 (the map, the flower trail, the constellation, latte art, the geese come back,
# protecting her flower, his head full of her, therapy, closing time, she comes back with a sugar cube, the end).
import math
from eng import *
import eng
from clawd import *
from props import bubble, stamp, sparkle, sparkles, impactLines, sunburst, puff, floatHearts
from sets import flatGround, starField
from sets2 import seat
from dx import backpack, speedLines
from sets_huibuhui import ginkgoLeaf
from sets2 import coffeeRing
from hl import vignette, tint
from nm import darkness
from wx import clinicWall, wallClock, monitorBox, ecgTrace, line, _pa
from props_chuanshao import bloom
from props_zuitian import cloche
from common import *
from kf import *
from story import addJ, heldCup, memory, sigh, U_WIDE
from story2 import roomWall, nightBg


# S28 70.55–72.41 · a map of the south: a pin a beat, every one crossed out; a big question mark
def s28(t, lt, dur):
    cam(t, 960, 540, 1.0)
    roomWall(t, 's28')
    mapBoard(240, 130, 1060, 650, 's28map')
    pins = [(520, 330, 152), (980, 300, 153), (1120, 600, 154)]
    for i, (px, py, k) in enumerate(pins):
        pk_ = clamp((t - (B[k] - .12)) / .1)
        ck = clamp((t - (B[k] - .06)) / .08)
        mapPin(px, py, pk_, ck, key=f's28pin{i}', sc=2.0)
    x, u = 1580, 34
    keys = [[0, 'hopeful'], [ek(153), 'nervous', {'emote': None}], [ek(154), 'sad'], [ek(155), 'confused', {'emote': None}]]
    o = heO(t, keys, view='q', flip=True, aL=.3, aR=.3)
    him(x, 900, u, o)
    if t >= B[155] - .045:
        k = backOut(clamp((t - (B[155] - .045)) / .16))
        text('？', x + 20, 900 - 12 * u, 150 * k, '#FFFFFF', stroke=INK, strokeW=16)
    camEnd()


# S29 72.41–74.26 · dawn path: her little white flowers light up one a beat, a trail out of frame; his eyes light up
def s29(t, lt, dur):
    cam(t, 960, 540, 1.0)
    skyGrad(DAWN_SKY, 760)
    glow(1600, 640, 520, '#FFE2B8', .7)
    hills(600, ['#C8A8C8', '#A88EB8'], t, 's29h')
    flatGround(760, '#B8D89A', '#8FBF7A', key='s29g')
    p = [[-100, H + 100], [700, H + 100], [1500, 780], [1900, 760], [1940, 772], [1560, 800], [300, H + 100]]
    paint([[200, H + 50], [900, H + 50], [1900, 770], [1820, 760]], wash='#E8D3B0', fill='#C9A77A', fillOp=40, ink=INK, sw=.8)
    flw = [(860, 850, 156, 50), (1280, 800, 157, 40), (1620, 772, 158, 30)]
    for i, (fx, fy, k, s) in enumerate(flw):
        on = clamp((t - (B[k] - .045)) / .14)
        if on > 0:
            glow(fx, fy, 6 * s * on, '#FFF2C8', .8 * on)
        flowerAt(fx, fy, s * (.6 + .4 * backOut(on)), 1.0, .9)
        if 0 <= t - B[k] < .4:
            sparkle(fx + s, fy - s * 1.5, 18 * (1 - (t - B[k]) / .4), '#FFFFFF', 1)
    x, u = 440, 34
    keys = [[0, 'sad'], [ek(156), 'surprised', {'emote': None}], [ek(158), 'hopeful'], [ek(159), 'starstruck']]
    o = heO(t, keys, view='q', aL=.3, aR=.3)
    step = 80 * landK(t, 159, .2)
    him(x + step, 930, u, o)
    camEnd()


# S30 74.26–76.12 · the constellation: stars appear, connect, and draw her (box + legs + flower); he gazes up
CST = dict(box=[(760, 330), (1180, 330), (1180, 560), (760, 560)], legs=[(820, 640), (920, 640), (1020, 640), (1120, 640)],
           flower=[(1080 + math.cos(i / 5 * TAU) * 46, 250 + math.sin(i / 5 * TAU) * 46) for i in range(5)])


def s30(t, lt, dur):
    cam(t, 960, 540, 1.0)
    gradRect(-300, -300, W + 600, H + 600, ['#0E1230', '#1E2A5A', '#3A3A78'])
    starField(t, 31, 120, 0, 0, W, 760, r=2.4)
    k0, k1, k2, k3 = [popK(t, k, .14) for k in (160, 161, 162, 163)]
    tw = 1 + .35 * hitK(t, 163, .25) * math.sin(t * 30)
    glw = .5 + .5 * k3

    def star(x, y, k, r=12):
        if k <= 0:
            return
        glow(x, y, 50 * k * tw, '#FFF2C8', .6 * glw)
        paint(starPts(x, y, r * k * tw, .4, 4), wash='#FFFDF0', ink=None)
    lp = skia.Paint(AntiAlias=True, Color=skcol('#FFF2C8', .75), StrokeWidth=3, Style=skia.Paint.kStroke_Style)
    if k1 > 0:
        bx = CST['box']
        for i in range(4):
            a, b = bx[i], bx[(i + 1) % 4]
            f = clamp(k1 * 4 - i)
            G.c.drawLine(a[0], a[1], lerp(a[0], b[0], f), lerp(a[1], b[1], f), lp)
    if k2 > 0:
        for i, (lx, ly) in enumerate(CST['legs']):
            G.c.drawLine(lx, 560, lx, lerp(560, ly, clamp(k2)), lp)
        fl = CST['flower']
        for i in range(5):
            a, b = fl[i], fl[(i + 2) % 5]
            G.c.drawLine(a[0], a[1], lerp(a[0], b[0], clamp(k2)), lerp(a[1], b[1], clamp(k2)), lp)
        for ex in (880, 1060):
            star(ex, 430, k2, 9)
        p = skia.Path()
        p.moveTo(920, 490)
        p.quadTo(970, 520 * k2 + 490 * (1 - k2), 1020, 490)
        G.c.drawPath(p, lp)
    for (x, y) in CST['box']:
        star(x, y, k0, 14)
    for (x, y) in CST['legs']:
        star(x, y, k2, 10)
    for (x, y) in CST['flower']:
        star(x, y, k2, 10)
    if k3 > 0:
        glow(970, 450, 520, '#FFB3C6', .25 * k3)
        sparkles(t, 30, 14, 650, 200, 1300, 700, 16, '#FFFFFF')
    # hill + him looking up
    boilSeed('s30hill')
    paint([[-100, H + 100], [-100, 900], [300, 860], [700, 880], [1000, 940], [1400, 960], [W + 100, 940], [W + 100, H + 100]],
          wash='#141A36', ink=INK, sw=1.0, curv=.3)
    x, u = 420, 26
    keys = [[0, 'hopeful', {'lookY': -1, 'lookX': .5}], [ek(162), 'starstruck', {'lookY': -1}], [ek(163), 'love', {'tint': None, 'lookY': -1}]]
    o = heO(t, keys, view='q', aL=.3, aR=.3)
    him(x, 880, u, o)
    camEnd()


# S31 76.12–77.97 · top-down latte art: heart, flower, her face, her face again — 「又是她」
def heartArt(x, y, r, k):
    milkFill(heartPts(x, y + r * .05, r * .55 * backOut(k), 24), 1)


def flowerArt(x, y, r, k):
    for i in range(5):
        a = i / 5 * TAU
        milkFill(ellPts(x + math.cos(a) * r * .32 * k, y + math.sin(a) * r * .32 * k, r * .24 * k, r * .24 * k, 16), 1)
    G.c.drawCircle(x, y, r * .14 * k, _pa('#E8C060'))


def faceArt(big):
    def f(x, y, r, k):
        s = (1.0 if big else .8) * backOut(k)
        milkFill(rrPts(x - r * .6 * s, y - r * .42 * s, r * 1.2 * s, r * .84 * s, r * .1), 1)
        for ex in (-.22, .22):
            G.c.drawCircle(x + ex * r * s, y - r * .06 * s, r * .07 * s, _pa('#6A3A22'))
        p = skia.Path()
        p.moveTo(x - r * .12 * s, y + r * .14 * s)
        p.quadTo(x, y + r * .26 * s, x + r * .12 * s, y + r * .14 * s)
        G.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol('#6A3A22'), Style=skia.Paint.kStroke_Style, StrokeWidth=r * .04))
        for i in range(5):
            a = i / 5 * TAU
            G.c.drawCircle(x + r * .3 * s + math.cos(a) * r * .1 * s, y - r * .5 * s + math.sin(a) * r * .1 * s, r * .07 * s, _pa(MILK))
        if big:
            for ex in (-.36, .36):
                G.c.drawCircle(x + ex * r * s, y + r * .1 * s, r * .07 * s, _pa('#E8A0A8', .8))
    return f


def s31(t, lt, dur):
    cam(t, 960, 520, 1.0)
    flatRect(-300, -300, W + 600, H + 600, '#C98B5A')
    boilSeed('s31wood')
    for i in range(-2, 16):
        line(-300, i * 90 + 20 * math.sin(i), W + 300, i * 90 + 20 * math.sin(i + 1), '#A8693E', .8, 3)
    arts = [(330, heartArt, 164), (750, flowerArt, 165), (1170, faceArt(False), 166), (1590, faceArt(True), 167)]
    for i, (x, fn, k) in enumerate(arts):
        ak = clamp((t - (B[k] - .2)) / .2)
        cupTop(x, 470, 128, art=fn, artK=ak, key=f's31c{i}', t=t)
        if 0 <= t - B[k] < .35:
            G.c.drawCircle(x, 470, 150 + 120 * (t - B[k]) / .35, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .6 * (1 - (t - B[k]) / .35)),
                                                                          Style=skia.Paint.kStroke_Style, StrokeWidth=5))
    coffeeRing(560, 860, 60, .3)
    beanBag(140, 1000, .9, 's31bag')
    if t >= B[167] - .04:
        stamp('又是她', 1180, 750, 110, HOT, bage(t, 167), rot=-.06)
    camEnd()


# S32 77.97–79.83 · the geese fly back north; the one leading wears her little white flower; a petal drifts down to the cart
def s32(t, lt, dur):
    cam(t, 960, 540, 1.0)
    skyGrad(['#9CB8E8', '#F2C2C8', '#FFE6C8'], 1100)
    glow(400, 900, 500, '#FFE2B8', .6)
    for i, (cx, cy, s) in enumerate([(300, 200, 22), (1500, 140, 26)]):
        puff(cx + 10 * math.sin(t * .4 + i), cy, s, '#FFFFFF', key=f's32cl{i}', a=.9)
    # the cart roof, small, at the bottom
    cart(t, 1500, 930, .5, 0, key='s32cart', lit=0)
    vx = 1820 - 340 * (t - B[168])
    for i in range(7):
        j = abs(i - 3)
        side = -1 if i < 3 else 1
        gx = vx + j * 135
        gy = 360 + side * j * 64
        lead = i == 3
        flap = t * 9 + i
        if lead and t >= B[169] - .1 and t < B[169] + .25:
            flap = math.pi / 2 * (1 + .0 * t)
            for j in range(3):
                line(gx + 90 + j * 26, gy - 70 + j * 20, gx + 150 + j * 26, gy - 70 + j * 20, '#FFFFFF', .8, 4)
        goose(gx, gy, 1.5 if lead else 1.1, flap, -1, key=f's32g{i}', flower=lead, col='#A8968E', flowerS=26)
    pk_ = t - (B[171] - .06)
    if pk_ > 0:
        gx0 = vx if False else 1820 - 340 * (B[171] - .06 - B[168])
        px = gx0 - 80 + 60 * math.sin(pk_ * 4)
        py = 300 + 260 * pk_
        push()
        translate(px, py)
        rotate(math.sin(pk_ * 5) * .6)
        paint(ellPts(0, 0, 40, 24, 14), wash='#FFB3C6', fill='#F28FB0', fillOp=60, ink=INK, sw=.8)
        pop()
        glow(px, py, 90, '#FFF2C8', .6)
    camEnd()


# S33 79.83–83.55 · he protects her little flower: glow, a gust, a raindrop, it blooms; onto the cart, under a glass dome; a hug
def s33(t, lt, dur):
    cam(t, 900, 580, 1.25)
    lay = corner(t, 'dawn', lights=.5, lamp_=.3, key='cn33', items=False)
    top = lay['top']
    x0, u = 580, 34
    put = landK(t, 176, .2)
    hug = landK(t, 179, .18)
    x = x0 + 60 * hug
    flipK = t >= B[173] - .04 and t < B[175] - .04
    keys = [[0, 'hopeful'], [ek(173), 'scared', {'emote': None}], [ek(174), 'determined'], [ek(175), 'love', {'tint': None}],
            [ek(177), 'happy'], [ek(179), 'love', {'tint': None}]]
    o = heO(t, keys, view='q', flip=flipK, aL=.35, aR=.35)
    if t >= B[174] - .04 and t < B[175] - .04:
        o['sq'] = (o.get('sq') or 0) + .12
        o['dy'] = (o.get('dy') or 0) + .6
    if hug > 0:
        o.update(aL=.35 + 1.0 * hug, aR=.35 + 1.0 * hug)
    him(x, GY, u, o)
    jx = LAY['cart'] + 50
    if put < 1 and t < B[176]:
        bx = x + (-1 if flipK else 1) * 1.2 * u
        by = GY - 1.3 * u
        k = put
        px, py = lerp(bx, jx, k), lerp(by, top, k) - 120 * math.sin(k * math.pi)
        jar(px, py, .75, glowK=.4 + .6 * landK(t, 172, .16), bloom=landK(t, 175, .16), key='s33jar', t=t)
        if k < .3:
            handDot(px - 36, py - 40, PAL['clay'], 10)
            handDot(px + 36, py - 40, PAL['clay'], 10)
        if 0 <= t - (B[175] - .04) < .4:
            sparkles(t, 175, 8, px - 90, py - 160, px + 90, py - 20, 18, '#FFFFFF')
    else:
        jar(jx, top, .75, glowK=1.0, bloom=1.0, key='s33jar', t=t)
        ck = landK(t, 177, .14)
        glassBell(jx, lerp(top - 260, top, ck), 82, key='s33clo')
        if t >= B[177] - .04 and t < B[178]:
            stamp('叮', jx + 110, top - 160, 56, '#FFE7A0', bage(t, 177), rot=.1)
        if t >= B[178] - .04:
            sparkles(t, 33, 10, jx - 140, top - 220, jx + 140, top + 10, 18, '#FFFFFF')
    if t >= B[173] - .04 and t < B[174]:
        a = t - (B[173] - .04)
        speedLines(t, 12, x - 300, GY - 420, W + 200, GY - 80, L=200, col='#FFFFFF', a=.7, seed=33)
        for i in range(4):
            ginkgoLeaf(1400 - 900 * a * (1 + i * .2), GY - 300 + i * 60 + 40 * math.sin(a * 9 + i), 18, rot=a * 8 + i, key=f's33lf{i}')
    if t >= B[174] - .3 and t < B[175]:
        a = t - (B[174] - .3)
        puff(x + 40, GY - 13 * u, 22, '#9AA3B8', key='s33cl', a=.95)
        dy_ = min(a / .3, 1)
        paint(ellPts(x + 40, lerp(GY - 12 * u, GY - 8.2 * u, dy_), 10, 15, 10), wash='#BFE6F7', ink=INK, sw=.5)
    if hug > 0:
        floatHearts(t, 33, 6, x - 100, GY - 520, x + 340, GY - 300, 18)
    camEnd()


# S34 83.55–85.40 · his head is full of her: a thought cloud fills with tiny hers until it bursts
def s34(t, lt, dur):
    cam(t, 960, 540, 1.0)
    sunburst(960, 560, '#FFD6E4', '#FFC2D6', 20, t * .15)
    x, u = 960, 38
    keys = [[0, 'thinking', {'emote': None}], [ek(181), 'love', {'tint': None}], [ek(183), 'dizzy', {'emote': None}]]
    o = heO(t, keys, view='front', aL=.3, aR=.3)
    him(x, GY + 40, u, o)
    bulge = 1 + .08 * hitK(t, 183, .2)
    ck = clamp((t - (B[180] - .045)) / .16)
    thoughtCloud(960, 300, 1000 * bulge, 460 * bulge, ck, key='s34tc', col='#FFFFFF', tail=(x, GY + 40 - 8.6 * u))
    n = [0, 1, 4, 13][max(0, lastBeat(t, [180, 181, 182, 183]))]
    spots = [(960, 320)] + [(760, 260), (1160, 260), (960, 430)] + [(600, 360), (1320, 360), (820, 430), (1100, 430), (700, 190),
                                                                     (1220, 190), (960, 180), (520, 260), (1400, 260)]
    for i in range(n):
        k_ = backOut(clamp((t - (B[181 if i == 0 else 182 if i < 4 else 183] - .045)) / .14))
        sx, sy = spots[i]
        push()
        translate(sx, sy + 40)
        scale(k_ * bulge)
        miniHer(0, 0, 11, t, i)
        pop()
    if t >= B[183] - .04:
        stamp('满了！', 1500, 140, 80, HOT, bage(t, 183), rot=.1)
        impactLines(960, 340, 520, 640, 18, t, '#FFFFFF', 's34imp', 1.4)
    camEnd()


# S35 85.40–87.26 · I need therapy: he sits on the clinic stool, the monitor beats hearts, 「相思」 stamp, prescription 「一杯她」
def s35(t, lt, dur):
    cam(t, 960, 540, 1.0)
    clinicWall(t, key='s35cl')
    wallClock(1600, 170, 60, t, key='s35clk')
    mode = 'hearts' if t >= B[185] - .04 else 'beat'
    monitorBox(980, 150, 460, 270, key='s35mon')
    ecgTrace(994, 240, 432, 170, t, mode, [B[k] for k in range(180, 190)], col='#FF8FB0' if mode == 'hearts' else '#7CF29A', sw=4)
    text('心率', 1050, 190, 34, '#7CF29A', shadow=False)
    if mode == 'hearts':
        paint(heartPts(1390, 190, 22, 16), wash='#FF6F7A', ink=None)
    x, u = 640, 34
    sk = stool(x, 900, .8, cushion='#7FB8B0', key='s35st')
    land = landK(t, 184, .16)
    keys = [[0, 'nervous', {'emote': None}], [ek(185), 'love', {'tint': None}], [ek(186), 'surprised', {'emote': None}], [ek(187), 'happy']]
    o = heO(t, keys, view='q', aL=.3, aR=.3)
    if land < 1:
        o['dy'] = (o.get('dy') or 0) - 2.5 * (1 - land)
    seat(him, x, sk, u, o)
    if t >= B[186] - .045:
        rubberStamp('相思', 1210, 560, 90, t - B[186], col='#E0344E', rot=-.15)
    rk = clamp((t - (B[187] - .045)) / .16)
    if rk > 0:
        push()
        translate(1080, 790)
        scale(backOut(rk))
        rotate(.05)
        boilSeed('s35rx')
        paint(rectPts(-200, -110, 400, 220), wash='#FFFDF6', ink=INK, sw=1.0)
        text('药方', -110, -60, 40, '#2F8C55', face=WENKAI, shadow=False)
        text('一杯她', 30, 20, 76, HOT, face=WENKAI, shadow=False)
        line(-170, 80, 170, 80, '#C9C1D6', 1, 3)
        pop()
    camEnd()


# S36 87.26–89.11 · closing time: he wipes the counter, the lights go out strand by strand, the lamp too; 「叮铃」 — a warm light
def s36(t, lt, dur):
    cam(t, 960, 560, 1.0)
    lamp_ = 1 - landK(t, 190, .08)
    lay = corner(t, 'night', lights=lamp_, lights2=1 - landK(t, 189, .08), lamp_=lamp_, cartLit=lamp_, key='cn36')
    x, u = LAY['he'], U_WIDE + 2
    keys = [[0, 'sad'], [ek(190), 'sad', {'eyes': 'closed'}], [ek(191), 'surprised', {'emote': '!', 'lookX': 1}]]
    o = heO(t, keys, view='q', aR=1.0, aL=.2)
    him(x, GY, u, o)
    hx, hy = nearHand(x, GY, u, o, LAY['cart'])
    wipe = math.sin(clamp((t - (B[188] - .1)) / .5) * math.pi * 2) * 30
    paint(rrPts(hx - 30 + wipe, hy - 14, 60, 26, 8), wash='#FFFFFF', fill='#DCE6FF', fillOp=50, ink=INK, sw=.6)
    handDot(hx + wipe * .5, hy, PAL['clay'], 9)
    if 0 <= t - B[188] < .5:
        sparkle(hx + 60, hy - 30, 16, '#FFFFFF', 1 - (t - B[188]) / .5)
    dk = .78 * landK(t, 190, .08)
    wk = clamp((t - (B[191] - .045)) / .12)
    darkness(dk, [(1640, 640, 360, wk), (x + 60, GY - 160, 180, .25)])
    if wk > 0:
        glow(1640, 640, 260, '#FFD27A', .6 * wk)
        stamp('叮铃', 1640, 360, 70, '#FFE7A0', bage(t, 191), rot=.1)
    camEnd()


# S37 89.11–92.83 · she is back: lights on, he freezes, a sugar cube, his bitter cup, plop, heart ripple, 「甜」, laughter
def s37(t, lt, dur):
    cam(t, lerp(1120, 1220, ease(lt / dur)), 580, lerp(1.12, 1.25, ease(lt / dur)))
    lay = corner(t, 'night', key='cn37', cartX=600, stool_=False)
    tt = lay['table']
    u = U_WIDE + 2
    # her
    sx = LAY['she']
    kH = [[0, 'happy'], [ek(194), 'smug'], [ek(197), 'love'], [ek(199), 'laugh']]
    oH = sheO(t, kH, view='q', flip=True, aL=.3 + 1.2 * hitK(t, 192, .4), aR=.3)
    backpack(sx, GY, u, oH, col='#7FB8E6', key='s37bp')
    her(sx, GY, u, oH)
    # him: freezes (k193), steps to the table (k193->k195), holds out his cup (k195), sips (k198)
    walk = ease(clamp((t - (B[193] + .05)) / (B[195] - B[193] - .25)))
    x = lerp(960, 1040, walk)
    kM = [[0, 'neutral'], [ek(193), 'surprised', {'emote': None}], [ek(195), 'hopeful'], [ek(198), 'happy', {'eyes': 'heart', 'blush': .9}],
          [ek(199), 'laugh']]
    oM = heO(t, kM, view='q')
    if 0 < walk < 1:
        oM.update(move('walk', t))
        oM['draw'] = apron('q')
    hold = landK(t, 195, .16)
    sip = landK(t, 198, .16) * (1 - seg(t, B[198] + .3, B[198] + .5))
    oM['aR'] = .25 + .2 * hold + .35 * sip
    oM['aL'] = .25 + .2 * hold + .35 * sip
    him(x, GY, u, oM)
    hx, hy = nearHand(x, GY, u, oM, LAY['table'])
    cx_, cy_ = hx + 4, hy + 30
    cup(cx_, cy_, .5, fill=1, key='s37cup', saucer=False, steam=.6, t=t, steamCol='#6A4A3A' if t < B[196] else None, rot=-.5 * sip)
    handDot(cx_ - 8, cy_ - 18, PAL['clay'], 9)
    if t >= B[193] - .04:
        stamp('！', x + 1.5 * u, GY - 10.6 * u, 90, '#FFE36E', bage(t, 193), rot=.05, life=.9)
    # the sugar cube: lands on the table (k194), hops into his cup (k196)
    cubeT = (LAY['table'] - 10, tt - 18)
    if t >= B[194] - .2:
        if t < B[196] - .3:
            k = clamp((t - (B[194] - .2)) / .2)
            hx2, hy2 = nearHand(sx, GY, u, oH, LAY['table'])
            p = arcPt([hx2, hy2], cubeT, 60, k)
            sugarCube(p[0], p[1], 18, rot=(1 - k) * 2, key='s37sc')
            if k >= 1:
                sparkle(cubeT[0] + 26, cubeT[1] - 30, 16 * hitK(t, 194, .2), '#FFFFFF', 1)
        elif t < B[196]:
            k = clamp((t - (B[196] - .3)) / .3)
            p = arcPt(cubeT, (cx_, cy_ - 46), 130, k)
            sugarCube(p[0], p[1], 18, rot=k * 6, key='s37sc')
    if t >= B[196] - .04:
        a = t - B[196]
        splash(cx_, cy_ - 46, a, .7, COFFEE)
        if a < .5:
            stamp('扑通', cx_ + 120, cy_ - 210, 54, '#FFFFFF', bage(t, 196), rot=.1, life=.5)
    rk = clamp((t - (B[197] - .12)) / .3)
    if rk > 0:
        for j in range(3):
            rr = 30 + 120 * clamp(rk - j * .2)
            if rr > 30:
                hp = heartPts(cx_, cy_ - 120 - j * 10, rr * .5, 22)
                G.c.drawPath(eng._path(hp), skia.Paint(AntiAlias=True, Color=skcol('#FF8FB0', .8 * (1 - clamp(rk - j * .2))),
                                                       Style=skia.Paint.kStroke_Style, StrokeWidth=5))
    if t >= B[198] - .04:
        stamp('甜！', x - 60, GY - 12 * u, 100, HOT, bage(t, 198), rot=-.1)
    if t >= B[199] - .04:
        floatHearts(t, 37, 10, x - 200, GY - 600, sx + 200, GY - 300, 20)
    camEnd()


# S38 92.83–95.13 · the end: both on stools at the little table, the board says 「今日：加糖」; cups clink; steam hearts; freeze; fade
def s38(t, lt, dur):
    cam(t, lerp(1000, 960, ease(lt / dur)), 560, lerp(1.12, 1.0, ease(lt / dur)))

    def board(bx, by, bw, bh):
        cx = bx + bw / 2
        chalkText('今日：', cx, by + 110, 64, writeK(t, 200, .26))
        chalkText('加糖', cx, by + 220, 96, writeK(t, 200, .26), col='#FFB3C6')
        hp = heartPts(cx, by + 310, 26, 18)
        chalkLine(hp + [hp[0]], writeK(t, 201, .26), '#FFB3C6', .9)
    lay = corner(t, 'night', key='cn38', board=board, cartX=740, boardX=330, tableX=1315, stool_=False)
    tt = lay['table']
    u = U_WIDE
    st1 = stool(1130, GY, .8, cushion='#F2A65A', key='s38st1', night=.8)
    st2 = stool(1500, GY, .8, cushion=PINK, key='s38st2', night=.8)
    clink = landK(t, 201, .16) * (1 - seg(t, B[201] + .3, B[201] + .6))
    kM = [[0, 'happy'], [ek(201), 'laugh'], [ek(203), 'happy', {'eyes': 'heart', 'blush': .9}]]
    oM = heO(t, kM, view='q', aR=.6 + .6 * clink, aL=.3)
    kH = [[0, 'happy'], [ek(201), 'laugh'], [ek(203), 'love']]
    oH = sheO(t, kH, view='q', flip=True, aL=.6 + .6 * clink, aR=.3)
    if t >= B[203] - .04:
        for o in (oM, oH):
            o.update(dy=0, sq=0)
    seat(him, 1130, st1, u, oM)
    seat(her, 1500, st2, u, oH)
    h1 = nearHand(1130, st1 + 2 * u, u, oM, 1315)
    h2 = nearHand(1500, st2 + 2 * u, u, oH, 1315)
    cup(h1[0] + 8, h1[1] + 16, .42, fill=1, key='s38c1', saucer=False, steam=.6, t=t)
    handDot(h1[0] - 4, h1[1], PAL['clay'], 8)
    cup(h2[0] - 8, h2[1] + 16, .42, fill=1, key='s38c2', saucer=False, steam=.6, t=t)
    handDot(h2[0] + 4, h2[1], HER['col'], 8)
    if t >= B[201] - .04 and t < B[202]:
        mx, my = (h1[0] + h2[0]) / 2, min(h1[1], h2[1]) - 20
        sparkle(mx, my, 40 * (1 - seg(t, B[201], B[201] + .4)), '#FFE36E', 1)
        stamp('叮', mx, my - 110, 60, '#FFE7A0', bage(t, 201), rot=.1)
    hk = clamp((t - (B[202] - .32)) / .28)
    if hk > 0:
        mx = (h1[0] + h2[0]) / 2
        for side in (-1, 1):
            pts = [[mx + side * 120, min(h1[1], h2[1]) - 40], [mx + side * 90, min(h1[1], h2[1]) - 130], [mx + side * 20, min(h1[1], h2[1]) - 200]]
            pa = skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .8), Style=skia.Paint.kStroke_Style, StrokeWidth=6, StrokeCap=skia.Paint.kRound_Cap)
            p = skia.Path()
            p.moveTo(*pts[0])
            p.quadTo(pts[1][0], pts[1][1], lerp(pts[0][0], pts[2][0], hk), lerp(pts[0][1], pts[2][1], hk))
            G.c.drawPath(p, pa)
        if hk >= 1:
            paint(heartPts(mx, min(h1[1], h2[1]) - 250, 44 * backOut(clamp((t - (B[202] - .04)) / .14)), 22), wash=HOT, ink=INK, sw=.8)
    if t >= B[203] - .04:
        a = t - (B[203] - .04)
        sparkles(t, 38, 14, 900, 300, 1700, 800, 18, '#FFE36E')
        if a < .2:
            flash(.25 * (1 - a / .2))
    camEnd()
