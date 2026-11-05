# sets.py: backgrounds and props for 新地球 (watercolour + ink)
import math
from eng import *
from props import gradient, puff, sparkle, bubble, stamp, impactLines, umbrellaAt, banner


def sky(c1, c2, y0=0, y1=H):
    gradient(c1, c2, y0, y1)


def sunDisc(x, y, r, col='#FFF6D8', glowCol='#FFE2A0', a=1.0, key='sun'):
    glow(x, y, r * 5, glowCol, .8 * a)
    boilSeed(key)
    paint(ellPts(x, y, r, r, 30), wash=col, washOp=int(255 * a), ink=None)


def band(pts, col, dk=None, key='band', inkK=.6, op=255):
    boilSeed(key)
    paint(pts, wash=col, washOp=op, fill=dk, fillOp=60 if dk else 0, bleed=.05, border=.5, ink=None)
    if inkK > 0:
        inkLine(pts[1:-2] if len(pts) > 4 else pts, inkK, mixCol(dk or col, INK, .45), 'ink', .4)


def dunes(y, col, dk, amp=40, n=5, ph=0.0, key='dune', inkK=.7, bottom=H + 300):
    pts = []
    for i in range(41):
        x = -100 + i * (W + 200) / 40
        yy = y - amp * (.6 * math.sin(i / 40 * n * math.pi + ph) + .4 * math.sin(i / 40 * n * 2.3 + ph * 1.7))
        pts.append([x, yy])
    pts = [[-100, bottom]] + pts + [[W + 100, bottom]]
    band(pts, col, dk, key, inkK)


def flatGround(y, col, dk, key='gnd', inkK=.8, bottom=H + 400):
    boilSeed(key)
    pts = [[-100, bottom], [-100, y]] + [[-100 + i * (W + 200) / 12, y + jit(2)] for i in range(1, 12)] + [[W + 100, y], [W + 100, bottom]]
    band(pts, col, dk, key, inkK)


def cracks(y0, y1, n, key='crk', col='#B98A45'):
    boilSeed(key)
    for i in range(n):
        x = 80 + hash1(i * 3.7) * (W - 160)
        y = lerp(y0, y1, hash1(i * 9.1))
        P = [[x, y]]
        for k in range(3):
            P.append([P[-1][0] + jit(40) + 30, P[-1][1] + jit(10)])
        inkLine(P, .5, col, 'inkfine', .3)


def sea(y, col, dk, t, key='sea', bottom=H + 600, waves=True, waveCol=None):
    boilSeed(key)
    flatRect(-100, y, W + 200, bottom - y, col)
    gradRect(-100, y, W + 200, 160, [mixCol(col, '#FFFFFF', .25), col])
    inkLine([[-100, y], [W + 100, y]], .7, mixCol(dk, INK, .3), 'ink', 0)
    if waves:
        wc = waveCol or mixCol(col, '#FFFFFF', .45)
        for i in range(26):
            yy = y + 18 + (i % 13) * ((bottom - y) / 13) ** .9 * 1.0
            if yy > bottom:
                continue
            x = (hash1(i * 5.1) * (W + 200) + t * (12 + 8 * hash1(i))) % (W + 300) - 150
            L = 30 + 50 * hash1(i * 2.2) * (1 + (yy - y) / 400)
            inkLine([[x, yy], [x + L * .5, yy - 4], [x + L, yy]], .5 + (yy - y) / 900, wc, 'inkfine', .5)


