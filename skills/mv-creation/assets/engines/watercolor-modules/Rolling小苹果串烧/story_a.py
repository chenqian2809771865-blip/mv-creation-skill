# story_a.py: S01–S08 — Rolling in the Deep intro + verse (the suspicion catches fire). Every beat carries a visible event.
import math
from eng import *
from clawd import *
from props import *
from props_chuanshao import *
from props3 import *
from props_zuitian import bunting, tentBack, tableCloth as tentCloth
from common import *


# ===================================================================== S01 the phone lights up on the coffee table
def s01(t, lt, dur):
    BB = beatsOf(1)
    n = nOn(t, BB)
    cam(t, 960, 540, lerp(1.0, 1.07, ease(lt / 2.0)))
    coffeeTableTop(t)
    lit = ease(seg(t, BB[0] - .04, BB[0] + .06))
    buzz = math.sin(t * 90) * 4 * math.exp(-(t - BB[0]) * 6) if t >= BB[0] - .04 else 0
    push()
    translate(880 + buzz, 520)
    rotate(-.06)
    bigPhone(0, 0, 440, 780, lit, key='ph1')
    if lit > .05:
        text('23:47', 0, -230, 96, '#FFFFFF', shadow=False, a=lit)
        text('10月28日 星期三', 0, -150, 30, '#EAF6FF', shadow=False, a=lit)
    notifCard(0, 10, 560, pk(t, BB[1], .14), '小苹果', '今晚老地方见', key='nc1')
    # the apple charm on its strap, lying on the table by the phone's corner
    sw_ = .08 * math.sin(t * 2.3)
    inkLine([[-205, -372], [-250, -420], [-290 + 6 * sw_, -446]], 1.2, '#B9B2A8', 'inkfine', .4)
    apple(-312 + 8 * sw_, -470, 30, key='charm1', rot=-.4 + sw_)
    pop()
    if n >= 1 and t - BB[0] < .5:
        a = t - BB[0]
        for s_ in (-1, 1):
            for k in range(3):
                r = 250 + k * 40 + a * 120
                inkLine([[880 + s_ * r, 380 - 40 * k], [880 + s_ * (r + 30), 520], [880 + s_ * r, 660 + 40 * k]], 1.6, '#FFF5E2', 'ink', .6)
        stamp('叮！', 1180, 200, 100, '#FFE36E', a, rot=.12, life=.5)
    # magnifier slides in from the left on beat 3 and settles over the reminder
    k3 = easeOut(seg(t, BB[2] - .14, BB[2] + .02))
    if k3 > 0:
        lx, ly, R = lerp(-300, 760, k3), 530 + 10 * math.sin(t * 3), 170
        boilSeed('lens1')
        push()
        translate(lx + R * .7, ly + R * .7)
        rotate(.78)
        paint(rrPts(0, -26, 300, 52, 20), wash='#7A4E33', ink=INK, sw=1.2)
        pop()
        c = G.c
        c.save()
        c.clipPath(skia.Path().addCircle(lx, ly, R), skia.ClipOp.kIntersect, True)
        push()
        translate(lx, ly)
        scale(1.7)
        translate(-lx, -ly)
        push()
        translate(880, 520)
        rotate(-.06)
        bigPhone(0, 0, 440, 780, lit, key='ph1z')
        notifCard(0, 10, 560, 1, '小苹果', '今晚老地方见', key='nc1')
        pop()
        pop()
        paint(ellPts(lx, ly, R, R, 40), wash='#DDF2FF', washOp=40, ink=None)
        c.restore()
        paint(ellPts(lx, ly, R + 10, R + 10, 48), ink='#C99A2E', sw=3.6)
        paint(ellPts(lx, ly, R, R, 48), ink=INK, sw=1.2)
        paint(ellPts(lx - R * .45, ly - R * .5, R * .16, R * .08, 12, 0, -.7), wash='#FFFFFF', washOp=150, ink=None)
    # she pops up from the bottom-right on beat 4
    k4 = backOut(seg(t, BB[3] - .1, BB[3] + .1))
    if k4 > 0:
        her(1500, lerp(1520, 1200, k4), 46, fo(feel('suspicious', t), view='q', flip=True, emote='!?', emoteK=pk(t, BB[3], .12),
                                              emoteAge=t - BB[3]), detective=True)
    camEnd()


