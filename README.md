# Hamster Hour — meme explainer

Deliverables:

- `artifacts/video.mp4`: primary X feed export; 40 seconds, 1080 × 1080, 24 fps.
- `media/video-vertical.mp4`: separately composed 9:16 version; 40 seconds, 1080 × 1920, 24 fps.
- `media/sleeping.gif`: 3-second, 480 × 480, infinitely looping reply GIF.

Both MP4s use H.264, yuv420p, AAC audio and faststart. The square export is below the requested 15 MB. Exact measured sizes and stream information are in `validation.json`.

The video has no voiceover. Captions carry every explanation when muted. The soundtrack is an original synthesized 80 BPM chiptune/lo-fi loop, with original wheel squeaks, snores, UI clicks, signature stamps and a cash-register chime. No sampled music or third-party footage was used.

The visual design uses the project's public pixel-art hamster illustrations, near-black backgrounds, acid-green accents and IBM Plex Mono. A green cap is added to the recurring face character. Wheel, breathing, chart, countdown, signature and pool animations are rendered locally. Source illustrations came from:

- https://hamsterhour.fun/assets/hamster-wheel.svg
- https://hamsterhour.fun/assets/hamster-asleep.svg
- https://hamsterhour.fun/assets/hamster-happy.svg
- https://hamsterhour.fun/assets/hamster-thumbs.svg

The reference site is https://hamsterhour.fun. Facts follow the supplied brief. The only X link in the video is the end card's `https://x.com/hamsterhourgame`.

## Timing and captions

| Time | Beat |
| --- | --- |
| 0–4 | “this hamster is the whole protocol”; Squeektoshi, real hamster, livestream, wheel-pass sensor |
| 4–9 | Hourly window; OVER / UNDER the line |
| 9–14 | Sleeping half the day; SLEEPING means zero passes |
| 14–18 | EXACT: guess the number; closest three share the pool |
| 18–23 | $IMD bet UI and countdown; bets close when the hour starts |
| 23–30 | IMD oracle; AI agents check published wheel data and sign the result on Ethereum; no admin button |
| 30–35 | Pari-mutuel pool; 91% to winners, 9% to stakers, oracle reserve and team |
| 35–40 | hamsterhour.fun, X account, “bet on the hamster”, “Lose a bet. Earn $HAMSTER.” and “lose to earn / coming soon” |

## Rebuild offline

Run `python3 sources/render.py` from this directory. Requires Python 3.12 on Linux x86_64 and ffmpeg with libx264/AAC support. Pillow 10.4.0 is vendored as a wheel in `sources/deps/`; the script unpacks it under disposable `test/scratch/`, with no network or installation step. Font and raster artwork are included. IBM Plex Mono is under the included OFL license. Pillow's license is in its wheel. Do not delete `sources/deps/` before rebuilding.

The rebuild creates all three exports and temporary audio under `test/scratch/`. Use `python3 sources/render.py --stills` for eight square and eight portrait storyboard images in scratch.

## Limitations and checks

This is an animated explainer using stylized artwork, rather than a recording of the real hamster or livestream. The graph and EXACT guesses are illustrative; the bet interface is a clearly labeled recreation with a demo transaction. No wallet is connected and no bet is submitted. The three displayed robots illustrate a panel, not a claim about the oracle's panel size. The 9% remainder is shown collectively because no individual allocation percentages were supplied.

Validation includes actual encoded-frame contact sheets, full decode checks, stream/duration/dimension checks, GIF duration/loop inspection and audio peak/loudness measurement. These are local checks, not independent certification. See `validation.json` for measured results.
