---
title: "Sentry SDK Skill Creator"
description: "Create a complete Sentry SDK skill bundle for any platform. Use when asked to 'create an SDK skill', 'add a new platform skill', 'write a Sentry skill for X', or build a new sentry-<platform>-sdk skill bundle with wizard flow and feature reference..."
category: "devops"
source: "community"
author: "Community"
tags: ["sentry", "sdk", "skill", "creator"]
date: 2026-03-20
---

# Create a Sentry SDK Skill Bundle

Produce a complete, research-backed SDK skill bundle — a main wizard SKILL.md plus deep-dive reference files for every feature pillar the SDK supports.

## Invoke This Skill When

- Asked to "create a Sentry SDK skill" for a new platform
- Asked to "add support for [language/framework]" to sentry-agent-skills
- Building a new `sentry-<platform>-sdk` skill bundle
- Porting the SDK skill pattern to a new Sentry SDK

> Read `${SKILL_ROOT}/references/philosophy.md` first — it defines the bundle architecture, wizard flow, and design principles this skill implements.

---

## Phase 1: Identify the SDK

Determine what you're building a skill for:

```bash
# What SDK? What's the package name?
# Examples: sentry-go, @sentry/sveltekit, sentry-python, sentry-ruby, sentry-cocoa
```

Establish the **feature matrix** — which Sentry pillars does this SDK support?

| Pillar | Check docs | Notes |
|--------|-----------|-------|
| Error Monitoring | Always available | Non-negotiable baseline |
| Tracing/Performance | Usually available | Check for span API |
| Profiling | Varies | May be removed or experimental |
| Logging | Newer feature | Check minimum version |
| Metrics | Newer feature | May be beta/experimental |
| Crons | Backend only | Not available for frontend SDKs |
| Session Replay | Frontend only | Not available for backend SDKs |
| AI Monitoring | Some SDKs | Usually JS + Python only |

**Reference existing SDK skills** to understand the target quality level:

```bash
ls skills/sentry-*-sdk/ 2>/dev/null
# Read 1-2 existing SDK skills for pattern reference
```

---

## Phase 2: Research

**This is the most critical phase.** Skill quality depends entirely on accurate, current API knowledge. Do NOT write skills from memory — research every feature against official docs.

### Research Strategy

Spin off **parallel research tasks** (using the `claude` tool with `outputFile`) — one per feature area. Each task should:
1. Visit the official Sentry docs pages for that feature
2. Visit the SDK's GitHub repo for source-level API verification
3. Write thorough findings to a dedicated research file

Read `${SKILL_ROOT}/references/research-playbook.md` for the detailed research execution plan, including prompt templates and file naming conventions.

### Research the Sentry Wizard

Before diving into feature research, check whether the Sentry wizard CLI supports this framework:

```bash
# Check the SDK's docs landing page for wizard instructions
# Visit: https://docs.sentry.io/platforms/<platform>/
# Look for: "npx @sentry/wizard@latest -i <integration>"
```

If a wizard integration exists:
1. Document the exact wizard command and `-i` flag
2. Document what the wizard creates/modifies (files, config, build plugins)
3. Note that the wizard handles **authentication interactively** — login, org/project selection, and auth token creation/download all happen automatically
4. Note whether the wizard sets up **source map upload** — this is critical for frontend SDKs
5. This will become "Option 1: Wizard (Recommended)" in Phase 3 of the generated skill

> **Why this matters:** The wizard handles the entire auth flow (login, org/project selection,
> auth token) and source map upload configuration automatically. Without source maps,
> production stack traces show minified code — making Sentry nearly useless for frontend
> debugging. And without the auth token, source maps can't be uploaded at all. The wizard
> is the most reliable way to get both right in a single step.

### Research Batching

Batch research tasks by topic area. Run them in parallel where possible:

| Batch | Topics | Output file |
|-------|--------|-------------|
| 1 | Setup, configuration, all init options, framework detection | `research/<sdk>-setup-config.md` |
| 2 | Error monitoring, panic/exception capture, scopes, enrichment | `research/<sdk>-error-monitoring.md` |
| 3 | Tracing, profiling (if supported) | `research/<sdk>-tracing-profiling.md` |
| 4 | Logging, metrics, crons (if supported) | `research/<sdk>-logging-metrics-crons.md` |
| 5 | Session replay (frontend only), AI monitoring (if supported) | `research/<sdk>-replay-ai.md` |

**Important:** Tell each research task to write its output to a file (`outputFile` parameter). Do NOT consume research results inline — they're large (500–1200 lines each). Workers will read them from disk later.

### Research Quality Gate

