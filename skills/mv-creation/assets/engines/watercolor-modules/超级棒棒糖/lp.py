# lp.py: props and sets for 《超级棒棒糖》 (watercolour + ink). Engine files stay untouched.
# Rainbow swirl lollipops, the bulb title sign over the weekend-market candy stall, his kitchen (no window), the magic pot,
# capes, a swing set, the kitten tree, the hero stat card, the weekend park, the fun-run track + finish arch (same bulb frame).
import math
from eng import *
import eng
from clawd import *
from props import C, puff, sparkle, sparkles, floatHearts, bubble, stamp, sunburst, stripes, groundBand, tree, bush, lamp, bench
from ch_chonghuai import rr, heart, popK, placardSign, batteryPct, HOT, WENKAI
from bsc import stringLights, spotlight, confetti, smokePuff, heartBalloon
from daw import line, _pa

RAINBOW = ['#F25C6E', '#F7A24B', '#F7D84E', '#7CCB6B', '#5BB8E8', '#9B7FE0']
GREYC = '#B9B6C0'
SKYA, SKYB = '#A9DBF5', '#E4F4FC'


def greyed(col, g):
    return mixCol(col, mixCol(GREYC, col, .15), clamp(g))


# ================================================================ the lollipop
def stickTo(x, y, L, ang, w, key='stk', grey=0.0):
    """white candy stick from (x, y) going L along angle ang (radians, 0 = right, pi/2 = down)"""
    ex, ey = x + math.cos(ang) * L, y + math.sin(ang) * L
    nx, ny = -math.sin(ang) * w / 2, math.cos(ang) * w / 2
    boilSeed(key)
    P = [[x + nx, y + ny], [ex + nx, ey + ny], [ex - nx, ey - ny], [x - nx, y - ny]]
    paint(P, wash='#FFFDF6', ink=INK, sw=max(.5, w / 22))
    n = int(L / (w * 1.6))
    for i in range(1, n):
        k = i / n
        cx, cy = lerp(x, ex, k), lerp(y, ey, k)
        line(cx + nx * .9, cy + ny * .9, cx - nx * .9 + math.cos(ang) * w * .5, cy - ny * .9 + math.sin(ang) * w * .5,
             greyed('#F48FB1', grey), .9, max(1.5, w * .22))
    return ex, ey


def lollipop(x, y, r, spin=0.0, key='lp', grey=0.0, glowK=0.0, stick=None, stickAng=math.pi / 2, sw=None, crack=0.0):
    """rainbow swirl lollipop: disc centred at (x, y), radius r. stick = length (from the centre) along stickAng."""
    sw = sw if sw is not None else clamp(r / 40, .5, 2.2)
    if glowK > .01:
        glow(x, y, r * 2.6, '#FFF2A8', .75 * glowK)
        glow(x, y, r * 1.6, '#FFFFFF', .5 * glowK)
    if stick:
        stickTo(x, y, stick, stickAng, max(4, r * .2), key=key + 's', grey=grey)
    boilSeed(key)
    disc = ellPts(x, y, r, r, 48)
    paint(disc, wash='#FFFDF6', ink=None)
    G.c.save()
    pth = eng._path(disc)
    G.c.clipPath(pth, skia.ClipOp.kIntersect, True)
    n = len(RAINBOW)
    turns = 1.15
    for i, col in enumerate(RAINBOW):
        P = []
        for j in range(19):
            s = j / 18
            a = spin + i * TAU / n + s * TAU * turns
            P.append([x + math.cos(a) * r * 1.05 * s, y + math.sin(a) * r * 1.05 * s])
        for j in range(18, -1, -1):
            s = j / 18
            a = spin + (i + .62) * TAU / n + s * TAU * turns
            P.append([x + math.cos(a) * r * 1.05 * s, y + math.sin(a) * r * 1.05 * s])
        flat(P, greyed(col, grey), 1)
    # soft centre + gloss
    G.c.drawCircle(x, y, r * .16, _pa(greyed('#FFFDF6', grey), .9))
    G.c.restore()
    paint(ellPts(x - r * .38, y - r * .42, r * .26, r * .14, 14, 0, -.7), wash='#FFFFFF', washOp=190, ink=None)
    paint(disc, ink=INK, sw=sw)
    if crack > 0:
        k = clamp(crack)
        inkLine([[x - r * .1, y - r * 1.02], [x + r * .12, y - r * .45], [x - r * .14, y + r * .05], [x + r * .1, y + r * .5],
                 [x - r * .02, y + r * 1.02 * k]], sw * 1.4, INK, 'ink', 0)


def lollipopHeld(hx, hy, r, L, ang=-math.pi / 2, **kw):
    """lollipop held at the stick's lower end (hx, hy); disc sits L away along ang (default straight up)"""
    cx, cy = hx + math.cos(ang) * L, hy + math.sin(ang) * L
    lollipop(cx, cy, r, stick=L, stickAng=ang + math.pi, **kw)
    return cx, cy


# ================================================================ bulbs + the title sign
def bulb(x, y, r, on, col='#FFE7A0'):
    G.c.drawCircle(x, y, r, _pa(mixCol('#6E6378', col, on)))
    G.c.drawCircle(x, y, r, _pa(INK, .85, max(1.2, r * .16)))
    if on > .03:
        glow(x, y, r * 3.6, col, .55 * on)
        G.c.drawCircle(x - r * .3, y - r * .3, r * .3, _pa('#FFFFFF', .8 * on))


def bulbRing(x, y, w, h, gap, lit, r=11, col='#FFE7A0'):
    """bulbs along a rectangle (x, y = centre). lit(i, n, px, py) -> 0..1"""
    pts = []
    per = 2 * (w + h)
    n = max(8, int(per / gap))
    for i in range(n):
        d = i / n * per
        if d < w:
            px, py = x - w / 2 + d, y - h / 2
        elif d < w + h:
            px, py = x + w / 2, y - h / 2 + (d - w)
        elif d < 2 * w + h:
            px, py = x + w / 2 - (d - w - h), y + h / 2
        else:
            px, py = x - w / 2, y + h / 2 - (d - 2 * w - h)
        pts.append((px, py))
    for i, (px, py) in enumerate(pts):
        bulb(px, py, r, clamp(lit(i, n, px, py)), col)


