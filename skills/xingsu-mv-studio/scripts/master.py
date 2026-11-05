#!/usr/bin/env python3
"""Encoding profiles and checks for MV deliverables: the single source of ffmpeg/x264 parameters.

Library use (render scripts, mvrun.py):
    from master import open_encoder
    enc = open_encoder('out/master_4k.mp4', W, H, 24, profile='master', scale=6)   # scale: nearest-neighbour ×N
    for t in times: enc.stdin.write(frame(t).tobytes())                             # BGRA uint8 (H, W, 4)
    enc.stdin.close(); assert enc.wait() == 0

CLI:
    master.py concat  SEG_DIR_OR_LIST AUDIO OUT        join segments with -c copy (one encode generation) + AAC 320k
    master.py mux     VIDEO AUDIO OUT                   put audio on a finished video stream (video copied)
    master.py down    MASTER_4K OUT [--size 2560x1440]  2K archive master from the 4K upload master, same profile
    master.py preview MASTER OUT [--height 720] [--max-mb 25]   two-pass preview for the chat window
    master.py check   FILE [--fps 24] [--dur S] [--size WxH] [--no-decode]   verify a master; exit 1 on failure

Profiles:
    master   upload/archive master: preset slow, crf 14, tune animation, BT.709 matrix + full colour tags,
             High@5.1, ref=4, VBV 50 Mb/s. Level 5.1 must stay locked: -tune animation doubles refs and x264
             then auto-picks level 6.0 at 4K, which Mac/phone hardware decoders reject (2K is unaffected).
    preview  fast draft: preset veryfast, crf 20, same colour handling.
Untagged RGB->YUV through ffmpeg defaults to the BT.601 matrix while players assume BT.709 for HD, so colours
shift (measured: red 230 shows as 249, green 200 as 168). Every profile here converts and tags BT.709.
"""
import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

# Newer ffmpeg takes primaries/transfer from the frames and ignores -color_primaries/-color_trc,
# so the filter chain also stamps all four properties on every frame (measured: 6.1 and 7.0 fine, 9.0 wrote unknown).
SETPARAMS = 'setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv'

COLOR_TAGS = ['-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv']

PROFILES = {
    'master': ['-c:v', 'libx264', '-preset', 'slow', '-crf', '14', '-tune', 'animation',
               '-profile:v', 'high', '-level:v', '5.1',
               '-x264-params', 'ref=4:vbv-maxrate=50000:vbv-bufsize=100000'],
    'preview': ['-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', '-profile:v', 'high', '-level:v', '5.1'],
}
AUDIO_MASTER = ['-c:a', 'aac', '-b:a', '320k']


def color_vf(scale=1, out_w=None, out_h=None, flags='lanczos'):
    """Video filter: optional resize, then BT.709 limited-range conversion to yuv420p."""
    if scale and scale != 1:
        size = 'iw*%d:ih*%d:flags=neighbor:' % (scale, scale)
    elif out_w:
        size = '%d:%d:flags=%s:' % (out_w, out_h, flags)
    else:
        size = ''
    return 'scale=%sout_color_matrix=bt709:out_range=tv,format=yuv420p,' % size + SETPARAMS


def encoder_cmd(out, w, h, fps, pix_fmt='bgra', profile='master', scale=1, threads=None, extra=None):
    """ffmpeg command that reads raw frames (w×h, pix_fmt) from stdin and writes a video-only MP4."""
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', pix_fmt, '-s', '%dx%d' % (w, h),
           '-r', str(fps), '-i', '-', '-vf', color_vf(scale)] + PROFILES[profile] + COLOR_TAGS
    if threads:
        cmd += ['-threads', str(threads)]
    return cmd + (extra or []) + ['-an', '-movflags', '+faststart', out]


def open_encoder(out, w, h, fps, **kw):
    return subprocess.Popen(encoder_cmd(out, w, h, fps, **kw), stdin=subprocess.PIPE)


def run(cmd):
    r = subprocess.run(cmd)
    if r.returncode:
        sys.exit('ffmpeg failed: ' + ' '.join(cmd))


