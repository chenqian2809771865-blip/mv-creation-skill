# props3.py: v2 sets for the Rolling in the Deep x 小苹果 mashup — every scene gets a layer of everyday things.
# Recurring small objects: his phone with an apple charm + the 「小苹果·今晚老地方见」 reminder, her room's fairy lights and photo
# string, the 「老地方」 sign, the deerstalker, two mugs (orange his, pink with a flower hers). Logical canvas 1920x1080.
import math
from eng import *
import eng
from clawd import *
from props import puff, sparkle, sparkles, bush, lamp as streetLamp, trashcan, mailbox, city, yiyun, banner, C
from props_chuanshao import (apple, applePts, flame, embers, bigPhone, notifCard, thermometer, spotBeam, spotLamp, crystalBall,
                             corkBoard, polaroid, pinThread, bloom, PETALS, petalsFly, starFace, wheat, mapleLeaf, snowflakes,
                             snowman, sign, bubble1, fish, seaweed, anglerfish, binoMask, appleTree, sprout, mound, LEAF, LEAF_DK)
from hl import (windowView, windowFrame, curtain, deskLamp, mug, fireflies, stars, rain as rainFX, WENKAI, tint)
from sets2 import (fairyLights, bookshelf, photoString, wallClock, wallCalendar, parkBench, seat, bigTreeSide, bike, butterfly as bfly,
                   washi, fakeText, coffeeRing, pencil, pencilDoodle, shopFront2, SHOPS, streetTall2, wateringCan, waterStream)
from sets import kite, milkyWay

HIS_MUG = '#E8874E'
HER_MUG = '#F4A9BC'


# ======================================================================== small shared things
def appleCharm(x, y, s, t, key='charm'):
    """the apple keychain dangling from his phone (callback object)"""
    sw_ = math.sin(t * 3.1) * .25
    inkLine([[x, y], [x + math.sin(sw_) * s * 1.6, y + math.cos(sw_) * s * 1.6]], max(.6, s / 20), '#B9B2A8', 'inkfine', .2)
    apple(x + math.sin(sw_) * s * 2.4, y + math.cos(sw_) * s * 2.4, s, key=key, rot=sw_ * .6)


def mugTop(x, y, r, col, t, key='mt', flower=False, steam=1.0):
    boilSeed(key)
    paint(ellPts(x, y, r, r * .96, 26), wash=col, fill=mixCol(col, INK, .25), fillOp=60, ink=INK, sw=.9)
    paint(ellPts(x, y, r * .74, r * .7, 24), wash='#7A4A2E', fill='#5A3420', fillOp=60, ink=INK, sw=.7)
    paint(ellPts(x - r * .2, y - r * .2, r * .2, r * .1, 10, 0, -.4), wash='#C99A6A', washOp=170, ink=None, lite=True)
    inkLine([[x + r * .95, y - r * .2], [x + r * 1.35, y - r * .25], [x + r * 1.35, y + r * .25], [x + r * .95, y + r * .2]], 1.6, INK, 'ink', .5)
    if flower:
        flowerAt(x - r * .55, y + r * .55, r * .22, .8)
    if steam > 0:
        for i in range(2):
            ph = frac(t * .35 + i * .5)
            inkLine([[x - 8 + i * 18, y - 6], [x - 18 + i * 18 + math.sin(t * 2 + i) * 10, y - 50 - ph * 40], [x - 2 + i * 18, y - 96 - ph * 40]], .9,
                    mixCol('#FFFFFF', '#C9B08F', .3), 'inkfine', .6)


def fruitBowlTop(x, y, r, key='fb'):
    boilSeed(key)
    paint(ellPts(x, y, r, r * .95, 30), wash='#E9E3D6', fill='#C9C0AE', fillOp=60, ink=INK, sw=1.0)
    paint(ellPts(x, y, r * .8, r * .76, 28), wash='#F6F1E6', ink=INK, sw=.6)
    for i, (dx, dy, rr) in enumerate([(-.3, -.15, .32), (.25, -.25, .3), (.05, .25, .33), (-.35, .3, .26), (.38, .2, .27)]):
        apple(x + dx * r, y + dy * r, rr * r, key=f'{key}a{i}', rot=i * .7)
    for i, (dx, dy) in enumerate([(.0, -.5)]):
        paint([[x + dx * r - 20, y + dy * r], [x + dx * r + 30, y + dy * r - 30], [x + dx * r + 50, y + dy * r - 5]], wash=LEAF, ink=INK, sw=.6, curv=.5)


def remote(x, y, rot, key='rm'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rrPts(-40, -110, 80, 220, 26), wash='#3A3550', fill='#2A2440', fillOp=60, ink=INK, sw=.9)
    G.c.drawCircle(0, -70, 12, skia.Paint(AntiAlias=True, Color=skcol('#E8574E')))
    for r in range(4):
        for c in range(3):
            G.c.drawCircle(-22 + c * 22, -20 + r * 26, 6, skia.Paint(AntiAlias=True, Color=skcol('#8A86A8')))
    pop()


def magazine(x, y, rot, key='mag'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-180, -240, 360, 480), wash='#F7C6D2', fill='#E8A0B4', fillOp=50, ink=INK, sw=.9)
    paint(rectPts(-150, -170, 300, 200), wash='#BFE3F5', ink=INK, sw=.6, lite=True)
    text('恋爱周刊', 0, -205, 44, '#B02A40', face=WENKAI, shadow=False)
    fakeText(-150, 60, 300, 20, 40, 5, a=.55)
    pop()


def stickyNote(x, y, s, rot, col='#FFE36E', txt=None, key='sn', tcol=INK):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint([[-s, -s], [s, -s], [s, s * .8], [s * .8, s], [-s, s]], wash=col, fill=mixCol(col, INK, .1), fillOp=50, ink=INK, sw=.7, lite=True)
    if txt:
        text(txt, 0, 0, s * .62, tcol, face=WENKAI, shadow=False)
    pop()


def coffeeTableTop(t):
    """S01: the coffee table seen from above (his phone is drawn by the shot)"""
    flatRect(-200, -200, W + 400, H + 400, '#8A5A3C')
    for i in range(9):
        y = -40 + i * 140
        boilSeed(f'plank{i}')
        flatRect(-200, y, W + 400, 136, mixCol('#9A6646', '#7E5034', hash1(i * 3.3)))
        inkLine([[-200, y], [W + 200, y + jit(3)]], .9, '#5A3826', 'inkfine', .1)
        for g in range(5):
            gx = hash1(i * 7 + g) * W
            inkLine([[gx, y + 30 + g * 18], [gx + 260, y + 34 + g * 18 + jit(4)]], .5, '#6E4630', 'inkfine', .4)
    glow(1700, -60, 900, '#FFC976', .45)
    coffeeRing(520, 900, 78, .3)
    magazine(1560, 760, .22, key='mag1')
    remote(300, 300, -.5, key='rm1')
    fruitBowlTop(1500, 260, 190, key='fb1')
    mugTop(560, 640, 92, HER_MUG, t, key='mugher', flower=True)
    mugTop(1240, 870, 86, HIS_MUG, t, key='mughis')
    stickyNote(160, 520, 64, -.2, '#BFE3F5', '买牛奶', key='sn1')
    # a potted plant leaning in from the corner
    for i in range(5):
        boilSeed(f'cpl{i}')
        a = -.3 + i * .32
        paint([[-40, 1120], [-40 + math.cos(a) * 380, 1120 - math.sin(a + .9) * 380], [60 + math.cos(a) * 300, 1120 - math.sin(a + .9) * 260]],
              wash=['#5E9E5A', '#4E8A4E', '#6EAE5E'][i % 3], ink=INK, sw=.8, curv=.5)


