---
title: "Speech"
description: "Use when the user asks for text-to-speech narration or voiceover, accessibility reads, audio prompts, or batch speech generation via the OpenAI Audio API; run the bundled CLI (`scripts/text_to_speech.py`) with built-in voices and require `OPENAI_A..."
category: "writing"
source: "community"
author: "Community"
tags: ["speech"]
date: 2026-03-20
---

# Speech Generation Skill

Generate spoken audio for the current project (narration, product demo voiceover, IVR prompts, accessibility reads). Defaults to `gpt-4o-mini-tts-2025-12-15` and built-in voices, and prefers the bundled CLI for deterministic, reproducible runs.

## When to use
- Generate a single spoken clip from text
- Generate a batch of prompts (many lines, many files)

## Decision tree (single vs batch)
- If the user provides multiple lines/prompts or wants many outputs -> **batch**
- Else -> **single**

## Workflow
1. Decide intent: single vs batch (see decision tree above).
2. Collect inputs up front: exact text (verbatim), desired voice, delivery style, format, and any constraints.
3. If batch: write a temporary JSONL under tmp/ (one job per line), run once, then delete the JSONL.
4. Augment instructions into a short labeled spec without rewriting the input text.
5. Run the bundled CLI (`scripts/text_to_speech.py`) with sensible defaults (see references/cli.md).
6. For important clips, validate: intelligibility, pacing, pronunciation, and adherence to constraints.
7. Iterate with a single targeted change (voice, speed, or instructions), then re-check.
8. Save/return final outputs and note the final text + instructions + flags used.

## Temp and output conventions
- Use `tmp/speech/` for intermediate files (for example JSONL batches); delete when done.
- Write final artifacts under `output/speech/` when working in this repo.
- Use `--out` or `--out-dir` to control output paths; keep filenames stable and descriptive.

## Dependencies (install if missing)
Prefer `uv` for dependency management.

Python packages:
```
uv pip install openai
```
If `uv` is unavailable:
```
python3 -m pip install openai
```

## Environment
- `OPENAI_API_KEY` must be set for live API calls.

If the key is missing, give the user these steps:
1. Create an API key in the OpenAI platform UI: https://platform.openai.com/api-keys
2. Set `OPENAI_API_KEY` as an environment variable in their system.
3. Offer to guide them through setting the environment variable for their OS/shell if needed.
- Never ask the user to paste the full key in chat. Ask them to set it locally and confirm when ready.

If installation isn't possible in this environment, tell the user which dependency is missing and how to install it locally.

## Defaults & rules
- Use `gpt-4o-mini-tts-2025-12-15` unless the user requests another model.
- Default voice: `cedar`. If the user wants a brighter tone, prefer `marin`.
- Built-in voices only. Custom voices are out of scope for this skill.
- `instructions` are supported for GPT-4o mini TTS models, but not for `tts-1` or `tts-1-hd`.
- Input length must be <= 4096 characters per request. Split longer text into chunks.
- Enforce 50 requests/minute. The CLI caps `--rpm` at 50.
- Require `OPENAI_API_KEY` before any live API call.
- Provide a clear disclosure to end users that the voice is AI-generated.
- Use the OpenAI Python SDK (`openai` package) for all API calls; do not use raw HTTP.
- Prefer the bundled CLI (`scripts/text_to_speech.py`) over writing new one-off scripts.
- Never modify `scripts/text_to_speech.py`. If something is missing, ask the user before doing anything else.

## Instruction augmentation
Reformat user direction into a short, labeled spec. Only make implicit details explicit; do not invent new requirements.

Quick clarification (augmentation vs invention):
- If the user says "narration for a demo", you may add implied delivery constraints (clear, steady pacing, friendly tone).
- Do not introduce a new persona, accent, or emotional style the user did not request.

Template (include only relevant lines):
```
Voice Affect: <overall character and texture of the voice>
Tone: <attitude, formality, warmth>
Pacing: <slow, steady, brisk>
Emotion: <key emotions to convey>
Pronunciation: <words to enunciate or emphasize>
Pauses: <where to add intentional pauses>
Emphasis: <key words or phrases to stress>
Delivery: <cadence or rhythm notes>
```

