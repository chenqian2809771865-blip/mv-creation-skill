# story_c.py: 《匆匆那年》 S23–S31 — verse 2, the same years from his seat: he only looked at her, he crossed on purpose,
# the letter was for her, the snowy goodbye, the class photo, the account he never erased, the letter taped under her half.
import math
from eng import *
import eng
from clawd import *
from cc import *
from cc2 import *
from props import bubble, sparkle
from hb import woodTop
from wo import scr
from nm import darkness
from story_b import front, handDot, slide, seasonTint, seated
from common import *


# ================================================================ S23 in class he only looks at her
def s23(t, lt, dur):
    glance = 121.6 < t < 122.5
    ho = feel('neutral', t, dict(lookX=.75 if glance else 0, lookY=-.2, aL=-.3, aR=-.1, blush=.2))
    caught = t > 121.7
    mo = feel('nervous' if 121.7 < t < 122.6 else 'neutral', t, dict(lookX=-.8 if not caught or t > 122.6 else 0, blush=.35 if not caught else .8,
                                                                   aL=-.3, aR=-.3, emote=None))
    if 121.7 < t < 122.6:
        mo['lookX'] = 0
    front(t, '2013', ho, mo, lambda: (deskBooks(PD_X0 + 20, 3, 'db1'), deskBooks(PD_X1 - 100, 3, 'db2')),
          cam_=(lerp(990, 1060, ease(lt / dur)), 640, lerp(1.3, 1.42, ease(lt / dur))))


# ================================================================ S24 on purpose: his pencil case waits at the line, then goes over
def s24(t, lt, dur):
    cam(t, 1000, 520, 1.5)
    nr, kr = (15, ease(seg(t, 125.8, 126.2))) if t > 125.75 else (14, 1.0)
    deskState(t, old=.05, his=10, her=nr, herK=kr, taunts=0.0, graffiti=.12)
    if t < 124.6:
        x, y, _ = slide(t, 123.8, 124.6, (1340, 470), (1062, 470))
    elif t < 125.2:
        x, y = 1062 - 6 * max(0, math.sin((t - 124.6) * 18)) * (t > 124.9), 470
    else:
        x, y, _ = slide(t, 125.2, 125.6, (1062, 470), (870, 470), easeOut)
    pencilCase(x, y, .02, '#3F5FAE', key='pc24')
    camEnd()
    pastGrade(1.0)


# ================================================================ S25 she's cross, he can't stop smiling
def s25(t, lt, dur):
    ho = feel('angry', t, dict(lookX=.4, lookY=.4, aR=.1 + .12 * math.sin(t * 16), aL=-.3, blush=.3))
    mo = feel('happy', t, dict(lookX=-.75, blush=.5, emote='heart' if t > 127.6 else None, emoteAge=t - 127.6))
    front(t, '2014', ho, mo, lambda: (deskBooks(PD_X0 + 20, 3, 'db1'), deskBooks(PD_X1 - 100, 3, 'db2')),
          cam_=(960, 640, lerp(1.35, 1.42, lt / dur)))


# ================================================================ S26 night, his desk at home: the letter
LP = (960, 560, 1000, 660)


def crumple(x, y, r, key):
    boilSeed(key)
    pts = []
    for i in range(14):
        a = i / 14 * TAU
        rr = r * (.75 + .35 * hash1(i * 3.1 + x))
        pts.append([x + math.cos(a) * rr, y + math.sin(a) * rr])
    paint(pts, wash='#F9D3DE', fill='#E6A9BA', fillOp=60, ink=INK, sw=.6)
    for i in range(4):
        a = hash1(i * 2.2 + y) * TAU
        inkLine([[x, y], [x + math.cos(a) * r * .7, y + math.sin(a) * r * .7]], .4, '#C98A9C', 'inkfine', .3)


def s26(t, lt, dur):
    cam(t, lerp(900, 960, ease(lt / dur)), lerp(470, 540, ease(lt / dur)), lerp(1.45, 1.3, ease(lt / dur)))
    woodTop(.1, key='hwood')
    crumple(300, 300, 60, 'cr1')
    crumple(410, 820, 50, 'cr2')
    crumple(1640, 260, 56, 'cr3')
    cx, cy, w, h = LP
    letterPaper(cx, cy, w, h, 0.0, key='lp26')
    progs = (seg(t, 129.5, 130.6), seg(t, 130.8, 133.7), seg(t, 133.9, 136.5), 0)
    tip = letterText(cx, cy, w, h, progs, 0.0)
    if tip:
        fountainPen(tip[0], tip[1], 40, ang=-1.0, key='fp26')
    else:
        fountainPen(cx + w / 2 + 40, cy + 200, 40, ang=-1.2, key='fp26')
    lamp = scr(1500, 120)
    camEnd()
    darkness(.6, [(lamp[0], lamp[1] + 220, 1100, 1.0)], '#0B1030')
    glow(lamp[0], lamp[1], 420, '#FFD58A', .45)
    pastGrade(.6)


