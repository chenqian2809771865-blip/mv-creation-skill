# eng.py: watercolour-and-ink painting engine in Skia, a port of the painted-animation template (core.js).
# Logical canvas 1920x1080 (same numbers as the JS template), rendered at OUT_W x OUT_H.
# Every frame is a pure function of t. Randomness comes from boilSeed(key) so linework "boils" at 12 fps.
import math, random, os
import numpy as np
import skia

W, H = (int(v) for v in os.environ.get('MV_CANVAS', '1920x1080').split('x'))
OUT_W, OUT_H = (int(v) for v in os.environ.get('MV_OUT', '2560x1440').split('x'))
SC = OUT_W / W
FPS = 24
BOIL = 8
TAU = math.pi * 2
HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, '..', 'fonts')

PAL = dict(paper='#F3EBDC', ink='#2B2233', clay='#D97757', clayDk='#A84D33', clayLt='#F2A283',
           night='#1F2550', indigo='#2F3C7A', rose='#E27A92', ochre='#E8AA38', sap='#6E9F58',
           teal='#3A9C98', violet='#7B5CA8', cream='#FFF5E2', sky='#8EC3E6')
INK = PAL['ink']


class _G:
    c = None          # skia canvas
    T = 0.0
    BOILN = 0
    CLAWD_N = 0
    BPM = 128.0
    OFF = 0.0
    BEATS = None      # measured beat times (optional) for bpOf


G = _G()
RNG = random.Random(0)


# ---------------- small helpers ----------------
def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def lerp(a, b, x):
    return a + (b - a) * x


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def easeOut(x):
    return 1 - (1 - clamp(x)) ** 3


def easeIn(x):
    return clamp(x) ** 3


def backOut(x):
    x = clamp(x)
    s = 1.9
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


def elasticOut(x):
    x = clamp(x)
    if x == 0 or x == 1:
        return x
    return 2 ** (-10 * x) * math.sin((x * 10 - .75) * (TAU / 3)) + 1


def hash1(i):
    x = math.sin(i * 127.1 + 311.7) * 43758.5453
    return x - math.floor(x)


def frac(x):
    return x - math.floor(x)


def seg(t, a, b):
    return clamp((t - a) / (b - a)) if b != a else (1.0 if t >= b else 0.0)


def boilSeed(key):
    h = 2166136261
    for ch in f'{key}|{G.BOILN}':
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    RNG.seed(h)


def jit(a):
    return (RNG.random() * 2 - 1) * a


def rnd():
    return RNG.random()


# beat position: uses the measured beat list when given (tempo drift), else BPM/OFF
def bpOf(t):
    B = G.BEATS
    if B is not None:
        n = len(B)
        if t <= B[0]:
            return (t - B[0]) / (B[1] - B[0])
        if t >= B[-1]:
            return (n - 1) + (t - B[-1]) / (B[-1] - B[-2])
        i = int(np.searchsorted(B, t) - 1)
        return i + (t - B[i]) / (B[i + 1] - B[i])
    return (t - G.OFF) / (60.0 / G.BPM)


def beatN(t):
    return math.floor(bpOf(t))


def pulse(t, k=6):
    return math.exp(-frac(bpOf(t)) * k)


def pulse2(t, k=6):
    return math.exp(-frac(bpOf(t) * 2) * k)


def wob(t, f=1, ph=0):
    return math.sin((t * f + ph) * TAU)


def kf(t, keys, e=ease):
    if t <= keys[0][0]:
        return keys[0][1]
    for i in range(1, len(keys)):
        if t < keys[i][0]:
            a, va = keys[i - 1]
            b, vb = keys[i]
            k = e((t - a) / (b - a))
            if isinstance(va, (list, tuple)):
                return [lerp(p, q, k) for p, q in zip(va, vb)]
            return lerp(va, vb, k)
    return keys[-1][1]


