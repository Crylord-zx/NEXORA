# Nexora promo video prompts

These are the prompts behind the four Nexora videos made so far. Paste one into Claude (or any AI that writes motion-graphics code) together with the files listed under **Assets**.

Each prompt asks for a self-contained HTML/JS animation where `render(t)` draws second `t`. You can then render it frame by frame on your own machine:
- **The quick way:** run `node render.js` from this folder; it works with any `showreel.html`.
- **On your GPU:** use Chrome/Puppeteer with GPU on and `deviceScaleFactor: 2`, then encode with `ffmpeg -c:v h264_nvenc -cq 16`.

The original source of each version is in git history (see each prompt).

## Assets (all in this repo)

- **App screenshots** in `promo/shots/` (1236×2676, taken from the real app):
  - `home.jpg` and `home_tall.jpg` (the full home feed)
  - `movies.jpg`, `series.jpg`, `anime.jpg`, `new.jpg`, `search.jpg`
  - `title.jpg` (Verity), `title_anime.jpg` (Mob Psycho 100), `title_more.jpg`
  - `player.jpg` and `player_video.jpg` (the player's video frame)
  - `profile_rose.jpg`, `profile_violet.jpg`, `profile_ocean.jpg`, `profile_emerald.jpg`, `profile_gold.jpg`
  - `ring_*.jpg` (close crops of the profile ring in each colour)
  - `topbar.png` and `tabbar.png`
- **Posters:** the list in `website/assets/posters.json`. Use them from TMDB as `https://image.tmdb.org/t/p/w780/<path>`.
- **Brand colours:** rose `#FF2E55`, crimson `#E81B43`, violet `#9C27B0` / `#7B1FA2`, black `#050507`. The five accent colours are:
  - Rose `#FF2D55`
  - Violet `#A06BFF`
  - Ocean `#2FA8FF`
  - Emerald `#2BD17E`
  - Gold `#F5B83D`
- **Fonts:** Inter (the app's font), Inter Tight, Instrument Serif italic, Archivo (width 62–125), JetBrains Mono.
- **The app's launch splash**, copied exactly from the APK's `assets/index.html`:
  - The drawing is a long ribbon N in a 540×800 viewBox: a left bar 155 wide (gradient `#E81B43` → `#B3092B` → `#600315`), a right bar at x=385 (gradient `#9C27B0` → `#7B1FA2` → `#4A0E6B`), and a fold polygon `0,0 155,0 540,800 385,800` (gradient `#FF2E55` → `#E01E78` → `#BA28C7` → `#9C27B0`, with a drop shadow).
  - The left bar grows from the top: scaleY 0→1 over 620 ms, `cubic-bezier(.16,1,.3,1)`.
  - The right bar grows from the bottom: 620 ms, starting at 110 ms, same curve.
  - A mask wipes the fold from the top: 640 ms, starting at 300 ms, `cubic-bezier(.65,0,.35,1)`.
  - A white shine passes: translateX −340 → 1000 with skewX(−18°), 720 ms, starting at 960 ms, `cubic-bezier(.4,0,.2,1)`.
  - "NEXORA" (Inter 800, letter-spacing .42em) rises 10 px with a fade in: 620 ms, starting at 820 ms.
  - "DEVELOPED BY ANSHXR.YN" (Inter 600, colour `#8A8CA2`, letter-spacing .38em) rises the same way: 620 ms, starting at 980 ms.
  - The background is pure black.

---

## 1. Neon launch film (first version, git `c3bfb07`)

> Make a 20-second vertical (1080×1920, 30 fps) launch video for NEXORA, a free Android app for movies, web series and anime with Hindi audio, up to 1080p and no sign-up. Make it like a heavy After Effects editor would, cut on a 120 BPM grid.
>
> 1. **0–2.5 s:** A WebGL projector-light background (volumetric rays in rose `#ff2d55` and violet `#8b5cf6`, with dust motes). The N logo draws itself in three strokes (left bar up, diagonal down, right bar up). At 2.0 s comes an impact: a white flash, camera shake, a shockwave ring, and the NEXORA wordmark tracking in with "Movies · Series · Anime".
> 2. **2.5–5 s:** Kinetic type, left-aligned at 250 px: "Press / play / on / *everything.*". Each word gets a mask reveal with an RGB-split glitch, and the last word is in Instrument Serif italic with a gradient. A play triangle pops next to "play". The camera then zooms through that triangle, which grows to reveal the next scene inside it.
> 3. **5–8 s:** A tilted 3D poster wall (7 columns scrolling in opposite directions) with "Movies." / "*Series.*" / "Anime." (outlined) on the beats, the caption "All in one free app", then a whip pan.
> 4. **8–16 s:** A 3D phone showing the real screens.
>    - The home feed scrolls, with glass callout chips: Top 10 in India, Hindi hits, South Indian.
>    - A tab tour taps through Movies, Series and Anime.
>    - Play is tapped on a title page, then the phone does a 360° flip (its back shows the N) into the player, with "Up to 1080p" chips.
>    - The profile recolours through all five accent colours as the whole scene's light changes colour, with "Make it yours."
> 5. **16–18 s:** Stat slams with glitch slices: 222 KB, 1080p, 0 sign-ups.
> 6. **18–20 s:** End card with the logo, "Tonight's *sorted.*", a white "Download for Android" pill with a glow, and a giant faded NEXORA wordmark.
>
> Add film grain, a vignette, light leaks on the transitions, and 180° shutter motion blur. Do not mention servers or pop-ups.

## 2. Cinematic clean (Apple-style, git `b3165d9`)

> Make a 20-second vertical (1080×1920, 30 fps) promo for NEXORA in a restrained, premium, Apple-keynote style. Use no glitch, no shake, no neon rays and no light leaks. Use hard cuts on bar lines of a 120 BPM score (bars start at 0.5 s and every 2 s after).
>
> Visual style:
> - Mostly black, with a soft charcoal spotlight.
> - A realistic phone: titanium edge, side buttons, a soft floor shadow.
> - Macro close-ups of the real app UI with depth of field (a backdrop-blur band, so only a strip is sharp).
> - Headlines in Inter Tight 650 at about 110 px, with one Instrument Serif italic word in a rose→violet gradient. Text appears through a mask reveal.
>
> Shots:
> 1. **0–2.5 s:** Three shelves of posters drift sideways, the middle one sharp: "The whole *library.*"
> 2. **2.5–4.5 s:** A macro on a title's audio picker: "In *Hindi,* first. Or English. Or the original."
> 3. **4.5–6.5 s:** The N logo draws, then NEXORA and "Movies · Series · Anime".
> 4. **6.5–8.5 s:** The phone at a 3/4 angle as the home feed scrolls: "Opens on what's *worth* watching."
> 5. **8.5–10.5 s:** A tap tour, one tab per beat: "Movies." "Series." "Anime." "And what's *new.*"
> 6. **10.5–12.5 s:** Play is tapped and the phone turns to landscape video: "One tap, and it *plays.*" (Up to 1080p)
> 7. **12.5–14.5 s:** A macro on the profile ring as it recolours through all five accents: "Make it *yours.*"
> 8. **14.5–16.5 s:** One word per beat: "Free." "No sign-up." "222 KB." "Just press *play.*"
> 9. **16.5–20 s:** "Tonight's *sorted.*", a white Download for Android pill, and the phone rising.
>
> Music: a warm FM electric piano on 9th chords (Fmaj9, G6/9, Am9, Em11), a half-time groove, sub bass and bells. Keep the motion blur from crossing hard cuts.

## 3. Netflix-style trailer (git `abac020`)

> Make a 20-second vertical (1080×1920, 30 fps) Netflix-style trailer for NEXORA. Add an editorial HUD on every frame: corner marks, "NEXORA / TRAILER", "● NOW STREAMING", a running timecode and scene labels.
>
> Shots:
> 1. **0–2 s:** Cold open: "NEXORA PRESENTS" flickers in, with clock ticks and a red anamorphic flare building into the first braam.
> 2. **2–4 s:** "PRESS" / "PLAY" / "ON" / "*everything.*" Each word fills the width (Archivo at 125% width, weight 900) and slams in with motion smear, each on its own hard-cut colour field: crimson `#E81B43`, black, violet `#7B1FA2`, black.
> 3. **4–5.5 s:** A key-art montage, one full-bleed poster every quarter beat, with "EVERY / STORY. / EVERY / GENRE. / ONE / APP."
> 4. **5.5–6.2 s:** The last poster pulls back into a 5×7 poster grid, which tilts away into a 3D wall.
> 5. **6.2–8 s:** The phone rises out of the wall: "ALL OF IT. / ONE APP."
> 6. **8–10 s:** "TOP 10 / In India · This month". Giant outlined 1, 2 and 3 burst out of the phone screen, then the camera dives into the phone.
> 7. **10–12 s:** "HINDI, / FIRST." A liquid-glass segmented control (Hindi / English / Original) over full-bleed key art. A tap moves the selection from Original to Hindi, with "Pick it once. Nexora remembers."
> 8. **12–14 s:** "ONE TAP." The white Play pill is tapped and morphs into the 16:9 video frame. The counter steps 480P → 720P → 1080P.
> 9. **14–16 s:** "MAKE IT / YOURS." Five hard-cut accent colour fields with the profile ring recoloured to match and the hex code shown.
> 10. **16–17.5 s:** "FREE." "NO SIGN-UP." "222 KB." Then a red-edged iris closes.
> 11. **17.5–20 s:** The app's exact launch splash (see Assets), with "Free on Android".
>
> Sound: a trailer design of ticks, braams, impacts, a 16th-note ostinato, taiko, risers and a splash sting, all hit-synced to the cuts.

## 4. Showreel cut to the song (git `16030da`)

> Make a 20-second vertical (1080×1920, 60 fps) showreel for NEXORA, in the style of a modern app showreel. Use these elements:
> - A dark `#050507` stage with soft drifting rose and violet glows.
> - Two-line headlines in Inter 800 at 116 px, the first line white and the second line rose `#FF2E55`, revealed letter by letter (14 ms stagger, rising with a blur).
> - A realistic phone with the real app screens. UI cards pop out of the screen in true 3D: they share the phone's 3D space, translateZ 160–260 px, scale 1.1–2×, with a spring curve, while the screen behind them dims.
> - Floating dark pill labels with an accent dot.
> - An editorial HUD: "● NEXORA — SHOWREEL", "TC 00:00:SS:FF · 140 BPM", the scene label, "1080×1920 · 60 FPS", and an accent progress bar along the bottom.
>
> The song runs at 139.6 BPM, with a bar every 1.719 s from 1.03 s. The song is cut to 20 s by removing three bars on a downbeat.
>
> Shots:
> 1. **0–2.75 s:** A rose dot becomes a Play button with "Press play / on everything." The button grows to fill the screen.
> 2. **2.75–4.47 s:** The screen folds into the app icon (black rounded square, ribbon N), then NEXORA and "Movies, series & anime. *One app.*"
> 3. **4.47–6.19 s:** "Opens on what's / worth watching." The hero card and Surprise me pop out of the home screen, with a "Today's pick" label.
> 4. **6.19–7.91 s:** "Movies. Series. / Anime." One tab per beat, with Hindi hits / South Indian / Action / Thriller labels.
> 5. **7.91–9.63 s:** "Top 10 / in India." The Top 10 row lifts out and the 1, 2 and 3 fly free.
> 6. **9.63–11.35 s:** "Hindi audio, / first." The audio picker pops out and Hindi is tapped, with "Remembers your pick".
> 7. **11.35–13.06 s:** "Up to / 1080p." The digits scramble-roll 480p → 720p → 1080p and the video area pops out, with an "HD · 1080p" label.
> 8. **13.06–14.78 s (the song's break):** "Make it / yours." The profile ring pops out and recolours on each beat through all five accents. The second headline line and the accent dots follow the colour.
> 9. **14.78–15.64 s (the drop):** A tilted 3D wall of 20 app screens with "ALL OF IT." and the line "HOME · MOVIES · SERIES · ANIME · TOP 10 · HINDI · 1080P".
> 10. **15.64–16.50 s:** "FREE." in rose on black, then "NO SIGN-UP." in black on white.
> 11. **16.50–18.22 s:** The app's exact launch splash (see Assets).
> 12. **18.22–20 s:** The splash moves up and the end card appears: "Movies, series & anime. *Free on Android.*", a rose "Download for Android" pill with a tap, and "FREE · NO SIGN-UP · 222 KB · ANDROID 7.0+".
>
> Do not mention servers or pop-ups.

## 5. Component showreel (latest)

> Study the best-rated videos and prompts on prompt-motion.com, then make a 20-second vertical (1080×1920, 60 fps) showreel for NEXORA, cut to the song from the reference video (139.6 BPM, a bar every 1.719 s from 1.03 s, with a break at 13.5–14.8 s and the drop at 14.78 s).
>
> Rules:
> - No raw screenshots: rebuild the app UI as live components so every part animates.
> - One continuous chain of morphs.
> - Light and dark scenes flip on the cut.
> - The text morphs.
> - The motion follows the music: drive the waveform and beat bumps from the song's real loudness and spectrum.
> - No HUD or corner labels.
> - Use the Nexora website's type system: Inter Tight, with one Instrument Serif italic word per line in a rose → violet gradient, each word revealed with a mask.
>
> Shots:
> 1. **0–1.03 s:** A search bar types "Something to watch tonight" with a rose caret.
> 2. **1.03–2.75 s:** The search bar morphs into a rose Play button (the magnifier turns into a triangle) under "Press *play*". A ripple on each beat, then a tap, and the button bursts into sparks.
> 3. **2.75–4.47 s:** Posters fly out of the burst into a rotating 3D ring, seen from slightly above, under "on *everything.*"
> 4. **4.47–6.19 s:** The ring collapses into the app's home rows (3×3) as a rose outline draws the phone around them and the phone shell fades in. The top bar, the typed row titles (Trending in India, Hindi hits, South Indian) and the tab bar appear. "Opens on what's *worth* watching."
> 5. **6.19–7.91 s:** Light mode (`#F2EDE7`): "Top 10 in *India.*" A giant outlined numeral slot-rolls 8 → 1 on every 8th note as posters slide in over it, ending on a "#1 IN INDIA" tag.
> 6. **7.91–9.63 s:** "Hindi audio, *first.*" The Hindi / English / Original picker. The underline slides from Original to Hindi with a tap, Hindi moves to the centre and grows, then morphs into "हिंदी" (Noto Sans Devanagari, gradient), over 40 mirrored waveform bars driven by the song's spectrum.
> 7. **9.63–11.35 s:** "One tap, it *plays.*" Verity's poster, title and meta, then the white Play pill is tapped and grows into the 16:9 video frame. A gradient badge below it rolls 480p → 720p → 1080p with scrambled digits.
> 8. **11.35–13.06 s:** "Never lose your *place.*" A typed "Continue watching" label, a landscape card whose progress bar fills to 64%, and Resume / + My List pills. My List is tapped and a gradient circle-wipe turns it into "✓ In My List" as the tick draws. Then a toast: "Saved on your phone. No account."
> 9. **13.06–14.78 s (the break):** "Make it *yours.*" A conic-gradient avatar ring recolours on each beat through the five accents. The headline and the background glow follow the colour, and the Titles / Hours / Day streak stats count up.
> 10. **14.78–15.64 s (the drop):** A flash, then about 130 small posters fly in from all around and tile the ribbon N. A brand-gradient colour blend washes over them, with "ALL OF IT." below.
> 11. **15.64–16.50 s:** "Free." morphs letter by letter into "No sign-up." with a rose full stop.
> 12. **16.50–18.22 s:** The app's exact launch splash (see Assets).
> 13. **18.22–20 s:** The splash moves up and the end card appears: "Press play on *everything.*", a white Download for Android pill that gets tapped, and "Free · No sign-up · 222 KB · Android 7.0+".
>
> Do not mention servers or pop-ups.
