# story2.py: 《99》 shots S14–S25. Data: storyboard.py.
import math
from nn import *
import nn
import eng

U = 32
GND = 880


# =====================================================================================
# S14 26.59–28.66 · 示例 歌词占位文字示 例歌词占位 文字示 例歌词占 位 文字示例歌词占: LOVE → her heart bubble → LOYALTY + lock → one locked heart 「咔」
def s14(t, lt, dur):
    sunburst(960, 560, '#FBD3DE', '#F59AB0', 20, -t * .1)
    cam(t, 960, 560, 1.02)
    hx, sx_ = 700, 1250
    u = 38
    oh = emM(t, [[0, 'cool', {'eyes': 'happy', 'emote': None}], [ek(54), 'determined'], [ek(55), 'happy', {'eyes': 'heart', 'blush': .8}]], view='q')
    oe = emH(t, [[0, 'happy', {'eyes': 'closed', 'blush': .6}], [ek(53), 'happy', {'blush': .9}], [ek(55), 'love']], view='q', flip=True)
    himN(hx, GND, u, oh)
    herN(sx_, GND, u, oe)
    merge = clamp((t - (B[55] - .16)) / .16)
    cxm, cym = 970, 300
    if t >= B[52] - .04 and merge < 1:
        bx, by = lerp(520, cxm, easeIn(merge)), lerp(230, cym, easeIn(merge))
        bubble(bx, by, 'LOVE', 70, (hx, GND - 9 * u) if merge == 0 else None, popIn(t, 52) * (1 - merge), key='s14b1', col='#FFFFFF', tcol=HOT)
    if t >= B[53] - .04 and merge < 1:
        bx, by = lerp(1420, cxm, easeIn(merge)), lerp(250, cym, easeIn(merge))
        k = popIn(t, 53) * (1 - merge)
        bubble(bx, by, '      ', 60, (sx_, GND - 9 * u) if merge == 0 else None, k, key='s14b2', col='#FFF0F4')
        if k > .2:
            heart(bx, by, 40 * k, HOT, key='s14bh')
    if t >= B[54] - .04 and merge < 1:
        bx, by = lerp(330, cxm, easeIn(merge)), lerp(470, cym, easeIn(merge))
        k = popIn(t, 54) * (1 - merge)
        tw = textW('LOYALTY', 56)
        bubble(bx, by, ' ' * 14, 56, (hx - 2.5 * u, GND - 8.6 * u) if merge == 0 else None, k, key='s14b3', col='#FFFBE8', minw=tw + 150)
        if k > .2:
            pk_ = backOut(k)
            text('LOYALTY', bx - 30 * pk_, by, 56 * pk_, '#B8724A', shadow=False)
            lockIcon(bx + (tw / 2 + 22) * pk_, by + 8 * pk_, 34 * pk_, 1.0, key='s14lk')
    if merge > 0:
        wx.lockHeart(cxm, cym, 110 * backOut(merge), shut=clamp((t - (B[55] - .02)) / .1), key='s14lh')
    if t >= B[55] - .04:
        stamp('咔', cxm + 170, cym - 120, 80, '#FFE36E', t - B[55], rot=.12)
        floatHearts(t, 55, 6, 600, 300, 1300, 600, 18)
    camEnd()


# =====================================================================================
# S15 28.66–30.73 · 示例歌词占位文字示例歌词: the plan board ticks off 锻炼 / 看书 / 学做饭, then he brings her soup
def s15(t, lt, dur):
    cam(t, 960, 540, 1.03)
    nm.hisRoomBack(t, hat=True, mag=False)
    chalkBoard(80, 200, 420, 450, key='s15cb')
    text('变好计划', 290, 262, 52, '#FFF3C8', face=WENKAI, shadow=False)
    items = [('锻炼', 56), ('看书', 57), ('学做饭', 58)]
    for i, (s_, k) in enumerate(items):
        y = 360 + i * 100
        paint(rectPts(130, y - 26, 52, 52), wash=None, ink='#F3F1E8', sw=1.0)
        text(s_, 215, y, 48, '#F3F1E8', face=WENKAI, align='left', shadow=False)
        if t >= B[k] - .1:
            checkMark(156, y - 4, 60, clamp((t - (B[k] - .1)) / .1), '#7CF29A')
    hx, sx_ = 1020, 1600
    u = 32
    stage = lastBeat(t, [56, 57, 58, 59], .08)
    keys = [[0, 'determined'], [ek(57), 'thinking', {'emote': None}], [ek(58), 'happy'], [ek(59), 'hopeful']]
    oh = emM(t, keys, view='q', lookX=.3)
    oe = emH(t, [[0, 'happy'], [ek(59), 'love']], view='q', flip=True)
    if stage == 0:
        oh['aR'] = 1.5 + .2 * math.sin(t * 14)
    elif stage == 1:
        oh['aR'] = .7
    elif stage == 2:
        oh['aR'] = 1.0 + .3 * math.sin(t * 16)
    elif stage >= 3:
        oh['aR'] = .75
    himN(hx, GND, u, oh)
    herN(sx_, GND, u, oe)
    hd = handXY(hx, GND, u, oh, 'R')
    if stage == 0:
        dumbbell(hd[0] + 40, hd[1] - 70, 70, -1.15, key='s15db')
    elif stage == 1:
        bookOpen(hd[0] + 90, hd[1] + 10, 80, -.1, key='s15bk')
    elif stage == 2:
        spatula(hd[0], hd[1], 90, .5, key='s15sp')
    elif stage >= 3:
        soupBowl(hd[0] + 50, hd[1] - 10, 56, t, key='s15sb')
        stamp('照顾你', hd[0] + 80, hd[1] - 180, 60, HOT, t - B[59], rot=-.1, stroke='#FFFFFF')
    if stage >= 0:
        dot(hd[0], hd[1], .5 * u, ME['col'])
        ring(hd[0], hd[1], .5 * u, INK, 2.5)
    for k in (56, 57, 58):
        if B[k] - .04 <= t < B[k + 1] - .06:
            stamp('✓' if False else '+1', hx - 5 * u, GND - 11 * u, 60, '#7CF29A', t - B[k], rot=-.1, life=.5)
    if t >= B[59] - .04:
        floatHearts(t, 59, 5, sx_ - 150, GND - 13 * u, sx_ + 120, GND - 9 * u, 16)
    camEnd()


