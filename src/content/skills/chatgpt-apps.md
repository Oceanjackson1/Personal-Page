---
title: "Chatgpt Apps"
description: "Build, scaffold, refactor, and troubleshoot ChatGPT Apps SDK applications that combine an MCP server and widget UI. Use when Codex needs to design tools, register UI resources, wire the MCP Apps bridge or ChatGPT compatibility APIs, apply Apps SDK..."
category: "development"
source: "community"
author: "Community"
tags: ["chatgpt", "apps"]
date: 2026-03-20
---

# ChatGPT Apps

## Overview

Scaffold ChatGPT Apps SDK implementations with a docs-first, example-first workflow, then generate code that follows current Apps SDK and MCP Apps bridge patterns.

Use this skill to produce:

- A primary app-archetype classification and repo-shape decision
- A tool plan (names, schemas, annotations, outputs)
- An upstream starting-point recommendation (official example, ext-apps example, or local fallback scaffold)
- An MCP server scaffold (resource registration, tool handlers, metadata)
- A widget scaffold (MCP Apps bridge first, `window.openai` compatibility/extensions second)
- A reusable Node + `@modelcontextprotocol/ext-apps` starter scaffold for low-dependency fallbacks
- A validation report against the minimum working repo contract
- Local dev and connector setup steps
- A short stakeholder summary of what the app does (when requested)

## Mandatory Docs-First Workflow

Use `$openai-docs` first whenever building or changing a ChatGPT Apps SDK app.

1. Invoke `$openai-docs` (preferred) or call the OpenAI docs MCP server directly.
2. Fetch current Apps SDK docs before writing code, especially (baseline pages):
   - `apps-sdk/build/mcp-server`
   - `apps-sdk/build/chatgpt-ui`
   - `apps-sdk/build/examples`
   - `apps-sdk/plan/tools`
   - `apps-sdk/reference`
3. Fetch `apps-sdk/quickstart` when scaffolding a new app or generating a first-pass implementation, and check the official examples repo/page before inventing a scaffold from scratch.
4. Fetch deployment/submission docs when the task includes local ChatGPT testing, hosting, or public launch:
   - `apps-sdk/deploy`
   - `apps-sdk/deploy/submission`
   - `apps-sdk/app-submission-guidelines`
5. Cite the docs URLs you used when explaining design choices or generated scaffolds.
6. Prefer current docs guidance over older repo patterns when they differ, and call out compatibility aliases explicitly.
7. If doc search times out or returns poor matches, fetch the canonical Apps SDK pages directly by URL and continue; do not let search failure block scaffolding.

If `$openai-docs` is unavailable, use:

- `mcp__openaiDeveloperDocs__search_openai_docs`
- `mcp__openaiDeveloperDocs__fetch_openai_doc`

Read `references/apps-sdk-docs-workflow.md` for suggested doc queries and a compact checklist.
Read `references/app-archetypes.md` to classify the request into a small number of supported app shapes before choosing examples or scaffolds.
Read `references/repo-contract-and-validation.md` when generating or reviewing a repo so the output stays inside a stable “working app” contract.
Read `references/search-fetch-standard.md` when the app is connector-like, data-only, sync-oriented, or meant to work well with company knowledge or deep research.
Read `references/upstream-example-workflow.md` when starting a greenfield app or when deciding whether to adapt an upstream example or use the local fallback scaffold.
Read `references/window-openai-patterns.md` when the task needs ChatGPT-specific widget behavior or when translating repo examples that use wrapper-specific `app.*` helpers.

## Prompt Guidance

Use prompts that explicitly pair this skill with `$openai-docs` so the resulting scaffold is grounded in current docs.

Preferred prompt patterns:

- `Use $chatgpt-apps with $openai-docs to scaffold a ChatGPT app for <use case> with a <TS/Python> MCP server and <React/vanilla> widget.`
- `Use $chatgpt-apps with $openai-docs to adapt the closest official Apps SDK example into a ChatGPT app for <use case>.`
- `Use $chatgpt-apps and $openai-docs to refactor this Apps SDK demo into a production-ready structure with tool annotations, CSP, and URI versioning.`
- `Use $chatgpt-apps with $openai-docs to plan tools first, then generate the MCP server and widget code.`

When responding, ask for or infer these inputs before coding:

- Use case and primary user flows
- Read-only vs mutating tools
- Demo vs production target
- Private/internal use vs public directory submission
- Backend language and UI stack
- Auth requirements
- External API domains for CSP allowlists
- Hosting target and local dev approach
- Org ownership/verification readiness (for submission tasks)

## Classify The App Before Choosing Code

Before choosing examples, repo shape, or scaffolds, classify the request into one primary archetype and state it.

- `tool-only`
- `vanilla-widget`
- `react-widget`
- `interactive-decoupled`
- `submission-ready`

Infer the archetype unless a missing detail is truly blocking. Use the archetype to choose:

- whether a UI is needed at all
- whether to preserve a split `server/` + `web/` layout
- whether to prefer official OpenAI examples, ext-apps examples, or the local fallback scaffold
- which validation checks matter most
- whether `search` and `fetch` should be the default read-only tool surface

Read `references/app-archetypes.md` for the decision rubric.

## Default Starting-Point Order

For greenfield apps, prefer these starting points in order:

1. **Official OpenAI examples** when a close example already matches the requested stack or interaction pattern.
2. **Version-matched `@modelcontextprotocol/ext-apps` examples** when the user needs a lower-level or more portable MCP Apps baseline.
3. **`scripts/scaffold_node_ext_apps.mjs`** only when no close example fits, the user wants a tiny Node + vanilla starter, or network access/example retrieval is undesirable.

