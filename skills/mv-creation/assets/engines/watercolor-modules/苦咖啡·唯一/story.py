# story.py: 《苦咖啡·唯一》 shots S01–S14 (intro, the 唯一 sample hook, chorus 1). Shot data: storyboard.py.
# Clawd couple (him clay + café apron 「橙」; her pink with the white flower). Every beat carries a visible event.
import math
from eng import *
import eng
from clawd import *
from props import bubble, stamp, sparkle, sparkles, impactLines, stripes, sunburst, puff, floatHearts
from sets2 import seat
from sets import sea, palm, sunDisc
from dx import flagPop, speedLines, backpack, deskBell
from sm import rainCloud
from props_chuanshao import snowflakes
from hl import memoryGrade, vignette, tint
from nm import polaroidW
from wx import ecgTrace, line, _pa
from common import *
from kf import *


U_WIDE = 31          # character size in the full corner shots


def addJ(o, j):
    o['dy'] = (o.get('dy') or 0) + j['dy']
    o['sq'] = (o.get('sq') or 0) + j['sq']
    return o


def heldCup(hx, hy, s=.5, fill=1.0, key='hc', steam=0.0, t=0.0, col=None, handCol=None, label=None):
    """a cup held in a hand at (hx, hy): cup body centred on the hand, hand nub drawn over the cup's side"""
    cup(hx + 4, hy + 30 * s, s, fill=fill, key=key, saucer=False, steam=steam, t=t, label=label)
    handDot(hx - 10 * s, hy - 4 * s, handCol or PAL['clay'], 10)


def memory(k=1.0):
    memoryGrade(k)
    vignette(.42 * k, '#5A3A1A')


def sigh(x, y, age, dirn=1):
    if 0 <= age < .6:
        a = 1 - age / .6
        puff(x + dirn * 60 * age, y - 30 * age, 9 + 8 * age, '#FFFFFF', key='sigh', a=.85 * a)


# =====================================================================================
# S01 0–3.71 · A1 title device: the chalk A-board writes 苦咖啡·唯一 one character a beat (complete on k4), then doodles
def s01(t, lt, dur):
    cam(t, 960, 540, lerp(1.0, 1.04, ease(lt / dur)))
    skyGrad(DUSK_SKY)
    skyline(.55, 's1sk')
    pavement(GY, .25, 's1pv')
    on = clamp((t - (B[4] - .04)) / .08)
    stringLights(t, -40, 1520, 110, sag=70, n=14, key='s1sl', on=.15 + .85 * on)
    cart(t, 1700, GY, .95, .2, key='s1cart', lit=on)
    potPlant(1230, GY, 1.2, 's1pp')
    if on > 0:
        sparkles(t, 11, 8, 100, 60, 1500, 260, 14 * on, '#FFE7A0')

    def inner(bx, by, bw, bh):
        cx = bx + bw / 2
        sz = 112
        for i, (c_, k) in enumerate([('苦', 0), ('咖', 1), ('啡', 2)]):
            chalkText(c_, cx + (i - 1) * sz * 1.08, by + 128, sz, writeK(t, k, .26))
        chalkText('·', cx - sz * 1.32, by + 262, sz * .9, writeK(t, 3, .2), col='#FFD9A8')
        chalkText('唯', cx - sz * .56, by + 262, sz, writeK(t, 3, .26), col='#FFD9A8')
        chalkText('一', cx + sz * .56, by + 262, sz, writeK(t, 4, .26), col='#FFD9A8')
        chalkText('·', cx + sz * 1.32, by + 262, sz * .9, writeK(t, 4, .2), col='#FFD9A8')
        # doodles: a cup (k5), its steam (k6), a heart with a hairline crack (k7)
        ux, uy = cx - 92, by + 470
        chalkLine([[ux - 46, uy - 56], [ux - 38, uy], [ux + 38, uy], [ux + 46, uy - 56], [ux - 46, uy - 56]], writeK(t, 5, .26), CHALK, 1.2)
        chalkLine([[ux + 44, uy - 44], [ux + 70, uy - 38], [ux + 66, uy - 14], [ux + 40, uy - 12]], writeK(t, 5, .26), CHALK, 1.0)
        for j in range(2):
            chalkLine([[ux - 14 + j * 28, uy - 68], [ux - 26 + j * 28, uy - 92], [ux - 8 + j * 28, uy - 116], [ux - 20 + j * 28, uy - 140]],
                      writeK(t, 6, .26), CHALK, .9)
        hp = heartPts(cx + 104, uy - 64, 46, 22)
        chalkLine(hp + [hp[0]], writeK(t, 7, .26), '#FF9FBA', 1.2)
        chalkLine([[cx + 104, uy - 100], [cx + 94, uy - 78], [cx + 112, uy - 62], [cx + 100, uy - 40]], writeK(t, 7, .14, .1), '#FF9FBA', .7)
    aBoard(860, GY + 60, 1.55, 's1ab', 0, inner=inner)
    camEnd()


