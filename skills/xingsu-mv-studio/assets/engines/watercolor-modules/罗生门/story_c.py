# story_c.py: 《罗生门》 S27–S53 — chorus 2 (he reaches her door: nobody), bridge (waiting, the guitar, the note), verse 2 (her version:
# the umbrella, the dead phone, the Rashomon split, two trains passing, the voice message), chorus 3 (he turns around; the umbrella
# tilts to him; her red scarf), outro (one weather for both).
import math
from eng import *
import eng
from hl import tint, desat, vignette
from couple import jhim, jher, HIM, HER
from lsm import *
from lsm2 import *
from lsm3 import *
from story_a import inPhone, grade, PH
from story_b import stepSeat, phoneInHand, inset, miniScreen, splitV, umbrellaPair, trainHim, L, t0of
from common import B, LY, cam, es, kt, pk

def knockX(t, knocks):
    """hand x (units, side view) for knocking: rests pulled back at 2.9, jabs out to 3.6 (touching the door) on each knock"""
    d = min((t - kk for kk in knocks), key=abs)
    if abs(d) < .14:
        return 3.9 - .6 * (abs(d) / .14)
    return 3.3


def knockFX(t, knocks, x, y):
    for kk in knocks:
        k = seg(t, kk - .02, kk + .35)
        if 0 < k < 1:
            for j in (-1, 0, 1):
                an = j * .5
                G.c.drawLine(x + 14 + math.cos(an) * 20, y + math.sin(an) * 20, x + 14 + math.cos(an) * (34 + 30 * k), y + math.sin(an) * (34 + 30 * k),
                             skia.Paint(AntiAlias=True, Color=skcol(INK, 1 - k), StrokeWidth=5, StrokeCap=skia.Paint.kRound_Cap))
            text('咚', x + 90, y - 70 - 40 * k, 60, INK, face=WK, stroke='#FFFDF6', strokeW=8, shadow=False, a=1 - k, sc=backOut(clamp(k * 4)))


def noteOnDoor(t, k, txt=('示例歌词占位文字？', '我在门口。')):
    """the yellow note pressed onto her door at hand height (settles with a little rotation as it sticks)"""
    if k <= .01:
        return
    push()
    translate(690, 1000)
    rotate(-.05 + .15 * (1 - easeOut(clamp(k))))
    paint(rectPts(-150, -78, 300, 156), wash='#FFE58A', ink=INK, sw=.5)
    text(txt[0], -130, -22, 34, INK, face=WK, align='left', shadow=False)
    text(txt[1], -130, 32, 34, INK, face=WK, align='left', shadow=False)
    G.c.drawRect(skia.Rect.MakeXYWH(-40, -90, 80, 22), skia.Paint(AntiAlias=True, Color=skcol('#F3F0E6', .8)))
    pop()


def thermos(x, y):
    boilSeed('thermos')
    paint(rrPts(x - 22, y - 110, 44, 110, 10), wash='#D9393E', ink=INK, sw=.6)
    for k in range(3):
        G.c.drawCircle(x - 6 + k * 6, y - 70 + k * 16, 5, skia.Paint(AntiAlias=True, Color=skcol('#FFFDF6')))
    paint(rrPts(x - 26, y - 128, 52, 22, 6), wash='#5A5E6E', ink=INK, sw=.5)
    steam(G.T, x, y - 130, 2, .5, .6, 90, 9)
    paint(rectPts(x + 30, y - 60, 70, 50), wash='#FFE58A', ink=INK, sw=.4)
    text('—301', x + 65, y - 35, 20, INK, face=WK, shadow=False)


SEAT_Y = 1300        # door scenes: ground for a sitting figure (feet on the step below), camera cy 890 keeps feet above the lyric bar


def caseFront(x, y, u, rot=0.0):
    """his guitar case held upright in front of his knees (sitting)"""
    push()
    translate(x, y)
    rotate(rot)
    boilSeed('casef')
    body = [[-1.6, -9.0], [1.6, -9.0], [1.9, -5.4], [3.0, -3.6], [3.1, .4], [1.9, 1.6], [-1.9, 1.6], [-3.1, .4], [-3.0, -3.6], [-1.9, -5.4]]
    paint(throughClosed([[a * u, b * u] for a, b in body], 3), wash=HIM['case'], fill=HIM['caseDk'], fillOp=80, ink=INK, sw=.8)
    inkLine([[-2.6 * u, -1.6 * u], [2.6 * u, -1.6 * u]], .4, HIM['caseLt'], 'inkfine', 0)
    pop()


