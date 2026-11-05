# render.py (《东西》, from 《可不可以给我你的微信》: 白山茶 base + 宠坏 flash/karaoke fixes): Renderer().frame(t) -> BGRA (H, W, 4). 2560x1440 (MV_OUT), 24 fps. Frames sample the END of the frame interval,
# so an event at beat time tb shows in the frame that contains tb. Karaoke colour leads the sung syllable by 2 frames.
import math, bisect
from eng import *
import eng
from story import SHOTS
from common import LY, DUR
from opening import openingTitle


# ---- opening title + signature timing (hard rule 8, 2026-11-01): enter on the landing beat, leave before the first
# bar line that still gives >= 1.2 s of exposure; fast songs pop in 0.22 s, slow songs (bar > 2.4 s) fade 0.4 s, no bounce.
from common import B as _B, isDown as _isDown
K_TITLE = 0                                                       # landing beat (k) of the title card
TA = _B[K_TITLE]
_downs = [_B[k] for k in range(K_TITLE + 1, len(_B)) if _isDown(k)]
BAR = _downs[1] - _downs[0]
SLOW = BAR > 2.4
TO = next(d for d in _downs if d - TA >= 1.2)                    # fully gone by this bar line
if TO - TA > 4:
    TO -= BAR / 2
FO = .4 if SLOW else .22

W_, H_, FPS = OUT_W, OUT_H, 24
STARTS = [s[0] for s in SHOTS]
LEAD = 2 / 24
FADE = (DUR - .3, DUR)
PRE = dict(wipe=.16, iris=.2)


def shotAt(t):
    return max(0, bisect.bisect_right(STARTS, t + 1e-9) - 1)


def drawShot(i, t):
    t0, fn, _, _ = SHOTS[i]
    dur = (SHOTS[i + 1][0] if i + 1 < len(SHOTS) else DUR) - t0
    G.CLAWD_N = 0
    n = G.c.getSaveCount()
    G.c.save()
    fn(t, t - t0, dur)
    G.c.restoreToCount(n)      # shots push a camera without popping it; never leak a save level (it would trap a wipe clip)


def wipePoly(k):
    x = lerp(-500, eng.W + 500, k)
    return [[-200, -200], [x + 250, -200], [x - 250, eng.H + 200], [-200, eng.H + 200]], (x + 250, -200, x - 250, eng.H + 200)


def composite(t):
    i = shotAt(t)
    # wipes / irises into the NEXT shot run BEFORE its downbeat, so the beat frame already shows the new shot
    # a flash into the NEXT shot whitens the outgoing shot just before the beat, so the beat frame already shows the new shot
    if i + 1 < len(SHOTS) and SHOTS[i + 1][2] == 'flash' and t > SHOTS[i + 1][0] - .1:
        drawShot(i, t)
        flash(.82 * ease(seg(t, SHOTS[i + 1][0] - .1, SHOTS[i + 1][0] - .01)))
        return
    if i + 1 < len(SHOTS) and SHOTS[i + 1][2] in PRE and t > SHOTS[i + 1][0] - PRE[SHOTS[i + 1][2]]:
        i += 1
    t0, fn, tr, sid = SHOTS[i]
    c = G.c
    if tr == 'wipe' and t < t0 and i > 0:
        k = ease(seg(t, t0 - PRE['wipe'], t0 - .005))
        drawShot(i - 1, t)
        poly, edge = wipePoly(k)
        c.save()
        c.clipPath(eng._path(poly), skia.ClipOp.kIntersect, True)
        drawShot(i, t)
        c.restore()
        boilSeed('wipeedge')
        inkLine([[edge[0], edge[1]], [edge[2], edge[3]]], 3.0, INK, 'ink', 0)
        return
    if tr == 'iris' and t < t0 and i > 0:
        k = easeOut(seg(t, t0 - PRE['iris'], t0 - .005))
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
    if tr == 'dissolve' and i > 0 and t < t0 + .25:
        k = ease(seg(t, t0 - .04, t0 + .25))
        drawShot(i - 1, t)
        c.saveLayerAlpha(None, int(255 * k))
        drawShot(i, t)
        c.restore()
        return
    drawShot(i, t)
    if tr == 'flash' and t < t0 + .16:
        flash(.4 * (1 - seg(t, t0, t0 + .16)))


def karaoke(t):
    n = len(LY)
    for i, (a, b, txt, ch) in enumerate(LY):
        nxt = LY[i + 1][0] if i + 1 < n else 1e9
        prv = LY[i - 1][1] if i > 0 else -1e9
        fin = 0 if a - prv < .35 else .12
        tight = nxt - b < .35
        end = nxt - LEAD if tight else b + .12
        start = a - LEAD if fin == 0 else a - fin
        if not (start <= t < end):
            continue
        alpha = (1 if fin == 0 else ease(seg(t, a - fin, a))) * (1 if tight else 1 - ease(seg(t, b, b + .12)))
        size = 64
        f = skia.Font(typeface(KUAILE), size)
        chars = list(txt)
        widths = [f.measureText(c_) if c_ != ' ' else size * .45 for c_ in chars]
        gap = 4
        total = sum(widths) + gap * (len(chars) - 1)
        x = eng.W / 2 - total / 2
        y = 1012
        pop_ = 1      # tight line changes hard-cut at full size (a scale-in reads as a tiny / wide-spaced line for a frame)
        ci = 0
        for c_, w_ in zip(chars, widths):
            if c_ == ' ':
                x += w_ + gap
                continue
            tc = ch[ci]
            ci += 1
            sung = t >= tc - LEAD
            ag = t - (tc - LEAD)
            sc = (1 + .22 * math.exp(-ag * 9) if sung and ag < .5 else 1) * pop_
            col = '#FF6F96' if sung else PAL['cream']
            text(c_, x + w_ / 2, y - (8 * math.exp(-ag * 10) if sung and ag < .4 else 0), size, col, stroke=INK, strokeW=13,
                 shadow=True, a=alpha, sc=sc)
            x += w_ + gap


class Renderer:
    def __init__(self, cache_dir=None):
        self.F = Frame()

    def frame(self, t):
        t = t + 1.0 / FPS - 1e-5          # sample the END of the frame interval (a beat 1 ms before the boundary still counts)
        self.F.surf.getCanvas().restoreToCount(1)
        self.F.begin(t)
        composite(t)
        self.F.grainPass()
        G.c.save()
        karaoke(t)
        G.c.restore()
        # opening tag: song title + the user's watermark 你的署名, screen space, over the first shot (hard rule 8)
        if SLOW:            # slow song: 0.4 s fade from 0.1 s before the landing beat, no bounce (the fade lives in the layer alpha)
            k_in = 1.0
            k_out = ease(seg(t, TA - .1, TA + .3)) * (1 - ease(seg(t, TO - FO, TO)))
        else:
            k_in = backOut(clamp((t - (TA - .04)) / .22))
            k_out = 1 - ease(seg(t, TO - FO, TO))
        if k_out > .01 and t < TO + .05:
            G.c.save()
            openingTitle(k_in, k_out)
            G.c.restore()
        f0, f1 = FADE
        if t > f0:
            G.c.save()
            G.c.resetMatrix()
            G.c.drawRect(skia.Rect.MakeXYWH(0, 0, OUT_W, OUT_H), skia.Paint(Color=skcol('#05060F', .9 * ease(seg(t, f0, f1)))))
            G.c.restore()
        return self.F.end()
