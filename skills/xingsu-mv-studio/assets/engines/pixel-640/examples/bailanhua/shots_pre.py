# -*- coding: utf-8 -*-
"""S10–S20：预副歌回忆（暖色）—— 咖啡馆 / 剪发 / 口红 / 眼睛 / 舞厅 / 递白兰花 / 深夜餐桌 / 蝴蝶结进盒 / 分屏 / 岔路。"""
import numpy as np, math
from core import *
from sprite import place
from chibi import HIM, HER, blink, unit_px, _hat, SB, BASE, _lit
from props import umbrella, orchid_pair, shape, npc_walker, npc_girl, bubble, phone_sprite
from scn_rooms import cafe, cafe_table, bentwood_chair, salon, salon_mirror_mask, dancehall, disco, dining, wall_clock, bedroom
from sh_street import render_street
from fx import rain, draw_drop, splash_ring
from shots_intro import _bokeh_bg, SPC
from shots_verse import beat_pulse

BEATS = TIMING['beats']


def beat_idx(t):
    n = 0
    for b in BEATS:
        if b <= t:
            n += 1
    return n


def vhs(img, t, t0, label='◀◀ x8', stamp='一个月前', strong=1.0):
    """tracking band + noise lines + HUD."""
    T = tq(t, 12)
    if strong > 0:
        band_y = int((T * 260) % (H + 60)) - 30
        for y in range(max(0, band_y), min(H, band_y + 22)):
            off = int(round(6 * strong * math.sin(y * 0.7 + T * 30)))
            img[y] = np.roll(img[y], off, axis=0) * 0.85 + 30
        for i in range(3):
            y = int(h01(int(T * 12), i) * H)
            img[y, :] = np.minimum(255, img[y, :] * 0.5 + 140)
    if label and int(T * 2) % 2 == 0:
        draw_text(img, label, 16, 12, (250, 250, 250), outline=(20, 20, 30))
    if stamp:
        draw_text(img, stamp, W - 16 - len(stamp) * 16, 300, (255, 186, 90), outline=(40, 20, 10))


def _place_world(img, T, z, spr, anc, x, y, flip=False, a=1.0):
    sx, sy = T(x, y)
    place(img, spr, anc, sx, sy, a=a, flip=flip)
    return sx, sy


# ---------------- S10 cafe (rewind in) ----------------
def _cafe_frame(t, z, cx, cy, rew=False):
    img, T = cafe(z, cx, cy)
    k = 1.25 * z
    # waiter walking backwards during rewind
    if rew:
        u = clamp((t - 31.46) / 0.94)
        wx = 520 - 420 * u
        spr, anc = HIM(view='side', s=k * 0.95, light='warm', walk=(1 - u * 6) % 1, hat=False,
                       over=tuple(sorted(dict(shirt=(240, 240, 236), vest=(40, 40, 46), shirt_m=(240, 240, 236), shirt_b=(240, 240, 236),
                                              vest_w=(40, 40, 46), vest_r=(40, 40, 46), bow1=(30, 30, 30), bow2=(30, 30, 30), bow3=(30, 30, 30)).items())),
                       mouth='flat')
        _place_world(img, T, z, spr, anc, wx, 262, flip=False)
    bentwood_chair(img, T, 262, facing=1)
    bentwood_chair(img, T, 378, facing=-1)
    cafe_table(img, T, z)
    # him: laughing at his phone
    bi = beat_idx(t)
    spr, anc = HIM(view='side', s=k, light='warm', sit=True, hand_r=(13.5, 60.0), eyes='happy', mouth='laugh' if bi % 2 else 'open',
                   look_up=-0.4, rim=(1, 0))
    sx, sy = _place_world(img, T, z, spr, anc, 262, 300)
    hx, hy = unit_px(anc, k, sx, sy, 13.5, 60.0)
    phone_sprite(img, hx - 2 * z, hy - 9 * z, 6 * z, 10 * z, screen=(170, 210, 240))
    return img, T, k, bi