def guitarLap(x, y, u, strum=0.0):
    """acoustic guitar across the lap of a sitting figure (body to his left, neck up to his right)"""
    push()
    translate(x, y)
    rotate(-.45)
    boilSeed('glap')
    bodyP = [[-.2, -2.6], [1.4, -2.2], [1.9, -1.0], [1.3, -.2], [2.1, .9], [1.8, 2.4], [0, 3.0], [-1.8, 2.4], [-2.1, .9], [-1.3, -.2], [-1.9, -1.0], [-1.4, -2.2]]
    paint(throughClosed([[a * u, b * u] for a, b in bodyP], 3), wash='#C98A4E', fill='#A86A36', fillOp=110, ink=INK, sw=.8)
    paint(ellPts(0, .2 * u, .65 * u, .65 * u, 16), wash='#3A2A22', ink=INK, sw=.4)
    paint(rectPts(-.32 * u, -8.6 * u, .64 * u, 6.2 * u), wash='#6E4A30', ink=INK, sw=.5)
    paint(rrPts(-.55 * u, -9.8 * u, 1.1 * u, 1.4 * u, 6), wash='#4A3226', ink=INK, sw=.5)
    for i in range(3):
        G.c.drawLine((-.15 + i * .15) * u, -9.0 * u, (-.15 + i * .15) * u + strum, 2.0 * u, skia.Paint(AntiAlias=True, Color=skcol('#EDE6D6', .7), StrokeWidth=1.2))
    pop()


def sitAtDoor(t, x, u, ex, case=False, guitar=False, strum=0.0, snowOn=0.0, rot=0.0, key=30, phone=False, blow=False, caseSide=False, blanket=0.0):
    seat = SEAT_Y - 2.9 * u
    stepSeat(x, seat, 15 * u, SEAT_Y + 40)
    hands = dict(L=[-2.4, -6.4], R=[2.4, -6.4])
    mid = None
    if guitar:
        hands = GUITAR_HANDS(t)
        mid = guitarMid(t)
    if phone:
        hands = dict(L=[-1.1, -7.4], R=[1.1, -7.4])
    if blow:
        hands = dict(L=[-.75, -11.3], R=[.75, -11.3])
    jhim(x, SEAT_Y, u, dict(legs='sit', hands=hands, ex=ex, key=key, rot=rot, mid=mid))
    if blow:
        breath(t, x + 30, SEAT_Y - 11.0 * u, .7, .8)
    if snowOn > .01:
        for (sx, sy) in ((-3.0, -10.7), (2.8, -10.6), (0, -18.0)):
            paint(ellPts(x + sx * u, SEAT_Y + (sy + 1.5) * u, 1.6 * u, .55 * u, 12), wash='#FFFFFF', washOp=int(240 * snowOn), ink=None)
    if blanket > .01:
        # a plaid blanket draped over his shoulders (narrow at the neck, falling past the knees), the head stays clear
        boilSeed('blanket')
        G.c.saveLayerAlpha(None, int(255 * clamp(blanket)))
        bx, by = x, SEAT_Y + 1.5 * u
        U = lambda pts: [[bx + a * u, by + b * u] for a, b in pts]
        shape = U([[-2.2, -10.7], [2.2, -10.7], [4.6, -9.9], [5.6, -7.6], [6.0, -3.6], [5.0, -1.9], [1.5, -2.3], [-1.6, -2.0], [-5.0, -1.9], [-6.0, -3.6], [-5.6, -7.6], [-4.6, -9.9]])
        paint(throughClosed(shape, 3), wash='#C94A4A', fill='#A83A3A', fillOp=70, ink=INK, sw=.7)
        G.c.save()
        G.c.clipPath(skia.Path().addPoly([skia.Point(float(a), float(b)) for a, b in shape], True), skia.ClipOp.kIntersect, True)
        for k in range(-4, 5):
            G.c.drawLine(bx + k * 1.6 * u, by - 11 * u, bx + k * 1.6 * u + .6 * u, by - 1.5 * u, skia.Paint(AntiAlias=True, Color=skcol('#F3E3C8', .45), StrokeWidth=5))
        for k in range(6):
            G.c.drawLine(bx - 7 * u, by - 9.5 * u + k * 1.4 * u, bx + 7 * u, by - 9.5 * u + k * 1.4 * u, skia.Paint(AntiAlias=True, Color=skcol('#7A2A2A', .35), StrokeWidth=6))
        G.c.restore()
        inkLine(U([[-.4, -10.6], [.6, -6.0], [.2, -2.2]]), .5, '#7A2A2A', 'inkfine', .4)      # the overlap fold down the front
        for k in range(9):
            fx = bx + (-4.6 + k * 1.15) * u
            G.c.drawLine(fx, by - 1.95 * u, fx, by - 1.4 * u, skia.Paint(AntiAlias=True, Color=skcol('#F3E3C8', .9), StrokeWidth=3))
        G.c.restore()
    if case:
        caseFront(x, SEAT_Y - 1.0 * u, u * .9, .04)
    if caseSide:
        caseFront(x + 7.4 * u, SEAT_Y + .6 * u, u * .95, .1)
    if phone:
        phoneObj(x, SEAT_Y - 6.4 * u, 1.9 * u, 0, glowK=.5)


