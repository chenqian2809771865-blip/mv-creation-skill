# -*- coding: utf-8 -*-
"""Timeline renderer for 《晴天》: frame(t) -> 320x180 RGB; full-res = x8 (2560x1440). 画面整体比音频提前 2 帧。"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from px import Cv, W, H, S, upscale
import story
from shots import IMPL, strip_mix
from ui import vcr

FPS = 24
DUR = story.DUR - story.SONG_START
LEAD = 2 / 24.0
SH = story.SHOTS


def shot_at(tv):
    for i, s in enumerate(SH):
        if s[1] <= tv < s[2]:
            return i
    return len(SH) - 1 if tv >= SH[-1][1] else 0


def render_shot(i, tv):
    return IMPL[SH[i][8]](tv)


def frame_small(t):
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
        elif trans == 'flash' and dt < 1 / FPS:
            c.a[:] = (236, 242, 255)
        elif trans == 'glitch' and dt < 3 / FPS:
            vcr(c, tv, label=None, noise=2.5, seed=i)
    return c.a


def frame(t):
    return upscale(frame_small(t), S)
