# props2.py: new props for 《最甜情歌》 (phone player, polygraph, cloche, claw machine, evidence board, crystal ball, ...)
import math
from eng import *
import eng
from clawd import *
from props import *


def fo(base, **kw):
    d = dict(base)
    d.update(kw)
    return d


# ---------------------------------------------------------------- S02: the phone on the desk becomes a music player (title device)
def miniFace(x, y, r, col, dk, flower=False, key='mf'):
    """a round avatar with a tiny Clawd face"""
    boilSeed(key)
    paint(ellPts(x, y, r, r, 24), wash=col, fill=dk, fillOp=40, ink=INK, sw=.7)
    for s in (-1, 1):
        paint(rectPts(x + s * r * .32 - r * .08, y - r * .22, r * .16, r * .32), wash=INK, ink=None)
    inkLine([[x - r * .2, y + r * .25], [x, y + r * .38], [x + r * .2, y + r * .25]], .6, INK, 'inkfine', .5)
    if flower:
        flowerAt(x - r * .55, y - r * .7, r * .3, .6, .9)


def albumArt(x, y, s, t, key='alb'):
    """square cover art: pink rays, a heart and the two of them (s = side)"""
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(x, y, s, s))
    flatRect(x, y, s, s, '#F7C6D2')
    p = skia.Path()
    for i in range(14):
        a0 = t * .4 + i * TAU / 14
        p.moveTo(x + s / 2, y + s * .55)
        p.lineTo(x + s / 2 + math.cos(a0) * s, y + s * .55 + math.sin(a0) * s)
        p.lineTo(x + s / 2 + math.cos(a0 + .22) * s, y + s * .55 + math.sin(a0 + .22) * s)
        p.close()
    G.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol('#F3AFC2')))
    boilSeed(key + 'h')
    paint(heartPts(x + s / 2, y + s * .42, s * .26 * (1 + .06 * pulse(t, 7)), 26), wash='#E8476E', fill='#B8324F', fillOp=50, ink=INK, sw=.8)
    clawd(x + s * .3, y + s * .98, s * .045, dict(col='#EE9AAE', dk='#C0637B', lt='#FBD0DA', hat='flower', eyes='happy', mouth='smile', view='q',
                                                  noShadow=True, lite=True, boilKey=key + 'a', aR=.9))
    clawd(x + s * .7, y + s * .98, s * .045, dict(col=PAL['clay'], dk=PAL['clayDk'], lt='#F5B394', eyes='happy', mouth='smile', view='q', flip=True,
                                                  noShadow=True, lite=True, boilKey=key + 'b', aR=.9))
    G.c.restore()
    boilSeed(key + 'f')
    paint(rectPts(x, y, s, s), ink=INK, sw=.9)


def phonePlayer(cx, cy, w, h, t, lit=1.0, notif=0.0, expand=0.0, titleT=None, play=0.0, prog=0.0, eq=0.0, rot=0.0, key='pp'):
    """portrait phone lying on the desk. titleT = list of per-character land times (None = not yet)"""
    push()
    translate(cx, cy)
    rotate(rot)
    boilSeed(key + 'body')
    # shadow under the phone
    paint(rrPts(-w / 2 + 14, -h / 2 + 22, w, h, 60), fill=INK, fillOp=70, bleed=.2, ink=None)
    paint(rrPts(-w / 2, -h / 2, w, h, 58), wash='#2E2A40', fill='#1E1A2C', fillOp=50, ink=INK, sw=1.3)
    sx, sy, sw_, sh = -w / 2 + 22, -h / 2 + 22, w - 44, h - 44
    scr = rrPts(sx, sy, sw_, sh, 42)
    G.c.save()
    G.c.clipPath(eng._path(scr), skia.ClipOp.kIntersect, True)
    gradRect(sx, sy, sw_, sh, [mixCol('#16142A', '#FCE3EC', lit), mixCol('#16142A', '#E6DAF7', lit)])
    if lit > .05:
        glow(0, -h * .1, w * 1.2, '#FFFFFF', .35 * lit)
        # status bar
        text('23:47', sx + 60, sy + 34, 26, mixCol('#16142A', INK, lit), shadow=False, a=lit)
        paint(rrPts(sx + sw_ - 70, sy + 24, 40, 20, 6), ink=INK, sw=.5)
        flatRect(sx + sw_ - 66, sy + 28, 22, 12, '#7BC47F', lit)
    # notification banner -> expands into the player card
    if notif > .01 and expand < .99:
        k = backOut(notif)
        bw, bh = sw_ - 40, 120
        by = sy + 70 - (1 - k) * 160
        G.c.saveLayerAlpha(None, int(255 * (1 - expand)))
        boilSeed(key + 'nt')
        paint(rrPts(-bw / 2, by, bw, bh, 28), wash='#FFFFFF', ink=INK, sw=.8)
        miniFace(-bw / 2 + 62, by + bh / 2, 38, PAL['clay'], PAL['clayDk'], key=key + 'av')
        text('他', -bw / 2 + 120, by + 38, 34, INK, align='left', shadow=False)
        text('分享了一首歌给你', -bw / 2 + 120, by + 84, 28, '#6A5A70', align='left', shadow=False)
        G.c.restore()
    if expand > .01:
        k = easeOut(expand)
        G.c.saveLayerAlpha(None, int(255 * clamp(expand * 1.6)))
        top = lerp(sy + 70, sy + 80, k)
        cw = lerp(sw_ - 40, sw_ - 40, k)
        chh = lerp(120, sh - 110, k)
        boilSeed(key + 'cd')
        paint(rrPts(-cw / 2, top, cw, chh, 30), wash='#FFFDF8', ink=INK, sw=.8)
        if k > .5:
            q = seg(k, .5, 1)
            art = cw - 150
            albumArt(-art / 2, top + 40, art, t, key=key + 'art')
            ty = top + 40 + art + 80
            if titleT:
                chars = '最甜情歌'
                fs = 86
                tw = textW(chars, fs) + 3 * 6
                x = -tw / 2
                for c_, tc in zip(chars, titleT):
                    cwid = textW(c_, fs)
                    if t >= tc:
                        a = t - tc
                        text(c_, x + cwid / 2, ty - 10 * math.exp(-a * 12), fs, '#E8476E', stroke=INK, strokeW=9, shadow=True,
                             sc=1 + .35 * math.exp(-a * 10))
                    x += cwid + 6
            text('红人馆', 0, ty + 66, 30, '#6A5A70', shadow=False, a=q)
            # progress bar
            py = ty + 130
            G.c.drawLine(-cw / 2 + 50, py, cw / 2 - 50, py, skia.Paint(AntiAlias=True, Color=skcol('#D9CFE0', q), StrokeWidth=8, StrokeCap=skia.Paint.kRound_Cap))
            px = lerp(-cw / 2 + 50, cw / 2 - 50, clamp(prog))
            G.c.drawLine(-cw / 2 + 50, py, px, py, skia.Paint(AntiAlias=True, Color=skcol('#E8476E', q), StrokeWidth=8, StrokeCap=skia.Paint.kRound_Cap))
            paint(ellPts(px, py, 13, 13, 12), wash='#E8476E', ink=INK, sw=.6)
            # buttons
            by_ = py + 90
            for s in (-1, 1):
                for j in range(2):
                    xx = s * (120 + j * 28)
                    paint([[xx, by_ - 20], [xx, by_ + 20], [xx + s * 28, by_]], wash=INK, ink=None)
            pb = 1 + .25 * math.exp(-max(0, play - .0) * 0) if False else 1
            r = 58 * (1 + .18 * math.sin(clamp(play) * math.pi))
            paint(ellPts(0, by_, r, r, 28), wash='#E8476E', ink=INK, sw=1)
            if play < .5:
                paint([[-16, by_ - 26], [-16, by_ + 26], [28, by_]], wash='#FFFFFF', ink=None)
            else:
                for s in (-1, 1):
                    paint(rectPts(s * 13 - 8, by_ - 24, 16, 48), wash='#FFFFFF', ink=None)
            # equaliser
            if eq > .01:
                for j in range(9):
                    hh = (14 + 46 * abs(math.sin(t * (7 + j * 1.3) + j))) * eq
                    paint(rrPts(-150 + j * 36 - 10, by_ + 120 - hh, 20, hh, 6), wash=['#F28FB0', '#F7C65C', '#7DD3C8'][j % 3], ink=None)
        G.c.restore()
    G.c.restore()
    boilSeed(key + 'rim')
    paint(rrPts(-w / 2, -h / 2, w, h, 58), ink=INK, sw=1.3)
    paint(rrPts(-46, -h / 2 + 8, 92, 10, 5), wash='#16142A', ink=None)
    pop()