# ================================================================ S27 chorus 2: running through her snowy city
def s27(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, W / 2, 860, 1.0)
    cityWide(t, 'north', 'dawn')
    x = lerp(120, 880, seg(t, t0, t0 + dur))
    for i in range(14):                                       # footprints behind him
        fx = x - 60 - i * 54
        if fx > -40:
            paint(ellPts(fx, 1236 + (8 if i % 2 else -8), 12, 6, 10), wash='#B8C4DA', ink=None)
    jhim(x, 1236, 24, dict(view='side', legs='run', ph=t * 1.8, guitar=True, ex=dict(mouth='o', brows='up', blush=.9), key=27))
    breath(t, x + 120, 880, .7)
    camEnd()


# ================================================================ S28 chorus 2: knock, knock — nobody
def s28(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, 600, 900, 1.05)
    doorScene(t, 'north', 'day', sill=.3)
    knocks = [t0 + .6, t0 + 1.0, t0 + 2.3, t0 + 2.7]
    worried = t > t0 + 2.0
    hx = knockX(t, knocks)
    jhim(421, 1268, 28, dict(view='side', guitar=True, bendR=1, hands=dict(R=[hx, -9.0]),
                              ex=dict(mouth='flat' if worried else 'small', brows='sad' if worried else 'up'), key=28))
    knockFX(t, knocks, 530, 1268 - 9.0 * 28)
    camEnd()
    grade('night', .25)


# ================================================================ S29 chorus 2: the call — 已关机
def s29(t, lt, dur):
    t0 = t0of(t, lt)
    off = t > t0 + 1.8
    def draw():
        callScreen(t, 'off' if off else 'calling', seg(t, t0 + 1.8, t0 + 2.4))
    doorScene(t, 'north', 'day', sill=.3)
    flatRect(-400, -400, W + 800, H + 800, '#141018', .45)
    inPhone(draw, 'none', t, tilt=.01)
    vignette(.3, '#2A2418')


# ================================================================ S30 chorus 2: then I'll wait here
def s30(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, 470, 900, lerp(1.0, 1.08, es(t, t0, t0 + dur)))
    doorScene(t, 'north', 'day', sill=.35)
    sitAtDoor(t, 400, 27, dict(eyes='closed' if frac(t * .4) < .5 else 'half', mouth='o', brows='sad', blush=.9), caseSide=True, blow=True)
    camEnd()
    grade('night', .2)


# ================================================================ S31 chorus 2: morning → noon; the battery dies
def s31(t, lt, dur):
    t0 = t0of(t, lt)
    k = seg(t, t0, t0 + dur)
    cam(t, W / 2, 890, 1.0)
    doorScene(t, 'north', 'noon', sill=lerp(.35, 1.0, k))
    sitAtDoor(t, 400, 27, dict(eyes='half', mouth='flat', brows='sad', lookY=.7), phone=True, caseSide=True)
    camEnd()
    dead = t > t0 + 4.2
    def scr(x, y, r):
        if dead:
            miniScreen(x, y, r, [], dark=True)
        else:
            miniScreen(x, y, r, [('电量 1%', '#E9585E'), ('她 · 未接通', '#4A4458')], big='12:58')
    inset(780, 380, 170, scr, a=es(t, t0 + 1.0, t0 + 1.4) * (1 - es(t, t0 + 5.0, t0 + 5.4)))
    grade('night', .15)


# ================================================================ S32 chorus 2: he plays every song she likes at her door
def s32(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, lerp(540, 420, es(t, t0, t0 + dur)), lerp(890, 960, es(t, t0, t0 + dur)), lerp(1.0, 1.18, es(t, t0, t0 + dur)))
    doorScene(t, 'north', 'dusk' if t > t0 + 5 else 'day', sill=1.0, neighbor=es(t, t0 + 3.0, t0 + 4.0) * .5, cat_=es(t, t0 + 3.6, t0 + 4.2))
    sitAtDoor(t, 400, 27, dict(eyes='closed', mouth='small', brows='sad', blush=.6), guitar=True, caseSide=True)
    musicNotes(t, 470, 760, 5, .9)
    camEnd()
    grade('night', .2)


# ================================================================ S33 chorus 2: dusk, her window is still dark
def s33(t, lt, dur):
    t0 = t0of(t, lt)
    def fig(x, y, u):
        boilSeed('entr')
        paint(rectPts(x - 70, y - 190, 140, 190), wash='#5A4E5E', ink=INK, sw=.6)
        glow(x, y - 210, 90, '#FFE7A8', .7)
        paint(ellPts(x, y - 205, 16, 8, 10), wash='#FFE7A8', ink=INK, sw=.4)
        jhim(x, y, u, dict(view='front', guitar=True, ex=dict(eyes='half'), key=33))
    cam(t, W / 2, lerp(900, 860, es(t, t0, t0 + dur)), 1.0)
    cityWide(t, 'north', 'night', fig, 520, 1236, 7)
    camEnd()
    grade('night', .5)


