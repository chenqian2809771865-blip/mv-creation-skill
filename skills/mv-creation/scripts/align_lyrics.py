#!/usr/bin/env python3
"""Align the user's lyric text to the sung vocals of a song: per-line start/end and per-character times.

usage:
  python3 align_lyrics.py SONG LYRICS --out data/lyrics.json [--from S] [--to S] [--trim-s0]
                          [--vocals FILE] [--models DIR] [--compensate 1.0] [--eq 偷不,掉到]
                          [--lang zh] [--windows 10,13] [--step 2] [--space-times]

SONG    any audio ffmpeg decodes. --from/--to analyse only that range; output times are relative to --from.
LYRICS  plain UTF-8 text (one lyric line per line, blank lines ignored) or an .lrc file ([mm:ss.xx]text, several
        time tags per line allowed, metadata tags such as [ar:] ignored, [offset:] applied). The user's text is the
        source of truth: it is never rewritten, only timed.

Pipeline (the procedure validated in earlier MV projects):
  1. ffmpeg decodes 44.1 kHz stereo. S0 = first sample with |x| > 1e-4 (leading digital silence) is reported;
     times are not shifted unless --trim-s0 is given (then they are relative to S0, for clips cut from S0).
  2. Vocal separation with UVR-MDX-NET-Voc_FT.onnx (onnxruntime, MDX-Net chunked STFT: n_fft 7680, hop 1024,
     dim_f 3072, dim_t 256, chunk hop*(dim_t-1), n_fft//2 trimmed at both chunk edges). Writes <out>.vocals.wav and
     <out>.inst.wav; pass --vocals <out>.vocals.wav (same --from/--to) to skip this step next time.
     --compensate scales the vocals (1.021 was used with this model in one project; default 1.0).
  3. ASR: sherpa-onnx SenseVoice (use_itn off) on the vocals as 16 kHz mono peak-normalised to 1/1.1, in
     overlapping windows of several sizes (default 10 s and 13 s, a new window every 2 s), with token timestamps.
     Tokens within 0.6 s of a window edge do not vote (except at the start/end of the audio).
  4. Matching units: CJK / kana / hangul per character, latin and digit runs per word (lower-cased); punctuation
     and spaces are not matched. A near match (score 1.4 instead of 2.0) is the same pinyin ignoring tone and the
     usual sung confusions z/zh c/ch s/sh n/l -an/-ang -en/-eng -in/-ing (needs pypinyin), or an --eq pair, so a
     homophone misrecognition keeps the user's text.
     a. Global: all windows' tokens are merged into one stream (the same unit recognised within 0.35 s in
        overlapping windows is one event, at most one token per window) and aligned to the whole text by a
        monotone DP. This only decides which part of the text each window can belong to, so repeated choruses
        cannot be confused.
     b. Local: each window is Smith-Waterman-aligned (match 2.0, near 1.4, mismatch -1.0, gap -1.2) to its band
        of the text; each unit collects the times of all windows; the largest group within 0.35 s gives the
        median time. Out-of-order outliers are dropped.
  5. Timing: each time is snapped to the strongest rise of the vocal envelope in [t-0.14, t+0.04] s (SenseVoice
     stamps tend to sit after the sung onset), else t-0.05; rises in near silence (30 dB under the coming peak) do
     not count, and a time left in vocal silence moves to the voice onset if it follows within 0.3 s.
     Gaps inside a line are interpolated; a line whose
     first units were missed starts at the vocal energy onset found by searching back (not before the previous
     line); times are forced monotone. Line end: where the vocal level falls 22 dB below the line's peak, +0.15 s,
     at least last unit + 0.4 s, capped 0.12 s before the next line.
  6. If fewer than 5% of the text units are recognised, prints INSTRUMENTAL, writes no JSON, exits with code 3.
     If fewer than 35% are recognised, the JSON is still written but a LOW MATCH warning is printed and put at
     the top of the report and the exit code is 4: the lyrics are probably for another song or version (or the
     range is wrong), so don't use the timings before checking.

Output (--out): UTF-8 JSON [[start, end, "text", [time of each character of text except ASCII spaces]], ...]
sorted by start, 3 decimals. The 4th element drives karaoke renderers (lyrics_to_subtitles.py ignores it);
--space-times also gives spaces a time (the next character's). Characters of a latin word share the word's time;
punctuation takes the previous character's. Next to it: <out>.report.md (S0, units matched, every line where the
ASR heard something else, starts from vocal energy, low-confidence lines, lines not found, LRC drift table).
Lines before the first / after the last recognised line (credits, parts outside --from/--to) are dropped and
listed in the report.

Exit codes: 0 ok, 1 error, 3 instrumental, 4 low match (alignment written, probably wrong lyrics/range).
Needs: ffmpeg, numpy, scipy, onnxruntime, sherpa-onnx; optional pypinyin (homophones). Models are downloaded on
first use to ~/.cache/mv-creation/models (--models DIR to use another folder; files are looked up there as
UVR-MDX-NET-Voc_FT.onnx and sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17/{model.int8.onnx,tokens.txt}).
"""
import argparse
import json
import math
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tarfile
import time
import unicodedata
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

UVR_FILE = 'UVR-MDX-NET-Voc_FT.onnx'
UVR_URL = 'https://github.com/TRvlvr/model_repo/releases/download/all_public_uvr_models/' + UVR_FILE
SV_NAME = 'sherpa-onnx-sense-voice-zh-en-ja-ko-yue-int8-2024-07-17'
SV_URL = f'https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/{SV_NAME}.tar.bz2'
SV_FILES = ('model.int8.onnx', 'tokens.txt')
DEFAULT_MODELS = '~/.cache/mv-creation/models'

MIX_SR, ASR_SR = 44100, 16000
MDX_N_FFT, MDX_HOP, MDX_DIM_F, MDX_DIM_T = 7680, 1024, 3072, 256

SILENCE_LEVEL = 1e-4             # S0 = first sample above this
EDGE_S = 0.6                     # tokens this close to a window edge do not vote
MERGE_S = 0.35                   # same unit within this time in overlapping windows = one event
SCORE_MATCH, SCORE_NEAR, SCORE_MISMATCH, SCORE_GAP = 2.0, 1.4, -1.0, -1.2
MIN_SUPPORT = 0.25               # a merged stream event needs this share of the windows that cover it
BAND_PAD_S, BAND_PAD_UNITS = 2.0, 8
MONOTONE_TOL = 0.1               # unit times may go back this much before one of them is an outlier
SNAP_BEFORE, SNAP_AFTER, SNAP_MIN_RISE, SNAP_DEFAULT = 0.14, 0.04, 0.02, 0.05
SNAP_FLOOR_DB, SNAP_FORWARD = 30.0, 0.3
MIN_GAP, COLLIDE = 0.08, 0.05    # monotone: a unit closer than COLLIDE to the previous one is put MIN_GAP after it
END_DROP_DB, END_TAIL, END_MIN, END_GUARD = 22.0, 0.15, 0.4, 0.12
ONSET_DROP_DB, ONSET_MAX_DIP = 25.0, 0.12
SILENT_WINDOW_DB = 40.0          # windows whose vocals stay this far below the loudest frame are not decoded
INSTRUMENTAL_RATIO = 0.05
MISMATCH_RATIO = 0.35   # sung pop usually recognises 60-90 %; below this the lyrics may not belong to the audio
LRC_MARGIN_S = 15.0              # with --from/--to, LRC lines this far outside the range are still offered


class AlignError(Exception):
    """A user-facing error: printed without a traceback, exit code 1."""