# ======================================================================== her room (front-facing) — no spare hat on the shelf
def herRoom(t, warm=0.0, board=False, lampK=1.0):
    """back wall + window + fairy lights + shelf + photo string + clock + calendar. warm 0..1 tints it fire-red"""
    c1, c2 = mixCol('#2B3168', '#6A2A3A', warm), mixCol('#3E4482', '#A8403A', warm)
    gradRect(-400, -400, W + 800, H + 800, [c1, c2])
    for i in range(-6, 40):
        G.c.drawRect(skia.Rect.MakeXYWH(i * 56, -400, 22, 1100), skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .025)))
    flatRect(-400, 600, W + 800, 200, mixCol(c2, INK, .25))
    G.c.drawLine(-400, 600, W + 400, 600, skia.Paint(AntiAlias=True, Color=skcol(mixCol(c2, '#FFFFFF', .2), .6), StrokeWidth=4))
    wx, wy, ww, wh = 600, 70, 720, 430
    windowView(wx, wy, ww, wh, t, key='wbher', moonXY=(wx + ww * .76, wy + wh * .25))
    windowFrame(wx, wy, ww, wh, '#6B4A3E', key='wbfher')
    curtain(wx - 40, wy - 30, wh + 90, -1, 0, '#8C7AA8', key='clher')
    curtain(wx + ww + 40, wy - 30, wh + 90, 1, 0, '#8C7AA8', key='crher')
    fairyLights(t, wx - 60, wx + ww + 60, wy - 46, 34, 16, key='flher', a=lampK)
    if board:
        return
    bookshelf(70, 150, 360, 450, key='bsher', who='him')
    photoString(t, 1440, 1840, 170, 'her', key='psher')
    wallClock(1520, 330, 46, t, key='clkher')
    wallCalendar(1680, 300, key='calher')


def herDesk(t, lampK=1.0, extra=None, mugSteam=1.0):
    """the desk in the foreground (drawn after the sitter): books, a tiny cactus, her pink mug, a framed photo of them, the lamp"""
    y = 760
    boilSeed('dskher')
    paint([[-100, y], [W + 100, y], [W + 100, y + 46], [-100, y + 46]], wash='#B98A60', fill='#8A5A3C', fillOp=50, ink=INK, sw=1.0)
    gradRect(-100, y + 46, W + 200, 400, ['#8A5A3C', '#5A3828'])
    inkLine([[-100, y + 46], [W + 100, y + 46]], 1.0, INK, 'ink', 0)
    for k in range(3):
        dx = 120 + k * 620
        paint(rectPts(dx, y + 80, 480, 120), wash='#7A5038', ink=INK, sw=.8, lite=True)
        paint(rrPts(dx + 210, y + 128, 60, 16, 8), wash='#D9B45A', ink=INK, sw=.6, lite=True)
    if lampK > 0:
        sh = skia.GradientShader.MakeRadial(skia.Point(1380, y + 20), 520, [skcol('#FFD48A', .32 * lampK), skcol('#FFD48A', 0)])
        G.c.drawRect(skia.Rect.MakeXYWH(700, y - 10, 1300, 70), skia.Paint(Shader=sh))
    for i, (bw, col) in enumerate([(230, '#5B7FC4'), (210, '#C8564F'), (220, '#E8B04A')]):
        boilSeed(f'stkher{i}')
        paint(rectPts(120 + i * 6, y + 24 - (i + 1) * 30, bw, 30), wash=col, ink=INK, sw=.7, lite=True)
    # framed photo of the two of them
    boilSeed('pfher')
    push()
    translate(500, y + 20)
    rotate(-.06)
    paint(rectPts(-70, -170, 140, 170), wash='#E8D3B8', ink=INK, sw=.9, lite=True)
    gradRect(-58, -158, 116, 146, ['#9FD4F2', '#F3E6C8'])
    clawd(-24, -20, 5.2, dict(col='#EE9AAE', dk='#C0637B', lt='#FBD0DA', hat='flower', eyes='happy', mouth='smile', lite=True, noShadow=True, boilKey='pfa'))
    clawd(26, -20, 5.2, dict(col=PAL['clay'], dk=PAL['clayDk'], lt='#F5B394', eyes='happy', mouth='smile', lite=True, noShadow=True, boilKey='pfb'))
    inkStroke(rectPts(-58, -158, 116, 146), True, .5, INK, 'inkfine')
    pop()
    # her mug with the flower
    mug(1300, y + 22, .85, key='mgher', col=HER_MUG, steam=mugSteam, t=t)
    flowerAt(1286, y - 30, 12, .8)
    boilSeed('ppher')
    paint([[1418, y + 22], [1478, y + 22], [1472, y - 50], [1424, y - 50]], wash='#7FB1B5', ink=INK, sw=.7, lite=True)
    for i, (dx, col) in enumerate([(-14, '#C8564F'), (0, '#2C2C44'), (14, '#E8B04A')]):
        inkLine([[1448 + dx, y - 48], [1448 + dx * 1.6, y - 120 + i * 8]], 2.2, col, 'ink', 0)
    deskLamp(1760, y + 26, 1.3, lampK, key='lpher', flip=True)
    if extra:
        extra()