# S02 3.71–5.57 · the cart at night, alone; the drums stop for three beats
def s02(t, lt, dur):
    cam(t, 960, 560, 1.0)
    on = clamp((t - (B[8] - .04)) / .06)
    lay = corner(t, 'night', lights=on, key='cn2')
    x, y, u = LAY['he'], GY, U_WIDE
    keys = [[0, 'sad'], [ek(9), 'surprised', {'emote': None, 'mouth': 'flat'}], [ek(10), 'sad', {'lookX': 1.0}], [ek(11), 'sad', {'eyes': 'closed'}]]
    o = heO(t, keys, view='q', aR=.75, aL=.1)
    if t >= B[9] - .04:                          # the stop: he freezes, cup raised
        o.update(dy=0, sq=0, aR=1.0)
        if t < B[10] - .04:
            fk = clamp((t - (B[9] - .045)) / .1)
            for sx_ in (-1, 1):
                for j in range(3):
                    xx = x + sx_ * (6.2 + .5 * j) * u
                    G.c.drawLine(xx, y - (6.5 - j * 1.2) * u, xx, y - (5.4 - j * 1.2) * u,
                                 skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .9 * fk), StrokeWidth=5, StrokeCap=skia.Paint.kRound_Cap))
            text('！', x + 1.5 * u, y - 10.4 * u, 70 * backOut(fk), '#FFE36E', stroke=INK, strokeW=9)
    hx, hy = nearHand(x, y, u, o, LAY['cart'])
    him(x, y, u, o)
    put = landK(t, 11, .16)
    if put < 1 and t < B[11] - .16:
        heldCup(hx, hy, .5, fill=0, key='s2c', t=t)
    else:
        p = arcPt([hx, hy + 15], [LAY['cart'] - 150, lay['top']], 40, put)
        cup(p[0], p[1], .5, fill=0, key='s2c', saucer=False)
        if t >= B[11] - .04:
            stamp('嗒', LAY['cart'] - 150, lay['top'] - 90, 54, '#FFE7A0', bage(t, 11), rot=.1)
    if t >= B[10] - .04:
        bubble(x + 40, y - 12.4 * u, '…', 52, tail=(x + 30, y - 9 * u), k=clamp((t - (B[10] - .04)) / .14), key='s2b')
    sigh(x + 5.8 * u, y - 4.4 * u, t - B[11] + .04, 1)
    camEnd()


# S03 5.57–9.28 · memory: she hops in, rings the bell, his cup flies to her table, steam heart, 唯一 flag, he blushes
def s03(t, lt, dur):
    cam(t, 1010, 560, lerp(1.0, 1.08, ease(lt / dur)))
    lay = corner(t, 'day', key='cn3')
    tt = lay['table']
    u = U_WIDE
    # him
    kM = [[0, 'happy'], [ek(16), 'happy', {'lookX': 1}], [ek(19), 'shy', {'blush': 1.0}]]
    oM = heO(t, kM, view='q', aR=.5 + .7 * landK(t, 14, .2) * (1 - seg(t, B[14] + .1, B[14] + .4)))
    him(LAY['he'], GY, u, oM)
    if t >= B[19] - .04:
        a = t - (B[19] - .04)
        for ex in (-.4, 2.6):
            paint(ellPts(LAY['he'] + ex * u, GY - 4.9 * u, .8 * u, .42 * u, 12), wash='#FF4F6E', washOp=170, ink=None)
        for i in range(3):
            puff(LAY['he'] + 1.2 * u + (i - 1) * 60, GY - 9.6 * u - 50 * a - i * 14, 10 + 14 * clamp(a / .3), '#FFFFFF', key=f's3st{i}', a=1 - seg(a, .5, 1.2))
        floatHearts(t, 31, 5, LAY['he'] - 160, GY - 520, LAY['he'] + 160, GY - 300, 18)
    # her: lands on k12, bell k13, takes the cup k16, hops k18
    sx = LAY['she']
    kH = [[0, 'excited'], [ek(13), 'happy'], [ek(16), 'love'], [ek(18), 'starstruck']]
    oH = sheO(t, kH, view='q', flip=True)
    addJ(oH, jump(t, B[18] - .02, B[18] + .3, 2.4))
    land = t - B[12]
    if land < .3:
        oH['sq'] = (oH.get('sq') or 0) + .25 * math.exp(-land * 10)
    if after(t, 13) and t < B[14]:
        oH['aL'] = .9
    if t >= B[16] - .2:
        oH['aL'] = .75
        oH['aR'] = .75
    her(sx, GY, u, oH)
    if land < .35:
        impactLines(sx, GY - 10, 160, 210, 8, t, '#FFFFFF', 's3imp')
    # the bell on the table
    bellX = LAY['table'] + 62
    deskBell(bellX, tt, 40, ring=hitK(t, 13, .25), key='s3bell')
    if after(t, 13) and t < B[14]:
        handDot(bellX + 4, tt - 44, HER['col'], 11)
        stamp('叮！', bellX + 10, tt - 160, 60, '#FFE36E', bage(t, 13), rot=.1)
    # the cup: on the counter → arc to the table (k14) → into her hand (k16)
    c0 = [LAY['cart'] + 70, lay['top']]
    c1 = [LAY['table'] + 40, tt]
    if t < B[14]:
        k = clamp((t - (B[14] - .3)) / .3)
        p = arcPt(c0, c1, 160, ease(k))
        cup(p[0], p[1], .55, key='s3cup', steam=.6, t=t)
    elif t < B[16] - .16:
        cup(c1[0], c1[1], .55, key='s3cup', steam=1, t=t, heartSteam=clamp((t - (B[15] - .1)) / .25) if t >= B[15] - .1 else 0)
        if t < B[14] + .2:
            stamp('咻', c1[0] + 80, c1[1] - 120, 46, '#FFFFFF', bage(t, 14), rot=.12, life=.5)
    else:
        hx, hy = nearHand(sx, GY, u, oH, LAY['table'])
        k = landK(t, 16, .16)
        px, py = lerp(c1[0], hx - 10, k), lerp(c1[1], hy + 30, k)
        cup(px, py, .55, key='s3cup', saucer=k < .5, steam=1, t=t, rot=.45 * k * (1 - seg(t, B[17] - .1, B[17] + .1)))
        if k >= 1:
            handDot(px + 6, py - 14, HER['col'], 10)
        fk = clamp((t - (B[17] - .045)) / .16)
        if fk > 0:
            flagPop(px + 20, py - 50, 56, '唯一', fk, key='s3flag', col='#E8574A')
    if t >= B[16] - .04:
        floatHearts(t, 17, 6, sx - 200, GY - 560, sx + 160, GY - 320, 18)
    memory(.8)
    camEnd()


