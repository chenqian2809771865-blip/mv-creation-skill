#!/usr/bin/env python3
"""Swap the opening segments of an mvrun master, keeping the old tail byte-for-byte (runs on the user's Mac VM).

usage: python3 splice.py OLD_MASTER WORKDIR N_FRAMES NEWSEG1 [NEWSEG2 ...]

mvrun masters are -c copy concatenations of per-shot H.264 segments, so every segment start is an IDR. N_FRAMES is
the first old keyframe after the re-rendered segments. Steps: split the old video at N_FRAMES (-c copy), check the
new segments' SPS/PPS equal the old ones, concat new head + old tail (-c copy), take the old AAC stream (-c copy),
then verify frame count, duration, a clean full decode, and that every tail packet is identical to the old master.
Writes WORKDIR/new_master.mp4 and WORKDIR/splice_report.txt. Never deletes anything outside WORKDIR.
"""
import hashlib
import json
import os
import subprocess
import sys


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)


def nals(path):
    """SPS (7) and PPS (8) NAL units of the first access unit, Annex-B bytes"""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-map', '0:v', '-c', 'copy', '-bsf:v', 'h264_mp4toannexb',
                          '-frames:v', '1', '-f', 'h264', '-'], check=True, capture_output=True).stdout
    out, i, starts = {}, 0, []
    while True:
        j = raw.find(b'\x00\x00\x01', i)
        if j < 0:
            break
        starts.append(j + 3)
        i = j + 3
    for a, b in zip(starts, starts[1:] + [len(raw) + 3]):
        unit = raw[a:b - 3].rstrip(b'\x00')
        t = unit[0] & 0x1f if unit else None
        if t in (7, 8):
            out.setdefault(t, unit)
    return out


def nframes(path):
    r = run(['ffprobe', '-v', 'error', '-select_streams', 'v', '-count_packets', '-show_entries', 'stream=nb_read_packets',
             '-of', 'csv=p=0', path])
    return int(r.stdout.strip())


def pkt_md5(path):
    r = run(['ffmpeg', '-v', 'error', '-i', path, '-map', '0:v', '-c', 'copy', '-f', 'framemd5', '-'])
    return [ln.split(',')[-1].strip() for ln in r.stdout.splitlines() if ln and not ln.startswith('#')]


def main():
    old, wd, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
    segs = sys.argv[4:]
    rep = []
    os.makedirs(wd, exist_ok=True)
    # 1. split the old video at frame n
    run(['ffmpeg', '-v', 'error', '-y', '-i', old, '-map', '0:v', '-c', 'copy', '-f', 'segment', '-segment_frames', str(n),
         '-reset_timestamps', '1', os.path.join(wd, 'old_%03d.mp4')])
    head_old, tail = os.path.join(wd, 'old_000.mp4'), os.path.join(wd, 'old_001.mp4')
    assert not os.path.exists(os.path.join(wd, 'old_002.mp4')), 'split made more than 2 parts'
    assert nframes(head_old) == n, 'old head has %d frames, expected %d (no keyframe at %d?)' % (nframes(head_old), n, n)
    n_new = sum(nframes(s) for s in segs)
    assert n_new == n, 'new segments have %d frames, expected %d' % (n_new, n)
    # 2. parameter sets must match, or the concat would need a re-encode
    ref = nals(tail)
    for s in segs:
        assert nals(s) == ref, 'SPS/PPS differ: ' + s
    rep.append('SPS/PPS identical across new segments and old tail')
    # 3. concat + old audio
    lst = os.path.join(wd, 'list.txt')
    with open(lst, 'w') as fh:
        fh.writelines("file '%s'\n" % os.path.abspath(p) for p in segs + [tail])
    out = os.path.join(wd, 'new_master.mp4')
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-i', old, '-map', '0:v', '-map', '1:a',
         '-c', 'copy', '-movflags', '+faststart', out])
    # 4. verify
    fo, fn = nframes(old), nframes(out)
    assert fo == fn, 'frame count %d != old %d' % (fn, fo)
    probe = lambda p: json.loads(run(['ffprobe', '-v', 'error', '-show_entries',
                                      'format=duration:stream=codec_name,width,height,r_frame_rate,color_space,color_transfer,color_primaries,color_range,profile,level',
                                      '-of', 'json', p]).stdout)
    po, pn = probe(old), probe(out)
    assert po['streams'] == pn['streams'], 'stream params differ:\n%s\n%s' % (po['streams'], pn['streams'])
    rep.append('frames %d = old; duration old %s new %s' % (fn, po['format']['duration'], pn['format']['duration']))
    dec = subprocess.run(['ffmpeg', '-v', 'error', '-i', out, '-f', 'null', '-'], capture_output=True, text=True)
    assert dec.returncode == 0 and not dec.stderr.strip(), 'decode errors: ' + dec.stderr[:500]
    rep.append('full decode clean')
    mo, mn = pkt_md5(old), pkt_md5(out)
    assert mo[n:] == mn[n:], 'tail packets differ'
    rep.append('tail packets %d..%d identical to old master' % (n, fo - 1))
    a_old = hashlib.md5(run(['ffmpeg', '-v', 'error', '-i', old, '-map', '0:a', '-c', 'copy', '-f', 'framemd5', '-']).stdout.encode()).hexdigest()
    a_new = hashlib.md5(run(['ffmpeg', '-v', 'error', '-i', out, '-map', '0:a', '-c', 'copy', '-f', 'framemd5', '-']).stdout.encode()).hexdigest()
    assert a_old == a_new, 'audio packets differ'
    rep.append('audio packets identical to old master')
    with open(os.path.join(wd, 'splice_report.txt'), 'w') as fh:
        fh.write('\n'.join(rep) + '\n')
    print('\n'.join(rep))
    print('OK', out, os.path.getsize(out))


if __name__ == '__main__':
    main()
