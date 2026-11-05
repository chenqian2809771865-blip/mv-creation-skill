# -*- coding: utf-8 -*-
"""Close-up props for 《半岛铁盒》: the book, the candy tin (new / rusty), candy jar, polaroids, mini pictures."""
import math
from functools import lru_cache
import numpy as np
from px import Cv, hx, mix, bayer, text, text_w, OUT, clamp, ease, ease_out, vgrad, upscale
from ui_tiny import tiny

TEAL, TEAL_LT, TEAL_DK = hx('#2e7f8a'), hx('#56a8ae'), hx('#1c5660')
LIDRED, LIDRED_DK = hx('#c83a36'), hx('#8e2428')
CREAM = hx('#f4ead6')
BRASS, BRASS_LT, BRASS_DK = hx('#c8a040'), hx('#f0d070'), hx('#7a5a1c')
RUST = [hx('#5a2a1a'), hx('#7a3a22'), hx('#a4542a'), hx('#c87a3a')]
CANDY = [hx('#e84a5f'), hx('#f6c040'), hx('#5ab0e0'), hx('#7ac060'), hx('#f08ac0'), hx('#ffffff')]


def candy_px(c, x, y, col, big=False):
    """wrapped candy: body + twisted ends."""
    if big:
        c.ellipse(x, y, 3.2, 2.4, col)
        c.poly([(x - 3, y), (x - 7, y - 3), (x - 7, y + 3)], mix(col, (255, 255, 255), 0.3))
        c.poly([(x + 3, y), (x + 7, y - 3), (x + 7, y + 3)], mix(col, (255, 255, 255), 0.3))
        c.px(x - 1, y - 1, (255, 255, 255))
    else:
        c.rect(x - 1, y - 1, 3, 2, col)
        c.px(x - 2, y - 2, col); c.px(x - 2, y + 1, col); c.px(x + 2, y - 2, col); c.px(x + 2, y + 1, col)


