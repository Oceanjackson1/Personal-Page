---
title: "Sora"
description: "Use when the user asks to generate, edit, extend, poll, list, download, or delete Sora videos, create reusable non-human Sora character references, or run local multi-video queues via the bundled CLI (`scripts/sora.py`); includes requests like: (i..."
category: "other"
source: "community"
author: "Community"
tags: ["sora"]
date: 2026-03-20
---

# Sora Video Generation Skill

Creates or manages Sora video jobs for the current project (product demos, marketing spots, cinematic shots, social clips, UI mocks). Defaults to `sora-2` with structured prompt augmentation and prefers the bundled CLI for deterministic runs. Note: `$sora` is a skill tag in prompts, not a shell command.

## When to use
- Generate a new video clip from a prompt
- Create a reusable character reference from a short non-human source clip
- Edit an existing generated video with a targeted prompt change
- Extend a completed video with a continuation prompt
- Poll status, list jobs, or download assets (video/thumbnail/spritesheet)
- Run a local multi-job queue now, or plan a true Batch API submission for offline rendering

## Decision tree
- If the user has a short non-human reference clip they want to reuse across shots → `create-character`
- If the user has a completed video and wants the next beat/continuation → `extend`
- If the user has a completed video and wants a targeted change while preserving the shot → `edit`
- If the user has a video id and wants status or assets → `status`, `poll`, or `download`
- If the user needs many renders immediately inside Codex → `create-batch` (local fan-out, not the Batch API)
- If the user needs many renders for offline processing or a studio pipeline → use the official Batch API flow described in `references/video-api.md`
- Otherwise → `create` (or `create-and-poll` if they need a ready asset in one step)

## Workflow
1. Decide intent: create vs create-character vs edit vs extend vs status/download vs local queue vs official Batch API.
2. Collect inputs: prompt, model, size, seconds, any image reference, and any character IDs.
3. Prefer CLI augmentation flags (`--use-case`, `--scene`, `--camera`, etc.) instead of hand-writing a long structured prompt. If you already have a structured prompt file, pass `--no-augment`.
4. Run the bundled CLI (`scripts/sora.py`) with sensible defaults. For long prompts, prefer `--prompt-file` to avoid shell-escaping issues.
5. For async jobs, poll until terminal status (or use `create-and-poll`).
6. Download assets (video/thumbnail/spritesheet) and save them locally before URLs expire.
7. If the user wants continuity across many shots, create character assets first, then reference them in later `create` calls.
8. If the user wants to iterate on a completed shot, prefer `edit`; if they want the shot to continue in time, prefer `extend`.
9. Use one targeted change per iteration.

## Authentication
- `OPENAI_API_KEY` must be set for live API calls.

If the key is missing, give the user these steps:
1. Create an API key in the OpenAI platform UI: https://platform.openai.com/api-keys
2. Set `OPENAI_API_KEY` as an environment variable in their system.
3. Offer to guide them through setting the environment variable for their OS/shell if needed.
- Never ask the user to paste the full key in chat. Ask them to set it locally and confirm when ready.

## Defaults & rules
- Default model: `sora-2` (use `sora-2-pro` for higher fidelity).
- Default size: `1280x720`.
- Default seconds: `4` (allowed: `"4"`, `"8"`, `"12"`, `"16"`, `"20"`).
- Always set size and seconds via API params; prose will not change them.
- `sora-2-pro` is required for `1920x1080` and `1080x1920`.
- Use up to two characters per generation.
- Use the OpenAI Python SDK (`openai` package). If high-level SDK helpers lag the latest Sora guide, use low-level `client.post/get/delete` inside the official SDK rather than standalone HTTP code.
- Require `OPENAI_API_KEY` before any live API call.
- If uv cache permissions fail, set `UV_CACHE_DIR=/tmp/uv-cache`.
- Input reference images must be jpg/png/webp and should match target size.
- JSON `input_reference` objects use either `file_id` or `image_url`; uploaded file paths use multipart.
- Download URLs expire after about 1 hour; copy assets to your own storage.
- Batch-generated videos remain downloadable for up to 24 hours after the batch completes.
- `create-batch` in `scripts/sora.py` is a local concurrent queue, not the official Batch API.
- Prefer the bundled CLI and **never modify** `scripts/sora.py` unless the user asks.
- Sora can generate audio; if a user requests voiceover/audio, specify it explicitly in the `Audio:` and `Dialogue:` lines and keep it short.

## API limitations
- Models are limited to `sora-2` and `sora-2-pro`.
- API access to Sora models requires an organization-verified account.
- Duration must be set via the `seconds` parameter and currently supports `4`, `8`, `12`, `16`, and `20`.
- Character uploads currently work best with short `2`-`4` second non-human MP4s in `16:9` or `9:16`, at `720p`-`1080p`.
- Extensions can add up to `20` seconds each, up to six times per source video, for a maximum total length of `120` seconds.
- Extensions currently do not support characters or image references.
- This skill supports editing existing generated videos by ID.
- The official Batch API currently supports `POST /v1/videos` only, with JSON bodies rather than multipart uploads.
- Output sizes are limited by model (see `references/video-api.md` for the supported sizes).
- Video creation is async; you must poll for completion before downloading.
- Rate limits apply by usage tier (do not list specific limits).
- Content restrictions are enforced by the API (see Guardrails below).

