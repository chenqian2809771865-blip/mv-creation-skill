# story_a.py: 《我好想你》 S01–S30 — intro (A1 note title, memory flash, dark room), verse 1 and chorus 1 (his side).
import math
from eng import *
import eng
from clawd import *
from props import puff, sparkle, sparkles, bubble
from props_bingbian import bolt
from hl import wtext, inkWrite, writeW, stars, rain, mug, deskLamp, desat, tint, vignette
from sets2 import seat, teacupTop, hillY2
from bbset import pillowProp, hairClip
from nm import heartP, postit, darkness, phoneP
from hb import thoughtCloud, woodTop, doodleHeart
from wo import *
from common import *

BG = '#0B1030'


def handDot(x, y, who):
    paint(ellPts(x, y, U * .42, U * .42, 10), wash=(ME if who == 'him' else HER)['col'], ink=INK, sw=.6)


def tween(t, a, b, v0, v1, e=ease):
    return lerp(v0, v1, e(seg(t, a, b)))


# ================================================================ S01 0–12.70 the note (A1 title) → the tin
NOTE = (900, 520, 400)
TIN_T = (1770, 560, 420, 300)


def deskTopScene(t, who='him', tinFill=1.0, tinLid=1.0, extraNotes=0, flowerK=1.0, mugK=1.0):
    flatRect(-1600, -1200, W + 3200, H + 2400, '#8F5C3A')
    for i in range(-30, 60):
        y = -1100 + i * 62
        if y < -300 or y > H + 300:
            inkLine([[-1600, y], [W + 1600, y + 6]], .35, '#5E3A22', 'inkfine', .6)
    woodTop(0.0, key='wood' + who)
    # lamp pool
    glow(760, 420, 900, '#FFC872', .55)
    glow(820, 480, 520, '#FFE2A8', .45)
    if mugK:
        teacupTop(420, 300, t, key='tc' + who)
    if flowerK:
        # her little white flower, dried, lying on the desk
        boilSeed('dfl' + who)
        inkLine([[520, 860], [600, 820], [650, 800]], 1.1, '#8A7A5A', 'ink', .4)
        push()
        translate(510, 865)
        rotate(.5)
        for i in range(5):
            a = i / 5 * TAU
            paint(ellPts(math.cos(a) * 16, math.sin(a) * 16, 14, 9, 10, 0, a), wash='#E8DCC0', ink=INK, sw=.45, lite=True)
        paint(ellPts(0, 0, 8, 8, 10), wash='#C9A65A', ink=None)
        pop()
    x, y, w, h = TIN_T
    if who == 'her':
        x = W - x
    tinTop(x, y, w, h, who, fill=tinFill, lid=tinLid, key='tinT' + who, extra=extraNotes)


def nightAround(lampXY, r):
    sx, sy = scr(*lampXY)
    z = eng.CAM[2] if eng.CAM else 1.0
    return [(sx, sy, r * z, 1.0)]


def s01(t, lt, dur):
    TA, TO = B[16], B[24]
    z = lerp(1.58, 1.64, seg(t, 0, TO)) if t < TO else lerp(1.64, 1.0, ease(seg(t, TO, TO + 1.7)))
    cx = lerp(900, 1240, ease(seg(t, TO, TO + 1.7)))
    cy = lerp(520, 545, ease(seg(t, TO, TO + 1.7)))
    cam(t, cx, cy, z)
    landT = 11.95
    deskTopScene(t, 'him', tinFill=1.0 if t < landT else 1.04, extraNotes=0 if t < landT else 1)
    nx, ny, nw = NOTE
    prog = ease(seg(t, .25, TA - .02)) if t < TA else 1.0
    fold = ease(seg(t, 10.15, 10.75))
    if t < 10.85:
        writtenNote('我好想你', nx, ny, nw, prog, t, NOTE_Y, key='n01', size=82, pen=t < TA, fold=fold)
        if t >= TA:       # the pen rests beside the note
            fountainPen(nx + 260, ny + 230, 44, ang=-1.1, key='fpen')
    else:
        fountainPen(nx + 260, ny + 230, 44, ang=-1.1, key='fpen')
        k = seg(t, 10.85, landT)
        tx, ty = TIN_T[0] - 40, TIN_T[1] + 10
        px, py = arcPt((nx, ny), (tx, ty), -260, ease(k))
        if t < landT:
            foldedNote(px, py, lerp(nw * .9, 90, ease(k)), k * 2.4, NOTE_Y, key='fly01')
        else:
            foldedNote(tx, ty, 90, 2.4, NOTE_Y, key='fly01')
            if t < landT + .4:
                sparkle(tx + 40, ty - 30, 30 * (1 - (t - landT) / .4), '#FFFFFF')
    lights = nightAround((820, 470), 640) + [scr(TIN_T[0], TIN_T[1]) + (420 * eng.CAM[2], .55)]
    camEnd()
    darkness(.62, lights, BG)


# ================================================================ S02 12.70–14.27 the tin bursts
def s02(t, lt, dur):
    cam(t, TIN_T[0], TIN_T[1] - 40, lerp(1.5, 1.7, lt / dur))
    deskTopScene(t, 'him', tinFill=1.1)
    a = t - B[32]
    n = 46
    for i in range(n):
        d0 = hash1(i * 3.7 + 2) * .25
        k = clamp((a - d0) / 1.3)
        if k <= 0:
            continue
        ang = hash1(i * 1.9) * TAU
        r = (40 + 900 * easeOut(k)) * (.5 + .7 * hash1(i * 5.1))
        px = TIN_T[0] + math.cos(ang) * r
        py = TIN_T[1] + math.sin(ang) * r * .8 - 120 * k
        s = 50 + 260 * k * k * (.6 + .6 * hash1(i))
        flyingNote(px, py, s, t, i, NOTE_Y if i % 5 else '#FFFDF6', key='b02')
    camEnd()
    memoryLook(seg(t, B[32], B[32] + .8))
    flash(ease(seg(t, B[36] - .45, B[36] - .02)) * .85, '#FFF8E8')


# ================================================================ memory flash S03–S09 (bright, saturated)
def memRoom(t, **kw):
    kw.setdefault('flowerDry', 0.0)
    kw.setdefault('lightsOn', 1.0)
    return roomBack(t, 'him', **kw)


