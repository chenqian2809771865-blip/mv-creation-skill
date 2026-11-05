# -*- coding: utf-8 -*-
"""frame(t) for the whole film + karaoke lyrics + encoder.
usage: python3 render.py out.mp4 SCALE [T0 T1] [--procs N]"""
import sys, os, math, importlib, subprocess, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from core import *
from story import SHOTS

DUR = TIMING['end']
LYR = TIMING['lyrics']

_reg = {}


def shot_fn(sid):
    if sid in _reg:
        return _reg[sid]
    fn = None
    for modname in ('shot_intro', 'shots_v1', 'shots_c1', 'shots_c2'):
        try:
            m = importlib.import_module(modname)
        except ModuleNotFoundError:
            continue
        if sid == 'S01' and modname == 'shot_intro':
            fn = lambda t, lt, d, m=m: m.frame(t)
            break
        f = getattr(m, sid, None)
        if f is not None:
            fn = f
            break
    _reg[sid] = fn
    return fn


def placeholder(sid, t):
    img = new((30, 30, 40))
    draw_text(img, sid, 320, 170, (200, 200, 220), anchor='mm')
    return img


# ---------------- karaoke ----------------
SUNG = (255, 212, 104)
UNSUNG = (240, 242, 250)
OUTL = (22, 20, 34)
LEAD = 0.083


def lyrics(img, t):
    for L in LYR:
        t0, t1 = L['t0'] - 0.25, L['t1'] + 0.15
        if not (t0 <= t < t1):
            continue
        a = 1.0
        if t < t0 + 0.08:
            a = 0.5
        elif t > t1 - 0.08:
            a = 0.5
        chars = L['chars']
        txt = L['text']
        widths = [glyph_mask(c, 16)[1] for c in txt]
        tw = sum(widths) + (len(txt) - 1) * 1
        x = 320 - tw // 2
        y = 330
        for (ct, ch), wdt in zip(chars, widths):
            col = SUNG if t >= ct - LEAD else UNSUNG
            draw_text(img, ch, x, y, col, outline=OUTL, shadow=OUTL, a=a)
            x += wdt + 1
    return img


def frame(t):
    sid, lt, d = None, 0, 0
    for r in SHOTS:
        if r[1] <= t < r[2]:
            sid, lt, d = r[0], t - r[1], r[2] - r[1]
            break
    if sid is None:
        sid, lt, d = SHOTS[-1][0], t - SHOTS[-1][1], SHOTS[-1][2] - SHOTS[-1][1]
    fn = shot_fn(sid)
    img = fn(t, lt, d) if fn else placeholder(sid, t)
    # two-frame light flash on the first downbeat of each chorus
    for tf in (60.88, 103.56):
        if tf <= t < tf + 2.0 / FPS:
            img = img * 0.55 + np.array([255, 246, 230], np.float32) * 0.45
        elif tf + 2.0 / FPS <= t < tf + 4.0 / FPS:
            img = img * 0.8 + np.array([255, 246, 230], np.float32) * 0.2
    img = lyrics(img, t)
    # global fade to black at the very end (stepped)
    if t > DUR - 1.2:
        k = [1.0, 0.75, 0.5, 0.28, 0.12, 0.0][min(5, int((t - (DUR - 1.2)) / 0.2))]
        img = img * k
    return np.clip(img, 0, 255)


def encode(out, scale=4, t0=0.0, t1=None, crf=16, audio=True, preset='medium'):
    t1 = DUR if t1 is None else t1
    f0, f1 = int(round(t0 * FPS)), int(round(t1 * FPS))
    Wd, Hd = W * scale, H * scale
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (Wd, Hd), '-r', str(FPS), '-i', '-']
    if audio:
        cmd += ['-ss', '%.3f' % t0, '-t', '%.3f' % (t1 - t0), '-i', os.path.join(ASSETS, 'audio_cut.wav')]
    cmd += ['-c:v', 'libx264', '-preset', preset, '-crf', str(crf), '-tune', 'animation', '-profile:v', 'high', '-level:v', '5.1', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
            '-x264-params', 'keyint=48:min-keyint=24:ref=4', '-threads', '2']
    if audio:
        cmd += ['-c:a', 'aac', '-b:a', '256k', '-shortest']
    cmd += ['-movflags', '+faststart', out]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    ts = time.time()
    for f in range(f0, f1):
        img = frame(f / FPS)
        p.stdin.write(upscale(img, scale).tobytes())
        if (f - f0) % 96 == 0:
            el = time.time() - ts
            print('frame %d/%d  %.1fs' % (f, f1, el), flush=True)
    p.stdin.close()
    p.wait()
    print('done', out, time.time() - ts)


if __name__ == '__main__':
    a = sys.argv[1:]
    out = a[0]
    scale = int(a[1]) if len(a) > 1 else 4
    t0 = float(a[2]) if len(a) > 2 else 0.0
    t1 = float(a[3]) if len(a) > 3 else None
    encode(out, scale, t0, t1)
