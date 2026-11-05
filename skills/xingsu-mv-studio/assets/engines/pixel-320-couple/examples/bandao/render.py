# -*- coding: utf-8 -*-
"""Timeline renderer for 《半岛铁盒》: frame(t) -> 320x180 RGB; full-res = x8 (2560x1440)."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from px import Cv, W, H, S, bayer, upscale, seg
import story
from shots import IMPL, strip_mix
from ui import karaoke, vcr

FPS = 24
DUR = story.DUR - story.SONG_START
LEAD = 2 / 24.0
HERE = os.path.dirname(os.path.abspath(__file__))
LY = json.load(open(os.path.join(HERE, '..', 'audio', 'lyrics_chars.json'), encoding='utf-8'))
SH = story.SHOTS


def shot_at(tv):
    for i, s in enumerate(SH):
        if s[1] <= tv < s[2]:
            return i
    return len(SH) - 1 if tv >= SH[-1][1] else 0


def render_shot(i, tv):
    return IMPL[SH[i][8]](tv)


def lyric_at(tv):
    for k, ln in enumerate(LY):
        a, b = ln[0], ln[1]
        nxt = LY[k + 1][0] if k + 1 < len(LY) else 1e9
        end = min(b + 0.35, nxt - 0.05)
        if a - 0.12 <= tv < end:
            alpha = min(1.0, (tv - (a - 0.12)) / 0.1, (end - tv) / 0.1)
            return ln, alpha
    return None, 0


def frame_small(t):
    """t = video time (seconds from the first video frame)."""
    tv = t + story.SONG_START + LEAD
    i = shot_at(tv)
    s = SH[i]
    c = render_shot(i, tv)
    trans = s[7]
    dt = tv - s[1]
    if i > 0 and dt >= 0:
        if trans == 'tear' and dt < 6 / FPS:
            prev = render_shot(i - 1, tv)
            c = Cv(arr=strip_mix(prev.a, c.a, dt / (6 / FPS), seed=i))
        elif trans == 'flash' and dt < 2 / FPS:
            c.a[:] = (255, 255, 255)
        elif trans == 'glitch' and dt < 3 / FPS:
            vcr(c, tv, label=None, noise=2.5, seed=i)
    if s[0].startswith('S'):
        ln, al = lyric_at(tv)
        if ln is not None and al > 0:
            karaoke(c, tv, ln, y=158, lead=0.0, alpha=al)
    return c.a


def frame(t):
    return upscale(frame_small(t), S)


class Renderer:
    def __init__(self, cache_dir=None):
        pass

    def frame(self, t):
        a = frame(t)
        out = np.empty((a.shape[0], a.shape[1], 4), np.uint8)
        out[..., 0] = a[..., 2]; out[..., 1] = a[..., 1]; out[..., 2] = a[..., 0]; out[..., 3] = 255
        return out


W_OUT, H_OUT = W * S, H * S
