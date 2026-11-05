# hb.py: props, looks and helpers for 《100》 (Tizzy T). 疑心病 Clawd couple: him clay + headphones (verse),
# her pink + white flower; in the chorus they grow old together (white fluffy hair, round glasses, canes, desaturated colours).
import math
from eng import *
import eng
import clawd as _cl
from clawd import *
from props import puff, sparkle, sparkles, floatHearts, bubble, stamp, sunburst, stripes
from ch import rr, heart, HOT, PINK, PINKDK, CREAM, WENKAI, fo
from common import *
import sets2, nm
from hl import wtext

PAPER = '#FFFBF0'
OLDPAPER = '#F1E2BE'
NOTE = '#2B2233'


# ------------------------------------------------------------------ calendar: today is Sunday 2026-11-01
def calendar11(x, y, key='cal'):
    boilSeed(key)
    paint(rectPts(x, y, 190, 220), wash='#FFFDF6', ink=INK, sw=.8, lite=True)
    paint(rectPts(x, y, 190, 54), wash='#C8564F', ink=INK, sw=.6, lite=True)
    text('11月', x + 95, y + 28, 32, '#FFF6E8', face=WENKAI, shadow=False)
    for r in range(5):
        for c in range(7):
            if r == 0 and c < 6:
                continue
            cx, cy = x + 18 + c * 26, y + 74 + r * 30
            G.c.drawCircle(cx, cy, 3, skia.Paint(AntiAlias=True, Color=skcol('#8A7A88', .7)))
    cx, cy = x + 18 + 6 * 26, y + 74            # Sunday the 1st, circled
    G.c.drawCircle(cx, cy, 13, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skcol('#C8564F')))
    G.c.drawCircle(x + 95, y - 6, 6, skia.Paint(AntiAlias=True, Color=skcol(INK)))


sets2.wallCalendar = calendar11
nm.wallCalendar = calendar11


# ------------------------------------------------------------------ looks: extra "hats" (white hair, snow, beanie-with-snow)
_hat0 = _cl.hat


def _whiteHair(u, sw, k=1.0):
    if k <= .01:
        return
    boilSeed('whair')
    pts = [(-4.6, -8.0, 1.05), (-3.0, -8.55, 1.15), (-1.0, -8.75, 1.2), (1.0, -8.75, 1.2), (3.0, -8.55, 1.15), (4.6, -8.0, 1.05),
           (-5.2, -7.0, .8), (5.2, -7.0, .8)]
    for (px, py, r) in pts:
        rr_ = r * u * k
        paint(ellPts(px * u, py * u + (1 - k) * .8 * u, rr_, rr_ * .82, 14), wash='#FBF8F2', fill='#D9D3DC', fillOp=70, ink=INK, sw=sw * .55)
    for (px, py, r) in pts[:6]:
        paint(ellPts(px * u - .25 * u, py * u - .3 * u, r * u * .45 * k, r * u * .3 * k, 10), wash='#FFFFFF', ink=None)


def _snowCap(u, sw, k):
    if k <= .01:
        return
    boilSeed('snowcap')
    h = 1.6 * k
    pts = [[-5.1 * u, -7.9 * u]]
    n = 9
    for i in range(n + 1):
        f = i / n
        x = lerp(-5.0, 5.0, f) * u
        y = (-7.9 - h * (.75 + .25 * math.sin(f * math.pi)) - .25 * k * math.sin(f * 17)) * u
        pts.append([x, y])
    pts.append([5.1 * u, -7.9 * u])
    paint(pts, wash='#FFFFFF', fill='#CFE0F2', fillOp=80, ink=INK, sw=sw * .5)


def _beanie(u, sw, col='#D9534F'):
    boilSeed('beanie2')
    paint([[-5.2 * u, -7.4 * u], [-4.8 * u, -10.2 * u], [0, -11.4 * u], [4.8 * u, -10.2 * u], [5.2 * u, -7.4 * u]], wash=col,
          fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=sw * .8, curv=.5)
    paint(rrPts(-5.5 * u, -8.3 * u, 11 * u, 1.5 * u, .5 * u), wash='#FFF3E2', ink=INK, sw=sw * .7)
    for i in range(6):
        x = (-4.4 + i * 1.75) * u
        inkLine([[x, -8.15 * u], [x, -6.95 * u]], sw * .4, '#C9B79A', 'inkfine', 0)
    paint(ellPts(0, -11.6 * u, 1.1 * u, 1.1 * u, 14), wash='#FFF3E2', ink=INK, sw=sw * .6)


def _hat(u, h, sw, o=None):
    o = o or {}
    if h == 'whitehair':
        _whiteHair(u, sw, o.get('hairK', 1.0))
    elif h == 'snow':
        _snowCap(u, sw, o.get('snowK', 0.0))
    elif h == 'beanieR':
        _beanie(u, sw, '#D9534F')
    elif h == 'beanieB':
        _beanie(u, sw, '#5B7FC4')
    elif h == 'snowhat':                    # snow piled on a beanie
        if o.get('snowK', 0) > .01:
            push()
            translate(0, -3.2 * u)
            scale(.9, 1)
            _snowCap(u, sw, o.get('snowK', 0.0))
            pop()
    else:
        _hat0(u, h, sw, o)


_cl.hat = _hat


def glassesDraw(view='front', col=INK):
    F = VIEWS[view]['face']

    def d(u, sw):
        if not F:
            return
        xs = [F['cx'] * u + s * 2.5 * u * F['fw'] for s in F['sides']]
        for x in xs:
            G.c.drawCircle(x, -5.95 * u, 1.25 * u * (F['fw'] ** .3),
                           skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .22)))
            G.c.drawCircle(x, -5.95 * u, 1.25 * u * (F['fw'] ** .3),
                           skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.5, u * .16), Color=skcol(col)))
        if len(xs) == 2:
            inkLine([[xs[0] + 1.2 * u * F['fw'] ** .3, -6.1 * u], [xs[1] - 1.2 * u * F['fw'] ** .3, -6.1 * u]], sw * .6, col, 'inkfine', .4)
    return d


OLD_ME = dict(col=mixCol(PAL['clay'], '#B9AFB4', .28), dk=mixCol(PAL['clayDk'], '#8E8590', .28), lt=mixCol('#F5B394', '#E6DEE0', .3))
OLD_HER = dict(col=mixCol('#EE9AAE', '#C9BFC6', .25), dk=mixCol('#C0637B', '#9B8F98', .25), lt=mixCol('#FBD0DA', '#EFE8EA', .3))


