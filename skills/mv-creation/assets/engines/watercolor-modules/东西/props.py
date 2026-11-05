# props.py: sets, props and graphic devices for 疑心病 (watercolour + ink, bright pastel palette).
import math
from eng import *
from clawd import *

C = dict(pinkA='#F7C6D2', pinkB='#F3AFC2', peachA='#FAD7B5', peachB='#F6C08F', yelA='#FBE7A1', yelB='#F7D36E',
         mintA='#CDEFE0', mintB='#A9E2CB', skyA='#BFE3F5', skyB='#9CD0EE', lavA='#D9CCF2', lavB='#C3B0EA',
         grass='#9ED27A', grassDk='#79B45B', heart='#E8476E', heartLt='#F7A1B6', gold='#F2C53D', red='#D8394E',
         nightA='#2A2D6E', nightB='#5B3F8C', asphalt='#3A3550', cream=PAL['cream'], yiyun='#B9A8D8', yiyunDk='#8E79BC')


# ---------------- backgrounds ----------------
def sunburst(cx, cy, c1, c2, n=18, rot=0.0, R=2600):
    flatRect(-80, -80, W + 160, H + 160, c1)
    p = skia.Path()
    for i in range(n):
        a0 = rot + i * TAU / n
        a1 = a0 + TAU / n * .5
        p.moveTo(cx, cy)
        p.lineTo(cx + math.cos(a0) * R, cy + math.sin(a0) * R)
        p.lineTo(cx + math.cos(a1) * R, cy + math.sin(a1) * R)
        p.close()
    G.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol(c2)))
    glow(cx, cy, 520, '#FFFFFF', .35)


def stripes(c1, c2, w=70, x0=-80):
    flatRect(-80, -80, W + 160, H + 160, c1)
    x = x0
    while x < W + 80:
        flatRect(x, -80, w / 2, H + 160, c2)
        x += w


def gradient(c1, c2, y0=0, y1=H):
    gradRect(-80, y0 - 80, W + 160, (y1 - y0) + 160, [c1, c2])


def groundBand(y, col, dk, key='ground', wavy=0):
    boilSeed(key)
    pts = [[-80, y]]
    for i in range(13):
        x = -80 + i * (W + 160) / 12
        pts.append([x, y + jit(3) + wavy * math.sin(i * 1.3)])
    pts += [[W + 80, H + 80], [-80, H + 80]]
    paint(pts, wash=col, ink=None)
    inkLine(pts[1:14], 1.1, mixCol(dk, INK, .35), 'ink', .3)


def puff(x, y, s, col=None, key='puff', ink=True, a=1.0):
    """a fluffy painted cloud, about 5s wide"""
    boilSeed(key)
    col = col or PAL['cream']
    c = []
    for i in range(36):
        ang = i / 36 * TAU
        up = math.sin(ang) < 0
        r = 1 + .32 * abs(math.sin(ang * 3)) ** .6 if up else 1
        c.append([x + math.cos(ang) * 2.6 * s * (r * .95 if up else 1), y + math.sin(ang) * (1.25 if up else .55) * s * r])
    paint(c, wash=col, washOp=255 * a, ink=INK if ink else None, sw=clamp(s / 22, .5, 1.6), curv=.4)


def heartCloud(x, y, s, key='hc'):
    boilSeed(key)
    pts = heartPts(x, y, s, 30)
    pts = [[px + jit(s * .03), py + jit(s * .03)] for px, py in pts]
    paint(pts, wash='#FFFFFF', fill=C['pinkA'], fillOp=70, ink=INK, sw=1.1, curv=.5)


def qCloud(x, y, s, key='qc'):
    """a cloud shaped like a question mark"""
    boilSeed(key)
    P = [[-1, -1.3], [-.55, -2.15], [.35, -2.3], [1, -1.6], [.7, -.75], [.05, -.3], [0, .4]]
    paint(ribbon([[x + a * s, y + b * s] for a, b in P], .9 * s, .7 * s), wash='#FFFFFF', fill=C['lavA'], fillOp=80, ink=INK, sw=1.1)
    paint(ellPts(x, y + 1.35 * s, .48 * s, .48 * s, 14), wash='#FFFFFF', ink=INK, sw=1.1)


