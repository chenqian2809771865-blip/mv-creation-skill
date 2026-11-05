# story_a.py: 《匆匆那年》 S01–S03 — the intro: the desk (hook), the blackboard title (A1), she comes back.
import math
from eng import *
import eng
from clawd import *
from cc import *
from cc2 import *
from common import *

TA = B[28]          # 13.03: last stroke of the chalk title lands on this bar line (hard rule 8, A1)
T_STR = B[12]       # 5.50: strings come in
T_BASS = B[36]      # 16.82: bass comes in


def placeholder(t, lt, dur):
    flatRect(-100, -100, W + 200, H + 200, '#20263A')
    text('待做', W / 2, H / 2, 80, CREAM, face=WENKAI, shadow=False)


# ================================================================ S01 0–9.26 the desk from above: the line, the account (the hook)
def ghostEcho(t, t0, t1, draw, x0, x1, y, markSide, markXY):
    """a memory replaying on the present desk: a warm translucent object slides across the line; when it crosses,
    a stroke flashes on the side it lands on (whoever crossed owes one)"""
    k = seg(t, t0, t1)
    if 0 < k < 1:
        a = math.sin(k * math.pi) ** .7
        x = lerp(x0, x1, ease(k))
        G.c.saveLayerAlpha(None, int(170 * a))
        draw(x, y)
        tp = skia.Paint(Color=skcol('#FFC870', .55))                    # warm-gold tint on the object only
        tp.setBlendMode(skia.BlendMode.kSrcATop)
        G.c.drawRect(skia.Rect.MakeXYWH(x - 300, y - 200, 600, 400), tp)
        G.c.restore()
        glow(x, y, 170, '#FFD99A', .5 * a)
        for i in range(5):                                               # a little trail of light behind it
            tx = x - (x1 - x0) / abs(x1 - x0) * (30 + i * 34)
            G.c.drawCircle(tx, y + (hash1(i * 3.1) - .5) * 40, 4 - .6 * i, skia.Paint(AntiAlias=True, Color=skcol('#FFF1C8', .7 * a * (1 - i / 5))))
    tc = t0 + (t1 - t0) * .5
    m = t - tc
    if 0 < m < 1.4:
        ka = (1 - m / 1.4) * clamp(m / .12)
        mx, my = markXY
        penStroke((mx - 22, my), (mx + 22, my + 1), 4.0, HER_PEN if markSide == 'her' else HIS_PEN, ka, 9, .05)
        glow(mx, my, 80, '#FFE7B8', .6 * ka)


def s01(t, lt, dur):
    if t < T_STR:
        k = seg(t, 0, T_STR)
        cx, cy, z, rot = lerp(960, 965, k), lerp(782, 760, ease(k)), lerp(1.70, 1.62, k), lerp(-.05, -.02, ease(k))
    else:
        k = ease(seg(t, T_STR, 8.0))
        cx, cy, z, rot = lerp(965, 952, k), lerp(760, 600, k), lerp(1.62, 1.16, k), lerp(-.02, 0, k)
        z *= 1 + .015 * seg(t, 8.0, B[20])
    cam(t, cx, cy, z, rot)

    lg = ease(seg(t, 8.0, 8.45)) * (1 - ease(seg(t, 8.7, 9.4)))
    deskState(t, old=1.0, his=99, her=96, white=(1, 1, 1), carve=1.0, loneGlow=lg, taunts=1.0, tents=1.0, shaft=1.0,
              carveA=ease(seg(t, 7.5, 8.3)), graffiti=1.0)
    # strings come in: the whole account lights up group by group, from the line outward
    for side, n in (('his', 20), ('her', 19)):
        for g in range(n):
            gx, gy = tallyAt(side, g)
            d = abs(gx + 25 - LINE_X) / 700 * 1.5 + abs(gy - 540) / 400 * .25
            p = math.exp(-((t - (T_STR + .3 + d)) / .28) ** 2)
            if p > .02:
                glow(gx + 25, gy + 25, 70, '#FFE2A8', .55 * p)
    # memories replaying during the piano solo
    ghostEcho(t, .9, 2.5, lambda x, y: pencilCase(x, y, .05, '#3F5FAE', key='gpc'), 1330, 640, 640, 'her', (905, 700))
    ghostEcho(t, 2.4, 3.9, lambda x, y: paint(rrPts(x - 46, y - 26, 92, 52, 10), wash='#F2A9BC', ink=INK, sw=.6), 640, 1260, 712, 'his', (1012, 640))
    ghostEcho(t, 3.8, 5.4, lambda x, y: milkBox(x, y, -.08, key='gmilk'), 1330, 700, 668, 'her', (905, 610))
    camEnd()
    glow(W / 2, H * .5, 760, '#DCE6FF', .14)
    presentGrade(.85, vig=.48)
    dustMotes(t, 46, .36)


