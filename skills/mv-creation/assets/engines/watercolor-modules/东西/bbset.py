# bbset.py: 《病变》 v2 set dressing — the lived-in layer (string lights, calendar, clock, bedside table, rug, plant,
# bathroom with shower curtain, coat hooks, floor lamp, table-top clutter). No glass windows anywhere (user rule).
# The same small objects recur: S00 bedside → S01 → S02 → S16 (knocked-over clock, face-down frame, his pillow on the floor).
import math
from eng import *
import eng
from clawd import *
from props_bingbian import P2, alarmClock, photoFrame
from sets2 import fairyLights, wallClock, coffeeRing, ticketStub

WENKAI = 'LXGWWenKai-Regular.ttf'


def nightCol(col, night, to='#2E3460', k=.55):
    return mixCol(col, to, night * k)


# ---------------------------------------------------------------- loose pillow (his, thrown at the clock)
def pillowProp(x, y, w, h, rot=0.0, col=None, key='pil', sq=0.0, night=0.0):
    col = nightCol(col or P2['pillowHe'], night)
    push()
    translate(x, y)
    rotate(rot)
    scale(1 + sq * .5, 1 - sq)
    boilSeed(key)
    paint(rrPts(-w / 2, -h / 2, w, h, h * .42, 1.5), wash=col, fill=mixCol(col, INK, .2), fillOp=50, ink=INK, sw=1.1)
    inkLine([[-w * .32, -h * .05], [0, h * .05], [w * .32, -h * .05]], .6, mixCol(col, INK, .35), 'inkfine', .5)
    for sx in (-1, 1):
        inkLine([[sx * w * .5, -h * .38], [sx * w * .56, -h * .44]], .6, INK, 'inkfine', 0)
        inkLine([[sx * w * .5, h * .38], [sx * w * .56, h * .44]], .6, INK, 'inkfine', 0)
    pop()


# ---------------------------------------------------------------- bedside table (+ lamp, toppled clock, face-down frame)
def bedsideTable(x, y, s, night=0.0, key='bst', lampOn=1.0, clock='down', frame='down', lamp=True):
    """(x, y) = floor centre. About 7s wide, 6.4s tall. clock: 'up' / 'down' (knocked over) / None"""
    w, h = 7 * s, 6.4 * s
    wd = nightCol(P2['wood'], night, k=.5)
    boilSeed(key)
    for sx in (-1, 1):
        paint(rectPts(x + sx * (w / 2 - .7 * s) - .3 * s, y - .9 * s, .6 * s, .9 * s), wash=P2['woodDk'], ink=INK, sw=.8)
    paint(rectPts(x - w / 2, y - h, w, h - .8 * s, 2), wash=wd, fill=P2['woodDk'], fillOp=55, ink=INK, sw=1.1)
    paint(rectPts(x - w / 2 - .3 * s, y - h - .45 * s, w + .6 * s, .55 * s), wash=mixCol(wd, '#FFFFFF', .12), ink=INK, sw=1.0)
    paint(rectPts(x - w / 2 + .5 * s, y - h + .9 * s, w - s, 2.0 * s, 1), wash=mixCol(wd, '#FFFFFF', .08), ink=INK, sw=.8)
    paint(ellPts(x, y - h + 1.9 * s, .3 * s, .3 * s, 10), wash='#F2C53D', ink=INK, sw=.6)
    top = y - h - .45 * s
    if lamp:
        lx = x - w * .3
        boilSeed(key + 'lamp')
        paint(ellPts(lx, top - .2 * s, 1.0 * s, .3 * s, 14), wash='#8C7AA8', ink=INK, sw=.7)
        inkLine([[lx, top - .3 * s], [lx, top - 2.6 * s]], 1.4, INK, 'ink', 0)
        shade = [[lx - 1.3 * s, top - 2.4 * s], [lx + 1.3 * s, top - 2.4 * s], [lx + .8 * s, top - 4.4 * s], [lx - .8 * s, top - 4.4 * s]]
        paint(shade, wash=mixCol('#FFE6B0', '#7F86B8', night * .3 * (1 - lampOn)), fill='#E8B86A', fillOp=60, ink=INK, sw=.9)
        if lampOn > 0:
            glow(lx, top - 3.0 * s, 6 * s, '#FFD48A', .55 * lampOn)
    if clock == 'down':
        push()
        translate(x + w * .12, top - .9 * s)
        rotate(1.35)
        alarmClock(0, 0, .95 * s, 0, key=key + 'clk', hourA=7, minA=1)
        pop()
    elif clock == 'up':
        alarmClock(x + w * .12, top - 2.1 * s, .95 * s, 0, key=key + 'clk', hourA=7, minA=0)
    if frame == 'down':
        photoFrame(x + w * .38, top, .55 * s, fall=1.0, key=key + 'pf')
    elif frame == 'up':
        photoFrame(x + w * .38, top, .55 * s, fall=0.0, key=key + 'pf')
    return top


