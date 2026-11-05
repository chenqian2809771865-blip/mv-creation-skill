# story.py: 《东西》 shots S01–S16 (one per 4-beat bar, every beat carries a visible event). Shot data: storyboard.py.
# 疑心病 Clawd couple (him clay + shop apron; her pink with the white flower), watercolour + boiling ink.
import math
from eng import *
import eng
from clawd import *
from props import bubble, stamp, sparkle, sparkles, impactLines, stripes, sunburst, puff, floatHearts, bush, tree, hills, lamp
from sets import sky, sunDisc, sea, palm, gull
from sets2 import seat
from common import *
from dx import *
from dx import _pa

U = 34          # medium-shot scale


def emH(t, keys, **kw):
    o = emotions(t, keys, HER)
    o.update(kw)
    return o


def emM(t, keys, **kw):
    o = emotions(t, keys, ME)
    o.update(kw)
    return o


def hitK(t, k, d=.12):
    """1 on the beat frame, decaying after"""
    a = t - (B[k] - .04)
    return 0.0 if a < 0 else math.exp(-a / d)


def landK(t, k, d=.16):
    """0..1 progress that reaches 1 on beat k (motion that arrives on the beat)"""
    return clamp((t - (B[k] - d)) / d)


def ek(k):
    """emotion key time: a little before the beat so the new face is fully there on the beat frame"""
    return B[k] - .06


def angSteps(t, ks, vals, d=.22):
    """angle that swings to vals[i+1] on beat ks[i] with a little overshoot"""
    v = vals[0]
    for i, k in enumerate(ks):
        tb = B[k] - d * .55
        if t >= tb:
            v = lerp(vals[i], vals[i + 1], backOut(clamp((t - tb) / d)))
    return v


def heroShadow(x, y, u, a=1.0):
    paint(ellPts(x, y, u * 5.4, u * .9, 20), fill=INK, fillOp=80 * a, bleed=.25, tex=.3, border=.1, ink=None)


# =====================================================================================
# S01 0–k6 · 示例: the phone on the counter wakes up; her messages land one per beat
MSGS = [('在吗？', 2), ('示例歌词占位文', 3), ('很急！！', 4), ('快回我', 5)]
PHX, PHY, PHS = 1130, 470, .86


def chatRows(t, sx, sw_, y0, rows, size=46):
    """rows: list of (side, text|callable, k, height); returns nothing (positions stack from y0)"""
    y = y0
    for side, txt, k, h in rows:
        kk = pk(t, k, .16) if isinstance(k, int) else k
        if callable(txt):
            txt(y, kk)
        else:
            chatMsg(sx, sw_, y, side, txt, kk, size, key=f'cm{k}{side}')
        y += h


def s01(t, lt, dur):
    CLOCK[0] = '10:24'
    cam(t, 960, 540, lerp(1.0, 1.05, ease(lt / dur)))
    counterTop(t)
    jx, jy = shakeAmt(t, B[5] - .02, 14, 13)
    bx, by = shakeAmt(t, B[1] - .02, 8, 16)
    jx, jy = jx + bx, jy + by

    def page(sx, sy, sw_, sh):
        if t < B[2] - .04:
            on = clamp((t - (B[0] - .1)) / .1)
            lockScreen(t, sx, sy, sw_, sh, on=on, banner=pk(t, 1, .2))
            return
        chatPage(t, sx, sy, sw_, sh, HERNAME)
        rows = [('L', m, k, 140) for m, k in MSGS]
        chatRows(t, sx, sw_, sy + 215, rows, size=52)
        # typing dots under the last message until it lands
        if B[4] <= t < B[5] - .04:
            wx.avatarBox(sx + 64, sy + 215 + 3 * 140 + 40, 38, 'her', 'happy', key='typav')
            push()
            translate(sx + 120, sy + 215 + 3 * 140 + 6)
            scale(1.2)
            typingDots(0, 0, t, 1)
            pop()

    phoneTop(t, page, PHX, PHY, PHS, (jx, jy))
    # buzz marks around the phone (k1 notification, k5 「快回我」)
    for k, amp in ((1, .8), (5, 1.0)):
        h = hitK(t, k, .3) * amp
        if h > .05:
            for d in (-1, 1):
                for i in range(3):
                    xx = PHX + d * (290 + i * 26)
                    line(xx, PHY - 120 + i * 70, xx + d * 16, PHY - 90 + i * 70, INK, h, 4)
    # unread badge on the phone corner
    n = lastBeat(t, [2, 3, 4, 5]) + 1
    if n > 0:
        badge(PHX + 230, PHY - 410, n, pk(t, 2, .14), key='s1bd')
    camEnd()


# =====================================================================================
# S02 k6–k10 · 示例歌词: he plays it cool, plucking a daisy — 回 / 不回 / 回 / 回！
CTR = (380, 800, 700)        # counter x0, x1, top (he stands beside it, legs visible)


def daisyHeld(hx, hy, petals, t, key='dz'):
    """a small daisy held at (hx, hy): stem up 110 px, `petals` petals left"""
    hx2, hy2 = hx + 14, hy - 160
    boilSeed(key + 's')
    inkLine([[hx, hy], [hx + 8, hy - 80], [hx2, hy2]], 2.0, '#5E9E4E', 'ink', .5)
    paint(ellPts(hx + 18, hy - 74, 22, 8, 10, 0, -.6), wash='#7FB86A', ink=INK, sw=.5)
    n = 4
    for i in range(petals):
        a = -math.pi / 4 + i / n * TAU
        boilSeed(f'{key}p{i}')
        paint(ellPts(hx2 + math.cos(a) * 40, hy2 + math.sin(a) * 40, 34, 13, 12, 0, a), wash='#FFFDF6', fill='#E8E0CC', fillOp=50, ink=INK, sw=.7)
    paint(ellPts(hx2, hy2, 20, 20, 14), wash='#F2B63A', ink=INK, sw=.7)
    return hx2, hy2


def flyingPetal(x, y, ag, i, key='fp'):
    if ag < 0 or ag > .8:
        return
    k = ag / .8
    px = x + 40 + 200 * k + 50 * math.sin(ag * 9 + i)
    py = y - 30 - 140 * k + 300 * k * k
    a = 1 - seg(k, .6, 1)
    boilSeed(key + str(i))
    paint(ellPts(px, py, 44, 17, 12, 0, ag * 12 + i), wash='#FFFDF6', washOp=int(255 * a), fill='#E8E0CC', fillOp=int(60 * a), ink=INK if a > .5 else None,
          sw=.8)
    if ag < .2:
        for q in range(3):
            line(px - 30 - q * 14, py + 20 + q * 10, px - 50 - q * 14, py + 30 + q * 10, INK, 1 - ag * 5, 3)


def shopWide(t, mapK=0.0, clockMin=24, door=None):
    shopWall(t, mapK=mapK, clockMin=clockMin)
    if door is None:
        shopDoor(t, outside=False)
    else:
        door()


def s02(t, lt, dur):
    cam(t, 960, 540, lerp(1.0, 1.05, ease(lt / dur)))
    shopWide(t)
    hx, hy = 1040, 880
    PET = [6, 7, 8, 9]
    gone = lastBeat(t, PET) + 1
    keys = [[0, 'thinking'], [ek(7), 'smug'], [ek(8), 'thinking'], [ek(9), 'idea']]
    o = emM(t, keys, view='front', aR=1.15, aL=.15 + .1 * math.sin(t * 3), draw=apronHook('front'), emote=None)
    if t >= ek(9):
        o['emote'] = 'bulb'
    him(hx, hy, U, o)
    hxR, hyR = handXY(hx, hy, U, o, 'R')
    fx, fy = daisyHeld(hxR, hyR, 4 - gone, t, 's2dz')
    for i, k in enumerate(PET):
        flyingPetal(fx, fy, t - (B[k] - .04), i, 's2fp')
    x0, x1, top = CTR
    counterFront(x0, x1, top, key='s2ctr')
    counterItems(x0 + 20, top, t, key='s2ci')
    phoneFlat(735, top + 4, 50, lit=1.0, buzz=hitK(t, 7, .2) + hitK(t, 8, .2), key='s2ph')
    # 回 / 不回 bubbles, alternate per beat
    labs = ['回', '不回', '回', '回！']
    j = lastBeat(t, PET)
    if j >= 0:
        k_ = pk(t, PET[j], .16)
        big = j == 3
        bubble(700, 430, labs[j], 64 if not big else 84, tail=(900, 620), k=k_, col='#FFF5E2' if not big else '#FFE36E',
               tcol=INK if j % 2 == 0 else '#8A7F96', key=f's2b{j}')
        if big:
            sparkles(t, 9, 8, 560, 310, 860, 530, r=14, col='#FFE36E')
    camEnd()