# =====================================================================================
# S16 30.73–32.79 · 示例歌词占位文字示例歌词: 压力 slams down, 情绪 stacks on top, he is squashed 「呼…」, the dark closes in
def s16(t, lt, dur):
    gradRect(-400, -400, W + 800, 1300, ['#5A6280', '#3E4560'])
    cam(t, 960, 560, lerp(1.03, 1.1, ease(lt / dur)))
    flatRect(-400, 860, W + 800, 500, '#4A4E66')
    inkLine([[-400, 860], [W + 400, 860]], 1.0, INK, 'ink', 0)
    hx = 960
    u = 34
    d1 = clamp((t - (B[60] - .16)) / .16)
    d2 = clamp((t - (B[61] - .16)) / .16)
    sq = 0.0
    if t >= B[60]:
        sq = .18 + .08 * math.exp(-(t - B[60]) * 12)
    if t >= B[61]:
        sq = .3 + .08 * math.exp(-(t - B[61]) * 12)
    if t >= B[62] - .04:
        sq = .38 + .04 * math.sin(t * 9)
    oh = emM(t, [[0, 'neutral'], [ek(60), 'scared', {'emote': None, 'tint': 'blue', 'tintK': .3}], [ek(62), 'ko', {'emote': None}]], view='front')
    oh.update(sq=sq, dy=0, rot=0, dx=0, aL=.9, aR=.9)
    himN(hx, GND, u, oh)
    top = GND - 8 * u * (1 - sq)
    W1, H1 = 420, 200
    y1 = lerp(-300, top, easeIn(d1))
    stoneBlock(hx, y1, W1, H1, '压力', rot=.03, key='s16a')
    if t >= B[61] - .16:
        y2 = lerp(-300, y1 - H1, easeIn(d2))
        stoneBlock(hx + 20, y2, 340, 180, '情绪', rot=-.04, key='s16b', col='#7A7E98')
    if t >= B[60] - .02:
        if t < B[60] + .2:
            boilSeed('s16imp')
            for i in range(9):
                a_ = math.pi + (i + .5) / 9 * math.pi
                inkLine([[hx + math.cos(a_) * 240, top - 60 + math.sin(a_) * 150], [hx + math.cos(a_) * 320, top - 60 + math.sin(a_) * 210]], 1.0, '#FFFFFF', 'ink', 0)
        stamp('咚', hx - 330, top - 120, 80, '#FFFFFF', t - B[60], rot=-.12, life=.4)
    if t >= B[61] - .02:
        stamp('咚！', hx + 330, top - 300, 80, '#FFFFFF', t - B[61], rot=.12, life=.45)
    if t >= B[62] - .04:
        bubble(hx + 330, GND - 4.5 * u, '呼…', 46, (hx + 5 * u, GND - 3.5 * u), popIn(t, 62), key='s16b1', col='#E8EEFA')
        for i in range(3):
            paint(heartPts(hx - 5.6 * u - i * 26, GND - 4 * u + 14 * i, 12), wash='#BFE3F5', ink=INK, sw=.4) if False else None
    lx, ly = toScreen(hx, GND - 4 * u)
    camEnd()
    dk = es(t, kt(63) - .12, kt(63) - .02)
    if dk > 0:
        nm.darkness(.88 * dk, [(lx, ly, lerp(1400, 520, dk), 1.0)])


