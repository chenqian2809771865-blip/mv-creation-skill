# bj.py: costumes, props and sets for 《去北极忘记你》 (watercolour + boiling ink). Engine files are untouched;
# the beanies / snow pile / ear muffs are added by wrapping clawd.hat (after ch_chonghuai's wrapper).
import math
from eng import *
import eng
import clawd as _cl
from clawd import *
import ch_chonghuai as CH
from ch_chonghuai import heart, popK, rr, suitcase, batteryPct, placardSign, HOT, PINK, PINKDK, CREAM
from props import puff, sparkle, sparkles, floatHearts, bubble, stamp, impactLines
from sets import thunderCloud, zigzag, starField
from hl import scarfHook, _chain, photoFrame, mug
from common import handXY, B, bt, pk, after, age, kt

WENKAI = 'LXGWWenKai-Regular.ttf'
SNOW = '#F8FBFF'
SNOWSH = '#D7E6F4'
ICE = '#BFE3F5'
ICEDK = '#8CC2E2'
WOOD, WOODDK = '#C48A5C', '#94603A'


def line(x0, y0, x1, y1, col, a=1.0, w=2.0):
    G.c.drawLine(x0, y0, x1, y1, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=skcol(col, a),
                                            StrokeCap=skia.Paint.kRound_Cap))


def dot(x, y, r, col, a=1.0):
    G.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=skcol(col, a)))


# ================================================================== costume: beanies, snow pile, ear muffs, scarves
_hat0 = _cl.hat


def _beanie(u, sw, col):
    boilSeed('beanie' + col)
    paint([[-5.2 * u, -7.4 * u], [-4.8 * u, -10.2 * u], [0, -11.4 * u], [4.8 * u, -10.2 * u], [5.2 * u, -7.4 * u]], wash=col,
          fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=sw * .8, curv=.5)
    for i in range(5):
        x = (-3.2 + i * 1.6) * u
        inkLine([[x, -10.6 * u + abs(x) * .12], [x * 1.05, -8.4 * u]], sw * .35, mixCol(col, INK, .35), 'inkfine', .3)
    paint(rrPts(-5.5 * u, -8.3 * u, 11 * u, 1.5 * u, .5 * u), wash='#FFF3E2', ink=INK, sw=sw * .7)
    for i in range(6):
        x = (-4.4 + i * 1.75) * u
        inkLine([[x, -8.15 * u], [x, -6.95 * u]], sw * .4, '#C9B79A', 'inkfine', 0)
    paint(ellPts(0, -11.6 * u, 1.1 * u, 1.1 * u, 14), wash='#FFF3E2', ink=INK, sw=sw * .6)


def _snowPile(u, sw, k):
    """snow piled on the beanie: k layers (0..6), each a little narrower, drawn bottom-up"""
    if k <= .01:
        return
    n = int(math.ceil(k))
    y = -11.0 * u
    for i in range(n):
        f = clamp(k - i)
        w = (8.8 - i * 1.15) * u
        h = 1.3 * u * f
        ox = (.45 if i % 2 else -.35) * u * min(1, i)
        boilSeed(f'snowp{i}')
        pts = []
        for j in range(15):
            a = math.pi + j / 14 * math.pi
            bump = .22 * u * math.sin(j * 2.3 + i * 1.7)
            pts.append([ox + math.cos(a) * (w / 2 + bump * .5), y + math.sin(a) * (h + bump)])
        pts += [[ox + w / 2 + .2 * u, y + .45 * u], [ox - w / 2 - .2 * u, y + .45 * u]]
        paint(pts, wash=SNOW, fill=SNOWSH, fillOp=70, ink=INK, sw=sw * .5, curv=.4)
        y -= h * .95


def _muffs(u, sw):
    boilSeed('muffs')
    inkLine([[-5.3 * u, -6.0 * u], [-4.6 * u, -10.4 * u], [0, -12.3 * u], [4.6 * u, -10.4 * u], [5.3 * u, -6.0 * u]], sw * 2.2, '#E8476E', 'ink', .6)
    for s in (-1, 1):
        cx, cy = s * 5.4 * u, -5.9 * u
        pts = []
        for i in range(20):
            a = i / 20 * TAU
            r = 1.35 * u * (1 + .1 * math.sin(a * 7))
            pts.append([cx + math.cos(a) * r, cy + math.sin(a) * r])
        paint(pts, wash='#FFFFFF', fill='#E6E2F0', fillOp=70, ink=INK, sw=sw * .6, curv=.4)


def _hat(u, h, sw, o=None):
    o = o or {}
    if h == 'beanieB':
        _beanie(u, sw, '#4F78C4')
    elif h == 'beanieR':
        _beanie(u, sw, '#D9534F')
    elif h == 'snowhat':
        _snowPile(u, sw, o.get('snowK', 0.0))
    elif h == 'muffs':
        _muffs(u, sw)
    elif h == 'flowerB':                     # her white flower, pinned on the beanie brim
        _cl.flowerAt(-2.7 * u, -8.1 * u, u, sw)
    else:
        _hat0(u, h, sw, o)


_cl.hat = _hat
ME_SCARF = ('#E8B04A', '#B9852C')
HER_SCARF = ('#F7EEE0', '#CDB797')


def himA(x, y, u, o=None):
    """him in this MV: blue beanie + mustard scarf (+ snow pile / ear muffs)"""
    o = dict(o or {})
    v = o.get('view', 'front')
    hats = list(o.pop('hats', None) or ['beanieB'])
    if (o.get('snowK') or 0) > .01:
        hats.append('snowhat')
    if o.pop('muffs', False):
        hats.append('muffs')
    o['hat'] = hats
    extra = o.pop('draw', None)
    sc = None if v in ('back',) else scarfHook(v, ME_SCARF[0], ME_SCARF[1], tail=-1, flutter=o.pop('flutter', 0))
    o['draw'] = _chain(sc, extra)
    him(x, y, u, o)


def herA(x, y, u, o=None):
    """her: red beanie with her white flower + cream scarf"""
    o = dict(o or {})
    v = o.get('view', 'front')
    o['hat'] = list(o.pop('hats', None) or ['beanieR', 'flowerB'])
    extra = o.pop('draw', None)
    sc = scarfHook(v, HER_SCARF[0], HER_SCARF[1], tail=1, flutter=o.pop('flutter', 0))
    o['draw'] = _chain(sc, extra)
    her(x, y, u, o)


def sitOn(fn, x, seatTop, u, o=None):
    """seat a Clawd on a block / bank / bench top (like sets2.seat, but without the contact shadow,
    which reads as a dark ring on the block's front face)"""
    d = dict(o or {})
    d['noShadow'] = True
    fn(x, seatTop + 2.0 * u, u, d)


def handDot(x, y, u, col=None, key='hd'):
    """a little round hand (body colour, ink edge) over a held stick, so it reads as 'held'"""
    boilSeed(key)
    paint(ellPts(x, y, .62 * u, .62 * u, 12), wash=col or PAL['clay'], ink=INK, sw=clamp(u / 15, .45, 2.4) * .6)


# ================================================================== the airport (S01, S02) — no windows
def hallBack(t, key='hall', floorY=820, pillars=(150, 1770)):
    gradRect(-400, -400, W + 800, floorY + 400, ['#F3E8D4', '#E8D9BF'])
    flatRect(-400, -400, W + 800, 330, '#DCCDB2')
    for i in range(-3, 22):
        x = i * 110
        line(x, -60, x, 120, '#CBB99A', .5, 3)
    # pillars
    for px in pillars:
        boilSeed(key + f'pl{px}')
        paint(rectPts(px - 70, -100, 140, floorY + 100), wash='#E2D3B8', fill='#C9B597', fillOp=60, ink=INK, sw=1.0)
        flatRect(px - 70, 560, 140, 14, '#B79F7D', .8)
    # wainscot
    flatRect(-400, floorY - 120, W + 800, 120, '#D7C3A2')
    line(-400, floorY - 120, W + 400, floorY - 120, INK, .8, 3)
    # floor tiles
    gradRect(-400, floorY, W + 800, 700, ['#C9B9A0', '#B5A388'])
    for j in range(7):
        y = floorY + 30 * j * (1 + j * .4)
        line(-400, y, W + 400, y, '#A08E73', .55, 2)
    for i in range(-10, 30):
        x0 = 960 + (i - 10) * 90
        line(x0 + (x0 - 960) * .0, floorY, x0 + (x0 - 960) * 1.4, floorY + 400, '#A08E73', .45, 2)
    line(-400, floorY, W + 400, floorY, INK, .9, 3)


