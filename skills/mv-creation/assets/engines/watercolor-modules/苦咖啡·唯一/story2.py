# story2.py: 《苦咖啡·唯一》 shots S15–S27 (verse: the paper-cup phone, her weird taste, the washed chalk, the music box,
# the note umbrella, the film wraps, the figurine, the chalk portrait, the stage, the dream, the search). Helpers come from story.py.
import math
from eng import *
import eng
from clawd import *
from props import bubble, stamp, sparkle, sparkles, impactLines, stripes, sunburst, puff, floatHearts, trashcan
from sets import flatGround, starField
from sets2 import seat
from dx import flagPop, speedLines
from hl import memoryGrade, vignette, tint, rain
from nm import recorder, darkness
from wx import shopStreet, cafeTable, line, _pa
from props_chuanshao import bloom, petalsFly
from props_zuitian import balloon
from sets_huibuhui import splashDrops
from common import *
from kf import *
from story import addJ, heldCup, memory, sigh, U_WIDE


def nightBg(t, key='nb', lamp_=1.0, lampX=1860):
    skyGrad(NIGHT_SKY)
    starField(t, 7, 50, 0, 0, W, 420, r=2.6)
    skyline(1.0, key + 'sk')
    pavement(GY, .9, key + 'pv')
    streetLamp(lampX, GY, 1.0, lamp_, key + 'lp', dirn=-1)


def shards(t, t0, cx, cy, n=14, key='sh'):
    a = t - t0
    if a < 0 or a > .7:
        return
    for i in range(n):
        ang = i / n * TAU + hash1(i) * .4
        r = 120 + 1400 * easeOut(a / .7) * (.6 + .5 * hash1(i * 3))
        x, y = cx + math.cos(ang) * r, cy + math.sin(ang) * r + 300 * a * a
        s = 26 + 20 * hash1(i * 7)
        rot = a * 9 * (1 if i % 2 else -1)
        pts = [[x + math.cos(rot) * s, y + math.sin(rot) * s], [x + math.cos(rot + 2.2) * s * .7, y + math.sin(rot + 2.2) * s * .7],
               [x + math.cos(rot + 4) * s * .8, y + math.sin(rot + 4) * s * .8]]
        paint(pts, wash='#DDF2FB', washOp=int(230 * (1 - a / .7)), ink=INK, sw=.5)


# S15 35.27–38.99 · paper-cup phone across the dusk hill; the waves reach an empty cup; he yells; the string snaps
def s15(t, lt, dur):
    cam(t, 960, 540, 1.0)
    skyGrad(['#5A4E96', '#D88AA0', '#FFC896'], 900)
    glow(1550, 640, 420, '#FFD08A', .6)
    paint(ellPts(1550, 660, 90, 90, 30), wash='#FFB36B', ink=None)
    hills(700, ['#9A86B8', '#7A6A9E'], t, 's15h')
    flatGround(820, '#8FBF7A', '#6E9F58', key='s15g')
    for i in range(14):
        bx = 60 + i * 140
        inkLine([[bx, 830], [bx - 8, 806]], .6, '#4E7A3A', 'inkfine', 0)
    x, y, u = 380, 830, 34
    keys = [[0, 'determined'], [ek(78), 'excited', {'mouth': 'open', 'emote': None}], [ek(80), 'hopeful', {'mouth': 'flat'}],
            [ek(81), 'angry', {'mouth': 'wail', 'emote': None}], [ek(83), 'surprised', {'emote': None}]]
    o = heO(t, keys, view='q')
    lift = landK(t, 77, .16)
    o['aR'] = .2 + 1.15 * lift
    o['aL'] = .2 + 1.15 * lift
    if t >= B[81] - .04 and t < B[83]:
        o['dx'] = (o.get('dx') or 0) + .2 * math.sin(t * 60)
    him(x, y, u, o)
    hx, hy = nearHand(x, y, u, o, 1600)
    cx_, cy_ = hx + 10, hy - 10
    tinCan(cx_, cy_, 1.4, rot=-.25 * lift, key='s15c1')
    handDot(hx, hy, PAL['clay'], 10)
    far = (1580, 812)
    jumpK = math.sin(clamp((t - (B[80] - .06)) / .3) * math.pi) if t >= B[80] - .06 else 0
    tinCan(far[0], far[1] - 40 * jumpK, 1.4, rot=math.pi + .35, key='s15c2')
    # the string: sag line; a bump travels k79->k80; wild vibration on k82; snaps on k83
    p0 = (cx_ + 4, cy_ + 2)
    p1 = (far[0] + 2, far[1] - 4 - 40 * jumpK)
    snapped = t >= B[83] - .04
    bump = clamp((t - (B[79] - .1)) / (B[80] - B[79]))
    vib = landK(t, 82, .08) * (1 - snapped)
    pts = []
    N = 40
    for i in range(N + 1):
        f = i / N
        xx = lerp(p0[0], p1[0], f)
        yy = lerp(p0[1], p1[1], f) + 60 * math.sin(f * math.pi) * (1 - lift * .7)
        if 0 < bump < 1:
            yy -= 90 * math.exp(-((f - bump) / .05) ** 2)
        yy += vib * 26 * math.sin(f * 40 + t * 70) * math.sin(f * math.pi)
        pts.append([xx, yy])
    if not snapped:
        inkLine(pts, 1.2, '#F3EBDC', 'ink', .5)
        if 0 < bump < 1:
            pp = pts[int(bump * N)]
            glow(pp[0], pp[1], 70, '#FF8FB0', .9)
            G.c.drawCircle(pp[0], pp[1], 14, _pa('#FF6F96'))
    else:
        a = t - (B[83] - .04)
        half = N // 2
        L = [[p[0], p[1] + 260 * clamp(a * 3) * ((i / half) ** 2)] for i, p in enumerate(pts[:half])]
        R_ = [[p[0], p[1] + 260 * clamp(a * 3) * (((N - half - i) / (N - half)) ** 2)] for i, p in enumerate(pts[half:])]
        inkLine(L, 1.2, '#F3EBDC', 'ink', .5)
        inkLine(R_, 1.2, '#F3EBDC', 'ink', .5)
        stamp('啪', pts[half][0], pts[half][1] - 120, 110, '#FFFFFF', bage(t, 83), rot=-.12)
        impactLines(pts[half][0], pts[half][1], 60, 150, 10, t, '#FFFFFF', 's15imp')
    if t >= B[78] - .04:
        n = 3 if t < B[81] - .04 else 5
        wa = 1 if t < B[83] - .04 else 1 - seg(t, B[83], B[83] + .2)
        soundWaves(cx_ + 60, cy_, -.2, n, 40 + 20 * frac(t * 3), 34, a=.85 * wa, col='#FFFFFF', sw=1.2 if n == 3 else 1.6)
    if t >= B[78] - .04 and t < B[81] - .04:
        bubble(x + 120, y - 13 * u, '喂——', 52, tail=(x + 60, y - 9 * u), k=clamp((t - (B[78] - .04)) / .14), key='s15b')
    if t >= B[81] - .04 and t < B[83] - .04:
        bubble(x + 160, y - 13.4 * u, '示例歌词！！', 58, tail=(x + 60, y - 9 * u), k=clamp((t - (B[81] - .04)) / .12), key='s15b2',
               col='#FFE7EF', tcol='#D8394E')
    if t >= B[80] - .04:
        bubble(far[0], far[1] - 210, '…', 48, tail=(far[0], far[1] - 80), k=clamp((t - (B[80] - .04)) / .14), key='s15b3')
    shards(t, B[76], 960, 500)
    camEnd()