# =====================================================================================
# S17 32.79–34.86 · 示例歌词占位文字示例歌词占: he shivers under the lamp in the snow → she wraps a red scarf → hot cocoa → warm light
def s17(t, lt, dur):
    warm = es(t, kt(67) - .1, kt(67) + .25)
    cam(t, 960, 560, 1.03)
    snowNight(t, warm, key='s17sn')
    props.lamp(560, 860, 50, on=1.0, key='s17lp')
    glow(560, 400, 300, '#FFE2A0', .5)
    # snow; from k67 the flakes turn into little stars and drift up
    if warm < 1:
        G.c.saveLayerAlpha(None, int(255 * (1 - warm)))
        snowfall(t, 17, 60, -100, -100, W + 100, 860, rate=1.0, a=.9)
        G.c.restore()
    if t >= B[67] - .06:
        a67 = t - (B[67] - .06)
        for i in range(26):
            x = -60 + hash1(i * 3.7) * (W + 120)
            y = 80 + hash1(i * 1.9) * 700 - 60 * a67
            paint(starPts(x, y, 9 + 6 * hash1(i), .42, 5), wash='#FFE9A0', washOp=int(255 * clamp(a67 / .12)), ink=None)
    hx = 860
    u = 32
    scarfK = clamp((t - (B[65] - .1)) / .1)
    oh = emM(t, [[0, 'scared', {'emote': None, 'tint': 'blue', 'tintK': .6}], [ek(65), 'surprised', {'emote': None, 'tint': 'blue', 'tintK': .3}],
                 [ek(66), 'happy', {'blush': .7}], [ek(67), 'happy', {'eyes': 'heart', 'blush': .9}]], view='q')
    if t < B[65]:
        oh.update(dx=.12 * math.sin(t * 70), aL=-.55, aR=-.55, sq=.12, dy=0, rot=0)
    if scarfK > 0:
        oh['draw'] = scarfDraw('q', '#D9534F', backOut(scarfK))
    himN(hx, GND, u, oh)
    run = clamp((t - (B[65] - .4)) / .36)
    sx_ = lerp(2150, 1300, ease(run))
    oe = emH(t, [[0, 'nervous'], [ek(65), 'happy'], [ek(66), 'happy', {'eyes': 'closed'}], [ek(67), 'love']], view='q', flip=True)
    if 0 < run < 1:
        oe.update(move('run', t))
        oe['rot'] = 0
    if t >= B[66] - .2:
        oe['aR'] = lerp(.2, -.1, es(t, kt(66) - .2, kt(66) - .02))
    herN(sx_, GND, u, oe)
    if t < B[65]:
        for i in range(4):
            inkLine([[hx - 6 * u - i * 6, GND - 6 * u + i * 30], [hx - 6.8 * u - i * 6, GND - 6 * u + i * 30]], 1.0, '#BFE3F5', 'ink', 0)
        stamp('好冷', hx + 6.5 * u, GND - 10.5 * u, 60, '#BFE3F5', t - B[64], rot=.1)
    if t >= B[65] - .04:
        stamp('围上', 1080, 380, 56, '#FFFFFF', t - B[65], rot=.1, life=.45)
    if t >= B[66] - .06:
        hd = handXY(sx_, GND, u, oe, 'R')
        k66 = clamp((t - (B[66] - .06)) / .12)
        cocoaCup(hd[0] - 34, hd[1] + 40, 1.0 * backOut(k66), t, key='s17cc')
        dot(hd[0], hd[1], .5 * u, HER['col'])
        ring(hd[0], hd[1], .5 * u, INK, 2.5)
    lx, ly = toScreen(1050, GND - 5 * u)
    camEnd()
    # k67: a ring of warm light sweeps out from between them
    if t >= B[67] - .06:
        a67 = t - (B[67] - .06)
        r = 120 + 1400 * easeOut(clamp(a67 / .6))
        G.c.drawCircle(lx, ly, r, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=26, Color=skcol('#FFD27A', .55 * (1 - clamp(a67 / .7)))))
        glow(lx, ly, 260 + 300 * clamp(a67 / .4), '#FFE2A0', .55)
        rubberStamp('熬过去了', 960, 210, 84, t - B[67], col=RED, rot=-.1)
        floatHearts(t, 67, 6, 820, 300, 1260, 560, 18)


# =====================================================================================
# S18 34.86–36.93 · 示例歌词 占位文字: honey jar + sweet smile → a honey-drop heart → lemon, sour squint → honey-lemon tea
def s18(t, lt, dur):
    sunburst(960, 600, '#FFF0B0', '#FFE07A', 20, t * .12)
    cam(t, 960, 560, 1.02)
    sx_, hx = 640, 1300
    u = 36
    oe = emH(t, [[0, 'happy', {'eyes': 'closed', 'blush': .8}], [ek(69), 'love'], [ek(71), 'happy']], view='q')
    oh = emM(t, [[0, 'happy'], [ek(70), 'neutral', {'eyes': 'squeeze', 'mouth': 'wobble', 'tint': 'green', 'tintK': .3}], [ek(71), 'happy', {'eyes': 'heart', 'blush': .8}]],
             view='q', flip=True)
    if B[70] - .1 < t < B[71] - .1:
        oh['sq'] = (oh.get('sq') or 0) + .08
    herN(sx_, GND, u, oe)
    himN(hx, GND, u, oh)
    into = clamp((t - (B[71] - .2)) / .18)          # jar + lemon fly into the cup, arriving on k71
    CUP = (970, 640)
    if t >= B[68] - .04 and into < 1:
        k68 = popIn(t, 68)
        jx, jy = lerp(300, CUP[0], easeIn(into)), lerp(GND, CUP[1], easeIn(into))
        push()
        translate(jx, jy)
        scale(k68 * lerp(1, .3, into))
        honeyJar(0, 0, 96, key='s18hj')
        pop()
    if t >= B[68] - .04:
        stamp('甜', 300, GND - 380, 76, '#FFFFFF', t - B[68], rot=-.1, life=.45)
    if t >= B[69] - .22 and into <= 0:
        # a honey drip runs from the jar spoon up into a golden heart
        f = clamp((t - (B[69] - .22)) / .2)
        boilSeed('s18drip')
        pts = [[300 + 40, GND - 210], [300 + 60, GND - 260 - 60 * f], [300 + 40, GND - 300 - 120 * f]]
        inkLine(pts, 3.2, '#F2A82A', 'ink', .6)
        heart(300 + 40, GND - 330 - 150 * f, lerp(10, 58, f), '#F7C24A', key='s18dh')
        if f >= 1:
            text('蜜', 300 + 40, GND - 482, 30, '#FFFFFF', face=WENKAI, stroke=INK, strokeW=5, shadow=False)
    if t >= B[70] - .04 and into < 1:
        k70 = popIn(t, 70)
        lx_, ly_ = lerp(1700, CUP[0], easeIn(into)), lerp(500, CUP[1] - 60, easeIn(into))
        lemonProp(lx_, ly_, 100 * k70 * lerp(1, .3, into), key='s18lm', rot=-.2)
    if t >= B[70] - .04:
        stamp('酸！', 1700, 340, 70, '#B8E04A', t - B[70], rot=.12, life=.45)
    if t >= B[71] - .04:
        k71 = popIn(t, 71)
        push()
        translate(CUP[0], CUP[1] + 220)
        scale(k71)
        teaGlass(0, 0, 96, t, key='s18tg')
        pop()
        floatHearts(t, 71, 6, 820, 360, 1120, 600, 16)
        stamp('刚刚好', 970, 250, 74, HOT, t - B[71], rot=-.08, stroke='#FFFFFF')
    camEnd()