def centreLit(t, t0, x, w, speed=.42):
    """lighting order from the vertical axis outwards (A1 sign rule): bulb at |dx| lights at t0 - speed*(1-|dx|/(w/2))"""
    def f(i, n, px, py):
        d = abs(px - x) / (w / 2)
        tt = t0 - speed * (1 - d)
        return clamp((t - tt) / .06)
    return f


def bunting(x0, x1, y, sag, n, key='bt', cols=None, flap=0.0, grey=0.0):
    cols = cols or ['#F25C6E', '#F7D84E', '#5BB8E8', '#7CCB6B', '#F7A24B', '#9B7FE0']
    pts = []
    for i in range(n + 1):
        k = i / n
        pts.append([lerp(x0, x1, k), y + sag * 4 * k * (1 - k)])
    boilSeed(key)
    inkLine(pts, 1.0, '#5A4A5A', 'inkfine', .5)
    for i in range(n):
        a, b = pts[i], pts[i + 1]
        mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
        L = math.hypot(b[0] - a[0], b[1] - a[1]) * .85
        wob = flap * math.sin(i * 1.7 + G.T * 9) * .25
        boilSeed(f'{key}{i}')
        paint([[a[0] + (b[0] - a[0]) * .08, a[1] + (b[1] - a[1]) * .08], [b[0] - (b[0] - a[0]) * .08, b[1] - (b[1] - a[1]) * .08],
               [mx + L * .5 * wob, my + L * .75]], wash=greyed(cols[i % len(cols)], grey), ink=INK, sw=.6)


def titleSign(x, y, w, h, t, title='超级棒棒糖', lit=None, glowK=1.0, spinL=0.0, spinR=0.0, key='sign', sub=None, size=None,
              tcol='#E8476E', grey=0.0, bulbCol='#FFE7A0'):
    """wooden bulb sign centred at (x, y). lit = bulb function (None = all on). glowK dims the whole thing (0 = unlit)."""
    # side lollipops (sticks behind the frame)
    lollipop(x - w / 2 - h * .05, y - h * .12, h * .36, spin=spinL, key=key + 'll', stick=h * .9, stickAng=math.pi / 2 + .35,
             grey=grey)
    lollipop(x + w / 2 + h * .05, y - h * .12, h * .36, spin=spinR, key=key + 'lr', stick=h * .9, stickAng=math.pi / 2 - .35,
             grey=grey)
    if glowK > .01:
        glow(x, y, w * .7, '#FFD98A', .45 * glowK)
    boilSeed(key)
    paint(rrPts(x - w / 2, y - h / 2, w, h, 26), wash=greyed('#C98B5A', grey), fill='#8E5E3A', fillOp=80, ink=INK, sw=1.8)
    panel = mixCol('#5A3A4A', greyed('#FFE9EF', grey), .25 + .75 * glowK)
    paint(rrPts(x - w / 2 + 34, y - h / 2 + 34, w - 68, h - 68, 16), wash=panel, ink='#8E5E3A', sw=1.0)
    bulbRing(x, y, w - 34, h - 34, 58, lit or (lambda *a: glowK), r=h * .045, col=bulbCol)
    size = size or h * .44
    a = .45 + .55 * glowK
    text(title, x, y - (h * .06 if sub else 0), size, mixCol('#8A6A78', greyed(tcol, grey), glowK), stroke='#FFFFFF', strokeW=size * .16,
         shadow=True, a=a)
    if sub:
        text(sub, x, y + h * .3, h * .11, '#8E5E3A', shadow=False, a=a)


# ================================================================ weekend market + candy stall
def marketBack(t, ground=900, key='mk', grey=0.0):
    gradRect(-600, -600, W + 1200, ground + 600, [greyed(SKYA, grey), greyed(SKYB, grey), greyed('#FFF6E2', grey)])
    for i, (cx, cy, s) in enumerate([(160, 140, 26), (720, 70, 18), (1380, 120, 24), (1860, 60, 18), (-300, 90, 20), (2250, 150, 22)]):
        puff(cx + 12 * math.sin(t * .5 + i), cy, s, '#FFFFFF', key=f'{key}cl{i}', ink=True, a=.95)
    # far trees + roofs of the other stalls
    for i in range(-3, 9):
        tree(i * 300 + 60, ground - 260, 40 + 10 * hash1(i), key=f'{key}tr{i}', col=greyed(['#8FCF7A', '#7CC36B', '#A6D98A'][i % 3], grey))
    sides = [(-420, '#5BB8E8', '冰淇淋'), (-60, '#F7D84E', '气球'), (1980, '#7CCB6B', '果汁'), (2340, '#9B7FE0', '玩具')]
    for i, (sx, col, nm) in enumerate(sides):
        boilSeed(f'{key}ss{i}')
        paint(rectPts(sx - 160, ground - 360, 320, 360), wash=greyed('#FFF3E2', grey), ink=INK, sw=1.0)
        for j in range(6):
            ax = sx - 190 + j * 64
            paint([[ax, ground - 400], [ax + 64, ground - 400], [ax + 64, ground - 345], [ax + 32, ground - 325], [ax, ground - 345]],
                  wash=greyed(col if j % 2 == 0 else '#FFFFFF', grey), ink=INK, sw=.6)
        text(nm, sx, ground - 430, 40, greyed(col, grey), stroke='#FFFFFF', strokeW=7, shadow=False)
        paint(rectPts(sx - 140, ground - 300, 280, 200), wash=greyed('#4A3A44', grey), ink=INK, sw=.8)
        paint(rectPts(sx - 170, ground - 110, 340, 110), wash=greyed('#E9C9A0', grey), ink=INK, sw=.9)
        if nm == '气球':
            for q in range(5):
                bx_, by_ = sx - 110 + q * 55, ground - 520 - 40 * hash1(q)
                line(bx_, by_ + 34, sx - 20 + q * 10, ground - 300, '#5A4A5A', .8, 1.5)
                boilSeed(f'{key}bl{q}')
                paint(ellPts(bx_, by_, 30, 36, 18), wash=greyed(RAINBOW[q % 6], grey), ink=INK, sw=.7)
    # ground: paving + grass verge
    flatRect(-600, ground, W + 1200, 600, greyed('#E9DCCB', grey))
    for i in range(-6, 26):
        line(i * 110, ground, i * 110 - 40, ground + 200, '#D2C2AC', .6, 2)
    line(-600, ground, W + 600, ground, INK, 1, 3)
    bunting(-500, 700, 60, 70, 12, key=key + 'bu1', grey=grey)
    bunting(1220, 2420, 60, 70, 12, key=key + 'bu2', grey=grey)


