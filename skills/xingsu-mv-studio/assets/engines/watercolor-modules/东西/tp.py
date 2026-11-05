# tp.py: props and sets for 《偷偷拍下你的样子》 (watercolour + ink). Engine files stay untouched.
# Her costume for this song: the white flower + a pink instant camera (drawn in world coordinates at her hand).
# His: an orange-cased phone. Both cameras get the same flash burst, so the last shot can mirror the first.
import math
from eng import *
import eng
from clawd import *
from props import puff, sparkle, sparkles, floatHearts, bubble, stamp, tree, bush, lamp, bench, trashcan, umbrellaAt
from ch_chonghuai import rr, heart, popK, shakeAmt, bobaCup, WENKAI, HOT, PINK, PINKDK, CREAM, fo
from common import handXY, B, bt, age, pk, after, kt

YEL = '#FFD84A'
HER_CASE, HER_CASE_DK = '#F4A3BC', '#C9657F'
HIS_CASE, HIS_CASE_DK = '#F2A65A', '#B8692E'
THEME = dict(her=dict(case=HER_CASE, dk=HER_CASE_DK, acc='#FF7FA6'), him=dict(case=HIS_CASE, dk=HIS_CASE_DK, acc='#FFB15C'))
HERC = dict(col='#EE9AAE', dk='#C0637B', lt='#FBD0DA')


def em(t, keys, who='her'):
    return emotions(t, keys, HERC if who == 'her' else ME)