# ===================================================================== S02 title
def s02(t, lt, dur):
    BB = beatsOf(2)
    sunburst(960, 560, '#5B2A6E', '#7A3A86', 20, rot=t * .25)
    cam(t)
    bunting(-60, 620, 40, 70, 7, t, key='tb1')
    bunting(1300, 1980, 40, 70, 7, t, key='tb2')
    for i in range(8):
        x = 120 + i * 240 + 30 * math.sin(t * .8 + i)
        y = 980 - frac(t * .12 + hash1(i)) * 1100
        if i % 2:
            apple(x, y, 22, key=f'fa{i}', rot=t + i)
        else:
            text('?', x, y, 56, '#C9B8EC', shadow=False, a=.7)
    for i, (x, y) in enumerate([(240, 270), (1680, 250), (300, 790), (1620, 770)]):
        yiyun(x, y + math.sin(bpOf(t) * math.pi) * -14, 60, t, i, pk(t, BB[2] + (i % 2) * .12, .2))
    k = backOut(seg(t, BB[0] - .04, BB[0] + .16))
    push()
    translate(960, 400)
    scale(lerp(1.6, 1, k) * (1 + .03 * pulse(t, 9)))
    rotate(-.035)
    banner(0, 0, 1300, 210, key='tban')
    text('Rolling in the Deep', 0, -18, 112, PAL['cream'], stroke=INK, strokeW=18)
    pop()
    a2 = pk(t, BB[1], .16)
    if a2 > 0:
        push()
        translate(1380, 600)
        scale(backOut(a2))
        rotate(.08)
        apple(-190, 0, 52, key='tap')
        text('× 小苹果', 40, 0, 96, '#FFFFFF', stroke=C['red'], strokeW=16)
        pop()
        text('Adele × 筷子兄弟 · 串烧', 640, 590, 44, '#FFF5E2', stroke=INK, strokeW=8, a=a2)
    up = backOut(seg(t, BB[3] - .1, BB[3] + .08))
    her(960, lerp(1320, 1020, up), 36, fo(feel('suspicious', t), aR=1.25, aL=-.3, armR=magnifierHook(1.15)), detective=True)
    if t > BB[3]:
        sparkles(t, 9, 8, 700, 650, 1250, 900, 18, '#FFFFFF')
    camEnd()


# ===================================================================== S03 There's a fire (her room catches the glow)
def s03(t, lt, dur):
    BB = beatsOf(3)
    n = nOn(t, BB)
    warm = steps(t, BB, [0, .12, .3, .5, .75])
    cam(t, 960, 520, 1.03 + .03 * lt)
    herRoom(t, warm=warm)
    embers(t, 3, 4 + 5 * n, 0, 0, W, 760)
    lampK = 1.0
    if n >= 2 and t - BB[1] < .25:
        lampK = .35 + .65 * (1 if int((t - BB[1]) * 24) % 2 else 0)
    emo = 'determined' if n < 3 else 'angry'
    her(760, 815, 42, fo(feel(emo, t), view='front', tint='flush', tintK=.18 * n, aL=.2, aR=.2), detective=True)
    herDesk(t, lampK=lampK)
    hx, hy, hr = 1270, 420, 150
    glow(hx, hy, hr * 2.6, '#FF8A3D', .25 * n)
    boilSeed('fheart')
    paint(heartPts(hx, hy, hr * (1 + .05 * pulse(t, 7)), 30), wash=C['heart'], fill='#9E1F30', fillOp=80, ink=INK, sw=1.6)
    if n >= 1:
        a = t - BB[0]
        paint(starPts(hx + 40, hy - hr * .55, 30 + 40 * math.exp(-a * 8), .35, 4), wash='#FFF3B0', ink=INK, sw=.8)
    if n >= 2:
        fk = [0, 0, .45, .75, 1.0][n] * (backOut(clamp((t - BB[n - 1] + .04) / .14)) * .3 + .7)
        xs = [-.55, -.2, .2, .55] if n >= 4 else ([-.1, .25] if n == 3 else [.1])
        for i, dx in enumerate(xs):
            flame(hx + dx * hr * 1.3, hy - hr * .55 + abs(dx) * hr * .5, 110 * fk * (1.1 - abs(dx) * .4), t, key=f'f3{i}')
    if n >= 4:
        stamp('燃！', 420, 330, 120, '#FFE36E', t - BB[3], rot=-.15)
    camEnd()