# ================================================================ S02 9.26–16.82 the blackboard: the chalk writes the title
def chalkDust(t, x, y, on):
    if not on:
        return
    for i in range(6):
        a = (t * 3.1 + i / 6) % 1.0
        px = x + (hash1(i * 3.7 + math.floor(t * 3.1)) - .5) * 26
        py = y + 6 + a * 70
        G.c.drawCircle(px, py, 2.2 * (1 - a) + .6, skia.Paint(AntiAlias=True, Color=skcol('#F4F1E6', .7 * (1 - a))))


def s02(t, lt, dur):
    z = lerp(1.72, 1.80, ease(seg(t, B[20], T_BASS)))
    cam(t, 1110, 85, z)
    prog = seg(t, 9.62, TA - .02)
    classroomFront(t, titleProg=prog, chalkOn=t < TA)
    if 0 < prog < 1:
        px, py = writeTip('匆匆那年', TITLE_X0, TITLE_Y0, TITLE_SIZE, prog)
        chalkDust(t, px, py, True)
    camEnd()
    presentGrade(1.0, vig=.5)
    dustMotes(t, 24, .22, seed=21)


# ================================================================ S03 16.82–28.17 tilt down into the empty classroom; she comes in
DOOR_X = 310
DESK_STOP = 1000


def herIntro(t):
    """her pose / position in S03 (present: beanie with snow, camel scarf)"""
    snow = lerp(1.0, .55, seg(t, 25.0, 28.4))
    if t < 21.0:
        o = feel('neutral', t, dict(view='front', lookX=lerp(-.5, .55, ease(seg(t, 20.3, 20.95))), lookY=-.1))
        return DOOR_X, o, snow
    st = stroll(t, 21.0, 24.3, DOOR_X, DESK_STOP, U)
    if t < 24.3:
        o = feel('neutral', t, dict(view='q', walk=st['walk'], dy=st['dy'], lookX=.35 + .3 * math.sin(t * 1.4), lookY=-.15))
    else:
        o = feel('neutral', t, dict(view='q', lookX=.6, lookY=lerp(.1, .6, ease(seg(t, 24.3, 25.0))), aL=-.2,
                                    aR=lerp(.2, -.35, ease(seg(t, 24.4, 25.2)))))
    return st['x'], o, snow


def s03(t, lt, dur):
    a1, a2 = 19.8, 24.3
    if t < a1:
        k = ease(seg(t, T_BASS, a1))
        cx, cy, z = lerp(1110, 1000, k), lerp(85, 700, k), lerp(1.80, 1.0, k)
    elif t < a2:
        cx, cy, z = 1000, 700, lerp(1.0, 1.02, seg(t, a1, a2))
    else:
        k = ease(seg(t, a2, 28.4))
        cx, cy, z = lerp(1000, 1170, k), lerp(700, 720, k), lerp(1.02, 1.3, k)
    cam(t, cx, cy, z)
    opn = ease(seg(t, 19.45, 20.3))
    x, o, snow = herIntro(t)
    inDoor = (lambda: herNow(x, FLOOR, U, o, snow)) if 19.4 <= t < 21.0 else None
    classroomFront(t, 1.0, False, opn, inDoor=inDoor)
    deskFront(t)
    if opn > .01:
        glow(280, 760, 260, '#DDE7FF', .25 * opn)
    if t >= 21.0:
        herNow(x, FLOOR, U, o, snow)
    # breath in the cold room
    for tb in (25.25, 27.05):
        a = t - tb
        if 0 < a < 1.6:
            k = a / 1.6
            puff(x + 2.6 * U + 60 * k, FLOOR - 5.4 * U - 50 * k, 7 + 9 * k, '#F4F8FF', key='breath%d' % int(tb), ink=False,
                 a=.75 * (1 - k) * min(1, a / .2))
    nameCard(DOOR_X, 440, '方茴 · 28岁', '毕业十年 第一次回来', ease(seg(t, 20.7, 21.25)) * (1 - ease(seg(t, 23.8, 24.3))))
    camEnd()
    presentGrade(1.0, vig=.45)
    dustMotes(t, 24, .22, seed=31)
