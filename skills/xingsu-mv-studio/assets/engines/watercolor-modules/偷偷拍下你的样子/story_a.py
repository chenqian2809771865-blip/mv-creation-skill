# story_a.py: 《偷偷拍下你的样子》 shots S01–S09 (one per bar; every beat carries a visible event). Data: storyboard.py.
import math
from eng import *
import eng
from clawd import *
from props import puff, sparkle, sparkles, floatHearts, bubble, stamp, sunburst, stripes, bush, lamp, umbrellaAt
from common import *
from ch import rr, heart, bobaCup, WENKAI, HOT, PINK, PINKDK, CREAM, fo
from tp import *
import tp
from sets2 import seat, parkBench, fairyLights, bookshelf, wallCalendar, coffeeRing, washi, pencil
from hl import inkWrite, deskLamp


def openBook(bx, by, u, key='book', flip=None):
    """open book on a seated Clawd's lap; (bx, by) = spine bottom"""
    boilSeed(key)
    w, h = 2.7 * u, 1.5 * u
    paint([[bx - w - .2 * u, by - .1 * u], [bx, by + .35 * u], [bx + w + .2 * u, by - .1 * u], [bx + w + .2 * u, by + .25 * u], [bx, by + .6 * u],
           [bx - w - .2 * u, by + .25 * u]], wash='#5B7FC4', ink=INK, sw=.8)
    paint([[bx - w, by - h], [bx, by - h + .35 * u], [bx, by + .3 * u], [bx - w, by - .1 * u]], wash='#FFFDF6', ink=INK, sw=.7)
    paint([[bx + w, by - h], [bx, by - h + .35 * u], [bx, by + .3 * u], [bx + w, by - .1 * u]], wash='#FFFDF6', ink=INK, sw=.7)
    for i in range(3):
        inkLine([[bx - w * .8, by - h * .7 + i * .35 * u], [bx - w * .2, by - h * .55 + i * .35 * u]], .3, '#9A90A0', 'inkfine', 0)
        inkLine([[bx + w * .2, by - h * .55 + i * .35 * u], [bx + w * .8, by - h * .7 + i * .35 * u]], .3, '#9A90A0', 'inkfine', 0)
    if flip is not None and 0 <= flip < 1:
        c = math.cos(flip * math.pi)
        paint([[bx, by - h + .35 * u], [bx + w * c, by - h - .6 * u * math.sin(flip * math.pi)], [bx + w * c, by - .1 * u - .6 * u * math.sin(flip * math.pi)],
               [bx, by + .3 * u]], wash='#FFFDF6', ink=INK, sw=.7)


def hop(t, k, d=.22, h=1.0):
    """a little hop that lands on beat k (rises from k - d); returns dy in u"""
    a = t - (B[k] - d)
    if a < 0 or a > d:
        return 0.0
    return -h * math.sin(a / d * math.pi)


def herCam(x, y, u, o, camS=None, face=1, flashTb=None, t=0.0, camRot=0.0, side='R', off=(0, 0)):
    """her with the pink instant camera at her hand (world coordinates, lens toward `face`)"""
    her(x, y, u, o)
    hx, hy = handXY(x, y, u, o, side)
    fk = 0.0
    if flashTb is not None:
        a = t - flashTb
        fk = clamp(1 - a / .22) if a >= -.01 else 0.0
    instantCam(hx + off[0] * u, hy + off[1] * u, camS or u * .9, face=face, rot=camRot, flashK=fk, key=f'cam{x:.0f}')
    return hx, hy


# =====================================================================================
# S01 0–1.82 示例歌词占位文字 · her phone camera: focus locks on him, two shots, he looks up, the frame whips away
def s01Scene(t, cx, cy, z):
    cam(t, cx, cy, z)
    st = parkScene(t, 'day', key='p1')
    u = 30
    look = after(t, 3, .06)
    o = feel('happy', t, dict(eyes='look', lookY=.85, mouth='smile', aL=.75, aR=.75, blush=.2))
    if look:
        o = feel('surprised', t, dict(lookY=-.2, aL=.75, aR=.75, emote='?', emoteK=clamp((t - B[3] + .06) / .12), emoteAge=t - B[3]))
    seat(him, PARK['benchX'] - 20, st, u, o)
    # open book on his lap (below the face: Clawd's face is on the body)
    bx, by = PARK['benchX'] - 20, st - .2 * u
    openBook(bx, by, u, key='book1')
    bobaCup(PARK['benchX'] + 175, st, 34, key='boba1')
    parkFront(t, 'day', key='p1')
    fx, fy = toScreen(PARK['benchX'] - 20, st - 4.6 * u)
    camEnd()
    return fx, fy


