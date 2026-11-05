# cc2.py: the rest of 《匆匆那年》's world — teen / present looks, the past classroom (teacher's view), the desk from above with
# every state of the account, desk props, the school gate, the underside of the desk, the letter and the graduation photo.
import math
from cc import *
import cc
from hl import her17, him17, inkWrite, writeW, GREYS
from props import bubble, sparkle
from sets2 import seat
from wo import tearDrops, fountainPen, memoryLook, stickyNote
from hb import woodTop
import hanzi
from common import cam

# ================================================================ looks
_hat_prev2 = cc._cl.hat


def _hat2(u, h, sw, o=None):
    if h == 'beanieC':
        hb._beanie(u, sw, '#5C6676')
    else:
        _hat_prev2(u, h, sw, o)


cc._cl.hat = _hat2


def teen(who, x, y, u, o=None):
    (her17 if who == 'her' else him17)(x, y, u, o)


def himNow(x, y, u, o=None, snow=0.0):
    o = dict(o or {})
    o['hat'] = ['beanieC'] + (['snowhat'] if snow > .01 else [])
    o['snowK'] = snow
    him(x, y, u, o)


def now(who, x, y, u, o=None, snow=0.0):
    (herNow if who == 'her' else himNow)(x, y, u, o, snow)


def seatT(who):
    return lambda x, y, u, o: teen(who, x, y, u, o)


def pastGrade(k=1.0):
    """after camEnd(): the past — warm, a little glowing"""
    memoryLook(k)


def zzz(t, x, y, s=40, a=1.0):
    for i in range(3):
        ph = frac(t * .7 + i / 3)
        text('Z' if i % 2 == 0 else 'z', x + 30 * ph + i * 6, y - 90 * ph, s * (.6 + .5 * ph), '#FFFFFF', stroke=INK, strokeW=5,
             shadow=False, a=a * math.sin(ph * math.pi))


def tears(t, x, y, u, a=1.0, seed=1):
    tearDrops(t, x, y, u, seed=seed, n=2, rate=.9, a=a)


# ================================================================ handwriting with punctuation / digits (letters, notes)
def _units(txt):
    out = []
    for ch in txt:
        if ch == ' ':
            out.append((ch, 0, 'sp'))
        elif hanzi.glyph(ch):
            out.append((ch, hanzi.char_len(ch), 'h'))
        else:
            out.append((ch, 420, 'f'))
    return out


def handLine(txt, x0, y0, size, prog, col=INK, gap=.06, a=1.0, face=WENKAI):
    """write txt (stroke order for hanzi, glyphs pop in for punctuation / digits) up to prog; returns (tip x, y)"""
    us = _units(txt)
    tot = sum(L for _, L, _ in us) or 1
    done = clamp(prog) * tot
    x = x0
    tip = (x0, y0 + size * .6)
    pa = skia.Paint(AntiAlias=True, Color=skcol(col, .93 * a))
    for ch, L, kind in us:
        if kind == 'sp':
            x += size * .4
            continue
        p = clamp(done / L) if L else 0
        done -= L
        adv = size * (1 + gap) if (kind == 'h' or ord(ch) > 0x2000) else size * .56
        if p > 0:
            if kind == 'h':
                hanzi.write_char(G.c, ch, x, y0, size, p, [pa], mode='brush')
                if p < 1:
                    hp = hanzi.head_point(ch, p)
                    if hp is not None:
                        tip = (x + hp[0] * size / 1024, y0 + hp[1] * size / 1024)
            else:
                if p > .3:
                    text(ch, x + adv / 2 - size * .03, y0 + size * .55, size * .92, col, face=face, shadow=False, a=a)
                tip = (x + adv * .5, y0 + size * .7)
        x += adv
    return tip


# ================================================================ the desk from above, every state of the account
def carvingWrite(txt, x0, y0, size, prog, old=1.0, a=1.0):
    """letters scratched into the laminate with a compass point (dark lip + pale groove), stroke order"""
    for dx, dy, col, al in ((2.6, 3.0, '#5E4428', .55), (0, 0, mixCol('#F7EBD0', '#E8D7B4', old), .9)):
        pa = skia.Paint(AntiAlias=True, Color=skcol(col, al * a))
        x = x0
        tot = sum(hanzi.char_len(c) for c in txt)
        done = clamp(prog) * tot
        for ch in txt:
            L = hanzi.char_len(ch)
            p = clamp(done / L)
            done -= L
            if p > 0:
                hanzi.write_char(G.c, ch, x + dx, y0 + dy, size, p, [pa], mode='brush')
            x += size * 1.08


CARVE = ('永远一起', 54)
CARVE_X0 = LINE_X - (4 * 54 * 1.08 - 54 * .08) / 2 - 2      # the line passes between 远 and 一
CARVE_Y0 = 309


def carveTip(prog):
    txt, size = CARVE
    from wo import writeTip
    return writeTip(txt, CARVE_X0, CARVE_Y0, size, prog)


