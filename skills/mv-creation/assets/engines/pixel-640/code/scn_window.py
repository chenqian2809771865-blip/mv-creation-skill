# -*- coding: utf-8 -*-
"""Window close-ups. Warm lamp inside / cool neon city outside. Layers: clear outside, fog alpha, soft glow, frame RGBA."""
import numpy as np, math, functools
from core import *

SKY_N = [C('#17152e'), C('#1e1a3a'), C('#272146'), C('#322852'), C('#40305c'), C('#523a66'), C('#6a466e')]


def city_outside(seed=11, w=W, h=H, horizon=230, sky=SKY_N, neon=True, win_rate=0.30):
    img = new(sky[0], w, h)
    vgrad_bands(img, 0, horizon + 20, sky[0], sky[-1], len(sky))
    img[horizon + 20:] = sky[-1]
    im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    rng = np.random.default_rng(seed)
    far = (52, 40, 80)
    x = -10
    fars = []
    while x < w:
        bw = int(rng.integers(24, 64)); bh = int(rng.integers(50, 140))
        d.rectangle([x, horizon - bh, x + bw, h], fill=far)
        fars.append((x, horizon - bh, bw))
        if rng.random() < 0.35:
            d.rectangle([x + bw // 2 - 1, horizon - bh - 16, x + bw // 2, horizon - bh], fill=far)
        x += bw + int(rng.integers(-6, 4))
    mid = (24, 20, 42)
    x = -20
    mids = []
    while x < w:
        bw = int(rng.integers(56, 120)); bh = int(rng.integers(10, 80))
        top = horizon - bh + 50
        d.rectangle([x, top, x + bw, h], fill=mid)
        d.rectangle([x, top, x + bw, top + 1], fill=(64, 50, 92))
        mids.append((x, top, bw))
        x += bw + int(rng.integers(4, 18))
    img = np.asarray(im, np.float32).copy()
    for (bx, top, bw) in fars:
        for yy in range(top + 5, horizon + 10, 7):
            for xx in range(bx + 3, bx + bw - 3, 5):
                if rng.random() < 0.12:
                    img[yy:yy + 2, xx:xx + 2] = (150, 120, 120) if rng.random() < 0.6 else (110, 130, 160)
    for (bx, top, bw) in mids:
        for yy in range(top + 7, h - 8, 12):
            for xx in range(bx + 6, bx + bw - 6, 10):
                r = rng.random()
                if r < win_rate:
                    c = C('#f0b26c') if rng.random() < 0.65 else C('#9fd2e0')
                    img[yy:yy + 5, xx:xx + 4] = c * (0.6 + 0.35 * rng.random())
                    img[yy + 4, xx:xx + 4] *= 0.75
    if neon:
        # a vertical neon sign
        nx, ny = int(w * 0.72), horizon - 20
        img[ny:ny + 46, nx:nx + 12] = (40, 22, 48)
        for k in range(4):
            img[ny + 4 + k * 11:ny + 12 + k * 11, nx + 3:nx + 9] = (255, 120, 170)
        stepped_glow(img, nx + 6, ny + 23, 34, (255, 110, 170), k=0.35, levels=3, sy=1.3)
    return img


def bokeh_lights(seed=5, n=30, w=W, h=H, y0=150, y1=330):
    rng = np.random.default_rng(seed)
    pal = [C('#ffb26b'), C('#ffd08a'), C('#ff8f5a'), C('#7fd6e0'), C('#ff8fb8'), C('#ffe2a6'), C('#b8a6ff')]
    wts = [5, 4, 3, 2, 2, 3, 1]
    pp = np.array(wts, float) / sum(wts)
    out = []
    for i in range(n):
        x = rng.uniform(-10, w + 10); y = rng.uniform(y0, y1)
        r = rng.uniform(6, 18) * (0.6 + 0.7 * (y - y0) / max(1, y1 - y0))
        out.append((x, y, r, pal[int(rng.choice(len(pal), p=pp))], rng.uniform(0.5, 0.9)))
    return out


def draw_bokeh_crisp(img, lights):
    for (x, y, r, col, s) in lights:
        rr = max(2.0, r * 0.45)
        m = m_ellipse(x, y, rr, rr, img.shape[1], img.shape[0])
        img[m] = np.minimum(255, img[m] * 0.35 + np.asarray(col, np.float32) * 0.75 * s + 18)
        e = inner_edge(m, 1, 1) | inner_edge(m, -1, -1)
        img[e] = np.minimum(255, img[e] * 1.08 + 10)
        stepped_glow(img, x, y, rr * 2.2, col, k=0.22 * s, levels=2)


def soft_glow_layer(lights, w=W, h=H, k=1.0):
    g = np.zeros((h, w, 3), np.float32)
    for (x, y, r, col, s) in lights:
        stepped_glow(g, x, y, r * 1.9, col, k=0.42 * s * k, levels=4)
    return g


def fog_alpha(pane, seed=3, base=0.27, bottom=0.50, edge=0.44):
    """smooth-ish condensation: denser at bottom and frame edges; 4 flat levels."""
    from scipy.ndimage import distance_transform_edt
    h, w = pane.shape
    rng = np.random.default_rng(seed)
    g = rng.random((h // 40 + 3, w // 40 + 3)).astype(np.float32)
    nz = np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((w + 80, h + 80), Image.BICUBIC), np.float32)[40:40 + h, 40:40 + w] / 255
    dd = distance_transform_edt(pane)
    yy = np.arange(h)[:, None] / h
    f = base + (nz - 0.5) * 0.04
    f += (edge - base) * np.clip(1 - dd / 22, 0, 1)
    ys = np.where(pane.any(1))[0]
    yb = ys.max() if len(ys) else h
    f += (bottom - base) * np.clip(1 - (yb - np.arange(h)[:, None]) / 46.0, 0, 1)
    lv = np.array([0.20, 0.28, 0.38, 0.50])
    q = lv[np.abs(f[..., None] - lv).argmin(-1)]
    return (q * pane).astype(np.float32)


@functools.lru_cache(maxsize=2)
def his_window():
    FX0, FX1, FY0, FY1 = 28, 612, 14, 298
    T = 9
    clear = city_outside(seed=11)
    lights = bokeh_lights(seed=5)
    draw_bokeh_crisp(clear, lights)
    soft = soft_glow_layer(lights)
    pane = m_rect(FX0 + T, FY0 + T, FX1 - T, FY1 - T)
    trans_y = 82
    pane &= ~m_rect(0, trans_y, W, trans_y + 7)
    for mx in (222, 418):
        pane &= ~m_rect(mx, 0, mx + 5, trans_y + 7)
    A = fog_alpha(pane, seed=7)
    # ---- room / frame overlay (warm lamp from the left) ----
    fr = np.zeros((H, W, 4), np.float32)
    col = fr[..., :3]
    al = fr[..., 3]
    al[:] = 1.0
    al[pane] = 0.0
    wall_bands = [C('#5a3a40'), C('#4a3240'), C('#3c2b3c'), C('#312438'), C('#291f33'), C('#221a2d')]
    xs = np.arange(W)
    band = np.clip((xs / 110).astype(int), 0, len(wall_bands) - 1)
    for i, c in enumerate(wall_bands):
        col[:, band == i] = c
    # frame wood
    frame_m = m_rect(FX0, FY0, FX1, FY1) & ~pane
    wood = C('#4a3333'); wood_l = C('#7b5446'); wood_hl = C('#a8735a'); wood_d = C('#2e2026'); cool = C('#8590c4')
    col[frame_m] = wood
    # warm lit faces: the left side of every bar (faces lamp) & top faces
    lit = frame_m & ~shift(frame_m, 1, 0)
    col[lit] = wood_l
    col[frame_m & ~shift(frame_m, 0, 1)] = wood_l
    # inner edges touching glass get cool rim (outside light)
    col[outline_of(pane) & frame_m & shift(pane, 0, -1)] = cool * 0.8      # above-glass edge (bottom face of bars)
    col[outline_of(pane) & frame_m & shift(pane, 0, 1)] = cool               # below-glass edge (top of bars) catches light
    col[outline_of(pane) & frame_m & shift(pane, -1, 0)] = cool * 0.7
    col[frame_m & ~shift(frame_m, -1, 0)] = wood_d
    outer = outline_of(m_rect(FX0, FY0, FX1, FY1))
    col[outer] = C('#1d151c')
    # latch
    col[m_rect(300, FY1 - 8, 340, FY1 - 3)] = C('#2a1f22')
    col[m_rect(302, FY1 - 7, 338, FY1 - 6)] = C('#c99a6c')
    # sill
    sill = m_rect(FX0 - 20, FY1, FX1 + 20, FY1 + 13)
    col[sill] = C('#6b4a3e')
    col[m_rect(FX0 - 20, FY1, FX1 + 20, FY1 + 2)] = wood_hl
    col[m_rect(FX0 - 20, FY1 + 2, FX1 + 20, FY1 + 3)] = C('#8d6250')
    col[m_rect(FX0 - 20, FY1 + 11, FX1 + 20, FY1 + 13)] = C('#3c2a2c')
    col[m_rect(FX0 - 20, FY1 + 13, FX1 + 20, FY1 + 16)] = C('#1a1219')
    below = m_rect(0, FY1 + 16, W, H)
    for i, c in enumerate([C('#3a2832'), C('#30222e'), C('#281d29'), C('#211824'), C('#1b1420'), C('#18121c')]):
        col[below & (band == i)] = c * 0.9
    # curtain right
    cur = m_poly([(566, 0), (640, 0), (640, 360), (596, 360), (580, 260), (590, 150), (572, 40)])
    col[cur] = C('#2c2a44')
    for i, x in enumerate(range(582, 640, 10)):
        fold = m_poly([(x, 0), (x + 3, 0), (x + 6 + (i % 2) * 2, 360), (x + 3, 360)]) & cur
        col[fold] = C('#3a3858')
        col[inner_edge(fold, -1, 0) & cur] = C('#4a4870')
    col[inner_edge(cur, -1, 0, 1)] = C('#7c6a8a')
    # sill props: mug (left, warm-lit) + plant (right)
    def prop(m, base, lit_c, rim_c=None):
        col[m] = base; al[m] = 1
        col[inner_edge(m, -1, 0) & m] = lit_c
        col[inner_edge(m, 0, -1) & m] = lit_c
        if rim_c is not None:
            col[inner_edge(m, 1, 0) & m] = rim_c
        col[outline_of(m) & ~pane & ~sill] = C('#1a1219')
    mug = m_rect(92, FY1 - 19, 110, FY1)
    prop(mug, C('#c8b8a8'), C('#f2e2cc'), C('#8f86a8'))
    col[m_rect(92, FY1 - 19, 110, FY1 - 17)] = C('#5a4a48')
    handle = m_ellipse(113, FY1 - 10, 4, 5) & ~m_ellipse(113, FY1 - 10, 2, 3)
    prop(handle, C('#b2a294'), C('#d8c8b6'))
    col[m_rect(97, FY1 - 12, 105, FY1 - 6)] = C('#d07a6a')  # little heart print
    pot = m_poly([(468, FY1 - 15), (492, FY1 - 15), (488, FY1), (472, FY1)])
    prop(pot, C('#9a5a46'), C('#c47c5a'), C('#6a5a7a'))
    col[m_rect(466, FY1 - 17, 494, FY1 - 14)] = C('#b06a50'); al[m_rect(466, FY1 - 17, 494, FY1 - 14)] = 1
    for (c, L) in ((-0.95, 24), (-0.35, 32), (0.15, 36), (0.7, 30), (1.15, 22)):
        pts = [(480 + math.sin(c) * s * L / 10 + (s * s * 0.08 * (1 if c > 0 else -1)), FY1 - 16 - math.cos(c) * s * L / 10) for s in range(11)]
        lm = m_line(pts, 3)
        col[lm] = C('#2f5a4a'); al[lm] = 1
        col[inner_edge(lm, -1, 0) & lm] = C('#5f9a72')
        col[inner_edge(lm, 1, 0) & lm] = C('#24403a')
    # lamp spill on wall top-left corner (stepped glow)
    spill = np.zeros((H, W, 3), np.float32)
    stepped_glow(spill, -60, 320, 300, (255, 170, 110), k=0.16, levels=3)
    m_out = al > 0
    col[m_out] = np.minimum(255, col[m_out] + spill[m_out] * 0.6)
    # fog colour: warmer on the lamp side (left), cool lavender on the right; 4 flat steps
    fogc = np.empty((H, W, 3), np.float32)
    steps = [C('#c6aebc'), C('#bcabc8'), C('#b2acd2'), C('#aaaad6')]
    for i, c in enumerate(steps):
        fogc[:, i * W // 4:(i + 1) * W // 4] = c
    return dict(clear=clear, soft=soft, A=A, pane=pane, frame=fr, sill_y=FY1, lights=lights, box=(FX0, FY0, FX1, FY1),
                fog=fogc)
