# -*- coding: utf-8 -*-
"""Intro (B-style chat long take) + title for 《半岛铁盒》. 0.00–16.85."""
import math
from functools import lru_cache
import numpy as np
from px import (Cv, hx, mix, W, H, OUT, vgrad, bayer, text, text_w, seg, ease, ease_out, clamp, darken_flat, grade_mul)
from scenes import buildings, rain, glass_rain
from ui import draw_chat, phone_body, lock_screen, title_card, vcr
from shots import shot, up2, dim_to

ROOM_DIM = 0.6


@lru_cache(maxsize=2)
def _intro_wall():
    c = Cv(W, H, hx('#1f2340'))
    for x in range(0, W, 12):
        c.rect(x, 0, 1, H, hx('#262a4c'))
    c.rect(6, 4, 308, 140, hx('#3a3050'))
    c.rect(0, 146, W, 34, hx('#3a2a26'))  # desk
    c.rect(0, 146, W, 2, hx('#5a4038'))
    for y in range(154, 180, 7):
        c.rect(0, y, W, 1, hx('#33241f'))
    return c


def intro_bg(t, z=0.0, rain_k=1.0):
    c = _intro_wall().copy()
    sub = Cv(300, 134)
    vgrad(sub, 0, 134, [hx('#0b0d20'), hx('#11143a'), hx('#1a1d44'), hx('#262650')])
    buildings(sub, 134, 21, hx('#0f1024'), win=hx('#e8b868'), lit=0.25, x1=300, hmin=20, hmax=70)
    buildings(sub, 134, 22, hx('#161834'), win=hx('#d8a058'), lit=0.2, x1=300, hmin=8, hmax=34)
    rain(sub, t, int(70 * rain_k), 41, speed=220, wind=-40, length=6, col=hx('#4a5a8a'), area=(0, 0, 300, 134))
    c.paste(sub, 10, 8)
    c.rect(10, 74, 300, 2, hx('#3a3050'))
    glass_rain(c, t, 10, 8, 300, 134, seed=21, n=int(30 * rain_k), static=int(160 * rain_k))
    a = darken_flat(c.a, ROOM_DIM)
    a = grade_mul(a, (0.85, 0.9, 1.15))
    c = Cv(arr=a)
    if z > 0:
        sh = int(z * 10)
        left = c.a[:, :160].copy(); right = c.a[:, 160:].copy()
        c.a[:, :160] = np.roll(left, -sh, axis=1); c.a[:, 160:] = np.roll(right, sh, axis=1)
    return c


def phone_geom(z):
    sw = 150 + 2 * int(round(8 * z))
    return (W - sw) // 2, 0, sw, 180


# ---------------------------------------------------------------- I1: the breakup message (present of that night, 2023.12.08)
CHAT_BASE = [dict(k='date', text='2023年12月8日 22:47'), dict(k='me', text='雨好大，\n你带伞了吗？')]
CHAT_NEW = [(0.72, dict(k='her', text='我想了很久')),
            (1.707, dict(k='her', text='他……对我\n很好。')),
            (2.508, dict(k='her', text='示例歌词\n分开吧')),
            (3.17, dict(k='me', text='那我呢？'))]
T_READ = 3.62


def msgs_at(t):
    m = list(CHAT_BASE)
    pop = {}
    for ta, msg in CHAT_NEW:
        if t >= ta:
            m.append(msg)
            pop[len(m) - 1] = (t - ta) / 0.12 if t - ta < 0.12 else 1.0
    return m, pop


@shot('intro_chat')
def intro_chat(t):
    c = intro_bg(t)
    x0, y0, sw, sh = phone_geom(0)
    phone_body(c, x0, y0, sw, sh)
    m, pop = msgs_at(t)
    typing = 1.0 <= t < 1.707 or 2.05 <= t < 2.508
    word = '那我呢？'
    inp = word[:max(0, min(4, int((t - 2.78) / 0.09)))] if 2.78 <= t < 3.17 else ''
    read = len(m) - 1 if t >= T_READ else None
    draw_chat(c, x0, y0, sw, sh, m, 'dark', header='她', typing=typing, t=t, pop=pop, clock='22:51', input_text=inp,
              read_idx=read)
    return c


@shot('title')
def title(t):
    c = Cv(W, H)
    title_card(c, t, 4.226, 5.341)
    return c


# ---------------------------------------------------------------- I3: rewind
REWIND = [
    (6.90, [dict(k='date', text='2022年11月20日'), dict(k='her', text='下雨了☂'), dict(k='pic', pic='umbrella'),
            dict(k='me', text='一把伞\n够两个人')]),
    (7.338, [dict(k='date', text='2022年2月14日'), dict(k='her', text='送你一盒糖♥'), dict(k='pic', pic='candy'),
             dict(k='me', text='盒子我要\n留着装宝贝')]),
    (7.889, [dict(k='date', text='2021年9月1日'), dict(k='her', text='又是同桌！'), dict(k='me', text='序你看完\n了吗'),
             dict(k='her', text='看哭了…')]),
]


