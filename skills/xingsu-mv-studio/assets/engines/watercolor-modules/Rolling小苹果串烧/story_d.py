# story_d.py: S25–S32 — 小苹果 chorus: the reveal at 老地方, the clouds turn pink, the dance, the hat goes, an apple tree grows.
import math
from eng import *
from clawd import *
from props import *
from props_chuanshao import *
from props3 import *
from props_zuitian import bunting, balloon
from common import *


# ===================================================================== S25 the reveal: a big red apple at 老地方
def s25(t, lt, dur):
    BB = beatsOf(25)
    n = nOn(t, BB)
    cam(t, 960, 560, 1.04 - .02 * lt)
    oldPlace(t, 1.0, decor=1.0, bench=False, signX=1720, key='op23')
    picnic(1500, 960, 560, 140, key='pic25')
    basket(1600, 920, 44, key='bsk25', apples=4)
    lantern(1800, 930, 22, t, 1.0, '#FFD45C', key='ln25')
    u = 34
    hx, gy = 1290, oldGround(1290)
    sh = 1 if n >= 1 else 0
    o = fo(feel('happy' if n < 2 else 'love', t), view='q', flip=True, aR=.9, aL=-.3)
    ax, ay = handXY(hx, gy, u, o, 'R')
    him(hx, gy, u, o)
    hx2 = 1240 - 14.5 * u
    gy2 = oldGround(hx2)
    emo = 'surprised' if n < 4 else 'love'
    o2 = fo(feel(emo, t), view='q', aR=.3, aL=1.2 if n < 3 else -.3, emote=None if n < 4 else 'hearts')
    if n < 3:
        o2['armL'] = magnifierHook(1.0)
    her(hx2, gy2, u, o2, detective=True)
    if n >= 3:
        a = t - BB[2]
        mx, my = handXY(hx2, gy2, u, fo(o2, aL=1.2), 'L')
        x = lerp(mx - 40, mx - 160, clamp(a / .5))
        aa = max(0, a)
        aland = (250 + math.sqrt(250 ** 2 + 4 * 2400 * max(0, gy2 - 30 - my))) / 4800
        y = min(gy2 - 30, my + 2400 * aa ** 2 - 250 * aa)
        push()
        translate(x, y)
        rotate(6 * min(aa, aland))
        magnifierHook(1.0)(u, 1.4)
        pop()
        if a < .3:
            stamp('啪嗒', x + 40, gy2 - 120, 56, '#FFFFFF', a, rot=-.1, life=.4)
    if n >= 2:
        a = t - BB[1]
        for i in range(7):
            ang = -math.pi / 2 + (i - 3) * .42
            r = 90 + 300 * easeOut(clamp(a / .5))
            boilSeed(f'h25{i}')
            paint(heartPts(ax - 60 + math.cos(ang) * r, ay - 120 + math.sin(ang) * r * .6, 22 * (1 - .4 * clamp(a / .8)), 18), wash=C['heart'], ink=INK, sw=.6)
    # the gift: drawn above her so her hat brim / arm never cover it; it lights up on beat 1
    if n >= 1:
        glow(ax - 60, ay - 20, 230, '#FFE8A0', .55 * (.7 + .3 * pulse(t, 6)))
    apple(ax - 60, ay - 20, 70, key='ap25', shine=sh * (.6 + .4 * pulse(t, 6)), bow=True)
    if n >= 1:
        a = pk(t, BB[0], .16)
        push()
        translate(ax + 40, ay - 230)
        rotate(-.08)
        scale(backOut(a))
        boilSeed('tag25')
        inkLine([[-60, 36], [-100, 130]], 1.0, INK, 'inkfine', 0)
        paint(rrPts(-150, -36, 300, 72, 18), wash='#FFFDF6', ink=INK, sw=1)
        text('给我的小苹果', 0, 0, 40, C['red'], shadow=False)
        pop()
    camEnd()


# ===================================================================== S26 her blush rises, the suspicion cloud pops (half-body, warm bokeh)
def bokeh(t, seed=26):
    gradRect(-200, -200, W + 400, H + 400, ['#2A2D6E', '#5A3A7E'])
    for i in range(36):
        x = hash1(seed + i * 3.1) * W
        y = hash1(seed + i * 5.7) * H
        r = 40 + 70 * hash1(i * 2.3)
        col = ['#FFD27A', '#F59BB0', '#FFF1C2', '#C9B8EC'][i % 4]
        a = .18 + .12 * math.sin(t * 1.5 + i)
        G.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=skcol(col, a)))
        glow(x, y, r * 1.4, col, .25)


