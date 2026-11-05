# build_data.py: beat grid + corrected lyric timing for 《东京不太热》 clip (user mp4, audio only, cut from S0 = 0.100 s).
# Beats: the clip is a splice of two tempos (first 8 bars sped up ≈ +1 semitone, 128.02 BPM; from bar 9 = the chorus,
# 120.85 BPM). Each part is fitted as its own constant grid on the high-confidence tracked beats (median residual 0.8 / 2.1 ms);
# the splice sits on the chorus downbeat k32, where both grids meet within 6 ms.
# Lyrics: align_lyrics on the clip lines (80.3 % units recognised), then hand fixes from short-window ASR + vocal pitch/onsets.
import json, os, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, '..')
S0 = 0.100
raw = json.load(open(os.path.join(R, 'data', 'beats_raw.json')))
PA = (0.46869, 0.0314)        # period, b0 (file time) for k <= 31
PB = (0.49648, -0.8529)       # for k >= 32
N = 97                        # k0..k96 (k96 = last downbeat, 0.28 s before the clip ends)
beats = []
for k in range(N):
    p, b0 = PA if k <= 31 else PB
    beats.append(round(b0 + p * k - S0, 4))
DUR = 46.990
bj = dict(src='user mp4 audio, cut from S0=0.100 s', bpm=120.85, bpm_intro=128.02, beat=PB[0], dur=DUR, beats=beats,
          downbeat_phase=0, splice_k=32, stops=[31, 63, 95],
          beats_measured=[round(b - S0, 4) for b in raw['beats']], conf=raw['conf'])
json.dump(bj, open(os.path.join(R, 'data', 'beats.json'), 'w'), indent=1)

# ---- lyrics
auto = os.path.join(R, 'data', 'lyrics.auto.json')
if not os.path.exists(auto):
    shutil.copy(os.path.join(R, 'data', 'lyrics.json'), auto)
L = json.load(open(auto, encoding='utf-8'))
by = {i: l for i, l in enumerate(L)}


def setl(i, start=None, end=None, times=None):
    l = by[i]
    if times is not None:
        l[3] = [round(x, 3) for x in times]
        l[0] = l[3][0]
    if start is not None:
        l[0] = start
        if times is None:
            l[3] = [start] * len(l[3])
    if end is not None:
        l[1] = end


# 示例歌词占位文字示例歌词: the line starts on the new note at 15.15 (pitch 70→73), not 15.22 (estimated); 呢 on 17.62
setl(5, times=[15.15, 15.45, 15.66, 15.94, 16.17, 16.17, 16.44, 16.63, 16.86, 17.12, 17.41, 17.62], end=17.88)
setl(6, start=17.93, end=18.45)                    # 示例歌词: ASR 「那样」 18.08/18.32, pitch jump at 17.92
setl(8, start=19.95, end=20.55)                    # 示例歌词 after 示例歌词 (ASR 那 20.02 / 样 20.20)
setl(9, times=[20.73, 21.05, 21.18, 21.41], end=21.76)   # 示例歌词: 呢 starts on the new note at 21.41
setl(10, start=21.82, end=22.48)                   # Ayo: ASR 爱 21.96 / よ 22.14, voice to 22.5
setl(15, times=[28.465, 28.98, 29.175, 29.40], end=29.86)   # 示例歌词
setl(16, start=29.9, end=30.56)                    # Ayo: the aligner put it into the vocal gap (30.81); voice 29.9–30.55
l17 = by[17][3]
setl(17, times=[30.84, 31.0, 31.17, 31.38] + l17[4:])   # 示例歌词: first syllable right after the vocal gap (30.6–30.8)
json.dump(L, open(os.path.join(R, 'data', 'lyrics.json'), 'w', encoding='utf-8'), ensure_ascii=False)
for l in L:
    print(f'{l[0]:7.3f} {l[1]:7.3f} {l[2]}')
print('beats', beats[:3], beats[30:34], beats[-2:])