# ------------------------------------------------------------------ cameras
def flashBurst(x, y, r, k, col='#FFFBE8'):
    """camera flash: glow + 8 rays, k 1 -> 0"""
    if k <= .02:
        return
    glow(x, y, r * 2.4, '#FFF4C4', k)
    glow(x, y, r * 1.1, '#FFFFFF', k)
    for i in range(8):
        a = i / 8 * TAU + .2
        L = r * (1.4 if i % 2 else .9) * (.6 + .4 * k)
        p = skia.Paint(AntiAlias=True, Color=skcol(col, .9 * k), StrokeWidth=max(2, r * .09), StrokeCap=skia.Paint.kRound_Cap)
        G.c.drawLine(x + math.cos(a) * r * .35, y + math.sin(a) * r * .35, x + math.cos(a) * L, y + math.sin(a) * L, p)
    G.c.drawCircle(x, y, r * .3 * k, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', k)))


def instantCam(x, y, s, face=1, rot=0.0, flashK=0.0, key='icam', col='#F7B2C6'):
    """her pink instant camera centred at (x, y), 2.6s wide; the lens looks toward `face` (1 = right)"""
    push()
    translate(x, y)
    rotate(rot)
    scale(face, 1)
    boilSeed(key)
    dk = mixCol(col, INK, .25)
    paint(rrPts(-1.3 * s, -.95 * s, 2.6 * s, 1.9 * s, .38 * s), wash=col, fill=dk, fillOp=55, ink=INK, sw=.9)
    paint(rrPts(-1.22 * s, -.9 * s, 2.44 * s, .42 * s, .2 * s), wash=mixCol(col, '#FFFFFF', .45), ink=None)
    paint(rectPts(-1.3 * s, .55 * s, 2.6 * s, .22 * s), wash=dk, ink=None)
    paint(ellPts(.25 * s, .12 * s, .66 * s, .66 * s, 22), wash='#F4EEE6', ink=INK, sw=.8)
    paint(ellPts(.25 * s, .12 * s, .46 * s, .46 * s, 18), wash='#3A3550', ink=None)
    paint(ellPts(.25 * s, .12 * s, .26 * s, .26 * s, 14), wash='#6E7FB8', ink=None)
    paint(ellPts(.14 * s, .0, .1 * s, .1 * s, 8), wash='#FFFFFF', washOp=220, ink=None)
    paint(rrPts(.62 * s, -.8 * s, .52 * s, .32 * s, .08 * s), wash='#FFF6D8', ink=INK, sw=.5)
    paint(rrPts(-1.08 * s, -.78 * s, .42 * s, .3 * s, .06 * s), wash='#3A3550', ink=None)
    paint(ellPts(-.72 * s, -1.03 * s, .2 * s, .12 * s, 10), wash=HOT, ink=INK, sw=.5)
    paint(heartPts(-.78 * s, .2 * s, .22 * s, 14), wash=HOT, ink=None)
    pop()
    if flashK > .02:
        fx, fy = x + face * .88 * s * math.cos(rot) - (-.64 * s) * math.sin(rot) * face, y + .88 * s * math.sin(rot) * face - .64 * s * math.cos(rot)
        flashBurst(fx, fy, s * 1.3, flashK)


def phoneCam(x, y, s, face=1, rot=0.0, flashK=0.0, key='pcam', screen=None, col=HIS_CASE):
    """his orange-cased phone held up sideways; we see its back (camera bump) when face=1, the screen when face=-1"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rrPts(-1.5 * s, -.85 * s, 3.0 * s, 1.7 * s, .3 * s), wash=col, fill=mixCol(col, INK, .25), fillOp=55, ink=INK, sw=.9)
    if face > 0:
        paint(rrPts(-1.25 * s, -.65 * s, .9 * s, .75 * s, .18 * s), wash='#3A3550', ink=INK, sw=.5)
        for lx, ly in ((-1.02, -.42), (-.6, -.42), (-1.02, -.08)):
            paint(ellPts(lx * s, ly * s, .15 * s, .15 * s, 10), wash='#6E7FB8', ink=None)
        paint(ellPts(-.6 * s, -.08 * s, .08 * s, .08 * s, 8), wash='#FFF6D8', ink=None)
        paint(heartPts(.55 * s, .15 * s, .3 * s, 14), wash='#FFF3E2', ink=None)
    else:
        paint(rrPts(-1.36 * s, -.72 * s, 2.72 * s, 1.44 * s, .2 * s), wash='#20203A', ink=None)
        if screen:
            G.c.save()
            G.c.clipRect(skia.Rect.MakeXYWH(-1.32 * s, -.68 * s, 2.64 * s, 1.36 * s), skia.ClipOp.kIntersect, True)
            screen(0, 0, 2.64 * s, 1.36 * s)
            G.c.restore()
    pop()
    if flashK > .02:
        fx = x + (-.6 * s) * math.cos(rot) - (-.08 * s) * math.sin(rot)
        fy = y + (-.6 * s) * math.sin(rot) + (-.08 * s) * math.cos(rot)
        flashBurst(fx, fy, s * 1.2, flashK)


# ------------------------------------------------------------------ the camera-app viewfinder (landscape: controls on the right)
MODES = ['延时', '视频', '拍照', '偷偷拍', '人像']
VF = dict(x0=36, y0=30, x1=W - 36, y1=H - 30, bar=1640)


def focusBox(x, y, w, h, k, t, lockAge=None, col=YEL):
    """yellow focus brackets; k = lock progress (0 big & faint -> 1 snapped)"""
    if k <= .02:
        return
    s = lerp(1.7, 1.0, backOut(k))
    a = clamp(k * 2)
    ww, hh = w * s / 2, h * s / 2
    L = min(w, h) * .22
    pa = skia.Paint(AntiAlias=True, Color=skcol(col, a), StrokeWidth=6, StrokeCap=skia.Paint.kRound_Cap, Style=skia.Paint.kStroke_Style)
    for sx in (-1, 1):
        for sy in (-1, 1):
            cx, cy = x + sx * ww, y + sy * hh
            p = skia.Path()
            p.moveTo(cx - sx * L, cy)
            p.lineTo(cx, cy)
            p.lineTo(cx, cy - sy * L)
            G.c.drawPath(p, pa)
    if lockAge is not None and lockAge > 0:
        # exposure sun + slider to the right of the box
        sx_ = x + ww + 34
        G.c.drawLine(sx_, y - hh * .7, sx_, y + hh * .7, skia.Paint(AntiAlias=True, Color=skcol(col, .8 * a), StrokeWidth=3))
        G.c.drawCircle(sx_, y - hh * .1, 12, skia.Paint(AntiAlias=True, Color=skcol(col, a)))
        for i in range(8):
            aa = i / 8 * TAU
            G.c.drawLine(sx_ + math.cos(aa) * 17, y - hh * .1 + math.sin(aa) * 17, sx_ + math.cos(aa) * 23, y - hh * .1 + math.sin(aa) * 23,
                         skia.Paint(AntiAlias=True, Color=skcol(col, a), StrokeWidth=3, StrokeCap=skia.Paint.kRound_Cap))
        if lockAge < .6:
            text('对焦', x, y - hh - 34, 30, col, stroke=INK, strokeW=5, shadow=False, a=a * (1 - seg(lockAge, .45, .6)))


def shutterFlash(t, shots, peak=.85):
    for tb in shots:
        a = t - tb
        if -.002 <= a < .16:
            flash(peak * (1 - a / .16))


def viewfinderUI(t, theme='her', shots=(), count0=97, zoom='1x', thumb=None, modeSel=3, flyFrom=None):
    """the camera-app chrome drawn over a scene; shots = beat times the shutter fires (flash, count, thumbnail fly-in)"""
    th = THEME[theme]
    x0, y0, x1, y1, bx = VF['x0'], VF['y0'], VF['x1'], VF['y1'], VF['bar']
    c = G.c
    # rule-of-thirds grid
    gp = skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .32), StrokeWidth=2)
    for i in (1, 2):
        xx = x0 + (bx - x0) * i / 3
        yy = y0 + (y1 - y0) * i / 3
        c.drawLine(xx, y0, xx, y1, gp)
        c.drawLine(x0, yy, bx, yy, gp)
    # top status: flash bolt, HDR, zoom pill
    flatRect(x0, y0, bx - x0, 92, '#000000', .28)
    boilSeed('vfbolt')
    paint([[118, 52], [100, 84], [114, 84], [104, 108], [132, 72], [117, 72], [126, 52]], wash=YEL, ink=None)
    text('HDR', 210, 80, 30, '#FFFFFF', shadow=False)
    c.drawCircle(300, 80, 14, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .9), Style=skia.Paint.kStroke_Style, StrokeWidth=3))
    c.drawLine(300, 80, 300, 70, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF'), StrokeWidth=3))
    rr((bx + x0) / 2 - 56, 52, 112, 56, 28, '#1C1A2A', ink=None, washOp=150)
    text(zoom, (bx + x0) / 2, 80, 34, YEL, shadow=False)
    # live dot
    c.drawCircle(bx - 60, 80, 9, skia.Paint(AntiAlias=True, Color=skcol(th['acc'], .6 + .4 * (math.sin(t * 9) > 0))))
    # right control bar
    flatRect(bx, y0, x1 - bx, y1 - y0, '#0E0C18', .62)
    my = (y0 + y1) / 2
    for i, m in enumerate(MODES):
        yy = my + (i - modeSel) * 74
        sel = i == modeSel
        text(m, bx + 70, yy, 34 if sel else 25, th['acc'] if sel else '#D8D2E2', shadow=False, a=1 if sel else .75)
        if sel:
            c.drawCircle(bx + 70, yy + 30, 5, skia.Paint(AntiAlias=True, Color=skcol(th['acc'])))
    # shutter (presses on each shot)
    sx, sy = bx + 182, my
    press = 0.0
    for tb in shots:
        a = t - tb
        if -.04 <= a < .14:
            press = max(press, 1 - abs(a - .03) / .11)
    c.drawCircle(sx, sy, 62, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF'), Style=skia.Paint.kStroke_Style, StrokeWidth=7))
    c.drawCircle(sx, sy, 50 * (1 - .14 * press), skia.Paint(AntiAlias=True, Color=skcol(th['acc'] if press > .3 else '#FFFFFF')))
    # switch-camera icon
    c.drawCircle(sx, y0 + 150, 34, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .2)))
    inkLine([[sx - 16, y0 + 142], [sx, y0 + 130], [sx + 16, y0 + 142]], 1.0, '#FFFFFF', 'inkfine', .5)
    inkLine([[sx + 16, y0 + 158], [sx, y0 + 170], [sx - 16, y0 + 158]], 1.0, '#FFFFFF', 'inkfine', .5)
    # gallery thumbnail + counter
    n = count0 + sum(1 for tb in shots if t >= tb)
    gx, gy, gs = sx - 52, y1 - 190, 104
    c.save()
    c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(gx, gy, gs, gs), 14, 14), skia.ClipOp.kIntersect, True)
    flatRect(gx, gy, gs, gs, '#FFFDF6')
    if thumb and n > count0 - 1:
        thumb(gx + gs / 2, gy + gs / 2, gs, gs)
    c.restore()
    c.drawRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(gx, gy, gs, gs), 14, 14),
                skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF'), Style=skia.Paint.kStroke_Style, StrokeWidth=4))
    lab = str(n) if (n < 100 or count0 >= 100) else '99+'
    bump_ = 0.0
    for tb in shots:
        bump_ = max(bump_, math.exp(-max(0, t - tb - .1) * 10) if t >= tb + .1 else 0)
    rr(gx - 70, gy - 34, 96, 50, 25, th['acc'], ink=INK, sw=.6, key='vfcnt')
    text(lab, gx - 22, gy - 9, 32 * (1 + .25 * bump_), '#FFFFFF', shadow=False)
    # each shot: a little photo flies from the frame centre into the gallery
    for tb in shots:
        a = t - tb
        if 0 <= a < .3:
            k = easeIn(a / .3)
            fx0, fy0 = flyFrom or ((x0 + bx) / 2, (y0 + y1) / 2)
            cx, cy = lerp(fx0, gx + gs / 2, k), lerp(fy0, gy + gs / 2, k)
            ww = lerp(560, gs, k)
            push()
            translate(cx, cy)
            rotate(-.15 * k)
            boilSeed('vffly')
            paint(rectPts(-ww / 2 - 10, -ww * .36 - 10, ww + 20, ww * .72 + 20), wash='#FFFDF6', ink=INK, sw=.8)
            if thumb:
                G.c.save()
                G.c.clipRect(skia.Rect.MakeXYWH(-ww / 2, -ww * .36, ww, ww * .72), skia.ClipOp.kIntersect, True)
                thumb(0, 0, ww, ww * .72)
                G.c.restore()
            pop()
    # phone case bezel
    p = skia.Path()
    p.setFillType(skia.PathFillType.kEvenOdd)
    p.addRect(skia.Rect.MakeXYWH(-200, -200, W + 400, H + 400))
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x0, y0, x1 - x0, y1 - y0), 64, 64))
    c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol(th['case'])))
    boilSeed('bezel' + theme)
    inkStroke(rrPts(x0, y0, x1 - x0, y1 - y0, 64), True, 1.3, INK)
    inkStroke(rrPts(10, 8, W - 20, H - 16, 80), True, 1.0, th['dk'])
    # little stickers on the case
    if theme == 'her':
        heart(W - 22, 120, 14, '#FFFFFF', key='cs1', sw=.4, shine=False)
        heart(18, H - 140, 12, '#FFFFFF', key='cs2', sw=.4, shine=False)
    else:
        paint(starPts(W - 20, 130, 16, .45, 5), wash='#FFF3E2', ink=None)
        paint(starPts(18, H - 150, 13, .45, 5), wash='#FFF3E2', ink=None)


def kacha(t, tb, x, y, size=72, col='#FFFFFF', rot=-.12, life=.36):
    stamp('咔嚓', x, y, size, col, t - tb, rot=rot, life=life)


# ------------------------------------------------------------------ the park (same layout in every park shot)
PARK = dict(horizon=600, benchX=960, benchY=812, benchW=430, lampX=640, treeX=1500, bushX=470, binX=1260)


def skyline(y, col, win=None, winA=0.0, key='sky'):
    boilSeed(key)
    xs = [-80, 60, 170, 330, 420, 560, 700, 820, 980, 1100, 1240, 1380, 1500, 1650, 1780, 1900, 2050]
    hs = [120, 200, 150, 240, 170, 130, 210, 160, 260, 140, 190, 230, 150, 210, 170, 140, 160]
    for i in range(len(xs) - 1):
        x, w, h = xs[i], xs[i + 1] - xs[i] + 6, hs[i]
        flat(rectPts(x, y - h, w, h), mixCol(col, INK, .06 * (i % 3)))
        if win and winA > .01:
            for r in range(int(h / 34)):
                for q in range(int(w / 30)):
                    if hash1(i * 31 + r * 7 + q) < .35:
                        flatRect(x + 10 + q * 30, y - h + 14 + r * 34, 10, 14, win, winA)


def bigTree(x, y, s, t, key='bt', col='#7CC36B', branch=True, night=0.0):
    """park tree with a long branch reaching left (she hangs from it in S02)"""
    c = mixCol(col, '#2A3A5A', night * .55)
    boilSeed(key)
    paint([[x - .45 * s, y], [x - .3 * s, y - 2.8 * s], [x + .3 * s, y - 2.8 * s], [x + .5 * s, y]], wash=mixCol('#9B6B45', '#3A3550', night * .4), ink=INK, sw=1.1)
    if branch:
        paint(ribbon([[x - .2 * s, y - 2.6 * s], [x - 1.5 * s, y - 3.0 * s], [x - 2.9 * s, y - 3.05 * s]], .32 * s, .16 * s),
              wash=mixCol('#9B6B45', '#3A3550', night * .4), ink=INK, sw=1)
        cl = []
        for i in range(24):
            a = i / 24 * TAU
            r = 1 + .16 * abs(math.sin(a * 3))
            cl.append([x - 2.9 * s + math.cos(a) * .9 * s * r, y - 3.35 * s + math.sin(a) * .55 * s * r])
        paint(cl, wash=c, fill=mixCol(c, '#2E6B3A', .4), fillOp=70, ink=INK, sw=1.0, curv=.3)
    cr = []
    for i in range(34):
        a = i / 34 * TAU
        r = 1 + .13 * abs(math.sin(a * 3.5))
        cr.append([x + math.cos(a) * 2.0 * s * r, y - 4.0 * s + math.sin(a) * 1.6 * s * r])
    paint(cr, wash=c, fill=mixCol(c, '#2E6B3A', .4), fillOp=70, ink=INK, sw=1.1, curv=.3)
    for i in range(6):
        paint(ellPts(x + (hash1(i + 3) - .5) * 2.8 * s, y - 4 * s + (hash1(i + 9) - .5) * 2 * s, .15 * s, .15 * s, 8),
              wash=mixCol('#F59AB0', '#6A5A90', night * .5), ink=None)


def grassTufts(y0, y1, n, seed, col, a=.7):
    for i in range(n):
        x = hash1(seed + i * 3.3) * (W + 200) - 100
        y = lerp(y0, y1, hash1(seed * 2 + i * 1.7))
        s = 8 + 10 * (y - y0) / max(1, y1 - y0)
        p = skia.Paint(AntiAlias=True, Color=skcol(col, a), StrokeWidth=2.2, StrokeCap=skia.Paint.kRound_Cap)
        for j in (-1, 0, 1):
            G.c.drawLine(x, y, x + j * s * .45, y - s * (1.2 - .3 * abs(j)), p)


def flowersDots(y0, y1, n, seed, cols, a=1.0):
    for i in range(n):
        x = hash1(seed + i * 5.1) * (W + 200) - 100
        y = lerp(y0, y1, hash1(seed * 3 + i * 2.3))
        r = 5 + 6 * (y - y0) / max(1, y1 - y0)
        col = cols[i % len(cols)]
        for k in range(5):
            aa = k / 5 * TAU
            G.c.drawCircle(x + math.cos(aa) * r * .7, y + math.sin(aa) * r * .7, r * .55, skia.Paint(AntiAlias=True, Color=skcol(col, a)))
        G.c.drawCircle(x, y, r * .4, skia.Paint(AntiAlias=True, Color=skcol('#F2C53D', a)))


def parkScene(t, mode='day', bench_=True, tree_=True, bush_=True, lamp_=True, bin_=True, binLid=0.0, key='pk'):
    """sky, skyline, grass, path, lamp, tree, bush, bench. returns the bench seat top (y)."""
    hz = PARK['horizon']
    night = 1.0 if mode == 'night' else 0.0
    if night:
        gradRect(-300, -300, W + 600, hz + 300, ['#141A44', '#2C2D66', '#5A4A86'])
        from hl import stars
        stars(t, 7, 70, -100, -100, W + 100, hz - 160, a=.9)
        boilSeed(key + 'moon')
        paint(ellPts(1640, 150, 62, 62, 28), wash='#FFF3C8', ink=INK, sw=.8)
        paint(ellPts(1668, 136, 52, 52, 28), wash='#2C2D66', ink=None)
        skyline(hz + 4, '#2A2A55', '#FFD98A', .8, key=key + 'sl')
    else:
        gradRect(-300, -300, W + 600, hz + 300, ['#8EC9EE', '#BFE3F5', '#EEF6E6'])
        puff(380, 150, 34, key=key + 'c1')
        puff(1250, 110, 26, key=key + 'c2')
        puff(1760, 220, 22, key=key + 'c3')
        skyline(hz + 4, '#B7CBE0', key=key + 'sl')
    # far tree line
    for i in range(14):
        x = -60 + i * 150 + 40 * hash1(i)
        boilSeed(f'{key}ft{i}')
        paint(ellPts(x, hz - 6, 110, 60, 18, 3), wash=mixCol('#8CC67A', '#24335A', night * .7), ink=None)
    # grass + path
    flatRect(-300, hz, W + 600, H + 400 - hz, mixCol('#A9DA8A', '#2E4A52', night * .8))
    gradRect(-300, hz, W + 600, 90, [mixCol('#94CC78', '#26404E', night * .8), mixCol('#A9DA8A', '#2E4A52', night * .8)])
    boilSeed(key + 'path')
    paint([[760, hz], [1160, hz], [1700, H + 60], [220, H + 60]], wash=mixCol('#F1DDB4', '#5A587A', night * .75), ink=None)
    inkLine([[760, hz], [220, H + 60]], .7, mixCol('#C9A97A', INK, .3), 'inkfine', 0)
    inkLine([[1160, hz], [1700, H + 60]], .7, mixCol('#C9A97A', INK, .3), 'inkfine', 0)
    grassTufts(hz + 30, H, 70, 3, mixCol('#5E9E4A', '#1E3440', night * .7))
    flowersDots(hz + 40, H - 40, 26, 5, ['#FFFFFF', '#F7B2C6', '#FFE38A'], a=1 - .5 * night)
    if night:
        from hl import fireflies
        fireflies(t, 3, 14, 100, hz - 60, W - 100, H - 100)
    if lamp_:
        lamp(PARK['lampX'], 760, 44, on=1.0 if night else 0.0, key=key + 'lamp')
    if tree_:
        bigTree(PARK['treeX'], 800, 100, t, key=key + 'tree', night=night)
    if bin_:
        trashcanLid(PARK['binX'], 790, 36, binLid, key=key + 'bin', night=night)
    st = None
    if bench_:
        from sets2 import parkBench
        st = parkBench(PARK['benchX'], PARK['benchY'], PARK['benchW'], 74, 112, key=key + 'bench', night=night)
    return st


def parkFront(t, mode='day', key='pk'):
    """things in front of the bench (the bush)"""
    night = 1.0 if mode == 'night' else 0.0
    bush(PARK['bushX'], 870, 104, key=key + 'bush', col=mixCol('#86C96E', '#2F4A5A', night * .6))


def trashcanLid(x, y, s, lid=0.0, key='trash', night=0.0, inside=None):
    """park bin; lid 0..1 lifts the lid off; inside() is drawn between the can's back and front rim"""
    boilSeed(key)
    col = mixCol('#7FA9C9', '#3E4A72', night * .5)
    paint([[x - 1.1 * s, y - 2.6 * s], [x + 1.1 * s, y - 2.6 * s], [x + .9 * s, y], [x - .9 * s, y]], wash=col, ink=INK, sw=1)
    for i in (-.5, 0, .5):
        inkLine([[x + i * s, y - 2.3 * s], [x + i * .85 * s, y - .25 * s]], .6, INK, 'inkfine', 0)
    if inside:
        inside()
    ly = -lid * 1.6 * s
    push()
    translate(x + lid * .5 * s, y - 2.85 * s + ly)
    rotate(-.35 * lid)
    paint(rrPts(-1.25 * s, -.22 * s, 2.5 * s, .44 * s, .15 * s), wash=mixCol(col, INK, .15), ink=INK, sw=1)
    paint(rrPts(-.3 * s, -.5 * s, .6 * s, .3 * s, .1 * s), wash=mixCol(col, INK, .15), ink=INK, sw=.8)
    pop()


def trashcanOpen(x, y, s, key='trash', night=0.0):
    """the bin without its lid (she is inside)"""
    boilSeed(key)
    col = mixCol('#7FA9C9', '#3E4A72', night * .5)
    paint(ellPts(x, y - 2.6 * s, 1.1 * s, .25 * s, 16), wash='#3A4260', ink=INK, sw=.8)
    paint([[x - 1.1 * s, y - 2.6 * s], [x + 1.1 * s, y - 2.6 * s], [x + .9 * s, y], [x - .9 * s, y]], wash=col, ink=INK, sw=1)
    for i in (-.5, 0, .5):
        inkLine([[x + i * s, y - 2.3 * s], [x + i * .85 * s, y - .25 * s]], .6, INK, 'inkfine', 0)


# ------------------------------------------------------------------ little photos of each other (polaroids, thumbnails)
def snap(cx, cy, iw, ih, who='him', pose='read', night=False, bg=None):
    """a tiny picture of him (or her) for polaroids / thumbnails, filling the iw x ih box centred at (cx, cy)"""
    x, y = cx - iw / 2, cy - ih / 2
    cols = bg or (['#2A2D6E', '#6B5AA8'] if night else ['#9FD4F2', '#F3E6C8'])
    gradRect(x, y, iw, ih, cols)
    flatRect(x, y + ih * .72, iw, ih * .28, '#3E5A4E' if night else '#A9DA8A')
    u = ih / 15
    o = dict(lite=True, noShadow=True, boilKey=f'snap{pose}{who}')
    if pose == 'read':
        o.update(eyes='look', lookY=.8, mouth='smile', aL=.9, aR=.9)
    elif pose == 'boba':
        o.update(eyes='happy', mouth='cat', blush=.4, aR=1.1)
    elif pose == 'yawn':
        o.update(eyes='sleepy', mouth='yawn', aL=1.4, aR=1.4)
    elif pose == 'wave':
        o.update(eyes='happy', mouth='open', aR=1.6)
    elif pose == 'sad':
        o.update(eyes='sad', mouth='frown', aL=-.6, aR=-.6)
    elif pose == 'smile':
        o.update(eyes='shine', mouth='smile', blush=.5)
    elif pose == 'daisy':
        o.update(eyes='look', lookY=.6, mouth='flat', aR=.9)
    fn = him if who == 'him' else her
    fn(cx, y + ih * .86, u, o)
    if pose == 'boba':
        bobaCup(cx + 6.5 * u, y + ih * .8, u * 1.1, key='snb')
    if pose == 'read':
        boilSeed('snbook')
        paint(rectPts(cx - 2.6 * u, y + ih * .58, 5.2 * u, 2.4 * u), wash='#5B7FC4', ink=INK, sw=.4, lite=True)
    if pose == 'daisy':
        inkLine([[cx + 6 * u, y + ih * .6], [cx + 6.3 * u, y + ih * .3]], .6, PAL['sap'], 'inkfine', 0)
        paint(ellPts(cx + 6.3 * u, y + ih * .3, u * .5, u * .5, 8), wash='#F2B63A', ink=None)


def polaroidPic(x, y, w, rot, k, scene, key='pp', label=None, pinCol=HOT, tape=False):
    """polaroid centred at (x, y) popping in with k; scene(cx, cy, iw, ih)"""
    p = backOut(k)
    if p < .02:
        return
    push()
    translate(x, y)
    rotate(rot)
    scale(p)
    boilSeed(key)
    h = w * 1.2
    paint(rectPts(-w / 2 + 6, -h / 2 + 8, w, h), wash=INK, washOp=55, ink=None)
    paint(rectPts(-w / 2, -h / 2, w, h, 1), wash='#FFFDF6', ink=INK, sw=.8)
    iw, ih = w * .86, w * .82
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(-iw / 2, -h / 2 + w * .07, iw, ih), skia.ClipOp.kIntersect, True)
    scene(0, -h / 2 + w * .07 + ih / 2, iw, ih)
    G.c.restore()
    inkStroke(rectPts(-iw / 2, -h / 2 + w * .07, iw, ih), True, .45, INK, 'inkfine')
    if label:
        text(label, 0, h / 2 - w * .13, w * .12, '#6A5A70', shadow=False, face=WENKAI)
    if tape:
        paint(rectPts(-w * .2, -h / 2 - w * .06, w * .4, w * .13), wash='#F7D36E', washOp=180, ink=None)
    elif pinCol:
        paint(ellPts(0, -h / 2 + w * .04, w * .05, w * .05, 10), wash=pinCol, ink=INK, sw=.6)
    pop()


