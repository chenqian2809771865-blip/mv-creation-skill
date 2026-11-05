# hl.py: 《后来》 cast costumes, sets and effects (watercolour + ink, Skia engine from 疑心病/新地球).
# Logical canvas 1920x1080. Present = indigo night + warm lamp; memory = summer gold/green + white gardenias.
import math, os, json
from eng import *
import eng
from clawd import *
from props import umbrellaAt, gradient, puff, bench, lamp, city, zebra, yiyun, bubble, sparkle, sparkles, phoneHook
from sets import starField, milkyWay, sunDisc, sea, polaroid

HERE = os.path.dirname(os.path.abspath(__file__))
WENKAI = 'LXGWWenKai-Regular.ttf'
PINK = '#EE9AAE'
SUNG = '#F59BB0'
NIGHT1, NIGHT2 = '#1E2457', '#3A3F7E'
LAMP = '#FFC976'
GARD = '#FFFDF4'          # gardenia white
LEAF, LEAFDK = '#5E9E5A', '#2F6440'


# ================================================================ costumes
def _span(view):
    V = VIEWS.get(view or 'front', VIEWS['front'])
    return V['L'], V['R']


def skirtHook(view, col='#5B7FC4', dk='#3C5A9A', flare=0.0):
    """blue pleated skirt (百褶裙), drawn in the body's local frame"""
    L, R = _span(view)

    def h(u, sw):
        boilSeed('skirt')
        fl = .7 + flare
        top, bot = -2.75 * u, -.85 * u
        pts = [[L * u - .15 * u, top], [R * u + .15 * u, top], [R * u + fl * u, bot], [L * u - fl * u, bot]]
        paint(pts, wash=col, fill=dk, fillOp=70, bleed=.04, border=.4, ink=INK, sw=sw * .8, lite=True)
        n = max(4, int((R - L) * 1.1))
        for i in range(1, n):
            k = i / n
            xa = lerp(L * u - .15 * u, R * u + .15 * u, k)
            xb = lerp(L * u - fl * u, R * u + fl * u, k)
            inkLine([[xa, top + .1 * u], [xb, bot - .05 * u]], sw * .4, dk, 'inkfine', 0)
        # hem zig-zag
        z = []
        for i in range(2 * n + 1):
            k = i / (2 * n)
            z.append([lerp(L * u - fl * u, R * u + fl * u, k), bot + (.18 * u if i % 2 else 0)])
        inkLine(z, sw * .5, INK, 'inkfine', 0)
    return h


def scarfHook(view, col, dk, tail=1, flutter=0.0):
    L, R = _span(view)

    def h(u, sw):
        boilSeed('scarf')
        y0, y1 = -3.85 * u, -3.1 * u
        x0, x1 = L * u - .12 * u, R * u + .12 * u
        pts = [[x0, y0], [lerp(x0, x1, .5), y0 + .08 * u], [x1, y0], [x1 + .05 * u, y1], [lerp(x0, x1, .5), y1 + .12 * u], [x0 - .05 * u, y1]]
        paint(pts, wash=col, fill=dk, fillOp=70, bleed=.03, ink=INK, sw=sw * .7, lite=True)
        n = max(5, int((R - L) * 1.3))
        for i in range(1, n):
            xx = lerp(x0, x1, i / n)
            inkLine([[xx, y0 + .12 * u], [xx, y1 - .02 * u]], sw * .3, dk, 'inkfine', 0)
        if tail and view != 'back':
            if view == 'side':
                tx = .5 * u
            elif view in ('q', 'qback'):
                tx = (2.2 if tail > 0 else -3.2) * u
            else:
                tx = (1.6 if tail > 0 else -2.8) * u
            f = flutter * .5 * u
            T_ = [[tx, y1 - .05 * u], [tx + 1.0 * u, y1 - .05 * u], [tx + 1.0 * u + f, y1 + 1.25 * u], [tx + f, y1 + 1.25 * u]]
            paint(T_, wash=col, fill=dk, fillOp=90, ink=INK, sw=sw * .6, lite=True)
            for k in range(3):
                xx = T_[3][0] + (k + .5) * .33 * u
                inkLine([[xx, T_[3][1]], [xx, T_[3][1] + .3 * u]], sw * .4, dk, 'inkfine', 0)
    return h


def tieHook(view):
    if view not in ('front', 'q'):
        return None
    cx = 0 if view == 'front' else 1.5

    def h(u, sw):
        boilSeed('tie')
        x = cx * u
        paint([[x - .45 * u, -3.75 * u], [x + .45 * u, -3.75 * u], [x + .25 * u, -3.35 * u], [x - .25 * u, -3.35 * u]], wash='#2E3E73', ink=INK, sw=sw * .6, lite=True)
        paint([[x - .25 * u, -3.35 * u], [x + .25 * u, -3.35 * u], [x + .45 * u, -2.1 * u], [x, -1.75 * u], [x - .45 * u, -2.1 * u]], wash='#3B4F8E', fill='#22306A', fillOp=60, ink=INK, sw=sw * .6, lite=True)
        inkLine([[x - .3 * u, -2.9 * u], [x + .35 * u, -2.6 * u]], sw * .35, '#C8324A', 'inkfine', 0)
    return h


def _chain(*hooks):
    hs = [h for h in hooks if h]
    if not hs:
        return None

    def h(u, sw):
        for f in hs:
            push()
            f(u, sw)
            pop()
    return h


def herNow(x, y, u, o=None):
    o = dict(o or {})
    v = o.get('view', 'front')
    extra = o.pop('draw', None)
    if not o.pop('noScarf', False):
        o['draw'] = _chain(scarfHook(v, '#EFE2CC', '#C9B08F', tail=1, flutter=o.pop('flutter', 0)), extra)
    else:
        o['draw'] = extra
    her(x, y, u, o)


def her17(x, y, u, o=None):
    o = dict(o or {})
    v = o.get('view', 'front')
    extra = o.pop('draw', None)
    o['draw'] = _chain(skirtHook(v, flare=o.pop('flare', 0)), extra)
    her(x, y, u, o)


def himNow(x, y, u, o=None):
    o = dict(o or {})
    v = o.get('view', 'front')
    extra = o.pop('draw', None)
    o['draw'] = _chain(scarfHook(v, '#4E6C8E', '#33496A', tail=-1, flutter=o.pop('flutter', 0)), extra)
    him(x, y, u, o)


def him17(x, y, u, o=None):
    o = dict(o or {})
    v = o.get('view', 'front')
    extra = o.pop('draw', None)
    o['draw'] = _chain(tieHook(v), extra)
    him(x, y, u, o)


GREYS = [('#A9A6BC', '#7E7A96', '#CFCCE0'), ('#9DB0C4', '#71879E', '#C9D6E3'), ('#B8A9B6', '#8D7C8B', '#DCCFD9'),
         ('#A3B5A8', '#77897C', '#CCD9CF'), ('#B3AFA0', '#88836F', '#D6D2C4')]
