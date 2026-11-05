# story_d.py: 《匆匆那年》 S32–S44 — ten years later in the classroom: they meet, blush, she reads the letter; the memories;
# "settle it today?" — no: a box of milk crosses the line both ways, a new stroke on each side; the gate in the snow; the board.
import math
from eng import *
import eng
from clawd import *
from cc import *
from cc2 import *
from props import bubble, sparkle
from story_b import presentRoom, handDot, slide
import story_b, story_a
from wo import scr
from common import *

HX, MX = 1000, 640          # her by the desk, him in front of her (13u apart)


def herEnv(o, x=HX):
    hx, hy = handXY(x, FLOOR, U, o, 'R')
    envelope(hx, hy - 4, 92, .2, '', 1.0, key='envh', sticker=True)
    handDot(hx, hy, 'her', U)


# ================================================================ S32 he walks up to her
def s32(t, lt, dur):
    st = stroll(t, 166.6, 169.2, DOOR_X, MX, U)
    mo = feel('nervous' if t < 169.2 else 'shy', t, dict(view='q', walk=st['walk'] if t < 169.2 else None, dy=st['dy'],
                                                         lookX=.5, emote=None))
    ho = feel('surprised' if t < 168.0 else 'hopeful', t, dict(view='q', flip=True, lookX=.6, take=0, aR=.3))
    ho['take'] = 0
    k = ease(seg(t, 168.4, 171.4))
    presentRoom(t, (lerp(1000, 820, k), lerp(700, 690, k), lerp(1.0, 1.3, k)),
                lambda: (herNow(HX, FLOOR, U, ho, .3), herEnv(ho)), lambda: himNow(st['x'], FLOOR, U, mo, .8), door=1.0)


# ================================================================ S33 both of them go red
def s33(t, lt, dur):
    ho = feel('shy', t, dict(view='q', flip=True, lookX=.5, lookY=.5, blush=1.0, aR=.3))
    mo = feel('shy', t, dict(view='q', lookX=-.3, lookY=.6, blush=1.0))
    presentRoom(t, (820, 680, lerp(1.58, 1.64, lt / dur)), lambda: (herNow(HX, FLOOR, U, ho, .25), herEnv(ho)),
                lambda: himNow(MX, FLOOR, U, mo, .6), door=1.0)


# ================================================================ S34 the carving is still there; his half was never erased
def s34(t, lt, dur):
    k = ease(seg(t, 176.2, 178.9))
    cam(t, lerp(960, 1320, k), lerp(340, 640, k), lerp(2.1, 1.55, k))
    deskState(t, old=1.0, his=99, her=96, white=(1, 1, 1), carve=1.0, taunts=1.0, tents=1.0, shaft=1.0, graffiti=1.0)
    gk = ease(seg(t, 174.4, 175.4)) * (1 - .6 * k)
    glow(LINE_X, 336, 260, '#FFE2A8', .4 * gk)
    if k > .3:
        for g in range(20):
            gx, gy = tallyAt('his', g)
            p = math.exp(-((t - (177.4 + g * .06)) / .3) ** 2)
            if p > .02:
                glow(gx + 25, gy + 25, 60, '#FFE2A8', .5 * p)
    camEnd()
    presentGrade(.8, vig=.45)
    dustMotes(t, 36, .3, seed=61)


# ================================================================ S35 / S36 the letter, read line by line
def letterOnDesk(t, hi, camv):
    cam(t, *camv)
    deskState(t, old=1.0, his=99, her=96, white=(1, 1, 1), carve=1.0, taunts=1.0, graffiti=1.0)
    envelope(1560, 280, 300, .25, '给方茴', 1.0, key='envopen')
    cx, cy, w, h = 960, 560, 1000, 660
    push()
    translate(cx, cy)
    rotate(-.015)
    translate(-cx, -cy)
    letterPaper(cx, cy, w, h, 1.0, key='lp35')
    letterText(cx, cy, w, h, (1, 1, 1, 1), 1.0, hi=hi)
    pop()
    camEnd()
    presentGrade(.6, vig=.5)
    glow(W / 2, H / 2, 700, '#FFE7C0', .18)


