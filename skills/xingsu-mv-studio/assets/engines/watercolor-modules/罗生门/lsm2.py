# lsm2.py: 《罗生门》 scenes for chorus 1 → the end: the rainy street (memory), the two apartment doors (south 502 / north 302),
# the train seat and the train outside (rain ↔ snow), two trains passing, the ticket drawer, the map, city wides, the north station,
# and the extra phone screens (typing, call, booking, notes, notifications, voice message). Vertical 2:3, canvas 1080x1620.
import math
from eng import *
import eng
from couple import jhim, jher, HIM, HER
from lsm import *

OLDHIM = dict(HIM, name='oldhim', hair='#C9C6CF', hairLt='#E6E3EA', coat='#7A7F8E', coatDk='#5A5E6C', coatLt='#A4A9B6',
              skin='#F0C8AA', pants='#4E4A44', pantsDk='#363330')
OLDHER = dict(HER, name='oldher', hair='#D4D0D8', hairLt='#EEEBF0', coat='#B88A9A', coatDk='#94687A', coatLt='#D8B2BE',
              skirt='#5E5068', skirtDk='#463B50', scarf=None)


# ================================================================ the rainy street in the south (memories + his night walk)
def rainStreet(t, frozen=False, rainA=.55, lampK=1.0):
    gradRect(-400, -400, W + 800, H + 800, ['#2A3150', '#3C4468', '#5A5F7E'])
    # far buildings
    for i in range(6):
        bx, bh = -60 + i * 200, 380 + hash1(i * 7) * 220
        paint(rectPts(bx, 760 - bh, 180, bh + 200), wash='#3A4062', ink=None)
        for r in range(int(bh / 70)):
            for c in range(3):
                if hash1(i * 17 + r * 5 + c) > .5:
                    flatRect(bx + 22 + c * 52, 760 - bh + 30 + r * 70, 26, 30, '#FFD27A', .6)
    # shopfronts
    boilSeed('shops')
    paint(rectPts(-40, 640, 560, 420), wash='#5A4A5E', ink=INK, sw=.8)
    paint(rectPts(540, 640, 600, 420), wash='#4A5A66', ink=INK, sw=.8)
    glow(250, 880, 360, '#FFE7A8', .55 * lampK)
    paint(rectPts(20, 760, 440, 300), wash='#FFF1C8', fill='#FFE29A', fillOp=90, ink=INK, sw=.7)
    for j in range(3):
        flatRect(40, 800 + j * 70, 400, 8, '#C9A27A', .8)
        for k in range(8):
            flatRect(50 + k * 48, 770 + j * 70, 30, 28, ['#E9585E', '#5D8FC9', '#7FB08A', '#E9A23B'][(j + k) % 4], .8)
    paint(rrPts(30, 670, 420, 74, 8), wash='#3F7F6A', ink=INK, sw=.6)
    text('24小时 便利店', 240, 707, 40, '#FFFDF6', face=WK, shadow=False)
    glow(840, 860, 300, '#FFB070', .45 * lampK)
    paint(rectPts(580, 780, 520, 280), wash='#F3D9B8', fill='#E9C08A', fillOp=70, ink=INK, sw=.7)
    paint(rrPts(600, 670, 460, 80, 8), wash='#B0403E', ink=INK, sw=.6)
    text('老街 面馆', 830, 710, 42, '#FFF3E2', face=WK, shadow=False)
    for k in range(4):
        paint(ellPts(640 + k * 120, 800, 26, 34, 12), wash='#E9585E', ink=INK, sw=.4)      # red lanterns
        glow(640 + k * 120, 800, 50, '#FF8A6A', .35)
    # awning edge + lamp post
    flatRect(-40, 1050, W + 80, 26, '#2E2A38', 1.0)
    paint(rectPts(985, 520, 16, 700), wash='#3A3346', ink=INK, sw=.6)
    glow(990, 520, 200, '#FFD27A', .6 * lampK)
    paint(ellPts(990, 520, 36, 18, 14), wash='#FFE7A8', ink=INK, sw=.5)
    # wet pavement with reflections
    gradRect(-400, 1076, W + 800, 900, ['#3E4460', '#566080'])
    for (rx, col, ww) in ((240, '#FFE7A8', 380), (830, '#FFB070', 420), (990, '#FFD27A', 60)):
        for j in range(6):
            G.c.drawRect(skia.Rect.MakeXYWH(rx - ww / 2 + 30 * hash1(j + rx), 1110 + j * 46, ww * (.8 - j * .1), 10),
                         skia.Paint(AntiAlias=True, Color=skcol(col, .22 - j * .03)))
    if frozen:
        for i in range(140):
            x, y = hash1(i * 3) * W, hash1(i * 7) * 1500
            G.c.drawLine(x, y, x - 5, y - 24, skia.Paint(AntiAlias=True, Color=skcol('#FFF3D6', .7), StrokeWidth=3, StrokeCap=skia.Paint.kRound_Cap))
    else:
        splashes(t, -20, W + 20, 1200, 16, .45)
        splashes(t + .4, -20, W + 20, 1450, 12, .4, 31)


