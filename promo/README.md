# Nexora promo showreel

`nexora-promo.mp4`: a 20-second vertical promo (1080×1920, 30 fps, H.264 + AAC, 24 MB), made for Reels, Shorts and Status. `node render.js` also writes a higher-bitrate `nexora-promo-master.mp4`, which is not kept in git.

| Time | Beat |
| --- | --- |
| 0.0–2.5 s | A projector light ignites and the **N** draws itself in three strokes. Then come the impact flash, a shockwave and the NEXORA wordmark. |
| 2.5–5.0 s | Kinetic type: *Press / play / on / everything.* The camera then zooms through the play triangle. |
| 5.0–8.0 s | A 3D tilted poster wall with *Movies. Series. Anime.*, followed by a whip pan. |
| 8.0–10.8 s | 3D phone on the real home feed: it scrolls, callouts appear (Top 10 in India, Hindi hits, South Indian) and a tap tour runs through Movies, Series and Anime. |
| 10.8–13.7 s | A title page and the Hindi audio callout. Play is tapped, the phone does a 360° flip into the player, then the 1080p / 28 servers / pop-ups blocked callouts appear. |
| 13.7–16.0 s | *Make it yours.* The profile recolours live through all five accents, and the whole scene follows. |
| 16.0–18.0 s | Stat slams with glitch cuts: 222 KB, 1080p, 28 servers, 0 sign-ups. |
| 18.0–20.0 s | End card: *Tonight's sorted.* and the Download for Android call to action. |

## Files

- `showreel.html` is the whole animation. `render(t)` draws second `t` as a pure function of time. Open `showreel.html?t=12.3` in Chrome at 1080×1920 to look at any single moment.
- `soundtrack.py` synthesises the music and sound design with numpy and writes `soundtrack.wav`. It has no samples and is cut to the same 120 BPM grid.
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