def spring(t, t0, k=6, w=18):
    return 0 if t < t0 else math.exp(-k * (t - t0)) * math.sin(w * (t - t0))


def ring(t, evs, k=6, w=18):
    return sum(spring(t, e, k, w) for e in evs)


def onTwos(t):
    return math.floor(t * 12 + 1e-6) / 12


def arcPt(p0, p1, h, k):
    return [lerp(p0[0], p1[0], k), lerp(p0[1], p1[1], k) - h * 4 * k * (1 - k)]


def jump(t, t0, t1, h=3):
    if t < t0 - .12:
        return dict(dy=0, sq=0)
    if t < t0:
        return dict(dy=0, sq=.18 * ease(seg(t, t0 - .12, t0)))
    if t < t1:
        k = (t - t0) / (t1 - t0)
        return dict(dy=-h * 4 * k * (1 - k), sq=-.16 * abs(1 - 2 * k))
    a = t - t1
    return dict(dy=0, sq=.22 * math.exp(-8 * a) * math.cos(20 * a))


def take(t, t0, amt=1):
    if t < t0 - .1:
        return dict(sq=0, dy=0)
    if t < t0:
        return dict(sq=.12 * amt * ease(seg(t, t0 - .1, t0)), dy=0)
    a = t - t0
    return dict(sq=-.26 * amt * math.exp(-6 * a) * math.cos(16 * a),
                dy=-1.2 * amt * math.exp(-7 * a) * max(0, math.cos(9 * a)))


def stroll(t, t0, t1, x0, x1, u):
    x = lerp(x0, x1, ease(seg(t, t0, t1)))
    d = abs(x - x0) / (4 * u)
    moving = t0 < t < t1
    return dict(x=x, walk=d, view='q' if moving else 'front', flip=x1 < x0,
                dy=-abs(math.sin(d * math.pi)) * .5 if moving else 0)


def shakeXY(t, amt):
    f = math.floor(t * 24)
    return ((hash1(f * 1.7) - .5) * 2 * amt, (hash1(f * 2.3 + 9) - .5) * 2 * amt)


# ---------------- colour ----------------
_hx = {}


def rgb(c):
    v = _hx.get(c)
    if v is None:
        s = c.lstrip('#')
        v = (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))
        _hx[c] = v
    return v


def mixCol(a, b, k):
    pa, pb = rgb(a), rgb(b)
    k = clamp(k)
    return '#%02x%02x%02x' % tuple(int(round(lerp(pa[i], pb[i], k))) for i in range(3))


def skcol(c, a=1.0):
    r, g, b = rgb(c)
    return skia.Color(r, g, b, int(255 * clamp(a)))


# ---------------- canvas transform (p5-like) ----------------
def push():
    G.c.save()


def pop():
    G.c.restore()


def translate(x, y):
    G.c.translate(x, y)


def rotate(a):
    if a:
        G.c.rotate(math.degrees(a))


def scale(sx, sy=None):
    G.c.scale(sx, sx if sy is None else sy)


CAM = None


def camBegin(cx=W / 2, cy=H / 2, zoom=1, rot=0):
    global CAM
    push()
    translate(W / 2, H / 2)
    rotate(rot)
    scale(zoom)
    translate(-cx, -cy)
    CAM = (cx, cy, zoom, rot)


def camEnd():
    global CAM
    pop()
    CAM = None


def toScreen(x, y, cam=None):
    cam = cam or CAM
    if not cam:
        return x, y
    cx, cy, z, r = cam
    c, s = math.cos(r), math.sin(r)
    dx, dy = (x - cx) * z, (y - cy) * z
    return W / 2 + dx * c - dy * s, H / 2 + dx * s + dy * c