def s01(t, lt, dur):
    z = steps(t, [2], [1.62, 2.05], d=.12)
    whip = easeIn(seg(t, B[3] + .1, B[3] + .26))
    cx = PARK['benchX'] - 20 + whip * 900
    cy = 640 - whip * 60
    fx, fy = s01Scene(t, cx, cy, z)
    if whip > 0:
        for i in range(9):      # whip streaks
            y = 140 + i * 95
            inkLine([[-50, y], [W + 50, y + 10]], 2.5 * whip, '#FFFFFF', 'dry', 0)
    shots = [B[1], B[2]]
    shutterFlash(t, shots)
    lk = max(.3, pk(t, 0, d=.22))
    focusBox(fx, fy, 380 * z / 1.62, 330 * z / 1.62, lk * (1 - whip), t, lockAge=t - B[0])
    for tb in shots:
        kacha(t, tb, 1400, 420, 84, life=.34)
    viewfinderUI(t, 'her', shots, count0=97, zoom='2x' if after(t, 2) else '1x',
                 thumb=lambda cx_, cy_, iw, ih: snap(cx_, cy_, iw, ih, 'him', 'read'))


# =====================================================================================
# S02 1.82–3.51 示例歌词占位文字 · wide park; she pops up somewhere new on every beat
def s02(t, lt, dur):
    cam(t, 990, 650, 1.3)
    k = lastBeat(t, [4, 5, 6, 7])
    st = parkScene(t, 'day', bin_=False, key='p1')
    u = 24
    seat(him, PARK['benchX'] - 20, st, u, feel('happy', t, dict(eyes='look', lookY=.85, mouth='smile', aL=.75, aR=.75)))
    openBook(PARK['benchX'] - 20, st - .2 * u, u, key='book1', flip=(t - B[7]) / .3 if after(t, 7) else None)
    bobaCup(PARK['benchX'] + 175, st, 28, key='boba1')
    if k == 0:      # behind the bush, left: only her top (eyes, flower) shows over the leaves
        x, y = PARK['bushX'] + 40, 830
        o = feel('happy', t, dict(eyes='narrow', mouth='smirk', dy=0, sq=0))
        o.update(aR=1.0, view='q')
        herCam(x, y, 26, o, face=1, flashTb=B[4], t=t)
    parkFront(t, 'day', key='p1')
    if k == 1:      # hanging upside down by her legs from a branch under the crown, camera flashing down at him
        x, y = 1460, 548
        sway = .05 * math.sin((t - B[5]) * 7)
        o = feel('playful', t, dict(dy=0, sq=0))
        o.update(rot=math.pi + sway, aL=.2, aR=.2, view='front')
        her(x, y, 24, o)
        boilSeed('hangbr')
        paint(ribbon([[1510, 520], [1460, 540], [1390, 550]], 26, 14), wash='#9B6B45', ink=INK, sw=1)
        # hand (upside down): rotate the unrotated hand position by pi around the feet
        ax, ay = handXY(x, y, 24, fo(o, rot=0), 'R')
        hx, hy = 2 * x - ax, 2 * y - ay
        instantCam(x - 70, y + 8.9 * 24, 26, face=-1, rot=-.45, flashK=clamp(1 - (t - B[5]) / .25), key='camb')
    bx, by, bs = PARK['binX'] - 20, 800, 54
    rim = by - 2.6 * bs
    if k == 3:      # popped out of the bin, the lid on her head
        trashcanOpen(bx, by, bs, key='p1bin')
        rise = backOut(clamp((t - B[7] + .05) / .16))
        uu = 18
        yy = rim + 1.2 * uu + (1 - rise) * 170
        o = feel('happy', t, dict(eyes='wide', mouth='open', dy=0, sq=0))
        o.update(aL=1.35, aR=.5, view='q', flip=True, noShadow=True)
        G.c.save()
        G.c.clipRect(skia.Rect.MakeXYWH(bx - 300, -400, 600, rim + 400 + 4), skia.ClipOp.kIntersect, True)
        her(bx, yy, uu, o)
        G.c.restore()
        push()
        translate(bx - 6, yy - 8.3 * uu)
        rotate(-.2)
        boilSeed('lidhead')
        paint(rrPts(-1.25 * bs, -.22 * bs, 2.5 * bs, .44 * bs, .15 * bs), wash='#6E95B8', ink=INK, sw=1)
        paint(rrPts(-.3 * bs, -.5 * bs, .6 * bs, .3 * bs, .1 * bs), wash='#6E95B8', ink=INK, sw=.8)
        pop()
        hs = [handXY(bx, yy, uu, o, sd) for sd in ('L', 'R')]
        hx, hy = min(hs)
        instantCam(hx - 8, hy - 4, 20, face=-1, rot=-.15, flashK=clamp(1 - (t - B[7]) / .22), key='camd')
    else:
        trashcanLid(bx, by, bs, 0.0, key='p1bin')
    labels = {0: ('侧拍！', PARK['bushX'] + 60, 520), 1: ('俯拍！', PARK['treeX'] - 120, 420), 3: ('抓拍！', PARK['binX'] + 150, 560)}
    lab = None
    if k in labels:
        lab = labels[k][0], toScreen(labels[k][1], labels[k][2])
    camEnd()
    if k == 2:      # flat in the grass, big in the foreground (bottom right), shooting up at him
        x, y = 1720, 1250
        o = feel('determined', t, dict(dy=0))
        o.update(view='q', flip=True, aL=1.3, aR=.4, lookY=-.6)
        her(x, y, 56, o)
        hs = [handXY(x, y, 56, o, sd) for sd in ('L', 'R')]
        hx, hy = min(hs)
        instantCam(hx - 20, hy - 10, 50, face=-1, rot=-.45, flashK=clamp(1 - (t - B[6]) / .22), key='camc')
        lab = '仰拍！', (1440, 560)
    if lab:
        txt, (lx, ly) = lab
        stamp(txt, lx, ly, 70, HOT, t - B[4 + k], rot=-.12 if k % 2 else .1)
        kacha(t, B[4 + k], lx + 40, ly + 86, 46, '#FFFFFF', life=.34)


