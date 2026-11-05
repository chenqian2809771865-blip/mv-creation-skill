# story_c.py: S17–S24 — Rolling in the Deep chorus: tailing him to 老地方, melodrama, the deep sea, the binoculars, the pounce.
import math
from eng import *
from clawd import *
from props import *
from props_chuanshao import *
from props3 import *
from sm import nightPark
from common import *


# ===================================================================== S17 tailing him down the shop street
HIDES = [('bush', 260), ('mail', 560), ('lamp', 860), ('trash', 1130)]


def s17(t, lt, dur):
    BB = beatsOf(17)
    n = nOn(t, BB)
    cam(t, 960, 470, 1.12)
    streetTall2(t, key='st7', rainK=0)
    gy = 668
    hx = lerp(1400, 1720, lt / dur)
    mv = move('walk', t)
    him(hx, gy, 26, fo(feel('happy', t), view='q', walk=mv['walk'], dy=mv['dy'], aR=1.2, armR=giftHook(1, 'g17'), aL=.3, emote='music'))
    j = max(0, n - 1)
    kind, sx = HIDES[j]
    tb = BB[j]
    rise = ease(seg(t, tb - .1, tb)) if n else 0
    nxt = BB[j + 1] if j < 3 else BB[3] + 2
    rise *= 1 - ease(seg(t, nxt - .18, nxt - .08))
    u = 24
    if kind == 'lamp':
        her(sx - 10, gy, u, fo(feel('suspicious', t), view='q', aR=1.1, armR=magnifierHook(1), sx=lerp(.4, 1, rise), sy=lerp(.4, 1, rise)), detective=True)
        streetLamp(sx + 40, gy + 6, 40, 1, key='lamp17')
    elif kind == 'mail':
        her(sx + lerp(0, 80, rise), gy, u, fo(feel('suspicious', t), view='q', aR=1.1, armR=magnifierHook(1), rot=-.25 * rise), detective=True)
        mailbox(sx, gy + 6, 66, key='mb17')
    else:
        hid = {'bush': 4.6, 'trash': 4.9}[kind]
        her(sx, gy + hid * u * (1 - rise), u, fo(feel('suspicious', t), view='q', aR=1.2, armR=magnifierHook(1), noShadow=True), detective=True)
        if kind == 'bush':
            bush(sx, gy + 6, 60, key='bu17')
        else:
            trashcan(sx, gy + 6, 54, key='tc17')
    if kind != 'bush':
        bush(260, gy + 6, 60, key='bu17')
    if kind != 'mail':
        mailbox(560, gy + 6, 66, key='mb17')
    if kind != 'lamp':
        streetLamp(900, gy + 6, 40, 1, key='lamp17')
    if kind != 'trash':
        trashcan(1130, gy + 6, 54, key='tc17')
    if rise > .5:
        emote('!?' if j == 3 else '?', sx + 70, gy - 260, 24, pk(t, tb, .14), t - tb)
    camEnd()


# ===================================================================== S18 the foot of the 老地方 path
def s18(t, lt, dur):
    BB = beatsOf(18)
    n = nOn(t, BB)
    cam(t, 960, 540, 1.0)
    nightPark(t, key='np18', horizon=700)
    # stone steps up the hill on the right, lamp, bench, a tree on the left
    boilSeed('steps18')
    for k in range(6):
        y = 860 - k * 40
        paint(rectPts(1500 + k * 40, y - 22, 300 - k * 30, 22), wash='#8A86A8', ink=INK, sw=.6, lite=True)
    streetLamp(1820, 880, 46, 1.0, key='lmp18')
    peek = .6 + .4 * math.sin(t * 3)
    her(300 + 95 + 30 * peek, 880, 28, fo(feel('suspicious', t), view='q', aR=1.2, armR=magnifierHook(1)), detective=True)
    tree(300, 860, 70, key='tr18', col='#4E8A5A')    # drawn over her: she hides behind the trunk
    sign(1130, 870, '老地方 ↗', 1.0, key='sg18')
    fairyLights(t, 1040, 1260, 618, 16, 6, key='sgl18', a=.8)
    u = 30
    if n < 4:
        lx = [0, 0, -1.0, 1.0][n]
        him(1360, 880, u, fo(feel('nervous' if n >= 2 else 'neutral', t), view='q', flip=(n == 2), lookX=lx, aR=1.2, armR=giftHook(1, 'g18'),
                             aL=.3, dy=take(t, BB[0], .6)['dy'] if n == 1 else 0))
    else:
        a = t - BB[3]
        k = clamp((a + .04) / .14)
        him(lerp(1360, 1600, k), 880 - 60 * math.sin(k * math.pi) + 60 * k * k, u, fo(feel('excited', t), view='q', rot=.6 * k, smear=.6 * (1 - k), smearDir=1,
                                                                              aR=1.2, armR=giftHook(1, 'g18')))
    bush(1620, 900, 96, key='bu18')
    if n >= 4:
        a = t - BB[3]
        if a < .4:
            for i in range(8):
                ang = -math.pi / 2 + (i - 3.5) * .3
                mapleLeaf(1620 + math.cos(ang) * 600 * a, 760 + math.sin(ang) * 480 * a, 16, rot=a * 10 + i, col='#86C96E', key=f'lf18{i}')
        stamp('嗖！', 1640, 520, 96, '#FFE36E', a, rot=.12)
    camEnd()


