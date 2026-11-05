# clawd.py: Clawd in watercolour and ink, ported from the painted-animation template (clawd.js).
# (x, y) = ground point between the feet; u = body unit (body 10u wide, 8u tall with legs).
import math
from eng import *

VIEWS = {
    'front': dict(L=-5, R=5, face=dict(cx=0, fw=1, sides=[-1, 1], mx=0, bx=3.6), hat=0, hw=1,
                  legs=[[-4, 0], [-2, 0], [1, 0], [3, 0]], arms=[[-4.9, -1, 'L', 0], [4.9, 1, 'R', 0]]),
    'q': dict(L=-5, R=5.1, strip=[-5, -2.3], seam=-2.3, face=dict(cx=1.5, fw=.74, sides=[-1, 1], mx=.3, bx=3.6), hat=.6, hw=1,
              legs=[[-4.3, 1], [-1.8, 0], [.8, 0], [3.3, 0]], arms=[[5, 1, 'R', 2], [-4.7, -1, 'L', 1]]),
    'side': dict(L=-3.1, R=3.1, face=dict(cx=1.35, fw=.55, sides=[1], mx=1.7, bx=1), hat=.3, hw=.66,
                 legs=[[-2.1, 1], [1.3, 1], [-2.6, 0], [.9, 0]], arms=[[1.6, 0, 'L', 1]]),
    'qback': dict(L=-5.1, R=5, strip=[2.3, 5], seam=2.3, face=None, hat=-.4, hw=1,
                  legs=[[3.3, 1], [.8, 0], [-1.8, 0], [-4.3, 0]], arms=[[-5, -1, 'R', 2], [4.7, 1, 'L', 1]]),
    'back': dict(L=-5, R=5, face=None, hat=0, hw=1, back=True,
                 legs=[[-4, 0], [-2, 0], [1, 0], [3, 0]], arms=[[-4.9, -1, 'R', 0], [4.9, 1, 'L', 0]]),
}


def spinView(a):
    K = [['front', 0], ['q', 0], ['side', 0], ['qback', 0], ['back', 0], ['qback', 1], ['side', 1], ['q', 1]]
    v, f = K[((round(a * 8) % 8) + 8) % 8]
    return dict(view=v, flip=bool(f))


def turn(t, t0, t1, a0, a1):
    k = ease(seg(t, t0, t1))
    v = spinView(lerp(a0, a1, k))
    v.update(smear=.55 * math.sin(k * math.pi) if t0 < t < t1 else 0, smearDir=0)
    return v


TINT = dict(pale='#F6E6D2', flush='#E23E36', blue='#6D86BE', rosy='#EF8EA8', green='#98B25E', gold='#F0BE46')


def tintCols(o):
    c = dict(col=o.get('col') or PAL['clay'], dk=o.get('dk') or PAL['clayDk'], lt=o.get('lt') or '#F5B394')
    tn = o.get('tint')
    tc = TINT.get(tn, tn) if tn else None
    k = clamp(o.get('tintK', 1) if o.get('tintK') is not None else 1)
    if not tc or k <= 0:
        return c
    return dict(col=mixCol(c['col'], tc, .55 * k), dk=mixCol(c['dk'], mixCol(tc, INK, .35), .5 * k),
                lt=mixCol(c['lt'], mixCol(tc, '#FFFFFF', .4), .45 * k))


def g(o, k, d=None):
    v = o.get(k)
    return d if v is None else v