# =====================================================================================
# S03 3.51–5.20 示例歌词占位文字示 · desk at night, a crumpled page lands in the bin on every beat
BIN = (1400, 760, 210, 230)


def s03(t, lt, dur):
    cam(t, 960, 540, lerp(1.0, 1.04, lt / dur))
    roomWallNight()
    fairyLights(t, 120, 1800, 60, sag=46, n=18, key='fl3')
    stringPhotos(t, 330, 1260, 150, n=5, key='sp3')
    wallCalendar(110, 300, key='cal3')
    bookshelf(1420, 250, 380, 330, key='bs3', who='her')
    u = 40
    x, y = 860, 820
    ths = [8, 9, 10]
    # arms: crumple (both up) just before each throw, throw arm out right
    th = lastBeat(t, ths, lead=.36)
    aL = .4 + .5 * math.sin(t * 9) * (1 - clamp(lt / .2))
    aR = .3
    if th >= 0:
        a = t - (B[ths[th]] - .36)
        aR = lerp(1.2, .1, clamp(a / .2)) if a < .36 else .3
    keys = [[0, 'determined'], [B[9] - .06, 'nervous'], [B[11] - .06, 'scared']]
    o = em(t, keys)
    o.update(aL=aL, aR=aR)
    her(x, y, u, o)
    # desk
    deskFront(760, key='dk3')
    deskLamp(330, 760, 1.3, on=1.0, key='dl3')
    glow(420, 600, 380, '#FFC766', .45)
    pencilCup(560, 760, 52, key='pc3')
    boilSeed('nb3')
    paint([[700, 760], [1060, 760], [1080, 740], [720, 738]], wash='#FFFDF6', ink=INK, sw=.8)
    mug_x = 1180
    boilSeed('mug3')
    paint(rrPts(mug_x - 40, 680, 80, 80, 14), wash='#E8E1D2', ink=INK, sw=.8)
    heart(mug_x, 722, 16, HOT, key='mh3', sw=.4, shine=False)
    # bin on the desk corner: back rim, pile, front
    bx, by, bw, bh = BIN
    wastebasket(bx, by, bw, bh, key='wb3', back=True)
    n = sum(1 for kk in ths if t >= B[kk])
    over = t >= B[11] - .12
    pile = [(-40, -bh - 6, 36), (36, -bh - 12, 34), (0, -bh - 40, 36), (-46, -bh - 58, 32), (40, -bh - 62, 33), (0, -bh - 96, 34)]
    show = min(len(pile), n * 2)
    for i in range(show):
        px, py, r = pile[i]
        paperBall(bx + px, by + py + 20, r, rot=i * 1.3, key=f'pile{i}')
    wastebasket(bx, by, bw, bh, key='wb3', back=False)
    if over:   # avalanche: the pile tumbles onto the desk
        a = t - (B[11] - .12)
        for i in range(8):
            ang = -math.pi / 2 + (hash1(i * 3.7) - .5) * 2.4
            sp = 420 + 300 * hash1(i * 1.9)
            px = bx + math.cos(ang) * sp * a * 1.2
            py = by - bh - 30 + math.sin(ang) * sp * a + 1300 * a * a
            py = min(py, 745 - 26)
            paperBall(px, py, 28, rot=i + a * 9, key=f'av{i}')
    # balls in flight (released .36 s before each beat, land on it)
    hx, hy = handXY(x, y, u, o, 'R')
    for i, kk in enumerate(ths):
        a = t - (B[kk] - .36)
        if 0 <= a < .36:
            p = arcPt([hx + 20, hy - 10], [bx, by - bh - 10], 180, a / .36)
            paperBall(p[0], p[1], 38, rot=a * 12, key=f'fly{i}')
        if 0 <= t - B[kk] < .18:
            boilSeed(f'plop{i}')
            for j in range(5):
                aa = -math.pi / 2 + (j - 2) * .45
                L = 30 + 40 * (t - B[kk]) / .18
                inkLine([[bx + math.cos(aa) * 40, by - bh - 30 + math.sin(aa) * 40], [bx + math.cos(aa) * (40 + L), by - bh - 30 + math.sin(aa) * (40 + L)]],
                        1.0, INK, 'ink', 0)
    for i, kk in enumerate(ths):
        stamp('+1', bx + 150, by - bh - 60 - i * 50, 56, HOT, t - B[kk], rot=.1, life=.4)
    stamp('第99版', bx - 120, 420, 74, HOT, t - B[11], rot=-.12)
    camEnd()


