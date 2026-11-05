# couple.py: 校园男女主的水彩手绘版（原设定是 320 像素版，见 references/cast.md）— 约 2.3 头身，可跨歌复用。
# 首次用于《罗生门（Follow）》竖屏 2:3 (2026-11-04，用户指定「直接用校园男女主」+ 水彩重画)。
# 骨架取自《新地球》阿屿 ayu.py（part / ik / _arm / face）。配色、发型、卫衣、红围巾照 cast.md 原设定。
#
# 调用：jhim(x, y, u, o) = 他，jher(x, y, u, o) = 她。(x, y) = 两脚之间的地面点；u = 单位，全身约 20u 高（头顶约 −19.3u）。
#   并排不穿模：正面两人中心距 ≥ 10.5u；他背琴盒时琴盒在身后左侧伸出约 2u，靠她那侧时 ≥ 12u。
# 识别特征：
#   他：黑色短碎发 + 锯齿刘海；藏青连帽卫衣（米白抽绳、袋鼠兜）、深色长裤、白球鞋；常背深棕吉他琴盒（guitar=True）。内敛的追梦音乐人。
#   她：棕色齐刘海波波头（长到下颌）；奶油色毛衣；红围巾（标志色，尾端垂在胸前，默认就戴）；深紫灰短裙、深色裤袜、棕短靴。温柔，笑着放手。
#   季节 / 剧情配件：beanie=True（她的奶白毛线帽），scarf=None 可摘掉她的围巾 / scarf='red' 给他戴，wet（淋湿：发梢滴水、衣服变深）。
# o（dict）：view front|side|back，flip，legs stand|walk|run|sit，ph 走路相位 0..1，hands=dict(L=[x,y], R=[x,y])（单位坐标，
#   相对身体，坐下时随身体下移），itemL/itemR = fn(u, sw, C) 画在手上，mid = fn(u, sw) 画在身体和手之间（抱着的吉他、琴盒），
#   over = fn(u, sw) 画在身体最上层（身体坐标），
#   ex = 表情 dict（eyes open|happy|closed|half|squeeze|wide|sparkle|teary，mouth flat|small|smile|grin|o|sad|wavy，brows sad|up|knit，
#   blush 0..1，tears 0..1，lookX/lookY −1..1），bob，rot，sq，shadow，key（墨线沸腾种子），blink（默认 True，约 3.6 秒眨一次）。
# 坐姿（正面）：身体下移 1.5u，座面顶 = y − 2.9u；场景先画椅背、椅面，再画人（腿垂在座面前沿）。侧面坐姿：膝盖在前，座面顶 = y − 3.3u。
import math
import skia
from eng import *

HIM = dict(name='jhim', skin='#F2C9A8', skinDk='#D9A083', skinLt='#FBE3D2', blush='#F19A92',
           hair='#2C2536', hairLt='#4B4060',
           coat='#3B5B98', coatDk='#2A4375', coatLt='#5A80C2', string='#DCD6CC',
           pants='#343A52', pantsDk='#252A3D',
           shoe='#E8E4DE', shoeDk='#BDB6AA', shoeLine='#9AA3B8',
           case='#3A2B27', caseDk='#231B1C', caseLt='#5A463F', strap='#231B1C')
HER = dict(name='jher', skin='#F6D0B2', skinDk='#DFA689', skinLt='#FDE8D8', blush='#F19A92',
           hair='#6B3D2B', hairLt='#94573A',
           coat='#EFE4CB', coatDk='#CDBD9C', coatLt='#FFF8EA',
           skirt='#4D4560', skirtDk='#363048',
           pants='#3F3747', pantsDk='#2A2431',
           shoe='#7B4A32', shoeDk='#553220', shoeLt='#A06A4C',
           scarf='red',
           beanie='#F3EAD8', beanieDk='#CFC2A8', pom='#FFFDF6')
SCARF = dict(red=('#CC3B42', '#972A35', '#E8777A'), cream=('#F1E6CF', '#CDBE9E', '#FFF8EA'))


def _P(pts, u):
    return [[a * u, b * u] for a, b in pts]


LITE = [False]


def part(P, col, dk=None, lt=None, sd=(1, .3), ink=True, sw=1.0, curv=True, opD=120, opL=130, br='ink', inkCol=None):
    """watercolour part: flat wash + clipped shadow/light blooms + boiling ink outline (P in canvas units)"""
    Q = throughClosed(P, 4) if curv else P
    if LITE[0]:
        paint(Q, wash=col, ink=None)
        if dk:
            xs = [p[0] for p in Q]
            ys = [p[1] for p in Q]
            cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
            w, h = max(xs) - min(xs), max(ys) - min(ys)
            G.c.save()
            G.c.clipPath(skia.Path().addPoly([skia.Point(float(a), float(b)) for a, b in Q], True), skia.ClipOp.kIntersect, True)
            paint(ellPts(cx + sd[0] * w * .55, cy + sd[1] * h * .5, w * .62, h * .78, 14), wash=dk, washOp=int(opD * .45), ink=None)
            G.c.restore()
        if ink:
            inkStroke(Q, True, sw, inkCol or INK, br)
        return
    paint(Q, wash=col, washOp=242, fill=col, fillOp=140, bleed=.06, tex=.5, border=.75, ink=None)
    if dk or lt:
        xs = [p[0] for p in Q]
        ys = [p[1] for p in Q]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        w, h = max(xs) - min(xs), max(ys) - min(ys)
        G.c.save()
        G.c.clipPath(skia.Path().addPoly([skia.Point(float(a), float(b)) for a, b in Q], True), skia.ClipOp.kIntersect, True)
        if dk:
            paint(ellPts(cx + sd[0] * w * .55, cy + sd[1] * h * .5, w * .62, h * .78, 20), fill=dk, fillOp=opD, bleed=.25, tex=.6, border=.3, ink=None)
        if lt:
            paint(ellPts(cx - sd[0] * w * .3, cy - sd[1] * h * .35 - h * .12, w * .3, h * .26, 16), fill=lt, fillOp=opL, bleed=.3, tex=.7, border=.2, ink=None)
        G.c.restore()
    if ink:
        inkStroke(Q, True, sw, inkCol or INK, br)


