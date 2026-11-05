# cc.py: props, sets and screen overlays for 《匆匆那年》(王菲). Watercolour + boiling ink, logical canvas 1920x1080. No windows.
# The recurring object is the shared double desk with the 三八线 down the middle: her half (left) keeps his debts in pink gel
# pen, his half (right) keeps hers in navy ballpoint; in the present a yellowed white-out patch covers her half except one stroke.
import math
import numpy as np
from eng import *
import eng
from clawd import *
import clawd as _cl
import hb                      # registers whitehair / snow / beanie hats on clawd.hat
from hb import scarfDraw, chain, snowfall, dot
from hl import WENKAI, tint, desat, vignette
import hanzi
from props import puff
from bbset import wallClock2
from wo import writeTip

U = 28
FLOOR = 880
HER_PEN = '#D2557A'        # her pink gel pen: his debts, written on her half
HIS_PEN = '#2E3A66'        # his navy ballpoint: her debts, written on his half
LINE_PEN = '#3F5FAE'       # the line itself (blue ballpoint, retraced many times)
CHALK = '#F4F1E6'
CREAM = '#FFF7EA'


# ================================================================ costume (present: grey-blue knit beanie + her flower, snow on top)
_hat_prev = _cl.hat


def _hat(u, h, sw, o=None):
    if h == 'beanieL':
        hb._beanie(u, sw, '#8EA2C6')
    else:
        _hat_prev(u, h, sw, o)


_cl.hat = _hat


def herNow(x, y, u, o=None, snow=0.0):
    o = dict(o or {})
    v = o.get('view') or 'front'
    o['hat'] = ['beanieL', 'flower'] + (['snowhat'] if snow > .01 else [])
    o['snowK'] = snow
    her(x, y, u, o)          # no scarf: on a Clawd body it sits at belt height and reads as a belt


# ================================================================ pen strokes, tallies
def penStroke(p0, p1, w, col, a=1.0, seed=0.0, wob=.035):
    """one crisp ballpoint stroke with a slight static bow (pen marks don't boil)"""
    if a <= .01:
        return
    (x0, y0), (x1, y1) = p0, p1
    L = math.hypot(x1 - x0, y1 - y0) or 1
    nx, ny = -(y1 - y0) / L, (x1 - x0) / L
    o = (hash1(seed * 1.37 + 3.1) - .5) * 2 * wob * L
    p = skia.Path()
    p.moveTo(x0, y0)
    p.quadTo((x0 + x1) / 2 + nx * o, (y0 + y1) / 2 + ny * o, x1, y1)
    G.c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=w, StrokeCap=skia.Paint.kRound_Cap,
                               Color=skcol(col, a)))


_ZH = [((.12, .12), (.88, .12)), ((.5, .12), (.5, .9)), ((.5, .5), (.82, .5)), ((.22, .44), (.22, .9)), ((.05, .9), (.95, .9))]


def tally(x, y, s, n, col, seed=0, a=1.0, w=3.4, rot=0.0):
    """the first n strokes (<= 5) of a 正 tally, box top-left (x, y), size s"""
    if a <= .01 or n <= 0:
        return
    push()
    translate(x, y)
    rotate(rot)
    for i in range(min(5, n)):
        (ax, ay), (bx, by) = _ZH[i]
        j = lambda k: (hash1(seed * 7.1 + i * 3.3 + k) - .5) * .08
        penStroke((ax * s + j(1) * s, ay * s + j(2) * s), (bx * s + j(3) * s, by * s + j(4) * s), w, col, a, seed * 5 + i)
    pop()