# =====================================================================================
# S03 k10–k14 · 示例歌词占: polite drafts crumpled into the bin one per beat; then 「来！」 goes out
DRAFTS = ['您好～', '请问是什么…', '麻烦您了！']
BIN = (1420, 880)


def draftCard(x, y, txt, k, key='dc'):
    if k <= .01:
        return
    p = backOut(k)
    push()
    translate(x, y)
    scale(p)
    rotate(-.04)
    boilSeed(key)
    paint(rectPts(-190, -110, 380, 220, 2), wash='#FFFDF6', fill='#EDE5D2', fillOp=40, ink=INK, sw=1)
    for q in range(4):
        line(-160, -60 + q * 44, 160, -60 + q * 44, '#C9C1D6', .8, 2)
    text('草稿', -150, -86, 24, '#9A8FA8', align='left', shadow=False, face=WENKAI)
    text(txt, 0, 4, 52, '#5A4A6A', shadow=False, face=WENKAI)
    pop()


def s03(t, lt, dur):
    cam(t, 1000, 600, lerp(1.28, 1.33, ease(lt / dur)))
    shopWall(t, plaque=False)
    shopDoor(t, outside=False, sign=None, key='s3door')
    hx, hy = 1040, 880
    keys = [[0, 'nervous'], [ek(11), 'confused'], [ek(12), 'nervous'], [ek(13), 'happy', {'eyes': 'shine'}]]
    o = emM(t, keys, view='q', flip=True, draw=apronHook('q', flip=True), aL=.2)
    up = landK(t, 13, .14)
    o['aR'] = lerp(o.get('aR', .2), 1.3, up)
    him(hx, hy, U, o)
    x0, x1, top = CTR
    # bin (back rim first)
    wastebasket(BIN[0], BIN[1], 150, 120, key='s3wb', back=True)
    counterFront(x0, x1, top, key='s2ctr')
    counterItems(x0 + 20, top, t, key='s2ci')
    # cards: card i is up from its beat until the next beat, then it becomes a ball flying into the bin
    CK = [10, 11, 12, 13]
    for i, txt in enumerate(DRAFTS):
        tin, tout = B[CK[i]], B[CK[i + 1]]
        T0, T1 = tout - .54, tout - .4           # crumple, then a 0.36 s throw that drops into the bin on the next beat
        if t < T0:
            draftCard(600, 380, txt, 1.0 if i == 0 else pk(t, CK[i], .16), key=f's3d{i}')
        elif t < T1:
            c_ = seg(t, T0, T1)
            push()
            translate(600, 380)
            scale(1 - .75 * c_, 1 - .65 * c_)
            rotate(c_ * 1.2)
            translate(-600, -380)
            draftCard(600, 380, txt, 1.0, key=f's3d{i}')
            pop()
        else:
            a = t - T1
            f = clamp(a / .36)
            bx = lerp(600, BIN[0], f)
            by = lerp(380, BIN[1] - 150, f) - 260 * math.sin(f * math.pi)
            if f < 1:
                paperBall(bx, by, 44, a * 12, key=f's3b{i}')
            else:
                paperBall(BIN[0] - 30 + i * 30, BIN[1] - 128 + (i % 2) * 6, 40, i, key=f's3b{i}')
    jb = max(hitK(t, 11, .12), hitK(t, 12, .12), hitK(t, 13, .12))
    push()
    translate(BIN[0], BIN[1])
    scale(1 + .06 * jb, 1 - .06 * jb)
    translate(-BIN[0], -BIN[1])
    wastebasket(BIN[0], BIN[1], 150, 120, key='s3wb', back=False)
    pop()
    for k in (11, 12, 13):
        if B[k] - .04 <= t < B[k] + .45:
            stamp('进！', BIN[0] + 20, BIN[1] - 220, 52, '#E07A4E', t - B[k], rot=.12, life=.45)
    # k13: the phone goes up, 「来！」 is sent
    if up > .01:
        hxR, hyR = handXY(hx, hy, U, o, 'R')
        boilSeed('s3ph')
        push()
        translate(hxR, hyR - 20)
        rotate(.15)
        paint(rrPts(-34, -60, 68, 112, 12), wash='#3D3A52', ink=INK, sw=.8)
        paint(rrPts(-26, -50, 52, 90, 8), wash='#DFF3E8', ink=None)
        pop()
        k_ = pk(t, 13, .16)
        bubble(hxR - 190, hyR - 200, '来！', 80, tail=(hxR - 30, hyR - 70), k=k_, col='#9EE8A8', key='s3go')
        if k_ > .5:
            sparkles(t, 4, 6, hxR - 380, hyR - 320, hxR - 40, hyR - 100, r=14, col='#FFE36E')
    camEnd()


# =====================================================================================
# S04 k14–k18 · 示例歌词: he waits; the bell jiggles; the door swings open on 「欢迎」 — she's there with the parcel
def s04(t, lt, dur):
    cam(t, 1250, 560, lerp(1.04, 1.08, ease(lt / dur)))
    clockMin = 24 if t < B[15] - .04 else 30
    opn = landK(t, 16, .16)
    bellSwing = .45 * math.sin((t - B[15]) * 30 + 1.2) * hitK(t, 15, .3) + .6 * math.sin((t - B[16]) * 22) * hitK(t, 16, .5)
    shopWall(t, clockMin=clockMin, lights=.15 + .85 * landK(t, 14, .1), plaque=False)
    ck15 = hitK(t, 15, .25)
    if ck15 > .05:
        for i in range(3):
            a = -math.pi / 2 + (i - 1) * .6
            line(1340 + math.cos(a) * 72, 215 + math.sin(a) * 72, 1340 + math.cos(a) * 100, 215 + math.sin(a) * 100, INK, ck15, 4)
        for d in (-1, 1):
            line(1490 + d * 40, 250, 1490 + d * 58, 290, INK, ck15, 4)
    sx_, sy_ = 1650, 862
    hx, hy = 1210, 880
    # door + outside first, then her in the doorway, then the frame again on top (shopDoor draws the frame last)
    shopDoor(t, opn=opn, bell=bellSwing, key='s4door')
    if opn > .5:
        ho = emH(t, [[0, 'happy'], [ek(17), 'happy', {'eyes': 'heart'}]], view='q', flip=True, aL=-.2, aR=-.25)
        if t >= B[17] - .04:
            ho['aL'] = 1.5 + .3 * math.sin(t * 14)
        her(sx_, sy_, 30, ho)
        parcel(sx_ - 1.4 * 30, sy_ - 1.6 * 30, 1.7 * 30, key='s4pc')
        # redraw the right post + bell so she is framed by the doorway
        boilSeed('s4door' + 'fr2')
        paint(rectPts(1820, 240, 26, 620), wash=WOODDK, ink=INK, sw=.9)
        paint(rectPts(1480 - 26, 240, 26, 620), wash=WOODDK, ink=INK, sw=.9)
        paint(rectPts(1440, 218, 420, 30), wash=WOODDK, ink=INK, sw=.9)
        doorBell(1490, 266, 30, bellSwing, 's4doorbell')
    doormat(1650, 900, 300, key='s4mat')
    # him behind the counter (right end), facing the door
    bow = es(t, B[17] - .1, B[17] + .1) * (1 - es(t, B[17] + .45, B[17] + .65))
    keys = [[0, 'proud'], [ek(15), 'nervous'], [ek(16), 'surprised', {'emote': None}], [ek(17), 'happy', {'eyes': 'closed'}]]
    o = emM(t, keys, view='q', draw=apronHook('q'))
    if t < B[15] - .04:
        o['lookX'] = .2
    elif t < B[16] - .04:
        o['lookX'], o['lookY'] = .6, -.6
    o['rot'] = (o.get('rot') or 0) + .32 * bow
    him(hx, hy, U, o)
    if t >= B[14] - .04 and t < B[14] + .5:
        sparkles(t, 14, 6, hx - 160, hy - 160, hx + 160, hy - 40, r=16 * hitK(t, 14, .3) + 4, col='#FFE36E')
    counterFront(380, 980, 700, key='s4ctr')
    counterItems(400, 700, t, key='s2ci', bell=hitK(t, 16, .3))
    phoneFlat(900, 704, 50, lit=.6, key='s4ph')
    # k15 knock marks on the door, k16 「叮铃」 + 欢迎光临 bubble
    kn = hitK(t, 15, .22)
    if kn > .05 and opn < .1:
        for i in range(3):
            a = -.6 + i * .6
            line(1650 + math.cos(a) * 70, 690 + math.sin(a) * 70, 1650 + math.cos(a) * 110, 690 + math.sin(a) * 110, INK, kn, 4)
        text('咚咚', 1650, 610, 54, '#8E5E3A', stroke='#FFF5E2', strokeW=8, a=kn, shadow=False)
    if t >= B[16] - .04:
        stamp('叮铃～', 1600, 200, 56, '#F2C53D', t - B[16], rot=.12, life=.9)
        bubble(930, 400, '欢迎光临！', 66, tail=(1120, 580), k=pk(t, 16, .16), col='#FFF5E2', key='s4wel')
    if t >= B[17] - .04:
        floatHearts(t - B[17], 7, 6, 1450, 380, 1750, 560, s=18)
    camEnd()