# ---------------------------------------------------------------- wall pieces
def wallClock2(x, y, r, hh, mm, night=0.0, key='wc'):
    """round wall clock showing hh:mm (7:01 in the morning shots, 11:02 at night)"""
    boilSeed(key)
    paint(ellPts(x, y, r, r, 24), wash=nightCol('#E8E1D2', night, k=.3), ink=INK, sw=1.0, lite=True)
    for i in range(12):
        a = i / 12 * TAU
        G.c.drawLine(x + math.cos(a) * r * .78, y + math.sin(a) * r * .78, x + math.cos(a) * r * .9, y + math.sin(a) * r * .9,
                     skia.Paint(AntiAlias=True, Color=skcol(INK, .7), StrokeWidth=2))
    ha = (hh % 12 + mm / 60) / 12 * TAU - math.pi / 2
    ma = mm / 60 * TAU - math.pi / 2
    inkLine([[x, y], [x + math.cos(ha) * r * .5, y + math.sin(ha) * r * .5]], 1.6, INK, 'ink', 0)
    inkLine([[x, y], [x + math.cos(ma) * r * .75, y + math.sin(ma) * r * .75]], 1.1, INK, 'ink', 0)


def calendar(x, y, s=1.0, night=0.0, key='cal', cross=0.0):
    """wall calendar; the 31st has a red heart (their day). cross 0..1 strikes the heart out."""
    boilSeed(key)
    w, h = 170 * s, 196 * s
    paint(rectPts(x - w / 2, y, w, h), wash=nightCol('#FFFDF6', night), ink=INK, sw=.8)
    paint(rectPts(x - w / 2, y, w, 48 * s), wash=nightCol('#D8546A', night, k=.35), ink=INK, sw=.6)
    text('10月', x, y + 25 * s, 30 * s, '#FFF6E8', face=WENKAI, shadow=False)
    G.c.drawCircle(x, y - 6 * s, 6 * s, skia.Paint(AntiAlias=True, Color=skcol(INK)))
    for r in range(5):
        for c_ in range(7):
            cx, cy = x - w / 2 + 16 * s + c_ * 23 * s, y + 66 * s + r * 26 * s
            if r == 4 and c_ == 4:
                paint(heartPts(cx, cy, 13 * s, 16), wash='#E0414F', ink=INK, sw=.5)
                if cross > 0:
                    L = 18 * s * ease(cross)
                    inkLine([[cx - L, cy - L], [cx + L, cy + L]], 1.4, INK, 'ink', 0)
            else:
                G.c.drawCircle(cx, cy, 2.6 * s, skia.Paint(AntiAlias=True, Color=skcol('#8A7A88', .7)))


