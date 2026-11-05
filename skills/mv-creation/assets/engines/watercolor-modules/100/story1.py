# story1.py: 《100》 shots S01–S12 (verse, first half). One bar per shot, every beat carries a visible event. Data: storyboard.py.
import math
from hb import *
import hb, nm, tp, wx, ch, sets, sets2, hl, bsc, props
from sets2 import seat

# =====================================================================================
# S01 0–3.17 · title device: the notebook. 《100》 is written one stroke-group per beat and completes on the downbeat k4
NB = dict(cx=960, cy=500, w=1360, h=820)
TITLE_CH = [('《', 1), ('1', 2), ('0', 3), ('0', 4), ('》', 4)]
TITLE_SIZE = 170
TITLE_Y = 330


def deskDressing(t, old=0.0, lamp=1.0, key='dd'):
    """the things around the notebook (shared by S01 / S05 / S24 / S32)"""
    topLamp(210, 180, lamp, key=key + 'lamp')
    sets2.teacupTop(1800, 150, t, key=key + 'cup')
    headphonesTop(150, 700, 100, .4, key=key + 'hp')
    sets2.pencil(1790, 560, 1.9, 300, key=key + 'pen')
    sets2.washi(1700, 740, 160, 46, .3, '#F7B2C6', key=key + 'wa')


def titleOnPage(t, L, prog_t=None, a=1.0):
    """《100》 on the left page, char i finishing on its beat; returns the x of the writing edge (for the nib)"""
    x0 = L[0] + L[2] / 2
    ws = [textW(c, TITLE_SIZE, WENKAI) for c, _ in TITLE_CH]
    tot = sum(ws)
    x = x0 - tot / 2
    edge = None
    for (c, k), w in zip(TITLE_CH, ws):
        p = 1.0 if prog_t is None else clamp((t - (B[k] - .26)) / .24)
        if c == '》' and prog_t is not None:
            p = clamp((t - (B[k] - .12)) / .1)
        if p > 0:
            G.c.save()
            G.c.clipRect(skia.Rect.MakeXYWH(x - 4, TITLE_Y - TITLE_SIZE, (w + 8) * p, TITLE_SIZE * 2))
            text(c, x + w / 2, TITLE_Y, TITLE_SIZE, INK, face=WENKAI, shadow=False, a=a)
            G.c.restore()
            if prog_t is not None:
                edge = (x + w * p, TITLE_Y + 20)
        x += w
    return edge


def s01(t, lt, dur):
    cam(t, 960, 520, lerp(1.0, 1.035, ease(lt / dur)))
    woodTop()
    lampOn = clamp((t - (B[1] - .02)) / .06) if t > 0 else 0
    deskDressing(t, lamp=max(.25, lampOn))
    L, R = notebook(NB['cx'], NB['cy'], NB['w'], NB['h'])
    text('2026.11.01  周日', L[0] + L[2] / 2, 150, 34, '#8A7A88', face=WENKAI, shadow=False)
    edge = titleOnPage(t, L, prog_t=True)
    # k4: the title is complete — sparkle burst around it
    sk = hitK(t, 4, .3)
    if sk > .02:
        for i in range(10):
            a = i / 10 * TAU + .2
            r = 290 + 80 * (1 - sk)
            sparkle(L[0] + L[2] / 2 + math.cos(a) * r, TITLE_Y + math.sin(a) * r * .45, 24 * sk, '#FFC93D', sk)
    # k5 / k6: the subtitle
    sub = [('写给你的', 5), ('情歌', 6)]
    sx = L[0] + L[2] / 2 - textW('示例歌词占位', 66, WENKAI) / 2
    for s_, k in sub:
        p = clamp((t - (B[k] - .34)) / .32)
        handText(s_, sx, 560, 66, p, '#5A4A6A', WENKAI, 'left', pen=False)
        if p > 0:
            edge = (sx + textW(s_, 66, WENKAI) * p, 580)
        sx += textW(s_, 66, WENKAI)
    # underline after the subtitle lands
    if t >= B[6] - .04:
        k6 = clamp((t - (B[6] - .04)) / .16)
        x0_ = L[0] + L[2] / 2 - 230
        inkLine([[x0_, 612], [x0_ + 460 * k6, 606]], 1.6, HOT, 'ink', .3)
    # k7: doodles in the page corner
    if t >= B[7] - .04:
        k7 = popIn(t, 7)
        doodleHeart(L[0] + 120, 760, 46, HOT, k7, key='s1dh')
        note(L[0] + 230, 790, 34 * k7, '#5B7FC4', 2, key='s1n')
        doodleHeart(L[0] + L[2] - 130, 780, 30, '#F2A65A', k7, key='s1dh2')
    # right page: a polaroid of the two, a cassette, a to-do sticky note
    sets2.polaroidTop(R[0] + 230, R[1] + 230, -.08, key='s1pol', draw=lambda x, y, w, h: sets2.coupleSnap(x, y, w, h))
    sets2.washi(R[0] + 160, R[1] + 70, 130, 40, -.4, '#BFE3F5', key='s1w1')
    cassette(R[0] + R[2] - 210, R[1] + 300, 280, '♡', rot=.12, key='s1cas')
    nm.postit(R[0] + 220, R[1] + 600, 230, -.06, '周末任务：\n给她写歌', key='s1pi', size=34)
    if R[0] and t >= B[4] - .04:
        G.c.save()
        a4 = clamp((t - (B[4] - .04)) / .16)
        inkLine([[R[0] + 140, R[1] + 690], [R[0] + 160, R[1] + 712], [R[0] + 200, R[1] + 662]], 1.4 * a4 + .01, '#3FA37A', 'ink', .4)
        G.c.restore()
    # the pen writes by itself (no hand)
    if t >= B[7] - .04:
        edge = (lerp(edge[0], L[0] + L[2] / 2 + 300, easeOut(clamp((t - B[7]) / .2))), lerp(edge[1], 660, easeOut(clamp((t - B[7]) / .2))))
    if edge is not None:
        penNib(edge[0], edge[1], 46)
    camEnd()