def clawd(x, y, u, o=None):
    o = o or {}
    G.CLAWD_N += 1
    cid = o.get('boilKey', G.CLAWD_N)

    def rs(part):
        boilSeed(f'clawd {cid} {part}')
    x += g(o, 'dx', 0) * u
    vname = o.get('view') or 'front'
    V = VIEWS.get(vname, VIEWS['front'])
    dy = g(o, 'dy', 0) * u
    sq = g(o, 'sq', 0) + g(o, 'take', 0)
    sm = clamp(g(o, 'smear', 0))
    sw = clamp(u / 15, .45, 2.4) * g(o, 'swMul', 1)
    J = u * .07
    tc = tintCols(o)
    col, dk, lt = tc['col'], tc['dk'], tc['lt']
    far = mixCol(dk, INK, .22)
    lite = o.get('lite', False)

    rs('shadow')
    if not o.get('noShadow'):
        f = 1 - min(.5, abs(g(o, 'dy', 0)) * .06)
        w = (V['R'] - V['L']) / 10
        paint(ellPts(x, y + u * .15, u * 5.6 * f * w, u * f, 22), fill=INK, fillOp=90 * g(o, 'shadowK', 1), bleed=.25, tex=.3, border=.1, ink=None, lite=lite)
    if sm > .05:
        smearTrail(x, y + dy, u, V, sm, o.get('smearDir', -1 if o.get('flip') else 1), col)

    push()
    translate(x, y + dy)
    if o.get('rot'):
        rotate(o['rot'])
    scale((-1 if o.get('flip') else 1) * g(o, 'sx', 1) * (1 + sq * .6) * (1 + sm * .35), g(o, 'sy', 1) * (1 - sq))

    def arm(spec):
        px, dr, which, layer = spec
        rs('arm' + which)
        a = g(o, 'aL', .2) if which == 'L' else g(o, 'aR', .2)
        hook = o.get('armL') if which == 'L' else o.get('armR')
        push()
        translate((px + dr * .55 * clamp((abs(a) - .7) / .9)) * u, -4.5 * u)
        if dr == 0:
            translate(0, .3 * u)
            rotate(.7 - a)
            paint(rectPts(-.2 * u, -.45 * u, 2.3 * u, .9 * u, J * .6), wash=col, fill=dk, fillOp=60, tex=.5, ink=INK, sw=sw * .8, lite=True)
            if hook:
                translate(2.1 * u, 0)
                hook(u, sw)
        else:
            rotate(a if dr < 0 else -a)
            paint(rectPts(-2.2 * u if dr < 0 else 0, -.5 * u, 2.2 * u, u, J * .6), wash=mixCol(col, dk, .4) if layer == 2 else col,
                  fill=dk, fillOp=60, tex=.5, ink=INK, sw=sw * .8, lite=True)
            if hook:
                translate(dr * 2.2 * u, 0)
                if dr < 0:
                    scale(-1, 1)
                hook(u, sw)
        pop()

    for a in V['arms']:
        if a[3] != 1:
            arm(a)
    if not o.get('noLegs'):
        for i, (lx, isFar) in enumerate(V['legs']):
            rs('leg%d' % i)
            h, sx = 2.2, 0
            wk = o.get('walk')
            if wk is not None:
                if vname == 'side':
                    ph = (wk + [0, .5, .5, 0][i]) * TAU
                    sx = math.sin(ph) * .55
                    h = 2.2 - max(0, math.cos(ph)) * .8
                else:
                    ph = math.sin((wk + (.5 if i % 2 else 0)) * TAU)
                    if ph > 0:
                        h = 2.2 - ph * .9
            paint(rectPts((lx + sx) * u, -2.4 * u, u, h * u, J * .6), wash=far if isFar else dk, ink=INK, sw=sw * .8)

    rs('body')
    L, R = V['L'] * u, V['R'] * u
    wk = (V['R'] - V['L']) / 10
    body = rectPts(L, -8 * u, R - L, 6 * u, J)
    paint(body, wash=col, ink=None)
    if 'strip' in V:
        st = V['strip']
        px = (V['seam'] + V['R']) / 2 - 1.2 if st[0] < 0 else (V['L'] + V['seam']) / 2 - .6
    else:
        px = -1.6 * wk
    paint(ellPts(px * u, -6.4 * u, 3.4 * u * (.75 if 'strip' in V else wk), 1.5 * u, 18, J * 2, -.08), fill=lt,
          fillOp=80 if V.get('back') else 120, bleed=.2, tex=.85, border=.8, ink=None, lite=lite)
    paint(rectPts(L + .2 * u, -3.8 * u, R - L - .4 * u, 1.6 * u, J), fill=dk, fillOp=120, bleed=.03, tex=.7, border=.5, ink=None, lite=lite)
    if 'strip' in V:
        st = V['strip']
        paint(rectPts(st[0] * u, -8 * u, (st[1] - st[0]) * u, 6 * u, J * .5), fill=dk, fillOp=150, bleed=.04, tex=.6, border=.4, ink=None, lite=lite)
        inkLine([[V['seam'] * u + jit(J), -7.9 * u], [V['seam'] * u + jit(J), -5 * u], [V['seam'] * u + jit(J), -2.1 * u]], sw * .55, INK, 'inkfine', 0)
    paint(body, ink=INK, sw=sw)
    if g(o, 'gloom', 0) > .02:
        gloom(u, sw, V, o['gloom'])
    F = V['face']
    if F:
        push()
        translate(F['cx'] * u, 0)
        scale(F['fw'], 1)
        if o.get('blush'):
            blush(u, sw, F, 1 if o['blush'] is True else o['blush'])
        rs('eyes')
        eyes(u, o, sw, F['sides'], sm)
        rs('mouth')
        push()
        translate(F['mx'] * u, 0)
        mouth(u, o.get('mouth'), sw)
        pop()
        pop()
    rs('hat')
    push()
    translate(V['hat'] * u, 0)
    scale(V['hw'], 1)
    hats = o.get('hat')
    if hats:
        for hname in (hats if isinstance(hats, (list, tuple)) else [hats]):
            hat(u, hname, sw, o)
    pop()
    for a in V['arms']:
        if a[3] == 1:
            arm(a)
    rs('draw')
    if o.get('draw'):
        o['draw'](u, sw)
    pop()

    rs('emote')
    if o.get('emote'):
        top = o['emote'] in EMOTE_TOP
        d = -1 if o.get('flip') else 1
        ex = x + d * V['hat'] * u if top else x + d * (V['R'] + .4) * u
        ey = y + dy + (-10.4 if top else -8.6) * u * (1 - sq) - (2.2 * u if (top and hats) else 0)
        emote(o['emote'], ex, ey, u * .9, g(o, 'emoteK', 1), g(o, 'emoteAge', G.T))
    rs('after')


def smearTrail(x, y, u, V, k, d, col):
    sides = [-1, 1] if d == 0 else [-d]
    for s in sides:
        for i in range(4):
            yy = y - (7.2 - i * 1.5) * u
            x0 = x + s * (V['R'] - .5) * u
            ln = (3 + 3 * hash1(i + 7 * s)) * u * k
            inkLine([[x0, yy], [x0 + s * ln * .5, yy + jit(u * .1)], [x0 + s * ln, yy]], 2.2 * k, col, 'dry', .3)
            if i % 2:
                inkLine([[x0 + s * ln * .3, yy + .5 * u], [x0 + s * ln * 1.1, yy + .5 * u]], .6, INK, 'inkfine', 0)


def gloom(u, sw, V, gl):
    L, R = V['L'] * u, V['R'] * u
    paint(rectPts(L + .15 * u, -7.9 * u, R - L - .3 * u, 2.6 * u, u * .05), fill=PAL['indigo'], fillOp=150 * gl, bleed=.08, tex=.5, border=.6, ink=None)
    n = round((V['R'] - V['L']) * .7)
    for i in range(n):
        gx = lerp(L + .7 * u, R - .7 * u, i / max(1, n - 1))
        inkLine([[gx, -7.8 * u], [gx + jit(u * .05), (-7.8 + 2.4 * gl * (.7 + .3 * hash1(i))) * u]], sw * .45, INK, 'inkfine', 0)


def blush(u, sw, F, b):
    for s in F['sides']:
        bx = s * F['bx'] * u
        paint(ellPts(bx, -4.6 * u, u * .85, u * .42, 14), fill=PAL['rose'], fillOp=170 * clamp(b), bleed=.2, ink=None)
        if b > .6:
            for k in range(3):
                inkLine([[bx - .5 * u + k * .4 * u, -4.35 * u], [bx - .3 * u + k * .4 * u, -4.85 * u]], sw * .4, mixCol(PAL['rose'], INK, .3), 'inkfine', 0)


def eyes(u, o, sw, sides, smear=0):
    e = o.get('eyes')
    if isinstance(e, (list, tuple)):
        kinds = list(e)
    elif e == 'wink':
        kinds = ['happy', 'normal']
    else:
        kinds = [e or 'normal', e or 'normal']
    sqz = clamp(g(o, 'squint', 0))
    if smear > .5:
        for s in sides:
            inkLine([[s * 2.5 * u - .9 * u, -6 * u], [s * 2.5 * u + .9 * u, -6 * u]], sw * 1.4, INK, 'ink', 0)
        return
    if sqz > .8:
        for s in sides:
            inkLine([[s * 2.5 * u - .8 * u, -5.9 * u], [s * 2.5 * u + .8 * u, -5.9 * u]], sw, INK, 'ink', 0)
        return
    if kinds[0] == 'shades':
        P = lambda pts: [[a * u, b * u] for a, b in pts]
        lens = lambda cx: P([[cx - 1.4, -7.1], [cx + 1.4, -7.1], [cx + 1.3, -6.2], [cx + .8, -5.35], [cx, -5.2], [cx - .8, -5.35], [cx - 1.3, -6.2]])
        if len(sides) > 1:
            for s in (-1, 1):
                inkLine(P([[s * 3.9, -6.85], [s * 5, -6.95]]), sw * .8, INK, 'ink', 0)
            inkLine(P([[-1.15, -6.75], [0, -7.05], [1.15, -6.75]]), sw * .8, INK, 'ink', .5)
        else:
            inkLine(P([[1.1, -6.85], [-5, -6.95]]), sw * .8, INK, 'ink', 0)
        for s in sides:
            cx = s * 2.5
            paint(lens(cx), wash='#2A2740', ink=INK, sw=sw * .9, curv=.3)
            inkLine(P([[cx - .85, -6.35], [cx - .25, -6.85]]), sw * .45, PAL['cream'], 'inkfine', 0)
        return
    if sqz > 0:
        push()
        translate(0, -6 * u)
        scale(1 + sqz * .15, 1 - sqz)
        translate(0, 6 * u)
    for s in sides:
        push()
        translate(s * 2.5 * u, -6 * u)
        eye(kinds[0 if s < 0 else 1], s, u, o, sw)
        pop()
    if sqz > 0:
        pop()


