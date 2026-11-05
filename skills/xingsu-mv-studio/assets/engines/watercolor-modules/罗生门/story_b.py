# story_b.py: 《罗生门》 S08–S26 — chorus 1 (memories, the weather ritual) and verse 1 (his version of night 312: the deleted message,
# the unread screen, the map, the 11 unused tickets, the 12th ticket, the train north, rain turning into snow, arrival).
import math
from eng import *
import eng
from hl import tint, desat, vignette
from couple import jhim, jher, HIM, HER
from lsm import *
from lsm2 import *
from lsm3 import *
from story_a import inPhone, grade, NOW312, PH
from common import B, LY, cam, es, kt, pk


def L(i, j=0):
    return LY[i][3][j] if j else LY[i][0]


def t0of(t, lt):
    return t - lt


def stepSeat(x, y_seat, w, floor_y, col='#9A8F80'):
    boilSeed(f'step{x}')
    paint(rectPts(x - w / 2, y_seat, w, floor_y - y_seat), wash=col, fill=mixCol(col, INK, .25), fillOp=90, ink=INK, sw=.7)


def phoneInHand(x, y, s=1.0, lit=True, rot=0.0):
    phoneObj(x, y, 40 * s, rot, glowK=.6 if lit else 0.0)


def inset(x, y, r, draw, a=1.0):
    """round magnified inset (phone close-up) with an ink ring and a little tail"""
    if a <= .01:
        return
    G.c.saveLayerAlpha(None, int(255 * clamp(a)))
    G.c.drawCircle(x + 8, y + 10, r, skia.Paint(AntiAlias=True, Color=skcol('#000000', .3)))
    G.c.save()
    p = skia.Path()
    p.addCircle(x, y, r)
    G.c.clipPath(p, skia.ClipOp.kIntersect, True)
    draw(x, y, r)
    G.c.restore()
    boilSeed(f'inset{x}')
    paint(ellPts(x, y, r, r, 40), wash=None, ink=INK, sw=1.2)
    G.c.restore()


def miniScreen(x, y, r, lines, bg='#DCE8F6', big=None, dark=False):
    if dark:
        # a dead phone: grey screen, empty red battery, 「已关机」 (never a plain black disc)
        G.c.drawRect(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), skia.Paint(AntiAlias=True, Color=skcol('#C9CCD6')))
        G.c.drawRoundRect(skia.Rect.MakeXYWH(x - r * .42, y - r * .42, r * .76, r * .4), 8, 8,
                          skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=6, Color=skcol('#E9585E')))
        G.c.drawRect(skia.Rect.MakeXYWH(x + r * .36, y - r * .3, r * .08, r * .16), skia.Paint(AntiAlias=True, Color=skcol('#E9585E')))
        G.c.drawRect(skia.Rect.MakeXYWH(x - r * .36, y - r * .36, r * .07, r * .28), skia.Paint(AntiAlias=True, Color=skcol('#E9585E')))
        text('电量耗尽 已关机', x, y + r * .28, r * .16, '#4A4458', face=WK, shadow=False)
        return
    G.c.drawRect(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), skia.Paint(AntiAlias=True, Color=skcol(bg)))
    if big:
        text(big, x, y - r * .25, r * .42, '#1F2233', face=WK, shadow=False)
    for j, (s, col) in enumerate(lines):
        text(s, x, y + r * (.12 + j * .26), r * .17, col, face=WK, shadow=False)