# =====================================================================================
# S05 k18–k22 · 示例歌词占 位文字示例歌词占位文: sunset island, gull, waves
def islandScene(t, sunK=1.0, key='is', u=30, people=True, gullK=None, splash=None):
    c1 = mixCol('#F7C6D8', '#FFB36B', sunK)
    c2 = mixCol('#FFE8D0', '#FFE08A', sunK)
    gradient(c1, c2, -200, 640)
    sunDisc(1560, 600 - 30 * sunK, 60 + 34 * sunK, col='#FFF2B8', glowCol='#FFB86A', a=1, key=key + 'sun')
    sea(620, '#6FB7D9', '#3D7FA8', t, key=key + 'sea')
    # sun path on the water
    for i in range(7):
        yy = 650 + i * 34
        w = 120 - i * 10 + 30 * sunK
        line(1560 - w / 2, yy, 1560 + w / 2, yy, '#FFE7A0', .55 + .3 * sunK, 5)
    # island
    boilSeed(key + 'isl')
    paint(ellPts(900, 790, 620, 130, 40), wash='#F2D9A0', fill='#D9B878', fillOp=60, ink=INK, sw=1.1)
    paint(ellPts(900, 770, 560, 92, 36), wash='#F7E3B4', ink=None)
    palm(560, 760, 46, key=key + 'palm', lean=-.18, t=t)
    palm(1350, 790, 30, key=key + 'palm2', lean=.22, t=t)
    for i in range(5):
        G.c.drawCircle(700 + i * 120 + 30 * hash1(i), 820 + 14 * hash1(i * 3), 6, _pa('#FFFDF6'))
    paint(starPts(1180, 820, 22, .45, 5), wash='#FF8F7A', ink=INK, sw=.6)
    if people:
        s_ = 712
        heroShadow(945, s_ + 2.2 * u, u * 1.9)
        boilSeed(key + 'log')
        paint(rrPts(610, s_, 670, 1.5 * u, .7 * u), wash='#B98A5A', fill='#8E6238', fillOp=70, ink=INK, sw=1)
        paint(ellPts(1270, s_ + .75 * u, .45 * u, .75 * u, 14), wash='#E3C08A', ink=INK, sw=.7)
        for q in range(4):
            line(660 + q * 150, s_ + 12, 760 + q * 150, s_ + 16, '#8E6238', .8, 2)
        o1 = emM(t, [[0, 'happy'], [ek(19), 'happy', {'eyes': 'heart', 'blush': .8}]], view='q', aL=.3, aR=.6)
        seat(him, 780, s_, u, o1)
        o2 = emH(t, [[0, 'happy'], [ek(21), 'laugh']], view='q', flip=True, aL=.3, aR=.6)
        seat(her, 1110, s_, u, o2)


def s05(t, lt, dur):
    cam(t, 960, 540, lerp(1.0, 1.05, ease(lt / dur)))
    sunK = es(t, B[19] - .1, B[19] + .2)
    islandScene(t, .25 + .75 * sunK)
    # k20 gull + sparkles on the water
    ga = t - (B[20] - .12)
    if ga > 0:
        gx = 1900 - 1500 * clamp(ga / 1.2)
        smallBird(gx, 300 + 30 * math.sin(ga * 4), 52, ga * 14)
        smallBird(gx + 170, 360 + 30 * math.sin(ga * 4 + 1), 38, ga * 14 + 1)
        sparkles(t, 20, 10, 1000, 640, 1700, 760, r=14 * hitK(t, 20, .5) + 6, col='#FFFFFF')
    # k21 wave splash on the shore
    sa = t - (B[21] - .04)
    if sa > 0 and sa < .9:
        k = clamp(sa / .5)
        for i in range(9):
            a = -math.pi * (.15 + .7 * i / 8)
            r = 40 + 150 * easeOut(k)
            puff(1420 + math.cos(a) * r, 800 + math.sin(a) * r * .8, 10 * (1 - k * .6), col='#FFFFFF', key=f's5sp{i}', a=1 - k)
        if sa < .5:
            for i in range(4):
                sparkle(1360 + i * 50, 690 - 40 * (i % 2), 18 * (1 - sa * 2), '#FFE36E')
    camEnd()
    dreamFrame(1, t, key='dfa')


# =====================================================================================
# S06 k22–k26 · 示例歌词占位文字: the giant bamboo-dragonfly lifts the basket; clouds, birds, she points ahead
def basketPeople(t, u, keysM, keysH, pointK=0.0, beret=0.0, bagK=0.0):
    def f(bx, rim):
        y = rim + 2.0 * u
        oM = emM(t, keysM, view='q', noShadow=True, aL=.4, aR=.5)
        if bagK > .01:
            oM['aL'] = lerp(oM['aL'], 1.75, bagK)
        him(bx - 5.3 * u, y, u, oM)
        oH = emH(t, keysH, view='q', flip=False, noShadow=True, aL=.4, aR=.5)
        if pointK > .01:
            oH['aR'] = lerp(oH['aR'], 1.25, pointK)
        if beret > .01:
            oH['hat'] = ['beret', 'flower'] if beret > .5 else 'flower'
        her(bx + 5.3 * u, y, u, oH)
        if bagK > .01:
            hxL, hyL = handXY(bx - 5.3 * u, y, u, oM, 'L')
            L = 190 * backOut(bagK)
            baguette(hxL + 18, hyL - L * .42, L, -math.pi / 2 + .22, key='bgt')
    return f


def s06(t, lt, dur):
    cam(t, 960, 540, 1.0)
    gradient('#8EC9F0', '#E8F6FF', -200, 1200)
    glow(1650, 120, 420, '#FFF4C8', .8)
    # far cloud layer
    for i in range(6):
        x = (300 + i * 420 - lt * 160) % 2600 - 300
        puff(x, 200 + 90 * (i % 3), 40 + 10 * (i % 2), col='#FFFFFF', key=f's6fc{i}', ink=True)
    # the island dropping away below
    rise = easeOut(seg(t, B[22] - .05, B[22] + .7))
    iy = 2000
    if iy < 1300:
        push()
        translate(0, iy - 760)
        boilSeed('s6isl')
        paint(ellPts(900, 900, 520, 110, 40), wash='#6FB7D9', ink=None)
        paint(ellPts(900, 860, 260, 50, 30), wash='#F2D9A0', ink=INK, sw=1)
        palm(820, 850, 26, key='s6palm', lean=-.18, t=t)
        pop()
    cy = lerp(600, 440, rise) + 12 * math.sin(t * 3.2)
    u = 25
    people = basketPeople(t, u, [[0, 'excited'], [ek(24), 'happy']], [[0, 'happy'], [ek(25), 'excited']], pointK=landK(t, 25, .14))
    speedLines(t, 14, -100, 80, 2100, 1000, L=180, col='#FFFFFF', a=.7 * (.4 + .6 * rise), seed=3)
    bambooCopter(960, cy, 38, t, spin=1.0, key='s6bc', people=people, basket='swing')
    # whoosh stamp + vertical speed lines under the basket at liftoff
    lv = hitK(t, 22, .35)
    if lv > .05:
        for i in range(4):
            x = 960 - 210 + i * 140
            line(x, cy + 260 + 30 * (i % 2), x, cy + 420 + 30 * (i % 2), '#FFFFFF', lv, 6)
    if t < B[22] + .8:
        stamp('呼～', 1360, 760, 72, '#FFFFFF', t - B[22], rot=-.1, life=.55)
    # k23 a big cloud whooshes past in front (low, under the basket)
    ca = t - B[23]
    if -.5 < ca < .6:
        x = 960 - 2900 * ca
        speedLines(t, 6, x + 260, 720, x + 1000, 860, L=240, col='#FFFFFF', a=.95, seed=23, spd=0)
        puff(x, 800, 80, col='#FFFFFF', key='s6cloud')
    # k24 a V of little birds
    ba = t - B[24]
    if -.4 < ba < 1.3:
        bx0 = 1450 - 800 * ba
        for i in range(5):
            smallBird(bx0 + abs(i - 2) * 110, 300 + (i - 2) * 70, 66, ba * 14 + i, col='#3A3550')
    # k25 she points ahead: arrow
    if t >= B[25] - .04:
        a = t - (B[25] - .04)
        stamp('去远方～', 1600, 420, 70, '#E8574A', a, rot=-.05)
        k_ = backOut(clamp(a / .16))
        push()
        translate(1290, 430)
        scale(k_)
        boilSeed('s6arrow')
        paint([[-90, -18], [40, -18], [40, -44], [100, 0], [40, 44], [40, 18], [-90, 18]], wash='#E8574A', ink=INK, sw=1)
        pop()
    camEnd()
    dreamFrame(1, t, key='dfb')