def ik(S, Hd, l1, l2, bend=1):
    dx, dy = Hd[0] - S[0], Hd[1] - S[1]
    d = math.hypot(dx, dy)
    d2 = clamp(d, .1, l1 + l2 - 1e-3)
    if d > d2:
        Hd = [S[0] + dx / d * d2, S[1] + dy / d * d2]
    a = math.atan2(Hd[1] - S[1], Hd[0] - S[0])
    c = clamp((l1 * l1 + d2 * d2 - l2 * l2) / (2 * l1 * d2), -1, 1)
    b = math.acos(c) * bend
    E = [S[0] + math.cos(a + b) * l1, S[1] + math.sin(a + b) * l1]
    return E, Hd


# ---------------------------------------------------------------- legs and shoes (local unit coords, canvas at the feet)
def _leg(x0, y0, x1, y1, u, sw, C, w=1.12):
    P = ribbon([[x0 * u, y0 * u], [(x0 + x1) / 2 * u, (y0 + y1) / 2 * u], [x1 * u, y1 * u]], w * u, w * .95 * u)
    part(P, C['pants'], C['pantsDk'], None, sd=(.5, 0), sw=sw * .7, curv=False, opD=90)


def _shoe(cx, u, sw, C, side=False, toe=1, rot=0, ox=0, oy=0, boot=False):
    push()
    translate(ox * u, oy * u)
    if rot:
        rotate(rot)
    h = 2.0 if boot else 1.15
    if side:
        pts = [[-.95, -h], [.75, -h], [.85, -.75], [1.95 * toe, -.5], [2.05 * toe, 0], [-1.0, 0]]
    else:
        pts = [[cx - 1.0, -h], [cx + 1.0, -h], [cx + 1.1, -.45], [cx + 1.16, 0], [cx - 1.16, 0], [cx - 1.1, -.45]]
    part(_P(pts, u), C['shoe'], C['shoeDk'], C.get('shoeLt'), sd=(.6, .2), sw=sw * .8)
    if side:
        inkLine(_P([[-1.0, -.3], [2.0 * toe, -.3]], u), sw * .5, C['shoeDk'], 'inkfine', 0)
        if not boot:
            inkLine(_P([[-.6, -.72], [1.2 * toe, -.6]], u), sw * .55, C['shoeLine'], 'inkfine', .2)
    else:
        inkLine(_P([[cx - 1.1, -.3], [cx + 1.1, -.3]], u), sw * .5, C['shoeDk'], 'inkfine', 0)
        if not boot:
            inkLine(_P([[cx - .55, -.75], [cx + .55, -.75]], u), sw * .55, C['shoeLine'], 'inkfine', 0)
        else:
            inkLine(_P([[cx - 1.0, -1.65], [cx + 1.0, -1.65]], u), sw * .45, INK, 'inkfine', 0)
    pop()


def _hand(x, y, u, sw, C, r=.62):
    part(ellPts(x * u, y * u, r * u, r * .92 * u, 14), C['skin'], C['skinDk'], None, sd=(.4, .4), sw=sw * .7, opD=80)


def _arm(S, Hd, u, sw, C, bend=1, item=None, far=False):
    E, Hd = ik(S, Hd, 2.35, 2.25, bend)
    col = C['coat']
    if far:
        col = mixCol(col, C['coatDk'], .35)
    dx, dy = Hd[0] - E[0], Hd[1] - E[1]
    d = math.hypot(dx, dy) or 1
    Wr = [Hd[0] - dx / d * .55, Hd[1] - dy / d * .55]
    P = ribbon(_P([S, E, Wr], u), 1.6 * u, 1.3 * u)
    part(P, col, mixCol(col, INK, .28), None, sd=(.3, .5), sw=sw * .8, curv=False, opD=90)
    cf = [Hd[0] - dx / d * .75, Hd[1] - dy / d * .75]
    inkLine(_P([[cf[0] - dy / d * .64, cf[1] + dx / d * .64], [cf[0] + dy / d * .64, cf[1] - dx / d * .64]], u), sw * .55, INK, 'inkfine', 0)
    _hand(Hd[0], Hd[1], u, sw, C)
    if item:
        push()
        translate(Hd[0] * u, Hd[1] * u)
        item(u, sw, C)
        pop()


# ---------------------------------------------------------------- face
def _blinking(C, o):
    if not o.get('blink', True):
        return False
    ph = hash1(len(C['name']) * 7 + (o.get('key', 0) if isinstance(o.get('key', 0), int) else 3)) * 3.6
    return frac((G.T + ph) / 3.6) < .035