# ================================================================ apartment door landings: south 502 (rain), north 302 (snow)
def doorScene(t, city='north', light='night', sill=0.0, note=0.0, noteTxt=('示例歌词占位文字？', '我在门口。'), doorOpen=0.0, clear=False):
    north = city == 'north'
    if north:
        gradRect(-400, -400, W + 800, H + 800, ['#E7E0D2', '#D9D0BE'] if light != 'night' else ['#5A5A72', '#6E6A80'])
    else:
        gradRect(-400, -400, W + 800, H + 800, ['#B8C8B8', '#A8B8A8'] if light != 'night' else ['#4A5A58', '#5A6A66'])
    # lower wall band (south: green paint; north: brown), small ads stuck on the south wall
    flatRect(-400, 900, W + 800, 500, '#6E8A70' if not north else '#8A6A54', .9)
    flatRect(-400, 896, W + 800, 8, INK, .5)
    if not north:
        for (ax, ay, at) in ((120, 960, '开锁'), (260, 1010, '通下水道'), (140, 1080, '搬家')):
            paint(rectPts(ax - 50, ay - 26, 100 + len(at) * 6, 52), wash='#F3F0E6', ink=None)
            text(at, ax + len(at) * 3, ay, 26, '#C0392B', face=WK, shadow=False, a=.8)
    # stairwell window (upper left): weather outside
    boilSeed('swin' + city)
    paint(rectPts(80, 220, 300, 380), wash='#2F3A5A' if light == 'night' else ('#B9C9DE' if north else '#8C9AB0'), ink=INK, sw=.9)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(84, 224, 292, 372))
    if clear:
        gradRect(84, 224, 292, 372, ['#9FC4F0', '#E6F0FA'])
        G.c.drawCircle(300, 300, 40, skia.Paint(AntiAlias=True, Color=skcol('#FFE7A8')))
    elif north:
        snow(t, 80, 200, 380, 600, 30, .95, 60, 13, 3, 7)
    else:
        rain(t, 80, 200, 380, 600, 40, .55, .15, 1400, 17)
    G.c.restore()
    G.c.drawLine(230, 220, 230, 600, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=5))
    G.c.drawLine(80, 410, 380, 410, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=5))
    if north and sill > .01:
        paint([[74, 600], [386, 600], [380, 600 - 30 * sill], [230, 600 - 44 * sill], [80, 600 - 28 * sill]], wash='#FFFFFF', ink=INK, sw=.5)
    # ceiling bulb
    G.c.drawLine(560, -20, 560, 110, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=3))
    glow(560, 140, 300 if light == 'night' else 150, '#FFE7A8', .6 if light == 'night' else .25)
    paint(ellPts(560, 135, 26, 30, 14), wash='#FFF1C8', ink=INK, sw=.5)
    # the door
    dx0, dy0, dw, dh = 520, 380, 360, 820
    boilSeed('door' + city)
    paint(rectPts(dx0 - 26, dy0 - 26, dw + 52, dh + 26), wash='#5E5A5A', ink=INK, sw=.8)
    if doorOpen > .01:
        flatRect(dx0, dy0, dw, dh, '#2A2420', 1.0)
        glow(dx0 + dw / 2, dy0 + dh / 2, 300, '#FFD9A0', .4 * doorOpen)
    dcol = '#8E3A34' if north else '#4E6A86'
    paint(rectPts(dx0, dy0, dw * (1 - .7 * doorOpen), dh), wash=dcol, fill=mixCol(dcol, INK, .3), fillOp=90, ink=INK, sw=.8)
    if doorOpen < .3:
        for (py, ph) in ((dy0 + 60, 300), (dy0 + 420, 330)):
            paint(rectPts(dx0 + 40, py, dw - 80, ph), wash=None, ink=mixCol(dcol, INK, .5), sw=.5)
        paint(rrPts(dx0 + dw - 70, dy0 + 420, 26, 80, 8), wash='#C9A24A', ink=INK, sw=.5)
        paint(rrPts(dx0 + dw / 2 - 60, dy0 - 10 + 20, 120, 54, 6), wash='#E9E2D2', ink=INK, sw=.5)
        text('302' if north else '502', dx0 + dw / 2, dy0 + 37, 36, INK, face=WK, shadow=False)
        if north:
            paint(ellPts(dx0 + 80, dy0 + 200, 22, 22, 12), wash='#FFFFFF', ink=INK, sw=.4)      # snowman sticker
            paint(ellPts(dx0 + 80, dy0 + 168, 15, 15, 12), wash='#FFFFFF', ink=INK, sw=.4)
            paint(rectPts(dx0 + 66, dy0 + 178, 28, 6), wash='#CC3B42', ink=None)
        else:
            paint(rectPts(dx0 + 50, dy0 + 140, 110, 150), wash='#E9585E', ink=INK, sw=.5)      # 福 on his door
            text('福', dx0 + 105, dy0 + 215, 70, '#FFE08A', face=WK, shadow=False, rot=math.pi / 4)
    if note > .01:
        push()
        translate(dx0 + dw / 2 - 20, dy0 + 330)
        rotate(-.05)
        G.c.saveLayerAlpha(None, int(255 * clamp(note * 3)))
        paint(rectPts(-150, -80, 300, 160), wash='#FFE58A', ink=INK, sw=.5)
        n = len(noteTxt[0]) + len(noteTxt[1])
        shown = int(n * clamp(note))
        l1 = noteTxt[0][:shown]
        l2 = noteTxt[1][:max(0, shown - len(noteTxt[0]))]
        text(l1, -130, -22, 34, INK, face=WK, align='left', shadow=False)
        text(l2, -130, 34, 34, INK, face=WK, align='left', shadow=False)
        G.c.restore()
        pop()
    # floor / steps going down on the left
    flatRect(-400, 1200, W + 800, 800, '#8A8478' if not north else '#9A9284', 1.0)
    flatRect(-400, 1196, W + 800, 8, INK, .5)
    paint(rrPts(dx0 + 20, 1196, dw - 40, 40, 6), wash='#7E5C46' if north else '#5E6E5A', ink=INK, sw=.5)   # doormat
    for j in range(3):
        flatRect(-400, 1300 + j * 100, 520 - j * 60 + 400, 10, '#5E584E', .5)