def s35(t, lt, dur):
    hi = 0 if t < 181.7 else 1
    k = ease(seg(t, 180.9, 182.4))
    letterOnDesk(t, hi, (lerp(820, 900, k), lerp(330, 420, k), lerp(1.75, 1.6, k)))


def s36(t, lt, dur):
    hi = 2 if t < 188.7 else 3
    k = ease(seg(t, 185.5, 189.6))
    letterOnDesk(t, hi, (lerp(900, 1020, k), lerp(480, 540, k), lerp(1.6, 1.5, k)))


# ================================================================ S37 she cries and laughs; he scratches his head
def s37(t, lt, dur):
    ho = feel('happy', t, dict(view='q', flip=True, lookX=.5, blush=.9, eyes='happy' if int(t * 1.2) % 3 == 0 else 'normal',
                               aR=.3, aL=-.3))
    mo = feel('shy', t, dict(view='q', lookX=.3, blush=1.0, aR=1.55 + .12 * math.sin(t * 9), aL=-.3))

    def her_():
        herNow(HX, FLOOR, U, ho, .2)
        herEnv(ho)
        ex = HX - 1.5 * U
        for dx in (-1.9, 1.9):
            tears(t, ex + dx * .74 * U, FLOOR - 5.8 * U, U, a=.9, seed=int(dx * 10))
    presentRoom(t, (lerp(840, 860, lt / dur), 670, lerp(1.55, 1.62, lt / dur)), her_, lambda: himNow(MX, FLOOR, U, mo, .3), door=1.0)


# ================================================================ S38 memories flash by
FLASH = [(196.79, story_b.s04, 32.6), (198.10, story_b.s10, 60.2), (199.40, story_b.s11, 62.9), (200.70, story_b.s15, 86.6)]


def s38(t, lt, dur):
    j = 0
    for i, (a, fn, base) in enumerate(FLASH):
        if t >= a:
            j = i
    a, fn, base = FLASH[j]
    tt = base + (t - a) * .8
    G.c.save()
    fn(tt, 0, 5)
    G.c.restore()
    if eng.CAM:
        camEnd()
    vignette(.35, '#FFF3DA')
    nxt = FLASH[j + 1][0] if j + 1 < len(FLASH) else 202.02
    flash(.75 * (1 - ease(seg(t, a, a + .18))))
    flash(.6 * ease(seg(t, nxt - .12, nxt - .01)))


# ================================================================ S39 "settle it today?" — she shakes her head, and takes out a box of milk
def s39(t, lt, dur):
    offer = ease(seg(t, 202.4, 203.0))
    mo = feel('hopeful', t, dict(view='q', lookX=.5, aR=lerp(-.3, .45, offer), aL=-.3, blush=.4))
    shake = .3 * math.sin((t - 205.0) * 16) * (1 if 205.0 < t < 205.7 else 0)
    ho = feel('neutral' if t < 205.6 else 'happy', t, dict(view='q', flip=True, lookX=.5, lookY=.3 if t < 205 else 0, dx=shake,
                                                           aR=lerp(.3, .7, ease(seg(t, 206.0, 206.5))), blush=.6))

    def him_():
        himNow(MX, FLOOR, U, mo, .3)
        if offer > .05:
            hx, hy = handXY(MX, FLOOR, U, mo, 'R')
            push()
            translate(hx + 10, hy - 6)
            rotate(-1.3)
            boilSeed('wp39')
            paint(rrPts(-6, -10, 66, 20, 7), wash='#FBFBF8', ink=INK, sw=.6)
            paint(rrPts(56, -11, 20, 22, 6), wash='#5E8FC4', ink=INK, sw=.6)
            pop()
            handDot(hx, hy, 'him', U)

    def her_():
        herNow(HX, FLOOR, U, ho, .2)
        hx, hy = handXY(HX, FLOOR, U, ho, 'R')
        if t > 206.0:
            push()
            translate(hx, hy - 30)
            boilSeed('milk39')
            paint(rrPts(-26, -40, 52, 70, 5), wash='#FBFBF6', ink=INK, sw=.7)
            paint(rectPts(-26, 4, 52, 24), wash='#5E9BD6', ink=None)
            text('牛奶', 0, -16, 18, '#3B6EA8', face=WENKAI, shadow=False)
            pop()
        handDot(hx, hy, 'her', U)
    presentRoom(t, (820, 685, lerp(1.45, 1.5, lt / dur)), her_, him_, door=1.0)


