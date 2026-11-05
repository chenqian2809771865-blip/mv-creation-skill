# -*- coding: utf-8 -*-
"""Verse 1 (16.85–74.74) for 《半岛铁盒》."""
import math
import numpy as np
from px import (Cv, hx, mix, W, H, OUT, vgrad, bayer, text, text_w, seg, ease, ease_out, ease_in, clamp,
                grade_warm, vignette, light, dither_blend, darken_flat, grade_mul, outline, lum, upscale)
from chars import chibi, blit_chibi, bust, emote, blink, P, BAG, BAG_DK, BAG_LT, PICK
from scenes import (room, room_static, window_view, window_light, clock_hands, corridor_static, dust, rain, glass_rain,
                    gate, gate_static, umbrella, RED_UMB, glow, light_cone, lamp, buildings, canopy, cloud_sprite, candy_jar_small,
                    WIN, splashes)
from props import (tin, tin_small, book_cover, open_book, candy_jar, polaroid, mini_pic, candy_px, CANDY, TEAL, LIDRED, CREAM)
from ui import vcr, phone_body, rrect, wallpaper_umbrella
from shots import (shot, up2, upk, lit, memory_post, bokeh_bg, dim_to, rain_shadows, flash_at)

SK_HE, SKD_HE = hx('#f2c9a8'), hx('#d9a083')
SK_SHE, SKD_SHE = hx('#f6d0b2'), hx('#dfa689')
NAVY, NAVY_DK = hx('#3b5b98'), hx('#2a4375')
CREAMS, CREAMS_DK = hx('#efe4cb'), hx('#cdbd9c')


def hand(c, x, y, skin, dk, sleeve, sleeve_dk, d=1, s=1.0, fingers=True, point=False):
    """mitten hand seen from above. (x,y)= knuckles center; d=+1 fingers point right, -1 left; sleeve trails behind."""
    sx = -d
    c.poly([(x + sx * 6 * s, y - 6 * s), (x + sx * 22 * s, y - 8 * s), (x + sx * 24 * s, y + 8 * s), (x + sx * 6 * s, y + 7 * s)], sleeve)
    c.line(x + sx * 6 * s, y - 6 * s, x + sx * 6 * s, y + 7 * s, sleeve_dk)
    c.ellipse(x, y, 6 * s, 6 * s, skin)
    if point:
        c.rect(x + d * 4 * s if d > 0 else x - 10 * s, y - 2 * s, 7 * s, 3 * s, skin)
    elif fingers:
        for k in range(3):
            c.rect(x + (d * 4 * s if d > 0 else -7 * s), y - 4 * s + k * 3 * s, 4 * s, 2 * s, skin)
            c.px(x + d * 7 * s, y - 4 * s + k * 3 * s + 1, dk)
    c.ellipse(x - d * 1 * s, y + 4 * s, 3 * s, 2 * s, dk)
    c.px(x + d * 2, y - 2, mix(skin, (255, 255, 255), 0.4))


def beam_mask(pts):
    m = Cv(W, H, alpha=True)
    m.poly(pts, (255, 255, 255))
    return m.a[..., 3] > 0


def apply_beam(c, bm, col=(255, 236, 190), k=0.35, dens=0.55, falloff=None):
    f = dens if falloff is None else falloff * dens
    mm = bm & (bayer() < f)
    cur = c.a[mm].astype(np.float32)
    c.a[mm] = np.clip(cur * (1 - k) + np.array(col) * k, 0, 255).astype(np.uint8)


# ================================================================ S01 corridor
@shot('corridor')
def corridor(t):
    on = t < 17.60 or (17.55 < t < 17.58)
    c = corridor_static(on).copy()
    if not on:  # faint night window light at the far right
        light_cone(c, 300, 20, 126, 10, 60, hx('#4a5a9a'), k=0.25, dens=0.35)
    x = 108 + 34 * ease(seg(t, 16.85, 18.0))
    walking = t < 18.0
    door_x = 128
    op = ease(seg(t, 18.3, 18.7))
    if op > 0:  # door 302 opens into the dark room
        c.rect(door_x, 52, 42, 76, hx('#141830'))
        c.rect(door_x + 4, 58, 20, 26, hx('#26305a'))  # a sliver of the window across the room
        rain(c, t, 10, 9, speed=200, wind=-30, length=4, col=hx('#3e4a7a'), area=(door_x + 4, 58, door_x + 24, 84))
        pw = int(42 * (1 - op * 0.82))
        c.rect(door_x + 42 - pw, 52, pw, 76, hx('#2a1a1a') if not on else hx('#7a4a34'))
        c.rect(door_x + 42 - pw, 52, 1, 76, hx('#100a0a'))
    if walking:
        spr = chibi('he', 'side', 'walk', phase=((t - 16.85) * 1.5) % 1, eyes='down', bag=True)
    elif t < 18.75:
        spr = chibi('he', 'side', 'stand', eyes='closed' if blink(t) else 'open', bag=True)
    else:
        spr = chibi('he', 'back', 'walk', phase=((t - 18.75) * 1.6) % 1, bag=True)
    am = 1.0
    xx, yy = x, 140
    if t >= 18.75:
        q = seg(t, 18.75, 19.15)
        xx = 142 + 8 * q; yy = 140 - 8 * q
        am = 1 - q * 0.8
    blit_chibi(c, lit(spr, 'corridor' if on else 'dark'), xx, yy, alpha_mul=am)
    if 17.58 <= t < 17.62:
        c.a[:] = (c.a.astype(np.float32) * 0.5).astype(np.uint8)
    return upk(c, 146, 96, 2)