# S04 9.28–13.00 · two worlds: vertical split, each half tilts / squashes, the seam cracks and the halves drift apart
def s04(t, lt, dur):
    c = G.c
    gap = 14 + 40 * landK(t, 24, .14) + 90 * ease(seg(t, B[27] - .2, B[27] + .1))
    slideR = 1 - easeOut(clamp((t - (B[20] - .2)) / .2))
    aL = -.05 * easeOut(landK(t, 21, .14)) + .015 * math.sin(t * 3)
    aR = .05 * easeOut(landK(t, 22, .14)) + .015 * math.sin(t * 3 + 1)
    sq = .07 * hitK(t, 23, .2)
    flatRect(-200, -200, W + 400, H + 400, '#16131C')
    # ---- left: night, him at the cart
    c.save()
    c.clipRect(skia.Rect.MakeXYWH(-200, -200, 960 - gap / 2 + 200, H + 400))
    push()
    translate(480 - gap / 2, 560)
    rotate(aL)
    scale(1 + sq, 1 - sq)
    translate(-480, -560)
    cam(t, 1040, 540, 1.0)
    corner(t, 'night', key='cn4')
    if t >= B[25] - .045:
        k = backOut(clamp((t - (B[25] - .045)) / .16))
        puff(LAY['he'], 150, 52 * k, '#9AA3B8', key='s4rc', a=1)
        if k > .6:
            from hl import rain as _rain
            G.c.save()
            G.c.clipRect(skia.Rect.MakeXYWH(LAY['he'] - 150, 170, 300, GY - 170))
            _rain(t, 4, 40, LAY['he'] - 160, 170, LAY['he'] + 190, GY, col='#DCE6FF', a=.8)
            G.c.restore()
    oM = heO(t, [[0, 'sad'], [ek(27), 'sad', {'lookX': 1}]], view='q')
    him(LAY['he'], GY, U_WIDE, oM)
    camEnd()
    pop()
    c.restore()
    # ---- right: a sunny southern beach, her with a backpack
    c.save()
    c.clipRect(skia.Rect.MakeXYWH(960 + gap / 2, -200, 1200, H + 400))
    push()
    translate(1440 + gap / 2 + slideR * 960, 560)
    rotate(aR)
    scale(1 + sq, 1 - sq)
    translate(-1440, -560)
    gradRect(-200, -200, W + 400, 1000, ['#7EC8F0', '#BFE6F7', '#FFF1C8'])
    sk = backOut(clamp((t - (B[26] - .045)) / .16)) if t >= B[26] - .045 else 0
    if sk > 0:
        for i in range(10):
            a = i / 10 * TAU + t * .5
            G.c.drawLine(1640 + math.cos(a) * 120 * sk, 230 + math.sin(a) * 120 * sk, 1640 + math.cos(a) * 190 * sk, 230 + math.sin(a) * 190 * sk,
                         skia.Paint(AntiAlias=True, Color=skcol('#FFD23A'), StrokeWidth=10, StrokeCap=skia.Paint.kRound_Cap))
        paint(ellPts(1640, 230, 100 * sk, 100 * sk, 30), wash='#FFD23A', fill='#F2A81E', fillOp=60, ink=INK, sw=1.2)
    sea(620, '#3FA6C8', '#2A7FA0', t, key='s4sea')
    flatRect(-200, 790, W + 400, 400, '#F2D9A8')
    inkLine([[900, 790], [2100, 790]], 1.0, INK, 'ink', 0)
    palm(1780, 800, 64, key='s4palm', lean=-.18, t=t)
    oH = sheO(t, [[0, 'happy'], [ek(25), 'hopeful'], [ek(27), 'sad', {'lookX': 1}]], view='q', flip=True)
    backpack(1420, 800, 32, oH, col='#7FB8E6', key='s4bp')
    her(1420, 800, 32, oH)
    pop()
    c.restore()
    # ---- the seam: a clean slash on k20, a zigzag crack from k24
    kz = landK(t, 24, .12)
    if kz > 0:
        pts = []
        for i in range(13):
            y_ = -40 + i * 100
            pts.append([960 + (18 if i % 2 else -18) * kz, y_])
        inkLine(pts, 2.2, '#FFFFFF', 'ink', 0)
    if t < B[20] + .25:
        a = 1 - seg(t, B[20], B[20] + .25)
        flatRect(960 - 6, -50, 12, H + 100, '#FFFFFF', a)
    if t >= B[23] - .04:
        stamp('变', 960, 140, 120, '#FFE36E', bage(t, 23), rot=-.08, life=.9)
    if t >= B[27] - .04:
        stamp('…', 960, 520, 90, '#FFFFFF', bage(t, 27), rot=0)