Augmentation rules:
- Keep it short; add only details the user already implied or provided elsewhere.
- Do not rewrite the input text.
- If any critical detail is missing and blocks success, ask a question; otherwise proceed.

## Examples

### Single example (narration)
```
Input text: "Welcome to the demo. Today we'll show how it works."
Instructions:
Voice Affect: Warm and composed.
Tone: Friendly and confident.
Pacing: Steady and moderate.
Emphasis: Stress "demo" and "show".
```

### Batch example (IVR prompts)
```
{"input":"Thank you for calling. Please hold.","voice":"cedar","response_format":"mp3","out":"hold.mp3"}
{"input":"For sales, press 1. For support, press 2.","voice":"marin","instructions":"Tone: Clear and neutral. Pacing: Slow.","response_format":"wav"}
```

## Instructioning best practices (short list)
- Structure directions as: affect -> tone -> pacing -> emotion -> pronunciation/pauses -> emphasis.
- Keep 4 to 8 short lines; avoid conflicting guidance.
- For names/acronyms, add pronunciation hints (e.g., "enunciate A-I") or supply a phonetic spelling in the text.
- For edits/iterations, repeat invariants (e.g., "keep pacing steady") to reduce drift.
- Iterate with single-change follow-ups.

More principles: `references/prompting.md`. Copy/paste specs: `references/sample-prompts.md`.

## Guidance by use case
Use these modules when the request is for a specific delivery style. They provide targeted defaults and templates.
- Narration / explainer: `references/narration.md`
- Product demo / voiceover: `references/voiceover.md`
- IVR / phone prompts: `references/ivr.md`
- Accessibility reads: `references/accessibility.md`

## CLI + environment notes
- CLI commands + examples: `references/cli.md`
- API parameter quick reference: `references/audio-api.md`
- Instruction patterns + examples: `references/voice-directions.md`
- If network approvals / sandbox settings are getting in the way: `references/codex-network.md`

## Reference map
- **`references/cli.md`**: how to run speech generation/batches via `scripts/text_to_speech.py` (commands, flags, recipes).
- **`references/audio-api.md`**: API parameters, limits, voice list.
- **`references/voice-directions.md`**: instruction patterns and examples.
- **`references/prompting.md`**: instruction best practices (structure, constraints, iteration patterns).
- **`references/sample-prompts.md`**: copy/paste instruction recipes (examples only; no extra theory).
- **`references/narration.md`**: templates + defaults for narration and explainers.
- **`references/voiceover.md`**: templates + defaults for product demo voiceovers.
- **`references/ivr.md`**: templates + defaults for IVR/phone prompts.
- **`references/accessibility.md`**: templates + defaults for accessibility reads.
- **`references/codex-network.md`**: environment/sandbox/network-approval troubleshooting.

---

## Reference: Accessibility

# Accessibility read defaults

## Suggested defaults
- Voice: `cedar`
- Format: `mp3` or `wav`
- Speed: `0.95` to `1.0`

## Guidance
- Keep delivery steady and neutral.
- Enunciate acronyms and numbers.
- Avoid dramatic or stylized delivery.

## Instruction template
```
Voice Affect: Neutral and clear.
Tone: Informational and steady.
Pacing: Slow and consistent.
Pronunciation: Enunciate acronyms and numbers.
Emphasis: Stress key warnings or labels.
```

## Example (short)
Input text:
"Warning: High voltage. Keep hands clear."

Instructions:
```
Voice Affect: Neutral and clear.
Tone: Informational and steady.
Pacing: Slow and consistent.
Emphasis: Stress "Warning" and "High voltage".
```

---

## Reference: Audio Api

# Audio Speech API quick reference

## Endpoint
- Create speech: `POST /v1/audio/speech`

## Default model
- `gpt-4o-mini-tts-2025-12-15`

## Other speech models (if requested)
- `gpt-4o-mini-tts`
- `tts-1`
- `tts-1-hd`

## Core parameters
- `model`: speech model
- `input`: text to synthesize (max 4096 characters)
- `voice`: built-in voice name
- `instructions`: optional style directions (not supported for `tts-1` or `tts-1-hd`)
- `response_format`: `mp3`, `opus`, `aac`, `flac`, `wav`, or `pcm`
- `speed`: 0.25 to 4.0