def pottedPlant(x, y, s, key='pp'):
    boilSeed(key)
    for i in range(7):
        a = -math.pi / 2 + (i - 3) * .32
        L = s * (1.6 + .5 * hash1(i * 3.1))
        paint(ellPts(x + math.cos(a) * L * .55, y - 1.1 * s + math.sin(a) * L * .55, .32 * s, L * .5, 14, 0, a + math.pi / 2),
              wash='#7CC36B', fill='#4F9A4A', fillOp=60, ink=INK, sw=.6)
    paint([[x - .75 * s, y - 1.2 * s], [x + .75 * s, y - 1.2 * s], [x + .55 * s, y], [x - .55 * s, y]], wash='#D9774E', fill='#B85C3A', fillOp=60, ink=INK, sw=.8)


TILE_POOL = '东京巴黎纽约伦敦首尔悉尼罗马开罗冰岛海口拉萨大理'
CODE_POOL = 'ABCDEFGHJKLMNPRSTUVWXYZ0123456789'


def _scram(ch, i, t, pool, salt=0.0):
    fi = int(t * 24 / 3)
    pl = pool.replace(ch, '')
    return pl[int(hash1(fi * 7.3 + i * 3.1 + salt) * len(pl)) % len(pl)]


def flapRow(x0, y, cw, chh, txt, lockT, t, key, big=False, dark=True):
    """a row of split-flap tiles starting at x0 (left), centred on y. lockT = time the whole row locks (or a list per tile).
    Spaces are gaps. Returns the x after the row."""
    x = x0
    gap = cw * .1
    for i, ch in enumerate(txt):
        if ch == ' ':
            x += cw * .55
            continue
        lt = lockT[i] if isinstance(lockT, (list, tuple)) else lockT
        fl = (t - (lt - .13)) / .12          # 0..1 flip that is finished just before the lock beat
        locked = fl >= .5
        if locked:
            c_ = ch
            pk_ = clamp(fl)
        else:
            pool = CODE_POOL if (ch.isascii()) else TILE_POOL
            c_ = _scram(ch, i, t, pool, salt=len(key))
            pk_ = clamp(fl) if fl > 0 else 0
        push()
        translate(x + cw / 2, y)
        if 0 < pk_ < 1:
            scale(1, max(.08, abs(math.cos(pk_ * math.pi))))
        boilSeed(f'{key}{i}')
        if big:
            tile = '#FFF8EE' if locked else '#DAD3E2'
            paint(rrPts(-cw / 2, -chh / 2, cw, chh, 12), wash=tile, ink=INK, sw=1.0)
            G.c.drawRect(skia.Rect.MakeXYWH(-cw / 2, -2, cw, 4), skia.Paint(AntiAlias=True, Color=skcol('#3A3550', .8)))
            text(c_, 0, 6, chh * .72, HOT if locked else '#6A647A', shadow=False)
        else:
            paint(rrPts(-cw / 2, -chh / 2, cw, chh, 6), wash='#3E4466' if dark else '#FFF8EE', ink=INK, sw=.6, lite=True)
            G.c.drawRect(skia.Rect.MakeXYWH(-cw / 2, -1, cw, 2), skia.Paint(AntiAlias=True, Color=skcol('#1C1E30', .9)))
            text(c_, 0, 3, chh * .7, '#FFE39A' if locked else '#B9B6C9', shadow=False, face=WENKAI)
        pop()
        x += cw + gap
    return x