# S05 13.00–16.71 · "回去": he runs on a conveyor toward the warm arch, it keeps receding; trip, face-plant, stamp
def s05(t, lt, dur):
    cam(t, 960, 540, 1.0)
    stripes('#FFF1DA', '#FBE3C4', 90)
    # the arch (recedes on k31 / k33)
    sc = 1 - .22 * landK(t, 31, .16) - .2 * landK(t, 33, .16)
    ax = 1560 + 120 * (1 - sc)
    ap = popK(t, 28, .16)
    if ap > 0:
        push()
        translate(ax, 800)
        scale(sc * ap)
        boilSeed('s5arch')
        glow(0, -230, 300, '#FFD27A', .8)
        paint(rrPts(-150, -420, 300, 420, 140), wash='#FFE2A8', fill='#F2B36B', fillOp=60, ink=INK, sw=1.4)
        paint(rrPts(-110, -380, 220, 380, 110), wash='#FFF6DE', ink=INK, sw=.9)
        # a tiny sunny cart inside the arch (the memory)
        paint(rectPts(-60, -120, 120, 80), wash=WOOD, ink=INK, sw=.6)
        awning(-80, 80, -200, 30, key='s5aw', cols=('#C8643C', '#FFF5E2'))
        paint(heartPts(0, -290, 30, 18), wash=HOT, ink=INK, sw=.6)
        paint(rrPts(-120, -500, 240, 70, 12), wash='#FFFDF6', ink=INK, sw=1.0)
        text('回去', 0, -465, 52, '#B04A2E', shadow=False)
        pop()
    # conveyor belt (speeds up on k30 / k32)
    spd = 200 + 500 * landK(t, 30, .2) + 700 * landK(t, 32, .2)
    if t >= B[35] - .04:
        spd = 0
    paint(rectPts(-100, 800, W + 200, 70), wash='#5A566E', ink=INK, sw=1.2)
    off = (t * spd) % 120
    for i in range(-2, 20):
        line(i * 120 + off, 806, i * 120 + off - 30, 864, '#8A86A0', 1, 4)
    for xr in (-60, W + 60):
        paint(ellPts(xr, 835, 40, 40, 20), wash='#3D3A52', ink=INK, sw=1.0)
    flatRect(-100, 870, W + 200, 300, '#E8D3B0')
    # him
    x, y, u = 720, 800, 34
    keys = [[0, 'determined'], [ek(30), 'nervous'], [ek(32), 'determined'], [ek(34), 'scared'], [ek(35), 'ko']]
    o = heO(t, keys, view='q')
    if after(t, 29) and t < B[34]:
        o.update(move('run', t * (1.6 if t > B[32] else 1.0)))
        o['draw'] = apron('q')
    if t >= B[34] - .1 and t < B[35] - .04:
        k = ease(seg(t, B[34] - .1, B[35] - .04))
        o.update(rot=.9 * k, dy=-5 * math.sin(.9 * k) - 1.2 * math.sin(k * math.pi))
    if t >= B[35] - .04:
        a = t - (B[35] - .04)
        o.update(rot=1.45, dy=-4.95, sq=.12 * math.exp(-a * 8), walk=None, aL=-.3, aR=-.3)
        x += 60
    him(x, y, u, o)
    if after(t, 30) and t < B[34]:
        for i in range(3):
            G.c.drawCircle(x - 120 - i * 40 - (t * 300 % 40), y - 40 - i * 8, 10 - i * 2, _pa('#FFFFFF', .7))
    if after(t, 32) and t < B[34]:
        speedLines(t, 10, 0, 520, 600, 820, L=180, col='#C9A57A', a=.7, seed=5)
    if t >= B[35] - .04:
        stamp('啪', x - 40, y - 360, 90, '#FFFFFF', bage(t, 35), rot=-.15)
        stamp('示例歌词', 960, 200, 120, '#E8574A', bage(t, 35), rot=-.06)
        impactLines(x + 160, y - 60, 120, 200, 10, t, INK, 's5imp')
    camEnd()