# ================================================================ S08 chorus 1: memory — one umbrella, always tilted to her side
def umbrellaPair(t, gx, gy, u, walking, ph, tiltHer=.22, front=False, wetHim=.8, exHim=None, exHer=None):
    if not front:
        jher(gx + 7.5 * u, gy, u, dict(view='side', legs='walk' if walking else 'stand', ph=ph + .5, ex=exHer or dict(mouth='smile'), key=11))
        o = dict(view='side', legs='walk' if walking else 'stand', ph=ph, hands=dict(R=[1.9, -10.6]), wet=wetHim, ex=exHim or dict(mouth='smile', lookX=.5), key=12)
        jhim(gx, gy, u, o)
        hx, hy = gx + 1.9 * u, gy + (-10.6 + (-abs(math.sin(ph * TAU)) * .22 if walking else 0)) * u
        umbrellaOpen(hx + 3.2 * u, hy - 9.6 * u, 8.4 * u, tiltHer)
        G.c.drawLine(hx, hy, hx + 3.2 * u, hy - 9.6 * u, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=max(3, u * .3)))
        paint(ellPts(hx, hy, .62 * u, .58 * u, 12), wash=HIM['skin'], ink=INK, sw=.5)
    else:
        jher(gx + 5.6 * u, gy, u, dict(ex=exHer or dict(eyes='happy', mouth='smile', blush=.8), key=11))
        jhim(gx - 5.6 * u, gy, u, dict(hands=dict(R=[2.6, -11.2]), wet=wetHim, ex=exHim or dict(mouth='smile', blush=.6), key=12))
        hx, hy = gx - 5.6 * u + 2.6 * u, gy - 11.2 * u
        umbrellaOpen(hx + 2.4 * u, hy - 9.2 * u, 10.5 * u, tiltHer)
        G.c.drawLine(hx, hy, hx + 2.4 * u, hy - 9.2 * u, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=max(3, u * .3)))
        paint(ellPts(hx, hy, .62 * u, .58 * u, 12), wash=HIM['skin'], ink=INK, sw=.5)


def s08(t, lt, dur):
    t0 = t0of(t, lt)
    stop = L(5) - .05
    cam(t, W / 2, 860, lerp(1.0, 1.06, es(t, t0, t0 + dur)))
    rainStreet(t)
    if t < stop:
        gx = lerp(230, 420, seg(t, t0, stop))
        umbrellaPair(t, gx, 1290, 24, True, t * 1.0)
    else:
        umbrellaPair(t, 470, 1290, 24, False, 0, front=True, tiltHer=.3)
    rain(t, -60, -100, W + 60, H + 80, 150, .5, .15, 1600, 7)
    camEnd()
    grade('past')


# ================================================================ S09 chorus 1: day 1 → 311, the board and the nightly 23:00
SEASONS = [('大雪', '-12℃', 'snow'), ('晴', '15℃', 'sun'), ('小雨', '18℃', 'rain'), ('大雪', '-8℃', 'snow')]


def s09(t, lt, dur):
    t0 = t0of(t, lt)
    k = es(t, t0 + 1.4, t0 + dur - .6)
    day = int(lerp(1, 311, k))
    si = min(3, int(k * 4))
    hv, ht, hi = SEASONS[si]
    cam(t, 545, 600, lerp(1.22, 1.3, es(t, t0, t0 + dur)))
    hisRoom(t, her=hv, herT=ht)
    camEnd()
    # the day counter tag on the board's corner (screen space, follows the camera roughly)
    push()
    translate(820, 300)
    rotate(.08)
    paint(rrPts(-110, -50, 220, 100, 10), wash='#FFFDF6', ink=INK, sw=.6)
    text(f'第{day}天', 0, 0, 50, '#E9585E', face=WK, shadow=False)
    pop()
    wr = 1 if t < t0 + 1.4 else 0
    jhim(600, 1930, 40, dict(view='back', key=13, hands=dict(R=[4.2, -14.0 + .4 * math.sin(t * 9) * wr], L=[-3.4, -6.0])))
    grade('night')


# ================================================================ S10 chorus 1: split — she sends her snow sky, he sends his rain
def splitV(t, top, bot, line=True, lab=None):
    for half, fn in ((0, top), (1, bot)):
        G.c.save()
        G.c.clipRect(skia.Rect.MakeXYWH(-10, half * H / 2, W + 20, H / 2))
        push()
        translate(0, -H / 4 if half == 0 else H / 4)
        fn()
        pop()
        G.c.restore()
    if line:
        flatRect(-10, H / 2 - 5, W + 20, 10, '#FFFDF6', 1.0)
        G.c.drawLine(-10, H / 2 - 5, W + 10, H / 2 - 5, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=3))
        G.c.drawLine(-10, H / 2 + 5, W + 10, H / 2 + 5, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=3))