# ================================================================ S02 into the room, to the window
@shot('room_window')
def room_window(t):
    c = room(t, 'night')
    drop = seg(t, 19.22, 19.40)
    # the bag lands by the bed
    bx, by = 150, 141
    if t < 19.22:
        spr = chibi('he', 'side', 'stand', bag=True, eyes='down')
        blit_chibi(c, lit(spr, 'night'), 152, 142, flip=True)
    else:
        yb = by - 12 + 12 * ease_in(drop)
        c.rect(bx - 3, yb - 8, 7, 9, BAG); c.rect(bx - 3, yb, 7, 1, BAG_DK); c.rect(bx - 3, yb - 8, 7, 1, BAG_LT)
        c.rect(bx - 4, yb - 8, 1, 9, OUT); c.rect(bx + 4, yb - 8, 1, 9, OUT); c.rect(bx - 3, yb + 1, 7, 1, OUT)
        if 19.40 <= t < 19.6:
            for k in range(-3, 4, 2):
                c.px(bx + k * 2, by - 1 - (t - 19.4) * 10, hx('#6a6a88'))
        q = seg(t, 19.5, 20.35)
        x = 140 - 48 * ease(q)
        if t < 20.35:
            spr = chibi('he', 'side', 'walk' if 19.5 < t else 'stand', phase=((t - 19.5) * 1.6) % 1, eyes='down')
            blit_chibi(c, lit(spr, 'night'), x, 142, flip=True)
        else:
            spr = chibi('he', 'back', 'stand')
            blit_chibi(c, lit(spr, 'night'), 92, 142)
    return c


# ================================================================ S03 the window glass: reflection + a memory flicker
@shot('window_reflect')
def window_reflect(t):
    c = room_static('night').copy()
    window_view(c, t, 'night', rain_k=1.3)
    x0, y0, w, h = WIN
    # memory flicker of the bookstore in the left pane
    f = ease(seg(t, 21.3, 22.4))
    if f > 0:
        pic = mini_pic('store', 48, 40)
        pic = Cv(arr=grade_warm(pic.a, 0.3))
        k = (0.2 + 0.6 * f) * (0.9 + 0.1 * math.sin(t * 25))
        sub = c.a[y0 + 1:y0 + 41, x0 + 1:x0 + 49].astype(np.float32)
        c.a[y0 + 1:y0 + 41, x0 + 1:x0 + 49] = (sub * (1 - k) + pic.a * k).astype(np.uint8)
    # his reflection (soft blend)
    b = light(bust('he', 'down' if t < 21.9 else 'open', 'line', 'sad'), (0.5, 0.56, 0.85))
    bx_, by_ = 90 - 36, 66 - 38
    reg = c.a[by_:by_ + b.h, bx_:bx_ + b.w].astype(np.float32)
    m = b.a[..., 3] > 127
    reg[m] = reg[m] * 0.68 + b.a[..., :3][m].astype(np.float32) * 0.32
    c.a[by_:by_ + b.h, bx_:bx_ + b.w] = reg.astype(np.uint8)
    glass_rain(c, t, x0, y0, w, h, seed=24, n=18, static=40)
    return upk(c, 90, 63, 2)


# ================================================================ S04 the new book (memory 2021.03.13)
@shot('book_cover')
def book_cover_shot(t):
    c = Cv(160, 90)
    bokeh_bg(c, t, 'store', n=12)
    lift = int((1 - ease_out(seg(t, 22.9, 23.3))) * 8)
    n = sum(1 for tc in (23.69, 23.87, 24.05, 24.23) if t + 0.06 >= tc)
    for (hx_, d) in ((50, 1), (110, -1)):
        hand(c, hx_, 52 + lift, SK_HE, SKD_HE, NAVY, NAVY_DK, d=d, s=1.0, fingers=False)
    book_cover(c, 52, 2 + lift, 56, 72, lit_chars=n, glow=seg(t, 24.23, 24.8) if n == 4 else 0)
    for (tx, d) in ((52, 1), (107, -1)):
        c.rect(tx - (0 if d > 0 else 3), 48 + lift, 4, 7, SK_HE); c.rect(tx - (0 if d > 0 else 3), 54 + lift, 4, 1, SKD_HE)
    c = up2(c)
    return memory_post(c, t, stamp='2021.03.13')


# ================================================================ S05 books piling up by the bed (memory)
PILE = [(24.88, hx('#c84a3a'), 22, 6), (25.36, hx('#5a6aa8'), 24, 5), (25.72, hx('#e0b050'), 20, 6), (25.96, hx('#7a9a5a'), 23, 5),
        (26.14, hx('#2a5a7a'), 18, 6)]


@shot('book_pile')
def book_pile(t):
    c = room(t, 'day', win_mode='day')
    he = chibi('he', 'front', 'sit', eyes='closed' if blink(t) else 'down', prop=None)
    blit_chibi(c, lit(he, 'day'), 262, 110)
    c.rect(257, 93, 11, 5, hx('#2a5a7a')); c.rect(262, 93, 1, 5, CREAM)  # the book on his lap
    base = 129
    y = base
    for i, (tc, col, bw, bh) in enumerate(PILE):
        if t + 0.06 < tc:
            break
        q = ease_in(seg(t + 0.06, tc, tc + 0.12))
        yy = (y - bh) - (1 - q) * 30
        xx = 196 - bw // 2 + (i % 2) * 2 - 1
        c.rect(xx, yy, bw, bh, col); c.rect(xx, yy, bw, 1, mix(col, (255, 255, 255), 0.35))
        c.rect(xx + 1, yy + 2, bw - 2, 1, CREAM)
        c.rect(xx - 1, yy, 1, bh, OUT); c.rect(xx + bw, yy, 1, bh, OUT)
        if q >= 1 and t + 0.06 < tc + 0.2:
            c.px(xx - 3, yy + bh - 2, hx('#fff0d0')); c.px(xx + bw + 2, yy + bh - 2, hx('#fff0d0'))
        y -= bh
    c.rect(186, 129, 22, 1, OUT)
    out = upk(c, 230, 100, 2)
    return memory_post(out, t, stamp='2021.03.13')


