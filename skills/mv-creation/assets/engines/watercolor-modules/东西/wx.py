# wx.py: props and sets for 《可不可以给我你的微信》 (watercolour + ink). Engine files stay untouched.
# Theme: love at first sight = 相思病; the 疑心病 detective (her) "diagnoses" him; a messenger app that is NOT any real brand
# (no logo, its own green), QR codes are random module art (not scannable).
import math
from eng import *
import eng
from clawd import *
from props import C, puff, sparkle, sparkles, floatHearts, bubble, stamp, sunburst, stripes, groundBand, tree, bush, lamp
from ch_chonghuai import rr, heart, popK, shakeAmt, phoneBody, screenClip, msgBubble, typingDots, placardSign, bobaCup, fo, \
    WENKAI, HOT, PINK, PINKDK, CREAM
from bsc import stringLights, spotlight, confetti, smokePuff, heartBalloon

APPG = '#43B873'          # the made-up messenger's accent green
APPG_DK = '#2F8C55'
UIBG = '#F2F2F2'
GREY = '#9A93A6'


def _pa(col, a=1.0, w=None):
    p = skia.Paint(AntiAlias=True, Color=skcol(col, a))
    if w:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(w)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


def line(x0, y0, x1, y1, col, a=1.0, w=2.0):
    G.c.drawLine(x0, y0, x1, y1, _pa(col, a, w))


def herD(x, y, u, o=None):
    """her in this MV: the 疑心病 detective (deerstalker with her white flower on it)"""
    her(x, y, u, o, detective=True)


def chevronL(x, y, s, col=INK, w=3.0):
    line(x + s * .4, y - s * .7, x - s * .3, y, col, 1, w)
    line(x - s * .3, y, x + s * .4, y + s * .7, col, 1, w)


# ------------------------------------------------------------------ avatars
def miniHead2(x, y, r, who='her', face='happy', key='mh'):
    """a tiny Clawd head for avatars; her wears the deerstalker"""
    base = HER if who == 'her' else ME
    o = dict(base, view='front', noShadow=True, noLegs=True, boilKey=key, aL=-1.6, aR=-1.6)
    o.update(dict(happy=dict(eyes='happy', mouth='smile', blush=.5), love=dict(eyes='heart', mouth='cat', blush=.8),
                  plain=dict(eyes='normal', mouth='smile'), shine=dict(eyes='shine', mouth='cat', blush=.4),
                  sus=dict(eyes='narrow', mouth='flat'), wink=dict(eyes=['closed', 'normal'], mouth='tongue', blush=.5)).get(face, {}))
    if who == 'her':
        o['hat'] = 'deer'
    G.c.save()
    clawd(x, y + r * (1.25 if who == 'her' else .95), r / (6.2 if who == 'her' else 5.2), o)
    G.c.restore()


def avatarBox(x, y, r, who='her', face='happy', key='av', bg=None):
    boilSeed(key + 'bx')
    paint(rrPts(x - r, y - r, 2 * r, 2 * r, r * .22), wash=bg or ('#FBE3EA' if who == 'her' else '#FCE6D6'), ink=INK, sw=.7)
    G.c.save()
    p = skia.Path()
    p.addRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), r * .22, r * .22))
    G.c.clipPath(p, skia.ClipOp.kIntersect, True)
    miniHead2(x, y + r * .18, r * .78, who, face, key)
    G.c.restore()


def unknownAvatar(x, y, r, key='uk'):
    boilSeed(key)
    paint(rrPts(x - r, y - r, 2 * r, 2 * r, r * .22), wash='#D9D5E0', ink=INK, sw=.7)
    paint(ellPts(x, y - r * .18, r * .36, r * .36, 16), wash='#B5AEC2', ink=None)
    paint(ellPts(x, y + r * .72, r * .7, r * .45, 18), wash='#B5AEC2', ink=None)
    text('?', x, y - r * .16, r * .62, '#FFFFFF', shadow=False)


# ------------------------------------------------------------------ QR code (random module art, 3 finder squares)
def qrCode(x, y, s, seed=1, col=INK, bg='#FFFFFF', center=None, a=1.0, n=21):
    """square code centred at (x, y), side s. center(cx, cy, r) draws a badge in the middle."""
    if a <= .01:
        return
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x - s / 2 - s * .06, y - s / 2 - s * .06, s * 1.12, s * 1.12), s * .06, s * .06, _pa(bg, a))
    m = s / n
    x0, y0 = x - s / 2, y - s / 2
    pa = _pa(col, a)

    def finder(cx, cy):
        G.c.drawRect(skia.Rect.MakeXYWH(x0 + cx * m, y0 + cy * m, 7 * m, 7 * m), pa)
        G.c.drawRect(skia.Rect.MakeXYWH(x0 + (cx + 1) * m, y0 + (cy + 1) * m, 5 * m, 5 * m), _pa(bg, a))
        G.c.drawRect(skia.Rect.MakeXYWH(x0 + (cx + 2) * m, y0 + (cy + 2) * m, 3 * m, 3 * m), pa)

    for i in range(n):
        for j in range(n):
            inF = (i < 8 and j < 8) or (i >= n - 8 and j < 8) or (i < 8 and j >= n - 8)
            mid = abs(i - n // 2) <= 3 and abs(j - n // 2) <= 3 and center
            if inF or mid:
                continue
            if hash1(seed * 97.1 + i * 13.7 + j * 5.3) < .48:
                G.c.drawRect(skia.Rect.MakeXYWH(x0 + i * m - .3, y0 + j * m - .3, m + .6, m + .6), pa)
    finder(0, 0)
    finder(n - 7, 0)
    finder(0, n - 7)
    if center:
        G.c.drawRoundRect(skia.Rect.MakeXYWH(x - 3.2 * m, y - 3.2 * m, 6.4 * m, 6.4 * m), m, m, _pa(bg, a))
        center(x, y, 2.8 * m)


# ------------------------------------------------------------------ the messenger app pages (inside a clipped phone screen)
def appTopBar(sx, sy, sw_, title, h=120):
    flatRect(sx, sy, sw_, h, '#EDEDED')
    line(sx, sy + h, sx + sw_, sy + h, '#D6D2DC', 1, 1.5)
    chevronL(sx + 44, sy + h * .58, 18, INK, 4)
    text(title, sx + sw_ / 2, sy + h * .58, 38, INK, shadow=False)


def statusBar(sx, sy, sw_, clock='13:14'):
    text(clock, sx + 70, sy + 26, 24, INK, shadow=False)
    for i in range(4):
        G.c.drawRect(skia.Rect.MakeXYWH(sx + sw_ - 150 + i * 10, sy + 34 - (i + 1) * 5, 6, (i + 1) * 5), _pa(INK))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(sx + sw_ - 90, sy + 16, 46, 22), 5, 5, _pa(INK, 1, 2))
    G.c.drawRect(skia.Rect.MakeXYWH(sx + sw_ - 86, sy + 20, 30, 14), _pa(APPG))