Before proceeding, verify each research file:
- Has actual content (not just Claude's process notes)
- Contains code examples with real API names
- Includes minimum SDK versions
- Covers framework-specific variations

```bash
# Quick verification
for f in research/<sdk>-*.md; do
  echo "=== $(basename $f) ==="
  wc -l "$f"
  grep -c "^#" "$f"  # should have multiple headings
done
```

**Re-run any research task that produced fewer than 100 lines** — it likely failed silently.

---

## Phase 3: Create the Main SKILL.md

The main SKILL.md implements the **four-phase wizard** from the philosophy doc. Keep it focused — the main file should cover the wizard flow, quick start config, framework tables, and reference dispatch. Deep-dive details for individual features belong in `references/` files, not here. Be thorough but not redundant.

### Gather Context First

Before writing, run a scout or read existing skills to understand conventions:
- Frontmatter pattern (name, description, license)
- "Invoke This Skill When" trigger phrases
- Table formatting and code example style
- Troubleshooting table conventions

### SKILL.md Structure

```markdown
---
name: sentry-<platform>-sdk
description: Full Sentry SDK setup for <Platform>. Use when asked to "add Sentry
  to <platform>", "install <package>", or configure error monitoring, tracing,
  [features] for <Platform> applications. Supports [frameworks].
license: Apache-2.0
---

# Sentry <Platform> SDK

## Invoke This Skill When
[trigger phrases]

## Phase 1: Detect
[bash commands to scan project — package manager, framework, existing Sentry, frontend/backend]

## Phase 2: Recommend
[opinionated feature matrix with "always / when detected / optional" logic]

## Phase 3: Guide
### Option 1: Wizard (Recommended)   ← if wizard exists for this framework
[wizard command, what it creates/modifies table, skip-to-verification note]
### Option 2: Manual Setup            ← always include
### Install
### Quick Start — Recommended Init
### Source Maps Setup                  ← required for frontend/mobile SDKs
### Framework Middleware (if applicable)
### For Each Agreed Feature
[reference dispatch table: feature → ${SKILL_ROOT}/references/<feature>.md]

## Configuration Reference
[key init options table, environment variables]

## Verification
[test snippet]

## Phase 4: Cross-Link
[detect companion frontend/backend, suggest matching SDK skills]

## Troubleshooting
[common issues table]
```

### Key Principles for the Main SKILL.md

1. **Keep it lean** — deep details go in references, not here
2. **Wizard-first for framework SDKs** — if the Sentry wizard supports this framework, present it as "Option 1: Wizard (Recommended)" before any manual setup. The wizard handles the full auth flow (login, org/project selection, auth token creation), source map upload, build tool plugins, and framework-specific wiring — all in one interactive step. See `${SKILL_ROOT}/references/philosophy.md` for the full pattern.
3. **Source maps are non-negotiable for frontend/mobile** — the manual setup path must include source map upload configuration (build tool plugin + env vars). Without source maps, production stack traces are unreadable minified code.
4. **Detection commands must be real** — test them against actual projects
5. **Recommendation logic must be opinionated** — "always", "when X detected", not "maybe consider"
6. **Quick Start config should enable the most features** with sensible defaults
7. **Framework middleware table** — exact import paths, middleware calls, and quirks
8. **Cross-link aggressively** — if Go backend, suggest frontend. If Svelte frontend, suggest backend.

---

## Phase 4: Create Reference Files

One reference file per feature pillar the SDK supports. These are deep dives — they can be longer than the main SKILL.md.

### Reference File Structure

```markdown
# <Feature> — Sentry <Platform> SDK

> Minimum SDK: `<package>` vX.Y.Z+

## Configuration

## Code Examples
### Basic usage
### Advanced patterns
### Framework-specific notes (if applicable)

## Best Practices

## Troubleshooting
| Issue | Solution |
|-------|----------|
```

### What Makes a Good Reference

Read `${SKILL_ROOT}/references/quality-checklist.md` for the full quality rubric.

Key points:
- **Working code examples** — not pseudo-code, not truncated snippets
- **Tables for config options** — type, default, minimum version
- **One complete example per pattern** — don't show 5 variations of the same thing
- **Framework-specific notes** — call out when behavior differs between frameworks
- **Minimum SDK version at the top** — always
- **Honest about limitations** — if a feature was removed (like Go profiling), say so

### Feature-Specific Guidance

| Feature | Key things to cover |
|---------|-------------------|
| Error Monitoring | Capture APIs, panic/exception recovery, scopes, enrichment (tags/user/breadcrumbs), error chains, BeforeSend, fingerprinting |
| Tracing | Sample rates, custom spans, distributed tracing, framework middleware, operation types |
| Profiling | Sample rate config, how it attaches to traces, or honest "removed/not available" |
| Logging | Enable flag, logger API, integration with popular logging libraries, filtering |
| Metrics | Counter/gauge/distribution APIs, units, attributes, best practices for cardinality |
| Crons | Check-in API, monitor config, schedule types, heartbeat patterns |
| Session Replay | Replay integration, sample rates, privacy masking, canvas/network recording |

> **Note for frontend/mobile SDKs:** Source map upload configuration belongs in the main SKILL.md (Phase 3: Guide), not in a reference file. It's part of the core setup flow — every frontend production deployment needs it. Cover the build tool plugin, the required env vars (`SENTRY_AUTH_TOKEN`, `SENTRY_ORG`, `SENTRY_PROJECT`), and add `.env` to `.gitignore`.

---

## Phase 5: Verify Everything

**Do NOT skip this phase.** SDK APIs change frequently. Research can hallucinate. Workers can fabricate config keys.

### API Verification

Run a dedicated verification pass against the SDK's actual source code:

```
Research prompt: "Verify these specific API names and signatures against
the <SDK> GitHub repo source code: [list every API from the skill files]"
```

Things that commonly go wrong:
- Config option names with wrong casing (`SendDefaultPii` vs `SendDefaultPII`)
- Fabricated config keys that don't exist (`experimental.tracing` — verify it's real)
- Deprecated APIs used instead of modern replacements (`configureScope` → `getIsolationScope`)
- Features listed as available when they've been removed (profiling in Go SDK)
- Wrong minimum version numbers

