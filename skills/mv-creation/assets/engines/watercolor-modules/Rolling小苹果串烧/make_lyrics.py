# make_lyrics.py: lyric timeline for the mashup clip (instrumental: no vocals, so line and word times come from the
# transcribed lead melody, basic-pitch notes of the mix + the UVR "vocal" stem). Clip time = file time - S0.
# Line starts were checked against the original LRC spacing (小苹果) and syllable counts (Rolling in the Deep).
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, '..')
AN = os.path.join(ROOT, '..', 'an')
S0 = json.load(open(os.path.join(ROOT, 'data', 'beats.json')))['s0']


# (song, part, text, syllables per unit (Rolling), syllable onsets (file time) OR ('span', a, b) for an even spread, end of line)
# Top-voice syllable onsets were picked by hand from the basic-pitch notes (counts match the syllables: 6/10/5/10/9 in the
# Rolling chorus, 12 in 示例歌, 8 in 示例歌词…). Where the lead is buried, the line is spread evenly over its melodic span.
L = [
    ('R', 'lead', '示例歌词占位文 字 示例歌词 占位文字示例歌词 占位 文字 示例歌词占', [1, 1, 2, 2, 1, 1, 1], ('span', 4.22, 5.75), 7.2),
    ('R', 'lead', '示例歌词占位文字 示 例歌词占位 文字示例歌 词占位 文字示例 歌词占位文字示例 歌词 占位文 字示例 歌词占位', [2, 1, 2, 1, 1, 1, 2, 1, 1, 1, 1], ('span', 8.05, 10.62), 11.5),
    ('R', 'lead', '示例歌词占位文 字 示例歌 词占位 文字示 例歌词占位文字 示例歌词占', [3, 1, 1, 1, 1, 2, 1], ('span', 11.92, 13.5), 15.3),
    ('X', 'lead', '示例歌词占位文字示例 歌词占', None, [15.68, 15.92, 16.14, 16.37, 16.48, 16.85, 17.34, 17.59, 17.81, 18.08, 18.30, 18.41, 18.60], 19.3),
    ('X', 'lead', '示例歌词占位文字示 例歌词占', None, [19.54, 19.78, 20.21, 20.33, 20.45, 20.97, 21.17, 21.43, 21.65, 21.90, 22.12, 22.25, 22.36], 23.1),
    ('X', 'lead', '示例歌词占位文字示 例歌词占', None, [23.35, 23.61, 23.84, 24.05, 24.16, 24.52, 25.02, 25.27, 25.50, 25.75, 25.95, 26.08, 26.21], 27.0),
    ('X', 'lead', '示例歌词占位文字 示例歌词', None, [27.22, 27.42, 27.68, 27.91, 28.01, 28.64, 28.85, 29.10, 29.33, 29.50, 29.65, 29.90], 30.9),
    ('R', 'lead', '示 例歌词占位 文字示例 歌词占位文字示', [1, 1, 1, 2], [31.13, 31.51, 31.96, 32.20, 32.70], 33.6),
    ('R', 'lead', '示例 歌词占位文字示例 歌词占 位文 字示例', [1, 2, 1, 1, 1], [33.89, 34.02, 34.38, 34.50, 34.62, 34.98], 38.0),
    ('R', 'back', '示例歌词占位 文字示例歌 词占位文 字示例 歌词占位文 字示例 歌词占 位文', [1, 2, 1, 1, 2, 1, 1, 1], [35.39, 35.79, 36.36, 36.56, 36.77, 37.00, 37.41, 37.51, 37.75, 37.99], 38.7),
    ('R', 'lead', '示例歌词占位文 字示 例歌词 占位文字', [2, 1, 1, 1], [38.23, 38.36, 38.47, 38.62, 38.81], 41.6),
    ('R', 'back', '示例歌词占 位文字 示例歌词占 位文字示 例歌词占位文字 示例 歌词占 位文字示', [1, 1, 2, 1, 2, 1, 1, 1], [39.23, 39.42, 39.66, 40.18, 40.41, 40.51, 40.61, 40.88, 41.14, 41.24], 41.7),
    ('R', 'lead', '示例歌 词占位 文字 示例歌词占 位文字示例歌 词占 位文字示 例歌词占', [1, 1, 1, 1, 2, 1, 1, 1], [41.81, 42.07, 42.33, 42.80, 43.08, 43.51, 43.72, 43.98, 44.33], 46.3),
    ('X', 'lead', '示例歌词占位文字示例', None, ('span', 46.86, 49.26), 50.5),
    ('X', 'lead', '示例歌词占位文字示', None, ('span', 50.71, 52.63), 53.9),
    ('X', 'lead', '示例歌词占位文字示例歌', None, ('span', 54.06, 56.76), 58.2),
    ('X', 'lead', '示例歌词占位文字', None, [58.39, 58.86, 59.34, 59.90, 60.31, 60.79, 61.01, 61.30], 62.3),
]

res = []
for song, part, txt, syl, on, lend in L:
    if song == 'R':
        units = txt.split(' ')
    else:
        units = [c for c in txt if c != ' ']
        syl = [1] * len(units)
    nsyl = sum(syl)
    if isinstance(on, tuple):
        a, b = on[1], on[2]
        on = [a + (b - a) * j / (nsyl - 1) for j in range(nsyl)]
    assert len(on) == nsyl, (txt, len(on), nsyl)
    ut, j = [], 0
    for n in syl:
        ut.append(on[j])
        j += n
    st = ut[0]
    res.append(dict(t=round(st - S0, 3), end=round(lend - S0, 3), song=song, part=part, text=txt,
                    units=units, ut=[round(x - S0, 3) for x in ut]))
    print(f"{st - S0:6.2f}-{lend - S0:6.2f} {part:4s} {txt}")
    print('        ', ' '.join(f'{u}@{x - S0:.2f}' for u, x in zip(units, ut)))
json.dump(res, open(os.path.join(ROOT, 'data', 'lyrics.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# SRT (lines; backing vocals in parentheses)
def ts(x):
    ms = int(round(x * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f'{h:02d}:{m:02d}:{s:02d},{ms:03d}'
with open(os.path.join(ROOT, 'out', '串烧_MV_歌词.srt'), 'w', encoding='utf-8') as f:
    for i, r in enumerate(res):
        txt = r['text'] if r['part'] == 'lead' else f"({r['text']})"
        f.write(f"{i + 1}\n{ts(r['t'])} --> {ts(r['end'])}\n{txt}\n\n")
