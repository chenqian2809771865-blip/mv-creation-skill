# wo.py: props and sets for 《我好想你》 (苏打绿). Watercolour + boiling ink, logical canvas 1920x1080. No windows anywhere.
# His room and her room are the same flat, hers mirrored (x -> 1920 - x) and pink; text is drawn outside the mirror.
# Objects that recur: the tin of folded notes (his yellow, hers pink), the wall light switch, her white flower, her slippers.
import math
from eng import *
import eng
from clawd import *
import clawd as _cl
from props import puff, sparkle, sparkles, bubble, umbrellaAt
from props_bingbian import bedBack, blanket, door, alarmClock, bolt, P2
from bbset import pillowProp, bedsideTable, wallClock2, plant, rug, stringLights, hairClip
from sets2 import seat, bookshelf, coupleSnap
from hl import desat, tint, vignette, wtext, inkWrite, writeW, stars, rain, mug, deskLamp, WENKAI
import hanzi
import hb
from hb import calendar11, glassesDraw, thoughtCloud, woodTop, doodleHeart
from nm import heartP, postit, darkness, phoneP, plushHim, magnifierW
from common import handXY, LY, B

U = 30                      # room-scale Clawd
FLOOR = 860
BED_X, BED_W, BED_Y, BED_S = 1560, 640, 800, 26     # mattress front bottom at BED_Y (legs below)
BED_SEAT = BED_Y - 4.2 * BED_S                      # top of the mattress
DESK_X0, DESK_X1, DESK_TOP = 600, 1080, 650
CHAIR_X, CHAIR_SEAT = 470, 718
SWITCH = (-150, 640)
DOOR_X = -360
NOTE_Y = '#FBE7A1'          # his notes
NOTE_P = '#F9C9D6'          # her notes
TIN_HIM = ('#6F8FC8', '#4A659E')
TIN_HER = ('#EE9AAE', '#C0637B')
PAL_ROOM = dict(
    him=dict(wall='#D9DFEC', stripe='#C9D2E4', floor='#BB8D62', floorDk='#946A46', skirting='#F3EEE6', rug='#9CB4D8'),
    her=dict(wall='#F6DCE1', stripe='#EECAD2', floor='#C79A70', floorDk='#9E7350', skirting='#FFF6EE', rug='#F2B3C3'),
)


def X(x, who):
    return x if who == 'him' else W - x


def who_fn(who):
    return him if who == 'him' else her


def fo(base, **kw):
    d = dict(base)
    d.update(kw)
    return d


def emo(t, keys, who):
    return emotions(t, keys, ME if who == 'him' else HER)


def person(who, x, y, u, o=None, hair=0.0, glasses=False):
    """him / her; hair = white-hair amount (示例歌词占), glasses pop on with glasses=True"""
    o = dict(o or {})
    if hair > .01 or glasses:
        hats = o.get('hat')
        hl_ = list(hats) if isinstance(hats, (list, tuple)) else ([hats] if hats else [])
        if who == 'her' and 'flower' not in hl_ and not o.get('noFlower'):
            hl_.append('flower')
        if hair > .01:
            hl_ = ['whitehair'] + hl_
            o['hairK'] = hair
        o['hat'] = hl_
        if glasses:
            gd = glassesDraw(o.get('view') or 'front')
            d0 = o.get('draw')

            def dd(u_, sw):
                gd(u_, sw)
                if d0:
                    d0(u_, sw)
            o['draw'] = dd
    if who == 'her' and o.get('noFlower'):
        o.setdefault('hat', [])
    who_fn(who)(x, y, u, o)


def armToward(o, x, y, u, tx, a):
    """copy of o with the arm whose hand ends up nearer tx set to angle a; returns (o2, side)"""
    oL, oR = dict(o, aL=a), dict(o, aR=a)
    hL, hR = handXY(x, y, u, oL, 'L'), handXY(x, y, u, oR, 'R')
    return (oL, 'L') if abs(hL[0] - tx) < abs(hR[0] - tx) else (oR, 'R')