def s03(t, lt, dur):
    """hanging the string lights: she on a stool, he on the floor, the bulbs light up one by one between their raised hands"""
    cam(t, 1480, 500, lerp(1.28, 1.34, lt / dur))
    memRoom(t, lightsOn=0.0)
    top = stool(1300, FLOOR, 1.25, key='stool3')
    oh, sh = armToward(fo(feel('happy', t, dict(lookX=.6)), view='front', dy=0, aL=.2, aR=.2), 1300, top, U, 1700, 1.25)
    om, sm = armToward(fo(feel('happy', t, dict(lookX=-.6)), view='front', aL=.2, aR=.2), 1700, FLOOR, U, 1300, 1.25)
    her(1300, top, U, oh)
    him(1700, FLOOR, U, om)
    hx, hy = handXY(1300, top, U, oh, sh)
    mx, my = handXY(1700, FLOOR, U, om, sm)
    pts = [[lerp(hx, mx, i / 20), lerp(hy, my, i / 20) + 50 * math.sin(i / 20 * math.pi)] for i in range(21)]
    inkLine(pts, .9, '#3A3550', 'ink', .3)
    on = seg(t, B[36] + .15, B[40] - .3)
    n = 7
    for i in range(n):
        k = (i + .5) / n
        bx, by = lerp(hx, mx, k), lerp(hy, my, k) + 50 * math.sin(k * math.pi) + 12
        lit = 1 if on * n > i else 0
        if lit:
            glow(bx, by, 70, '#FFD27A', .85)
        G.c.drawCircle(bx, by, 9, skia.Paint(AntiAlias=True, Color=skcol(mixCol('#6A6688', '#FFF1C2', lit))))
    handDot(hx, hy, 'her')
    handDot(mx, my, 'him')
    camEnd()
    memoryLook()


def s04(t, lt, dur):
    """pillow fight on the bed, feathers"""
    cam(t, 1560, 520, 1.3)
    memRoom(t, bedKw=dict(clip=False))
    top = BED_Y - 4.2 * BED_S + 8
    sw_ = math.sin((t - B[40]) * 7)
    om = fo(feel('laugh', t, dict(aL=.2, aR=.2)), view='front', dy=-.6 * abs(math.sin((t - B[40]) * 5)))
    oh = fo(feel('laugh', t, dict(aL=.2, aR=.2)), view='front', dy=-.6 * abs(math.cos((t - B[40]) * 5)))
    om, sm = armToward(om, 1390, top, U, 1730, 1.25 + .3 * sw_)
    oh, sh = armToward(oh, 1730, top, U, 1390, 1.25 - .3 * sw_)
    him(1390, top, U, om)
    her(1730, top, U, oh)
    for (x, o, side, col, key, who) in ((1390, om, sm, '#F7F1E4', 'pl4a', 'him'), (1730, oh, sh, '#FBD0DA', 'pl4b', 'her')):
        px, py = handXY(x, top, U, o, side)
        pillowProp(px + (25 if who == 'him' else -25), py - 62, 140, 80, (.5 if who == 'him' else -.5) + .25 * sw_, col=col, key=key)
        handDot(px, py, who)
    featherFall(t, B[40] + .2, 1560, 330, n=14, spread=520)
    camEnd()
    memoryLook()


def s05(t, lt, dur):
    """two mugs clink (below face height), a little heart of steam"""
    cam(t, 860, 540, 1.42)
    memRoom(t, mugs=0)
    a = t - B[44]
    reach = ease(seg(a, .15, .65))
    om = fo(feel('happy', t, dict(lookX=.7)), view='q', dx=1.0 * reach)
    oh = fo(feel('happy', t, dict(lookX=-.7)), view='q', flip=True, dx=-1.0 * reach)
    om, sm = armToward(om, 640, FLOOR, U, 1080, -.15 + .1 * reach)
    oh, sh = armToward(oh, 1080, FLOOR, U, 640, -.15 + .1 * reach)
    him(640, FLOOR, U, om)
    her(1080, FLOOR, U, oh)
    mx, my = handXY(640, FLOOR, U, om, sm)
    hx, hy = handXY(1080, FLOOR, U, oh, sh)
    mug(mx + 16, my + 34, 1.0, key='mg5a', col='#E8E1D2')
    mug(hx - 16, hy + 34, 1.0, key='mg5b', col='#FFF0F3')
    handDot(mx, my, 'him')
    handDot(hx, hy, 'her')
    if a > .62:
        k = seg(a, .62, .9)
        sparkle((mx + hx) / 2, (my + hy) / 2 - 10, 40 * (1 - k) + 10, '#FFFFFF')
        floatHeartsUp(t, B[44] + .62, (mx + hx) / 2, (my + hy) / 2 - 60, n=5, spread=50, rise=200, life=1.0, s=16, seed=5)
    camEnd()
    memoryLook()


def s06(t, lt, dur):
    """she takes the little white flower off her head and drops it into the mug he is holding; he blushes"""
    cam(t, 1110, 560, 1.4)
    memRoom(t, mugs=0)
    a = t - B[48]
    up = ease(seg(a, .05, .3))          # hand up to the flower
    carry = ease(seg(a, .35, .85))      # hand over to his mug
    placed = a > .9
    om = fo(feel('shy' if placed else 'surprised', t, dict(lookX=-.8, emote=None)), view='q', flip=True, blush=1 if placed else .3)
    om, sm = armToward(om, 1320, FLOOR, U, 900, .05)
    him(1320, FLOOR, U, om)
    mx, my = handXY(1320, FLOOR, U, om, sm)
    flowerMug(mx - 6, my + 36, 1.0, dry=0.0, flower=placed, key='fm6')
    handDot(mx, my, 'him')
    ang = lerp(.2, 1.55, up) if carry <= 0 else lerp(1.55, .15, carry)
    oh = fo(feel('happy', t, dict(lookX=.8, lookY=.2)), view='q', hat=[] if a > .3 else 'flower')
    oh, sh = armToward(oh, 900, FLOOR, U, 1320, ang)
    her(900, FLOOR, U, oh)
    hx, hy = handXY(900, FLOOR, U, oh, sh)
    if .3 < a <= .9:
        tx, ty = (hx, hy - 16) if carry < 1 else (mx - 6, my - 40)
        flowerStar(tx, ty, 13, 1.0, key='fl6')
    handDot(hx, hy, 'her')
    camEnd()
    memoryLook()


