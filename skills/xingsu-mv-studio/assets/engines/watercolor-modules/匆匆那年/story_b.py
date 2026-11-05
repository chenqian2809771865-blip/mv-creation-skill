# story_b.py: 《匆匆那年》 S04–S22 — verse 1 (how the line started), verse 1B (the account grows), chorus 1 (the carving, the
# letter she suspects, the book wall, the white-out and the one stroke she kept), interlude (the envelope under the desk, he comes).
import math
from eng import *
import eng
from clawd import *
from cc import *
from cc2 import *
from props import bubble, sparkle
from sets2 import seat
from wo import armToward
from hb import thoughtCloud
from wo import scr
from nm import darkness
from common import *


# ================================================================ shared stagings
def seated(who, x, o):
    seat(seatT(who), x, PD_SEAT, U2, o)


def front(t, era, herO, himO, items=None, cam_=(960, 560, 1.0), light=1.0, after=None, back=True, grade=1.0):
    """past classroom from the teacher's side: the two of them seated behind their desk, facing us"""
    def people(t_):
        seated('her', P_HER, herO)
        seated('him', P_HIM, himO)
    pastClass(t, era, people, items, light, cam_, back)
    if after:
        after()
    camEnd()
    pastGrade(grade)


def handDot(x, y, who, u):
    paint(ellPts(x, y, u * .42, u * .42, 10), wash=(ME if who == 'him' else HER)['col'], ink=INK, sw=.6)


def cnt(t, a, b, n0, n1):
    """a stroke count growing from n0 to n1 over [a, b]: (n, progress of the n-th stroke)"""
    v = lerp(n0, n1, seg(t, a, b))
    n = int(math.floor(v))
    k = v - n
    if k < 1e-3:
        return max(n, 0), 1.0
    return n + 1, k


def slide(t, t0, t1, p0, p1, e=ease):
    k = e(seg(t, t0, t1))
    return lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k), k


def seasonTint(k, col):
    if k > .01:
        tint(col, .16 * k, skia.BlendMode.kSoftLight)


# ================================================================ S04 the school gate, autumn 2013: goodbye, and goodbye again
def s04(t, lt, dur):
    cam(t, 960, 560, 1.0)
    gateScene(t, 'dusk', leaves=1.0)
    u = 30
    # her (left) and him (right): wave, walk apart, look back, walk back, walk on together
    phases = [(28.07, 29.30), (29.30, 30.55), (30.55, 31.0), (31.0, 32.25), (32.25, 33.6)]
    if t < 29.30:
        hx, mx = 800, 1150
        wave = 1.15 + .3 * math.sin(t * 11)
        ho = feel('happy', t, dict(view='q', aR=wave, lookX=.5))
        mo = feel('happy', t, dict(view='q', flip=True, aR=wave, lookX=.5))
    elif t < 30.55:
        sh = stroll(t, 29.30, 30.55, 800, 540, u)
        sm = stroll(t, 29.30, 30.55, 1150, 1420, u)
        hx, mx = sh['x'], sm['x']
        ho = feel('neutral', t, dict(view='q', flip=True, walk=sh['walk'], dy=sh['dy']))
        mo = feel('neutral', t, dict(view='q', walk=sm['walk'], dy=sm['dy']))
    elif t < 31.0:
        hx, mx = 540, 1420
        ho = feel('hopeful', t, dict(view='q', lookX=.6))
        mo = feel('hopeful', t, dict(view='q', flip=True, lookX=.6))
    elif t < 32.25:
        sh = stroll(t, 31.0, 32.25, 540, 800, u)
        sm = stroll(t, 31.0, 32.25, 1420, 1150, u)
        hx, mx = sh['x'], sm['x']
        ho = feel('happy', t, dict(view='q', walk=sh['walk'], dy=sh['dy']))
        mo = feel('happy', t, dict(view='q', flip=True, walk=sm['walk'], dy=sm['dy']))
    else:
        sh = stroll(t, 32.25, 34.2, 800, 1060, u)
        sm = stroll(t, 32.25, 34.2, 1150, 1410, u)
        hx, mx = sh['x'], sm['x']
        ho = feel('happy', t, dict(view='q', walk=sh['walk'], dy=sh['dy'], lookX=.6, blush=.4))
        mo = feel('happy', t, dict(view='q', walk=sm['walk'], dy=sm['dy'], lookX=-.2))
    teen('her', hx, GATE_FLOOR, u, ho)
    teen('him', mx, GATE_FLOOR, u, mo)
    for (a, b, x, key) in ((28.25, 29.6, hx - 40, 'bh1'), (28.45, 29.7, mx + 40, 'bm1'), (30.6, 31.3, hx, 'bh2'), (30.7, 31.35, mx, 'bm2')):
        k = ease(seg(t, a, a + .25)) * (1 - ease(seg(t, b - .2, b)))
        txt = '再见！' if a < 30 else '……'
        bubble(x, GATE_FLOOR - 15 * u, txt, 40, (x, GATE_FLOOR - 10 * u), k, key=key)
    camEnd()
    pastGrade(1.0)