def sendButton(cx, cy, w, h, lit=0.0, press=0.0, label='发送', key='sbtn'):
    s = 1 - .08 * press
    push()
    translate(cx, cy)
    scale(s)
    if lit > .02:
        glow(0, 0, w * .9, '#B8F5CF', .55 * lit)
    boilSeed(key)
    paint(rrPts(-w / 2, -h / 2, w, h, h * .22), wash=mixCol('#BFE5CC', APPG, lit), ink=INK, sw=.9)
    text(label, 0, 0, h * .46, '#FFFFFF', shadow=False)
    pop()


def cursorArrow(x, y, s=1.0, a=1.0):
    pts = [[0, 0], [0, 44], [11, 33], [20, 52], [28, 48], [19, 30], [34, 30]]
    P = [[x + px * s, y + py * s] for px, py in pts]
    boilSeed('cur')
    paint(P, wash='#FFFFFF', washOp=255 * a, ink=INK, sw=1.0)


def caret(x, y, h, t, a=1.0):
    if frac(t * 1.7) < .55:
        flatRect(x, y - h / 2, 4, h, APPG, a)


def friendRequestPage(t, sx, sy, sw_, sh, chars=(), caretOn=True, sendLit=0.0, sendPress=0.0, who='unknown', after=None):
    """'申请添加朋友' page (needs sh >= ~930). chars = [(char, age)] typed into the verification box (age<0 = not yet)."""
    flatRect(sx, sy, sw_, sh, UIBG)
    statusBar(sx, sy, sw_)
    appTopBar(sx, sy + 50, sw_, '申请添加朋友')
    cy = sy + 190
    flatRect(sx, cy, sw_, 150, '#FFFFFF')
    if who == 'unknown':
        unknownAvatar(sx + 92, cy + 75, 52, key='ukfr')
        text('附近的她', sx + 176, cy + 52, 40, INK, align='left', shadow=False)
        text('来自：咖啡店 · 距离 3 米', sx + 176, cy + 104, 24, GREY, align='left', shadow=False, face=WENKAI)
    else:
        avatarBox(sx + 92, cy + 75, 52, 'her', 'happy', key='avfr')
        text('侦探小姐', sx + 176, cy + 52, 40, INK, align='left', shadow=False)
        text('真相只有一个', sx + 176, cy + 104, 24, GREY, align='left', shadow=False, face=WENKAI)
    text('发送添加朋友申请', sx + 36, cy + 190, 26, GREY, align='left', shadow=False, face=WENKAI)
    by = cy + 215
    flatRect(sx + 20, by, sw_ - 40, 210, '#FFFFFF')
    G.c.drawRoundRect(skia.Rect.MakeXYWH(sx + 20, by, sw_ - 40, 210), 14, 14, _pa('#D6D2DC', 1, 2))
    size = 60
    tx, ty = sx + 48, by + 66
    x = tx
    cx_, cy_ = tx, ty
    n = 0
    for i, (ch, ag) in enumerate(chars):
        if ag < 0:
            break
        if i == 6:
            x = tx
            ty += 92
        w = textW(ch, size)
        p = backOut(clamp(ag / .1))
        text(ch, x + w / 2, ty - 10 * math.exp(-ag * 14), size, INK, shadow=False, sc=p)
        x += w + 2
        cx_, cy_ = x, ty
        n += 1
    if caretOn:
        caret(cx_ + 4, cy_, size * 1.05, t)
    text(f'{n}/50', sx + sw_ - 46, by + 188, 22, GREY, align='right', shadow=False, face=WENKAI)
    ry = by + 235
    flatRect(sx, ry, sw_, 78, '#FFFFFF')
    text('备注名', sx + 36, ry + 39, 28, INK, align='left', shadow=False)
    text('附近的她' if who == 'unknown' else '侦探小姐', sx + sw_ - 46, ry + 39, 28, GREY, align='right', shadow=False)
    ry += 86
    flatRect(sx, ry, sw_, 78, '#FFFFFF')
    text('朋友权限', sx + 36, ry + 39, 28, INK, align='left', shadow=False)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(sx + sw_ - 130, ry + 19, 84, 40), 20, 20, _pa(APPG))
    G.c.drawCircle(sx + sw_ - 66, ry + 39, 16, _pa('#FFFFFF'))
    sendButton(sx + sw_ / 2, ry + 150, 300, 88, sendLit, sendPress)
    if after:
        after()


def chatPage(t, sx, sy, sw_, sh, title='侦探小姐'):
    flatRect(sx, sy, sw_, sh, '#EDEDED')
    statusBar(sx, sy, sw_, '13:14')
    appTopBar(sx, sy + 50, sw_, title)
    # input bar
    flatRect(sx, sy + sh - 110, sw_, 110, '#F7F7F7')
    line(sx, sy + sh - 110, sx + sw_, sy + sh - 110, '#D6D2DC', 1, 1.5)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(sx + 90, sy + sh - 88, sw_ - 230, 64), 12, 12, _pa('#FFFFFF'))
    G.c.drawCircle(sx + 46, sy + sh - 56, 24, _pa(INK, 1, 2.5))
    G.c.drawCircle(sx + sw_ - 100, sy + sh - 56, 24, _pa(INK, 1, 2.5))
    G.c.drawCircle(sx + sw_ - 46, sy + sh - 56, 24, _pa(INK, 1, 2.5))
    line(sx + sw_ - 58, sy + sh - 56, sx + sw_ - 34, sy + sh - 56, INK, 1, 2.5)
    line(sx + sw_ - 46, sy + sh - 68, sx + sw_ - 46, sy + sh - 44, INK, 1, 2.5)


def chatMsg(sx, sw_, y, side, txt, k, size=44, key='cm', who=None, sticker=None):
    """one chat row: avatar + bubble. side 'L' = her, 'R' = him. Returns row height."""
    if k <= .02:
        return
    p = backOut(k)
    av = 'her' if side == 'L' else 'him'
    ax = sx + 64 if side == 'L' else sx + sw_ - 64
    push()
    translate(ax, y + 40)
    scale(min(1, p * 1.1))
    translate(-ax, -(y + 40))
    avatarBox(ax, y + 40, 38, av, 'happy' if side == 'L' else 'plain', key=key + 'av')
    pop()
    if sticker:
        sticker(sx + (130 if side == 'L' else sw_ - 130), y, p)
        return
    w = textW(txt, size) + size * 1.1
    h = size * 1.75
    bx = sx + 120 if side == 'L' else sx + sw_ - 120 - w
    col = '#FFFFFF' if side == 'L' else '#9EE8A8'
    ox = bx if side == 'L' else bx + w
    push()
    translate(ox, y + 40)
    scale(p)
    translate(-ox, -(y + 40))
    boilSeed(key)
    paint(rrPts(bx, y, w, h, 12), wash=col, ink=INK, sw=.8)
    if side == 'L':
        paint([[bx, y + 26], [bx - 16, y + 38], [bx, y + 50]], wash=col, ink=None)
    else:
        paint([[bx + w, y + 26], [bx + w + 16, y + 38], [bx + w, y + 50]], wash=col, ink=None)
    text(txt, bx + w / 2, y + h / 2, size, INK, shadow=False)
    pop()


