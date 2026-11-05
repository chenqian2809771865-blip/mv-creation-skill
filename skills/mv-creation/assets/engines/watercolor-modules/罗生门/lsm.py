# lsm.py: 《罗生门（Follow）》 scenes, props and phone UI (watercolour, vertical 2:3 logical canvas 1080x1620).
# Story device: the two-city weather (「我这 · 南方 小雨」 / 「她那 · 北方 大雪」) and the nightly 「示例歌词占位文字？」.
import math
from eng import *
import eng
from hl import tint, desat, vignette
from couple import jhim, jher, part, _P

WK = 'LXGWWenKai-Regular.ttf'
CREAM = PAL['cream']


def wrapText(s, n):
    out, line = [], ''
    for ch in s:
        line += ch
        if len(line) >= n:
            out.append(line)
            line = ''
    if line:
        out.append(line)
    return out


# ================================================================ overlays: narration, corner tag, name card (from 《匆匆那年》 cc.py)
def softBand(cx, cy, w, h, a, col='#0B1022'):
    if a <= .01:
        return
    pa = skia.Paint(AntiAlias=True, Color=skcol(col, a))
    pa.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, h * .28))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(cx - w / 2, cy - h / 2, w, h), h / 2, h / 2, pa)


def narration(t, items, y=96, size=50):
    """first-person narration, one short line at a time, top centre (lyrics stay at the bottom); 4th item 'her' = her voice"""
    for it in items:
        a, b, s = it[0], it[1], it[2]
        who = it[3] if len(it) > 3 else 'him'
        if a <= t <= b:
            k = ease(seg(t, a, a + .45)) * (1 - ease(seg(t, b - .45, b)))
            if k <= .01:
                continue
            dy = (1 - ease(seg(t, a, a + .7))) * 10
            w = textW(s, size, WK)
            softBand(W / 2, y + dy, w + 170, size * 1.5, .36 * k)
            text(s, W / 2, y + dy, size, CREAM, face=WK, stroke=INK, strokeW=size * .15, shadow=True, a=k)
            mx = W / 2 - w / 2 - 34
            if who == 'him':
                G.c.drawRoundRect(skia.Rect.MakeXYWH(mx - 11, y + dy - 11, 22, 22), 4, 4, skia.Paint(AntiAlias=True, Color=skcol('#3B5B98', k)))
            else:
                G.c.drawCircle(mx, y + dy, 11, skia.Paint(AntiAlias=True, Color=skcol('#CC3B42', k)))
            G.c.drawCircle(mx, y + dy, 13, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skcol(INK, k)))


def cornerTag(t, items, x=56, y=184, size=34):
    for (a, b, s) in items:
        if a <= t <= b:
            k = ease(seg(t, a, a + .5)) * (1 - ease(seg(t, b - .5, b)))
            if k > .01:
                tw = textW(s, size, WK)
                softBand(x + tw / 2, y + 4, tw + 80, size * 1.6, .30 * k)
                text(s, x, y, size, CREAM, face=WK, align='left', stroke=INK, strokeW=6, shadow=False, a=k)
                G.c.drawLine(x + 2, y + size * .72, x + tw * ease(seg(t, a + .2, a + .9)), y + size * .74,
                             skia.Paint(AntiAlias=True, Color=skcol(CREAM, .8 * k), StrokeWidth=2.4, StrokeCap=skia.Paint.kRound_Cap))


def nameCard(x, y, name, sub, k, rot=-.035, key='nc', pin='#3B5B98'):
    if k <= .01:
        return
    push()
    translate(x, y + (1 - ease(clamp(k))) * 14)
    rotate(rot)
    w = max(textW(name, 40, WK), textW(sub, 26, WK)) + 64
    h = 108
    G.c.saveLayerAlpha(None, int(255 * clamp(k)))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(-w / 2 + 7, -h / 2 + 9, w, h), 10, 10, skia.Paint(AntiAlias=True, Color=skcol('#000000', .25)))
    boilSeed(key)
    paint(rrPts(-w / 2, -h / 2, w, h, 10), wash='#FBF5E6', fill='#EADFC6', fillOp=50, ink=INK, sw=.8, lite=True)
    paint(ellPts(0, -h / 2 + 11, 9, 9, 12), wash=pin, ink=INK, sw=.5)
    text(name, 0, -10, 40, INK, face=WK, shadow=False)
    text(sub, 0, 30, 26, '#5E5668', face=WK, shadow=False)
    G.c.restore()
    pop()


# ================================================================ weather: rain, snow, icons
def rain(t, x0, y0, x1, y1, n=120, a=.55, ang=.22, speed=1500, seed=3, col='#CFE3F5', ln=46, sw=2.2):
    pa = skia.Paint(AntiAlias=True, Color=skcol(col, a), StrokeWidth=sw, StrokeCap=skia.Paint.kRound_Cap)
    h = y1 - y0
    for i in range(n):
        r1, r2, r3 = hash1(i * 3 + seed), hash1(i * 7 + seed * 5), hash1(i * 13 + seed * 11)
        sp = speed * (.8 + .4 * r3)
        yy = y0 + (r2 * h + t * sp) % h
        xx = x0 + r1 * (x1 - x0) + (yy - y0) * ang * .0
        L = ln * (.7 + .6 * r3)
        G.c.drawLine(xx, yy, xx - L * ang, yy - L, pa)


def splashes(t, x0, x1, y, n=14, a=.5, seed=9, col='#E4F0FA'):
    for i in range(n):
        ph = frac(t * (1.6 + hash1(i + seed)) + hash1(i * 5 + seed))
        x = x0 + hash1(i * 11 + seed) * (x1 - x0)
        r = 4 + ph * 18
        G.c.drawOval(skia.Rect.MakeXYWH(x - r, y - r * .3, 2 * r, r * .6),
                     skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2, Color=skcol(col, a * (1 - ph))))


def snow(t, x0, y0, x1, y1, n=90, a=.9, speed=90, seed=5, r0=3.0, r1=7.5, drift=26, col='#FFFFFF'):
    h = y1 - y0
    for i in range(n):
        q1, q2, q3 = hash1(i * 3 + seed), hash1(i * 7 + seed * 5), hash1(i * 13 + seed * 11)
        sp = speed * (.6 + .8 * q3)
        yy = y0 + (q2 * h + t * sp) % h
        xx = x0 + q1 * (x1 - x0) + math.sin(t * (.8 + q3) + i) * drift
        r = lerp(r0, r1, q3)
        G.c.drawCircle(xx, yy, r, skia.Paint(AntiAlias=True, Color=skcol(col, a * (.6 + .4 * q1))))


def snowflake(x, y, r, col=INK, sw=3.0, a=1.0, rot=0.0):
    pa = skia.Paint(AntiAlias=True, Color=skcol(col, a), StrokeWidth=sw, StrokeCap=skia.Paint.kRound_Cap, Style=skia.Paint.kStroke_Style)
    for k in range(6):
        an = rot + k * math.pi / 3
        ex, ey = x + math.cos(an) * r, y + math.sin(an) * r
        G.c.drawLine(x, y, ex, ey, pa)
        for f in (.55,):
            mx, my = x + math.cos(an) * r * f, y + math.sin(an) * r * f
            for s in (-1, 1):
                b = an + s * .7
                G.c.drawLine(mx, my, mx + math.cos(b) * r * .32, my + math.sin(b) * r * .32, pa)


