# Nexora promo showreel

`nexora-promo.mp4`: a 20-second vertical promo (1080×1920, 30 fps, H.264 + AAC, 24 MB), made for Reels, Shorts and Status. `node render.js` also writes a higher-bitrate `nexora-promo-master.mp4`, which is not kept in git.

A Netflix-style trailer with an editorial HUD (timecode, scene labels, corner marks). It has hard cuts on colour fields, screen-filling kinetic type, and a sound design of braams and impacts hit-synced to every cut. It ends on the app's own launch splash, rebuilt from the APK's code with the same drawing, timings and curves.

| Time | Shot |
| --- | --- |
| 0–2 s | Cold open: NEXORA PRESENTS with clock ticks, and an anamorphic flare that builds into the first braam. |
| 2–4 s | PRESS / PLAY / ON / *everything.* Each word slams in on its own colour field. |
| 4–5.5 s | Key-art montage, one poster every quarter beat: EVERY STORY. EVERY GENRE. ONE APP. |
| 5.5–6.2 s | The last poster pulls back into the full poster grid, which tilts away into a wall. |
| 6.2–8 s | The phone rises out of the wall. ALL OF IT. ONE APP. |
| 8–10 s | TOP 10: the 1, 2 and 3 burst out of the screen, then the camera dives into the phone. |
| 10–12 s | HINDI, FIRST. A liquid-glass audio control over key art; a tap moves Original to Hindi. |
| 12–14 s | ONE TAP. The Play pill morphs into the video frame, and the counter goes 480P, 720P, 1080P. |
| 14–16 s | MAKE IT YOURS. Five accent colour fields cut on the beat, with the profile ring recoloured to match. |
| 16–17.5 s | FREE. NO SIGN-UP. 222 KB. Then an iris closes. |
| 17.5–20 s | The Nexora launch splash: the bars fall in, the fold wipes, the light passes, then NEXORA and DEVELOPED BY ANSHXR.YN. |

## Files

- `showreel.html` is the whole animation. `render(t)` draws second `t` as a pure function of time. Open `showreel.html?t=12.3` in Chrome at 1080×1920 to look at any single moment.
- `soundtrack.py` synthesises the trailer score with numpy (ticks, braams, impacts, a 16th-note ostinato, taiko, risers and the splash sting) and writes `soundtrack.wav`. It has no samples: an FM electric piano on 9th chords, a half-time groove, sub bass and bells, at 120 BPM with bars on the same lines as the cuts. For a licensed track instead, drop its audio in place of `soundtrack.wav`; the cuts land every 2 s from 0.5 s.
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
