"""Cut the promo's song to 20 s on the beat. Takes the reference video (or any audio file), removes three
bars from its second phrase on downbeats so the song keeps its own ending, and writes soundtrack.wav.
Usage: python3 song_edit.py <input video or audio> [out.wav]"""
import subprocess
import sys
import wave
import numpy as np

SR = 48000
src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else 'soundtrack.wav'
raw = subprocess.run(['ffmpeg', '-nostdin', '-loglevel', 'error', '-i', src, '-vn', '-ac', '2', '-ar', str(SR), '-f', 's16le', '-'],
                     check=True, capture_output=True).stdout
x = np.frombuffer(raw, '<i2').reshape(-1, 2).astype(np.float64) / 32768

# beat grid, measured from the song: 139.6 BPM, first beat at 0.17 s, downbeats every 4 beats from beat 2
BEAT = 60 / 139.6
def downbeat(k):
    return 0.17 + BEAT * (2 + 4 * k)

def snap(t, span=.04):
    """Move a grid time onto the actual kick transient nearby (largest rise in low-band energy)."""
    a, b = int((t - span) * SR), int((t + span) * SR)
    seg = x[a:b].mean(1)
    lo = np.convolve(seg, np.ones(64) / 64, 'same')            # rough low-pass
    env = np.convolve(lo ** 2, np.ones(96) / 96, 'same')
    rise = np.diff(env, prepend=env[0])
    return (a + int(np.argmax(rise))) / SR

cut_from, cut_to = snap(downbeat(9)), snap(downbeat(12))      # drop bars 9, 10 and 11
print(f'splice {cut_from:.3f} s -> {cut_to:.3f} s (removes {cut_to - cut_from:.3f} s)')
i, j = int(cut_from * SR), int(cut_to * SR)
fade = int(.012 * SR)
ramp = np.linspace(0, 1, fade)[:, None]
joined = x[i - fade:i] * (1 - ramp) + x[j - fade:j] * ramp     # equal-gain crossfade into the next downbeat
y = np.concatenate([x[:i - fade], joined, x[j:]])
y = y[: int(20.0 * SR)]
tail = int(.45 * SR)
y[-tail:] *= np.linspace(1, 0, tail)[:, None] ** 2
y *= 10 ** (-1 / 20) / max(1e-9, np.max(np.abs(y)))
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((y * 32767).astype('<i2').tobytes())
print(f'wrote {out}: {len(y) / SR:.2f} s')

# Loudness, kick and a 24-band spectrum per video frame (60 fps), for the audio-reactive parts of showreel.html
import json, os
fps, hop = 60, SR // 60
mono = y.mean(1)
rms, low, bands = [], [], []
f = np.fft.rfftfreq(2048, 1 / SR)
edges = np.geomspace(60, 12000, 25)
for i in range(int(len(mono) / SR * fps)):
    seg = mono[i * hop:i * hop + 2048]
    seg = np.pad(seg, (0, 2048 - len(seg)))
    S = np.abs(np.fft.rfft(seg * np.hanning(2048)))
    rms.append(float(np.sqrt(np.mean(seg ** 2))))
    low.append(float(S[f < 150].sum()))
    bands.append([float(S[(f >= edges[k]) & (f < edges[k + 1])].mean()) if np.any((f >= edges[k]) & (f < edges[k + 1])) else 0.0 for k in range(24)])
rms, low, bands = np.array(rms), np.array(low), np.array(bands)
rms /= rms.max(); low /= np.percentile(low, 99)
bands /= np.maximum(np.percentile(bands, 98, axis=0), 1e-9)
os.makedirs('cache', exist_ok=True)
with open('cache/env.js', 'w') as fh:
    fh.write('window.ENV=' + json.dumps({'fps': fps, 'rms': [round(v, 3) for v in rms], 'low': [round(min(v, 1.5), 3) for v in low],
                                        'bands': [[round(min(v, 1.4), 2) for v in b] for b in bands]}) + ';')
print('wrote cache/env.js')
