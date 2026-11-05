# -*- coding: utf-8 -*-
"""S01 0-19.79: rain knocks on the window, one piano note = one drop; finger writes 下雨了 on the fog."""
import numpy as np, math, functools
from core import *
from fx import *
from scn_window import his_window
from writing import Writer
from props import pointing_hand

FREEZE = (19.38, 19.80)
WRITE = (9.31, 12.90)
TITLE = [('下', 212, 206, 104), ('雨', 322, 206, 104), ('了', 432, 206, 104)]


@functools.lru_cache(maxsize=1)
def setup():
    S = his_window()
    g = Glass(S['pane'], S['A'], fog_color=S['fog'], soft=S['soft'])
    D = []
    # 0.32 rolled chord: big drop centre + 4 small hits (0.51..0.67)
    big = Drop(0.32, 320, 112, 11, slide_at=1.55, speed=20, seed=1, stop_y=146)
    D.append(big)
    for i, (tt, dx, dy) in enumerate(((0.51, -26, 10), (0.57, 22, -12), (0.63, 30, 16), (0.67, -18, -16))):
        D.append(Drop(tt, 320 + dx, 110 + dy, 2.5 + (i % 2), seed=10 + i, beads=False))
    D.append(Drop(4.31, 548, 120, 5, slide_at=5.0, speed=16, seed=3, stop_y=176))
    D.append(Drop(5.52, 116, 236, 6, slide_at=6.2, speed=22, seed=4))
    D.append(Drop(5.67, 140, 222, 5, seed=5))
    # 6.81..8.38 six-note rising run: left -> right, each a little higher, last biggest
    run_t = (6.81, 7.14, 7.45, 7.77, 8.06, 8.38)
    for i, tt in enumerate(run_t):
        x = 118 + i * 80
        y = 146 - i * 8
        r = 4 + i * 0.7 + (2 if i == 5 else 0)
        D.append(Drop(tt, x, y, r, seed=20 + i, slide_at=(None if i not in (1, 4) else tt + 1.6), speed=14, stop_y=y + 30))
    D.append(Drop(8.77, 486, 268, 3, seed=30))
    g.drops = D
    # rain gets heavier on 12.90: beads appear on 12fps steps over 0.8s
    rng = np.random.default_rng(4)
    pane = S['pane']
    beads = []
    for i in range(70):
        while True:
            x, y = rng.integers(45, 595), rng.integers(30, 290)
            if pane[y, x]:
                break
        beads.append((int(x), int(y), 1 if rng.random() < 0.75 else 2, 12.90 + rng.random() * 1.1))
    for i in range(16):  # a few beads from the start
        while True:
            x, y = rng.integers(45, 595), rng.integers(30, 290)
            if pane[y, x]:
                break
        beads.append((int(x), int(y), 1, 0.0))
    g.beads = beads
    wr = Writer(TITLE, WRITE[0], WRITE[1], width=8, lift=0.24)
    # drips at char bottoms (15.25 / 15.36 / 15.48)
    m_full, _, _ = wr.state(WRITE[1] + 0.01)
    drips = []
    for (ch, cx, cy, sz), tt in zip(TITLE, (15.25, 15.36, 15.48)):
        x0, x1 = int(cx - sz / 2), int(cx + sz / 2)
        sub = m_full[:, x0:x1]
        ys, xs = np.nonzero(sub)
        k = np.argmax(ys)
        drips.append(Drop(tt, x0 + xs[k], ys[k] + 2, 3.2, slide_at=tt + 0.05, speed=46, seed=40 + len(drips),
                          splash=False, stop_y=292))
    g.drops = D + drips
    # reflection silhouette (him, fedora) - left of title
    rx, ry = 92, 70
    refl = (m_poly([(rx - 64, ry + 54), (rx - 30, ry + 46), (rx - 24, ry + 14), (rx - 14, ry + 2), (rx + 16, ry + 2),
                    (rx + 26, ry + 14), (rx + 30, ry + 46), (rx + 66, ry + 56), (rx + 64, ry + 62), (rx - 66, ry + 60)])  # hat
            | m_ellipse(rx, ry + 76, 22, 26)  # head
            | m_poly([(rx - 16, ry + 96), (rx + 16, ry + 96), (rx + 20, ry + 116), (rx - 20, ry + 116)])
            | m_poly([(rx - 90, ry + 240), (rx - 70, ry + 140), (rx - 22, ry + 112), (rx + 22, ry + 112), (rx + 74, ry + 140), (rx + 96, ry + 240)]))
    refl &= pane
    return S, g, wr, refl


def frame(t):
    S, g, wr, refl = setup()
    te = t
    frozen = FREEZE[0] <= t
    if frozen:
        te = FREEZE[0]
    out = S['clear'].copy()
    # outside rain behind glass
    dens = 0.0 + 0.35 * seg(te, 0.2, 2.0) + 0.65 * seg(te, 12.85, 13.3)
    if dens > 0:
        rain(out, te, layers=('far', 'mid'), density=dens, color=(190, 190, 230), slant=0.12, seed=3)
    # bokeh breathes a touch on 12.90 (rain thickens, lights blur)
    m, tip, touching = wr.state(te)
    img = g.render(out, S['clear'], te, extra_clear=m)
    # reflection fades in (stepped) 15.5 -> 17.5
    ra = [0, 0.18, 0.3, 0.42][int(clamp(seg(te, 15.5, 17.6)) * 3 + 1e-6) if te >= 15.5 else 0]
    if ra > 0:
        dark = img[refl] * 0.45 + np.array([20, 22, 34], np.float32) * 0.55
        img[refl] = img[refl] * (1 - ra) + dark * ra
        rim = inner_edge(refl, 1, 0) & S['pane']
        img[rim] = img[rim] * (1 - ra) + np.array([200, 210, 238], np.float32) * ra
    # frame overlay
    fr = S['frame']
    a = fr[..., 3:4]
    img = img * (1 - a) + fr[..., :3] * a
    # hand: enters 8.85-9.31, writes, leaves 12.95-13.6
    if 8.85 <= te < 13.6 and tip is not None:
        fx, fy = tip
        if te < WRITE[0]:
            u = ease_out(seg(te, 8.85, WRITE[0]))
            fx, fy = fx + (1 - u) * 220, fy + (1 - u) * 260
        elif te > WRITE[1] + 0.05:
            u = ease_in(seg(te, WRITE[1] + 0.05, 13.6))
            fx, fy = fx + u * 260, fy + u * 300
        if not touching and WRITE[0] <= te <= WRITE[1]:
            fy -= 0
        pointing_hand(img, fx, fy, angle=-0.62, S=1.55)
    # credit
    if te >= 12.90:
        ca = [0.0, 0.5, 1.0][min(2, int(seg(te, 12.9, 13.2) * 2 + 1e-6) + (1 if te >= 13.2 else 0))]
        draw_text(img, '薛之谦', 322, 274, (236, 240, 250), outline=(36, 40, 60), a=ca, anchor='mt')
    # impact shake on the very first hit (integer px)
    if 0.32 <= te < 0.45:
        dx = (1, -1, 1)[min(2, int((te - 0.32) * 24))]
        img = np.roll(img, dx, axis=1)
    if frozen and t >= 19.42:
        img = img * 0.86 + np.array([60, 70, 100], np.float32) * 0.14
    return img
