# story.py: 《失眠》 shots S01–S16 (one per bar, every beat carries a visible event). Shot data lives in storyboard.py.
import math
from eng import *
import eng
from clawd import *
from props import *
from hl import scarfHook, _chain, WENKAI, stars, rain, ripples, windowView, windowFrame, mug, deskLamp, walker
from sets2 import parkBench, seat, streetTall2, coupleSnap
from sm import *
from common import *


def emH(t, keys):
    return emotions(t, keys, HER)


def emM(t, keys):
    return emotions(t, keys, ME)


def fo(base, **kw):
    d = dict(base)
    d.update(kw)
    return d


def herScarf(view='front', tail=1):
    return scarfHook(view, YARN, YARNDK, tail=tail)


def knitHeart(cx, cy, r, key='kh', col=YARN, dk=YARNDK):
    P = heartPts(cx, cy, r, 40)
    boilSeed(key)
    paint(P, wash=col, fill=dk, fillOp=60, bleed=.05, ink=INK, sw=1.3)
    G.c.save()
    G.c.clipPath(eng._path(P), skia.ClipOp.kIntersect, True)
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.4, Color=skcol(dk, .5), StrokeCap=skia.Paint.kRound_Cap)
    cw = r * .16
    for rr in range(-8, 9):
        yy = cy + rr * cw * .8
        for c in range(-8, 9):
            xx = cx + c * cw
            G.c.drawLine(xx, yy, xx + cw / 2, yy + cw * .55, pa)
            G.c.drawLine(xx + cw / 2, yy + cw * .55, xx + cw, yy, pa)
    G.c.restore()
    G.c.drawCircle(cx - r * .45, cy - r * .45, r * .12, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .4)))


# =====================================================================================
# S01 0–1.60 (pickup) 示例歌 · the nightstand: lamp clicks on, the title is knitted into the scarf stitch by stitch
def s01(t, lt, dur):
    lampK = ease(seg(t, B[0] - .04, B[0] + .05))
    cam(t, 900, 600, lerp(1.16, 1.24, ease(t / 1.6)))
    gradRect(-300, -300, W + 600, H + 600, ['#232A60', '#3A407E'])
    for i in range(-6, 40):
        G.c.drawRect(skia.Rect.MakeXYWH(i * 64, -300, 26, 1100), skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .03)))
    # a polaroid of the two pinned on the wall
    push()
    translate(520, 250)
    rotate(-.08)
    boilSeed('pol1')
    paint(rectPts(-110, -120, 220, 250), wash='#FFFDF6', ink=INK, sw=.9)
    coupleSnap(-92, -102, 184, 170, night=True)
    paint(rectPts(-24, -136, 48, 30), wash='#F2C6D0', washOp=200, ink=None)
    pop()
    # tabletop
    boilSeed('tab1')
    paint([[-200, 690], [W + 200, 690], [W + 200, 750], [-200, 750]], wash='#A07AB0', fill='#7A5A8A', fillOp=60, ink=INK, sw=1.1)
    gradRect(-200, 750, W + 400, 500, ['#7A5A8A', '#523A64'])
    inkLine([[-200, 750], [W + 200, 750]], 1.0, INK, 'ink', 0)
    # basket with yarn
    hop_ = jump(t, B[1] - .02, B[1] + .28, 1.0)
    basket(540, 712, 440, 180, key='bk1')
    yarnBall(650, 560, 78, '#B8AEEA', '#7E73C8', key='yb1b', rot=.6)
    yarnBall(450, 548 + hop_['dy'] * 40, 96, key='yb1', rot=-.3)
    needle(330, 430 + hop_['dy'] * 40, 500, 600 + hop_['dy'] * 40)
    needle(380, 410 + hop_['dy'] * 40, 470, 610 + hop_['dy'] * 40, knob='#7FB8E6')
    # the knitted strip draped over the front edge, the title stitched into it
    knitPiece(250, 700, 700, 210, rot=-.03, key='kp1', title='失眠', titleK=[pk(t, 1, .22), pk(t, 2, .22)], titleSize=132)
    # sewn label
    push()
    translate(840, 885)
    rotate(-.03)
    boilSeed('lab1')
    paint(rectPts(-80, -18, 160, 36), wash='#FFF6EC', ink=INK, sw=.7)
    text('Suki刘舒妤', 0, 0, 22, '#C9587E', face=WENKAI, shadow=False, a=pk(t, 2, .3))
    pop()
    strand([[450, 640], [520, 700], [600, 690]], key='s1a')
    mug(1400, 712, 1.0, key='mg1', col='#F2C6D0')
    # darkness before the lamp
    if lampK < 1:
        flatRect(-300, -300, W + 600, H + 600, '#080A22', .64 * (1 - lampK))
    colon = beatIdx(t) % 2 == 0 if t > B[0] else True
    alarmClock(1180, 712, 1.0, '03:00', key='ac1', colonOn=colon, body=mixCol('#E8E1D2', '#2A2A48', .65 * (1 - lampK)))
    deskLamp(1600, 712, 1.6, lampK, key='l1', flip=True)
    if lampK > 0:
        glow(1460, 450, 900, '#FFB867', .35 * lampK)
    camEnd()