# =====================================================================================
# S07 k26–k30 · 示例歌词占位: landing on a Paris corner; the heart-shaped fog clears off the tower; beret; baguette
def parisBack(t, lights=0.0, fog=1.0, key='pa', towerX=1330, towerY=760, towerH=640):
    gradient('#C9B6E8', '#FFD9C8', -200, 780)
    for i in range(14):
        G.c.drawCircle(hash1(i * 2.3) * W, hash1(i * 4.1) * 380, 2 + 2 * hash1(i), _pa('#FFFFFF', .6))
    # far rooftops
    boilSeed(key + 'roof')
    pts = [[-100, 780]]
    for i in range(22):
        x = -100 + i * 100
        y = 600 + 50 * hash1(i * 1.9)
        pts += [[x, y], [x + 60, y - 30 * hash1(i * 3.1)], [x + 100, y]]
    pts.append([2100, 780])
    paint(pts, wash='#9C8AC0', fill='#7C6AA0', fillOp=60, ink=INK, sw=.8)
    eiffel(towerX, towerY, towerH, lights=lights, t=t, key=key + 'eif')
    if fog > .01:
        G.c.saveLayerAlpha(None, int(255 * clamp(fog)))
        s = 1 + .5 * (1 - fog)
        for i in range(10):
            a = i / 10 * TAU
            hx_ = 16 * math.sin(a) ** 3
            hy_ = -(13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a))
            puff(towerX + hx_ * 17 * s, towerY - 330 + hy_ * 17 * s, 62, col='#FFC2D3', key=f'{key}fog{i}', ink=False)
        boilSeed(key + 'fogh')
        paint(heartPts(towerX, towerY - 400, 330 * s, 34), wash='#FFC2D3', washOp=235, fill='#F7A1B6', fillOp=60, ink=INK, sw=1.4)
        text('？', towerX, towerY - 400, 170, '#FFFFFF', stroke=INK, strokeW=8, shadow=False)
        G.c.restore()
    # street
    flatRect(-200, 760, W + 400, 600, '#D9C2B0')
    for r in range(6):
        y = 780 + r * 40
        for c_ in range(-2, 34):
            x = c_ * 70 + (r % 2) * 35
            paint(rrPts(x, y, 62, 32, 10), wash='#E8D6C4', ink=None)
    line(-200, 760, W + 200, 760, INK, 1, 3)
    # café on the left: wall, door, awning, sign, flower boxes, a little table
    boilSeed(key + 'cafe')
    paint(rectPts(-120, 300, 560, 460), wash='#F3E3C8', fill='#E3CFA8', fillOp=60, ink=INK, sw=1)
    paint(rectPts(150, 470, 150, 290), wash='#4A6E8E', ink=INK, sw=.9)
    G.c.drawCircle(280, 620, 8, _pa(BRASS))
    awning(-120, 440, 380, 80, key=key + 'aw')
    paint(rrPts(-40, 316, 360, 56, 10), wash='#3F4A6E', ink=INK, sw=.8)
    text('CAFÉ  巴黎', 140, 344, 36, '#FFE3B0', shadow=False)
    for fx in (40, 360):
        paint(rectPts(fx - 60, 560, 120, 40), wash='#B9784E', ink=INK, sw=.7)
        for j in range(5):
            G.c.drawCircle(fx - 44 + j * 22, 552, 12, _pa(['#FF6F96', '#FFD36A', '#FFFFFF'][j % 3]))
    lamp(1700, 770, 34, on=.5 + .5 * lights, key=key + 'lamp')
    bush(1820, 780, 40, key=key + 'bush')