def noteGlyph(x, y, s, col=INK, rot=0.0, key='nt', double=False):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    if double:
        paint(ellPts(-.9 * s, .9 * s, .55 * s, .4 * s, 12, 0, -.3), wash=col, ink=None)
        paint(ellPts(.9 * s, .7 * s, .55 * s, .4 * s, 12, 0, -.3), wash=col, ink=None)
        inkLine([[-.45 * s, .85 * s], [-.45 * s, -1.2 * s]], s / 12, col, 'ink', 0)
        inkLine([[1.35 * s, .65 * s], [1.35 * s, -1.4 * s]], s / 12, col, 'ink', 0)
        paint([[-.45 * s, -1.2 * s], [1.35 * s, -1.4 * s], [1.35 * s, -1.0 * s], [-.45 * s, -.8 * s]], wash=col, ink=None)
    else:
        paint(ellPts(0, .9 * s, .6 * s, .45 * s, 12, 0, -.3), wash=col, ink=None)
        inkLine([[.5 * s, .8 * s], [.5 * s, -1.3 * s], [1.3 * s, -.8 * s]], s / 12, col, 'ink', 0)
    pop()


# ---------------------------------------------------------------- S04: polygraph with a paper strip; each beat the needle draws a heart
def brickWall(c_bg, c_line, key='brk', rows=12, cols=13, y0=-60):
    flatRect(-200, -200, W + 400, H + 400, c_bg)
    for r in range(rows):
        for c_ in range(cols):
            boilSeed(f'{key}{r}{c_}')
            x = c_ * 170 - (85 if r % 2 else 0) - 100
            inkLine([[x, y0 + r * 86], [x + 162, y0 + r * 86]], .5, c_line, 'inkfine', 0)
            inkLine([[x, y0 + r * 86], [x, y0 + r * 86 + 86]], .5, c_line, 'inkfine', 0)


def polygraph(x, y, s, t, beats, v=330.0, key='pg', lit=1.0):
    """machine whose front-bottom centre is (x, y); the paper strip runs out to the left on the table top.
    beats = beat times at which the needle draws a heart loop (0.22 s each)"""
    boilSeed(key)
    # body
    paint(rrPts(x - 2.2 * s, y - 2.6 * s, 4.4 * s, 2.6 * s, .25 * s), wash='#8A93B8', fill='#5E668E', fillOp=60, ink=INK, sw=1.1)
    paint(rrPts(x - 1.9 * s, y - 2.35 * s, 2.0 * s, 1.2 * s, .15 * s), wash='#203238', ink=INK, sw=.8)
    # little screen: a pulse line
    pts = []
    for i in range(24):
        xx = x - 1.85 * s + i * 1.9 * s / 23
        ph = (i / 23 * 3 - t * 2.5) % 1
        pts.append([xx, y - 1.75 * s - (math.sin(ph * TAU) * .2 * s if ph < .5 else 0)])
    inkLine(pts, .8, '#7BE0A0', 'inkfine', 0)
    for i, col in enumerate(['#E8476E', '#F2C53D', '#7BE0A0']):
        paint(ellPts(x + .55 * s + i * .5 * s, y - 2.0 * s, .17 * s, .17 * s, 10), wash=col if (int(t * 4) + i) % 3 else mixCol(col, INK, .5), ink=INK, sw=.5)
    for i in range(2):
        paint(ellPts(x + .8 * s + i * .8 * s, y - 1.1 * s, .3 * s, .3 * s, 14), wash='#EDE6D8', ink=INK, sw=.6)
        inkLine([[x + .8 * s + i * .8 * s, y - 1.1 * s], [x + .8 * s + i * .8 * s + math.cos(t * 3 + i) * .22 * s, y - 1.1 * s - .2 * s]], .6, INK, 'inkfine', 0)
    # paper roll on the left side
    paint(ellPts(x - 2.3 * s, y - .55 * s, .45 * s, .45 * s, 16), wash='#FFFDF6', ink=INK, sw=.8)
    # paper strip lying on the table, scrolling left
    x0 = x - 2.5 * s
    px1 = x0 - 9 * s
    boilSeed(key + 'paper')
    paint([[px1, y + .1 * s], [x0, y + .1 * s], [x0, y - 1.35 * s], [px1, y - 1.35 * s]], wash='#FFFDF6', ink=INK, sw=.7)
    for k in range(7):
        G.c.drawLine(px1, y - .05 * s - k * .19 * s, x0, y - .05 * s - k * .19 * s, skia.Paint(AntiAlias=True, Color=skcol('#F2B8C6', .6), StrokeWidth=1.2))
    base = y - .25 * s
    hs = .52 * s
    H_ = heartPts(0, 0, 1, 40)
    # parametrise the heart from its bottom tip
    tip = max(range(len(H_)), key=lambda i: H_[i][1])
    H_ = H_[tip:] + H_[:tip + 1]
    d = .22
    pts = []
    G.c.save()
    G.c.clipRect(skia.Rect.MakeLTRB(px1, y - 1.4 * s, x0, y + .1 * s))
    tt = t - (x0 - px1) / v
    step = 1 / 120
    segs = []
    cur = []
    while tt <= t:
        dx, dy = 0.0, 0.0
        for tb in beats:
            if tb <= tt < tb + d:
                q = (tt - tb) / d
                f = q * (len(H_) - 1)
                i = int(f)
                j = min(i + 1, len(H_) - 1)
                hx = lerp(H_[i][0], H_[j][0], f - i) - H_[0][0]
                hy = lerp(H_[i][1], H_[j][1], f - i) - H_[0][1]
                dx, dy = hx * hs - v * (tt - tb), hy * hs
        jit_ = math.sin(tt * 53) * .03 * s + math.sin(tt * 31) * .02 * s
        cur.append([x0 - v * (t - tt) + dx, base + dy + jit_])
        tt += step
    if len(cur) > 1:
        inkLine(cur, 1.5, '#C8324A', 'inkfine', 0)
    G.c.restore()
    # the needle arm
    ny = cur[-1][1] if cur else base
    nx = cur[-1][0] if cur else x0
    inkLine([[x - 1.6 * s, y - .9 * s], [nx, ny]], 1.0, INK, 'ink', 0)
    paint(ellPts(nx, ny, .07 * s, .07 * s, 8), wash='#C8324A', ink=None)


def suctionWire(p0, p1, sag=60, col='#4A4E86'):
    mid = [(p0[0] + p1[0]) / 2, min(p0[1], p1[1]) - sag]
    inkLine([p0, mid, p1], 1.2, col, 'ink', .6)
    paint(ellPts(p0[0], p0[1], 14, 9, 12), wash='#E8476E', ink=INK, sw=.6)