def tallyAt(side, i):
    """top-left of tally group i on a side"""
    gx, gy = HIS_GRID if side == 'his' else HER_GRID
    seed = 100 if side == 'his' else 300
    return gx + (i % 8) * 66 + (hash1(seed + i * 1.9) - .5) * 6, gy + (i // 8) * 76 + (hash1(seed + i * 2.7) - .5) * 6


def tallySide(side, n, newK=1.0, reveal=None, a=1.0):
    """n strokes on a side; the n-th stroke is drawn up to newK (a stroke being written)"""
    col = HIS_PEN if side == 'his' else HER_PEN
    seed = 100 if side == 'his' else 300
    rot0 = -.03 if side == 'his' else .02
    g = 0
    left = n
    while left > 0:
        k = min(5, left)
        gx, gy = tallyAt(side, g)
        al = a * (1.0 if reveal is None else reveal(gx + 25, gy + 25))
        last = left <= 5
        push()
        translate(gx, gy)
        rotate(rot0 + (hash1(seed + g + seed) - .5) * .06 if False else rot0 + (hash1(seed + g) - .5) * .06)
        for i in range(k):
            (ax, ay), (bx, by) = cc._ZH[i]
            j = lambda q: (hash1((seed + g) * 7.1 + i * 3.3 + q) - .5) * .08
            p0 = (ax * 50 + j(1) * 50, ay * 50 + j(2) * 50)
            p1 = (bx * 50 + j(3) * 50, by * 50 + j(4) * 50)
            if last and i == k - 1 and newK < 1:
                if newK <= 0:
                    break
                p1 = (lerp(p0[0], p1[0], newK), lerp(p0[1], p1[1], newK))
            penStroke(p0, p1, 3.4, col, al, (seed + g) * 5 + i)
        pop()
        left -= k
        g += 1


def whiteRows(prog=(1, 1, 1), old=1.0, a=1.0):
    """the correction-fluid patch over her 95 strokes, row by row; prog per row 0..1 (the pen moves left→right)"""
    gx, gy = HER_GRID
    rows = [(gx - 14, gx + 7 * 66 + 64, gy), (gx - 14, gx + 7 * 66 + 64, gy + 76), (gx - 14, gx + 2 * 66 + 62, gy + 152)]
    vis = []
    for (x0, x1, y), p in zip(rows, prog):
        if p > .01:
            vis.append((x0, lerp(x0 + 20, x1, p), y))
    if vis:
        whiteOut(vis, a, old, seed=8)
    return rows


def deskState(t, old=0.0, line=1.0, note=1.0, his=0, her=0, hisK=1.0, herK=1.0, white=None, carve=0.0, reveal=None,
              loneGlow=0.0, objs=None, petals=0.0, books=0.0, season='autumn', taunts=0.0, tents=0.0, shaft=0.0, carveA=1.0, graffiti=0.0):
    """the shared double desk from above in any year. old 0 = 2013 new laminate, 1 = 2026 worn"""
    x0, y0, x1, y1 = DESK
    cc._terrazzo(-1400, -1200, W + 1400, H + 1300, mixCol('#A39A88', '#8E8F8C', old), seed=5)
    for cx in (520, 1400):
        boilSeed('chairtop%d' % cx)
        paint(rrPts(cx - 130, y1 + 26, 260, 34, 12), wash='#A9784C', fill='#7E5636', fillOp=60, ink=INK, sw=.8)
    G.c.drawRect(skia.Rect.MakeXYWH(x0 + 26, y0 + 36, x1 - x0, y1 - y0), skia.Paint(AntiAlias=True, Color=skcol('#000000', .28)))
    boilSeed('deskedge')
    paint(rrPts(x0 - 16, y0 - 16, x1 - x0 + 32, y1 - y0 + 32, 16), wash='#8C6A48', fill='#6E5034', fillOp=60, ink=INK, sw=1.0)
    boilSeed('desktop')
    paint(rectPts(x0, y0, x1 - x0, y1 - y0), wash=mixCol('#E8CC9C', '#D2B98F', old), fill='#C49C6C', fillOp=60 if old > .5 else 40,
          bleed=.04, tex=.6, border=.5, ink=INK, sw=.9)
    for i in range(24):
        y = y0 + 18 + i * (y1 - y0 - 30) / 23 + 6 * math.sin(i * 1.9)
        p = skia.Path()
        p.moveTo(x0 + 6, y)
        p.cubicTo(x0 + 500, y + 10 * math.sin(i), x0 + 1100, y - 9 * math.cos(i * 1.3), x1 - 6, y + 4)
        G.c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=skcol('#A9814F', .28)))
    paint(rrPts(x0 + 120, y0 + 26, x1 - x0 - 240, 22, 10), wash='#B08860', fill='#8A6440', fillOp=50, ink=INK, sw=.5)
    if old > .3:                                              # ten years of other people's scratches
        for i in range(18):
            x = x0 + 80 + hash1(i * 4.1) * (x1 - x0 - 160)
            y = y0 + 80 + hash1(i * 6.7) * (y1 - y0 - 160)
            a_ = hash1(i * 2.3) * TAU
            L = 20 + 40 * hash1(i * 8.1)
            penStroke((x, y), (x + math.cos(a_) * L, y + math.sin(a_) * L), 1.5, '#8E6A44', .35 * old, i, .1)
        for (cx, cy, r) in ((1500, 740, 34), (1540, 770, 18), (1470, 790, 52)):
            G.c.drawCircle(cx, cy, r, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=skcol('#8E6A44', .45)))
        for (bx, by, r) in ((1196, 690, 7), (1214, 702, 4), (402, 640, 5)):
            G.c.drawCircle(bx, by, r, skia.Paint(AntiAlias=True, Color=skcol(HIS_PEN if bx > 900 else HER_PEN, .5)))
        boilSeed('sticker')
        paint(starPts(300, 800, 38, .45, 5, -.3), wash=mixCol('#F7D36E', '#E8DCC0', .5 * old), ink=INK, sw=.5, lite=True)
    else:
        boilSeed('sticker')
        paint(starPts(300, 800, 38, .45, 5, -.3), wash='#F7D36E', ink=INK, sw=.5, lite=True)
    if graffiti > .01:
        graffitiDraw(graffiti, old)
    if carve > 0 and carveA > .01:
        carvingWrite(CARVE[0], CARVE_X0, CARVE_Y0, CARVE[1], carve, old, carveA)
    if taunts > .01:
        tauntsDraw(taunts, old)
    if tents > .01:
        placeCard(505, 872, '方茴', -.05, tents, 'pcH')
        placeCard(1418, 872, '陈寻', .04, tents, 'pcM')
    # the line
    if line > 0:
        ya, yb = y0 + 14, y1 - 14
        for j, off in enumerate((-1.6, 0.0, 1.8)):
            if old < .5 and j != 1:
                continue
            yy = lerp(yb, ya, line) if j == 1 else ya
            penStroke((LINE_X + off * .6, yb), (LINE_X + off, yy), 4.2 - j * .6, LINE_PEN, (.85 - .12 * j) * (1 - .25 * old), 40 + j, .004)
    if his:
        tallySide('his', his, hisK, reveal)
    if her:
        tallySide('her', her, herK, reveal)
    if white is not None:
        whiteRows(white, old, 1.0 if reveal is None else reveal(600, HER_GRID[1] + 80))
        if old > .5:
            G.c.saveLayerAlpha(None, 30)
            tallySide('her', min(her, 95), 1.0, reveal)
            G.c.restore()
    if loneGlow > .01:
        glow(LONE[0], LONE[1], 60, '#FFD6E2', .45 * loneGlow)
    if note > .01:
        nx, ny = NOTE_XY
        push()
        translate(nx, ny)
        rotate(-.035)
        G.c.saveLayerAlpha(None, int(255 * clamp(note)))
        G.c.drawRect(skia.Rect.MakeXYWH(-196, -44, 400, 100), skia.Paint(AntiAlias=True, Color=skcol('#000000', .18)))
        boilSeed('rulenote')
        paint(rectPts(-200, -50, 400, 100, 1), wash=mixCol('#FFF8E0', '#EBDDB2', old), fill='#E2D2A4', fillOp=50, ink=INK, sw=.7, lite=True)
        for tx in (-200, 200):
            G.c.save()
            G.c.translate(tx, -40)
            G.c.rotate(-20 if tx < 0 else 18)
            G.c.drawRect(skia.Rect.MakeXYWH(-34, -13, 68, 26), skia.Paint(AntiAlias=True, Color=skcol('#F1EEE4', .55)))
            G.c.restore()
        text('过线一次 欠一次！', 0, 2, 38, mixCol(HER_PEN, '#9A6E7C', .35 * old), face=WENKAI, shadow=False, a=.92)
        G.c.restore()
        pop()
    if shaft > .01:
        lightShaft(shaft)
    if books > .01:
        textbookStack(250, 260, books, 'L')
        textbookStack(1670, 260, books, 'R')
    if petals > .01:
        driftPetals(t, petals, season)
    if objs:
        objs()


