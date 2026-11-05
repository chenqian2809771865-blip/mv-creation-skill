# tk.py: 《东京不太热》 sets & props — a summer night in a Tokyo-ish town (lanterns, vending machines, utility poles,
# a red lattice tower far away), his little room (no window), a fictional chat app, and the gag props.
import math
from eng import *
import eng
from clawd import *
from props import puff, sparkle, sparkles, bubble, heartCloud, qCloud, floatHearts, impactLines
from common import *

NS = ['#141A45', '#2A2E69', '#56448A', '#B97492']      # night sky, top → horizon
LANT = '#E4533F'
GREYS = [('#B8B6C4', '#8E8BA0', '#DCDAE6'), ('#A7A5B6', '#7E7B92', '#CFCDDC'), ('#C4C2CE', '#9895AA', '#E4E2EC')]
COUPLE = [(dict(col='#8FD3B6', dk='#5FA88A', lt='#CFF1E2'), dict(col='#F5D36E', dk='#C9A13A', lt='#FCEDBE')),
          (dict(col='#F2C26B', dk='#C8933A', lt='#FCE6B8'), dict(col='#8FC1EB', dk='#5C8FC0', lt='#D3E7F8'))]
BLUE = dict(col='#7FA7D9', dk='#4E77AE', lt='#C6DCF5')
HOT = '#FF6F96'
WENKAI = 'LXGWWenKai-Regular.ttf'
APP = '#5BC0EB'          # the fictional chat app's own blue (no real logo)


def pa_(col, a=1.0, w=None):
    p = skia.Paint(AntiAlias=True, Color=skcol(col, a))
    if w:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(w)
        p.setStrokeCap(skia.Paint.kRound_Cap)
    return p


def ln(x0, y0, x1, y1, col=INK, a=1.0, w=2.0):
    G.c.drawLine(x0, y0, x1, y1, pa_(col, a, w))


def em(t, keys, base=None, **kw):
    o = emotions(t, keys, base)
    o.update(kw)
    return o


def ek(k):
    """emotion key time: a little before the beat so the new face is fully there on the beat frame"""
    return B[k] - .06


def hitK(t, k, d=.12):
    a = t - (B[k] - .04)
    return 0.0 if a < 0 else math.exp(-a / d)


def landK(t, k, d=.16):
    return clamp((t - (B[k] - d)) / d)


def arrive(t, ks, vals, d=.16, e=None):
    """value that moves to vals[i+1] during the d seconds BEFORE beat ks[i] (it lands on the beat frame)"""
    e = e or easeOut
    v = vals[0]
    for i, k in enumerate(ks):
        tb = B[k] - d
        if t >= tb:
            v = lerp(vals[i], vals[i + 1], e(clamp((t - tb) / d)))
    return v


def popK(t, k, d=.16):
    """0..1 backOut pop that is ~full on the beat frame"""
    return backOut(clamp((t - (B[k] - .06)) / d))


def stampAt(txt, x, y, size, t, k, col='#E0344E', rot=-.14):
    rubberStamp(txt, x, y, size, t - B[k], col, rot)


# ===================================================================== sky / far city
def nightSky(t, key='ns', y1=900, stars=True, moon=(1640, 170)):
    gradRect(-400, -400, W + 800, y1 + 400, NS)
    if stars:
        for i in range(40):
            x = -200 + hash1(i * 7.1) * (W + 400)
            y = -100 + hash1(i * 3.3) * (y1 * .55)
            tw = .55 + .45 * math.sin(t * 3 + i * 1.7)
            G.c.drawCircle(x, y, 1.6 + 1.6 * hash1(i * 1.9), pa_('#FFF6D8', .7 * tw))
    if moon:
        mx, my = moon
        glow(mx, my, 160, '#FFF1C2', .5)
        boilSeed(key + 'moon')
        paint(ellPts(mx, my, 46, 46, 26), wash='#FFF4CF', fill='#F3DFA3', fillOp=60, ink=INK, sw=.8)
        G.c.drawCircle(mx + 14, my - 10, 9, pa_('#EAD49A', .7))
        G.c.drawCircle(mx - 12, my + 12, 6, pa_('#EAD49A', .6))


def tower(x, y, s, key='tw', lit=1.0):
    """red lattice tower far away (a generic Tokyo skyline icon). (x, y) = foot centre; s = scale (height ≈ 30 s)"""
    boilSeed(key)
    red, wh = '#E0573F', '#F6EFE6'
    hgt = 30 * s

    def wAt(f):           # half width at height fraction f (0 foot .. 1 top)
        return s * (6.2 * (1 - f) ** 2.2 + .35)
    L = [[x - wAt(f), y - f * hgt] for f in [i / 12 * .86 for i in range(13)]]
    R_ = [[x + wAt(f), y - f * hgt] for f in [i / 12 * .86 for i in range(13)]]
    body = L + R_[::-1]
    paint(body, wash=red, ink=INK, sw=.7)
    # white bands
    for f0, f1 in ((.18, .23), (.5, .54), (.7, .73)):
        paint([[x - wAt(f0), y - f0 * hgt], [x + wAt(f0), y - f0 * hgt], [x + wAt(f1), y - f1 * hgt], [x - wAt(f1), y - f1 * hgt]],
              wash=wh, ink=None)
    # lattice
    for i in range(10):
        f0, f1 = i / 10 * .84, (i + 1) / 10 * .84
        inkLine([[x - wAt(f0), y - f0 * hgt], [x + wAt(f1), y - f1 * hgt]], .45, '#8E2F22', 'inkfine', 0)
        inkLine([[x + wAt(f0), y - f0 * hgt], [x - wAt(f1), y - f1 * hgt]], .45, '#8E2F22', 'inkfine', 0)
    # arch between the legs
    paint(ellPts(x, y, wAt(0) * .55, 2.6 * s, 18), wash=NS[3], ink=None)
    # decks
    for f, w_ in ((.36, 2.1), (.62, 1.2)):
        yy = y - f * hgt
        paint(rectPts(x - w_ * s, yy - .9 * s, 2 * w_ * s, 1.4 * s), wash='#F3E7D8', fill='#FFD27A', fillOp=int(140 * lit), ink=INK, sw=.6)
    inkLine([[x, y - .86 * hgt], [x, y - hgt]], 1.0, wh, 'ink', 0)
    if lit > .02:
        glow(x, y - .5 * hgt, 9 * s, '#FFB27A', .45 * lit)
        G.c.drawCircle(x, y - hgt, 2.2 * s * .4 + 2, pa_('#FF5A5A', .6 + .4 * math.sin(G.T * 6)))