def candyJar(x, y, s, col, key='cj', grey=0.0, n=6):
    """glass-free sweet jar (opaque painted tin) standing on (x, y)"""
    boilSeed(key)
    paint(rrPts(x - s * .5, y - s * 1.1, s, s * 1.1, s * .18), wash=greyed('#FFF8EE', grey), ink=INK, sw=.8)
    for i in range(n):
        cx = x + (hash1(i * 3.1 + s) - .5) * s * .7
        cy = y - s * .2 - hash1(i * 7.7 + s) * s * .7
        G.c.drawCircle(cx, cy, s * .13, _pa(greyed(RAINBOW[(i + int(s)) % 6], grey)))
    paint(rrPts(x - s * .56, y - s * 1.28, s * 1.12, s * .22, s * .08), wash=greyed(col, grey), ink=INK, sw=.7)


def candyStall(t, x=960, ground=900, w=980, key='cs', grey=0.0, rackFull=False, rackPop=None):
    """front view stall. Returns dict of anchor points: sign centre, rack card, counter top."""
    top = ground - 600
    for s in (-1, 1):
        boilSeed(key + 'p%d' % s)
        paint(rectPts(x + s * w / 2 - 16, top + 60, 32, 540), wash=greyed('#B07A54', grey), ink=INK, sw=1.0)
    # back wall with shelves of jars
    flatRect(x - w / 2 + 16, top + 150, w - 32, 300, greyed('#F7E1E8', grey))
    for j in range(2):
        yy = top + 280 + j * 135
        line(x - w / 2 + 16, yy, x + w / 2 - 16, yy, greyed('#B07A54', grey), 1, 8)
        for i in range(8):
            px = x - w / 2 + 80 + i * (w - 160) / 7
            candyJar(px, yy - 4, 62, RAINBOW[(i + j * 3) % 6], key=f'{key}j{j}{i}', grey=grey)
    # awning
    boilSeed(key + 'aw')
    aw = [[x - w / 2 - 70, top + 160], [x - w / 2 + 20, top], [x + w / 2 - 20, top], [x + w / 2 + 70, top + 160]]
    paint(aw, wash='#FFFFFF', ink=INK, sw=1.4)
    n = 12
    for i in range(0, n, 2):
        a0, a1 = i / n, (i + 1) / n
        P = [[lerp(x - w / 2 + 20, x + w / 2 - 20, a0), top], [lerp(x - w / 2 + 20, x + w / 2 - 20, a1), top],
             [lerp(x - w / 2 - 70, x + w / 2 + 70, a1), top + 160], [lerp(x - w / 2 - 70, x + w / 2 + 70, a0), top + 160]]
        paint(P, wash=greyed('#F48FB1', grey), ink=None)
    paint(aw, ink=INK, sw=1.4)
    for i in range(n):
        cx = lerp(x - w / 2 - 70, x + w / 2 + 70, (i + .5) / n)
        r = (w + 140) / n / 2
        boilSeed(f'{key}sc{i}')
        paint(ellPts(cx, top + 160, r, r * .55, 16), wash=greyed('#F48FB1', grey) if i % 2 == 0 else '#FFFFFF', ink=INK, sw=1.0)
    stringLights([[x - w / 2 - 60, top + 190], [x, top + 235], [x + w / 2 + 60, top + 190]], t, 1 - grey, key=key + 'sl')
    # counter
    ct = ground - 210
    boilSeed(key + 'ct')
    paint(rectPts(x - w / 2 + 10, ct, w - 20, 210), wash=greyed('#F7C6D2', grey), fill='#E8909F', fillOp=60, ink=INK, sw=1.3)
    for i in range(7):
        cx = x - w / 2 + 90 + i * (w - 180) / 6
        boilSeed(f'{key}cd{i}')
        paint(ellPts(cx, ct + 110, 34, 24, 16), wash=greyed(RAINBOW[i % 6], grey), ink=INK, sw=.7)
        for sgn in (-1, 1):
            paint([[cx + sgn * 32, ct + 110], [cx + sgn * 58, ct + 92], [cx + sgn * 58, ct + 128]], wash=greyed(RAINBOW[i % 6], grey), ink=INK,
                  sw=.6)
    paint(rectPts(x - w / 2 - 14, ct - 30, w + 28, 34), wash=greyed('#C98B5A', grey), ink=INK, sw=1.2)
    # lollipop rack (wooden block with holes) on the counter, right of centre
    rx, ry = x + 170, ct - 30
    boilSeed(key + 'rack')
    paint(rrPts(rx - 150, ry - 70, 300, 70, 12), wash=greyed('#D9A36F', grey), fill='#B07A54', fillOp=60, ink=INK, sw=1.0)
    for i in range(6):
        hx = rx - 115 + i * 46
        if rackFull or (rackPop and rackPop(i)):
            lollipop(hx, ry - 190, 34, spin=i, key=f'{key}rl{i}', stick=120, grey=grey)
        G.c.drawCircle(hx, ry - 52, 9, _pa('#5A3A2A'))
    # price card on a little stake
    cx_, cy_ = rx + 230, ry - 150
    line(cx_, cy_ + 50, cx_, ry - 4, '#8E5E3A', 1, 5)
    boilSeed(key + 'card')
    paint(rrPts(cx_ - 90, cy_ - 55, 180, 110, 10), wash='#FFFDF6', ink=INK, sw=.9)
    text('超级棒棒糖', cx_, cy_ - 22, 26, HOT, shadow=False)
    text('¥ 5', cx_, cy_ + 20, 36, INK, shadow=False)
    return dict(sign=(x, top - 150), rack=(rx, ry - 50), card=(cx_, cy_), counter=ct - 30)