def log(msg):
    print(msg, file=sys.stderr, flush=True)


# ----------------------------------------------------------------------------------------------------- lyrics text

TIME_TAG = re.compile(r'(\d+):(\d+(?:[.:]\d+)?)$')
META_TAG = re.compile(r'([A-Za-z#]+)\s*:(.*)$', re.S)
INLINE_TAG = re.compile(r'<\d+:\d+(?:[.:]\d+)?>')
LRC_LINE = re.compile(r'^\s*\[\d+:\d+(?:[.:]\d+)?\]', re.M)
CREDIT_LINE = re.compile(r'^\s*(?:作词|作曲|编曲|词|曲|原唱|演唱|翻唱|制作人?|监制|出品|发行|策划|统筹|录音|混音|母带|和声|配唱|'
                         r'吉他|贝斯|鼓|键盘|弦乐|钢琴|人声|OP|SP|ISRC|lyrics?|lyricist|composer|arranger|'
                         r'producer|written by|music by)[^:：]{0,12}[:：]', re.I)

_KANA = '\u3041-\u3096\u30a1-\u30fa\u30fc'
_CJK = '\u3007\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uac00-\ud7af\U00020000-\U0003134f' + _KANA
_WORD = '0-9A-Za-z\u00c0-\u024f\uff10-\uff19\uff21-\uff3a\uff41-\uff5a'
UNIT_RE = re.compile(f"[{_CJK}]|[{_WORD}]+(?:['\u2019][{_WORD}]+)*")
CJK_RE = re.compile(f'[{_CJK}]')
HAN_RE = re.compile('[\u3007\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\U00020000-\U0003134f]')


@dataclass
class Line:
    text: str
    lrc_time: float = None       # seconds in the song (LRC input only)


@dataclass
class Unit:
    key: str                     # compared form: one CJK character, or a lower-cased latin/digit word
    line: int                    # index into the lyric lines
    positions: list              # indices of the characters of the line text that this unit covers


def norm_key(s):
    return unicodedata.normalize('NFKC', s).lower().replace('\u2019', "'")


def parse_lrc(content):
    """LRC text -> [Line] sorted by time. A line with several time tags is sung several times."""
    lines, offset = [], 0.0
    for raw in content.splitlines():
        rest, times = raw.strip(), []
        while rest.startswith('['):
            close = rest.find(']')
            if close < 0:
                break
            tag = rest[1:close].strip()
            m = TIME_TAG.match(tag)
            if m:
                times.append(int(m.group(1)) * 60 + float(m.group(2).replace(':', '.')))
            else:
                meta = META_TAG.match(tag)
                if not meta:
                    break                      # e.g. "[Chorus]" without a colon: part of the text
                if meta.group(1).lower() == 'offset':
                    try:
                        offset = float(meta.group(2).strip()) / 1000.0
                    except ValueError:
                        pass
            rest = rest[close + 1:].strip()
        text = INLINE_TAG.sub('', rest).strip()
        if text:
            lines += [Line(text, t) for t in times]
    for line in lines:
        line.lrc_time = max(0.0, line.lrc_time - offset)   # positive [offset:] shows lyrics sooner
    lines.sort(key=lambda line: line.lrc_time)
    return lines


def read_lyrics(path):
    """Returns ([Line], is_lrc, [skipped credit lines])."""
    try:
        content = Path(path).read_text(encoding='utf-8-sig')
    except UnicodeDecodeError:
        raise AlignError(f'{path} is not UTF-8 text') from None
    except OSError as e:
        raise AlignError(f'cannot read lyrics {path}: {e}') from None
    is_lrc = Path(path).suffix.lower() == '.lrc' or bool(LRC_LINE.search(content))
    lines = parse_lrc(content) if is_lrc else [Line(s.strip()) for s in content.splitlines() if s.strip()]
    credits = [line.text for line in lines if CREDIT_LINE.match(line.text)]
    return [line for line in lines if not CREDIT_LINE.match(line.text)], is_lrc, credits


def filter_lrc_range(lines, start, end):
    """Keep LRC lines near the analysed range. LRC times may drift (it grows along the song), so the margin
    is LRC_MARGIN_S plus 15% of the time."""
    def near(t):
        margin = LRC_MARGIN_S + 0.15 * t
        return start - margin <= t and (end is None or t <= end + margin)
    return [line for line in lines if near(line.lrc_time)]


def text_units(lines):
    units = []
    for i, line in enumerate(lines):
        for m in UNIT_RE.finditer(line.text):
            units.append(Unit(norm_key(m.group()), i, list(range(m.start(), m.end()))))
    return units


def asr_units(tokens, timestamps, offset=0.0):
    """SenseVoice tokens -> [(key, time)]: one entry per CJK character, word pieces joined into words
    (a piece starting with a space / U+2581 starts a new word), language/event tags and punctuation dropped."""
    out, word = [], None                     # word: index in out of the latin word that may still grow
    for tok, ts in zip(tokens, timestamps):
        t = offset + float(ts)
        if tok.startswith('<|'):
            word = None
            continue
        new_word = tok[:1] in (' ', '\u2581')
        piece = norm_key(tok.replace('\u2581', ' ').strip())
        if piece == "'" and word is not None:
            out[word][0] += "'"
            continue
        pos = 0
        for m in UNIT_RE.finditer(piece):
            key = m.group()
            if m.start() > pos:
                word = None                  # punctuation inside the piece ends the word
            if CJK_RE.fullmatch(key):
                out.append([key, t])
                word = None
            elif word is not None and not new_word and m.start() == 0:
                out[word][0] += key
            else:
                out.append([key, t])
                word = len(out) - 1
            pos = m.end()
        if pos < len(piece) or not piece:
            word = None
    return [(k.strip("'"), t) for k, t in out if k.strip("'")]


def parse_eq(values):
    """--eq '偷不,掉到' or 'baby/bae' -> [(a, b)] pairs that count as near matches."""
    pairs = []
    for value in values or []:
        for item in re.split(r'[,，\s]+', value.strip()):
            if not item:
                continue
            parts = item.split('/') if '/' in item else list(item)
            if len(parts) != 2 or not all(parts):
                raise AlignError(f'--eq item {item!r}: give two characters (偷不) or two words joined by / (baby/bae)')
            pairs.append((norm_key(parts[0]), norm_key(parts[1])))
    return pairs


def fuzzy_pinyin(p):
    """Tone-less pinyin with the usual sung / regional confusions folded together."""
    p = p.lower().replace('\u00fc', 'v')
    for a, b in (('zh', 'z'), ('ch', 'c'), ('sh', 's')):
        if p.startswith(a):
            p = b + p[2:]
            break
    if p.startswith('l'):
        p = 'n' + p[1:]
    if p.endswith(('ang', 'eng', 'ing')):
        p = p[:-1]
    return p


class Similarity:
    """Compares an ASR unit with a text unit: 'exact', 'near' (same fuzzy pinyin or an --eq pair) or None."""

    def __init__(self, eq_pairs=(), use_pinyin=True):
        self.eq = {frozenset(p) for p in eq_pairs}
        self._pinyin = None
        if use_pinyin:
            try:
                from pypinyin import Style, pinyin
                self._pinyin = lambda ch: pinyin(ch, style=Style.NORMAL, heteronym=True, errors='ignore')
            except ImportError:
                pass
        self._readings, self._scores = {}, {}

    @property
    def has_pinyin(self):
        return self._pinyin is not None

    def readings(self, key):
        r = self._readings.get(key)
        if r is None:
            r = set()
            if self._pinyin is not None and HAN_RE.fullmatch(key):
                for group in self._pinyin(key):
                    r.update(fuzzy_pinyin(p) for p in group)
            self._readings[key] = r
        return r

    def kind(self, a, b):
        if a == b:
            return 'exact'
        if frozenset((a, b)) in self.eq or self.readings(a) & self.readings(b):
            return 'near'
        return None

    def score(self, a, b):
        s = self._scores.get((a, b))
        if s is None:
            k = self.kind(a, b)
            s = SCORE_MATCH if k == 'exact' else SCORE_NEAR if k == 'near' else SCORE_MISMATCH
            self._scores[(a, b)] = s
        return s