Do not generate a large custom scaffold from scratch if a close upstream example already exists.
Copy the smallest matching example, remove unrelated demo code, then patch it to the current docs and the user request.

## Build Workflow

### 0. Classify The App Archetype

Pick one primary archetype before planning tools or choosing a starting point.

- Prefer a single primary archetype instead of mixing several.
- If the request is broad, infer the smallest archetype that can still satisfy it.
- Escalate to `submission-ready` only when the user asks for public launch, directory submission, or review-ready deployment.
- Call out the chosen archetype in your response so the user can correct it early if needed.

### 1. Plan Tools Before Code

Define the tool surface area from user intents.

- Use one job per tool.
- Write tool descriptions that start with "Use this when..." behavior cues.
- Make inputs explicit and machine-friendly (enums, required fields, bounds).
- Decide whether each tool is data-only, render-only, or both.
- Set annotations accurately (`readOnlyHint`, `destructiveHint`, `openWorldHint`; add `idempotentHint` when true).
- If the app is connector-like, data-only, sync-oriented, or intended for company knowledge or deep research, default to the standard `search` and `fetch` tools instead of inventing custom read-only equivalents.
- For educational/demo apps, prefer one concept per tool so the model can pick the right example cleanly.
- Group demo tools by learning objective: data into the widget, widget actions back into the conversation or tools, host/layout environment signals, and lifecycle/streaming behavior.

Read `references/search-fetch-standard.md` when `search` and `fetch` may be relevant.

### 2. Choose an App Architecture

Choose the simplest structure that fits the goal.

- Use a **minimal demo pattern** for quick prototypes, workshops, or proofs of concept.
- Use a **decoupled data/render pattern** for production UX so the widget does not re-render on every tool call.

Prefer the decoupled pattern for non-trivial apps:

- Data tools return reusable `structuredContent`.
- Render tools attach `_meta.ui.resourceUri` and optional `_meta["openai/outputTemplate"]`.
- Render tool descriptions state prerequisites (for example, "Call `search` first").

### 2a. Start From An Upstream Example When One Fits

Default to upstream examples for greenfield work when they are close to the requested app.

- Check the official OpenAI examples first for ChatGPT-facing apps, polished UI patterns, React components, file upload flows, modal flows, or apps that resemble the docs examples.
- Use `@modelcontextprotocol/ext-apps` examples when the request is closer to raw MCP Apps bridge/server wiring, or when version-matched package patterns matter more than ChatGPT-specific polish.
- Pick the smallest matching example and copy only the relevant files; do not transplant an entire showcase app unchanged.
- After copying, reconcile the example with the current docs you fetched: tool names/descriptions, annotations, `_meta.ui.*`, CSP, URI versioning, and local run instructions.
- State which example you chose and why in one sentence.

Read `references/upstream-example-workflow.md` for the selection and adaptation rubric.

### 2b. Use the Starter Script When a Low-Dependency Fallback Helps

Use `scripts/scaffold_node_ext_apps.mjs` only when the user wants a quick, greenfield Node starter and a vanilla HTML widget is acceptable, and no upstream example is a better starting point.

- Run it only after fetching current docs, then reconcile the generated files with the docs you fetched.
- If you choose the script instead of an upstream example, say why the fallback is better for that request.
- Skip it when a close official example exists, when the user already has an existing app structure, when they need a non-Node stack, when they explicitly want React first, or when they only want a plan/review instead of code.
- The script generates a minimal `@modelcontextprotocol/ext-apps` server plus a vanilla HTML widget that uses the MCP Apps bridge by default.
- The generated widget keeps follow-up messaging on the standard `ui/message` bridge and only uses `window.openai` for optional host signals/extensions.
- After running it, patch the generated output to match the current docs and the user request: adjust tool names/descriptions, annotations, resource metadata, URI versioning, and README/run instructions.

### 3. Scaffold the MCP Server

Generate a server that:

- Registers a widget resource/template with the MCP Apps UI MIME type (`text/html;profile=mcp-app`) or the SDK constant (`RESOURCE_MIME_TYPE`) when using `@modelcontextprotocol/ext-apps/server`
- Registers tools with clear names, schemas, titles, and descriptions
- Returns `structuredContent` (model + widget), `content` (model narration), and `_meta` (widget-only data) intentionally
- Keeps handlers idempotent or documents non-idempotent behavior explicitly
- Includes tool status strings (`openai/toolInvocation/*`) when helpful in ChatGPT

Keep `structuredContent` concise. Move large or sensitive widget-only payloads to `_meta`.

### 4. Scaffold the Widget UI

Use the MCP Apps bridge first for portability, then add ChatGPT-specific `window.openai` APIs when they materially improve UX.

- Listen for `ui/notifications/tool-result` (JSON-RPC over `postMessage`)
- Render from `structuredContent`
- Use `tools/call` for component-initiated tool calls
- Use `ui/update-model-context` only when UI state should change what the model sees

Use `window.openai` for compatibility and extensions (file upload, modal, display mode, etc.), not as the only integration path for new apps.

#### API Surface Guardrails