def s07(t, lt, dur):
    cam(t, 960, 540, lerp(1.02, 1.07, ease(lt / dur)))
    fog = 1 - es(t, B[27] - .2, B[27] + .1)
    lights = landK(t, 27, .1)
    parisBack(t, lights=lights, fog=fog)
    land = landK(t, 26, .18)
    by = 596 - 140 * (1 - easeIn(land)) + 10 * math.sin(t * 3) * land
    if land >= 1:
        sq = hitK(t, 26, .1)
        by += 10 * sq
    u = 25
    people = basketPeople(t, u, [[0, 'happy'], [ek(29), 'excited']], [[0, 'surprised'], [ek(27), 'starstruck'], [ek(28), 'happy']],
                          beret=landK(t, 28, .1), bagK=pk(t, 29, .16))
    bambooCopter(880, by, 38, t, spin=.6, key='s6bc', people=people, basket='swing')
    # landing dust
    da = t - (B[26] - .04)
    if 0 < da < .8:
        for i in range(8):
            d = -1 if i % 2 else 1
            puff(880 + d * (260 + 140 * easeOut(da / .8)) + (i // 2) * 30 * d, 820 - (i // 2) * 14, 16 * (1 - da / .8), col='#F3E6D4',
                 key=f's7d{i}', a=1 - da / .8)
        stamp('噗！', 1230, 700, 64, '#FFFFFF', da, rot=.1, life=.7)
    if t >= B[27] - .04:
        stamp('巴黎！', 1330, 160, 70, '#FF6F96', t - B[27], rot=.08, life=1.2)
    if t >= B[28] - .04:
        sparkles(t, 28, 6, 1000, 300, 1180, 420, r=14 * hitK(t, 28, .4) + 4, col='#FFE36E')
    if t >= B[29] - .04:
        floatHearts(t - B[29], 11, 6, 560, 260, 1060, 440, s=16)
    camEnd()
    dreamFrame(1, t, key='dfc')


# =====================================================================================
# S08 k30–k34 · 示例歌词占位文字示例歌: picnic under the tower; babies pop up one / one / two / a bunch
BABIES = [(30, 960, 905, 'him'), (31, 1060, 920, 'her'), (32, 860, 922, 'her'), (32, 1160, 918, 'him'),
          (33, 700, 915, 'him'), (33, 1280, 914, 'her'), (33, 590, 900, 'her'), (33, 1390, 900, 'him')]


def s08(t, lt, dur):
    cam(t, 960, 560, lerp(1.03, 1.07, ease(lt / dur)))
    gradient('#C9B6E8', '#FFD9C8', -200, 700)
    eiffel(1560, 690, 520, lights=1, t=t, key='s8eif')
    eiffel(240, 660, 300, lights=.6, t=t + 1, key='s8eif2', col='#7C6AA0')
    boilSeed('s8lawn')
    flatRect(-200, 660, W + 400, 700, '#A9D98A')
    paint([[-200, 690], [600, 650], [1300, 670], [2200, 640], [2200, 1400], [-200, 1400]], wash='#9ED27A', fill='#79B45B', fillOp=50, ink=INK, sw=1, curv=.4)
    for i in range(30):
        x, y = hash1(i * 1.3) * W, 700 + hash1(i * 2.7) * 300
        G.c.drawCircle(x, y, 5, _pa(['#FFFFFF', '#FFD36A', '#FF9FBA'][i % 3]))
    picnicBlanket(960, 810, 1100, 150, key='s8pic')
    u = 30
    keysM = [[0, 'happy'], [ek(31), 'happy', {'eyes': 'heart', 'blush': .9}], [ek(33), 'excited', {'eyes': 'heart', 'blush': 1, 'emote': None}]]
    keysH = [[0, 'happy'], [ek(32), 'shy'], [ek(33), 'shy', {'aR': 1.65, 'aL': -.4}]]
    for cx_, col in ((740, '#F7D36E'), (1180, '#9AD0EE')):
        boilSeed(f's8cu{cx_}')
        paint(ellPts(cx_, 806, 5.4 * u, 1.3 * u, 24), wash=col, fill=mixCol(col, INK, .25), fillOp=60, ink=INK, sw=1)
        paint(ellPts(cx_, 790, 5.0 * u, .8 * u, 22), wash=mixCol(col, '#FFFFFF', .35), ink=INK, sw=.7)
    oM = emM(t, keysM, view='q')
    seat(him, 740, 790, u, oM)
    oH = emH(t, keysH, view='q', flip=True, hat=['beret', 'flower'])
    seat(her, 1180, 790, u, oH)
    for i, (k, x, y, who) in enumerate(BABIES):
        kk = pk(t, k, .18)
        hop = 1.6 * abs(math.sin((t - B[k]) * 7 + i)) * (1 if t > B[k] + .2 else 0)
        baby(x, y, 10, who, t, kk, key=f's8b{i}', flip=i % 2 == 1, hop=hop)
    n = lastBeat(t, [30, 31, 32, 33])
    if n >= 0:
        cnt = [1, 2, 4, 8][n]
        bubble(960, 360, f'baby ×{cnt}' if n < 3 else 'baby ×一群！', 56 if n < 3 else 64, k=pk(t, [30, 31, 32, 33][n], .16),
               col='#FFF5E2' if n < 3 else '#FFE36E', key=f's8bub{n}')
    if t >= B[33] - .04:
        floatHearts(t - B[33], 21, 10, 560, 420, 1360, 700, s=18)
    camEnd()
    dreamFrame(1, t, key='dfd')
    # k33: her shy poke bursts the dream bubble (pop ring + cracks at the cloud border, top right), flash on k34
    pa_ = t - (B[33] - .04)
    if pa_ >= 0:
        px_, py_ = 1500, 150
        r_ = 40 + 260 * easeOut(clamp(pa_ / .5))
        G.c.drawCircle(px_, py_, r_, _pa('#FFFFFF', .9 * (1 - clamp(pa_ / .6)), 8))
        for i in range(7):
            a = i / 7 * TAU + .4
            L = 60 + 70 * hash1(i)
            inkLine([[px_ + math.cos(a) * 30, py_ + math.sin(a) * 30], [px_ + math.cos(a + .15) * (30 + L * .5), py_ + math.sin(a + .15) * (30 + L * .5)],
                     [px_ + math.cos(a) * (30 + L), py_ + math.sin(a) * (30 + L)]], 1.4, INK, 'ink', 0)
        stamp('啵！', px_ - 40, py_ + 120, 84, '#FF6F96', pa_, rot=-.12)


# =====================================================================================
# S09 k34–k38 · 示例歌词占位文字 示例歌词占位文 字示例歌词 占位文字示例歌词: the parcel opens — a brass compass with only 东 and 西
def s09(t, lt, dur):
    cam(t, 1000, 540, lerp(1.04, 1.08, ease(lt / dur)))
    mapK = es(t, B[36] - .2, B[36] + .05)
    shopWall(t, mapK=mapK, mapRoute=es(t, B[36] - .2, B[36] + .02))
    shopDoor(t, outside=False, signFlip=(B[37], '去旅行啦～'), key='s9door')
    # rays from the compass
    ck = pk(t, 34, .2)
    cx, cy = 1030, 470
    G.c.saveLayerAlpha(None, int(100 * clamp(ck) * (1 - .4 * es(t, B[35], B[36]))))
    sunburst(cx, cy, '#FFE9A0', '#FFF6D8', n=20, rot=t * .2, R=1600)
    G.c.restore()
    oM = emM(t, [[0, 'starstruck'], [ek(36), 'excited'], [ek(37), 'happy', {'eyes': 'heart', 'blush': .8}]], view='q', draw=apronHook('q'))
    him(590, 880, U, oM)
    counterFront(800, 1260, 700, key='s9ctr')
    candyJarTop(870, 704, 34, 's9cj')
    lid = landK(t, 34, .12)
    parcel(cx, 704, 64, lid=lid, key='s9pc')
    # compass rises out of the box
    if ck > 0:
        rise = backOut(ck)
        ang = -math.pi / 2 + (t - B[35]) * 22 if t >= B[35] - .04 else -math.pi / 2
        if t >= B[36] - .2:
            ang = angSteps(t, [36], [-math.pi / 2 + (B[36] - .2 - B[35]) * 22, -math.pi / 2 + 6 * math.pi])
        compass(cx, lerp(660, cy, rise), 140 * rise, ang, t, key='s9cmp', spinBlur=hitK(t, 35, .6) * 1.5, shine=1)
        if t >= B[35] - .04 and t < B[36]:
            sparkles(t, 35, 10, cx - 220, cy - 220, cx + 220, cy + 220, r=16, col='#FFE36E')
    oH = emH(t, [[0, 'proud'], [ek(36), 'excited'], [ek(37), 'happy']], view='q', flip=True, aL=1.3 if t < B[36] else .3, aR=1.2)
    her(1430, 900, 32, oH)
    confetti(t, cx, cy - 40, (t - (B[34] - .04)) / 1.0, seed=34, n=90, spread=900)
    if t >= B[37] - .04:
        stamp('出发！', 1650, 180, 60, '#E8574A', t - B[37], rot=.1)
    camEnd()


# =====================================================================================
# S10 k38–k42 · 示例歌词占位: compass close-up (prop only); 东 = sunrise on the right, 西 = sunset on the left
def miniScene(x, y, w, h, kind, t, k, key='mn'):
    if k <= .01:
        return
    p = backOut(k)
    push()
    translate(x, y)
    scale(p)
    boilSeed(key)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + 12, -h / 2 + 16, w, h), 30, 30, _pa(INK, .25))
    pth = skia.Path()
    pth.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), 30, 30))
    G.c.save()
    G.c.clipPath(pth, skia.ClipOp.kIntersect, True)
    if kind == 'east':
        gradRect(-w / 2, -h / 2, w, h, ['#9FD3F5', '#FFE9B8'])
        sunDisc(0, h * .12, 70, col='#FFF2B8', glowCol='#FFD27A', key=key + 'sun')
        for i in range(10):
            a = -math.pi + i / 9 * math.pi
            line(math.cos(a) * 95, h * .12 + math.sin(a) * 95, math.cos(a) * 140, h * .12 + math.sin(a) * 140, '#FFC94A', 1, 5)
    else:
        gradRect(-w / 2, -h / 2, w, h, ['#5B4A9C', '#FF9A6B'])
        sunDisc(0, h * .16, 70, col='#FFB86A', glowCol='#FF7A5A', key=key + 'sun')
    flatRect(-w / 2, h * .16, w, h, '#7CB86A' if kind == 'east' else '#6A5A8C')
    line(-w / 2, h * .16, w / 2, h * .16, INK, 1, 3)
    o = dict(HER, view='front', boilKey=key + 'her', eyes='happy', mouth='smile', blush=.6, aR=1.4 + .3 * math.sin(t * 10), aL=.2)
    her(-w * .18, h * .4, 13, o)
    boilSeed(key + 'case')
    paint(rrPts(w * .02, h * .4 - 52, 70, 52, 8), wash='#E8574A' if kind == 'east' else '#4A7FD9', ink=INK, sw=.7)
    G.c.restore()
    paint(rrPts(-w / 2, -h / 2, w, h, 30), ink=INK, sw=1.4)
    text(kind == 'east' and '东' or '西', 0, -h / 2 - 50, 72, EAST if kind == 'east' else WEST, stroke='#FFFFFF', strokeW=10, shadow=False)
    pop()


