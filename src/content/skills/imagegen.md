---
title: "Imagegen"
description: "Use when the user asks to generate or edit images via the OpenAI Image API (for example: generate image, edit/inpaint/mask, background removal or replacement, transparent background, product shots, concept art, covers, or batch variants); run the ..."
category: "development"
source: "community"
author: "Community"
tags: ["imagegen"]
date: 2026-03-20
---

# Image Generation Skill

Generates or edits images for the current project (e.g., website assets, game assets, UI mockups, product mockups, wireframes, logo design, photorealistic images, infographics). Defaults to `gpt-image-1.5` and the OpenAI Image API, and prefers the bundled CLI for deterministic, reproducible runs.

## When to use
- Generate a new image (concept art, product shot, cover, website hero)
- Edit an existing image (inpainting, masked edits, lighting or weather transformations, background replacement, object removal, compositing, transparent background)
- Batch runs (many prompts, or many variants across prompts)

## Decision tree (generate vs edit vs batch)
- If the user provides an input image (or says “edit/retouch/inpaint/mask/translate/localize/change only X”) → **edit**
- Else if the user needs many different prompts/assets → **generate-batch**
- Else → **generate**

## Workflow
1. Decide intent: generate vs edit vs batch (see decision tree above).
2. Collect inputs up front: prompt(s), exact text (verbatim), constraints/avoid list, and any input image(s)/mask(s). For multi-image edits, label each input by index and role; for edits, list invariants explicitly.
3. If batch: write a temporary JSONL under tmp/ (one job per line), run once, then delete the JSONL.
4. Augment prompt into a short labeled spec (structure + constraints) without inventing new creative requirements.
5. Run the bundled CLI (`scripts/image_gen.py`) with sensible defaults (see references/cli.md).
6. For complex edits/generations, inspect outputs (open/view images) and validate: subject, style, composition, text accuracy, and invariants/avoid items.
7. Iterate: make a single targeted change (prompt or mask), re-run, re-check.
8. Save/return final outputs and note the final prompt + flags used.

## Temp and output conventions
- Use `tmp/imagegen/` for intermediate files (for example JSONL batches); delete when done.
- Write final artifacts under `output/imagegen/` when working in this repo.
- Use `--out` or `--out-dir` to control output paths; keep filenames stable and descriptive.

## Dependencies (install if missing)
Prefer `uv` for dependency management.