# ================================================================ inside the train: a window seat, the outside passing by
def trainSeat(t, outside='rain', mix=0.0, night=True, flip=False, reflection=None, clock=None, clockSpeed=0.0):
    """window seat facing the camera; window on the left (x 60–520, y 330–900); outside: 'rain' | 'snow' | 'mix' (mix 0 rain → 1 snow)"""
    gradRect(-400, -400, W + 800, H + 800, ['#3A3E58', '#4A4E68', '#56506A'] if night else ['#9AA3B8', '#B8BCC8'])
    if flip:
        push()
        translate(W, 0)
        scale(-1, 1)
    # window
    wx, wy, ww, wh = 60, 330, 470, 580
    boilSeed('twin')
    paint(rrPts(wx - 20, wy - 20, ww + 40, wh + 40, 40), wash='#C9C4B4', ink=INK, sw=.8)
    G.c.save()
    G.c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(wx, wy, ww, wh), 30, 30), True)
    m = mix if outside == 'mix' else (1.0 if outside == 'snow' else 0.0)
    sky = [mixCol('#1E2440', '#5A6890', m), mixCol('#2E3658', '#8EA0C0', m)] if night else [mixCol('#7A88A8', '#C8D4E6', m), mixCol('#9AA6BE', '#E6ECF4', m)]
    gradRect(wx, wy, ww, wh, sky)
    for i in range(8):                                      # hills and poles flowing left
        hx = wx + ((i * 140 - t * 260) % (ww + 280)) - 140
        paint(ellPts(hx, wy + wh - 120, 160, 70, 18), wash=mixCol('#2A3A3A', '#E8EEF6', m), ink=None)
    for i in range(4):
        px = wx + ((i * 190 - t * 900) % (ww + 200)) - 100
        G.c.drawRect(skia.Rect.MakeXYWH(px, wy + 120, 10, wh), skia.Paint(AntiAlias=True, Color=skcol('#1A1E2C', .8)))
        G.c.drawLine(px - 200, wy + 140, px + 200, wy + 170, skia.Paint(AntiAlias=True, Color=skcol('#1A1E2C', .5), StrokeWidth=2))
    if night:
        for i in range(6):
            lx = wx + ((i * 120 - t * 150) % (ww + 120)) - 60
            G.c.drawCircle(lx, wy + wh - 160 - 30 * hash1(i), 4, skia.Paint(AntiAlias=True, Color=skcol('#FFD27A', .8)))
    if m < .98:
        rain(t, wx, wy, wx + ww, wy + wh, 50, .5 * (1 - m), .9, 900, 23, ln=60)
    if m > .02:
        snow(t * 1.6, wx, wy, wx + ww, wy + wh, 40, .95 * m, 180, 27, 3, 7, drift=60)
    if reflection:
        G.c.saveLayerAlpha(None, 70)
        reflection()
        G.c.restore()
    G.c.restore()
    paint(rrPts(wx, wy, ww, wh, 30), wash=None, ink=INK, sw=.7)
    flatRect(wx, wy + wh * .45, ww, 6, '#9A958A', .7)
    # wall + curtain + carriage clock
    boilSeed('curtain')
    paint([[wx - 30, wy - 40], [wx + 70, wy - 40], [wx + 50, wy + wh + 40], [wx - 40, wy + wh + 40]], wash='#3F6A8A', fill='#2E5070', fillOp=90, ink=INK, sw=.6)
    if clock is not None:
        cx_, cy_ = 800, 250
        paint(ellPts(cx_, cy_, 80, 80, 28), wash='#FFFDF6', ink=INK, sw=.8)
        for k in range(12):
            an = k / 12 * TAU
            G.c.drawLine(cx_ + math.cos(an) * 64, cy_ + math.sin(an) * 64, cx_ + math.cos(an) * 72, cy_ + math.sin(an) * 72,
                         skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=3))
        mn = clock + t * clockSpeed
        for (ln_, an, wd) in ((40, (mn / 720) * TAU - math.pi / 2, 6), (60, (mn / 60) * TAU - math.pi / 2, 4)):
            G.c.drawLine(cx_, cy_, cx_ + math.cos(an) * ln_, cy_ + math.sin(an) * ln_, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=wd,
                                                                                              StrokeCap=skia.Paint.kRound_Cap))
    if flip:
        pop()