def s10(t, lt, dur):
    t0 = t0of(t, lt)
    def top():
        cam(t, W / 2, 980, 1.0)
        cityWide(t, 'north', 'night')
        jher(470, 1250, 22, dict(beanie=True, hands=dict(R=[2.6, -15.5]), ex=dict(mouth='smile', lookY=-.8, blush=.7), key=14,
                                itemR=lambda u, sw, C: phoneObj(0, -1.2 * u, 1.9 * u, 0, glowK=.5)))
        breath(t, 560, 940, .7)
        camEnd()
        text('她那 · 北方 23:00', 60, 640, 40, '#FFFDF6', face=WK, align='left', stroke=INK, strokeW=6, shadow=False)
    def bot():
        cam(t, 470, 1000, 1.25)
        hisRoom(t)
        u = 26
        chairBack(470, 1330 - 2.9 * u, u)
        jhim(470, 1330, u, dict(legs='sit', hands=dict(L=[-1.15, -7.7], R=[1.15, -7.7]), ex=dict(lookY=.7, mouth='smile', blush=.6), key=15))
        deskTop(t)
        deskItems(t)
        phoneObj(470, 1140, 66, 0.0, glowK=1.0)
        camEnd()
        grade('night', .8)
        text('我这 · 南方 23:00', 60, 1080, 40, '#FFFDF6', face=WK, align='left', stroke=INK, strokeW=6, shadow=False)
    splitV(t, top, bot)
    # her photo flies down across the split; his "rain" bubble flies up
    for (ta, kind, x0, y0, x1, y1) in ((t0 + 1.0, 'snowman', 600, 380, 700, 1150), (t0 + 3.4, None, 700, 1150, 620, 420)):
        k = seg(t, ta, ta + 1.4)
        if 0 < k < 1:
            x, y = lerp(x0, x1, ease(k)), lerp(y0, y1, ease(k)) - math.sin(k * math.pi) * 80
            if kind:
                push()
                translate(x, y)
                rotate(.1)
                polaroid(0, 0, 150, 0, miniSnowman, 'fly1')
                pop()
            else:
                push()
                translate(x - 200, y - 40)
                bubble(400, 0, '我这下雨 想你', True, THEMES['now'])
                pop()


# ================================================================ S11 verse 1: night 312, 02:10 — head on the desk
def deskClose(t, cx=470, cy=1010, z=1.55, phoneLit=0.0, ex=None, head=False, notif=0.0, standing=0.0, guitar=False):
    cam(t, cx, cy, z)
    hisRoom(t, her='暴雪' if standing > 0 else '大雪', herT='-18℃' if standing > 0 else '-12℃', storm=1.0 if standing > 0 else 0.0)
    u = 26
    chairBack(470, 1330 - 2.9 * u, u)
    if standing > 0:
        jhim(560, 1330, u, dict(guitar=guitar, ex=ex or dict(brows='knit', mouth='flat'), key=16))
    else:
        o = dict(legs='sit', hands=dict(L=[-3.2, -7.0], R=[3.2, -7.0]), ex=ex or {}, key=16)
        if head:
            o.update(rot=.0, bob=1.3, ex=dict(eyes='closed', mouth='flat'))
        jhim(470, 1330, u, o)
    deskTop(t)
    deskItems(t)
    # the phone lying on the desk
    boilSeed('flatphone')
    if phoneLit > .01:
        glow(560, 1182, 120, '#BFE3FF', .6 * phoneLit)
    paint([[500, 1192], [620, 1192], [632, 1180], [512, 1180]], wash='#BFE3FF' if phoneLit > .3 else '#22212C', ink=INK, sw=.5)
    if notif > .01:
        a = clamp(notif * 4) * (1 - seg(notif, .8, 1))
        push()
        translate(600, 1080 - 30 * easeOut(clamp(notif * 3)))
        G.c.saveLayerAlpha(None, int(255 * a))
        G.c.drawRoundRect(skia.Rect.MakeXYWH(-190, -46, 380, 92), 20, 20, skia.Paint(AntiAlias=True, Color=skcol('#F4F2F8', .95)))
        text('天气提醒：明天小雨', 0, 0, 34, '#1F2233', face=WK, shadow=False)
        G.c.restore()
        pop()
    camEnd()
    grade('night')


def s11(t, lt, dur):
    deskClose(t, 470, 1190, lerp(1.45, 1.5, es(t, t - lt, t - lt + dur)), head=True)


# ================================================================ S12 verse 1: types a long message, deletes it, sends 「不回就算了」, withdraws it
BASE312 = [('sep', '11月20日 23:00 · 第312天'), ('me', '示例歌词占位文字？'), ('status', '未读'), ('sep', '00:41'), ('me', '睡了吗'),
           ('status', '未读'), ('sep', '01:52'), ('me', '那 晚安'), ('status', '未读')]
LONG = '你是不是不想理我了 我知道异地很累 可我真的很想你'


