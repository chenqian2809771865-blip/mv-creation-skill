# nm.py: 《你瞒我瞒》 props and sets — case-file folder, lip marks, phones, a world-space magnifier (lens can hold lip prints or
# an x-ray view), candle-lit restaurant, living-room loveseat, his room with the 疑心病 deerstalker shelf, the 「谈心室」 interrogation
# table, the little room inside her heart, the suspect line-up, cardboard box, photo booth and the photo-booth print.
# Logical canvas 1920x1080. No windows anywhere (house rule); text lives on paper, boards and stamps.
import math
from eng import *
import eng
from clawd import *
from props import *
from hl import deskLamp, deerHatAlone, WENKAI, wtext, mug
from sets2 import fairyLights, wallCalendar, wallClock, washi, coffeeRing, pencil, coupleSnap, pencilDoodle, fakeText
from props_chuanshao import spotBeam

PINK, PINKDK = '#EE9AAE', '#C0637B'
LIP, LIPDK = '#E8476E', '#B8324F'
MANILA, MANILADK = '#E2C38A', '#B8955A'
REDINK = '#D8394E'
BRASS = '#C99A2E'
GLASS = '#DDF2FF'


# ================================================================ small marks
def lips(x, y, s, rot=0.0, col=LIP, a=1.0, key='lip'):
    """a lipstick print, s = half width"""
    if a <= .02:
        return
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    up = [[-1.0, .05], [-.62, -.42], [-.28, -.5], [0, -.3], [.28, -.5], [.62, -.42], [1.0, .05], [0, .02]]
    lo = [[-1.0, .05], [-.5, .45], [0, .56], [.5, .45], [1.0, .05], [0, .12]]
    for P in (up, lo):
        paint([[px * s, py * s] for px, py in P], wash=col, washOp=int(235 * a), fill=mixCol(col, INK, .25), fillOp=int(60 * a),
              bleed=.08, ink=None, curv=.35)
    inkLine([[-.92 * s, .06 * s], [0, .1 * s], [.92 * s, .06 * s]], .8, mixCol(col, INK, .45), 'inkfine', .3)
    for i in range(4):
        xx = (-.6 + .4 * i) * s
        inkLine([[xx, .18 * s], [xx + .04 * s, .38 * s]], .5, mixCol(col, '#FFFFFF', .35), 'inkfine', 0)
    pop()


def heartP(x, y, r, col=C['heart'], dk=None, a=1.0, key='hp'):
    boilSeed(key)
    paint(heartPts(x, y, r, 26), wash=col, washOp=int(255 * a), fill=dk or mixCol(col, INK, .25), fillOp=int(50 * a), ink=INK if a > .5 else None, sw=.8)


def postit(x, y, w, rot, txt='', col='#FBE7A1', size=None, key='pi', tcol='#5A4A6A', face=None, k=1.0):
    p = backOut(k)
    if p < .02:
        return
    push()
    translate(x, y)
    rotate(rot)
    scale(p)
    boilSeed(key)
    paint(rectPts(-w / 2 + 4, -w / 2 + 6, w, w), wash=INK, washOp=40, ink=None)
    paint(rectPts(-w / 2, -w / 2, w, w), wash=col, fill=mixCol(col, INK, .1), fillOp=40, ink=INK, sw=.7)
    paint(rectPts(-w / 2, -w / 2, w, w * .16), wash=mixCol(col, INK, .08), ink=None)
    if txt:
        lines = txt.split('\n')
        sz = size or w * .22
        for i, ln in enumerate(lines):
            text(ln, 0, (i - (len(lines) - 1) / 2) * sz * 1.2 + w * .06, sz, tcol, face=face or KUAILE, shadow=False)
    pop()


def sweatDrop(x, y, s, a=1.0, key='sd'):
    boilSeed(key)
    paint([[x, y - 1.3 * s], [x + .75 * s, y + .2 * s], [x, y + .8 * s], [x - .75 * s, y + .2 * s]], wash='#BFE6FA', washOp=int(240 * a), ink=INK, sw=.6, curv=.6)


# ================================================================ phones
def phoneP(x, y, s, rot=0.0, lit=1.0, case=PINK, faceDown=False, key='ph', heart=0.0, msg=None):
    """a phone standing for (x, y) = centre, s = height"""
    w, h = s * .52, s
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rrPts(-w / 2, -h / 2, w, h, w * .18), wash=case, fill=mixCol(case, INK, .3), fillOp=60, ink=INK, sw=1.0)
    if faceDown:
        paint(ellPts(0, -h * .28, w * .14, w * .14, 12), wash=mixCol(case, INK, .45), ink=None)
        paint(heartPts(0, h * .1, w * .16, 16), wash='#FFFFFF', washOp=170, ink=None)
    else:
        scr = mixCol('#1E2235', '#CFEFFF', lit)
        paint(rrPts(-w / 2 + w * .1, -h / 2 + w * .14, w * .8, h - w * .28, w * .08), wash=scr, ink=None)
        if lit > .05:
            for i in range(3):
                G.c.drawRoundRect(skia.Rect.MakeXYWH(-w * .3, -h * .3 + i * h * .14, w * (.6 - .15 * (i % 2)), h * .06), 3, 3,
                                  skia.Paint(AntiAlias=True, Color=skcol('#8FB5D6', .7 * lit)))
        if heart > .02:
            heartP(0, h * .2, w * .22 * backOut(heart), key=key + 'h')
    pop()
    if lit > .05 and not faceDown:
        glow(x, y, s * 1.2, '#BDEBFF', .35 * lit)


def phoneHookP(case=PINK, lit=1.0):
    def h(u, sw):
        paint(rrPts(-.2 * u, -1.2 * u, 1.3 * u, 2.2 * u, .28 * u), wash=case, ink=INK, sw=sw * .7)
        paint(rrPts(-.06 * u, -1.0 * u, 1.02 * u, 1.75 * u, .15 * u), wash=mixCol('#1E2235', '#CFEFFF', lit), ink=None)
        if lit > .05:
            glow(.45 * u, -.15 * u, 2.6 * u, '#BDEBFF', .45 * lit)
    return h