def tallyGrid(x0, y0, n, col, per=8, s=50, dx=66, dy=76, seed=0, rot=-.03, reveal=None):
    """n strokes as rows of 正; returns [(x, y, strokes)] per group. reveal(x, y) -> alpha per group"""
    out = []
    g = 0
    while n > 0:
        k = min(5, n)
        gx = x0 + (g % per) * dx + (hash1(seed + g * 1.9) - .5) * 6
        gy = y0 + (g // per) * dy + (hash1(seed + g * 2.7) - .5) * 6
        a = 1.0 if reveal is None else reveal(gx + s / 2, gy + s / 2)
        tally(gx, gy, s, k, col, seed + g, a, rot=rot + (hash1(seed + g) - .5) * .06)
        out.append((gx, gy, k))
        n -= k
        g += 1
    return out


# ================================================================ chalk
_CHK = {}


def chalkShader(seed=7, holes=.42, sc=1.6):
    key = (seed, holes, sc)
    if key not in _CHK:
        rs = np.random.RandomState(seed)
        n = rs.rand(192, 192)
        streak = np.repeat(rs.rand(192, 1), 192, axis=1) * .25        # faint horizontal drag of the chalk
        a = (np.clip((n * .85 + streak - (1 - holes)) / .14, 0, 1) * 255).astype(np.uint8)
        arr = np.zeros((192, 192, 4), np.uint8)
        arr[..., 3] = a
        img = skia.Image.fromarray(arr, colorType=skia.kRGBA_8888_ColorType, alphaType=skia.kPremul_AlphaType)
        _CHK[key] = img.makeShader(skia.TileMode.kRepeat, skia.TileMode.kRepeat, skia.SamplingOptions(), skia.Matrix.Scale(sc, sc))
    return _CHK[key]


def _grainOut(l, t_, r, b, k=.9, seed=7, holes=.42):
    p = skia.Paint(Shader=chalkShader(seed, holes))
    p.setBlendMode(skia.BlendMode.kDstOut)
    p.setAlphaf(clamp(k))
    G.c.drawRect(skia.Rect.MakeLTRB(l, t_, r, b), p)


def chalkWrite(txt, x0, y0, size, prog, col=CHALK, a=.94, gap=.08):
    """write txt in chalk in real stroke order up to prog (0..1, shared across chars by stroke length); top-left x0, y0"""
    chars = list(txt)
    lens = [hanzi.char_len(ch) if ch != ' ' else 0 for ch in chars]
    tot = sum(lens) or 1
    done = clamp(prog) * tot
    c = G.c
    c.saveLayer(None, None)
    pa = skia.Paint(AntiAlias=True, Color=skcol(col, a))
    pb = skia.Paint(AntiAlias=True, Color=skcol(col, .16 * a))
    pb.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, size * .03))
    x = x0
    for ch, Ln in zip(chars, lens):
        if ch == ' ':
            x += size * .45
            continue
        p = clamp(done / Ln) if Ln else 0
        done -= Ln
        if p > 0:
            hanzi.write_char(c, ch, x + size * .01, y0 + size * .012, size, p, [pb], mode='brush')
            hanzi.write_char(c, ch, x, y0, size, p, [pa], mode='brush')
        x += size * (1 + gap)
    _grainOut(x0 - 30, y0 - 30, x + 30, y0 + size + 30, .8)
    c.restore()


def chalkStick(x, y, s=1.0, ang=-.95, col=CHALK):
    """a stick of chalk whose tip touches (x, y); no hand — it writes by itself"""
    push()
    translate(x, y)
    rotate(ang)
    L, w = 74 * s, 16 * s
    G.c.drawRoundRect(skia.Rect.MakeXYWH(8, -w / 2 + 12, L, w), w * .4, w * .4, skia.Paint(AntiAlias=True, Color=skcol('#000000', .28)))
    boilSeed('chalkstick')
    paint(rrPts(0, -w / 2, L, w, w * .38), wash=col, fill='#D8D2C2', fillOp=70, ink=INK, sw=.5, lite=True)
    G.c.drawCircle(1, 0, w * .32, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .9)))
    pop()


def chalkText(txt, x, y, size, a=.85, col=CHALK, align='center', rot=0.0, seed=3):
    if a <= .01:
        return
    w = textW(txt, size, WENKAI)
    G.c.saveLayer(None, None)
    text(txt, x, y, size, col, face=WENKAI, align=align, shadow=False, a=a, rot=rot)
    x0 = x - w / 2 if align == 'center' else (x if align == 'left' else x - w)
    _grainOut(x0 - 12, y - size, x0 + w + 12, y + size, .75, seed)
    G.c.restore()


# ================================================================ screen overlays: narration, corner tag, name card
def narration(t, items, y=92, size=50):
    """first-person narration, one short line at a time, top centre (lyrics stay at the bottom)"""
    for it in items:
        a, b, s = it[0], it[1], it[2]
        who = it[3] if len(it) > 3 else 'her'
        if a <= t <= b:
            k = ease(seg(t, a, a + .45)) * (1 - ease(seg(t, b - .45, b)))
            if k <= .01:
                continue
            dy = (1 - ease(seg(t, a, a + .7))) * 10
            w = textW(s, size, WENKAI)
            softBand(W / 2, y + dy, w + 170, size * 1.5, .34 * k)
            text(s, W / 2, y + dy, size, CREAM, face=WENKAI, stroke=INK, strokeW=size * .15, shadow=True, a=k)
            mx = W / 2 - w / 2 - 34
            if who == 'him':
                G.c.drawRoundRect(skia.Rect.MakeXYWH(mx - 11, y + dy - 11, 22, 22), 4, 4, skia.Paint(AntiAlias=True, Color=skcol('#D97757', k)))
            else:
                G.c.drawCircle(mx, y + dy, 11, skia.Paint(AntiAlias=True, Color=skcol('#EE9AAE', k)))
            G.c.drawCircle(mx, y + dy, 13, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skcol(INK, k)))


def softBand(cx, cy, w, h, a, col='#0B1022'):
    if a <= .01:
        return
    pa = skia.Paint(AntiAlias=True, Color=skcol(col, a))
    pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, h * .35))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), h / 2, h / 2, pa)