# =====================================================================================
# S19 36.93–38.99 · 示例歌词 占位文字: spotlight on her at the mic → notes fly to him → swap: he sings, she listens → glow stick
def stool(x, seatTop, key='stl', col='#C98B5A'):
    boilSeed(key)
    for sx in (-1, 1):
        paint(rectPts(x + sx * 70 - 8, seatTop + 10, 16, GND - seatTop - 10), wash='#8A5A3C', ink=INK, sw=.7)
    paint(rrPts(x - 110, seatTop - 6, 220, 30, 10), wash=col, ink=INK, sw=.9)


def s19(t, lt, dur):
    cam(t, 960, 540, 1.0)
    props.curtainStage(t, 1.0)
    swap = t >= B[74] - .04
    MX, CX = 600, 1520
    u = 34
    # the stage platform ends at x≈1140; to the right is the audience floor, one step lower, darker
    boilSeed('s19aud')
    flatRect(1140, 760, W + 400, 600, '#5A3A4A')
    for i in range(6):
        inkLine([[1140, 800 + i * 40], [W + 300, 800 + i * 40]], .5, '#4A2E3C', 'inkfine', 0)
    paint([[1100, 790], [1180, 790], [1180, 1300], [1100, 1300]], wash='#8A5434', fill='#6A3E26', fillOp=60, ink=INK, sw=1.0)
    paint(rectPts(-100, 790, 1240, 26), wash='#C98B5A', ink=INK, sw=.8)
    for i in range(3):                      # two empty audience chairs behind for context
        boilSeed(f's19ch{i}')
        paint(rrPts(1300 + i * 230, 700, 140, 26, 8), wash='#7A4A5A', ink=INK, sw=.6)
    st = 780
    stool(CX, st, key='s19st')
    beamK = clamp((t - (B[72] - .08)) / .08)
    ch.lightBeam(MX, -100, 880, 120, 480, .35 * beamK, '#FFF6C8')
    hb.micStand(MX + 230, 880, 330, key='s19mic')
    singer, listener = (himN, herN) if swap else (herN, himN)
    if swap:
        os_ = emM(t, [[0, 'happy', {'mouth': 'open', 'eyes': 'closed'}]], view='q')
        ol = emH(t, [[0, 'love'], [ek(75), 'excited', {'emote': None}]], view='q', flip=True)
    else:
        os_ = emH(t, [[0, 'happy', {'mouth': 'open', 'eyes': 'closed'}]], view='q')
        ol = emM(t, [[0, 'happy', {'eyes': 'heart', 'blush': .7}]], view='q', flip=True)
    os_['aR'] = .9
    os_.update(dy=hopOn(t, 74, 1.2) if swap else 0)
    singer(MX, 880, u, os_)
    if t >= B[75] - .2 and swap:
        ol['aR'] = lerp(.3, 1.6, es(t, kt(75) - .2, kt(75) - .02)) + .2 * math.sin(t * 16) * (1 if t > B[75] else 0)
    seat(listener, CX, st, u, ol)
    if swap and t >= B[75] - .2:
        hd = handXY(CX, st + 2 * u, u, ol, 'R')
        glowStick(hd[0], hd[1] + 10, 80, -.4 + .3 * math.sin(t * 16) * (1 if t > B[75] else 0), key='s19gs')
        dot(hd[0], hd[1], .5 * u, HER['col'])
        ring(hd[0], hd[1], .5 * u, INK, 2.5)
    # notes fly from the singer to the listener, the first ones arriving on k73 (and on k75 after the swap)
    for k in (73, 75):
        t0 = B[k] - .5
        if t >= t0:
            noteStream(t, t0, MX + 170, 880 - 8 * u, CX - 40, st - 5 * u, 5, s=40, arc=-200, dur=.46, key=f's19n{k}')
        if t >= B[k] - .04:
            heart(CX - 3 * u, st - 7.8 * u, 34 * popIn(t, k), HOT, key=f's19h{k}')
    if t >= B[72] - .04 and not swap:
        stamp('开唱', MX - 240, 250, 64, '#FFE36E', t - B[72], rot=-.1, life=.6)
    if swap:
        stamp('换！', 1000, 220, 80, '#FFFFFF', t - B[74], rot=.1, life=.45)
    if t >= B[75] - .04:
        stamp('安可', CX, 300, 74, '#7CF2E8', t - B[75], rot=-.1)
    camEnd()


