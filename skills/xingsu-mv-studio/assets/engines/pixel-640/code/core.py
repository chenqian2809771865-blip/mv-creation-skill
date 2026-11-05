# -*- coding: utf-8 -*-
"""Pixel core: 640x360 logical grid, integer upscale. Flat colours, stepped light, no full-frame dither/grain
(those turn into mush after Douyin re-encode)."""
import numpy as np, math, functools, json, os
from PIL import Image, ImageDraw, ImageFont

W, H = 640, 360
FPS = 24
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, 'assets')
TIMING = json.load(open(os.path.join(ASSETS, 'timing.json'), encoding='utf-8'))


def C(h):
    h = h.lstrip('#')
    return np.array([int(h[i:i + 2], 16) for i in (0, 2, 4)], np.float32)


def mix(a, b, k):
    return np.asarray(a, np.float32) * (1 - k) + np.asarray(b, np.float32) * k


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def ease_in(x):
    x = clamp(x)
    return x ** 3


def seg(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= a)


def tq(t, fps=12):
    """animate on twos (12 fps) - effects step cleanly and encode well"""
    return math.floor(t * fps + 1e-6) / fps


def h01(*k):
    """deterministic hash -> [0,1)"""
    x = 0x345678
    for v in k:
        x = (x ^ (int(v) & 0xffffffff)) * 1000003 & 0xffffffff
        x ^= x >> 13
        x = (x * 0x5bd1e995) & 0xffffffff
        x ^= x >> 15
    return (x & 0xffffff) / float(0x1000000)


def new(color, w=W, h=H):
    img = np.empty((h, w, 3), np.float32)
    img[:] = color
    return img


# ---------- masks ----------

def _mask_img(w, h):
    im = Image.new('L', (w, h), 0)
    return im, ImageDraw.Draw(im)


def m_poly(pts, w=W, h=H):
    im, d = _mask_img(w, h)
    d.polygon([(round(x), round(y)) for x, y in pts], fill=1)
    return np.asarray(im, bool)


def m_ellipse(cx, cy, rx, ry, w=W, h=H):
    im, d = _mask_img(w, h)
    if round(cx + rx) - 1 < round(cx - rx) or round(cy + ry) - 1 < round(cy - ry):
        return np.zeros((h, w), bool)
    d.ellipse([round(cx - rx), round(cy - ry), round(cx + rx) - 1, round(cy + ry) - 1], fill=1)
    return np.asarray(im, bool)


def m_rect(x0, y0, x1, y1, w=W, h=H):
    m = np.zeros((h, w), bool)
    m[max(0, int(y0)):max(0, int(y1)), max(0, int(x0)):max(0, int(x1))] = True
    return m


def m_line(pts, width, w=W, h=H):
    im, d = _mask_img(w, h)
    p = [(round(x), round(y)) for x, y in pts]
    d.line(p, fill=1, width=int(width), joint='curve')
    if width > 2:
        r = width / 2
        for x, y in (p[0], p[-1]):
            d.ellipse([x - r, y - r, x + r - 1, y + r - 1], fill=1)
    return np.asarray(im, bool)


def shift(m, dx, dy):
    out = np.zeros_like(m)
    h, w = m.shape[:2]
    xs0, xs1 = max(0, -dx), min(w, w - dx)
    ys0, ys1 = max(0, -dy), min(h, h - dy)
    out[ys0 + dy:ys1 + dy, xs0 + dx:xs1 + dx] = m[ys0:ys1, xs0:xs1]
    return out


def outline_of(m, diag=False):
    """1px exterior border of mask"""
    o = shift(m, 1, 0) | shift(m, -1, 0) | shift(m, 0, 1) | shift(m, 0, -1)
    if diag:
        o |= shift(m, 1, 1) | shift(m, -1, -1) | shift(m, 1, -1) | shift(m, -1, 1)
    return o & ~m


def inner_edge(m, dx, dy, width=1):
    """pixels of m whose neighbour in direction (dx,dy) (up to width) is outside m"""
    e = np.zeros_like(m)
    for k in range(1, width + 1):
        e |= m & ~shift(m, -dx * k, -dy * k)
    return e


# ---------- painting ----------

def fill(img, m, color, a=1.0):
    if a >= 1:
        img[m] = color
    elif a > 0:
        img[m] = img[m] * (1 - a) + np.asarray(color, np.float32) * a


def add(img, m, color, a=1.0):
    img[m] = np.minimum(255, img[m] + np.asarray(color, np.float32) * a)


def blit(img, spr, x, y, a=1.0):
    """spr: (h,w,4) float32, alpha channel 0..1 (usually 0/1). x,y top-left (ints)."""
    x, y = int(round(x)), int(round(y))
    sh, sw = spr.shape[:2]
    H_, W_ = img.shape[:2]
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W_, x + sw), min(H_, y + sh)
    if x1 <= x0 or y1 <= y0:
        return
    s = spr[y0 - y:y1 - y, x0 - x:x1 - x]
    al = s[..., 3:4] * a
    reg = img[y0:y1, x0:x1]
    reg[:] = reg * (1 - al) + s[..., :3] * al


