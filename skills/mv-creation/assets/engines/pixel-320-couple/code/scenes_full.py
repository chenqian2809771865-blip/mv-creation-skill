# -*- coding: utf-8 -*-
"""《晴天》正片新场景：教室前方黑板、课桌纸条特写、雾玻璃窗、谱架、手部、地上的红伞、雨后彩虹。"""
import math
from functools import lru_cache
import numpy as np
from px import (Cv, hx, mix, vgrad, bayer, outline, W, H, OUT, ease, ease_out, seg, clamp, text, text_w, glyph)
from scenes import cloud_sprite, rain, splashes, ripples, glow, _parts, umbrella, RED_UMB
from ui_tiny import pix

CHALK = hx('#e8eee4')
CHALK_Y = hx('#f2e08a')
GRAPHITE = hx('#4a4650')

# ================================================================ front of the classroom: blackboard + podium
BOARD = dict(x=24, y=42, w=272, h=76)


@lru_cache(maxsize=4)
def board_static(mode='day'):
    D = mode == 'day'
    c = Cv(W, H, hx('#e4d2ae'))
    c.rect(0, 0, W, 6, hx('#f2e8d4')); c.rect(0, 6, W, 2, hx('#c8b48e'))
    for x in range(0, W, 40):
        c.rect(x, 8, 1, 140, hx('#d8c49e'))
    # small TV above the board (the same set as the opening)
    c.rect(158, 8, 4, 6, hx('#6a6874'))
    c.rect(140, 14, 40, 24, OUT); c.rect(141, 15, 38, 22, hx('#3c3a46')); c.rect(144, 17, 32, 17, hx('#181a22'))
    # blackboard
    b = BOARD
    c.rect(b['x'] - 4, b['y'] - 4, b['w'] + 8, b['h'] + 8, hx('#6a4a32')); c.rect(b['x'] - 4, b['y'] - 4, b['w'] + 8, 1, hx('#8a6444'))
    c.rect(b['x'], b['y'], b['w'], b['h'], hx('#2e5244'))
    r = np.random.default_rng(3)
    for i in range(14):  # erased smudges
        x, y = r.uniform(b['x'], b['x'] + b['w'] - 40), r.uniform(b['y'], b['y'] + b['h'] - 12)
        m = Cv(W, H, alpha=True); m.ellipse(x + 20, y + 6, r.uniform(10, 26), r.uniform(3, 7), (255, 255, 255))
        mm = (m.a[..., 3] > 0) & (bayer() < 0.25)
        c.a[mm] = hx('#3a5e50')
    # chalk tray + chalk
    c.rect(b['x'] - 6, b['y'] + b['h'] + 4, b['w'] + 12, 3, hx('#5a3e2a'))
    for i, (x, col) in enumerate(((60, CHALK), (66, CHALK_Y), (250, hx('#f29a9a')))):
        c.rect(x, b['y'] + b['h'] + 3, 5, 1, col)
    text(c, b['x'] + 4, b['y'] + 2, '7月31日' if D else '7月31日', hx('#cfd8cc'), font='w')
    text(c, b['x'] + b['w'] - 66, b['y'] + 2, '值日生：', hx('#cfd8cc'), font='w')
    # floor + podium
    c.rect(0, 148, W, 32, hx('#a88a62'))
    for y in range(152, 180, 7):
        c.rect(0, y, W, 1, hx('#94764e'))
    c.rect(96, 128, 128, 6, hx('#9a6a44')); c.rect(96, 134, 128, 16, hx('#7a5034')); c.rect(96, 128, 128, 1, hx('#b88a5a'))
    # teacher's desk on the podium with the flower bottle
    c.rect(130, 112, 60, 5, hx('#b88a5a')); c.rect(132, 117, 56, 11, hx('#8a5a3a'))
    c.rect(176, 103, 6, 9, hx('#9ac8d0')); c.rect(177, 104, 1, 7, hx('#d8f0f4'))
    c.line(179, 103, 177, 95, hx('#4a7a3a')); c.line(179, 103, 183, 97, hx('#4a7a3a'))
    c.ellipse(177, 94, 2, 2, hx('#ffd23a')); c.ellipse(183, 96, 2, 2, hx('#ffd23a')); c.px(177, 94, hx('#b8861a'))
    # door at right
    c.rect(300, 40, 20, 108, hx('#8a6a4a')); c.rect(302, 44, 14, 30, hx('#a8d0e8'))
    return c


