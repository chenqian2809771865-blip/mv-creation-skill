# -*- coding: utf-8 -*-
"""The street: world-space vector scene rasterized at any zoom straight onto the pixel grid.
World: x 0..1640, sidewalk top y=262, curb 284-287, road below. Variants: night / moon / memory."""
import numpy as np, math, functools
from core import *

GY, CURB0, CURB1 = 262, 284, 287
WORLD_W = 1640
LAMPS = [160, 524, 884, 1252, 1574]


def _bands(h, cols, y0=0, y1=None):
    pass


def grade(img, variant):
    if variant == 'memory':
        out = img * np.array([1.42, 1.08, 0.86], np.float32) + np.array([22, 8, 0], np.float32)
    elif variant == 'moon':
        out = img * np.array([0.92, 1.04, 1.2], np.float32) + np.array([2, 8, 20], np.float32)
    else:
        out = img
    return np.clip(out, 0, 255)


SKY = {
    'night': [C('#16152a'), C('#1c1a33'), C('#23203d'), C('#2b2646'), C('#352d50'), C('#423558')],
    'moon': [C('#121a34'), C('#16213f'), C('#1b294b'), C('#223257'), C('#2a3c63'), C('#34476e')],
    'memory': [C('#5a4268'), C('#7a5272'), C('#9a6276'), C('#bd7676'), C('#dc8c74'), C('#f0a678')],
}


