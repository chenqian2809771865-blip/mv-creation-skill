# sets2.py: second-pass sets for 《后来》 — front-facing room (her face visible behind the desk), a bench two Clawds fit on,
# a watering can drawn in world space, a much richer diary, a hilltop tree. Logical canvas 1920x1080.
import math
from eng import *
import eng
from clawd import *
from hl import *
from props import city, lamp as streetLamp


# ================================================================ seating
def seat(fn, x, seatTop, u, o=None):
    """seat a Clawd (her/him/her17/…): body bottom rests on seatTop, legs hang in front of the seat edge"""
    d = dict(o or {})
    d.setdefault('noShadow', True)
    fn(x, seatTop + 2.0 * u, u, d)
    if not d.get('noLegs'):
        boilSeed(f'sh{x:.0f}')
        paint(ellPts(x, seatTop - .1 * u, 4.6 * u, .45 * u, 16), fill=INK, fillOp=70, bleed=.2, ink=None, lite=True)


def parkBench(x, y, w, seatH, backH, key='pb', col='#B9784E', iron='#3A3550', night=0.0):
    """front-facing park bench. (x, y) = ground centre. returns seatTop. Draw characters after this."""
    c = mixCol(col, '#3A4278', night * .6)
    dk = mixCol(c, INK, .3)
    ir = iron
    st = y - seatH
    boilSeed(key)
    # back posts + slats
    for px in (x - w / 2 + 30, x + w / 2 - 30):
        paint(rectPts(px - 9, st - backH, 18, backH), wash=ir, ink=INK, sw=.8, lite=True)
    for k in range(3):
        yy = st - backH + 8 + k * (backH - 30) / 3
        paint(rectPts(x - w / 2 + 10, yy, w - 20, (backH - 30) / 3 - 10), wash=c, fill=dk, fillOp=50, ink=INK, sw=.8, lite=True)
    # legs
    for px in (x - w / 2 + 40, x + w / 2 - 40):
        paint(rectPts(px - 10, st, 20, seatH), wash=ir, ink=INK, sw=.8, lite=True)
        inkLine([[px - 40, y], [px, st + seatH * .4], [px + 40, y]], 1.6, ir, 'ink', .3)
    # arm rests (curly iron)
    for s_ in (-1, 1):
        ax = x + s_ * (w / 2 - 6)
        inkLine([[ax, st], [ax, st - backH * .45], [ax - s_ * 40, st - backH * .55], [ax - s_ * 60, st - backH * .42]], 2.4, ir, 'ink', .5)
    # seat: top surface (seen a little from above) + front edge
    paint([[x - w / 2, st - 16], [x + w / 2, st - 16], [x + w / 2 + 8, st], [x - w / 2 - 8, st]], wash=mixCol(c, '#FFFFFF', .15), ink=INK, sw=.8, lite=True)
    paint(rectPts(x - w / 2 - 8, st, w + 16, 22), wash=c, fill=dk, fillOp=70, ink=INK, sw=.9, lite=True)
    for k in range(1, 6):
        xx = x - w / 2 + k * w / 6
        G.c.drawLine(xx, st + 3, xx, st + 19, skia.Paint(AntiAlias=True, Color=skcol(dk, .5), StrokeWidth=1.5))
    return st - 4


# ================================================================ a watering can drawn in world space
def wateringCan(x, y, s, pour=0.0, facing=-1, key='wc'):
    """body centre (x, y); facing -1 = spout to the left. pour 0..1 tips the spout down. returns spout tip (world)"""
    push()
    translate(x, y)
    scale(facing, 1)
    ang = pour * .8
    rotate(ang)
    boilSeed(key)
    col, dk = '#7FB8C9', '#4E8AA0'
    # handle on the back/top
    inkLine([[-.9 * s, -.7 * s], [-.6 * s, -1.5 * s], [.4 * s, -1.5 * s], [.7 * s, -.7 * s]], 2.6, dk, 'ink', .6)
    # spout from the lower front up to the rose
    paint([[.8 * s, .25 * s], [2.3 * s, -.75 * s], [2.45 * s, -.55 * s], [.95 * s, .55 * s]], wash=dk, ink=INK, sw=.7, lite=True)
    paint(ellPts(2.42 * s, -.68 * s, .26 * s, .18 * s, 12, 0, -.6), wash=mixCol(dk, INK, .2), ink=INK, sw=.6, lite=True)
    # body
    paint(rrPts(-1.1 * s, -.8 * s, 2.2 * s, 1.6 * s, .35 * s), wash=col, fill=dk, fillOp=60, ink=INK, sw=.9, lite=True)
    paint(rectPts(-1.1 * s, -.1 * s, 2.2 * s, .22 * s), wash=mixCol(col, '#FFFFFF', .35), ink=None, lite=True)
    pop()
    tx, ty = 2.5 * s, -.7 * s
    ca, sa = math.cos(ang), math.sin(ang)
    rx, ry = tx * ca - ty * sa, tx * sa + ty * ca
    return x + facing * rx, y + ry


def waterStream(t, x0, y0, x1, y1, k=1.0, key='ws'):
    if k <= .02:
        return
    for i in range(10):
        ph = frac(t * 2.6 + i / 10)
        px = lerp(x0, x1, ph)
        py = lerp(y0, y1, ph) - 30 * math.sin(ph * math.pi) * (1 - ph)
        boilSeed(f'{key}{i}')
        paint(ellPts(px, py, 4.5 * k, 7 * k, 8), wash='#CFEAF8', washOp=int(230 * k), ink=None, lite=True)
    pa = skia.Paint(AntiAlias=True, Color=skcol('#CFEAF8', .45 * k), Style=skia.Paint.kStroke_Style, StrokeWidth=3)
    p = skia.Path()
    p.moveTo(x0, y0)
    p.quadTo((x0 + x1) / 2, min(y0, y1) - 10, x1, y1)
    G.c.drawPath(p, pa)


# ================================================================ the front-facing room (hers; his is the mirror image)
WALL = {'her': ('#2B3168', '#3E4482'), 'him': ('#22394F', '#355068')}
DESK_Y = 760           # desk top edge


def fairyLights(t, x0, x1, y, sag=40, n=16, key='fl', a=1.0):
    pts = [[lerp(x0, x1, i / 30), y + sag * math.sin(i / 30 * math.pi)] for i in range(31)]
    inkLine(pts, .7, '#3A3550', 'inkfine', .3)
    for i in range(n):
        k = (i + .5) / n
        bx, by = lerp(x0, x1, k), y + sag * math.sin(k * math.pi) + 10
        tw = .75 + .25 * math.sin(t * 2.2 + i * 1.7)
        glow(bx, by, 34 * tw, '#FFD27A', .55 * tw * a)
        G.c.drawCircle(bx, by, 5.5, skia.Paint(AntiAlias=True, Color=skcol('#FFF1C2', a)))


