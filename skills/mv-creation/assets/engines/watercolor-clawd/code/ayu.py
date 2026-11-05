# ayu.py: 阿屿 —《新地球》MV 的新主角（水彩手绘 · 约 2.3 头身，比例取自《小酒窝》小人）
# (x, y) = 两脚之间的地面点；u = 单位（全身约 20u 高，头高约 8.6u）。
# 识别特征：海蓝渔夫帽（在新地球褪色起毛）、珊瑚红防风夹克（帽兜在背后）、米白围脖（可拉起当口罩）、
#          胸前挂一只小漂流瓶（里面卷着小岛的旧照片和一枚粉贝壳）、藏蓝短裤、沙黄雨靴；
#          笑起来两颊有小酒窝——在示例歌词不笑，酒窝只在回忆和片尾出现。
import math
import skia
from eng import *

AYU = dict(
    skin='#F4CFB2', skinDk='#DDA587', skinLt='#FBE6D6', blush='#EE8F8A',
    hair='#2F2B38', hairLt='#4E4860',
    hat='#3E7FAE', hatDk='#2B5D86', hatLt='#8DBFE0',
    hatOld='#7FA6BE', hatOldDk='#5C8199', hatOldLt='#B8D2E2',
    coat='#E06A4E', coatDk='#B04A36', coatLt='#F4A184', patch='#E3B456',
    gaiter='#EFE3C8', gaiterDk='#C9B48E',
    shorts='#3F4A66', shortsDk='#2B3349',
    boot='#E9B949', bootDk='#BF8A2B', bootLt='#F7DB8E',
    glass='#BFE6E2', cork='#9A6B45', paperC='#FBF3DE', shell='#F2A7B5',
    tee='#FFFDF6', teeDk='#D9D2C2', swim='#5BB3A9', swimDk='#3E8A80',
)


def _P(pts, u):
    return [[a * u, b * u] for a, b in pts]


LITE = [False]


def part(P, col, dk=None, lt=None, sd=(1, .3), ink=True, sw=1.0, curv=True, opD=120, opL=130, br='ink', inkCol=None):
    """watercolour part: flat wash + clipped shadow/light blooms + boiling ink outline (P in canvas units)."""
    Q = throughClosed(P, 4) if curv else P
    if LITE[0]:
        # small on screen: flat wash + one soft shadow, no blurred bleed layers
        paint(Q, wash=col, ink=None)
        if dk:
            xs = [p[0] for p in Q]
            ys = [p[1] for p in Q]
            cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
            w, h = max(xs) - min(xs), max(ys) - min(ys)
            G.c.save()
            G.c.clipPath(skia.Path().addPoly([skia.Point(float(a), float(b)) for a, b in Q], True), skia.ClipOp.kIntersect, True)
            paint(ellPts(cx + sd[0] * w * .55, cy + sd[1] * h * .5, w * .62, h * .78, 14), wash=dk, washOp=int(opD * .45), ink=None)
            G.c.restore()
        if ink:
            inkStroke(Q, True, sw, inkCol or INK, br)
        return
    # base: thin flat wash + a bleeding watercolour layer with a darker wet edge
    paint(Q, wash=col, washOp=242, fill=col, fillOp=140, bleed=.06, tex=.5, border=.75, ink=None)
    if dk or lt:
        xs = [p[0] for p in Q]
        ys = [p[1] for p in Q]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        G.c.save()
        G.c.clipPath(skia.Path().addPoly([skia.Point(float(a), float(b)) for a, b in Q], True), skia.ClipOp.kIntersect, True)
        if dk:
            paint(ellPts(cx + sd[0] * w * .55, cy + sd[1] * h * .5, w * .62, h * .78, 20), fill=dk, fillOp=opD, bleed=.25, tex=.6, border=.3, ink=None)
        if lt:
            paint(ellPts(cx - sd[0] * w * .3, cy - sd[1] * h * .35 - h * .12, w * .3, h * .26, 16), fill=lt, fillOp=opL, bleed=.3, tex=.7, border=.2, ink=None)
        G.c.restore()
    if ink:
        inkStroke(Q, True, sw, inkCol or INK, br)


def ik(S, Hd, l1, l2, bend=1):
    dx, dy = Hd[0] - S[0], Hd[1] - S[1]
    d = math.hypot(dx, dy)
    d2 = clamp(d, .1, l1 + l2 - 1e-3)
    if d > d2:
        Hd = [S[0] + dx / d * d2, S[1] + dy / d * d2]
    a = math.atan2(Hd[1] - S[1], Hd[0] - S[0])
    c = clamp((l1 * l1 + d2 * d2 - l2 * l2) / (2 * l1 * d2), -1, 1)
    b = math.acos(c) * bend
    E = [S[0] + math.cos(a + b) * l1, S[1] + math.sin(a + b) * l1]
    return E, Hd


