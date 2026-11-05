# -*- coding: utf-8 -*-
"""Stroke-order handwriting from Make Me a Hanzi data (graphics.txt, Arphic Public License)."""
import json
import os
import re
import functools
import numpy as np
import skia

HERE = os.path.dirname(os.path.abspath(__file__))
# {char: {"m": medians, "s": stroke outlines}} built by build_strokes.py. Loaded on first use (or assign hanzi.DATA).
DATA = None


def _data():
    global DATA
    if DATA is None:
        path = os.environ.get('MV_STROKES', os.path.join(HERE, 'strokes.json'))
        if not os.path.exists(path):
            raise FileNotFoundError('stroke data missing: %s (make it with build_strokes.py, or set MV_STROKES)' % path)
        DATA = json.load(open(path, encoding='utf-8'))
    return DATA


def _svg_path(d):
    p = skia.Path()
    tok = re.findall(r'[MLQCZ]|-?\d+(?:\.\d+)?', d)
    i, cmd = 0, None
    while i < len(tok):
        t = tok[i]
        if t in 'MLQCZ':
            cmd = t
            i += 1
            if cmd == 'Z':
                p.close()
            continue
        n = {'M': 2, 'L': 2, 'Q': 4, 'C': 6}[cmd]
        v = [float(x) for x in tok[i:i + n]]
        i += n
        if cmd == 'M':
            p.moveTo(*v)
            cmd = 'L'
        elif cmd == 'L':
            p.lineTo(*v)
        elif cmd == 'Q':
            p.quadTo(*v)
        else:
            p.cubicTo(*v)
    return p


@functools.lru_cache(maxsize=None)
def glyph(ch):
    """returns list of strokes: (outline_path in 1024-box screen orientation, median Nx2 array, length)"""
    d = _data().get(ch)
    if d is None:
        return []
    m = skia.Matrix()
    m.setScale(1, -1)
    m.postTranslate(0, 900)
    out = []
    for st, med in zip(d['s'], d['m']):
        p = _svg_path(st)
        p.transform(m)
        a = np.array([[x, 900 - y] for x, y in med], np.float64)
        L = float(np.sum(np.hypot(*np.diff(a, axis=0).T))) if len(a) > 1 else 1.0
        out.append((p, a, max(L, 20.0)))
    return out


def char_len(ch):
    return sum(L for _, _, L in glyph(ch)) or 1.0


def partial_polyline(a, u):
    """first fraction u of polyline a"""
    if u >= 1:
        return a
    seg = np.hypot(*np.diff(a, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    target = cum[-1] * max(0.0, u)
    k = int(np.searchsorted(cum, target))
    if k <= 0:
        return a[:1]
    t = (target - cum[k - 1]) / max(1e-9, seg[k - 1])
    return np.vstack([a[:k], a[k - 1] + (a[k] - a[k - 1]) * t])


def poly_path(a, x0, y0, k):
    p = skia.Path()
    for i, (px, py) in enumerate(a):
        X, Y = x0 + px * k, y0 + py * k
        p.moveTo(X, Y) if i == 0 else p.lineTo(X, Y)
    if len(a) == 1:
        p.lineTo(x0 + a[0][0] * k + 0.01, y0 + a[0][1] * k)
    return p


def write_char(c, ch, x0, y0, size, prog, paints, mode='finger'):
    """Draw character ch (top-left x0,y0, em size) written up to prog in [0,1] in stroke order.
    paints: list of Paints applied per stroke (outer to inner)."""
    strokes = glyph(ch)
    if not strokes or prog <= 0:
        return
    k = size / 1024.0
    total = sum(L for _, _, L in strokes)
    done = prog * total
    for path, med, L in strokes:
        if done <= 0:
            break
        u = min(1.0, done / L)
        done -= L
        pp = poly_path(partial_polyline(med, u), x0, y0, k)
        if mode == 'finger':
            for pf in paints:
                c.drawPath(pp, pf)
        else:   # brush: reveal the real stroke outline along the median
            c.save()
            m = skia.Matrix()
            m.setScale(k, k)
            m.postTranslate(x0, y0)
            op = skia.Path(path)
            op.transform(m)
            if u < 1:
                mask = skia.Paint()
                mask.setStyle(skia.Paint.kStroke_Style)
                mask.setStrokeWidth(size * 0.16)
                mask.setStrokeCap(skia.Paint.kRound_Cap)
                mk = skia.Path()
                mask.getFillPath(pp, mk)
                op = skia.Op(op, mk, skia.PathOp.kIntersect_PathOp) or op
            for pf in paints:
                c.drawPath(op, pf)
            c.restore()


def head_point(ch, prog):
    """current pen position (1024-box coords) at writing progress prog, or None."""
    strokes = glyph(ch)
    if not strokes or prog <= 0 or prog >= 1:
        return None
    total = sum(L for _, _, L in strokes)
    done = prog * total
    for path, med, L in strokes:
        if done <= L:
            return partial_polyline(med, done / L)[-1]
        done -= L
    return None