def skyline(y, key='sk', col='#2B2B5E', win='#FFD98A', seed=0, x0=-300, x1=W + 300, hmin=120, hmax=330, winA=.75):
    boilSeed(key)
    x = x0
    i = 0
    while x < x1:
        w = 90 + 120 * hash1(seed + i * 1.37)
        h = hmin + (hmax - hmin) * hash1(seed + i * 2.71)
        flatRect(x, y - h, w + 2, h + 4, col)
        for r in range(int(h // 34)):
            for c_ in range(int(w // 30)):
                if win and winA > 0 and hash1(seed + i * 13 + r * 7 + c_ * 3) > .55:
                    flatRect(x + 10 + c_ * 30, y - h + 14 + r * 34, 12, 14, win, winA * (.5 + .5 * hash1(i + r + c_)))
        x += w + 6
        i += 1


# ===================================================================== street pieces
def pole(x, y, h, key='pole', col='#8E8A9C', night=1.0):
    """concrete utility pole with a cross arm + transformer; returns the wire anchor points"""
    boilSeed(key)
    paint(rectPts(x - 11, y - h, 22, h), wash=col, fill=mixCol(col, INK, .25), fillOp=70, ink=INK, sw=.9)
    for yy in (y - h + 40, y - h + 110):
        paint(rectPts(x - 80, yy, 160, 12), wash=mixCol(col, INK, .2), ink=INK, sw=.7)
        for s in (-1, 1):
            paint(ellPts(x + s * 62, yy - 6, 7, 9, 10), wash='#EDE8DC', ink=INK, sw=.5)
    paint(rrPts(x + 14, y - h + 150, 46, 70, 8), wash='#A9A6B6', fill='#77738A', fillOp=70, ink=INK, sw=.7)
    # small address plate
    paint(rectPts(x - 14, y - 330, 28, 70), wash='#2F5C9E', ink=INK, sw=.5)
    text('一', x, y - 305, 18, '#FFFFFF', face=WENKAI, shadow=False)
    text('丁', x, y - 282, 18, '#FFFFFF', face=WENKAI, shadow=False)
    return [(x - 62, y - h + 34), (x + 62, y - h + 34), (x - 62, y - h + 104), (x + 62, y - h + 104)]


def wire(p0, p1, sag=40, col='#1E1B30', w=1.6, a=.85):
    pts = []
    for i in range(17):
        f = i / 16
        pts.append([lerp(p0[0], p1[0], f), lerp(p0[1], p1[1], f) + sag * 4 * f * (1 - f)])
    p = skia.Path()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    G.c.drawPath(p, pa_(col, a, w))


def lantern(x, y, r, lit=1.0, key='lt', txt=None, col=LANT, sway=0.0):
    """red paper lantern (chōchin). (x, y) = hanging point"""
    push()
    translate(x, y)
    rotate(sway)
    boilSeed(key)
    cy = r * 1.25
    if lit > .02:
        glow(0, cy, r * 3.2, '#FFB070', .55 * lit)
    paint(rectPts(-r * .42, cy - r * 1.12, r * .84, r * .2), wash='#2A2233', ink=INK, sw=.6)
    paint(rectPts(-r * .42, cy + r * .92, r * .84, r * .2), wash='#2A2233', ink=INK, sw=.6)
    body = ellPts(0, cy, r * .82, r * .98, 26)
    paint(body, wash=mixCol(col, '#FFD9A0', .25 * lit), fill=mixCol(col, INK, .15), fillOp=70, ink=INK, sw=.8)
    for i in range(1, 6):
        yy = cy - r * .98 + i * r * 1.96 / 6
        ww = r * .82 * math.sqrt(max(0, 1 - ((yy - cy) / (r * .98)) ** 2))
        ln(-ww, yy, ww, yy, mixCol(col, INK, .4), .5, 1.2)
    if txt:
        text(txt, 0, cy + 2, r * .82, '#FFF3E0' if lit > .5 else '#2A2233', face=WENKAI, shadow=False)
    ln(0, 0, 0, cy - r * 1.12, '#1E1B30', .9, 1.5)
    pop()


def lanternRow(t, x0, x1, y, n, key='lr', lit=1.0, sag=50, txts=None, r=34, cols=None):
    wire((x0, y), (x1, y), sag)
    for i in range(n):
        f = (i + .5) / n
        x = lerp(x0, x1, f)
        yy = y + sag * 4 * f * (1 - f)
        lantern(x, yy, r, lit, key=f'{key}{i}', txt=(txts[i % len(txts)] if txts else None),
                col=(cols[i % len(cols)] if cols else LANT), sway=.05 * math.sin(t * 2.1 + i))


def vending(x, y, s=1.0, lit=1.0, key='vm', drop=None, col='#E9E6EE', band='#D8394E'):
    """drink vending machine; (x, y) = bottom centre; ~260 x 520 at s=1. drop = seconds since a can dropped (or None)"""
    boilSeed(key)
    w, h = 260 * s, 520 * s
    x0, y0 = x - w / 2, y - h
    if lit > .02:
        glow(x, y - h * .55, 420 * s, '#E8F4FF', .5 * lit)
    paint(rrPts(x0, y0, w, h, 14 * s), wash=col, fill=mixCol(col, INK, .12), fillOp=60, ink=INK, sw=1.1)
    paint(rectPts(x0 + 10 * s, y0 + 10 * s, w - 20 * s, 44 * s), wash=band, ink=INK, sw=.7)
    text('つめた～い', x, y0 + 32 * s, 26 * s, '#FFFFFF', face=WENKAI, shadow=False)
    # display window: 3 rows x 5 cans
    dx0, dy0, dw, dh = x0 + 18 * s, y0 + 66 * s, w - 36 * s, 250 * s
    paint(rectPts(dx0, dy0, dw, dh), wash=mixCol('#F6FBFF', '#FFFFFF', lit), ink=INK, sw=.8)
    cans = ['#E8476E', '#5BC0EB', '#F2C53D', '#7FCB7A', '#F08A4B', '#B9A3E3']
    for r in range(3):
        for c_ in range(5):
            cx = dx0 + 22 * s + c_ * (dw - 44 * s) / 4
            cy = dy0 + 18 * s + r * 80 * s
            cc = cans[(r * 5 + c_ * 2 + r) % len(cans)]
            paint(rrPts(cx - 13 * s, cy, 26 * s, 48 * s, 6 * s), wash=cc, ink=INK, sw=.4)
            flatRect(cx - 13 * s, cy + 16 * s, 26 * s, 9 * s, '#FFFFFF', .7)
            G.c.drawCircle(cx, cy + 60 * s, 4 * s, pa_('#3FD17A' if (r + c_) % 3 else '#FF5A5A', .9))
        ln(dx0, dy0 + 76 * s + r * 80 * s, dx0 + dw, dy0 + 76 * s + r * 80 * s, '#C9C4D6', 1, 1.2)
    # coin slot + buttons
    paint(rrPts(x + 60 * s, y0 + 340 * s, 44 * s, 70 * s, 6 * s), wash='#C9C4D6', ink=INK, sw=.5)
    ln(x + 82 * s, y0 + 352 * s, x + 82 * s, y0 + 372 * s, INK, 1, 3 * s)
    # dispenser
    paint(rrPts(x0 + 30 * s, y - 120 * s, w - 60 * s, 70 * s, 8 * s), wash='#2F2B3E', ink=INK, sw=.8)
    if drop is not None and drop >= 0:
        k = clamp(drop / .1)
        cy = lerp(y - 150 * s, y - 92 * s, easeIn(k))
        paint(rrPts(x - 34 * s, cy - 20 * s, 68 * s, 40 * s, 8 * s), wash='#5BC0EB', ink=INK, sw=.6)
    flatRect(x0 + 30 * s, y - 40 * s, w - 60 * s, 18 * s, '#BDB8CC')
    return dict(x0=x0, x1=x0 + w, top=y0)


def noren(x, y, w, h, col, txt, key='nr', t=0.0, sway=0.0):
    """split shop curtain hanging from y"""
    n = 3
    for i in range(n):
        boilSeed(f'{key}{i}')
        xx = x - w / 2 + i * w / n
        dx = sway * 10 * math.sin(t * 2 + i)
        paint([[xx + 3, y], [xx + w / n - 3, y], [xx + w / n - 3 + dx, y + h], [xx + 3 + dx, y + h]], wash=col,
              fill=mixCol(col, INK, .2), fillOp=60, ink=INK, sw=.7)
    flatRect(x - w / 2 - 10, y - 8, w + 20, 10, '#6B4A3E')
    if txt:
        for i, ch in enumerate(txt[:3]):
            text(ch, x - w / 2 + (i + .5) * w / n, y + h * .45, min(w / n * .6, h * .5), '#FFF6E8', face=WENKAI, shadow=False)


def shutter(x0, x1, top, bot, col='#9AA0B8', key='sh', night=1.0):
    boilSeed(key)
    paint(rectPts(x0, top, x1 - x0, bot - top), wash=col, fill=mixCol(col, INK, .18), fillOp=50, ink=INK, sw=1.0)
    y = top + 16
    while y < bot - 6:
        ln(x0 + 6, y, x1 - 6, y, mixCol(col, INK, .35), .55, 2.2)
        ln(x0 + 6, y + 4, x1 - 6, y + 4, '#FFFFFF', .18, 2)
        y += 26
    paint(rectPts(x0 - 14, top - 30, x1 - x0 + 28, 34), wash=mixCol(col, INK, .25), ink=INK, sw=.8)
    paint(rectPts(x0 + (x1 - x0) / 2 - 30, bot - 34, 60, 14), wash=mixCol(col, INK, .3), ink=INK, sw=.5)


SHOPS = [  # name, wall, sign, noren, kind
    ('拉面', '#E8D2B0', '#C8402F', '#2F3E6A', 'shop'),
    ('杂货', '#CFDDE8', '#3E7FB0', '#7A4E9A', 'shop'),
    ('居酒屋', '#E4C9A8', '#2B2233', '#B8324F', 'shop'),
    ('汤屋', '#D9E4CF', '#4E8A5A', '#2E6A8E', 'shop'),
    ('', '#D8CFE2', '#6E6A80', '', 'shutter'),
    ('甜品', '#F3D3DA', '#D25C7E', '#E87B9C', 'shop'),
]


def shopFront(x0, x1, ground, h, spec, t, key='sf', lit=1.0, lanterns=True):
    name, wall, sign, nr, kind = spec
    boilSeed(key)
    wall_ = mixCol(wall, '#3A3870', .32)
    paint(rectPts(x0, ground - h, x1 - x0, h), wash=wall_, fill=mixCol(wall_, INK, .15), fillOp=50, ink=INK, sw=1.0)
    # roof eave
    paint([[x0 - 26, ground - h], [x1 + 26, ground - h], [x1 + 8, ground - h - 34], [x0 - 8, ground - h - 34]],
          wash='#4A4560', fill='#2E2A40', fillOp=70, ink=INK, sw=.9)
    if kind == 'shutter':
        shutter(x0 + 30, x1 - 30, ground - h + 110, ground - 4, key=key + 'sh')
        return
    # sign board
    sw_ = min(x1 - x0 - 80, 60 + 62 * len(name))
    paint(rrPts((x0 + x1) / 2 - sw_ / 2, ground - h + 26, sw_, 76, 10), wash=sign, ink=INK, sw=.9)
    text(name, (x0 + x1) / 2, ground - h + 64, 50, '#FFF6E8', face=WENKAI, shadow=False)
    if lit > .02:
        glow((x0 + x1) / 2, ground - h + 64, 160, '#FFE0A0', .35 * lit)
    # lit doorway (warm interior) + noren
    dx0, dx1 = x0 + 40, x1 - 40
    paint(rectPts(dx0, ground - h + 130, dx1 - dx0, h - 130), wash=mixCol('#6A4A3A', '#FFD08A', .55 * lit), ink=INK, sw=.9)
    for j in range(3):
        flatRect(dx0 + 20 + j * (dx1 - dx0 - 40) / 3, ground - 120, (dx1 - dx0 - 60) / 3, 8, '#8E5E3A', .7)
    noren((x0 + x1) / 2, ground - h + 134, dx1 - dx0 - 20, 120, nr, name, key=key + 'nr', t=t, sway=.6)
    if lanterns:
        for s in (-1, 1):
            lantern((x0 + x1) / 2 + s * ((x1 - x0) / 2 - 30), ground - h + 108, 26, lit, key=f'{key}l{s}',
                    txt='祭' if s < 0 else None, sway=.04 * math.sin(t * 2 + s))


def sidewalk(y, key='sw', night=1.0):
    flatRect(-400, y, W + 800, H - y + 400, '#5A5878')
    flatRect(-400, y, W + 800, 16, '#77748F')
    for i in range(-6, 30):
        ln(i * 110, y + 16, i * 110 - 60, H + 60, '#4A4866', .5, 2)
    inkLine([[-400, y], [W + 400, y]], 1.2, INK, 'ink', 0)


def lanternStreet(t, key='ls', ground=860, x0=-260, widths=(430, 420, 470, 400, 430, 420), order=(0, 1, 2, 4, 3, 5),
                  far=True, lit=1.0, poles=(250, 1520), vend=None, row=True):
    """side view of a little lantern street at night"""
    nightSky(t, key + 'sky', ground)
    if far:
        skyline(ground - 330, key + 'sk1', '#33336A', seed=3, hmin=60, hmax=220, winA=.5)
        tower(1390, ground - 320, 13.5, key + 'tw')
        skyline(ground - 300, key + 'sk2', '#26285A', seed=11, hmin=40, hmax=150, winA=.6)
    x = x0
    tops = []
    for i, w in enumerate(widths):
        spec = SHOPS[order[i % len(order)]]
        h = [400, 440, 420, 460, 410, 430][i % 6]
        shopFront(x, x + w, ground, h, spec, t, key=f'{key}s{i}', lit=lit)
        tops.append(ground - h)
        x += w + 10
    sidewalk(ground, key + 'swk')
    anchors = []
    for i, px in enumerate(poles):
        anchors.append(pole(px, ground + 6, 720, key=f'{key}p{i}'))
    if len(anchors) >= 2:
        for j in range(4):
            wire(anchors[0][j], anchors[1][j], 60 + 10 * j)
        for j in range(2):
            wire((-300, anchors[0][j][1] + 30), anchors[0][j], 30)
            wire(anchors[1][j], (W + 300, anchors[1][j][1] + 40), 30)
    if row:
        lanternRow(t, -100, W + 100, ground - 470, 9, key + 'row', lit, sag=70, txts=['夏', None, '祭', None])
    if vend is not None:
        vending(vend, ground + 4, .9, lit, key=key + 'vm')


# ===================================================================== crossing (S01 / S18)
def walkSignal(x, y, s, green=1.0, key='sig'):
    boilSeed(key)
    paint(rectPts(x - 6 * s, y, 12 * s, 340 * s), wash='#6E6A80', ink=INK, sw=.7)
    paint(rrPts(x - 40 * s, y - 150 * s, 80 * s, 150 * s, 10 * s), wash='#3A3650', ink=INK, sw=.8)
    for j, (cy, on, col) in enumerate(((y - 112 * s, 1 - green, '#FF5A4E'), (y - 40 * s, green, '#3FE07A'))):
        paint(rrPts(x - 30 * s, cy - 32 * s, 60 * s, 64 * s, 8 * s), wash=mixCol('#2A2638', col, .25 + .75 * on), ink=None)
        if on > .3:
            glow(x, cy, 90 * s, col, .5 * on)
        icon = '#FFFFFF' if on > .3 else mixCol(col, '#2A2638', .5)
        # pictogram (standing / walking person)
        G.c.drawCircle(x, cy - 18 * s, 6 * s, pa_(icon))
        if j == 1:
            for a, b in (((0, -10), (2, 8)), ((2, 8), (-8, 24)), ((2, 8), (10, 24)), ((0, -6), (-10, 6)), ((0, -6), (10, 2))):
                ln(x + a[0] * s, cy + a[1] * s, x + b[0] * s, cy + b[1] * s, icon, 1, 4.4 * s)
        else:
            for a, b in (((0, -10), (0, 10)), ((0, 10), (-5, 26)), ((0, 10), (5, 26)), ((0, -6), (-8, 8)), ((0, -6), (8, 8))):
                ln(x + a[0] * s, cy + a[1] * s, x + b[0] * s, cy + b[1] * s, icon, 1, 4.4 * s)


def crossing(t, key='cx', horizon=560, green=1.0, lit=1.0, skip=(), moon=(300, 140)):
    """high-ish view of a scramble crossing at night: buildings with signboards at the back, zebra stripes in front"""
    nightSky(t, key + 'sky', horizon + 40, moon=moon)
    skyline(horizon - 160, key + 'f1', '#34346C', seed=5, hmin=80, hmax=260, winA=.5)
    tower(1500, horizon - 150, 12, key + 'tw')
    skyline(horizon, key + 'f2', '#2A2A5E', seed=17, hmin=160, hmax=380, winA=.75)
    # big signboards on the front buildings
    for i, (x, y, w, h, txt, col) in enumerate([(160, horizon - 330, 90, 260, '拉面', '#E8476E'), (560, horizon - 280, 300, 80, '卡拉OK', '#F2C53D'),
                                                (1180, horizon - 340, 90, 300, '唱片', '#5BC0EB'), (1700, horizon - 300, 260, 76, '书店', '#7FCB7A')]):
        if txt in skip:
            continue
        boilSeed(f'{key}sg{i}')
        on = lit * (.85 + .15 * math.sin(t * 7 + i * 2))
        glow(x + w / 2, y + h / 2, max(w, h) * .9, col, .45 * on)
        paint(rrPts(x, y, w, h, 10), wash=mixCol('#2B2233', col, .75 * on + .1), ink=INK, sw=.9)
        if w < h:
            for j, ch in enumerate(txt):
                text(ch, x + w / 2, y + 50 + j * (h - 60) / max(1, len(txt) - 1) * .85, w * .62, '#FFFFFF', face=WENKAI, shadow=False)
        else:
            text(txt, x + w / 2, y + h / 2 + 2, h * .62, '#FFFFFF', face=WENKAI, shadow=False)
    # ground: asphalt + zebra
    flat([[-400, horizon], [W + 400, horizon], [W + 400, H + 400], [-400, H + 400]], '#3E3C5E')
    boilSeed(key + 'zb')
    n = 12
    for i in range(n):
        xf = lerp(-150, W + 150, (i + .25) / n)
        xn = lerp(-700, W + 700, (i + .25) / n)
        wf, wn = (W + 300) / n * .5, (W + 1400) / n * .5
        paint([[xf, horizon + 60], [xf + wf, horizon + 60], [xn + wn, H + 60], [xn, H + 60]], wash='#E9E4F2', washOp=230, ink=None)
    flatRect(-400, horizon, W + 800, 40, '#55537A')
    inkLine([[-400, horizon], [W + 400, horizon]], 1.2, INK, 'ink', 0)
    walkSignal(120, horizon - 40, 1.0, green, key + 'sigL')
    walkSignal(1820, horizon - 40, 1.0, green, key + 'sigR')


# ===================================================================== people
def grey(x, y, u, i, o=None, key='gr', walk=None, a=1.0):
    g_ = GREYS[i % 3]
    d = dict(col=g_[0], dk=g_[1], lt=g_[2], view='q', eyes='normal', mouth=None, boilKey=f'{key}{i}', aL=.1, aR=.1, lite=True)
    if walk is not None:
        d.update(walk=walk, dy=-abs(math.sin(walk * TAU)) * .4)
    if o:
        d.update(o)
    if a < 1:
        G.c.saveLayerAlpha(None, int(255 * clamp(a)))
        clawd(x, y, u, d)
        G.c.restore()
    else:
        clawd(x, y, u, d)


def blueGuy(x, y, u, o=None):
    d = dict(BLUE)
    d.update(hat='beanie', boilKey='blue')
    if o:
        d.update(o)
    clawd(x, y, u, d)


def silhouette(fn, col='#231E3E', a=.42):
    """draw anything as a flat shadow silhouette (alpha kept, colour replaced)"""
    p = skia.Paint()
    p.setColorFilter(skia.ColorFilters.Blend(skcol(col), skia.BlendMode.kSrcIn))
    p.setAlphaf(a)
    G.c.saveLayer(None, p)
    fn()
    G.c.restore()


def handDot(x, y, u, col, dk=None):
    paint(ellPts(x, y, .62 * u, .62 * u, 12), wash=col, fill=dk or mixCol(col, INK, .25), fillOp=40, ink=INK, sw=max(.5, u / 30))


def faceXY(o, side, u):
    """body-local position of an eye (side -1/1) for draw hooks"""
    V = VIEWS[o.get('view') or 'front']
    F = V['face']
    if not F:
        return None
    return ((F['cx'] + side * 2.5 * F['fw']) * u, -6.2 * u)


def mouthXY(o, u):
    V = VIEWS[o.get('view') or 'front']
    F = V['face']
    return ((F['cx'] + F['mx'] * F['fw']) * u, -4.3 * u)


def glassesHook(o, col='#2B2233'):
    def h(u, sw):
        for s in (-1, 1):
            p = faceXY(o, s, u)
            if p is None:
                return
            r = 1.25 * u * VIEWS[o.get('view') or 'front']['face']['fw'] ** .3
            G.c.drawCircle(p[0], p[1], r, pa_(col, 1, max(1.5, .32 * u)))
            G.c.drawCircle(p[0] - .35 * u, p[1] - .35 * u, .25 * u, pa_('#FFFFFF', .7))
        a, b = faceXY(o, -1, u), faceXY(o, 1, u)
        ln(a[0] + 1.2 * u, a[1], b[0] - 1.2 * u, b[1], col, 1, max(1.4, .28 * u))
    return h


def zipperHook(o, k=1.0):
    def h(u, sw):
        if k <= 0:
            return
        mx, my = mouthXY(o, u)
        L = 2.2 * u * k
        ln(mx - 1.1 * u, my, mx - 1.1 * u + L, my, '#2B2233', 1, .35 * u)
        n = int(L / (.3 * u))
        for i in range(n):
            xx = mx - 1.1 * u + (i + .5) * .3 * u
            ln(xx, my - .25 * u, xx, my + .25 * u, '#8A8698', 1, max(1, .1 * u))
        tx = mx - 1.1 * u + L
        paint(rrPts(tx - .2 * u, my - .2 * u, .45 * u, .9 * u, .1 * u), wash='#C9C4D6', ink=INK, sw=.5)
    return h


def crackHook(o, k=1.0):
    """cracks across the sunglasses lenses"""
    def h(u, sw):
        if k <= 0:
            return
        for s in (-1, 1):
            p = faceXY(o, s, u)
            if p is None:
                return
            x, y = p
            L = 1.25 * u * k
            inkLine([[x - .2 * u, y - .7 * u], [x + .15 * u, y - .1 * u], [x - .25 * u, y + .25 * u], [x + .1 * u, y + .75 * u * k]], sw * .6, '#F3F0FF', 'inkfine', 0)
            inkLine([[x + .15 * u, y - .1 * u], [x + L * .7, y - .35 * u]], sw * .5, '#F3F0FF', 'inkfine', 0)
            inkLine([[x - .25 * u, y + .25 * u], [x - L * .75, y + .1 * u]], sw * .5, '#F3F0FF', 'inkfine', 0)
    return h


def chainHooks(*hs):
    hs = [h for h in hs if h]

    def h(u, sw):
        for f in hs:
            f(u, sw)
    return h


def collarHook(o, k=1.0, col='#2B2B3E'):
    """a popped-up dark jacket collar around the lower body (高冷)"""
    def h(u, sw):
        if k <= 0:
            return
        V = VIEWS[o.get('view') or 'front']
        L, R = V['L'] * u, V['R'] * u
        top = -3.8 * u - 1.6 * u * k
        for s, xe in ((-1, L), (1, R)):
            xm = (L + R) / 2 + s * 1.4 * u
            paint([[xe - s * .1 * u, -2.0 * u], [xe - s * .1 * u, top], [xm, -3.0 * u], [xm, -2.0 * u]], wash=col,
                  fill=mixCol(col, '#FFFFFF', .15), fillOp=60, ink=INK, sw=sw * .7)
    return h


# ===================================================================== his room (no window)
def hisRoom(t, key='rm', floor=860, lamp=1.0, lights=1.0, dim=0.0):
    wall = mixCol('#F1D3AE', '#3C3C70', .22 + .5 * dim)
    gradRect(-400, -400, W + 800, floor + 400, [mixCol(wall, '#FFFFFF', .08), wall])
    for r in range(16):
        for c_ in range(26):
            G.c.drawCircle(-200 + c_ * 92 + (46 if r % 2 else 0), -100 + r * 74, 4, pa_(mixCol(wall, INK, .18), .45))
    # floor
    flatRect(-400, floor, W + 800, H - floor + 400, mixCol('#B98352', '#3C3C70', .25 + .4 * dim))
    for i in range(-4, 30):
        ln(-400, floor + 26 + i * 34, W + 400, floor + 26 + i * 34, '#8E5E3A', .35, 2)
    inkLine([[-400, floor], [W + 400, floor]], 1.2, INK, 'ink', 0)
    # bookshelf (left)
    boilSeed(key + 'bs')
    paint(rectPts(70, floor - 560, 330, 560), wash='#A8714A', fill='#7E4E30', fillOp=70, ink=INK, sw=1.0)
    for r in range(4):
        yy = floor - 540 + r * 136
        paint(rectPts(90, yy + 118, 290, 14), wash='#7E4E30', ink=INK, sw=.5)
        x = 100
        j = 0
        while x < 360:
            bw = 22 + 18 * hash1(r * 9 + j)
            bh = 70 + 40 * hash1(r * 5 + j * 3)
            cc = ['#E8476E', '#5BC0EB', '#F2C53D', '#7FCB7A', '#B9A3E3', '#F08A4B', '#EDE6DA'][(r * 3 + j) % 7]
            if r == 1 and j == 3:
                paint(ellPts(x + 30, yy + 98, 28, 20, 14), wash='#7FCB7A', ink=INK, sw=.5)     # a little cactus pot
                paint(rectPts(x + 16, yy + 100, 28, 18), wash='#D9774E', ink=INK, sw=.5)
                x += 70
            else:
                paint(rectPts(x, yy + 118 - bh, bw, bh), wash=cc, ink=INK, sw=.45)
                x += bw + 3
            j += 1
    # posters + calendar
    boilSeed(key + 'po')
    paint(rectPts(520, 160, 220, 300), wash='#2B2B5E', ink=INK, sw=.9)
    tower(630, 430, 8.5, key + 'ptw', lit=.6)
    text('TOKYO', 630, 200, 40, '#FFE36E', shadow=False)
    paint(rectPts(800, 210, 170, 200), wash='#FFFDF6', ink=INK, sw=.8)
    paint(rectPts(800, 210, 170, 48), wash='#D8546A', ink=INK, sw=.6)
    text('7月', 885, 236, 30, '#FFF6E8', face=WENKAI, shadow=False)
    for r in range(5):
        for c_ in range(7):
            G.c.drawCircle(816 + c_ * 23, 280 + r * 25, 2.6, pa_('#8A7A88', .7))
    G.c.drawCircle(885, 204, 6, pa_(INK))
    # string lights
    if lights > 0:
        pts = []
        for i in range(19):
            f = i / 18
            pts.append((lerp(-60, W + 60, f), 70 + 60 * math.sin(f * math.pi * 3) ** 2))
        for a, b in zip(pts, pts[1:]):
            wire(a, b, 10, '#4A3A44', 1.4)
        for i, (x, y) in enumerate(pts[1:-1]):
            on = lights * (.75 + .25 * math.sin(t * 4 + i * 1.3))
            cc = ['#FFE36E', '#FF8FB0', '#8FD3FF'][i % 3]
            glow(x, y + 14, 46, cc, .55 * on)
            paint(ellPts(x, y + 14, 8, 11, 10), wash=mixCol('#77738A', cc, on), ink=INK, sw=.4)
    # bed (right): headboard + mattress
    boilSeed(key + 'bed')
    paint(rrPts(1180, floor - 360, 700, 240, 30), wash='#8C6E9E', fill='#6E5088', fillOp=60, ink=INK, sw=1.0)
    paint(rrPts(1150, floor - 170, 760, 120, 20), wash='#F4EFE6', ink=INK, sw=.9)
    paint(rrPts(1230, floor - 210, 200, 70, 30), wash='#FFFFFF', fill='#E6DED2', fillOp=60, ink=INK, sw=.8)
    paint(rectPts(1160, floor - 50, 740, 50), wash='#6E5088', ink=INK, sw=.8)
    # bedside table + lamp
    boilSeed(key + 'bt')
    paint(rectPts(960, floor - 190, 170, 190), wash='#C99A6A', fill='#A0704A', fillOp=60, ink=INK, sw=.9)
    paint(rectPts(975, floor - 120, 140, 50), wash='#B7865A', ink=INK, sw=.5)
    G.c.drawCircle(1045, floor - 95, 6, pa_('#6B4A3E'))
    if lamp > 0:
        glow(1010, floor - 300, 200, '#FFD27A', .55 * lamp)
    paint(rectPts(1005, floor - 260, 10, 70), wash='#6B4A3E', ink=INK, sw=.4)
    paint([[965, floor - 255], [1055, floor - 255], [1035, floor - 320], [985, floor - 320]], wash=mixCol('#E8D6B8', '#FFE7A0', lamp), ink=INK, sw=.7)
    # rug
    paint(ellPts(300, floor + 55, 230, 36, 30), wash='#E8B7C4', fill='#D08AA0', fillOp=50, ink=INK, sw=.7)


def phoneProp(x, y, w, h, rot=0.0, lit=1.0, key='ph', case='#F08A4B', screen=None, glowK=1.0):
    """a phone drawn in world space; screen(sx, sy, sw, sh) draws the screen contents (clipped)"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    if lit > .02 and glowK > 0:
        glow(0, 0, max(w, h) * 1.2, '#BFE6FF', .45 * lit * glowK)
    paint(rrPts(-w / 2, -h / 2, w, h, min(w, h) * .16), wash=case, fill=mixCol(case, INK, .2), fillOp=60, ink=INK, sw=1.0)
    m = min(w, h) * .07
    sx, sy, sw_, sh = -w / 2 + m, -h / 2 + m, w - 2 * m, h - 2 * m
    G.c.drawRoundRect(skia.Rect.MakeXYWH(sx, sy, sw_, sh), m * 1.6, m * 1.6, pa_(mixCol('#1C1A26', '#EAF6FF', lit)))
    if screen and lit > .02:
        G.c.save()
        p = skia.Path()
        p.addRoundRect(skia.Rect.MakeXYWH(sx, sy, sw_, sh), m * 1.6, m * 1.6)
        G.c.clipPath(p, skia.ClipOp.kIntersect, True)
        screen(sx, sy, sw_, sh)
        G.c.restore()
    pop()


# ===================================================================== chat (fictional app)
def miniFace(x, y, r, who='her', ring=APP, bg=None):
    """round avatar with a little Clawd head inside"""
    G.c.drawCircle(x, y, r, pa_(bg or ('#FFE4EC' if who == 'her' else '#FFE9D6')))
    G.c.save()
    p = skia.Path()
    p.addCircle(x, y, r)
    G.c.clipPath(p, skia.ClipOp.kIntersect, True)
    u = r / 4.4
    o = dict(view='front', noShadow=True, noLegs=True, eyes='happy', mouth='smile', blush=.5, boilKey='mf' + who, aL=-.5, aR=-.5)
    if who == 'her':
        o.update(HER)
        o['hat'] = 'flower'
    elif who == 'him':
        o.update(ME)
        o['hat'] = 'headphones'
    elif who == 'blue':
        o.update(BLUE)
        o['hat'] = 'beanie'
    clawd(x, y + 7.0 * u, u, o)
    if who == 'him':
        for d in (-1, 1):
            paint(rrPts(x + d * .78 * r - .16 * r, y - .2 * r, .32 * r, .62 * r, .12 * r), wash=PAL['violet'], ink=INK, sw=.6)
        G.c.drawArc(skia.Rect.MakeXYWH(x - .78 * r, y - .95 * r, 1.56 * r, 1.4 * r), 200, 140, False, pa_(INK, 1, max(2, r * .08)))
    G.c.restore()
    G.c.drawCircle(x, y, r, pa_(ring, 1, max(2, r * .09)))


def qFace(x, y, r):
    G.c.drawCircle(x, y, r, pa_('#C9C4D6'))
    text('?', x, y + 2, r * 1.3, '#FFFFFF', shadow=False)
    G.c.drawCircle(x, y, r, pa_(APP, 1, max(2, r * .09)))


def chatBub(x, y, txt, who='her', k=1.0, size=46, draft=False, strike=0.0, a=1.0, face=True, icon=None, maxw=900):
    """a floating chat bubble. who='her' → left aligned (avatar left of x), who='him' → right aligned (avatar right of x).
    (x, y) = avatar centre. k = pop 0..1. strike 0..1 = red line through the (draft) text, then it fades."""
    if k <= .01 or a <= .01:
        return
    tw = textW(txt, size)
    iw = size * 1.15 if icon else 0
    bw, bh = min(maxw, tw + iw + size * 1.1), size * 1.75
    r = size * .78
    left = who == 'her'
    push()
    G.c.saveLayerAlpha(None, int(255 * clamp(a)))
    translate(x, y)
    sc = backOut(clamp(k))
    scale(sc)
    if face:
        if who == 'q':
            qFace(0, 0, r)
        else:
            miniFace(0, 0, r, who)
    bx = r + 18 if left else -r - 18 - bw
    col = '#FFFFFF' if left else '#C7ECFF'
    boilSeed('cb' + txt)
    if draft:
        G.c.drawRoundRect(skia.Rect.MakeXYWH(bx, -bh / 2, bw, bh), bh * .42, bh * .42, pa_('#FFFFFF', .55))
        eff = skia.DashPathEffect.Make([16, 10], 0)
        pp = pa_(APP, 1, 3.5)
        pp.setPathEffect(eff)
        G.c.drawRoundRect(skia.Rect.MakeXYWH(bx, -bh / 2, bw, bh), bh * .42, bh * .42, pp)
    else:
        G.c.drawRoundRect(skia.Rect.MakeXYWH(bx + 6, -bh / 2 + 8, bw, bh), bh * .42, bh * .42, pa_(INK, .16))
        paint(rrPts(bx, -bh / 2, bw, bh, bh * .42), wash=col, ink=INK, sw=1.1)
        tail = [[bx + 4, -6], [bx - 16, 4], [bx + 10, 16]] if left else [[bx + bw - 4, -6], [bx + bw + 16, 4], [bx + bw - 10, 16]]
        paint(tail, wash=col, ink=None)
    tx = bx + size * .55 + iw + tw / 2
    text(txt, tx, 2, size, INK, shadow=False, a=.85 if draft else 1)
    if icon:
        icon(bx + size * .55 + iw * .45, 0, size * .42)
    if strike > 0:
        L = (tw + iw) * clamp(strike / .5)
        ln(bx + size * .5, 0, bx + size * .5 + L, -4, '#E0344E', 1, 6)
    G.c.restore()
    pop()


def typingDots(x, y, t, k=1.0, who='her', size=46):
    if k <= .01:
        return
    push()
    translate(x, y)
    scale(backOut(clamp(k)))
    r = size * .78
    if who == 'her':
        miniFace(0, 0, r, 'her')
    bx = r + 18
    paint(rrPts(bx, -size * .85, size * 2.6, size * 1.7, size * .7), wash='#FFFFFF', ink=INK, sw=1.0)
    for i in range(3):
        a = .35 + .65 * (.5 + .5 * math.sin(t * 9 - i * 1.1))
        G.c.drawCircle(bx + size * .65 + i * size * .65, 0, size * .17, pa_('#8A8698', a))
    pop()


def riceIcon(x, y, s):
    paint([[x - s, y - .1 * s], [x + s, y - .1 * s], [x + .7 * s, y + .8 * s], [x - .7 * s, y + .8 * s]], wash='#E8476E', ink=INK, sw=.6)
    paint(ellPts(x, y - .15 * s, s * .95, s * .55, 14), wash='#FFFFFF', ink=INK, sw=.5)
    ln(x + .2 * s, y - .9 * s, x + 1.2 * s, y - 1.5 * s, '#8E5E3A', 1, 3)
    ln(x + .45 * s, y - .8 * s, x + 1.4 * s, y - 1.25 * s, '#8E5E3A', 1, 3)


def shadesIcon(x, y, s):
    for d in (-1, 1):
        paint(ellPts(x + d * .55 * s, y, .5 * s, .38 * s, 12), wash='#2A2740', ink=INK, sw=.5)
    ln(x - .1 * s, y - .1 * s, x + .1 * s, y - .1 * s, INK, 1, 3)


# ===================================================================== gag props
def heartP(x, y, r, col='#E8476E', a=1.0, key='hp', ink=True):
    if r <= 1:
        return
    boilSeed(key)
    if a < 1:
        G.c.saveLayerAlpha(None, int(255 * clamp(a)))
    paint(heartPts(x, y, r, 22), wash=col, fill=mixCol(col, INK, .18), fillOp=60, ink=INK if ink else None, sw=max(.6, r / 40))
    G.c.drawCircle(x - r * .35, y - r * .35, r * .14, pa_('#FFFFFF', .7))
    if a < 1:
        G.c.restore()


def crackedHeart(x, y, r, crack=0.0, gap=0.0, key='chp'):
    """a heart that cracks down the middle (crack 0..1) and splits by gap px"""
    for s in (-1, 1):
        G.c.save()
        p = skia.Path()
        zig = [[x, y - r * 1.3], [x - r * .12, y - r * .6], [x + r * .14, y - r * .15], [x - r * .1, y + r * .3], [x, y + r * 1.4]]
        if s < 0:
            poly = [[x - r * 2, y - r * 2], [x, y - r * 2]] + zig + [[x - r * 2, y + r * 2]]
        else:
            poly = [[x, y - r * 2], [x + r * 2, y - r * 2], [x + r * 2, y + r * 2]] + zig[::-1]
        G.c.clipPath(eng._path(poly), skia.ClipOp.kIntersect, True)
        G.c.translate(s * gap, 0)
        heartP(x, y, r, key=key)
        G.c.restore()
    if crack > 0:
        zig = [[x, y - r * .9], [x - r * .12, y - r * .6], [x + r * .14, y - r * .15], [x - r * .1, y + r * .3], [x, y + r * .9]]
        n = max(2, int(len(zig) * clamp(crack)))
        inkLine(zig[:n], 2.0, INK, 'ink', 0)


def bandAid(x, y, s, rot=.6, k=1.0):
    if k <= .01:
        return
    push()
    translate(x, y)
    rotate(rot)
    scale(backOut(k))
    boilSeed('band')
    paint(rrPts(-1.6 * s, -.45 * s, 3.2 * s, .9 * s, .45 * s), wash='#F6C9A0', ink=INK, sw=.8)
    paint(rectPts(-.5 * s, -.42 * s, 1.0 * s, .84 * s), wash='#EFB385', ink=None)
    for i in range(3):
        for j in range(2):
            G.c.drawCircle(-.25 * s + i * .25 * s, -.15 * s + j * .3 * s, .05 * s, pa_('#C98A5E'))
    pop()


def note(x, y, s, col='#5BC0EB', rot=0.0, a=1.0):
    push()
    translate(x, y)
    rotate(rot)
    G.c.drawOval(skia.Rect.MakeXYWH(-s * .55, -s * .3, s * .9, s * .62), pa_(col, a))
    ln(s * .3, 0, s * .3, -s * 1.3, col, a, max(2, s * .14))
    ln(s * .3, -s * 1.3, s * .8, -s * 1.0, col, a, max(2, s * .14))
    pop()


def thermo(x, y, h, val, label='', k=1.0, burst=0.0, t=0.0, key='th'):
    """big thermometer. (x, y) = bulb centre; val 0..1 fill (1 = top)."""
    boilSeed(key)
    r = h * .11
    tw = r * .9
    paint(rrPts(x - tw / 2 - 6, y - h, tw + 12, h, tw / 2 + 6), wash='#FFFFFF', ink=INK, sw=1.2)
    for i in range(9):
        yy = y - r - 20 - i * (h - r - 60) / 8
        ln(x + tw / 2 + 10, yy, x + tw / 2 + 34, yy, INK, .7, 3)
    top = y - r - (h - r - 30) * clamp(val)
    col = mixCol('#FF8A5B', '#E0242E', clamp(val))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x - tw / 2 + 6, top, tw - 12, y - top), (tw - 12) / 2, (tw - 12) / 2, pa_(col))
    paint(ellPts(x, y, r, r, 22), wash=col, ink=INK, sw=1.2)
    G.c.drawCircle(x - r * .35, y - r * .35, r * .2, pa_('#FFFFFF', .7))
    if label:
        text(label, x, y + r + 50, 64, col, stroke=INK, strokeW=10, shadow=False, sc=1 + .25 * math.exp(-max(0, k) * 8) if k >= 0 else 1)
    if burst > 0:
        b = clamp(burst * 3)
        G.c.drawCircle(x, y - h + 6, 26 + 30 * b, pa_('#E0242E'))
        G.c.drawCircle(x, y - h + 6, 26 + 30 * b, pa_(INK, 1, 3))
        cy = y - h - 30 - 260 * easeOut(clamp(burst * 2))
        paint(rrPts(x - 30, cy - 18, 60, 36, 10), wash='#C9C4D6', ink=INK, sw=.8)
        for i in range(7):
            a = -math.pi / 2 + (i - 3) * .42
            rr = 80 + 180 * easeOut(clamp(burst * 1.5))
            puff(x + math.cos(a) * rr, y - h - 20 + math.sin(a) * rr * .8, 60 * (1 - .3 * burst), '#FFFFFF', key=f'{key}st{i}', a=1 - .5 * burst)


def tapeMeasure(x0, x1, y, label, k=1.0, key='tm'):
    """yellow tape case at x0, tape out to x1"""
    boilSeed(key)
    xs, xe = min(x0, x1), max(x0, x1)
    paint(rectPts(xs, y - 18, xe - xs, 36), wash='#FFD84A', ink=INK, sw=.8)
    i = 0
    xx = x0
    step = 24 if x1 > x0 else -24
    while (xx - x1) * step < 0:
        L = 16 if i % 5 == 0 else 8
        ln(xx, y - 18, xx, y - 18 + L, INK, .8, 2)
        xx += step
        i += 1
    paint(rrPts(x0 - 54, y - 58, 108, 108, 24), wash='#F2C53D', fill='#D8A82A', fillOp=60, ink=INK, sw=1.0)
    G.c.drawCircle(x0, y - 4, 22, pa_('#2B2233'))
    paint(rectPts(x1 - 6 if x1 > x0 else x1 - 4, y - 26, 10, 52), wash='#9A96A8', ink=INK, sw=.6)
    if label:
        bubble((x0 + x1) / 2, y - 70, label, 50, None, k, col='#FFFDF6', key=key + 'lb')


def glassHeart(x, y, r, a=1.0, crack=0.0, key='gh', tag=True):
    boilSeed(key)
    G.c.saveLayerAlpha(None, int(255 * clamp(a)))
    glow(x, y, r * 2.2, '#BFE6FF', .5)
    paint(heartPts(x, y, r, 24), wash='#D8F0FF', washOp=200, ink=INK, sw=1.0)
    paint(heartPts(x - r * .1, y - r * .1, r * .6, 18), wash='#FFFFFF', washOp=120, ink=None)
    ln(x - r * .55, y - r * .4, x - r * .3, y - r * .7, '#FFFFFF', .9, 6)
    if tag:
        push()
        translate(x + r * .9, y + r * .55)
        rotate(.25)
        paint(rrPts(-50, -24, 100, 48, 8), wash='#FFFDF6', ink=INK, sw=.8)
        text('易碎', 0, 2, 32, '#E0344E', face=WENKAI, shadow=False)
        pop()
    G.c.restore()


def safeBox(x, y, s, lid=0.0, lock=0.0, key='safe'):
    """small safe; lid 0 = door swung wide open to the left (dial visible) .. 1 = shut; lock 0..1 padlock clicks"""
    boilSeed(key)
    w, h = 3.4 * s, 2.6 * s
    x0 = x - w / 2
    paint(rrPts(x0, y - h, w, h, .2 * s), wash='#8E96AE', fill='#6A7290', fillOp=60, ink=INK, sw=1.2)
    paint(rrPts(x0 + .4 * s, y - h + .4 * s, w - .8 * s, h - .8 * s, .1 * s), wash='#262A3C', ink=INK, sw=.7)
    for yy in (y - h + .9 * s, y - .5 * s):          # inner shelf lines
        ln(x0 + .5 * s, yy, x0 + w - .5 * s, yy, '#3E4460', 1, 3)
    for hy in (y - h + .5 * s, y - .7 * s):          # hinges
        paint(rrPts(x0 - .12 * s, hy, .24 * s, .35 * s, .06 * s), wash='#5E6680', ink=INK, sw=.5)
    k = easeOut(clamp(lid))
    ang = lerp(2.5, 0, k)                               # door angle around the hinge (0 = shut)
    dw = (w - .1 * s) * math.cos(ang)                   # projected width (negative = swung out to the left)
    sk = .35 * s * math.sin(ang)                        # perspective skew of the far edge
    hx_ = x0 + .05 * s
    door = [[hx_, y - h + .05 * s], [hx_ + dw, y - h + .05 * s - sk], [hx_ + dw, y - .05 * s + sk], [hx_, y - .05 * s]]
    paint(door, wash='#A9B0C6', fill='#8890AA', fillOp=50, ink=INK, sw=1.0)
    cx = hx_ + dw * .62
    dr = .42 * s * max(.25, abs(math.cos(ang)))
    G.c.drawOval(skia.Rect.MakeXYWH(cx - dr, y - h / 2 - .42 * s, 2 * dr, .84 * s), pa_('#DCE0EC'))
    G.c.drawOval(skia.Rect.MakeXYWH(cx - dr, y - h / 2 - .42 * s, 2 * dr, .84 * s), pa_(INK, 1, 2))
    ln(cx, y - h / 2, cx + dr * .7 * math.cos(lock * 3), y - h / 2 - .3 * s * math.sin(lock * 3 + .5), INK, 1, 2.5)
    if lock > 0:
        px, py = x + w * .32, y - h * .2
        shf = (1 - easeOut(clamp(lock))) * .4 * s
        G.c.drawArc(skia.Rect.MakeXYWH(px - .32 * s, py - .9 * s - shf, .64 * s, .8 * s), 180, 180, False, pa_('#5E5A70', 1, .14 * s))
        paint(rrPts(px - .45 * s, py - .5 * s, .9 * s, .75 * s, .12 * s), wash='#F2C53D', ink=INK, sw=.8)
        G.c.drawCircle(px, py - .15 * s, .09 * s, pa_(INK))


def mallet(hx, hy, ang, L, s, key='ml'):
    """wooden mallet held at (hx, hy); ang = handle direction (rad, 0 = right); head at the far end"""
    boilSeed(key)
    ex, ey = hx + math.cos(ang) * L, hy + math.sin(ang) * L
    inkLine([[hx, hy], [ex, ey]], 1.0, INK, 'ink', 0)
    p = skia.Path()
    p.moveTo(hx, hy)
    p.lineTo(ex, ey)
    G.c.drawPath(p, pa_('#C98A5A', 1, s * .26))
    G.c.drawPath(p, pa_(INK, .9, 1.5))
    push()
    translate(ex, ey)
    rotate(ang + math.pi / 2)
    paint(rrPts(-1.3 * s, -.7 * s, 2.6 * s, 1.4 * s, .25 * s), wash='#B9784E', fill='#8E5634', fillOp=70, ink=INK, sw=1.0)
    for d in (-1, 1):
        paint(rectPts(d * 1.3 * s - (.2 * s if d > 0 else 0), -.72 * s, .2 * s, 1.44 * s), wash='#8E5634', ink=None)
    pop()


def probBlock(x, y, w, h, txt, flat_=0.0, key='pb', col='#9AA0B8'):
    """a problem block standing on y; flat_ 0..1 squashes it into a pancake with a tick"""
    boilSeed(key)
    f = easeOut(clamp(flat_))
    hh = h * lerp(1, .16, f)
    ww = w * lerp(1, 1.5, f)
    paint(rrPts(x - ww / 2, y - hh, ww, hh, 14), wash=mixCol(col, '#7FCB7A', f), fill=mixCol(col, INK, .2), fillOp=60, ink=INK, sw=1.1)
    if f < .5:
        text(txt, x, y - hh * .62, min(w * .34, 60), '#FFFFFF', stroke=INK, strokeW=7, shadow=False)
        text('?', x, y - hh * .25, 54, '#FFE36E', stroke=INK, strokeW=7, shadow=False)
    else:
        check(x, y - hh / 2 - 36, 36, '#3FA45B', a=clamp((f - .5) * 3))


def check(x, y, s, col='#3FA45B', a=1.0):
    if a <= 0:
        return
    p = skia.Path()
    p.moveTo(x - s * .8, y)
    p.lineTo(x - s * .2, y + s * .6)
    p.lineTo(x + s * .9, y - s * .7)
    G.c.drawPath(p, pa_('#FFFFFF', a, s * .5))
    G.c.drawPath(p, pa_(col, a, s * .3))


def crossX(x, y, s, col='#E0344E', a=1.0, k=1.0):
    if a <= 0 or k <= 0:
        return
    s *= backOut(clamp(k))
    for d in (-1, 1):
        ln(x - s, y - d * s, x + s, y + d * s, '#FFFFFF', a, s * .5)
        ln(x - s, y - d * s, x + s, y + d * s, col, a, s * .3)


def snowflake(x, y, r, rot=0.0, col='#E8F6FF', a=1.0):
    for i in range(3):
        ang = rot + i * math.pi / 3
        dx, dy = math.cos(ang) * r, math.sin(ang) * r
        ln(x - dx, y - dy, x + dx, y + dy, col, a, max(1.5, r * .16))
        for s in (-1, 1):
            mx, my = x + s * dx * .55, y + s * dy * .55
            for b in (-.6, .6):
                ang2 = ang + b + (0 if s > 0 else math.pi)
                ln(mx, my, mx + math.cos(ang2) * r * .35, my + math.sin(ang2) * r * .35, col, a, max(1.2, r * .12))


def icicles(x0, x1, y, k, n=5, key='ic'):
    if k <= 0:
        return
    for i in range(n):
        xx = lerp(x0, x1, (i + .5) / n)
        L = (22 + 26 * hash1(i * 3.1)) * k
        boilSeed(f'{key}{i}')
        paint([[xx - 9, y], [xx + 9, y], [xx, y + L]], wash='#DDF4FF', washOp=230, ink=INK, sw=.6)


def leaf(x, y, s, rot, col='#E8833A'):
    push()
    translate(x, y)
    rotate(rot)
    paint([[-s, 0], [0, -s * .55], [s, 0], [0, s * .55]], wash=col, ink=INK, sw=.5, curv=.6)
    ln(-s * .8, 0, s * .8, 0, mixCol(col, INK, .4), .8, 1.2)
    pop()


def petal(x, y, s, rot, col='#FFC2D4'):
    push()
    translate(x, y)
    rotate(rot)
    G.c.drawOval(skia.Rect.MakeXYWH(-s, -s * .55, s * 2, s * 1.1), pa_(col))
    pop()


def pigeon(x, y, s, key='pg', flip=False):
    push()
    translate(x, y)
    if flip:
        scale(-1, 1)
    boilSeed(key)
    paint(ellPts(0, -s * .9, s * 1.3, s * .85, 18), wash='#A9A7B8', fill='#7E7B92', fillOp=60, ink=INK, sw=.8)
    paint(ellPts(s * 1.0, -s * 1.7, s * .55, s * .5, 14), wash='#9896AA', ink=INK, sw=.7)
    G.c.drawCircle(s * 1.15, -s * 1.8, s * .1, pa_(INK))
    paint([[s * 1.5, -s * 1.75], [s * 1.9, -s * 1.62], [s * 1.5, -s * 1.55]], wash='#F2C53D', ink=INK, sw=.4)
    paint(ellPts(-s * .2, -s * .95, s * .7, s * .45, 12), wash='#8E8BA0', ink=None)
    ln(-s * .1, 0, -s * .2, s * .25, '#E8833A', 1, 2.4)
    ln(s * .3, 0, s * .35, s * .25, '#E8833A', 1, 2.4)
    pop()


def busStop(x, y, s=1.0, key='bus'):
    boilSeed(key)
    paint(rectPts(x - 7 * s, y - 420 * s, 14 * s, 420 * s), wash='#77738A', ink=INK, sw=.7)
    paint(ellPts(x, y - 440 * s, 74 * s, 74 * s, 30), wash='#FFFFFF', ink=INK, sw=1.0)
    G.c.drawCircle(x, y - 440 * s, 60 * s, pa_('#E0573F', 1, 10 * s))
    text('巴士', x, y - 438 * s, 40 * s, '#2B2233', face=WENKAI, shadow=False)
    paint(rectPts(x - 50 * s, y - 340 * s, 100 * s, 140 * s), wash='#FFFDF6', ink=INK, sw=.6)
    for i in range(5):
        ln(x - 38 * s, y - 318 * s + i * 24 * s, x + 38 * s, y - 318 * s + i * 24 * s, '#C9C1D6', 1, 2)


def tempSign(x, y, txt, col='#E0573F', s=1.0, key='ts'):
    boilSeed(key)
    paint(rectPts(x - 6 * s, y - 300 * s, 12 * s, 300 * s), wash='#77738A', ink=INK, sw=.6)
    paint(rrPts(x - 110 * s, y - 400 * s, 220 * s, 110 * s, 12 * s), wash='#2B2233', ink=INK, sw=.9)
    text(txt, x, y - 344 * s, 62 * s, col, face=WENKAI, shadow=False)