def probe(path):
    out = subprocess.run(['ffprobe', '-v', 'error', '-count_packets', '-show_streams', '-show_format', '-of', 'json',
                          path], capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def concat(src, audio, out):
    if os.path.isdir(src):
        segs = sorted(f for f in os.listdir(src) if f.startswith('seg_') and f.endswith('.mp4') and '.part' not in f)
        if not segs:
            sys.exit('no seg_*.mp4 in ' + src)
        lst = os.path.join(src, 'list.txt')
        with open(lst, 'w') as fh:
            fh.writelines("file '%s'\n" % os.path.abspath(os.path.join(src, s)) for s in segs)
        src = lst
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', src]
    cmd += (['-i', audio, '-map', '0:v', '-map', '1:a'] + AUDIO_MASTER) if audio else ['-an']
    run(cmd + ['-c:v', 'copy', '-movflags', '+faststart', out])


def mux(video, audio, out):
    run(['ffmpeg', '-v', 'error', '-y', '-i', video, '-i', audio, '-map', '0:v', '-map', '1:a', '-c:v', 'copy']
        + AUDIO_MASTER + ['-movflags', '+faststart', out])


def down(src, out, size):
    w, h = map(int, size.lower().split('x'))
    run(['ffmpeg', '-v', 'error', '-y', '-i', src, '-map', '0:v', '-map', '0:a?', '-vf',
         'scale=%d:%d:flags=lanczos:in_color_matrix=bt709:in_range=tv:out_color_matrix=bt709:out_range=tv,'
         'format=yuv420p,' % (w, h) + SETPARAMS] + PROFILES['master'] + COLOR_TAGS + ['-c:a', 'copy', '-movflags', '+faststart', out])


def preview(src, out, height, max_mb, kbps):
    info = probe(src)
    dur = float(info['format']['duration'])
    v = next(s for s in info['streams'] if s['codec_type'] == 'video')
    master_kbps = int(v.get('bit_rate') or info['format'].get('bit_rate') or 8e6) / 1000
    if not kbps:
        budget = max_mb * 8192 / dur - 128            # kbit/s left for video after 128k audio
        kbps = min(budget * 0.96, 6000, master_kbps * 0.5)   # never larger than the master
    kbps = int(max(kbps, 300))
    vf = 'scale=-2:%d:flags=lanczos:in_color_matrix=bt709:out_color_matrix=bt709:out_range=tv,format=yuv420p,' % height + SETPARAMS
    base = ['ffmpeg', '-v', 'error', '-y', '-i', src, '-vf', vf, '-c:v', 'libx264', '-preset', 'slow',
            '-b:v', '%dk' % kbps] + COLOR_TAGS
    with tempfile.TemporaryDirectory() as tmp:
        log = os.path.join(tmp, 'pass')
        run(base + ['-pass', '1', '-passlogfile', log, '-an', '-f', 'mp4', os.devnull])
        run(base + ['-pass', '2', '-passlogfile', log, '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', out])
    print('preview %s: %d kbps video, %.1f MB' % (out, kbps, os.path.getsize(out) / 2 ** 20))


def check(path, fps=None, dur=None, size=None, decode=True):
    info = probe(path)
    v = next((s for s in info['streams'] if s['codec_type'] == 'video'), None)
    a = next((s for s in info['streams'] if s['codec_type'] == 'audio'), None)
    bad, rows = [], []

    def item(name, value, ok):
        rows.append('%-4s %-14s %s' % ('ok' if ok else 'FAIL', name, value))
        if not ok:
            bad.append(name)

    if v is None:
        item('video', 'missing', False)
    else:
        num, den = map(int, v['r_frame_rate'].split('/'))
        rate = num / den
        frames = int(v.get('nb_read_packets') or v.get('nb_frames') or 0)
        vdur = float(v.get('duration') or info['format']['duration'])
        item('size', '%sx%s' % (v['width'], v['height']),
             size is None or '%sx%s' % (v['width'], v['height']) == size.lower())
        item('fps', '%.3f' % rate, fps is None or abs(rate - fps) < 1e-3)
        if dur is not None and fps:
            want = int(round(dur * fps))
            item('frames', '%d (expected %d)' % (frames, want), frames == want)
        else:
            item('frames', frames, frames > 0)
        item('duration', '%.3f s' % vdur, dur is None or abs(vdur - dur) < 1.5 / rate)
        item('codec', '%s %s' % (v['codec_name'], v.get('profile')), v['codec_name'] == 'h264')
        item('level', v.get('level'), int(v.get('level', 99)) <= 51)
        item('pix_fmt', v.get('pix_fmt'), v.get('pix_fmt') == 'yuv420p')
        tags = [v.get('color_space'), v.get('color_primaries'), v.get('color_transfer'), v.get('color_range')]
        item('color', '/'.join(map(str, tags)), tags == ['bt709', 'bt709', 'bt709', 'tv'])
    item('audio', '%s %s kbps' % (a['codec_name'], int(a.get('bit_rate', 0)) // 1000) if a else 'none', a is not None)
    item('file', '%.1f MB' % (os.path.getsize(path) / 2 ** 20), True)
    if decode:
        r = subprocess.run(['ffmpeg', '-v', 'error', '-xerror', '-i', path, '-f', 'null', '-'],
                           capture_output=True, text=True)
        item('decode', 'full decode ' + ('clean' if r.returncode == 0 and not r.stderr.strip()
                                          else r.stderr.strip()[:200]), r.returncode == 0 and not r.stderr.strip())
    print('\n'.join(rows))
    print('PASS' if not bad else 'FAIL: ' + ', '.join(bad))
    return not bad


def main():
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        sys.exit('ffmpeg and ffprobe are required')
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('concat'); p.add_argument('src'); p.add_argument('audio'); p.add_argument('out')
    p = sub.add_parser('mux'); p.add_argument('video'); p.add_argument('audio'); p.add_argument('out')
    p = sub.add_parser('down'); p.add_argument('src'); p.add_argument('out'); p.add_argument('--size', default='2560x1440')
    p = sub.add_parser('preview'); p.add_argument('src'); p.add_argument('out')
    p.add_argument('--height', type=int, default=720); p.add_argument('--max-mb', type=float, default=25)
    p.add_argument('--kbps', type=int)
    p = sub.add_parser('check'); p.add_argument('file'); p.add_argument('--fps', type=float)
    p.add_argument('--dur', type=float); p.add_argument('--size'); p.add_argument('--no-decode', action='store_true')
    a = ap.parse_args()
    if a.cmd == 'concat':
        concat(a.src, a.audio, a.out)
    elif a.cmd == 'mux':
        mux(a.video, a.audio, a.out)
    elif a.cmd == 'down':
        down(a.src, a.out, a.size)
    elif a.cmd == 'preview':
        preview(a.src, a.out, a.height, a.max_mb, a.kbps)
    else:
        sys.exit(0 if check(a.file, a.fps, a.dur, a.size, not a.no_decode) else 1)


if __name__ == '__main__':
    main()