def desk_row(c, y, s=1.0, n=5, x0=-6, gap=70, col=hx('#c89a5a'), dk=hx('#8a6234')):
    for i in range(n):
        x = x0 + i * gap
        w = int(40 * s)
        c.rect(x, y, w, int(4 * s), col); c.rect(x, y + int(4 * s), w, int(10 * s), dk)
        c.rect(x + 2, y + int(14 * s), 2, int(6 * s), hx('#4a4a54')); c.rect(x + w - 4, y + int(14 * s), 2, int(6 * s), hx('#4a4a54'))


# ================================================================ desk close-up (160x90 native, shown x2)
def desk_top(c, t, sun=True):
    vgrad(c, 0, c.h, [hx('#d8a868'), hx('#c8955a'), hx('#b8864e')] if sun else [hx('#6a5a50'), hx('#5a4a42')])
    for y in range(4, c.h, 9):
        for x in range(0, c.w, 1):
            if (x * 7 + y * 3) % 23 < 2:
                c.px(x, y + int(2 * math.sin(x * 0.05 + y)), hx('#a8763e') if sun else hx('#4a3c36'))
    # textbook corner + pencil case
    c.poly([(-4, 56), (30, 50), (36, 92), (-4, 92)], hx('#3a6aa8')); c.poly([(-4, 56), (30, 50), (31, 53), (-4, 59)], hx('#f2ece0'))
    c.rect(132, 4, 34, 10, hx('#e86a6a')); c.rect(132, 4, 34, 2, hx('#f29a9a'))


def note_paper(c, cx, cy, w, h, unfold=1.0, crease=True, sun=True):
    """lined note paper centred at (cx,cy). unfold 0 = folded small square."""
    ww = int(26 + (w - 26) * ease_out(unfold))
    hh = int(18 + (h - 18) * ease_out(unfold))
    x0, y0 = int(cx - ww / 2), int(cy - hh / 2)
    paper = hx('#fbf6ea') if sun else hx('#c8c4c0')
    c.rect(x0 + 2, y0 + 2, ww, hh, mix(hx('#7a5a3a'), (0, 0, 0), 0.2))  # shadow
    c.rect(x0, y0, ww, hh, paper)
    if unfold > 0.6:
        for yy in range(y0 + 12, y0 + hh - 2, 13):
            c.rect(x0 + 3, yy, ww - 6, 1, hx('#bcd4ec') if sun else hx('#8a96a8'))
        c.rect(x0 + 8, y0 + 1, 1, hh - 2, hx('#f2b8b8') if sun else hx('#a88a8a'))
    if crease:
        c.rect(int(cx), y0, 1, hh, mix(paper, (0, 0, 0), 0.08))
    c.rect(x0, y0, ww, 1, mix(paper, (255, 255, 255), 0.5))
    return x0, y0, ww, hh


def sleeve_hand(c, x, y, who='he', ang=0.0, L=40, pencil=False, finger=False):
    """an arm coming in from off-frame ending at hand (x,y). ang: direction the forearm points (deg, 0 = up)."""
    a = math.radians(ang)
    dx, dy = math.sin(a), -math.cos(a)
    sx, sy = x - dx * L, y - dy * L
    top, dk = (hx('#3b5b98'), hx('#2a4375')) if who == 'he' else (hx('#efe4cb'), hx('#cdbd9c'))
    skin, sd = (hx('#f2c9a8'), hx('#d9a083')) if who == 'he' else (hx('#f6d0b2'), hx('#dfa689'))
    nx, ny = -dy, dx
    wdt = 7
    pts = [(sx + nx * wdt, sy + ny * wdt), (x - dx * 7 + nx * wdt, y - dy * 7 + ny * wdt),
           (x - dx * 7 - nx * wdt, y - dy * 7 - ny * wdt), (sx - nx * wdt, sy - ny * wdt)]
    c.poly(pts, top)
    c.line(pts[1][0], pts[1][1], pts[2][0], pts[2][1], dk)
    c.line(pts[0][0], pts[0][1], pts[1][0], pts[1][1], OUT); c.line(pts[2][0], pts[2][1], pts[3][0], pts[3][1], OUT)
    c.ellipse(x, y, 6, 5, skin)
    c.ellipse(x + nx * 2, y + ny * 2 + 1, 4, 3, sd)
    if pencil:
        c.line(x + 2, y - 1, x + 2 + dx * -10 + 6, y - 9, hx('#f2c84a'))
        c.line(x + 3, y - 1, x + 3 + dx * -10 + 6, y - 9, hx('#d8a82a'))
        c.px(x + 1, y + 1, GRAPHITE)
    if finger:
        c.rect(x - 1, y - 9, 3, 6, skin); c.px(x, y - 9, mix(skin, (255, 255, 255), 0.3))