def s26(t, lt, dur):
    BB = beatsOf(26)
    n = nOn(t, BB)
    bokeh(t)
    cam(t, 900, 560, 1.0)
    floatHearts(t, 26, 8, 100, 100, 1820, 900, 15)
    bl = [.2, .45, .7, .95, 1.0][n]
    u = 60
    o = fo(feel('shy' if n < 4 else 'love', t), view='front', blush=bl, tint='rosy', tintK=.22 * n, aL=1.0, aR=1.0)
    ax, ay = handXY(800, 1060, u, o, 'R')
    her(800, 1060, u, o, detective=True)
    apple(ax + 30, ay - 20, 70, key='ap26', shine=.5)
    him(1700, 1060, 54, fo(feel('happy', t), view='q', flip=True))
    if n < 4:
        sx = shake(t, BB[2], 12, .5)[0] if n >= 3 else 0
        yiyun(800 + sx, 190, 70, t, 26, 1)
        if n >= 3:
            emote('sweat', 900, 150, 26, 1, t - BB[2])
    else:
        a = t - BB[3]
        if a < .35:
            paint(starPts(800, 190, 120 * backOut(clamp(a / .15)), .4, 6), wash='#FFE36E', ink=INK, sw=1)
            impactLines(800, 190, 120, 260, 12, t, '#FFFFFF', key='imp26', sw=1.2)
        sparkles(t, 26, 10, 580, 80, 1030, 330, 20, '#FFFFFF')
        stamp('啵！', 1100, 180, 96, '#FFFFFF', a, rot=.1, stroke=C['heart'])
    camEnd()


# ===================================================================== S27 the suspicion clouds turn into pink clouds over 老地方
CL27 = [(830, 190), (1080, 110), (1330, 200), (1590, 120)]
HEART27 = [(930, 215), (1190, 215), (835, 410), (1285, 410)]   # two top lobes + two flanks around the heart


def s27(t, lt, dur):
    BB = beatsOf(27)
    n = nOn(t, BB)
    cam(t, 960, 540, 1.0)
    st = oldPlace(t, 0.0, decor=0.0, bench=True, signX=1290, key='op27')
    seat(him, 1640 - 5.6 * 15, st, 15, fo(feel('happy', t), view='front', lookY=-1, aL=.2, aR=.2, dy=0))
    seat(her, 1640 + 5.6 * 15, st, 15, fo(feel('happy', t), view='front', lookY=-1, aL=.2, aR=.2, dy=0, hat='deer'))
    for i, (bx, col) in enumerate([(1500, '#F28FB0'), (1560, '#7DD3C8'), (1530, '#F7C65C')]):
        balloon(bx + i * 20, 520 - i * 40, 22, col, t, key=f'bl27{i}')
    mg = ease(seg(t, BB[3] - .04, BB[3] + .25)) if n >= 4 else 0
    for i, (x, y) in enumerate(CL27):
        if i < n:
            a = t - BB[i]
            tx, ty = HEART27[i]
            xx, yy = lerp(x, tx, mg), lerp(y, ty, mg)
            k = backOut(clamp((a + .04) / .14))
            puff(xx, yy, 46 * (1 + .25 * (1 - k)), col='#FBD0DA', key=f'pc{i}')
            for sgn in (-1, 1):
                inkLine([[xx + sgn * 30 - 12, yy + 4], [xx + sgn * 30, yy - 6], [xx + sgn * 30 + 12, yy + 4]], 1.2, INK, 'ink', .4)
            paint(ellPts(xx - 50, yy + 14, 12, 7, 8), wash='#F19AB0', ink=None)
            paint(ellPts(xx + 50, yy + 14, 12, 7, 8), wash='#F19AB0', ink=None)
            if a < .3:
                sparkles(t, 27 + i, 6, xx - 120, yy - 80, xx + 120, yy + 60, 16, '#FFFFFF')
        else:
            yiyun(x, y, 56, t, 80 + i, 1)
    if n >= 4:
        a = t - BB[3]
        glow(1060, 330, 260, '#FFD0DC', .6)
        boilSeed('bigheart27')
        paint(heartPts(1060, 330, 105 * backOut(clamp((a + .04) / .16)), 30), wash=C['heart'], ink=INK, sw=1.2)
        if a < .3:
            sparkles(t, 270, 8, 900, 180, 1220, 460, 18, '#FFFFFF')
    camEnd()