# ------------------------------------------------------------------ café
def cafeWall(t, dim=0.0, key='cafe'):
    flatRect(-300, -300, W + 600, 1000, '#F7E6CC')
    for i in range(-3, 30):
        flatRect(i * 90, -300, 45, 1000, '#F2DCBC', .7)
    # wainscot
    flatRect(-300, 640, W + 600, 300, '#C08A5C')
    for i in range(-3, 30):
        line(i * 120, 650, i * 120, 900, '#9E6C44', .8, 3)
    line(-300, 640, W + 300, 640, INK, 1, 3)
    flatRect(-300, 630, W + 600, 14, '#D9A36F')
    # floor (checker)
    flatRect(-300, 900, W + 600, 600, '#E9D7BE')
    for r in range(4):
        for c_ in range(-4, 26):
            if (r + c_) % 2 == 0:
                x = c_ * 110 + (r * 0)
                flat([[x - (r * 40), 900 + r * 60], [x + 110 - (r * 40), 900 + r * 60], [x + 110 - (r + 1) * 40, 960 + r * 60],
                      [x - (r + 1) * 40, 960 + r * 60]], '#D7BF9F', 1)
    line(-300, 900, W + 300, 900, INK, 1, 3)
    # chalkboard menu
    boilSeed(key + 'cb')
    paint(rrPts(220, 150, 520, 360, 16), wash='#3E4A44', fill='#2F3A35', fillOp=90, ink=None)
    paint(rrPts(204, 134, 552, 392, 22), ink='#8E5E3A', sw=4.0)
    text('今日特调', 480, 205, 52, '#FFF5E2', shadow=False)
    items = [('珍珠奶茶', '15'), ('拿铁', '18'), ('一见钟情', '520')]
    for i, (nm, pr) in enumerate(items):
        yy = 290 + i * 70
        text(nm, 270, yy, 40, '#F7D36E' if i == 2 else '#FFF5E2', align='left', shadow=False)
        text(pr, 690, yy, 40, '#F7D36E' if i == 2 else '#FFF5E2', align='right', shadow=False)
    heart(705, 440, 18, '#FF8FB0', key=key + 'cbh', sw=.4, shine=False)
    # shelf with jars + plants (right)
    boilSeed(key + 'sh')
    for j, sy_ in enumerate((260, 430)):
        paint(rectPts(1180, sy_, 520, 22), wash='#B07A54', ink=INK, sw=.9)
        for q in range(5):
            jx = 1215 + q * 100
            if (q + j) % 3 == 0:
                paint([[jx - 26, sy_], [jx + 26, sy_], [jx + 20, sy_ - 46], [jx - 20, sy_ - 46]], wash='#D9774E', ink=INK, sw=.7)
                for lf in range(4):
                    a = -math.pi / 2 + (lf - 1.5) * .5
                    paint(ellPts(jx + math.cos(a) * 26, sy_ - 70 + math.sin(a) * 18, 10, 24, 8, 0, a + math.pi / 2), wash='#7CC36B', ink=INK, sw=.4)
            else:
                paint(rrPts(jx - 26, sy_ - 74, 52, 74, 10), wash=['#F3E2C3', '#E9C9A0', '#F7D9DE'][q % 3], ink=INK, sw=.7)
                flatRect(jx - 28, sy_ - 84, 56, 14, '#8E5E3A')
                G.c.drawCircle(jx, sy_ - 36, 8, _pa(['#6B4A33', '#3A2B2B', '#C0637B'][q % 3]))
    # pendant lamps
    for i, lx in enumerate((560, 1000, 1440)):
        line(lx, -300, lx, 70, INK, 1, 2)
        boilSeed(f'{key}pl{i}')
        paint([[lx - 60, 120], [lx + 60, 120], [lx + 26, 66], [lx - 26, 66]], wash='#2F5D57', ink=INK, sw=.9)
        glow(lx, 150, 190, '#FFE7A0', .55 * (1 - dim))
        G.c.drawCircle(lx, 128, 14, _pa('#FFF4C8'))
    # string lights
    stringLights([[-40, 40], [400, 110], [800, 50], [1200, 110], [1600, 40], [1980, 100]], t, on=1 - .6 * dim, key=key + 'sl')
    # door (far right) with a bell
    boilSeed(key + 'door')
    paint(rectPts(1770, 330, 230, 570), wash='#8E5E3A', fill='#6B4A33', fillOp=60, ink=INK, sw=1.0)
    paint(rectPts(1800, 370, 170, 230), wash='#A8764E', ink=INK, sw=.7)
    paint(rectPts(1800, 630, 170, 230), wash='#A8764E', ink=INK, sw=.7)
    G.c.drawCircle(1800, 640, 10, _pa('#F2C53D'))


def doorBell(x, y, s, swing=0.0, key='bell'):
    push()
    translate(x, y)
    rotate(swing)
    line(0, -s * .9, 0, 0, INK, 1, 2)
    boilSeed(key)
    paint([[-s * .55, s * .8], [s * .55, s * .8], [s * .38, s * .1], [0, -s * .05], [-s * .38, s * .1]], wash='#F2C53D', fill='#C99A2E',
          fillOp=80, ink=INK, sw=.8, curv=.2)
    G.c.drawCircle(0, s * .9, s * .15, _pa('#8E6A3E'))
    pop()


def cafeTable(x, y, w, key='ctab', cloth='#F7C6D2'):
    """round table seen from the front: (x, y) = top centre of the cloth. Draw after the people (hides their legs)."""
    boilSeed(key)
    paint(rectPts(x - 16, y + 60, 32, 900 - y + 20), wash='#6B4A33', ink=INK, sw=.8)
    paint(ellPts(x, 920, 90, 16, 18), wash='#4A3A30', ink=INK, sw=.6)
    pts = [[x - w / 2, y], [x + w / 2, y], [x + w / 2 + 14, y + 110], [x - w / 2 - 14, y + 110]]
    paint(pts, wash=cloth, fill=mixCol(cloth, INK, .15), fillOp=40, ink=INK, sw=1.0)
    # gingham hint
    for i in range(1, 7):
        xx = x - w / 2 + i * w / 7
        line(xx, y + 4, xx + (xx - x) * .03, y + 106, '#FFFFFF', .55, 6)
    for j in range(1, 3):
        line(x - w / 2 - j * 4, y + j * 36, x + w / 2 + j * 4, y + j * 36, '#FFFFFF', .55, 6)
    paint(ellPts(x, y, w / 2, 22, 30), wash=mixCol(cloth, '#FFFFFF', .35), ink=INK, sw=.9)


