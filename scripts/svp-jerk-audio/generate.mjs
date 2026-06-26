#!/usr/bin/env node
// Generate "The SVP" two-voice audio (in the style of The Jerk) from lines.json.
//
// Pipeline:
//   1. For each spoken line, call ElevenLabs TTS with the line's voice + emotion tag.
//   2. Normalize every clip to a uniform WAV format, inserting silence per `pauseAfter`.
//   3. Concatenate all clips into one continuous dialogue track.
//   4. (Optional) Duck a user-supplied music bed under the dialogue and mix.
//
// Requirements: Node 18+ (built-in fetch) and `ffmpeg` on PATH.
// Auth: set ELEVENLABS_API_KEY in the environment.
//
// Usage:
//   ELEVENLABS_API_KEY=sk_... node generate.mjs --out the-svp.mp3
//   ELEVENLABS_API_KEY=sk_... node generate.mjs --music ./tonight.mp3 --out the-svp.mp3
//
// Flags:
//   --out <file>        Output file (default: the-svp.mp3)
//   --music <file>      Backing track to duck under the dialogue (you supply this)
//   --music-volume <n>  Music bed gain, 0..1 (default: 0.30)
//   --navin-voice <id>  ElevenLabs voice ID for Navin (or env NAVIN_VOICE_ID)
//   --darla-voice <id>  ElevenLabs voice ID for Darla (or env DARLA_VOICE_ID)
//   --model <id>        ElevenLabs model (default: eleven_v3)
//   --keep-temp         Keep the intermediate clips for inspection

import { spawn } from "node:child_process";
import { mkdtemp, mkdir, readFile, writeFile, rm } from "node:fs/promises";
import { existsSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));

// --- Defaults ---------------------------------------------------------------
// ElevenLabs "default" library voices. Override with flags/env for a better cast:
// Navin should read earnest + energetic; Darla flat + dry. The contrast is the joke.
const DEFAULTS = {
  navinVoice: "TxGEqnHWrfWFTfGW9XjX", // Josh — earnest young male
  darlaVoice: "EXAVITQu4vr4xnSDxMaL", // Sarah — calm, even female
  model: "eleven_v3",
  out: "the-svp.mp3",
  musicVolume: 0.3,
};

// Uniform intermediate audio format so concat never re-encodes mismatched clips.
const SR = "44100";
const CH = "2";

function parseArgs(argv) {
  const opts = {
    out: DEFAULTS.out,
    music: null,
    musicVolume: DEFAULTS.musicVolume,
    navinVoice: process.env.NAVIN_VOICE_ID || DEFAULTS.navinVoice,
    darlaVoice: process.env.DARLA_VOICE_ID || DEFAULTS.darlaVoice,
    model: process.env.ELEVENLABS_MODEL || DEFAULTS.model,
    keepTemp: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    const next = () => argv[++i];
    if (a === "--out") opts.out = next();
    else if (a === "--music") opts.music = next();
    else if (a === "--music-volume") opts.musicVolume = Number(next());
    else if (a === "--navin-voice") opts.navinVoice = next();
    else if (a === "--darla-voice") opts.darlaVoice = next();
    else if (a === "--model") opts.model = next();
    else if (a === "--keep-temp") opts.keepTemp = true;
    else if (a === "--help" || a === "-h") opts.help = true;
    else throw new Error(`Unknown flag: ${a}`);
  }
  return opts;
}

function run(cmd, args) {
  return new Promise((resolve, reject) => {
    const child = spawn(cmd, args, { stdio: ["ignore", "pipe", "pipe"] });
    let stderr = "";
    child.stderr.on("data", (d) => (stderr += d));
    child.on("error", (err) =>
      reject(new Error(`Failed to start ${cmd}: ${err.message}`)),
    );
    child.on("close", (code) => {
      if (code === 0) resolve();
      else reject(new Error(`${cmd} exited ${code}:\n${stderr.slice(-2000)}`));
    });
  });
}

async function haveFfmpeg() {
  try {
    await run("ffmpeg", ["-version"]);
    return true;
  } catch {
    return false;
  }
}

async function tts({ text, emotion, voiceId, model, apiKey, outFile }) {
  // ElevenLabs v3 reads bracketed cues as delivery direction; harmless on v2.
  const directed = emotion ? `[${emotion}] ${text}` : text;
  const url = `https://api.elevenlabs.io/v1/text-to-speech/${voiceId}?output_format=mp3_44100_128`;
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "xi-api-key": apiKey,
      "content-type": "application/json",
      accept: "audio/mpeg",
    },
    body: JSON.stringify({
      text: directed,
      model_id: model,
      voice_settings: { stability: 0.4, similarity_boost: 0.8 },
    }),
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => "");
    throw new Error(
      `ElevenLabs TTS failed (${res.status}) for "${text.slice(0, 40)}...": ${detail.slice(0, 300)}`,
    );
  }
  const buf = Buffer.from(await res.arrayBuffer());
  await writeFile(outFile, buf);
}

