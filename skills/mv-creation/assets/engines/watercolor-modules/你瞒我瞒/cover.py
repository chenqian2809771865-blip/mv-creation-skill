# cover.py: 3:4 (1440x1920) and 4:3 (1920x1440) title key frames for 《你瞒我瞒》, repainted with the same engine and cast
# (not frame grabs): the split screen from S12 — she hides her phone, he hides the magnifier — under the case-file title stamp.
# usage: python3 code/cover.py out_dir [scale]
import sys, math, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import eng
from eng import *
from clawd import *
from props import sparkle, yiyun
from hl import WENKAI
from nm import *
from common import rubberStamp
from PIL import Image


def wt(txt, x, y, size, col, a=1.0, stroke=None, strokeW=None, face=WENKAI):
    text(txt, x, y, size, col, face=face, stroke=stroke, strokeW=strokeW, shadow=False, a=a)


def scene(CW, CH, u, gy, cx_her, cx_him, mid):
    """the split backdrop and the two of them; mid = divider x"""
    flatRect(-50, -50, mid + 50, CH + 100, '#F7C6D2')
    for i in range(-2, 40):
        for j in range(-2, 40):
            G.c.drawCircle(i * 70 + (35 if j % 2 else 0), j * 70, 10, skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .55)))
    G.c.save()
    G.c.clipRect(skia.Rect.MakeXYWH(mid, -50, CW, CH + 100))
    flatRect(mid, -50, CW, CH + 100, '#BFE3F5')
    for i in range(0, 40):
        G.c.drawRect(skia.Rect.MakeXYWH(mid + i * 80, -50, 36, CH + 100), skia.Paint(AntiAlias=True, Color=skcol('#FFFFFF', .4)))
    G.c.restore()
    flatRect(-50, gy, mid + 50, CH, '#E27A92')
    flatRect(mid, gy, CW, CH, '#7FA8D0')
    inkLine([[-50, gy], [CW + 50, gy]], 1.0, INK, 'ink', 0)
    # her: phone glowing behind her back, side-eye towards him
    glow(cx_her - 4.8 * u, gy - 4.4 * u, 5.5 * u, '#BDEBFF', .7)
    phoneP(cx_her - 5.3 * u, gy - 4.4 * u, 2.7 * u, -.5, lit=1.0, key='cvph')
    her(cx_her, gy, u, dict(HER, view='front', eyes='narrow', mouth='smile', blush=.5, lookX=1, aL=-.9, aR=-.9, emote='sweat', emoteK=1,
                             emoteAge=.4, boilKey='cvh'))
    # him: magnifier peeking out behind his shoulder, side-eye towards her
    magnifierW(cx_him + 4.0 * u, gy - 3.0 * u, -.85, 1.6 * u, key='cvmg', glint=.8)
    him(cx_him, gy, u, dict(ME, view='front', eyes='narrow', mouth='smile', blush=.3, lookX=-1, aL=-.9, aR=-.9, hat='deer', emote='sweat',
                            emoteK=1, emoteAge=.4, boilKey='cvm'))
    boilSeed('cvsplit')
    inkLine([[mid, -50], [mid, gy]], 4.0, INK, 'ink', 0)


def titleBlock(x, y, s):
    """manila label strip + the red rubber-stamp title + credit line"""
    push()
    translate(x, y)
    rotate(-.03)
    boilSeed('cvlab')
    paint(rectPts(-330 * s, -120 * s, 660 * s, 240 * s), wash=MANILA, fill=MANILADK, fillOp=50, ink=INK, sw=1.2)
    paint([[-300 * s, -120 * s], [-280 * s, -160 * s], [-80 * s, -160 * s], [-60 * s, -120 * s]], wash=MANILA, ink=INK, sw=1.0)
    text('档案 No.0520', -180 * s, -140 * s, 26 * s, '#6A4A2A', shadow=False)
    pop()
    rubberStamp('你瞒我瞒', x, y - 4 * s, 150 * s, 9.0, col=REDINK, rot=-.1)
    paperclip(x + 300 * s, y - 150 * s, 30 * s, .15)


def make(path, CW, CH, scale_=1.0):
    ow, oh = int(CW * 1440 / min(CW, CH) * scale_), int(CH * 1440 / min(CW, CH) * scale_)
    eng.OUT_W, eng.OUT_H = ow, oh
    paper, grain = makePaper(), makeGrain()
    surf = skia.Surface(ow, oh)
    c = surf.getCanvas()
    G.c = c
    G.T = 2.0
    G.BOILN = 5
    c.drawImage(paper, 0, 0)
    c.scale(ow / CW, oh / CH)
    if CH > CW:          # 3:4 portrait, logical 1080 x 1440; bottom sixth (y > 1200) left to the floor
        gy = 1130
        scene(CW, CH, 30, gy, 285, 795, 540)
        yiyun(795, 700, 40, 2.0, seed=4, k=1.0)
        heartP(285, 720, 30, key='cvh3')
        titleBlock(540, 250, 1.0)
        wt('陈柏宇', 540, 432, 46, '#2B2233', stroke='#FFF5E2', strokeW=8)
        boilSeed('cvtag')
        paint(rrPts(330, 474, 420, 58, 29), wash='#FFF5E2', ink=INK, sw=1.0)
        wt('疑心病男女主 · 水彩手绘 MV', 540, 503, 26, '#2B2233')
        wt('示例歌词占位文字示例', 540, 600, 60, '#FFFFFF', stroke=INK, strokeW=10)
        heartP(150, 600, 26, key='cvh1')
        heartP(930, 600, 26, key='cvh2')
    else:                # 4:3 landscape, logical 1440 x 1080; bottom sixth (y > 900) left to the floor
        gy = 860
        scene(CW, CH, 26, gy, 430, 1010, 720)
        yiyun(1230, 600, 34, 2.0, seed=4, k=1.0)
        heartP(430, 590, 26, key='cvh3')
        titleBlock(720, 200, .95)
        wt('陈柏宇', 720, 370, 44, '#2B2233', stroke='#FFF5E2', strokeW=8)
        boilSeed('cvtag')
        paint(rrPts(515, 406, 410, 56, 28), wash='#FFF5E2', ink=INK, sw=1.0)
        wt('疑心病男女主 · 水彩手绘 MV', 720, 434, 25, '#2B2233')
        wt('示例歌词占位文字示例', 720, 500, 54, '#FFFFFF', stroke=INK, strokeW=9)
    c.resetMatrix()
    pa = skia.Paint()
    pa.setBlendMode(skia.BlendMode.kMultiply)
    c.drawImage(grain, 0, 0, skia.SamplingOptions(), pa)
    a = surf.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)
    Image.fromarray(a[..., :3]).save(path)


if __name__ == '__main__':
    od = sys.argv[1] if len(sys.argv) > 1 else '.'
    sc = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    make(os.path.join(od, '你瞒我瞒_封面_3x4.png'), 1080, 1440, sc)
    make(os.path.join(od, '你瞒我瞒_封面_4x3.png'), 1440, 1080, sc)