UMB = ['#8FA6C9', '#B3A0C9', '#7FB1B5', '#C9A0A8', '#A7B48F', '#9C95B8', '#C2B08A']


def walker(x, y, u, t, i, dirn=1, umb=True, k=1.0, rate=1.0, lite=True, view='q', wk=None, ucol=None):
    g_ = GREYS[i % len(GREYS)]
    ph = t * rate * 1.25 + hash1(i * 1.3)
    w = ph if wk is None else wk
    o = dict(col=g_[0], dk=g_[1], lt=g_[2], walk=w, dy=-abs(math.sin(w * TAU)) * .4, view=view, flip=dirn < 0,
             aL=.1, aR=.55 if umb else .1, eyes='normal', boilKey=f'w{i}', lite=lite, sx=k, sy=k, seed=i)
    clawd(x, y, u, o)
    if umb and k > .3:
        d = -1 if dirn < 0 else 1
        if view in ('back', 'qback'):
            d = 0
        umbrellaAt(x + 1.2 * u * d, y - 4.4 * u + o['dy'] * u, 5.6 * u * k, ucol or UMB[i % len(UMB)], 1, key=f'wu{i}', tilt=-.1 * d + .04 * math.sin(t * 2 + i), handle=True, dots=False)


# ================================================================ helpers
def tint(col, k, mode=skia.BlendMode.kMultiply):
    if k <= 0:
        return
    pa = skia.Paint(AntiAlias=False, Color=skcol(col, clamp(k)))
    pa.setBlendMode(mode)
    G.c.drawRect(skia.Rect.MakeXYWH(-400, -400, W + 800, H + 800), pa)


def desat(k):
    if k <= 0:
        return
    pa = skia.Paint(AntiAlias=False, Color=skcol('#808080', clamp(k)))
    pa.setBlendMode(skia.BlendMode.kSaturation)
    G.c.drawRect(skia.Rect.MakeXYWH(-400, -400, W + 800, H + 800), pa)


def memoryGrade(k=1.0):
    """summer memory look: warm golden wash + soft light, applied over the whole shot"""
    tint('#FFE3B0', .22 * k, skia.BlendMode.kSoftLight)
    tint('#FFF1D6', .10 * k, skia.BlendMode.kScreen)


def vignette(k=.5, col='#1A1530'):
    if k <= 0:
        return
    sh = skia.GradientShader.MakeRadial(skia.Point(W / 2, H / 2), W * .72, [skcol(col, 0), skcol(col, 0), skcol(col, k)], [0, .55, 1])
    G.c.drawRect(skia.Rect.MakeXYWH(-400, -400, W + 800, H + 800), skia.Paint(Shader=sh))


def wtext(txt, x, y, size, col, a=1.0, align='center', rot=0.0, face=WENKAI, shadow=False, stroke=None, strokeW=None):
    return text(txt, x, y, size, col, face=face, align=align, shadow=shadow, a=a, rot=rot, stroke=stroke, strokeW=strokeW)


def caption(txt, x, y, size=40, col='#FFF5E2', a=1.0, rot=-.03):
    """little handwritten diary caption painted into memory scenes (date / place)"""
    if a <= .01:
        return
    wtext(txt, x + 2, y + 3, size, INK, a * .35, 'left', rot)
    wtext(txt, x, y, size, col, a, 'left', rot)


# ================================================================ handwriting (stroke order, ink bleeding into paper)
import hanzi
hanzi.DATA = json.load(open(os.path.join(HERE, 'strokes.json'), encoding='utf-8'))


def inkWrite(txt, x0, y0, size, prog, col=INK, gap=.08, bleed=True, a=1.0, mode='brush'):
    """write txt left to right (top-left x0, y0, em size) up to prog 0..1 (shared across chars by stroke length)"""
    chars = [c for c in txt]
    lens = [hanzi.char_len(c) if c != ' ' else 0 for c in chars]
    tot = sum(lens) or 1
    done = prog * tot
    x = x0
    c = G.c
    pa = skia.Paint(AntiAlias=True, Color=skcol(col, .93 * a))
    pb = skia.Paint(AntiAlias=True, Color=skcol(col, .18 * a))
    pb.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, size * .018))
    for ch, L in zip(chars, lens):
        if ch == ' ':
            x += size * .45
            continue
        p = clamp(done / L) if L else 0
        done -= L
        if p > 0:
            if bleed:
                hanzi.write_char(c, ch, x - size * .006, y0 + size * .004, size, p, [pb], mode=mode)
            hanzi.write_char(c, ch, x, y0, size, p, [pa], mode=mode)
        x += size * (1 + gap)


def writeW(txt, size, gap=.08):
    n = sum(1 for c in txt if c != ' ')
    s = sum(1 for c in txt if c == ' ')
    return n * size * (1 + gap) - size * gap + s * size * .45


# ================================================================ small effects
def petals(t, seed, n, x0, y0, x1, y1, s=12, col=GARD, fall=60, a=1.0):
    """drifting gardenia petals, positions only from t"""
    for i in range(n):
        h1, h2, h3 = hash1(seed + i * 3.7), hash1(seed * 1.3 + i * 5.1), hash1(seed * 2.1 + i * 1.7)
        span = (y1 - y0) + 200
        yy = y0 - 100 + (h2 * span + t * fall * (.6 + .6 * h3)) % span
        xx = lerp(x0, x1, h1) + math.sin(t * (.6 + h3) + i) * 40 + t * 12 * (h3 - .3)
        xx = x0 + (xx - x0) % max(1, (x1 - x0))
        ang = t * (1.2 + h1) + i
        r = s * (.7 + .5 * h2)
        boilSeed(f'pt{seed}{i}')
        pts = [[xx + math.cos(ang) * r, yy + math.sin(ang) * r * .45], [xx + math.cos(ang + 1.6) * r * .35, yy + math.sin(ang + 1.6) * r * .3],
               [xx - math.cos(ang) * r * .8, yy - math.sin(ang) * r * .4], [xx + math.cos(ang - 1.6) * r * .35, yy + math.sin(ang - 1.6) * r * .3]]
        paint(pts, wash=col, washOp=int(235 * a), ink=mixCol('#C9C2A8', INK, .2), sw=.45, curv=.6, lite=True)


def rain(t, seed, n, x0, y0, x1, y1, col='#C9D6F0', a=.55, ln=46, ang=.18, sp=1400):
    step = math.floor(t * 12) / 12
    p = skia.Paint(AntiAlias=True, Color=skcol(col, a), StrokeWidth=2.2, Style=skia.Paint.kStroke_Style, StrokeCap=skia.Paint.kRound_Cap)
    span = y1 - y0 + 200
    for i in range(n):
        h1, h2 = hash1(seed + i * 1.91), hash1(seed * .7 + i * 3.3)
        yy = y0 - 100 + (h2 * span + step * sp * (.8 + .4 * h1)) % span
        xx = lerp(x0, x1, h1) - (yy - y0) * ang
        G.c.drawLine(xx, yy, xx - ln * ang, yy + ln, p)