def face(u, sw, C, o, ex, side=False):
    eyes = ex.get('eyes', 'open')
    if eyes in ('open', 'teary', 'wide') and _blinking(C, o):
        eyes = 'closed'
    mouth = ex.get('mouth', 'flat')
    lx, ly = ex.get('lookX', 0) * .28, ex.get('lookY', 0) * .25
    xs = [2.55] if side else [-1.8, 1.8]
    ey = -13.35
    for i, x in enumerate(xs):
        if eyes in ('open', 'wide', 'sparkle', 'teary'):
            rx, ry = (.6, .86) if eyes != 'wide' else (.72, 1.0)
            if side:
                rx *= .8
            paint(ellPts((x + lx) * u, (ey + ly) * u, rx * u, ry * u, 16), wash=INK, ink=None)
            paint(ellPts((x + lx - .2) * u, (ey + ly - .32) * u, .22 * u, .27 * u, 10), wash='#FFFFFF', ink=None)
            paint(ellPts((x + lx + .2) * u, (ey + ly + .35) * u, .1 * u, .1 * u, 8), wash='#FFFFFF', washOp=220, ink=None)
            if eyes == 'sparkle':
                paint(starPts((x + lx + .15) * u, (ey + ly + .15) * u, .38 * u, .3, 4), wash='#FFF3B0', ink=None)
            if eyes == 'teary':
                paint(ellPts(x * u, (ey + .72) * u, .72 * u, .26 * u, 12), wash='#9CC9EC', washOp=210, ink=INK, sw=sw * .3)
        elif eyes == 'happy':
            inkLine(_P([[x - .65, ey + .35], [x, ey - .35], [x + .65, ey + .35]], u), sw * .9, INK, 'ink', .4)
        elif eyes == 'closed':
            inkLine(_P([[x - .65, ey], [x, ey + .3], [x + .65, ey]], u), sw * .85, INK, 'ink', .4)
        elif eyes == 'half':
            hx, hy = lx * 1.6, max(-.15, ly * .5)
            paint(_P([[x - .58 + hx, ey - .05], [x + .58 + hx, ey - .05], [x + .5 + hx, ey + .6], [x - .5 + hx, ey + .6]], u), wash=INK, ink=None)
            inkLine(_P([[x - .75, ey - .1], [x + .75, ey - .1]], u), sw * .8, INK, 'ink', 0)
        elif eyes == 'squeeze':
            s = -1 if (i == 0 and not side) else 1
            inkLine(_P([[x - .5 * s, ey - .5], [x + .45 * s, ey], [x - .5 * s, ey + .5]], u), sw * .85, INK, 'ink', 0)
    br = ex.get('brows')
    if br:
        for i, x in enumerate(xs):
            s = -1 if (i == 0 and not side) else 1
            if br == 'sad':
                inkLine(_P([[x - .6 * s, -14.75], [x + .55 * s, -15.15]], u), sw * .55, INK, 'inkfine', 0)
            elif br == 'up':
                inkLine(_P([[x - .6, -15.0], [x, -15.25], [x + .6, -15.0]], u), sw * .55, INK, 'inkfine', .5)
            elif br == 'knit':
                inkLine(_P([[x - .6 * s, -15.15], [x + .55 * s, -14.8]], u), sw * .55, INK, 'inkfine', 0)
    bl = ex.get('blush', .35)
    bxs = [2.9] if side else [-2.95, 2.95]
    if bl:
        for x in bxs:
            paint(ellPts(x * u, -12.35 * u, .8 * u, .38 * u, 12), fill=C['blush'], fillOp=150 * bl, bleed=.25, ink=None)
    nx = 3.95 if side else .05
    paint(ellPts(nx * u, -12.72 * u, .17 * u, .12 * u, 8), wash=mixCol(C['skinDk'], C['blush'], .3), ink=None)
    mx = 3.0 if side else 0
    my = -11.95
    w = .55 if side else 1
    if mouth == 'flat':
        inkLine(_P([[mx - .5 * w, my], [mx + .5 * w, my]], u), sw * .7, INK, 'ink', 0)
    elif mouth == 'small':
        inkLine(_P([[mx - .45 * w, my - .05], [mx, my + .16], [mx + .45 * w, my - .05]], u), sw * .65, INK, 'ink', .5)
    elif mouth == 'smile':
        inkLine(_P([[mx - .85 * w, my - .2], [mx, my + .35], [mx + .85 * w, my - .2]], u), sw * .75, INK, 'ink', .5)
    elif mouth == 'grin':
        P = [[mx - .95 * w, my - .3], [mx + .95 * w, my - .3], [mx + .6 * w, my + .5], [mx, my + .72], [mx - .6 * w, my + .5]]
        paint(throughClosed(_P(P, u), 3), wash='#7E2E36', ink=INK, sw=sw * .6)
        paint(ellPts(mx * u, (my + .45) * u, .45 * w * u, .2 * u, 10), wash='#EE7C86', ink=None)
    elif mouth == 'o':
        paint(ellPts(mx * u, (my + .1) * u, .32 * w * u, .4 * u, 12), wash='#7E2E36', ink=INK, sw=sw * .5)
    elif mouth == 'sad':
        inkLine(_P([[mx - .6 * w, my + .22], [mx, my - .12], [mx + .6 * w, my + .22]], u), sw * .65, INK, 'ink', .5)
    elif mouth == 'wavy':
        inkLine(_P([[mx - .8 * w, my], [mx - .4 * w, my - .2], [mx, my + .1], [mx + .4 * w, my - .2], [mx + .8 * w, my]], u), sw * .65, INK, 'ink', .3)
    tr = ex.get('tears', 0)
    if tr > .01:
        for x in xs:
            s = -1 if x < 0 else 1
            L = 1.2 + 2.0 * tr
            P = [[x + .25 * s, ey + .7], [x + .45 * s, ey + .7 + L * .5], [x + .35 * s, ey + .7 + L]]
            inkLine(_P(P, u), sw * 1.1, '#8CC3EC', 'ink', .4)
            paint(ellPts((x + .35 * s) * u, (ey + .9 + L) * u, .28 * u, .36 * u, 10), wash='#A9D3F2', washOp=int(230 * tr), ink=INK, sw=sw * .3)


