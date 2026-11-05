# story_a.py: 《罗生门》 S01–S07 — the intro (night 312: the unread weather question, ◀◀ rewind, title gate, the blizzard alert)
# and the first line of chorus 1 (day 0 at the station). Vertical 2:3 canvas 1080x1620.
import math
from eng import *
import eng
from hl import tint, desat, vignette
from couple import jhim, jher
from lsm import *
from lsm2 import stationNorth
from common import B, cam, es, kt, pk

K4, K12, K16, K28, K32, K34, K36, K44, K46, K48, K52, K54, K60, K64, K68 = (B[k] for k in (4, 12, 16, 28, 32, 34, 36, 44, 46, 48, 52, 54, 60, 64, 68))
EB = B[2] - B[0]          # one felt beat (0.94 s); B[k+1]-B[k] = one eighth (0.47 s)


def placeholder(t, lt, dur):
    gradRect(-100, -100, W + 200, H + 200, ['#20263A', '#2E3550'])
    text('待做', W / 2, H / 2, 80, CREAM, face=WK, shadow=False)


def grade(kind, k=1.0):
    """after camEnd(): night = cool, past = warm gold"""
    if kind == 'night':
        tint('#B4C0E6', .22 * k, skia.BlendMode.kMultiply)
        vignette(.38 * k, '#0E1128')
    elif kind == 'past':
        tint('#FFD9A8', .20 * k, skia.BlendMode.kMultiply)
        tint('#FFE9C8', .07 * k, skia.BlendMode.kScreen)
        vignette(.30 * k, '#2A1A10')


# ---------------------------------------------------------------- phone frame (the UI sits inside a phone so the top stays free for narration)
PH = dict(x=86, y=214, s=.84)


def inPhone(draw, bg='room', t=0.0, tilt=0.0):
    if bg == 'room':
        gradRect(-400, -400, W + 800, H + 800, ['#1E2140', '#2C2A4E', '#3A3358'])
        for i in range(9):                                     # bokeh of the string lights behind the phone
            bx, by = hash1(i * 5) * W, 120 + hash1(i * 9) * 300
            glow(bx, by, 90, ['#FFD27A', '#FFB2A6', '#BFE3F2'][i % 3], .32 + .1 * math.sin(t * 2 + i))
    x, y, s = PH['x'], PH['y'], PH['s']
    w, h = W * s, H * s
    push()
    translate(W / 2, y + h / 2)
    rotate(tilt)
    translate(-W / 2, -(y + h / 2))
    glow(W / 2, y + h / 2, 760, '#9FC4F0', .28)
    boilSeed('phonebody')
    paint(rrPts(x - 26, y - 26, w + 52, h + 52, 78), wash='#22212C', ink=INK, sw=1.0)
    G.c.save()
    G.c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), 56, 56), True)
    push()
    translate(x, y)
    scale(s, s)
    draw()
    pop()
    G.c.restore()
    paint(rrPts(W / 2 - 70, y + 10, 140, 30, 15), wash='#111018', ink=None)     # camera notch
    pop()


# ================================================================ S01 0 – K12: his room, the 312th question goes out (hook)
def s01(t, lt, dur):
    z = lerp(1.0, 1.45, es(t, 2.2, K12 + .1))
    cx = lerp(W / 2, 470, es(t, 2.2, K12))
    cy = lerp(H / 2, 1080, es(t, 2.2, K12))
    cam(t, cx, cy, z)
    hisRoom(t)
    u = 26
    gx, gy = 470, 1330
    chairBack(gx, gy - 2.9 * u, u)
    sent = t >= K4 - .05
    ex = dict(lookY=.7, mouth='small' if sent else 'flat', brows='up' if sent else None, blush=.5)
    jhim(gx, gy, u, dict(legs='sit', hands=dict(L=[-1.15, -7.7], R=[1.15, -7.7]), ex=ex, key=1))
    deskTop(t)
    deskItems(t)
    phoneObj(gx, 1140, 66, 0.0, glowK=1.0)
    # the message leaves the phone on the first bar line
    k = seg(t, K4 - .06, K4 + 1.9)
    if 0 < k < 1:
        yb = lerp(1100, 770, easeOut(k))
        a = clamp(k * 6) * (1 - seg(k, .75, 1))
        sc = lerp(.5, 1.0, easeOut(clamp(k * 3)))
        push()
        translate(gx + 60, yb)
        scale(sc, sc)
        bubble(260, -45, '示例歌词占位文字？', True, THEMES['now'], a=a)
        pop()
    camEnd()
    grade('night')
    nameCard(300, 1325, '他 · 留在南方', '在小酒馆唱歌', es(t, 2.2, 2.7) * (1 - es(t, 5.0, 5.5)), -.03, 'nc_him')


