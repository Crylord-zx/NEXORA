"""Nexora promo score, synthesised from scratch (no samples): an FM electric piano on 9th chords,
a half-time groove, sub bass and bells, cut to the same bar lines as showreel.html
(120 BPM, bars at 0.5 s + 2 s * n). Writes soundtrack.wav (48 kHz, stereo, 20 s).
Run: python3 soundtrack.py"""
import wave
import numpy as np

SR = 48000
DUR = 20.0
N = int(SR * DUR)
T = np.arange(N) / SR
rng = np.random.default_rng(11)
BAR = lambda n: 0.5 + 2.0 * n          # bar n starts here
BUS = {k: np.zeros((N, 2)) for k in ('keys', 'bells', 'bass', 'drums', 'fx')}


def add(bus, sig, at, gain=1.0, pan=0.0):
    i = int(round(at * SR))
    if i >= N or len(sig) == 0:
        return
    if sig.ndim == 1:
        l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
        sig = np.stack([sig * l, sig * r], 1) * 1.4142
    if i < 0:
        sig, i = sig[-i:], 0
    sig = sig[: N - i]
    BUS[bus][i:i + len(sig)] += sig * gain


def fft_filter(x, lo=None, hi=None, order=4):
    X = np.fft.rfft(x, axis=0)
    f = np.fft.rfftfreq(x.shape[0], 1 / SR)
    g = np.ones_like(f)
    if hi:
        g *= 1 / np.sqrt(1 + (f / hi) ** order)
    if lo:
        g *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-3)) ** order)
    if x.ndim == 2:
        g = g[:, None]
    return np.fft.irfft(X * g, x.shape[0], axis=0)


def hz(name):
    names = {'C': -9, 'D': -7, 'E': -5, 'F': -4, 'G': -2, 'A': 0, 'B': 2}
    n, octv = name[:-1], int(name[-1])
    return 440 * 2 ** ((names[n[0]] + n.count('#') - n.count('b') + (octv - 4) * 12) / 12)


# ---------- instruments ----------
def epiano(f, dur, vel=.8):
    """DX-style electric piano: 1:1 FM body with a decaying index, plus a short metallic tine."""
    n = int(SR * (dur + 1.2))
    x = np.arange(n) / SR
    idx = vel * (1.6 * np.exp(-x / .3) + .22)
    body = np.sin(2 * np.pi * f * x + idx * np.sin(2 * np.pi * f * x))
    tine = .2 * vel * np.sin(2 * np.pi * f * 14 * x + 1.2 * np.sin(2 * np.pi * f * x)) * np.exp(-x / .018)
    decay = 1.9 * (220 / f) ** .35
    env = np.minimum(1, x / .004) * np.exp(-x / decay)
    rel = np.clip((dur + .25 - x) / .25, 0, 1)        # key release
    s = (body + tine) * env * rel * vel
    # suitcase tremolo panning
    trem = .5 + .16 * np.sin(2 * np.pi * 4.6 * x)
    return np.stack([s * trem, s * (1 - trem)], 1) * 1.6


def bell(f, vel=.6):
    n = int(SR * 2.2)
    x = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * x + 1.3 * np.exp(-x / .22) * np.sin(2 * np.pi * f * 3.5 * x))
    s += .25 * np.sin(2 * np.pi * f * 2 * x) * np.exp(-x / .3)
    return s * np.minimum(1, x / .002) * np.exp(-x / .75) * vel


def sub(f, dur, vel=1.0):
    n = int(SR * (dur + .1))
    x = np.arange(n) / SR
    s = np.sin(2 * np.pi * f * x) + .18 * np.sin(4 * np.pi * f * x)
    env = np.minimum(1, x / .008) * np.clip((dur - x) / .08 + 1, 0, 1) * (.7 + .3 * np.exp(-x / .2))
    return np.tanh(1.4 * s * env) * vel


def kick(vel=1.0):
    n = int(SR * .6)
    x = np.arange(n) / SR
    f = 44 + 70 * np.exp(-x * 30)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / .26)
    click = fft_filter(rng.standard_normal(n), lo=1500, hi=5000) * np.exp(-x * 400) * .25
    return np.tanh((s + click) * 1.3) * vel


def snap(vel=1.0):
    n = int(SR * .4)
    x = np.arange(n) / SR
    nz = fft_filter(rng.standard_normal(n), lo=1200, hi=7000)
    e = np.zeros(n)
    for off, d in ((0, .006), (.007, .006), (.014, .09)):
        i = int(off * SR)
        e[i:] += np.exp(-x[: n - i] / d)
    body = np.sin(2 * np.pi * 190 * x) * np.exp(-x / .04) * .5
    return (nz * e * .55 + body) * vel


