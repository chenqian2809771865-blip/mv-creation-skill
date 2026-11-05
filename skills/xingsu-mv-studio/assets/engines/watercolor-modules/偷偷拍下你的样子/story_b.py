# story_b.py: 《偷偷拍下你的样子》 shots S10–S18. S17/S18 mirror S01: his camera, her on the bench, then both cameras at once.
import math
from eng import *
import eng
from clawd import *
from props import puff, sparkle, sparkles, floatHearts, bubble, stamp, banner, bush, lamp, tree
from common import *
from ch import rr, heart, bobaCup, WENKAI, HOT, PINK, PINKDK, CREAM, fo
from tp import *
from sets2 import seat, parkBench, fairyLights
from story_a import hop, herCam


# =====================================================================================
# S10 15.31–17.00 示例歌词占位文字 · quiz in her head: a red ✗ lands on one option per beat
def s10(t, lt, dur):
    cam(t, 960, 540, 1.0)
    flatRect(-200, -200, W + 400, H + 400, '#ECE4F8')
    for i in range(-2, 40):
        G.c.drawLine(i * 60, -200, i * 60, H + 200, skia.Paint(AntiAlias=True, Color=skcol('#C9B8E8', .5), StrokeWidth=1.5))
        G.c.drawLine(-200, i * 60, W + 200, i * 60, skia.Paint(AntiAlias=True, Color=skcol('#C9B8E8', .5), StrokeWidth=1.5))
    opts = [('A', '递伞'), ('B', '抱抱'), ('C', '讲个笑话'), ('D', '买杯奶茶')]
    pos = quizCard(150, 70, 1000, 840, '怎么安慰他？', opts, key='qz10')
    from props_bingbian import xmark
    for i, kk in enumerate((36, 37, 38, 39)):
        if after(t, kk, .04):
            xmark(pos[i][0] + 260, pos[i][1], 58, t - B[kk] + .04)
    keys = [[0, 'nervous'], [B[37] - .06, 'shy'], [B[38] - .06, 'nervous'], [B[39] - .06, 'dizzy']]
    o = em(t, keys)
    o.update(view='q', flip=True)
    her(1520, 900, 46, o)
    # thought dots from her head to the card
    for j in range(3):
        G.c.drawCircle(1330 - j * 50, 420 - j * 40, 14 - j * 3, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF')))
    stamp(['太刻意？', '太突然！', '好冷…', '示例歌词占'][max(0, lastBeat(t, [36, 37, 38, 39]))], 1520, 300, 62, HOT,
          t - B[[36, 37, 38, 39][max(0, lastBeat(t, [36, 37, 38, 39]))]], rot=.08, life=.42)
    camEnd()


# =====================================================================================
# S11 17.00–18.68 示例歌词占位文字 · dusk path; her confession bubble and she herself shrink on every beat
def s11(t, lt, dur):
    cam(t, 960, 540, 1.0)
    gradRect(-200, -200, W + 400, 700, ['#FFB88C', '#F29AAE', '#9A7AC4'])
    from sets import sunDisc
    sunDisc(1500, 560, 110, col='#FFE6B8', glowCol='#FFC7A0', key='sun11')
    skyline(640, '#7A5A98', '#FFD98A', .5, key='sl11')
    flatRect(-200, 640, W + 400, H, '#D9A8A0')
    gradRect(-200, 640, W + 400, 100, ['#C08A98', '#D9A8A0'])
    for i, x in enumerate((140, 520, 1420, 1800)):
        tree(x, 700, 62, key=f'tr11{i}', col='#E39A8E' if i % 2 else '#D8889A')
    lamp(330, 720, 40, on=.6, key='lp11')
    lamp(1640, 720, 40, on=.6, key='lp11b')
    m = feel('neutral', t, dict(view='q', flip=True, aL=.3, aR=.3))
    if after(t, 43, .06):
        m = feel('confused', t, dict(view='q', flip=True))
    him(1300, 880, 34, m)
    us = [34, 30, 23, 14]
    u = steps(t, [41, 42, 43], us, d=.12)
    i = max(0, lastBeat(t, [40, 41, 42, 43]))
    keys = [[0, 'determined'], [B[41] - .06, 'nervous'], [B[42] - .06, 'shy'], [B[43] - .06, 'scared']]
    o = em(t, keys)
    o.update(view='q', aL=.5, aR=.5)
    her(700, 880, u, o)
    txts = ['我喜欢你——', '我喜欢…', '我…', '…']
    sizes = [74, 60, 48, 36]
    a = t - B[40 + i]
    k = backOut(clamp((a + .04) / .14))
    bubble(lerp(860, 760, i / 3), 880 - 9 * u - 120 + i * 40, txts[i], sizes[i], tail=(700 + 3 * u, 880 - 8 * u), k=k, key=f'bb11{i}')
    stamp('怂', 520, 520, 120, HOT, t - B[43], rot=-.15)
    camEnd()


# =====================================================================================
# S12 18.68–20.37 示例歌词占位文字 · the snow globe of "just friends" slips, flies, is caught
def s12(t, lt, dur):
    cam(t, 960, 540, 1.0)
    gradRect(-200, -200, W + 400, H + 400, ['#1E2456', '#33306E', '#4A3A7E'])
    from hl import stars
    stars(t, 12, 70, -100, -100, W + 100, H, a=.9)
    sparkles(t, 21, 12, 100, 100, 1820, 900, 14, '#FFF3C8')
    u = 46
    x, y = 860, 900
    keys = [[0, 'hopeful'], [B[45] - .06, 'surprised'], [B[46] - .06, 'scared'], [B[47] - .06, 'relieved']]
    o = em(t, keys)
    up = after(t, 45, .06) and not after(t, 47, .06)
    o.update(aL=1.5 if up else (-.15 if t > B[47] - .06 else .45), aR=1.5 if up else (-.15 if t > B[47] - .06 else .55))
    her(x, y, u, o)
    # globe path: rest at her right hand -> pops up (k45) -> peak (k46) -> caught in a hug (k47)
    rest = (1200, 720)
    hug = (880, 790)
    t45, t46, t47 = B[45] - .05, B[46], B[47]
    if t < t45:
        gx, gy = rest[0], rest[1] + 6 * math.sin(t * 3)
        rot = 0
    elif t < t46:
        k = easeOut(seg(t, t45, t46))
        gx, gy = lerp(rest[0], 1180, k), lerp(rest[1], 300, k)
        rot = 1.2 * k
    elif t < t47:
        k = easeIn(seg(t, t46, t47))
        gx, gy = lerp(1180, hug[0], k), lerp(300, hug[1], k)
        rot = 1.2 + 1.1 * k
    else:
        gx, gy = hug[0], hug[1] + 8 * math.exp(-(t - t47) * 10) * math.cos((t - t47) * 40)
        rot = 2 * math.pi + .1 * math.exp(-(t - t47) * 6) * math.sin((t - t47) * 30)
    snowGlobe(gx, gy, 132, t, key='sg12', shine=clamp(1 - abs(t - B[44] - .1) / .3) + (1 if t > t47 + .05 else 0) * .6, tilt=rot if t < t47 else rot - 2 * math.pi)
    if t46 - .3 < t < t47:
        for j in range(4):     # motion lines
            inkLine([[gx - 150 + j * 100, gy + 150], [gx - 150 + j * 100, gy + 230]], 1.2, '#FFFFFF', 'ink', 0)
    stamp('!', 1400, 560, 110, '#FFE36E', t - B[45], life=.4)
    stamp('啊啊啊', 600, 330, 70, '#FFFFFF', t - B[46], rot=-.1, life=.4)
    if after(t, 47, .04):
        bubble(560, 420, '呼～', 56, tail=(760, 560), k=clamp((t - B[47] + .04) / .14), key='bb12')
    camEnd()


# =====================================================================================
# S13 20.37–22.06 示例歌词占位文字 · her cork board fills with polaroids of him, one pinned per beat
WALLPICS = [(420, 200, -.12, 'read'), (600, 250, .08, 'boba'), (790, 190, -.05, 'wave'), (1130, 200, .1, 'smile'), (1320, 250, -.08, 'yawn'),
            (1500, 190, .06, 'read'), (440, 470, .07, 'smile'), (1480, 480, -.1, 'boba'), (640, 520, -.04, 'yawn'), (1290, 520, .05, 'wave')]
NEWPICS = [(48, 760, 400, .12, 'read'), (49, 1150, 410, -.1, 'boba'), (50, 560, 330, -.14, 'yawn'), (51, 960, 230, .03, 'smile')]


def s13(t, lt, dur):
    cam(t, 960, 520, lerp(1.0, 1.06, ease(lt / dur)))
    gradRect(-200, -200, W + 400, H + 400, ['#33295A', '#53427E'])
    for i in range(-2, 22):
        flatRect(i * 110, -100, 3, H + 200, '#FFFFFF', .03)
    from props_chuanshao import corkBoard
    corkBoard(320, 90, 1280, 560, key='cb13')
    for i, (x, y, r, pose) in enumerate(WALLPICS):
        polaroidPic(x, y, 150, r, 1, lambda cx, cy, iw, ih, p=pose: snap(cx, cy, iw, ih, 'him', p), key=f'wp{i}', pinCol='#7FB8E6')
    for i, (kk, x, y, r, pose) in enumerate(NEWPICS):
        if after(t, kk, .06):
            k = clamp((t - B[kk] + .06) / .16)
            polaroidPic(x, y, 180 if kk != 51 else 220, r, k, lambda cx, cy, iw, ih, p=pose: snap(cx, cy, iw, ih, 'him', p), key=f'np{i}', pinCol=HOT)
    fairyLights(t, 120, 1800, 50, sag=36, n=18, key='fl13')
    # her on the bed, hugging a pillow
    u = 40
    x, y = 960, 930
    keys = [[0, 'hopeful'], [B[50] - .06, 'shy'], [B[51] - .06, 'love']]
    o = em(t, keys)
    o.update(aL=1.0, aR=1.0)
    her(x, y, u, o)
    boilSeed('pil13')
    paint(rrPts(x - 190, y - 3.9 * u, 380, 140, 50), wash='#FFFDF6', fill='#F4E0E8', fillOp=60, ink=INK, sw=1)
    for j in (-1, 1):
        inkLine([[x + j * 120, y - 3.9 * u + 20], [x + j * 120, y - 3.9 * u + 120]], .5, '#E3B8C8', 'inkfine', 0)
    heart(x, y - 3.9 * u + 70, 30, '#F7A8C0', key='ph13', sw=.5, shine=False)
    # quilt in front
    boilSeed('q13')
    paint([[-200, 840], [W + 200, 820], [W + 200, H + 200], [-200, H + 200]], wash='#F2B5C5', fill='#E27A92', fillOp=40, ink=INK, sw=1.1)
    for i in range(14):
        heart(80 + i * 140, 900 + 40 * (i % 2), 14, '#FFFFFF', key=f'qh{i}', sw=.3, shine=False)
    for kk in (48, 49, 50, 51):
        stamp('啪', [760, 1150, 560, 960][kk - 48] + 110, [400, 410, 330, 230][kk - 48] - 120, 44, '#FFFFFF', t - B[kk], life=.35)
    if after(t, 51):
        floatHearts(t, 13, 6, 860, 120, 1060, 330, 16)
    camEnd()


# =====================================================================================
# S14 22.06–23.74 示例歌词占位文字 · night walk: a lamp lights per beat; their shadows' hands meet on the 4th
def shadowOf(fn, x, y, u, o, skew, sy=-.5, col='#1A1838', a=.5):
    G.c.save()
    pa = skia.Paint()
    pa.setColorFilter(skia.ColorFilters.Blend(skcol(col), skia.BlendMode.kSrcIn))
    pa.setAlphaf(a)
    G.c.saveLayer(None, pa)
    G.c.translate(x, y)
    m = skia.Matrix()
    m.setAll(1, skew, 0, 0, sy, 0, 0, 0, 1)
    G.c.concat(m)
    fn(0, 0, u, fo(o, noShadow=True))
    G.c.restore()
    G.c.restore()


def wallShadow(fn, x, y, u, o, sc, col='#1E1840', a=.55):
    """silhouette of a Clawd projected onto the wall: feet at (x, y), scaled sc"""
    G.c.save()
    pa = skia.Paint()
    pa.setColorFilter(skia.ColorFilters.Blend(skcol(col), skia.BlendMode.kSrcIn))
    pa.setAlphaf(a)
    G.c.saveLayer(None, pa)
    G.c.translate(x, y)
    G.c.scale(sc, sc)
    fn(0, 0, u, fo(o, noShadow=True, emote=None, blush=0, gloom=0))
    G.c.restore()
    G.c.restore()


def s14(t, lt, dur):
    pan = lt * 80
    cam(t, 960, 540, 1.0)
    gradRect(-200, -200, W + 400, 330, ['#141A44', '#2A2A62'])
    from hl import stars
    stars(t, 14, 40, -100, -100, W + 100, 200, a=.8)
    skyline(250, '#22224A', '#FFD98A', .6, key='sl14')
    # the long garden wall
    flatRect(-200, 240, W + 400, 640, '#6B5F98')
    G.c.save()
    G.c.translate(-pan, 0)
    for r in range(9):
        yy = 270 + r * 66
        off = 60 if r % 2 else 0
        G.c.drawLine(-200, yy, W + 400, yy, skia.Paint(AntiAlias=True, Color=skcol('#5A4F86', .7), StrokeWidth=2))
        for q in range(-2, 22):
            xx = q * 120 + off
            G.c.drawLine(xx, yy, xx, yy + 66, skia.Paint(AntiAlias=True, Color=skcol('#5A4F86', .5), StrokeWidth=2))
    boilSeed('cope14')
    paint(rectPts(-200, 222, W + 600, 40), wash='#4C4278', ink=INK, sw=.9)
    # wall lamps: one lights per beat, a warm pool spreads down the wall
    for i, (lx, kk) in enumerate(((420, 52), (1000, 53), (1580, 54))):
        on = clamp((t - B[kk] + .04) / .08)
        if on > 0:
            sh = skia.GradientShader.MakeRadial(skia.Point(lx, 360), 420, [skcol('#FFE3A0', .42 * on), skcol('#FFE3A0', 0)])
            G.c.drawRect(skia.Rect.MakeXYWH(lx - 460, 300, 920, 580), skia.Paint(AntiAlias=True, Shader=sh))
        boilSeed(f'sc14{i}')
        paint(rectPts(lx - 8, 300, 16, 40), wash='#3A3550', ink=INK, sw=.6)
        paint(rrPts(lx - 30, 320, 60, 74, 14), wash=mixCol('#77738A', '#FFE7A0', on), ink=INK, sw=.8)
        if on > 0:
            glow(lx, 356, 160 * on, '#FFD27A', on)
    G.c.restore()
    # pavement
    flatRect(-200, 880, W + 400, 400, '#46486E')
    inkLine([[-200, 880], [W + 200, 880]], 1.0, INK, 'ink', 0)
    for q in range(-2, 14):
        xx = q * 200 - pan * 1.3 % 200
        G.c.drawLine(xx, 880, xx - 120, H + 20, skia.Paint(AntiAlias=True, Color=skcol('#3A3C60', .8), StrokeWidth=2))
    # walkers (apart) and their shadows on the wall (together)
    u = 30
    sx_, hx = 690, 1230
    wk = lt * 1.7
    reach = ease(seg(t, B[52] - .1, B[55] - .02))
    ko = [[0, 'hopeful'], [B[55] - .06, 'shy']]
    o = em(t, ko)
    o.update(view='q', walk=wk, aL=-.9, aR=-.9)
    if after(t, 55, .06):
        o.update(lookX=-.6, lookY=-.7)
    m = feel('happy', t, dict(view='q', walk=wk + .5, aL=-.9, aR=-.9))
    sc = 1.65
    shS, shH = 625, 1295
    SY = 812
    so = fo(o, aR=lerp(-1.0, .05, reach), aL=-.4, walk=None)
    smo = fo(m, aL=lerp(-1.0, .05, reach), aR=-.4, walk=None)
    wallShadow(her, shS, SY, u, so, sc, a=.62)
    wallShadow(him, shH, SY, u, smo, sc, a=.62)
    if after(t, 55, .04):
        a = t - B[55]
        hxs, hys = handXY(0, 0, u, so, 'R')
        px_, py_ = shS + hxs * sc, SY + hys * sc
        heart(px_ + 10, py_ - 90 - 30 * clamp(a / .4), 60 * backOut(clamp((a + .04) / .16)), HOT, key='h14', sw=.9)
        stamp('牵到了', px_ + 10, py_ - 210, 60, '#FFE36E', a, rot=-.06)
        sparkles(t, 14, 6, px_ - 120, py_ - 160, px_ + 120, py_ + 20, 14, '#FFF3C8')
    her(sx_, 900, u, o)
    him(hx, 900, u, m)
    camEnd()


# =====================================================================================
# S15 23.74–25.43 示例歌词占位文字示 · night bench, she plucks a daisy: 喜欢 / 不喜欢 per beat
def s15(t, lt, dur):
    from sets_huibuhui import daisyHead, daisyStem, pluck
    cam(t, PARK['benchX'] - 20, 600, 1.45)
    st = parkScene(t, 'night', key='p15')
    u = 30
    x = PARK['benchX'] - 80
    keys = [[0, 'hopeful'], [B[57] - .06, 'sad'], [B[58] - .06, 'hopeful'], [B[59] - .06, 'sad']]
    o = em(t, keys)
    o.update(view='q', aR=.95, aL=.3)
    seat(her, x, st, u, o)
    hx, hy = handXY(x, st + 2 * u, u, o, 'R')
    fx, fy = hx + 6, hy - 118
    daisyStem(fx, fy, 118, bend=.03, w=3, key='ds15')
    gone = 4 + max(0, lastBeat(t, [56, 57, 58, 59]) + 1)
    daisyHead(fx, fy, 50, gone=gone, key='dh15')
    labs = ['喜欢', '不喜欢', '喜欢', '不喜欢']
    for i, kk in enumerate((56, 57, 58, 59)):
        pluck(t, B[kk] - .02, fx, fy, 50, 4 + i, dirx=1 if i % 2 == 0 else -1, key=f'pk15{i}', dist=260, life=.8)
    i = lastBeat(t, [56, 57, 58, 59])
    if i >= 0:
        lx, ly = (fx + 170, fy - 70) if i % 2 == 0 else (fx - 330, fy - 90)
        stamp(labs[i], lx, ly, 64, '#F5C04A' if i % 2 == 0 else '#9DB2D6', t - B[56 + i], rot=-.1 if i % 2 == 0 else .1, life=.42)
    camEnd()


# =====================================================================================
# S16 25.43–27.11 示例歌词占位文字示 · mood roller coaster: peak on k60/k62 (开心), trough on k61/k63 (失落)
TRK_L = 560.0
TRK_X0 = 1000.0


def trackY(X):
    return 600 - 230 * math.cos(math.pi * (X - TRK_X0) / TRK_L)


def s16(t, lt, dur):
    bp = bpOf(t) - 60
    X = TRK_X0 + TRK_L * bp
    Y = trackY(X)
    ang = math.atan2(trackY(X + 5) - trackY(X - 5), 10)
    z = lerp(.92, 1.8, easeIn(seg(t, B[61] + .08, B[62])))
    cam(t, X + lerp(120, 0, seg(t, B[61], B[62])), lerp(560, Y - 120, easeIn(seg(t, B[61] + .08, B[62]))), z)
    gradRect(X - 1600, -400, 3400, 1800, ['#FFB88C', '#F7A8C0', '#B89AE0'])
    from props_zuitian import ferrisWheel
    ferrisWheel(X + 700 - 0.4 * TRK_L * bp, 640, 260, t, key='fw16')
    puff(X - 500 - .2 * TRK_L * bp, 160, 30, col='#FFE8EE', key='c16a')
    puff(X + 500 - .3 * TRK_L * bp, 230, 24, col='#FFE8EE', key='c16b')
    # track
    pts = [[xx, trackY(xx)] for xx in range(int(X - 1400), int(X + 1500), 20)]
    for i, (xx, yy) in enumerate(pts[::7]):
        inkLine([[xx, yy + 20], [xx, 1400]], 1.6, '#8A6A8E', 'ink', 0)
    inkLine(pts, 3.6, '#C8324A', 'ink', 0)
    inkLine([[p[0], p[1] + 16] for p in pts], 2.0, '#8E1E35', 'ink', 0)
    for xx, yy in pts[::3]:
        G.c.drawLine(xx, yy, xx, yy + 16, skia.Paint(AntiAlias=True, Color=skcol(INK, .7), StrokeWidth=3))
    # cart with her
    keys = [[0, 'excited'], [B[61] - .1, 'scared']]
    o = em(t, keys)
    push()
    translate(X, Y)
    rotate(ang)
    her(-10, 26, 26, fo(o, view='q', noLegs=True, noShadow=True, aL=1.4, aR=1.4, dx=0, dy=0, rot=0, sq=0))
    boilSeed('cart16')
    paint(rrPts(-170, -90, 340, 96, 26), wash='#E8476E', fill='#B8324F', fillOp=50, ink=INK, sw=1.1)
    paint(heartPts(0, -44, 26, 18), wash='#FFFFFF', ink=INK, sw=.6)
    for wx in (-110, 110):
        paint(ellPts(wx, 10, 20, 20, 14), wash='#3A3550', ink=INK, sw=.8)
    pop()
    for j in range(5):
        sx = X - 260 - j * 70
        inkLine([[sx, Y - 100 + j * 30], [sx - 120, Y - 100 + j * 30 - 30 * math.sin(ang)]], 1.4, '#FFFFFF', 'dry', 0)
    camEnd()
    # mood label in screen space: one per beat
    i = lastBeat(t, [60, 61])
    if i >= 0:
        top = i % 2 == 0
        stamp('开心！' if top else '失落…', 330, 170, 100, '#FFE36E' if top else '#9DB2D6', t - B[60 + i], rot=-.08 if top else .08, life=.42)


# =====================================================================================
# S17 27.11–28.80 示例歌词占位 · HIS phone camera (orange case) frames HER on the bench; pull back: he is behind the bush
def herBenchScene(t, z, cx, cy, key='p17'):
    cam(t, cx, cy, z)
    st = parkScene(t, 'night', key=key)
    u = 30
    x = PARK['benchX'] - 80
    o = feel('sad', t, dict(view='q', aR=.8, aL=.2, gloom=.15))
    seat(her, x, st, u, o)
    hx, hy = handXY(x, st + 2 * u, u, o, 'R')
    from sets_huibuhui import daisyStem, daisyHead
    daisyStem(hx + 6, hy - 118, 118, bend=.03, w=3, key='ds15')
    daisyHead(hx + 6, hy - 118, 50, gone=8, key='dh15')
    fx, fy = toScreen(x, st - 2.5 * u)
    parkFront(t, 'night', key=key)
    camEnd()
    return fx, fy


HIS_SHOTS = (63,)


def titleBanner(k, a_credit=1.0):
    if k <= .01:
        return
    push()
    translate(960, 160 - 40 * (1 - k))
    scale(k)
    banner(0, 0, 1120, 156, key="ban18")
    text('偷偷拍下你的样子', 0, -4, 92, '#FFFFFF', stroke=INK, strokeW=12)
    pop()
    text('外卖梁 / 白允y', 1380, 312, 44, '#FFF3E2', stroke=INK, strokeW=7, shadow=False, a=a_credit)


def titleTag(k):
    """small rounded title tag in the viewfinder's empty top-left sky (hard rule 8, row 3: the first frame IS the camera
    UI, so no full-width banner over it). Stays clear of the top bar (y < 120), the 1x/2x zoom pill, the focus box,
    his face at 1x/2x, the mode bar and shutter on the right, and the album bottom-right: x 62–408, y 168–332."""
    if k <= .01:
        return
    push()
    translate(235, 250 - 30 * (1 - k))
    scale(k)
    rotate(-.05)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-173 + 9, -82 + 12, 346, 164), 30, 30, skia.Paint(AntiAlias=True, Color=skcol(INK, .25)))
    boilSeed('tptag')
    paint(rrPts(-173, -82, 346, 164, 30), wash='#E8476E', fill='#B8324F', fillOp=40, ink=INK, sw=1.4)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-160, -69, 320, 138), 22, 22,
                      skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skcol('#FFFFFF', .7)))
    text('偷偷拍下', 0, -31, 60, '#FFFFFF', stroke=INK, strokeW=9)
    text('你的样子', 0, 35, 60, '#FFFFFF', stroke=INK, strokeW=9)
    boilSeed('tptagh')
    paint(heartPts(156, -72, 22, 22), wash='#FFD1DF', ink=INK, sw=.8)
    pop()