# ======================================================================== the apartment block at night (S04)
def apartment(t, inside=None, doorK=1.0, catLook=0.0):
    """building face with a lit window for her (3rd floor, centre x=700), a ground-floor entrance at x≈1060, the pavement at y=900.
    inside(x, y, w, h) draws what is seen through her window. doorK 1 = open, 0 = shut"""
    gradRect(-300, -300, W + 600, 400, ['#10143A', '#1E2457'])
    stars(t, 41, 30, -200, -200, W + 200, 80, .8, 2.4)
    boilSeed('apt')
    paint(rectPts(-200, 40, W + 400, 900), wash='#3B4384', fill='#2C3370', fillOp=70, ink=INK, sw=1.0)
    gradRect(-200, 40, W + 400, 900, ['#3E4688', '#2A3068'])
    for yy in (290, 580):
        flatRect(-200, yy - 8, W + 400, 14, '#2A2F63')
    cols = ['#FFCF85', '#FFB98A', '#FFE2A0']
    wins = []
    for r, wy in enumerate((90, 380)):
        for c in range(-1, 8):
            wx = 60 + c * 290
            wins.append((r, c, wx, wy))
    mine = (1, 2)
    for (r, c, wx, wy) in wins:
        if (r, c) == mine:
            continue
        on = hash1(c * 5 + r * 11 + 3) < .4
        col = cols[(c + r) % 3]
        boilSeed(f'aw{r}{c}')
        paint(rectPts(wx, wy, 180, 160), wash=col if on else '#1B2050', washOp=230, ink=INK, sw=.8, lite=True)
        if on:
            glow(wx + 90, wy + 80, 150, col, .22)
            for s_ in (-1, 1):
                paint(rectPts(wx + 90 + s_ * 64 - 26, wy + 4, 52, 152), wash='#C98A7A' if (c + r) % 2 else '#8A9AC8', washOp=200, ink=None, lite=True)
            if hash1(c * 7 + r) < .4:
                paint([[wx + 60, wy + 160], [wx + 70, wy + 120], [wx + 110, wy + 116], [wx + 120, wy + 160]], wash='#2A2440', washOp=200, ink=None, lite=True)
        G.c.drawLine(wx + 90, wy, wx + 90, wy + 160, skia.Paint(AntiAlias=True, Color=skcol('#11132F', .85), StrokeWidth=5))
        paint(rectPts(wx - 12, wy + 160, 204, 14), wash='#4A528E', ink=INK, sw=.6, lite=True)
        if hash1(c * 3.3 + r * 1.7) < .35:
            paint(rectPts(wx + 110, wy + 176, 70, 48), wash='#7E86B4', ink=INK, sw=.6, lite=True)
            for k in range(3):
                G.c.drawLine(wx + 116, wy + 186 + k * 10, wx + 174, wy + 186 + k * 10, skia.Paint(AntiAlias=True, Color=skcol(INK, .4), StrokeWidth=1.5))
        elif hash1(c * 9.1 + r) < .45:
            # a little flower box on the sill
            paint(rectPts(wx + 20, wy + 144, 140, 22), wash='#9B6B45', ink=INK, sw=.5, lite=True)
            for k in range(5):
                G.c.drawCircle(wx + 34 + k * 28, wy + 138, 9, skia.Paint(AntiAlias=True, Color=skcol(PETALS[(k + c) % 6], .95)))
    # her window: bigger, warm, with the fairy lights inside
    r, c, wx, wy = 1, 2, 60 + 2 * 290 - 20, 360
    ww, wh = 220, 200
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(wx, wy, ww, wh))
    gradRect(wx, wy, ww, wh, ['#FFD594', '#F2A96A'])
    fairyLights(t, wx - 10, wx + ww + 10, wy + 14, 14, 7, key='aptfl')
    if inside:
        inside(wx, wy, ww, wh)
    G.c.restore()
    glow(wx + ww / 2, wy + wh / 2, ww * 1.1, '#FFC976', .35)
    windowFrame(wx, wy, ww, wh, '#7A5A4E', bars=False, key='aptwf')
    # ground floor: shop-ish wall, the entrance with a little awning and the number plate
    flatRect(-200, 640, W + 400, 260, '#4A4A86')
    boilSeed('aptgf')
    paint(rectPts(-200, 640, W + 400, 20), wash='#5A5A96', ink=INK, sw=.6, lite=True)
    dx, dy, dw, dh = 980, 690, 170, 210
    glow(dx + dw / 2, dy + dh / 2, 260, '#FFD48A', .4 * doorK)
    paint(rectPts(dx - 16, dy - 16, dw + 32, dh + 16), wash='#6B4A3E', ink=INK, sw=.9, lite=True)
    paint(rectPts(dx, dy, dw, dh), wash=mixCol('#2A2440', '#FFDFA0', doorK), ink=INK, sw=.7, lite=True)
    if doorK < 1:
        w = dw * (1 - doorK)
        paint(rectPts(dx, dy, max(3, w), dh), wash='#8E5E3E', ink=INK, sw=.8, lite=True)
        G.c.drawCircle(dx + w - 18, dy + dh * .55, 6, skia.Paint(AntiAlias=True, Color=skcol('#F2C53D')))
    for i in range(5):
        paint([[dx - 40 + i * 50, dy - 50], [dx + 10 + i * 50, dy - 50], [dx + 10 + i * 50, dy - 22], [dx - 15 + i * 50, dy - 14], [dx - 40 + i * 50, dy - 22]],
              wash='#E8476E' if i % 2 == 0 else '#FFF6E8', washOp=230, ink=INK, sw=.5, lite=True)
    paint(rrPts(dx + dw + 30, dy + 20, 70, 44, 8), wash='#E8E1D2', ink=INK, sw=.6, lite=True)
    text('3-2', dx + dw + 65, dy + 42, 26, '#3A3550', shadow=False)
    # ground-floor windows
    for i, gx in enumerate((120, 420, 1400, 1700)):
        paint(rectPts(gx, 700, 200, 140), wash='#FFD98A' if i % 2 else '#2A2850', washOp=220, ink=INK, sw=.7, lite=True)
    # pavement
    flatRect(-200, 900, W + 400, 300, '#3A3658')
    flatRect(-200, 900, W + 400, 14, '#6A6687')
    for i in range(12):
        G.c.drawLine(i * 180 - 40, 914, i * 180 - 100, 1200, skia.Paint(AntiAlias=True, Color=skcol('#2A2648', .6), StrokeWidth=2))
    # props on the pavement: bike, flower pots, mailbox, lamp
    bike(300, 905, 46, '#E8574E', key='aptbk')
    for i, px in enumerate((880, 1200)):
        boilSeed(f'aptpot{i}')
        paint([[px - 34, 905], [px + 34, 905], [px + 26, 845], [px - 26, 845]], wash='#C9774E', ink=INK, sw=.6, lite=True)
        paint(ellPts(px, 815, 46, 40, 16), wash='#4E8A4E', fill='#3A6A3E', fillOp=60, ink=INK, sw=.6, lite=True)
        for k in range(3):
            G.c.drawCircle(px - 20 + k * 20, 800 + (k % 2) * 14, 8, skia.Paint(AntiAlias=True, Color=skcol(PETALS[(k + i) % 6])))
    streetLamp(1640, 905, 46, 1.0, key='aptlamp')
    # a cat on the second-floor ledge (watches him go)
    boilSeed('cat')
    cx, cy = 1530, 580
    paint(ellPts(cx, cy - 26, 34, 26, 16), wash='#2A2440', ink=INK, sw=.6)
    paint(ellPts(cx + 26 * (1 if catLook >= 0 else -1), cy - 52, 20, 18, 14), wash='#2A2440', ink=INK, sw=.6)
    for s_ in (-1, 1):
        ex = cx + 26 * (1 if catLook >= 0 else -1) + s_ * 8
        paint([[ex - 8, cy - 62], [ex, cy - 80], [ex + 8, cy - 62]], wash='#2A2440', ink=None)
        G.c.drawCircle(ex, cy - 54, 3.2, skia.Paint(AntiAlias=True, Color=skcol('#FFE36E')))
    inkLine([[cx - 30, cy - 10], [cx - 60, cy + 30], [cx - 50, cy + 60]], 2.2, '#2A2440', 'ink', .5)