# =====================================================================================
# S02 3.17–4.97 · 示例歌词占位: notes hop and swap, he goes dizzy, the notes slide off into a heap
def s02(t, lt, dur):
    cam(t, 960, 560, lerp(1.06, 1.1, ease(lt / dur)))
    nm.hisRoomBack(t)
    sx, sy, sw_, sh = musicStand(720, 900, 420, 420, key='s2ms')
    kIn = popIn(t, 8)
    push()
    translate(720, sy + sh)
    scale(1, kIn)
    translate(-720, -(sy + sh))
    gaps = staffPaper(sx - 20, sy - 60, sw_ + 40, sh + 40, key='s2sp', title='给她的歌')
    pop()
    # notes on the staff: positions are re-dealt on k9; on k11 they slide off and fall into a heap
    base = [(0, 3), (1, 1), (2, 4), (3, 2), (4, 0), (5, 3)]
    swap = [(0, 1), (1, 4), (2, 0), (3, 3), (4, 2), (5, 0)]
    fall = clamp((t - (B[11] - .14)) / .14)
    for i in range(6):
        row = i // 3
        col = i % 3 + row * 0
        slot, ln = base[i]
        if t >= B[9] - .1:
            k9 = clamp((t - (B[9] - .1)) / .1)
            s2, ln2 = swap[i]
            slot = lerp(slot, s2, easeOut(k9))
            ln = lerp(ln, ln2, easeOut(k9))
            hop = math.sin(k9 * math.pi) * 8
        else:
            hop = 0
        nx = sx + 40 + (slot % 3) * (sw_ - 40) / 3 + 30
        ny = gaps[i // 3] + 56 - ln * 14 - hop
        if kIn < .9:
            continue
        if fall > 0:
            nx += (i - 2.5) * 30 * fall
            ny = lerp(ny, 870 - (i % 3) * 22, easeIn(fall))
        note(nx, ny, 26, NOTE_COLS[i % 5], 1 + (i % 2), rot=.6 * fall * (1 if i % 2 else -1), key=f's2n{i}')
    if t >= B[11] - .04:
        stamp('啪', 560, 820, 64, '#FFF5E2', t - B[11], rot=-.15)
    # him: puzzled → dizzy → sweat
    u = 30
    o = emM(t, [[0, 'thinking'], [ek(9), 'confused'], [ek(10), 'dizzy'], [ek(11), 'nervous']], view='q', flip=True, lookX=.6)
    himH(1180, 900, u, o)
    if t >= B[10] - .04:
        stamp('？', 1180 - 5 * u, 900 - 12.5 * u, 110, '#FFE36E', t - B[10], rot=-.12)
        stamp('？', 1180 + 4.5 * u, 900 - 11 * u, 70, '#FFFFFF', t - B[10] - .05, rot=.18)
    camEnd()


# =====================================================================================
# S03 4.97–6.78 · 示例歌词占位: the bulb lights, he hums, the notes arc into a rainbow that ends in a heart
def s03(t, lt, dur):
    sunburst(700, 560, '#FFE9A8', '#FFD36A', 20, t * .15)
    cam(t, 960, 560, 1.0)
    u = 36
    o = emM(t, [[0, 'idea'], [ek(14) - .1, 'happy', {'mouth': 'O'}], [ek(15), 'love']], view='q', lookX=.7, lookY=-.4)
    if t >= B[13] - .1:
        o.update(view='q', aR=1.2)
    glow(600 + .6 * u, 900 - 12.6 * u, 120, '#FFF2A8', .8)
    himH(600, 900, u, o)
    if t >= B[12] - .04:
        stamp('叮！', 600 + 6 * u, 900 - 13 * u, 90, '#FFFFFF', t - B[12], rot=.12)
    # the melody arc from his mouth to the upper right
    P0, P1 = (600 + 6.8 * u, 900 - 7.4 * u), (1560, 420)
    n = 8

    def arcPt(f):
        return lerp(P0[0], P1[0], f), lerp(P0[1], P1[1], f) - 330 * math.sin(f * math.pi)
    shown = 0.0
    if t >= B[13] - .03:
        shown = 1.0 / n + (n - 1.0) / n * clamp((t - (B[14] - .2)) / (B[15] - B[14] + .02))
        if t < B[14] - .2:
            shown = 1.0 / n
    # rainbow ribbon under the notes (k14)
    if t >= B[14] - .2:
        kr = clamp((t - (B[14] - .2)) / (B[15] - B[14] + .02))
        cols = ['#FF8FB0', '#FFC27A', '#FFE36E', '#9EE29A', '#8FC7FF', '#C3A6FF']
        for j, c in enumerate(cols):
            pts = []
            for i in range(41):
                f = i / 40 * kr
                x, y = arcPt(f)
                pts.append([x, y + 34 + j * 16 * min(1, f * 6)])
            if len(pts) > 2:
                pa = skia.Path()
                pa.moveTo(*pts[0])
                for p in pts[1:]:
                    pa.lineTo(*p)
                G.c.drawPath(pa, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=17, Color=skcol(c, .85),
                                            StrokeCap=skia.Paint.kRound_Cap))
    for i in range(n):
        f = (i + .5) / n
        if f > shown + .001:
            continue
        x, y = arcPt(f)
        age_ = t - (B[13] if i == 0 else B[14] - .2 + (B[15] - B[14]) * (i / n))
        sc = 1 + .4 * math.exp(-max(0, age_) * 10)
        note(x, y + 6 * math.sin(t * 8 + i), 34 * sc, NOTE_COLS[i % 5], 1 + (i % 3 == 1), key=f's3n{i}')
    # k15: a heart opens at the end of the rainbow
    if t >= B[15] - .06:
        k15 = popIn(t, 15, .16)
        glow(P1[0], P1[1] + 60, 260, '#FF8FB0', .6 * k15)
        heart(P1[0] + 40, P1[1] + 60, 90 * k15, HOT, key='s3h')
        sparkles(t, 3, 10, P1[0] - 200, P1[1] - 150, P1[0] + 260, P1[1] + 250, 16, '#FFFFFF')
    camEnd()