# ================================================================ S40 the milk crosses the line, and comes back, and stops on it
def s40(t, lt, dur):
    cam(t, 960, 560, lerp(1.22, 1.3, lt / dur))
    deskState(t, old=1.0, his=99, her=96, white=(1, 1, 1), carve=1.0, taunts=1.0, tents=1.0, shaft=1.0, graffiti=1.0)
    if t < 210.5:
        x, y, _ = slide(t, 208.2, 209.4, (620, 470), (1260, 470))
    else:
        x, y, _ = slide(t, 210.6, 211.7, (1260, 470), (960, 470), easeOut)
    milkBox(x, y, -.05, key='m40', old=0.0)
    camEnd()
    presentGrade(.75, vig=.45)
    dustMotes(t, 36, .3, seed=71)


# ================================================================ S41 one new stroke on each side: owing each other again
def s41(t, lt, dur):
    cam(t, lerp(900, 905, lt / dur), 640, lerp(1.5, 1.56, lt / dur))
    k = ease(seg(t, 213.75, 214.4))
    nh, kh = (100, k) if t > 213.75 else (99, 1.0)
    nr, kr = (97, k) if t > 213.75 else (96, 1.0)
    deskState(t, old=1.0, his=nh, hisK=kh, her=nr, herK=kr, white=(1, 1, 1), carve=1.0, taunts=1.0, tents=1.0, shaft=1.0, graffiti=1.0)
    milkBox(960, 470, -.05, key='m40', old=0.0)
    if t > 213.75:
        p = math.exp(-((t - 214.3) / .5) ** 2)
        for side in ('his', 'her'):
            gx, gy = tallyAt(side, 19)
            glow(gx + 25, gy + 25, 110, '#FFE2A8', .7 * p + .2)
    warm = ease(seg(t, 214.0, 218.0))
    camEnd()
    presentGrade(.8 * (1 - .6 * warm), vig=.4)
    memoryLook(.6 * warm)
    dustMotes(t, 40, .34, seed=81)


# ================================================================ S42 the gate in the snow: goodbye — this time it means "see you"
def s42(t, lt, dur):
    cam(t, 960, 560, lerp(1.06, 1.0, lt / dur))
    gateScene(t, 'eve', snow=.8)
    u = 30
    if t < 221.5:
        hx, mx = 820, 1180
        wave = 1.15 + .3 * math.sin(t * 9)
        ho = feel('happy', t, dict(view='q', aR=wave if t > 219.7 else .2, blush=.5))
        mo = feel('happy', t, dict(view='q', flip=True, aR=wave if t > 219.9 else .2, blush=.5))
    else:
        sh = stroll(t, 221.6, 225.2, 820, 540, u)
        sm = stroll(t, 221.6, 225.2, 1180, 1460, u)
        hx, mx = sh['x'], sm['x']
        ho = feel('neutral', t, dict(view='q', flip=True, walk=sh['walk'], dy=sh['dy']))
        mo = feel('neutral', t, dict(view='q', walk=sm['walk'], dy=sm['dy']))
        footprints(hx + 50, 800, GATE_FLOOR + 10, max(1, int((820 - hx) / 60)), .45)
        footprints(1200, mx - 50, GATE_FLOOR + 14, max(1, int((mx - 1180) / 60)), .45)
    herNow(hx, GATE_FLOOR, u, ho, .5)
    himNow(mx, GATE_FLOOR, u, mo, .5)
    for (a, b, x, key) in ((219.6, 221.3, 760, 'b42h'), (219.85, 221.4, 1240, 'b42m')):
        k = ease(seg(t, a, a + .25)) * (1 - ease(seg(t, b - .2, b)))
        bubble(x, GATE_FLOOR - 15 * u, '再见！', 40, (x + (40 if x < 960 else -40), GATE_FLOOR - 10 * u), k, key=key)
    lx, ly = scr(1095, GATE_FLOOR - 680)
    camEnd()
    presentGrade(.6, vig=.35)
    glow(lx, ly, 300, '#FFE9B0', .25)