# years of scribbles: theirs first (2013–2016), then the classes after them. (text, x, y, size, colour, rot, alpha)
_BLUE, _BLK, _RED, _PCL, _GRN = '#3A55A0', '#2B2B38', '#C8324A', '#7A7A84', '#2F7A5A'
GRAFFITI = [
    ('早', 232, 262, 66, 'carve', -.05, 1.0),
    ('sin²α+cos²α=1', 440, 236, 30, _PCL, -.05, .8),
    ('好困…', 690, 252, 36, _BLUE, .08, .85),
    ('#ttt', 330, 400, 92, _BLK, 0, .8),
    ('考试必过！！', 560, 338, 34, _RED, -.1, .85),
    ('Fighting!', 730, 420, 32, _BLK, .12, .8),
    ('#smile', 480, 470, 24, _BLUE, 0, .8),
    ('E=mc²', 1170, 242, 36, _BLK, -.04, .8),
    ('距高考 200 天', 1430, 250, 32, _RED, .05, .85),
    ('下课了吗', 1650, 302, 30, _BLUE, -.15, .8),
    ('#cat', 1280, 352, 30, _PCL, 0, .85),
    ('学习使我快乐？', 1470, 362, 28, _PCL, .04, .8),
    ('Never give up', 1190, 444, 28, _BLUE, -.06, .8),
    ('老班来了！！', 1580, 450, 30, _RED, .1, .85),
    ('Δ=b²-4ac', 880, 236, 26, _PCL, -.03, .8),
    ('今天吃什么', 880, 470, 28, _GRN, .05, .8),
    ('加油', 1050, 462, 34, _RED, -.08, .8),
    ('静', 242, 610, 56, _PCL, -.05, .7),
    ('#stick', 250, 720, 30, _BLK, 0, .8),
    ('忍', 1690, 600, 56, _PCL, .06, .7),
    ('2015.12.18', 1688, 716, 24, _BLUE, -1.4, .75),
    ('高考必胜', 268, 858, 28, _RED, -.05, .85),
    ('#scribble', 1236, 900, 40, _BLK, 0, .7),
    ('到此一游', 1640, 868, 28, _BLUE, .06, .8),
    ('zZ', 690, 924, 26, _PCL, -.1, .7),
    ('2019届 王小胖到此一游', 600, 512, 22, _BLK, -.04, .65),
    ('a²+b²=c²', 1600, 520, 24, _PCL, .08, .7),
    ('#star', 395, 320, 16, _RED, 0, .8),
    ('#star', 1350, 290, 14, _BLUE, 0, .8),
    ('#heart', 1385, 470, 16, _RED, 0, .75),
    ('#house', 1712, 410, 26, _BLK, 0, .75),
    ('#arrow', 760, 300, 40, _BLUE, .3, .7),
    ('#scribble', 330, 940, 26, _BLUE, 0, .55),
    ('我要上大学', 1120, 300, 26, _GRN, .1, .7),
    ('2023 加油！', 300, 556, 22, _GRN, -.08, .65),
    ('#ttt', 1690, 830, 50, _PCL, .1, .55),
]
_GRAF_ERA = 18          # the first entries are from their years; the rest came after they graduated


def _doodle(kind, s, col, a):
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.6, StrokeCap=skia.Paint.kRound_Cap, Color=skcol(col, a))
    c = G.c
    if kind == '#ttt':
        for i in (1, 2):
            c.drawLine(-s / 2 + i * s / 3, -s / 2, -s / 2 + i * s / 3, s / 2, pa)
            c.drawLine(-s / 2, -s / 2 + i * s / 3, s / 2, -s / 2 + i * s / 3, pa)
        for (i, j, m) in ((0, 0, 'x'), (1, 1, 'o'), (2, 0, 'x'), (0, 2, 'o'), (2, 2, 'x')):
            cx, cy = -s / 3 + i * s / 3, -s / 3 + j * s / 3
            r = s * .1
            if m == 'x':
                p2 = skia.Paint(pa)
                p2.setColor(skcol(_RED, a))
                c.drawLine(cx - r, cy - r, cx + r, cy + r, p2)
                c.drawLine(cx - r, cy + r, cx + r, cy - r, p2)
            else:
                c.drawCircle(cx, cy, r, pa)
    elif kind == '#smile':
        c.drawCircle(0, 0, s, pa)
        c.drawCircle(-s * .35, -s * .25, 2.5, skia.Paint(AntiAlias=True, Color=skcol(col, a)))
        c.drawCircle(s * .35, -s * .25, 2.5, skia.Paint(AntiAlias=True, Color=skcol(col, a)))
        c.drawArc(skia.Rect.MakeXYWH(-s * .55, -s * .4, s * 1.1, s * .9), 20, 140, False, pa)
    elif kind == '#cat':
        c.drawCircle(0, 0, s, pa)
        for d in (-1, 1):
            p = skia.Path()
            p.moveTo(d * s * .5, -s * .85)
            p.lineTo(d * s * .9, -s * 1.5)
            p.lineTo(d * s * .95, -s * .45)
            c.drawPath(p, pa)
            c.drawLine(d * s * .3, s * .15, d * s * 1.4, s * .05, pa)
            c.drawLine(d * s * .3, s * .3, d * s * 1.35, s * .4, pa)
            c.drawCircle(d * s * .35, -s * .2, 2.4, skia.Paint(AntiAlias=True, Color=skcol(col, a)))
    elif kind == '#stick':
        c.drawCircle(0, -s * 1.1, s * .35, pa)
        c.drawLine(0, -s * .75, 0, s * .2, pa)
        c.drawLine(-s * .5, -s * .5, s * .5, -s * .7, pa)
        c.drawLine(0, s * .2, -s * .35, s * .8, pa)
        c.drawLine(0, s * .2, s * .35, s * .8, pa)
    elif kind == '#scribble':
        p = skia.Path()
        p.moveTo(-s, 0)
        for i in range(14):
            p.lineTo(-s + (i + 1) * s * 2 / 14, (s * .45 if i % 2 else -s * .45) + (hash1(i * 2.7) - .5) * s * .3)
        c.drawPath(p, pa)
    elif kind == '#star':
        c.drawPath(_path_pts(starPts(0, 0, s, .45, 5)), pa)
    elif kind == '#heart':
        c.drawPath(_path_pts(heartPts(0, 0, s)), pa)
        c.drawLine(-s * 1.8, s * .9, s * 1.8, -s * .9, pa)
    elif kind == '#house':
        c.drawRect(skia.Rect.MakeXYWH(-s * .6, -s * .2, s * 1.2, s), pa)
        p = skia.Path()
        p.moveTo(-s * .8, -s * .2)
        p.lineTo(0, -s)
        p.lineTo(s * .8, -s * .2)
        c.drawPath(p, pa)
    elif kind == '#arrow':
        c.drawLine(-s, 0, s, 0, pa)
        c.drawLine(s, 0, s * .6, -s * .3, pa)
        c.drawLine(s, 0, s * .6, s * .3, pa)


def _path_pts(pts):
    p = skia.Path()
    p.addPoly([skia.Point(float(a), float(b)) for a, b in pts], True)
    return p


def graffitiDraw(k, old=1.0):
    """scribbles all over the desk; k = how much of the list (their years first, then the classes after)"""
    n = int(round(len(GRAFFITI) * clamp(k)))
    fade = 1 - .28 * old
    for i, (s, x, y, size, col, rot, a) in enumerate(GRAFFITI[:n]):
        if i < _GRAF_ERA:
            a *= fade
        push()
        translate(x, y)
        rotate(rot)
        if s.startswith('#'):
            _doodle(s, size, col, a)
        elif col == 'carve':
            text(s, 2.5, 3, size, '#5E4428', face=WENKAI, shadow=False, a=.5 * a)
            text(s, 0, 0, size, mixCol('#F7EBD0', '#E8D7B4', old), face=WENKAI, shadow=False, a=.85 * a)
        else:
            text(s, 0, 0, size, col, face=WENKAI, shadow=False, a=a)
        pop()
    # tiny marks everywhere free: hash marks, dots, little arrows
    for i in range(int(70 * clamp(k))):
        x = DESK[0] + 40 + hash1(i * 7.7 + 1) * (DESK[2] - DESK[0] - 80)
        y = DESK[1] + 60 + hash1(i * 3.9 + 2) * (DESK[3] - DESK[1] - 100)
        if (330 < x < 940 and 520 < y < 770) or (1030 < x < 1610 and 520 < y < 770) or (740 < x < 1180 and 760 < y < 940) \
                or (390 < x < 640 and 810 < y < 930) or (1300 < x < 1540 and 810 < y < 930) or (830 < x < 1090 and 290 < y < 380):
            continue
        col = (_BLUE, _BLK, _PCL, _RED)[i % 4]
        L = 8 + 14 * hash1(i * 5.1)
        ang = hash1(i * 2.2) * TAU
        penStroke((x, y), (x + math.cos(ang) * L, y + math.sin(ang) * L), 2.0, col, .45, i, .2)