# =====================================================================================
# S04 5.20–6.88 示例歌词占位文字示 · notebook close-up; 喜/欢/你 one per beat, then sucked into the pen nib
def s04(t, lt, dur):
    cam(t, 960, 540, lerp(1.0, 1.08, ease(lt / dur)))
    flatRect(-200, -200, W + 400, H + 400, '#C98B5A')
    for i in range(-2, 12):
        G.c.drawLine(-200, i * 120 + 30, W + 200, i * 120 + 50, skia.Paint(AntiAlias=True, Color=skcol('#9B6B45', .45), StrokeWidth=3))
    coffeeRing(1700, 180, 90)
    washi(150, 120, 220, 50, -.4, '#F7B2C6', key='w4a')
    pencil(1620, 760, -1.1, 320, key='pc4')
    push()
    translate(960, 540)
    rotate(-.025)
    translate(-960, -540)
    px0, py0, pw, ph = 330, 40, 1260, 1000
    gap = notebookPage(px0, py0, pw, ph, key='nb4')
    # crossed-out drafts + doodles
    from sets2 import fakeText
    for i, (yy, w_) in enumerate(((1, 760), (2, 620), (3, 820), (9, 700), (10, 540))):
        fakeText(px0 + 150, py0 + yy * gap - 8, w_, 34, 1, 11 + i, col='#7A6A80', a=.7)
        strike(px0 + 150, px0 + 150 + w_, py0 + yy * gap - 18, key=f'st4{i}')
    noteDoodle(px0 + 1060, py0 + 3 * gap, 34, key='nd1')
    noteDoodle(px0 + 1140, py0 + 2.4 * gap, 26, key='nd2')
    heart(px0 + 1090, py0 + 10 * gap - 10, 20, '#F08A9C', key='dh4', sw=.5, shine=False)
    text('歌词 #99', px0 + 230, py0 + gap * .5, 40, '#C0637B', shadow=False, face=WENKAI)
    pop()
    size = 210
    xs = [560, 840, 1120]
    y0 = 330
    ks = [12, 13, 14]
    suck = easeIn(seg(t, B[15] - .17, B[15] + .02))
    nib = (1310, 600)
    pen_x, pen_y = None, None
    for i, (ch_, kk) in enumerate(zip('喜欢你', ks)):
        p = clamp((t - B[kk] + .24) / .3)
        if p <= 0:
            continue
        cx, cy = xs[i] + size / 2, y0 + size / 2
        if suck > 0:
            G.c.save()
            tx, ty = lerp(cx, nib[0], suck), lerp(cy, nib[1], suck)
            G.c.translate(tx, ty)
            G.c.scale(1 - .95 * suck, 1 - .95 * suck)
            G.c.translate(-cx, -cy)
            inkWrite(ch_, xs[i], y0, size, p, col='#E8476E', a=1 - .3 * suck)
            G.c.restore()
        else:
            inkWrite(ch_, xs[i], y0, size, p, col='#E8476E')
        if 0 < p < 1:
            pen_x = xs[i] + size * (.25 + .5 * p) + 30 * math.sin(t * 40)
            pen_y = y0 + size * (.3 + .45 * ((p * 3.3) % 1)) + 20 * math.cos(t * 33)
    if pen_x is None:
        # resting / gliding between characters
        last = lastBeat(t, ks)
        if last < 0:
            pen_x, pen_y = xs[0] + 40, y0 + 60
        elif t < B[15] - .17:
            pen_x, pen_y = xs[last] + size * .85, y0 + size * .7
        else:
            pen_x, pen_y = nib
        if last >= 0 and last + 1 < 3 and t > B[ks[last]] + .06:
            k_ = ease(seg(t, B[ks[last]] + .06, B[ks[last + 1]] - .24))
            pen_x = lerp(xs[last] + size * .85, xs[last + 1] + size * .25, k_)
            pen_y = lerp(y0 + size * .7, y0 + size * .3, k_) - 40 * math.sin(k_ * math.pi)
        if last == 2 and B[14] + .06 < t < B[15] - .17:
            k_ = ease(seg(t, B[14] + .06, B[15] - .2))
            pen_x, pen_y = lerp(xs[2] + size * .85, nib[0], k_), lerp(y0 + size * .7, nib[1], k_)
    glowK = clamp((t - B[15] + .02) / .1) * (1 + .15 * math.sin(t * 12))
    penProp(pen_x, pen_y, -.75, 1.25, key='pen4', glowK=glowK)
    if t >= B[15] - .04:
        stamp('嘘——', 980, 760, 80, HOT, t - B[15], rot=-.08)
    camEnd()