# ================================================================ magnifier (world space: handle from the hand to the lens)
def magnifierW(hx, hy, ang, r, L=None, lips_=0, lipsK=None, inside=None, glint=0.0, key='mg', pink=0.0):
    """hand at (hx, hy); handle points along ang; returns the lens centre. lips_ = number of lip prints on the glass,
    lipsK = pop-in for each, inside(cx, cy, r) draws a view clipped to the glass (x-ray etc.)"""
    L = L or r * 1.15
    ca, sa = math.cos(ang), math.sin(ang)
    cx, cy = hx + ca * (L + r), hy + sa * (L + r)
    boilSeed(key)
    # handle
    push()
    translate(hx, hy)
    rotate(ang)
    paint(rrPts(-r * .18, -r * .13, L + r * .1, r * .26, r * .1), wash='#7A4E33', fill='#5A3622', fillOp=60, ink=INK, sw=1.0)
    paint(rectPts(L - r * .12, -r * .17, r * .2, r * .34), wash=BRASS, ink=INK, sw=.8)
    pop()
    # glass
    if inside is not None:
        G.c.save()
        cp = skia.Path()
        cp.addCircle(cx, cy, r)
        G.c.clipPath(cp, skia.ClipOp.kIntersect, True)
        inside(cx, cy, r)
        G.c.restore()
    else:
        paint(ellPts(cx, cy, r, r, 36), wash=GLASS, washOp=110, ink=None)
    if pink > 0:
        paint(ellPts(cx, cy, r, r, 36), wash='#F7A1B6', washOp=int(170 * pink), ink=None)
    if lips_:
        G.c.save()
        cp = skia.Path()
        cp.addCircle(cx, cy, r)
        G.c.clipPath(cp, skia.ClipOp.kIntersect, True)
        spots = [(-.3, -.25, -.3), (.32, .1, .25), (-.12, .42, .05), (.1, -.5, .4), (.45, -.35, -.2)]
        for i in range(lips_):
            k = 1 if lipsK is None else lipsK[i]
            if k <= 0:
                continue
            sx, sy, rr = spots[i % len(spots)]
            sc = lerp(1.6, 1.0, easeOut(clamp(k * 1.4)))
            lips(cx + sx * r, cy + sy * r, r * .36 * sc, rr, a=clamp(k * 3), key=f'{key}l{i}')
        G.c.restore()
    paint(ellPts(cx - r * .35, cy - r * .42, r * .26, r * .12, 10, 0, -.6), wash='#FFFFFF', washOp=190, ink=None)
    paint(ellPts(cx, cy, r, r, 36), ink=BRASS, sw=max(2.2, r * .045))
    paint(ellPts(cx, cy, r * 1.06, r * 1.06, 36), ink=INK, sw=1.0)
    if glint > .02:
        sparkle(cx - r * .45, cy - r * .5, r * .45 * glint, '#FFFFFF')
        glow(cx, cy, r * 1.8, '#FFF6CC', .45 * glint)
    return cx, cy


# ================================================================ case-file folder (desk top-down)
def deskWood(t, lampK=1.0, key='dw'):
    gradRect(-300, -300, W + 600, H + 600, ['#6B4A3A', '#4E3428'])
    for i in range(-4, 30):
        y = i * 46 + 10 * math.sin(i * 1.7)
        G.c.drawLine(-300, y, W + 300, y + 18, skia.Paint(AntiAlias=True, Color=skcol('#3A2418', .22), StrokeWidth=2))
    for i in range(6):
        x = 200 + i * 330
        G.c.drawOval(skia.Rect.MakeXYWH(x, 140 + 120 * hash1(i), 90, 24), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style,
                     StrokeWidth=1.6, Color=skcol('#2E1B12', .25)))
    if lampK > 0:
        glow(1500, 260, 1100, '#FFC978', .32 * lampK)