def rainCloud(x, y, s, t, k=1.0, key='rc'):
    """a small grey cloud with drizzle; k = pop-in"""
    p = backOut(clamp(k))
    if p < .02:
        return
    push()
    translate(x, y)
    scale(p)
    for i in range(11):
        ph = frac(t * 2.2 + i * .37)
        dx = (i - 5) * s * .21 + math.sin(i * 2.1) * s * .06
        y0 = s * .45 + ph * s * 1.5
        line(dx, y0, dx - s * .07, y0 + s * .3, '#5F8FD0', .95 * (1 - .7 * ph), max(4, s * .075))
    puff(0, 0, s * .45, '#C8C6D6', key=key, ink=True)
    pop()


# ================================================================ capes, headband
def cape(x, y, u, col, dk, flutter=0.0, side=1, k=1.0, view='front', key='cape'):
    """drawn BEFORE the character: a little cape hanging behind the body; side = which way it streams (+1 right)"""
    if k <= .01:
        return
    s = backOut(clamp(k))
    push()
    translate(x, y)
    scale(s, s)
    boilSeed(key)
    fl = flutter
    if view in ('front', 'back'):
        P = [[-4.4 * u, -7.6 * u], [4.4 * u, -7.6 * u], [6.0 * u + side * fl * 2 * u, -1.0 * u], [3.0 * u + side * fl * 2.4 * u, -.2 * u],
             [0 + side * fl * 2.6 * u, -.9 * u], [-3.0 * u + side * fl * 2.4 * u, -.2 * u], [-6.0 * u + side * fl * 2 * u, -1.0 * u]]
    else:
        b = side
        P = [[b * -1.0 * u, -7.7 * u], [b * 5.0 * u, -7.4 * u], [b * (8.0 + 3 * fl) * u, (-3.2 - 2.2 * fl) * u],
             [b * (9.4 + 3.6 * fl) * u, (-.9 - 2.6 * fl) * u], [b * (6.4 + 2.4 * fl) * u, (-.6 - 1.6 * fl) * u], [b * 3.6 * u, -1.2 * u]]
    paint(P, wash=col, fill=dk, fillOp=80, ink=INK, sw=clamp(u / 15, .45, 2.0), curv=.35)
    pop()


def headbandDraw(txt='加油', col='#E8476E'):
    """clawd 'draw' hook (local body coords): a red headband with tails"""
    def f(u, sw):
        P = [[-5.05 * u, -7.75 * u], [5.05 * u, -7.75 * u], [5.05 * u, -6.95 * u], [-5.05 * u, -6.95 * u]]
        boilSeed('hband')
        paint(P, wash=col, ink=INK, sw=sw * .7)
        paint([[5.0 * u, -7.4 * u], [6.6 * u, -8.3 * u], [6.9 * u, -7.7 * u]], wash=col, ink=INK, sw=sw * .6)
        paint([[5.0 * u, -7.3 * u], [6.8 * u, -6.6 * u], [6.6 * u, -6.1 * u]], wash=col, ink=INK, sw=sw * .6)
        text(txt, 0, -7.35 * u, .72 * u, '#FFFFFF', shadow=False)
    return f


# ================================================================ kitchen (no window)
def kitchenBack(t, key='kt', warm=1.0):
    flatRect(-500, -500, W + 1000, 1300, '#FBE9D2')
    for i in range(-6, 30):
        flatRect(i * 96, -500, 48, 1300, '#F6DEC0', .6)
    # tiled backsplash
    flatRect(-500, 470, W + 1000, 300, '#E6F2EE')
    for i in range(-6, 30):
        line(i * 80, 470, i * 80, 770, '#C3DCD4', 1, 2)
    for j in range(5):
        line(-500, 470 + j * 60, W + 500, 470 + j * 60, '#C3DCD4', 1, 2)
    line(-500, 470, W + 500, 470, INK, 1, 2.5)
    # shelves with jars (left) and a hanging utensil rail (right)
    for j, sy_ in enumerate((190, 350)):
        boilSeed(f'{key}sh{j}')
        paint(rectPts(80, sy_, 560, 20), wash='#B07A54', ink=INK, sw=.9)
        for q in range(6):
            candyJar(130 + q * 92, sy_, 56, RAINBOW[(q + j * 2) % 6], key=f'{key}j{j}{q}')
    line(1260, 170, 1840, 170, '#6A5A70', 1, 6)
    tools = [('spoon', 1310), ('whisk', 1400), ('ladle', 1490), ('pan', 1620), ('spat', 1760)]
    for nm, tx in tools:
        boilSeed(f'{key}{nm}')
        line(tx, 170, tx, 200, INK, 1, 2)
        if nm == 'pan':
            paint(ellPts(tx, 300, 70, 70, 26), wash='#6A6478', fill='#4A4458', fillOp=80, ink=INK, sw=1.0)
            paint(rectPts(tx - 8, 196, 16, 40), wash='#8E5E3A', ink=INK, sw=.7)
        elif nm == 'whisk':
            for q in range(5):
                inkLine([[tx, 230], [tx - 30 + q * 15, 300], [tx, 340]], .8, '#8A8A98', 'inkfine', .6)
            paint(rectPts(tx - 7, 196, 14, 40), wash='#E8909F', ink=INK, sw=.7)
        else:
            paint(rectPts(tx - 6, 196, 12, 110), wash='#C98B5A', ink=INK, sw=.7)
            paint(ellPts(tx, 330, 26 if nm != 'spat' else 22, 30, 16), wash='#C98B5A' if nm != 'ladle' else '#A9A4B8', ink=INK, sw=.8)
    # calendar (周六 circled) + clock
    boilSeed(key + 'cal')
    paint(rectPts(800, 120, 210, 250), wash='#FFFDF6', ink=INK, sw=1.0)
    flatRect(800, 120, 210, 56, '#E8476E')
    text('十一月', 905, 148, 30, '#FFFFFF', shadow=False)
    for r_ in range(4):
        for c_ in range(5):
            G.c.drawCircle(830 + c_ * 38, 210 + r_ * 40, 5, _pa('#C9C1D6'))
    text('周六', 905, 330, 34, HOT, shadow=False)
    paint(ellPts(905, 330, 58, 30, 20), ink=HOT, sw=1.1)
    boilSeed(key + 'clk')
    paint(ellPts(1120, 230, 70, 70, 30), wash='#FFFDF6', ink=INK, sw=1.2)
    a1 = t * .25
    line(1120, 230, 1120 + math.cos(a1 - 1.2) * 46, 230 + math.sin(a1 - 1.2) * 46, INK, 1, 4)
    line(1120, 230, 1120 + math.cos(-.4) * 32, 230 + math.sin(-.4) * 32, INK, 1, 5)
    stringLights([[-40, 60], [500, 110], [960, 70], [1420, 110], [1980, 60]], t, warm, key=key + 'sl')
    # a potted herb on the shelf end
    boilSeed(key + 'herb')
    paint([[650, 350], [700, 350], [694, 300], [656, 300]], wash='#D9774E', ink=INK, sw=.7)
    for lf in range(5):
        a = -math.pi / 2 + (lf - 2) * .45
        paint(ellPts(675 + math.cos(a) * 26, 280 + math.sin(a) * 18, 9, 22, 8, 0, a + math.pi / 2), wash='#7CC36B', ink=INK, sw=.4)