def cornerTag(t, items, x=70, y=66, size=36):
    for (a, b, s) in items:
        if a <= t <= b:
            k = ease(seg(t, a, a + .5)) * (1 - ease(seg(t, b - .5, b)))
            if k > .01:
                softBand(x + textW(s, size, WENKAI) / 2, y + 4, textW(s, size, WENKAI) + 90, size * 1.6, .30 * k)
                w = text(s, x, y, size, CREAM, face=WENKAI, align='left', stroke=INK, strokeW=6.5, shadow=False, a=k)
                G.c.drawLine(x + 2, y + size * .72, x + (w or 120) * ease(seg(t, a + .2, a + .9)), y + size * .74,
                             skia.Paint(AntiAlias=True, Color=skcol(CREAM, .8 * k), StrokeWidth=2.4, StrokeCap=skia.Paint.kRound_Cap))


def nameCard(x, y, name, sub, k, rot=-.035, key='nc'):
    """a small pinned paper tag: name · age, and one line of situation"""
    if k <= .01:
        return
    push()
    translate(x, y + (1 - ease(k)) * 14)
    rotate(rot)
    w = max(textW(name, 46, WENKAI), textW(sub, 28, WENKAI)) + 76
    h = 124
    G.c.saveLayerAlpha(None, int(255 * clamp(k)))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + 8, -h / 2 + 10, w, h), 10, 10, skia.Paint(AntiAlias=True, Color=skcol('#000000', .25)))
    boilSeed(key)
    paint(rrPts(-w / 2, -h / 2, w, h, 10), wash='#FBF5E6', fill='#EADFC6', fillOp=50, ink=INK, sw=.8, lite=True)
    paint(ellPts(0, -h / 2 + 12, 10, 10, 12), wash=HER_PEN, ink=INK, sw=.5)
    text(name, 0, -12, 46, INK, face=WENKAI, shadow=False)
    text(sub, 0, 34, 28, '#5E5668', face=WENKAI, shadow=False)
    G.c.restore()
    pop()


def presentGrade(k=1.0, vig=.42):
    """after camEnd(): the present — cold winter daylight, a little drained"""
    if k <= .01:
        return
    tint('#A9BCDD', .30 * k, skia.BlendMode.kMultiply)
    desat(.20 * k)
    tint('#DCE6FA', .06 * k, skia.BlendMode.kScreen)
    vignette(vig * k, '#10142A')


def dustMotes(t, n=36, a=.35, seed=11):
    """screen space: slow floating dust in the cold light"""
    for i in range(n):
        h = hash1(seed + i * 1.71)
        x = (h * W + t * (6 + 10 * hash1(i * 3.3)) + 40 * math.sin(t * .4 + i)) % (W + 40) - 20
        y = (hash1(seed + i * 2.9) * H - t * (4 + 8 * hash1(i * 1.1)) + 30 * math.sin(t * .3 + i * 2)) % (H + 40) - 20
        r = 1.6 + 2.4 * hash1(i * 5.7)
        tw = .55 + .45 * math.sin(t * (1 + hash1(i)) + i)
        G.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=skcol('#F4F7FF', a * tw)))


# ================================================================ the desk, seen from above (present)
DESK = (160, 150, 1760, 950)      # x0, y0, x1, y1; the seat edge is the bottom
LINE_X = 960
NOTE_XY = (960, 878)
HIS_N, HER_N = 99, 95              # his half keeps her debts (never erased); her half keeps his (white-out, one stroke left)
HIS_GRID = (1046, 540)
HER_GRID = (348, 540)
LONE = (348 + 3 * 66 + 26, 540 + 2 * 76 + 7)    # the 96th stroke (top bar of the next 正), just past the patch