# S16 38.99–42.70 · memory: chili, lemon, a marshmallow plop into her coffee; she loves it; he gapes; 「谜」 card; wink
def s16(t, lt, dur):
    cam(t, 1100, 560, 1.18)
    lay = corner(t, 'day', key='cn16')
    u = U_WIDE + 2
    kM = [[0, 'neutral', {'lookX': 1}], [ek(89), 'surprised', {'emote': None}]]
    oM = heO(t, kM, view='q')
    him(LAY['he'] + 60, GY, u, oM)
    sx = LAY['she']
    kH = [[0, 'happy'], [ek(88), 'love'], [ek(91), 'playful']]
    oH = sheO(t, kH, view='q', flip=True, aL=.2, aR=.2)
    sip = landK(t, 88, .16) * (1 - seg(t, B[89], B[89] + .3))
    oH['aL'] = .45 + .45 * sip
    her(sx, GY, u, oH)
    hx, hy = nearHand(sx, GY, u, oH, LAY['table'])
    hx -= 6
    cy_ = hy + 24
    cup(hx, cy_, .55, fill=1, key='s16cup', saucer=False, steam=.7, t=t, rot=.45 * sip)
    handDot(hx + 8, cy_ - 16, HER['col'], 10)
    # items dropping into the cup
    for i, (k, fn) in enumerate([(85, chili), (86, lemon), (87, marshmallow)]):
        a = t - (B[k] - .24)
        if 0 <= a < .24:
            px, py = hx + 6 + (1 - a / .24) * 120 * (1 if i % 2 else -1), lerp(cy_ - 420, cy_ - 50, (a / .24) ** 2)
            fn(px, py, 26, rot=a * 10)
        elif a >= .24:
            if a < .3:
                fn(hx + 6, cy_ - 50 + 20 * (a - .24) / .06, 26, 0)
            splash(hx + 6, cy_ - 50, a - .24, .8, COFFEE)
            if a < .6:
                stamp('扑通', hx + 6 + (i - 1) * 140, cy_ - 230 - i * 30, 46, '#FFFFFF', a - .24, rot=.1 * (i - 1), life=.4)
    # leftovers sticking out of the cup after they land
    if t >= B[85]:
        chili(hx - 4, cy_ - 46, 18, rot=-.8)
    if t >= B[86]:
        lemon(hx + 22, cy_ - 48, 16)
    if t >= B[87]:
        marshmallow(hx + 2, cy_ - 54, 14, .3)
    if t >= B[88] - .04:
        floatHearts(t, 23, 5, sx - 120, GY - 520, sx + 140, GY - 320, 18)
    if t >= B[89] - .04:
        stamp('？？', LAY['he'] + 60 + 1.5 * u, GY - 11 * u, 80, '#FFFFFF', bage(t, 89), rot=-.1)
    if t >= B[90] - .1:
        k = backOut(clamp((t - (B[90] - .1)) / .14))
        push()
        translate(1340, 250 - 300 * (1 - k))
        rotate(-.06)
        boilSeed('s16card')
        paint(rrPts(-120, -120, 240, 240, 20), wash='#FFFDF6', fill='#F2E6D6', fillOp=50, ink=INK, sw=1.4)
        text('谜', 0, 0, 150, '#7B5CA8', face=WENKAI, shadow=False)
        text('？', 92, -86, 60, HOT, shadow=False)
        pop()
    memory(.8)
    camEnd()