# ---------------- geometry ----------------
def rectPts(x, y, w, h, j=0):
    return [[x + jit(j), y + jit(j)], [x + w / 2 + jit(j), y + jit(j) * .5], [x + w + jit(j), y + jit(j)],
            [x + w + jit(j) * .5, y + h / 2], [x + w + jit(j), y + h + jit(j)], [x + w / 2 + jit(j), y + h + jit(j) * .5],
            [x + jit(j), y + h + jit(j)], [x + jit(j) * .5, y + h / 2]]


def ellPts(cx, cy, rx, ry, n=28, j=0, rot=0):
    out = []
    for i in range(n):
        a = rot + i / n * TAU
        out.append([cx + math.cos(a) * rx + jit(j), cy + math.sin(a) * ry + jit(j)])
    return out


def rrPts(x, y, w, h, r, j=0):
    p = []
    seg_ = 5

    def corner(cx, cy, a0):
        for i in range(seg_ + 1):
            a = a0 + i / seg_ * math.pi / 2
            p.append([cx + math.cos(a) * r + jit(j), cy + math.sin(a) * r + jit(j)])
    corner(x + w - r, y + r, -math.pi / 2)
    corner(x + w - r, y + h - r, 0)
    corner(x + r, y + h - r, math.pi / 2)
    corner(x + r, y + r, math.pi)
    return p


def starPts(cx, cy, r, inner=.38, n=4, rot=-math.pi / 2):
    p = []
    for i in range(n * 2):
        a = rot + i * math.pi / n
        q = r * inner if i % 2 else r
        p.append([cx + math.cos(a) * q, cy + math.sin(a) * q])
    return p


def heartPts(cx, cy, r, n=22):
    p = []
    for i in range(n):
        a = i / n * TAU
        p.append([cx + 16 * math.sin(a) ** 3 * r / 16,
                  cy - (13 * math.cos(a) - 5 * math.cos(2 * a) - 2 * math.cos(3 * a) - math.cos(4 * a)) * r / 16])
    return p


def through(P, n=6):
    P = [list(p) for p in P]
    if len(P) < 3:
        return P
    out = []
    m = len(P)
    for i in range(m - 1):
        p0, p1, p2, p3 = P[max(0, i - 1)], P[i], P[i + 1], P[min(m - 1, i + 2)]
        for k in range(n):
            u = k / n
            u2, u3 = u * u, u * u * u
            out.append([.5 * (2 * p1[d] + (p2[d] - p0[d]) * u + (2 * p0[d] - 5 * p1[d] + 4 * p2[d] - p3[d]) * u2 +
                              (3 * p1[d] - p0[d] - 3 * p2[d] + p3[d]) * u3) for d in (0, 1)])
    out.append(P[-1])
    return out


def throughClosed(P, n=5):
    P = [list(p) for p in P]
    m = len(P)
    out = []
    for i in range(m):
        p0, p1, p2, p3 = P[(i - 1) % m], P[i], P[(i + 1) % m], P[(i + 2) % m]
        for k in range(n):
            u = k / n
            u2, u3 = u * u, u * u * u
            out.append([.5 * (2 * p1[d] + (p2[d] - p0[d]) * u + (2 * p0[d] - 5 * p1[d] + 4 * p2[d] - p3[d]) * u2 +
                              (3 * p1[d] - p0[d] - 3 * p2[d] + p3[d]) * u3) for d in (0, 1)])
    return out


def ribbon(P, w0, w1=None):
    if w1 is None:
        w1 = w0
    C = through(P)
    n = len(C)
    L, R = [], []
    for i in range(n):
        a, b = C[max(0, i - 1)], C[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        d = math.hypot(dx, dy) or 1
        w = lerp(w0, w1, i / max(1, n - 1)) / 2
        L.append([C[i][0] - dy / d * w, C[i][1] + dx / d * w])
        R.append([C[i][0] + dy / d * w, C[i][1] - dx / d * w])
    return L + R[::-1]


def _path(P, close=True):
    p = skia.Path()
    p.addPoly([skia.Point(float(x), float(y)) for x, y in P], close)
    return p


# ---------------- paint ----------------
_mf = {}


def _blur(s):
    s = max(.5, round(s * 2) / 2)
    m = _mf.get(s)
    if m is None:
        m = skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, s)
        _mf[s] = m
    return m