# ================================================================ S06 pages 1 / 6 / 7 / preface
@shot('pages')
def pages(t):
    c = Cv(160, 90, hx('#b8865a'))
    for y in range(0, 90, 9):
        c.rect(0, y, 160, 1, hx('#9c6e48'))
    tt = t + 0.06
    if tt < 26.96:
        left = dict(num=None, lines=None)
        right = dict(num=1, title='半岛铁盒', tcol=hx('#2a5a7a'), lines=1)
        fl = None
    else:
        fl = seg(tt, 26.96, 27.2)
        left = dict(num=6, lines=6)
        right = dict(num=7, lines=7, title='序' if tt >= 27.86 else None)
        if fl < 1:
            left = dict(num=None, lines=None) if fl < 0.5 else left
    open_book(c, 80, 9, 58, 72, left=left, right=right, flip=fl)
    if tt < 26.96:
        c.rect(22, 9, 58, 72, hx('#2a5a7a')); c.rect(76, 9, 4, 72, hx('#1e4256'))  # inside cover
    if tt >= 27.86:
        q = seg(tt, 27.86, 28.3)
        for k in range(6):
            a = k / 6 * 2 * math.pi + q * 4
            c.px(109 + math.cos(a) * (9 + q * 6), 17 + math.sin(a) * (6 + q * 4), hx('#fff0b0'))
    # his hand holding the left page; her finger points from the top right on 七
    hand(c, 30, 78, SK_HE, SKD_HE, NAVY, NAVY_DK, d=1)
    if tt >= 27.44:
        q = ease_out(seg(tt, 27.44, 27.62))
        hand(c, 150 - 22 * q, 44 - 4 * q, SK_SHE, SKD_SHE, CREAMS, CREAMS_DK, d=-1, point=True)
    out = up2(c)
    return memory_post(out, t, stamp='2021.03.18')


# ================================================================ S07/S08 reading together on the bed edge, then she fades
def reading_pair(t, mode='day', she_alpha=1.0, she=True):
    c = room(t, mode, win_mode=mode)
    laugh = 29.36 < t < 30.2
    he = chibi('he', 'front', 'sit', eyes='open' if not blink(t) else 'closed', look=1 if (mode == 'day' and t > 28.9) else 0,
               mouth='smile' if mode == 'day' else 'line')
    blit_chibi(c, lit(he, mode), 244, 140)
    if she and she_alpha > 0:
        s = chibi('she', 'front', 'sit', eyes='smile' if laugh else ('closed' if blink(t, 2) else 'down'),
                  mouth='big' if laugh else 'smile', arm='cup')
        blit_chibi(c, lit(s, mode), 264, 140 + (1 if laugh and int(t * 8) % 2 else 0), alpha_mul=she_alpha)
        if she_alpha > 0.5:
            c.rect(257, 121, 13, 6, CREAM); c.rect(257, 121, 13, 1, hx('#2a5a7a')); c.rect(263, 121, 1, 6, hx('#c8bc9c'))
    return c


@shot('read_together')
def read_together(t):
    c = reading_pair(t, 'day')
    if 29.0 < t < 29.9:
        c.blit(emote('heart', hx('#e84a5f')), 250, 94)
    out = upk(c, 252, 112, 2)
    return memory_post(out, t, stamp='2021.03.18')


@shot('read_fade')
def read_fade(t):
    f = ease(seg(t, 30.9, 31.6))
    A = reading_pair(t, 'day')
    A = memory_post(upk(A, 252, 112, 2), t, stamp='2021.03.18' if f < 0.5 else None)
    B = reading_pair(t, 'night', she_alpha=1 - ease(seg(t, 31.0, 31.6)))
    B = upk(B, 252, 112, 2)
    return Cv(arr=dither_blend(A.a, B.a, f))


# ================================================================ S09 his close-up, rain shadows
@shot('he_bust_rain')
def he_bust_rain(t):
    c = Cv(W, H, hx('#1c2040'))
    for x in range(0, W, 12):
        c.rect(x, 0, 1, H, hx('#22264a'))
    for i in range(3):
        x0 = 26 + i * 40
        c.poly([(x0, 0), (x0 + 24, 0), (x0 + 44, H), (x0 + 20, H)], hx('#283060'))
    eyes = 'down'
    if blink(t, 1):
        eyes = 'closed'
    b = bust('he', eyes, 'line', 'sad', look=0 if t < 33.2 else 1)
    by = 70 + int(ease(seg(t, 33.2, 33.8)) * 3)
    c.blit(lit(b, 'night'), 124, by)
    rain_shadows(c, t, 0, W, 0, H, seed=4, k=0.3)
    return c