# ---------------------------------------------------------------- bouquet, bus stop, big clock
def bouquetHook(k=1.0, key='bq'):
    def h(u, sw):
        boilSeed(key)
        s = u * k
        paint([[0, -.5 * s], [0, .5 * s], [2.6 * s, 1.4 * s], [2.9 * s, -1.4 * s]], wash='#F7E3C8', fill='#E8C9A0', fillOp=60, ink=INK, sw=sw * .6)
        for i, (dx, dy, col) in enumerate([(2.9, -1.0, '#F28FB0'), (3.3, .2, '#FFE36E'), (2.8, 1.1, '#FFFFFF'), (3.7, -.6, '#E8476E'), (3.8, .9, '#F59A6B')]):
            fx, fy = dx * s, dy * s
            for j in range(5):
                a = j / 5 * TAU + i
                paint(ellPts(fx + math.cos(a) * .45 * s, fy + math.sin(a) * .45 * s, .38 * s, .38 * s, 10), wash=col, ink=INK, sw=sw * .35, lite=True)
            paint(ellPts(fx, fy, .28 * s, .28 * s, 8), wash='#E8AA38', ink=None)
        paint([[.6 * s, -.25 * s], [1.0 * s, -.7 * s], [1.3 * s, -.2 * s]], wash='#E8476E', ink=INK, sw=sw * .4)
    return h


def bigClock(x, y, r, t, heart=0.0, key='bclk', spin=1.0):
    boilSeed(key)
    if heart < .5:
        paint(ellPts(x, y, r * 1.1, r * 1.1, 30), wash='#C8564F', ink=INK, sw=1.1)
        paint(ellPts(x, y, r * .92, r * .92, 30), wash='#FFFDF6', ink=INK, sw=.8)
        for i in range(12):
            a = i / 12 * TAU
            inkLine([[x + math.cos(a) * r * .74, y + math.sin(a) * r * .74], [x + math.cos(a) * r * .84, y + math.sin(a) * r * .84]], .8, INK, 'inkfine', 0)
        ma = -math.pi / 2 + t * 9 * spin
        ha = -math.pi / 2 + t * .75 * spin
        inkLine([[x, y], [x + math.cos(ha) * r * .45, y + math.sin(ha) * r * .45]], 1.8, INK, 'ink', 0)
        inkLine([[x, y], [x + math.cos(ma) * r * .7, y + math.sin(ma) * r * .7]], 1.2, INK, 'ink', 0)
        paint(ellPts(x, y, r * .07, r * .07, 8), wash=INK, ink=None)
    else:
        k = backOut(seg(heart, .5, 1))
        paint(heartPts(x, y + r * .1, r * 1.15 * k, 28), wash='#E8476E', fill='#B8324F', fillOp=50, ink=INK, sw=1.1)
        glow(x, y, r * 2.5, '#FFB3C6', .6 * k)


def busStop(x, y, w, h, key='bus'):
    """shelter: (x, y) = ground centre; returns nothing. Draw the bench and the sitter after it."""
    boilSeed(key)
    # back glass panel with a poster
    paint(rectPts(x - w / 2 + 20, y - h + 40, w - 40, h - 80), wash='#BFE3F5', washOp=150, ink=INK, sw=.8, lite=True)
    paint(rectPts(x + w / 2 - 230, y - h + 80, 170, 230), wash='#F7C6D2', ink=INK, sw=.8, lite=True)
    paint(heartPts(x + w / 2 - 145, y - h + 170, 46, 20), wash='#E8476E', ink=INK, sw=.6)
    text('520', x + w / 2 - 145, y - h + 265, 34, INK, shadow=False)
    for px in (x - w / 2 + 20, x + w / 2 - 20):
        paint(rectPts(px - 10, y - h, 20, h), wash='#4A4E86', ink=INK, sw=.9, lite=True)
    paint([[x - w / 2 - 40, y - h + 10], [x + w / 2 + 40, y - h + 10], [x + w / 2 + 10, y - h - 50], [x - w / 2 - 10, y - h - 50]], wash='#C8564F',
          fill='#963A35', fillOp=60, ink=INK, sw=1)
    # stop sign
    paint(rectPts(x - w / 2 - 100, y - h - 10, 14, h + 10), wash='#4A4E86', ink=INK, sw=.8, lite=True)
    paint(ellPts(x - w / 2 - 93, y - h - 40, 54, 54, 24), wash='#3A9C98', ink=INK, sw=1)
    text('站', x - w / 2 - 93, y - h - 40, 54, PAL['cream'], shadow=False)


# ---------------------------------------------------------------- S06: restaurant: cloche, heart cake, menu board
def cloche(x, y, s, key='clo', tilt=0.0):
    """silver dome; (x, y) = centre of its rim"""
    push()
    translate(x, y)
    rotate(tilt)
    boilSeed(key)
    d = [[-2.6 * s, 0]]
    for i in range(1, 20):
        a = math.pi + i / 20 * math.pi
        d.append([math.cos(a) * 2.6 * s, math.sin(a) * 2.2 * s])
    d.append([2.6 * s, 0])
    paint(d, wash='#D8DEE8', fill='#9AA3B8', fillOp=70, ink=INK, sw=1.1)
    paint(ellPts(-1.1 * s, -1.4 * s, .5 * s, .9 * s, 14, 0, -.5), wash='#FFFFFF', washOp=170, ink=None)
    paint(rrPts(-2.75 * s, -.18 * s, 5.5 * s, .36 * s, .15 * s), wash='#B8C0D0', ink=INK, sw=.8)
    paint(ellPts(0, -2.35 * s, .35 * s, .28 * s, 12), wash='#B8C0D0', ink=INK, sw=.8)
    pop()


def heartCake(x, y, s, t, key='cake', figure=True):
    """(x, y) = plate centre"""
    boilSeed(key)
    paint(ellPts(x, y, 3.3 * s, .6 * s, 28), wash='#FFFFFF', fill='#D9D2C2', fillOp=40, ink=INK, sw=.9)
    # cake: a heart prism (top face + front)
    top = heartPts(x, y - 1.6 * s, 2.0 * s, 30)
    top = [[px, y - 1.6 * s + (py - (y - 1.6 * s)) * .45] for px, py in top]
    front = [[p[0], p[1] + 1.1 * s] for p in top]
    paint([[x - 2.0 * s, y - 1.95 * s]] + [[x - 2.0 * s, y - .8 * s]] + [[x, y - .1 * s]] + [[x + 2.0 * s, y - .8 * s], [x + 2.0 * s, y - 1.95 * s]],
          wash='#F28FB0', fill='#C8567A', fillOp=60, ink=INK, sw=1)
    inkLine([[x - 2.0 * s, y - 1.3 * s], [x, y - .65 * s], [x + 2.0 * s, y - 1.3 * s]], .8, '#FFFFFF', 'ink', .3)
    paint(top, wash='#FBD0DA', fill='#F59AB0', fillOp=50, ink=INK, sw=1)
    for i in range(7):
        a = i / 7 * TAU
        paint(ellPts(x + math.cos(a) * 1.4 * s, y - 1.75 * s + math.sin(a) * .35 * s, .2 * s, .2 * s, 8), wash='#E8476E', ink=INK, sw=.4)
    if figure:
        clawd(x, y - 1.75 * s, .19 * s, dict(col='#EE9AAE', dk='#C0637B', lt='#FBD0DA', hat='flower', eyes='happy', mouth='smile', view='front',
                                            noShadow=True, aL=1.0, aR=1.0, boilKey=key + 'fig'))


def menuBoard(x, y, w, h, t, items, key='menu'):
    """items: list of (text, appear_k, col)"""
    boilSeed(key)
    paint(rectPts(x - 14, y - 14, w + 28, h + 28), wash='#8A5A3C', ink=INK, sw=1)
    paint(rectPts(x, y, w, h), wash='#2E3B36', fill='#22302B', fillOp=60, ink=INK, sw=.8)
    text('今日特供', x + w / 2, y + 50, 46, '#FFF5E2', shadow=False)
    inkLine([[x + 40, y + 88], [x + w - 40, y + 88]], .6, '#FFF5E2', 'inkfine', 0)
    for i, (tx, k, col) in enumerate(items):
        if k <= 0:
            continue
        text(tx, x + w / 2, y + 140 + i * 66, 44 if len(tx) > 1 else 72, col, shadow=False, sc=backOut(clamp(k)), a=clamp(k * 2))


