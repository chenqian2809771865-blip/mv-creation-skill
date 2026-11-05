# props2.py: sets and props for 病变 (watercolour + ink). Bedroom, the bear, the letter, album, stage, storm, sky.
import math
from eng import *
from clawd import *
from props import *

P2 = dict(wallA='#F4E9D6', wallB='#EBDCC2', floor='#C99A6B', floorDk='#A87B52', wood='#B98352', woodDk='#8A5A36',
          blanket='#9CC3E6', blanketDk='#6F9CC8', pillowHe='#BFD8EE', pillowHer='#F6BCCB', sheet='#F7F1E6',
          bear='#E9B7A0', bearDk='#C98A72', bearLt='#F7D9C9', stain='#7D7596', stainDk='#5A5274',
          sepia='#E9C58F', sepiaDk='#B8895A', cold='#AFC0D6', red='#D8394E', tomato='#E4473C')


# ---------------- generic helpers ----------------
def xmark(x, y, s, age, col=None):
    """a red brushed X that slams in (age = seconds since the beat)"""
    if age < 0:
        return
    col = col or P2['red']
    k = backOut(clamp(age / .14))
    push()
    translate(x, y)
    scale(k)
    rotate(-.12 + math.sin(age * 20) * .05 * math.exp(-age * 6))
    boilSeed(f'xm{x:.0f}')
    inkLine([[-s, -s], [s, s]], s / 9, col, 'ink', 0)
    inkLine([[s, -s], [-s, s]], s / 9, col, 'ink', 0)
    pop()


def blot(cx, cy, r, key='blot', col=None, op=200, lobes=7, dk=None):
    """a 病变 stain: an irregular watercolour bloom with a darker rim"""
    if r < 2:
        return
    boilSeed(key)
    col = col or P2['stain']
    pts = []
    ph = [hash1(i * 3.7 + len(key)) * TAU for i in range(3)]
    for i in range(48):
        a = i / 48 * TAU
        rr = r * (1 + .16 * math.sin(a * lobes + ph[0]) + .09 * math.sin(a * (lobes + 4) + ph[1]) + .05 * math.sin(a * 17 + ph[2]))
        pts.append([cx + math.cos(a) * rr, cy + math.sin(a) * rr * .82])
    paint(pts, fill=col, fillOp=op, bleed=.18, tex=.6, border=.9, ink=None)
    paint([[cx + (p[0] - cx) * .55, cy + (p[1] - cy) * .55] for p in pts], fill=dk or P2['stainDk'], fillOp=op * .5, bleed=.25, border=.3, ink=None)
    # satellite drops
    for i in range(5):
        a = hash1(i * 7.1 + len(key)) * TAU
        d = r * (1.15 + .35 * hash1(i * 2.3))
        rs_ = r * (.06 + .06 * hash1(i * 5.5))
        paint(ellPts(cx + math.cos(a) * d, cy + math.sin(a) * d * .82, rs_, rs_, 12), fill=col, fillOp=op * .9, bleed=.2, ink=None)


def rainField(t, n=90, col='#DCE6FF', seed=1, x0=-60, x1=W + 60, y0=-80, y1=H, sp=1500, ln=40, sw=.8, slant=10):
    tt = onTwos(t)
    for i in range(n):
        x = lerp(x0, x1, hash1(i * 3.3 + seed))
        y = (hash1(i * 7.1 + seed) * (y1 - y0 + 200) + tt * sp) % (y1 - y0 + 200) + y0 - 100
        boilSeed(f'rn{seed}{i}')
        inkLine([[x, y], [x - slant, y + ln]], sw, col, 'inkfine', 0)


def vignette(a=.35, col=INK):
    """soft dark corners (painted, not a gradient filter)"""
    for i in range(5):
        k = i / 4
        r = lerp(1250, 900, k)
        p = skia.Path()
        p.setFillType(skia.PathFillType.kEvenOdd)
        p.addRect(skia.Rect.MakeXYWH(-200, -200, W + 400, H + 400))
        p.addOval(skia.Rect.MakeXYWH(W / 2 - r * 1.05, H / 2 - r * .66, r * 2.1, r * 1.32))
        G.c.drawPath(p, skia.Paint(AntiAlias=True, Color=skcol(col, a * .2)))


def wallpaper(c1, c2, dots=True, key='wp'):
    flatRect(-80, -80, W + 160, H + 160, c1)
    if dots:
        for r in range(14):
            for c_ in range(22):
                x = c_ * 92 + (46 if r % 2 else 0) - 40
                y = r * 84 - 30
                boilSeed(f'{key}{r}{c_}')
                paint(ellPts(x, y, 9, 9, 8), wash=c2, ink=None)


def woodFloor(y, col=None, dk=None, key='fl'):
    col = col or P2['floor']
    dk = dk or P2['floorDk']
    flatRect(-80, y, W + 160, H - y + 120, col)
    boilSeed(key)
    for i in range(7):
        yy = y + 22 + i * (i + 3) * 6
        inkLine([[-80, yy], [W + 80, yy + jit(3)]], .55, dk, 'inkfine', 0)
    inkLine([[-80, y], [W + 80, y]], 1.2, INK, 'ink', 0)