def chimney(x, y, w, h, col='#8C6E5A', dk='#5E4636', key='chm', bend=0.0, bands=True):
    """factory chimney standing on (x, y) going up h; bend curves it like kelp (radians at the top)"""
    boilSeed(key)
    n = 8
    L, R = [], []
    ang = 0
    px, py = x, y
    pts = []
    for i in range(n + 1):
        k = i / n
        ang = bend * k * k
        pts.append((px, py))
        px += math.sin(ang) * h / n
        py -= math.cos(ang) * h / n
    for i, (cx, cy) in enumerate(pts):
        k = i / n
        ww = lerp(w * .55, w * .42, k)
        a = bend * k * k
        nx, ny = math.cos(a), math.sin(a)
        L.append([cx - nx * ww, cy - ny * ww])
        R.append([cx + nx * ww, cy + ny * ww])
    poly = L + R[::-1]
    paint(poly, wash=col, fill=dk, fillOp=70, bleed=.05, border=.5, ink=INK, sw=.9)
    if bands:
        for k in (.72, .82):
            i = int(k * n)
            cx, cy = pts[i]
            a = bend * k * k
            ww = lerp(w * .55, w * .42, k)
            inkLine([[cx - math.cos(a) * ww, cy - math.sin(a) * ww], [cx + math.cos(a) * ww, cy + math.sin(a) * ww]], 1.4, '#C9B28F', 'ink', 0)
    return pts[-1]


def factory(x, y, w, h, col='#8A7466', dk='#5B4A40', key='fac'):
    boilSeed(key)
    teeth = 4
    pts = [[x, y], [x, y - h]]
    for i in range(teeth):
        x0 = x + i * w / teeth
        pts += [[x0 + w / teeth * .7, y - h - h * .25], [x0 + w / teeth, y - h]]
    pts += [[x + w, y]]
    paint(pts, wash=col, fill=dk, fillOp=60, bleed=.05, border=.5, ink=INK, sw=1.0)
    for i in range(int(w / 70)):
        wx = x + 25 + i * 70
        paint(rectPts(wx, y - h * .6, 26, 30, 1), wash=mixCol(dk, INK, .3), ink=None)


def board(x, y, w, h, col='#F5EEDD', frame='#6B5A4A', key='brd', legs=True, legH=200):
    boilSeed(key)
    if legs:
        for s in (-1, 1):
            paint(rectPts(x + s * w * .32 - 8, y + h / 2 - 10, 16, legH, 1), wash=frame, ink=INK, sw=.8)
    paint(rrPts(x - w / 2 - 12, y - h / 2 - 12, w + 24, h + 24, 10, 1.2), wash=frame, ink=INK, sw=1.2)
    paint(rrPts(x - w / 2, y - h / 2, w, h, 6, 1.0), wash=col, fill=mixCol(col, INK, .1), fillOp=40, ink=INK, sw=.8)


def heartBalloon(x, y, s, col='#E8475A', key='hb', string=None):
    boilSeed(key)
    if string:
        inkLine([[x, y + s * 1.05], [lerp(x, string[0], .5) + 10, lerp(y, string[1], .5)], string], .5, INK, 'inkfine', .6)
    paint(heartPts(x, y, s, 26), wash=col, fill=mixCol(col, INK, .25), fillOp=60, ink=INK, sw=.9, curv=.4)
    paint(ellPts(x - s * .35, y - s * .35, s * .18, s * .12, 10, 0, -.6), wash='#FFFFFF', washOp=180, ink=None)


def thunderCloud(x, y, s, key='tc', col='#8F93A3'):
    puff(x, y, s, col, key)
    boilSeed(key + 'f')
    for i, dx in enumerate((-1.2, 0, 1.2)):
        paint(ellPts(x + dx * s, y - .2 * s, .12 * s, .06 * s, 6), wash=INK, ink=None)


def zigzag(x0, y0, x1, y1, n=6, key='zz', col='#FFE24A', w=2.4):
    boilSeed(key)
    P = []
    for i in range(n + 1):
        k = i / n
        off = (18 if i % 2 else -18) if 0 < i < n else 0
        P.append([lerp(x0, x1, k) + off, lerp(y0, y1, k)])
    paint(ribbon(P, w * 10, w * 4), wash=col, ink=INK, sw=.8)


def tent(x, y, w, h, col='#B9875A', lit=1.0, key='tent'):
    boilSeed(key)
    paint([[x - w / 2, y], [x, y - h], [x + w / 2, y]], wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=.7)
    if lit > 0:
        paint([[x - w * .12, y], [x, y - h * .45], [x + w * .12, y]], wash='#FFD27A', washOp=int(255 * lit), ink=None)
        glow(x, y - h * .2, w * .7, '#FFB55A', .5 * lit)