def tableCloth(x0, x1, y, drop=420, key='tc'):
    boilSeed(key)
    paint([[x0, y], [x1, y], [x1 + 20, y + drop], [x0 - 20, y + drop]], wash='#FFFDF6', fill='#E9DFD0', fillOp=40, ink=INK, sw=1)
    for i in range(int((x1 - x0) / 70) + 1):
        xx = x0 + i * 70
        G.c.drawLine(xx, y, xx + (xx - (x0 + x1) / 2) * .04, y + drop, skia.Paint(AntiAlias=True, Color=skcol('#F2A3B8', .35), StrokeWidth=16))
    for j in range(6):
        G.c.drawLine(x0 - 10, y + 30 + j * 70, x1 + 10, y + 30 + j * 70, skia.Paint(AntiAlias=True, Color=skcol('#F2A3B8', .25), StrokeWidth=16))


# ---------------------------------------------------------------- S07: claw machine
PLUSH = [('#F7C65C', '#C99A2E', '#FBE7A1'), ('#7DD3C8', '#4FA79C', '#C9EFEA'), ('#9C8FE0', '#7166B8', '#D3CCF5'), ('#F59A6B', '#C46E44', '#FBD0B5'),
         ('#A3B5A8', '#77897C', '#CCD9CF'), ('#7FB8EE', '#5288C0', '#CFE4F8')]


def plush(x, y, u, i, key='pl', face='happy', rot=0.0, flower=False, col=None):
    c = col or PLUSH[i % len(PLUSH)]
    clawd(x, y, u, dict(col=c[0], dk=c[1], lt=c[2], eyes=face, mouth='smile' if face == 'happy' else 'cat', view='front', noShadow=True, lite=True,
                        rot=rot, aL=.6, aR=.6, boilKey=f'{key}{i}', hat='flower' if flower else None))


def clawHead(x, y, s, open_=1.0, key='claw'):
    boilSeed(key)
    paint(rrPts(x - .9 * s, y - .8 * s, 1.8 * s, 1.0 * s, .2 * s), wash='#C8CED8', fill='#8A93A8', fillOp=60, ink=INK, sw=.9)
    for side in (-1, 0, 1):
        a = side * (.35 + .5 * open_)
        x0, y0 = x + side * .5 * s, y + .2 * s
        x1, y1 = x0 + math.sin(a) * 1.4 * s, y0 + math.cos(a) * 1.4 * s
        x2, y2 = x1 - side * .5 * s * (1 - open_ * .3) - (0 if side else 0), y1 + .6 * s
        inkLine([[x0, y0], [x1, y1], [x2, y2]], 1.8, '#5E6680', 'ink', .2)


def clawMachine(x, y, w, h, t, lights=0.0, key='cm'):
    """(x, y) = floor centre. returns the glass box rect (x0, y0, x1, y1)."""
    boilSeed(key)
    x0, x1 = x - w / 2, x + w / 2
    top = y - h
    gy1 = y - h * .36
    paint(rrPts(x0 - 20, top - 70, w + 40, 100, 30), wash='#E8476E', fill='#B8324F', fillOp=60, ink=INK, sw=1.2)
    text('抓抓乐', x, top - 22, 64, '#FFF5E2', stroke=INK, strokeW=9)
    for i in range(14):
        bx = x0 + 10 + i * (w + 0) / 13
        on = (int(t * 8) + i) % 2 == 0 or lights > .5
        paint(ellPts(bx - 10, top - 76, 9, 9, 8), wash='#FFF2B0' if on else '#B89A60', ink=INK, sw=.4)
    paint(rectPts(x0, top + 30, w, gy1 - top - 30), wash='#3A2E58', ink=INK, sw=1.2)
    glow(x, top + 200, w * .7, '#FFE2F0', .35 + .3 * lights)
    paint(rectPts(x0, gy1, w, y - gy1), wash='#7DD3C8', fill='#4FA79C', fillOp=60, ink=INK, sw=1.2)
    for i in range(6):
        inkLine([[x0 + 20, gy1 + 30 + i * 40], [x1 - 20, gy1 + 30 + i * 40]], .5, '#4FA79C', 'inkfine', 0)
    # control panel
    paint([[x0 - 30, gy1], [x1 + 30, gy1], [x1, gy1 + 70], [x0, gy1 + 70]], wash='#F7C65C', fill='#C99A2E', fillOp=50, ink=INK, sw=1)
    # prize chute + coin slot
    paint(rrPts(x0 + 40, gy1 + 120, 200, 150, 14), wash='#2A2440', ink=INK, sw=1)
    paint(rrPts(x1 - 140, gy1 + 130, 70, 110, 10), wash='#C8CED8', ink=INK, sw=.9)
    inkLine([[x1 - 105, gy1 + 150], [x1 - 105, gy1 + 200]], 1.6, INK, 'ink', 0)
    return (x0 + 14, top + 44, x1 - 14, gy1 - 6)


def joystick(x, y, s, tilt=0.0, key='js'):
    boilSeed(key)
    paint(ellPts(x, y, 1.0 * s, .35 * s, 16), wash='#2A2440', ink=INK, sw=.8)
    tx, ty = x + math.sin(tilt) * 1.6 * s, y - math.cos(tilt) * 1.6 * s
    inkLine([[x, y], [tx, ty]], 2.4, INK, 'ink', 0)
    paint(ellPts(tx, ty, .5 * s, .5 * s, 14), wash='#E8476E', ink=INK, sw=.8)


# ---------------------------------------------------------------- S08: detective office, cork board
def blindsWindow(x, y, w, h, t, key='bl'):
    boilSeed(key)
    paint(rectPts(x, y, w, h), wash='#FFE7B8', ink=INK, sw=1)
    for i in range(int(h / 34)):
        yy = y + 10 + i * 34
        paint(rectPts(x + 6, yy, w - 12, 20), wash='#E8D3B0', fill='#C9A97E', fillOp=50, ink=INK, sw=.5, lite=True)
    inkLine([[x + w * .3, y], [x + w * .3, y + h]], .6, INK, 'inkfine', 0)


def blindStripes(x0, y0, w, h, ang=.35, a=.16):
    for i in range(9):
        yy = y0 + i * 60
        flat([[x0, yy], [x0 + w, yy + w * ang], [x0 + w, yy + w * ang + 28], [x0, yy + 28]], '#FFE7B8', a)


def stickyNote(x, y, s, flip, rot=0.0, key='sn'):
    """flip 0..1: 0 = yellow '?' side, 1 = pink heart side (turns through edge-on at .5)"""
    sx = abs(math.cos(flip * math.pi))
    heart = flip > .5
    push()
    translate(x, y)
    rotate(rot)
    scale(max(.02, sx), 1)
    boilSeed(key + ('h' if heart else 'q'))
    paint(rectPts(-s, -s, 2 * s, 2 * s, s * .03), wash='#FBD0DA' if heart else '#FBE7A1', fill='#F59AB0' if heart else '#F2C53D', fillOp=40, ink=INK, sw=.8)
    if heart:
        paint(heartPts(0, s * .05, s * .62, 22), wash='#E8476E', ink=INK, sw=.6)
    else:
        text('?', 0, s * .05, s * 1.5, '#5B4A66', shadow=False)
    pop()
    boilSeed(key + 'pin')
    paint(ellPts(x, y - s * .85, s * .14, s * .14, 10), wash='#E03A4E', ink=INK, sw=.5)


