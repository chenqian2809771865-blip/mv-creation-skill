# story1.py: 《99》 shots S01–S13 (one rap line per bar, every beat a visible event). Data: storyboard.py.
import math
from nn import *
import nn

U = 32
GND = 880


def ear(x, y, u):
    """screen point just above a Clawd's head (for bubbles / clouds)"""
    return x, y - 8 * u


# =====================================================================================
# S01 0–1.80 · title device: the wall calendar. 「98」 is torn away and 「99」 lands on k1 (title complete)
CAL1 = dict(cx=800, top=170, w=560, h=640)


def s01(t, lt, dur):
    cam(t, 900, 540, lerp(1.0, 1.035, ease(lt / dur)))
    wallRoom(t, key='w1')
    sets2.photoString(t, 1180, 1690, 600, key='s1ps')
    sets2.wallClock(1560, 300, 80, t, key='s1clk')
    plantPot(250, 840, 70, key='s1pl')
    plantPot(1760, 840, 56, key='s1pl2', col='#8CCB7A')
    # k3: every fairy light flashes (the pickup 「baby」)
    fk = hitK(t, 3, .22) if t >= B[3] - .04 else 0
    if fk > .02:
        sets2.fairyLights(t, -60, W + 60, 70, sag=60, n=22, key='w1fl', a=fk)
        for i in range(22):
            k_ = (i + .5) / 22
            glow(lerp(-60, W + 60, k_), 80 + 60 * math.sin(k_ * math.pi), 90, '#FFE9A0', .6 * fk)
    tk = (t - (B[1] - .32)) / .44
    tear = ('98', tk) if tk < 1 else None
    sway = .012 * math.sin(lt * 9) * math.exp(-max(0, t - B[1]) * 3) if t > B[1] - .1 else 0
    push()
    translate(CAL1['cx'], CAL1['top'] - 72)
    rotate(sway)
    translate(-CAL1['cx'], -(CAL1['top'] - 72))
    dayCal(CAL1['cx'], CAL1['top'], CAL1['w'], CAL1['h'], '99', t, key='cal', heartK=popIn(t, 2) if t >= B[2] - .04 else 0,
           tear=None, glint=hitK(t, 1, .3) if t >= B[1] - .04 else 0)
    pop()
    if tear:
        # the torn page flies up and out (fast start so the beat frame already shows the whole 99)
        k = clamp(tk)
        push()
        translate(CAL1['cx'] + 300 * k, CAL1['top'] - 1100 * ease(k) + 30 * math.sin(k * 6))
        rotate(.5 * k)
        nn.calPage('98', CAL1['w'], CAL1['h'], 'calt')
        pop()
    if t >= B[1] - .04:
        stamp('撕～', CAL1['cx'] + 360, CAL1['top'] + 120, 56, '#FFFFFF', t - B[1], rot=.15, life=.7)
    if t >= B[3] - .04:
        floatHearts(t, 3, 4, CAL1['cx'] - 300, CAL1['top'] + 100, CAL1['cx'] - 200, CAL1['top'] + 400, 16)
    camEnd()


# =====================================================================================
# S02 1.80–3.87 · 示例歌词 占位文: the EGO balloon pops out of his head, swells, she takes the string, it shrinks into a heart
def s02(t, lt, dur):
    sunburst(960, 620, '#FBD3DE', '#F7B9CA', 18, t * .12)
    cam(t, 960, 560, 1.02)
    hx, sx_ = 690, 1260
    u = 38
    oh = emM(t, [[0, 'proud'], [ek(5), 'smug'], [ek(6), 'surprised', {'emote': None}], [B[7] - .2, 'happy', {'eyes': 'closed', 'blush': 1.0}]], view='q')
    oe = emH(t, [[0, 'neutral'], [ek(5), 'happy'], [ek(6), 'happy', {'eyes': 'closed'}], [ek(7), 'love']], view='q', flip=True)
    raise_ = es(t, kt(5.6), kt(6) - .02)
    oe['aR'] = lerp(oe.get('aR', .2), 1.25, raise_)
    himN(hx, GND, u, oh)
    herN(sx_, GND, u, oe)
    # balloon
    headTop = (hx + .6 * u, GND - 8 * u + (oh.get('dy') or 0) * u)
    r = 0.0
    if t >= B[4] - .04:
        r = 105 * popIn(t, 4)
    if t >= B[5] - .14:
        r = lerp(r, 190, backOut(clamp((t - (B[5] - .14)) / .16)))
    shrink = clamp((t - (B[7] - .3)) / .14)
    if shrink > 0:
        r = lerp(190, 0, easeIn(shrink))
    drift = es(t, kt(5) - .14, kt(5) + .02)
    bx, by = lerp(hx + .6 * u, 960, drift), lerp(headTop[1] - 130 - 140 * popIn(t, 4) if t >= B[4] - .04 else headTop[1] - 60, 300, drift)
    hand = handXY(sx_, GND, u, oe, 'R')
    anchor = headTop if raise_ < .5 else hand
    if r > 3:
        egoBalloon(bx, by, r, 'EGO', key='s2eg', anchor=anchor, sq=.05 * math.sin(t * 12) * (1 if t > B[5] else 0))
        if raise_ >= .5:
            dot(hand[0], hand[1], .55 * u, HER['col'])
            ring(hand[0], hand[1], .55 * u, INK, 2.5)
    if t >= B[5] - .04 and t < B[7] - .1:
        stamp('膨～', 1180, 200, 70, '#FFC93D', t - B[5], rot=.15, life=.8)
    if t >= B[6] - .04 and t < B[7]:
        stamp('包容', 1400, 470, 60, HOT, t - B[6], rot=-.12, stroke='#FFFFFF')
    if t >= B[7] - .16:
        # the balloon has become a small heart that drops onto his head, landing on the k7 frame
        k7 = clamp((t - (B[7] - .16)) / .16)
        hy = lerp(by, headTop[1] - 34, easeIn(k7))
        heart(lerp(bx, headTop[0], easeIn(k7)), hy, 44, HOT, key='s2h')
        if t >= B[7] - .02:
            stamp('啵', headTop[0] + 120, headTop[1] - 90, 56, '#FFFFFF', t - B[7], rot=.12, life=.6)
        if t > B[7] + .15:
            floatHearts(t, 5, 5, hx - 120, GND - 12 * u, hx + 160, GND - 9 * u, 16)
    camEnd()