- Some examples wrap the bridge with an `app` object (for example, `@modelcontextprotocol/ext-apps/react`) and expose helper names like `app.sendMessage()`, `app.callServerTool()`, `app.openLink()`, or host getter methods.
- Treat those wrappers as implementation details or convenience layers, not the canonical public API to teach by default.
- For ChatGPT-facing guidance, prefer the current documented surface: `window.openai.callTool(...)`, `window.openai.sendFollowUpMessage(...)`, `window.openai.openExternal(...)`, `window.openai.requestDisplayMode(...)`, and direct globals like `window.openai.theme`, `window.openai.locale`, `window.openai.displayMode`, `window.openai.toolInput`, `window.openai.toolOutput`, `window.openai.toolResponseMetadata`, and `window.openai.widgetState`.
- If you reference wrapper helpers from repo examples, map them back to the documented `window.openai` or MCP Apps bridge primitives and call out that the wrapper is not the normative API surface.
- Use `references/window-openai-patterns.md` for the wrapper-to-canonical mapping and for React helper extraction patterns.

### 5. Add Resource Metadata and Security

Set resource metadata deliberately on the widget resource/template:

- `_meta.ui.csp` with exact `connectDomains` and `resourceDomains`
- `_meta.ui.domain` for app submission-ready deployments
- `_meta.ui.prefersBorder` (or OpenAI compatibility alias when needed)
- Optional `openai/widgetDescription` to reduce redundant narration

Avoid `frameDomains` unless iframe embeds are core to the product.

### 5a. Enforce A Minimum Working Repo Contract

Every generated repo should satisfy a small, stable contract before you consider it done.

- The repo shape matches the chosen archetype.
- The MCP server and tools are wired to a reachable `/mcp` endpoint.
- Tools have clear descriptions, accurate annotations, and UI metadata where needed.
- Connector-like, data-only, sync-oriented, and company-knowledge-style apps use the standard `search` and `fetch` tool shapes when relevant.
- The widget uses the MCP Apps bridge correctly when a UI exists.
- The repo includes enough scripts or commands for a user to run and check it locally.
- The response explicitly says what validation was run and what was not run.

Read `references/repo-contract-and-validation.md` for the detailed checklist and validation ladder.

### 6. Validate the Local Loop

Validate against the minimum working repo contract, not just “did files get created.”

- Run the lowest-cost checks first:
  - static contract review
  - syntax or compile checks when feasible
  - local `/mcp` health check when feasible
- Then move up to runtime checks:
  - verify tool descriptors and widget rendering in MCP Inspector
  - test the app in ChatGPT developer mode through HTTPS tunneling
  - exercise retries and repeated tool calls to confirm idempotent behavior
  - check widget updates after host events and follow-up tool calls
- If you are only delivering a scaffold and are not installing dependencies, still run low-cost checks and say exactly what you did not run.

Read `references/repo-contract-and-validation.md` for the validation ladder.

### 7. Connect and Test in ChatGPT (Developer Mode)

For local development, include explicit ChatGPT setup steps (not just code/run commands).

- Run the MCP server locally on `http://localhost:<port>/mcp`
- Expose the local server with a public HTTPS tunnel (for example `ngrok http <port>`)
- Use the tunneled HTTPS URL plus `/mcp` path when connecting from ChatGPT
- In ChatGPT, enable Developer Mode under **Settings → Apps & Connectors → Advanced settings**
- In ChatGPT app settings, create a new app for the remote MCP server and paste the public MCP URL
- Tell users to refresh the app after MCP tool/metadata changes so ChatGPT reloads the latest descriptors

Note: Some docs/screenshots still use older "connector" terminology. Prefer current product wording ("app") while acknowledging both labels when giving step-by-step instructions.

### 8. Plan Production Hosting and Deployment

When the user asks to deploy or prepare for launch, generate hosting guidance for the MCP server (and widget assets if hosted separately).

- Host behind a stable public HTTPS endpoint (not a tunnel) with dependable TLS
- Preserve low-latency streaming behavior on `/mcp`
- Configure secrets outside the repo (environment variables / secret manager)
- Add logging, request latency tracking, and error visibility for tool calls
- Add basic observability (CPU, memory, request volume) and a troubleshooting path
- Re-test the hosted endpoint in ChatGPT Developer Mode before submission

### 9. Prepare Submission and Publish (Public Apps Only)

Only include these steps when the user intends a public directory listing.

- Use `apps-sdk/deploy/submission` for the submission flow and `apps-sdk/app-submission-guidelines` for review requirements
- Keep private/internal apps in Developer Mode instead of submitting
- Confirm org verification and Owner-role prerequisites before submission work
- Ensure the MCP server uses a public production endpoint (no localhost/testing URLs) and has submission-ready CSP configured
- Prepare submission artifacts: app metadata, logo/screenshots, privacy policy URL, support contact, test prompts/responses, localization info
- If auth is required, include review-safe demo credentials and test the login path end-to-end
- Submit for review in the Platform dashboard, monitor review status, and publish only after approval

## Interactive State Guidance

Read `references/interactive-state-sync-patterns.md` when the app has long-lived widget state, repeated interactions, or component-initiated tool calls (for example, games, boards, maps, dashboards, editors).

Use it to choose patterns for:

- State snapshots plus monotonic event tokens (`stateVersion`, `resetCount`, etc.)
- Idempotent retry-safe handlers
- `structuredContent` vs `_meta` partitioning
- MCP Apps bridge-first update flows with optional `window.openai` compatibility
- Decoupled data/render tool architecture for more complex interactive apps

## Output Expectations

When using this skill to scaffold code, produce output in this order unless the user asks otherwise:

- For direct scaffold requests, do not stop at the plan: give the brief plan, then create the files immediately.