# S17 42.70–46.41 · the rain washes HIM out of the chalk drawing, beat by beat; only she and half a heart remain
def s17(t, lt, dur):
    cam(t, 960, 520, 1.0)
    dark = .4 * landK(t, 93, .3)
    nightBg(t, 's17', lamp_=.6)
    cart(t, 1760, GY, 1.0, .9, key='s17cart', lit=.5)
    sm = .3 * landK(t, 96, .14) + .3 * landK(t, 97, .14) + .4 * landK(t, 98, .14)

    def inner(bx, by, bw, bh):
        cx = bx + bw / 2
        chalkCouple(cx, by + bh * .72, 1.9, 1.0, 1.0, 1.0, smear=sm, t=t)
        if t >= B[99] - .04:       # half the heart is gone with him
            G.c.save()
            G.c.clipRect(skia.Rect.MakeXYWH(bx, by, bw / 2, bh))
            flatRect(bx, by + 40, bw / 2, bh * .5, BOARD)
            G.c.restore()
            hy0 = by + bh * .72 - 110 * 1.9
            jag = [[cx, hy0 - 40], [cx - 12, hy0 - 14], [cx + 10, hy0 + 8], [cx - 10, hy0 + 32], [cx + 6, hy0 + 56]]
            chalkLine(jag, 1, '#FF8FB0', 1.0)
        # rain drops hitting the board
        if t >= B[94] - .04:
            for i in range(10 if t < B[95] - .04 else 22):
                ph = frac(t * 1.7 + hash1(i * 3.1))
                G.c.drawLine(bx + bw * hash1(i * 7.7), by + bh * ph, bx + bw * hash1(i * 7.7), by + bh * ph + 30,
                             skia.Paint(AntiAlias=True, Color=skcol('#DCE6FF', .5), StrokeWidth=3))
    aBoard(860, GY + 60, 1.55, 's17ab', .3, inner=inner)
    if dark > 0:
        tint('#3A4466', dark, skia.BlendMode.kMultiply)
    ck = clamp((t - (B[93] - .3)) / .3)
    if ck > 0:
        for i in range(4):
            puff(lerp(-300, 520, easeOut(ck)) + i * 300, 110 + 30 * (i % 2) + 18 * hitK(t, 93, .1), 40, '#8E93A8', key=f's17cl{i}', a=.95)
    if t >= B[94] - .04:
        ra = .45 if t < B[95] - .04 else .8
        rain(t, 5, 90 if t < B[95] - .04 else 200, -100, 0, W + 200, H, col='#DCE6FF', a=ra)
    if t >= B[98] - .04 and t < B[99]:
        stamp('洗掉了', 1340, 300, 72, '#DCE6FF', bage(t, 98), rot=.08)
    camEnd()


def deskSet(x, top, key='dk'):
    """a small wooden desk seen from the front, (x, top) = centre of the top"""
    boilSeed(key)
    for sx in (-1, 1):
        paint(rectPts(x + sx * 190 - 10, top + 10, 20, 840 + 60 - top), wash=WOODDK, ink=INK, sw=.8)
    paint(rectPts(x - 220, top, 440, 26, 3), wash=WOOD, fill=WOODDK, fillOp=50, ink=INK, sw=1.0)
    paint(rectPts(x - 190, top + 26, 380, 70, 3), wash=mixCol(WOOD, INK, .1), ink=INK, sw=.8)
    G.c.drawCircle(x, top + 61, 8, _pa('#F2C53D'))


def roomWall(t, key='rw'):
    from props_bingbian import wallpaper as wp, woodFloor as wf
    wp('#2F3358', '#383E68', key=key + 'wp')
    wallClock2(1500, 230, 58, 2, 10, night=1, key=key + 'wc')
    calendar11(400, 170, .9, key=key + 'cal')
    wallFrames(960, 260, .8, night=1, key=key + 'wfr')
    stringLights(t, 160, 1760, 120, sag=50, n=18, key=key + 'sl', on=1)
    wf(900, col='#5A4E66', dk='#3E3550', key=key + 'fl')
    plant(1800, 960, .95, night=1, key=key + 'plant')


# S18 46.41–50.13 · he sings into a recorder; the notes loop round and dive into the music box; lid shuts; a heart lock
def s18(t, lt, dur):
    cam(t, 1000, 600, 1.12)
    roomWall(t, 's18')
    top = 700
    deskSet(1180, top, 's18dk')
    glow(1180, top - 120, 360, '#FFE2A0', .35)
    x, y, u = 680, 900, 34
    keys = [[0, 'determined'], [ek(101), 'happy', {'mouth': 'open', 'eyes': 'closed'}], [ek(106), 'surprised', {'emote': None}], [ek(107), 'proud']]
    o = heO(t, keys, view='q')
    him(x, y, u, o)
    rec = 1.0 if t >= B[100] - .04 else 0.0
    recorder(1040, top, 110, rec=rec, t=t, key='s18rec')
    if rec and t < B[100] + .4:
        glow(1100, top - 22, 60, '#FF3B4E', .8 * (1 - seg(t, B[100], B[100] + .4)))
    lid = landK(t, 103, .16) * (1 - landK(t, 106, .1))
    lockK = clamp((t - (B[107] - .045)) / .16)
    mbx, mby = 1300, top
    musicBox(mbx, mby, .9, lid=lid, glowK=.6 * lid, lock=lockK, key='s18mb', t=t)
    for kd in (104, 105):
        if 0 <= t - (B[kd] - .04) < .3:
            glow(mbx, mby - 60, 120, '#FFE7A0', 1 - (t - (B[kd] - .04)) / .3)
            sparkle(mbx + 40, mby - 90, 22 * (1 - (t - B[kd]) / .3), '#FFFFFF', 1)
    if t >= B[106] - .04 and t < B[107]:
        stamp('咔', mbx, mby - 200, 70, '#FFE7A0', bage(t, 106), rot=.1)
    # notes: out of his mouth (k101), loop (k102), into the box (k104/k105)
    mx, my = x + 5.8 * u, y - 4.6 * u
    for i in range(8):
        start = B[101] + i * .12
        if t < start - .04:
            continue
        a = t - start
        loopC = (1000, 360)
        ang = a * 4.5 + i * .8
        px = lerp(mx, loopC[0] + math.cos(ang) * 170, clamp(a / .45))
        py = lerp(my, loopC[1] + math.sin(ang) * 90, clamp(a / .45))
        kd = 104 if i < 4 else 105
        dive = clamp((t - (B[kd] - .25)) / .35)
        px, py = lerp(px, mbx, dive), lerp(py, mby - 50, dive)
        if dive >= 1 or (lid < .2 and dive > .5):
            continue
        s_ = 30 * (1 - .6 * dive)
        noteGlyph(px, py, s_, ['#FF6F96', '#FFB347', '#7FB8E6', '#8FD18A'][i % 4], rot=.2 * math.sin(t * 4 + i), key=f's18n{i}', double=i % 3 == 1)
    camEnd()


