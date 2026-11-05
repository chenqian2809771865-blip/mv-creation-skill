# -*- coding: utf-8 -*-
"""Chorus (74.74–138.6) for 《半岛铁盒》."""
import math
import numpy as np
from px import (Cv, hx, mix, W, H, OUT, vgrad, bayer, text, text_w, seg, ease, ease_out, ease_in, clamp,
                grade_warm, grade_ice, vignette, light, silhouette, dither_blend, darken_flat, grade_mul, outline, lum, upscale)
from chars import chibi, blit_chibi, bust, emote, blink, P, PICK, TEAR, TEAR_HI
from scenes import (room, room_static, window_view, window_light, clock_hands, dust, rain, glass_rain, gate, umbrella,
                    RED_UMB, BLK_UMB, glow, street, candy_jar_small, WIN, splashes, ROOM)
from props import (tin, tin_small, open_book, polaroid, candy_px, CANDY, page_lines, PAGE, INK)
from ui import vcr, phone_body, lock_screen
from ui_tiny import tiny
from shots import (shot, up2, upk, lit, memory_post, ice_post, bokeh_bg, dim_to, rain_shadows)
from shots_intro import intro_bg, phone_geom, NOTE

STAMP = '2023.12.08'


def hand_pos(x, y, ang, flip=False):
    """scene position of a side-view chibi's near hand for arm angle ang (feet at x,y)."""
    a = math.radians(ang)
    dx = -1 + 7 * math.sin(a)
    return (x - dx if flip else x + dx), y - 18 + 7 * math.cos(a)


# ================================================================ S24 the school gate in the rain
def gate_pair(t, she_x=78, she_spr=None, he_arm=None, he_eyes=None):
    c = gate(t, rain_k=1.0 + 0.3 * ease(seg(t, 76.5, 77.0)))
    he = chibi('he', 'side', 'stand', bag=True, arm=he_arm, eyes=he_eyes or ('closed' if blink(t) else 'open'))
    blit_chibi(c, lit(he, 'rain'), 58, 138)
    if she_spr is not None:
        blit_chibi(c, lit(she_spr, 'rain'), she_x, 138, flip=True)
    return c


@shot('gate_rain')
def gate_rain(t):
    she = chibi('she', 'side', 'stand', eyes='down' if t > 76.0 else 'open')
    c = gate_pair(t, 78, she)
    return ice_post(c, t, STAMP)


@shot('sleeve')
def sleeve(t):
    tt = t + 0.06
    she = chibi('she', 'side', 'stand', arm=82, eyes='down' if not (81.37 <= tt < 81.8) else 'open')
    c = gate_pair(t, 72, she, he_eyes='open' if tt < 81.4 else 'down')
    if tt >= 80.41:
        c.blit(emote('dots', hx('#3a3a5a')), 70, 96 - int(ease_out(seg(tt, 80.41, 80.6)) * 3))
    return ice_post(upk(c, 66, 112, 2), t, STAMP)


@shot('he_confused')
def he_confused(t):
    tt = t + 0.06
    c = Cv(W, H)
    bokeh_bg(c, t, 'rain', seed=21)
    eyes = 'wide' if tt >= 82.79 else 'open'
    b = bust('he', eyes, 'o' if 82.79 <= tt < 83.5 else 'line', 'knit' if tt >= 83.81 else 'up', look=0)
    c.blit(lit(b, 'rain'), 124, 70)
    rain(c, t, 120, 31, speed=320, wind=-60, length=10, col=hx('#9aaad0'))
    return ice_post(c, t, STAMP)