def s07(t, lt, dur):
    """a selfie with the instant camera in front of the photo wall: flash, the photo slides out"""
    cam(t, 1580, 470, 1.32)
    memRoom(t)
    a = t - B[52]
    Em = feel('happy', t, dict(aR=1.45, aL=.25, lookX=.2, lookY=-.3))
    Eh = feel('love', t, dict(aL=.9, aR=.3, dx=0, rot=0))
    om = fo(Em, view='front')
    oh = fo(Eh, view='front', blush=.8)
    him(1420, FLOOR, U, om)
    her(1740, FLOOR, U, oh)
    px, py = handXY(1420, FLOOR, U, om, 'R')
    if px < 1420:
        px, py = handXY(1420, FLOOR, U, om, 'L')
    fl = math.exp(-max(0, a - .55) * 9) if a > .55 else 0
    instantCamera(px + 10, py - 40, 1.1, key='cam7', flashK=fl)
    paint(ellPts(px, py, U * .45, U * .45, 10), wash=PAL['clay'], ink=INK, sw=.6)
    if a > .7:
        k = ease(seg(a, .7, 1.3))
        polaroidMini(px + 10, py - 40 - 30 - 70 * k, 90, -.1, 1, drain=1 - k, key='pol7')
    camEnd()
    memoryLook()
    if a > .55:
        flash(.45 * math.exp(-(a - .55) * 10))


def s08(t, lt, dur):
    """a slow dance under the string lights"""
    cam(t, 1260, 470, 1.36)
    memRoom(t)
    a = t - B[56]
    sw_ = math.sin(a * 3.2)
    Em = feel('love', t, dict(aR=.9, aL=.2, rot=.05 * sw_, dx=.3 * sw_))
    Eh = feel('love', t, dict(aR=.9, aL=.2, rot=.05 * sw_, dx=.3 * sw_))
    him(1090, FLOOR, U, fo(Em, view='q', boilKey='him8'))
    her(1430, FLOOR, U, fo(Eh, view='q', flip=True, boilKey='her8'))
    floatHeartsUp(t, B[56], 1260, 560, n=7, spread=120, rise=260, life=1.6, s=15, seed=8)
    camEnd()
    memoryLook()


def s09_draw(t, k_off=0.0):
    roomBack(t, 'him', lightsOn=1 - k_off, flowerDry=0.0, switchOn=1 - k_off, bed=False)
    suitcase(150, FLOOR, 1.0, key='suit9')
    Eh = feel('sad', t, dict(aR=lerp(.3, 1.42, ease(seg(t, B[62], B[63]))), aL=-.2, lookX=-.8))
    oh = fo(Eh, view='q', flip=True, boilKey='her9')
    her(-20, FLOOR, U, oh)


def s09(t, lt, dur):
    cam(t, -60, 560, 1.38)
    k_off = 1.0 if t >= B[64] - .06 else 0.0
    s09_draw(t, k_off)
    camEnd()
    memoryLook(1 - k_off)


# ================================================================ S10 25.32–30.80 black; the last memory lingers as a ghost
def s10(t, lt, dur):
    flatRect(-200, -200, W + 400, H + 400, '#05060F')
    a = .42 * (1 - ease(seg(t, B[64] + .15, 30.3)))
    if a > .01:
        G.c.saveLayerAlpha(None, int(255 * a))
        z = lerp(1.38, 1.3, lt / dur)
        cam(t, -60, 560, z)
        s09_draw(B[64] - .1, 0.0)
        camEnd()
        desat(1.0)
        tint('#6A78B8', .5, skia.BlendMode.kMultiply)
        sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), W * .48, [skcol('#000000', 1), skcol('#000000', .6), skcol('#000000', 0)],
                                            [0, .5, 1])
        G.c.drawRect(skia.Rect.MakeXYWH(-400, -400, W + 800, H + 800), skia.Paint(Shader=sh, BlendMode=skia.BlendMode.kDstIn))
        G.c.restore()


# ================================================================ S11 30.80–38.38 now: the dark room, the camera drifts to the switch
def s11(t, lt, dur):
    k = ease(seg(t, 31.0, 36.6))
    cx = lerp(1700, -40, k)
    z = lerp(1.22, 1.42, k) + .12 * ease(seg(t, 36.0, 38.38))
    cam(t, cx, 560, z)
    roomBack(t, 'him', lightsOn=0.0, flowerDry=1.0, switchOn=0.0, bedKw=dict(night=.3))
    reach = ease(seg(t, 37.15, 38.25))
    glance = ease(seg(t, 36.3, 36.8)) * (1 - ease(seg(t, 37.3, 37.7)))
    breath = math.sin(max(0, t - 37.7) / .3 * math.pi) if 37.7 < t < 38.0 else 0
    Em = feel('sad', t, dict(aR=lerp(.2, 1.45, reach), aL=-.4, lookX=lerp(-.6, .8, glance), lookY=.2, sq=-.05 * breath, dy=-.15 * breath))
    om = fo(Em, view='q', flip=True, boilKey='him11', gloom=0)
    him(30, FLOOR, U, om)
    lights = [scr(2010 - 48, FLOOR - 154 - 70) + (360 * z, .75), scr(DOOR_X, FLOOR - 4) + (180 * z, .5)]
    camEnd()
    nightVeil(.95, lights)


# ================================================================ S12 38.38–42.49 「示例歌」: the light snaps on, a big empty room
def s12(t, lt, dur):
    on = lightOn(t, Ls(0))
    z = lerp(.74, .64, ease(lt / dur))
    cam(t, 980, 520, z)
    roomBack(t, 'him', lightsOn=0.0, flowerDry=1.0, switchOn=1.0)
    look = ease(seg(t, Ls(0) + 1.3, Ls(0) + 2.2))
    Em = feel('sad', t, dict(aR=lerp(1.4, .1, ease(seg(t, Ls(0) + .2, Ls(0) + .8))), lookX=lerp(-.5, .8, look)))
    om = fo(Em, view='q' if look > .5 else 'q', flip=look < .5, boilKey='him12')
    him(30, FLOOR, U, om)
    camEnd()
    nightVeil(.9 * (1 - on))
    if on > 0 and t - Ls(0) < .3:
        flash(.18 * (1 - (t - Ls(0)) / .3), '#FFF4D8')


