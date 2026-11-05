# -*- coding: utf-8 -*-
"""午夜的上海街：世界坐标矢量场景，任意缩放直接光栅到像素网格（沿用《下雨了》street.py 的做法）。
世界 x 0..1700，人行道顶 y=262，路沿 284-287，下面是马路。
从左到右：石库门弄堂口(安和里) / 理发店 / 咖啡馆 / 舞厅 / 午夜场影院(钟、翻牌招牌、雨棚) / 海报墙+公交站 / 骑楼小店 / 路口。
静态部分按 (z, cam_y, variant, state) 缓存；招牌灯泡、翻牌字、跑马灯、钟针、霓虹闪烁、理发柱每帧叠加。"""
import numpy as np, math
from core import *

GY, CURB0, CURB1 = 262, 284, 287
WORLD_W = 1700
LAMPS = [24, 300, 646, 1046, 1316, 1612]
CIN = dict(x0=700, x1=1010, mx0=735, mx1=975, my0=104, my1=174, clock=(855, 60, 19))

SKY = {
    'night': [C('#100f24'), C('#15142c'), C('#1b1934'), C('#221f3d'), C('#2a2546'), C('#352c50')],
    'memory': [C('#5a4268'), C('#7a5272'), C('#9a6276'), C('#bd7676'), C('#dc8c74'), C('#f0a678')],
    'dusk': [C('#2a2a52'), C('#3a3460'), C('#54406a'), C('#72506e'), C('#946070'), C('#b47470')],
}


def grade(img, variant):
    if variant == 'memory':
        out = img * np.array([1.40, 1.08, 0.86], np.float32) + np.array([24, 10, 0], np.float32)
    elif variant == 'dusk':
        out = img * np.array([1.12, 0.98, 1.0], np.float32) + np.array([12, 4, 8], np.float32)
    else:
        out = img
    return np.clip(out, 0, 255)