def wallFrames(x, y, s=1.0, night=0.0, key='wf'):
    """two little framed pictures: a heart and her white flower"""
    for i, (dx, dy, w, h) in enumerate([(-70, 0, 110, 130), (70, 24, 96, 96)]):
        boilSeed(f'{key}{i}')
        cx, cy = x + dx * s, y + dy * s
        paint(rectPts(cx - w / 2 * s, cy - h / 2 * s, w * s, h * s), wash=nightCol('#B98352', night), ink=INK, sw=.8)
        paint(rectPts(cx - (w / 2 - 10) * s, cy - (h / 2 - 10) * s, (w - 20) * s, (h - 20) * s), wash=nightCol('#FBE7C4', night), ink=INK, sw=.5)
        if i == 0:
            paint(heartPts(cx, cy + 4 * s, 22 * s, 18), wash=nightCol('#F28FB0', night), ink=INK, sw=.5)
        else:
            flowerAt(cx, cy, 14 * s, 1.0, 1.0)


def plant(x, y, s=1.0, night=0.0, key='plant', sway=0.0):
    """(x, y) = floor centre; a leafy pot plant about 220 s tall"""
    boilSeed(key)
    leaf = nightCol('#6E9F58', night)
    lfdk = nightCol('#4A7A3E', night)
    for i in range(7):
        a = -math.pi / 2 + (i - 3) * .36 + sway * math.sin(G.T * 1.3 + i)
        L = (120 + 40 * hash1(i * 3.3)) * s
        bx, by = x, y - 70 * s
        tx, ty = bx + math.cos(a) * L, by + math.sin(a) * L
        nx, ny = -math.sin(a) * 26 * s, math.cos(a) * 26 * s
        mx, my = (bx + tx) / 2, (by + ty) / 2
        boilSeed(f'{key}l{i}')
        paint([[bx, by], [mx + nx, my + ny], [tx, ty], [mx - nx, my - ny]], wash=leaf, fill=lfdk, fillOp=50, ink=INK, sw=.7, curv=.5)
        inkLine([[bx, by], [tx, ty]], .5, lfdk, 'inkfine', .3)
    boilSeed(key + 'pot')
    paint([[x - 52 * s, y - 84 * s], [x + 52 * s, y - 84 * s], [x + 40 * s, y], [x - 40 * s, y]], wash=nightCol('#D98A5E', night), fill='#B0663E', fillOp=50, ink=INK, sw=.9)
    paint(rectPts(x - 58 * s, y - 96 * s, 116 * s, 18 * s), wash=nightCol('#E39A6E', night), ink=INK, sw=.8)


def rug(cx, cy, rx, ry, col='#E8B7C4', night=0.0, key='rug'):
    boilSeed(key)
    c = nightCol(col, night)
    paint(ellPts(cx, cy, rx, ry, 40), wash=c, fill=mixCol(c, INK, .15), fillOp=40, ink=INK, sw=.9)
    paint(ellPts(cx, cy, rx * .8, ry * .7, 36), ink=mixCol(c, '#FFFFFF', .5), sw=.8)


def stringLights(t, x0, x1, y, sag=40, n=16, key='sl', on=1.0, offFrom=None):
    """fairy lights; on 0..1; offFrom = (t_off, dir): bulbs pop off one by one across ~0.12 s from that time"""
    pts = [[lerp(x0, x1, i / 30), y + sag * math.sin(i / 30 * math.pi)] for i in range(31)]
    inkLine(pts, .7, '#3A3550', 'inkfine', .3)
    for i in range(n):
        k = (i + .5) / n
        bx, by = lerp(x0, x1, k), y + sag * math.sin(k * math.pi) + 10
        a = on
        if offFrom is not None:
            t0, d = offFrom
            j = i if d > 0 else n - 1 - i
            if t >= t0 + j * .12 / n:
                a = 0
        tw = .75 + .25 * math.sin(t * 2.2 + i * 1.7)
        if a > 0:
            glow(bx, by, 34 * tw, '#FFD27A', .55 * tw * a)
        G.c.drawCircle(bx, by, 5.5, skia.Paint(AntiAlias=True, Color=skcol(mixCol('#6A6688', '#FFF1C2', a))))