# =====================================================================================
# S04 6.78–8.58 · 示例歌词占位文: split screen — her humming at home (left), the notes cross into his headphones (right)
def splitLine(t, x=960):
    pts = []
    for i in range(13):
        y = -60 + i * 100
        pts.append([x + (24 if i % 2 else -24), y])
    pa = skia.Path()
    pa.moveTo(*pts[0])
    for p in pts[1:]:
        pa.lineTo(*p)
    G.c.drawPath(pa, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=16, Color=skcol('#FFFDF6')))
    G.c.drawPath(pa, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skcol(INK)))


def s04(t, lt, dur):
    cam(t, 960, 540, 1.0)
    nod = hitK(t, 19, .14)
    # ---- left: her room, watering a pot while humming
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(-100, -100, 1060, H + 200))
    push()
    translate(-520, 0)
    nm.livingBack(t)
    pop()
    u = 30
    oH = emH(t, [[0, 'happy', {'eyes': 'closed', 'mouth': 'O'}]], view='q', aR=.9, lookX=.6)
    oH['dy'] = (oH.get('dy') or 0) + 1.0 * nod
    her(400, 900, u, oH)
    hx, hy = handXY(400, 900, u, oH, 'R')
    sets2.wateringCan(hx + 70, hy + 10, 56, pour=.55, facing=1, key='s4wc')
    # potted plant
    boilSeed('s4pot')
    paint([[650, 820], [760, 820], [740, 905], [670, 905]], wash='#D9774E', fill='#B85C3A', fillOp=60, ink=INK, sw=.9)
    for i in range(5):
        a = -math.pi / 2 + (i - 2) * .45
        paint(ellPts(705 + math.cos(a) * 60, 800 + math.sin(a) * 50, 38, 18, 12, 0, a), wash='#8FCB7A', fill='#6BAA5C', fillOp=50, ink=INK, sw=.5)
    for i in range(6):
        f = frac(t * 2.2 + i / 6)
        dot(lerp(hx + 140, 700, f), lerp(hy + 30, 800, f), 5, '#7FC6E8', 1 - f)
    G.c.restore()
    # ---- right: his room, at the desk with headphones and a sheet
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(960, -100, 1100, H + 200))
    push()
    translate(560, 0)
    nm.hisRoomBack(t)
    pop()
    oM = emM(t, [[0, 'thinking'], [ek(18), 'excited'], [ek(19), 'happy', {'eyes': 'closed'}]], view='q', flip=True, lookX=.4)
    oM['dy'] = (oM.get('dy') or 0) + 1.0 * nod
    himH(1560, 830, u, oM)
    tp.deskFront(760, 1000, 2000, key='s4dk')
    staffPaper(1090, 690, 300, 200, key='s4sp')
    # notes landing on his sheet in order (k18)
    if t >= B[18] - .1:
        for i in range(5):
            k = clamp((t - (B[18] - .1 + i * .03)) / .1)
            note(1150 + i * 50, 770 - (i % 3) * 14 - 30 * (1 - k), 18, NOTE_COLS[i], 1, a=k, key=f's4pn{i}')
    G.c.restore()
    # ---- the notes: from her mouth (k16) across the divider (k17) into his headphones (k18)
    for i in range(6):
        t0 = B[16] - .06 + i * .07
        f = clamp((t - t0) / (B[18] - t0 - .05))
        if t < t0 or (t > B[18] + .25):
            continue
        x = lerp(470, 1335, f)
        y = lerp(680, 640, f) - 220 * math.sin(f * math.pi) + 18 * math.sin(t * 10 + i) * (1 - f)
        note(x, y, 30, NOTE_COLS[i % 5], 1 + (i % 2), rot=.3 * math.sin(t * 7 + i), a=(1 - seg(f, .8, 1.0)) * (1 - seg(t, B[18], B[18] + .2)), key=f's4n{i}')
    splitLine(t)
    if t >= B[18] - .04:
        bubble(1380, 420, '就是这个！', 52, tail=(1520, 560), k=popIn(t, 18), key='s4b')
    if t >= B[19] - .04:
        for x in (400, 1560):
            heart(x + 150, 560 - 40 * easeOut(clamp((t - B[19]) / .3)), 26 * popIn(t, 19), HOT, key=f's4h{x}')
    camEnd()