def departureBoard(t, titleLocks, rows, key='db'):
    """the hanging departure board of S01. titleLocks: per-tile lock times of 去北极忘记你; rows = [(txt, lockT, lampT)]"""
    x0, y0, w, h = 330, 70, 1260, 560
    for sx in (x0 + 140, x0 + w - 140):
        line(sx, -200, sx, y0, '#6A647A', 1, 6)
    boilSeed(key)
    paint(rectPts(x0 + 18, y0 + 22, w, h), wash=INK, washOp=60, ink=None)
    paint(rrPts(x0, y0, w, h, 26), wash='#2C3150', fill='#1D2038', fillOp=60, ink=INK, sw=1.3)
    # header
    text('出发', x0 + 70, y0 + 48, 40, '#FFFFFF', shadow=False, align='left')
    text('DEPARTURES', x0 + 170, y0 + 50, 30, '#B9C3E8', shadow=False, align='left', face=WENKAI)
    hh = 9 + (41 + int(t // 4)) // 60
    text(f'0{hh}:{(41 + int(t // 4)) % 60:02d}', x0 + w - 70, y0 + 48, 38, '#FFE39A', shadow=False, align='right', face=WENKAI)
    line(x0 + 30, y0 + 86, x0 + w - 30, y0 + 86, '#4D557D', 1, 3)
    # title row (big tiles)
    cw, chh = 158, 196
    tw = 6 * cw + 5 * cw * .1
    flapRow(960 - tw / 2, y0 + 200, cw, chh, '去北极忘记你', titleLocks, t, key + 'T', big=True)
    # small rows
    yy = y0 + 350
    for j, (txt, lt, lampT, stat) in enumerate(rows):
        y = yy + j * 72
        flapRow(x0 + 60, y, 46, 58, txt, lt, t, key + f'r{j}', big=False)
        # status lamp
        on = clamp((t - (lampT - .04)) / .1) if lampT is not None else 0
        cx = x0 + w - 220
        col = mixCol('#565B78', stat[1], on)
        boilSeed(key + f'lamp{j}')
        paint(ellPts(cx, y, 16, 16, 12), wash=col, ink=INK, sw=.6)
        if on > 0:
            blink = 1 if (frac((t - lampT + .04) * 2.4) < .6) else .55
            glow(cx, y, 40, stat[1], .7 * on * blink)
        text(stat[0], cx + 30, y + 2, 34, mixCol('#8C90A8', '#FFFFFF', on), shadow=False, align='left', face=WENKAI)


def gateSign(x, y, key='gs'):
    boilSeed(key)
    line(x - 200, -100, x - 200, y - 50, '#6A647A', 1, 5)
    line(x + 200, -100, x + 200, y - 50, '#6A647A', 1, 5)
    paint(rrPts(x - 330, y - 60, 660, 120, 18), wash='#F6C343', fill='#D9A322', fillOp=60, ink=INK, sw=1.1)
    text('登机口 N1 · 北极', x - 60, y + 2, 50, INK, shadow=False)
    # a painted arrow (KuaiLe has no arrow glyphs)
    paint([[x + 196, y - 22], [x + 246, y - 22], [x + 246, y - 42], [x + 296, y], [x + 246, y + 42], [x + 246, y + 22], [x + 196, y + 22]],
          wash=INK, ink=None)


def gateSeats(x0, n, seatTop, key='seats', col='#4F6FA8'):
    """a row of airport seats (seat top y); returns the seat centres. Drawn in two passes: backs (call first)."""
    cs = []
    w = 170
    boilSeed(key)
    line(x0 - 20, seatTop + 70, x0 + n * w + 20, seatTop + 70, '#5A566E', 1, 10)
    for i in range(n):
        cx = x0 + i * w + w / 2
        cs.append(cx)
        paint(rrPts(cx - 72, seatTop - 150, 144, 150, 22), wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=.9)
        boilSeed(key + f'f{i}')
        paint(rrPts(cx - 80, seatTop - 6, 160, 40, 14), wash=mixCol(col, '#FFFFFF', .15), fill=col, fillOp=60, ink=INK, sw=.9)
    for sx in (x0 + 30, x0 + n * w - 30):
        paint(rectPts(sx - 8, seatTop + 70, 16, 1000 - seatTop - 70 if seatTop < 1000 else 10), wash='#5A566E', ink=INK, sw=.6)
    return cs


def gateSeatsFront(x0, n, seatTop, key='seats', col='#4F6FA8'):
    w = 170
    for i in range(n):
        cx = x0 + i * w + w / 2
        boilSeed(key + f'f{i}')
        paint(rrPts(cx - 80, seatTop - 6, 160, 40, 14), wash=mixCol(col, '#FFFFFF', .15), fill=col, fillOp=60, ink=INK, sw=.9)


def iceCup(x, y, s, cubes, t, key='cup', splash=None):
    """tall iced drink on a small round table; (x, y) = cup bottom centre. cubes = list of (landTime, dx, rot). Returns cup top y."""
    top = y - 3.4 * s
    boilSeed(key)
    # drink
    paint([[x - 1.05 * s, top + .7 * s], [x + 1.05 * s, top + .7 * s], [x + .8 * s, y - .12 * s], [x - .8 * s, y - .12 * s]],
          wash='#A6D8F0', fill='#73B6DE', fillOp=70, ink=None)
    # cubes (already landed ones float near the top, stacked)
    for i, (lt, dx, rot) in enumerate(cubes):
        a = t - lt
        if a < -.2:
            continue
        if a < 0:   # falling in
            cy_ = top - 2.4 * s + (2.4 * s + 1.05 * s - i * .55 * s) * easeIn(clamp((a + .2) / .2))
        else:
            cy_ = top + 1.05 * s - i * .55 * s + .12 * s * math.exp(-a * 8) * math.cos(a * 30)
        push()
        translate(x + dx * s, cy_)
        rotate(rot + (0 if a > 0 else a * 3))
        boilSeed(key + f'c{i}')
        paint(rrPts(-.42 * s, -.42 * s, .84 * s, .84 * s, .14 * s), wash='#EAF7FF', washOp=230, fill='#BFE3F5', fillOp=60, ink=INK, sw=.6)
        line(-.22 * s, -.25 * s, .1 * s, -.25 * s, '#FFFFFF', .9, 4)
        pop()
        if 0 <= a < .3:
            for j in range(6):
                ang = -math.pi / 2 + (j - 2.5) * .45
                r = (.6 + a * 6) * s
                dot(x + dx * s + math.cos(ang) * r, top + .6 * s + math.sin(ang) * r * .8 + a * a * 30 * s, .14 * s * (1 - a / .3), '#7FC4EA')
    # glass
    paint([[x - 1.15 * s, top], [x + 1.15 * s, top], [x + .85 * s, y], [x - .85 * s, y]], wash='#FFFFFF', washOp=70, ink=INK, sw=.9)
    line(x - .7 * s, top + .4 * s, x - .55 * s, y - .5 * s, '#FFFFFF', .7, 5)
    # straw
    inkLine([[x + .35 * s, top + 1.6 * s], [x + .6 * s, top - 1.1 * s], [x + 1.2 * s, top - 1.5 * s]], 1.6, HOT, 'ink', .3)
    return top


def sideTable(x, y, top, key='stb'):
    boilSeed(key)
    paint(rectPts(x - 10, top, 20, y - top), wash='#6A647A', ink=INK, sw=.6)
    paint(ellPts(x, y, 70, 14, 16), wash='#6A647A', ink=INK, sw=.6)
    paint(ellPts(x, top, 130, 24, 22), wash='#D9C3A0', fill='#B79F7D', fillOp=60, ink=INK, sw=.9)


# ================================================================== her disguise: a cardboard box with pink feet
def herBox(x, y, s, t, walk=0.0, eyes=1.0, pom=True, label='易碎', key='hb', wiggle=0.0, lid=0.0, blush=0.0, look=0.0, rot=0.0, legs=True):
    """(x, y) = ground under the box centre, s = box width. Pink Clawd feet stick out below; two eye holes show her eyes;
    her red beanie pom-pom pokes through the top flaps. walk = stride phase (0 = standing)."""
    w, h = s, s * .66
    legH = s * .13 if legs else 0
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key + 'sh')
    paint(ellPts(0, 4, w * .55, s * .05, 18), fill=INK, fillOp=80, bleed=.25, ink=None, lite=True)
    # legs (her colour)
    for i, lx in enumerate((-.32, -.12, .12, .32) if legs else ()):
        ph = walk * math.pi + (0 if i % 2 else math.pi)
        lift = max(0, math.sin(ph)) * legH * .5 if walk else 0
        wig = math.sin(t * 40 + i) * legH * .25 * wiggle
        boilSeed(key + f'l{i}')
        paint(rrPts(lx * w - s * .045, -legH - 2 - lift + wig, s * .09, legH + 4, s * .03), wash=PINK, fill=PINKDK, fillOp=50, ink=INK, sw=.7)
    push()
    translate(0, -legH)
    # back flaps
    boilSeed(key + 'b')
    op = clamp(1 - lid)
    for sx in (-1, 1):
        paint([[sx * w / 2, -h], [sx * w / 2 + sx * w * .2 * op, -h - w * .26 * op], [sx * w * .05, -h - w * .28 * op - w * .02], [sx * w * .05, -h]],
              wash='#C99A6B', ink=INK, sw=.8)
    if pom:
        boilSeed(key + 'pom')
        paint(ellPts(w * .1, -h - s * .06, s * .07, s * .07, 12), wash='#FFF3E2', ink=INK, sw=.6)
        paint([[w * .02, -h + 2], [w * .18, -h + 2], [w * .14, -h - s * .02], [w * .06, -h - s * .02]], wash='#D9534F', ink=INK, sw=.5)
    # front
    boilSeed(key + 'f')
    paint(rectPts(-w / 2, -h, w, h), wash='#C99A6B', fill='#A87B52', fillOp=60, ink=INK, sw=1.0)
    inkLine([[-w / 2 + 6, -h * .55], [w / 2 - 6, -h * .55]], .5, '#A87B52', 'inkfine', 0)
    # eye holes with her eyes
    if eyes > .01:
        for ex in (-.16, .16):
            cx, cy = ex * w + look * w * .03, -h * .7
            boilSeed(key + f'e{ex}')
            paint(ellPts(cx, cy, w * .085, w * .06, 14), wash='#2B2233', ink=INK, sw=.6)
            G.c.save()
            pth = skia.Path()
            pth.addOval(skia.Rect.MakeXYWH(cx - w * .085, cy - w * .06, w * .17, w * .12))
            G.c.clipPath(pth, skia.ClipOp.kIntersect, True)
            dot(cx + look * w * .02, cy + w * .005, w * .035 * eyes, '#FFFFFF')
            dot(cx + look * w * .02 + w * .012, cy - w * .012, w * .012 * eyes, '#2B2233')
            G.c.restore()
        if blush > .01:
            for ex in (-.27, .27):
                dot(ex * w, -h * .52, w * .045, '#F39AAE', .8 * blush)
    text(label, 0, -h * .3, s * .17, '#C8324A', shadow=False)
    # fragile glass icon (painted)
    boilSeed(key + 'gl')
    paint([[w * .3, -h * .42], [w * .4, -h * .42], [w * .37, -h * .3], [w * .33, -h * .3]], wash='#FFFFFF', washOp=150, ink='#C8324A', sw=.5)
    pop()
    pop()


def pinkPrints(pts, a=1.0, key='pp'):
    for i, (x, y, ang) in enumerate(pts):
        boilSeed(key + str(i))
        paint(ellPts(x, y, 13, 7, 10, 0, ang), wash='#F2A8BA', washOp=int(200 * a), ink=None)


# ================================================================== the arctic
def _farDetails(t, mode, horizon, key):
    """small things on the horizon: a camp tent (glows at dusk/night), a string of flags, a seal on an ice floe, birds by day"""
    night = 0 if mode == 'day' else (.5 if mode == 'dusk' else 1)
    # camp tent + flag string, far left
    tx, ty = 140, horizon + 14
    boilSeed(key + 'tent')
    paint([[tx - 46, ty], [tx, ty - 52], [tx + 46, ty]], wash=mixCol('#E8744A', '#7A4A5A', night * .5), fill='#B85C3A', fillOp=60, ink=INK, sw=.6)
    paint([[tx - 9, ty], [tx, ty - 20], [tx + 9, ty]], wash=mixCol('#5A3A3A', '#FFD27A', night), ink=None)
    if night > 0:
        glow(tx, ty - 10, 80, '#FFB55A', .55 * night)
    inkLine([[tx + 40, ty - 40], [tx + 300, ty - 30]], .5, INK, 'inkfine', .5)
    for i in range(7):
        fx = tx + 60 + i * 34
        fy = ty - 39 + i * 1.4 + 4 * math.sin(i * 1.3)
        col = ['#E8476E', '#F6C343', '#5BA8D9', '#7CC36B'][i % 4]
        boilSeed(key + f'fl{i}')
        paint([[fx, fy], [fx + 18, fy], [fx + 9, fy + 18 + 2 * math.sin(t * 4 + i)]], wash=col, ink=INK, sw=.35)
    boilSeed(key + 'pole')
    inkLine([[tx + 300, ty], [tx + 300, ty - 44]], .7, WOODDK, 'ink', 0)
    # seal on a floe, right-centre
    sx, sy = 1180, horizon + 22
    boilSeed(key + 'floe')
    paint(ellPts(sx, sy, 90, 14, 16), wash=mixCol('#FFFFFF', '#8FA1D0', night), ink=INK, sw=.5)
    paint(ellPts(sx - 6, sy - 16, 34, 14, 14), wash=mixCol('#8E96A8', '#4A5470', night), ink=INK, sw=.5)
    paint(ellPts(sx + 26, sy - 26, 13, 12, 12), wash=mixCol('#8E96A8', '#4A5470', night), ink=INK, sw=.5)
    dot(sx + 31, sy - 28, 2.2, INK)
    if mode == 'day':
        for i, (bx, by) in enumerate([(1420, 170), (1470, 140), (1510, 185)]):
            bxx = bx + 30 * math.sin(t * .4 + i)
            a = .55 + .35 * math.sin(t * 9 + i * 2)
            inkLine([[bxx - 12, by - 12 * a], [bxx - 4, by], [bxx, by + 1.5], [bxx + 4, by], [bxx + 12, by - 12 * a]], .55, INK, 'ink', .6)


def arcticBack(t, mode='day', horizon=640, key='ab', mtn=True, sparkle_=True, sky=None, deco=True):
    if sky is None:
        sky = {'day': ['#A9D6F2', '#E8F5FC'], 'dusk': ['#3A3F86', '#A58FC6'], 'night': ['#0D1636', '#283A72']}[mode]
    gradRect(-600, -600, W + 1200, horizon + 600, sky)
    if mode != 'day':
        starField(t, 7, 90, -300, -300, W + 300, horizon - 60, on=1.0 if mode == 'night' else .5, r=3.2)
    if mtn:
        # far ice mountains
        far = '#DCEBF7' if mode == 'day' else ('#7D86B8' if mode == 'dusk' else '#3B4E86')
        fdk = mixCol(far, INK, .2)
        boilSeed(key + 'm1')
        P = [[-600, horizon + 10]]
        for i in range(15):
            x = -600 + i * 230
            P.append([x + 60, horizon - 110 - 160 * hash1(i * 3.7)])
            P.append([x + 175, horizon - 40 - 60 * hash1(i * 1.3)])
        P.append([W + 600, horizon + 10])
        paint(P, wash=far, fill=fdk, fillOp=40, ink=INK, sw=.7, curv=.2)
        near = '#EEF6FC' if mode == 'day' else ('#99A3CF' if mode == 'dusk' else '#4C619C')
        boilSeed(key + 'm2')
        P = [[-600, horizon + 20]]
        for i in range(10):
            x = -600 + i * 360 + 100
            P.append([x, horizon - 30 - 70 * hash1(i * 5.1 + 2)])
            P.append([x + 150, horizon - 10])
        P.append([W + 600, horizon + 20])
        paint(P, wash=near, fill=mixCol(near, INK, .15), fillOp=40, ink=INK, sw=.6, curv=.3)
    snow = SNOW if mode == 'day' else ('#C9CFEA' if mode == 'dusk' else '#8FA1D0')
    snowsh = mixCol(snow, '#6E86C2', .3)
    gradRect(-600, horizon, W + 1200, 1200, [snow, mixCol(snow, snowsh, .45)])
    boilSeed(key + 'sn')
    for i in range(7):
        cx = -200 + i * 380 + 120 * hash1(i)
        paint(ellPts(cx, horizon + 120 + 150 * hash1(i * 2.2), 260, 26, 20), wash=snowsh, washOp=70, ink=None)
    inkLine([[-600, horizon], [W + 600, horizon]], .8, INK, 'ink', 0)
    if deco:
        _farDetails(t, mode, horizon, key + 'fd')
    if sparkle_ and mode == 'day':
        for i in range(14):
            sx = hash1(i * 4.4) * W
            sy = horizon + 40 + hash1(i * 7.7) * (H - horizon - 140)
            k = .5 + .5 * math.sin(t * 3 + i * 1.7)
            if k > .55:
                sparkle(sx, sy, 10 * k, '#FFFFFF', k)


def snowfall(t, seed, n, x0, y0, x1, y1, a=1.0, r=6.0, sp=1.0):
    for i in range(n):
        h = hash1(seed + i * 1.13)
        v = (80 + 70 * hash1(i * 2.7)) * sp
        y = y0 + ((h * (y1 - y0) + t * v) % (y1 - y0))
        x = x0 + hash1(seed + i * 3.1) * (x1 - x0) + 26 * math.sin(t * 1.4 + i)
        dot(x, y, r * (.6 + .7 * hash1(i * 5.3)), '#FFFFFF', a * (.65 + .35 * hash1(i)))


def igloo(x, y, r, lit=0.0, key='ig', night=0.0):
    """dome of snow blocks; (x, y) = ground centre"""
    boilSeed(key)
    col = mixCol(SNOW, '#9FB2DE', night * .6)
    dk = mixCol(SNOWSH, '#5E72AE', night * .6)
    pts = [[x + math.cos(a) * r, y + math.sin(a) * r * .92] for a in [math.pi + i / 24 * math.pi for i in range(25)]]
    paint(pts, wash=col, fill=dk, fillOp=70, ink=INK, sw=1.0)
    for j in range(1, 5):
        yy = y - r * .92 * j / 5
        hw = r * math.sqrt(max(0, 1 - (j / 5) ** 2))
        inkLine([[x - hw, yy], [x + hw, yy]], .5, mixCol(dk, INK, .3), 'inkfine', 0)
        n = 6 - j
        for i in range(n + 1):
            xx = x - hw + (i + (.5 if j % 2 else 0)) * 2 * hw / (n + .5)
            if x - hw < xx < x + hw:
                inkLine([[xx, yy], [xx, yy + r * .92 / 5]], .45, mixCol(dk, INK, .3), 'inkfine', 0)
    # entrance tunnel
    ex = x + r * .45
    boilSeed(key + 'e')
    tun = [[ex - r * .38, y], [ex - r * .38, y - r * .32], [ex - r * .2, y - r * .5], [ex + r * .2, y - r * .5], [ex + r * .38, y - r * .32], [ex + r * .38, y]]
    paint(tun, wash=col, fill=dk, fillOp=60, ink=INK, sw=.9, curv=.5)
    door = [[ex - r * .22, y], [ex - r * .22, y - r * .22], [ex, y - r * .36], [ex + r * .22, y - r * .22], [ex + r * .22, y]]
    paint(door, wash=mixCol('#3B3550', '#FFC976', lit), ink=INK, sw=.7, curv=.5)
    if lit > .02:
        glow(ex, y - r * .15, r * .9, '#FFC976', .7 * lit)


def iceBlock(x, top, w, h, key='ib', night=0.0):
    boilSeed(key)
    col = mixCol(ICE, '#6D86C8', night * .5)
    paint(rectPts(x - w / 2, top, w, h, 2), wash=col, fill=mixCol(col, INK, .2), fillOp=60, ink=INK, sw=.9)
    paint(rectPts(x - w / 2, top - 16, w, 16, 2), wash=mixCol(col, '#FFFFFF', .5), ink=INK, sw=.7)
    line(x - w * .35, top + 18, x - w * .15, top + h * .6, '#FFFFFF', .6, 4)


def iceHole(x, y, rx, key='ih', night=0.0):
    boilSeed(key)
    paint(ellPts(x, y, rx * 1.25, rx * .34, 22), wash=mixCol('#E2F1FB', '#7D93C8', night * .6), ink=INK, sw=.7)
    paint(ellPts(x, y, rx, rx * .25, 20), wash=mixCol('#2E6E9E', '#1A2E5E', night * .5), fill='#1E4C78', fillOp=60, ink=INK, sw=.8)
    line(x - rx * .5, y - rx * .06, x - rx * .1, y - rx * .1, '#9FD3F0', .7, 4)


def calPage(day, label):
    return (day, label)


def calendarStand(x, y, w, h, page, t, key='cal', tear=None, bounce=0.0):
    """tear-off calendar on a wooden stake stuck in the snow. (x, y) = top centre; page = (day, label).
    tear = (oldPage, k) flying up and away to the upper left (never across the character on the right)."""
    boilSeed(key + 'st')
    paint(rectPts(x - 14, y + h - 20, 28, 250), wash=WOOD, fill=WOODDK, fillOp=60, ink=INK, sw=.8)
    paint(rectPts(x - w / 2 - 10, y - 10, w + 20, h + 14), wash='#E8476E', fill='#B8324F', fillOp=50, ink=INK, sw=1.1)

    def drawPage(pg, px, py, rot=0.0, sc=1.0):
        day, label = pg
        push()
        translate(px, py)
        rotate(rot)
        scale(sc)
        boilSeed(key + day)
        paint(rectPts(-w / 2, 0, w, h - 10), wash='#FFFDF6', ink=INK, sw=.9)
        flatRect(-w / 2, 0, w, 64, '#FCE3EA')
        text('第', -w * .3, 34, 34, '#B8324F', shadow=False, face=WENKAI)
        text('天', w * .3, 34, 34, '#B8324F', shadow=False, face=WENKAI)
        text(day, 0, h * .44, h * .36, HOT, shadow=False)
        text(label, 0, h - 62, 46, '#5A4A6A', shadow=False, face=WENKAI)
        pop()
    b = 1 + .05 * bounce
    drawPage(page, x, y, sc=b)
    for i in range(5):
        rx = x - w / 2 + 30 + i * (w - 60) / 4
        paint(rrPts(rx - 7, y - 26, 14, 40, 7), wash='#C9C1D6', ink=INK, sw=.6)
    if tear:
        pg, k = tear
        if 0 <= k < 1:
            drawPage(pg, x - 220 * easeIn(k), y - 900 * easeIn(k) - 40 * math.sin(k * 3), -.7 * easeIn(k))


def fish(x, y, s, rot=0.0, key='fish', note=None):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint([[-1.3 * s, 0], [-2.0 * s, -.6 * s], [-1.9 * s, .6 * s]], wash='#F2A65A', ink=INK, sw=.7)
    paint(ellPts(0, 0, 1.45 * s, .72 * s, 20), wash='#F6B26B', fill='#E08A3C', fillOp=60, ink=INK, sw=.8)
    dot(.85 * s, -.18 * s, .14 * s, INK)
    dot(.8 * s, -.22 * s, .05 * s, '#FFFFFF')
    inkLine([[-.2 * s, -.5 * s], [-.45 * s, 0], [-.2 * s, .5 * s]], .5, '#C9702A', 'inkfine', .5)
    if note:
        push()
        translate(1.9 * s, .35 * s)
        rotate(.25)
        boilSeed(key + 'n')
        nw = textW(note, 30, WENKAI) + 30
        paint(rectPts(0, -26, nw, 52, 1), wash='#FFFDF6', ink=INK, sw=.6)
        text(note, nw / 2, 1, 30, INK, shadow=False, face=WENKAI)
        pop()
    pop()


def bulb(x, y, s, on, key='bulb'):
    boilSeed(key)
    if on > .02:
        glow(x, y, 4 * s * on, '#FFE36E', .9 * on)
        for i in range(8):
            a = i / 8 * TAU
            r0, r1 = 1.5 * s, (1.5 + .9 * on) * s
            line(x + math.cos(a) * r0, y + math.sin(a) * r0, x + math.cos(a) * r1, y + math.sin(a) * r1, '#F2B33D', on, 5)
    paint(ellPts(x, y, s, s * 1.05, 18), wash=mixCol('#E8E4EC', '#FFE36E', on), ink=INK, sw=.8)
    paint(rectPts(x - .45 * s, y + .85 * s, .9 * s, .55 * s, 1), wash='#9A94A8', ink=INK, sw=.6)


def snowman(x, y, s, turn=0.0, key='sm', disguise=False, t=0.0, heartK=0.0, scarf='#5BA8D9', hatCol=INK, look=0.0):
    """(x, y) = ground; s = bottom ball radius. turn 0..1 = head turned away (face slides off, back of head shows).
    disguise = her hiding inside a snowman: pink Clawd feet below, red beanie + white flower, her eyes."""
    boilSeed(key + 'sh')
    paint(ellPts(x, y + 4, s * 1.15, s * .18, 16), fill=INK, fillOp=70, bleed=.25, ink=None, lite=True)
    if disguise:
        for i, lx in enumerate((-.42, -.15, .15, .42)):
            boilSeed(key + f'leg{i}')
            paint(rrPts(x + lx * s - s * .09, y - s * .16, s * .18, s * .2, s * .05), wash=PINK, fill=PINKDK, fillOp=50, ink=INK, sw=.7)
    yb = y - s * (.95 if not disguise else 1.08)
    boilSeed(key + 'b')
    paint(ellPts(x, yb, s, s * .92, 26), wash=SNOW, fill=SNOWSH, fillOp=70, ink=INK, sw=1.0)
    for j in range(2):
        dot(x, yb - s * .25 + j * s * .38, s * .07, INK)
    rh = s * .66
    yh = yb - s * .8 - rh * .85
    # scarf
    boilSeed(key + 'sc')
    paint(rrPts(x - rh * 1.05, yh + rh * .72, rh * 2.1, rh * .32, rh * .14), wash=scarf, ink=INK, sw=.7)
    # stick arms
    inkLine([[x - s * .9, yb - s * .35], [x - s * 1.6, yb - s * .85], [x - s * 1.75, yb - s * 1.05]], 1.2, WOODDK, 'ink', .3)
    inkLine([[x + s * .9, yb - s * .35], [x + s * 1.6, yb - s * .8], [x + s * 1.8, yb - s * .75]], 1.2, WOODDK, 'ink', .3)
    boilSeed(key + 'h')
    paint(ellPts(x, yh, rh, rh * .95, 24), wash=SNOW, fill=SNOWSH, fillOp=70, ink=INK, sw=1.0)
    # face (slides to the side as the head turns, gone past half)
    fx = x + look * rh * .15 + turn * rh * .78
    fa = 1.0
    if fa > .02:
        G.c.save()
        pth = skia.Path()
        pth.addOval(skia.Rect.MakeXYWH(x - rh, yh - rh * .95, rh * 2, rh * 1.9))
        G.c.clipPath(pth, skia.ClipOp.kIntersect, True)
        if disguise:
            for ex in (-.32, .32):
                paint(ellPts(fx + ex * rh, yh - rh * .1, rh * .13, rh * .2, 12), wash=INK, ink=None)
                dot(fx + ex * rh + rh * .04, yh - rh * .18, rh * .05, '#FFFFFF', fa)
            dot(fx - rh * .55, yh + rh * .2, rh * .14, '#F39AAE', .8 * fa)
            dot(fx + rh * .55, yh + rh * .2, rh * .14, '#F39AAE', .8 * fa)
        else:
            if turn < .6:
                dot(fx - rh * .32, yh - rh * .12, rh * .1, INK, fa)
            dot(fx + rh * .32 * (1 - turn * .5), yh - rh * .12, rh * .1, INK, fa)
            for m in range(5 if turn < .5 else 2):
                dot(fx - rh * .32 + m * rh * .16 + turn * rh * .3, yh + rh * .35 + math.sin(m / 4 * math.pi) * rh * .1, rh * .045, INK, fa)
        # carrot nose
        if not disguise:
            paint([[fx - rh * .02, yh - rh * .04], [fx + rh * .02, yh + rh * .14], [fx + rh * (.55 + .2 * turn), yh + rh * .08]], wash='#F08A3A', washOp=255 * fa,
                  ink=INK if fa > .5 else None, sw=.6)
        G.c.restore()
    if turn > .95 and not disguise:
        bubble(x + rh * 1.2, yh - rh * 2.0, '哼！', 40, tail=(x + rh * .6, yh - rh * .8), k=clamp((turn - .95) * 20), key=key + 'hb')
    # hat
    if disguise:
        push()
        u = rh / 4.6
        translate(x, yh - rh * .5 + 7.55 * u)
        _beanie(u, .8, '#D9534F')
        _cl.flowerAt(-2.7 * u, -8.1 * u, u, .8)
        pop()
    else:
        boilSeed(key + 'hat')
        paint(rectPts(x - rh * .9, yh - rh * .78, rh * 1.8, rh * .16), wash=hatCol, ink=INK, sw=.6)
        paint(rectPts(x - rh * .55, yh - rh * 1.55, rh * 1.1, rh * .8), wash=hatCol, ink=INK, sw=.6)
    if heartK > .01:
        heart(x + rh * .9, yh - rh * 1.6 - 20 * heartK, rh * .45 * backOut(clamp(heartK)), HOT, key=key + 'ht')


def mitten(x, y, s, rot=0.0, key='mit', col='#D9534F'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint([[-.6 * s, .9 * s], [-.7 * s, -.3 * s], [-.4 * s, -.9 * s], [.3 * s, -.9 * s], [.6 * s, -.3 * s], [.6 * s, .9 * s]], wash=col, ink=INK, sw=.7, curv=.5)
    paint(ellPts(-.8 * s, -.05 * s, .28 * s, .42 * s, 10, 0, -.4), wash=col, ink=INK, sw=.6)
    paint(rectPts(-.68 * s, .75 * s, 1.36 * s, .35 * s, 1), wash='#FFF3E2', ink=INK, sw=.6)
    pop()


def duck(x, y, s, rot=0.0, key='dk'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(ellPts(0, .2 * s, 1.0 * s, .62 * s, 18), wash='#F7D34E', fill='#E0A92C', fillOp=50, ink=INK, sw=.7)
    paint(ellPts(.55 * s, -.45 * s, .5 * s, .48 * s, 16), wash='#F7D34E', ink=INK, sw=.7)
    paint([[.95 * s, -.5 * s], [1.45 * s, -.38 * s], [.95 * s, -.25 * s]], wash='#F08A3A', ink=INK, sw=.5)
    dot(.7 * s, -.55 * s, .08 * s, INK)
    pop()


def fishbone(x, y, s, rot=0.0, key='fb'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    inkLine([[-1.3 * s, 0], [1.0 * s, 0]], 1.8, '#4A4458', 'ink', 0)
    for i in range(4):
        xx = -.8 * s + i * .45 * s
        inkLine([[xx, -.5 * s], [xx + .2 * s, 0], [xx, .5 * s]], 1.3, '#4A4458', 'ink', .3)
    paint([[1.0 * s, -.45 * s], [1.6 * s, 0], [1.0 * s, .45 * s]], wash='#EDEAF2', ink=INK, sw=.6)
    paint([[-1.3 * s, 0], [-1.8 * s, -.45 * s], [-1.8 * s, .45 * s]], wash='#EDEAF2', ink=INK, sw=.6)
    pop()


def storyBook(x, y, s, rot=0.0, title='我们的故事', key='book', col='#E8749A', sc=1.0):
    """closed book standing upright (cover facing us), (x, y) = centre"""
    push()
    translate(x, y)
    rotate(rot)
    scale(sc)
    boilSeed(key)
    paint(rectPts(-1.05 * s, -1.35 * s, 2.1 * s, 2.7 * s, 1), wash='#FFFDF6', ink=INK, sw=.7)
    paint(rrPts(-1.15 * s, -1.4 * s, 2.15 * s, 2.75 * s, .12 * s), wash=col, fill=mixCol(col, INK, .25), fillOp=50, ink=INK, sw=.9)
    flatRect(-1.15 * s, -1.4 * s, .28 * s, 2.75 * s, mixCol(col, INK, .3), .7)
    paint(heartPts(.1 * s, -.55 * s, .42 * s, 18), wash='#FFF3E2', ink=INK, sw=.5)
    lines = [title[i:i + 3] for i in range(0, len(title), 3)]
    for i, l_ in enumerate(lines):
        text(l_, .1 * s, .25 * s + i * .5 * s, .42 * s, '#FFFFFF', shadow=False, stroke=INK, strokeW=.08 * s)
    pop()


def openBook(x, y, s, title='她的使用说明书', key='ob', flip=0.0, shut=0.0):
    """a thick open manual seen from the front, (x, y) = bottom centre of the spine. shut 0..1 closes it."""
    push()
    translate(x, y)
    boilSeed(key)
    k = 1 - shut
    # thickness
    paint([[-2.4 * s * k - .2 * s, 0], [2.4 * s * k + .2 * s, 0], [2.4 * s * k + .2 * s, .45 * s], [-2.4 * s * k - .2 * s, .45 * s]], wash='#F2E8D4', ink=INK, sw=.7)
    for sgn in (-1, 1):
        P = [[0, -.15 * s], [sgn * 2.4 * s * k, -.5 * s * k - .15 * s], [sgn * 2.4 * s * k, 1.0 * s - .35 * s * k], [0, .3 * s]]
        if k < .08:
            P = [[0, -.15 * s], [sgn * .2 * s, -.15 * s], [sgn * .2 * s, .3 * s], [0, .3 * s]]
        paint(P, wash='#FFFDF6', ink=INK, sw=.8)
        if k > .5:
            for j in range(4):
                yy = -.15 * s + j * .28 * s
                line(sgn * .35 * s, yy + .05 * s, sgn * 2.1 * s * k, yy - .2 * s * k + .05 * s, '#B7AEC8', .8, 3)
    if shut > .5:
        paint(rrPts(-2.0 * s, -1.0 * s, 4.0 * s, 1.45 * s, .15 * s), wash='#5B7FC4', fill='#3C5A9A', fillOp=60, ink=INK, sw=1.0)
        text(title, 0, -.3 * s, .5 * s, '#FFFFFF', shadow=False, stroke=INK, strokeW=.07 * s)
    else:
        # the hard cover shows below the open pages, carrying the title
        boilSeed(key + 'cv')
        paint(rrPts(-2.5 * s * k - .1 * s, .4 * s, 5.0 * s * k + .2 * s, .78 * s, .1 * s), wash='#5B7FC4', fill='#3C5A9A', fillOp=60, ink=INK, sw=.8)
        if k > .6:
            text(title, 0, .8 * s, .54 * s, '#FFFFFF', shadow=False, stroke=INK, strokeW=.07 * s)
    pop()


def crate(x, y, w, h, key='crate'):
    """wooden crate, (x, y) = bottom centre; returns the rim y"""
    boilSeed(key)
    paint(rectPts(x - w / 2, y - h, w, h, 1), wash=WOOD, fill=WOODDK, fillOp=60, ink=INK, sw=1.0)
    for j in range(1, 3):
        line(x - w / 2 + 6, y - h + j * h / 3, x + w / 2 - 6, y - h + j * h / 3, WOODDK, .8, 4)
    inkLine([[x - w / 2 + 10, y - 10], [x + w / 2 - 10, y - h + 10]], .7, WOODDK, 'ink', 0)
    return y - h


def giveSign(x, y, k=1.0, key='gsn'):
    """a wooden sign on a stake: 示例甲 示例乙 / 免费. (x, y) = stake bottom"""
    if k <= .01:
        return
    p = backOut(k)
    push()
    translate(x, y)
    scale(p)
    boilSeed(key)
    paint(rectPts(-10, -330, 20, 330), wash=WOODDK, ink=INK, sw=.8)
    paint(rrPts(-170, -420, 340, 190, 14), wash='#FFF5E2', fill='#E8D3B8', fillOp=50, ink=INK, sw=1.1)
    text('示例甲', 0, -372, 56, INK, shadow=False)
    text('示例乙', 0, -300, 56, INK, shadow=False)
    push()
    translate(150, -420)
    rotate(.2)
    boilSeed(key + 'f')
    paint(rrPts(-60, -26, 120, 52, 10), wash=HOT, ink=INK, sw=.8)
    text('免费', 0, 2, 36, '#FFFFFF', shadow=False)
    pop()
    pop()


def mugPair(x, y, s, rot=0.0, key='mp'):
    push()
    translate(x, y)
    rotate(rot)
    for i, (dx, col) in enumerate(((-.6, '#F7A8BC'), (.6, '#F2A65A'))):
        boilSeed(key + str(i))
        paint(rrPts((dx - .5) * s, -.6 * s, s, 1.2 * s, .12 * s), wash=col, fill=mixCol(col, INK, .25), fillOp=50, ink=INK, sw=.7)
        paint(ellPts((dx + (.62 if dx > 0 else -.62)) * s, 0, .25 * s, .32 * s, 12), ink=INK, sw=.8)
        heart(dx * s, -.05 * s, .22 * s, '#FFFFFF', key=key + f'h{i}', sw=.4, shine=False)
    pop()


def couplePhoto(x, y, s, rot=0.0, key='cph'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-1.3 * s, -1.0 * s, 2.6 * s, 2.0 * s, 1), wash='#E8D3B8', ink=INK, sw=.8)
    paint(rectPts(-1.05 * s, -.78 * s, 2.1 * s, 1.56 * s, 1), wash='#CFE8F8', ink=None)
    flatRect(-1.05 * s, .25 * s, 2.1 * s, .53 * s, '#FFFFFF')
    u = s / 9
    her(-.45 * s, .55 * s, u, dict(eyes='happy', mouth='smile', blush=.5, lite=True, noShadow=True, boilKey=key + 'h', hat=['beanieR', 'flowerB']))
    him(.45 * s, .55 * s, u, dict(eyes='happy', mouth='smile', blush=.3, lite=True, noShadow=True, boilKey=key + 'm', flip=True, hat=['beanieB']))
    pop()


def snowGlobe(x, y, r, t, key='sg', shine=0.0, tilt=0.0):
    """snow globe; (x, y) = centre of the sphere. inside: tiny him and her side by side"""
    push()
    translate(x, y)
    rotate(tilt)
    boilSeed(key)
    paint([[-r * .95, r * .75], [r * .95, r * .75], [r * .8, r * 1.3], [-r * .8, r * 1.3]], wash='#B9784E', fill='#8A5A3C', fillOp=50, ink=INK, sw=1)
    G.c.save()
    pth = skia.Path()
    pth.addCircle(0, 0, r)
    G.c.clipPath(pth, skia.ClipOp.kIntersect, True)
    gradRect(-r, -r, 2 * r, 2 * r, ['#CFE8F8', '#F6E6F0'])
    flatRect(-r, r * .45, 2 * r, r, '#FFFFFF', .9)
    u = r / 11
    her(-r * .32, r * .52, u, dict(eyes='happy', mouth='smile', blush=.5, lite=True, noShadow=True, boilKey=key + 'h', aR=.6, hat=['beanieR', 'flowerB']))
    him(r * .32, r * .52, u, dict(eyes='happy', mouth='smile', blush=.3, lite=True, noShadow=True, boilKey=key + 'm', aL=.6, flip=True, hat=['beanieB']))
    for i in range(22):
        ph = frac(t * (.12 + .08 * hash1(i)) + hash1(i * 3.3))
        sx = (hash1(i * 7.1) - .5) * 1.8 * r + math.sin(t * 1.5 + i) * r * .08
        sy = lerp(-r, r * .5, ph)
        dot(sx, sy, r * .025 + 2, '#FFFFFF', .9)
    G.c.restore()
    paint(ellPts(0, 0, r, r, 40), wash='#DDEFFF', washOp=60, ink=INK, sw=1.1)
    paint(ellPts(-r * .42, -r * .45, r * .22, r * .12, 14, 0, -.7), wash='#FFFFFF', washOp=200, ink=None)
    pop()
    if shine > .02:
        sparkle(x + r * .6, y - r * .7, 26 * shine, '#FFFFFF', shine)
        sparkle(x - r * .7, y - r * .1, 18 * shine, '#FFFFFF', shine)


def battery2(x, y, s, frac_, blink=0.0, key='bat', red=0.0):
    boilSeed(key)
    w, h = 2.2 * s, 1.1 * s
    if red > .01:
        glow(x, y, 2.4 * s, '#FF4A4A', .7 * red)
    paint(rrPts(x - w / 2, y - h / 2, w, h, .2 * s), wash=mixCol('#FFFDF6', '#FF8A80', red), ink=mixCol(INK, '#D8394E', red), sw=1.1)
    paint(rrPts(x + w / 2, y - h * .22, .2 * s, h * .44, .06 * s), wash=INK, ink=None)
    col = '#E8574E' if frac_ < .25 else ('#F2C14E' if frac_ < .6 else '#7CC36B')
    if frac_ > .005 and blink < .5:
        fw = max(.16 * s, (w - .3 * s) * clamp(frac_))
        paint(rrPts(x - w / 2 + .15 * s, y - h / 2 + .15 * s, fw, h - .3 * s, .1 * s), wash=col, ink=None)
    pct = int(round(clamp(frac_) * 100))
    if pct > 0:
        text(f'{pct}%', x - w / 2 - .3 * s, y, s * .62, col if frac_ < .25 else INK, align='right', stroke='#FFFFFF', strokeW=8, shadow=False)


def signUp(sx, sy, w, h, txt, size, hx, hy, rot=0.0, key='su', tcol=HOT, col='#FFFDF6'):
    """a hand-held sign at (sx, sy) with its stick running down to the hand (hx, hy); draw BEFORE the character"""
    boilSeed(key + 's')
    inkLine([[sx, sy + h / 2 - 6], [hx, hy + 30]], 2.4, WOODDK, 'ink', 0)
    push()
    translate(sx, sy)
    rotate(rot)
    boilSeed(key)
    paint(rrPts(-w / 2, -h / 2, w, h, 16), wash=col, ink=INK, sw=1.1)
    text(txt, 0, 0, size, tcol, shadow=False)
    pop()


def zzz(x, y, s, t, t0, a=1.0):
    for i in range(3):
        ph = frac((t - t0) * .9 + i / 3)
        text('Z', x + i * s * .7 + ph * s * .6, y - ph * s * 2.2 - i * s * .5, s * (.75 + .3 * i), '#FFFFFF', shadow=False,
             stroke=INK, strokeW=s * .16, a=a * clamp(1.6 - ph * 1.6) * clamp((t - t0) * 8))


def muteIcon(x, y, s, k=1.0, key='mute'):
    """speaker with a red slash (painted: KuaiLe has no emoji)"""
    if k <= .01:
        return
    p = backOut(k)
    push()
    translate(x, y)
    scale(p)
    rotate(-.12)
    boilSeed(key)
    paint(ellPts(0, 0, 1.55 * s, 1.55 * s, 26), wash='#FFFDF6', ink=INK, sw=1.0)
    paint(rectPts(-.85 * s, -.32 * s, .45 * s, .64 * s, 1), wash=INK, ink=None)
    paint([[-.4 * s, -.32 * s], [.25 * s, -.8 * s], [.25 * s, .8 * s], [-.4 * s, .32 * s]], wash=INK, ink=None)
    inkLine([[-1.1 * s, 1.1 * s], [1.1 * s, -1.1 * s]], 2.6, '#E8476E', 'ink', 0)
    pop()


def sled(x, y, s, key='sled', front=True, back=True):
    """wooden sled seen from the side, facing right; (x, y) = runner bottom centre. back = rear board (draw before the rider),
    front = side board + runners (draw after; it covers the rider's lower body)"""
    boilSeed(key)
    if back:
        paint(rrPts(-2.4 * s + x, y - 1.95 * s, .5 * s, 1.3 * s, .15 * s), wash='#B9532F', ink=INK, sw=.8)
    if front:
        inkLine([[x - 2.6 * s, y], [x + 2.0 * s, y], [x + 2.6 * s, y - .35 * s], [x + 2.5 * s, y - .8 * s]], 2.2, '#5A566E', 'ink', .6)
        for sx in (-1.5, 0, 1.5):
            line(x + sx * s, y - .05 * s, x + sx * s, y - .55 * s, '#5A566E', 1, 5)
        paint(rrPts(x - 2.6 * s, y - 1.3 * s, 5.0 * s, .8 * s, .2 * s), wash='#D9774E', fill='#B85C3A', fillOp=60, ink=INK, sw=1.0)
        for i in range(4):
            line(x - 2.1 * s + i * 1.2 * s, y - 1.25 * s, x - 2.1 * s + i * 1.2 * s, y - .55 * s, '#B85C3A', .8, 3)
        inkLine([[x + 2.4 * s, y - 1.1 * s], [x + 3.4 * s, y - 1.5 * s], [x + 3.6 * s, y - 1.0 * s]], .9, '#E8B04A', 'ink', .5)


def auroraRibbon(P, col, a=1.0, hgt=180, key='au', reveal=1.0, wob=0.0, t=0.0):
    """a curtain of light hanging up from the polyline P (list of [x, y]); reveal 0..1 draws it from the first point"""
    if a <= .01 or reveal <= .01:
        return
    n = len(P)
    m = max(2, int(n * clamp(reveal)))
    # dense resampling (~7 px) so the curtain reads as soft light, not bars
    D = []
    for i in range(m - 1):
        x0, y0 = P[i]
        x1, y1 = P[i + 1]
        steps_ = max(1, int(math.hypot(x1 - x0, y1 - y0) / 7))
        for j in range(steps_):
            f = j / steps_
            D.append((lerp(x0, x1, f), lerp(y0, y1, f), i + f))
    G.c.save()
    pa = skia.Paint(AntiAlias=True, MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 5))
    pa.setBlendMode(skia.BlendMode.kScreen)
    for x, y, fi in D:
        y += math.sin(t * 2 + fi * .3) * wob
        hh = hgt * (.62 + .25 * math.sin(fi * .7 + t * 1.3) + .13 * math.sin(fi * 2.9 + 1))
        al = .34 + .12 * math.sin(fi * 1.7 + t)
        sh = skia.GradientShader.MakeLinear([skia.Point(x, y), skia.Point(x, y - hh)], [skcol(col, al * a), skcol(col, 0)])
        pa.setShader(sh)
        G.c.drawRect(skia.Rect.MakeXYWH(x - 6, y - hh, 12, hh + 6), pa)
    # bright lower edge
    pts = [[P[i][0], P[i][1] + math.sin(t * 2 + i * .3) * wob] for i in range(m)]
    if len(pts) > 1:
        pth = eng._path(through(pts, 4) if len(pts) > 3 else pts, False)
        G.c.drawPath(pth, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=10, Color=skcol(mixCol(col, '#FFFFFF', .5), .8 * a),
                                     MaskFilter=skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 6)))
    G.c.restore()