def bookshelf(x, y, w, h, key='bs', who='her', night=1.0):
    boilSeed(key)
    wood = '#6B4A3E'
    paint(rectPts(x, y, w, h), wash=mixCol(wood, '#2A2440', .35), ink=INK, sw=1.0, lite=True)
    rows = 3
    cols = ['#C8564F', '#5B7FC4', '#E8B04A', '#7FB1B5', '#9C8FE0', '#E89AAE', '#8AAE6A', '#D9C29A']
    for r in range(rows):
        sy = y + (r + 1) * h / rows
        paint(rectPts(x - 6, sy - 14, w + 12, 16), wash=wood, ink=INK, sw=.8, lite=True)
        bx = x + 14
        i = 0
        while bx < x + w - 30:
            hh = h / rows * (.55 + .3 * hash1(r * 17 + i))
            bw = 18 + 16 * hash1(r * 7 + i * 3)
            lean = .12 if hash1(r + i * 5) < .12 else 0
            if r == 0 and bx > x + w * .45:
                break
            push()
            translate(bx, sy - 14)
            rotate(lean)
            boilSeed(f'{key}b{r}{i}')
            paint(rectPts(0, -hh, bw, hh), wash=cols[(r * 3 + i) % len(cols)], ink=INK, sw=.6, lite=True)
            G.c.drawLine(3, -hh * .8, bw - 3, -hh * .8, skia.Paint(AntiAlias=True, Color=skcol('#FFF6E2', .6), StrokeWidth=2))
            pop()
            bx += bw + 3
            i += 1
    # top shelf extras
    if who == 'her':
        deerHatAlone(x + w * .72, y + h / rows - 14, 12, key=key + 'hat')
    else:
        boilSeed(key + 'pl')
        px, py = x + w * .72, y + h / rows - 50
        paint([[px - 70, py], [px + 70, py - 6], [px + 76, py + 6], [px - 64, py + 10]], wash='#E8E1D2', ink=INK, sw=.7, lite=True)
        paint([[px - 10, py - 4], [px + 20, py - 40], [px + 34, py - 36], [px + 16, py + 4]], wash='#E8E1D2', ink=INK, sw=.6, lite=True)
    # a small cactus pot on the middle shelf
    cx, cy = x + w - 60, y + 2 * h / rows - 14
    boilSeed(key + 'cac')
    paint([[cx - 20, cy - 34], [cx + 20, cy - 34], [cx + 15, cy], [cx - 15, cy]], wash='#D98A5E', ink=INK, sw=.6, lite=True)
    paint(rrPts(cx - 11, cy - 80, 22, 50, 10), wash='#6E9F58', ink=INK, sw=.6, lite=True)


def photoString(t, x0, x1, y, who='her', key='ps'):
    pts = [[lerp(x0, x1, i / 20), y + 26 * math.sin(i / 20 * math.pi)] for i in range(21)]
    inkLine(pts, .8, '#C9B08F', 'inkfine', .3)
    pics = 4
    for i in range(pics):
        k = (i + .5) / pics
        px, py = lerp(x0, x1, k), y + 26 * math.sin(k * math.pi)
        rot = (hash1(i * 3.1) - .5) * .25 + .02 * math.sin(t * .8 + i)
        push()
        translate(px, py + 6)
        rotate(rot)
        boilSeed(f'{key}{i}')
        paint(rectPts(-40, 0, 80, 92), wash='#FFFDF6', ink=INK, sw=.6, lite=True)
        x, yy, w, h = -32, 8, 64, 58
        if i == 0:
            gradRect(x, yy, w, h, ['#9FD4F2', '#F3E6C8'])
            gardeniaFlower(0, yy + 30, 20, 1, key=f'{key}g{i}')
        elif i == 1:
            gradRect(x, yy, w, h, ['#2A2D6E', '#6B5AA8'])
            for j in range(8):
                G.c.drawCircle(x + hash1(j * 2.2) * w, yy + hash1(j * 4.4) * h * .6, 1.6, skia.Paint(AntiAlias=True, Color=skcol('#FFF7DE')))
            paint(rectPts(x, yy + h * .75, w, h * .25), wash='#1D2F45', ink=None, lite=True)
        elif i == 2:
            gradRect(x, yy, w, h, ['#F7B98A', '#E58A8A'])
            clawd(-12, yy + h - 4, 4.2, dict(col=PINK, dk='#C0637B', lt='#FBD0DA', hat='flower', eyes='happy', mouth='smile', lite=True, noShadow=True, boilKey=f'{key}c1'))
            clawd(14, yy + h - 4, 4.2, dict(col=PAL['clay'], dk=PAL['clayDk'], lt='#F5B394', eyes='happy', mouth='smile', lite=True, noShadow=True, boilKey=f'{key}c2'))
        else:
            gradRect(x, yy, w, h, ['#BFE3F5', '#F2E6CF'])
            paint(rectPts(x + 8, yy + 20, 48, 26), wash='#E8574E', ink=INK, sw=.5, lite=True)
        # clothespin
        paint(rectPts(-6, -10, 12, 22), wash='#D9B45A', ink=INK, sw=.5, lite=True)
        pop()


def wallCalendar(x, y, key='cal'):
    boilSeed(key)
    paint(rectPts(x, y, 190, 220), wash='#FFFDF6', ink=INK, sw=.8, lite=True)
    paint(rectPts(x, y, 190, 54), wash='#C8564F', ink=INK, sw=.6, lite=True)
    text('10月', x + 95, y + 28, 32, '#FFF6E8', face=WENKAI, shadow=False)
    for r in range(5):
        for c in range(7):
            cx, cy = x + 18 + c * 26, y + 74 + r * 30
            G.c.drawCircle(cx, cy, 3, skia.Paint(AntiAlias=True, Color=skcol('#8A7A88', .7)))
    cx, cy = x + 18 + 2 * 26, y + 74 + 4 * 30
    inkLine([[cx - 12, cy], [cx, cy - 12], [cx + 12, cy], [cx, cy + 12], [cx - 12, cy]], .8, '#C8564F', 'inkfine', .7)
    G.c.drawCircle(x + 95, y - 6, 6, skia.Paint(AntiAlias=True, Color=skcol(INK)))


def wallClock(x, y, r, t, key='clk'):
    boilSeed(key)
    paint(ellPts(x, y, r, r, 24), wash='#E8E1D2', ink=INK, sw=1.0, lite=True)
    for i in range(12):
        a = i / 12 * TAU
        G.c.drawLine(x + math.cos(a) * r * .78, y + math.sin(a) * r * .78, x + math.cos(a) * r * .9, y + math.sin(a) * r * .9,
                     skia.Paint(AntiAlias=True, Color=skcol(INK, .7), StrokeWidth=2))
    hm = -math.pi / 2 + (11.5 / 12) * TAU
    mm = -math.pi / 2 + (t / 60) * TAU * .05 + 1.2
    inkLine([[x, y], [x + math.cos(hm) * r * .5, y + math.sin(hm) * r * .5]], 1.6, INK, 'ink', 0)
    inkLine([[x, y], [x + math.cos(mm) * r * .75, y + math.sin(mm) * r * .75]], 1.1, INK, 'ink', 0)