# ================================================================ fogged window close-up
def fog_window(t, present=True, mask=None, mask_xy=(0, 0), reveal=None, seed=1):
    """full-frame window. mask: bool text mask written in the fog at mask_xy (cols < reveal visible)."""
    c = Cv(W, H, hx('#c9b892') if not present else hx('#4a4438'))
    gx0, gy0, gx1, gy1 = 18, 10, 302, 146
    # outside
    sub = Cv(gx1 - gx0, gy1 - gy0)
    if present:
        vgrad(sub, 0, sub.h, [hx('#1a1e30'), hx('#262b42'), hx('#343a54'), hx('#3e4460')])
        for i in range(4):
            cs = cloud_sprite(90, 36, 40 + i, hx('#2a2f46'), hx('#3e445e'), hx('#1c2032'))
            sub.blit(cs, int((i * 80 - t * 30) % (sub.w + 120)) - 90, -6 + i * 8)
        sub.rect(0, 100, sub.w, 36, hx('#1a1e2a'))
        rain(sub, t, 90, 81, speed=360, wind=-150, length=8, col=hx('#7a8ab0'), area=(0, 0, sub.w, sub.h))
    else:
        vgrad(sub, 0, sub.h, [hx('#3a5a72'), hx('#4a6a80'), hx('#5a7a8a'), hx('#6a8a90')])
        sub.rect(0, 100, sub.w, 36, hx('#3e5a44'))
        for i in range(6):
            sub.ellipse(20 + i * 48, 100, 22, 12, hx('#2e4a36'))
        # two figures sharing a red umbrella in the yard (soft, far)
        x = 150 + 10 * math.sin(t * 0.4)
        for dx, col in ((-4, hx('#3b5b98')), (4, hx('#efe4cb'))):
            sub.rect(x + dx - 2, 92, 4, 12, col)
        umbrella(sub, x, 92, *RED_UMB, open_=1.0, w=24, tilt=-4, shaft=8)
        rain(sub, t, 50, 82, speed=200, wind=-30, length=6, col=hx('#d8e0ec'), area=(0, 0, sub.w, sub.h))
    clear = sub.a.copy()
    # fog layer
    fogc = hx('#5c6478') if present else hx('#e4e8ec')
    fogk = 0.78 if present else 0.86
    fog = np.clip(clear.astype(np.float32) * (1 - fogk) + np.array(fogc) * fogk, 0, 255).astype(np.uint8)
    out = fog.copy()
    r = np.random.default_rng(seed)
    beads = r.random(out.shape[:2]) < 0.025
    out[beads] = mix(fogc, (255, 255, 255), 0.35)
    if mask is not None:
        mx, my = mask_xy
        mm = np.zeros(out.shape[:2], bool)
        hh, ww = mask.shape
        m2 = mask.copy()
        if reveal is not None:
            m2[:, int(reveal):] = False
        # widen strokes by 1 (finger is wider than a font stroke)
        m3 = m2.copy(); m3[1:, :] |= m2[:-1, :]; m3[:, 1:] |= m2[:, :-1]
        y0, x0 = my - gy0, mx - gx0
        ys, xs = np.nonzero(m3)
        ys, xs = ys + y0, xs + x0
        ok = (ys >= 0) & (ys < out.shape[0]) & (xs >= 0) & (xs < out.shape[1])
        mm[ys[ok], xs[ok]] = True
        out[mm] = clear[mm]
        # drips running down from the strokes
        cols = np.unique(xs[ok])
        for x in cols[::5]:
            yb = ys[ok][xs[ok] == x].max()
            L = int(3 + (int(x * 7) % 9))
            for k in range(L):
                if yb + k < out.shape[0]:
                    out[yb + k, x] = clear[yb + k, x]
    c.a[gy0:gy1, gx0:gx1] = out
    # frame + mullion + sill
    fr = hx('#3a3630') if present else hx('#e8e0cc')
    c.rect(gx0 - 4, gy0 - 4, gx1 - gx0 + 8, 4, fr); c.rect(gx0 - 4, gy1, gx1 - gx0 + 8, 4, fr)
    c.rect(gx0 - 4, gy0, 4, gy1 - gy0, fr); c.rect(gx1, gy0, 4, gy1 - gy0, fr)
    c.rect(159, gy0, 3, gy1 - gy0, fr)
    c.rect(0, 150, W, 8, hx('#5a5244') if present else hx('#ddd2b8')); c.rect(0, 157, W, 1, hx('#3a342c') if present else hx('#a8987a'))
    c.rect(0, 158, W, 22, hx('#3a3a46') if present else hx('#6f8a6a'))
    return c