def ripples(t, seed, n, x0, y0, x1, y1, col='#C9D6F0', a=.5):
    for i in range(n):
        h1, h2 = hash1(seed + i * 2.3), hash1(seed + i * 7.1)
        ph = frac(t * 1.3 + h2)
        x, y = lerp(x0, x1, h1), lerp(y0, y1, hash1(seed * 3 + i))
        r = 8 + ph * 34
        pa = skia.Paint(AntiAlias=True, Color=skcol(col, a * (1 - ph)), Style=skia.Paint.kStroke_Style, StrokeWidth=1.6)
        G.c.drawOval(skia.Rect.MakeXYWH(x - r, y - r * .32, 2 * r, r * .64), pa)


def fireflies(t, seed, n, x0, y0, x1, y1, a=1.0):
    for i in range(n):
        h1, h2, h3 = hash1(seed + i * 2.9), hash1(seed + i * 4.3), hash1(seed + i * 6.7)
        x = lerp(x0, x1, h1) + math.sin(t * (.4 + h3) + i) * 50
        y = lerp(y0, y1, h2) + math.cos(t * (.5 + h1) + i * 2) * 30
        k = .5 + .5 * math.sin(t * (1.5 + h3 * 2) + i * 3)
        if k < .15:
            continue
        glow(x, y, 26 + 20 * k, '#FFF0A0', .7 * k * a)
        G.c.drawCircle(x, y, 3.2, skia.Paint(AntiAlias=True, Color=skcol('#FFFBD8', k * a)))


def stars(t, seed, n, x0, y0, x1, y1, a=1.0, r=3.0):
    starField(t, seed, n, x0, y0, x1, y1, on=a, r=r)


def bloomRing(x, y, r, col, a=1.0, key='bl'):
    """a watercolour bloom (wet drop spreading on paper): soft fill with a darker drying edge"""
    if r < 2 or a <= .01:
        return
    boilSeed(key)
    P = []
    for i in range(44):
        ang = i / 44 * TAU
        rr = r * (1 + .1 * math.sin(ang * 5 + 1.1) + .06 * math.sin(ang * 11 + 2.3))
        P.append([x + math.cos(ang) * rr, y + math.sin(ang) * rr])
    paint(P, wash=col, washOp=int(80 * a), ink=None)
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.5, r * .06), Color=skcol(mixCol(col, INK, .25), .45 * a))
    pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, max(1, r * .03)))
    G.c.drawPath(eng._path(P), pa)


def gardeniaFlower(x, y, r, open_=1.0, key='gf', rot=0.0, col=GARD, dry=False):
    """a single gardenia, seen from above: spiral of 6 broad petals around a creamy centre"""
    if open_ <= .01:
        return
    boilSeed(key)
    k = easeOut(open_)
    edge = mixCol('#D8CFAE', INK, .15) if not dry else '#A89272'
    for ring_, (n, rr, off) in enumerate(((6, 1.0, 0), (5, .62, .4))):
        for i in range(n):
            a = rot + off + i / n * TAU
            pr = r * rr * k
            cx, cy = x + math.cos(a) * pr * .45, y + math.sin(a) * pr * .45
            P = [[cx + math.cos(a) * pr * .75, cy + math.sin(a) * pr * .75], [cx + math.cos(a + 1.3) * pr * .42, cy + math.sin(a + 1.3) * pr * .42],
                 [x + math.cos(a + .5) * pr * .1, y + math.sin(a + .5) * pr * .1], [cx + math.cos(a - 1.3) * pr * .42, cy + math.sin(a - 1.3) * pr * .42]]
            paint(P, wash=col if not dry else mixCol('#E8D9B5', '#C9AE80', ring_ * .4), fill='#EFE6C8' if not dry else '#BFA27A', fillOp=60,
                  ink=edge, sw=.5, curv=.6, lite=True)
    paint(ellPts(x, y, r * .16 * k, r * .16 * k, 10), wash='#F3D98A' if not dry else '#C9A86A', ink=None)


def gardeniaBush(x, y, w, h, t=0.0, key='gb', flowers=26, lite=False, night=0.0):
    """a big gardenia hedge: dark glossy leaves, white flowers dotted all over"""
    boilSeed(key)
    c1 = mixCol(LEAF, '#1E3A55', night * .7)
    c2 = mixCol(LEAFDK, '#141F3A', night * .7)
    P = []
    for i in range(40):
        a = math.pi + i / 39 * math.pi
        r = 1 + .12 * abs(math.sin(a * 5)) + .06 * math.sin(a * 13)
        P.append([x + math.cos(a) * w / 2 * r, y + math.sin(a) * h * r])
    P += [[x + w / 2, y + 20], [x - w / 2, y + 20]]
    paint(P, wash=c1, fill=c2, fillOp=110, bleed=.08, ink=INK, sw=1.1, curv=.2, lite=lite)
    # leaf clumps
    for i in range(18):
        hx, hy = hash1(i * 3.3 + 1), hash1(i * 5.7 + 2)
        lx = x + (hx - .5) * w * .85
        ly = y - hy * h * .85 * math.sin(math.acos(clamp(abs(hx - .5) * 2 * .9)))
        boilSeed(f'{key}l{i}')
        paint(ellPts(lx, ly, 34, 18, 10, 2, hx * 3), wash=mixCol(c1, '#9FD39A', .25 * (1 - night)), washOp=150, ink=None, lite=True)
    for i in range(flowers):
        hx, hy = hash1(i * 7.1 + 3), hash1(i * 2.9 + 8)
        fx = x + (hx - .5) * w * .82
        fy = y - 18 - hy * h * .8 * math.sin(math.acos(clamp(abs(hx - .5) * 2 * .92)))
        gardeniaFlower(fx, fy, 16 + 8 * hash1(i), 1, key=f'{key}f{i}', rot=hx * 6, col=mixCol(GARD, '#C9D3F0', night * .35))