# =====================================================================================
# S05 8.58–10.39 · 示例歌词占位: the lyric page fills up, bigger each beat, then a stamp
def s05(t, lt, dur):
    cam(t, 1290, 470, lerp(1.32, 1.38, ease(lt / dur)))
    woodTop()
    deskDressing(t)
    L, R = notebook(NB['cx'], NB['cy'], NB['w'], NB['h'])
    rx = R[0] + 90
    text('歌词', R[0] + R[2] / 2, R[1] + 70, 52, '#5A4A6A', face=WENKAI, shadow=False)
    inkLine([[R[0] + R[2] / 2 - 60, R[1] + 104], [R[0] + R[2] / 2 + 60, R[1] + 100]], 1.2, HOT, 'ink', .3)
    lines = [('想你', 20, 62, 220), ('很想你', 21, 86, 340), ('超级想你', 22, 112, 490)]
    last = None
    for txt, k, sz, y in lines:
        p = clamp((t - (B[k] - .3)) / .28)
        handText(txt, rx, y, sz, p, INK, WENKAI, 'left', pen=False)
        if p > 0:
            last = (rx + (textW(txt, sz, WENKAI) + 10) * p, y + sz * .1, sz)
    if last is not None and t < B[23] - .06:
        penNib(last[0], last[1], last[2] * .9)
    if t >= B[23] - .06:
        k23 = clamp((t - (B[23] - .06)) / .1)
        for i in range(26):
            hx_ = hash1(i * 3.3)
            hy_ = hash1(i * 7.7)
            x = R[0] + 90 + hx_ * (R[2] - 380)
            y = 575 + hy_ * 110
            if i < 26 * k23:
                text('想你', x, y, 26 + 10 * hash1(i), mixCol('#5A4A6A', HOT, hash1(i * 2.1)), face=WENKAI, shadow=False,
                     rot=(hash1(i * 9.1) - .5) * .5)
        rubberStamp('思念×100', R[0] + R[2] - 150, 630, 54, t - B[23], rot=-.16)
    camEnd()