def flagPole(x, y, h, flagY, wave, t, key='flag'):
    boilSeed(key)
    paint(rectPts(x - 5, y - h, 10, h, .5), wash='#8D8A86', ink=INK, sw=.7)
    paint(ellPts(x, y - h - 8, 10, 10, 10), wash='#D9B54A', ink=INK, sw=.6)
    fw, fh = 260, 170
    P = []
    for i in range(9):
        k = i / 8
        P.append([x + 6 + fw * k, flagY + math.sin(k * 5 - t * 7) * 10 * wave * k])
    for i in range(8, -1, -1):
        k = i / 8
        P.append([x + 6 + fw * k * (lerp(.25, 1, wave)), flagY + fh * lerp(1.0, 1, wave) + math.sin(k * 5 - t * 7 + .6) * 10 * wave * k])
    paint(P, wash='#C9733E', fill='#9B4F25', fillOp=70, ink=INK, sw=.9)
    if wave > .5:
        cx, cy = x + 6 + fw * .5, flagY + fh * .5 + math.sin(2.5 - t * 7) * 5
        newPlanet(cx, cy, 44, key + 'p')


def newPlanet(x, y, r, key='np', rot=0.0):
    """the New Earth emblem: an orange-brown planet with a ring"""
    boilSeed(key)
    push()
    translate(x, y)
    rotate(-.35)
    paint(ellPts(0, 0, r * 1.75, r * .42, 30), wash=None, ink='#F3D9A0', sw=r / 30)
    pop()
    paint(ellPts(x, y, r, r, 28), wash='#D7843F', fill='#A4572A', fillOp=80, bleed=.1, ink=INK, sw=r / 45)
    # continents slide with rot
    for i in range(3):
        a = rot + i * 2.1
        cx = x + math.cos(a) * r * .45
        if math.cos(a) > -.2:
            paint(ellPts(cx, y + (i - 1) * r * .35, r * .28 * max(.2, math.cos(a)), r * .16, 10), wash='#F0B46A', ink=None)
    push()
    translate(x, y)
    rotate(-.35)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(-r * 2, 0, r * 4, r * 2))
    paint(ellPts(0, 0, r * 1.75, r * .42, 30), wash=None, ink='#F3D9A0', sw=r / 30)
    G.c.restore()
    pop()


def speaker(x, y, s, ang=0.0, key='spk'):
    boilSeed(key)
    push()
    translate(x, y)
    rotate(ang)
    paint(rectPts(-s * .5, -s * .4, s * .55, s * .8, 1), wash='#77716A', ink=INK, sw=.8)
    paint([[0, -s * .3], [s * 1.5, -s * .85], [s * 1.5, s * .85], [0, s * .3]], wash='#D9D3C6', fill='#9A9488', fillOp=80, ink=INK, sw=.9)
    paint(ellPts(s * 1.5, 0, s * .28, s * .85, 18), wash='#3A3640', ink=INK, sw=.8)
    pop()


def soundLines(x, y, ang, r0, r1, n, key='sl', col=INK, sw=1.0):
    boilSeed(key)
    for i in range(n):
        a = ang + (i - (n - 1) / 2) * .22
        inkLine([[x + math.cos(a) * r0, y + math.sin(a) * r0], [x + math.cos(a) * r1, y + math.sin(a) * r1]], sw, col, 'ink', 0)
    for j in range(3):
        rr = lerp(r0, r1, (j + 1) / 4)
        P = [[x + math.cos(ang + d) * rr, y + math.sin(ang + d) * rr] for d in (-.45, -.2, 0, .2, .45)]
        inkLine(P, sw * .8, col, 'ink', .6)