def book(x, y, s, open_=1.0, flip=0.0, key='book', title='侦探'):
    """open book held up (front view). flip 0..1 = a page turning."""
    boilSeed(key)
    w = 3.2 * s
    h = 2.2 * s
    if open_ < .5:
        paint(rrPts(x - w * .26, y - h / 2, w * .52, h, s * .08), wash='#7A2E3A', ink=INK, sw=.9)
        text(title, x, y, s * .5, '#F7D36E', shadow=False)
        return
    paint([[x - w / 2, y - h / 2 + s * .1], [x, y - h / 2], [x + w / 2, y - h / 2 + s * .1], [x + w / 2, y + h / 2], [x, y + h / 2 - s * .1],
           [x - w / 2, y + h / 2]], wash='#7A2E3A', ink=INK, sw=.9)
    paint([[x - w / 2 + s * .1, y - h / 2 + s * .14], [x - s * .05, y - h / 2 + s * .06], [x - s * .05, y + h / 2 - s * .14],
           [x - w / 2 + s * .1, y + h / 2 - s * .06]], wash='#FFFBF0', ink=INK, sw=.6)
    paint([[x + s * .05, y - h / 2 + s * .06], [x + w / 2 - s * .1, y - h / 2 + s * .14], [x + w / 2 - s * .1, y + h / 2 - s * .06],
           [x + s * .05, y + h / 2 - s * .14]], wash='#FFFBF0', ink=INK, sw=.6)
    for i in range(5):
        yy = y - h / 2 + s * .4 + i * s * .32
        line(x - w / 2 + s * .3, yy, x - s * .3, yy, '#B9AFC4', 1, 2)
        line(x + s * .3, yy, x + w / 2 - s * .3, yy, '#B9AFC4', 1, 2)
    if 0 < flip < 1:
        a = flip * math.pi
        px = x + math.cos(a) * (w / 2 - s * .1)
        paint([[x, y - h / 2 + s * .06], [px, y - h / 2 + s * .12 - math.sin(a) * s * .3], [px, y + h / 2 - s * .1 - math.sin(a) * s * .3],
               [x, y + h / 2 - s * .14]], wash='#FFFFFF', ink=INK, sw=.6)


# ------------------------------------------------------------------ clinic
def clinicWall(t, key='cl', col='#CFEDE0', tile='#F4FAF7'):
    flatRect(-300, -300, W + 600, 1000, col)
    flatRect(-300, 560, W + 600, 340, tile)
    for i in range(-3, 30):
        line(i * 80, 560, i * 80, 900, '#D5E6DE', 1, 2)
    for j in range(5):
        line(-300, 560 + j * 80, W + 300, 560 + j * 80, '#D5E6DE', 1, 2)
    line(-300, 560, W + 300, 560, INK, .8, 2.5)
    flatRect(-300, 900, W + 600, 600, '#BFD3E0')
    for i in range(-3, 30):
        line(i * 140, 900, i * 140 - 80, 1200, '#A9C0D0', 1, 2)
    line(-300, 900, W + 300, 900, INK, 1, 3)


def wallClock(x, y, r, t, key='clk', hh=10.2, mm=None):
    boilSeed(key)
    paint(ellPts(x, y, r, r, 30), wash='#FFFFFF', ink=INK, sw=1.2)
    for i in range(12):
        a = i / 12 * TAU
        line(x + math.cos(a) * r * .78, y + math.sin(a) * r * .78, x + math.cos(a) * r * .9, y + math.sin(a) * r * .9, INK, 1, 3)
    mm = (t * 6) % 60 if mm is None else mm
    a1 = (hh / 12) * TAU - math.pi / 2
    a2 = (mm / 60) * TAU - math.pi / 2
    line(x, y, x + math.cos(a1) * r * .5, y + math.sin(a1) * r * .5, INK, 1, 6)
    line(x, y, x + math.cos(a2) * r * .75, y + math.sin(a2) * r * .75, INK, 1, 4)
    G.c.drawCircle(x, y, 6, _pa(HOT))


def medCabinet(x, y, w, h, key='mc'):
    boilSeed(key)
    paint(rectPts(x, y, w, h), wash='#FFFFFF', fill='#E6EEF0', fillOp=60, ink=INK, sw=1.0)
    line(x + w / 2, y + 10, x + w / 2, y + h - 10, INK, .7, 2)
    flat(rectPts(x + w / 2 - 50, y + 40, 100, 30), '#E8574E')
    flat(rectPts(x + w / 2 - 15, y + 5, 30, 100), '#E8574E')
    for i in range(3):
        paint(rectPts(x + 20, y + 140 + i * 70, w - 40, 10), wash='#D9E4E8', ink=None)
        for q in range(4):
            bx = x + 40 + q * (w - 80) / 4
            paint(rrPts(bx, y + 100 + i * 70, 34, 42, 6), wash=['#F7C6D2', '#BFE3F5', '#FBE7A1', '#CDEFE0'][(q + i) % 4], ink=INK, sw=.5)


def heightChart(x, y, h, key='hc'):
    boilSeed(key)
    paint(rectPts(x, y, 60, h), wash='#FFFBF0', ink=INK, sw=.8)
    for i in range(int(h // 30)):
        line(x, y + i * 30, x + (30 if i % 2 else 45), y + i * 30, INK, .7, 2)


def monitorBox(x, y, w, h, key='mon'):
    boilSeed(key)
    paint(rrPts(x - 16, y - 16, w + 32, h + 80, 24), wash='#E9ECF2', fill='#C9CED8', fillOp=60, ink=INK, sw=1.2)
    flatRect(x, y, w, h, '#16202A')
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), 10, 10, _pa(INK, 1, 3))


def ecgTrace(x, y, w, h, t, mode='beat', beats=(), col='#7CF29A', speed=520.0, amp=1.0, a=1.0, sw=4.0):
    """scrolling ECG inside (x, y, w, h). mode: 'beat' = spike on each beat time, 'flat', 'hearts' = heart-shaped blips."""
    pts = []
    n = 160
    for i in range(n + 1):
        px = x + w * i / n
        tt = t - (x + w - px) / speed
        v = 0.0
        if mode != 'flat':
            for tb in beats:
                d = tt - tb
                if -.02 < d < .22:
                    if mode == 'beat':
                        v += (math.exp(-((d - .03) / .012) ** 2) * 1.0 - math.exp(-((d - .06) / .015) ** 2) * .45
                              + .18 * math.exp(-((d - .15) / .03) ** 2))
            v += .03 * math.sin(tt * 37)
        pts.append([px, y + h / 2 - v * h * .42 * amp])
    G.c.drawPath(eng._path(pts, False), _pa(col, a, sw))
    if mode == 'hearts':
        for tb in beats:
            px = x + w - (t - tb) * speed
            if x + 40 < px < x + w - 20 and t >= tb:
                paint(heartPts(px, y + h / 2 - h * .18, h * .2, 22), wash=None, ink=col, sw=1.2)
    # leading dot
    G.c.drawCircle(pts[-1][0], pts[-1][1], 7, _pa('#FFFFFF', a))