# ======================================================================== kitchen (S05)
def kettle(x, y, s, t, heat=0.0, lidPop=0.0, key='kt', lidHop=-1.0):
    """(x, y) = base centre on the stove; heat 0..1 (steam), lidPop = seconds since the lid popped (<0 = on)"""
    boilSeed(key)
    paint([[x - 1.6 * s, y], [x + 1.6 * s, y], [x + 1.3 * s, y - 1.6 * s], [x - 1.3 * s, y - 1.6 * s]], wash=mixCol('#E8E1D2', '#F2A07A', heat * .6), fill='#C9C0AE',
          fillOp=60, ink=INK, sw=1.0, curv=.3)
    paint([[x + 1.4 * s, y - .6 * s], [x + 2.6 * s, y - 1.6 * s], [x + 2.75 * s, y - 1.45 * s], [x + 1.5 * s, y - .2 * s]], wash='#C9C0AE', ink=INK, sw=.8)
    inkLine([[x - 1.0 * s, y - 1.6 * s], [x - .8 * s, y - 2.4 * s], [x + .8 * s, y - 2.4 * s], [x + 1.0 * s, y - 1.6 * s]], 2.4, '#3A3550', 'ink', .5)
    lx, ly, rot = x, y - 1.75 * s, 0
    if lidPop >= 0:
        lx, ly, rot = x + 120 * lidPop, y - 1.75 * s - 600 * lidPop + 1400 * lidPop * lidPop, lidPop * 12
        if ly > y - 1.75 * s:
            ly = y - 1.75 * s
    elif lidHop >= -.04:
        hh = lidHop + .04
        ly -= 1.3 * s * abs(math.sin(hh * 18)) * math.exp(-hh * 2.5)
        rot = .18 * math.sin(hh * 30) * math.exp(-hh * 2)
    push()
    translate(lx, ly)
    rotate(rot)
    paint(ellPts(0, 0, .9 * s, .25 * s, 16), wash='#C9C0AE', ink=INK, sw=.8)
    paint(ellPts(0, -.25 * s, .2 * s, .15 * s, 10), wash='#3A3550', ink=None)
    pop()
    if heat > .05:
        for i in range(int(3 + 6 * heat)):
            ph = frac(t * (1.2 + heat) + i / (3 + 6 * heat))
            sx_, sy_ = x + 2.7 * s + ph * 160 * heat, y - 1.6 * s - ph * 240 * heat
            puff(sx_, sy_, 10 + 22 * ph * heat, col='#FFFFFF', key=f'{key}st{i}', ink=False, a=(1 - ph) * .8)


def kitchen(t, warm=0.0):
    c1 = mixCol('#F7E7C8', '#F7B48A', warm)
    gradRect(-200, -200, W + 400, H + 400, [c1, mixCol('#EAD2A8', '#E8826A', warm)])
    # tiles
    for r in range(-1, 9):
        for c in range(-1, 18):
            G.c.drawRect(skia.Rect.MakeXYWH(c * 120 + (60 if r % 2 else 0), 300 + r * 70, 116, 66),
                         skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .25)))
    # window with a night view and checked curtains
    windowView(1180, 70, 420, 260, t, key='kwv', moonXY=(1520, 120))
    windowFrame(1180, 70, 420, 260, '#B98552', key='kwf')
    for s_ in (-1, 1):
        boilSeed(f'kcur{s_}')
        x0 = 1180 + (0 if s_ < 0 else 420)
        paint([[x0, 60], [x0 - s_ * 110, 60], [x0 - s_ * 80, 200], [x0, 240]], wash='#F28FA0', fill='#C9587E', fillOp=40, ink=INK, sw=.7)
    # shelf with jars and a herb pot
    boilSeed('kshelf')
    paint(rectPts(120, 250, 760, 22), wash='#9B6B45', ink=INK, sw=.8)
    for i, (jx, col, lab) in enumerate([(170, '#F7D36E', '糖'), (280, '#FFFFFF', '盐'), (390, '#C8564F', '辣'), (500, '#9FD8C8', '茶')]):
        paint(rrPts(jx, 150, 84, 100, 14), wash=col, washOp=200, ink=INK, sw=.7, lite=True)
        paint(rrPts(jx - 4, 140, 92, 22, 6), wash='#B98552', ink=INK, sw=.6, lite=True)
        text(lab, jx + 42, 205, 34, '#5A4A40', face=WENKAI, shadow=False)
    paint([[640, 250], [720, 250], [710, 190], [650, 190]], wash='#C9774E', ink=INK, sw=.6)
    for k in range(5):
        a = -1.9 + k * .45
        inkLine([[680, 190], [680 + math.cos(a) * 60, 190 + math.sin(a) * 70]], 2.0, '#5E9E5A', 'ink', .4)
    wallClock(980, 160, 56, t, key='kclk')
    # hanging utensils
    inkLine([[140, 330], [700, 330]], 2.0, '#8A86A8', 'ink', 0)
    for i in range(5):
        hx = 190 + i * 110
        inkLine([[hx, 330], [hx, 420]], 2.0, '#8A86A8', 'ink', 0)
        if i % 2:
            paint(ellPts(hx, 450, 30, 34, 14), wash='#B9C2CC', ink=INK, sw=.7)
        else:
            paint(rrPts(hx - 12, 420, 24, 70, 8), wash='#B98552', ink=INK, sw=.6)
    # counter + stove
    boilSeed('kcounter')
    paint(rectPts(-200, 760, W + 400, 40), wash='#E9E3D6', ink=INK, sw=1.0)
    gradRect(-200, 800, W + 400, 400, ['#9FB3C9', '#7E92AA'])
    for i in range(5):
        paint(rectPts(40 + i * 400, 830, 360, 200), wash='#8EA2BA', ink=INK, sw=.7, lite=True)
        paint(rrPts(40 + i * 400 + 150, 860, 60, 14, 7), wash='#D9D2C2', ink=INK, sw=.5, lite=True)
    paint(rectPts(1340, 740, 420, 26), wash='#3A3550', ink=INK, sw=.8)
    for i in range(2):
        paint(ellPts(1440 + i * 220, 738, 70, 14, 16), wash='#2A2440', ink=INK, sw=.6)
        if warm > .1:
            for k in range(8):
                a = k / 8 * TAU
                paint([[1440 + i * 220 + math.cos(a) * 40, 736], [1440 + i * 220 + math.cos(a) * 52, 726 - 10 * warm], [1440 + i * 220 + math.cos(a + .2) * 46, 736]],
                      wash='#6FA8FF', washOp=200, ink=None, lite=True)


# ======================================================================== little theatre (S06, S19)
def theatre(t, signK=0.0, signTxt='侦探社', floor='#6E4630', rose=False):
    flatRect(-200, -200, W + 400, H + 400, '#1A1428')
    # back wall planks
    for i in range(-2, 22):
        flatRect(i * 100, -200, 96, 1000, '#211A33' if i % 2 else '#1D1730')
    # floor boards
    boilSeed('tfloor')
    flat([[-200, 800], [W + 200, 800], [W + 200, H + 200], [-200, H + 200]], floor)
    for i in range(-10, 30):
        x0 = 960 + (i - 10) * 90
        G.c.drawLine(960 + (x0 - 960) * .55, 800, x0 + (x0 - 960) * .7, H + 100, skia.Paint(AntiAlias=True, Color=skcol(INK, .25), StrokeWidth=2))
    inkLine([[-200, 800], [W + 200, 800]], 1.4, INK, 'ink', 0)
    # footlights
    for i in range(14):
        fx = 60 + i * 140
        paint(ellPts(fx, 1040, 34, 14, 12), wash='#3A3550', ink=INK, sw=.6, lite=True)
        glow(fx, 1030, 70, '#FFE2A0', .35)
    # curtains + valance
    for s_ in (-1, 1):
        boilSeed(f'tcur{s_}')
        x0 = 960 + s_ * 1100
        x1 = 960 + s_ * 760
        pts = [[x0, -200], [x1, -200]]
        for i in range(12):
            yy = -200 + i * 110
            pts.append([x1 + s_ * (math.sin(i * 1.1) * 18 + (yy / H) ** 2 * 100), yy])
        pts += [[x0, H + 200]]
        paint(pts, wash='#C8324A', fill='#8E1E35', fillOp=70, ink=INK, sw=1.3)
        for k in range(1, 5):
            xx = lerp(x0, x1, k / 5)
            inkLine([[xx, -200], [xx + s_ * 20, 1000]], .7, '#8E1E35', 'inkfine', .3)
    boilSeed('tval')
    pts = [[-200, -200], [W + 200, -200], [W + 200, 60]]
    for i in range(16, -1, -1):
        x = -200 + i * (W + 400) / 16
        pts.append([x, 60 + 35 * abs(math.sin(i * math.pi / 2))])
    paint(pts, wash='#C8324A', fill='#8E1E35', fillOp=60, ink=INK, sw=1.2)
    for i in range(16):
        G.c.drawCircle(-200 + (i + .5) * (W + 400) / 16, 95, 9, skia.Paint(AntiAlias=True, Color=skcol('#F2C53D')))
    # light-box sign
    boilSeed('tsign')
    w = textW(signTxt, 76) + 120
    paint(rrPts(960 - w / 2, 120, w, 120, 20), wash=mixCol('#2A2440', '#3A2A50', signK), ink=INK, sw=1.2)
    paint(rrPts(960 - w / 2 + 12, 132, w - 24, 96, 14), ink=mixCol('#555555', '#FFD84A', signK), sw=1.6)
    if signK > .05:
        glow(960, 180, w * .8, '#FFD84A', .8 * signK)
    text(signTxt, 960, 180, 76, mixCol('#6A6080', '#FFF3C4', signK), stroke=INK if signK > .5 else None, strokeW=8, shadow=False)
    for i in range(10):
        bx = 960 - w / 2 + 10 + i * (w - 20) / 9
        G.c.drawCircle(bx, 116, 7, skia.Paint(AntiAlias=True, Color=skcol(mixCol('#6A6080', '#FFF3C4', signK))))
        G.c.drawCircle(bx, 244, 7, skia.Paint(AntiAlias=True, Color=skcol(mixCol('#6A6080', '#FFF3C4', signK))))