def rainStreet(t, grey=.5, key='rs'):
    shopStreet(t, key=key, ground=GY, dusk=0.0, grey=grey)


# S19 50.13–53.84 · far away, heavy rain; she hugs the music box; notes build an umbrella; thunder, splash, she smiles
def s19(t, lt, dur):
    xh = lerp(760, 1060, ease(clamp(lt / dur)))
    cam(t, xh + 60, 540, 1.15)
    rainStreet(t, .55, 's19st')
    tint('#5A6A8E', .35, skia.BlendMode.kMultiply)
    u = 34
    keys = [[0, 'sad'], [ek(109), 'hopeful'], [ek(112), 'scared', {'emote': None}], [ek(113), 'hopeful'], [ek(115), 'happy']]
    o = sheO(t, keys, view='q', flip=False, aL=.35, aR=.35)
    o.update(move('walk', t))
    o['aL'], o['aR'] = .35, .35
    her(xh, GY, u, o)
    bx, by = xh + 1.4 * u, GY - 1.25 * u
    gk = landK(t, 109, .16)
    musicBox(bx, by, .42, lid=.25 * landK(t, 110, .16), glowK=gk, key='s19mb', t=t)
    handDot(bx - 40, by - 18, HER['col'], 9)
    handDot(bx + 40, by - 18, HER['col'], 9)
    # notes rising (k110) and forming the umbrella (k111)
    umbK = landK(t, 111, .16)
    if t >= B[110] - .2:
        for i in range(7):
            a = t - (B[110] - .2) - i * .03
            if a < 0:
                continue
            ang = math.pi + (i + .5) / 7 * math.pi
            tx, ty = xh + math.cos(ang) * 6.5 * u, GY - 11 * u + math.sin(ang) * 2.6 * u
            sx0 = xh + (-1 if i < 3.5 else 1) * 7.2 * u
            f_ = clamp(a / .35)
            px = lerp(lerp(bx, sx0, clamp(f_ * 2)), tx, clamp(f_ * 2 - 1))
            py = lerp(lerp(by - 40, by - 60, clamp(f_ * 2)), ty, clamp(f_ * 2 - 1))
            noteGlyph(px, py, 26, ['#FFE36E', '#FFB3C6', '#BFE6F7'][i % 3], key=f's19n{i}')
    if umbK > 0:
        G.c.saveLayerAlpha(None, int(200 * umbK))
        from props import umbrellaAt
        umbrellaAt(xh, GY - 3 * u, 6.8 * u, col='#FFE7A0', k=umbK, key='s19umb', handle=False, dots=False)
        G.c.restore()
        glow(xh, GY - 11 * u, 260, '#FFE7A0', .35 * umbK)
    # rain everywhere except under the umbrella
    G.c.save()
    if umbK > .5:
        p = skia.Path()
        p.addRect(skia.Rect.MakeXYWH(-500, -500, W + 1000, H + 1000))
        p.addRect(skia.Rect.MakeXYWH(xh - 6.6 * u, GY - 11 * u, 13.2 * u, 11 * u + 40))
        p.setFillType(skia.PathFillType.kEvenOdd)
        G.c.clipPath(p, skia.ClipOp.kIntersect, True)
    rain(t, 9, 220, -200, -100, W + 300, H, col='#DCE6FF', a=.75)
    G.c.restore()
    if t >= B[114] - .04 and umbK > .5:
        for i in range(6):
            ang = math.pi + (i + .5) / 6 * math.pi
            px, py = xh + math.cos(ang) * 6.6 * u, GY - 9.2 * u + math.sin(ang) * 2.4 * u
            a = frac(t * 2 + i * .3)
            G.c.drawCircle(px + math.cos(ang) * 60 * a, py - 40 * a + 80 * a * a, 11, _pa('#DCE6FF', 1 - a))
            if a < .3:
                sparkle(px, py - 6, 16 * (1 - a / .3), '#FFFFFF', 1)
    if t >= B[112] - .04:
        a = t - (B[112] - .04)
        if a < .25:
            flash(.3 * (1 - a / .25))
        from props_bingbian import bolt as bbolt
        if a < .3:
            bbolt(1500 + (xh - 900), -20, 1380 + (xh - 900), 420, key='s19bolt', w=1.4)
    splashDrops(xh + 40, GY, t - (B[113] - .04), 14, 1.4)
    if t >= B[115] - .04:
        floatHearts(t, 41, 4, xh - 160, GY - 9 * u, xh + 160, GY - 5 * u, 16)
    camEnd()


