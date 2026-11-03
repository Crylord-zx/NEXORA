"""Nexora promo soundtrack, synthesised from scratch (no samples) and cut to the same
120 BPM grid as showreel.html. Writes soundtrack.wav (48 kHz, stereo, 20 s).
Run: python3 soundtrack.py"""
import wave
import numpy as np

SR = 48000
DUR = 20.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
t_all = np.arange(N) / SR
L = np.zeros(N)
Rch = np.zeros(N)


def add(sig, at, gain=1.0, pan=0.0):
    """Mix a mono signal in at time `at` (seconds); pan -1..1."""
    i = int(at * SR)
    if i >= N:
        return
    sig = sig[: N - max(i, 0)]
    if i < 0:
        sig, i = sig[-i:], 0
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    L[i:i + len(sig)] += sig * gain * l * 1.414
    Rch[i:i + len(sig)] += sig * gain * r * 1.414


def env(n, a, d):  # attack/decay in seconds, exponential decay
    x = np.arange(n) / SR
    return np.minimum(1, x / max(a, 1e-4)) * np.exp(-x / d)


def onepole(x, cut):
    """Low-pass with a cutoff that may vary per sample (Hz)."""
    cut = np.broadcast_to(np.asarray(cut, float), x.shape)
    a = 1 - np.exp(-2 * np.pi * cut / SR)
    y = np.empty_like(x)
    s = 0.0
    for k in range(len(x)):
        s += a[k] * (x[k] - s)
        y[k] = s
    return y


def fft_filter(x, lo=None, hi=None):
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(len(x), 1 / SR)
    g = np.ones_like(f)
    if hi:
        g *= 1 / np.sqrt(1 + (f / hi) ** 4)
    if lo:
        g *= 1 / np.sqrt(1 + (lo / np.maximum(f, 1e-3)) ** 4)
    return np.fft.irfft(X * g, len(x))


def saw(freq, n, phase=0.0):
    ph = (np.cumsum(np.broadcast_to(freq, (n,)) / SR) + phase) % 1
    return 2 * ph - 1


def note(name):
    names = {'C': -9, 'D': -7, 'E': -5, 'F': -4, 'G': -2, 'A': 0, 'B': 2}
    n, octv = name[:-1], int(name[-1])
    semi = names[n[0]] + (1 if '#' in n else 0) + (octv - 4) * 12
    return 440 * 2 ** (semi / 12)


# ---------- instruments ----------
def kick(gain=1.0, big=False):
    n = int(SR * (0.9 if big else 0.45))
    x = np.arange(n) / SR
    f = 42 + 130 * np.exp(-x * 28) + (40 * np.exp(-x * 6) if big else 0)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / (0.38 if big else 0.16))
    s += 0.5 * rng.standard_normal(n) * np.exp(-x * 300)  # click
    return np.tanh(s * 1.6) * gain


def clap(gain=1.0):
    n = int(SR * 0.35)
    x = np.arange(n) / SR
    nz = fft_filter(rng.standard_normal(n), lo=900, hi=5000)
    e = np.zeros(n)
    for off in (0, .008, .016, .024):
        i = int(off * SR)
        e[i:] += np.exp(-(x[: n - i]) / (0.012 if off < .024 else 0.11))
    return nz * e * 0.6 * gain


def hat(gain=1.0, length=.045):
    n = int(SR * 0.12)
    x = np.arange(n) / SR
    return fft_filter(rng.standard_normal(n), lo=7000) * np.exp(-x / length) * gain


def boom(gain=1.0, length=2.2):
    """Trailer impact: sub drop, distorted body, noise crash."""
    n = int(SR * length)
    x = np.arange(n) / SR
    f = 30 + 60 * np.exp(-x * 5)
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x / 0.9)
    body = np.tanh(3 * np.sin(2 * np.pi * np.cumsum(55 + 90 * np.exp(-x * 18)) / SR)) * np.exp(-x / .25)
    crash = fft_filter(rng.standard_normal(n), lo=300, hi=9000) * np.exp(-x / 0.55)
    return (sub * 1.0 + body * .45 + crash * .35) * gain


def riser(length, f0=200, f1=4000, gain=1.0):
    n = int(SR * length)
    x = np.arange(n) / SR
    p = x / length
    nz = onepole(rng.standard_normal(n), f0 * (f1 / f0) ** p)
    nz = nz - onepole(nz, 120)
    tone = np.sin(2 * np.pi * np.cumsum(110 * 2 ** (p * 4)) / SR) * 0.25
    return (nz * 2.2 + tone) * (p ** 2.2) * gain