# ------------------------------------------------------------------ desk night room (S03)
def paperBall(x, y, r, rot=0.0, key='pb', col='#FFFDF6'):
    boilSeed(key)
    pts = []
    for i in range(11):
        a = rot + i / 11 * TAU
        rr_ = r * (.78 + .32 * hash1(i * 7.7 + len(key)))
        pts.append([x + math.cos(a) * rr_, y + math.sin(a) * rr_])
    paint(pts, wash=col, fill='#D9D2C2', fillOp=60, ink=INK, sw=.7)
    for i in range(3):
        a = rot + hash1(i + len(key)) * TAU
        inkLine([[x + math.cos(a) * r * .1, y + math.sin(a) * r * .1], [x + math.cos(a + .8) * r * .6, y + math.sin(a + .8) * r * .6]], .4,
                '#9A90A0', 'inkfine', 0)
    for i in range(2):
        yy = y - r * .3 + i * r * .35
        inkLine([[x - r * .4, yy], [x + r * .3, yy + r * .05]], .3, '#8FA9D8', 'inkfine', 0)


def wastebasket(x, y, w, h, key='wb', back=True):
    boilSeed(key)
    if back:
        paint(ellPts(x, y - h, w / 2, w * .12, 20), wash='#5E5470', ink=INK, sw=.7)
        return
    paint([[x - w / 2, y - h], [x + w / 2, y - h], [x + w * .4, y], [x - w * .4, y]], wash='#C9B8E8', fill='#9C8AC0', fillOp=60, ink=INK, sw=1)
    for i in range(1, 6):
        k = i / 6
        inkLine([[x - w / 2 + w * k, y - h + 4], [x - w * .4 + w * .8 * k, y - 4]], .45, '#7C6AA0', 'inkfine', 0)
    inkLine([[x - w / 2, y - h], [x + w / 2, y - h]], 1.4, INK, 'ink', 0)