# ---------------- the alarm clock ----------------
def alarmClock(x, y, s, ring=0.0, key='clk', squash=0.0, hourA=7, minA=0):
    """twin-bell alarm clock; (x, y) = face centre; s = face radius. ring 0..1 shakes the bells."""
    boilSeed(key)
    sh = ring * math.sin(G.T * 70) * .07
    push()
    translate(x, y + s * 1.0)
    scale(1 + squash * .5, 1 - squash)
    rotate(sh)
    translate(0, -s * 1.0)
    # legs
    for sx in (-1, 1):
        paint([[sx * s * .55, s * .78], [sx * s * .8, s * 1.12], [sx * s * .62, s * 1.15], [sx * s * .4, s * .85]], wash='#C9A24A', ink=INK, sw=1.0)
    # bells + hammer
    for sx in (-1, 1):
        bx, by = sx * s * .62, -s * .92
        a = sx * (.5 + .12 * ring * math.sin(G.T * 90 + sx))
        push()
        translate(bx, by)
        rotate(a)
        d = []
        for i in range(15):
            ang = math.pi + i / 14 * math.pi
            d.append([math.cos(ang) * s * .42, math.sin(ang) * s * .32])
        paint(d, wash='#F2C53D', fill='#C9962A', fillOp=70, ink=INK, sw=1.1)
        paint(ellPts(0, -s * .34, s * .07, s * .07, 8), wash='#C9962A', ink=INK, sw=.6)
        pop()
    inkLine([[0, -s * 1.02], [0, -s * 1.3]], 1.2, INK, 'ink', 0)
    paint(ellPts(0, -s * 1.32, s * .1, s * .08, 10), wash='#C9962A', ink=INK, sw=.7)
    # body
    paint(ellPts(0, 0, s * 1.08, s * 1.08, 40), wash='#F28FB0', fill='#D8648A', fillOp=60, ink=INK, sw=1.4)
    paint(ellPts(0, 0, s * .88, s * .88, 40), wash='#FFFBF2', ink=INK, sw=1.0)
    for i in range(12):
        a = i / 12 * TAU
        r0, r1 = (.68, .8) if i % 3 else (.62, .8)
        inkLine([[math.cos(a) * s * r0, math.sin(a) * s * r0], [math.cos(a) * s * r1, math.sin(a) * s * r1]], 1.4 if i % 3 == 0 else .8, INK, 'inkfine', 0)
    ha = (hourA % 12 + minA / 60) / 12 * TAU - math.pi / 2
    ma = minA / 60 * TAU - math.pi / 2
    inkLine([[0, 0], [math.cos(ha) * s * .42, math.sin(ha) * s * .42]], 2.4, INK, 'ink', 0)
    inkLine([[0, 0], [math.cos(ma) * s * .64, math.sin(ma) * s * .64]], 1.7, INK, 'ink', 0)
    sa = G.T * 6
    inkLine([[0, 0], [math.cos(sa) * s * .7, math.sin(sa) * s * .7]], .7, P2['red'], 'inkfine', 0)
    paint(ellPts(0, 0, s * .06, s * .06, 8), wash=P2['red'], ink=None)
    pop()
    if ring > .05:
        for sx in (-1, 1):
            for j in range(3):
                r = s * (.55 + j * .22)
                cx, cy = x + sx * s * .62, y - s * .95
                arc = [[cx + sx * math.cos(a) * r, cy + math.sin(a) * r] for a in [-1.0 + i * .2 for i in range(9)]]
                inkLine(arc, 1.1 * ring, INK, 'ink', .5)


def photoFrame(x, y, s, fall=0.0, key='pf'):
    """a little standing photo frame of the couple; (x, y) = bottom centre; fall 0..1 tips it face down backwards"""
    boilSeed(key)
    push()
    translate(x, y)
    rotate(-fall * math.pi / 2 * .98)
    w, h = 3.2 * s, 4.0 * s
    paint(rectPts(-w / 2, -h, w, h, s * .03), wash='#B98352', fill='#8A5A36', fillOp=60, ink=INK, sw=1.0)
    paint(rectPts(-w / 2 + .3 * s, -h + .3 * s, w - .6 * s, h - .6 * s), wash='#FBE7C4', ink=INK, sw=.6)
    # the two of them, tiny
    G.CLAWD_N += 10
    him(-.55 * s, -.55 * s, .19 * s, dict(view='front', eyes='happy', mouth='smile', blush=.6, noShadow=True, lite=True, aL=.6, aR=.1, boilKey='pfhim'))
    her(.55 * s, -.55 * s, .19 * s, dict(view='front', eyes='happy', mouth='smile', blush=.6, noShadow=True, lite=True, aL=.1, aR=.6, boilKey='pfher'))
    paint(heartPts(0, -h * .72, .32 * s, 16), wash=C['heart'], ink=None)
    pop()