def dossier(x, y, w, h, rot=0.0, key='dos', label='档案 No.0520', cover=1.0, coverDY=0.0, inside=None):
    """manila folder lying on the desk; (x, y) = centre. cover 1 = closed; inside() draws the papers under the cover"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-w / 2 + 10, -h / 2 + 14, w, h), wash=INK, washOp=60, ink=None, bleed=.2)
    paint(rectPts(-w / 2, -h / 2, w, h), wash=mixCol(MANILA, INK, .08), ink=INK, sw=1.0)
    if inside:
        inside(w, h)
    if cover > 0:
        ch = h * cover
        y0 = -h / 2 + coverDY
        boilSeed(key + 'c')
        paint(rectPts(-w / 2, y0, w, ch), wash=MANILA, fill=MANILADK, fillOp=50, ink=INK, sw=1.1)
        paint([[-w / 2 + w * .06, y0], [-w / 2 + w * .1, y0 - h * .07], [-w / 2 + w * .42, y0 - h * .07], [-w / 2 + w * .46, y0]],
              wash=MANILA, ink=INK, sw=1.0)
        text(label, -w / 2 + w * .26, y0 - h * .035, h * .042, '#6A4A2A', shadow=False)
        if cover > .6:
            # string-tie buttons
            for bx in (w * .32, w * .32):
                paint(ellPts(bx, y0 + ch - h * .1, h * .035, h * .035, 14), wash='#B98352', ink=INK, sw=.7)
            inkLine([[w * .32, y0 + ch - h * .1], [w * .25, y0 + ch - h * .02], [w * .36, y0 + ch + h * .05]], 1.4, '#F3EBDC', 'ink', .5)
            # printed form lines
            for i in range(3):
                yy = y0 + h * (.68 + i * .07)
                G.c.drawLine(-w * .38, yy, -w * .02, yy, skia.Paint(AntiAlias=True, Color=skcol('#8A6A40', .55), StrokeWidth=1.6))
            text('嫌疑人：', -w * .33, y0 + h * .655, h * .04, '#6A4A2A', align='left', shadow=False)
    pop()


def polaroidW(x, y, w, rot=0.0, key='pol', draw=None, label=None):
    """white polaroid; draw(px, py, pw, ph) paints the picture area"""
    h = w * 1.16
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-w / 2 + 6, -h / 2 + 8, w, h), wash=INK, washOp=50, ink=None)
    paint(rectPts(-w / 2, -h / 2, w, h), wash='#FFFDF6', ink=INK, sw=.9)
    pw, ph = w * .86, w * .8
    if draw:
        G.c.save()
        G.c.clipRect(skia.Rect.MakeXYWH(-pw / 2, -h / 2 + w * .07, pw, ph))
        draw(-pw / 2, -h / 2 + w * .07, pw, ph)
        G.c.restore()
    else:
        coupleSnap(-pw / 2, -h / 2 + w * .07, pw, ph, night=False)
    if label:
        wtext(label, 0, h / 2 - w * .12, w * .09, '#7A6A80')
    pop()


def paperclip(x, y, s, rot=0.0, col='#9AA3B8'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed('pc')
    P = [[0, 1.8], [0, -1.4], [.35, -1.8], [.7, -1.4], [.7, 1.4], [.35, 1.7], [.12, 1.4], [.12, -.8]]
    inkLine([[a * s, b * s] for a, b in P], 2.2, col, 'ink', .6)
    pop()


# ================================================================ restaurant (front composition, no windows)
def restaurantBack(t, dim=0.0, key='rb'):
    wallA, wallB = mixCol('#E9B7A0', '#2A2440', dim * .75), mixCol('#D99A88', '#221D36', dim * .75)
    gradRect(-300, -300, W + 600, 1100, [wallA, wallB])
    for i in range(-3, 26):
        G.c.drawRect(skia.Rect.MakeXYWH(i * 92, -300, 40, 1100), skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .06 * (1 - dim))))
    # wainscot
    boilSeed(key + 'ws')
    paint(rectPts(-300, 640, W + 600, 500), wash=mixCol('#8E5A4A', '#1A1528', dim * .7), fill=mixCol('#6E4034', '#120E20', dim * .7), fillOp=60, ink=INK, sw=1.0)
    for i in range(-2, 22):
        xx = i * 120 + 30
        paint(rectPts(xx, 680, 90, 200), ink=mixCol('#5A3428', '#0E0A18', dim), sw=.8, lite=True)
    # framed pictures
    for j, (fx, fy, fw, fh, kind) in enumerate([(300, 230, 200, 150, 'heart'), (1620, 220, 170, 210, 'flower')]):
        boilSeed(key + f'f{j}')
        paint(rectPts(fx - fw / 2 - 14, fy - fh / 2 - 14, fw + 28, fh + 28), wash=mixCol('#B98352', '#3A2B3F', dim * .7), ink=INK, sw=1.0)
        paint(rectPts(fx - fw / 2, fy - fh / 2, fw, fh), wash=mixCol('#FFF5E2', '#3A3550', dim * .7), ink=INK, sw=.7)
        if kind == 'heart':
            heartP(fx, fy + 6, 46, col=mixCol('#E8476E', '#4A3550', dim * .6), key=key + 'fh')
        else:
            for k in range(5):
                a = k / 5 * TAU
                paint(ellPts(fx + math.cos(a) * 22, fy - 20 + math.sin(a) * 22, 18, 18, 10), wash=mixCol('#F59AB0', '#4A3550', dim * .6), ink=None)
            paint(ellPts(fx, fy - 20, 12, 12, 10), wash=mixCol('#F2C53D', '#4A3550', dim * .6), ink=None)
            inkLine([[fx, fy], [fx, fy + 80]], 2.5, '#5E9E5A', 'ink', .3)
    # menu chalkboard
    boilSeed(key + 'mb')
    paint(rectPts(1180, 150, 300, 230), wash='#A07850', ink=INK, sw=1.0)
    paint(rectPts(1196, 166, 268, 198), wash=mixCol('#2F3B36', '#14181A', dim * .5), ink=None)
    wtext('今日推荐', 1330, 200, 34, mixCol('#FFF5E2', '#6A6A7A', dim * .6))
    wtext('情侣套餐 ♡ 2位', 1330, 252, 28, mixCol('#F7A1B6', '#6A5A6A', dim * .6))
    wtext('意面 · 红酒 · 蜡烛', 1330, 296, 24, mixCol('#E8E1D2', '#5A5A6A', dim * .6))
    inkLine([[1220, 330], [1440, 326]], 1.2, mixCol('#E8E1D2', '#5A5A6A', dim * .6), 'dry', .2)
    # wall clock + string lights
    if dim < .9:
        wallClock(860, 190, 70, t, key=key + 'clk')
    fairyLights(t, -100, W + 100, 70, sag=60, n=22, key=key + 'fl', a=1 - dim * .8)
    # potted plant on the left
    boilSeed(key + 'pl')
    paint([[60, 640], [180, 640], [165, 760], [75, 760]], wash=mixCol('#C97B5A', '#2A2034', dim * .7), ink=INK, sw=.9)
    for i in range(7):
        a = -math.pi / 2 + (i - 3) * .35
        paint(ellPts(120 + math.cos(a) * 90, 600 + math.sin(a) * 110, 30, 62, 14, 0, a + math.pi / 2),
              wash=mixCol('#7CC36B', '#1E3A30', dim * .7), fill=mixCol('#4E9A4A', '#16281E', dim * .7), fillOp=60, ink=INK, sw=.6)


def candle(x, y, s, t, on=1.0, key='cdl', puffAge=None):
    """(x, y) = bottom of the holder; s ~ candle height"""
    boilSeed(key)
    paint(ellPts(x, y - s * .05, s * .38, s * .1, 18), wash=BRASS, ink=INK, sw=.8)
    paint(rectPts(x - s * .06, y - s * .3, s * .12, s * .26), wash=BRASS, ink=INK, sw=.7)
    paint(rectPts(x - s * .13, y - s * 1.05, s * .26, s * .76), wash='#FFF6E4', fill='#EADBC0', fillOp=60, ink=INK, sw=.8)
    inkLine([[x, y - s * 1.05], [x, y - s * 1.13]], 1.2, INK, 'ink', 0)
    if on > .02:
        fl = 1 + .12 * math.sin(t * 23) + .08 * math.sin(t * 37)
        fy = y - s * 1.13
        glow(x, fy - s * .1, s * 3.2 * on, '#FFC976', .55 * on)
        fh = s * .42 * fl * on
        paint([[x, fy - fh], [x + s * .12 * on, fy - fh * .35], [x, fy + s * .02], [x - s * .12 * on, fy - fh * .35]], wash='#FFC23D', ink=None, curv=.6)
        paint([[x, fy - fh * .62], [x + s * .06 * on, fy - fh * .25], [x, fy], [x - s * .06 * on, fy - fh * .25]], wash='#FFF4C8', ink=None, curv=.6)
    if puffAge is not None and 0 < puffAge < 2.0:
        for j in range(3):
            a_ = puffAge - j * .12
            if a_ <= 0:
                continue
            yy = y - s * 1.2 - a_ * s * 1.4
            xx = x + math.sin(a_ * 4 + j) * s * .3
            r = s * (.1 + a_ * .22)
            paint(ellPts(xx, yy, r, r * .8, 14), wash='#C9CCDA', washOp=int(170 * max(0, 1 - a_ / 2)), ink=None)


def wineGlass(x, y, s, fill=.5, col='#B8324F', key='wg', tilt=0.0):
    push()
    translate(x, y)
    rotate(tilt)
    boilSeed(key)
    paint(ellPts(0, 0, s * .32, s * .07, 16), wash='#EAF4FA', washOp=170, ink=INK, sw=.6)
    inkLine([[0, 0], [0, -s * .55]], 1.4, INK, 'ink', 0)
    bowl = [[-s * .3, -s * 1.15], [s * .3, -s * 1.15], [s * .24, -s * .7], [0, -s * .55], [-s * .24, -s * .7]]
    if fill > 0:
        paint([[-s * .27, -s * (.7 + .4 * fill)], [s * .27, -s * (.7 + .4 * fill)], [s * .22, -s * .72], [0, -s * .58], [-s * .22, -s * .72]],
              wash=col, washOp=210, ink=None, curv=.4)
    paint(bowl, wash='#EAF4FA', washOp=70, ink=INK, sw=.8, curv=.4)
    pop()


def pastaPlate(x, y, s, key='pp'):
    boilSeed(key)
    paint(ellPts(x, y, s, s * .3, 24), wash='#FFFDF6', ink=INK, sw=.8)
    paint(ellPts(x, y - s * .06, s * .55, s * .17, 20), wash='#F2C66A', fill='#D9A040', fillOp=60, ink=None)
    for i in range(5):
        a = i * 1.3
        inkLine([[x - s * .4 + i * s * .2, y - s * .1], [x - s * .3 + i * s * .18 + math.cos(a) * s * .1, y - s * .2]], 1.0, '#C98A30', 'inkfine', .5)
    paint(ellPts(x + s * .1, y - s * .14, s * .1, s * .05, 10), wash='#D8394E', ink=None)


def diningTable(t, top=760, cx=960, w=1240, cloth='#FFF6E8', key='dt', props_=True, candleOn=1.0, puffAge=None, dim=0.0,
                glassTilt=(0.0, 0.0), glassXY=None, plates=True, vase=True):
    """front edge of a long tablecloth; things on the table sit on y≈top; returns nothing"""
    boilSeed(key)
    cl = mixCol(cloth, '#2A2440', dim * .7)
    # table top surface seen slightly from above
    paint([[cx - w / 2 + 40, top - 70], [cx + w / 2 - 40, top - 70], [cx + w / 2, top], [cx - w / 2, top]], wash=cl, ink=INK, sw=.9)
    # drape
    paint([[cx - w / 2, top], [cx + w / 2, top], [cx + w / 2 + 10, top + 330], [cx - w / 2 - 10, top + 330]], wash=cl, fill=mixCol(cl, INK, .12), fillOp=50, ink=INK, sw=1.0)
    for i in range(14):
        xx = cx - w / 2 + 20 + i * (w - 40) / 13
        G.c.drawLine(xx, top + 10, xx + (i - 6.5) * 2, top + 320, skia.Paint(AntiAlias=True, Color=skcol(INK, .06), StrokeWidth=3))
    # red check border
    for j in range(2):
        yy = top + 40 + j * 46
        for i in range(30):
            xx = cx - w / 2 + i * w / 30
            if (i + j) % 2 == 0:
                G.c.drawRect(skia.Rect.MakeXYWH(xx, yy, w / 30, 40), skia.Paint(AntiAlias=True, Color=skcol(mixCol('#D8394E', '#3A2440', dim * .6), .55)))
    if not props_:
        return
    if plates:
        pastaPlate(cx - 330, top - 34, 110, key=key + 'p1')
        pastaPlate(cx + 330, top - 34, 110, key=key + 'p2')
    gx = glassXY or ((cx - 150, top - 30), (cx + 150, top - 30))
    wineGlass(gx[0][0], gx[0][1], 120, key=key + 'g1', tilt=glassTilt[0])
    wineGlass(gx[1][0], gx[1][1], 120, key=key + 'g2', tilt=glassTilt[1])
    if vase:
        boilSeed(key + 'v')
        paint([[cx + 40, top - 30], [cx + 70, top - 30], [cx + 78, top - 100], [cx + 32, top - 100]], wash='#9CD0EE', washOp=170, ink=INK, sw=.7)
        inkLine([[cx + 55, top - 100], [cx + 62, top - 160]], 1.6, '#5E9E5A', 'ink', .3)
        heartP(cx + 62, top - 172, 16, col='#E8476E', key=key + 'rose')
    candle(cx - 40, top - 30, 100, t, on=candleOn, key=key + 'c', puffAge=puffAge)


# ================================================================ living room + loveseat
def livingBack(t, key='lv'):
    gradRect(-300, -300, W + 600, 1100, ['#F5D9B8', '#EFC9A4'])
    for i in range(-3, 40):
        for j in range(0, 14):
            if (i + j) % 2 == 0:
                G.c.drawCircle(i * 60 + (30 if j % 2 else 0), j * 70, 4, skia.Paint(AntiAlias=True, Color=skcol('#E2A880', .5)))
    flatRect(-300, 820, W + 600, 400, '#B98352')
    for i in range(-2, 24):
        G.c.drawLine(i * 110, 820, i * 110 - 60, 1100, skia.Paint(AntiAlias=True, Color=skcol('#8A5A36', .35), StrokeWidth=2))
    inkLine([[-300, 820], [W + 300, 820]], 1.0, INK, 'ink', 0)
    # rug
    boilSeed(key + 'rug')
    paint(ellPts(960, 930, 620, 80, 40), wash='#E27A92', fill='#B85A72', fillOp=50, ink=INK, sw=.9)
    paint(ellPts(960, 930, 520, 58, 40), ink='#FFF5E2', sw=1.2)
    fairyLights(t, 100, 1820, 90, sag=70, n=20, key=key + 'fl')
    wallCalendar(260, 300, key=key + 'cal')
    # floor lamp right
    boilSeed(key + 'fl2')
    inkLine([[1700, 820], [1700, 380]], 3.0, INK, 'ink', 0)
    paint([[1610, 380], [1790, 380], [1750, 260], [1650, 260]], wash='#FBE7A1', fill='#F2C53D', fillOp=60, ink=INK, sw=.9)
    glow(1700, 360, 360, '#FFE2A0', .45)
    paint(ellPts(1700, 822, 60, 12, 16), wash=INK, ink=None)
    # little framed photo string above the sofa
    for j in range(3):
        px = 760 + j * 200
        boilSeed(key + f'ph{j}')
        paint(rectPts(px - 60, 250 + 12 * math.sin(j * 2), 120, 140), wash='#FFFDF6', ink=INK, sw=.8)
        paint(rectPts(px - 50, 262 + 12 * math.sin(j * 2), 100, 96), wash=['#BFE3F5', '#F7C6D2', '#CDEFE0'][j], ink=None)
        heartP(px, 310 + 12 * math.sin(j * 2), 18, col=['#E8476E', '#D97757', '#E8476E'][j], key=key + f'h{j}')


def loveseat(x, y, w, col='#7FB8B0', key='ls'):
    """front-facing two-seater; (x, y) = floor centre. Draws the back and the seat cushion; returns the seat top y.
    Seat people with sets2.seat() after this (legs hang in front of the cushion), then loveseatArms() on top."""
    dk = mixCol(col, INK, .3)
    st = y - 150
    boilSeed(key)
    paint(rrPts(x - w / 2, st - 300, w, 330, 60), wash=col, fill=dk, fillOp=50, ink=INK, sw=1.2)
    for sx in (-1, 1):
        paint(rrPts(x + sx * w / 4 - w / 4 + 20, st - 270, w / 2 - 40, 250, 40), wash=mixCol(col, '#FFFFFF', .12), ink=INK, sw=.8, lite=True)
    boilSeed(key + 'f')
    paint(rrPts(x - w / 2 - 10, st - 14, w + 20, 134, 30), wash=col, fill=dk, fillOp=70, ink=INK, sw=1.2)
    inkLine([[x, st - 10], [x, st + 30]], .8, dk, 'inkfine', 0)
    for sx in (-1, 1):
        paint(rectPts(x + sx * (w / 2 - 40) - 14, y - 32, 28, 32), wash='#8A5A36', ink=INK, sw=.8)
    return st


def loveseatArms(x, y, w, col='#7FB8B0', key='ls'):
    dk = mixCol(col, INK, .3)
    st = y - 150
    boilSeed(key + 'a')
    for sx in (-1, 1):
        paint(rrPts(x + sx * (w / 2 + 10) - 55, st - 110, 110, 240, 45), wash=mixCol(col, '#FFFFFF', .08), fill=dk, fillOp=60, ink=INK, sw=1.1)


def cocoaTable(t, x, y, key='ct'):
    boilSeed(key)
    paint(rrPts(x - 170, y - 20, 340, 36, 12), wash='#C98B5A', ink=INK, sw=.9)
    for sx in (-1, 1):
        paint(rectPts(x + sx * 130 - 10, y + 16, 20, 70), wash='#8A5A36', ink=INK, sw=.8)
    mug(x - 70, y - 20, .9, key=key + 'm1', col='#F7C6D2', steam=1.0, t=t)
    mug(x + 70, y - 20, .9, key=key + 'm2', col='#F2A283', steam=1.0, t=t)


# ================================================================ his room (deep blue night, no window)
SHELF = (1330, 430)        # shelf top centre


def hisRoomBack(t, hat=True, mag=True, glint=0.0, key='hr', boxShelf=False):
    gradRect(-300, -300, W + 600, 1100, ['#22394F', '#2F4A66'])
    for i in range(-3, 30):
        G.c.drawRect(skia.Rect.MakeXYWH(i * 78, -300, 30, 1100), skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .035)))
    flatRect(-300, 840, W + 600, 400, '#3A3F5E')
    for i in range(-2, 24):
        G.c.drawLine(i * 120, 840, i * 120 - 80, 1100, skia.Paint(AntiAlias=True, Color=skcol('#262A44', .5), StrokeWidth=2))
    inkLine([[-300, 840], [W + 300, 840]], 1.0, INK, 'ink', 0)
    # warm lamp light pool from the desk lamp on the left
    glow(330, 560, 700, '#FFC976', .32)
    # desk + lamp left
    boilSeed(key + 'dk')
    paint(rectPts(80, 640, 520, 40), wash='#8A5A3C', ink=INK, sw=1.0)
    for sx in (110, 550):
        paint(rectPts(sx, 680, 26, 160), wash='#5E3A27', ink=INK, sw=.8)
    deskLamp(200, 640, 1.2, 1.0, key=key + 'l')
    mug(470, 640, .9, key=key + 'mg', col='#9CD0EE')
    # framed photo of the two on the desk
    boilSeed(key + 'pf')
    paint(rectPts(300, 520, 120, 120), wash='#B98352', ink=INK, sw=.8)
    coupleSnap(312, 532, 96, 96, night=True)
    # wall: calendar + clock
    wallCalendar(560, 240, key=key + 'cal')
    wallClock(880, 200, 62, t, key=key + 'clk')
    # shelf on the right with the deerstalker and magnifier from 疑心病
    sx, sy = SHELF
    boilSeed(key + 'sh')
    paint(rectPts(sx - 230, sy, 460, 26), wash='#8A5A3C', ink=INK, sw=.9)
    for bx in (sx - 180, sx + 180):
        paint([[bx - 10, sy + 26], [bx + 10, sy + 26], [bx, sy + 70]], wash='#5E3A27', ink=INK, sw=.7)
    # books on the shelf
    for j, (bw, bh, col) in enumerate([(34, 120, '#D8394E'), (28, 100, '#3A9C98'), (40, 130, '#E8AA38')]):
        bx = sx - 210 + j * 44
        paint(rectPts(bx, sy - bh, bw, bh), wash=col, ink=INK, sw=.7, lite=True)
    if boxShelf:
        pass
    if glint > 0:
        glow(sx + 20, sy - 60, 320, '#FFF0B0', .6 * glint)
        spotBeam(sx + 20, -100, sy, 120, 300, '#FFF2C4', .18 * glint)
    if hat:
        deerHatAlone(sx + 20, sy - 2, 13, key=key + 'hat')
    if mag:
        magnifierW(sx + 230, sy - 18, math.pi, 46, key=key + 'mg2')
    if glint > 0:
        sparkle(sx - 30, sy - 90, 30 * glint, '#FFFFFF')
        sparkle(sx + 90, sy - 70, 20 * glint, '#FFFFFF')
    # bed corner on the right edge
    boilSeed(key + 'bed')
    paint(rrPts(1640, 640, 500, 220, 30), wash='#8E86D8', fill='#6A60B8', fillOp=60, ink=INK, sw=1.0)
    paint(rrPts(1700, 590, 200, 80, 30), wash='#F3EBDC', ink=INK, sw=.8)


def cardBox(x, y, s, lidK=0.0, tape=0.0, key='cb', front=True, back=True):
    """cardboard box, (x, y) = bottom centre, s = width. lidK 0 open -> 1 shut. back/front drawn separately so things fall inside"""
    w, h = s, s * .62
    boilSeed(key)
    if back:
        paint([[x - w / 2, y - h], [x + w / 2, y - h], [x + w / 2 - w * .06, y - h - w * .16], [x - w / 2 + w * .06, y - h - w * .16]],
              wash='#A87B52', ink=INK, sw=.9)
        if lidK < .99:
            # open flaps standing up
            fl = (1 - lidK)
            for sx in (-1, 1):
                paint([[x + sx * w / 2, y - h], [x + sx * w / 2 + sx * w * .28 * fl, y - h - w * .32 * fl], [x, y - h - w * .32 * fl - w * .02],
                       [x, y - h]], wash='#C99A6B', ink=INK, sw=.8)
    if front:
        paint(rectPts(x - w / 2, y - h, w, h), wash='#C99A6B', fill='#A87B52', fillOp=60, ink=INK, sw=1.0)
        if lidK > .5:
            paint([[x - w / 2, y - h], [x + w / 2, y - h], [x + w / 2 - w * .06, y - h - w * .16], [x - w / 2 + w * .06, y - h - w * .16]],
                  wash='#D9AE7E', ink=INK, sw=.9)
            inkLine([[x, y - h - w * .16], [x, y - h]], .8, INK, 'inkfine', 0)
        text('杂物', x, y - h * .5, s * .14, '#7A5434', shadow=False)
        if tape > 0:
            for sgn in (-1, 1):
                p = clamp(tape * 1.4 - (0 if sgn < 0 else .4))
                if p > 0:
                    push()
                    translate(x, y - h * .5)
                    rotate(sgn * .5)
                    paint(rectPts(-w * .45 * p, -s * .05, w * .9 * p, s * .1), wash='#F2DD8A', washOp=230, ink=INK, sw=.6)
                    pop()


# ================================================================ 谈心室 interrogation table
def hangingLamp(x, y, on=1.0, swing=0.0, key='hl'):
    push()
    translate(x, -40)
    rotate(swing)
    boilSeed(key)
    inkLine([[0, 0], [0, y + 40 - 60]], 2.0, INK, 'ink', 0)
    yy = y + 40
    paint([[-110, yy], [110, yy], [50, yy - 80], [-50, yy - 80]], wash='#3A5A6A', fill='#24404E', fillOp=60, ink=INK, sw=1.0)
    paint(ellPts(0, yy, 60, 16, 18), wash=mixCol('#5A566E', '#FFF6CC', on), ink=INK, sw=.8)
    pop()
    if on > .02:
        lx = x + math.sin(swing) * (y + 40)
        glow(lx, y + 60, 260, '#FFF0B0', .9 * on)


def interroBack(t, lampK=1.0, swing=0.0, key='ib'):
    d = 1 - lampK * .55
    gradRect(-300, -300, W + 600, 1100, [mixCol('#5B6378', '#16182A', d), mixCol('#454B60', '#101220', d)])
    for i in range(-3, 30):
        G.c.drawRect(skia.Rect.MakeXYWH(-300, i * 60, W + 600, 3), skia.Paint(AntiAlias=True, Color=skcol('#000000', .08)))
    # sign + clock + filing cabinet
    boilSeed(key + 'sg')
    paint(rrPts(760, 90, 400, 90, 14), wash=mixCol('#FFF5E2', '#3A3550', d * .8), ink=INK, sw=1.0)
    text('谈 心 室', 960, 135, 54, mixCol(REDINK, '#4A3550', d * .7), shadow=False)
    wallClock(1640, 200, 60, t, key=key + 'clk')
    boilSeed(key + 'fc')
    paint(rectPts(1560, 430, 220, 420), wash=mixCol('#8A93B8', '#2A2D44', d), ink=INK, sw=1.0)
    for j in range(3):
        paint(rectPts(1576, 450 + j * 132, 188, 116), wash=mixCol('#9CA6C8', '#30344E', d), ink=INK, sw=.7, lite=True)
        paint(rrPts(1640, 495 + j * 132, 60, 18, 8), wash=mixCol('#C9CDD8', '#40445E', d), ink=INK, sw=.6)
    # a cork board with pinned clues on the left
    boilSeed(key + 'cb')
    paint(rectPts(140, 230, 360, 260), wash=mixCol('#C9965E', '#3A2B2A', d), ink=INK, sw=1.0)
    for j, (px, py) in enumerate([(200, 290), (330, 280), (430, 350), (250, 410)]):
        postit(px + 20, py + 20, 70, (j - 1.5) * .12, '', col=['#FBE7A1', '#F7C6D2', '#CDEFE0', '#BFE3F5'][j], key=key + f'p{j}')
    inkLine([[220, 300], [350, 290], [450, 360], [270, 420]], 1.6, REDINK, 'ink', .4)
    flatRect(-300, 860, W + 600, 400, mixCol('#3A3F52', '#0E1020', d))
    inkLine([[-300, 860], [W + 300, 860]], 1.0, INK, 'ink', 0)


def interroTable(top=780, cx=960, w=1100, key='it'):
    boilSeed(key)
    paint([[cx - w / 2 + 50, top - 60], [cx + w / 2 - 50, top - 60], [cx + w / 2, top], [cx - w / 2, top]], wash='#9A8C7A', ink=INK, sw=1.0)
    paint(rectPts(cx - w / 2, top, w, 34), wash='#6E6252', ink=INK, sw=1.0)
    for sx in (-1, 1):
        paint(rectPts(cx + sx * (w / 2 - 50) - 16, top + 34, 32, 300), wash='#4E4436', ink=INK, sw=.8)


def recorder(x, y, s, rec=0.0, t=0.0, key='rec'):
    """cassette recorder, (x, y) = bottom centre"""
    boilSeed(key)
    paint(rrPts(x - s, y - s * .9, 2 * s, s * .9, s * .12), wash='#3D3A52', fill='#2A2838', fillOp=60, ink=INK, sw=1.0)
    paint(rrPts(x - s * .8, y - s * .78, s * 1.1, s * .5, s * .06), wash='#C9CDD8', ink=INK, sw=.7)
    for cx_ in (x - s * .55, x - s * .05):
        paint(ellPts(cx_, y - s * .53, s * .14, s * .14, 12), wash='#5A566E', ink=INK, sw=.5)
        a = t * 6 * (1 if rec > .5 else 0)
        inkLine([[cx_ + math.cos(a) * s * .1, y - s * .53 + math.sin(a) * s * .1], [cx_ - math.cos(a) * s * .1, y - s * .53 - math.sin(a) * s * .1]],
                .8, INK, 'inkfine', 0)
    for i in range(4):
        paint(rrPts(x + s * .42 + (i % 2) * s * .24, y - s * .78 + (i // 2) * s * .2, s * .18, s * .14, 3), wash='#8A93B8', ink=INK, sw=.5)
    on = rec > .5 and (math.floor(t * 3) % 2 == 0)
    paint(ellPts(x + s * .55, y - s * .2, s * .08, s * .08, 10), wash='#FF3B4E' if rec > .5 else '#5A3038', ink=INK, sw=.5)
    if on:
        glow(x + s * .55, y - s * .2, s * .5, '#FF5A6A', .7)
    if rec > .5:
        text('REC', x + s * .55, y - s * .05 - s * .5 - 6, s * .2, '#FF3B4E', shadow=False, a=1.0 if on else .5)
    # microphone on a stalk
    inkLine([[x + s * .85, y - s * .9], [x + s * 1.0, y - s * 1.5]], 2.0, INK, 'ink', .3)
    paint(ellPts(x + s * 1.02, y - s * 1.62, s * .16, s * .2, 12), wash='#5A566E', ink=INK, sw=.7)


def caseFile(x, y, w, rot=0.0, key='cf', mark='？'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    h = w * .7
    paint(rectPts(-w / 2, -h / 2, w, h), wash=MANILA, fill=MANILADK, fillOp=50, ink=INK, sw=1.0)
    text(mark, 0, 0, h * .6, REDINK, shadow=False)
    pop()


# ================================================================ inside her heart
def heartRoom(t, key='hr2', grey=0.0):
    gradRect(-300, -300, W + 600, H + 600, ['#F7C6D2', '#F3AFC2'])
    # the heart-shaped wall arch
    boilSeed(key)
    paint(heartPts(960, 420, 680, 48), wash='#FBD0DA', fill='#F59AB0', fillOp=40, ink=INK, sw=1.6)
    paint(heartPts(960, 430, 610, 48), ink=mixCol('#E27A92', '#FFFFFF', .3), sw=1.0)
    # wallpaper of tiny hearts inside
    G.c.save()
    G.c.clipPath(eng._path(heartPts(960, 430, 610, 48)), skia.ClipOp.kIntersect, True)
    for i in range(-2, 22):
        for j in range(-2, 14):
            if (i + j) % 2 == 0:
                paint(heartPts(i * 90 + (45 if j % 2 else 0), j * 80, 9, 12), wash=mixCol('#F7A1B6', '#B8B4C8', grey), washOp=150, ink=None)
    if grey > 0:
        flatRect(-300, -300, W + 600, H + 600, '#8E8AA8', .25 * grey)
    G.c.restore()
    flatRect(-300, 860, W + 600, 400, '#E27A92')
    inkLine([[-300, 860], [W + 300, 860]], 1.0, INK, 'ink', 0)


def bench2(x, y, w, key='b2', col='#FFF5E2'):
    """little two-seat bench, (x, y) = floor centre: back + seat cushion. Seat people with sets2.seat() after this
    (legs hang in front of the cushion), then bench2Front() for the bench legs. Returns the seat top."""
    st = y - 120
    boilSeed(key)
    paint(rrPts(x - w / 2, st - 160, w, 170, 30), wash=col, fill='#E8D3B8', fillOp=60, ink=INK, sw=1.0)
    inkLine([[x, st - 150], [x, st]], 1.0, '#C9B89A', 'inkfine', 0)
    boilSeed(key + 'f')
    paint(rrPts(x - w / 2 - 8, st - 6, w + 16, 46, 12), wash=col, fill='#E8D3B8', fillOp=70, ink=INK, sw=1.0)
    return st


def bench2Front(x, y, w, key='b2', col='#FFF5E2'):
    st = y - 120
    boilSeed(key + 'l')
    for sx in (-1, 1):
        paint(rectPts(x + sx * (w / 2 - 30) - 12, st + 40, 24, y - st - 40), wash='#C9A27A', ink=INK, sw=.8)


def fedora(x, y, s, rot=0.0, key='fd', col='#6E6A80'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(ellPts(0, 0, s * 1.3, s * .28, 22), wash=mixCol(col, INK, .1), ink=INK, sw=.9)
    paint([[-s * .78, 0], [-s * .7, -s * .78], [0, -s * .62], [s * .7, -s * .78], [s * .78, 0]], wash=col, fill=mixCol(col, INK, .25), fillOp=60, ink=INK, sw=.9, curv=.4)
    paint(rectPts(-s * .76, -s * .26, s * 1.52, s * .2), wash='#2B2233', ink=None)
    pop()


def ghost(x, y, u, k=1.0, key='gh', fed=True, plac=None, a=1.0, seated=False):
    """the 「多出的一个人」: a grey Clawd silhouette with a question mark for a face (and a fedora)"""
    if k <= .02:
        return
    p = backOut(clamp(k))
    push()
    translate(x, y)
    scale(p)
    translate(-x, -y)
    o = dict(col='#8E8AA0', dk='#5E5A74', lt='#B8B4C8', eyes='blank', mouth=None, view='front', aL=-.6, aR=-.6, boilKey=key, noShadow=seated)
    if plac is not None:
        o.update(aL=.25, aR=.25)
    clawd(x, y, u, o)
    # cover the blank eyes with a big ?
    paint(rectPts(x - 3.6 * u, y - 7.4 * u, 7.2 * u, 3.0 * u), wash='#8E8AA0', ink=None)
    text('?', x, y - 5.6 * u, 4.6 * u, '#F3EBDC', stroke=INK, strokeW=u * .5, shadow=False)
    if fed:
        fedora(x, y - 8.0 * u, 4.0 * u, -.06, key=key + 'f')
    pop()


# ================================================================ photo booth + the print
def photoBooth(t, key='pb'):
    gradRect(-300, -300, W + 600, H + 600, ['#BFE3F5', '#9CD0EE'])
    # starry backdrop panel
    boilSeed(key)
    paint(rectPts(300, 80, 1320, 800), wash='#FBD0DA', fill='#F7A1B6', fillOp=40, ink=INK, sw=1.0)
    for i in range(24):
        sx = 340 + (i * 197) % 1240
        sy = 120 + (i * 131) % 700
        if i % 3 == 0:
            heartP(sx, sy, 14, col='#FFFFFF', key=key + f'h{i}', a=.7)
        else:
            sparkle(sx, sy, 10, '#FFFFFF')
    # curtains on both sides
    for sx in (-1, 1):
        cx = 960 + sx * 820
        boilSeed(key + f'c{sx}')
        pts = []
        for i in range(9):
            pts.append([cx - sx * (40 + 20 * math.sin(i * 1.3 + t)), -100 + i * 150])
        paint([[cx + sx * 400, -100]] + pts + [[cx + sx * 400, 1200]], wash='#E8476E', fill='#B8324F', fillOp=70, ink=INK, sw=1.0)
        for j in range(4):
            xx = cx + sx * (90 + j * 80)
            inkLine([[xx, -100], [xx + 10 * math.sin(t + j), 1200]], 1.0, '#9A2A42', 'inkfine', .3)
    flatRect(-300, 880, W + 600, 300, '#7B5CA8')
    inkLine([[-300, 880], [W + 300, 880]], 1.0, INK, 'ink', 0)


def countdownLights(x, y, n_on, key='cd'):
    for i in range(3):
        on = i < n_on
        boilSeed(key + str(i))
        paint(ellPts(x + (i - 1) * 60, y, 20, 20, 14), wash='#FF5A6A' if on else '#5A3038', ink=INK, sw=.7)
        if on:
            glow(x + (i - 1) * 60, y, 60, '#FF8A9A', .6)


def boothPrint(x, y, w, rot=0.0, dev=1.0, key='bp', drawPic=None, label='2026.10.31'):
    """a photo-booth print (single big frame); dev 0..1 develops the picture"""
    h = w * 1.22
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-w / 2 + 10, -h / 2 + 12, w, h), wash=INK, washOp=60, ink=None)
    paint(rectPts(-w / 2, -h / 2, w, h), wash='#FFFDF6', ink=INK, sw=1.0)
    pw, ph = w * .88, w * .92
    px, py = -pw / 2, -h / 2 + w * .06
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(px, py, pw, ph))
    flatRect(px, py, pw, ph, '#3A3550')
    if drawPic and dev > 0:
        G.c.saveLayerAlpha(None, int(255 * clamp(dev)))
        drawPic(px, py, pw, ph)
        G.c.restore()
    G.c.restore()
    paint(rectPts(px, py, pw, ph), ink=INK, sw=.8)
    wtext(label, 0, h / 2 - w * .1, w * .065, '#9A8AA0')
    pop()


# ================================================================ folder with a hinged cover (top-down), darkness with light holes
def folderHinged(x, y, w, h, rot, c, inside=None, key='fh', label='档案 No.0520', title=None):
    """c = cos of the cover angle: 1 closed over the papers, -1 laid open to the left (inside face up)"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-w / 2 + 10, -h / 2 + 14, w, h), wash=INK, washOp=60, ink=None, bleed=.2)
    paint(rectPts(-w / 2, -h / 2, w, h), wash=mixCol(MANILA, INK, .08), ink=INK, sw=1.0)
    if inside:
        inside(w, h)
    push()
    translate(-w / 2, 0)
    scale(c, 1)
    translate(w / 2, 0)
    boilSeed(key + 'c')
    if c >= 0:
        paint(rectPts(-w / 2, -h / 2, w, h), wash=MANILA, fill=MANILADK, fillOp=50, ink=INK, sw=1.1)
        paint([[-w / 2 + w * .06, -h / 2], [-w / 2 + w * .1, -h / 2 - h * .07], [-w / 2 + w * .42, -h / 2 - h * .07], [-w / 2 + w * .46, -h / 2]],
              wash=MANILA, ink=INK, sw=1.0)
        text(label, -w / 2 + w * .26, -h / 2 - h * .035, h * .042, '#6A4A2A', shadow=False)
        if title and c > .3:
            title()
    else:
        paint(rectPts(-w / 2, -h / 2, w, h), wash=mixCol(MANILA, '#FFFFFF', .15), fill=MANILADK, fillOp=30, ink=INK, sw=1.1)
    pop()
    pop()