def tauntsDraw(a, old=0.0):
    """what they scribbled at the line: hers 「过线的是猪」 + a pig, his reply 「你才是」 + an arrow at hers"""
    G.c.saveLayerAlpha(None, int(255 * clamp(a) * (1 - .22 * old)))
    push()
    translate(842, 786)
    rotate(-.06)
    text('过线的是猪', 0, 0, 36, HER_PEN, face=WENKAI, shadow=False)
    pigDoodle(-128, -2, 22, HER_PEN)
    pop()
    push()
    translate(1094, 792)
    rotate(.05)
    text('你才是', 0, 0, 36, HIS_PEN, face=WENKAI, shadow=False)
    pop()
    penStroke((1036, 796), (996, 794), 3.0, HIS_PEN, 1.0, 5, .1)
    penStroke((996, 794), (1010, 783), 3.0, HIS_PEN, 1.0, 6, .05)
    penStroke((996, 794), (1010, 806), 3.0, HIS_PEN, 1.0, 7, .05)
    G.c.restore()


def pigDoodle(x, y, r, col):
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skcol(col, .95))
    G.c.drawCircle(x, y, r, pa)
    G.c.drawOval(skia.Rect.MakeXYWH(x - r * .45, y + r * .05, r * .9, r * .55), pa)
    for dx in (-.18, .18):
        G.c.drawCircle(x + dx * r, y + r * .32, 2.2, skia.Paint(AntiAlias=True, Color=skcol(col)))
        G.c.drawCircle(x + dx * 2.2 * r, y - r * .3, 2.6, skia.Paint(AntiAlias=True, Color=skcol(col)))
    for d in (-1, 1):
        p = skia.Path()
        p.moveTo(x + d * r * .55, y - r * .8)
        p.lineTo(x + d * r * .95, y - r * 1.25)
        p.lineTo(x + d * r * .9, y - r * .6)
        G.c.drawPath(p, pa)


def placeCard(x, y, name, rot, a, key):
    """a reunion place card lying flat on a seat end of the desk"""
    push()
    translate(x, y)
    rotate(rot)
    G.c.saveLayerAlpha(None, int(255 * clamp(a)))
    G.c.drawRect(skia.Rect.MakeXYWH(-104, -44, 220, 104), skia.Paint(AntiAlias=True, Color=skcol('#000000', .22)))
    boilSeed(key)
    paint(rectPts(-110, -50, 220, 100, 1), wash='#FFFDF8', ink=INK, sw=.7)
    paint(rectPts(-110, -50, 220, 22), wash='#C8324A', ink=None)
    text('高三(2)班 · 十年', 0, -39, 15, '#FFF3E2', face=WENKAI, shadow=False)
    text(name, 0, 14, 46, INK, face=WENKAI, shadow=False)
    G.c.restore()
    pop()


def lightShaft(a, col='#FFF2D8'):
    """a soft diagonal band of light across the desk (world space), with a brighter core"""
    for w_, al in ((520, .10), (220, .10)):
        p = skia.Path()
        p.addPoly([skia.Point(-300, -200), skia.Point(-300 + w_, -200), skia.Point(1700 + w_, 1300), skia.Point(1700, 1300)], True)
        pa = skia.Paint(AntiAlias=True, Color=skcol(col, al * a))
        pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, 70))
        pa.setBlendMode(skia.BlendMode.kScreen)
        G.c.drawPath(p, pa)


def driftPetals(t, a, season='spring'):
    col = {'spring': '#F7C6D4', 'autumn': '#F2C14E', 'summer': '#BFE3A8'}.get(season, '#F7C6D4')
    for i in range(7):
        x = 300 + hash1(i * 3.1) * 1300 + 40 * math.sin(t * .6 + i)
        y = 220 + hash1(i * 5.3) * 620 + 20 * math.cos(t * .5 + i)
        boilSeed('pet%d' % i)
        paint(ellPts(x, y, 14, 9, 10, 0, hash1(i) * TAU + t * .3), wash=col, washOp=int(255 * a), ink=INK, sw=.4, lite=True)


def textbookStack(x, y, k, side):
    """高三 piles of textbooks seen from above at the far corners"""
    titles = ['数学', '英语', '物理', '语文', '化学']
    cols = ['#5E8FC4', '#C9727F', '#E7C46A', '#7FB59A', '#A98BC9']
    n = int(1 + 4 * clamp(k))
    for i in range(n):
        push()
        translate(x + (i % 2) * 8 * (1 if side == 'L' else -1), y + i * 6)
        rotate((hash1(i * 3 + (side == 'L')) - .5) * .12)
        G.c.drawRect(skia.Rect.MakeXYWH(-118, -78, 236, 160), skia.Paint(AntiAlias=True, Color=skcol('#000000', .15)))
        boilSeed('tb%s%d' % (side, i))
        paint(rectPts(-120, -84, 236, 160), wash=cols[i % 5], fill=mixCol(cols[i % 5], INK, .3), fillOp=40, ink=INK, sw=.7)
        if i == n - 1:
            paint(rectPts(-80, -40, 156, 54), wash='#FBF8F0', ink=None)
            text(titles[i % 5], -2, -13, 36, INK, face=WENKAI, shadow=False)
        pop()


# ---------------------------------------------------------------- desk props (seen from above)
def penTop(x, y, ang=-2.3, col='#2E3A66', L=300, key='pen', white=False):
    """a pen seen from above whose tip is at (x, y); no hand"""
    push()
    translate(x, y)
    rotate(ang)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(14, -8, L, 26), 10, 10, skia.Paint(AntiAlias=True, Color=skcol('#000000', .25)))
    boilSeed(key)
    if white:                                                  # correction pen: white body, blue cap end
        paint([[0, 0], [30, -10], [30, 10]], wash='#C9CED6', ink=INK, sw=.6)
        paint(rrPts(28, -15, L * .78, 30, 12), wash='#FBFBF8', ink=INK, sw=.8)
        paint(rrPts(28 + L * .78, -16, L * .24, 32, 12), wash='#5E8FC4', ink=INK, sw=.8)
        text('修正液', 28 + L * .38, 0, 18, '#5E8FC4', face=WENKAI, shadow=False)
    else:
        paint([[0, 0], [26, -7], [26, 7]], wash='#D8D3C8', ink=INK, sw=.5)
        paint(rrPts(24, -10, L, 20, 9), wash=col, fill=mixCol(col, INK, .3), fillOp=50, ink=INK, sw=.7)
        paint(rrPts(24 + L * .72, -14, 12, 28, 4), wash='#D8D3C8', ink=INK, sw=.5)
    pop()


