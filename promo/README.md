# Nexora promo showreel

`nexora-promo.mp4`: a 20-second vertical promo (1080×1920, 30 fps, H.264 + AAC, 24 MB), made for Reels, Shorts and Status. `node render.js` also writes a higher-bitrate `nexora-promo-master.mp4`, which is not kept in git.

The cut is restrained and editorial. It uses hard cuts on bar lines, real phone hardware, macro close-ups of the UI with depth of field, and the site's own copy. There is no glitch, no camera shake, no light leaks, and no mention of servers or pop-ups.

| Time | Shot |
| --- | --- |
| 0.0–2.5 s | Poster shelves drift, the middle one sharp. *The whole library.* |
| 2.5–4.5 s | Macro on a title's audio choice. *In Hindi, first. Or English. Or the original.* |
| 4.5–6.5 s | The N draws itself, then NEXORA and Movies · Series · Anime. |
| 6.5–8.5 s | 3D phone, and the home feed scrolls. *Opens on what's worth watching.* |
| 8.5–10.5 s | Tap tour, one beat each: *Movies. Series. Anime. And what's new.* |
| 10.5–12.5 s | Play is tapped and the phone turns to landscape video. *One tap, and it plays.* Up to 1080p. |
| 12.5–14.5 s | Macro on the profile ring as it recolours through all five accents. *Make it yours.* |
| 14.5–16.5 s | One word per beat: *Free. No sign-up. 222 KB. Just press play.* |
| 16.5–20 s | *Tonight's sorted.*, Download for Android, and the phone rising. |

## Files

- `showreel.html` is the whole animation. `render(t)` draws second `t` as a pure function of time. Open `showreel.html?t=12.3` in Chrome at 1080×1920 to look at any single moment.
- `soundtrack.py` synthesises the score with numpy and writes `soundtrack.wav`. It has no samples: an FM electric piano on 9th chords, a half-time groove, sub bass and bells, at 120 BPM with bars on the same lines as the cuts. For a licensed track instead, drop its audio in place of `soundtrack.wav`; the cuts land every 2 s from 0.5 s.
- `render.js` renders the video. Four headless Chromium workers each blend 4 sub-frames per frame, which gives a 180° shutter motion blur. ffmpeg encodes the result and muxes in the audio at −14 LUFS.
- `preview.js` builds a contact sheet of chosen moments: `node preview.js sheet.jpg 1.5 4.8 9.3`.
- `shots/` holds fresh screenshots of the app. They come from the APK's own `assets/index.html` running in a phone-sized Chromium (412×892 at 3×), with analytics pings and third-party player frames blocked during the capture. `player.jpg` is the existing one from `website/assets`.

## Rebuild

```bash
./fetch-assets.sh
```

```bash
python3 soundtrack.py
```

```bash
node render.js
```

The full render takes about 15–30 minutes on 4 cores.