def counterFront(y=720, key='kc', flame=1.0, t=0.0, potX=960):
    """counter in front of the cooks (draw AFTER the characters). y = worktop."""
    boilSeed(key)
    paint(rectPts(-200, y, W + 400, 30), wash='#D9C3A5', ink=INK, sw=1.3)
    paint(rectPts(-200, y + 30, W + 400, 400), wash='#8FC9B8', fill='#6FAE9C', fillOp=60, ink=INK, sw=1.2)
    for i in range(-1, 9):
        paint(rectPts(i * 260 + 30, y + 70, 220, 180, 2), ink='#5E9A88', sw=.8)
        G.c.drawCircle(i * 260 + 140, y + 92, 7, _pa('#F2C53D'))
    # burner glow under the pot
    if flame > .01:
        for q in range(5):
            fx = potX - 80 + q * 40
            fh = 18 + 8 * math.sin(t * 20 + q * 1.7)
            paint([[fx - 10, y + 2], [fx + 10, y + 2], [fx, y - fh]], wash='#FF9A3C', ink=None)
            paint([[fx - 5, y + 2], [fx + 5, y + 2], [fx, y - fh * .55]], wash='#5BB8E8', ink=None)


def pot(x, y, s, lid=0.0, glowK=0.0, syrup='#F7A1B6', key='pot', t=0.0, lidPop=None):
    """big cooking pot standing on (x, y); s = half width. lid 0 = on, 1 = gone; returns rim centre."""
    rimY = y - s * 1.05
    if glowK > .01:
        glow(x, rimY, s * 3.2, '#FFE38A', .8 * glowK)
    boilSeed(key)
    for sg in (-1, 1):
        paint(rrPts(x + sg * s - (0 if sg > 0 else s * .32), rimY + s * .18, s * .32, s * .18, s * .06), wash='#3E3A52', ink=INK, sw=1.0)
    paint([[x - s, rimY], [x + s, rimY], [x + s * .92, y], [x - s * .92, y]], wash='#E8574E', fill='#B8324F', fillOp=70, ink=INK, sw=1.4)
    paint(rectPts(x - s, rimY + s * .1, s * 2, s * .12), wash='#FFFDF6', ink=None)
    paint(ellPts(x, rimY, s, s * .22, 30), wash='#B8324F', ink=INK, sw=1.2)
    paint(ellPts(x, rimY + s * .03, s * .9, s * .17, 30), wash=syrup, ink=None)
    if glowK > .01:
        paint(ellPts(x, rimY + s * .03, s * .9, s * .17, 30), wash='#FFF6C8', washOp=int(220 * glowK), ink=None)
    if lid < 1:
        if lidPop is not None:
            ly, la = lidPop
        else:
            ly, la = 0.0, 0.0
        push()
        translate(x, rimY - ly)
        rotate(la)
        boilSeed(key + 'lid')
        paint(ellPts(0, 0, s * 1.02, s * .24, 30), wash='#F06A5E', fill='#B8324F', fillOp=50, ink=INK, sw=1.2)
        paint(ellPts(0, -s * .26, s * .16, s * .08, 14), wash='#3E3A52', ink=INK, sw=.9)
        paint(rectPts(-s * .05, -s * .26, s * .1, s * .2), wash='#3E3A52', ink=None)
        pop()
    return x, rimY


def syrupBottle(x, y, s, ang, col, key='sb'):
    """a squeeze bottle: (x, y) = where the hand holds it; nozzle points along ang"""
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    paint(rrPts(-s * .4, -s * .9, s * .8, s * 1.4, s * .2), wash=col, fill=mixCol(col, INK, .3), fillOp=50, ink=INK, sw=.9)
    paint([[-s * .18, -s * .9], [s * .18, -s * .9], [s * .05, -s * 1.35], [-s * .05, -s * 1.35]], wash='#FFFDF6', ink=INK, sw=.8)
    paint(rrPts(-s * .3, -s * .4, s * .6, s * .45, s * .1), wash='#FFFDF6', ink=None)
    pop()
    return x + math.sin(ang) * s * 1.35, y - math.cos(ang) * s * 1.35


def pour(p0, p1, col, k=1.0, w=10):
    if k <= .01:
        return
    mx = (p0[0] + p1[0]) / 2 + 20
    P = through([p0, [mx, (p0[1] + p1[1]) / 2], [p1[0], p1[1]]], 8)
    n = max(2, int(len(P) * clamp(k)))
    G.c.drawPath(eng._path(P[:n], close=False), _pa(col, .95, w))