def sparkle(x, y, r, col=None, a=1.0):
    col = col or PAL['cream']
    paint(starPts(x, y, r, .3, 4), wash=col, washOp=255 * a, ink=None)


def sparkles(t, seed, n, x0, y0, x1, y1, r=10, col=None):
    for i in range(n):
        h = hash1(seed * 31 + i)
        ph = frac(t * (.6 + .5 * hash1(i + seed)) + h)
        k = math.sin(ph * math.pi)
        if k < .05:
            continue
        sparkle(lerp(x0, x1, hash1(seed + i * 7.3)), lerp(y0, y1, hash1(seed * 3 + i * 1.9)), r * (.5 + .5 * k), col, k)


def floatHearts(t, seed, n, x0, y0, x1, y1, s=14):
    for i in range(n):
        ph = frac(t * .35 + hash1(seed + i * 3.1))
        a = math.sin(ph * math.pi)
        if a < .08:
            continue
        x = lerp(x0, x1, hash1(seed * 5 + i * 2.7)) + math.sin(t * 2 + i) * 20
        y = lerp(y1, y0, ph)
        boilSeed(f'fh{seed}{i}')
        paint(heartPts(x, y, s * (.6 + .5 * a), 18), wash=C['heart'] if i % 2 else C['heartLt'], ink=INK, sw=.6)


# ---------------- the suspicion clouds (疑云) ----------------
def yiyun(x, y, s, t, seed=0, k=1.0, mood='sus', col=None):
    """a little violet cloud creature with a question mark on its head. k = pop-in 0..1"""
    p = backOut(k)
    if p < .02:
        return
    bob = math.sin(t * 3 + seed) * s * .12
    push()
    translate(x, y + bob)
    scale(p)
    boilSeed(f'yy{seed}')
    col = col or C['yiyun']
    c = []
    for i in range(30):
        a = i / 30 * TAU
        up = math.sin(a) < 0
        r = 1 + .3 * abs(math.sin(a * 2.5)) ** .7 if up else 1
        c.append([math.cos(a) * 1.5 * s * (r * .95 if up else 1), math.sin(a) * (1.0 if up else .62) * s * r])
    paint(c, wash=col, fill=C['yiyunDk'], fillOp=60, ink=INK, sw=clamp(s / 30, .5, 1.4), curv=.4, lite=True)
    # eyes
    ex = .38 * s
    if mood == 'sus':
        for sx in (-1, 1):
            paint(rectPts(sx * ex - .16 * s, .02 * s, .32 * s, .14 * s), wash=INK, ink=None)
    elif mood == 'happy':
        for sx in (-1, 1):
            inkLine([[sx * ex - .16 * s, .15 * s], [sx * ex, 0], [sx * ex + .16 * s, .15 * s]], clamp(s / 30, .4, 1.2), INK, 'ink', .3)
    else:
        for sx in (-1, 1):
            paint(ellPts(sx * ex, .08 * s, .09 * s, .13 * s, 8), wash=INK, ink=None)
    # question mark on top
    Q = [[-.28, -1.15], [-.15, -1.42], [.12, -1.48], [.3, -1.28], [.2, -1.05], [.02, -.92], [0, -.75]]
    inkLine([[a * s, b * s] for a, b in Q], clamp(s / 22, .6, 2.2), mixCol(C['yiyunDk'], INK, .4), 'ink', .5)
    paint(ellPts(0, -.6 * s, .07 * s, .07 * s, 8), wash=mixCol(C['yiyunDk'], INK, .4), ink=None)
    pop()