def roomBack(t, who='her', lampK=1.0, rainK=0.0, fogK=0.0, starsK=1.0, curtainSway=0.0, windowLight=1.0, moonXY=None):
    """back wall + window + shelves + wall decor of the front-facing room. Mirror for him."""
    mirror = who == 'him'
    c1, c2 = WALL[who]
    gradRect(-400, -400, W + 800, H + 800, [c1, c2])
    for i in range(-6, 40):
        x = i * 56
        G.c.drawRect(skia.Rect.MakeXYWH(x, -400, 22, 1100), skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .025)))
    # wainscot
    flatRect(-400, 600, W + 800, 200, mixCol(c2, INK, .25))
    G.c.drawLine(-400, 600, W + 400, 600, skia.Paint(AntiAlias=True, Color=skcol(mixCol(c2, '#FFFFFF', .2), .6), StrokeWidth=4))
    push()
    if mirror:
        translate(W, 0)
        scale(-1, 1)
    # window behind her
    wx, wy, ww, wh = 600, 70, 720, 430
    windowView(wx, wy, ww, wh, t, cityK=1.0, rainK=rainK, fogK=fogK, starsK=starsK, key='wb' + who, moonXY=moonXY or (wx + ww * .76, wy + wh * .25))
    windowFrame(wx, wy, ww, wh, '#6B4A3E' if not mirror else '#5A4A42', key='wbf' + who)
    if rainK > 0:
        for i in range(18):
            boilSeed(f'rd{who}{i}')
            yy = wy + 20 + ((hash1(i * 3.1) * (wh - 40) + t * 50 * (1 + hash1(i))) % (wh - 40))
            paint(ellPts(wx + 20 + hash1(i * 7.7) * (ww - 40), yy, 6, 9, 8), wash='#DDE8FA', washOp=int(170 * rainK), ink=None, lite=True)
    curtain(wx - 40, wy - 30, wh + 90, -1, curtainSway, '#8C7AA8' if not mirror else '#6F8A9A', key='cl' + who)
    curtain(wx + ww + 40, wy - 30, wh + 90, 1, curtainSway, '#8C7AA8' if not mirror else '#6F8A9A', key='cr' + who)
    fairyLights(t, wx - 60, wx + ww + 60, wy - 46, 34, 16, key='fl' + who)
    bookshelf(70, 150, 360, 450, key='bs' + who, who=who)
    photoString(t, 1440, 1840, 170, who, key='ps' + who)
    wallClock(1520, 330, 46, t, key='clk' + who)
    pop()
    wallCalendar(1680 if not mirror else W - 1680 - 190, 300, key='cal' + who)
    # chair back behind the sitter
    boilSeed('chb' + who)
    paint(rrPts(800, 560, 320, 230, 30), wash='#6B4A3E', fill='#4A2E22', fillOp=60, ink=INK, sw=1.0, lite=True)
    paint(rrPts(830, 590, 260, 170, 20), wash='#86593F', ink=INK, sw=.7, lite=True)


def deskFront(t, who='her', lampK=1.0, potOpen=0.0, potBuds=3, fullBloom=0.0, diary=True, mugSteam=1.0, diaryLift=0.0, extra=None):
    """the desk in the foreground with its things; drawn after the sitter"""
    mirror = who == 'him'
    push()
    if mirror:
        translate(W, 0)
        scale(-1, 1)
    y = DESK_Y
    boilSeed('dsk' + who)
    paint([[-100, y], [W + 100, y], [W + 100, y + 46], [-100, y + 46]], wash='#B98A60', fill='#8A5A3C', fillOp=50, ink=INK, sw=1.0)
    gradRect(-100, y + 46, W + 200, 400, ['#8A5A3C', '#5A3828'])
    inkLine([[-100, y + 46], [W + 100, y + 46]], 1.0, INK, 'ink', 0)
    for k in range(3):
        dx = 120 + k * 620
        paint(rectPts(dx, y + 80, 480, 120), wash='#7A5038', ink=INK, sw=.8, lite=True)
        paint(rrPts(dx + 210, y + 128, 60, 16, 8), wash='#D9B45A', ink=INK, sw=.6, lite=True)
    # lamp pool on the desk
    if lampK > 0:
        sh = skia.GradientShader.MakeRadial(skia.Point(1380, y + 20), 520, [skcol('#FFD48A', .32 * lampK), skcol('#FFD48A', 0)])
        G.c.drawRect(skia.Rect.MakeXYWH(700, y - 10, 1300, 70), skia.Paint(Shader=sh))
    # book stack (left)
    for i, (bw, col) in enumerate([(230, '#5B7FC4'), (210, '#C8564F'), (220, '#E8B04A')]):
        boilSeed(f'stk{who}{i}')
        paint(rectPts(120 + i * 6, y + 24 - (i + 1) * 30, bw, 30), wash=col, ink=INK, sw=.7, lite=True)
        G.c.drawLine(130 + i * 6, y + 24 - (i + 1) * 30 + 15, 110 + bw + i * 6, y + 24 - (i + 1) * 30 + 15, skia.Paint(AntiAlias=True, Color=skcol('#FFF6E2', .5), StrokeWidth=2))
    # gardenia pot
    potGardenia(560, y + 30, 32, potBuds, potOpen, key='pt' + who, night=.6)
    if fullBloom > 0:
        for i, dx in enumerate((-.8, .8)):
            gardeniaFlower(560 + dx * 32, y + 30 - 3.1 * 32 - (10 if i else 0), .6 * 32, fullBloom, key=f'pfb{who}{i}', col=mixCol(GARD, '#D8DEF5', .2))
    # diary lying open in front of the sitter
    if diary:
        boilSeed('dd' + who)
        cx = 960
        paint([[cx - 250, y + 34], [cx + 250, y + 34], [cx + 236, y + 4], [cx - 236, y + 4]], wash='#6E3B42', ink=INK, sw=.8, lite=True)
        for s_ in (-1, 1):
            lift = diaryLift if s_ > 0 else 0
            P = [[cx, y + 26], [cx + s_ * 120, y + 18 - 8], [cx + s_ * 236, y + 22 - lift * 60], [cx + s_ * 228, y - 2 - lift * 70], [cx + s_ * 110, y - 14], [cx, y - 6]]
            paint(P, wash=PAGE, fill=PAGE2, fillOp=60, ink=INK, sw=.7, curv=.25, lite=True)
            for r in range(3):
                G.c.drawLine(cx + s_ * 30, y + 2 + r * 7, cx + s_ * 200, y + 2 + r * 7 - (lift * 40 if s_ > 0 else 0),
                             skia.Paint(AntiAlias=True, Color=skcol('#9FB3D1', .45), StrokeWidth=1.4))
    # mug + pen pot
    mug(1300, y + 22, .85, key='mg' + who, steam=mugSteam, t=t)
    boilSeed('pp' + who)
    paint([[1418, y + 22], [1478, y + 22], [1472, y - 50], [1424, y - 50]], wash='#7FB1B5', ink=INK, sw=.7, lite=True)
    for i, (dx, col) in enumerate([(-14, '#C8564F'), (0, '#2C2C44'), (14, '#E8B04A')]):
        inkLine([[1448 + dx, y - 48], [1448 + dx * 1.6, y - 120 + i * 8]], 2.2, col, 'ink', 0)
    # the lamp (right)
    deskLamp(1760, y + 26, 1.3, lampK, key='lp' + who, flip=True)
    pop()
    if extra:
        extra()


# ================================================================ diary, second pass (rich, consistent props for S01 / S05 / S43)
def washi(x, y, w, h, rot, col, key='wt', pattern='dots', a=.72):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    zig = [[-w / 2, -h / 2]] + [[-w / 2 + (4 if i % 2 else 0), -h / 2 + i * h / 6] for i in range(1, 6)] + [[-w / 2, h / 2], [w / 2, h / 2]] + \
          [[w / 2 - (4 if i % 2 else 0), h / 2 - i * h / 6] for i in range(1, 6)] + [[w / 2, -h / 2]]
    paint(zig, wash=col, washOp=int(255 * a), ink=None, lite=True)
    if pattern == 'dots':
        for i in range(int(w // 18)):
            for j in range(2):
                G.c.drawCircle(-w / 2 + 10 + i * 18 + (j * 9), -h / 4 + j * h / 2, 2.6, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .6)))
    else:
        for i in range(int(w // 14)):
            G.c.drawLine(-w / 2 + i * 14, -h / 2, -w / 2 + i * 14 + 8, h / 2, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .35), StrokeWidth=4))
    pop()