def ruler(x, y, L, ang=-math.pi / 2, a=.8):
    push()
    translate(x, y)
    rotate(ang)
    G.c.drawRect(skia.Rect.MakeXYWH(0, 6, L, 52), skia.Paint(AntiAlias=True, Color=skcol('#DDF0F4', .45 * a)))
    G.c.drawRect(skia.Rect.MakeXYWH(0, 6, L, 52), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2,
                                                               Color=skcol('#6E8C96', .7 * a)))
    for i in range(int(L / 20)):
        G.c.drawLine(i * 20, 6, i * 20, 6 + (16 if i % 5 == 0 else 9), skia.Paint(AntiAlias=True, Color=skcol('#4E6A74', .7 * a), StrokeWidth=1.5))
    pop()


def pencilCase(x, y, rot=0.0, col='#3F5FAE', key='pcase'):
    push()
    translate(x, y)
    rotate(rot)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-126, -24, 260, 70), 30, 30, skia.Paint(AntiAlias=True, Color=skcol('#000000', .25)))
    boilSeed(key)
    paint(rrPts(-130, -34, 260, 68, 30), wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=.9)
    inkLine([[-110, -2], [110, -2]], .7, '#E8E1D2', 'inkfine', 0)
    paint(rrPts(96, -12, 24, 18, 5), wash='#E8E1D2', ink=INK, sw=.5)
    pop()


def milkBox(x, y, rot=0.0, s=1.0, key='milk', old=0.0):
    """a 250 ml carton of milk seen from above, with its bent straw"""
    push()
    translate(x, y)
    rotate(rot)
    scale(s)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-62, -36, 132, 88), 8, 8, skia.Paint(AntiAlias=True, Color=skcol('#000000', .25)))
    boilSeed(key)
    paint(rrPts(-66, -44, 132, 88, 8), wash=mixCol('#FBFBF6', '#EEE8D8', old), ink=INK, sw=.9)
    paint(rrPts(-66, 8, 132, 36, 6), wash='#5E9BD6', ink=None)
    text('纯牛奶', 0, -16, 26, '#3B6EA8', face=WENKAI, shadow=False)
    paint(ellPts(40, -26, 7, 7, 10), wash='#C9CED6', ink=INK, sw=.4)
    inkLine([[40, -26], [80, -70], [130, -66]], 2.4, '#F2A9BC', 'ink', .4)
    pop()


def noteText(x, y, w, lines, col='#FBE7A1', rot=0.0, key='nt', size=30, ink_=HIS_PEN, a=1.0):
    if a <= .01:
        return
    G.c.saveLayerAlpha(None, int(255 * a))
    stickyNote(x, y, w, rot, col, key=key)
    push()
    translate(x, y)
    rotate(rot)
    for i, s in enumerate(lines):
        text(s, 0, -w * .12 + i * size * 1.3 - (len(lines) - 1) * size * .5, size, ink_, face=WENKAI, shadow=False)
    pop()
    G.c.restore()


def compassTop(x, y, ang=-.6, key='cmp'):
    """a compass seen from above: the needle leg's point at (x, y), the pencil leg off to one side"""
    hx, hy = x + math.cos(ang) * 190, y + math.sin(ang) * 190
    px, py = hx + math.cos(ang + .9) * 190, hy + math.sin(ang + .9) * 190
    G.c.drawLine(x + 10, y + 14, hx + 10, hy + 14, skia.Paint(AntiAlias=True, Color=skcol('#000000', .25), StrokeWidth=10))
    boilSeed(key)
    inkLine([[x, y], [hx, hy]], 2.6, '#9AA3AE', 'ink', 0)
    inkLine([[px, py], [hx, hy]], 2.6, '#9AA3AE', 'ink', 0)
    paint(ellPts(hx, hy, 16, 16, 12), wash='#C9CED6', ink=INK, sw=.6)
    paint(ellPts(px, py, 9, 9, 10), wash='#E7C46A', ink=INK, sw=.5)
    G.c.drawCircle(x, y, 3, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .9)))


def envelope(x, y, w, rot=0.0, label='', old=0.0, key='env', a=1.0, sticker=True):
    """pink envelope seen flat; label written on it in his navy hand"""
    if a <= .01:
        return
    h = w * .62
    push()
    translate(x, y)
    rotate(rot)
    G.c.saveLayerAlpha(None, int(255 * a))
    G.c.drawRect(skia.Rect.MakeXYWH(-w / 2 + 8, -h / 2 + 10, w, h), skia.Paint(AntiAlias=True, Color=skcol('#000000', .22)))
    boilSeed(key)
    col = mixCol('#F9C9D6', '#E9CFB8', old)
    paint(rectPts(-w / 2, -h / 2, w, h), wash=col, fill=mixCol(col, INK, .12), fillOp=40, ink=INK, sw=.8)
    inkLine([[-w / 2, -h / 2], [0, h * .08], [w / 2, -h / 2]], .6, mixCol(col, INK, .4), 'inkfine', 0)
    if sticker:
        heart(0, h * .05, w * .07, '#E2476E', key=key + 'h', sw=.4, shine=False) if False else \
            paint(heartPts(0, h * .06, w * .07), wash=mixCol('#E2476E', '#C9A0A8', old), ink=INK, sw=.4)
    if label:
        text(label, 0, h * .3, w * .12, mixCol(HIS_PEN, '#6E6A80', old * .5), face=WENKAI, shadow=False)
    G.c.restore()
    pop()


# ================================================================ the past classroom, teacher's view (they sit facing us)
PD_FLOOR = 880
PD_SEAT = 760
PD_TOP = 706
PD_X0, PD_X1 = 540, 1380
P_HER, P_HIM = 760, 1160
U2 = 34


def backWall(t, era='2013', light=1.0):
    flatRect(-900, -1000, W + 1800, 1520, '#F0E6D0')
    boilSeed('bwall')
    paint(rectPts(-900, -1000, W + 1800, 1520), fill='#E0D2B6', fillOp=40, bleed=.02, tex=.8, border=.2, ink=None)
    flatRect(-900, 520, W + 1800, 360, '#93B6A0')
    boilSeed('bdado')
    paint(rectPts(-900, 520, W + 1800, 360), fill='#78A08A', fillOp=50, bleed=.02, tex=.8, border=.2, ink=None)
    flatRect(-900, 514, W + 1800, 10, '#6D8E7E')
    cc._terrazzo(-900, 880, W + 900, 1700, '#B8AF9C', seed=19)
    flatRect(-900, 868, W + 1800, 14, '#6A6052')
    # warm afternoon light falling across the wall
    G.c.drawPath(cc_poly([[-200, -200], [520, -200], [980, 900], [260, 900]]), skia.Paint(AntiAlias=True, Color=skcol('#FFE7B8', .22 * light)))
    # the back blackboard bulletin 黑板报
    boilSeed('bbb')
    paint(rrPts(420, 70, 1080, 380, 8), wash='#6E5038', ink=INK, sw=.9)
    paint(rectPts(444, 94, 1032, 332), wash='#35503F', fill='#2A4433', fillOp=70, tex=.7, ink=INK, sw=.6)
    title = {'2013': '新学期 新起点', '2014': '青春不散场', '2015': '高考加油！'}.get(era, '新学期 新起点')
    chalkText(title, 960, 150, 56, .92, col='#F7D36E', seed=12)
    boilSeed('bbbdoodle')
    G.c.drawCircle(560, 170, 34, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=skcol('#F7D36E', .8)))
    for i in range(8):
        a_ = i / 8 * TAU
        G.c.drawLine(560 + math.cos(a_) * 44, 170 + math.sin(a_) * 44, 560 + math.cos(a_) * 60, 170 + math.sin(a_) * 60,
                     skia.Paint(AntiAlias=True, Color=skcol('#F7D36E', .8), StrokeWidth=4))
    for i, (fx, fy, col) in enumerate(((1340, 360, '#F2A9BC'), (1400, 340, '#9FD3E8'), (1280, 350, '#F7D36E'))):
        for j in range(5):
            a_ = j / 5 * TAU
            G.c.drawCircle(fx + math.cos(a_) * 14, fy + math.sin(a_) * 14, 9, skia.Paint(AntiAlias=True, Color=skcol(col, .75)))
    for j in range(3):
        G.c.drawLine(500, 250 + j * 50, 860 - j * 40, 250 + j * 50, skia.Paint(AntiAlias=True, Color=skcol('#E8EDE6', .45), StrokeWidth=4))
        G.c.drawLine(1000, 250 + j * 50, 1420 - j * 60, 250 + j * 50, skia.Paint(AntiAlias=True, Color=skcol('#9FD3E8', .45), StrokeWidth=4))
    # clock and a row of bag hooks
    wallClock2(1700, 200, 54, 3, 40, key='bclock')
    for i in range(6):
        hx = -380 + i * 110
        G.c.drawCircle(hx, 470, 6, skia.Paint(AntiAlias=True, Color=skcol('#6E6878')))