## Guardrails (must enforce)
- Only content suitable for audiences under 18.
- No copyrighted characters or copyrighted music.
- No real people (including public figures).
- Input images with human faces are rejected.
- Character uploads in this skill are for non-human subjects only.

## Prompt augmentation
Reformat prompts into a structured, production-oriented spec. Only make implicit details explicit; do not invent new creative requirements.

Template (include only relevant lines):
```
Use case: <where the clip will be used>
Primary request: <user's main prompt>
Scene/background: <location, time of day, atmosphere>
Subject: <main subject>
Action: <single clear action>
Camera: <shot type, angle, motion>
Lighting/mood: <lighting + mood>
Color palette: <3-5 color anchors>
Style/format: <film/animation/format cues>
Timing/beats: <counts or beats>
Audio: <ambient cue / music / voiceover if requested>
Text (verbatim): "<exact text>"
Dialogue:
<dialogue>
- Speaker: "Short line."
</dialogue>
Constraints: <must keep/must avoid>
Avoid: <negative constraints>
```

Augmentation rules:
- Keep it short; add only details the user already implied or provided elsewhere.
- For edits, explicitly list invariants ("same shot, change only X").
- For character-based shots, mention the character name verbatim in the prompt.
- If any critical detail is missing and blocks success, ask a question; otherwise proceed.
- If you pass a structured prompt file to the CLI, add `--no-augment` to avoid the tool re-wrapping it.

## Examples

### Generation example (single shot)
```
Use case: product teaser
Primary request: a close-up of a matte black camera on a pedestal
Action: slow 30-degree orbit over 4 seconds
Camera: 85mm, shallow depth of field, gentle handheld drift
Lighting/mood: soft key light, subtle rim, premium studio feel
Constraints: no logos, no text
```

### Edit example (invariants)
```
Primary request: same shot and framing, switch palette to teal/sand/rust with warmer backlight
Constraints: keep the subject and camera move unchanged
```

### Character consistency example
```
Primary request: Mossy, a moss-covered teapot mascot, hurries through a lantern-lit market at dusk
Camera: cinematic tracking shot, 35mm, shoulder height
Lighting/mood: warm dusk practicals, soft haze
Constraints: keep Mossy’s silhouette and moss texture consistent across the shot
```

## Prompting best practices (short list)
- One main action + one camera move per shot.
- Use counts or beats for timing ("two steps, pause, turn").
- Keep text short and the camera locked-off for UI or on-screen text.
- Add a brief avoid line when artifacts appear (flicker, jitter, fast motion).
- Shorter prompts are more creative; longer prompts are more controlled.
- Put dialogue in a dedicated block; keep lines short for 4-8s clips.
- Mention character names verbatim when using uploaded character IDs.
- State invariants explicitly for edits (same shot, same camera move).
- Prefer `edit` for targeted changes and `extend` for timeline continuation.
- Iterate with single-change follow-ups to preserve continuity.

## Guidance by asset type
Use these modules when the request is for a specific artifact. They provide targeted templates and defaults.
- Cinematic shots: `references/cinematic-shots.md`
- Social ads: `references/social-ads.md`

## CLI + environment notes
- CLI commands + examples: `references/cli.md`
- API parameter quick reference: `references/video-api.md`
- Prompting guidance: `references/prompting.md`
- Sample prompts: `references/sample-prompts.md`
- Troubleshooting: `references/troubleshooting.md`
- Network/sandbox tips: `references/codex-network.md`

## Reference map
- **`references/cli.md`**: how to run create/edit/extend/create-character/poll/download/local-queue flows via `scripts/sora.py`.
- **`references/video-api.md`**: API-level knobs (models, sizes, duration, characters, edits, extensions, official Batch API).
- **`references/prompting.md`**: prompt structure, character continuity, editing, and extension guidance.
- **`references/sample-prompts.md`**: copy/paste prompt recipes (examples only; no extra theory).
- **`references/cinematic-shots.md`**: templates for filmic shots.
- **`references/social-ads.md`**: templates for short social ad beats.
- **`references/troubleshooting.md`**: common errors and fixes.
- **`references/codex-network.md`**: network/approval troubleshooting.

---

## Reference: Cinematic Shots

# Cinematic shot templates

Use these for filmic, mood-forward clips. Keep one subject, one action, one camera move.

## Shot grammar (pick one)
- Static wide: locked-off, slow atmosphere changes
- Dolly-in: slow push toward subject
- Dolly-out: reveal more context
- Orbit: 15-45 degree arc around subject
- Lateral move: smooth left-right slide
- Crane: subtle vertical rise
- Handheld drift: gentle, controlled sway