# S20 53.84–57.55 · the notes become little guardians; the rain stops; rainbow, sun; a 「约定」 card gets a heart stamp
def s20(t, lt, dur):
    cam(t, 1000, 540, 1.1)
    clear = landK(t, 120, .3)
    rainStreet(t, .55 * (1 - clear), 's20st')
    tint('#5A6A8E', .35 * (1 - clear), skia.BlendMode.kMultiply)
    if t >= B[121] - .04:
        k = clamp((t - (B[121] - .04)) / .3)
        for i in range(9):
            a = -math.pi / 2 + (i - 4) * .18
            G.c.drawLine(1700, -100, 1700 + math.cos(a + math.pi / 2 + .6) * 1600, -100 + math.sin(a + math.pi / 2 + .6) * 1600,
                         skia.Paint(AntiAlias=True, Color=skcol('#FFF2C8', .34 * k), StrokeWidth=70))
        sk_ = backOut(k)
        glow(1700, 40, 380 * sk_, '#FFE7A0', .9)
        paint(ellPts(1700, 40, 110 * sk_, 110 * sk_, 30), wash='#FFD23A', ink=INK, sw=1.0)
    rb = landK(t, 119, .3)
    if rb > 0:
        cols = ['#E8574A', '#F2A65A', '#F2D45A', '#7CC36B', '#5BA8E0', '#8A6AC8']
        for i, c_ in enumerate(cols):
            r = 1040 - i * 34
            p = skia.Path()
            p.addArc(skia.Rect.MakeXYWH(1000 - r, 1180 - r, 2 * r, 2 * r), 180, 180 * rb)
            G.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol(c_, .42), Style=skia.Paint.kStroke_Style, StrokeWidth=34))
    x, u = 1000, 34
    if t < B[116] + .25:
        ua = 1 - seg(t, B[116], B[116] + .25)
        G.c.saveLayerAlpha(None, int(200 * ua))
        from props import umbrellaAt
        umbrellaAt(x, GY - 3 * u, 6.8 * u, col='#FFE7A0', k=1, key='s19umb', handle=False, dots=False)
        G.c.restore()
    keys = [[0, 'hopeful'], [ek(118), 'starstruck'], [ek(121), 'happy'], [ek(123), 'love']]
    o = sheO(t, keys, view='front', flip=False, aL=.35, aR=.35)
    her(x, GY, u, o)
    bx, by = x, GY - 1.25 * u
    musicBox(bx, by, .42, lid=.3, glowK=.8, key='s20mb', t=t)
    handDot(bx - 40, by - 18, HER['col'], 9)
    handDot(bx + 40, by - 18, HER['col'], 9)
    if clamp(1 - clear) > 0:
        G.c.saveLayerAlpha(None, int(255 * (1 - clear)))
        p = skia.Path()
        p.addRect(skia.Rect.MakeXYWH(-500, -500, W + 1000, H + 1000))
        p.addCircle(x, GY - 6 * u, 330)
        p.setFillType(skia.PathFillType.kEvenOdd)
        G.c.save()
        G.c.clipPath(p, skia.ClipOp.kIntersect, True)
        rain(t, 9, 200, -200, -100, W + 300, H, col='#DCE6FF', a=.7)
        G.c.restore()
        G.c.restore()
    # guardian notes circling (k116); one bonks a raindrop (k117); one turns into a star (k118)
    for i in range(6):
        ang = (t - B[116]) * 2.6 + i / 6 * TAU
        r = 300 * popK(t, 116, .2)
        px, py = x + math.cos(ang) * r, GY - 6 * u + math.sin(ang) * r * .45
        if i in (0, 2, 4) and t >= B[118] - .045:
            sk2 = backOut(clamp((t - (B[118] - .045)) / .14))
            glow(px, py, 70 * sk2, '#FFE36E', .7)
            paint(starPts(px, py, 30 * sk2, .45, 5), wash='#FFE36E', ink=INK, sw=.8)
            continue
        noteGlyph(px, py, 26, ['#FFE36E', '#FFB3C6', '#BFE6F7'][i % 3], rot=.2 * math.sin(t * 5 + i), key=f's20n{i}')
        if i == 0 or i == 3:
            G.c.drawCircle(px - 10, py - 16, 3, _pa(INK))
    if t >= B[117] - .04 and t < B[117] + .4:
        a = t - (B[117] - .04)
        bx_, by_ = x + 240, GY - 9 * u
        for j in range(6):
            ang = j / 6 * TAU
            G.c.drawCircle(bx_ + math.cos(ang) * 60 * a / .4, by_ + math.sin(ang) * 60 * a / .4, 6 * (1 - a / .4), _pa('#DCE6FF'))
        stamp('叮', bx_ + 40, by_ - 70, 50, '#FFE36E', a, rot=.1)
    # the promise card
    ck = landK(t, 122, .3)
    if ck > 0:
        cx_, cy_ = 1460, lerp(-200, 330, ease(ck))
        push()
        translate(cx_, cy_)
        rotate(.08 * math.sin(t * 2))
        boilSeed('s20card')
        paint(rrPts(-150, -100, 300, 200, 14), wash='#FFFDF6', fill='#F2E6D6', fillOp=40, ink=INK, sw=1.2)
        text('约定', 0, -30, 70, '#B04A2E', face=WENKAI, shadow=False)
        line(-100, 40, 100, 40, '#C9C1D6', 1, 3)
        pop()
        if t >= B[123] - .045:
            sk = clamp((t - (B[123] - .045)) / .1)
            paint(heartPts(cx_ + 90, cy_ + 55, 40 * lerp(1.8, 1, easeIn(sk)), 20), wash='#E8392E', washOp=int(220 * sk), ink=None)
    camEnd()


# S21 57.55–59.41 · the film wraps: film frame slides in, clapper pops, claps, 「杀青」 stamp, edges burn
def s21(t, lt, dur):
    cam(t, 960, 560, 1.15)
    corner(t, 'night', lights=.4, key='cn21')
    oM = heO(t, [[0, 'sad']], view='q')
    him(LAY['he'], GY, U_WIDE + 2, oM)
    camEnd()
    tint('#C8A070', .35, skia.BlendMode.kMultiply)
    filmBorder(clamp((t - (B[124] - .2)) / .2) if t > B[124] - .2 else 0, burn=.85 * landK(t, 127, .3))
    bk = landK(t, 127, .2)
    if bk > 0:
        for i in range(10):
            side = -1 if i % 2 else 1
            bx_ = (130 if side < 0 else W - 130) + side * -40 * hash1(i)
            by_ = 80 + i * 100 + 30 * hash1(i * 3)
            r_ = (60 + 70 * hash1(i * 7)) * bk
            G.c.drawCircle(bx_, by_, r_, skia.Paint(AntiAlias=True, Color=skcol('#1A0C04', .85)))
            G.c.drawCircle(bx_, by_, r_ * 1.15, skia.Paint(AntiAlias=True, Color=skcol('#8A3A10', .35), Style=skia.Paint.kStroke_Style, StrokeWidth=8))
    ck = popK(t, 125, .16)
    if ck > 0:
        push()
        translate(480, 470)
        scale(ck)
        clapper(-120, 80, 1.2, openA=.5 * (1 - landK(t, 126, .06)), key='s21clp', txt='第 99 场')
        pop()
    if t >= B[126] - .04 and t < B[127]:
        stamp('啪！', 760, 230, 90, '#FFFFFF', bage(t, 126), rot=-.1)
    if t >= B[127] - .04:
        stamp('杀青', 1250, 470, 190, '#E8392E', bage(t, 127), rot=-.12, stroke='#FFFFFF')