# S02 1.60–3.48 示例歌词内 · she knits in bed, the yarn tangles beat by beat until it swallows her
U2 = 38


def bedHer(t, x, u, o):
    gy = BED_Y + 2.5 * u
    d = dict(o)
    d.setdefault('noShadow', True)
    her(x, gy, u, d)
    return gy


def knitting(t, x, gy, u, o, spd=4.0, piece=True):
    """needles crossing in the lap + the knitted piece; returns the yarn exit point"""
    hl_ = handXY(x, gy, u, o, 'L')
    hr_ = handXY(x, gy, u, o, 'R')
    cx, cy = x, gy - 3.0 * u
    if piece:
        knitPiece(cx - 3.2 * u, cy - .2 * u, 6.4 * u, 1.6 * u, key='kpl', rot=0.0, rib=False)
    wig = math.sin(t * TAU * spd) * .25 * u
    needle(hl_[0], hl_[1], cx + 2.4 * u + wig, cy - .1 * u)
    needle(hr_[0], hr_[1], cx - 2.4 * u - wig, cy - .1 * u, knob='#7FB8E6')
    return cx + 2.0 * u, cy + .6 * u


def s02(t, lt, dur):
    cam(t, 1010, 640, 1.26)
    bedBack(t)
    E = emH(t, [(0, 'happy'), (B[4] - .04, 'confused'), (B[5] - .04, 'nervous'), (B[6] - .04, 'dizzy')])
    wv = math.sin(t * TAU * 3.5)
    o = fo(E, view='front', aL=-.95 + .1 * wv, aR=-.95 - .1 * wv, dx=0, rot=(E.get('rot') or 0) * .5)
    gy = bedHer(t, 960, U2, o)
    quilt(t)
    ex, ey = knitting(t, 960, gy, U2, o)
    strand([[ex, ey], [1120, 900], [1240, 905]], key='s2a')
    yarnBall(1290, 895, 60, key='yb2', rot=t * .5)
    bedFront(t, '03:05', clockS=.62)
    tk = steps(t, [4, 5, 6], [0, .3, .62, 1.0], d=.22)
    if tk > 0:
        tangle(960, lerp(800, 720, tk), lerp(260, 400, tk), lerp(90, 230, tk), tk, seed=3, sw=2.4, ring=True,
               avoid=(960, BED_Y + 2.5 * U2 - 5.6 * U2, 4.6 * U2, 2.3 * U2))
    stamp('示例', 1460, 330, 120, '#FF8FB0', age(t, 3) + .06, rot=-.12)
    camEnd()


# S03 3.48–5.35 示例歌词 · memory: he holds up her scarf, "示例？" … "示例一啦"
def s03(t, lt, dur):
    sunburst(960, 560, '#E6DDF8', '#D4C8F1', 20, rot=t * .25)
    cam(t, 960, 560, 1.0)
    sparkles(t, 5, 12, 100, 80, 1820, 600, 9, '#FFFFFF')
    groundBand(900, '#CFC3EC', '#A99AD8', key='g3')
    # her (left, facing him): hopeful, then her face falls on "示例一"
    Eh = emH(t, [(0, 'hopeful'), (B[10] - .04, 'sad')])
    her(560, 905, 30, fo(Eh, view='q', aL=.35, aR=.55))
    # him (right, facing her)
    Em = emM(t, [(0, 'surprised'), (B[9] - .04, 'neutral', dict(eyes='normal', mouth='flat', rot=.09)),
                      (B[10] - .04, 'neutral', dict(eyes='closed', mouth='smile', rot=-.03, emote='sweat'))])
    up = steps(t, [7, 10], [.2, 1.05, .2], d=.16)
    o = fo(Em, view='q', flip=True, aR=up, aL=up if t < B[10] - .04 else lerp(1.05, -.3, ease(sg(t, 10, kt(10.4)))))
    hx, hy = 1260, 905
    him(hx, hy, 30, o)
    p0 = handXY(hx, hy, 30, o, 'R')
    p1 = handXY(hx, hy, 30, o, 'L')
    if t > B[7] - .1:
        lift = backOut(seg(t, B[7] - .1, B[7] + .1))
        sw_ = math.sin(t * 4) * .5
        if t < B[10] - .04:
            scarfBand(p0, [p1[0], p1[1]], 120 * lift, 70, 110 * lift, 110 * lift, key='sb3', sway=sw_)
        else:
            scarfHang(p0[0], p0[1], 210, 70, sway=sw_, key='sc3', curl=.5)
        for p in (p0, p1):
            G.c.drawCircle(p[0], p[1], 15, skia.Paint(AntiAlias=True, Color=skcol(PAL['clay'])))
            G.c.drawCircle(p[0], p[1], 15, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2, Color=skcol(INK, .8)))
    b8 = pk(t, 8, .18)
    b10 = pk(t, 10, .18)
    if b10 < .5:
        bubble(1210, 360, '示例？', 66, tail=(1250, 600), k=b8 * (1 - b10 * 2), key='bb3')
    if b10 > 0:
        bubble(1180, 350, '示例一啦～', 66, tail=(1250, 600), k=b10, key='bb3b')
    camEnd()