def openingTitle(k_in, k_out):
    """the title tag over the opening viewfinder + the user's watermark (你的署名) under it + the singers"""
    push()
    G.c.saveLayerAlpha(None, int(255 * clamp(k_out)))
    titleTag(k_in)
    a = clamp(k_in)
    signature(228, 392, 50, a=.95 * a)
    text('外卖梁 / 白允y', 228, 446, 34, '#FFF3E2', stroke=INK, strokeW=6, shadow=False, a=a)
    G.c.restore()
    pop()


def his_viewfinder(t):
    z = steps(t, [63], [1.8, 2.2], d=.12)
    fx, fy = herBenchScene(t, z, PARK['benchX'] - 80, 640)
    shots = [B[k] for k in HIS_SHOTS]
    shutterFlash(t, shots)
    focusBox(fx, fy, 420 * z / 1.8, 380 * z / 1.8, max(.3, pk(t, 62, d=.2)), t, lockAge=t - B[62], col='#FFB15C')
    viewfinderUI(t, 'him', shots, count0=519, zoom='2x' if after(t, 63) else '1x',
                 thumb=lambda cx_, cy_, iw, ih: snap(cx_, cy_, iw, ih, 'her', 'daisy', night=True))


def s17(t, lt, dur):
    """k62 his phone (orange case) locks focus on her; k63 shutter -> album 520, the title drops in"""
    his_viewfinder(t)
    kacha(t, B[63], 1380, 230, 84, '#FFE6C4')