## Default template
```
Use case: cinematic shot
Primary request: <subject + setting>
Scene/background: <location, time of day, atmosphere>
Subject: <main subject>
Action: <one clear action>
Camera: <shot type, lens, motion>
Lighting/mood: <key light + mood>
Color palette: <3-5 anchors>
Style/format: filmic, natural grain
Constraints: no logos, no text, no people
Avoid: jitter; flicker; oversharpening
```

## Example: moody exterior
```
Use case: cinematic shot
Primary request: a lone cabin on a cliff above the sea
Scene/background: foggy coastline at dawn, drifting mist
Subject: small wooden cabin with warm window glow
Action: light fog rolls past the cabin
Camera: slow dolly-in, 35mm, steady
Lighting/mood: moody, soft dawn light, subtle contrast
Color palette: deep blue, slate, warm amber
Constraints: no logos, no text, no people
```

## Example: intimate detail
```
Use case: cinematic detail
Primary request: close-up of a vinyl record spinning
Scene/background: dim room, soft lamp glow
Subject: record grooves and stylus
Action: slow rotation, subtle dust motes
Camera: macro, locked-off
Lighting/mood: warm, low-key, soft highlights
Color palette: warm amber, deep brown, charcoal
Constraints: no logos, no text
```

---

## Reference: Cli

# CLI reference (`scripts/sora.py`)

This file contains the command catalog for the bundled Sora CLI. Keep `SKILL.md` overview-first; put verbose CLI details here.

## What this CLI does
- `create`: create a new video job
- `create-and-poll`: create a job, poll until complete, optionally download
- `create-character`: upload a reusable non-human character reference clip
- `edit`: edit an existing generated video by ID
- `extend`: continue a completed video
- `poll`: wait for an existing job to finish
- `status`: retrieve job status/details
- `download`: download video/thumbnail/spritesheet
- `list`: list recent jobs
- `delete`: delete a job
- `remix`: legacy remix endpoint
- `create-batch`: create multiple video jobs locally from JSONL input

Real API calls require network access and `OPENAI_API_KEY`. `--dry-run` does not.

## Important distinction
- `create-batch` is a local concurrent fan-out helper.
- It is not the official Batch API.
- For the official Batch API, prepare a JSONL file for `POST /v1/videos`, upload it with `purpose=batch`, then create a batch via the Files and Batches APIs.

## Quick start
Set a stable path to the skill CLI (default `CODEX_HOME` is `~/.codex`):

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export SORA_CLI="$CODEX_HOME/skills/sora/scripts/sora.py"
```

If you're in this repo, set the path directly:

```bash
export SORA_CLI="$(git rev-parse --show-toplevel)/<path-to-skill>/scripts/sora.py"
```

If uv cache fails with permission errors:

```bash
export UV_CACHE_DIR="/tmp/uv-cache"
```

Dry-run without calling the API:

```bash
python "$SORA_CLI" create --prompt "Test" --dry-run
```

## Defaults
- Model: `sora-2`
- Size: `1280x720`
- Seconds: `4`
- Variant: `video`
- Poll interval: `10` seconds

Allowed seconds: `4`, `8`, `12`, `16`, `20`

Allowed sizes:
- `sora-2`: `1280x720`, `720x1280`
- `sora-2-pro`: `1280x720`, `720x1280`, `1024x1792`, `1792x1024`, `1920x1080`, `1080x1920`

## Create
Create a job:

```bash
uv run --with openai python "$SORA_CLI" create \
  --model sora-2 \
  --prompt "Wide tracking shot of a teal coupe on a desert highway" \
  --size 1280x720 \
  --seconds 8
```

Create with a file-based first-frame reference:

```bash
uv run --with openai python "$SORA_CLI" create \
  --model sora-2-pro \
  --prompt "She turns around and smiles, then slowly walks out of frame." \
  --size 1280x720 \
  --seconds 8 \
  --input-reference sample_720p.jpeg
```

Create with a stored/remote JSON reference object:

```bash
uv run --with openai python "$SORA_CLI" create \
  --prompt "Slow reveal of a mossy mascot in a lantern-lit market" \
  --input-reference-file-id file_abc123
```

Create with characters:

```bash
uv run --with openai python "$SORA_CLI" create \
  --model sora-2 \
  --prompt "Mossy, a moss-covered teapot mascot, rushes through a lantern-lit market at dusk." \
  --character-id char_123 \
  --seconds 8
```

If the prompt is already structured, disable augmentation:

```bash
uv run --with openai python "$SORA_CLI" create \
  --prompt-file prompt.txt \
  --no-augment \
  --seconds 16
```

## Create and poll

```bash
uv run --with openai python "$SORA_CLI" create-and-poll \
  --model sora-2-pro \
  --prompt "Close-up of a steaming coffee cup on a wooden table" \
  --size 1920x1080 \
  --seconds 16 \
  --download \
  --variant video \
  --out coffee.mp4