def pin(x, y, r=9, col='#E03A4E', key='pin'):
    boilSeed(key)
    paint(ellPts(x, y, r, r, 10), wash=col, ink=INK, sw=.5)
    paint(ellPts(x - r * .3, y - r * .3, r * .3, r * .3, 6), wash='#FFFFFF', ink=None)


# ---------------------------------------------------------------- S09: crystal ball futures
def tentBack(t, key='tent'):
    gradRect(-200, -200, W + 400, H + 400, ['#2A1F4E', '#5B3F8C'])
    for i in range(14):
        a0 = -math.pi / 2 + (i - 6.5) * .22
        boilSeed(f'{key}{i}')
        x1 = 960 + math.cos(a0) * 2400
        y1 = -260 + math.sin(a0) * 2400 + 2400
        flat([[960, -260], [960 + (i - 6.5) * 320 - 160, 1400], [960 + (i - 6.5) * 320 + 160, 1400]], '#6E4FA0' if i % 2 else '#4B3480', .5)
    for i in range(9):
        x = 160 + i * 200
        L = 120 + 120 * hash1(i * 2.3)
        inkLine([[x, -20], [x, L]], .6, '#C9B8EC', 'inkfine', 0)
        sw_ = math.sin(t * 2 + i) * .15
        if i % 3 == 0:
            boilSeed(f'{key}m{i}')
            paint(ellPts(x, L + 22, 22, 22, 18), wash='#FFE36E', ink=INK, sw=.6)
            paint(ellPts(x + 9, L + 16, 18, 18, 18), wash='#5B3F8C', ink=None)
        else:
            paint(starPts(x, L + 20, 20, .45, 5, sw_), wash='#FFE36E', ink=INK, sw=.5)


def lemniscate(cx, cy, a, k=1.0, col='#E8476E', sw=3.0):
    pts = []
    n = max(2, int(80 * k))
    for i in range(n):
        th = i / 79 * TAU
        d = 1 + math.sin(th) ** 2
        pts.append([cx + a * math.cos(th) / d, cy + a * math.sin(th) * math.cos(th) / d])
    inkLine(pts, sw, col, 'ink', 0)


def ballVision(i, cx, cy, r, t, key='bv'):
    """the i-th future inside the crystal ball (drawn into a clip already set)"""
    G.c.save()
    if i == 0:      # a little house, two of them in front, heart smoke
        gradRect(cx - r, cy - r, 2 * r, 2 * r, ['#BFE3F5', '#F3E6C8'])
        flatRect(cx - r, cy + r * .35, 2 * r, r, '#9ED27A')
        boilSeed(key + 'h')
        paint(rectPts(cx - r * .35, cy - r * .2, r * .7, r * .55), wash='#F7D79A', ink=INK, sw=.8)
        paint([[cx - r * .45, cy - r * .2], [cx, cy - r * .62], [cx + r * .45, cy - r * .2]], wash='#C8564F', ink=INK, sw=.8)
        paint(rectPts(cx - r * .08, cy + r * .1, r * .16, r * .25), wash='#8A5A3C', ink=INK, sw=.6)
        for j in range(3):
            paint(heartPts(cx + r * .3 + j * 8, cy - r * .7 - j * r * .14 - (t * 30 % 20), r * .06 + j * 3, 14), wash='#E8476E', ink=None)
        clawd(cx - r * .62, cy + r * .58, r * .065, dict(col='#EE9AAE', dk='#C0637B', lt='#FBD0DA', hat='flower', eyes='happy', mouth='smile', noShadow=True, lite=True, boilKey=key + 'a'))
        clawd(cx + r * .62, cy + r * .58, r * .065, dict(col=PAL['clay'], dk=PAL['clayDk'], lt='#F5B394', eyes='happy', mouth='smile', noShadow=True, lite=True, boilKey=key + 'b'))
    elif i == 1:    # wedding: veil, bells, petals
        gradRect(cx - r, cy - r, 2 * r, 2 * r, ['#FCE3EC', '#F7C6D2'])
        for j in range(2):
            boilSeed(key + f'bell{j}')
            bx = cx + (j * 2 - 1) * r * .28
            paint([[bx - r * .14, cy - r * .3], [bx + r * .14, cy - r * .3], [bx + r * .09, cy - r * .62], [bx - r * .09, cy - r * .62]], wash='#F2C53D', ink=INK, sw=.6)
        clawd(cx - r * .32, cy + r * .66, r * .07, dict(col='#EE9AAE', dk='#C0637B', lt='#FBD0DA', hat=['flower'], eyes='happy', mouth='smile', noShadow=True, lite=True,
                                                    boilKey=key + 'c', draw=lambda u, sw: veilShape(u, sw, .8)))
        clawd(cx + r * .32, cy + r * .66, r * .07, dict(col=PAL['clay'], dk=PAL['clayDk'], lt='#F5B394', hat='top', eyes='happy', mouth='smile', noShadow=True, lite=True, boilKey=key + 'd'))
        for j in range(10):
            ph = frac(t * .5 + hash1(j))
            paint(ellPts(cx - r + hash1(j * 3) * 2 * r, cy - r + ph * 2 * r, 6, 4, 6), wash='#FFFFFF', ink=None)
    elif i == 2:    # old couple on a bench, glasses and a cane
        gradRect(cx - r, cy - r, 2 * r, 2 * r, ['#F7B28A', '#FBD3C7'])
        boilSeed(key + 'bench')
        paint(rectPts(cx - r * .6, cy + r * .42, r * 1.2, r * .08), wash='#B9784E', ink=INK, sw=.6)
        for j, (col, dk, lt) in enumerate([('#E9B9C4', '#B98896', '#F6DCE2'), ('#D9A58C', '#A8775F', '#EFCDBD')]):
            x = cx + (j * 2 - 1) * r * .3
            clawd(x, cy + r * .5, r * .065, dict(col=col, dk=dk, lt=lt, hat='flower' if j == 0 else None, eyes='closed', mouth='smile', noShadow=True, lite=True,
                                                boilKey=key + f'o{j}', draw=lambda u, sw: glasses(u, sw)))
        inkLine([[cx + r * .62, cy + r * .5], [cx + r * .66, cy + r * .05], [cx + r * .56, cy - r * .02]], 2.0, '#8A5A3C', 'ink', .4)
        paint(heartPts(cx, cy - r * .35, r * .14 * (1 + .1 * pulse(t, 6)), 18), wash='#E8476E', ink=INK, sw=.5)
    else:           # forever
        gradRect(cx - r, cy - r, 2 * r, 2 * r, ['#5B3F8C', '#C77AA0'])
        for j in range(16):
            sparkle(cx - r + hash1(j * 7) * 2 * r, cy - r + hash1(j * 3) * 2 * r, 6 + 6 * hash1(j), '#FFF5E2')
        lemniscate(cx, cy, r * .62, 1.0, '#FFE36E', 4.0)
        paint(heartPts(cx - r * .38, cy, r * .13, 16), wash='#E8476E', ink=INK, sw=.5)
        paint(heartPts(cx + r * .38, cy, r * .13, 16), wash='#E8476E', ink=INK, sw=.5)
    G.c.restore()


def veilShape(u, sw, k=1.0):
    """bridal veil over a Clawd's head (draw hook in body coords)"""
    boilSeed('veil')
    P = [[-3.6 * u, -8.2 * u], [0, -9.4 * u], [3.6 * u, -8.2 * u], [5.6 * u * k, -2.0 * u], [4.0 * u, -1.6 * u], [3.4 * u, -6.8 * u], [-3.4 * u, -6.8 * u],
         [-4.0 * u, -1.6 * u], [-5.6 * u * k, -2.0 * u]]
    paint(P, wash='#FFFFFF', washOp=150, ink=INK, sw=sw * .5, curv=.4)
    paint(ellPts(0, -8.9 * u, 1.0 * u, .5 * u, 12), wash='#FFFFFF', ink=INK, sw=sw * .4)