def emM(t, keys, **kw):
    o = emotions(t, keys, ME)
    o.update(kw)
    return o


def emH(t, keys, **kw):
    o = emotions(t, keys, HER)
    o.update(kw)
    return o


def emMo(t, keys, **kw):
    o = emotions(t, keys, OLD_ME)
    o.update(kw)
    return o


def emHo(t, keys, **kw):
    o = emotions(t, keys, OLD_HER)
    o.update(kw)
    return o


def himH(x, y, u, o=None):
    """him in the verse: the songwriter with his headphones on"""
    o = dict(o or {})
    o.setdefault('hat', 'headphones')
    him(x, y, u, o)


def _oldO(o, base, extra_hats=()):
    o = dict(o or {})
    for k_, v in base.items():
        o.setdefault(k_, v)
    hats = o.get('hat')
    hl_ = ['whitehair'] + list(extra_hats)
    if hats:
        hl_ += list(hats) if isinstance(hats, (list, tuple)) else [hats]
    if o.get('nohair'):
        hl_.remove('whitehair')
    o['hat'] = hl_
    if not o.get('noGlasses'):
        g0 = o.get('draw')
        gd = glassesDraw(o.get('view') or 'front')

        def dd(u, sw):
            gd(u, sw)
            if g0:
                g0(u, sw)
        o['draw'] = dd
    return o


def himOld(x, y, u, o=None):
    o = _oldO(o, OLD_ME)
    o.setdefault('boilKey', 'himold')
    clawd(x, y, u, o)


def herOld(x, y, u, o=None):
    o = dict(o or {})
    hats = o.get('hat')
    o['hat'] = (list(hats) if isinstance(hats, (list, tuple)) else ([hats] if hats else [])) + ['flower']
    o = _oldO(o, OLD_HER)
    o.setdefault('boilKey', 'herold')
    clawd(x, y, u, o)


def caneAt(x, ground, top, d=1, w=9.0, col='#8A5A3C', key='cane', lean=0.0):
    """a walking stick standing on the ground at x, its hook at `top`, curling toward d (1 = right)"""
    p = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w + 5, Color=skcol(INK), StrokeCap=skia.Paint.kRound_Cap)
    q = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=skcol(col), StrokeCap=skia.Paint.kRound_Cap)
    tx = x + lean * (ground - top)
    r = w * 2.4
    pa = skia.Path()
    pa.moveTo(x, ground)
    pa.lineTo(tx, top + r)
    pa.cubicTo(tx, top - r * .4, tx + d * r * 2, top - r * .4, tx + d * r * 2, top + r * .6)
    G.c.drawPath(pa, p)
    G.c.drawPath(pa, q)
    G.c.drawCircle(x, ground, w * .55, skia.Paint(AntiAlias=True, Color=skcol(INK)))


def cane(x, y, u, o, ground, side='R', col='#8A5A3C', key='cane'):
    """walking stick held in the hand (world coords): hook at the hand, foot on the ground"""
    hx, hy = handXY(x, y, u, o, side)
    d = -1 if o.get('flip') else 1
    caneAt(hx + d * .3 * u, ground, hy - .4 * u, -d, max(5.0, u * .28), col, key)


def hitK(t, k, d=.12):
    """1 on the beat frame, decaying after"""
    a = t - (B[k] - .04)
    return 0.0 if a < 0 else math.exp(-a / d)


def landK(t, k, d=.16):
    """0..1 progress that reaches 1 on beat k (motion that arrives on the beat)"""
    return clamp((t - (B[k] - d)) / d)


def ek(k):
    """emotion key a little before the beat so the new face is fully there on the beat frame"""
    return B[k] - .06


def popIn(t, k, d=.14):
    return backOut(clamp((t - (B[k] - .04)) / d))


def bg(col):
    flatRect(-400, -400, W + 800, H + 800, col)


def line(x0, y0, x1, y1, col, a=1.0, w=2.0):
    p = skia.Paint(AntiAlias=True, Color=skcol(col, a), StrokeWidth=w, Style=skia.Paint.kStroke_Style)
    p.setStrokeCap(skia.Paint.kRound_Cap)
    G.c.drawLine(x0, y0, x1, y1, p)


def dot(x, y, r, col, a=1.0):
    G.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=skcol(col, a)))


def ring(x, y, r, col, w=3.0, a=1.0):
    G.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, Color=skcol(col, a)))


# ------------------------------------------------------------------ music notes
def note(x, y, s, col=NOTE, kind=1, rot=0.0, a=1.0, key='nt'):
    """an eighth note (kind 1) or two beamed eighths (kind 2); (x, y) = centre of the (first) head; s = head width"""
    if a <= .01 or s <= 1:
        return
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    heads = [(0, 0)] if kind == 1 else [(0, 0), (s * 1.5, -s * .35)]
    for hx, hy in heads:
        paint(ellPts(hx, hy, s * .62, s * .46, 14, 0, -.35), wash=col, washOp=int(255 * a), ink=INK if a > .5 else None, sw=.6)
    w = max(2.5, s * .16)
    p = skia.Paint(AntiAlias=True, Color=skcol(col if col != NOTE else INK, a), StrokeWidth=w, Style=skia.Paint.kStroke_Style)
    for hx, hy in heads:
        G.c.drawLine(hx + s * .55, hy - s * .1, hx + s * .55, hy - s * 2.3, p)
    if kind == 1:
        pa = skia.Path()
        pa.moveTo(s * .55, -s * 2.3)
        pa.cubicTo(s * 1.3, -s * 1.9, s * 1.4, -s * 1.3, s * 1.0, -s * .9)
        G.c.drawPath(pa, p)
    else:
        q = skia.Paint(AntiAlias=True, Color=skcol(col if col != NOTE else INK, a))
        pa = skia.Path()
        pa.moveTo(s * .55 - w / 2, -s * 2.3)
        pa.lineTo(s * 2.05 + w / 2, -s * 2.65)
        pa.lineTo(s * 2.05 + w / 2, -s * 2.25)
        pa.lineTo(s * .55 - w / 2, -s * 1.9)
        pa.close()
        G.c.drawPath(pa, q)
    pop()


NOTE_COLS = ['#E8476E', '#F2A65A', '#5B7FC4', '#3FA37A', '#9B6BC9']