# ---------------------------------------------------------------- pieces (local unit coords, canvas already at feet)
def _boot(cx, u, sw, C, side=False, toe=1, rot=0, ox=0, oy=0):
    push()
    translate(ox * u, oy * u)
    if rot:
        rotate(rot)
    if side:
        pts = [[-.95, -2.0], [.75, -2.0], [.85, -.8], [1.95 * toe, -.55], [2.05 * toe, 0], [-1.0, 0]]
    else:
        pts = [[cx - 1.0, -2.0], [cx + 1.0, -2.0], [cx + 1.05, -.5], [cx + 1.12, 0], [cx - 1.12, 0], [cx - 1.05, -.5]]
    part(_P(pts, u), C['boot'], C['bootDk'], C['bootLt'], sd=(.6, .2), sw=sw * .8)
    if side:
        inkLine(_P([[-1.0, -.32], [2.0 * toe, -.32]], u), sw * .5, C['bootDk'], 'inkfine', 0)
        inkLine(_P([[-.95, -1.6], [.8, -1.6]], u), sw * .5, INK, 'inkfine', 0)
    else:
        inkLine(_P([[cx - 1.1, -.32], [cx + 1.1, -.32]], u), sw * .5, C['bootDk'], 'inkfine', 0)
        inkLine(_P([[cx - 1.0, -1.6], [cx + 1.0, -1.6]], u), sw * .5, INK, 'inkfine', 0)
    pop()


def _leg(x0, y0, x1, y1, u, sw, C, w=1.05):
    P = ribbon([[x0 * u, y0 * u], [(x0 + x1) / 2 * u, (y0 + y1) / 2 * u], [x1 * u, y1 * u]], w * u, w * .95 * u)
    part(P, C['skin'], C['skinDk'], None, sd=(.5, 0), sw=sw * .7, curv=False, opD=90)


def _hand(x, y, u, sw, C, r=.62):
    part(ellPts(x * u, y * u, r * u, r * .92 * u, 14), C['skin'], C['skinDk'], None, sd=(.4, .4), sw=sw * .7, opD=80)


def _arm(S, Hd, u, sw, C, bend=1, sleeve=None, item=None, far=False):
    E, Hd = ik(S, Hd, 2.35, 2.25, bend)
    col = sleeve or C['coat']
    if far:
        col = mixCol(col, C['coatDk'], .35)
    # wrist point a little before the hand
    dx, dy = Hd[0] - E[0], Hd[1] - E[1]
    d = math.hypot(dx, dy) or 1
    Wr = [Hd[0] - dx / d * .55, Hd[1] - dy / d * .55]
    P = ribbon(_P([S, E, Wr], u), 1.55 * u, 1.25 * u)
    part(P, col, mixCol(col, INK, .28), None, sd=(.3, .5), sw=sw * .8, curv=False, opD=90)
    # cuff
    cf = [Hd[0] - dx / d * .75, Hd[1] - dy / d * .75]
    inkLine(_P([[cf[0] - dy / d * .62, cf[1] + dx / d * .62], [cf[0] + dy / d * .62, cf[1] - dx / d * .62]], u), sw * .55, INK, 'inkfine', 0)
    _hand(Hd[0], Hd[1], u, sw, C)
    if item:
        push()
        translate(Hd[0] * u, Hd[1] * u)
        item(u, sw, C)
        pop()


def bottle(u, sw, C=AYU, s=1.0, cork=True, glowK=0):
    """the message bottle, centred on its belly; s = scale"""
    U = u * s
    if glowK > 0:
        glow(0, 0, 3.2 * U, '#FFE9A8', glowK)
    body = [[-.62, -.15], [-.55, .8], [-.3, 1.05], [.3, 1.05], [.55, .8], [.62, -.15], [.42, -.55], [.25, -.75], [-.25, -.75], [-.42, -.55]]
    neck = [[-.24, -.75], [.24, -.75], [.22, -1.25], [-.22, -1.25]]
    paint(_P(body, U), wash=C['glass'], washOp=210, ink=None)
    # rolled photo + shell inside
    paint(_P([[-.32, -.4], [.08, -.48], [.18, .72], [-.22, .8]], U), wash=C['paperC'], ink=INK, sw=sw * .35)
    paint(ellPts(.28 * U, .72 * U, .2 * U, .15 * U, 10), wash=C['shell'], ink=INK, sw=sw * .3)
    paint(_P(neck, U), wash=C['glass'], washOp=210, ink=None)
    inkStroke(throughClosed(_P(body, U), 4), True, sw * .55, INK, 'ink')
    inkStroke(_P(neck, U), True, sw * .5, INK, 'ink')
    if cork:
        paint(_P([[-.2, -1.2], [.2, -1.2], [.24, -1.6], [-.24, -1.6]], U), wash=C['cork'], ink=INK, sw=sw * .45)
    inkLine(_P([[-.4, -.2], [-.36, .55]], U), sw * .45, '#FFFFFF', 'inkfine', 0)