def darkness(a, lights=(), col='#05060F'):
    """dark veil with soft holes punched out at each light (x, y, r, k)"""
    if a <= .01:
        return
    G.c.saveLayer(None, None)
    G.c.drawRect(skia.Rect.MakeXYWH(-400, -400, W + 800, H + 800), skia.Paint(Color=skcol(col, a)))
    for (x, y, r, k) in lights:
        if k <= .01:
            continue
        sh = skia.GradientShader.MakeRadial(skia.Point(x, y), r, [skcol('#000000', k), skcol('#000000', k * .55), skcol('#000000', 0)], [0, .45, 1])
        G.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Shader=sh, BlendMode=skia.BlendMode.kDstOut))
    G.c.restore()


def plushHim(x, y, s, key='plh'):
    """a little orange Clawd plush (his stand-in inside her heart); (x, y) = ground, as seat() gives it"""
    clawd(x, y, s, dict(col='#D97757', dk='#A84D33', lt='#F5B394', eyes='happy', mouth='smile', blush=.4, view='front', aL=-.4, aR=-.4,
                        boilKey=key, noShadow=True))
    for i in range(5):
        G.c.drawLine(x - 4 * s + i * 2 * s, y - 2.2 * s, x - 3.6 * s + i * 2 * s, y - 2.0 * s,
                     skia.Paint(AntiAlias=True, Color=skcol('#FFF5E2', .8), StrokeWidth=1.2))