# ===================================================================== S28 the 小苹果 dance, the pink clouds cheer
def s28(t, lt, dur):
    BB = beatsOf(28)
    n = nOn(t, BB)
    flatRect(-80, -80, W + 160, H + 160, '#3A2250')
    for i, (x, col) in enumerate([(480, '#FF8FB1'), (960, '#FFE07A'), (1440, '#FF8A8A')]):
        glow(x, 420, 520, col, .5)
    cam(t, 960, 560, 1.0)
    bunting(-60, 980, 60, 60, 9, t, key='bt28a')
    bunting(940, 1980, 60, 60, 9, t, key='bt28b')
    k = beatIdx(t)
    for i in range(6):
        on = 1 if (k + i) % 2 == 0 else .25
        appleLight(260 + i * 280, 170, 40, on, key=f'al{i}')
    # light-up dance floor
    for r in range(3):
        for c in range(12):
            x0, y0 = -80 + c * 170 + r * 20, 800 + r * 60
            on = (c + r + k) % 3 == 0
            col = ['#FF8FB1', '#FFE07A', '#7DD3C8'][(c + r) % 3]
            flat([[x0, y0], [x0 + 166, y0], [x0 + 166 + 20, y0 + 56], [x0 + 20, y0 + 56]], col if on else '#5A3A6A', .9 if on else 1)
    inkLine([[-80, 800], [W + 80, 800]], 1.4, INK, 'ink', 0)
    side = 1 if n % 2 else -1
    tb = BB[max(0, n - 1)] if n else BB[0]
    tk = take(t, tb, .7) if n else dict(sq=0, dy=0)
    if n < 4:
        aL, aR = (1.6, -.4) if side > 0 else (-.4, 1.6)
        rot, emo = .12 * side, 'excited'
    else:
        aL, aR, rot, emo = 1.5, 1.5, 0, 'love'
    for who, x in (('him', 680), ('her', 1240)):
        o = fo(feel(emo, t), view='front', aL=aL, aR=aR, rot=rot, sq=tk['sq'], dy=tk['dy'] - 1.2 * abs(math.sin(bpOf(t) * math.pi)))
        if who == 'him':
            him(x, 860, 34, o)
        else:
            her(x, 860, 34, o, detective=True)
    # the audience: the clouds, now pink, with glowsticks
    for i in range(7):
        x = 120 + i * 280
        y = 1010 + 10 * math.sin(bpOf(t) * math.pi + i)
        yiyun(x, y, 56, t, 90 + i, 1, mood='happy', col='#FBD0DA')
        ang = -.6 + 1.2 * (1 if (k + i) % 2 else 0)
        inkLine([[x + 50, y - 20], [x + 50 + math.sin(ang) * 70, y - 20 - math.cos(ang) * 70]], 5, ['#7DFFC8', '#FFE36E', '#FF8FB1'][i % 3], 'ink', 0)
    if n >= 4:
        a = t - BB[3]
        boilSeed('h28')
        paint(heartPts(960, 400, 120 * backOut(clamp(a / .15)), 26), wash=C['heart'], ink=INK, sw=1.2)
        floatHearts(t, 28, 10, 500, 200, 1400, 700, 16)
    elif n:
        stamp(['左！', '右！', '左！'][n - 1], 960, 360, 90, '#FFE36E', t - tb, rot=.1 * side, life=.45)
    camEnd()


# ===================================================================== S29 flowers bloom across 老地方 in waves
def s29(t, lt, dur):
    BB = beatsOf(29)
    n = nOn(t, BB)
    cam(t, 960, 540, 1.0)
    oldPlace(t, 0.0, decor=0.0, bench=True, signX=1290, key='op27')
    for i in range(90):
        x = -40 + hash1(i * 3.3) * 2000
        y = oldGround(x) + 30 + hash1(i * 7.7) ** 1.2 * 280
        band = min(3, int((x + 40) / 500))
        if band < n:
            a = t - BB[band] - (x - band * 500) / 500 * .18
            k = clamp((a + .06) / .1)
            bloom(x, y, 20 + 10 * hash1(i), k, PETALS[i % 6], key=f'b29{i}', stem=False)
    u = 26
    him(700, oldGround(700) + 4, u, fo(feel('happy', t), view='q', aL=1.3))
    her(700 + 12.5 * u, oldGround(700 + 12.5 * u) + 4, u, fo(feel('excited', t), view='q', flip=True, aR=1.3), detective=True)
    if n >= 4:
        petalsFly(t, 29, 24, 0, -50, W, 900, 12)
    camEnd()