def hatShape(u, sw, C, view, old=False, lift=0, tilt=0):
    col, dk, lt = (C['hatOld'], C['hatOldDk'], C['hatOldLt']) if old else (C['hat'], C['hatDk'], C['hatLt'])
    push()
    translate(0, -lift * u)
    if tilt:
        translate(0, -16.3 * u)
        rotate(tilt)
        translate(0, 16.3 * u)
    if view == 'side':
        crown = [[-3.3, -16.6], [-3.0, -19.0], [-2.0, -19.6], [2.4, -19.6], [3.4, -19.0], [3.7, -16.6]]
        brim = [[-4.6, -16.9], [4.2, -16.9], [6.2, -15.75], [6.0, -15.3], [-4.7, -15.6], [-5.1, -16.0]]
    else:
        crown = [[-3.45, -16.6], [-3.15, -19.0], [-2.2, -19.6], [2.2, -19.6], [3.15, -19.0], [3.45, -16.6]]
        brim = [[-4.5, -16.95], [4.5, -16.95], [6.0, -15.75], [5.7, -15.25], [-5.7, -15.25], [-6.0, -15.75]]
    part(_P(crown, u), col, dk, lt, sd=(.7, -.1), sw=sw * .9)
    # band
    bx = (crown[0][0] + .05, crown[-1][0] - .05)
    paint(_P([[bx[0], -17.35], [bx[1], -17.35], [bx[1] + .05, -16.6], [bx[0] - .05, -16.6]], u), wash=mixCol(dk, INK, .25), ink=INK, sw=sw * .55)
    part(_P(brim, u), col, dk, lt, sd=(.2, .9), sw=sw * .9, opD=110)
    # stitch line on brim
    xs = [p[0] for p in brim]
    n = 9
    for i in range(n):
        a = lerp(min(xs) + .9, max(xs) - .9, i / n)
        b = a + (max(xs) - min(xs) - 1.8) / n * .55
        yy = -15.62 if view != 'side' else -15.7
        inkLine(_P([[a, yy], [b, yy]], u), sw * .32, mixCol(lt, '#FFFFFF', .3), 'inkfine', 0)
    if old:
        # frayed brim edge + a darker sun-bleach patch
        for i in range(10):
            fx = lerp(min(xs) + .4, max(xs) - .4, i / 9)
            inkLine(_P([[fx, -15.28], [fx + jit(.15), -14.95 - rnd() * .2]], u), sw * .35, dk, 'inkfine', 0)
        paint(_P([[1.0, -18.9], [2.3, -18.8], [2.4, -17.6], [1.1, -17.7]], u), wash=mixCol(col, '#EADFC6', .35), ink=INK, sw=sw * .4)
        for k in range(3):
            inkLine(_P([[1.0 + k * .5, -18.95], [1.1 + k * .5, -18.75]], u), sw * .3, INK, 'inkfine', 0)
    pop()