## Built-in voices
- `alloy`, `ash`, `ballad`, `cedar`, `coral`, `echo`, `fable`, `marin`, `nova`, `onyx`, `sage`, `shimmer`, `verse`

## Output notes
- Default format is `mp3`.
- `pcm` is raw 24 kHz 16-bit little-endian samples (no header).
- `wav` includes a header (better for quick playback).

## Compliance note
- Provide a clear disclosure that the voice is AI-generated.

---

## Reference: Cli

# CLI reference (`scripts/text_to_speech.py`)

This file contains the "command catalog" for the bundled speech generation CLI. Keep `SKILL.md` as overview-first; put verbose CLI details here.

## What this CLI does
- `speak`: generate a single audio file
- `speak-batch`: run many jobs from a JSONL file (one job per line)
- `list-voices`: list supported voices

Real API calls require network access + `OPENAI_API_KEY`. `--dry-run` does not.

## Quick start (works from any repo)
Set a stable path to the skill CLI (default `CODEX_HOME` is `~/.codex`):

```
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export TTS_GEN="$CODEX_HOME/skills/speech/scripts/text_to_speech.py"
```

Dry-run (no API call; no network required; does not require the `openai` package):

```
python "$TTS_GEN" speak --input "Test" --dry-run
```

Generate (requires `OPENAI_API_KEY` + network):

```
uv run --with openai python "$TTS_GEN" speak \
  --input "Today is a wonderful day to build something people love!" \
  --voice cedar \
  --instructions "Voice Affect: Warm and composed. Tone: upbeat and encouraging." \
  --response-format mp3 \
  --out speech.mp3
```

No `uv` installed? Use your active Python env:

```
python "$TTS_GEN" speak --input "Hello" --voice cedar --out speech.mp3
```

## Guardrails (important)
- Use `python "$TTS_GEN" ...` (or equivalent full path) for all TTS work.
- Do **not** create one-off runners (e.g., `gen_audio.py`) unless the user explicitly asks.
- **Never modify** `scripts/text_to_speech.py`. If something is missing, ask the user before doing anything else.

## Defaults (unless overridden by flags)
- Model: `gpt-4o-mini-tts-2025-12-15`
- Voice: `cedar`
- Response format: `mp3`
- Speed: `1.0`
- Batch rpm cap: `50`

## Input limits
- Input text must be <= 4096 characters per request.
- For longer text, split into smaller chunks (manual or via batch JSONL).

## Instructions compatibility
- `instructions` are supported for GPT-4o mini TTS models.
- `tts-1` and `tts-1-hd` ignore instructions (the CLI will warn and drop them).

## Common recipes

List voices:
```
python "$TTS_GEN" list-voices
```

Generate with explicit pacing:
```
python "$TTS_GEN" speak \
  --input "Welcome to the demo. We'll show how it works." \
  --instructions "Tone: friendly and confident. Pacing: steady and moderate." \
  --out demo.mp3
```

Batch generation (JSONL):
```
mkdir -p tmp/speech
cat > tmp/speech/jobs.jsonl << 'JSONL'
{"input":"Thank you for calling. Please hold.","voice":"cedar","response_format":"mp3","out":"hold.mp3"}
{"input":"For sales, press 1. For support, press 2.","voice":"marin","instructions":"Tone: clear and neutral. Pacing: slow.","response_format":"wav"}
JSONL

python "$TTS_GEN" speak-batch --input tmp/speech/jobs.jsonl --out-dir out --rpm 50

# Cleanup (recommended)
rm -f tmp/speech/jobs.jsonl
```

Notes:
- Use `--rpm` to control rate limiting (default `50`, max `50`).
- Per-job overrides are supported in JSONL (`model`, `voice`, `response_format`, `speed`, `instructions`, `out`).
- Treat the JSONL file as temporary: write it under `tmp/` and delete it after the run (do not commit it).

## See also
- API parameter quick reference: `references/audio-api.md`
- Instruction patterns and examples: `references/voice-directions.md`

---

## Reference: Codex Network

# Codex network approvals / sandbox notes