# ---------------- bed ----------------
def bedBack(x, y, w, s, key='bed', night=0.0, skip=()):
    """headboard + mattress + pillows. (x, y) = centre-bottom of the mattress front; w = width.
    returns pillow centres (left, right)."""
    boilSeed(key)
    wd = mixCol(P2['wood'], '#3A3A5A', night * .5)
    hb = [[x - w / 2 - 20, y - 6.2 * s], [x - w / 2 - 20, y - 11.5 * s], [x - w / 2 + 40, y - 12.6 * s], [x + w / 2 - 40, y - 12.6 * s],
          [x + w / 2 + 20, y - 11.5 * s], [x + w / 2 + 20, y - 6.2 * s]]
    paint(hb, wash=wd, fill=P2['woodDk'], fillOp=70, ink=INK, sw=1.3)
    paint(rectPts(x - w / 2 + 60, y - 11.4 * s, w - 120, 4.2 * s, 2), wash=mixCol(wd, '#FFFFFF', .2), ink=INK, sw=.8)
    # mattress
    paint(rectPts(x - w / 2, y - 4.2 * s, w, 4.2 * s, 2), wash=mixCol(P2['sheet'], '#3A3A5A', night * .45), ink=INK, sw=1.2)
    # pillows
    pl = (x - w * .24, y - 6.0 * s)
    pr = (x + w * .24, y - 6.0 * s)
    for side, (px, py), col in (('he', pl, P2['pillowHe']), ('her', pr, P2['pillowHer'])):
        if side in skip:
            continue
        paint(rrPts(px - w * .165, py - 2.3 * s, w * .33, 4.4 * s, 1.8 * s, 1.5), wash=mixCol(col, '#3A3A5A', night * .45),
              fill=mixCol(col, INK, .2), fillOp=50, ink=INK, sw=1.1)
    return pl, pr


def blanket(x, y, w, s, key='blk', night=0.0, lump=0.0, top=None):
    """blanket covering the front of the mattress; top = y of the blanket's upper edge"""
    boilSeed(key)
    col = mixCol(P2['blanket'], '#2F3C6A', night * .45)
    top = top if top is not None else y - 4.6 * s
    pts = [[x - w / 2 - 15, y + .4 * s]]
    for i in range(13):
        k = i / 12
        bump_ = lump * math.exp(-((k - .26) / .12) ** 2) * 2.2 * s
        pts.append([x - w / 2 - 15 + (w + 30) * k, top + math.sin(k * 9) * 6 - bump_])
    pts.append([x + w / 2 + 15, y + .4 * s])
    paint(pts, wash=col, fill=mixCol(col, INK, .3), fillOp=50, ink=INK, sw=1.3)
    # checks
    for i in range(1, 8):
        xx = x - w / 2 + w * i / 8
        inkLine([[xx, top + 16], [xx + jit(4), y]], .6, mixCol(col, INK, .35), 'inkfine', .2)
    inkLine([[x - w / 2, top + 40], [x + w / 2, top + 40]], .9, '#FFFFFF', 'inkfine', .2)