def glyph(x, y, s, kind, key='gl', col=INK):
    boilSeed(key + str(kind))
    if kind == 0:
        inkLine([[x - s, y + s * .6], [x, y - s * .7], [x + s, y + s * .6], [x - s, y + s * .6]], .9, col, 'ink', 0)
    elif kind == 1:
        paint(ellPts(x, y, s * .8, s * .8, 16), ink=col, sw=.9)
        paint(ellPts(x, y, s * .25, s * .25, 8), wash=col, ink=None)
    elif kind == 2:
        inkLine([[x - s, y], [x - s * .5, y - s * .6], [x, y], [x + s * .5, y + s * .6], [x + s, y]], .9, col, 'ink', .6)
    elif kind == 3:
        inkLine([[x - s * .7, y - s * .7], [x + s * .7, y + s * .7]], 1.0, col, 'ink', 0)
        inkLine([[x + s * .7, y - s * .7], [x - s * .7, y + s * .7]], 1.0, col, 'ink', 0)
    elif kind == 4:
        inkLine([[x, y - s * .8], [x + s * .8, y], [x, y + s * .8], [x - s * .8, y], [x, y - s * .8]], .9, col, 'ink', 0)
    else:
        inkLine([[x - s, y + s * .4], [x - s * .3, y - s * .5], [x + s * .2, y + s * .3], [x + s, y - s * .6]], .9, col, 'ink', .3)


def glyphBubble(x, y, kinds, s=26, k=1.0, tail=None, key='gb', col='#FFFFFF'):
    p = backOut(k)
    if p < .02:
        return
    w = len(kinds) * s * 2.3 + s * 1.2
    h = s * 3.0
    push()
    translate(x, y)
    scale(p)
    boilSeed(key)
    if tail:
        tx, ty = (tail[0] - x) / p, (tail[1] - y) / p
        bx = clamp(tx, -w * .3, w * .3)
        paint([[bx - s * .5, h * .3], [bx + s * .5, h * .3], [tx * .6 + bx * .4, ty * .6]], wash=col, ink=INK, sw=.9)
    paint(rrPts(-w / 2, -h / 2, w, h, h * .45, 1.5), wash=col, ink=INK, sw=1.0)
    for i, kd in enumerate(kinds):
        glyph(-w / 2 + s * 1.75 + i * s * 2.3, 0, s * .75, kd, key)
    pop()


def medal(x, y, s, glint=0.0, key='med'):
    boilSeed(key)
    paint([[x - s * .5, y - s * 1.6], [x + s * .5, y - s * 1.6], [x + s * .25, y - s * .6], [x - s * .25, y - s * .6]], wash='#C8463C', ink=INK, sw=.5)
    paint(ellPts(x, y, s * .7, s * .7, 14), wash='#E7B93E', fill='#B8872A', fillOp=70, ink=INK, sw=.6)
    paint(starPts(x, y, s * .4, .45, 5), wash='#FFF0B0', ink=None)
    if glint > 0:
        glow(x, y, s * 6, '#FFF2B0', glint)
        paint(starPts(x + s * .5, y - s * .5, s * 2.2 * glint, .18, 4), wash='#FFFFFF', washOp=int(255 * glint), ink=None)


def raft(x, y, s, key='raft', tilt=0.0):
    boilSeed(key)
    push()
    translate(x, y)
    rotate(tilt)
    for i in range(6):
        px = -s * 3 + i * s
        paint(rrPts(px, -s * .35, s * .95, s * .7, s * .3, 1), wash=['#A57A4E', '#B88A5C'][i % 2], fill='#7A5434', fillOp=60, ink=INK, sw=.7)
    for px in (-s * 2.2, s * 2.0):
        inkLine([[px, -s * .35], [px + s * .2, s * .35]], .8, '#5B3D25', 'ink', 0)
    pop()