def _terrazzo(x0, y0, x1, y1, base='#8E8F8C', seed=5):
    flatRect(x0, y0, x1 - x0, y1 - y0, base)
    for i in range(520):
        x = x0 + hash1(seed + i * 1.13) * (x1 - x0)
        y = y0 + hash1(seed + i * 2.31) * (y1 - y0)
        r = 1.5 + 4 * hash1(i * 3.7)
        col = ('#B9BAB6', '#6F706D', '#A6A08F', '#C9C6BC')[i % 4]
        G.c.drawCircle(x, y, r, skia.Paint(AntiAlias=True, Color=skcol(col, .7)))
    for gx in range(int(x0 // 320) * 320, int(x1), 320):
        G.c.drawLine(gx, y0, gx, y1, skia.Paint(AntiAlias=True, Color=skcol('#5E5F5C', .35), StrokeWidth=2))
    for gy in range(int(y0 // 320) * 320, int(y1), 320):
        G.c.drawLine(x0, gy, x1, gy, skia.Paint(AntiAlias=True, Color=skcol('#5E5F5C', .35), StrokeWidth=2))


def whiteOut(rows, k=1.0, old=1.0, seed=3):
    """correction-pen patch over tally rows: rows = [(x0, x1, y)] (y = top of a tally row); two fat strokes per row,
    yellowed with a raised edge and hairline cracks"""
    if k <= .01:
        return
    col = mixCol('#F6F2E4', '#E6D9B4', old)
    sts = []
    for r, (x0, x1, y) in enumerate(rows):
        for j, dy in enumerate((14, 40)):
            xa = x0 + (hash1(seed + r * 3 + j) - .5) * 24
            xb = x1 + (hash1(seed + r * 5 + j * 2.2) - .5) * 30
            sts.append(((xa, y + dy + (hash1(r + j) - .5) * 6), (xb, y + dy + 3 + (hash1(r * 2 + j) - .5) * 6), seed + r * 2 + j))
    G.c.saveLayerAlpha(None, int(255 * clamp(k)))
    for p0, p1, sd in sts:                                       # raised edge / shadow
        penStroke((p0[0] + 2, p0[1] + 3), (p1[0] + 2, p1[1] + 3), 36, mixCol(col, '#6E5A3A', .45), .55, sd, .015)
    for p0, p1, sd in sts:
        penStroke(p0, p1, 33, col, 1.0, sd, .015)
    for p0, p1, sd in sts:                                       # the nib's drag marks
        penStroke((p0[0] + 10, p0[1] - 6), (p1[0] - 10, p1[1] - 6), 2.2, '#FFFFFF', .45, sd + 9, .015)
    for i in range(10):                                          # hairline cracks
        x0, x1, y = rows[i % len(rows)]
        x = lerp(x0, x1, hash1(seed * 3 + i))
        yy = y + 10 + 36 * hash1(seed * 5 + i)
        ang = hash1(seed + i * 9) * TAU
        L = 10 + 16 * hash1(i * 7.3)
        penStroke((x, yy), (x + math.cos(ang) * L, yy + math.sin(ang) * L), 1.3, '#9C8C66', .6, i, .2)
    G.c.restore()


def carving(cx, cy, old=1.0, k=1.0, size=54):
    """「永远一起」 scratched into the laminate with a compass point, straddling the line (incised: dark lip + pale groove)"""
    if k <= .01:
        return
    push()
    translate(cx, cy)
    rotate(-.04)
    off = size * .55          # the line runs between 远 and 一
    text('永远一起', off * 0 + 2.5, 3, size, '#5E4428', face=WENKAI, shadow=False, a=.55 * k)
    text('永远一起', 0, 0, size, mixCol('#F7EBD0', '#E8D7B4', old), face=WENKAI, shadow=False, a=.85 * k)
    pop()


def deskTop(t, reveal=None, old=1.0, loneGlow=0.0):
    """the shared double desk from above. reveal(x, y) -> 0..1 alpha for the tally groups / patch (None = all shown)"""
    x0, y0, x1, y1 = DESK
    _terrazzo(-1400, -1200, W + 1400, H + 1300)
    # two chair backrests just below the seat edge (pushed in)
    for cx in (520, 1400):
        boilSeed('chairtop%d' % cx)
        paint(rrPts(cx - 130, y1 + 26, 260, 34, 12), wash='#A9784C', fill='#7E5636', fillOp=60, ink=INK, sw=.8)
    G.c.drawRect(skia.Rect.MakeXYWH(x0 + 26, y0 + 36, x1 - x0, y1 - y0), skia.Paint(AntiAlias=True, Color=skcol('#000000', .28)))
    boilSeed('deskedge')
    paint(rrPts(x0 - 16, y0 - 16, x1 - x0 + 32, y1 - y0 + 32, 16), wash='#8C6A48', fill='#6E5034', fillOp=60, ink=INK, sw=1.0)
    boilSeed('desktop')
    paint(rectPts(x0, y0, x1 - x0, y1 - y0), wash=mixCol('#E2C69A', '#D2B98F', old), fill='#C49C6C', fillOp=60, bleed=.04, tex=.6,
          border=.5, ink=INK, sw=.9)
    for i in range(24):                                          # laminate grain
        y = y0 + 18 + i * (y1 - y0 - 30) / 23 + 6 * math.sin(i * 1.9)
        p = skia.Path()
        p.moveTo(x0 + 6, y)
        p.cubicTo(x0 + 500, y + 10 * math.sin(i), x0 + 1100, y - 9 * math.cos(i * 1.3), x1 - 6, y + 4)
        G.c.drawPath(p, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.6, Color=skcol('#A9814F', .28)))
    # wear where forearms rest + the far pencil groove
    paint(rrPts(x0 + 120, y0 + 26, x1 - x0 - 240, 22, 10), wash='#B08860', fill='#8A6440', fillOp=50, ink=INK, sw=.5)
    # scratches, compass marks, ink blots, a faded star sticker
    for i in range(18):
        x = x0 + 80 + hash1(i * 4.1) * (x1 - x0 - 160)
        y = y0 + 80 + hash1(i * 6.7) * (y1 - y0 - 160)
        a_ = hash1(i * 2.3) * TAU
        L = 20 + 40 * hash1(i * 8.1)
        penStroke((x, y), (x + math.cos(a_) * L, y + math.sin(a_) * L), 1.5, '#8E6A44', .35, i, .1)
    for (cx, cy, r) in ((1500, 740, 34), (1540, 770, 18), (1470, 790, 52)):
        G.c.drawCircle(cx, cy, r, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=1.4, Color=skcol('#8E6A44', .45)))
        G.c.drawCircle(cx, cy, 2.5, skia.Paint(AntiAlias=True, Color=skcol('#5E4428', .6)))
    for (bx, by, r) in ((1196, 690, 7), (1214, 702, 4), (402, 640, 5)):
        G.c.drawCircle(bx, by, r, skia.Paint(AntiAlias=True, Color=skcol(HIS_PEN if bx > 900 else HER_PEN, .5)))
    boilSeed('sticker')
    paint(starPts(300, 800, 38, .45, 5, -.3), wash=mixCol('#F7D36E', '#E8DCC0', .5 * old), ink=INK, sw=.5, lite=True)
    carving(LINE_X, 336, old)
    # the line: blue ballpoint retraced many times
    for j, off in enumerate((-1.6, 0.0, 1.8)):
        penStroke((LINE_X + off, y0 + 14), (LINE_X + off * .6, y1 - 14), 4.2 - j * .6, LINE_PEN, (.78 - .12 * j) * (1 - .25 * old), 40 + j, .004)
    # tallies: his half (her debts, navy) — never erased
    tallyGrid(HIS_GRID[0], HIS_GRID[1], HIS_N, HIS_PEN, seed=100, rot=-.03, reveal=reveal)
    # her half (his debts, pink) — covered by the patch except the last stroke
    groups = tallyGrid(HER_GRID[0], HER_GRID[1], HER_N, HER_PEN, seed=300, rot=.02, reveal=reveal)
    gx, gy = HER_GRID
    pk = 1.0 if reveal is None else reveal(600, gy + 80)
    whiteOut([(gx - 14, gx + 7 * 66 + 64, gy), (gx - 14, gx + 7 * 66 + 64, gy + 76), (gx - 14, gx + 2 * 66 + 62, gy + 152)], pk, old, seed=8)
    G.c.saveLayerAlpha(None, 30)                                 # the pink shows faintly through the old patch
    tallyGrid(HER_GRID[0], HER_GRID[1], HER_N, HER_PEN, seed=300, rot=.02, reveal=reveal)
    G.c.restore()
    lx, ly = LONE
    la = 1.0 if reveal is None else reveal(lx, ly)
    penStroke((lx - 22, ly), (lx + 22, ly + 1), 3.6, HER_PEN, .95 * la, 77, .04)
    if loneGlow > .01:
        glow(lx, ly, 60, '#FFD6E2', .45 * loneGlow)
    # the rule note taped across the line at the seat end
    nx, ny = NOTE_XY
    push()
    translate(nx, ny)
    rotate(-.035)
    G.c.drawRect(skia.Rect.MakeXYWH(-196, -44, 400, 100), skia.Paint(AntiAlias=True, Color=skcol('#000000', .18)))
    boilSeed('rulenote')
    paint(rectPts(-200, -50, 400, 100, 1), wash=mixCol('#FBF3D6', '#EBDDB2', old), fill='#E2D2A4', fillOp=50, ink=INK, sw=.7, lite=True)
    for tx in (-200, 200):
        G.c.save()
        G.c.translate(tx, -40)
        G.c.rotate(-20 if tx < 0 else 18)
        G.c.drawRect(skia.Rect.MakeXYWH(-34, -13, 68, 26), skia.Paint(AntiAlias=True, Color=skcol('#F1EEE4', .55)))
        G.c.restore()
    text('过线一次 欠一次！', 0, 2, 38, mixCol(HER_PEN, '#9A6E7C', .35 * old), face=WENKAI, shadow=False, a=.92)
    pop()


# ================================================================ the classroom, front wall (present)
BOARD = (560, -160, 1560, 330)
TITLE_SIZE = 150
TITLE_X0, TITLE_Y0 = 746, -47
DOOR = (120, 330, 440, 872)
DESK_F = (1160, 1800)             # her front-row double desk (front elevation)
DESK_TOP_Y = 720
DOOR_X = 310                      # where someone stands in the doorway


def doorWay(t, opn, snowK=1.0, inDoor=None):
    x0, y0, x1, y1 = DOOR
    w, h = x1 - x0, y1 - y0
    # opening: the corridor, and the snowy yard beyond it
    G.c.save()
    G.c.clipRect(skia.Rect.MakeLTRB(x0, y0, x1, y1))
    gradRect(x0, y0, w, h, ['#4F6283', '#8FA2C2'])
    flatRect(x0, y0 + h * .62, w, h * .38, '#D8E2F0')
    G.c.drawRect(skia.Rect.MakeXYWH(x0, y0 + h * .55, w, 16), skia.Paint(Color=skcol('#3E4C66', .9)))     # corridor railing
    for i in range(5):
        G.c.drawRect(skia.Rect.MakeXYWH(x0 + 20 + i * 56, y0 + h * .55, 6, h * .1), skia.Paint(Color=skcol('#3E4C66', .9)))
    if snowK > .01:
        snowfall(t, 3, 40, x0, y0, x1, y1, a=.85 * snowK, r=5)
    G.c.restore()
    if inDoor:
        inDoor()                       # someone standing in the doorway: behind the leaf and the frame
    # leaf: hinged on the left, swings toward us (drawn narrowing)
    lw = w * (1 - .88 * opn)
    sk = 26 * opn
    boilSeed('doorleaf')
    paint([[x0, y0], [x0 + lw, y0 - sk], [x0 + lw, y1 + sk * .4], [x0, y1]], wash='#B57F51', fill='#8C5F3A', fillOp=60, ink=INK, sw=.9)
    if lw > 60:
        paint(rectPts(x0 + lw * .18, y0 + 60 - sk * .6, lw * .64, 170), wash='#A06E45', ink=INK, sw=.5, lite=True)
        G.c.drawCircle(x0 + lw * .86, y0 + h * .52, 9, skia.Paint(AntiAlias=True, Color=skcol('#D8C9A0')))
    # frame
    boilSeed('doorframe')
    for pts in ([[x0 - 18, y0 - 18], [x1 + 18, y0 - 18], [x1 + 18, y0], [x0 - 18, y0]],
                [[x0 - 18, y0], [x0, y0], [x0, y1], [x0 - 18, y1]], [[x1, y0], [x1 + 18, y0], [x1 + 18, y1], [x1, y1]]):
        paint(pts, wash='#7A5638', ink=INK, sw=.7)
    # class plate above the door
    boilSeed('plate')
    paint(rrPts(200, 246, 160, 52, 6), wash='#FBFAF6', ink=INK, sw=.8)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(206, 252, 148, 40), 4, 4, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style,
                                                                              StrokeWidth=2.5, Color=skcol('#3A5FA8')))
    text('高三(2)班', 280, 272, 28, '#2E4C8E', face=WENKAI, shadow=False)