def s12(t, lt, dur):
    t0 = t0of(t, lt)
    tA, tB, tC, tSend, tW = t0 + .1, t0 + 1.4, t0 + 1.9, t0 + 2.45, L(11, 7) - .05
    if t < tB:
        typed = LONG[:int(len(LONG) * seg(t, tA, tB))]
    elif t < tC:
        typed = LONG[:int(len(LONG) * (1 - seg(t, tB, tC)))]
    elif t < tSend:
        typed = '不回就算了'[:int(5 * seg(t, tC, tSend - .15)) + 0]
    else:
        typed = ''
    sent = ('不回就算了',) if t >= tSend else ()
    def draw():
        typingScreen(t, typed, sent=sent, withdrawn=t >= tW, clock='02:16', base=BASE312)
    inPhone(draw, 'room', t, tilt=-.01)
    vignette(.3, '#0E1128')


# ================================================================ S13 verse 1: stares at the phone; it lights — only a weather reminder
def s13(t, lt, dur):
    t0 = t0of(t, lt)
    tn = t0 + 1.2
    lit = es(t, tn - .05, tn + .1) * (1 - es(t, tn + 2.2, tn + 2.6))
    hope = t >= tn and t < tn + .9
    ex = dict(eyes='wide' if hope else 'half', mouth='o' if hope else 'flat', brows='up' if hope else 'sad', lookY=.8)
    if t >= tn + .9:
        ex = dict(eyes='half', mouth='sad', brows='sad', lookY=.8)
    deskClose(t, 500, 1190, 1.55, phoneLit=lit, ex=ex, notif=seg(t, tn, tn + 2.6))


# ================================================================ S14 verse 1: the map — 2875 km
def s14(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, W / 2, H / 2, lerp(1.0, 1.08, es(t, t0, t0 + dur)))
    mapWall(t, seg(t, t0 + .3, t0 + 2.6))
    polaroid(260, 420, 150, -.12, miniCouple, 'mp1')                          # photos and notes taped onto the map
    polaroid(860, 1120, 140, .1, miniSnowman, 'mp2', '#3B5B98')
    for (nx, ny, nr, s_, col) in ((850, 300, .08, '她的学校', '#FFE58A'), (230, 1210, -.06, '第一次见面', '#BFE3C8'), (800, 640, .05, '等我', '#FFC9C2')):
        push()
        translate(nx, ny)
        rotate(nr)
        paint(rectPts(-80, -34, 160, 68), wash=col, ink=INK, sw=.4)
        text(s_, 0, 0, 28, INK, face=WK, shadow=False)
        pop()
    G.c.drawCircle(760, 1000, 46, skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=8, Color=skcol('#8A5A3C', .35)))   # coffee ring
    camEnd()
    grade('night', .7)


# ================================================================ S15 verse 1: scrolled back to day 240 — 「示例歌词占位文字」
D240 = [('sep', '第240天 · 23:00'), ('me', '示例歌词占位文字？'), ('her', '示例歌词占位文字'), ('me', '……'), ('her', '算了 晚安')]


def s15(t, lt, dur):
    t0 = t0of(t, lt)
    def draw():
        chatScreen(t, D240, 'old', '02:30', scroll=-120 * (1 - es(t, t0, t0 + .6)))
        k = es(t, t0 + .8, t0 + 1.2)
        glow(400, 1000, 260, '#FFB2A6', .4 * k)
        tint('#FFE2B0', .10, skia.BlendMode.kMultiply)
    inPhone(draw, 'room', t, tilt=.01)
    vignette(.3, '#0E1128')


# ================================================================ S16 verse 1: the drawer — 11 tickets, never used
def s16(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, W / 2, 900, lerp(1.0, 1.06, es(t, t0, t0 + dur)))
    deskDrawer(t, 11, es(t, t0 + .2, t0 + 1.0))
    dy = 260 * ease(es(t, t0 + .2, t0 + 1.0))
    boilSeed('drawerextra')
    paint(rrPts(170, 940 + dy, 120, 80, 10), wash='#B0403E', ink=INK, sw=.5)              # pick tin
    paint(heartPts(230, 980 + dy, 16), wash='#E84A5F', ink=INK, sw=.3)
    paint(rectPts(800, 900 + dy, 110, 140), wash='#3F6A8A', ink=INK, sw=.5)               # little notebook
    text('歌词本', 855, 970 + dy, 24, '#FFFDF6', face=WK, shadow=False)
    G.c.drawOval(skia.Rect.MakeXYWH(640, 1000 + dy, 60, 30), skia.Paint(AntiAlias=True, Style=skia.Paint.kStroke_Style, StrokeWidth=4, Color=skcol('#E9A23B')))
    camEnd()
    grade('night', .7)