# S04 5.35–7.22 示例歌词 · her knitted heart on the scale: needle to the red, stamped 示例, the heart deflates
def s04(t, lt, dur):
    stripes('#FBE7A1', '#F7D36E', 74)
    cam(t, 960, 560, 1.0)
    flatRect(-100, 830, W + 200, 300, '#E8C46A')
    inkLine([[-100, 830], [W + 100, 830]], 1.0, INK, 'ink', 0)
    sx_, sy_, ss = 1080, 835, 42
    nd = steps(t, [12], [.12, 1.12], d=.2, e=backOut) + .05 * spring(t, B[12] + .1, 5, 26)
    scaleProp(sx_, sy_, ss, nd, key='sc4')
    top = sy_ - 1.25 * ss
    r0 = 165
    land = B[11]
    fall = seg(t, land - .3, land)
    defl = 1 - .42 * easeOut(seg(t, B[14] - .04, B[14] + .2))
    r = r0 * defl
    hy = lerp(-260, top - r * .95, easeIn(fall)) if t < land else top - r * .95 + 18 * spring(t, land, 7, 22)
    sq = .12 * math.exp(-(t - land) * 8) if t > land else 0
    push()
    translate(sx_, hy + r * .9)
    scale(1 + sq, 1 - sq)
    translate(-sx_, -(hy + r * .9))
    knitHeart(sx_, hy, r, key='kh4')
    pop()
    if t > B[14] - .04:
        stamp('噗～', sx_ + 230, hy - 120, 64, '#FFFFFF', age(t, 14) + .06, rot=.15, life=.7)
    rubberStamp('示例', sx_, hy + 10, 118, age(t, 13), rot=-.2)
    E = emH(t, [(0, 'hopeful'), (B[12] - .04, 'surprised'), (B[14] - .04, 'nervous')])
    her(520, 840, 32, fo(E, view='q', aL=.4, aR=.9 if t < B[12] else .3))
    camEnd()


# S05 7.22–9.10 (间奏) 示例 · rainy shop street: she walks without an umbrella, the yarn snags, she lands in a puddle
def s05(t, lt, dur):
    u = 26
    bp = bpOf(t)
    x = 700 + 56 * clamp(bp - 14.6, 0, 2.6)
    if t > B[17] - .1:
        x -= 60 * easeOut(sg(t, kt(16.8), 18))
    cam(t, 860, 600, 1.45)
    streetTall2(t, key='st5', rainK=1.0)
    for i in range(2):
        wx = 1250 + i * 330 - (t - 7.2) * 60
        walker(wx, 660, 12, t, i + 3, -1, umb=True, rate=1.0)
    # the snagged thread: from her back to the lamp post at 600, then off to the left
    gy = 800
    taut = es(t, kt(15.9), 16)
    back = x - 2.4 * u, gy - 5 * u
    sag = lerp(60, 0, taut)
    strand([[-200, 740], [300, 700], [592, 600], [600, 590]], key='s5a')
    strand([[600, 590], [lerp(600, back[0], .5), lerp(590, back[1], .5) + sag], [back[0], back[1]]], key='s5b')
    # puddle
    boilSeed('pd5')
    paint(ellPts(900, gy + 10, 170, 26, 24), wash='#7F8FC0', washOp=200, ink=INK, sw=.7, lite=True)
    turned = t > B[17] - .06
    if not turned:
        mv = move('walk', t)
        o = dict(view='side', walk=mv['walk'], dy=mv['dy'], eyes='normal', mouth=None, aL=.3, aR=-.3)
        if t > B[16] - .04:
            tk = take(t, B[16], 1.0)
            o.update(sq=tk['sq'], dy=tk['dy'] * .4, emote='!', emoteK=pk(t, 16, .12), emoteAge=age(t, 16), rot=-.1 * math.exp(-age(t, 16) * 5))
        her(x, gy, u, o)
    else:
        tr = turn(t, B[17] - .06, B[17] + .08, .25, .875)
        E = emH(t, [(B[17] - .06, 'angry'), (B[18] - .04, 'cry')])
        o = fo(E, view=tr['view'], flip=tr['flip'], smear=tr['smear'], aL=1.0, aR=.2)
        her(x, gy, u, o)
    # splash on k18
    a = age(t, 18)
    if -.02 < a < .55:
        for i in range(14):
            ang = math.pi * (1.05 + .9 * i / 13)
            sp = 260 + 160 * hash1(i * 3.3)
            px = 900 + math.cos(ang) * sp * a * 1.6
            py = gy - 10 + math.sin(ang) * sp * a * 2.2 + 900 * a * a
            boilSeed(f'spl{i}')
            paint(ellPts(px, py, 10, 14, 10), wash='#BFD3F5', ink=INK, sw=.5, lite=True)
    rain(t, 3, 90, 100, 150, 1700, 1100, a=.55, ln=34)
    camEnd()