# =====================================================================================
# S03 3.87–5.93 · 示例歌词占位文字 示例歌: rain cloud → huff + steam → the steam blows the cloud away → sun, she claps
def s03(t, lt, dur):
    cam(t, 960, 540, lerp(1.04, 1.07, ease(lt / dur)))
    nm.livingBack(t)
    hx, sx_ = 740, 1300
    u = 36
    oh = emM(t, [[0, 'sad'], [ek(9), 'angry'], [ek(10), 'determined'], [ek(11), 'happy']], view='q')
    oe = emH(t, [[0, 'nervous'], [ek(9), 'surprised', {'emote': None}], [ek(11), 'laugh']], view='q', flip=True)
    if t >= B[11] - .1:
        oe.update(aL=1.5 + .25 * math.sin(t * 26), aR=1.5 + .25 * math.sin(t * 26 + 1), rot=0)
    himN(hx, GND, u, oh)
    herN(sx_, GND, u, oe)
    cx, cy = hx + 20, GND - 13.4 * u
    blow = clamp((t - (B[10] - .1)) / .36)
    if t < B[10] + .3:
        ex = cx - 260 * ease(blow)
        ey = cy - 760 * ease(blow)
        emoCloud(ex, ey, 120 * popIn(t, 8) if t < B[8] + .2 else 120, t, rain=1 - blow, a=1, key='s3ec')
        if blow > 0:
            for i in range(5):
                yy = ey - 60 + i * 30
                xx = ex - 90 + i * 45
                inkLine([[xx, ey + 90 + 80 * blow], [xx + 20 * blow, ey + 90 + 220 * blow]], 1.0, '#FFFFFF', 'ink', 0)
    if t >= B[9] - .06:
        steamPuff(hx + .6 * u, GND - 9 * u, 34, t - (B[9] - .06), dirx=1, key='s3st')
        steamPuff(hx + .6 * u, GND - 9 * u, 30, t - (B[10] - .2), dirx=1, key='s3st2')
        stamp('哼！', hx - 5.5 * u, GND - 10 * u, 84, '#FFFFFF', t - B[9], rot=-.15, life=.9)
    if t >= B[10] - .04:
        stamp('呼——', hx - 6 * u, GND - 14 * u, 64, '#BFE3F5', t - B[10], rot=-.1, life=.45)
    if t >= B[11] - .06:
        littleSun(cx, cy - 30, 70, clamp((t - (B[11] - .06)) / .14), t, key='s3sun')
        sparkles(t, 11, 7, 420, 120, 1500, 420, 12)
        stamp('啪啪', sx_ + 5.5 * u, GND - 12 * u, 60, '#FFFFFF', t - B[11], rot=.12)
    camEnd()


# =====================================================================================
# S04 5.93–8.00 · 示例歌词占 位文字示例歌: a heart 「谢谢」 → the grudge book pops up → erased → binned, 不记仇
def s04(t, lt, dur):
    cam(t, 960, 540, 1.03)
    wallRoom(t, c1='#FBE3D2', c2='#F6D2BC', key='w4')
    sets2.wallClock(1650, 260, 64, t, key='s4clk')
    sets2.photoString(t, 120, 620, 220, key='s4ps')
    nm.cocoaTable(t, 960, 800, key='s4ct')
    hx, sx_ = 540, 1380
    u = 36
    oh = emM(t, [[0, 'happy'], [ek(13), 'happy', {'eyes': 'closed', 'blush': .7}], [ek(14), 'nervous'], [ek(15), 'happy', {'eyes': 'heart', 'blush': .8}]], view='q')
    oe = emH(t, [[0, 'hopeful'], [ek(13), 'love'], [ek(14), 'thinking'], [ek(15), 'playful']], view='q', flip=True)
    give = clamp((t - (B[13] - .2)) / .2)
    oh['aR'] = lerp(1.0, .3, give)
    himN(hx, GND, u, oh)
    herN(sx_, GND, u, oe)
    # k12: the heart card 「谢谢」 in his hand; k13: it flies into her arms (held low in front of her, under her mouth)
    hh = handXY(hx, GND, u, oh, 'R')
    if t >= B[12] - .2:
        k12 = popIn(t, 12) if t < B[13] - .2 else 1.0
        p0 = (hh[0] + 60, hh[1] - 50)
        p1 = (sx_ - 2.2 * u, GND - 3.4 * u)
        f = ease(give)
        x_ = lerp(p0[0], p1[0], f)
        y_ = lerp(p0[1], p1[1], f) - 160 * math.sin(f * math.pi)
        r_ = lerp(70, 54, f) * k12
        heart(x_, y_, r_, HOT, key='s4ht')
        text('谢谢', x_, y_ - 2, r_ * .56, '#FFFFFF', stroke=INK, strokeW=6, shadow=False)
        if give < .5:
            dot(hh[0], hh[1], .5 * u, ME['col'])
            ring(hh[0], hh[1], .5 * u, INK, 2.5)
    if t >= B[13] - .04:
        stamp('收到', sx_ + 4.5 * u, GND - 11 * u, 56, HOT, t - B[13], rot=.12, stroke='#FFFFFF', life=.5)
    # k14: her grudge book pops up as a comic panel; the eraser sweeps it blank, landing on k15; then it is binned
    px, py = 1180, 330
    if t >= B[14] - .04:
        toss = clamp((t - (B[15] + .26)) / .3)
        k14 = popIn(t, 14)
        er = clamp((t - (B[15] - .3)) / .26)
        bxp = lerp(px, 1730, easeIn(toss))
        byp = lerp(py, 720, easeIn(toss)) - 160 * math.sin(toss * math.pi)
        if toss < 1:
            push()
            translate(bxp, byp)
            scale(k14 * lerp(1, .5, toss))
            grudgeBook(0, 0, 250, open_=1 if toss < .2 else 0, erased=er, rot=1.4 * easeIn(toss), key='s4gb')
            if t >= B[14] - .04 and er < 1:
                ex = lerp(-250, 250, er)
                eraser(ex, -30 + 70 * math.sin(er * 26), 52, -.3, key='s4er')
                if er > 0:
                    crumbs(ex, 0, t, t - (B[15] - .3), key='s4cr')
            pop()
        if toss <= 0:
            for j, f in enumerate((.3, .55, .8)):
                dot(lerp(sx_ - 40, px + 60, f), lerp(GND - 8.6 * u, py + 190, f), 8 + j * 4, '#FFFFFF')
    if t >= B[14] - .04:
        stamp('记仇本？', 640, 170, 56, '#FFFFFF', t - B[14], rot=-.1, life=.45)
    tp.wastebasket(1730, 880, 170, 190, key='s4wb', back=False)
    if t >= B[15] - .04:
        stamp('不记仇', 760, 230, 96, RED, t - B[15], rot=-.14, stroke='#FFFFFF')
    if t >= B[15] + .5:
        stamp('进！', 1730, 600, 56, '#FFFFFF', t - (B[15] + .56), rot=.12, life=.6)
    camEnd()