def lemniscate(cx, cy, a, n=80, squash=.55, rot=0.0, split=0.0, sep=0.0):
    """points of an infinity sign (Bernoulli lemniscate). split>0 opens a gap at the crossing; sep pushes the loops apart.
    Returns (left loop points, right loop points)"""
    L, R = [], []
    for i in range(n + 1):
        th = -math.pi / 2 + i / n * math.pi * 2
        d = 1 + math.sin(th) ** 2
        x = a * math.cos(th) / d
        y = a * math.sin(th) * math.cos(th) / d * squash * 2
        (R if x >= 0 else L).append([x, y, th])
    out = []
    for loop, sgn in ((L, -1), (R, 1)):
        pts = []
        for x, y, th in loop:
            if split > 0 and abs(x) < a * .06 * split:
                continue
            pts.append([cx + x + sgn * sep, cy + y])
        out.append(pts)
    return out


def northPole(x, y, h, t, glowK=0.0, key='np', night=1.0):
    """red-white striped pole with a gold ball and a sign 北极点; (x, y) = ground"""
    boilSeed(key + 'sh')
    paint(ellPts(x, y + 4, 80, 14, 16), fill=INK, fillOp=80, bleed=.25, ink=None, lite=True)
    w = 46
    boilSeed(key)
    paint(rectPts(x - w / 2, y - h, w, h, 1), wash='#FFFDF6', ink=INK, sw=1.0)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(x - w / 2, y - h, w, h))
    for i in range(-2, int(h / 60) + 3):
        yy = y - h + i * 60
        flat([[x - w / 2, yy], [x + w / 2, yy - 30], [x + w / 2, yy], [x - w / 2, yy + 30]], '#E8474E', .95)
    G.c.restore()
    paint(rectPts(x - w / 2, y - h, w, h, 1), ink=INK, sw=1.0)
    if glowK > .02:
        glow(x, y - h - 40, 260 * glowK, '#FFE36E', .9 * glowK)
    paint(ellPts(x, y - h - 38, 44, 44, 22), wash=mixCol('#E8B83A', '#FFF09A', glowK), fill='#C9922A', fillOp=60, ink=INK, sw=1.0)
    dot(x - 14, y - h - 52, 9, '#FFFFFF', .8)
    # sign
    push()
    translate(x + 4, y - h * .62)
    rotate(-.05)
    boilSeed(key + 's')
    paint(rrPts(-150, -50, 300, 100, 14), wash='#FFF5E2', fill='#E8D3B8', fillOp=50, ink=INK, sw=1.0)
    text('北极点', 0, 2, 56, '#C8324A', shadow=False)
    pop()


