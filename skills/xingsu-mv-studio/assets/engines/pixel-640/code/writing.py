# -*- coding: utf-8 -*-
"""Finger-on-fog handwriting with real stroke order (Make Me a Hanzi medians)."""
import json, math, os, functools
import numpy as np
from core import *

STROKES = json.load(open(os.path.join(ASSETS, 'strokes.json'), encoding='utf-8'))


def _dense(pts, step=1.0):
    out = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
        L = math.hypot(x1 - x0, y1 - y0)
        n = max(1, int(L / step))
        for i in range(1, n + 1):
            out.append((x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n))
    return out


def char_polylines(ch, cx, cy, size):
    d = STROKES[ch]
    s = size / 1024.0
    out = []
    for med in d['m']:
        pts = [(cx + (x - 512) * s, cy + (900 - y - 512) * s + size * 0.06) for x, y in med]
        out.append(_dense(pts))
    return out


class Writer:
    def __init__(self, layout, t0, t1, width=7, lift=0.22):
        """layout: list of (ch, cx, cy, size). Strokes drawn sequentially between t0 and t1."""
        self.strokes = []
        for ch, cx, cy, size in layout:
            for pl in char_polylines(ch, cx, cy, size):
                self.strokes.append(pl)
        L = [len(p) for p in self.strokes]
        total = sum(L)
        n = len(self.strokes)
        dur = t1 - t0
        lift_t = dur * lift / max(1, n - 1)
        draw_t = dur * (1 - lift)
        t = t0
        self.sched = []
        for i, p in enumerate(self.strokes):
            dt = draw_t * len(p) / total
            self.sched.append((t, t + dt))
            t += dt + (lift_t if i < n - 1 else 0)
        self.width = width
        self.t0, self.t1 = t0, t1
        self._cache = {}

    def state(self, t, w=W, h=H):
        """returns (mask, fingertip(x,y) or None, touching)"""
        key = round(t * 48)
        if key in self._cache:
            return self._cache[key]
        im = Image.new('L', (w, h), 0)
        d = ImageDraw.Draw(im)
        tip, touching = None, False
        r = self.width / 2
        for i, (p, (a, b)) in enumerate(zip(self.strokes, self.sched)):
            if t < a:
                if tip is None and i > 0:
                    # lifting between strokes: interpolate from previous end to this start
                    pa, pb = self.sched[i - 1][1], a
                    u = ease(seg(t, pa, pb))
                    q0, q1 = self.strokes[i - 1][-1], p[0]
                    tip = (q0[0] + (q1[0] - q0[0]) * u, q0[1] + (q1[1] - q0[1]) * u - math.sin(u * math.pi) * 8)
                break
            k = len(p) if t >= b else max(1, int(len(p) * ease_out(seg(t, a, b)) if False else len(p) * seg(t, a, b)))
            pts = [(round(x), round(y)) for x, y in p[:k]]
            if len(pts) > 1:
                d.line(pts, fill=255, width=int(self.width), joint='curve')
            for (x, y) in (pts[0], pts[-1]):
                d.ellipse([x - r, y - r, x + r - 1, y + r - 1], fill=255)
            if t < b:
                tip = p[k - 1]
                touching = True
        m = np.asarray(im) > 0
        if tip is None and t < self.t0:
            tip = self.strokes[0][0]
        res = (m, tip, touching)
        if len(self._cache) > 200:
            self._cache.clear()
        self._cache[key] = res
        return res

    def bottoms(self, n_chars_layout):
        """lowest point of each char (for drips)"""
        return None