@shot('umbrella_leave')
def umbrella_leave(t):
    tt = t + 0.06
    c = gate(t, 1.3)
    q = seg(t, 86.2, 90.3)
    x = 78 + 140 * q
    walking = t >= 86.2
    opened = ease_out(seg(tt, 88.07, 88.22))
    arm = 20 if tt < 87.9 else (150 if opened > 0 else 20 + 130 * seg(tt, 87.9, 88.07))
    if walking:
        she = chibi('she', 'side', 'walk', phase=((t - 86.2) * 1.5) % 1, eyes='down', arm=arm)
        hy_off = int(min(1, q * 6) * 22)
        blit_chibi(c, lit(she, 'rain'), x, 138 + hy_off)
    else:
        she = chibi('she', 'side', 'stand', eyes='down', arm=arm)
        blit_chibi(c, lit(she, 'rain'), x, 138)
        hy_off = 0
    hx_, hy_ = hand_pos(x, 138 + hy_off, arm)
    if opened <= 0:
        umbrella(c, hx_, hy_, *RED_UMB, open_=0.05, tilt=180 if arm < 60 else 0, shaft=12)
    else:
        umbrella(c, hx_, hy_, *RED_UMB, open_=opened, w=36, tilt=-6, shaft=16)
    he_arm = 60 if 86.4 < tt < 87.2 else None
    he = chibi('he', 'side', 'stand', bag=True, arm=he_arm, eyes='open' if tt < 88.5 else 'down')
    blit_chibi(c, lit(he, 'rain'), 58, 138)
    return ice_post(c, t, STAMP)