def seatBack(x, y_seat, u, col='#3E5A8A'):
    boilSeed('tseat')
    paint(rrPts(x - 6.4 * u, y_seat - 12.5 * u, 12.8 * u, 12.6 * u, 24), wash=col, fill=mixCol(col, INK, .3), fillOp=80, ink=INK, sw=.8)
    paint(rrPts(x - 5.0 * u, y_seat - 12.0 * u, 10.0 * u, 2.4 * u, 10), wash='#F3F0E6', ink=INK, sw=.5)
    paint(rrPts(x - 6.6 * u, y_seat - .4 * u, 13.2 * u, 1.4 * u, 8), wash=mixCol(col, INK, .15), ink=INK, sw=.6)


def trainTable(y, x0=40, x1=1040):
    boilSeed('ttable')
    paint(rrPts(x0, y - 10, x1 - x0, 26, 8), wash='#D9D2C2', fill='#BDB6AA', fillOp=80, ink=INK, sw=.7)


# ================================================================ the train outside: on a long bridge; weather changes along the way
def trainOutside(t, mix=0.0, night=False, x=0.0, dawn=0.0):
    sky0 = mixCol('#6A7898', '#B8C6DC', mix)
    sky1 = mixCol('#9AA6BE', '#E8EEF6', mix)
    if night:
        sky0, sky1 = mixCol('#141830', '#2A3050', mix), mixCol('#2A3050', '#4A5878', mix)
    gradRect(-400, -400, W + 800, H + 800, [sky0, sky1])
    if dawn > .01:
        gradRect(-400, 300, W + 800, 700, ['#F7B27A', '#F4D2A8'], a=dawn * .6)
    for i in range(5):                                  # mountains, snowy as mix grows
        mx_ = -200 + i * 320
        pts = [[mx_ - 260, 980], [mx_, 560 + 80 * hash1(i)], [mx_ + 260, 980]]
        paint(pts, wash=mixCol('#4A5A6A', '#C8D2E0', mix), ink=None)
        if mix > .3:
            paint([[mx_ - 70, 680 + 80 * hash1(i)], [mx_, 560 + 80 * hash1(i)], [mx_ + 70, 680 + 80 * hash1(i)]], wash='#FFFFFF', washOp=int(255 * mix), ink=None)
    flatRect(-400, 980, W + 800, 900, mixCol('#3E5A66', '#DCE4EE', mix), 1.0)          # water / snow field
    # bridge
    flatRect(-400, 900, W + 800, 30, '#4A4458', 1.0)
    for i in range(9):
        bx = -40 + i * 140
        paint([[bx, 930], [bx + 30, 930], [bx + 40, 1100], [bx - 10, 1100]], wash='#4A4458', ink=None)
    # the train (long, moving right to left at x)
    boilSeed('trainout')
    for c in range(4):
        cx0 = x + c * 520 - 200
        paint(rrPts(cx0, 720, 500, 180, 26), wash='#E8E4D2', ink=INK, sw=.8)
        flatRect(cx0 + 8, 840, 484, 22, '#3F7F6A', .95)
        for k in range(5):
            wl = '#FFE7A8' if night else '#5A6888'
            paint(rrPts(cx0 + 30 + k * 92, 750, 70, 60, 10), wash=wl, ink=INK, sw=.5)
    if mix < .98:
        rain(t, -60, -60, W + 60, H, 120, .45 * (1 - mix), .2, 1500, 41)
    if mix > .02:
        snow(t, -60, -60, W + 60, H, 110, .9 * mix, 110, 43, 3, 8, drift=40)


def twoTrains(t, k):
    """night: two trains pass on a bridge in opposite directions; their windows line up at k = .5"""
    trainOutside(t, .5, night=True, x=lerp(900, -1300, k))
    boilSeed('train2')
    x2 = lerp(-1700, 700, k)
    for c in range(4):
        cx0 = x2 + c * 520 - 200
        paint(rrPts(cx0, 560, 500, 170, 26), wash='#D9D2C0', ink=INK, sw=.8)
        flatRect(cx0 + 8, 676, 484, 20, '#8E3A34', .95)
        for kk in range(5):
            paint(rrPts(cx0 + 30 + kk * 92, 588, 70, 56, 10), wash='#FFE7A8', ink=INK, sw=.5)