def flowerCarpet(t, seed=30):
    for i in range(70):
        x = -40 + hash1(i * 3.3 + seed) * 2000
        y = oldGround(x) + 30 + hash1(i * 7.7 + seed) ** 1.2 * 300
        bloom(x, y, 20 + 10 * hash1(i), 1, PETALS[i % 6], key=f'fc{seed}{i}', stem=False)


# ===================================================================== S30 she throws the detective hat away
def s30(t, lt, dur):
    BB = beatsOf(30)
    n = nOn(t, BB)
    cam(t, 960, 560, 1.05)
    oldPlace(t, 0.0, decor=0.0, bench=False, signX=1600, key='op27')
    flowerCarpet(t)
    u = 34
    thrown = n >= 1
    hx2 = 780
    o = fo(feel('laugh' if thrown else 'happy', t), view='q', aR=1.6 if (thrown and n < 3) else 0.0, aL=.3)
    her(hx2, oldGround(hx2), u, o, detective=not thrown)
    hx = hx2 + 12 * u
    him(hx, oldGround(hx), u, fo(feel('happy' if n < 3 else 'love', t), view='q', flip=True, aR=0.0 if n >= 3 else .4))
    if thrown:
        a = t - BB[0]
        p = arcPt([hx2, oldGround(hx2) - 10 * u], [1900, 80], 260, clamp((a + .04) / .9))
        push()
        translate(p[0], p[1])
        rotate(a * 8)
        translate(0, 9 * u)
        hat(u, 'deer', 1.4)
        pop()
        if a < .35:
            stamp('拜拜~', 1300, 300, 90, '#FFE36E', a, rot=.12, life=.9)
            sparkles(t, 30, 10, hx2 - 150, oldGround(hx2) - 12 * u, hx2 + 150, oldGround(hx2) - 7 * u, 18, '#FFFFFF')
    if n >= 3:
        boilSeed('hands30')
        paint(ellPts((hx2 + hx) / 2, oldGround(hx2) - 4.5 * u, .6 * u, .55 * u, 12), wash='#F2A283', ink=INK, sw=.8)
        floatHearts(t, 30, 6, hx2, 380, hx, 760, 16)
    if n >= 4:
        petalsFly(t, 30, 30, 0, -60, W, 900, 13)
    camEnd()


# ===================================================================== S31 planting by the 老地方 sign: dig, seed, water, sprout
MX = 980


def s31(t, lt, dur):
    BB = beatsOf(31)
    n = nOn(t, BB)
    cam(t, 1000, 560, 1.08)
    oldPlace(t, 0.0, decor=0.0, bench=True, signX=1620, key='op31', benchX=1800)
    flowerCarpet(t)
    gy = oldGround(MX)
    mound(MX, gy + 40, 60, key='md31')
    u = 32
    hx = MX - 11 * u
    oh = fo(feel('determined' if n < 3 else 'happy', t), view='q', aR=.2 if n < 3 else .5)
    him(hx, oldGround(hx), u, oh)
    # the shovel (world coordinates): handle from his front hand down to the blade in the dirt; lifts before beat 1, bites on it
    if n < 3:
        dig = math.sin(clamp((t - BB[0] + .3) / .45) * math.pi) if t > BB[0] - .3 else 0
        hxx, hyy = max((handXY(hx, oldGround(hx), u, oh, sd) for sd in ('L', 'R')), key=lambda p: p[0])
        bx, by = MX - 70, gy + 30 - 70 * dig
        ang = math.atan2(by - hyy, bx - hxx)
        boilSeed('shovel31')
        inkLine([[hxx - 30 * math.cos(ang), hyy - 30 * math.sin(ang)], [bx, by]], 3.0, '#9B6B45', 'ink', 0)
        push()
        translate(bx, by)
        rotate(ang - math.pi / 2)
        paint([[-28, 0], [28, 0], [32, 40], [0, 70], [-32, 40]], wash='#B9C2CC', ink=INK, sw=.8)
        pop()
    hx2 = MX + 11 * u
    her(hx2, oldGround(hx2), u, fo(feel('happy', t), view='q', flip=True, aR=1.2 if n == 2 else .4))
    if n >= 1:
        a = t - BB[0]
        if a < .35:
            for i in range(6):
                paint(ellPts(MX - 40 + i * 22, gy - 300 * a + 600 * a * a - i * 10, 10, 8, 8), wash='#7F5A3A', ink=None)
    if n >= 2:
        a = t - BB[1]
        if a < .35:
            boilSeed('seed')
            paint(ellPts(lerp(MX + 120, MX, clamp((a + .04) / .2)), lerp(gy - 120, gy + 20, clamp((a + .04) / .2)), 10, 14, 10), wash='#6B4A35', ink=INK, sw=.6)
    if n >= 3:
        pour = ease(seg(t, BB[2] - .12, BB[2] + .05))
        sx, sy = wateringCan(MX - 150, gy - 160, 34, pour=pour, facing=1, key='wc31')
        if t > BB[2] - .04:
            waterStream(t, sx, sy, MX, gy + 10, 1.0, key='ws31')
    if n >= 4:
        sprout(MX, gy + 20, 40, clamp((t - BB[3] + .04) / .16), key='spr31')
        stamp('发芽！', MX + 160, 430, 90, '#86C96E', t - BB[3], rot=.1)
    camEnd()