# ================================================================ S13 42.49–50.69 示例歌词 占位文字
def s13(t, lt, dur):
    t0 = shotT('S13')[0]
    k = ease(seg(t, t0, t0 + 3.0))
    cam(t, lerp(1360, 1560, k), lerp(560, 590, k), lerp(1.12, 1.4, ease(lt / dur)))
    tc = Lc(1, 7) + .4          # after 「床」: he picks up her hair clip from her pillow
    got = t > tc + .5
    r = roomBack(t, 'him', lightsOn=0.0, flowerDry=1.0, bedKw=dict(clip=not got))
    st = BED_Y - 4.2 * BED_S + 4
    reach = ease(seg(t, tc - .2, tc + .3)) * (1 - ease(seg(t, tc + .55, tc + 1.1)))
    Em = feel('sad', t, dict(aR=lerp(.15, .9, reach) if not got else .55, aL=-.5, lookX=.9 if t < tc + 1.0 else .3, lookY=.6 if got else .1))
    om = fo(Em, view='q', boilKey='him13', dx=.5 * reach)
    seat(him, 1400, st, U, om)
    if got:
        hx, hy = handXY(1400, st + 2 * U, U, om, 'R')
        hairClip(hx + 4, hy - 8, 1.25, -.3, key='clip13')
        paint(ellPts(hx, hy, U * .45, U * .45, 10), wash=PAL['clay'], ink=INK, sw=.6)
    camEnd()
    tint('#D8E2FF', .12, skia.BlendMode.kMultiply)


# ================================================================ S14 50.69–55.26 示例歌 词占位文字 (on / off, the same)
def s14(t, lt, dur):
    togg = [Lc(2, 0), Lc(2, 3) - .05, Lc(2, 5) - .05, Lc(2, 6) + .1, Lc(2, 7)]
    n = sum(1 for x in togg if t >= x)
    on = 1.0 if n % 2 == 0 else 0.0
    cam(t, 120, 560, lerp(1.32, 1.4, lt / dur))
    roomBack(t, 'him', lightsOn=0.0, flowerDry=1.0, switchOn=on, bed=False)
    bumpA = max([math.exp(-max(0, t - x) * 12) for x in togg if t >= x - .1] + [0])
    Em = feel('sad', t, dict(aR=1.42 + .08 * bumpA, aL=-.4, lookX=.7 if n >= 2 else -.4))
    om = fo(Em, view='q', flip=True, boilKey='him14')
    him(30, FLOOR, U, om)
    lights = [scr(*SWITCH) + (90, .3)]
    camEnd()
    nightVeil(.92 * (1 - on), lights)


# ================================================================ S15 55.26–61.51 示例歌词 占位文字
def s15(t, lt, dur):
    cam(t, 1520, 560, lerp(1.5, 1.6, lt / dur))
    roomBack(t, 'him', lightsOn=0.0, flowerDry=1.0, bedKw=dict(night=.4))
    st = BED_Y - 4.2 * BED_S + 4
    t_off, t_dim, t_back = Lc(3, 4) - .3, Lc(3, 6), Lc(3, 7) + .4
    off = ease(seg(t, t_off, t_off + .7)) * (1 - ease(seg(t, t_back, t_back + .7)))
    grey = ease(seg(t, t_dim, t_dim + .8))
    hug = ease(seg(t, t_back + .3, t_back + 1.0))
    Em = feel('sad', t, dict(aR=lerp(.2, .55, off), aL=-.6, lookX=lerp(.2, .9, off), lookY=.4))
    om = fo(Em, view='q', boilKey='him15', dx=.3 * off)
    seat(him, 1400, st, U, om)
    bx, by = 1400 + 5.6 * U, st - 2.0 * U
    hx2, hy2 = lerp(bx, 1400 + 9.5 * U, off), lerp(by, st - 3.4 * U, off)
    if hug > .01:
        hx2, hy2 = lerp(hx2, 1400 + 5.0 * U, hug), lerp(hy2, st - 1.6 * U, hug)
    beat = max(0, math.sin(t * 6.5)) ** 8 * (1 - grey)
    crackedHeart(hx2, hy2, 46, crack=1.0, grey=grey, band=1.0, key='ch15', beat=beat)
    if grey < .9:
        glow(hx2, hy2, 140, '#FF6A7A', .35 * (1 - grey))
    lights = [scr(hx2, hy2) + (230 * 1.55, .55 * (1 - grey) + .2), scr(1960, 560) + (380, .45)]
    camEnd()
    nightVeil(.9, lights)


# ================================================================ S16 61.51–65.48 示例歌词占位文: calendar pages, clock, the tin fills
MONTHS = ['11月', '12月', '1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月']


def monthPage(x, y, label, key, a=1.0, rot=0.0):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-95, 0, 190, 220), wash='#FFFDF6', washOp=int(255 * a), ink=INK if a > .5 else None, sw=.8, lite=True)
    paint(rectPts(-95, 0, 190, 54), wash='#C8564F', washOp=int(255 * a), ink=INK if a > .5 else None, sw=.6, lite=True)
    text(label, 0, 28, 32, '#FFF6E8', face=WENKAI, shadow=False, a=a)
    for r in range(5):
        for c in range(7):
            G.c.drawCircle(-77 + c * 26, 74 + r * 30, 3, skia.Paint(AntiAlias=True, Color=skcol('#8A7A88', .7 * a)))
    pop()


def timeLapse(t, t0, t1, who):
    k = seg(t, t0 + .2, t1 - .3)
    n = len(MONTHS) - 1
    idx = min(n, int(k * n))
    sub = k * n - idx
    day = .5 + .5 * math.cos((t - t0) * 9)
    cx = 735 if who == 'him' else W - 735
    roomBack(t, who, lightsOn=0.0, flowerDry=1.0, calendarK=0, bed=False, tinOnDesk=True, tinFill=lerp(.4, 1.35, k),
             clockHM=(int((t - t0) * 40) % 12, ((t - t0) * 480) % 60), lamp=1)
    # tear-off month pages
    monthPage(cx, 300, MONTHS[min(n, idx + 1)], key='mp' + who + str(idx + 1))
    if idx < n:
        fl = ease(sub)
        monthPage(cx - 260 * fl, 300 - 200 * fl, MONTHS[idx], key='mp' + who + str(idx), a=1 - fl * .8, rot=-1.2 * fl)
    G.c.drawCircle(cx, 294, 6, skia.Paint(AntiAlias=True, Color=skcol(INK)))
    return day


def s16(t, lt, dur):
    t0, t1 = shotT('S16')
    cam(t, 820, 500, 1.55)
    day = timeLapse(t, t0, t1, 'him')
    camEnd()
    tint('#3A4378', .5 * (1 - day), skia.BlendMode.kMultiply)
    tint('#FFE9C0', .25 * day, skia.BlendMode.kSoftLight)