class Street:
    def __init__(self):
        self._cache = {}

    # ---------------- raster of the whole street at zoom z ----------------
    def strip(self, z, cam_y, variant='night', state=None, hh=None):
        hh = H if hh is None else hh
        key = (round(z, 3), round(cam_y, 2), variant, tuple(sorted((state or {}).items())), hh)
        if key in self._cache:
            return self._cache[key]
        if len(self._cache) > 6:
            self._cache.pop(next(iter(self._cache)))
        st = dict(shutter=0.0, flower=1, noodle=1, b4=1, cafe=0, lantern=0, oldshop=0, signal='red', vend=1, apt=1)
        if state:
            st.update(state)
        Wp = int(WORLD_W * z) + 2
        Hh = hh
        T = lambda x, y: (x * z, (y - cam_y) * z)
        img = np.zeros((Hh, Wp, 3), np.float32)
        # sky (screen-space bands)
        sky = SKY[variant]
        vgrad_bands(img, 0, Hh, sky[0], sky[-1], len(sky))
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
            d.ellipse([round(a), round(b), round(cc) - 1, round(dd) - 1], fill=tuple(int(v) for v in c))

        texts = []   # (string, wx, wy, color, scale, outline)
        emis = []    # emissive glows: (wx, wy, radius_world, color, strength)
        lit = []     # emissive rects to draw after grading: (x0,y0,x1,y1,color)
        streaks = [] # reflection light streaks: (wx, wy_src, color, width, strength)

        # ---- far city silhouettes (parallax handled by caller drawing separately; here static backdrop) ----
        rng = np.random.default_rng(3)
        x = -20
        while x < WORLD_W + 40:
            bw = int(rng.integers(40, 110)); top = int(rng.integers(-60, 40))
            R(x, top, x + bw, GY, (40, 36, 62))
            for yy in range(top + 8, 160, 14):
                for xx in range(x + 6, x + bw - 6, 12):
                    if rng.random() < 0.14:
                        R(xx, yy, xx + 4, yy + 5, (150, 120, 96) if rng.random() < 0.7 else (100, 120, 150))
            x += bw + int(rng.integers(0, 16))

        def windows(x0, x1, rows, wcol, ww=26, wh=30, gap=None, litp=0.4, seed=0, ac=True):
            r = np.random.default_rng(seed)
            n = max(1, int((x1 - x0 - 12) // (ww + 14)))
            gap = ((x1 - x0) - n * ww) / (n + 1)
            for ry in rows:
                for i in range(n):
                    wx = x0 + gap + i * (ww + gap)
                    R(wx - 2, ry - 2, wx + ww + 2, ry + wh + 3, (34, 34, 50))
                    on = r.random() < litp
                    R(wx, ry, wx + ww, ry + wh, (30, 33, 50))
                    if on:
                        c = (238, 180, 108) if r.random() < 0.75 else (150, 190, 214)
                        lit.append((wx, ry, wx + ww, ry + wh, c))
                        if r.random() < 0.5:  # curtain / silhouette
                            lit.append((wx + ww * 0.55, ry, wx + ww, ry + wh, tuple(int(v * 0.75) for v in c)))
                    else:
                        R(wx, ry, wx + ww * 0.5, ry + wh, (38, 42, 62))
                    if z >= 1.4:
                        LN([(wx + ww / 2, ry), (wx + ww / 2, ry + wh)], (40, 40, 58))
                        LN([(wx, ry + wh * 0.45), (wx + ww, ry + wh * 0.45)], (40, 40, 58))
                    R(wx - 3, ry + wh + 2, wx + ww + 3, ry + wh + 5, (88, 90, 110))  # sill
                    if ac and r.random() < 0.3:
                        R(wx + ww + 4, ry + wh - 12, wx + ww + 20, ry + wh, (110, 112, 126))
                        R(wx + ww + 4, ry + wh - 12, wx + ww + 20, ry + wh - 10, (140, 142, 156))

        def cornice(x0, x1, y, c=(96, 96, 118)):
            R(x0 - 3, y, x1 + 3, y + 5, c)
            R(x0 - 3, y + 5, x1 + 3, y + 7, (40, 40, 56))

        # ---- B1 apartment (his) ----
        R(0, -400, 200, GY, (56, 60, 84))
        if z >= 1.3:
            for yy in range(-400, GY, 7):
                LN([(0, yy), (200, yy)], (50, 54, 76))
        windows(0, 200, [-140, -60, 20, 96], None, litp=0.45, seed=1)
        cornice(0, 200, 170)
        R(64, 192, 116, GY, (38, 30, 36))
        R(70, 198, 110, GY, (60, 42, 40))
        if st['apt']:
            lit.append((76, 204, 104, 236, (230, 176, 112)))
        else:
            R(76, 204, 104, 236, (40, 40, 56))
        R(58, 186, 122, 192, (90, 92, 112))
        emis.append((118, 206, 30, (255, 196, 130), 0.5))
        lit.append((116, 202, 121, 210, (255, 220, 160)))
        for i in range(3):
            R(18 + i * 13, 214, 28 + i * 13, 240, (84, 90, 112))
        # ---- B2 flower shop ----
        R(200, 40, 380, GY, (74, 66, 84))
        cornice(200, 380, 40)
        windows(200, 380, [64, 116], None, litp=0.35, seed=2, ww=30)
        R(206, 150, 374, 168, (44, 40, 52))
        texts.append(('花店', 290, 151, (236, 220, 200) if st['flower'] else (130, 120, 120), 1, (30, 26, 34)))
        if st['flower']:
            emis.append((290, 159, 40, (255, 214, 170), 0.18))
        # awning stripes
        for i in range(9):
            c = (80, 120, 104) if i % 2 == 0 else (196, 200, 186)
            PG([(206 + i * 18.7, 168), (206 + (i + 1) * 18.7, 168), (206 + (i + 1) * 18.7, 186), (206 + i * 18.7, 186)], c)
        for i in range(9):
            ELL(206 + i * 18.7 + 9.3, 186, 9.3, 3.5, (80, 120, 104) if i % 2 == 0 else (196, 200, 186))
        R(212, 192, 368, 254, (36, 36, 50))
        if st['flower']:
            lit.append((216, 196, 364, 250, (246, 228, 196)))
            for i in range(14):
                c = [(214, 80, 96), (240, 200, 80), (236, 140, 170), (250, 246, 240), (150, 90, 170)][i % 5]
                lit.append((222 + i * 10, 232 - (i % 3) * 4, 230 + i * 10, 240 - (i % 3) * 4, c))
                lit.append((223 + i * 10, 240, 229 + i * 10, 250, (60, 90, 70)))
            emis.append((290, 236, 70, (255, 226, 190), 0.16))
            streaks.append((240, 230, (255, 226, 190), 6, 0.25)); streaks.append((340, 230, (255, 226, 190), 6, 0.25))
        else:
            for i in range(14):
                R(222 + i * 10, 236 - (i % 3) * 4, 230 + i * 10, 250, (54, 50, 64))
        LN([(290, 192), (290, 254)], (60, 58, 76))
        # ---- B3 noodle ----
        R(380, 10, 540, GY, (66, 56, 72))
        cornice(380, 540, 10)
        windows(380, 540, [34, 96], None, litp=0.5, seed=3, ww=28)
        R(386, 154, 534, 176, (110, 40, 44))
        texts.append(('面馆', 460, 157, (252, 236, 210) if st['noodle'] else (150, 120, 120), 1, (60, 18, 22)))
        R(392, 184, 528, 254, (34, 28, 34))
        if st['noodle']:
            lit.append((398, 190, 522, 252, (252, 190, 120)))
            emis.append((460, 230, 70, (255, 180, 110), 0.18))
            streaks.append((420, 220, (255, 180, 110), 7, 0.3)); streaks.append((500, 220, (255, 180, 110), 7, 0.3))
        # noren
        for i in range(4):
            R(404 + i * 30, 186, 430 + i * 30, 214, (40, 52, 90))
        texts.append(('面', 460, 192, (230, 232, 240), 1, None))
        # lantern
        ELL(536, 196, 6, 8, (200, 50, 50) if st['noodle'] else (100, 40, 44))
        if st['noodle']:
            emis.append((536, 196, 22, (255, 90, 70), 0.5))
        # ---- B4 shutter shop ----
        R(540, 60, 700, GY, (58, 62, 78))
        cornice(540, 700, 60)
        windows(540, 700, [84, 136], None, litp=0.3, seed=4)
        R(550, 178, 690, 186, (40, 42, 56))
        sh_y = 186 + (GY - 186) * st['shutter']   # shutter bottom edge
        R(552, 186, 688, GY, (30, 30, 42))
        if st['b4'] and st['shutter'] < 1:
            lit.append((556, max(sh_y, 190), 684, GY - 4, (214, 230, 236)))
            emis.append((620, 236, 64, (200, 225, 240), 0.14 * (1 - st['shutter'])))
        R(552, 186, 688, sh_y, (92, 96, 110))
        yy = 186
        while yy < sh_y:
            LN([(552, yy), (688, yy)], (72, 76, 90))
            yy += 3
        R(552, sh_y - 3, 688, sh_y, (60, 62, 74))
        # ---- B5 cafe ----
        R(700, 30, 900, GY, (70, 74, 92))
        cornice(700, 900, 30)
        windows(700, 900, [52, 108], None, litp=0.3, seed=5, ww=30)
        R(706, 170, 894, 260, (40, 40, 54))
        R(712, 176, 888, 256, (26, 28, 40))
        for (cx_, cy_) in ((744, 236), (800, 240), (856, 236)):
            R(cx_ - 10, cy_ - 2, cx_ + 10, cy_, (44, 44, 60)); R(cx_ - 1, cy_, cx_ + 1, 256, (44, 44, 60))
        for k in range(3):  # glass sheen
            PG([(724 + k * 60, 176), (740 + k * 60, 176), (708 + k * 60, 256), (712 + k * 60, 256)], (36, 40, 56))
        R(708, 172, 892, 176, (96, 98, 118))
        ELL(904, 182, 10, 8, (180, 150, 110))
        texts.append(('咖啡', 800, 156, (200, 196, 210), 1, (30, 30, 40)))
        # ---- B6 alley + vending machine ----
        R(900, -40, 950, GY, (26, 24, 38))
        R(906, 206, 944, GY, (60, 64, 84))
        if st['vend']:
            lit.append((910, 210, 940, 246, (200, 230, 246)))
            for r_ in range(3):
                for c_ in range(4):
                    lit.append((912 + c_ * 7, 214 + r_ * 10, 916 + c_ * 7, 220 + r_ * 10, [(220, 80, 80), (80, 140, 220), (240, 200, 80), (90, 190, 120)][(r_ + c_) % 4]))
            emis.append((925, 228, 48, (180, 220, 255), 0.35))
            streaks.append((925, 228, (180, 220, 255), 8, 0.35))
        # ---- B7 old shop with tiled eave ----
        R(950, 128, 1180, GY, (92, 84, 90))
        R(950, 186, 1180, 190, (66, 48, 44))
        R(958, 186, 964, GY, (74, 52, 46)); R(1166, 186, 1172, GY, (74, 52, 46))
        # door lattice
        R(988, 196, 1086, GY, (70, 48, 42))
        if st['oldshop']:
            lit.append((994, 202, 1080, 256, (236, 170, 100)))
            lit.append((994, 202, 1080, 214, (250, 196, 124)))
            emis.append((1037, 236, 60, (255, 190, 120), 0.2))
            streaks.append((1037, 230, (255, 190, 120), 9, 0.3))
        else:
            R(994, 202, 1080, 256, (48, 40, 46))
        post = []
        for k in range(1, 6):
            post.append(([(994 + k * 14.3, 202), (994 + k * 14.3, 256)], (70, 48, 42), None))
        for k in range(1, 4):
            post.append(([(994, 202 + k * 13.5), (1080, 202 + k * 13.5)], (70, 48, 42), None))
        post.append(([(1037, 202), (1037, 256)], (60, 40, 36), max(1, int(2 * z))))
        # plaque
        R(1002, 176, 1072, 190, (52, 34, 30))
        texts.append(('杂货铺', 1037, 176, (226, 196, 140), 1, None))
        # bench
        R(1098, 244, 1160, 248, (96, 70, 56)); R(1102, 248, 1106, GY, (70, 50, 42)); R(1152, 248, 1156, GY, (70, 50, 42))
        # roof + eave (the 屋檐)
        PG([(944, 172), (1186, 172), (1170, 124), (960, 124)], (52, 54, 68))
        k = 0
        xx = 946
        while xx < 1186:
            LN([(xx + 3, 126), (xx + 1, 170)], (66, 70, 88))
            xx += 8
        R(940, 118, 1190, 126, (44, 46, 58))
        R(936, 116, 944, 124, (44, 46, 58)); R(1186, 116, 1194, 124, (44, 46, 58))
        xx = 944
        while xx < 1188:
            ELL(xx + 4, 173, 4, 3.4, (70, 74, 92))
            ELL(xx + 4, 172.4, 2.2, 1.6, (96, 100, 120))
            xx += 8
        R(944, 176, 1186, 178, (30, 30, 40))
        # lantern under eave
        LN([(1176, 178), (1176, 186)], (40, 30, 30))
        ELL(1176, 194, 7, 9, (210, 60, 52) if st['lantern'] else (110, 44, 46))
        R(1171, 184, 1181, 186, (60, 40, 30)); R(1171, 202, 1181, 204, (60, 40, 30))
        if st['lantern']:
            emis.append((1176, 194, 30, (255, 120, 80), 0.6))
        # ---- B8 bus stop ----
        R(1180, 0, 1360, GY, (60, 62, 82))
        cornice(1180, 1360, 0)
        windows(1180, 1360, [24, 84, 140], None, litp=0.4, seed=8, ww=28)
        R(1196, 194, 1330, 199, (120, 124, 140))
        LN([(1200, 199), (1200, GY)], (110, 114, 130)); LN([(1326, 199), (1326, GY)], (110, 114, 130))
        R(1202, 200, 1288, 250, (52, 60, 80))
        lit.append((1292, 204, 1320, 252, (210, 220, 236)))
        lit.append((1296, 210, 1316, 230, (120, 170, 200)))
        emis.append((1306, 228, 50, (200, 220, 240), 0.3))
        R(1210, 236, 1280, 240, (110, 114, 130))
        # ---- B9 corner ----
        R(1360, 50, 1640, GY, (64, 60, 80))
        cornice(1360, 1640, 50)
        windows(1360, 1640, [74, 130], None, litp=0.42, seed=9)
        R(1370, 180, 1630, 256, (48, 46, 62))
        for k in range(5):
            R(1378 + k * 50, 188, 1420 + k * 50, 250, (34, 36, 50))
        # traffic light
        LN([(1452, GY), (1452, 150)], (70, 72, 88), w=max(1, int(3 * z)))
        R(1444, 150, 1460, 182, (36, 36, 44))
        sig = st['signal']
        ELL(1452, 158, 4, 4, (230, 60, 60) if sig == 'red' else (70, 40, 40))
        ELL(1452, 174, 4, 4, (80, 230, 160) if sig == 'green' else (40, 60, 50))
        emis.append((1452, 158 if sig == 'red' else 174, 26, (255, 70, 70) if sig == 'red' else (80, 255, 170), 0.55))
        streaks.append((1452, 166, (255, 80, 80) if sig == 'red' else (80, 255, 170), 4, 0.4))
        # ---- lamps ----
        for lx in LAMPS:
            LN([(lx, GY), (lx, 128)], (60, 62, 76), w=max(1, int(3 * z)))
            LN([(lx, 128), (lx + 4, 120), (lx + 16, 118)], (60, 62, 76), w=max(1, int(2 * z)))
            R(lx + 10, 116, lx + 24, 122, (50, 50, 60))
            lit.append((lx + 12, 121, lx + 22, 124, (255, 220, 160)))
            emis.append((lx + 17, 124, 54, (255, 186, 110), 0.42))
            streaks.append((lx + 17, 124, (255, 190, 120), 6, 0.5))
        # ---- ground ----
        R(-10, GY, WORLD_W + 10, CURB0, (52, 54, 72))
        xx = 0
        while xx < WORLD_W:
            LN([(xx, GY), (xx - 6, CURB0)], (46, 48, 64))
            xx += 24
        LN([(0, GY + 10), (WORLD_W, GY + 10)], (48, 50, 66))
        R(-10, CURB0, WORLD_W + 10, CURB1, (90, 94, 116))
        R(-10, CURB1, WORLD_W + 10, 600, (30, 32, 46))
        for xx in range(0, WORLD_W, 90):
            R(xx, 330, xx + 44, 333, (70, 72, 86))
        img = np.asarray(im, np.float32).copy()
        img = grade(img, variant)
        # sky replaced after grading for memory/moon (keep their own colours)
        # lit rects (not graded)
        lvar = 1.0 if variant != 'moon' else 0.85
        for (x0, y0, x1, y1, c) in lit:
            a, b = T(x0, y0); cc, dd = T(x1, y1)
            a, b, cc, dd = int(round(a)), int(round(b)), int(round(cc)), int(round(dd))
            if dd <= 0 or b >= Hh:
                continue
            col = np.asarray(c, np.float32) * lvar
            if variant == 'memory':
                col = np.minimum(255, col * np.array([1.1, 1.0, 0.85]) + 10)
            img[max(0, b):max(0, dd), max(0, a):max(0, cc)] = col
        if post:
            im2 = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
            d2 = ImageDraw.Draw(im2)
            for pts, c, w_ in post:
                cc = np.asarray(c, np.float32)
                if variant == 'memory':
                    cc = np.clip(cc * np.array([1.42, 1.08, 0.86]) + np.array([22, 8, 0]), 0, 255)
                d2.line([tuple(round(v) for v in T(x, y)) for x, y in pts], fill=tuple(int(v) for v in cc), width=w_ or lw)
            img = np.asarray(im2, np.float32).copy()
        for (s_, wx, wy, col, sc, ol) in texts:
            k = max(1, int(round(z * sc)))
            m = text_mask(s_, 16)
            if k > 1:
                m = np.repeat(np.repeat(m, k, 0), k, 1)
            x, y = T(wx, wy)
            x = int(round(x - m.shape[1] / 2)); y = int(round(y))
            sub = np.zeros(img.shape[:2], bool)
            ys0, xs0 = max(0, y), max(0, x)
            ys1, xs1 = min(Hh, y + m.shape[0]), min(img.shape[1], x + m.shape[1])
            if ys1 > ys0 and xs1 > xs0:
                sub[ys0:ys1, xs0:xs1] = m[ys0 - y:ys1 - y, xs0 - x:xs1 - x]
                if ol is not None:
                    img[outline_of(sub)] = ol
                img[sub] = col
        res = dict(img=img, emis=emis, streaks=streaks, z=z, cam_y=cam_y, T=T)
        self._cache[key] = res
        return res


STREET = Street()


def render_street(cam_x, cam_y, z, variant='night', state=None, t=0.0, rain_on=True, wet=True, glow=True,
                  rain_density=1.0, reflect_k=0.4, extra=None, ow=None, oh=None):
    """returns (frame 640x360, info). cam_x/cam_y are world coords of the screen's top-left."""
    ow = W if ow is None else ow
    oh = H if oh is None else oh
    S = STREET.strip(z, cam_y, variant, state, hh=oh)
    x0 = int(round(cam_x * z))
    x0 = max(0, min(S['img'].shape[1] - ow, x0))
    img = S['img'][:, x0:x0 + ow].copy()
    if img.shape[1] < ow:
        img = np.concatenate([img, np.repeat(img[:, -1:], ow - img.shape[1], 1)], 1)
    T = lambda x, y: (x * z - x0, (y - cam_y) * z)
    info = dict(T=T, z=z, x0=x0)
    if glow:
        for (wx, wy, r, c, s) in S['emis']:
            sx, sy = T(wx, wy)
            if -r * z < sx < ow + r * z:
                stepped_glow(img, sx, sy, r * min(z, 1.6), c, k=s / max(1.0, z) ** 0.6, levels=4)
        # light pools on the sidewalk under lamps
        for lx in LAMPS:
            sx, sy = T(lx + 17, GY + 11)
            if -80 * z < sx < ow + 80 * z:
                stepped_glow(img, sx, sy, 58 * z, (255, 180, 110), k=0.22, levels=3, sy=0.18)
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