# ---------------- the bear ----------------
def bear(x, y, s, o=None):
    """her favourite toy: a plush bear with her white flower on one ear. (x, y) = bottom centre (sitting)."""
    o = o or {}
    boilSeed(o.get('key', 'bear'))
    col = o.get('col', P2['bear'])
    dk, lt = P2['bearDk'], P2['bearLt']
    if o.get('grey'):
        col, dk, lt = mixCol(col, '#9A98A8', .7), mixCol(dk, '#77758A', .7), mixCol(lt, '#C9C7D4', .7)
    push()
    translate(x, y)
    rotate(o.get('rot', 0))
    sq = o.get('sq', 0)
    scale(1 + sq * .5, 1 - sq)
    # legs
    for sx in (-1, 1):
        paint(ellPts(sx * 1.55 * s, -.7 * s, 1.05 * s, .8 * s, 18), wash=col, ink=INK, sw=1.0)
        paint(ellPts(sx * 1.6 * s, -.65 * s, .55 * s, .45 * s, 14), wash=lt, ink=None)
    # body
    paint(ellPts(0, -2.4 * s, 2.1 * s, 2.0 * s, 28), wash=col, fill=dk, fillOp=50, ink=INK, sw=1.1)
    paint(ellPts(0, -2.2 * s, 1.2 * s, 1.15 * s, 22), wash=lt, ink=None)
    paint(heartPts(0, -2.3 * s, .55 * s, 16), wash=C['heart'], ink=INK, sw=.5)
    # arms
    for sx in (-1, 1):
        a = o.get('aL' if sx < 0 else 'aR', 0)
        push()
        translate(sx * 1.6 * s, -3.4 * s)
        rotate(sx * (.5 - a))
        paint(ellPts(sx * .3 * s, .9 * s, .62 * s, 1.1 * s, 16), wash=col, ink=INK, sw=.9)
        pop()
    # head
    push()
    translate(0, -4.6 * s)
    rotate(o.get('tilt', 0))
    for sx in (-1, 1):
        paint(ellPts(sx * 1.45 * s, -1.45 * s, .72 * s, .72 * s, 16), wash=col, ink=INK, sw=1.0)
        paint(ellPts(sx * 1.45 * s, -1.45 * s, .38 * s, .38 * s, 12), wash=lt, ink=None)
    paint(ellPts(0, 0, 2.0 * s, 1.75 * s, 30), wash=col, fill=dk, fillOp=40, ink=INK, sw=1.1)
    paint(ellPts(0, .5 * s, .85 * s, .62 * s, 18), wash=lt, ink=INK, sw=.6)
    paint(ellPts(0, .25 * s, .28 * s, .2 * s, 10), wash=INK, ink=None)
    inkLine([[0, .45 * s], [0, .75 * s]], .7, INK, 'inkfine', 0)
    inkLine([[-.35 * s, .9 * s], [0, .75 * s], [.35 * s, .9 * s]], .7, INK, 'inkfine', .5)
    ey = o.get('eyes', 'button')
    for sx in (-1, 1):
        if ey == 'closed':
            inkLine([[sx * .75 * s - .25 * s, -.3 * s], [sx * .75 * s, -.18 * s], [sx * .75 * s + .25 * s, -.3 * s]], .9, INK, 'ink', .5)
        else:
            paint(ellPts(sx * .75 * s, -.3 * s, .22 * s, .22 * s, 10), wash=INK, ink=None)
            paint(ellPts(sx * .75 * s - .07 * s, -.37 * s, .07 * s, .07 * s, 6), wash='#FFFFFF', ink=None)
    if o.get('blush', 0):
        for sx in (-1, 1):
            paint(ellPts(sx * 1.2 * s, .35 * s, .35 * s, .2 * s, 10), fill=PAL['rose'], fillOp=150 * o['blush'], ink=None)
    if o.get('flower', True):
        flowerAt(1.2 * s, -1.6 * s, s * .9, 1.0, .85)
    pop()
    pop()


# ---------------- furniture ----------------
def wardrobe(x, y, s, opn=0.0, key='wd', hatIn=True):
    """(x, y) = bottom centre; about 6s wide, 11s tall; opn 0..1 swings both doors"""
    boilSeed(key)
    w, h = 6 * s, 11 * s
    paint(rectPts(x - w / 2, y - h, w, h, 2), wash=P2['wood'], fill=P2['woodDk'], fillOp=60, ink=INK, sw=1.3)
    paint(rectPts(x - w / 2 + .3 * s, y - h + .3 * s, w - .6 * s, h - 1.2 * s), wash='#3E3046', ink=INK, sw=.8)
    if opn > .02:
        # rail, hangers, her hat
        inkLine([[x - w / 2 + .5 * s, y - h + 1.6 * s], [x + w / 2 - .5 * s, y - h + 1.6 * s]], 1.6, '#C9C2B4', 'ink', 0)
        for i in range(4):
            hx = x - 1.8 * s + i * 1.2 * s
            sw_ = math.sin(G.T * 8 + i) * .1 * math.exp(-max(0, opn - .9))
            push()
            translate(hx, y - h + 1.6 * s)
            rotate(sw_)
            inkLine([[0, 0], [0, .4 * s], [-.7 * s, 1.0 * s], [.7 * s, 1.0 * s], [0, .4 * s]], .9, '#D8D2C6', 'inkfine', 0)
            pop()
        if hatIn:
            push()
            translate(x + 1.5 * s, y - 2.6 * s)
            hat(s * .75, 'deer', 1.0)
            pop()
    for sx in (-1, 1):
        dw = w / 2 * (1 - opn * .82)
        x0 = x + sx * w / 2
        x1 = x0 - sx * dw if opn < .02 else x0 + sx * w / 2 * opn * .55
        # open doors: drawn as thin panels outside the cabinet
        if opn < .02:
            pts = [[x, y - h + .2 * s], [x0 - sx * .2 * s, y - h + .2 * s], [x0 - sx * .2 * s, y - .9 * s], [x, y - .9 * s]]
        else:
            pts = [[x0, y - h + .2 * s], [x1, y - h - .2 * s * opn], [x1, y - .6 * s], [x0, y - .9 * s]]
        paint(pts, wash=mixCol(P2['wood'], '#FFFFFF', .12), fill=P2['woodDk'], fillOp=50, ink=INK, sw=1.1)
        kx = (x - sx * .5 * s) if opn < .02 else (x1 - sx * .5 * s)
        paint(ellPts(kx, y - h / 2, .22 * s, .22 * s, 8), wash='#F2C53D', ink=INK, sw=.6)
    paint(rectPts(x - w / 2 - .2 * s, y - h - .5 * s, w + .4 * s, .6 * s), wash=P2['woodDk'], ink=INK, sw=1)


