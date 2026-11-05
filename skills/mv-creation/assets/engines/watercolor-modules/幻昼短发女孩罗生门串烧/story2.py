# story2.py: 《幻昼+短发女孩+罗生门》串烧 shots S07–S11 (night half: his room, his phone). One shot per bar.
import math
from eng import *
import eng
from clawd import *
from props import bubble, stamp, sparkle, sparkles, impactLines, puff, floatHearts
from sets2 import seat, bookshelf
from props_bingbian import wallpaper, woodFloor, bedBack, blanket
from bbset import wallClock2, calendar, wallFrames, plant, rug, stringLights, bedsideTable, pillowProp
from common import *
from mz import *
import mz
import nm


def _todo(col, label):
    def f(t, lt, dur):
        flatRect(-300, -300, W + 600, H + 600, col)
        text(label, 960, 500, 90, INK, shadow=False)
    return f


BED = dict(x=1000, y=900, w=1120, s=30)
MATTOP = BED['y'] - 4.2 * BED['s']


def hisRoom(t, lights=1.0, hh=11, mm=0, key='rm', pillows=True):
    """his bedroom at night, no window: wallpaper, wall clock, calendar, frames, bookshelf, string lights, bed, bedside table, plant"""
    wallpaper('#2F3358', '#383E68', key=key + 'wp')
    wallClock2(960, 205, 50, hh, mm, night=1, key=key + 'wc')
    calendar(1650, 220, .9, night=1, key=key + 'cal')
    wallFrames(1665, 520, .75, night=1, key=key + 'wfr')
    bookshelf(80, 330, 300, 420, key=key + 'bs', who='him', night=1)
    stringLights(t, 420, 1520, 330, sag=48, n=18, key=key + 'sl', on=lights)
    woodFloor(840, col='#5A4E66', dk='#3E3550', key=key + 'fl')
    rug(1000, 1010, 760, 80, night=1, key=key + 'rug')
    plant(1760, 905, .95, night=1, key=key + 'plant')
    if pillows:
        bedBack(BED['x'], BED['y'], BED['w'], BED['s'], key=key + 'bed', night=.9)
    else:
        bedBack(BED['x'], BED['y'], BED['w'], BED['s'], key=key + 'bed', night=.9)
    return MATTOP


def bedFront(key='rm'):
    blanket(BED['x'], BED['y'], BED['w'], BED['s'], key=key + 'blk', night=.9, top=MATTOP + 40)


# =====================================================================================
# S07 12.23–14.11 · 示例歌词占位文字示例 — his room at night; the 理智 card flips to 感性
def s07(t, lt, dur):
    cam(t, 960, 560, lerp(1.0, 1.05, ease(lt / dur)))
    tw = 1 + .5 * hitK(t, 29, .3)
    top = hisRoom(t, lights=min(1, tw), key='s7')
    glow(960, 205, 140, '#FFE7A0', .3 * hitK(t, 26, .5))
    if after(t, 26):
        a26 = age(t, 26) + .04
        push()
        translate(1075, 160)
        scale(backOut(clamp(a26 / .14)))
        boilSeed('s7moon')
        paint([[0, -40], [24, -20], [30, 10], [10, 34], [-20, 40], [0, 20], [6, -6]], wash='#FFE36E', ink=INK, sw=.9, curv=.6)
        pop()
        stamp('23:00', 1180, 240, 44, '#FFE36E', a26, rot=.1, life=1.6)
    bedsideTable(285, 905, 26, night=1, key='s7bst', lampOn=1, clock='up', frame='up')
    pillowProp(1230, top - 70, 230, 110, rot=.05, key='s7pr', col='#F6BCCB', night=.6)
    # him sitting on the bed; k29 hugs the pillow
    hug = popB(t, 29, .14)
    oM = emM(t, [(0, 'thinking'), (ek(28), 'shy'), (ek(29), 'happy', dict(eyes='heart', blush=1.0, emote=None))])
    oM.update(view='front')
    if hug > 0:
        oM.update(aL=-.9, aR=-.9, rot=.06 * math.sin(t * 9))
    seat(him, 820, top, 32, oM)
    bedFront('s7')
    if hug > 0:
        pillowProp(820, top - 60, 250 * (.8 + .2 * backOut(hug)), 120, rot=-.08 + .05 * math.sin(t * 9), key='s7ph', col='#BFD8EE', night=.3)
        floatHearts(t, 71, 6, 640, 380, 1000, 560, 16)
    # k27 the 理智 card pops over his head; k28 it flips to 感性
    fl = ease(clamp((t - (B[28] - .14)) / .12))
    flipSign(820, 300, 320, 120, fl, '理智', '#4F7BD8', '感性', '#FF6F96', key='s7fs', k=popB(t, 27, .14))
    if after(t, 28):
        sparkles(t, 28, 8, 620, 200, 1020, 400, 16, '#FFC2D3')