def s10(t, lt, dur):
    cam(t, 960, 500, lerp(1.0, 1.04, ease(lt / dur)))
    # wooden counter, top view (no props: the compass is the star)
    flatRect(-400, -400, W + 800, H + 800, '#C9905E')
    for j in range(-6, 22):
        y = j * 92
        flatRect(-400, y, W + 800, 46, '#C08654', .45)
    wob = .25 * math.sin((t - B[38]) * 16) * math.exp(-(t - B[38]) * 2)
    ang = angSteps(t, [39, 40], [-math.pi / 2 + wob, 0, math.pi])
    blur = 0.0
    if t >= B[41] - .04:
        a = t - (B[41] - .04)
        ang = math.pi + a * 20
        blur = clamp(a * 4)
    elif t < B[39] - .12:
        ang = -math.pi / 2 + wob
    lit = None
    if B[39] - .04 <= t < B[40] - .04:
        lit = ('东', hitK(t, 39, .5) * .7 + .3)
    elif B[40] - .04 <= t < B[41] - .04:
        lit = ('西', hitK(t, 40, .5) * .7 + .3)
    compass(960, 470, 380, ang, t, key='s10cmp', lit=lit, spinBlur=blur, shine=1)
    miniScene(1620, 520, 420, 380, 'east', t, pk(t, 39, .18), key='s10e')
    miniScene(300, 520, 420, 380, 'west', t, pk(t, 40, .18), key='s10w')
    if t >= B[41] - .04:
        impactLines(960, 470, 420, 520, 18, t, col='#FFFFFF', key='s10imp', sw=1.2)
    camEnd()


# =====================================================================================
# S11 k42–k46 · 示例歌词占位文字: the balance tips 东, tips 西, settles level — 「没关系」; he nods 「示例歌～」
def s11(t, lt, dur):
    cam(t, 960, 540, lerp(1.0, 1.04, ease(lt / dur)))
    sunburst(960, 500, '#CDEFE0', '#E8F8EF', n=18, rot=t * .1, R=2000)
    flatRect(-200, 860, W + 400, 400, '#BFE6D2')
    line(-200, 860, W + 200, 860, INK, 1, 3)
    ang = angSteps(t, [42, 43, 44], [0, -.24, .24, 0])
    balance(960, 900, 40, ang, key='s11bal')
    nod = hitK(t, 45, .18)
    oM = emM(t, [[0, 'surprised'], [ek(43), 'confused'], [ek(44), 'happy'], [ek(45), 'happy', {'eyes': 'closed'}]], view='q', aL=.3, aR=.3)
    oM['dy'] = (oM.get('dy') or 0) + 1.2 * nod
    oM['lookX'] = .5 if t < B[43] - .04 else (1 if t < B[44] - .04 else .4)
    backpack(330, 880, 30, oM, col='#4A90D9', key='s11bp1')
    oM['draw'] = strapHook('q')
    him(330, 880, 30, oM)
    oH = emH(t, [[0, 'happy'], [ek(44), 'laugh'], [ek(45), 'happy']], view='q', flip=True, aL=.3, aR=.3)
    backpack(1590, 880, 30, oH, col='#F28CA8', key='s11bp2')
    oH['draw'] = strapHook('q', '#C0637B')
    her(1590, 880, 30, oH)
    if t >= B[44] - .1:
        rubberStamp('没关系', 960, 230, 92, t - B[44], col='#E0344E', rot=-.12)
    if t >= B[45] - .04:
        bubble(420, 420, '示例歌～', 58, tail=(360, 560), k=pk(t, 45, .16), col='#FFF5E2', key='s11b')
        floatHearts(t - B[45], 45, 5, 1450, 420, 1700, 600, s=16)
    camEnd()


# =====================================================================================
# S12 k46–k50 · 示例歌: outside the shop; she points 东, 西, ahead — he turns his head each time; 「出发！」
def outsideStreet(t, key='os', signTxt='去旅行啦～'):
    gradient('#9FD3F5', '#FFF1D6', -200, 760)
    glow(1600, 140, 400, '#FFF4C8', .8)
    for i in range(3):
        puff(300 + i * 640 + 40 * math.sin(t * .5 + i), 160 + 50 * (i % 2), 46, col='#FFFFFF', key=f'{key}cl{i}')
    hills(560, ['#BFE3B0', '#9ED27A'], t, key=key + 'hl')
    # the shop's facade on the left edge
    boilSeed(key + 'fac')
    paint(rectPts(-200, 250, 640, 560), wash='#F6E5C8', fill='#E3CFA8', fillOp=60, ink=INK, sw=1)
    awning(-200, 440, 250, 80, key=key + 'aw', cols=('#E07A4E', '#FFF5E2'))
    paint(rrPts(70, 160, 360, 80, 12), wash='#8E5E3A', ink=INK, sw=1)
    text('小橘杂货铺', 250, 200, 46, '#FFE3B0', shadow=False)
    paint(rectPts(150, 400, 220, 410), wash='#9A6640', fill='#7A4E30', fillOp=60, ink=INK, sw=1)
    doorSign(260, 520, 1.0, '营业中', (-1, signTxt), t, key + 'ds')
    # road + sidewalk
    flatRect(-200, 800, W + 400, 500, '#D9CDB8')
    paint([[-200, 800], [2200, 800], [2200, 1300], [-200, 1300]], ink=INK, sw=1)
    for i in range(12):
        flatRect(-100 + i * 200, 900, 110, 14, '#FFFFFF', .8)
    bush(560, 800, 40, key=key + 'b1')
    tree(1780, 800, 60, key=key + 't1')


def s12(t, lt, dur):
    cam(t, 960, 540, lerp(1.02, 1.06, ease(lt / dur)))
    outsideStreet(t)
    lit = (pk(t, 46, .12) * (1 - pk(t, 47, .12)), pk(t, 47, .12) * (1 - pk(t, 48, .12)))
    signPost(1060, 880, 560, lit, key='s12sp')
    u = 32
    jump = 0.0
    if t >= B[49] - .2:
        a = t - (B[49] - .2)
        jump = max(0, math.sin(clamp(a / .55) * math.pi)) * 2.5 if a < .55 else 0
    # her (left): points right (东) on k46, left (西) on k47, holds the compass up on k48
    j = lastBeat(t, [46, 47, 48, 49])
    hflip = j == 1
    oH = emH(t, [[0, 'determined'], [ek(46), 'happy'], [ek(47), 'playful'], [ek(48), 'proud'], [ek(49), 'excited']], view='q', flip=hflip)
    if j in (0, 1):
        oH['aR'] = 1.1
        oH['aL'] = .1
    elif j == 2:
        oH['aR'] = 1.55
    oH['dy'] = (oH.get('dy') or 0) - jump
    backpack(600, 880, u, oH, col='#F28CA8', key='s12bp2')
    oH['draw'] = strapHook('q', '#C0637B')
    her(600, 880, u, oH)
    if j == 2 or j == 3:
        hx, hy = handXY(600, 880, u, oH, 'R')
        compass(hx + 10, hy - 40, 52, -math.pi / 2 + .3 * math.sin(t * 6), t, key='s12cmp', shine=1)
    # him (right): looks where she points
    mflip = not (j == 0)
    if j == 2:
        mflip = True
    oM = emM(t, [[0, 'happy'], [ek(46), 'surprised'], [ek(47), 'surprised'], [ek(48), 'starstruck'], [ek(49), 'excited']], view='q', flip=mflip)
    oM['emote'] = None if j < 2 else oM.get('emote')
    oM['dy'] = (oM.get('dy') or 0) - jump
    backpack(1420, 880, u, oM, col='#4A90D9', key='s12bp1')
    oM['draw'] = strapHook('q')
    him(1420, 880, u, oM)
    # turn whoosh marks on his head
    for k in (46, 47):
        h = hitK(t, k, .16)
        if h > .05:
            for i in range(3):
                line(1420 - 170 + i * 30, 560 - 20 * i, 1420 - 120 + i * 30, 540 - 20 * i, INK, h, 4)
    if t >= B[49] - .16:
        flagPop(1590, 640, 62, '出发！', clamp((t - (B[49] - .16)) / .16), key='s12flag')
        confetti(t, 1060, 400, (t - B[49]) / .9, seed=49, n=50, spread=700)
    camEnd()