# ------------------------------------------------------------------------------------------------------- alignment

@dataclass
class Window:
    start: float
    end: float
    valid_lo: float              # tokens outside [valid_lo, valid_hi] (window edges) do not vote
    valid_hi: float
    tokens: list                 # [(key, time)] in time order, times in clip seconds

    def valid(self, t):
        return self.valid_lo <= t <= self.valid_hi


@dataclass
class Cluster:
    key: str
    times: list = field(default_factory=list)
    windows: set = field(default_factory=set)

    @property
    def time(self):
        return float(np.median(self.times))


def merge_windows(windows):
    """All windows' (non-edge) tokens as one time-ordered stream of events. The same unit recognised within
    MERGE_S in different windows is one event; a window contributes at most one token to an event, so a unit
    really sung twice in quick succession (示例句 示例句) stays two events."""
    items = sorted((t, key, w) for w, win in enumerate(windows) for key, t in win.tokens if win.valid(t))
    clusters, recent = [], {}
    for t, key, w in items:
        near = [c for c in recent.get(key, ()) if w not in c.windows and abs(c.time - t) <= MERGE_S]
        if near:
            c = min(near, key=lambda c: abs(c.time - t))
        else:
            c = Cluster(key)
            clusters.append(c)
            recent.setdefault(key, []).append(c)
        c.times.append(t)
        c.windows.add(w)
        recent[key] = [c for c in recent[key] if c.times[-1] > t - 2 * MERGE_S]
    clusters.sort(key=lambda c: c.time)
    return clusters


def supported(clusters, windows):
    """Drop stream events seen by too few of the windows that cover them (one-window hallucinations)."""
    kept = []
    for c in clusters:
        cover = sum(1 for win in windows if win.valid(c.time))
        if len(c.windows) >= max(1, math.ceil(MIN_SUPPORT * cover)):
            kept.append(c)
    return kept


def global_align(stream, keys, sim):
    """Monotone DP alignment of the stream keys onto the whole text keys; unaligned ends on either side are free.
    Returns [(stream_index or None, text_index or None)] in order."""
    n, m = len(stream), len(keys)
    H = [[0.0] * (m + 1)]
    P = [bytearray([3]) * (m + 1)]                   # 1 diagonal, 2 stream gap (extra token), 3 text gap
    for i in range(1, n + 1):
        a, prev = stream[i - 1], H[i - 1]
        row, ptr = [0.0] * (m + 1), bytearray(m + 1)
        ptr[0] = 2
        for j in range(1, m + 1):
            v, k = prev[j - 1] + sim.score(a, keys[j - 1]), 1
            u = prev[j] + SCORE_GAP
            if u > v:
                v, k = u, 2
            left = row[j - 1] + SCORE_GAP
            if left > v:
                v, k = left, 3
            row[j], ptr[j] = v, k
        H.append(row)
        P.append(ptr)
    ends = [(H[n][j], n, j) for j in range(m + 1)] + [(H[i][m], i, m) for i in range(n + 1)]
    _, i, j = max(ends, key=lambda e: e[0])
    ops = [(None, jj) for jj in range(m - 1, j - 1, -1)] + [(ii, None) for ii in range(n - 1, i - 1, -1)]
    while i > 0 or j > 0:
        k = P[i][j] if i > 0 and j > 0 else (2 if i > 0 else 3)
        if k == 1:
            ops.append((i - 1, j - 1))
            i, j = i - 1, j - 1
        elif k == 2:
            ops.append((i - 1, None))
            i -= 1
        else:
            ops.append((None, j - 1))
            j -= 1
    return ops[::-1]


def local_align(tokens, keys, sim, lo=0, hi=None):
    """Smith-Waterman of one window's tokens [(key, t)] against keys[lo:hi]. Returns [(text_index, t)] for the
    exact/near pairs of the best local alignment, in text order."""
    hi = len(keys) if hi is None else hi
    sub = keys[lo:hi]
    n, m = len(tokens), len(sub)
    if not n or not m:
        return []
    H, P = [[0.0] * (m + 1)], [bytearray(m + 1)]
    best, bi, bj = 0.0, 0, 0
    for i in range(1, n + 1):
        a, prev = tokens[i - 1][0], H[i - 1]
        row, ptr = [0.0] * (m + 1), bytearray(m + 1)
        for j in range(1, m + 1):
            v, k = 0.0, 0
            d = prev[j - 1] + sim.score(a, sub[j - 1])
            if d > v:
                v, k = d, 1
            u = prev[j] + SCORE_GAP
            if u > v:
                v, k = u, 2
            left = row[j - 1] + SCORE_GAP
            if left > v:
                v, k = left, 3
            row[j], ptr[j] = v, k
            if v > best:
                best, bi, bj = v, i, j
        H.append(row)
        P.append(ptr)
    out, i, j = [], bi, bj
    while i > 0 and j > 0 and H[i][j] > 0:
        k = P[i][j]
        if k == 1:
            if sim.score(tokens[i - 1][0], sub[j - 1]) > 0:
                out.append((lo + j - 1, tokens[i - 1][1]))
            i, j = i - 1, j - 1
        elif k == 2:
            i -= 1
        elif k == 3:
            j -= 1
        else:
            break
    return out[::-1]


def monotone_subset(points, tol=MONOTONE_TOL):
    """points [(index, time, weight)] sorted by index -> positions of the heaviest chain whose time never goes
    back by more than tol. Everything else is an out-of-order outlier."""
    n = len(points)
    if not n:
        return []
    best = [w for _, _, w in points]
    prev = [-1] * n
    for b in range(n):
        tb, wb = points[b][1], points[b][2]
        for a in range(b):
            if tb >= points[a][1] - tol and best[a] + wb > best[b]:
                best[b], prev[b] = best[a] + wb, a
    k = int(np.argmax(best))
    chain = []
    while k >= 0:
        chain.append(k)
        k = prev[k]
    return chain[::-1]


def time_guide(n_units, anchors, dur, per_unit=0.3):
    """A rough monotone time for every text unit from the global alignment anchors {unit: time}."""
    if not anchors:
        return None
    pts = sorted(anchors.items())
    keep = monotone_subset([(j, t, 1.0) for j, t in pts])
    js = np.array([pts[k][0] for k in keep], float)
    ts = np.array([pts[k][1] for k in keep], float)
    idx = np.arange(n_units, dtype=float)
    g = np.interp(idx, js, ts)
    g = np.where(idx < js[0], ts[0] - (js[0] - idx) * per_unit, g)
    g = np.where(idx > js[-1], ts[-1] + (idx - js[-1]) * per_unit, g)
    return np.clip(g, 0.0, dur)