# ================================================================ desk drawer full of unused tickets, the map with a string
def deskDrawer(t, n=11, k=1.0):
    gradRect(-400, -400, W + 800, H + 800, ['#2E2A44', '#3A3450'])
    glow(540, 600, 600, '#FFC07A', .35)
    boilSeed('drawerdesk')
    paint(rectPts(-60, 380, W + 120, 120), wash='#9A6A44', fill='#7E5434', fillOp=80, ink=INK, sw=.9)
    paint(rectPts(-60, 500, W + 120, 560), wash='#7E5434', ink=INK, sw=.9)
    dy = lerp(0, 260, ease(k))
    paint([[120, 560 + dy], [960, 560 + dy], [1000, 1080 + dy], [80, 1080 + dy]], wash='#5E3E28', ink=INK, sw=.8)
    paint([[150, 580 + dy], [930, 580 + dy], [960, 1040 + dy], [120, 1040 + dy]], wash='#3E2A1E', ink=None)
    for i in range(n):
        q = i / max(1, n - 1)
        ticket(300 + q * 480, 760 + dy + 60 * math.sin(q * 3.1), 300, -.35 + q * .7, '南方 → 北方', f'K1314 · 未使用', key=f'dt{i}')
    paint(rrPts(480, 1050 + dy, 120, 30, 10), wash='#C9A24A', ink=INK, sw=.5)


def mapWall(t, k=1.0):
    gradRect(-400, -400, W + 800, H + 800, ['#2E2A44', '#3A3450'])
    boilSeed('map')
    paint(rectPts(80, 240, 920, 1100), wash='#F2E8D2', fill='#E2D4B6', fillOp=80, ink=INK, sw=.9)
    land = [[200, 520], [380, 360], [620, 330], [840, 420], [900, 640], [820, 860], [860, 1060], [700, 1220], [460, 1260], [300, 1120], [220, 900], [160, 700]]
    paint(throughClosed(land, 4), wash='#CFE0C2', fill='#B6CFA4', fillOp=80, ink=INK, sw=.6)
    for i in range(5):
        inkLine([[200 + i * 140, 300], [220 + i * 140, 1300]], .25, '#B9A98A', 'inkfine', .2)
    north, south = (700, 470), (560, 1130)
    for (px, py, lab, col) in ((north[0], north[1], '她 · 北方', '#CC3B42'), (south[0], south[1], '我 · 南方', '#3B5B98')):
        paint(ellPts(px, py, 20, 20, 12), wash=col, ink=INK, sw=.5)
        text(lab, px + (110 if px > 600 else -110), py, 36, INK, face=WK, shadow=False)
    kk = ease(clamp(k))
    ex, ey = lerp(south[0], north[0], kk), lerp(south[1], north[1], kk)
    inkLine([[south[0], south[1]], [lerp(south[0], ex, .5) + 40, lerp(south[1], ey, .5)], [ex, ey]], 1.1, '#E9585E', 'ink', .5)
    if k > .9:
        text('2875 公里', 760, 800, 54, '#E9585E', face=WK, stroke='#FFFDF6', strokeW=8, shadow=False, a=clamp((k - .9) * 10))


# ================================================================ city wides, north station
def cityWide(t, city='north', tod='dawn', fig=None, fx=540, fy=1260, fu=6):
    north = city == 'north'
    if north:
        gradRect(-400, -400, W + 800, H + 800, ['#8E9CC0', '#C9D2E6', '#F2D9C8'] if tod == 'dawn' else ['#3A4468', '#6A7498'])
    else:
        gradRect(-400, -400, W + 800, H + 800, ['#4A5470', '#6E7690', '#8A8EA2'])
    for layer, (base, col, hmax) in enumerate(((900, '#7A86A8' if north else '#4E5672', 520), (1100, '#5E6A8C' if north else '#3E4660', 640))):
        for i in range(7):
            bx = -80 + i * 170 + layer * 60
            bh = 260 + hash1(i * 5 + layer * 9) * hmax
            paint(rectPts(bx, base - bh, 150, bh + 600), wash=col, ink=None)
            if north:
                paint(rectPts(bx - 6, base - bh - 14, 162, 18), wash='#FFFFFF', ink=None)
            for r in range(int(bh / 70)):
                for c in range(3):
                    if hash1(i * 13 + r * 3 + c + layer * 99) > .55:
                        flatRect(bx + 20 + c * 44, base - bh + 26 + r * 70, 22, 26, '#FFD27A', .55)
    flatRect(-400, 1180, W + 800, 900, '#F3F6FB' if north else '#3E4660', 1.0)
    if north:
        snow(t, -60, -60, W + 60, H, 140, .9, 80, 51, 2.5, 7)
    else:
        rain(t, -60, -60, W + 60, H, 160, .5, .18, 1600, 53)
    if fig:
        fig(fx, fy, fu)