# =====================================================================================
# S13 k50–k54 · 示例歌词占位: side-on walk along a country road, milestones 1 → 10 → 100 → ∞ km
def s13(t, lt, dur):
    cam(t, 960, 540, 1.0)
    gradient('#9FD3F5', '#FFF1D6', -200, 700)
    sunDisc(1600, 200, 60, key='s13sun')
    sp = 40.0
    push()
    translate(-(lt * 12) % 400, 0)
    hills(470, ['#CFE8C0', '#B6DCA0'], 0, key='s13hl')
    pop()
    # mid trees + poles scrolling
    for i in range(8):
        x = (i * 330 - lt * 90) % 2640 - 300
        tree(x, 760, 34 + 6 * (i % 2), key=f's13t{i}', col=['#7CC36B', '#8FCB7A'][i % 2])
    for i in range(5):
        x = (i * 520 + 200 - lt * 150) % 2600 - 300
        boilSeed(f's13p{i}')
        paint(rectPts(x - 7, 470, 14, 330), wash='#8E6A4A', ink=INK, sw=.7)
        paint(rectPts(x - 40, 490, 80, 12), wash='#8E6A4A', ink=INK, sw=.6)
    for i in range(5):
        x0 = (i * 520 + 200 - lt * 150) % 2600 - 300
        x1 = x0 + 520
        inkLine([[x0, 496], [(x0 + x1) / 2, 530], [x1, 496]], .5, INK, 'inkfine', .5)
    flatRect(-200, 790, W + 400, 500, '#9ED27A')
    flatRect(-200, 800, W + 400, 110, '#C9C2B8')
    line(-200, 800, W + 200, 800, INK, 1, 3)
    line(-200, 910, W + 200, 910, INK, 1, 3)
    for i in range(14):
        x = (i * 200 - lt * sp) % 2800 - 300
        flatRect(x, 851, 100, 8, '#FFFFFF', .9)
    for i in range(20):
        x = (i * 130 - lt * sp * 1.3) % 2600 - 300
        G.c.drawCircle(x, 950 + 20 * hash1(i), 6, _pa(['#FFFFFF', '#FFD36A', '#FF9FBA'][i % 3]))
    # milestones: each pops on its beat at the roadside ahead, the previous one folds down
    labs = ['1km', '10km', '100km', '∞km']
    ks = [50, 51, 52, 53]
    for i, k in enumerate(ks):
        kin = clamp((t - (B[k] - .12)) / .12) if i > 0 else 1.0
        kout = 1 - clamp((t - (B[ks[i + 1]] - .26)) / .12) if i + 1 < len(ks) else 1.0
        mileSign(1520, 812, 80, labs[i], min(kin, kout), key=f's13ms{i}')
    u1, u2 = 28, 30
    w1 = move('walk', t)
    oM = emM(t, [[0, 'happy'], [ek(52), 'excited', {'emote': None}], [ek(53), 'happy']], view='q')
    oM.update(walk=w1['walk'], aL=w1['aL'] + .2, aR=w1['aR'] + .2, dy=(oM.get('dy') or 0) * .3 + w1['dy'])
    backpack(1130, 830, u1, oM, col='#4A90D9', key='s13bp1')
    oM['draw'] = strapHook('q')
    him(1130, 830, u1, oM)
    w2 = move('walk', t + .35)
    oH = emH(t, [[0, 'happy'], [ek(51), 'happy', {'eyes': 'heart'}], [ek(53), 'laugh']], view='q')
    oH.update(walk=w2['walk'], aL=w2['aL'] + .2, aR=w2['aR'] + .2, dy=(oH.get('dy') or 0) * .3 + w2['dy'])
    backpack(700, 880, u2, oH, col='#F28CA8', key='s13bp2')
    oH['draw'] = strapHook('q', '#C0637B')
    her(700, 880, u2, oH)
    if t >= B[53] - .04:
        sparkles(t, 53, 8, 1380, 400, 1700, 600, r=16, col='#FFE36E')
    camEnd()


# =====================================================================================
# S14 k54–k58 · 示例歌词占位: a cork board under string lights — four polaroids, one per beat
def picIsland(cx, cy, iw, ih):
    gradRect(cx - iw / 2, cy - ih / 2, iw, ih, ['#FFB36B', '#FFE8D0'])
    flatRect(cx - iw / 2, cy + ih * .08, iw, ih, '#6FB7D9')
    G.c.drawCircle(cx + iw * .25, cy + ih * .02, 26, _pa('#FFF2B8'))
    paint(ellPts(cx, cy + ih * .36, iw * .45, ih * .14, 20), wash='#F2D9A0', ink=INK, sw=.5)
    palm(cx - iw * .32, cy + ih * .3, 12, key='pi1', lean=-.2)
    picCouple(cx, cy + ih * .36, 8)


def picCouple(cx, y, u, beret=False):
    him(cx - 5.4 * u, y, u, dict(view='front', eyes='happy', mouth='smile', blush=.6, aL=.3, aR=1.3, boilKey='pcm', noShadow=True))
    her(cx + 5.4 * u, y, u, dict(view='front', eyes='happy', mouth='smile', blush=.6, aL=1.3, aR=.3, boilKey='pch', noShadow=True,
                                 hat=['beret', 'flower'] if beret else 'flower'))


def picSky(cx, cy, iw, ih):
    gradRect(cx - iw / 2, cy - ih / 2, iw, ih, ['#8EC9F0', '#E8F6FF'])
    puff(cx - iw * .3, cy + ih * .3, 16, col='#FFFFFF', key='psk1')
    puff(cx + iw * .34, cy - ih * .2, 12, col='#FFFFFF', key='psk2')
    u = 6

    def people(bx, rim):
        y = rim + 2.0 * u
        him(bx - 5.3 * u, y, u, dict(view='front', eyes='happy', mouth='smile', noShadow=True, boilKey='psm', aR=1.3))
        her(bx + 5.3 * u, y, u, dict(view='front', eyes='happy', mouth='smile', noShadow=True, boilKey='psh', aL=1.3))
    bambooCopter(cx, cy - ih * .12, 9.5, 2.0, spin=1, key='psbc', people=people, basket='swing')


def picParis(cx, cy, iw, ih):
    gradRect(cx - iw / 2, cy - ih / 2, iw, ih, ['#C9B6E8', '#FFD9C8'])
    eiffel(cx + iw * .2, cy + ih * .3, ih * .85, lights=1, t=1.0, key='ppeif')
    flatRect(cx - iw / 2, cy + ih * .3, iw, ih, '#D9C2B0')
    picCouple(cx - iw * .1, cy + ih * .42, 8, beret=True)


def picShop(cx, cy, iw, ih):
    flatRect(cx - iw / 2, cy - ih / 2, iw, ih, '#F6E5C8')
    flatRect(cx - iw / 2, cy + ih * .3, iw, ih, '#D9CDB8')
    boilSeed('psd')
    paint(rectPts(cx + iw * .12, cy - ih * .3, iw * .3, ih * .6), wash='#9A6640', ink=INK, sw=.6)
    paint(rrPts(cx + iw * .15, cy - ih * .18, iw * .24, ih * .16, 6), wash='#FFE36E', ink=INK, sw=.4)
    text('去旅行啦', cx + iw * .27, cy - ih * .1, 16, '#D9573E', shadow=False)
    awning(cx - iw / 2, cx + iw / 2, cy - ih / 2, 34, key='psaw', cols=('#E07A4E', '#FFF5E2'))
    picCouple(cx - iw * .14, cy + ih * .42, 8)
    backpackMini = None


def s14(t, lt, dur):
    cam(t, 960, 520, lerp(1.0, 1.08, ease(lt / dur)))
    flatRect(-300, -300, W + 600, H + 600, '#F6E5C8')
    for i in range(-6, 32):
        flatRect(i * 80, -300, 40, H + 600, '#F1DAB8', .55)
    boilSeed('s14cork')
    paint(rectPts(240, 150, 1440, 700), wash='#C99A62', fill='#B5824C', fillOp=80, ink=INK, sw=1.2)
    paint(rectPts(222, 132, 1476, 736), ink='#6B4A33', sw=5)
    for i in range(60):
        G.c.drawCircle(260 + hash1(i * 1.1) * 1400, 170 + hash1(i * 2.3) * 660, 3, _pa('#8E6A3E', .5))
    on = .35 + .65 * landK(t, 57, .1)
    stringLights([[160, 100], [560, 190], [960, 120], [1360, 190], [1760, 100]], t, on=on, key='s14sl')
    pics = [(54, 450, 520, -.07, picIsland, '海岛'), (55, 790, 470, .05, picSky, '天上'), (56, 1130, 520, -.04, picParis, '巴黎'),
            (57, 1470, 470, .06, picShop, '出发那天')]
    for k, x, y, rot, sc, lab in pics:
        polaroidPic(x, y, 320, rot, pk(t, k, .18), sc, key=f's14p{k}', label=lab, pinCol=HOT)
    # a red thread map line linking them
    if t >= B[55]:
        n = lastBeat(t, [54, 55, 56, 57])
        P = [[450, 318], [790, 268], [1130, 318], [1470, 268]][:n + 1]
        if len(P) > 1:
            inkLine(P, 1.0, '#E8476E', 'ink', .3)
    if t >= B[57] - .04:
        floatHearts(t - B[57], 57, 8, 400, 200, 1500, 700, s=18)
    camEnd()