# ---------------- text devices ----------------
def bubble(x, y, txt, size=44, tail=None, k=1.0, col='#FFFFFF', tcol=INK, key='bub', minw=0):
    """speech bubble centred at (x, y); tail = (tx, ty) point it comes from"""
    p = backOut(k)
    if p < .02:
        return
    w = max(minw, textW(txt, size) + size * 1.1)
    h = size * 1.75
    push()
    translate(x, y)
    scale(p)
    boilSeed(key)
    if tail:
        tx, ty = (tail[0] - x) / p, (tail[1] - y) / p
        bx = clamp(tx, -w * .3, w * .3)
        paint([[bx - size * .35, h * .3], [bx + size * .35, h * .3], [tx * .6 + bx * .4, ty * .6]], wash=col, ink=INK, sw=.9)
    paint(rrPts(-w / 2, -h / 2, w, h, h * .45, 1.5), wash=col, ink=INK, sw=1.0)
    text(txt, 0, 0, size, tcol, shadow=False)
    pop()


def stamp(txt, x, y, size, col, age, rot=-.1, life=None, stroke=INK):
    """big pop-in lettering (comic SFX); age = seconds since it hit (starts ~1 frame early so the hit frame shows it)"""
    age += .035
    if age < 0:
        return
    k = backOut(clamp(age / .16))
    a = 1.0
    if life is not None:
        a = 1 - seg(age, life - .2, life)
    text(txt, x, y, size, col, stroke=stroke, strokeW=size * .16, shadow=True, a=a,
         rot=rot + math.sin(age * 22) * .05 * math.exp(-age * 5), sc=k)


def impactLines(x, y, r0, r1, n, t, col=INK, key='imp', sw=1.0):
    boilSeed(key)
    for i in range(n):
        a = i / n * TAU + jit(.15)
        inkLine([[x + math.cos(a) * r0, y + math.sin(a) * r0], [x + math.cos(a) * r1, y + math.sin(a) * r1]], sw, col, 'ink', 0)


# ---------------- props ----------------
def tree(x, y, s, key='tree', col='#7CC36B'):
    boilSeed(key)
    paint(rectPts(x - .35 * s, y - 2.6 * s, .7 * s, 2.6 * s, s * .05), wash='#9B6B45', ink=INK, sw=1)
    c = []
    for i in range(30):
        a = i / 30 * TAU
        r = 1 + .14 * abs(math.sin(a * 3.5))
        c.append([x + math.cos(a) * 1.9 * s * r, y - 3.6 * s + math.sin(a) * 1.55 * s * r])
    paint(c, wash=col, fill=mixCol(col, '#2E6B3A', .4), fillOp=70, ink=INK, sw=1.1, curv=.3)
    for i in range(4):
        paint(ellPts(x + (hash1(i + 3) - .5) * 2.6 * s, y - 3.6 * s + (hash1(i + 9) - .5) * 1.8 * s, .16 * s, .16 * s, 8), wash='#F59AB0', ink=None)


def bush(x, y, s, key='bush', col='#86C96E'):
    boilSeed(key)
    c = []
    for i in range(34):
        a = math.pi + i / 33 * math.pi
        r = 1 + .18 * abs(math.sin(a * 4))
        c.append([x + math.cos(a) * 2.2 * s * r, y + math.sin(a) * 1.5 * s * r])
    paint(c, wash=col, fill=mixCol(col, '#2E6B3A', .35), fillOp=60, ink=INK, sw=1.1, curv=.25)


def bench(x, y, s, key='bench', col='#C98B5A'):
    boilSeed(key)
    for lx in (-2.2, 2.0):
        paint(rectPts(x + lx * s, y - 1.3 * s, .25 * s, 1.3 * s), wash=mixCol(col, INK, .3), ink=INK, sw=.8)
    paint(rectPts(x - 2.7 * s, y - 1.45 * s, 5.4 * s, .3 * s), wash=col, ink=INK, sw=.9)
    paint(rectPts(x - 2.7 * s, y - 2.6 * s, 5.4 * s, .28 * s), wash=col, ink=INK, sw=.9)
    paint(rectPts(x - 2.7 * s, y - 2.15 * s, 5.4 * s, .28 * s), wash=col, ink=INK, sw=.9)