def eye(e, s, u, o, sw):
    T = G.T
    lx, ly = g(o, 'lookX', 0) * u * .5, g(o, 'lookY', 0) * u * .4

    def slit(w, h):
        paint(rectPts(-w / 2 * u + lx, -h / 2 * u + ly, w * u, h * u, u * .04), wash=INK, ink=None)
        if u > 9:
            paint(ellPts(lx - w * .18 * u, ly - h * .29 * u, u * .17 * w, u * .24 * w, 10), wash=PAL['cream'], washOp=230, ink=None)
    blinkOn = e in ('normal', 'look', 'wide') and ((T * .9 + g(o, 'seed', 0) * 1.7) % 3.3) < .12
    if blinkOn:
        inkLine([[-.7 * u, .5 * u], [.7 * u, .5 * u]], sw, INK, 'ink', 0)
        return

    def lineEye(pts, w=1.3, c=.2):
        inkLine([[a * u, b * u] for a, b in pts], sw * w, INK, 'ink', c)
    if e in ('normal', 'look'):
        slit(1, 2)
    elif e == 'wide':
        slit(1.25, 2.7)
    elif e == 'happy':
        lineEye([[-.9, .7], [0, -.5], [.9, .7]])
    elif e == 'closed':
        lineEye([[-.9, .2], [0, .6], [.9, .2]], 1.2, .4)
    elif e == 'sleepy':
        paint(rectPts(-.5 * u + lx, .05 * u, u, .95 * u, u * .03), wash=INK, ink=None)
        lineEye([[-.8, .05], [0, -.1], [.8, .1]], 1.1, .4)
    elif e == 'narrow':
        paint(rectPts(-.6 * u + lx, -.1 * u + ly, 1.2 * u, .7 * u, u * .03), wash=INK, ink=None)
    elif e in ('angry', 'determined'):
        hi = .75 if e == 'angry' else .5
        top = -.7 if e == 'angry' else -.55
        P = [[-.65, top if s < 0 else top + hi], [.65, top + hi if s < 0 else top], [.65, 1], [-.65, 1]]
        paint([[a * u + lx, b * u + ly] for a, b in P], wash=INK, ink=None)
        if e == 'determined' and u > 9:
            paint(ellPts(lx - .2 * u, ly + .25 * u, u * .16, u * .2, 8), wash=PAL['cream'], ink=None)
    elif e in ('sad', 'teary'):
        P = [[-.6, -.2 if s < 0 else -.85], [.6, -.85 if s < 0 else -.2], [.6, .9], [-.6, .9]]
        paint([[a * u + lx, b * u + ly] for a, b in P], wash=INK, ink=None)
        if u > 9:
            paint(ellPts(lx - .18 * u, ly + .05 * u, u * .16, u * .22, 8), wash=PAL['cream'], ink=None)
        if e == 'teary':
            w = math.sin(T * 9 + s) * .06 * u
            paint(ellPts(0, .95 * u + w, .95 * u, .38 * u, 14), wash=PAL['sky'], washOp=210, ink=INK, sw=sw * .4)
            paint(ellPts(-.35 * u, .85 * u + w, .18 * u, .1 * u, 8), wash='#FFFFFF', ink=None)
    elif e == 'cry':
        lineEye([[a * -s, b] for a, b in [[-.9, .45], [-.3, -.05], [.3, .15], [.9, -.2]]], 1.3, .3)
        Rr = [[(s * .55 + math.sin(T * 8 + k * 1.3 + s) * .12 * k / 5) * u, (.4 + k * .72) * u] for k in range(6)]
        paint(ribbon(Rr, .45 * u, .8 * u), wash=PAL['sky'], washOp=230, ink=INK, sw=sw * .45)
    elif e == 'squeeze':
        lineEye([[-.55 * -s, -.7], [.55 * -s, 0], [-.55 * -s, .7]], 1.3, 0)
    elif e == 'shine':
        paint(ellPts(lx * .6, ly * .6, u * .78, u * 1.12, 16), wash=INK, ink=None)
        paint(ellPts(lx * .6 - .25 * u, ly * .6 - .45 * u, u * .3, u * .38, 10), wash=PAL['cream'], ink=None)
        paint(ellPts(lx * .6 + .25 * u, ly * .6 + .45 * u, u * .14, u * .14, 8), wash=PAL['cream'], ink=None)
    elif e == 'scared':
        paint(ellPts(0, 0, u * .95, u * 1.15, 16), wash=PAL['cream'], ink=INK, sw=sw * .6)
        paint(ellPts(g(o, 'lookX', 0) * u * .3 + math.sin(T * 40) * .04 * u, .1 * u, u * .3, u * .4, 10), wash=INK, ink=None)
    elif e == 'blank':
        paint(ellPts(0, 0, u * .8, u * 1.05, 14), wash=PAL['cream'], ink=INK, sw=sw * .7)
    elif e == 'spark':
        paint(ellPts(0, 0, u * 1.5, u * 1.5, 18), fill=PAL['ochre'], fillOp=90, bleed=.3, ink=None)
        paint(starPts(0, 0, u * 1.35 * (1 + .12 * math.sin(T * 14))), wash=PAL['cream'], fill=PAL['ochre'], fillOp=80, ink=INK, sw=sw * .55)
    elif e == 'heart':
        paint(heartPts(0, .1 * u, u * .9 * (1 + .1 * pulse(T))), wash='#E2476E', ink=INK, sw=sw * .5)
    elif e == 'x':
        lineEye([[-.8, -.8], [.8, .8]], 1, 0)
        lineEye([[.8, -.8], [-.8, .8]], 1, 0)
    elif e == 'swirl':
        sp = []
        for k in range(16):
            a = k * .7 + T * 6 * s
            r = k * .06 * u
            sp.append([math.cos(a) * r, math.sin(a) * r])
        inkLine(sp, sw * .6, INK, 'inkfine', .6)
    elif e == 'dot':
        paint(ellPts(lx * .5, ly * .5, u * .45, u * .55, 12), wash=INK, ink=None)
    else:
        slit(1, 2)