def whoosh(length=.5, gain=1.0):
    n = int(SR * length)
    x = np.arange(n) / SR
    p = x / length
    bell = np.sin(np.pi * p) ** 2
    nz = onepole(rng.standard_normal(n), 300 + 5000 * np.sin(np.pi * p) ** 1.5)
    nz = nz - onepole(nz, 200)
    return nz * bell * .9 * gain


def blip(freq=1800, gain=1.0, length=.06):
    n = int(SR * length)
    x = np.arange(n) / SR
    return (np.sin(2 * np.pi * freq * x) + .3 * np.sin(4 * np.pi * freq * x)) * env(n, .002, length / 3) * gain


def pluck(freq, length=.35, gain=1.0):
    n = int(SR * length)
    x = np.arange(n) / SR
    s = saw(freq, n) * .5 + np.sin(2 * np.pi * freq * x)
    s = onepole(s, 600 + 6000 * np.exp(-x * 18))
    return s * env(n, .003, .12) * gain


def supersaw(freqs, length, cutoff=1800):
    n = int(SR * length)
    s = np.zeros(n)
    for f in freqs:
        for d in (-.12, -.05, 0, .05, .12):
            s += saw(f * 2 ** (d / 12), n, rng.random())
    s = fft_filter(s / (len(freqs) * 5), hi=cutoff)
    return s


# ---------- arrangement ----------
BEAT = .5
CHORDS = [('A2', ['A3', 'C4', 'E4', 'A4']), ('F2', ['F3', 'A3', 'C4', 'F4']),
          ('C3', ['C4', 'E4', 'G4', 'C5']), ('G2', ['G3', 'B3', 'D4', 'G4'])]

