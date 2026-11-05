# -*- coding: utf-8 -*-
"""《晴天》新场景：教室电视 / 天气预报屏、停电教室、暴风雨校园、屋檐、校门。全部画在 320x180 网格上。"""
import math
from functools import lru_cache
import numpy as np
from px import (Cv, hx, mix, mul, vgrad, bayer, outline, W, H, OUT, ease, ease_out, seg, clamp, text, text_w, text_big,
                glyph)
from scenes import cloud_sprite, rain, splashes, ripples, glass_rain, buildings, lamp, glow, _parts
from ui_tiny import tiny, pix

# ================================================================ helpers


def shade(c, k):
    """flat multiply whole canvas (no dither)."""
    c.a[..., :3] = np.clip(c.a[..., :3].astype(np.float32) * np.array(k, np.float32), 0, 255).astype(np.uint8)
    return c


def flash_env(t, t0, dur=0.22):
    if t < t0:
        return 0.0
    return math.exp(-(t - t0) / dur)


def shake(c, dx, dy, fill=None):
    if dx == 0 and dy == 0:
        return c
    a = np.roll(np.roll(c.a, dy, 0), dx, 1)
    if fill is not None:
        if dy > 0: a[:dy] = fill
        if dy < 0: a[dy:] = fill
        if dx > 0: a[:, :dx] = fill
        if dx < 0: a[:, dx:] = fill
    c.a = a
    return c


# ================================================================ weather icons (screen pixel art)
def icon_sun(c, x, y, t, burst=0.0):
    cx, cy = x + 16, y + 16
    rays = 8
    spin = t * 0.6
    L = 5 + int(round(3 * burst))
    for i in range(rays):
        a = spin + i * 2 * math.pi / rays
        x0, y0 = cx + math.cos(a) * 11, cy + math.sin(a) * 11
        x1, y1 = cx + math.cos(a) * (11 + L), cy + math.sin(a) * (11 + L)
        c.line(x0, y0, x1, y1, hx('#ffd23a'))
        c.line(x0 + 1, y0, x1 + 1, y1, hx('#ffb52a'))
    c.ellipse(cx, cy, 9, 9, hx('#ff9e1e'))
    c.ellipse(cx, cy, 8, 8, hx('#ffc630'))
    c.ellipse(cx - 2, cy - 2, 4, 4, hx('#ffe27a'))
    # face
    c.px(cx - 3, cy - 1, hx('#b8561a')); c.px(cx + 3, cy - 1, hx('#b8561a'))
    c.hline(cx - 2, cx + 2, cy + 3, hx('#b8561a'))
    if burst > 0.3:
        for i in range(4):
            a = i * math.pi / 2 + 0.4
            c.px(cx + math.cos(a) * 20, cy + math.sin(a) * 20, hx('#fff6c8'))


def icon_cloud(c, x, y, dark=False):
    if dark:
        cs = cloud_sprite(34, 22, 5, hx('#5a6074'), hx('#7a8094'), hx('#3e4254'))
    else:
        cs = cloud_sprite(34, 22, 5, hx('#e6ecf4'), hx('#ffffff'), hx('#b4bccc'))
    c.blit(outline(cs, hx('#2a3040')), x - 1, y + 4)