def glasses(u, sw, C, side=False):
    col = C['glass']
    if side:
        paint(ellPts(2.7 * u, -13.35 * u, .78 * u, .95 * u, 18), wash='#FFFFFF', washOp=34, ink=col, sw=sw * .55, br='inkfine')
        inkLine(_P([[1.92, -13.55], [.2, -13.8]], u), sw * .5, col, 'inkfine', .2)
        return
    for s in (-1, 1):
        paint(ellPts(s * 1.8 * u, -13.35 * u, 1.08 * u, 1.0 * u, 20), wash='#FFFFFF', washOp=34, ink=col, sw=sw * .55, br='inkfine')
        inkLine(_P([[s * 2.88, -13.5], [s * 4.3, -13.75]], u), sw * .5, col, 'inkfine', 0)
    inkLine(_P([[-.72, -13.5], [0, -13.75], [.72, -13.5]], u), sw * .5, col, 'inkfine', .5)


def starClip(x, y, u, sw, C, r=.95, rot=-.25):
    paint(starPts(x * u, y * u, r * u, .45, 5, rot - math.pi / 2), wash=C['clip'], ink=INK, sw=sw * .55)
    paint(ellPts((x - .2) * u, (y - .25) * u, .22 * u, .16 * u, 8), wash='#FFF6C8', ink=None)


# ---------------------------------------------------------------- hair
def _boyTop(u, sw, C, side):
    hc, hd, hl = C['hair'], mixCol(C['hair'], INK, .4), C['hairLt']
    if side:
        P = [[-5.0, -12.6], [-5.15, -15.6], [-3.8, -18.3], [-1.0, -19.3], [2.0, -19.1], [4.0, -17.7], [4.85, -15.6], [4.3, -15.9],
             [3.75, -15.0], [3.1, -15.75], [2.3, -15.1], [1.4, -16.05], [.4, -15.5], [-.6, -15.0], [-1.1, -13.4], [-2.0, -12.0], [-3.6, -11.6]]
        ah = [[.6, -19.15], [1.0, -20.4], [2.1, -21.1], [2.5, -20.6]]
    else:
        P = [[-4.95, -12.9], [-5.1, -15.6], [-3.95, -18.15], [-1.5, -19.3], [1.5, -19.3], [3.95, -18.15], [5.1, -15.6], [4.95, -12.9],
             [4.35, -13.8], [3.95, -15.25], [2.85, -14.7], [1.75, -15.5], [.55, -14.8], [-.55, -15.55], [-1.75, -14.85], [-2.85, -15.55], [-3.95, -15.0], [-4.35, -13.8]]
        ah = [[.2, -19.25], [.55, -20.5], [1.6, -21.25], [2.0, -20.75]]
    part(_P(P, u), hc, hd, hl, sd=(.3, .3), sw=sw * .85, curv=False, opL=170)
    if C.get('ahoge'):
        inkLine(_P(ah, u), sw * 1.5, INK, 'ink', .6)
        inkLine(_P(ah, u), sw * .8, hc, 'ink', .6)
    # a few spiky tufts on the crown (短碎发)
    sp = [[-2.6, -18.9], [-2.0, -20.0], [-1.2, -19.2], [-.4, -20.25], [.5, -19.3], [1.4, -20.1], [2.1, -19.0]] if not side else \
         [[-1.6, -19.1], [-1.0, -20.2], [-.1, -19.4], [.9, -20.3], [1.7, -19.3], [2.6, -19.9], [3.1, -18.7]]
    part(_P(sp + [[sp[-1][0], -18.6], [sp[0][0], -18.6]], u), hc, None, hl, sw=sw * .7, curv=False)
    for k in range(3):
        xx = -2.4 + k * 1.9
        inkLine(_P([[xx, -18.4], [xx + .6, -16.6]], u), sw * .3, hl, 'inkfine', .4)


def _girlBack(u, sw, C, side, wet=0):
    """the bob behind the head (drawn before the torso): jaw length, slightly flared"""
    hc, hd, hl = C['hair'], mixCol(C['hair'], INK, .4), C['hairLt']
    if side:
        P = [[-5.2, -15.6], [-5.6, -13.0], [-5.5, -11.2], [-4.6, -10.6], [-3.0, -10.9], [-1.6, -11.2], [-.6, -12.6], [0, -14.6]]
    else:
        P = [[-5.2, -15.4], [-5.75, -13.0], [-5.85, -11.3], [-5.0, -10.65], [5.0, -10.65], [5.85, -11.3], [5.75, -13.0], [5.2, -15.4]]
    part(_P(P, u), hc, hd, hl, sd=(.2, .5), sw=sw * .85, curv=True, opL=150)
    if wet > .05:
        for k, xx in enumerate((-5.0, -3.6, 3.7, 5.1) if not side else (-4.8, -3.0)):
            ph = frac(G.T * .9 + k * .37)
            paint(ellPts(xx * u, (-10.2 + ph * 2.4) * u, .18 * u, .26 * u, 8), wash='#BFE0F5', washOp=int(220 * wet * (1 - ph)), ink=None)