def fakeText(x0, y0, w, size, n, seed, col='#6A5A70', a=.75, lineGap=1.7):
    """distant handwriting: n character cells of little strokes, wrapping at w"""
    pa = skia.Paint(AntiAlias=True, Color=skcol(col, a), StrokeWidth=max(1.2, size * .09), Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
    x, y = x0, y0
    for i in range(n):
        if x > x0 + w - size:
            x = x0
            y += size * lineGap
        h1 = hash1(seed * 13 + i * 3.7)
        if h1 < .07:
            x += size * .6
            continue
        k = 2 + int(hash1(seed + i * 5.1) * 3)
        for j in range(k):
            r1, r2, r3 = hash1(seed + i * 7 + j * 1.3), hash1(seed + i * 11 + j * 2.9), hash1(seed + i * 17 + j * 4.1)
            if r1 < .45:
                yy = y + size * (.15 + .7 * r2)
                G.c.drawLine(x + size * .1, yy, x + size * (.5 + .4 * r3), yy + size * .05, pa)
            elif r1 < .8:
                xx = x + size * (.15 + .7 * r2)
                G.c.drawLine(xx, y + size * .1, xx - size * .05, y + size * (.55 + .4 * r3), pa)
            else:
                G.c.drawLine(x + size * .2, y + size * .2 + r2 * size * .3, x + size * .75, y + size * .7, pa)
        x += size * 1.05


def ticketStub(x, y, rot, key='tk'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-110, -48, 220, 96), wash='#F2D9A8', ink=INK, sw=.7, lite=True)
    for i in range(9):
        G.c.drawCircle(60, -40 + i * 10, 2, skia.Paint(AntiAlias=True, Color=skcol('#8A6A4A', .7)))
    text('从前 → 后来', -28, -14, 26, '#6A4A3A', face=WENKAI, shadow=False)
    text('No.0717', -28, 22, 20, '#8A6A4A', shadow=False)
    text('票', 86, 0, 30, '#B8574E', face=WENKAI, shadow=False)
    pop()


def coffeeRing(x, y, r, a=.35):
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=skcol('#9A6A3A', a))
    pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 2.5))
    G.c.drawOval(skia.Rect.MakeXYWH(x - r, y - r * .96, 2 * r, 1.92 * r), pa)
    pa2 = skia.Paint(AntiAlias=True, Color=skcol('#C9A06A', a * .25))
    G.c.drawOval(skia.Rect.MakeXYWH(x - r, y - r * .96, 2 * r, 1.92 * r), pa2)


def pencilDoodle(kind, x, y, s, a=.6, col='#7A6A80'):
    pa = skia.Paint(AntiAlias=True, Color=skcol(col, a), StrokeWidth=2.2, Style=skia.Paint.kStroke_Style, StrokeJoin=skia.Paint.kRound_Join)
    p = skia.Path()
    if kind == 'star':
        pts = starPts(x, y, s, .45, 5)
        p.addPoly([skia.Point(*q) for q in pts], True)
    elif kind == 'heart':
        pts = heartPts(x, y, s, 24)
        p.addPoly([skia.Point(*q) for q in pts], True)
    elif kind == 'moon':
        p.addArc(skia.Rect.MakeXYWH(x - s, y - s, 2 * s, 2 * s), 60, 250)
        p.addArc(skia.Rect.MakeXYWH(x - s * .55, y - s * 1.0, 1.6 * s, 1.6 * s), 290, -200)
    G.c.drawPath(p, pa)


def inkBottle(x, y, key='ib'):
    boilSeed(key)
    paint(rrPts(x - 52, y - 52, 104, 104, 18), wash='#3A3A5A', fill='#1E1E36', fillOp=80, ink=INK, sw=.9)
    paint(ellPts(x, y, 30, 30, 18), wash='#2A2238', ink=INK, sw=.8)
    paint(rectPts(x - 48, y + 14, 96, 30), wash='#E8D9B8', ink=INK, sw=.5, lite=True)
    text('INK', x, y + 29, 18, '#3A3A5A', shadow=False)
    paint(ellPts(x - 12, y - 12, 8, 5, 8, 0, -.6), wash='#FFFFFF', washOp=120, ink=None, lite=True)


def teacupTop(x, y, t, key='tc'):
    boilSeed(key)
    paint(ellPts(x, y, 96, 90, 28), wash='#F2EEE6', fill='#D9D2C2', fillOp=50, ink=INK, sw=.8)
    paint(ellPts(x, y, 64, 60, 24), wash='#FFFDF6', ink=INK, sw=.8)
    paint(ellPts(x, y, 50, 46, 24), wash='#C98A3A', fill='#A86A2A', fillOp=60, ink=None)
    paint(ellPts(x - 14, y - 12, 14, 6, 10, 0, -.4), wash='#FFE2A8', washOp=180, ink=None, lite=True)
    inkLine([[x + 62, y - 8], [x + 92, y - 14], [x + 92, y + 12], [x + 62, y + 10]], 1.6, INK, 'ink', .5)
    for i in range(2):
        ph = frac(t * .3 + i * .5)
        inkLine([[x - 10 + i * 24, y - 10], [x - 20 + i * 24 + math.sin(t + i) * 12, y - 60 - ph * 40], [x - 4 + i * 24, y - 110 - ph * 50]], .8,
                mixCol('#FFFFFF', '#C9B08F', .3), 'inkfine', .6)


def loosePetals(pts, key='lp'):
    for i, (x, y, r, rot) in enumerate(pts):
        boilSeed(f'{key}{i}')
        P = [[x + math.cos(rot) * r, y + math.sin(rot) * r * .5], [x + math.cos(rot + 1.6) * r * .35, y + math.sin(rot + 1.6) * r * .3],
             [x - math.cos(rot) * r * .8, y - math.sin(rot) * r * .4], [x + math.cos(rot - 1.6) * r * .35, y + math.sin(rot - 1.6) * r * .3]]
        paint(P, wash='#E8D9B5', fill='#C9AE80', fillOp=60, ink='#A89272', sw=.5, curv=.6, lite=True)


def pencil(x, y, ang, L=300, key='pc'):
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    paint(rectPts(-L / 2, -9, L, 18), wash='#E8B04A', ink=INK, sw=.7, lite=True)
    paint([[L / 2, -9], [L / 2 + 34, 0], [L / 2, 9]], wash='#F2D9A8', ink=INK, sw=.6, lite=True)
    paint([[L / 2 + 22, -3], [L / 2 + 34, 0], [L / 2 + 22, 3]], wash=INK, ink=None, lite=True)
    paint(rectPts(-L / 2 - 26, -9, 26, 18), wash='#F59BB0', ink=INK, sw=.6, lite=True)
    paint(rectPts(-L / 2 - 6, -10, 8, 20), wash='#B8B8C8', ink=INK, sw=.5, lite=True)
    pop()


def polaroidTop(x, y, rot, key='pt', draw=None):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-110, -120, 220, 250), wash='#FFFDF6', fill='#E8E0CC', fillOp=40, ink=INK, sw=.8)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(-92, -102, 184, 170))
    if draw:
        draw(-92, -102, 184, 170)
    G.c.restore()
    pop()


def coupleSnap(x, y, w, h, night=False):
    gradRect(x, y, w, h, ['#2A2D6E', '#6B5AA8'] if night else ['#9FD4F2', '#F3E6C8'])
    clawd(x + w * .36, y + h * .9, 6.5, dict(col=PINK, dk='#C0637B', lt='#FBD0DA', hat='flower', eyes='happy', mouth='smile', lite=True, noShadow=True, boilKey='cs1'))
    clawd(x + w * .66, y + h * .9, 6.5, dict(col=PAL['clay'], dk=PAL['clayDk'], lt='#F5B394', eyes='happy', mouth='smile', lite=True, noShadow=True, boilKey='cs2'))


