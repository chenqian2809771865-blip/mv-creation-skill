# dx.py: props, sets and costumes for 《东西》 (林俊呈) — watercolour + boiling ink. Engine files stay untouched.
# Theme: 「示例歌词占位文」 — he runs a tiny general store (小橘杂货铺); she brings a parcel; inside is a compass with only 东 and 西.
# The messenger app is made up (its own green, no logo).
import math
from eng import *
import eng
import clawd as CL
from clawd import *
from props import puff, sparkle, sparkles, floatHearts, bubble, stamp, sunburst, stripes, tree, bush, lamp, impactLines, gradient
from sets import sky, sunDisc, sea, palm, gull
from ch_chonghuai import heart, popK, shakeAmt, phoneBody, screenClip, typingDots, WENKAI, HOT, PINK, PINKDK, CREAM, miniHead
from bsc import stringLights, confetti
import wx
from wx import chatPage, chatMsg, statusBar, appTopBar, line, _pa, doorBell, hearts, GREY, APPG
from tp import paperBall, wastebasket, dreamFrame, polaroidPic
from bbset import wallClock2, calendar, plant
from common import handXY, B, bt, pk, after, age, kt

WOOD, WOODDK, WOODLT = '#C48A5C', '#94603A', '#DDA878'
BRASS, BRASSDK, BRASSLT = '#D9A63E', '#9C7224', '#F4D27A'
EAST, WEST = '#E8574A', '#4A7FD9'          # 东 warm red, 西 cool blue
HERNAME = '小花'


# ------------------------------------------------------------------ cast tweaks
def miniHead2(x, y, r, who='her', face='happy', key='mh'):
    """chat avatar head: her keeps her white flower (no detective hat in this film)"""
    base = HER if who == 'her' else ME
    o = dict(base, view='front', noShadow=True, noLegs=True, boilKey=key, aL=-1.6, aR=-1.6)
    o.update(dict(happy=dict(eyes='happy', mouth='smile', blush=.5), love=dict(eyes='heart', mouth='cat', blush=.8),
                  plain=dict(eyes='normal', mouth='smile'), shine=dict(eyes='shine', mouth='cat', blush=.4),
                  cool=dict(eyes='narrow', mouth='smirk')).get(face, {}))
    if who == 'her':
        o['hat'] = 'flower'
    G.c.save()
    clawd(x, y + r * (1.12 if who == 'her' else .95), r / (5.7 if who == 'her' else 5.2), o)
    G.c.restore()


wx.miniHead2 = miniHead2
CLOCK = ['10:24']          # phone status-bar clock (S01 morning, S16 evening)
_statusBar0 = wx.statusBar
wx.statusBar = lambda sx, sy, sw_, clock=None: _statusBar0(sx, sy, sw_, CLOCK[0])

_hat0 = CL.hat


def _hat2(u, h, sw, o=None):
    if h == 'beret':
        P = ellPts(.5 * u, -8.25 * u, 4.1 * u, 1.55 * u, 26, 0, .1)
        paint(P, wash='#C8324A', fill='#8E1F33', fillOp=70, ink=INK, sw=sw * .8)
        inkLine([[.9 * u, -9.6 * u], [1.3 * u, -10.4 * u]], sw * 1.3, INK, 'ink', 0)
    elif h == 'babyflower':
        CL.flowerAt(-2.3 * u, -8.5 * u, u, sw, .8)
    else:
        _hat0(u, h, sw, o)


CL.hat = _hat2


def apronHook(view='front', flip=False):
    """his shop apron (waist panel + pocket + straps), drawn in body-local coords; stays below the mouth.
    flip=True when the character is drawn flipped (keeps the 「橘」 label readable)"""
    def h(u, sw):
        V = CL.VIEWS[view]
        L, R = V['L'] * u, V['R'] * u
        y0, y1 = -3.7 * u, -1.7 * u
        boilSeed('apron')
        paint(rectPts(L + .45 * u, y0, R - L - .9 * u, y1 - y0, u * .05), wash='#FFF6E6', fill='#E8D9BE', fillOp=70, ink=INK, sw=sw * .7)
        inkLine([[L + .25 * u, y0], [R - .25 * u, y0]], sw * 1.1, '#E07A4E', 'ink', 0)
        cx = V['face']['cx'] * u if V.get('face') else 0
        paint(rectPts(cx - 1.25 * u, -3.15 * u, 2.5 * u, 1.0 * u), wash='#F7E7CC', ink=INK, sw=sw * .45)
        push()
        translate(cx, -2.62 * u)
        if flip:
            scale(-1, 1)
        text('橘', 0, 0, u * .72, '#E07A4E', shadow=False)
        pop()
        xs = [L + 1.15 * u, R - 1.15 * u] if view == 'front' else ([-1.9 * u] if view == 'q' else [])
        for x in xs:
            inkLine([[x, y0], [x, -7.95 * u]], sw * 1.0, '#E8D9BE', 'ink', 0)
    return h


def strapHook(view='front', col='#3F6FB5'):
    def h(u, sw):
        xs = [-3.9 * u, 3.9 * u] if view == 'front' else ([-1.7 * u] if view == 'q' else ([.2 * u] if view == 'side' else []))
        for x in xs:
            inkLine([[x, -7.95 * u], [x, -3.3 * u]], sw * 1.6, col, 'ink', 0)
    return h


def hooks(*hs):
    hs = [h for h in hs if h]

    def h(u, sw):
        for f in hs:
            f(u, sw)
    return h


def backpack(x, y, u, o, col='#4A90D9', key='bp'):
    """drawn BEFORE the character (world coords): the bag on the character's back"""
    view = o.get('view') or 'front'
    d = -1 if o.get('flip') else 1
    x += (o.get('dx', 0) or 0) * u
    y += (o.get('dy', 0) or 0) * u
    boilSeed(key)
    if view == 'front':
        paint(rrPts(x - 5.7 * u, y - 8.5 * u, 11.4 * u, 5.8 * u, 1.2 * u), wash=col, fill=mixCol(col, INK, .3), fillOp=70, ink=INK, sw=1)
        return
    if view == 'side':
        bx = x - d * 4.3 * u
    else:
        bx = x - d * 5.6 * u
    paint(rrPts(bx - 1.6 * u, y - 7.9 * u, 3.2 * u, 5.4 * u, .9 * u), wash=col, fill=mixCol(col, INK, .3), fillOp=70, ink=INK, sw=1)
    paint(rrPts(bx - 1.3 * u, y - 5.0 * u, 2.6 * u, 1.8 * u, .5 * u), wash=mixCol(col, '#FFFFFF', .25), ink=INK, sw=.6)
    paint(ellPts(bx, y - 8.4 * u, 1.3 * u, .55 * u, 14), wash='#E86A5A', ink=INK, sw=.6)       # rolled mat on top