def potGardenia(x, y, s, buds=3, open_=0.0, key='pg', night=1.0):
    """windowsill pot: terracotta pot, a little gardenia shrub; open_ opens one flower (0..1)"""
    boilSeed(key)
    paint([[x - 1.1 * s, y - 1.6 * s], [x + 1.1 * s, y - 1.6 * s], [x + .85 * s, y], [x - .85 * s, y]], wash=mixCol('#C9774E', '#5A3A4A', night * .35), ink=INK, sw=.9, lite=True)
    paint(rectPts(x - 1.25 * s, y - 1.85 * s, 2.5 * s, .35 * s), wash=mixCol('#D98A5E', '#6A4458', night * .35), ink=INK, sw=.8, lite=True)
    lc = mixCol(LEAF, '#24406A', night * .5)
    for i in range(9):
        a = -math.pi / 2 + (i - 4) * .33
        L = s * (1.6 + .5 * hash1(i))
        bx, by = x + math.cos(a) * L * .35, y - 1.85 * s + math.sin(a) * L * .4
        tx, ty = x + math.cos(a) * L, y - 1.85 * s + math.sin(a) * L
        paint([[bx, by], [lerp(bx, tx, .5) + .25 * s, lerp(by, ty, .5)], [tx, ty], [lerp(bx, tx, .5) - .25 * s, lerp(by, ty, .5)]], wash=lc, fill=mixCol(lc, INK, .3), fillOp=70, ink=INK, sw=.6, curv=.5, lite=True)
    for i in range(buds):
        bx = x + (i - (buds - 1) / 2) * .8 * s
        by = y - 3.1 * s - (.3 * s if i % 2 else 0)
        if i == buds // 2 and open_ > 0:
            gardeniaFlower(bx, by, .75 * s * (.6 + .4 * open_), open_, key=f'{key}o', col=mixCol(GARD, '#D8DEF5', night * .25))
        else:
            paint(ellPts(bx, by, .22 * s, .34 * s, 10), wash=mixCol('#EDEBD8', '#B8C0DD', night * .3), ink=INK, sw=.5, lite=True)


# ================================================================ diary
PAGE = '#F7EEDC'
PAGE2 = '#F2E6CF'


def desk(col='#8A5A3C', dk='#5E3A27', y0=-200, light=1.0):
    gradRect(-200, y0, W + 400, H + 400 - y0, [mixCol(col, '#2A1E33', .25 * (1 - light)), mixCol(dk, '#1E1426', .3)])
    for i in range(14):
        boilSeed(f'grain{i}')
        yy = y0 + 60 + i * 95 + jit(10)
        inkLine([[-200, yy], [700, yy + 14], [1400, yy - 8], [W + 200, yy + 6]], .5, mixCol(dk, INK, .3), 'inkfine', .6)


def diarySpread(cx, cy, w, h, tilt=0.0, key='diary', light=1.0, pressed=True, pressedK=1.0, ribbon=True, ruled=True, leftAge=0.0):
    """open diary seen from above: two cream pages with a soft gutter, cover edges below. returns page rects"""
    push()
    translate(cx, cy)
    rotate(tilt)
    boilSeed(key)
    # cover
    paint(rrPts(-w / 2 - 26, -h / 2 - 20, w + 52, h + 40, 18), wash='#6E3B42', fill='#4A2430', fillOp=90, ink=INK, sw=1.2)
    # page stack edges
    for k in range(3):
        paint(rrPts(-w / 2 - 6 + k * 2, -h / 2 - 6 + k * 3, w + 12 - k * 4, h + 10, 8), wash=mixCol(PAGE2, '#C9B48F', .3 + k * .1), ink=None, lite=True)
    lp = mixCol(PAGE, '#E6CFA0', leftAge)
    for s in (-1, 1):
        x0 = -w / 2 if s < 0 else 0
        P = [[x0, -h / 2], [x0 + w / 2, -h / 2], [x0 + w / 2, h / 2], [x0, h / 2]]
        if s < 0:
            P = [[-w / 2, -h / 2 + 4], [0, -h / 2], [0, h / 2], [-w / 2, h / 2 + 4]]
        else:
            P = [[0, -h / 2], [w / 2, -h / 2 + 4], [w / 2, h / 2 + 4], [0, h / 2]]
        paint(P, wash=lp if s < 0 else PAGE, fill=PAGE2, fillOp=70, bleed=.03, border=.3, ink=mixCol('#B89C70', INK, .2), sw=.7)
        if ruled:
            for r in range(1, 13):
                yy = -h / 2 + r * h / 13.5
                G.c.drawLine(x0 + 30 if s > 0 else -w / 2 + 30, yy, (w / 2 - 30) if s > 0 else -30, yy,
                             skia.Paint(AntiAlias=True, Color=skcol('#9FB3D1', .35), StrokeWidth=1.2))
    # gutter shadow
    sh = skia.GradientShader.MakeLinear([skia.Point(-60, 0), skia.Point(60, 0)], [skcol('#5A4030', 0), skcol('#5A4030', .28), skcol('#5A4030', 0)])
    G.c.drawRect(skia.Rect.MakeXYWH(-60, -h / 2, 120, h), skia.Paint(Shader=sh))
    if ribbon:
        boilSeed(key + 'rb')
        paint([[-8, -h / 2 - 30], [10, -h / 2 - 30], [18, h / 2 + 70], [2, h / 2 + 52], [-10, h / 2 + 74]], wash='#B8324F', ink=INK, sw=.7, lite=True)
    if pressed and pressedK > 0:
        gardeniaFlower(-w * .22, h * .18, h * .13, 1, key=key + 'pf', rot=.7, dry=True)
        boilSeed(key + 'st')
        inkLine([[-w * .22 + 10, h * .18 + 20], [-w * .3, h * .38], [-w * .34, h * .44]], 1.2, '#8E7A4E', 'ink', .4)
    pop()


def fountainPen(x, y, ang, s=1.0, key='pen'):
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    paint(rrPts(-160 * s, -13 * s, 230 * s, 26 * s, 12 * s), wash='#2C2C44', fill='#15152A', fillOp=80, ink=INK, sw=.8)
    paint(rectPts(40 * s, -14 * s, 18 * s, 28 * s), wash='#D9B45A', ink=INK, sw=.6)
    paint([[70 * s, -10 * s], [110 * s, 0], [70 * s, 10 * s]], wash='#D9B45A', ink=INK, sw=.6)
    inkLine([[-140 * s, -15 * s], [-40 * s, -15 * s]], 1.4, '#D9B45A', 'ink', 0)
    pop()


# ================================================================ rooms
def windowView(x, y, w, h, t, sky=(NIGHT1, '#3E4C8E'), moon=True, cityK=1.0, starsK=1.0, key='wv', moonXY=None, cityY=None, rainK=0.0, fogK=0.0):
    """what is seen through a window (drawn clipped to the opening)"""
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(x, y, w, h))
    gradRect(x, y, w, h, list(sky))
    if starsK > 0:
        stars(t, 17, 40, x, y, x + w, y + h * .6, starsK, 2.6)
    if moon:
        mx, my = moonXY or (x + w * .74, y + h * .22)
        glow(mx, my, 150, '#E8E4FF', .55)
        boilSeed(key + 'm')
        paint(ellPts(mx, my, 34, 34, 24), wash='#FFF8E4', ink=None)
    if cityK > 0:
        push()
        cy = cityY if cityY is not None else y + h * .62
        translate(x, cy - 640 * .5)
        scale(w / W, .5)
        city(t, cityK, key=key + 'c', col='#2C2F66', win='#FFD98A')
        pop()
    if rainK > 0:
        rain(t, 3, 40, x, y, x + w, y + h, a=.35 * rainK, ln=30)
    G.c.restore()
    if fogK > 0:
        flatRect(x, y, w, h, '#DDE4F5', .28 * fogK)