def roomWallNight(c1='#2B3168', c2='#4A4486'):
    gradRect(-300, -300, W + 600, H + 600, [c1, c2])
    for i in range(-2, 22):
        flatRect(i * 110, -100, 3, H + 200, '#FFFFFF', .035)


def deskFront(y, x0=-100, x1=W + 100, col='#8A5A3C', key='dk'):
    boilSeed(key)
    paint(rectPts(x0, y, x1 - x0, 40), wash=mixCol(col, '#FFFFFF', .12), ink=INK, sw=1.0)
    paint(rectPts(x0, y + 40, x1 - x0, H + 200 - y), wash=mixCol(col, INK, .18), fill=mixCol(col, INK, .35), fillOp=50, ink=INK, sw=1.0)
    for i in range(6):
        yy = y + 60 + i * 34
        inkLine([[x0 + 20, yy], [x1 - 20, yy + 6 * math.sin(i)]], .35, mixCol(col, INK, .4), 'inkfine', .5)


def pencilCup(x, y, s, key='pcup'):
    boilSeed(key)
    for i, (dx, col, L) in enumerate(((-.5, '#E8476E', 2.8), (0, '#5B7FC4', 3.2), (.45, '#F2C53D', 2.6))):
        inkLine([[x + dx * s, y - 1.5 * s], [x + dx * 1.3 * s, y - L * s]], 1.6, col, 'ink', 0)
    paint(rrPts(x - .9 * s, y - 1.8 * s, 1.8 * s, 1.8 * s, .25 * s), wash='#7FB1B5', ink=INK, sw=.8)