1. Primary app archetype chosen and why
2. Tool plan and architecture choice (minimal vs decoupled)
3. Upstream starting point chosen (official example, ext-apps example, or local fallback scaffold) and why
4. Doc pages/URLs used from `$openai-docs`
5. File tree to create or modify
6. Implementation (server + widget)
7. Validation performed against the minimum working repo contract
8. Local run/test instructions (including tunnel + ChatGPT Developer Mode app setup)
9. Deployment/hosting guidance (if requested or implied)
10. Submission-readiness checklist (for public launch requests)
11. Risks, gaps, and follow-up improvements

## References

- `references/app-archetypes.md` for classifying requests into a small number of supported app shapes
- `references/apps-sdk-docs-workflow.md` for doc queries, page targets, and code-generation checklist
- `references/interactive-state-sync-patterns.md` for reusable patterns for stateful or highly interactive widget apps
- `references/repo-contract-and-validation.md` for the minimum working repo contract and lightweight validation ladder
- `references/search-fetch-standard.md` for when and how to default to the standard `search` and `fetch` tools
- `references/upstream-example-workflow.md` for choosing between official examples, ext-apps examples, and the local fallback scaffold
- `references/window-openai-patterns.md` for ChatGPT-specific extensions, wrapper API translation, and React helper patterns
- `scripts/scaffold_node_ext_apps.mjs` for a minimal Node + `@modelcontextprotocol/ext-apps` fallback starter scaffold

---

## Reference: App Archetypes

# App Archetypes

Load this reference before choosing a starting point for a new ChatGPT app. The goal is to keep the skill inside a small number of supported app shapes instead of inventing a custom structure for every prompt.

## Rule

Choose one primary archetype per request and state it.

Do not combine several archetypes unless the user explicitly asks for a hybrid app and the extra complexity is necessary.

## Archetypes

### `tool-only`

Use when:

- The user does not need an in-ChatGPT UI
- The task is mainly search, fetch, retrieval, or background actions

Default shape:

- MCP server only

Best starting point:

- Official docs and MCP server examples

Validation emphasis:

- `/mcp` route works
- tool schemas and annotations are correct
- no unnecessary UI resource is registered
- if the app is connector-like or sync-oriented, `search` and `fetch` should be the default read-only tools

### `vanilla-widget`

Use when:

- The user wants a small demo, workshop starter, or simple inline widget
- A single HTML widget is enough
- The user wants the fastest path to a working repo

Default shape:

- Root-level server plus `public/` widget assets

Best starting point:

- Apps SDK quickstart first
- Local fallback scaffold if the quickstart is not a good fit

Validation emphasis:

- bridge initialization
- `ui/notifications/tool-result`
- `tools/call` only when the widget is interactive

### `react-widget`

Use when:

- The user wants a polished UI
- The UI is clearly component-based
- The user mentions React, TypeScript frontend tooling, or richer design requirements

Default shape:

- Split `server/` + `web/` layout when the example already uses it

Best starting point:

- Official OpenAI examples

Validation emphasis:

- build output is wired into the server correctly
- bundle references resolve
- widget renders from `structuredContent`

### `interactive-decoupled`

Use when:

- The app has repeated user interaction
- The widget should stay mounted while tools are called repeatedly
- The app is a board, map, editor, game, dashboard, or other stateful experience

Default shape:

- Split `server/` + `web/`
- data tools plus render tools

Best starting point:

- Official OpenAI examples plus `references/interactive-state-sync-patterns.md`

Validation emphasis:

- tool retries are safe
- widget does not remount unnecessarily
- state sync is intentional
- UI tool calls work independently of model reruns

### `submission-ready`

Use when:

- The user asks for public launch, review readiness, or directory submission

Default shape:

- Smallest viable repo that still includes deployment and review requirements

Best starting point:

- Closest official example that matches the requested stack

Validation emphasis:

- `_meta.ui.domain`
- accurate CSP
- auth and review-safe flows
- submission prerequisites and artifacts

## Selection Heuristic

- If the prompt does not mention a UI, choose `tool-only`.
- If the prompt is about a knowledge source, sync app, connector-like integration, or deep research, strongly prefer `tool-only` plus the standard `search` and `fetch` tools unless the user clearly needs a widget.
- If the prompt asks for a simple demo or starter, choose `vanilla-widget`.
- If the prompt asks for a polished UI or React, choose `react-widget`.
- If the prompt implies long-lived client state or repeated interaction, choose `interactive-decoupled`.
- Only choose `submission-ready` when the user explicitly asks for launch or review-readiness work.

---

## Reference: Apps Sdk Docs Workflow

# Apps SDK Docs Workflow

Use this reference to keep code generation aligned with current OpenAI Apps SDK docs.

## Always Fetch These Pages (Baseline)

- `https://developers.openai.com/apps-sdk/build/mcp-server/`
- `https://developers.openai.com/apps-sdk/build/chatgpt-ui/`
- `https://developers.openai.com/apps-sdk/build/examples/`
- `https://developers.openai.com/apps-sdk/plan/tools/`
- `https://developers.openai.com/apps-sdk/reference/`

## Fetch Conditionally (Greenfield / First Pass)

- `https://developers.openai.com/apps-sdk/quickstart/` for first implementation scaffolds and happy-path wiring
- `https://developers.openai.com/apps-sdk/deploy/` when the task includes local ChatGPT testing via tunnel, hosting, or production deployment planning
- `https://developers.openai.com/apps-sdk/deploy/submission/` when the task includes public launch, app review, or publishing steps
- `https://developers.openai.com/apps-sdk/app-submission-guidelines/` when the task includes submission readiness, policy/reliability checks, or review-risk reduction