def face(u, sw, C, o, ex, side=False):
    """ex: dict(eyes=, mouth=, blush=, dimple=, lookX=, lookY=, brows=)"""
    eyes = ex.get('eyes', 'open')
    mouth = ex.get('mouth', 'flat')
    lx, ly = ex.get('lookX', 0) * .28, ex.get('lookY', 0) * .25
    xs = [2.55] if side else [-1.8, 1.8]
    ey = -13.35
    for i, x in enumerate(xs):
        if eyes in ('open', 'side', 'wide', 'sparkle', 'teary'):
            rx, ry = (.6, .86) if eyes != 'wide' else (.72, 1.0)
            if side:
                rx *= .8
            paint(ellPts((x + lx) * u, (ey + ly) * u, rx * u, ry * u, 16), wash=INK, ink=None)
            paint(ellPts((x + lx - .2) * u, (ey + ly - .32) * u, .22 * u, .27 * u, 10), wash='#FFFFFF', ink=None)
            paint(ellPts((x + lx + .2) * u, (ey + ly + .35) * u, .1 * u, .1 * u, 8), wash='#FFFFFF', washOp=220, ink=None)
            if eyes == 'sparkle':
                paint(starPts((x + lx + .15) * u, (ey + ly + .15) * u, .38 * u, .3, 4), wash='#FFF3B0', ink=None)
                paint(ellPts((x + lx) * u, (ey + ly + .5) * u, .45 * u, .2 * u, 10), wash='#7FA6E6', washOp=150, ink=None)
            if eyes == 'teary':
                paint(ellPts(x * u, (ey + .78) * u, .75 * u, .28 * u, 12), wash='#9CC9EC', washOp=200, ink=INK, sw=sw * .3)
        elif eyes == 'happy':
            inkLine(_P([[x - .65, ey + .35], [x, ey - .35], [x + .65, ey + .35]], u), sw * .9, INK, 'ink', .4)
        elif eyes == 'closed':
            inkLine(_P([[x - .65, ey], [x, ey + .3], [x + .65, ey]], u), sw * .85, INK, 'ink', .4)
        elif eyes == 'half':
            hx, hy = lx * 1.6, max(-.15, ly * .5)
            paint(_P([[x - .58 + hx, ey - .05], [x + .58 + hx, ey - .05], [x + .5 + hx, ey + .6], [x - .5 + hx, ey + .6]], u), wash=INK, ink=None)
            inkLine(_P([[x - .75, ey - .1], [x + .75, ey - .1]], u), sw * .8, INK, 'ink', 0)
        elif eyes == 'squeeze':
            s = -1 if (i == 0 and not side) else 1
            inkLine(_P([[x - .5 * s, ey - .5], [x + .45 * s, ey], [x - .5 * s, ey + .5]], u), sw * .85, INK, 'ink', 0)
    br = ex.get('brows')
    if br:
        for i, x in enumerate(xs):
            s = -1 if (i == 0 and not side) else 1
            if br == 'sad':
                inkLine(_P([[x - .6 * s, -14.75], [x + .55 * s, -15.15]], u), sw * .55, INK, 'inkfine', 0)
            elif br == 'up':
                inkLine(_P([[x - .6, -15.0], [x, -15.25], [x + .6, -15.0]], u), sw * .55, INK, 'inkfine', .5)
            elif br == 'knit':
                inkLine(_P([[x - .6 * s, -15.15], [x + .55 * s, -14.8]], u), sw * .55, INK, 'inkfine', 0)
    # blush
    bl = ex.get('blush', 0)
    bxs = [2.9] if side else [-2.95, 2.95]
    if bl:
        for x in bxs:
            paint(ellPts(x * u, -12.35 * u, .78 * u, .36 * u, 12), fill=C['blush'], fillOp=150 * bl, bleed=.25, ink=None)
    # nose
    nx = 3.95 if side else .05
    paint(ellPts(nx * u, -12.72 * u, .17 * u, .12 * u, 8), wash=mixCol(C['skinDk'], C['blush'], .3), ink=None)
    # mouth
    mx = 3.0 if side else 0
    my = -11.95
    w = .55 if side else 1
    if mouth == 'flat':
        inkLine(_P([[mx - .55 * w, my], [mx + .55 * w, my]], u), sw * .7, INK, 'ink', 0)
    elif mouth == 'small':
        inkLine(_P([[mx - .5 * w, my - .05], [mx, my + .16], [mx + .5 * w, my - .05]], u), sw * .65, INK, 'ink', .5)
    elif mouth == 'smile':
        inkLine(_P([[mx - .85 * w, my - .2], [mx, my + .35], [mx + .85 * w, my - .2]], u), sw * .75, INK, 'ink', .5)
    elif mouth == 'grin':
        P = [[mx - .95 * w, my - .3], [mx + .95 * w, my - .3], [mx + .6 * w, my + .5], [mx, my + .72], [mx - .6 * w, my + .5]]
        paint(throughClosed(_P(P, u), 3), wash='#7E2E36', ink=INK, sw=sw * .6)
        paint(ellPts(mx * u, (my + .45) * u, .45 * w * u, .2 * u, 10), wash='#EE7C86', ink=None)
    elif mouth == 'o':
        paint(ellPts(mx * u, (my + .1) * u, .32 * w * u, .4 * u, 12), wash='#7E2E36', ink=INK, sw=sw * .5)
    elif mouth == 'sad':
        inkLine(_P([[mx - .6 * w, my + .22], [mx, my - .12], [mx + .6 * w, my + .22]], u), sw * .65, INK, 'ink', .5)
    elif mouth == 'wavy':
        inkLine(_P([[mx - .8 * w, my], [mx - .4 * w, my - .2], [mx, my + .1], [mx + .4 * w, my - .2], [mx + .8 * w, my]], u), sw * .65, INK, 'ink', .3)
        paint(ellPts((mx + .35 * w) * u, (my + .3) * u, .28 * u, .22 * u, 8), wash='#EE7C86', ink=INK, sw=sw * .35)
    # dimples (小酒窝)
    dk = ex.get('dimple', mouth in ('smile', 'grin'))
    if dk:
        k = 1.0 if dk is True else dk
        dxs = [2.2] if side else [-1.62, 1.62]
        for x in dxs:
            s = -1 if x < 0 else 1
            paint(ellPts(x * u, -11.6 * u, .34 * u, .27 * u, 10), fill=C['blush'], fillOp=190 * k, bleed=.12, ink=None)
            inkLine(_P([[x - .2 * s, -11.92], [x + .06 * s, -11.62], [x - .08 * s, -11.32]], u), sw * .5 * k, mixCol(C['skinDk'], INK, .4), 'inkfine', .6)


def hairTop(u, sw, C, style, side):
    hc, hd, hl = C['hair'], mixCol(C['hair'], INK, .4), C['hairLt']
    if style == 'bald':
        for s_ in ((1,) if side else (-1, 1)):
            x0 = -4.0 if side else s_ * 4.3
            part(_P([[x0 - .4 * s_, -15.0], [x0 + .7 * s_, -14.6], [x0 + .5 * s_, -12.9], [x0 - .5 * s_, -13.2]], u), hc, None, hl, sw=sw * .6)
        inkLine(_P([[-1.6, -17.9], [-.6, -18.25], [.6, -18.25]], u), sw * .35, C['skinDk'], 'inkfine', .5)
        return
    if side:
        P = [[-5.0, -12.6], [-5.1, -15.6], [-3.8, -18.2], [-1.0, -19.2], [2.0, -19.0], [4.0, -17.6], [4.75, -15.6], [4.2, -15.9],
             [3.7, -15.1], [3.1, -15.8], [2.3, -15.2], [1.4, -16.1], [.4, -15.6], [-.6, -15.0], [-1.1, -13.4], [-2.0, -12.0], [-3.6, -11.6]]
    else:
        P = [[-4.9, -12.9], [-5.05, -15.6], [-3.9, -18.1], [-1.5, -19.25], [1.5, -19.25], [3.9, -18.1], [5.05, -15.6], [4.9, -12.9],
             [4.3, -13.8], [3.9, -15.2], [2.8, -14.7], [1.7, -15.45], [.5, -14.85], [-.6, -15.45], [-1.7, -14.85], [-2.8, -15.45], [-3.9, -15.0], [-4.3, -13.8]]
    if style == 'long' and not side:
        P = [[-5.0, -11.2], [-5.5, -12.6], [-5.3, -15.6]] + P[2:6] + [[5.3, -15.6], [5.5, -12.6], [5.0, -11.2], [4.4, -11.8], [4.5, -13.4]] + P[9:-1] + [[-4.5, -13.4], [-4.4, -11.8]]
    part(_P(P, u), hc, hd, hl, sd=(.3, .3), sw=sw * .85, curv=False, opL=170)
    if style == 'bun':
        part(ellPts(0, -19.9 * u, 1.7 * u, 1.4 * u, 16), hc, hd, hl, sw=sw * .8)
    if style == 'cap':
        part(_P([[-4.9, -16.6], [-4.3, -19.2], [-1.6, -20.2], [1.8, -20.2], [4.4, -19.2], [4.9, -16.6]], u), C.get('capC', '#8A7F6E'), C.get('capDk', '#635A4D'), None, sw=sw * .85)
        part(_P([[-1.0 if side else -4.9, -16.9], [5.9 if side else 4.9, -16.9], [6.6 if side else 5.6, -16.1], [-1.0 if side else -5.6, -16.1]], u), C.get('capDk', '#635A4D'), None, None, sw=sw * .8, curv=False)