def _subdiv(P, maxlen):
    out = []
    n = len(P)
    for i in range(n):
        a, b = P[i], P[(i + 1) % n]
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        k = max(1, int(d / maxlen))
        for j in range(k):
            out.append([lerp(a[0], b[0], j / k), lerp(a[1], b[1], j / k)])
    return out


_DEF = object()


def paint(pts, wash=None, washOp=255, fill=None, fillOp=170, bleed=.1, tex=.4, border=.35, ink=_DEF, sw=1,
          curv=0, br='ink', lite=False):
    if not pts or len(pts) < 2:
        return
    P = throughClosed(pts, 4) if curv else pts
    c = G.c
    if wash:
        pa = skia.Paint(AntiAlias=True, Color=skcol(wash, washOp / 255))
        c.drawPath(_path(P), pa)
    if fill:
        wcFill(P, fill, fillOp, bleed, tex, border, lite)
    if ink is not None:
        inkStroke(P, True, sw, INK if ink is _DEF else ink, br)


def wcFill(P, col, op, bleed, tex, border, lite=False):
    xs = [p[0] for p in P]
    ys = [p[1] for p in P]
    bw, bh = max(xs) - min(xs), max(ys) - min(ys)
    size = max(3.0, math.sqrt(max(1.0, bw * bh)))
    cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
    a = op / 255
    Q = _subdiv(P, max(6, size * .22)) if not lite else P
    c = G.c
    layers = 2 if lite else 3
    for i in range(layers):
        R = []
        for (x, y) in Q:
            dx, dy = x - cx, y - cy
            d = math.hypot(dx, dy) or 1
            m = jit(bleed * size * .30) + size * .012
            R.append([x + dx / d * m, y + dy / d * m])
        pa = skia.Paint(AntiAlias=True, Color=skcol(col, a * (.62 if lite else .44)))
        if not lite:
            pa.setMaskFilter(_blur(min(14, size * (.015 + bleed * .06))))
        c.drawPath(_path(R), pa)
    if border > .05 and not lite:
        pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1.2, min(9, size * .045 * border)),
                        Color=skcol(mixCol(col, INK, .18), a * .28 * border))
        pa.setMaskFilter(_blur(max(.8, min(4, size * .012))))
        c.drawPath(_path(Q), pa)


BR = {'ink': (5.0, .25, 235, 1.15, .75, .15), 'inkfine': (2.6, .15, 230, 1.1, .8, .1), 'dry': (14.0, 3, 90, 1, .6, .4)}