# ================================================================ park
def parkBack(t, ground=820, key='pk', grey=0.0, hills=True):
    gradRect(-600, -600, W + 1200, ground + 600, [greyed('#9FD6F2', grey), greyed('#DDF2FB', grey), greyed('#FFF6E2', grey)])
    for i, (cx, cy, s) in enumerate([(240, 120, 26), (900, 80, 20), (1500, 150, 28), (2100, 90, 20), (-300, 140, 22)]):
        puff(cx + 14 * math.sin(t * .4 + i), cy, s, '#FFFFFF', key=f'{key}cl{i}', ink=True, a=.95)
    if hills:
        for j, col in enumerate(['#BFE3A8', '#A6D98A']):
            boilSeed(f'{key}h{j}')
            y0 = ground - 150 + j * 70
            pts = [[-600, ground + 50]]
            for i in range(31):
                x = -600 + i * (W + 1200) / 30
                pts.append([x, y0 - 50 * math.sin(i * .5 + j * 1.9) ** 2 - 20 * math.sin(i * 1.4 + j)])
            pts.append([W + 600, ground + 50])
            paint(pts, wash=greyed(col, grey), ink=INK, sw=.9, curv=.4)
    boilSeed(key + 'g')
    paint([[-600, ground], [W + 600, ground], [W + 600, H + 600], [-600, H + 600]], wash=greyed('#9ED27A', grey), fill=greyed('#79B45B', grey),
          fillOp=50, ink=None)
    line(-600, ground, W + 600, ground, mixCol('#79B45B', INK, .4), 1, 2.5)
    for i in range(40):
        gx = -500 + hash1(i * 3.3) * (W + 1000)
        gy = ground + 20 + hash1(i * 5.1) * 220
        inkLine([[gx - 8, gy], [gx - 3, gy - 16], [gx + 2, gy]], .6, greyed('#5E9A48', grey), 'inkfine', .3)
        if i % 3 == 0:
            G.c.drawCircle(gx + 14, gy - 6, 6, _pa(greyed(['#FFFFFF', '#F7D84E', '#F48FB1'][i % 3], grey)))


def bird(x, y, s, t, seed=0):
    f = math.sin(t * 14 + seed * 2.3)
    inkLine([[x - s, y - s * .3 * f], [x - s * .3, y + s * .1], [x, y], [x + s * .3, y + s * .1], [x + s, y - s * .3 * f]], max(.8, s / 14),
            INK, 'ink', .4)


def swingSet(x, top, w, key='sw'):
    """A-frame swing set, (x, top) = top bar centre. Draw before the swinger."""
    boilSeed(key)
    for sg in (-1, 1):
        for d in (-1, 1):
            inkLine([[x + sg * w / 2, top], [x + sg * w / 2 + d * 120, top + 640]], 5.0, '#5B7FC4', 'ink', 0)
    paint(rrPts(x - w / 2 - 30, top - 16, w + 60, 32, 14), wash='#E8476E', ink=INK, sw=1.2)


def rainbowArc(cx, cy, R, bw, bands, key='rb', a=1.0, grey=0.0, a0=math.pi, a1=TAU):
    """bands = list of 0..1 progress for each of the 6 colours (outer first); arc from a0 to a1"""
    for i, k in enumerate(bands):
        if k <= .01:
            continue
        r0 = R - i * bw
        aa = lerp(a0, a1, clamp(k))
        P = []
        n = 40
        for j in range(n + 1):
            ang = lerp(a0, aa, j / n)
            P.append([cx + math.cos(ang) * r0, cy + math.sin(ang) * r0])
        for j in range(n, -1, -1):
            ang = lerp(a0, aa, j / n)
            P.append([cx + math.cos(ang) * (r0 - bw), cy + math.sin(ang) * (r0 - bw)])
        boilSeed(f'{key}{i}')
        paint(P, wash=greyed(RAINBOW[i], grey), washOp=int(235 * a), ink=INK if a > .5 else None, sw=.8)


# ================================================================ dream / gift / hero card
def giftBox(x, y, w, h, shake=0.0, bow=0.0, key='gift', t=0.0):
    """tall gift box standing on (x, y); bow 0..1 = ribbon loosening"""
    push()
    translate(x + shake * math.sin(t * 70) * 10, y)
    rotate(shake * .05 * math.sin(t * 55))
    boilSeed(key)
    paint(rrPts(-w / 2, -h, w, h, 14), wash='#9B7FE0', fill='#6E54B8', fillOp=60, ink=INK, sw=1.4)
    for q in range(5):
        G.c.drawCircle(-w / 2 + w * (.2 + .15 * q), -h * (.2 + .13 * (q % 3)), 10, _pa('#F7D84E', .9))
    paint(rectPts(-w * .08, -h, w * .16, h), wash='#F25C6E', ink=INK, sw=.9)
    paint(rrPts(-w / 2 - 12, -h - 10, w + 24, 50, 12), wash='#B49CF0', ink=INK, sw=1.2)
    paint(rectPts(-w * .08, -h - 10, w * .16, 50), wash='#F25C6E', ink=None)
    lo = clamp(bow)
    for sg in (-1, 1):
        paint([[0, -h - 14], [sg * w * (.42 + .1 * lo), -h - 70 + 120 * lo], [sg * w * (.4 + .05 * lo), -h - 4 + 110 * lo]], wash='#F25C6E',
              ink=INK, sw=1.0, curv=.3)
        if lo > .05:
            inkLine([[sg * 10, -h - 10], [sg * (30 + 40 * lo), -h + 60 * lo], [sg * (20 + 70 * lo), -h + 150 * lo]], 7, '#F25C6E', 'ink', .5)
    paint(ellPts(0, -h - 14 + 20 * lo, 16, 14, 12), wash='#E0344E', ink=INK, sw=.9)
    pop()


def meterBar(x, y, w, h, frac, col, label, key='mb'):
    boilSeed(key)
    text(label, x - 30, y, h * .9, INK, align='right', shadow=False)
    paint(rrPts(x, y - h / 2, w, h, h / 2), wash='#FFFDF6', ink=INK, sw=1.1)
    n = 8
    for i in range(n):
        if (i + .5) / n <= frac:
            paint(rrPts(x + 8 + i * (w - 16) / n, y - h / 2 + 8, (w - 16) / n - 6, h - 16, 6), wash=col, ink=None)