# ================================================================ S05 2013: she draws the line
def s05(t, lt, dur):
    cam(t, 960, lerp(600, 560, lt / dur), 1.16)
    prog = ease(seg(t, 33.62, 35.55))
    note = ease(seg(t, 35.65, 36.15))
    x0, y0, x1, y1 = DESK
    deskState(t, old=0.0, line=prog, note=note)
    ruler(LINE_X + 10, y1 - 8, y1 - y0 - 16, -math.pi / 2, a=1 - ease(seg(t, 35.7, 36.2)))
    if 0 < prog < 1:
        penTop(LINE_X, lerp(y1 - 14, y0 + 14, prog), .75, HER_PEN, key='lpen')
    elif prog >= 1:
        penTop(LINE_X - 60, y0 + 120, 1.2, HER_PEN, key='lpen')
    if 35.6 < t < 36.4:
        sparkle(NOTE_XY[0] + 180, NOTE_XY[1] - 40, 26 * (1 - seg(t, 35.9, 36.4)), '#FFFFFF')
    camEnd()
    pastGrade(1.0)


# ================================================================ S06 the first argument: his pencil case is over the line
def s06(t, lt, dur):
    def items():
        x, _, _ = slide(t, 36.6, 37.0, (1080, 0), (930, 0))
        boilSeed('fpcase')
        paint(rrPts(x - 70, PD_TOP - 18 - 26, 140, 30, 12), wash='#3F5FAE', fill='#2A3F80', fillOp=60, ink=INK, sw=.8)
        deskBooks(PD_X0 + 20, 3, 'db1')
        deskBooks(PD_X1 - 100, 3, 'db2')
    ho = feel('angry', t, dict(lookX=.7, aR=lerp(.2, .9, ease(seg(t, 36.8, 37.1)))))
    mo = feel('happy', t, dict(lookX=-.6, eyes='happy', aL=.4 + .2 * math.sin(t * 7)))

    def after():
        bubble(600, 420, '过线了！', 46, (700, 540), ease(seg(t, 36.85, 37.1)), key='b6h')
        bubble(1330, 430, '就一点点！', 46, (1230, 540), ease(seg(t, 37.7, 37.95)), key='b6m')
    front(t, '2013', ho, mo, items, cam_=(960, 640, 1.3), after=after)