def inkStroke(P, closed, sw, col, br='ink'):
    wgt, scat, op, p0, p1, noise = BR.get(br, BR['ink'])
    base = wgt * sw * .9
    if base < .15:
        return
    A = np.asarray(P, dtype=float)
    if len(A) < 2:
        return
    if closed:
        A = np.vstack([A, A[:1]])
    if br == 'dry':
        _dryStroke(A, base, col, op)
        return
    # resample each segment, keeping the original vertices (crisp corners)
    step = max(2.5, base * 1.4)
    pts, vtx = [], []
    for i in range(len(A) - 1):
        a, b = A[i], A[i + 1]
        d = float(np.hypot(*(b - a)))
        k = max(1, int(d / step))
        for j in range(k):
            pts.append(a + (b - a) * (j / k))
            vtx.append(j == 0)
    pts.append(A[-1])
    vtx.append(True)
    S = np.array(pts)
    n = len(S)
    # normals: average of adjacent segment directions (miter at corners)
    d_prev = np.zeros_like(S)
    d_next = np.zeros_like(S)
    dif = S[1:] - S[:-1]
    ln = np.hypot(dif[:, 0], dif[:, 1])[:, None]
    ln[ln == 0] = 1
    u = dif / ln
    d_next[:-1] = u
    d_next[-1] = u[-1] if not closed else u[0]
    d_prev[1:] = u
    d_prev[0] = u[0] if not closed else u[-1]
    t = d_prev + d_next
    tl = np.hypot(t[:, 0], t[:, 1])[:, None]
    bad = tl[:, 0] < 1e-6
    tl[tl == 0] = 1
    t = t / tl
    t[bad] = d_next[bad]
    N = np.stack([-t[:, 1], t[:, 0]], 1)
    cosh = np.clip((N * np.stack([-d_next[:, 1], d_next[:, 0]], 1)).sum(1), .5, 1)
    # width along the stroke: pressure taper plus smooth noise
    s = np.linspace(0, 1, n)
    kn = max(2, n // 4 + 2)
    knots = np.array([jit(1) for _ in range(kn)])
    nz = np.interp(np.linspace(0, kn - 1, n), np.arange(kn), knots)
    w = base * (p0 + (p1 - p0) * s) * (1 + noise * 1.6 * nz) / cosh
    # centreline wobble (boils)
    kn2 = max(2, n // 6 + 2)
    wv = np.array([jit(1) for _ in range(kn2)])
    wob_ = np.interp(np.linspace(0, kn2 - 1, n), np.arange(kn2), wv) * scat * base * .35
    C = S + N * wob_[:, None]
    L = C + N * (w[:, None] / 2)
    R = C - N * (w[:, None] / 2)
    poly = np.vstack([L, R[::-1]])
    pa = skia.Paint(AntiAlias=True, Color=skcol(col, op / 255))
    path = _path(poly.tolist())
    G.c.drawPath(path, pa)
    if not closed:
        # round caps (drawn separately: adding them to the path can punch winding holes in short strokes)
        G.c.drawCircle(float(C[0, 0]), float(C[0, 1]), float(w[0] / 2), pa)
        G.c.drawCircle(float(C[-1, 0]), float(C[-1, 1]), float(w[-1] / 2), pa)


def _dryStroke(A, base, col, op):
    for i in range(4):
        off = jit(base * .35)
        pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=max(1, base * (.25 + .2 * rnd())),
                        Color=skcol(col, op / 255 * .8), StrokeCap=skia.Paint.kRound_Cap)
        Q = [[x + jit(base * .1), y + off] for x, y in A.tolist()]
        G.c.drawPath(_path(Q, False), pa)


def inkLine(pts, sw=1, col=INK, br='ink', curv=.5):
    if len(pts) < 2:
        return
    P = through(pts, 6) if (curv and len(pts) >= 3) else pts
    inkStroke(P, False, sw, col, br)


def flat(pts, col, a=1.0):
    """plain antialiased fill (no watercolour): for big background planes, rays, glows of colour."""
    G.c.drawPath(_path(pts), skia.Paint(AntiAlias=True, Color=skcol(col, a)))


def flatRect(x, y, w, h, col, a=1.0):
    G.c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), skia.Paint(AntiAlias=True, Color=skcol(col, a)))


def gradRect(x, y, w, h, cols, vertical=True, a=1.0):
    pts = [skia.Point(x, y), skia.Point(x, y + h) if vertical else skia.Point(x + w, y)]
    sh = skia.GradientShader.MakeLinear(pts, [skcol(c, a) for c in cols])
    G.c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), skia.Paint(AntiAlias=True, Shader=sh))


# ---------------- light ----------------
_glowImg = None