# ================================================================ S34 bridge: close — tears freeze in the cold
def s34(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, 400, 1000, lerp(1.7, 1.8, es(t, t0, t0 + dur)))
    doorScene(t, 'north', 'night', sill=1.0)
    sitAtDoor(t, 400, 27, dict(eyes='teary', mouth='sad', brows='sad', tears=es(t, t0 + .5, t0 + 2.0), blush=1.0), blow=True, caseSide=True, snowOn=.4)
    breath(t, 440, 910, .7, .8)
    camEnd()
    grade('night', .6)


# ================================================================ S35 bridge: he sticks a note on her door
def s35(t, lt, dur):
    t0 = t0of(t, lt)
    back = es(t, t0 + 1.6, t0 + 2.4)
    cam(t, 620, 900, 1.15)
    doorScene(t, 'north', 'night', sill=1.0, note=0.0)
    noteOnDoor(t, clamp((t - t0) / .5))
    gx = lerp(478, 400, back)
    jhim(gx, 1268, 28, dict(view='side', guitar=True, bendR=1, hands=dict(R=[3.5, -9.4]) if back < .3 else {},
                              ex=dict(mouth='flat', brows='sad', eyes='teary' if back > .5 else 'open'), key=35))
    camEnd()
    grade('night', .5)


# ================================================================ S36 bridge: asleep against her door
def s36(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, W / 2, 890, lerp(1.0, 1.05, es(t, t0, t0 + dur)))
    doorScene(t, 'north', 'night', sill=1.0, neighbor=.6)
    noteOnDoor(t, 1.0)
    sitAtDoor(t, 400, 27, dict(eyes='closed', mouth='small', brows='sad'), caseSide=True, snowOn=.8, rot=-.06, blanket=1.0)
    thermos(640, 1290)
    for i in range(3):
        ph = frac(t * .4 + i / 3)
        text('z', 520 + ph * 60, 780 - ph * 120, 34 + 16 * ph, '#FFFDF6', face=WK, shadow=False, a=math.sin(ph * math.pi))
    camEnd()
    grade('night', .7)


# ================================================================ S37 verse 2 (her version): the same night, 22:30, her room
def herDesk(t, ex, umbrella=1.0, cx=W / 2, cy=H / 2, z=1.0, standing=False, storm=0.0, her='暴雨', herT='4℃'):
    cam(t, cx, cy, z)
    hisRoom(t, who='her', her=her, herT=herT, mine='大雪', mineT='-12℃', lamp=umbrella, storm=storm)
    u = 26
    if standing:
        jher(540, 1300, 30, dict(beanie=True, ex=ex, key=37, hands=dict(R=[3.9, -5.4]), itemR=umbDown))
    else:
        chairBack(470, 1330 - 2.9 * u, u)
        jher(470, 1330, u, dict(legs='sit', hands=dict(L=[-1.15, -7.7], R=[1.15, -7.7]), ex=ex, key=37))
        deskTop(t)
        deskItems(t, 1.0, 'her')
        phoneObj(470, 1140, 66, 0.0, glowK=1.0)
    camEnd()


def s37(t, lt, dur):
    t0 = t0of(t, lt)
    herDesk(t, dict(lookY=.7, mouth='small', brows='up', blush=.6), 1.0, lerp(W / 2, 520, es(t, t0, t0 + dur)), lerp(H / 2, 760, es(t, t0, t0 + dur)),
            lerp(1.0, 1.25, es(t, t0, t0 + dur)))
    grade('night', .5)
    tint('#FFD8C8', .06, skia.BlendMode.kScreen)
    k = es(t, t0 + .1, t0 + .5) * (1 - es(t, t0 + 2.6, t0 + 3.1))
    if k > .01:
        softBand(W / 2, 760, 600, 150, .5 * k)
        text('同一晚 · 她的版本', W / 2, 760, 72, '#FFF3E2', face=WK, stroke=INK, strokeW=10, shadow=True, a=k)


# ================================================================ S38 verse 2: his city is in a rainstorm — and his umbrella is here
def s38(t, lt, dur):
    t0 = t0of(t, lt)
    herDesk(t, dict(brows='knit', mouth='flat', blush=.6), 0.0, 540, 860, 1.0, standing=True, storm=1.0, her='暴雨预警', herT='4℃ 湿冷')
    grade('night', .5)


# ================================================================ S39 verse 2: on the train south; 23:00, her phone dies
def trainHer(t, outside='snow', mix=1.0, ex=None, clock=None, speed=0.0, refl=None):
    cam(t, W / 2, 890, 1.0)
    def main():
        u = 26
        jher(280, 1300, u, dict(legs='sit', hands=dict(L=[-1.0, -7.6], R=[1.0, -7.6]), ex=ex or dict(lookX=.9), key=39))
        umbLean(280, 1300 - 2.9 * u, u)
    trainBooth(t, outside, mix, True, 'left', [('right', lambda x, y, u: passengerStudent(t, x, y, u))], refl, clock, speed, main=main)
    camEnd()


