# daw.py: the beat-grid (DAW) world for 《白山茶》 — lanes, clips, waveforms, ruler, playhead, transport, keycaps,
# mixer, BPM display — plus the song's flowers (white camellia, red rose). Everything is a pure function of its args.
import math
from eng import *
import eng

# themes: present (ice blue), memory (warm gold on plum), grey (after he is deleted)
BLUE = dict(bg0='#0B1230', bg1='#131C42', lane='#141E46', lane2='#18234F', laneLn='#2A3A70', beat='#22305E', bar='#4B66B0',
            clip='#2F7FD6', clipDk='#1D5BA8', clipLt='#8FD3FF', wave='#CFEFFF', head='#0E1636', txt='#CFE6FF', ruler='#0F1838',
            accent='#5FC4FF', panel='#0A0F26')
WARM = dict(bg0='#24142A', bg1='#3A2036', lane='#2E1A32', lane2='#36203A', laneLn='#5A3A58', beat='#432A46', bar='#9A6A62',
            clip='#E3A04A', clipDk='#B27330', clipLt='#FFE0A0', wave='#FFF4D6', head='#22122A', txt='#FFE8C8', ruler='#26142C',
            accent='#FFC86A', panel='#1A0D20')
GREY = dict(bg0='#0E1018', bg1='#171A26', lane='#161924', lane2='#1A1D2A', laneLn='#2C3042', beat='#22263A', bar='#4A4F66',
            clip='#4F5670', clipDk='#3A4058', clipLt='#9AA2BC', wave='#C8CEE0', head='#10121C', txt='#AEB4C8', ruler='#12141E',
            accent='#9AA2BC', panel='#0A0B12')

HIM_C = ('#D97757', '#A84D33', '#F5B394')
HER_C = ('#EE9AAE', '#C0637B', '#FBD0DA')
ROSE_C = ('#D83A4E', '#9C2236', '#FF8A98')
CAM_C = ('#F4F1EA', '#C9C2B4', '#FFFFFF')


def mixTheme(a, b, k):
    if k <= 0:
        return a
    if k >= 1:
        return b
    return {key: mixCol(a[key], b[key], k) for key in a}


def _pa(col, a=1.0, w=None, cap=True):
    p = skia.Paint(AntiAlias=True, Color=skcol(col, a))
    if w is not None:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(w)
        if cap:
            p.setStrokeCap(skia.Paint.kRound_Cap)
    return p


def line(x0, y0, x1, y1, col, a=1.0, w=1.5):
    G.c.drawLine(x0, y0, x1, y1, _pa(col, a, w))


def rrect(x, y, w, h, r, col, a=1.0):
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), r, r, _pa(col, a))


def rrectS(x, y, w, h, r, col, a=1.0, sw=2):
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), r, r, _pa(col, a, sw))


def tri(pts, col, a=1.0):
    flat(pts, col, a)


# ------------------------------------------------------------------ icons drawn as shapes (the font has no ▶ ◀ ● ■ ♥)
def icoPlay(x, y, s, col, a=1.0):
    tri([[x - s * .45, y - s * .55], [x + s * .6, y], [x - s * .45, y + s * .55]], col, a)


def icoRew(x, y, s, col, a=1.0):
    for dx in (0, -s * .55):
        tri([[x + dx + s * .35, y - s * .5], [x + dx - s * .35, y], [x + dx + s * .35, y + s * .5]], col, a)


def icoRec(x, y, s, col, a=1.0):
    G.c.drawCircle(x, y, s * .45, _pa(col, a))


def icoStop(x, y, s, col, a=1.0):
    rrect(x - s * .42, y - s * .42, s * .84, s * .84, s * .08, col, a)


def icoHeart(x, y, s, col, a=1.0, ink=False, key='ih'):
    P = heartPts(x, y, s, 26)
    if ink:
        boilSeed(key)
        paint(P, wash=col, washOp=int(255 * a), ink=INK, sw=1.0)
    else:
        flat(P, col, a)


def icoWave(x, y, s, col, a=1.0):
    for i, hh in enumerate((.3, .7, 1, .55, .85, .4, .2)):
        xx = x + (i - 3) * s * .18
        line(xx, y - s * .4 * hh, xx, y + s * .4 * hh, col, a, s * .07)


