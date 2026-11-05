# -*- coding: utf-8 -*-
"""Her room (warm lamp, yellow curtains, fairy lights), her desk top-down, window views."""
import numpy as np, math, functools
from core import *
from skyline import moon


@functools.lru_cache(maxsize=4)
def room_bg(rain_out=False, cloud_x=None):
    """interior: wall left, window right (x 360-600, y 40-250) with night sky + moon + city."""
    img = new(C('#6b4a52'))
    # wall bands (lamp from left)
    for i, c in enumerate([C('#8c5e5a'), C('#7f5658'), C('#724e56'), C('#674853'), C('#5d4250'), C('#553d4c')]):
        img[:, i * 110:(i + 1) * 110] = c
    # wallpaper dots (static)
    for y in range(8, H, 18):
        for x in range((y // 18) % 2 * 9, 360, 18):
            img[y:y + 2, x:x + 2] = img[y, x] * 1.08
    # window
    X0, Y0, X1, Y1 = 366, 34, 600, 252
    sky = [C('#16203c'), C('#1a2644'), C('#1f2d4e'), C('#253558'), C('#2c3e62'), C('#35486c')]
    vgrad_bands(img, Y0, Y1, sky[0], sky[-1], 6, X0, X1)
    rng = np.random.default_rng(4)
    for i in range(40):
        img[rng.integers(Y0, Y0 + 120), rng.integers(X0, X1)] = (210, 214, 240)
    moon(img, 548, 78, 15, glow=0.8)
    # far city in window
    x = X0
    while x < X1:
        bw = int(rng.integers(16, 40)); top = int(rng.integers(170, 215))
        img[top:Y1, x:min(X1, x + bw)] = (34, 32, 58)
        for yy in range(top + 4, Y1 - 2, 8):
            for xx in range(x + 3, min(X1, x + bw) - 3, 6):
                if rng.random() < 0.25:
                    img[yy:yy + 3, xx:xx + 2] = (236, 176, 104) if rng.random() < 0.7 else (150, 186, 214)
        x += bw + 2
    # frame + mullion
    fr = C('#e6dccf'); frd = C('#b8aa9c')
    img[Y0 - 6:Y0, X0 - 6:X1 + 6] = fr
    img[Y1:Y1 + 6, X0 - 6:X1 + 6] = fr
    img[Y0 - 6:Y1 + 6, X0 - 6:X0] = fr
    img[Y0 - 6:Y1 + 6, X1:X1 + 6] = fr
    img[Y0:Y1, 481:487] = fr
    img[Y0:Y1, 486:487] = frd
    img[Y1 + 5:Y1 + 6, X0 - 6:X1 + 6] = frd
    # sill
    img[Y1 + 6:Y1 + 16, X0 - 16:X1 + 16] = C('#f0e6da')
    img[Y1 + 15:Y1 + 18, X0 - 16:X1 + 16] = C('#a8988c')
    # curtains (yellow) both sides with folds
    for (a, b_) in ((X0 - 34, X0 + 16), (X1 - 16, X1 + 34)):
        img[10:Y1 + 40, a:b_] = C('#e7b84a')
        for k in range(a + 4, b_, 9):
            img[10:Y1 + 40, k:k + 3] = C('#c99632')
            img[10:Y1 + 40, k + 3:k + 4] = C('#f5d27a')
        img[Y1 + 36:Y1 + 40, a:b_] = C('#c99632')
    img[6:12, X0 - 40:X1 + 40] = C('#8a6a50')
    # fairy lights along the top
    for i in range(18):
        x = 20 + i * 34
        y = 22 + int(10 * math.sin(i * 0.9) ** 2)
        img[y - 1:y + 2, x - 1:x + 2] = (255, 214, 140)
        stepped_glow(img, x, y, 10, (255, 200, 120), k=0.4, levels=2)
    for i in range(17):
        x0, x1 = 20 + i * 34, 54 + i * 34
        for x in range(x0, x1):
            u = (x - x0) / 34
            y = 22 + int(10 * math.sin((i + u) * 0.9) ** 2) - int(4 * math.sin(u * math.pi))
            img[y, x] = (60, 40, 40)
    # shelf left with books + small plant
    img[120:126, 30:200] = C('#9a6a50')
    img[126:128, 30:200] = C('#5a3a34')
    for k, (w_, hgt, c) in enumerate(((10, 30, '#5a7a9a'), (8, 26, '#c96a5a'), (12, 32, '#e0c27a'), (9, 24, '#7a9a72'), (11, 28, '#8a6aa0'))):
        x = 40 + k * 13
        img[120 - hgt:120, x:x + w_] = C(c)
        img[120 - hgt:120 - hgt + 2, x:x + w_] = C(c) * 1.2
    img[100:120, 150:166] = C('#b36a50')
    fill(img, m_ellipse(158, 96, 12, 9), C('#5f9a72'))
    # lamp glow from the left
    stepped_glow(img, 0, 200, 280, (255, 190, 120), k=0.22, levels=4)
    return img


@functools.lru_cache(maxsize=1)
def desk_bg():
    img = new(C('#9a6648'))
    for y in range(0, H, 44):
        img[y:y + 1] = C('#7a4c38')
        img[y + 1:y + 2] = C('#ae7a58')
    rng = np.random.default_rng(3)
    for i in range(60):
        x, y = rng.integers(0, W - 40), rng.integers(0, H)
        img[y, x:x + rng.integers(10, 40)] = C('#8e5c42')
    # open book (left)
    bk = m_poly([(60, 90), (230, 70), (250, 250), (80, 280)])
    img[bk] = C('#f2ead8')
    img[outline_of(bk)] = C('#6a5040')
    sp = m_line([(152, 80), (166, 265)], 2)
    img[sp] = C('#cfc4ae')
    for k in range(9):
        y0 = 104 + k * 16
        img[m_line([(84, y0 + 4), (146, y0 - 4)], 1)] = C('#b0a690')
        img[m_line([(172, y0 - 6), (232, y0 - 14)], 1)] = C('#b0a690')
    # pencil
    pc = m_line([(270, 300), (380, 330)], 5)
    img[pc] = C('#e8b84a')
    img[m_line([(380, 330), (392, 333)], 3)] = C('#3a2a2a')
    # mug (right of centre)
    mx, my = 430, 170
    sh = m_ellipse(mx + 8, my + 8, 46, 46)
    img[sh] = img[sh] * 0.75
    hd = m_ellipse(mx + 52, my, 14, 10) & ~m_ellipse(mx + 52, my, 7, 4)
    img[hd] = C('#e8e2da'); img[outline_of(hd)] = C('#7a6a62')
    cup = m_ellipse(mx, my, 44, 44)
    img[cup] = C('#efe9e2')
    img[inner_edge(cup, 1, 1, 3)] = C('#c8beb4')
    img[outline_of(cup)] = C('#7a6a62')
    tea = m_ellipse(mx, my, 36, 36)
    img[tea] = C('#8a4e2a')
    img[inner_edge(tea, -1, -1, 2)] = C('#5a3220')
    img[tea & ~m_ellipse(mx + 4, my + 4, 34, 34)] = C('#a8683a')
    # lamp light
    stepped_glow(img, 120, 40, 320, (255, 200, 140), k=0.18, levels=4)
    return img, (mx, my, 36)