def mouth(u, m, sw):
    if not m:
        return
    T = G.T
    P = lambda pts: [[a * u, b * u] for a, b in pts]
    dark = '#4A1F2A'

    def line(pts, w=.8, c=.6):
        inkLine(P(pts), sw * w, INK, 'ink', c)
    if m == 'o':
        paint(ellPts(0, -4.3 * u, u * .45, u * .5, 12), wash=INK, ink=None)
    elif m == 'O':
        paint(ellPts(0, -4.1 * u, u * .8, u * .95, 14), wash=dark, ink=INK, sw=sw * .6)
    elif m == 'smile':
        line([[-.8, -4.6], [0, -4.1], [.8, -4.6]])
    elif m == 'frown':
        line([[-.8, -4.1], [0, -4.6], [.8, -4.1]])
    elif m == 'grin':
        paint(P([[-1.3, -4.8], [1.3, -4.8], [.9, -3.9], [-.9, -3.9]]), wash=dark, ink=INK, sw=sw * .6, curv=.3)
    elif m == 'flat':
        line([[-.7, -4.4], [.7, -4.4]], .8, 0)
    elif m == 'wobble':
        line([[-1, -4.4], [-.5, -4.7], [0, -4.4], [.5, -4.7], [1, -4.4]], .7, .3)
    elif m == 'cat':
        line([[-.9, -4.5], [-.45, -4.1], [0, -4.5], [.45, -4.1], [.9, -4.5]], .7, .5)
    elif m == 'smirk':
        line([[-.8, -4.35], [.2, -4.3], [.9, -4.75]], .8, .5)
    elif m == 'laugh':
        paint(P([[-1.4, -4.9], [1.4, -4.9], [1, -4], [0, -3.4], [-1, -4]]), wash=dark, ink=INK, sw=sw * .6, curv=.4)
        paint(ellPts(0, -3.85 * u, .7 * u, .32 * u, 12), wash=PAL['rose'], ink=None)
    elif m == 'open':
        paint(ellPts(0, -4.25 * u, u * .75, u * .6, 14), wash=dark, ink=INK, sw=sw * .6)
        paint(ellPts(0, -3.95 * u, u * .45, u * .2, 10), wash=PAL['rose'], ink=None)
    elif m == 'wail':
        w = math.sin(T * 30) * .06
        paint(P([[-1.5, -4.5 + w], [-.5, -4.9], [.5, -4.9 - w], [1.5, -4.5], [1.2, -3.3], [-1.2, -3.3]]), wash=dark, ink=INK, sw=sw * .6, curv=.3)
        paint(ellPts(0, -3.6 * u, .8 * u, .25 * u, 12), wash=PAL['rose'], ink=None)
    elif m == 'teeth':
        paint(rectPts(-1.3 * u, -4.85 * u, 2.6 * u, .95 * u, u * .04), wash=PAL['cream'], ink=INK, sw=sw * .6)
        line([[-1.25, -4.38], [1.25, -4.38]], .4, 0)
    elif m == 'tongue':
        paint(P([[.05, -4.3], [.75, -4.3], [.72, -3.75], [.4, -3.55], [.08, -3.75]]), wash=PAL['rose'], ink=INK, sw=sw * .5, curv=.5)
        line([[-.8, -4.6], [0, -4.2], [.8, -4.5]])
    elif m == 'pout':
        line([[-.45, -4.2], [0, -4.5], [.45, -4.2]], 1, .6)
    elif m == 'yawn':
        paint(ellPts(0, -4.1 * u, u * .6, u * 1.05, 14), wash=dark, ink=INK, sw=sw * .6)


def flowerAt(fx, fy, u, sw, k=1.0):
    inkLine([[fx, fy], [fx + .3 * u, fy + .7 * u]], sw * .6, PAL['sap'], 'ink', 0)
    for i in range(5):
        a = i / 5 * TAU + .3
        paint(ellPts(fx + math.cos(a) * .7 * u * k, fy + math.sin(a) * .7 * u * k, .55 * u * k, .55 * u * k, 10), wash=PAL['cream'], ink=INK, sw=sw * .4)
    paint(ellPts(fx, fy, .45 * u * k, .45 * u * k, 10), wash=PAL['ochre'], ink=INK, sw=sw * .4)