# ------------------------------------------------------------------ waveform inside a clip
def waveform(x, y, w, h, col, a=1.0, seed=0, style='song', amp=1.0, bw=4.0, gap=2.0, env=None, t=0.0):
    """vertical mirrored bars. style: song (dense), chop (DJ chops), smooth, heart (outline of a heart), none"""
    n = max(1, int(w / (bw + gap)))
    p = _pa(col, a, bw * .8)
    cy = y + h / 2
    for i in range(n):
        u = i / max(1, n - 1)
        xx = x + i * (bw + gap) + bw / 2
        r = hash1(seed * 7.3 + i * 1.37)
        if style == 'song':
            v = .25 + .55 * abs(math.sin(i * .35 + seed)) * (.6 + .4 * r) + .2 * r
        elif style == 'chop':
            blk = int(i / 6)
            on = hash1(seed + blk * 3.1) > .3
            v = (.35 + .6 * r) * (1 if on else .08) * (1 - (i % 6) / 9)
        elif style == 'smooth':
            v = .25 + .25 * math.sin(i * .22 + seed) + .15 * r
        elif style == 'heart':
            hx = (u - .5) * 2.2
            # half-height of a heart curve at hx
            v = 0
            if abs(hx) < 1.1:
                top = math.sqrt(max(0, 1 - (abs(hx) - .5) ** 2 * 3.6)) * .55 + .35
                v = top * (1 - .15 * r)
            v *= .95
        else:
            v = .1
        if env:
            v *= env(u)
        v = clamp(v * amp, .02, 1)
        if style == 'heart':
            # heart: taller upward lobes, pointed bottom
            hx = (u - .5) * 2
            up = h * .5 * v
            dn = h * .5 * clamp(1 - abs(hx) * 1.05) * amp
            G.c.drawLine(xx, cy - up, xx, cy + dn, p)
        else:
            G.c.drawLine(xx, cy - h * .5 * v, xx, cy + h * .5 * v, p)


# ------------------------------------------------------------------ a clip block
def clipBlock(x, y, w, h, th, name='', cols=None, wave='song', seed=0, lit=0.0, key='clip', a=1.0, amp=1.0, nameSize=None,
              env=None, sel=False, t=0.0, waveCol=None):
    c, dk, lt = cols or (th['clip'], th['clipDk'], th['clipLt'])
    if lit > .01:
        glow(x + w / 2, y + h / 2, max(w, h) * .65, lt, .55 * lit * a)
    boilSeed(key)
    body = rrPts(x, y, w, h, min(14, h * .2), 1.2)
    paint(body, wash=mixCol(c, lt, .25 * lit), washOp=int(235 * a), fill=dk, fillOp=int(70 * a), bleed=.05, tex=.5, ink=None)
    hh = min(30, h * .26) if name else 0
    if name:
        G.c.save()
        G.c.clipPath(eng._path(body), skia.ClipOp.kIntersect, True)
        flatRect(x, y, w, hh, dk, .85 * a)
        G.c.restore()
        ns = nameSize or hh * .72
        text(name, x + 10, y + hh / 2 + 1, ns, mixCol(lt, '#FFFFFF', .5), align='left', shadow=False, a=a)
    if wave and wave != 'none':
        waveform(x + 8, y + hh + 6, w - 16, h - hh - 12, waveCol or mixCol(lt, '#FFFFFF', .35 + .4 * lit), .9 * a, seed, wave, amp,
                 env=env, t=t)
    paint(body, ink=INK, sw=1.1)
    if lit > .01:
        rrectS(x - 2, y - 2, w + 4, h + 4, 14, '#FFFFFF', .5 * lit * a, 2.5)


# ------------------------------------------------------------------ the whole arrangement view
def laneLayout(heights, y0=118):
    ys = []
    y = y0
    for hh in heights:
        ys.append((y, y + hh))
        y += hh
    return ys