Python packages:
```
uv pip install openai pillow
```
If `uv` is unavailable:
```
python3 -m pip install openai pillow
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
- Use `gpt-image-1.5` unless the user explicitly asks for `gpt-image-1-mini` or explicitly prefers a cheaper/faster model.
- Assume the user wants a new image unless they explicitly ask for an edit.
- Require `OPENAI_API_KEY` before any live API call.
- Use the OpenAI Python SDK (`openai` package) for all API calls; do not use raw HTTP.
- If the user requests edits, use `client.images.edit(...)` and include input images (and mask if provided).
- Prefer the bundled CLI (`scripts/image_gen.py`) over writing new one-off scripts.
- Never modify `scripts/image_gen.py`. If something is missing, ask the user before doing anything else.
- If the result isn’t clearly relevant or doesn’t satisfy constraints, iterate with small targeted prompt changes; only ask a question if a missing detail blocks success.

## Prompt augmentation
Reformat user prompts into a structured, production-oriented spec. Only make implicit details explicit; do not invent new requirements.

## Use-case taxonomy (exact slugs)
Classify each request into one of these buckets and keep the slug consistent across prompts and references.

Generate:
- photorealistic-natural — candid/editorial lifestyle scenes with real texture and natural lighting.
- product-mockup — product/packaging shots, catalog imagery, merch concepts.
- ui-mockup — app/web interface mockups that look shippable.
- infographic-diagram — diagrams/infographics with structured layout and text.
- logo-brand — logo/mark exploration, vector-friendly.
- illustration-story — comics, children’s book art, narrative scenes.
- stylized-concept — style-driven concept art, 3D/stylized renders.
- historical-scene — period-accurate/world-knowledge scenes.

Edit:
- text-localization — translate/replace in-image text, preserve layout.
- identity-preserve — try-on, person-in-scene; lock face/body/pose.
- precise-object-edit — remove/replace a specific element (incl. interior swaps).
- lighting-weather — time-of-day/season/atmosphere changes only.
- background-extraction — transparent background / clean cutout.
- style-transfer — apply reference style while changing subject/scene.
- compositing — multi-image insert/merge with matched lighting/perspective.
- sketch-to-render — drawing/line art to photoreal render.

Quick clarification (augmentation vs invention):
- If the user says “a hero image for a landing page”, you may add *layout/composition constraints* that are implied by that use (e.g., “generous negative space on the right for headline text”).
- Do not introduce new creative elements the user didn’t ask for (e.g., adding a mascot, changing the subject, inventing brand names/logos).

Template (include only relevant lines):
```
Use case: <taxonomy slug>
Asset type: <where the asset will be used>
Primary request: <user's main prompt>
Scene/background: <environment>
Subject: <main subject>
Style/medium: <photo/illustration/3D/etc>
Composition/framing: <wide/close/top-down; placement>
Lighting/mood: <lighting + mood>
Color palette: <palette notes>
Materials/textures: <surface details>
Quality: <low/medium/high/auto>
Input fidelity (edits): <low/high>
Text (verbatim): "<exact text>"
Constraints: <must keep/must avoid>
Avoid: <negative constraints>
```

Augmentation rules:
- Keep it short; add only details the user already implied or provided elsewhere.
- Always classify the request into a taxonomy slug above and tailor constraints/composition/quality to that bucket. Use the slug to find the matching example in `references/sample-prompts.md`.
- If the user gives a broad request (e.g., "Generate images for this website"), use judgment to propose tasteful, context-appropriate assets and map each to a taxonomy slug.
- For edits, explicitly list invariants ("change only X; keep Y unchanged").
- If any critical detail is missing and blocks success, ask a question; otherwise proceed.

## Examples

### Generation example (hero image)
```
Use case: stylized-concept
Asset type: landing page hero
Primary request: a minimal hero image of a ceramic coffee mug
Style/medium: clean product photography
Composition/framing: centered product, generous negative space on the right
Lighting/mood: soft studio lighting
Constraints: no logos, no text, no watermark
```

### Edit example (invariants)
```
Use case: precise-object-edit
Asset type: product photo background replacement
Primary request: replace the background with a warm sunset gradient
Constraints: change only the background; keep the product and its edges unchanged; no text; no watermark
```

## Prompting best practices (short list)
- Structure prompt as scene -> subject -> details -> constraints.
- Include intended use (ad, UI mock, infographic) to set the mode and polish level.
- Use camera/composition language for photorealism.
- Quote exact text and specify typography + placement.
- For tricky words, spell them letter-by-letter and require verbatim rendering.
- For multi-image inputs, reference images by index and describe how to combine them.
- For edits, repeat invariants every iteration to reduce drift.
- Iterate with single-change follow-ups.
- For latency-sensitive runs, start with quality=low; use quality=high for text-heavy or detail-critical outputs.
- For strict edits (identity/layout lock), consider input_fidelity=high.
- If results feel “tacky”, add a brief “Avoid:” line (stock-photo vibe; cheesy lens flare; oversaturated neon; harsh bloom; oversharpening; clutter) and specify restraint (“editorial”, “premium”, “subtle”).

More principles: `references/prompting.md`. Copy/paste specs: `references/sample-prompts.md`.

## Guidance by asset type
Asset-type templates (website assets, game assets, wireframes, logo) are consolidated in `references/sample-prompts.md`.

## CLI + environment notes
- CLI commands + examples: `references/cli.md`
- API parameter quick reference: `references/image-api.md`
- If network approvals / sandbox settings are getting in the way: `references/codex-network.md`

## Reference map
- **`references/cli.md`**: how to *run* image generation/edits/batches via `scripts/image_gen.py` (commands, flags, recipes).
- **`references/image-api.md`**: what knobs exist at the API level (parameters, sizes, quality, background, edit-only fields).
- **`references/prompting.md`**: prompting principles (structure, constraints/invariants, iteration patterns).
- **`references/sample-prompts.md`**: copy/paste prompt recipes (generate + edit workflows; examples only).
- **`references/codex-network.md`**: environment/sandbox/network-approval troubleshooting.

---

## Reference: Cli

# CLI reference (`scripts/image_gen.py`)

This file contains the “command catalog” for the bundled image generation CLI. Keep `SKILL.md` as overview-first; put verbose CLI details here.

## What this CLI does
- `generate`: generate new images from a prompt
- `edit`: edit an existing image (optionally with a mask) — inpainting / background replacement / “change only X”
- `generate-batch`: run many jobs from a JSONL file (one job per line)

Real API calls require **network access** + `OPENAI_API_KEY`. `--dry-run` does not.

## Quick start (works from any repo)
Set a stable path to the skill CLI (default `CODEX_HOME` is `~/.codex`):

```
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export IMAGE_GEN="$CODEX_HOME/skills/imagegen/scripts/image_gen.py"
```

Dry-run (no API call; no network required; does not require the `openai` package):

```
python "$IMAGE_GEN" generate --prompt "Test" --dry-run
```

Generate (requires `OPENAI_API_KEY` + network):

```
uv run --with openai python "$IMAGE_GEN" generate --prompt "A cozy alpine cabin at dawn" --size 1024x1024
```

No `uv` installed? Use your active Python env:

```
python "$IMAGE_GEN" generate --prompt "A cozy alpine cabin at dawn" --size 1024x1024
```

## Guardrails (important)
- Use `python "$IMAGE_GEN" ...` (or equivalent full path) for generations/edits/batch work.
- Do **not** create one-off runners (e.g. `gen_images.py`) unless the user explicitly asks for a custom wrapper.
- **Never modify** `scripts/image_gen.py`. If something is missing, ask the user before doing anything else.

## Defaults (unless overridden by flags)
- Model: `gpt-image-1.5`
- Size: `1024x1024`
- Quality: `auto`
- Output format: `png`
- Background: unspecified (API default). If you set `--background transparent`, also set `--output-format png` or `webp`.

## Quality + input fidelity
- `--quality` works for `generate`, `edit`, and `generate-batch`: `low|medium|high|auto`.
- `--input-fidelity` is **edit-only**: `low|high` (use `high` for strict edits like identity or layout lock).

Example:
```
python "$IMAGE_GEN" edit --image input.png --prompt "Change only the background" --quality high --input-fidelity high
```

## Masks (edits)
- Use a **PNG** mask; an alpha channel is strongly recommended.
- The mask should match the input image dimensions.
- In the edit prompt, repeat invariants (e.g., “change only the background; keep the subject unchanged”) to reduce drift.

## Optional deps
Prefer `uv run --with ...` for an out-of-the-box run without changing the current project env; otherwise install into your active env:

```
uv pip install openai
```

## Common recipes

Generate + also write a downscaled copy for fast web loading:

```
uv run --with openai --with pillow python "$IMAGE_GEN" generate \
  --prompt "A cozy alpine cabin at dawn" \
  --size 1024x1024 \
  --downscale-max-dim 1024