# =====================================================================================
# S15 k58–k62 · 示例歌词占位文字示例: dusk plaza with a giant compass rose; they land on it; 东 lights
def s15(t, lt, dur):
    cam(t, 960, 560, lerp(1.04, 1.1, ease(lt / dur)))
    gradient('#5B4A9C', '#FFB38A', -200, 640)
    sunDisc(960, 600, 90, col='#FFD27A', glowCol='#FF9A6B', key='s15sun')
    boilSeed('s15sky')
    pts = [[-200, 640]]
    for i in range(24):
        x = -200 + i * 100
        pts += [[x, 600 - 60 * hash1(i * 1.7)], [x + 50, 600 - 90 * hash1(i * 2.9)]]
    pts.append([2200, 640])
    paint(pts, wash='#4A3A7A', fill='#3A2C66', fillOp=60, ink=INK, sw=.8)
    flatRect(-200, 640, W + 400, 800, '#CDB8A0')
    for r in range(8):
        line(-200, 660 + r * r * 8, W + 200, 660 + r * r * 8, '#B8A088', .6, 2)
    lamp(260, 700, 30, on=1, key='s15l1')
    lamp(1660, 700, 30, on=1, key='s15l2')
    # needle: spins from k59, lands on 东 (0) at k61
    if t < B[59] - .04:
        nd = -math.pi / 2
    elif t < B[61] - .2:
        nd = -math.pi / 2 + (t - (B[59] - .04)) * 9
    else:
        n0 = -math.pi / 2 + (B[61] - .2 - (B[59] - .04)) * 9
        n1 = math.ceil(n0 / TAU) * TAU
        nd = lerp(n0, n1, backOut(clamp((t - (B[61] - .2)) / .2)))
    litE = landK(t, 61, .1)
    plazaRose(960, 880, 820, 190, t, needle=nd, litE=litE, key='s15pr')
    if t >= B[59] - .04 and t < B[61]:
        boilSeed('s15imp')
        for i in range(9):
            a = math.pi + (i + .5) / 9 * math.pi
            inkLine([[960 + math.cos(a) * 860, 880 + math.sin(a) * 210], [960 + math.cos(a) * 960, 880 + math.sin(a) * 250]], 1.2, '#FFFFFF', 'ink', 0)
    u = 30
    land = hitK(t, 58, .12)
    turnM = j = lastBeat(t, [58, 59, 60, 61])
    oM = emM(t, [[0, 'excited', {'emote': None}], [ek(60), 'happy', {'eyes': 'heart', 'blush': .9}], [ek(61), 'happy']], view='q')
    if t < B[60] - .04:
        oM['lookX'] = -.2
    oM['sq'] = (oM.get('sq') or 0) + .2 * land
    backpack(750, 800, u, oM, col='#4A90D9', key='s15bp1')
    oM['draw'] = strapHook('q')
    him(750, 800, u, oM)
    oH = emH(t, [[0, 'excited', {'emote': None}], [ek(60), 'shy'], [ek(61), 'happy']], view='q', flip=True)
    oH['sq'] = (oH.get('sq') or 0) + .2 * land
    backpack(1170, 800, u, oH, col='#F28CA8', key='s15bp2')
    oH['draw'] = strapHook('q', '#C0637B')
    her(1170, 800, u, oH)
    da = t - (B[58] - .04)
    if 0 < da < .6:
        for i in range(8):
            d = -1 if i % 2 else 1
            puff(960 + d * (260 + 140 * easeOut(da / .6)) + (i // 2) * 24 * d, 810, 12 * (1 - da / .6), col='#FFF1DC', key=f's15d{i}', a=1 - da / .6)
    if t >= B[60] - .04:
        a = t - (B[60] - .04)
        heart(960, 430 - 40 * easeOut(clamp(a / .4)), 50 * backOut(clamp(a / .16)), HOT, key='s15h')
    camEnd()


# =====================================================================================
# S16 k62–end · 示 例歌词占位文: back to the counter top and the same chat — he finally replies; her heart; a photo of the two
def picPlaza(sx, sy, w, h):
    gradRect(sx, sy, w, h, ['#5B4A9C', '#FFB38A'])
    G.c.drawCircle(sx + w / 2, sy + h * .62, 40, _pa('#FFD27A'))
    flatRect(sx, sy + h * .64, w, h, '#CDB8A0')
    paint(ellPts(sx + w / 2, sy + h * .84, w * .46, h * .1, 30), wash='#E9D8C0', ink=INK, sw=.5)
    u = 11
    him(sx + w / 2 - 5.6 * u, sy + h * .9, u, dict(view='front', eyes='happy', mouth='smile', blush=.7, aL=.3, aR=1.4, boilKey='ppm'))
    her(sx + w / 2 + 5.6 * u, sy + h * .9, u, dict(view='front', eyes='happy', mouth='smile', blush=.7, aL=1.4, aR=.3, boilKey='pph'))
    heart(sx + w / 2, sy + h * .3, 22, HOT, key='pph2', sw=.5)


def s16(t, lt, dur):
    CLOCK[0] = '18:42'
    cam(t, 960, 540, lerp(1.0, 1.06, ease(lt / dur)))

    def extra():
        # opened parcel + the compass + two tickets where the title tag used to be
        boilSeed('s16box')
        paint(rectPts(150, 260, 360, 300), wash='#D9B07A', fill='#B8895A', fillOp=60, ink=INK, sw=1)
        paint(rectPts(176, 286, 308, 248), wash='#B8895A', ink=None)
        flatRect(315, 260, 30, 300, '#E8476E')
        compass(330, 410, 120, .4 * math.sin(t * 2.2), t, key='s16cmp', shine=1)
        for i, (x, y, r) in enumerate(((260, 700, -.12), (430, 730, .08))):
            push()
            translate(x, y)
            rotate(r)
            boilSeed(f's16tk{i}')
            paint(rrPts(-120, -48, 240, 96, 10), wash='#FFF5E2', ink=INK, sw=.8)
            line(60, -40, 60, 40, '#C9C1D6', 1, 2)
            text('东 ⇄ 西', -24, 0, 34, '#D9573E', shadow=False, face=WENKAI)
            pop()
    counterTop(t, extra=extra)
    jx, jy = shakeAmt(t, B[62] - .02, 10, 14)

    def page(sx, sy, sw_, sh):
        chatPage(t, sx, sy, sw_, sh, HERNAME)
        rows = [('L', m, 1.0, 118) for m, _ in MSGS]
        rows.append(('R', '东或西 都陪你', 62, 118))

        def stick(y, k):
            wx.avatarBox(sx + 64, y + 40, 38, 'her', 'love', key='s16av1')
            heartSticker(sx + 230, y + 100, k, key='s16hs')
        rows.append(('L', stick, 63, 220))

        def photo(y, k):
            if k > .02:
                wx.avatarBox(sx + 64, y + 40, 38, 'her', 'happy', key='s16av2')
            photoMsg(sx + 120, y, 330, 250, k, picPlaza, key='s16pm')
        rows.append(('L', photo, 64, 270))
        # scroll up as new rows land
        heights = [r[3] for r in rows]
        y_top = sy + 205
        bottom = sy + sh - 125
        off, prev = 0.0, max(0, y_top + sum(heights[:4]) - bottom)
        off = prev
        for i, k in enumerate([62, 63, 64]):
            need = max(0, y_top + sum(heights[:5 + i]) - bottom)
            off += (need - prev) * easeOut(clamp((t - (B[k] - .1)) / .18))
            prev = need
        G.c.save()
        G.c.clipRect(skia.Rect.MakeXYWH(sx, sy + 172, sw_, sh - 172 - 112))
        chatRows(t, sx, sw_, y_top - off, rows)
        G.c.restore()

    if t >= B[64] - .04:
        a = t - (B[64] - .04)
        confetti(t, PHX, PHY - 60, a / .9, seed=64, n=80, spread=800)
        hearts(t, PHX, PHY - 40, 10, 460, 26, a / .9, seed=6)
    phoneTop(t, page, PHX, PHY, PHS, (jx, jy))
    if t >= B[63] - .04:
        floatHearts(t - B[63], 63, 6, PHX - 300, 300, PHX + 300, 700, s=16)
    camEnd()


_FN = dict(S01=s01, S02=s02, S03=s03, S04=s04, S05=s05, S06=s06, S07=s07, S08=s08, S09=s09, S10=s10, S11=s11, S12=s12, S13=s13,
           S14=s14, S15=s15, S16=s16)
SHOTS = []
for s in SB['shots']:
    SHOTS.append((s['start'], _FN[s['id']], s['tr'], s['id']))