### Review Pass

Run a reviewer on the complete skill bundle:
- Technical accuracy of code examples
- Consistency between main SKILL.md and reference files
- Consistency with existing SDK skills in the repo
- Agent Skills spec compliance (frontmatter, naming)

### Fix Review Findings

Triage by priority:
- **P0**: Misleading claims (advertising removed features) — fix immediately
- **P1**: Incorrect APIs, deprecated methods — fix before merge
- **P2**: Style inconsistencies, version nitpicks — fix if quick
- **P3**: Skip

---

## Phase 6: Register and Update Docs

After the skill passes review:

1. **Update README.md** — add to the SDK Skills table
2. **Update AGENTS.md** — if the philosophy doc or skill categories section needs it
3. **Add usage examples** — trigger phrases in the Usage section
4. **Document the bundle pattern** — if this is a new SDK, note the references/ structure

### Commit Strategy

Each major piece gets its own commit:
1. `feat(<platform>-sdk): add sentry-<platform>-sdk main SKILL.md wizard`
2. `feat(<platform>-sdk): add reference deep-dives for all feature pillars`
3. `docs(readme): add sentry-<platform>-sdk to available skills`
4. `fix(skills): address review findings` (if any)

---

## Checklist

Before declaring the skill complete:

- [ ] Philosophy doc read and followed
- [ ] All feature pillars researched from official docs (not from memory)
- [ ] Research files verified (real content, correct APIs, >100 lines each)
- [ ] Main SKILL.md is focused — wizard flow + quick start + reference dispatch; deep dives in references
- [ ] Main SKILL.md implements all 4 wizard phases
- [ ] Wizard CLI checked — if supported, presented as "Option 1: Wizard (Recommended)" with auth flow + source map benefits described
- [ ] Source map / debug symbol upload covered in manual setup path (frontend/mobile SDKs)
- [ ] Reference file for each supported feature pillar
- [ ] APIs verified against SDK source code
- [ ] Review pass completed, findings addressed
- [ ] Profiling/removed features honestly documented (not advertised)
- [ ] Cross-links to companion frontend/backend skills
- [ ] README.md updated
- [ ] All commits polished with descriptive messages

---

## Reference: Philosophy

# SDK Skill Philosophy

Guide for authoring SDK skill bundles — a new pattern that ships complete, opinionated Sentry setup wizards alongside each SDK.

## The Vision

SDK skills are **living documentation bundles**. Instead of a flat SKILL.md that covers one feature, an SDK skill covers everything a project needs: error monitoring, tracing, profiling, logging, session replay, and more. The agent acts as an expert who reads the project, makes opinionated recommendations, and guides the user through each feature — loading deep-dive references as needed.

## Bundle Architecture

```
skills/
  sentry-<platform>-sdk/
    SKILL.md                    # Main wizard
    references/
      error-monitoring.md       # Deep dive: errors, panics, wrapping
      tracing.md                # Deep dive: spans, distributed tracing
      profiling.md              # Deep dive: continuous profiling
      logging.md                # Deep dive: structured logs
      metrics.md                # Deep dive: counters, gauges, distributions
      crons.md                  # Deep dive: cron job monitoring
      session-replay.md         # Deep dive: replay (frontend only)
```