# =====================================================================================
# S06 10.39–12.19 · 示例歌词占: chalkboard bullets — 你 / 你 / 还是你 — and a pie chart 你 100%
def s06(t, lt, dur):
    cam(t, 960, 560, 1.05)
    nm.hisRoomBack(t)
    bx, by, bw, bh = 220, 170, 900, 520
    sets.board(bx + bw / 2, by + bh / 2, bw, bh, col='#2F5D50', frame='#8A5A3C', key='s6b', legH=200)
    chalk('这首歌的大致内容：', bx + 50, by + 70, 46, 1.0)
    items = [('① 你', 24), ('② 你', 25), ('③ 还是你', 26)]
    for i, (txt, k) in enumerate(items):
        p = clamp((t - (B[k] - .2)) / .18)
        chalk(txt, bx + 80, by + 170 + i * 110, 72 if i < 2 else 80, p, '#FFF6C8' if i == 2 else '#F3F1E8')
        if i == 2 and p >= 1:
            hearts_ = popIn(t, 26)
            doodleHeart(bx + 470, by + 390, 30, '#FF9FBA', hearts_, key='s6dh')
    if t >= B[27] - .06:
        pieChart(bx + bw - 190, by + 300, 150, clamp((t - (B[27] - .06)) / .14), key='s6pie')
        kp = clamp((t - (B[27] - .06)) / .14)
        line(bx + bw - 190, by + 300, bx + bw - 190, by + 300 - 150 * backOut(kp), '#FFFFFF', .9, 5)
    # him with a pointer, tapping the line of the beat
    u = 32
    o = emM(t, [[0, 'determined'], [ek(27), 'proud']], view='q', flip=True, lookX=.6)
    j = lastBeat(t, [24, 25, 26, 27])
    targets = [.62, .45, .28, .7]
    a = targets[max(0, j)]
    tap = hitK(t, [24, 25, 26, 27][max(0, j)], .1) if j >= 0 else 0
    o.update(aR=a - .12 * tap, armR=wx.pointerHook(9.0))
    himH(1440, 900, u, o)
    if j >= 0 and j < 3:
        ty = by + 170 + j * 110
        ring(bx + 60, ty, 30 + 40 * (1 - hitK(t, [24, 25, 26][j], .2)), '#FFE36E', 5, hitK(t, [24, 25, 26][j], .25))
    camEnd()


# =====================================================================================
# S07 12.19–14.00 · 示例歌词: she listens on the sofa; the "corner of mouth" chart rises; +100%
def s07(t, lt, dur):
    cam(t, 960, 560, lerp(1.04, 1.1, ease(lt / dur)))
    nm.livingBack(t)
    st = nm.loveseat(820, 880, 620, key='s7ls')
    u = 30
    o = emH(t, [[0, 'neutral', {'eyes': 'closed'}], [ek(29), 'happy', {'eyes': 'closed'}], [ek(30), 'happy', {'eyes': 'closed', 'blush': .9}], [ek(31), 'love']],
            view='front', hat=['headphones', 'flower'])
    seat(her, 820, st, u, o)
    nm.loveseatArms(820, 880, 620, key='s7ls')
    # side table + tape deck
    boilSeed('s7tab')
    paint(rectPts(330, 790, 230, 26), wash='#C98B5A', ink=INK, sw=.8)
    for x in (350, 530):
        paint(rectPts(x, 816, 16, 90), wash='#A8714A', ink=INK, sw=.6)
    tapeDeck(445, 790, 230, play=landK(t, 28, .08), lit=1.0 if t >= B[28] - .04 else 0, key='s7td',
             tape=lambda x, y, s: cassette(x, y, s, spin=t * 2 if t >= B[28] else 0, key='s7c'))
    if t >= B[28] - .04:
        playIcon(445, 590, 50, t - B[28], life=.6)
    if t >= B[29] - .06:
        a29 = t - (B[29] - .06)
        for i in range(6):
            ang = -2.5 + i * .32
            d = 60 + 420 * easeOut(clamp(a29 / .5))
            note(445 + math.cos(ang) * d * 1.2, 600 + math.sin(ang) * d * .7 - 40 * a29, 34, NOTE_COLS[i % 5], 1 + i % 2,
                 rot=.3 * math.sin(t * 6 + i), a=1 - seg(a29, .9, 1.3), key=f's7b{i}')
    # the chart
    prog = 0.08 + .92 * clamp((t - (B[30] - .25)) / (B[31] - B[30] + .2))
    lineChart(1240, 230, 460, 380, prog, key='s7lc', label='她的嘴角')
    if t >= B[31] - .04:
        stamp('+100%', 1470, 690, 74, HOT, t - B[31], rot=.12, stroke='#FFFFFF')
        floatHearts(t, 7, 6, 650, 300, 1000, 600, 22)
    camEnd()