def chord_at(t):
    return CHORDS[int(max(0, t - 2) // 4) % 4]

# intro: drone + shimmer + riser + reverse swell into the 2.0 hit
n = int(SR * 2.3)
x = np.arange(n) / SR
drone = (np.sin(2 * np.pi * 55 * x) + .5 * np.sin(2 * np.pi * 82.4 * x) + .25 * saw(110, n)) * np.minimum(1, x / 1.6)
add(fft_filter(drone, hi=600) * .35, 0)
shimmer = sum(np.sin(2 * np.pi * f * x + i) for i, f in enumerate([1760, 2217, 2637, 3520])) * (.5 + .5 * np.sin(2 * np.pi * 6 * x)) * (x / 2.3) ** 2
add(shimmer * .05, 0, pan=.3)
add(riser(2.0, 150, 6000), 0.0, .4)
# logo strokes: three soft hits as the N draws
for at, f in ((.35, 220), (.7, 277), (1.05, 330)):
    add(pluck(f, .6) * .5, at, pan=(-.4, 0, .4)[[.35, .7, 1.05].index(at)])
    add(kick(.35), at)

# main hits
add(boom(1.3, 2.5), 2.0)
add(kick(1.0, big=True), 2.0)

# drums 2.0 to 16.0
for k in range(28):
    at = 2.0 + k * BEAT
    if k > 0:
        add(kick(.85), at)
    if k % 2 == 1:
        add(clap(.55), at, pan=.05)
    add(hat(.22), at + .25, pan=.35)
    if at >= 8.0:
        add(hat(.1, .025), at + .125, pan=-.35)
        add(hat(.1, .025), at + .375, pan=-.35)

# sidechain envelope from the kick grid
duck = np.ones(N)
for k in range(28):
    i = int((2.0 + k * BEAT) * SR)
    m = min(N - i, int(SR * .4))
    duck[i:i + m] = np.minimum(duck[i:i + m], 1 - .75 * np.exp(-np.arange(m) / SR / .09))

# pad 2.0 to 18.0
pad = np.zeros(N)
for b in range(4):
    root, tones = CHORDS[b]
    at = 2.0 + b * 4
    seg = supersaw([note(n) for n in tones], 4.2, cutoff=900 + b * 350)
    i = int(at * SR)
    fade = np.minimum(1, np.arange(len(seg)) / (SR * .05)) * np.minimum(1, (len(seg) - np.arange(len(seg))) / (SR * .2))
    pad[i:i + len(seg)] += seg[: N - i] * fade[: N - i]
pad *= duck * np.clip((t_all - 2.0) / .4, 0, 1)
add(pad * .5, 0, pan=-.2)
add(np.roll(pad, int(SR * .012)) * .5, 0, pan=.2)

# bass: off-beat eighths from 5.0
for k in range(int((16 - 5) / .25)):
    at = 5.0 + k * .25
    if k % 2 == 0:
        continue
    root = note(chord_at(at)[0])
    m = int(SR * .22)
    xx = np.arange(m) / SR
    b = onepole(saw(root, m), 500 + 1400 * np.exp(-xx * 20)) * env(m, .004, .12)
    add(np.tanh(b * 2) * .5, at)

# arp: sixteenths 8.0 to 16.0
pattern = [0, 1, 2, 3, 2, 1, 2, 3]
for k in range(32 * 1):
    at = 8.0 + k * .25
    tones = chord_at(at)[1]
    f = note(tones[pattern[k % 8]]) * 2
    add(pluck(f, .3, .22), at, pan=(-.5 if k % 2 else .5))
    add(pluck(f, .3, .08), at + .375, pan=(.5 if k % 2 else -.5))  # dotted-eighth echo

# transitions
for at, ln, g in ((4.5, .55, 1.0), (7.75, .55, 1.1), (11.55, .65, .9), (13.65, .45, .8), (15.7, .4, 1.0)):
    add(whoosh(ln, g), at, pan=(.3 if at < 10 else -.3))
add(riser(.5, 400, 8000, .25), 4.5)

# UI: taps, chips, accent switches
for at in (9.92, 10.17, 10.42, 11.4):
    add(blip(2400, .25, .035), at, pan=.1)
for at in (9.0, 9.55, 9.72, 11.0, 12.3, 12.6, 12.9, 14.3, 14.8, 15.3):
    add(blip(1500, .18, .08), at, pan=.2)
    add(blip(2250, .1, .08), at + .03, pan=-.2)
for k, at in enumerate((14.25, 14.75, 15.25, 15.75)):
    add(pluck(note('E5') * 2 ** (k * 2 / 12), .5, .35), at, pan=(k - 1.5) / 2)
add(boom(.35, .8), 12.15)

# stats 16.0 to 18.0: slams on each card, snare roll and riser into the last hit
for at in (16.0, 16.5, 17.0, 17.5):
    add(boom(.55, .6), at)
    add(kick(.9), at)
    add(clap(.35), at)
for k in range(16):
    at = 16.0 + k * .125
    if at < 17.875:
        add(clap(.12 + .25 * k / 16), at + .0625 * (k % 2), pan=.1)
add(riser(1.9, 300, 9000, .45), 16.0)
add(whoosh(.4, .9), 17.6)

# finale
add(boom(1.4, 2.0), 18.0)
add(kick(1.0, big=True), 18.0)
n = int(SR * 2.0)
x = np.arange(n) / SR
fin = supersaw([note(n) for n in ('A3', 'C4', 'E4', 'A4', 'E5')], 2.0, cutoff=2600) * np.exp(-x / 1.4)
add(fin * .55, 18.0, pan=-.15)
add(np.roll(fin, int(SR * .015)) * .55, 18.0, pan=.15)
add(blip(3520, .12, .5), 19.15, pan=.4)  # button shine
add(pluck(note('A5'), .8, .25), 18.55, pan=0)

# ---------- reverb (FFT convolution, decaying noise IR) ----------
def reverb(x, secs=1.6, mix=.22, seed=1):
    r = np.random.default_rng(seed)
    m = int(SR * secs)
    ir = r.standard_normal(m) * np.exp(-np.arange(m) / SR / (secs / 5))
    ir = fft_filter(ir, lo=200, hi=7000)
    ir /= np.sqrt(np.sum(ir ** 2))
    size = 1 << int(np.ceil(np.log2(len(x) + m)))
    wet = np.fft.irfft(np.fft.rfft(x, size) * np.fft.rfft(ir, size), size)[: len(x)]
    return x + wet * mix * 3

L = reverb(L, seed=1)
Rch = reverb(Rch, seed=2)

# ---------- master ----------
out = np.stack([L, Rch], 1)
out = fft_filter(out[:, 0], lo=25)[:, None] * [1, 0] + fft_filter(out[:, 1], lo=25)[:, None] * [0, 1]
fade = np.clip((DUR - t_all) / .35, 0, 1)[:, None]
out *= fade
out /= np.max(np.abs(out)) + 1e-9
out = np.tanh(out * 1.8) / np.tanh(1.8)  # glue / soft clip
out *= 10 ** (-1 / 20) / np.max(np.abs(out))
pcm = (out * 32767).astype('<i2')
with wave.open('soundtrack.wav', 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(pcm.tobytes())
print('wrote soundtrack.wav', pcm.shape)