def stationNorth(t, tx, train=True):
    gradRect(-400, -400, W + 800, H + 800, ['#8E9CC0', '#C2CCE0', '#E6ECF4'])
    for i in range(7):
        bx, bh = -40 + i * 170, 220 + hash1(i * 3 + 5) * 160
        paint(rectPts(bx, 640 - bh, 150, bh + 300), wash='#7A86A8', ink=None)
        paint(rectPts(bx - 5, 640 - bh - 12, 160, 16), wash='#FFFFFF', ink=None)
    if train:
        boilSeed('trainN')
        x0 = -60 + tx
        paint(rrPts(x0, 470, 1260, 450, 30), wash='#E8E4D2', ink=INK, sw=1.0)
        flatRect(x0 + 10, 790, 1240, 34, '#3F7F6A', .95)
        for i in range(4):
            paint(rrPts(x0 + 120 + i * 300, 560, 230, 200, 16), wash='#8E9CB8', ink=INK, sw=.7)
        paint(rectPts(x0, 462, 1260, 22), wash='#FFFFFF', ink=None)                     # snow on the roof
        text('K1314', x0 + 620, 520, 34, '#3F7F6A', face=WK, shadow=False)
    flatRect(-400, 900, W + 800, 70, '#4A4E60', .95)
    gradRect(-400, 960, W + 800, 900, ['#E6ECF4', '#F6F8FC'])
    flatRect(-400, 975, W + 800, 18, '#E9C84A', .9)
    flatRect(-400, -400, W + 800, 600, '#3A4058', 1.0)
    flatRect(-400, 186, W + 800, 22, '#FFFFFF', 1.0)
    for lx in (180, 540, 900):
        glow(lx, 270, 150, '#FFE7A8', .4)
        paint(ellPts(lx, 262, 34, 16, 14), wash='#FFE7A8', ink=INK, sw=.5)
    boilSeed('signN')
    paint(rrPts(330, 300, 420, 110, 12), wash='#2F4A7A', ink=INK, sw=.8)
    text('北方站', 540, 340, 46, '#FFFDF6', face=WK, shadow=False)
    text('-18℃  大雪', 540, 386, 28, '#BFE3F2', face=WK, shadow=False)
    snow(t, -60, 200, W + 60, H, 120, .95, 90, 61, 3, 8)


def musicNotes(t, x, y, n=4, a=1.0):
    for i in range(n):
        ph = frac(t * .5 + i / n)
        nx = x + 40 * math.sin(ph * 5 + i) + i * 30
        ny = y - ph * 300
        al = a * math.sin(ph * math.pi)
        push()
        translate(nx, ny)
        rotate(math.sin(t + i) * .2)
        G.c.drawCircle(0, 0, 12, skia.Paint(AntiAlias=True, Color=skcol('#FFE7A8', al)))
        G.c.drawLine(10, 0, 10, -44, skia.Paint(AntiAlias=True, Color=skcol('#FFE7A8', al), StrokeWidth=4))
        G.c.drawLine(10, -44, 26, -34, skia.Paint(AntiAlias=True, Color=skcol('#FFE7A8', al), StrokeWidth=4))
        pop()