def cloudIcon(x, y, s, col='#9FB3CC', drops=True, t=0.0, a=1.0):
    pts = []
    for (cx, cy, r) in ((-.55, .05, .45), (-.1, -.25, .55), (.45, -.05, .48), (.75, .2, .32), (-.85, .25, .3)):
        pass
    boilSeed('cloudicon')
    paint(ellPts(x - .5 * s, y + .05 * s, .45 * s, .38 * s, 18), wash=col, washOp=int(255 * a), ink=None)
    paint(ellPts(x + .05 * s, y - .22 * s, .55 * s, .5 * s, 18), wash=col, washOp=int(255 * a), ink=None)
    paint(ellPts(x + .55 * s, y + .05 * s, .42 * s, .36 * s, 18), wash=col, washOp=int(255 * a), ink=None)
    paint(rrPts(x - .9 * s, y - .05 * s, 1.8 * s, .45 * s, .2 * s), wash=col, washOp=int(255 * a), ink=None)
    if drops:
        for i in range(3):
            ph = frac(t * 1.4 + i * .33)
            dx = x + (-.5 + i * .5) * s
            dy = y + (.55 + ph * .5) * s
            G.c.drawLine(dx, dy, dx - .08 * s, dy + .22 * s, skia.Paint(AntiAlias=True, Color=skcol('#5D8FC9', a * (1 - ph)), StrokeWidth=s * .07,
                                                                           StrokeCap=skia.Paint.kRound_Cap))


# ================================================================ the two-city weather chalkboard (the device)
def weatherBoard(cx, cy, w, h, t, her='大雪', herT='-12℃', mine='小雨', mineT='12℃', storm=0.0, circle=0.0, note=0.0,
                 labels=('我这 · 南方', '她那 · 北方'), icons=('rain', 'snow'), unified=None, noteTxt='她怕冷'):
    """small blackboard on his wall: 「今日天气」, left half 我这·南方 (rain), right half 她那·北方 (snow); storm shakes her icon"""
    x, y = cx - w / 2, cy - h / 2
    boilSeed('wb frame')
    paint(rrPts(x - 18, y - 18, w + 36, h + 36, 10), wash='#8A5A3C', fill='#6E4630', fillOp=110, ink=INK, sw=1.0)
    paint(rrPts(x, y, w, h, 6), wash='#2F4A43', fill='#243C36', fillOp=120, ink=INK, sw=.7)
    ch = '#F3F0E6'
    text('今日天气', cx, y + 46, 40, ch, face=WK, shadow=False, a=.92)
    for s in (-1, 1):
        paint(heartPts(cx + s * 118, y + 46, 11), wash='#F19A92', ink=None)
    if unified:
        # the ending: one weather for both of them
        G.c.drawCircle(cx, y + 200, 58, skia.Paint(AntiAlias=True, Color=skcol('#FFD27A', .95)))
        for k in range(10):
            an = k / 10 * TAU + t * .4
            G.c.drawLine(cx + math.cos(an) * 74, y + 200 + math.sin(an) * 74, cx + math.cos(an) * 100, y + 200 + math.sin(an) * 100,
                         skia.Paint(AntiAlias=True, Color=skcol('#FFD27A', .9), StrokeWidth=6, StrokeCap=skia.Paint.kRound_Cap))
        text(unified[0], cx, y + 118, 32, ch, face=WK, shadow=False, a=.9)
        text(unified[1], cx, y + 310, 48, ch, face=WK, shadow=False)
        paint(rrPts(x - 10, y + h + 14, w + 20, 16, 4), wash='#7A4E36', ink=INK, sw=.6)
        return
    G.c.drawLine(cx, y + 86, cx, y + h - 24, skia.Paint(AntiAlias=True, Color=skcol(ch, .55), StrokeWidth=3))
    lx, rx = x + w * .25, x + w * .75
    text(labels[0], lx, y + 112, 30, ch, face=WK, shadow=False, a=.85)
    text(labels[1], rx, y + 112, 30, ch, face=WK, shadow=False, a=.85)
    sh = storm * math.sin(t * 38) * 4
    for (ix, kind, shake) in ((lx, icons[0], 0), (rx, icons[1], sh)):
        if kind == 'rain':
            cloudIcon(ix + shake, y + 190, 62, '#C9D6E6', True, t, .95)
        else:
            for k in range(3 if storm < .5 else 5):
                snowflake(ix - 40 + (k % 3) * 40 + shake, y + 175 + (k // 3) * 36 + (k % 2) * 16, 15 + storm * 4, ch, 3.2, .95, t * .3 + k)
    text(mine, lx, y + 285, 40, ch, face=WK, shadow=False)
    text(mineT, lx, y + 335, 38, '#BFE3F2', face=WK, shadow=False)
    text(her, rx + sh, y + 285, 40 + storm * 6, '#FFD7D2' if storm > .5 else ch, face=WK, shadow=False)
    text(herT, rx + sh, y + 335, 38, '#BFE3F2', face=WK, shadow=False)
    if circle > .01:
        n = int(40 * clamp(circle))
        pts = [[rx + math.cos(-1.9 + i / 40 * TAU * 1.05) * 108, y + 300 + math.sin(-1.9 + i / 40 * TAU * 1.05) * 62] for i in range(n + 1)]
        if len(pts) > 2:
            boilSeed('wb circ')
            inkLine(pts, 1.1, '#E9585E', 'ink', .4)
    # chalk ledge with chalk + eraser
    paint(rrPts(x - 10, y + h + 14, w + 20, 16, 4), wash='#7A4E36', ink=INK, sw=.6)
    paint(rrPts(x + 40, y + h + 2, 46, 14, 5), wash='#F3F0E6', ink=INK, sw=.4)
    paint(rrPts(x + w - 120, y + h - 4, 70, 22, 4), wash='#C9A27A', ink=INK, sw=.5)
    if note > .01:
        push()
        translate(x + w + 4, y + h + 6)
        rotate(.14)
        G.c.saveLayerAlpha(None, int(255 * clamp(note)))
        paint(rrPts(-62, -40, 124, 80, 4), wash='#FFE58A', ink=INK, sw=.5)
        text(noteTxt, 0, 2, 32, INK, face=WK, shadow=False)
        G.c.restore()
        pop()


# ================================================================ his room at night (vertical)
def stringLights(t, y0=150, x0=-40, x1=W + 40, n=13, sag=60, a=1.0):
    pts = []
    for i in range(41):
        q = i / 40
        pts.append([lerp(x0, x1, q), y0 + math.sin(q * math.pi) * sag])
    boilSeed('wire')
    inkLine(pts, .5, '#3A3346', 'inkfine', .3)
    cols = ['#FFD27A', '#FFB2A6', '#BFE3F2', '#FFE7A8']
    for i in range(n):
        q = (i + .5) / n
        bx, by = lerp(x0, x1, q), y0 + math.sin(q * math.pi) * sag + 16
        tw = .75 + .25 * math.sin(t * 2.3 + i * 1.7)
        glow(bx, by, 46, cols[i % 4], .55 * tw * a)
        paint(ellPts(bx, by, 9, 13, 10), wash=cols[i % 4], ink=INK, sw=.35)


def polaroid(x, y, w, rot, draw, key='pol', pin='#E9585E'):
    push()
    translate(x, y)
    rotate(rot)
    h = w * 1.18
    G.c.drawRect(skia.Rect.MakeXYWH(-w / 2 + 6, -h / 2 + 8, w, h), skia.Paint(AntiAlias=True, Color=skcol('#000000', .22)))
    boilSeed(key)
    paint(rectPts(-w / 2, -h / 2, w, h), wash='#FFFDF6', ink=INK, sw=.5)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(-w / 2 + 9, -h / 2 + 9, w - 18, w - 18))
    draw(-w / 2 + 9, -h / 2 + 9, w - 18)
    G.c.restore()
    paint(ellPts(0, -h / 2 + 4, 7, 7, 10), wash=pin, ink=INK, sw=.4)
    pop()


def miniCouple(x, y, s, umbrella=True):
    """tiny photo content: the two of them under one yellow umbrella in the rain"""
    gradRect(x, y, s, s, ['#9FB4CF', '#C9D4E2'])
    if umbrella:
        paint([[x + s * .14, y + s * .42], [x + s * .5, y + s * .16], [x + s * .86, y + s * .42]], wash='#F2C14E', ink=INK, sw=.4)
        G.c.drawLine(x + s * .5, y + s * .3, x + s * .5, y + s * .7, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=2))
    for (cx, hc, bc) in ((.36, '#2C2536', '#3B5B98'), (.64, '#6B3D2B', '#EFE4CB')):
        paint(ellPts(x + s * cx, y + s * .55, s * .1, s * .1, 12), wash='#F2C9A8', ink=INK, sw=.3)
        paint(ellPts(x + s * cx, y + s * .5, s * .11, s * .06, 12), wash=hc, ink=None)
        paint(rrPts(x + s * (cx - .1), y + s * .65, s * .2, s * .3, 4), wash=bc, ink=INK, sw=.3)
    paint(rectPts(x + s * .58, y + s * .68, s * .12, s * .04), wash='#CC3B42', ink=None)