def s39(t, lt, dur):
    t0 = t0of(t, lt)
    dead = t > t0 + 1.9
    trainHer(t, 'snow', 1.0, ex=dict(lookY=.5, mouth='o' if dead else 'small', brows='up', eyes='wide' if dead else 'open'))
    grade('night', .7)
    def scr(x, y, r):
        if dead:
            miniScreen(x, y, r, [], dark=True)
        else:
            miniScreen(x, y, r, [('电量 1%', '#E9585E')], big='22:59' if t < t0 + .9 else '23:00')
    inset(210, 430, 160, scr, a=es(t, t0 + .2, t0 + .6) * (1 - es(t, t0 + 2.4, t0 + 2.8)))


# ================================================================ S40 verse 2: she can't sleep; the snow outside slowly turns into rain
def s40(t, lt, dur):
    t0 = t0of(t, lt)
    trainHer(t, 'mix', 1 - es(t, t0, t0 + dur), ex=dict(eyes='half', mouth='flat', brows='sad', lookX=.9), clock=180, speed=8)
    grade('night', .8)


# ================================================================ S41 verse 2: 罗生门 — the same moment, two doors
def s41(t, lt, dur):
    t0 = t0of(t, lt)
    def top():
        cam(t, W / 2, 1000, .55)
        doorScene(t, 'north', 'dawn', sill=1.0)
        noteOnDoor(t, 1.0)
        sitAtDoor(t, 400, 27, dict(eyes='closed', mouth='small', brows='sad'), caseSide=True, snowOn=1.0, rot=-.06, blanket=1.0)
        thermos(640, 1290)
        camEnd()
    def bot():
        cam(t, W / 2, 1232, .55)
        doorScene(t, 'south', 'dawn')
        kn = [t0 + .5, t0 + .9, t0 + 2.1, t0 + 2.5]
        jher(421, 1268, 28, dict(view='side', wet=1.0, bendR=1, hands=dict(R=[knockX(t, kn), -9.0]), ex=dict(mouth='flat', brows='sad'), key=41, itemL=umbDown))
        knockFX(t, kn, 530, 1268 - 9.0 * 28)
        camEnd()
    splitV(t, top, bot)
    grade('night', .2)
    for (y, s, col) in ((176, '他 · 在她门口（北方 302）', '#3B5B98'), (912, '她 · 在他门口（南方 502）', '#CC3B42')):
        softBand(300, y, 520, 64, .5)
        text(s, 300, y, 36, '#FFFDF6', face=WK, shadow=False)
    k = backOut(clamp((t - (t0 + .3)) / .3))
    if k > .01:
        G.c.drawRoundRect(skia.Rect.MakeXYWH(W / 2 - 190 * k, H / 2 - 44, 380 * k, 88), 44, 44, skia.Paint(AntiAlias=True, Color=skcol('#1C1E2C', .9)))
        text('同一时刻 07:40', W / 2, H / 2, 44, '#FFE7A8', face=WK, shadow=False, sc=k)


# ================================================================ S42 verse 2: 03:00, two trains pass each other in the night
def s42(t, lt, dur):
    t0 = t0of(t, lt)
    k = seg(t, t0, t0 + dur)
    gradRect(-400, -400, W + 800, H + 800, ['#0E1228', '#1A2040', '#232A4E'])
    for i in range(40):
        G.c.drawCircle(hash1(i * 3) * W, hash1(i * 7) * 500 + 40, 2, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .5)))
    flatRect(-400, 1180, W + 800, 900, '#141830', 1.0)
    for (y0, dirn, who, col, stripe) in ((520, 1, 'her', '#D9D2C0', '#8E3A34'), (860, -1, 'him', '#E8E4D2', '#3F7F6A')):
        off = (k - .5) * 1500 * dirn
        boilSeed(f'band{who}')
        paint(rectPts(-400 + off, y0, W + 800 + 1600, 300), wash=col, ink=INK, sw=.9)
        flatRect(-400 + off, y0 + 250, W + 800 + 1600, 24, stripe, .95)
        for wi in range(-4, 8):
            wx = W / 2 - 130 + wi * 320 + off
            G.c.save()
            G.c.clipRRect(skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(wx, y0 + 30, 260, 200), 18, 18), True)
            gradRect(wx, y0 + 30, 260, 200, ['#FFE7A8', '#F2C88A'])
            if wi != 0 and wi % 2 == 0:
                for hh in range(1 + (wi % 3 == 0)):                       # other passengers: dozing heads, a reading lamp
                    G.c.drawCircle(wx + 80 + hh * 90, y0 + 170, 30, skia.Paint(AntiAlias=True, Color=skcol('#3A3346', .75)))
                    G.c.drawRect(skia.Rect.MakeXYWH(wx + 50 + hh * 90, y0 + 196, 60, 40), skia.Paint(AntiAlias=True, Color=skcol('#3A3346', .75)))
            elif wi != 0 and wi % 3 == 1:
                glow(wx + 200, y0 + 80, 60, '#FFFFFF', .4)
                G.c.drawCircle(wx + 150, y0 + 160, 28, skia.Paint(AntiAlias=True, Color=skcol('#3A3346', .7)))
            if wi == 0:
                if who == 'him':
                    jhim(wx + 130, y0 + 370, 17, dict(ex=dict(eyes='closed', mouth='flat', brows='sad'), key=42, rot=.05))
                else:
                    jher(wx + 130, y0 + 370, 17, dict(ex=dict(eyes='half', mouth='flat', brows='sad', lookY=.6), key=43))
            G.c.restore()
            paint(rrPts(wx, y0 + 30, 260, 200, 18), wash=None, ink=INK, sw=.6)
    a = math.exp(-((k - .5) / .06) ** 2)
    flash(.25 * a, '#FFF3D0')
    flatRect(-400, 820, W + 800, 40, '#0A0C18', .9)