# =====================================================================================
# S18 27.11–27.60 示例歌 词占位文字 示例歌词 占位文字 · both cameras flash at once, both blush; the title stays; fade out
def s18(t, lt, dur):
    cam(t, 690, 630, 1.3)
    st = parkScene(t, 'night', key='p18', bush_=False)
    u = 28
    sx = PARK['benchX'] - 60
    o = feel('surprised', t, dict(emote=None, blush=1))
    o.update(HERC)
    o.update(view='q', flip=True, aL=1.25, aR=.3)
    seat(her, sx, st, u, o)
    hs = [handXY(sx, st + 2 * u, u, o, sd) for sd in ('L', 'R')]
    hx, hy = min(hs)
    fk = clamp(1 - (t - B[64]) / .3) if t >= B[64] - .01 else 0
    instantCam(hx - 8, hy - 4, 26, face=-1, flashK=fk, key='cam18')
    from sets_huibuhui import daisyStem, daisyHead
    mx, my = 420, 850
    m = feel('surprised', t, dict(emote=None, blush=1))
    m.update(ME)
    m.update(view='q', aR=1.25, aL=.3)
    him(mx, my, 30, m)
    ps = [handXY(mx, my, 30, m, sd) for sd in ('L', 'R')]
    phx, phy = max(ps)
    phoneCam(phx + 10, phy - 4, 30, face=1, flashK=fk, key='ph18')
    for i, (bx, by, s) in enumerate(((330, 905, 74), (560, 915, 62))):
        bush(bx, by, s, key=f'b18{i}', col='#2F4A5A')
    from clawd import emote
    ek = clamp((t - B[64] + .02) / .1)
    emote('!!', sx, st + 2 * u - 10.6 * u, 26, ek, t - B[64])
    emote('!!', mx, my - 10.8 * 30, 26, ek, t - B[64])
    a = t - B[64] - .14
    if a > -.04:
        heart((sx + mx) / 2, 560 - 40 * clamp(a / .4), 50 * backOut(clamp((a + .04) / .16)), HOT, key='h18', sw=.8)
    camEnd()
    a = t - B[64]
    if 0 <= a < .1:
        flash(.32 * (1 - a / .1))
    kacha(t, B[64], 960, 300, 110, '#FFFFFF', rot=-.06, life=.26)