# ------------------------------------------------------------------ the general store (one wide world, cameras frame parts of it)
def calendar11(x, y, s=1.0, key='cal'):
    """wall calendar, November; the 1st (today) has a red heart"""
    boilSeed(key)
    w, h = 170 * s, 196 * s
    paint(rectPts(x - w / 2, y, w, h), wash='#FFFDF6', ink=INK, sw=.8)
    paint(rectPts(x - w / 2, y, w, 48 * s), wash='#D8546A', ink=INK, sw=.6)
    text('11月', x, y + 25 * s, 30 * s, '#FFF6E8', face=WENKAI, shadow=False)
    G.c.drawCircle(x, y - 6 * s, 6 * s, _pa(INK))
    for r in range(5):
        for c_ in range(7):
            cx, cy = x - w / 2 + 16 * s + c_ * 23 * s, y + 66 * s + r * 26 * s
            if r == 0 and c_ == 6:
                paint(heartPts(cx, cy, 13 * s, 16), wash='#E0414F', ink=INK, sw=.5)
            else:
                G.c.drawCircle(cx, cy, 2.6 * s, _pa('#8A7A88', .7))


def shopWall(t, lights=1.0, key='shop', mapK=0.0, mapRoute=0.0, clockMin=24, plaque=True):
    flatRect(-500, -400, W + 1000, 1010, '#F6E5C8')
    for i in range(-6, 32):
        flatRect(i * 80, -400, 40, 1010, '#F1DAB8', .55)
    # wainscot
    flatRect(-500, 600, W + 1000, 270, WOOD)
    for i in range(-6, 32):
        line(i * 110, 612, i * 110, 860, WOODDK, .7, 3)
    flatRect(-500, 592, W + 1000, 16, WOODLT)
    line(-500, 600, W + 500, 600, INK, 1, 3)
    # floor planks
    flatRect(-500, 860, W + 1000, 700, '#B67E52')
    for r in range(6):
        y = 860 + r * 46
        line(-500, y, W + 500, y, '#8E5C38', .7, 2)
        for c_ in range(-4, 24):
            x = c_ * 260 + (r % 2) * 130
            line(x, y, x, y + 46, '#8E5C38', .5, 2)
    line(-500, 860, W + 500, 860, INK, 1, 3)
    # string lights along the top
    stringLights([[-420, 30], [0, 92], [420, 36], [840, 96], [1260, 36], [1680, 96], [2100, 36], [2420, 90]], t, on=lights, key=key + 'sl')
    # left shelves (two boards with jars, snack boxes, plants)
    shelves(t, -330, 560, key + 'sh')
    # the sign plaque over the shelves
    if plaque:
        boilSeed(key + 'sign')
        for sx in (140, 420):
            line(sx, 72, sx, 128, '#6B4A33', 1, 3)
        paint(rrPts(60, 120, 440, 110, 16), wash='#8E5E3A', fill='#6B4A33', fillOp=60, ink=INK, sw=1.2)
        paint(rrPts(76, 134, 408, 82, 10), ink='#E9C08A', sw=1.5)
        text('小橘杂货铺', 280, 175, 56, '#FFE3B0', shadow=False)
    # rolled / unrolled map poster in the middle of the wall
    mapPoster(900, 120, 620, 240, mapK, mapRoute, key + 'map')
    # clock + calendar right of the map
    wallClock2(1340, 215, 58, 10, clockMin, key=key + 'clk')
    calendar11(1340, 315, .85, key=key + 'cal')
    # door (closed) + bell; S04 / S09 draw their own door state on top when needed
    plant(-120, 860, 1.2, key=key + 'pl')