# =====================================================================================
# S05 8.00–10.06 · 示例歌词占位文字示例歌: chin up 「我没错」 → she glares → he bows 「对不起」 → she pats his head
def s05(t, lt, dur):
    stripes('#FFF3C8', '#FBE7A1', 80, -t * 30)
    cam(t, 960, 560, 1.02)
    hx, sx_ = 770, 1300
    u = 38
    bow = es(t, kt(18) - .2, kt(18) - .02)
    oh = emM(t, [[0, 'proud'], [ek(17), 'nervous'], [ek(18), 'sad', {'tint': None, 'gloom': 0}], [ek(19), 'shy']], view='q')
    oh['rot'] = lerp(-.12, .24, bow)
    oh['dx'] = 0
    if bow > 0:
        oh['aR'] = lerp(oh.get('aR', .2), -.35, bow)
        oh['aL'] = lerp(oh.get('aL', .2), -.35, bow)
    oe = emH(t, [[0, 'suspicious'], [ek(17), 'angry'], [ek(18), 'surprised', {'emote': None}], [ek(19), 'happy']], view='q', flip=True)
    pat = es(t, kt(19) - .2, kt(19) - .02)
    oe['aR'] = lerp(oe.get('aR', .2), .55, pat)
    oe['dx'] = lerp(0, -.6, pat)
    himN(hx, GND, u, oh)
    herN(sx_, GND, u, oe)
    if t < B[18] - .06:
        bubble(hx - 60, GND - 12.6 * u, '我没错', 50, (hx, GND - 9 * u), popIn(t, 16), key='s5b1')
    else:
        bubble(hx - 40, GND - 11.2 * u, '对不起…', 50, (hx + 3 * u, GND - 8 * u), popIn(t, 18), key='s5b2', col='#FFF3E2')
    if t >= B[17] - .04 and t < B[18]:
        stamp('哼', sx_ + 5.4 * u, GND - 10.5 * u, 80, '#FFFFFF', t - B[17], rot=.12)
    if t >= B[19] - .04:
        hd = handXY(sx_, GND, u, oe, 'R')
        dot(hd[0], hd[1], .5 * u, HER['col'])
        ring(hd[0], hd[1], .5 * u, INK, 2.5)
        stamp('摸摸', hd[0] + 10, hd[1] - 120, 56, HOT, t - B[19], rot=-.1, stroke='#FFFFFF')
        floatHearts(t, 9, 5, hx - 60, GND - 13 * u, hx + 260, GND - 9 * u, 18)
    camEnd()


# =====================================================================================
# S06 10.06–12.13 · 示例歌词 占位文字示例: the projector screen lights → popcorn → the screen turns into space → planets float out
def filmReel(x, y, s, key='fr'):
    boilSeed(key)
    paint(ellPts(x, y, s, s, 22), wash='#3D3A52', ink=INK, sw=.7)
    for i in range(5):
        a = i / 5 * TAU
        paint(ellPts(x + math.cos(a) * s * .55, y + math.sin(a) * s * .55, s * .2, s * .2, 10), wash='#FFFDF6', ink=None)
    G.c.drawCircle(x, y, s * .12, skia.Paint(AntiAlias=True, Color=skcol('#FFFDF6')))


def planetSmall(x, y, r, col, ring_=False, key='pls'):
    boilSeed(key)
    paint(ellPts(x, y, r, r, 24), wash=col, fill=mixCol(col, INK, .25), fillOp=60, ink=INK, sw=.8)
    if ring_:
        paint(ellPts(x, y, r * 1.8, r * .4, 30, 0, -.3), wash=None, ink='#F3D9A0', sw=1.4)