# ================================================================ S17 65.48–68.87 示例歌词占 (and S22: writing at the desk)
def deskWriter(t, who, hair=0.0, glasses=False, emo_='sad', key='dw', tinFill=1.15, writing=True, noteCol=None):
    st = CHAIR_SEAT
    cxw = X(CHAIR_X, who)
    roomBack(t, who, lightsOn=0.0, flowerDry=1.0, tinOnDesk=True, tinFill=tinFill, lamp=1)
    chairSide(cxw, FLOOR, st, key=key + 'ch', flip=who == 'her')
    wr = math.sin(t * 9) * .12 if writing else 0
    E = feel(emo_, t, dict(aR=.42 + wr, aL=-.3, lookX=.5, lookY=.8))
    o = fo(E, view='q', flip=who == 'her', boilKey=key + who, gloom=0)
    nx = X(690, who)
    stickyNote(nx, DESK_TOP - 3, 70, 0, noteCol or (NOTE_Y if who == 'him' else NOTE_P), key=key + 'note', fold=.82)
    seat(lambda x, y, u, oo: person(who, x, y, u, oo, hair=hair, glasses=glasses), cxw, st, U, o)
    hx, hy = handXY(cxw, st + 2 * U, U, o, 'R')
    fountainPen(hx + (8 if who == 'him' else -8), hy + 4, 22, ang=-.9 if who == 'him' else -2.25, key=key + 'pen')
    paint(ellPts(hx, hy, U * .42, U * .42, 10), wash=o['col'] if 'col' in o else (ME if who == 'him' else HER)['col'], ink=INK, sw=.6)
    # desk lamp light (lamp at x 1010 flipped)
    lx = X(1010 - 55, who)
    glow(lx, DESK_TOP - 160, 420, '#FFD48A', .7)
    return [scr(lx, DESK_TOP - 120) + (520 * (eng.CAM[2] if eng.CAM else 1), 1.0)]


def s17(t, lt, dur):
    t0, t1 = shotT('S17')
    cam(t, 700, 560, 1.55)
    hair = ease(seg(t, Lc(5, 1), Lc(5, 4) + .2))
    lights = deskWriter(t, 'him', hair=hair, glasses=t > Lc(5, 4), key='dw17')
    camEnd()
    nightVeil(.8, lights)


# ================================================================ S18 68.87–75.48 示例歌词占 位文字示例歌
def s18(t, lt, dur):
    from wx import shopStreet
    t0, t1 = shotT('S18')
    cam(t, 960, 540, 1.0)
    shopStreet(t, key='st18', ground=860, dusk=1.0)
    # her walking away to the right with the suitcase
    wk = (t - t0) * .9
    hx = lerp(980, 2250, seg(t, t0 + .3, t1 - .2))
    Eh = feel('sad', t, dict(walk=wk, aL=.2, aR=-.2))
    her(hx, 880, U, fo(Eh, view='side', boilKey='her18'))
    suitcase(hx - 120, 880, .95, key='suit18', tilt=.15)
    # him holding the 「快乐」 balloon; it slips away on 「快乐」
    rel = Lc(6, 5) - .1
    Em = feel('sad', t, dict(aR=1.0, aL=-.3, lookX=.8, lookY=-.4 if t > rel + .3 else .1))
    om = fo(Em, view='q', boilKey='him18')
    him(560, 880, U, om)
    px, py = handXY(560, 880, U, om, 'R')
    paint(ellPts(px, py, U * .42, U * .42, 10), wash=PAL['clay'], ink=INK, sw=.6)
    fly = max(0, t - rel)
    bx = px + 40 + fly * 70 + math.sin(t * 1.3) * 12
    by = py - 260 - fly * fly * 30 - fly * 90
    balloon(bx, by, 62, '#F7D36E', '快乐', sx=px if fly <= 0 else bx - 30 + math.sin(t * 3) * 10,
            sy=py if fly <= 0 else by + 230, key='bal18', rot=.1 * math.sin(t * 1.7))
    camEnd()
    tint('#B79BD8', .12, skia.BlendMode.kMultiply)


# ================================================================ S19 75.48–78.17 示例歌词占: the photos fade one by one
def photoClose(t, who, starts, key='pc'):
    P = PAL_ROOM[who]
    flatRect(-200, -200, W + 400, H + 400, P['wall'])
    for i in range(-4, 30):
        G.c.drawRect(skia.Rect.MakeXYWH(i * 120, -200, 46, H + 400), skia.Paint(Color=skcol(P['stripe'], .55)))
    pts = [[lerp(160, 1760, i / 24), 210 + 70 * math.sin(i / 24 * math.pi)] for i in range(25)]
    boilSeed(key + 'str')
    inkLine(pts, 1.4, '#B59A7A', 'inkfine', .3)
    stringLights(t, -100, 2020, 70, sag=50, n=14, key=key + 'sl', on=.6)
    for i in range(4):
        k = (i + .5) / 4
        px, py = lerp(160, 1760, k), 210 + 70 * math.sin(k * math.pi)
        d = ease(seg(t, starts[i], starts[i] + .55))
        polaroidMini(px, py + 220, 330, (hash1(i * 3.1) - .5) * .16, i + (0 if who == 'him' else 2), d, key=f'{key}{i}')


def s19(t, lt, dur):
    cam(t, lerp(900, 1020, lt / dur), 520, 1.0)
    photoClose(t, 'him', [Lc(7, j) for j in range(1, 5)], key='pc19')
    camEnd()
    tint('#D8E2FF', .15, skia.BlendMode.kMultiply)


# ================================================================ S20 78.17–81.33 示例歌词占
def sleeper(t, who, key='slp', dream=False):
    """him / her asleep in bed: tucked in, head on own pillow, blanket up to the chin (front view)"""
    x0 = X(BED_X - 154, who)
    breathe = .03 * math.sin(t * 2.2)
    o = dict(view='front', eyes='closed', mouth='smile' if dream else None, noShadow=True, boilKey=key, aL=-.6, aR=-.6, sq=breathe,
             blush=.3 if dream else 0)
    person(who, x0, 842, U, o)
    blanket(X(BED_X, who), BED_Y, BED_W, BED_S, key=key + 'blk', night=.4, lump=0.0, top=700)