# ======================================================================== fortune tent (S08)
def candle(x, y, h, t, key='cd'):
    boilSeed(key)
    paint(rectPts(x - 16, y - h, 32, h), wash='#FFF6E2', fill='#E9DCC0', fillOp=50, ink=INK, sw=.7, lite=True)
    paint(ellPts(x, y, 34, 10, 14), wash='#C99A2E', ink=INK, sw=.6, lite=True)
    fl = 1 + .15 * math.sin(onTwos(t) * 23 + x)
    glow(x, y - h - 18, 90 * fl, '#FFC976', .7)
    paint([[x, y - h - 40 * fl], [x + 9, y - h - 12], [x, y - h - 2], [x - 9, y - h - 12]], wash='#FFD45C', ink=INK, sw=.4, curv=.5)
    inkLine([[x, y - h], [x, y - h - 8]], .8, INK, 'ink', 0)


def tarot(x, y, rot, face, key='tr'):
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rrPts(-56, -90, 112, 180, 10), wash='#3A2A5E', ink=INK, sw=.8, lite=True)
    paint(rrPts(-46, -80, 92, 160, 8), wash='#F7E7C8' if face else '#5B3F8C', ink=INK, sw=.5, lite=True)
    if face == 'heart':
        paint(heartPts(0, -6, 28, 18), wash=C['heart'], ink=INK, sw=.5)
    elif face == 'apple':
        apple(0, 0, 26, key=key + 'ap')
    elif face == 'moon':
        paint(ellPts(0, 0, 26, 26, 18), wash='#FFE36E', ink=INK, sw=.5)
        paint(ellPts(10, -8, 22, 22, 18), wash='#F7E7C8', ink=None)
    else:
        paint(starPts(0, 0, 30, .45, 5), wash='#FFE36E', ink=INK, sw=.5)
    pop()


# ======================================================================== evidence wall (S09)
def evidenceWall(t):
    herRoom(t, board=True)
    corkBoard(160, 110, 1600, 640, key='cork9')
    # a city map pinned in the corner, sticky notes, a calendar page
    boilSeed('map9')
    paint(rectPts(1420, 520, 300, 200), wash='#E9F0D8', ink=INK, sw=.7, lite=True)
    for i in range(6):
        inkLine([[1420, 540 + i * 32], [1720, 560 + i * 26]], .6, '#B9C2A8', 'inkfine', .2)
        inkLine([[1440 + i * 50, 520], [1460 + i * 46, 720]], .6, '#B9C2A8', 'inkfine', .2)
    inkLine([[1450, 700], [1520, 640], [1600, 660], [1680, 560]], 1.6, '#E03A4E', 'ink', .3)
    paint(heartPts(1680, 556, 14, 14), wash='#E03A4E', ink=None)
    stickyNote(300, 640, 52, .12, '#FFE36E', '23:47？', key='sn9a')
    stickyNote(1260, 640, 48, -.1, '#F7C6D2', '老地方？', key='sn9b')
    stickyNote(240, 230, 44, -.15, '#BFE3F5', '小苹果=?', key='sn9c')


# ======================================================================== the 「老地方」 hilltop (S23–S25, S27, S29–S32)
def oldGround(x):
    """gentle hilltop: flat around x≈800, falls away to both sides"""
    return 790 + .00012 * (x - 800) ** 2


def picnic(x, y, w, d, key='pic'):
    """checked blanket in perspective, front edge centred at (x, y)"""
    boilSeed(key)
    P = [[x - w / 2, y], [x + w / 2, y], [x + w * .38, y - d], [x - w * .38, y - d]]
    paint(P, wash='#FFF6E8', ink=INK, sw=.9)
    n = 6
    for i in range(n):
        for j in range(3):
            if (i + j) % 2:
                continue
            a0, a1 = i / n, (i + 1) / n
            b0, b1 = j / 3, (j + 1) / 3

            def pt(a, b):
                xl = lerp(x - w / 2, x - w * .38, b)
                xr = lerp(x + w / 2, x + w * .38, b)
                return [lerp(xl, xr, a), lerp(y, y - d, b)]
            paint([pt(a0, b0), pt(a1, b0), pt(a1, b1), pt(a0, b1)], wash='#E8574E', washOp=200, ink=None, lite=True)


def basket(x, y, s, key='bsk', apples=4):
    boilSeed(key)
    inkLine([[x - 1.2 * s, y - 1.2 * s], [x - .6 * s, y - 2.6 * s], [x + .6 * s, y - 2.6 * s], [x + 1.2 * s, y - 1.2 * s]], max(1.5, s / 12), '#9B6B45', 'ink', .6)
    for i in range(apples):
        apple(x - .9 * s + i * .6 * s, y - 1.3 * s - (i % 2) * .25 * s, .42 * s, key=f'{key}a{i}', rot=i * .5)
    paint([[x - 1.5 * s, y - 1.2 * s], [x + 1.5 * s, y - 1.2 * s], [x + 1.15 * s, y], [x - 1.15 * s, y]], wash='#C99A5E', fill='#9B6B45', fillOp=60, ink=INK, sw=.9)
    for k in range(4):
        G.c.drawLine(x - 1.4 * s + k * .1 * s, y - 1.0 * s + k * .3 * s, x + 1.4 * s - k * .1 * s, y - 1.0 * s + k * .3 * s,
                     skia.Paint(AntiAlias=True, Color=skcol('#8A5A34', .6), StrokeWidth=2))


