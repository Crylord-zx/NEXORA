"""Nexora trailer score, synthesised from scratch (no samples): clock ticks, braams, impacts, a driving
16th-note ostinato, taiko, risers and the splash sting, all hit-synced to showreel.html.
Writes soundtrack.wav (48 kHz, stereo, 20 s). Run: python3 soundtrack.py"""
import wave
import numpy as np

SR = 48000
DUR = 20.0
N = int(SR * DUR)
T = np.arange(N) / SR
rng = np.random.default_rng(23)
BUS = {k: np.zeros((N, 2)) for k in ('music', 'drums', 'hits', 'fx')}


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


def filt(x, lo=None, hi=None, order=4):
    X = np.fft.rfft(x, axis=0)
    f = np.fft.rfftfreq(x.shape[0], 1 / SR)
    g = np.ones_like(f)
    if hi:
        g *= 1 / np.sqrt(1 + (f / hi) ** order)
    if lo:
        g *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-3)) ** order)
    return np.fft.irfft(X * (g[:, None] if x.ndim == 2 else g), x.shape[0], axis=0)


def onepole(x, cut):
    cut = np.broadcast_to(np.asarray(cut, float), x.shape)
    a = 1 - np.exp(-2 * np.pi * cut / SR)
    y = np.empty_like(x); s = 0.0
    for k in range(len(x)):
        s += a[k] * (x[k] - s); y[k] = s
    return y


def hz(name):
    names = {'C': -9, 'D': -7, 'E': -5, 'F': -4, 'G': -2, 'A': 0, 'B': 2}
    n, o = name[:-1], int(name[-1])
    return 440 * 2 ** ((names[n[0]] + n.count('#') - n.count('b') + (o - 4) * 12) / 12)


def saw(f, n, ph=0.0):
    p = (np.cumsum(np.broadcast_to(np.asarray(f, float), (n,))) / SR + ph) % 1
    return 2 * p - 1


# ---------- sound design ----------
def braam(dur=1.6, vel=1.0, notes=('A1', 'E2', 'A2', 'C3')):
    """Trailer brass: stacked detuned saws, filter swelling open, saturated."""
    n = int(SR * (dur + .6))
    x = np.arange(n) / SR
    s = np.zeros(n)
    for nm in notes:
        for d in (-.18, -.07, .07, .18):
            s += saw(hz(nm) * 2 ** (d / 12), n, rng.random())
    cut = 180 + 2600 * np.exp(-((x - .12) / .5) ** 2) * (x > .02) + 300 * np.exp(-x / .8)
    s = onepole(s / (len(notes) * 4), cut)
    env = np.minimum(1, x / .02) * np.exp(-x / (dur * .75)) * np.clip((dur + .6 - x) / .6, 0, 1)
    return np.tanh(s * env * 3.2) * vel


def boom(vel=1.0, length=2.2):
    n = int(SR * length)
    x = np.arange(n) / SR
    sub = np.sin(2 * np.pi * np.cumsum(30 + 70 * np.exp(-x * 7)) / SR) * np.exp(-x / .8)
    body = np.tanh(3 * np.sin(2 * np.pi * np.cumsum(60 + 120 * np.exp(-x * 22)) / SR)) * np.exp(-x / .18)
    crash = filt(rng.standard_normal(n), lo=400, hi=9000) * np.exp(-x / .45)
    metal = sum(np.sin(2 * np.pi * f * x) for f in (311, 467, 733, 1109)) * np.exp(-x / .35) * .08
    return (sub + body * .5 + crash * .28 + metal) * vel


def hit(vel=1.0):  # short punchy impact
    n = int(SR * .9)
    x = np.arange(n) / SR
    k = np.sin(2 * np.pi * np.cumsum(45 + 140 * np.exp(-x * 30)) / SR) * np.exp(-x / .22)
    nz = filt(rng.standard_normal(n), lo=900, hi=8000) * np.exp(-x / .09)
    return np.tanh((k + nz * .4) * 1.6) * vel


def taiko(vel=1.0, f0=70):
    n = int(SR * .7)
    x = np.arange(n) / SR
    s = np.sin(2 * np.pi * np.cumsum(f0 + 60 * np.exp(-x * 25)) / SR) * np.exp(-x / .2)
    skin = filt(rng.standard_normal(n), lo=150, hi=1800) * np.exp(-x / .05) * .5
    return np.tanh((s + skin) * 1.5) * vel


def tick(vel=1.0, f=3200):
    n = int(SR * .05)
    x = np.arange(n) / SR
    return (np.sin(2 * np.pi * f * x) * .5 + filt(rng.standard_normal(n), lo=2500) * .5) * np.exp(-x / .006) * vel


def hat(vel=1.0):
    n = int(SR * .08)
    x = np.arange(n) / SR
    return filt(rng.standard_normal(n), lo=8000, hi=16000) * np.exp(-x / .018) * vel


def snare(vel=1.0):
    n = int(SR * .35)
    x = np.arange(n) / SR
    return (filt(rng.standard_normal(n), lo=1500, hi=9000) * np.exp(-x / .07) + np.sin(2 * np.pi * 200 * x) * np.exp(-x / .04) * .5) * vel