def glasses(u, sw):
    for s in (-1, 1):
        paint(ellPts(s * 2.5 * u, -6 * u, 1.1 * u, 1.0 * u, 12), ink=INK, sw=sw * .5)
    inkLine([[-1.4 * u, -6.1 * u], [1.4 * u, -6.1 * u]], sw * .4, INK, 'inkfine', 0)


def crystalBall(cx, cy, r, t, vision, mix=1.0, key='cb'):
    """vision: index of the current future (-1 = misty); mix = swirl-in amount 0..1"""
    boilSeed(key + 'st')
    paint([[cx - r * .75, cy + r * 1.25], [cx + r * .75, cy + r * 1.25], [cx + r * .5, cy + r * .85], [cx - r * .5, cy + r * .85]], wash='#C99A2E', fill='#8E6A3E', fillOp=50, ink=INK, sw=1)
    glow(cx, cy, r * 2.4, '#C9B8EC', .5)
    circ = skia.Path()
    circ.addCircle(cx, cy, r)
    G.c.save()
    G.c.clipPath(circ, skia.ClipOp.kIntersect, True)
    gradRect(cx - r, cy - r, 2 * r, 2 * r, ['#D9CCF2', '#9C8FE0'])
    if vision >= 0:
        G.c.saveLayerAlpha(None, int(255 * clamp(mix)))
        ballVision(vision, cx, cy, r, t, key=key + f'v{vision}')
        G.c.restore()
    # swirl mist on top
    for j in range(4):
        a0 = t * 2.5 + j * TAU / 4
        pts = [[cx + math.cos(a0 + q * .35) * r * (.85 - q * .06), cy + math.sin(a0 + q * .35) * r * (.85 - q * .06)] for q in range(8)]
        inkLine(pts, 3.0 * (1 - clamp(mix) * .7), '#FFFFFF', 'dry', .4)
    G.c.restore()
    paint(ellPts(cx - r * .35, cy - r * .45, r * .3, r * .16, 12, 0, -.6), wash='#FFFFFF', washOp=170, ink=None)
    boilSeed(key + 'rim')
    paint(ellPts(cx, cy, r, r, 40), ink=INK, sw=1.3)


# ---------------------------------------------------------------- S11: storm, lightning
def bolt(x0, y0, x1, y1, k=1.0, seed=0, col='#FFF6B0', w=4.0):
    """zigzag lightning from (x0,y0) to (x1,y1); k = how far it has reached"""
    n = 7
    pts = [[x0, y0]]
    for i in range(1, n):
        q = i / n
        if q > k:
            break
        off = (hash1(seed * 13 + i) - .5) * 120
        pts.append([lerp(x0, x1, q) + off, lerp(y0, y1, q)])
    if k >= 1:
        pts.append([x1, y1])
    if len(pts) < 2:
        return
    for (a, b) in zip(pts, pts[1:]):
        glow((a[0] + b[0]) / 2, (a[1] + b[1]) / 2, 90, '#FFF6B0', .35)
    G.c.drawPath(eng._path(pts, False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w * 3.2, Color=skcol(INK),
                                                    StrokeJoin=skia.Paint.kRound_Join, StrokeCap=skia.Paint.kRound_Cap))
    G.c.drawPath(eng._path(pts, False), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w * 2, Color=skcol(col),
                                                    StrokeJoin=skia.Paint.kRound_Join, StrokeCap=skia.Paint.kRound_Cap))


def rainLines(t, seed, n, x0, y0, x1, y1, col='#C9D6F0', ln=40, sp=1500, ang=.2, sw=.8):
    tt = onTwos(t)
    for i in range(n):
        x = lerp(x0, x1, hash1(seed + i * 3.3))
        y = y0 + (hash1(seed + i * 7.1) * (y1 - y0) + tt * sp) % (y1 - y0)
        inkLine([[x, y], [x - ln * ang, y + ln]], sw, col, 'inkfine', 0)


# ---------------------------------------------------------------- S12: heart piggy bank
def piggy(x, y, s, broken=0.0, key='pig'):
    """heart-shaped piggy bank; broken 0..1 splits it in two halves"""
    boilSeed(key)
    for side in (-1, 1):
        dx = side * broken * 1.4 * s
        rot = side * broken * .5
        push()
        translate(x + dx, y)
        rotate(rot)
        P = heartPts(0, 0, 2.2 * s, 30)
        if broken > .02:
            P = [p for p in P if (p[0] <= 0 if side < 0 else p[0] >= 0)]
            P += [[0, 1.8 * s], [side * .2 * s, .8 * s], [-side * .2 * s, 0], [side * .15 * s, -1.0 * s]]
            P = P if side > 0 else P
        paint(P, wash='#F59AB0', fill='#E8476E', fillOp=50, ink=INK, sw=1.1)
        if side > 0 and broken < .02:
            pass
        pop()
    if broken < .02:
        paint(rrPts(x - .8 * s, y - 1.6 * s, 1.6 * s, .25 * s, .1 * s), wash=INK, ink=None)
        paint(ellPts(x + 1.2 * s, y - .2 * s, .45 * s, .35 * s, 12), wash='#F7C6D2', ink=INK, sw=.6)
        for q in (-1, 1):
            paint(ellPts(x + 1.1 * s + q * .14 * s, y - .2 * s, .07 * s, .1 * s, 6), wash=INK, ink=None)
        paint(ellPts(x - .2 * s, y - .5 * s, .12 * s, .12 * s, 6), wash=INK, ink=None)


def heartRain(t, t0, seed, n, x0, x1, y0, yfloor, s=26):
    """hearts that start falling at t0 and pile up at yfloor"""
    if t < t0:
        return
    for i in range(n):
        st = t0 + hash1(seed + i) * .35
        if t < st:
            continue
        a = t - st
        x = lerp(x0, x1, hash1(seed * 3 + i * 1.7))
        y = y0 + a * a * 2600 + a * 300
        yf = yfloor - (i % 7) * s * .9 - hash1(i) * s
        if y > yf:
            y = yf
        boilSeed(f'hr{seed}{i}')
        paint(heartPts(x, y, s * (.8 + .4 * hash1(i * 5)), 16), wash=['#E8476E', '#F59AB0', '#FF8FB1'][i % 3], ink=INK, sw=.5, lite=True)


# ---------------------------------------------------------------- S13: line-up
def lineupWall(t, key='lw'):
    flatRect(-200, -200, W + 400, H + 400, '#C9CDD8')
    for i in range(9):
        y = 180 + i * 80
        inkLine([[-200, y], [W + 200, y]], .8 if i % 2 == 0 else .4, '#5B6070', 'inkfine', 0)
        if i % 2 == 0:
            text(f'{200 - i * 10}', 90, y - 22, 30, '#5B6070', shadow=False)
    flatRect(-200, 900, W + 400, 400, '#8A8EA0')
    inkLine([[-200, 900], [W + 200, 900]], 1.0, INK, 'ink', 0)


def placard(x, y, num, key='plc'):
    boilSeed(key)
    paint(rectPts(x - 60, y - 40, 120, 80), wash='#2E2A40', ink=INK, sw=.8)
    text(str(num), x, y, 56, '#FFF5E2', shadow=False)


def bigX(x, y, s, k=1.0, col='#D8394E'):
    if k <= 0:
        return
    p = backOut(clamp(k))
    for sgn in (-1, 1):
        G.c.drawLine(x - s * p, y - s * p * sgn, x + s * p, y + s * p * sgn,
                     skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=s * .42, StrokeCap=skia.Paint.kRound_Cap))
        G.c.drawLine(x - s * p, y - s * p * sgn, x + s * p, y + s * p * sgn,
                     skia.Paint(AntiAlias=True, Color=skcol(col), StrokeWidth=s * .28, StrokeCap=skia.Paint.kRound_Cap))


