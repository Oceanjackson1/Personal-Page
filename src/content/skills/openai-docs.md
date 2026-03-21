---
title: "Openai Docs"
description: "Use when the user asks how to build with OpenAI products or APIs and needs up-to-date official documentation with citations, help choosing the latest model for a use case, or explicit GPT-5.4 upgrade and prompt-upgrade guidance; prioritize OpenAI ..."
category: "research"
source: "community"
author: "Community"
tags: ["openai", "docs"]
date: 2026-03-20
---

# OpenAI Docs

Provide authoritative, current guidance from OpenAI developer docs using the developers.openai.com MCP server. Always prioritize the developer docs MCP tools over web.run for OpenAI-related questions. This skill may also load targeted files from `references/` for model-selection and GPT-5.4-specific requests, but current OpenAI docs remain authoritative. Only if the MCP server is installed and returns no meaningful results should you fall back to web search.

## Quick start

- Use `mcp__openaiDeveloperDocs__search_openai_docs` to find the most relevant doc pages.
- Use `mcp__openaiDeveloperDocs__fetch_openai_doc` to pull exact sections and quote/paraphrase accurately.
- Use `mcp__openaiDeveloperDocs__list_openai_docs` only when you need to browse or discover pages without a clear query.
- Load only the relevant file from `references/` when the question is about model selection or a GPT-5.4 upgrade.

## OpenAI product snapshots

1. Apps SDK: Build ChatGPT apps by providing a web component UI and an MCP server that exposes your app's tools to ChatGPT.
2. Responses API: A unified endpoint designed for stateful, multimodal, tool-using interactions in agentic workflows.
3. Chat Completions API: Generate a model response from a list of messages comprising a conversation.
4. Codex: OpenAI's coding agent for software development that can write, understand, review, and debug code.
5. gpt-oss: Open-weight OpenAI reasoning models (gpt-oss-120b and gpt-oss-20b) released under the Apache 2.0 license.
6. Realtime API: Build low-latency, multimodal experiences including natural speech-to-speech conversations.
7. Agents SDK: A toolkit for building agentic apps where a model can use tools and context, hand off to other agents, stream partial results, and keep a full trace.

## If MCP server is missing

If MCP tools fail or no OpenAI docs resources are available:

1. Run the install command yourself: `codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp`
2. If it fails due to permissions/sandboxing, immediately retry the same command with escalated permissions and include a 1-sentence justification for approval. Do not ask the user to run it yet.
3. Only if the escalated attempt fails, ask the user to run the install command.
4. Ask the user to restart Codex.
5. Re-run the doc search/fetch after restart.

## Workflow

1. Clarify the product scope and whether the request is general docs lookup, model selection, a GPT-5.4 upgrade, or a GPT-5.4 prompt upgrade.
2. If it is a model-selection request, load `references/latest-model.md`.
3. If it is an explicit GPT-5.4 upgrade request, load `references/upgrading-to-gpt-5p4.md`.
4. If the upgrade may require prompt changes, or the workflow is research-heavy, tool-heavy, coding-oriented, multi-agent, or long-running, also load `references/gpt-5p4-prompting-guide.md`.
5. Search docs with a precise query.
6. Fetch the best page and the exact section needed (use `anchor` when possible).
7. For GPT-5.4 upgrade reviews, always make the per-usage-site output explicit: target model, starting reasoning recommendation, `phase` assessment when relevant, prompt blocks, and compatibility status.
8. Answer with concise guidance and cite the doc source, using the reference files only as helper context.

## Reference map

Read only what you need:

- `references/latest-model.md` -> model-selection and "best/latest/current model" questions; verify every recommendation against current OpenAI docs before answering.
- `references/upgrading-to-gpt-5p4.md` -> only for explicit GPT-5.4 upgrade and upgrade-planning requests; verify the checklist and compatibility guidance against current OpenAI docs before answering.
- `references/gpt-5p4-prompting-guide.md` -> prompt rewrites and prompt-behavior upgrades for GPT-5.4; verify prompting guidance against current OpenAI docs before answering.

## Quality rules