@shot('intro_rewind')
def intro_rewind(t):
    c = intro_bg(t)
    c = Cv(arr=grade_mul(c.a, (1.15, 1.0, 0.8)))
    x0, y0, sw, sh = phone_geom(0)
    phone_body(c, x0, y0, sw, sh, col=hx('#2a2420'), edge=hx('#5a4a3a'))
    idx = 0
    for i, (ta, _) in enumerate(REWIND):
        if t >= ta:
            idx = i
    ta, msgs = REWIND[idx]
    p = seg(t, ta, ta + 0.14)
    scroll = -int((1 - ease_out(p)) * 70)
    draw_chat(c, x0, y0, sw, sh, msgs, 'old', header='她', t=t, scroll=scroll, clock='22:51', cursor=False)
    vcr(c, t, label='◀◀ x8', noise=0.7 if p < 1 else 0.3, seed=idx)
    if t > 8.22:
        vcr(c, t, label=None, noise=2.2, seed=99)
    return c


# ---------------------------------------------------------------- I4: landing on 2021.3.13 - the voice message from the bookstore
TRANS = [('示', 8.87),
 ('，', 8.95),
 ('例', 9.17),
 ('一', 9.29),
 ('，', 9.35),
 ('句', 9.53),
 ('歌', 9.59),
 ('词', 9.71),
 ('内', 9.77),
 ('，', 9.83),
 ('容', 9.89),
 ('示', 9.95),
 ('例', 10.01),
 ('一', 10.13),
 ('句', 10.31),
 ('歌', 10.49),
 ('词', 10.61),
 ('内', 10.85),
 ('？', 10.95),
 ('\n', 11.2),
 ('容', 11.39),
 ('示', 11.51),
 ('，', 11.57),
 ('例', 11.69),
 ('一', 11.81),
 ('句', 11.93),
 ('歌', 12.05),
 ('词', 12.23),
 ('内', 12.35),
 ('容', 12.47),
 ('示', 12.65),
 ('例', 12.71),
 ('一', 12.83),
 ('句', 13.07),
 ('歌', 13.19),
 ('词', 13.31),
 ('内', 13.49),
 ('容', 13.61),
 ('示', 13.73),
 ('例', 14.03),
 ('。', 14.1),
 ('\n', 14.2),
 ('一', 14.27),
 ('，', 14.33),
 ('句', 14.45),
 ('歌', 14.57),
 ('。', 14.63),
 ('词', 14.87),
 ('内', 14.99),
 ('。', 15.05)]
TRANS_TEXT = ''.join(ch for ch, _ in TRANS)
VOICE_BASE = [dict(k='date', text='2021年3月12日'), dict(k='sys', text='你们已成为好友'),
              dict(k='her', text='有本书叫\n《半岛铁盒》'), dict(k='her', text='很好看哦'),
              dict(k='date', text='2021年3月13日'), dict(k='me', text='我现在\n去买！')]
T_VOICE = 8.55


@shot('intro_voice')
def intro_voice(t):
    z = ease(seg(t, 8.35, 15.25))
    c = intro_bg(t, z)
    c = Cv(arr=grade_mul(c.a, (1.15, 1.0, 0.8)))
    x0, y0, sw, sh = phone_geom(z)
    phone_body(c, x0, y0, sw, sh, col=hx('#2a2420'), edge=hx('#5a4a3a'))
    m = list(VOICE_BASE)
    pop = {}
    if t >= T_VOICE:
        n = sum(1 for ch, tc in TRANS if t + 0.04 >= tc)
        m.append(dict(k='voice', dur='0:06', me=True, trans=TRANS_TEXT, trans_n=n))
        if t - T_VOICE < 0.12:
            pop[len(m) - 1] = (t - T_VOICE) / 0.12
    vp = seg(t, 8.87, 15.1) if 8.8 < t < 15.12 else None
    draw_chat(c, x0, y0, sw, sh, m, 'old', header='她', t=t, pop=pop, clock='16:20', cursor=False, voice_p=vp)
    vcr(c, t, label=None, stamp='2021.03.13')
    if t < 8.45:
        vcr(c, t, label=None, noise=2.0, seed=7)
    return c


# ---------------------------------------------------------------- I5: back to now - screen off, lock screen with a 3-year-old notification
NOTE = [('她 · 3年前', '示例歌词分开吧')]


@shot('intro_lock')
def intro_lock(t):
    if t < 15.31:  # glitch out of the past
        c = intro_bg(t)
        x0, y0, sw, sh = phone_geom(1.0)
        phone_body(c, x0, y0, sw, sh)
        c.rect(x0, y0, sw, sh, (5, 5, 8))
        vcr(c, t, label=None, noise=2.5, seed=5)
        return c
    lvl = 0 if t < 16.45 else 1
    if lvl == 0:
        c = intro_bg(t)
        x0, y0, sw, sh = phone_geom(0)
        phone_body(c, x0, y0, sw, sh)
        if t < 15.85:
            c.rect(x0, y0, sw, sh, (5, 5, 8))
            # faint reflection of the rainy window on the black glass
            r = np.random.default_rng(3)
            for i in range(30):
                c.px(x0 + r.integers(0, sw), y0 + r.integers(0, sh), (22, 24, 40))
        else:
            np_ = seg(t, 16.0, 16.22)
            lock_screen(c, x0, y0, sw, sh, t, notes=NOTE, note_p=np_, dim=1 - seg(t, 15.85, 15.98))
    else:
        big = Cv(196, 180)
        lock_screen(big, 0, 0, 196, 180, t, notes=NOTE, note_p=1.0)
        crop = Cv(arr=big.a[18:108, 18:178].copy())
        c = up2(crop)
        if t < 16.45 + 0.09:
            c.a[:] = (255, 255, 255)
    return c