DIARY2 = dict(cx=960, cy=560, w=1440, h=840, tilt=-.03)


def deskTop(t, lampK=1.0):
    """the desk seen from above with the same things every time the diary is shown"""
    desk()
    glow(1720, 40, 1100, '#FFC976', .7 * lampK)
    # lamp base in the top-right corner
    boilSeed('lbase')
    paint(ellPts(1830, 90, 120, 110, 24), wash='#3A3550', fill='#2A2440', fillOp=60, ink=INK, sw=1.0)
    inkLine([[1830, 90], [1700, -60]], 6, '#3A3550', 'ink', 0)
    teacupTop(170, 170, t)
    inkBottle(1790, 760)
    loosePetals([(120, 760, 26, .4), (210, 860, 22, 2.1), (1700, 330, 24, 1.2), (1640, 980, 20, 2.8), (80, 520, 18, .9)])
    polaroidTop(140, 980, .35, key='ptd', draw=lambda x, y, w, h: coupleSnap(x, y, w, h))
    pencil(1660, 560, 1.2, 280, key='pcl')


def pageDecor(mode, t, title=1.0, dateK=1.0, creditK=1.0):
    """decorations on the open spread, in the diary's own (untilted) frame"""
    cx, cy, w, h = DIARY2['cx'], DIARY2['cy'], DIARY2['w'], DIARY2['h']
    L0, R0 = cx - w / 2, cx
    top = cy - h / 2
    if mode == 'now':
        # left page: the pressed gardenia under tape, a ticket stub, faded lines, page number 17
        fakeText(L0 + 70, top + 70, w / 2 - 140, 22, 46, 3, a=.45)
        gardeniaFlower(L0 + 300, cy + 120, 110, 1, key='dpf', rot=.7, dry=True)
        boilSeed('dst')
        inkLine([[L0 + 310, cy + 210], [L0 + 250, cy + 300], [L0 + 220, cy + 350]], 1.2, '#8E7A4E', 'ink', .4)
        washi(L0 + 230, cy + 40, 170, 38, -.5, '#F59BB0', 'wt1', 'dots')
        washi(L0 + 380, cy + 230, 150, 34, .35, '#9FD8C8', 'wt2', 'stripes')
        ticketStub(L0 + 520, cy + 300, -.12, 'tk1')
        pencilDoodle('star', L0 + 560, top + 330, 30)
        text('17', L0 + 60, cy + h / 2 - 40, 24, '#9A8A90', shadow=False)
        # right page: date, the title, a ring stain, pencil credit
        coffeeRing(R0 + 600, cy + 300, 70)
        size = 260
        x0 = R0 + 375 - writeW('后来', size) / 2
        inkWrite('后来', x0, top + 210, size, title)
        if title >= 1:
            ul = skia.Paint(AntiAlias=True, Color=skcol('#3A3050', .55), StrokeWidth=3, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
            k = ease(seg(t, B_title_end(), B_title_end() + .6))
            p = skia.Path()
            p.moveTo(x0 + 10, top + 500)
            p.quadTo(R0 + 375, top + 520, x0 + 10 + (writeW('后来', size) - 20) * k, top + 498)
            G.c.drawPath(p, ul)
        wtext('十月二十八日 · 夜', R0 + 375, top + 130, 38, '#6A5A70', .85 * dateK)
        fakeText(R0 + 90, top + 580, w / 2 - 180, 22, 30, 9, a=.35 * dateK)
        wtext('刘若英《后来》', R0 + 600, cy + h / 2 - 50, 28, '#8E8090', .75 * creditK)
        pencilDoodle('moon', R0 + 120, cy + h / 2 - 70, 26, .5 * creditK)
    elif mode == 'old':
        fakeText(R0 + 90, top + 220, w / 2 - 180, 24, 60, 21, col='#5B4A66', a=.6)
        wtext('十七岁 · 夏', R0 + 375, top + 120, 54, '#5B4A66', .9)
        loosePetals([(R0 + 560, cy + 290, 40, .6)], key='opp')
        washi(R0 + 560, cy + 250, 120, 30, .2, '#F7D36E', 'wt3', 'dots')
        pencilDoodle('heart', R0 + 180, cy + 300, 34, .7, '#C0637B')
        for i, (sx, sy) in enumerate([(R0 + 650, top + 90), (R0 + 90, top + 110), (R0 + 400, cy + 330)]):
            boilSeed(f'stk{i}')
            paint(starPts(sx, sy, 20, .45, 5), wash='#F7D36E', ink=INK, sw=.5, lite=True)
        text('17', R0 + w / 2 - 60, cy + h / 2 - 40, 24, '#9A8A90', shadow=False)
    elif mode == 'first':
        wtext('十七岁 · 仲夏', R0 + 375, top + 90, 40, '#5B4A66', .85)
        for i, (sx, sy) in enumerate([(R0 + 660, top + 70), (L0 + 70, top + 60)]):
            boilSeed(f'fs{i}')
            paint(starPts(sx, sy, 18, .45, 5), wash='#F7D36E', ink=INK, sw=.5, lite=True)


_TE = [None]


def B_title_end():
    if _TE[0] is None:
        from common import B
        _TE[0] = B[8]
    return _TE[0]


def diaryNow(t, lampK=1.0, title=1.0, dateK=1.0, creditK=1.0, mode='now', pressed=False, leftAge=0.0):
    deskTop(t, lampK)
    d = DIARY2
    diarySpread(d['cx'], d['cy'], d['w'], d['h'], d['tilt'], pressed=pressed, leftAge=leftAge)
    push()
    translate(d['cx'], d['cy'])
    rotate(d['tilt'])
    translate(-d['cx'], -d['cy'])
    pageDecor(mode, t, title, dateK, creditK)
    pop()
    fountainPen(1560, 930, -.5)
    if lampK < 1:
        tint('#3A4488', .55 * (1 - lampK))
    vignette(.42)


# ================================================================ yard, second pass: more of the school
def bike(x, y, s, col='#5B7FC4', key='bk', flip=False):
    push()
    translate(x, y)
    if flip:
        scale(-1, 1)
    boilSeed(key)
    for cx in (-1.3 * s, 1.3 * s):
        paint(ellPts(cx, -s, s, s, 22), ink=INK, sw=1.2, lite=True)
        G.c.drawLine(cx - s * .9, -s, cx + s * .9, -s, skia.Paint(AntiAlias=True, Color=skcol(INK, .3), StrokeWidth=1.2))
        G.c.drawLine(cx, -1.9 * s, cx, -.1 * s, skia.Paint(AntiAlias=True, Color=skcol(INK, .3), StrokeWidth=1.2))
    for a_, b_ in (((-1.3 * s, -s), (0, -s)), ((0, -s), (-.5 * s, -2.0 * s)), ((-.5 * s, -2.0 * s), (.9 * s, -1.9 * s)), ((.9 * s, -1.9 * s), (0, -s)),
                   ((1.3 * s, -s), (1.0 * s, -2.2 * s)), ((-1.3 * s, -s), (-.5 * s, -2.0 * s))):
        inkLine([list(a_), list(b_)], 2.0, col, 'ink', 0)
    inkLine([[.8 * s, -2.3 * s], [1.25 * s, -2.35 * s]], 2.0, INK, 'ink', 0)
    paint(rrPts(-.75 * s, -2.12 * s, .55 * s, .14 * s, .05 * s), wash=INK, ink=None, lite=True)
    paint(rectPts(.75 * s, -1.85 * s, .55 * s, .4 * s), wash='#C9B08F', ink=INK, sw=.5, lite=True)
    pop()


def butterfly(x, y, s, t, key='bf', col='#F7D36E'):
    flap = abs(math.sin(t * 9))
    boilSeed(key)
    for sx in (-1, 1):
        paint(ellPts(x + sx * s * .55 * (.4 + .6 * flap), y - s * .2, s * .55 * (.4 + .6 * flap), s * .5, 10), wash=col, ink=INK, sw=.5, lite=True)
        paint(ellPts(x + sx * s * .4 * (.4 + .6 * flap), y + s * .35, s * .38 * (.4 + .6 * flap), s * .3, 10), wash=mixCol(col, '#FFFFFF', .3), ink=INK, sw=.5, lite=True)
    G.c.drawLine(x, y - s * .5, x, y + s * .5, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=2))