## Suggested `openai-docs` / MCP Queries

Use focused searches before fetching:

- `ChatGPT Apps SDK build MCP server register resource template resourceUri outputTemplate`
- `ChatGPT Apps SDK build ChatGPT UI MCP Apps bridge ui/notifications/tool-result`
- `ChatGPT Apps SDK examples React widget upload modal Pizzaz`
- `Apps SDK define tools annotations readOnlyHint destructiveHint openWorldHint`
- `Apps SDK reference tool descriptor _meta ui.resourceUri openai/outputTemplate`
- `ChatGPT Apps SDK quickstart build web component tools/call`
- `ChatGPT app company knowledge compatibility search fetch tools`
- `platform MCP search tool fetch tool schema`
- `ChatGPT Apps SDK deploy app local development tunnel ngrok refresh connector`
- `ChatGPT Apps SDK submit app review prerequisites app submission guidelines`

## Docs-Derived Checklist (Current Guidance)

### Archetype / Shape

- Classify the request into one primary app archetype before choosing examples or scaffolds
- Keep the repo shape consistent with that archetype instead of inventing a new structure for each prompt

### Server

- Register the widget resource/template with the MCP Apps UI MIME type (`text/html;profile=mcp-app`) or `RESOURCE_MIME_TYPE` when using `@modelcontextprotocol/ext-apps/server`
- Version template URIs when widget HTML or JS or CSS changes in a breaking way (treat URI as cache key)
- Set `_meta.ui.resourceUri` on render tools; optionally mirror `_meta["openai/outputTemplate"]` for ChatGPT compatibility
- Design tool handlers to be idempotent because the model may retry calls
- Keep `structuredContent` concise and move widget-only payloads to `_meta`

### Tool Design

- Plan one user intent per tool
- Use action-oriented names and precise descriptions
- Set tool impact hints accurately (`readOnlyHint`, `destructiveHint`, `openWorldHint`)
- Split data and render tools so that the model can fetch the data and look at it before choosing to render the widget UI or not
- Make the widget input a list of unique identifiers (e.g. `propertyIds` for a render property map widget that takes IDs returned from the fetch properties nearby tool) if you want to make sure the widget only renders 1p data; make the widget input semantically relevant if you want to allow the model to render the widget with generated data (e.g. `questionAndAnswerPairs` for a flashcards widget)
- For connector-like, data-only, sync-oriented, or company-knowledge-style apps, prefer the standard `search` and `fetch` tools by default

### UI

- Prefer the MCP Apps bridge (`ui/*` notifications + `tools/call`) for new apps
- Prefer `ui/message` for follow-up messaging in baseline examples; treat `window.openai.sendFollowUpMessage` as optional ChatGPT-specific compatibility
- Treat `window.openai` as compatibility plus optional ChatGPT extensions
- Render from `structuredContent` and treat host-delivered data as untrusted input
- Use `ui/update-model-context` only for UI state the model should reason about

### Starting Point Selection

- Check `apps-sdk/build/examples` and the official examples repo before generating a greenfield scaffold from scratch
- Prefer the smallest upstream example that matches the requested stack and interaction pattern
- Use the local fallback scaffold only when upstream examples are a poor fit or undesirable for the request

### Resource Metadata / Security

- Set `_meta.ui.csp.connectDomains` and `_meta.ui.csp.resourceDomains` exactly
- Avoid `frameDomains` unless iframe embedding is central to the experience
- Set `_meta.ui.domain` for submission-ready apps
- Always set `openai/widgetDescription` to inform the model what the widget is to be used for

### Developer Mode / Local Testing

- Run the MCP server locally on `http://localhost:<port>/mcp`
- Expose it with a public HTTPS tunnel for ChatGPT access during development
- Use the public URL + `/mcp` when adding the app in ChatGPT settings
- Include ChatGPT Developer Mode setup and app creation steps in implementation handoff
- Remind users to refresh the app after MCP tool/metadata changes
- Note terminology differences when relevant: some docs/screenshots may still say "connector" while product UI uses "app"

### Validation

- Validate against a minimum working repo contract, not just file creation
- Run the cheapest useful syntax or compile check first
- If feasible, confirm the local `/mcp` route responds before calling the result “working”
- If you cannot run a deeper check, say so explicitly
- If the app is connector-like or sync-oriented, verify the `search` and `fetch` tool shapes against the standard

### Production Hosting / Deploy

- Prefer a stable public HTTPS endpoint with reliable TLS and low-latency streaming `/mcp`
- Document platform-specific secrets handling and environment variables
- Include logging/metrics expectations for debugging production tool calls
- Re-test the hosted endpoint in ChatGPT Developer Mode before submission

### Submission / Review

- Read `deploy/submission` and `app-submission-guidelines` together (process + policy requirements)
- Check org verification and Owner-role prerequisites before generating submission steps
- Ensure the endpoint is public production infrastructure (not localhost/tunnel/testing URLs)
- Ensure CSP is defined and accurate for submission
- Prepare submission artifacts (metadata, screenshots, privacy policy/support contacts, test prompts/responses)
- If auth is required, prepare review-safe demo credentials and validate them outside internal networks

## Generation Pattern