def kitten(x, y, s, t, pose='sit', look=1, key='kit', mouthOpen=0.0):
    """small ginger kitten, (x, y) = ground point; s ~ head radius"""
    boilSeed(key)
    col, dk = '#F4A24B', '#C9742E'
    push()
    translate(x, y)
    scale(look, 1)
    if pose == 'slide':
        rotate(.5)
    # tail
    tw = math.sin(t * 6) * .3
    inkLine([[-s * .9, -s * .5], [-s * 1.7, -s * 1.0 + tw * s], [-s * 1.6, -s * 1.9 + tw * s]], s * .28, col, 'ink', .6)
    paint(ellPts(0, -s * .7, s * 1.05, s * .75, 20), wash=col, fill=dk, fillOp=50, ink=INK, sw=.9)
    paint(ellPts(s * .55, -s * 1.7, s * .85, s * .75, 20), wash=col, fill=dk, fillOp=40, ink=INK, sw=.9)
    for sg in (-1, 1):
        ex = s * .55 + sg * s * .5
        paint([[ex - s * .25, -s * 2.2], [ex + sg * s * .1, -s * 2.75], [ex + s * .25, -s * 2.2]], wash=col, ink=INK, sw=.7)
    for sg in (-1, 1):
        G.c.drawCircle(s * .55 + sg * s * .3, -s * 1.78, s * .1, _pa(INK))
    if mouthOpen > .1:
        paint(ellPts(s * .55, -s * 1.42, s * .14, s * .14 * mouthOpen + s * .04, 10), wash='#B8324F', ink=INK, sw=.5)
    else:
        inkLine([[s * .45, -s * 1.45], [s * .55, -s * 1.38], [s * .65, -s * 1.45]], .7, INK, 'inkfine', .3)
    for q in range(3):
        line(s * .2, -s * (1.0 + .3 * q), s * .9, -s * (1.0 + .3 * q), dk, .7, 3)
    pop()


def bigTree(x, y, s, key='bt', grey=0.0, bloom=0.0):
    """large park tree; returns the tip of its long right branch"""
    boilSeed(key)
    trunk = '#9B6B45'
    paint([[x - .55 * s, y], [x + .55 * s, y], [x + .35 * s, y - 4.2 * s], [x - .35 * s, y - 4.2 * s]], wash=greyed(trunk, grey), ink=INK, sw=1.3)
    bx0, by0 = x + .2 * s, y - 3.4 * s
    tip = (x + 3.6 * s, y - 4.3 * s)
    inkLine([[bx0, by0], [x + 1.8 * s, y - 4.0 * s], tip], s * .1, greyed(trunk, grey), 'ink', .4)
    blobs = [(0, -5.6, 2.6, 1.8), (-1.6, -4.9, 1.7, 1.3), (1.5, -5.2, 1.9, 1.4), (.2, -6.9, 1.8, 1.2), (3.4, -4.9, 1.3, .8)]
    for i, (dx, dy, rx, ry) in enumerate(blobs):
        boilSeed(f'{key}c{i}')
        paint(ellPts(x + dx * s, y + dy * s, rx * s, ry * s, 26, s * .04), wash=greyed('#7CC36B', grey), fill=greyed('#4E9A4E', grey),
              fillOp=60, ink=INK, sw=1.1, curv=.2)
    for i in range(12):
        fx = x + (hash1(i * 2.3) - .4) * 4.4 * s
        fy = y - (4.6 + hash1(i * 3.9) * 2.6) * s
        r = s * .16 * (bloom if bloom else .8)
        if r > 1:
            boilSeed(f'{key}f{i}')
            paint(ellPts(fx, fy, r, r, 10), wash=greyed('#F7A1B6', grey), ink=None)
    return tip


def flowerBed(x, y, w, t, bloom=1.0, key='fb', grey=0.0):
    boilSeed(key)
    paint(rrPts(x - w / 2, y - 40, w, 70, 30), wash=greyed('#B07A54', grey), ink=INK, sw=1.0)
    n = int(w / 50)
    for i in range(n):
        fx = x - w / 2 + 30 + i * (w - 60) / max(1, n - 1)
        fy = y - 60 - 20 * hash1(i * 4.1)
        inkLine([[fx, y - 30], [fx, fy]], 1.2, greyed('#4E9A4E', grey), 'ink', 0)
        b = clamp(bloom * 1.3 - hash1(i) * .3)
        if b > .02:
            col = greyed(RAINBOW[i % 6], grey)
            for p in range(5):
                a = p / 5 * TAU + i
                G.c.drawCircle(fx + math.cos(a) * 12 * b, fy + math.sin(a) * 12 * b, 10 * b, _pa(col))
            G.c.drawCircle(fx, fy, 7 * b, _pa(greyed('#FFF27A', grey)))
        else:
            G.c.drawCircle(fx, fy, 7, _pa(greyed('#7CC36B', grey)))


def fountain(x, y, s, t, spray=1.0, key='fn', grey=0.0):
    boilSeed(key)
    if spray > .01:
        for i in range(9):
            a = -math.pi / 2 + (i - 4) * .22
            h_ = s * (2.2 + .4 * math.sin(t * 6 + i)) * spray
            P = [[x, y - s * 1.6], [x + math.cos(a) * h_ * .5, y - s * 1.6 - h_ * .9], [x + math.cos(a) * h_ * 1.1, y - s * .7]]
            inkLine(P, 2.0, greyed('#7FC8F0', grey), 'ink', .6)
        glow(x, y - s * 2.6, s * 2, '#FFFFFF', .3 * spray)
    paint(ellPts(x, y - s * .35, s * 2.4, s * .5, 30), wash=greyed('#C9C3D6', grey), ink=INK, sw=1.1)
    paint(ellPts(x, y - s * .45, s * 2.0, s * .32, 30), wash=greyed('#8FD3FF', grey), ink=None)
    paint(rectPts(x - s * .25, y - s * 1.6, s * .5, s * 1.2), wash=greyed('#C9C3D6', grey), ink=INK, sw=.9)
    paint(ellPts(x, y - s * 1.6, s * .8, s * .2, 20), wash=greyed('#C9C3D6', grey), ink=INK, sw=.9)