def dawBG(th, lanes, gx0=230, bw=120, bar0=1, k0=2, y0=118, header=True, ruler=True, dimL=None, scroll=0.0, xHead=230, t=0.0,
          beatHit=None):
    """lanes: list of (name, height, colourTriple or None, icon). Draws bg, lane bands, beat grid, ruler, track headers.
    gx0: x of beat k0 (downbeat of bar0); bw: pixels per beat. scroll shifts the grid left (beats). returns lane y spans."""
    gradRect(-300, -300, W + 600, H + 600, [th['bg0'], th['bg1']])
    ys = laneLayout([l[1] for l in lanes], y0)
    for i, ((a_, b_), L) in enumerate(zip(ys, lanes)):
        dim = (dimL or {}).get(i, 0)
        flatRect(-300, a_, W + 600, b_ - a_, th['lane'] if i % 2 == 0 else th['lane2'], 1)
        if dim:
            flatRect(-300, a_, W + 600, b_ - a_, '#000000', .45 * dim)
        line(-300, b_, W + 300, b_, th['laneLn'], .9, 1.4)
    yTop, yBot = ys[0][0], ys[-1][1]
    # beat grid
    off = gx0 - scroll * bw
    i0 = int(math.floor((-300 - off) / bw)) - 1
    i1 = int(math.ceil((W + 300 - off) / bw)) + 1
    for i in range(i0, i1):
        x = off + i * bw
        down = i % 4 == 0
        hitA = 0
        if beatHit is not None:
            hitA = beatHit(i)
        line(x, yTop, x, yBot, mixCol(th['bar'] if down else th['beat'], '#FFFFFF', .5 * hitA), .9 if down else .7, 2.0 if down else 1.0)
    if ruler:
        flatRect(-300, yTop - 34, W + 600, 34, th['ruler'], 1)
        line(-300, yTop, W + 300, yTop, th['laneLn'], 1, 1.2)
        for i in range(i0, i1):
            x = off + i * bw
            if i % 4 == 0:
                n = bar0 + i // 4
                line(x, yTop - 30, x, yTop, th['bar'], 1, 2)
                text(str(n), x + 14, yTop - 16, 22, th['txt'], align='left', shadow=False, a=.85)
            else:
                line(x, yTop - 10, x, yTop, th['beat'], 1, 1.2)
    if header:
        flatRect(-300, yTop - 34, xHead + 300, yBot - yTop + 34, th['head'], 1)
        line(xHead, yTop - 34, xHead, yBot, th['laneLn'], 1, 2)
        for i, ((a_, b_), L) in enumerate(zip(ys, lanes)):
            nm = L[0]
            cols = L[2] or (th['clip'], th['clipDk'], th['clipLt'])
            dim = (dimL or {}).get(i, 0)
            cy = (a_ + b_) / 2
            rrect(18, a_ + 12, 10, b_ - a_ - 24, 4, mixCol(cols[0], '#555566', dim), 1)
            icoWave(56, cy, 34, mixCol(th['txt'], '#555566', dim), .9)
            text(nm, 82, cy, 26 if b_ - a_ > 70 else 20, mixCol(th['txt'], '#555566', dim), align='left', shadow=False, a=1)
    return ys


def playhead(x, y0, y1, th=BLUE, a=1.0):
    glow(x, (y0 + y1) / 2, 60, th['accent'], .25 * a)
    line(x, y0, x, y1, '#F4FBFF', a, 3)
    tri([[x - 12, y0 - 18], [x + 12, y0 - 18], [x, y0]], '#F4FBFF', a)