def flower_bottle(c, x, y, t, drop=0.0, present=True):
    """bottle on the sill (bottom at y). drop>0: petals falling (count)."""
    gl = hx('#5a7a84') if present else hx('#9ac8d0')
    c.rect(x - 4, y - 14, 9, 14, gl); c.rect(x - 3, y - 13, 1, 11, mix(gl, (255, 255, 255), 0.5))
    c.rect(x - 2, y - 17, 5, 3, gl)
    st = hx('#2e4a2a') if present else hx('#4a7a3a')
    c.line(x, y - 17, x - 3, y - 32, st); c.line(x, y - 17, x + 5, y - 28, st)
    fl = hx('#c8a830') if present else hx('#ffd23a')
    c.ellipse(x - 3, y - 33, 3, 3, fl); c.ellipse(x + 5, y - 29, 3, 3, fl)
    c.px(x - 3, y - 33, hx('#8a6a1a')); c.px(x + 5, y - 29, hx('#8a6a1a'))
    for i in range(int(drop)):
        ph = (t * 0.6 + i * 0.37) % 1
        px_ = x + 4 + 14 * ph + 3 * math.sin(t * 4 + i)
        py_ = y - 30 + ph * 32
        c.rect(px_, py_, 2, 1, fl)


# ================================================================ music stand + sheet
def music_sheet(c, x, y, w, h):
    c.rect(x + 2, y + 2, w, h, hx('#8a6a4a'))
    c.rect(x, y, w, h, hx('#fbf6ea')); c.rect(x, y, w, 1, hx('#ffffff'))
    return x, y


def staff(c, x, y, w, col=hx('#6a6070')):
    for k in range(5):
        c.rect(x, y + k * 3, w, 1, col)
    # treble-ish clef
    pix(c, [".#.", "#.#", "#.#", ".#.", "##.", "#.#", ".#.", ".#.", "#.."], x + 1, y - 3, col)


def note_head(c, x, y, col=hx('#2a2430'), stem_up=True):
    c.ellipse(x + 1.5, y + 1, 2.2, 1.6, col)
    if stem_up:
        c.rect(x + 3, y - 8, 1, 9, col)
    else:
        c.rect(x, y + 1, 1, 9, col)