def hat(vel=1.0):
    n = int(SR * .09)
    x = np.arange(n) / SR
    return fft_filter(rng.standard_normal(n), lo=7500, hi=15000) * np.exp(-x / .022) * vel


def swell(dur, vel=1.0, lo=300, hi=6000):
    """Soft rising air, for the run into a bar."""
    n = int(SR * dur)
    x = np.arange(n) / SR
    nz = fft_filter(rng.standard_normal(n), lo=lo, hi=hi)
    return nz * (x / dur) ** 3 * vel


def click(vel=1.0):
    n = int(SR * .03)
    x = np.arange(n) / SR
    return (np.sin(2 * np.pi * 2600 * x) * .6 + fft_filter(rng.standard_normal(n), lo=3000) * .4) * np.exp(-x / .004) * vel


def boom(vel=1.0):
    n = int(SR * 2.5)
    x = np.arange(n) / SR
    f = 32 + 40 * np.exp(-x * 6)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / 1.0) * np.minimum(1, x / .005) * vel


# ---------- harmony ----------
CH = {
    'Fmaj9': ('F2', ['A3', 'C4', 'E4', 'G4']),
    'G69':   ('G2', ['B3', 'D4', 'E4', 'A4']),
    'Am9':   ('A2', ['C4', 'E4', 'G4', 'B4']),
    'Em11':  ('E2', ['G3', 'B3', 'D4', 'A4']),
    'Dm9':   ('D2', ['F3', 'A3', 'C4', 'E4']),
    'Aadd9': ('A1', ['E3', 'A3', 'B3', 'C4', 'E4']),
}

def chord(name, at, dur, vel=.7, strum=.012):
    root, tones = CH[name]
    for k, nme in enumerate(tones):
        add('keys', epiano(hz(nme), dur, vel * (1 - .06 * k)), at + k * strum, .32)

# ---------- arrangement ----------
# pickup: reversed chord swelling into bar 1
rev = epiano(hz('E4'), 1.0, .7)[::-1][-int(SR * .5):] + epiano(hz('A3'), 1.0, .6)[::-1][-int(SR * .5):]
add('keys', rev * np.linspace(0, 1, len(rev))[:, None] ** 2, 0.0, .35)

# bar 1 (library) and bar 2 (Hindi)
chord('Fmaj9', BAR(0), 1.9, .5)
add('bass', sub(hz('F1'), 1.9, .3), BAR(0))
chord('G69', BAR(1), 1.9, .55)
add('bass', sub(hz('G1'), 1.9, .38), BAR(1))
for b in range(8):                          # a quiet pulse joins in bar 2
    at = BAR(1) + b * .25
    add('drums', hat(.16 if b % 2 else .09), at + (.02 if b % 2 else 0), pan=.3)
add('drums', kick(.45), BAR(1)); add('drums', kick(.35), BAR(1) + 1.0)
add('fx', click(.25), 3.35, pan=-.2)
add('fx', swell(1.0, .22), BAR(2) - 1.0)

# bar 3 (brand): the hit
add('fx', boom(.9), BAR(2))
add('drums', kick(.9), BAR(2))
chord('Am9', BAR(2), 1.9, .9, strum=.02)
add('bass', sub(hz('A1'), 1.9, .75), BAR(2))
for at, nme in ((BAR(2) + .3, 'E5'), (BAR(2) + .55, 'B5'), (BAR(2) + .8, 'C6'), (BAR(2) + 1.3, 'E6')):
    add('bells', bell(hz(nme), .5), at, pan=.25)
add('fx', swell(.5, .18), BAR(3) - .5)

# bars 4-7: the groove (half-time: kick on 1 and the "and" of 2, snap on 3)
prog = ['Fmaj9', 'G69', 'Am9', 'Em11']
melody = {0: [(0, 'E5'), (.5, 'G5'), (1.25, 'A5')], 1: [(0, 'B5'), (.75, 'A5'), (1.5, 'E5')],
          2: [(0, 'C6'), (.75, 'B5'), (1.25, 'G5')], 3: [(0, 'B5'), (.75, 'G5'), (1.25, 'A5')]}
