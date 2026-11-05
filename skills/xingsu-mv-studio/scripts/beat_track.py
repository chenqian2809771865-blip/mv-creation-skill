#!/usr/bin/env python3
"""beat_track.py SONG --out beats.json [--from S --to S] [--relative] [--meter 4] [--bpm-hint 128]
                    [--bpm-min 70 --bpm-max 180] [--click check.wav] [-q]

Measured per-beat table for 卡点 (cutting / animating on the beat). numpy + scipy + ffmpeg only (no librosa).
numpy/scipy port of the validated beats_refine.py (会不会 / 病变 / 新地球 / 失眠): same features (its envelope,
kick band and beats reproduce to <0.1 ms on the same audio) and JSON keys, plus downbeats / conf / drift. Changed:
the beats are TRACKED (beats_refine.py snapped a constant grid, which loses the beat once the tempo has drifted
more than 35 ms away from it), the tempo range is --bpm-min..--bpm-max with an octave check, beats sit on the attack.

  1. HPSS: median filter of the STFT magnitude along time (harmonic) and along frequency (percussive), kernel 31,
     Wiener soft masks; onset envelope = mel log-power spectral flux of the percussive signal (hop 128 = 5.8 ms).
  2. Seed tempo from the autocorrelation of the mean-removed envelope, in --bpm-min..--bpm-max. Octave: with
     --bpm-hint the autocorrelation peak near the hint; otherwise go up an octave while the pulses halfway
     between beats are >= 0.5 x as strong as the beats (backbeat snares -> fast level; only hats -> slow).
     Seed phase + local tempo: comb search (2 ms steps, +-3 % tempo) on the strongest 16-beat passage.
  3. Tracking forward and backward from the seed through the whole range: each beat is predicted from a
     strength-weighted line through the previous 9 (so drift accumulates), then snapped to the highest onset-
     envelope peak within +-35 ms that rises clearly above the local level. No such peak -> the prediction is
     kept, conf 0. After 4 misses in a row an 8-beat comb re-locks when the drums come back (small phase/tempo
     correction; a big one only after 8 misses and 7 of 8 comb hits). Runs of misses are bridged by
     interpolation between the found beats around them. Then the sliding 9-beat linear fit, weighted by onset
     strength (sqrt-weighted rows) and evaluated at the centre beat: tempo may drift, single picks don't jitter.
  4. Downbeats: chroma (12 classes from the harmonic STFT); novelty[k] = 1 - cos(chroma over beats k-2..k,
     chroma over k..k+2); phase p = argmax mean(z(novelty)[p::meter]) + 0.5 mean(z(kick)[p::meter]).
  5. Per-beat band energies in -20..+100 ms: kick 30-120 Hz, snare 1.5-5 kHz, hat 6-11 kHz (percussive part),
     bass 30-150 Hz (full mix). The table printed per beat (ratios to median) shows drops, gaps and accents.
  6. --click out.wav: the audio of the range with a click on every beat and a higher, louder one on downbeats.
     The wav starts at --from (file time "from" in the JSON).

JSON: src/file, time_base ("file": seconds from the start of the input file; "from": seconds from --from, with
--relative), from, to, s0 (first sample with |x| > 1e-4, same time base), bpm (median of the tracked beats),
bpm_half, bpm_seed, beat (60/bpm), meter, beats, conf (per beat: onset height / typical beat-onset height, capped
at 1; picks need >= 0.3; 0 = no clear onset, the tracked prediction is kept), downbeats, downbeat_phase
(beats[p::meter] are the bar first beats), downbeat_conf (0..1 margin of the best bar phase over the 2nd),
drift_ms_max (max |beat - best constant grid|), low_conf_beats (count of conf 0), kick, snare, bass, hat, nov.

Render code: interpolate the beat table instead of a constant BPM. Python (importable from this file too):

    import bisect
    def beat_at(t, beats):        # fractional beat index; edge tempo extrapolates
        i = min(max(bisect.bisect_right(beats, t) - 1, 0), len(beats) - 2)
        return i + (t - beats[i]) / (beats[i + 1] - beats[i])
    def time_of(b, beats):        # inverse: time of fractional beat index b
        i = min(max(int(b // 1), 0), len(beats) - 2)
        return beats[i] + (b - i) * (beats[i + 1] - beats[i])

JS (painted-character core.js: replace `bpOf`; BEATS = beats.json "beats" in video time, beat 0 = BEATS[0];
bar position = (bpOf(t) - downbeat_phase) / meter):

    const bpOf = t => { let lo = 0, hi = BEATS.length - 2; while (lo < hi) { const m = (lo + hi + 1) >> 1;
      if (BEATS[m] <= t) lo = m; else hi = m - 1; } return lo + (t - BEATS[lo]) / (BEATS[lo + 1] - BEATS[lo]); };
    const timeOf = b => { const i = Math.min(Math.max(Math.floor(b), 0), BEATS.length - 2);
      return BEATS[i] + (b - i) * (BEATS[i + 1] - BEATS[i]); };
"""
import argparse, bisect, json, subprocess, sys, time
import numpy as np
from scipy import fft as sfft, ndimage