# ================================================================ paper notes and the tin
def foldedNote(x, y, s, rot=0.0, col=NOTE_Y, key='fn', a=1.0):
    """a small folded note (seen from the front or above): s = width"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-s / 2, -s * .32, s, s * .64, 1), wash=col, washOp=int(255 * a), fill=mixCol(col, INK, .12), fillOp=int(40 * a),
          ink=INK if a > .5 else None, sw=.55, lite=True)
    G.c.drawLine(-s / 2, 0, s / 2, 0, skia.Paint(AntiAlias=True, Color=skcol(mixCol(col, INK, .35), .7 * a), StrokeWidth=max(1, s * .03)))
    pop()


def tinFront(x, y, w, who='him', fill=.6, lid=0.0, glowK=0.0, key='tin', t=0.0, shake=0.0):
    """the cookie tin seen from the front; (x, y) = bottom centre. fill 0..1.4 (>1 = notes spill over the rim).
    lid 0 = closed, 1 = open (lid tipped back behind)."""
    col, dk = TIN_HIM if who == 'him' else TIN_HER
    nc = NOTE_Y if who == 'him' else NOTE_P
    h = w * .52
    push()
    translate(x + shake * math.sin(t * 60) * 3, y)
    if glowK > .01:
        glow(0, -h * .6, w * 1.1, '#FFD98A', .6 * glowK)
    boilSeed(key)
    if lid > .01:      # lid behind, tipped open
        push()
        translate(0, -h)
        rotate(-.9 * lid * (1 if who == 'him' else -1) * 0)
        paint(rrPts(-w / 2 - 4, -h * .55 * lid - 8, w + 8, h * .55 * lid + 8, 10), wash=mixCol(col, '#FFFFFF', .1), fill=dk, fillOp=50,
              ink=INK, sw=.9, lite=True)
        pop()
    # notes above the rim
    n = int(6 + 18 * clamp(fill, 0, 1.4))
    if fill > .55 or lid > .01:
        for i in range(n):
            px = (hash1(i * 3.3 + 1) - .5) * w * .82
            top = -h - (fill - .6) * h * .9 * (.4 + .6 * hash1(i * 7.1)) if fill > .6 else -h + 6
            foldedNote(px, top + 4, w * (.16 + .06 * hash1(i)), (hash1(i * 5.7) - .5) * .9, nc, key=f'{key}n{i}')
    paint(rrPts(-w / 2, -h, w, h, 12), wash=col, fill=dk, fillOp=55, ink=INK, sw=1.0)
    paint(rectPts(-w / 2, -h, w, h * .16), wash=mixCol(col, '#FFFFFF', .25), ink=INK, sw=.7, lite=True)
    # little hearts / dots on the tin
    for i in range(5):
        heartP(-w * .32 + i * w * .16, -h * .5 + (i % 2) * h * .14, w * .045, col='#FFF6EE', key=f'{key}h{i}')
    if lid < .01:
        paint(rrPts(-w / 2 - 6, -h - h * .14, w + 12, h * .2, 8), wash=mixCol(col, '#FFFFFF', .12), fill=dk, fillOp=50, ink=INK, sw=.9, lite=True)
    pop()


def tinTop(x, y, w, h, who='him', fill=.8, lid=1.0, key='tint', extra=0):
    """the tin seen from above (desk top-down shots); lid hinged at the top edge, open lid drawn above"""
    col, dk = TIN_HIM if who == 'him' else TIN_HER
    nc = NOTE_Y if who == 'him' else NOTE_P
    boilSeed(key)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x - w / 2 + 14, y - h / 2 + 18, w, h), 26, 26, skia.Paint(AntiAlias=True, Color=skcol(INK, .3)))
    if lid > .01:
        lh = h * .8 * lid
        paint(rrPts(x - w / 2, y - h / 2 - lh, w, lh, 22), wash=mixCol(col, '#FFFFFF', .1), fill=dk, fillOp=45, ink=INK, sw=1.0, lite=True)
        for i in range(4):
            heartP(x - w * .3 + i * w * .2, y - h / 2 - lh * .5, w * .05 * lid, col='#FFF6EE', key=f'{key}lh{i}')
    paint(rrPts(x - w / 2, y - h / 2, w, h, 22), wash=col, fill=dk, fillOp=50, ink=INK, sw=1.1)
    paint(rrPts(x - w / 2 + 14, y - h / 2 + 14, w - 28, h - 28, 16), wash=mixCol(dk, INK, .25), ink=INK, sw=.6, lite=True)
    if lid > .01:
        n = int(10 + 40 * clamp(fill, 0, 1.3)) + extra
        for i in range(n):
            px = x + (hash1(i * 2.7 + 3) - .5) * (w - 70)
            py = y + (hash1(i * 4.1 + 1) - .5) * (h - 60)
            foldedNote(px, py, w * (.17 + .05 * hash1(i * 1.3)), (hash1(i * 6.1) - .5) * 1.6, nc, key=f'{key}n{i}')
    else:
        paint(rrPts(x - w / 2 - 6, y - h / 2 - 6, w + 12, h + 12, 24), wash=mixCol(col, '#FFFFFF', .12), fill=dk, fillOp=45, ink=INK, sw=1.0)
        for i in range(5):
            heartP(x - w * .32 + i * w * .16, y + (i % 2) * 20 - 10, w * .05, col='#FFF6EE', key=f'{key}ch{i}')


def stickyNote(x, y, w, rot=0.0, col=NOTE_Y, key='sn', fold=0.0):
    """a square sticky note seen from above; fold 0..1 squashes it into a folded strip"""
    push()
    translate(x, y)
    rotate(rot)
    scale(1, 1 - .62 * fold)
    boilSeed(key)
    paint(rectPts(-w / 2 + 8, -w / 2 + 12, w, w), wash=INK, washOp=50, ink=None)
    paint(rectPts(-w / 2, -w / 2, w, w, 1.5), wash=col, fill=mixCol(col, INK, .1), fillOp=35, ink=INK, sw=.8)
    paint(rectPts(-w / 2, -w / 2, w, w * .14), wash=mixCol(col, INK, .07), ink=None)
    if fold > .02:
        G.c.drawLine(-w / 2, 0, w / 2, 0, skia.Paint(AntiAlias=True, Color=skcol(mixCol(col, INK, .4), .8), StrokeWidth=3))
    pop()


def writeTip(txt, x0, y0, size, prog, gap=.08):
    """where the pen nib is when inkWrite(txt, x0, y0, size, prog) has written up to prog"""
    chars = list(txt)
    lens = [hanzi.char_len(c) if c != ' ' else 0 for c in chars]
    tot = sum(lens) or 1
    done = clamp(prog) * tot
    x = x0
    k = size / 1024.0
    for ch, Ln in zip(chars, lens):
        if ch == ' ':
            x += size * .45
            continue
        if done <= Ln:
            for path, med, L in hanzi.glyph(ch):
                if done <= L:
                    a = hanzi.partial_polyline(med, max(.001, done / L))
                    px, py = a[-1]
                    return x + px * k, y0 + py * k
                done -= L
            return x + size * .5, y0 + size * .5
        done -= Ln
        x += size * (1 + gap)
    return x - size * gap, y0 + size * .6


def fountainPen(x, y, s, ang=-.85, key='fpen', col='#2E3A6E'):
    """a fountain pen whose nib touches (x, y); no hand — the pen writes by itself"""
    push()
    translate(x, y)
    rotate(ang)
    boilSeed(key)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(s * .3 + 10, -s * .16 + 14, s * 3.2, s * .32), s * .14, s * .14,
                      skia.Paint(AntiAlias=True, Color=skcol(INK, .25)))
    paint([[0, 0], [s * .36, -s * .14], [s * .36, s * .14]], wash='#D8B04A', ink=INK, sw=.6)
    paint(rrPts(s * .34, -s * .17, s * 3.2, s * .34, s * .14), wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=.7)
    paint(rrPts(s * 1.3, -s * .19, s * .28, s * .38, s * .05), wash='#D8B04A', ink=None)
    pop()


def writtenNote(txt, x, y, w, prog, t, col=NOTE_Y, key='wn', size=None, pen=True, ink_='#2B2233', fold=0.0, rot=0.0):
    """sticky note centred at (x, y) with txt hand-written (real stroke order) up to prog; the pen follows the stroke"""
    stickyNote(x, y, w, rot, col, key=key, fold=fold)
    if fold > .3:
        return
    size = size or w * .19
    tw = writeW(txt, size)
    x0, y0 = x - tw / 2, y - size * .5
    push()
    translate(x, y)
    rotate(rot)
    scale(1, 1 - .62 * fold)
    translate(-x, -y)
    inkWrite(txt, x0, y0, size, prog, col=ink_, mode='brush')
    pop()
    if pen and 0 < prog < 1:
        px, py = writeTip(txt, x0, y0, size, prog)
        fountainPen(px, py, size * .55)


# ================================================================ the room
def lightSwitch(x, y, s=1.0, on=1.0, key='sw'):
    boilSeed(key)
    paint(rrPts(x - 20 * s, y - 30 * s, 40 * s, 60 * s, 6 * s), wash='#FBF8F2', ink=INK, sw=.8)
    ty = lerp(8, -8, on) * s
    paint(rrPts(x - 7 * s, y + ty - 9 * s, 14 * s, 18 * s, 4 * s), wash='#E8E1D2', fill='#B9B1A4', fillOp=60, ink=INK, sw=.6)


def slippers(x, y, s=1.0, col='#F7A9BC', key='slp'):
    for i, dx in enumerate((-22, 22)):
        boilSeed(key + str(i))
        paint(ellPts(x + dx * s, y - 6 * s, 20 * s, 9 * s, 14), wash=col, fill=mixCol(col, INK, .25), fillOp=50, ink=INK, sw=.7)
        paint(ellPts(x + dx * s, y - 12 * s, 14 * s, 7 * s, 12), wash=mixCol(col, '#FFFFFF', .35), ink=INK, sw=.5)
        heartP(x + dx * s, y - 12 * s, 5 * s, col='#E8476E', key=key + 'h' + str(i))


def flowerMug(x, y, s=1.0, dry=0.0, flower=True, key='fm', col='#E8E1D2', steam=0.0, t=0.0):
    """his mug on the desk, her little white flower stuck in it (dry = wilted)"""
    if flower:
        boilSeed(key + 'st')
        tip = (x + lerp(4, 40, dry) * s, y - lerp(98, 70, dry) * s)
        inkLine([[x, y - 40 * s], [x + 8 * dry * s, y - 70 * s], tip], 1.1, mixCol('#6E9F58', '#8A7A5A', dry), 'ink', .5)
        push()
        translate(*tip)
        rotate(.9 * dry)
        pc = mixCol('#FFFFFF', '#D9C9A8', dry)
        for i in range(5):
            a = i / 5 * TAU
            paint(ellPts(math.cos(a) * 9 * s, math.sin(a) * 9 * s, 8 * s * (1 - .3 * dry), 6 * s, 10), wash=pc, ink=INK, sw=.45, lite=True)
        paint(ellPts(0, 0, 5 * s, 5 * s, 10), wash=mixCol('#F2C53D', '#B89A5A', dry), ink=None)
        pop()
    mug(x, y, s, key=key, col=col, steam=steam, t=t)


def stool(x, y, s=1.0, key='stool'):
    """(x, y) = floor; returns the top y"""
    boilSeed(key)
    top = y - 70 * s
    for dx in (-36, 36):
        inkLine([[x + dx * s * .7, top], [x + dx * s, y]], 2.0, '#8A5A36', 'ink', 0)
    paint(ellPts(x, top, 52 * s, 12 * s, 16), wash='#C98B5A', fill='#8A5A36', fillOp=60, ink=INK, sw=.8)
    return top - 6 * s


def chairSide(x, y, seat_y, key='chair', flip=False):
    """a simple wooden chair seen from the front-ish; back drawn behind the sitter. returns the seat top"""
    d = -1 if flip else 1
    boilSeed(key)
    paint(rectPts(x - d * 60 - 8, seat_y - 170, 16, 170), wash='#A86E44', ink=INK, sw=.7, lite=True)
    paint(rrPts(x - 66, seat_y - 4, 132, 22, 6), wash='#C98B5A', fill='#8A5A36', fillOp=50, ink=INK, sw=.8, lite=True)
    for dx in (-54, 54):
        inkLine([[x + dx, seat_y + 16], [x + dx, y]], 2.0, '#8A5A36', 'ink', 0)
    return seat_y


def deskFront(x0, x1, top, floor=FLOOR, key='desk', col='#B07A4E'):
    boilSeed(key)
    paint(rectPts(x0 - 14, top - 6, x1 - x0 + 28, 26, 2), wash=col, fill=mixCol(col, INK, .3), fillOp=50, ink=INK, sw=1.0)
    # drawer unit on the right
    dx0 = x1 - 190
    paint(rectPts(dx0, top + 20, 180, floor - top - 20), wash=mixCol(col, '#FFFFFF', .06), fill=mixCol(col, INK, .25), fillOp=40,
          ink=INK, sw=.9, lite=True)
    for i in range(3):
        yy = top + 34 + i * (floor - top - 40) / 3
        paint(rectPts(dx0 + 12, yy, 156, (floor - top - 40) / 3 - 14), wash=mixCol(col, '#FFFFFF', .12), ink=INK, sw=.6, lite=True)
        paint(ellPts(dx0 + 90, yy + 22, 9, 5, 8), wash='#F2C53D', ink=INK, sw=.4, lite=True)
    inkLine([[x0 + 10, top + 20], [x0 + 10, floor]], 2.4, mixCol(col, INK, .4), 'ink', 0)


def bedFull(t, who, night=0.0, herPillow=True, hisDent=0.0, key='bed', blanketK=1.0, lump=0.0, clip=True, tinUnder=0.0, tinGlow=0.0):
    """the bed (front view) at BED_X; returns seat top. tinUnder 0..1 = how far the tin has been pushed under (drawn in the gap)."""
    x = BED_X
    s = BED_S
    boilSeed(key + 'legs')
    for dx in (-BED_W / 2 + 30, BED_W / 2 - 30):
        paint(rectPts(x + dx - 12, BED_Y - 4, 24, FLOOR - BED_Y + 4), wash=P2['woodDk'], ink=INK, sw=.7, lite=True)
    # dark gap under the bed
    paint(rectPts(x - BED_W / 2 + 44, BED_Y, BED_W - 88, FLOOR - BED_Y - 4), wash=mixCol('#2A2440', '#000000', .2), washOp=170, ink=None)
    if tinUnder > 0:
        tx = x - 120 + 160 * clamp(tinUnder)
        tinFront(tx, FLOOR - 4, 110, who, fill=.8, glowK=tinGlow, key=key + 'tinU')
        if tinGlow > .01:
            glow(tx, FLOOR - 30, 300, '#FFD98A', .8 * tinGlow)
    pl, pr = bedBack(x, BED_Y, BED_W, s, key=key, night=night)
    if blanketK > 0:
        blanket(x, BED_Y, BED_W, s, key=key + 'blk', night=night, lump=lump, top=BED_Y - 3.0 * s)
    if clip:
        # her hair clip on her pillow
        hx = pr[0] if who == 'him' else pr[0]
        hairClip(hx + 30, pr[1] - 10, 1.0, .4, key=key + 'clip')
    return BED_Y - 3.0 * s


def roomBack(t, who='him', lightsOn=1.0, memory=False, tinOnDesk=False, tinFill=.6, flowerDry=1.0, flower=True, slippersK=1.0,
             switchOn=1.0, night=0.0, key='room', clockHM=(23, 40), bed=True, bedKw=None, calendarK=1.0, photoDrain=0.0, bedside=1.0,
             mugs=1, lamp=1.0):
    """his (or her, mirrored) room. Returns dict of handy world positions (already mirrored for her)."""
    P = PAL_ROOM[who]
    mir = who == 'her'
    if mir:
        push()
        translate(W, 0)
        scale(-1, 1)
    # wall + stripes + skirting + floor
    flatRect(-900, -900, W + 1800, FLOOR + 900, P['wall'])
    for i in range(-14, 40):
        xx = i * 90
        G.c.drawRect(skia.Rect.MakeXYWH(xx, -900, 34, FLOOR + 900), skia.Paint(Color=skcol(P['stripe'], .55)))
    flatRect(-900, FLOOR - 26, W + 1800, 26, P['skirting'])
    inkLine([[-900, FLOOR - 26], [W + 900, FLOOR - 26]], .6, INK, 'inkfine', 0)
    flatRect(-900, FLOOR, W + 1800, 900, P['floor'])
    for i in range(-10, 30):
        G.c.drawLine(i * 140, FLOOR, i * 140 - 220, FLOOR + 640, skia.Paint(AntiAlias=True, Color=skcol(P['floorDk'], .3), StrokeWidth=2))
    inkLine([[-900, FLOOR], [W + 900, FLOOR]], 1.0, INK, 'ink', 0)
    rug(BED_X - 420, FLOOR + 90, 360, 50, col=P['rug'], night=0, key=key + 'rug')
    # door + coat hooks + slippers
    door(DOOR_X, FLOOR, 32, 0.0, key=key + 'door', col='#C98B5A' if who == 'him' else '#D9A27A')
    boilSeed(key + 'hooks')
    for i in range(3):
        hx = DOOR_X + 150 + i * 46
        paint(ellPts(hx, 420, 8, 8, 10), wash='#3A3550', ink=None)
    if who == 'him':
        paint([[DOOR_X + 132, 430], [DOOR_X + 168, 430], [DOOR_X + 182, 560], [DOOR_X + 118, 560]], wash='#7FA3D6', ink=INK, sw=.7, lite=True)
    else:
        paint([[DOOR_X + 132, 430], [DOOR_X + 168, 430], [DOOR_X + 186, 540], [DOOR_X + 114, 540]], wash='#F2B3C3', ink=INK, sw=.7, lite=True)
    if slippersK > 0:
        slippers(DOOR_X + 40, FLOOR + 30, 1.1, col='#F7A9BC' if who == 'him' else '#F2A283', key=key + 'slp')
    lightSwitch(SWITCH[0], SWITCH[1], 1.0, switchOn, key=key + 'sw')
    # bookshelf
    bookshelf(40, 440, 300, FLOOR - 440, key=key + 'bs', who='her' if who == 'her' else 'him')
    # desk wall: clock (calendar drawn after the mirror)
    hh, mm = clockHM
    wallClock2(1000, 330, 46, hh, mm, night=0, key=key + 'clk')
    # photo string above the bed + string lights along the top
    photoWall(t, 1240, 1880, 300, who, drain=photoDrain, key=key + 'pw')
    stringLights(t, -300, 2300, 150, sag=60, n=26, key=key + 'sl', on=lightsOn)
    # desk + lamp + mug + tin
    deskFront(DESK_X0, DESK_X1, DESK_TOP, key=key + 'desk')
    if lamp:
        deskLamp(1010, DESK_TOP - 6, .9, on=0.0, key=key + 'dl', flip=True)
    if mugs:
        flowerMug(780, DESK_TOP - 4, 1.0, dry=flowerDry, flower=flower and who == 'him', key=key + 'mug', col='#E8E1D2' if who == 'him' else '#FFF0F3')
    if tinOnDesk:
        tinFront(900, DESK_TOP - 4, 120, who, fill=tinFill, key=key + 'tinD')
    # bedside table + plant
    if bedside:
        bedsideTable(2010, FLOOR, 24, night=0, key=key + 'bst', lampOn=0.0, clock='up', frame='up')
    plant(2260, FLOOR, 1.1, night=0, key=key + 'plant')
    out = {}
    if bed:
        out['seat'] = bedFull(t, who, key=key + 'bed', **(bedKw or {}))
    if mir:
        pop()
    if calendarK > 0:
        cx = 640 if not mir else W - 640 - 190
        calendar11(cx, 300, key=key + 'cal')
    out.update(switch=(X(SWITCH[0], who), SWITCH[1]), door=X(DOOR_X, who), bedL=X(BED_X - 150, who), bedR=X(BED_X + 150, who),
               desk=(X(DESK_X0, who), X(DESK_X1, who)), chair=X(CHAIR_X, who))
    return out


def photoWall(t, x0, x1, y, who, drain=0.0, key='pw', n=4, w=110):
    """a string of polaroids of the two of them; drain 0..n: how many have faded to blank (fractional = fading)"""
    pts = [[lerp(x0, x1, i / 20), y + 30 * math.sin(i / 20 * math.pi)] for i in range(21)]
    inkLine(pts, .8, '#B59A7A', 'inkfine', .3)
    for i in range(n):
        k = (i + .5) / n
        px, py = lerp(x0, x1, k), y + 30 * math.sin(k * math.pi)
        d = clamp(drain - i)
        polaroidMini(px, py + w * .62, w, (hash1(i * 3.1) - .5) * .18, i, d, key=f'{key}{i}')


def polaroidMini(x, y, w, rot, i, drain=0.0, key='pm', night=False):
    h = w * 1.2
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(rectPts(-w / 2 + 5, -h / 2 + 7, w, h), wash=INK, washOp=50, ink=None)
    paint(rectPts(-w / 2, -h / 2, w, h, 1), wash='#FFFDF7', ink=INK, sw=.7, lite=True)
    pw = w * .84
    px, py = -pw / 2, -h / 2 + w * .08
    if drain < .999:
        G.c.saveLayerAlpha(None, int(255 * (1 - drain)))
        G.c.save()
        G.c.clipRect(skia.Rect.MakeXYWH(px, py, pw, pw))
        snapScene(px, py, pw, i, night)
        G.c.restore()
        G.c.restore()
    if drain > .001:
        paint(rectPts(px, py, pw, pw), wash='#F1ECE4', washOp=int(255 * drain * .9), ink=None)
    paint(rectPts(px, py, pw, pw), ink=INK, sw=.5)
    G.c.drawCircle(0, -h / 2 + 6, 4, skia.Paint(AntiAlias=True, Color=skcol('#C8564F')))
    pop()


SNAPS = [(['#9FD4F2', '#F3E6C8'], 'happy'), (['#F7C6D2', '#FFF0D8'], 'love'), (['#B9E3C6', '#F6F1D0'], 'laugh'), (['#2A2D6E', '#6B5AA8'], 'happy'),
         (['#FFD9A0', '#F7A9BC'], 'love'), (['#CFE3F2', '#FFFFFF'], 'happy')]


def snapScene(x, y, w, i, night=False):
    cols, mood = SNAPS[i % len(SNAPS)]
    gradRect(x, y, w, w, cols)
    s = w / 15
    eyes_ = {'happy': 'happy', 'love': 'heart', 'laugh': 'squeeze'}[mood]
    clawd(x + w * .34, y + w * .94, s, dict(col='#EE9AAE', dk='#C0637B', lt='#FBD0DA', hat='flower', eyes=eyes_, mouth='smile', lite=True,
                                            noShadow=True, boilKey=f'sn{i}a', view='front', aL=.3, aR=.9 if i % 2 else .3))
    clawd(x + w * .68, y + w * .94, s, dict(col=PAL['clay'], dk=PAL['clayDk'], lt='#F5B394', eyes=eyes_, mouth='smile', lite=True,
                                            noShadow=True, boilKey=f'sn{i}b', view='front', aL=.9 if i % 2 == 0 else .3, aR=.3))
    if i % 3 == 1:
        heartP(x + w * .51, y + w * .22, w * .08, key=f'snh{i}')


# ================================================================ looks
def nightVeil(k, lights=(), col='#0B1030', tintCol='#36407A'):
    """after camEnd(): darken the frame toward night; lights = [(sx, sy, r, k)] in screen coords stay warm"""
    if k <= .01:
        return
    tint(tintCol, .55 * k, skia.BlendMode.kMultiply)
    darkness(.72 * k, lights, col)


def memoryLook(k=1.0):
    """after camEnd(): warm, bright, slightly glowing — the memories"""
    if k <= .01:
        return
    tint('#FFE0A8', .28 * k, skia.BlendMode.kSoftLight)
    tint('#FFF4DC', .12 * k, skia.BlendMode.kScreen)
    vignette(.25 * k, '#FFF3DA')


def scr(x, y):
    return toScreen(x, y)


def lightOn(t, t_on, d=.12):
    """0..1 as the ceiling light snaps on at t_on (slight flicker)"""
    if t < t_on - .01:
        return 0.0
    a = t - t_on
    if a < .04:
        return .55
    if a < .08:
        return .3
    return clamp(.6 + a / d)


def splitScreen(t, left, right, gap=6, line=True):
    """draw left(t) into the left half and right(t) into the right half; each scene is composed for the full 1920 frame with its
    subject near x = 960, and gets shifted so the subject sits in the middle of its half"""
    c = G.c
    for i, fn in enumerate((left, right)):
        c.save()
        c.clipRect(skia.Rect.MakeXYWH(0 if i == 0 else W / 2 + gap / 2, -10, W / 2 - gap / 2, H + 20))
        c.translate(-W / 4 if i == 0 else W / 4, 0)
        n = c.getSaveCount()
        fn(t)
        c.restoreToCount(n)
        c.restore()
    if line:
        flatRect(W / 2 - gap / 2, -10, gap, H + 20, '#FFF8EE')
        inkLine([[W / 2 - gap / 2, -10], [W / 2 - gap / 2, H + 10]], .6, INK, 'inkfine', 0)
        inkLine([[W / 2 + gap / 2, -10], [W / 2 + gap / 2, H + 10]], .6, INK, 'inkfine', 0)


# ================================================================ small things
def crackedHeart(x, y, r, crack=1.0, grey=0.0, band=1.0, key='ch', a=1.0, beat=0.0):
    col = mixCol('#E0344E', '#8E8A98', grey)
    s = 1 + .06 * beat
    push()
    translate(x, y)
    scale(s)
    heartP(0, 0, r, col=col, key=key, a=a)
    if crack > .01:
        boilSeed(key + 'cr')
        pts = [[-r * .05, -r * .62], [r * .14, -r * .3], [-r * .1, -r * .05], [r * .12, r * .22], [0, r * .45]]
        n = max(2, int(len(pts) * crack + .5))
        inkLine(pts[:n], 1.2, INK, 'ink', 0)
    if band > .01:
        push()
        rotate(-.6)
        boilSeed(key + 'bd')
        paint(rrPts(-r * .5, -r * .15, r * 1.0, r * .3, r * .1), wash='#F2D2B0', washOp=int(255 * band * a), ink=INK, sw=.6, lite=True)
        for i in range(3):
            G.c.drawCircle(-r * .12 + i * r * .12, 0, r * .025, skia.Paint(AntiAlias=True, Color=skcol('#C9A27A', band * a)))
        pop()
    pop()


def balloon(x, y, r, col='#F7D36E', label='快乐', sx=None, sy=None, key='bal', a=1.0, rot=0.0):
    """a round balloon centred at (x, y); string down to (sx, sy) if given"""
    if sx is not None:
        boilSeed(key + 's')
        inkLine([[x, y + r * 1.15], [lerp(x, sx, .5) + 14, lerp(y + r, sy, .5)], [sx, sy]], .7, INK, 'inkfine', .6)
    push()
    translate(x, y)
    rotate(rot)
    boilSeed(key)
    paint(ellPts(0, 0, r * .92, r * 1.08, 24), wash=col, washOp=int(255 * a), fill=mixCol(col, INK, .2), fillOp=int(50 * a), ink=INK, sw=.9)
    paint([[-r * .12, r * 1.06], [r * .12, r * 1.06], [0, r * 1.2]], wash=mixCol(col, INK, .2), ink=INK, sw=.5)
    paint(ellPts(-r * .35, -r * .45, r * .16, r * .26, 10, 0, -.5), wash='#FFFFFF', washOp=int(170 * a), ink=None)
    if label:
        text(label, 0, r * .06, r * .5, '#8A5A1A', shadow=False, a=a)
    pop()


def suitcase(x, y, s=1.0, col='#7FB8E6', key='suit', handle=True, tilt=0.0):
    """rolling suitcase; (x, y) = wheels on the floor"""
    push()
    translate(x, y)
    rotate(tilt)
    boilSeed(key)
    if handle:
        inkLine([[-14 * s, -150 * s], [-14 * s, -210 * s], [14 * s, -210 * s], [14 * s, -150 * s]], 1.6, '#3A3550', 'ink', 0)
    paint(rrPts(-55 * s, -150 * s, 110 * s, 140 * s, 14 * s), wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=1.0)
    for dx in (-25, 0, 25):
        G.c.drawLine(dx * s, -140 * s, dx * s, -20 * s, skia.Paint(AntiAlias=True, Color=skcol(mixCol(col, INK, .35), .6), StrokeWidth=3 * s))
    heartP(-20 * s, -110 * s, 12 * s, col='#F7A9BC', key=key + 'stk')
    for dx in (-36, 36):
        paint(ellPts(dx * s, -4 * s, 9 * s, 9 * s, 10), wash='#3A3550', ink=None)
    pop()


def instantCamera(x, y, s=1.0, key='cam', flashK=0.0):
    boilSeed(key)
    paint(rrPts(x - 46 * s, y - 34 * s, 92 * s, 68 * s, 12 * s), wash='#F2E6D8', fill='#C9B8A4', fillOp=60, ink=INK, sw=.9)
    paint(ellPts(x, y + 2 * s, 20 * s, 20 * s, 18), wash='#3A3550', ink=INK, sw=.7)
    paint(ellPts(x, y + 2 * s, 10 * s, 10 * s, 14), wash='#7FA3D6', ink=None)
    paint(rectPts(x + 18 * s, y - 28 * s, 20 * s, 10 * s), wash='#FFFFFF', ink=INK, sw=.5)
    paint(rectPts(x - 40 * s, y - 30 * s, 22 * s, 8 * s), wash=['#E8476E', '#F2C53D', '#5FB8A8'][0], ink=None)
    if flashK > .01:
        glow(x + 28 * s, y - 23 * s, 160 * s, '#FFFFFF', flashK)


def phoneCard(x, y, h, mode, t, t0=0.0, name='她', key='pc', lit=1.0, case='#7FB8E6'):
    """a big phone screen card (graphic insert). mode: 'call' (呼叫 name…, ripples), 'incoming' (name 来电 + buttons),
    'ended' (通话已取消), 'missed' (未接来电 · name), 'dark'"""
    w = h * .52
    push()
    translate(x, y)
    boilSeed(key)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + 14, -h / 2 + 18, w, h), w * .14, w * .14, skia.Paint(AntiAlias=True, Color=skcol(INK, .3)))
    paint(rrPts(-w / 2, -h / 2, w, h, w * .14), wash=case, fill=mixCol(case, INK, .3), fillOp=60, ink=INK, sw=1.1)
    sx, sy, sw_, sh_ = -w / 2 + w * .07, -h / 2 + w * .1, w * .86, h - w * .2
    scrCol = '#1E2235' if mode == 'dark' else mixCol('#1E2235', '#F4F7FB', lit)
    paint(rrPts(sx, sy, sw_, sh_, w * .07), wash=scrCol, ink=None)
    if mode != 'dark':
        top = sy + sh_ * .26
        # avatar
        av = w * .2
        paint(ellPts(0, top, av, av, 24), wash='#FBD0DA' if name == '她' else '#F5B394', ink=INK, sw=.8)
        clawd(0, top + av * .85, av / 7.2, dict(col='#EE9AAE' if name == '她' else PAL['clay'], dk='#C0637B' if name == '她' else PAL['clayDk'],
                                               lt='#FBD0DA' if name == '她' else '#F5B394', hat='flower' if name == '她' else None, eyes='happy',
                                               mouth='smile', noLegs=True, noShadow=True, lite=True, boilKey=key + 'av', view='front'))
        if mode == 'call':
            for j in range(3):
                ph = frac((t - t0) * .9 - j / 3)
                G.c.drawCircle(0, top, av * (1 + ph * 1.2), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3,
                                                                      Color=skcol('#7FB8E6', .7 * (1 - ph))))
            wtext('呼叫 ' + name, 0, top + av * 1.9, w * .12, '#2B2233')
            dots = '·' * (1 + int((t - t0) * 2.5) % 3)
            wtext(dots, 0, top + av * 2.5, w * .1, '#6A6A80')
            hangBtn(0, sy + sh_ * .84, w * .11)
        elif mode == 'incoming':
            wtext(name + ' 来电', 0, top + av * 1.9, w * .12, '#2B2233')
            bob = math.sin((t - t0) * 14) * 4
            hangBtn(-w * .2, sy + sh_ * .84, w * .1)
            pickBtn(w * .2, sy + sh_ * .84 + bob, w * .1)
        elif mode == 'ended':
            wtext('通话已取消', 0, top + av * 1.9, w * .1, '#6A6A80')
        elif mode == 'missed':
            wtext('未接来电', 0, top + av * 1.9, w * .11, '#D8394E')
            wtext(name, 0, top + av * 2.6, w * .1, '#2B2233')
    pop()
    if lit > .05 and mode != 'dark':
        glow(x, y, h * .9, '#CFE8FF', .25 * lit)


def hangBtn(x, y, r):
    paint(ellPts(x, y, r, r, 20), wash='#E8476E', ink=INK, sw=.7)
    boilSeed('hb')
    inkLine([[x - r * .45, y + r * .1], [x, y - r * .12], [x + r * .45, y + r * .1]], 1.4, '#FFFFFF', 'ink', .5)


def pickBtn(x, y, r):
    paint(ellPts(x, y, r, r, 20), wash='#4CC38A', ink=INK, sw=.7)
    boilSeed('pb')
    inkLine([[x - r * .4, y - r * .3], [x - r * .1, y + r * .2], [x + r * .4, y + r * .35]], 1.4, '#FFFFFF', 'ink', .5)


def tearDrops(t, x, y, u, seed=1, n=2, rate=1.2, fall=None, a=1.0, size=1.0):
    """tears sliding from an eye at (x, y) (world), u-scaled"""
    fall = fall or 3.2 * u
    for i in range(n):
        ph = frac(t * rate + i / n + hash1(seed) * .3)
        py = y + ph * fall
        r = u * .22 * size * (1 - .3 * ph)
        boilSeed(f'td{seed}{i}')
        paint([[x, py - r * 1.8], [x + r, py], [x, py + r], [x - r, py]], wash='#BFE6FF', washOp=int(230 * a * (1 - ph * .4)), ink=INK if a > .5 else None,
              sw=.45, curv=1)
    # a wet glint line
    G.c.drawLine(x, y, x, y + fall * .7, skia.Paint(AntiAlias=True, Color=skcol('#DDF3FF', .45 * a), StrokeWidth=max(1.5, u * .12)))


def nightSkyHill(t, key='nsh', tree=True, moonK=1.0, starsK=1.0, nightK=1.0):
    from sets2 import nightHill
    nightHill(t, nightK=nightK, key=key, milky=1.0 * nightK, starsK=starsK, moonK=moonK, tree=tree, flowers=True)


def crate(x, y, s=1.0, key='crate'):
    """wooden crate; (x, y) = floor centre; returns top y"""
    boilSeed(key)
    w, h = 120 * s, 80 * s
    paint(rectPts(x - w / 2, y - h, w, h, 1.5), wash='#C98B5A', fill='#8A5A36', fillOp=60, ink=INK, sw=.9)
    for i in range(1, 3):
        G.c.drawLine(x - w / 2 + 6, y - h + i * h / 3, x + w / 2 - 6, y - h + i * h / 3,
                     skia.Paint(AntiAlias=True, Color=skcol('#7A4E2E', .7), StrokeWidth=3))
    inkLine([[x - w / 2 + 8, y - h + 6], [x + w / 2 - 8, y - 6]], .6, '#7A4E2E', 'inkfine', 0)
    return y - h


def flowerStar(x, y, r, k, key='fst'):
    """a star that blooms into her five-petal white flower (k 0..1)"""
    if k < .5:
        glow(x, y, r * 3, '#FFF6D8', .6)
        paint(starPts(x, y, r * (1 + .3 * math.sin(k * 20)), .4, 4), wash='#FFF6D8', ink=None)
        return
    kk = backOut(clamp((k - .5) / .5))
    glow(x, y, r * 4, '#FFFFFF', .5)
    boilSeed(key)
    for i in range(5):
        a = i / 5 * TAU - math.pi / 2
        paint(ellPts(x + math.cos(a) * r * .9 * kk, y + math.sin(a) * r * .9 * kk, r * .75 * kk, r * .55 * kk, 12, 0, a), wash='#FFFFFF', ink=INK, sw=.5)
    paint(ellPts(x, y, r * .45 * kk, r * .45 * kk, 12), wash='#F2C53D', ink=None)


def flyingNote(x, y, s, t, seed, col=NOTE_Y, key='fly', a=1.0):
    """a paper note fluttering through the air (flips while it flies)"""
    flip = math.sin(t * (4 + 2 * hash1(seed)) + seed)
    push()
    translate(x, y)
    rotate(math.sin(t * 2.3 + seed * 1.7) * .6)
    scale(1, .35 + .65 * abs(flip))
    boilSeed(f'{key}{seed}')
    paint(rectPts(-s / 2, -s / 2, s, s, 1), wash=col if flip > 0 else mixCol(col, '#FFFFFF', .35), washOp=int(255 * a),
          ink=INK if a > .5 else None, sw=.45, lite=True)
    if flip > 0 and s > 30:
        G.c.drawLine(-s * .3, -s * .05, s * .3, -s * .05, skia.Paint(AntiAlias=True, Color=skcol(INK, .5 * a), StrokeWidth=2))
        G.c.drawLine(-s * .3, s * .15, s * .15, s * .15, skia.Paint(AntiAlias=True, Color=skcol(INK, .5 * a), StrokeWidth=2))
    pop()


def featherFall(t, t0, x, y, n=10, spread=320, key='fth'):
    a = t - t0
    if a < 0:
        return
    for i in range(n):
        px = x + (hash1(i * 2.3 + 1) - .5) * spread + math.sin(a * 3 + i) * 30
        py = y - 140 * hash1(i * 1.9) + a * 70 + (1 - math.exp(-a * 4)) * -120 * hash1(i)
        push()
        translate(px, py)
        rotate(math.sin(a * 4 + i) * .8)
        boilSeed(f'{key}{i}')
        paint(ellPts(0, 0, 14, 5, 10), wash='#FFFFFF', ink=INK, sw=.4, lite=True)
        pop()


def floatHeartsUp(t, t0, x, y, n=6, spread=120, rise=220, life=1.6, s=16, seed=1):
    a = t - t0
    if a <= 0 or a > life:
        return
    for i in range(n):
        px = x + (hash1(seed + i * 3.1) - .5) * spread * 2 + math.sin(a * 5 + i) * 10
        py = y - rise * (a / life) * (.6 + .6 * hash1(seed + i * 1.7))
        heartP(px, py, s * (.6 + .5 * hash1(i + seed)), col='#E8476E' if i % 2 else '#F7A1B6', key=f'fh{seed}{i}', a=1 - a / life)