The main `SKILL.md` is the wizard — it stays lean. References are loaded conditionally based on what the user wants to configure.

**Loading a reference in SKILL.md:**
```markdown
Read ${SKILL_ROOT}/references/tracing.md for detailed tracing setup steps.
```

## Feature Pillars

Each SDK supports a subset of Sentry's pillars:

| Pillar | Backend SDKs | Frontend SDKs |
|--------|-------------|---------------|
| Error Monitoring | ✅ Always | ✅ Always |
| Tracing/Performance | ✅ Common | ✅ Common |
| Profiling | ✅ Some | ✅ Some |
| Logging | ✅ Common | ✅ Common |
| Metrics | ✅ Some | ✅ Some |
| Crons | ✅ Backend only | ❌ |
| Session Replay | ❌ | ✅ Frontend only |
| AI Monitoring | ✅ Some | ✅ Some |

Only include reference files for pillars the SDK actually supports. If a feature is experimental or beta, mark it clearly in the reference header.

## The Wizard Flow

The main SKILL.md implements a four-phase wizard:

### Phase 1: Detect

Scan the project to understand the stack:

```markdown
## Phase 1: Detect

Run these commands to understand the project:
- `cat go.mod` / `cat package.json` — identify language and framework
- `grep -r "sentry" go.mod package.json 2>/dev/null` — check if Sentry is already installed
- `ls frontend/ web/ client/ 2>/dev/null` — detect companion frontend/backend
```

### Phase 2: Recommend

Present opinionated feature recommendations based on what you found. Don't ask open-ended "what do you want?" — lead with a concrete proposal:

```markdown
## Phase 2: Recommend

Based on what I found, here's what I recommend setting up:

**Recommended (core coverage):**
- ✅ Error monitoring — captures panics, exceptions, and unhandled errors
- ✅ Tracing — your app has HTTP handlers; distributed tracing will show latency across services
- ✅ Logging — you're using zap; Sentry can capture structured logs automatically

**Optional (enhanced observability):**
- ⚡ Profiling — low-overhead CPU/memory profiling in production
- ⚡ Metrics — custom counters and gauges for business KPIs
- ⚡ Crons — detect silent failures in scheduled jobs

Shall I set up everything recommended, or customize the list?
```

Recommendation logic:
- **Error monitoring**: Always recommend — this is the baseline
- **Tracing**: Recommend when HTTP handlers, APIs, gRPC, or queues are detected
- **Profiling**: Recommend for production apps where perf matters
- **Logging**: Recommend when the app already uses a logging library
- **Metrics**: Recommend for apps tracking business events or SLOs
- **Crons**: Recommend when cron/scheduler patterns are detected
- **Session Replay**: Recommend for frontend apps, never for backend

### Phase 3: Guide

#### Wizard-First for Framework SDKs

Many Sentry SDKs ship with a CLI wizard (`npx @sentry/wizard@latest -i <integration>`) that scaffolds the entire setup in one command. **When a wizard integration exists for the target framework, the skill must present it as the primary recommended path — before any manual instructions.**

Why this matters:
- The wizard walks through **authentication interactively** — it opens the browser for login, lets the user select their Sentry org and project, and creates/downloads the auth token automatically. No manual token creation or copy-pasting from the Sentry dashboard.
- The wizard configures **source map upload** automatically — without source maps, production stack traces show minified garbage. This is the single most common setup mistake in frontend projects.
- The wizard handles framework-specific wiring (hook files, config plugins, build tool plugins) that's easy to get wrong manually.
- The wizard creates a test page/component for immediate verification.

**Pattern for skills with wizard support:**

```markdown
### Option 1: Wizard (Recommended)

\`\`\`bash
npx @sentry/wizard@latest -i <framework>
\`\`\`

The wizard walks you through login, org/project selection, and auth token
setup interactively. It then handles installation, SDK initialization,
source map upload configuration, and creates a test page for verification.
Skip to [Verification](#verification) after running it.

### Option 2: Manual Setup

[Full manual instructions follow here...]
```

**When to include a wizard option:**
- The SDK docs page shows a wizard command for the framework
- During research (Phase 2), verify wizard support by checking `https://docs.sentry.io/platforms/<platform>/` for wizard instructions

**Known wizard integrations** (verify during research — this list may be outdated):

