# common.py: beat helpers for 《你瞒我瞒》. Times are clip seconds; B[k] = measured 152-grid beat k.
# The song moves at 76 BPM: a felt beat = every even k, bar n (1-based) starts at k = 4 + 8 (n - 1); k0..k4 is the pickup bar.
import json, os, math, bisect
from eng import *
from clawd import VIEWS

HERE = os.path.dirname(os.path.abspath(__file__))
SB = json.load(open(os.path.join(HERE, '..', 'data', 'storyboard.json'), encoding='utf-8'))
B = SB['beats']
DUR = SB['dur']
BRK = SB['breakdown']
G.BEATS = B[0::2]          # character bounce follows the 76 BPM felt beat
LY = json.load(open(os.path.join(HERE, '..', 'data', 'lyrics.json'), encoding='utf-8'))
SHOT = {s['id']: s for s in SB['shots']}


def beatIdx(t):
    return bisect.bisect_right(B, t + 1e-6) - 1


def isDown(k):
    return (k - 4) % 8 == 0


def isBeat(k):
    return k % 2 == 0


def KB(n, j=0):
    """k of bar n (1-based), felt beat j (0..3)"""
    return 4 + 8 * (n - 1) + 2 * j


def bump(t):
    """camera push on every beat: 2 % on the downbeat, 1.1 % otherwise, gone in ~0.09 s; softer in the kick-less breakdown"""
    k = beatIdx(t)
    if k < 0:
        return 0.0
    k -= k % 2                    # felt beats only (76 BPM)
    if k >= 125:                  # drums are out for the tail
        return 0.0
    a = t - B[k]
    amp = .02 if isDown(k) else .011
    if BRK[0] <= k < BRK[1]:
        amp *= .45
    return amp * math.exp(-a / .09)


def cam(t, cx=W / 2, cy=H / 2, z=1.0, rot=0.0):
    camBegin(cx, cy, z * (1 + bump(t)), rot)


def bt(k):
    return B[k] if isinstance(k, int) else float(k)


def pk(t, k, d=.16, lead=.04):
    """0..1 progress of something that pops on beat k (starts ~1 frame early so it lands on the beat)"""
    tb = bt(k) - lead
    return 0.0 if t < tb else clamp((t - tb) / d)


def after(t, k, lead=.04):
    return t >= bt(k) - lead


def age(t, k):
    return t - bt(k)


def sg(t, a, b):
    return seg(t, bt(a), bt(b))


def es(t, a, b):
    return ease(sg(t, a, b))


def kt(x):
    """time of a fractional beat index"""
    i = int(math.floor(x))
    if i >= len(B) - 1:
        return B[-1] + (x - (len(B) - 1)) * (B[-1] - B[-2])
    return B[i] + (x - i) * (B[i + 1] - B[i])


def steps(t, ks, vals, d=.14, lead=.04, e=None):
    """value that steps on each beat in ks (vals has len(ks)+1 entries), eased over d seconds"""
    e = e or easeOut
    v = vals[0]
    for i, k in enumerate(ks):
        tb = bt(k) - lead
        if t >= tb:
            v = lerp(vals[i], vals[i + 1], e(clamp((t - tb) / d)))
    return v


def lastBeat(t, ks, lead=.04):
    """index into ks of the last beat that has hit (-1 if none)"""
    j = -1
    for i, k in enumerate(ks):
        if t >= bt(k) - lead:
            j = i
    return j


def handXY(x, y, u, o, side='R'):
    """world position of a Clawd's hand (end of the arm), ignoring squash; matches clawd.arm()"""
    v = o.get('view') or 'front'
    V = VIEWS[v]
    spec = None
    for a in V['arms']:
        if a[2] == side:
            spec = a
    if spec is None:
        spec = V['arms'][0]
    px, dr, which, layer = spec
    a = o.get('aL', .2) if which == 'L' else o.get('aR', .2)
    if dr == 0:
        sx_, sy_ = px * u + 0, -4.5 * u + .3 * u
        ang = .7 - a
        lx, ly = sx_ + 2.1 * u * math.cos(ang), sy_ + 2.1 * u * math.sin(ang)
    else:
        sh = (px + dr * .55 * clamp((abs(a) - .7) / .9)) * u
        lx, ly = sh + dr * 2.2 * u * math.cos(a), -4.5 * u - 2.2 * u * math.sin(a)
    f = -1 if o.get('flip') else 1
    sx = o.get('sx', 1) or 1
    sy = o.get('sy', 1) or 1
    return x + (o.get('dx', 0) or 0) * u + f * sx * lx, y + (o.get('dy', 0) or 0) * u + sy * ly


def rubberStamp(txt, x, y, size, ag, col='#E0344E', rot=-.18, life=None):
    """an inked rubber stamp slammed onto the page; ag = seconds since it hit"""
    if ag < -.08:
        return
    k = clamp((ag + .08) / .08)
    sc = lerp(1.8, 1.0, easeIn(k)) if ag < 0 else 1 + .06 * math.exp(-ag * 12) * math.cos(ag * 40)
    a = clamp(k * 1.5) * (1 if life is None else 1 - seg(ag, life - .2, life))
    push()
    translate(x, y)
    rotate(rot)
    scale(sc)
    w = textW(txt, size) + size * .7
    h = size * 1.45
    boilSeed('stamp' + txt)
    pa = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=size * .09, Color=skcol(col, .92 * a))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2, -h / 2, w, h), size * .18, size * .18, pa)
    pa2 = skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=size * .03, Color=skcol(col, .7 * a))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + size * .14, -h / 2 + size * .14, w - size * .28, h - size * .28), size * .12, size * .12, pa2)
    text(txt, 0, 0, size, col, shadow=False, a=.92 * a)
    # ink speckle gaps (paper showing through)
    for i in range(16):
        px = (hash1(i * 3.7) - .5) * w * .9
        py = (hash1(i * 5.3) - .5) * h * .8
        G.c.drawCircle(px, py, size * (.015 + .03 * hash1(i)), skia.Paint(AntiAlias=True, Color=skcol('#F3EBDC', .55 * a)))
    pop()