def curtainPanel(x0, x1, top, bot, key='cp', col='#7B5CA8'):
    """a gathered curtain hanging from a rod between x0 and x1"""
    if x1 - x0 < 4:
        return
    boilSeed(key)
    inkLine([[x0 - 40, top], [x1 + 40, top]], 4.0, '#3A3550', 'ink', 0)
    paint(rectPts(x0, top, x1 - x0, bot - top), wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=1.0)
    n = max(2, int((x1 - x0) / 70))
    for i in range(1, n):
        xx = x0 + i * (x1 - x0) / n
        inkLine([[xx, top + 10], [xx + 6, bot - 10]], 1.2, mixCol(col, INK, .45), 'inkfine', .3)
    for i in range(n + 1):
        xx = x0 + i * (x1 - x0) / n
        paint(ellPts(xx, top, 10, 10, 10), wash='#C9A0D8', ink=INK, sw=.5)


# ================================================================ opening title + the user's signature watermark (hard rule 8)
from mv_config import load_signature


def signature(x, y, size=44, a=.92, rot=-.06, col='#FFFFFF'):
    SIGN = load_signature().lstrip('★')
    """small hand-lettered signature with a little star, placed beside the song title (from 《偷偷拍下你的样子》 tp.signature)"""
    if a <= .01:
        return
    push()
    translate(x, y)
    rotate(rot)
    w = textW(SIGN, size, WENKAI)
    boilSeed('signstar')
    paint(starPts(-w / 2 - size * .55, -size * .05, size * .38, .45, 5), wash='#FFE36E', washOp=int(255 * a), ink=INK, sw=.5)
    text(SIGN, 0, 0, size, col, face=WENKAI, stroke=INK, strokeW=size * .14, shadow=False, a=a)
    pop()