// Re-encode an mp3 clip to uniform WAV, appending `pauseAfter` seconds of silence.
async function toClipWav(mp3In, wavOut, pauseAfter) {
  const pad = Math.max(0, pauseAfter || 0);
  await run("ffmpeg", [
    "-y",
    "-i", mp3In,
    "-af", `apad=pad_dur=${pad}`,
    "-ar", SR, "-ac", CH,
    wavOut,
  ]);
}

// A pure-silence WAV clip (used for the SFX/door beat — no speech).
async function silenceWav(wavOut, seconds) {
  await run("ffmpeg", [
    "-y",
    "-f", "lavfi",
    "-i", `anullsrc=r=${SR}:cl=stereo`,
    "-t", String(Math.max(0.1, seconds)),
    "-ar", SR, "-ac", CH,
    wavOut,
  ]);
}

async function main() {
  const opts = parseArgs(process.argv.slice(2));
  if (opts.help) {
    console.log(
      "Generate 'The SVP' audio. See header of generate.mjs for flags.\n" +
        "  ELEVENLABS_API_KEY=sk_... node generate.mjs --music ./bed.mp3 --out the-svp.mp3",
    );
    return;
  }

  const apiKey = process.env.ELEVENLABS_API_KEY;
  if (!apiKey) {
    console.error("Error: set ELEVENLABS_API_KEY in the environment.");
    process.exit(1);
  }
  if (!(await haveFfmpeg())) {
    console.error("Error: ffmpeg not found on PATH. Install it and retry.");
    process.exit(1);
  }
  if (opts.music && !existsSync(opts.music)) {
    console.error(`Error: --music file not found: ${opts.music}`);
    process.exit(1);
  }

  const data = JSON.parse(await readFile(path.join(HERE, "lines.json"), "utf8"));
  const tmp = await mkdtemp(path.join(tmpdir(), "svp-jerk-"));
  const clipsDir = path.join(tmp, "clips");
  await mkdir(clipsDir, { recursive: true });

  console.log(`Rendering ${data.lines.length} lines…`);
  const clipWavs = [];
  for (let i = 0; i < data.lines.length; i++) {
    const line = data.lines[i];
    const idx = String(i).padStart(2, "0");
    const wav = path.join(clipsDir, `clip-${idx}.wav`);

    if (line.speaker === "SFX" || !line.text) {
      console.log(`  [${idx}] (silence ${line.pauseAfter}s)`);
      await silenceWav(wav, line.pauseAfter);
    } else {
      const voiceId =
        line.speaker === "DARLA" ? opts.darlaVoice : opts.navinVoice;
      console.log(`  [${idx}] ${line.speaker}: ${line.text.slice(0, 50)}…`);
      const mp3 = path.join(clipsDir, `clip-${idx}.mp3`);
      await tts({
        text: line.text,
        emotion: line.emotion,
        voiceId,
        model: opts.model,
        apiKey,
        outFile: mp3,
      });
      await toClipWav(mp3, wav, line.pauseAfter);
    }
    clipWavs.push(wav);
  }

  // Concatenate dialogue via the concat demuxer (all clips share format).
  const listFile = path.join(tmp, "concat.txt");
  await writeFile(
    listFile,
    clipWavs.map((w) => `file '${w.replace(/'/g, "'\\''")}'`).join("\n"),
  );
  const dialogueWav = path.join(tmp, "dialogue.wav");
  await run("ffmpeg", [
    "-y",
    "-f", "concat", "-safe", "0",
    "-i", listFile,
    "-ar", SR, "-ac", CH,
    dialogueWav,
  ]);

  const outAbs = path.resolve(opts.out);
  if (!opts.music) {
    console.log("Encoding dialogue-only output…");
    await run("ffmpeg", ["-y", "-i", dialogueWav, "-b:a", "192k", outAbs]);
  } else {
    console.log(`Mixing music bed (ducked) from ${opts.music}…`);
    const vol = Number.isFinite(opts.musicVolume) ? opts.musicVolume : 0.3;
    // Loop the music to cover the dialogue, set bed gain, sidechain-compress it
    // keyed by the voice so it dips under speech, then mix and loudness-normalize.
    const filter =
      `[1:a]volume=${vol}[bed];` +
      `[bed][0:a]sidechaincompress=threshold=0.05:ratio=6:attack=15:release=350[duck];` +
      `[duck][0:a]amix=inputs=2:duration=first:normalize=0[mixed];` +
      `[mixed]loudnorm=I=-16:TP=-1.5:LRA=11[out]`;
    await run("ffmpeg", [
      "-y",
      "-i", dialogueWav,
      "-stream_loop", "-1", "-i", opts.music,
      "-filter_complex", filter,
      "-map", "[out]",
      "-b:a", "192k",
      outAbs,
    ]);
  }

  if (!opts.keepTemp) {
    await rm(tmp, { recursive: true, force: true });
  } else {
    console.log(`Intermediate clips kept in: ${tmp}`);
  }
  console.log(`\nDone → ${outAbs}`);
}

main().catch((err) => {
  console.error(`\n${err.message}`);
  process.exit(1);
});