```

## Create a character

```bash
uv run --with openai python "$SORA_CLI" create-character \
  --name Mossy \
  --video-file character.mp4
```

Use short non-human MP4 source clips and mention the character name verbatim in later prompts.

## Edit
Edit an existing generated video by ID:

```bash
uv run --with openai python "$SORA_CLI" edit \
  --id video_abc123 \
  --prompt "Same shot and camera move; shift the palette to teal, sand, and rust."
```

## Extend

```bash
uv run --with openai python "$SORA_CLI" extend \
  --id video_abc123 \
  --seconds 8 \
  --prompt "Continue the scene as the camera rises above the rooftops and reveals sunrise."
```

## Poll / status / download

```bash
uv run --with openai python "$SORA_CLI" poll --id video_abc123 --download --out out.mp4
uv run --with openai python "$SORA_CLI" status --id video_abc123
uv run --with openai python "$SORA_CLI" download --id video_abc123 --variant thumbnail --out thumb.webp
uv run --with openai python "$SORA_CLI" download --id video_abc123 --variant spritesheet --out sheet.jpg
```

## List / delete

```bash
uv run --with openai python "$SORA_CLI" list --limit 20 --after video_123 --order asc
uv run --with openai python "$SORA_CLI" delete --id video_abc123
```

## Legacy remix

```bash
uv run --with openai python "$SORA_CLI" remix \
  --id video_abc123 \
  --prompt "Same shot and framing; change only the palette to teal and sand."
```

Use `edit` for new workflows. `remix` is retained only for legacy compatibility.

## JSON output (`--json-out`)
- `create`, `status`, `list`, `delete`, `poll`, `remix`, `edit`, `extend`, and `create-character` write the response to a file.
- `create-and-poll` writes `{ "create": ..., "final": ... }`.
- In `--dry-run`, `--json-out` writes the request preview.
- If the path has no extension, `.json` is added automatically.

## Local batch JSONL schema (`create-batch`)
Each line is a JSON object (or a raw prompt string). Required key: `prompt`.

Common top-level keys:
- `model`, `size`, `seconds`
- `characters`: list like `[{"id":"char_123"}]` or `["char_123"]`
- `character_ids`: alternate list form such as `["char_123"]`
- `input_reference`: either a file path string or a JSON object with `file_id` or `image_url`
- `input_reference_path` / `input_reference_file`: file path aliases
- `input_reference_file_id`
- `input_reference_url`
- `out`: optional output filename for the job JSON

Prompt augmentation keys:
- `use_case`, `scene`, `subject`, `action`, `camera`, `style`, `lighting`, `palette`, `audio`, `dialogue`, `text`, `timing`, `constraints`, `negative`

Example:

```bash
mkdir -p tmp/sora
cat > tmp/sora/prompts.jsonl << 'EOB'
{"prompt":"A neon-lit rainy alley, slow dolly-in","seconds":"8"}
{"prompt":"Mossy, a moss-covered teapot mascot, jogs through a lantern-lit alley","seconds":"16","character_ids":["char_123"]}
{"prompt":"A warm sunrise over a misty lake, gentle pan","input_reference":{"file_id":"file_abc123"}}
EOB

uv run --with openai python "$SORA_CLI" create-batch \
  --input tmp/sora/prompts.jsonl \
  --out-dir out \
  --concurrency 3
```

Notes:
- `create-batch` writes one JSON response per job under `--out-dir`.
- Output names default to `NNN-<prompt-slug>.json`.
- Higher concurrency can hit rate limits.
- Treat the JSONL file as temporary and clean it up after use.

## Guardrails
- Use `python "$SORA_CLI" ...` or `uv run --with openai python "$SORA_CLI" ...`.
- For live API calls, prefer `uv run --with openai ...`.
- Do not create one-off runners unless the user explicitly asks.
- `edit` replaces `remix` for new integrations.

## See also
- API parameter quick reference: `references/video-api.md`
- Prompt structure and iteration: `references/prompting.md`
- Sample prompts: `references/sample-prompts.md`
- Troubleshooting: `references/troubleshooting.md`

---

## Reference: Codex Network

# Codex network approvals / sandbox notes

This guidance is intentionally isolated from `SKILL.md` because it can vary by environment and may become stale. Prefer the defaults in your environment when in doubt.

## Why am I asked to approve every video generation call?
Video generation uses the OpenAI Video API, so the CLI needs outbound network access. In many Codex setups, network access is disabled by default (especially under stricter sandbox modes), and/or the approval policy may require confirmation before networked commands run.

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

## Reference: Prompting

# Prompting best practices (Sora)

## Contents
- [Mindset & tradeoffs](#mindset--tradeoffs)
- [API-controlled params](#api-controlled-params)
- [Structure](#structure)
- [Specificity](#specificity)
- [Style & visual cues](#style--visual-cues)
- [Camera & composition](#camera--composition)
- [Motion & timing](#motion--timing)
- [Lighting & palette](#lighting--palette)
- [Character continuity](#character-continuity)
- [Multi-shot prompts](#multi-shot-prompts)
- [Ultra-detailed briefs](#ultra-detailed-briefs)
- [Image input](#image-input)
- [Constraints & invariants](#constraints--invariants)
- [Text, dialogue & audio](#text-dialogue--audio)
- [Avoiding artifacts](#avoiding-artifacts)
- [Editing & extensions](#editing--extensions)
- [Iterate deliberately](#iterate-deliberately)

## Mindset & tradeoffs
- Treat the prompt like a cinematography brief, not a contract.
- The same prompt can yield different results; rerun for variants.
- Short prompts give more creative freedom; longer prompts give more control.
- Shorter clips tend to follow instructions better; even though `16`s and `20`s are available, start shorter when precision matters.

## API-controlled params
- Model, size, seconds, and character IDs are controlled by API params, not prose.
- Put desired duration in the `seconds` param; the prompt cannot make a clip longer.
- `1920x1080` and `1080x1920` require `sora-2-pro`.

## Structure
- Use short labeled lines; omit sections that do not matter.
- Keep one main subject and one main action.
- Put timing in beats or counts if it matters.
- If you prefer a prose-first template, use:
```
<Prose scene description in plain language. Describe subject, setting, time of day, and key visual details.>