# ================================================================ S43 verse 2: dawn in the south, pouring rain — she waits at his door
def s43(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, W / 2, 890, lerp(1.0, 1.06, es(t, t0, t0 + dur)))
    doorScene(t, 'south', 'dawn')
    jher(400, 1268, 28, dict(wet=1.0, hands=dict(R=[3.9, -5.4]), ex=dict(lookX=.8, mouth='flat', brows='sad', blush=.7), key=43, itemR=umbDown))
    camEnd()
    grade('night', .3)


# ================================================================ S44 verse 2: two lovers lost in two big cities
def s44(t, lt, dur):
    t0 = t0of(t, lt)
    def top():
        cam(t, W / 2, 900, 1.0)
        cityWide(t, 'north', 'dawn', lambda x, y, u: jhim(x, y, u, dict(legs='stand', guitar=True, key=44)), 560, 1236, 6)
        camEnd()
    def bot():
        cam(t, W / 2, 1250, 1.0)
        cityWide(t, 'south', 'dawn', lambda x, y, u: jher(x, y, u, dict(key=45)), 520, 1236, 6)
        camEnd()
    splitV(t, top, bot)


# ================================================================ S45 verse 2: a borrowed charger — his messages pour in
NOTIFS = [('他 · 23:00', '示例歌词占位文字？'), ('他 · 00:41', '睡了吗'), ('他 · 01:52', '那 晚安'), ('他 · 02:16', '撤回了一条消息'),
          ('他 · 03:31', '我去找你'), ('他 · 07:42', '我到你家门口了'), ('他 · 09:05', '未接来电 ×7')]


def s45(t, lt, dur):
    t0 = t0of(t, lt)
    def draw():
        notifStack(t, NOTIFS, seg(t, t0 + .5, t0 + dur - .2), '09:31', boot=es(t, t0, t0 + .4))
    rainStreet(t)
    flatRect(-400, -400, W + 800, H + 800, '#140E10', .4)
    inPhone(draw, 'none', t, tilt=.01)
    vignette(.3, '#2A1A10')


# ================================================================ S46 verse 2: her voice message
VOICE = '示例歌词占位文字？我在你家门口 示例歌 词占位文字示'


def s46(t, lt, dur):
    t0 = t0of(t, lt)
    base = [('sep', '09:33'), ('her', '我不在家'), ('her', '我在你家门口')]
    def draw():
        voiceScreen(t, VOICE, seg(t, t0 + .3, t0 + dur - .6), True, 'her', '09:33', base=base)
    rainStreet(t)
    flatRect(-400, -400, W + 800, H + 800, '#140E10', .4)
    inPhone(draw, 'none', t, tilt=-.01)
    vignette(.3, '#2A1A10')


# ================================================================ S47 verse 2: his phone lights again — 09:00, a voice message
def s47(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, W / 2, 890, 1.0)
    doorScene(t, 'north', 'day', sill=1.0, neighbor=.7)
    noteOnDoor(t, 1.0)
    sitAtDoor(t, 400, 27, dict(eyes='wide' if t > t0 + 2.2 else 'half', mouth='o' if t > t0 + 2.2 else 'flat', brows='up', lookY=.7), phone=True,
              caseSide=True, blanket=1.0)
    boilSeed('pbank')
    paint(rrPts(520, SEAT_Y - 2.9 * 27 - 40, 90, 44, 8), wash='#E9E2D2', ink=INK, sw=.5)       # borrowed power bank on the step
    G.c.drawLine(560, SEAT_Y - 2.9 * 27 - 30, 440, SEAT_Y - 6.6 * 27, skia.Paint(AntiAlias=True, Color=skcol('#2E2A38'), StrokeWidth=4))
    push()
    translate(600, SEAT_Y - 2.9 * 27 - 90)
    rotate(.08)
    paint(rectPts(-70, -36, 140, 72), wash='#FFE58A', ink=INK, sw=.4)
    text('先用着', 0, -10, 26, INK, face=WK, shadow=False)
    text('—301', 20, 20, 22, INK, face=WK, shadow=False)
    pop()
    thermos(700, 1290)
    camEnd()
    sec = int((t - t0) * 3) % 60
    def scr(x, y, r):
        if t < t0 + .5:
            miniScreen(x, y, r, [('充电中', '#3F9F5A')], big='6%')
        else:
            lines = [('电量 6%', '#4A4458')]
            if t > t0 + 2.2:
                lines = [('她 · 语音 0:08', '#CC3B42'), ('电量 6%', '#4A4458')]
            miniScreen(x, y, r, lines, big='09:00' if t > t0 + 1.3 else '08:59')
    inset(780, 380, 170, scr, a=es(t, t0 + .1, t0 + .4))
    grade('night', .15)