def cc_poly(pts):
    p = skia.Path()
    p.addPoly([skia.Point(float(a), float(b)) for a, b in pts], True)
    return p


def backRow(t, n_off=()):
    """classmates in the row behind (grey, smaller and higher: farther from us), seated at their desks"""
    xs = [80, 380, 1540, 1840]
    u = 22
    for i, x in enumerate(xs):
        if i in n_off:
            continue
        g_ = GREYS[i % len(GREYS)]
        seatTop = 600
        boilSeed('brchair%d' % i)
        paint(rectPts(x - 56, seatTop - 92, 112, 54), wash='#B58A5E', ink=INK, sw=.5, lite=True)
        clawd(x, seatTop + 2 * u, u, dict(col=g_[0], dk=g_[1], lt=g_[2], view='front', eyes='normal', mouth='flat', noShadow=True,
                                          boilKey='cm%d' % i, lite=True, lookX=.3 * math.sin(t * .4 + i), aL=-.2, aR=-.2,
                                          dy=-.15 * abs(math.sin(t * 1.1 + i))))
        boilSeed('brdesk%d' % i)
        paint(rectPts(x - 150, 560, 300, 10), wash='#D8B88E', ink=INK, sw=.5, lite=True)
        paint(rectPts(x - 150, 570, 300, 14), wash='#9C7652', ink=INK, sw=.5, lite=True)
        for lx in (x - 140, x + 140):
            inkLine([[lx, 584], [lx, 700]], .9, '#7A7F88', 'ink', 0)
    flatRect(-900, 520, W + 1800, 200, '#F0E6D0', .0)


def chairBack(x, key):
    boilSeed(key)
    paint(rrPts(x - 82, PD_SEAT - 200, 164, 96, 10), wash='#B07D50', fill='#8A5E38', fillOp=60, ink=INK, sw=.8)
    for px in (x - 70, x + 70):
        inkLine([[px, PD_SEAT - 104], [px, PD_SEAT]], 1.3, '#6E737C', 'ink', 0)


def chairSeat(x, key):
    boilSeed(key + 's')
    paint(rectPts(x - 88, PD_SEAT, 176, 14), wash='#A9784C', ink=INK, sw=.7)
    for px in (x - 74, x + 74):
        inkLine([[px, PD_SEAT + 14], [px, PD_FLOOR + 4]], 1.3, '#6E737C', 'ink', 0)


def pastDesk(t, items=None, lineMark=True):
    """the main double desk in front of them: thin top + front edge, metal legs (no front panel: their legs show)"""
    boilSeed('pdtop')
    paint([[PD_X0 + 10, PD_TOP - 18], [PD_X1 - 10, PD_TOP - 18], [PD_X1, PD_TOP], [PD_X0, PD_TOP]], wash='#EAD1A6', ink=INK, sw=.8)
    paint(rectPts(PD_X0, PD_TOP, PD_X1 - PD_X0, 22), wash='#A97E55', fill='#86603E', fillOp=60, ink=INK, sw=.9)
    if lineMark:
        G.c.drawLine(LINE_X, PD_TOP - 17, LINE_X, PD_TOP - 1, skia.Paint(AntiAlias=True, Color=skcol(LINE_PEN, .9), StrokeWidth=4))
    boilSeed('pdlegs')
    for lx in (PD_X0 + 24, PD_X1 - 24):
        inkLine([[lx, PD_TOP + 22], [lx, PD_FLOOR]], 1.6, '#6E737C', 'ink', 0)
    inkLine([[PD_X0 + 24, PD_TOP + 60], [PD_X1 - 24, PD_TOP + 60]], 1.0, '#6E737C', 'ink', 0)
    if items:
        items()


def deskBooks(x, n=3, key='dbk'):
    """a few books standing on the desk top (front view)"""
    cols = ['#5E8FC4', '#C9727F', '#E7C46A', '#7FB59A']
    for i in range(n):
        boilSeed(key + str(i))
        paint(rectPts(x + i * 26, PD_TOP - 18 - 90 - 10 * (i % 2), 24, 90 + 10 * (i % 2)), wash=cols[i % 4], ink=INK, sw=.6, lite=True)


def bookWall(k, key='bw'):
    """the wall of books she stacks on the line (front view): k 0..1 grows it"""
    cols = ['#5E8FC4', '#C9727F', '#E7C46A', '#7FB59A', '#A98BC9', '#E39A6A']
    n = int(clamp(k) * 9 + .999)
    y = PD_TOP - 18
    for i in range(n):
        h = 28 + 6 * hash1(i * 2.1)
        w = 150 + 26 * hash1(i * 3.3)
        dx = (hash1(i * 5.7) - .5) * 20
        land = clamp(k * 9 - i) if i == n - 1 else 1
        yy = y - h - (1 - easeOut(land)) * 60
        boilSeed(key + str(i))
        paint(rectPts(LINE_X - w / 2 + dx, yy, w, h), wash=cols[i % 6], fill=mixCol(cols[i % 6], INK, .3), fillOp=50, ink=INK, sw=.7)
        G.c.drawLine(LINE_X - w / 2 + dx + 8, yy + h * .5, LINE_X + w / 2 + dx - 8, yy + h * .5,
                     skia.Paint(AntiAlias=True, Color=skcol('#FBF8F0', .5), StrokeWidth=2))
        y = yy


def pastClass(t, era, people, items=None, light=1.0, cam_=(960, 560, 1.0), back=True):
    """people(t) draws the two of them seated (between the chair backs and the desk)"""
    cam(t, *cam_)
    backWall(t, era, light)
    if back:
        backRow(t)
    chairBack(P_HER, 'chH')
    chairBack(P_HIM, 'chM')
    chairSeat(P_HER, 'chH')
    chairSeat(P_HIM, 'chM')
    people(t)
    pastDesk(t, items)


# ================================================================ the school gate street
GATE_FLOOR = 860