# S06 9.10–10.98 示例 (breakdown) · soaked on the ground, a little cloud raining on her alone
def s06(t, lt, dur):
    stripes('#9CA8C4', '#8D99B6', 64)
    cam(t, 960, 560, 1.0)
    flatRect(-100, 900, W + 200, 300, '#7E8AA8')
    boilSeed('pd6')
    paint(ellPts(960, 905, 330, 48, 28), wash='#B9C8E8', fill='#8EA0CC', fillOp=60, ink=INK, sw=.8)
    a21 = age(t, 21)
    for j in range(3):
        aa = a21 - j * .18
        if 0 < aa < 1.2:
            rr = 40 + aa * 260
            G.c.drawOval(skia.Rect.MakeXYWH(960 - rr, 905 - rr * .14, 2 * rr, rr * .28),
                         skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skcol('#EEF3FF', .8 * (1 - aa / 1.2))))
    zapK = pk(t, 20, .06) * (1 - seg(t, B[20] + .12, B[20] + .3))
    keys = [(0, 'sad'), (B[20] - .04, 'scared'), (B[20] + .3, 'sad'), (B[22] - .04, 'neutral', dict(eyes='squeeze', mouth='O', emote=None))]
    E = emH(t, keys)
    sneeze = take(t, B[22], 1.4)
    u = 40
    o = fo(E, view='front', aL=-.6, aR=-.6, tint='blue', tintK=.35)
    if t > B[22] - .04:
        o.update(sq=sneeze['sq'], dy=sneeze['dy'] * .6)
    her(960, 900, u, o)
    # yarn wrapped round her
    strand([[960 - 5.6 * u, 900 - 4.2 * u], [960, 900 - 3.4 * u], [960 + 5.6 * u, 900 - 2.6 * u]], key='w6a')
    strand([[960 - 5.6 * u, 900 - 2.4 * u], [960 - 1 * u, 900 - 2.9 * u], [960 + 5.6 * u, 900 - 3.9 * u]], key='w6b')
    strand([[960 + 5.6 * u, 900 - 3.4 * u], [960 + 8 * u, 900 - .5 * u], [960 + 10 * u, 900 + .2 * u]], key='w6c')
    # drip from her flower into the puddle on k21
    fy0, fy1 = 900 - 8.6 * u, 905
    if t > B[21] - .5 and a21 < 0:
        k = seg(t, B[21] - .45, B[21])
        boilSeed('drip')
        paint(ellPts(960 + 10, lerp(fy0, fy1, easeIn(k)), 9, 13, 10), wash='#CFE0FF', ink=INK, sw=.6)
    rainCloud(960, 900 - 10.3 * u, 86, t, key='rc6', zap=zapK, w=300)
    stamp('示例', 400, 330, 150, '#5E78B8', age(t, 19) + .06, rot=-.1)
    if t > B[22] - .04:
        stamp('啊嚏！', 1440, 520, 96, '#FFFFFF', age(t, 22) + .06, rot=.12)
    camEnd()


# S07 10.98–12.86 示例 · she knits like mad on a mountain of scarves, the length sign flips every beat
def scarfPile(cx, base, n, t, newAge=None):
    cols = [YARN, '#F7A8C2', '#E87FA4']
    y = base
    for i in range(n):
        w = max(340, 900 - i * 50)
        h = 54
        off = (40 if i % 2 else -40) + (hash1(i * 3.1) - .5) * 30
        yy = y - h + 6
        drop = 0
        if newAge is not None and i == n - 1 and newAge < .14:
            drop = -260 * (1 - easeIn(clamp(newAge / .14)))
        x0 = cx - w / 2 + off
        knitPiece(x0, yy + drop, w, h, col=cols[i % 3], dk=YARNDK, key=f'sp{i}', rot=0, rib=False)
        for e in (x0, x0 + w):
            d_ = -1 if e == x0 else 1
            for k in range(5):
                fy = yy + drop + 8 + k * (h - 16) / 4
                inkLine([[e, fy], [e + d_ * 22, fy + 4 + 3 * math.sin(t * 3 + k)]], 1.4, YARNDK, 'ink', 0)
        y = yy + 4
    return y