def s06(t, lt, dur):
    cam(t, 960, 540, 1.0)
    space = clamp((t - (B[22] - .14)) / .14)
    # night living room (dim)
    gradRect(-400, -400, W + 800, 1300, ['#2A2F5A', '#3B3F70'])
    flatRect(-400, 860, W + 800, 500, '#4A3E5E')
    inkLine([[-400, 860], [W + 400, 860]], 1.0, INK, 'ink', 0)
    sets2.fairyLights(t, -60, W + 60, 60, sag=40, n=20, key='s6fl', a=.8)
    # projector screen on the left wall
    sx0, sy0, sw_, sh_ = 120, 150, 860, 520
    boilSeed('s6scr')
    inkLine([[sx0 - 20, sy0 - 20], [sx0 + sw_ + 20, sy0 - 20]], 3.0, '#9AA3B8', 'ink', 0)
    on = clamp((t - (B[20] - .06)) / .1) if t >= B[20] - .1 else .15
    paint(rectPts(sx0, sy0, sw_, sh_), wash=mixCol('#5A5E80', '#FFF6E0', on), ink=INK, sw=1.0)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(sx0 + 6, sy0 + 6, sw_ - 12, sh_ - 12))
    if space < 1 and on > .5:
        # the movie: a tiny cartoon couple under a moon on a cliff
        gradRect(sx0, sy0, sw_, sh_, ['#FFD9A8', '#F59AB0'])
        flatRect(sx0, sy0 + sh_ * .72, sw_, sh_ * .3, '#7A4A6A')
        glow(sx0 + sw_ * .7, sy0 + sh_ * .3, 160, '#FFF6C8', .8)
        G.c.drawCircle(sx0 + sw_ * .7, sy0 + sh_ * .3, 60, skia.Paint(AntiAlias=True, Color=skcol('#FFF6C8')))
        for j, (dx, col) in enumerate(((-.07, '#2B2233'), (.04, '#2B2233'))):
            G.c.drawRect(skia.Rect.MakeXYWH(sx0 + sw_ * (.42 + dx), sy0 + sh_ * .55, 46, 52), skia.Paint(AntiAlias=True, Color=skcol(col)))
        flatRect(sx0, sy0, sw_, 46, INK)
        flatRect(sx0, sy0 + sh_ - 46, sw_, 46, INK)
        text('今晚的电影 · 开场', sx0 + sw_ / 2, sy0 + 23, 28, '#FFF6E0', face=WENKAI, shadow=False)
    if space > 0:
        G.c.saveLayerAlpha(None, int(255 * space))
        gradRect(sx0, sy0, sw_, sh_, ['#0C1140', '#3A2A7A', '#6A3A8A'])
        hl.stars(t, 5, 60, sx0, sy0, sx0 + sw_, sy0 + sh_, a=1.0)
        sets.milkyWay(.8)
        G.c.restore()
    G.c.restore()
    if on > .5 and space < 1:
        tp.tvGlow(.6 * on, t, '#FFE2B0')
    # couch on the right, the two seated, looking left at the screen
    st = nm.loveseat(1430, 900, 600, col='#E27A92', key='s6ls')
    u = 25
    lookUp = 1 if t >= B[22] - .06 else 0
    oh = emM(t, [[0, 'hopeful'], [ek(21), 'happy'], [ek(22), 'surprised', {'emote': None}], [ek(23), 'starstruck']], view='q', flip=True,
             lookX=.6, lookY=-.3 * lookUp)
    oe = emH(t, [[0, 'hopeful'], [ek(21), 'laugh'], [ek(22), 'surprised', {'emote': None}], [ek(23), 'starstruck']], view='q', flip=True,
             lookX=.6, lookY=-.3 * lookUp)
    oh.update(dy=min(0, oh.get('dy', 0)) * .3, rot=0)
    oe.update(dy=min(0, oe.get('dy', 0)) * .3, rot=0)
    if t >= B[23] - .2:
        oe['aR'] = lerp(.3, .95, es(t, kt(23) - .2, kt(23) - .02))
    seat(herN, 1430 - 140, st, u, oe)
    seat(himN, 1430 + 140, st, u, oh)
    nm.loveseatArms(1430, 900, 600, col='#E27A92', key='s6ls')
    # popcorn bucket on the floor in front of the couch
    tp.popcorn(1740, 640, 44, t, jumpTb=B[21] - .06, key='s6pop')
    if t >= B[21] - .04:
        k21 = popIn(t, 21)
        bubble(1430, 420, '        ', 54, (1430, 560), k21, key='s6b')
        if k21 > .3:
            filmReel(1380, 420, 34 * k21, key='s6r1')
            filmReel(1480, 420, 34 * k21, key='s6r2')
        if t < B[22] - .1:
            stamp('嘭', 1740, 470, 56, '#FFFFFF', t - B[21], rot=.12, life=.5)
    if space > 0:
        stamp('哇', 1200, 300, 80, '#FFE36E', t - B[22], rot=.1, life=.45)
    # k23: planets float out of the screen into the room
    if t >= B[23] - .2:
        a23 = t - (B[23] - .2)
        f = easeOut(clamp(a23 / .3))
        planetSmall(lerp(700, 1060, f), lerp(380, 300, f), 70, '#F2A65A', True, key='s6p1')
        hd = handXY(1430 - 140, st + 2 * 25, 25, oe, 'R')
        dot(hd[0], hd[1], .5 * 25, HER['col'])
        ring(hd[0], hd[1], .5 * 25, INK, 2.5)
        for j in range(6):
            f_ = (j + .5) / 6 * f
            dot(lerp(hd[0], 1060 + 60, f_), lerp(hd[1], 300 + 40, f_), 5, '#FFE36E')
        stamp('土星！', 1060, 180, 56, '#FFE36E', t - B[23], rot=-.08)
        planetSmall(lerp(400, 640, f), lerp(300, 220, f), 40, '#8FD3FF', key='s6p2')
        planetSmall(lerp(800, 1180, f), lerp(560, 600, f), 30, '#F59AB0', key='s6p3')
        sparkles(t, 23, 10, 500, 120, 1300, 700, 10)
    camEnd()