def stepped_glow(img, cx, cy, r, color, k=0.5, levels=3, sy=1.0, mask=None):
    """additive light in concentric flat rings (no smooth gradient -> no banding/mush)."""
    x0, x1 = int(max(0, cx - r)), int(min(img.shape[1], cx + r + 1))
    y0, y1 = int(max(0, cy - r * sy)), int(min(img.shape[0], cy + r * sy + 1))
    if x1 <= x0 or y1 <= y0:
        return
    yy, xx = np.mgrid[y0:y1, x0:x1]
    d = np.sqrt(((xx - cx) / r) ** 2 + ((yy - cy) / (r * sy)) ** 2)
    lv = np.floor((1 - d) * levels + 1e-6).clip(0, levels) / levels
    lv = lv ** 1.6
    if mask is not None:
        lv = lv * mask[y0:y1, x0:x1]
    reg = img[y0:y1, x0:x1]
    reg[:] = np.minimum(255, reg + lv[..., None] * np.asarray(color, np.float32) * k)


def darken(img, m, k):
    img[m] *= k


def vgrad_bands(img, y0, y1, c0, c1, n, x0=0, x1=None):
    """flat horizontal bands from c0 to c1"""
    x1 = img.shape[1] if x1 is None else x1
    for i in range(n):
        a = int(round(y0 + (y1 - y0) * i / n))
        b = int(round(y0 + (y1 - y0) * (i + 1) / n))
        img[max(0, a):max(0, b), x0:x1] = mix(c0, c1, i / max(1, n - 1))


# ---------- text ----------
@functools.lru_cache(maxsize=8)
def font(size=16, name='unifont.ttf'):
    return ImageFont.truetype(os.path.join(ASSETS, name), size)


@functools.lru_cache(maxsize=4096)
def glyph_mask(ch, size=16):
    f = font(size)
    im = Image.new('L', (size * 2, size * 2), 0)
    d = ImageDraw.Draw(im)
    d.fontmode = '1'
    d.text((0, 0), ch, font=f, fill=255)
    a = np.asarray(im) > 127
    adv = int(round(f.getlength(ch)))
    return a, adv


def text_mask(s, size=16, spacing=0):
    gl = [glyph_mask(c, size) for c in s]
    w = sum(g[1] + spacing for g in gl) - spacing
    hgt = size * 2
    m = np.zeros((hgt, max(1, w)), bool)
    x = 0
    for a, adv in gl:
        ww = min(a.shape[1], m.shape[1] - x)
        m[:, x:x + ww] |= a[:, :ww]
        x += adv + spacing
    # trim rows
    rows = np.where(m.any(1))[0]
    if len(rows):
        m = m[rows[0]:rows[-1] + 1]
    return m


def draw_text(img, s, x, y, color, size=16, outline=None, shadow=None, a=1.0, scale=1, spacing=0, anchor='lt'):
    m = text_mask(s, size, spacing)
    if scale > 1:
        m = np.repeat(np.repeat(m, scale, 0), scale, 1)
    h, w = m.shape
    if anchor[0] == 'm':
        x -= w // 2
    if anchor[1] == 'm':
        y -= h // 2
    x, y = int(x), int(y)
    pad = 2
    big = np.zeros((h + 2 * pad, w + 2 * pad), bool)
    big[pad:pad + h, pad:pad + w] = m
    full = np.zeros(img.shape[:2], bool)

    def place(mm, ox, oy):
        out = np.zeros(img.shape[:2], bool)
        hh, ww = mm.shape
        X0, Y0 = x - pad + ox, y - pad + oy
        xs0, ys0 = max(0, X0), max(0, Y0)
        xs1, ys1 = min(img.shape[1], X0 + ww), min(img.shape[0], Y0 + hh)
        if xs1 > xs0 and ys1 > ys0:
            out[ys0:ys1, xs0:xs1] = mm[ys0 - Y0:ys1 - Y0, xs0 - X0:xs1 - X0]
        return out
    body = place(big, 0, 0)
    if shadow is not None:
        sh = place(big, 1 * scale, 1 * scale)
        if outline is not None:
            sh = place(big | outline_of(big), 1 * scale, 1 * scale)
        fill(img, sh & ~body, shadow, a)
    if outline is not None:
        ol = outline_of(body, diag=True)
        fill(img, ol, outline, a)
    fill(img, body, color, a)
    return body


def upscale(img, k):
    a = np.clip(img + 0.5, 0, 255).astype(np.uint8)
    return np.repeat(np.repeat(a, k, 0), k, 1)


def save_png(img, path, k=2):
    Image.fromarray(upscale(img, k)).save(path)