def bigTreeSide(x, y, s, t, key='bt', col='#5E9E5A', dk='#2F6440', night=0.0, flowers=False):
    """a big leafy tree; (x, y) = trunk base"""
    c = mixCol(col, '#1E3550', night * .75)
    d = mixCol(dk, '#101C34', night * .75)
    boilSeed(key)
    trunk = mixCol('#7A5238', '#2A2238', night * .6)
    paint([[x - .45 * s, y], [x - .3 * s, y - 2.6 * s], [x - .9 * s, y - 3.6 * s], [x - .6 * s, y - 3.8 * s], [x, y - 3.0 * s], [x + .5 * s, y - 3.9 * s],
           [x + .85 * s, y - 3.7 * s], [x + .35 * s, y - 2.5 * s], [x + .5 * s, y]], wash=trunk, fill=mixCol(trunk, INK, .3), fillOp=70, ink=INK, sw=1.1, curv=.2)
    for k in range(5):
        boilSeed(f'{key}c{k}')
        cx = x + (k - 2) * .95 * s + math.sin(t * .6 + k) * 4
        cy = y - 4.4 * s - (1 - abs(k - 2) / 2) * .9 * s
        r = s * (1.35 - abs(k - 2) * .12)
        P = []
        for i in range(30):
            a = i / 30 * TAU
            rr = r * (1 + .13 * abs(math.sin(a * 3.5 + k)))
            P.append([cx + math.cos(a) * rr, cy + math.sin(a) * rr * .8])
        paint(P, wash=c, fill=d, fillOp=90, ink=INK, sw=1.0, curv=.3)
    for i in range(14):
        hx, hy = hash1(i * 3.3 + 7), hash1(i * 5.9 + 1)
        boilSeed(f'{key}h{i}')
        paint(ellPts(x + (hx - .5) * 4.6 * s, y - 4.6 * s + (hy - .5) * 2.2 * s, s * .32, s * .2, 10), wash=mixCol(c, '#CFEAA0', .3 * (1 - night)), washOp=140, ink=None, lite=True)
    if flowers:
        for i in range(10):
            hx, hy = hash1(i * 4.1 + 2), hash1(i * 6.3 + 5)
            gardeniaFlower(x + (hx - .5) * 4 * s, y - 4.5 * s + (hy - .5) * 1.8 * s, s * .16, 1, key=f'{key}f{i}', col=mixCol(GARD, '#C9D3F0', night * .4))


def yardDetail(t, mode='day', key='ydx'):
    """extra life in the school yard: flagpole, bikes, a notice board, lamp post, butterflies, path tiles"""
    night = 1.0 if mode == 'night' else 0.0
    dusk = 1.0 if mode == 'dusk' else 0.0
    # flagpole behind the hedge
    boilSeed(key + 'fp')
    paint(rectPts(1560, 20, 12, 560), wash='#C9C2B4', ink=INK, sw=.8, lite=True)
    fl = [[1572, 40]] + [[1572 + i * 26, 40 + 10 * math.sin(t * 3 + i * .9) + i * 1.5] for i in range(1, 7)] + \
         [[1572 + i * 26, 110 + 10 * math.sin(t * 3 + i * .9) + i * 1.5] for i in range(6, 0, -1)] + [[1572, 110]]
    paint(fl, wash=mixCol('#E8474E', '#5A2A4A', night * .7), ink=INK, sw=.8, curv=.3, lite=True)
    # notice board on the low wall
    boilSeed(key + 'nb')
    paint(rectPts(250, 470, 260, 170), wash=mixCol('#4E7A5A', '#1E2A40', night * .7), ink=INK, sw=1.0, lite=True)
    for i, (px, py, pc) in enumerate([(275, 490, '#FFF6E2'), (370, 500, '#F7D36E'), (440, 488, '#BFE3F5'), (300, 570, '#F59BB0')]):
        paint(rectPts(px, py, 70, 60), wash=mixCol(pc, '#3A4278', night * .6), ink=INK, sw=.5, lite=True)
    text('栀子花开', 380, 455, 30, mixCol('#FFF5E2', '#9FA8D8', night * .5), face=WENKAI, shadow=False)
    # parked bikes along the wall (left)
    for i in range(3):
        bike(80 + i * 120, 770, 34, ['#5B7FC4', '#E8574E', '#7FB1B5'][i], key=f'{key}bk{i}', flip=i % 2 == 1)
    # path tiles
    for i in range(14):
        y = 820 + i * i * 2.4
        if y > 1100:
            break
        G.c.drawLine(-200, y, W + 200, y, skia.Paint(AntiAlias=True, Color=skcol(INK, .07), StrokeWidth=2))
    for i in range(-10, 30):
        x0 = 960 + (i - 10) * 70
        G.c.drawLine(960 + (x0 - 960) * .45, 790, x0 + (x0 - 960) * .9, 1100, skia.Paint(AntiAlias=True, Color=skcol(INK, .05), StrokeWidth=2))
    if mode == 'day':
        butterfly(1380 + 120 * math.sin(t * .7), 640 + 50 * math.sin(t * 1.3), 20, t, key=key + 'b1')
        butterfly(420 + 90 * math.sin(t * .9 + 2), 600 + 40 * math.cos(t * 1.1), 16, t + .3, key=key + 'b2', col='#F59BB0')
    # the big tree framing the right edge
    bigTreeSide(1870, 860, 120, t, key=key + 'tr', night=night * .9 + dusk * .3)
    if mode in ('night', 'dusk'):
        streetLamp(1660, 900, 48, 1.0, key=key + 'lp')