# =====================================================================================
# S07 12.13–14.20 · 示例歌词 占位文字示例: pantry pops onto the shelf; the two look at a little 「以后」 notebook; a house in the cloud
def s07(t, lt, dur):
    cam(t, 960, 540, lerp(1.02, 1.06, ease(lt / dur)))
    kitchenBack(t, key='s7k')
    shelfBoard(180, 900, 600, key='s7sh')
    for kind, x, k in (('柴', 290, 24), ('米', 460, 24), ('油', 630, 25), ('盐', 790, 25)):
        if t >= B[k] - .04:
            pantry(kind, x, 600, 84, popIn(t, k), key='s7p')
    if t >= B[24] - .04:
        stamp('柴米', 380, 330, 64, '#FFFFFF', t - B[24], rot=-.1, life=.8)
    if t >= B[25] - .04:
        stamp('油盐', 720, 330, 64, '#FFFFFF', t - B[25], rot=.1, life=.8)
    hx, sx_ = 1110, 1620
    u = 33
    oh = emM(t, [[0, 'happy'], [ek(26), 'thinking'], [ek(27), 'happy', {'eyes': 'heart', 'blush': .8}]], view='q', lookX=.6)
    oe = emH(t, [[0, 'happy'], [ek(26), 'thinking'], [ek(27), 'love']], view='q', flip=True, lookX=.6)
    oe['aR'] = lerp(.2, .95, es(t, kt(26) - .2, kt(26) - .02))
    himN(hx, GND, u, oh)
    herN(sx_, GND, u, oe)
    if t >= B[26] - .2:
        hd = handXY(sx_, GND, u, oe, 'R')
        k26 = popIn(t, 26)
        push()
        translate(hd[0] - 20, hd[1] - 36)
        rotate(-.08)
        scale(k26)
        boilSeed('s7nb')
        paint(rrPts(-70, -50, 140, 100, 8), wash='#7FC6E8', ink=INK, sw=.8)
        paint(rectPts(-58, -38, 116, 76), wash='#FFFDF6', ink=INK, sw=.5)
        text('以后', 0, -2, 40, '#5A4A6A', face=WENKAI, shadow=False)
        pop()
        dot(hd[0], hd[1], .5 * u, HER['col'])
        ring(hd[0], hd[1], .5 * u, INK, 2.5)
    if t >= B[27] - .06:
        k27 = clamp((t - (B[27] - .06)) / .16)
        thoughtCloud(1360, 300, 440, 300, k27, tail=(1360, GND - 9 * u), key='s7tc')
        houseIcon(1360, 310, 84, k27, key='s7hs')
    camEnd()


# =====================================================================================
# S08 14.20–16.26 · 示例歌词占 位文字示例歌: the plan board fills up beat by beat; a suitcase pops, she puts on a straw hat
def s08(t, lt, dur):
    cam(t, 960, 540, 1.03)
    wallRoom(t, c1='#E3EEF7', c2='#D2E3F0', key='w8', dots='#BFD3E6')
    corkBoard(140, 130, 980, 540, key='s8cb')
    text('我们的计划', 630, 175, 46, '#5A4A6A', face=WENKAI, shadow=False)
    stickyNote(330, 330, 200, '约会', -.08, popIn(t, 28) if t >= B[28] - .04 else 0, '#F9CFDA', key='s8n1',
               icon=lambda x, y, s: heart(x, y, s * .8, HOT, key='s8nh'))
    movieTicket(590, 300, 220, .1, popIn(t, 29) if t >= B[29] - .04 else 0, key='s8t1')
    movieTicket(620, 430, 220, -.06, popIn(t, 29) if t >= B[29] - .04 else 0, key='s8t2', col='#BFE3F5')
    stickyNote(900, 360, 210, '旅游', .07, popIn(t, 30) if t >= B[30] - .04 else 0, '#CDEFE0', key='s8n2',
               icon=lambda x, y, s: planeIcon(x, y, s * 1.2, key='s8pl'))
    if t >= B[30] - .04:
        redString([[330, 300], [470, 250], [600, 280], [760, 300], [900, 320]], clamp((t - (B[30] - .04)) / .14))
        stamp('出发！', 920, 600, 56, '#FFFFFF', t - B[30], rot=.1, life=.9)
    hx, sx_ = 1180, 1530
    u = 32
    oh = emM(t, [[0, 'happy'], [ek(29), 'excited'], [ek(31), 'happy']], view='q', flip=True, lookX=.4)
    hatOn = t >= B[31] - .04
    oe = emH(t, [[0, 'hopeful'], [ek(30), 'happy'], [ek(31), 'excited', {'emote': None}]], view='q', flip=True,
             hat='straw' if hatOn else 'flower')
    if hatOn:
        oe['dy'] = (oe.get('dy') or 0) + hopOn(t, 31, 1.4)
    himN(hx, GND, u, oh)
    herN(sx_, GND, u, oe)
    if t >= B[31] - .06:
        ks = clamp((t - (B[31] - .06)) / .14)
        ch.suitcase(1760, GND, 40 * backOut(ks), col='#F59AB0', key='s8sc')
        stamp('啪', 1880, GND - 300, 60, '#FFFFFF', t - B[31], rot=-.1, life=.6)
    camEnd()


