# -*- coding: utf-8 -*-
"""Rain, splashes, ripples, glass drops/fog, reflections. All deterministic in t; particles step at 12 fps."""
import numpy as np, math
from core import *


# ---------------- rain streaks ----------------
RAIN_LAYERS = {
    # name: (count per 640x360, speed px/s, length, width, alpha)
    'far': (260, 330, 4, 1, 0.30),
    'mid': (120, 470, 7, 1, 0.48),
    'near': (34, 640, 12, 2, 0.62),
}


def rain(img, t, layers=('far', 'mid', 'near'), color=(200, 214, 236), slant=0.18, density=1.0, seed=0,
         light=None, region=None, ox=0, oy=0, fps=12, stop_at=None):
    """light: optional HxWx3 additive light map (0..1 scale) - streaks pick up lamp colour.
    ox,oy: camera offset (parallax)."""
    T = tq(t, fps) if stop_at is None else min(tq(t, fps), stop_at)
    Hh, Ww = img.shape[:2]
    col = np.asarray(color, np.float32)
    for li, name in enumerate(layers):
        n, sp, ln, wd, al = RAIN_LAYERS[name]
        par = (0.5, 0.8, 1.3)[li % 3] if len(layers) == 3 else 1.0
        n = int(n * density * (Ww * Hh) / (640 * 360))
        if n <= 0:
            continue
        i = np.arange(n)
        r1 = (np.sin(i * 12.9898 + seed * 7.13 + li * 3.1) * 43758.5453) % 1
        r2 = (np.sin(i * 78.233 + seed * 3.71 + li * 1.7) * 24634.6345) % 1
        r3 = (np.sin(i * 39.425 + seed * 1.37 + li * 5.3) * 12345.6789) % 1
        spd = sp * (0.85 + 0.3 * r3)
        span = Hh + ln + 40
        y = (r2 * span + spd * T - oy * par) % span - ln - 20
        x = (r1 * (Ww + 80) + y * slant - ox * par) % (Ww + 80) - 40
        ks = np.arange(ln)
        py = (y[:, None] + ks[None, :]).astype(int)
        px = (x[:, None] + ks[None, :] * slant).astype(int)
        # tail fades: last third lighter alpha
        a = np.full(py.shape, al, np.float32)
        a[:, :ln // 3] *= 0.5
        for dx in range(wd):
            qx = px + dx
            ok = (py >= 0) & (py < Hh) & (qx >= 0) & (qx < Ww)
            yy, xx, aa = py[ok], qx[ok], a[ok]
            if region is not None:
                k = region[yy, xx]
                yy, xx, aa = yy[k], xx[k], aa[k]
            c = col[None, :]
            if light is not None:
                c = np.minimum(255, col[None, :] * 0.7 + light[yy, xx] * 255 * 0.9)
            img[yy, xx] = img[yy, xx] * (1 - aa[:, None]) + c * aa[:, None]


def splashes(img, t, y0, y1, x0=0, x1=None, rate=40, color=(205, 218, 240), seed=1, region=None, scale=(0.6, 1.4), fps=12):
    """little crown splashes on a ground band. rate = splashes per second in band"""
    x1 = img.shape[1] if x1 is None else x1
    s = math.floor(t * fps + 1e-6)
    per = max(1, int(rate / fps))
    col = np.asarray(color, np.float32)
    for age in range(3):
        k = s - age
        for j in range(per):
            u, v = h01(k, j, seed), h01(j, k, seed + 9)
            x = int(x0 + u * (x1 - x0))
            yf = y0 + v * (y1 - y0)
            y = int(yf)
            sc = scale[0] + (scale[1] - scale[0]) * v  # nearer = bigger
            pts = []
            if age == 0:
                pts = [(0, 0), (-1, -1), (1, -1)]
            elif age == 1:
                w = max(1, int(2 * sc))
                pts = [(-w, -1), (w, -1), (-w - 1, -2 - int(sc)), (w + 1, -2 - int(sc)), (0, -2)]
            else:
                w = max(2, int(3 * sc))
                pts = [(-w, 0), (w, 0), (-w - 1, -1 - int(2 * sc)), (w + 1, -1 - int(2 * sc))]
            a = (0.85, 0.7, 0.45)[age]
            for dx, dy in pts:
                X, Y = x + dx, y + dy
                if 0 <= X < img.shape[1] and 0 <= Y < img.shape[0]:
                    if region is None or region[Y, X]:
                        img[Y, X] = img[Y, X] * (1 - a) + col * a


def ripples(img, t, mask, rate=10, color=(190, 205, 232), seed=2, flat=0.35, rmax=7, fps=12):
    """expanding ellipse rings inside mask (puddles). flat = ry/rx (1 for top-down)."""
    s = math.floor(t * fps + 1e-6)
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return
    per = max(1, int(round(rate / fps)))
    col = np.asarray(color, np.float32)
    life = 6
    for age in range(life):
        k = s - age
        for j in range(per):
            idx = int(h01(k, j, seed) * len(xs))
            cx, cy = xs[idx], ys[idx]
            r = 1 + age * (rmax - 1) / (life - 1)
            a = 0.75 * (1 - age / life)
            n = max(8, int(r * 6))
            th = np.linspace(0, 2 * np.pi, n, endpoint=False)
            px = np.round(cx + r * np.cos(th)).astype(int)
            py = np.round(cy + r * flat * np.sin(th)).astype(int)
            ok = (px >= 0) & (px < img.shape[1]) & (py >= 0) & (py < img.shape[0])
            px, py = px[ok], py[ok]
            ok = mask[py, px]
            px, py = px[ok], py[ok]
            img[py, px] = img[py, px] * (1 - a) + col * a


def reflect(img, y_ground, y_end=None, k=0.42, squash=1.0, t=0, wobble=1, mask=None, tint=(60, 70, 96), broken=True):
    """mirror everything above y_ground into the band below it; rows broken by integer wobble."""
    Hh = img.shape[0]
    y_end = Hh if y_end is None else y_end
    T = tq(t, 8)
    src = img.copy()
    tint = np.asarray(tint, np.float32)
    for y in range(y_ground, y_end):
        d = y - y_ground
        sy = int(y_ground - 1 - d * squash)
        if sy < 0:
            break
        off = 0
        if wobble:
            off = int(round(math.sin(y * 0.9 + T * 5.0) * wobble * (0.4 + d / 60)))
        row = np.roll(src[sy], off, axis=0)
        kk = k * (0.55 if (broken and d % 3 == 2) else 1.0) * max(0.35, 1 - d / 140)
        if mask is None:
            img[y] = img[y] * (1 - kk) + (row * 0.7 + tint * 0.3) * kk
        else:
            m = mask[y]
            img[y, m] = img[y, m] * (1 - kk) + (row[m] * 0.7 + tint * 0.3) * kk


def light_streaks(img, t, lights, y_ground, y_end, mask=None):
    """lights: list of (x, y_src, color, width, strength) -> vertical broken streaks in wet ground"""
    T = tq(t, 8)
    for (x, ys, color, wd, st) in lights:
        L = int((y_ground - ys) * 1.1 + 20)
        col = np.asarray(color, np.float32)
        for d in range(0, min(L, y_end - y_ground)):
            y = y_ground + d
            if ((d // 2) + int(T * 6)) % 3 == 2:
                continue
            fall = 1 - d / max(1, L)
            ww = max(1, int(wd * (0.6 + 0.6 * fall)))
            off = int(round(math.sin((y // 2) * 1.3 + T * 4) * (0.4 + d / 50)))
            xa, xb = int(x - ww / 2 + off), int(x + ww / 2 + off) + 1
            xa, xb = max(0, xa), min(img.shape[1], xb)
            if xb <= xa:
                continue
            a = st * (0.35 + 0.65 * fall)
            if mask is not None:
                m = mask[y, xa:xb]
                seg_ = img[y, xa:xb]
                seg_[m] = np.minimum(255, seg_[m] + col * a)
            else:
                img[y, xa:xb] = np.minimum(255, img[y, xa:xb] + col * a)


# ---------------- glass: fog + drops ----------------

def fog_map(w, h, seed=3, base=0.5, var=0.18, levels=(0.38, 0.5, 0.62), pane=None, edge=0.12):
    """blotchy fog alpha, quantized to 3 flat levels (static -> free for the encoder)."""
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    for sc, amp in ((60, 1.0), (28, 0.5), (12, 0.25)):
        g = rng.random((h // sc + 3, w // sc + 3)).astype(np.float32)
        im = Image.fromarray((g * 255).astype(np.uint8)).resize((w + 2 * sc, h + 2 * sc), Image.BICUBIC)
        a = np.asarray(im, np.float32)[sc:sc + h, sc:sc + w] / 255
        acc += a * amp
    acc /= 1.75
    yy = np.linspace(0, 1, h)[:, None]
    f = base + (acc - 0.5) * var * 2 + (yy - 0.5) * 0.16
    if pane is not None:
        from scipy.ndimage import distance_transform_edt
        dd = distance_transform_edt(pane)
        f += edge * np.clip(1 - dd / 26, 0, 1)
    out = np.full_like(f, levels[0])
    out[f > (levels[0] + levels[1]) / 2] = levels[1]
    out[f > (levels[1] + levels[2]) / 2] = levels[2]
    return out


class Drop:
    def __init__(self, t_hit, x, y, r, slide_at=None, speed=26, seed=0, splash=True, beads=True, stop_y=None):
        self.t_hit, self.x, self.y, self.r = t_hit, x, y, r
        self.slide_at = slide_at
        self.speed, self.seed, self.splash, self.beads = speed, seed, splash, beads
        self.stop_y = stop_y

    def path_y(self, u):
        # stick-slip slide
        return self.speed * (u + 0.22 * math.sin(2 * math.pi * 1.3 * u + self.seed) / (2 * math.pi * 1.3)
                             - 0.22 * math.sin(self.seed) / (2 * math.pi * 1.3))

    def pos(self, t):
        if self.slide_at is None or t < self.slide_at:
            return self.x, self.y
        u = t - self.slide_at
        dy = self.path_y(u)
        if self.stop_y is not None:
            dy = min(dy, self.stop_y - self.y)
        dx = round(1.5 * math.sin(dy * 0.09 + self.seed))
        return self.x + dx, self.y + dy

    def trail(self, t, step=1.0):
        if self.slide_at is None or t <= self.slide_at:
            return []
        pts = []
        u = 0.0
        x1, y1 = self.pos(t)
        yy = self.y
        while yy < y1:
            dx = round(1.5 * math.sin((yy - self.y) * 0.09 + self.seed))
            pts.append((self.x + dx, yy))
            yy += step
        pts.append((x1, y1))
        return pts


def draw_drop(img, through, cx, cy, r, glow=None):
    """water bead on glass. through = clear outside image (for refraction)."""
    cx, cy = int(round(cx)), int(round(cy))
    Hh, Ww = img.shape[:2]
    if r <= 1.2:
        if 0 <= cx < Ww and 0 <= cy < Hh:
            img[cy, cx] = np.minimum(255, through[cy, cx] * 1.25 + 30)
            if cy + 1 < Hh:
                img[cy + 1, cx] = through[cy + 1, cx] * 0.6
        return
    R = int(math.ceil(r)) + 1
    x0, y0 = cx - R, cy - R
    yy, xx = np.mgrid[-R:R + 1, -R:R + 1]
    body = (xx / r) ** 2 + (yy / (r * 1.06)) ** 2 <= 1.0
    # refraction: inverted, minified sample
    sx = np.clip(cx - (xx * 1.6).astype(int), 0, Ww - 1)
    sy = np.clip(cy - (yy * 1.6).astype(int) - int(r), 0, Hh - 1)
    col = np.minimum(255, through[sy, sx] * 1.05 + 22)
    dark = body & ~np.roll(np.roll(body, 1, 0), 1, 1)  # top-left rim
    lite = body & ~np.roll(np.roll(body, -1, 0), -1, 1)  # bottom-right rim
    lite2 = body & ~np.roll(body, -2, 0) & (yy > 0)
    out = col.copy()
    if r >= 5:
        out[lite2] = np.minimum(255, col[lite2] * 0.6 + np.array([95, 100, 130], np.float32))
    out[dark] = col[dark] * 0.45 + np.array([10, 8, 22], np.float32)
    out[lite] = np.minimum(255, col[lite] * 0.4 + np.array([150, 155, 185], np.float32))
    if glow is not None:
        out[body] = np.minimum(255, out[body] * 0.6 + np.asarray(glow, np.float32) * 0.55)
    # specular
    hx, hy = int(round(-r * 0.38)), int(round(-r * 0.42))
    spec = np.zeros_like(body)
    spec[R + hy, R + hx] = True
    if r >= 4.5:
        spec[R + hy, R + hx + 1] = True
        spec[R + hy + 1, R + hx] = True
    if r >= 8:
        spec[R + hy - 1, R + hx] = True
        spec[R + hy, R + hx - 1] = True
    out[spec & body] = (246, 250, 255)
    # paste
    ys0, xs0 = max(0, y0), max(0, x0)
    ys1, xs1 = min(Hh, y0 + 2 * R + 1), min(Ww, x0 + 2 * R + 1)
    if ys1 <= ys0 or xs1 <= xs0:
        return
    b = body[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]
    o = out[ys0 - y0:ys1 - y0, xs0 - x0:xs1 - x0]
    reg = img[ys0:ys1, xs0:xs1]
    reg[b] = o[b]


def splash_ring(img, cx, cy, r, age, color=(235, 242, 255)):
    """age in 0..1 over ~0.25s: broken ring + flecks"""
    col = np.asarray(color, np.float32)
    rr = r * (0.7 + 1.1 * age)
    n = 10
    for i in range(n):
        if (i + int(age * 3)) % 3 == 0:
            continue
        th = i / n * 2 * math.pi + 0.3
        for dr in (0, 1):
            x = int(round(cx + (rr + dr) * math.cos(th)))
            y = int(round(cy + (rr + dr) * math.sin(th) * 0.95))
            if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
                a = 0.9 * (1 - age)
                img[y, x] = img[y, x] * (1 - a) + col * a
    if age < 0.35:
        stepped_glow(img, cx, cy, r * 2.6, color, k=0.7 * (1 - age / 0.35), levels=3)
    if age < 0.2 and r >= 6:
        L = int(r * 1.6)
        for k in range(-L, L + 1):
            for (x, y) in ((cx + k, cy), (cx, cy + k)):
                x, y = int(x), int(y)
                if 0 <= x < img.shape[1] and 0 <= y < img.shape[0]:
                    a = 0.95 * (1 - abs(k) / (L + 1))
                    img[y, x] = img[y, x] * (1 - a) + col * a


class Glass:
    """window pane: clear outside (+rain) -> fog (static alpha) + soft light glow -> wiped areas -> drops."""

    def __init__(self, pane, A, fog_color=(169, 166, 200), soft=None):
        self.pane = pane
        self.fog_color = np.asarray(fog_color, np.float32)
        self.A = A
        self.soft = soft
        self.drops = []
        self.beads = []  # (x, y, r, t_appear)

    def satellites(self, d):
        out = []
        if not d.splash:
            return out
        n = 3 + int(h01(d.seed, 5) * 3)
        for i in range(n):
            th = h01(d.seed, i) * 2 * math.pi
            dist = d.r * (1.5 + 1.4 * h01(i, d.seed))
            out.append((d.x + dist * math.cos(th), d.y + dist * math.sin(th) * 0.9,
                        1 if h01(i, 7, d.seed) < 0.7 else 2))
        return out

    def render(self, out_dyn, through, t, extra_clear=None, fog_k=1.0, glow_drops=None, wet_edges=True):
        A = self.A * fog_k
        clear = np.zeros(self.pane.shape, bool)
        if extra_clear is not None:
            clear |= extra_clear
        live = []
        for d in self.drops:
            if t < d.t_hit:
                continue
            tr = d.trail(t)
            if len(tr) > 1:
                clear |= m_line(tr, max(1, int(d.r * 1.15)), self.pane.shape[1], self.pane.shape[0])
            live.append(d)
        clear &= self.pane
        A2 = np.where(clear, 0.0, A)[..., None]
        out = out_dyn * (1 - A2) + self.fog_color * A2
        if self.soft is not None:
            out = np.minimum(255, out + self.soft * np.where(clear, 0.25, 1.0)[..., None])
        out[clear] = np.minimum(255, out_dyn[clear] * 1.06 + 4)
        if wet_edges:
            e = outline_of(clear) & self.pane
            fc = self.fog_color[e] if self.fog_color.ndim == 3 else self.fog_color
            out[e] = np.minimum(255, out[e] * 0.82 + fc * 0.32)
            # water line under wiped areas (collects at the lower edge)
            lo = clear & ~shift(clear, 0, -1) & self.pane
            out[lo] = np.minimum(255, out[lo] * 0.6 + np.array([210, 220, 245], np.float32) * 0.45)
        for (x, y, r, ta) in self.beads:
            if t >= ta:
                draw_drop(out, through, x, y, r)
        for d in live:
            if d.splash:
                for (sx, sy, sr) in self.satellites(d):
                    if t >= d.t_hit + 0.08:
                        draw_drop(out, through, sx, sy, sr)
            tr = d.trail(t)
            if d.beads and len(tr) > 12:
                for i in range(10, len(tr) - 6, 13 + int(h01(d.seed) * 6)):
                    draw_drop(out, through, tr[i][0], tr[i][1], 1)
            x, y = d.pos(t)
            age = (t - d.t_hit) / 0.25
            rr = d.r * (0.6 + 0.4 * clamp(age * 2)) if age < 0.5 else d.r
            g = None
            if glow_drops is not None and id(d) in glow_drops:
                g = glow_drops[id(d)]
            draw_drop(out, through, x, y, rr, glow=g)
            if d.splash and age < 1:
                splash_ring(out, d.x, d.y, d.r, age)
        return out