def _girlFront(u, sw, C, side, beanie=False):
    """bob: crown, straight-cut bangs (齐刘海) and jaw-length side hair over the ears (after the face)"""
    hc, hd, hl = C['hair'], mixCol(C['hair'], INK, .4), C['hairLt']
    if side:
        P = [[-5.0, -11.4], [-5.25, -15.6], [-3.8, -18.4], [-1.0, -19.4], [2.1, -19.1], [4.1, -17.7], [4.95, -15.6], [4.9, -15.15],
             [.6, -15.15], [.3, -14.0], [.9, -12.6], [.6, -11.0], [-.8, -10.7], [-2.6, -10.8]]
        part(_P(P, u), hc, hd, hl, sd=(.3, .3), sw=sw * .85, curv=False, opL=170)
        for k in range(4):
            xx = 1.2 + k * .95
            inkLine(_P([[xx, -17.2], [xx + .1, -15.3]], u), sw * .3, hl, 'inkfine', .3)
        return
    P = [[-5.35, -10.9], [-5.6, -13.2], [-5.35, -15.8], [-4.0, -18.3], [-1.5, -19.4], [1.5, -19.4], [4.0, -18.3], [5.35, -15.8],
         [5.6, -13.2], [5.35, -10.9], [4.45, -10.9], [4.3, -12.7], [4.32, -15.05], [-4.32, -15.05], [-4.3, -12.7], [-4.45, -10.9]]
    part(_P(P, u), hc, hd, hl, sd=(.3, .3), sw=sw * .85, curv=False, opL=170)
    for k in range(6):
        xx = -3.4 + k * 1.36
        inkLine(_P([[xx * .8, -17.6], [xx, -15.25]], u), sw * .3, hl, 'inkfine', .3)
    for s_ in (-1, 1):
        inkLine(_P([[s_ * 4.95, -14.6], [s_ * 5.05, -11.4]], u), sw * .3, hl, 'inkfine', .4)


def _beanie(u, sw, C, side):
    if side:
        cap = [[-5.3, -15.6], [-4.6, -18.6], [-1.6, -20.2], [1.8, -20.0], [4.3, -18.4], [5.0, -15.8]]
        band = [[-5.45, -16.4], [5.15, -16.4], [5.25, -15.0], [-5.55, -15.0]]
        px = -.2
    else:
        cap = [[-5.25, -15.9], [-4.6, -18.7], [-2.2, -20.3], [2.2, -20.3], [4.6, -18.7], [5.25, -15.9]]
        band = [[-5.45, -16.6], [5.45, -16.6], [5.6, -15.0], [-5.6, -15.0]]
        px = 0
    part(_P(cap, u), C['beanie'], C['beanieDk'], None, sd=(.3, .4), sw=sw * .85)
    for k in range(5):
        xx = -3.2 + k * 1.6
        inkLine(_P([[xx * .9, -19.6], [xx, -16.8]], u), sw * .3, C['beanieDk'], 'inkfine', .3)
    part(_P(band, u), mixCol(C['beanie'], C['beanieDk'], .3), C['beanieDk'], None, sw=sw * .8, curv=False)
    for k in range(9):
        xx = -4.8 + k * 1.2
        inkLine(_P([[xx, -16.4], [xx, -15.2]], u), sw * .28, C['beanieDk'], 'inkfine', 0)
    part(ellPts(px * u, -20.7 * u, 1.25 * u, 1.15 * u, 16), C['pom'], C['beanieDk'], None, sw=sw * .7)


# ---------------------------------------------------------------- torso
def _torsoBoy(u, sw, C, side, back):
    """navy pullover hoodie: hood lying behind the neck, cream drawstrings, kangaroo pocket, ribbed hem"""
    if side:
        coat = [[-1.9, -10.5], [1.9, -10.5], [2.5, -9.6], [2.8, -4.2], [0, -4.15], [-2.65, -4.2], [-2.55, -9.6]]
    else:
        coat = [[-2.2, -10.5], [2.2, -10.5], [3.0, -9.9], [3.25, -8.8], [3.4, -4.2], [0, -4.15], [-3.4, -4.2], [-3.25, -8.8], [-3.0, -9.9]]
    part(_P(coat, u), C['coat'], C['coatDk'], C['coatLt'], sd=(.65, .35), sw=sw)
    hx = (-2.65, 2.8) if side else (-3.4, 3.4)
    paint(_P([[hx[0] + .05, -4.9], [hx[1] - .05, -4.9], [hx[1], -4.2], [hx[0], -4.2]], u), fill=C['coatDk'], fillOp=160, bleed=.05, ink=None)
    inkLine(_P([[hx[0] + .1, -4.9], [hx[1] - .1, -4.9]], u), sw * .45, INK, 'inkfine', 0)
    if back:
        hood = [[-2.5, -10.7], [2.5, -10.7], [2.7, -9.1], [1.7, -7.7], [0, -7.3], [-1.7, -7.7], [-2.7, -9.1]]
        part(_P(hood, u), mixCol(C['coat'], C['coatDk'], .2), C['coatDk'], None, sd=(0, .6), sw=sw * .8)
        inkLine(_P([[-1.7, -9.9], [0, -8.8], [1.7, -9.9]], u), sw * .45, INK, 'inkfine', .5)
    elif side:
        hood = [[-1.9, -10.7], [-.4, -10.6], [-.9, -9.2], [-2.2, -8.4], [-3.05, -9.2], [-2.9, -10.3]]
        part(_P(hood, u), mixCol(C['coat'], C['coatDk'], .2), C['coatDk'], None, sd=(-.4, .4), sw=sw * .8)
        inkLine(_P([[1.6, -10.3], [1.75, -8.2]], u), sw * .6, C['string'], 'inkfine', .3)
        paint(_P([[.5, -7.3], [2.6, -7.3], [2.7, -5.2], [.6, -5.2]], u), fill=C['coatDk'], fillOp=120, ink=INK, sw=sw * .4)
    else:
        rim = [[-2.6, -10.75], [-1.2, -11.0], [1.2, -11.0], [2.6, -10.75], [2.4, -10.0], [1.0, -9.85], [-1.0, -9.85], [-2.4, -10.0]]
        part(_P(rim, u), mixCol(C['coat'], C['coatDk'], .25), C['coatDk'], None, sd=(0, .5), sw=sw * .65)
        for s_ in (-1, 1):
            inkLine(_P([[s_ * .7, -10.0], [s_ * .82, -7.6]], u), sw * .7, C['string'], 'inkfine', .2)
            paint(ellPts(s_ * .83 * u, -7.45 * u, .18 * u, .24 * u, 8), wash=C['string'], ink=INK, sw=sw * .3)
        pk = [[-2.1, -7.0], [2.1, -7.0], [2.6, -5.2], [-2.6, -5.2]]
        part(_P(pk, u), mixCol(C['coat'], C['coatDk'], .15), C['coatDk'], None, sd=(0, .6), sw=sw * .55, curv=False, opD=70)


