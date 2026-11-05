# -*- coding: utf-8 -*-
"""涉及 Claude 云端后台时限的说明仅适用于 Claude 桌面版 / 云端会话；其他环境直接写本地文件。
Resumable segmented renderer: frames -> H.264 segments that concat with -c copy into the final master.

usage: python3 mvrun.py WORKDIR [BUDGET_S=6600] [PROCS=2] [CHUNK_FRAMES=240] [T0 T1]
           [--profile master|preview] [--scale N] [--shots shots.json] [--redo T0 T1]
           [--audio song.m4a --out final.mp4] [--status]

WORKDIR/code/render.py must provide FPS, DUR, the output size (OUT_W/OUT_H if defined — the Skia engines keep W/H
for the 1920x1080 logical canvas — else W/H) and Renderer(cache_dir).frame(t) -> uint8 (H, W, 4) BGRA.
Segments: WORKDIR/chunks[_<profile>]/seg_NNNNNN.mp4 (NNNNNN = first frame). Finished segments are skipped, so run
it again (e.g. as a background job, which is killed after 2 h — hence the default 6600 s budget) until ALL DONE.

- Encoding comes from master.py (BT.709 conversion + tags, locked level 5.1). Segments made with the master
  profile ARE the final encode: concatenating with -c copy adds no generation. Preview segments go to a separate
  chunks_preview/ folder so they are never mixed into a master.
- --scale N: nearest-neighbour ×N in ffmpeg (pixel engines render the logical grid, e.g. 640×360 ×4 = 2K, ×6 = 4K).
- --shots: JSON list of shot start times (s); segment boundaries then fall on shot starts, long shots are split
  into CHUNK_FRAMES pieces, so a revision re-renders only the shots it touches.
- --redo T0 T1: delete the segments overlapping [T0, T1] (include transition overlaps) before rendering.
- --audio/--out: when everything is done, write the final file (segments + AAC 320k) and run master.py check.
- --status: print progress from chunks/progress.json and whether the recorded worker pid is still alive
  (use this instead of pgrep -f, which also matches any waiting script that mentions the same words).
"""
import argparse
import glob
import json
import multiprocessing as mp
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import master  # noqa: E402


def plan(total, chunk, shots, fps, f_lo, f_hi):
    """Segment start frames within [f_lo, f_hi): shot starts (if given) plus a split every `chunk` frames."""
    cuts = {0, total}
    if shots:
        cuts |= {min(total, max(0, int(round(s * fps)))) for s in shots}
    cuts = sorted(cuts)
    starts = []
    for a, b in zip(cuts, cuts[1:]):
        starts += list(range(a, b, chunk))
    starts = sorted(set(starts))
    ends = dict(zip(starts, starts[1:] + [total]))
    return [(s, ends[s]) for s in starts if ends[s] > f_lo and s < f_hi]


def out_size(render):
    return getattr(render, 'OUT_W', render.W), getattr(render, 'OUT_H', render.H)


def seg_path(out, f0, part=False):
    return os.path.join(out, 'seg_%06d%s.mp4' % (f0, '.part' if part else ''))