def hat(u, h, sw, o=None):
    if not h:
        return
    P = lambda pts: [[a * u, b * u] for a, b in pts]
    if h == 'party':
        paint(P([[-1.8, -7.9], [0, -12.8], [1.8, -7.9]]), wash=PAL['rose'], fill=PAL['violet'], fillOp=50, ink=INK, sw=sw * .8)
        for i in range(3):
            inkLine(P([[-1.3 + i * .25, -8.8 - i * 1.2], [1.1 - i * .3, -9.6 - i * 1.2]]), sw * .6, PAL['ochre'], 'ink', 0)
        paint(ellPts(0, -12.8 * u, u * .75, u * .75, 12), wash=PAL['ochre'], ink=INK, sw=sw * .6)
    elif h == 'crown':
        paint(P([[-3, -7.9], [-3, -10.8], [-1.5, -9.3], [0, -11.2], [1.5, -9.3], [3, -10.8], [3, -7.9]]), wash='#F2C53D', fill=PAL['ochre'], fillOp=90, ink=INK, sw=sw * .8)
        for gx in (-1.5, 0, 1.5):
            paint(ellPts(gx * u, -8.7 * u, u * .3, u * .3, 8), wash=PAL['teal'] if gx else PAL['rose'], ink=None)
    elif h in ('wizard', 'hood'):
        paint(P([[-3.9, -7.9], [.9, -15], [3.9, -7.9]]), wash=PAL['violet'] if h == 'hood' else PAL['indigo'], fill=PAL['violet'], fillOp=80, ink=INK, sw=sw * .8)
        paint(starPts(.2 * u, -10.6 * u, u * .9, .4, 5), wash=PAL['ochre'], ink=None)
    elif h == 'top':
        paint(rectPts(-2.6 * u, -12.5 * u, 5.2 * u, 4.3 * u), wash=INK, ink=None)
        paint(rectPts(-2.6 * u, -9.4 * u, 5.2 * u, .8 * u), wash='#C8324A', ink=None)
        paint(rectPts(-3.9 * u, -8.6 * u, 7.8 * u, .8 * u), wash=INK, ink=None)
    elif h == 'beanie':
        d = []
        for i in range(13):
            a = math.pi + i / 12 * math.pi
            d.append([math.cos(a) * 3.9 * u, -8.4 * u + math.sin(a) * 2.6 * u])
        paint(d, wash=PAL['teal'], fill=PAL['sky'], fillOp=60, ink=INK, sw=sw * .8)
        paint(rectPts(-4.2 * u, -8.9 * u, 8.4 * u, 1.1 * u), wash=mixCol(PAL['teal'], INK, .2), ink=INK, sw=sw * .7)
        paint(ellPts(0, -11.2 * u, .8 * u, .8 * u, 12), wash=PAL['cream'], ink=INK, sw=sw * .6)
    elif h == 'bow':
        for s in (-1, 1):
            paint(P([[2.6, -8.1], [2.6 + s * 1.7, -9.3], [2.6 + s * 1.7, -7.1]]), wash=PAL['rose'], fill='#E2476E', fillOp=70, ink=INK, sw=sw * .6, curv=.3)
        paint(ellPts(2.6 * u, -8.2 * u, .45 * u, .45 * u, 10), wash='#E2476E', ink=INK, sw=sw * .5)
    elif h == 'flower':
        flowerAt(-2.6 * u, -8.6 * u, u, sw)
    elif h == 'headphones':
        inkLine(P([[-5.1, -5.8], [-4.6, -9.4], [0, -10.6], [4.6, -9.4], [5.1, -5.8]]), sw * 2.4, INK, 'ink', .6)
        for s in (-1, 1):
            paint(rrPts((-6.1 if s < 0 else 4.6) * u, -7.4 * u, 1.5 * u, 2.8 * u, .6 * u), wash=PAL['violet'], fill=PAL['rose'], fillOp=50, ink=INK, sw=sw * .7)
    elif h == 'cat':
        for s in (-1, 1):
            paint([[s * 4.9 * u, -7.9 * u], [s * 4.3 * u, -11 * u], [s * 1.9 * u, -7.9 * u]], wash=(o or {}).get('col') or PAL['clay'], ink=INK, sw=sw * .8)
            paint([[s * 4.2 * u, -8.1 * u], [s * 4 * u, -10 * u], [s * 2.8 * u, -8.1 * u]], wash=PAL['rose'], ink=None)
    elif h == 'deer':
        # detective deerstalker: a check-pattern dome with a front peak and ear flaps tied on top
        dome = []
        for i in range(15):
            a = math.pi + i / 14 * math.pi
            dome.append([math.cos(a) * 4.3 * u, -7.7 * u + math.sin(a) * 3.0 * u])
        base_ = '#C9A06A'
        paint(dome, wash=base_, ink=None)
        for k in range(-3, 4):
            inkLine(P([[k * 1.15, -7.8], [k * 1.0, -10.4 + abs(k) * .3]]), sw * .45, '#8E6A3E', 'inkfine', .3)
        for k in range(3):
            yy = -8.5 - k * .85
            ww = 4.1 - k * .7
            inkLine(P([[-ww, yy], [0, yy - .15], [ww, yy]]), sw * .45, '#8E6A3E', 'inkfine', .5)
        paint(dome, ink=INK, sw=sw * .8)
        paint(P([[2.8, -8.0], [6.0, -7.4], [5.6, -6.9], [2.6, -7.3]]), wash=mixCol(base_, INK, .18), ink=INK, sw=sw * .7, curv=.2)
        paint(P([[-2.8, -8.0], [-5.6, -7.6], [-5.3, -7.1], [-2.6, -7.3]]), wash=mixCol(base_, INK, .25), ink=INK, sw=sw * .7, curv=.2)
        paint(ellPts(0, -10.75 * u, .5 * u, .5 * u, 10), wash='#8E6A3E', ink=INK, sw=sw * .5)
        flowerAt(-2.2 * u, -9.3 * u, u, sw, .9)
    elif h == 'chef':
        paint(rectPts(-3 * u, -9.6 * u, 6 * u, 1.8 * u), wash='#FFFFFF', ink=INK, sw=sw * .7)
        cl = []
        for i in range(30):
            a = math.pi + i / 29 * math.pi
            r = 1 + .12 * abs(math.sin(a * 4))
            cl.append([math.cos(a) * 3.6 * u * r, -10.2 * u + math.sin(a) * 2.8 * u * r])
        paint(cl, wash='#FFFFFF', ink=INK, sw=sw * .7)
    elif h == 'pirate':
        paint(P([[-4.6, -8.0], [-3.2, -10.6], [0, -11.4], [3.2, -10.6], [4.6, -8.0], [0, -8.6]]), wash=INK, ink=INK, sw=sw * .7, curv=.2)
        paint(ellPts(0, -9.7 * u, .7 * u, .55 * u, 10), wash=PAL['cream'], ink=None)
    elif h == 'antlers':
        for s in (-1, 1):
            inkLine(P([[s * 2, -8], [s * 2.6, -10.5], [s * 3.8, -12]]), sw * 1.4, '#8E6A3E', 'ink', .4)
            inkLine(P([[s * 2.5, -10.0], [s * 1.3, -11.4]]), sw * 1.2, '#8E6A3E', 'ink', 0)
            inkLine(P([[s * 3.1, -11.1], [s * 4.6, -11.0]]), sw * 1.1, '#8E6A3E', 'ink', 0)


EMOTE_TOP = ['steam', 'stars', 'cloud', 'bulb', 'scribble']