def footprints(pts, col='#B8C8E6', a=.8, key='fp'):
    for i, (x, y) in enumerate(pts):
        boilSeed(key + str(i))
        paint(ellPts(x, y, 30, 12, 12), wash=col, washOp=int(255 * a), ink=mixCol(col, INK, .4), sw=.4)


def arrowSign(x, y, k, txt='北极点', key='as'):
    """a wooden arrow sign pointing right on a stake (x, y) = ground; pops with k"""
    if k <= .01:
        return
    p = backOut(k)
    push()
    translate(x, y)
    scale(p)
    boilSeed(key)
    paint(rectPts(-9, -300, 18, 300), wash=WOODDK, ink=INK, sw=.8)
    paint([[-150, -380], [120, -380], [175, -330], [120, -280], [-150, -280]], wash='#FFF5E2', fill='#E8D3B8', fillOp=50, ink=INK, sw=1.1)
    text(txt, -20, -330, 54, '#C8324A', shadow=False)
    pop()


def plane(x, y, s, key='pl', rot=0.0):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rrPts(-2.2 * s, -.35 * s, 4.4 * s, .7 * s, .35 * s), wash='#FFFFFF', fill='#C9D3E6', fillOp=60, ink=INK, sw=.7)
    paint([[-.3 * s, 0], [.6 * s, 0], [-.5 * s, 1.5 * s], [-1.0 * s, 1.5 * s]], wash='#E8476E', ink=INK, sw=.6)
    paint([[-1.6 * s, -.2 * s], [-2.2 * s, -1.1 * s], [-1.8 * s, -1.1 * s], [-1.0 * s, -.2 * s]], wash='#E8476E', ink=INK, sw=.6)
    for i in range(3):
        dot(.6 * s + i * .45 * s, -.08 * s, .1 * s, '#5B7FC4')
    pop()