def topBar(th, t, title='白山茶', titleK=None, titleSize=44, play=0.0, rec=0.0, stop=0.0, bpm='128', cx=W / 2, bpmK=0.0):
    """the DAW's title strip: transport on the left, project name centre. titleK = per-char landing progress (0..1, None = shown)."""
    flatRect(-300, -300, W + 600, 300 + 84, th['panel'], 1)
    line(-300, 84, W + 300, 84, th['laneLn'], 1, 1.5)
    # window chrome above the strip (only seen in the opening close-up)
    flatRect(-300, -300, W + 600, 210, '#070B1C', 1)
    line(-300, -90, W + 300, -90, th['laneLn'], .8, 1.2)
    for i, c_ in enumerate(('#FF5F57', '#FEBC2E', '#28C840')):
        G.c.drawCircle(560 + i * 34, -130, 10, _pa(c_, .85))
    text(title + '.flp  —  编曲', cx, -130, 26, th['txt'], shadow=False, a=.75)
    for i, m in enumerate(('文件', '编辑', '视图', '插入', '混音', '帮助')):
        text(m, 560 + i * 84, -55, 22, th['txt'], align='left', shadow=False, a=.55)
    text('00:0%d' % int(t) if t < 10 else '00:%02d' % int(t), 1300, -55, 24, th['accent'], shadow=False, a=.8)
    # transport
    bx = 60
    icoRec(bx, 42, 34, mixCol('#C04A5A', '#FF3B4E', rec), .55 + .45 * rec)
    if rec > .05:
        glow(bx, 42, 40, '#FF3B4E', .7 * rec)
    icoRew(bx + 72, 42, 30, th['txt'], .8)
    G.c.drawCircle(bx + 150, 42, 26, _pa(mixCol('#FFFFFF', th['accent'], play), .95))
    icoPlay(bx + 153, 42, 24, th['panel'], 1)
    if play > .05:
        glow(bx + 150, 42, 60, th['accent'], .6 * play)
    icoStop(bx + 220, 42, 28, mixCol(th['txt'], '#FF5A6A', stop), .8 + .2 * stop)
    text(bpm, bx + 300, 38, 34, mixCol(th['txt'], '#FFFFFF', bpmK), shadow=False)
    text('BPM', bx + 300, 66, 14, th['txt'], shadow=False, a=.7)
    # title: 《白山茶》 with each character landing on its beat
    chars = list('《' + title + '》')
    widths = [textW(ch, titleSize) for ch in chars]
    tot = sum(widths) + 4 * (len(chars) - 1)
    x = cx - tot / 2
    for i, (ch, w_) in enumerate(zip(chars, widths)):
        if 0 < i < len(chars) - 1 and titleK is not None:
            k = titleK[i - 1]
        elif titleK is not None:
            k = min(titleK) if i == 0 else titleK[-1]
            k = clamp(k * 1.5)
        else:
            k = 1
        if k > .01:
            sc = backOut(clamp(k))
            text(ch, x + w_ / 2, 42 - 18 * (1 - clamp(k * 1.3)), titleSize, '#F6FBFF', stroke=INK, strokeW=6, shadow=True, a=clamp(k * 2),
                 sc=sc)
            if 0 < k < 1:
                glow(x + w_ / 2, 42, titleSize * 1.1, th['accent'], .6 * (1 - k))
        x += w_ + 4


# ------------------------------------------------------------------ keycaps, cursor, selection, loop brace
def keycap(txt, x, y, s, press=0.0, key='kc', col='#F2F4FA', a=1.0, wmul=1.0):
    """a keyboard key; press 0..1 pushes it down. (x, y) = centre of the top face"""
    if a <= .01:
        return
    w = s * wmul
    d = s * .16 * (1 - press)
    boilSeed(key)
    paint(rrPts(x - w / 2, y - s / 2 + s * .16, w, s, s * .16), wash='#9AA0B8', ink=INK, sw=1.0)
    paint(rrPts(x - w / 2, y - s / 2 + s * .16 - d, w, s, s * .16), wash=mixCol(col, '#BFE8FF', press * .6), ink=INK, sw=1.1)
    text(txt, x, y + s * .16 - d, s * (.36 if len(txt) > 2 else .5), INK, shadow=False, a=a)
    if press > .3:
        glow(x, y, s * 1.2, '#9FE2FF', .5 * press)


def cursorArrow(x, y, s=1.0, grab=False):
    P = [[0, 0], [0, 34], [9, 26], [16, 40], [22, 37], [15, 24], [27, 24]]
    P = [[x + px * s, y + py * s] for px, py in P]
    boilSeed('cursor')
    paint(P, wash='#FFFFFF', ink=INK, sw=1.4)
    if grab:
        G.c.drawCircle(x, y, 9 * s, _pa('#5FC4FF', .9, 3))


def marchingBox(x, y, w, h, t, col='#7FD8FF', a=1.0, sw=3):
    p = _pa(col, a, sw, cap=False)
    ph = (t * 60) % 24
    p.setPathEffect(skia.DashPathEffect.Make([14, 10], ph))
    G.c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), p)
    flatRect(x, y, w, h, col, .10 * a)


def loopBrace(x0, x1, y, th, label='', a=1.0, h=26):
    rrect(x0, y, x1 - x0, h, 6, th['accent'], .85 * a)
    flatRect(x0, y + h, x1 - x0, 12, th['accent'], .18 * a)
    if label:
        text(label, (x0 + x1) / 2, y + h / 2 + 1, h * .78, th['panel'], shadow=False, a=a)