def s20(t, lt, dur):
    t0, t1 = shotT('S20')
    cam(t, 1520, 520, 1.38)
    roomBack(t, 'him', lightsOn=0.0, flowerDry=1.0, bedKw=dict(night=.4, blanketK=0))
    sleeper(t, 'him', key='slp20', dream=t < Lc(8, 4) + .1)
    pop_ = Lc(8, 4) + .1
    k = ease(seg(t, t0 + .3, t0 + 1.0))
    if t < pop_:
        thoughtCloud(1460, 330, 360, 260, k, tail=(1350, 560), key='tc20')
        if k > .5:
            clawd(1460, 440, 12.5 * k, dict(col='#EE9AAE', dk='#C0637B', lt='#FBD0DA', hat='flower', eyes='happy', mouth='smile',
                                           noShadow=True, boilKey='dr20', view='front', aL=.8 + .3 * math.sin(t * 5), aR=.3, lite=True))
    else:
        a = t - pop_
        if a < .4:
            for i in range(10):
                ang = i / 10 * TAU
                r = 90 + 260 * a
                sparkle(1460 + math.cos(ang) * r, 330 + math.sin(ang) * r * .7, 18 * (1 - a / .4), '#FFFFFF')
    lights = [scr(1460, 330) + (320, .6 if t < pop_ else .2), scr(1960, 560) + (360, .35)]
    camEnd()
    nightVeil(.88, lights)


# ================================================================ S21 81.33–85.98 示例歌词占位文字示
def heartDrift(t, t0, t1, who, key='hd'):
    nightSkyHill(t, key=key + 'sky', tree=True)
    x = 720
    gy = hillY2(x)
    E = feel('neutral', t, dict(eyes='normal', lookY=-.6, lookX=.4, aL=-.3, aR=-.3))
    person(who, x, gy, U * 1.05, fo(E, view='q', boilKey=key + who))
    grey = ease(seg(t, t0 + .6, t0 + 1.8))
    up = ease(seg(t, t0 + 1.9, t1 - .2))
    hx = lerp(x + 2.4 * U, 1500, up) + math.sin(t * 1.6) * 20 * up
    hy = lerp(gy - 4.4 * U, 160, up)
    r = lerp(40, 10, up)
    if up < .92:
        if up > .01:
            boilSeed(key + 'st')
            inkLine([[hx, hy + r], [hx - 10, hy + r + 60 * (1 - up)]], .6, '#C9C4D8', 'inkfine', .5)
        crackedHeart(hx, hy, r, crack=0, grey=grey, band=0, key=key + 'h')
    else:
        flowerStar(1500, 160, 12, .2 + .2 * math.sin(t * 5), key=key + 'star')


def s21(t, lt, dur):
    t0, t1 = shotT('S21')
    cam(t, 960, lerp(540, 470, ease(lt / dur)), 1.0)
    heartDrift(t, t0, t1, 'him', key='hd21')
    camEnd()


# ================================================================ chorus 1
def s22(t, lt, dur):
    cam(t, 700, 560, lerp(1.45, 1.55, lt / dur))
    lights = deskWriter(t, 'him', key='dw22', emo_='sad', tinFill=1.25)
    camEnd()
    nightVeil(.8, lights)


def s23(t, lt, dur):
    t0, t1 = shotT('S23')
    cam(t, 1200, 540, 1.12)
    deskTopScene(t, 'him', tinFill=1.25, extraNotes=12)
    prog = ease(seg(t, t0 + .1, Lc(10, 6) - .25))
    fold = ease(seg(t, t1 - 1.5, t1 - 1.1))
    landT = t1 - .45
    nx, ny, nw = NOTE
    if t < t1 - 1.05:
        writtenNote('想你', nx, ny, nw, prog, t, NOTE_Y, key='n23', size=110, pen=prog < 1, fold=fold)
        if prog >= 1:
            fountainPen(nx + 260, ny + 230, 44, ang=-1.1, key='fpen')
    else:
        fountainPen(nx + 260, ny + 230, 44, ang=-1.1, key='fpen')
        k = seg(t, t1 - 1.05, landT)
        tx, ty = TIN_T[0] - 60, TIN_T[1] - 30
        px, py = arcPt((nx, ny), (tx, ty), -220, ease(k))
        foldedNote(px, py, lerp(nw * .9, 90, ease(k)), k * 2.4, NOTE_Y, key='fly23')
    lights = [scr(820, 470) + (700 * eng.CAM[2], 1.0), scr(TIN_T[0], TIN_T[1]) + (420 * eng.CAM[2], .55)]
    camEnd()
    darkness(.55, lights, BG)


def s24(t, lt, dur):
    """示例歌词占: the tin goes under the bed, the sheet is smoothed, a squeezed smile"""
    t0, t1 = shotT('S24')
    cam(t, 1400, 600, 1.48)
    push_ = ease(seg(t, t0 + .5, t0 + 1.9))
    smooth = seg(t, t0 + 2.4, t0 + 3.6)
    smile = t > t0 + 4.0
    roomBack(t, 'him', lightsOn=0.0, flowerDry=1.0, bedKw=dict(tinUnder=push_ if push_ > .98 else 0.0))
    if push_ < .98:
        tx = lerp(1200, 1440, push_)
        tinFront(tx, FLOOR + 20 - 18 * push_, 120, 'him', fill=1.25, key='tin24')
    bend = 1 - ease(seg(t, t0 + 3.7, t0 + 4.1))
    if smile:
        E = feel('happy', t, dict(emote='sweat', aL=-.2, aR=-.2))
    else:
        E = feel('sad', t, dict(aR=lerp(.1, .5, bend) if push_ < 1 else .3 + .3 * math.sin(smooth * TAU * 2), aL=-.3, lookY=.8, lookX=.5))
    mx = 1060 if t < t0 + 2.2 else lerp(1060, 1250, ease(seg(t, t0 + 2.0, t0 + 2.6)))
    om = fo(E, view='q', boilKey='him24', rot=.18 * bend * (1 if not smile else 0), sq=.12 * bend)
    him(mx, FLOOR + 20, U, om)
    camEnd()
    tint('#D8E2FF', .12, skia.BlendMode.kMultiply)