# ================================================================ S48 verse 2: her voice — he gets up and turns around
def s48(t, lt, dur):
    t0 = t0of(t, lt)
    tup, tturn = t0 + 1.1, L(83, 6) - .1
    cam(t, W / 2, 890, 1.0)
    doorScene(t, 'north', 'noon', sill=1.0, neighbor=.4)
    noteOnDoor(t, 1.0)
    thermos(700, 1290)
    if t < tup:
        sitAtDoor(t, 400, 27, dict(eyes='teary', mouth='o', brows='up', tears=.6, lookY=.6), phone=True, caseSide=True, blanket=1.0)
    elif t < tturn:
        boilSeed('blanketfold')
        paint(rrPts(260, SEAT_Y - 2.9 * 27 - 40, 220, 44, 10), wash='#C94A4A', ink=INK, sw=.6)
        jhim(420, 1268, 28, dict(view='side', guitar=True, ex=dict(eyes='teary', mouth='small', brows='up', tears=.6), key=48))
    else:
        k = seg(t, tturn, tturn + .5)
        x = lerp(420, -200, easeIn(seg(t, tturn + .25, tturn + 1.4)))
        jhim(x, 1268, 28, dict(view='front' if k < .45 else 'side', flip=k >= .45, legs='run' if k >= .45 else 'stand', ph=t * 1.8,
                               guitar=True, ex=dict(eyes='teary', mouth='grin', tears=.5, brows='up'), key=48))
        if k < .6:
            for i in range(5):
                G.c.drawLine(470 + i * 14, 900 + i * 30, 540 + i * 14, 900 + i * 30, skia.Paint(AntiAlias=True, Color=skcol(INK, .4 * (1 - k)), StrokeWidth=4))
    camEnd()
    def scr(x, y, r):
        G.c.drawRect(skia.Rect.MakeXYWH(x - r, y - r, 2 * r, 2 * r), skia.Paint(AntiAlias=True, Color=skcol('#E3E8F0')))
        for i in range(12):
            hh = 14 + 40 * abs(math.sin(t * 8 + i))
            flatRect(x - r * .7 + i * r * .12, y - r * .3 - hh / 2, r * .06, hh, '#7FC97A')
        for j, l in enumerate(('我在你家门口', '示例歌 词占位文字示')):
            text(l, x, y + r * (.2 + j * .26), r * .15, '#1F2233', face=WK, shadow=False)
    inset(780, 380, 170, scr, a=es(t, t0, t0 + .3) * (1 - es(t, tturn + .6, tturn + 1.0)))
    grade('night', .1)


# ================================================================ S49 chorus 3: back south — following her weather; snow turns to rain
def s49(t, lt, dur):
    t0 = t0of(t, lt)
    trainHim(t, 'mix', 1 - es(t, t0 + .5, t0 + dur - .5), ex=dict(eyes='happy', mouth='smile', tears=.5, blush=.8), night=False)
    grade('past', .35)


# ================================================================ S50 chorus 3: she is under the shop awning by his place
def s50(t, lt, dur):
    t0 = t0of(t, lt)
    tA = t0 + 1.2
    cam(t, W / 2, 860, 1.0)
    rainStreet(t)
    seat = 1290 - 2.9 * 24
    stepSeat(330, seat, 15 * 24, 1330, '#7E7A86')
    if t < tA + 1.0:
        jher(330, 1290, 24, dict(legs='sit', hands=dict(L=[-1.2, -7.2], R=[1.2, -7.2]), ex=dict(eyes='half' if t < tA else 'wide', mouth='flat' if t < tA else 'o', brows='up', blush=.7), key=50))
        umbLean(330, seat, 24)
    else:
        jher(330, 1290, 24, dict(ex=dict(eyes='teary', mouth='grin', brows='up', blush=1.0), key=50, hands=dict(R=[3.9, -5.4]), itemR=umbDown))
    x = lerp(1250, 720, easeOut(seg(t, tA - .2, tA + .9)))
    jhim(x, 1290, 24, dict(view='side', flip=True, legs='run' if t < tA + .9 else 'stand', ph=t * 1.8, guitar=True, wet=1.0,
                            ex=dict(mouth='grin', eyes='teary', tears=.4, brows='up'), key=51))
    rain(t, -60, -100, W + 60, H + 80, 150, .5, .15, 1600, 7)
    camEnd()
    grade('past', .5)