# ================================================================ S17 verse 1: out in the rain, looking up — her sky must be clear tonight
def s17(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, W / 2, lerp(860, 760, es(t, t0, t0 + dur)), 1.0)
    rainStreet(t, lampK=.8)
    jhim(470, 1290, 28, dict(view='back', wet=1.0, key=17))
    rain(t, -60, -200, W + 60, H + 80, 190, .6, .14, 1700, 9)
    camEnd()
    grade('night')
    inset(790, 360, 160, lambda x, y, r: (miniSnowStreet(x - r, y - r, 2 * r), snow(t, x - r, y - r, x + r, y + r, 20, .9, 40, 3, 2, 5)),
          a=es(t, t0 + 1.0, t0 + 1.5))


# ================================================================ S18 verse 1: he can't sit still — stands, slings the guitar
def s18(t, lt, dur):
    t0 = t0of(t, lt)
    up = t > t0 + 1.0
    deskClose(t, 540, 880, 1.0, ex=dict(brows='knit', mouth='flat') if up else dict(eyes='half', mouth='flat', lookY=.6),
              standing=1.0 if up else 0.0, guitar=t > t0 + 2.1)


# ================================================================ S19 verse 1: the booking app — 第 12 张
def s19(t, lt, dur):
    t0 = t0of(t, lt)
    tap = L(26, 4)
    def draw():
        bookingScreen(t, seg(t, tap - .1, tap + .2), seg(t, L(27) - .05, L(27) + .6))
    inPhone(draw, 'room', t, tilt=-.012)
    vignette(.3, '#0E1128')


# ================================================================ S20 verse 1: on the train north at 05:40 — her sad face in the window
def trainHim(t, outside='rain', mix=0.0, ex=None, refl=None, night=True, clock=None, speed=0.0, guitarBeside=True, others=None):
    cam(t, W / 2, 890, 1.0)
    if others is None:
        others = [('left', lambda x, y, u: passengerUncle(t, x, y, u))]
    def main():
        u = 26
        if guitarBeside:
            push()
            translate(1000, 1110)
            rotate(.1)
            boilSeed('gcase2')
            body = [[-40, -260], [40, -260], [50, -120], [80, -60], [84, 120], [40, 180], [-40, 180], [-84, 120], [-80, -60], [-50, -120]]
            paint(throughClosed(body, 3), wash=HIM['case'], fill=HIM['caseDk'], fillOp=80, ink=INK, sw=.8)
            pop()
        jhim(800, 1300, u, dict(legs='sit', hands=dict(L=[-2.6, -7.4], R=[2.6, -7.4]), ex=ex or dict(lookX=-.9, mouth='flat'), key=20))
    trainBooth(t, outside, mix, night, 'right', others, refl, clock, speed, main=main)
    camEnd()


def s20(t, lt, dur):
    t0 = t0of(t, lt)
    def refl():
        jher(540, 1000, 30, dict(ex=dict(eyes='teary', mouth='sad', brows='sad', tears=.8), key=21, shadow=False, blink=False))
    trainHim(t, 'rain', 0.0, ex=dict(lookX=-.9, mouth='sad', brows='sad', eyes='teary'), refl=refl if t > t0 + .8 else None)
    grade('night', .8)


# ================================================================ S21 verse 1: if only that moment could stop — the memory, frozen
def s21(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, W / 2, 860, 1.02)
    rainStreet(t0 + .01, frozen=True)
    umbrellaPair(t0 + .3, 470, 1290, 24, False, 0, front=True, tiltHer=.3)
    camEnd()
    grade('past', 1.0)
    desat(.25)
    # polaroid frame around everything
    k = es(t, t0, t0 + .35)
    sh = 1 - k
    G.c.save()
    pth = skia.Path()
    pth.setFillType(skia.PathFillType.kEvenOdd)
    pth.addRect(skia.Rect.MakeXYWH(-50, -50, W + 100, H + 100))
    pth.addRect(skia.Rect.MakeXYWH(70, 230, W - 140, 900))
    G.c.drawPath(pth, skia.Paint(AntiAlias=True, Color=skcol('#FFFDF6', .97 * k)))
    G.c.restore()
    text('去年秋天 · 一把伞', W / 2, 1192, 50, INK, face=WK, shadow=False, a=k)
    flash(.6 * (1 - seg(t, t0, t0 + .25)))