def S10(t, lt, d):
    rew = t < 32.40
    z = 1.0
    img, T, k, bi = _cafe_frame(t, z, 320, 180, rew)
    spr, anc = HER(view='side', s=k, light='warm', sit=True, hand_r=(15.0, 64.0), eyes='closed' if blink(t, 0.4) else 'open',
                   mouth='flat', style='memory', rim=(1, 0))
    sx, sy = _place_world(img, T, z, spr, anc, 378, 300, flip=True)
    hx, hy = unit_px(anc, k, sx, sy, 15.0, 64.0, flip=True)
    cup = m_rect(hx - 5, hy - 6, hx + 5, hy + 3)
    img[outline_of(cup)] = (90, 60, 50); img[cup] = (250, 246, 240)
    if rew:
        img[:] = img * np.array([0.92, 0.92, 1.0], np.float32)
        vhs(img, t, 31.46, strong=1.0)
        # ripple flash of the falling tear at the cut
        if t < 31.46 + 3 / FPS:
            u = (t - 31.46) / (3 / FPS)
            img[:] = img * (0.3 + 0.5 * u)
            r = 20 + 300 * u
            ring = m_ellipse(320, 200, r, r * 0.4) & ~m_ellipse(320, 200, r - 4, r * 0.4 - 3)
            img[ring] = (220, 236, 255)
    else:
        vhs(img, t, 31.46, label=None, strong=0.0)
    return img


def S11(t, lt, d):
    z = 1.7
    cx, cy = 360, 226
    img, T, k, bi = _cafe_frame(t, z, cx, cy)
    if t >= 36.54 and t < 37.2:
        # him looks up with '?'
        spr, anc = HIM(view='side', s=k, light='warm', sit=True, hand_r=(13.5, 60.0), eyes='open', mouth='o', rim=(1, 0))
        sx, sy = _place_world(img, T, z, spr, anc, 262, 300)
        bubble(img, sx + 10 * z, sy - 92 * k, '？')
    # her stirring the cup, looking out of the window
    spr, anc = HER(view='side', s=k, light='warm', sit=True, hand_r=(15.0, 64.0), hand_l=(17.0, 62.0),
                   eyes='closed' if blink(t, 0.4) else 'down', mouth='flat', style='memory', look_up=0.0, rim=(1, 0))
    sx, sy = _place_world(img, T, z, spr, anc, 378, 300, flip=True)
    hx, hy = unit_px(anc, k, sx, sy, 15.5, 64.0, flip=True)
    cup = m_rect(hx - 6 * z, hy - 6 * z, hx + 6 * z, hy + 3 * z)
    img[outline_of(cup)] = (90, 60, 50); img[cup] = (250, 246, 240)
    img[m_rect(hx - 5 * z, hy - 6 * z, hx + 5 * z, hy - 4 * z)] = (110, 60, 36)
    # spoon circling once per beat
    ph = (t - 34.56) / 0.947 * 2 * math.pi
    spx, spy = hx + math.cos(ph) * 3 * z, hy - 6 * z + math.sin(ph) * 1 * z
    img[m_line([(spx, spy), (spx + 3 * z, spy - 10 * z)], max(1, int(z)))] = (200, 200, 210)
    if t >= 36.22:
        bubble(img, sx - 2 * z, sy - 96 * k, '…', a=1.0)
    vhs(img, t, 31.46, label=None, strong=0.0)
    return img


# ---------------- S12 salon: two snips ----------------
def S12(t, lt, d):
    img, T = salon(1.0)
    mm = salon_mirror_mask(T)
    ref = img.copy()
    s = 2.6
    style = 'memory' if t < 39.38 else 'cut'
    spr, anc = HER(view='front', s=s, light='room', style=style, eyes='closed' if blink(t, 1.3) else 'down', mouth='flat', rim=None)
    place(ref, spr, anc, 320, 380)
    # cape
    cape = m_poly([(276, 252), (364, 252), (420, 300), (220, 300)])
    shape(ref, cape, (240, 240, 244), outline=(80, 90, 100))
    for k in range(-6, 7):
        ref[m_line([(320 + k * 14, 252), (320 + k * 22, 300)], 1) & cape] = (170, 196, 230)
    # hairdresser's dark sleeve + scissors (ring handles cover the hand: no fingers on screen)
    arm = m_poly([(162, 232), (222, 214), (240, 222), (236, 234), (218, 232), (162, 262)])
    shape(ref, arm, (40, 40, 50), outline=(16, 16, 20))
    snips = (38.46, 39.38)
    opn = 0.42
    for sn in snips:
        if sn - 0.18 <= t < sn:
            opn = 0.42 * (1 - (t - (sn - 0.18)) / 0.18) + 0.04
        elif sn <= t < sn + 0.12:
            opn = 0.04
    pv = (262, 226)
    for sg in (-1, 1):
        a = -0.42 + sg * opn
        tip = (pv[0] + math.cos(a) * 34, pv[1] + math.sin(a) * 34)
        blade = m_poly([(pv[0], pv[1] - 1.5), (tip[0], tip[1]), (pv[0], pv[1] + 1.5)])
        shape(ref, blade | m_line([pv, tip], 2), (214, 218, 226), outline=(70, 74, 86))
        hx, hy = pv[0] - math.cos(a) * 14, pv[1] - math.sin(a) * 14 + sg * 3
        ring = m_ellipse(hx, hy, 6, 5) & ~m_ellipse(hx, hy, 3.2, 2.6)
        shape(ref, ring | m_line([pv, (hx, hy)], 2), (60, 64, 76), outline=(20, 20, 28))
    ref[m_ellipse(pv[0], pv[1], 2.5, 2.5)] = (150, 150, 160)
    # falling hair
    for sn, n in ((38.46, 3), (39.38, 9)):
        if sn <= t < sn + 1.0:
            u = (t - sn)
            for i in range(n):
                x0 = 270 + 100 * h01(i, int(sn)) if sn > 39 else 268
                y = 240 + 220 * u * u + 8 * h01(i, 3)
                x = x0 + 12 * math.sin(u * 6 + i)
                L = 10 + 6 * h01(i, 5)
                ref[m_line([(x, y), (x + 3, y + L)], 3)] = (104, 60, 46)
    img[mm] = ref[mm]
    # mirror sheen
    img[m_line([(190, 110), (230, 90)], 3) & mm] = np.minimum(255, img[m_line([(190, 110), (230, 90)], 3) & mm] + 40)
    return img