def miniSnowman(x, y, s):
    gradRect(x, y, s, s, ['#C9D8EA', '#EEF3FA'])
    paint(ellPts(x + s * .5, y + s * .72, s * .22, s * .2, 16), wash='#FFFFFF', ink=INK, sw=.35)
    paint(ellPts(x + s * .5, y + s * .45, s * .15, s * .14, 16), wash='#FFFFFF', ink=INK, sw=.35)
    paint(rectPts(x + s * .36, y + s * .52, s * .28, s * .05), wash='#CC3B42', ink=None)
    paint([[x + s * .5, y + s * .45], [x + s * .62, y + s * .47], [x + s * .5, y + s * .49]], wash='#F08A3C', ink=None)
    for i in range(10):
        G.c.drawCircle(x + hash1(i) * s, y + hash1(i + 9) * s * .7, 2.5, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .9)))


def miniSnowStreet(x, y, s):
    gradRect(x, y, s, s, ['#5A6C94', '#9FB0CC'])
    for i in range(4):
        paint(rectPts(x + s * (.05 + i * .24), y + s * (.3 + .1 * (i % 2)), s * .2, s * .7), wash='#3E4A6C', ink=None)
        for j in range(3):
            paint(rectPts(x + s * (.09 + i * .24), y + s * (.4 + j * .14 + .1 * (i % 2)), s * .05, s * .05), wash='#FFD27A', ink=None)
    paint(rectPts(x, y + s * .82, s, s * .18), wash='#F3F6FB', ink=None)
    for i in range(14):
        G.c.drawCircle(x + hash1(i * 3) * s, y + hash1(i * 5) * s * .8, 2.2, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .9)))


def miniSunset(x, y, s):
    gradRect(x, y, s, s, ['#F7B27A', '#F48F8F', '#8C7BB8'])
    paint(ellPts(x + s * .5, y + s * .62, s * .14, s * .14, 16), wash='#FFE3A0', ink=None)
    paint(rectPts(x, y + s * .7, s, s * .3), wash='#5A4E7E', ink=None)


def miniUmbrella(x, y, s):
    gradRect(x, y, s, s, ['#B8C6DA', '#E2E8F1'])
    paint([[x + s * .12, y + s * .5], [x + s * .5, y + s * .18], [x + s * .88, y + s * .5]], wash='#F2C14E', ink=INK, sw=.4)
    G.c.drawLine(x + s * .5, y + s * .35, x + s * .5, y + s * .82, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=2.4))
    for i in range(10):
        G.c.drawCircle(x + hash1(i * 3) * s, y + hash1(i * 5) * s, 2.2, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .9)))


PICS = dict(couple=miniCouple, snowman=miniSnowman, street=miniSnowStreet, sunset=miniSunset, umbrella=miniUmbrella)


def ticket(x, y, w, rot=0.0, txt='南方 → 北方', sub='K1314 · 未使用', a=1.0, key='tk'):
    push()
    translate(x, y)
    rotate(rot)
    h = w * .45
    boilSeed(key)
    paint(rrPts(-w / 2, -h / 2, w, h, 6), wash='#F6C9C2', fill='#E9A9A0', fillOp=40, ink=INK, sw=.5)
    G.c.drawLine(w * .22, -h / 2 + 6, w * .22, h / 2 - 6, skia.Paint(AntiAlias=True, Color=skcol(INK, .5), StrokeWidth=2,
                                                                     PathEffect=skia.DashPathEffect.Make([6, 6], 0)))
    text(txt, -w * .12, -h * .12, w * .12, INK, face=WK, shadow=False, a=a)
    text(sub, -w * .12, h * .22, w * .075, '#7A5A60', face=WK, shadow=False, a=a)
    pop()


def calendarNov(x, y, w, t, upto=20, circ=20):
    h = w * 1.05
    boilSeed('cal')
    paint(rectPts(x, y, w, h), wash='#FFFDF6', ink=INK, sw=.6)
    paint(rectPts(x, y, w, h * .2), wash='#E9585E', ink=INK, sw=.5)
    text('11月', x + w / 2, y + h * .1, w * .13, '#FFFDF6', face=WK, shadow=False)
    cw, chh = w / 7, (h * .78) / 5
    for d in range(30):
        c, r = (d + 6) % 7, (d + 6) // 7
        if r > 4:
            continue
        cx, cy = x + cw * (c + .5), y + h * .22 + chh * (r + .5)
        text(str(d + 1), cx, cy, w * .062, '#4A4458', face=WK, shadow=False, a=.8)
        if d + 1 < upto:
            pa = skia.Paint(AntiAlias=True, Color=skcol('#E9585E', .7), StrokeWidth=2.2)
            G.c.drawLine(cx - 8, cy - 8, cx + 8, cy + 8, pa)
            G.c.drawLine(cx + 8, cy - 8, cx - 8, cy + 8, pa)
        if d + 1 == circ:
            G.c.drawOval(skia.Rect.MakeXYWH(cx - 15, cy - 13, 30, 26), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3,
                                                                                  Color=skcol('#3B5B98', .9)))