| Wizard `-i` flag | Framework |
|-----------------|-----------|
| `nextjs` | Next.js |
| `sveltekit` | SvelteKit |
| `remix` | Remix |
| `nuxt` | Nuxt |
| `reactNative` | React Native / Expo |
| `angular` | Angular |
| `vue` | Vue |
| `flutter` | Flutter |
| `apple` | iOS / macOS (Cocoa) |
| `android` | Android |
| `dotnet` | .NET |

> **Important:** Even when the wizard is available, the skill must still include full manual setup instructions. The wizard may not cover all configuration options, and some users work in environments where interactive CLIs aren't practical (CI, Docker, restricted shells). The manual path is the fallback, not an afterthought — it must be complete.

#### Source Maps: The Non-Negotiable for Frontend

Source map upload is **critical** for any frontend or mobile SDK. Without it, error stack traces in Sentry show minified/bundled code that's unreadable.

Every frontend/mobile SDK skill must:
1. Present the wizard as the easiest path to get source maps working
2. Include manual source map upload instructions for the manual setup path
3. Cover the correct build tool plugin (`sentryVitePlugin`, `sentryWebpackPlugin`, `sentrySvelteKit`, etc.)
4. Document the required environment variables (`SENTRY_AUTH_TOKEN`, `SENTRY_ORG`, `SENTRY_PROJECT`)
5. Add source map troubleshooting entries to the troubleshooting table

#### Feature Reference Loading

Walk through each agreed feature, loading the relevant reference:

```markdown
## Phase 3: Guide

For each feature in the agreed list:
1. Load the reference: `Read ${SKILL_ROOT}/references/<feature>.md`
2. Follow the reference steps exactly
3. Verify the feature works before moving to the next
```

Keep the main SKILL.md free of deep implementation details — that lives in the references.

### Phase 4: Cross-Link

After completing setup, check for coverage gaps:

```markdown
## Phase 4: Cross-Link

Check for a companion frontend or backend that's missing Sentry:
- `ls frontend/ web/ client/ 2>/dev/null` + check for package.json with a JS framework
- `ls backend/ server/ api/ 2>/dev/null` + check for go.mod or requirements.txt

If found, suggest:
> I see a React frontend in `frontend/` with no Sentry. Consider running the
> `sentry-react-sdk` or `sentry-svelte-sdk` skill for full-stack coverage.
```

## Reference File Guidelines

Each reference covers **one feature pillar** and is loaded on demand. Reference files can be longer than a typical skill — they are deep dives, not wizard flows.

**Required sections for each reference:**

```markdown
# <Feature> — <Platform> SDK

> Minimum SDK: `<package>@X.Y.Z+`

## Installation

## Configuration

## Code Examples

### Basic usage

### Framework-specific notes (if applicable)

## Best Practices

## Troubleshooting

| Issue | Solution |
|-------|----------|
```

**Style rules:**
- Tables for config options, not prose lists
- One complete, working code example per use case — not multiple variations
- Note framework-specific differences (e.g., SvelteKit vs Svelte, Gin vs net/http)
- Include minimum SDK version at the top of every reference

## Error Monitoring: The Non-Negotiable Baseline

Error monitoring is not optional. Every SDK skill must:

1. Set up error monitoring in the initial `Init()` call — not as an opt-in
2. Use opinionated defaults that capture the most useful data:
   - `SendDefaultPii: true` (or platform equivalent) — includes user context
   - A sensible `TracesSampleRate` starting point (e.g., `1.0` for dev, lower for prod)
   - Automatic framework integrations (e.g., `http.Integration`, `gin.Integration`)
3. Make clear this is the baseline — everything else enhances it

```go
// Example opinionated baseline for Go
sentry.Init(sentry.ClientOptions{
    Dsn:              os.Getenv("SENTRY_DSN"),
    SendDefaultPii:   true,
    TracesSampleRate: 1.0,
    EnableTracing:    true,
})
```

Never present a minimal config that leaves users under-instrumented. The goal is full observability from day one.

## Staying Current

SDK skills ship alongside the SDK and must reflect the current API.

**In every SKILL.md and reference file:**
- State the minimum SDK version required for each feature
- Use current API names — never deprecated ones
- Mark experimental features with ⚠️ **Experimental** or 🔬 **Beta**
- Add this disclaimer in the Invoke section:

```markdown
> **Note:** SDK versions and APIs below reflect current Sentry docs.
> Always verify against [docs.sentry.io](https://docs.sentry.io) before implementing.
```

**When updating a skill:**
1. Check the SDK changelog for breaking changes since last update
2. Verify all code examples compile/run against the latest SDK version
3. Update minimum version requirements if new features raised the floor
4. Remove deprecated API usage