def breath(t, x, y, a=.6, s=1.0):
    for i in range(3):
        ph = frac(t * .7 + i / 3)
        G.c.drawCircle(x + ph * 60 * s, y - ph * 30 * s, (10 + ph * 26) * s, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', a * (1 - ph) * .7)))


# ================================================================ more phone screens (full canvas 1080x1620; place with inPhone)
def appBg(th='now'):
    T = THEMES[th]
    gradRect(-400, -400, W + 800, H + 800, [T['bg'], T['bg2']])


def typingScreen(t, typed, sent=(), withdrawn=False, clock='02:10', base=None, caret=True):
    """chat page with the input box being typed into; sent = extra messages already sent"""
    items = list(base or [])
    for s_ in sent:
        items.append(('me', s_))
    if withdrawn:
        items = items[:-1] + [('sep', '你撤回了一条消息')]
    chatScreen(t, items, 'now', clock, batt=.18, bottom=1250 if typed else 1410)
    if typed:
        lines = wrapText(typed, 13)[-3:]
        h = 70 + 54 * len(lines)
        G.c.drawRect(skia.Rect.MakeXYWH(-10, 1440 - h + 70, W + 20, h + 200), skia.Paint(AntiAlias=True, Color=skcol('#F7F8FB')))
        G.c.drawRoundRect(skia.Rect.MakeXYWH(110, 1460 - h + 70, 720, h - 10), 16, 16, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF')))
        for j, l in enumerate(lines):
            text(l, 136, 1500 - h + 70 + j * 54, 40, '#1F2233', face=WK, align='left', shadow=False)
        if caret and frac(t * 2) < .6:
            lw = textW(lines[-1], 40, WK)
            flatRect(140 + lw, 1478 - h + 70 + (len(lines) - 1) * 54, 4, 44, '#3B7BD9')
        paint(rrPts(850, 1462, 140, 70, 14), wash='#7FC97A', ink=None)
        text('发送', 920, 1497, 36, '#FFFFFF', face=WK, shadow=False)


def callScreen(t, state='calling', k=0.0):
    gradRect(-400, -400, W + 800, H + 800, ['#2A2E48', '#3E3A5E', '#5A4A6E'])
    statusBar('09:06', THEMES['now'], dark=True, batt=.06)
    avatarHer(W / 2, 470, 120)
    text('她', W / 2, 680, 64, '#FFFFFF', face=WK, shadow=False)
    if state == 'calling':
        dots = '.' * (1 + int(t * 3) % 3)
        text('正在呼叫' + dots, W / 2, 760, 40, '#C9C6DA', face=WK, shadow=False)
        for i in range(3):
            ph = frac(t * .8 + i / 3)
            G.c.drawCircle(W / 2, 470, 130 + ph * 160, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4,
                                                                  Color=skcol('#FFFFFF', .4 * (1 - ph))))
    else:
        text('您拨打的电话已关机', W / 2, 760, 46, '#FFB2A6', face=WK, shadow=False, a=clamp(k * 4))
    G.c.drawCircle(W / 2, 1120, 70, skia.Paint(AntiAlias=True, Color=skcol('#E9585E')))
    G.c.drawLine(W / 2 - 34, 1120, W / 2 + 34, 1120, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF'), StrokeWidth=12, StrokeCap=skia.Paint.kRound_Cap))


def bookingScreen(t, k_tap=0.0, k_ok=0.0):
    appBg('now')
    flatRect(-10, -10, W + 20, 420, '#3B7BD9', 1.0)
    statusBar('03:31', THEMES['now'], dark=True, batt=.15)
    text('购票', W / 2, 130, 46, '#FFFFFF', face=WK, shadow=False)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(60, 230, 960, 420), 30, 30, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF')))
    text('南方', 230, 380, 72, '#1F2233', face=WK, shadow=False)
    text('北方', 850, 380, 72, '#1F2233', face=WK, shadow=False)
    inkLine([[400, 380], [680, 380]], 1.0, '#3B7BD9', 'ink', 0)
    paint([[660, 360], [690, 380], [660, 400]], wash='#3B7BD9', ink=None)
    text('K1314', W / 2, 330, 40, '#3B7BD9', face=WK, shadow=False)
    text('05:40 出发  ·  硬座  ·  ¥368', W / 2, 500, 38, '#4A4458', face=WK, shadow=False)
    text('11月21日 周六', W / 2, 580, 34, '#8A90A2', face=WK, shadow=False)
    for i, (lab, val) in enumerate((('乘车人', '他'), ('余票', '仅剩 3 张'))):
        y = 740 + i * 110
        G.c.drawRoundRect(skia.Rect.MakeXYWH(60, y, 960, 90), 20, 20, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF')))
        text(lab, 110, y + 45, 36, '#8A90A2', face=WK, align='left', shadow=False)
        text(val, 970, y + 45, 36, '#1F2233', face=WK, align='right', shadow=False)
    sc = 1 - .08 * math.sin(clamp(k_tap) * math.pi)
    push()
    translate(W / 2, 1180)
    scale(sc, sc)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-400, -60, 800, 120), 60, 60, skia.Paint(AntiAlias=True, Color=skcol('#F2A33A')))
    text('立即购买', 0, 0, 50, '#FFFFFF', face=WK, shadow=False)
    pop()
    if k_ok > .01:
        a = clamp(k_ok * 3)
        flatRect(-10, -10, W + 20, H + 20, '#000000', .35 * a)
        sc = lerp(1.6, 1.0, easeOut(clamp(k_ok * 2.5)))
        push()
        translate(W / 2, 800)
        rotate(-.12)
        scale(sc, sc)
        G.c.drawCircle(0, 0, 210, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=12, Color=skcol('#E9585E', a)))
        G.c.drawCircle(0, 0, 180, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skcol('#E9585E', a)))
        text('出票成功', 0, -20, 70, '#E9585E', face=WK, shadow=False, a=a)
        text('第 12 张', 0, 60, 44, '#E9585E', face=WK, shadow=False, a=a)
        pop()