def guitarOnStand(x, y, s=1.0):
    """acoustic guitar standing on a little stand; (x, y) = floor point"""
    push()
    translate(x, y)
    scale(s, s)
    boilSeed('gtr')
    inkLine([[-30, 0], [0, -60], [30, 0]], 1.0, '#2F2A33', 'ink', 0)
    body = [[0, -330], [-52, -300], [-62, -250], [-44, -205], [-76, -150], [-80, -95], [-56, -58], [0, -48], [56, -58], [80, -95], [76, -150], [44, -205], [62, -250], [52, -300]]
    paint(throughClosed(body, 4), wash='#C98A4E', fill='#A86A36', fillOp=120, ink=INK, sw=.9)
    paint(ellPts(0, -205, 22, 22, 18), wash='#3A2A22', ink=INK, sw=.5)
    paint(rectPts(-12, -520, 24, 200), wash='#6E4A30', ink=INK, sw=.6)
    paint(rrPts(-20, -575, 40, 60, 8), wash='#4A3226', ink=INK, sw=.6)
    for i in range(3):
        G.c.drawLine(-4 + i * 4, -560, -4 + i * 4, -70, skia.Paint(AntiAlias=True, Color=skcol('#EDE6D6', .7), StrokeWidth=1.2))
    paint(rectPts(-30, -98, 60, 10), wash='#3A2A22', ink=None)
    paint(heartPts(-42, -130, 9), wash='#E84A5F', ink=INK, sw=.3)      # the red heart pick stuck on the guard
    pop()


def deskLamp(x, y, on=1.0, flip=False):
    push()
    translate(x, y)
    if flip:
        scale(-1, 1)
    if on > 0:
        glow(70, -150, 260, '#FFCB7A', .55 * on)
    boilSeed('lamp')
    paint(ellPts(0, -6, 46, 12, 18), wash='#3F4A66', ink=INK, sw=.6)
    inkLine([[0, -10], [-14, -110], [50, -170]], 1.4, '#3F4A66', 'ink', .3)
    paint([[30, -200], [100, -170], [80, -130], [20, -150]], wash='#3F4A66', ink=INK, sw=.6)
    paint(ellPts(85, -142, 22, 10, 12, rot=.5), wash='#FFF1C8', ink=None)
    pop()


def cupNoodle(x, y, s=1.0):
    push()
    translate(x, y)
    scale(s, s)
    boilSeed('cup')
    paint([[-34, -86], [34, -86], [26, 0], [-26, 0]], wash='#FFFDF6', ink=INK, sw=.6)
    paint([[-32, -62], [32, -62], [30, -40], [-30, -40]], wash='#E9585E', ink=None)
    paint(ellPts(0, -88, 36, 9, 14), wash='#E9E2D2', ink=INK, sw=.5)
    for i in range(2):
        inkLine([[-8 + i * 16, -100], [-2 + i * 16, -130], [-10 + i * 16, -160]], .4, '#FFFFFF', 'inkfine', .5)
    pop()


def phoneObj(x, y, w, rot=0.0, glowK=1.0, screen=None):
    h = w * 1.9
    push()
    translate(x, y)
    rotate(rot)
    if glowK > 0:
        glow(0, 0, w * 2.6, '#BFE3FF', .5 * glowK)
    boilSeed('phone')
    paint(rrPts(-w / 2, -h / 2, w, h, w * .16), wash='#2B2A36', ink=INK, sw=.6)
    paint(rrPts(-w / 2 + 4, -h / 2 + 4, w - 8, h - 8, w * .13), wash='#D8E8F7' if glowK > .3 else '#1A1C26', ink=None)
    if screen:
        G.c.save()
        G.c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(-w / 2 + 4, -h / 2 + 4, w - 8, h - 8), w * .13, w * .13), True)
        screen(-w / 2 + 4, -h / 2 + 4, w - 8, h - 8)
        G.c.restore()
    pop()


def hisRoom(t, storm=0.0, circle=0.0, note=0.0, her='大雪', herT='-12℃', lamp=1.0, who='him', mine='小雨', mineT='12℃', unified=None,
            morning=0.0, noteTxt='她怕冷'):
    """his rented room at night, vertical: string lights, the weather board, calendar, cork board, guitar, desk at y 1195"""
    if who == 'her':
        gradRect(-400, -400, W + 800, H + 800, ['#4A3550', '#5E4462', '#6E5070'])
    else:
        gradRect(-400, -400, W + 800, H + 800, ['#2B2F52', '#3B3A62', '#4A4468'])
    if morning > .01:
        gradRect(-400, -400, W + 800, H + 800, ['#E9D6B8', '#F2E2C4', '#E6CFA8'], a=morning * .75)
    # wallpaper: faint vertical stripes + a warm pool of lamplight
    for i in range(-2, 16):
        flatRect(i * 80, -200, 3, 1450, '#5A5682', .25)
    glow(330, 1010, 640, '#FFC07A', .30 * lamp)
    flatRect(-400, -400, W + 800, 210, '#232645', 1.0)
    stringLights(t, 150)
    if who == 'her':
        weatherBoard(W / 2 - 10, 450, 640, 380, t, her=her, herT=herT, mine=mine, mineT=mineT, storm=storm, circle=circle, note=note,
                     labels=('我这 · 北方', '他那 · 南方'), icons=('snow', 'rain'), noteTxt=noteTxt)
    else:
        weatherBoard(W / 2 - 10, 450, 640, 380, t, her=her, herT=herT, mine=mine, mineT=mineT, storm=storm, circle=circle, note=note,
                     unified=unified, noteTxt=noteTxt)
    # cork board with photos + an unused ticket
    boilSeed('cork')
    paint(rectPts(70, 760, 330, 300), wash='#C79A6B', fill='#B0845A', fillOp=90, ink=INK, sw=.8)
    polaroid(160, 860, 120, -.12, miniCouple, 'p1')
    polaroid(310, 880, 112, .1, miniSnowman, 'p2', '#3B5B98')
    ticket(235, 1010, 170, -.05, key='tk1')
    calendarNov(705, 735, 190, t)
    # sticky notes on the wall
    notes = ((610, 760, .08, '北方 -12℃\n多穿点', '#FFE58A'), (640, 900, -.1, '23:00\n问天气', '#BFE3C8')) if who == 'him' else \
            ((610, 760, .08, '他没带伞\n雨天', '#FFC9C2'), (640, 900, -.1, '23:00\n等他问', '#BFE3C8'))
    for (nx, ny, nr, s, col) in notes:
        push()
        translate(nx, ny)
        rotate(nr)
        boilSeed(s)
        paint(rectPts(-62, -50, 124, 100), wash=col, ink=INK, sw=.4)
        for j, ln in enumerate(s.split('\n')):
            text(ln, 0, -16 + j * 34, 24, INK, face=WK, shadow=False)
        pop()
    roomLife(t, who)
    if who == 'her':
        hangingUmbrella(980, 760, t, present=lamp)
        glow(880, 1240, 140, '#FFB070', .25)
        boilSeed('radiator')
        paint(rrPts(800, 1150, 170, 140, 10), wash='#E9E2D2', ink=INK, sw=.6)
        for j in range(6):
            G.c.drawLine(822 + j * 26, 1162, 822 + j * 26, 1278, skia.Paint(AntiAlias=True, Color=skcol('#BDB6AA'), StrokeWidth=5))
    else:
        guitarOnStand(975, 1290, 1.0)
    # floor
    if who == 'her':
        flatRect(-400, 1290, W + 800, 800, '#6A4A3A', 1.0)
        for i in range(8):
            flatRect(-400, 1300 + i * 46, W + 800, 2, '#4A3226', .5)
        boilSeed('rugh')
        paint(ellPts(470, 1460, 420, 90, 32), wash='#E9B8B0', fill='#D99A92', fillOp=90, ink=INK, sw=.6)
        for sx in (520, 588):
            paint(ellPts(sx, 1500, 30, 14, 14, rot=.2), wash='#F19A92', ink=INK, sw=.45)
        roomLife(t, who, 'floor')
        return
    flatRect(-400, 1290, W + 800, 800, '#5A4234', 1.0)
    for i in range(8):
        flatRect(-400, 1300 + i * 46, W + 800, 2, '#3E2C22', .5)
    boilSeed('rug')
    paint(ellPts(470, 1460, 420, 90, 32), wash='#7E5C86', fill='#6A4A72', fillOp=90, ink=INK, sw=.6)
    for i in range(3):
        paint(ellPts(470, 1460, 360 - i * 90, 70 - i * 18, 32), wash=None, ink='#A68AAE', sw=.35, br='inkfine')
    # open guitar case on the floor (the guitar is on its stand), a set list and the red pick inside
    boilSeed('gcase')
    case = [[60, 1420], [150, 1380], [330, 1372], [420, 1400], [425, 1470], [330, 1500], [150, 1494], [58, 1468]]
    paint(throughClosed(case, 3), wash='#3A2B27', ink=INK, sw=.8)
    paint(throughClosed([[90, 1426], [160, 1398], [320, 1392], [392, 1414], [394, 1458], [320, 1478], [160, 1474], [88, 1456]], 3), wash='#8E2F3A', fill='#6E2230', fillOp=90, ink=None)
    push()
    translate(240, 1436)
    rotate(-.08)
    paint(rectPts(-60, -26, 120, 52), wash='#FFFDF6', ink=INK, sw=.35)
    for j in range(3):
        G.c.drawLine(-46, -12 + j * 13, 40, -12 + j * 13, skia.Paint(AntiAlias=True, Color=skcol('#5E5668', .6), StrokeWidth=2))
    pop()
    paint(heartPts(340, 1440, 10), wash='#E84A5F', ink=INK, sw=.3)
    # slippers
    for sx in (520, 588):
        paint(ellPts(sx, 1500, 30, 14, 14, rot=.2), wash='#5D8FC9', ink=INK, sw=.45)
    # small electric heater glowing (warm here; cold up north)
    glow(868, 1320, 150, '#FF9A4A', .45)
    boilSeed('heater')
    paint(rrPts(810, 1240, 116, 110, 14), wash='#E9E2D2', ink=INK, sw=.6)
    for j in range(3):
        paint(rrPts(826, 1258 + j * 28, 84, 14, 7), wash='#FF8A3C', ink=None)
    roomLife(t, who, 'floor')