# =====================================================================================
# S09 16.26–18.33 · 示例歌词占 位文字示例歌: the 99 rocket pops up, they hop in, 3·2·1 ignition, lift-off into space
def s09(t, lt, dur):
    up = clamp((t - (B[35] - .1)) / .1)
    rise = 0.0
    if t >= B[34] - .04:
        rise = 40 * clamp((t - B[34]) / .5)
    if up < 1:
        cam(t, 960, 540, 1.0)
        gradRect(-400, -400, W + 800, 1900, ['#0C1140', '#26306E', '#46468A'])
        hl.stars(t, 9, 90, -100, -100, W + 100, 720, a=1.0)
        boilSeed('s9moon')
        paint(ellPts(1640, 180, 56, 56, 26), wash='#FFF8E4', ink=None)
        tp.skyline(800, '#2A2A55', '#FFD98A', .7, key='s9sky')
        flatRect(-400, 840, W + 800, 500, '#2E4A52')
        boilSeed('s9gr')
        paint([[-400, 860], [500, 830], [1200, 850], [W + 400, 832], [W + 400, 1300], [-400, 1300]], wash='#3A5E5A', ink=INK, sw=.9)
        hl.fireflies(t, 9, 10, 100, 600, W - 100, 840)
        RX, RY, S = 960, 850 - rise, 110
        rk = popIn(t, 32) if t >= B[32] - .04 else 0
        u = 22
        jumped = t >= B[33] - .42
        if rk > .01:
            push()
            translate(RX, RY)
            scale(1, rk)
            translate(-RX, -RY)
            rocketBox(RX, RY, S, t, flame=0, key='s9rk', front=False, back=True)
            pop()
        rim = RY - 2.95 * S
        shake = 4 * math.sin(t * 60) if t >= B[34] - .04 else 0
        if jumped:
            ja = clamp((t - (B[33] - .42)) / .42)
            for who, x0, x1 in ((herN, 440, RX - 112), (himN, 1480, RX + 112)):
                x = lerp(x0, x1, ease(ja))
                yl = rim + 1.4 * u + 2 * u
                y = lerp(GND, yl, ease(ja)) - 260 * 4 * ja * (1 - ja)
                o = emH(t, [[0, 'excited', {'emote': None}], [ek(34), 'starstruck']], view='front') if who is herN else \
                    emM(t, [[0, 'excited', {'emote': None}], [ek(34), 'determined']], view='front')
                o.update(dx=shake / u, rot=0, dy=0, aL=1.2, aR=1.2)
                if ja >= 1:
                    o['noLegs'] = True
                    o['noShadow'] = True
                who(x, y, u, o)
        else:
            oe = emH(t, [[0, 'surprised', {'emote': None}]], view='q')
            oh = emM(t, [[0, 'surprised', {'emote': None}]], view='q', flip=True)
            herN(440, GND, 30, oe)
            himN(1480, GND, 30, oh)
        if rk > .01:
            push()
            translate(RX + shake, RY)
            scale(1, rk)
            translate(-RX - shake, -RY)
            fl = clamp((t - (B[34] - .06)) / .1)
            rocketBox(RX + shake, RY, S, t, flame=fl, key='s9rk', front=True, back=False)
            pop()
        if t >= B[32] - .04:
            stamp('造！', 960, 200, 70, '#FFE36E', t - B[32], rot=-.1, life=.45)
        if t >= B[34] - .04:
            stamp('3·2·1', 1480, 300, 80, '#FFE36E', t - B[34], rot=.12)
            for i in range(6):
                puff(RX - 300 + i * 120, 860 + 10 * math.sin(i), 26 + 16 * clamp((t - B[34]) / .4), '#E8E4F0', key=f's9sm{i}', a=.9)
        camEnd()
        if up > 0:
            flash(.3 * up)
        return
    # k35: up in space — the rocket flying, the earth below
    cam(t, 960, 540, 1.0)
    gradRect(-400, -400, W + 800, 1900, ['#060A2A', '#141A4A', '#2A2266'])
    hl.stars(t, 13, 140, -100, -100, W + 100, H + 100, a=1.0)
    sets.milkyWay(.7)
    earthBall(420, 1180, 520, key='s9earth')
    a35 = t - B[35]
    fx, fy = 1150 + 260 * a35, 600 - 300 * a35
    speedLines(t, 35, 10, fx - 600, fy - 200, fx + 200, fy + 400, '#FFFFFF', .5, 260)
    push()
    translate(fx, fy)
    rotate(.5)
    translate(-fx, -fy)
    rocketBox(fx, fy, 70, t, flame=0, key='s9rk2', front=False, back=True)
    u = 14
    for who, dx in ((herN, -72), (himN, 72)):
        o = emH(t, [[0, 'starstruck']], view='front') if who is herN else emM(t, [[0, 'starstruck']], view='front')
        o.update(noLegs=True, noShadow=True, aL=1.4, aR=1.4, dy=0, rot=0)
        who(fx + dx, fy - 2.95 * 70 + 3.4 * u, u, o)
    rocketBox(fx, fy, 70, t, flame=1.0, key='s9rk2', front=True, back=False)
    pop()
    stamp('出发！', 560, 220, 84, '#FFE36E', a35, rot=-.1)
    flash(.2 * (1 - clamp(a35 / .1)))
    camEnd()


# =====================================================================================
# S10 18.33–20.40 · 示例歌词占位文字示例歌: her frown scribble → it jumps onto him → his scribble grows → he holds his head, 苦恼
def s10(t, lt, dur):
    gradRect(-400, -400, W + 800, 1300, ['#C9C1D6', '#B3A9C6'])
    cam(t, 960, 560, lerp(1.03, 1.08, ease(lt / dur)))
    flatRect(-400, 860, W + 800, 500, '#9C8AB0')
    inkLine([[-400, 860], [W + 400, 860]], 1.0, INK, 'ink', 0)
    sets2.wallClock(1020, 170, 60, t, key='s10clk')
    sets2.bookshelf(120, 380, 300, 480, key='s10bs', who='her', night=0.3)
    sets2.photoString(t, 1420, 1880, 200, key='s10ps')
    plantPot(1780, 860, 60, key='s10pl', col='#9DB89A')
    sx_, hx = 760, 1240
    u = 36
    oe = emH(t, [[0, 'sad', {'tint': None}], [ek(37), 'sad', {'tint': None}], [ek(39), 'surprised', {'emote': None}]], view='q', lookX=-.3)
    oh = emM(t, [[0, 'nervous'], [ek(37), 'nervous'], [ek(38), 'sad', {'tint': None}], [ek(39), 'cry', {'tint': None}]], view='q', flip=True)
    if t >= B[39] - .1:
        hk = es(t, kt(39) - .1, kt(39) - .02)
        oh.update(view='front', flip=False, aL=lerp(.9, 1.75, hk), aR=lerp(.9, 1.75, hk), dy=0, rot=0, dx=0)
    herN(sx_, GND, u, oe)
    himN(hx, GND, u, oh)
    if t >= B[36] - .04:
        scribble(sx_ - 1.2 * u, GND - 12.4 * u, 70, popIn(t, 36), t, key='s10s1')
    if t >= B[37] - .14:
        # a little scribble hops from her head to his
        f = clamp((t - (B[37] - .14)) / .14)
        sz = 40 if t < B[38] - .06 else lerp(40, 100, backOut(clamp((t - (B[38] - .06)) / .14)))
        x = lerp(sx_ - 1.2 * u, hx + .5 * u, ease(f))
        y = lerp(GND - 12.4 * u, GND - 12.0 * u, f) - 140 * math.sin(f * math.pi)
        scribble(x, y, sz, 1.0, t * 1.4, key='s10s2')
    if t >= B[38] - .04:
        stamp('乱', hx + 6.2 * u, GND - 12.5 * u, 70, '#FFFFFF', t - B[38], rot=.15, life=.9)
    if t >= B[39] - .04:
        stamp('苦恼', 1000, 360, 110, RED, t - B[39], rot=-.12, stroke='#FFFFFF')
    camEnd()