def gateScene(t, mode='dusk', snow=0.0, leaves=0.0, lampOn=1.0, shopLit=1.0):
    """mode: dusk (autumn 2013), night (snow 2015), eve (snowy dusk 2026)"""
    sky = {'dusk': ['#F4B98A', '#C9A4C8', '#8E86B8'], 'night': ['#1B2140', '#2C3660', '#4A5584'],
           'eve': ['#5D6E98', '#8A98BC', '#C3CCE0']}[mode]
    gradRect(-1200, -900, W + 2400, 900 + GATE_FLOOR - 40, [sky[0], sky[1], sky[2]])
    if mode == 'dusk':
        glow(1500, 520, 520, '#FFD7A0', .5)
    # far buildings (silhouettes, no windows)
    for i in range(9):
        bx = -400 + i * 300
        bh = 220 + 160 * hash1(i * 3.3)
        flatRect(bx, GATE_FLOOR - 120 - bh, 260, bh + 40, mixCol(sky[1], '#3A3550', .35))
    # school wall + pillar with the name, the retractable gate
    boilSeed('swall')
    paint(rectPts(-1000, GATE_FLOOR - 260, 1300, 260), wash='#C9B79A', fill='#A8957A', fillOp=50, ink=INK, sw=.8)
    for i in range(10):
        G.c.drawLine(-1000 + i * 130, GATE_FLOOR - 260, -1000 + i * 130, GATE_FLOOR, skia.Paint(AntiAlias=True, Color=skcol('#8E7C62', .5), StrokeWidth=2))
    boilSeed('pillar')
    paint(rectPts(260, GATE_FLOOR - 470, 120, 470), wash='#D9CDB6', fill='#B8A88C', fillOp=50, ink=INK, sw=.9)
    paint(rectPts(278, GATE_FLOOR - 440, 84, 300), wash='#FBF8F0', ink=INK, sw=.6)
    for i, ch in enumerate('第二中学'):
        text(ch, 320, GATE_FLOOR - 404 + i * 70, 54, '#2E2A36', face=WENKAI, shadow=False)
    boilSeed('rgate')
    for i in range(9):
        gx = 390 + i * 26
        inkLine([[gx, GATE_FLOOR - 120], [gx + 26, GATE_FLOOR - 20]], .8, '#8A93A0', 'inkfine', 0)
        inkLine([[gx + 26, GATE_FLOOR - 120], [gx, GATE_FLOOR - 20]], .8, '#8A93A0', 'inkfine', 0)
    paint(rectPts(386, GATE_FLOOR - 130, 244, 14), wash='#9AA3AE', ink=INK, sw=.6)
    # tree behind the wall
    boilSeed('tree')
    inkLine([[60, GATE_FLOOR - 250], [40, GATE_FLOOR - 560], [-30, GATE_FLOOR - 720]], 4.0, '#5A4636', 'ink', .4)
    inkLine([[44, GATE_FLOOR - 520], [170, GATE_FLOOR - 690]], 2.4, '#5A4636', 'ink', .4)
    if mode == 'dusk':
        for i in range(14):
            a_ = i / 14 * TAU
            paint(ellPts(40 + math.cos(a_) * 150, GATE_FLOOR - 660 + math.sin(a_) * 90, 90, 64, 16), wash='#F2C14E', fill='#D9A12E',
                  fillOp=60, ink=INK if i % 3 == 0 else None, sw=.6, lite=True)
    # sidewalk
    flatRect(-1200, GATE_FLOOR, W + 2400, 700, {'dusk': '#B9A99A', 'night': '#5B6280', 'eve': '#A9B2C6'}[mode])
    for i in range(-6, 22):
        G.c.drawLine(i * 120, GATE_FLOOR, i * 120 - 60, GATE_FLOOR + 300, skia.Paint(AntiAlias=True, Color=skcol('#000000', .08), StrokeWidth=2))
    if mode in ('night', 'eve'):
        boilSeed('snowground')
        paint([[-1200, GATE_FLOOR - 6], [W + 1200, GATE_FLOOR - 6], [W + 1200, GATE_FLOOR + 700], [-1200, GATE_FLOOR + 700]],
              wash='#EEF2FA' if mode == 'eve' else '#C9D2EA', washOp=200, ink=None)
        paint(rectPts(-1000, GATE_FLOOR - 272, 1300, 16), wash='#F4F7FF', ink=None)
        paint(rectPts(254, GATE_FLOOR - 484, 132, 18), wash='#F4F7FF', ink=None)
    # the shop
    boilSeed('shop')
    paint(rectPts(1420, GATE_FLOOR - 420, 520, 420), wash='#E7D9C0', fill='#C9B597', fillOp=50, ink=INK, sw=.9)
    paint(rectPts(1460, GATE_FLOOR - 300, 440, 300), wash=mixCol('#5A4636', '#FFD58A', .55 * shopLit), ink=INK, sw=.7)
    for r in range(3):
        paint(rectPts(1480, GATE_FLOOR - 270 + r * 86, 400, 10), wash='#8A6A4C', ink=None)
        for j in range(7):
            col = ['#E39A6A', '#5E9BD6', '#F7D36E', '#C9727F', '#7FB59A'][(j + r) % 5]
            paint(rectPts(1494 + j * 54, GATE_FLOOR - 312 + r * 86, 40, 40), wash=col, ink=INK, sw=.4, lite=True)
    for j in range(8):
        paint([[1420 + j * 65, GATE_FLOOR - 360], [1485 + j * 65, GATE_FLOOR - 360], [1495 + j * 65, GATE_FLOOR - 300],
               [1430 + j * 65, GATE_FLOOR - 300]], wash='#D9534F' if j % 2 == 0 else '#FBF8F0', ink=INK, sw=.5)
    paint(rectPts(1460, GATE_FLOOR - 470, 440, 90), wash='#2E5FA8', ink=INK, sw=.9)
    text('小卖部', 1680, GATE_FLOOR - 425, 60, '#FFF7EA', face=WENKAI, stroke=INK, strokeW=6, shadow=False)
    if shopLit > .01:
        glow(1680, GATE_FLOOR - 150, 320, '#FFD58A', .35 * shopLit)
    # streetlamp
    boilSeed('lamp')
    inkLine([[960, GATE_FLOOR], [960, GATE_FLOOR - 640], [1000, GATE_FLOOR - 690], [1090, GATE_FLOOR - 690]], 3.2, '#3A3550', 'ink', .3)
    paint(rrPts(1050, GATE_FLOOR - 706, 90, 30, 8), wash='#4A4560', ink=INK, sw=.8)
    if lampOn > .01:
        paint([[1060, GATE_FLOOR - 676], [1130, GATE_FLOOR - 676], [1300, GATE_FLOOR], [890, GATE_FLOOR]], wash='#FFE9B0',
              washOp=int(50 * lampOn), ink=None)
        glow(1095, GATE_FLOOR - 680, 160, '#FFE9B0', .9 * lampOn)
    if snow > .01:
        snowfall(t, 7, 90, -300, -300, W + 300, GATE_FLOOR + 200, a=.9 * snow, r=6)
    if leaves > .01:
        for i in range(10):
            ph = frac(t * .18 + hash1(i * 2.3))
            x = -100 + hash1(i * 4.4) * 1400 + 120 * math.sin(t * 1.3 + i) + ph * 300
            y = -100 + ph * 1000
            boilSeed('lf%d' % i)
            paint(ellPts(x, y, 13, 9, 10, 0, t * 2 + i), wash='#F2C14E', washOp=int(255 * leaves), ink=INK, sw=.4, lite=True)