# ================================================================ S51 chorus 3: the umbrella tilts to him for the first time; her red scarf
def s51(t, lt, dur):
    t0 = t0of(t, lt)
    tS = t0 + 1.4
    cam(t, 520, 900, lerp(1.0, 1.18, es(t, t0, t0 + dur)))
    rainStreet(t)
    u = 25
    gx = 520
    scarfOn = t > tS
    jhim(gx + 5.7 * u, 1290, u, dict(wet=1.0, scarf='red' if scarfOn else None, ex=dict(eyes='happy' if scarfOn else 'teary', mouth='smile', tears=.5, blush=1.0), key=52))
    jher(gx - 5.7 * u, 1290, u, dict(scarf=None if scarfOn else 'red', hands=dict(R=[2.6, -11.4]), ex=dict(eyes='happy', mouth='grin', blush=1.0), key=53))
    hx, hy = gx - 5.7 * u + 2.6 * u, 1290 - 11.4 * u
    umbrellaOpen(hx + 3.0 * u, hy - 9.4 * u, 10.8 * u, .28)
    G.c.drawLine(hx, hy, hx + 3.0 * u, hy - 9.4 * u, skia.Paint(AntiAlias=True, Color=skcol(INK), StrokeWidth=7))
    paint(ellPts(hx, hy, .62 * u, .58 * u, 12), wash=HER['skin'], ink=INK, sw=.5)
    k = seg(t, tS - .5, tS)
    if 0 < k < 1:                                      # the scarf travels from her neck to his
        x, y = lerp(gx - 5.7 * u, gx + 5.7 * u, ease(k)), 1290 - 10.4 * u - math.sin(k * math.pi) * 60
        paint(ellPts(x, y, 2.4 * u, .8 * u, 16), wash='#CC3B42', ink=INK, sw=.6)
    if scarfOn:
        for i in range(4):
            ph = frac(t * .5 + i / 4)
            paint(heartPts(gx + (i - 1.5) * 60, 760 - ph * 160, 14), wash='#F19A92', washOp=int(255 * math.sin(ph * math.pi)), ink=None)
    rain(t, -60, -100, W + 60, H + 80, 130, .45, .15, 1600, 8)
    camEnd()
    grade('past', .6)


# ================================================================ S52 outro: next morning — one weather on the board
def s52(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, 540, lerp(700, 760, es(t, t0, t0 + dur)), 1.12)
    hisRoom(t, unified=('我们这 · 南方', '晴  18℃'), morning=1.0, lamp=0.0)
    u = 27
    jhim(400, 1310, u, dict(scarf='red', ex=dict(eyes='happy', mouth='smile', blush=.8), key=54))
    jher(400 + 11 * u, 1310, u, dict(scarf=None, hands=dict(R=[1.3, -7.3]), ex=dict(mouth='grin', blush=.9, lookX=-.4), key=55,
                                    itemR=lambda uu, sw, C: paint(rrPts(-.25 * uu, -1.0 * uu, .5 * uu, 1.2 * uu, 4), wash='#F3F0E6', ink=INK, sw=.4)))
    camEnd()
    tint('#FFF1D6', .10, skia.BlendMode.kScreen)


# ================================================================ S53 outro: on the step outside his door, the rain has stopped
def s53(t, lt, dur):
    t0 = t0of(t, lt)
    cam(t, W / 2, lerp(900, 840, es(t, t0, t0 + dur)), lerp(1.08, .98, es(t, t0, t0 + dur)))
    doorScene(t, 'south', 'day', clear=True)
    glow(230, 410, 300, '#FFE7A8', .5)
    u = 26
    seat = SEAT_Y - 2.9 * u
    stepSeat(440, seat, 26 * u, SEAT_Y + 40, '#9A8F80')
    jhim(330, SEAT_Y, u, dict(legs='sit', scarf='red', hands=GUITAR_HANDS(t), mid=guitarMid(t), ex=dict(eyes='happy', mouth='smile', blush=.8), key=56))
    jher(330 + 12.4 * u, SEAT_Y, u, dict(legs='sit', scarf=None, rot=-.08, hands=dict(L=[-2.4, -6.6], R=[2.4, -6.6]),
                                         ex=dict(eyes='closed', mouth='smile', blush=.9), key=57))
    boilSeed('umbW')
    paint([[860, 1150], [884, 1150], [940, 760], [928, 752]], wash='#F2C14E', ink=INK, sw=.6)       # the yellow umbrella, closed, against the wall
    musicNotes(t, 360, 760, 4, .8)
    camEnd()
    tint('#FFF1D6', .08, skia.BlendMode.kScreen)