SR = 22050          # analysis rate (as beats_refine.py / beat_grid.py)
N_FFT = 2048
HOP_ONSET = 128     # onset envelope: 5.8 ms frames
HOP_BAND = 256      # band-energy frames; every 2nd one is an HPSS frame (hop 512)
HPSS_KERNEL = 31
PICK_WIN = 0.035    # +-35 ms peak search
PEAK_MIN = 0.3      # a pick must rise PEAK_MIN x the typical beat-onset height above the local (2 s median) level
FIT_LEN = 9         # sliding linear fit length (beats)
MARGIN = 3.0        # seconds of extra audio decoded around --from/--to for context
# The librosa-style envelope (onset_strength with its centre shift) peaks after the attack of a drum hit: +10.3 ms
# on synthetic kicks/snares with beats_refine.py, median +8..+22 ms on two real mixes. Beats are moved onto the attack
# by this much (--onset-delay 0 gives beats_refine.py's timing; band-energy windows stay on beats_refine.py's).
ONSET_DELAY = 0.010


# ---------------------------------------------------------------- beat-table helpers (importable)
def beat_at(t, beats):
    """Fractional beat index at time t (linear interpolation over beats, edge tempo extrapolates)."""
    i = min(max(bisect.bisect_right(beats, t) - 1, 0), len(beats) - 2)
    return i + (t - beats[i]) / (beats[i + 1] - beats[i])