def whoosh(length=.5, vel=1.0, rev=False):
    n = int(SR * length)
    x = np.arange(n) / SR
    p = x / length
    shape = p ** 3 if rev else np.sin(np.pi * p) ** 2
    nz = onepole(rng.standard_normal(n), 400 + 7000 * (p if rev else np.sin(np.pi * p)))
    nz = nz - onepole(nz, 250)
    return nz * shape * 2.2 * vel


def riser(length, vel=1.0):
    n = int(SR * length)
    x = np.arange(n) / SR
    p = x / length
    nz = onepole(rng.standard_normal(n), 300 * (40 ** p)); nz -= onepole(nz, 200)
    tone = sum(np.sin(2 * np.pi * np.cumsum(f * 2 ** (p * 2)) / SR) for f in (220, 330.5, 440.7)) / 3
    return (nz * 1.8 + tone * .35) * p ** 2.4 * vel


def shimmer(length=1.2, vel=1.0, base=1760):
    n = int(SR * length)
    x = np.arange(n) / SR
    s = sum(np.sin(2 * np.pi * base * r * x + i) * np.exp(-x / (length * .5)) for i, r in enumerate((1, 1.25, 1.5, 2, 2.5, 3)))
    return s * np.minimum(1, x / .01) * (.6 + .4 * np.sin(2 * np.pi * 9 * x)) / 6 * vel


def pluck(f, vel=1.0, length=.22):
    n = int(SR * length)
    x = np.arange(n) / SR
    s = saw(f, n) * .7 + saw(f * 1.005, n, .3) * .5 + np.sin(2 * np.pi * f / 2 * x) * .6
    s = onepole(s, 300 + 4200 * np.exp(-x * 26))
    return s * np.minimum(1, x / .002) * np.exp(-x / .07) * vel


def pad(notes, length, vel=1.0, cut=1400):
    n = int(SR * length)
    x = np.arange(n) / SR
    s = sum(saw(hz(nm) * 2 ** (d / 12), n, rng.random()) for nm in notes for d in (-.1, 0, .1))
    s = filt(s / (len(notes) * 3), hi=cut)
    return s * np.minimum(1, x / .4) * np.clip((length - x) / .6, 0, 1) * vel


def sub(f, length, vel=1.0):
    n = int(SR * length)
    x = np.arange(n) / SR
    return np.tanh(1.5 * np.sin(2 * np.pi * f * x) * np.minimum(1, x / .01) * np.clip((length - x) / .05, 0, 1)) * vel


# ---------- 0-2: cold open ----------
for k in range(8):
    add('fx', tick(.5 if k % 2 == 0 else .32, 3200 if k % 2 == 0 else 2400), k * .25 if k < 4 else 1.0 + (k - 4) * .25, pan=(-.3 if k % 2 else .3))
add('music', pad(['A1', 'E2', 'A2'], 2.2, .55, cut=500), 0)
add('fx', shimmer(1.4, .25, 2637), .35, pan=.2)
add('fx', riser(1.95, .5), .05)
add('fx', whoosh(.6, .6, rev=True), 1.4)

# ---------- 2-4: the title words ----------
add('hits', boom(1.1), 2.0)
add('music', braam(1.4, 1.0), 2.0)
for at, v in ((2.5, .8), (3.0, .85)):
    add('hits', hit(v), at); add('music', braam(.45, .55, ('A1', 'E2', 'A2')), at)
add('fx', whoosh(.45, .8), 3.42)
add('hits', hit(.7), 3.5)
add('fx', shimmer(.8, .3, 1760), 3.55, pan=-.2)
add('fx', whoosh(.5, .7, rev=True), 3.5)