## Naming Conventions

| What | Convention | Example |
|------|-----------|---------|
| Skill directory | `sentry-<platform>-sdk` | `sentry-go-sdk`, `sentry-svelte-sdk` |
| Main file | `SKILL.md` | — |
| Reference files | `<feature>.md` in `references/` | `references/tracing.md` |
| Skill `name` field | matches directory | `sentry-go-sdk` |

## Complete Skill Scaffold

```
skills/sentry-<platform>-sdk/
  SKILL.md
  references/
    error-monitoring.md
    tracing.md
    profiling.md       # if supported
    logging.md
    metrics.md         # if supported
    crons.md           # backend only
    session-replay.md  # frontend only
```

Minimal `SKILL.md` structure:

```markdown
---
name: sentry-<platform>-sdk
description: Full Sentry SDK setup for <Platform>. Use when asked to add Sentry
  to a <platform> project, install the <platform> SDK, or configure error
  monitoring, tracing, profiling, logging, or crons for <Platform>.
license: Apache-2.0
---

# Sentry <Platform> SDK

Opinionated wizard that scans your project and guides you through complete Sentry setup.

## Invoke This Skill When

- User asks to "add Sentry to <platform>" or "set up Sentry"
- User wants error monitoring, tracing, profiling, or logging in <platform>
- User mentions the <platform> Sentry SDK package name

> **Note:** SDK versions and APIs below reflect current Sentry docs at time of writing.
> Always verify against [docs.sentry.io](https://docs.sentry.io/<platform>/) before implementing.

## Phase 1: Detect
...

## Phase 2: Recommend
...

## Phase 3: Guide
### Option 1: Wizard (Recommended)  ← if wizard exists for this framework
### Option 2: Manual Setup
...

## Phase 4: Cross-Link
...
```

## See Also