def windowCurtain(x, y, w, h, opn=0.0, key='win', sky=('#CFE3F2', '#EEF5FA'), cur='#F2B5C5', night=0.0):
    """window with two curtains; (x, y) = top-left; opn 0 = closed, 1 = fully open"""
    boilSeed(key)
    gradRect(x, y, w, h, [mixCol(sky[0], '#1F2550', night), mixCol(sky[1], '#3B3770', night)])
    paint(rectPts(x, y, w, h, 2), ink=INK, sw=1.4)
    inkLine([[x + w / 2, y], [x + w / 2, y + h]], 1.6, '#FFFFFF', 'ink', 0)
    inkLine([[x, y + h / 2], [x + w, y + h / 2]], 1.6, '#FFFFFF', 'ink', 0)
    paint(rectPts(x - 20, y + h, w + 40, 26), wash='#FFFFFF', ink=INK, sw=1)
    inkLine([[x - 40, y - 24], [x + w + 40, y - 24]], 2.2, P2['woodDk'], 'ink', 0)
    col = mixCol(cur, '#2F3C6A', night * .5)
    for sx in (-1, 1):
        cw = w / 2 * lerp(1.02, .22, opn)
        x0 = x if sx < 0 else x + w
        x1 = x0 - sx * cw
        pts = [[x0 + sx * 30, y - 24], [x1, y - 24]]
        for i in range(8):
            yy = y - 24 + i * (h + 60) / 7
            pts.append([x1 - sx * (math.sin(i * 1.4) * 10 + (1 - opn) * 0), yy])
        pts.append([x0 + sx * 30, y + h + 36])
        paint(pts, wash=col, fill=mixCol(col, INK, .3), fillOp=60, ink=INK, sw=1.1)
        for k in range(1, 4):
            xx = lerp(x0, x1, k / 4)
            inkLine([[xx, y - 20], [xx, y + h + 30]], .6, mixCol(col, INK, .4), 'inkfine', .2)


def sofa(x, y, s, key='sofa', col='#8FB9A8', cushion=0.0):
    """(x, y) = bottom centre; ~14s wide. cushion 0..1 = the left cushion flying up"""
    boilSeed(key)
    dk = mixCol(col, INK, .3)
    w = 14 * s
    paint(rrPts(x - w / 2, y - 6.4 * s, w, 3.6 * s, 1.2 * s), wash=col, fill=dk, fillOp=50, ink=INK, sw=1.2)
    paint(rrPts(x - w / 2 - .4 * s, y - 3.6 * s, w + .8 * s, 2.6 * s, .8 * s), wash=col, fill=dk, fillOp=60, ink=INK, sw=1.2)
    for sx in (-1, 1):
        paint(rrPts(x + sx * (w / 2 + .2 * s) - 1.1 * s, y - 4.6 * s, 2.2 * s, 3.8 * s, .9 * s), wash=mixCol(col, '#FFFFFF', .1), fill=dk, fillOp=60, ink=INK, sw=1.1)
    for sx in (-1, 0, 1):
        paint(rectPts(x + sx * 4.6 * s - .3 * s, y - 1.0 * s, .6 * s, 1.0 * s), wash=P2['woodDk'], ink=INK, sw=.7)
    for i, cx in enumerate((x - 3.2 * s, x + 3.2 * s)):
        dy = 0
        rot = 0
        if i == 0 and cushion > 0:
            dy = -math.sin(cushion * math.pi) * 6 * s
            rot = cushion * 2.4
        push()
        translate(cx, y - 4.0 * s + dy)
        rotate(rot)
        paint(rrPts(-2.9 * s, -1.0 * s, 5.8 * s, 2.0 * s, .8 * s), wash=mixCol(col, '#FFFFFF', .25), ink=INK, sw=1.0)
        pop()


def fridge(x, y, s, opn=0.0, key='frg'):
    """(x, y) = bottom centre; ~5s wide, 12s tall"""
    boilSeed(key)
    w, h = 5 * s, 12 * s
    paint(rrPts(x - w / 2, y - h, w, h, .6 * s), wash='#E8EEF2', fill='#AFC0D6', fillOp=50, ink=INK, sw=1.3)
    if opn > .02:
        paint(rectPts(x - w / 2 + .3 * s, y - h + .3 * s, w - .6 * s, h - .6 * s), wash='#FFFDE8', ink=INK, sw=.8)
        glow(x, y - h * .55, 5 * s * opn, '#FFF6C8', .9 * opn)
        for k in range(3):
            inkLine([[x - w / 2 + .4 * s, y - h + (2.6 + k * 3) * s], [x + w / 2 - .4 * s, y - h + (2.6 + k * 3) * s]], 1.0, '#C9D3DE', 'ink', 0)
        # one carton of milk, alone
        paint(rectPts(x - .6 * s, y - h + 4.5 * s, 1.2 * s, 2.4 * s), wash='#FFFFFF', ink=INK, sw=.7)
        paint([[x - .6 * s, y - h + 4.5 * s], [x, y - h + 3.8 * s], [x + .6 * s, y - h + 4.5 * s]], wash='#9CC3E6', ink=INK, sw=.7)
        dx = w * .95 * opn
        paint([[x + w / 2, y - h], [x + w / 2 + dx, y - h - .5 * s], [x + w / 2 + dx, y + .2 * s], [x + w / 2, y]], wash='#DCE6EE', ink=INK, sw=1.1)
    else:
        inkLine([[x - w / 2, y - h * .68], [x + w / 2, y - h * .68]], 1.0, INK, 'ink', 0)
        for yy in (y - h * .8, y - h * .45):
            paint(rectPts(x + w / 2 - .9 * s, yy, .35 * s, 1.6 * s), wash='#9AA6B4', ink=INK, sw=.6)
        paint(heartPts(x - .8 * s, y - h * .85, .45 * s, 14), wash=C['heart'], ink=INK, sw=.5)