# ===================================================================== S04 he sneaks out of the building, she peeks
def s04(t, lt, dur):
    BB = beatsOf(4)
    n = nOn(t, BB)
    cam(t, 960, 560, 1.0)
    up = 0.0
    if n >= 2:
        up = ease(seg(t, BB[1] - .12, BB[1]))
    if n >= 3:
        up = 1 - ease(seg(t, BB[2] - .08, BB[2]))
    if n >= 4:
        up = .75 * ease(seg(t, BB[3], BB[3] + .2))

    def inside(x, y, w, h):
        her(x + w / 2, y + h + lerp(150, 10, up), 16, fo(feel('suspicious', t), view='q', noShadow=True, lookX=.8), detective=True)
        curtain(x + 10, y - 6, h + 20, -1, .1 * math.sin(t * 3), '#E89AAE', key='apc1')
        curtain(x + w - 10, y - 6, h + 20, 1, .1 * math.sin(t * 3), '#E89AAE', key='apc2')
    doorK = 1.0 if n < 4 else 1 - easeOut(clamp((t - BB[3] + .04) / .1))
    apartment(t, inside=inside, doorK=doorK, catLook=1 if n < 3 else 1)
    # him: one tiptoe step per beat, landing ON the beat
    xs = [1070, 1180, 1290, 1400, 1510]
    j = n
    x = xs[j]
    dy, sq = 0, 0
    if j < 4:
        nb = BB[j]
        if t > nb - .3:
            x = lerp(xs[j], xs[j + 1], ease(seg(t, nb - .3, nb)))
            dy, sq = hop(t, nb - .3, nb, 26)
    if j >= 1 and t - BB[j - 1] < .2:
        dy, sq = hop(t, BB[j - 1] - .3, BB[j - 1], 26)
    look = n == 3
    him(x, 905 + dy, 30, fo(feel('nervous', t), view='q', flip=look, aR=1.2, armR=giftHook(1, 'g4'), sq=sq, aL=.6, emote='sweat' if look else None))
    if n >= 4:
        stamp('咔哒', 1060, 600, 70, '#FFE36E', t - BB[3], rot=.1)
    camEnd()


# ===================================================================== S05 fever pitch: the kitchen boils over
def s05(t, lt, dur):
    BB = beatsOf(5)
    n = nOn(t, BB)
    warm = steps(t, BB, [0, .15, .35, .6, .9])
    cam(t, 960, 540, 1.0)
    kitchen(t, warm)
    lid = t - BB[3] if n >= 4 else -1
    jig = math.sin(t * 60) * 6 * (1 if n == 3 else 0)
    kettle(1500, 735 + jig * .3, 60, t, heat=steps(t, BB, [.1, .3, .55, .8, 1.0]), lidPop=lid, key='kt5', lidHop=t - BB[2] if n == 3 else -1)
    lv = steps(t, BB, [.1, .3, .52, .78, 1.05])
    thermometer(1130, 920, 620, lv, key='th5', burst=t - BB[3] if n >= 4 else 0)
    if n == 3 and t - BB[2] < .4:
        stamp('哐！', 1640, 560, 64, '#FFFFFF', t - BB[2], rot=.12, life=.4)
    labels = ['37°', '38.5°', '40°', '爆表！']
    if n >= 1:
        col = INK if n < 4 else C['red']
        text(labels[n - 1], 1300, 220 if n < 4 else 180, 96 if n < 4 else 124, col, stroke=PAL['cream'], strokeW=14, shadow=True,
             sc=backOut(pk(t, BB[n - 1], .12)), rot=.06)
    emo = ['nervous', 'nervous', 'determined', 'angry', 'angry'][n]
    sh = shake(t, BB[3], 14, .4) if n >= 4 else (0, 0)
    her(620 + sh[0], 905, 42, fo(feel(emo, t), view='q', tint='flush', tintK=.2 * n, emote='anger' if n >= 3 else 'sweat'), detective=True)
    for i in range(n):
        a = t - BB[i]
        if a < .5:
            puff(620 + (i - 1.5) * 90, 905 - 13 * 42 - a * 300, 18 + a * 40, col='#FFFFFF', key=f'stm{i}', ink=False, a=1 - a / .5)
    if n >= 4:
        impactLines(1130, 260, 120, 380, 16, t, '#FFF5E2', key='imp5', sw=1.4)
    camEnd()