# ================================================================ S07 the promise: settle it all on graduation day
def s07(t, lt, dur):
    up = ease(seg(t, 41.9, 42.5))
    a = lerp(.2, 1.35, up)
    ho = feel('determined' if t < 41.8 else 'happy', t, dict(lookX=.6, aR=a, aL=-.2))
    mo = feel('neutral' if t < 41.4 else 'happy', t, dict(lookX=-.6, aL=a, aR=-.2))

    def after():
        bubble(560, 420, '毕业那天 一起算清！', 42, (690, 540), ease(seg(t, 39.6, 39.9)) * (1 - ease(seg(t, 42.6, 42.9))), key='b7h')
        bubble(1330, 430, '好！', 48, (1230, 540), ease(seg(t, 41.3, 41.55)) * (1 - ease(seg(t, 42.6, 42.9))), key='b7m')
        if up > .5:
            hx, hy = handXY(P_HER, PD_SEAT + 2 * U2, U2, ho, 'R')
            mx, my = handXY(P_HIM, PD_SEAT + 2 * U2, U2, mo, 'L')
            handDot(hx, hy, 'her', U2)
            handDot(mx, my, 'him', U2)
            if t > 42.5:
                k = seg(t, 42.5, 43.6)
                sparkle((hx + mx) / 2, (hy + my) / 2 - 20 - 30 * k, 30 * (1 - k) + 8, '#FFE36E')
                sparkle((hx + mx) / 2 - 40 * k, hy - 10 - 50 * k, 18 * (1 - k), '#FFFFFF')
    front(t, '2013', ho, mo, lambda: (deskBooks(PD_X0 + 20, 3, 'db1'), deskBooks(PD_X1 - 100, 3, 'db2')), cam_=(960, 640, 1.3), after=after)


# ================================================================ S08 now: graduation day never came
def presentRoom(t, camv, her_=None, him_=None, door=0.0, inDoor=None, extra=None, board='reunion', grade=1.0):
    cam(t, *camv)
    classroomFront(t, 1.0, False, door, inDoor=inDoor, board=board)
    deskFront(t)
    if door > .01:
        glow(280, 760, 260, '#DDE7FF', .25 * door)
    if him_:
        him_()
    if her_:
        her_()
    if extra:
        extra()
    camEnd()
    presentGrade(grade, vig=.45)
    dustMotes(t, 24, .22, seed=41)


def s08(t, lt, dur):
    o = feel('sad', t, dict(tint=None, view='q', lookX=.6, lookY=.6, aL=-.3, aR=-.5))
    presentRoom(t, (lerp(1080, 1110, lt / dur), 700, lerp(1.4, 1.5, lt / dur)), lambda: herNow(1000, FLOOR, U, o, .5))


# ================================================================ S09 spring 2014: things cross the line, strokes pile up
def s09(t, lt, dur):
    cam(t, lerp(960, 940, lt / dur), 600, lerp(1.24, 1.3, lt / dur))
    nh, kh = cnt(t, 50.9, 56.2, 3, 14)
    nr, kr = cnt(t, 50.9, 56.2, 6, 21)
    deskState(t, old=.05, his=nh, hisK=kh, her=nr, herK=kr, taunts=1.0, petals=1.0, season='spring', graffiti=.15)
    x, y, _ = slide(t, 51.0, 52.1, (1360, 470), (700, 470))
    pencilCase(x, y, .05, '#3F5FAE', key='pc9')
    x, y, _ = slide(t, 52.6, 53.5, (560, 610), (1250, 610))
    boilSeed('er9')
    paint(rrPts(x - 46, y - 26, 92, 52, 10), wash='#F2A9BC', ink=INK, sw=.6)
    x, y, _ = slide(t, 54.2, 55.3, (1400, 380), (760, 380))
    penTop(x, y, -.2, HIS_PEN, key='pn9')
    camEnd()
    pastGrade(1.0)
    seasonTint(1.0, '#FFC6D9')