# =====================================================================================
# S08 / S09 · his phone: 编短信 → 删掉 → 我才不在乎呢 → 嘴硬
PHN = dict(cx=960, cy=458, w=500, h=810)
ACC = '#F2A65A'


def wrapText(txt, size, maxw):
    lines, cur = [], ''
    for c_ in txt:
        if textW(cur + c_, size) > maxw and cur:
            lines.append(cur)
            cur = c_
        else:
            cur += c_
    if cur:
        lines.append(cur)
    return lines


def herAvatar(x, y, r, key='hav'):
    paint(ellPts(x, y, r, r, 24), wash='#FBE3EA', ink=INK, sw=.8)
    G.c.save()
    p = skia.Path()
    p.addCircle(x, y, r - 2)
    G.c.clipPath(p, skia.ClipOp.kIntersect, True)
    herM(x, y + r * 1.25, r / 6.6, dict(view='front', noShadow=True, noLegs=True, boilKey=key, eyes='happy', mouth='smile', blush=.5, aL=-1.6, aR=-1.6))
    G.c.restore()


def chatScreen(t, sx, sy, sw_, sh, draft='', caretOn=True, sent=None, sentK=0.0, flyK=1.0, stampAge=None, draftAlpha=1.0, flyBits=None):
    flatRect(sx, sy, sw_, sh, '#F1EEF4')
    # status + top bar
    text('23:41', sx + 66, sy + 30, 24, INK, shadow=False)
    G.c.drawRoundRect(skia.Rect.MakeXYWH(sx + sw_ - 86, sy + 18, 44, 22), 5, 5, skia.Paint(AntiAlias=True, Color=skcol(INK), Style=skia.Paint.kStroke_Style, StrokeWidth=2))
    flatRect(sx + sw_ - 82, sy + 22, 18, 14, '#E0344E')
    flatRect(sx, sy + 52, sw_, 112, '#FFFFFF')
    line(sx, sy + 164, sx + sw_, sy + 164, '#D6D2DC', 1, 1.5)
    inkLine([[sx + 44, sy + 90], [sx + 28, sy + 108], [sx + 44, sy + 126]], 2.4, '#7A6E88', 'ink', 0)
    herAvatar(sx + 104, sy + 108, 36)
    text('白月光', sx + 158, sy + 108, 42, INK, align='left', shadow=False)
    boilSeed('chmoon')
    mx = sx + 158 + textW('白月光', 42) + 28
    paint([[mx, sy + 88], [mx + 14, sy + 98], [mx + 16, sy + 114], [mx + 6, sy + 126], [mx - 10, sy + 128], [mx, sy + 116], [mx + 4, sy + 102]],
          wash='#FFE36E', ink=INK, sw=.6, curv=.6)
    # history
    G.c.drawRoundRect(skia.Rect.MakeXYWH(sx + sw_ / 2 - 80, sy + 190, 160, 40), 16, 16, skia.Paint(AntiAlias=True, Color=skcol('#DCD6E4')))
    text('昨天 22:10', sx + sw_ / 2, sy + 210, 22, '#7A6E88', shadow=False, face=WENKAI)
    herAvatar(sx + 56, sy + 290, 30, key='hav2')
    boilSeed('chh1')
    paint(rrPts(sx + 100, sy + 262, 130, 62, 14), wash='#FFFFFF', ink=INK, sw=.7)
    text('晚安', sx + 165, sy + 293, 34, INK, shadow=False)
    boilSeed('chh2')
    paint(rrPts(sx + sw_ - 214, sy + 350, 150, 62, 14), wash='#FFD2A8', ink=INK, sw=.7)
    text('晚安~', sx + sw_ - 139, sy + 381, 34, INK, shadow=False)
    paint(ellPts(sx + sw_ - 34, sy + 381, 24, 24, 16), wash=ACC, ink=INK, sw=.7)
    # sent bubble (flies up from the input on k36)
    by = sy + 470
    if sent and sentK > 0:
        k = clamp(flyK)
        w = textW(sent, 36) + 44
        yy = lerp(sy + sh - 140, by, easeOut(k))
        x1 = sx + sw_ - 64
        push()
        sc = lerp(.9, 1.0, k)
        translate(x1, yy + 32)
        scale(sc)
        translate(-x1, -(yy + 32))
        boilSeed('chsent')
        paint(rrPts(x1 - w, yy, w, 64, 14), wash='#FFD2A8', ink=INK, sw=.8)
        text(sent, x1 - w / 2, yy + 32, 36, INK, shadow=False)
        pop()
        paint(ellPts(sx + sw_ - 34, by + 32, 24, 24, 16), wash=ACC, ink=INK, sw=.7)
        if k >= 1:
            text('已送达', x1 - 50, by + 92, 22, '#9A8FA8', shadow=False, face=WENKAI)
        if stampAge is not None:
            rubberStamp('嘴硬', x1 - w / 2 - 10, by + 34, 74, stampAge, col='#E0344E', rot=-.14)
    # input area
    iy = sy + sh - 220
    flatRect(sx, iy, sw_, 220, '#FAF8FC')
    line(sx, iy, sx + sw_, iy, '#D6D2DC', 1, 1.5)
    boxW = sw_ - 150
    G.c.drawRoundRect(skia.Rect.MakeXYWH(sx + 24, iy + 20, boxW, 176), 18, 18, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF')))
    G.c.drawRoundRect(skia.Rect.MakeXYWH(sx + 24, iy + 20, boxW, 176), 18, 18, skia.Paint(AntiAlias=True, Color=skcol('#C9C1D6'), Style=skia.Paint.kStroke_Style, StrokeWidth=2))
    lines = wrapText(draft, 34, boxW - 40)
    cx_, cy_ = sx + 44, iy + 62
    for i, ln in enumerate(lines[-3:]):
        text(ln, sx + 44, iy + 62 + i * 48, 34, INK, align='left', shadow=False, a=draftAlpha)
        cx_ = sx + 44 + textW(ln, 34) + 4
        cy_ = iy + 62 + i * 48
    if caretOn and math.sin(t * 14) > -.2:
        line(cx_ + 2, cy_ - 20, cx_ + 2, cy_ + 20, ACC, 1, 3)
    if flyBits:
        for i, (c_, ag) in enumerate(flyBits):
            if 0 <= ag < .6:
                ang = -1.2 - hash1(i) * 1.4
                d = 300 * easeOut(clamp(ag / .5))
                text(c_, sx + 60 + (i % 9) * 40 + math.cos(ang) * d, iy + 62 + (i // 9) * 48 + math.sin(ang) * d, 34, '#9A8FA8',
                     shadow=False, a=1 - clamp(ag / .6), rot=ag * 4 * (1 if i % 2 else -1))
    # send button
    lit = 1 if draft else .3
    boilSeed('chsend')
    paint(rrPts(sx + sw_ - 112, iy + 120, 92, 64, 16), wash=mixCol('#E8E2EE', ACC, lit), ink=INK, sw=.8)
    text('发送', sx + sw_ - 66, iy + 152, 28, '#FFFFFF' if lit > .5 else '#9A8FA8', shadow=False)


def phoneScene(t, page, jolt=(0, 0)):
    # top-down bed sheet: blue gingham, a pillow corner, a plush
    flatRect(-300, -300, W + 600, H + 600, '#BFD3EE')
    for i in range(-4, 24):
        flatRect(i * 110, -300, 55, H + 600, '#FFFFFF', .35)
    for j in range(-4, 14):
        flatRect(-300, j * 110, W + 600, 55, '#FFFFFF', .35)
    pillowProp(260, 230, 420, 260, rot=-.2, key='phpl', col='#F6BCCB', night=.1)
    stringLightsPts = [[1350, -40], [1500, 120], [1700, 160], [2000, 60]]
    import bsc
    bsc.stringLights(stringLightsPts, t, on=1, key='phsl')
    glow(PHN['cx'], PHN['cy'], 700, '#CFE6FF', .25)
    import ch_chonghuai as CH
    cx, cy, w, h = PHN['cx'] + jolt[0], PHN['cy'] + jolt[1], PHN['w'], PHN['h']
    G.c.drawRoundRect(skia.Rect.MakeXYWH(cx - w / 2 + 18, cy - h / 2 + 24, w, h), 70, 70, skia.Paint(AntiAlias=True, Color=skcol(INK, .18)))
    CH.phoneBody(cx, cy, w, h, key='phb', case=ACC)
    p, (sx, sy, sw_, sh) = CH.screenClip(cx, cy, w, h)
    G.c.save()
    G.c.clipPath(p, skia.ClipOp.kIntersect, True)
    page(sx, sy, sw_, sh)
    G.c.restore()
    return sx, sy, sw_, sh


DRAFT = [(31, '在吗'), (32, '在吗，今天的月亮好圆'), (33, '在吗，今天的月亮好圆，你睡了吗')]


def typed(t, steps, lead=.2):
    """the draft at time t: each (k, text) finishes typing on beat k (typing runs over the `lead` seconds before it)"""
    cur = ''
    for k, txt in steps:
        t0 = B[k] - lead
        if t >= B[k] - .02:
            cur = txt
        elif t >= t0:
            n0 = len(cur)
            f = (t - t0) / (lead - .02)
            cur = txt[:n0 + int((len(txt) - n0) * f)]
            break
        else:
            break
    return cur


def s08(t, lt, dur):
    cam(t, 960, 520, lerp(1.0, 1.06, ease(lt / dur)))
    on = clamp((t - (B[30] - .05)) / .08)

    def page(sx, sy, sw_, sh):
        chatScreen(t, sx, sy, sw_, sh, typed(t, DRAFT), caretOn=True)
        if on < 1:
            flatRect(sx, sy, sw_, sh, '#1C1A26', 1 - on)

    phoneScene(t, page)
    if after(t, 33):
        a33 = age(t, 33) + .04
        nm.sweatDrop(1300, 300, 40 * backOut(clamp(a33 / .14)), key='s8sw') if hasattr(nm, 'sweatDrop') else None
        stamp('编…', 1420, 250, 60, ACC, a33, rot=.1)


def s09(t, lt, dur):
    pz = easeOut(clamp((t - (B[37] - .1)) / .1))
    cam(t, lerp(960, 1080, pz), lerp(520, 470, pz), lerp(1.06, 1.1, ease(lt / dur)) + .45 * pz)
    old = DRAFT[-1][1]
    if t < B[34] - .14:
        draft, bits, alpha = old, None, 1
    else:
        a = t - (B[34] - .14)
        bits = [(c_, a - i * .006) for i, c_ in enumerate(old)]
        draft, alpha = '', 1
        draft = typed(t, [(35, '我才不在乎呢')], .22)
        if t >= B[36] - .14:
            draft = ''
    sent = '我才不在乎呢'
    fly = clamp((t - (B[36] - .14)) / .14)
    stA = (age(t, 37) + .04) if after(t, 37) else None

    def page(sx, sy, sw_, sh):
        chatScreen(t, sx, sy, sw_, sh, draft, caretOn=t < B[36] - .14, sent=sent if fly > 0 else None, sentK=fly, flyK=fly, stampAge=stA,
                   flyBits=bits)

    jolt = (8 * math.sin(t * 60) * hitK(t, 37, .1), 0)
    phoneScene(t, page, jolt)
    if after(t, 34):
        stamp('删删删', 1420, 760, 58, '#7A5AC8', age(t, 34) + .04, rot=.08, life=.9)
    if after(t, 36):
        stamp('嗖', 1400, 300, 70, ACC, age(t, 36) + .04, rot=-.1, life=.9)


# =====================================================================================
# S10 17.86–19.73 · 示例歌词占位文字示例 — he stares at the phone; a buzz… it's only the weather
def s10(t, lt, dur):
    cam(t, 960, 560, 1.0)
    top = hisRoom(t, key='s10')
    bedsideTable(285, 905, 26, night=1, key='s10bst', lampOn=1, clock='up', frame='up')
    # phone standing against the right pillow
    px, py = 1290, top - 120
    buzz = hitK(t, 39, .25)
    lit = clamp((t - (B[39] - .05)) / .06)
    nm.phoneP(px + 10 * math.sin(t * 90) * buzz, py, 190, rot=.04, lit=lit, case=ACC, key='s10ph')
    if buzz > .05:
        for s_ in (-1, 1):
            for j in range(2):
                inkLine([[px + s_ * (80 + j * 22), py - 50], [px + s_ * (92 + j * 22), py], [px + s_ * (80 + j * 22), py + 50]], 2.4, INK, 'ink', .5)
    if after(t, 39):
        stamp('嗡', px + 160, py - 140, 64, '#FFFFFF', age(t, 39) + .04, rot=.12, life=.7)
    # k40: it's the weather app
    if after(t, 40, .05):
        a40 = age(t, 40) + .05
        push()
        translate(px - 40, py - 250)
        scale(backOut(clamp(a40 / .14)))
        boilSeed('s10nt')
        paint(rrPts(-230, -62, 460, 124, 26), wash='#FFFFFF', ink=INK, sw=1.0)
        paint(ellPts(-170, 0, 34, 34, 18), wash='#FFD84A', ink=INK, sw=.8)
        for i in range(8):
            ang = i / 8 * TAU
            line(-170 + math.cos(ang) * 44, math.sin(ang) * 44, -170 + math.cos(ang) * 56, math.sin(ang) * 56, '#F2B02A', 1, 4)
        text('天气提醒', -110, -22, 28, '#9A8FA8', align='left', shadow=False)
        text('明天 晴', -110, 20, 38, INK, align='left', shadow=False)
        pop()
    # him: sitting on the bed, staring; k39 jumps; k40 deflates; k41 flops back
    flop = ease(clamp((t - (B[41] - .16)) / .16))
    oM = emM(t, [(0, 'hopeful', dict(lookX=.8)), (ek(39), 'excited'), (ek(40), 'sad', dict(emote=None)), (ek(41), 'sad', dict(eyes='closed', emote=None))])
    oM.update(view='q')
    if t > B[39] - .1 and t < B[40]:
        hop = jump(t, B[39] - .1, B[39] + .35, 2.4)
        oM['dy'] = (oM.get('dy', 0) or 0) + hop['dy']
    if flop > 0:
        oM.update(rot=-.12 * flop, sq=(oM.get('sq', 0) or 0) + .22 * flop, aL=-1.0 * flop, aR=-1.0 * flop, gloom=.5 * flop)
    seat(him, 840, top, 32, oM)
    bedFront('s10')
    if after(t, 41):
        dots3(700, 430, 70, popB(t, 41, .14), key='s10d3')
    if t < B[39] - .1:
        bubble(1060, 500, '回我?', 40, (960, 580), popB(t, 38, .14), '#FFE1EA', key='s10q')


# =====================================================================================
# S11 19.73–21.61 · 示例歌词占位文字示例 — an ice pack labelled 冷静 melts; the thermometer pegs
def s11(t, lt, dur):
    cam(t, 900, 560, 1.22)
    top = hisRoom(t, key='s11')
    bedsideTable(285, 905, 26, night=1, key='s11bst', lampOn=1, clock='up', frame='up')
    lv = steps(t, [42, 43, 44], [.25, .35, .55, 1.0], d=.12)
    thermometer(1280, top - 30, 330, lv, key='s11th', t=t)
    if after(t, 44):
        stamp('100°', 1380, top - 330, 60, '#FF4A3A', age(t, 44) + .04, rot=.12)
    oM = emM(t, [(0, 'determined'), (ek(43), 'nervous'), (ek(45), 'happy', dict(eyes='heart', blush=1.0, tint='flush', tintK=.35, emote=None))])
    oM.update(view='front', aL=-.5, aR=-.5)
    hx, u = 840, 32
    seat(him, hx, top, u, oM)
    bedFront('s11')
    # the ice pack: drops onto his head on k42, melts k43–k44, gone in a puff on k45
    headY = top - 6 * u + (oM.get('dy', 0) or 0) * u
    drop = clamp((t - (B[42] - .16)) / .16)
    melt = .45 * ease(seg(t, B[43] - .1, B[44])) + .4 * ease(seg(t, B[44], B[45] - .06))
    if t < B[45] - .04:
        iy = lerp(headY - 400, headY - 30, easeIn(drop))
        icePack(hx, iy, 150, melt, key='s11ip', rot=.06)
        if drop >= 1 and t < B[42] + .2:
            impactLines(hx, headY - 30, 120, 180, 8, t, INK, key='s11imp')
    if t > B[43] - .1:
        steamPuffs(hx, headY - 80, 120, t, clamp((t - (B[43] - .1)) / .1), key='s11st')
    if after(t, 43):
        stamp('滋滋', hx + 230, headY - 120, 52, '#FFFFFF', age(t, 43) + .04, rot=.1, life=.8)
    if after(t, 45):
        a45 = age(t, 45) + .04
        puff(hx, headY - 70, 95 * backOut(clamp(a45 / .14)) * (1 - .3 * clamp(a45)), '#FFFFFF', key='s11pf', a=1 - clamp((a45 - .25) / .35))
        stamp('噗', hx - 250, headY - 150, 70, '#FFFFFF', a45, rot=-.12)
        floatHearts(t, 45, 6, hx - 200, headY - 200, hx + 200, headY + 100, 18)