- Treat OpenAI docs as the source of truth; avoid speculation.
- Keep quotes short and within policy limits; prefer paraphrase with citations.
- If multiple pages differ, call out the difference and cite both.
- Reference files are convenience guides only; for volatile guidance such as recommended models, upgrade instructions, or prompting advice, current OpenAI docs always win.
- If docs do not cover the user’s need, say so and offer next steps.

## Tooling notes

- Always use MCP doc tools before any web search for OpenAI-related questions.
- If the MCP server is installed but returns no meaningful results, then use web search as a fallback.
- When falling back to web search, restrict to official OpenAI domains (developers.openai.com, platform.openai.com) and cite sources.

---

## Reference: Gpt 5P4 Prompting Guide

# GPT-5.4 prompting upgrade guide

Use this guide when prompts written for older models need to be adapted for GPT-5.4 during an upgrade. Start lean: keep the model-string change narrow, preserve the original task intent, and add only the smallest prompt changes needed to recover behavior.

## Default upgrade posture

- Start with `model string only` whenever the old prompt is already short, explicit, and task-bounded.
- Move to `model string + light prompt rewrite` only when regressions appear in completeness, persistence, citation quality, verification, or verbosity.
- Prefer one or two targeted prompt additions over a broad rewrite.
- Treat reasoning effort as a last-mile knob. Start lower, then increase only after prompt-level fixes and evals.
- Before increasing reasoning effort, first add a completeness contract, a verification loop, and tool persistence rules - depending on the usage case.
- If the workflow clearly depends on implementation changes rather than prompt changes, treat it as blocked for prompt-only upgrade guidance.
- Do not classify a case as blocked just because the workflow uses tools; block only if the upgrade requires changing tool definitions, wiring, or other implementation details.

## Behavioral differences to account for

Current GPT-5.4 upgrade guidance suggests these strengths:

- stronger personality and tone adherence, with less drift over long answers
- better long-horizon and agentic workflow stamina
- stronger spreadsheet, finance, and formatting tasks
- more efficient tool selection and fewer unnecessary calls by default
- stronger structured generation and classification reliability

The main places where prompt guidance still helps are:

- retrieval-heavy workflows that need persistent tool use and explicit completeness
- research and citation discipline
- verification before irreversible or high-impact actions
- terminal and tool workflow hygiene
- defaults and implied follow-through
- verbosity control for compact, information-dense answers

Start with the smallest set of instructions that preserves correctness. Add the prompt blocks below only for workflows that actually need them.

## Prompt rewrite patterns

| Older prompt pattern | GPT-5.4 adjustment | Why | Example addition |
| --- | --- | --- | --- |
| Long, repetitive instructions that compensate for weaker instruction following | Remove duplicate scaffolding and keep only the constraints that materially change behavior | GPT-5.4 usually needs less repeated steering | Replace repeated reminders with one concise rule plus a verification block |
| Fast assistant prompt with no verbosity control | Keep the prompt as-is first; add a verbosity clamp only if outputs become too long | Many GPT-4o or GPT-4.1 upgrades work with just a model-string swap | Add `output_verbosity_spec` only after a verbosity regression |
| Tool-heavy agent prompt that assumes the model will keep searching until complete | Add persistence and verification rules | GPT-5.4 may use fewer tool calls by default for efficiency | Add `tool_persistence_rules` and `verification_loop` |
| Tool-heavy workflow where later actions depend on earlier lookup or retrieval | Add prerequisite and missing-context rules before action steps | GPT-5.4 benefits from explicit dependency-aware routing when context is still thin | Add `dependency_checks` and `missing_context_gating` |
| Retrieval workflow with several independent lookups | Add selective parallelism guidance | GPT-5.4 is strong at parallel tool use, but should not parallelize dependent steps | Add `parallel_tool_calling` |
| Batch workflow prompt that often misses items | Add an explicit completeness contract | Item accounting benefits from direct instruction | Add `completeness_contract` |
| Research prompt that needs grounding and citation discipline | Add research, citation, and empty-result recovery blocks | Multi-pass retrieval is stronger when the model is told how to react to weak or empty search results | Add `research_mode`, `citation_rules`, and `empty_result_handling`; add `tool_persistence_rules` when retrieval tools are already in use |
| Coding or terminal prompt with shell misuse or early stop failures | Keep the same tool surface and add terminal hygiene and verification instructions | Tool-using coding workflows are not blocked just because tools exist; they usually need better prompt steering, not host rewiring | Add `terminal_tool_hygiene` and `verification_loop`, optionally `tool_persistence_rules` |
| Multi-agent or support-triage workflow with escalation or completeness requirements | Add one lightweight control block for persistence, completeness, or verification | GPT-5.4 can be more efficient by default, so multi-step support flows benefit from an explicit completion or verification contract | Add at least one of `tool_persistence_rules`, `completeness_contract`, or `verification_loop` |