# =====================================================================================
# S11 20.40–22.46 · 示例歌词占位文字示例歌词: she walks ahead, he follows; she looks back twice, he is always there
def s11(t, lt, dur):
    # she walks ahead (to the right), he follows a few steps behind; on k41 and k43 she turns around and he is right there
    W1 = clamp((t - (B[40] - .1)) / (B[41] - .16 - (B[40] - .1)))        # walk k40 → just before k41
    W2 = clamp((t - (B[42] - .1)) / (B[43] - .16 - (B[42] - .1)))        # walk k42 → just before k43
    walkX = 220 * W1 + 220 * W2
    cam(t, 1010 + walkX * .85, 540, 1.04)
    gradRect(-400, -400, W + 1800, 1500, ['#F7A86A', '#FBC98A', '#FFE7B8'])
    glow(1900, 700, 700, '#FFD08A', .6)
    tp.skyline(780, '#C77A6A', None, 0, key='s11sky')
    push()
    translate(960, 0)
    tp.skyline(780, '#C77A6A', None, 0, key='s11sky2')
    pop()
    flatRect(-400, 820, W + 1800, 600, '#C9A06A')
    boilSeed('s11path')
    paint([[-400, 860], [W + 1400, 850], [W + 1400, 1300], [-400, 1300]], wash='#E6C79A', ink=INK, sw=.8)
    for x in (80, 760, 1440, 2120, 2800):
        props.tree(x, 830, 80, key=f's11tr{x}', col='#E0A04A')
    for x in (420, 2480):
        props.lamp(x, 840, 44, on=.6, key=f's11lp{x}')
    u = 28
    sx_ = 1240 + walkX
    hx = 720 + walkX
    walking = (B[40] - .1 <= t < B[41] - .16) or (B[42] - .1 <= t < B[43] - .16)
    look1 = B[41] - .16 <= t < B[42] - .12
    look2 = t >= B[43] - .16
    if walking:
        oe = emH(t, [[0, 'happy']], view='side')
        oe.update(move('walk', t))
        oe['walk'] = (t - B[40]) * 2.6
    else:
        oe = emH(t, [[0, 'happy'], [ek(41), 'happy', {'eyes': 'shine', 'blush': .6}], [ek(42), 'happy'], [ek(43), 'love']], view='q', flip=True)
        if look1 or look2:
            oe['dy'] = (oe.get('dy') or 0) + hopOn(t, 41 if look1 else 43, .8, .26)
        else:
            oe.update(view='qback', flip=False)
    if walking:
        oh = emM(t, [[0, 'happy']], view='side')
        oh.update(move('walk', t, 1))
        oh['walk'] = (t - B[40]) * 2.6 + .25
    else:
        oh = emM(t, [[0, 'happy'], [ek(41), 'excited', {'emote': None}], [ek(42), 'happy'], [ek(43), 'happy', {'eyes': 'heart', 'blush': .8}]], view='q')
        if look1:
            oh['aR'] = 1.4 + .3 * math.sin(t * 20)
        if look2:
            oh['aR'] = 1.15
    herN(sx_, GND, u, oe)
    himN(hx, GND, u, oh)
    if look1 and t >= B[41] - .04:
        bubble(hx - 30, GND - 12.4 * u, '在！', 58, (hx, GND - 8.5 * u), popIn(t, 41), key='s11b1')
        stamp('回头', sx_ + 4.6 * u, GND - 11 * u, 56, '#FFFFFF', t - B[41], rot=.12, life=.6)
    if look2:
        hd = handXY(hx, GND, u, oh, 'R')
        k43 = popIn(t, 43) if t >= B[43] - .04 else 0
        if k43 > .01:
            push()
            translate(hd[0] + 10, hd[1] - 30)
            scale(k43)
            boilSeed('s11sign')
            inkLine([[0, 30], [0, -50]], 2.2, '#8A5A3C', 'ink', 0)
            heart(0, -120, 84, HOT, key='s11h')
            text('一直在', 0, -122, 36, '#FFFFFF', stroke=INK, strokeW=5, shadow=False)
            pop()
            dot(hd[0], hd[1], .5 * u, ME['col'])
            ring(hd[0], hd[1], .5 * u, INK, 2.5)
            floatHearts(t, 43, 5, sx_ - 200, GND - 13 * u, sx_ + 100, GND - 9 * u, 16)
            stamp('又回头', sx_ + 4.6 * u, GND - 11 * u, 56, '#FFFFFF', t - B[43], rot=.12, life=.6)
    camEnd()


