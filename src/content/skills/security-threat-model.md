---
title: "Security Threat Model"
description: "Repository-grounded threat modeling that enumerates trust boundaries, assets, attacker capabilities, abuse paths, and mitigations, and writes a concise Markdown threat model. Trigger only when the user explicitly asks to threat model a codebase or..."
category: "development"
source: "community"
author: "Community"
tags: ["security", "threat", "model"]
date: 2026-03-20
---

# Threat Model Source Code Repo

Deliver an actionable AppSec-grade threat model that is specific to the repository or a project path, not a generic checklist. Anchor every architectural claim to evidence in the repo and keep assumptions explicit. Prioritizing realistic attacker goals and concrete impacts over generic checklists.

## Quick start

1) Collect (or infer) inputs:
- Repo root path and any in-scope paths.
- Intended usage, deployment model, internet exposure, and auth expectations (if known).
- Any existing repository summary or architecture spec.
- Use prompts in `references/prompt-template.md` to generate a repository summary.
- Follow the required output contract in `references/prompt-template.md`. Use it verbatim when possible.

## Workflow

### 1) Scope and extract the system model
- Identify primary components, data stores, and external integrations from the repo summary.
- Identify how the system runs (server, CLI, library, worker) and its entrypoints.
- Separate runtime behavior from CI/build/dev tooling and from tests/examples.
- Map the in-scope locations to those components and exclude out-of-scope items explicitly.
- Do not claim components, flows, or controls without evidence.

### 2) Derive boundaries, assets, and entry points
- Enumerate trust boundaries as concrete edges between components, noting protocol, auth, encryption, validation, and rate limiting.
- List assets that drive risk (data, credentials, models, config, compute resources, audit logs).
- Identify entry points (endpoints, upload surfaces, parsers/decoders, job triggers, admin tooling, logging/error sinks).

### 3) Calibrate assets and attacker capabilities
- List the assets that drive risk (credentials, PII, integrity-critical state, availability-critical components, build artifacts).
- Describe realistic attacker capabilities based on exposure and intended usage.
- Explicitly note non-capabilities to avoid inflated severity.


### 4) Enumerate threats as abuse paths
- Prefer attacker goals that map to assets and boundaries (exfiltration, privilege escalation, integrity compromise, denial of service).
- Classify each threat and tie it to impacted assets.
- Keep the number of threats small but high quality.

### 5) Prioritize with explicit likelihood and impact reasoning
- Use qualitative likelihood and impact (low/medium/high) with short justifications.
- Set overall priority (critical/high/medium/low) using likelihood x impact, adjusted for existing controls.
- State which assumptions most influence the ranking.

### 6) Validate service context and assumptions with the user
- Summarize key assumptions that materially affect threat ranking or scope, then ask the user to confirm or correct them.
- Ask 1–3 targeted questions to resolve missing context (service owner and environment, scale/users, deployment model, authn/authz, internet exposure, data sensitivity, multi-tenancy).
- Pause and wait for user feedback before producing the final report.
- If the user declines or can’t answer, state which assumptions remain and how they influence priority.

### 7) Recommend mitigations and focus paths
- Distinguish existing mitigations (with evidence) from recommended mitigations.
- Tie mitigations to concrete locations (component, boundary, or entry point) and control types (authZ checks, input validation, schema enforcement, sandboxing, rate limits, secrets isolation, audit logging).
- Prefer specific implementation hints over generic advice (e.g., "enforce schema at gateway for upload payloads" vs "validate inputs").
- Base recommendations on validated user context; if assumptions remain unresolved, mark recommendations as conditional.

### 8) Run a quality check before finalizing
- Confirm all discovered entrypoints are covered.
- Confirm each trust boundary is represented in threats.
- Confirm runtime vs CI/dev separation.
- Confirm user clarifications (or explicit non-responses) are reflected.
- Confirm assumptions and open questions are explicit.
- Confirm that the format of the report matches closely the required output format defined in prompt template: `references/prompt-template.md`
- Write the final Markdown to a file named `<repo-or-dir-name>-threat-model.md` (use the basename of the repo root, or the in-scope directory if you were asked to model a subpath).


## Risk prioritization guidance (illustrative, not exhaustive)
- High: pre-auth RCE, auth bypass, cross-tenant access, sensitive data exfiltration, key or token theft, model or config integrity compromise, sandbox escape.
- Medium: targeted DoS of critical components, partial data exposure, rate-limit bypass with measurable impact, log/metrics poisoning that affects detection.
- Low: low-sensitivity info leaks, noisy DoS with easy mitigation, issues requiring unlikely preconditions.