def lamp(x, y, s, on=1.0, key='lamp', col='#4A4760', head='#FFE7A0'):
    boilSeed(key)
    paint(rectPts(x - .12 * s, y - 6 * s, .24 * s, 6 * s, s * .03), wash=col, ink=INK, sw=.9)
    paint(rectPts(x - .4 * s, y - .35 * s, .8 * s, .35 * s), wash=col, ink=INK, sw=.8)
    paint([[x - .7 * s, y - 6.0 * s], [x + .7 * s, y - 6.0 * s], [x + .4 * s, y - 6.8 * s], [x - .4 * s, y - 6.8 * s]], wash=col, ink=INK, sw=.9)
    paint(ellPts(x, y - 5.75 * s, .5 * s, .32 * s, 12), wash=mixCol('#77738A', head, on), ink=INK, sw=.7)
    if on > .02:
        glow(x, y - 5.6 * s, 3.2 * s, '#FFD27A', on)


def trashcan(x, y, s, key='trash'):
    boilSeed(key)
    paint([[x - 1 * s, y - 2.4 * s], [x + 1 * s, y - 2.4 * s], [x + .8 * s, y], [x - .8 * s, y]], wash='#7FA9C9', ink=INK, sw=1)
    for i in (-.45, 0, .45):
        inkLine([[x + i * s, y - 2.1 * s], [x + i * .85 * s, y - .25 * s]], .6, INK, 'inkfine', 0)
    paint(rrPts(x - 1.15 * s, y - 2.75 * s, 2.3 * s, .4 * s, .15 * s), wash='#5F88AA', ink=INK, sw=1)


def mailbox(x, y, s, key='mail'):
    boilSeed(key)
    paint(rectPts(x - .15 * s, y - 2 * s, .3 * s, 2 * s), wash='#5B5470', ink=INK, sw=.8)
    d = [[x - 1 * s, y - 2 * s]]
    for i in range(9):
        a = math.pi + i / 8 * math.pi
        d.append([x + math.cos(a) * 1 * s, y - 3.2 * s + math.sin(a) * .9 * s])
    d.append([x + 1 * s, y - 2 * s])
    paint(d, wash='#E25B4F', ink=INK, sw=1)
    paint(rectPts(x - .55 * s, y - 3.05 * s, 1.1 * s, .18 * s), wash=INK, ink=None)


def phoneHook(glowK=1.0):
    def h(u, sw):
        paint(rrPts(-.2 * u, -1.1 * u, 1.3 * u, 2.1 * u, .25 * u), wash='#3D3A52', ink=INK, sw=sw * .7)
        paint(rrPts(-.05 * u, -.9 * u, 1.0 * u, 1.6 * u, .15 * u), wash=mixCol('#9FD8F0', '#FFFFFF', .3 * glowK), ink=None)
        if glowK > .05:
            glow(.45 * u, -.1 * u, 2.2 * u, '#BDEBFF', .5 * glowK)
    return h


def magnifierHook(big=1.0):
    def h(u, sw):
        r = 1.25 * u * big
        paint(rectPts(-.15 * u, -.25 * u, 1.5 * u, .5 * u), wash='#7A4E33', ink=INK, sw=sw * .7)
        cx = 1.35 * u + r
        paint(ellPts(cx, 0, r, r, 24), wash='#DDF2FF', washOp=150, ink=None)
        paint(ellPts(cx - r * .3, -r * .35, r * .25, r * .14, 10, 0, -.6), wash='#FFFFFF', washOp=200, ink=None)
        paint(ellPts(cx, 0, r, r, 24), ink='#C99A2E', sw=sw * 1.5)
    return h


