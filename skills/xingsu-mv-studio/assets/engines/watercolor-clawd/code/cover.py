# cover.py: 3:4 title key frame (1440x1920) for 《失眠》, painted with the same engine, cast and bedroom (not a frame grab).
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eng
from eng import *
from clawd import *
from sm import *
from hl import WENKAI
from PIL import Image

CW, CH = 1080, 1440
OW, OH = 1440, 1920


def wtext(txt, x, y, size, col, a=1.0, stroke=None, strokeW=None, face=WENKAI, shadow=False):
    text(txt, x, y, size, col, face=face, stroke=stroke, strokeW=strokeW, shadow=shadow, a=a)


def make(path, t=2.0, scale_=1.0):
    ow, oh = int(OW * scale_), int(OH * scale_)
    eng.OUT_W, eng.OUT_H = ow, oh
    paper, grain = makePaper(), makeGrain()
    surf = skia.Surface(ow, oh)
    c = surf.getCanvas()
    G.c = c
    G.T = t
    G.BOILN = 5
    c.drawImage(paper, 0, 0)
    c.scale(ow / CW, oh / CH)
    gradRect(-50, -50, CW + 100, 600, ['#252C62', '#2B3168'])
    # the bedroom, set coordinates mapped into the cover
    s = .95
    push()
    translate(540 - 960 * s, 413)
    scale(s)
    bedBack(t, moonXY=(1200, 150))
    alarmClock(1250, 474, .55, '03:00', key='cvclk')
    u = 44
    gy = BED_Y + 2.5 * u
    o = dict(view='front', eyes='wide', mouth='wobble', aL=-.95, aR=-.95, noShadow=True, blush=.3, emote='sweat', emoteK=1, emoteAge=.4)
    her(960, gy, u, o)
    quilt(t)
    tangle(960, 680, 430, 165, 1.0, seed=3, sw=2.6, ring=True, avoid=(960, gy - 5.6 * u, 4.6 * u, 2.3 * u))
    yarnBall(1300, 790, 62, key='cvyb', rot=.4)
    strand([[1180, 760], [1250, 780], [1290, 790]], key='cvs')
    pop()
    # title: the knitted strip with the stitched name
    push()
    translate(540, 250)
    rotate(-.04)
    knitPiece(-370, -115, 740, 230, key='cvkp', title='失眠', titleSize=150)
    boilSeed('cvlab')
    paint(rectPts(160, 80, 190, 44), wash='#FFF6EC', ink=INK, sw=.8)
    text('Suki刘舒妤', 255, 102, 28, '#A8324A', face=WENKAI, shadow=False)
    pop()
    needle(140, 60, 330, 170)
    needle(960, 70, 760, 160, knob='#7FB8E6')
    # small label + hook
    boilSeed('cvtag')
    paint(rrPts(390, 410, 300, 56, 28), wash='#F28FB0', ink=INK, sw=1.0)
    wtext('水彩手绘 MV', 540, 438, 32, '#2B2233')
    wtext('织了 999 米围巾，他说太浪费', 540, 530, 50, '#FFF5E2', stroke='#1A1E4C', strokeW=10)
    c.resetMatrix()
    pa = skia.Paint()
    pa.setBlendMode(skia.BlendMode.kMultiply)
    c.drawImage(grain, 0, 0, skia.SamplingOptions(), pa)
    a = surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
    Image.fromarray(a[..., :3]).save(path)


if __name__ == '__main__':
    make(sys.argv[1] if len(sys.argv) > 1 else 'cover.png', scale_=float(sys.argv[2]) if len(sys.argv) > 2 else 1.0)