This guidance is intentionally isolated from `SKILL.md` because it can vary by environment and may become stale. Prefer the defaults in your environment when in doubt.

## Why am I asked to approve every speech generation call?
Speech generation uses the OpenAI Audio API, so the CLI needs outbound network access. In many Codex setups, network access is disabled by default (especially under stricter sandbox modes), and/or the approval policy may require confirmation before networked commands run.

## How do I reduce repeated approval prompts (network)?
If you trust the repo and want fewer prompts, enable network access for the relevant sandbox mode and relax the approval policy.

Example `~/.codex/config.toml` pattern:

```
approval_policy = "never"
sandbox_mode = "workspace-write"

[sandbox_workspace_write]
network_access = true
```

Or for a single session:

```
codex --sandbox workspace-write --ask-for-approval never
```

## Safety note
Use caution: enabling network and disabling approvals reduces friction but increases risk if you run untrusted code or work in an untrusted repository.

---

## Reference: Ivr

# IVR / phone prompt defaults

## Suggested defaults
- Voice: `cedar` (clear) or `marin` (brighter)
- Format: `wav`
- Speed: `0.9` to `1.0`

## Guidance
- Prioritize clarity and slower pacing.
- Enunciate numbers and menu options.
- Keep sentences short and consistent.

## Instruction template
```
Voice Affect: Clear and neutral.
Tone: Professional and concise.
Pacing: Slow and even.
Pronunciation: Enunciate numbers and menu options.
Emphasis: Stress the option numbers.
```

## Example (short)
Input text:
"For sales, press 1. For support, press 2."

Instructions:
```
Voice Affect: Clear and neutral.
Tone: Professional and concise.
Pacing: Slow and even.
Emphasis: Stress "press 1" and "press 2".
```

---

## Reference: Narration

# Narration / explainer defaults

## Suggested defaults
- Voice: `cedar`
- Format: `mp3`
- Speed: `1.0`

## Guidance
- Keep pacing steady and clear.
- Emphasize section headings and key transitions.
- If the script is long, chunk it into logical paragraphs.

## Instruction template
```
Voice Affect: Warm and composed.
Tone: Friendly and confident.
Pacing: Steady and moderate.
Emphasis: Stress section titles and key terms.
Pauses: Brief pause after each section.
```

## Example (short)
Input text:
"Welcome to the demo. Today we'll show how it works."

Instructions:
```
Voice Affect: Warm and composed.
Tone: Friendly and confident.
Pacing: Steady and moderate.
```

---

## Reference: Prompting

# Instructioning best practices (TTS)

## Contents
- Structure
- Specificity
- Avoiding conflicts
- Pronunciation and names
- Pauses and pacing
- Iterate deliberately
- Where to find copy/paste recipes

## Structure
- Use a consistent order: affect -> tone -> pacing -> emotion -> pronunciation/pauses -> emphasis -> delivery.
- For complex requests, use short labeled lines instead of a long paragraph.

## Specificity
- Name the delivery you want ("calm and steady" vs "friendly").
- If you need a specific cadence, call it out explicitly ("slow and measured", "brisk and energetic").

## Avoiding conflicts
- Do not mix opposing instructions ("fast and slow", "formal and casual").
- Keep instructions short: 4 to 8 lines are usually enough.

## Pronunciation and names
- For acronyms, write the pronunciation hint in text ("A-I" instead of "AI").
- For names or brands, add a simple phonetic guide in the input text if clarity matters.
- If a word must be emphasized, add an Emphasis line and repeat the word exactly.

## Pauses and pacing
- Use punctuation or short line breaks in the input text to create natural pauses.
- Use the Pauses line for intentional pauses ("pause after the greeting").

## Iterate deliberately
- Start with a clean base instruction set, then make one change at a time.
- Repeat critical constraints on each iteration ("keep pacing steady").

## Where to find copy/paste recipes
For copy/paste instruction templates, see `references/sample-prompts.md`. This file focuses on principles, structure, and iteration patterns.

---

## Reference: Sample Prompts

# Sample instruction templates (copy/paste)

These are short instruction blocks. Use only the lines you need and keep them consistent with the input text.