# =====================================================================================
# S20 38.99–41.06 · 示例歌词 占位文字: a big flower opens by her → petals float → the sky turns to stars → the stars join into a heart
def s20(t, lt, dur):
    nightK = es(t, kt(78) - .14, kt(78) - .02)
    cam(t, 860, 520, 1.02)
    sets2.nightHill(t, nightK, key='s20nh', moonK=nightK, tree=True)
    u = 28
    sx_, hx = 900, 1210
    sy, hy = sets2.hillY2(sx_), sets2.hillY2(hx)
    oe = emH(t, [[0, 'happy'], [ek(76), 'surprised', {'emote': None}], [ek(77), 'happy', {'eyes': 'closed'}], [ek(78), 'starstruck']], view='q')
    oh = emM(t, [[0, 'happy', {'eyes': 'heart', 'blush': .7}], [ek(78), 'starstruck']], view='q', flip=True)
    if t >= B[79] - .2:
        oe['aR'] = lerp(.3, 1.6, es(t, kt(79) - .2, kt(79) - .02))
    # the stem + bloom (drawn behind her)
    fx, fy = 680, sets2.hillY2(680)
    if t >= B[76] - .1:
        gk = clamp((t - (B[76] - .1)) / .14)
        boilSeed('s20stem')
        inkLine([[fx, fy], [fx + 10, fy - 140 * gk], [fx - 10, fy - 280 * gk]], 2.2, '#4E9A5A', 'ink', .5)
        paint(ellPts(fx + 30, fy - 120 * gk, 40 * gk, 16 * gk, 12, 0, -.5), wash='#7CC36B', ink=INK, sw=.6)
        bigBloom(fx - 10, fy - 290 * gk, 110, gk, key='s20bl', t=t)
    herN(sx_, sy, u, oe)
    himN(hx, hy, u, oh)
    if t >= B[76] - .04:
        stamp('啵', fx - 170, fy - 380, 64, '#FFFFFF', t - B[76], rot=.12, life=.7)
    if t >= B[77] - .16:
        a = t - (B[77] - .16)
        for i in range(10):
            ang = -2.6 + i * .32
            d = 90 + 520 * easeOut(clamp(a / .5)) * (.6 + .5 * hash1(i))
            px = fx + math.cos(ang) * d
            py = fy - 290 + math.sin(ang) * d * .7 + 30 * math.sin(t * 5 + i)
            petal(px, py, 22, t * 3 + i, '#F59AB0', 1 - seg(a, 1.6, 2.2), key=f's20pt{i}')
    if t >= B[78] - .04:
        stamp('星空', 1360, 520, 70, '#FFF3A8', t - B[78], rot=-.08, life=.8)
    if t >= B[79] - .2:
        hk = clamp((t - (B[79] - .2)) / .2)
        pts = heartPts(1150, 230, 180, 14)
        n = len(pts)
        m = max(2, int(n * hk) + 1)
        sel = pts[:m]
        inkLine(sel + ([pts[0]] if hk >= 1 else []), 1.0, '#FFF3A8', 'inkfine', 0)
        for (px, py) in pts:
            paint(starPts(px, py, 13, .42, 5), wash='#FFF3A8', ink=None)
        if hk >= 1:
            glow(1150, 230, 260, '#FFE2F0', .5)
    camEnd()


# =====================================================================================
# S21 41.06–43.12 · 示例歌词占位文字示例歌词: a row of identical grey figures (he is grey too) → she lands beside him → colour spreads → 「不怕！」
ROW21 = [160, 460, 760, 1080, 1400, 1720]
HIM_I, HER_I = 2, 3
CROWD_COLS = ['#9FD3F0', '#F7D36E', '#B8E0A0', '#F59AB0', '#C3A6FF', '#FFC27A']


def s21stage(t, colK):
    gradRect(-400, -400, W + 800, 1300, ['#E8F2FA', '#FFF2E6'])
    for i in range(14):
        puff(-100 + i * 160, 160 + 40 * math.sin(i), 18, ['#FFD9E2', '#D8ECFF', '#FFF2B0'][i % 3], key=f's21p{i}')
    flatRect(-400, 860, W + 800, 500, '#E9C99A')
    inkLine([[-400, 860], [W + 400, 860]], 1.0, INK, 'ink', 0)
    for i in range(12):
        props.bush(-60 + i * 180, 870, 46, key=f's21bu{i}', col=['#86C96E', '#9ED38A'][i % 2])
    happy = colK > .3
    for i, x in enumerate(ROW21):
        if i in (HIM_I, HER_I):
            continue
        c = CROWD_COLS[i]
        o = dict(col=c, dk=mixCol(c, INK, .3), lt=mixCol(c, '#FFFFFF', .4), view='front', eyes='happy' if happy else 'normal',
                 mouth='smile' if happy else None, boilKey=f's21g{i}', aL=(1.0 + .3 * math.sin(t * 12 + i)) if happy else .1,
                 aR=1.0 if happy else .1, dy=hopOn(t, 83, 1.0) if happy else 0)
        clawd(x, GND, 26, o)


def s21(t, lt, dur):
    colK = es(t, kt(82) - .0001, kt(82) + .35)
    cam(t, 960, 560, 1.02)
    s21stage(t, colK)
    cxs, cys = toScreen(920, 700)
    z = eng.CAM[2]
    camEnd()
    r = (lerp(300, 1600, colK) if t >= B[82] else 0) * z
    G.c.save()
    if t >= B[82]:
        p = skia.Path()
        p.addCircle(cxs, cys, r)
        G.c.clipPath(p, skia.ClipOp.kDifference, True)
    hl.desat(1.0)
    G.c.restore()
    if t >= B[82] and colK < 1:
        for w_, col_ in ((34, '#FF8FB0'), (18, '#FFE36E')):
            G.c.drawCircle(cxs, cys, r, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w_, Color=skcol(col_, .85 * (1 - colK * .7))))
    # the two, always in front
    cam(t, 960, 560, 1.02)
    u = 26
    grey = 0.0 if t >= B[82] else 1.0
    hcol = dict(col=mixCol(ME['col'], '#B8B6BE', grey), dk=mixCol(ME['dk'], '#8A8794', grey), lt=mixCol(ME['lt'], '#D8D6DC', grey))
    oh = emotions(t, [[0, 'nervous', {'tint': None}], [ek(81), 'surprised', {'emote': None}], [ek(82), 'happy'], [ek(83), 'proud']], hcol)
    oh.update(hcol)
    oh.update(view='q', tint=None, boilKey='him')
    if t >= B[83] - .04:
        oh['dy'] = (oh.get('dy') or 0) + hopOn(t, 83, 1.0)
    clawd(ROW21[HIM_I], GND, u, oh)
    land = clamp((t - (B[81] - .3)) / .3)
    oe = emH(t, [[0, 'happy'], [ek(82), 'happy'], [ek(83), 'excited', {'emote': None}]], view='q', flip=True)
    if t >= B[81] - .3:
        herN(ROW21[HER_I], lerp(-150, GND, easeIn(land)), u, oe)
    if t >= B[81] - .04:
        stamp('咚', ROW21[HER_I] + 6 * u, GND - 10 * u, 56, '#FFFFFF', t - B[81], rot=.12, life=.4)
    if t >= B[83] - .04:
        bubble(920, GND - 13.5 * u, '不怕！', 70, (920, GND - 9 * u), popIn(t, 83), key='s21b', col='#FFFBE8', tcol=HOT)
        floatHearts(t, 83, 6, 560, 260, 720, 520, 18)
        floatHearts(t, 84, 6, 1130, 260, 1300, 520, 18)
    if t < B[81]:
        stamp('都一样…', ROW21[HIM_I], GND - 12 * u, 46, '#8A8794', t - B[80], rot=-.08, life=.9)
    camEnd()