# ================================================================ S02 K12 – K36: the chat; ◀◀ rewind through 311 nights; ▶▶ back to the unread one
NOW312 = [('sep', '11月19日 23:00 · 第311天'), ('me', '示例歌词占位文字？'), ('her', '还在下雪 堆了个雪人'), ('herpic', 'snowman'),
          ('her', '晚安'), ('sep', '11月20日 23:00 · 第312天'), ('me', '示例歌词占位文字？'), ('status', '未读')]
REW = [
    [('sep', '第298天'), ('me', '示例歌词占位文字？'), ('her', '零下二十度！'), ('her', '鼻子都冻红了')],
    [('sep', '第276天'), ('me', '示例歌词占位文字？'), ('her', '晴天 可还是想你')],
    [('sep', '第240天'), ('me', '示例歌词占位文字？'), ('her', '示例歌词占位文字'), ('me', '……')],
    [('sep', '第213天'), ('me', '示例歌词占位文字？'), ('her', '下雨了 撑着你的伞'), ('herpic', 'umbrella')],
    [('sep', '第180天'), ('me', '示例歌词占位文字？'), ('her', '热死啦')],
    [('sep', '第150天'), ('me', '示例歌词占位文字？'), ('herpic', 'sunset'), ('her', '今天的晚霞 给你')],
    [('sep', '第100天'), ('me', '一百天快乐'), ('her', '示例歌词占位文字？'), ('me', '下雨 想你')],
    [('sep', '第64天'), ('me', '示例歌词占位文字？'), ('her', '第一场雪！'), ('herpic', 'street')],
    [('sep', '第30天'), ('me', '示例歌词占位文字？'), ('her', '冷 但是还好')],
    [('sep', '第7天'), ('me', '示例歌词占位文字？'), ('her', '有点想家')],
    [('sep', '第2天'), ('me', '示例歌词占位文字？'), ('her', '又下雪了')],
]
DAY1 = [('sep', '去年11月13日 · 第1天'), ('me', '到了吗？'), ('her', '到啦！'), ('me', '示例歌词占位文字？'), ('her', '下雪了 好冷'),
        ('herpic', 'street'), ('me', '那以后 我每天都问')]


def s02(t, lt, dur):
    rewind = K16 <= t < K28
    hold1 = K28 <= t < K32
    ffwd = K32 <= t < K34
    def draw():
        if t < K16:
            chatScreen(t, NOW312, 'now', '23:00', scroll=0)
        elif rewind:
            i = min(len(REW) - 1, int((t - K16) / (B[17] - B[16])))
            p = (t - (K16 + i * (B[17] - B[16]))) / (B[17] - B[16])
            off = -340 * (1 - easeOut(clamp(p * 2.4)))
            chatScreen(t, REW[i], 'old', '23:00', scroll=off)
        elif hold1:
            n = len(DAY1)
            al = [1.0] * n
            al[-1] = clamp((t - (K28 + .5)) / .2)
            chatScreen(t, DAY1, 'old', '23:00', scroll=0, a_items=al)
            if t > K28 + .5:
                k = es(t, K28 + .5, K28 + .9)
                glow(720, 1100, 240, '#FFE3A0', .45 * k * (.8 + .2 * math.sin(t * 6)))
        elif ffwd:
            seqs = list(reversed(REW))
            i = min(len(seqs) - 1, int((t - K32) / ((K34 - K32) / len(seqs))))
            chatScreen(t, seqs[i], 'now', '23:00', scroll=180 * frac((t - K32) * 9))
        else:
            k = t - K34
            chatScreen(t, NOW312, 'now', '23:00', scroll=0, pulse=1 + .6 * math.exp(-k * 7))
        if rewind or ffwd:
            scanJitter(t, .8)
        if rewind:
            rewindBadge(t, 1.0)
        if ffwd:
            rewindBadge(t, 1.0, fwd=True)
        if rewind or hold1:
            tint('#FFE2B0', .10, skia.BlendMode.kMultiply)
    sh = math.sin(t * 40) * 3 if (rewind and frac((t - K16) / (B[17] - B[16])) < .15) else 0
    push()
    translate(sh, 0)
    inPhone(draw, 'room', t, tilt=-.012 + .006 * math.sin(t * .7))
    pop()
    vignette(.30, '#0E1128')


# ================================================================ S03 K36 – K44: the title gate 「罗生门 / Follow」
def s03(t, lt, dur):
    z = lerp(1.0, 1.04, es(t, K36, K44))
    cam(t, W / 2, H / 2, z)
    titleGate(t, 1.0)
    camEnd()
    vignette(.35, '#0A0C1E')