def deskTop(t, x0=110, x1=870, y=1195, legs=True):
    boilSeed('desk')
    if legs:
        for lx in (x0 + 30, x1 - 30):
            paint(rectPts(lx - 9, y, 18, 1290 - y), wash='#6E4A30', ink=INK, sw=.6)
    paint(rrPts(x0, y - 8, x1 - x0, 22, 5), wash='#9A6A44', fill='#7E5434', fillOp=80, ink=INK, sw=.8)


def chairBack(x, y_seat, u):
    boilSeed('chair')
    paint(rrPts(x - 5.6 * u, y_seat - 9.5 * u, 11.2 * u, 7.0 * u, 18), wash='#7E5434', ink=INK, sw=.8)
    paint(rrPts(x - 6.0 * u, y_seat - .4 * u, 12.0 * u, 1.0 * u, 6), wash='#9A6A44', ink=INK, sw=.7)
    for s in (-1, 1):
        paint(rectPts(x + s * 5.2 * u - 8, y_seat + .5 * u, 16, 2.4 * u), wash='#6E4A30', ink=INK, sw=.5)


def deskItems(t, lampOn=1.0, who='him'):
    deskLamp(170, 1190, lampOn)
    if who == 'her':
        deskItemsHer(t)
        return
    boilSeed('books')
    for i, (bw, col) in enumerate(((150, '#5D8FC9'), (140, '#E9A23B'), (156, '#7FB08A'))):
        paint(rrPts(280 - bw / 2, 1188 - 26 * (i + 1), bw, 24, 4), wash=col, ink=INK, sw=.5)
    cupNoodle(760, 1190, .95)
    paint(rrPts(640, 1158, 80, 30, 6), wash='#FFFDF6', ink=INK, sw=.5)        # mug
    paint(ellPts(722, 1172, 14, 12, 10), wash=None, ink=INK, sw=.5)
    for i in range(3):                                                          # music sheets
        push()
        translate(560 + i * 8, 1182)
        rotate(-.05 + i * .04)
        paint(rectPts(-60, -10, 120, 12), wash='#FFFDF6', ink=INK, sw=.35)
        pop()


# ================================================================ phone UI
THEMES = dict(
    now=dict(bg='#E3E8F0', bg2='#D5DCE8', head='#F7F8FB', me='#B7E3A6', meDk='#8CC27A', her='#FFFFFF', txt='#1F2233', sep='#8A90A2', ink=INK),
    old=dict(bg='#EFE2C6', bg2='#E6D4B1', head='#F7EEDC', me='#E7D08E', meDk='#C8AD62', her='#FFF8EA', txt='#4A3A2A', sep='#9A8466', ink='#5A4632'),
)


def avatarHer(x, y, r):
    G.c.save()
    G.c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), r * .3, r * .3), True)
    flatRect(x - r, y - r, 2 * r, 2 * r, '#CFE0F2')
    paint(ellPts(x, y - r * .05, r * .78, r * .72, 16), wash='#6B3D2B', ink=None)
    paint(ellPts(x, y + r * .12, r * .56, r * .52, 16), wash='#F6D0B2', ink=None)
    flatRect(x - r * .56, y - r * .38, r * 1.12, r * .3, '#6B3D2B')
    paint(rectPts(x - r * .5, y + r * .62, r, r * .3), wash='#CC3B42', ink=None)
    for s in (-1, 1):
        G.c.drawCircle(x + s * r * .2, y + r * .12, r * .07, skia.Paint(AntiAlias=True, Color=skcol(INK)))
    G.c.restore()
    paint(rrPts(x - r, y - r, 2 * r, 2 * r, r * .3), wash=None, ink=INK, sw=.4)


def statusBar(clock, th, dark=False, batt=.62):
    col = '#FFFFFF' if dark else th['txt']
    text(clock, 70, 38, 30, col, face=WK, align='left', shadow=False)
    for i in range(4):
        h = 8 + i * 5
        G.c.drawRect(skia.Rect.MakeXYWH(860 + i * 11, 50 - h, 7, h), skia.Paint(AntiAlias=True, Color=skcol(col, .9)))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(920, 26, 58, 26), 6, 6, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=2.4, Color=skcol(col)))
    G.c.drawRect(skia.Rect.MakeXYWH(924, 30, 50 * batt, 18), skia.Paint(AntiAlias=True, Color=skcol('#E9585E' if batt < .2 else col)))


def bubble(x, y, s, mine, th, wmax=600, size=44, a=1.0):
    """chat bubble; mine = right aligned at x (right edge), else left aligned at x; returns height"""
    lines = wrapText(s, 12)
    tw = max(textW(l, size, WK) for l in lines)
    w, h = tw + 56, len(lines) * (size + 12) + 34
    bx = x - w if mine else x
    col = th['me'] if mine else th['her']
    G.c.saveLayerAlpha(None, int(255 * a))
    boilSeed(f'bub{s}{mine}')
    paint(rrPts(bx, y, w, h, 22), wash=col, ink=th['ink'], sw=.55)
    tx = bx + w - 14 if mine else bx + 14
    paint([[tx - 8, y + 26], [tx + (14 if mine else -14), y + 34], [tx - 8 if mine else tx + 8, y + 46]], wash=col, ink=None)
    for j, l in enumerate(lines):
        text(l, bx + 28, y + 17 + size / 2 + j * (size + 12), size, th['txt'], face=WK, align='left', shadow=False)
    G.c.restore()
    return h