# =====================================================================================
# S22 43.12–45.19 · 示例歌词 占位文字示例: she holds a big heart at the start line → dashes off, dust → grey runners cough in the dust → finish, the heart to him
def s22(t, lt, dur):
    run1 = clamp((t - (B[85] - .2)) / .2)
    run2 = clamp((t - (B[87] - .5)) / .46)
    cx = lerp(900, 1240, ease(run2))
    cam(t, cx, 540, 1.02)
    track(t, key='s22tr', finishX=1250)
    # start line
    flatRect(470, 650, 14, 300, '#FFFFFF')
    u = 26
    HX = 1670
    sx_ = 560 + 330 * easeOut(run1) + 470 * ease(run2)
    gy = [(150, 765, 0), (300, 935, 1)]
    cough = t >= B[86] - .04
    for (x, y, i) in gy:
        o = dict(col='#B8B6BE', dk='#8A8794', lt='#D8D6DC', view='q', eyes='squeeze' if cough else 'blank', mouth='O' if cough else None,
                 boilKey=f's22g{i}', aL=.1, aR=.15 if not cough else 1.3, dx=.1 * math.sin(t * 40) if cough else 0)
        clawd(x, y, 22, o)
    # finish tape: whole until she breaks it on k87, then two loose ends
    broke = t >= B[87] - .2
    boilSeed('s22tape')
    if not broke:
        inkLine([[1262, 700], [1262, 900]], 3.0, '#E8476E', 'ink', 0)
    else:
        a_ = clamp((t - (B[87] - .2)) / .3)
        inkLine([[1262, 700], [1262 + 60 * a_, 760], [1262 + 30 * a_, 800]], 3.0, '#E8476E', 'ink', .6)
        inkLine([[1262, 900], [1262 + 70 * a_, 860], [1262 + 40 * a_, 830]], 3.0, '#E8476E', 'ink', .6)
    oh = emM(t, [[0, 'hopeful'], [ek(87), 'happy', {'eyes': 'heart', 'blush': .8}]], view='q', flip=True)
    oh['aR'] = .4 if t >= B[87] - .1 else .3
    himN(HX, 840, u, oh)
    oe = emH(t, [[0, 'determined'], [ek(85), 'excited', {'emote': None}], [ek(87), 'love']], view='q')
    running = (B[85] - .2 < t < B[85] + .1) or (B[87] - .5 < t < B[87])
    if running:
        oe.update(move('run', t))
        oe['smear'] = .5
        oe['rot'] = 0
    oe['aR'] = 1.1
    herN(sx_, 840, u, oe)
    # the big heart: in her hand → into his arms (held low in front of him) on k87
    hd = handXY(sx_, 840, u, oe, 'R')
    give = clamp((t - (B[87] - .14)) / .14)
    tgt = (HX - 1.6 * u, 840 - 3.6 * u)
    hx_, hy_ = lerp(hd[0] + 40, tgt[0], give), lerp(hd[1] - 60, tgt[1], give) - 80 * math.sin(give * math.pi)
    heart(hx_, hy_, lerp(62, 48, give), HOT, key='s22h')
    if give < .5:
        dot(hd[0], hd[1], .5 * u, HER['col'])
        ring(hd[0], hd[1], .5 * u, INK, 2.5)
    if t >= B[85] - .2:
        dustCloud(sx_ - 6 * u, 880, 90, t - (B[85] - .1), key='s22d1')
        dustCloud(440, 850, 130, t - (B[86] - .3), key='s22d2')
    if t >= B[85] - .04:
        stamp('冲！', 860, 300, 72, '#FFFFFF', t - B[85], rot=-.1, life=.45)
    if cough:
        stamp('咳咳', 330, 600, 60, '#FFFFFF', t - B[86], rot=.1)
    if t >= B[84] - .04 and t < B[85]:
        stamp('预备', 560, 420, 60, '#FFFFFF', t - B[84], rot=-.1)
    if t >= B[87] - .04:
        stamp('No.1', HX - 120, 400, 84, '#FFC93D', t - B[87], rot=-.1)
        floatHearts(t, 87, 6, HX - 300, 480, HX + 100, 640, 18)
    camEnd()