def door(x, y, s, opn=0.0, key='door', col='#C98B5A'):
    """(x, y) = bottom centre; opn swings it toward the viewer (drawn as narrowing)"""
    boilSeed(key)
    w, h = 5.4 * s, 12 * s
    paint(rectPts(x - w / 2 - .4 * s, y - h - .4 * s, w + .8 * s, h + .4 * s), wash='#5A4A5E', ink=INK, sw=1.2)
    paint(rectPts(x - w / 2, y - h, w, h), wash='#3A3046', ink=None)
    dw = w * (1 - opn * .8)
    pts = [[x - w / 2, y - h], [x - w / 2 + dw, y - h - opn * .6 * s], [x - w / 2 + dw, y + opn * .4 * s], [x - w / 2, y]]
    paint(pts, wash=col, fill=mixCol(col, INK, .3), fillOp=50, ink=INK, sw=1.2)
    if opn < .5:
        paint(ellPts(x - w / 2 + dw - .7 * s, y - h * .48, .3 * s, .3 * s, 8), wash='#F2C53D', ink=INK, sw=.6)


def table(x, y, w, s, key='tbl', col=None):
    """(x, y) = top-front edge centre of the tabletop"""
    boilSeed(key)
    col = col or P2['wood']
    paint([[x - w / 2, y], [x + w / 2, y], [x + w / 2 - 1.2 * s, y - 1.6 * s], [x - w / 2 + 1.2 * s, y - 1.6 * s]], wash=mixCol(col, '#FFFFFF', .15), ink=INK, sw=1.1)
    paint(rectPts(x - w / 2, y, w, .7 * s), wash=P2['woodDk'], ink=INK, sw=1.0)
    for sx in (-1, 1):
        paint(rectPts(x + sx * (w / 2 - 1.0 * s) - .3 * s, y + .7 * s, .6 * s, 4.0 * s), wash=P2['woodDk'], ink=INK, sw=.9)


# ---------------- letter, envelope ----------------
def envelope(x, y, w, opn=0.0, seal=1.0, key='env', col='#F7C6D2'):
    """(x, y) = centre; h = .62 w. opn lifts the flap; seal = flower seal still on (0..1 scale)"""
    boilSeed(key)
    h = w * .62
    dk = mixCol(col, INK, .25)
    paint(rectPts(x - w / 2, y - h / 2, w, h, 2), wash=col, fill=dk, fillOp=40, ink=INK, sw=1.3)
    if opn > .02:
        # paper peeking out
        paint(rectPts(x - w * .42, y - h / 2 - h * .45 * opn, w * .84, h * .6), wash='#FFFBF0', ink=INK, sw=.9)
        for k in range(3):
            inkLine([[x - w * .34, y - h / 2 - h * .45 * opn + h * (.1 + k * .12)], [x + w * .3, y - h / 2 - h * .45 * opn + h * (.1 + k * .12)]], .6, '#C9BBAA', 'inkfine', .2)
    paint([[x - w / 2, y + h / 2], [x, y + h * .02], [x + w / 2, y + h / 2]], wash=mixCol(col, '#FFFFFF', .12), ink=INK, sw=1.0)
    paint([[x - w / 2, y - h / 2], [x, y + h * .02], [x - w / 2, y + h / 2]], wash=mixCol(col, INK, .06), ink=INK, sw=.8)
    paint([[x + w / 2, y - h / 2], [x, y + h * .02], [x + w / 2, y + h / 2]], wash=mixCol(col, INK, .06), ink=INK, sw=.8)
    fy = lerp(y + h * .06, y - h / 2 - h * .5, opn)
    paint([[x - w / 2, y - h / 2], [x, fy], [x + w / 2, y - h / 2]], wash=mixCol(col, '#FFFFFF', .2), ink=INK, sw=1.1)
    if seal > .02:
        push()
        translate(x, y + h * .04)
        scale(seal)
        paint(ellPts(0, 0, w * .075, w * .075, 18), wash=P2['red'], fill='#9E2436', fillOp=60, ink=INK, sw=.8)
        flowerAt(0, 0, w * .03, 1.0, .9)
        pop()