# ---------------------------------------------------------------- the bedroom (S01 / S16 framing: cam 980,620 ×1.18)
def bedroomBack(t, night=0.0, lights=1.0, lightsOff=None, cross=0.0, key='br'):
    """wall + decor + floor + rug + bedside table (his side, left) + his pillow on the floor + the bed (no pillow on his side).
    Returns pillow centres (pl, pr) of bedBack(1000, 900, 1120, 30)."""
    from props_bingbian import wallpaper, woodFloor, bedBack
    if night:
        wallpaper('#2F3358', '#383E68', key=key + 'wp')
    else:
        wallpaper('#E3ECF4', '#D3E0EC', key=key + 'wp')
        glow(1000, 330, 900, '#FFF1D2', .35)
    wallClock2(1000, 250, 46, 11 if night else 7, 2 if night else 1, night=night, key=key + 'wc')
    calendar(1650, 220, .9, night=night, key=key + 'cal', cross=cross)
    wallFrames(1660, 520, .75, night=night, key=key + 'wfr')
    stringLights(t, 450, 1550, 330, sag=48, n=18, key=key + 'sl', on=lights, offFrom=lightsOff)
    if night:
        woodFloor(840, col='#5A4E66', dk='#3E3550', key=key + 'fl')
    else:
        woodFloor(840, key=key + 'fl')
    rug(1000, 1010, 760, 80, night=night, key=key + 'rug')
    plant(1700, 905, .95, night=night, key=key + 'plant')
    lampOn = lights if night else .35
    if lightsOff is not None and t >= lightsOff[0]:
        lampOn = 0
    bedsideTable(285, 905, 26, night=night, key=key + 'bst', lampOn=lampOn)
    pillowProp(250, 925, 230, 110, rot=-.12, key=key + 'hp', night=night)
    pl, pr = bedBack(1000, 900, 1120, 30, key='bed1', night=night, skip=('he',))
    return pl, pr


# ---------------------------------------------------------------- bathroom doorway with a shower curtain (S05, replaces the window)
def duck(x, y, s, key='duck', tilt=0.0):
    push()
    translate(x, y)
    rotate(tilt)
    boilSeed(key)
    paint(ellPts(0, 0, 1.6 * s, 1.0 * s, 20), wash='#FFD94A', fill='#E8B020', fillOp=50, ink=INK, sw=.8)
    paint(ellPts(1.0 * s, -1.2 * s, .8 * s, .75 * s, 16), wash='#FFD94A', ink=INK, sw=.8)
    paint([[1.7 * s, -1.25 * s], [2.4 * s, -1.05 * s], [1.7 * s, -.9 * s]], wash='#F28C38', ink=INK, sw=.6)
    G.c.drawCircle(1.2 * s, -1.4 * s, .14 * s, skia.Paint(AntiAlias=True, Color=skcol(INK)))
    flowerAt(.6 * s, -1.9 * s, .45 * s, 1.0, .9)
    pop()