# ================================================================ S10 winter 2014: the nap — he sleeps over the line, she doesn't count it
def s10(t, lt, dur):
    lean = ease(seg(t, 56.6, 58.2))
    wake = ease(seg(t, 59.0, 59.4))
    smile = t > 59.9
    mo = dict(view='front', eyes='closed', mouth='flat', sq=.1, dy=.3, rot=-.15 * lean, dx=-.4 * lean, aL=-.6, aR=-.6, blush=.3)
    if t < 59.0:
        ho = dict(view='front', eyes='closed', mouth='flat', sq=.1, dy=.3, aL=-.6, aR=-.6)
    else:
        ho = feel('happy' if smile else 'surprised', t, dict(view='front', lookX=.8, aL=-.4, aR=-.4, blush=.7 if smile else .2,
                                                              take=0, emote=None if not smile else 'heart', emoteAge=t - 59.9))
        if not smile:
            ho['take'] = 0
            ho['sq'] = .02

    def after():
        if t < 59.0:
            zzz(t, P_HER - 40, PD_SEAT - 6.4 * U2, 34)
        zzz(t + .4, P_HIM + 20, PD_SEAT - 6.2 * U2, 34)
        if lean > .9:
            G.c.drawLine(LINE_X, 520, LINE_X, PD_TOP - 18, skia.Paint(AntiAlias=True, Color=skcol(LINE_PEN, .35 * (1 - wake * .5)),
                                                                    StrokeWidth=3, PathEffect=skia.DashPathEffect.Make([10, 10], 0)))
    front(t, '2014', ho, mo, lambda: (deskBooks(PD_X0 + 20, 2, 'db1'), deskBooks(PD_X1 - 80, 2, 'db2')),
          cam_=(960, 640, lerp(1.28, 1.36, lt / dur)), after=after, light=.8)
    tint('#CFE0FF', .08, skia.BlendMode.kSoftLight)


# ================================================================ S11 spring 2015: a box of milk — "I crossed, so I treat you"
def s11(t, lt, dur):
    cam(t, 960, 520, lerp(1.36, 1.42, lt / dur))
    landed = t > 63.7
    nr, kr = (34, ease(seg(t, 63.8, 64.25))) if landed else (33, 1.0)
    deskState(t, old=.1, his=25, her=nr, herK=kr, taunts=1.0, graffiti=.25)
    x, y, k = slide(t, 62.2, 63.6, (1420, 430), (650, 440))
    milkBox(x, y, -.08 + .1 * k, key='m11')
    noteText(x + 190, y + 40, 210, ['我过线了', '罚我请你'], rot=.04 + .06 * k, key='mn11', size=30)
    camEnd()
    pastGrade(1.0)
    seasonTint(1.0, '#FFE2B8')


# ================================================================ S12 the account fills up through the seasons; 高三 books pile up
def s12(t, lt, dur):
    cam(t, 960, lerp(560, 580, lt / dur), lerp(1.3, 1.14, ease(lt / dur)))
    nh, kh = cnt(t, 67.4, 72.6, 25, 99)
    nr, kr = cnt(t, 67.4, 72.6, 34, 96)
    deskState(t, old=.15, his=nh, hisK=kh, her=nr, herK=kr, taunts=1.0, books=ease(seg(t, 70.8, 72.8)), graffiti=lerp(.25, .5, seg(t, 67.2, 73.5)))
    x, y, _ = slide(t, 67.4, 68.3, (560, 450), (1240, 450))
    boilSeed('clip12')
    paint(rrPts(x - 44, y - 12, 88, 24, 10), wash='#F2A9BC', fill='#E2476E', fillOp=60, ink=INK, sw=.6)
    G.c.drawCircle(x - 30, y, 14, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .9)))
    x, y, _ = slide(t, 68.9, 69.8, (600, 650), (1280, 650))
    boilSeed('candy12')
    paint(ellPts(x, y, 26, 18, 14), wash='#F7D36E', ink=INK, sw=.6)
    for d in (-1, 1):
        paint([[x + d * 24, y], [x + d * 52, y - 18], [x + d * 52, y + 18]], wash='#F7D36E', ink=INK, sw=.5)
    camEnd()
    pastGrade(1.0)
    ph = seg(t, 67.2, 73.5) * 3
    cols = ['#FFC6D9', '#C8F0B8', '#FFD27A', '#CFE0FF']
    i = min(2, int(ph))
    f = ph - i
    seasonTint(1 - f, cols[i])
    seasonTint(f, cols[i + 1])


