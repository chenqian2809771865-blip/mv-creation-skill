# -*- coding: utf-8 -*-
import os as _os
_CODE = _os.path.normpath(_os.path.join(_os.path.dirname(_os.path.abspath(__file__))))
_ROOT = _os.path.normpath(_os.path.join(_CODE, '..'))   # project root (fonts/, out/, assets/)
"""Pixel canvas toolkit: 320x180 logical grid, numpy RGB(A) canvases, dithering, text, sprites, grading."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, S = 320, 180, 8


def hx(s):
    s = s.lstrip('#')
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


def mix(a, b, f):
    return tuple(int(round(a[i] + (b[i] - a[i]) * f)) for i in range(3))


def mul(c, k):
    if isinstance(k, (int, float)):
        k = (k, k, k)
    return tuple(max(0, min(255, int(c[i] * k[i]))) for i in range(3))


OUT = hx('#1d1828')

BAYER4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) + 0.5) / 16
_BY = np.tile(BAYER4, (160, 260))


def bayer(h=H, w=W, ox=0, oy=0):
    return _BY[oy % 4:oy % 4 + h, ox % 4:ox % 4 + w]


class Cv:
    """numpy canvas. a: HxWx3 (or x4 with alpha) uint8."""

    def __init__(self, w=W, h=H, col=(0, 0, 0), alpha=False, arr=None):
        if arr is not None:
            self.a = arr
        else:
            ch = 4 if alpha else 3
            self.a = np.zeros((h, w, ch), np.uint8)
            if not alpha:
                self.a[:] = col
        self.h, self.w = self.a.shape[:2]
        self.alpha = self.a.shape[2] == 4

    def _c(self, col):
        if self.alpha:
            return (col[0], col[1], col[2], col[3] if len(col) > 3 else 255)
        return col[:3]

    def copy(self):
        return Cv(arr=self.a.copy())

    def px(self, x, y, col):
        x, y = int(x), int(y)
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x] = self._c(col)

    def rect(self, x, y, w, h, col):
        x0, y0 = int(round(x)), int(round(y))
        x1, y1 = x0 + int(round(w)), y0 + int(round(h))
        x0, y0, x1, y1 = max(0, x0), max(0, y0), min(self.w, x1), min(self.h, y1)
        if x1 > x0 and y1 > y0:
            self.a[y0:y1, x0:x1] = self._c(col)

    def hline(self, x0, x1, y, col):
        if x1 < x0:
            x0, x1 = x1, x0
        self.rect(x0, y, x1 - x0 + 1, 1, col)

    def vline(self, x, y0, y1, col):
        if y1 < y0:
            y0, y1 = y1, y0
        self.rect(x, y0, 1, y1 - y0 + 1, col)

    def line(self, x0, y0, x1, y1, col):
        x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x1)), int(round(y1))
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx, sy = (1 if x0 < x1 else -1), (1 if y0 < y1 else -1)
        err = dx + dy
        while True:
            self.px(x0, y0, col)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy; x0 += sx
            if e2 <= dx:
                err += dx; y0 += sy

    def mask_fill(self, m, col, x=0, y=0):
        """m: bool array placed at (x,y)."""
        x, y = int(round(x)), int(round(y))
        mh, mw = m.shape
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + mw), min(self.h, y + mh)
        if x1 <= x0 or y1 <= y0:
            return
        sub = m[y0 - y:y1 - y, x0 - x:x1 - x]
        self.a[y0:y1, x0:x1][sub] = self._c(col)

    def ellipse(self, cx, cy, rx, ry, col):
        x0, x1 = int(math.floor(cx - rx)), int(math.ceil(cx + rx))
        y0, y1 = int(math.floor(cy - ry)), int(math.ceil(cy + ry))
        yy, xx = np.mgrid[y0:y1 + 1, x0:x1 + 1]
        m = ((xx + 0.5 - cx) / max(rx, 0.01)) ** 2 + ((yy + 0.5 - cy) / max(ry, 0.01)) ** 2 <= 1.0
        self.mask_fill(m, col, x0, y0)

    def poly(self, pts, col):
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        x0, y0 = int(math.floor(min(xs))), int(math.floor(min(ys)))
        w, h = int(math.ceil(max(xs))) - x0 + 2, int(math.ceil(max(ys))) - y0 + 2
        im = Image.new('1', (w, h), 0)
        ImageDraw.Draw(im).polygon([(p[0] - x0, p[1] - y0) for p in pts], fill=1, outline=1)
        self.mask_fill(np.array(im, bool), col, x0, y0)

    def dither_rect(self, x, y, w, h, col, f, ox=0, oy=0):
        """fill a rect with col where bayer < f (ordered dither coverage)."""
        x0, y0 = int(x), int(y)
        m = bayer(int(h), int(w), x0 + ox, y0 + oy) < f
        self.mask_fill(m, col, x0, y0)

    def blit(self, spr, x, y, flip=False, alpha_mul=1.0):
        """spr: Cv with alpha or HxWx4 array; (x,y) top-left."""
        s = spr.a if isinstance(spr, Cv) else spr
        if flip:
            s = s[:, ::-1]
        x, y = int(round(x)), int(round(y))
        sh, sw = s.shape[:2]
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + sw), min(self.h, y + sh)
        if x1 <= x0 or y1 <= y0:
            return
        sub = s[y0 - y:y1 - y, x0 - x:x1 - x]
        if alpha_mul >= 1.0:
            m = sub[..., 3] > 127
        else:
            m = (sub[..., 3] > 127) & (bayer(y1 - y0, x1 - x0, x0, y0) < alpha_mul)
        dst = self.a[y0:y1, x0:x1]
        if self.alpha:
            dst[m] = sub[m]
        else:
            dst[m] = sub[..., :3][m]

    def paste(self, other, x, y):
        s = other.a
        x, y = int(round(x)), int(round(y))
        sh, sw = s.shape[:2]
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(self.w, x + sw), min(self.h, y + sh)
        if x1 <= x0 or y1 <= y0:
            return
        self.a[y0:y1, x0:x1, :3] = s[y0 - y:y1 - y, x0 - x:x1 - x, :3]


# ---------------------------------------------------------------- sprites helpers
def outline(spr, col=OUT, diag=False):
    """add a 1px outer outline around alpha>0 pixels. returns new Cv padded by 1."""
    a = spr.a
    h, w = a.shape[:2]
    o = np.zeros((h + 2, w + 2, 4), np.uint8)
    o[1:-1, 1:-1] = a
    m = o[..., 3] > 127
    d = np.zeros_like(m)
    d[1:, :] |= m[:-1, :]; d[:-1, :] |= m[1:, :]; d[:, 1:] |= m[:, :-1]; d[:, :-1] |= m[:, 1:]
    if diag:
        d[1:, 1:] |= m[:-1, :-1]; d[:-1, :-1] |= m[1:, 1:]; d[1:, :-1] |= m[:-1, 1:]; d[:-1, 1:] |= m[1:, :-1]
    ring = d & ~m
    o[ring] = (col[0], col[1], col[2], 255)
    return Cv(arr=o)


def light(spr, k=(1, 1, 1), rim=None, rim_side=1, rim_k=0.55, keep=None):
    """multiply sprite colors by k; rim light on side (+1 right, -1 left). keep: list of colors not multiplied."""
    a = spr.a.copy()
    m = a[..., 3] > 127
    rgb = a[..., :3].astype(np.float32)
    km = np.array(k, np.float32)
    res = rgb * km
    if keep:
        kmask = np.zeros(m.shape, bool)
        for c in keep:
            kmask |= (a[..., 0] == c[0]) & (a[..., 1] == c[1]) & (a[..., 2] == c[2])
        res[kmask] = rgb[kmask] * np.maximum(km, 0.85)
    if rim is not None:
        e = np.zeros_like(m)
        if rim_side > 0:
            e[:, :-1] = m[:, :-1] & ~m[:, 1:]
            e[:, -1] = m[:, -1]
        else:
            e[:, 1:] = m[:, 1:] & ~m[:, :-1]
            e[:, 0] = m[:, 0]
        # skip outline color
        isout = (a[..., 0] == OUT[0]) & (a[..., 1] == OUT[1]) & (a[..., 2] == OUT[2])
        e &= ~isout
        # step one pixel inward if edge pixel is outline
        rimc = np.array(rim, np.float32)
        res[e] = res[e] * (1 - rim_k) + rimc * rim_k
    a[..., :3] = np.clip(res, 0, 255).astype(np.uint8)
    return Cv(arr=a)


def silhouette(spr, col):
    a = spr.a.copy()
    m = a[..., 3] > 127
    a[m, :3] = col
    return Cv(arr=a)


# ---------------------------------------------------------------- gradients / dither fills
def vgrad(c, y0, y1, cols, ox=0, x0=0, x1=None):
    """vertical gradient from y0..y1 through list of colors, ordered dither between steps."""
    x1 = c.w if x1 is None else x1
    n = len(cols) - 1
    hgt = y1 - y0
    if hgt <= 0:
        return
    t = (np.arange(hgt, dtype=np.float32) + 0.5) / hgt * n  # 0..n
    b = bayer(hgt, x1 - x0, x0 + ox, y0)
    v = t[:, None] + (b - 0.5)
    idx = np.clip(np.floor(v + 0.5), 0, n).astype(int)
    pal = np.array(cols, np.uint8)
    yy0, yy1 = max(0, y0), min(c.h, y1)
    c.a[yy0:yy1, x0:x1, :3] = pal[idx[yy0 - y0:yy1 - y0]]


def dither_blend(a, b, f, ox=0, oy=0):
    """per-pixel choose b where bayer<f. a,b HxWx3 arrays; f scalar or HxW."""
    h, w = a.shape[:2]
    m = bayer(h, w, ox, oy) < f
    out = a.copy()
    out[m] = b[m]
    return out


# ---------------------------------------------------------------- color grading
WARM_RAMP = [hx('#3e2226'), hx('#7a3a2e'), hx('#b8643c'), hx('#e3995e'), hx('#f6c890'), hx('#fde9c6')]
ICE = [hx('#141a2e'), hx('#22304e'), hx('#34507a'), hx('#5276a4'), hx('#7ea2c8'), hx('#b4cce2'), hx('#e2eef6')]


def lum(a):
    return (a[..., 0] * 0.299 + a[..., 1] * 0.587 + a[..., 2] * 0.114) / 255.0


def ramp_map(a, ramp, dither=True):
    L = lum(a.astype(np.float32))
    n = len(ramp) - 1
    v = L * n
    if dither:
        v = v + (bayer(a.shape[0], a.shape[1]) - 0.5) * 0.9
    idx = np.clip(np.round(v), 0, n).astype(int)
    return np.array(ramp, np.uint8)[idx]


def grade_warm(a, k=0.38):
    r = ramp_map(a, WARM_RAMP, dither=False).astype(np.float32)
    out = a.astype(np.float32) * (1 - k) + r * k
    # warm bias
    out[..., 0] *= 1.04; out[..., 2] *= 0.9
    return np.clip(out, 0, 255).astype(np.uint8)


def is_red(a):
    r, g, b = a[..., 0].astype(int), a[..., 1].astype(int), a[..., 2].astype(int)
    return (r > 120) & (r > g * 1.7) & (r > b * 1.5)


def grade_ice(a, keep_red=True):
    out = ramp_map(a, ICE, dither=False)
    if keep_red:
        m = is_red(a)
        out[m] = a[m]
    return out


def grade_mul(a, k):
    return np.clip(a.astype(np.float32) * np.array(k, np.float32), 0, 255).astype(np.uint8)


def vignette(a, strength=0.5, col=(20, 12, 16)):
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
    f = np.clip((d - 0.78) / 0.5, 0, 1) * strength
    m = bayer(h, w) < f
    out = a.copy()
    out[m] = col
    return out


def darken_flat(a, k=0.4):
    return (a.astype(np.float32) * k).astype(np.uint8)


# ---------------------------------------------------------------- text
_UNI = None
_GLY = {}
FONT_DIR = _os.environ.get('MV_FONT_DIR', _os.path.join(_ROOT, 'fonts'))
FONT_UNI = _os.path.join(FONT_DIR, 'unifont.ttf')
FONT_FP = _os.path.join(FONT_DIR, 'fp12') + '/'


def _uni_glyph(ch):
    global _UNI
    key = ('u', ch)
    if key in _GLY:
        return _GLY[key]
    if _UNI is None:
        _UNI = ImageFont.truetype(FONT_UNI, 16)
    im = Image.new('L', (20, 18), 0)
    d = ImageDraw.Draw(im)
    d.fontmode = '1'
    d.text((0, 0), ch, font=_UNI, fill=255)
    m = np.array(im) > 127
    adv = int(round(_UNI.getlength(ch)))
    g = (m[:16, :max(adv, 1)], adv)
    _GLY[key] = g
    return g


_FPMAP = None
_FPF = {}


def _wqy_glyph(ch):
    """12px small font: Fusion Pixel 12px proportional (zh_hans). returns (13-row bool box, advance)."""
    global _FPMAP
    key = ('w', ch)
    if key in _GLY:
        return _GLY[key]
    if _FPMAP is None:
        import json
        _FPMAP = {int(k): FONT_FP + v.split('/')[-1] for k, v in json.load(open(FONT_FP + 'cmap.json')).items()}
    path = _FPMAP.get(ord(ch)) or _FPMAP.get(ord('?'))
    if path not in _FPF:
        _FPF[path] = ImageFont.truetype(path, 12)
    f = _FPF[path]
    im = Image.new('L', (24, 16), 0)
    d = ImageDraw.Draw(im)
    d.fontmode = '1'
    d.text((0, -2), ch, font=f, fill=255)
    m = np.array(im) > 127
    adv = int(round(f.getlength(ch)))
    g = (m[:13, :max(adv, 1)], adv)
    _GLY[key] = g
    return g


def glyph(ch, font='u'):
    return _uni_glyph(ch) if font == 'u' else _wqy_glyph(ch)


def text_w(s, font='u', sp=0):
    return sum(glyph(ch, font)[1] + sp for ch in s) - (sp if s else 0)


def text(c, x, y, s, col, font='u', sp=0, shadow=None, outline_col=None, upto=None, col2=None, split=None):
    """draw text at (x,y) top-left. upto: number of chars to draw (typing). chars >= split drawn in col2."""
    items = []
    xx = int(x)
    for i, ch in enumerate(s):
        if upto is not None and i >= upto:
            break
        m, adv = glyph(ch, font)
        items.append((i, m, xx))
        xx += adv + sp
    if outline_col is not None:
        for i, m, gx in items:
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
                c.mask_fill(m, outline_col, gx + dx, y + dy)
    if shadow is not None:
        for i, m, gx in items:
            c.mask_fill(m, shadow, gx + 1, y + 1)
    for i, m, gx in items:
        cc = col if (split is None or i < split) else col2
        c.mask_fill(m, cc, gx, y)
    return xx


def text_big(c, x, y, s, col, k=4, font='u', outline_col=None, sp=0):
    """integer-scaled glyph text (chunky pixel title)."""
    xx = int(x)
    for ch in s:
        m, adv = glyph(ch, font)
        mk = np.repeat(np.repeat(m, k, 0), k, 1)
        if outline_col is not None:
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
                c.mask_fill(mk, outline_col, xx + dx, y + dy)
        c.mask_fill(mk, col, xx, y)
        xx += adv * k + sp
    return xx


# ---------------------------------------------------------------- small numerics
def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ease_out(x):
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


def ease_in(x):
    x = min(1.0, max(0.0, x))
    return x ** 3


def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def seg(t, a, b):
    """0..1 progress of t in [a,b]."""
    if b <= a:
        return 1.0 if t >= b else 0.0
    return clamp((t - a) / (b - a))


def rng(seed):
    return np.random.default_rng(seed)


def upscale(a, k=S):
    return np.repeat(np.repeat(a, k, 0), k, 1)