1. Classify the app archetype.
2. Fetch docs with `$openai-docs`.
3. Check official examples before inventing a scaffold from scratch.
4. Summarize relevant constraints and metadata keys.
5. Propose tool plan and architecture.
6. Adapt the closest example or use the local fallback scaffold.
7. Generate or patch the server scaffold.
8. Generate or patch the widget scaffold.
9. Validate the repo against the minimum working contract.
10. Add local run + tunnel + ChatGPT Developer Mode app setup instructions.
11. Add hosting/deployment guidance when the task implies go-live.
12. Add submission/readiness steps when the user intends public distribution.
13. Call out compatibility aliases vs MCP Apps standard fields.

## Starter Scaffold Script

- Use `./scripts/scaffold_node_ext_apps.mjs <output-dir> --app-name <name>` only when the user wants a greenfield Node + `@modelcontextprotocol/ext-apps` starter and no upstream example is the better fit.
- If the file is not executable in the current environment, fall back to `node scripts/scaffold_node_ext_apps.mjs <output-dir> --app-name <name>`.
- The script generates `package.json`, `tsconfig.json`, `public/widget.html`, and `src/server.ts`.
- It intentionally uses the MCP Apps bridge by default, keeps follow-up messaging on `ui/message`, and limits `window.openai` to optional host signals/extensions.
- After generation, compare the output against the docs you fetched and adjust package versions, metadata, transport details, or URI/versioning if the docs changed.

---

## Reference: Interactive State Sync Patterns

# Interactive State Sync Patterns

Use this reference when building ChatGPT apps with long-lived widget state, repeated interactions, or component-initiated tool calls (for example: games, boards, maps, dashboards, editors, or realtime-ish UIs).

Do not load this file for simple read-only render apps unless state sync behavior is part of the task.

## When This Reference Helps

Read this file when the app needs one or more of these patterns:

- Repeated actions that may return similar data (retry, refresh, reset, reroll)
- UI controls that trigger tool calls after the initial render
- Local widget behavior that should also work outside ChatGPT during development
- Multiple tool calls updating one mounted widget over time
- Clear separation between model-visible state and widget-only state

## Reusable Patterns

### 1. Snapshot + Event Token

Return a stable state snapshot in `structuredContent` and add a monotonic event token for repeated actions that may not change other fields.

Examples:

- `stateVersion`
- `refreshCount`
- `resetCount`
- `lastMutationId`

Use this when the widget must detect "same shape, new event" updates reliably.

### 2. Intent-Focused Tool Surface

Prefer small, explicit tools that map to user-visible actions or data operations.

- Keep names action-oriented
- Use enums and bounded schemas where possible
- Avoid kitchen-sink tools that mix unrelated reads and writes

This improves model tool selection and reduces malformed calls.

### 3. Idempotent Handlers (or Explicitly Non-Idempotent)

Design handlers to tolerate retries. If a tool is not idempotent, make the side effect explicit and confirm intent in the flow.

- Reads and pure transforms should usually be idempotent
- Writes should include clear impact hints and current-turn confirmation where needed
- Repeated calls with the same input should not corrupt widget state

### 4. `structuredContent` / `_meta` Partitioning

Partition payloads intentionally:

- `structuredContent`: concise model-visible state the widget also uses
- `content`: short narration/status text
- `_meta`: large maps, caches, or sensitive widget-only hydration data

Keep `structuredContent` small enough for follow-up reasoning and chaining.

### 5. MCP Apps Bridge First, `window.openai` Second

For new scaffolds:

- Prefer MCP Apps bridge notifications and `tools/call` (portable across hosts)
- Use `window.openai` as a compatibility layer plus optional ChatGPT extensions

This keeps the app portable while still enabling ChatGPT-specific capabilities when helpful.

### 6. Component-Initiated Tool Calls Without Remounting

For interactive widgets, allow the UI to call data/action tools directly and update the existing widget state instead of forcing a full re-render/remount every time.

This is especially useful for:

- Refresh
- Retry
- Rerun
- Toggle/filter actions
- Incremental interactions inside one widget session

### 7. Standalone / No-Host Fallback Mode

When feasible, make the widget usable without ChatGPT during development:

- If host APIs are unavailable, apply local state directly
- Preserve basic interactions in a normal browser

This speeds up front-end iteration and reduces dependence on connector setup for every UI tweak.

### 8. Decouple Data Tools from Render Tools (When Complexity Grows)

Use separate data and render tools when the app has multi-step reasoning or frequent updates.

- Data tools fetch/compute/mutate and return reusable `structuredContent`
- Render tools attach the widget template and focus on presentation

This reduces unnecessary remounts and gives the model a chance to refine data before rendering.

## Common Anti-Patterns

- Putting large widget-only blobs into `structuredContent`
- Attaching a widget template to every tool when only one render tool needs it
- Using hidden client-side state as the source of truth for critical actions
- Depending only on `window.openai` APIs for baseline app behavior
- Using ambiguous tool names that do not match user intent

## Example App Types That Benefit From These Patterns

- Multiplayer or turn-based games
- Collaborative boards / task views
- Maps with filters and repeated searches
- Dashboards with refresh and drill-down actions
- Editors or builders with iterative tool calls

---

## Reference: Repo Contract And Validation

# Repo Contract And Validation

Load this reference when scaffolding or reviewing a generated ChatGPT app repo.

The goal is not “files were created.” The goal is “the repo is plausibly runnable and follows a stable working-app contract.”

## Minimum Working Repo Contract

Every generated repo should satisfy the relevant parts of this contract.

### 1. Shape

- The repo shape matches the chosen archetype.
- The repo structure is simple enough that a user can identify where the server and widget live.

### 2. Server