def lens(x, y, r, key='lens'):
    boilSeed(key)
    glow(x, y, r * 1.4, '#FFFFFF', .25)
    paint(ellPts(x, y, r, r, 36), wash='#DDF2FF', washOp=60, ink=None)
    paint(ellPts(x - r * .35, y - r * .4, r * .25, r * .13, 10, 0, -.6), wash='#FFFFFF', washOp=180, ink=None)
    paint(ellPts(x, y, r, r, 36), ink='#C99A2E', sw=4)
    push()
    translate(x + r * .72, y + r * .72)
    rotate(.78)
    paint(rectPts(0, -r * .12, r * 1.1, r * .24), wash='#7A4E33', ink=INK, sw=1.2)
    pop()


# ---------------------------------------------------------------- S14: the big wave
def bigWave(t, rise=1.0, crash=0.0, key='wv'):
    """a giant curling wave on the right; crash 0..1 drops the lip"""
    up = 120 * rise
    boilSeed(key)
    body = [[-300, 1300], [-300, 830], [300, 810], [700, 720], [950, 560], [1150, 380 - up * .8], [1350, 290 - up], [1520, 330 - up * .8],
            [1680, 540], [1840, 770], [2200, 830], [2200, 1300]]
    paint(throughClosed(body, 4), wash='#3E8FC9', fill='#2B6DA6', fillOp=60, ink=INK, sw=1.4)
    inner = [[700, 760], [950, 610], [1140, 440 - up * .7], [1320, 360 - up * .9], [1460, 420 - up * .6], [1560, 600], [1600, 820], [800, 830]]
    paint(throughClosed(inner, 4), wash='#7CC3E8', washOp=200, ink=None)
    for i in range(5):
        y = 640 + i * 40
        inkLine([[820 + i * 40, y], [1100 + i * 30, y - 50], [1400, y - 30]], .7, '#CFEAF8', 'inkfine', .5)
    # the lip: pivots at the crest and falls forward when it crashes
    push()
    translate(1350, 290 - up)
    rotate(-crash * 1.1)
    lip = [[0, 0], [-120, -20], [-250, 10], [-330, 90], [-330, 170], [-290, 130], [-230, 100], [-140, 90], [-60, 70]]
    paint(throughClosed(lip, 4), wash='#5AA9DA', fill='#2B6DA6', fillOp=40, ink=INK, sw=1.2)
    foam = [[20, -10], [-120, -36], [-250, -8], [-340, 80], [-345, 180]]
    inkLine(foam, 4.0, '#FFFFFF', 'ink', .5)
    for j in range(6):
        fx, fy = lerp(-340, 0, j / 5), -20 - 10 * math.sin(j * 1.7)
        paint(ellPts(fx, fy, 26, 18, 12), wash='#FFFFFF', ink=INK, sw=.5)
    pop()
    # sea in front
    flatRect(-300, 830, W + 600, 600, '#2B6DA6')
    for i in range(7):
        y = 860 + i * 34
        boilSeed(f'{key}s{i}')
        pts = [[-300 + k * 120, y + 10 * math.sin(k * 1.3 + t * 3 + i)] for k in range(20)]
        inkLine(pts, .7, '#7CC3E8', 'inkfine', .4)


def surfboard(x, y, L, ang, key='sb'):
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    paint(ellPts(0, 0, L / 2, 22, 30), wash='#F28FB0', fill='#E8476E', fillOp=40, ink=INK, sw=1)
    inkLine([[-L / 2 + 30, 0], [L / 2 - 30, 0]], 1.0, '#FFFFFF', 'ink', 0)
    paint(heartPts(0, -2, 14, 14), wash='#FFFFFF', ink=None)
    pop()


# ---------------------------------------------------------------- S15: cupid's arrow
def bowHook(draw_=0.0):
    def h(u, sw):
        boilSeed('bow')
        pts = [[.6 * u, -2.4 * u], [1.5 * u, -1.2 * u], [1.7 * u, 0], [1.5 * u, 1.2 * u], [.6 * u, 2.4 * u]]
        inkLine(pts, sw * 2.2, '#C99A2E', 'ink', .6)
        inkLine([[.6 * u, -2.4 * u], [.6 * u - draw_ * 1.2 * u, 0], [.6 * u, 2.4 * u]], sw * .6, INK, 'inkfine', 0)
    return h


def arrow(x, y, L, ang, key='ar', stuck=False):
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    inkLine([[0, 0], [-L, 0]], 2.2, '#8A5A3C', 'ink', 0)
    paint(heartPts(10, 0, 22, 16), wash='#E8476E', ink=INK, sw=.7) if not stuck else None
    for s in (-1, 1):
        paint([[-L, 0], [-L - 30, s * 18], [-L - 10, 0]], wash='#FFFFFF', ink=INK, sw=.6)
        paint([[-L + 20, 0], [-L - 10, s * 18], [-L + 10, 0]], wash='#F7C6D2', ink=INK, sw=.5)
    pop()


# ---------------------------------------------------------------- S16: roller coaster
COASTER = [[-500, 760], [100, 740], [600, 560], [1000, 330], [1300, 240], [1520, 300], [1800, 640], [2050, 900], [2400, 960], [2800, 880],
           [3300, 760], [3800, 800], [4300, 820]]


def _trackPts():
    P = through(COASTER, 10)
    L = [0.0]
    for a, b in zip(P, P[1:]):
        L.append(L[-1] + math.hypot(b[0] - a[0], b[1] - a[1]))
    return P, L


TRACK, TRACK_L = _trackPts()


def trackAtX(x):
    """(y, angle) of the track at world x"""
    for a, b in zip(TRACK, TRACK[1:]):
        if a[0] <= x <= b[0]:
            k = (x - a[0]) / max(1e-6, b[0] - a[0])
            return lerp(a[1], b[1], k), math.atan2(b[1] - a[1], b[0] - a[0])
    return TRACK[-1][1], 0.0


def drawTrack(x0, x1, key='trk'):
    pts = [p for p in TRACK if x0 - 200 <= p[0] <= x1 + 200]
    for i, p in enumerate(pts[::6]):
        boilSeed(f'{key}p{i}')
        inkLine([[p[0], p[1] + 20], [p[0], 1400]], 1.6, '#8A6A8E', 'ink', 0)
        if i % 2:
            inkLine([[p[0], p[1] + 120], [p[0] + 90, 1400]], .8, '#8A6A8E', 'inkfine', 0)
    up = [[p[0], p[1] + 14] for p in pts]
    inkLine(pts, 3.4, '#C8324A', 'ink', 0)
    inkLine(up, 2.0, '#8E1E35', 'ink', 0)
    for i, p in enumerate(pts[::3]):
        G.c.drawLine(p[0], p[1], p[0], p[1] + 14, skia.Paint(AntiAlias=True, Color=skcol(INK, .7), StrokeWidth=3))


def cart(x, y, ang, u, t, armsUp=0.0, key='cart', emoH='happy', emoM='happy'):
    push()
    translate(x, y)
    rotate(ang)
    # riders first (their lower halves go behind the car body)
    her(-120, -40, u, fo(feel(emoH, t), view='q', noLegs=True, noShadow=True, aL=lerp(.2, 1.6, armsUp), aR=lerp(.2, 1.6, armsUp), boilKey=key + 'h'))
    him(140, -40, u, fo(feel(emoM, t), view='q', noLegs=True, noShadow=True, aL=lerp(.2, 1.6, armsUp), aR=lerp(.2, 1.6, armsUp), boilKey=key + 'm'))
    boilSeed(key)
    paint(rrPts(-300, -110, 600, 110, 30), wash='#E8476E', fill='#B8324F', fillOp=50, ink=INK, sw=1.2)
    paint([[260, -110], [330, -110], [330, -30], [300, 0], [260, 0]], wash='#F2C53D', ink=INK, sw=1)
    paint(heartPts(0, -55, 34, 18), wash='#FFFFFF', ink=INK, sw=.6)
    for wx in (-200, 200):
        paint(ellPts(wx, 6, 22, 22, 14), wash='#3A3550', ink=INK, sw=.8)
    pop()