def time_of(b, beats):
    """Time of fractional beat index b (inverse of beat_at)."""
    i = min(max(int(b // 1), 0), len(beats) - 2)
    return beats[i] + (b - i) * (beats[i + 1] - beats[i])


# ---------------------------------------------------------------- audio / spectra
def load_audio(path, start=0.0, dur=None, sr=SR, channels=1):
    cmd = ['ffmpeg', '-v', 'error', '-nostdin', '-ss', f'{start:.6f}'] + (['-t', f'{dur:.6f}'] if dur else []) + \
          ['-i', path, '-ac', str(channels), '-ar', str(sr), '-f', 'f32le', '-']
    x = np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, dtype=np.float32)
    return x.reshape(-1, channels) if channels > 1 else x.copy()


_WIN = (0.5 - 0.5 * np.cos(2 * np.pi * np.arange(N_FFT) / N_FFT)).astype(np.float32)   # periodic Hann


def stft_chunks(y, hop, chunk=2048):
    """Centred (zero-padded) STFT like librosa.stft, yielded as (first_frame, complex64 [frames, bins])."""
    yp = np.pad(y.astype(np.float32), N_FFT // 2)
    n = 1 + (len(yp) - N_FFT) // hop
    fr = np.lib.stride_tricks.as_strided(yp, (n, N_FFT), (yp.strides[0] * hop, yp.strides[0]), writeable=False)
    for a in range(0, n, chunk):
        yield a, sfft.rfft(fr[a:a + chunk] * _WIN, axis=1, workers=-1).astype(np.complex64)


def istft(D, hop, length):
    """Inverse of the centred STFT (frames x bins), overlap-add with window-square normalisation, like librosa."""
    T = D.shape[0]; k = N_FFT // hop
    fr = sfft.irfft(D, n=N_FFT, axis=1, workers=-1).astype(np.float32) * _WIN
    out = np.zeros((T + k - 1, hop), np.float32)
    ws = np.zeros((T + k - 1, hop), np.float32)
    w2 = (_WIN ** 2).reshape(k, hop)
    fr = fr.reshape(T, k, hop)
    for j in range(k):
        out[j:j + T] += fr[:, j]
        ws[j:j + T] += w2[j]
    out, ws = out.ravel(), ws.ravel()
    out[ws > 1e-8] /= ws[ws > 1e-8]
    out = out[N_FFT // 2:N_FFT // 2 + length]
    return np.pad(out, (0, max(0, length - len(out))))


def hpss_masks(S):
    """Soft (power-2 Wiener) masks from time / frequency median filters, like librosa.decompose.hpss."""
    from concurrent.futures import ThreadPoolExecutor            # median_filter releases the GIL: 2 cores
    med = lambda size: ndimage.median_filter(S, size=size, mode='reflect')
    with ThreadPoolExecutor(2) as ex:                             # S is [frames, bins]
        harm, perc = ex.map(med, [(HPSS_KERNEL, 1), (1, HPSS_KERNEL)])
    h2, p2 = harm.astype(np.float32) ** 2, perc.astype(np.float32) ** 2
    tot = h2 + p2
    mh = np.where(tot > 0, h2 / np.where(tot > 0, tot, 1), .5).astype(np.float32)
    return mh, (1 - mh).astype(np.float32)


def mel_filters(sr=SR, n_fft=N_FFT, n_mels=128):
    """Slaney mel filterbank (librosa default)."""
    def hz2mel(f):
        f = np.asanyarray(f, float); m = f / (200 / 3)
        return np.where(f >= 1000, 15 + np.log(np.maximum(f, 1e-9) / 1000) / (np.log(6.4) / 27), m)
    def mel2hz(m):
        m = np.asanyarray(m, float)
        return np.where(m >= 15, 1000 * np.exp((np.log(6.4) / 27) * (m - 15)), m * 200 / 3)
    fftf = np.linspace(0, sr / 2, 1 + n_fft // 2)
    melf = mel2hz(np.linspace(hz2mel(0), hz2mel(sr / 2), n_mels + 2))
    fd, ramps = np.diff(melf), melf[:, None] - fftf[None, :]
    W = np.maximum(0, np.minimum(-ramps[:-2] / fd[:-1, None], ramps[2:] / fd[1:, None]))
    return (W * (2 / (melf[2:] - melf[:-2]))[:, None]).astype(np.float32)


def chroma_filters(sr=SR, n_fft=N_FFT, fmin=65., fmax=5000.):
    f = np.arange(1 + n_fft // 2) * sr / n_fft
    W = np.zeros((12, len(f)), np.float32)
    ok = (f >= fmin) & (f <= fmax)
    s = 12 * np.log2(f[ok] / 440) + 69                         # MIDI pitch of each bin
    width = 12 * np.log2((f[ok] + sr / n_fft / 2) / (f[ok] - sr / n_fft / 2))
    sig = np.maximum(.4, width / 2)
    for c in range(12):
        d = (s - c + 6) % 12 - 6
        W[c, ok] = np.exp(-.5 * (d / sig) ** 2)
    W[:, ok] /= W[:, ok].sum(0)
    return W


def analyse_spectra(y, sr=SR):
    """-> dict: onset env (hop 128), per-frame band sums (hop 256), chroma (hop 512)."""
    fr256 = np.arange(1 + N_FFT // 2) * sr / N_FFT
    band = lambda lo, hi: (fr256 >= lo) & (fr256 < hi)
    bass_b = band(30, 150)
    # full mix at hop 256: bass band per frame; even frames = the hop-512 STFT used for HPSS
    bass, D = [], []
    for a, X in stft_chunks(y, HOP_BAND):
        M = np.abs(X)
        bass.append(M[:, bass_b].sum(1))
        D.append(X[(a % 2)::2])
    bass = np.concatenate(bass); D = np.concatenate(D)
    S = np.abs(D)
    mh, mp_ = hpss_masks(S)
    C = (S * mh) @ chroma_filters().T                           # harmonic chroma [frames, 12]
    mx = C.max(1, keepdims=True)
    C = np.where(mx > 1e-6, C / np.maximum(mx, 1e-12), 0)       # per-frame max-normalised (librosa norm=inf)
    yp = istft(D * mp_, 512, len(y))
    del D, S, mh, mp_
    # percussive part at hop 128: mel power for the onset envelope; even frames (hop 256) for band energies
    mel = mel_filters().T
    kb, sb, hb = band(30, 120), band(1500, 5000), band(6000, 11000)
    P, kick, snare, hat = [], [], [], []
    for a, X in stft_chunks(yp, HOP_ONSET):
        M2 = X.real ** 2 + X.imag ** 2
        P.append(M2 @ mel)
        M = np.sqrt(M2[(a % 2)::2])
        kick.append(M[:, kb].sum(1)); snare.append(M[:, sb].sum(1)); hat.append(M[:, hb].sum(1))
    P = np.concatenate(P)
    Sdb = 10 * np.log10(np.maximum(P, 1e-10))
    Sdb = np.maximum(Sdb, Sdb.max() - 80)
    flux = np.maximum(0, Sdb[1:] - Sdb[:-1]).mean(1)
    lag = 1 + N_FFT // (2 * HOP_ONSET)                          # librosa onset_strength(center=True) alignment
    env = np.concatenate([np.zeros(lag), flux])[:len(Sdb)].astype(np.float64)
    return dict(env=env, kick=np.concatenate(kick), snare=np.concatenate(snare), hat=np.concatenate(hat),
                bass=bass, chroma=C)


# ---------------------------------------------------------------- tempo
def _autocorr(e):
    e = e - e.mean(); n = len(e)
    f = np.fft.rfft(e, 2 * n)
    return np.fft.irfft(np.abs(f) ** 2)[:n]


def _ac_score(ac, fps, bpm):
    lag = fps * 60 / np.asarray(bpm); l = lag.astype(int); f = lag - l
    ok = l + 1 < len(ac)
    out = np.full(np.shape(lag), -np.inf)
    out[ok] = ac[l[ok]] * (1 - f[ok]) + ac[l[ok] + 1] * f[ok]
    return out


def _comb_mean(e, fps, P, phase, t_end):
    idx = np.round(np.arange(phase, t_end, P) * fps).astype(int)
    idx = idx[idx < len(e)]
    return e[idx].mean() if len(idx) else 0.


def _best_phase(e, fps, P, t_end):
    ph = np.arange(0, P, .002)
    return max(ph, key=lambda p: _comb_mean(e, fps, P, p, t_end))


OCTAVE_RATIO = .5   # in-between / on-beat pulse ratio above which the faster of two octave candidates is the beat


def estimate_tempo(env, fps, bpm_min=70., bpm_max=180., hint=None, log=None):
    """Seed BPM from the autocorrelation of the mean-removed envelope (as beats_refine.py). Octave: with --bpm-hint,
    the autocorrelation peak within x/÷1.25 of the hint; otherwise, when both S and 2S are in range, 2S is taken
    if the pulses halfway between S's beats are at least OCTAVE_RATIO as strong as S's own (backbeat snares),
    else S (in-between pulses are only weak hats)."""
    ac = _autocorr(env)

    def peak(lo, hi):
        g = np.arange(lo, hi, .02)
        return float(g[np.argmax(_ac_score(ac, fps, g))])
    if hint:
        bpm = peak(hint / 1.25, hint * 1.25)
        how = f'hint {hint:g}'
    else:
        best = peak(bpm_min, bpm_max + .01)
        fam = sorted(peak(best * m * .985, best * m * 1.015) for m in (.25, .5, 1, 2, 4) if bpm_min <= best * m <= bpm_max)
        bpm, how = fam[0], 'autocorrelation'
        t_end = len(env) / fps
        e = np.maximum(env - ndimage.uniform_filter1d(env, int(fps)), 0)
        for slow, fast in zip(fam[:-1], fam[1:]):          # go up an octave while the in-between pulses are strong
            Ps = 60 / slow
            ph = _best_phase(e, fps, Ps, t_end)
            on, mid = _comb_mean(e, fps, Ps, ph, t_end), _comb_mean(e, fps, Ps, (ph + Ps / 2) % Ps, t_end)
            r = mid / (on + 1e-12)
            how = (f'octave {slow:.1f} vs {fast:.1f}: in-between/on-beat pulse {r:.2f} -> '
                   f'{"fast" if r >= OCTAVE_RATIO else "slow"}; --bpm-hint forces')
            if r < OCTAVE_RATIO:
                break
            bpm = fast
    if log: log(f'seed tempo {bpm:.2f} BPM ({how})')
    return bpm, how


# ---------------------------------------------------------------- tracking
class Picker:
    def __init__(self, env, fps, t_off, n_beats_guess):
        self.env, self.fps, self.t_off = env, fps, t_off
        self.lvl = ndimage.median_filter(env, size=int(2 * fps) | 1, mode='nearest')
        e = env
        pk = np.where((e[1:-1] >= e[:-2]) & (e[1:-1] > e[2:]))[0] + 1
        h = np.sort(e[pk] - self.lvl[pk])[::-1]
        self.h_typ = float(np.median(h[:max(8, n_beats_guess)])) if len(h) else 1.
        self.h_min = PEAK_MIN * self.h_typ

    def t2i(self, t):
        return (t - self.t_off) * self.fps

    def pick(self, pred, win):
        """Highest local max of the envelope within +-win of pred -> (time, strength, height) or None."""
        e = self.env
        a = max(1, int(np.ceil(self.t2i(pred - win)))); b = min(len(e) - 2, int(np.floor(self.t2i(pred + win))))
        if b < a:
            return None
        seg = e[a:b + 1]
        loc = np.where((seg >= e[a - 1:b]) & (seg > e[a + 1:b + 2]))[0]
        if not len(loc):
            return None
        i = a + loc[np.argmax(seg[loc])]
        h = e[i] - self.lvl[i]
        if h < self.h_min:
            return None
        den = e[i - 1] - 2 * e[i] + e[i + 1]
        d = np.clip(.5 * (e[i - 1] - e[i + 1]) / den, -.5, .5) if den < 0 else 0.
        return self.t_off + (i + d) / self.fps, float(e[i]), float(h)


def _wfit(j, t, w):
    """weighted (sqrt-weighted rows) least-squares line t = s*j + c."""
    A = np.vstack([j, np.ones_like(j)]).T * np.sqrt(w)[:, None]
    (s, c), *_ = np.linalg.lstsq(A, t * np.sqrt(w), rcond=None)
    return s, c


RELOCK_AFTER = 4   # consecutive misses before trying to re-lock (drift / tempo change during a break)
RELOCK_FAR = 8     # misses before a re-lock may also shift the phase by more than 0.15 beat
TEMPO_RANGE = .12  # tracked tempo stays within +-12 % of the seed tempo


def relock(pk, pred, P, direction, far_ok):
    """After a gap: 8-beat combs that land on clear onsets. A small correction (phase <= 0.15 beat, tempo +-4 %)
    is taken when 6 of 8 comb teeth hit; a larger one (a phase jump in an edit, a tempo change at a section or
    song change: phase +-0.5 beat, tempo +-12 %) only after RELOCK_FAR misses and with 7 of 8 hits, so syncopated
    hits in a sparse passage do not move the beat onto the off-beat. Returns (new prediction, new period) or None."""
    e = ndimage.maximum_filter1d(np.maximum(pk.env - pk.lvl, 0), 3)
    for need, dmax, smax, n_s in ((6, .15, .04, 17), (7, .5, .12, 49)):
        if need == 7 and not far_ok:
            break
        d = np.arange(-dmax * P, dmax * P, .002)
        s = 1 + np.linspace(-smax, smax, n_s)
        t = pred + d[None, :, None] + direction * (P * s)[:, None, None] * np.arange(8)[None, None, :]
        idx = np.round(pk.t2i(t)).astype(int)
        if idx.min() < 0 or idx.max() >= len(e) - 1:
            return None
        v = e[idx]                                                # [tempo, phase, beat]
        c = np.where((v > pk.h_min * 2).sum(2) >= need, v.sum(2), -1)
        a, b = np.unravel_index(np.argmax(c), c.shape)
        if c[a, b] > 0 and v[a, b].mean() >= .3 * pk.h_typ:
            return pred + d[b], P * s[a]
    return None


def track(pk, t_first, P, direction, t_lo, t_hi, hist=None):
    """Follow the beat from t_first in one direction. Each beat: predict from a weighted line through the last
    FIT_LEN beats, snap to the envelope peak within +-35 ms. After RELOCK_AFTER misses in a row, re-lock on the
    returning drums. Returns list of [t, strength, height, accepted] in tracking order (hist entries first)."""
    H = [list(h) for h in (hist or [])]
    pred, P_cur, misses, h0 = t_first, P, 0, 0
    P_lo, P_hi = P / (1 + TEMPO_RANGE), P * (1 + TEMPO_RANGE)
    while t_lo <= pred <= t_hi:
        if misses >= RELOCK_AFTER:
            rl = relock(pk, pred, P_cur, direction, misses >= RELOCK_FAR)
            if rl:                                    # new phase: the fit restarts here (gap is bridged later)
                pred, P_cur = rl[0], float(np.clip(rl[1], P_lo, P_hi))
                h0 = len(H)
        r = pk.pick(pred, min(PICK_WIN, .2 * P_cur))
        if r:
            H.append([r[0], r[1], r[2], True]); misses = 0
        else:
            H.append([pred, 0., 0., False]); misses += 1
        a = max(h0, len(H) - FIT_LEN)
        last = H[a:]
        j = np.arange(a, len(H), dtype=float)
        t = np.array([h[0] for h in last]); w = np.array([h[1] if h[3] else 0. for h in last]) + 1e-3
        if sum(h[3] for h in last) >= 5:
            s_fit, _ = _wfit(j, t, w)
            if P_lo <= direction * s_fit <= P_hi:
                P_cur = abs(s_fit)
        s = direction * P_cur
        c = np.sum(w * (t - s * j)) / w.sum()
        pred = s * len(H) + c
    return H


def seed(pk, env, fps, P0, t_end):
    """Local tempo + phase on the strongest 16-beat passage (comb, 2 ms phase steps, +-3 % tempo)."""
    es = ndimage.maximum_filter1d(env, 3)
    W = 16
    Ps = P0 * (1 + np.linspace(-.03, .03, 31))
    best = (-1, 0., P0)
    k = np.arange(W)
    for t0 in np.arange(0, max(t_end - W * P0, 0) + 1e-9, 4 * P0):
        ph = np.arange(0, P0, .002)
        idx = np.round((t0 + ph[None, :, None] + Ps[:, None, None] * k[None, None, :]) * fps).astype(int)
        idx = np.clip(idx, 0, len(es) - 1)
        sc = es[idx].sum(2)
        a, b = np.unravel_index(np.argmax(sc), sc.shape)
        if sc[a, b] > best[0]:
            best = (sc[a, b], t0 + ph[b], Ps[a])
    return best[1], best[2]


def track_all(env, fps, P0, t_end, log=None):
    pk = Picker(env, fps, 0., int(t_end / P0))
    t_s, P_s = seed(pk, env, fps, P0, t_end)
    fwd = track(pk, t_s, P_s, +1, 0, t_end - .05)
    n_h = min(FIT_LEN, len(fwd))
    bwd = track(pk, fwd[0][0] - P_s, P_s, -1, 0, t_end, hist=fwd[:n_h][::-1])
    H = bwd[n_h:][::-1] + fwd
    t = np.array([h[0] for h in H]); s = np.array([h[1] for h in H])
    hgt = np.array([h[2] for h in H]); acc = np.array([h[3] for h in H])
    # bridge runs of misses between two found beats evenly (forward / backward predictions may disagree there)
    ia = np.where(acc)[0]
    for a, b in zip(ia[:-1], ia[1:]):
        if b - a > 1:
            t[a + 1:b] = t[a] + (t[b] - t[a]) * np.arange(1, b - a) / (b - a)
    # sliding 9-beat linear fit weighted by onset strength, evaluated at the centre beat
    w = np.where(acc, s, 0.) + 1e-3
    n, half = len(t), FIT_LEN // 2
    fit = np.empty(n)
    for k in range(n):
        a, b = max(0, k - half), min(n, k + half + 1)
        sl, c = _wfit(np.arange(a, b, dtype=float), t[a:b], w[a:b])
        fit[k] = sl * k + c
    # beats without an onset (drum breaks, intro/outro): the weighted fit there would extrapolate the few found
    # beats at one side of the window and amplify their jitter, so interpolate the smoothed beats across the gap
    # (constant tempo inside it) and extrapolate the edges with the edge tempo.
    ia = np.where(acc)[0]
    if len(ia) >= 2:
        for a, b in zip(ia[:-1], ia[1:]):
            if b - a > 1:
                fit[a + 1:b] = fit[a] + (fit[b] - fit[a]) * np.arange(1, b - a) / (b - a)
        for edge, side in ((ia[0], -1), (ia[-1], +1)):
            nb = ia[ia <= edge + 8] if side < 0 else ia[ia >= edge - 8]
            P_e = (fit[nb[-1]] - fit[nb[0]]) / (nb[-1] - nb[0]) if nb[-1] > nb[0] else P0
            ks = np.arange(0, edge) if side < 0 else np.arange(edge + 1, n)
            fit[ks] = fit[edge] + (ks - edge) * P_e
    conf = np.where(acc, np.minimum(1, hgt / pk.h_typ), 0.)
    if log: log(f'seed at {t_s:.3f} s, local tempo {60 / P_s:.2f} BPM; {acc.sum()}/{n} beats found an onset '
                f'within +-{PICK_WIN * 1000:.0f} ms')
    return fit, conf


# ---------------------------------------------------------------- downbeats / features
def per_beat_max(frames, fps, beats, lo=-.02, hi=.10):
    out = np.zeros(len(beats))
    for k, t in enumerate(beats):
        a, b = max(0, int(np.ceil((t + lo) * fps))), min(len(frames), int(np.ceil((t + hi) * fps)))
        out[k] = frames[a:b].max() if b > a else 0.
    return out


def novelty(chroma, cfps, beats):
    n, B = len(beats), np.median(np.diff(beats)) if len(beats) > 1 else .5
    def cvec(a, b):
        i0, i1 = max(0, int(np.ceil(a * cfps))), min(len(chroma), int(np.ceil(b * cfps)))
        if i1 - i0 < 2:
            return None
        v = chroma[i0:i1].mean(0)
        return v / (np.linalg.norm(v) + 1e-9)
    nov = np.full(n, np.nan)
    for k in range(n):
        a = beats[k - 2] if k >= 2 else beats[k] - 2 * B
        b = beats[k + 2] if k + 2 < n else beats[k] + 2 * B
        if a < 0 or b * cfps > len(chroma):
            continue
        l, r = cvec(a, beats[k]), cvec(beats[k], b)
        if l is not None and r is not None:
            nov[k] = 1 - float(np.dot(l, r))
    return nov


def downbeat_phase(nov, kick, meter):
    z = lambda v: (v - np.nanmean(v)) / (np.nanstd(v) + 1e-9)
    nz, kz = z(nov), z(kick)
    sc = []
    for p in range(meter):
        a, b = nz[p::meter], kz[p::meter]
        sc.append((np.nanmean(a) if np.isfinite(a).any() else 0.) + .5 * (np.nanmean(b) if len(b) else 0.))
    sc = np.array(sc); order = np.argsort(sc)[::-1]
    conf = float((sc[order[0]] - sc[order[1]]) / (sc[order[0]] - sc[order[-1]] + 1e-9)) if meter > 1 else 1.
    return int(order[0]), conf, sc


def write_click(path, src, a, b, beats_file, is_down, sr=44100):
    """Audio of [a, b] (file time) with a 1.5 kHz click on each beat and a louder 3 kHz one where is_down."""
    x = load_audio(src, a, b - a, sr=sr, channels=2).astype(np.float64)
    out = x * .7
    def burst(f, dur, amp):
        tt = np.arange(int(dur * sr)) / sr
        return amp * np.sin(2 * np.pi * f * tt) * np.exp(-tt / (dur / 4))
    c_beat, c_down = burst(1500, .03, .45), burst(3000, .045, .8)
    for t, dn in zip(beats_file, is_down):
        c = c_down if dn else c_beat
        i = int(round((t - a) * sr))
        if 0 <= i < len(out):
            m = min(len(c), len(out) - i)
            out[i:i + m] += c[:m, None]
    pk = np.abs(out).max()
    if pk > .98:
        out *= .98 / pk
    from scipy.io import wavfile
    wavfile.write(path, sr, (out * 32767).astype(np.int16))


# ---------------------------------------------------------------- main analysis
def analyse(src, t_from=0., t_to=None, meter=4, bpm_min=70., bpm_max=180., bpm_hint=None, relative=False, log=None,
            onset_delay=ONSET_DELAY):
    """Full analysis -> result dict (the JSON). Times in file time unless relative."""
    a = max(0., t_from - MARGIN)
    y = load_audio(src, a, (t_to + MARGIN - a) if t_to else None)
    if not len(y):
        raise SystemExit(f'no audio decoded from {src} at {a:.3f} s')
    end = a + len(y) / SR
    t_to = min(t_to, end) if t_to else end
    F = analyse_spectra(y)
    env, fps = F['env'], SR / HOP_ONSET
    bpm_seed, how = estimate_tempo(env, fps, bpm_min, bpm_max, bpm_hint, log)
    # onset times (decoded-audio clock): frame m at m*hop/sr, minus the envelope's delay
    fit, conf = track_all(env, fps, 60 / bpm_seed, len(y) / SR, log)
    fit = fit - onset_delay
    # (all times below in the decoded-audio clock until `off` is added)
    sel = (fit + a >= t_from - 1e-6) & (fit + a <= t_to + 1e-6)
    off = a - (t_from if relative else 0.)
    i0, i1 = int(round((t_from - a) * SR)), int(round((t_to - a) * SR))
    nz = np.nonzero(np.abs(y[i0:i1]) > 1e-4)[0]
    s0 = (i0 + (nz[0] if len(nz) else 0)) / SR + off
    if len(nz):   # extrapolated (no-onset) beats in digital silence before the first / after the last sound: drop
        P_m = 60 / bpm_seed
        q0, q1 = (i0 + nz[0]) / SR - P_m / 2, (i0 + nz[-1]) / SR + P_m / 2
        sel &= (conf > 0) | ((fit >= q0) & (fit <= q1))
    bt, cf = fit[sel], conf[sel]
    if len(bt) < 2:
        raise SystemExit('fewer than 2 beats in the range')
    bfps = SR / HOP_BAND
    # band windows -20..+100 ms around the envelope peak, exactly as beats_refine.py
    kick, snare, hat, bass = (per_beat_max(F[k], bfps, bt + onset_delay) for k in ('kick', 'snare', 'hat', 'bass'))
    nov = novelty(F['chroma'], SR / 512, fit)[sel]
    ph, ph_conf, ph_sc = downbeat_phase(nov, kick, meter)
    beats = bt + off
    d = np.diff(beats)
    bpm = float(60 / np.median(d)) if len(d) else bpm_seed
    if len(beats) > 2:
        k = np.arange(len(beats)); s, c = np.polyfit(k, beats, 1)
        drift = float(np.abs(beats - (s * k + c)).max() * 1000)
    else:
        drift = 0.
    r4 = lambda v: [round(float(x), 4) for x in v]
    res = dict(src=src, file=src, time_base='from' if relative else 'file', **{'from': round(t_from, 4)},
               to=round(t_to, 4), s0=round(float(s0), 4), bpm=round(bpm, 3), bpm_half=round(bpm / 2, 3),
               bpm_seed=round(bpm_seed, 3), beat=round(60 / bpm, 6), meter=meter, beats=r4(beats),
               conf=[round(float(x), 3) for x in cf], downbeats=r4(beats[ph::meter]), downbeat_phase=ph,
               downbeat_conf=round(ph_conf, 3), downbeat_scores=[round(float(x), 3) for x in ph_sc],
               drift_ms_max=round(drift, 1), low_conf_beats=int(np.sum(cf == 0)),
               kick=kick.round(1).tolist(), snare=snare.round(1).tolist(), bass=bass.round(1).tolist(),
               hat=hat.round(1).tolist(), nov=[round(float(x), 3) if np.isfinite(x) else 0. for x in nov],
               tempo_method=how)
    return res


def print_table(r, out=sys.stdout):
    ph, m = r['downbeat_phase'], r['meter']
    med = {k: (np.median(r[k]) or 1.) for k in ('kick', 'snare', 'bass', 'hat')}
    for k, t in enumerate(r['beats']):
        bar, bi = (k - ph) // m + 1, (k - ph) % m + 1
        print(f"k{k:3d} bar{bar:3d}.{bi} t={t:8.3f} kick {r['kick'][k] / med['kick']:4.2f} "
              f"snare {r['snare'][k] / med['snare']:4.2f} bass {r['bass'][k] / med['bass']:4.2f} "
              f"hat {r['hat'][k] / med['hat']:4.2f} nov {r['nov'][k]:.3f} conf {r['conf'][k]:.2f}"
              + ('  ? no onset' if r['conf'][k] == 0 else ''), file=out)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0], formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('song'); ap.add_argument('out_pos', nargs='?', help=argparse.SUPPRESS)
    ap.add_argument('--out', help='beats JSON to write')
    ap.add_argument('--from', dest='t_from', type=float, default=0.); ap.add_argument('--to', dest='t_to', type=float)
    ap.add_argument('--relative', action='store_true', help='times relative to --from (default: file time)')
    ap.add_argument('--meter', type=int, default=4)
    ap.add_argument('--bpm-min', type=float, default=70.); ap.add_argument('--bpm-max', type=float, default=180.)
    ap.add_argument('--bpm-hint', type=float)
    ap.add_argument('--click', help='write audio + clicks (downbeats higher/louder) for listening')
    ap.add_argument('--onset-delay', type=float, default=ONSET_DELAY,
                    help='seconds subtracted so beats sit on the attack (0 = beats_refine.py timing)')
    ap.add_argument('-q', '--quiet', action='store_true', help='no per-beat table')
    A = ap.parse_args()
    out = A.out or A.out_pos
    t_start = time.time()
    log = lambda s: print(s, file=sys.stderr)
    r = analyse(A.song, A.t_from, A.t_to, A.meter, A.bpm_min, A.bpm_max, A.bpm_hint, A.relative, log, A.onset_delay)
    if out:
        with open(out, 'w') as f:
            json.dump(r, f, indent=1)
    if not A.quiet:
        print_table(r)
    if A.click:
        off = 0. if r['time_base'] == 'file' else r['from']
        k = np.arange(len(r['beats']))
        write_click(A.click, A.song, r['from'], r['to'], np.array(r['beats']) + off,
                    k % r['meter'] == r['downbeat_phase'])
    c = np.array(r['conf'])
    print(f"bpm {r['bpm']:.2f} (half {r['bpm_half']:.2f}, seed {r['bpm_seed']:.2f})  beats {len(r['beats'])}"
          f" ({r['beats'][0]:.3f} .. {r['beats'][-1]:.3f} s, {r['time_base']} time)  drift max {r['drift_ms_max']:.1f} ms"
          f"  low-conf {r['low_conf_beats']}  mean conf {c.mean():.2f}")
    print(f"downbeat phase {r['downbeat_phase']} of {r['meter']} (conf {r['downbeat_conf']:.2f}; scores "
          f"{' '.join(f'{s:+.2f}' for s in r['downbeat_scores'])})  first downbeat {r['downbeats'][0]:.3f} s"
          + (f"  -> {out}" if out else '') + (f"  click -> {A.click} (starts at file time {r['from']:.3f})" if A.click else '')
          + f"  [{time.time() - t_start:.1f} s]")


if __name__ == '__main__':
    main()