# =====================================================================================
# S12 22.46–24.53 · 示例歌词 占位文字示例: grey crowd fills the street → the two slip through → towers rise → they leap over the roofs
def towers(t, k, key='tw'):
    cols = ['#9FB7D8', '#B9A8D8', '#8FC7C0', '#D8A8B8', '#A8C0E0', '#C8B8E8']
    for i in range(7):
        x = -120 + i * 330 + 40 * hash1(i)
        hgt = ((520 + 180 * hash1(i * 3.1)) if i not in (3, 4) else 400) * clamp(k * 1.3 - i * .05)
        if hgt < 4:
            continue
        w = 220 + 60 * hash1(i * 1.7)
        boilSeed(f'{key}{i}')
        paint(rectPts(x, 820 - hgt, w, hgt), wash=cols[i % 6], fill=mixCol(cols[i % 6], INK, .25), fillOp=60, ink=INK, sw=.9)
        for j in range(int(hgt // 70)):
            flatRect(x + 20, 820 - hgt + 30 + j * 70, w - 40, 10, mixCol(cols[i % 6], '#FFFFFF', .35))
        paint(rrPts(x + w / 2 - 40, 820 - hgt + 14, 80, 30, 8), wash='#FFE36E', ink=INK, sw=.5)


def s12(t, lt, dur):
    cam(t, 960, 540, 1.02)
    gradRect(-400, -400, W + 800, 1300, ['#A9DBF5', '#DDF2FB', '#FFF6E2'])
    puff(300, 120, 26, key='s12c1')
    puff(1500, 90, 22, key='s12c2')
    tk = clamp((t - (B[46] - .2)) / .2)
    towers(t, .35 + .65 * easeOut(tk), key='s12tw')
    flatRect(-400, 820, W + 800, 500, '#E9DCCB')
    for i in range(-3, 24):
        line(i * 100, 820, i * 100 - 30, 1300, '#C9B8A2', .6, 2)
    inkLine([[-400, 820], [W + 400, 820]], 1.0, INK, 'ink', 0)
    if t >= B[46] - .04:
        stamp('长高！', 1500, 180, 64, '#FFFFFF', t - B[46], rot=.1, life=.45)
    # the crowd (two rows), drawn back row first
    crowdK = popIn(t, 44) if t >= B[44] - .04 else 0
    gap = es(t, kt(45) - .2, kt(45) - .02)
    back = [(140, 860), (430, 852), (720, 862), (1180, 856), (1470, 860), (1760, 852)]
    for i, (x, y) in enumerate(back):
        if crowdK > .01:
            push()
            lean = (-.16 if x < 960 else .16) * gap
            translate(x, y)
            rotate(lean)
            translate(-x, -y)
            wx.greyClawd(x + (-(70) if x < 960 else 70) * gap, y - 40 * (1 - crowdK), 22, i, a=clamp(crowdK), key='s12b')
            pop()
    if t >= B[45] - .04 and t < B[46] + .1:
        bubble(960, 420, '借过～', 54, None, popIn(t, 45), key='s12jg')
    u = 26
    jump = 0.0
    if t >= B[47] - .4:
        a = clamp((t - (B[47] - .4)) / .8)
        jump = -17 * u * math.sin(a * math.pi)
    run = clamp((t - (B[45] - .3)) / (B[47] - B[45] + .3))
    px = lerp(560, 1240, ease(run))
    oe = emH(t, [[0, 'surprised', {'emote': None}], [ek(45), 'determined'], [ek(47), 'excited', {'emote': None}]], view='q')
    oh = emM(t, [[0, 'surprised', {'emote': None}], [ek(45), 'determined'], [ek(47), 'excited', {'emote': None}]], view='q')
    if B[45] - .3 < t < B[47] - .44:
        oe.update(move('run', t))
        oh.update(move('run', t, 1))
        oe['rot'] = oh['rot'] = 0
    oe['dy'] = (oe.get('dy') or 0) + jump / u
    oh['dy'] = (oh.get('dy') or 0) + jump / u
    herN(px + 150, 900, u, oe)
    himN(px - 150, 900, u, oh)
    front = [(110, 945), (1810, 945)]
    for i, (x, y) in enumerate(front):
        if crowdK > .01:
            wx.greyClawd(x + (-(110) if x < 960 else 110) * gap, y + 60 * (1 - crowdK), 24, i + 3, a=clamp(crowdK), key='s12f')
    if t >= B[44] - .04:
        stamp('人好多', 960, 200, 64, '#FFFFFF', t - B[44], rot=-.08, life=.45)
    if t >= B[47] - .04:
        floatHearts(t, 47, 7, px - 260, 160, px + 260, 380, 20)
        stamp('跳过去！', px + 420, 160, 72, '#FFE36E', t - B[47], rot=-.1)
    camEnd()


# =====================================================================================
# S13 24.53–26.59 · 示例歌词占位 文字示例歌词占位: night hill, she wishes, he wishes, a shooting star, the wish strip floats up
def s13(t, lt, dur):
    cam(t, 900, 520, lerp(1.0, 1.06, ease(lt / dur)))
    sets2.nightHill(t, 1.0, key='s13nh', moonK=1.0, tree=True)
    u = 28
    sx_, hx = 800, 1120
    sy, hy = sets2.hillY2(sx_), sets2.hillY2(hx)
    pray = {'eyes': 'closed', 'mouth': 'smile', 'blush': .5}
    oe = emH(t, [[0, 'hopeful'], [ek(48), 'hopeful', pray]], view='front')
    oh = emM(t, [[0, 'hopeful'], [ek(49), 'hopeful', pray]], view='front')
    for o, kk in ((oe, 48), (oh, 49)):
        if t >= B[kk] - .1:
            o.update(aL=1.95, aR=1.95, dy=0, rot=0)
    herN(sx_, sy, u, oe)
    himN(hx, hy, u, oh)
    for x, y, kk in ((sx_, sy, 48), (hx, hy, 49)):
        if t >= B[kk] - .04:
            glow(x, y - 3.4 * u, 70, '#FFF2B0', .8 * popIn(t, kk))
            paint(starPts(x, y - 3.6 * u, 16 * popIn(t, kk), .45, 5), wash='#FFF3A8', ink=INK, sw=.5)
    if t >= B[48] - .04:
        stamp('许愿', sx_ - 6 * u, sy - 11 * u, 52, '#FFF3A8', t - B[48], rot=-.1, life=.45)
    sk = (t - (B[50] - .2)) / .3
    shootingStar(1900, 40, 1180, 360, sk, key='s13ss')
    if t >= B[51] - .2:
        a = t - (B[51] - .2)
        wy = lerp(sy - 8 * u, 250, easeOut(clamp(a / .5)))
        wishStrip(lerp(960, 1340, easeOut(clamp(a / .5))), wy, 96, '示例歌词', rot=.08 * math.sin(t * 5), key='s13ws')
        sparkles(t, 51, 8, 1200, wy - 100, 1480, wy + 200, 12)
    camEnd()