def parkBg(t, key='pk'):
    skyGrad(['#8ECFF0', '#CFEAF7', '#FFF6DE'])
    for i, (cx, cy, s) in enumerate([(300, 140, 26), (1100, 100, 20), (1700, 160, 24)]):
        puff(cx + 10 * math.sin(t * .4 + i), cy, s, '#FFFFFF', key=f'{key}cl{i}', a=.95)
    hills(640, ['#A8D890', '#8CC874'], t, key + 'h')
    flatGround(840, '#9ED184', '#7CB866', key=key + 'g')
    tree(180, 840, 80, key=key + 't1')
    tree(1760, 840, 70, key=key + 't2', col='#8DCB72')
    for i in range(8):
        bloom(300 + i * 190, 900 + 10 * (i % 2), 12, 1, col=['#FFFFFF', '#FFB3C6', '#FFE36E'][i % 3], key=f'{key}fl{i}', stem=False)


# S22 59.41–61.27 · she opens the music box: a little orange him rises and twirls; notes and hearts
def s22(t, lt, dur):
    cam(t, 1000, 560, 1.15)
    parkBg(t, 's22')
    top = 660
    boilSeed('s22tab')
    paint(rectPts(850, top + 20, 20, 840 - top), wash='#6B4A33', ink=INK, sw=.8)
    paint(ellPts(860, 850, 70, 12, 16), wash='#4A3A30', ink=INK, sw=.6)
    paint(ellPts(860, top + 10, 170, 26, 24), wash='#FFFDF6', fill='#F7C6D2', fillOp=60, ink=INK, sw=1.0)
    lid = landK(t, 128, .14)
    rise = landK(t, 129, .2)

    def fig(fx, fy, k):
        if rise <= .02:
            return
        spin = seg(t, B[130] - .1, B[130] + .4)
        views = ['front', 'q', 'side', 'qback', 'back', 'qback', 'side', 'q', 'front']
        v = views[min(len(views) - 1, int(spin * (len(views) - 1) + .5))] if 0 < spin < 1 else 'front'
        flipv = .25 < spin < .75
        paint(rectPts(fx - 3, fy - 80 * rise, 6, 80 * rise), wash='#F2C53D', ink=INK, sw=.4)
        him(fx, fy - 80 * rise, 15, dict(view=v, flip=flipv, eyes='happy', mouth='smile', blush=.5, boilKey='s22fig', noShadow=True,
                                        aL=1.2, aR=1.2))
    musicBox(860, top, 1.1, lid=lid, glowK=.5 * lid, key='s22mb', figure=fig, t=t)
    x, u = 1180, 34
    keys = [[0, 'hopeful'], [ek(129), 'surprised', {'emote': None}], [ek(131), 'laugh', {'blush': 1.0}]]
    o = sheO(t, keys, view='q', flip=True)
    her(x, 840, u, o)
    if t >= B[131] - .045:
        pts = []
        for i in range(6):
            a = t - (B[131] - .045)
            pts.append((860 + (i - 2.5) * 90 + 30 * math.sin(t * 3 + i), top - 330 - 200 * clamp(a * 1.5) * (.5 + .5 * hash1(i))))
        notes(t, 22, pts, 26)
        floatHearts(t, 22, 6, 640, 120, 1400, 380, 20)
    camEnd()


# S23 61.27–63.12 · he chalks her portrait on the A-board, one stroke group a beat, then steps back proud
def s23(t, lt, dur):
    cam(t, 1100, 560, 1.2)
    nightBg(t, 's23')
    cart(t, 420, GY, .85, .9, key='s23cart', lit=1)
    stringLights(t, 420 + 175, 1860 - 97, GY - 520, sag=50, n=10, key='s23sl', on=1)
    bxc = 1060

    def inner(bx, by, bw, bh):
        cx, cy = bx + bw / 2, by + bh * .72
        s = 1.25
        body = [[cx - 70 * s, cy], [cx - 70 * s, cy - 100 * s], [cx + 70 * s, cy - 100 * s], [cx + 70 * s, cy], [cx - 70 * s, cy]]
        chalkLine(body, writeK(t, 132, .26), '#FFB3C6', 1.3)
        for lx in (-44, -16, 16, 44):
            chalkLine([[cx + lx * s, cy], [cx + lx * s, cy + 26 * s]], writeK(t, 132, .26), '#FFB3C6', 1.1)
        fk = writeK(t, 133, .2)
        if fk > 0:
            for i in range(5):
                ang = i / 5 * TAU
                G.c.drawCircle(cx + 30 * s + math.cos(ang) * 14 * s, cy - 116 * s + math.sin(ang) * 14 * s, 9 * s * fk, _pa('#FFFFFF', .9))
            G.c.drawCircle(cx + 30 * s, cy - 116 * s, 6 * s * fk, _pa('#FFE36E', .9))
        fc = writeK(t, 134, .2)
        if fc > 0:
            for ex in (-24, 24):
                chalkLine([[cx + (ex - 10) * s, cy - 58 * s], [cx + ex * s, cy - 66 * s], [cx + (ex + 10) * s, cy - 58 * s]], fc, CHALK, 1.0)
            chalkLine([[cx - 14 * s, cy - 36 * s], [cx, cy - 26 * s], [cx + 14 * s, cy - 36 * s]], fc, '#FF8FB0', 1.0)
        hk = writeK(t, 135, .22)
        for i in range(7):
            ang = -math.pi + i / 6 * math.pi
            hp = heartPts(cx + math.cos(ang) * 150 * s, cy - 50 * s + math.sin(ang) * 130 * s, 16, 16)
            chalkLine(hp + [hp[0]], clamp(hk * 7 - i), '#FF8FB0', .8)
    aBoard(bxc, GY + 30, 1.3, 's23ab', .6, inner=inner)
    x, u = 1440, 34
    keys = [[0, 'determined'], [ek(134), 'happy'], [ek(135), 'proud']]
    o = heO(t, keys, view='q', flip=True, aL=1.0 - .7 * landK(t, 135, .16), aR=.2)
    back = 80 * landK(t, 135, .16)
    him(x + back, GY, u, o)
    hx, hy = nearHand(x + back, GY, u, o, bxc)
    if t < B[135]:
        a = 0 if t < B[132] - .24 else frac((t - B[132]) * 2.15)
        paint(rrPts(hx - 30 - 10 * math.sin(a * TAU), hy - 8, 30, 12, 4), wash='#FFFDF6', ink=INK, sw=.5)
        handDot(hx, hy, PAL['clay'], 9)
    camEnd()