# ---------------------------------------------------------------- the tin (close-up on a 160x90 canvas)
@lru_cache(maxsize=8)
def _rust_noise(w, h, seed):
    from PIL import Image
    r = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    for cell, amp in ((9, 1.0), (4, 0.45), (2, 0.18)):
        g = r.random((h // cell + 2, w // cell + 2)).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize(((w // cell + 2) * cell, (h // cell + 2) * cell), Image.BILINEAR)
        acc += np.array(im, np.float32)[:h, :w] / 255 * amp
    acc /= 1.63
    yy, xx = np.mgrid[0:h, 0:w]
    edge = np.minimum.reduce([xx, yy, w - 1 - xx, h - 1 - yy]).astype(np.float32)
    return acc - np.clip(1 - edge / 8, 0, 1) * 0.3


def tin(c, x, y, w=80, h=32, lid=10, rust=0.0, dusty=0.0, open_=0.0, seed=3, lit=None, keyhole=True, label=True):
    """candy tin front view. (x,y)= top-left of the body (lid sits above). open_ 0..1 lifts the lid."""
    x, y = int(x), int(y)
    body = Cv(w, h, TEAL)
    body.rect(0, 0, w, 2, TEAL_LT); body.rect(0, h - 3, w, 3, TEAL_DK); body.rect(w - 3, 0, 3, h, TEAL_DK)
    body.rect(0, 2, 2, h - 5, TEAL_LT)
    if label:
        lw, lh = int(w * 0.5), int(h * 0.55)
        lx, ly = (w - lw) // 2, (h - lh) // 2 + 1
        body.rect(lx + 1, ly, lw - 2, lh, CREAM); body.rect(lx, ly + 1, lw, lh - 2, CREAM)
        body.rect(lx + 1, ly + lh - 1, lw - 2, 1, mix(CREAM, (0, 0, 0), 0.2))
        for i, col in enumerate(CANDY[:5]):
            candy_px(body, lx + 5 + i * (lw - 10) / 4, ly + lh // 2, col)
    lidc = Cv(w + 4, lid, LIDRED)
    lidc.rect(0, 0, w + 4, 2, mix(LIDRED, (255, 255, 255), 0.25)); lidc.rect(0, lid - 2, w + 4, 2, LIDRED_DK)
    for i in range(6, w, 9):
        lidc.rect(i, 3 + (i // 9) % 2 * 2, 2, 2, CREAM)
    if rust > 0:
        for cv_, sd in ((body, seed), (lidc, seed + 1)):
            nz = _rust_noise(cv_.w, cv_.h, sd)
            th = 0.12 + rust * 0.62
            m = nz < th
            lvl = np.clip(((th - nz) / 0.12 * 1.0), 0, 3).astype(int)
            pal = np.array(RUST, np.uint8)
            cv_.a[m] = pal[3 - lvl[m]]
    if dusty > 0:
        nzd = _rust_noise(lidc.w, lidc.h, seed + 9)
        m = (nzd > 0.62 - dusty * 0.25) | (np.arange(lidc.h)[:, None] < 2) & (bayer(lidc.h, lidc.w) < dusty * 0.7)
        lidc.a[m] = (lidc.a[m].astype(np.float32) * 0.35 + np.array([176, 172, 164]) * 0.65).astype(np.uint8)
        nzb = _rust_noise(body.w, body.h, seed + 11)
        m = nzb > 0.72 - dusty * 0.12
        body.a[m] = (body.a[m].astype(np.float32) * 0.55 + np.array([150, 148, 140]) * 0.45).astype(np.uint8)
    if keyhole:
        kx = w // 2 - 4
        body.rect(kx, 1, 8, 10, BRASS); body.rect(kx, 1, 8, 1, BRASS_LT); body.rect(kx + 7, 1, 1, 10, BRASS_DK)
        if rust > 0.3:
            body.px(kx + 1, 8, RUST[2]); body.px(kx + 6, 3, RUST[1])
        body.rect(kx + 3, 3, 2, 2, (12, 10, 14)); body.rect(kx + 3, 5, 2, 3, (12, 10, 14))
        body.px(kx + 2, 7, (12, 10, 14)); body.px(kx + 5, 7, (12, 10, 14))
    if lit is not None:
        body.a[:] = np.clip(body.a.astype(np.float32) * np.array(lit), 0, 255).astype(np.uint8)
        lidc.a[:] = np.clip(lidc.a.astype(np.float32) * np.array(lit), 0, 255).astype(np.uint8)
    c.paste(body, x, y)
    c.rect(x - 1, y, 1, h, OUT); c.rect(x + w, y, 1, h, OUT); c.rect(x, y + h, w, 1, OUT)
    ly_ = y - lid - int(open_ * 14)
    c.paste(lidc, x - 2, ly_)
    c.rect(x - 2, ly_ - 1, w + 4, 1, OUT); c.rect(x - 3, ly_, 1, lid, OUT); c.rect(x + w + 2, ly_, 1, lid, OUT)
    c.rect(x - 2, ly_ + lid, w + 4, 1, OUT)
    return (x + w // 2, y + 6)  # keyhole center


def tin_small(c, x, y, rust=0.0, dusty=0.0, s=1):
    """small tin for wide shots: (x,y)=bottom-center. about 16x9."""
    w, h = 16 * s, 6 * s
    x0, y0 = int(x - w // 2), int(y - h)
    c.rect(x0, y0, w, h, TEAL); c.rect(x0, y0 + h - 1, w, 1, TEAL_DK)
    c.rect(x0 - 1, y0 - 3 * s, w + 2, 3 * s, LIDRED); c.rect(x0 - 1, y0 - 1, w + 2, 1, LIDRED_DK)
    c.rect(x0 + w // 2 - 1, y0, 2, 2, BRASS)
    if rust > 0:
        r = np.random.default_rng(5)
        for i in range(int(rust * 14)):
            c.px(x0 + r.integers(0, w), y0 - 3 * s + r.integers(0, h + 3 * s), RUST[int(r.integers(1, 4))])
    if dusty > 0:
        m = Cv(w + 2, 2)
        for i in range(0, w + 2, 2):
            c.px(x0 - 1 + i, y0 - 3 * s, hx('#b8b4aa'))
    c.rect(x0 - 2, y0 - 3 * s, 1, h + 3 * s, OUT); c.rect(x0 + w + 1, y0 - 3 * s, 1, h + 3 * s, OUT)
    c.rect(x0 - 1, y0 - 3 * s - 1, w + 2, 1, OUT); c.rect(x0 - 1, y0 + h, w + 2, 1, OUT)


# ---------------------------------------------------------------- the book
BOOK_COVER = hx('#2a5a6a')


def book_cover(c, x, y, w=66, h=84, lit_chars=4, price=True, glow=0.0, worn=0.0):
    """《半岛铁盒》 cover, portrait. (x,y)=top-left. lit_chars: how many title chars are shown (sung)."""
    x, y = int(x), int(y)
    b = Cv(w, h)
    vgrad(b, 0, h, [hx('#1e3a5a'), hx('#2a5a7a'), hx('#3a7a8e'), hx('#5aa0a6')])
    # sea line + peninsula
    b.rect(0, int(h * 0.62), w, int(h * 0.38), hx('#2e6a86'))
    for yy in range(int(h * 0.64), h, 4):
        for xx in range((yy * 7) % 6, w, 9):
            b.rect(xx, yy, 3, 1, hx('#4a8aa2'))
    b.poly([(0, h * 0.56), (w * 0.35, h * 0.58), (w * 0.62, h * 0.63), (w * 0.66, h * 0.67), (w * 0.4, h * 0.7), (0, h * 0.72)], hx('#e6c890'))
    b.poly([(0, h * 0.58), (w * 0.3, h * 0.6), (w * 0.5, h * 0.64), (w * 0.3, h * 0.67), (0, h * 0.69)], hx('#c8a46a'))
    # a little tin on the peninsula + a tree
    tx, ty = int(w * 0.36), int(h * 0.585)
    b.rect(tx, ty - 3, 7, 4, hx('#c83a36')); b.rect(tx, ty - 4, 7, 1, hx('#f4ead6')); b.px(tx + 3, ty - 2, hx('#f0d070'))
    b.rect(int(w * 0.15), int(h * 0.47), 1, 6, hx('#3a2a22'))
    b.ellipse(w * 0.15, h * 0.45, 4, 3.5, hx('#3e7a44')); b.ellipse(w * 0.13, h * 0.44, 2, 2, hx('#5a9a4c'))
    # moon / stars
    b.ellipse(w * 0.2, h * 0.18, 4, 4, hx('#f6ecc8')); b.ellipse(w * 0.22, h * 0.16, 3.4, 3.4, hx('#2a4a6a'))
    for (sx, sy) in ((0.08, 0.3), (0.32, 0.1), (0.44, 0.3), (0.12, 0.08), (0.5, 0.18)):
        b.px(w * sx, h * sy, hx('#f6ecc8'))
    # vertical title strip on the right
    sx0 = w - 22
    b.rect(sx0, 4, 18, 70, hx('#f4ead6')); b.rect(sx0, 4, 18, 1, hx('#ffffff')); b.rect(sx0 + 17, 4, 1, 70, hx('#c8b898'))
    for i, ch in enumerate('半岛铁盒'):
        if i < lit_chars:
            text(b, sx0 + 1, 5 + i * 17, ch, hx('#1e2a3a'))
    # author line
    text(b, 4, h - 13, '着', hx('#f4ead6'), font='w') if False else None
    # spine shading
    b.rect(0, 0, 3, h, mix(BOOK_COVER, (0, 0, 0), 0.35)); b.rect(3, 0, 1, h, mix(BOOK_COVER, (255, 255, 255), 0.2))
    if price:
        b.rect(5, h - 10, 16, 7, hx('#f6f2e8')); b.rect(5, h - 10, 16, 1, hx('#e84a5f'))
        tiny(b, 6, h - 8, '28.0', hx('#3a3030'))
    if worn > 0:
        m = bayer(h, w, 2, 1) < worn * 0.4
        b.a[m] = (b.a[m].astype(np.float32) * 0.6 + np.array([200, 190, 170]) * 0.4).astype(np.uint8)
    c.paste(b, x, y)
    c.rect(x - 1, y, 1, h, OUT); c.rect(x + w, y, 1, h, OUT); c.rect(x, y - 1, w, 1, OUT); c.rect(x, y + h, w, 1, OUT)
    c.rect(x + w + 1, y + 1, 2, h, mix(BOOK_COVER, (0, 0, 0), 0.5))  # page block edge
    c.rect(x + 2, y + h + 1, w, 2, hx('#e8e0cc'))
    if glow > 0:
        for i in range(int(glow * 12)):
            a = i / 12 * 2 * math.pi + glow * 3
            c.px(x + w / 2 + math.cos(a) * (w * 0.7), y + h / 2 + math.sin(a) * (h * 0.6), hx('#fff4c8'))


PAGE, PAGE_DK, INK = hx('#f6efdc'), hx('#d8ccb0'), hx('#7a7060')


def page_lines(c, x, y, w, h, seed, n=None, col=INK, start=0, gap=6):
    r = np.random.default_rng(seed)
    rows = list(range(y, y + h, gap))
    for k, yy in enumerate(rows[start:n]):
        ln = int(w * r.uniform(0.6, 1.0)) if k % 5 != 4 else int(w * r.uniform(0.2, 0.5))
        xx = x
        while xx < x + ln:
            seg_ = int(r.integers(2, 6))
            c.rect(xx, yy, min(seg_, x + ln - xx), 1, col)
            xx += seg_ + 1


def open_book(c, x, y, pw=58, ph=70, left=None, right=None, flip=None, warm=True):
    """open book, spine at x. left/right: dict(num=, title=, lines=seed). flip: 0..1 page turning right->left."""
    x, y = int(x), int(y)
    shadow = hx('#5a4a3a')
    c.rect(x - pw - 3, y + 3, pw * 2 + 6, ph, shadow)
    for side, info in ((-1, left), (1, right)):
        x0 = x - pw if side < 0 else x
        c.rect(x0, y, pw, ph, PAGE)
        c.rect(x0 + (pw - 4 if side < 0 else 0), y, 4, ph, PAGE_DK)
        if side < 0:
            c.rect(x0 - 2, y + 2, 2, ph - 1, PAGE_DK); c.rect(x0 - 3, y + 3, 1, ph - 2, hx('#c8bc9c'))
        else:
            c.rect(x0 + pw, y + 2, 2, ph - 1, PAGE_DK); c.rect(x0 + pw + 2, y + 3, 1, ph - 2, hx('#c8bc9c'))
        if info:
            ty = y + 6
            if info.get('title'):
                f_ = 'u' if text_w(info['title']) <= pw - 6 else 'w'
                tw = text_w(info['title'], f_)
                text(c, x0 + (pw - tw) // 2, y + 4, info['title'], info.get('tcol', hx('#3a3028')), font=f_)
                ty = y + 24
            if info.get('lines') is not None:
                page_lines(c, x0 + 6, ty, pw - 12, y + ph - 12 - ty, info['lines'], col=info.get('lcol', INK))
            if info.get('num') is not None:
                s = str(info['num'])
                tiny(c, (x0 + 4) if side < 0 else (x0 + pw - 4 - 4 * len(s)), y + ph - 7, s, hx('#5a5040'))
    c.rect(x - 1, y, 2, ph, hx('#b8aa8a'))
    if flip is not None and 0 < flip < 1:
        f = ease(flip)
        # page attached at spine, its free edge moves from right (x+pw) to left (x-pw)
        ex = x + pw * math.cos(f * math.pi)
        lift = math.sin(f * math.pi) * 10
        pts = [(x, y), (ex, y - lift), (ex, y + ph - lift * 0.4), (x, y + ph)]
        c.poly(pts, mix(PAGE, (255, 255, 255), 0.3) if f < 0.5 else PAGE)
        c.line(ex, y - lift, ex, y + ph - lift * 0.4, PAGE_DK)
        c.line(x, y, ex, y - lift, PAGE_DK)


# ---------------------------------------------------------------- candy jar (close-up)
def candy_jar(c, x, y, w=40, h=46, fill=0.8, t=0.0, key=False, empty=False):
    """glass jar, (x,y)=bottom-left."""
    x, y = int(x), int(y)
    glass, glass_lt, glass_dk = hx('#bcd8e4'), hx('#eaf6fa'), hx('#88aabc')
    top = y - h
    # contents
    if not empty:
        r = np.random.default_rng(11)
        lvl = int(h * fill)
        for i in range(int(w * lvl / 9)):
            cx = x + 4 + r.uniform(0, w - 8); cy = y - 4 - r.uniform(0, lvl - 6)
            candy_px(c, cx, cy, CANDY[int(r.integers(0, 5))])
    if key:
        kx, ky = x + w // 2 - 4, y - 6
        c.ellipse(kx, ky, 2.5, 2.5, BRASS); c.px(kx, ky, (40, 30, 20)); c.rect(kx + 2, ky - 1, 7, 2, BRASS)
        c.rect(kx + 6, ky + 1, 1, 2, BRASS); c.rect(kx + 8, ky + 1, 1, 2, BRASS)
    # glass body (outline + highlights, leave the inside see-through)
    c.rect(x, top + 6, 1, h - 6, glass_dk); c.rect(x + w - 1, top + 6, 1, h - 6, glass_dk)
    c.rect(x + 1, y - 1, w - 2, 1, glass_dk)
    c.rect(x + 3, top + 9, 1, h - 16, glass_lt); c.rect(x + 4, top + 9, 1, 8, glass_lt)
    c.rect(x + w - 5, top + 12, 1, h - 22, glass)
    c.rect(x + 3, top + 4, w - 6, 3, glass); c.rect(x + 2, top + 6, w - 4, 1, glass_dk)
    # lid
    c.rect(x + 2, top - 2, w - 4, 6, hx('#e0b050')); c.rect(x + 2, top - 2, w - 4, 1, hx('#f6d070')); c.rect(x + 2, top + 3, w - 4, 1, hx('#a07828'))
    c.rect(x + 1, top - 3, w - 2, 1, OUT); c.rect(x + 1, top - 2, 1, 6, OUT); c.rect(x + w - 2, top - 2, 1, 6, OUT)


# ---------------------------------------------------------------- mini pictures (for polaroids, chat images, wall photo)
def mini_pic(kind, w, h, t=0.0):
    p = Cv(w, h)
    if kind == 'umbrella':  # the two under her red umbrella at night
        vgrad(p, 0, h, [hx('#141a34'), hx('#22284a'), hx('#34365a')])
        r = np.random.default_rng(2)
        for i in range(int(w * h / 40)):
            p.px(r.integers(0, w), r.integers(0, h), hx('#5a6a9a'))
        for i in range(5):
            p.ellipse(r.uniform(0, w), r.uniform(0, h * 0.6), 2 + w / 20, 2 + w / 20, hx('#e8b868'))
        p.rect(0, int(h * 0.8), w, h, hx('#2a2a3e'))
        cx = w // 2
        s = max(1, w // 20)
        p.ellipse(cx, h * 0.38, w * 0.3, h * 0.16, hx('#cc3b42')); p.rect(0, int(h * 0.38), w, int(h * 0.2), hx('#22284a')) if False else None
        p.rect(int(cx - w * 0.3), int(h * 0.38), int(w * 0.6) + 1, 1, hx('#972a35'))
        p.rect(cx, int(h * 0.38), 1, int(h * 0.15), hx('#3a3440'))
        # two little figures
        for (fx, hair, top) in ((cx - w * 0.13, hx('#2c2536'), hx('#3b5b98')), (cx + w * 0.05, hx('#6b3d2b'), hx('#efe4cb'))):
            fw = max(2, int(w * 0.1))
            p.rect(fx, h * 0.5, fw, fw, hx('#f4cbaa')); p.rect(fx, h * 0.5, fw, max(1, fw // 2), hair)
            p.rect(fx, h * 0.5 + fw, fw, int(h * 0.25), top)
            if hair == hx('#6b3d2b'):
                p.rect(fx, h * 0.5 + fw, fw, max(1, fw // 3), hx('#cc3b42'))
    elif kind == 'book':  # the book on the shelf / cover
        p.a[:] = hx('#e8dcc0')
        p.rect(0, int(h * 0.7), w, int(h * 0.3) + 1, hx('#8a5a3a'))
        bw, bh = int(w * 0.45), int(h * 0.62)
        bx, by = (w - bw) // 2, int(h * 0.7) - bh
        p.rect(bx, by, bw, bh, hx('#2a5a7a')); p.rect(bx, by + int(bh * 0.62), bw, int(bh * 0.38), hx('#3a7a8e'))
        p.rect(bx + bw - max(2, bw // 4) - 1, by + 1, max(2, bw // 4), bh - 2, hx('#f4ead6'))
        p.rect(bx + 1, by + int(bh * 0.55), int(bw * 0.5), max(1, bh // 10), hx('#e6c890'))
    elif kind == 'candy':  # the candy tin (new) full of candy
        p.a[:] = hx('#f6e0c0')
        tw_, th_ = int(w * 0.7), int(h * 0.45)
        tx, ty = (w - tw_) // 2, int(h * 0.42)
        p.rect(tx, ty, tw_, th_, TEAL); p.rect(tx, ty + th_ - 1, tw_, 1, TEAL_DK)
        p.rect(tx - 1, ty - max(2, h // 8), tw_ + 2, max(2, h // 8), LIDRED)
        r = np.random.default_rng(4)
        for i in range(6):
            p.px(tx + r.integers(1, tw_ - 1), ty - max(2, h // 8) - 1 - r.integers(0, 3), CANDY[i % 5])
        p.px(w // 2, ty + 1, BRASS)
    elif kind == 'read':  # two reading on the floor (warm)
        vgrad(p, 0, h, [hx('#f6d8a0'), hx('#f0c088'), hx('#d89a68')])
        p.rect(0, int(h * 0.7), w, h, hx('#b8865a'))
        for (fx, hair, top) in ((w * 0.3, hx('#2c2536'), hx('#3b5b98')), (w * 0.55, hx('#6b3d2b'), hx('#efe4cb'))):
            fw = max(2, int(w * 0.12))
            p.rect(fx, h * 0.38, fw, fw, hx('#f4cbaa')); p.rect(fx, h * 0.38, fw, max(1, fw // 2), hair)
            p.rect(fx, h * 0.38 + fw, fw, int(h * 0.3), top)
        p.rect(int(w * 0.42), int(h * 0.62), int(w * 0.18), max(1, h // 12), hx('#2a5a7a'))
    elif kind == 'store':  # bookstore shelves
        p.a[:] = hx('#f2e2c0')
        for k in range(3):
            yy = int(h * (0.15 + k * 0.3))
            p.rect(0, yy + int(h * 0.22), w, max(1, h // 18), hx('#8a5a3a'))
            book_strip(p, 1, yy, w - 2, int(h * 0.22), seed=k + 3)
    elif kind == 'roof':  # rooftop sunset, sharing earphones
        vgrad(p, 0, h, [hx('#f08a5a'), hx('#f6b070'), hx('#fde0a0')])
        p.ellipse(w * 0.7, h * 0.55, w * 0.12, w * 0.12, hx('#fff0c0'))
        p.rect(0, int(h * 0.72), w, h, hx('#6a4a5a'))
        for (fx, hair) in ((w * 0.3, hx('#2c2536')), (w * 0.48, hx('#6b3d2b'))):
            fw = max(2, int(w * 0.12))
            p.rect(fx, h * 0.48, fw, fw, hair); p.rect(fx, h * 0.48 + fw, fw, int(h * 0.25), hx('#3a2a3a'))
    return p


def book_strip(c, x, y, w, h, seed=1):
    r = np.random.default_rng(seed)
    pal = [hx('#c84a3a'), hx('#3a7a8a'), hx('#e0b050'), hx('#5a6aa8'), hx('#7a9a5a'), hx('#8a4a6a'), hx('#d8d0c0')]
    xx = x
    while xx < x + w:
        bw = int(r.integers(2, 5)); bh = int(h - r.integers(0, max(1, h // 4)))
        c.rect(xx, y + h - bh, min(bw, x + w - xx), bh, pal[int(r.integers(0, len(pal)))])
        xx += bw


def polaroid(c, x, y, kind, w=26, h=30, rot=0, alpha=1.0, burn=0.0, t=0.0, yellow=0.0):
    """white-framed photo centered at (x,y)."""
    pw, ph = w - 4, h - 9
    p = Cv(w, h, (250, 248, 240))
    p.rect(0, h - 1, w, 1, hx('#c8c4b8')); p.rect(w - 1, 0, 1, h, hx('#d8d4c8'))
    pic = mini_pic(kind, pw, ph, t)
    if yellow > 0:
        pic.a[:] = np.clip(pic.a.astype(np.float32) * (1 - 0.45 * yellow) + np.array([230, 190, 120]) * 0.45 * yellow, 0, 255).astype(np.uint8)
        p.a[:] = np.clip(p.a.astype(np.float32) * (1 - 0.3 * yellow) + np.array([220, 196, 140]) * 0.3 * yellow, 0, 255).astype(np.uint8)
    p.paste(pic, 2, 2)
    a = np.zeros((h, w, 4), np.uint8)
    a[..., :3] = p.a; a[..., 3] = 255
    if burn > 0:  # crumble from a corner into dust
        yy, xx = np.mgrid[0:h, 0:w]
        d = (xx / w + yy / h) / 2 + (np.random.default_rng(int(x * 7 + y)).random((h, w)) - 0.5) * 0.25
        gone = d < burn * 1.3 - 0.15
        edge = (d < burn * 1.3 - 0.05) & ~gone
        a[gone, 3] = 0
        a[edge, :3] = (120, 110, 100)
    spr = Cv(arr=a)
    if rot:
        from PIL import Image
        im = Image.fromarray(a, 'RGBA').rotate(rot, resample=Image.NEAREST, expand=True)
        spr = Cv(arr=np.array(im))
    c.blit(spr, x - spr.w // 2, y - spr.h // 2, alpha_mul=alpha)