## Prompt blocks

Use these selectively. Do not add all of them by default.

### `output_verbosity_spec`

Use when:

- the upgraded model gets too wordy
- the host needs compact, information-dense answers
- the workflow benefits from a short overview plus a checklist

```text
<output_verbosity_spec>
- Default: 3-6 sentences or up to 6 bullets.
- If the user asked for a doc or report, use headings with short bullets.
- For multi-step tasks:
  - Start with 1 short overview paragraph.
  - Then provide a checklist with statuses: [done], [todo], or [blocked].
- Avoid repeating the user's request.
- Prefer compact, information-dense writing.
</output_verbosity_spec>
```

### `default_follow_through_policy`

Use when:

- the host expects the model to proceed on reversible, low-risk steps
- the upgraded model becomes too conservative or asks for confirmation too often

```text
<default_follow_through_policy>
- If the user's intent is clear and the next step is reversible and low-risk, proceed without asking permission.
- Only ask permission if the next step is:
  (a) irreversible,
  (b) has external side effects, or
  (c) requires missing sensitive information or a choice that materially changes outcomes.
- If proceeding, state what you did and what remains optional.
</default_follow_through_policy>
```

### `instruction_priority`

Use when:

- users often change task shape, format, or tone mid-conversation
- the host needs an explicit override policy instead of relying on defaults

```text
<instruction_priority>
- User instructions override default style, tone, formatting, and initiative preferences.
- Safety, honesty, privacy, and permission constraints do not yield.
- If a newer user instruction conflicts with an earlier one, follow the newer instruction.
- Preserve earlier instructions that do not conflict.
</instruction_priority>
```

### `tool_persistence_rules`

Use when:

- the workflow needs multiple retrieval or verification steps
- the model starts stopping too early because it is trying to save tool calls

```text
<tool_persistence_rules>
- Use tools whenever they materially improve correctness, completeness, or grounding.
- Do not stop early just to save tool calls.
- Keep calling tools until:
  (1) the task is complete, and
  (2) verification passes.
- If a tool returns empty or partial results, retry with a different strategy.
</tool_persistence_rules>
```

### `dig_deeper_nudge`

Use when:

- the model is too literal or stops at the first plausible answer
- the task is safety- or accuracy-sensitive and needs a small initiative nudge before raising reasoning effort

```text
<dig_deeper_nudge>
- Do not stop at the first plausible answer.
- Look for second-order issues, edge cases, and missing constraints.
- If the task is safety- or accuracy-critical, perform at least one verification step.
</dig_deeper_nudge>
```

### `dependency_checks`

Use when:

- later actions depend on prerequisite lookup, memory retrieval, or discovery steps
- the model may be tempted to skip prerequisite work because the intended end state seems obvious

```text
<dependency_checks>
- Before taking an action, check whether prerequisite discovery, lookup, or memory retrieval is required.
- Do not skip prerequisite steps just because the intended final action seems obvious.
- If a later step depends on the output of an earlier one, resolve that dependency first.
</dependency_checks>
```

### `parallel_tool_calling`

Use when:

- the workflow has multiple independent retrieval steps
- wall-clock time matters but some steps still need sequencing

```text
<parallel_tool_calling>
- When multiple retrieval or lookup steps are independent, prefer parallel tool calls to reduce wall-clock time.
- Do not parallelize steps with prerequisite dependencies or where one result determines the next action.
- After parallel retrieval, pause to synthesize before making more calls.
- Prefer selective parallelism: parallelize independent evidence gathering, not speculative or redundant tool use.
</parallel_tool_calling>
```

### `completeness_contract`

Use when:

- the task involves batches, lists, enumerations, or multiple deliverables
- missing items are a common failure mode

