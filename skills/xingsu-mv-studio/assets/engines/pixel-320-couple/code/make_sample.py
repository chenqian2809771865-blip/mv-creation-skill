# render the sample: python3 make_sample.py out.mp4
import os, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render, story
FPS = 24
out = sys.argv[1]
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
total = int(round(story.DUR * FPS))
a0, a1 = story.SONG_END_FADE
cmd = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '2560x1440', '-r', str(FPS), '-i', '-',
       '-ss', '0', '-t', '%.4f' % (total / FPS), '-i', os.path.join(ROOT, 'audio', 'song.wav'),
       '-map', '0:v', '-map', '1:a', '-af', 'afade=t=out:st=%.3f:d=%.3f' % (a0, a1 - a0),
       '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-tune', 'animation', '-x264-params', 'ref=4', '-profile:v', 'high', '-level:v', '5.1', '-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv',
       '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', out]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
t0 = time.time()
for f in range(total):
    p.stdin.write(render.frame(f / FPS).tobytes())
p.stdin.close(); p.wait()
print('frames', total, 'time %.0fs' % (time.time() - t0))