# ================================================================ S27 he tries to give it to her; she has turned away
def s27(t, lt, dur):
    ho = feel('sad', t, dict(tint=None, view='q', flip=True, lookX=.4, aL=-.3, aR=-.3))
    lift = ease(seg(t, 136.0, 136.8)) * (1 - ease(seg(t, 138.6, 140.0)))
    mo = feel('hopeful' if t < 138.4 else 'sad', t, dict(view='q', flip=True, lookX=.5, aL=-.3, aR=lerp(-.3, .55, lift)))

    def after():
        hx, hy = handXY(P_HIM, PD_SEAT + 2 * U2, U2, mo, 'R')
        envelope(hx - 30, hy - 10, 110, -.2, '', 0.0, key='env27')
        handDot(hx, hy, 'him', U2)
    front(t, '2015', ho, mo, lambda: (deskBooks(PD_X0 + 20, 4, 'db1'), deskBooks(PD_X1 - 120, 4, 'db2'), bookWall(1.0)),
          cam_=(lerp(1000, 1060, lt / dur), 640, lerp(1.32, 1.42, lt / dur)), after=after, grade=.7)
    desat(.25)
    tint('#9AA8C8', .12, skia.BlendMode.kMultiply)


# ================================================================ S28 snowy night at the gate: "we're even" — he doesn't go after her
def s28(t, lt, dur):
    cam(t, lerp(960, 1080, ease(seg(t, 143.0, 146.0))), 560, lerp(1.0, 1.18, ease(seg(t, 143.0, 146.0))))
    gateScene(t, 'night', snow=1.0, shopLit=.6)
    u = 30
    if t < 141.9:
        hx = 820
        ho = feel('sad', t, dict(tint=None, view='q', lookX=.4, hat=['beanieR', 'flower']))
    else:
        st = stroll(t, 141.9, 146.6, 820, 120, u)
        hx = st['x']
        ho = feel('sad', t, dict(tint=None, view='q', flip=True, walk=st['walk'], dy=st['dy'], hat=['beanieR', 'flower']))
        footprints(hx + 60, 800, GATE_FLOOR + 10, int(abs(820 - hx) / 60) + 1, .45)
    mo = feel('sad', t, dict(tint=None, view='q', flip=True, lookX=.6, hat=['beanieB'], aR=.2, aL=-.4))
    teen('her', hx, GATE_FLOOR, u, ho)
    teen('him', 1160, GATE_FLOOR, u, mo)
    hx2, hy2 = handXY(1160, GATE_FLOOR, u, mo, 'R')
    envelope(hx2 - 16, hy2 - 6, 80, -.3, '', 0.0, key='env28')
    handDot(hx2, hy2, 'him', u)
    if t > 143.0:
        tears(t, 1160 - 1.5 * u - 1.9 * u, GATE_FLOOR - 5.7 * u, u, a=ease(seg(t, 143.0, 143.6)), seed=3)
    bubble(760, GATE_FLOOR - 15 * u, '两清了。', 42, (800, GATE_FLOOR - 10 * u), ease(seg(t, 140.95, 141.2)) * (1 - ease(seg(t, 142.3, 142.6))), key='b28')
    camEnd()
    pastGrade(.5)
    tint('#8EA0D0', .1, skia.BlendMode.kMultiply)


# ================================================================ S29 the class photo, summer 2016: as far apart as they could stand
def s29(t, lt, dur):
    cam(t, lerp(960, 960, lt / dur), 540, lerp(1.0, 1.08, ease(lt / dur)))
    flatRect(-900, -900, W + 1800, H + 1800, '#5A4A44')
    boilSeed('cork')
    paint(rectPts(-200, -200, W + 400, H + 400), fill='#3E322E', fillOp=50, bleed=.02, tex=.9, border=.2, ink=None)
    push()
    translate(960, 520)
    rotate(-.02)
    translate(-960, -520)
    gradPhoto(t, 960, 520, 1300, flashK=1 - ease(seg(t, 146.2, 146.75)))
    pop()
    driftPetals(t * 1.3, 1.0, 'spring')
    camEnd()
    pastGrade(.7)


# ================================================================ S30 graduation day: his half, never erased
def s30(t, lt, dur):
    k = ease(lt / dur)
    cam(t, lerp(1320, 1080, k), lerp(640, 600, k), lerp(1.6, 1.3, k))
    deskState(t, old=.22, his=99, her=96, white=(1, 1, 1), carve=1.0, taunts=1.0, graffiti=.5)
    noteText(1560, 860, 200, ['毕业快乐'], col='#C9F0D8', rot=.08, key='bye30', size=34, ink_='#2F7A5A')
    camEnd()
    pastGrade(1.0)
    seasonTint(1.0, '#C8F0B8')


# ================================================================ S31 under her half of the desk: the letter, taped where she'd find it
def s31(t, lt, dur):
    cam(t, 860, 560, lerp(1.0, 1.12, ease(lt / dur)))
    envK = ease(seg(t, 157.6, 158.4))
    tapes = clamp((t - 159.4) / .4) + clamp((t - 160.4) / .4)
    push()
    translate(0, (1 - envK) * 260)
    pop()
    underside(t, old=0.08, envK=envK, tapes=tapes)
    camEnd()
    glow(W * .45, H * .6, 900, '#FFD58A', .25)
    pastGrade(.8)
    dim = ease(seg(t, 164.4, 166.4))
    flatRect(-60, -60, W + 120, H + 120, '#0B1030', .35 * dim)