## Friendly product demo
```
Voice Affect: Warm and composed.
Tone: Friendly and confident.
Pacing: Steady and moderate.
Emphasis: Stress key product benefits.
```

## Calm support update
```
Voice Affect: Calm and reassuring.
Tone: Sincere and empathetic.
Pacing: Slow and steady.
Emotion: Warmth and care.
Pauses: Brief pause after apologies.
```

## IVR menu
```
Voice Affect: Clear and neutral.
Tone: Professional and concise.
Pacing: Slow and even.
Emphasis: Stress menu options and numbers.
```

## Accessibility readout
```
Voice Affect: Neutral and clear.
Tone: Informational and steady.
Pacing: Slow and consistent.
Pronunciation: Enunciate acronyms and numbers.
```

## Energetic intro
```
Voice Affect: Bright and upbeat.
Tone: Enthusiastic and welcoming.
Pacing: Brisk but clear.
Emphasis: Stress the opening greeting.
```

---

## Reference: Voice Directions

# Voice directions

## Template
Use only the lines you need. Keep directions concise and aligned to the input text.

```
Voice Affect: <overall character and texture>
Tone: <attitude, formality, warmth>
Pacing: <slow, steady, brisk>
Emotion: <key emotions to convey>
Pronunciation: <words to enunciate or emphasize>
Pauses: <where to insert brief pauses>
Emphasis: <key phrases to stress>
Delivery: <cadence or rhythm notes>
```

## Best practices
- Keep 4 to 8 short lines. Avoid conflicting instructions.
- Prefer concrete guidance over adjectives alone.
- Do not rewrite the input text in the instructions; only guide delivery.
- If you need a language or accent, write the input text in that language.
- Repeat critical constraints (for example: "slow and steady") when iterating.

## Examples (short)

### Calm support
```
Voice Affect: Calm and composed, reassuring.
Tone: Sincere and empathetic.
Pacing: Steady and moderate.
Emotion: Warmth and genuine care.
Pronunciation: Clear, with emphasis on key reassurances.
Pauses: Brief pauses after apologies and before requests.
```

### Dramatic narrator
```
Voice Affect: Low and suspenseful.
Tone: Serious and mysterious.
Pacing: Slow and deliberate.
Emotion: Restrained intensity.
Emphasis: Highlight sensory details and cliffhanger lines.
Pauses: Add pauses after suspenseful moments.
```

### Fitness instructor
```
Voice Affect: High energy and upbeat.
Tone: Motivational and encouraging.
Pacing: Fast and dynamic.
Emotion: Enthusiasm and momentum.
Emphasis: Stress action verbs and countdowns.
```

### Serene guide
```
Voice Affect: Soft and soothing.
Tone: Calm and reassuring.
Pacing: Slow and unhurried.
Emotion: Peaceful warmth.
Pauses: Gentle pauses after breathing cues.
```

### Robot agent
```
Voice Affect: Monotone and mechanical.
Tone: Neutral and formal.
Pacing: Even and controlled.
Emotion: None; strictly informational.
Pronunciation: Precise and consistent.
```

### Old-time announcer
```
Voice Affect: Refined and theatrical.
Tone: Formal and welcoming.
Pacing: Steady with a classic cadence.
Emotion: Warm enthusiasm.
Pronunciation: Crisp enunciation with vintage flair.
```

---

## Reference: Voiceover

# Product demo / voiceover defaults

## Suggested defaults
- Voice: `cedar` (neutral) or `marin` (brighter)
- Format: `wav` for video sync, `mp3` for quick review
- Speed: `1.0`

## Guidance
- Keep tone confident and helpful.
- Emphasize product benefits and call-to-action phrases.
- Avoid overly dramatic delivery unless requested.

## Instruction template
```
Voice Affect: Confident and composed.
Tone: Helpful and upbeat.
Pacing: Steady, slightly brisk.
Emphasis: Stress product benefits and the call to action.
```

## Example (short)
Input text:
"Meet the new dashboard. Find insights faster and act with confidence."

Instructions:
```
Voice Affect: Confident and composed.
Tone: Helpful and upbeat.
Pacing: Steady, slightly brisk.
Emphasis: Stress "insights" and "confidence".
```