def stringPhotos(t, x0, x1, y, n=5, key='sp', night=True):
    pts = [[lerp(x0, x1, i / 20), y + 30 * math.sin(i / 20 * math.pi)] for i in range(21)]
    inkLine(pts, .8, '#C9B08F', 'inkfine', .3)
    poses = ['read', 'boba', 'wave', 'smile', 'yawn', 'read']
    for i in range(n):
        k = (i + .5) / n
        px, py = lerp(x0, x1, k), y + 30 * math.sin(k * math.pi)
        rot = (hash1(i * 3.1) - .5) * .3 + .02 * math.sin(t * .8 + i)
        polaroidPic(px, py + 64, 96, rot, 1, lambda cx, cy, iw, ih, p=poses[i % len(poses)]: snap(cx, cy, iw, ih, 'him', p), key=f'{key}{i}',
                    pinCol=None, tape=False)
        boilSeed(f'{key}pin{i}')
        paint(rectPts(px - 6, py - 4, 12, 24), wash='#D9B45A', ink=INK, sw=.5, lite=True)


# ------------------------------------------------------------------ notebook page (S04)
def notebookPage(x, y, w, h, key='nb', lines=14):
    boilSeed(key)
    paint(rectPts(x + 14, y + 16, w, h), wash=INK, washOp=50, ink=None)
    paint(rectPts(x, y, w, h, 1.5), wash='#FFFDF6', ink=INK, sw=1.0)
    gap = h / (lines + 1)
    for i in range(1, lines + 1):
        G.c.drawLine(x + 10, y + i * gap, x + w - 10, y + i * gap, skia.Paint(AntiAlias=True, Color=skcol('#9EC3E8', .55), StrokeWidth=2))
    G.c.drawLine(x + 110, y + 6, x + 110, y + h - 6, skia.Paint(AntiAlias=True, Color=skcol('#F08A9C', .6), StrokeWidth=2.5))
    for i in range(8):
        G.c.drawCircle(x + 46, y + 60 + i * (h - 120) / 7, 12, skia.Paint(AntiAlias=True, Color=skcol('#3A3550', .85)))
    return gap