def _makeGlow():
    s = 256
    yy, xx = np.mgrid[0:s, 0:s]
    r = np.hypot(xx - s / 2 + .5, yy - s / 2 + .5) / (s / 2)
    stops = [(0, 1), (.18, .8), (.45, .32), (.75, .08), (1, 0)]
    a = np.interp(r, [p for p, _ in stops], [v for _, v in stops])
    a = np.clip(a, 0, 1)
    arr = np.zeros((s, s, 4), np.uint8)
    arr[..., 0] = arr[..., 1] = arr[..., 2] = (255 * a).astype(np.uint8)   # premultiplied white
    arr[..., 3] = (255 * a).astype(np.uint8)
    return skia.Image.fromarray(arr, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)


def glow(x, y, r, col='#FFC766', a=1.0):
    global _glowImg
    if a <= 0 or r < 1:
        return
    if _glowImg is None:
        _glowImg = _makeGlow()
    rr = r * (1 + jit(.03))
    rc, gc, bc = rgb(col)
    pa = skia.Paint(AntiAlias=True)
    pa.setBlendMode(skia.BlendMode.kPlus)
    pa.setColorFilter(skia.ColorFilters.Blend(skia.Color(rc, gc, bc, 255), skia.BlendMode.kModulate))
    pa.setAlphaf(clamp(150 / 255 * a))
    G.c.drawImageRect(_glowImg, skia.Rect.MakeXYWH(x - rr, y - rr, 2 * rr, 2 * rr), skia.SamplingOptions(skia.FilterMode.kLinear), pa)


def flash(k, col='#FFFDF6'):
    if k > .01:
        flatRect(-60, -60, W + 120, H + 120, col, clamp(k))


def irisShape(pts, col=INK, a=1.0):
    p = skia.Path()
    p.setFillType(skia.PathFillType.kEvenOdd)
    p.addRect(skia.Rect.MakeXYWH(-200, -200, W + 400, H + 400))
    p.addPoly([skia.Point(float(x), float(y)) for x, y in pts], True)
    G.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol(col, a)))


def iris(cx, cy, r, col=INK):
    if r < 4:
        flatRect(-60, -60, W + 120, H + 120, col)
    else:
        irisShape(ellPts(cx, cy, r, r, 64), col)


# ---------------- text ----------------
_tf = {}


def typeface(name):
    t = _tf.get(name)
    if t is None:
        t = skia.Typeface.MakeFromFile(os.path.join(FONT_DIR, name))
        _tf[name] = t
    return t


KUAILE = 'ZCOOLKuaiLe-Regular.ttf'
BRUSH = 'MaShanZheng-Regular.ttf'


def textW(txt, size, face=KUAILE):
    f = skia.Font(typeface(face), size)
    return f.measureText(txt)


def text(txt, x, y, size, col, face=KUAILE, align='center', stroke=None, strokeW=None, shadow=True, a=1.0, rot=0, sc=1.0):
    """Lettering for bubbles, stamps, signs. (x, y) = centre of the line (baseline-corrected)."""
    if sc <= .01 or a <= .01:
        return
    f = skia.Font(typeface(face), size)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    w = f.measureText(txt)
    m = f.getMetrics()
    yb = -(m.fAscent + m.fDescent) / 2
    xb = -w / 2 if align == 'center' else (0 if align == 'left' else -w)
    blob = skia.TextBlob.MakeFromString(txt, f)
    c = G.c
    c.save()
    c.translate(x, y)
    if rot:
        c.rotate(math.degrees(rot))
    if sc != 1:
        c.scale(sc, sc)
    if stroke:
        sp = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=strokeW or size * .14,
                        Color=skcol(stroke, a), StrokeJoin=skia.Paint.kRound_Join)
        if shadow:
            c.drawTextBlob(blob, xb + size * .05, yb + size * .07, sp)
        c.drawTextBlob(blob, xb, yb, sp)
    elif shadow:
        c.drawTextBlob(blob, xb + size * .045, yb + size * .055, skia.Paint(AntiAlias=True, Color=skcol(INK, a)))
    c.drawTextBlob(blob, xb, yb, skia.Paint(AntiAlias=True, Color=skcol(col, a)))
    c.restore()
    return w