def footprints(x0, x1, y, n=10, a=.5, step=1):
    for i in range(n):
        x = lerp(x0, x1, i / max(1, n - 1))
        G.c.drawOval(skia.Rect.MakeXYWH(x - 12, y + (10 if i % 2 else -6), 24, 12), skia.Paint(AntiAlias=True, Color=skcol('#9AA6C2', a)))


# ================================================================ under the desk, the letter, the graduation photo
def underside(t, old=1.0, envK=1.0, tapes=2.0, light=None):
    """looking up at the underside of the desk top; the envelope taped under her half"""
    flatRect(-900, -900, W + 1800, H + 1800, mixCol('#6E5034', '#4A3828', old))
    boilSeed('usd')
    paint(rectPts(-200, -100, W + 400, H + 200), fill='#3E2E20', fillOp=50, bleed=.02, tex=.9, border=.2, ink=None)
    for i in range(16):
        y = -40 + i * 76
        G.c.drawLine(-200, y, W + 200, y + 10 * math.sin(i), skia.Paint(AntiAlias=True, Color=skcol('#2E2018', .35), StrokeWidth=3))
    for x in (120, 1800):
        paint(rectPts(x - 30, -100, 60, H + 200), wash='#6E737C', fill='#4E535C', fillOp=60, ink=INK, sw=.8)
    paint(rectPts(-100, 140, W + 200, 46), wash='#6E737C', fill='#4E535C', fillOp=60, ink=INK, sw=.8)
    for (gx, gy, r, col) in ((300, 760, 26, '#E39AB0'), (1500, 300, 20, '#9FD3E8'), (1620, 820, 16, '#C9C4B8')):
        paint(ellPts(gx, gy, r, r * .8, 12), wash=col, ink=INK, sw=.5, lite=True)
    if old > .5:
        for i in range(6):                                     # a cobweb in the corner
            a_ = i / 6 * math.pi / 2
            G.c.drawLine(1920, 1080, 1920 - math.cos(a_) * 300, 1080 - math.sin(a_) * 300, skia.Paint(AntiAlias=True, Color=skcol('#E8EDF4', .25), StrokeWidth=1.2))
    if envK > .01:
        envelope(820, 560, 520, -.05, '给方茴', old, key='uenv', a=envK)
        for i in range(2):
            k = clamp(tapes - i)
            if k > .01:
                push()
                translate(820 + (-240 if i == 0 else 240), 560 - 150 + (i * 300))
                rotate(-.6 if i == 0 else -.6)
                G.c.drawRect(skia.Rect.MakeXYWH(-70 * k, -20, 140 * k, 40), skia.Paint(AntiAlias=True, Color=skcol(mixCol('#F4F1E6', '#E6D7A8', old), .7)))
                pop()


def letterPaper(cx, cy, w, h, old=0.0, key='lp'):
    G.c.drawRect(skia.Rect.MakeXYWH(cx - w / 2 + 14, cy - h / 2 + 18, w, h), skia.Paint(AntiAlias=True, Color=skcol('#000000', .25)))
    boilSeed(key)
    col = mixCol('#FFF1F4', '#F1E6CF', old)
    paint(rectPts(cx - w / 2, cy - h / 2, w, h, 1), wash=col, fill=mixCol(col, INK, .08), fillOp=40, ink=INK, sw=.8)
    for i in range(7):
        y = cy - h / 2 + 110 + i * 78
        G.c.drawLine(cx - w / 2 + 50, y, cx + w / 2 - 50, y, skia.Paint(AntiAlias=True, Color=skcol('#F2A9BC', .55 - .25 * old), StrokeWidth=2))
    paint(heartPts(cx + w / 2 - 70, cy - h / 2 + 60, 22), wash=mixCol('#F2A9BC', '#D9B8A8', old), ink=INK, sw=.4, lite=True)


LETTER = [('方茴：', 0), ('过线是我故意的。', 1), ('欠你的，我想一直欠着。', 2), ('陈寻 2015.12', 3)]


def letterText(cx, cy, w, h, progs, old=0.0, hi=None):
    """progs: progress per line; hi: line index to highlight (reading)"""
    tip = None
    for (s, i), p in zip(LETTER, progs):
        size = 60 if i < 3 else 44
        y0 = cy - h / 2 + 110 + i * 78 - size * .95
        x0 = cx - w / 2 + 80 if i < 3 else cx + w / 2 - 80 - (len(s) - 5) * size * 1.06 - 5 * size * .56
        if hi is not None and i == hi and p > 0:
            G.c.drawRoundRect(skia.Rect.MakeXYWH(x0 - 16, y0 - 6, len(s) * size * 1.06 + 30, size * 1.25), 12, 12,
                              skia.Paint(AntiAlias=True, Color=skcol('#FFF2A8', .35)))
        if p > 0:
            tp = handLine(s, x0, y0, size, p, mixCol('#2B3266', '#4A4E70', old * .6))
            if 0 < p < 1:
                tip = tp
    return tip


def gradPhoto(t, cx=960, cy=520, w=1300, flashK=0.0):
    """the class photo, 2016.6: three rows; she at the far left of the front row, he at the far right of the back row"""
    h = w * .62
    G.c.drawRect(skia.Rect.MakeXYWH(cx - w / 2 + 20, cy - h / 2 + 26, w, h), skia.Paint(AntiAlias=True, Color=skcol('#000000', .35)))
    boilSeed('photoframe')
    paint(rectPts(cx - w / 2 - 30, cy - h / 2 - 30, w + 60, h + 60), wash='#FBF8F0', ink=INK, sw=1.0)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h))
    gradRect(cx - w / 2, cy - h / 2, w, h, ['#BFD8EE', '#E8F0E6'])
    paint(rectPts(cx - w / 2, cy + h * .05, w, h * .5), wash='#C9B79A', ink=None)
    for r in range(3):                                          # risers
        paint(rectPts(cx - w / 2, cy - h * .05 + r * 90, w, 18), wash='#A8957A', ink=None)
    paint(rectPts(cx - w * .36, cy - h / 2 + 30, w * .72, 74), wash='#C8324A', ink=INK, sw=.6)
    text('高三(2)班 毕业留念 2016.6', cx, cy - h / 2 + 67, 46, '#FFE36E', face=WENKAI, shadow=False)
    u = 15
    rows = [(cy - h * .05 - 6, 13, 'back'), (cy - h * .05 + 84, 13, 'mid'), (cy - h * .05 + 174, 12, 'front')]
    for ri, (gy, n, tag) in enumerate(rows):
        for j in range(n):
            x = cx - w / 2 + 120 + j * (w - 240) / (n - 1)
            if tag == 'front' and j == 0:
                teen('her', x, gy + 4 * u, u, dict(view='front', eyes='normal', mouth='smile', noShadow=True, boilKey='ph_her', aL=-.3, aR=-.3))
                continue
            if tag == 'back' and j == n - 1:
                teen('him', x, gy + 4 * u, u, dict(view='front', eyes='normal', mouth='smile', noShadow=True, boilKey='ph_him', aL=-.3, aR=-.3))
                continue
            g_ = GREYS[(j + ri * 3) % len(GREYS)]
            clawd(x, gy + 4 * u, u, dict(col=g_[0], dk=g_[1], lt=g_[2], view='front', eyes=['normal', 'happy'][(j + ri) % 2],
                                         mouth='smile', noShadow=True, boilKey='ph%d_%d' % (ri, j), lite=True, aL=-.3, aR=-.3))
    G.c.restore()
    if flashK > .01:
        flatRect(cx - w / 2, cy - h / 2, w, h, '#FFFFFF', flashK)
