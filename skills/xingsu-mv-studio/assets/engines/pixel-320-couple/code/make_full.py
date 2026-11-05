# full render: python3 make_full.py out.mp4 [procs]  (resumable 10 s segments -> concat + audio)
import os, subprocess, sys, time
import multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEG = os.path.join(ROOT, 'segs')
FPS = 24
CH = 240


def work(job):
    f0, f1 = job
    sys.path.insert(0, HERE)
    import render
    out = os.path.join(SEG, 'seg_%05d.mp4' % f0)
    tmp = out + '.part.mp4'
    cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '2560x1440', '-r', str(FPS), '-i', '-',
           '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-tune', 'animation', '-profile:v', 'high', '-level:v', '5.1', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
           '-threads', '2', '-x264-params', 'keyint=48:min-keyint=24:ref=4', '-f', 'mp4', tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    t0 = time.time()
    for f in range(f0, f1):
        p.stdin.write(render.frame(f / FPS).tobytes())
    p.stdin.close()
    if p.wait() == 0:
        os.replace(tmp, out)
        print('seg %d-%d %.0fs' % (f0, f1 - 1, time.time() - t0), flush=True)


def main():
    out = sys.argv[1]
    procs = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    sys.path.insert(0, HERE)
    import story
    total = int(round(story.DUR * FPS))
    os.makedirs(SEG, exist_ok=True)
    jobs = [(f, min(total, f + CH)) for f in range(0, total, CH)]
    todo = [j for j in jobs if not os.path.exists(os.path.join(SEG, 'seg_%05d.mp4' % j[0]))]
    print('total frames %d, segments %d, todo %d' % (total, len(jobs), len(todo)), flush=True)
    with mp.get_context('fork').Pool(procs) as pool:
        pool.map(work, todo, chunksize=1)
    lst = os.path.join(SEG, 'list.txt')
    with open(lst, 'w') as f:
        for j in jobs:
            f.write("file '%s'\n" % os.path.join(SEG, 'seg_%05d.mp4' % j[0]))
    vdur = total / FPS
    audio = os.path.join(SEG, 'audio.m4a')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', os.path.join(ROOT, 'audio', 'song.wav'), '-t', '%.4f' % vdur,
                    '-c:a', 'aac', '-b:a', '320k', audio], check=True)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-i', audio, '-map', '0:v', '-map', '1:a',
                    '-c', 'copy', '-movflags', '+faststart', out], check=True)
    print('DONE', out, flush=True)


if __name__ == '__main__':
    main()