# S06 16.71–18.57 · back to now: he sits up dizzy, stands, shoulders the 「苦」 bean sack, thumps it onto the cart
def s06(t, lt, dur):
    cam(t, 800, 600, 1.32)
    lay = corner(t, 'night', key='cn6', cartLit=0)
    x, u = 620, 34
    keys = [[0, 'dizzy'], [ek(37), 'neutral'], [ek(38), 'determined'], [ek(39), 'proud']]
    o = heO(t, keys, view='q')
    standK = landK(t, 37, .16)
    bag = landK(t, 38, .16)
    if bag > 0:
        o.update(aL=1.4 * bag, aR=1.4 * bag)
    if t < B[37] - .16:
        seat(him, x, GY - 30, u, o)
    else:
        if t < B[37] + .3:
            addJ(o, dict(dy=-1.2 * math.sin(standK * math.pi), sq=.1 * math.exp(-(t - B[37]) * 8) if t > B[37] else 0))
        him(x, GY, u, o)
        if t >= B[37] - .04 and t < B[38]:
            for i in range(4):
                a = t - B[37]
                puff(x - 170 + i * 110, GY - 10 - 50 * a, 5 + 8 * a, '#E8E1F0', key=f's6d{i}', a=.7 * (1 - seg(a, .15, .4)))
    # the sack: on the ground → over his head (k38) → onto the counter (k39)
    if t < B[38] - .16:
        beanBag(780, GY, .9, 's6bag')
    elif t < B[39] - .16:
        l_, r_ = hands(x, GY, u, o)
        cx_, cy_ = (l_[0] + r_[0]) / 2, min(l_[1], r_[1]) - 30
        p_ = arcPt([780, GY], [cx_, cy_], 260, bag)
        p_[0] += 160 * math.sin(bag * math.pi)
        bx, by = p_
        beanBag(bx, by, .9, 's6bag')
        handDot(l_[0], l_[1], PAL['clay'], 10)
        handDot(r_[0], r_[1], PAL['clay'], 10)
    else:
        k = landK(t, 39, .16)
        l_, r_ = hands(x, GY, u, o)
        p = arcPt([(l_[0] + r_[0]) / 2, min(l_[1], r_[1]) - 30], [LAY['cart'] - 70, lay['top']], 90, k)
        beanBag(p[0], p[1], .9, 's6bag', rot=-.2 * (1 - k))
        if t >= B[39] - .04:
            a = t - (B[39] - .04)
            stamp('咚', LAY['cart'] - 70, lay['top'] - 220, 80, '#FFE7A0', a, rot=.1)
            for i in range(9):
                bx = LAY['cart'] - 70 + (i - 4) * 26
                by = lay['top'] - 30 - 160 * a + 380 * a * a - 30 * hash1(i)
                if by < lay['top']:
                    bean(bx + (i - 4) * 60 * a, by, 1.4, rot=a * 8 + i)
    if t < B[37]:
        emote('stars', x, GY - 30 - 10.2 * u, u * .9, 1, t)
    camEnd()


# S07 18.57–22.28 · the espresso: lights, two drops, a full black cup; he sips — 「苦！」, shivers, a ring of question marks
def s07(t, lt, dur):
    cx, cy = 790, 590
    cam(t, cx, cy, 1.7)
    lit = clamp((t - (B[40] - .04)) / .08)
    lay = corner(t, 'night', key='cn7', cartLit=lit, machine=False)
    top = lay['top']
    mx = LAY['cart'] - 110
    espresso(mx, top, 1.25, lit=lit, key='s7es')
    x, u = 610, 34
    keys = [[0, 'neutral'], [ek(44), 'hopeful', {'eyes': 'closed'}], [ek(45), 'neutral', {'eyes': 'squeeze', 'mouth': 'wobble', 'tint': 'pale', 'tintK': .4}],
            [ek(46), 'scared', {'emote': None}], [ek(47), 'confused', {'emote': None}]]
    o = heO(t, keys, view='q')
    lift = landK(t, 44, .2)
    if lift > 0:
        o['aR'] = .2 + .55 * lift
        o['aL'] = .2 + .55 * lift
    if t >= B[46] - .04:
        o['dx'] = (o.get('dx') or 0) + .25 * math.sin(t * 70) * math.exp(-(t - B[46]) * 3)
    him(x, GY, u, o)
    # drops k41, k42; the cup fills on k43
    fill = .25 * landK(t, 41, .1) + .25 * landK(t, 42, .1) + .5 * landK(t, 43, .12)
    for k in (41, 42):
        a = t - (B[k] - .2)
        if 0 <= a < .2:
            yy = lerp(top - 82 * 1.25, top - 50, a / .2)
            paint(ellPts(mx, yy, 9, 15, 12), wash='#6A3A22', ink=INK, sw=.4)
        if 0 <= t - B[k] < .5:
            stamp('滴', mx + 70, top - 150, 40, '#FFE7A0', t - B[k], rot=.1, life=.5)
    if t < B[44] - .2:
        cup(mx, top, .6, fill=fill, key='s7cup', steam=1.6 if t >= B[43] - .04 else 0, t=t, steamCol='#4A2C1E')
    else:
        hx, hy = nearHand(x, GY, u, o, LAY['cart'])
        k = clamp((t - (B[44] - .2)) / .2)
        px, py = lerp(mx, hx + 14, k), lerp(top, hy + 34, k)
        cup(px, py, .6, fill=1, key='s7cup', saucer=False, rot=-.5 * lift, steam=.8, t=t, steamCol='#4A2C1E')
        handDot(px + 14, py - 20, PAL['clay'], 10)
    if t >= B[40] - .04 and t < B[41]:
        stamp('嗡', mx, top - 210, 50, '#FFE7A0', bage(t, 40), rot=-.1)
    if t >= B[45] - .04:
        stamp('苦！', x - 30, GY - 11.5 * u, 110, '#6A4A3A', bage(t, 45), rot=-.12, stroke='#FFFFFF')
    if t >= B[46] - .04:
        n = 1 if t < B[47] - .04 else 7
        for i in range(n):
            a = -math.pi / 2 + (i / max(1, n) * TAU if n > 1 else 0) + (t - B[46]) * 1.6
            r = 0 if n == 1 else 6.5 * u
            k_ = backOut(clamp((t - (B[46 if n == 1 else 47] - .045)) / .14))
            text('？', x + 40 + math.cos(a) * r, GY - 8.5 * u + math.sin(a) * r * .55, 64 * k_, '#FFFFFF', stroke=INK, strokeW=9)
    camEnd()