# ================================================================ S10 pulling the tin out from under the bed
@shot('under_bed')
def under_bed(t):
    c = room(t, 'night')
    bg = c.a.copy()
    q = ease_out(seg(t, 34.35, 35.0))
    tx = 240 - 30 * q
    tin_small(c, tx, 131, rust=0.6, dusty=1)
    c.a[96:131, 214:] = bg[96:131, 214:]
    if tx > 214:
        pass
    arm = 75 if t < 34.3 else (60 if t < 35.0 else 40)
    spr = chibi('he', 'side', 'crouch', arm=arm, eyes='down')
    blit_chibi(c, lit(spr, 'night'), 194, 142)
    if t >= 35.0:
        d = t - 35.0
        r = np.random.default_rng(9)
        for i in range(26):
            a = r.uniform(math.pi, 2 * math.pi); sp = r.uniform(8, 26)
            x = tx + math.cos(a) * sp * min(d, 0.8) * 1.6
            y = 128 + math.sin(a) * sp * min(d, 0.8) * 0.8 + d * 3
            if d < 1.0 + r.uniform(0, 0.6):
                c.px(x, y, hx('#8a88a0') if i % 2 else hx('#b0aec0'))
    return upk(c, 200, 112, 2)


# ================================================================ S11–S13 the rusty tin: keyhole, light, rust
def tin_closeup(t, rust=0.35, key_light=0.0, cx_off=0):
    c = Cv(160, 90)
    vgrad(c, 0, 90, [hx('#141626'), hx('#1c1c30'), hx('#26223a')])
    c.rect(0, 70, 160, 20, hx('#2a2236'))
    for y in range(74, 90, 5):
        c.rect(0, y, 160, 1, hx('#211a2c'))
    # torch pool from the right
    yy, xx = np.mgrid[0:90, 0:160]
    m = (((xx - 100) / 1.6) ** 2 + (yy - 52) ** 2 < 46 ** 2) & (bayer(90, 160) < 0.42)
    c.a[m] = (c.a[m].astype(np.float32) * 0.75 + np.array([150, 148, 175]) * 0.25).astype(np.uint8)
    kx, ky = tin(c, 40 + cx_off, 42, 80, 30, 10, rust=rust, dusty=0.75, lit=(0.78, 0.8, 0.95))
    if key_light > 0:
        c.rect(kx - 1, ky - 3, 2, 2, hx('#fff2c8')); c.rect(kx - 1, ky - 1, 2, 3, hx('#fff2c8'))
        for k in range(8):
            a = k / 8 * 2 * math.pi
            r1, r2 = 4, 4 + 6 * key_light
            c.line(kx + r1 * math.cos(a), ky + r1 * math.sin(a), kx + r2 * math.cos(a), ky + r2 * math.sin(a), hx('#f6e6b0'))
    return c, kx, ky


@shot('box_close')
def box_close(t):
    c, kx, ky = tin_closeup(t, 0.35, cx_off=int(round(math.sin(t * 0.8) * 1)))
    if t + 0.06 >= 37.03:
        c.px(kx + 3, ky - 4, (255, 255, 255))
    return up2(c)


@shot('keyhole')
def keyhole(t):
    rust = 0.35 + 0.5 * ease(seg(t, 38.2, 39.3))
    kl = ease_out(seg(t + 0.06, 37.70, 38.0))
    c, kx, ky = tin_closeup(t, rust, key_light=kl)
    return upk(c, kx, ky + 2, 3)


@shot('rust_punch')
def rust_punch(t):
    c, kx, ky = tin_closeup(t, 0.88, key_light=1.0)
    tt = t + 0.06
    if tt < 39.65:
        return upk(c, kx, ky + 2, 3)
    if tt < 40.13:
        return upk(c, 46, 34, 4)
    return upk(c, 112, 64, 5)


# ================================================================ S14/S15 dust around him in the torch beam; it gets dark
def floor_sit(t, n_dust=40, dark=0.0, torch=True):
    c = room(t, 'night', rain_k=0.8)
    c.a[:] = darken_flat(c.a, 0.62)
    he = chibi('he', 'front', 'sit', eyes='down' if not blink(t) else 'closed')
    blit_chibi(c, light(he, (0.72, 0.72, 0.88), rim=(255, 236, 190), rim_side=1, rim_k=0.55), 146, 150)
    tin_small(c, 166, 156, rust=0.7, dusty=1)
    # phone on the floor shining up-left
    c.rect(192, 150, 8, 2, hx('#24202e'))
    bm = beam_mask([(194, 150), (198, 150), (120, 60), (70, 100)])
    if torch:
        apply_beam(c, bm, (230, 226, 210), k=0.28, dens=0.5)
        c.rect(193, 149, 2, 1, (255, 255, 240))
    dust(c, t, n_dust, 52, swirl=(150, 128, 38, 1.1), col=hx('#e8e0c8'), col2=hx('#5a5a78'), beam=bm if torch else None)
    dust(c, t, 20, 53, area=(60, 40, 260, 160), col=hx('#c8c0b0'), col2=hx('#4a4a66'), speed=2, beam=bm if torch else None)
    if dark > 0:
        a = vignette(c.a, dark * 2.2, col=(4, 4, 8))
        c = Cv(arr=a)
        dim_to(c, dark * 0.5, (4, 4, 8))
    return c


@shot('dust_swirl')
def dust_swirl(t):
    n = int(20 + 70 * ease(seg(t, 40.84, 42.6)))
    return upk(floor_sit(t, n), 150, 118, 2)


@shot('dark_steps')
def dark_steps(t):
    tt = t + 0.06
    dark = 0.0 + (0.3 if tt >= 43.28 else 0) + (0.3 if tt >= 43.82 else 0)
    torch = not (43.28 <= tt < 43.36 or 43.82 <= tt < 43.9)
    return upk(floor_sit(t, 90, dark, torch), 150, 118, 2)