def picBubble(x, y, kind, mine, th, s=300, a=1.0):
    bx = x - s if mine else x
    G.c.saveLayerAlpha(None, int(255 * a))
    G.c.save()
    G.c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(bx, y, s, s), 20, 20), True)
    PICS[kind](bx, y, s)
    G.c.restore()
    boilSeed(f'pic{kind}')
    paint(rrPts(bx, y, s, s, 20), wash=None, ink=th['ink'], sw=.6)
    G.c.restore()
    return s


def chatScreen(t, items, theme='now', clock='23:00', scroll=0.0, a_items=None, title='她', sub='北方 · 大雪', batt=.62, pulse=1.0, bottom=1410):
    """full-canvas chat page. items: list of (kind, text) with kind in sep|me|her|mepic|herpic|status; a_items: per-item alpha"""
    th = THEMES[theme]
    gradRect(-400, -400, W + 800, H + 800, [th['bg'], th['bg2']])
    # wallpaper doodles: faint snowflakes and raindrops
    for i in range(16):
        x, y = hash1(i * 3) * W, 220 + hash1(i * 7) * 1150
        if i % 2:
            snowflake(x, y, 16, th['sep'], 2, .14, i)
        else:
            G.c.drawLine(x, y, x - 6, y + 22, skia.Paint(AntiAlias=True, Color=skcol(th['sep'], .16), StrokeWidth=3, StrokeCap=skia.Paint.kRound_Cap))
    def hOf(kind, s):
        if kind == 'sep':
            return 74
        if kind in ('me', 'her'):
            return len(wrapText(s, 12)) * 56 + 34 + 26
        if kind in ('mepic', 'herpic'):
            return 326
        return 30
    total = sum(hOf(k_, s_) for k_, s_ in items)
    y = max(250, bottom - total) - scroll
    for i, (kind, s) in enumerate(items):
        al = 1.0 if a_items is None else a_items[i]
        if kind == 'sep':
            if al > .01:
                tw = textW(s, 30, WK)
                G.c.drawRoundRect(skia.Rect.MakeXYWH(W / 2 - tw / 2 - 22, y, tw + 44, 46), 23, 23, skia.Paint(AntiAlias=True, Color=skcol('#000000', .08 * al)))
                text(s, W / 2, y + 23, 30, th['sep'], face=WK, shadow=False, a=al)
            y += 74
        elif kind in ('me', 'her'):
            if al > .01:
                if kind == 'her':
                    avatarHer(100, y + 38, 38)
                h = bubble(890 if kind == 'me' else 160, y, s, kind == 'me', th, a=al)
            else:
                h = len(wrapText(s, 12)) * 56 + 34
            y += h + 26
        elif kind in ('mepic', 'herpic'):
            if al > .01:
                if kind == 'herpic':
                    avatarHer(100, y + 38, 38)
                picBubble(890 if kind == 'mepic' else 160, y, s, kind == 'mepic', th, a=al)
            y += 300 + 26
        elif kind == 'status':
            if al > .01:
                sc_ = pulse if i == len(items) - 1 else 1.0
                text(s, 890, y - 4, 34, '#E9585E' if s == '未读' else th['sep'], face=WK, align='right', shadow=False, a=al, sc=sc_)
            y += 30
    # header + status bar on top
    flatRect(-10, -10, W + 20, 200, th['head'], .97)
    G.c.drawLine(0, 190, W, 190, skia.Paint(AntiAlias=True, Color=skcol(th['sep'], .35), StrokeWidth=2))
    statusBar(clock, th, batt=batt)
    inkLine([[90, 112], [66, 136], [90, 160]], .9, th['txt'], 'ink', 0)
    text(title, W / 2, 122, 46, th['txt'], face=WK, shadow=False)
    snowflake(W / 2 + 58, 120, 14, '#7FA6D6', 2.6, 1.0, .3)
    text(sub, W / 2, 166, 26, th['sep'], face=WK, shadow=False)
    for i in range(3):
        G.c.drawCircle(950 + i * 18, 136, 5, skia.Paint(AntiAlias=True, Color=skcol(th['txt'])))
    # input bar
    flatRect(-10, 1440, W + 20, 200, th['head'], .97)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(120, 1470, 700, 76), 16, 16, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF')))
    G.c.drawCircle(70, 1508, 30, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skcol(th['txt'], .7)))
    G.c.drawCircle(880, 1508, 30, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=3, Color=skcol(th['txt'], .7)))


def rewindBadge(t, a=1.0, fwd=False):
    if a <= .01:
        return
    x, y = W / 2, 262
    G.c.drawRoundRect(skia.Rect.MakeXYWH(x - 130, y - 40, 260, 80), 40, 40, skia.Paint(AntiAlias=True, Color=skcol('#1C1E2C', .78 * a)))
    for k in range(2):
        ox = x - 70 + k * 36
        pts = [[ox + 30, y - 22], [ox, y], [ox + 30, y + 22]] if not fwd else [[ox, y - 22], [ox + 30, y], [ox, y + 22]]
        paint(pts, wash='#FFFDF6', washOp=int(255 * a), ink=None)
    text('×8', x + 62, y + 2, 44, '#FFFDF6', face=WK, shadow=False, a=a)


def scanJitter(t, a=.5):
    """VHS-ish rewind lines over the UI"""
    for i in range(6):
        yy = (hash1(int(t * 24) * 7 + i) * H)
        G.c.drawRect(skia.Rect.MakeXYWH(0, yy, W, 3 + 6 * hash1(i + int(t * 24))), skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .18 * a)))


def lockScreen(t, clock='03:12', date='11月21日 星期六', notif=0.0, dark=0.0):
    gradRect(-400, -400, W + 800, H + 800, ['#1E2340', '#33305A', '#4A3E66'])
    # wallpaper: the two of them under the yellow umbrella, dim
    G.c.saveLayerAlpha(None, 120)
    miniCouple(140, 620, 800)
    G.c.restore()
    flatRect(-400, -400, W + 800, H + 800, '#141830', .35)
    statusBar('', THEMES['now'], dark=True, batt=.41)
    text(date, W / 2, 330, 40, '#FFFFFF', face=WK, shadow=False, a=.9)
    text(clock, W / 2, 470, 190, '#FFFFFF', face=WK, shadow=False, a=.95)
    if notif > .01:
        k = easeOut(clamp(notif))
        y = lerp(560, 640, k)
        G.c.saveLayerAlpha(None, int(255 * clamp(notif * 2)))
        G.c.drawRoundRect(skia.Rect.MakeXYWH(90, y, 900 - 90 + 40 - 40, 210), 34, 34, skia.Paint(AntiAlias=True, Color=skcol('#F4F2F8', .94)))
        paint(rrPts(124, y + 34, 72, 72, 16), wash='#E9585E', ink=None)
        text('!', 160, y + 70, 54, '#FFFFFF', face=WK, shadow=False)
        text('天气预警 · 现在', 220, y + 52, 28, '#6A6478', face=WK, align='left', shadow=False)
        text('北方 暴雪红色预警', 220, y + 104, 44, '#1F2233', face=WK, align='left', shadow=False)
        text('-18℃ 大风 夜间有大到暴雪', 220, y + 158, 32, '#4A4458', face=WK, align='left', shadow=False)
        G.c.restore()
    if dark > .01:
        flatRect(-400, -400, W + 800, H + 800, '#05060C', dark)