# ---------------- S13 lipstick (props only, no lips/face) ----------------
def _poly_rot(pts, ox, oy, ang):
    ca, sa = math.cos(ang), math.sin(ang)
    return [(ox + x * ca - y * sa, oy + x * sa + y * ca) for x, y in pts]


def _lip_print(img, cx, cy, col, a=1.0):
    up = m_poly([(cx - 22, cy), (cx - 10, cy - 8), (cx - 2, cy - 6), (cx, cy - 3), (cx + 2, cy - 6), (cx + 10, cy - 8), (cx + 22, cy), (cx, cy + 1)])
    lo = m_poly([(cx - 22, cy + 1), (cx, cy + 2), (cx + 22, cy + 1), (cx + 12, cy + 9), (cx, cy + 11), (cx - 12, cy + 9)])
    m = up | lo
    img[m] = img[m] * (1 - a) + np.asarray(col, np.float32) * a
    img[m_line([(cx - 20, cy + 1), (cx + 20, cy + 1)], 1)] = img[m_line([(cx - 20, cy + 1), (cx + 20, cy + 1)], 1)] * 0.9


def S13(t, lt, d):
    img = new((170, 120, 130))
    for x in range(0, W, 24):                                   # damask-ish wallpaper stripes
        img[0:150, x:x + 2] = (158, 108, 120)
        for y in range(10, 150, 28):
            img[m_ellipse(x + 12, y + (x // 24 % 2) * 14, 3, 4) & m_rect(0, 0, W, 150)] = (182, 132, 142)
    ring = m_ellipse(320, -60, 196, 196) & ~m_ellipse(320, -60, 184, 184) & m_rect(0, 0, W, 150)
    img[ring] = (206, 170, 96)                                  # bottom of the round vanity mirror
    inner = m_ellipse(320, -60, 184, 184) & m_rect(0, 0, W, 150)
    img[inner] = img[inner] * 0.5 + np.array((120, 130, 150), np.float32) * 0.5
    img[150:] = (112, 74, 60)                                   # wooden vanity top
    for y in range(158, H, 11):
        img[y, :] = (100, 64, 52)
    img[150:153] = (150, 104, 80)
    stepped_glow(img, 470, 120, 260, (255, 210, 160), k=0.16, levels=4)
    # perfume bottle (back left) + the orchid pair lying in front
    shape(img, m_rect(88, 150, 132, 206), (210, 220, 236), outline=(60, 50, 60))
    img[m_rect(92, 164, 128, 202)] = (236, 190, 200)
    shape(img, m_rect(102, 136, 118, 150), (206, 170, 96), outline=(60, 50, 40))
    orchid_pair(img, 112, 292, s=3.2, angle=-0.25, light=0.95)
    # tissue with blot prints (pink old, then red at 40.98, deep wine at 41.18)
    tis = m_poly([(430, 214), (566, 206), (574, 296), (436, 304)])
    shape(img, tis, (246, 242, 238), outline=(150, 130, 130))
    img[m_line([(432, 258), (570, 252)], 1) & tis] = (226, 220, 218)
    _lip_print(img, 470, 236, (226, 128, 146), 0.8)
    if t >= 40.98:
        _lip_print(img, 528, 236, (196, 42, 64), 0.9)
    if t >= 41.18:
        _lip_print(img, 500, 278, (130, 16, 42), 0.95)
    # cap of the new lipstick lying down
    shape(img, m_rect(330, 286, 392, 306), (30, 26, 32), outline=(10, 8, 12))
    img[m_rect(330, 288, 392, 291)] = (70, 64, 76)
    img[m_rect(384, 286, 392, 306)] = (206, 170, 96)
    # new lipstick: black tube + gold band, bullet twists up on 变 / 深
    cx, base = 300, 300
    h_b = 6
    if t >= 40.98:
        h_b = 6 + 20 * ease_out(clamp((t - 40.98) / 0.12))
    if t >= 41.18:
        h_b = 26 + 14 * ease_out(clamp((t - 41.18) / 0.12))
    col = np.array((226, 118, 136), np.float32) if t < 40.98 else (np.array((198, 42, 64), np.float32) if t < 41.18 else np.array((130, 16, 42), np.float32))
    shape(img, m_rect(cx - 17, base - 70, cx + 17, base), (28, 24, 30), outline=(8, 6, 10))
    img[m_rect(cx - 17, base - 74, cx + 17, base - 66)] = (210, 174, 100)
    img[m_rect(cx - 13, base - 74, cx - 9, base - 66)] = (240, 214, 150)
    img[m_rect(cx - 14, base - 66, cx - 11, base - 4)] = (56, 50, 60)
    sleeve = m_rect(cx - 12, base - 74 - min(h_b, 10), cx + 12, base - 74)
    shape(img, sleeve, (206, 170, 96), outline=(70, 50, 30))
    top = base - 74 - min(h_b, 10)
    bul = m_poly([(cx - 10, top), (cx + 10, top), (cx + 10, top - max(0, h_b - 10) - 8), (cx - 10, top - max(0, h_b - 10) - 2)])
    shape(img, bul, col, outline=col * 0.5)
    img[m_line([(cx - 6, top - 2), (cx - 6, top - max(0, h_b - 10) - 4)], 1) & bul] = np.minimum(255, col * 1.35 + 30)
    for tt in (40.98, 41.18):
        if tt <= t < tt + 0.14:
            stepped_glow(img, cx, top - 10, 60, (255, 190, 200), k=0.4, levels=3)
    # old pink lipstick (gold): stands, then tips over and rolls away at 41.18
    ang = 0.0
    ox, oy = 210, 300
    if t >= 41.18:
        u = clamp((t - 41.18) / 0.16)
        ang = -math.pi / 2 * ease_in(u)
        if t >= 41.34:
            ox -= 520 * (t - 41.34)
    tube = _poly_rot([(-13, 0), (13, 0), (13, -60), (-13, -60)], ox, oy, ang)
    shape(img, m_poly(tube), (206, 170, 96), outline=(70, 50, 30))
    band = _poly_rot([(-13, -36), (13, -36), (13, -42), (-13, -42)], ox, oy, ang)
    img[m_poly(band)] = (240, 214, 150)
    tip = _poly_rot([(-9, -60), (9, -60), (9, -76), (-9, -70)], ox, oy, ang)
    shape(img, m_poly(tip), (226, 118, 136), outline=(120, 50, 70))
    return img


# ---------------- S14 her bust in the dance-hall corner ----------------
def S14(t, lt, d):
    z = 1.0
    img, T = dancehall(z)
    disco(img, T, z, t)
    bi = beat_idx(t)
    # the party in the background (right), small and warm
    k = 1.0
    for (x, kind, ph) in ((448, 0, 0), (552, 3, 1)):
        bob = 0 if (bi + ph) % 2 else -2
        npc_girl(img, T(x, 262)[0], T(x, 262)[1] + bob, k * 0.95, view='front', kind=kind, light='warm', expr='laugh')
    spr, anc = HIM(view='front', s=k, light='warm', hat=False, eyes='happy', mouth='laugh' if bi % 2 else 'smile', hand_r=(19.0, 46.0))
    sx, sy = _place_world(img, T, z, spr, anc, 500, 262)
    hs = _hat_sprite(k)
    hx, hy = unit_px(anc, k, sx, sy, 21.0, 40.0)
    place(img, hs[0], hs[1], hx, hy)
    # push the background back: darker, a little desaturated
    g = img.mean(2, keepdims=True)
    img[:] = (img * 0.62 + g * 0.18) * 0.82
    # her bust (cut bob + ribbon, deep lips), looking toward the party
    s = 3.1
    tear = clamp((t - 44.50) / 0.9) if t >= 44.50 else 0.0
    if t >= 45.80:
        tear = 1.0 + (t - 45.80) * 0.8
    eyes = 'closed' if 45.60 <= t < 45.72 else ('open' if t < 44.50 else 'sad')
    spr, anc = HER(view='front', s=s, light='corner', style='cut', eyes=eyes, mouth='lips', lip=(140, 22, 46), look=2.2,
                   tear=min(tear, 1.6), blush=False, rim=(1, 0))
    fx, fy = 210, 432
    place(img, spr, anc, fx, fy)
    # neon flicker across her face (pink/cyan) on the beat from 42.94
    if t >= 42.94:
        p = beat_pulse(t, 0.3)
        if p > 0:
            face = m_ellipse(fx + 6, fy - 67 * s, 64, 60)
            col = (255, 120, 200) if bi % 2 else (110, 220, 255)
            img[face] = np.minimum(255, img[face] + np.asarray(col, np.float32) * 0.10 * p)
    # tear glint (the film over the eyes)
    if t >= 44.20:
        for sg in (-1, 1):
            ex, ey = unit_px(anc, s, fx, fy, sg * 7.6 + 2.2, 36.0)
            gl = clamp((t - 44.20) / 0.5)
            img[m_rect(ex - 4, ey + 4, ex + 5, ey + 6)] = np.minimum(255, img[m_rect(ex - 4, ey + 4, ex + 5, ey + 6)] * (1 - 0.6 * gl) + 200 * 0.6 * gl)
    return img


# ---------------- S15 dance hall ----------------
def S15(t, lt, d):
    z = 1.0
    img, T = dancehall(z)
    disco(img, T, z, t)
    k = 1.35
    bi = beat_idx(t)
    # her alone in the back-left corner (dim)
    tb = m_rect(*T(70, 226), *T(118, 230))
    img[tb] = (90, 50, 50)
    img[m_rect(*T(92, 230), *T(96, 262))] = (70, 40, 40)
    spr, anc = HER(view='side', s=0.95, light='dim', sit=True, style='cut', eyes='down', mouth='flat', hand_r=(15.0, 66.0), rim=None)
    _place_world(img, T, z, spr, anc, 60, 262)
    # girls laughing
    for (x, kind, ph) in ((246, 0, 0), (396, 3, 1)):
        bob = 0 if (bi + ph) % 2 else -2
        npc_girl(img, T(x, 300)[0], T(x, 300)[1] + bob, k * 0.96, view='front', kind=kind, light='warm', expr='laugh',
                 hand_r=(4.0, 52.0) if kind == 3 else None)
    hat_off = t >= 46.99
    eyes = 'wink' if 47.94 <= t < 48.6 else ('happy' if hat_off else 'open')
    spr, anc = HIM(view='front', s=k, light='warm', hat=not hat_off, eyes=eyes, mouth='laugh' if bi % 2 else 'smile',
                   hand_r=(19.0, 46.0) if hat_off else None, rim=(0, -1))
    sx, sy = _place_world(img, T, z, spr, anc, 320, 300)
    if hat_off:
        hs = _hat_sprite(k)
        hx, hy = unit_px(anc, k, sx, sy, 21.0, 40.0)
        place(img, hs[0], hs[1], hx, hy)
    # notes floating up
    for i in range(4):
        tt = (t - 46.46 + i * 0.5) % 2.0
        nx, ny = sx + 60 + i * 8 + 10 * math.sin(tt * 3 + i), sy - 150 - tt * 40
        draw_text(img, '♪', nx, ny, (255, 230, 170), outline=(80, 30, 40))
    return img


import functools


@functools.lru_cache(maxsize=8)
def _hat_sprite(s):
    P = {k: _lit(v, 'warm') for k, v in BASE.items() if not isinstance(v, str)}
    b = SB(s, wu=60, hu=24, oxu=30, top_u=-2)
    _hat(b, 'side', P, s=s)
    spr = b.finish(outline=(20, 14, 26))
    return spr, (b.X(0), b.Y(14))


# ---------------- S16 dusk street: the orchid ----------------
def S16(t, lt, d):
    z = 2.4
    cam_x, cam_y = 452 - 320 / z, 272 - 312 / z
    img, info = render_street(cam_x, cam_y, z, 'memory', t=t, wet=False, state=dict(cinema=0.0))
    T = info['T']
    k = SPC * z
    took = t >= 51.02
    shrug = t >= 51.78
    if not shrug:
        spr, anc = HIM(view='side', s=k, light='warm', hand_r=(16.0, 62.0), eyes='happy', mouth='laugh', rim=(1, 0))
        sx, sy = _place_world(img, T, z, spr, anc, 430, 272)
        if not took:
            hx, hy = unit_px(anc, k, sx, sy, 16.0, 62.0)
            orchid_pair(img, hx + 3, hy, s=1.6, angle=-0.2)
    else:
        spr, anc = HIM(view='front', s=k, light='warm', hand_r=(19.0, 58.0), hand_l=(-19.0, 58.0), eyes='open', mouth='smile', rim=(1, 0))
        sx, sy = _place_world(img, T, z, spr, anc, 430, 272)
        bubble(img, sx + 26, sy - 112 * k, '？')
    hr = (14.0, 64.0) if (took and not shrug) else ((7.0, 60.0) if shrug else None)
    spr, anc = HER(view='side', s=k, light='warm', style='cut', eyes='down' if took else ('closed' if blink(t, 2) else 'down'),
                   mouth='flat', hand_r=hr, rim=(1, 0))
    sx2, sy2 = _place_world(img, T, z, spr, anc, 478, 272, flip=True)
    if took:
        hx, hy = unit_px(anc, k, sx2, sy2, hr[0], hr[1], flip=True)
        orchid_pair(img, hx - 2, hy, s=1.6, angle=0.3)
    return img


# ---------------- S17 waiting at the dinner table ----------------
def S17(t, lt, d):
    img, T = dining(1.0)
    bi = beat_idx(t)
    wall_clock(img, T, 1.0, 320, 88, 26, 1, 12, ss=(bi * 1) % 60)
    # rain in the window
    win = m_rect(48, 68, 162, 192)
    tmp = img.copy()
    rain(tmp, t, layers=('far', 'mid'), density=1.2)
    img[win] = tmp[win]
    k = 1.35
    down = t >= 54.56
    if not down:
        spr, anc = HER(view='front', s=k, light='lamp', sit=True, style='cut', eyes='closed' if blink(t, 0.7) else 'down', mouth='flat',
                       hand_r=(3.0, 46.5), rim=(0, -1))
        place(img, spr, anc, 360, 292)
    else:
        spr, anc = HER(view='front', s=k, light='lamp', sit=True, style='cut', eyes='closed', mouth='flat',
                       hand_r=(9.0, 66.0), hand_l=(-9.0, 66.0), rim=(0, -1))
        place(img, spr, anc, 360, 300)
    # table (front) + cloth + dishes
    TY = 272
    top = m_rect(150, TY, 490, TY + 8)
    img[top] = (240, 236, 230)
    img[m_rect(150, TY + 8, 490, 340)] = (222, 216, 210)
    for x in range(150, 490, 20):
        img[m_rect(x, TY + 8, x + 10, 340)] = (196, 70, 70) if (x // 20) % 2 == 0 else (222, 216, 210)
    img[m_rect(150, TY + 8, 490, TY + 10)] = (170, 160, 156)
    for (x, food) in ((222, 'fish'), (292, 'rice'), (430, 'rice')):
        img[m_ellipse(x, TY + 2, 26, 6)] = (250, 250, 250)
        img[outline_of(m_ellipse(x, TY + 2, 26, 6))] = (150, 150, 160)
        if food == 'fish':
            img[m_ellipse(x, TY - 2, 18, 5)] = (200, 140, 80)
        else:
            img[m_ellipse(x, TY - 4, 12, 7)] = (250, 250, 246)
            img[m_rect(x - 12, TY - 4, x + 12, TY + 2)] = (230, 120, 110)
    img[m_line([(260, TY + 6), (280, TY - 10)], 2)] = (130, 90, 60)
    img[m_rect(470, TY - 16, 478, TY + 2)] = (240, 230, 210)
    if int(tq(t, 12) * 12) % 2:
        img[m_ellipse(474, TY - 20, 2, 4)] = (255, 210, 120)
    else:
        img[m_ellipse(474, TY - 21, 2, 4)] = (255, 220, 140)
    stepped_glow(img, 474, TY - 20, 30, (255, 190, 110), k=0.3, levels=3)
    return img


# ---------------- S18 the ribbon goes into the box ----------------
def S18(t, lt, d):
    img = new((120, 82, 60))
    for y in range(0, H, 14):
        img[m_rect(0, y, W, y + 1)] = (104, 70, 52)
    bx0, by0, bx1, by1 = 200, 90, 440, 270
    img[m_rect(bx0 + 6, by0 + 8, bx1 + 6, by1 + 8)] = (80, 52, 40)
    shape(img, m_rect(bx0, by0, bx1, by1), (170, 200, 220), outline=(40, 40, 60))
    img[m_rect(bx0 + 8, by0 + 8, bx1 - 8, by1 - 8)] = (230, 222, 206)
    # photo strip (4 frames) from 小酒窝
    px0, py0 = bx0 + 24, by0 + 18
    shape(img, m_rect(px0, py0, px0 + 44, py0 + 146), (250, 250, 250), outline=(120, 120, 130))
    for i in range(4):
        fy = py0 + 4 + i * 35
        img[m_rect(px0 + 4, fy, px0 + 40, fy + 31)] = (250, 210, 220)
        img[m_ellipse(px0 + 15, fy + 18, 7, 7)] = (244, 204, 172)
        img[m_rect(px0 + 7, fy + 6, px0 + 23, fy + 11)] = (124, 116, 110)
        img[m_ellipse(px0 + 29, fy + 18, 7, 7)] = (250, 214, 188)
        img[m_rect(px0 + 22, fy + 10, px0 + 36, fy + 15)] = (104, 60, 46)
        img[m_rect(px0 + 33, fy + 9, px0 + 36, fy + 11)] = (238, 80, 100)
    # ticket stub + dried orchid
    shape(img, m_rect(bx0 + 90, by0 + 120, bx0 + 170, by0 + 150), (236, 222, 196), outline=(120, 100, 90))
    img[m_rect(bx0 + 90, by0 + 120, bx0 + 170, by0 + 128)] = (176, 40, 52)
    orchid_pair(img, bx0 + 150, by0 + 60, s=3.0, light=0.78, angle=0.5)
    # the red ribbon is lowered into the box from above (no hands on screen), sways, lands with a tiny bounce
    u = ease(seg(t, 55.40, 56.10))
    land = by0 + 100
    rx = 380 + 6 * math.sin(tq(t, 12) * 5) * (1 - u)
    ry = -40 + (land + 40) * u
    if 56.10 <= t < 56.30:
        ry = land - 4 * math.sin((t - 56.10) / 0.2 * math.pi)
    if t < 56.10:                                 # its tails trail upward while it is being lowered
        for sg in (-1, 1):
            img[m_line([(rx + sg * 4, ry + 4), (rx + sg * 12, ry + 30), (rx + sg * 8, ry + 44)], 3)] = (220, 70, 90)
    else:
        for sg in (-1, 1):
            img[m_line([(rx + sg * 4, ry + 4), (rx + sg * 14, ry + 22), (rx + sg * 22, ry + 26)], 3)] = (220, 70, 90)
    rib = m_poly([(rx - 30, ry - 14), (rx, ry), (rx - 30, ry + 14)]) | m_poly([(rx + 30, ry - 14), (rx, ry), (rx + 30, ry + 14)])
    shape(img, rib, (238, 80, 100), outline=(110, 30, 40))
    img[m_line([(rx - 26, ry - 8), (rx - 6, ry - 2)], 1) & rib] = (200, 56, 76)
    img[m_line([(rx + 26, ry - 8), (rx + 6, ry - 2)], 1) & rib] = (200, 56, 76)
    img[m_ellipse(rx, ry, 6, 7)] = (196, 56, 76)
    # lid closes at 56.44
    if t >= 56.30:
        v = ease(seg(t, 56.30, 56.44))
        ly0 = -200 + (by0 - 6 - (-200)) * v
        lid = m_rect(bx0 - 6, ly0, bx1 + 6, ly0 + (by1 - by0) + 12)
        shape(img, lid, (160, 196, 226), outline=(40, 40, 60))
        for i in range(10):
            fx = bx0 + 20 + (i * 47) % (bx1 - bx0 - 30)
            fy = ly0 + 24 + (i * 31) % (by1 - by0 - 30)
            for a in range(5):
                ang = a / 5 * 2 * math.pi
                img[m_ellipse(fx + math.cos(ang) * 5, fy + math.sin(ang) * 5, 3, 3) & lid] = (250, 240, 246)
            img[m_ellipse(fx, fy, 2, 2) & lid] = (240, 200, 90)
        if t < 56.44 + 0.1 and t >= 56.44:
            img[:] = img * 0.85
    return img


# ---------------- S19 split: him whistling home / her closing the suitcase ----------------
def S19(t, lt, d):
    out = new((0, 0, 0))
    # left: street night
    z = 1.7
    hx = 360 + 34 * (t - 57.26)
    cam_x = hx - 150 / z
    left, info = render_street(cam_x, 272 - 312 / z, z, 'night', t=t, ow=320, state=dict(cinema=1.0))
    T = info['T']
    k = SPC * z
    spr, anc = HIM(view='side', s=k, light='lamp', walk=(t * 1.6) % 1, eyes='happy', mouth='o', rim=(1, 0))
    sx, sy = T(hx, 272)
    place(left, spr, anc, sx, sy)
    for i in range(3):
        tt = (t - 57.26 + i * 0.45) % 1.35
        draw_text(left, '♪', sx + 18 + i * 6, sy - 92 * k - tt * 30, (255, 236, 170), outline=(40, 30, 50))
    rain(left, t, density=0.5)
    out[:, :320] = left[:, :320]
    # right: bedroom
    right, Tb = bedroom(1.0, 300, 200, w=320)
    kk = 1.35
    closed = t >= 58.94
    spr, anc = HER(view='front', s=1.2, light='lamp', style='now', eyes='down', mouth='flat',
                   hand_r=(10.0, 60.0) if not closed else (12.0, 64.0), hand_l=(-10.0, 60.0) if not closed else (-12.0, 64.0), rim=(1, 0))
    place(right, spr, anc, 160, 262)
    # suitcase in front of her
    sbx0, sby0, sbx1, sby1 = 96, 266, 224, 306
    RW = right.shape[1]
    shape(right, m_rect(sbx0, sby0, sbx1, sby1, RW, H), (150, 60, 60), outline=(40, 20, 24))
    right[m_rect(sbx0, sby0 + 18, sbx1, sby0 + 22, RW, H)] = (110, 40, 44)
    if not closed:
        v = ease(seg(t, 58.70, 58.94))
        lid_h = int(30 * (1 - v)) + 4
        shape(right, m_rect(sbx0, sby0 - lid_h, sbx1, sby0, RW, H), (170, 70, 70), outline=(40, 20, 24))
        if lid_h > 20:
            right[m_rect(sbx0 + 8, sby0 - lid_h + 6, sbx1 - 8, sby0 - 4, RW, H)] = (220, 210, 200)
    else:
        right[m_rect(156, sby0 - 4, 164, sby0 + 6, RW, H)] = (220, 190, 90)
        if t < 58.94 + 0.12:
            right[:] = np.minimum(255, right * 1.15)
    out[:, 320:] = right[:, :320]
    out[:, 319:321] = (240, 240, 246)
    return out


# ---------------- S20 dusk walk: footsteps fall out of step, she turns into the lane ----------------
def S20(t, lt, d):
    z = 1.9
    tt = min(t, 64.80)
    x_him = 80 + 40 * (min(tt, 64.68) - 59.58)
    cam_x = x_him - 260 / z
    cam_y = 272 - 300 / z
    img, info = render_street(cam_x, cam_y, z, 'dusk', t=tt, wet=False, state=dict(cinema=1.0, apt=0.6))
    T = info['T']
    k = SPC * z
    walk_ph = (tt * 1.45) % 1
    # her: on the far side, slightly higher; out of step after 60.54; turns into the lane at 60.96
    if tt < 60.96:
        x_her = x_him - 15
        ph = walk_ph if tt < 60.54 else (walk_ph + 0.5) % 1
        spr, anc = HER(view='side', s=k * 0.96, light='dusk', walk=ph, style='now', eyes='down', mouth='flat', rim=(1, 0))
        sx, sy = T(x_her, 265)
        place(img, spr, anc, sx, sy)
    elif tt < 62.4:
        u = (tt - 60.96) / 1.44
        x_her = 135 + 4 * u
        ss = k * (1 - 0.28 * u)
        spr, anc = HER(view='back', s=ss, light='dim', walk=(tt * 1.4) % 1, style='now', rim=None)
        sx, sy = T(x_her, 266 - 26 * u)
        place(img, spr, anc, sx, sy, a=1 - u ** 1.5)
    # him
    if tt < 64.68:
        spr, anc = HIM(view='side', s=k, light='dusk', walk=walk_ph, eyes='happy', mouth='laugh' if int(tt * 2.1) % 2 else 'open', rim=(1, 0))
        sx, sy = T(x_him, 272)
        place(img, spr, anc, sx, sy)
        if 61.3 <= tt < 64.3:
            bubble(img, sx + 26, sy - 100 * k, '～♪')
    else:
        spr, anc = HIM(view='front', s=k, light='dusk', eyes='wide', mouth='o', look=-2.0, rim=(1, 0))
        sx, sy = T(x_him, 272)
        place(img, spr, anc, sx, sy)
        if t >= 64.86:
            bubble(img, sx - 30, sy - 100 * k, '？')
    if t >= 64.80:
        g = img.mean(2, keepdims=True)
        img[:] = img * 0.55 + g * 0.45
    return img