def snowMound(x, y, w, h, key='smd', night=0.0):
    boilSeed(key)
    col = mixCol(SNOW, '#9FB2DE', night * .6)
    pts = [[x + math.cos(a) * w / 2, y + math.sin(a) * h] for a in [math.pi + i / 18 * math.pi for i in range(19)]]
    paint(pts, wash=col, fill=mixCol(SNOWSH, '#5E72AE', night * .6), fillOp=60, ink=INK, sw=.8, curv=.4)


def snowBank(x0, x1, top, bottom, key='sbk', night=0.0):
    """a drift with a front edge (somewhere to sit); top = seat surface"""
    boilSeed(key)
    col = mixCol(SNOW, '#9FB2DE', night * .6)
    dk = mixCol(SNOWSH, '#5E72AE', night * .6)
    pts = [[x0 - 60, bottom], [x0, top + 30], [x0 + 60, top], [x1 - 60, top], [x1, top + 30], [x1 + 60, bottom]]
    paint(pts, wash=col, fill=dk, fillOp=60, ink=INK, sw=.9, curv=.4)


def snowSpray(x, y, s, a, n=10, key='spr', col='#FFFFFF'):
    """snow chunks flying out; a = seconds since the burst"""
    if a < 0 or a > .55:
        return
    for i in range(n):
        ang = -math.pi / 2 + (hash1(i * 3.3 + len(key)) - .5) * 2.4
        sp = (380 + 300 * hash1(i * 1.7)) * s
        px = x + math.cos(ang) * sp * a
        py = y + math.sin(ang) * sp * a + 900 * s * a * a
        dot(px, py, (7 + 5 * hash1(i)) * s * (1 - a / .55), col, .95)
        G.c.drawCircle(px, py, (7 + 5 * hash1(i)) * s * (1 - a / .55),
                       skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.5, Color=skcol(INK, .5)))