# ================================================================ S16 searching for the key
FLY = [(44.72, 'pencil'), (45.20, 'paper'), (45.56, 'eraser'), (45.86, 'paper'), (46.04, 'pencil')]


@shot('search')
def search(t):
    c = room(t, 'night')
    glow(c, 6, 98, 46, hx('#ffd68a'), k=0.35, dens=0.5)
    c.rect(1, 96, 9, 4, hx('#ffe0a0'))
    tt = t + 0.06
    op = ease_out(seg(tt, 44.48, 44.7))
    # drawer pulled out of the desk
    c.rect(4 + int(op * 10), 112, 24, 8, hx('#5a3a30')); c.rect(4 + int(op * 10), 112, 24, 1, hx('#7a5040'))
    c.rect(14 + int(op * 10), 115, 4, 1, hx('#d8b048'))
    for i, (tc, kind) in enumerate(FLY):
        if tt < tc:
            continue
        d = tt - tc
        x = 30 + d * (40 + i * 12)
        y = 110 - d * 60 + d * d * 110
        if y > 150:
            y = 150
        if kind == 'pencil':
            c.line(x, y, x + 5, y - 2 if i % 2 else y + 2, hx('#e0b050'))
        elif kind == 'paper':
            c.rect(x, y, 6, 5, hx('#e8e4dc')); c.rect(x + 1, y + 1, 4, 1, hx('#9a98a8'))
        else:
            c.rect(x, y, 3, 2, hx('#f08ac0'))
    shake = tt >= 46.22
    if shake:
        jx = int(round(math.sin(t * 60) * 1.5))
        spr = chibi('he', 'side', 'stand', arm=110, eyes='open')
        blit_chibi(c, lit(spr, 'lamp'), 52, 142, flip=True)
        tin_small(c, 42 + jx, 125, rust=0.7, dusty=1)
        if tt > 46.4:
            c.blit(emote('q', hx('#3a3a5a')), 50, 92)
    else:
        spr = chibi('he', 'side', 'stand', arm=70 if int(t * 5) % 2 else 85, eyes='down')
        blit_chibi(c, lit(spr, 'lamp'), 52, 142, flip=True)
        tin_small(c, 72, 143, rust=0.7, dusty=1)
    return upk(c, 80, 108, 2)


# ================================================================ S17 candy jar + the new tin (memory 2022.02.14)
def desk_warm(t):
    c = Cv(160, 90, hx('#e8c890'))
    vgrad(c, 0, 56, [hx('#f6e0b0'), hx('#f0d0a0'), hx('#e8c090')])
    c.rect(0, 56, 160, 34, hx('#a8744a'))
    for y in range(60, 90, 6):
        c.rect(0, y, 160, 1, hx('#946440'))
    c.rect(0, 56, 160, 1, hx('#c8946a'))
    # window light stripes
    for i in range(3):
        x0 = 20 + i * 44
        c.poly([(x0, 0), (x0 + 16, 0), (x0 + 30, 56), (x0 + 14, 56)], hx('#fbecc8'))
    return c


@shot('candy_jar')
def candy_jar_shot(t):
    c = desk_warm(t)
    candy_jar(c, 20, 80, w=42, h=50, fill=0.75)
    tt = t + 0.06
    q = ease_out(seg(tt, 47.49, 47.9))
    tx = 170 - 82 * q
    tin(c, tx, 54, 58, 24, 8, rust=0.0)
    # her hands pushing it in, then placing a candy on the lid
    if tt < 48.2:
        hand(c, tx + 62, 64, SK_SHE, SKD_SHE, CREAMS, CREAMS_DK, d=-1)
    pc = ease_out(seg(tt, 48.33, 48.7))
    if tt >= 48.2:
        hx_ = 118 - 6 * pc; hy_ = 10 + 30 * pc - (6 * ease(seg(tt, 48.83, 49.2)) if tt > 48.83 else 0)
        if tt < 48.83:
            candy_px(c, hx_ - 8, hy_ + 4, CANDY[0], big=True)
        hand(c, hx_, hy_, SK_SHE, SKD_SHE, CREAMS, CREAMS_DK, d=-1)
    if tt >= 48.83:
        candy_px(c, 110, 41, CANDY[0], big=True)
        if tt < 49.2:
            for k in range(6):
                a = k / 6 * 2 * math.pi
                c.px(110 + 10 * math.cos(a), 41 + 6 * math.sin(a), (255, 255, 255))
    out = up2(c)
    return memory_post(out, t, stamp='2022.02.14', k=0.22)


# ================================================================ S18 she offers a candy / S18b he smiles
def pinch(c, x, y, s=1):
    """hand pinching a wrapped candy at (x,y) (candy center), sleeve going down."""
    sp = Cv(40 * s, 60 * s, alpha=True)
    ox, oy = 20 * s, 8 * s
    sp.rect(ox - 7 * s, oy + 16 * s, 15 * s, 44 * s, CREAMS + (255,)); sp.rect(ox + 5 * s, oy + 16 * s, 3 * s, 44 * s, CREAMS_DK + (255,))
    sp.ellipse(ox, oy + 9 * s, 7 * s, 6 * s, SK_SHE + (255,))
    sp.ellipse(ox - 6 * s, oy + 7 * s, 2.5 * s, 2.5 * s, SK_SHE + (255,))
    for k in range(3):
        sp.rect(ox - 3 * s + k * 3 * s, oy + 4 * s, 1, 3 * s, SKD_SHE + (255,))
    sp.rect(ox - 4 * s, oy + 13 * s, 8 * s, 1 * s, SKD_SHE + (255,))
    spo = outline(sp)
    c.blit(spo, x - ox - 1, y - oy - 1)
    k = 1.0 if s == 1 else 1.8
    c.ellipse(x, y, 3.2 * k, 2.4 * k, CANDY[1])
    c.poly([(x - 3 * k, y), (x - 7 * k, y - 3 * k), (x - 7 * k, y + 3 * k)], mix(CANDY[1], (255, 255, 255), 0.3))
    c.poly([(x + 3 * k, y), (x + 7 * k, y - 3 * k), (x + 7 * k, y + 3 * k)], mix(CANDY[1], (255, 255, 255), 0.3))
    c.px(x - 1, y - 1, (255, 255, 255))