# =====================================================================================
# S08 14.00–15.80 · 示例歌词占: radar ping, the heart battery fills, 生效！, he jumps
def s08(t, lt, dur):
    cam(t, 960, 560, 1.05)
    nm.hisRoomBack(t)
    # the radar on a stand
    boilSeed('s8st')
    paint(rectPts(470, 640, 24, 260), wash='#4A4760', ink=INK, sw=.7)
    paint(ellPts(482, 905, 90, 18, 16), wash='#4A4760', ink=INK, sw=.7)
    radar(482, 500, 160, t, ping=hitK(t, 32, .35) if t >= B[32] - .04 else 0, key='s8rd')
    if t >= B[32] - .04:
        stamp('嘀！', 482, 270, 60, '#7CF29A', t - B[32], rot=-.1, life=.8)
    n = steps(t, [33, 34], [1, 2, 3], d=.06)
    blink = 0 if t >= B[34] - .04 else .5 * (1 + math.sin(t * 30))
    heartBattery(960, 430, 150, int(round(n)), key='s8hb', blink=blink * 0)
    text('爱心电量', 960, 640, 48, '#FFFFFF', face=WENKAI, stroke=INK, strokeW=8, shadow=False)
    if t >= B[34] - .04:
        rubberStamp('生效！', 960, 760, 72, t - B[34], rot=-.12)
    u = 32
    o = emM(t, [[0, 'hopeful'], [ek(34), 'surprised'], [ek(35), 'excited']], view='q', flip=True, lookX=.6)
    if t >= B[35] - .12:
        o['dy'] = (o.get('dy') or 0) - 1.5 * math.sin(clamp((t - (B[35] - .12)) / .5) * math.pi)
        o['aR'] = 2.0
    himH(1460, 900, u, o)
    if t >= B[35] - .04:
        bsc.confetti(t, 1200, 240, (t - B[35]) / .9, seed=8, n=50, spread=520)
    camEnd()


# =====================================================================================
# S09 15.80–17.61 · 示例歌 词占位 文字示: he bursts in with a boombox, BOOM; she frowns and holds up 不爱听
def s09(t, lt, dur):
    shake = hitK(t, 37, .12) * 14
    cam(t, 960 + shake * math.sin(t * 90), 560, 1.04)
    nm.livingBack(t)
    st = nm.loveseat(1300, 880, 520, key='s9ls')
    u = 30
    oH = emH(t, [[0, 'neutral'], [ek(37), 'surprised'], [ek(38), 'angry']], view='q', flip=True, lookX=.6)
    if t >= B[39] - .1:
        oH['aR'] = 1.9
    seat(her, 1300, st, u, oH)
    nm.loveseatArms(1300, 880, 520, key='s9ls')
    if t >= B[39] - .1:
        hx, hy = handXY(1300, st + 2 * u, u, oH, 'R')
        ch.placardSign(hx, hy - 196 + 40 * (1 - popIn(t, 39)), 320, 150, '不爱听', 70, rot=.0, key='s9pc')
    # him sliding in from the left with the boombox on his shoulder
    ent = landK(t, 36, .2)
    xM = lerp(-200, 520, easeOut(ent))
    oM = emM(t, [[0, 'cool']], view='q', aR=2.3, aL=.4)
    if t >= B[38] - .04:
        oM = emM(t, [[0, 'cool'], [ek(38), 'nervous']], view='q', aR=2.3, aL=.4)
    oM['hat'] = 'beanie'
    him(xM, 900, u, oM)
    beat = hitK(t, beatIdx(t), .1) if t >= B[36] - .04 else 0
    boombox(xM + 3.2 * u, 900 - 10.6 * u, 300, beat, key='s9bb')
    if t >= B[36] - .04:
        stamp('BOOM', xM + 40, 170, 96, '#FFE36E', t - B[36], rot=-.12, life=.7)
        bassRings(xM + 3.2 * u, 900 - 10.6 * u, (t - B[36]) % (B[37] - B[36]), 3, '#FFFFFF', 700, .7)
    if t >= B[37] - .04:
        bassRings(xM + 3.2 * u, 900 - 10.6 * u, t - B[37], 3, '#FF8FB0', 900, .8)
        # her picture frame on the wall knocked crooked
    boilSeed('s9fr')
    tilt = .25 * clamp((t - (B[37] - .04)) / .08) if t >= B[37] - .04 else 0
    push()
    translate(1640, 300)
    rotate(tilt + .03 * math.sin(t * 40) * hitK(t, 37, .2))
    paint(rectPts(-80, -60, 160, 120), wash='#E8D3B8', ink=INK, sw=.8)
    paint(rectPts(-62, -44, 124, 88), wash='#BFE3F5', ink=None)
    heart(0, 0, 24, HOT, key='s9frh')
    pop()
    if B[38] - .04 <= t < B[39] - .1:
        bubble(1300 - 6 * u, st - 9 * u, '哼！', 60, tail=(1300 - 2 * u, st - 4 * u), k=popIn(t, 38), key='s9b')
    camEnd()