```text
<completeness_contract>
- Deliver all requested items.
- Maintain an itemized checklist of deliverables.
- For lists or batches:
  - state the expected count,
  - enumerate items 1..N,
  - confirm that none are missing before finalizing.
- If any item is blocked by missing data, mark it [blocked] and state exactly what is missing.
</completeness_contract>
```

### `empty_result_handling`

Use when:

- the workflow frequently performs search, CRM, logs, or retrieval steps
- no-results failures are often false negatives

```text
<empty_result_handling>
If a lookup returns empty or suspiciously small results:
- Do not conclude that no results exist immediately.
- Try at least 2 fallback strategies, such as a broader query, alternate filters, or another source.
- Only then report that no results were found, along with what you tried.
</empty_result_handling>
```

### `verification_loop`

Use when:

- the workflow has downstream impact
- accuracy, formatting, or completeness regressions matter

```text
<verification_loop>
Before finalizing:
- Check correctness: does the output satisfy every requirement?
- Check grounding: are factual claims backed by retrieved sources or tool output?
- Check formatting: does the output match the requested schema or style?
- Check safety and irreversibility: if the next step has external side effects, ask permission first.
</verification_loop>
```

### `missing_context_gating`

Use when:

- required context is sometimes missing early in the workflow
- the model should prefer retrieval over guessing

```text
<missing_context_gating>
- If required context is missing, do not guess.
- Prefer the appropriate lookup tool when the context is retrievable; ask a minimal clarifying question only when it is not.
- If you must proceed, label assumptions explicitly and choose a reversible action.
</missing_context_gating>
```

### `action_safety`

Use when:

- the agent will actively take actions through tools
- the host benefits from a short pre-flight and post-flight execution frame

```text
<action_safety>
- Pre-flight: summarize the intended action and parameters in 1-2 lines.
- Execute via tool.
- Post-flight: confirm the outcome and any validation that was performed.
</action_safety>
```

### `citation_rules`

Use when:

- the workflow produces cited answers
- fabricated citations or wrong citation formats are costly

```text
<citation_rules>
- Only cite sources that were actually retrieved in this session.
- Never fabricate citations, URLs, IDs, or quote spans.
- If you cannot find a source for a claim, say so and either:
  - soften the claim, or
  - explain how to verify it with tools.
- Use exactly the citation format required by the host application.
</citation_rules>
```

### `research_mode`

Use when:

- the workflow is research-heavy
- the host uses web search or retrieval tools

```text
<research_mode>
- Do research in 3 passes:
  1) Plan: list 3-6 sub-questions to answer.
  2) Retrieve: search each sub-question and follow 1-2 second-order leads.
  3) Synthesize: resolve contradictions and write the final answer with citations.
- Stop only when more searching is unlikely to change the conclusion.
</research_mode>
```

If your host environment uses a specific research tool or requires a submit step, combine this with the host's finalization contract.

### `structured_output_contract`

Use when:

- the host depends on strict JSON, SQL, or other structured output

```text
<structured_output_contract>
- Output only the requested format.
- Do not add prose or markdown fences unless they were requested.
- Validate that parentheses and brackets are balanced.
- Do not invent tables or fields.
- If required schema information is missing, ask for it or return an explicit error object.
</structured_output_contract>
```

### `bbox_extraction_spec`

Use when:

- the workflow extracts OCR boxes, document regions, or other coordinates
- layout drift or missed dense regions are common failure modes

```text
<bbox_extraction_spec>
- Use the specified coordinate format exactly, such as [x1,y1,x2,y2] normalized to 0..1.
- For each box, include page, label, text snippet, and confidence.
- Add a vertical-drift sanity check so boxes stay aligned with the correct line of text.
- If the layout is dense, process page by page and do a second pass for missed items.
</bbox_extraction_spec>
```

### `terminal_tool_hygiene`

Use when:

- the prompt belongs to a terminal-based or coding-agent workflow
- tool misuse or shell misuse has been observed

```text
<terminal_tool_hygiene>
- Only run shell commands through the terminal tool.
- Never try to "run" tool names as shell commands.
- If a patch or edit tool exists, use it directly instead of emulating it in bash.
- After changes, run a lightweight verification step such as ls, tests, or a build before declaring the task done.
</terminal_tool_hygiene>
```

### `user_updates_spec`

Use when:

- the workflow is long-running and user updates matter