# ================================================================ S22 verse 1: an old couple asleep across the aisle; the clock runs fast
def s22(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, W / 2, 890, 1.0)
    def old(x, y, u):
        jhim(120, y, 24, dict(C=OLDHIM, legs='sit', rot=.05, hands=dict(L=[-2.8, -6.6], R=[2.0, -6.8]), ex=dict(eyes='closed', mouth='smile', blush=.4), key=23))
        jher(392, y, 24, dict(C=OLDHER, legs='sit', rot=-.09, hands=dict(L=[-1.8, -6.6], R=[1.6, -6.6]), ex=dict(eyes='closed', mouth='small', blush=.5), key=22))
        boilSeed('oldblanket')
        paint([[60, y - 120], [470, y - 130], [480, y - 40], [50, y - 30]], wash='#C9A0A0', fill='#A87878', fillOp=70, ink=INK, sw=.6)
    def main():
        jhim(800, 1300, 26, dict(legs='sit', hands=dict(L=[-2.6, -7.4], R=[2.6, -7.4]), ex=dict(lookX=-.9, mouth='smile', brows='sad', eyes='teary'), key=24))
    trainBooth(t, 'rain', .15, True, 'right', [('left', old)], None, 330, 420, main=main)
    camEnd()
    grade('night', .6)
    tint('#FFE2B8', .08, skia.BlendMode.kScreen)


# ================================================================ S23 verse 1: the notes app — 「她的脾气」
TEMPER = ['1. 生气的时候说「随便」', '2. 怕冷 手总是冰的', '3. 爱吃糖炒栗子', '4. 下雨天会想家', '5. 说「没事」就是有事',
          '6. 吵完架 先哭的是她', '7. 其实最心软']


def s23(t, lt, dur):
    t0 = t0of(t, lt)
    def draw():
        notesScreen(t, TEMPER, seg(t, t0 + .2, t0 + dur - .3))
    inPhone(draw, 'room', t, tilt=.01)
    vignette(.3, '#0E1128')


# ================================================================ S24 verse 1: but we still fight — old quarrels flash
FIGHTS = [
    [('sep', '第88天'), ('her', '随便'), ('me', '你又这样'), ('her', '示例歌词占')],
    [('sep', '第163天'), ('me', '我不懂？'), ('her', '好'), ('status', '已读')],
    [('sep', '第240天'), ('her', '我们是不是太远了'), ('me', '……')],
]


def s24(t, lt, dur):
    t0 = t0of(t, lt)
    i = min(2, int((t - t0) / (dur / 3)))
    def draw():
        chatScreen(t, FIGHTS[i], 'old', '23:00')
        tint('#FFB0A0', .14, skia.BlendMode.kMultiply)
    sh = math.sin(t * 50) * 6 * (1 - seg(frac((t - t0) / (dur / 3)), 0, .12))
    push()
    translate(sh, 0)
    inPhone(draw, 'room', t, tilt=-.015)
    pop()
    vignette(.36, '#1A0E10')


# ================================================================ S25 verse 1: on the bridge, the rain slowly turns into snow
def s25(t, lt, dur):
    t0 = t0of(t, lt)
    m = es(t, t0 + .4, t0 + dur - .3)
    cam(t, W / 2, 880, 1.0)
    trainOutside(t, m, night=False, x=lerp(300, -900, seg(t, t0, t0 + dur)), dawn=.6)
    camEnd()


# ================================================================ S26 verse 1: 07:40, the north station; breath and snow
def s26(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, W / 2, 870, lerp(1.0, 1.05, es(t, t0, t0 + dur)))
    stationNorth(t, 0.0)
    shiver = math.sin(t * 30) * .08
    jhim(560, 1238, 30, dict(guitar=True, dx=shiver, ex=dict(eyes='wide', mouth='o', brows='up', blush=.9), key=26,
                              hands=dict(L=[-1.4, -7.6], R=[1.4, -7.6])))
    breath(t, 610, 840, .8, 1.3)
    camEnd()
    grade('night', .4)