```

Notes:
- Downscaling writes an extra file next to the original (default suffix `-web`, e.g. `output-web.png`).
- Downscaling requires Pillow (use `uv run --with pillow ...` or install it into your env).

Generate with augmentation fields:

```
python "$IMAGE_GEN" generate \
  --prompt "A minimal hero image of a ceramic coffee mug" \
  --use-case "landing page hero" \
  --style "clean product photography" \
  --composition "centered product, generous negative space" \
  --constraints "no logos, no text"
```

Generate multiple prompts concurrently (async batch):

```
mkdir -p tmp/imagegen
cat > tmp/imagegen/prompts.jsonl << 'EOF'
{"prompt":"Cavernous hangar interior with a compact shuttle parked center-left, open bay door","use_case":"game concept art environment","composition":"wide-angle, low-angle, cinematic framing","lighting":"volumetric light rays through drifting fog","constraints":"no logos or trademarks; no watermark","size":"1536x1024"}
{"prompt":"Gray wolf in profile in a snowy forest, crisp fur texture","use_case":"wildlife photography print","composition":"100mm, eye-level, shallow depth of field","constraints":"no logos or trademarks; no watermark","size":"1024x1024"}
EOF

python "$IMAGE_GEN" generate-batch --input tmp/imagegen/prompts.jsonl --out-dir out --concurrency 5

