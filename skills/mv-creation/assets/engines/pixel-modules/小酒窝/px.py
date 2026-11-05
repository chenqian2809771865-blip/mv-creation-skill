# 像素画布工具：320x180 逻辑网格，最近邻 x8 输出 2560x1440
import json, math, functools, os
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, SCALE = 320, 180, 24, 8
FONTS = str(Path(os.environ.get('MV_FONT_DIR', Path(__file__).resolve().parent.parent / 'fonts'))) + os.sep
OUT = (29, 24, 40)

U16 = ImageFont.truetype(FONTS + 'unifont.ttf', 16)
U32 = ImageFont.truetype(FONTS + 'unifont.ttf', 32)
_FPIDX = {int(k): FONTS + v for k, v in json.load(open(FONTS + 'fp12/index.json')).items()}

@functools.lru_cache(None)
def _fp(path):
    return ImageFont.truetype(path, 12)

def fp_font(ch):
    p = _FPIDX.get(ord(ch))
    return _fp(p) if p else None

# ---------- text ----------
def text_w(s, size=12):
    if size == 16: return int(U16.getlength(s))
    if size == 32: return int(U32.getlength(s))
    w = 0
    for ch in s:
        f = fp_font(ch)
        w += int(f.getlength(ch)) if f else int(U16.getlength(ch) * .75)
    return w

def text(d, xy, s, fill, size=12, outline=None):
    """像素字，fontmode 1；outline 给 1px 描边色"""
    d.fontmode = '1'
    x, y = xy
    if outline is not None:
        for dx, dy in ((-1,0),(1,0),(0,-1),(0,1),(-1,-1),(1,1),(-1,1),(1,-1)):
            text(d, (x+dx, y+dy), s, outline, size)
    if size in (16, 32):
        d.text((x, y), s, font=U16 if size == 16 else U32, fill=fill)
        return
    for ch in s:
        f = fp_font(ch) or U16
        d.text((x, y), ch, font=f, fill=fill)
        x += int(f.getlength(ch))

