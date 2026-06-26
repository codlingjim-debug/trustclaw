# The SVP — audio generator

Generates a full two-voice audio reading of **"The SVP — A Departure in the
Style of _The Jerk_"** and (optionally) mixes it over a music bed you supply,
ducked under the dialogue.

This is a standalone utility — it is **not** part of the Next.js app or its
build. It only needs Node 18+ and `ffmpeg`.

## What it does

1. Reads the script from [`lines.json`](./lines.json).
2. Sends each spoken line to **ElevenLabs** TTS with the line's voice and its
   bracketed emotion cue (`[deadpan]`, `[triumphant]`, …).
3. Stitches every clip into one continuous dialogue track, inserting the
   per-line pauses (including the closing "Tesla door / silence" beat).
4. If you pass `--music`, loops your backing track, **ducks** it under the
   speech with `ffmpeg`'s `sidechaincompress`, mixes, and loudness-normalizes.

## The music ("Jerk" theme)

The film's signature tune is _"Tonight You Belong to Me."_ That recording is
copyrighted, so **this script does not ship any music** — you provide the file
via `--music`. Use something you own or a royalty-free ukulele/old-timey track
for the same feel.

## Prerequisites

- **Node 18+** (uses built-in `fetch`).
- **ffmpeg** on your `PATH` — `ffmpeg -version` should work.
- An **ElevenLabs API key**.

## Usage

```bash
cd scripts/svp-jerk-audio

# Dialogue only:
ELEVENLABS_API_KEY=sk_xxx node generate.mjs --out the-svp.mp3

# With a ducked music bed you supply:
ELEVENLABS_API_KEY=sk_xxx node generate.mjs \
  --music ./tonight-you-belong-to-me.mp3 \
  --out the-svp.mp3
```

### Flags

| Flag                  | Default        | Description                                              |
| --------------------- | -------------- | -------------------------------------------------------- |
| `--out <file>`        | `the-svp.mp3`  | Output file.                                             |
| `--music <file>`      | _(none)_       | Backing track to duck under the dialogue.                |
| `--music-volume <n>`  | `0.30`         | Music bed gain, `0`–`1`.                                 |
| `--navin-voice <id>`  | a default male | ElevenLabs voice ID for Navin (energetic/earnest).       |
| `--darla-voice <id>`  | a default fem. | ElevenLabs voice ID for Darla (flat/dry).                |
| `--model <id>`        | `eleven_v3`    | ElevenLabs model. `eleven_v3` honors the emotion cues.   |
| `--keep-temp`         | off            | Keep intermediate clips for inspection.                  |

Voice IDs can also be set via `NAVIN_VOICE_ID` / `DARLA_VOICE_ID` env vars.
Browse and copy IDs from your ElevenLabs **Voices** library — casting Navin
earnest/energetic and Darla flat/dry is what makes the bit land.

## Editing the script

Edit `lines.json`. Each entry:

```json
{
  "speaker": "NAVIN",        // NAVIN | DARLA | SFX
  "emotion": "triumphant",   // passed through as a [bracketed] cue
  "text": "And this piece of wire!",
  "pauseAfter": 0.5          // seconds of silence after the line
}
```

`SFX` lines (or any line with empty `text`) render as pure silence of
`pauseAfter` seconds — used here for the closing car-door beat.
