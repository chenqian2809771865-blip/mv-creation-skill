# render.py: Renderer().frame(t) -> BGRA (H, W, 4). 2560x1440 (MV_OUT), 24 fps. Frames sample the END of the frame interval.
# Lyrics: the track is instrumental, so no karaoke colouring. Each line is a torn paper strip taped into the picture;
# its words write on as the lead melody reaches them (2 frames early), Rolling in navy ink, 小苹果 in apple-red ink.
import math, bisect
from eng import *
import eng
from story import SHOTS
from story_d import outro
from common import LY, DUR
from props_chuanshao import apple

FPS = 24
STARTS = [s[0] for s in SHOTS]
LEAD = 2 / 24


def shotAt(t):
    return max(0, bisect.bisect_right(STARTS, t + 1e-9) - 1)


def drawShot(i, t):
    t0, fn, _, _ = SHOTS[i]
    dur = (SHOTS[i + 1][0] if i + 1 < len(SHOTS) else DUR) - t0
    G.CLAWD_N = 0
    G.c.save()
    fn(t, t - t0, dur)
    G.c.restore()


TR_LEAD = {'wipe': .14, 'iris': .13}


def wipePoly(k):
    x = lerp(-500, eng.W + 500, k)
    return [[-200, -200], [x + 250, -200], [x - 250, eng.H + 200], [-200, eng.H + 200]], (x + 250, -200, x - 250, eng.H + 200)


def composite(t):
    i = shotAt(t)
    t0, fn, tr, sid = SHOTS[i]
    # wipes and irises into the NEXT shot start before its downbeat and are done on the beat frame, so the beat-1 event is never hidden
    if i + 1 < len(SHOTS) and SHOTS[i + 1][2] in TR_LEAD and t > SHOTS[i + 1][0] - TR_LEAD[SHOTS[i + 1][2]]:
        i, (t0, fn, tr, sid) = i + 1, SHOTS[i + 1]
    c = G.c
    if tr == 'wipe' and t < t0 + .01 and i > 0:
        k = ease(seg(t, t0 - TR_LEAD['wipe'], t0 + .01))
        drawShot(i - 1, t)
        poly, edge = wipePoly(k)
        c.save()
        c.clipPath(eng._path(poly), skia.ClipOp.kIntersect, True)
        drawShot(i, t)
        c.restore()
        boilSeed('wipeedge')
        inkLine([[edge[0], edge[1]], [edge[2], edge[3]]], 3.0, INK, 'ink', 0)
        return
    if tr == 'iris' and t < t0 + .06 and i > 0:
        k = easeOut(seg(t, t0 - TR_LEAD['iris'], t0 + .06))
        drawShot(i - 1, t)
        r = lerp(10, 1300, k)
        circ = skia.Path()
        circ.addCircle(eng.W / 2, eng.H / 2, r)
        c.save()
        c.clipPath(circ, skia.ClipOp.kIntersect, True)
        drawShot(i, t)
        c.restore()
        boilSeed('irisedge')
        paint(ellPts(eng.W / 2, eng.H / 2, r, r, 48), ink=INK, sw=2.2)
        return
    if tr == 'pop' and t < t0 + .14:
        s = lerp(1.07, 1.0, easeOut(seg(t, t0, t0 + .14)))
        c.save()
        c.translate(eng.W / 2, eng.H / 2)
        c.scale(s, s)
        c.translate(-eng.W / 2, -eng.H / 2)
        drawShot(i, t)
        c.restore()
        return
    drawShot(i, t)
    if tr == 'flash' and t < t0 + .14:
        flash(1 - seg(t, t0 + 1 / 24, t0 + .14))


# ---------------------------------------------------------------- lyric strips
INKC = {'R': '#25306E', 'X': '#B02A40'}
TAPE = {'R': '#8FA6E8', 'X': '#F28FA0'}


def tornStrip(x0, y0, w, h, key):
    boilSeed(key)
    top, bot = [], []
    n = max(6, int(w / 38))
    for i in range(n + 1):
        x = x0 + w * i / n
        top.append([x, y0 + jit(3.5)])
        bot.append([x, y0 + h + jit(3.5)])
    return top + bot[::-1]