def windowFrame(x, y, w, h, col='#6B4A3E', bars=True, key='wf', sill=True):
    boilSeed(key)
    fw = 26
    for P in ([x - fw, y - fw, w + 2 * fw, fw], [x - fw, y + h, w + 2 * fw, fw], [x - fw, y, fw, h], [x + w, y, fw, h]):
        paint(rectPts(*P), wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=1.0, lite=True)
    if bars:
        paint(rectPts(x + w / 2 - 9, y, 18, h), wash=col, ink=INK, sw=.9, lite=True)
        paint(rectPts(x, y + h * .42 - 9, w, 18), wash=col, ink=INK, sw=.9, lite=True)
    if sill:
        paint(rectPts(x - fw - 40, y + h + fw - 6, w + 2 * fw + 80, 34), wash=mixCol(col, '#E8D3B8', .2), ink=INK, sw=1.0)


def roomWall(c1='#2B3168', c2='#454A86', lampXY=(1500, 520), lampK=1.0):
    gradRect(-300, -300, W + 600, H + 600, [c1, c2])
    if lampK > 0:
        glow(lampXY[0], lampXY[1], 900, '#FFB867', .55 * lampK)
        glow(lampXY[0], lampXY[1], 380, '#FFD9A0', .5 * lampK)


def deskLamp(x, y, s=1.0, on=1.0, key='dl', flip=False):
    push()
    translate(x, y)
    if flip:
        scale(-1, 1)
    boilSeed(key)
    paint(ellPts(0, 0, 70 * s, 16 * s, 16), wash='#3A3550', ink=INK, sw=.9)
    inkLine([[0, -6 * s], [-40 * s, -150 * s], [10 * s, -250 * s]], 3.2 * s, '#3A3550', 'ink', .2)
    paint([[-30 * s, -230 * s], [70 * s, -270 * s], [110 * s, -185 * s], [10 * s, -160 * s]], wash='#E8B04A', fill='#B97A2A', fillOp=70, ink=INK, sw=.9, curv=.2)
    pop()
    if on > 0:
        lx = x + (60 if not flip else -60) * s
        glow(lx, y - 170 * s, 300 * s, '#FFD48A', .9 * on)


def shelf(x, y, w, items=(), key='shelf'):
    boilSeed(key)
    paint(rectPts(x, y, w, 22), wash='#6B4A3E', ink=INK, sw=.9, lite=True)
    for it in items:
        it()


def deerHatAlone(x, y, s, key='dh'):
    """the detective deerstalker from 疑心病, resting on a shelf"""
    push()
    translate(x, y)
    boilSeed(key)
    u = s
    dome = []
    for i in range(15):
        a = math.pi + i / 14 * math.pi
        dome.append([math.cos(a) * 4.3 * u, math.sin(a) * 3.0 * u])
    paint(dome, wash='#C9A06A', ink=None)
    for k in range(-3, 4):
        inkLine([[k * 1.15 * u, 0], [k * 1.0 * u, (-2.6 + abs(k) * .3) * u]], .5, '#8E6A3E', 'inkfine', .3)
    paint(dome, ink=INK, sw=.9)
    paint([[2.8 * u, -.3 * u], [6.0 * u, .3 * u], [5.6 * u, .8 * u], [2.6 * u, .4 * u]], wash=mixCol('#C9A06A', INK, .18), ink=INK, sw=.8, curv=.2)
    paint(ellPts(0, -3.05 * u, .5 * u, .5 * u, 10), wash='#8E6A3E', ink=INK, sw=.6)
    pop()


def photoFrame(x, y, w, h, draw=None, key='pf', rot=0.0, col='#E8D3B8'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-w / 2, -h, w, h), wash=col, ink=INK, sw=.9, lite=True)
    paint(rectPts(-w / 2 + 10, -h + 10, w - 20, h - 20), wash='#F6E7C8', ink=INK, sw=.6, lite=True)
    if draw:
        G.c.save()
        G.c.clipRect(skia.Rect.MakeXYWH(-w / 2 + 10, -h + 10, w - 20, h - 20))
        draw(-w / 2 + 10, -h + 10, w - 20, h - 20)
        G.c.restore()
    pop()


def mug(x, y, s=1.0, key='mug', col='#E8E1D2', steam=0.0, t=0.0):
    boilSeed(key)
    paint(rrPts(x - 34 * s, y - 70 * s, 68 * s, 70 * s, 10 * s), wash=col, fill=mixCol(col, INK, .2), fillOp=60, ink=INK, sw=.8)
    inkLine([[x + 34 * s, y - 55 * s], [x + 56 * s, y - 45 * s], [x + 52 * s, y - 20 * s], [x + 34 * s, y - 16 * s]], 1.6 * s, INK, 'ink', .5)
    if steam > 0:
        for i in range(2):
            ph = frac(t * .4 + i * .5)
            yy = y - 80 * s - ph * 90 * s
            inkLine([[x - 10 * s + i * 20 * s, y - 80 * s], [x - 20 * s + i * 20 * s + math.sin(t * 2 + i) * 10, yy + 40 * s], [x - 5 * s + i * 20 * s, yy]], 1.0,
                    mixCol('#FFFFFF', INK, .2), 'inkfine', .6)


# ================================================================ bench (split so sitters go between back and seat)
def benchBack(x, y, s, key='bench', col='#C98B5A'):
    boilSeed(key + 'b')
    for lx in (-2.3, 2.1):
        paint(rectPts(x + lx * s, y - 2.9 * s, .22 * s, 1.6 * s), wash=mixCol(col, INK, .35), ink=INK, sw=.8, lite=True)
    paint(rectPts(x - 2.8 * s, y - 2.75 * s, 5.6 * s, .3 * s), wash=col, ink=INK, sw=.9, lite=True)
    paint(rectPts(x - 2.8 * s, y - 2.3 * s, 5.6 * s, .28 * s), wash=col, ink=INK, sw=.9, lite=True)


def benchSeat(x, y, s, key='bench', col='#C98B5A'):
    boilSeed(key + 's')
    for lx in (-2.3, 2.1):
        paint(rectPts(x + lx * s, y - 1.35 * s, .25 * s, 1.35 * s), wash=mixCol(col, INK, .35), ink=INK, sw=.8, lite=True)
    paint(rectPts(x - 2.85 * s, y - 1.55 * s, 5.7 * s, .36 * s), wash=mixCol(col, '#FFFFFF', .08), fill=mixCol(col, INK, .2), fillOp=60, ink=INK, sw=.9, lite=True)


def seatY(y, s):
    """ground point to pass to clawd(noLegs=True) so it sits on benchSeat(x, y, s)"""
    return y - 1.45 * s


