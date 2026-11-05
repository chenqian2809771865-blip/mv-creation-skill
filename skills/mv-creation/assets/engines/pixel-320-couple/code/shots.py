# -*- coding: utf-8 -*-
"""Shot registry + shared helpers for 《晴天》. Each shot takes visual time t (song seconds) -> Cv 320x180 RGB.
Shot bodies live in shots_intro.py / shots_verse.py / shots_chorus.py and register through @shot."""
import math
import numpy as np
from px import (Cv, hx, mix, W, H, OUT, vgrad, bayer, text, text_w, upscale, seg, ease, ease_out, ease_in, clamp,
                grade_warm, grade_ice, vignette, light, silhouette, dither_blend, darken_flat, grade_mul, outline, lum)
from chars import P
from ui import vcr

IMPL = {}


def shot(name):
    def deco(f):
        IMPL[name] = f
        return f
    return deco


def up2(c):
    return Cv(arr=upscale(c.a, 2))


def upk(c, cx, cy, k):
    """integer zoom k around (cx, cy) of a 320x180 (or smaller) canvas -> 320x180."""
    cw, ch = int(math.ceil(W / k)), int(math.ceil(H / k))
    x0 = int(clamp(cx - cw / 2, 0, c.w - cw)); y0 = int(clamp(cy - ch / 2, 0, c.h - ch))
    a = upscale(c.a[y0:y0 + ch, x0:x0 + cw], k)[:H, :W]
    return Cv(arr=np.ascontiguousarray(a))


def lit(spr, mode):
    keep = [P['she']['scarf'], P['she']['scarf_dk']]
    if mode == 'night':
        return light(spr, (0.62, 0.66, 0.92), rim=(150, 170, 235), rim_side=-1, rim_k=0.45, keep=keep)
    if mode == 'dark':
        return light(spr, (0.42, 0.45, 0.68), rim=(120, 140, 210), rim_side=-1, rim_k=0.4)
    if mode == 'corridor':
        return light(spr, (0.92, 0.92, 0.96), rim=(255, 246, 220), rim_side=1, rim_k=0.2)
    if mode == 'day':
        return light(spr, (1.0, 0.97, 0.92), rim=(255, 236, 190), rim_side=-1, rim_k=0.35)
    if mode == 'lamp':
        return light(spr, (0.8, 0.74, 0.8), rim=(255, 200, 130), rim_side=-1, rim_k=0.5)
    if mode == 'torch':
        return light(spr, (0.55, 0.56, 0.75), rim=(255, 236, 190), rim_side=1, rim_k=0.55)
    if mode == 'rain':
        return light(spr, (0.8, 0.82, 0.95), rim=(200, 210, 250), rim_side=1, rim_k=0.3)
    if mode == 'sunset':
        return light(spr, (0.92, 0.8, 0.78), rim=(255, 190, 120), rim_side=1, rim_k=0.55)
    if mode == 'dawn':
        return light(spr, (0.9, 0.84, 0.86), rim=(255, 206, 150), rim_side=-1, rim_k=0.5)
    return spr


def memory_post(c, t, stamp='2021.03.13', k=0.34, dust_n=10, vig=0.7):
    a = grade_warm(c.a, k)
    a = vignette(a, vig, col=(52, 26, 22))
    c = Cv(arr=a)
    if dust_n:
        r = np.random.default_rng(int(t * 12))
        for i in range(dust_n):
            c.px(r.integers(0, W), r.integers(0, H), (255, 236, 200) if i % 3 else (90, 50, 40))
    if stamp:
        vcr(c, t, label=None, stamp=stamp)
    return c


def ice_post(c, t, stamp='2023.12.08', vig=0.6):
    a = grade_ice(c.a)
    a = vignette(a, vig, col=(14, 18, 34))
    c = Cv(arr=a)
    if stamp:
        vcr(c, t, label=None, stamp=stamp)
    return c


def strip_mix(a, b, p, seed=3, sw=8):
    r = np.random.default_rng(seed)
    n = W // sw + 1
    th = r.uniform(0.15, 0.85, n)
    out = a.copy()
    for i in range(n):
        x0, x1 = i * sw, min(W, (i + 1) * sw)
        if p >= th[i]:
            out[:, x0:x1] = b[:, x0:x1]
        else:
            d = int((1 - (th[i] - p) / th[i]) * 20 * (1 if i % 2 else -1))
            out[:, x0:x1] = np.roll(a[:, x0:x1], d, axis=0)
    return out


def bokeh_bg(c, t, mode='mem', seed=5, n=14):
    if mode == 'mem':
        vgrad(c, 0, c.h, [hx('#8cc4e6'), hx('#b8dcea'), hx('#f2e6c8'), hx('#f0c888')])
        cols = [hx('#f6d08a'), hx('#fbe6b0'), hx('#e8a868')]
    elif mode == 'pink':
        vgrad(c, 0, c.h, [hx('#f6c8c0'), hx('#f8dccc'), hx('#fbe8d0'), hx('#f6d0a8')])
        cols = [hx('#fff0d8'), hx('#f8b8b0'), hx('#f6d890')]
    elif mode == 'store':
        vgrad(c, 0, c.h, [hx('#6a4a3a'), hx('#8a6044'), hx('#b8865a'), hx('#e0b07a')])
        cols = [hx('#c84a3a'), hx('#3a7a8a'), hx('#e0b050'), hx('#5a6aa8'), hx('#f6d08a')]
    elif mode == 'rain':
        vgrad(c, 0, c.h, [hx('#1a2038'), hx('#26304e'), hx('#3a4566'), hx('#56607e')])
        cols = [hx('#ffd68a'), hx('#e8b868'), hx('#6a7aa4')]
    else:  # night room
        vgrad(c, 0, c.h, [hx('#0b0c1c'), hx('#121430'), hx('#1b1d3e'), hx('#262650')])
        cols = [hx('#2a3060'), hx('#e8b868'), hx('#3a3a6a')]
    r = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:c.h, 0:c.w]
    for i in range(n):
        x = r.uniform(0, c.w) + math.sin(t * 0.3 + i) * 3
        y = r.uniform(0, c.h * 0.8)
        rad = r.uniform(8, 24) * c.w / 320
        m = ((xx - x) ** 2 + (yy - y) ** 2 <= rad * rad) & (bayer(c.h, c.w) < 0.5)
        c.a[m] = cols[i % len(cols)]


def flash_at(c, t, t0, n=2):
    if t0 <= t < t0 + n / 24.0:
        c.a[:] = (255, 255, 255)
    return c


def dim_to(c, f, col=(0, 0, 0)):
    if f > 0:
        m = bayer(c.h, c.w) < f
        c.a[m] = col
    return c


def rain_shadows(c, t, x0, x1, y0, y1, seed=3, k=0.35, col=(150, 170, 235)):
    """moving vertical streaks of window light (rain running down the glass casts shadows on a face/wall)."""
    r = np.random.default_rng(seed)
    for i in range(14):
        x = int(r.uniform(x0, x1)); sp = r.uniform(8, 22); ln = int(r.uniform(10, 40))
        y = int((r.uniform(0, 200) + t * sp) % (y1 - y0 + ln)) + y0 - ln
        for yy in range(max(y0, y), min(y1, y + ln)):
            if 0 <= x < c.w and 0 <= yy < c.h and (yy + x) % 2 == 0:
                c.a[yy, x] = np.clip(c.a[yy, x].astype(np.float32) * (1 - k) + np.array(col) * k, 0, 255).astype(np.uint8)



import shots_open  # noqa: E402,F401
import shots_full  # noqa: E402,F401