# ================================================================ the title gate (罗生门)
def titleGate(t, k=1.0):
    gradRect(-400, -400, W + 800, H + 800, ['#141833', '#232A4E', '#2E3459'])
    x0, x1, y0, y1 = 190, 890, 720, 1320
    mid = (x0 + x1) / 2
    # inside the doorway: left = rain at night (south), right = snow (north)
    G.c.save()
    G.c.clipRect(skia.Rect.MakeLTRB(x0, y0, mid, y1))
    gradRect(x0, y0, mid - x0, y1 - y0, ['#2C3E66', '#4A5F8C'])
    glow(x0 + 120, y0 + 160, 220, '#FFC07A', .35)
    rain(t, x0, y0 - 60, mid, y1, 60, .6, .18, 1500, 4)
    G.c.restore()
    G.c.save()
    G.c.clipRect(skia.Rect.MakeLTRB(mid, y0, x1, y1))
    gradRect(mid, y0, x1 - mid, y1 - y0, ['#8EA2C4', '#D9E2EF'])
    snow(t, mid, y0 - 40, x1, y1, 46, .95, 70, 7, 3, 8)
    flatRect(mid, y1 - 90, x1 - mid, 90, '#F3F6FB')
    G.c.restore()
    # the gate: posts, lintel with a roof
    boilSeed('gate')
    for px in (x0 - 50, x1):
        paint(rectPts(px, y0 - 20, 50, y1 - y0 + 40), wash='#7A3E34', fill='#5E2C26', fillOp=110, ink=INK, sw=.9)
    paint(rectPts(x0 - 90, y0 - 80, x1 - x0 + 180, 70), wash='#7A3E34', fill='#5E2C26', fillOp=110, ink=INK, sw=.9)
    paint([[x0 - 150, y0 - 78], [x1 + 150, y0 - 78], [x1 + 60, y0 - 170], [x0 - 60, y0 - 170]], wash='#3A3346', fill='#2A2436', fillOp=120, ink=INK, sw=.9)
    G.c.drawLine(mid, y0, mid, y1, skia.Paint(AntiAlias=True, Color=skcol('#E9E2D2', .7), StrokeWidth=4))
    # ground outside
    flatRect(-400, y1, W + 800, 800, '#1A1D33')
    # the two of them, backs to us, one in each weather
    # outside the door: rain puddles on her side, a strip of snow with footprints on his side
    for i in range(5):
        boilSeed(f'tpud{i}')
        paint(ellPts(x0 - 60 + i * 80 + 30 * hash1(i), y1 + 60 + 70 * hash1(i * 3), 70, 14, 16), wash='#4A5F8C', washOp=150, ink=None)
    splashes(t, x0 - 120, mid, y1 + 80, 10, .5)
    boilSeed('tsnow')
    paint([[mid, y1], [x1 + 60, y1], [x1 + 200, H + 60], [mid + 40, H + 60]], wash='#DCE4F0', fill='#C9D3E3', fillOp=80, ink=None)
    for i in range(7):
        fx = mid + 150 + 10 * (i % 2) * 3 + i * 6
        fy = y1 + 40 + i * 44
        paint(ellPts(fx + (14 if i % 2 else -14), fy, 9, 15, 10), wash='#9FAECB', washOp=200, ink=None)
    jher(mid - 175, y1 - 6, 21, dict(view='back', key=1, wet=1.0))
    jhim(mid + 175, y1 - 6, 21, dict(view='back', key=2, guitar=True))
    snow(t * .7, mid, y1 - 400, x1, y1, 10, .8, 50, 21, 2, 5)
    # title lettering
    a = clamp(k)
    text('罗生门', W / 2, 250, 176, '#FFF3E2', face=WK, stroke=INK, strokeW=20, shadow=True, a=a)
    text('Follow', W / 2, 372, 64, '#FFD27A', face=WK, stroke=INK, strokeW=9, shadow=False, a=a)


def hangingUmbrella(x, y, t, present=1.0):
    """his yellow umbrella hanging (closed) on a hook on her wall; present = 0 once she has taken it"""
    boilSeed('hook')
    paint(ellPts(x, y, 8, 8, 10), wash='#8A8F9E', ink=INK, sw=.4)
    if present < .5:
        return
    push()
    translate(x, y)
    rotate(math.sin(t * .8) * .03)
    inkLine([[0, 0], [-14, 18], [0, 34]], 1.0, '#6E4A30', 'ink', .6)
    paint([[-6, 30], [6, 30], [30, 330], [0, 360], [-30, 330]], wash='#F2C14E', fill='#E0A92A', fillOp=80, ink=INK, sw=.7)
    for j in (-1, 1):
        inkLine([[j * 2, 40], [j * 18, 320]], .35, '#C9962C', 'inkfine', 0)
    paint(rectPts(-3, 360, 6, 40), wash='#6E4A30', ink=INK, sw=.4)
    pop()


def umbrellaOpen(x, y, r, tilt=0.0, col='#F2C14E', dk='#C9962C', a=1.0, handle=True):
    """open umbrella; (x, y) = top of the shaft (canopy centre), handle goes down 1.15 r"""
    push()
    translate(x, y)
    rotate(tilt)
    if handle:
        G.c.drawLine(0, 0, 0, r * 1.15, skia.Paint(AntiAlias=True, Color=skcol(INK, a), StrokeWidth=max(3, r * .035)))
        inkLine([[0, r * 1.15], [r * .1, r * 1.25], [r * .2, r * 1.15]], .7, INK, 'ink', .6)
    boilSeed('umbo')
    pts = [[-r, r * .18]]
    for i in range(1, 6):
        q = i / 6
        pts.append([lerp(-r, r, q), r * .18 - r * .1 * math.sin(q * math.pi * 6) ** 2 * 0 + r * .06])
    pts.append([r, r * .18])
    arc = [[math.cos(math.pi + q * math.pi) * r, -math.sin(q * math.pi) * r * .62] for q in [i / 20 for i in range(21)]]
    scal = []
    for i in range(6):
        x0, x1 = lerp(-r, r, i / 6), lerp(-r, r, (i + 1) / 6)
        scal += [[x0, r * .02], [(x0 + x1) / 2, r * .12]]
    scal.append([r, r * .02])
    poly = arc + list(reversed(scal))
    paint(poly, wash=col, washOp=int(255 * a), fill=dk, fillOp=int(60 * a), ink=INK, sw=.8)
    for i in range(1, 6):
        xx = lerp(-r, r, i / 6)
        inkLine([[0, -r * .62], [xx, r * .04]], .45, dk, 'inkfine', .2)
    paint(ellPts(0, -r * .64, r * .05, r * .05, 8), wash=dk, ink=INK, sw=.3)
    pop()