def _torsoGirl(u, sw, C, side, back):
    """cream sweater (ribbed hem and cuffs) over a short purple-grey A-line skirt"""
    if side:
        sk = [[-2.3, -5.4], [2.4, -5.4], [3.1, -3.35], [-3.0, -3.35]]
        sw_ = [[-1.85, -10.5], [1.85, -10.5], [2.4, -9.5], [2.55, -5.0], [0, -4.95], [-2.45, -5.0], [-2.45, -9.5]]
    else:
        sk = [[-2.9, -5.4], [2.9, -5.4], [3.85, -3.4], [0, -3.3], [-3.85, -3.4]]
        sw_ = [[-2.15, -10.5], [2.15, -10.5], [2.95, -9.9], [3.2, -8.7], [3.25, -5.0], [0, -4.95], [-3.25, -5.0], [-3.2, -8.7], [-2.95, -9.9]]
    part(_P(sk, u), C['skirt'], C['skirtDk'], None, sd=(.5, .5), sw=sw * .85, curv=False)
    if not side:
        for k in (-1.6, 0, 1.6):
            inkLine(_P([[k * .9, -5.0], [k * 1.15, -3.5]], u), sw * .35, C['skirtDk'], 'inkfine', 0)
    part(_P(sw_, u), C['coat'], C['coatDk'], C['coatLt'], sd=(.65, .35), sw=sw)
    hx = (-2.45, 2.55) if side else (-3.25, 3.25)
    paint(_P([[hx[0] + .05, -5.6], [hx[1] - .05, -5.6], [hx[1], -4.95], [hx[0], -4.95]], u), fill=C['coatDk'], fillOp=120, bleed=.05, ink=None)
    for k in range(9 if not side else 6):
        xx = lerp(hx[0] + .3, hx[1] - .3, k / (8 if not side else 5))
        inkLine(_P([[xx, -5.55], [xx, -5.05]], u), sw * .28, C['coatDk'], 'inkfine', 0)
    if not side and not back:
        for k in range(3):
            yy = -9.2 + k * 1.2
            inkLine(_P([[-1.6, yy], [-1.2, yy + .35], [-.8, yy]], u), sw * .3, C['coatDk'], 'inkfine', .4)
            inkLine(_P([[.8, yy], [1.2, yy + .35], [1.6, yy]], u), sw * .3, C['coatDk'], 'inkfine', .4)


def _guitar(u, sw, C, view, front_layer):
    """dark-brown guitar case slung on his back (strap across the chest in front view)"""
    if view == 'side':
        if front_layer:
            inkLine(_P([[-.6, -10.2], [1.9, -7.4]], u), sw * 1.1, C['strap'], 'ink', .2)
            return
        push()
        translate(-2.3 * u, -8.2 * u)
        rotate(-.32)
        body = [[-1.3, -6.2], [-.7, -7.0], [.7, -7.0], [1.3, -6.2], [1.15, -3.2], [1.9, -1.8], [2.0, 1.4], [1.0, 3.0], [-1.0, 3.0], [-2.0, 1.4], [-1.9, -1.8], [-1.15, -3.2]]
        part(_P(body, u), C['case'], C['caseDk'], C['caseLt'], sd=(.5, .3), sw=sw * .8)
        pop()
        return
    if view == 'back':
        push()
        translate(.6 * u, -8.0 * u)
        rotate(-.18)
        body = [[-1.1, -6.6], [-.6, -7.4], [.6, -7.4], [1.1, -6.6], [1.0, -3.4], [1.9, -1.9], [2.05, 1.6], [1.1, 3.3], [-1.1, 3.3], [-2.05, 1.6], [-1.9, -1.9], [-1.0, -3.4]]
        part(_P(body, u), C['case'], C['caseDk'], C['caseLt'], sd=(.5, .3), sw=sw * .8)
        inkLine(_P([[-1.5, -.5], [1.5, -.5]], u), sw * .4, C['caseLt'], 'inkfine', 0)
        pop()
        return
    if front_layer:
        inkLine(_P([[2.2, -10.3], [.6, -8.6], [-2.6, -5.4]], u), sw * 1.15, C['strap'], 'ink', .3)
        return
    push()
    translate(-3.4 * u, -9.0 * u)
    rotate(-.2)
    body = [[-1.0, -7.0], [-.5, -7.8], [.5, -7.8], [1.0, -7.0], [.95, -3.6], [1.7, -2.2], [1.85, 1.2], [.9, 2.8], [-.9, 2.8], [-1.85, 1.2], [-1.7, -2.2], [-.95, -3.6]]
    part(_P(body, u), C['case'], C['caseDk'], C['caseLt'], sd=(.5, .3), sw=sw * .8)
    pop()


def _scarfBand(u, sw, kind, side):
    col, dk, lt = SCARF[kind]
    g0 = ellPts((.15 if side else 0) * u, -10.4 * u, 2.45 * u, .9 * u, 18)
    part(g0, col, dk, lt, sd=(.3, .6), sw=sw * .75)
    for k in range(4):
        xx = -1.6 + k * 1.05
        inkLine(_P([[xx, -10.9], [xx + .15, -9.9]], u), sw * .28, dk, 'inkfine', .2)