# =====================================================================================
# S05 6.88–8.57 示例歌词占位文字 · dream frame: he sails in on a paper boat, docks on the 4th beat
def s05(t, lt, dur):
    cam(t, 960, 540, 1.0)
    gradRect(-200, -200, W + 400, 820, ['#F7B7A3', '#F7A8C0', '#E8B8E0'])
    from sets import sunDisc, sea
    sunDisc(820, 560, 120, key='sun5')
    puff(420, 210, 28, col='#FFE8EE', key='c5a')
    puff(1350, 160, 22, col='#FFE8EE', key='c5b')
    sea(600, '#F2A7B8', '#C0637B', t, key='sea5', waveCol='#FFE3EA')
    glow(820, 640, 300, '#FFE3B0', .45)
    beam = .35 * math.sin((t - B[16]) * 4.0) - .1
    lighthouse(1690, 640, 48, beam=beam, key='lh5')
    for kk in (17, 18, 19):
        a = t - B[kk]
        if -.02 <= a < .3:
            glow(1690, 640 - 5.8 * 48, 260 * (1 - a / .3), '#FFF6C8', 1 - a / .3)
    pier(1180, 2100, 700, key='pier5')
    # her at the end of the pier
    u = 30
    keys = [[0, 'hopeful'], [B[18] - .06, 'excited'], [B[19] - .06, 'love']]
    o = em(t, keys)
    wave = .3 + 1.2 * max(0, math.sin((t - B[18]) * 14)) if after(t, 18) and not after(t, 19) else o.get('aR', .4)
    o.update(view='q', flip=True, aR=wave)
    her(1310, 680, u, o)
    # boat: steps toward the pier on each beat, bobbing
    bxs = [-160, 260, 560, 820, 990]
    X = steps(t, [16, 17, 18, 19], bxs, d=.3, lead=.1)
    bob = 10 * math.sin(t * 5)
    for kk in (17, 18):
        a = t - B[kk] + .1
        if 0 <= a < .4:
            bob -= 34 * math.sin(a / .4 * math.pi)
    by = 742 + bob
    bu = 26
    mo = feel('happy', t, dict(eyes='happy', mouth='open' if after(t, 19) else 'smile', blush=.4))
    if after(t, 19):
        mo = feel('love', t)
    bs_ = 58
    him(X, by - 1.1 * bs_ + 3.4 * bu, bu, fo(mo, noLegs=True, noShadow=True, view='q', aL=.6, aR=1.1 if after(t, 19) else .5))
    paperBoat(X, by, bs_, rot=.04 * math.sin(t * 4), key='boat5', sail=False)
    # wake
    inkLine([[X - 140, by + 20], [X - 220, by + 26], [X - 300, by + 20]], 1.0, '#FFE3EA', 'ink', .5)
    if after(t, 19, .04):
        a = t - B[19]
        stamp('咚', 1150, 820, 70, HOT, a, rot=.1, life=.6)
        heart(1150, 420 - 60 * clamp(a / .4), 40 * backOut(clamp((a + .04) / .16)), HOT, key='h5', sw=.8)
    camEnd()
    dreamFrame(pk(t, 16, d=.28), t, key='df5')