- There is a clear MCP server entry point.
- The server exposes `/mcp`.
- The server registers tools intentionally.
- If a UI exists, the server registers a resource/template with the MCP Apps UI MIME type.

### 3. Tools

- Each tool maps to one user intent.
- Descriptions help the model choose the tool.
- Required annotations are present and accurate.
- UI-linked tools use `_meta.ui.resourceUri`.
- `_meta["openai/outputTemplate"]` is treated as optional compatibility, not the primary contract.
- When the app is connector-like, data-only, sync-oriented, or intended for company knowledge or deep research, it implements standard `search` and `fetch` tools instead of custom substitutes.

### 4. Widget

- The widget initializes the MCP Apps bridge when needed.
- The widget can receive `ui/notifications/tool-result`.
- The widget renders from `structuredContent`.
- Interactive widgets use `tools/call`.
- Baseline follow-up messaging uses `ui/message`.
- `window.openai` is optional and additive.

### 5. Local Developer Experience

- There is a clear way to start the app locally.
- There is at least one low-cost check command when the stack supports it.
- The response explains how to connect the app in ChatGPT Developer Mode when relevant.

## Validation Ladder

Run the highest level you can without overfitting to a single stack.

### Level 0: Static contract review

Check for:

- chosen archetype is sensible
- repo shape matches archetype
- `/mcp` route is present
- tool/resource/widget responsibilities are coherent
- if the app is connector-like or sync-oriented, `search` and `fetch` are present with the expected standard shape

### Level 1: Syntax or compile checks

Use the stack-appropriate cheapest check available, for example:

- Python syntax check
- TypeScript compile check
- framework-specific lint or build sanity check if already installed

### Level 2: Local runtime sanity

If feasible:

- start the server
- confirm the health route or `/mcp` endpoint responds

### Level 3: Host loop validation

If feasible:

- inspect with MCP Inspector
- test through ChatGPT Developer Mode
- confirm widget updates after tool results

## Reporting Rule

Always say which validation level was reached and what was not run.

That makes the skill more reliable because it separates:

- “repo shape looks right”
- “syntax is valid”
- “server starts”
- “host integration was actually exercised”

---

## Reference: Search Fetch Standard

# Search And Fetch Standard

Load this reference when the app is connector-like, data-only, sync-oriented, or meant to work well with company knowledge or deep research.

## Default Rule

If the app is primarily a read-only knowledge source, do not invent custom equivalents to `search` and `fetch`.

Default to implementing the standard `search` and `fetch` tools exactly, then add other tools only if the use case clearly needs them.

## When This Applies

Use the standard by default when the request is about:

- a data-only app
- a sync app
- a company knowledge source
- deep research compatibility
- a connector-like integration over documents, tickets, wiki pages, CRM records, or similar read-only data

## Tool Requirements

### `search`

- Read-only tool
- Takes a single query string
- Returns exactly one MCP content item with `type: "text"`
- That text is a JSON-encoded object with:
  - `results`
  - each result has `id`, `title`, and `url`

### `fetch`

- Read-only tool
- Takes a single document/item id string
- Returns exactly one MCP content item with `type: "text"`
- That text is a JSON-encoded object with:
  - `id`
  - `title`
  - `text`
  - `url`
  - optional `metadata`

## Implementation Rules

- Match the schema exactly when the app is intended for company knowledge or deep research compatibility.
- Use canonical `url` values for citations.
- Mark these tools as read-only.
- Prefer these names exactly: `search` and `fetch`.
- If you add other read-only tools, they should complement the standard rather than replace it.

## Validation Checks

When `search` and `fetch` are relevant, verify:

- both tools exist
- they are read-only
- their input shapes match the standard
- their returned payloads are wrapped as one `content` item with JSON-encoded `text`
- result URLs are canonical enough for citation use

## Source

This standard is described in:

- `https://developers.openai.com/apps-sdk/build/mcp-server/#company-knowledge-compatibility`
- `https://platform.openai.com/docs/mcp`

---

## Reference: Upstream Example Workflow

# Upstream Example Workflow

Load this reference when starting a greenfield ChatGPT app or when deciding whether to adapt an upstream example or use the local fallback scaffold.

## Default Order

Prefer these starting points in order:

1. Official OpenAI Apps SDK examples
2. Version-matched `@modelcontextprotocol/ext-apps` examples
3. Local `scripts/scaffold_node_ext_apps.mjs` fallback

This keeps the skill aligned with current docs and maintained example code while still preserving a low-dependency fallback when examples are not a good fit.

## Choose The Right Source

### 1. Official OpenAI examples

Prefer these when:

- The app is clearly ChatGPT-facing
- The user wants a polished UI or React component
- The task involves file upload, modal flows, display-mode changes, or other ChatGPT extensions
- The docs/examples page already shows a similar interaction pattern

Typical sources:

- `https://developers.openai.com/apps-sdk/build/examples/`
- `https://github.com/openai/openai-apps-sdk-examples`
- `https://developers.openai.com/apps-sdk/quickstart/` for the smallest vanilla baseline

### 2. `@modelcontextprotocol/ext-apps` examples

Prefer these when:

- The user needs a lower-level MCP Apps baseline
- Portability across MCP Apps-compatible hosts matters more than ChatGPT-specific polish
- You want version-matched examples close to the installed `@modelcontextprotocol/ext-apps` package shape

This follows the same basic idea as the upstream `create-mcp-app` skill: use maintained examples as the starting point, then adapt them.

Typical examples from upstream flows:

- `examples/demo-vanilla-html`
- `examples/demo-react-simple`
- `examples/demo-connectors-api`