def roomLife(t, who='him', part='wall'):
    """the lived-in layer of the two rooms (user: 「房间都可以多加点细节 太单调 可以多加点烟火气息」); part = 'wall' | 'floor'"""
    her = who == 'her'
    if part == 'floor':
        return roomFloor(t, who)
    # jacket / scarf on a wall hook, top left
    boilSeed('hook' + who)
    G.c.drawCircle(110, 236, 8, skia.Paint(AntiAlias=True, Color=skcol('#8A8F9E')))
    if her:
        paint([[70, 244], [150, 244], [168, 560], [52, 560]], wash='#E8857E', fill='#BC5C57', fillOp=80, ink=INK, sw=.6)
        paint([[96, 244], [124, 244], [134, 640], [86, 640]], wash='#F1E6CF', ink=INK, sw=.5)
    else:
        paint([[66, 244], [154, 244], [174, 580], [46, 580]], wash='#3B5B98', fill='#2A4375', fillOp=80, ink=INK, sw=.6)
        G.c.drawLine(104, 250, 100, 420, skia.Paint(AntiAlias=True, Color=skcol('#DCD6CC'), StrokeWidth=4))
        G.c.drawLine(118, 250, 122, 420, skia.Paint(AntiAlias=True, Color=skcol('#DCD6CC'), StrokeWidth=4))
    # top right: his gig poster / her frosty window onto the block across the street
    if her:
        x0, y0, w, h = 892, 236, 170, 300
        boilSeed('herwin')
        paint(rectPts(x0 - 12, y0 - 12, w + 24, h + 24), wash='#E9E2D2', ink=INK, sw=.7)
        G.c.save()
        G.c.clipRect(skia.Rect.MakeXYWH(x0, y0, w, h))
        gradRect(x0, y0, w, h, ['#1E2444', '#3A4670'])
        paint(rectPts(x0 + 10, y0 + 40, 150, 300), wash='#4A4E6E', ink=None)
        import lsm3 as _l3
        for r in range(4):
            for c in range(2):
                _l3.litWindow(x0 + 24 + c * 70, y0 + 60 + r * 60, 50, 40, ['cook', 'tv', 'family', 'study', 'dark', 'plant', 'tv', 'cook'][r * 2 + c], t, True, r * 2 + c)
        snow(t, x0, y0 - 20, x0 + w, y0 + h, 18, .95, 50, 33, 2.5, 5)
        G.c.restore()
        G.c.drawLine(x0 + w / 2, y0, x0 + w / 2, y0 + h, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=5))
        for k in range(12):
            G.c.drawCircle(x0 + hash1(k) * w, y0 + h - 4 - hash1(k * 3) * 40, 6 + 9 * hash1(k * 5), skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .6)))
        paint(rectPts(x0 - 18, y0 + h + 10, w + 36, 16), wash='#FFFFFF', ink=INK, sw=.5)
    else:
        push()
        translate(976, 470)
        rotate(.04)
        boilSeed('poster')
        paint(rectPts(-84, -150, 168, 300), wash='#2E2A44', fill='#3E3456', fillOp=80, ink=INK, sw=.7)
        G.c.drawCircle(0, -40, 50, skia.Paint(AntiAlias=True, Color=skcol('#E9A23B', .9)))
        inkLine([[-20, 20], [30, -90]], 1.0, '#FFFDF6', 'ink', 0)
        text('小酒馆 LIVE', 0, 60, 26, '#FFFDF6', face=WK, shadow=False)
        text('周五 21:00', 0, 100, 22, '#FFD27A', face=WK, shadow=False)
        G.c.drawCircle(0, -146, 6, skia.Paint(AntiAlias=True, Color=skcol('#E9585E')))
        pop()


def roomFloor(t, who='him'):
    her = who == 'her'
    # floor: a drying rack with socks and a T-shirt; noodle stack / plush; small amp
    boilSeed('rack' + who)
    for lx in (660, 800):
        G.c.drawLine(lx, 1300, lx + (40 if lx == 660 else -40), 1430, skia.Paint(AntiAlias=True, Color=skcol('#BDB6AA'), StrokeWidth=4))
    G.c.drawLine(650, 1300, 810, 1300, skia.Paint(AntiAlias=True, Color=skcol('#BDB6AA'), StrokeWidth=4))
    cols = ['#FFFDF6', '#E9585E', '#5D8FC9'] if not her else ['#F19A92', '#FFFDF6', '#C9A0D0']
    paint(rectPts(668, 1302, 54, 60), wash=cols[0], ink=INK, sw=.4)
    paint(rectPts(732, 1302, 18, 34), wash=cols[1], ink=INK, sw=.3)
    paint(rectPts(760, 1302, 18, 34), wash=cols[2], ink=INK, sw=.3)
    if her:
        paint(ellPts(886, 1118, 34, 30, 16), wash='#C9A27A', ink=INK, sw=.5)              # plush bear on the radiator
        paint(ellPts(886, 1080, 24, 22, 14), wash='#C9A27A', ink=INK, sw=.5)
        for d in (-1, 1):
            G.c.drawCircle(886 + d * 18, 1062, 8, skia.Paint(AntiAlias=True, Color=skcol('#C9A27A')))
        paint(rectPts(866, 1094, 40, 8), wash='#CC3B42', ink=None)
    else:
        for k in range(4):
            paint([[100, 1288 - k * 26], [150, 1288 - k * 26], [146, 1264 - k * 26], [104, 1264 - k * 26]], wash='#FFFDF6', ink=INK, sw=.4)
            paint([[102, 1278 - k * 26], [148, 1278 - k * 26], [147, 1272 - k * 26], [103, 1272 - k * 26]], wash='#E9585E', ink=None)
        paint(rrPts(930, 1300, 110, 90, 8), wash='#2E2A38', ink=INK, sw=.6)               # little amp under the guitar
        G.c.drawCircle(985, 1345, 28, skia.Paint(AntiAlias=True, Color=skcol('#4A4458')))
        text('AMP', 985, 1312, 16, '#E9C84A', face=WK, shadow=False)


def deskItemsHer(t):
    boilSeed('booksH')
    for i, (bw, col) in enumerate(((160, '#C9A0D0'), (150, '#7FB08A'), (166, '#F2C14E'), (140, '#5D8FC9'))):
        paint(rrPts(280 - bw / 2, 1188 - 24 * (i + 1), bw, 22, 4), wash=col, ink=INK, sw=.5)
        G.c.drawRect(skia.Rect.MakeXYWH(280 + bw / 2 - 14, 1188 - 24 * (i + 1) - 6, 8, 10), skia.Paint(AntiAlias=True, Color=skcol(['#E9585E', '#FFD27A', '#5D8FC9', '#7FB08A'][i])))
    paint(rrPts(640, 1140, 70, 50, 8), wash='#FFFDF6', ink=INK, sw=.5)                      # tea mug with steam
    paint(ellPts(712, 1162, 14, 12, 10), wash=None, ink=INK, sw=.5)
    import lsm3 as _l3
    _l3.steam(t, 675, 1130, 3, .5, .7, 110, 4)
    paint(ellPts(770, 1150, 40, 40, 20), wash='#DCEBF7', washOp=200, ink=INK, sw=.6)         # snow globe
    paint(rrPts(736, 1176, 68, 16, 4), wash='#8A5A3C', ink=INK, sw=.4)
    paint(ellPts(770, 1160, 14, 12, 10), wash='#FFFFFF', ink=None)
    for k in range(6):
        G.c.drawCircle(752 + hash1(k) * 36, 1130 + hash1(k * 3) * 30, 2.5, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF')))
    paint(rrPts(560, 1166, 60, 22, 4), wash='#F3D9E0', ink=INK, sw=.4)                       # hand warmer