# ================================================================ S43 a few steps apart — both look back, walk back, and go on together
def s43(t, lt, dur):
    cam(t, 960, 540, lerp(.95, .9, lt / dur))
    gateScene(t, 'eve', snow=.8)
    u = 30
    if t < 226.6:
        sh = stroll(t, 224.9, 226.6, 540, 330, u)
        sm = stroll(t, 224.9, 226.6, 1460, 1680, u)
        hx, mx = sh['x'], sm['x']
        ho = feel('neutral', t, dict(view='q', flip=True, walk=sh['walk'], dy=sh['dy']))
        mo = feel('neutral', t, dict(view='q', walk=sm['walk'], dy=sm['dy']))
    elif t < 227.6:
        hx, mx = 330, 1680
        ho = feel('hopeful', t, dict(view='q', lookX=.6, emote='!' if t > 226.9 else None, emoteAge=t - 226.9))
        mo = feel('hopeful', t, dict(view='q', flip=True, lookX=.6, emote='!' if t > 227.0 else None, emoteAge=t - 227.0))
    elif t < 229.9:
        sh = stroll(t, 227.6, 229.9, 330, 800, u)
        sm = stroll(t, 227.6, 229.9, 1680, 1160, u)
        hx, mx = sh['x'], sm['x']
        ho = feel('happy', t, dict(view='q', walk=sh['walk'], dy=sh['dy'], blush=.6))
        mo = feel('happy', t, dict(view='q', flip=True, walk=sm['walk'], dy=sm['dy'], blush=.6))
    else:
        sh = stroll(t, 230.3, 234.5, 800, 1620, u)
        sm = stroll(t, 230.3, 234.5, 1160, 1980, u)
        hx, mx = sh['x'], sm['x']
        ho = feel('happy', t, dict(view='q', walk=sh['walk'] if t > 230.3 else None, dy=sh['dy'], lookX=.6, blush=.6))
        mo = feel('happy', t, dict(view='q', walk=sm['walk'] if t > 230.3 else None, dy=sm['dy'], lookX=-.2, blush=.6))
    footprints(340, 800, GATE_FLOOR + 10, 9, .4)
    footprints(1160, 1680, GATE_FLOOR + 14, 9, .4)
    if t > 230.3:
        footprints(820, hx - 40, GATE_FLOOR + 22, max(1, int((hx - 820) / 60)), .45)
        footprints(1180, mx - 40, GATE_FLOOR + 26, max(1, int((mx - 1180) / 60)), .45)
    herNow(hx, GATE_FLOOR, u, ho, .5)
    himNow(mx, GATE_FLOOR, u, mo, .5)
    camEnd()
    presentGrade(.55, vig=.35)


# ================================================================ S44 the board at dusk: 「下次再算」
def s44(t, lt, dur):
    k = ease(seg(t, 236.8, 240.8))
    cam(t, lerp(1110, 1060, k), lerp(85, 200, k), lerp(1.72, 1.35, k))
    classroomFront(t, 1.0, False, 0.0, board='final', endProg=seg(t, 234.0, 236.6))
    camEnd()
    presentGrade(1.0, vig=.55)
    tint('#7F8CC0', .22, skia.BlendMode.kMultiply)
    glow(W * .7, H * .2, 600, '#FFC98A', .12)