# ===================================================================== S19 ...all: the melodrama theatre
def s19(t, lt, dur):
    BB = beatsOf(19)
    n = nOn(t, BB)
    cam(t, 960, 560, 1.04 + .04 * lt, rot=.02 * math.sin(t * 2.5))
    theatre(t, 1.0, '苦情剧场', floor='#4A3A5A')
    spotBeam(960, -60, 930, 160, 640, '#E6DCFF', .22)
    for i in range(7):
        ang = t * 1.6 + i / 7 * TAU
        yiyun(960 + math.cos(ang) * 600, 500 + math.sin(ang) * 240, 50, t, 70 + i, 1, mood='sad')
    her(960, 920, 46, fo(feel('cry', t), view='front', sq=.22, aL=1.3, aR=1.3), detective=True)
    rainFX(t, 19, 70, 300, -60, 1620, 960, a=.35)
    petalsFly(t, 19, 14, 500, -60, 1420, 900, 12, cols=['#E8476E', '#C8324A'])
    for i in range(n):
        a = t - BB[i]
        if -.04 <= a < .22:
            x = [520, 1420, 760, 1200][i]
            lightning(x, -40, x + [120, -160, 60, -60][i], 520, key=f'lt19{i}', w=4)
            if a < .045:
                flash(.16)
    if n:
        stamp('呜哇——', 960, 380, 110, '#C9B8EC', t - BB[0], rot=-.06)
    camEnd()


# ===================================================================== S20 stamping his file
def himPhoto(cx, cy, w, h):
    gradRect(cx - w / 2, cy - h / 2, w, h, ['#BFE3F5', '#E9F6FC'])
    flat([[cx - w / 2, cy + h * .25], [cx + w / 2, cy + h * .25], [cx + w / 2, cy + h / 2], [cx - w / 2, cy + h / 2]], '#9ED27A')
    him(cx, cy + h * .42, w / 13, dict(view='front', eyes='happy', mouth='smile', aL=1.3, aR=.2, noShadow=True))


def dossier(t):
    flatRect(-200, -200, W + 400, H + 400, '#6E4A34')
    for i in range(9):
        boilSeed(f'dk{i}')
        inkLine([[-200, i * 130], [W + 200, i * 130 + jit(4)]], .7, '#5A3826', 'inkfine', .1)
    # the open kraft folder
    boilSeed('folder')
    paint([[120, 90], [1800, 70], [1820, 1010], [100, 1030]], wash='#D9B07A', fill='#B98A50', fillOp=50, ink=INK, sw=1.0)
    inkLine([[960, 80], [962, 1020]], 1.0, '#8A6A3E', 'ink', .1)
    paint([[180, 40], [520, 36], [540, 96], [170, 100]], wash='#D9B07A', ink=INK, sw=.8)
    text('调查档案 No.520', 360, 66, 30, '#6A4A3A', face=WENKAI, shadow=False)
    # right page: notes, sticky notes, a doodle, a coffee ring
    fakeText(1020, 160, 700, 26, 70, 7, a=.55)
    stickyNote(1600, 640, 70, .12, '#FFE36E', '23:47', key='sn20a')
    stickyNote(1180, 760, 64, -.1, '#F7C6D2', '老地方', key='sn20b')
    pencilDoodle('heart', 1450, 840, 40, .55, '#C0637B')
    coffeeRing(1600, 900, 80, .32)
    pencil(1720, 420, 1.9, 300, key='pc20')
    # ink pad and eraser crumbs
    boilSeed('pad')
    paint(rrPts(1050, 860, 200, 120, 16), wash='#3A3550', ink=INK, sw=.9)
    paint(rrPts(1064, 874, 172, 92, 12), wash='#C8324A', ink=None)
    for i in range(8):
        G.c.drawCircle(1350 + hash1(i * 3) * 120, 560 + hash1(i * 5) * 60, 4, skia.Paint(AntiAlias=True, Color=skcol('#F59BB0')))