def palm(x, y, s, key='palm', lean=.15, t=0.0):
    boilSeed(key)
    P = [[x, y]]
    for i in range(1, 7):
        k = i / 6
        P.append([x + lean * s * 6 * k * k, y - s * 6 * k])
    paint(ribbon(P, s * .55, s * .35), wash='#A07A50', fill='#7A5834', fillOp=60, ink=INK, sw=.8)
    tx, ty = P[-1]
    for j in range(6):
        a = -math.pi / 2 + (j - 2.5) * .62 + math.sin(t * 2 + j) * .04
        L = s * (3.0 + .4 * (j % 2))
        Q = [[tx, ty], [tx + math.cos(a) * L * .5, ty + math.sin(a) * L * .5 - s * .4], [tx + math.cos(a) * L, ty + math.sin(a) * L + s * .6]]
        paint(ribbon(Q, s * .2, s * .9), wash='#4FA65A', fill='#2F7A3F', fillOp=60, ink=INK, sw=.7)
    for k in range(2):
        paint(ellPts(tx + (k - .5) * s * .5, ty + s * .35, s * .3, s * .3, 10), wash='#7A5530', ink=INK, sw=.5)


def gull(x, y, s, flap, key='gull'):
    boilSeed(key)
    a = .5 + .35 * math.sin(flap)
    inkLine([[x - s, y - s * a], [x - s * .4, y - s * .1], [x, y + s * .15], [x + s * .4, y - s * .1], [x + s, y - s * a]], .9, '#FFFFFF', 'ink', .6)


def drops(x, y, s, k, n=8, key='drp', col='#BFF0F5'):
    """splash: drops flying out; k = 0..1 age fraction"""
    if k <= 0 or k >= 1:
        return
    boilSeed(key)
    for i in range(n):
        a = -math.pi * (.15 + .7 * i / (n - 1))
        r = s * (1 + 2.6 * k) * (.7 + .5 * hash1(i))
        px, py = x + math.cos(a) * r, y + math.sin(a) * r + s * 3 * k * k
        paint(ellPts(px, py, s * .22 * (1 - k * .5), s * .3 * (1 - k * .5), 8), wash=col, ink=INK, sw=.4)


def starField(t, seed, n, x0, y0, x1, y1, on=1.0, big=None, r=3.0):
    """painted stars; big = list of (index, intensity) to flare"""
    if on <= 0:
        return
    for i in range(n):
        h1, h2, h3 = hash1(seed + i * 1.37), hash1(seed * 2 + i * 7.1), hash1(seed * 3 + i * 3.3)
        x, y = lerp(x0, x1, h1), lerp(y0, y1, h2 ** 1.2)
        tw = .65 + .35 * math.sin(t * (1.5 + 3 * h3) + i)
        rr = r * (.4 + 1.1 * h3 ** 3) * tw
        G.c.drawCircle(x, y, rr, skia.Paint(AntiAlias=True, Color=skcol('#FFF7DE', on * (.55 + .45 * tw))))
    for (i, k) in (big or []):
        if k <= 0:
            continue
        h1, h2 = hash1(seed + i * 1.37), hash1(seed * 2 + i * 7.1)
        x, y = lerp(x0, x1, h1), lerp(y0, y1, h2 ** 1.2)
        glow(x, y, 60 * k, '#FFF3C0', k)
        paint(starPts(x, y, 26 * k, .14, 4), wash='#FFFFFF', washOp=int(255 * min(1, k)), ink=None)


def milkyWay(on=1.0):
    if on <= 0:
        return
    push()
    translate(W / 2, H * .35)
    rotate(-.45)
    for i in range(7):
        a = (.035 - i * .003) * on
        boilSeed(f'mw{i}')
        P = []
        for j in range(41):
            x = -1500 + j * 75
            P.append([x, -(190 - i * 22) * (1 + .35 * math.sin(j * .7 + i)) + 30 * math.sin(j * .31)])
        for j in range(40, -1, -1):
            x = -1500 + j * 75
            P.append([x, (170 - i * 20) * (1 + .3 * math.sin(j * .5 + i * 2)) + 30 * math.sin(j * .31)])
        paint(P, wash=['#5E5AA8', '#6E68B4', '#8A80C4', '#A498D2', '#C2B4E0', '#DDD0EC', '#F2E8F4'][i], washOp=int(255 * a * 4), ink=None)
    for j in range(260):
        x = (hash1(j * 1.9) - .5) * 2900
        y = (hash1(j * 4.3) - .5) * 2 * (60 + 140 * hash1(j * 7.7)) * (.5 + .5 * abs(math.sin(x * .002)))
        G.c.drawCircle(x, y, .8 + 1.6 * hash1(j * 2.9) ** 3, skia.Paint(AntiAlias=True, Color=skcol('#FFF7E8', on * (.4 + .5 * hash1(j)))))
    pop()