## References

- Output contract and full prompt template: `references/prompt-template.md`
- Optional controls/asset list: `references/security-controls-and-assets.md`

Only load the reference files you need. Keep the final result concise, grounded, and reviewable.

---

## Reference: Prompt Template

# Threat Modeling Prompt Template for LLMs

This reference provides a disciplined, repo-grounded prompt that produces AppSec-usable threat models. Use it when you need a reliable output contract and a consistent process to assemble the threat model output

## System prompt

Use this as a stable system prompt:

````text
You are a senior application security engineer producing a threat model that will be read by other AppSec engineers.

Primary objective:
- Generate a threat model that is specific to THIS repository and its real-world usage.
- Prefer concrete, evidence-backed findings over generic vulnerability checklists.

Evidence and grounding rules:
- Do not invent components, data stores, endpoints, flows, or controls.
- Every architectural claim must be backed by at least one "Evidence anchor" referencing a repo path
  (and a symbol name, config key, or a short quoted snippet if available).
- If information is missing, state assumptions explicitly and list the open questions needed to validate them.

Security hygiene:
- Never output secrets. If you encounter tokens/keys/passwords, redact them and only describe their presence and location.

Threat modeling approach:
- Model the system using data flows and trust boundaries.
- Enumerate threats and produce attack goals and abuse paths
- Prioritize threats using explicit likelihood and impact reasoning (qualitative is acceptable: low/medium/high).

Scope discipline:
- Clearly separate: production/runtime behavior vs CI/build/dev tooling vs tests/examples.
- Clearly separate attacker-controlled inputs vs operator-controlled inputs vs developer-controlled inputs.
- If a vulnerability class requires attacker control that likely does not exist for this repo's real usage, say so and downgrade severity.

Communication quality:
- Write for AppSec engineers: concise but specific.
- Use precise terminology. Include mitigations and residual risks.
- Avoid restating large blocks of README/spec; summarize and point to evidence.

Diagram requirements:
- Produce a single compact Mermaid flowchart showing primary components and trust boundaries.
- Mermaid must render cleanly. Use a conservative subset:
  - Use `flowchart TD` or `flowchart LR` and only `-->` arrows.
  - Use simple node IDs (letters/numbers/underscores only) and quoted labels (e.g., `A["Label"]`); avoid `A(Label)` shape syntax.
  - Do not use Mermaid `title` lines or `style` directives.
  - Keep edge labels to plain words/spaces only via `-->|label|`; avoid `{}`, `[]`, `()`, or quotes in edge labels (if needed, drop the label).
  - Keep node labels short and readable: do not include file paths, URLs, or socket paths (put those details in prose outside the diagram).
- Wrap the diagram in a Markdown fenced block:
  ```mermaid
  <mermaid syntax here>
  ```
````

## Repository summary prompt

```
We have a codebase located at {repo_directory/path}, currently on branch {branch_name}.

Please produce a security-oriented summary of the repository (or the specified sub-path) with the goal of helping a follow-on security engineer quickly understand the system well enough to build an initial threat model and investigate potential security hypotheses.

Objectives
1.	Project overview
	•	Identify the primary programming languages, frameworks, and build system.
	•	Summarize the project’s core purpose and high-level architecture.
	•	Describe major components, services, or modules and how they interact.
2.	Security posture and entry points
	•	Identify likely user entry points and trust boundaries.
	•	Describe existing security layers (e.g., authentication, authorization, validation, sandboxing, isolation, privilege boundaries).
	•	Call out security-critical components and assumptions that must hold for the system to remain secure.

Guidance for Security Analysis

Structure the summary so an application security engineer can quickly answer questions such as:
	•	Where does user input originate?
	•	How is untrusted data parsed, validated, and handled?
	•	What security assumptions should not be violated?
	•	Where are the most likely choke points for security bugs?

Adapt the analysis to the project type. For example:
	•	Web applications: where requests enter, how user data is parsed, routed, authenticated, and stored.
	•	Command-line tools: supported inputs (arguments, files, environment variables, stdin) and how they are processed.
	•	Network daemons: exposed ports, supported protocols, message formats, and request handling paths.
	•	Operating system or low-level components: common vulnerability classes (e.g., memory corruption, logic flaws) that could lead to LPE or RCE.

Be thorough but pragmatic: the goal is to help a security engineer quickly determine whether a discovered bug is security-relevant and where deeper investigation should focus.

Tooling Notes

If Ripgrep (rg) is available, use it to explore the codebase. When using grep or rg, always include the -I flag to avoid searching through binary files.
```