def blackboard(t, titleProg=1.0, chalkOn=False, mode='reunion', num=200, endProg=0.0):
    x0, y0, x1, y1 = BOARD
    boilSeed('bbframe')
    paint(rrPts(x0 - 26, y0 - 26, x1 - x0 + 52, y1 - y0 + 52, 8), wash='#6E5038', fill='#563C28', fillOp=60, ink=INK, sw=1.0)
    boilSeed('board')
    paint(rectPts(x0, y0, x1 - x0, y1 - y0), wash='#2E4A3E', fill='#25402F', fillOp=80, bleed=.03, tex=.7, border=.3, ink=INK, sw=.8)
    # old erasing smears
    for i in range(7):
        sx = x0 + 60 + hash1(i * 3.3) * (x1 - x0 - 300)
        sy = y0 + 40 + hash1(i * 5.1) * (y1 - y0 - 80)
        G.c.drawOval(skia.Rect.MakeXYWH(sx, sy, 220 + 200 * hash1(i), 46), skia.Paint(AntiAlias=True, Color=skcol('#E8EDE6', .07)))
    Y, P, Bl = '#F7D36E', '#F2A9BC', '#9FD3E8'
    for i, ch in enumerate('天道酬勤'):                         # left margin, top to bottom, yellow chalk
        chalkText(ch, 612, -62 + i * 42, 36, .75, col=Y, seed=20 + i)
    if mode == 'countdown':
        chalkText('12月18日 星期五', x0 + 34, y0 + 42, 34, .8, align='left', seed=4)
        chalkText('值日：李静 刘洋', x1 - 300, y0 + 42, 30, .75, align='left', seed=6)
        chalkText('不苦不累 高三无味', 1060, y0 + 42, 28, .7, col=P, seed=31)
        chalkText('距高考', 820, 40, 70, .9, seed=13)
        chalkText(str(num), 1110, 30, 190, .95, col='#F7D9A0', seed=14)
        chalkText('天', 1330, 60, 70, .9, seed=15)
        chalkText('高三(2)班 加油！', 1064, 210, 44, .8, col=P, seed=16)
        chalkText('提高一分', 1478, -40, 30, .72, col=Bl, seed=32)
        chalkText('干掉千人', 1478, -2, 30, .72, col=Bl, seed=33)
        chalkText('今日作业：数学卷P23 英语听力', x0 + 30, 290, 26, .6, align='left', seed=34)
        chalkText('乾坤未定 你我皆是黑马', x1 - 30, 290, 28, .7, col=Y, align='right', seed=35)
    else:
        chalkText('12月20日 星期日', x0 + 34, y0 + 42, 34, .8, align='left', seed=4)
        duty = '值日：方茴 陈寻' if mode == 'final' else '值日：张伟 王小胖'
        chalkText(duty, x1 - 300, y0 + 42, 30, .75, align='left', seed=6)
        chalkText('乾坤未定 你我皆是黑马', 1060, y0 + 42, 28, .7, col=Y, seed=31)
        chalkText('提高一分', 1478, -40, 30, .72, col=Bl, seed=32)
        chalkText('干掉千人', 1478, -2, 30, .72, col=Bl, seed=33)
        chalkText('高三(2)班 · 毕业十年', 1064, 152, 38, .82, seed=5)
        chalkText('同学们好', 600, 286, 28, .7, col=P, align='left', seed=36)
        chalkText('欢迎回家', x1 - 30, 286, 30, .75, col=Y, align='right', seed=37)
    if mode == 'final':
        for i in range(4):                                     # the title, wiped off with the eraser
            G.c.drawOval(skia.Rect.MakeXYWH(720 + i * 40, -60 + i * 34, 700, 70), skia.Paint(AntiAlias=True, Color=skcol('#E8EDE6', .09)))
        if endProg > 0:
            chalkWrite('下次再算', TITLE_X0 + 20, TITLE_Y0, TITLE_SIZE * .9, endProg)
            if endProg < 1:
                px, py = writeTip('下次再算', TITLE_X0 + 20, TITLE_Y0, TITLE_SIZE * .9, endProg)
                chalkStick(px, py, 1.1)
    elif mode == 'countdown':
        pass
    elif titleProg > 0:
        chalkWrite('匆匆那年', TITLE_X0, TITLE_Y0, TITLE_SIZE, titleProg)
        if chalkOn and titleProg < 1:
            px, py = writeTip('匆匆那年', TITLE_X0, TITLE_Y0, TITLE_SIZE, titleProg)
            chalkStick(px, py, 1.15)
    # tray: chalk pieces and the eraser
    boilSeed('tray')
    paint(rectPts(x0 - 20, y1 + 26, x1 - x0 + 40, 18), wash='#7A5A40', ink=INK, sw=.7)
    for i, (cx, col) in enumerate(((640, '#F4F1E6'), (690, '#F2A9BC'), (726, '#F4E08A'), (1180, '#F4F1E6'))):
        paint(rrPts(cx, y1 + 14, 34, 12, 5), wash=col, ink=INK, sw=.4, lite=True)
    if not chalkOn and titleProg >= 1 and mode == 'reunion':
        paint(rrPts(1110, y1 + 14, 40, 12, 5), wash=CHALK, ink=INK, sw=.4, lite=True)      # the stick that wrote the title, put back
    paint(rrPts(1400, y1 - 4, 120, 32, 6), wash='#8A6A4C', ink=INK, sw=.6)
    paint(rectPts(1404, y1 + 20, 112, 10), wash='#9A9A98', ink=None)