def eyeChart(x, y, w, h, lit, t, key='ec'):
    """light-box eye chart, every letter is 你. lit = list of 0..1 for the 4 rows (pop progress)."""
    boilSeed(key)
    glow(x + w / 2, y + h / 2, w * .8, '#FFFFFF', .35)
    paint(rrPts(x - 14, y - 14, w + 28, h + 28, 16), wash='#E9ECF2', ink=INK, sw=1.2)
    flatRect(x, y, w, h, '#FFFFFF')
    rows = [(1, 120), (2, 82), (3, 60), (0, 46)]
    yy = y + 110
    for i, (n, size) in enumerate(rows):
        k = lit[i] if i < len(lit) else 0
        if k > .01:
            p = backOut(clamp(k))
            if n == 0:
                text('只有你', x + w / 2, yy, size * 1.25, HOT, shadow=False, sc=p)
            else:
                gap = w / (n + 1)
                for j in range(n):
                    text('你', x + gap * (j + 1), yy, size, INK, shadow=False, sc=p)
        else:
            for j in range(max(1, n)):
                gap = w / (max(1, n) + 1)
                flatRect(x + gap * (j + 1) - size * .35, yy - size * .06, size * .7, size * .12, '#E3E0E8')
        yy += size + 70
    # side rule
    for i in range(4):
        text(['0.1', '0.3', '0.6', '1.0'][i], x + 36, y + 110 + sum(r[1] + 70 for r in rows[:i]), 20, GREY, shadow=False, face=WENKAI)


def pointerHook(L=4.6, col='#B07A54'):
    def h(u, sw):
        paint(rectPts(-.2 * u, -.13 * u, L * u, .26 * u), wash=col, ink=INK, sw=sw * .5)
        G.c.drawCircle((L - .2) * u, 0, .22 * u, _pa(HOT))
    return h


def occluderHook():
    def h(u, sw):
        paint(rectPts(-.1 * u, -.12 * u, 1.6 * u, .24 * u), wash='#3A3550', ink=INK, sw=sw * .5)
        paint(ellPts(2.3 * u, 0, .85 * u, .85 * u, 16), wash='#3A3550', ink=INK, sw=sw * .6)
    return h


# ------------------------------------------------------------------ hospital
def hospitalBed(x, y, w, key='bed'):
    """(x, y) = mattress top centre; returns nothing. head board on the left."""
    boilSeed(key)
    paint(rectPts(x - w / 2 - 30, y - 150, 30, 330), wash='#E9ECF2', ink=INK, sw=1.0)
    paint(rectPts(x + w / 2, y - 60, 26, 240), wash='#E9ECF2', ink=INK, sw=1.0)
    paint(rectPts(x - w / 2, y + 40, w, 36), wash='#C9CED8', ink=INK, sw=.9)
    for lx in (x - w / 2 + 30, x + w / 2 - 30):
        paint(rectPts(lx - 8, y + 76, 16, 104), wash='#9AA3B2', ink=INK, sw=.6)
        G.c.drawCircle(lx, y + 186, 12, _pa(INK))
    paint(rrPts(x - w / 2, y - 10, w, 56, 20), wash='#FFFFFF', fill='#E6EEF5', fillOp=60, ink=INK, sw=.9)


def bedBlanket(x, y, w, key='blk'):
    boilSeed(key)
    paint(rrPts(x - w / 2 + w * .32, y - 34, w * .7, 90, 26), wash='#9CC8EE', fill='#7FB0DC', fillOp=60, ink=INK, sw=1.0)
    for i in range(1, 5):
        line(x - w / 2 + w * .32 + i * w * .14, y - 30, x - w / 2 + w * .32 + i * w * .14, y + 52, '#FFFFFF', .5, 4)


def ivStand(x, y, h, t, key='iv'):
    boilSeed(key)
    line(x, y, x, y - h, '#9AA3B2', 1, 6)
    line(x - 60, y, x + 60, y, '#9AA3B2', 1, 6)
    line(x - 40, y - h, x + 40, y - h, '#9AA3B2', 1, 5)
    paint(heartPts(x + 30, y - h + 80, 46, 24), wash='#FFC2D3', washOp=230, ink=INK, sw=.8)
    line(x + 30, y - h + 120, x + 30, y - h + 180, '#E8476E', .8, 2)


def bedCurtain(x0, x1, y0, y1, open_=0.0, key='bc', col='#BFE3F5'):
    """ceiling-rail bed curtain (not a window). open_ 0 = closed across [x0, x1]; 1 = bunched at x1."""
    line(x0 - 40, y0, x1 + 40, y0, '#9AA3B2', 1, 6)
    w = (x1 - x0) * (1 - .82 * ease(open_))
    xa = x1 - w
    boilSeed(key)
    n = 7
    pts = [[xa, y0]]
    for i in range(n + 1):
        pts.append([xa + w * i / n, y0 + (8 if i % 2 else 0)])
    pts += [[x1, y1], [xa, y1]]
    paint(pts, wash=col, fill=mixCol(col, INK, .12), fillOp=50, ink=INK, sw=.9)
    for i in range(1, n):
        line(xa + w * i / n, y0 + 10, xa + w * i / n + 6, y1 - 6, mixCol(col, INK, .2), .7, 3)


def hpHearts(x, y, s, n, blink=0.0, key='hp'):
    """a row of 5 heart pips (n full)"""
    for i in range(5):
        full = i < n
        col = '#E8476E' if full else '#E3DEE8'
        if full and n == 1 and blink > .5:
            col = '#FFB0C0'
        heart(x + i * s * 2.3, y, s, col, key=f'{key}{i}', sw=.6, shine=full)


def paddleHook(glowK=0.0, key='pd'):
    def h(u, sw):
        paint(rectPts(-.1 * u, -.3 * u, 1.3 * u, .6 * u), wash='#3A3550', ink=INK, sw=sw * .5)
        push()
        translate(2.4 * u, 0)
        rotate(math.pi / 2)
        paint(heartPts(0, 0, 1.4 * u, 24), wash='#F2F4F8', fill='#C9CED8', fillOp=60, ink=INK, sw=sw * .7)
        paint(heartPts(0, .08 * u, .85 * u, 20), wash='#E8476E', ink=None)
        pop()
        if glowK > .05:
            glow(2.2 * u, 0, 2.6 * u, '#FFF6B0', .7 * glowK)
    return h


def bolt(x0, y0, x1, y1, seed=0, col='#FFF27A', w=6.0, a=1.0):
    glow((x0 + x1) / 2, (y0 + y1) / 2, math.hypot(x1 - x0, y1 - y0) * .5, '#FFF6B0', .35 * a)
    pts = [[x0, y0]]
    n = 6
    for i in range(1, n):
        k = i / n
        nx, ny = -(y1 - y0), (x1 - x0)
        L = math.hypot(nx, ny) or 1
        off = (hash1(seed * 7 + i) - .5) * 60
        pts.append([lerp(x0, x1, k) + nx / L * off, lerp(y0, y1, k) + ny / L * off])
    pts.append([x1, y1])
    G.c.drawPath(eng._path(pts, False), _pa(INK, a, w + 5))
    G.c.drawPath(eng._path(pts, False), _pa(col, a, w))