def worker(wid, code, out, queue, est, deadline, lock, profile, scale, progress):
    sys.path.insert(0, code)
    import render  # imported after fork
    r = render.Renderer(cache_dir=out)
    while True:
        try:
            f0, f1 = queue.get_nowait()
        except Exception:
            return
        with lock:
            per_frame = est.value
        if time.time() + per_frame * (f1 - f0) > deadline:
            return
        tmp = seg_path(out, f0, True)
        p = master.open_encoder(tmp, *out_size(render), render.FPS, profile=profile, scale=scale, threads=2)
        t0 = time.time()
        for f in range(f0, f1):
            p.stdin.write(r.frame(f / render.FPS).tobytes())
        p.stdin.close()
        if p.wait() != 0:
            print('[w%d] ffmpeg failed at frame %d' % (wid, f0), flush=True)
            return
        os.replace(tmp, seg_path(out, f0))
        dt = time.time() - t0
        with lock:
            est.value = max(est.value * 0.5, dt / (f1 - f0) * 1.15)
            progress(f1 - f0, dt)
        print('[w%d] frames %d-%d  %.1fs (%.2fs/frame)' % (wid, f0, f1 - 1, dt, dt / (f1 - f0)), flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('workdir')
    ap.add_argument('budget', nargs='?', type=float, default=6600)
    ap.add_argument('procs', nargs='?', type=int, default=2)
    ap.add_argument('chunk', nargs='?', type=int, default=240)
    ap.add_argument('t0', nargs='?', type=float)
    ap.add_argument('t1', nargs='?', type=float)
    ap.add_argument('--profile', choices=sorted(master.PROFILES), default='master')
    ap.add_argument('--scale', type=int, default=1)
    ap.add_argument('--shots')
    ap.add_argument('--redo', nargs=2, type=float, metavar=('T0', 'T1'))
    ap.add_argument('--audio')
    ap.add_argument('--out')
    ap.add_argument('--status', action='store_true')
    a = ap.parse_args()

    start = time.time()
    work = os.path.abspath(a.workdir)
    code = os.path.join(work, 'code')
    out = os.path.join(work, 'chunks' if a.profile == 'master' else 'chunks_' + a.profile)
    prog_file = os.path.join(out, 'progress.json')
    if a.status:
        if not os.path.exists(prog_file):
            sys.exit('no progress.json in ' + out)
        st = json.load(open(prog_file))
        try:
            os.kill(st['pid'], 0)
            alive = True
        except OSError:
            alive = False
        print(json.dumps(dict(st, running=alive), ensure_ascii=False, indent=1))
        return

    os.makedirs(out, exist_ok=True)
    for f in glob.glob(os.path.join(out, '*.part.mp4')):
        os.remove(f)
    sys.path.insert(0, code)
    import render
    total = int(round(render.DUR * render.FPS))
    shots = json.load(open(a.shots)) if a.shots else None
    f_lo = 0 if a.t0 is None else int(a.t0 * render.FPS)
    f_hi = total if a.t1 is None else min(total, int(round(a.t1 * render.FPS)))
    segs = plan(total, a.chunk, shots, render.FPS, f_lo, f_hi)
    if a.redo:
        r0, r1 = (int(x * render.FPS) for x in a.redo)
        for s, e in plan(total, a.chunk, shots, render.FPS, r0, r1 + 1):
            if os.path.exists(seg_path(out, s)):
                os.remove(seg_path(out, s))
                print('removed segment %d-%d for redo' % (s, e - 1))
    # segments from an older plan (different chunk/shots) would overlap: refuse to mix them
    valid = {s for s, _ in plan(total, a.chunk, shots, render.FPS, 0, total)}
    stray = [p for p in glob.glob(os.path.join(out, 'seg_*.mp4'))
             if int(os.path.basename(p)[4:10]) not in valid]
    if stray:
        sys.exit('segments from a different chunk/shot plan exist (%d, e.g. %s); remove them or use the old plan'
                 % (len(stray), os.path.basename(stray[0])))
    todo = [(s, e) for s, e in segs if not os.path.exists(seg_path(out, s))]
    print('segments: %d in range, %d done, %d to render (%s, %dx%d ×%d @%s fps)'
          % ((len(segs), len(segs) - len(todo), len(todo), a.profile) + out_size(render) + (a.scale, render.FPS)),
          flush=True)

    done_frames = mp.get_context('fork').Value('d', 0)
    parent = os.getpid()

    def progress(n, dt):
        done_frames.value += n
        left = sum(e - s for s, e in todo) - done_frames.value
        json.dump({'pid': parent, 'profile': a.profile, 'frames_done_this_run': int(done_frames.value),
                   'frames_left': int(left), 'last_segment_s': round(dt, 1), 'updated': time.ctime()},
                  open(prog_file, 'w'))

    if todo:
        ctx = mp.get_context('fork')
        q = ctx.Queue()
        for item in todo:
            q.put(item)
        time.sleep(0.3)
        est, lock = ctx.Value('d', 1.6), ctx.Lock()   # seconds per frame, refined after the first segment
        deadline = start + a.budget
        ps = [ctx.Process(target=worker, args=(i, code, out, q, est, deadline, lock, a.profile, a.scale, progress))
              for i in range(a.procs)]
        for p in ps:
            p.start()
        for p in ps:
            p.join(max(0.1, deadline + 30 - time.time()))
        for p in ps:
            if p.is_alive():
                p.terminate()
                print('worker terminated (time limit)', flush=True)
    left = [s for s, _ in plan(total, a.chunk, shots, render.FPS, 0, total) if not os.path.exists(seg_path(out, s))]
    print('this run: %.0fs, remaining segments in whole film: %d' % (time.time() - start, len(left)), flush=True)
    if left:
        return
    print('ALL DONE', flush=True)
    if a.out:
        master.concat(out, a.audio, a.out)
        ok = master.check(a.out, fps=render.FPS, dur=total / render.FPS, decode=True)
        sys.exit(0 if ok else 1)


if __name__ == '__main__':
    main()