```text
<user_updates_spec>
- Only update the user when starting a new major phase or when the plan changes.
- Each update should contain:
  - 1 sentence on what changed,
  - 1 sentence on the next step.
- Do not narrate routine tool calls.
- Keep the user-facing update short, even when the actual work is exhaustive.
</user_updates_spec>
```

If you are using [Compaction](https://developers.openai.com/api/docs/guides/compaction) in the Responses API, compact after major milestones, treat compacted items as opaque state, and keep prompts functionally identical after compaction.

## Responses `phase` guidance

For long-running Responses workflows, preambles, or tool-heavy agents that replay assistant items, review whether `phase` is already preserved.

- If the host already round-trips `phase`, keep it intact during the upgrade.
- If the host uses `previous_response_id` and does not manually replay assistant items, note that this may reduce manual `phase` handling needs.
- If reliable GPT-5.4 behavior would require adding or preserving `phase` and that would need code edits, treat the case as blocked for prompt-only or model-string-only migration guidance.

## Example upgrade profiles

### GPT-5.2

- Use `gpt-5.4`
- Match the current reasoning effort first
- Preserve the existing latency and quality profile before tuning prompt blocks
- If the repo does not expose the exact setting, emit `same` as the starting recommendation

### GPT-5.3-Codex

- Use `gpt-5.4`
- Match the current reasoning effort first
- If you need Codex-style speed and efficiency, add verification blocks before increasing reasoning effort
- If the repo does not expose the exact setting, emit `same` as the starting recommendation

### GPT-4o or GPT-4.1 assistant

- Use `gpt-5.4`
- Start with `none` reasoning effort
- Add `output_verbosity_spec` only if output becomes too verbose

### Long-horizon agent

- Use `gpt-5.4`
- Start with `medium` reasoning effort
- Add `tool_persistence_rules`
- Add `completeness_contract`
- Add `verification_loop`

### Research workflow

- Use `gpt-5.4`
- Start with `medium` reasoning effort
- Add `research_mode`
- Add `citation_rules`
- Add `empty_result_handling`
- Add `tool_persistence_rules` when the host already uses web or retrieval tools
- Add `parallel_tool_calling` when the retrieval steps are independent

### Support triage or multi-agent workflow

- Use `gpt-5.4`
- Prefer `model string + light prompt rewrite` over `model string only`
- Add at least one of `tool_persistence_rules`, `completeness_contract`, or `verification_loop`
- Add more only if evals show a real regression

### Coding or terminal workflow

- Use `gpt-5.4`
- Keep the model-string change narrow
- Match the current reasoning effort first if you are upgrading from GPT-5.3-Codex
- Add `terminal_tool_hygiene`
- Add `verification_loop`
- Add `dependency_checks` when actions depend on prerequisite lookup or discovery
- Add `tool_persistence_rules` if the agent stops too early
- Review whether `phase` is already preserved for long-running Responses flows or assistant preambles
- Do not classify this as blocked just because the workflow uses tools; block only if the upgrade requires changing tool definitions or wiring
- If the repo already uses Responses plus tools and no required host-side change is shown, prefer `model_string_plus_light_prompt_rewrite` over `blocked`

## Prompt regression checklist

- Check whether the upgraded prompt still preserves the original task intent.
- Check whether the new prompt is leaner, not just longer.
- Check completeness, citation quality, dependency handling, verification behavior, and verbosity.
- For long-running Responses agents, check whether `phase` handling is already in place or needs implementation work.
- Confirm that each added prompt block addresses an observed regression.
- Remove prompt blocks that are not earning their keep.

---

## Reference: Latest Model

# Latest model guide

This file is a curated helper. Every recommendation here must be verified against current OpenAI docs before it is repeated to a user.

## Current model map

| Model ID | Use for |
| --- | --- |
| `gpt-5.4` | Default text plus reasoning for most new apps, including for coding use-cases |
| `gpt-5.4-pro` | Only when the user explicitly asks for maximum reasoning or quality; substantially slower and more expensive |
| `gpt-5.4-mini` | Cheaper and faster reasoning with good quality, including for coding use-cases |
| `gpt-5.4-nano` | High-throughput simple tasks and classification |
| `gpt-image-1.5` | Best image generation and edit quality |
| `gpt-image-1-mini` | Cost-optimized image generation |
| `gpt-4o-mini-tts` | Text-to-speech |
| `gpt-4o-mini-transcribe` | Speech-to-text, fast and cost-efficient |
| `gpt-realtime-1.5` | Realtime voice and multimodal sessions |
| `gpt-realtime-mini` | Cheaper realtime sessions |
| `gpt-audio` | Chat Completions audio input and output |
| `gpt-audio-mini` | Cheaper Chat Completions audio workflows |
| `sora-2` | Faster iteration and draft video generation |
| `sora-2-pro` | Higher-quality production video |
| `omni-moderation-latest` | Text and image moderation |
| `text-embedding-3-large` | Higher-quality retrieval embeddings; default in this skill because no best-specific row exists |
| `text-embedding-3-small` | Lower-cost embeddings |

## Maintenance notes

- This file will drift unless it is periodically re-verified against current OpenAI docs.
- If this file conflicts with current docs, the docs win.

---

## Reference: Upgrading To Gpt 5P4

# Upgrading to GPT-5.4

Use this guide when the user explicitly asks to upgrade an existing integration to GPT-5.4. Pair it with current OpenAI docs lookups. The default target string is `gpt-5.4`.

## Upgrade posture

Upgrade with the narrowest safe change set:

- replace the model string first
- update only the prompts that are directly tied to that model usage
- prefer prompt-only upgrades when possible
- if the upgrade would require API-surface changes, parameter rewrites, tool rewiring, or broader code edits, mark it as blocked instead of stretching the scope

## Upgrade workflow

1. Inventory current model usage.
   - Search for model strings, client calls, and prompt-bearing files.
   - Include inline prompts, prompt templates, YAML or JSON configs, Markdown docs, and saved prompts when they are clearly tied to a model usage site.
2. Pair each model usage with its prompt surface.
   - Prefer the closest prompt surface first: inline system or developer text, then adjacent prompt files, then shared templates.
   - If you cannot confidently tie a prompt to the model usage, say so instead of guessing.
3. Classify the source model family.
   - Common buckets: `gpt-4o` or `gpt-4.1`, `o1` or `o3` or `o4-mini`, early `gpt-5`, later `gpt-5.x`, or mixed and unclear.
4. Decide the upgrade class.
   - `model string only`
   - `model string + light prompt rewrite`
   - `blocked without code changes`
5. Run the no-code compatibility gate.
   - Check whether the current integration can accept `gpt-5.4` without API-surface changes or implementation changes.
   - For long-running Responses or tool-heavy agents, check whether `phase` is already preserved or round-tripped when the host replays assistant items or uses preambles.
   - If compatibility depends on code changes, return `blocked`.
   - If compatibility is unclear, return `unknown` rather than improvising.
6. Recommend the upgrade.
   - Default replacement string: `gpt-5.4`
   - Keep the intervention small and behavior-preserving.
7. Deliver a structured recommendation.
   - `Current model usage`
   - `Recommended model-string updates`
   - `Starting reasoning recommendation`
   - `Prompt updates`
   - `Phase assessment` when the flow is long-running, replayed, or tool-heavy
   - `No-code compatibility check`
   - `Validation plan`
   - `Launch-day refresh items`

Output rule:

- Always emit a starting `reasoning_effort_recommendation` for each usage site.
- If the repo exposes the current reasoning setting, preserve it first unless the source guide says otherwise.
- If the repo does not expose the current setting, use the source-family starting mapping instead of returning `null`.

## Upgrade outcomes

### `model string only`

Choose this when:

- the existing prompts are already short, explicit, and task-bounded
- the workflow is not strongly research-heavy, tool-heavy, multi-agent, batch or completeness-sensitive, or long-horizon
- there are no obvious compatibility blockers

Default action:

- replace the model string with `gpt-5.4`
- keep prompts unchanged
- validate behavior with existing evals or spot checks

### `model string + light prompt rewrite`

Choose this when:

- the old prompt was compensating for weaker instruction following
- the workflow needs more persistence than the default tool-use behavior will likely provide
- the task needs stronger completeness, citation discipline, or verification
- the upgraded model becomes too verbose or under-complete unless instructed otherwise
- the workflow is research-heavy and needs stronger handling of sparse or empty retrieval results
- the workflow is coding-oriented, tool-heavy, or multi-agent, but the existing API surface and tool definitions can remain unchanged

Default action:

- replace the model string with `gpt-5.4`
- add one or two targeted prompt blocks
- read `references/gpt-5p4-prompting-guide.md` to choose the smallest prompt changes that recover the old behavior
- avoid broad prompt cleanup unrelated to the upgrade
- for research workflows, default to `research_mode` + `citation_rules` + `empty_result_handling`; add `tool_persistence_rules` when the host already uses retrieval tools
- for dependency-aware or tool-heavy workflows, default to `tool_persistence_rules` + `dependency_checks` + `verification_loop`; add `parallel_tool_calling` only when retrieval steps are truly independent
- for coding or terminal workflows, default to `terminal_tool_hygiene` + `verification_loop`
- for multi-agent support or triage workflows, default to at least one of `tool_persistence_rules`, `completeness_contract`, or `verification_loop`
- for long-running Responses agents with preambles or multiple assistant messages, explicitly review whether `phase` is already handled; if adding or preserving `phase` would require code edits, mark the path as `blocked`
- do not classify a coding or tool-using Responses workflow as `blocked` just because the visible snippet is minimal; prefer `model string + light prompt rewrite` unless the repo clearly shows that a safe GPT-5.4 path would require host-side code changes

### `blocked`

Choose this when:

- the upgrade appears to require API-surface changes
- the upgrade appears to require parameter rewrites or reasoning-setting changes that are not exposed outside implementation code
- the upgrade would require changing tool definitions, tool handler wiring, or schema contracts
- you cannot confidently identify the prompt surface tied to the model usage

Default action:

- do not improvise a broader upgrade
- report the blocker and explain that the fix is out of scope for this guide

## No-code compatibility checklist

Before recommending a no-code upgrade, check:

1. Can the current host accept the `gpt-5.4` model string without changing client code or API surface?
2. Are the related prompts identifiable and editable?
3. Does the host depend on behavior that likely needs API-surface changes, parameter rewrites, or tool rewiring?
4. Would the likely fix be prompt-only, or would it need implementation changes?
5. Is the prompt surface close enough to the model usage that you can make a targeted change instead of a broad cleanup?
6. For long-running Responses or tool-heavy agents, is `phase` already preserved if the host relies on preambles, replayed assistant items, or multiple assistant messages?

If item 1 is no, items 3 through 4 point to implementation work, or item 6 is no and the fix needs code changes, return `blocked`.

If item 2 is no, return `unknown` unless the user can point to the prompt location.

Important:

- Existing use of tools, agents, or multiple usage sites is not by itself a blocker.
- If the current host can keep the same API surface and the same tool definitions, prefer `model string + light prompt rewrite` over `blocked`.
- Reserve `blocked` for cases that truly require implementation changes, not cases that only need stronger prompt steering.

## Scope boundaries

This guide may:

- update or recommend updated model strings
- update or recommend updated prompts
- inspect code and prompt files to understand where those changes belong
- inspect whether existing Responses flows already preserve `phase`
- flag compatibility blockers

This guide may not:

- move Chat Completions code to Responses
- move Responses code to another API surface
- rewrite parameter shapes
- change tool definitions or tool-call handling
- change structured-output wiring
- add or retrofit `phase` handling in implementation code
- edit business logic, orchestration logic, or SDK usage beyond a literal model-string replacement

If a safe GPT-5.4 upgrade requires any of those changes, mark the path as blocked and out of scope.

## Validation plan

- Validate each upgraded usage site with existing evals or realistic spot checks.
- Check whether the upgraded model still matches expected latency, output shape, and quality.
- If prompt edits were added, confirm each block is doing real work instead of adding noise.
- If the workflow has downstream impact, add a lightweight verification pass before finalization.

## Launch-day refresh items

When final GPT-5.4 guidance changes:

1. Replace release-candidate assumptions with final GPT-5.4 guidance where appropriate.
2. Re-check whether the default target string should stay `gpt-5.4` for all source families.
3. Re-check any prompt-block recommendations whose semantics may have changed.
4. Re-check research, citation, and compatibility guidance against the final model behavior.
5. Re-run the same upgrade scenarios and confirm the blocked-versus-viable boundaries still hold.