- [AGENTS.md](../../../AGENTS.md) — General skill authoring guidelines and style rules
- [Agent Skills Specification](https://agentskills.io/specification)
- [Sentry Documentation](https://docs.sentry.io/)

---

## Reference: Quality Checklist

# Quality Checklist

Rubric for evaluating SDK skill bundles before merge. Every item must pass.

## Main SKILL.md

### Spec Compliance

| Check | Requirement |
|-------|-------------|
| Focus | Wizard flow + quick start + reference dispatch; deep dives belong in `references/` |
| `name` field | Matches directory name, kebab-case, 1-64 chars |
| `description` field | Under 1024 chars, includes trigger phrases, no angle brackets |
| `license` field | `Apache-2.0` |
| No content before `---` | YAML frontmatter must be the first thing in the file |

### Wizard Flow

| Phase | Must include |
|-------|-------------|
| Phase 1: Detect | Real bash commands that work on actual projects. Not pseudo-code. |
| Phase 2: Recommend | Opinionated feature matrix. "Always / when detected / optional" — NOT "maybe consider". |
| Phase 3: Guide | Install commands, quick start init, framework middleware, reference dispatch table. |
| Phase 4: Cross-Link | Frontend/backend detection, specific skill suggestions with table. |

### Content Quality

| Check | Pass criteria |
|-------|--------------|
| Quick Start config | Enables the most features with sensible defaults. Not a minimal config. |
| Framework table | Exact import paths, middleware calls, and framework-specific quirks. |
| Config reference | Table with option name, type, default, purpose. |
| Environment variables | Which env vars the SDK reads and what they map to. |
| Verification | Real test snippet — not "check the dashboard". |
| Troubleshooting | 5+ common issues with concrete solutions. |

## Reference Files

### Per-File Checks

| Check | Requirement |
|-------|-------------|
| Minimum SDK version | Stated at the top of every reference file |
| Working code examples | Real, compilable/runnable code — not pseudo-code |
| Config options table | Type, default, minimum version for each option |
| Troubleshooting table | At least 3 common issues with solutions |
| One topic per file | Error monitoring in one file, tracing in another — no mixing |

### Code Example Quality

| Good | Bad |
|------|-----|
| Complete, working snippet | Truncated with `// ...` |
| Real import paths | Fake package names |
| Correct API names verified against source | API names from memory |
| One example per pattern | Five variations of the same thing |
| Framework-specific notes called out | Generic "this works everywhere" |

### Accuracy Indicators

Watch for these red flags that indicate fabricated or outdated content:

| Red flag | What to check |
|----------|---------------|
| Config option with no source reference | Search SDK repo for the option name |
| Feature listed as "available" with no code example | Likely doesn't exist |
| API signature that looks "too clean" | Verify against actual source |
| Missing error handling in examples | Real code has edge cases |
| Version number that's a round number (e.g., "8.0.0") | Check changelog for actual version |

### Honesty Checks

| Check | Requirement |
|-------|-------------|
| Removed features | Documented honestly with alternatives (not advertised as available) |
| Experimental features | Marked with ⚠️ or 🔬 |
| Deprecated APIs | Not used — replaced with modern equivalents |
| PII implications | Called out explicitly (especially for AI monitoring, session replay) |
| Performance impact | Noted for session replay, profiling, high sample rates |

## Cross-Cutting Checks

### Consistency Between Files

| Check | What to verify |
|-------|---------------|
| API names match | Same function name in SKILL.md and reference files |
| Config option names match | Same casing and spelling everywhere |
| Version numbers match | Same minimum version claims across files |
| Scope APIs consistent | Don't use deprecated API in one file and modern in another |

### Consistency With Existing Skills

| Check | What to verify |
|-------|---------------|
| Frontmatter style | Same fields and format as other SDK skills |
| Trigger phrase style | Same "Invoke This Skill When" pattern |
| Table format | Same column headers and layout |
| Disclaimer | Same or consciously evolved style |
| Troubleshooting format | Same Issue/Solution table pattern |

### Cross-Link Accuracy

| Check | Requirement |
|-------|-------------|
| Referenced skills exist | Every suggested skill name is a real skill in the repo |
| Suggestions make sense | Don't suggest a Python skill for a JavaScript project |
| Detection commands work | Frontend/backend detection bash commands are real |

## Final Verification

Run these before the last commit:

```bash
# 1. Verify all files exist and SKILL.md is focused (not bloated with deep-dive content)

# 2. All files exist
find skills/sentry-<platform>-sdk -type f | sort

# 3. Frontmatter valid
head -5 skills/sentry-<platform>-sdk/SKILL.md
# Must start with ---

# 4. No TODO/FIXME left behind
grep -r "TODO\|FIXME\|XXX\|HACK" skills/sentry-<platform>-sdk/

# 5. Referenced skills exist
grep -oP 'sentry-[\w-]+' skills/sentry-<platform>-sdk/SKILL.md | sort -u
# Verify each exists in skills/
```

---

## Reference: Research Playbook

# Research Playbook

How to research a Sentry SDK systematically using parallel agent tasks. This is the exact pattern that produced the Go and Svelte SDK skills.

## Principles

1. **Never write skills from memory** — always research current docs first
2. **Write to files, not inline** — research is 500–1200 lines per topic; keep it out of your context
3. **Parallel where possible** — batch independent research tasks
4. **Verify the output** — check line counts, look for real headings, re-run failures
5. **Source-verify critical APIs** — after research, verify key API names against GitHub source

## Research File Location

Store all research in a persistent directory the workers can access later:

```
~/.pi/history/<project>/research/<sdk>-<topic>.md
```

Examples:
```
~/.pi/history/sentry-agent-skills/research/go-setup-config.md
~/.pi/history/sentry-agent-skills/research/go-error-monitoring.md
~/.pi/history/sentry-agent-skills/research/svelte-setup-errors.md
```

## Prompt Templates

### Batch 1: Setup & Configuration

```
Research the Sentry <Platform> SDK setup and configuration. Visit these pages
and extract ALL technical details:

1. https://docs.sentry.io/platforms/<platform>/ — main setup page
2. https://docs.sentry.io/platforms/<platform>/configuration/ — configuration
3. https://docs.sentry.io/platforms/<platform>/configuration/options/ — init options

Document:
- Installation command (package manager)
- Init function full configuration with ALL options
- Options struct/object fields with types and defaults
- Environment variables the SDK reads
- Framework integrations — how to detect and configure each
- Flush/shutdown patterns
- Debug mode
- Release/environment detection

Include exact code examples. Accuracy matters more than brevity.
```

### Batch 2: Error Monitoring

```
Research Sentry <Platform> SDK error monitoring capabilities. Visit:

1. https://docs.sentry.io/platforms/<platform>/usage/
2. https://docs.sentry.io/platforms/<platform>/enriching-events/
3. https://docs.sentry.io/platforms/<platform>/enriching-events/context/
4. https://docs.sentry.io/platforms/<platform>/enriching-events/tags/
5. https://docs.sentry.io/platforms/<platform>/enriching-events/breadcrumbs/
6. https://docs.sentry.io/platforms/<platform>/enriching-events/scopes/

Document:
- Capture APIs (captureException, captureMessage, etc.)
- Panic/exception recovery patterns
- Hub and Scope management
- Context enrichment: tags, user, breadcrumbs, extra data
- Error wrapping / error chains
- BeforeSend hooks for filtering/modifying events
- Fingerprinting and custom grouping

Include real code examples from the docs.
```

### Batch 3: Tracing + Profiling

```
Research Sentry <Platform> SDK tracing AND profiling. Visit:

1. https://docs.sentry.io/platforms/<platform>/tracing/
2. https://docs.sentry.io/platforms/<platform>/tracing/instrumentation/
3. https://docs.sentry.io/platforms/<platform>/tracing/instrumentation/custom-instrumentation/
4. https://docs.sentry.io/platforms/<platform>/distributed-tracing/
5. https://docs.sentry.io/platforms/<platform>/profiling/

For tracing: sample rates, custom spans, framework middleware, distributed tracing,
operation types, dynamic sampling.

For profiling: sample rate config, how it attaches to traces, limitations,
or if profiling was removed/is not available.

Include exact code examples.
```

### Batch 4: Logging + Metrics + Crons

```
Research Sentry <Platform> SDK logging, metrics, AND crons. Visit:

1. https://docs.sentry.io/platforms/<platform>/logs/
2. https://docs.sentry.io/platforms/<platform>/metrics/
3. https://docs.sentry.io/platforms/<platform>/crons/

For logging: enable flag, logger API, integration with popular <platform>
logging libraries, log filtering.

For metrics: counters, gauges, distributions, sets, units, attributes.
Note if metrics are GA, beta, or experimental.

For crons: check-in API, monitor config, schedule types, heartbeat patterns.

If any feature is NOT available for <platform>, explicitly note that.
Include exact code examples.
```

### Batch 5: Frontend-Specific (Session Replay + AI Monitoring)

```
Research Sentry <Platform> SDK session replay and AI monitoring. Visit:

1. https://docs.sentry.io/platforms/<platform>/session-replay/
2. https://docs.sentry.io/platforms/<platform>/session-replay/configuration/
3. https://docs.sentry.io/platforms/<platform>/session-replay/privacy/
4. https://docs.sentry.io/platforms/<platform>/guides/ai-monitoring/ (if exists)

For session replay: integration setup, sample rates, privacy masking,
network capture, canvas recording, lazy loading.

For AI monitoring: supported AI SDKs, auto vs manual instrumentation,
token tracking, prompt capture (PII considerations).

If either feature is NOT available, explicitly note that.
```

## Execution Pattern

```python
# Pseudocode for the research phase

# 1. Determine batches based on SDK type
batches = [
    ("setup-config", batch_1_prompt),
    ("error-monitoring", batch_2_prompt),
    ("tracing-profiling", batch_3_prompt),
    ("logging-metrics-crons", batch_4_prompt),
]
if is_frontend_sdk:
    batches.append(("replay-ai", batch_5_prompt))

# 2. Run all batches in parallel
for topic, prompt in batches:
    claude(
        prompt=prompt.format(platform=platform),
        outputFile=f"~/.pi/history/{project}/research/{sdk}-{topic}.md"
    )

# 3. Verify outputs
for topic, _ in batches:
    file = f"~/.pi/history/{project}/research/{sdk}-{topic}.md"
    lines = count_lines(file)
    if lines < 100:
        print(f"WARNING: {file} only has {lines} lines — re-run")

# 4. Re-run any failures
```

## Verification Research

After workers create the skill files, run one final verification:

```
Verify these specific API names and signatures against the <SDK> GitHub repo
(<repo-url>). For each, state whether it EXISTS or NOT, the correct API if
different, and the source URL:

1. <API from skill file>
2. <Config option from skill file>
3. <Integration name from skill file>
...
```

### What To Verify

| Category | Examples to check |
|----------|------------------|
| Init options | Field names, types, casing (SendDefaultPII vs SendDefaultPii) |
| Feature flags | EnableLogs, EnableTracing — do they exist? |
| Config keys | experimental.tracing, ignoreSpans — real or fabricated? |
| Deprecated APIs | configureScope → getIsolationScope |
| Removed features | Profiling in Go SDK (removed v0.31.0) |
| Minimum versions | Cross-reference changelog for when features were added |

## Common Research Failures

| Symptom | Cause | Fix |
|---------|-------|-----|
| File has 0 lines | Claude Code failed silently | Re-run the task |
| File has <100 lines | Partial failure, only process notes captured | Re-run with simpler prompt |
| APIs don't match source | Research hallucinated or used old docs | Run verification against GitHub |
| Missing framework support | Research didn't visit framework-specific pages | Add framework URLs to prompt |
| Wrong minimum versions | Docs page was out of date | Check SDK changelog on GitHub |