def letterSheet(x, y, w, h, lines, shown, key='ls', rot=-.03, ink_=None):
    """paper with handwritten lines; shown = list of (age, alpha) per line, None = not yet"""
    boilSeed(key)
    push()
    translate(x, y)
    rotate(rot)
    paint(rectPts(-w / 2, -h / 2, w, h, 2), wash='#FFFBF0', fill='#EADFCB', fillOp=40, ink=INK, sw=1.2)
    for k in range(7):
        yy = -h / 2 + h * (.16 + k * .12)
        inkLine([[-w * .42, yy + 22], [w * .42, yy + 22]], .45, '#E2B9C2', 'inkfine', 0)
    for i, (txt, size, dy, col) in enumerate(lines):
        if i >= len(shown) or shown[i] is None:
            continue
        age = shown[i]
        a = clamp(age / .12)
        text(txt, -w * .38, -h / 2 + h * dy, size, col, align='left', shadow=False, a=a, sc=1 + .15 * math.exp(-age * 12))
    pop()


# ---------------- album, polaroids ----------------
def polaroid(x, y, w, rot, scene, drain=0.0, key='pol', drop=1.0):
    """scene(cx, cy, s, drain) draws the picture; drop = 0..1 landing progress (scale/fall)"""
    if drop <= .001:
        return
    boilSeed(key)
    h = w * 1.18
    push()
    translate(x, y - (1 - drop) * 260)
    rotate(rot + (1 - drop) * .5)
    sc_ = lerp(1.25, 1.0, drop)
    scale(sc_)
    paint(rectPts(-w / 2 + 8, -h / 2 + 12, w, h, 1), wash=INK, washOp=60, ink=None)
    paint(rectPts(-w / 2, -h / 2, w, h, 1.5), wash='#FFFDF7', ink=INK, sw=1.1)
    pw = w * .86
    px, py = -pw / 2, -h / 2 + w * .07
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(px, py, pw, pw))
    scene(0, py + pw / 2, pw / 2, drain)
    G.c.restore()
    paint(rectPts(px, py, pw, pw), ink=INK, sw=.7)
    pop()


# ---------------- stage bits ----------------
def tomato(x, y, s, key='tom', rot=0):
    boilSeed(key)
    push()
    translate(x, y)
    rotate(rot)
    paint(ellPts(0, 0, s, s * .86, 18), wash=P2['tomato'], fill='#A8241E', fillOp=60, ink=INK, sw=1)
    paint(starPts(0, -s * .8, s * .5, .35, 5), wash='#5E9E3A', ink=INK, sw=.5)
    paint(ellPts(-s * .35, -s * .3, s * .2, s * .12, 8), wash='#FFFFFF', washOp=170, ink=None)
    pop()


def splat(x, y, s, age, key='spl', col=None):
    if age < 0:
        return
    col = col or P2['tomato']
    k = backOut(clamp(age / .1))
    boilSeed(key)
    pts = []
    for i in range(24):
        a = i / 24 * TAU
        r = s * k * (1 + .45 * (hash1(i * 3.1 + len(key)) - .3) * (1 if i % 2 else .3))
        pts.append([x + math.cos(a) * r, y + math.sin(a) * r * .8])
    paint(pts, wash=col, fill='#A8241E', fillOp=50, ink=INK, sw=.9)
    for i in range(6):
        a = hash1(i * 5.3 + len(key)) * TAU
        d = s * (1.3 + .6 * hash1(i)) * k
        paint(ellPts(x + math.cos(a) * d, y + math.sin(a) * d * .8, s * .14, s * .14, 8), wash=col, ink=None)
    # drip
    dr = max(0, age - .1) * s * 1.2
    if dr > 2:
        paint(ribbon([[x - s * .2, y + s * .4], [x - s * .22, y + s * .4 + min(dr, s * 1.5)]], s * .22, s * .12), wash=col, ink=None)


def starBadge(x, y, s, txt='主演', k=1.0, key='sb'):
    p = backOut(k)
    if p < .02:
        return
    boilSeed(key)
    push()
    translate(x, y)
    scale(p)
    rotate(-.12)
    paint(starPts(0, 0, s, .55, 5), wash='#F2C53D', fill='#C9962A', fillOp=60, ink=INK, sw=1.2)
    text(txt, 0, s * .1, s * .5, INK, shadow=False)
    for sx in (-1, 1):
        paint([[sx * s * .25, s * .7], [sx * s * .6, s * 1.6], [sx * s * .35, s * 1.45], [sx * s * .05, s * 1.65]], wash=P2['red'], ink=INK, sw=.8)
    pop()