class ShStreet:
    def __init__(self):
        self._cache = {}

    def strip(self, z, cam_y, variant='night', state=None, hh=None):
        hh = H if hh is None else hh
        st = dict(salon=1, cafe=1, dance=1, cinema=1.0, shops=0, apt=0.45, poster=1)
        if state:
            st.update(state)
        key = (round(z, 3), round(cam_y, 2), variant, tuple(sorted(st.items())), hh)
        if key in self._cache:
            return self._cache[key]
        if len(self._cache) > 8:
            self._cache.pop(next(iter(self._cache)))
        Wp = int(WORLD_W * z) + 2
        T = lambda x, y: (x * z, (y - cam_y) * z)
        img = np.zeros((hh, Wp, 3), np.float32)
        sky = SKY[variant]
        vgrad_bands(img, 0, hh, sky[0], sky[-1], len(sky))
        im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
        d = ImageDraw.Draw(im)
        lw = max(1, int(round(z)))

        def R(x0, y0, x1, y1, c):
            a, b = T(x0, y0); cc, dd = T(x1, y1)
            if round(cc) - 1 < round(a) or round(dd) - 1 < round(b):
                return
            d.rectangle([round(a), round(b), round(cc) - 1, round(dd) - 1], fill=tuple(int(v) for v in c))

        def PG(pts, c):
            d.polygon([tuple(round(v) for v in T(x, y)) for x, y in pts], fill=tuple(int(v) for v in c))

        def LN(pts, c, w=None):
            d.line([tuple(round(v) for v in T(x, y)) for x, y in pts], fill=tuple(int(v) for v in c), width=w or lw)

        def ELL(cx, cy, rx, ry, c):
            a, b = T(cx - rx, cy - ry); cc, dd = T(cx + rx, cy + ry)
            if round(cc) - 1 < round(a) or round(dd) - 1 < round(b):
                return
            d.ellipse([round(a), round(b), round(cc) - 1, round(dd) - 1], fill=tuple(int(v) for v in c))

        texts, emis, lit, streaks = [], [], [], []

        # ---- far skyline (static backdrop, includes a pearl-tower-ish spire far away) ----
        rng = np.random.default_rng(11)
        x = -20
        while x < WORLD_W + 40:
            bw = int(rng.integers(36, 100)); top = int(rng.integers(-70, 30))
            R(x, top, x + bw, GY, (34, 30, 56))
            for yy in range(top + 8, 150, 13):
                for xx in range(x + 5, x + bw - 5, 11):
                    if rng.random() < 0.12:
                        R(xx, yy, xx + 4, yy + 5, (150, 118, 96) if rng.random() < 0.7 else (100, 118, 150))
            x += bw + int(rng.integers(0, 14))

        def windows(x0, x1, rows, ww=24, wh=28, litp=0.35, seed=0, frame=(34, 32, 48)):
            r = np.random.default_rng(seed)
            n = max(1, int((x1 - x0 - 12) // (ww + 14)))
            gap = ((x1 - x0) - n * ww) / (n + 1)
            for ry in rows:
                for i in range(n):
                    wx = x0 + gap + i * (ww + gap)
                    R(wx - 2, ry - 2, wx + ww + 2, ry + wh + 3, frame)
                    R(wx, ry, wx + ww, ry + wh, (30, 32, 50))
                    if r.random() < litp * st['apt'] / 0.45:
                        c = (236, 176, 104) if r.random() < 0.75 else (150, 186, 212)
                        lit.append((wx, ry, wx + ww, ry + wh, c))
                        if r.random() < 0.5:
                            lit.append((wx + ww * 0.55, ry, wx + ww, ry + wh, tuple(int(v * 0.72) for v in c)))
                    else:
                        R(wx, ry, wx + ww * 0.5, ry + wh, (38, 40, 60))
                    if z >= 1.3:
                        LN([(wx + ww / 2, ry), (wx + ww / 2, ry + wh)], (40, 40, 58))
                    R(wx - 3, ry + wh + 2, wx + ww + 3, ry + wh + 5, (84, 84, 104))

        def cornice(x0, x1, y, c=(92, 90, 112)):
            R(x0 - 3, y, x1 + 3, y + 5, c)
            R(x0 - 3, y + 5, x1 + 3, y + 7, (38, 38, 54))

        def text(s_, wx, wy, col, sc=1, ol=None, vertical=False):
            texts.append((s_, wx, wy, col, sc, ol, vertical))

        # ---- B0 filler ----
        R(-20, -60, 40, GY, (50, 50, 72))
        windows(-20, 40, [-30, 30, 90], seed=20)
        # ---- B1 石库门 row with stone gate (安和里) ----
        R(40, 30, 230, GY, (96, 56, 52))            # red brick
        if z >= 1.0:
            for yy in range(34, GY, 6):
                LN([(40, yy), (230, yy)], (86, 50, 48))
        cornice(40, 230, 30, (120, 104, 98))
        windows(40, 230, [52, 112], ww=22, wh=30, litp=0.5, seed=21, frame=(70, 60, 64))
        R(86, 150, 184, GY, (132, 124, 116))        # stone frame
        PG([(80, 150), (190, 150), (176, 132), (94, 132)], (140, 132, 122))
        PG([(110, 132), (160, 132), (135, 118)], (140, 132, 122))
        R(96, 160, 174, GY, (22, 20, 30))           # lane mouth (dark)
        # deep lane perspective: far lamp + walls
        PG([(96, 160), (122, 186), (122, 246), (96, GY)], (36, 30, 40))
        PG([(174, 160), (148, 186), (148, 246), (174, GY)], (40, 34, 44))
        R(122, 186, 148, 246, (28, 26, 38))
        lit.append((132, 196, 138, 200, (255, 214, 150)))
        emis.append((135, 198, 18, (255, 190, 120), 0.5))
        R(104, 137, 166, 149, (60, 46, 40))
        text('安和里', 135, 137, (226, 200, 150), 1, None)
        # ---- B2 hair salon ----
        R(230, 60, 380, GY, (70, 72, 92))
        cornice(230, 380, 60)
        windows(230, 380, [80, 128], seed=22, ww=28)
        R(236, 170, 374, 188, (40, 46, 70))
        text('理发', 305, 171, (222, 236, 250) if st['salon'] else (120, 124, 140), 1, (20, 26, 40))
        R(240, 192, 362, 256, (30, 32, 46))
        if st['salon']:
            lit.append((244, 196, 358, 252, (196, 222, 236)))
            for k in range(3):   # mirrors + chairs silhouettes
                lit.append((252 + k * 36, 202, 276 + k * 36, 226, (226, 240, 248)))
                R(258 + k * 36, 230, 270 + k * 36, 252, (70, 80, 96))
            emis.append((302, 226, 60, (190, 226, 250), 0.14))
            streaks.append((302, 226, (190, 226, 250), 8, 0.22))
        else:
            R(244, 196, 358, 252, (26, 28, 40))
            for k in range(3):
                PG([(250 + k * 38, 196), (262 + k * 38, 196), (246 + k * 38, 252), (242 + k * 38, 252)], (34, 36, 50))
        R(366, 186, 374, 236, (60, 60, 76))           # barber pole housing (stripes animated in overlay)
        # ---- B3 cafe ----
        R(380, 20, 540, GY, (78, 66, 74))
        cornice(380, 540, 20)
        windows(380, 540, [42, 100], seed=23, ww=26)
        R(386, 158, 534, 176, (60, 40, 36))
        text('咖啡', 460, 159, (246, 222, 180) if st['cafe'] else (120, 110, 100), 1, (40, 24, 20))
        for i in range(8):     # striped awning
            c = (150, 62, 60) if i % 2 == 0 else (226, 214, 196)
            PG([(386 + i * 18.5, 176), (386 + (i + 1) * 18.5, 176), (386 + (i + 1) * 18.5, 190), (386 + i * 18.5, 190)], c)
            ELL(386 + i * 18.5 + 9.25, 190, 9.25, 3.2, c)
        R(392, 196, 528, 256, (34, 28, 32))
        if st['cafe']:
            lit.append((396, 200, 524, 252, (246, 196, 132)))
            for cx_ in (420, 460, 500):
                R(cx_ - 9, 234, cx_ + 9, 237, (120, 80, 56)); R(cx_ - 1, 237, cx_ + 1, 252, (120, 80, 56))
            emis.append((460, 230, 64, (255, 190, 120), 0.16))
            streaks.append((430, 226, (255, 190, 120), 7, 0.28)); streaks.append((492, 226, (255, 190, 120), 7, 0.28))
        else:
            R(396, 200, 524, 252, (26, 24, 32))
        for k in range(3):
            PG([(404 + k * 44, 200), (416 + k * 44, 200), (400 + k * 44, 252), (396 + k * 44, 252)], (60, 52, 56) if not st['cafe'] else (255, 216, 160))
        # ---- B4 dance hall (neon handled in overlay) ----
        R(540, 0, 700, GY, (52, 44, 66))
        cornice(540, 700, 0, (84, 72, 100))
        windows(540, 700, [24, 84], seed=24, ww=26, litp=0.25)
        R(560, 150, 680, 160, (40, 32, 52))
        R(586, 186, 654, GY, (30, 20, 34))
        R(592, 192, 648, GY, (110, 30, 52))                # velvet curtain door
        for k in range(1, 4):
            LN([(592 + k * 14, 192), (592 + k * 14, GY)], (84, 22, 42))
        R(560, 182, 680, 186, (60, 50, 72))
        # ---- B5 CINEMA ----
        _cinema_static(R, PG, LN, ELL, lit, emis, streaks, text, st, z)
        # ---- B6 poster wall + bus stop ----
        R(1010, 70, 1180, GY, (74, 70, 86))
        cornice(1010, 1180, 70)
        windows(1010, 1180, [92, 140], seed=26, ww=26)
        R(1020, 186, 1084, 254, (88, 84, 96))        # wall panel for posters
        R(1024, 192, 1054, 240, (60, 56, 70))        # poster slot A (film poster drawn in overlay)
        R(1058, 196, 1080, 230, (176, 160, 120))     # small poster B
        R(1060, 200, 1078, 214, (140, 80, 70))
        R(1092, 196, 1172, 200, (120, 124, 140))     # shelter roof
        LN([(1096, 200), (1096, GY)], (110, 114, 130)); LN([(1168, 200), (1168, GY)], (110, 114, 130))
        R(1098, 202, 1146, 246, (46, 54, 72))
        lit.append((1148, 206, 1166, 248, (210, 220, 236)))
        emis.append((1157, 226, 40, (200, 220, 240), 0.26))
        R(1104, 238, 1160, 242, (120, 96, 70)); R(1108, 242, 1111, GY, (90, 70, 56)); R(1153, 242, 1156, GY, (90, 70, 56))
        # bus stop sign
        LN([(1176, GY), (1176, 190)], (110, 114, 130), w=max(1, int(2 * z)))
        R(1170, 180, 1182, 196, (60, 120, 90))
        # ---- B7 shophouses (arcade) ----
        R(1180, 40, 1420, GY, (86, 78, 88))
        cornice(1180, 1420, 40)
        windows(1180, 1420, [62, 116], seed=27, ww=26)
        R(1180, 170, 1420, 178, (66, 60, 72))
        for px_ in range(1190, 1420, 46):
            R(px_, 178, px_ + 8, GY, (96, 88, 98))
        R(1198, 186, 1290, 256, (30, 30, 42))
        y_sh = 186
        while y_sh < 256:
            LN([(1198, y_sh), (1290, y_sh)], (64, 66, 80)); y_sh += 3
        R(1300, 186, 1410, 256, (34, 30, 40))
        if st['shops']:
            lit.append((1304, 190, 1406, 252, (236, 200, 140)))
        R(1304, 160, 1406, 170, (50, 42, 44))
        text('南货店', 1355, 159, (220, 200, 160), 1, None)
        # ---- B8 corner ----
        R(1420, 10, 1720, GY, (60, 58, 80))
        cornice(1420, 1720, 10)
        windows(1420, 1720, [30, 86, 140], seed=28)
        R(1430, 186, 1700, 256, (44, 44, 60))
        LN([(1520, GY), (1520, 150)], (70, 72, 88), w=max(1, int(3 * z)))
        R(1512, 150, 1528, 182, (36, 36, 44))
        ELL(1520, 158, 4, 4, (230, 60, 60)); ELL(1520, 174, 4, 4, (40, 60, 50))
        emis.append((1520, 158, 24, (255, 70, 70), 0.5))
        streaks.append((1520, 166, (255, 80, 80), 4, 0.36))
        # ---- lamps ----
        for lx in LAMPS:
            LN([(lx, GY), (lx, 128)], (60, 62, 76), w=max(1, int(3 * z)))
            LN([(lx, 128), (lx + 4, 120), (lx + 16, 118)], (60, 62, 76), w=max(1, int(2 * z)))
            R(lx + 10, 116, lx + 24, 122, (50, 50, 60))
            lit.append((lx + 12, 121, lx + 22, 124, (255, 220, 160)))
            emis.append((lx + 17, 124, 50, (255, 186, 110), 0.40))
            streaks.append((lx + 17, 124, (255, 190, 120), 6, 0.45))
        # ---- ground ----
        R(-10, GY, WORLD_W + 10, CURB0, (50, 52, 70))
        xx = 0
        while xx < WORLD_W:
            LN([(xx, GY), (xx - 6, CURB0)], (44, 46, 62)); xx += 24
        LN([(0, GY + 10), (WORLD_W, GY + 10)], (46, 48, 64))
        R(-10, CURB0, WORLD_W + 10, CURB1, (88, 92, 114))
        R(-10, CURB1, WORLD_W + 10, 700, (28, 30, 44))
        for xx in range(0, WORLD_W, 90):
            R(xx, 330, xx + 44, 333, (68, 70, 84))
        img = np.asarray(im, np.float32).copy()
        img = grade(img, variant)
        for (x0, y0, x1, y1, c) in lit:
            a, b = T(x0, y0); cc, dd = T(x1, y1)
            a, b, cc, dd = int(round(a)), int(round(b)), int(round(cc)), int(round(dd))
            if dd <= 0 or b >= hh:
                continue
            col = np.asarray(c, np.float32)
            if variant == 'memory':
                col = np.minimum(255, col * np.array([1.1, 1.0, 0.85]) + 10)
            img[max(0, b):max(0, dd), max(0, a):max(0, cc)] = col
        for (s_, wx, wy, col, sc, ol, vert) in texts:
            _put_text(img, s_, T, z, wx, wy, col, sc, ol, vert)
        res = dict(img=img, emis=emis, streaks=streaks, z=z, cam_y=cam_y)
        self._cache[key] = res
        return res


def _put_text(img, s_, T, z, wx, wy, col, sc=1, ol=None, vertical=False):
    k = max(1, int(round(z * sc)))
    if vertical:
        ms = [text_mask(c, 16) for c in s_]
        wmax = max(m.shape[1] for m in ms)
        hsum = sum(m.shape[0] + 3 for m in ms)
        m = np.zeros((hsum, wmax), bool)
        y = 0
        for mm in ms:
            o = (wmax - mm.shape[1]) // 2
            m[y:y + mm.shape[0], o:o + mm.shape[1]] = mm
            y += mm.shape[0] + 3
    else:
        m = text_mask(s_, 16)
    if k > 1:
        m = np.repeat(np.repeat(m, k, 0), k, 1)
    x, y = T(wx, wy)
    x = int(round(x - m.shape[1] / 2)); y = int(round(y))
    Hh, Ww = img.shape[:2]
    sub = np.zeros((Hh, Ww), bool)
    ys0, xs0 = max(0, y), max(0, x)
    ys1, xs1 = min(Hh, y + m.shape[0]), min(Ww, x + m.shape[1])
    if ys1 > ys0 and xs1 > xs0:
        sub[ys0:ys1, xs0:xs1] = m[ys0 - y:ys1 - y, xs0 - x:xs1 - x]
        if ol is not None:
            img[outline_of(sub)] = ol
        img[sub] = col
    return sub


def _cinema_static(R, PG, LN, ELL, lit, emis, streaks, text, st, z):
    c = CIN
    stone, stone_d, stone_l = (92, 82, 92), (66, 58, 70), (120, 108, 112)
    R(700, -30, 1010, GY, stone)
    # tower
    R(812, -170, 898, 120, stone)
    PG([(812, -170), (898, -170), (884, -196), (826, -196)], stone_l)
    R(846, -214, 864, -196, stone_l)
    LN([(855, -214), (855, -244)], (90, 84, 90), w=max(1, int(2 * z)))
    # art-deco fins
    for fx in (706, 730, 980, 1004):
        R(fx - 5, -30, fx + 5, 118, stone_l)
        R(fx + 2, -30, fx + 5, 118, stone_d)
    for fx in (818, 892):
        R(fx - 4, -170, fx + 4, 118, stone_l)
    R(700, -36, 1010, -30, stone_l)
    # vertical blade sign housing (neon letters in overlay)
    R(840, -150, 870, 24, (40, 32, 44))
    # clock disc
    cx, cy, r = c['clock']
    ELL(cx, cy, r + 4, r + 4, stone_l)
    ELL(cx, cy, r + 1, r + 1, (60, 52, 58))
    ELL(cx, cy, r, r, (226, 214, 188))
    for k in range(12):
        a = k / 12 * 2 * math.pi
        x0, y0 = cx + math.sin(a) * (r - 2.0), cy - math.cos(a) * (r - 2.0)
        x1, y1 = cx + math.sin(a) * (r - (5.0 if k % 3 == 0 else 3.4)), cy - math.cos(a) * (r - (5.0 if k % 3 == 0 else 3.4))
        LN([(x0, y0), (x1, y1)], (60, 50, 50), w=max(1, int(z * (1.2 if k % 3 == 0 else 0.8))))
    lit_k = st['cinema']
    if lit_k > 0:
        emis.append((cx, cy, 34, (255, 230, 180), 0.22 * lit_k))
    # windows on facade sides
    for wx in (744, 770, 940, 966):
        for wy in (-6, 40, 86):
            R(wx - 8, wy, wx + 8, wy + 22, (40, 36, 52))
            R(wx - 6, wy + 2, wx + 6, wy + 20, (60, 52, 66))
    # marquee box
    R(c['mx0'] - 4, c['my0'] - 4, c['mx1'] + 4, c['my1'] + 4, (200, 186, 150))
    R(c['mx0'], c['my0'], c['mx1'], c['my1'], (226, 210, 170))
    R(c['mx0'] + 6, c['my0'] + 6, c['mx1'] - 6, c['my1'] - 6, (18, 16, 22))
    # canopy
    PG([(722, 178), (988, 178), (996, 190), (714, 190)], (92, 80, 84))
    R(714, 190, 996, 194, (60, 52, 58))
    # entrance
    R(760, 194, 950, 256, (40, 32, 38))
    if lit_k > 0:
        dc = tuple(int(v) for v in mix((60, 50, 52), (250, 206, 140), lit_k))
        for k in range(4):
            dx0 = 774 + k * 41.5
            lit.append((dx0 + 2, 200, dx0 + 18, 224, dc)); lit.append((dx0 + 21, 200, dx0 + 37, 224, dc))
            lit.append((dx0 + 2, 228, dx0 + 18, 254, dc)); lit.append((dx0 + 21, 228, dx0 + 37, 254, dc))
        emis.append((855, 232, 84, (255, 200, 130), 0.2 * lit_k))
        streaks.append((800, 226, (255, 200, 130), 9, 0.3 * lit_k)); streaks.append((910, 226, (255, 200, 130), 9, 0.3 * lit_k))
    else:
        R(772, 198, 938, 256, (34, 28, 34))
    for k in range(5):
        LN([(772 + k * 41.5, 198), (772 + k * 41.5, 256)], (70, 56, 50), w=max(1, int(2 * z)))
    LN([(772, 226), (938, 226)], (70, 56, 50))
    # poster cases on both sides
    for px_ in (734, 954):
        R(px_, 198, px_ + 22, 250, (150, 130, 100))
        R(px_ + 2, 200, px_ + 20, 248, (44, 36, 46))
    # steps
    R(752, 256, 958, 259, (128, 116, 112)); R(744, 259, 966, 262, (110, 100, 98))


STREET = ShStreet()


# ---------------- dynamic overlays ----------------

def flip_char(final, t, lock, seed=0, chars='白兰花午夜场电影今晚雨街她爱等灯钟上海'):
    """flip-board letter: random every 3 frames until lock, then final."""
    if t >= lock:
        return final, True
    f = math.floor(t * FPS / 3)
    return chars[int(h01(f, seed) * len(chars))], False


# marquee board layout (world units), mirror-symmetric about x=855
MQ_ROW1 = (110, 123)          # '今夜 · 午夜场'
MQ_TILES = (124, 152)         # flip tiles
MQ_ROW3 = (154, 168)          # centred static line
MQ_TW, MQ_TG = 32, 6          # tile width, gap


def _ink(s_, k):
    m = text_mask(s_, 16)
    cols = np.where(m.any(0))[0]
    if len(cols):
        m = m[:, cols[0]:cols[-1] + 1]
    if k > 1:
        m = np.repeat(np.repeat(m, k, 0), k, 1)
    return m


def _stamp(img, m, cx, cy, col):
    """paste text mask with its ink box centred on (cx, cy)"""
    Hh, Ww = img.shape[:2]
    h, w = m.shape
    x0, y0 = int(round(cx - w / 2.0)), int(round(cy - h / 2.0))
    xs0, ys0, xs1, ys1 = max(0, x0), max(0, y0), min(Ww, x0 + w), min(Hh, y0 + h)
    if xs1 <= xs0 or ys1 <= ys0:
        return
    sub = m[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]
    reg = img[ys0:ys1, xs0:xs1]
    reg[sub] = col


def _band_text(img, T, z, s_, y0, y1, col):
    """centred line in a band; 16px Unifont when it fits, else symmetric dashes (reads as text from afar)."""
    cx, cy = T(855, (y0 + y1) / 2.0)
    bh = min(MQ_ROW1[1] - MQ_ROW1[0], MQ_ROW3[1] - MQ_ROW3[0]) * z   # same rule for both rows
    if bh >= 15:
        _stamp(img, _ink(s_, 1), cx, cy, col)
        return
    Hh, Ww = img.shape[:2]
    n = len(s_)
    cw = 7.0 * z
    for i, ch in enumerate(s_):
        if ch == ' ':
            continue
        x = cx + (i - (n - 1) / 2.0) * cw
        if ch in '·:':
            img[m_rect(x, cy, x + 1, cy + 1, Ww, Hh)] = col
        else:
            img[m_rect(x - cw * 0.36, cy - max(0.5, 0.8 * z), x + cw * 0.36, cy + max(0.5, 0.8 * z), Ww, Hh)] = col


def _bulb_track():
    c = CIN
    x0, x1 = c['mx0'] + 3, c['mx1'] - 3
    y0, y1 = c['my0'] + 3, c['my1'] - 3
    nx = int(round((x1 - x0) / 6.0))
    ny = int(round((y1 - y0) / 6.0))
    half_w, hgt = (x1 - x0) / 2.0, (y1 - y0)
    out = []
    for i in range(nx + 1):
        x = x0 + (x1 - x0) * i / nx
        dx = abs(x - 855)
        out.append((x, y0, dx))                          # top row: distance from top centre
        out.append((x, y1, half_w + hgt + (half_w - dx)))  # bottom row
    for j in range(1, ny):
        y = y0 + (y1 - y0) * j / ny
        out.append((x0, y, half_w + (y - y0)))
        out.append((x1, y, half_w + (y - y0)))
    return out, 2 * half_w + hgt


BULBS, BULB_D = _bulb_track()


def marquee_overlay(img, T, z, t, st):
    """bulbs, flip tiles, centred text lines, clock hands, blade neon. All mirror-symmetric about x=855.
    st: bulbs_on 0..1 (lights spread from top centre down both sides), chase, lights 0..1 (off from bottom centre up),
    board, flips [t白,t兰,t花], flip_start, blank [..] (flip back to blank), land (all-bulb flash time), msg, msg_at, kt, clock, blade"""
    c = CIN
    Hh, Ww = img.shape[:2]
    on = st.get('lights', 1.0)
    frac = st.get('bulbs_on', 1.0)
    chase = st.get('chase', True)
    land = st.get('land')
    flash = land is not None and 0 <= t - land < 3.0 / FPS
    ph = int(math.floor(t * 8)) % 3
    r = max(1.0, 1.3 * z)
    for (bx, by, d) in BULBS:
        sx, sy = T(bx, by)
        if not (-6 < sx < Ww + 6 and -6 < sy < Hh + 6):
            continue
        u = d / BULB_D
        lit_ = u < frac and u < on
        q = int(round(d / 6.0))
        bright = lit_ and (flash or not chase or (q - ph) % 3 != 0)
        col = (255, 236, 170) if bright else ((150, 120, 80) if lit_ else (90, 80, 70))
        img[m_ellipse(sx, sy, r, r, Ww, Hh)] = col
        if bright and z >= 1.2:
            stepped_glow(img, sx, sy, r * (4.0 if flash else 3.2), (255, 210, 120), k=0.4 if flash else 0.28, levels=2)
    board_on = st.get('board', 1.0) * on
    if board_on > 0:
        _band_text(img, T, z, '今夜 · 午夜场', MQ_ROW1[0], MQ_ROW1[1], tuple(int(v) for v in mix((70, 60, 60), (246, 236, 214), board_on)))
        if t >= st.get('msg_at', -1.0):
            _band_text(img, T, z, st.get('msg', '00:00 开映'), MQ_ROW3[0], MQ_ROW3[1],
                       tuple(int(v) for v in mix((60, 50, 40), (255, 196, 96), board_on)))
    # --- flip tiles ---
    flips = st.get('flips', [3.07, 4.01, 4.96])
    off_chars = st.get('off_chars', 0)
    blank = st.get('blank')
    ty0, ty1 = MQ_TILES
    kt = st.get('kt') or max(1, int(round((ty1 - ty0) * z * 0.62 / 15.0)))
    for k, ch in enumerate('白兰花'):
        tx0 = 855 + (k - 1) * (MQ_TW + MQ_TG) - MQ_TW / 2.0
        a, b_ = T(tx0, ty0); cc, dd = T(tx0 + MQ_TW, ty1)
        a, b_, cc, dd = int(round(a)), int(round(b_)), int(round(cc)), int(round(dd))
        tile = m_rect(a, b_, cc, dd, Ww, Hh)
        mid = (b_ + dd) // 2
        lock = flips[k]
        if lock is None or t < st.get('flip_start', 1.17) or (blank is not None and t >= blank[k]):
            img[tile] = (32, 30, 38)
            if 0 <= mid < Hh:
                img[mid, max(0, a):max(0, cc)] = (20, 18, 24)
            continue
        g, done = flip_char(ch, t, lock, seed=k * 7 + 1)
        if blank is not None and t >= blank[k] - 0.14:
            g, done = flip_char(' ', t, 9e9, seed=k * 5 + 3, chars=' 白 兰 花 ')
        dark = k < off_chars
        tl = 0.5 + 0.5 * on
        img[tile] = (40, 36, 44) if dark else np.array((236, 228, 210), np.float32) * tl
        colr = np.array((196, 40, 60), np.float32) * tl if done else np.array((60, 54, 60), np.float32)
        if dark:
            colr = (64, 56, 62)
        if g.strip():
            _stamp(img, _ink(g, kt), (a + cc) / 2.0, (b_ + dd) / 2.0, colr)
        if 0 <= mid < Hh:
            seg_ = img[mid, max(0, a):max(0, cc)]
            seg_[:] = seg_ * 0.55 + np.array((120, 110, 100), np.float32) * 0.45 if not dark else (30, 28, 34)
        if done and not dark and 0 <= t - lock < 0.25:
            stepped_glow(img, (a + cc) / 2, (b_ + dd) / 2, (cc - a) * 0.9, (255, 220, 160), k=0.5 * (1 - (t - lock) / 0.25), levels=3)
    # --- clock hands ---
    cx, cy, rr = c['clock']
    mins = st.get('clock', 58.0)    # minutes after 23:00 (60 = 00:00)
    hh_ = 11 + mins / 60.0
    am = mins / 60 * 2 * math.pi
    ah = (hh_ % 12) / 12 * 2 * math.pi
    for ang, L, w in ((ah, rr * 0.55, 1.6), (am, rr * 0.82, 1.1)):
        p0 = T(cx, cy); p1 = T(cx + math.sin(ang) * L, cy - math.cos(ang) * L)
        img[m_line([p0, p1], max(1, int(round(w * z * 0.9))), Ww, Hh)] = (40, 30, 34)
    p = T(cx, cy)
    img[m_ellipse(p[0], p[1], max(1, z * 1.2), max(1, z * 1.2), Ww, Hh)] = (150, 40, 44)
    # --- vertical blade neon 电影院 ---
    neon = st.get('blade', 1.0) * on
    col = (255, 120, 190) if neon > 0.5 else (90, 50, 70)
    sub = _put_text(img, '电影院', T, z, 855, -142, col, 1.4, None, vertical=True)
    if neon > 0.5:
        ys, xs = np.nonzero(sub)
        if len(xs):
            stepped_glow(img, xs.mean(), ys.mean(), max(30, (ys.max() - ys.min()) * 0.7), (255, 90, 170), k=0.22, levels=3, sy=1.8)
    # --- canopy underside bulbs (symmetric, switch off from the outside in) ---
    for kk in range(-15, 16):
        xx = 855 + 9 * kk
        sx, sy = T(xx, 192)
        if -4 < sx < Ww + 4 and -4 < sy < Hh + 4:
            lit_ = on > abs(kk) / 15.5
            img[m_ellipse(sx, sy, max(1, z * 0.9), max(1, z * 0.9), Ww, Hh)] = (255, 232, 170) if lit_ else (90, 80, 70)


def neon_overlay(img, T, z, t, st):
    """dance hall neon + salon barber pole + film poster on wall."""
    Hh, Ww = img.shape[:2]
    if st.get('dance', 1):
        flick = st.get('dance_flick', 1.0)
        col = (120, 240, 255) if flick > 0.5 else (40, 70, 90)
        sub = _put_text(img, '舞厅', T, z, 620, 30, col, 1.3, None, vertical=True)
        if flick > 0.5:
            ys, xs = np.nonzero(sub)
            if len(xs):
                stepped_glow(img, xs.mean(), ys.mean(), max(24, (ys.max() - ys.min()) * 0.8), (90, 220, 255), k=0.2, levels=3, sy=1.6)
        # neon frame line
        p0 = T(562, 152); p1 = T(678, 158)
        m = m_rect(p0[0], p0[1], p1[0], p1[1], Ww, Hh)
        img[m] = (255, 110, 180) if flick > 0.5 else (90, 50, 70)
        sub2 = _put_text(img, '夜 上 海', T, z, 620, 148, (255, 240, 250) if flick > 0.5 else (90, 70, 80), 0.6)
    # barber pole
    if st.get('salon', 1):
        a, b_ = T(367, 188); cc, dd = T(373, 234)
        a, b_, cc, dd = int(round(a)), int(round(b_)), int(round(cc)), int(round(dd))
        ya, yb, xa, xb = max(0, b_), min(Hh, dd), max(0, a), min(Ww, cc)
        if xb > xa and yb > ya:
            ys, xs = np.mgrid[ya:yb, xa:xb]
            if ys.size:
                ph = (ys + (xs - a) * 0.8 - tq(t, 12) * 24 * z) / max(2, 4 * z)
                band = np.floor(ph).astype(int) % 3
                cols = np.array([(220, 40, 50), (240, 240, 250), (40, 70, 200)], np.float32)
                img[ys, xs] = cols[band]
    # film poster on wall (her in 月份牌 style, simplified at street scale)
    if st.get('poster', 1):
        draw_poster(img, T, z, 1024, 192, 1054, 240, t, wet=st.get('poster_wet', 0.0))


def draw_poster(img, T, z, x0, y0, x1, y1, t, wet=0.0):
    Hh, Ww = img.shape[:2]
    a, b_ = T(x0, y0); cc, dd = T(x1, y1)
    if cc < 0 or a > Ww or dd < 0 or b_ > Hh:
        return
    pw, ph = cc - a, dd - b_
    m = m_rect(a, b_, cc, dd, Ww, Hh)
    img[m] = (236, 214, 176)
    # sky band + orchid + woman silhouette (bob, red lips)
    img[m_rect(a + pw * 0.06, b_ + ph * 0.05, cc - pw * 0.06, b_ + ph * 0.72, Ww, Hh)] = (64, 96, 112)
    hx, hy = a + pw * 0.5, b_ + ph * 0.34
    img[m_ellipse(hx, hy + ph * 0.02, pw * 0.25, ph * 0.17, Ww, Hh)] = (90, 50, 40)     # bob hair
    img[m_ellipse(hx + pw * 0.02, hy + ph * 0.03, pw * 0.17, ph * 0.12, Ww, Hh)] = (248, 214, 190)
    img[m_poly([(hx - pw * 0.28, b_ + ph * 0.72), (hx + pw * 0.28, b_ + ph * 0.72), (hx + pw * 0.18, hy + ph * 0.18), (hx - pw * 0.18, hy + ph * 0.18)], Ww, Hh)] = (110, 40, 70)
    if pw > 30:
        img[m_ellipse(hx + pw * 0.02, hy + ph * 0.09, pw * 0.035, ph * 0.012 + 0.6, Ww, Hh)] = (150, 20, 44)
    for k in range(3):    # white orchids at the bottom corner
        ox = a + pw * (0.18 + k * 0.1); oy = b_ + ph * (0.66 - (k % 2) * 0.05)
        img[m_ellipse(ox, oy, max(1, pw * 0.05), max(1, pw * 0.04), Ww, Hh)] = (252, 250, 236)
    # title band
    img[m_rect(a + pw * 0.06, b_ + ph * 0.76, cc - pw * 0.06, b_ + ph * 0.93, Ww, Hh)] = (160, 40, 50)
    if pw >= 40:
        _put_text(img, '白兰花', lambda x, y: (x, y), 1, a + pw / 2, b_ + ph * 0.77, (250, 236, 210), max(0.5, pw / 90))
    if wet > 0:
        # running colour streaks (water)
        n = int(6 + wet * 10)
        for i in range(n):
            sx = a + pw * h01(i, 3)
            L = ph * (0.15 + 0.6 * h01(i, 9)) * min(1.0, wet * 1.4)
            sy0 = b_ + ph * 0.1 * h01(i, 5)
            wcol = np.array((90, 60, 80), np.float32) if h01(i, 1) < 0.5 else np.array((150, 50, 70), np.float32)
            mm = m_line([(sx, sy0), (sx + 1, sy0 + L)], max(1, int(pw * 0.03)), Ww, Hh)
            img[mm] = img[mm] * (1 - 0.6 * wet) + wcol * 0.6 * wet


def render_street(cam_x, cam_y, z, variant='night', state=None, t=0.0, wet=True, glow=True, reflect_k=0.4, ow=None, oh=None,
                  marquee=None, neon=None):
    """returns (frame, info). cam_x/cam_y: world coords of top-left."""
    ow = W if ow is None else ow
    oh = H if oh is None else oh
    S = STREET.strip(z, cam_y, variant, state, hh=oh)
    x0 = int(round(cam_x * z))
    x0 = max(0, min(S['img'].shape[1] - ow, x0))
    img = S['img'][:, x0:x0 + ow].copy()
    T = lambda x, y: (x * z - x0, (y - cam_y) * z)
    info = dict(T=T, z=z, x0=x0)
    st = dict(state or {})
    if marquee is not None:
        marquee_overlay(img, T, z, t, marquee)
    nst = dict(dance=st.get('dance', 1), salon=st.get('salon', 1), poster=st.get('poster', 1))
    if neon:
        nst.update(neon)
    neon_overlay(img, T, z, t, nst)
    if glow:
        for (wx, wy, r, c, s) in S['emis']:
            sx, sy = T(wx, wy)
            if -r * z < sx < ow + r * z:
                stepped_glow(img, sx, sy, r * min(z, 1.6), c, k=s / max(1.0, z) ** 0.6, levels=4)
        for lx in LAMPS:
            sx, sy = T(lx + 17, GY + 11)
            if -80 * z < sx < ow + 80 * z:
                stepped_glow(img, sx, sy, 56 * z, (255, 180, 110), k=0.2, levels=3, sy=0.18)
    if wet:
        _, gy = T(0, CURB1)
        gy = int(round(gy))
        if 0 < gy < oh:
            from fx import reflect, light_streaks
            reflect(img, gy, oh, k=reflect_k, squash=1.0, t=t, wobble=1, broken=False)
            sl = []
            for (wx, wy, c, wd, s_) in S['streaks']:
                sx, sy = T(wx, wy)
                if -20 < sx < ow + 20:
                    sl.append((sx, sy, c, wd * z, s_))
            light_streaks(img, t, sl, gy, oh)
    return img, info