# S24 63.12–64.98 · a crate stage by the cart: spotlight, he grabs the mic, notes burst; on the stop the light narrows
def s24(t, lt, dur):
    cam(t, 960, 560, 1.15)
    flatRect(-300, -300, W + 600, H + 600, '#1A1630')
    starField(t, 9, 40, 0, 0, W, 500, r=2.4)
    boilSeed('s24crate')
    paint(rectPts(560, GY - 70, 800, 70 + 200, 3), wash=WOOD, fill=WOODDK, fillOp=60, ink=INK, sw=1.2)
    for i in range(1, 5):
        line(560 + i * 160, GY - 66, 560 + i * 160, GY + 120, WOODDK, 1, 3)
    on = popK(t, 136, .12)
    narrow = landK(t, 139, .16)
    spotlight(900, -60, GY - 70, lerp(680, 330, narrow), on, '#FFF2C8')
    if t < B[139] - .04:
        darkness(.0, ())
    x, y, u = 860, GY - 70, 34
    keys = [[0, 'neutral'], [ek(137), 'cool', {'emote': None}], [ek(138), 'happy', {'mouth': 'open', 'eyes': 'closed'}], [ek(139), 'love', {'tint': None}]]
    o = heO(t, keys, view='q')
    grab = landK(t, 137, .16)
    o['aR'] = .2 + .9 * grab
    o['aL'] = .2 + .9 * grab
    micX = x + 6.2 * u
    him(x, y, u, o)
    micStand(micX, y, .44, 's24mic', head=2.0)
    if grab > .5:
        hx, hy = nearHand(x, y, u, o, micX)
        handDot(micX - 10, y - 150, PAL['clay'], 10)
    if t >= B[138] - .045:
        a = t - (B[138] - .045)
        rr_ = 160 + 380 * easeOut(clamp(a / .5))
        pts = [(micX + 60 + math.cos(-2.6 + i / 7 * 2.9) * rr_, min(870, y - 260 + math.sin(-2.6 + i / 7 * 2.9) * rr_ * .7)) for i in range(8)]
        notes(t, 24, pts, 30)
    if t >= B[139] - .04:
        tint('#000000', .35 * narrow, skia.BlendMode.kMultiply)
    camEnd()


# S25 64.98–66.84 · dream: she on a cloud, a ring of flowers bursts, she twirls, petals rain, a rainbow arcs
def s25(t, lt, dur):
    cam(t, 960, 560, 1.0)
    gradRect(-300, -300, W + 600, H + 600, ['#B9A2E8', '#F2B8D8', '#FFE2EA'])
    starField(t, 13, 40, 0, 0, W, 600, r=3)
    rb = landK(t, 143, .3)
    if rb > 0:
        cols = ['#FF8FA0', '#FFC28A', '#FFF0A0', '#B8E8A0', '#A0D8F0', '#C8B0F0']
        for i, c_ in enumerate(cols):
            r = 640 - i * 30
            p = skia.Path()
            p.addArc(skia.Rect.MakeXYWH(960 - r, 820 - r, 2 * r, 2 * r), 180, 180 * rb)
            G.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol(c_, .75), Style=skia.Paint.kStroke_Style, StrokeWidth=30))
    for i, (cx, cy, s) in enumerate([(300, 900, 60), (960, 930, 80), (1640, 900, 64)]):
        puff(cx + 10 * math.sin(t + i), cy, s, '#FFFFFF', key=f's25c{i}', a=1)
    x, u = 960, 36
    spin = seg(t, B[141] - .1, B[141] + .35)
    views = ['front', 'q', 'side', 'qback', 'back', 'qback', 'side', 'q', 'front']
    v = views[min(len(views) - 1, int(spin * (len(views) - 1) + .5))] if 0 < spin < 1 else 'front'
    keys = [[0, 'starstruck'], [ek(142), 'happy'], [ek(143), 'love']]
    o = sheO(t, keys, view=v, flip=.25 < spin < .75)
    addJ(o, jump(t, B[141] - .1, B[141] + .3, 1.4))
    her(x, 870, u, o)
    fk = clamp((t - (B[140] - .045)) / .2)
    for i in range(10):
        ang = i / 10 * TAU - math.pi / 2
        r = 360 * easeOut(fk)
        bloom(x + math.cos(ang) * r, 600 + math.sin(ang) * r * .7, 22, fk, col=['#FFFFFF', '#FFB3C6', '#FFE36E'][i % 3], key=f's25b{i}', stem=False)
    if t >= B[142] - .1:
        petalsFly(t, 5, 40, 0, -50, W, 900, 14)
    sparkles(t, 7, 12, 200, 100, 1700, 800, 16, '#FFFFFF')
    camEnd()