# ===================================================================== S06 out of the dark: the spotlights of the little theatre
def s06(t, lt, dur):
    BB = beatsOf(6)
    n = nOn(t, BB)
    signK = ease(seg(t, BB[3] - .04, BB[3] + .1)) if n >= 4 else 0
    cam(t, 960, 540)
    theatre(t, signK)
    poses = [(.2, .2), (1.4, -.3), (-.3, 1.4), (1.2, 1.2), (1.5, -.2)]
    p = poses[n]
    her(960, 900, 40, fo(feel('cool' if n >= 4 else 'determined', t), view='front', aL=p[0], aR=p[1],
                          armR=magnifierHook(1.1) if n >= 4 else None, sq=take(t, BB[max(0, n - 1)], .8)['sq'] if n else 0), detective=True)
    camEnd()
    xs = [300, 1660, 1320, 960]
    full = skia.Path()
    full.addRect(skia.Rect.MakeXYWH(-200, -200, W + 400, H + 400))
    holes = None
    for i in range(n):
        x = xs[i]
        k = easeOut(clamp((t - BB[i] + .04) / .08))
        w0, w1 = 90 * k, (320 if i < 3 else 540) * k
        b = skia.Path()
        b.addPoly([skia.Point(x - w0 / 2, -50), skia.Point(x + w0 / 2, -50), skia.Point(x + w1 / 2, 920), skia.Point(x - w1 / 2, 920)], True)
        b.addOval(skia.Rect.MakeXYWH(x - w1 * .55, 920 - w1 * .12, w1 * 1.1, w1 * .24))
        holes = b if holes is None else skia.Op(holes, b, skia.PathOp.kUnion_PathOp)
    if signK > 0:
        b = skia.Path()
        b.addOval(skia.Rect.MakeXYWH(560, 40, 800, 300))
        holes = b if holes is None else skia.Op(holes, b, skia.PathOp.kUnion_PathOp)
    dark = skia.Op(full, holes, skia.PathOp.kDifference_PathOp) if holes is not None else full
    G.c.drawPath(dark, skia.Paint(AntiAlias=True, Color=skcol('#0C0A18', .9)))
    for i in range(n):
        x = xs[i]
        spotLamp(x, 40, 1, key=f'sl{i}')
        k = easeOut(clamp((t - BB[i] + .04) / .08))
        flat([[x - 45 * k, 60], [x + 45 * k, 60], [x + (160 if i < 3 else 270) * k, 920], [x - (160 if i < 3 else 270) * k, 920]], '#FFF2C4', .14)
    for i in range(n, 4):
        spotLamp(xs[i], 40, 0, key=f'sl{i}')
    if n >= 4:
        sparkles(t, 6, 10, 700, 300, 1250, 850, 22, '#FFFFFF')
        stamp('登场！', 1460, 380, 110, '#FFE36E', t - BB[3], rot=.12)


# ===================================================================== S07 Finally I can see you: magnifier POV over the shop street
def street7(t, hx):
    streetTall2(t, key='st7', rainK=0)
    mv = move('walk', t)
    him(hx, 668, 24, fo(feel('happy', t), view='q', walk=mv['walk'], dy=mv['dy'], aR=1.2, armR=giftHook(1, 'g7'), aL=.3))