def collect_votes(windows, keys, sim, guide=None):
    """Local alignment of every window (restricted to its band of the text when a guide is given)."""
    votes = [[] for _ in keys]
    for win in windows:
        lo, hi = 0, len(keys)
        if guide is not None:
            band = np.nonzero((guide >= win.start - BAND_PAD_S) & (guide <= win.end + BAND_PAD_S))[0]
            if not len(band):
                continue
            lo, hi = max(0, int(band[0]) - BAND_PAD_UNITS), min(len(keys), int(band[-1]) + 1 + BAND_PAD_UNITS)
        for j, t in local_align(win.tokens, keys, sim, lo, hi):
            if win.valid(t):
                votes[j].append(t)
    return votes


def vote_time(times, prefer=None):
    """Median of the largest group of votes that lie within MERGE_S of each other -> (time, votes in group)."""
    if not times:
        return None, 0
    ts = sorted(times)
    groups = [[ts[0]]]
    for t in ts[1:]:
        if t - groups[-1][-1] <= MERGE_S:
            groups[-1].append(t)
        else:
            groups.append([t])
    g = max(groups, key=lambda g: (len(g), -abs(float(np.median(g)) - prefer) if prefer is not None else 0.0))
    return float(np.median(g)), len(g)


@dataclass
class Alignment:
    stream: list                 # merged ASR events kept for the global alignment
    ops: list                    # global alignment of stream onto the text units
    times: list                  # per unit: ASR time (None = not recognised), outliers removed
    support: list                # per unit: windows that agree on that time
    coverage: list               # per unit: windows whose non-edge part covers that time
    outliers: list               # unit indices whose time was out of order and dropped

    @property
    def matched(self):
        return sum(t is not None for t in self.times)


def align_units(windows, units, sim, dur, use_band=True):
    keys = [u.key for u in units]
    stream = supported(merge_windows(windows), windows)
    ops = global_align([c.key for c in stream], keys, sim)
    anchors = {j: stream[i].time for i, j in ops
               if i is not None and j is not None and sim.kind(stream[i].key, keys[j])}
    guide = time_guide(len(keys), anchors, dur) if use_band else None
    votes = collect_votes(windows, keys, sim, guide)
    times, support = [None] * len(keys), [0] * len(keys)
    for j in range(len(keys)):
        times[j], support[j] = vote_time(votes[j], None if guide is None else float(guide[j]))
        if times[j] is None and j in anchors:
            times[j], support[j] = anchors[j], 1
    pts = [(j, t, support[j]) for j, t in enumerate(times) if t is not None]
    keep = {pts[k][0] for k in monotone_subset(pts)}
    outliers = [j for j, _, _ in pts if j not in keep]
    for j in outliers:
        times[j], support[j] = None, 0
    coverage = [sum(1 for w in windows if w.valid(t)) if t is not None else 0 for t in times]
    return Alignment(stream, ops, times, support, coverage, outliers)


# ----------------------------------------------------------------------------------------------------------- audio

def require_ffmpeg():
    if shutil.which('ffmpeg') is None:
        raise AlignError('ffmpeg not found on PATH (install it, e.g. apt-get install ffmpeg)')