def s20(t, lt, dur):
    BB = beatsOf(20)
    n = nOn(t, BB)
    cam(t, 960, 540, 1.0)
    dossier(t)
    polaroid(560, 520, 540, -.04, 1, himPhoto, key='hp20')
    boilSeed('clip20')
    inkLine([[480, 200], [480, 150], [530, 150], [530, 230]], 2.4, '#B9C2CC', 'ink', .3)
    marks = [('嫌疑', 360, 320, 74, INK, -.2), ('可疑', 770, 330, 74, INK, .18), ('非常可疑', 420, 760, 66, INK, .12), ('有罪！', 560, 520, 150, C['red'], -.12)]
    for i in range(n):
        txt, x, y, s, col, r = marks[i]
        rubberStamp(txt, x, y, s, t - BB[i], col=col, rot=r)
        if 0 <= t - BB[i] < .2:
            impactLines(x, y, 130, 230, 12, t, INK, key=f'i20{i}', sw=1.2)
    j = max(0, n - 1)
    if n == 0:
        tx, ty, lift = marks[0][1], marks[0][2], 160 * (1 - ease(seg(t, BB[0] - .2, BB[0] - .04)))
    elif n < 4:
        k = ease(seg(t, BB[j] + .08, BB[j + 1] - .04))
        tx, ty = lerp(marks[j][1], marks[j + 1][1], k), lerp(marks[j][2], marks[j + 1][2], k)
        lift = 160 * math.sin(k * math.pi) if k < .5 else 160 * (1 - ease(seg(t, BB[j + 1] - .2, BB[j + 1] - .04)))
    else:
        e = ease(seg(t, BB[3] + .03, BB[3] + .2))
        tx, ty = marks[3][1] + 300 * e, marks[3][2]
        lift = 220 * e
    boilSeed('stamper')
    sx_, sy_ = tx + 30, ty - 60 - lift
    paint(rrPts(sx_ - 70, sy_ - 20, 140, 60, 14), wash='#7A4E33', ink=INK, sw=1.2)
    paint(rrPts(sx_ - 26, sy_ - 130, 52, 115, 20), wash='#9B6B45', ink=INK, sw=1.1)
    paint(ellPts(sx_, sy_ - 140, 42, 34, 16), wash='#C0637B', ink=INK, sw=1)
    her(1700, 1050, 48, fo(feel('angry', t), view='q', flip=True, noShadow=True), detective=True)
    camEnd()