Cinematography:
Camera shot: <framing + angle>
Mood: <tone>

Actions:
- <clear action beat>
- <clear action beat>

Dialogue:
<short lines if needed>
```

## Specificity
- Name the subject and materials (metal, fabric, glass).
- Use camera language (lens, angle, shot type) for stability.
- Describe the environment with time of day and atmosphere.

## Style & visual cues
- Set style early (e.g., "1970s film", "IMAX-scale", "16mm black-and-white").
- Use visible nouns and verbs, not vague adjectives.
- Weak: "A beautiful street at night."
- Strong: "Wet asphalt, zebra crosswalk, neon signs reflecting in puddles."

## Camera & composition
- Prefer one camera move: dolly, orbit, lateral slide, or locked-off.
- Straight-on framing is best for UI and text.
- For close-ups, use longer lenses (85mm+); for wide scenes, 24-35mm.
- Depth of field is a strong lever: shallow for subject isolation, deep for context.
- Example framings: wide establishing, medium close-up, aerial wide, low angle.
- Example camera motions: slow tilt, gentle handheld drift, smooth lateral slide.

## Motion & timing
- Use short beats: "0-2s", "2-4s", "4-6s".
- Keep actions sequential, not simultaneous.
- For 4s clips, limit to 1-2 beats.
- Describe actions as counts or steps when possible (e.g., "takes four steps, pauses, turns in the final second").

## Lighting & palette
- Describe light quality and direction (soft window light, hard rim, backlight).
- Name 3-5 palette anchors to stabilize color across shots.
- If continuity matters, keep lighting logic consistent across clips.

## Character continuity
- Keep character descriptors consistent across shots; reuse phrasing.
- Avoid mixing competing traits that can shift identity or pose.
- When using uploaded character assets, mention the character name verbatim in the prompt.
- Use no more than two characters per generation.
- Character uploads work best from short non-human MP4 reference clips.

## Multi-shot prompts
- You can describe multiple shots in one prompt, but keep each shot block distinct.
- For each shot, specify one camera setup, one action, one lighting recipe.
- Treat each shot as a creative unit you can later edit or stitch.

## Ultra-detailed briefs
- Use when you need a specific, filmic look or strict continuity.
- Call out format/look, lensing/filters, grade/palette, lighting direction, texture, and sound.
- If needed, include a short shot list with timing beats.

## Image input
- Use an input image to lock composition, character design, or set dressing.
- The input image should match the target size and be jpg/png/webp.
- The image anchors the first frame; the prompt describes what happens next.
- If you lack a reference, generate one first and pass it as `input_reference`.

## Constraints & invariants
- State what must not change: "same shot", "same framing", "keep background".
- Repeat invariants in every edit to reduce drift.
- Use invariants sparingly in extensions; tell the model what should continue, not just what should stay frozen.

## Text, dialogue & audio
- Keep text short and specific; quote exact strings.
- Specify placement and avoid motion blur.
- For dialogue, use a dedicated block and keep lines short.
- Label speakers consistently for multi-character scenes.
- If silent, you can still add a small ambient sound cue to set rhythm.
- Sora can generate audio; include an `Audio:` line and a short dialogue block when needed.
- As a rule of thumb, 4s clips fit 1-2 short lines; 8s clips can handle a few more.

Example:
```
Audio: soft ambient café noise, clear warm voiceover
Dialogue:
<dialogue>
- Speaker: "Let's get started."
</dialogue>
```

## Avoiding artifacts
- Avoid multiple actions in 4-8 seconds.
- Keep camera motion smooth and limited.
- Add explicit negatives when needed: "avoid flicker", "avoid jitter", "no fast motion".

## Editing & extensions
- Prefer edits when the shot is mostly right and you want one targeted change.
- Prefer extensions when the existing clip should continue forward in time.
- For edits, change one thing at a time: palette, lighting, or action.
- For extensions, describe the next beat clearly and preserve motion continuity.
- If a shot misfires, simplify: freeze the camera, reduce action, clear background, then add complexity back in.

## Iterate deliberately
- Start simple, then add one constraint per iteration.
- If results look chaotic, reduce motion and simplify the scene.
- When a result is close, pin it as a reference and describe only the tweak.

---

## Reference: Sample Prompts

# Sample prompts (copy/paste)

Use these as starting points. Keep user-provided requirements and constraints; do not invent new creative elements.

For prompting principles (structure, invariants, iteration), see `references/prompting.md`.

## Contents
- [Product teaser (single shot)](#product-teaser-single-shot)
- [UI demo (screen recording style)](#ui-demo-screen-recording-style)
- [Cinematic detail shot](#cinematic-detail-shot)
- [Social ad (6s with beats)](#social-ad-6s-with-beats)
- [Character continuity shot](#character-continuity-shot)
- [Edit follow-up](#edit-follow-up)
- [Extension follow-up](#extension-follow-up)
- [Motion graphics explainer](#motion-graphics-explainer)
- [Ambient loop (atmosphere)](#ambient-loop-atmosphere)

## Product teaser (single shot)
```
Use case: product teaser
Primary request: close-up of a matte black wireless speaker on a stone pedestal
Scene/background: dark studio cyclorama, subtle haze
Subject: compact speaker with soft fabric texture
Action: slow 20-degree orbit over 4 seconds
Camera: 85mm, shallow depth of field, steady dolly
Lighting/mood: soft key, gentle rim, premium studio feel
Color palette: charcoal, slate, warm amber accents
Constraints: no logos, no text
Avoid: harsh bloom; oversharpening; clutter
```

## UI demo (screen recording style)
```
Use case: UI product demo
Primary request: a clean mobile budgeting app demo showing a weekly spend chart
Scene/background: neutral gradient backdrop
Subject: smartphone UI, centered, screen content crisp and legible
Action: tap the "Add expense" button, modal opens, amount typed, save
Camera: locked-off, straight-on, no tilt
Lighting/mood: soft studio light, minimal reflections
Color palette: off-white, slate, mint accent
Text (verbatim): "Add expense", "$24.50", "Groceries"
Constraints: no brand logos; keep UI text readable; avoid motion blur
```

## Cinematic detail shot
```
Use case: cinematic product detail
Primary request: macro shot of raindrops sliding across a car hood
Scene/background: night city bokeh, soft rain mist
Subject: glossy hood surface with water beads
Action: slow push-in over 4 seconds
Camera: 100mm macro, shallow depth of field
Lighting/mood: moody, high-contrast reflections, soft speculars
Color palette: deep navy, teal, silver highlights
Constraints: no logos, no text
Avoid: flicker; unstable reflections; excessive noise
```

## Social ad (6s with beats)
```
Use case: social ad
Primary request: minimal coffee subscription ad with three quick beats
Scene/background: warm kitchen counter, morning light
Subject: ceramic mug, coffee bag, steam
Action: beat 1 (0-2s) pour coffee; beat 2 (2-4s) steam rises; beat 3 (4-6s) mug slides to center
Camera: 50mm, gentle handheld drift
Lighting/mood: warm, cozy, natural light
Text (verbatim): "Fresh roast" (top-left), "Weekly delivery" (bottom-right)
Constraints: no logos; text must be legible; avoid fast motion
```

## Character continuity shot
```
Use case: mascot continuity
Primary request: Mossy, a moss-covered teapot mascot, rushes through a lantern-lit market at dusk
Scene/background: narrow alley, hanging lanterns, light haze
Subject: Mossy the moss-covered teapot mascot
Action: quick jog through the alley, glances toward camera near the end
Camera: 35mm, shoulder-height tracking shot, smooth lateral move
Lighting/mood: warm dusk practicals, cinematic glow
Color palette: moss green, warm amber, charcoal
Constraints: keep Mossy's silhouette, moss texture, and teapot proportions consistent
Avoid: flicker; warped limbs; identity drift
```

## Edit follow-up
```
Primary request: same shot and camera move; change only the palette to teal, sand, and rust with a warmer backlight
Constraints: keep the subject, framing, and motion unchanged
Avoid: new objects; reframing; speed changes
```

## Extension follow-up
```
Primary request: continue the same shot as the camera rises above the rooftops and reveals sunrise over the city
Action: maintain the existing motion, then gently tilt upward into the skyline reveal
Lighting/mood: dawn light growing warmer through the extension
Constraints: preserve scene continuity, camera direction, and overall pacing
Avoid: abrupt cuts; jumpy motion; sudden subject changes
```

## Motion graphics explainer
```
Use case: explainer clip
Primary request: clean motion-graphics animation showing data flowing into a dashboard
Scene/background: soft gradient background
Subject: abstract nodes and lines, simple dashboard cards
Action: nodes connect, data pulses, cards fill with charts
Camera: locked-off, no depth, flat design
Lighting/mood: minimal, modern
Color palette: off-white, graphite, teal, coral accents
Constraints: no logos; keep shapes simple; avoid heavy texture
```

## Ambient loop (atmosphere)
```
Use case: ambient background loop
Primary request: fog drifting through a pine forest at dawn
Scene/background: tall pines, soft fog layers, distant hills
Subject: drifting fog and light rays
Action: slow lateral drift, subtle light change
Camera: wide, locked-off, no tilt
Lighting/mood: calm, soft dawn light
Color palette: muted greens, cool gray, pale gold
Constraints: no text, no logos, no people
Avoid: fast motion; flicker; abrupt lighting shifts
```

---

## Reference: Social Ads

# Social ad templates (4-8s)

Short clips work best with clear beats. Use 2-3 beats and keep text minimal.

## Default template
```
Use case: social ad
Primary request: <ad concept>
Scene/background: <simple backdrop>
Subject: <product or scene>
Action: beat 1 (0-2s) <action>; beat 2 (2-4s) <action>; beat 3 (4-6s) <action>
Camera: <shot type + motion>
Lighting/mood: <mood>
Text (verbatim): "<short headline>", "<short subhead>"
Constraints: no logos; keep text legible; avoid fast motion
```

## Example: product benefit
```
Use case: social ad
Primary request: a compact humidifier emphasizing quiet operation
Scene/background: minimal bedroom nightstand
Subject: matte white humidifier with soft vapor
Action: beat 1 (0-2s) vapor begins; beat 2 (2-4s) soft glow turns on; beat 3 (4-6s) device slides to center
Camera: 50mm, gentle push-in
Lighting/mood: calm, warm night light
Text (verbatim): "Quiet mist", "Sleep better"
Constraints: no logos; text must be legible; avoid harsh highlights
```

## Example: before/after
```
Use case: social ad
Primary request: before/after of a cluttered desk becoming tidy
Scene/background: home office desk, neutral wall
Subject: desk surface, organizer tray
Action: beat 1 (0-2s) cluttered desk; beat 2 (2-4s) quick tidy motion; beat 3 (4-6s) clean desk with organizer
Camera: top-down, locked-off
Lighting/mood: soft daylight
Text (verbatim): "Before", "After"
Constraints: no logos; keep motion minimal; avoid blur
```

---

## Reference: Troubleshooting

# Troubleshooting

## Job fails with size or seconds errors
- Cause: size is not supported by the chosen model, or seconds is outside `4`, `8`, `12`, `16`, `20`.
- Fix: match size to model; use `sora-2-pro` for `1920x1080` or `1080x1920`.

## Docs and SDK disagree on the latest limits or helpers
- Cause: the March 2026 Sora guide/changelog is ahead of some typed SDK/API-reference surfaces.
- Fix: follow the latest guide/changelog and use the bundled CLI, which bridges new flows through the official client’s low-level methods.

## `edit`, `extend`, or `create-character` isn't available in your installed Python SDK
- Cause: the published SDK may not expose new Sora helpers yet.
- Fix: use `scripts/sora.py`; it uses the official OpenAI client directly for those endpoints.

## openai SDK not installed
- Cause: running `python "$SORA_CLI" ...` without the OpenAI SDK available.
- Fix: run with `uv run --with openai python "$SORA_CLI" ...`.

## uv cache permission error
- Cause: uv cache directory is not writable in CI or sandboxed environments.
- Fix: set `UV_CACHE_DIR=/tmp/uv-cache` (or another writable path) before running `uv`.

## Prompt shell escaping issues
- Cause: multi-line prompts or quotes break the shell.
- Fix: use `--prompt-file prompt.txt`.

## Prompt looks double-wrapped ("Primary request: Use case: ...")
- Cause: you structured the prompt manually but left CLI augmentation on.
- Fix: add `--no-augment`, or use the CLI fields (`--use-case`, `--scene`, etc.) instead of pre-formatting.

## Input reference rejected
- Cause: the file is not jpg/png/webp, includes a human face, or does not match the target size.
- Fix: convert to jpg/png/webp, remove faces, and resize to match `--size`.

## Character continuity is weak
- Cause: the character clip is too long, mismatched in aspect ratio, outside the skill's non-human character workflow, or the prompt never names the character.
- Fix: use a short non-human MP4, match aspect ratio to the target shot, and mention the character name verbatim in the prompt.

## Extension looks jumpy or drifts
- Cause: the continuation prompt changes too many things at once, or asks for a hard scene break.
- Fix: describe the next beat only, preserve motion direction, and avoid introducing unrelated subjects or abrupt camera changes.

## Remix drifts from the original
- Cause: remix is a legacy endpoint and too many changes were requested at once.
- Fix: prefer `edit`, state invariants explicitly, and change one element at a time.

## Download fails or returns expired URL
- Cause: normal download URLs expire after about 1 hour.
- Fix: re-download while the link is fresh and copy the asset to your own storage promptly.

## Video completes but looks unstable or flickers
- Cause: multiple actions, aggressive camera motion, or overly long prompt timing for the clip length.
- Fix: reduce to one main action and one camera move; keep beats simple; add constraints like `avoid flicker` or `stable motion`.

## Text is unreadable
- Cause: text is too long, too small, or moving.
- Fix: shorten text, keep the camera locked-off, and avoid fast motion.

## Job stuck in `queued` or `in_progress`
- Cause: temporary queue delays or slower higher-resolution renders.
- Fix: increase timeout, poll less aggressively, and expect longer waits for `16`/`20` second or 1080p jobs.

## `create-batch` is not behaving like the Batch API
- Cause: `create-batch` is a local concurrent helper, not the official Batch API.
- Fix: use the Files + Batches APIs for true offline batching; use `create-batch` only for immediate local fan-out.

## Cleanup blocked by sandbox policy
- Cause: some environments block `rm`.
- Fix: skip cleanup, or truncate temporary files instead of deleting them.

---

## Reference: Video Api

# Sora Video API quick reference

Keep this file short; the full source of truth is the latest OpenAI Sora guide plus the API changelog.

## Source-of-truth note
- The March 2026 changelog and Sora guide added characters, 16s/20s clips, `1920x1080` / `1080x1920` on `sora-2-pro`, extensions, and edits.
- Some typed SDK and API-reference pages may still show the older `4`/`8`/`12` and pre-1080p enums.
- If they disagree, follow the latest guide/changelog and use the bundled CLI, which bridges the SDK lag with low-level official-client calls.

## Models
- `sora-2`: faster, flexible iteration
- `sora-2-pro`: higher fidelity, slower, more expensive

## Sizes (by model)
- `sora-2`: `1280x720`, `720x1280`
- `sora-2-pro`: `1280x720`, `720x1280`, `1024x1792`, `1792x1024`, `1920x1080`, `1080x1920`
- Use `sora-2-pro` for 1080p exports.

## Duration
- `seconds`: `"4"`, `"8"`, `"12"`, `"16"`, `"20"`
- Use shorter clips first when iterating on motion, timing, or composition.

## Input references
- `input_reference` guides the first frame of a generation.
- Multipart requests use an uploaded image file.
- JSON requests use an object with exactly one of `file_id` or `image_url`.
- Supported image formats: jpg/jpeg, png, webp.
- Input references should match the target `size`.

## Characters
- Create reusable non-human characters via `POST /v1/videos/characters`.
- Character source clips work best as short MP4s (`2`-`4`s) in `16:9` or `9:16`, at `720p`-`1080p`.
- Reference up to two characters per generation with `characters: [{"id": "..."}]`.
- Mention the character name verbatim in the prompt; the ID alone is not enough.
- Characters can be combined with `input_reference`.
- In this skill, character workflows are limited to non-human subjects.

## Edits vs remix
- Preferred: `POST /v1/videos/edits`
- Legacy/deprecated: `POST /v1/videos/{video_id}/remix`
- Use edits for new integrations.
- In this skill, use edits for existing generated video IDs only.

## Extensions
- Use `POST /v1/videos/extensions` to continue a completed video.
- Each extension can add up to `20` seconds.
- A single video can be extended up to six times, for a maximum total length of `120` seconds.
- Extensions do not support characters or image references.

## Jobs and status
- Creation, edit, and extension jobs are async.
- Common statuses: `queued`, `in_progress`, `completed`, `failed`
- Poll every `10`-`20`s or use webhooks.
- Webhook events: `video.completed`, `video.failed`

## Core endpoints
- `POST /videos`: create
- `POST /videos/characters`: create a reusable character
- `POST /videos/edits`: edit an existing generated video by ID
- `POST /videos/extensions`: extend a completed video
- `GET /videos/{id}`: retrieve status/details
- `GET /videos/{id}/content`: download content
- `GET /videos`: list
- `DELETE /videos/{id}`: delete
- `POST /videos/{id}/remix`: legacy/deprecated

## Download variants
- `video` -> mp4
- `thumbnail` -> webp
- `spritesheet` -> jpg

Download URLs expire after about 1 hour; save assets to your own storage promptly.

## Batch API
- The official Batch API supports `POST /v1/videos` only.
- Batch requests must use JSON, not multipart.
- Upload assets ahead of time and reference them in the JSON body.
- For image-guided Batch jobs, use JSON `input_reference` with `file_id` or `image_url`.
- Batch-generated videos remain downloadable for up to 24 hours after the batch completes.
- The bundled `scripts/sora.py create-batch` command is a local fan-out helper, not the official Batch API.

## Guardrails
- Only content suitable for audiences under 18
- No copyrighted characters or copyrighted music
- No real people (including public figures)
- Input images with human faces are currently rejected