def noteDoodle(x, y, s, key='nd', col='#7A6A80'):
    boilSeed(key)
    paint(ellPts(x, y, s * .45, s * .32, 12, 0, -.4), wash=col, ink=None)
    inkLine([[x + s * .4, y - s * .05], [x + s * .4, y - s * 1.4], [x + s * 1.0, y - s * 1.1]], .7, col, 'ink', 0)


def strike(x0, x1, y, key='st', col='#7A6A80'):
    boilSeed(key)
    inkLine([[x0, y], [x0 + (x1 - x0) * .33, y - 6], [x0 + (x1 - x0) * .66, y + 4], [x1, y - 3]], .9, col, 'ink', .5)


def penProp(x, y, ang, s=1.0, key='pen', glowK=0.0):
    """pink gel pen, nib at (x, y), body going up-right at angle ang"""
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    paint([[0, 0], [38 * s, -9 * s], [38 * s, 9 * s]], wash='#E8E1D2', ink=INK, sw=.7)
    paint(rrPts(36 * s, -15 * s, 280 * s, 30 * s, 12 * s), wash='#F7A8C0', fill='#E27A92', fillOp=60, ink=INK, sw=.9)
    paint(rectPts(70 * s, -16 * s, 60 * s, 32 * s), wash='#E8476E', fill=INK, fillOp=30, ink=INK, sw=.6)
    paint(rectPts(250 * s, -22 * s, 14 * s, 28 * s), wash='#D9B45A', ink=INK, sw=.5)
    heart(330 * s, 0, 22 * s, HOT, key=key + 'h', sw=.6)
    pop()
    if glowK > .02:
        glow(x, y, 90 * glowK, '#FF9FBF', glowK)
        heart(x, y - 10, 22 * glowK, HOT, key=key + 'nh', sw=.6)


# ------------------------------------------------------------------ dream frame (S05 / S06)
def dreamFrame(k, t, key='df'):
    """puffy cloud border that opens in (k 0..1)"""
    if k <= .01:
        return
    p = backOut(k)
    for i in range(22):
        a = i / 22 * TAU
        rx, ry = 1040, 640
        cx, cy = W / 2 + math.cos(a) * rx / (1 + .0 * p), H / 2 + math.sin(a) * ry
        cx = W / 2 + (cx - W / 2) * lerp(.55, 1, p)
        cy = H / 2 + (cy - H / 2) * lerp(.55, 1, p)
        s = 56 + 14 * hash1(i)
        puff(cx, cy, s * (1 + .03 * math.sin(t * 2 + i)), col='#FFF6FA', key=f'{key}{i}', ink=True)
    sparkles(t, 13, 10, 60, 60, W - 60, H - 60, r=12, col='#FFFFFF')


def paperBoat(x, y, s, rot=0.0, key='boat', col='#FFFDF6', sail=True):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint([[-3.2 * s, -1.1 * s], [3.2 * s, -1.1 * s], [2.2 * s, .5 * s], [-2.2 * s, .5 * s]], wash=col, fill='#D9D2C2', fillOp=60, ink=INK, sw=1)
    if sail:
        paint([[-1.4 * s, -1.1 * s], [0, -3.4 * s], [1.4 * s, -1.1 * s]], wash=mixCol(col, '#F7B2C6', .4), ink=INK, sw=.9)
    else:
        paint([[2.2 * s, -1.1 * s], [3.4 * s, -2.4 * s], [3.2 * s, -1.1 * s]], wash=mixCol(col, '#F7B2C6', .4), ink=INK, sw=.9)
    inkLine([[-2.6 * s, -.5 * s], [2.6 * s, -.5 * s]], .4, '#9A90A0', 'inkfine', 0)
    pop()


def lighthouse(x, y, s, beam=0.0, key='lh'):
    """lighthouse standing at (x, y); beam = angle of the sweeping light (radians, 0 = pointing left)"""
    boilSeed(key)
    pts = [[x - 1.0 * s, y], [x - .62 * s, y - 5.2 * s], [x + .62 * s, y - 5.2 * s], [x + 1.0 * s, y]]
    paint(pts, wash='#FFFDF6', ink=INK, sw=1)
    for i in range(3):
        y0, y1 = y - (.6 + i * 1.6) * s, y - (1.3 + i * 1.6) * s
        f0, f1 = lerp(1.0, .62, (y - y0) / (5.2 * s)), lerp(1.0, .62, (y - y1) / (5.2 * s))
        paint([[x - f0 * s, y0], [x - f1 * s, y1], [x + f1 * s, y1], [x + f0 * s, y0]], wash='#E8476E', ink=None)
    paint(rectPts(x - .75 * s, y - 6.4 * s, 1.5 * s, 1.2 * s), wash='#FFE68A', ink=INK, sw=.9)
    paint([[x - .95 * s, y - 6.4 * s], [x, y - 7.4 * s], [x + .95 * s, y - 6.4 * s]], wash='#E8476E', ink=INK, sw=.9)
    paint(rectPts(x - 1.0 * s, y - 5.35 * s, 2.0 * s, .22 * s), wash='#3A3550', ink=None)
    lx, ly = x, y - 5.8 * s
    glow(lx, ly, 2.2 * s, '#FFE7A0', .9)
    if beam is not None:
        L = 14 * s
        a0, a1 = math.pi + beam - .12, math.pi + beam + .12
        p = skia.Path()
        p.moveTo(lx, ly)
        p.lineTo(lx + math.cos(a0) * L, ly + math.sin(a0) * L)
        p.lineTo(lx + math.cos(a1) * L, ly + math.sin(a1) * L)
        p.close()
        sh = skia.GradientShader.MakeRadial(skia.Point(lx, ly), L, [skcol('#FFF6C8', .55), skcol('#FFF6C8', 0)])
        G.c.drawPath(p, skia.Paint(AntiAlias=True, Shader=sh))