# ================================================================ S04 K44 – K52: 00:41「睡了吗」, 01:52「那 晚安」, unread; the screen goes dark
def s04(t, lt, dur):
    items = list(NOW312)
    clock = '23:00'
    pops = []
    if t >= K44 - .05:
        items += [('sep', '00:41'), ('me', '睡了吗'), ('status', '未读')]
        clock = '00:41'
        pops.append(K44)
    if t >= K46 - .05:
        items += [('sep', '01:52'), ('me', '那 晚安'), ('status', '未读')]
        clock = '01:52'
        pops.append(K46)
    full = [('sep', ''), ('me', 'x'), ('status', '')]
    scroll = 0
    if t >= K44 - .05:
        scroll += 220 * easeOut(clamp((t - (K44 - .05)) / .3))
    if t >= K46 - .05:
        scroll += 220 * easeOut(clamp((t - (K46 - .05)) / .3))
    def draw():
        n = len(items)
        al = [1.0] * n
        chatScreen(t, items, 'now', clock, scroll=scroll, a_items=al, batt=.22)
        # screen off at the mini break: dark glass with the room reflected
        d = es(t, K48 - .05, K48 + .12)
        if d > .01:
            flatRect(-50, -50, W + 100, H + 100, '#06070E', .96 * d)
            for i in range(9):
                bx, by = hash1(i * 5 + 1) * W, 300 + hash1(i * 9 + 2) * 260
                glow(bx, by, 60, ['#FFD27A', '#FFB2A6', '#BFE3F2'][i % 3], .22 * d)
            # his reflection: a faint head with spiky hair, looking down
            G.c.saveLayerAlpha(None, int(60 * d))
            jhim(W / 2, 1900, 52, dict(view='front', ex=dict(eyes='half', mouth='flat', lookY=.6), key=9, shadow=False, blink=False))
            G.c.restore()
    inPhone(draw, 'room', t, tilt=-.01)
    vignette(.32, '#0E1128')


# ================================================================ S05 K52 – K60: 03:12, the lock screen wakes: blizzard red alert up north
def s05(t, lt, dur):
    def draw():
        wake = es(t, K52 - .04, K52 + .2)
        lockScreen(t, '03:12', '11月21日 星期六', notif=clamp((t - (K54 - .2)) / .35), dark=1 - wake)
    z = lerp(1.0, 1.06, es(t, K52, K60))
    push()
    translate(W / 2, H / 2)
    scale(z, z)
    translate(-W / 2, -H / 2)
    inPhone(draw, 'room', t, tilt=.008)
    pop()
    vignette(.32, '#0E1128')


# ================================================================ S06 K60 – L0: he stands at the board: her half now says 暴雪 -18℃, circled; 「她怕冷」
def s06(t, lt, dur):
    z = lerp(1.25, 1.38, es(t, K60, K64 + 1.0))
    cam(t, 545, 520, z)
    hisRoom(t, storm=1.0, circle=clamp((t - (K60 + .4)) / .8), note=pk(t, K60 + 1.5, .2), her='暴雪', herT='-18℃')
    camEnd()
    jhim(560, 1930, 40, dict(view='back', key=3, hands=dict(L=[-3.4, -6.0], R=[3.4, -6.2])))
    grade('night')


# ================================================================ S07 L0 – L3: day 0, the station in the rain; he doesn't turn around
def trainX(t):
    if t < K68:
        return 0.0
    d = t - K68
    return 210 * d * d + 30 * d