# ---------- 4-10: montage and app, the driving section ----------
OST = ['A2', 'A2', 'C3', 'A2', 'E3', 'A2', 'D3', 'C3']   # 16ths
ROOT = {4: 'A1', 6: 'F1', 8: 'D2', 10: 'E1'}
for k in range(int((10 - 4) / .125)):
    at = 4 + k * .125
    bar = 4 + 2 * int((at - 4) // 2)
    shift = {4: 0, 6: -4, 8: 5, 10: -5}[bar]
    f = hz(OST[k % 8]) * 2 ** (shift / 12)
    add('music', pluck(f, .55 if k % 2 == 0 else .38), at, pan=(-.25 if k % 2 else .25))
for at in np.arange(4, 10, .25):
    add('drums', hat(.16 if int(at * 4) % 2 else .1), at, pan=.35)
for at in np.arange(4, 10, .5):
    add('drums', taiko(.85 if int(at * 2) % 2 == 0 else .55, 62 if int(at * 2) % 2 == 0 else 85), at)
for at in np.arange(5, 10, 1.0):
    add('drums', snare(.4), at + .5, pan=.05)
for bar, root in ROOT.items():
    if bar < 10:
        add('music', sub(hz(root), 2.0, .55), bar)
        add('music', pad([root[:-1] + '3', 'E3' if root[0] in 'AE' else 'A3', 'C4'], 2.0, .25, 1100), bar)
for at in (4.0, 4.25, 4.5, 4.75, 5.0, 5.25):         # every montage cut
    add('hits', hit(.55), at)
add('fx', whoosh(.6, .9), 5.45)
add('hits', boom(.7, 1.6), 6.05)
add('music', braam(.5, .6), 6.35); add('music', braam(.5, .6, ('F1', 'C2', 'F2', 'A2')), 6.5)
add('hits', hit(.9), 8.0); add('music', braam(.9, .8, ('D2', 'A2', 'D3', 'F3')), 8.0)
for at in (8.0, 8.12, 8.24):
    add('fx', whoosh(.35, .5), at, pan=(-.6, 0, .6)[[8.0, 8.12, 8.24].index(at)])
add('fx', riser(.5, .7), 9.5)

# ---------- 10-12: the audio choice (the drive drops away) ----------
add('hits', boom(.8, 1.8), 10.0)
add('music', pad(['E2', 'B2', 'E3', 'G3'], 2.0, .45, 1600), 10.0)
add('music', sub(hz('E1'), 2.0, .5), 10.0)
for at in np.arange(10, 12, .5):
    add('drums', taiko(.35, 90), at + .25)
add('fx', tick(.5, 2600), 10.9)
add('fx', shimmer(.9, .3, 2093), 10.95, pan=.3)

# ---------- 12-14: one tap ----------
add('music', pad(['C2', 'G2', 'C3', 'E3'], 2.0, .4, 1800), 12.0)
add('fx', tick(.6, 2400), 12.45)
add('fx', whoosh(.5, .8), 12.5)
add('hits', boom(.85, 1.4), 13.0)
add('music', braam(.8, .6, ('C2', 'G2', 'C3', 'E3')), 13.0)
for at in (13.25, 13.45):
    add('fx', tick(.45, 4200), at); add('fx', tick(.3, 5200), at + .03)

# ---------- 14-16: colour cuts ----------
for k, at in enumerate((14.0, 14.4, 14.8, 15.2, 15.6)):
    semis = (0, 3, 5, 7, 10)[k]
    add('hits', hit(.6), at)
    for nm in ('A2', 'E3', 'A3'):
        add('music', pluck(hz(nm) * 2 ** (semis / 12), .55, .35), at)
    add('drums', snare(.25), at + .2)
add('music', sub(hz('A1'), 2.0, .5), 14.0)

# ---------- 16-17.5: last words ----------
for at, v in ((16.0, 1.0), (16.5, .95), (17.0, 1.0)):
    add('hits', hit(v), at); add('music', braam(.42, .75), at)
for k in range(10):
    add('drums', snare(.12 + .03 * k), 16.0 + k * .1, pan=.1)
add('fx', whoosh(.3, .8, rev=True), 17.2)

# ---------- 17.5-20: the splash sting ----------
S0 = 17.5
add('hits', boom(1.0, 2.5), S0)
add('drums', taiko(.7, 55), S0); add('drums', taiko(.55, 65), S0 + .11)      # the two bars land
add('fx', whoosh(.64, .55), S0 + .30)                                           # the fold wipes
add('fx', shimmer(1.2, .45, 2349), S0 + .96, pan=.3)                            # the line of light
add('music', pad(['A2', 'E3', 'A3', 'B3', 'C4', 'E4'], 2.5, .55, 2400), S0 + .05)
add('music', sub(hz('A1'), 2.4, .6), S0)

# ---------- mix ----------
def reverb(x, secs=2.2, seed=1):
    r = np.random.default_rng(seed)
    m = int(SR * secs)
    tt = np.arange(m) / SR
    ir = r.standard_normal((m, 2)) * np.exp(-tt / (secs / 6))[:, None]
    ir = filt(ir, lo=200, hi=6000)
    ir /= np.sqrt(np.sum(ir ** 2, 0))
    size = 1 << int(np.ceil(np.log2(x.shape[0] + m)))
    return np.fft.irfft(np.fft.rfft(x, size, axis=0) * np.fft.rfft(ir, size, axis=0), size, axis=0)[: x.shape[0]]

send = BUS['music'] * .35 + BUS['hits'] * .5 + BUS['fx'] * .5 + BUS['drums'] * .15
mix = BUS['music'] * .75 + BUS['drums'] * .8 + BUS['hits'] * .9 + BUS['fx'] * .7 + reverb(send) * .45
mix = filt(mix, lo=25)
rms = np.sqrt(np.convolve(np.mean(mix ** 2, 1), np.ones(2400) / 2400, mode='same')) + 1e-6
gain = np.convolve(np.where(rms > .3, (.3 / rms) ** .35, 1.0), np.ones(1200) / 1200, mode='same')
mix *= gain[:, None]
mix *= np.clip((DUR - T) / .5, 0, 1)[:, None]
mix /= np.max(np.abs(mix)) + 1e-9
mix = np.tanh(mix * 1.5) / np.tanh(1.5)
mix *= 10 ** (-1 / 20) / np.max(np.abs(mix))
pcm = (mix * 32767).astype('<i2')
with wave.open('soundtrack.wav', 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('wrote soundtrack.wav', pcm.shape)