def classroomFront(t, titleProg=1.0, chalkOn=False, doorOpn=0.0, inDoor=None, board='reunion', num=200, endProg=0.0):
    # wall, dado, floor
    flatRect(-900, -1100, W + 1800, 1620, '#E7E3D7')
    boilSeed('wallwash')
    paint(rectPts(-900, -1100, W + 1800, 1620), fill='#D9D3C2', fillOp=40, bleed=.02, tex=.8, border=.2, ink=None)
    flatRect(-900, 520, W + 1800, 352, '#8BB09F')
    boilSeed('dado')
    paint(rectPts(-900, 520, W + 1800, 352), fill='#6F9786', fillOp=50, bleed=.02, tex=.8, border=.2, ink=None)
    flatRect(-900, 514, W + 1800, 10, '#6D8E7E')
    _terrazzo(-900, 872, W + 900, 1700, '#A7A59E', seed=9)
    flatRect(-900, 860, W + 1800, 14, '#5F5A52')
    # clock, board, notice board
    wallClock2(1060, -330, 54, 4, 20, key='clock')
    boilSeed('speaker')
    paint(rrPts(380, -330, 120, 90, 8), wash='#E8E1D2', ink=INK, sw=.8)
    for j in range(5):
        G.c.drawLine(398, -310 + j * 14, 482, -310 + j * 14, skia.Paint(AntiAlias=True, Color=skcol('#6E6878', .6), StrokeWidth=3))
    boilSeed('radiator')
    paint(rectPts(1826, 600, 230, 180), wash='#E7E4DC', fill='#C9C4B8', fillOp=50, ink=INK, sw=.8)
    for j in range(9):
        G.c.drawLine(1846 + j * 24, 612, 1846 + j * 24, 768, skia.Paint(AntiAlias=True, Color=skcol('#9A958A', .7), StrokeWidth=4))
    inkLine([[1826, 790], [1800, 790], [1800, 872]], 1.0, '#9A958A', 'ink', 0)
    blackboard(t, titleProg, chalkOn, board, num, endProg)
    boilSeed('notice')
    paint(rectPts(1650, 40, 230, 300), wash='#C9A479', fill='#A9825A', fillOp=60, ink=INK, sw=.8)
    for i, (px, py, pw, ph, rot) in enumerate(((1672, 64, 92, 120, -.04), (1774, 70, 86, 110, .05), (1690, 200, 160, 116, .02))):
        push()
        translate(px + pw / 2, py + ph / 2)
        rotate(rot)
        paint(rectPts(-pw / 2, -ph / 2, pw, ph), wash='#FBF8F0', ink=INK, sw=.5, lite=True)
        for j in range(4):
            G.c.drawLine(-pw / 2 + 12, -ph / 2 + 22 + j * 22, pw / 2 - 12 - (j == 3) * 30, -ph / 2 + 22 + j * 22,
                         skia.Paint(AntiAlias=True, Color=skcol('#8A8494', .6), StrokeWidth=2))
        G.c.drawCircle(0, -ph / 2 + 6, 5, skia.Paint(AntiAlias=True, Color=skcol(('#D2557A', '#3F5FAE', '#E0A030')[i])))
        pop()
    text('班级公告', 1765, 26, 26, '#4A4152', face=WENKAI, shadow=False)
    # the door
    doorWay(t, doorOpn, inDoor=inDoor)
    # broom and dustpan by the door
    boilSeed('broom')
    inkLine([[498, 872], [530, 560]], 1.6, '#9A7650', 'ink', 0)
    paint([[470, 872], [530, 872], [524, 800], [482, 800]], wash='#D8B46A', fill='#B8924A', fillOp=60, ink=INK, sw=.6)
    paint([[548, 872], [612, 872], [618, 830], [552, 836]], wash='#5E8FC4', ink=INK, sw=.6)
    # the platform in front of the board and the teacher's desk
    boilSeed('platform')
    paint(rectPts(520, 846, 1100, 26), wash='#A47C56', fill='#7E5A3C', fillOp=50, ink=INK, sw=.7)
    boilSeed('lectern')
    paint(rectPts(650, 690, 260, 156), wash='#B48A60', fill='#8E6640', fillOp=60, ink=INK, sw=.9)
    paint(rectPts(636, 676, 288, 18), wash='#C79C70', ink=INK, sw=.8)
    paint(rectPts(680, 720, 200, 96), wash='#A57B52', ink=INK, sw=.5, lite=True)
    push()
    translate(720, 668)
    rotate(-.05)
    paint(rectPts(-46, -12, 92, 16), wash='#FBF8F0', ink=INK, sw=.5, lite=True)       # reunion sign-in sheet
    pop()
    paint(rectPts(820, 652, 52, 26), wash='#F2EFE6', ink=INK, sw=.5)                   # chalk box
    text('签到', 720, 640, 22, '#4A4152', face=WENKAI, shadow=False, rot=-.05)