# ================================================================ S13 winter 2015: 200 days to the 高考
def s13(t, lt, dur):
    cam(t, 1110, 85, lerp(1.7, 1.78, lt / dur))
    num = 201 if t < 75.6 else 200
    classroomFront(t, 1.0, False, 0.0, board='countdown', num=num)
    if 75.5 < t < 76.0:
        sparkle(1110, 30, 60 * (1 - seg(t, 75.5, 76.0)), '#FFFFFF')
    camEnd()
    pastGrade(1.0)


# ================================================================ S14 chorus 1: a note from the back row — 「你俩是一对吧？」 — both blush
def s14(t, lt, dur):
    blushK = ease(seg(t, 80.2, 81.0))
    ho = feel('shy' if t > 80.2 else 'surprised', t, dict(lookX=-.7, blush=.9 * blushK, take=0))
    mo = feel('shy' if t > 80.4 else 'surprised', t, dict(lookX=.7, blush=.9 * blushK, take=0))
    ho['take'] = mo['take'] = 0

    def items():
        deskBooks(PD_X0 + 20, 4, 'db1')
        deskBooks(PD_X1 - 120, 4, 'db2')
        if t < 79.4:
            k = seg(t, 78.5, 79.3)
            px, py = arcPt((380, 540), (960, PD_TOP - 30), -160, ease(k))
            boilSeed('pball')
            paint(ellPts(px, py, 22, 20, 12, 3), wash='#FBF8F0', ink=INK, sw=.6)

    def after():
        k = ease(seg(t, 79.4, 79.8))
        if k > .01:
            push()
            translate(960, lerp(PD_TOP - 30, 470, k))
            scale(lerp(.2, 1, backOut(k)))
            rotate(-.04)
            boilSeed('tnote')
            paint(rectPts(-190, -60, 380, 120, 2), wash='#FBF8F0', ink=INK, sw=.8)
            for i in range(3):
                G.c.drawLine(-170, -30 + i * 30, 170, -30 + i * 30, skia.Paint(AntiAlias=True, Color=skcol('#C9C4D6', .4), StrokeWidth=2))
            text('你俩是一对吧？', 0, 0, 44, '#2E3A66', face=WENKAI, shadow=False)
            pop()
    front(t, '2015', ho, mo, items, cam_=(960, 640, 1.3), after=after)


# ================================================================ S15 the compass carves 「永远一起」 across the line
def s15(t, lt, dur):
    cam(t, lerp(940, 975, lt / dur), 360, lerp(2.0, 2.15, lt / dur))
    prog = ease(seg(t, 84.5, 88.9))
    deskState(t, old=.18, his=95, her=92, taunts=1.0, carve=prog, books=1.0, graffiti=.5)
    if 0 < prog < 1:
        x, y = carveTip(prog)
        compassTop(x, y, -.55)
        for i in range(4):
            a = frac(t * 4 + i / 4)
            G.c.drawCircle(x + (hash1(i + math.floor(t * 4)) - .5) * 30 * a, y + 6 + 20 * a, 2.4 * (1 - a), skia.Paint(AntiAlias=True, Color=skcol('#FFF6E2', .8)))
    elif prog >= 1:
        compassTop(LINE_X + 260, 470, -.2)
    camEnd()
    pastGrade(1.0)
    if prog >= 1:
        glow(W / 2, H / 2 - 20, 360, '#FFE7B8', .25 * (1 - seg(t, 89.0, 89.5)))