def noteStream(t, t0, x0, y0, x1, y1, n, s=26, arc=-120, dur=1.0, key='ns', cols=None, wob=14):
    """n notes flying from (x0, y0) to (x1, y1) along an arc, released from t0 one after another"""
    cols = cols or NOTE_COLS
    for i in range(n):
        ti = t0 + i * dur * .18
        f = (t - ti) / dur
        if f < 0 or f > 1.15:
            continue
        f2 = clamp(f)
        x = lerp(x0, x1, f2)
        y = lerp(y0, y1, f2) + arc * math.sin(f2 * math.pi) + wob * math.sin(t * 9 + i)
        a = clamp(f * 6) * (1 - seg(f, .9, 1.15))
        note(x, y, s * (.8 + .4 * hash1(i * 7.1)), cols[i % len(cols)], 1 + (i % 3 == 2), rot=.25 * math.sin(t * 6 + i), a=a, key=f'{key}{i}')


# ------------------------------------------------------------------ top-down desk + notebook (S01 / S05 / S24 / S32)
def woodTop(old=0.0, key='wood'):
    gradRect(-300, -300, W + 600, H + 600, [mixCol('#B57A4A', '#8F6A50', old), mixCol('#8A5634', '#6E5444', old)])
    boilSeed(key)
    for i in range(22):
        y = -100 + i * 62 + 10 * math.sin(i * 1.7)
        inkLine([[-200, y], [700, y + 12 * math.sin(i)], [1400, y - 8], [W + 200, y + 6]], .35, '#5E3A22', 'inkfine', .6)


def notebook(cx, cy, w, h, old=0.0, key='nbk', rule=True):
    """open spiral notebook seen from above; returns ((lx, ly, lw, lh), (rx, ry, rw, rh)) page rects"""
    boilSeed(key)
    pc = mixCol(PAPER, OLDPAPER, old)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(cx - w / 2 + 20, cy - h / 2 + 26, w, h), 18, 18, skia.Paint(AntiAlias=True, Color=skcol(INK, .3)))
    paint(rrPts(cx - w / 2 - 14, cy - h / 2 - 12, w + 28, h + 24, 18), wash=mixCol('#5B7FC4', '#7E7A8C', old * .6), ink=INK, sw=1.0)
    gap = 26
    pw = (w - gap) / 2
    L = (cx - w / 2, cy - h / 2, pw, h)
    Rr = (cx + gap / 2, cy - h / 2, pw, h)
    for (x, y, ww, hh) in (L, Rr):
        paint(rectPts(x, y, ww, hh, 1), wash=pc, ink=INK, sw=.8)
        if rule:
            for i in range(1, 15):
                yy = y + 70 + i * (hh - 90) / 15
                G.c.drawLine(x + 24, yy, x + ww - 24, yy, skia.Paint(AntiAlias=True, Color=skcol('#9EC3E8', .5 - .25 * old), StrokeWidth=2))
            G.c.drawLine(x + 70, y + 10, x + 70, y + hh - 10, skia.Paint(AntiAlias=True, Color=skcol('#F29AA8', .45 - .2 * old), StrokeWidth=2))
        if old > .05:
            G.c.drawCircle(x + ww * .8, y + hh * .82, 70, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=9,
                                                                    Color=skcol('#B88A62', .25 * old)))
    # spiral rings
    for i in range(12):
        yy = cy - h / 2 + 40 + i * (h - 80) / 11
        G.c.drawRoundRect(skia.Rect.MakeXYWH(cx - 26, yy - 9, 52, 18), 9, 9,
                          skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=5, Color=skcol('#8E93A6')))
    return L, Rr


def handText(txt, x, y, size, prog, col=INK, face=WENKAI, align='center', rot=0.0, pen=True):
    """hand-written reveal: the line appears left→right up to prog (0..1), with a small nib at the edge"""
    if prog <= 0:
        return
    w = textW(txt, size, face)
    x0 = x - w / 2 if align == 'center' else x
    push()
    translate(x0, y)
    rotate(rot)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(-10, -size, (w + 20) * clamp(prog), size * 2))
    text(txt, w / 2, 0, size, col, face=face, shadow=False)
    G.c.restore()
    if pen and prog < 1:
        nx = (w + 10) * prog
        penNib(nx, size * .1, size * .9)
    pop()


def penNib(x, y, s):
    """a fountain pen lying with its nib at (x, y) (no hand — the pen writes by itself)"""
    push()
    translate(x, y)
    rotate(-.75)
    boilSeed('nib')
    paint([[0, 0], [s * .3, -s * .18], [s * .3, s * .18]], wash='#C9A13A', ink=INK, sw=.6)
    paint(rrPts(s * .28, -s * .2, s * 2.6, s * .4, s * .15), wash='#2E3A6E', ink=INK, sw=.7)
    paint(rrPts(s * 1.2, -s * .22, s * .3, s * .44, s * .05), wash='#C9A13A', ink=None)
    pop()


def doodleHeart(x, y, r, col=HOT, k=1.0, key='dh'):
    if k <= .01:
        return
    boilSeed(key)
    pts = heartPts(x, y, r * backOut(k), 24)
    inkLine(pts + [pts[0]], 1.2, col, 'ink', .5)


def topLamp(x, y, on=1.0, key='tl'):
    """desk lamp from above: a pool of warm light + the lamp shade"""
    if on > .01:
        glow(x + 300, y + 220, 1000, '#FFD98A', .75 * on)
        glow(x + 60, y + 60, 260, '#FFF2C2', .8 * on)
    boilSeed(key)
    paint(ellPts(x, y, 120, 120, 30), wash='#E8E1D2', fill='#B9B0A0', fillOp=80, ink=INK, sw=1.0)
    paint(ellPts(x, y, 84, 84, 26), wash='#CFC6B6', ink=INK, sw=.5)
    paint(ellPts(x + 6, y + 6, 46, 46, 20), wash=mixCol('#8E8676', '#FFF2C2', on), ink=None)


def headphonesTop(x, y, s, rot=0.0, key='hpt'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    pa = skia.Path()
    pa.addArc(skia.Rect.MakeXYWH(-s, -s * .9, 2 * s, 1.8 * s), 200, 140)
    G.c.drawPath(pa, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=s * .16, Color=skcol(INK)))
    for sx in (-1, 1):
        paint(rrPts(sx * s * .95 - s * .28, -s * .05, s * .56, s * .8, s * .2), wash=PAL['violet'], fill=PAL['rose'], fillOp=50, ink=INK, sw=.8)
    pop()