def deskFront(t, seatsTaken=(), key='dkf'):
    """her front-row double desk (front elevation) with the two chairs pushed in toward us"""
    x0, x1 = DESK_F
    ty = DESK_TOP_Y
    boilSeed(key + 'legs')
    for lx in (x0 + 26, x1 - 26):
        inkLine([[lx, ty + 60], [lx, FLOOR]], 1.5, '#6E737C', 'ink', 0)
    inkLine([[x0 + 26, 836], [x1 - 26, 836]], 1.0, '#6E737C', 'ink', 0)
    boilSeed(key + 'box')
    paint(rectPts(x0 + 14, ty + 20, x1 - x0 - 28, 54), wash='#3B3036', fill='#2A2228', fillOp=60, ink=INK, sw=.8)      # the 桌肚
    for i, (bx, bw, col) in enumerate(((x0 + 70, 22, '#5E8FC4'), (x0 + 96, 18, '#E7C46A'), (x1 - 150, 24, '#C9727F'))):
        paint(rectPts(bx, ty + 32, bw, 40), wash=col, ink=INK, sw=.4, lite=True)
    boilSeed(key + 'top')
    paint(rectPts(x0 - 10, ty - 10, x1 - x0 + 20, 12), wash='#E2C69A', ink=INK, sw=.7)
    paint(rectPts(x0 - 10, ty + 2, x1 - x0 + 20, 20), wash='#9C7652', fill='#7A5A3C', fillOp=60, ink=INK, sw=.8)
    for i, cx in enumerate((x0 + 170, x1 - 170)):
        boilSeed(key + 'chair%d' % i)
        paint(rrPts(cx - 78, 676, 156, 52, 8), wash='#B07D50', fill='#8A5E38', fillOp=60, ink=INK, sw=.8)
        for px in (cx - 62, cx + 62):
            inkLine([[px, 728], [px, 800]], 1.3, '#6E737C', 'ink', 0)
        paint(rectPts(cx - 84, 792, 168, 14), wash='#A9784C', ink=INK, sw=.7)
        for px in (cx - 70, cx + 70):
            inkLine([[px, 806], [px, FLOOR + 4]], 1.3, '#6E737C', 'ink', 0)