# ------------------------------------------------------------------ pharmacy + BP gauge
def pharmacyShelves(t, key='ph'):
    flatRect(-300, -300, W + 600, 1600, '#D7F0E6')
    for i in range(-3, 30):
        flatRect(i * 100, -300, 50, 1600, '#CBEADC', .8)
    for j, sy_ in enumerate((260, 520, 780)):
        boilSeed(f'{key}s{j}')
        paint(rectPts(-60, sy_, W + 120, 26), wash='#FFFFFF', fill='#DDE6E2', fillOp=60, ink=INK, sw=.9)
        for q in range(16):
            bx = 40 + q * 120 + (j * 37) % 60
            if 680 < bx < 1240:
                continue
            hh = 70 + 40 * hash1(q * 3 + j)
            col = ['#F7C6D2', '#BFE3F5', '#FBE7A1', '#FFFFFF', '#CDEFE0'][(q + j) % 5]
            boilSeed(f'{key}b{j}{q}')
            if (q + j) % 3 == 0:
                paint(rrPts(bx - 30, sy_ - hh, 60, hh, 10), wash=col, ink=INK, sw=.6)
                flatRect(bx - 32, sy_ - hh - 14, 64, 16, '#FFFFFF')
                G.c.drawRect(skia.Rect.MakeXYWH(bx - 32, sy_ - hh - 14, 64, 16), _pa(INK, 1, 1.5))
            else:
                paint(rectPts(bx - 40, sy_ - hh * .8, 80, hh * .8), wash=col, ink=INK, sw=.6)
                flat(rectPts(bx - 22, sy_ - hh * .5, 44, 10), '#E8574E')
                flat(rectPts(bx - 5, sy_ - hh * .5 - 17, 10, 44), '#E8574E')
    flatRect(-300, 900, W + 600, 600, '#F4F0E8')
    line(-300, 900, W + 300, 900, INK, 1, 3)


def pillBottle(x, y, s, cap=0.0, key='pb', label='硝苯地平'):
    """(x, y) = bottom centre; ~3s wide, 4.4s tall. cap = 0 closed .. 1 flown off (returns cap position)"""
    boilSeed(key)
    w, h = 3.0 * s, 3.6 * s
    paint(rrPts(x - w / 2, y - h, w, h, s * .5), wash='#FFFFFF', fill='#E9ECF2', fillOp=60, ink=INK, sw=1.4)
    paint(rrPts(x - w / 2 + s * .2, y - h * .78, w - s * .4, h * .5, s * .15), wash='#FFE7EE', ink=INK, sw=.9)
    text(label, x, y - h * .62, s * .5, HOT, shadow=False)
    text('相思病专用 · 每次一颗', x, y - h * .4, s * .22, GREY, shadow=False, face=WENKAI)
    heart(x, y - h * .9, s * .22, HOT, key=key + 'lh', sw=.4, shine=False)
    paint(rectPts(x - w * .36, y - h - s * .3, w * .72, s * .32), wash='#FFFFFF', ink=INK, sw=.9)
    if cap < 1:
        cx = x + cap * 2.4 * s
        cy = y - h - s * .3 - math.sin(cap * math.pi) * 2.4 * s - cap * s
        push()
        translate(cx, cy)
        rotate(cap * 1.1)
        paint(rrPts(-w * .4, -s * 1.05, w * .8, s * 1.05, s * .22), wash='#E8476E', fill='#B8324F', fillOp=50, ink=INK, sw=1.1)
        paint(rrPts(-w * .4, -s * 1.05, w * .8, s * .3, s * .14), wash='#F37C98', ink=INK, sw=.8)
        for i in range(7):
            line(-w * .32 + i * w * .107, -s * .65, -w * .32 + i * w * .107, -s * .12, '#B8324F', .8, 3)
        pop()


def pill(x, y, s, rot=0.0, key='pl'):
    """a heart-shaped pill: two-tone, glossy"""
    push()
    translate(x, y)
    rotate(rot)
    glow(0, 0, s * 1.8, '#FFC2D3', .45)
    boilSeed(key)
    P = heartPts(0, 0, s, 30)
    paint(P, wash='#FFFFFF', ink=INK, sw=1.1)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(-s * 2, -s * 2, s * 2, s * 4))
    paint(P, wash='#FF6F96', ink=None)
    G.c.restore()
    paint(P, ink=INK, sw=1.1)
    paint(ellPts(-s * .42, -s * .38, s * .2, s * .11, 10, 0, -.6), wash='#FFFFFF', washOp=200, ink=None)
    pop()


def bpGauge(x, y, r, val, key='bp'):
    """round blood-pressure dial; val 0 (left, green 平) .. 1 (right, red 爆表)"""
    boilSeed(key)
    paint(ellPts(x, y, r + 26, r + 26, 40), wash='#C9CED8', ink=INK, sw=1.4)
    paint(ellPts(x, y, r, r, 40), wash='#FFFDF6', ink=INK, sw=1.0)
    a0, a1 = math.pi * .8, math.pi * 2.2
    segs = [('#7CC36B', 0, .4), ('#F2C14E', .4, .7), ('#E8574E', .7, 1.0)]
    for col, s0, s1 in segs:
        pts = []
        for i in range(21):
            a = lerp(a0, a1, lerp(s0, s1, i / 20))
            pts.append([x + math.cos(a) * r * .8, y + math.sin(a) * r * .8])
        G.c.drawPath(eng._path(pts, False), _pa(col, 1, r * .14))
    for i in range(11):
        a = lerp(a0, a1, i / 10)
        line(x + math.cos(a) * r * .62, y + math.sin(a) * r * .62, x + math.cos(a) * r * .7, y + math.sin(a) * r * .7, INK, 1, 3)
    text('平', x + math.cos(lerp(a0, a1, .12)) * r * .45, y + math.sin(lerp(a0, a1, .12)) * r * .45, r * .2, '#4E9A45', shadow=False)
    text('爆表', x + math.cos(lerp(a0, a1, .88)) * r * .42, y + math.sin(lerp(a0, a1, .88)) * r * .42, r * .15, '#C8323F', shadow=False)
    text('mmHg', x, y + r * .5, r * .12, GREY, shadow=False, face=WENKAI)
    a = lerp(a0, a1, clamp(val, -.02, 1.04))
    G.c.drawLine(x, y, x + math.cos(a) * r * .74, y + math.sin(a) * r * .74, _pa(INK, 1, r * .05))
    G.c.drawCircle(x, y, r * .08, _pa(HOT))


# ------------------------------------------------------------------ street (shop fronts are open counters, no glass)
SHOPS2 = [('奶茶', '#F7C6D2', '#E8476E'), ('花店', '#CDEFE0', '#3FA36B'), ('书店', '#FBE7A1', '#C98B2E'), ('甜品', '#D9CCF2', '#7B5CA8')]