def text_c(d, cx, y, s, fill, size=12, outline=None):
    text(d, (cx - text_w(s, size) // 2, y), s, fill, size, outline)

PUNCT = '，。！？、…~～）」!?,.☺♥☾'
def wrap(s, maxw, size=12):
    lines, cur = [], ''
    for ch in s:
        if ch == '\n':
            lines.append(cur); cur = ''; continue
        if text_w(cur + ch, size) > maxw and cur and ch not in PUNCT:
            lines.append(cur); cur = ch
        else:
            cur += ch
    if cur: lines.append(cur)
    return lines

# ---------- math ----------
def clamp(x, a=0., b=1.): return max(a, min(b, x))
def lerp(a, b, k): return a + (b - a) * k
def ease(x): x = clamp(x); return x * x * (3 - 2 * x)
def eout(x): x = clamp(x); return 1 - (1 - x) ** 3
def ein(x): x = clamp(x); return x ** 3
def back(x, s=1.7):
    x = clamp(x) - 1; return 1 + x * x * ((s + 1) * x + s)
def prog(t, a, b): return clamp((t - a) / (b - a)) if b > a else float(t >= a)
def lc(c1, c2, k): return tuple(int(round(a + (b - a) * k)) for a, b in zip(c1, c2))
def mulc(c, m): return tuple(int(clamp(v * mm, 0, 255)) for v, mm in zip(c, m if isinstance(m, (tuple, list)) else (m, m, m)))
def hexc(h): h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16 + 1 / 32
def bayer(w, h, ox=0, oy=0):
    return np.tile(BAYER, (h // 4 + 2, w // 4 + 2))[oy % 4:oy % 4 + h, ox % 4:ox % 4 + w]

def rng(seed): return np.random.default_rng(seed)

# ---------- images ----------
def new(w=W, h=H, c=(0, 0, 0)): return Image.new('RGB', (w, h), c)
def newa(w, h): return Image.new('RGBA', (w, h), (0, 0, 0, 0))
def dr(im): d = ImageDraw.Draw(im); d.fontmode = '1'; return d

def vgrad(w, h, stops, dither=True, oy=0):
    """竖直渐变：stops=[(pos0..1, color), ...]，有序抖动成色带"""
    ys = (np.arange(h) + oy) / max(1, h - 1)
    pos = np.array([s[0] for s in stops]); cols = np.array([s[1] for s in stops], float)
    out = np.zeros((h, w, 3), np.uint8)
    nb = 6  # 每段色带数
    for i in range(len(stops) - 1):
        a, b = pos[i], pos[i + 1]
        m = (ys >= a) & (ys <= b)
        if not m.any(): continue
        k = (ys[m] - a) / max(1e-6, b - a)
        if dither:
            kk = k[:, None] * nb + bayer(w, int(m.sum()), 0, 0) - .5
            kk = np.clip(np.round(kk), 0, nb) / nb
            c = cols[i][None, None] + (cols[i + 1] - cols[i])[None, None] * kk[..., None]
        else:
            c = np.broadcast_to((cols[i] + (cols[i + 1] - cols[i]) * k[:, None])[:, None], (int(m.sum()), w, 3))
        out[m] = np.round(c).astype(np.uint8)
    return Image.fromarray(out)

def outline_rgba(im, col=OUT, inner=False):
    """给 RGBA 精灵加 1px 外轮廓"""
    a = np.array(im)
    m = a[..., 3] > 0
    p = np.pad(m, 1)
    d = p[:-2, 1:-1] | p[2:, 1:-1] | p[1:-1, :-2] | p[1:-1, 2:]
    o = d & ~m
    a[o] = (*col, 255)
    return Image.fromarray(a)

def tint(im, m=(1, 1, 1), add=(0, 0, 0)):
    a = np.array(im).astype(np.float32)
    a[..., :3] = np.clip(a[..., :3] * np.array(m) + np.array(add), 0, 255)
    return Image.fromarray(a.astype(np.uint8), im.mode)

def paste(base, spr, x, y, flip=False):
    """把 RGBA 精灵按左上角贴到底图（整数坐标）"""
    if flip: spr = spr.transpose(Image.FLIP_LEFT_RIGHT)
    base.paste(spr, (int(round(x)), int(round(y))), spr)

def darken(im, k=.4, col=(0, 0, 0)):
    a = np.array(im).astype(np.float32)
    a = a * k + np.array(col) * (1 - k)
    return Image.fromarray(a.astype(np.uint8))

def dither_mix(a, b, k, ox=0, oy=0):
    """按比例 k 以有序抖动把 b 混进 a（两图同尺寸 RGB）"""
    A, B = np.array(a), np.array(b)
    m = bayer(A.shape[1], A.shape[0], ox, oy) < k
    A[m] = B[m]
    return Image.fromarray(A)

# ---------- small icons (像素小图标) ----------
HEART = ["0110110", "1111111", "1111111", "0111110", "0011100", "0001000"]
HEART_S = ["01010", "11111", "01110", "00100"]
SPARK = ["00100", "00100", "11011", "00100", "00100"]
SPARK_S = ["010", "101", "010"]
NOTE = ["0011", "0010", "0010", "1110", "1110"]
DROP = ["010", "111", "111", "010"]
def icon(d, x, y, pat, col, outline=None):
    if outline is not None:
        for dy, row in enumerate(pat):
            for dx, ch in enumerate(row):
                if ch == '1':
                    for ex, ey in ((-1,0),(1,0),(0,-1),(0,1)):
                        d.point((x + dx + ex, y + dy + ey), fill=outline)
    for dy, row in enumerate(pat):
        for dx, ch in enumerate(row):
            if ch == '1': d.point((x + dx, y + dy), fill=col)

def heart(d, cx, cy, size, col, outline=OUT):
    """可缩放像素心（size 为半宽）"""
    pts = []
    for yy in range(-size, size + 2):
        for xx in range(-size - 1, size + 2):
            X, Y = xx / (size + .5), -yy / (size + .5)
            if (X * X + Y * Y - 1) ** 3 - X * X * Y ** 3 <= 0:
                pts.append((cx + xx, cy + yy))
    S = set(pts)
    if outline is not None:
        for (x, y) in pts:
            for ex, ey in ((-1,0),(1,0),(0,-1),(0,1)):
                if (x + ex, y + ey) not in S: d.point((x + ex, y + ey), fill=outline)
    for p in pts: d.point(p, fill=col)
    if size >= 3:
        d.point((cx - size // 2 - 1, cy - size // 2), fill=lc(col, (255, 255, 255), .6))

# ---------- upscale & output ----------
def up(img, zoom=1.0, cx=W / 2, cy=H / 2, ox=0, oy=0):
    """逻辑画布 → 2560x1440；zoom>1 时按最近邻裁切放大（镜头推近）"""
    a = np.asarray(img.convert('RGB'))
    if zoom == 1.0 and ox == 0 and oy == 0:
        return a.repeat(SCALE, 0).repeat(SCALE, 1)
    OW, OH = W * SCALE, H * SCALE
    s = SCALE * zoom
    xs = ((np.arange(OW) + .5 - OW / 2) / s + cx + ox).astype(np.int32)
    ys = ((np.arange(OH) + .5 - OH / 2) / s + cy + oy).astype(np.int32)
    xs = np.clip(xs, 0, W - 1); ys = np.clip(ys, 0, H - 1)
    return a[ys][:, xs]

def over(big, ui, alpha=1.0):
    """RGBA 320x180 叠加层 ×8 叠到大图"""
    u = np.asarray(ui)
    if not u[..., 3].any(): return big
    u = u.repeat(SCALE, 0).repeat(SCALE, 1)
    a = (u[..., 3:4].astype(np.float32) / 255) * alpha
    return (big * (1 - a) + u[..., :3] * a).astype(np.uint8)