# =====================================================================================
# S23 45.19–47.26 · 示例歌词 占位文字示例: eye line dashes → it lights up 「叮」 → both jump at once → quiz cards both show a heart, 默契 100%
def s23(t, lt, dur):
    gradRect(-400, -400, W + 800, 1300, ['#D8ECFF', '#EAF5FF'])
    for i in range(-3, 40):
        for j in range(0, 16):
            if (i + j) % 2 == 0:
                G.c.drawCircle(i * 70 + (35 if j % 2 else 0), j * 70, 5, skia.Paint(AntiAlias=True, Color=skcol('#BFD8F2', .7)))
    cam(t, 960, 560, 1.03)
    flatRect(-400, 860, W + 800, 500, '#BFD8F2')
    inkLine([[-400, 860], [W + 400, 860]], 1.0, INK, 'ink', 0)
    sx_, hx = 720, 1210
    u = 35
    ja = (t - (B[90] - .24)) / .48
    j = -3.0 * math.sin(clamp(ja) * math.pi) if 0 <= ja <= 1 else 0.0
    oe = emH(t, [[0, 'hopeful', {'lookX': .9}], [ek(89), 'starstruck'], [ek(90), 'excited', {'emote': None}], [ek(91), 'love']], view='q')
    oh = emM(t, [[0, 'hopeful', {'lookX': .9}], [ek(89), 'starstruck'], [ek(90), 'excited', {'emote': None}], [ek(91), 'happy', {'eyes': 'heart', 'blush': .8}]],
             view='q', flip=True)
    oe['dy'] = (oe.get('dy') or 0) * .3 + j
    oh['dy'] = (oh.get('dy') or 0) * .3 + j
    oe['rot'] = oh['rot'] = 0
    herN(sx_, GND, u, oe)
    himN(hx, GND, u, oh)
    ey = GND - 6 * u + ((oe.get('dy') or 0) + (oh.get('dy') or 0)) * .5 * u
    e1, e2 = (sx_ + 3.2 * u, ey), (hx - 3.2 * u, ey)
    if t >= B[88] - .2 and t < B[90] - .3:
        dk = clamp((t - (B[88] - .2)) / .2)
        n = 9
        for i in range(n):
            f0, f1 = i / n, (i + .5) / n
            if f0 > dk:
                break
            x0, x1 = lerp(e1[0], e2[0], f0), lerp(e1[0], e2[0], min(f1, dk))
            lit = t >= B[89] - .04
            line(x0, ey, x1, ey, '#FFC93D' if lit else '#E8476E', 1, 9 if lit else 7)
        if t >= B[89] - .04:
            for i in range(5):
                sparkle(lerp(e1[0], e2[0], (i + .5) / 5), ey - 10, 22 * hitK(t, 89, .4) + 8, '#FFC93D')
            stamp('叮！', 960, ey - 150, 64, '#FFC93D', t - B[89], rot=-.1, life=.8)
    if t >= B[90] - .04:
        stamp('同时', 960, 220, 64, '#FFFFFF', t - B[90], rot=.1, life=.45)
    if t >= B[91] - .04:
        k91 = popIn(t, 91)
        for x, key in ((sx_ - 330, 'a'), (hx + 330, 'b')):
            push()
            translate(x, 380)
            scale(k91)
            boilSeed('s23q' + key)
            paint(rrPts(-120, -150, 240, 300, 20), wash='#FFFDF6', ink=INK, sw=1.0)
            flatRect(-108, -138, 216, 66, '#FCE3EA')
            text('最喜欢？', 0, -104, 38, HOT, shadow=False)
            heart(0, 40, 64, HOT, key='s23qh' + key)
            pop()
        stamp('默契 100%', 960, 300, 84, RED, t - B[91], rot=-.1, stroke='#FFFFFF')
    camEnd()


# =====================================================================================
# S24 47.26–49.32 · 示例歌词占 位文 字示例歌 词占位文字示: summer jasmine hedge → her flower glows → jasmine opens one by one → he brings a jasmine bunch
def s24(t, lt, dur):
    cam(t, 960, 540, lerp(1.0, 1.05, ease(lt / dur)))
    jasmineWall(t, key='s24jw')
    # a little hanging month card 「7月」 on a stake
    boilSeed('s24stk')
    paint(rectPts(1700, 560, 16, 300), wash='#8A5A3C', ink=INK, sw=.7)
    paint(rrPts(1620, 480, 180, 130, 12), wash='#FFFDF6', ink=INK, sw=.9)
    flatRect(1626, 486, 168, 40, '#7CC36B')
    text('7月', 1710, 560, 56, '#4E9A5A', face=WENKAI, shadow=False)
    sx_, hx = 760, 1260
    u = 32
    oe = emH(t, [[0, 'happy', {'eyes': 'closed', 'blush': .7}], [ek(93), 'happy', {'eyes': 'closed', 'blush': 1.0}], [ek(94), 'starstruck'], [ek(95), 'love']], view='q')
    herN(sx_, GND, u, oe)
    if t >= B[93] - .04:
        fx, fy = sx_ - 2.0 * u, GND - 8.6 * u + (oe.get('dy') or 0) * u
        glow(fx, fy, 120, '#FFFBE0', 1.0 * hitK(t, 93, .5) + .3)
        for i in range(6):
            a = i / 6 * TAU + t
            sparkle(fx + math.cos(a) * 70, fy + math.sin(a) * 50, 10 + 8 * hitK(t, 93, .4), '#FFFFFF')
    # three big jasmine flowers opening one after another, the last on k94
    for i, (x, y) in enumerate(((330, 520), (470, 430), (1080, 470))):
        tb = B[94] - .26 + i * .12
        k = clamp((t - tb) / .12)
        if k > 0:
            jasmine(x, y, 52, k, key=f's24big{i}', glowK=.5 * k)
    if t >= B[94] - .04:
        stamp('开了', 600, 300, 60, '#FFFFFF', t - B[94], rot=-.1, life=.8)
    walk = clamp((t - (B[95] - .44)) / .4)
    hxx = lerp(1500, hx, ease(walk))
    oh = emM(t, [[0, 'happy'], [ek(95), 'happy', {'eyes': 'heart', 'blush': .8}]], view='q', flip=True)
    if 0 < walk < 1:
        oh.update(move('walk', t, 1))
    oh['aR'] = .9
    if t >= B[95] - .44:
        himN(hxx, GND, u, oh)
        hd = handXY(hxx, GND, u, oh, 'R')
        jasmineBunch(hd[0], hd[1], 58, key='s24jb', rot=-.75)
        dot(hd[0], hd[1], .5 * u, ME['col'])
        ring(hd[0], hd[1], .5 * u, INK, 2.5)
    if t >= B[95] - .04:
        # the scent drifts over to her as a heart
        for i in range(3):
            ph = clamp((t - B[95]) * 1.2 - i * .15)
            inkLine([[hx - 300 - 60 * ph, 500 - 40 * i], [hx - 380 - 80 * ph, 470 - 40 * i + 20 * math.sin(t * 6 + i)], [hx - 460 - 100 * ph, 500 - 40 * i]],
                    1.0, '#FFFFFF', 'ink', .6)
        heart(sx_ + 120, GND - 12 * u, 46 * popIn(t, 95), '#FFFFFF', key='s24ht')
        stamp('好香', hx - 360, 380, 60, HOT, t - B[95], rot=.1, stroke='#FFFFFF')
    camEnd()