def legsDangle(x, y, u, view='front', col='#A84D33', swing=0.0):
    """two little legs hanging over the seat front (drawn after the seat)"""
    xs = (-2.6, 1.6) if view == 'front' else ((-1.2, .8) if view == 'side' else (-2.2, 1.2))
    for i, lx in enumerate(xs):
        boilSeed(f'leg{x:.0f}{i}')
        sw_ = math.sin(swing + i * 1.7) * .35 * u
        paint(rectPts(x + lx * u + sw_ * .3, y - .1 * u, u, 1.9 * u), wash=col, ink=INK, sw=clamp(u / 15, .45, 2.4) * .8, lite=True)


# ================================================================ the school yard with the gardenia hedge
def yardSet(t, mode='day', wind=0.0, key='yd', sun=True, building=True):
    night = 1.0 if mode == 'night' else 0.0
    dusk = 1.0 if mode == 'dusk' else 0.0
    if mode == 'day':
        gradRect(-400, -600, W + 800, 1200, ['#7FC3EA', '#CBE8F2', '#F3F1E2'])
    elif mode == 'dusk':
        gradRect(-400, -600, W + 800, 1200, ['#4B3D7A', '#B3698E', '#F2A77A'])
    else:
        gradRect(-400, -600, W + 800, 1200, ['#141A45', '#26306A', '#3B3F78'])
        stars(t, 31, 50, -200, -200, W + 200, 380, .9, 2.6)
    if mode == 'day' and sun:
        glow(1580, 90, 520, '#FFF2C0', .7)
        puff(330, 150, 34, '#FFFFFF', key + 'c1')
        puff(1180, 90, 24, '#FFFFFF', key + 'c2')
    if mode == 'dusk':
        glow(1500, 470, 700, '#FFB27A', .6)
    if mode == 'night':
        glow(1560, 120, 260, '#E8E4FF', .5)
        boilSeed(key + 'moon')
        paint(ellPts(1560, 120, 40, 40, 24), wash='#FFF8E4', ink=None)
    # school building
    if building:
        wallc = mixCol(mixCol('#F1E6CF', '#B48A9C', dusk * .6), '#3C4680', night * .8)
        boilSeed(key + 'bld')
        paint(rectPts(-160, 250, 2240, 380), wash=wallc, fill=mixCol(wallc, INK, .2), fillOp=40, ink=INK, sw=1.0)
        paint(rectPts(-180, 222, 2280, 40), wash=mixCol(mixCol('#C8664F', '#7A4A6A', dusk * .5), '#2C2F5E', night * .7), ink=INK, sw=1.0, lite=True)
        for r in range(2):
            for c in range(13):
                x = -60 + c * 165
                y = 300 + r * 130
                lit = night > 0 and hash1(c * 3 + r * 7) < .25
                wc = '#FFD98A' if lit else mixCol(mixCol('#A9D3EC', '#C7A0B8', dusk * .6), '#24295A', night * .8)
                boilSeed(f'{key}w{r}{c}')
                paint(rectPts(x, y, 92, 82), wash=wc, ink=INK, sw=.7, lite=True)
                G.c.drawLine(x + 46, y, x + 46, y + 82, skia.Paint(AntiAlias=True, Color=skcol(INK, .5), StrokeWidth=1.4))
        boilSeed(key + 'clk')
        paint(ellPts(960, 205, 54, 54, 24), wash=mixCol('#FFFDF4', '#8A90C0', night * .6), ink=INK, sw=1.0)
        inkLine([[960, 205], [960, 170]], 1.2, INK, 'ink', 0)
        inkLine([[960, 205], [985, 215]], 1.2, INK, 'ink', 0)
    # low wall
    lw = mixCol(mixCol('#E9E2D6', '#A98AA6', dusk * .5), '#2E3466', night * .8)
    boilSeed(key + 'lw')
    paint(rectPts(-160, 560, 2240, 200), wash=lw, ink=INK, sw=.9, lite=True)
    # gardenia hedge (sways with wind)
    push()
    translate(960, 780)
    G.c.skew(.05 * wind * math.sin(t * 2.1), 0)
    translate(-960, -780)
    gardeniaBush(960, 780, 2000, 300, t, key + 'gb', flowers=34, night=night * .9 + dusk * .3)
    pop()
    # ground
    gc = mixCol(mixCol('#E3CFA2', '#B78A86', dusk * .5), '#2A2E55', night * .85)
    boilSeed(key + 'gr')
    paint(rectPts(-200, 770, 2320, 520), wash=gc, fill=mixCol(gc, INK, .15), fillOp=50, ink=None)
    inkLine([[-200, 772], [960, 776], [2120, 770]], .9, mixCol(gc, INK, .5), 'ink', .3)
    # dappled light / lamp pool
    if mode == 'day':
        for i in range(9):
            hx, hy = hash1(i * 4.1 + 2), hash1(i * 2.3 + 5)
            G.c.drawOval(skia.Rect.MakeXYWH(-100 + hx * 2100, 820 + hy * 220, 70 + 60 * hash1(i), 22 + 12 * hash1(i + 3)),
                         skia.Paint(AntiAlias=True, Color=skcol('#FFF6D8', .35)))
    if mode == 'night':
        glow(1500, 760, 520, '#FFD48A', .45)


def yardLamp(x, y, on=1.0, key='yl'):
    lamp(x, y, 46, on, key=key)


# ================================================================ summer night hill
def hillSet(t, nightK=1.0, key='hill', milky=1.0, starsK=1.0, horizon=760):
    top = mixCol('#E28B6A', '#0F1442', nightK)
    mid = mixCol('#F2B27E', '#28306E', nightK)
    low = mixCol('#FBD6A0', '#4A4A8A', nightK)
    gradRect(-400, -700, W + 800, horizon + 760, [top, mid, low])
    if nightK > .2:
        milkyWay(milky * clamp((nightK - .2) / .8))
        stars(t, 7, 160, -300, -600, W + 300, horizon - 60, starsK * clamp((nightK - .1) / .9), 3.0)
    if nightK < .6:
        glow(1500, horizon - 40, 600, '#FFC48A', .7 * (1 - nightK / .6))
    # far town lights
    boilSeed(key + 'far')
    paint([[-300, horizon + 30], [-300, horizon - 20]] + [[-300 + i * 120, horizon - 20 - 30 * hash1(i * 2.2)] for i in range(23)] + [[W + 300, horizon + 30]],
          wash=mixCol('#7C6A8E', '#1C214E', nightK), ink=None)
    for i in range(40):
        x = -200 + hash1(i * 3.1) * (W + 400)
        G.c.drawCircle(x, horizon - 6 + hash1(i * 5.3) * 18, 2.2, skia.Paint(AntiAlias=True, Color=skcol('#FFD98A', .85 * nightK)))
    # the hill
    hc = mixCol('#7FA35A', '#1D2F45', nightK)
    boilSeed(key + 'h')
    P = [[-300, H + 400]]
    for i in range(31):
        x = -300 + i * (W + 600) / 30
        k = (x - 960) / 1300
        P.append([x, horizon - 40 + 260 * k * k - 40 * math.sin(i * .9)])
    P.append([W + 300, H + 400])
    paint(P, wash=hc, fill=mixCol(hc, INK, .3), fillOp=80, ink=INK, sw=1.0, curv=.3)
    # grass tufts
    for i in range(46):
        x = -250 + hash1(i * 1.7) * (W + 500)
        k = (x - 960) / 1300
        y = horizon - 30 + 260 * k * k + 40 + hash1(i * 4.4) * 300
        sw_ = math.sin(t * 1.5 + i) * 6
        boilSeed(f'{key}g{i}')
        for j in range(3):
            inkLine([[x + j * 8, y], [x + j * 8 + sw_ + (j - 1) * 6, y - 26 - 10 * hash1(i + j)]], .7, mixCol(hc, '#BFD9A0', .25), 'inkfine', .3)
    fireflies(t, 5, 16, 0, horizon - 120, W, H, nightK)