def shelves(t, x0, x1, key='sh'):
    boilSeed(key)
    for j, sy in enumerate((330, 520)):
        paint(rectPts(x0, sy, x1 - x0, 22), wash=WOODDK, ink=INK, sw=.9)
        n = int((x1 - x0) / 96)
        for q in range(n):
            jx = x0 + 52 + q * 96
            kind = (q * 3 + j * 5) % 5
            boilSeed(f'{key}{j}{q}')
            if kind == 0:      # candy jar with a lid
                paint(rrPts(jx - 30, sy - 86, 60, 86, 14), wash='#F7E9DA', ink=INK, sw=.7)
                for b_ in range(6):
                    G.c.drawCircle(jx - 16 + (b_ % 3) * 16, sy - 22 - (b_ // 3) * 18, 8,
                                   _pa(['#FF8FB0', '#FFD36A', '#8FD3FF', '#B8F0A0'][(b_ + q) % 4]))
                flatRect(jx - 32, sy - 96, 64, 14, '#D9573E')
            elif kind == 1:    # snack box
                col = ['#F7A35C', '#7CC3E8', '#F28CB1'][(q + j) % 3]
                paint(rectPts(jx - 34, sy - 104, 68, 104), wash=col, fill=mixCol(col, INK, .25), fillOp=60, ink=INK, sw=.7)
                paint(ellPts(jx, sy - 60, 20, 14, 12), wash='#FFFDF6', ink=None)
                G.c.drawCircle(jx, sy - 60, 6, _pa(INK))
            elif kind == 2:    # potted plant
                paint([[jx - 24, sy], [jx + 24, sy], [jx + 18, sy - 40], [jx - 18, sy - 40]], wash='#D9774E', ink=INK, sw=.7)
                for lf in range(5):
                    a = -math.pi / 2 + (lf - 2) * .45
                    paint(ellPts(jx + math.cos(a) * 24, sy - 62 + math.sin(a) * 16, 9, 24, 8, 0, a + math.pi / 2), wash='#7CC36B', ink=INK, sw=.4)
            elif kind == 3:    # stacked tins
                for s_ in range(2):
                    paint(rrPts(jx - 26, sy - 44 - s_ * 44, 52, 44, 6), wash=['#E8C35A', '#9AD0B8'][s_], ink=INK, sw=.6)
                    line(jx - 26, sy - 22 - s_ * 44, jx + 26, sy - 22 - s_ * 44, INK, .4, 2)
            else:              # bottles
                for s_ in range(2):
                    bx = jx - 14 + s_ * 28
                    paint(rrPts(bx - 11, sy - 76, 22, 76, 7), wash=['#9FD8C8', '#F5B7C8'][s_], ink=INK, sw=.6)
                    flatRect(bx - 5, sy - 88, 10, 14, '#6B4A33')
            line(jx - 22, sy + 6, jx + 22, sy + 6, '#FFFDF6', .9, 6)     # price tag strip
            text(f'{(q * 7 + j * 3) % 9 + 1}元', jx, sy + 12, 16, '#B04A2E', shadow=False)


def mapPoster(cx, top, w, h, k, route=0.0, key='map'):
    """a world map that unrolls downward from a wooden rod (k 0..1); route draws a red dotted line 东 ↔ 西"""
    boilSeed(key + 'rod')
    hh = h * easeOut(clamp(k))
    if hh > 6:
        paint(rectPts(cx - w / 2, top + 10, w, hh), wash='#F4E7C6', fill='#E3CFA0', fillOp=60, ink=INK, sw=.9)
        G.c.save()
        G.c.clipRect(skia.Rect.MakeXYWH(cx - w / 2, top + 10, w, hh))
        # sea + continents (made-up blobs)
        flatRect(cx - w / 2 + 14, top + 24, w - 28, h - 28, '#BFE3F5', .9)
        for i, (px, py, rx, ry) in enumerate([(-.3, .38, .16, .22), (-.05, .55, .11, .2), (.22, .35, .2, .17), (.32, .7, .08, .1), (-.38, .75, .06, .08)]):
            boilSeed(f'{key}c{i}')
            paint(ellPts(cx + px * w, top + py * h, rx * w, ry * h, 18, 6), wash='#A6D68A', fill='#7CB86A', fillOp=60, ink=INK, sw=.5)
        text('东', cx + w * .44, top + h * .5, 40, EAST, shadow=False)
        text('西', cx - w * .44, top + h * .5, 40, WEST, shadow=False)
        if route > 0:
            pts = [[cx - w * .36, top + h * .55], [cx - w * .1, top + h * .3], [cx + w * .14, top + h * .62], [cx + w * .36, top + h * .45]]
            P = through(pts, 12)
            n = int(len(P) * clamp(route))
            for i in range(0, n, 2):
                G.c.drawCircle(P[i][0], P[i][1], 6, _pa('#E8476E'))
            if n > 2:
                heart(P[n - 1][0], P[n - 1][1] - 4, 16, HOT, key=key + 'rh', sw=.5, shine=False)
        G.c.restore()
    boilSeed(key + 'rod2')
    paint(rrPts(cx - w / 2 - 30, top, w + 60, 22, 10), wash=WOODDK, ink=INK, sw=.9)
    if hh > 6:
        paint(rrPts(cx - w / 2 - 20, top + 6 + hh, w + 40, 18, 8), wash=WOODDK, ink=INK, sw=.8)
    else:     # rolled tube
        paint(rrPts(cx - w / 2 - 10, top + 12, w + 20, 34, 16), wash='#F4E7C6', fill='#E3CFA0', fillOp=80, ink=INK, sw=.9)
        line(cx - 30, top + 46, cx - 30, top + 74, '#E8476E', 1, 3)
        line(cx + 30, top + 46, cx + 30, top + 74, '#E8476E', 1, 3)


def counterFront(x0, x1, top, key='ctr', bottom=880):
    """the shop counter seen from the front (draw AFTER the person behind it: it hides the legs)"""
    boilSeed(key)
    paint(rectPts(x0, top + 16, x1 - x0, bottom - top - 16), wash=WOOD, fill=WOODDK, fillOp=60, ink=INK, sw=1.1)
    n = max(2, int((x1 - x0) / 120))
    for i in range(1, n):
        x = x0 + (x1 - x0) * i / n
        line(x, top + 30, x, bottom - 6, WOODDK, .8, 3)
    paint(rectPts(x0 - 24, top, x1 - x0 + 48, 24, 3), wash=WOODLT, fill=WOOD, fillOp=60, ink=INK, sw=1.0)
    # little front sign
    paint(rrPts((x0 + x1) / 2 - 90, top + 60, 180, 64, 10), wash='#FFF5E2', ink=INK, sw=.7)
    text('欢迎选购', (x0 + x1) / 2, top + 92, 34, '#B04A2E', shadow=False)


def deskBell(x, y, s, ring=0.0, key='db'):
    boilSeed(key)
    paint(ellPts(x, y, s * 1.1, s * .25, 16), wash='#6B6880', ink=INK, sw=.6)
    paint([[x - s, y - 2]] + [[x + math.cos(math.pi + i / 12 * math.pi) * s * .9, y - 4 + math.sin(math.pi + i / 12 * math.pi) * s * .9] for i in range(13)],
          wash='#E8E4EC', fill='#B8B4C8', fillOp=70, ink=INK, sw=.7)
    G.c.drawCircle(x, y - s * .95, s * .16, _pa(INK))
    if ring > .02:
        for i in range(3):
            a = -math.pi / 2 + (i - 1) * .7
            line(x + math.cos(a) * s * 1.3, y - s * .5 + math.sin(a) * s * 1.3, x + math.cos(a) * s * 1.8, y - s * .5 + math.sin(a) * s * 1.8,
                 INK, ring, 3)


def phoneFlat(x, y, s, lit=0.0, buzz=0.0, key='pf'):
    """a phone lying on the counter, seen from the front (a thin slab with a glow)"""
    jx = math.sin(G.T * 90) * 4 * buzz
    boilSeed(key)
    paint(rrPts(x - s + jx, y - s * .22, 2 * s, s * .22, 4), wash='#3D3A52', ink=INK, sw=.7)
    if lit > .02:
        glow(x + jx, y - s * .3, s * 1.4, '#BFF5D0', .6 * lit)
    if buzz > .05:
        for d in (-1, 1):
            for i in range(2):
                xx = x + d * (s * 1.15 + i * 16)
                line(xx, y - s * .5, xx + d * 8, y - s * .1, INK, buzz, 3)


def candyJarTop(x, y, s, key='cj'):
    boilSeed(key)
    paint(rrPts(x - s, y - s * 2.2, 2 * s, s * 2.2, s * .4), wash='#F7E9DA', ink=INK, sw=.7)
    for b_ in range(7):
        G.c.drawCircle(x - s * .55 + (b_ % 3) * s * .55, y - s * .45 - (b_ // 3) * s * .5, s * .26, _pa(['#FF8FB0', '#FFD36A', '#8FD3FF', '#B8F0A0'][b_ % 4]))
    flatRect(x - s * 1.05, y - s * 2.45, s * 2.1, s * .35, '#D9573E')


def counterItems(x0, top, t, key='ci', bell=0.0):
    """things standing on the counter top (left part)"""
    candyJarTop(x0 + 70, top + 4, 34, key + 'j')
    deskBell(x0 + 190, top + 6, 30, bell, key + 'b')
    boilSeed(key + 'cac')
    paint([[x0 + 260, top + 4], [x0 + 300, top + 4], [x0 + 296, top - 26], [x0 + 264, top - 26]], wash='#D9774E', ink=INK, sw=.6)
    paint(rrPts(x0 + 266, top - 74, 28, 52, 12), wash='#7CC36B', fill='#5A9E4E', fillOp=60, ink=INK, sw=.6)
    paint(rrPts(x0 + 248, top - 56, 18, 26, 8), wash='#7CC36B', ink=INK, sw=.5)


# ------------------------------------------------------------------ door (S04 / S09 / S12)
def outsideDay(x0, y0, x1, y1, key='out'):
    """what's outside the open door: sky, a tree, the sidewalk (bright, warm)"""
    G.c.save()
    G.c.clipRect(skia.Rect.MakeLTRB(x0, y0, x1, y1))
    gradRect(x0, y0, x1 - x0, y1 - y0, ['#CFEFFF', '#FFF4D6'])
    tree(x0 + (x1 - x0) * .7, y1 - 120, 52, key=key + 't')
    flatRect(x0, y1 - 120, x1 - x0, 120, '#E9DCC6')
    line(x0, y1 - 120, x1, y1 - 120, INK, .8, 2)
    glow((x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) * 1.2, '#FFF4C8', .5)
    G.c.restore()


def shopDoor(t, x0=1480, x1=1820, top=270, bottom=860, opn=0.0, sign='营业中', signFlip=None, bell=0.0, key='door', outside=True):
    """wooden door, hinge on the right; opn 0..1 swings it open (the panel narrows toward the hinge, outside shows)"""
    if outside:
        outsideDay(x0, top, x1, bottom, key + 'o')
    boilSeed(key + 'fr')
    w = (x1 - x0) * (1 - .78 * ease(clamp(opn)))
    px0 = x1 - w
    skew = 40 * ease(clamp(opn))
    if not outside or opn < .02:
        flatRect(x0, top, x1 - x0, bottom - top, '#5E3E26')
    pts = [[px0, top - skew * .2], [x1, top], [x1, bottom], [px0, bottom + skew * .2]]
    paint(pts, wash='#9A6640', fill='#7A4E30', fillOp=60, ink=INK, sw=1.1)
    if w > 80:
        ix = lambda f: px0 + (x1 - px0) * f
        paint([[ix(.14), top + 50], [ix(.86), top + 50], [ix(.86), top + 260], [ix(.14), top + 260]], wash='#A8764E', ink=INK, sw=.7)
        paint([[ix(.14), top + 300], [ix(.86), top + 300], [ix(.86), bottom - 50], [ix(.14), bottom - 50]], wash='#A8764E', ink=INK, sw=.7)
        G.c.drawCircle(ix(.12), top + 290, 11, _pa(BRASS))
        G.c.drawCircle(ix(.12), top + 290, 11, _pa(INK, 1, 2))
        if sign:
            doorSign(ix(.5), top + 150, (x1 - px0) / (x1 - x0), sign, signFlip, t, key + 's')
    # frame
    boilSeed(key + 'fr2')
    paint(rectPts(x0 - 26, top - 30, 26, bottom - top + 30), wash=WOODDK, ink=INK, sw=.9)
    paint(rectPts(x1, top - 30, 26, bottom - top + 30), wash=WOODDK, ink=INK, sw=.9)
    paint(rectPts(x0 - 40, top - 52, x1 - x0 + 80, 30), wash=WOODDK, ink=INK, sw=.9)
    doorBell(x0 + 10, top - 4, 30, bell, key + 'bell')


def doorSign(x, y, sx, sign, flip, t, key='ds'):
    """hanging card on the door; flip = (t0, newText): it spins on its string and lands on the beat"""
    txt, fk = sign, 1.0
    if flip:
        t0, new = flip
        a = t - (t0 - .16)
        if a > 0:
            p = clamp(a / .16)
            fk = abs(math.cos(p * math.pi))
            txt = new if p > .5 else sign
    line(x - 40 * sx, y - 70, x, y - 100, INK, 1, 2)
    line(x + 40 * sx, y - 70, x, y - 100, INK, 1, 2)
    G.c.drawCircle(x, y - 100, 6, _pa(BRASS))
    push()
    translate(x, y)
    scale(max(.04, sx * fk), 1)
    boilSeed(key)
    big = txt != '营业中'
    paint(rrPts(-82, -66, 164, 132, 14), wash='#FFF5E2' if not big else '#FFE36E', ink=INK, sw=.9)
    if big:
        text('去旅行', 0, -20, 40, '#D9573E', shadow=False)
        text('啦～', 0, 28, 40, '#D9573E', shadow=False)
    else:
        text(txt, 0, 0, 42, '#3F8C55', shadow=False)
    pop()


def doormat(x, y, w, key='mat'):
    boilSeed(key)
    paint([[x - w / 2 + 20, y - 18], [x + w / 2 - 20, y - 18], [x + w / 2, y + 18], [x - w / 2, y + 18]], wash='#C9534A', fill='#9E3B34', fillOp=60, ink=INK, sw=.8)
    text('欢 迎', x, y, 26, '#FFE3B0', shadow=False)


def parcel(x, y, s, lid=0.0, key='parcel', rot=0.0):
    """kraft parcel with a red ribbon, (x, y) = bottom centre; lid 0..1 lifts the lid off"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-s, -1.4 * s, 2 * s, 1.4 * s), wash='#D9B07A', fill='#B8895A', fillOp=60, ink=INK, sw=.9)
    flatRect(-s * .14, -1.4 * s, s * .28, 1.4 * s, '#E8476E')
    if lid < .98:
        ly = -1.4 * s - 140 * ease(lid)
        push()
        translate(0, ly)
        rotate(-.6 * ease(lid))
        paint(rectPts(-1.08 * s, -.32 * s, 2.16 * s, .34 * s), wash='#E3BE88', fill='#B8895A', fillOp=60, ink=INK, sw=.9)
        flatRect(-s * .14, -.32 * s, s * .28, .34 * s, '#E8476E')
        if lid < .05:
            for d in (-1, 1):
                paint(ellPts(d * .32 * s, -.5 * s, .32 * s, .2 * s, 12, 0, d * .5), wash='#FF6F96', ink=INK, sw=.6)
        pop()
    pop()


# ------------------------------------------------------------------ the compass (the 「东西」 in the parcel)
def compass(x, y, r, ang, t, key='cmp', lit=None, spinBlur=0.0, shine=0.0, tilt=1.0):
    """brass compass seen from above (tilt < 1 squashes it into perspective). Only 东 (right) and 西 (left);
    hearts at the top / bottom. ang = needle angle (0 points to 东, pi to 西). lit = ('东'|'西', k) glow."""
    push()
    translate(x, y)
    scale(1, tilt)
    boilSeed(key)
    G.c.drawCircle(10, 14, r * 1.02, _pa(INK, .22))
    paint(ellPts(0, 0, r, r, 48), wash=BRASS, fill=BRASSDK, fillOp=80, ink=INK, sw=1.4)
    paint(ellPts(0, 0, r * .86, r * .86, 44), wash='#FFF8E6', fill='#EFE0C0', fillOp=50, ink=INK, sw=.9)
    for i in range(36):
        a = i / 36 * TAU
        L = .1 if i % 9 == 0 else (.06 if i % 3 == 0 else .03)
        line(math.cos(a) * r * .84, math.sin(a) * r * .84, math.cos(a) * r * (.84 - L), math.sin(a) * r * (.84 - L), INK, .8, 2.4 if i % 9 == 0 else 1.4)
    # rose star
    paint(starPts(0, 0, r * .62, .2, 4, 0), wash='#F2E3C2', fill='#D9C59A', fillOp=60, ink=INK, sw=.6)
    for lab, a, col in (('东', 0, EAST), ('西', math.pi, WEST)):
        lx, ly = math.cos(a) * r * .62, math.sin(a) * r * .62
        if lit and lit[0] == lab and lit[1] > .02:
            glow(lx, ly, r * .5, '#FFE36E', lit[1])
            G.c.drawCircle(lx, ly, r * .17 * (1 + .15 * lit[1]), _pa('#FFE36E', .85 * lit[1]))
        text(lab, lx, ly, r * .24, col, stroke='#FFF8E6', strokeW=r * .03, shadow=False)
    heart(0, -r * .64, r * .085, HOT, key=key + 'hn', sw=.5, shine=False)
    heart(0, r * .64, r * .085, '#FF9FBA', key=key + 'hs', sw=.5, shine=False)
    # needle
    if spinBlur > .05:
        for i in range(10):
            a = ang - i * .16 * spinBlur
            G.c.save()
            G.c.rotate(math.degrees(a))
            flat([[r * .66, 0], [0, r * .06], [-r * .5, 0], [0, -r * .06]], '#E8574A', .12 * (1 - i / 10))
            G.c.restore()
    G.c.save()
    G.c.rotate(math.degrees(ang))
    boilSeed(key + 'nd')
    paint([[r * .7, 0], [0, r * .085], [0, -r * .085]], wash='#E8574A', fill='#B8323A', fillOp=70, ink=INK, sw=.8)
    paint([[-r * .52, 0], [0, r * .085], [0, -r * .085]], wash='#3F4A6E', ink=INK, sw=.8)
    G.c.restore()
    paint(ellPts(0, 0, r * .07, r * .07, 14), wash=BRASSLT, ink=INK, sw=.7)
    if shine > .02:
        paint(ellPts(-r * .35, -r * .42, r * .22, r * .1, 14, 0, -.6), wash='#FFFFFF', washOp=int(150 * shine), ink=None)
    pop()


# ------------------------------------------------------------------ the daydream sets
def bambooCopter(x, y, s, t, spin=1.0, key='bc', basket=True, people=None):
    """giant bamboo-dragonfly toy: stick from the basket top (x, y) up 7s, two blades spinning on top.
    people(bx, rim) draws whoever sits in the basket (between the basket's back and front)."""
    top = y - 7 * s
    boilSeed(key + 'st')
    paint(rrPts(x - .22 * s, top, .44 * s, 7 * s, .15 * s), wash='#C8A46A', fill='#9C7A44', fillOp=60, ink=INK, sw=1)
    for i in range(1, 4):
        line(x - .22 * s, top + i * 1.75 * s, x + .22 * s, top + i * 1.75 * s, '#8A6A3A', 1, 3)
    ph = t * 26 * spin
    # blur disc
    if spin > .3:
        paint(ellPts(x, top, 6.4 * s, .9 * s, 30), wash='#F3E6C4', washOp=int(90 * min(1, spin)), ink=None)
    for k_ in range(2):
        a = ph + k_ * math.pi
        c = math.cos(a)
        L = 6.2 * s * c
        boilSeed(f'{key}b{k_}')
        paint([[x, top - .2 * s], [x + L, top - .55 * s - .25 * s * math.sin(a)], [x + L * .96, top + .1 * s], [x, top + .25 * s]],
              wash='#E7C98C', fill='#B8935A', fillOp=60, ink=INK, sw=.9, curv=.2)
    paint(ellPts(x, top, .55 * s, .4 * s, 14), wash='#9C7A44', ink=INK, sw=.8)
    if not basket:
        return
    if basket == 'swing':          # a plank swing seat: they sit on it, legs dangling
        pw = 15 * s
        py = y + 3.0 * s
        for d in (-1, 1):
            line(x, y, x + d * pw * .47, py, '#8A6A3A', 1, 3)
        boilSeed(key + 'pl')
        paint(rrPts(x - pw / 2, py, pw, .55 * s, .2 * s), wash='#C99A5C', fill='#9C7240', fillOp=70, ink=INK, sw=1.1)
        for d in (-1, 1):
            G.c.drawCircle(x + d * pw * .47, py + .25 * s, .18 * s, _pa('#6B4A33'))
        if people:
            people(x, py)
        return
    bw = 15 * s
    rim = y + 2.2 * s
    for d in (-1, 1):
        line(x, y, x + d * bw * .46, rim, '#8A6A3A', 1, 3)
    boilSeed(key + 'bk')
    paint(ellPts(x, rim, bw / 2, .7 * s, 24), wash='#8A6236', ink=INK, sw=.8)
    if people:
        people(x, rim)
    boilSeed(key + 'bf')
    paint([[x - bw / 2, rim], [x + bw / 2, rim], [x + bw * .42, rim + 3.4 * s], [x - bw * .42, rim + 3.4 * s]], wash='#C99A5C', fill='#9C7240', fillOp=70,
          ink=INK, sw=1.1)
    for i in range(1, 7):
        xx = x - bw / 2 + bw * i / 7
        line(xx, rim + 4, xx - (xx - x) * .16, rim + 3.4 * s - 4, '#8A6236', .9, 2.5)
    for j in range(1, 3):
        yy = rim + j * 1.13 * s
        f = 1 - .16 * j * 1.13 / 3.4
        line(x - bw / 2 * f, yy, x + bw / 2 * f, yy, '#8A6236', .9, 2.5)
    paint(ellPts(x, rim, bw / 2, .7 * s, 24), ink=INK, sw=1.0)


def eiffel(x, y, h, lights=0.0, t=0.0, key='eif', col='#5A4A72'):
    """a simple lattice tower silhouette (base centre (x, y), height h)"""
    boilSeed(key)
    w = h * .42
    L = lambda f: x - w / 2 * (1 - f) ** 1.6 - h * .012
    R = lambda f: x + w / 2 * (1 - f) ** 1.6 + h * .012
    pts = []
    for i in range(13):
        f = i / 12 * .96
        pts.append([L(f), y - h * f])
    pts.append([x, y - h])
    for i in range(12, -1, -1):
        f = i / 12 * .96
        pts.append([R(f), y - h * f])
    paint(pts, wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=1.0)
    # arch at the base
    paint(ellPts(x, y, w * .26, h * .14, 20), wash='#F3D9E0', ink=None)
    flatRect(x - w * .3, y, w * .6, h * .15, '#F3D9E0')
    # platforms
    for f in (.17, .42):
        paint(rectPts(L(f) - h * .02, y - h * f - h * .015, R(f) - L(f) + h * .04, h * .03), wash=mixCol(col, '#FFFFFF', .2), ink=INK, sw=.6)
    # lattice
    for i in range(14):
        f0, f1 = i / 14 * .9, (i + 1) / 14 * .9
        line(L(f0), y - h * f0, R(f1), y - h * f1, mixCol(col, '#FFFFFF', .35), .8, 1.6)
        line(R(f0), y - h * f0, L(f1), y - h * f1, mixCol(col, '#FFFFFF', .35), .8, 1.6)
    if lights > .02:
        for i in range(26):
            f = hash1(i * 3.3) * .92
            side = L(f) if i % 2 else R(f)
            px = lerp(side, x, hash1(i * 7.1) * .8)
            tw = .5 + .5 * math.sin(t * 9 + i * 2.1)
            G.c.drawCircle(px, y - h * f, 4 + 2 * tw, _pa('#FFE9A0', lights * (.5 + .5 * tw)))
        glow(x, y - h * .5, h * .55, '#FFD98A', .35 * lights)
        G.c.drawCircle(x, y - h - 6, 7, _pa('#FFF4C8', lights))


def awning(x0, x1, y, depth=70, key='aw', cols=('#E8574A', '#FFF5E2')):
    boilSeed(key)
    n = int((x1 - x0) / 60)
    for i in range(n):
        xa = x0 + (x1 - x0) * i / n
        xb = x0 + (x1 - x0) * (i + 1) / n
        flat([[xa, y], [xb, y], [xb, y + depth], [xa, y + depth]], cols[i % 2])
        paint(ellPts((xa + xb) / 2, y + depth, (xb - xa) / 2, 16, 12), wash=cols[i % 2], ink=None)
    inkLine([[x0, y], [x1, y]], 1.2, INK, 'ink', 0)
    paint(rectPts(x0, y, x1 - x0, depth), ink=INK, sw=.9)


def baguette(x, y, L, ang, key='bag'):
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    paint(ellPts(0, 0, L / 2, L * .09, 20), wash='#E3A65A', fill='#B8783A', fillOp=70, ink=INK, sw=.8)
    for i in range(4):
        xx = -L * .3 + i * L * .2
        inkLine([[xx - L * .05, -L * .04], [xx + L * .05, L * .02]], .6, '#8E5A2A', 'ink', 0)
    pop()


def baby(x, y, u, who, t, k=1.0, face='happy', key='bb', flip=False, hop=0.0):
    """a tiny Clawd baby popping out of the ground (k 0..1 pop-in), (x, y) = feet"""
    if k <= .01:
        return
    p = backOut(k)
    o = dict(HER if who == 'her' else ME)
    o.update(view='front', boilKey=key, eyes='happy' if face == 'happy' else face, mouth='smile', blush=.8, flip=flip,
             aL=.9 + .4 * math.sin(t * 9 + len(key)), aR=.9 - .4 * math.sin(t * 9 + len(key)), dy=-hop)
    if who == 'her':
        o['hat'] = 'babyflower'
    push()
    translate(x, y)
    scale(p, p)
    translate(-x, -y)
    clawd(x, y, u, o)
    pop()


def picnicBlanket(cx, cy, w, h, key='pic'):
    boilSeed(key)
    paint([[cx - w / 2 + 40, cy - h / 2], [cx + w / 2 - 40, cy - h / 2], [cx + w / 2, cy + h / 2], [cx - w / 2, cy + h / 2]], wash='#FFFDF6', ink=INK, sw=1)
    n = 8
    for i in range(n):
        f0, f1 = i / n, (i + 1) / n
        if i % 2 == 0:
            xa0 = lerp(cx - w / 2 + 40, cx + w / 2 - 40, f0)
            xa1 = lerp(cx - w / 2 + 40, cx + w / 2 - 40, f1)
            xb0 = lerp(cx - w / 2, cx + w / 2, f0)
            xb1 = lerp(cx - w / 2, cx + w / 2, f1)
            flat([[xa0, cy - h / 2], [xa1, cy - h / 2], [xb1, cy + h / 2], [xb0, cy + h / 2]], '#F28CA8', .55)
    for j in range(3):
        yy = cy - h / 2 + h * (j * 2 + 1) / 6
        flatRect(cx - w / 2, yy - h / 12, w, h / 6, '#F28CA8', .35)


# ------------------------------------------------------------------ chorus props
def balance(x, y, s, ang, key='bal', loadL='东', loadR='西'):
    """a big balance: pillar base (x, y), pivot at y - 9s; ang tilts the beam (negative = left side down)"""
    py = y - 9 * s
    boilSeed(key + 'base')
    paint([[x - 2.6 * s, y], [x + 2.6 * s, y], [x + 1.6 * s, y - .8 * s], [x - 1.6 * s, y - .8 * s]], wash=BRASS, fill=BRASSDK, fillOp=70, ink=INK, sw=1)
    paint(rectPts(x - .35 * s, py, .7 * s, 9 * s - .8 * s), wash=BRASS, fill=BRASSDK, fillOp=60, ink=INK, sw=1)
    L = 7.2 * s
    ends = []
    for d in (-1, 1):
        ex, ey = x + d * L * math.cos(ang), py + d * L * math.sin(ang)
        ends.append((ex, ey))
    boilSeed(key + 'beam')
    paint(ribbon([[ends[0][0], ends[0][1]], [x, py], [ends[1][0], ends[1][1]]], .45 * s, .45 * s), wash=BRASS, fill=BRASSDK, fillOp=60, ink=INK, sw=1)
    paint(ellPts(x, py, .7 * s, .7 * s, 16), wash=BRASSLT, ink=INK, sw=.8)
    for i, ((ex, ey), lab, col) in enumerate(zip(ends, (loadL, loadR), (EAST, WEST))):
        pan_y = ey + 4.2 * s
        line(ex, ey, ex - 2.2 * s, pan_y, INK, .9, 2.5)
        line(ex, ey, ex + 2.2 * s, pan_y, INK, .9, 2.5)
        boilSeed(f'{key}blk{i}')
        paint(rrPts(ex - 1.5 * s, pan_y - 2.9 * s, 3.0 * s, 2.9 * s, .4 * s), wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=.9)
        text(lab, ex, pan_y - 1.45 * s, 1.9 * s, '#FFFFFF', stroke=INK, strokeW=s * .22, shadow=False)
        boilSeed(f'{key}pan{i}')
        paint([[ex - 2.8 * s, pan_y], [ex + 2.8 * s, pan_y], [ex + 2.0 * s, pan_y + .8 * s], [ex - 2.0 * s, pan_y + .8 * s]], wash=BRASS, fill=BRASSDK,
              fillOp=70, ink=INK, sw=.9)


def signPost(x, y, h, lit=(0.0, 0.0), key='sp'):
    """wooden signpost: top board 东 → (pointing right), lower board ← 西; lit = (east, west) glow 0..1"""
    boilSeed(key)
    paint(rectPts(x - 16, y - h, 32, h), wash=WOODDK, ink=INK, sw=.9)
    for i, (lab, d, yy, col, k) in enumerate((('东', 1, y - h + 40, EAST, lit[0]), ('西', -1, y - h + 150, WEST, lit[1]))):
        boilSeed(f'{key}b{i}')
        x0, x1 = (x - 20, x + 240) if d > 0 else (x - 240, x + 20)
        tip = x1 + 50 if d > 0 else x0 - 50
        pts = [[x0, yy - 40], [x1, yy - 40], [tip, yy], [x1, yy + 40], [x0, yy + 40]] if d > 0 else \
              [[x1, yy - 40], [x0, yy - 40], [tip, yy], [x0, yy + 40], [x1, yy + 40]]
        if k > .02:
            glow((x0 + x1) / 2, yy, 320, '#FFE36E', 1.2 * k)
        paint(pts, wash=mixCol('#F1DDB4', '#FFE36E', k), fill=WOOD, fillOp=50, ink=INK, sw=1)
        if k > .02:
            paint(pts, ink='#FFFFFF', sw=3.2 * k)
        text(lab, (x0 + x1) / 2 + d * 20, yy, 58, col, shadow=False, sc=1 + .2 * k)


def mileSign(x, y, s, txt, k=1.0, key='ms'):
    """roadside milestone popping up from the ground (k 0..1)"""
    if k <= .01:
        return
    p = backOut(k)
    push()
    translate(x, y)
    scale(1, p)
    boilSeed(key)
    paint(rectPts(-.12 * s, -2.4 * s, .24 * s, 2.4 * s), wash='#8E8AA0', ink=INK, sw=.8)
    paint(rrPts(-1.25 * s, -3.6 * s, 2.5 * s, 1.5 * s, .2 * s), wash='#3F8C55', ink=INK, sw=1)
    paint(rrPts(-1.12 * s, -3.48 * s, 2.24 * s, 1.26 * s, .15 * s), ink='#FFFFFF', sw=1.2)
    text(txt, 0, -2.85 * s, .62 * s, '#FFFFFF', shadow=False, face=WENKAI)
    pop()


def plazaRose(cx, cy, rx, ry, t, needle=0.0, litE=0.0, key='pr'):
    """giant compass rose painted on a plaza floor (perspective ellipse); needle angle in ground plane"""
    boilSeed(key)
    paint(ellPts(cx, cy, rx, ry, 64), wash='#E9D8C0', fill='#CDB89A', fillOp=60, ink=INK, sw=1.2)
    paint(ellPts(cx, cy, rx * .88, ry * .88, 60), ink='#A88A66', sw=1.4)
    for i in range(16):
        a = i / 16 * TAU
        r0, r1 = (.62, .86) if i % 4 == 0 else (.74, .86)
        line(cx + math.cos(a) * rx * r0, cy + math.sin(a) * ry * r0, cx + math.cos(a) * rx * r1, cy + math.sin(a) * ry * r1, '#A88A66', 1, 3)
    star = []
    for i in range(16):
        a = i / 16 * TAU
        r = .6 if i % 4 == 0 else (.18 if i % 2 else .3)
        star.append([cx + math.cos(a) * rx * r, cy + math.sin(a) * ry * r])
    paint(star, wash='#F2E3C2', fill='#D9C59A', fillOp=60, ink=INK, sw=.8)
    for lab, a, col, k in (('东', 0, EAST, litE), ('西', math.pi, WEST, 0)):
        lx, ly = cx + math.cos(a) * rx * .75, cy + math.sin(a) * ry * .75
        if k > .02:
            glow(lx, ly, 200, '#FFE36E', k)
        text(lab, lx, ly, 70, col, stroke='#FFF8E6', strokeW=8, shadow=False, sc=1 + .25 * k)
    for a, col in ((-math.pi / 2, HOT), (math.pi / 2, '#FF9FBA')):
        heart(cx + math.cos(a) * rx * .75, cy + math.sin(a) * ry * .75, 22, col, key=key + str(a), sw=.5, shine=False)
    # needle on the ground
    ex, ey = math.cos(needle), math.sin(needle)
    tip = [cx + ex * rx * .55, cy + ey * ry * .55]
    tail = [cx - ex * rx * .4, cy - ey * ry * .4]
    nx, ny = -ey * rx * .05, ex * ry * .05
    boilSeed(key + 'nd')
    paint([tip, [cx + nx, cy + ny], [cx - nx, cy - ny]], wash='#E8574A', ink=INK, sw=.8)
    paint([tail, [cx + nx, cy + ny], [cx - nx, cy - ny]], wash='#3F4A6E', ink=INK, sw=.8)


# ------------------------------------------------------------------ phone on the counter (top view) + chat
PH = dict(cx=960, cy=525, w=600, h=1010)


def counterTop(t, key='ct', extra=None):
    """top-down wooden counter for S01 / S16"""
    flatRect(-400, -400, W + 800, H + 800, '#C9905E')
    for j in range(-6, 22):
        y = j * 92
        flatRect(-400, y, W + 800, 46, '#C08654', .45)
        line(-400, y, W + 400, y, '#9E6A40', .6, 2)
    for i in range(40):
        x, y = hash1(i * 1.7) * W, hash1(i * 2.9) * H
        inkLine([[x, y], [x + 90 + 60 * hash1(i), y + 6 * (hash1(i * 5) - .5)]], .35, '#9E6A40', 'inkfine', .5)
    # receipt (top right)
    boilSeed(key + 'rc')
    push()
    translate(1690, 300)
    rotate(.14)
    paint(rectPts(-105, -150, 210, 300), wash='#FFFDF6', ink=INK, sw=.8)
    text('小橘杂货', 0, -112, 30, INK, shadow=False)
    for q in range(5):
        line(-80, -62 + q * 32, 80, -62 + q * 32, '#C9C1D6', 1, 2)
    text('示例歌词 ×1', 0, 116, 22, HOT, shadow=False, face=WENKAI)
    pop()
    # little cactus pot (top view)
    boilSeed(key + 'cac')
    paint(ellPts(1640, 760, 70, 70, 24), wash='#D9774E', fill='#B85C3A', fillOp=60, ink=INK, sw=1.0)
    paint(ellPts(1640, 760, 52, 52, 22), wash='#7CC36B', fill='#5A9E4E', fillOp=60, ink=INK, sw=.7)
    for i in range(10):
        a = i / 10 * TAU
        line(1640 + math.cos(a) * 18, 760 + math.sin(a) * 18, 1640 + math.cos(a) * 46, 760 + math.sin(a) * 46, '#3F7A3A', .8, 1.6)
    G.c.drawCircle(1640, 760, 12, _pa('#FF8FB0'))
    # coins
    for i, (cx_, cy_) in enumerate(((1460, 900), (1500, 870), (1530, 915))):
        boilSeed(f'{key}co{i}')
        paint(ellPts(cx_, cy_, 26, 26, 16), wash=BRASSLT, fill=BRASS, fillOp=60, ink=INK, sw=.6)
        text('1', cx_, cy_, 20, BRASSDK, shadow=False)
    # keys + keychain (bottom left)
    boilSeed(key + 'key')
    G.c.drawCircle(250, 880, 30, _pa(INK, 1, 3))
    paint(rrPts(270, 860, 120, 30, 10), wash='#C8C4D4', ink=INK, sw=.6)
    paint(starPts(200, 920, 34, .45, 5), wash='#FFD36A', ink=INK, sw=.6)
    # mug (top view) + sticky note, top left
    boilSeed(key + 'mug')
    paint(ellPts(200, 170, 74, 74, 24), wash='#F7F2E8', ink=INK, sw=1)
    paint(ellPts(200, 170, 58, 58, 22), wash='#8E5A3A', fill='#6B4A33', fillOp=60, ink=INK, sw=.6)
    paint(rrPts(266, 150, 40, 40, 14), ink=INK, sw=1.2)
    paint(ellPts(186, 156, 20, 9, 10, 0, -.4), wash='#FFFFFF', washOp=120, ink=None)
    push()
    translate(470, 170)
    rotate(-.08)
    boilSeed(key + 'note')
    paint(rectPts(-90, -80, 180, 160), wash='#FBE7A1', fill='#F2D36E', fillOp=50, ink=INK, sw=.7)
    text('进货清单', 0, -46, 30, '#6A5A40', shadow=False, face=WENKAI)
    for q in range(3):
        line(-62, -6 + q * 30, 62, -6 + q * 30, '#C9A85A', 1, 2)
    text('糖 ×3', -10, -12, 24, '#6A5A40', shadow=False, face=WENKAI)
    pop()
    # pencil
    boilSeed(key + 'pen')
    push()
    translate(560, 900)
    rotate(-.12)
    paint(rectPts(-110, -9, 200, 18), wash='#F2C53D', ink=INK, sw=.6)
    paint([[90, -9], [122, 0], [90, 9]], wash='#F3D9B8', ink=INK, sw=.6)
    paint(rectPts(-128, -9, 18, 18), wash='#FF8FB0', ink=INK, sw=.6)
    pop()
    if extra:
        extra()


def phoneTop(t, page, cx, cy, s, jolt=(0, 0), case='#F7C6D2', key='ph'):
    """the phone lying on the counter (top view), its screen page(sx, sy, sw, sh) drawn in the phone's own coords"""
    push()
    translate(cx + jolt[0], cy + jolt[1])
    scale(s)
    translate(-PH['cx'], -PH['cy'])
    x0, y0, w, h = PH['cx'], PH['cy'], PH['w'], PH['h']
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x0 - w / 2 + 18, y0 - h / 2 + 24, w, h), 70, 70, _pa(INK, .2))
    phoneBody(x0, y0, w, h, key=key, case=case)
    p, (sx, sy, sw_, sh) = screenClip(x0, y0, w, h)
    G.c.save()
    G.c.clipPath(p, skia.ClipOp.kIntersect, True)
    page(sx, sy, sw_, sh)
    G.c.restore()
    pop()


def lockScreen(t, sx, sy, sw_, sh, on=1.0, banner=0.0):
    gradRect(sx, sy, sw_, sh, ['#2C3B7A', '#7A5CA8', '#F29FB5'])
    for i in range(24):
        x, y = sx + hash1(i * 1.3) * sw_, sy + hash1(i * 2.1) * sh * .6
        G.c.drawCircle(x, y, 2 + 2 * hash1(i), _pa('#FFFFFF', .5 + .4 * math.sin(t * 3 + i)))
    text('10:24', sx + sw_ / 2, sy + 250, 130, '#FFFFFF', shadow=False)
    text('11月1日 星期日', sx + sw_ / 2, sy + 345, 34, '#FFFFFF', shadow=False, face=WENKAI)
    # a little compass on the wallpaper
    compass(sx + sw_ / 2, sy + sh - 230, 90, -math.pi / 2 + .2 * math.sin(t * 2), t, key='lscmp', tilt=1.0)
    if banner > .01:
        p = backOut(banner)
        by = sy + 420 - 120 * (1 - p)
        push()
        G.c.saveLayerAlpha(None, int(255 * clamp(banner * 2)))
        boilSeed('lsban')
        paint(rrPts(sx + 22, by, sw_ - 44, 140, 26), wash='#FFFFFF', washOp=235, ink=INK, sw=.8)
        wx.avatarBox(sx + 86, by + 70, 40, 'her', 'happy', key='lsav')
        text(HERNAME, sx + 146, by + 46, 34, INK, align='left', shadow=False)
        text('[4条] 示例歌词占位文…', sx + 146, by + 98, 30, '#6A5A70', align='left', shadow=False, face=WENKAI)
        G.c.restore()
        pop()
    if on < 1:
        flatRect(sx, sy, sw_, sh, '#14121C', 1 - on)


def badge(x, y, n, k=1.0, key='bd'):
    if k <= .01:
        return
    p = backOut(k)
    push()
    translate(x, y)
    scale(p)
    G.c.drawCircle(0, 0, 26, _pa('#E8394E'))
    G.c.drawCircle(0, 0, 26, _pa(INK, 1, 2.5))
    text(str(n), 0, 0, 30, '#FFFFFF', shadow=False)
    pop()


def heartSticker(x, y, k, key='hst'):
    if k <= .02:
        return
    push()
    translate(x, y)
    scale(backOut(k))
    rotate(.06)
    boilSeed(key)
    paint(rrPts(-95, -95, 190, 190, 28), wash='#FFFFFF', ink=INK, sw=.9)
    heart(0, 6, 64, HOT, key=key + 'h')
    pop()


def photoMsg(x, y, w, h, k, scene, key='pm'):
    """a photo message bubble (right side, his avatar is on the right; this one is from her: left side)"""
    if k <= .02:
        return
    p = backOut(k)
    push()
    translate(x, y)
    scale(p)
    boilSeed(key)
    paint(rrPts(0, 0, w, h, 18), wash='#FFFFFF', ink=INK, sw=.9)
    G.c.save()
    pth = skia.Path()
    pth.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(10, 10, w - 20, h - 20), 12, 12))
    G.c.clipPath(pth, skia.ClipOp.kIntersect, True)
    scene(10, 10, w - 20, h - 20)
    G.c.restore()
    pop()