# ---------------- paper and grain (precomputed at output resolution) ----------------
def _lowNoise(h, w, cell, rs):
    gh, gw = h // cell + 3, w // cell + 3
    g = rs.random((gh, gw))
    from PIL import Image
    im = Image.fromarray((g * 255).astype(np.uint8)).resize((w + 3 * cell, h + 3 * cell), Image.BICUBIC)
    return np.asarray(im, np.float32)[:h, :w] / 255.0


def makePaper():
    rs = np.random.default_rng(11)
    h, w = (OUT_H, OUT_W) if OUT_W <= 2560 else (1440, 2560)
    base = np.array(rgb(PAL['paper']), np.float32)
    n1 = _lowNoise(h, w, 220, rs)
    n2 = _lowNoise(h, w, 60, rs)
    shade = 1 - .05 * n1 - .025 * n2
    img = base[None, None, :] * shade[..., None]
    fib = rs.random((h, w)) < .004
    img[fib] *= .93
    arr = np.concatenate([np.clip(img, 0, 255).astype(np.uint8), np.full((h, w, 1), 255, np.uint8)], 2)
    return skia.Image.fromarray(_fit(arr), colorType=skia.kRGBA_8888_ColorType)


def _fit(arr):
    """textures are made at 2K at most; larger outputs get them resized so grain keeps its size on screen"""
    if arr.shape[1] == OUT_W and arr.shape[0] == OUT_H:
        return np.ascontiguousarray(arr)
    from PIL import Image
    return np.ascontiguousarray(np.asarray(Image.fromarray(arr).resize((OUT_W, OUT_H), Image.BICUBIC)))


def makeGrain():
    rs = np.random.default_rng(5)
    h, w = (OUT_H, OUT_W) if OUT_W <= 2560 else (1440, 2560)
    r = rs.random((h, w)).astype(np.float32)
    r2 = rs.random((h, w)).astype(np.float32)
    v = 255 - np.where(r < .55, r2 * rs.random((h, w)).astype(np.float32) * 22, 0)
    # watercolour blooms: soft low-frequency mottling so flat washes read as pigment on paper
    m = _lowNoise(h, w, 140, rs)
    v = v * (1 - .03 * m)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.hypot((xx - w / 2) / (w / 2), (yy - h / 2) / (h / 2)) / math.sqrt(2)
    vig = np.clip((d - .6) / .45, 0, 1) ** 1.6 * .16
    R = v * (1 - vig * (1 - 120 / 255))
    Gc = (v - 1) * (1 - vig * (1 - 95 / 255))
    B = (v - 3) * (1 - vig * (1 - 70 / 255))
    arr = np.stack([R, Gc, B, np.full_like(R, 255)], 2)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    return skia.Image.fromarray(_fit(arr), colorType=skia.kRGBA_8888_ColorType)


class Frame:
    """Owns the surface and the precomputed paper/grain images."""

    def __init__(self):
        self.surf = skia.Surface(OUT_W, OUT_H)
        self.paper = makePaper()
        self.grain = makeGrain()

    def begin(self, t):
        G.T = t
        G.BOILN = math.floor(t * BOIL + 1e-6)
        G.CLAWD_N = 0
        c = self.surf.getCanvas()
        G.c = c
        c.resetMatrix()
        c.clear(skia.ColorWHITE)
        c.drawImage(self.paper, 0, 0)
        c.scale(SC, SC)
        boilSeed('frame')
        return c

    def grainPass(self):
        c = G.c
        c.save()
        c.resetMatrix()
        pa = skia.Paint()
        pa.setBlendMode(skia.BlendMode.kMultiply)
        c.drawImage(self.grain, 0, 0, skia.SamplingOptions(), pa)
        c.restore()

    def end(self):
        img = self.surf.makeImageSnapshot()
        return img.toarray(colorType=skia.kBGRA_8888_ColorType)