# ===================================================================== S32 the apple tree grows; the hat hangs on a branch; the phone; title; heart iris
def s32(t, lt, dur):
    BB = beatsOf(32)
    n = nOn(t, BB)
    cam(t, 1000, 560, 1.06 - .03 * clamp(lt / dur))
    gradRect(-500, -500, W + 1000, 1400, ['#FFC9A0', '#FFE8C8', '#FFF4E0'])
    glow(1000, 480, 700, '#FFE2A8', .7)
    st = oldPlace(t, 0.0, decor=0.0, bench=True, signX=1620, key='op31', sky=False, benchX=1800)
    flowerCarpet(t)
    gy = oldGround(MX)
    g = steps(t, BB, [.08, .4, .72, 1.0, 1.0])
    bl = ease(seg(t, BB[2] - .09, BB[2] + .03)) if t > BB[2] - .09 else 0
    ages = [t - BB[3] + .06 - i * .025 for i in range(7)] if t > BB[3] - .06 else None
    appleTree(MX, gy + 30, 64, g, 7 if ages else 0, t, key='at32', blossom=bl * (1 if n < 4 else .5), ages=ages)
    # the deerstalker hangs on a branch, a photo string across the crown
    if g > .7:
        ka = clamp((g - .7) / .3)
        push()
        translate(MX - 230, gy + 30 - 64 * 6 * g - 30)
        rotate(.2 + .05 * math.sin(t * 2))
        scale(ka)
        translate(0, 9 * 14)
        hat(14, 'deer', 1.0)
        pop()
        photoString(t, MX - 160, MX + 200, gy + 30 - 64 * 6 * g - 120, 'her', key='ps32')
    # his phone propped on the bench: the reminder is done
    px, py = 1860, st
    bigPhone(px, py - 70, 80, 140, 1.0, key='ph32')
    if n >= 4:
        notifCard(px - 200, py - 250, 420, pk(t, BB[3] + .08, .14), '小苹果', '已送到 ♥', key='nc32')
    u = 30
    hx = MX - 12 * u
    him(hx, oldGround(hx), u, fo(feel('love' if n >= 4 else 'happy', t), view='q', aR=1.2))
    hx2 = MX + 12 * u
    her(hx2, oldGround(hx2), u, fo(feel('love' if n >= 4 else 'excited', t), view='q', flip=True, aR=1.2))
    if n >= 4:
        floatHearts(t, 32, 10, 300, 200, 1720, 760, 16)
    camEnd()


def outro(t):
    # called by the renderer AFTER the lyric strips: the heart iris closes over everything, the title banner sits on top
    endB = bar(33)
    if t < endB - .04:
        return
    if t > endB + .06:
        k = ease(seg(t, endB + .06, DUR - .1))
        r = lerp(1500, 0, k)
        if r > 3:
            irisShape(heartPts(960, 620, r, 48), INK)
        else:
            flatRect(-80, -80, W + 160, H + 160, INK)
    a = t - endB
    push()
    translate(960, 170)
    scale(backOut(clamp((a + .04) / .16)) * .8)
    banner(0, 0, 1240, 190, key='ban32')
    text('Rolling in the Deep × 小苹果', 0, -14, 96, PAL['cream'], stroke=INK, strokeW=16)
    pop()