@shot('candy_give')
def candy_give(t):
    c = Cv(W, H)
    bokeh_bg(c, t, 'pink', seed=8)
    tt = t + 0.06
    laugh = tt >= 50.57
    eyes = 'smile' if tt >= 51.41 else ('closed' if blink(t, 3) else 'open')
    b = bust('she', eyes, 'bigsmile' if 50.57 <= tt < 51.6 else 'smile', 'up' if laugh else 'calm')
    bob = int(round(math.sin(t * 7))) if 50.57 <= tt < 51.6 else 0
    c.blit(b, 112, 72 + bob)
    # her hand pinching the candy, raised toward the camera
    q = ease_out(seg(tt, 49.73, 50.3))
    s = 1 if tt < 50.0 else 2
    hx_, hy_ = 200 - 6 * q, 178 - 58 * q
    pinch(c, hx_, hy_, s)
    if tt >= 51.83:
        c.blit(emote('heart', hx('#e84a5f')), 176, 56)
    if tt >= 52.25:
        r = np.random.default_rng(int(t * 10))
        for i in range(8):
            c.px(hx_ + r.integers(-14, 15), hy_ + r.integers(-10, 11), (255, 255, 255))
    return memory_post(c, t, stamp='2022.02.14', k=0.2)


@shot('candy_he')
def candy_he(t):
    c = Cv(W, H)
    bokeh_bg(c, t, 'mem', seed=9)
    tt = t + 0.06
    eyes = 'smile' if tt > 52.6 else 'open'
    b = bust('he', eyes, 'smile', 'up' if tt > 53.3 else 'calm', look=0)
    c.blit(b, 124, 72)
    # a candy stick in his mouth? just the wrapper in his fingers
    candy_px(c, 206, 140, CANDY[1], big=True)
    c.ellipse(206, 150, 7, 6, SK_HE); c.rect(198, 154, 16, 30, NAVY)
    if int(t * 6) % 2 == 0:
        c.px(212, 136, (255, 255, 255)); c.px(200, 134, (255, 255, 255))
    if tt > 53.2:
        c.blit(emote('note', hx('#5a4a6a')), 186, 64)
    return memory_post(c, t, stamp='2022.02.14', k=0.2)


# ================================================================ S19 filtering "you and me" (present, photo editor)
FILTERS = [(0.0, '原图'), (55.71, '怀旧'), (56.49, '褪色'), (57.21, '柔光')]


def apply_filter(a, k):
    if k == 0:
        return a
    if k == 1:
        return vignette(grade_warm(a, 0.6), 0.6, col=(60, 36, 24))
    if k == 2:
        L = lum(a.astype(np.float32))[..., None] * 255
        g = a.astype(np.float32) * 0.45 + L * 0.55
        return np.clip(g * 0.65 + 255 * 0.35, 0, 255).astype(np.uint8)
    out = np.clip(a.astype(np.float32) * 1.12 + np.array([28, 18, 22]), 0, 255).astype(np.uint8)
    out = grade_warm(out, 0.25)
    h, w = out.shape[:2]
    br = lum(out.astype(np.float32)) > 0.55
    sp = np.zeros_like(br)
    for dy, dx in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        sp |= np.roll(np.roll(br, dy, 0), dx, 1)
    m = sp & (bayer(h, w) < 0.5)
    out[m] = np.clip(out[m].astype(np.float32) * 0.6 + 255 * 0.4, 0, 255).astype(np.uint8)
    return out