def pier(x0, x1, y, key='pier'):
    boilSeed(key)
    for px in range(int(x0) + 30, int(x1), 120):
        paint(rectPts(px - 10, y, 20, 150), wash='#7A5A48', ink=INK, sw=.7)
    paint(rectPts(x0, y - 22, x1 - x0, 30), wash='#C98B5A', fill='#9B6B45', fillOp=50, ink=INK, sw=1)
    for px in range(int(x0) + 40, int(x1), 60):
        G.c.drawLine(px, y - 20, px, y + 6, skia.Paint(AntiAlias=True, Color=skcol('#8A5A3C', .6), StrokeWidth=2))


# ------------------------------------------------------------------ tear-off calendar (S06)
def iceCream(x, y, s, key='ic'):
    boilSeed(key)
    paint([[x - .8 * s, y - 1.6 * s], [x + .8 * s, y - 1.6 * s], [x, y + .6 * s]], wash='#E8B46A', ink=INK, sw=.8)
    for i in range(3):
        inkLine([[x - .6 * s + i * .4 * s, y - 1.5 * s], [x + .1 * s + i * .25 * s, y - .3 * s]], .4, '#B8823A', 'inkfine', 0)
    paint(ellPts(x - .35 * s, y - 2.0 * s, .7 * s, .6 * s, 16), wash='#F7B2C6', ink=INK, sw=.8)
    paint(ellPts(x + .4 * s, y - 2.05 * s, .65 * s, .58 * s, 16), wash='#B8E3C8', ink=INK, sw=.8)
    paint(ellPts(x, y - 2.7 * s, .6 * s, .55 * s, 16), wash='#FFF3C8', ink=INK, sw=.8)
    paint(ellPts(x + .05 * s, y - 3.3 * s, .18 * s, .18 * s, 10), wash='#E8476E', ink=INK, sw=.5)


def catFace(x, y, s, key='cat'):
    boilSeed(key)
    paint(ellPts(x, y, 1.4 * s, 1.15 * s, 22), wash='#F4C27A', fill='#D9944A', fillOp=50, ink=INK, sw=.9)
    for sx in (-1, 1):
        paint([[x + sx * 1.25 * s, y - .35 * s], [x + sx * 1.0 * s, y - 1.6 * s], [x + sx * .35 * s, y - 1.0 * s]], wash='#F4C27A', ink=INK, sw=.8)
        G.c.drawCircle(x + sx * .5 * s, y - .1 * s, .14 * s, skia.Paint(AntiAlias=True, Color=skcol(INK)))
        for j in (-1, 1):
            inkLine([[x + sx * .9 * s, y + .25 * s], [x + sx * 1.9 * s, y + .25 * s + j * .25 * s]], .4, INK, 'inkfine', 0)
    inkLine([[x - .25 * s, y + .35 * s], [x, y + .5 * s], [x + .25 * s, y + .35 * s]], .6, INK, 'ink', .5)
    paint(ellPts(x, y + .22 * s, .12 * s, .08 * s, 8), wash='#E8476E', ink=None)


def calendarPad(x, y, w, h, page, t, key='cal', tear=None):
    """tear-off calendar centred at x, top y; page = (day, label, drawFn); tear = (page, k) flying off on top"""
    boilSeed(key)
    paint(rectPts(x - w / 2 + 12, y + 14, w, h), wash=INK, washOp=50, ink=None)
    paint(rectPts(x - w / 2 - 10, y - 10, w + 20, h + 14), wash='#E8476E', fill='#B8324F', fillOp=50, ink=INK, sw=1.1)

    def drawPage(pg, px, py, rot=0.0, a=1.0, curl=0.0):
        day, label, fn = pg
        push()
        translate(px, py)
        rotate(rot)
        boilSeed(key + day)
        paint(rectPts(-w / 2, 0, w, h - 10), wash='#FFFDF6', ink=INK, sw=.9)
        flatRect(-w / 2, 0, w, 90, '#FCE3EA')
        text(day, 0, 50, 58, HOT, shadow=False)
        fn(0, h * .52)
        text(label, 0, h - 70, 44, '#6A5A70', shadow=False, face=WENKAI)
        pop()
    drawPage(page, x, y)
    for i in range(6):
        rx = x - w / 2 + 40 + i * (w - 80) / 5
        paint(rrPts(rx - 8, y - 30, 16, 44, 8), wash='#C9C1D6', ink=INK, sw=.6)
    if tear:
        pg, k = tear
        if k < 1:
            ang = .5 * easeIn(k)
            drawPage(pg, x + 160 * k, y - 60 * math.sin(k * 3) - 1100 * easeIn(k), ang)


# ------------------------------------------------------------------ misc
def tvGlow(k, t, col='#7FB8FF'):
    fl = .85 + .15 * math.sin(t * 23) * math.sin(t * 7)
    G.c.save()
    G.c.resetMatrix()
    sh = skia.GradientShader.MakeLinear([skia.Point(0, OUT_H), skia.Point(0, OUT_H * .25)], [skcol(col, .38 * k * fl), skcol(col, 0)])
    pa = skia.Paint(Shader=sh)
    pa.setBlendMode(skia.BlendMode.kScreen)
    G.c.drawRect(skia.Rect.MakeXYWH(0, 0, OUT_W, OUT_H), pa)
    G.c.restore()


def gamepad(x, y, s, rot=0.0, key='gp', col='#E8E1D2'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rrPts(-1.4 * s, -.6 * s, 2.8 * s, 1.2 * s, .55 * s), wash=col, fill='#9A93A8', fillOp=50, ink=INK, sw=.8)
    flatRect(-1.0 * s, -.1 * s, .5 * s, .16 * s, INK)
    flatRect(-.83 * s, -.27 * s, .16 * s, .5 * s, INK)
    G.c.drawCircle(.8 * s, -.15 * s, .14 * s, skia.Paint(AntiAlias=True, Color=skcol(HOT)))
    G.c.drawCircle(1.05 * s, .1 * s, .14 * s, skia.Paint(AntiAlias=True, Color=skcol('#5B7FC4')))
    pop()