def station(t, tx, north=False, train=True):
    if north:
        return stationNorth(t, tx, train)
    gradRect(-400, -400, W + 800, H + 800, ['#4E5878', '#7A839C', '#9AA0B0'])
    # far side: fence + city blocks with lit windows (revealed when the train leaves)
    for i in range(7):
        bx = -40 + i * 170
        bh = 220 + hash1(i * 3) * 160
        paint(rectPts(bx, 640 - bh, 150, bh + 300), wash='#4A5270', ink=None)
        for r in range(int(bh / 60)):
            for c in range(3):
                if hash1(i * 31 + r * 7 + c) > .45:
                    flatRect(bx + 18 + c * 44, 640 - bh + 24 + r * 60, 22, 26, '#FFD27A', .8)
    for i in range(30):
        flatRect(-40 + i * 40, 820, 4, 120, '#3A405A', .9)
    flatRect(-400, 860, W + 800, 6, '#3A405A', .9)
    # the train
    boilSeed('train')
    x0 = -60 + tx
    paint(rrPts(x0, 470, 1260, 450, 30), wash='#E8E4D2', fill='#D6D0BA', fillOp=80, ink=INK, sw=1.0)
    flatRect(x0 + 10, 790, 1240, 34, '#3F7F6A', .95)
    flatRect(x0 + 10, 832, 1240, 10, '#E9A23B', .95)
    for i in range(4):
        wx = x0 + 120 + i * 300
        paint(rrPts(wx, 560, 230, 200, 16), wash='#5A6888', fill='#3E4A6C', fillOp=90, ink=INK, sw=.7)
    paint(rrPts(x0 + 1150, 540, 100, 330, 10), wash='#D6D0BA', ink=INK, sw=.7)
    text('K1314', x0 + 620, 520, 34, '#3F7F6A', face=WK, shadow=False)
    # her in the second window, hugging his yellow umbrella
    wx = x0 + 120
    G.c.save()
    G.c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(wx, 560, 230, 200), 16, 16), True)
    glow(wx + 115, 640, 200, '#FFD9A0', .45)
    jher(wx + 115, 955, 20, dict(ex=dict(eyes='teary', mouth='sad', brows='sad', lookX=.7, tears=es(t, K68, K68 + 1.5)), key=4))
    boilSeed('umb')
    paint([[wx + 150, 772], [wx + 178, 772], [wx + 214, 640], [wx + 206, 612], [wx + 196, 610], [wx + 186, 640]], wash='#F2C14E', ink=INK, sw=.6)
    for j in range(2):
        G.c.drawLine(wx + 162 + j * 10, 770, wx + 198 + j * 4, 630, skia.Paint(AntiAlias=True, Color=skcol('#C9962C', .8), StrokeWidth=2))
    G.c.restore()
    paint(rrPts(wx, 560, 230, 200, 16), wash=None, ink=INK, sw=.7)
    for i in range(5):                                                     # rain on the window glass
        G.c.drawLine(wx + 30 + i * 42, 570 + 20 * hash1(i), wx + 26 + i * 42, 610 + 60 * hash1(i + 3),
                     skia.Paint(AntiAlias=True, Color=skcol('#E6F0FA', .5), StrokeWidth=2))
    # wheels / track shadow
    flatRect(-400, 900, W + 800, 70, '#2A2E40', .95)
    # platform
    gradRect(-400, 960, W + 800, 900, ['#7E8496', '#9AA0AE'])
    flatRect(-400, 975, W + 800, 18, '#E9C84A', .95)
    for i in range(6):
        boilSeed(f'pud{i}')
        px, py = 120 + i * 190 + 40 * hash1(i), 1110 + 260 * hash1(i * 3)
        paint(ellPts(px, py, 90, 18, 18), wash='#B9C6DA', washOp=120, ink=None)
    splashes(t, -20, W + 20, 1180, 18, .5)
    splashes(t + .5, -20, W + 20, 1440, 14, .45, 21)
    # canopy + hanging lamps + the sign
    flatRect(-400, -400, W + 800, 600, '#2C3048', 1.0)
    flatRect(-400, 190, W + 800, 16, '#1E2236', 1.0)
    for lx in (180, 540, 900):
        G.c.drawLine(lx, 200, lx, 250, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=3))
        glow(lx, 270, 170, '#FFD27A', .55)
        paint(ellPts(lx, 262, 34, 16, 14), wash='#FFE7A8', ink=INK, sw=.5)
    boilSeed('sign')
    paint(rrPts(320, 300, 440, 120, 12), wash='#2F4A7A', ink=INK, sw=.8)
    text('开往  北方', 540, 342, 46, '#FFFDF6', face=WK, shadow=False)
    text('K1314  19:20  正点', 540, 392, 28, '#FFD27A', face=WK, shadow=False)
    for sx in (360, 720):
        G.c.drawLine(sx, 206, sx, 300, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=3))


def s07(t, lt, dur):
    t0 = t - lt
    cam(t, W / 2, H / 2 - 10, lerp(1.0, 1.05, es(t, t0, t0 + dur)))
    tx = trainX(t)
    station(t, tx)
    ph = t * 1.05
    ex = dict(eyes='teary' if t < K68 + .2 else 'closed', mouth='flat' if t < K68 else 'sad', brows='sad',
              tears=es(t, K68, K68 + 1.2), blush=.6)
    if t > L0_ + 4.2:
        ex = dict(eyes='teary', mouth='sad', brows='sad', tears=1.0, blush=.6)
    s = 1.0 + .05 * es(t, L0_, L0_ + 7)
    jhim(720, 1232, 30 * s, dict(legs='walk', ph=ph, wet=1.0, guitar=True, ex=ex, key=5))
    rain(t, -60, -100, W + 60, H + 50, 170, .55, .16, 1700, 3)
    camEnd()
    grade('past', .9)
    nameCard(180 + tx, 482, '她 · 去北方读研', '带走了他的黄伞', es(t, L0_ + .3, L0_ + .8) * (1 - es(t, K68 + 1.4, K68 + 1.8)), -.03, 'nc_her', '#CC3B42')
    nameCard(430, 640, '他 · 没有回头', '淋着雨走回去', es(t, K68 + 1.6, K68 + 2.1) * (1 - es(t, L0_ + 6.6, L0_ + 7.0)), .04, 'nc_him2')


from common import LY as _LY
L0_ = _LY[0][0]