def ecgLine(x0, x1, y, t, k0, col='#3FD17A', key='ecg'):
    """flat line with one blip that has already passed (k0 = beat time of the blip)"""
    boilSeed(key)
    P = []
    bx = lerp(x0, x1, clamp((t - k0) / .6)) if t >= k0 else -1e9
    n = 60
    for i in range(n + 1):
        x = lerp(x0, x1, i / n)
        d = x - bx
        yy = y
        if t >= k0 and -60 < d < 60 and bx < x1:
            yy = y - (math.exp(-((d + 10) / 12) ** 2) * 70 - math.exp(-((d - 18) / 10) ** 2) * 30)
        P.append([x, yy])
    inkLine(P, 1.3, col, 'ink', 0)


def watermelon(x, y, s, key='wm', rot=0.0):
    boilSeed(key)
    push()
    translate(x, y)
    rotate(rot)
    paint([[-s, 0], [s, 0], [0, -s * 1.3]], wash='#EB5A5A', ink=INK, sw=.7)
    paint(ribbon([[-s, 0], [0, s * .12], [s, 0]], s * .25), wash='#4D9A4E', ink=INK, sw=.6)
    for i in range(4):
        paint(ellPts((i - 1.5) * s * .35, -s * .45 - (i % 2) * s * .2, s * .06, s * .09, 6), wash=INK, ink=None)
    pop()


def kite(x, y, s, key='kite', t=0.0):
    boilSeed(key)
    paint([[x, y - s], [x + s * .7, y], [x, y + s * 1.2], [x - s * .7, y]], wash='#F2C14E', fill='#E0563E', fillOp=120, ink=INK, sw=.9)
    inkLine([[x, y - s], [x, y + s * 1.2]], .5, INK, 'inkfine', 0)
    inkLine([[x - s * .7, y], [x + s * .7, y]], .5, INK, 'inkfine', 0)
    P = [[x, y + s * 1.2]]
    for i in range(1, 6):
        P.append([x + math.sin(t * 6 + i) * s * .3, y + s * 1.2 + i * s * .4])
    inkLine(P, .5, INK, 'inkfine', .6)
    for i in (2, 4):
        paint(ellPts(P[i][0], P[i][1], s * .15, s * .08, 6), wash='#E0563E', ink=None)


def firework(x, y, r, k, col, key='fw'):
    if k <= 0 or k >= 1.2:
        return
    boilSeed(key)
    a = 1 - seg(k, .7, 1.2)
    rr = r * easeOut(clamp(k / .7))
    for i in range(16):
        ang = i / 16 * TAU
        x1, y1 = x + math.cos(ang) * rr, y + math.sin(ang) * rr + 40 * k * k
        x0, y0 = x + math.cos(ang) * rr * .55, y + math.sin(ang) * rr * .55
        inkLine([[x0, y0], [x1, y1]], 1.2 * a, col, 'ink', 0)
        G.c.drawCircle(x1, y1, 5 * a, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', a)))
    glow(x, y, r * 1.2, col, .5 * a)


def polaroid(cx, cy, w, h, rot, draw, key='pol'):
    """white-bordered memory card; draw() paints inside a clip in the card's own coords (0..w, 0..h)"""
    boilSeed(key)
    push()
    translate(cx, cy)
    rotate(rot)
    b = 26
    paint(rectPts(-w / 2 - b, -h / 2 - b, w + 2 * b, h + 2 * b + 50, 1), wash='#FFFDF6', fill='#E8E0CC', fillOp=40, ink=INK, sw=.9)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h))
    translate(-w / 2, -h / 2)
    draw(w, h)
    G.c.restore()
    pop()
