# -*- coding: utf-8 -*-
"""画面里的歌词：粉笔 / 铅笔 / 手指在雾玻璃上写字。字随演唱逐字写出（时间来自 audio/lyrics.json）。"""
import json, os, math
import numpy as np
from px import glyph, hx, mix

HERE = os.path.dirname(os.path.abspath(__file__))
LY = json.load(open(os.path.join(HERE, '..', 'audio', 'lyrics.json'), encoding='utf-8'))


def L(prefix):
    for ln in LY:
        if ln[2].startswith(prefix):
            return ln
    raise KeyError(prefix)


def units(s):
    """writing units: CJK chars one by one; 注音 tokens (space separated) as one unit."""
    if 'ㄙ' in s or 'ㄖ' in s or 'ㄌ' in s:
        return s.split(' ')
    return [ch for ch in s if ch != ' ']


def progress(t, ln, per=0.27, frac=0.82):
    """number of units written at time t (0 before the line starts)."""
    a, b, s = ln[0], ln[1], ln[2]
    u = units(s)
    n = len(u)
    if t < a:
        return 0, 0.0
    dur = max(0.25, min((b - a) * frac, per * n))
    x = (t - a) / dur * n
    k = min(n, int(x) + 1)
    return k, (x - int(x)) if k < n else 1.0


def rows_of(s, per_row):
    u = units(s)
    rows = []
    for i in range(0, len(u), per_row):
        rows.append(u[i:i + per_row])
    return rows


def _mask(ch, font, k):
    m, adv = glyph(ch, font)
    if k > 1:
        m = np.repeat(np.repeat(m, k, 0), k, 1)
    return m, adv * k


def write(c, x, y, ln, t, col, font='u', k=1, per_row=99, row_h=None, style='chalk', seed=0, fresh=None,
          sp=0, align='left', width=None):
    """draw the line ln progressively. style: chalk (dropout texture) / pencil / plain. returns (x_end, y_end, n)."""
    n, frac = progress(t, ln)
    rows = rows_of(ln[2], per_row)
    gh = (16 if font == 'u' else 13) * k
    row_h = row_h or gh + 2 * k
    fresh = fresh or mix(col, (255, 255, 255), 0.6)
    idx = 0
    xe = x
    for r, row in enumerate(rows):
        yy = y + r * row_h
        # row width for centering
        if align == 'center' and width:
            tw = 0
            for u in row:
                for ch in u:
                    tw += glyph(ch, font)[1] * k + sp
            xx = x + (width - tw) // 2
        else:
            xx = x
        for ui, u in enumerate(row):
            if idx >= n:
                return xe, yy, n
            newest = idx == n - 1 and frac < 1.0
            for ch in u:
                m, adv = _mask(ch, font, k)
                mm = m
                if style == 'chalk':
                    rr = np.random.default_rng(seed * 977 + idx * 31 + ord(ch))
                    mm = m & (rr.random(m.shape) > 0.16)
                    if newest:  # the stroke being written: draw only the top part
                        cut = max(1, int(m.shape[0] * min(1.0, 0.35 + frac * 1.3)))
                        mm = mm.copy(); mm[cut:] = False
                elif style == 'pencil':
                    rr = np.random.default_rng(seed * 577 + idx * 17 + ord(ch))
                    mm = m & (rr.random(m.shape) > 0.06)
                    if newest:
                        cut = max(1, int(m.shape[1] * min(1.0, 0.3 + frac * 1.4)))
                        mm = mm.copy(); mm[:, cut:] = False
                c.mask_fill(mm, fresh if newest else col, xx, yy)
                xx += adv + sp
            if ui < len(row) - 1 and len(u) > 1:  # 注音 token gap
                xx += 5 * k
            idx += 1
            xe = xx
    return xe, y + (len(rows) - 1) * row_h, n


def text_mask(s, font='u', k=1, sp=0):
    """bool mask of a whole string (for writing on fogged glass)."""
    ms = [_mask(ch, font, k) for ch in s]
    w = sum(a for _, a in ms) + sp * len(ms)
    h = ms[0][0].shape[0] if ms else 1
    out = np.zeros((h, max(w, 1)), bool)
    x = 0
    pos = []
    for m, adv in ms:
        out[:m.shape[0], x:x + m.shape[1]] |= m
        pos.append(x)
        x += adv + sp
    return out, pos