@shot('photo_filter')
def photo_filter(t):
    c = Cv(W, H)
    bokeh_bg(c, t, 'night', seed=4)
    c.a[:] = darken_flat(c.a, 0.7)
    x0, sw, sh = 85, 150, 180
    phone_body(c, x0, 0, sw, sh)
    scr = Cv(sw, sh, hx('#101218'))
    scr.rect(0, 0, sw, 22, hx('#181a24'))
    text(scr, 6, 5, '编辑', hx('#eef0f6'), font='w')
    rrect(scr, sw - 34, 4, 30, 14, hx('#e0b050'), r=3)
    text(scr, sw - 31, 5, '完成', hx('#2a2020'), font='w')
    photo = Cv(sw - 12, 104)
    wallpaper_umbrella(photo, 1.0)
    tt = t + 0.06
    k = max(i for i, (tc, _) in enumerate(FILTERS) if tt >= tc)
    photo.a[:] = apply_filter(photo.a, k)
    scr.paste(photo, 6, 28)
    # thumbnails
    for i, (_, name) in enumerate(FILTERS):
        tx = 6 + i * 35
        th = Cv(32, 22)
        th.a[:] = apply_filter(wallpaper_thumb(), i)
        scr.paste(th, tx, 140)
        if i == k:
            scr.rect(tx - 1, 139, 34, 1, hx('#e0b050')); scr.rect(tx - 1, 162, 34, 1, hx('#e0b050'))
            scr.rect(tx - 1, 139, 1, 24, hx('#e0b050')); scr.rect(tx + 32, 139, 1, 24, hx('#e0b050'))
        text(scr, tx + (32 - text_w(name, 'w')) // 2, 165, name, hx('#e0b050') if i == k else hx('#8a8ea0'), font='w')
    c.paste(scr, x0, 0)
    # his thumb tapping each filter
    for (tc, _), i in zip(FILTERS[1:], range(1, 4)):
        if tc - 0.12 <= tt < tc + 0.1:
            tx = x0 + 6 + i * 35 + 16
            c.ellipse(tx, 160, 7, 8, SK_HE); c.rect(tx - 4, 166, 9, 14, SK_HE)
    return c


_THUMB = None


def wallpaper_thumb():
    global _THUMB
    if _THUMB is None:
        p = Cv(138, 104)
        wallpaper_umbrella(p, 1.0)
        _THUMB = p.a[10:98:4, 3:131:4].copy()
    return _THUMB


# ================================================================ S20 the pretty memory: the two under her red umbrella (2022.11.20)
@shot('umbrella_pretty')
def umbrella_pretty(t):
    c = gate(t, rain_k=0.55)
    x = 116 + 70 * seg(t, 57.9, 61.85)
    ph = ((t - 57.9) * 1.3) % 1
    she = chibi('she', 'side', 'walk', phase=(ph + 0.5) % 1, eyes='smile', mouth='smile', arm=150)
    he = chibi('he', 'side', 'walk', phase=ph, eyes='open', look=0, mouth='smile', bag=True)
    blit_chibi(c, lit(she, 'rain'), x + 10, 164)
    blit_chibi(c, lit(he, 'rain'), x - 2, 164)
    umbrella(c, x + 12, 141, *RED_UMB, open_=1.0, w=46, tilt=-8, shaft=17)
    c = upk(c, x + 6, 128, 2)
    # soft bokeh bloom
    r = np.random.default_rng(12)
    yy, xx = np.mgrid[0:H, 0:W]
    for i in range(10):
        bx_ = r.uniform(0, W) + math.sin(t * 0.4 + i) * 4; by_ = r.uniform(0, 110); br = r.uniform(8, 18)
        m = ((xx - bx_) ** 2 + (yy - by_) ** 2 < br * br) & (bayer() < 0.22)
        c.a[m] = np.clip(c.a[m].astype(np.float32) * 0.5 + np.array([255, 214, 150]) * 0.5, 0, 255).astype(np.uint8)
    if t > 58.85:
        r2 = np.random.default_rng(int(t * 8))
        for i in range(6):
            c.px(r2.integers(0, W), r2.integers(0, 120), (255, 246, 220))
    return memory_post(c, t, stamp='2022.11.20', k=0.08, vig=0.5)


# ================================================================ S21 inside the box (imagined): keepsakes sinking
SINK = [(61.9, 'note', 40, 0), (62.3, 'read', 112, -12), (62.9, 'pick', 70, 0), (63.4, 'candy', 128, 0),
        (63.9, 'umbrella', 34, 10), (64.6, 'her', 84, 0)]


@shot('box_inside')
def box_inside(t):
    c = Cv(160, 90)
    vgrad(c, 0, 90, [hx('#0c2a30'), hx('#103640'), hx('#14404a'), hx('#0e2c34')])
    for y in range(0, 90, 7):  # caustic wobble lines
        for x in range(0, 160, 2):
            if math.sin(x * 0.15 + t * 2 + y) > 0.85:
                c.px(x, y + math.sin(x * 0.2 + t) * 1.5, hx('#2a6a70'))
    # the inside walls of the tin + the lid seen from below
    c.poly([(0, 0), (18, 10), (18, 80), (0, 90)], hx('#0a2228')); c.poly([(160, 0), (142, 10), (142, 80), (160, 90)], hx('#0a2228'))
    c.rect(0, 0, 160, 10, hx('#5a2a1a')); c.rect(0, 9, 160, 1, hx('#7a3a22'))
    for x in range(4, 160, 11):
        c.rect(x, 3 + (x % 3), 3, 2, hx('#a4542a'))
    c.poly([(18, 80), (142, 80), (160, 90), (0, 90)], hx('#081c20'))
    # keyhole light from above
    c.rect(78, 4, 4, 6, hx('#fff2c8'))
    bm = Cv(160, 90, alpha=True)
    bm.poly([(78, 0), (82, 0), (110, 90), (50, 90)], (255, 255, 255))
    m = (bm.a[..., 3] > 0) & (bayer(90, 160) < 0.3)
    c.a[m] = (c.a[m].astype(np.float32) * 0.6 + np.array([120, 200, 190]) * 0.4).astype(np.uint8)
    for (t0, kind, x, rot) in SINK:
        if t < t0:
            continue
        d = t - t0
        y = 6 + d * 15 - d * d * 1.2
        y = min(y, 64)
        xx = x + math.sin(d * 1.6 + x) * 5
        rr = rot + math.sin(d * 1.3) * 8
        if kind in ('read', 'umbrella', 'her'):
            pk = 'roof' if kind == 'her' else kind
            polaroid(c, xx, y, pk, w=24, h=28, rot=int(rr))
            if kind == 'her':
                gl = 0.5 + 0.5 * math.sin(t * 4)
                for k in range(10):
                    a = k / 10 * 2 * math.pi + t
                    c.px(xx + math.cos(a) * 17, y + math.sin(a) * 19, mix(hx('#fff2c8'), hx('#2a6a70'), 1 - gl))
        elif kind == 'pick':
            from ui_tiny import pix
            pix(c, [".##.##.", "#######", "#######", ".#####.", "..###..", "...#..."], xx - 3, y - 3, PICK)
            c.px(xx - 2, y - 2, (255, 255, 255))
        elif kind == 'candy':
            candy_px(c, xx, y, CANDY[2], big=True)
        else:  # folded note with a heart
            c.rect(xx - 8, y - 6, 16, 11, hx('#f6efdc')); c.line(xx - 8, y - 6, xx, y - 1, hx('#d8ccb0'))
            c.line(xx + 7, y - 6, xx, y - 1, hx('#d8ccb0'))
            c.px(xx, y + 2, hx('#e84a5f')); c.px(xx - 1, y + 1, hx('#e84a5f')); c.px(xx + 1, y + 1, hx('#e84a5f'))
    r = np.random.default_rng(3)
    for i in range(16):  # bubbles
        bx_ = r.uniform(0, 160); sp = r.uniform(6, 14)
        by_ = (r.uniform(0, 90) - t * sp) % 90
        c.px(bx_ + math.sin(t * 2 + i) * 1.5, by_, hx('#5aa0a0'))
    return up2(c)


# ================================================================ S22 rooftop at sunset, sharing earphones
@shot('joy')
def joy(t):
    c = Cv(W, H)
    vgrad(c, 0, 120, [hx('#5a4a8a'), hx('#a0608a'), hx('#e0806a'), hx('#f6a860'), hx('#fde0a0')])
    c.ellipse(232, 104, 16, 16, hx('#fff0c0'))
    cs = cloud_sprite(90, 24, 6, hx('#f6b0a0'), hx('#fde0c8'), hx('#c88090'))
    c.blit(cs, int(60 - t * 2) % 400 - 80, 34)
    buildings(c, 128, 71, hx('#5a3a5a'), win=hx('#fde0a0'), lit=0.15, hmin=14, hmax=48)
    buildings(c, 132, 72, hx('#462c48'), win=None, hmin=6, hmax=22)
    c.rect(0, 132, W, 48, hx('#6a4a5a'))
    c.rect(0, 132, W, 2, hx('#8a6070'))
    for x in range(0, W, 14):  # railing
        c.rect(x, 116, 1, 16, hx('#3a2a3a'))
    c.rect(0, 116, W, 2, hx('#3a2a3a'))
    tt = t + 0.06
    sway = int(round(math.sin(t * 3.4)))
    he = chibi('he', 'front', 'sit', eyes='closed' if tt > 66.1 else 'open', mouth='smile', look=1)
    she = chibi('she', 'front', 'sit', eyes='smile', mouth='smile', look=-1)
    blit_chibi(c, lit(he, 'sunset'), 150, 146)
    blit_chibi(c, lit(she, 'sunset'), 170 + sway * 0, 146 + (1 if sway > 0 else 0))
    # shared earphones: white wire from his right ear and her left ear down to a phone between them
    c.line(155, 117, 160, 132, hx('#f6f2ec')); c.line(165, 117 + (1 if sway > 0 else 0), 160, 132, hx('#f6f2ec'))
    c.rect(158, 132, 4, 6, hx('#24202e'))
    for tc, x in ((65.70, 142), (66.12, 178), (66.78, 160)):
        if tt >= tc:
            q = tt - tc
            c.blit(emote('note', hx('#7a4a5a')), x - 6 + math.sin(q * 3) * 3, 84 - q * 6)
    for i in range(3):  # birds
        bx_ = (t * 18 + i * 60) % 380 - 30; by_ = 40 + i * 8 + math.sin(t * 2 + i) * 2
        w_ = int(t * 6 + i) % 2
        c.px(bx_, by_, hx('#3a2a3a')); c.px(bx_ - 1, by_ - w_, hx('#3a2a3a')); c.px(bx_ + 1, by_ - w_, hx('#3a2a3a'))
    c = upk(c, 160, 118, 2)
    return memory_post(c, t, stamp='2022.06.30', k=0.12, vig=0.5)


# ================================================================ S23 I want to remember, but I can't: her face pixelates away
def pixelate(a, b):
    if b <= 1:
        return a
    h, w = a.shape[:2]
    hh, ww = (h + b - 1) // b, (w + b - 1) // b
    pad = np.zeros((hh * b, ww * b, 3), np.float32)
    pad[:h, :w] = a
    pad[h:, :w] = a[-1:, :]
    pad[:, w:] = pad[:, w - 1:w]
    m = pad.reshape(hh, b, ww, b, 3).mean((1, 3))
    return np.repeat(np.repeat(m, b, 0), b, 1)[:h, :w].astype(np.uint8)


@shot('forget')
def forget(t):
    c = Cv(W, H)
    bokeh_bg(c, t, 'mem', seed=13)
    tt = t + 0.06
    eyes = 'smile' if tt < 71.74 else ('closed' if blink(t, 4) else 'open')
    b = bust('she', eyes, 'smile' if tt < 72.5 else 'line', 'calm')
    c.blit(b, 124, 70)
    c = memory_post(c, t, stamp='2022.--.--' if tt > 72.6 else '2022.12.24', k=0.25)
    bl = 1
    for tc, v in ((72.58, 2), (73.24, 3), (73.60, 5), (73.90, 8), (74.40, 12)):
        if tt >= tc:
            bl = v
    a = pixelate(c.a, bl)
    g = ease(seg(tt, 73.24, 74.5))
    if g > 0:
        L = (lum(a.astype(np.float32)) * 255)[..., None]
        a = np.clip(a.astype(np.float32) * (1 - g) + L * g, 0, 255).astype(np.uint8)
    return Cv(arr=a)