def s07(t, lt, dur):
    BB = beatsOf(7)
    n = nOn(t, BB)
    hx = lerp(1060, 1300, lt / dur)
    camBegin(960, 430, 1 + bump(t))
    street7(t, hx)
    camEnd()
    darken = .6
    flatRect(-200, -200, W + 400, H + 400, '#0E0B1E', darken)
    z = steps(t, BB, [1.1, 1.35, 1.65, 1.95, 2.25])
    lx, ly, R = 960, 470, 380
    c = G.c
    c.save()
    c.clipPath(skia.Path().addCircle(lx, ly, R), skia.ClipOp.kIntersect, True)
    c.translate(lx - 960, ly - 540)
    camBegin(hx + 40, 548, z)
    street7(t, hx)
    camEnd()
    paint(ellPts(lx, ly, R, R, 50), wash='#DDF2FF', washOp=36, ink=None)
    c.restore()
    boilSeed('lens7')
    push()
    translate(lx + R * .72, ly + R * .72)
    rotate(.78)
    paint(rrPts(0, -32, 420, 64, 22), wash='#7A4E33', ink=INK, sw=1.4)
    pop()
    paint(ellPts(lx, ly, R + 18, R + 18, 60), ink='#C99A2E', sw=4.5)
    paint(ellPts(lx, ly, R, R, 60), ink=INK, sw=1.6)
    paint(ellPts(lx - R * .45, ly - R * .5, R * .16, R * .08, 12, 0, -.7), wash='#FFFFFF', washOp=150, ink=None)
    if n >= 4:
        stamp('看清了！', 1580, 240, 96, '#FFE36E', t - BB[3], rot=.12)


# ===================================================================== S08 crystal clear: the fortune tent
def s08(t, lt, dur):
    BB = beatsOf(8)
    n = nOn(t, BB)
    tentBack(t, key='tent8')
    cam(t, 960, 540, 1.0 + .03 * lt)
    o = fo(feel('suspicious' if n < 4 else 'surprised', t), view='q', aR=1.0, aL=.4, armR=magnifierHook(1.2),
           emote='!' if n >= 4 else None, emoteK=pk(t, BB[3], .12), emoteAge=t - BB[3])
    her(690, 760, 44, o, detective=True)
    tentCloth(120, 1800, 640, 500, key='tc8')
    for i, (cx, h) in enumerate([(260, 120), (360, 80), (1620, 100), (1720, 140)]):
        flick = 1.0 if not (n >= 1 and 0 <= t - BB[0] < .2) else .6
        candle(cx, 690, h * flick, t, key=f'cd8{i}')
    for i, (tx, rot, face) in enumerate([(560, -.2, 'heart' if n >= 3 else None), (690, -.08, 'apple' if n >= 3 else None),
                                         (880, .1, 'moon'), (1430, .22, 'star')]):
        tarot(tx, 800, rot, face, key=f'tr8{i}')
    k = ease(seg(t, BB[0] - .04, BB[0] + .1)) if n else 0
    bx, by, br = 1180, 460, 170

    def inside():
        fog = 1 - ease(seg(t, BB[1] - .07, BB[1] + .07)) if t > BB[1] - .07 else 1
        gradRect(bx - br, by - br, 2 * br, 2 * br, ['#3B3770', '#8E79BC'])
        if n >= 3:
            a = pk(t, BB[2], .2)
            him(bx - 10, by + 120, 13, fo(feel('happy', t), view='q', aR=1.2, armR=appleHook(1.5, shine=1, key='cbap'), noShadow=True, tint='blue', tintK=.6))
            glow(bx + 30, by + 20, 110, '#FF5A6A', a * (.8 + .4 * pulse(t, 6)))
        for i in range(6):
            puff(bx - 160 + i * 62, by + 50 * math.sin(i * 1.7 + t), 34 + 8 * (i % 3), col='#D9CCF2', key=f'fog{i}', ink=False, a=.85 * fog)
    crystalBall(bx, by, br, k, key='cb8', inside=inside)
    if n >= 4:
        flash(.55 * (1 - clamp((t - BB[3]) / .12)))
        sparkles(t, 18, 12, 950, 260, 1420, 680, 24, '#FFFFFF')
    camEnd()