# ------------------------------------------------------------------ mixer pieces
def ledMeter(x, y, w, h, v, a=1.0, n=16):
    seg_ = h / n
    for i in range(n):
        yy = y + h - (i + 1) * seg_
        u = i / (n - 1)
        col = '#4FE07A' if u < .6 else ('#F6D04D' if u < .85 else '#FF4F5E')
        on = (i + .5) / n <= v
        rrect(x, yy + 2, w, seg_ - 4, 3, col if on else '#1A2240', a * (1 if on else .9))
        if on and i == int(v * n) - 1:
            glow(x + w / 2, yy + seg_ / 2, w * 1.6, col, .5 * a)


def faderStrip(x, y, h, v, th, name='', capCol='#E8ECF6', w=120, a=1.0, meter=None, key='fd'):
    """a channel strip: v 0..1 cap position. returns the cap's top-centre (where a character can stand)"""
    flatRect(x - w / 2, y - 60, w, h + 120, th['head'], .95 * a)
    line(x - w / 2, y - 60, x - w / 2, y + h + 60, th['laneLn'], a, 1.5)
    rrect(x - 7, y, 14, h, 7, '#05081A', a)
    for i in range(11):
        yy = y + h * i / 10
        line(x - 30, yy, x - 16, yy, th['txt'], .5 * a, 2)
        line(x + 16, yy, x + 30, yy, th['txt'], .5 * a, 2)
    if meter is not None:
        ledMeter(x + 34, y, 14, h, meter, a, 18)
    cy = y + h * (1 - v)
    boilSeed(key)
    paint(rrPts(x - 34, cy - 16, 68, 32, 8), wash=capCol, fill='#9AA0B8', fillOp=60, ink=INK, sw=1.2)
    line(x - 26, cy, x + 26, cy, INK, .8, 2)
    if name:
        text(name, x, y + h + 34, 24, th['txt'], shadow=False, a=a)
    return x, cy - 16


def bpmScreen(x, y, w, h, val, th, a=1.0, glowK=0.0, label='BPM'):
    boilSeed('bpmscr')
    paint(rrPts(x - w / 2 - 14, y - h / 2 - 14, w + 28, h + 28, 26), wash='#2A3150', ink=INK, sw=1.6)
    rrect(x - w / 2, y - h / 2, w, h, 16, '#06101E', a)
    if glowK > .01:
        glow(x, y, w * .7, '#FF7FA8', .5 * glowK)
    col = mixCol('#7FF0FF', '#FF8FB4', glowK)
    text(val, x - w * .08, y + 4, h * .62, col, shadow=False, a=a)
    text(label, x + w * .36, y + h * .22, h * .16, col, shadow=False, a=.8 * a)


def knob(x, y, r, ang, th, key='knob'):
    boilSeed(key)
    paint(ellPts(x, y + r * .12, r, r, 32), wash='#14182C', ink=None)
    paint(ellPts(x, y, r, r, 32), wash='#C8CEE0', fill='#8A92AC', fillOp=70, ink=INK, sw=1.3)
    for i in range(11):
        aa = -math.pi * 1.25 + i / 10 * math.pi * 1.5
        line(x + math.cos(aa) * r * 1.18, y + math.sin(aa) * r * 1.18, x + math.cos(aa) * r * 1.34, y + math.sin(aa) * r * 1.34,
             th['txt'], .8, 3)
    aa = -math.pi * 1.25 + ang * math.pi * 1.5
    line(x, y, x + math.cos(aa) * r * .78, y + math.sin(aa) * r * .78, INK, 1, r * .14)