# =====================================================================================
# S06 8.57–10.25 示例歌词占位文字 · tear-off calendar, one small happiness per beat
PAGES = [('周一', '示例歌词占', lambda x, y: bobaCup(x, y + 110, 70, key='cb6')),
         ('周二', '示例歌词占', lambda x, y: catFace(x, y, 95, key='cat6')),
         ('周三', '示例歌词占', lambda x, y: umbrellaAt(x, y + 10, 150, col='#F7A8C0', key='umb6')),
         ('周四', '示例歌词占位', lambda x, y: iceCream(x, y + 140, 80, key='ice6'))]


def s06(t, lt, dur):
    cam(t, 960, 540, 1.0)
    stripes('#CFEFE0', '#E2F7EC', 80)
    floatHearts(t, 6, 10, 80, 120, 1840, 900, 16)
    tk = [21, 22, 23]
    i = sum(1 for kk in tk if t >= B[kk] - .3)
    tear = None
    if i >= 1:
        k = clamp((t - (B[tk[i - 1]] - .3)) / .28)
        tear = (PAGES[i - 1], k)
    pg = 1.0
    if i >= 1:
        a = t - B[tk[i - 1]]
        pg = 1 + .06 * math.exp(-max(0, a) * 12) if a > -.02 else 1
    push()
    translate(960, 470)
    scale(pg)
    translate(-960, -470)
    calendarPad(960, 140, 560, 660, PAGES[i], t, key='cal6', tear=tear)
    pop()
    u = 36
    for who, x in (('her', 420), ('him', 1500)):
        dy = sum(hop(t, kk, .24, 1.4) for kk in (20, 21, 22, 23))
        if after(t, 23, .06):
            o = feel('love', t, dict(aL=1.5, aR=1.5))
        else:
            o = feel('happy', t, dict(aL=.9, aR=.9))
        o.update(dy=o.get('dy', 0) + dy, view='q', flip=(who == 'him'))
        (her if who == 'her' else him)(x, 900, u, o)
    if after(t, 23, .04):
        a = t - B[23]
        heart(960, 880 - 30 * math.sin(clamp(a / .3) * math.pi), 80 * backOut(clamp((a + .04) / .18)), HOT, key='bh6', sw=1.1)
    for j, kk in enumerate((21, 22, 23)):
        stamp('撕！', 1340, 300 + j * 40, 64, HOT, t - B[kk] + .26, rot=.15, life=.42)
    camEnd()