def cassette(x, y, s, label='', rot=0.0, spin=0.0, key='cs', col='#3D3A52', labelCol='#FFF3E2', heartIn=0.0, a=1.0):
    """a cassette tape centred at (x, y), s = width"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    h = s * .63
    paint(rrPts(-s / 2, -h / 2, s, h, s * .05), wash=col, fill=mixCol(col, INK, .4), fillOp=60, ink=INK, sw=1.1)
    paint(rrPts(-s * .43, -h * .4, s * .86, h * .5, s * .03), wash=labelCol, ink=INK, sw=.7)
    G.c.drawRect(skia.Rect.MakeXYWH(-s * .43, -h * .4, s * .86, h * .1), skia.Paint(AntiAlias=True, Color=skcol(HOT, .85)))
    if label:
        text(label, 0, -h * .2, s * .1, INK, face=WENKAI, shadow=False)
    # window with reels
    paint(rrPts(-s * .3, h * .02, s * .6, h * .22, s * .04), wash='#2A2638', ink=INK, sw=.6)
    for sx in (-1, 1):
        cx_, cy_ = sx * s * .19, h * .13
        G.c.drawCircle(cx_, cy_, s * .075, skia.Paint(AntiAlias=True, Color=skcol('#F3EBDC')))
        for i in range(6):
            ang = spin * TAU + i / 6 * TAU
            G.c.drawLine(cx_, cy_, cx_ + math.cos(ang) * s * .06, cy_ + math.sin(ang) * s * .06,
                         skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=max(1.5, s * .012)))
    if heartIn > .01:
        glow(0, h * .13, s * .25, '#FF8FB0', .8 * heartIn)
        heart(0, h * .13, s * .06 * heartIn, '#FF6F96', key=key + 'h', sw=.4)
    paint(rrPts(-s * .35, h * .32, s * .7, h * .14, s * .02), wash=mixCol(col, '#FFFFFF', .15), ink=INK, sw=.5)
    pop()


def tapeDeck(x, y, s, play=0.0, lit=0.0, key='td', col='#E8E1D2', tape=None):
    """front-facing portable cassette player, (x, y) = bottom centre, s = width; play = ▶ pressed amount"""
    boilSeed(key)
    h = s * .62
    paint(rrPts(x - s / 2, y - h, s, h, s * .06), wash=col, fill=mixCol(col, INK, .25), fillOp=60, ink=INK, sw=1.1)
    inkLine([[x - s * .35, y - h], [x - s * .3, y - h - s * .14], [x + s * .3, y - h - s * .14], [x + s * .35, y - h]], 1.0, INK, 'ink', .4)
    # speakers
    for sx in (-1, 1):
        cx_, cy_ = x + sx * s * .3, y - h * .42
        paint(ellPts(cx_, cy_, s * .14, s * .14, 20), wash='#4A4760', ink=INK, sw=.8)
        for r in (s * .1, s * .06):
            ring(cx_, cy_, r, '#2B2233', 2)
    # tape window
    paint(rrPts(x - s * .13, y - h * .7, s * .26, h * .42, s * .02), wash='#2A2638', ink=INK, sw=.6)
    if tape:
        tape(x, y - h * .5, s * .22)
    # buttons
    for i, lab in enumerate(['◀◀', '▶', '■', '▶▶']):
        bx = x - s * .27 + i * s * .18
        down = play * 6 if lab == '▶' else 0
        paint(rrPts(bx - s * .07, y - h - s * .03 + down, s * .14, s * .05, 4), wash=('#6FD38A' if (lab == '▶' and lit > .5) else '#C9C1D6'),
              ink=INK, sw=.5)
    if lit > .01:
        glow(x - s * .27 + s * .18, y - h - s * .01, s * .12, '#7CF29A', .6 * lit)


# ------------------------------------------------------------------ verse props
def musicStand(x, y, w, h, key='ms'):
    """music stand: (x, y) = floor point; returns the sheet rect (sx, sy, sw, sh)"""
    boilSeed(key)
    sy = y - h
    inkLine([[x, y], [x, sy + w * .55]], 2.4, '#4A4760', 'ink', 0)
    for d in (-1, 1):
        inkLine([[x, y - 60], [x + d * 90, y]], 1.8, '#4A4760', 'ink', 0)
    paint(rectPts(x - w / 2, sy, w, w * .72), wash='#4A4760', ink=INK, sw=.9)
    sx, sy2, sw_, sh = x - w / 2 + 14, sy - 30, w - 28, w * .72 + 10
    return sx, sy2, sw_, sh


def staffPaper(x, y, w, h, key='sp', title=None):
    boilSeed(key)
    paint(rectPts(x, y, w, h, 1), wash=PAPER, ink=INK, sw=.8)
    gaps = []
    for s_ in range(3):
        y0 = y + 70 + s_ * (h - 90) / 3
        for i in range(5):
            yy = y0 + i * 14
            G.c.drawLine(x + 20, yy, x + w - 20, yy, skia.Paint(AntiAlias=True, Color=skcol('#6A5A70', .7), StrokeWidth=2))
        gaps.append(y0)
    if title:
        text(title, x + w / 2, y + 34, 30, INK, face=WENKAI, shadow=False)
    return gaps


def boombox(x, y, s, beat=0.0, key='bb', col='#3D3A52'):
    """boombox centred at (x, y), s = width; beat (0..1) pumps the speaker cones"""
    boilSeed(key)
    h = s * .55
    inkLine([[x - s * .32, y - h / 2], [x - s * .28, y - h / 2 - s * .16], [x + s * .28, y - h / 2 - s * .16], [x + s * .32, y - h / 2]],
            max(2.0, s * .02), INK, 'ink', .4)
    paint(rrPts(x - s / 2, y - h / 2, s, h, s * .06), wash=col, fill=mixCol(col, INK, .4), fillOp=60, ink=INK, sw=1.0)
    for sx in (-1, 1):
        cx_ = x + sx * s * .29
        r = s * .17 * (1 + .12 * beat)
        paint(ellPts(cx_, y + h * .05, r, r, 22), wash='#22202E', ink=INK, sw=.8)
        paint(ellPts(cx_, y + h * .05, r * .45, r * .45, 14), wash='#5A5670', ink=INK, sw=.5)
    paint(rrPts(x - s * .1, y - h * .3, s * .2, h * .3, 6), wash='#7FC6E8', ink=INK, sw=.5)
    for i in range(3):
        G.c.drawCircle(x - s * .06 + i * s * .06, y + h * .25, s * .018, skia.Paint(AntiAlias=True, Color=skcol(HOT if i == 0 else '#F2C53D')))


def bassRings(x, y, age, n=3, col='#FFFFFF', maxR=520, a=.8):
    for i in range(n):
        r = 80 + (age * 1100 - i * 130)
        if 60 < r < maxR:
            ring(x, y, r, col, 7, a * (1 - r / maxR))


def drum808(x, y, w, t, lit=1.0, beatK=0.0, key='808', grey=0.0):
    """drum machine centred at (x, y), w wide. Pads blink in a running pattern while lit."""
    boilSeed(key)
    h = w * .48
    body = mixCol('#E8E1D2', '#A9A3AE', grey)
    paint(rrPts(x - w / 2, y - h / 2, w, h, 14), wash=body, fill=mixCol(body, INK, .25), fillOp=60, ink=INK, sw=1.1)
    paint(rectPts(x - w / 2 + 16, y - h / 2 + 16, w * .42, h * .3), wash=mixCol('#2B2233', '#77717E', grey), ink=INK, sw=.6)
    text('808', x - w / 2 + 16 + w * .21, y - h / 2 + 16 + h * .15, h * .22, mixCol('#FF7A5C', '#BDB6C2', grey), shadow=False)
    for i in range(3):
        kx = x + w * .14 + i * w * .11
        paint(ellPts(kx, y - h * .26, w * .035, w * .035, 14), wash=mixCol('#F2A65A', '#9E98A4', grey), ink=INK, sw=.5)
    cols = ['#E8476E', '#F2A65A', '#F2C53D', '#FFFDF6']
    step = int(bpOf(t) * 2) % 16 if lit > .5 else -1
    for i in range(16):
        px = x - w / 2 + 24 + i * (w - 48) / 16
        c = cols[i // 4]
        on = (i == step) or (i % 4 == 0 and beatK > .3)
        paint(rrPts(px + 3, y + h * .08, (w - 48) / 16 - 6, h * .26, 5), wash=mixCol(c, '#9E98A4', grey) if not on else '#FFFFFF', ink=INK, sw=.5)
        if on and lit > .5:
            glow(px + (w - 48) / 32, y + h * .21, 34, c, .7)


def bigX(x, y, s, k=1.0, col='#E0344E', age=0.0):
    if k <= .01:
        return
    sc = 1 + .5 * (1 - easeOut(k)) + .05 * math.exp(-age * 10) * math.cos(age * 40)
    push()
    translate(x, y)
    scale(sc)
    rotate(-.06)
    for d in (-1, 1):
        inkLine([[-s, -s * d], [s, s * d]], s * .028 + 3, col, 'dry', 0)
        G.c.drawLine(-s, -s * d, s, s * d, skia.Paint(AntiAlias=True, Color=skcol(col, .9 * k), StrokeWidth=s * .2, StrokeCap=skia.Paint.kRound_Cap))
    pop()


def micStand(x, y, h, key='mic', col='#3D3A52'):
    """floor mic stand, (x, y) = floor; returns mic head (mx, my)"""
    boilSeed(key)
    inkLine([[x, y], [x, y - h]], 2.6, col, 'ink', 0)
    for d in (-1, 0, 1):
        inkLine([[x, y - 40], [x + d * 70, y]], 2.0, col, 'ink', 0)
    mx, my = x - 26, y - h - 34
    inkLine([[x, y - h], [mx + 10, my + 18]], 2.0, col, 'ink', 0)
    paint(rrPts(mx - 18, my - 40, 36, 66, 18), wash='#C9C1D6', fill='#8E89A0', fillOp=60, ink=INK, sw=.8)
    for i in range(4):
        G.c.drawLine(mx - 14, my - 30 + i * 12, mx + 14, my - 30 + i * 12, skia.Paint(AntiAlias=True, Color=skcol('#6A647A', .7), StrokeWidth=2))
    return mx, my - 10


def handMic(x, y, s, ang=-1.0, key='hm'):
    """a handheld mic whose grip end is at (x, y), pointing at ang"""
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    paint(rrPts(0, -s * .14, s * 1.1, s * .28, s * .1), wash='#3D3A52', ink=INK, sw=.7)
    paint(ellPts(s * 1.3, 0, s * .32, s * .32, 16), wash='#C9C1D6', fill='#8E89A0', fillOp=60, ink=INK, sw=.7)
    pop()


def guitar(x, y, s, ang=-.5, key='gtr', strum=0.0, snap=0.0, t=0.0):
    """acoustic guitar, body centre (x, y), neck going up-right at ang; strum vibrates the strings; snap curls one string"""
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    # neck + head
    paint(rectPts(s * .7, -s * .09, s * 1.55, s * .18), wash='#6B4A3E', ink=INK, sw=.8)
    paint(rrPts(s * 2.2, -s * .14, s * .38, s * .28, s * .05), wash='#4A3229', ink=INK, sw=.7)
    for i in range(1, 7):
        G.c.drawLine(s * (.7 + i * .2), -s * .09, s * (.7 + i * .2), s * .09, skia.Paint(AntiAlias=True, Color=skcol('#D9C9A8'), StrokeWidth=2))
    # body (figure-8)
    paint(ellPts(s * .1, 0, s * .52, s * .46, 26), wash='#E0A35C', fill='#B8733A', fillOp=70, ink=INK, sw=1.0)
    paint(ellPts(-s * .42, 0, s * .62, s * .56, 26), wash='#E0A35C', fill='#B8733A', fillOp=70, ink=INK, sw=1.0)
    paint(ellPts(-s * .02, 0, s * .18, s * .18, 18), wash='#3A2620', ink=INK, sw=.6)
    paint(rectPts(-s * .62, -s * .16, s * .1, s * .32), wash='#4A3229', ink=INK, sw=.5)
    # strings
    for i in range(4):
        yy = (-1.5 + i) * s * .045
        vib = strum * 6 * math.sin(t * 90 + i)
        if snap > .01 and i == 3:
            pa = skia.Path()
            pa.moveTo(s * 2.25, yy)
            pa.cubicTo(s * 1.6, yy, s * 1.3, yy + s * .5 * snap, s * 1.1, yy + s * .7 * snap)
            G.c.drawPath(pa, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2, Color=skcol('#F3EBDC')))
            pa2 = skia.Path()
            pa2.moveTo(-s * .57, yy)
            pa2.cubicTo(-s * .2, yy, 0, yy - s * .3 * snap, s * .2, yy - s * .5 * snap)
            G.c.drawPath(pa2, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2, Color=skcol('#F3EBDC')))
            continue
        pa = skia.Path()
        pa.moveTo(-s * .57, yy)
        pa.quadTo(s * .8, yy + vib, s * 2.25, yy)
        G.c.drawPath(pa, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2, Color=skcol('#F3EBDC')))
    pop()


def tinCan(x, y, s, face=1, key='tc', col='#E8E1D2'):
    """paper-cup phone held at (x, y), mouth facing `face` (1 = right); returns the string anchor"""
    boilSeed(key)
    push()
    translate(x, y)
    scale(face, 1)
    paint([[-s * .3, -s * .5], [s * .4, -s * .7], [s * .4, s * .7], [-s * .3, s * .5]], wash=col, fill=mixCol(col, INK, .2), fillOp=50, ink=INK, sw=.8)
    paint(ellPts(s * .4, 0, s * .14, s * .7, 16), wash=mixCol(col, INK, .12), ink=INK, sw=.6)
    G.c.drawLine(-s * .1, -s * .55, -s * .1, s * .55, skia.Paint(AntiAlias=True, Color=skcol(HOT, .8), StrokeWidth=s * .08))
    pop()
    return x - face * s * .3, y


def mixer(x, y, w, h, t, faders, key='mx'):
    """mixing desk front: (x, y) = top-left; faders = list of 0..1 positions"""
    boilSeed(key)
    paint(rectPts(x, y, w, h), wash='#3B3550', fill='#2A2540', fillOp=80, ink=INK, sw=1.0)
    paint(rectPts(x - 20, y - 18, w + 40, 30), wash='#58507A', ink=INK, sw=.8)
    n = len(faders)
    for i, f in enumerate(faders):
        fx = x + 40 + i * (w - 80) / (n - 1)
        for kk in range(2):
            paint(ellPts(fx, y + 50 + kk * 46, 15, 15, 12), wash='#C9C1D6', ink=INK, sw=.5)
            ang = (hash1(i * 3 + kk) - .5) * 3
            line(fx, y + 50 + kk * 46, fx + 11 * math.cos(ang), y + 50 + kk * 46 + 11 * math.sin(ang), INK, 1, 2)
        y0, y1 = y + 130, y + h - 30
        line(fx, y0, fx, y1, '#18142A', 1, 6)
        fy = lerp(y1, y0, f)
        paint(rrPts(fx - 26, fy - 15, 52, 30, 6), wash='#FFFDF6', ink=INK, sw=.7)
        line(fx - 20, fy, fx + 20, fy, HOT, 1, 4)


def eqScreen(x, y, w, h, t, morph, key='eq'):
    """studio monitor with an EQ curve; morph 0 = jagged, 1 = a heart"""
    boilSeed(key)
    paint(rrPts(x - 14, y - 14, w + 28, h + 28, 14), wash='#2B2233', ink=INK, sw=1.0)
    paint(rectPts(x, y, w, h), wash='#141A3A', ink=None)
    for i in range(1, 6):
        G.c.drawLine(x, y + i * h / 6, x + w, y + i * h / 6, skia.Paint(AntiAlias=True, Color=skcol('#3A4A8A', .5), StrokeWidth=1.5))
        G.c.drawLine(x + i * w / 6, y, x + i * w / 6, y + h, skia.Paint(AntiAlias=True, Color=skcol('#3A4A8A', .5), StrokeWidth=1.5))
    N = 64
    hp = heartPts(x + w / 2, y + h * .54, h * .36, N)
    pts = []
    for i in range(N):
        f = i / (N - 1)
        jx = x + 20 + f * (w - 40)
        jy = y + h * .55 + h * .28 * (math.sin(f * 23 + t * 7) * .6 + math.sin(f * 51 - t * 5) * .4) * (1 - morph * .5)
        hx_, hy_ = hp[i]
        pts.append([lerp(jx, hx_, ease(morph)), lerp(jy, hy_, ease(morph))])
    col = mixCol('#7CF29A', '#FF6F96', morph)
    if morph > .95:
        pts.append(pts[0])
        glow(x + w / 2, y + h * .54, h * .5, '#FF6F96', .5)
    pa = skia.Path()
    pa.moveTo(*pts[0])
    for p in pts[1:]:
        pa.lineTo(*p)
    G.c.drawPath(pa, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7, Color=skcol(col), StrokeJoin=skia.Paint.kRound_Join))
    text('EQ', x + 50, y + 40, 34, '#8FA2E6', shadow=False)


def loadingBar(x, y, w, h, frac, label='', col='#7CF29A', key='lb', bgc='#FFFDF6'):
    boilSeed(key)
    paint(rrPts(x, y, w, h, h / 2), wash=bgc, ink=INK, sw=1.0)
    if frac > .01:
        G.c.drawRoundRect(skia.Rect.MakeXYWH(x + 6, y + 6, (w - 12) * clamp(frac), h - 12), (h - 12) / 2, (h - 12) / 2,
                          skia.Paint(AntiAlias=True, Color=skcol(col)))
    if label:
        text(label, x + w / 2, y + h / 2, h * .55, INK, shadow=False)


def heartBattery(x, y, s, n, key='hbat', blink=0.0):
    """a heart outline with 3 horizontal charge bars inside (n = 0..3)"""
    boilSeed(key)
    paint(heartPts(x, y, s, 26), wash='#FFFDF6', ink=INK, sw=1.4)
    for i in range(3):
        on = i < n
        yy = y + s * .32 - i * s * .42
        ww = s * (1.1 - .12 * i) * (1 if i < 2 else .9)
        c = '#7CF29A' if n >= 3 else ('#F2C53D' if n == 2 else '#FF6F96')
        if on:
            G.c.drawRoundRect(skia.Rect.MakeXYWH(x - ww / 2, yy - s * .15, ww, s * .3), 8, 8, skia.Paint(AntiAlias=True, Color=skcol(c, 1 - .5 * blink)))


def radar(x, y, r, t, ping=0.0, key='rd'):
    boilSeed(key)
    paint(ellPts(x, y, r, r, 30), wash='#163A2C', ink=INK, sw=1.0)
    for f in (.33, .66):
        ring(x, y, r * f, '#3FD17A', 2, .6)
    a = t * 4
    G.c.drawLine(x, y, x + math.cos(a) * r, y + math.sin(a) * r, skia.Paint(AntiAlias=True, Color=skcol('#7CF29A'), StrokeWidth=4))
    if ping > .01:
        heart(x + r * .4, y - r * .35, r * .16 * (1 + .3 * ping), '#FF6F96', key=key + 'h', sw=.4)
        ring(x + r * .4, y - r * .35, r * (.2 + .5 * (1 - ping)), '#FF8FB0', 4, ping)


def lineChart(x, y, w, h, prog, key='lc', label='嘴角', col=HOT):
    """little chart card: a line that rises to the top-right as prog goes 0..1"""
    boilSeed(key)
    paint(rrPts(x, y, w, h, 16), wash='#FFFDF6', ink=INK, sw=1.0)
    text(label, x + w / 2, y + 38, 34, INK, face=WENKAI, shadow=False)
    ax, ay = x + 34, y + h - 30
    line(ax, ay, x + w - 24, ay, INK, 1, 3)
    line(ax, ay, ax, y + 70, INK, 1, 3)
    pts = [(0, .1), (.2, .12), (.35, .08), (.5, .3), (.7, .55), (.85, .78), (1, 1)]
    n = int(prog * (len(pts) - 1) * 10)
    P = []
    for i in range(n + 1):
        f = i / 10
        j = min(int(f), len(pts) - 2)
        q = f - j
        fx = lerp(pts[j][0], pts[j + 1][0], q)
        fy = lerp(pts[j][1], pts[j + 1][1], q)
        P.append([ax + 10 + fx * (w - 80), ay - 10 - fy * (h - 120)])
    if len(P) > 1:
        pa = skia.Path()
        pa.moveTo(*P[0])
        for p in P[1:]:
            pa.lineTo(*p)
        G.c.drawPath(pa, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=7, Color=skcol(col), StrokeJoin=skia.Paint.kRound_Join))
        ex, ey = P[-1]
        a_ = math.atan2(P[-1][1] - P[-2][1], P[-1][0] - P[-2][0])
        for d in (-1, 1):
            line(ex, ey, ex - 22 * math.cos(a_ + d * .5), ey - 22 * math.sin(a_ + d * .5), col, 1, 7)


def pieChart(x, y, r, k, key='pie', label='你 100%'):
    if k <= .01:
        return
    boilSeed(key)
    rr_ = r * backOut(k)
    paint(ellPts(x, y, rr_, rr_, 32), wash='#FF8FB0', fill=HOT, fillOp=60, ink=INK, sw=1.2)
    heart(x, y - rr_ * .12, rr_ * .32, '#FFFFFF', key=key + 'h', sw=.5, shine=False)
    text(label, x, y + rr_ * .42, rr_ * .26, '#FFFFFF', stroke=INK, strokeW=8, shadow=False)


def chalk(txt, x, y, size, prog=1.0, col='#F3F1E8', align='left'):
    handText(txt, x, y, size, prog, col, WENKAI, align, pen=False)


def thoughtCloud(x, y, w, h, k, tail=None, key='tcl', col='#FFFFFF'):
    """a puffy thought cloud centred at (x, y) popping in with k; tail = (tx, ty) where the little dots come from"""
    if k <= .01:
        return
    p = backOut(k)
    push()
    translate(x, y)
    scale(p)
    boilSeed(key)
    n = 12
    for i in range(n):
        a = i / n * TAU
        paint(ellPts(math.cos(a) * w * .42, math.sin(a) * h * .38, w * .18, h * .22, 16), wash=col, ink=INK, sw=1.0)
    paint(ellPts(0, 0, w * .44, h * .4, 30), wash=col, ink=None)
    pop()
    if tail:
        tx, ty = tail
        for j, f in enumerate((.25, .5, .75)):
            if k > f:
                px, py = lerp(tx, x, f * .7), lerp(ty, y + h * .38, f * .7)
                r = 10 + j * 8
                paint(ellPts(px, py, r, r, 12), wash=col, ink=INK, sw=.7)


def giftWings(x, y, s, flap, key='gw'):
    for d in (-1, 1):
        push()
        translate(x + d * s * .55, y - s * .1)
        rotate(d * (-.3 - .5 * flap))
        boilSeed(key + str(d))
        paint([[0, 0], [d * s * .5, -s * .45], [d * s * .85, -s * .3], [d * s * .7, -s * .05], [d * s * .4, s * .05]],
              wash='#FFFFFF', fill='#CFE0F2', fillOp=60, ink=INK, sw=.8)
        pop()


def speedLines(t, seed, n, x0, y0, x1, y1, col='#FFFFFF', a=.7, L=240):
    for i in range(n):
        y = y0 + hash1(seed + i * 1.37) * (y1 - y0)
        x = x0 + ((hash1(seed + i * 2.11) * (x1 - x0) - t * 2600) % (x1 - x0 + L)) - L
        line(x, y, x + L * (.5 + hash1(i)), y, col, a, 5)


def doorbellChime(x, y, k, key='ding'):
    if k <= .01:
        return
    for i in range(3):
        a = -1.1 + i * .55
        r0, r1 = 50, 50 + 70 * easeOut(k)
        line(x + math.cos(a) * r0, y + math.sin(a) * r0, x + math.cos(a) * r1, y + math.sin(a) * r1, '#FFE36E', 1 - k * .3, 8)


def pressMachine(cx, top, bottom, w, press, key='pm'):
    """a hand-drawn press: posts, top plate at y = lerp(top, bottom_contact, press)"""
    boilSeed(key)
    for sx in (-1, 1):
        paint(rectPts(cx + sx * w / 2 - 22, top - 120, 44, bottom - top + 160), wash='#8E93A6', fill='#5E6378', fillOp=60, ink=INK, sw=1.0)
    paint(rectPts(cx - w / 2 - 50, top - 170, w + 100, 70), wash='#5E6378', ink=INK, sw=1.0)
    paint(rectPts(cx - w / 2 - 40, bottom, w + 80, 50), wash='#5E6378', ink=INK, sw=1.0)
    py = lerp(top, bottom - 70, press)
    inkLine([[cx, top - 110], [cx, py - 40]], 6, '#3B3F52', 'ink', 0)
    paint(rectPts(cx - w / 2, py - 40, w, 40), wash='#B9C0D6', fill='#7E86A2', fillOp=60, ink=INK, sw=1.0)
    return py


def keyProp(x, y, s, rot=0.0, key='key', col='#F2C53D'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(ellPts(-s * .6, 0, s * .4, s * .4, 18), wash=col, ink=INK, sw=.7)
    G.c.drawCircle(-s * .6, 0, s * .15, skia.Paint(AntiAlias=True, Color=skcol(INK)))
    paint(rectPts(-s * .25, -s * .1, s * 1.2, s * .2), wash=col, ink=INK, sw=.6)
    paint(rectPts(s * .7, 0, s * .15, s * .3), wash=col, ink=INK, sw=.5)
    paint(rectPts(s * .4, 0, s * .12, s * .22), wash=col, ink=INK, sw=.5)
    pop()


def railing(y, x0, x1, key='rail', col='#F3EBDC'):
    boilSeed(key)
    paint(rectPts(x0, y - 10, x1 - x0, 20), wash=col, ink=INK, sw=.9)
    paint(rectPts(x0, y + 120, x1 - x0, 14), wash=col, ink=INK, sw=.8)
    for x in range(int(x0), int(x1), 90):
        paint(rectPts(x, y, 14, 240), wash=col, ink=INK, sw=.6)


def scarfDraw(view='front', col='#D9534F', k=1.0):
    """a red scarf around the neck line (body-local), plus a tail"""
    def d(u, sw):
        if k <= .01:
            return
        boilSeed('scf' + col)
        V = VIEWS[view]
        L, R = V['L'] * u, V['R'] * u
        paint(rrPts(L - .2 * u, -4.4 * u, (R - L + .4 * u), 1.2 * u * k, .5 * u), wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=sw * .6)
        tx = (L + 2.2 * u) if view != 'front' else -1.4 * u
        paint(rrPts(tx, -3.6 * u, 1.1 * u, 2.4 * u * k, .3 * u), wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=sw * .6)
        for i in range(3):
            G.c.drawLine(tx + .2 * u + i * .35 * u, -1.2 * u, tx + .2 * u + i * .35 * u, -1.0 * u + .4 * u * k,
                         skia.Paint(AntiAlias=True, Color=skcol(col), StrokeWidth=max(1.5, u * .15)))
    return d


def chain(*fns):
    def d(u, sw):
        for f in fns:
            if f:
                f(u, sw)
    return d


def puzzleHalf(x, y, s, side=-1, col=HOT, key='pz'):
    """left (side -1) or right (1) half of a heart with a jigsaw tab on the seam"""
    boilSeed(key + str(side))
    hp = heartPts(x, y, s, 40)
    half = [p for p in hp if (p[0] - x) * side >= -1]
    half.sort(key=lambda p: math.atan2(p[1] - y, (p[0] - x) * side))
    seam = []
    for i in range(9):
        f = i / 8
        yy = lerp(y - s * .55, y + s * .95, f)
        bump = side * -s * .22 * math.sin(clamp((f - .35) / .3) * math.pi) if .35 < f < .65 else 0
        seam.append([x + bump, yy])
    pts = [[x, y - s * .55]] + [p for p in hp if (p[0] - x) * side > 0] + seam[::-1]
    paint(pts, wash=col, fill=mixCol(col, INK, .25), fillOp=50, ink=INK, sw=1.0)


def clockFace(x, y, r, hh, mm, key='clk', night=0.0):
    boilSeed(key)
    paint(ellPts(x, y, r + 12, r + 12, 32), wash='#6B4A3E', ink=INK, sw=1.0)
    paint(ellPts(x, y, r, r, 32), wash=mixCol('#FFFDF6', '#FFE9A8', night), ink=INK, sw=.8)
    for i in range(12):
        a = i / 12 * TAU
        line(x + math.cos(a) * r * .82, y + math.sin(a) * r * .82, x + math.cos(a) * r * .92, y + math.sin(a) * r * .92, INK, 1, 4)
    ah = (hh % 12 + mm / 60) / 12 * TAU - math.pi / 2
    am = mm / 60 * TAU - math.pi / 2
    line(x, y, x + math.cos(ah) * r * .5, y + math.sin(ah) * r * .5, INK, 1, 9)
    line(x, y, x + math.cos(am) * r * .75, y + math.sin(am) * r * .75, INK, 1, 6)
    dot(x, y, 8, HOT)


def snowfall(t, seed, n, x0, y0, x1, y1, rate=1.0, a=1.0, r=7.0):
    for i in range(int(n * rate)):
        h = hash1(seed + i * 1.13)
        sp = 90 + 80 * hash1(i * 2.7)
        y = y0 + ((h * (y1 - y0) + t * sp) % (y1 - y0))
        x = x0 + hash1(seed + i * 3.1) * (x1 - x0) + 30 * math.sin(t * 1.5 + i)
        dot(x, y, r * (.6 + .7 * hash1(i * 5.3)), '#FFFFFF', a * (.6 + .4 * hash1(i)))


def yearDigits(x, y, size, year, prev, k, col=INK, face=WENKAI):
    """a year written as 4 digits; digits that changed from prev roll in (k 0..1)"""
    s1, s0 = str(year), str(prev)
    w = textW('0', size, face) * 1.05
    x0 = x - w * 2
    for i in range(4):
        cx_ = x0 + w * (i + .5)
        if s1[i] == s0[i] or k >= 1:
            text(s1[i], cx_, y, size, col, face=face, shadow=False)
        else:
            G.c.save()
            G.c.clipRect(skia.Rect.MakeXYWH(cx_ - w / 2, y - size * .62, w, size * 1.24))
            e = easeOut(k)
            text(s0[i], cx_, y + size * e, size, col, face=face, shadow=False, a=1 - e)
            text(s1[i], cx_, y - size * (1 - e), size, col, face=face, shadow=False, a=e)
            G.c.restore()


def glowStick(x, y, s, ang, col='#7CF2E8', key='gs'):
    push()
    translate(x, y)
    rotate(ang)
    glow(0, -s, s * .8, col, .6)
    boilSeed(key)
    paint(rrPts(-s * .09, -s * 1.6, s * .18, s * 1.3, s * .08), wash=col, ink=INK, sw=.6)
    paint(rrPts(-s * .11, -s * .35, s * .22, s * .45, s * .05), wash='#3D3A52', ink=INK, sw=.5)
    pop()


def playIcon(x, y, s, age, col='#3FA37A', life=None):
    """a green ▶ badge that pops on (drawn: the fonts have no ▶ glyph)"""
    if age < -.04:
        return
    k = backOut(clamp((age + .04) / .14))
    a = 1.0 if life is None else 1 - seg(age, life - .2, life)
    push()
    translate(x, y)
    scale(k)
    boilSeed('play')
    paint(ellPts(0, 0, s, s, 26), wash='#FFFFFF', washOp=int(255 * a), ink=INK if a > .5 else None, sw=1.0)
    paint([[-s * .3, -s * .48], [s * .52, 0], [-s * .3, s * .48]], wash=col, washOp=int(255 * a), ink=None)
    pop()


def checkMark(x, y, s, k=1.0, col='#3FA37A'):
    if k <= .01:
        return
    inkLine([[x - s * .5, y], [x - s * .5 + s * .4 * min(1, k * 2), y + s * .4 * min(1, k * 2)]] +
            ([[x - s * .1 + s * .7 * clamp(k * 2 - 1), y + s * .4 - s * .9 * clamp(k * 2 - 1)]] if k > .5 else []), 1.6, col, 'ink', .3)