def icon_rain(c, x, y, t, heavy=False):
    icon_cloud(c, x, y - 4, dark=True)
    n = 7 if heavy else 4
    for i in range(n):
        ph = (t * (2.6 if heavy else 1.8) + i * 0.37) % 1
        xx = x + 6 + i * (22 // max(1, n - 1)) - ph * 3
        yy = y + 22 + ph * 10
        c.line(xx, yy, xx - 1, yy + 3, hx('#7ec8ff'))


def icon_storm(c, x, y, t, k=1.0):
    icon_rain(c, x, y, t, heavy=True)
    if int(t * 9.3) % 2 == 0 or k > 0.8:
        bolt = [(x + 18, y + 12), (x + 12, y + 22), (x + 17, y + 22), (x + 11, y + 33), (x + 22, y + 19), (x + 16, y + 19), (x + 21, y + 12)]
        c.poly(bolt, hx('#ffe44a'))
        for i in range(len(bolt) - 1):
            c.line(*bolt[i], *bolt[i + 1], hx('#c88a10'))


# ================================================================ the forecast screen
STATES = [  # (label, temp, sky colours, ticker, ticker colour)
    ('晴天', '26°', [hx('#2e6cc0'), hx('#4a8ad6'), hx('#7cb6ec'), hx('#a8d6f6')],
     '明日天气晴 · 微风二级 · 紫外线强 · 适宜出游 · ', hx('#1c3a6e')),
    ('多云', '21°', [hx('#3e5276'), hx('#56688a'), hx('#7a8aa4'), hx('#98a4b8')],
     '明日多云转阴 · 风力渐大 · ', hx('#2a3448')),
    ('大雨', '17°', [hx('#16203a'), hx('#202c4c'), hx('#2c3a5e'), hx('#3a4a70')],
     '明日有大雨 · 出门请带伞 · ', hx('#141c30')),
    ('暴雨', '12°', [hx('#1a0c14'), hx('#2a1018'), hx('#3e141c'), hx('#521a22')],
     '紧急：气象台发布暴雨红色预警 · 请师生尽快回家 · 关好门窗 · ', hx('#a8141e')),
]
SCRAMBLE = '晴天多云阴雨暴风雷电'


def forecast_screen(t, state, flip_p=1.0, burst=0.0, alert_on=True, seed=0):
    """returns 176x100 Cv with the weather programme. state 0..3; flip_p<1 = flip-board scramble."""
    sw, sh = 176, 100
    c = Cv(sw, sh)
    lab, temp, sky, tick, tick_col = STATES[state]
    vgrad(c, 0, sh, sky)
    # soft scanline texture
    for y in range(0, sh, 2):
        c.a[y] = (c.a[y].astype(np.int16) * 0.9).astype(np.uint8)
    # header bar
    c.rect(0, 0, sw, 13, hx('#10203e') if state < 3 else hx('#3a0a10'))
    c.rect(0, 13, sw, 1, hx('#f2c84a') if state < 3 else hx('#ff4a4a'))
    text(c, 4, 0, '周杰伦 · 管弦乐版', hx('#f4f0e6'), font='w')
    tiny(c, sw - 22, 4, '18:00', hx('#f4f0e6'))
    # icon
    ix, iy = 10, 24
    if state == 0:
        icon_sun(c, ix, iy, t, burst)
    elif state == 1:
        icon_cloud(c, ix, iy + 2)
        # sun peeking (only right after the flip)
    elif state == 2:
        icon_rain(c, ix, iy, t)
    else:
        icon_storm(c, ix, iy, t)
    # temperature under icon
    text(c, ix + 2, iy + 44, temp, hx('#ffffff'), outline_col=hx('#10203e') if state < 3 else hx('#3a0a10'))
    # label + big condition
    if state < 3:
        text(c, 62, 18, '明日天气', hx('#e8f0fa'), font='w')
    else:
        c.rect(0, 15, sw, 14, hx('#e0141e') if alert_on else hx('#7a0a12'))
        text(c, 46, 15, '⚠ 暴雨红色预警', hx('#ffffff') if alert_on else hx('#ffb0b0'), font='w')
    big_col = hx('#ffffff') if state < 3 else hx('#ffe9e0')
    shadow = hx('#18305a') if state < 3 else hx('#5a0a12')
    gx, gy = 60, 33
    if flip_p < 1.0:
        r = np.random.default_rng(seed)
        s2 = ''.join(SCRAMBLE[int(i)] for i in r.integers(0, len(SCRAMBLE), 2))
        # split-flap: two panels with a dark seam, glyphs squashed
        for k, ch in enumerate(s2):
            m, adv = glyph(ch)
            mk = np.repeat(np.repeat(m, 3, 0), 3, 1)
            hh = mk.shape[0]
            sq = max(2, int(hh * (0.35 + 0.65 * abs(math.cos(flip_p * math.pi * 2)))))
            idx = np.linspace(0, hh - 1, sq).astype(int)
            mk2 = mk[idx]
            oy = gy + (hh - sq) // 2
            c.mask_fill(mk2, shadow, gx + k * 50 + 2, oy + 2)
            c.mask_fill(mk2, big_col, gx + k * 50, oy)
        c.rect(gx - 2, gy + 23, 104, 1, hx('#0a0a12'))
    else:
        text_big(c, gx + 2, gy + 2, lab, shadow, k=3, sp=2)
        text_big(c, gx, gy, lab, big_col, k=3, sp=2)
        c.rect(gx - 2, gy + 23, 104, 1, mix(sky[1], (0, 0, 0), 0.35))  # split-flap seam
    # alert banner (state 3)
    # ticker
    ty = sh - 14
    c.rect(0, ty, sw, 14, tick_col)
    c.rect(0, ty, sw, 1, hx('#f2c84a') if state < 3 else hx('#ffd23a'))
    if state == 3:
        c.rect(0, ty + 1, 34, 13, hx('#ffd23a'))
        text(c, 3, ty + 1, '紧急', hx('#a8141e'), font='w')
        x0 = 36
    else:
        c.rect(0, ty + 1, 34, 13, hx('#f2c84a'))
        text(c, 3, ty + 1, '预报', hx('#10203e'), font='w')
        x0 = 36
    speed = 46 if state < 3 else 70
    tw = text_w(tick, 'w')
    sub = Cv(sw - x0, 13)
    sub.a[:] = tick_col
    off = int(t * speed) % max(tw, 1)
    text(sub, -off, 0, tick + tick, hx('#ffffff'), font='w')
    c.paste(sub, x0, ty + 1)
    return c


# ================================================================ O1 classroom corner with the TV
TV = dict(x0=50, y0=16, w=220, h=138, sx=72, sy=28, sw=176, sh=100)


@lru_cache(maxsize=4)
def tv_room_static(chalk=True):
    c = Cv(W, H, hx('#e4d2ae'))
    # ceiling strip + cornice
    c.rect(0, 0, W, 8, hx('#f2e8d4')); c.rect(0, 8, W, 2, hx('#c8b48e'))
    # wall texture: faint vertical panel seams
    for x in range(0, W, 40):
        c.rect(x, 10, 1, 148, hx('#d8c49e'))
    # bracket
    c.rect(154, 0, 12, 4, hx('#4a4852')); c.rect(158, 4, 4, 14, hx('#6a6874')); c.rect(158, 4, 1, 14, hx('#8a8894'))
    # blackboard top edge
    c.rect(0, 160, W, 4, hx('#6a4a32')); c.rect(0, 160, W, 1, hx('#8a6444'))
    c.rect(0, 164, W, 16, hx('#2e5244'))
    for x in range(0, W, 3):
        if (x * 7) % 5 == 0:
            c.px(x, 166 + (x % 11), hx('#3a5e50'))
    # chalk (tray shadow)
    if chalk:
        text(c, 10, 165, '7月31日  星期四', hx('#dfe6dc'), font='w')
    text(c, 226, 165, '天气：晴', hx('#dfe6dc'), font='w')
    pix(c, ["..#..", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "..#.."], 278, 167, hx('#f2e6a0'))
    return c


def tv_body(c, led='red', glass=None):
    T = TV
    x0, y0, w, h = T['x0'], T['y0'], T['w'], T['h']
    c.rect(x0 - 1, y0 + 2, w + 2, h - 4, OUT); c.rect(x0 + 2, y0 - 1, w - 4, h + 2, OUT)
    c.rect(x0, y0, w, h, hx('#3c3a46'))
    c.rect(x0, y0, w, 2, hx('#5a5866')); c.rect(x0, y0 + h - 3, w, 3, hx('#2a2832'))
    c.rect(x0 + w - 2, y0, 2, h, hx('#2e2c36'))
    # bezel
    sx, sy, sw, sh = T['sx'], T['sy'], T['sw'], T['sh']
    c.rect(sx - 6, sy - 6, sw + 12, sh + 12, hx('#24222a'))
    c.rect(sx - 6, sy - 6, sw + 12, 1, hx('#1a1820'))
    # control strip
    cy = sy + sh + 9
    for i, kx in enumerate((sx + 8, sx + 22, sx + 36)):
        c.rect(kx, cy, 8, 4, hx('#2a2832')); c.rect(kx + 1, cy + 1, 6, 1, hx('#56545e'))
    c.rect(sx + 60, cy + 1, 60, 2, hx('#2a2832'))  # speaker slot
    c.rect(sx + 60, cy + 1, 60, 1, hx('#1e1c24'))
    lc = {'red': hx('#ff3a3a'), 'green': hx('#5aff7a'), 'off': hx('#3a1a1e')}[led]
    c.rect(sx + sw - 8, cy + 1, 3, 2, lc)
    if led != 'off':
        c.px(sx + sw - 9, cy + 1, mix(lc, (60, 60, 60), 0.6)); c.px(sx + sw - 5, cy + 2, mix(lc, (60, 60, 60), 0.6))
    # brand
    if glass is not None:
        c.paste(glass, sx, sy)


def tv_glass_off(t, refl=0.0, lightning=0.0):
    """dark CRT glass, faint reflection of the window panes."""
    T = TV
    g = Cv(T['sw'], T['sh'], hx('#181a22'))
    vgrad(g, 0, T['sh'], [hx('#1e2230'), hx('#181a24'), hx('#14161e'), hx('#181a22')])
    k = 0.25 + 0.75 * refl
    if k > 0:
        for i, wx in enumerate((14, 60, 106)):
            col = mix(hx('#181a22'), hx('#5a6a90'), 0.35 * k + 0.6 * lightning)
            for y in range(10, 70):
                for x in range(wx + (70 - y) // 6, wx + 34 + (70 - y) // 6):
                    if (x + y) % 2 == 0 and 0 <= x < T['sw']:
                        g.a[y, x] = col
    # highlight curve
    for x in range(10, 60):
        g.px(x, 6 + int((x - 35) ** 2 / 120), hx('#3a3e50'))
    return g


# ================================================================ O2 dark classroom
@lru_cache(maxsize=2)
def classroom_static():
    c = Cv(W, H, hx('#c9b892'))
    c.rect(0, 0, W, 6, hx('#e2d6be')); c.rect(0, 6, W, 2, hx('#a89870'))
    # three tall windows on the back wall
    for wx in (20, 120, 220):
        c.rect(wx - 3, 18, 86, 92, hx('#e8e0cc'))   # frame
        c.rect(wx, 21, 80, 86, hx('#8aa0c0'))         # glass (gets replaced each frame)
        c.rect(wx - 6, 108, 92, 5, hx('#ddd2b8')); c.rect(wx - 6, 112, 92, 1, hx('#a8987a'))  # sill
    # dado
    c.rect(0, 113, W, 2, hx('#8a7a5a')); c.rect(0, 115, W, 20, hx('#6f8a6a')); c.rect(0, 134, W, 2, hx('#55704f'))
    # floor
    c.rect(0, 136, W, 44, hx('#a88a62'))
    for y in range(140, 180, 8):
        c.rect(0, y, W, 1, hx('#94764e'))
    return c


def desk(c, x, y, s=1.0, col=hx('#c89a5a'), dk=hx('#8a6234'), leg=hx('#4a4a54')):
    w = int(34 * s); h = int(4 * s)
    c.rect(x, y, w, h, col); c.rect(x, y + h, w, max(1, int(2 * s)), dk)
    lh = int(14 * s)
    c.rect(x + 2, y + h, max(1, int(2 * s)), lh, leg); c.rect(x + w - 4, y + h, max(1, int(2 * s)), lh, leg)
    # chair back behind
    c.rect(x + w // 2 - int(8 * s), y - int(10 * s), int(16 * s), int(6 * s), mix(col, (0, 0, 0), 0.1))
    c.rect(x + w // 2 - int(8 * s), y - int(4 * s), max(1, int(2 * s)), int(4 * s), leg)
    c.rect(x + w // 2 + int(6 * s), y - int(4 * s), max(1, int(2 * s)), int(4 * s), leg)


def storm_sky(w, h, t, light=0.0, seed=3, speed=1.0):
    sub = Cv(w, h)
    vgrad(sub, 0, h, [hx('#1a1e30'), hx('#262b42'), hx('#343a54'), hx('#3e4460')])
    for i in range(5):
        cs = cloud_sprite(90, 36, seed + i, hx('#2a2f46'), hx('#3e445e'), hx('#1c2032'))
        xx = int((i * 70 - t * 40 * speed * (1 + 0.3 * i)) % (w + 120)) - 90
        sub.blit(cs, xx, -10 + i * 7)
    if light > 0:
        sub.a[:] = np.clip(sub.a.astype(np.float32) + np.array([150, 160, 200]) * light, 0, 255).astype(np.uint8)
    return sub


# ================================================================ O3/O7 schoolyard (storm / sun)
YARD_H = 180


@lru_cache(maxsize=4)
def yard_static(mode='storm'):
    S = mode == 'sun'
    c = Cv(W, H)
    if S:
        vgrad(c, 0, 96, [hx('#5aa0e6'), hx('#7ab8ee'), hx('#a0d0f4'), hx('#c8e6f8')])
    else:
        vgrad(c, 0, 96, [hx('#141828'), hx('#1e2436'), hx('#2a3046'), hx('#363e58')])
    # far city
    buildings(c, 92, 41, hx('#9ab4d0') if S else hx('#1a2034'), win=None if S else hx('#3a4054'), lit=0.1, hmin=8, hmax=22)
    # far ground plane behind the courtyard
    c.rect(0, 92, W, 36, hx('#c4b490') if S else hx('#262a3a'))
    # hedge row between the block and the gate
    for x in range(146, 246, 9):
        c.ellipse(x, 112, 7, 6, hx('#4a7a34') if S else hx('#1a2620'))
    c.rect(140, 112, 106, 16, hx('#4a7a34') if S else hx('#1a2620'))
    # teaching block (left) with covered walkway
    bc, bdk, bwin = (hx('#e8dcc4'), hx('#c8b898'), hx('#8ab4d8')) if S else (hx('#3a3e52'), hx('#2a2e3e'), hx('#1e2232'))
    c.rect(0, 30, 150, 98, bc); c.rect(0, 30, 150, 3, bdk); c.rect(148, 30, 2, 98, bdk)
    # ground floor behind the walkway: darker wall, doors
    c.rect(0, 97, 150, 31, mix(bc, (0, 0, 0), 0.28))
    for dx in (24, 74, 124):
        c.rect(dx, 104, 14, 24, hx('#8a6a4a') if S else hx('#1e1a22')); c.rect(dx + 11, 115, 2, 2, hx('#d8b048') if S else hx('#3a3424'))
    c.rect(0, 124, 160, 4, hx('#b0a890') if S else hx('#30323e'))
    for fy in (38, 58, 78):
        c.rect(0, fy + 16, 150, 2, bdk)
        for wx in range(6, 144, 18):
            c.rect(wx, fy, 12, 12, bwin); c.rect(wx + 6, fy, 1, 12, bdk)
            if S:
                c.rect(wx + 1, fy + 1, 3, 2, hx('#e8f4fc'))
    # flag on roof
    c.rect(128, 12, 1, 18, hx('#c8c8d0') if S else hx('#5a5e70'))
    c.rect(129, 12, 10, 6, hx('#e04040') if S else hx('#7a2a2e'))
    # walkway roof
    c.rect(0, 92, 160, 5, hx('#a8453a') if S else hx('#4a2a2e')); c.rect(0, 96, 160, 1, hx('#7a2e28') if S else hx('#2e1a1e'))
    for px_ in (6, 56, 106, 154):
        c.rect(px_, 97, 4, 31, hx('#d8ccb4') if S else hx('#4a4c5e'))
    # gate (right)
    gc = hx('#b8bccc') if S else hx('#5a5e72')
    c.rect(240, 62, 8, 66, gc); c.rect(304, 62, 8, 66, gc)
    c.rect(234, 56, 84, 7, hx('#8a4a3a') if S else hx('#4a2e2e'))
    c.rect(250, 46, 54, 11, hx('#f0ece0') if S else hx('#8a8a96'))
    text(c, 253, 45, '第三中学', hx('#3a3a4a') if S else hx('#2a2a36'), font='w')
    for x in range(250, 304, 6):
        c.rect(x, 104, 2, 24, hx('#6a6e80') if S else hx('#33364a'))
    c.rect(248, 104, 56, 2, hx('#6a6e80') if S else hx('#33364a'))
    # ground: courtyard
    vgrad(c, 128, H, [hx('#d8c8a4'), hx('#ccb894'), hx('#c0aa84')] if S else [hx('#2c3042'), hx('#262a3a'), hx('#202432')])
    c.rect(0, 128, W, 1, hx('#b8a47e') if S else hx('#3a3e52'))
    # flower bed (bottom-left)
    c.rect(0, 160, 120, 20, hx('#5a8a3a') if S else hx('#1e2e22'))
    c.rect(0, 158, 122, 3, hx('#c8bca0') if S else hx('#3a3c4a'))
    r = np.random.default_rng(5)
    for i in range(70):
        x = r.uniform(2, 118); y = r.uniform(162, 179)
        if S:
            c.px(x, y, hx('#ffd83a')); c.px(x + 1, y, hx('#ffe878')); c.px(x, y + 1, hx('#3e6a2a'))
        else:
            c.px(x, y, hx('#6a6a3a'))
    sky0 = Cv(W, 96)
    if S:
        vgrad(sky0, 0, 96, [hx('#5aa0e6'), hx('#7ab8ee'), hx('#a0d0f4'), hx('#c8e6f8')])
    else:
        vgrad(sky0, 0, 96, [hx('#141828'), hx('#1e2436'), hx('#2a3046'), hx('#363e58')])
    skym = np.all(c.a[:96] == sky0.a, axis=2)
    return c, skym


SWING = dict(x=190, top=112, base=158)


def swing(c, t, ang, S=False):
    """A-frame swing; ang in degrees (0 = hanging)."""
    x, top, base = SWING['x'], SWING['top'], SWING['base']
    fc = hx('#d8584a') if S else hx('#6a3a40')
    fd = hx('#a83a32') if S else hx('#4a2a30')
    for dx in (-26, 26):
        c.line(x + dx - 6, base, x + dx, top, fd); c.line(x + dx - 5, base, x + dx + 1, top, fc)
        c.line(x + dx + 6, base, x + dx, top, fd)
    c.rect(x - 28, top - 2, 57, 3, fc); c.rect(x - 28, top + 1, 57, 1, fd)
    L = 34
    a = math.radians(ang)
    for dx in (-8, 8):
        ex, ey = x + dx + math.sin(a) * L, top + math.cos(a) * L
        c.line(x + dx, top + 1, ex, ey, hx('#9a9aa8') if S else hx('#5a5c6c'))
    sx, sy = x + math.sin(a) * L, top + math.cos(a) * L
    c.rect(sx - 10, sy, 21, 3, hx('#8a5a34') if S else hx('#3a2a26'))
    c.rect(sx - 10, sy + 2, 21, 1, hx('#5a3a22') if S else hx('#2a1e1c'))
    return sx, sy


def tree(c, x, base, t, sway=0.0, S=False, seed=1, h=64):
    tc = hx('#6a4a32') if S else hx('#1e1a22')
    c.rect(x - 2, base - h * 0.5, 5, h * 0.5, tc)
    r = np.random.default_rng(seed)
    for i in range(9):
        ox = r.uniform(-16, 16) + sway * (0.5 + 0.5 * r.random()) * (1 - i / 12)
        oy = -h * 0.55 - r.uniform(0, h * 0.45)
        rad = r.uniform(9, 15)
        col = (hx('#4a8a3a') if i % 2 else hx('#5aa04a')) if S else (hx('#18221e') if i % 2 else hx('#202c26'))
        c.ellipse(x + ox, base + oy, rad, rad * 0.8, col)


def petals(c, t, n=40, seed=12, wind=-150, area=(0, 60, W, 180), col=hx('#ffd83a'), col2=hx('#e8b820'), gust=1.0):
    p = _parts(seed, n)
    x0, y0, x1, y1 = area
    ww, hh = x1 - x0 + 40, y1 - y0
    for i in range(n):
        v = 0.6 + 0.8 * p['v'][i]
        x = (p['x'][i] * ww + wind * v * gust * t) % ww + x0 - 20
        y = y0 + (p['y'][i] * hh + math.sin(t * p['fr'][i] * 5 + p['ph'][i]) * p['amp'][i] * 2 - t * 18 * v) % hh
        cc = col if p['big'][i] > 0.4 else col2
        c.px(x, y, cc)
        if p['big'][i] > 0.7:
            c.px(x + 1, y, cc)


# ================================================================ O4 eaves (side view, closer)
EAVES_Y = 142  # feet line


BB = dict(x=150, y=28, w=124, h=72)  # bulletin board on the walkway wall


@lru_cache(maxsize=4)
def eaves_static(mode='storm'):
    D = mode == 'day'
    c = Cv(W, H, hx('#5a6076'))
    # back wall with windows (classroom side)
    c.rect(0, 0, W, 112, hx('#e0d4bc') if D else hx('#6a6e84'))
    for wx in (10, 80, 290):
        fr = hx('#f2ece0') if D else hx('#9aa0b4')
        c.rect(wx, 30, 44, 50, fr); c.rect(wx + 2, 32, 40, 46, hx('#8ab4d8') if D else hx('#2a3044'))
        c.rect(wx + 21, 32, 2, 46, fr); c.rect(wx, 54, 44, 2, fr)
        if D:
            c.rect(wx + 4, 34, 6, 3, hx('#e8f4fc'))
    # bulletin board (黑板报)
    b = BB
    c.rect(b['x'] - 3, b['y'] - 3, b['w'] + 6, b['h'] + 6, hx('#8a5a3a') if D else hx('#3a2a28'))
    c.rect(b['x'], b['y'], b['w'], b['h'], hx('#2e5244') if D else hx('#1e342c'))
    c.rect(b['x'] - 3, b['y'] - 3, b['w'] + 6, 1, hx('#b07a52') if D else hx('#4a3632'))
    text(c, b['x'] + 4, b['y'] + 1, '班级黑板报', hx('#f2c84a') if D else hx('#8a7a3a'), font='w')
    for k in range(6):
        c.px(b['x'] + 70 + k * 8, b['y'] + 6, hx('#e86a6a') if D else hx('#5a3a3a'))
    c.rect(0, 108, W, 4, hx('#b8a88a') if D else hx('#4a4e62'))
    # floor of the walkway
    c.rect(0, 112, W, 32, hx('#c8c0b0') if D else hx('#7a7a86')); c.rect(0, 112, W, 1, hx('#d8d0c0') if D else hx('#8a8a96'))
    for x in range(0, W, 24):
        c.rect(x, 112, 1, 32, hx('#b8b0a0') if D else hx('#6a6a76'))
    c.rect(0, 144, W, 2, hx('#e0dacc') if D else hx('#9a9aa6'))  # kerb
    # yard beyond (lower)
    if D:
        vgrad(c, 146, H, [hx('#d8c8a4'), hx('#ccb894'), hx('#c0aa84')])
    else:
        c.rect(0, 146, W, 34, hx('#2a2e40'))
    # roof overhang
    c.rect(0, 0, W, 14, hx('#a8453a') if D else hx('#4a2a2e')); c.rect(0, 14, W, 3, hx('#7a2e28') if D else hx('#2e1a1e'))
    # pillars
    for px_ in (40, 286):
        pc, pl, pd = (hx('#e8e0d0'), hx('#fbf6ec'), hx('#c8bca8')) if D else (hx('#8a8c9c'), hx('#a8aab8'), hx('#6a6c7c'))
        c.rect(px_, 17, 10, 127, pc); c.rect(px_, 17, 2, 127, pl); c.rect(px_ + 8, 17, 2, 127, pd)
    return c


def roof_drip(c, t, y0=17, y1=146, seed=4, n=60, col=hx('#a8b8dc')):
    """sheet of water falling from the roof edge."""
    p = _parts(seed, n)
    for i in range(n):
        x = int(p['x'][i] * W)
        sp = 260 * (0.8 + 0.4 * p['v'][i])
        L = 10 + int(10 * p['v'][i])
        y = (p['y'][i] * (y1 - y0) + sp * t) % (y1 - y0) + y0
        c.line(x, y, x, min(y1, y + L), col)


# ================================================================ O5 school gate (front, closer)
GATE_FEET = 150


GB = dict(x=54, y=64, w=100, h=50)  # 黑板报 standing inside the gate (left)


@lru_cache(maxsize=4)
def gate2_static(mode='storm'):
    SUN = mode == 'sun'
    c = Cv(W, H)
    if SUN:
        vgrad(c, 0, 120, [hx('#4a90e0'), hx('#6aaeea'), hx('#96cdf2'), hx('#c4e4f6')])
        buildings(c, 118, 61, hx('#8aa4c4'), win=hx('#e8f4fc'), lit=0.18, hmin=20, hmax=60)
    else:
        vgrad(c, 0, 120, [hx('#161a2c'), hx('#20263c'), hx('#2c3450'), hx('#3a4462')])
        buildings(c, 118, 61, hx('#1c2034'), win=hx('#d8b060'), lit=0.18, hmin=20, hmax=60)
    # gate posts + beam
    gc, gl = (hx('#b8bccc'), hx('#dcdee8')) if SUN else (hx('#6a6e84'), hx('#8a8ea2'))
    c.rect(28, 40, 14, 112, gc); c.rect(28, 40, 2, 112, gl)
    c.rect(278, 40, 14, 112, gc); c.rect(278, 40, 2, 112, gl)
    c.rect(18, 30, 284, 12, hx('#4a2e30')); c.rect(18, 30, 284, 2, hx('#6a4044')); c.rect(18, 40, 284, 2, hx('#2e1a1e'))
    c.rect(118, 16, 84, 16, hx('#d8d4c8')); c.rect(118, 16, 84, 1, hx('#f2eee4'))
    text(c, 136, 17, '第三中学', hx('#2a2a3a'))
    # sliding fence
    fcol = hx('#6a6e80') if SUN else hx('#3a3e52')
    for x in range(42, 278, 7):
        c.rect(x, 100, 2, 52, fcol)
    c.rect(42, 100, 236, 3, fcol); c.rect(42, 124, 236, 2, fcol)
    # ground
    if SUN:
        c.rect(0, 152, W, 28, hx('#8a8a96')); c.rect(0, 152, W, 1, hx('#a8a8b4'))
        for x in range(8, W, 40):
            c.rect(x, 168, 22, 1, hx('#a8a8b4'))
    else:
        c.rect(0, 152, W, 28, hx('#22263a')); c.rect(0, 152, W, 1, hx('#3a3e54'))
        for x in range(8, W, 40):
            c.rect(x, 168, 22, 1, hx('#3a3e54'))
    # 黑板报 on two legs, little roof
    b = GB
    wood, wd = (hx('#9a6a44'), hx('#6a4a30')) if SUN else (hx('#4a3430'), hx('#2e201e'))
    c.rect(b['x'] + 8, b['y'] + b['h'], 3, 152 - b['y'] - b['h'], wd); c.rect(b['x'] + b['w'] - 11, b['y'] + b['h'], 3, 152 - b['y'] - b['h'], wd)
    c.rect(b['x'] - 6, b['y'] - 8, b['w'] + 12, 4, hx('#a8453a') if SUN else hx('#4a2a2e'))
    c.rect(b['x'] - 3, b['y'] - 4, b['w'] + 6, b['h'] + 7, wood)
    c.rect(b['x'], b['y'], b['w'], b['h'], hx('#2e5244') if SUN else hx('#1e342c'))
    text(c, b['x'] + 3, b['y'], '公告', hx('#f2c84a') if SUN else hx('#7a6a34'), font='w')
    return c