def emote(kind, x, y, s, k=1, age=None):
    if age is None:
        age = G.T
    p = backOut(k)
    if p < .02:
        return
    sw = clamp(s / 15, .4, 2)
    P = lambda pts: [[a * s, b * s] for a, b in pts]

    def dot(dx, col):
        paint(ellPts(dx, 1.25 * s, .42 * s, .42 * s, 12), wash=col, ink=INK, sw=sw * .7)

    def bang(dx, col):
        push()
        translate(dx, 0)
        rotate(.1 + .08 * math.sin(age * 16) * math.exp(-age * 3))
        paint(P([[-.62, -2.3], [.62, -2.3], [.22, .45], [-.22, .45]]), wash=col, fill=PAL['cream'], fillOp=70, ink=INK, sw=sw * .8, curv=.25)
        dot(0, col)
        pop()

    def quest(dx, col):
        push()
        translate(dx, 0)
        rotate(-.08 + .08 * math.sin(age * 12) * math.exp(-age * 3))
        paint(ribbon(P([[-1, -1.3], [-.55, -2.15], [.35, -2.3], [1, -1.6], [.7, -.75], [.05, -.3], [0, .4]]), .75 * s, .5 * s), wash=col, ink=INK, sw=sw * .8)
        dot(0, col)
        pop()
    push()
    translate(x, y)
    scale(p)
    if kind == '!':
        bang(0, PAL['ochre'])
    elif kind == '?':
        quest(0, PAL['sky'])
    elif kind == '??':
        quest(-.9 * s, PAL['sky'])
        quest(1.0 * s, '#B79BE0')
    elif kind == '!!':
        bang(-.8 * s, PAL['ochre'])
        bang(.9 * s, PAL['ochre'])
    elif kind == '!?':
        bang(-.9 * s, PAL['ochre'])
        quest(1 * s, PAL['sky'])
    elif kind == 'sweat':
        for dx, dy, r in [[0, 0, 1], [1.6, 1.4, .7]]:
            paint(P([[dx, dy - 1.6 * r], [dx + .9 * r, dy + .2], [dx, dy + .9 * r], [dx - .9 * r, dy + .2]]), wash=PAL['sky'], ink=INK, sw=sw * .6, curv=.7)
    elif kind == 'spark':
        tw = 1 + .15 * math.sin(age * 12)
        paint(starPts(0, 0, 1.6 * s * tw), wash=PAL['cream'], fill=PAL['ochre'], fillOp=80, ink=INK, sw=sw * .5)
        paint(starPts(1.9 * s, 1.2 * s, .8 * s / tw), wash=PAL['ochre'], ink=INK, sw=sw * .4)
    elif kind == 'heart':
        paint(heartPts(0, 0, s * 1.8 * (1 + .12 * pulse(G.T))), wash='#E2476E', fill=PAL['rose'], fillOp=90, ink=INK, sw=sw * .6)
    elif kind == 'hearts':
        for i in range(3):
            ph = frac(age * .55 + i / 3)
            a = math.sin(ph * math.pi)
            if a < .1:
                continue
            paint(heartPts((math.sin(ph * 6 + i * 2) * .7 + i * .7 - .7) * s, -ph * 3.8 * s, s * (.5 + .6 * a)), wash='#E2476E', ink=INK, sw=sw * .5)
    elif kind == 'anger':
        b = 1 + .15 * pulse(G.T, 8)
        for i in range(4):
            push()
            rotate(i * math.pi / 2 + math.pi / 4)
            scale(b)
            inkLine(P([[2.1 + 1.3 * math.cos(d * math.pi / 180), 1.3 * math.sin(d * math.pi / 180)] for d in (140, 160, 180, 200, 220)]), sw * 1.1, '#D8394E', 'ink', .6)
            pop()
    elif kind == 'dots':
        for i in range(3):
            ph = frac(age / 1.8)
            q = backOut(clamp((ph - i * .22) * 6))
            if q < .02:
                continue
            paint(ellPts((i - 1) * 1.3 * s, 0, .42 * s * q, .42 * s * q, 10), wash=INK, ink=None)
    elif kind == 'music':
        b = math.sin(age * 5) * .3 * s
        push()
        translate(0, b)
        rotate(.1 * math.sin(age * 5))
        paint(ellPts(0, 1.2 * s, .7 * s, .5 * s, 12, 0, -.3), wash=INK, ink=None)
        inkLine(P([[.6, 1.1], [.6, -1.6], [1.6, -1]]), sw * .8, INK, 'ink', 0)
        pop()
    elif kind == 'stars':
        for i in range(3):
            a = age * 5 + i * TAU / 3
            d = .75 + .25 * math.sin(a)
            paint(starPts(math.cos(a) * 4.2 * s, math.sin(a) * s, .75 * s * d, .45, 5, age * 3), wash=PAL['ochre'], ink=INK, sw=sw * .5)
    elif kind == 'cloud':
        bob = math.sin(age * 2) * .15 * s
        c = []
        for i in range(40):
            a = i / 40 * TAU
            up = math.sin(a) < 0
            r = 1 + .38 * abs(math.sin(a * 3)) ** .6 if up else 1
            c.append([math.cos(a) * 2.8 * s * (r * .92 if up else 1), bob - .2 * s + math.sin(a) * (1.35 if up else .7) * s * r])
        for i in range(6):
            ph = frac(age * 2.4 + hash1(i))
            rx, ry = (-2 + i * .8) * s, (.7 + ph * 2) * s
            inkLine([[rx, ry], [rx - .12 * s, ry + .7 * s]], sw * 1.1, mixCol(PAL['sky'], PAL['indigo'], .3), 'ink', 0)
        paint(c, wash='#A3A8C4', fill=PAL['indigo'], fillOp=70, bleed=.1, ink=INK, sw=sw * .8, curv=.4)
    elif kind == 'bulb':
        gl = .5 + .5 * math.sin(age * 10)
        glow(0, -1.4 * s, 4.5 * s, '#FFD27A', .75 + .25 * gl)
        paint(ellPts(0, -1.4 * s, 1.15 * s, 1.2 * s, 16), wash='#FFE68A', ink=INK, sw=sw * .7)
        paint(rectPts(-.5 * s, -.3 * s, s, .8 * s), wash='#9A93A8', ink=INK, sw=sw * .6)
    pop()


def _b(t):
    bp = bpOf(t)
    s1 = math.sin(bp * math.pi)
    return dict(bp=bp, s1=s1, ab=abs(s1), hit=pulse(t), s2=math.sin(bp * TAU), f=frac(bp))


def _e(eyes=None, mouth=None, **kw):
    d = dict(eyes=eyes, mouth=mouth)
    d.update(kw)
    return d