# ================================================================ S28 he stands still; her red umbrella grows small (perspective street)
def tiny_walker(c, x, y, s, col_top=hx('#efe4cb'), col_leg=hx('#3f3747'), umb=True, phase=0.0):
    """far-away figure: s = scale (0..1). (x,y) = feet."""
    h = max(3, int(30 * s)); w = max(2, int(10 * s))
    st = int(round(math.sin(phase * 6.28) * max(1, w * 0.3)))
    c.rect(x - w // 2, y - h, w, int(h * 0.55), col_top)
    c.rect(x - w // 2 + st, y - int(h * 0.45), max(1, w // 3), int(h * 0.45), col_leg)
    c.rect(x + w // 2 - max(1, w // 3) - st, y - int(h * 0.45), max(1, w // 3), int(h * 0.45), col_leg)
    if umb:
        umbrella(c, x + 1, y - h + int(h * 0.2), *RED_UMB, open_=1.0, w=max(5, int(44 * s)), tilt=-6, shaft=max(3, int(16 * s)))


@shot('stand_still')
def stand_still(t):
    tt = t + 0.06
    c = street(t, 1.2)
    q = ease_out(seg(t, 90.3, 93.85))
    s = 0.55 - 0.45 * q
    fx = 168 - 6 * q; fy = 132 - 56 * q
    tiny_walker(c, fx, fy, s, phase=t * 1.4)
    he = chibi('he', 'back', 'stand', bag=True)
    blit_chibi(c, lit(he, 'rain'), 160, 152)
    if tt < 92.0:
        out = upk(c, 160, 112, 2)
    else:
        out = c
    return ice_post(out, t, STAMP)


# ================================================================ S29 waiting by the window (time-lapse)
MONTHS = ['12', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11']
STAMPS = ['2023.12.09', '2024.01.15', '2024.02.14', '2024.03.13', '2024.05.01', '2024.06.12', '2024.08.20', '2024.11.20']


@shot('wait_window')
def wait_window(t):
    p = (t - 93.85) * 1.6
    f = clamp(0.5 + 2.2 * math.sin(p * 2 * math.pi - math.pi / 2))
    A = room(t, 'night', rain_k=1.0 if int(p) % 3 != 1 else 0.0, clock_speed=4000)
    B = room(t, 'day', win_mode='day', clock_speed=4000)
    for cc in (A, B):
        mi = int((t - 93.85) / 0.45) % len(MONTHS)
        cc.rect(191, 63, 12, 10, hx('#f2ece0'))
        tiny(cc, 191 + (6 - 2 * len(MONTHS[mi])), 65, MONTHS[mi], hx('#2a2236'))
        cc.rect(84, 104, 6, 2, hx('#24202e'))  # phone on the sill, never lights up
    c = Cv(arr=dither_blend(A.a, B.a, f))
    he = chibi('he', 'side', 'floor', eyes='down' if f < 0.5 else 'open')
    blit_chibi(c, light(he, tuple(0.62 + 0.38 * f * v for v in (1, 1, 1)), rim=(150, 170, 235), rim_side=-1, rim_k=0.4 * (1 - f)), 118, 142, flip=True)
    si = min(len(STAMPS) - 1, int((t - 93.85) / (4.1 / len(STAMPS))))
    vcr(c, t, label='▶▶ x8', stamp=STAMPS[si], blink=True)
    return c


# ================================================================ S30/S31 the photo on the wall: dust, time, fading
def wall_photo(t, dusty=0.0, yellow=0.0, cracks=0, fade=0.0, clock_speed=1.0, show_clock=False):
    from ui import wallpaper_umbrella
    c = Cv(160, 90, hx('#1f2340'))
    for x in range(0, 160, 6):
        c.rect(x, 0, 1, 90, hx('#262a4c'))
    fx, fy, fw, fh = (78, 18, 60, 48) if show_clock else (50, 18, 60, 48)
    c.rect(fx + 3, fy + 3, fw, fh, hx('#141628'))
    c.rect(fx, fy, fw, fh, hx('#6a4a3a')); c.rect(fx, fy, fw, 1, hx('#8a6a50')); c.rect(fx + fw - 1, fy, 1, fh, hx('#4a3428'))
    ph = Cv(fw - 8, fh - 8)
    wallpaper_umbrella(ph, 1.0)
    a = ph.a.astype(np.float32)
    if yellow > 0:
        L = lum(a)[..., None] * 255
        sep = np.concatenate([L * 1.05 + 30, L * 0.9 + 18, L * 0.65], axis=2)
        a = a * (1 - yellow) + sep * yellow
    if fade > 0:
        a = a * (1 - fade) + np.array([230, 220, 200]) * fade
    ph.a[:] = np.clip(a, 0, 255).astype(np.uint8)
    r = np.random.default_rng(17)
    for k in range(cracks):
        x0_, y0_ = r.uniform(0, ph.w), r.uniform(0, ph.h)
        for j in range(5):
            x1_, y1_ = x0_ + r.uniform(-10, 10), y0_ + r.uniform(-8, 8)
            ph.line(x0_, y0_, x1_, y1_, hx('#3a2a20'))
            x0_, y0_ = x1_, y1_
    c.paste(ph, fx + 4, fy + 4)
    if dusty > 0:
        m = bayer(90, 160, 1, 1) < dusty * 0.45
        reg = np.zeros((90, 160), bool); reg[fy:fy + fh, fx:fx + fw] = True
        mm = m & reg
        c.a[mm] = (c.a[mm].astype(np.float32) * 0.5 + np.array([170, 166, 160]) * 0.5).astype(np.uint8)
        c.rect(fx, fy - 1, int(fw * min(1, dusty * 1.5)), 1, hx('#a8a4a0'))
    if dusty > 0.6:  # cobweb in the corner
        for k in range(5):
            c.line(fx + fw - 1, fy, fx + fw - 1 - 10 + k * 2.5, fy + 10 - k * 2.5, hx('#8a8aa0'))
        c.line(fx + fw - 6, fy, fx + fw - 1, fy + 5, hx('#8a8aa0'))
    if show_clock:
        cx, cy = 36, 42
        c.ellipse(cx, cy, 20, 20, hx('#9a96a8')); c.ellipse(cx, cy, 17, 17, hx('#d8d4e0'))
        for k in range(12):
            a_ = k / 12 * 2 * math.pi
            c.px(cx + 14 * math.sin(a_), cy - 14 * math.cos(a_), hx('#2a2236'))
        a1 = t * clock_speed / 60 * 2 * math.pi; a2 = t * clock_speed / 3600 * 2 * math.pi
        c.line(cx, cy, cx + 13 * math.sin(a1), cy - 13 * math.cos(a1), hx('#c83a36'))
        c.line(cx, cy, cx + 10 * math.sin(a2), cy - 10 * math.cos(a2), hx('#2a2236'))
        c.line(cx, cy, cx + 6 * math.sin(a2 / 12 + 1), cy - 6 * math.cos(a2 / 12 + 1), hx('#2a2236'))
    return c


@shot('photo_wall')
def photo_wall(t):
    d = ease(seg(t, 97.95, 100.6))
    c = wall_photo(t, dusty=d)
    dust(c, t, 16, 61, area=(0, 0, 160, 90), col=hx('#b8b4c8'), speed=2)
    return up2(c)


@shot('photo_age')
def photo_age(t):
    tt = t + 0.06
    cracks = sum(1 for tc in (102.06, 102.66, 103.14, 103.44, 103.74) if tt >= tc)
    y = ease(seg(t, 100.7, 103.0))
    fade = ease(seg(t, 103.0, 104.4)) * 0.75
    c = wall_photo(t, dusty=1.0, yellow=y, cracks=cracks * 2, fade=fade, clock_speed=3600 * 6, show_clock=True)
    return up2(c)


# ================================================================ S32 mirror: she stops and looks back at him far away
@shot('gate_mirror')
def gate_mirror(t):
    """mirror of S27: she stops on the far right under her red umbrella and looks back; he is still under the gate."""
    tt = t + 0.06
    c = gate(t, 1.3)
    he = chibi('he', 'side', 'stand', bag=True, eyes='down' if not blink(t) else 'closed')
    blit_chibi(c, lit(he, 'rain'), 58, 138)
    x, y = 232, 160
    if tt < 106.4:
        she = chibi('she', 'side', 'stand', eyes='open' if tt > 104.9 else 'down', arm=150)
        blit_chibi(c, lit(she, 'rain'), x, y, flip=True)
        hx_, hy_ = hand_pos(x, y, 150, flip=True)
        umbrella(c, hx_, hy_, *RED_UMB, open_=1.0, w=36, tilt=6, shaft=16)
    else:
        q = seg(t, 106.6, 108.0)
        xx = x + 60 * q
        she = chibi('she', 'side', 'walk' if q > 0 else 'stand', phase=((t - 106.6) * 1.5) % 1, eyes='down', arm=150)
        blit_chibi(c, lit(she, 'rain'), xx, y)
        hx_, hy_ = hand_pos(xx, y, 150)
        umbrella(c, hx_, hy_, *RED_UMB, open_=1.0, w=36, tilt=-6, shaft=16)
    return ice_post(c, t, STAMP)


# ================================================================ S33 her face: she has decided
@shot('she_decided')
def she_decided(t):
    tt = t + 0.06
    c = Cv(W, H)
    bokeh_bg(c, t, 'rain', seed=23)
    eyes = 'down' if tt < 109.93 else ('closed' if blink(t, 5) else 'open')
    b = bust('she', eyes, 'line', 'calm', wind=1 if tt >= 111.55 else 0)
    c.blit(lit(b, 'rain'), 124, 70)
    rain(c, t, 110, 33, speed=320, wind=-60, length=10, col=hx('#9aaad0'))
    c = ice_post(c, t, None)
    if tt >= 110.55:
        c = upk(c, 160, 108, 2)
    vcr(c, t, label=None, stamp=STAMP)
    return c


# ================================================================ S34 I can't hold you (hands)
def _hand_piece(w, h, parts, skin):
    cc = Cv(w, h, alpha=True)
    for pp in parts:
        if pp[0] == 'e':
            cc.ellipse(pp[1], pp[2], pp[3], pp[4], skin)
        else:
            cc.poly(pp[1], skin)
    return outline(cc)


@shot('hands_slip')
def hands_slip(t):
    c = Cv(160, 90)
    vgrad(c, 0, 90, [hx('#2a3048'), hx('#3a4566'), hx('#56607e')])
    p = ease_in(seg(t, 112.55, 114.1))
    off = int(p * 64)
    sk, sd = hx('#f6d0b2'), hx('#dfa689')
    hk, hd = hx('#f2c9a8'), hx('#d9a083')
    her = _hand_piece(110, 60, [('e', 40, 30, 17, 13)] + [('e', 18, 20 + k * 6, 10, 3.2) for k in range(4)] + [('e', 36, 16, 8, 4)], sk)
    for k in range(3):
        her.a[22 + k * 6, 10:26] = (*sd, 255)
    c.blit(her, 50 + off, 16)
    c.poly([(100 + off, 30), (170, 22), (170, 74), (100 + off, 62)], hx('#efe4cb'))
    c.line(100 + off, 30, 100 + off, 62, OUT)
    for k in range(4):
        c.line(104 + off + k * 6, 30, 104 + off + k * 6, 62, hx('#cdbd9c'))
    grip = clamp(1 - (p - 0.1) * 2.2)
    c.poly([(-10, 24), (40, 28), (40, 70), (-10, 76)], hx('#3b5b98'))
    c.rect(34, 28, 6, 42, hx('#2a4375')); c.line(40, 28, 40, 70, OUT)
    fl = 8 + grip * 10
    parts = [('e', 22, 32, 18, 15)] + [('e', 38 + fl / 2, 22 + k * 6.5, fl, 3.4) for k in range(4)] + [('e', 30, 14, 10, 4.5)]
    hisp = _hand_piece(90, 60, parts, hk)
    for k in range(3):
        hisp.a[25 + int(k * 6.5), 40:40 + int(fl)] = (*hd, 255)
    c.blit(hisp, 26, 14)
    rain(c, t, 40, 35, speed=200, wind=-40, length=6, col=hx('#b8c8e8'), area=(0, 0, 160, 90))
    c = up2(c)
    return ice_post(c, t, STAMP, vig=0.4)


# ================================================================ S35 his hand must be warmer than mine
def stretch(spr, k=1.18):
    a = spr.a
    h = a.shape[0]
    nh = int(h * k)
    idx = np.clip((np.arange(nh) / k).astype(int), 0, h - 1)
    return Cv(arr=np.ascontiguousarray(a[idx]))


@shot('warmer')
def warmer(t):
    tt = t + 0.06
    c = gate(t, 1.0)
    q = t - 115.35
    x = 150 + 11 * q
    ph = (q * 1.3) % 1
    she = chibi('she', 'side', 'walk', phase=(ph + 0.5) % 1, eyes='open', arm=55)
    blit_chibi(c, lit(she, 'rain'), x, 164)
    other = stretch(silhouette(chibi('he', 'side', 'walk', phase=ph, arm=150), hx('#3a3a48')), 1.2)
    blit_chibi(c, other, x + 13, 164 + 7)
    umbrella(c, x + 16, 134, *BLK_UMB, open_=1.0, w=48, tilt=-6, shaft=18)
    umbrella(c, x - 5, 155, *RED_UMB, open_=0.05, tilt=180, shaft=8)
    he = chibi('he', 'side', 'stand', bag=True, arm=150 if 116.0 < tt < 118.6 else 30, eyes='down')
    blit_chibi(c, lit(he, 'rain'), 100, 164)
    for (ph_, d) in ((0.0, 1), (0.9, 1)):  # breath puffs on his hands
        qq = ((t - 116.0 + ph_) % 1.8) / 1.8
        if 116.0 < tt < 118.8 and qq < 0.6:
            for k in range(3):
                c.px(108 + k * 2 + qq * 6, 138 - qq * 12 - k, (240, 244, 250))
    c = ice_post(upk(c, 150, 132, 2), t, STAMP)
    # their joined hands glow warm (after the cold grade)
    jx, jy = (x + 6 - 70) * 2, (147 - 87) * 2
    gl = 0.6 + 0.4 * math.sin(t * 5)
    glow(c, jx, jy, 22 + 5 * gl, hx('#ffb060'), k=0.55, dens=0.6)
    c.rect(jx - 2, jy - 2, 5, 4, hx('#ffd8a0'))
    return c


# ================================================================ S36/S37 the preface becomes a diary, then air, then memories
ENTRIES = [(120.23, '12.08', '雨', 'L', 0), (120.95, '12.09', '雨', 'L', 1), (121.55, '12.20', '没回来', 'L', 2),
           (122.33, '01.01', '一个人', 'R', 0), (122.81, '03.13', '想你', 'R', 1)]
DIARY_INK = hx('#2a3a7a')


def diary_book(t, written=None):
    c = Cv(160, 90, hx('#2a2236'))
    for y in range(0, 90, 7):
        c.rect(0, y, 160, 1, hx('#241c2e'))
    open_book(c, 80, 8, 60, 74, left=dict(num=6, lines=6), right=dict(num=7, lines=7, title='序'))
    yy, xx = np.mgrid[0:90, 0:160]
    m = ((xx - 96) ** 2 / 2.2 + (yy - 40) ** 2 < 52 ** 2) & (bayer(90, 160) < 0.45)
    c.a[m] = np.clip(c.a[m].astype(np.float32) * 0.75 + np.array([255, 230, 180]) * 0.25, 0, 255).astype(np.uint8)
    pos = {}
    for (tc, d, s, side, row) in ENTRIES:
        x0 = 24 if side == 'L' else 84
        y0 = (14 if side == 'L' else 30) + row * 14
        pos[tc] = (x0, y0, d, s)
        if written is None:
            continue
        n = written(tc)
        if n <= 0:
            continue
        c.rect(x0 - 1, y0 - 1, 56, 13, PAGE)
        full = d + ' ' + s
        shown = full[:n]
        tx = tiny(c, x0, y0 + 4, shown[:5], DIARY_INK)
        if len(shown) > 6:
            text(c, tx + 3, y0, shown[6:], DIARY_INK, font='w')
    return c, pos


def chars_written(tt):
    def f(tc):
        if tt < tc:
            return 0
        full = 7 + 3
        return int(clamp((tt - tc) / 0.3) * full) + 1
    return f


@shot('diary')
def diary(t):
    tt = t + 0.06
    c, pos = diary_book(t, chars_written(tt))
    # the pen writing the newest line
    cur = [e for e in ENTRIES if tt >= e[0]]
    if cur and tt - cur[-1][0] < 0.45:
        x0, y0, d, s = pos[cur[-1][0]]
        px_ = x0 + 4 + (tt - cur[-1][0]) / 0.3 * 40
        c.line(px_, y0 + 10, px_ + 10, y0 - 8, hx('#1a1a2a')); c.line(px_ + 1, y0 + 10, px_ + 11, y0 - 8, hx('#3a3a5a'))
        c.rect(px_ + 8, y0 - 14, 6, 8, hx('#3b5b98'))
    return up2(c)


def _entry_pixels(pos):
    pts = []
    for tc, (x0, y0, d, s) in pos.items():
        tmp = Cv(60, 14)
        tx = tiny(tmp, 0, 4, d, (255, 255, 255))
        text(tmp, tx + 3, 0, s, (255, 255, 255), font='w')
        ys, xs = np.nonzero(tmp.a[..., 0] > 0)
        for yv, xv in zip(ys, xs):
            pts.append((tc, x0 + xv, y0 + yv))
    return pts


LIFT = [123.41, 123.65, 123.89, 124.25, 124.73]
TARGETS = [(36, 22, 'store', -8), (80, 16, 'read', 4), (124, 22, 'candy', 10)]


@shot('to_air')
def to_air(t):
    tt = t + 0.06
    c, pos = diary_book(t, None)
    dim = ease(seg(t, 124.6, 125.8))
    if dim > 0:
        c.a[:] = np.clip(c.a.astype(np.float32) * (1 - 0.55 * dim), 0, 255).astype(np.uint8)
    keys = sorted(pos.keys())
    pts = _entry_pixels(pos)
    rng = np.random.default_rng(5)
    conv = ease_in(seg(tt, 125.03, 126.0))
    for i, (tc, x, y) in enumerate(pts):
        li = LIFT[keys.index(tc)]
        if tt < li:
            c.px(x, y, DIARY_INK)
            continue
        d = tt - li
        sx = x + math.sin(d * 2 + i) * 4 * min(1, d) + rng.uniform(-1, 1)
        sy = y - d * (10 + (i % 7) * 2)
        if conv > 0:
            tx_, ty_, _, _ = TARGETS[i % 3]
            tx_ += (i * 7 % 18) - 9; ty_ += (i * 5 % 20) - 10
            sx = sx * (1 - conv) + tx_ * conv; sy = sy * (1 - conv) + ty_ * conv
        col = DIARY_INK if d < 0.25 else mix(hx('#c8c8e8'), hx('#fff2c8'), conv)
        if 0 <= sy < 90:
            c.px(sx, sy, col)
    ap = seg(tt, 125.7, 126.35)
    if ap > 0:
        for (x_, y_, kind, rot) in TARGETS:
            polaroid(c, x_, y_ + math.sin(t * 1.5 + x_) * 1.5, kind, w=22, h=26, rot=rot, alpha=ap)
    return up2(c)


# ================================================================ S38/S39 the memories float around him, then crumble
ORBIT = [('store', 0.0), ('read', 1.26), ('candy', 2.51), ('umbrella', 3.77), ('roof', 5.03)]
CRUMBLE = [131.54, 132.08, 132.44, 132.98, 133.22]


def orbit_room(t, burn_at=None):
    c = room(t, 'night', rain_k=1.0)
    c.a[:] = darken_flat(c.a, 0.55)
    he = chibi('he', 'front', 'sit', eyes='closed' if blink(t) else 'open', look=0)
    blit_chibi(c, light(he, (0.7, 0.7, 0.85), rim=(255, 236, 190), rim_side=1, rim_k=0.4), 150, 150)
    tin_small(c, 170, 156, rust=0.7, dusty=1)
    glow(c, 150, 118, 60, hx('#fff0c8'), k=0.12, dens=0.35)
    items = []
    for i, (kind, a0) in enumerate(ORBIT):
        a = a0 + t * 0.45
        x = 150 + math.cos(a) * 60
        y = 110 + math.sin(a) * 14
        items.append((math.sin(a), i, kind, x, y, int(math.sin(a + t) * 10)))
    for depth, i, kind, x, y, rot in sorted(items):
        b = 0.0
        if burn_at is not None:
            b = burn_at(i)
            if b >= 1:
                continue
        polaroid(c, x, y, kind, w=24, h=28, rot=rot, burn=b, yellow=min(1, b * 2))
        if b > 0:
            r = np.random.default_rng(i * 3 + int(t * 10))
            for k in range(int(10 + 30 * b)):
                c.px(x + r.uniform(-14, 14), y + r.uniform(0, 30) + b * 20, hx('#8a8070') if k % 2 else hx('#c8c0b0'))
    return c


@shot('polaroids')
def polaroids(t):
    return upk(orbit_room(t), 150, 116, 2)


@shot('crumble')
def crumble(t):
    tt = t + 0.06

    def burn_at(i):
        return clamp((tt - CRUMBLE[i]) / 0.4) if tt >= CRUMBLE[i] else 0.0
    c = orbit_room(t, burn_at)
    if tt > 133.3:
        dust(c, t, 30, 71, area=(110, 120, 200, 160), col=hx('#a8a090'), speed=-4)
    return upk(c, 150, 116, 2)


# ================================================================ S40 the rain stops; he lets go
@shot('rain_stops')
def rain_stops(t):
    tt = t + 0.06
    rk = 1 - ease(seg(t, 134.04, 135.4))
    dawn = ease(seg(t, 135.0, 136.6))
    A = room(t, 'night', rain_k=rk)
    B = room_static('night').copy()
    window_view(B, t, 'dawn', rain_k=0, sun=(70, 70 - 20 * dawn))
    B.a[:] = np.clip(B.a.astype(np.float32) * 1.2 + np.array([30, 16, 8]), 0, 255).astype(np.uint8)
    c = Cv(arr=np.clip(A.a.astype(np.float32) * (1 - dawn) + B.a.astype(np.float32) * dawn, 0, 255).astype(np.uint8))
    candy_jar_small(c, 14, 108, full=False, key_glint=seg(tt, 136.0, 136.3))
    # the tin with the book on top, on the windowsill
    place = ease_out(seg(tt, 134.46, 134.9))
    tin_small(c, 70, 106 - int((1 - place) * 6), rust=0.7, dusty=0.5)
    if place > 0.5:
        by_ = 93 - int((1 - place) * 6)
        c.rect(60, by_ - 1, 20, 5, OUT); c.rect(61, by_, 18, 3, hx('#2a5a7a')); c.rect(61, by_, 18, 1, hx('#3a7a8e')); c.rect(76, by_, 2, 3, hx('#f4ead6'))
    if tt < 135.6:
        he = chibi('he', 'side', 'stand', arm=80 if tt < 134.95 else 20, eyes='down')
        blit_chibi(c, lit(he, 'dawn' if dawn > 0.5 else 'night'), 92, 142, flip=True)
    else:
        he = chibi('he', 'front', 'stand', eyes='closed' if tt >= 135.9 else 'down', mouth='line')
        blit_chibi(c, lit(he, 'dawn'), 96, 142)
    if dawn > 0:  # dawn light patch on the floor
        x0, y0, w, h = WIN
        pts = [(x0 + 10, 128), (x0 + w - 10, 128), (x0 + w + 40, H), (x0 + 20, H)]
        m_c = Cv(W, H, alpha=True)
        m_c.poly(pts, (255, 255, 255))
        m = (m_c.a[..., 3] > 0) & (bayer() < 0.45 * dawn)
        c.a[m] = np.clip(c.a[m].astype(np.float32) * 0.7 + np.array([255, 200, 150]) * 0.3, 0, 255).astype(np.uint8)
    return upk(c, 90, 100, 2)


# ================================================================ S41 lock screen: the old notification is swiped away
@shot('lock_end')
def lock_end(t):
    tt = t + 0.06
    c = intro_bg(t, 0, rain_k=0.0)
    c.a[:] = np.clip(c.a.astype(np.float32) * np.array([1.5, 1.25, 1.05]) + np.array([20, 10, 0]), 0, 255).astype(np.uint8)
    x0, y0, sw, sh = phone_geom(0)
    phone_body(c, x0, y0, sw, sh)
    dis = seg(tt, 137.15, 137.5)
    lock_screen(c, x0, y0, sw, sh, t, clock='06:12', date='10月26日 星期一', wall='dawn', notes=NOTE, note_p=1.0, dismiss=dis,
                empty_text='没有新通知' if tt >= 137.55 else None)
    if 137.0 < tt < 137.5:  # his thumb swiping
        q = ease(seg(tt, 137.1, 137.5))
        hx_ = x0 + sw - 20 - q * 110
        c.ellipse(hx_, 96, 8, 9, hx('#f2c9a8')); c.rect(hx_ - 5, 102, 11, 80, hx('#f2c9a8'))
        c.rect(hx_ - 7, 140, 15, 40, hx('#3b5b98'))
    dim_to(c, ease(seg(t, 137.9, 138.55)))
    return c