# =====================================================================================
# S25 49.32–END · 示例歌词 占位文字示例: back at the calendar wall. He sings → a card written for her → she hugs it → the page curls → torn: 「100 未完待续」
CAL25 = dict(cx=960, top=80, w=270, h=290)


def s25(t, lt, dur):
    cam(t, 960, 540, lerp(1.02, 1.07, ease(lt / dur)))
    wallRoom(t, key='w25')
    sets2.photoString(t, 1240, 1720, 600, key='s25ps')
    sets2.wallClock(1560, 300, 80, t, key='s25clk')
    plantPot(250, 900, 70, key='s25pl')
    plantPot(1780, 900, 56, key='s25pl2', col='#8CCB7A')
    curl = es(t, kt(99) - .2, kt(99) - .02) * .7
    tk = (t - (B[100] - .2)) / .44
    num = '99' if tk < 0 else '100'
    dayCal(CAL25['cx'], CAL25['top'], CAL25['w'], CAL25['h'], num, t, key='cal25', heartK=1.0 if num == '99' else 0,
           curl=curl if num == '99' else 0, under='100', sub='未完待续' if num == '100' else None)
    if 0 <= tk < 1:
        push()
        translate(CAL25['cx'] + 260 * tk, CAL25['top'] - 900 * ease(tk) + 20 * math.sin(tk * 6))
        rotate(.6 * tk)
        nn.calPage('99', CAL25['w'], CAL25['h'], 'cal25t', heartK=1.0)
        pop()
    st = nm.loveseat(960, 900, 620, col='#7FB8B0', key='s25ls')
    u = 26
    hop = hopOn(t, 100, 1.0, .3)
    oh = emM(t, [[0, 'happy', {'mouth': 'open', 'eyes': 'closed'}], [ek(97), 'hopeful'], [ek(98), 'happy', {'blush': .8}], [ek(100), 'excited', {'emote': None}]],
             view='q')
    oe = emH(t, [[0, 'happy', {'eyes': 'heart', 'blush': .7}], [ek(97), 'hopeful'], [ek(98), 'happy', {'eyes': 'closed', 'blush': 1.0}],
                 [ek(100), 'excited', {'emote': None}]], view='q', flip=True)
    oh.update(rot=0, dy=min(0, oh.get('dy', 0)) * .3 + hop)
    oe.update(rot=0, dy=min(0, oe.get('dy', 0)) * .3 + hop)
    raiseK = es(t, kt(97) - .3, kt(97) - .12)
    give = clamp((t - (B[98] - .18)) / .18)
    oh['aL'] = lerp(.3, 1.2, raiseK) if give < 1 else lerp(1.2, .3, clamp((t - B[98]) / .2))
    seat(himN, 960 - 140, st, u, oh)
    seat(herN, 960 + 140, st, u, oe)
    nm.loveseatArms(960, 900, 620, col='#7FB8B0', key='s25ls')
    if t < B[97]:
        noteStream(t, B[96] - .3, 960 - 140 + 3 * u, st - 4 * u, 960 + 140, st - 8 * u, 5, s=34, arc=-120, dur=.5, key='s25n')
    if t >= B[96] - .04:
        stamp('唱给你', 560, 420, 60, '#FFFFFF', t - B[96], rot=-.1, life=.5)
    if t >= B[97] - .3:
        # k97: the card, written stroke by stroke, held up between them above their heads; k98: it drops into her lap
        hhd = handXY(960 - 140, st + 2 * u, u, oh, 'L')
        prog = clamp((t - (B[97] - .3)) / .28)
        up = (hhd[0] - 250 * .36, hhd[1] - 250 * .72 * .36)
        lap = (960 + 140 - 1.5 * u, st - 1.5 * u)
        cx_ = lerp(up[0], lap[0], ease(give))
        cy_ = lerp(up[1], lap[1], ease(give))
        w_ = lerp(250, 120, ease(give))
        loveCard(cx_, cy_, w_, prog, rot=-.04, key='s25lc', k=clamp((t - (B[97] - .3)) / .12))
        if give < .5:
            dot(hhd[0], hhd[1], .55 * u, ME['col'])
            ring(hhd[0], hhd[1], .55 * u, INK, 2.5)
    if t >= B[98] - .04:
        floatHearts(t, 98, 5, 1060, 470, 1240, 600, 16)
        stamp('收好啦', 1330, 470, 52, HOT, t - B[98], rot=.1, stroke='#FFFFFF', life=.6)
    if t >= B[100] - .04:
        cxh, cyh = CAL25['cx'], CAL25['top'] + CAL25['h'] / 2
        for i in range(10):
            side = -1 if i % 2 else 1                               # two fans of hearts out of the page's left and right edges
            a = (i // 2 - 2) * .28
            r = 190 + 300 * easeOut(clamp((t - B[100]) / .5))
            heart(cxh + side * math.cos(a) * r, cyh + math.sin(a) * r * .8, 20, [HOT, '#FFC93D', '#F59AB0'][i % 3], key=f's25h{i}')
    camEnd()