EMO = {
    'neutral': _e('normal', None, take=.3, body=lambda t, b: dict(dy=-.25 * b['ab'], sq=.03 * b['hit'], aL=.15 + .05 * b['s1'], aR=.15 - .05 * b['s1'])),
    'happy': _e('happy', 'smile', blush=.3, take=.6, body=lambda t, b: dict(dy=-1.2 * b['ab'], sq=.1 * b['hit'], aL=.4 + .4 * b['s1'], aR=.4 - .4 * b['s1'])),
    'excited': _e('wide', 'open', emote='spark', take=1, body=lambda t, b: dict(dy=-2.4 * abs(b['s2']), sq=.16 * pulse2(t) - .06 * abs(b['s2']), aL=1 + .5 * math.sin(b['bp'] * TAU * 2), aR=1 - .5 * math.sin(b['bp'] * TAU * 2))),
    'laugh': _e('squeeze', 'laugh', blush=.45, take=.8, body=lambda t, b: (lambda c: dict(dy=-.45 * c, sq=.08 * c - .04, rot=-.07 + .03 * math.sin(t * TAU * 5), aL=-.35 + .12 * c, aR=-.35 + .12 * c))(abs(math.sin(t * TAU * 5)))),
    'love': _e('heart', 'cat', blush=.8, tint='rosy', tintK=.5, emote='hearts', take=.7, body=lambda t, b: (lambda s: dict(rot=.08 * s, dx=.5 * s, dy=-.6 * b['ab'], sq=.05 * b['hit'], aL=-.1 + .15 * b['s1'], aR=-.1 - .15 * b['s1']))(math.sin(b['bp'] * math.pi / 2))),
    'shy': _e('look', 'wobble', blush=1, take=.3, body=lambda t, b: (lambda s: dict(lookX=-.7, lookY=.8, sq=.06, rot=-.05 + .02 * s, dx=.15 * s, aL=-.55 + .15 * math.sin(t * TAU * 1.5), aR=-.6 - .12 * math.sin(t * TAU * 1.5)))(math.sin(b['bp'] * math.pi / 2))),
    'proud': _e('closed', 'smile', tint='gold', tintK=.3, emote='spark', take=.5, body=lambda t, b: dict(sq=-.1 - .03 * b['ab'], dy=-.3 * b['hit'], aL=-.9, aR=-.9, rot=.02 * b['s1'])),
    'smug': _e('narrow', 'smirk', take=.4, body=lambda t, b: (lambda s: dict(lookX=.4, rot=-.06 + .03 * s, dy=-.2 * b['ab'], aL=-.5, aR=.5 + .15 * s))(math.sin(b['bp'] * math.pi / 2))),
    'relieved': _e('closed', 'smile', emote='sweat', take=.4, body=lambda t, b: (lambda br: dict(sq=.05 + .05 * br, dy=-.15 * b['ab'], aL=-.7 + .1 * br, aR=-.7 + .1 * br))(math.sin(t * TAU * .35))),
    'sad': _e('sad', 'frown', tint='blue', tintK=.35, gloom=.35, take=.3, body=lambda t, b: (lambda s: dict(sq=.08 + .02 * s, rot=.03 * s, aL=-.75, aR=-.75, lookY=.5))(math.sin(b['bp'] * math.pi / 4))),
    'cry': _e('cry', 'wail', tint='blue', tintK=.2, take=.8, body=lambda t, b: (lambda sob: dict(sq=.14 * sob - .02, dy=-.7 * sob, aL=.9 + .15 * math.sin(t * TAU * 6), aR=.9 - .15 * math.sin(t * TAU * 6), rot=.03 * b['s1']))(math.sin(b['f'] * math.pi) * math.exp(-b['f'] * 2))),
    'angry': _e('angry', 'teeth', tint='flush', tintK=.45, emote='anger', take=.8, body=lambda t, b: dict(dx=.1 * math.sin(t * TAU * 18), sq=.12 * b['hit'], aL=-.3 + .1 * b['hit'], aR=-.3 + .1 * b['hit'])),
    'scared': _e('scared', 'wobble', tint='pale', tintK=.6, emote='sweat', take=1.1, body=lambda t, b: dict(dx=.1 * math.sin(t * TAU * 22), sq=-.06, aL=1 + .08 * math.sin(t * TAU * 17), aR=1 + .08 * math.sin(t * TAU * 19), lookX=.6 * (1 if math.sin(t * 2.3) >= 0 else -1))),
    'surprised': _e('wide', 'O', emote='!', fade=True, take=1.3, body=lambda t, b: dict(sq=-.12, dy=-.3 - .15 * b['ab'], aL=1.1 + .05 * b['s2'], aR=1.1 - .05 * b['s2'])),
    'confused': _e(['narrow', 'wide'], 'wobble', emote='?', take=.6, body=lambda t, b: dict(rot=.1 * math.sin(b['bp'] * math.pi / 4), aL=.1, aR=1.5 + .15 * math.sin(t * TAU * 3), dy=-.15 * b['ab'])),
    'thinking': _e('look', 'flat', emote='dots', take=.4, body=lambda t, b: dict(lookX=.5, lookY=-.8, rot=.05, aR=.9, aL=-.3 + .25 * math.sin(b['f'] * math.pi), dy=-.1 * b['ab'])),
    'idea': _e('shine', 'grin', emote='bulb', take=1.1, body=lambda t, b: dict(dy=-1 * b['ab'], sq=-.05 + .1 * b['hit'], aR=1.55 + .1 * b['s2'], aL=.2 + .2 * b['s1'])),
    'determined': _e('determined', 'flat', take=.7, body=lambda t, b: dict(rot=.06, sq=-.04 + .06 * b['hit'], dy=-.3 * b['ab'], aL=.1 + .7 * math.sin(b['f'] * math.pi), aR=.1 + .7 * abs(math.cos(b['f'] * math.pi)))),
    'nervous': _e('look', 'wobble', tint='pale', tintK=.2, emote='sweat', take=.5, body=lambda t, b: dict(lookX=.8 if beatN(t) % 2 else -.8, dx=.3 * b['s1'], sq=.04, aL=-.1 + .2 * math.sin(t * TAU * 5), aR=-.1 + .2 * math.sin(t * TAU * 5 + 1))),
    'suspicious': _e('narrow', 'flat', take=.4, body=lambda t, b: (lambda s: dict(lookX=s, rot=-.08 * s, dx=.4 * s, sq=.04, aL=-.4, aR=-.4))(math.sin(t * TAU * .25))),
    'dizzy': _e('swirl', 'wobble', emote='stars', take=.7, body=lambda t, b: (lambda a: dict(rot=.12 * math.sin(a), dx=.7 * math.sin(a), dy=-.3 * abs(math.cos(a)), aL=.3 + .6 * math.sin(a * 1.3), aR=.3 - .6 * math.sin(a * 1.3)))(t * TAU * .8)),
    'cool': _e('shades', 'smirk', emote='music', take=.4, body=lambda t, b: dict(rot=.04 * b['hit'], dy=-.35 * b['hit'], sq=.06 * b['hit'], aL=-.4, aR=.7 + .1 * b['s1'])),
    'starstruck': _e('spark', 'open', tint='gold', tintK=.3, take=1, body=lambda t, b: dict(dy=-1.6 * abs(b['s2']), sq=.1 * pulse2(t), aL=1.1 + .35 * math.sin(b['bp'] * TAU * 2), aR=1.1 + .35 * math.sin(b['bp'] * TAU * 2))),
    'ko': _e('x', 'wobble', tint='pale', tintK=.3, emote='stars', take=1, body=lambda t, b: dict(sq=.28 + .02 * math.sin(t * 3), rot=.12, aL=-1, aR=-.9)),
    'playful': _e('wink', 'tongue', take=.6, body=lambda t, b: (lambda k: dict(dx=.8 * k, dy=-1.4 * b['ab'], rot=.1 * k, sq=.1 * b['hit'], aL=.65 + .55 * k, aR=.65 - .55 * k))(lerp(-(1 if beatN(t) % 2 else -1), (1 if beatN(t) % 2 else -1), easeOut(clamp(b['f'] * 3))))),
    'hopeful': _e('shine', 'cat', blush=.35, take=.5, body=lambda t, b: dict(sq=-.06 - .02 * b['ab'], dy=-.25 * b['ab'], lookY=-.4, aL=.5 + .05 * b['s1'], aR=.5 - .05 * b['s1'], rot=.03 * math.sin(b['bp'] * math.pi / 2))),
}