def umbrellaAt(x, y, r, col='#6FC3C9', k=1.0, key='umb', tilt=0.0, handle=True, dots=True):
    """umbrella whose shaft bottom is at (x, y); k = how open (0..1)"""
    boilSeed(key)
    push()
    translate(x, y)
    rotate(tilt)
    H_ = 1.75 * r
    if handle:
        inkLine([[0, 0], [0, -H_]], 1.4, INK, 'ink', 0)
        inkLine([[0, 0], [0, .25 * r], [-.25 * r, .3 * r]], 1.3, INK, 'ink', .5)
    w = r * lerp(.25, 1, k)
    hh = r * lerp(1.1, .66, k)
    top = -H_
    pts = [[-w, top + hh]]
    for i in range(1, 16):
        a = math.pi + i / 16 * math.pi
        pts.append([math.cos(a) * w, top + hh + math.sin(a) * hh])
    pts.append([w, top + hh])
    for i in range(4, 0, -1):
        x0 = -w + (i) * w * 2 / 4
        x1 = -w + (i - 1) * w * 2 / 4
        pts.append([(x0 + x1) / 2, top + hh - .16 * r * k])
        pts.append([x1, top + hh])
    paint(pts, wash=col, fill=mixCol(col, INK, .25), fillOp=50, ink=INK, sw=1.1)
    if dots and k > .5:
        for i in range(5):
            dx = (-.7 + i * .35) * w
            paint(ellPts(dx, top + hh * .55 - abs(dx) * .1, .07 * r, .07 * r, 8), wash='#FFFFFF', ink=None)
    pop()


def scaleProp(x, y, s, needle, key='scale', body='#F4F0E8', maxMark=True):
    """a bathroom scale (top surface at y - .5s). needle 0..1 (1 = max)"""
    boilSeed(key)
    paint(rrPts(x - 4.4 * s, y - .9 * s, 8.8 * s, 1.1 * s, .35 * s), wash=mixCol(body, INK, .25), ink=INK, sw=1.1)
    paint(rrPts(x - 4.6 * s, y - 1.25 * s, 9.2 * s, .6 * s, .3 * s), wash=body, ink=INK, sw=1.1)
    # dial on a stand in front
    dx, dy, r = x, y + 1.7 * s, 1.55 * s
    paint(ellPts(dx, dy, r * 1.12, r * 1.12, 26), wash='#E9E3D6', ink=INK, sw=1.1)
    paint(ellPts(dx, dy, r, r, 26), wash='#FFFDF6', ink=None)
    for i in range(9):
        a = math.pi * (1.1 + .8 * i / 8)
        c = C['red'] if i >= 7 else INK
        inkLine([[dx + math.cos(a) * r * .72, dy + math.sin(a) * r * .72], [dx + math.cos(a) * r * .92, dy + math.sin(a) * r * .92]], .8, c, 'inkfine', 0)
    a = math.pi * (1.1 + .8 * clamp(needle, 0, 1.15))
    inkLine([[dx, dy], [dx + math.cos(a) * r * .85, dy + math.sin(a) * r * .85]], 1.6, C['red'], 'ink', 0)
    paint(ellPts(dx, dy, .16 * s, .16 * s, 8), wash=INK, ink=None)


def seesaw(x, y, L, ang, key='ss', col='#F2A65A'):
    """pivot base at (x, y) on the ground; plank half-length L; returns seat points (left, right)"""
    boilSeed(key)
    ph = L * .26
    paint([[x - ph * .55, y], [x + ph * .55, y], [x, y - ph]], wash='#7FA9C9', ink=INK, sw=1.1)
    cx, cy = x, y - ph
    ca, sa = math.cos(ang), math.sin(ang)
    th = L * .06

    def P(px, py):
        return [cx + px * ca - py * sa, cy + px * sa + py * ca]
    paint([P(-L, -th), P(L, -th), P(L, th * .4), P(-L, th * .4)], wash=col, ink=INK, sw=1.2)
    for sx in (-1, 1):
        paint([P(sx * L * .78 - th * .3, -th), P(sx * L * .78 + th * .3, -th), P(sx * L * .78 + th * .3, -th * 3.2), P(sx * L * .78 - th * .3, -th * 3.2)],
              wash=mixCol(col, INK, .25), ink=INK, sw=.8)
    return P(-L * .55, -th), P(L * .55, -th)