# ================================================================ the hilltop under the tree (S10 / S11, cover)
def hillTreeScene(t, nightK=1.0, key='hts', milky=1.0, starsK=1.0, horizon=760, tree=True, moonK=1.0):
    hillSet(t, nightK, key=key, milky=milky, starsK=starsK, horizon=horizon)
    # moon low over the town + its path on the river
    if moonK > 0 and nightK > .3:
        mx, my = 1540, 330
        glow(mx, my, 320, '#E8E4FF', .5 * moonK * nightK)
        boilSeed(key + 'mn')
        paint(ellPts(mx, my, 62, 62, 30), wash='#FFF8E4', washOp=int(255 * moonK), ink=None)
        paint(ellPts(mx + 16, my - 10, 12, 9, 10), wash='#EDE6D0', washOp=int(150 * moonK), ink=None, lite=True)
    # river band in front of the town
    rc = mixCol('#F2B27E', '#2A3478', nightK)
    boilSeed(key + 'rv')
    paint([[-300, horizon + 20], [W + 300, horizon + 4], [W + 300, horizon + 46], [-300, horizon + 64]], wash=rc, ink=None, lite=True)
    for i in range(12):
        x = 1540 + (hash1(i * 2.7) - .5) * 160
        y = horizon + 14 + hash1(i * 5.1) * 40
        G.c.drawLine(x - 30, y, x + 30, y, skia.Paint(AntiAlias=True, Color=skcol('#FFF6D8', .5 * nightK * moonK), StrokeWidth=3))
    if tree:
        bigTreeSide(560, hillY(560, horizon) + 30, 118, t, key=key + 'tree', night=nightK * .85, flowers=True)
        fireflies(t, 19, 14, 300, 120, 860, 620, nightK)
    # small white flowers in the grass
    for i in range(30):
        x = -100 + hash1(i * 2.3 + 9) * (W + 200)
        y = hillY(x, horizon) + 40 + hash1(i * 6.1) * 300
        boilSeed(f'{key}gf{i}')
        paint(ellPts(x, y, 6, 5, 8), wash=mixCol('#FFFDF4', '#B8C0E0', nightK * .5), ink=None, lite=True)


# ================================================================ the hill, third pass: a real slope above the town
HILL_TOP = (700, 700)


def hillY2(x):
    """ground height of the hill at x (top near x=700, falls away to both sides, steeper to the right)"""
    tx, ty = HILL_TOP
    d = x - tx
    if d < 0:
        return ty + 0.00022 * d * d + 30 * (1 - math.exp(-abs(d) / 400))
    return ty + 0.00045 * d * d


def nightHill(t, nightK=1.0, key='nh', milky=1.0, starsK=1.0, moonK=1.0, tree=True, flowers=True):
    top = mixCol('#E28B6A', '#0C1140', nightK)
    mid = mixCol('#F2B27E', '#26306E', nightK)
    low = mixCol('#FBD6A0', '#46468A', nightK)
    gradRect(-500, -900, W + 1000, 1800, [top, mid, low])
    if nightK > .2:
        push()
        translate(120, -60)
        milkyWay(milky * clamp((nightK - .2) / .8))
        pop()
        stars(t, 7, 190, -400, -800, W + 400, 780, starsK * clamp((nightK - .1) / .9), 3.0)
    if nightK < .6:
        glow(1500, 760, 700, '#FFC48A', .7 * (1 - nightK / .6))
    # moon
    if moonK > 0 and nightK > .3:
        mx, my = 1560, 300
        glow(mx, my, 330, '#E8E4FF', .5 * moonK * nightK)
        boilSeed(key + 'mn')
        paint(ellPts(mx, my, 64, 64, 30), wash='#FFF8E4', washOp=int(255 * moonK), ink=None)
        paint(ellPts(mx + 18, my - 12, 12, 9, 10), wash='#EDE6D0', washOp=int(150 * moonK), ink=None, lite=True)
    # far mountains, the town and the river below the hill
    boilSeed(key + 'mt')
    P = [[-300, 900], [-300, 760]] + [[-300 + i * 120, 760 - 60 * abs(math.sin(i * .7)) - 30 * hash1(i * 3.3)] for i in range(23)] + [[W + 300, 900]]
    paint(P, wash=mixCol('#9A7A9A', '#1C2252', nightK), ink=None, lite=True)
    flatRect(-300, 790, W + 600, 110, mixCol('#7C6A8E', '#1A1E48', nightK))
    for i in range(70):
        x = -200 + hash1(i * 3.1) * (W + 400)
        y = 800 + hash1(i * 5.3) * 40
        on = .55 + .45 * math.sin(t * (1 + hash1(i)) + i)
        G.c.drawCircle(x, y, 2.4, skia.Paint(AntiAlias=True, Color=skcol(['#FFD98A', '#FFB98A', '#FFF1C2'][i % 3], (.6 + .4 * on) * nightK)))
    rc = mixCol('#F2B27E', '#2A3478', nightK)
    gradRect(-300, 880, W + 600, 700, [mixCol('#8A7A70', '#1A2240', nightK), mixCol('#6A5A50', '#10162E', nightK)])
    for i in range(40):
        x = -200 + hash1(i * 7.3) * (W + 400)
        y = 900 + hash1(i * 2.9) * 180
        G.c.drawCircle(x, y, 2.0, skia.Paint(AntiAlias=True, Color=skcol('#FFD98A', .5 * nightK)))
    boilSeed(key + 'rv')
    paint([[-300, 848], [W + 300, 840], [W + 300, 884], [-300, 896]], wash=rc, ink=None, lite=True)
    for i in range(14):
        x = 1560 + (hash1(i * 2.7) - .5) * 180
        y = 852 + hash1(i * 5.1) * 34
        G.c.drawLine(x - 34, y, x + 34, y, skia.Paint(AntiAlias=True, Color=skcol('#FFF6D8', .55 * nightK * moonK), StrokeWidth=3))
    # the hill itself
    hc = mixCol('#7FA35A', '#1C3044', nightK)
    hd = mixCol('#5E8445', '#122236', nightK)
    boilSeed(key + 'h')
    P = [[-300, H + 400]] + [[x, hillY2(x)] for x in range(-300, W + 320, 60)] + [[W + 300, H + 400]]
    paint(P, wash=hc, fill=hd, fillOp=90, ink=INK, sw=1.1, curv=.2)
    # grass tufts + little white flowers on the slope
    for i in range(70):
        x = -250 + hash1(i * 1.7) * (W + 500)
        y = hillY2(x) + 20 + hash1(i * 4.4) ** 1.4 * 420
        sw_ = math.sin(t * 1.5 + i) * 6
        boilSeed(f'{key}g{i}')
        for j in range(3):
            inkLine([[x + j * 8, y], [x + j * 8 + sw_ + (j - 1) * 6, y - 24 - 12 * hash1(i + j)]], .8, mixCol(hc, '#CFE6B0', .35), 'inkfine', .3)
    if flowers:
        for i in range(40):
            x = -200 + hash1(i * 2.3 + 9) * (W + 400)
            y = hillY2(x) + 30 + hash1(i * 6.1) ** 1.3 * 380
            boilSeed(f'{key}gf{i}')
            paint(ellPts(x, y, 7, 6, 8), wash=mixCol('#FFFDF4', '#C9D0EA', nightK * .4), ink=None, lite=True)
            G.c.drawCircle(x, y, 2, skia.Paint(AntiAlias=True, Color=skcol('#F3D98A')))
    if tree:
        bigTreeSide(470, hillY2(470) + 26, 120, t, key=key + 'tree', night=nightK * .85, flowers=True)
        fireflies(t, 19, 16, 150, 120, 900, 680, nightK)
    fireflies(t, 5, 18, 0, 650, W, H, nightK)


# ================================================================ the shop street, second pass (S03, S25–S28, S38–S41)
SHOPS = [('花店', '#F59BB0', 'flowers'), ('书店', '#9FE0FF', 'books'), ('咖啡', '#FFCF85', 'cups'), ('便利店', '#BFEAA8', 'shelves'),
         ('面包', '#FFE59A', 'bread'), ('唱片', '#C9A0FF', 'records'), ('花店', '#F59BB0', 'flowers'), ('书店', '#9FE0FF', 'books')]