def hillY(x, horizon=760):
    k = (x - 960) / 1300
    return horizon - 40 + 260 * k * k


# ================================================================ present-day city facade with her window
def facade(t, litK=1.0, key='fac', winX=960, winY=520, winW=300, winH=330, inside=None, fogK=0.0):
    gradRect(-400, -1400, W + 800, 1600, ['#0E1238', '#1E2457', '#323A78'])
    stars(t, 23, 70, -300, -1300, W + 300, 120, .9, 2.8)
    glow(1500, -900, 220, '#E8E4FF', .5)
    boilSeed(key + 'moon')
    paint(ellPts(1500, -900, 42, 42, 24), wash='#FFF8E4', ink=None)
    boilSeed(key)
    paint(rectPts(-200, 140, W + 400, 1400), wash='#3B4384', fill='#2C3370', fillOp=70, ink=INK, sw=1.0)
    gradRect(-200, 140, W + 400, 1400, ['#3B4384', '#2A3068'])
    for r in range(-1, 4):
        yslab = winY - winH / 2 + r * (winH + 110) - 55
        flatRect(-200, yslab - 8, W + 400, 16, '#2A2F63')
    cols = ['#FFCF85', '#FFB98A', '#FFE2A0']
    for r in range(-1, 4):
        for c in range(-2, 7):
            x = winX - winW / 2 + (c - 2) * (winW + 120)
            y = winY - winH / 2 + r * (winH + 110)
            mine = (c == 2 and r == 0)
            if mine:
                continue
            on = hash1(c * 5 + r * 11 + 3) < .3
            boilSeed(f'{key}w{r}{c}')
            col = cols[(c + r) % 3]
            paint(rectPts(x, y, winW, winH), wash=col if on else '#1B2050', washOp=230, ink=INK, sw=.8, lite=True)
            if on:
                glow(x + winW / 2, y + winH / 2, winW * .75, col, .22)
                for s_ in (-1, 1):
                    cx_ = x + winW / 2 + s_ * winW * .36
                    paint(rectPts(cx_ - winW * .14, y + 6, winW * .28, winH - 12), wash='#C98A7A' if (c + r) % 2 else '#8A9AC8', washOp=200, ink=None, lite=True)
                if hash1(c * 7 + r) < .4:
                    clawd(x + winW * .5, y + winH + 10, 9, dict(col='#2A2440', dk='#1E1A30', lt='#3A3456', view='side', flip=hash1(c + r) < .5, noLegs=True,
                                                         noShadow=True, lite=True, boilKey=f'sil{r}{c}', eyes='closed'))
            G.c.drawLine(x + winW / 2, y, x + winW / 2, y + winH, skia.Paint(AntiAlias=True, Color=skcol('#11132F', .85), StrokeWidth=5))
            G.c.drawLine(x, y + winH * .4, x + winW, y + winH * .4, skia.Paint(AntiAlias=True, Color=skcol('#11132F', .85), StrokeWidth=5))
            paint(rectPts(x - 16, y + winH, winW + 32, 16), wash='#4A528E', ink=INK, sw=.6, lite=True)
            if hash1(c * 3.3 + r * 1.7) < .25:
                paint(rectPts(x + winW - 90, y + winH + 16, 80, 54), wash='#7E86B4', ink=INK, sw=.6, lite=True)
                for k in range(4):
                    G.c.drawLine(x + winW - 84, y + winH + 26 + k * 10, x + winW - 16, y + winH + 26 + k * 10,
                                 skia.Paint(AntiAlias=True, Color=skcol(INK, .4), StrokeWidth=1.5))
    x, y = winX - winW / 2, winY - winH / 2
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(x, y, winW, winH))
    gradRect(x, y, winW, winH, [mixCol('#1A1F48', '#FFD594', litK), mixCol('#1A1F48', '#F2A96A', litK)])
    if inside:
        inside(x, y, winW, winH)
    for s_ in (-1, 1):
        cx_ = x + winW / 2 + s_ * winW * .42
        paint(rectPts(cx_ - winW * .1, y, winW * .2, winH), wash='#E8B6A8', washOp=220, ink=None, lite=True)
    if fogK > 0:
        flatRect(x, y, winW, winH, '#E9EEF8', .45 * fogK)
    G.c.restore()
    glow(winX, winY, winW * 1.1, '#FFC976', .35 * litK)
    windowFrame(x, y, winW, winH, '#7A5A4E', bars=False, key=key + 'f')


# ================================================================ watering can / book / flower hooks
def canHook(tilt=0.0):
    def h(u, sw):
        push()
        rotate(tilt)
        boilSeed('can')
        paint(rrPts(-.2 * u, -1.0 * u, 2.2 * u, 1.6 * u, .3 * u), wash='#7FB8C9', fill='#4E8AA0', fillOp=60, ink=INK, sw=sw * .7, lite=True)
        inkLine([[1.9 * u, -.5 * u], [3.2 * u, -1.4 * u]], sw * 1.6, '#4E8AA0', 'ink', 0)
        paint(ellPts(3.3 * u, -1.45 * u, .35 * u, .22 * u, 10, 0, -.6), wash='#4E8AA0', ink=INK, sw=sw * .5, lite=True)
        pop()
    return h


def bookHook(open_=1.0, col='#C8564F'):
    def h(u, sw):
        boilSeed('book')
        push()
        translate(0, 1.15 * u)
        scale(.72)
        y = -4.0 * u
        paint([[-2.4 * u, y - 1.3 * u], [0, y - 1.0 * u], [2.4 * u, y - 1.3 * u], [2.4 * u, y + .6 * u], [0, y + .9 * u], [-2.4 * u, y + .6 * u]], wash=col, ink=INK, sw=sw * .7, lite=True)
        paint([[-2.2 * u, y - 1.15 * u], [0, y - .85 * u], [0, y + .7 * u], [-2.2 * u, y + .45 * u]], wash='#FFF8E6', ink=INK, sw=sw * .5, lite=True)
        paint([[0, y - .85 * u], [2.2 * u, y - 1.15 * u], [2.2 * u, y + .45 * u], [0, y + .7 * u]], wash='#FFF8E6', ink=INK, sw=sw * .5, lite=True)
        for i in range(3):
            for s_ in (-1, 1):
                yy = y - .55 * u + i * .38 * u
                inkLine([[s_ * .35 * u, yy + .05 * u], [s_ * 1.85 * u, yy - .12 * u]], sw * .3, '#9A9AA8', 'inkfine', 0)
        pop()
    return h