# ================================================================ S16 a pink envelope in his desk
def s16(t, lt, dur):
    z = lerp(1.0, 1.18, ease(lt / dur))
    cam(t, lerp(960, 1080, ease(lt / dur)), 520, z)
    flatRect(-900, -900, W + 1800, H + 1800, '#8BB09F')
    boilSeed('d16top')
    paint(rectPts(-200, 170, W + 400, 60), wash='#E2C69A', ink=INK, sw=1.0)
    paint(rectPts(-200, 230, W + 400, 40), wash='#9C7652', fill='#7A5A3C', fillOp=60, ink=INK, sw=.9)
    paint(rectPts(-160, 270, W + 320, 420), wash='#33282E', fill='#241C22', fillOp=70, ink=INK, sw=.9)
    cols = ['#5E8FC4', '#C9727F', '#E7C46A', '#7FB59A', '#A98BC9', '#E39A6A', '#9FD3E8']
    x = 140
    i = 0
    while x < 1780:
        if 1020 < x < 1300:
            x += 30
            continue
        w = 40 + 30 * hash1(i * 2.1)
        h = 250 + 120 * hash1(i * 3.7)
        boilSeed('d16b%d' % i)
        paint(rectPts(x, 690 - h, w, h), wash=cols[i % 7], fill=mixCol(cols[i % 7], INK, .3), fillOp=50, ink=INK, sw=.6, lite=True)
        x += w + 6
        i += 1
    paint(rectPts(-200, 690, W + 400, 30), wash='#7A7F88', ink=INK, sw=.8)
    envelope(1160, 520, 300, -.32, '', 0.0, key='env16')
    camEnd()
    thoughtCloud(470, 230, 330, 170, ease(seg(t, 90.2, 90.6)), tail=(300, 420), key='tc16')
    if t > 90.3:
        text('谁写的？', 470, 230, 54, INK, face=WENKAI, shadow=False, a=ease(seg(t, 90.35, 90.6)))
    pastGrade(.8)
    tint('#B8C6E0', .12 * seg(t, 90.0, 92.4), skia.BlendMode.kMultiply)


# ================================================================ S17 she builds a wall of books on the line
def s17(t, lt, dur):
    k = seg(t, 92.6, 94.3)
    turned = t > 94.4
    ho = feel('angry', t, dict(view='q' if turned else 'front', flip=turned, lookX=-.6, aL=-.3, aR=.3))
    mo = feel('confused', t, dict(lookX=-.6))
    front(t, '2015', ho, mo, lambda: (deskBooks(PD_X0 + 20, 4, 'db1'), deskBooks(PD_X1 - 120, 4, 'db2'), bookWall(k)),
          cam_=(960, 640, 1.3), grade=.85)
    tint('#B8C6E0', .1, skia.BlendMode.kMultiply)


# ================================================================ S18 the white-out: "we're even"
def whitePenAt(rows, prog):
    for (x0, x1, y), p in zip(rows, prog):
        if 0 < p < 1:
            return lerp(x0 + 20, x1, p), y + 26
    return None


def s18(t, lt, dur):
    cam(t, lerp(620, 650, lt / dur), 630, 1.5)
    prog = (seg(t, 95.6, 97.3), seg(t, 97.4, 99.1), seg(t, 99.2, 100.6))
    deskState(t, old=.2, his=99, her=96, taunts=1.0, carve=1.0, books=1.0, white=prog, graffiti=.5)
    gx, gy = HER_GRID
    rows = [(gx - 14, gx + 7 * 66 + 64, gy), (gx - 14, gx + 7 * 66 + 64, gy + 76), (gx - 14, gx + 2 * 66 + 62, gy + 152)]
    p = whitePenAt(rows, prog)
    if p:
        penTop(p[0], p[1], .55, white=True, L=280, key='wpen')
    elif t >= 100.6:
        penTop(560, 730, .5, white=True, L=280, key='wpen')
    camEnd()
    pastGrade(.8)
    tint('#9AA8C8', .14, skia.BlendMode.kMultiply)