def shopStreet(t, key='st', ground=860, dusk=0.0, grey=0.0):
    sky = ['#A9DBF5', '#DDF2FB', '#FFF6E2'] if dusk < .5 else ['#6E5AA8', '#E58FA6', '#FFC98A']
    gradRect(-400, -400, W + 800, ground + 400, [mixCol(c, '#D8D6DC', grey) for c in sky])
    if dusk < .5:
        for i, (cx, cy, s) in enumerate([(220, 120, 24), (760, 80, 18), (1420, 140, 26), (1840, 90, 16)]):
            puff(cx + 10 * math.sin(t * .4 + i), cy, s, '#FFFFFF', key=f'{key}cl{i}', ink=True, a=.95)
    else:
        glow(1500, 520, 420, '#FFD08A', .6)
        paint(ellPts(1500, 560, 120, 120, 30), wash='#FFB36B', ink=None)
    xs = [-140, 330, 800, 1270, 1740, 2210]
    for i in range(5):
        x0, x1 = xs[i] + 10, xs[i + 1] - 10
        hgt = [470, 560, 600, 500, 540][i]
        name, col, sign = SHOPS2[i % 4]
        col = mixCol(col, '#D8D6DC', grey)
        sign = mixCol(sign, '#8A8794', grey)
        boilSeed(f'{key}b{i}')
        paint(rectPts(x0, ground - hgt, x1 - x0, hgt), wash=col, fill=mixCol(col, INK, .2), fillOp=50, ink=INK, sw=1.0)
        # upper floor: closed wooden shutters + flower boxes
        for c_ in range(3):
            wx = x0 + 40 + c_ * (x1 - x0 - 80) / 3
            wy = ground - hgt + 40
            if wy < ground - 330:
                ww = (x1 - x0 - 80) / 3 - 30
                paint(rectPts(wx, wy, ww, 76), wash=mixCol('#B98552', '#D8D6DC', grey), ink=INK, sw=.6)
                line(wx + ww / 2, wy, wx + ww / 2, wy + 76, INK, .6, 2)
                for q in range(3):
                    line(wx + 6, wy + 18 + q * 20, wx + ww - 6, wy + 18 + q * 20, mixCol('#8E5E3A', '#B0AEB6', grey), 1, 2)
                paint(rectPts(wx - 6, wy + 76, ww + 12, 16), wash=mixCol('#8E5E3A', '#B0AEB6', grey), ink=INK, sw=.5)
                for q in range(4):
                    G.c.drawCircle(wx + 8 + q * ww / 3.4, wy + 72, 8, _pa(mixCol(['#FF8FB0', '#FFD36A'][q % 2], '#C8C6CC', grey)))
        ay = ground - 290
        n = 8
        aw = (x1 - x0 + 40) / n
        for j in range(n):
            boilSeed(f'{key}aw{i}{j}')
            ax = x0 - 20 + j * aw
            paint([[ax, ay], [ax + aw, ay], [ax + aw, ay + 60], [ax + aw / 2, ay + 80], [ax, ay + 60]],
                  wash=sign if j % 2 == 0 else mixCol('#FFFFFF', '#E0DEE4', grey), ink=INK, sw=.6)
        paint(rrPts(x0 + 40, ay - 90, x1 - x0 - 80, 70, 14), wash=mixCol('#FFFDF6', '#E8E6EC', grey), ink=INK, sw=.9)
        text(name, (x0 + x1) / 2, ay - 55, 46, sign, shadow=False)
        # open counter (dark interior + goods on a sill)
        paint(rectPts(x0 + 30, ay + 100, x1 - x0 - 60, ground - ay - 160), wash=mixCol('#4A3A44', '#6A6870', grey), ink=INK, sw=.9)
        paint(rectPts(x0 + 20, ground - 70, x1 - x0 - 40, 70), wash=mixCol('#B98552', '#A8A6AE', grey), ink=INK, sw=.8)
        for j in range(4):
            gx = x0 + 70 + j * (x1 - x0 - 140) / 3
            gc = ['#FFD36A', '#FF8FB0', '#8FD3FF', '#B8F0A0'][(i + j) % 4]
            boilSeed(f'{key}g{i}{j}')
            paint(rrPts(gx - 26, ground - 120, 52, 50, 10), wash=mixCol(gc, '#C8C6CC', grey), ink=INK, sw=.5)
    flatRect(-400, ground, W + 800, 90, mixCol('#E9DCCB', '#DCDAE0', grey))
    for i in range(-3, 24):
        line(i * 100, ground, i * 100 - 30, ground + 90, '#C9B8A2', .6, 2)
    line(-400, ground, W + 400, ground, INK, 1, 3)
    flatRect(-400, ground + 90, W + 800, 400, mixCol('#8A8EA0', '#A0A0A8', grey))
    line(-400, ground + 90, W + 400, ground + 90, INK, 1, 2.5)
    for i in range(-2, 12):
        flatRect(i * 260 + 40, ground + 170, 140, 14, '#FFFFFF', .8)


def greyClawd(x, y, u, i, a=1.0, key='gc'):
    """a grey cardboard passer-by (everyone who is not her)"""
    if a <= .02:
        return
    shade = ['#B8B6BE', '#A9A7B0', '#C4C2CA'][i % 3]
    o = dict(col=shade, dk=mixCol(shade, INK, .25), lt=mixCol(shade, '#FFFFFF', .4), view=['q', 'front', 'q'][i % 3], flip=i % 2 == 1,
             eyes='blank', mouth=None, boilKey=f'{key}{i}', walk=None, noShadow=False, aL=.1, aR=.15)
    if a < 1:
        G.c.saveLayerAlpha(None, int(255 * a))
        clawd(x, y, u, o)
        G.c.restore()
    else:
        clawd(x, y, u, o)


# ------------------------------------------------------------------ ring box / x-ray / lock
def qrRingBox(x, y, s, k=1.0, t=0.0, key='qrb'):
    """velvet ring box (x, y = bottom centre). k = lid open 0..1; inside a glowing QR code"""
    boilSeed(key)
    w = 3.2 * s
    if k > .2:
        glow(x, y - 2.0 * s, 3.4 * s * k, '#FFF3B0', .8 * k)
    paint(rrPts(x - w / 2, y - 1.3 * s, w, 1.3 * s, .2 * s), wash='#E8476E', fill='#B8324F', fillOp=60, ink=INK, sw=1.1)
    push()
    translate(x, y - 1.3 * s)
    rotate(-1.75 * ease(k))
    translate(0, 0)
    paint(rrPts(-w / 2, -1.1 * s, w, 1.1 * s, .2 * s), wash='#F37C98', fill='#C8456A', fillOp=50, ink=INK, sw=1.1)
    pop()
    if k > .25:
        a = clamp((k - .25) / .4)
        qrCode(x, y - 2.15 * s, 1.55 * s, seed=7, a=a, center=lambda cx, cy, r: heart(cx, cy, r * .8, HOT, key=key + 'qh', sw=.4, shine=False))


def xrayBox(x, y, w, h, on=1.0, key='xr'):
    boilSeed(key)
    paint(rrPts(x - 20, y - 20, w + 40, h + 40, 20), wash='#E9ECF2', fill='#C9CED8', fillOp=50, ink=INK, sw=1.2)
    flatRect(x, y, w, h, mixCol('#20263A', '#9FC4F0', on * .55))
    if on > .05:
        glow(x + w / 2, y + h / 2, w * .7, '#CFE6FF', .35 * on)
    G.c.drawRect(skia.Rect.MakeXYWH(x, y, w, h), _pa(INK, 1, 3))
    # clips
    for cx in (x + w * .3, x + w * .7):
        paint(rectPts(cx - 26, y - 34, 52, 30), wash='#9AA3B2', ink=INK, sw=.7)


