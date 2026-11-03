# Nexora promo showreel

`nexora-promo.mp4`: a 20-second vertical showreel (1080×1920, 60 fps, H.264 + AAC), cut to the song from the reference video.

The style follows the reference Audiofy reel:
- dark stage with soft rose and violet glow
- two-line headlines, white then rose, revealed letter by letter
- a real phone with UI cards popping out of the screen in 3D
- floating labels
- a 3D wall of screens
- an editorial HUD

The video ends on the app's own launch splash, rebuilt from the APK's code with the same drawing, timings and curves, then the download card.

Every cut sits on the song's beat grid: 139.6 BPM, with bars every 1.72 s from 1.03 s.

| Time | Shot |
| --- | --- |
| 0–2.7 s | A rose dot becomes the play button. *Press play on everything.* The button grows to fill the screen. |
| 2.7–4.5 s | The screen folds into the app icon, the ribbon N draws, then NEXORA and *Movies, series & anime. One app.* |
| 4.5–6.2 s | *Opens on what's worth watching.* Today's pick and Surprise me pop out of the home screen. |
| 6.2–7.9 s | *Movies. Series. Anime.* One tab per beat, with Hindi hits / South Indian / Action / Thriller labels. |
| 7.9–9.6 s | *Top 10 in India.* The row lifts out of the screen and the 1, 2 and 3 fly free. |
| 9.6–11.3 s | *Hindi audio, first.* The audio picker pops out and Hindi is tapped. |
| 11.3–13.1 s | *Up to 1080p.* The number rolls 480p, 720p, 1080p and the video pops out. |
| 13.1–14.8 s | *Make it yours.* Over the song's break, the profile ring recolours through all five accents. |
| 14.8–15.6 s | The drop: a 3D wall of Nexora screens, *ALL OF IT.* |
| 15.6–16.5 s | *FREE.* then *NO SIGN-UP.* |
| 16.5–18.2 s | The Nexora launch splash. |
| 18.2–20 s | *Movies, series & anime. Free on Android.* and the Download for Android pill. |

## Files

- `showreel.html` is the whole animation. `render(t)` draws second `t` as a pure function of time. Open `showreel.html?t=8.5` in Chrome at 1080×1920 to look at any single moment.
- `song_edit.py` takes the song from the reference video and cuts it to 20 s on the beat. It removes three bars from the second phrase, joined on a downbeat, so the song keeps its own ending. It writes `soundtrack.wav`.
- `render.js` renders the video. Four headless Chromium workers render 60 fps with two sub-frames per frame for motion blur, which never blends across a hard cut. ffmpeg muxes in the audio at −14 LUFS.
- `preview.js` builds a contact sheet of chosen moments: `node preview.js sheet.jpg 1.5 4.8 9.3`.
- `shots/` holds screenshots of the app. They come from the APK's own `assets/index.html` running in a phone-sized Chromium (412×892 at 3×), with analytics pings and third-party player frames blocked during the capture.

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