def feel(name, t, over=None):
    E = EMO.get(name, EMO['neutral'])
    d = dict(eyes=E['eyes'], mouth=E['mouth'], tint=E.get('tint'), tintK=E.get('tintK', 1), blush=E.get('blush', 0),
             gloom=E.get('gloom', 0), emote=E.get('emote'))
    if E.get('body'):
        d.update(E['body'](t, _b(t)))
    if over:
        d.update(over)
    return d


def emotions(t, keys, o=None):
    o = o or {}
    i = 0
    while i + 1 < len(keys) and t >= keys[i + 1][0]:
        i += 1
    tc, name = keys[i][0], keys[i][1]
    over = keys[i][2] if len(keys[i]) > 2 else None
    age = t - tc
    cur = feel(name, t, over)
    tn = keys[i + 1][0] if i + 1 < len(keys) else 1e9
    tkS = o.get('take', 1)
    E = EMO.get(name, EMO['neutral'])
    squint = cur.get('squint', 0) or 0
    if tn - t < .1:
        squint = max(squint, 1 - (tn - t) / .1)
    if i > 0 and age < .14:
        squint = max(squint, 1 - age / .14)
    prev = feel(keys[i - 1][1], t, keys[i - 1][2] if len(keys[i - 1]) > 2 else None) if i > 0 else None
    for d_ in (prev, cur):
        if d_ is not None:
            for kk in ('col', 'dk', 'lt'):
                if o.get(kk) and not d_.get(kk):
                    d_[kk] = o[kk]
    if prev and age < .5:
        base = dict(dy=0, sq=0, aL=.2, aR=.2, rot=0, dx=0, lookX=0, lookY=0)
        k = backOut(seg(age, 0, .4))
        kc = ease(seg(age, 0, .3))
        for f in base:
            pv = prev.get(f)
            cv = cur.get(f)
            cur[f] = lerp(base[f] if pv is None else pv, base[f] if cv is None else cv, k)
        a, b = tintCols(prev), tintCols(cur)
        cur['col'] = mixCol(a['col'], b['col'], kc)
        cur['dk'] = mixCol(a['dk'], b['dk'], kc)
        cur['lt'] = mixCol(a['lt'], b['lt'], kc)
        cur['tint'] = None
        for f in ('blush', 'gloom'):
            cur[f] = lerp(prev.get(f) or 0, cur.get(f) or 0, kc)
    t1 = take(t, tc, E.get('take', .6) * tkS) if prev else dict(sq=0, dy=0)
    En = EMO.get(keys[i + 1][1], EMO['neutral']) if i + 1 < len(keys) else None
    t2 = take(t, tn, En.get('take', .6) * tkS) if En else dict(sq=0, dy=0)
    cur['sq'] = (cur.get('sq') or 0) + t1['sq'] + t2['sq']
    cur['dy'] = (cur.get('dy') or 0) + t1['dy'] + t2['dy']
    cur['squint'] = squint
    same = prev and prev.get('emote') == cur.get('emote')
    cur['emoteK'] = 1 if same else seg(age, .06, .32) * ((1 - seg(age, 1.4, 1.8)) if (E.get('fade') and not (over and over.get('emote'))) else 1)
    cur['emoteAge'] = age
    return cur


def move(style, t, seed=0):
    bp = bpOf(t)
    bi = math.floor(bp)
    bf = bp - bi
    hit = max(0, 1 - bf * 3.5)
    s1 = math.sin(bp * math.pi)
    ab = abs(s1)
    o = dict(dy=0, sq=0, aL=.2, aR=.2, rot=0, dx=0)
    if style == 'bounce':
        o.update(dy=-ab * 1.6, sq=hit * .12, aL=.4 + s1, aR=.4 - s1)
    elif style == 'hop':
        o.update(dy=-ab * 4, sq=hit * .18, aL=.3 + ab * 1.1, aR=.3 + ab * 1.1)
    elif style == 'roof':
        o.update(dy=-ab * 1.2, sq=hit * .1, aL=1.25 + .3 * math.sin(bp * TAU), aR=1.25 + .3 * math.sin(bp * TAU))
    elif style == 'sway':
        o.update(dx=s1 * 3, rot=s1 * .12, aL=.5 + .6 * s1, aR=.5 - .6 * s1, sq=hit * .08)
    elif style == 'wave':
        o.update(dy=-ab, aL=1.1 + .5 * math.sin(bp * TAU * 2), aR=-.2, sq=hit * .08)
    elif style == 'walk':
        o.update(walk=bp / 2, dy=-ab * .6, aL=.3 * s1, aR=-.3 * s1)
    elif style == 'run':
        o.update(walk=bp * 1.5, dy=-abs(math.sin(bp * TAU)), aL=.8 * math.sin(bp * TAU * 1.5), aR=-.8 * math.sin(bp * TAU * 1.5), rot=-.08)
    elif style == 'idle':
        o.update(dy=-ab * .5, sq=hit * .05)
    elif style == 'stomp':
        o.update(dy=-max(0, math.sin(bp * TAU)) * 1.4, sq=hit * .2, rot=(1 if bi % 2 else -1) * .06 * hit, aL=-.3 + hit * .9, aR=-.3 + hit * .9)
    elif style == 'shimmy':
        o.update(dx=math.sin(bp * TAU * 2) * .6, rot=math.sin(bp * TAU * 2) * .05, aL=.9 + .4 * math.sin(bp * TAU * 2), aR=.9 - .4 * math.sin(bp * TAU * 2), dy=-ab * .5)
    return o


# the cast: him (Clawd, clay orange) and her (rosy Clawd with a white flower on her head)
ME = dict(col=PAL['clay'], dk=PAL['clayDk'], lt='#F5B394')
HER = dict(col='#EE9AAE', dk='#C0637B', lt='#FBD0DA')


def him(x, y, u, o=None):
    o = dict(o or {})
    for k, v in ME.items():
        o.setdefault(k, v)
    o.setdefault('boilKey', 'him')
    clawd(x, y, u, o)


def her(x, y, u, o=None, detective=False):
    o = dict(o or {})
    for k, v in HER.items():
        o.setdefault(k, v)
    o.setdefault('boilKey', 'her')
    if 'hat' not in o:
        o['hat'] = 'deer' if detective else 'flower'
    clawd(x, y, u, o)