def stopwatch(x, y, r, ang, key='sw', face='#FFFDF6'):
    boilSeed(key)
    paint(rectPts(x - .18 * r, y - 1.35 * r, .36 * r, .3 * r), wash='#C9C2B4', ink=INK, sw=1)
    paint(ellPts(x, y - 1.42 * r, .3 * r, .14 * r, 10), wash='#C9C2B4', ink=INK, sw=.8)
    paint(ellPts(x, y, r * 1.08, r * 1.08, 30), wash='#F2C53D', ink=INK, sw=1.3)
    paint(ellPts(x, y, r * .9, r * .9, 30), wash=face, ink=None)
    for i in range(12):
        a = i / 12 * TAU
        inkLine([[x + math.cos(a) * r * .72, y + math.sin(a) * r * .72], [x + math.cos(a) * r * .84, y + math.sin(a) * r * .84]], 1 if i % 3 else 1.6, INK, 'inkfine', 0)
    inkLine([[x, y], [x + math.cos(ang - math.pi / 2) * r * .78, y + math.sin(ang - math.pi / 2) * r * .78]], 1.6, C['red'], 'ink', 0)
    paint(ellPts(x, y, .08 * r, .08 * r, 8), wash=INK, ink=None)


def banner(x, y, w, h, col='#E8476E', dk='#B8324F', key='ban'):
    """a ribbon banner centred at (x, y) with folded tails"""
    boilSeed(key)
    for s in (-1, 1):
        ex = x + s * w / 2
        paint([[ex - s * h * .3, y - h * .2], [ex + s * h * 1.1, y - h * .2], [ex + s * h * .7, y + h * .35], [ex + s * h * 1.1, y + h * .9], [ex - s * h * .3, y + h * .9]], wash=dk, ink=INK, sw=1.2)
    pts = []
    for i in range(13):
        k = i / 12
        pts.append([x - w / 2 + w * k, y - h / 2 - math.sin(k * math.pi) * h * .18])
    for i in range(12, -1, -1):
        k = i / 12
        pts.append([x - w / 2 + w * k, y + h / 2 - math.sin(k * math.pi) * h * .18])
    paint(pts, wash=col, fill=dk, fillOp=40, ink=INK, sw=1.4)


def netHook(swing=0.0):
    def h(u, sw):
        push()
        rotate(swing)
        inkLine([[0, 0], [4.2 * u, 0]], sw * 1.3, '#9B6B45', 'ink', 0)
        cx = 5.4 * u
        paint(ellPts(cx, 0, 1.2 * u, 1.2 * u, 20), wash='#FFFFFF', washOp=90, ink=INK, sw=sw * .8)
        for i in range(-2, 3):
            inkLine([[cx + i * .45 * u, -1.1 * u], [cx + i * .3 * u, 1.1 * u]], sw * .35, INK, 'inkfine', 0)
            inkLine([[cx - 1.1 * u, i * .45 * u], [cx + 1.1 * u, i * .3 * u]], sw * .35, INK, 'inkfine', 0)
        pop()
    return h


def hills(base_y, cols, t=0, key='hills'):
    """layered rolling hills, back to front"""
    for j, col in enumerate(cols):
        boilSeed(f'{key}{j}')
        y0 = base_y + j * 70
        pts = [[-80, H + 80]]
        for i in range(25):
            x = -80 + i * (W + 160) / 24
            pts.append([x, y0 - 60 * math.sin(i * .55 + j * 1.7) ** 2 - 25 * math.sin(i * 1.3 + j)])
        pts.append([W + 80, H + 80])
        paint(pts, wash=col, ink=INK, sw=1.0, curv=.4)