# ================================================================ S19 the last stroke: she doesn't cover it
def s19(t, lt, dur):
    cam(t, lerp(600, 610, lt / dur), 690, lerp(2.5, 2.7, lt / dur))
    deskState(t, old=.2, his=99, her=96, taunts=1.0, carve=1.0, books=1.0, white=(1, 1, 1), loneGlow=ease(seg(t, 104.8, 105.6)), graffiti=.5)
    if t < 101.5:
        x, y = 560, 730
    elif t < 104.5:
        k = ease(seg(t, 101.5, 102.5))
        x, y = lerp(560, 600, k), lerp(730, 702, k) + 3 * math.sin(t * 5) * seg(t, 102.5, 103)
    else:
        k = easeIn(seg(t, 104.5, 105.6))
        x, y = lerp(600, 980, k), lerp(702, 420, k)
    if t < 105.7:
        hover = 1 if 102.5 < t < 104.5 else 0
        G.c.drawRoundRect(skia.Rect.MakeXYWH(x + 30, y + 20, 260, 30), 12, 12, skia.Paint(AntiAlias=True, Color=skcol('#000000', .15 * hover)))
        penTop(x, y - 12 * hover, .5, white=True, L=280, key='wpen')
    camEnd()
    pastGrade(.8)
    tint('#9AA8C8', .14, skia.BlendMode.kMultiply)


# ================================================================ S20 ten years later: the same stroke
def s20(t, lt, dur):
    k = ease(seg(t, 107.4, 111.6))
    cam(t, lerp(605, 900, k), lerp(690, 620, k), lerp(2.6, 1.45, k))
    deskState(t, old=1.0, his=99, her=96, white=(1, 1, 1), carve=1.0, taunts=1.0, tents=1.0, shaft=1.0,
              loneGlow=.6 + .4 * math.sin(t * 2.2), graffiti=1.0)
    camEnd()
    presentGrade(.85, vig=.48)
    dustMotes(t, 40, .32, seed=51)


# ================================================================ S21 under the desk: 「给方茴」
def s21(t, lt, dur):
    cam(t, 900, 560, lerp(1.0, 1.1, lt / dur))
    underside(t, old=1.0, envK=1.0, tapes=2.0)
    lx = lerp(-200, 820, ease(seg(t, 112.0, 113.0)))
    sx, sy = scr(lx, 560)
    z = eng.CAM[2]
    camEnd()
    darkness(.6, [(sx, sy, 560 * z, 1.0)], '#05060F')
    glow(sx, sy, 380 * z, '#EAF0FF', .25)
    presentGrade(.7, vig=.4)


# ================================================================ S22 the door opens: he came too
def s22(t, lt, dur):
    opn = ease(seg(t, 115.7, 116.4))
    ho = feel('surprised' if t > 116.3 else 'neutral', t, dict(view='q', flip=t > 116.0, lookX=.6, take=0, aL=-.2, aR=.3))
    ho['take'] = 0
    mo = feel('nervous', t, dict(view='front', lookX=.4))

    def herD():
        herNow(1000, FLOOR, U, ho, .4)
        side = 'R'
        hx, hy = handXY(1000, FLOOR, U, ho, side)
        envelope(hx, hy - 4, 92, .2, '', 1.0, key='env22', sticker=True)
        handDot(hx, hy, 'her', U)

    def extra():
        nameCard(DOOR_X, 440, '陈寻 · 28岁', '毕业十年 也回来了', ease(seg(t, 116.5, 116.95)) * (1 - ease(seg(t, 117.7, 118.1))))
    inDoor = (lambda: himNow(DOOR_X, FLOOR, U, mo, 1.0)) if t > 115.6 else None
    presentRoom(t, (1000, 700, 1.0), herD, None, door=opn, inDoor=inDoor, extra=extra)