# ===================================================================== S21 Rolling in the deep: splash and sink
def s21(t, lt, dur):
    BB = beatsOf(21)
    n = nOn(t, BB)
    seaBed(t, .25 + .35 * clamp(lt / dur), floorY=910)
    cam(t, 960, 540, 1.0)
    for i, (x, col) in enumerate([(160, '#F59A6B'), (420, '#E8476E'), (1500, '#9C8FE0'), (1780, '#F7C65C')]):
        coral(x, 930, 46 + 10 * (i % 2), col, key=f'cor21{i}')
    for i in range(5):
        seaweed(260 + i * 380, 1100, 240 + 60 * (i % 2), t, key=f'sw21{i}')
    chest(1240, 960, 40, key='ch21')
    jelly(300 + 30 * math.sin(t), 300, 50, t, key='jf21a')
    jelly(1650, 420 + 20 * math.sin(t * 1.3), 40, t, col='#C9B8EC', key='jf21b')
    d = 1 if n < 3 else -1
    for i in range(8):
        fx = 1300 + (i % 4) * 70 + (lt * 60 * d) + (0 if d > 0 else -200)
        fish(fx, 260 + (i // 4) * 60 + (i % 2) * 20, 22, d, key=f'f21{i}')
    a = t - BB[0]
    y = lerp(-120, 300, easeOut(clamp((a + .04) / .2)))
    if n >= 2:
        y = lerp(300, 820, ease(seg(t, BB[1], BB[3])))
    rot = t * 5 if n < 4 else (BB[3] * 5)
    sq = .2 * math.exp(-(t - BB[3]) * 8) * math.cos((t - BB[3]) * 28) if n >= 4 else 0
    push()
    translate(960, y - 3 * 30)
    rotate(rot)
    her(0, 3 * 30, 30, fo(feel('cry', t), view='front', aL=1.4, aR=1.4, noShadow=True, sq=.12 + sq), detective=True)
    pop()
    if -.04 <= a < .45:
        for i in range(14):
            ang = -math.pi / 2 + (i - 6.5) * .22
            r = 60 + 420 * easeOut(clamp((a + .04) / .45))
            bubble1(960 + math.cos(ang) * r, 120 + math.sin(ang) * r * .4 + 80, 16 + 8 * hash1(i), 1 - clamp(a / .45))
        stamp('扑通！', 1350, 200, 110, '#FFFFFF', a, rot=.12, life=.55)
    bubbles(t, 21, 18, 880, 0, 1040, y, 10, .9)
    if n >= 4:
        a4 = t - BB[3]
        if a4 < .45:
            for i in range(8):
                puff(960 + (i - 3.5) * 40 * (1 + a4 * 4), 910 - a4 * 60, 12, col='#D9C49A', key=f'sand{i}', ink=False, a=1 - a4 / .45)
    camEnd()


# ===================================================================== S22 tears float up as bubbles; a crab pats her
def s22(t, lt, dur):
    BB = beatsOf(22)
    n = nOn(t, BB)
    seaBed(t, .75, floorY=880)
    cam(t, 960, 560, 1.05)
    for i in range(6):
        seaweed(120 + i * 340, 1000, 300 + 80 * (i % 3), t, key=f'sw22{i}', col='#2E7A62')
    for i, (x, col) in enumerate([(220, '#C8564F'), (1720, '#9C8FE0')]):
        coral(x, 900, 60, col, key=f'cor22{i}')
    starfish(560, 960, 34, .4, key='sf22')
    shell(1280, 960, 30, key='shl22')
    lit = .55 + .45 * math.exp(-(t - BB[n - 1]) * 5) if n >= 2 else 0
    anglerfish(1480, 480, 80, lit, key='af22')
    her(900, 900, 40, fo(feel('cry', t), view='front', aL=-.9, aR=-.9, tint='blue', tintK=.3, sq=.15), detective=True)
    pat = 0
    if n >= 3:
        pat = abs(math.sin((t - BB[2]) * 14)) * math.exp(-(t - BB[2]) * 2)
    crab(1180, 930, 46, t, pat, key='crab22')
    if n >= 3 and t - BB[2] < .5:
        stamp('拍拍', 1240, 760, 56, '#FFFFFF', t - BB[2], rot=.1, life=.5)
    for i in range(n):
        a = t - BB[i]
        for side in (-1, 1):
            if i == 3:
                kb = easeOut(clamp((a + .04) / .16))
                for m in range(5):
                    ang = -math.pi / 2 + side * (.35 + .28 * m)
                    r = 60 + 170 * kb + 60 * m * kb
                    bubble1(900 + math.cos(ang) * r + math.sin(a * 6 + m) * 12, 900 - 250 + math.sin(ang) * r * .8 - max(0, a) * 380, (14 + 5 * m) * (.5 + .5 * kb))
            else:
                bubble1(900 + side * 70 + math.sin(a * 5 + i) * 20, 900 - 230 - max(0, a) * 380, 20 + 6 * i)
    bubbles(t, 22, 10, 0, 0, W, 900, 8, .4)
    camEnd()


# ===================================================================== S23 binocular POV: a glowing red thing in his hand at 老地方
HX23 = 820


def hill23(t, gk):
    oldPlace(t, 1.0, decor=1.0, bench=True, key='op23')
    picnic(1060, 900, 520, 130, key='pic23')
    basket(1180, 860, 40, key='bsk23', apples=0)
    o = fo(feel('happy', t), view='q', aR=.9, aL=.9, tint='blue', tintK=.35)
    y = oldGround(HX23)
    hx, hy = handXY(HX23, y, 24, o, 'R')
    him(HX23, y, 24, o)
    glow(hx + 30, hy, 160, '#FF4A5A', gk)
    boilSeed('heart23')
    paint(heartPts(hx + 30, hy, 34, 22), wash='#E8476E', ink=INK, sw=.8)
    return hx + 30, hy


def s23(t, lt, dur):
    BB = beatsOf(23)
    n = nOn(t, BB)
    z = steps(t, BB, [1.2, 1.45, 1.75, 2.05, 2.4])
    gk = .6 + (.8 * math.exp(-(t - BB[3]) * 5) if n >= 4 else 0)
    hx, hy = 880, 640
    camBegin(hx, hy, z * (1 + bump(t)), .01 * math.sin(t * 7))
    hill23(t, gk)
    camEnd()
    binoMask(960, 560, 420, 300)
    if n >= 4:
        stamp('心！？', 1600, 200, 90, '#FF7D9C', t - BB[3], rot=.14)


# ===================================================================== S24 the pounce at 老地方
def s24(t, lt, dur):
    BB = beatsOf(24)
    n = nOn(t, BB)
    cam(t, 960, 560, 1.0)
    oldPlace(t, 1.0, decor=1.0, bench=False, signX=1700, key='op23')
    picnic(1520, 930, 520, 130, key='pic24')
    basket(1600, 890, 40, key='bsk24', apples=0)
    u = 30
    hxp = 1240
    gy = oldGround(hxp)
    if n >= 4:
        impactLines(860, 620, 140, 300, 14, t, '#FFF5E2', key='imp24', sw=1.4)
    if n < 4:
        him(hxp, gy, u, fo(feel('happy', t), view='qback', aL=.8, aR=.8, emote='music'))
    else:
        tr = turn(t, BB[3] - .1, BB[3] + .02, .375, .875 + 1)
        him(hxp, gy, u, fo(feel('surprised', t), view=tr['view'], flip=not tr['flip'], smear=tr['smear'], aL=.2, aR=-.4,
                           emote='!', emoteK=pk(t, BB[3], .12), emoteAge=t - BB[3]))
    x0, x1 = 360, 860
    if t < BB[0]:
        x, y, sq, rot = x0, oldGround(x0), .15 * ease(seg(t, BB[0] - .2, BB[0])), 0
    elif t < BB[3]:
        k = (t - BB[0]) / (BB[3] - BB[0])
        kk = k * .8 + .2 * ease(k)
        x = lerp(x0, x1, kk)
        y = lerp(oldGround(x0), oldGround(x1), kk) - 420 * 4 * kk * (1 - kk)
        sq, rot = -.1, -.25 + .5 * kk
    else:
        a = t - BB[3]
        x, y, sq, rot = x1, oldGround(x1), .25 * math.exp(-a * 8) * math.cos(a * 25), 0
    her(x, y, u, fo(feel('determined', t), view='q', aR=1.5, aL=1.5, sq=sq, rot=rot, smear=.5 if BB[0] < t < BB[0] + .25 else 0, smearDir=1), detective=True)
    bush(360, oldGround(360) + 30, 96, key='bu24')
    if n >= 1 and t - BB[0] < .35:
        a = t - BB[0]
        for i in range(8):
            mapleLeaf(360 + (i - 3.5) * 40 * (1 + a * 5), 760 - a * 300 + (i % 2) * 30, 16, rot=a * 9 + i, col='#86C96E', key=f'lf24{i}')
    if n >= 4:
        stamp('抓到你了！', 760, 300, 110, '#FFE36E', t - BB[3], rot=-.08)
    camEnd()
