# Nexora: all servers and their sub-servers

Tested on 4 Nov 2026 with the Android app's own server list (`p=a`, 37 servers for movies, 36 for series),
movie: *Drive – The Pretenders* (TMDB 1596275), audio Hindi. Each server's player was opened on its own and
its server/source menu was read (and its API answers, where the names come from there).

- **Sub-servers** = the player's own server/source menu inside that main server.
- "Single source" = the player has no server menu; it plays one stream.
- "Did not load here" = the page refused or failed in the test browser. It may still work in the app on a phone or TV.
- 🎬 = the stream was also caught and can play in the native (single) player. 🔒 = video hidden (blob/encrypted).

| # | Server ID | Site | Sub-servers (names) |
|---|---|---|---|
| 1 | x52b8b74b | vidly.pro | Did not load here |
| 2 | xcd3de789 | yapgrid.com 🎬 | **Vela** (same "embedwave" player as #3: Vela, Titan, Atlas, Lyra) · audio EN / ES / PT-BR |
| 3 | xbdb1db5b | embed.vidrift.in 🎬 | **Vela, Titan, Atlas, Lyra** (provider) · server "English FAST" |
| 4 | xccd29edc | rozgarlelo.modiplay.xyz 🎬 | **StreamHG, VidShared, Vidara, Bingr, Filemoon, EarnVids** · mirrors: Server Hindi, Server Original, Server English, Server Tamil, Server Telugu, Server Malayalam, Server Kannada, Server Arabic (all 1080p), Server Titan (H.264 Fast) |
| 5 | x925970d7 | vidbolt.pro 🎬 | **Orion, Vega, Quantum, Quasar** |
| 6 | x49d3d7a8 | play4u.org 🎬 | Single source · audio HIN 5.1 / ENG · up to 1080p |
| 7 | xeb640c7a | vidnest.fun | **Lamda, Zeta, Filxer, Ophim, Prime, Alfa, Beta, Sigma, Gama, Catflix, Hexa, Delta** (all "Original audio") |
| 8 | xdbc97590 | zxcstream.cc | Sources: **Orion I, Valstrax II, Atlas III, Ursa IV, Alatreon V, Daedalus VI** · dubs: Original, Arabic, English, French, Hindi, Kannada, Malayalam, Portuguese, Tamil, Telugu, Spanish (DASH) |
| 9 | xb2b92f63 | vidy.st | **Miami, Boise, Nashville, Chicago, Vegas, Reno, Oakland, Seattle, Phoenix, Atlanta, Portland, Austin, Dallas, Munich, Berlin, Paris, Delhi, Cancun** |
| 10 | xd2701c47 | nxsha.space 🎬 (tap to start) | **Nitro [Multi-Lang], Multi-bill [Multi-Lang], AwsPly [Multi-Lang], Citadel, Vixo, VidStpM, ShowNitro** (needs FebBox cookie)**, VidHindi, VidEmd, VidEmt, VidFk, VidMv, VidPro, VidBo** |
| 11 | x8dc33114 | cinemaos.tech (tap to start) | Did not load here (site error) |
| 12 | x73fac1ae | vidbolt.xyz 🎬 | **Orion, Vega, Quantum, Quasar** (same as #5) |
| 13 | x2a728bd8 | vidstuck.cc | **Orion, Andromeda, Atlas, Daedalus, Ursa** (each with Source 1 / Source 2) (DASH) |
| 14 | x355b7c4d | vidup.to | Did not load here |
| 15 | xf1fe2066 | vidfast.vc | Did not load here |
| 16 | xeeef6d62 | cinesrc.st | Sources: **Builtin, External** (plays the VidRock stream) · up to 2160p, many audio/subtitle languages |
| 17 | xcc1da2f1 | vidrock.to 🎬 | Single source · up to 4K (fMP4) |
| 18 | xc32ce9d6 | vidsrc.pm 🎬 | Single source |
| 19 | x919212a7 | vidcore.org | Single source ("Direct player"), no video in test |
| 20 | x3d678cf4 | embedmaster.link | Did not load here (it uses ChillFlix's list below) |
| 21 | xa86cf466 | chillflix.pw | **VAPlayer, Videasy, 7Movies, Athena, NovaHD, Movy, FileSuN, GaiaFlix, HollyMovieHD, Cine4K, Bingr, OnlyFlix, VidSrc.sh, 4K, MovieBox, NoTorrent, MoviesOnlineHD, Flixhqz, FshareTV, Huhu, vidapi.ru, CineSu, Cineplay, VSEmbed, FlixHQ, Vidmoly, VixSrc, UpCloud, VidNest, Peachify** (30) |
| 22 | x6915722b | player.cinezo.live | Did not load here (403) 🔒 |
| 23 | x850f0378 | player.vidzee.wtf 🎬 | **Peak, Dcloud, Acme, TCloud** · server language: Hindi / English |
| 24 | xacaf1ddf | vidking.ws 🔒 | "This media is unavailable" in test (same backend as #25, #33) |
| 25 | x9a59a593 | vidsrc.sh 🔒 | "This media is unavailable" in test |
| 26 | x87e10cc9 | vidsrc.su | Server menu present, **0 available** for this title |
| 27 | xf2890642 | play.xpass.top 🎬 | **TOK 1, TOK 2, VIP 1, LUL 1, MOL 1, VXR 1, VRK 1** |
| 28 | xd823344c | vidlink.pro | Single source · audio: Arabic, English, Spanish, French, Hindi, Indonesian, Malay, Portuguese, German · 1080p/720p/480p (DASH) |
| 29 | xe4c51f0c | viduki.net/2 | "Video Not Found" for this title |
| 30 | xfb9a92d1 | playapi.co 🎬 | **👑 Crown Hindi, 👑 Crown Tamil, 👑 Crown Malayalam, 🎵 Pulse, 🛡️ Titan, 🌟 Express, ✨ Swift, 💎 Ultra (2160p)** · behind them: 4KHDHub (HubCloud 2160p/1080p, Pixeldrain 1080p), CastleTV (Hindi/Tamil/Malayalam), NetMirror (Netflix), OneTouchTV (loklok), VaPlayer, Vidlink |
| 31 | x73a1bc15 | viduki.net/1 🎬 | **Leon, Jill, Ada, Claire, Sherry, Ethan, Chris, Wesker, Grace, Ashley** |
| 32 | x64a10a92 | vidcore.io (tap to start) | Did not load here |
| 33 | xdd43d5fc | vidsrc.io 🔒 | "This media is unavailable" in test |
| 34 | x360b8414 | vidsrc.to (tap to start) 🔒 | "upstream request failed" in test |
| 35 | x13e12bda | player.videasy.to | **Yoru** (4K), **Cypher, Breach, Neon, Vyse** (original audio), **Killjoy** (German), **Fade** (Hindi), **Omen** (Spanish), **Raze** (Portuguese) |
| 36 | xd4236ac1 | nxsha.screenscape.me (tap to start) | Did not load here |
| 37 | xdd4b9842 | 2embed.cc 🎬 | **2embed, Vsrc, Videm, Vcr** |

Anime / cartoon only (not in the list above, not tested here: they run through the app's own `/anime-player`):

| Server ID | Needs | Sites |
|---|---|---|
| x20f92f1b | TMDB images | Hindi cartoon sites (animesalt / watchanimeworld) |
| xc38f0578 | TMDB images | Hindi cartoon sites (animesalt / watchanimeworld) |
| x0da97b82 | AniList id | Anime sites |
| xec046b18 | AniList id | Anime sites |

## Totals

- Main servers: **37** for movies (36 for series), **41** with the anime/cartoon ones.
- Main servers with named sub-servers: **18** (#2, 3, 4, 5, 7, 8, 9, 10, 12, 13, 16, 21, 23, 27, 30, 31, 35, 37).
- Single-source players (no server menu): #6, 17, 18, 19, 28.
- Sub-server names found: **about 160**. Biggest lists: ChillFlix 30, vidy.st 18, nxsha.space 14, modiplay 15 (6 hosts + 9 mirrors), vidnest 12, playapi 8 (+ 6 backends).
- Main servers that did not load or had no video for this title in the test: **#1, 11, 14, 15, 19, 20, 22, 24, 25, 26, 29, 32, 33, 34, 36**.