def lantern(x, y, r, t, on=1.0, col='#F28FA0', key='ln'):
    sw_ = math.sin(t * 1.7 + x) * .06
    push()
    translate(x, y)
    rotate(sw_)
    inkLine([[0, -r * 2.2], [0, -r * 1.05]], .7, INK, 'inkfine', 0)
    if on > .05:
        glow(0, 0, r * 3.2, '#FFD48A', .6 * on)
    boilSeed(key)
    paint(ellPts(0, 0, r, r * 1.1, 20), wash=mixCol(col, '#FFF1C2', .35 * on), ink=INK, sw=.7)
    for k in (-.5, 0, .5):
        inkLine([[k * r, -r * 1.05], [k * r * 1.25, 0], [k * r, r * 1.05]], .5, mixCol(col, INK, .3), 'inkfine', .5)
    paint(rectPts(-r * .35, -r * 1.2, r * .7, r * .2), wash='#3A3550', ink=None, lite=True)
    paint(rectPts(-r * .35, r * 1.05, r * .7, r * .2), wash='#3A3550', ink=None, lite=True)
    pop()


TREE_X = 380


def treeLights(t, x, y, s, on=1.0, key='tl'):
    """strings of fairy lights draped over bigTreeSide(x, y, s)"""
    for j, (dy, half, sag, n) in enumerate([(-5.0, 2.6, .35, 13), (-4.3, 3.0, .45, 15), (-3.6, 2.5, .3, 12)]):
        fairyLights(t + j, x - half * s, x + half * s, y + dy * s, sag * s, n, key=f'{key}{j}', a=on)


def oldPlace(t, nightK=1.0, decor=1.0, bench=True, signX=1290, key='op', tree=True, lanterns=True, sky=True, benchX=1640):
    """the hilltop: sky (night / day), town below, the big tree with fairy lights + lanterns, the 「老地方」 sign, the bench"""
    if sky:
        if nightK > .5:
            gradRect(-500, -500, W + 1000, 1400, ['#0C1140', '#26306E', '#46468A'])
            push()
            translate(120, -60)
            milkyWay(.8)
            pop()
            stars(t, 7, 150, -400, -400, W + 400, 680, 1.0, 3.0)
            mx, my = 1580, 210
            glow(mx, my, 330, '#E8E4FF', .55)
            boilSeed(key + 'mn')
            paint(ellPts(mx, my, 64, 64, 30), wash='#FFF8E4', ink=None)
            paint(ellPts(mx + 18, my - 12, 12, 9, 10), wash='#EDE6D0', washOp=150, ink=None, lite=True)
        else:
            gradRect(-500, -500, W + 1000, 1400, ['#7EC4EE', '#BFE3F5', '#F2F8FC'])
            glow(1600, 140, 300, '#FFF6D0', .8)
            boilSeed(key + 'sun')
            paint(ellPts(1600, 140, 60, 60, 28), wash='#FFE58A', ink=INK, sw=.8)
            for i, (px, py, s_) in enumerate([(300, 150, 34), (980, 90, 26), (1300, 260, 22)]):
                puff(px + 20 * math.sin(t * .2 + i), py, s_, key=f'{key}pf{i}')
    # far town and river
    boilSeed(key + 'mt')
    P = [[-300, 900], [-300, 700]] + [[-300 + i * 120, 700 - 50 * abs(math.sin(i * .7)) - 26 * hash1(i * 3.3)] for i in range(23)] + [[W + 300, 900]]
    paint(P, wash=mixCol('#9FB8D8', '#1C2252', nightK), ink=None, lite=True)
    flatRect(-300, 720, W + 600, 120, mixCol('#B8C8DC', '#1A1E48', nightK))
    for i in range(60):
        x = -200 + hash1(i * 3.1) * (W + 400)
        yy = 728 + hash1(i * 5.3) * 60
        if nightK > .5:
            G.c.drawCircle(x, yy, 2.4, skia.Paint(AntiAlias=True, Color=skcol(['#FFD98A', '#FFB98A', '#FFF1C2'][i % 3], .5 + .4 * math.sin(t + i))))
        else:
            G.c.drawRect(skia.Rect.MakeXYWH(x, yy - 14, 16, 16), skia.Paint(AntiAlias=True, Color=skcol(['#E8C9B0', '#D9B8C8', '#C8D3E8'][i % 3])))
    boilSeed(key + 'rv')
    paint([[-300, 772], [W + 300, 766], [W + 300, 800], [-300, 808]], wash=mixCol('#9FD3F0', '#2A3478', nightK), ink=None, lite=True)
    # the hill
    hc = mixCol('#8DC66A', '#1C3044', nightK)
    hd = mixCol('#6EA650', '#122236', nightK)
    boilSeed(key + 'h')
    P = [[-300, H + 400]] + [[x, oldGround(x)] for x in range(-300, W + 320, 60)] + [[W + 300, H + 400]]
    paint(P, wash=hc, fill=hd, fillOp=90, ink=INK, sw=1.1, curv=.2)
    for i in range(60):
        x = -250 + hash1(i * 1.7) * (W + 500)
        y = oldGround(x) + 20 + hash1(i * 4.4) ** 1.4 * 300
        sw_ = math.sin(t * 1.5 + i) * 6
        boilSeed(f'{key}g{i}')
        for j in range(3):
            inkLine([[x + j * 8, y], [x + j * 8 + sw_ + (j - 1) * 6, y - 22 - 12 * hash1(i + j)]], .8, mixCol(hc, '#CFE6B0', .35), 'inkfine', .3)
    if tree:
        ty = oldGround(TREE_X) + 26
        bigTreeSide(TREE_X, ty, 120, t, key=key + 'tree', night=nightK * .85, flowers=True)
        if decor > 0:
            treeLights(t, TREE_X, ty, 120, decor, key=key + 'tl')
            if lanterns:
                for i, (dx, dy, col) in enumerate([(-1.9, -3.25, '#F28FA0'), (-.4, -3.0, '#FFD45C'), (1.4, -3.3, '#9FD8C8'), (2.6, -3.05, '#F28FA0')]):
                    lantern(TREE_X + dx * 120, ty + dy * 120, 26, t, decor, col, key=f'{key}ln{i}')
    if signX:
        sign(signX, oldGround(signX) + 10, '老地方', 1.0, key=key + 'sg')
        if decor > 0 and nightK > .5:
            fairyLights(t + 2, signX - 90, signX + 110, oldGround(signX) - 240, 18, 6, key=key + 'sgl', a=decor)
    if bench:
        bx = benchX
        return parkBench(bx, oldGround(bx) + 30, 330, 110, 120, key=key + 'bn', night=nightK)
    return None


# ======================================================================== seasons
def springField(t):
    gradRect(-300, -300, W + 600, 1000, ['#BFE3F5', '#FBE0EA'])
    for i, (px, py, s_) in enumerate([(330, 150, 34), (1050, 110, 26), (1650, 190, 30)]):
        puff(px + 14 * math.sin(t * .3 + i), py, s_, key=f'sp{i}')
    kite(1450, 230 + 20 * math.sin(t * 1.3), 60, key='spkite', t=t)
    inkLine([[1450, 290], [1600, 520], [1700, 700]], .6, INK, 'inkfine', .6)
    # far hills with tiny houses
    boilSeed('sphill')
    paint([[-300, 620]] + [[x, 560 - 50 * math.sin(x / 300)] for x in range(-300, W + 320, 80)] + [[W + 300, 620], [W + 300, 900], [-300, 900]],
          wash='#B8E39A', ink=INK, sw=.8, curv=.3)
    for i, hx in enumerate((520, 640, 1180)):
        boilSeed(f'sph{i}')
        paint(rectPts(hx, 540, 60, 46), wash='#FFF6E2', ink=INK, sw=.6, lite=True)
        paint([[hx - 8, 540], [hx + 30, 510], [hx + 68, 540]], wash=['#E8574E', '#5B7FC4', '#E8B04A'][i], ink=INK, sw=.6, lite=True)
    flat([[-300, 640], [W + 300, 620], [W + 300, H + 300], [-300, H + 300]], '#9ED27A')
    bigTreeSide(1700, 760, 110, t, key='sptree', col='#7CC36B', dk='#4E9A47', flowers=True)
    for i in range(40):
        bloom(-20 + hash1(i * 2.1) * 1960, 660 + hash1(i * 4.7) * 120, 12, 1, PETALS[i % 6], key=f'spb{i}', stem=False)
    picnic(330, 860, 420, 120, key='sppic')
    basket(400, 820, 40, key='spbsk')
    bike(1480, 760, 36, '#5B7FC4', key='spbike', flip=True)