# ---------------------------------------------------------------- the character
def ayu(x, y, u, o=None):
    """o: view front|side|back, flip, hands=dict(L=[x,y], R=[x,y]) (unit coords), itemL/itemR callables,
          legs 'stand'|'walk'|'run'|'sit', ph (walk phase 0..1), ex (face dict), mask (gaiter up), old (faded hat),
          hatLift, hatTilt, noHat, bob, child (memory version), shadow"""
    o = o or {}
    LITE[0] = o.get('lite', u < 15)
    C = o.get('C', AYU)
    view = o.get('view', 'front')
    side = view == 'side'
    back = view == 'back'
    sw = clamp(u / 15, .45, 2.6) * o.get('swMul', 1)
    child = o.get('child', False)
    ex = o.get('ex', {})
    legs = o.get('legs', 'stand')
    ph = o.get('ph', 0.0)
    boilSeed(f"ayu {o.get('key', 0)}")

    if o.get('shadow', True) and legs != 'lie':
        paint(ellPts(x, y + u * .1, u * (4.2 if not side else 3.6), u * .7, 20), fill=INK, fillOp=70, bleed=.3, border=.1, ink=None)
    push()
    translate(x, y)
    if o.get('rot'):
        rotate(o['rot'])
    if o.get('flip'):
        scale(-1, 1)
    if o.get('sy', 1) != 1:
        scale(1, o['sy'])
    sq = o.get('sq', 0)
    if sq:
        scale(1 + sq * .5, 1 - sq)
    bob = o.get('bob', 0)
    sitDrop = 2.7 if legs == 'sit' else 0
    run = legs == 'run'
    if run:
        bob += -abs(math.sin(ph * TAU)) * .6

    # ---------- legs + boots
    C0 = C
    if 'pants' in C:
        C = dict(C, skin=C['pants'], skinDk=C['pantsDk'])
    if not side:
        if legs == 'sit':
            pass
        else:
            for s in (-1, 1):
                lift = 0
                if legs == 'walk':
                    lift = max(0, math.sin((ph + (0 if s < 0 else .5)) * TAU)) * .7
                _leg(s * 1.3, -3.6 - bob * 0, s * 1.3, -1.7 - lift, u, sw, C)
                _boot(s * 1.3, u, sw, C, oy=-lift)
    else:
        if legs == 'sit':
            # far foot peeks out behind the near shin
            _boot(0, u, sw, dict(C, boot=mixCol(C['boot'], C['bootDk'], .35)), side=True, ox=2.55, oy=0, toe=.9)
        else:
            for i in (0, 1):
                if legs in ('walk', 'run'):
                    amp = .42 if legs == 'walk' else .78
                    a = math.sin((ph + (0 if i == 0 else .5)) * TAU) * amp
                else:
                    a = [.04, -.04][i]
                Cl = C if i else dict(C, skin=mixCol(C['skin'], C['skinDk'], .3), boot=mixCol(C['boot'], C['bootDk'], .35))
                push()
                translate((-.3 + i * .6) * u, (-3.55 + bob) * u)
                rotate(-a)
                lift = 0
                if legs == 'run' and a < 0:
                    lift = -a * .9        # trailing leg kicks up behind
                _leg(0, 0, 0, 1.95, u, sw, Cl)
                _boot(0, u, sw, Cl, side=True, ox=.35, oy=1.95 + 1.75, rot=lift)
                pop()

    C = C0
    push()
    translate(0, (bob + sitDrop) * u)
    # ---------- far arm (side view) / back view arms drawn after body
    hands = o.get('hands', {})
    if side:
        Sfar = [-.3, -9.5]
        Hfar = hands.get('L', [-1.0, -5.4] if not run else [-2.4 + 1.6 * math.sin(ph * TAU), -7.0])
        _arm(Sfar, Hfar, u, sw, C, bend=-1, far=True, item=o.get('itemL'))

    # ---------- shorts
    if child:
        shorts = [[-2.8, -5.3], [2.8, -5.3], [3.0, -3.4], [.25, -3.4], [0, -3.9], [-.25, -3.4], [-3.0, -3.4]]
        part(_P(shorts if not side else [[-2.3, -5.3], [2.4, -5.3], [2.6, -3.4], [-2.5, -3.4]], u), C['swim'], C['swimDk'], None, sd=(.5, .5), sw=sw * .8, curv=False)
    elif legs != 'sit' or not side:
        shorts = [[-2.9, -5.4], [2.9, -5.4], [3.05, -3.3], [.25, -3.3], [0, -3.85], [-.25, -3.3], [-3.05, -3.3]]
        if side:
            shorts = [[-2.4, -5.4], [2.5, -5.4], [2.7, -3.3], [-2.55, -3.3]]
        part(_P(shorts, u), C['shorts'], C['shortsDk'], None, sd=(.6, .5), sw=sw * .8, curv=False)
    else:
        part(_P([[-2.4, -5.4], [1.6, -5.4], [2.6, -4.3], [2.2, -3.2], [-2.6, -3.0]], u), C['shorts'], C['shortsDk'], None, sw=sw * .8, curv=False)

    # ---------- torso
    if child:
        tee = [[-2.1, -10.3], [2.1, -10.3], [2.8, -9.8], [3.0, -8.6], [2.9, -5.1], [-2.9, -5.1], [-3.0, -8.6], [-2.8, -9.8]]
        if side:
            tee = [[-1.8, -10.3], [1.9, -10.3], [2.3, -9.4], [2.4, -5.1], [-2.3, -5.1], [-2.3, -9.4]]
        part(_P(tee, u), C['tee'], C['teeDk'], None, sd=(.6, .4), sw=sw * .85)
        if not back:
            # little palm-tree print
            cx = 1.4 if side else 0
            inkLine(_P([[cx, -6.0], [cx + .15, -7.3], [cx + .05, -8.2]], u), sw * .5, '#8A6A45', 'ink', .5)
            for a in (-2.4, -1.6, -.9, -.2, .5):
                inkLine(_P([[cx + .05, -8.2], [cx + .05 + math.cos(a) * 1.0, -8.2 + math.sin(a) * .8 + .3]], u), sw * .55, PAL['sap'], 'ink', 0)
            paint(ellPts(cx * u, -5.75 * u, .9 * u, .25 * u, 10), wash=PAL['ochre'], washOp=160, ink=None)
    else:
        if side:
            coat = [[-1.9, -10.5], [1.9, -10.5], [2.45, -9.6], [2.75, -4.4], [0, -4.35], [-2.6, -4.4], [-2.5, -9.6]]
        else:
            coat = [[-2.2, -10.5], [2.2, -10.5], [3.0, -9.9], [3.25, -8.8], [3.42, -4.35], [0, -4.3], [-3.42, -4.35], [-3.25, -8.8], [-3.0, -9.9]]
        part(_P(coat, u), C['coat'], C['coatDk'], C['coatLt'], sd=(.65, .35), sw=sw)
        # hem band
        hx = (-2.6, 2.75) if side else (-3.4, 3.4)
        paint(_P([[hx[0] + .05, -5.0], [hx[1] - .05, -5.0], [hx[1], -4.4], [hx[0], -4.4]], u), fill=C['coatDk'], fillOp=150, bleed=.05, ink=None)
        inkLine(_P([[hx[0] + .1, -5.0], [hx[1] - .1, -5.0]], u), sw * .45, INK, 'inkfine', 0)
        if back:
            # hood lying on the back
            hood = [[-2.3, -10.5], [2.3, -10.5], [2.5, -9.3], [1.6, -8.1], [0, -7.7], [-1.6, -8.1], [-2.5, -9.3]]
            part(_P(hood, u), mixCol(C['coat'], C['coatDk'], .2), C['coatDk'], None, sd=(0, .6), sw=sw * .8)
            inkLine(_P([[-1.6, -9.9], [0, -9.0], [1.6, -9.9]], u), sw * .45, INK, 'inkfine', .5)
        elif side:
            hood = [[-1.9, -10.6], [-.5, -10.5], [-.9, -9.3], [-2.2, -8.6], [-2.95, -9.3], [-2.8, -10.3]]
            part(_P(hood, u), mixCol(C['coat'], C['coatDk'], .2), C['coatDk'], None, sd=(-.4, .4), sw=sw * .8)
            inkLine(_P([[2.0, -10.2], [2.3, -7.0], [2.45, -4.6]], u), sw * .5, INK, 'inkfine', .3)      # zip edge
            paint(_P([[.6, -6.9], [2.0, -6.9], [2.0, -6.35], [.6, -6.35]], u), fill=C['coatDk'], fillOp=150, ink=INK, sw=sw * .45)
        else:
            # zipper + pull, pockets, shoulder patch
            inkLine(_P([[0, -10.3], [.03, -7.5], [0, -4.5]], u), sw * .55, INK, 'inkfine', .3)
            for k in range(9):
                yy = -10.0 + k * .62
                inkLine(_P([[-.15, yy], [.15, yy]], u), sw * .28, mixCol(C['coatDk'], INK, .3), 'inkfine', 0)
            paint(_P([[-.17, -9.1], [.17, -9.1], [.2, -8.4], [-.2, -8.4]], u), wash='#D8D4CC', ink=INK, sw=sw * .35)
            for s in (-1, 1):
                paint(_P([[s * 1.0, -6.95], [s * 2.6, -6.95], [s * 2.55, -6.35], [s * 1.05, -6.35]], u), fill=C['coatDk'], fillOp=150, ink=INK, sw=sw * .45)
            if not o.get('hairStyle'):
                paint(_P([[1.45, -9.9], [2.55, -9.75], [2.6, -8.7], [1.5, -8.8]], u), wash=C['patch'], ink=INK, sw=sw * .45)
                for k in range(4):
                    inkLine(_P([[1.5 + k * .3, -9.95], [1.55 + k * .3, -9.7]], u), sw * .25, INK, 'inkfine', 0)

    # ---------- neck gaiter
    if not child:
        if o.get('mask') and not back:
            mk = [[-3.4, -13.0], [3.4, -13.0], [3.5, -11.0], [2.4, -10.0], [-2.4, -10.0], [-3.5, -11.0]] if not side else \
                 [[-.6, -13.0], [3.95, -13.0], [3.7, -11.0], [2.4, -10.0], [-1.8, -10.0], [-1.6, -11.6]]
        else:
            mk = None
        if not mk:
            g0 = ellPts((.15 if side else 0) * u, -10.45 * u, 2.15 * u, .72 * u, 18)
            part(g0, C['gaiter'], C['gaiterDk'], None, sd=(.3, .6), sw=sw * .7)
            inkLine(_P([[-1.2, -10.55], [-.4, -10.2]], u), sw * .3, C['gaiterDk'], 'inkfine', 0)

    # ---------- bottle pendant
    if not back and not child and not o.get('noBottle'):
        bxp = 2.45 if side else -1.05
        inkLine(_P([[bxp - (.9 if not side else 1.2), -10.2], [bxp, -8.85]], u), sw * .3, '#6B4A35', 'inkfine', .3)
        if not side:
            inkLine(_P([[bxp + .9, -10.2], [bxp, -8.85]], u), sw * .3, '#6B4A35', 'inkfine', .3)
        push()
        translate(bxp * u, -7.85 * u)
        bottle(u, sw, C, .62, glowK=o.get('bottleGlow', 0))
        pop()

    # ---------- head
    hd = -14.55
    if not side:
        for s in (-1, 1):
            part(ellPts(s * 4.5 * u, -13.85 * u, .62 * u, .88 * u, 12), C['skin'], C['skinDk'], None, sd=(s * .5, .2), sw=sw * .7)
    headPts = []
    for i in range(36):
        a = i / 36 * TAU
        rx = 4.72 if math.sin(a) < 0 else 4.72 - .3 * math.sin(a) ** 2
        ry = 4.3
        headPts.append([(math.cos(a) * rx + (.25 if side else 0)) * u, (hd + math.sin(a) * ry) * u])
    if back:
        part(headPts, C['hair'], mixCol(C['hair'], INK, .4), C['hairLt'], sd=(.2, .6), sw=sw, curv=False, opL=190)
        for k in range(7):
            xx = -3.0 + k
            inkLine(_P([[xx * .9, -16.2], [xx * 1.05 + jit(.2), -12.4 - abs(xx) * .25]], u), sw * .32, C['hairLt'], 'inkfine', .4)
        # nape tufts
        tuft = [[-3.6, -11.9], [-2.6, -10.9], [-1.8, -11.6], [-.9, -10.7], [0, -11.5], [.9, -10.7], [1.8, -11.6], [2.6, -10.9], [3.6, -11.9]]
        inkLine(_P(tuft, u), sw * .6, INK, 'ink', .2)
        for s in (-1, 1):
            part(ellPts(s * 4.55 * u, -13.6 * u, .55 * u, .82 * u, 12), C['skin'], C['skinDk'], None, sw=sw * .7)
    else:
        part(headPts, C['skin'], C['skinDk'], C['skinLt'], sd=(.55 if not side else -.6, .45), sw=sw, curv=False, opD=70, opL=120)
        # hair under the hat
        if side and o.get('hairStyle'):
            part(ellPts(-.05 * u, -13.65 * u, .58 * u, .8 * u, 12), mixCol(C['skin'], C['blush'], .18), C['skinDk'], None, sd=(-.4, .2), sw=sw * .7)
        elif side:
            # back hair, clipped to the skull so it follows the head outline
            G.c.save()
            G.c.clipPath(skia.Path().addPoly([skia.Point(float(a), float(b)) for a, b in headPts], True), skia.ClipOp.kIntersect, True)
            hairB = [[-5.4, -17.0], [.4, -17.0], [.1, -15.6], [-.9, -15.2], [-1.25, -14.6], [-1.15, -13.2], [-1.7, -12.3], [-2.1, -11.0], [-5.4, -11.0]]
            part(_P(hairB, u), C['hair'], mixCol(C['hair'], INK, .4), C['hairLt'], sd=(-.5, .4), sw=sw * .8, curv=False, opL=170)
            for k in range(4):
                inkLine(_P([[-4.2 + k * .7, -15.6 + k * .1], [-3.9 + k * .75, -13.6 + k * .3]], u), sw * .3, C['hairLt'], 'inkfine', .4)
            G.c.restore()
            inkStroke(headPts, True, sw, INK, 'ink')
            # nape tuft sticking out below the skull
            nape = [[-4.3, -12.5], [-4.6, -11.8], [-3.9, -11.95], [-3.5, -11.3], [-3.0, -11.7], [-2.5, -11.2], [-2.3, -11.9]]
            part(_P(nape, u), C['hair'], None, None, sw=sw * .6, curv=False)
            part(ellPts(-.05 * u, -13.65 * u, .58 * u, .8 * u, 12), mixCol(C['skin'], C['blush'], .18), C['skinDk'], None, sd=(-.4, .2), sw=sw * .7)
            inkLine(_P([[-.15, -14.0], [.1, -13.5], [-.1, -13.25]], u), sw * .3, C['skinDk'], 'inkfine', .5)
            bang = [[1.6, -16.4], [4.5, -16.4], [4.45, -15.25], [3.9, -15.65], [3.45, -14.95], [2.95, -15.55], [2.45, -15.05], [2.0, -15.6]]
            part(_P(bang, u), C['hair'], None, C['hairLt'], sw=sw * .7, curv=False)
        elif not o.get('hairStyle'):
            for s in (-1, 1):
                tuft = [[s * 3.0, -16.4], [s * 4.95, -15.9], [s * 5.0, -14.4], [s * 5.3, -13.6], [s * 4.75, -13.75], [s * 4.95, -12.6], [s * 4.3, -13.1], [s * 4.0, -14.6], [s * 3.4, -15.3]]
                part(_P(tuft, u), C['hair'], mixCol(C['hair'], INK, .4), C['hairLt'], sd=(s * .3, .3), sw=sw * .8, curv=False)
            bang = [[-3.6, -16.3], [3.6, -16.3], [3.4, -15.0], [2.7, -15.5], [2.0, -14.75], [1.2, -15.45], [.3, -14.65], [-.6, -15.4], [-1.5, -14.8], [-2.3, -15.45], [-3.0, -14.95]]
            part(_P(bang, u), C['hair'], mixCol(C['hair'], INK, .4), C['hairLt'], sd=(.2, .2), sw=sw * .8, curv=False)
        face(u, sw, C, o, ex, side)
        if o.get('hairStyle'):
            hairTop(u, sw, C, o['hairStyle'], side)
        if o.get('mask'):
            mk = [[-3.6, -13.0], [3.6, -13.0], [3.7, -11.2], [2.6, -10.0], [-2.6, -10.0], [-3.7, -11.2]] if not side else \
                 [[-.5, -13.0], [4.2, -12.9], [4.0, -11.0], [2.6, -10.0], [-1.7, -10.0], [-1.4, -11.6]]
            part(_P(mk, u), C['gaiter'], C['gaiterDk'], None, sd=(.3, .5), sw=sw * .75)
            for k in range(3):
                inkLine(_P([[-2.6 + k * 2.4 if not side else .3 + k * 1.1, -12.3], [-2.0 + k * 2.4 if not side else .8 + k * 1.1, -11.4]], u), sw * .3, C['gaiterDk'], 'inkfine', 0)

    # ---------- hat
    if not o.get('noHat'):
        hatShape(u, sw, C, view, old=o.get('old', False) and not child, lift=o.get('hatLift', 0), tilt=o.get('hatTilt', 0))

    # ---------- sitting: knees up in front of the chest (ground-frame numbers minus the drop)
    if legs == 'sit' and side:
        d = sitDrop + bob
        hip, knee, ank = [.6, -1.6 - d], [2.85, -4.15 - d], [3.2, -1.75 - d]
        mid = [lerp(hip[0], knee[0], .45), lerp(hip[1], knee[1], .45)]
        _leg(mid[0], mid[1], knee[0], knee[1], u, sw, C, 1.3)            # bare thigh up to the knee
        _leg(knee[0], knee[1], ank[0], ank[1], u, sw, C, 1.15)           # shin straight down
        _boot(0, u, sw, C, side=True, ox=ank[0] + .25, oy=-d, toe=.9)
        th = ribbon(_P([[hip[0] - 1.0, hip[1] + .25], hip, mid], u), 1.9 * u, 1.6 * u)   # shorts leg
        part(th, C['shorts'], C['shortsDk'], None, sd=(.2, .6), sw=sw * .8, curv=False)
        push()
        translate(knee[0] * u, knee[1] * u)
        part(ellPts(0, 0, .78 * u, .72 * u, 14), C['skin'], C['skinDk'], C['skinLt'], sd=(.3, .5), sw=sw * .7)
        pop()
    # ---------- near arms
    if side:
        S = [.6, -9.5]
        Hn = hands.get('R', [1.15, -5.3] if not run else [1.2 - 1.8 * math.sin(ph * TAU), -7.2])
        _arm(S, Hn, u, sw, C, bend=-1, item=o.get('itemR'), sleeve=C['tee'] if child else None)
    else:
        for s, k in ((-1, 'L'), (1, 'R')):
            S = [s * 2.75, -9.55]
            Hd = hands.get(k, [s * 3.75, -5.25])
            _arm(S, Hd, u, sw, C, bend=1 if s < 0 else -1, item=o.get('item' + k), sleeve=C['tee'] if child else None)
    if legs == 'sit' and side:
        pass
    pop()
    pop()