def city(t, lights=1.0, key='city', col='#3B3770', win='#FFD98A'):
    """night city silhouette with lit windows"""
    x = -60
    i = 0
    while x < W + 60:
        boilSeed(f'{key}{i}')
        w = 120 + 90 * hash1(i * 3.1)
        h = 220 + 260 * hash1(i * 7.7)
        paint(rectPts(x, 640 - h, w, h + 40, 2), wash=mixCol(col, '#5B4F9A', hash1(i) * .5), ink=INK, sw=.8)
        for r in range(int(h // 55)):
            for c_ in range(int(w // 42)):
                on = hash1(i * 13 + r * 5 + c_) < .45 * lights
                if on:
                    flatRect(x + 16 + c_ * 42, 640 - h + 22 + r * 55, 18, 24, win, .9)
        x += w + 14
        i += 1


def neon(x, y, w, h, col, on=1.0, key='neon'):
    boilSeed(key)
    paint(rrPts(x, y, w, h, 14), wash='#2A2440', ink=INK, sw=1)
    paint(rrPts(x + 10, y + 10, w - 20, h - 20, 10), ink=mixCol('#555555', col, on), sw=1.6)
    if on > .05:
        glow(x + w / 2, y + h / 2, max(w, h) * .9, col, .9 * on)


def zebra(y0, y1, t=0, key='zeb'):
    """asphalt with zebra stripes in mild perspective between y0 (far) and y1 (near)"""
    boilSeed(key)
    flat([[-80, y0], [W + 80, y0], [W + 80, H + 80], [-80, H + 80]], C['asphalt'])
    n = 11
    for i in range(n):
        xf = lerp(-100, W + 100, (i + .25) / n)
        xn = lerp(-500, W + 500, (i + .25) / n)
        wf, wn = (W + 200) / n * .5, (W + 1000) / n * .5
        paint([[xf, y0 + 8], [xf + wf, y0 + 8], [xn + wn, y1], [xn, y1]], wash='#E9E4F2', washOp=235, ink=None)
    inkLine([[-80, y0], [W + 80, y0]], 1.2, INK, 'ink', 0)


def curtainStage(t, open_=1.0):
    flatRect(-80, -80, W + 160, H + 160, '#3A2250')
    for i, (x, col) in enumerate([(480, '#FF8FB1'), (960, '#FFE07A'), (1440, '#8FD3FF')]):
        glow(x, 420, 520, col, .55)
    flat([[-80, 790], [W + 80, 790], [W + 80, H + 80], [-80, H + 80]], '#A8653E')
    for i in range(9):
        inkLine([[-80, 805 + i * 32], [W + 80, 805 + i * 32]], .6, '#7A4527', 'inkfine', 0)
    inkLine([[-80, 790], [W + 80, 790]], 1.4, INK, 'ink', 0)
    for s in (-1, 1):
        boilSeed(f'cur{s}')
        x0 = W / 2 + s * (W / 2 + 60)
        x1 = W / 2 + s * lerp(60, 700, open_)
        pts = [[x0, -80], [x1, -80]]
        for i in range(12):
            yy = -80 + i * 85
            pts.append([x1 + s * (math.sin(i * 1.1) * 18 + (yy / H) ** 2 * 120 * open_), yy])
        pts += [[x0, H + 80]]
        paint(pts, wash='#C8324A', fill='#8E1E35', fillOp=70, ink=INK, sw=1.3)
        for k in range(1, 5):
            xx = lerp(x0, x1, k / 5)
            inkLine([[xx, -80], [xx + s * 20, 790]], .7, '#8E1E35', 'inkfine', .3)
    # valance
    boilSeed('val')
    pts = [[-80, -80], [W + 80, -80], [W + 80, 70]]
    for i in range(16, -1, -1):
        x = -80 + i * (W + 160) / 16
        pts.append([x, 70 + 35 * abs(math.sin(i * math.pi / 2))])
    paint(pts, wash='#C8324A', fill='#8E1E35', fillOp=60, ink=INK, sw=1.2)


def ringBox(x, y, s, k=1.0, key='ring'):
    boilSeed(key)
    paint(rrPts(x - 1.2 * s, y - 1.0 * s, 2.4 * s, 1.0 * s, .2 * s), wash='#E8476E', ink=INK, sw=1)
    push()
    translate(x, y - 1.0 * s)
    rotate(-1.9 * k)
    paint(rrPts(-1.2 * s, -.9 * s, 2.4 * s, .9 * s, .2 * s), wash='#F37C98', ink=INK, sw=1)
    pop()
    if k > .3:
        paint(ellPts(x, y - 1.25 * s, .5 * s, .38 * s, 14), ink='#F2C53D', sw=1.6)
        paint(starPts(x, y - 1.7 * s, .35 * s, .45, 4), wash='#DDF6FF', ink=INK, sw=.6)
        glow(x, y - 1.6 * s, 2.5 * s, '#FFF3B0', k)


def redThread(pts, sw=1.6):
    inkLine(pts, sw, '#E03A4E', 'ink', .5)