def openingTitle(k_in, k_out):
    """screen-space title card over the first ~2 s (crosses the S01 -> S02 cut): a manila case-file strip with the
    red rubber-stamp title, the user's signature ★你的署名 on the left below it, the singer on the right"""
    from common import rubberStamp
    push()
    G.c.saveLayerAlpha(None, int(255 * clamp(k_out)))
    k = k_in
    if k > .01:
        push()
        translate(960, 150 - 40 * (1 - k))
        scale(k)
        rotate(-.025)
        boilSeed('otstrip')
        paint(rectPts(-318, -98, 636, 196), wash=INK, washOp=70, ink=None, bleed=.2)
        paint(rectPts(-310, -92, 620, 184), wash=MANILA, fill=MANILADK, fillOp=50, ink=INK, sw=1.3)
        pop()
        push()
        translate(960, 150 - 40 * (1 - k))
        scale(k)
        rubberStamp('你瞒我瞒', 0, 0, 128, 9.0, col=REDINK, rot=-.06)
        paperclip(285, -105, 26, .15)
        pop()
    signature(700, 298, 50, a=.92 * clamp(k_in))
    text('陈柏宇', 1222, 298, 44, '#FFF3E2', face=WENKAI, stroke=INK, strokeW=7, shadow=False, a=clamp(k_in))
    G.c.restore()
    pop()