def s07(t, lt, dur):
    sunburst(960, 520, '#FAD7B5', '#F6C08F', 22, rot=t * .3)
    cam(t, 960, 540, lerp(1.06, 1.0, ease(lt / dur)))
    ks = [23, 24, 25, 26]
    j = lastBeat(t, ks, lead=.10)
    n = 3 + 2 * (j + 1)
    na = age(t, ks[j]) + .04 if j >= 0 else None
    top = scarfPile(960, 960, n, t, newAge=na)
    # her on top, knitting fast
    u = 30
    wv = math.sin(t * TAU * 7)
    E = emH(t, [(0, 'determined')])
    o = fo(E, view='front', aL=-.95 + .14 * wv, aR=-.95 - .14 * wv, noShadow=True)
    her(960, top + 10, u, o)
    knitting(t, 960, top + 10, u, o, spd=7, piece=False)
    strand([[960 + 2 * u, top - 3 * u + 10], [1160, top - 20], [1300, top + 40]], key='s7')
    # length sign
    labels = ['1 米', '10 米', '99 米', '999 米']
    fk = seg(t, B[ks[max(0, j)]] - .10, B[ks[max(0, j)]] + .02) if j >= 0 else 1
    txt = labels[max(0, j)] if fk > .5 or j <= 0 else labels[j - 1]
    sy = abs(math.cos(fk * math.pi)) if j > 0 else 1
    sx0, sy0 = 960, 150
    inkLine([[sx0 - 150, -40], [sx0 - 150, sy0 - 40]], 1.2, '#6B4A33', 'ink', 0)
    inkLine([[sx0 + 150, -40], [sx0 + 150, sy0 - 40]], 1.2, '#6B4A33', 'ink', 0)
    push()
    translate(sx0, sy0 + 10)
    scale(1, max(.05, sy))
    boilSeed('sign7')
    paint(rrPts(-200, -62, 400, 124, 16), wash='#C98B5A', fill='#9A6438', fillOp=60, ink=INK, sw=1.1)
    text(txt, 0, 0, 72, '#FFF6E2', stroke=INK, strokeW=9)
    pop()
    stamp('示例', 330, 420, 140, '#E8476E', age(t, 23) + .06, rot=-.12)
    if j == 3:
        stamp('！？', 1560, 440, 90, '#FFFFFF', age(t, 26) + .06, rot=.1)
    camEnd()


# S08 12.86–14.73 示例歌词 · night park: she wraps the endless scarf round a cardboard him; the wind flips it to its blank back
def s08(t, lt, dur):
    nightPark(t, horizon=700)
    cam(t, 1010, 680, 1.22)
    lamp(420, 905, 48, 1.0, key='lp8')
    tree(1720, 900, 66, key='tr8', col='#4E8A5E')
    flipK = ease(seg(t, B[30] - .04, B[30] + .24))
    sxp, gy, u = 1260, 905, 31
    nloop = lastBeat(t, [27, 28]) + 1
    fall = es(t, kt(30.2), kt(30.9))
    hs = [-3.0, -5.2]
    # back halves of the loops
    for i in range(nloop):
        yy = lerp(gy + hs[i] * u, gy - .3 * u - i * 8, fall)
        rx = 6.4 * u * (1 if flipK < .5 else abs(math.cos(flipK * math.pi))) + 30 * fall
        pts = [[sxp + math.cos(a) * rx, yy + math.sin(a) * .8 * u] for a in [math.pi * (1 + s / 10) for s in range(11)]]
        strand(pts, key=f'lb8{i}')
    standee(sxp, gy, u, flipK, dict(view='front', eyes='happy', mouth='smile'), key='sd8')
    for i in range(nloop):
        yy = lerp(gy + hs[i] * u, gy - .3 * u - i * 8, fall)
        rx = 6.4 * u * (1 if flipK < .5 else abs(math.cos(flipK * math.pi))) + 30 * fall
        pts = [[sxp + math.cos(a) * rx, yy + math.sin(a) * .8 * u] for a in [math.pi * s / 10 for s in range(11)]]
        strand(pts, key=f'lf8{i}')
    hx = steps(t, [29], [800, 935], d=.2)
    E = emH(t, [(0, 'happy'), (B[29] - .04, 'love'), (B[30] - .04, 'surprised'), (B[30] + .35, 'sad')])
    o = fo(E, view='q', aL=.2, aR=.8, rot=(.12 if B[29] - .04 < t < B[30] else 0))
    her(hx, gy, u, o)
    hpx, hpy = handXY(hx, gy, u, o, 'R')
    strand([[hpx, hpy], [lerp(hpx, sxp - 6 * u, .5), hpy + 40], [sxp - 6.2 * u, gy + hs[0] * u * (1 - fall)]], key='s8h')
    # the coil she holds
    yarnBall(hpx, hpy - 10, 30, key='yb8')
    stamp('示例歌词', 1010, 400, 100, '#FF8FB0', age(t, 28) + .06, rot=-.06)
    # wind on k30
    a = age(t, 30)
    if -.05 < a < 1.0:
        for i in range(7):
            lx = -200 + (a * 2600 + i * 230) % 2400
            ly = 360 + i * 70 + math.sin(a * 9 + i) * 30
            inkLine([[lx, ly], [lx + 160, ly - 10], [lx + 260, ly + 6]], 1.0, '#D9E2FF', 'inkfine', .6)
            boilSeed(f'lf{i}')
            paint(ellPts(lx + 280, ly, 14, 7, 10, 0, a * 8 + i), wash='#E8B04A' if i % 2 else '#D98A5E', ink=INK, sw=.5)
    camEnd()


