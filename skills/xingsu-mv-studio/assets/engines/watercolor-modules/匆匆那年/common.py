# common.py: time helpers for 《匆匆那年》. Times are clip seconds (audio cut at S0 = 6997 samples). B[k] = tracked beat k
# (128 BPM eighth-note level; the felt pulse is ~64 BPM = every other k, a bar = 8 k, bar lines at K4, K12, ... K60 = voice).
# No beat grid: shots follow sections and lyric lines; B is used for the section hits only.
import json, os, math, bisect
from eng import *
from clawd import VIEWS

HERE = os.path.dirname(os.path.abspath(__file__))
SB = json.load(open(os.path.join(HERE, '..', 'data', 'storyboard.json'), encoding='utf-8'))
B = SB['beats']
DUR = SB['dur']
RING = SB['ring']
G.BEATS = B[0::2]          # character idle sway follows the felt ~64 BPM pulse (K4 is a bar line, even k = felt beats)
LY = json.load(open(os.path.join(HERE, '..', 'data', 'lyrics.json'), encoding='utf-8'))
SHOT = {s['id']: s for s in SB['shots']}


def Ls(i):
    """first syllable of lyric line i"""
    return LY[i][0]


def Lc(i, j):
    """time of the j-th (non-space) character of lyric line i"""
    return LY[i][3][j]


def beatIdx(t):
    return bisect.bisect_right(B, t + 1e-6) - 1


def isDown(k):
    return (k - 4) % 8 == 0     # intro bar lines: K4 1.78, K12 5.50 (strings), K20, K28, K36 16.82 (bass), K44, K52, K60 28.19 (voice)


def cam(t, cx=W / 2, cy=H / 2, z=1.0, rot=0.0):
    camBegin(cx, cy, z, rot)


def shotT(sid):
    s = SHOT[sid]
    return s['start'], s['end']


def lt01(t, sid):
    """0..1 progress through shot sid"""
    a, b = shotT(sid)
    return clamp((t - a) / (b - a))


def es(t, a, b):
    return ease(seg(t, a, b))


def bt(k):
    """beat index (int) -> time; a float is already a time"""
    return B[k] if isinstance(k, int) else float(k)


def pk(t, k, d=.16, lead=.04):
    """0..1 progress of something that pops at k (int beat index or float time), starting ~1 frame early"""
    a = bt(k) - lead
    return 0.0 if t < a else clamp((t - a) / d)


def after(t, k, lead=.04):
    return t >= bt(k) - lead


def age(t, k):
    return t - bt(k)


def kt(x):
    i = int(math.floor(x))
    if i >= len(B) - 1:
        return B[-1] + (x - (len(B) - 1)) * (B[-1] - B[-2])
    return B[i] + (x - i) * (B[i + 1] - B[i])


def bump(t):
    return 0.0


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