# =====================================================================================
# S10 17.61–19.41 · 示例 歌词占: the drum machine blinks, he pulls the plug, it greys out, a big red X
def s10(t, lt, dur):
    cam(t, 960, 540, lerp(1.0, 1.04, ease(lt / dur)))
    gradRect(-300, -300, W + 600, H + 600, ['#2B3168', '#4A4486'])
    sets2.fairyLights(t, -100, 2020, 90, 50, 18, key='s10fl')
    u = 40
    o = emM(t, [[0, 'cool'], [ek(41), 'determined'], [ek(43), 'happy', {'eyes': 'wink'}]], view='front')
    pulled = t >= B[41] - .04
    o.update(aR=.08 if not pulled else .08 + .5 * clamp((t - (B[41] - .04)) / .12), aL=.3)
    himH(1330, 760, u, o)
    tp.deskFront(700, key='s10dk')
    grey = clamp((t - (B[42] - .06)) / .08)
    drum808(700, 610, 680, t, 0 if pulled else 1, hitK(t, 40, .12), key='s10dm', grey=grey)
    # the cable to the wall socket (right), and the plug
    boilSeed('s10sock')
    paint(rrPts(1560, 520, 90, 120, 12), wash='#FFFDF6', ink=INK, sw=.8)
    for d in (-1, 1):
        dot(1605 + d * 16, 580, 8, INK)
    if not pulled:
        ch.cable((1040, 640), (1590, 580), sag=60, col='#3D3A52')
        ch.plug(1590, 580, 34, ang=0, key='s10plg')
    else:
        kk = clamp((t - (B[41] - .04)) / .25)
        px, py = lerp(1590, 1560, easeOut(kk)), lerp(580, 690, easeIn(kk))
        ch.cable((1040, 640), (px, py), sag=80, col='#3D3A52')
        ch.plug(px, py, 34, ang=-1.2 * kk, key='s10plg')
        if t < B[41] + .25:
            for i in range(7):
                a = i / 7 * TAU
                line(1600 + math.cos(a) * 30, 580 + math.sin(a) * 30, 1600 + math.cos(a) * (60 + 60 * kk), 580 + math.sin(a) * (60 + 60 * kk),
                     '#FFE36E', 1 - kk, 6)
            stamp('啵', 1660, 470, 60, '#FFE36E', t - B[41], rot=.15, life=.4)
    if t < B[41] - .04 and t >= B[40] - .04:
        stamp('动次打次', 700, 340, 70, '#FFE36E', t - B[40], rot=-.08, life=.5)
    if t >= B[42] - .04:
        bigX(700, 600, 220, clamp((t - (B[42] - .04)) / .1), age=t - B[42])
    if t >= B[43] - .04:
        ch.heartSticker(1620, 300, 120, '温柔版', popIn(t, 43), rot=.12, key='s10hs')
    camEnd()