def guitar(c, x, y, s=1, strum=0.0, flip=False):
    """acoustic guitar held across the lap; (x,y) = body centre."""
    f = -1 if flip else 1
    body, dk, lt = hx('#c8823a'), hx('#8a5424'), hx('#e8a858')
    c.ellipse(x, y, 9 * s, 7 * s, body)
    c.ellipse(x - f * 8 * s, y - 1 * s, 7 * s, 6 * s, body)
    c.ellipse(x - f * 3 * s, y, 2.4 * s, 2.4 * s, hx('#2a1a12'))
    c.ellipse(x + f * 2 * s, y - 3 * s, 3 * s, 1.5 * s, lt)
    # neck
    for k in range(int(3 * s)):
        c.line(x - f * 14 * s, y - 2 * s + k, x - f * 34 * s, y - 12 * s + k, hx('#4a3020'))
    c.rect(x - f * 36 * s - (3 * s if not flip else 0), y - 15 * s, 4 * s, 4 * s, hx('#2a1a12'))
    # strings
    c.line(x + f * 6 * s, y - 1 * s, x - f * 34 * s, y - 12 * s, hx('#e8e0d0'))
    if strum > 0:
        c.px(x - f * 1 * s, y - 4 * s - strum * 2, hx('#ffffff'))


# ================================================================ rainbow + puddles
def rainbow(c, cx, cy, r, alpha=1.0, width=2):
    cols = [hx('#ff6a6a'), hx('#ffb04a'), hx('#ffe06a'), hx('#7ad87a'), hx('#6ab0ff'), hx('#9a7aff')]
    yy, xx = np.mgrid[0:c.h, 0:c.w]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    for i, col in enumerate(cols):
        rr = r - i * width
        m = (d >= rr - width) & (d < rr) & (yy < cy) & (bayer(c.h, c.w) < 0.55 * alpha)
        c.a[m] = np.clip(c.a[m].astype(np.float32) * 0.45 + np.array(col) * 0.55, 0, 255).astype(np.uint8)


def puddle(c, x, y, rx, ry, sky_col, t=0.0, seed=1):
    m = Cv(W, H, alpha=True); m.ellipse(x, y, rx, ry, (255, 255, 255))
    mm = m.a[..., 3] > 0
    c.a[mm] = np.clip(c.a[mm].astype(np.float32) * 0.35 + np.array(sky_col) * 0.65, 0, 255).astype(np.uint8)
    c.hline(x - rx * 0.6, x + rx * 0.2, y - ry * 0.3, mix(sky_col, (255, 255, 255), 0.5))


# ================================================================ hands holding (160x90 native)
def _hand_piece(w, h, parts, skin):
    cc = Cv(w, h, alpha=True)
    for pp in parts:
        if pp[0] == 'e':
            cc.ellipse(pp[1], pp[2], pp[3], pp[4], skin)
        else:
            cc.poly(pp[1], skin)
    return outline(cc)


def draw_hands(c, t, grip=1.0):
    """his hand (left, navy sleeve) holding hers (right, cream sleeve)."""
    tr = int(round(math.sin(t * 9) * 0.6))
    sk, sd = hx('#f6d0b2'), hx('#dfa689')
    hk, hd = hx('#f2c9a8'), hx('#d9a083')
    her = _hand_piece(110, 60, [('e', 40, 30, 17, 13)] + [('e', 18, 20 + k * 6, 10, 3.2) for k in range(4)] + [('e', 36, 16, 8, 4)], sk)
    for k in range(3):
        her.a[22 + k * 6, 10:26] = (*sd, 255)
    c.blit(her, 50, 16 + tr)
    c.poly([(100, 30), (170, 22), (170, 74), (100, 62)], hx('#efe4cb'))
    c.line(100, 30, 100, 62, OUT)
    for k in range(4):
        c.line(104 + k * 6, 30, 104 + k * 6, 62, hx('#cdbd9c'))
    c.poly([(-10, 24), (40, 28), (40, 70), (-10, 76)], hx('#3b5b98'))
    c.rect(34, 28, 6, 42, hx('#2a4375')); c.line(40, 28, 40, 70, OUT)
    fl = 8 + grip * 12
    parts = [('e', 22, 32, 18, 15)] + [('e', 38 + fl / 2, 22 + k * 6.5, fl, 3.4) for k in range(4)] + [('e', 30, 14, 10, 4.5)]
    hisp = _hand_piece(90, 60, parts, hk)
    for k in range(3):
        hisp.a[25 + int(k * 6.5), 40:40 + int(fl)] = (*hd, 255)
    c.blit(hisp, 26, 14)