def wheatScene(t, waveX, wavesOn):
    gradRect(-300, -300, W + 600, 900, ['#F4A7A0', '#F7D6A0'])
    glow(960, 480, 600, '#FFC07A', .6)
    boilSeed('sun14')
    paint(ellPts(960, 500, 120, 120, 30), wash='#FFD06A', ink=INK, sw=1)
    for i, (px, py, s_) in enumerate([(380, 180, 30), (1500, 140, 36)]):
        puff(px, py, s_, col='#FFE8D8', key=f'wcl{i}')
    boilSeed('wh14')
    paint([[-300, 600]] + [[x, 540 - 40 * math.sin(x / 260 + 1)] for x in range(-300, W + 320, 80)] + [[W + 300, 620], [W + 300, 900], [-300, 900]],
          wash='#E6A15A', ink=INK, sw=.8, curv=.3)
    # farmhouse and windmill on the ridge
    boilSeed('farm')
    paint(rectPts(1460, 480, 150, 90), wash='#F2D9B8', ink=INK, sw=.7, lite=True)
    paint([[1445, 480], [1535, 420], [1625, 480]], wash='#B8574E', ink=INK, sw=.7, lite=True)
    paint(rectPts(1500, 510, 30, 30), wash='#FFD98A', ink=INK, sw=.5, lite=True)
    wmx, wmy = 1760, 420
    paint([[wmx - 22, 560], [wmx + 22, 560], [wmx + 12, wmy], [wmx - 12, wmy]], wash='#E9E3D6', ink=INK, sw=.7, lite=True)
    for k in range(4):
        a = t * 1.3 + k * math.pi / 2
        paint([[wmx, wmy], [wmx + math.cos(a) * 110, wmy + math.sin(a) * 110], [wmx + math.cos(a + .25) * 100, wmy + math.sin(a + .25) * 100]],
              wash='#FFF6E2', ink=INK, sw=.6)
    flat([[-300, 600], [W + 300, 600], [W + 300, H + 300], [-300, H + 300]], '#E9B44C')
    # the path between the fields
    flat([[880, 600], [1040, 600], [1360, H + 80], [560, H + 80]], '#D9A04A')
    for r in range(4):
        y0 = 640 + r * 110
        hh = 110 + r * 40
        for i in range(34 - r * 4):
            x = -60 + i * (W + 120) / (33 - r * 4) + (r % 2) * 20
            if 760 < x < 1180 and r >= 1:
                continue
            sway = .12 * math.sin(t * 2 + i * .4) + .5 * math.exp(-((x - waveX) / 220) ** 2) * wavesOn
            wheat(x, y0 + hh, hh, sway, key=f'w14{r}{i}', col=['#E9B44C', '#F0C25A', '#E2A63E', '#F2C866'][r])
    # scarecrow
    boilSeed('scare')
    sx, sy = 420, 760
    inkLine([[sx, sy + 120], [sx, sy - 120]], 4, '#8A5A34', 'ink', 0)
    inkLine([[sx - 110, sy - 50], [sx + 110, sy - 60]], 4, '#8A5A34', 'ink', 0)
    paint(rectPts(sx - 60, sy - 70, 120, 120), wash='#7FB1B5', fill='#5B8A8E', fillOp=60, ink=INK, sw=.8)
    paint(ellPts(sx, sy - 120, 44, 44, 18), wash='#E9D3A8', ink=INK, sw=.8)
    paint([[sx - 70, sy - 140], [sx + 70, sy - 140], [sx, sy - 210]], wash='#C99A5E', ink=INK, sw=.8)
    for s_ in (-1, 1):
        inkLine([[sx + s_ * 16 - 8, sy - 126], [sx + s_ * 16 + 8, sy - 114]], 1.4, INK, 'ink', 0)
        inkLine([[sx + s_ * 16 + 8, sy - 126], [sx + s_ * 16 - 8, sy - 114]], 1.4, INK, 'ink', 0)
    inkLine([[sx - 16, sy - 96], [sx, sy - 90], [sx + 16, sy - 96]], 1.2, INK, 'ink', .5)


def snowCap(pts, key='cap'):
    boilSeed(key)
    paint(pts, wash='#FFFFFF', fill='#DDE6F2', fillOp=60, ink=INK, sw=.6, curv=.3, lite=True)


def winterCorner(t):
    gradRect(-300, -300, W + 600, 1000, ['#5A6AA8', '#9FB0D8'])
    stars(t, 15, 20, -200, -200, W + 200, 200, .5, 2.4)
    # two shopfronts with snow on the awnings
    for i, (sx, name, lit, kind) in enumerate([(-60, '面包', '#FFE59A', 'bread'), (300, '咖啡', '#FFCF85', 'cups'), (1340, '花店', '#F59BB0', 'flowers'),
                                              (1640, '书店', '#9FE0FF', 'books')]):
        shopFront2(sx, 250, 300, 420, name, lit, kind, t, key=f'wsf{i}', rain=False)
        snowCap([[sx + 6, 316], [sx + 296, 316], [sx + 300, 330], [sx + 150, 340], [sx + 2, 330]], key=f'wcap{i}')
    # a brick wall in the middle with a poster
    boilSeed('wwall')
    paint(rectPts(600, 250, 740, 420), wash='#8E6A7A', fill='#6E4A5A', fillOp=60, ink=INK, sw=.8, lite=True)
    for r in range(10):
        for c in range(10):
            G.c.drawRect(skia.Rect.MakeXYWH(600 + c * 74 + (37 if r % 2 else 0), 254 + r * 42, 70, 38), skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .05)))
    paint(rectPts(860, 330, 220, 280), wash='#FFF6E2', ink=INK, sw=.7, lite=True)
    text('冬日市集', 970, 380, 40, '#C8564F', face=WENKAI, shadow=False)
    snowflakes(0, 3, 8, 880, 420, 1060, 590, 10)
    # snowy ground
    flat([[-300, 670], [W + 300, 670], [W + 300, H + 300], [-300, H + 300]], '#F4F8FD')
    for i in range(30):
        x = hash1(i * 3.7) * W
        G.c.drawOval(skia.Rect.MakeXYWH(x, 700 + hash1(i * 2.1) * 360, 120, 18), skia.Paint(AntiAlias=True, Color=skcol('#DDE6F2', .6)))
    streetLamp(200, 860, 46, 1.0, key='wlamp')
    snowCap([[176, 860 - 6 * 46 - 14], [224, 860 - 6 * 46 - 14], [216, 860 - 6 * 46 - 24], [184, 860 - 6 * 46 - 24]], key='wlcap')
    # bench with snow
    boilSeed('wbench')
    paint(rectPts(1500, 840, 300, 20), wash='#B9784E', ink=INK, sw=.8, lite=True)
    paint(rectPts(1500, 780, 300, 18), wash='#B9784E', ink=INK, sw=.8, lite=True)
    for lx in (1520, 1770):
        paint(rectPts(lx, 780, 14, 120), wash='#3A3550', ink=INK, sw=.6, lite=True)
    snowCap([[1496, 840], [1804, 840], [1790, 826], [1510, 826]], key='wbcap')
    # a hot cocoa on the bench
    mug(1700, 840, .55, key='wcocoa', col=HIS_MUG, steam=1.0, t=t)