def bathDoorway(t, x0, x1, top, base, opn=0.0, key='bath'):
    """a door frame into the bathroom: tiles, a bathtub with her duck, and a pink shower curtain on a rail.
    opn 0..1 yanks the curtain to the LEFT (where he pulls it)."""
    w = x1 - x0
    boilSeed(key)
    flatRect(x0, top, w, base - top, '#CFE4EA')
    for r in range(int((base - top) / 46) + 1):
        inkLine([[x0, top + r * 46], [x1, top + r * 46]], .4, '#A9C6CF', 'inkfine', 0)
    for c_ in range(int(w / 46) + 1):
        inkLine([[x0 + c_ * 46, top], [x0 + c_ * 46, base]], .4, '#A9C6CF', 'inkfine', 0)
    # tub
    ty = base - 150
    boilSeed(key + 'tub')
    paint(rrPts(x0 + 20, ty, w - 40, 150, 40, 1), wash='#FFFDF8', fill='#D9E2E8', fillOp=50, ink=INK, sw=1.0)
    paint(rectPts(x0 + 14, ty - 8, w - 28, 22), wash='#FFFFFF', ink=INK, sw=.9)
    # bubbles + duck (her duck, wearing her flower)
    for i in range(6):
        boilSeed(f'{key}bb{i}')
        paint(ellPts(x0 + 60 + i * (w - 120) / 5, ty - 6 - 12 * hash1(i), 22 + 10 * hash1(i * 3), 16, 12), wash='#FFFFFF', ink=INK, sw=.5)
    duck(x0 + w * .68, ty - 20, 22, key=key + 'duck', tilt=.06 * math.sin(G.T * 3))
    # rail + curtain
    ry = top + 40
    inkLine([[x0 + 10, ry], [x1 - 10, ry]], 1.6, '#9A93A8', 'ink', 0)
    cw = lerp(w - 20, 70, opn)
    cx0 = x0 + 10
    pts = [[cx0, ry]]
    n = 9
    for i in range(n + 1):
        k = i / n
        pts.append([cx0 + cw * k, ry + (8 if i % 2 else 0)])
    pts.append([cx0 + cw + 6 * opn, base - 40])
    for i in range(n, -1, -1):
        k = i / n
        pts.append([cx0 + cw * k + 10 * math.sin(i * 1.7 + G.T * 6) * (1 - opn), base - 40 + (14 if i % 2 else 0)])
    boilSeed(key + 'cur')
    paint(pts, wash='#F7C6D2', fill='#E9A3B6', fillOp=60, ink=INK, sw=1.0)
    for i in range(1, n):
        xx = cx0 + cw * i / n
        inkLine([[xx, ry + 10], [xx + 4, base - 50]], .5, '#D98AA0', 'inkfine', .3)
    for i in range(n + 1):
        G.c.drawCircle(cx0 + cw * i / n, ry, 6, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.4, Color=skcol('#9A93A8')))
    # door frame (wood)
    boilSeed(key + 'frm')
    paint(rectPts(x0 - 26, top - 26, 26, base - top + 26), wash=P2['wood'], ink=INK, sw=1.0)
    paint(rectPts(x1, top - 26, 26, base - top + 26), wash=P2['wood'], ink=INK, sw=1.0)
    paint(rectPts(x0 - 26, top - 26, w + 52, 26), wash=P2['wood'], ink=INK, sw=1.0)


# ---------------------------------------------------------------- living room pieces (S06)
def coatHooks(x, y, s=1.0, key='hooks'):
    """two hooks by the door: his orange scarf on one; hers — just an empty hook and a little flower tag"""
    boilSeed(key)
    paint(rectPts(x - 110 * s, y, 220 * s, 34 * s), wash=P2['wood'], ink=INK, sw=.9)
    for i, hx in enumerate((x - 55 * s, x + 55 * s)):
        inkLine([[hx, y + 26 * s], [hx, y + 56 * s], [hx + 14 * s, y + 66 * s]], 1.6, '#6A6070', 'ink', .5)
    boilSeed(key + 'sc')
    hx = x - 55 * s
    sway = .04 * math.sin(G.T * 2)
    push()
    translate(hx, y + 58 * s)
    rotate(sway)
    paint([[-30 * s, 0], [30 * s, 0], [26 * s, 210 * s], [6 * s, 214 * s], [8 * s, 30 * s], [-8 * s, 30 * s], [-10 * s, 190 * s], [-30 * s, 186 * s]],
          wash='#E8743B', fill='#B9542A', fillOp=50, ink=INK, sw=.9)
    for j in range(4):
        inkLine([[-28 * s, 50 * s + j * 36 * s], [-10 * s, 50 * s + j * 36 * s]], .5, '#FFE2C8', 'inkfine', 0)
    pop()
    flowerAt(x + 55 * s, y + 17 * s, 12 * s, 1.0, .9)