### 3. Local fallback scaffold

Use `scripts/scaffold_node_ext_apps.mjs` when:

- No close upstream example exists
- The user wants a tiny Node + vanilla HTML starter
- Network/example retrieval is undesirable
- You need a throwaway starter to patch quickly during a live coding task

Do not prefer the local scaffold just because it is available. It is the fallback, not the default.

## Adaptation Rules

- Copy the smallest matching example, not the entire showcase app.
- Remove unrelated demo tools, assets, and routes immediately.
- Keep the upstream file structure when it is already clean and docs-aligned.
- Reconcile the copied example with the current docs before finishing:
  - tool names and descriptions
  - annotations (`readOnlyHint`, `destructiveHint`, `openWorldHint`, `idempotentHint` when true)
  - `_meta.ui.resourceUri` and optional `_meta["openai/outputTemplate"]`
  - resource `_meta.ui.csp`, `_meta.ui.domain`, and `openai/widgetDescription`
  - URI versioning for template changes
  - local run/test instructions
- State which example you chose and why.
- If you rely on upstream code, note the source repo and branch/tag/commit when practical; avoid silently depending on a floating example shape for long-lived work.

## Minimal Selection Heuristic

- If the user asks for **React + polished UI**, start with official OpenAI examples.
- If the user asks for **vanilla HTML + tiny demo**, start with the quickstart example; use the local fallback scaffold only if the quickstart is still too opinionated or unavailable.
- If the user asks for **portable MCP Apps wiring**, start with `@modelcontextprotocol/ext-apps` examples.
- If the user already has an app, adapt their code directly instead of importing a new example.

---

## Reference: Window Openai Patterns

# Window.openai Patterns

Load this reference when a task needs ChatGPT-only widget features, when translating older examples that use an `app` wrapper, or when a React widget should read host globals safely.

## Core Rule

- Build baseline widget behavior on the MCP Apps bridge: `ui/*` notifications, `tools/call`, `ui/message`, and `ui/update-model-context`.
- Use `window.openai` only when the task specifically benefits from ChatGPT-only runtime conveniences.
- Treat `window.openai` as additive. The app should still have a coherent baseline path on the MCP Apps standard when possible.

## Canonical `window.openai` Surface

### State And Data

- `window.openai.toolInput`: tool arguments supplied by the host
- `window.openai.toolOutput`: current `structuredContent`
- `window.openai.toolResponseMetadata`: current `_meta` payload (widget-only)
- `window.openai.widgetState`: persisted widget-local snapshot
- `window.openai.setWidgetState(state)`: persist widget-local snapshot after meaningful UI changes

### Runtime APIs

- `window.openai.callTool(name, args)`: call another MCP tool from the widget
- `window.openai.sendFollowUpMessage({ prompt, scrollToBottom? })`: ask ChatGPT to post a widget-authored follow-up message
- `window.openai.openExternal({ href, redirectUrl? })`: open an external URL through ChatGPT's vetted flow
- `window.openai.requestDisplayMode({ mode })`: request `inline`, `pip`, or `fullscreen`
- `window.openai.requestModal({ params, template? })`: open a host-owned modal
- `window.openai.requestClose()`: ask ChatGPT to close the widget
- `window.openai.uploadFile(file)`: upload a file from the widget
- `window.openai.getFileDownloadUrl({ fileId })`: resolve a temporary download URL
- `window.openai.notifyIntrinsicHeight(...)`: report dynamic height changes
- `window.openai.setOpenInAppUrl({ href })`: override the fullscreen punch-out target

### Context Signals

- `window.openai.theme`
- `window.openai.displayMode`
- `window.openai.maxHeight`
- `window.openai.safeArea`
- `window.openai.view`
- `window.openai.userAgent`
- `window.openai.locale`

## Mapping From Repo Wrapper Examples

- `app.callServerTool({ name, arguments })`:
  Use `window.openai.callTool(name, args)` when you intentionally want the ChatGPT compatibility layer.
  Use `tools/call` over the bridge when you want the portable MCP Apps path.
- `app.sendMessage(...)`:
  Use `ui/message` for portable bridge messaging.
  If the task is intentionally ChatGPT-specific, `window.openai.sendFollowUpMessage({ prompt })` is the closest supported path.
- `app.updateModelContext(...)`:
  Use `ui/update-model-context` over the bridge.
  This is part of the standard bridge, not a `window.openai` feature.
- `app.openLink({ url })`:
  Use `window.openai.openExternal({ href: url })` when you intentionally want ChatGPT's external navigation flow.
- `app.requestDisplayMode({ mode })`:
  Use `window.openai.requestDisplayMode({ mode })`.
- `app.getHostContext()`:
  Read the documented globals directly (`theme`, `displayMode`, `locale`, `maxHeight`, `safeArea`, `userAgent`).
- `app.getHostCapabilities()` / `app.getHostVersion()`:
  These are wrapper-level convenience APIs.
  Prefer feature detection (`if (window.openai?.requestModal)`) and the documented globals instead of teaching these as the primary public surface.

## React Helper Extraction

- The repo's `src/use-openai-global.ts` is a good baseline for subscribing to host global changes without scattering direct `window.openai` reads through components.
- The repo's `src/use-widget-state.ts` is a good baseline for mirroring React state into `window.openai.setWidgetState(...)`.
- The repo's `src/use-widget-props.ts` is a good baseline for reading typed `toolOutput` with a local fallback.
- Keep these helpers optional. Do not force a React abstraction when a simple vanilla widget is enough.