# ---------------- storm & sky ----------------
def bigQ(x, y, s, k=1.0, age=1.0, key='bq', col=None):
    """a giant question mark that falls and lands (k 0..1 fall progress)"""
    if k <= 0:
        return
    col = col or P2['stain']
    boilSeed(key)
    yy = lerp(y - 1200, y, easeIn(k))
    sq = .25 * math.exp(-age * 8) * math.cos(age * 30) if k >= 1 else 0
    push()
    translate(x, yy)
    scale(1 + sq * .4, 1 - sq)
    Q = [[-1, -2.6], [-.55, -3.45], [.35, -3.6], [1, -2.9], [.7, -2.05], [.05, -1.6], [0, -.9]]
    paint(ribbon([[a * s, b * s] for a, b in Q], .8 * s, .6 * s), wash=col, fill=P2['stainDk'], fillOp=60, ink=INK, sw=1.6)
    paint(ellPts(0, -.3 * s, .42 * s, .36 * s, 14), wash=col, ink=INK, sw=1.4)
    pop()
    if k >= 1 and age < .35:
        impactLines(x, y - .3 * s, s * .8, s * (1.2 + age * 2), 10, G.T, '#E8E6FF', key=key + 'i', sw=1.4)
        for i in range(5):
            a = math.pi + (i + .5) / 5 * math.pi
            d = s * (.4 + age * 3)
            paint(ellPts(x + math.cos(a) * d * 1.6, y + math.sin(a) * d * .5, s * .12, s * .12, 8), wash='#C9CFF0', ink=None)


def bolt(x0, y0, x1, y1, key='bolt', w=1.0):
    boilSeed(key)
    pts = [[x0, y0]]
    n = 7
    for i in range(1, n):
        k = i / n
        pts.append([lerp(x0, x1, k) + jit(70), lerp(y0, y1, k)])
    pts.append([x1, y1])
    glow(x1, y1, 300, '#E6EEFF', .8 * w)
    inkLine(pts, 7 * w, '#FFF8C8', 'ink', 0)
    inkLine(pts, 2.4 * w, '#FFFFFF', 'ink', 0)


def skyFace(x, y, s, t, mask=1.0, turn=0.0, key='sky'):
    """老天: a huge sleeping cloud with a sleep mask. (x, y) = centre; ~9s wide"""
    boilSeed(key)
    c = []
    for i in range(60):
        a = i / 60 * TAU
        up = math.sin(a) < 0
        r = 1 + .22 * abs(math.sin(a * 4)) ** .6 if up else 1 + .05 * abs(math.sin(a * 6))
        c.append([x + math.cos(a) * 4.6 * s * r, y + math.sin(a) * (2.3 if up else 1.5) * s * r])
    breathe = 1 + .02 * math.sin(t * 3)
    push()
    translate(x, y)
    scale(breathe)
    translate(-x, -y)
    paint(c, wash='#D9DCF0', fill='#9EA3C8', fillOp=70, ink=INK, sw=1.8, curv=.4)
    fx = x + turn * 2.4 * s
    if turn < .9:
        # sleep mask over the eyes
        if mask > .02:
            paint(rrPts(fx - 2.9 * s, y - 1.0 * s, 5.8 * s, 1.3 * s, .6 * s), wash='#5B4F9A', fill='#3B3770', fillOp=60, ink=INK, sw=1.3)
            inkLine([[fx - 2.9 * s, y - .5 * s], [x - 4.4 * s, y - .8 * s]], 1.2, '#3B3770', 'ink', .3)
            inkLine([[fx + 2.9 * s, y - .5 * s], [x + 4.4 * s, y - .8 * s]], 1.2, '#3B3770', 'ink', .3)
            for sx in (-1, 1):
                inkLine([[fx + sx * 1.4 * s - .5 * s, y - .35 * s], [fx + sx * 1.4 * s, y - .15 * s], [fx + sx * 1.4 * s + .5 * s, y - .35 * s]], 1.2, '#FFF5E2', 'ink', .5)
        # snoring mouth
        mo = .25 + .15 * (1 + math.sin(t * 3)) / 2
        paint(ellPts(fx, y + .9 * s, .55 * s, mo * s, 16), wash='#4A1F2A', ink=INK, sw=1.0)
        for sx in (-1, 1):
            paint(ellPts(fx + sx * 2.3 * s, y + .4 * s, .5 * s, .25 * s, 12), fill=PAL['rose'], fillOp=110, ink=None)
    pop()


def moon(x, y, r, key='moon'):
    boilSeed(key)
    glow(x, y, r * 4, '#FFF0C0', .55)
    paint(ellPts(x, y, r, r, 30), wash='#FFF3C8', ink=INK, sw=1.0)
    paint(ellPts(x + r * .45, y - r * .2, r * .85, r * .85, 30), wash='#232864', ink=None)


def starsField(t, n=40, seed=3, y1=600):
    for i in range(n):
        x = hash1(i * 4.1 + seed) * W
        y = hash1(i * 9.3 + seed) * y1
        tw = .6 + .4 * math.sin(t * (2 + hash1(i)) * 3 + i)
        sparkle(x, y, (5 + 7 * hash1(i * 2.2)) * tw, '#FFF5E2', .9)