# =====================================================================================
# S07 10.25–11.94 示例歌词占位文字示例 · sofa at night, the clock jumps an hour per beat
def s07(t, lt, dur):
    cam(t, 960, 600, 1.22)
    gradRect(-200, -200, W + 400, H + 400, ['#252250', '#3B3270'])
    for i in range(-2, 22):
        flatRect(i * 110, -100, 3, H + 200, '#FFFFFF', .03)
    fairyLights(t, 200, 1720, 70, sag=40, n=16, key='fl7')
    # posters
    for px, py, rot, col in ((420, 190, -.05, '#F7A8C0'), (1480, 200, .06, '#9FD4F2')):
        push()
        translate(px, py)
        rotate(rot)
        boilSeed(f'post{px}')
        paint(rectPts(-110, -130, 220, 260), wash=col, ink=INK, sw=.8)
        paint(starPts(0, -20, 60, .45, 5), wash='#FFF3C8', ink=INK, sw=.6)
        text('GAME' if px < 900 else 'MOVIE', 0, 80, 40, '#FFFFFF', stroke=INK, strokeW=5, shadow=False)
        pop()
    from props_bingbian import sofa
    sofa(960, 905, 50, key='sofa7', col='#8FB9A8')
    st = 905 - 4.75 * 50
    u = 30
    hrs = lastBeat(t, [24, 25, 26, 27]) + 0
    tired = after(t, 27, .06)
    win = after(t, 26, .06) and not tired
    for who, x in (('her', 800), ('him', 1120)):
        if tired:
            o = feel('neutral', t, dict(eyes='sleepy', mouth='yawn', aL=.4, aR=.4, gloom=.25))
        elif win:
            o = feel('starstruck', t, dict(aL=1.5, aR=1.5))
        else:
            o = feel('determined', t, dict(aL=.55 + .15 * math.sin(t * 30 + x), aR=.55 + .15 * math.sin(t * 27 + x)))
        o.update(view='front')
        seat(her if who == 'her' else him, x, st, u, o)
        hx, hy = handXY(x, st + 2 * u, u, o, 'R' if who == 'her' else 'L')
        gamepad(hx + (-20 if who == 'her' else 20), hy + 10, 30, rot=.2 * math.sin(t * 20 + x) if not tired else .5, key=f'gp{who}')
        if tired:   # dark circles
            for sx in (-1, 1):
                ex = x + sx * 2.2 * u
                ey = st + 2 * u - 5.35 * u
                paint(ellPts(ex, ey, .9 * u, .32 * u, 12), wash='#5A4A7A', washOp=150, ink=None)
    # side tables: digital clock left, popcorn right
    for tx in (300, 1640):
        boilSeed(f'tbl{tx}')
        paint(rectPts(tx - 110, 760, 220, 26), wash='#9B6B45', ink=INK, sw=.8)
        paint(rectPts(tx - 90, 786, 20, 140), wash='#7A5A48', ink=INK, sw=.6)
        paint(rectPts(tx + 70, 786, 20, 140), wash='#7A5A48', ink=INK, sw=.6)
    from sm import alarmClock
    clk = ['00:00', '01:00', '02:00', '03:00'][max(0, hrs)]
    shk = 0.0
    for kk in (25, 26, 27):
        a = t - B[kk]
        if 0 <= a < .25:
            shk = 1 - a / .25
    alarmClock(300, 760, .9, txt=clk, key='ac7', shake=.12 * shk * math.sin((t) * 60))
    popcorn(1640, 760, 46, t, jumpTb=B[25] - .1, key='pop7')
    tvGlow(1.0, t)
    stamp('START', 960, 300, 80, '#9FE8FF', t - B[24], rot=-.06, life=.45)
    stamp('WIN!', 960, 300, 110, '#FFE36E', t - B[26], rot=.08, life=.42)
    stamp('熬夜冠军', 960, 300, 86, HOT, t - B[27], rot=-.08)
    camEnd()


# =====================================================================================
# S08 11.94–13.63 示例歌词占位文字 · candles light one per beat, then the cloche lifts: a heart-shaped egg
def s08(t, lt, dur):
    lit = [clamp((t - B[kk] + .05) / .12) for kk in (28, 29, 30)]
    warm = sum(lit) / 3
    cam(t, 1000, 560, lerp(1.22, 1.28, ease(lt / dur)))
    gradRect(-200, -200, W + 400, H + 400, [mixCol('#2E2240', '#5A3048', warm), mixCol('#3A2A50', '#7A4250', warm)])
    for i in range(-2, 22):
        flatRect(i * 110, -100, 3, H + 200, '#FFFFFF', .03)
    # wall frame + a little vase
    push()
    translate(1520, 230)
    boilSeed('frame8')
    paint(rectPts(-120, -90, 240, 180), wash='#D9B45A', ink=INK, sw=.9)
    paint(rectPts(-100, -70, 200, 140), wash='#F7D9C0', ink=None)
    heart(0, 0, 40, HOT, key='fh8', sw=.6)
    pop()
    u = 36
    lift = ease(seg(t, B[31] - .14, B[31] + .02))
    ko = [[0, 'proud'], [B[31] - .06, 'happy']]
    o = em(t, ko)
    o.update(hat=['chef', 'flower'], view='q', aR=lerp(.3, 1.7, lift), aL=.3)
    her(700, 760, u, o)
    mo = [[0, 'hopeful'], [B[31] - .06, 'starstruck']]
    m = emotions(t, mo, ME)
    m.update(view='q', flip=True, aL=.6, aR=.6)

    def bib(u_, sw):
        paint([[-2.2 * u_, -3.6 * u_], [2.2 * u_, -3.6 * u_], [0, -1.2 * u_]], wash='#FFFFFF', ink=INK, sw=sw * .6)
        paint(ellPts(0, -3.6 * u_, .5 * u_, .35 * u_, 10), wash=HOT, ink=None)
    m['draw'] = bib
    him(1350, 760, u, m)
    from props_zuitian import tableCloth, cloche
    tableCloth(260, 1660, 700, drop=420, key='tc8')
    plate(930, 728, 40, key='pl8')
    plate(1240, 728, 36, key='pl8b')
    boilSeed('fork8')
    inkLine([[1360, 700], [1380, 760]], 1.6, '#B8C0D0', 'ink', 0)
    for i, (cx, kk) in enumerate(zip((1040, 1100, 1160), (28, 29, 30))):
        candle(cx, 716, 30 + 6 * (i == 1), lit[i], t, key=f'cd8{i}')
    if lift > 0:
        heartEgg(930, 712, 46, key='egg8')
    hs = [handXY(700, 760, u, o, sd) for sd in ('L', 'R')]
    hx, hy = max(hs)
    cx, cy = lerp(930, hx + 60, lift), lerp(724, hy + 80, lift)
    cloche(cx, cy, 40, key='clo8', tilt=lerp(0, .5, lift))
    if after(t, 31, .02):
        sparkles(t, 8, 8, 830, 600, 1040, 740, 18, '#FFF3C8')
        stamp('当当！', 1010, 600, 64, '#FFE36E', t - B[31], rot=-.1)
    camEnd()