def popcorn(x, y, s, t, jumpTb=None, key='pop'):
    """striped bucket; kernels hop out at jumpTb"""
    boilSeed(key)
    a = (t - jumpTb) if jumpTb is not None else -1
    for i in range(9):
        kx = x + (hash1(i * 2.1) - .5) * 1.6 * s
        ky = y - 2.1 * s - hash1(i * 3.3) * .4 * s
        if 0 <= a < .7:
            h = (1.4 + hash1(i) * 1.6) * s
            ky -= h * math.sin(clamp(a / .55) * math.pi)
            kx += (hash1(i * 5.5) - .5) * 2 * s * clamp(a / .55)
        paint(ellPts(kx, ky, .34 * s, .3 * s, 10, s * .03), wash='#FFF6DA', ink=INK, sw=.5, lite=True)
    pts = [[x - 1.1 * s, y - 2.0 * s], [x + 1.1 * s, y - 2.0 * s], [x + .8 * s, y], [x - .8 * s, y]]
    paint(pts, wash='#FFFDF6', ink=INK, sw=.9)
    for i in range(3):
        k0 = (i * 2 + .5) / 6
        k1 = (i * 2 + 1.5) / 6
        paint([[lerp(-1.1, 1.1, k0) * s + x, y - 2 * s], [lerp(-1.1, 1.1, k1) * s + x, y - 2 * s],
               [lerp(-.8, .8, k1) * s + x, y], [lerp(-.8, .8, k0) * s + x, y]], wash='#E8476E', ink=None)
    paint(pts, ink=INK, sw=.9)


def candle(x, y, s, lit, t, key='cdl'):
    from props_chuanshao import flame
    boilSeed(key)
    paint(rectPts(x - .35 * s, y - 2.6 * s, .7 * s, 2.6 * s), wash='#FFF6E2', fill='#E8D8B8', fillOp=50, ink=INK, sw=.7)
    paint(ellPts(x, y, .9 * s, .25 * s, 14), wash='#D9B45A', ink=INK, sw=.6)
    inkLine([[x, y - 2.6 * s], [x, y - 2.95 * s]], .5, INK, 'inkfine', 0)
    if lit > .02:
        glow(x, y - 3.2 * s, 5.5 * s * lit, '#FFC766', .9 * lit)
        flame(x, y - 2.85 * s, .9 * s, t, key=key + 'f', k=backOut(lit))


def heartEgg(x, y, s, key='egg'):
    boilSeed(key)
    pts = []
    for i in range(18):
        a = i / 18 * TAU
        r = 1 + .14 * math.sin(a * 3 + 1)
        pts.append([x + math.cos(a) * 2.2 * s * r, y + math.sin(a) * 1.0 * s * r])
    paint(pts, wash='#FFFDF6', ink=INK, sw=.8, curv=.4)
    paint(heartPts(x, y - .1 * s, .75 * s, 20), wash='#F6B73C', fill='#E0952A', fillOp=60, ink=INK, sw=.7)
    paint(ellPts(x - .3 * s, y - .35 * s, .14 * s, .1 * s, 8), wash='#FFFFFF', washOp=200, ink=None)


def plate(x, y, s, key='plt'):
    boilSeed(key)
    paint(ellPts(x, y, 2.9 * s, 1.15 * s, 26), wash='#FFFFFF', ink=INK, sw=.9)
    paint(ellPts(x, y, 2.2 * s, .82 * s, 24), wash='#F4F0E8', ink=None)


def snowGlobe(x, y, r, t, key='sg', shine=0.0, tilt=0.0):
    """snow globe; (x, y) = centre of the sphere. inside: tiny him and her side by side"""
    push()
    translate(x, y)
    rotate(tilt)
    boilSeed(key)
    paint([[-r * .95, r * .75], [r * .95, r * .75], [r * .8, r * 1.3], [-r * .8, r * 1.3]], wash='#B9784E', fill='#8A5A3C', fillOp=50, ink=INK, sw=1)
    text('好朋友', 0, r * 1.02, r * .34, '#FFF3E2', stroke=INK, strokeW=r * .03, shadow=False)
    G.c.save()
    pth = skia.Path()
    pth.addCircle(0, 0, r)
    G.c.clipPath(pth, skia.ClipOp.kIntersect, True)
    gradRect(-r, -r, 2 * r, 2 * r, ['#CFE8F8', '#F6E6F0'])
    flatRect(-r, r * .45, 2 * r, r, '#FFFFFF', .9)
    u = r / 11
    her(-r * .32, r * .52, u, dict(eyes='happy', mouth='smile', blush=.5, lite=True, noShadow=True, boilKey=key + 'h', aR=.6))
    him(r * .32, r * .52, u, dict(eyes='happy', mouth='smile', blush=.3, lite=True, noShadow=True, boilKey=key + 'm', aL=.6, flip=True))
    for i in range(26):
        ph = frac(t * (.12 + .08 * hash1(i)) + hash1(i * 3.3))
        sx = (hash1(i * 7.1) - .5) * 1.8 * r + math.sin(t * 1.5 + i) * r * .08
        sy = lerp(-r, r * .5, ph)
        G.c.drawCircle(sx, sy, r * .025 + 2, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .9)))
    G.c.restore()
    paint(ellPts(0, 0, r, r, 40), wash='#DDEFFF', washOp=60, ink=INK, sw=1.1)
    paint(ellPts(-r * .42, -r * .45, r * .22, r * .12, 14, 0, -.7), wash='#FFFFFF', washOp=200, ink=None)
    pop()
    if shine > .02:
        sparkle(x + r * .6, y - r * .7, 26 * shine, '#FFFFFF', shine)
        sparkle(x - r * .7, y - r * .1, 18 * shine, '#FFFFFF', shine)


def quizCard(x, y, w, h, title, opts, key='qz'):
    boilSeed(key)
    paint(rectPts(x + 14, y + 16, w, h), wash=INK, washOp=50, ink=None)
    paint(rrPts(x, y, w, h, 26), wash='#FFFDF6', ink=INK, sw=1.2)
    flatRect(x + 20, y + 20, w - 40, 104, '#FCE3EA')
    text(title, x + w / 2, y + 72, 58, HOT, shadow=False)
    out = []
    for i, (lt, txt) in enumerate(opts):
        yy = y + 190 + i * ((h - 230) / len(opts))
        rr(x + 40, yy - 48, w - 80, 92, 22, '#F4F0FA', ink=INK, sw=.7, key=f'{key}o{i}')
        paint(ellPts(x + 100, yy - 2, 30, 30, 16), wash='#B79BE0', ink=INK, sw=.6)
        text(lt, x + 100, yy - 2, 38, '#FFFFFF', shadow=False)
        text(txt, x + 160, yy - 2, 58, INK, align='left', shadow=False)
        out.append((x + w / 2, yy - 2))
    return out


# ------------------------------------------------------------------ the user's signature watermark next to every title (你的署名)
from mv_config import load_signature


def signature(x, y, size=44, a=.92, rot=-.06, col='#FFFFFF'):
    SIGN = load_signature().lstrip('★')
    """small hand-lettered signature with a little star, placed beside the song title"""
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