# ------------------------------------------------------------------ misc
def speedLines(t, n, x0, y0, x1, y1, ang=math.pi, L=140, col='#FFFFFF', a=.8, seed=0, spd=1800):
    for i in range(n):
        h1, h2 = hash1(seed + i * 1.7), hash1(seed + i * 3.1)
        y = lerp(y0, y1, h1)
        x = x1 - ((t * spd * (.6 + .6 * h2) + h2 * 3000) % (x1 - x0 + L * 2))
        line(x, y, x + math.cos(ang + math.pi) * -L, y, col, a * (.5 + .5 * h2), 3)


def smallBird(x, y, s, flap, col=INK):
    a = .55 + .35 * math.sin(flap)
    inkLine([[x - s, y - s * a], [x - s * .35, y], [x, y + s * .12], [x + s * .35, y], [x + s, y - s * a]], .9, col, 'ink', .6)


def flagPop(x, y, s, txt, k, key='flag', col='#E8574A'):
    if k <= .01:
        return
    p = backOut(k)
    push()
    translate(x, y)
    scale(p)
    rotate(-.08)
    boilSeed(key)
    paint(rectPts(-.08 * s, -3.4 * s, .16 * s, 3.4 * s), wash=WOODDK, ink=INK, sw=.8)
    wave = math.sin(G.T * 8) * .12 * s
    paint([[.08 * s, -3.4 * s], [2.8 * s, -3.2 * s + wave], [2.7 * s, -2.0 * s + wave], [.08 * s, -2.2 * s]], wash=col, ink=INK, sw=.9, curv=.3)
    text(txt, 1.42 * s, -2.7 * s + wave * .5, .62 * s, '#FFFFFF', shadow=False)
    pop()