# S08 22.28–24.14 · sleepless: the clocks jump an hour a beat
def s08(t, lt, dur):
    cam(t, 820, 560, 1.12)
    hrs = 1 + lastBeat(t, [49, 50, 51]) + 1
    jitter = hitK(t, [48, 49, 50, 51][hrs - 1], .1)
    bedroom(t, hh=hrs, mm=0, key='bd8', digital='%02d:00' % hrs, dshake=.12 * jitter)
    x, u = 900, 34
    keys = [[0, 'scared', {'eyes': 'wide', 'emote': None}], [ek(50), 'sad', {'eyes': 'wide', 'gloom': .6}], [ek(51), 'cry']]
    o = heO(t, keys, view='front', apron_=False, noShadow=True, noLegs=True)
    if t >= B[51] - .04:
        o.update(aL=1.6, aR=1.6)
    him(x, 880, u, o)
    bedFrontCover('bd8')
    # eye bags grow (k50+)
    if t >= B[50] - .04:
        for ex in (-1.8, 1.8):
            paint(ellPts(x + ex * u, 880 - 5.3 * u, .9 * u, .25 * u, 10), wash='#6A5A8A', washOp=150, ink=None)
    for i, k in enumerate([48, 49, 50, 51]):
        if 0 <= t - (B[k] - .04) < .5:
            stamp(['1点', '2点', '3点', '4点'][i], 1060, 120, 56, '#FFE36E', t - B[k], rot=.1, life=.45)
    camEnd()


# S09 24.14–25.99 · one person, one pour-over; a second cup pops in by habit and gets crossed out
def s09(t, lt, dur):
    cam(t, 820, 600, 1.4)
    lay = corner(t, 'night', lights=.15, lamp_=.25, key='cn9', items=False)
    top = lay['top']
    glow(860, top - 200, 300, '#FFD27A', .5)
    x, u = 610, 34
    keys = [[0, 'sad'], [ek(55), 'sad', {'lookX': 1}]]
    o = heO(t, keys, view='q', aR=1.0, aL=.2)
    gy = GY - 150
    boilSeed('s9crate')
    paint(rectPts(x - 190, gy, 380, 150, 3), wash=WOOD, fill=WOODDK, fillOp=60, ink=INK, sw=1.0)
    for j in range(1, 3):
        line(x - 190, gy + j * 50, x + 190, gy + j * 50, WOODDK, .8, 3)
    text('咖啡豆', x, gy + 78, 34, '#5A3A22', face=WENKAI, shadow=False, a=.8)
    him(x, gy, u, o)
    cupX = 860
    cup(cupX, top, .5, fill=.2 + .5 * landK(t, 54, .1), key='s9cup', saucer=True)
    dripper(cupX, top - 52, .9, key='s9dr')
    hx, hy = nearHand(x, gy, u, o, cupX)
    tilt = .45 * landK(t, 52, .16)
    sx_, sy_ = kettle(hx, hy, .9, tilt=tilt, key='s9ket')
    handDot(hx, hy, PAL['clay'], 10)
    if t >= B[52] - .04:
        pa = skia.Paint(AntiAlias=True, Color=skcol('#CFEFFF', .85), Style=skia.Paint.kStroke_Style, StrokeWidth=5, StrokeCap=skia.Paint.kRound_Cap)
        p = skia.Path()
        p.moveTo(sx_, sy_)
        p.quadTo(sx_ + 30, sy_ - 10, cupX, top - 110)
        G.c.drawPath(p, pa)
    if t >= B[53] - .16:
        for i in range(5):
            a = t - (B[53] - .16)
            G.c.drawCircle(cupX - 32 + i * 16, top - 114 - 8 * math.sin(a * 9 + i), 12 * clamp(a * 7), _pa('#C78B5A', .95))
    a54 = t - (B[54] - .16)
    if 0 <= a54 < .16:
        paint(ellPts(cupX, lerp(top - 52, top - 20, a54 / .16), 6, 9, 10), wash=COFFEE, ink=None)
    if t >= B[54] - .04 and t < B[55]:
        stamp('滴', cupX + 80, top - 170, 40, '#FFE7A0', bage(t, 54), rot=.1)
    if t >= B[55] - .25:
        k = backOut(clamp((t - (B[55] - .25)) / .12))
        push()
        translate(cupX + 150, top)
        scale(k)
        cup(0, 0, .5, fill=0, key='s9cup2')
        pop()
        if t >= B[55] - .12:
            a = t - (B[55] - .12)
            c_ = clamp(a * 9)
            G.c.drawLine(cupX + 100, top - 100, cupX + 100 + 100 * c_, top - 100 + 90 * c_,
                         skia.Paint(AntiAlias=True, Color=skcol('#D8394E'), StrokeWidth=12, StrokeCap=skia.Paint.kRound_Cap))
            G.c.drawLine(cupX + 200, top - 100, cupX + 200 - 100 * c_, top - 100 + 90 * c_,
                         skia.Paint(AntiAlias=True, Color=skcol('#D8394E'), StrokeWidth=12, StrokeCap=skia.Paint.kRound_Cap))
    camEnd()