# S09 14.73–16.61 (build) 示例 · the scarf goes into a gift box, lid, ribbon, tag — pushing in on every beat
def s09(t, lt, dur):
    gradient('#F7C6D2', '#F3AFC2')
    for i in range(30):
        boilSeed(f'bg9{i}')
        x = (i % 6) * 360 + (90 if (i // 6) % 2 else -90)
        y = (i // 6) * 240 - 60
        paint(heartPts(x, y, 26, 18), wash='#FBD6E0', ink=None, lite=True)
    z = steps(t, [31, 32, 33, 34], [1.0, 1.08, 1.17, 1.28, 1.42], d=.16)
    cam(t, 960, 640, z)
    speed = sg(t, 31, 35)
    if speed > 0:
        impactLines(960, 620, 520, 1300, 28, t, '#FFFFFF', key='im9', sw=1.4 + 2 * speed)
    boilSeed('tbl9')
    paint([[-200, 860], [W + 200, 860], [W + 200, 1300], [-200, 1300]], wash='#FFF1F4', fill='#F2C6D0', fillOp=50, ink=INK, sw=1.0)
    # the folded scarf drops into the box on k31
    inBox = t > B[31] - .04
    if not inBox:
        k = seg(t, B[31] - .32, B[31] - .04)
        knitPiece(860, lerp(-150, 560, easeIn(k)), 200, 70, key='kp9', rib=False)
    giftBox(960, 900, 70, lidK=seg(t, B[32] - .13, B[32] - .01), ribbonK=pk(t, 33, .12), bowK=pk(t, 33, .2), tagK=pk(t, 34, .2), key='gb9', scarf=inBox)
    if t > B[31] - .04 and age(t, 31) < .4:
        sparkles(t, 9, 8, 700, 500, 1220, 700, 16, '#FFFFFF')
    camEnd()


# S10 16.61–18.48 (drop) 示例一 示例 · flash: she bursts in holding the gift high, hearts explode
def s10(t, lt, dur):
    sunburst(960, 500, '#FF9EC0', '#FF80AA', 24, rot=t * .6)
    cam(t, 960, 590, 1.1)
    floatHearts(t, 7, 18, 0, 0, 1920, 1080, 24)
    up = backOut(seg(t, B[35] - .06, B[35] + .14))
    gy = lerp(1600, 935, up)
    jp = jump(t, kt(36.45), B[37], 2.4)
    E = emH(t, [(0, 'excited'), (B[38] - .04, 'love')])
    o = fo(E, view='front', aL=1.6, aR=1.6, dy=jp['dy'], sq=jp['sq'], emote=None)
    u = 40
    her(960, gy, u, o)
    lx, ly = handXY(960, gy, u, o, 'L')
    rx, ry = handXY(960, gy, u, o, 'R')
    bs = 44 * (1 + .25 * easeOut(sg(t, 38, kt(38.4))))
    giftBox((lx + rx) / 2, min(ly, ry) - 6, bs, 1, 1, 1, 1, key='gb10')
    a = age(t, 36)
    if -.04 < a < .8:
        for i in range(14):
            ang = i / 14 * TAU + .2
            d = 120 + 900 * easeOut(clamp(a / .8))
            boilSeed(f'hb{i}')
            paint(heartPts(960 + math.cos(ang) * d, 420 + math.sin(ang) * d * .7, 30 * (1 - a), 18), wash='#E2476E' if i % 2 else '#FFFFFF', ink=INK, sw=.6)
    a38 = age(t, 38)
    if a38 > -.04:
        hk = backOut(clamp((a38 + .04) / .16)) * (1 + .08 * math.sin(a38 * 14) * math.exp(-a38 * 4))
        boilSeed('bigh')
        paint(heartPts(1520, 320, 120 * hk, 30), wash='#FFFFFF', fill='#FFD0DE', fillOp=80, ink=INK, sw=1.4)
        paint(heartPts(400, 380, 80 * hk, 30), wash='#E2476E', ink=INK, sw=1.2)
    camEnd()


# S11 18.48–20.35 示例一 最后 · night bench: one scarf round both necks; he stands up, it slides off, he walks away
def s11(t, lt, dur):
    nightPark(t, horizon=660)
    cam(t, 1000, 740, 1.42)
    lamp(470, 905, 48, 1.0, key='lp11')
    tree(1590, 905, 60, key='tr11', col='#4E8A5E')
    u = 26
    st = parkBench(960, 905, 760, 150, 170, key='pb11', night=.6)
    Eh = emH(t, [(0, 'happy'), (B[40] - .04, 'love'), (B[41] - .04, 'surprised'), (B[42] - .04, 'sad', dict(eyes='teary'))])
    hx = 780
    oh = fo(Eh, view='q', aL=.2, aR=.5 if t < B[42] - .04 else .9, draw=herScarf('q', tail=0))
    seat(her, hx, st, u, oh)
    nx = hx + 5.2 * u
    ny = st + 2 * u - 3.5 * u
    stood = t > B[41] - .04
    if not stood:
        Em = emM(t, [(0, 'happy'), (B[40] - .04, 'love')])
        mx = 1150
        seat(him, mx, st, u, fo(Em, view='q', flip=True, aL=.2, aR=.3, draw=scarfHook('q', YARN, YARNDK, tail=0)))
        mxn = mx - 5.2 * u
        strand([[nx, ny], [(nx + mxn) / 2, ny + 70], [mxn, ny]], key='arc11')
        if t > B[40] - .04:
            floatHearts(t, 11, 6, nx, ny - 260, mxn, ny - 20, 16)
    else:
        # the scarf slid off him: its end lies on the seat
        strand([[nx, ny], [nx + 120, st - 6], [1180, st - 4], [1240, st + 30]], key='arc11b')
        if t < B[42] - .04:
            k = ease(seg(t, B[41] - .04, B[41] + .14))
            mx, my = lerp(1150, 1460, k), lerp(st + 2 * u, 905, k)
            jp = -math.sin(k * math.pi) * 90
            him(mx, my + jp, u, dict(view='qback', flip=False, eyes='normal', mouth='flat', aL=.1, aR=.1))
        else:
            mv = move('walk', t)
            mx = 1460 + 520 * easeIn(sg(t, 42, kt(43.6)))
            him(mx, 905, u, dict(view='side', walk=mv['walk'], dy=mv['dy'], aL=.1, aR=.1, eyes='normal'))
    camEnd()


# S12 20.35–22.23 示例歌词 · back in bed hugging the scarf, eyes open; the clock jumps every beat
def s12(t, lt, dur):
    cam(t, 1130, 600, 1.12)
    bedBack(t)
    E = emH(t, [(0, 'sad', dict(eyes='wide', mouth='flat', gloom=.2)), (B[45] - .04, 'sad', dict(eyes='teary', mouth='wobble'))])
    o = fo(E, view='front', aL=-.2, aR=-.2, draw=herScarf('front', tail=1))
    gy = bedHer(t, 860, U2, o)
    quilt(t)
    j = lastBeat(t, [43, 44, 45, 46])
    txt = ['04:00', '04:30', '05:00', '05:30'][max(0, j)]
    sh = .05 * spring(t, B[[43, 44, 45, 46][max(0, j)]], 7, 30) if j >= 0 else 0
    bedFront(t, txt, clockS=.92, clockShake=sh)
    stamp('失眠', 1240, 300, 150, '#B8AEEA', age(t, 45) + .06, rot=-.1)
    camEnd()


# S13 22.23–24.11 示例歌词内 · the building at night: the other windows go dark one beat at a time
LIT13 = {(0, 4): 47, (-1, 1): 48, (1, 3): 49, (0, 0): 49, (-1, 3): 50, (1, 1): 50, (-1, 4): 47, (1, 0): 48}


def herInWindow(alpha=1.0, emo='sad'):
    def inside(x, y, w, h):
        glow(x + w * .7, y + h * .35, 160, '#FFE2A0', .6 * alpha)
        her(x + w / 2, y + h + 34, 23, dict(view='front', eyes='teary' if emo == 'sad' else 'wide', mouth='flat', aL=-.4, aR=-.4, noShadow=True,
                                             lite=True, draw=herScarf('front', tail=1)))
    return inside


def s13(t, lt, dur):
    cam(t, 960, 520, lerp(1.14, 1.0, ease(lt / dur)))

    def lit(r, c):
        k = LIT13.get((r, c))
        if k is None:
            return 0.0
        return 1 - ease(seg(t, B[k] - .04, B[k] + .05))
    facade2(t, lit, 1.0, inside=herInWindow())
    camEnd()


# S14 24.11–25.99 示例 一句 · the windowsill: his cigarette still smoking in the ashtray, a curl of smoke every beat
def sillSet(t):
    gradRect(-400, -400, W + 800, H + 800, ['#141838', '#22285A'])
    wx, wy, ww, wh = 300, -120, 1320, 740
    windowView(wx, wy, ww, wh, t, cityK=.18, starsK=1.0, key='swv', moonXY=(wx + ww * .8, wy + wh * .36))
    windowFrame(wx, wy, ww, wh, '#4E3A3E', key='swf', sill=False)
    glow(1360, 160, 700, '#C9D2FF', .16)
    # the sill: top lit by the moon, front face, wall below
    boilSeed('sill14')
    paint([[wx - 90, wy + wh + 8], [wx + ww + 90, wy + wh + 8], [wx + ww + 110, wy + wh + 50], [wx - 110, wy + wh + 50]], wash='#6E6A8E', fill='#4E4A6E', fillOp=60, ink=INK, sw=1.0)
    flatRect(wx - 90, wy + wh + 8, ww + 180, 10, '#B8C0E8', .35)
    paint(rectPts(wx - 110, wy + wh + 50, ww + 220, 46), wash='#4A4668', ink=INK, sw=1.0)
    gradRect(-400, wy + wh + 96, W + 800, 600, ['#1C2048', '#141836'])
    sy = wy + wh + 30
    mug(640, sy + 4, 1.35, key='mg14', col='#F2C6D0')
    lighter(1340, sy + 6, 48, key='lt14')
    basket(400, sy + 4, 230, 110, key='bk14')
    yarnBall(360, sy - 120, 62, key='yb14', rot=.4)
    yarnBall(450, sy - 108, 50, '#B8AEEA', '#7E73C8', key='yb14b', rot=1.2)
    needle(300, sy - 250, 420, sy - 110)
    strand([[450, sy - 70], [540, sy + 10], [560, sy + 60], [548, sy + 180]], key='s14')
    return ashtray(1010, sy, 62, key='at14', t=t)


def s14(t, lt, dur):
    cam(t, 980, 470, lerp(1.22, 1.32, ease(lt / dur)))
    ex, ey = sillSet(t)
    spawns = [B[51] - 2.4, B[51] - 1.2, B[52], B[53], B[54], B[54] + .24]
    for i, tb in enumerate(spawns):
        smokeCurl(t, ex, ey - 6, i + 1, t - tb, rise=520, sway=80, w=13, a=.6, life=3.4)
    smokeRing(t, ex + 10, ey - 80, age(t, 53), r=48, a=.7)
    camEnd()


# S15 25.99–27.87 示例歌词 · the smoke gathers into him; she reaches out and he drifts apart
def s15(t, lt, dur):
    cam(t, 980, 400, 1.3)
    ex, ey = sillSet(t)
    spawns = [B[53], B[54], B[55], B[56], B[57], B[58]]
    for i, tb in enumerate(spawns):
        smokeCurl(t, ex, ey - 6, i + 11, t - tb, rise=300, sway=60, w=12, a=.5, life=2.6)
    form = ease(seg(t, B[55] - .3, B[55] + .02))
    spread = ease(seg(t, B[58] - .04, B[58] + 1.0))
    a56 = age(t, 56)
    blink = 1 - abs(clamp(a56 / .07, -1, 1)) if -.07 < a56 < .07 else 0
    smokeHim(t, 1080, 520, 26, form, spread, blink, a=.9 * (1 - .7 * spread))
    if t > B[58] - .04:
        for j in range(3):
            smokeRing(t, 1080 + (j - 1) * 140, 380, age(t, 58) - j * .08, r=52, a=.6)
    E = emH(t, [(0, 'sad', dict(eyes='teary')), (B[57] - .04, 'hopeful'), (B[58] - .04, 'sad', dict(eyes='teary'))])
    reach = es(t, kt(56.7), 57)
    o = fo(E, view='q', aL=-.3, aR=lerp(-.2, .75, reach), draw=herScarf('q', tail=0))
    her(560, 790, 30, o)
    camEnd()


# S16 27.87–END 尾 · the whole building dark but her window; smoke drifts to the moon; her light goes out — two eyes still open
def s16(t, lt, dur):
    k62 = B[62]
    zsnap = easeOut(seg(t, k62 - .04, k62 + .22))
    z = lerp(lerp(.74, .68, ease(seg(t, B[59], k62))), 2.2, zsnap)
    cy = lerp(150, 520, zsnap)
    cam(t, 960, cy, z)
    flick = 1 - .75 * math.exp(-max(0, age(t, 61)) * 9) if t > B[61] - .04 else 1
    herLit = flick * (1 - ease(seg(t, k62 - .04, k62 + .02)))
    veil = es(t, 60, kt(60.6))
    eyesK = pk(t, 62, .12)
    ab = t - (k62 + .2)
    blink = 1 - abs(ab) / .06 if abs(ab) < .06 else 0
    insideFn = herInWindow(herLit) if herLit > .05 else None
    facade2(t, lambda r, c: 0.0, herLit, inside=insideFn, moonXY=(1330, -470), moonVeil=veil, eyesK=eyesK, eyesBlink=blink)
    # smoke from her window up to the moon
    for i in range(6):
        tb = B[59] - 1.4 + i * .5
        smokeCurl(t, 960 + (i % 3 - 1) * 40, 340, i + 21, t - tb, rise=820, sway=170, w=18, a=.45 * (1 - zsnap), life=3.0)
    if veil > 0:
        for j in range(3):
            softLine([[1330 - 170 + j * 30, -470 + (j - 1) * 26], [1330, -490 + j * 30], [1330 + 180, -470 + (j - 1) * 20]], 28, SMOKE, .5 * veil * (1 - zsnap), blur=12)
    camEnd()


SHOTS = []
_FN = dict(S01=s01, S02=s02, S03=s03, S04=s04, S05=s05, S06=s06, S07=s07, S08=s08, S09=s09, S10=s10, S11=s11, S12=s12, S13=s13,
           S14=s14, S15=s15, S16=s16)
for s in SB['shots']:
    SHOTS.append((s['start'], _FN[s['id']], s['tr'], s['id']))