def _scarfTail(u, sw, kind, side, t=0.0, wind=0.0):
    col, dk, lt = SCARF[kind]
    sway = math.sin(t * 2.2) * .25 + wind
    if side:
        P = [[-1.2, -10.3], [-.2, -10.2], [-.9 - sway * 1.2, -7.0], [-1.9 - sway * 1.6, -6.7]]
    else:
        P = [[-1.7, -10.0], [-.5, -9.9], [-.75 + sway * .3, -6.6], [-1.95 + sway * .3, -6.75]]
    part(_P(P, u), col, dk, lt, sd=(.3, .5), sw=sw * .7, curv=False)
    a, b = P[3], P[2]
    for k in range(4):
        q = k / 3
        x, y = lerp(a[0], b[0], q), lerp(a[1], b[1], q)
        inkLine(_P([[x, y], [x + .05, y + .55]], u), sw * .4, dk, 'inkfine', 0)


# ---------------------------------------------------------------- the character
def person(x, y, u, o, C, boy):
    LITE[0] = o.get('lite', u < 12)
    view = o.get('view', 'front')
    side = view == 'side'
    back = view == 'back'
    sw = clamp(u / 15, .45, 2.6) * o.get('swMul', 1)
    ex = o.get('ex', {})
    legs = o.get('legs', 'stand')
    ph = o.get('ph', 0.0)
    wet = o.get('wet', 0.0)
    if wet > .01:
        C = dict(C, coat=mixCol(C['coat'], C['coatDk'], .45 * wet), hair=mixCol(C['hair'], INK, .2 * wet))
    boilSeed(f"{C['name']} {o.get('key', 0)}")
    if o.get('shadow', True):
        paint(ellPts(x, y + u * .1, u * (4.4 if not side else 3.8), u * .72, 20), fill=INK, fillOp=o.get('shadowOp', 70), bleed=.3, border=.1, ink=None)
    push()
    translate(x, y)
    if o.get('rot'):
        rotate(o['rot'])
    if o.get('flip'):
        scale(-1, 1)
    sq = o.get('sq', 0)
    if sq:
        scale(1 + sq * .5, 1 - sq)
    bob = o.get('bob', 0)
    run = legs == 'run'
    if run:
        bob += -abs(math.sin(ph * TAU)) * .6
    elif legs == 'walk':
        bob += -abs(math.sin(ph * TAU)) * .22
    sitDrop = 1.5 if legs == 'sit' else 0
    boot = not boy

    # long hair behind everything
    if not boy and not back:
        push()
        translate(0, (bob + sitDrop) * u)
        _girlBack(u, sw, C, side, wet)
        pop()

    # legs + shoes
    top = -4.5 if boy else -3.7
    guitar = boy and o.get('guitar')
    if guitar and not back:
        push()
        translate(0, (bob + sitDrop) * u)
        _guitar(u, sw, C, view, False)
        pop()
    if not side:
        for s in (-1, 1):
            if legs == 'sit':
                _leg(s * 1.4, -2.6, s * 1.4, -1.0, u, sw, C)
                part(ellPts(s * 1.45 * u, -2.75 * u, 1.3 * u, .95 * u, 16), C['pants'], C['pantsDk'], None, sd=(0, .7), sw=sw * .65)
                _shoe(s * 1.35, u, sw, C, boot=boot)
                continue
            lift = 0
            if legs in ('walk', 'run'):
                lift = max(0, math.sin((ph + (0 if s < 0 else .5)) * TAU)) * (.7 if legs == 'walk' else 1.2)
            _leg(s * 1.32, top + bob * .5, s * 1.32, -1.0 - lift, u, sw, C)
            _shoe(s * 1.32, u, sw, C, oy=-lift, boot=boot)
    else:
        if legs == 'sit':
            d = sitDrop + bob
            hip, knee, ank = [.4, -3.3], [2.9, -3.45], [3.0, -1.0]
            _leg(knee[0], knee[1], ank[0], ank[1], u, sw, C, 1.15)
            _shoe(0, u, sw, C, side=True, ox=ank[0] - .1, oy=0, toe=.9, boot=boot)
            th = ribbon(_P([[hip[0] - 1.2, hip[1]], hip, knee], u), 2.0 * u, 1.6 * u)
            part(th, C['pants'] if boy else C['skirt'], C['pantsDk'] if boy else C['skirtDk'], None, sd=(.2, .6), sw=sw * .8, curv=False)
        else:
            for i in (0, 1):
                if legs in ('walk', 'run'):
                    amp = .42 if legs == 'walk' else .8
                    a = math.sin((ph + (0 if i == 0 else .5)) * TAU) * amp
                else:
                    a = [.04, -.04][i]
                Cl = C if i else dict(C, pants=mixCol(C['pants'], C['pantsDk'], .4), shoe=mixCol(C['shoe'], C['shoeDk'], .35))
                push()
                translate((-.3 + i * .6) * u, (top + .5 + bob) * u)
                rotate(-a)
                lift = 0
                if run and a < 0:
                    lift = -a * .9
                L = -top - .5 - (1.0 if boy else 1.8)
                _leg(0, -.5, 0, L, u, sw, Cl)
                _shoe(0, u, sw, Cl, side=True, ox=.35, oy=L + (1.0 if boy else 1.8), rot=lift, boot=boot)
                pop()

    push()
    translate(0, (bob + sitDrop) * u)
    hands = o.get('hands', {})
    if side:
        Hfar = hands.get('L', [-1.0, -5.4] if not run else [-2.4 + 1.6 * math.sin(ph * TAU), -7.0])
        if legs == 'walk' and 'L' not in hands:
            Hfar = [-.6 - 1.4 * math.sin(ph * TAU), -5.6]
        _arm([-.3, -9.5], Hfar, u, sw, C, bend=o.get('bendL', 1), far=True, item=o.get('itemL'))

    if boy:
        _torsoBoy(u, sw, C, side, back)
    else:
        _torsoGirl(u, sw, C, side, back)
    if guitar and back:
        _guitar(u, sw, C, view, False)
    elif guitar:
        _guitar(u, sw, C, view, True)
    scarf = o.get('scarf', C.get('scarf'))
    if scarf and not back:
        _scarfBand(u, sw, scarf, side)

    # head
    hd = -14.55
    if not side and boy:
        for s in (-1, 1):
            part(ellPts(s * 4.5 * u, -13.85 * u, .62 * u, .88 * u, 12), C['skin'], C['skinDk'], None, sd=(s * .5, .2), sw=sw * .7)
    headPts = []
    for i in range(36):
        a = i / 36 * TAU
        rx = 4.72 if math.sin(a) < 0 else 4.72 - .3 * math.sin(a) ** 2
        headPts.append([(math.cos(a) * rx + (.25 if side else 0)) * u, (hd + math.sin(a) * 4.3) * u])
    if back:
        part(headPts, C['hair'], mixCol(C['hair'], INK, .4), C['hairLt'], sd=(.2, .6), sw=sw, curv=False, opL=190)
        for k in range(7):
            xx = -3.0 + k
            inkLine(_P([[xx * .9, -16.2], [xx * 1.05, -12.4 - abs(xx) * .25]], u), sw * .32, C['hairLt'], 'inkfine', .4)
        if boy:
            tuft = [[-3.6, -11.9], [-2.6, -10.9], [-1.8, -11.6], [-.9, -10.7], [0, -11.5], [.9, -10.7], [1.8, -11.6], [2.6, -10.9], [3.6, -11.9]]
            inkLine(_P(tuft, u), sw * .6, INK, 'ink', .2)
            for s in (-1, 1):
                part(ellPts(s * 4.55 * u, -13.6 * u, .55 * u, .82 * u, 12), C['skin'], C['skinDk'], None, sw=sw * .7)
        else:
            P = [[-5.2, -15.4], [-5.75, -13.0], [-5.85, -11.3], [-5.0, -10.5], [5.0, -10.5], [5.85, -11.3], [5.75, -13.0], [5.2, -15.4],
                 [3.6, -18.4], [0, -19.4], [-3.6, -18.4]]
            part(_P(P, u), C['hair'], mixCol(C['hair'], INK, .4), C['hairLt'], sd=(.2, .5), sw=sw * .85, curv=True, opL=150)
            for k in range(6):
                xx = -3.6 + k * 1.45
                inkLine(_P([[xx * .7, -17.0], [xx, -11.2]], u), sw * .3, C['hairLt'], 'inkfine', .4)
            if o.get('beanie'):
                _beanie(u, sw, C, False)
    else:
        part(headPts, C['skin'], C['skinDk'], C['skinLt'], sd=(.55 if not side else -.6, .45), sw=sw, curv=False, opD=70, opL=120)
        if side and boy:
            part(ellPts(-.05 * u, -13.65 * u, .58 * u, .8 * u, 12), mixCol(C['skin'], C['blush'], .18), C['skinDk'], None, sd=(-.4, .2), sw=sw * .7)
        face(u, sw, C, o, ex, side)
        if boy:
            _boyTop(u, sw, C, side)
            if C.get('glasses'):
                glasses(u, sw, C, side)
        else:
            _girlFront(u, sw, C, side, o.get('beanie'))
            if o.get('beanie'):
                _beanie(u, sw, C, side)
        if wet > .05:
            for k, xx in enumerate((-3.5, -1.2, 1.5, 3.8) if not side else (2.0, 3.6)):
                ph2 = frac(G.T * 1.1 + k * .29)
                paint(ellPts(xx * u, (-15.2 + ph2 * 3.0) * u, .16 * u, .24 * u, 8), wash='#BFE0F5', washOp=int(220 * wet * (1 - ph2)), ink=None)
    if scarf and not back:
        _scarfTail(u, sw, scarf, side, G.T, o.get('wind', 0))
    if o.get('mid'):
        o['mid'](u, sw)          # held object between the body and the hands (guitar, case, box): hands are drawn over it

    # near arms
    if side:
        Hn = hands.get('R', [1.15, -5.3] if not run else [1.2 - 1.8 * math.sin(ph * TAU), -7.2])
        if legs == 'walk' and 'R' not in hands:
            Hn = [.9 + 1.4 * math.sin(ph * TAU), -5.5]
        _arm([.6, -9.5], Hn, u, sw, C, bend=o.get('bendR', 1), item=o.get('itemR'))       # side view: elbow down by default (user 2026-11-04: elbow-up arms read as a hand under the chin)
    else:
        for s, k in ((-1, 'L'), (1, 'R')):
            Hd = hands.get(k, [s * 3.8, -5.3])
            _arm([s * 2.75, -9.55], Hd, u, sw, C, bend=1 if s < 0 else -1, item=o.get('item' + k))
    if o.get('over'):
        o['over'](u, sw)
    pop()
    pop()


def jhim(x, y, u, o=None):
    o = dict(o or {})
    person(x, y, u, o, o.get('C', HIM), True)


def jher(x, y, u, o=None):
    o = dict(o or {})
    person(x, y, u, o, o.get('C', HER), False)


def handPos(x, y, u, o, side='R'):
    """world position of a hand given o['hands'] (default rest pose); matches person()"""
    legs = o.get('legs', 'stand')
    sd = 1.5 if legs == 'sit' else 0
    view = o.get('view', 'front')
    hands = o.get('hands', {})
    if view == 'side':
        h = hands.get(side, [1.15, -5.3] if side == 'R' else [-1.0, -5.4])
    else:
        h = hands.get(side, [3.8 if side == 'R' else -3.8, -5.3])
    f = -1 if o.get('flip') else 1
    return x + f * h[0] * u, y + (h[1] + sd + o.get('bob', 0)) * u