## User prompt template

Use this as the task prompt, filling in what you know and marking the rest as assumptions:

```text
# Inputs
Context (fill as available; otherwise infer and mark assumptions):
- intended_usage: {intended_usage}
- deployment_model: {deployment_model}
- data_sensitivity: {data_sensitivity}
- internet_exposure: {internet_exposure}
- authn_authz_expectations: {authn_authz_expectations}
- out_of_scope: {out_of_scope}

Provided summaries (may be incomplete):
- repository_summary: {repository_summary}


In-scope code locations (if known):
- in_scope_paths: {in_scope_paths}

# Task
Construct a repo-centric threat model that helps AppSec engineers understand the most important security risks and where to focus manual review.

You MUST follow this process and reflect outputs in the final document:

## Process
1) Repo discovery (evidence collection)
   a. Identify the repo shape:
      - languages and frameworks
      - how it runs (server/cli/library), entrypoints, build artifacts
   b. Identify security-relevant surfaces and controls by searching for evidences, such as:
      - network listeners/routes/endpoints; RPC handlers; message consumers
      - authentication, session/token handling, authorization checks, RBAC/ACL logic
      - parsing/serialization/deserialization (JSON/YAML/XML/protobuf), template rendering, eval/dynamic code
      - file upload/read paths, archive extraction, image/document parsing
      - database/queue/cache clients and query construction
      - secrets/config loading, environment variables, key management
      - SSRF-capable HTTP clients, webhooks, URL fetchers
      - sandboxing/isolation, privilege boundaries, subprocess execution
      - logging/auditing and error handling paths
      - CI/build/release: pipelines, dependency management, artifact publishing
   
2) System model
   a. Summarize the primary components (runtime plus critical build/CI components when relevant).
   b. Enumerate data flows and trust boundaries.
      - For each trust boundary, specify:
        * source to destination
        * data types crossing (e.g., credentials, PII, files, tokens, prompts)
        * channel/protocol (HTTP/gRPC/IPC/file/db)
        * security guarantees and validation (auth, mTLS, origin checks, schema validation, rate limits)
   c. Provide a compact Mermaid diagram showing components and trust boundaries.

3) Assets and security objectives
   - List assets (data, credentials, integrity-critical state, availability-critical components, build artifacts).
   - For each asset, state why it matters (confidentiality/integrity/availability, compliance, user harm).

4) Attacker model
   - Capabilities: realistic remote attacker assumptions based on intended usage and exposure.
   - Non-capabilities: things attacker cannot plausibly do (unless explicitly in scope), to avoid inflated severity.

5) Threat enumeration (concrete, system-specific)
   - Generate threats as attacker stories tied to:
     * entry points
     * trust boundaries
     * privileged components
   - Prefer abuse paths (multi-step sequences) over single-line generic threats.

6) Risk prioritization
   - For each threat:
     * Likelihood: low/medium/high with a 1 to 2 sentence justification
     * Impact: low/medium/high with a 1 to 2 sentence justification
     * Overall priority: critical/high/medium/low (based on likelihood x impact, adjusted for existing controls)
   - Explicitly state which assumptions most affect risk.

7) Validate assumptions and service context with the user (required before final report)
   - Summarize key assumptions that materially affect scope or risk ranking.
   - Ask 1 to 3 targeted questions to resolve missing service meta-context (service owner/environment, scale/users, deployment model, authn/authz, internet exposure, data sensitivity, multi-tenancy).
   - Pause and wait for user feedback before producing the final report.
   - If the user cannot answer, proceed with explicit assumptions and mark any conditional conclusions.

8) Mitigations and recommendations
   - For each high/critical threat:
     * Existing mitigations (with evidence anchors)
     * Gaps/weaknesses
     * Recommended mitigations (code/config/process)
     * Detection/monitoring ideas (logging, metrics, alerts)

9) Focus paths for manual security review
   - Output 2 to 30 repo-relative paths (files or directories) that merit deeper review.
   - For each path, give a one-sentence reason tied to the threat model.

10) Quality check
   - Provide a short checklist confirming you covered:
     * all entry points you discovered
     * each trust boundary at least once in threats
     * runtime vs CI/dev separation
     * user clarifications (or explicit non-responses)
     * assumptions and open questions

## Required output format (exact)
Before producing the final Markdown report, first provide an assumption-validation check-in:
- List the key assumptions in 3 to 6 bullets.
- Ask 1 to 3 targeted context questions.
- Wait for the user response, then produce the final report below using the clarified context.

Produce valid Markdown with these sections in this order:

## Executive summary
- 1 short paragraph on the top risk themes and highest-risk areas.

## Scope and assumptions
- In-scope paths, out-of-scope items, and explicit assumptions.
- A short list of open questions that would materially change the risk ranking.


## System model
### Primary components
### Data flows and trust boundaries
Represent the system as a sequence of arrow-style bullets (e.g., Internet → API Server, User Input -> Application Logic, etc). For each boundary, document:
	•	the primary data types crossing the boundary,
	•	the communication channel or protocol,
	•	the security guarantees (e.g., authentication, origin checks, encryption, rate limiting), and
	•	any input validation, normalization, or schema enforcement performed.

#### Diagram
- Include a single, compact Mermaid diagram (`flowchart TD` or `flowchart LR`) showing primary components and trust boundaries (e.g., separate trust zones via subgraphs). Keep it compact, use only `-->`, avoid `title`/`style`, keep node labels short (no paths/URLs), and keep edge labels to plain words only (avoid `{}`, `[]`, `()`, or quotes).


## Assets and security objectives
- A table: Asset | Why it matters | Security objective (C/I/A)

## Attacker model
### Capabilities
### Non-capabilities

## Entry points and attack surfaces
- A table: Surface | How reached | Trust boundary | Notes | Evidence (repo path / symbol)

## Top abuse paths
- 5 to 10 short abuse paths, each as a numbered sequence of steps (attacker goal -> steps -> impact).

## Threat model table
- A Markdown table with columns:
  Threat ID | Threat source | Prerequisites | Threat action | Impact | Impacted assets | Existing controls (evidence) | Gaps | Recommended mitigations | Detection ideas | Likelihood | Impact severity | Priority

Rules:
- Threat IDs must be stable and formatted: TM-001, TM-002, ...
- Priority must be one of: critical, high, medium, low.
- Keep prerequisites to 1 to 2 sentences. Keep recommended mitigations concrete.

## Criticality calibration
- Define what counts as critical/high/medium/low for THIS repo and context.
- Include 2 to 3 examples per level (tailored to the repo's assets and exposure).

## Focus paths for security review
- A table: Path | Why it matters | Related Threat IDs

## Notes on use

- Fill in known context, but allow the model to infer and mark assumptions.
- Include 1–2 repo-path anchors per major claim; do not dump every match.

---

## Reference: Security Controls And Assets

# Security Controls and Asset Categories

Use this as a lightweight checklist to keep outputs consistent across teams. Prefer concrete, system-specific items over generic text.

## Asset categories (pick only what applies)
- User data (PII, content, uploads)
- Authentication artifacts (passwords, tokens, sessions, cookies)
- Authorization state (roles, policies, ACLs)
- Secrets and keys (API keys, signing keys, encryption keys)
- Configuration and feature flags
- Models and weights (if ML systems)
- Source code and build artifacts
- Audit logs and telemetry
- Availability-critical resources (queues, caches, rate limits, compute budgets)
- Tenant isolation boundaries and metadata

## Security control categories
- Identity and access: authN, authZ, session handling, mTLS, key rotation
- Input protection: schema validation, parsing hardening, upload scanning, sandboxing
- Network safeguards: TLS, network policies, WAF, rate limiting, DoS controls
- Data protection: encryption at rest/in transit, tokenization, redaction
- Isolation: process sandboxing, container boundaries, tenant isolation, seccomp
- Observability: audit logs, alerting, anomaly detection, tamper resistance
- Supply chain: dependency pinning, SBOMs, provenance, signing
- Change control: CI checks, deployment approvals, config guardrails

## Mitigation phrasing patterns
- "Enforce schema at <boundary> for <payload> before <component>."
- "Require authZ check for <action> on <resource> in <service>."
- "Isolate <parser/component> in a sandbox with <resource limits>."
- "Rate limit <endpoint> by <key> and apply burst caps."
- "Encrypt <data> at rest using <key management> and rotate <keys>."