def decode(path, sr, channels, start=0.0, duration=None):
    """ffmpeg -> float32 array (channels, n)."""
    cmd = ['ffmpeg', '-v', 'error', '-nostdin']
    if start:
        cmd += ['-ss', f'{start:.6f}']
    cmd += ['-i', str(path)]
    if duration is not None:
        cmd += ['-t', f'{duration:.6f}']
    cmd += ['-vn', '-ac', str(channels), '-ar', str(sr), '-f', 'f32le', '-']
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        raise AlignError(f'ffmpeg could not decode {path}: {p.stderr.decode(errors="replace").strip()[-400:]}')
    x = np.frombuffer(p.stdout, np.float32)
    return x[:len(x) // channels * channels].reshape(-1, channels).T


def leading_silence(x, sr):
    loud = np.nonzero(np.abs(x).max(0) > SILENCE_LEVEL)[0]
    return float(loud[0] / sr) if len(loud) else 0.0


def write_wav(path, x, sr):
    """32-bit float WAV (no clipping of separation output above full scale)."""
    from scipy.io import wavfile
    wavfile.write(str(path), sr, np.ascontiguousarray(x.T, dtype=np.float32))


def download(url, dest):
    """urllib download to dest + '.part', renamed when complete."""
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    part = dest.with_name(dest.name + '.part')
    hint = f'Download it some other way and put it at {dest} (or pass --models DIR).'
    log(f'downloading {url}')
    total = done = 0
    try:
        with urllib.request.urlopen(url, timeout=60) as r, open(part, 'wb') as f:
            total, mark = int(r.headers.get('Content-Length') or 0), 0.25
            while True:
                block = r.read(1 << 20)
                if not block:
                    break
                f.write(block)
                done += len(block)
                if total and done / total >= mark:
                    log(f'  {done / 1e6:.0f} / {total / 1e6:.0f} MB')
                    mark += 0.25
    except urllib.error.HTTPError as e:
        part.unlink(missing_ok=True)
        raise AlignError(f'download refused: HTTP {e.code} {e.reason} for {url}\n  {hint}') from None
    except (urllib.error.URLError, OSError) as e:
        part.unlink(missing_ok=True)
        reason = str(getattr(e, 'reason', e))
        what = 'download refused by the network/proxy' if re.search(r'\b40[37]\b', reason) else 'download failed'
        raise AlignError(f'{what} for {url}: {reason}\n  {hint}') from None
    if total and done != total:
        part.unlink(missing_ok=True)
        raise AlignError(f'download of {url} stopped at {done} of {total} bytes; run again. {hint}')
    os.replace(part, dest)


def extract_members(tar_path, dest_dir, names):
    """Extract only the named files (by base name) from a .tar.bz2 into dest_dir."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    found = set()
    try:
        with tarfile.open(tar_path, 'r:bz2') as tf:
            for member in tf:
                base = posixpath.basename(member.name)
                if base in names and base not in found and member.isfile():
                    part = dest_dir / (base + '.part')
                    with tf.extractfile(member) as src, open(part, 'wb') as f:
                        shutil.copyfileobj(src, f, 1 << 20)
                    os.replace(part, dest_dir / base)
                    found.add(base)
                    if found == set(names):
                        break
    except (tarfile.TarError, EOFError, OSError) as e:
        raise AlignError(f'cannot extract {tar_path}: {e} (delete it and run again)') from None
    missing = set(names) - found
    if missing:
        raise AlignError(f'{tar_path} does not contain {", ".join(sorted(missing))}')


def ensure_uvr(models):
    path = models / UVR_FILE
    if not path.is_file():
        download(UVR_URL, path)
    return path


def ensure_sensevoice(models):
    d = models / SV_NAME
    if all((d / f).is_file() for f in SV_FILES):
        return d
    tar = models / f'{SV_NAME}.tar.bz2'
    if not tar.is_file():
        download(SV_URL, tar)
    log(f'extracting {", ".join(SV_FILES)} from {tar.name}')
    extract_members(tar, d, SV_FILES)
    tar.unlink()
    return d


def _stft(x, window):
    """(n,) -> (n_fft//2+1, frames) complex, like torch.stft(center=True, pad_mode='reflect')."""
    xp = np.pad(x, MDX_N_FFT // 2, mode='reflect')
    frames = 1 + (len(xp) - MDX_N_FFT) // MDX_HOP
    idx = np.arange(MDX_N_FFT)[None, :] + MDX_HOP * np.arange(frames)[:, None]
    return np.fft.rfft(xp[idx] * window, axis=1).T


def _istft(X, length, window):
    frames = np.fft.irfft(X.T, n=MDX_N_FFT, axis=1) * window
    out = np.zeros(MDX_N_FFT + MDX_HOP * (len(frames) - 1))
    norm = np.zeros_like(out)
    for t, frame in enumerate(frames):
        out[t * MDX_HOP:t * MDX_HOP + MDX_N_FFT] += frame
        norm[t * MDX_HOP:t * MDX_HOP + MDX_N_FFT] += window ** 2
    out /= np.maximum(norm, 1e-8)
    return out[MDX_N_FFT // 2:MDX_N_FFT // 2 + length]


def separate_vocals(mix, model_path, compensate=1.0):
    """UVR MDX-Net vocal separation of a (2, n) 44.1 kHz mix -> vocals (2, n)."""
    try:
        import onnxruntime as ort
    except ImportError:
        raise AlignError('onnxruntime is not installed: pip install onnxruntime --break-system-packages') from None
    chunk = MDX_HOP * (MDX_DIM_T - 1)
    trim = MDX_N_FFT // 2
    gen = chunk - 2 * trim
    n = mix.shape[1]
    pad = gen - n % gen
    padded = np.concatenate([np.zeros((2, trim), np.float32), mix.astype(np.float32),
                             np.zeros((2, pad + trim), np.float32)], 1)
    window = 0.5 - 0.5 * np.cos(2 * np.pi * np.arange(MDX_N_FFT) / MDX_N_FFT)   # periodic Hann
    try:
        sess = ort.InferenceSession(str(model_path), providers=['CPUExecutionProvider'])
    except Exception as e:
        raise AlignError(f'cannot load {model_path}: {e} (delete it to download again)') from None
    name = sess.get_inputs()[0].name
    parts, t0 = [], time.time()
    for i in range(0, n + pad, gen):
        seg = padded[:, i:i + chunk].astype(np.float64)
        specs = [_stft(seg[c], window) for c in range(2)]
        inp = np.stack([specs[0].real, specs[0].imag, specs[1].real, specs[1].imag])[:, :MDX_DIM_F]
        out = sess.run(None, {name: inp[None].astype(np.float32)})[0][0]
        chans = []
        for c in range(2):
            X = np.zeros((MDX_N_FFT // 2 + 1, MDX_DIM_T), complex)
            X[:MDX_DIM_F] = out[2 * c] + 1j * out[2 * c + 1]
            chans.append(_istft(X, chunk, window))
        parts.append(np.stack(chans)[:, trim:-trim])
        log(f'  separation {min(i + gen, n) / MIX_SR:6.1f} / {n / MIX_SR:.1f} s  ({time.time() - t0:.0f} s)')
    return np.concatenate(parts, 1)[:, :n] * compensate


class VocalEnvelope:
    """Level of the separated vocals. db: 30 ms RMS in dB every 10 ms (line ends, onsets).
    rise: positive steps of the log mean-abs envelope every 5 ms, smoothed over 20 ms (snapping unit onsets)."""

    def __init__(self, mono, sr):
        x = np.asarray(mono, np.float64)
        self.hop = 0.01
        h = int(sr * self.hop)
        csum = np.concatenate([[0.0], np.cumsum(x * x)])
        centres = np.arange(0, len(x), h)
        a = np.clip(centres - 3 * h // 2, 0, len(x))
        b = np.clip(centres - 3 * h // 2 + 3 * h, 0, len(x))
        self.db = 10 * np.log10((csum[b] - csum[a]) / (3 * h) + 1e-12)
        self.rise_hop = 0.005
        h2 = int(sr * self.rise_hop)
        frames = len(x) // h2
        env = np.abs(x[:frames * h2]).reshape(frames, h2).mean(1) if frames else np.zeros(1)
        lv = np.log(np.convolve(env, np.ones(4) / 4, 'same') + 1e-4)
        self.rise = np.maximum(0.0, np.diff(lv, prepend=lv[0]))

    def frame(self, t):
        return int(min(len(self.db) - 1, max(0, round(t / self.hop))))


def snap_onset(env, t):
    """Strongest envelope rise in [t - 0.14, t + 0.04] (else t - 0.05). A rise only counts if the vocals right after
    it are within SNAP_FLOOR_DB of the coming local peak (log-envelope rises in near silence are separation
    residue). A time that still lies in vocal silence moves forward to the voice onset if one follows within
    SNAP_FORWARD."""
    db, r, h = env.db, env.rise, env.rise_hop
    floor = db[env.frame(t - 0.3):env.frame(t + 1.0) + 1].max() - SNAP_FLOOR_DB
    i0, i1 = max(0, int((t - SNAP_BEFORE) / h)), min(len(r), int((t + SNAP_AFTER) / h))
    best = None
    for k in range(i0, i1):
        if r[k] > SNAP_MIN_RISE and (best is None or r[k] > r[best]):
            if db[env.frame(k * h):env.frame(k * h + 0.04) + 1].max() > floor:
                best = k
    s = best * h if best is not None else max(0.0, t - SNAP_DEFAULT)
    a, b = env.frame(s), env.frame(s + 0.05)
    if db[a:b + 1].max() <= floor:
        ahead = np.nonzero(db[a:env.frame(s + SNAP_FORWARD) + 1] > floor)[0]
        if len(ahead):
            s = (a + int(ahead[0])) * env.hop
    return s


def voiced_segments(env, lo, hi, thr):
    """[(start_time, end_time)] where the vocal level is above thr in [lo, hi], dips < ONSET_MAX_DIP bridged.
    A segment that is already voiced at lo gets start None (no onset visible)."""
    db, h = env.db, env.hop
    a, b = max(0, int(math.ceil(lo / h))), min(len(db), int(hi / h))
    dip = int(round(ONSET_MAX_DIP / h))
    segs, k = [], a
    while k < b:
        if db[k] <= thr:
            k += 1
            continue
        s = e = k
        while k < b and (db[k] > thr or k - e <= dip):
            if db[k] > thr:
                e = k
            k += 1
        rising = s > a or (a > 0 and db[a - 1] <= thr)
        segs.append((s * h if rising else None, e * h))
    return segs


def energy_onset(env, t_first, n_missing, spacing, lo):
    """Where a line starts whose first n_missing units were not recognised, searching back from its first
    recognised unit t_first to lo: the vocal onset closest to t_first - n_missing * spacing.
    Returns (time, found_in_energy)."""
    expect = max(lo, t_first - n_missing * spacing)
    lo = max(lo, t_first - n_missing * 0.6 - 0.6, 0.0)
    if t_first - lo < 0.05:
        return expect, False
    thr = env.db[env.frame(lo):env.frame(t_first + 0.5) + 1].max() - ONSET_DROP_DB
    starts = [s for s, _ in voiced_segments(env, lo, t_first, thr) if s is not None and s <= t_first - 0.05]
    if not starts:
        return expect, False
    return min(starts, key=lambda s: abs(s - expect)), True


def line_end(env, t_first, t_last, cap):
    """Vocal level stays within END_DROP_DB of the line's peak, then + END_TAIL; at least t_last + END_MIN;
    never after cap."""
    db = env.db
    a, b = env.frame(t_first), env.frame(t_last)
    peak = db[a:b + 30].max()
    k = b
    while k < len(db) - 1 and k * env.hop < cap and db[k] > peak - END_DROP_DB:
        k += 1
    return min(max(k * env.hop + END_TAIL, t_last + END_MIN), cap)


# ------------------------------------------------------------------------------------------------------------- ASR

def make_recognizer(sv_dir, lang):
    try:
        import sherpa_onnx
    except ImportError:
        raise AlignError('sherpa-onnx is not installed: pip install sherpa-onnx --break-system-packages') from None
    return sherpa_onnx.OfflineRecognizer.from_sense_voice(
        model=str(sv_dir / 'model.int8.onnx'), tokens=str(sv_dir / 'tokens.txt'), use_itn=False,
        language=lang, num_threads=2)


def asr_input(mono):
    from scipy.signal import resample_poly
    x16 = resample_poly(np.asarray(mono, np.float64), 160, 441).astype(np.float32)
    x16 /= max(1e-6, float(np.abs(x16).max())) * 1.1
    return x16


def run_asr(recognizer, x16, env, sizes, step):
    """SenseVoice over overlapping windows of each size. Returns ([Window], windows skipped as silent)."""
    dur = len(x16) / ASR_SR
    loudest = float(env.db.max())
    windows, skipped, t0 = [], 0, time.time()
    for size in sizes:
        t = 0.0
        while t == 0.0 or t < dur - 2.0:
            seg = x16[int(t * ASR_SR):int((t + size) * ASR_SR)]
            end = t + len(seg) / ASR_SR
            if env.db[env.frame(t):env.frame(end) + 1].max() < loudest - SILENT_WINDOW_DB:
                skipped += 1
            else:
                s = recognizer.create_stream()
                s.accept_waveform(ASR_SR, seg)
                recognizer.decode_stream(s)
                r = s.result
                if r.tokens and len(r.timestamps) != len(r.tokens):
                    raise AlignError('this sherpa-onnx build gives no token timestamps; '
                                     'pip install -U sherpa-onnx --break-system-packages')
                windows.append(Window(t, end, t + EDGE_S if t > 0 else -math.inf,
                                      end - EDGE_S if end < dur - 1e-6 else math.inf,
                                      asr_units(r.tokens, r.timestamps, t)))
            t += step
        log(f'  ASR {size:g} s windows done ({time.time() - t0:.0f} s)')
    return windows, skipped


# ---------------------------------------------------------------------------------------------------------- timing

@dataclass
class LineResult:
    index: int
    start: float = 0.0
    end: float = 0.0
    unit_times: list = field(default_factory=list)
    matched: int = 0
    total: int = 0
    flags: list = field(default_factory=list)


def typical_spacing(t, known):
    steps = [(t[b] - t[a]) / (b - a) for a, b in zip(known, known[1:])]
    return float(np.clip(np.median(steps), 0.15, 0.6)) if steps else 0.3


def compute_timings(lines, units, times, env, dur):
    """Per-unit ASR times (None = missed) -> ([LineResult] in order, [dropped line indices])."""
    by_line = [[] for _ in lines]
    for j, u in enumerate(units):
        by_line[u.line].append(j)
    t = list(times)
    has = [any(t[j] is not None for j in idx) for idx in by_line]
    found = [i for i, h in enumerate(has) if h]
    if not found:
        return [], list(range(len(lines)))
    keep = [i for i in range(found[0], found[-1] + 1) if by_line[i]]
    dropped = [i for i in range(len(lines)) if i not in set(keep)]
    asr = [v is not None for v in t]
    t = [snap_onset(env, v) if v is not None else None for v in t]
    first_known = {i: next(t[j] for j in by_line[i] if t[j] is not None) for i in keep if has[i]}
    results, prev_last = [], None
    for pos, i in enumerate(keep):
        idx = by_line[i]
        res = LineResult(i, matched=sum(asr[j] for j in idx), total=len(idx))
        next_first = next((first_known[k] for k in keep[pos + 1:] if k in first_known), dur)
        lo = prev_last + 0.2 if prev_last is not None else 0.0
        if not has[i]:
            # the neighbouring lines can leave no room at all (previous line's tail runs into the next line's
            # first recognised unit): search at least a short window instead of an empty one
            hi = max(next_first, lo + 0.3)
            seg = env.db[env.frame(lo):env.frame(hi) + 1]
            thr = (seg.max() if seg.size else float(env.db.max())) - ONSET_DROP_DB
            onsets = [s for s, _ in voiced_segments(env, lo, hi - 0.2, thr) if s is not None] if hi - 0.2 > lo else []
            onset = onsets[0] if onsets else lo
            step = max(0.05, min(0.3, (hi - 0.2 - onset) / len(idx)))
            for q, j in enumerate(idx):
                t[j] = onset + q * step
            res.flags.append('no ASR match: placed by vocal energy' if next_first - lo >= 0.3
                             else 'no ASR match and no room between neighbours: rough placement, check by ear')
        else:
            known = [j for j in idx if t[j] is not None]
            spacing = typical_spacing(t, known)
            for a, b in zip(known, known[1:]):
                for j in range(a + 1, b):
                    t[j] = snap_onset(env, t[a] + (t[b] - t[a]) * (j - a) / (b - a))
            head = known[0] - idx[0]
            if head:
                onset, from_energy = energy_onset(env, t[known[0]], head, spacing, lo)
                for q in range(head):
                    t[idx[q]] = onset + (t[known[0]] - onset) * q / head
                res.flags.append('start from vocal energy' if from_energy else 'start estimated (no clear onset)')
            tail = idx[-1] - known[-1]
            if tail:
                room = next_first - END_GUARD - t[known[-1]]
                step = max(0.05, min(spacing, room / (tail + 1)))
                for q in range(1, tail + 1):
                    t[known[-1] + q] = t[known[-1]] + q * step
                res.flags.append(f'last {tail} unit(s) not recognised')
        prev_last = t[idx[-1]]
        results.append(res)
    order = [j for i in keep for j in by_line[i]]
    for a, b in zip(order, order[1:]):
        if t[b] <= t[a] + COLLIDE:
            t[b] = t[a] + MIN_GAP
    for pos, res in enumerate(results):
        idx = by_line[res.index]
        res.unit_times = [t[j] for j in idx]
        res.start, last = t[idx[0]], t[idx[-1]]
        cap = t[by_line[results[pos + 1].index][0]] - END_GUARD if pos + 1 < len(results) else dur - 0.1
        res.end = max(line_end(env, res.start, last, cap), last + 0.05)
    return results, dropped


def char_times(line, line_units, unit_times, space_times=False):
    """One time per character of line.text, skipping ASCII spaces unless space_times. The characters of a unit
    take its time; punctuation takes the previous unit's time (the next one's at the line start); spaces take the
    next character's time."""
    text = line.text
    per = [None] * len(text)
    for u, t in zip(line_units, unit_times):
        for p in u.positions:
            per[p] = t
    last = None
    for p, ch in enumerate(text):
        if ch != ' ':
            per[p] = last if per[p] is None else per[p]
            last = per[p]
    nxt = None
    for p in range(len(text) - 1, -1, -1):
        if text[p] == ' ':
            per[p] = nxt if nxt is not None else last
        else:
            per[p] = nxt if per[p] is None else per[p]
            nxt = per[p]
    return [per[p] for p, ch in enumerate(text) if ch != ' ' or space_times]


# ---------------------------------------------------------------------------------------------------------- report

def heard_by_line(al, units, sim, n_lines):
    """Per line: [(heard key or None, text key or None, kind)] from the global alignment, kind in
    exact / near / sub / missing / extra (extra tokens are kept only inside a line)."""
    per = [[] for _ in range(n_lines)]
    cur, pending = None, []
    for i, j in al.ops:
        if j is None:
            if cur is not None:
                pending.append((al.stream[i].key, None, 'extra'))
            continue
        line = units[j].line
        if line == cur:
            per[cur] += pending
        pending, cur = [], line
        if i is None:
            per[line].append((None, units[j].key, 'missing'))
        else:
            per[line].append((al.stream[i].key, units[j].key, sim.kind(al.stream[i].key, units[j].key) or 'sub'))
    return per


def join_keys(keys):
    out = ''
    for k in keys:
        if out and not CJK_RE.fullmatch(k) and not CJK_RE.fullmatch(out[-1]):
            out += ' '
        out += k
    return out


def describe_diff(entries):
    heard = join_keys(['_' if h is None else h for h, _, kind in entries if kind != 'extra' or h])
    notes = []
    near = [f'{u}→{h}' for h, u, k in entries if k == 'near']
    sub = [f'{u}→{h}' for h, u, k in entries if k == 'sub']
    missing = sum(k == 'missing' for _, _, k in entries)
    extra = [h for h, _, k in entries if k == 'extra']
    if near:
        notes.append('sounds alike (pinyin/--eq), text kept: ' + ' '.join(near))
    if sub:
        notes.append('heard differently: ' + ' '.join(sub))
    if missing:
        notes.append(f'{missing} not heard')
    if extra:
        notes.append('extra: ' + join_keys(extra))
    return heard, '; '.join(notes)


ENERGY_FLAGS = ('start ', 'no ASR match')


def md_cell(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


def write_report(path, info, lines, results, dropped, diffs, drift, instrumental=None, warning=None):
    out = ['# Lyric alignment report', '']
    if warning:
        out += [f'> **{warning}**', '']
    out += [f'- {k}: {v}' for k, v in info]
    if instrumental:
        out += ['', '## INSTRUMENTAL', '', instrumental]
    if results:
        out += ['', '## Lines', '', '| # | start | end | recognised | flags | text |', '|---|---|---|---|---|---|']
        for r in results:
            out.append(f'| {r.index + 1} | {r.start:.3f} | {r.end:.3f} | {r.matched}/{r.total} | '
                       f'{md_cell("; ".join(r.flags))} | {md_cell(lines[r.index].text)} |')
    if diffs:
        out += ['', '## ASR heard something else (text kept; check against the singing)', '',
                '| # | start | text | heard | notes |', '|---|---|---|---|---|']
        out += [f'| {i + 1} | {s:.3f} | {md_cell(lines[i].text)} | {md_cell(h)} | {md_cell(n)} |'
                for i, s, h, n in diffs]
    energy = [r for r in results if any(f.startswith(ENERGY_FLAGS) for f in r.flags)]
    if energy:
        out += ['', '## Starts not from a recognised unit', '']
        out += [f'- line {r.index + 1} at {r.start:.3f}: {r.flags[0]} — {lines[r.index].text}' for r in energy]
    low = [r for r in results if 'LOW CONFIDENCE' in ' '.join(r.flags)]
    if low:
        out += ['', '## Low confidence', '']
        out += [f'- line {r.index + 1} at {r.start:.3f}: {"; ".join(r.flags)} — {lines[r.index].text}' for r in low]
    if dropped:
        out += ['', '## Not found in the audio (left out of the JSON)', '']
        out += [f'- line {i + 1}: {lines[i].text}' for i in dropped]
    if drift:
        out += ['', '## LRC drift (aligned start − LRC start, in output time)', '',
                '| # | LRC | aligned | drift | text |', '|---|---|---|---|---|']
        out += [f'| {i + 1} | {lrc:.3f} | {s:.3f} | {s - lrc:+.3f} | {md_cell(lines[i].text)} |' for i, lrc, s in drift]
        if len(drift) >= 3:
            a, b = np.polyfit([d[1] for d in drift], [d[2] for d in drift], 1)
            out += ['', f'Linear fit: aligned ≈ {a:.4f} × LRC {b:+.3f} s (slope ≠ 1: the LRC is from a version at '
                        f'another tempo, {(1 / a - 1) * 100:+.1f}% vocal speed vs LRC).']
    Path(path).write_text('\n'.join(out) + '\n', encoding='utf-8')


def write_rows(path, rows):
    body = ',\n'.join(' ' + json.dumps(r, ensure_ascii=False) for r in rows)
    Path(path).write_text('[\n' + body + '\n]\n', encoding='utf-8')


# ------------------------------------------------------------------------------------------------------------ main

def build_parser():
    p = argparse.ArgumentParser(description=__doc__.split('\n\n')[0],
                                epilog='Exit codes: 0 ok, 1 error, 3 instrumental (no vocals recognised).')
    p.add_argument('song', help='audio file (anything ffmpeg decodes)')
    p.add_argument('lyrics', help='UTF-8 text (one line per lyric line) or .lrc')
    p.add_argument('--out', required=True, help='output JSON, e.g. data/lyrics.json')
    p.add_argument('--from', dest='start', type=float, default=None, metavar='S', help='analyse from S seconds')
    p.add_argument('--to', dest='end', type=float, default=None, metavar='S', help='analyse up to S seconds')
    p.add_argument('--trim-s0', action='store_true', help='output times relative to the first non-silent sample')
    p.add_argument('--vocals', help='separated vocals of exactly this range (e.g. <out>.vocals.wav): skip separation')
    p.add_argument('--models', default=DEFAULT_MODELS, help=f'model cache folder (default {DEFAULT_MODELS})')
    p.add_argument('--compensate', type=float, default=1.0, help='vocal volume compensation (1.021 for this model '
                                                                 'in one old project; default 1.0)')
    p.add_argument('--eq', action='append', metavar='PAIRS', help='extra near-match pairs, e.g. 偷不,掉到 or baby/bae')
    p.add_argument('--lang', default='zh', choices=('zh', 'yue', 'en', 'ja', 'ko', 'auto'), help='SenseVoice language')
    p.add_argument('--windows', default='10,13', help='ASR window sizes in seconds (default 10,13)')
    p.add_argument('--step', type=float, default=2.0, help='seconds between window starts (default 2)')
    p.add_argument('--space-times', action='store_true', help='4th element also has a time for each ASCII space')
    return p


def run(args):
    t_all = time.time()
    stages = {}
    if args.start is not None and args.start < 0:
        raise AlignError('--from must be >= 0')
    start = args.start or 0.0
    if args.end is not None and args.end <= start:
        raise AlignError('--to must be after --from')
    try:
        sizes = [float(s) for s in args.windows.split(',') if s.strip()]
    except ValueError:
        raise AlignError(f'--windows {args.windows!r}: give sizes in seconds like 10,13') from None
    if not sizes or not all(4 <= s <= 30 for s in sizes) or args.step <= 0:
        raise AlignError('--windows sizes must be 4..30 s and --step > 0')
    eq_pairs = parse_eq(args.eq)
    require_ffmpeg()
    for f in (args.song, args.lyrics) + ((args.vocals,) if args.vocals else ()):
        if not Path(f).is_file():
            raise AlignError(f'file not found: {f}')

    lines, is_lrc, credits = read_lyrics(args.lyrics)
    if is_lrc and (args.start is not None or args.end is not None):
        lines = filter_lrc_range(lines, start, args.end)
    units = text_units(lines)
    if not units:
        raise AlignError(f'no lyric lines with characters found in {args.lyrics}')
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    report_path = out.with_suffix('.report.md')

    tic = time.time()
    mix = decode(args.song, MIX_SR, 2, start, None if args.end is None else args.end - start)
    if mix.shape[1] < MIX_SR:
        raise AlignError(f'less than 1 s of audio decoded from {args.song} in the requested range')
    dur = mix.shape[1] / MIX_SR
    s0 = leading_silence(mix, MIX_SR)
    stages['decode'] = time.time() - tic
    log(f'{dur:.1f} s of audio, leading digital silence S0 = {s0:.3f} s')
    models = Path(args.models).expanduser()

    tic = time.time()
    if args.vocals:
        vocals = decode(args.vocals, MIX_SR, 2)
        if abs(vocals.shape[1] - mix.shape[1]) > 0.1 * MIX_SR:
            log(f'warning: --vocals is {vocals.shape[1] / MIX_SR:.2f} s but the analysed range is {dur:.2f} s; '
                'it must be the vocals of exactly this range')
        vocal_note = f'reused {args.vocals}'
    else:
        uvr = ensure_uvr(models)
        log('separating vocals (UVR-MDX-NET-Voc_FT)')
        vocals = separate_vocals(mix, uvr, args.compensate)
        voc_path, inst_path = out.with_suffix('.vocals.wav'), out.with_suffix('.inst.wav')
        write_wav(voc_path, vocals, MIX_SR)
        write_wav(inst_path, mix - vocals, MIX_SR)
        vocal_note = f'UVR-MDX-NET-Voc_FT, compensate {args.compensate:g} → {voc_path} (+ {inst_path.name})'
    del mix
    stages['separation'] = time.time() - tic

    tic = time.time()
    mono = vocals.mean(0)
    del vocals
    env = VocalEnvelope(mono, MIX_SR)
    recognizer = make_recognizer(ensure_sensevoice(models), args.lang)
    log(f'ASR: SenseVoice ({args.lang}), windows {args.windows} s every {args.step:g} s')
    windows, skipped = run_asr(recognizer, asr_input(mono), env, sizes, args.step)
    stages['asr'] = time.time() - tic

    tic = time.time()
    sim = Similarity(eq_pairs)
    if not sim.has_pinyin:
        log('note: pypinyin not installed, homophones are not matched (pip install pypinyin --break-system-packages)')
    al = align_units(windows, units, sim, dur)
    shift = s0 if args.trim_s0 else 0.0
    info = [('song', f'{args.song}' + (f' (range {start:.3f}–{args.end:.3f} s)' if args.end is not None else
                                       f' (from {start:.3f} s)' if start else '')),
            ('lyrics', f'{args.lyrics} ({"LRC" if is_lrc else "text"}, {len(lines)} lines, {len(units)} units)'),
            ('analysed audio', f'{dur:.2f} s'),
            ('leading digital silence S0', f'{s0:.3f} s (first sample with |x| > {SILENCE_LEVEL:g}) — ' +
             ('output times are relative to S0 (--trim-s0)' if args.trim_s0 else
              'output times are NOT shifted (relative to --from); use --trim-s0 if the clip is cut from S0')),
            ('vocals', vocal_note),
            ('ASR', f'SenseVoice {args.lang}, windows {args.windows} s every {args.step:g} s: {len(windows)} decoded, '
                    f'{skipped} skipped as silent'),
            ('recognised units', f'{al.matched} / {len(units)} ({100 * al.matched / len(units):.1f}%)'),
            ('homophones', 'same fuzzy pinyin' + (' + --eq pairs' if eq_pairs else '') if sim.has_pinyin else
             ('only --eq pairs' if eq_pairs else 'off') + ' (pypinyin not installed)')]
    if credits:
        info.append(('credit lines skipped', ' / '.join(credits)))

    if al.matched < INSTRUMENTAL_RATIO * len(units):
        heard = join_keys([c.key for c in al.stream])[:300] or '(nothing)'
        verdict = (f'INSTRUMENTAL: only {al.matched} of {len(units)} lyric units ({100 * al.matched / len(units):.1f}%) '
                   f'were recognised in the separated vocals. No alignment written.')
        write_report(report_path, info + [('ASR heard', heard)], lines, [], [], [], [], verdict)
        print(verdict)
        print(f'report: {report_path}')
        return 3

    results, dropped = compute_timings(lines, units, al.times, env, dur)
    unit_index = {}
    for j, u in enumerate(units):
        unit_index.setdefault(u.line, []).append(j)
    for r in results:
        idx = unit_index[r.index]
        ratios = [al.support[j] / al.coverage[j] for j in idx if al.times[j] is not None and al.coverage[j]]
        reasons = []
        if r.matched < 0.5 * r.total:
            reasons.append(f'only {r.matched}/{r.total} recognised')
        if ratios and float(np.mean(ratios)) < 0.3:
            reasons.append(f'windows agree {float(np.mean(ratios)):.0%}')
        if any(j in al.outliers for j in idx):
            reasons.append('out-of-order times dropped')
        if r.total / max(0.05, r.unit_times[-1] - r.start + 0.3) > 9:
            reasons.append('implausibly fast')
        if reasons:
            r.flags.append('LOW CONFIDENCE: ' + ', '.join(reasons))

    rows = []
    for r in results:
        line = lines[r.index]
        times = char_times(line, [units[j] for j in unit_index[r.index]], r.unit_times, args.space_times)
        rows.append([round(max(0.0, r.start - shift), 3), round(max(0.0, r.end - shift), 3), line.text,
                     [round(max(0.0, t - shift), 3) for t in times]])
    order = sorted(range(len(rows)), key=lambda k: rows[k][0])
    rows = [rows[k] for k in order]
    results = [results[k] for k in order]
    write_rows(out, rows)

    diffs = []
    for r, entries in ((r, heard_by_line(al, units, sim, len(lines))[r.index]) for r in results):
        if any(kind != 'exact' for _, _, kind in entries):
            heard, notes = describe_diff(entries)
            diffs.append((r.index, r.start - shift, heard, notes))
    drift = []
    if is_lrc:
        drift = [(r.index, lines[r.index].lrc_time - start - shift, r.start - shift) for r in results]
    stages['align'] = time.time() - tic
    total = time.time() - t_all
    info.append(('runtime', ', '.join(f'{k} {v:.1f} s' for k, v in stages.items()) +
                 f'; total {total:.1f} s = {total / (dur / 60):.1f} s per minute of audio'))
    low_match = al.matched < MISMATCH_RATIO * len(units)
    warning = (f'LOW MATCH: only {al.matched} of {len(units)} lyric units ({100 * al.matched / len(units):.1f}%) were '
               f'recognised. The lyrics are probably for a different song or version, or the range is wrong; '
               f'check before using these timings.') if low_match else None
    write_report(report_path, info, lines, results, dropped, diffs, drift, warning=warning)

    n_energy = sum(any(f.startswith(ENERGY_FLAGS) for f in r.flags) for r in results)
    n_low = sum('LOW CONFIDENCE' in ' '.join(r.flags) for r in results)
    print(f'aligned {len(rows)} lines, {al.matched}/{len(units)} units recognised '
          f'({100 * al.matched / len(units):.1f}%) -> {out}')
    print(f'S0 (leading digital silence) {s0:.3f} s' +
          (' (times relative to S0)' if args.trim_s0 else ' (times not shifted; --trim-s0 to cut from S0)'))
    print(f'{len(diffs)} lines differ from ASR, {n_energy} starts from vocal energy, {n_low} low confidence, '
          f'{len(dropped)} not found -> {report_path}')
    if drift:
        d = [s - lrc for _, lrc, s in drift]
        print(f'LRC drift: first {d[0]:+.2f} s, last {d[-1]:+.2f} s, range {min(d):+.2f} .. {max(d):+.2f} s')
    print(f'runtime {total:.0f} s for {dur:.0f} s of audio ({total / (dur / 60):.0f} s per minute)')
    if warning:
        print(warning)
        return 4
    return 0


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        return run(args)
    except AlignError as e:
        print(f'error: {e}', file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        return 130


if __name__ == '__main__':
    sys.exit(main())