def tiptoe(t, t0, t1, who, key='tt', xo=0):
    nightSkyHill(t, key=key + 'sky', tree=True)
    x = 900 + xo
    gy = hillY2(x)
    top = crate(x, gy + 8, 1.9, key=key + 'cr')
    reach = ease(seg(t, t0 + 3.6, t0 + 4.4))
    toe = .5 + .5 * math.sin(t * 2.2)
    E = feel('hopeful', t, dict(aR=lerp(.4, 1.5, reach), aL=.3, emote=None))
    o = fo(E, view='qback', boilKey=key + who, dy=-.35 - .15 * toe, sy=1.03 + .02 * toe, flip=who == 'her')
    person(who, x, top, U * .9, o)
    sx, sy = (1320 + xo, 230) if who == 'him' else (1320 + xo, 230)
    fk = ease(seg(t, t0 + 3.0, t0 + 4.0))
    flowerStar(sx, sy, 40, .3 + .7 * fk if fk > 0 else .2 + .2 * math.sin(t * 6), key=key + 'fs')
    if .5 < fk < 1:
        for i in range(8):
            a_ = i / 8 * TAU
            sparkle(sx + math.cos(a_) * 110 * fk, sy + math.sin(a_) * 110 * fk, 16 * (1 - fk) + 6, '#FFFFFF')


def s25(t, lt, dur):
    t0, t1 = shotT('S25')
    cam(t, 1000, lerp(520, 470, ease(lt / dur)), 1.0)
    tiptoe(t, t0, t1, 'him', key='tt25')
    camEnd()


def orbit(t, t0, who, key='orb'):
    """photos circling around him / her like a carousel (back half behind, front half in front)"""
    cx = X(1150, who)
    roomBack(t, who, lightsOn=.3, flowerDry=1.0, bedKw=dict(night=.4))
    n = 8
    ang0 = (t - t0) * .8
    items = []
    for i in range(n):
        a = ang0 + i / n * TAU
        px, py = cx + math.cos(a) * 420, 770 + math.sin(a) * 70 - 14 * math.sin(a * 2 + i)
        items.append((math.sin(a), px, py, i))
    items.sort()
    for s_, px, py, i in items:
        if s_ < 0:
            polaroidMini(px, py, 100 + 18 * s_, .15 * math.cos(ang0 + i), i, 0.0, key=f'{key}{i}')
    E = feel('sad', t, dict(lookX=math.cos(ang0 + 1.2), lookY=-.2, aL=-.3, aR=-.3, emote=None))
    person(who, cx, FLOOR, U, fo(E, view='front', boilKey=key + who))
    for s_, px, py, i in items:
        if s_ >= 0:
            polaroidMini(px, py, 100 + 18 * s_, .15 * math.cos(ang0 + i), i, 0.0, key=f'{key}{i}')
    return [scr(cx, 600) + (560, .8)]


def s26(t, lt, dur):
    t0, t1 = shotT('S26')
    cam(t, 1150, 560, lerp(1.25, 1.42, ease(lt / dur)))
    lights = orbit(t, t0, 'him', key='orb26')
    camEnd()
    nightVeil(.7, lights)


def cryClose(t, t0, t1, who, key='cry', noteCol=NOTE_Y):
    """half-body close-up: eyes closed, tears sliding down and dropping onto the note lying in the lap"""
    x = X(1400, who)
    st = BED_Y - 4.2 * BED_S + 4
    roomBack(t, who, lightsOn=0.0, flowerDry=1.0, bedKw=dict(night=.4))
    sob = .5 + .5 * math.sin(t * 3.4)
    E = dict(eyes='closed', mouth='wobble', blush=.4, aL=-1.15, aR=-1.15, sq=.03 * sob, view='front', boilKey=key + who, tint='blue', tintK=.15)
    seat(lambda xx, yy, u, oo: person(who, xx, yy, u, oo), x, st, U, E)
    body_y = st + 2 * U
    nyy = st + .35 * U
    stickyNote(x + .3 * U, nyy, 2.7 * U, -.1, noteCol, key=key + 'nt')
    for j in range(3):
        bt_ = t0 + 1.2 + j * 1.6
        if t > bt_:
            r = 9 + 15 * ease(seg(t, bt_, bt_ + .8))
            paint(ellPts(x - 22 + j * 24, nyy - 8 + j * 9, r, r * .8, 12), wash='#9EC3E8', washOp=130, ink=None)
    for sx_, sd in ((-1, 1), (1, 2)):
        tearDrops(t, x + sx_ * 2.05 * U, body_y - 5.55 * U, U, seed=sd, n=2, rate=.9, fall=2.2 * U, size=1.3)
    # drops falling from the chin to the note
    for j in range(2):
        ph = frac(t * .8 + j * .5)
        dx_ = x + (j - .5) * 1.4 * U
        dy_ = lerp(body_y - 3.2 * U, nyy - .2 * U, ph)
        paint([[dx_, dy_ - 9], [dx_ + 6, dy_], [dx_, dy_ + 6], [dx_ - 6, dy_]], wash='#BFE6FF', washOp=int(230 * (1 - ph * .5)), ink=INK, sw=.4, curv=1)


def s27(t, lt, dur):
    t0, t1 = shotT('S27')
    cam(t, 1400, 590, lerp(2.15, 2.25, lt / dur))
    cryClose(t, t0, t1, 'him', key='cry27')
    lights = [scr(1400, 520) + (520, .75)]
    camEnd()
    nightVeil(.75, lights)


def walkShades(t, t0, t1, who, x0, x1, y, key='ws', tearAt=None, lane=0):
    wk = (t - t0) * 1.15
    x = lerp(x0, x1, seg(t, t0, t1))
    E = feel('cool', t, dict(walk=wk, aL=.25, aR=-.25))
    d = 1 if x1 > x0 else -1
    o = fo(E, view='side', flip=d < 0, boilKey=key + who, dy=-.3 * abs(math.sin(wk * math.pi)))
    if tearAt and tearAt[0] < t < tearAt[1]:
        o['aR'] = 1.6
    person(who, x, y, U * 1.05, o)
    if tearAt and tearAt[0] - .8 < t < tearAt[0] + .1:
        tearDrops(t, x + d * 3.6 * U * 1.05, y - 5.2 * U * 1.05, U, seed=9, n=1, rate=1.2, fall=1.3 * U, a=.9)
    return x