# ------------------------------------------------------------------ flowers
def camellia(x, y, r, open_=1.0, wilt=0.0, outer=8, key='cam', rot=0.0, a=1.0, stem=0.0):
    """white camellia, head centred at (x, y). open_: bud 0 → full 1. wilt droops and yellows. outer = petals left on the outer ring."""
    if r < 1:
        return
    boilSeed(key)
    col = mixCol('#FBF8F2', '#E2D2A6', wilt * .8)
    shade = mixCol('#D9D2C6', '#B79E6E', wilt)
    push()
    translate(x, y)
    rotate(rot + wilt * .5)
    if stem > 0:
        inkLine([[0, r * .4], [r * .1, r * .4 + stem * .5], [-r * .05, r * .4 + stem]], 2.2, '#4E7A44', 'ink', .5)
        paint([[r * .05, r * .4 + stem * .5], [r * .9, r * .2 + stem * .45], [r * .25, r * .62 + stem * .5]], wash='#5F8F4E', ink=INK,
              sw=.8)
    ok = clamp(open_)
    if ok < .25:
        # bud: green sepals around a white tip
        bw = r * .45
        paint(ellPts(0, 0, bw * .75, bw, 18), wash=col, fill=shade, fillOp=70, ink=INK, sw=1.0)
        paint([[-bw * .8, bw * .2], [0, bw * 1.15], [bw * .8, bw * .2], [bw * .3, bw * .55], [0, bw * .1], [-bw * .3, bw * .55]],
              wash='#6E9F58', ink=INK, sw=.9)
    else:
        k = (ok - .25) / .75
        rr = r * lerp(.55, 1, easeOut(k))
        droop = wilt * .35
        for ring_, (n, rad, sz) in enumerate(((outer, 1.0, .58), (6, .66, .48), (5, .38, .36))):
            for i in range(n if ring_ == 0 else (6 if ring_ == 1 else 5)):
                ang = i / (8 if ring_ == 0 else n) * TAU + ring_ * .4 + .2
                px = math.cos(ang) * rr * rad * .55 * (.4 + .6 * k)
                py = math.sin(ang) * rr * rad * .55 * (.4 + .6 * k) + droop * rr * (1 if math.sin(ang) > 0 else .3)
                ps = rr * sz * (.6 + .4 * k)
                P = ellPts(px, py, ps, ps * .82, 16, 0, ang)
                paint(P, wash=mixCol(col, '#FFFFFF', .3 * (2 - ring_) / 2) if ring_ else col, fill=shade, fillOp=int(55 + 25 * wilt),
                      bleed=.04, ink=INK, sw=.8)
        if wilt > .2:
            for i in range(outer):
                ang = i / 8 * TAU + .2
                G.c.drawCircle(math.cos(ang) * rr * .82, math.sin(ang) * rr * .82 + droop * rr, rr * .09,
                               _pa('#A88A50', .35 * wilt))
        paint(ellPts(0, droop * rr * .3, rr * .17, rr * .17, 14), wash=mixCol('#F2C94C', '#B08A3C', wilt), ink=INK, sw=.7)
        for i in range(9):
            ang = i / 9 * TAU
            G.c.drawCircle(math.cos(ang) * rr * .12, math.sin(ang) * rr * .12 + droop * rr * .3, rr * .03, _pa('#C08A1E', .9))
    pop()


def petal(x, y, s, rot, wilt=.5, key='pt'):
    boilSeed(key)
    col = mixCol('#FBF8F2', '#E2D2A6', wilt * .8)
    paint(ellPts(x, y, s, s * .7, 14, 0, rot), wash=col, fill='#C9B78E', fillOp=60, ink=INK, sw=.7)


def rose(x, y, r, key='rose', a=1.0, stem=0.0, lean=0.0):
    """red rose head at (x, y)"""
    boilSeed(key)
    push()
    translate(x, y)
    rotate(lean)
    if stem > 0:
        inkLine([[0, r * .6], [-r * .1, r * .6 + stem * .5], [0, r * .6 + stem]], 2.4, '#3F6E3A', 'ink', .5)
        paint([[-r * .05, r * .6 + stem * .45], [-r * .95, r * .35 + stem * .4], [-r * .3, r * .8 + stem * .45]], wash='#4F8A45', ink=INK,
              sw=.8)
    c, dk, lt = ROSE_C
    paint([[-r * .95, -r * .1], [-r * .7, r * .7], [0, r], [r * .7, r * .7], [r * .95, -r * .1], [r * .5, -r * .35], [0, -r * .2],
           [-r * .5, -r * .35]], wash=c, fill=dk, fillOp=90, curv=.4, ink=INK, sw=1.0)
    paint([[-r * .62, -r * .45], [-r * .25, -r * .95], [r * .3, -r * .9], [r * .66, -r * .42], [r * .2, -r * .15], [-r * .2, -r * .2]],
          wash=mixCol(c, lt, .25), fill=dk, fillOp=60, curv=.4, ink=INK, sw=.9)
    inkLine([[-r * .35, -r * .3], [0, -r * .55], [r * .3, -r * .35], [r * .05, -r * .1], [-r * .15, -r * .3]], 1.0, INK, 'inkfine', .5)
    inkLine([[-r * .6, r * .2], [0, r * .45], [r * .6, r * .2]], .9, dk, 'inkfine', .5)
    pop()