def notesScreen(t, lines, k=1.0, title='她的脾气'):
    gradRect(-400, -400, W + 800, H + 800, ['#FFF8E0', '#FBEFC8'])
    statusBar('06:58', THEMES['now'], batt=.1)
    text('备忘录', 120, 130, 40, '#C9962C', face=WK, align='left', shadow=False)
    text(title, 90, 250, 70, '#1F2233', face=WK, align='left', shadow=False)
    for i in range(22):
        flatRect(80, 330 + i * 70, 920, 2, '#E8D9A8', 1.0)
    shown = k * len(lines)
    for i, l in enumerate(lines):
        if i < int(shown):
            text(l, 90, 360 + i * 70 + 4, 40, '#3A3346', face=WK, align='left', shadow=False)
        elif i == int(shown):
            part = l[:int(len(l) * frac(shown))]
            text(part, 90, 360 + i * 70 + 4, 40, '#3A3346', face=WK, align='left', shadow=False)
            if frac(t * 2) < .6:
                flatRect(96 + textW(part, 40, WK), 340 + i * 70, 4, 44, '#C9962C')


def notifStack(t, items, k=1.0, clock='08:47', boot=1.0):
    """lock screen after the phone boots: notifications pour in one by one (k = 0..1 of len(items))"""
    gradRect(-400, -400, W + 800, H + 800, ['#2A2E48', '#3E3A5E', '#5A4A6E'])
    statusBar('', THEMES['now'], dark=True, batt=.08)
    text(clock, W / 2, 300, 150, '#FFFFFF', face=WK, shadow=False, a=.95)
    n = min(len(items), int(k * len(items) + 1e-6))
    for i in range(n):
        j = n - 1 - i
        y = 470 + j * 132
        if y > 1380:
            continue
        age_ = k * len(items) - i
        dx = (1 - easeOut(clamp(age_ * 4))) * 120
        G.c.drawRoundRect(skia.Rect.MakeXYWH(70 + dx, y, 800, 116), 28, 28, skia.Paint(AntiAlias=True, Color=skcol('#F4F2F8', .94)))
        paint(rrPts(98 + dx, y + 26, 64, 64, 14), wash='#3B5B98', ink=None)
        text('他', 130 + dx, y + 58, 36, '#FFFFFF', face=WK, shadow=False)
        text(items[i][0], 190 + dx, y + 36, 26, '#6A6478', face=WK, align='left', shadow=False)
        text(items[i][1], 190 + dx, y + 80, 38, '#1F2233', face=WK, align='left', shadow=False)
    if boot < .99:
        flatRect(-10, -10, W + 20, H + 20, '#05060C', 1 - boot)


def voiceScreen(t, words, k=0.0, holding=True, who='her', clock='08:52', base=None, played=None):
    """voice message: hold-to-talk waveform + live voice-to-text of `words`; played = (bubble shown with text) for the receiver"""
    items = list(base or [])
    chatScreen(t, items, 'now', clock, title='他' if who == 'her' else '她', sub='南方 · 暴雨' if who == 'her' else '北方 · 大雪', batt=.3,
               bottom=820 if holding else 1410)
    if holding:
        flatRect(-10, 850, W + 20, 900, '#1C1E2C', .88)
        for i in range(36):
            hh = 20 + 80 * abs(math.sin(t * 9 + i * .7)) * (.5 + .5 * math.sin(i * .9 + t * 3))
            flatRect(160 + i * 21, 1130 - hh / 2, 12, hh, '#7FC97A')
        shown = words[:int(len(words) * clamp(k))]
        for j, l in enumerate(wrapText(shown, 11)):
            text(l, W / 2, 910 + j * 62, 48, '#FFFFFF', face=WK, shadow=False)
        text('松开 发送', W / 2, 1210, 34, '#C9C6DA', face=WK, shadow=False)


def umbDown(u, sw, C):
    """closed umbrella hanging tip-down from the hand (itemR / itemL); never crosses the face"""
    inkLine([[0, -.2 * u], [-.6 * u, -.7 * u], [-.9 * u, -.1 * u]], .8, '#6E4A30', 'ink', .6)
    paint([[-.3 * u, .2 * u], [.3 * u, .2 * u], [.85 * u, 6.0 * u], [0, 7.2 * u], [-.85 * u, 6.0 * u]], wash='#F2C14E', fill='#E0A92A', fillOp=70, ink=INK, sw=.6)
    inkLine([[.1 * u, .5 * u], [.4 * u, 6.0 * u]], .3, '#C9962C', 'inkfine', 0)


def umbLean(x, y_seat, u):
    """closed umbrella leaning against a sitting person's right side (outside the face)"""
    boilSeed('umblean')
    paint([[x + 3.4 * u, y_seat + 2.6 * u], [x + 4.4 * u, y_seat + 2.6 * u], [x + 7.0 * u, y_seat - 9.0 * u], [x + 6.4 * u, y_seat - 9.4 * u]],
          wash='#F2C14E', fill='#E0A92A', fillOp=70, ink=INK, sw=.6)
    inkLine([[x + 6.7 * u, y_seat - 9.2 * u], [x + 6.2 * u, y_seat - 10.0 * u], [x + 5.6 * u, y_seat - 9.6 * u]], .8, '#6E4A30', 'ink', .6)
