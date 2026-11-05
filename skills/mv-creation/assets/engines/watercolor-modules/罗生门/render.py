# render.py (《罗生门》 vertical 2:3: lyric bar at y≈1330, x 80–900; from 《匆匆那年》; from 《我好想你》 / 《99》; from 《100》 / 《可不可以给我你的微信》: 白山茶 base + 宠坏 flash/karaoke fixes): Renderer().frame(t) -> BGRA (H, W, 4). 2560x1440 (MV_OUT), 24 fps. Frames sample the END of the frame interval,
# so an event at beat time tb shows in the frame that contains tb. Karaoke colour leads the sung syllable by 2 frames.
import math, bisect
from eng import *
import eng
from story import SHOTS
from common import LY, DUR
from opening import openingTitle
from lsm import narration, cornerTag
from common import SB as _SB
NARR = [tuple(x) for x in _SB.get('narr', [])]
TAGS = [tuple(x) for x in _SB.get('tags', [])]


# ---- opening credit timing (hard rule 8, B-style title card): S03 the gate 「罗生门 / Follow」 opens on K36 (16.88, hats in);
# slow song (bar 3.75 s): signature + artists fade in 0.4 s from K36 - 0.1 and are gone by the next bar line K44 (20.64) = the cut.
from common import B as _B, isDown as _isDown
K_TITLE = 36
TA = _B[K_TITLE]
_downs = [_B[k] for k in range(K_TITLE + 1, len(_B)) if _isDown(k)]
BAR = _downs[1] - _downs[0]
SLOW = BAR > 2.4
TO = next(d for d in _downs if d - TA >= 1.2)
if TO - TA > 4:
    TO -= BAR / 2
FO = .4 if SLOW else .22

W_, H_, FPS = OUT_W, OUT_H, 24
STARTS = [s[0] for s in SHOTS]
LEAD = 2 / 24
FADE = (DUR - 2.5, DUR - .04)                # the record fades by itself: slow fade to full black over the last 2.5 s
PRE = dict(wipe=.16, iris=.2)
XD = (.35, .6)                                # 'xdis': slow cross-dissolve for the ballad, 0.95 s around the cut


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
    if i + 1 < len(SHOTS) and SHOTS[i + 1][2] == 'xdis' and t > SHOTS[i + 1][0] - XD[0]:
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
    if tr == 'xdis' and i > 0 and t < t0 + XD[1]:
        k = ease(seg(t, t0 - XD[0], t0 + XD[1]))
        drawShot(i - 1, t)
        c.saveLayerAlpha(None, int(255 * k))
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
        flash(.22 * (1 - seg(t, t0, t0 + .12)))


def _cutBefore(a):
    """a shot cut up to 0.45 s before a line's first syllable (rap lines start just after the bar line): the line page
    switches on that cut frame, so the new shot never opens under the previous shot's lyric"""
    cs = [s for s in STARTS if a - .45 <= s <= a + 1e-6]
    return max(cs) if cs else None


def karaoke(t):
    n = len(LY)
    for i, (a, b, txt, ch) in enumerate(LY):
        nxt = LY[i + 1][0] if i + 1 < n else 1e9
        prv = LY[i - 1][1] if i > 0 else -1e9
        fin = 0 if a - prv < .45 else .12
        tight = nxt - b < .45
        end = nxt - LEAD if tight else b + .12
        start = a - LEAD if fin == 0 else a - fin
        c0 = _cutBefore(a)
        if c0 is not None and i > 0:
            start, fin = min(start, c0 - 1e-4), 0
        c1 = _cutBefore(nxt) if i + 1 < n else None
        if c1 is not None and c1 > a:
            end, tight = min(end, c1 - 1e-4), True
        if not (start <= t < end):
            continue
        alpha = (1 if fin == 0 else ease(seg(t, a - fin, a))) * (1 if tight else 1 - ease(seg(t, b, b + .12)))
        # vertical 2:3: the bar sits at y≈1330 between x 80 and 900 (the right button column starts at x≈920); shrink to >= 52,
        # else break into two rows
        chars = list(txt)
        gap = 4
        size = 64
        while True:
            f = skia.Font(typeface(KUAILE), size)
            widths = [f.measureText(c_) if c_ != ' ' else size * .45 for c_ in chars]
            total = sum(widths) + gap * (len(chars) - 1)
            if total <= 820 or size <= 52:
                break
            size -= 2
        rows = [(0, len(chars))]
        if total > 820:
            cut = len(chars) // 2
            if ' ' in txt:
                sp = [i for i, c_ in enumerate(chars) if c_ == ' ']
                cut = min(sp, key=lambda i: abs(i - len(chars) / 2))
            rows = [(0, cut), (cut, len(chars))]
        pop_ = 1      # tight line changes hard-cut at full size (a scale-in reads as a tiny / wide-spaced line for a frame)
        ci = 0
        for ri, (r0, r1) in enumerate(rows):
          rw = sum(widths[r0:r1]) + gap * (r1 - r0 - 1)
          x = 490 - rw / 2
          y = 1330 if len(rows) == 1 else 1294 + ri * (size + 14)
          for c_, w_ in zip(chars[r0:r1], widths[r0:r1]):
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
        narration(t, NARR)
        cornerTag(t, TAGS)
        G.c.restore()
        # opening credit: 「★你的署名」 + artist beside the note title (A1), slow fade in / out (hard rule 8)
        if SLOW:
            a_ = ease(seg(t, TA - .1, TA + .3)) * (1 - ease(seg(t, TO - FO, TO)))
            if a_ > .01:
                G.c.save()
                openingTitle(1.0, a_)
                G.c.restore()
        else:
            k_in = backOut(clamp((t - (TA - .04)) / .22))
            k_out = 1 - ease(seg(t, TO - FO, TO))
            if k_in > .01 and k_out > .01:
                G.c.save()
                openingTitle(k_in, k_out)
                G.c.restore()
        f0, f1 = FADE
        if t > f0:
            G.c.save()
            G.c.resetMatrix()
            G.c.drawRect(skia.Rect.MakeXYWH(0, 0, OUT_W, OUT_H), skia.Paint(Color=skcol('#05060F', ease(seg(t, f0, f1)))))
            G.c.restore()
        return self.F.end()