def ferrisWheel(x, y, r, t, key='fw'):
    boilSeed(key)
    a0 = t * .3
    paint(ellPts(x, y, r, r, 40), ink='#B86FA0', sw=2.4)
    for i in range(8):
        a = a0 + i * TAU / 8
        inkLine([[x, y], [x + math.cos(a) * r, y + math.sin(a) * r]], .8, '#B86FA0', 'inkfine', 0)
        paint(rrPts(x + math.cos(a) * r - 22, y + math.sin(a) * r, 44, 36, 8), wash=['#F28FB0', '#7DD3C8', '#F7C65C', '#9C8FE0'][i % 4], ink=INK, sw=.6)
    inkLine([[x, y], [x - r * .7, y + r * 1.6]], 2.0, '#8A6A8E', 'ink', 0)
    inkLine([[x, y], [x + r * .7, y + r * 1.6]], 2.0, '#8A6A8E', 'ink', 0)


def heartArch(x, y, s, key='harch'):
    boilSeed(key)
    P = heartPts(x, y, s, 36)
    inkLine(P + [P[0]], 9, '#E8476E', 'ink', 0)
    for i in range(12):
        p = P[i * 3]
        glow(p[0], p[1], 40, '#FFE6A0', .7)
        G.c.drawCircle(p[0], p[1], 8, skia.Paint(AntiAlias=True, Color=skcol('#FFF6C2')))


# ---------------------------------------------------------------- S17: parade
def bunting(x0, x1, y, sag, n, t, key='bt'):
    pts = [[lerp(x0, x1, i / 30), y + sag * math.sin(i / 30 * math.pi)] for i in range(31)]
    inkLine(pts, .8, INK, 'inkfine', .3)
    for i in range(n):
        k = (i + .5) / n
        bx, by = lerp(x0, x1, k), y + sag * math.sin(k * math.pi)
        sw_ = math.sin(t * 3 + i) * 6
        boilSeed(f'{key}{i}')
        paint([[bx - 26, by], [bx + 26, by], [bx + sw_, by + 56]], wash=['#E8476E', '#F7C65C', '#7DD3C8', '#9C8FE0', '#F59A6B'][i % 5], ink=INK, sw=.6)


def balloon(x, y, r, col, t, key='bln'):
    boilSeed(key)
    yy = y + math.sin(t * 2 + x) * 10
    inkLine([[x, yy + r * 1.2], [x + 10 * math.sin(t * 3 + x), yy + r * 3.2]], .6, INK, 'inkfine', .5)
    paint(ellPts(x, yy, r, r * 1.2, 20), wash=col, ink=INK, sw=.8)
    paint(ellPts(x - r * .35, yy - r * .4, r * .2, r * .3, 8), wash='#FFFFFF', washOp=180, ink=None)


def floatCar(x, y, w, t, key='flt'):
    """parade float: (x, y) = deck top centre"""
    boilSeed(key)
    paint(rrPts(x - w / 2, y, w, 150, 24), wash='#F7C6D2', fill='#E8476E', fillOp=40, ink=INK, sw=1.2)
    for i in range(14):
        fx = x - w / 2 + 30 + i * (w - 60) / 13
        paint(ellPts(fx, y + 4, 22, 22, 12), wash=['#FFFFFF', '#FFE36E', '#F28FB0'][i % 3], ink=INK, sw=.5)
    for i in range(5):
        paint(heartPts(x - w / 2 + 90 + i * (w - 180) / 4, y + 85, 28, 16), wash='#E8476E', ink=INK, sw=.6)
    for wx in (x - w / 2 + 110, x + w / 2 - 110):
        paint(ellPts(wx, y + 160, 44, 44, 18), wash='#3A3550', ink=INK, sw=.9)
        paint(ellPts(wx, y + 160, 16, 16, 10), wash='#C8CED8', ink=None)
    # heart arch behind them
    P = heartPts(x, y - 260, 260, 36)
    inkLine(P + [P[0]], 10, '#FF8FB1', 'ink', 0)
    for i in range(12):
        p = P[i * 3]
        paint(ellPts(p[0], p[1], 14, 14, 10), wash=['#FFFFFF', '#FFE36E'][i % 2], ink=INK, sw=.4)


def heartSign(x, y, s, k=1.0, key='hsg'):
    if k <= .01:
        return
    p = backOut(clamp(k))
    boilSeed(key)
    inkLine([[x, y], [x, y - 2.2 * s * p]], 1.4, '#8A5A3C', 'ink', 0)
    paint(heartPts(x, y - 2.6 * s * p, s * p, 18), wash='#E8476E', fill='#B8324F', fillOp=40, ink=INK, sw=.7)


# ---------------------------------------------------------------- S18 / S19: proposal and finale
def ringBoxHook(k=1.0):
    def h(u, sw):
        ringBox(.9 * u, .3 * u, .9 * u, k, key='rbx')
    return h


def redBook(x, y, s, k=1.0, key='rb'):
    """a red booklet with gold lettering (肖太太)"""
    if k <= .01:
        return
    p = backOut(clamp(k))
    push()
    translate(x, y)
    scale(p)
    rotate(-.06)
    boilSeed(key)
    paint(rrPts(-1.6 * s, -2.1 * s, 3.2 * s, 4.2 * s, .2 * s), wash='#C8243A', fill='#8E1427', fillOp=60, ink=INK, sw=1.2)
    paint(rrPts(-1.35 * s, -1.85 * s, 2.7 * s, 3.7 * s, .15 * s), ink='#F2C53D', sw=1.0)
    paint(heartPts(0, -.75 * s, .55 * s, 18), wash='#F2C53D', ink=None)
    text('肖太太', 0, .6 * s, .78 * s, '#F2C53D', shadow=False)
    pop()


def sealMark(x, y, s, age, key='seal'):
    if age < 0:
        return
    k = backOut(clamp(age / .12))
    push()
    translate(x, y)
    scale(lerp(1.6, 1, k))
    rotate(.12)
    boilSeed(key)
    G.c.saveLayerAlpha(None, int(255 * clamp(age / .06)))
    paint(rrPts(-s, -s, 2 * s, 2 * s, .2 * s), ink='#E03A4E', sw=2.2)
    text('囍', 0, 0, s * 1.3, '#E03A4E', shadow=False)
    G.c.restore()
    pop()


def sunsetHill(t, key='sh'):
    gradRect(-200, -200, W + 400, 900, ['#F7A28A', '#FBC8B0', '#FFE3C8'])
    glow(960, 560, 640, '#FFE2A8', .8)
    boilSeed(key + 'sun')
    paint(ellPts(960, 600, 220, 220, 40), wash='#FFD06A', ink=INK, sw=1.2)
    for i in range(3):
        boilSeed(f'{key}b{i}')
        bx = 300 + i * 120 + (t * 40 % 200)
        by = 260 + i * 30
        inkLine([[bx - 14, by], [bx, by + 8], [bx + 14, by]], 1.0, INK, 'ink', .5)
    hills(720, ['#F49AA8', '#EE8399', '#F6B1BC'], key=key + 'h')
    for i in range(16):
        boilSeed(f'{key}f{i}')
        fx = 80 + i * 118 + 30 * hash1(i)
        fy = 1000 + 50 * hash1(i * 3)
        paint(ellPts(fx, fy, 12, 12, 10), wash=['#FFFFFF', '#FFE36E', '#F28FB0'][i % 3], ink=INK, sw=.4)