def flowerHook(k=1.0):
    def h(u, sw):
        gardeniaFlower(.6 * u, -.2 * u, .9 * u * k, 1, key='hf')
    return h


# ================================================================ her / his room (his = mirror image of hers)
ROOM = dict(win=(220, 120, 660, 500), pot=(1262, 760, 30), desk=(1180, 760), lamp=(1720, 760), floor=1010, chairX=1040, sitY=834)


def curtain(x, y, h, side=1, sway=0.0, col='#8C7AA8', key='cur'):
    boilSeed(key)
    P = [[x, y - 10], [x + side * 150, y - 10]]
    for i in range(1, 11):
        yy = y + i * h / 10
        P.append([x + side * (150 - 40 * math.sin(i * .5) + sway * 30 * i / 10 * math.sin(i * .8 + G.T * 2)), yy])
    P.append([x, y + h])
    paint(P, wash=col, fill=mixCol(col, INK, .3), fillOp=80, ink=INK, sw=.9, curv=.3)
    for k in range(1, 4):
        inkLine([[x + side * 38 * k, y], [x + side * (38 * k + 10), y + h]], .6, mixCol(col, INK, .4), 'inkfine', .4)


def chair(x, y_floor, seat_y, key='ch', flip=False):
    boilSeed(key)
    d = -1 if flip else 1
    paint(rectPts(x - 60, seat_y, 120, 22), wash='#7A5544', ink=INK, sw=.8, lite=True)
    for lx in (-50, 40):
        paint(rectPts(x + lx, seat_y + 20, 12, y_floor - seat_y - 20), wash='#5E3F33', ink=INK, sw=.7, lite=True)
    paint(rectPts(x - d * 62 - 6, seat_y - 230, 14, 250), wash='#5E3F33', ink=INK, sw=.7, lite=True)


def roomSet(t, who='her', lampK=1.0, potOpen=0.0, potBuds=3, rainK=0.0, fogK=0.0, curtainSway=0.0, shelfHat=True, cityK=1.0,
            moonXY=None, wall=None, windowOpen=0.0, starsK=1.0, diaryOnDesk=True, mugSteam=1.0):
    mirror = who == 'him'
    push()
    if mirror:
        translate(W, 0)
        scale(-1, 1)
    wx, wy, ww, wh = ROOM['win']
    c1, c2 = wall or (('#2B3168', '#454A86') if not mirror else ('#23384F', '#3B5470'))
    lx, ly = ROOM['lamp']
    roomWall(c1, c2, (lx + 40, ly - 170), lampK)
    windowView(wx, wy, ww, wh, t, moonXY=moonXY, cityK=cityK, rainK=rainK, fogK=fogK, starsK=starsK, key='wv' + who)
    windowFrame(wx, wy, ww, wh, '#6B4A3E' if not mirror else '#5A4A42', key='wf' + who)
    curtain(wx - 30, wy - 30, wh + 80, -1, curtainSway, '#8C7AA8' if not mirror else '#6F8A9A', key='cu' + who)
    px, py, ps = ROOM['pot']
    potGardenia(px, py, ps, potBuds, potOpen, key='pot' + who)
    # shelf
    sx, sy = 1330, 330
    boilSeed('sh' + who)
    paint(rectPts(sx, sy, 470, 22), wash='#6B4A3E', ink=INK, sw=.9, lite=True)
    if not mirror:
        if shelfHat:
            deerHatAlone(sx + 120, sy, 15, key='shhat')
        photoFrame(sx + 330, sy, 110, 130, draw=lambda x, y, w, h: _miniCouple(x, y, w, h), key='shpf')
    else:
        for i, (bw, bc) in enumerate([(34, '#C8564F'), (28, '#5B7FC4'), (40, '#E8B04A'), (30, '#7FB1B5')]):
            paint(rectPts(sx + 60 + i * 44, sy - 150 + (i % 2) * 14, bw, 150 - (i % 2) * 14), wash=bc, ink=INK, sw=.7, lite=True)
        photoFrame(sx + 340, sy, 110, 130, draw=lambda x, y, w, h: _miniCouple(x, y, w, h, faded=True), key='shpf2')
    # floor
    fl = ROOM['floor']
    gradRect(-300, fl, W + 600, 500, ['#4A3A4E', '#2E2436'])
    for i in range(6):
        G.c.drawLine(-300, fl + 20 + i * 34 * (1 + i * .3), W + 300, fl + 20 + i * 34 * (1 + i * .3), skia.Paint(AntiAlias=True, Color=skcol('#251C2C', .6), StrokeWidth=2))
    # desk
    dx, dy = ROOM['desk']
    boilSeed('dk' + who)
    paint(rectPts(dx, dy, 900, 26), wash='#A97A55', fill='#7A5038', fillOp=60, ink=INK, sw=1.0)
    paint(rectPts(dx + 20, dy + 26, 860, fl - dy - 26), wash='#7A5038', fill='#5A3828', fillOp=60, ink=INK, sw=.9, lite=True)
    for k in range(2):
        paint(rectPts(dx + 80 + k * 420, dy + 70, 330, 90), wash='#86593F', ink=INK, sw=.7, lite=True)
        paint(ellPts(dx + 245 + k * 420, dy + 115, 10, 10, 10), wash='#D9B45A', ink=None)
    deskLamp(lx, ly, 1.0, lampK, key='lmp' + who, flip=not mirror)
    if diaryOnDesk:
        boilSeed('dd' + who)
        paint([[1360, dy - 4], [1390, dy - 18], [1460, dy - 22], [1490, dy - 6], [1520, dy - 22], [1590, dy - 18], [1620, dy - 4]],
              wash=PAGE, ink=INK, sw=.8, curv=.2, lite=True)
        paint(rectPts(1352, dy - 6, 276, 8), wash='#6E3B42', ink=INK, sw=.6, lite=True)
    mug(1880, dy, .8, key='mug' + who, steam=mugSteam, t=t)
    pop()


def _miniCouple(x, y, w, h, faded=False):
    gradRect(x, y, w, h, ['#9FD4F2', '#F3E6C8'])
    clawd(x + w * .36, y + h * .9, 5, dict(col=PINK, dk='#C0637B', lt='#FBD0DA', hat='flower', eyes='happy', mouth='smile', lite=True, noShadow=True, boilKey='mc1'))
    clawd(x + w * .66, y + h * .9, 5, dict(col=PAL['clay'], dk=PAL['clayDk'], lt='#F5B394', eyes='happy', mouth='smile', lite=True, noShadow=True, boilKey='mc2'))
    if faded:
        flatRect(x, y, w, h, '#F3E6C8', .35)


def mirrorX(x):
    return W - x