def floorLamp(x, y, s=1.0, on=1.0, key='fl', col='#E8B86A', glowCol='#FFD48A'):
    boilSeed(key)
    paint(ellPts(x, y - 6 * s, 60 * s, 14 * s, 16), wash='#3A3550', ink=INK, sw=.8)
    inkLine([[x, y - 10 * s], [x, y - 420 * s]], 2.2, '#3A3550', 'ink', 0)
    shade = [[x - 85 * s, y - 400 * s], [x + 85 * s, y - 400 * s], [x + 55 * s, y - 520 * s], [x - 55 * s, y - 520 * s]]
    paint(shade, wash='#FFE6B0', fill=col, fillOp=60, ink=INK, sw=.9)
    if on > 0:
        glow(x, y - 440 * s, 380 * s, glowCol, .6 * on)


def shoes(x, y, s=1.0, key='shoes'):
    """his sneakers by the door (her slippers are gone)"""
    for i, dx in enumerate((-34, 34)):
        boilSeed(f'{key}{i}')
        paint([[x + (dx - 30) * s, y], [x + (dx - 30) * s, y - 22 * s], [x + (dx + 6) * s, y - 30 * s], [x + (dx + 34) * s, y - 14 * s], [x + (dx + 34) * s, y]],
              wash='#5B7FC4', ink=INK, sw=.8)
        inkLine([[x + (dx - 30) * s, y - 4 * s], [x + (dx + 34) * s, y - 4 * s]], .7, '#FFFFFF', 'inkfine', 0)


# ---------------------------------------------------------------- table-top clutter (S07)
def hairClip(x, y, s=1.0, rot=0.0, key='hc'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rrPts(-60 * s, -12 * s, 120 * s, 24 * s, 12 * s), wash='#F28FB0', fill='#D8648A', fillOp=50, ink=INK, sw=.8)
    for i in range(5):
        inkLine([[-48 * s + i * 24 * s, -10 * s], [-48 * s + i * 24 * s, 10 * s]], .5, '#FFFFFF', 'inkfine', 0)
    flowerAt(-40 * s, 0, 22 * s, 1.0, 1.0)
    pop()


def keys(x, y, s=1.0, rot=0.0, key='keys'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    G.c.drawCircle(0, 0, 30 * s, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4 * s, Color=skcol('#9A93A8')))
    for i, (a, col) in enumerate(((.3, '#D9B45A'), (1.4, '#B8C2D0'))):
        push()
        rotate(a)
        boilSeed(f'{key}{i}')
        paint(rrPts(26 * s, -12 * s, 34 * s, 24 * s, 8 * s), wash=col, ink=INK, sw=.6)
        paint([[58 * s, -6 * s], [120 * s, -6 * s], [120 * s, 2 * s], [110 * s, 2 * s], [110 * s, 10 * s], [96 * s, 10 * s], [96 * s, 6 * s], [58 * s, 6 * s]],
              wash=col, ink=INK, sw=.6)
        pop()
    paint(heartPts(-10 * s, 44 * s, 18 * s, 14), wash='#F28FB0', ink=INK, sw=.5)
    pop()


def movieTickets(x, y, rot=0.0, key='mt'):
    """two movie tickets for tonight (10/31 19:30) — two seats, one of them won't be used"""
    for i, (dx, dy, r) in enumerate(((0, 0, 0), (26, 20, .12))):
        push()
        translate(x + dx, y + dy)
        rotate(rot + r)
        boilSeed(f'{key}{i}')
        paint(rectPts(-120, -50, 240, 100), wash='#F2D9A8', fill='#E3C48A', fillOp=40, ink=INK, sw=.7)
        for j in range(9):
            G.c.drawCircle(66, -42 + j * 10.5, 2, skia.Paint(AntiAlias=True, Color=skcol('#8A6A4A', .7)))
        if i == 1:
            text('电影票', -30, -16, 28, '#6A4A3A', face=WENKAI, shadow=False)
            text('10/31 19:30', -30, 20, 22, '#8A6A4A', shadow=False)
            text(f'7排{8}座', 94, 0, 18, '#B8574E', face=WENKAI, shadow=False, rot=-math.pi / 2)
        pop()