# S26 66.84–68.69 · he sleeps; a dream bubble pops; she waves inside; he smiles in his sleep
def s26(t, lt, dur):
    cam(t, 900, 560, 1.12)
    bedroom(t, hh=2, mm=30, key='bd26', lights=.6)
    x, u = 900, 34
    keys = [[0, 'neutral', {'eyes': 'closed', 'mouth': 'o', 'emote': None}], [ek(147), 'happy', {'eyes': 'closed', 'blush': .9, 'emote': None}]]
    o = heO(t, keys, view='front', apron_=False, noShadow=True, noLegs=True)
    o.update(dy=-.15 * math.sin(t * 2.4), sq=.03 * math.sin(t * 2.4))
    him(x, 880, u, o)
    bedFrontCover('bd26')
    if t >= B[144] - .04:
        for i, ch in enumerate('Zzz'):
            a = frac(t * .6 + i * .3)
            text(ch, x + 160 + i * 40 + 30 * a, 600 - 120 * a - i * 30, 50 - i * 10, '#FFFFFF', shadow=False, a=math.sin(a * math.pi))
    bk = clamp((t - (B[145] - .045)) / .16)
    if bk > 0:
        thoughtCloud(1280, 330, 560, 330, bk, key='s26tc', col='#FFE9F2', tail=(x + 80, 640))
        if t >= B[146] - .045:
            k = backOut(clamp((t - (B[146] - .045)) / .16))
            push()
            translate(1280, 430)
            scale(k)
            o2 = dict(view='front', eyes='happy', mouth='smile', blush=.7, boilKey='s26h', noShadow=True,
                      aL=1.3 + .4 * math.sin(t * 9), aR=.2)
            her(0, 60, 17, o2)
            pop()
    if t >= B[147] - .04:
        floatHearts(t, 26, 5, x - 140, 420, x + 140, 640, 18)
    camEnd()


def cat(x, y, s, key='cat'):
    boilSeed(key)
    paint(ellPts(x, y - 40 * s, 60 * s, 36 * s, 18), wash='#F2A65A', fill='#C87A3A', fillOp=50, ink=INK, sw=.8)
    paint(ellPts(x + 56 * s, y - 70 * s, 32 * s, 28 * s, 16), wash='#F2A65A', ink=INK, sw=.8)
    for ex in (40, 72):
        paint([[x + ex * s - 12 * s, y - 88 * s], [x + ex * s - 4 * s, y - 112 * s], [x + ex * s + 6 * s, y - 92 * s]], wash='#F2A65A', ink=INK, sw=.6)
    for ex in (46, 66):
        G.c.drawCircle(x + ex * s, y - 72 * s, 4 * s, _pa(INK))
    inkLine([[x - 58 * s, y - 40 * s], [x - 90 * s, y - 70 * s], [x - 80 * s, y - 100 * s]], 2.4 * s, '#C87A3A', 'ink', .5)
    for lx in (-30, 30):
        paint(rectPts(x + lx * s - 8 * s, y - 14 * s, 16 * s, 14 * s), wash='#F2A65A', ink=INK, sw=.5)


def poster(x, y, s, key='post'):
    boilSeed(key)
    push()
    translate(x, y)
    rotate(-.05)
    paint(rectPts(-110 * s, -150 * s, 220 * s, 300 * s), wash='#FFFDF6', ink=INK, sw=1.0)
    text('寻', 0, -110 * s, 52 * s, '#D8394E', face=WENKAI, shadow=False)
    gradRect(-80 * s, -76 * s, 160 * s, 130 * s, ['#FFE9F2', '#FFD6E6'])
    her(0, 50 * s, 11 * s, dict(view='front', eyes='happy', mouth='smile', blush=.6, boilKey='postH', noShadow=True))
    line(-70 * s, 84 * s, 70 * s, 84 * s, '#C9C1D6', 1, 3)
    line(-70 * s, 110 * s, 40 * s, 110 * s, '#C9C1D6', 1, 3)
    pop()


# S27 68.69–70.55 · the flashlight search: a bin, a cat, a pink balloon, then a missing poster of her
def s27(t, lt, dur):
    cam(t, 960, 560, 1.05)
    rainStreet(t, .2, 's27st')
    trashcan(320, GY, 52, key='s27tc')
    cat(1320, GY, 1.1, 's27cat')
    balloon(1560, 300, 60, '#FF8FB0', t, key='s27bln')
    poster(640, 420, 1.0, 's27post')
    targets = [(320, GY - 70, 148), (1360, GY - 70, 149), (1560, 300, 150), (640, 420, 151)]
    j = max(0, lastBeat(t, [148, 149, 150, 151]))
    tx, ty, k = targets[j]
    if j > 0:
        px, py, _ = targets[j - 1]
        m = clamp((t - (B[k] - .16)) / .16)
        tx, ty = lerp(px, tx, easeOut(m)), lerp(py, ty, easeOut(m))
    x, u = 960, 32
    flip = tx < x
    keys = [[0, 'determined'], [ek(149), 'neutral', {'eyes': 'wide'}], [ek(150), 'nervous', {'emote': None}], [ek(151), 'surprised', {'emote': '!'}]]
    o = heO(t, keys, view='q', flip=flip, aL=.9, aR=.9)
    hx, hy = nearHand(x, GY, u, o, tx)
    darkness(.72, [(tx, ty, 260, 1.0), (hx, hy, 120, .5)])
    p = skia.Path()
    ang = math.atan2(ty - hy, tx - hx)
    d = math.hypot(tx - hx, ty - hy)
    nx, ny = -math.sin(ang), math.cos(ang)
    p.moveTo(hx + nx * 12, hy + ny * 12)
    p.lineTo(hx - nx * 12, hy - ny * 12)
    p.lineTo(tx - nx * 170, ty - ny * 170)
    p.lineTo(tx + nx * 170, ty + ny * 170)
    p.close()
    G.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol('#FFF2B0', .22)))
    him(x, GY, u, o)
    push()
    translate(hx, hy)
    rotate(ang)
    paint(rrPts(-10, -14, 70, 28, 6), wash='#4A4760', ink=INK, sw=.7)
    paint(rectPts(56, -18, 16, 36), wash='#FFE7A0', ink=INK, sw=.6)
    pop()
    handDot(hx, hy, PAL['clay'], 10)
    for i, (k_, lab) in enumerate([(148, '不是'), (149, '不是'), (150, '不是')]):
        if B[k_] - .04 <= t < B[k_ + 1] - .04:
            px, py, _ = targets[i]
            stamp(lab, px + 60, py - 150, 50, '#FFFFFF', t - B[k_], rot=.1)
    camEnd()