# =====================================================================================
# S11 19.41–21.21 · 示例歌词占位: curly notes up, down, a falsetto that stretches him, the wine glass cracks
def s11(t, lt, dur):
    cam(t, 960, 560, 1.03)
    bg('#D6EFE6')
    # piano-key wall decal + floor
    boilSeed('s11keys')
    for i in range(14):
        paint(rectPts(240 + i * 72, 120, 70, 260), wash='#FFFDF6', ink=INK, sw=.6)
    for i in range(14):
        if i % 7 in (0, 1, 3, 4, 5):
            paint(rectPts(240 + i * 72 + 48, 120, 44, 160), wash='#2B2233', ink=None)
    text('声乐课', 750, 440, 56, '#3FA37A', face=WENKAI, shadow=False)
    flatRect(-300, 820, W + 600, 600, '#B9D9C9')
    G.c.drawLine(-300, 820, W + 300, 820, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=3))
    # pitch meter on the left
    pitch = steps(t, [44, 45, 46, 47], [.3, .65, .35, 1.0, .85], d=.12)
    boilSeed('s11pm')
    paint(rrPts(110, 300, 80, 480, 30), wash='#FFFDF6', ink=INK, sw=.9)
    hgt = 440 * pitch
    G.c.drawRoundRect(skia.Rect.MakeXYWH(124, 760 - hgt, 52, hgt), 20, 20,
                      skia.Paint(AntiAlias=True, Color=skcol(mixCol('#7CF29A', '#FF6F96', pitch))))
    text('音高', 150, 830, 36, INK, face=WENKAI, shadow=False)
    mx, my = micStand(860, 900, 330, key='s11mic')
    u = 32
    stretch = 0
    if t >= B[46] - .08:
        stretch = math.sin(clamp((t - (B[46] - .08)) / .45) * math.pi)
    o = emM(t, [[0, 'happy', {'mouth': 'O', 'eyes': 'closed'}], [ek(46), 'excited', {'mouth': 'O'}], [B[47] - .16, 'surprised']],
            view='q', flip=True, aR=.9)
    o.update(sy=1 + .35 * stretch, sx=1 - .15 * stretch)
    himH(1060, 900, u, o)
    # curly notes (转音): a spiral path that rises (k44) then falls (k45)
    for i in range(7):
        if t < B[44] - .06:
            break
        f = clamp((t - (B[44] - .06)) / (B[46] - B[44]))
        g = i / 7
        if g > f:
            continue
        up = g < .5
        x = 1300 + g * 380 + 45 * math.cos(g * 25)
        y = (560 - g * 2 * 300 if up else 260 + (g - .5) * 2 * 300) + 45 * math.sin(g * 25)
        note(x, y, 40, NOTE_COLS[i % 5], 1, rot=math.sin(t * 6 + i) * .3, key=f's11n{i}')
    if t >= B[46] - .04:
        stamp('假音～', 1180, 480 - 40 * stretch, 80, '#FF6F96', t - B[46], rot=.1, stroke='#FFFFFF')
    # the wine glass on a little stand
    boilSeed('s11st')
    paint(rectPts(1480, 760, 220, 22), wash='#C98B5A', ink=INK, sw=.8)
    paint(rectPts(1580, 782, 20, 120), wash='#A8714A', ink=INK, sw=.6)
    nm.wineGlass(1590, 760, 120, fill=.45, key='s11wg')
    if t >= B[47] - .04:
        k47 = clamp((t - (B[47] - .04)) / .12)
        for d in (-1, 1):
            inkLine([[1590, 560], [1590 + d * 14, 600], [1590 - d * 6, 630], [1590 + d * 18, 670]], 1.2 * k47 + .01, INK, 'ink', 0)
        for i in range(6):
            a = -math.pi / 2 + (i - 2.5) * .5
            r = 40 + 140 * clamp((t - B[47]) / .4)
            dot(1590 + math.cos(a) * r, 600 + math.sin(a) * r, 6, '#CFE8F7', 1 - clamp((t - B[47]) / .5))
        stamp('叮！', 1720, 500, 90, '#FFE36E', t - B[47], rot=.15)
    camEnd()


# =====================================================================================
# S12 21.21–23.02 · 示例歌: strum, strum, a chord of hearts, then a string snaps 嘣
def s12(t, lt, dur):
    cam(t, 960, 560, lerp(1.05, 1.1, ease(lt / dur)))
    nm.hisRoomBack(t)
    u = 34
    j = lastBeat(t, [48, 49, 50, 51])
    strumK = hitK(t, [48, 49, 50, 51][max(0, j)], .18) if j >= 0 and j < 3 else 0
    o = emM(t, [[0, 'determined'], [ek(50), 'happy', {'eyes': 'closed'}], [ek(51), 'surprised']], view='front')
    o.update(aL=.9, aR=-.2 + .6 * strumK)
    himH(960, 900, u, o)
    snap = clamp((t - (B[51] - .04)) / .1) if t >= B[51] - .04 else 0
    guitar(960 - 1.6 * u, 900 - 2.5 * u, 5.0 * u, -.3, key='s12g', strum=strumK, snap=snap, t=t)
    for i, k in enumerate([48, 49]):
        if t >= B[k] - .04:
            a_ = t - B[k]
            note(960 + 7 * u + i * 60, 900 - 9 * u - a_ * 300, 34, NOTE_COLS[i], 1 + i, a=1 - seg(a_, .5, .8), key=f's12n{i}')
    if t >= B[50] - .04:
        wx.hearts(t, 960, 900 - 12 * u, 10, 300, 34, (t - (B[50] - .04)) / .7, seed=12)
        note(960 + 7 * u, 900 - 11 * u - (t - B[50]) * 200, 50, HOT, 2, key='s12big', a=1 - seg(t - B[50], .35, .5))
    if t >= B[51] - .04:
        stamp('嘣！', 960 + 6 * u, 900 - 12 * u, 96, '#FFE36E', t - B[51], rot=.15)
    camEnd()