def xrayClawd(x, y, u, a=1.0):
    """his outline on the x-ray film (pale blue ink on dark)"""
    col = '#DDEBFF'
    P = [[x - 5 * u, y - 8 * u], [x + 5 * u, y - 8 * u], [x + 5 * u, y - 2 * u], [x - 5 * u, y - 2 * u]]
    G.c.drawPath(eng._path(P, True), _pa(col, .8 * a, 4))
    for lx in (-4, -2, 1, 3):
        G.c.drawRect(skia.Rect.MakeXYWH(x + lx * u, y - 2 * u, u, 2 * u), _pa(col, .6 * a, 3))
    for s_ in (-1, 1):
        G.c.drawRect(skia.Rect.MakeXYWH(x + (5 if s_ > 0 else -7.2) * u, y - 5 * u, 2.2 * u, u), _pa(col, .6 * a, 3))
    # 'bones' (stripes) faint
    for i in range(4):
        line(x - 3.6 * u, y - 7 * u + i * 1.2 * u, x + 3.6 * u, y - 7 * u + i * 1.2 * u, col, .25 * a, 3)
    for ex in (-1.6, 1.6):
        G.c.drawRect(skia.Rect.MakeXYWH(x + ex * u - .3 * u, y - 6.6 * u, .6 * u, 1.2 * u), _pa(col, .8 * a))


def lockHeart(x, y, s, shut=1.0, key='lk', a=1.0):
    """heart with a little padlock on it; shut 0..1 = shackle closing"""
    boilSeed(key)
    glow(x, y, s * 2.2, '#FFC2D3', .5 * a)
    paint(heartPts(x, y, s, 30), wash='#FF6F96', fill='#E8476E', fillOp=50, ink=INK, sw=1.2)
    paint(ellPts(x - s * .4, y - s * .35, s * .18, s * .1, 10, 0, -.6), wash='#FFFFFF', washOp=170, ink=None)
    lx, ly = x, y + s * .25
    up = (1 - ease(shut)) * s * .22
    pts = []
    for i in range(17):
        aa = math.pi + i / 16 * math.pi
        pts.append([lx + math.cos(aa) * s * .22, ly - s * .1 - up + math.sin(aa) * s * .26])
    G.c.drawPath(eng._path(pts, False), _pa(INK, 1, s * .1))
    G.c.drawPath(eng._path(pts, False), _pa('#F2C53D', 1, s * .06))
    paint(rrPts(lx - s * .32, ly - s * .12, s * .64, s * .5, s * .08), wash='#F2C53D', fill='#C99A2E', fillOp=60, ink=INK, sw=.9)
    G.c.drawCircle(lx, ly + s * .1, s * .06, _pa(INK))


def corkWall(t, key='cw'):
    flatRect(-300, -300, W + 600, 1600, '#2F4B5C')
    for i in range(-3, 30):
        flatRect(i * 110, -300, 55, 1600, '#2B4554', .8)
    boilSeed(key + 'cb')
    paint(rectPts(140, 120, 760, 470), wash='#C99A62', fill='#B5824C', fillOp=80, ink=INK, sw=1.2)
    paint(rectPts(124, 104, 792, 502), ink='#6B4A33', sw=4)
    for i, (px, py, rot) in enumerate([(260, 230, -.08), (520, 200, .06), (760, 260, -.05), (330, 450, .07), (640, 460, -.06)]):
        push()
        translate(px, py)
        rotate(rot)
        boilSeed(f'{key}p{i}')
        paint(rectPts(-80, -70, 160, 140), wash='#FFFBF0', ink=INK, sw=.7)
        if i == 2:
            miniHead2(0, 10, 40, 'him', 'love', key=f'{key}mh')
        elif i == 0:
            text('？', 0, 0, 80, HOT, shadow=False)
        else:
            for q in range(4):
                line(-60, -40 + q * 26, 60, -40 + q * 26, '#B9AFC4', 1, 2)
        G.c.drawCircle(0, -62, 9, _pa('#E03A4E'))
        pop()
    line(260, 168, 760, 198, '#E03A4E', 1, 3)
    line(520, 138, 330, 388, '#E03A4E', 1, 3)
    line(760, 198, 640, 398, '#E03A4E', 1, 3)
    # filing cabinet
    boilSeed(key + 'fc')
    paint(rectPts(1500, 380, 300, 520), wash='#7B8A94', fill='#5E6C76', fillOp=60, ink=INK, sw=1.0)
    for j in range(3):
        paint(rectPts(1520, 400 + j * 165, 260, 145), wash='#8E9CA6', ink=INK, sw=.7)
        paint(rrPts(1610, 440 + j * 165, 80, 20, 8), wash='#D9E0E6', ink=INK, sw=.5)
        paint(rectPts(1620, 480 + j * 165, 60, 30), wash='#FFFBF0', ink=INK, sw=.4)
    flatRect(-300, 900, W + 600, 600, '#5A4038')
    line(-300, 900, W + 300, 900, INK, 1, 3)


def magLens(x, y, r, inner=None, key='ml', handleAng=.78, handleLen=None):
    """big magnifier: inner(x, y, r) draws the magnified view inside the lens"""
    if inner:
        G.c.save()
        p = skia.Path()
        p.addCircle(x, y, r)
        G.c.clipPath(p, skia.ClipOp.kIntersect, True)
        inner(x, y, r)
        G.c.restore()
    else:
        paint(ellPts(x, y, r, r, 36), wash='#DDF2FF', washOp=70, ink=None)
    paint(ellPts(x - r * .38, y - r * .42, r * .22, r * .12, 10, 0, -.6), wash='#FFFFFF', washOp=170, ink=None)
    boilSeed(key)
    G.c.drawCircle(x, y, r, _pa(INK, 1, 14))
    G.c.drawCircle(x, y, r, _pa('#E2B444', 1, 8))
    push()
    translate(x + math.cos(handleAng) * r, y + math.sin(handleAng) * r)
    rotate(handleAng)
    paint(rectPts(0, -r * .11, r * 1.0 if handleLen is None else max(8, handleLen), r * .22), wash='#7A4E33', ink=INK, sw=1.2)
    pop()


def placard2(x, y, w, h, txt, size, rot=0.0, key='pc', col='#FFFDF6', tcol=HOT, k=1.0):
    """hand-held sign that pops in (k)"""
    if k <= .02:
        return
    push()
    translate(x, y + h * .9)
    scale(backOut(k))
    translate(-x, -(y + h * .9))
    placardSign(x, y, w, h, txt, size, rot, key, col, tcol)
    pop()


def hearts(t, cx, cy, n, R, s, k, seed=0):
    """a ring of hearts bursting out (k = 0..1 age progress)"""
    if k <= 0 or k >= 1.2:
        return
    for i in range(n):
        a = i / n * TAU + hash1(seed + i) * .4
        d = R * easeOut(clamp(k))
        x = cx + math.cos(a) * d
        y = cy + math.sin(a) * d - 60 * k
        al = 1 - clamp((k - .7) / .5)
        heart(x, y, s * (.7 + .5 * hash1(seed * 3 + i)), HOT if i % 2 else '#FF9FBA', key=f'hb{seed}{i}', sw=.6, a=al)