# ================================================================ fun-run track + finish arch
def trackScene(t, ground=760, key='tr', ditchX=(980, 1180)):
    parkBack(t, ground - 40, key=key + 'pk', hills=True)
    # running track (two lanes) + a little stream crossing it
    boilSeed(key + 'tk')
    paint([[-600, ground - 10], [W + 600, ground - 10], [W + 600, ground + 190], [-600, ground + 190]], wash='#E9906E', fill='#C96A4E',
          fillOp=50, ink=INK, sw=1.0)
    for ly in (ground + 60, ground + 125):
        line(-600, ly, W + 600, ly, '#FFFFFF', .9, 4)
    x0, x1 = ditchX
    boilSeed(key + 'dt')
    paint([[x0 - 26, ground - 12], [x1 + 26, ground - 12], [x1 + 70, ground + 192], [x0 - 70, ground + 192]], wash='#8A6A4A', fill='#6A4A32',
          fillOp=70, ink=INK, sw=1.1)
    paint([[x0, ground - 4], [x1, ground - 4], [x1 + 40, ground + 192], [x0 - 40, ground + 192]], wash='#4F9ED6', fill='#2F6EA8', fillOp=80,
          ink=INK, sw=1.0)
    for q in range(5):
        boilSeed(f'{key}rd{q}')
        rx_ = x0 - 30 + q * (x1 - x0 + 60) / 4
        for j in range(3):
            inkLine([[rx_ + j * 8, ground + 4], [rx_ + j * 8 - 6 + 4 * j, ground - 40 - 14 * j]], 1.2, '#4E7A3E', 'ink', .3)
    for q in range(4):
        yy = ground + 20 + q * 45
        wv = math.sin(t * 5 + q) * 8
        inkLine([[x0 - 10 + q * 6, yy], [(x0 + x1) / 2 + wv, yy + 6], [x1 + 10 - q * 6, yy]], .9, '#FFFFFF', 'inkfine', .5)
    for q, (bx, by) in enumerate([(x0 - 30, ground - 4), (x1 + 34, ground + 6), (x0 - 10, ground + 186)]):
        boilSeed(f'{key}st{q}')
        paint(ellPts(bx, by, 26, 14, 12), wash='#A9A4B8', ink=INK, sw=.7)


def finishBoard(x, yBack, w, h, t, lit=None, txt='周末快乐', key='fa', glowK=1.0):
    """finish gantry standing on the far edge of the track: two striped posts + the bulb sign (same frame as the opening sign)"""
    for sg in (-1, 1):
        boilSeed(key + 'p%d' % sg)
        px = x + sg * w / 2
        paint(rectPts(px - 20, yBack - h, 40, h), wash='#F48FB1', fill='#E8476E', fillOp=60, ink=INK, sw=1.2)
        for q in range(6):
            line(px - 20, yBack - h + 40 + q * (h - 60) / 6, px + 20, yBack - h + 70 + q * (h - 60) / 6, '#FFFFFF', .8, 6)
    titleSign(x, yBack - h - 40, w + 160, 180, t, title=txt, lit=lit, glowK=glowK, key=key + 's', size=88, spinL=t * 2, spinR=-t * 2)


def finishTape(x, yBack, yFront, hgt, snap=0.0, key='ftp'):
    """finish line across the track (checkered band) + the tape between a far post and a near post; snap > 0 = broken"""
    for j in range(8):
        for q in range(2):
            y0 = lerp(yBack, yFront, j / 8)
            y1 = lerp(yBack, yFront, (j + 1) / 8)
            if (j + q) % 2 == 0:
                flat([[x - 26 + q * 26, y0], [x + q * 26, y0], [x + q * 26, y1], [x - 26 + q * 26, y1]], '#FFFFFF', .95)
            else:
                flat([[x - 26 + q * 26, y0], [x + q * 26, y0], [x + q * 26, y1], [x - 26 + q * 26, y1]], '#3A3550', .9)
    tops = []
    for yy in (yBack, yFront):
        boilSeed(f'{key}{yy:.0f}')
        paint(rectPts(x - 7, yy - hgt, 14, hgt), wash='#FFFDF6', ink=INK, sw=.8)
        tops.append((x, yy - hgt + 8))
    (x0, y0), (x1, y1) = tops
    if snap <= 0:
        inkLine([[x0, y0], [x + 14, (y0 + y1) / 2], [x1, y1]], 5.0, '#E8476E', 'ink', .5)
    else:
        k = clamp(snap)
        for (px, py), sg in (((x0, y0), -1), ((x1, y1), 1)):
            L = (y1 - y0) / 2
            inkLine([[px, py], [px + 40 * k, py - sg * L * .5 * (1 - k) + 30 * k], [px + 90 * k + 20, py - sg * L * (1 - .7 * k) + 80 * k]],
                    5.0, '#E8476E', 'ink', .5)


def speedLines(x0, x1, y0, y1, t, n=10, col=INK, a=.7, seed=0):
    for i in range(n):
        y = lerp(y0, y1, hash1(seed + i * 1.7))
        L = lerp(.3, 1, hash1(seed + i * 3.1)) * (x1 - x0)
        ph = frac(t * 3 + hash1(i))
        xs = lerp(x1, x0 - L, ph)
        line(xs, y, xs + L * .5, y, col, a * math.sin(ph * math.pi), 3)


def candyPiece(x, y, s, col, rot=0.0, key='cp'):
    """wrapped sweet"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(ellPts(0, 0, s, s * .7, 16), wash=col, ink=INK, sw=.7)
    for sg in (-1, 1):
        paint([[sg * s * .9, 0], [sg * s * 1.7, -s * .6], [sg * s * 1.7, s * .6]], wash=col, ink=INK, sw=.6)
    G.c.drawCircle(-s * .3, -s * .25, s * .2, _pa('#FFFFFF', .7))
    pop()
