# Nexora promo showreel

`nexora-promo.mp4`: a 20-second vertical showreel (1080×1920, 60 fps, H.264 + AAC), cut to the song from the reference video.

The approach comes from studying the best-rated videos and prompts on prompt-motion.com:
- The UI is rebuilt as live components instead of raw screenshots, so every part can move.
- One shot turns into the next.
- Light and dark scenes flip on the cut.
- The text morphs.
- The motion follows the music: the waveform and the beat bumps read the song itself.
- There are no HUD labels in the corners.

Every cut sits on the song's grid: 139.6 BPM, with bars every 1.72 s from 1.03 s. The video ends on the app's own launch splash, rebuilt from the APK's code, then the download card.

| Time | Shot |
| --- | --- |
| 0–1.0 s | A search bar types "Something to watch tonight". |
| 1.0–2.7 s | The search bar morphs into the rose Play button. *Press play.* A tap, then the button bursts into sparks. |
| 2.7–4.5 s | Posters fly out into a rotating 3D ring. *on everything.* |
| 4.5–6.2 s | The ring falls into the app's home rows as the phone draws itself around them, and the row titles type in. *Opens on what's worth watching.* |
| 6.2–7.9 s | Light mode. *Top 10 in India.* A giant numeral rolls 8 → 1 as the posters slide in, ending on #1 IN INDIA. |
| 7.9–9.6 s | *Hindi audio, first.* The audio picker slides from Original to Hindi, and Hindi becomes हिंदी over waveform bars driven by the song. |
| 9.6–11.3 s | *One tap, it plays.* Verity's Play pill grows into the video, and the badge rolls 480p → 720p → 1080p. |
| 11.3–13.1 s | *Never lose your place.* Continue watching fills up, My List turns into "In My List" with a tick, and a toast says "Saved on your phone. No account." |
| 13.1–14.8 s | Over the song's break, *Make it yours.* The profile ring recolours through all five accents and the stats count up. |
| 14.8–15.6 s | The drop: about 130 posters fly in and form the ribbon N. *ALL OF IT.* |
| 15.6–16.5 s | *Free.* morphs into *No sign-up.* |
| 16.5–18.2 s | The Nexora launch splash. |
| 18.2–20 s | *Press play on everything.* and Download for Android. |

## Files

- `showreel.html` is the whole animation. `render(t)` draws second `t` as a pure function of time. Open `showreel.html?t=8.5` in Chrome at 1080×1920 to look at any single moment.
- `song_edit.py` takes the song from the reference video and cuts it to 20 s on downbeats, keeping the song's own ending. It writes `soundtrack.wav`, plus `cache/env.js` with the loudness and spectrum the animation reacts to.
- `render.js` renders the video. Four headless Chromium workers render 60 fps with two sub-frames per frame for motion blur, which never blends across a hard cut. ffmpeg muxes in the audio at −14 LUFS.
- `preview.js` builds a contact sheet of chosen moments: `node preview.js sheet.jpg 1.5 4.8 9.3`.
- `PROMPTS.md` holds the prompts for every version made so far.
- `shots/` holds screenshots of the app, taken from the APK's own UI.

## Rebuild

```bash
./fetch-assets.sh
```

```bash
python3 song_edit.py path/to/reference.mp4
```

```bash
node render.js
```

For best quality on your own GPU, use `node render.js 8 4 60` (8 workers, 4 sub-frames).