# ======================================================================== deep sea
def coral(x, y, s, col, key='cor'):
    boilSeed(key)
    for k in range(5):
        a = -math.pi / 2 + (k - 2) * .35
        L = s * (1.6 + .5 * hash1(k + len(key)))
        pts = [[x, y], [x + math.cos(a) * L * .5, y + math.sin(a) * L * .5], [x + math.cos(a) * L, y + math.sin(a) * L]]
        paint(ribbon(pts, s * .32, s * .2), wash=col, fill=mixCol(col, INK, .2), fillOp=50, ink=INK, sw=.7)
        G.c.drawCircle(pts[-1][0], pts[-1][1], s * .14, skia.Paint(AntiAlias=True, Color=skcol(mixCol(col, '#FFFFFF', .4))))


def jelly(x, y, s, t, col='#F7C6D2', key='jf'):
    p = math.sin(t * 2.4 + x) * .1
    boilSeed(key)
    pts = []
    for i in range(13):
        a = math.pi + i / 12 * math.pi
        pts.append([x + math.cos(a) * s * (1 + p), y + math.sin(a) * s * .8 * (1 - p)])
    pts += [[x + s * (1 + p), y + s * .1], [x - s * (1 + p), y + s * .1]]
    paint(pts, wash=col, washOp=200, ink=INK, sw=.6, curv=.3)
    for k in range(5):
        tx = x - s * .7 + k * s * .35
        inkLine([[tx, y + s * .1], [tx + math.sin(t * 3 + k) * 10, y + s * .9], [tx + math.sin(t * 3 + k + 1) * 14, y + s * 1.7]], .7, mixCol(col, INK, .2), 'inkfine', .6)


def chest(x, y, s, key='ch'):
    boilSeed(key)
    paint(rectPts(x - 1.6 * s, y - 1.6 * s, 3.2 * s, 1.6 * s), wash='#9B6B45', fill='#6B4A35', fillOp=60, ink=INK, sw=.9)
    paint([[x - 1.6 * s, y - 1.6 * s], [x + 1.6 * s, y - 1.6 * s], [x + 1.4 * s, y - 2.5 * s], [x - 1.4 * s, y - 2.5 * s]], wash='#8A5A34', ink=INK, sw=.9, curv=.2)
    for k in (-1, 0, 1):
        paint(rectPts(x + k * 1.1 * s - .1 * s, y - 2.5 * s, .2 * s, 2.5 * s), wash='#C99A2E', ink=None, lite=True)
    glow(x, y - 1.7 * s, 2.5 * s, '#FFE36E', .5)
    for k in range(5):
        paint(ellPts(x - .8 * s + k * .4 * s, y - 1.7 * s, .22 * s, .12 * s, 10), wash='#F2C53D', ink=INK, sw=.4)


def starfish(x, y, s, rot, col='#F59A6B', key='sfh'):
    boilSeed(key)
    paint(starPts(x, y, s, .45, 5, rot), wash=col, ink=INK, sw=.6, curv=.2)
    for k in range(5):
        a = rot + k * TAU / 5
        G.c.drawCircle(x + math.cos(a) * s * .5, y + math.sin(a) * s * .5, s * .06, skia.Paint(AntiAlias=True, Color=skcol('#FFF6E2')))


def shell(x, y, s, key='shl', col='#F7D6C8'):
    boilSeed(key)
    pts = [[x, y]]
    for i in range(9):
        a = math.pi + .15 + i / 8 * (math.pi - .3)
        pts.append([x + math.cos(a) * s, y + math.sin(a) * s])
    paint(pts, wash=col, ink=INK, sw=.6)
    for k in range(5):
        a = math.pi + .3 + k / 4 * (math.pi - .6)
        G.c.drawLine(x, y, x + math.cos(a) * s * .9, y + math.sin(a) * s * .9, skia.Paint(AntiAlias=True, Color=skcol(INK, .4), StrokeWidth=1.2))


def crab(x, y, s, t, pat=0.0, key='crab'):
    boilSeed(key)
    for s_ in (-1, 1):
        for k in range(3):
            inkLine([[x + s_ * .6 * s, y - .1 * s], [x + s_ * (1.1 + k * .15) * s, y - .3 * s + k * .1 * s], [x + s_ * (1.3 + k * .15) * s, y + .1 * s]], 1.2, '#C8443A', 'ink', .5)
    paint(ellPts(x, y - .3 * s, .9 * s, .55 * s, 18), wash='#E8574E', fill='#B8392E', fillOp=60, ink=INK, sw=.7)
    for s_ in (-1, 1):
        ang = -1.2 - (pat * .8 if s_ > 0 else 0) + .15 * math.sin(t * 6 + s_)
        cx_, cy_ = x + s_ * .8 * s, y - .6 * s
        ex, ey = cx_ + s_ * math.cos(ang) * .5 * s, cy_ + math.sin(ang) * .9 * s
        inkLine([[cx_, cy_], [ex, ey]], 1.4, '#C8443A', 'ink', 0)
        paint(ellPts(ex, ey, .28 * s, .2 * s, 12), wash='#E8574E', ink=INK, sw=.6)
        inkLine([[x + s_ * .25 * s, y - .8 * s], [x + s_ * .3 * s, y - 1.05 * s]], 1.0, INK, 'ink', 0)
        G.c.drawCircle(x + s_ * .3 * s, y - 1.1 * s, .09 * s, skia.Paint(AntiAlias=True, Color=skcol(INK)))


def seaBed(t, depth, floorY=900):
    gradRect(-300, -300, W + 600, H + 600, [mixCol('#4FA7D8', '#1D3E78', depth), mixCol('#1D3E78', '#0E1B44', depth)])
    tt = onTwos(t)
    for i in range(6):
        x = 200 + i * 320 + math.sin(tt * .7 + i) * 40
        flat([[x - 40, -80], [x + 40, -80], [x + 220, H + 80], [x + 60, H + 80]], '#BFE9FF', .07 * (1 - depth * .6))
    # far rocks
    boilSeed('rocks')
    paint([[-300, floorY - 60]] + [[x, floorY - 120 - 60 * abs(math.sin(x / 210))] for x in range(-300, W + 320, 90)] + [[W + 300, floorY], [-300, floorY]],
          wash=mixCol('#2E5A8A', '#16284E', depth), ink=None, lite=True)
    flat([[-300, floorY], [W + 300, floorY - 20], [W + 300, H + 300], [-300, H + 300]], mixCol('#D9C49A', '#5A6A8A', depth * .7))
    for i in range(30):
        x = hash1(i * 2.3) * W
        G.c.drawOval(skia.Rect.MakeXYWH(x, floorY + 10 + hash1(i * 4.1) * 160, 40, 8), skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .12)))