# Cleanup (recommended)
rm -f tmp/imagegen/prompts.jsonl
```

Notes:
- Use `--concurrency` to control parallelism (default `5`). Higher concurrency can hit rate limits; the CLI retries on transient errors.
- Per-job overrides are supported in JSONL (e.g., `size`, `quality`, `background`, `output_format`, `n`, and prompt-augmentation fields).
- `--n` generates multiple variants for a single prompt; `generate-batch` is for many different prompts.
- Treat the JSONL file as temporary: write it under `tmp/` and delete it after the run (don’t commit it).

Edit:

```
python "$IMAGE_GEN" edit --image input.png --mask mask.png --prompt "Replace the background with a warm sunset"
```

## CLI notes
- Supported sizes: `1024x1024`, `1536x1024`, `1024x1536`, or `auto`.
- Transparent backgrounds require `output_format` to be `png` or `webp`.
- Default output is `output.png`; multiple images become `output-1.png`, `output-2.png`, etc.
- Use `--no-augment` to skip prompt augmentation.

## See also
- API parameter quick reference: `references/image-api.md`
- Prompt examples: `references/sample-prompts.md`

---

## Reference: Codex Network

# Codex network approvals / sandbox notes

This guidance is intentionally isolated from `SKILL.md` because it can vary by environment and may become stale. Prefer the defaults in your environment when in doubt.

## Why am I asked to approve every image generation call?
Image generation uses the OpenAI Image API, so the CLI needs outbound network access. In many Codex setups, network access is disabled by default (especially under stricter sandbox modes), and/or the approval policy may require confirmation before networked commands run.

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

## Reference: Image Api

# Image API quick reference

## Endpoints
- Generate: `POST /v1/images/generations` (`client.images.generate(...)`)
- Edit: `POST /v1/images/edits` (`client.images.edit(...)`)

## Models
- Default: `gpt-image-1.5`
- Alternatives: `gpt-image-1-mini` (for faster, lower-cost generation)

## Core parameters (generate + edit)
- `prompt`: text prompt
- `model`: image model
- `n`: number of images (1-10)
- `size`: `1024x1024`, `1536x1024`, `1024x1536`, or `auto`
- `quality`: `low`, `medium`, `high`, or `auto`
- `background`: `transparent`, `opaque`, or `auto` (transparent requires `png`/`webp`)
- `output_format`: `png` (default), `jpeg`, `webp`
- `output_compression`: 0-100 (jpeg/webp only)
- `moderation`: `auto` (default) or `low`

## Edit-specific parameters
- `image`: one or more input images (first image is primary)
- `mask`: optional mask image (same size, alpha channel required)
- `input_fidelity`: `low` (default) or `high` (support varies by model) - set it to `high` if the user needs a very specific edit and you can't achieve it with the default `low` fidelity.

## Output
- `data[]` list with `b64_json` per image

## Limits & notes
- Input images and masks must be under 50MB.
- Use edits endpoint when the user requests changes to an existing image.
- Masking is prompt-guided; exact shapes are not guaranteed.
- Large sizes and high quality increase latency and cost.
- For fast iteration or latency-sensitive runs, start with `quality=low`; raise to `high` for text-heavy or detail-critical outputs.
- Use `input_fidelity=high` for strict edits (identity preservation, layout lock, or precise compositing).

---

## Reference: Prompting

# Prompting best practices (gpt-image-1.5)

## Contents
- [Structure](#structure)
- [Specificity](#specificity)
- [Avoiding “tacky” outputs](#avoiding-tacky-outputs)
- [Composition & layout](#composition--layout)
- [Constraints & invariants](#constraints--invariants)
- [Text in images](#text-in-images)
- [Multi-image inputs](#multi-image-inputs)
- [Iterate deliberately](#iterate-deliberately)
- [Quality vs latency](#quality-vs-latency)
- [Use-case tips](#use-case-tips)
- [Where to find copy/paste recipes](#where-to-find-copypaste-recipes)

## Structure
- Use a consistent order: scene/background -> subject -> key details -> constraints -> output intent.
- Include intended use (ad, UI mock, infographic) to set the mode and polish level.
- For complex requests, use short labeled lines instead of a long paragraph.

## Specificity
- Name materials, textures, and visual medium (photo, watercolor, 3D render).
- For photorealism, include camera/composition language (lens, framing, lighting).
- Add targeted quality cues only when needed (film grain, textured brushstrokes, macro detail); avoid generic "8K" style prompts.

## Avoiding “tacky” outputs
- Don’t use vibe-only buzzwords (“epic”, “cinematic”, “trending”, “8k”, “award-winning”, “unreal engine”, “artstation”) unless the user explicitly wants that look.
- Specify restraint: “minimal”, “editorial”, “premium”, “subtle”, “natural color grading”, “soft contrast”, “no harsh bloom”, “no oversharpening”.
- For 3D/illustration, name the finish you want: “matte”, “paper grain”, “ink texture”, “flat color with soft shadow”; avoid “glossy plastic” unless requested.
- Add a short negative line when needed (especially for marketing art): “Avoid: stock-photo vibe; cheesy lens flare; oversaturated neon; excessive bokeh; fake-looking smiles; clutter”.

## Composition & layout
- Specify framing and viewpoint (close-up, wide, top-down) and placement ("logo top-right").
- Call out negative space if you need room for UI or overlays.

## Constraints & invariants
- State what must not change ("keep background unchanged").
- For edits, say "change only X; keep Y unchanged" and repeat invariants on every iteration to reduce drift.

## Text in images
- Put literal text in quotes or ALL CAPS and specify typography (font style, size, color, placement).
- Spell uncommon words letter-by-letter if accuracy matters.
- For in-image copy, require verbatim rendering and no extra characters.

## Multi-image inputs
- Reference inputs by index and role ("Image 1: product, Image 2: style").
- Describe how to combine them ("apply Image 2's style to Image 1").
- For compositing, specify what moves where and what must remain unchanged.

## Iterate deliberately
- Start with a clean base prompt, then make small single-change edits.
- Re-specify critical constraints when you iterate.

## Quality vs latency
- For latency-sensitive runs, start at `quality=low` and only raise it if needed.
- Use `quality=high` for text-heavy or detail-critical images.
- For strict edits (identity preservation, layout lock), consider `input_fidelity=high`.

## Use-case tips
Generate:
- photorealistic-natural: Prompt as if a real photo is captured in the moment; use photography language (lens, lighting, framing); call for real texture (pores, wrinkles, fabric wear, imperfections); avoid studio polish or staging; use `quality=high` when detail matters.
- product-mockup: Describe the product/packaging and materials; ensure clean silhouette and label clarity; if in-image text is needed, require verbatim rendering and specify typography.
- ui-mockup: Describe a real product; focus on layout, hierarchy, and common UI elements; avoid concept-art language so it looks shippable.
- infographic-diagram: Define the audience and layout flow; label parts explicitly; require verbatim text; use `quality=high`.
- logo-brand: Keep it simple and scalable; ask for a strong silhouette and balanced negative space; avoid gradients and fine detail.
- illustration-story: Define panels or scene beats; keep each action concrete; for continuity, restate character traits and outfit each time.
- stylized-concept: Specify style cues, material finish, and rendering approach (3D, painterly, clay); add a short "Avoid" line to prevent tacky effects.
- historical-scene: State the location/date and required period accuracy; constrain clothing, props, and environment to match the era.

Edit:
- text-localization: Change only the text; preserve layout, typography, spacing, and hierarchy; no extra words or reflow unless needed.
- identity-preserve: Lock identity (face, body, pose, hair, expression); change only the specified elements; match lighting and shadows; use `input_fidelity=high` if likeness drifts.
- precise-object-edit: Specify exactly what to remove/replace; preserve surrounding texture and lighting; keep everything else unchanged.
- lighting-weather: Change only environmental conditions (light, shadows, atmosphere, precipitation); keep geometry, framing, and subject identity.
- background-extraction: Request transparent background; crisp silhouette; no halos; preserve label text exactly; optionally add a subtle contact shadow.
- style-transfer: Specify style cues to preserve (palette, texture, brushwork) and what must change; add "no extra elements" to prevent drift.
- compositing: Reference inputs by index; specify what moves where; match lighting, perspective, and scale; keep background and framing unchanged.
- sketch-to-render: Preserve layout, proportions, and perspective; add plausible materials, lighting, and environment; "do not add new elements or text."

## Where to find copy/paste recipes
For copy/paste prompt specs (examples only), see `references/sample-prompts.md`. This file focuses on principles, structure, and iteration patterns.

---

## Reference: Sample Prompts

# Sample prompts (copy/paste)

Use these as starting points (recipes only). Keep user-provided requirements; do not invent new creative elements.

For prompting principles (structure, invariants, iteration), see `references/prompting.md`.

## Generate

### photorealistic-natural
```
Use case: photorealistic-natural
Primary request: candid photo of an elderly sailor on a small fishing boat adjusting a net
Scene/background: coastal water with soft haze
Subject: weathered skin with wrinkles and sun texture; a calm dog on deck nearby
Style/medium: photorealistic candid photo
Composition/framing: medium close-up, eye-level, 50mm lens
Lighting/mood: soft coastal daylight, shallow depth of field, subtle film grain
Materials/textures: real skin texture, worn fabric, salt-worn wood
Constraints: natural color balance; no heavy retouching; no glamorization; no watermark
Avoid: studio polish; staged look
Quality: high
```

### product-mockup
```
Use case: product-mockup
Primary request: premium product photo of a matte black shampoo bottle with a minimal label
Scene/background: clean studio gradient from light gray to white
Subject: single bottle centered with subtle reflection
Style/medium: premium product photography
Composition/framing: centered, slight three-quarter angle, generous padding
Lighting/mood: softbox lighting, clean highlights, controlled shadows
Materials/textures: matte plastic, crisp label printing
Constraints: no logos or trademarks; no watermark
Quality: high
```

### ui-mockup
```
Use case: ui-mockup
Primary request: mobile app UI for a local farmers market with vendors and specials
Scene/background: clean white background with subtle natural accents
Subject: header, vendor list with small photos, "Today's specials" section, location and hours
Style/medium: realistic product UI, not concept art
Composition/framing: iPhone frame, balanced spacing and hierarchy
Constraints: practical layout, clear typography, no logos or trademarks, no watermark
```

### infographic-diagram
```
Use case: infographic-diagram
Primary request: detailed infographic of an automatic coffee machine flow
Scene/background: clean, light neutral background
Subject: bean hopper -> grinder -> brew group -> boiler -> water tank -> drip tray
Style/medium: clean vector-like infographic with clear callouts and arrows
Composition/framing: vertical poster layout, top-to-bottom flow
Text (verbatim): "Bean Hopper", "Grinder", "Brew Group", "Boiler", "Water Tank", "Drip Tray"
Constraints: clear labels, strong contrast, no logos or trademarks, no watermark
Quality: high
```

### logo-brand
```
Use case: logo-brand
Primary request: original logo for "Field & Flour", a local bakery
Style/medium: vector logo mark; flat colors; minimal
Composition/framing: single centered logo on plain background with padding
Constraints: strong silhouette, balanced negative space; original design only; no gradients unless essential; no trademarks; no watermark
```

### illustration-story
```
Use case: illustration-story
Primary request: 4-panel comic about a pet left alone at home
Scene/background: cozy living room across panels
Subject: pet reacting to the owner leaving, then relaxing, then returning to a composed pose
Style/medium: comic illustration with clear panels
Composition/framing: 4 equal-sized vertical panels, readable actions per panel
Constraints: no text; no logos or trademarks; no watermark
```

### stylized-concept
```
Use case: stylized-concept
Primary request: cavernous hangar interior with tall support beams and drifting fog
Scene/background: industrial hangar interior, deep scale, light haze
Subject: compact shuttle, parked center-left, bay door open
Style/medium: cinematic concept art, industrial realism
Composition/framing: wide-angle, low-angle, cinematic framing
Lighting/mood: volumetric light rays cutting through fog
Constraints: no logos or trademarks; no watermark
```

### historical-scene
```
Use case: historical-scene
Primary request: outdoor crowd scene in Bethel, New York on August 16, 1969
Scene/background: open field, temporary stages, period-accurate tents and signage
Subject: crowd in period-accurate clothing, authentic staging and environment
Style/medium: photorealistic photo
Composition/framing: wide shot, eye-level
Constraints: period-accurate details; no modern objects; no logos or trademarks; no watermark
```

## Asset type templates (taxonomy-aligned)

### Website assets template
```
Use case: <photorealistic-natural|stylized-concept|product-mockup|infographic-diagram|ui-mockup>
Asset type: <hero image / section illustration / blog header>
Primary request: <short description>
Scene/background: <environment or abstract background>
Subject: <main subject>
Style/medium: <photo/illustration/3D>
Composition/framing: <wide/centered; specify negative space side>
Lighting/mood: <soft/bright/neutral>
Color palette: <brand colors or neutral>
Constraints: <no text; no logos; no watermark; leave space for UI>
```

### Website assets example: minimal hero background
```
Use case: stylized-concept
Asset type: landing page hero background
Primary request: minimal abstract background with a soft gradient and subtle texture (calm, modern)
Style/medium: matte illustration / soft-rendered abstract background (not glossy 3D)
Composition/framing: wide composition; large negative space on the right for headline
Lighting/mood: gentle studio glow
Color palette: cool neutrals with a restrained blue accent
Constraints: no text; no logos; no watermark
```

### Website assets example: feature section illustration
```
Use case: stylized-concept
Asset type: feature section illustration
Primary request: simple abstract shapes suggesting connection and flow (tasteful, minimal)
Scene/background: subtle light-gray backdrop with faint texture
Style/medium: flat illustration; soft shadows; restrained contrast
Composition/framing: centered cluster; open margins for UI
Color palette: muted teal and slate, low contrast accents
Constraints: no text; no logos; no watermark
```

### Website assets example: blog header image
```
Use case: photorealistic-natural
Asset type: blog header image
Primary request: overhead desk scene with notebook, pen, and coffee cup
Scene/background: warm wooden tabletop
Style/medium: photorealistic photo
Composition/framing: wide crop; subject placed left; right side left empty
Lighting/mood: soft morning light
Constraints: no text; no logos; no watermark
```

### Game assets template
```
Use case: stylized-concept
Asset type: <game environment concept art / game character concept / game UI icon / tileable game texture>
Primary request: <biome/scene/character/icon/material>
Scene/background: <location + set dressing> (if applicable)
Subject: <main focal element(s)>
Style/medium: <realistic/stylized>; <concept art / character render / UI icon / texture>
Composition/framing: <wide/establishing/top-down>; <camera angle>; <focal point placement>
Lighting/mood: <time of day>; <mood>; <volumetric/fog/etc>
Constraints: no logos or trademarks; no watermark
```

### Game assets example: environment concept art
```
Use case: stylized-concept
Asset type: game environment concept art
Primary request: cavernous hangar interior with tall support beams and drifting fog
Scene/background: industrial hangar interior, deep scale, light haze
Subject: compact shuttle, parked center-left, bay door open
Foreground: painted floor markings; cables; tool carts along edges
Style/medium: cinematic concept art, industrial realism
Composition/framing: wide-angle, low-angle, cinematic framing
Lighting/mood: volumetric light rays cutting through fog
Constraints: no logos or trademarks; no watermark
```

### Game assets example: character concept
```
Use case: stylized-concept
Asset type: game character concept
Primary request: desert scout character with layered travel gear
Silhouette: long coat with hood, wide boots, satchel
Outfit/gear: dusty canvas, leather straps, brass buckles
Face/hair: windworn face, short cropped hair
Style/medium: character render; stylized realism
Pose: neutral hero pose
Background: simple neutral backdrop
Constraints: no logos or trademarks; no watermark
```

### Game assets example: UI icon
```
Use case: stylized-concept
Asset type: game UI icon
Primary request: round shield icon with a subtle rune pattern
Style/medium: painted game UI icon
Composition/framing: centered icon; generous padding; clear silhouette
Background: transparent
Lighting/mood: subtle highlights; crisp edges
Constraints: no text; no logos or trademarks; no watermark
```

### Game assets example: tileable texture
```
Use case: stylized-concept
Asset type: tileable game texture
Primary request: worn sandstone blocks
Style/medium: seamless tileable texture; PBR-ish look
Scale: medium tiling
Lighting: neutral / flat lighting
Constraints: seamless edges; no obvious focal elements; no text; no logos or trademarks; no watermark
```

### Wireframe template
```
Use case: ui-mockup
Asset type: website wireframe
Primary request: <page or flow to sketch>
Fidelity: low-fi grayscale wireframe; hand-drawn feel; simple boxes
Layout: <sections in order; grid/columns>
Annotations: <labels for key blocks>
Resolution/orientation: <landscape or portrait to match expected device>
Constraints: no color; no logos; no real photos; no watermark
```

### Wireframe example: homepage (desktop)
```
Use case: ui-mockup
Asset type: website wireframe
Primary request: SaaS homepage layout with clear hierarchy
Fidelity: low-fi grayscale wireframe; hand-drawn feel; simple boxes
Layout: top nav; hero with headline and CTA; three feature cards; testimonial strip; pricing preview; footer
Annotations: label each block ("Nav", "Hero", "CTA", "Feature", "Testimonial", "Pricing", "Footer")
Resolution/orientation: landscape (wide) for desktop
Constraints: no color; no logos; no real photos; no watermark
```

### Wireframe example: pricing page
```
Use case: ui-mockup
Asset type: website wireframe
Primary request: pricing page layout with comparison table
Fidelity: low-fi grayscale wireframe; sketchy lines; simple boxes
Layout: header; plan toggle; 3 pricing cards; comparison table; FAQ accordion; footer
Annotations: label key areas ("Toggle", "Plan Card", "Table", "FAQ")
Resolution/orientation: landscape for desktop or portrait for tablet
Constraints: no color; no logos; no real photos; no watermark
```

### Wireframe example: mobile onboarding flow
```
Use case: ui-mockup
Asset type: website wireframe
Primary request: three-screen mobile onboarding flow
Fidelity: low-fi grayscale wireframe; hand-drawn feel; simple boxes
Layout: screen 1 (logo placeholder, headline, illustration placeholder, CTA); screen 2 (feature bullets); screen 3 (form fields + CTA)
Annotations: label each block and screen number
Resolution/orientation: portrait (tall) for mobile
Constraints: no color; no logos; no real photos; no watermark
```

### Logo template
```
Use case: logo-brand
Asset type: logo concept
Primary request: <brand idea or symbol concept>
Style/medium: vector logo mark; flat colors; minimal
Composition/framing: centered mark; clear silhouette; generous margin
Color palette: <1-2 colors; high contrast>
Text (verbatim): "<exact name>" (only if needed)
Constraints: no gradients; no mockups; no 3D; no watermark
```

### Logo example: abstract symbol mark
```
Use case: logo-brand
Asset type: logo concept
Primary request: geometric leaf symbol suggesting sustainability and growth
Style/medium: vector logo mark; flat colors; minimal
Composition/framing: centered mark; clear silhouette
Color palette: deep green and off-white
Constraints: no text; no gradients; no mockups; no 3D; no watermark
```

### Logo example: monogram mark
```
Use case: logo-brand
Asset type: logo concept
Primary request: interlocking monogram of the letters "AV"
Style/medium: vector logo mark; flat colors; minimal
Composition/framing: centered mark; balanced spacing
Color palette: black on white
Constraints: no gradients; no mockups; no 3D; no watermark
```

### Logo example: wordmark
```
Use case: logo-brand
Asset type: logo concept
Primary request: clean wordmark for a modern studio
Style/medium: vector wordmark; flat colors; minimal
Text (verbatim): "Studio North"
Composition/framing: centered text; even letter spacing
Color palette: charcoal on white
Constraints: no gradients; no mockups; no 3D; no watermark
```

## Edit

### text-localization
```
Use case: text-localization
Input images: Image 1: original infographic
Primary request: translate all in-image text to Spanish
Constraints: change only the text; preserve layout, typography, spacing, and hierarchy; no extra words; do not alter logos or imagery
```

### identity-preserve
```
Use case: identity-preserve
Input images: Image 1: person photo; Image 2..N: clothing items
Primary request: replace only the clothing with the provided garments
Constraints: preserve face, body shape, pose, hair, expression, and identity; match lighting and shadows; keep background unchanged; no accessories or text
Input fidelity (edits): high
```

### precise-object-edit
```
Use case: precise-object-edit
Input images: Image 1: room photo
Primary request: replace ONLY the white chairs with wooden chairs
Constraints: preserve camera angle, room lighting, floor shadows, and surrounding objects; keep all other aspects unchanged
```

### lighting-weather
```
Use case: lighting-weather
Input images: Image 1: original photo
Primary request: make it look like a winter evening with gentle snowfall
Constraints: preserve subject identity, geometry, camera angle, and composition; change only lighting, atmosphere, and weather
Quality: high
```

### background-extraction
```
Use case: background-extraction
Input images: Image 1: product photo
Primary request: extract the product on a transparent background
Output: transparent background (RGBA PNG)
Constraints: crisp silhouette, no halos/fringing; preserve label text exactly; no restyling
```

### style-transfer
```
Use case: style-transfer
Input images: Image 1: style reference
Primary request: apply Image 1's visual style to a man riding a motorcycle on a white background
Constraints: preserve palette, texture, and brushwork; no extra elements; plain white background
```

### compositing
```
Use case: compositing
Input images: Image 1: base scene; Image 2: subject to insert
Primary request: place the subject from Image 2 next to the person in Image 1
Constraints: match lighting, perspective, and scale; keep background and framing unchanged; no extra elements
Input fidelity (edits): high
```

### sketch-to-render
```
Use case: sketch-to-render
Input images: Image 1: drawing
Primary request: turn the drawing into a photorealistic image
Constraints: preserve layout, proportions, and perspective; choose realistic materials and lighting; do not add new elements or text
Quality: high
```