# ------------------------------------------------------------------ misc
def folderIcon(x, y, w, h, open_=0.0, key='fold', col='#F2C55C', dk='#C2912E', label=''):
    """folder whose bottom-left is (x, y + h). open_ tilts the front flap open."""
    boilSeed(key)
    paint([[x, y + h * .12], [x + w * .38, y + h * .12], [x + w * .45, y], [x + w, y], [x + w, y + h], [x, y + h]], wash=dk, ink=INK, sw=1.2)
    fy = y + h * .2 + h * .5 * open_
    paint([[x - w * .02 * open_, fy], [x + w + w * .02 * open_, fy], [x + w, y + h], [x, y + h]], wash=col, fill=dk, fillOp=40, ink=INK,
          sw=1.3)
    if label:
        text(label, x + w / 2, (fy + y + h) / 2, h * .2, '#5A3A10', shadow=False)


def pixelDust(cx, cy, u, k, cols, seed=0, n=70):
    """a character breaking into square pixels that drift up and away. k 0..1"""
    if k <= 0:
        return
    for i in range(n):
        h1, h2, h3 = hash1(seed + i * 1.7), hash1(seed + i * 3.1), hash1(seed + i * 5.9)
        x0 = cx + (h1 - .5) * 10 * u
        y0 = cy - h2 * 8 * u
        dx = (h1 - .5) * 9 * u * k + 4 * u * k * (h3 - .3)
        dy = -k * (3 + 6 * h3) * u
        s = u * (.9 - .7 * k) * (.6 + .6 * h2)
        col = cols[i % len(cols)]
        a = 1 - clamp((k - .25 * h3) / .75)
        if s > .5 and a > .01:
            flatRect(x0 + dx - s / 2, y0 + dy - s / 2, s, s, col, a)


def headphones(u, sw, view='front', col='#4A5A8A'):
    """draw hook (body-local coords) for a Clawd wearing headphones over the hat"""
    P = [[-5.4 * u, -5.6 * u], [-5.6 * u, -9.0 * u], [-3.0 * u, -12.2 * u], [0, -12.8 * u], [3.0 * u, -12.2 * u], [5.6 * u, -9.0 * u],
         [5.4 * u, -5.6 * u]]
    inkLine(P, sw * 2.6, INK, 'ink', .6)
    inkLine(P, sw * 1.5, col, 'ink', .6)
    for s in (-1, 1):
        paint(rrPts(s * 5.6 * u - 1.0 * u, -7.0 * u, 2.0 * u, 2.8 * u, .7 * u), wash=col, fill='#2A3460', fillOp=80, ink=INK, sw=sw * .8)


def micStand(x, y, s, key='mic', glowK=0.0, ink=INK):
    """floor mic stand, base at (x, y); s = height of the stand"""
    boilSeed(key)
    inkLine([[x - s * .22, y], [x, y - s * .05], [x + s * .22, y]], 2.4, ink, 'ink', .3)
    inkLine([[x, y - s * .05], [x, y - s * .8]], 2.6, ink, 'ink', 0)
    inkLine([[x, y - s * .8], [x - s * .14, y - s * .92]], 2.4, ink, 'ink', 0)
    if glowK > .01:
        glow(x - s * .18, y - s * .98, s * .25, '#FF8FB4', .6 * glowK)
    paint(rrPts(x - s * .26, y - s * 1.08, s * .16, s * .24, s * .07), wash='#5A6280', fill='#2E3450', fillOp=90, ink=INK, sw=1.0)
    for i in range(3):
        line(x - s * .24, y - s * (1.03 - i * .055), x - s * .12, y - s * (1.03 - i * .055), '#C8CEE0', .7, 1.4)


def splash(x, y, s, k, col='#BFE8FF'):
    if k <= 0 or k >= 1:
        return
    for i in range(7):
        ang = -math.pi * (.15 + .7 * i / 6)
        d = s * (.3 + .9 * easeOut(k))
        G.c.drawCircle(x + math.cos(ang) * d, y + math.sin(ang) * d + s * .8 * k * k, s * .07 * (1 - k), _pa(col, .9 * (1 - k)))