def s28(t, lt, dur):
    from wx import shopStreet
    from hl import walker
    t0, t1 = shotT('S28')
    ta, tb = Lc(15, 6) - .4, Lc(15, 6) + .9
    x = lerp(300, 1650, seg(t, t0, t1))
    push_ = ease(seg(t, ta - .5, ta)) * (1 - ease(seg(t, tb, tb + .5)))
    cam(t, lerp(lerp(700, 1300, seg(t, t0, t1)), x + 40, push_), lerp(540, 690, push_), 1.0 + .75 * push_)
    shopStreet(t, key='st28', ground=860)
    for i in range(6):
        wx_ = (i * 420 + (t - t0) * (60 if i % 2 else -70)) % 2600 - 300
        walker(wx_, 830 - 10 * (i % 2), 22, t, i, dirn=1 if i % 2 else -1, umb=False, view='side')
    wk = (t - t0) * 1.15
    E = feel('cool', t, dict(walk=wk, aL=.25, aR=-.25, emote='music' if t < ta else None))
    o = fo(E, view='side', boilKey='ws28him', dy=-.3 * abs(math.sin(wk * math.pi)))
    wipe = tb - .35 < t < tb + .25
    if wipe:
        o['aR'] = 1.7
    him(x, 900, U * 1.05, o)
    if ta < t < tb:
        k = seg(t, ta, tb - .35)
        ex, ey = x + 3.0 * U * 1.05, 900 - 5.0 * U * 1.05
        paint([[ex, ey + 50 * k - 16], [ex + 9, ey + 50 * k], [ex, ey + 50 * k + 9], [ex - 9, ey + 50 * k]], wash='#BFE6FF', ink=INK, sw=.6, curv=1)
        G.c.drawLine(ex, ey, ex, ey + 50 * k, skia.Paint(AntiAlias=True, Color=skcol('#DDF3FF', .7), StrokeWidth=4))
    camEnd()


def phoneBed(t, t0, t1, who, mode_fn, key='pb', name='她'):
    x = X(1400, who)
    st = BED_Y - 4.2 * BED_S + 4
    roomBack(t, who, lightsOn=0.0, flowerDry=1.0, bedKw=dict(night=.4))
    mode = mode_fn(t)
    E = feel('hopeful' if mode in ('call', 'incoming') else 'sad', t, dict(aR=.75, aL=.6, lookY=.5, lookX=.3 if who == 'him' else -.3, emote=None))
    o = fo(E, view='q', flip=who == 'her', boilKey=key + who)
    seat(lambda xx, yy, u, oo: person(who, xx, yy, u, oo), x, st, U, o)
    hx, hy = handXY(x, st + 2 * U, U, o, 'R')
    phoneP(hx, hy - 20, 64, .1 if who == 'him' else -.1, lit=0 if mode == 'dark' else 1.0, case='#7FB8E6' if who == 'him' else '#EE9AAE',
           key=key + 'ph')
    paint(ellPts(hx, hy, U * .42, U * .42, 10), wash=o.get('col', (ME if who == 'him' else HER)['col']), ink=INK, sw=.6)
    return mode, hx, hy


def s29(t, lt, dur):
    t0, t1 = shotT('S29')
    hang = Lc(16, 6) + .25

    def mode_fn(tt):
        if tt < t0 + .5:
            return 'dark'
        if tt < hang:
            return 'call'
        if tt < hang + 1.0:
            return 'ended'
        return 'dark'
    cam(t, 1580, 560, 1.45)
    mode, hx, hy = phoneBed(t, t0, t1, 'him', mode_fn, key='pb29')
    lights = [scr(hx, hy) + (260, .7 if mode != 'dark' else .2)]
    camEnd()
    nightVeil(.85, lights)
    phoneCard(1450, 470, 640, mode, t, t0 + .5, name='她', key='pcard29', case='#7FB8E6')


def wallFine(t, t0, who, key='wf', stickAt=None):
    """a big framed photo of the two of them; a 「我很好！」 note gets pressed on over it"""
    P = PAL_ROOM[who]
    flatRect(-300, -300, W + 600, FLOOR + 300, P['wall'])
    for i in range(-6, 30):
        G.c.drawRect(skia.Rect.MakeXYWH(i * 90, -300, 34, FLOOR + 300), skia.Paint(Color=skcol(P['stripe'], .55)))
    flatRect(-300, FLOOR, W + 600, 600, P['floor'])
    inkLine([[-300, FLOOR], [W + 300, FLOOR]], 1.0, INK, 'ink', 0)
    fx = X(840, who)
    boilSeed(key + 'fr')
    paint(rectPts(fx - 230, 220, 460, 380, 2), wash='#C9A27A', fill='#8A5A36', fillOp=60, ink=INK, sw=1.2)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(fx - 200, 250, 400, 320))
    snapScene(fx - 200, 250 - 40, 400, 1)
    G.c.restore()
    paint(rectPts(fx - 200, 250, 400, 320), ink=INK, sw=.8)
    nx, ny = X(990, who), 470
    k = pk(t, stickAt, .22) if stickAt else 0
    if k > 0:
        postit(nx, ny, 230, -.08 * (1 if who == 'him' else -1), '我很好！', col=NOTE_Y if who == 'him' else NOTE_P, key=key + 'pi', size=48, k=k)
    sx = X(1250, who)
    reach = ease(seg(t, stickAt - .6, stickAt - .05)) * (1 - ease(seg(t, stickAt + .35, stickAt + .75))) if stickAt else 0
    after_ = stickAt and t > stickAt + .3
    nod = math.sin((t - stickAt - .4) * 9) * math.exp(-(t - stickAt - .4) * 2) if stickAt and t > stickAt + .4 else 0
    E = feel('happy', t, dict(emote='sweat', aL=-.2, aR=-.2, dy=.25 * nod)) if after_ else feel('neutral', t, dict(aL=-.2, aR=-.2, lookX=-.9))
    o = fo(E, view='q', flip=who == 'him', boilKey=key + who)
    o, side = armToward(o, sx, FLOOR, U * 1.2, nx, lerp(-.2, .75, reach))
    person(who, sx, FLOOR, U * 1.2, o)
    if reach > .05:
        hx, hy = handXY(sx, FLOOR, U * 1.2, o, side)
        handDot(hx, hy, who)
    if 0 < k < 1 or (stickAt and abs(t - stickAt) < .3):
        hx, hy = handXY(sx, FLOOR, U * 1.2, o, side)
        if reach > .5 and k <= 0:
            postit(hx - 40 * (1 if who == 'him' else -1), hy - 10, 200, -.1, '我很好！', col=NOTE_Y if who == 'him' else NOTE_P,
                   key=key + 'pih', size=42, k=1.0)


def s30(t, lt, dur):
    t0, t1 = shotT('S30')
    cam(t, 1000, 560, 1.0)
    wallFine(t, t0, 'him', key='wf30', stickAt=Lc(17, 1))
    camEnd()