for k, name in enumerate(prog):
    b0 = BAR(3 + k)
    chord(name, b0, .9, .7)                         # stab, then a re-strike on the "and" of 2
    chord(name, b0 + .75, 1.15, .5, strum=.008)
    root = CH[name][0]
    lo = hz(root) / 2
    for at, d, v in ((0, .7, .8), (.75, .2, .6), (1.0, .45, .7), (1.5, .45, .7)):
        add('bass', sub(lo, d, v), b0 + at)
    add('drums', kick(.85), b0); add('drums', kick(.6), b0 + .75); add('drums', kick(.45), b0 + 1.75)
    add('drums', snap(.5), b0 + 1.0, pan=.05)
    for h in range(8):
        add('drums', hat(.2 if h % 2 else .11), b0 + h * .25 + (.025 if h % 2 else 0), pan=(.35 if h % 2 else -.2))
    for at, nme in melody[k]:
        add('bells', bell(hz(nme), .38), b0 + at, pan=-.3 + .2 * (at > .5))
for ti in (8.48, 8.98, 9.48, 9.98, 11.05):
    add('fx', click(.3), ti, pan=.15)
add('fx', swell(.7, .12, 500, 9000), 11.25)

# bar 8 (words): stops, one chord per word
for at, name in ((14.5, 'Dm9'), (15.0, 'Fmaj9'), (15.5, 'G69')):
    chord(name, at, .45, .8, strum=.006)
    add('bass', sub(hz(CH[name][0]) / 2, .42, .85), at)
    add('drums', kick(.8), at)
add('bells', bell(hz('E6'), .4), 16.0, pan=.2)
add('fx', swell(.5, .25), BAR(8) - .5)

# bar 9 to the end: resolve
add('fx', boom(.8), BAR(8))
add('drums', kick(.85), BAR(8))
chord('Aadd9', BAR(8), 3.0, .85, strum=.025)
add('bass', sub(hz('A1'), 3.0, .7), BAR(8))
for at, nme in ((BAR(8) + .5, 'A5'), (BAR(8) + 1.0, 'G5'), (BAR(8) + 1.5, 'E5'), (BAR(8) + 2.25, 'B4')):
    add('bells', bell(hz(nme), .42), at, pan=.2)

# ---------- mix ----------
# sidechain keys and bass to the kick pattern
duck = np.ones(N)
kicks = [BAR(1), BAR(1) + 1] + [BAR(3 + k) + o for k in range(4) for o in (0, .75, 1.75)]
for at in kicks:
    i = int(at * SR); m = min(N - i, int(SR * .35))
    duck[i:i + m] = np.minimum(duck[i:i + m], 1 - .45 * np.exp(-np.arange(m) / SR / .1))
BUS['keys'] *= duck[:, None]
BUS['bass'] *= (1 - (1 - duck) * .6)[:, None]


def reverb(x, secs=2.6, pre=.025, seed=1):
    r = np.random.default_rng(seed)
    m = int(SR * secs)
    tt = np.arange(m) / SR
    ir = r.standard_normal((m, 2)) * np.exp(-tt / (secs / 6.5))[:, None]
    ir = fft_filter(ir, lo=250, hi=5500)
    ir = np.concatenate([np.zeros((int(pre * SR), 2)), ir])
    ir /= np.sqrt(np.sum(ir ** 2, 0))
    size = 1 << int(np.ceil(np.log2(x.shape[0] + ir.shape[0])))
    return np.fft.irfft(np.fft.rfft(x, size, axis=0) * np.fft.rfft(ir, size, axis=0), size, axis=0)[: x.shape[0]]


keys = fft_filter(BUS['keys'], lo=90, hi=9000)
bells = BUS['bells']
drums = BUS['drums']
send = keys * .5 + bells * .9 + drums * .12 + BUS['fx'] * .3
wet = reverb(send)
mix = keys * .9 + bells * .5 + BUS['bass'] * .8 + drums * .9 + BUS['fx'] * .6 + wet * .55
mix = fft_filter(mix, lo=28)

# gentle bus compression (smoothed RMS), then a soft clip
rms = np.sqrt(np.convolve(np.mean(mix ** 2, 1), np.ones(2400) / 2400, mode='same')) + 1e-6
target = .3
gain = np.where(rms > target, (target / rms) ** .3, 1.0)
gain = np.convolve(gain, np.ones(1200) / 1200, mode='same')
mix *= gain[:, None]
mix *= np.clip((DUR - T) / .45, 0, 1)[:, None] * np.clip(T / .02, 0, 1)[:, None]
mix /= np.max(np.abs(mix)) + 1e-9
mix = np.tanh(mix * 1.4) / np.tanh(1.4)
mix *= 10 ** (-1 / 20) / np.max(np.abs(mix))
pcm = (mix * 32767).astype('<i2')
with wave.open('soundtrack.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('wrote soundtrack.wav', pcm.shape)