def strip(t, r, idx, st, en, cx, cy, size, rot, back=False):
    units, ut, song = r['units'], r['ut'], r['song']
    zh = song == 'X'
    gap = 2 if zh else size * .3
    f = skia.Font(typeface(KUAILE), size)
    ws = [f.measureText(u) for u in units]
    total = sum(ws) + gap * (len(units) - 1)
    lim = 1700 if not back else 1100
    sc = min(1.0, lim / total)
    pad = size * .9
    w = total * sc + pad * 2 + size * .9
    h = size * 1.55
    # unroll in, slide out
    kin = easeOut(clamp((t - st) / .1))
    kout = ease(clamp((t - (en - .14)) / .14)) if en < 1e8 else 0
    if kin <= 0 or kout >= 1:
        return
    push()
    translate(cx, cy + 40 * kout)
    rotate(rot)
    c = G.c
    c.save()
    c.clipRect(skia.Rect.MakeXYWH(-w / 2 - 40, -h, (w + 80) * kin, h * 2), skia.ClipOp.kIntersect, True)
    a = 1 - kout
    P = tornStrip(-w / 2, -h / 2, w, h, f'ly{idx}')
    paint([[x + 7, y + 9] for x, y in P], wash=INK, washOp=55 * a, ink=None)
    paint(P, wash='#E9E1F4' if back else '#FFF8EA', washOp=248 * a, fill='#E9DCC6', fillOp=50 * a, bleed=.05, border=.4, ink=INK, sw=.55)
    # washi tape at both ends
    for sgn in (-1, 1):
        boilSeed(f'tape{idx}{sgn}')
        push()
        translate(sgn * (w / 2 - size * .25), -h * .42)
        rotate(sgn * .5)
        paint(rectPts(-size * .55, -size * .2, size * 1.1, size * .4, 1), wash=TAPE[song], washOp=170 * a, ink=None)
        pop()
    # song mark at the left end
    ix = -w / 2 + pad * .75
    if zh:
        apple(ix, 4, size * .3, key=f'lyap{idx}')
    else:
        boilSeed(f'wave{idx}')
        inkLine([[ix - size * .32 + k * size * .08, size * .1 * math.sin(k * 1.4)] for k in range(9)], max(.8, size / 40), '#4E6AD8', 'ink', .4)
    c.restore()
    # words / characters write on as the melody reaches them
    x = -w / 2 + pad + size * .7
    col = INKC[song] if not back else '#5A4E7A'
    for u, wu, tu in zip(units, ws, ut):
        ag = t - (tu - LEAD)
        if ag >= 0:
            k = clamp(ag / .12)
            s_ = (1 + .35 * (1 - backOut(k))) * sc
            yy = -8 * math.exp(-ag * 12)
            text(u, x + wu * sc / 2, yy, size, col, shadow=False, a=a * clamp(ag / .05), sc=s_)
        x += (wu + gap) * sc
    pop()


def lyrics(t):
    for part in ('lead', 'back'):
        L = [(i, r) for i, r in enumerate(LY) if r['part'] == part]
        for j, (idx, r) in enumerate(L):
            st = r['ut'][0] - LEAD - .1
            nxt = L[j + 1][1]['ut'][0] - LEAD - .1 if j + 1 < len(L) else 1e9
            tight = nxt - r['end'] < .35
            en = nxt if tight else r['end']
            if tight and t >= nxt:
                continue
            if not (st <= t < (en if tight else en + .01)):
                continue
            zh = r['song'] == 'X'
            if part == 'lead':
                # while a backing line is up (Rolling chorus), the lead strip moves left to make room
                bk = any(q['part'] == 'back' and q['ut'][0] - LEAD - .1 <= t < q['end'] for q in LY)
                strip(t, r, idx, st, 1e9 if tight else en, 700 if bk else 960, 1010, 58 if zh else 52, -.012 if idx % 2 else .012)
            else:
                strip(t, r, idx, st, en, 1390, 935, 40, .025, back=True)


class Renderer:
    def __init__(self, cache_dir=None):
        self.F = Frame()

    def frame(self, t):
        t = t + 1.0 / FPS - 1e-3    # sample the END of the frame: an event at time tb shows in the frame that contains tb
        self.F.begin(t)
        composite(t)
        G.c.save()
        lyrics(t)
        G.c.restore()
        G.c.save()
        outro(t)    # closing heart iris + title banner sit above the lyric strip
        G.c.restore()
        self.F.grainPass()
        return self.F.end()