def shopFront2(x, y, w, h, name, lit, kind, t, key='sf', rain=True):
    """one lit shopfront; (x, y) = top-left of the facade, h down to the pavement"""
    boilSeed(key)
    paint(rectPts(x, y, w, h), wash='#2F2A4E', fill='#221E3A', fillOp=60, ink=INK, sw=.9, lite=True)
    # sign board
    paint(rectPts(x + 12, y + 10, w - 24, 46), wash=mixCol(lit, INK, .45), ink=INK, sw=.7, lite=True)
    glow(x + w / 2, y + 33, w * .6, lit, .25)
    text(name, x + w / 2, y + 34, 30, mixCol(lit, '#FFFFFF', .5), face=WENKAI, shadow=False)
    # awning
    aw_y = y + 62
    for i in range(6):
        ax = x + 8 + i * (w - 16) / 6
        paint([[ax, aw_y], [ax + (w - 16) / 6, aw_y], [ax + (w - 16) / 6, aw_y + 34], [ax + (w - 16) / 12, aw_y + 44], [ax, aw_y + 34]],
              wash=lit if i % 2 == 0 else '#FFF6E8', washOp=200, ink=INK, sw=.5, lite=True)
    # window display
    wx, wy, ww, wh = x + 20, y + 120, w * .62, h - 170
    paint(rectPts(wx, wy, ww, wh), wash=lit, washOp=210, ink=INK, sw=.7, lite=True)
    glow(wx + ww / 2, wy + wh / 2, ww * .9, lit, .35)
    if kind == 'flowers':
        for i in range(5):
            bx = wx + 20 + i * (ww - 40) / 4
            paint([[bx - 14, wy + wh - 6], [bx + 14, wy + wh - 6], [bx + 10, wy + wh - 40], [bx - 10, wy + wh - 40]], wash='#C9774E', ink=INK, sw=.4, lite=True)
            for j in range(3):
                G.c.drawCircle(bx - 10 + j * 10, wy + wh - 52 - (j % 2) * 10, 8, skia.Paint(AntiAlias=True, Color=skcol(['#E8474E', '#FFFDF4', '#F7D36E'][(i + j) % 3])))
    elif kind == 'books':
        for r in range(2):
            for i in range(7):
                bh = 34 + 14 * hash1(i * 3 + r)
                paint(rectPts(wx + 10 + i * (ww - 20) / 7, wy + 20 + r * wh / 2 + (wh / 2 - 20 - bh), (ww - 20) / 7 - 4, bh),
                      wash=['#C8564F', '#5B7FC4', '#E8B04A', '#7FB1B5', '#9C8FE0'][(i + r) % 5], ink=INK, sw=.4, lite=True)
    elif kind == 'cups':
        for i in range(4):
            cx_ = wx + 30 + i * (ww - 60) / 3
            paint(rrPts(cx_ - 14, wy + wh - 50, 28, 34, 6), wash='#FFFDF6', ink=INK, sw=.4, lite=True)
            inkLine([[cx_ - 4, wy + wh - 60], [cx_ - 8 + math.sin(t * 2 + i) * 4, wy + wh - 84]], .6, '#FFFFFF', 'inkfine', .6)
    elif kind == 'shelves':
        for r in range(3):
            G.c.drawLine(wx + 6, wy + 20 + r * wh / 3, wx + ww - 6, wy + 20 + r * wh / 3, skia.Paint(AntiAlias=True, Color=skcol(INK, .4), StrokeWidth=2))
            for i in range(6):
                G.c.drawRect(skia.Rect.MakeXYWH(wx + 12 + i * (ww - 24) / 6, wy + 20 + r * wh / 3 - 22, 14, 20),
                             skia.Paint(AntiAlias=True, Color=skcol(['#E8574E', '#5B7FC4', '#F7D36E', '#7FB1B5'][(i + r) % 4], .9)))
    elif kind == 'bread':
        for i in range(4):
            paint(ellPts(wx + 30 + i * (ww - 60) / 3, wy + wh - 30, 26, 14, 12), wash='#D9A25A', ink=INK, sw=.4, lite=True)
    elif kind == 'records':
        for i in range(3):
            paint(ellPts(wx + 40 + i * (ww - 80) / 2, wy + wh / 2, 30, 30, 18), wash='#2A2438', ink=INK, sw=.4, lite=True)
            G.c.drawCircle(wx + 40 + i * (ww - 80) / 2, wy + wh / 2, 9, skia.Paint(AntiAlias=True, Color=skcol(lit)))
    # door
    dx = x + w * .7
    paint(rectPts(dx, y + 120, w * .24, h - 120), wash=mixCol(lit, '#2F2A4E', .5), ink=INK, sw=.7, lite=True)
    G.c.drawCircle(dx + w * .05, y + 120 + (h - 120) * .55, 4, skia.Paint(AntiAlias=True, Color=skcol('#D9B45A')))
    # potted plant by the door
    boilSeed(key + 'pl')
    paint([[dx - 30, y + h], [dx - 6, y + h], [dx - 10, y + h - 30], [dx - 26, y + h - 30]], wash='#C9774E', ink=INK, sw=.4, lite=True)
    paint(ellPts(dx - 18, y + h - 52, 22, 26, 12), wash='#4E7A5A', ink=INK, sw=.4, lite=True)


def streetTall2(t, key='st', rainK=1.0):
    """tall street world: sky + two skyline layers above, shops at y 300..640, road below"""
    gradRect(-400, -1500, W + 800, 2000, ['#0E1238', '#1E2457', '#3A3F7E'])
    stars(t, 13, 60, -300, -1400, W + 300, -500, .8, 2.6)
    glow(1500, -1100, 220, '#E8E4FF', .5)
    boilSeed(key + 'moon')
    paint(ellPts(1500, -1100, 40, 40, 24), wash='#FFF8E4', ink=None)
    push()
    translate(0, -560)
    scale(1, 1.25)
    city(t, 1.0, key=key + 'c1', col='#262A60', win='#FFD98A')
    pop()
    push()
    translate(-120, -150)
    scale(1.15, 1.0)
    city(t, .8, key=key + 'c2', col='#30346E', win='#FFE2A0')
    pop()
    # upper floors above the shops: windows, balconies
    flatRect(-300, 200, W + 600, 130, '#2A2850')
    for i in range(16):
        wx = -120 + i * 140
        on = hash1(i * 4.4) < .45
        paint(rectPts(wx, 220, 70, 80), wash='#FFD98A' if on else '#1C1A3A', washOp=220, ink=INK, sw=.5, lite=True)
        G.c.drawLine(wx - 10, 302, wx + 80, 302, skia.Paint(AntiAlias=True, Color=skcol('#4A4878'), StrokeWidth=5))
    for i, (name, lit, kind) in enumerate(SHOPS):
        shopFront2(-160 + i * 290, 330, 278, 310, name, lit, kind, t, key=f'{key}sh{i}')
    # pavement + kerb
    flatRect(-300, 640, W + 600, 30, '#4A4668')
    flatRect(-300, 668, W + 600, 8, '#8A86A8')
    # road
    gradRect(-300, 676, W + 600, 700, ['#3A3658', '#24223A'])
    # wet reflections of the shop lights
    for i, (name, lit, kind) in enumerate(SHOPS):
        x = -160 + i * 290 + 100
        sh = skia.GradientShader.MakeLinear([skia.Point(0, 680), skia.Point(0, 1060)], [skcol(lit, .28), skcol(lit, 0)])
        G.c.drawRect(skia.Rect.MakeXYWH(x, 680, 90, 380), skia.Paint(Shader=sh))
    # street lamps
    for i in range(4):
        streetLamp(-40 + i * 640, 668, 44, 1.0, key=f'{key}lm{i}')