# S10 25.99–27.85 · the geese fly south in a V; one with an orange scarf lags behind and ends up alone
def s10(t, lt, dur):
    cam(t, 960, 540, 1.0)
    skyGrad(['#5A4E96', '#C77FA0', '#FFC08A'], 1100)
    glow(1500, 760, 520, '#FFD08A', .7)
    paint(ellPts(1500, 780, 110, 110, 30), wash='#FFB36B', ink=None)
    hills(760, ['#7A5A8A', '#5A4472', '#3E3058'], t, 's10h')
    # the sign
    boilSeed('s10sign')
    paint(rectPts(300, 640, 16, 300), wash=WOODDK, ink=INK, sw=.8)
    paint([[200, 600], [470, 600], [520, 650], [470, 700], [200, 700]], wash='#FFF5E2', ink=INK, sw=1.0)
    text('南 →', 350, 652, 54, '#B04A2E', face=WENKAI, shadow=False)
    # V flock: enters at k56, pulls away on k58
    vx = lerp(-300, 1150, ease(clamp((t - (B[56] - .4)) / .4))) + 1200 * ease(seg(t, B[58] - .25, B[58] + .7))
    vs = 1 - .45 * ease(seg(t, B[58] - .25, B[58] + .7))
    for i in range(7):
        j = abs(i - 3)
        side = -1 if i < 3 else 1
        gx = vx - j * 130 * vs
        gy = 330 + side * j * 62 * vs
        goose(gx, gy, 1.15 * vs, t * 9 + i, 1, key=f's10g{i}')
    # the straggler
    lx = 400 + 50 * math.sin(t * 2)
    ly = 440 + 18 * math.sin(t * 5)
    flapK = 1 + 1.4 * hitK(t, 57, .25)
    goose(lx, ly, 1.5, t * 9 * flapK, 1, key='s10lag', scarf='#E8743B')
    if t >= B[57] - .04:
        for i in range(3):
            a = t - B[57]
            G.c.drawCircle(lx - 120 - i * 30, ly + 10 + i * 6, 8 * (1 - a), _pa('#FFFFFF', .6 * (1 - seg(a, .2, .5))))
    if t >= B[59] - .04:
        bubble(lx + 40, ly - 140, '…', 48, tail=(lx + 40, ly - 50), k=clamp((t - (B[59] - .04)) / .14), key='s10b')
    camEnd()


# S11 27.85–29.70 · frozen: snow, frost on him, icicles on the lamp, frozen into a block of ice
def s11(t, lt, dur):
    cam(t, 900, 560, 1.12)
    skyGrad(['#1A2246', '#2E3A6E', '#4E5A8E'])
    skyline(1.0, 's11sk')
    snowK = landK(t, 60, .12)
    pavement(GY, .9, 's11pv')
    flatRect(-500, GY, W + 1000, 30 * snowK, '#E8F2FA')
    hx, hy = streetLamp(1120, GY, 1.0, 1.0, 's11lp', dirn=-1, icicles=landK(t, 62, .16))
    x, u = 860, 36
    frost = .5 * landK(t, 61, .16) + .5 * landK(t, 63, .12)
    keys = [[0, 'sad'], [ek(61), 'sad', {'tint': 'blue', 'tintK': .5}], [ek(63), 'neutral', {'eyes': 'wide', 'mouth': 'o', 'emote': None}]]
    o = heO(t, keys, view='front')
    o['col'] = mixCol(ME['col'], '#BFD8EA', .6 * frost)
    o['lt'] = mixCol(ME['lt'], '#FFFFFF', .6 * frost)
    o['dk'] = mixCol(ME['dk'], '#7A9AB8', .6 * frost)
    if t >= B[63] - .04:
        o.update(dy=0, sq=0, aL=.3, aR=.3)
    him(x, GY, u, o)
    if frost > 0:
        inkLine([[x - 4.8 * u, GY - 7.85 * u + o.get('dy', 0) * u], [x + 4.9 * u, GY - 7.85 * u + o.get('dy', 0) * u]], 4 * frost, '#FFFFFF', 'ink', 0)
        for i in range(14):
            fx = x + (hash1(i * 3.1) - .5) * 10 * u
            fy = GY - 2.5 * u - hash1(i * 5.7) * 5.5 * u
            sparkle(fx, fy, 9 * frost, '#FFFFFF', frost)
    if after(t, 60):
        snowflakes(t, 3, 70, -100, -60, W + 100, GY + 20, 7)
    if t >= B[63] - .04:
        k = clamp((t - (B[63] - .04)) / .1)
        iceBlock(x, GY + 10, 12.5 * u, 11 * u, k, 's11ice')
        stamp('咔', x + 280, GY - 420, 80, '#CFEFFF', bage(t, 63), rot=.12)
    camEnd()


# S12–S14 · the ice heart
def iceStage(t, glowK, cracks, shards=0.0, zoom=1.0):
    gradRect(-300, -300, W + 600, H + 600, ['#0F1430', '#1E2A5A', '#2E3C78'])
    from sets import starField
    starField(t, 21, 60, 0, 0, W, H, r=2.4)


def s12(t, lt, dur):
    cam(t, 960, 520, 1.0)
    iceStage(t, 0, 0)
    thump = hitK(t, 66, .14)
    r = 230 * (1 + .04 * thump)
    crack = landK(t, 67, .1)
    hy_ = 430 - 26 * thump
    iceHeart(960, hy_, r, cracks=.15 * crack, glowK=.35 * crack, key='s12ih', t=t)
    if crack > 0:
        zz = [[960, hy_ - r * .62], [940, hy_ - r * .42], [985, hy_ - r * .25], [950, hy_ - r * .05], [975, hy_ + r * .12]]
        n = 2 + int(3 * crack)
        inkLine(zz[:n], 3.0, '#FF6F96', 'ink', 0)
        inkLine(zz[:n], 1.2, INK, 'inkfine', 0)
    flat_ = t >= B[65] - .04
    ecgTrace(360, 720, 1200, 120, t, 'flat' if flat_ else 'beat', [B[64] - .3], col='#7CF29A', sw=4)
    if flat_ and t < B[66]:
        stamp('哔——', 960, 860, 60, '#7CF29A', bage(t, 65), rot=0, stroke=INK)
    if t >= B[66] - .04 and t < B[67]:
        stamp('跳？', 1300, 220, 64, '#FFFFFF', bage(t, 66), rot=.12)
    if crack > 0:
        glow(960, 430, 160, '#FF8FB0', .6 * crack)
    camEnd()