# =====================================================================================
# S09 13.63–15.31 示例歌词占位文字 · back to reality: rain, he is sad on the bench, she peeks out with an umbrella
def s09(t, lt, dur):
    cam(t, 960, 600, 1.14)
    gradRect(-200, -200, W + 400, 760, ['#4E5A7E', '#7D88A8', '#A3ADC4'])
    skyline(640, '#5D6688', '#FFE3A0', .35, key='sl9')
    flatRect(-200, 640, W + 400, H, '#6F7A96')
    gradRect(-200, 640, W + 400, 120, ['#5A6482', '#6F7A96'])
    for i in range(7):
        boilSeed(f'pud{i}')
        paint(ellPts(200 + i * 260 + 60 * hash1(i), 880 + 60 * hash1(i * 2), 90 + 30 * hash1(i), 14, 16), wash='#8A97B8', ink=None)
    # bus stop sign
    boilSeed('stop9')
    paint(rectPts(1640, 330, 18, 520), wash='#3A4278', ink=INK, sw=.8)
    paint(ellPts(1649, 320, 70, 70, 24), wash='#3A9C98', ink=INK, sw=1)
    text('站', 1649, 320, 70, '#FFFFFF', shadow=False)
    st = parkBench(1180, 860, 400, 74, 108, key='b9', night=.6)
    u = 28
    mo = feel('sad', t, dict(aL=-.6, aR=-.6))
    seat(him, 1180, st, u, mo)
    from sm import rainCloud
    rainCloud(1180, st - 9.6 * u - 70, 64, t, key='rc9', zap=clamp(1 - (t - B[32]) / .25) if t >= B[32] - .02 else 0, rainA=.85)
    # her: hidden behind the advertising column, peeks (k33), steps out with the umbrella (k34), freezes (k35)
    xs = [440, 560, 700, 700]
    X = steps(t, [33, 34], [440, 560, 700], d=.14)
    keys = [[0, 'nervous'], [B[33] - .06, 'surprised'], [B[34] - .06, 'determined'], [B[35] - .06, 'scared']]
    o = em(t, keys)
    trem = 6 * math.sin(t * 60) if after(t, 35) else 0
    o.update(view='q', aR=1.2 if after(t, 34) else .4, dx=trem / 26)
    her(X, 850, 26, o)
    if after(t, 34, .06):
        hs = [handXY(X, 850, 26, o, sd) for sd in ('L', 'R')]
        hx, hy = max(hs)
        uk = backOut(clamp((t - B[34] + .06) / .16))
        umbrellaAt(hx + trem, hy + 6, 110, col='#F7A8C0', k=clamp(uk), key='umb9', tilt=.28, handle=True)
    # advertising column (drawn after her so she hides behind it)
    boilSeed('col9')
    paint(rectPts(300, 260, 220, 620), wash='#C9C1D6', fill='#9A93A8', fillOp=50, ink=INK, sw=1)
    paint(rrPts(285, 230, 250, 40, 14), wash='#5A6482', ink=INK, sw=.9)
    paint(rrPts(285, 870, 250, 30, 10), wash='#5A6482', ink=INK, sw=.9)
    paint(rectPts(325, 330, 170, 230), wash='#F7D36E', ink=INK, sw=.6)
    heart(410, 420, 40, HOT, key='colh', sw=.5)
    text('520', 410, 510, 40, INK, shadow=False)
    paint(rectPts(330, 600, 160, 200), wash='#9FD4F2', ink=INK, sw=.6)
    from props_zuitian import rainLines
    rainLines(t, 9, 120, -60, -60, W + 60, H, col='#DCE6FF', ln=40, sp=1500, ang=.18, sw=.8)
    stamp('!', X + 80, 560, 90, '#FFE36E', t - B[33], life=.5) if not after(t, 34) else None
    if after(t, 35, .04):
        from clawd import emote
        emote('sweat', X + 160, 600, 26, 1, t - B[35])
    camEnd()