PICS = []


def _pic1(px, py, pw, ph):
    flatRect(px, py, pw, ph, '#FFE9C8')
    her(px + pw / 2, py + ph * .95, pw / 14, dict(view='front', eyes='happy', mouth='laugh', blush=.6, boilKey='p1', noShadow=True, aL=.8, aR=.8))


def _pic2(px, py, pw, ph):
    flatRect(px, py, pw, ph, '#D8F0FF')
    o = dict(view='q', flip=True, eyes='closed', mouth='cat', blush=.5, boilKey='p2', noShadow=True, aL=1.0, aR=.2)
    her(px + pw * .55, py + ph * .95, pw / 14, o)
    cup(px + pw * .28, py + ph * .55, pw / 260, fill=1, key='p2c', saucer=False)


def _pic3(px, py, pw, ph):
    flatRect(px, py, pw, ph, '#FFF1DA')
    paint(rectPts(px + pw * .32, py + ph * .45, pw * .36, ph * .4), wash=WOOD, ink=INK, sw=.5)
    awning(px + pw * .26, px + pw * .74, py + ph * .3, 18, key='p3aw', cols=('#C8643C', '#FFF5E2'))
    him(px + pw * .2, py + ph * .95, pw / 18, dict(view='q', eyes='happy', mouth='smile', boilKey='p3m', noShadow=True))
    her(px + pw * .8, py + ph * .95, pw / 18, dict(view='q', flip=True, eyes='happy', mouth='smile', boilKey='p3h', noShadow=True))


def _pic4(px, py, pw, ph):
    flatRect(px, py, pw, ph, '#FFE0EA')
    flowerAt(px + pw / 2, py + ph / 2, pw * .18, 1.0, 1.2)


PICS = [_pic1, _pic2, _pic3, _pic4]
PIC_POS = [(380, 300, -.12), (1540, 300, .1), (420, 760, .08), (1500, 760, -.08)]


def s13(t, lt, dur):
    cam(t, 960, 520, 1.0)
    iceStage(t, 0, 0)
    n = lastBeat(t, [68, 69, 70, 71]) + 1
    gk = .35 + .15 * n
    ecgTrace(360, 720, 1200, 120, t, 'flat', (), col='#7CF29A', sw=4, a=1 - seg(t, B[68], B[69]))
    iceHeart(960, 430, 230, cracks=.15 + .1 * n, glowK=gk, key='s12ih', t=t)
    for i in range(n):
        k = backOut(clamp((t - (B[68 + i] - .045)) / .16))
        x, y, r = PIC_POS[i]
        push()
        translate(lerp(960, x, k), lerp(430, y, k))
        scale(k)
        polaroidW(0, 0, 250, r, key=f's13p{i}', draw=PICS[i])
        pop()
        if 0 <= t - B[68 + i] < .3:
            G.c.drawLine(960, 430, x, y, skia.Paint(AntiAlias=True, Color=skcol('#FF8FB0', .6 * (1 - (t - B[68 + i]) / .3)), StrokeWidth=6))
    camEnd()


def s14(t, lt, dur):
    zk = ease(seg(t, B[72], B[75]))
    z = lerp(1.0, 1.2, zk)
    cam(t, 960, 430, z)
    iceStage(t, 0, 0)
    for i in range(4):
        x, y, r = PIC_POS[i]
        if i >= 2:
            y = lerp(y, 620, zk)
        polaroidW(x, y, 250, r, key=f's13p{i}', draw=PICS[i])
    cr = .55 + .15 * lastBeat(t, [72, 73, 74]) + .1
    gk = .95 + .4 * landK(t, 74, .12)
    shake = shakeXY(t, 6 * landK(t, 74, .1)) if t < B[75] - .04 else (0, 0)
    iceHeart(960 + shake[0], 430 + shake[1], 230, cracks=cr, glowK=gk, key='s12ih', t=t)
    if t >= B[73] - .04:
        for i in range(6):
            a = i / 6 * TAU + .4
            k = landK(t, 73, .12)
            px, py = 960 + math.cos(a) * 170, 430 + math.sin(a) * 150
            paint([[px, py], [px + 30 * math.cos(a + .5) * k, py + 30 * math.sin(a + .5) * k - 10 * k], [px + 24 * math.cos(a - .4), py + 24 * math.sin(a - .4)]],
                  wash='#DDF2FB', ink=INK, sw=.5)
    if t >= B[75] - .04:
        glow(960, 430, 380, '#FFFFFF', .5)
        stamp('…', 960, 150, 90, '#FFFFFF', bage(t, 75), rot=0)
    camEnd()


from story2 import *
from story3 import *

SHOTS = []
_FN = {f'S{i:02d}': globals()[f's{i:02d}'] for i in range(1, 39)}
for s in SB['shots']:
    SHOTS.append((s['start'], _FN[s['id']], s['tr'], s['id']))
