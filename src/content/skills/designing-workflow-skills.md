---
title: "Designing Workflow Skills"
description: "Guides the design and structuring of workflow-based Claude Code skills with multi-step phases, decision trees, subagent delegation, and progressive disclosure. Use when creating skills that involve sequential pipelines, routing patterns, safety ga..."
category: "devops"
source: "community"
author: "Community"
tags: ["designing", "workflow"]
date: 2026-03-20
---

# Designing Workflow Skills

Build workflow-based skills that execute reliably by following structural patterns, not prose.

## Essential Principles

<essential_principles>

<principle name="description-is-the-trigger">
**The `description` field is the only thing that controls when a skill activates.**

Claude decides whether to load a skill based solely on its frontmatter `description`. The body of SKILL.md — including "When to Use" and "When NOT to Use" sections — is only read AFTER the skill is already active. Put your trigger keywords, use cases, and exclusions in the description. A bad description means wrong activations or missed activations regardless of what the body says.

"When to Use" and "When NOT to Use" sections still serve a purpose: they scope the LLM's behavior once active. "When NOT to Use" should name specific alternatives: "use Semgrep for simple pattern matching" not "not for simple tasks."
</principle>

<principle name="numbered-phases">
**Phases must be numbered with entry and exit criteria.**

Unnumbered prose instructions produce unreliable execution order. Every phase needs:
- A number (Phase 1, Phase 2, ...)
- Entry criteria (what must be true before starting)
- Numbered actions (what to do)
- Exit criteria (how to know it's done)
</principle>

<principle name="tools-match-executor">
**Tools must match the executor.**

Skills use `allowed-tools:` in frontmatter. Agents use `tools:` in frontmatter. Subagents get tools from their `subagent_type`. Never list tools the component doesn't use. Never use Bash for operations that have dedicated tools (Glob, Grep, Read, Write, Edit).

Most skills and agents should include `TodoRead` and `TodoWrite` in their tool list — these enable progress tracking during multi-step execution and are useful even for skills that don't explicitly manage tasks.
</principle>

<principle name="progressive-disclosure">
**Progressive disclosure is structural, not optional.**

SKILL.md stays under 500 lines. It contains only what the LLM needs for every invocation: principles, routing, quick references, and links. Detailed patterns go in `references/`. Step-by-step processes go in `workflows/`. One level deep — no reference chains.
</principle>

<principle name="scalable-tool-patterns">
**Instructions must produce tool-calling patterns that scale.**

Every workflow instruction becomes tool calls at runtime. If a workflow searches N files for M patterns, combine into one regex — not N×M calls. If a workflow spawns subagents per item, use batching — not one subagent per file. Apply the 10,000-file test: mentally run the workflow against a large repo and check that tool call count stays bounded. See [anti-patterns.md](references/anti-patterns.md) AP-18 and AP-19.
</principle>

<principle name="degrees-of-freedom">
**Match instruction specificity to task fragility.**

Not every step needs the same level of prescription. Calibrate per step:
- **Low freedom** (exact commands, no variation): Fragile operations — database migrations, crypto, destructive actions. "Run exactly this script."
- **Medium freedom** (pseudocode with parameters): Preferred patterns where variation is acceptable. "Use this template and customize as needed."
- **High freedom** (heuristics and judgment): Variable tasks — code review, exploration, documentation. "Analyze the structure and suggest improvements."

A skill can mix freedom levels. A security audit skill might use high freedom for the discovery phase ("explore the codebase for auth patterns") and low freedom for the reporting phase ("use exactly this severity classification table").
</principle>

</essential_principles>

## When to Use

- Designing a new skill with multi-step workflows or phased execution
- Creating a skill that routes between multiple independent tasks
- Building a skill with safety gates (destructive actions requiring confirmation)
- Structuring a skill that uses subagents or task tracking
- Reviewing or refactoring an existing workflow skill for quality
- Deciding how to split content between SKILL.md, references/, and workflows/

## When NOT to Use

- Simple single-purpose skills with no workflow (just guidance) — write the SKILL.md directly
- Writing the actual domain content of a skill (this teaches structure, not domain expertise)
- Plugin configuration (plugin.json, hooks, commands) — use plugin development guides
- Non-skill Claude Code development — this is specifically for skill architecture

## Pattern Selection

Choose the right pattern for your skill's structure. Read the full pattern description in [workflow-patterns.md](references/workflow-patterns.md).

```
How many distinct paths does the skill have?
|
+-- One path, always the same
|   +-- Does it perform destructive actions?
|       +-- YES -> Safety Gate Pattern
|       +-- NO  -> Linear Progression Pattern
|
+-- Multiple independent paths from shared setup
|   +-- Routing Pattern
|
+-- Multiple dependent steps in sequence
    +-- Do steps have complex dependencies?
        +-- YES -> Task-Driven Pattern
        +-- NO  -> Sequential Pipeline Pattern
```

### Pattern Summary

| Pattern | Use When | Key Feature |
|---------|----------|-------------|
| **Routing** | Multiple independent tasks from shared intake | Routing table maps intent to workflow files |
| **Sequential Pipeline** | Dependent steps, each feeding the next | Auto-detection may resume from partial progress |
| **Linear Progression** | Single path, same every time | Numbered phases with entry/exit criteria |
| **Safety Gate** | Destructive/irreversible actions | Two confirmation gates before execution |
| **Task-Driven** | Complex dependencies, partial failure tolerance | TaskCreate/TaskUpdate with dependency tracking |

## Structural Anatomy

Every workflow skill needs this skeleton, regardless of pattern:

```markdown
---
name: kebab-case-name
description: "Third-person description with trigger keywords — this is how Claude decides to activate the skill"
allowed-tools:
  - [minimum tools needed]
# Optional fields — see tool-assignment-guide.md for full reference:
# disable-model-invocation: true    # Only user can invoke (not Claude)
# user-invocable: false             # Only Claude can invoke (hidden from / menu)
# context: fork                     # Run in isolated subagent context
# agent: Explore                    # Subagent type (requires context: fork)
# model: [model-name]               # Switch model when skill is active
# argument-hint: "[filename]"       # Hint shown during autocomplete
---

# Title

## Essential Principles
[3-5 non-negotiable rules with WHY explanations]

## When to Use
[4-6 specific scenarios — scopes behavior after activation]

## When NOT to Use
[3-5 scenarios with named alternatives — scopes behavior after activation]

## [Pattern-Specific Section]
[Routing table / Pipeline steps / Phase list / Gates]

## Quick Reference
[Compact tables for frequently-needed info]

## Reference Index
[Links to all supporting files]

## Success Criteria
[Checklist for output validation]
```

Skills support three types of string substitutions: dollar-prefixed variables for arguments and session ID, and exclamation-backtick syntax for shell preprocessing. The skill loader processes these before Claude sees the file — even inside code fences — so never use the raw syntax in documentation text. See [tool-assignment-guide.md](references/tool-assignment-guide.md) for the full variable reference and usage guidance.

## Anti-Pattern Quick Reference

The most common mistakes. Full catalog with before/after fixes in [anti-patterns.md](references/anti-patterns.md).

| AP | Anti-Pattern | One-Line Fix |
|----|-------------|-------------|
| AP-1 | Missing goals/anti-goals | Add When to Use AND When NOT to Use sections |
| AP-2 | Monolithic SKILL.md (>500 lines) | Split into references/ and workflows/ |
| AP-3 | Reference chains (A -> B -> C) | All files one hop from SKILL.md |
| AP-4 | Hardcoded paths | Use `{baseDir}` for all internal paths |
| AP-5 | Broken file references | Verify every path resolves before submitting |
| AP-6 | Unnumbered phases | Number every phase with entry/exit criteria |
| AP-7 | Missing exit criteria | Define what "done" means for every phase |
| AP-8 | No verification step | Add validation at the end of every workflow |
| AP-9 | Vague routing keywords | Use distinctive keywords per workflow route |
| AP-11 | Wrong tool for the job | Use Glob/Grep/Read, not Bash equivalents |
| AP-12 | Overprivileged tools | Remove tools not actually used |
| AP-13 | Vague subagent prompts | Specify what to analyze, look for, and return |
| AP-15 | Reference dumps | Teach judgment, not raw documentation |
| AP-16 | Missing rationalizations | Add "Rationalizations to Reject" for audit skills |
| AP-17 | No concrete examples | Show input -> output for key instructions |
| AP-18 | Cartesian product tool calls | Combine patterns into single regex, grep once, then filter |
| AP-19 | Unbounded subagent spawning | Batch items into groups, one subagent per batch |
| AP-20 | Description summarizes workflow | Description = triggering conditions only, never workflow steps |

*AP-10 (No Default/Fallback Route), AP-14 (Missing Tool Justification in Agents), and AP-20 (Description Summarizes Workflow) are in the [full catalog](references/anti-patterns.md). AP-20 is included in the quick reference above due to its high impact.*

## Tool Assignment Quick Reference

Map your component type to the right tool set. Full guide in [tool-assignment-guide.md](references/tool-assignment-guide.md).

| Component Type | Typical Tools |
|---------------|---------------|
| Read-only analysis skill | Read, Glob, Grep, TodoRead, TodoWrite |
| Interactive analysis skill | Read, Glob, Grep, AskUserQuestion, TodoRead, TodoWrite |
| Code generation skill | Read, Glob, Grep, Write, Bash, TodoRead, TodoWrite |
| Pipeline skill | Read, Write, Glob, Grep, Bash, AskUserQuestion, Task, TaskCreate, TaskList, TaskUpdate, TodoRead, TodoWrite |
| Read-only agent | Read, Grep, Glob, TodoRead, TodoWrite |
| Action agent | Read, Grep, Glob, Write, Bash, TodoRead, TodoWrite |

**Key rules:**
- Use Glob (not `find`), Grep (not `grep`), Read (not `cat`) — always prefer dedicated tools
- Skills use `allowed-tools:` — agents use `tools:`
- List only tools that instructions actually reference
- Read-only components should never have Write or Bash

## Rationalizations to Reject

When designing workflow skills, reject these shortcuts:

| Rationalization | Why It's Wrong |
|-----------------|----------------|
| "It's obvious which phase comes next" | LLMs don't infer ordering from prose. Number the phases. |
| "Exit criteria are implied" | Implied criteria are skipped criteria. Write them explicitly. |
| "One big SKILL.md is simpler" | Simpler to write, worse to execute. The LLM loses focus past 500 lines. |
| "The description doesn't matter much" | The description is how the skill gets triggered. A bad description means wrong activations or missed activations. |
| "Bash can do everything" | Bash file operations are fragile. Dedicated tools handle encoding, permissions, and formatting better. |
| "The LLM will figure out the tools" | It will guess wrong. Specify exactly which tool for each operation. |
| "I'll add details later" | Incomplete skills ship incomplete. Design fully before writing. |

## Reference Index

| File | Content |
|------|---------|
| [workflow-patterns.md](references/workflow-patterns.md) | 5 patterns with structural skeletons and examples |
| [anti-patterns.md](references/anti-patterns.md) | 20 anti-patterns with before/after fixes |
| [tool-assignment-guide.md](references/tool-assignment-guide.md) | Tool selection matrix, component comparison, subagent guidance |
| [progressive-disclosure-guide.md](references/progressive-disclosure-guide.md) | Content splitting rules, the 500-line rule, sizing guidelines |

| Workflow | Purpose |
|----------|---------|
| [design-a-workflow-skill.md](workflows/design-a-workflow-skill.md) | 6-phase creation process from scope to self-review |
| [review-checklist.md](workflows/review-checklist.md) | Structured self-review checklist for submission readiness |

## Success Criteria

A well-designed workflow skill:

- [ ] Has When to Use AND When NOT to Use sections
- [ ] Uses a recognizable pattern (routing, pipeline, linear, safety gate, or task-driven)
- [ ] Numbers all phases with entry and exit criteria
- [ ] Lists only the tools it actually uses (least privilege)
- [ ] Keeps SKILL.md under 500 lines with details in references/workflows
- [ ] Has no hardcoded paths (uses `{baseDir}`)
- [ ] Has no broken file references
- [ ] Has no reference chains (all links one hop from SKILL.md)
- [ ] Includes a verification step at the end of the workflow
- [ ] Has a description that triggers correctly (third-person, specific keywords)
- [ ] Includes concrete examples for key instructions
- [ ] Explains WHY, not just WHAT, for essential principles

---

## Reference: Anti Patterns

# Anti-Patterns Catalog

Common mistakes in workflow-based skills, organized by category. Each anti-pattern includes the symptom, why it's wrong, and a before/after fix.

---

## Structure Anti-Patterns

### AP-1: Vague Description and Missing Scope Sections

**Symptom:** Skill has a vague `description` in frontmatter and no "When to Use" or "When NOT to Use" sections in the body.

**Why it's wrong:** Claude decides whether to activate a skill based solely on the `description` field. A vague description causes wrong activations or missed activations. Once active, "When to Use" and "When NOT to Use" sections scope the LLM's behavior — without them, the LLM attempts tasks outside the skill's competence.

**Before:**
```markdown
---
name: analyzing-logs
description: "Analyzes log files"
---
# Log Analysis
Here's how to analyze logs...
```

**After:**
```markdown
---
name: analyzing-logs
description: >-
  Analyzes structured log files (JSON, logfmt) for error triage,
  cross-service event correlation, and recurring pattern detection.
  Use when triaging application errors or investigating incidents.
  NOT for real-time monitoring, binary files, or metrics/tracing.
---

## When to Use
- Triaging application errors from structured log files (JSON, logfmt)
- Correlating log events across multiple services
- Identifying recurring error patterns over time

## When NOT to Use
- Real-time log monitoring — use dedicated observability tools
- Binary file analysis — this skill handles text-based logs only
- Metrics or tracing analysis — use APM-specific skills
```

The `description` controls activation. The body sections scope behavior after activation.

**Format rule:** Start descriptions with triggering conditions ("Use when..."), use third-person voice ("Analyzes X" not "I analyze X"), and include specific trigger keywords. See also AP-20 for the related trap of putting workflow steps in the description.

---

### AP-2: Monolithic SKILL.md

**Symptom:** SKILL.md exceeds 500 lines with everything inlined.

**Why it's wrong:** Oversized files dilute the LLM's attention. Critical instructions get buried in reference material. The skill triggers correctly but executes poorly because the LLM cannot prioritize.

**Before:** A 900-line SKILL.md with full API documentation, examples, and workflow steps all in one file.

**After:** SKILL.md under 500 lines with core principles and routing. Detailed reference material in `references/`. Step-by-step processes in `workflows/`. SKILL.md links to these with one-line summaries.

---

### AP-3: Reference Chains

**Symptom:** SKILL.md links to file A, which links to file B, which links to file C.

**Why it's wrong:** The LLM follows chains linearly. By the time it reaches file C, the context from SKILL.md has degraded. Each hop adds latency and increases the chance of the LLM stopping early.

**Before:**
```
SKILL.md -> references/setup.md -> references/advanced-setup.md -> references/edge-cases.md
```

**After:**
```
SKILL.md -> references/setup.md (includes advanced and edge cases)
SKILL.md -> references/edge-cases.md (standalone)
```

All files are one hop from SKILL.md. Files do not reference other reference files.

---

### AP-4: Hardcoded Paths

**Symptom:** File contains absolute paths like `/Users/jane/projects/skill/scripts/run.py`.

**Why it's wrong:** The skill breaks for any user whose filesystem differs. This is always wrong, with no exceptions.

**Before:**
```markdown
Run the script:
\`\`\`bash
python /Users/jane/projects/my-skill/scripts/analyze.py
\`\`\`
```

**After:**
```markdown
Run the script:
\`\`\`bash
uv run {baseDir}/scripts/analyze.py
\`\`\`
```

---

### AP-5: Missing File References Validation

**Symptom:** SKILL.md references `workflows/advanced.md` but the file doesn't exist.

**Why it's wrong:** The LLM attempts to read the file, fails, and either hallucinates the content or stops. Broken references are silent failures that produce unpredictable behavior.

**Fix:** Before submitting, verify every path referenced in SKILL.md exists. Use glob to check.

---

## Workflow Design Anti-Patterns

### AP-6: Unnumbered Phases

**Symptom:** Workflow uses prose paragraphs or vague headings instead of numbered phases.

**Why it's wrong:** The LLM cannot reliably determine ordering from prose. Numbered phases with entry/exit criteria create unambiguous execution order.

**Before:**
```markdown
## Workflow
First, gather the data. Then analyze it. After that, present findings.
Make sure to validate before presenting.
```

**After:**
```markdown
## Workflow

### Phase 1: Gather Data
**Entry:** User has specified target directory
**Actions:**
1. Scan directory for relevant files
2. Validate file formats
**Exit:** File list confirmed, all formats valid

### Phase 2: Analyze
**Entry:** Phase 1 complete
**Actions:**
1. Run analysis on each file
2. Aggregate results
**Exit:** Analysis results stored in structured format

### Phase 3: Present Findings
**Entry:** Phase 2 complete
**Actions:**
1. Validate results against expected schema
2. Format and present to user
**Exit:** User has received formatted report
```

---

### AP-7: Missing Exit Criteria

**Symptom:** Phases say what to do but not how to know when it's done.

**Why it's wrong:** Without exit criteria, the LLM may produce incomplete work for a phase and move on, or loop endlessly trying to "finish" a phase with no definition of done.

**Before:**
```markdown
### Phase 2: Build Database
Build the CodeQL database from the source code.
```

**After:**
```markdown
### Phase 2: Build Database
**Entry:** Language detected, build command identified
**Actions:**
1. Run `codeql database create` with detected settings
2. Verify database creation succeeded
**Exit:** Database exists, `codeql resolve database` returns success, extracted file count > 0
```

---

### AP-8: No Verification Step

**Symptom:** The workflow ends with "output the results" and no validation.

**Why it's wrong:** LLMs can produce plausible but incorrect output. A verification step catches errors before the user acts on bad results.

**Before:**
```markdown
### Phase 3: Generate Report
Write the analysis report to output.md.
```

**After:**
```markdown
### Phase 3: Generate Report
1. Write analysis report to output.md
2. Verify: all input files are represented in the report
3. Verify: no placeholder text remains
4. Verify: all referenced paths exist

Report to user:
- Key findings (2-3 bullet points)
- Any warnings or limitations
```

---

### AP-9: Vague Routing Keywords

**Symptom:** Multiple workflows match the same user input because routing keywords overlap.

**Why it's wrong:** Ambiguous routing causes the LLM to pick the wrong workflow or freeze deciding between them.

**Before:**
```markdown
| "analyze" | `workflows/static-analysis.md` |
| "analyze code" | `workflows/dynamic-analysis.md` |
```

**After:**
```markdown
| "static", "scan", "lint", "find bugs" | `workflows/static-analysis.md` |
| "dynamic", "fuzz", "runtime", "execute" | `workflows/dynamic-analysis.md` |
```

Use distinctive keywords per workflow. If two workflows genuinely overlap, add a disambiguation step.

---

### AP-10: No Default/Fallback Route

**Symptom:** Routing table covers known options but has no catch-all.

**Why it's wrong:** When user input doesn't match any route, the LLM improvises. The improvised behavior is unpredictable and usually wrong.

**Before:** Routing table with 5 specific options and nothing else.

**After:**
```markdown
| None of the above | Ask user to clarify: "I can help with X, Y, or Z. Which would you like?" |
```

---

## Tool and Agent Anti-Patterns

### AP-11: Wrong Tool for the Job

**Symptom:** Skill uses `Bash` with `grep` instead of the `Grep` tool, or `Bash` with `find` instead of `Glob`.

**Why it's wrong:** Dedicated tools (Glob, Grep, Read) are optimized for their purpose, handle edge cases (permissions, encoding), and provide better output formatting. Bash equivalents are fragile and verbose.

**Before:**
```markdown
allowed-tools:
  - Bash
```
```markdown
Find all Python files:
\`\`\`bash
find . -name "*.py" -type f
\`\`\`
```

**After:**
```markdown
allowed-tools:
  - Glob
  - Grep
  - Read
```
```markdown
Find all Python files using Glob with pattern `**/*.py`.
```

---

### AP-12: Overprivileged Tool Lists

**Symptom:** Skill lists tools it never uses, or includes Write/Bash for a read-only analysis skill.

**Why it's wrong:** Extra tools expand the attack surface. A read-only analysis skill with Write access might create files the user didn't expect. Principle of least privilege applies.

**Before:**
```yaml
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - Task
  - AskUserQuestion
```

**After (for a read-only analysis skill):**
```yaml
allowed-tools:
  - Read
  - Glob
  - Grep
```

Only list tools the skill actually needs. Audit by checking which tools appear in instructions.

---

### AP-13: Vague Subagent Instructions

**Symptom:** Spawning a subagent with "analyze this code" and no specific instructions.

**Why it's wrong:** Subagents start fresh with no context. They need explicit instructions about what to look for, what format to produce, and what tools to use.

**Before:**
```markdown
Spawn a subagent to analyze the function.
```

**After:**
```markdown
Spawn a Task agent (subagent_type=Explore) with prompt:
"Read the function `processInput` in `src/handler.py`. List all external
calls it makes, what validation is performed on inputs, and whether any
input reaches a shell command or SQL query without sanitization.
Return findings as a markdown list."
```

---

### AP-14: Missing Tool Justification in Agents

**Symptom:** Agent frontmatter lists tools without the agent body explaining when to use each one.

**Why it's wrong:** Agents with ambiguous tool access make inconsistent choices about which tool to use for a given operation.

**Before:**
```yaml
tools: Read, Grep, Glob, Bash, Write
```
(Agent body never mentions when to use which tool.)

**After:**
```yaml
tools: Read, Grep, Glob
```
```markdown
## Tool Usage
- **Glob** to find files by pattern (e.g., `**/*.sol`, `**/SKILL.md`)
- **Read** to examine file contents after finding them
- **Grep** to search for specific patterns across files (e.g., `{baseDir}`, hardcoded paths)
```

---

## Content Anti-Patterns

### AP-15: Reference Dump Instead of Guidance

**Symptom:** Skill pastes a full specification or API reference instead of teaching when and how to use it.

**Why it's wrong:** The LLM already has general knowledge. What it needs is judgment: when to apply technique A vs B, what tradeoffs to consider, what mistakes to avoid.

**Before:** 200 lines of API documentation copied from official docs.

**After:**
```markdown
## When to Use X vs Y

Use X when:
- Input is structured and schema is known
- Performance matters (X is 10x faster)

Use Y when:
- Input format varies
- You need human-readable intermediate output

**Common mistake:** Using Y for structured input because it "feels safer."
Y's flexibility is overhead when the schema is known.
```

---

### AP-16: Missing Rationalizations Section

**Symptom:** Security/audit skill has no "Rationalizations to Reject" section.

**Why it's wrong:** LLMs naturally take shortcuts. Without explicit rationalization rejection, the LLM talks itself into skipping important steps. This is the #1 cause of missed findings in audit skills.

**Before:** Skill describes what to do but not what shortcuts to avoid.

**After:**
```markdown
## Rationalizations to Reject

| Rationalization | Why It's Wrong |
|-----------------|----------------|
| "The code looks clean, skip deep analysis" | Surface appearance doesn't indicate security. Analyze every entry point. |
| "This is a well-known library, it's safe" | Libraries have bugs. Check the specific version and usage pattern. |
| "No findings means the code is secure" | Zero findings may indicate poor analysis, not good code. |
```

---

### AP-17: No Concrete Examples

**Symptom:** Skill describes rules in abstract terms without showing input -> output.

**Why it's wrong:** Abstract rules are ambiguous. Concrete examples anchor the LLM's understanding and reduce interpretation drift.

**Before:**
```markdown
Ensure the output is well-formatted and includes all relevant information.
```

**After:**
```markdown
## Output Format

\`\`\`markdown
## Analysis Report

### Findings
| # | File | Line | Issue | Severity |
|---|------|------|-------|----------|
| 1 | src/auth.py | 42 | SQL injection via unsanitized user input | High |

### Summary
- 3 findings total (1 high, 2 medium)
- Primary risk area: input validation in authentication module
\`\`\`
```

---

## Scalability Anti-Patterns

### AP-18: Cartesian Product Tool Calls

**Symptom:** Skill says "find all matching files, then search each file for each pattern" — producing N files × M patterns = N×M tool calls.

**Why it's wrong:** The agent won't actually execute N×M calls. It will shortcut — scanning a few files, skipping patterns, or summarizing early — and miss results silently. Even if it tries, the volume of calls degrades response quality and exhausts context.

**Before:**
```markdown
### Phase 2: Search for Vulnerabilities
1. Use Glob to find all `.sol` files
2. Filter out test paths
3. For each file, Grep for each of these 12 patterns:
   - `delegatecall`
   - `selfdestruct`
   - `tx.origin`
   - `block.timestamp`
   - ... (8 more patterns)
```

**After:**
```markdown
### Phase 2: Search for Vulnerabilities
1. Grep the codebase for `delegatecall|selfdestruct|tx\.origin|block\.timestamp|...` (single combined regex)
2. Filter results to exclude test paths (`**/test/**`, `**/mock/**`)
3. Read matching files for context around each hit
```

Combine patterns into one regex. Grep once across the codebase. Filter results afterward.

---

### AP-19: Unbounded Subagent Spawning

**Symptom:** Skill says "spawn one subagent per file" or "one subagent per function" — subagent count scales with codebase size.

**Why it's wrong:** With 1000 files, that's 1000 subagents. The agent will hit context limits, refuse, or produce degraded results long before finishing. Even with 50 files, spawning 50 subagents creates massive overhead and unpredictable execution.

**Before:**
```markdown
### Phase 3: Analyze Code
For each code file discovered in Phase 2, spawn a Task subagent to:
- Read the file
- Build a summary of its public API
- Identify potential issues
```

**After:**
```markdown
### Phase 3: Analyze Code
Batch discovered files into groups of 10-20. For each batch, spawn a single Task subagent with prompt:
"Read the following files: [list]. For each file, summarize its public API and identify potential issues. Return a markdown table with one row per file."
```

Batch items into fixed-size groups. One subagent per batch, not one per item.

---

## Description Anti-Patterns

### AP-20: Description Summarizes Workflow

**Symptom:** The `description` field summarizes the skill's workflow steps instead of listing triggering conditions.

**Why it's wrong:** Claude treats the description as an executive summary. When it contains workflow steps ("dispatches subagent per task with code review between tasks"), Claude follows the description and shortcuts past the actual SKILL.md body. A description saying "code review between tasks" caused Claude to do ONE review, even though the SKILL.md flowchart showed TWO reviews (spec compliance then code quality). When the description was changed to triggering conditions only, Claude correctly read and followed the full process.

**Before:**
```markdown
---
name: subagent-driven-development
description: >-
  Use when executing plans — dispatches subagent per task
  with code review between tasks for quality assurance
---
```

**After:**
```markdown
---
name: subagent-driven-development
description: >-
  Use when executing implementation plans with independent
  tasks in the current session
---
```

The description should contain ONLY triggering conditions ("Use when..."), never workflow steps. Process details belong in the SKILL.md body.

---

## Reference: Progressive Disclosure Guide

# Progressive Disclosure Guide

How to split skill content across files so the LLM prioritizes correctly.

---

## The 500-Line Rule

SKILL.md must stay under 500 lines. This is not arbitrary — it's the threshold where LLM attention degrades. Beyond 500 lines, instructions at the bottom of SKILL.md get less weight than instructions at the top.

If your SKILL.md exceeds 500 lines, split content into `references/` and `workflows/`.

---

## What Goes Where

### SKILL.md (always read first)

Content the LLM needs for **every** invocation:

- Frontmatter (name, description, allowed-tools) — description controls activation
- Essential principles (5-7 non-negotiable rules)
- When to Use / When NOT to Use (behavioral scope, not activation triggers)
- Routing logic or pattern selection (if applicable)
- Quick reference tables (compact summaries)
- Reference index (links to all supporting files)
- Success criteria checklist

**Test:** If removing this content would cause the LLM to produce wrong output on any invocation, it belongs in SKILL.md.

### references/ (read on demand)

Detailed knowledge the LLM needs for **specific** tasks:

- Full pattern descriptions with examples
- Complete anti-pattern catalogs
- API references
- Domain-specific knowledge
- Tool documentation

**Test:** If this content is only needed for some invocations (e.g., one workflow path but not others), it belongs in references/.

### workflows/ (read for specific processes)

Step-by-step procedures:

- Multi-phase processes
- Checklists
- Decision procedures
- Specific task guides

**Test:** If this content is a series of ordered steps to follow for a specific task, it belongs in workflows/.

---

## File Naming

Use kebab-case descriptive names:

| Good | Bad |
|------|-----|
| `workflow-patterns.md` | `patterns.md` (too vague) |
| `anti-patterns.md` | `bad-stuff.md` (unprofessional) |
| `tool-assignment-guide.md` | `tools.md` (too vague) |
| `design-a-workflow-skill.md` | `workflow.md` (ambiguous) |
| `review-checklist.md` | `checklist.md` (which checklist?) |

The filename should tell you what's inside without opening it.

---

## The One-Level-Deep Rule

SKILL.md links to reference and workflow files. Those files do NOT link to other reference files.

```
ALLOWED:
SKILL.md -> references/patterns.md
SKILL.md -> references/anti-patterns.md
SKILL.md -> workflows/build-process.md

NOT ALLOWED:
references/patterns.md -> references/pattern-details.md
workflows/build-process.md -> references/build-config.md
```

**Why:** Each hop degrades context. By the second hop, the LLM has lost track of where it started and why. If a reference file needs content from another reference file, either merge them or restructure so SKILL.md links to both directly.

**Exception:** Directory nesting for organization is fine (`references/guides/topic.md`). The restriction is on *reference chains* (file A telling the LLM to go read file B), not on directory depth.

---

## Sizing Guidelines

| File type | Target size | Maximum |
|-----------|-------------|---------|
| SKILL.md | 200-400 lines | 500 lines |
| Reference file | 100-300 lines | 400 lines |
| Workflow file | 80-200 lines | 300 lines |
| Agent definition | 80-200 lines | 300 lines |

If a reference file exceeds 400 lines, split it into two files that SKILL.md links to separately.

---

## Progressive Disclosure in Practice

Structure SKILL.md as a funnel: broad overview first, details via links.

```markdown
## Essential Principles     <- Always read (5-7 bullet points)
## When to Use / NOT        <- Scopes behavior (not activation — that's the description)
## Decision Tree            <- Routes to the right pattern
## Quick Reference Table    <- Compact summary (10-15 rows)
## Reference Index          <- Links to detailed files
## Success Criteria         <- Final checklist
```

The LLM reads top-to-bottom. Front-load what matters for every invocation. Push details into files that are only read when needed.

---

## Reference: Tool Assignment Guide

# Tool Assignment Guide

How to choose the right tools for skills, agents, and subagents.

---

## Skills vs Agents vs Subagents

| Component | What it is | When to use | How it's triggered |
|-----------|-----------|-------------|-------------------|
| **Skill** | Knowledge/guidance (SKILL.md) | Teaching patterns, providing domain expertise, guiding decisions | Auto-activated when frontmatter `description` matches user intent |
| **Agent** | Autonomous executor (agents/*.md) | Tasks that run independently, produce structured output | Spawned via Task tool with `subagent_type` |
| **Subagent** | Agent spawned by another agent | Delegating subtasks within a larger workflow | Parent agent uses Task tool |
| **Command** | User-invoked action (commands/*.md) | Explicit operations the user triggers with `/command-name` | User types the slash command |
| **Hook** | Event-driven interceptor (hooks/) | Validating or transforming tool calls automatically | System events (PreToolUse, PostToolUse, etc.) |
| **LSP Server** | Code intelligence provider (.lsp.json) | Language-specific completions, diagnostics, hover info | Plugin includes `.lsp.json` config |

**Decision:** If the user should invoke it explicitly, make it a command. If it should trigger automatically based on context, make it a skill. If it runs autonomously to produce output, make it an agent.

---

## Skill Frontmatter Reference

| Field | Required | Description |
|-------|----------|-------------|
| `name` | No | Display name (kebab-case, max 64 chars). Defaults to directory name. |
| `description` | Recommended | What it does and when to use it. **Controls skill activation.** |
| `allowed-tools` | No | Tools Claude can use without asking when skill is active. |
| `disable-model-invocation` | No | Set `true` to prevent Claude from auto-loading. User invokes with `/name`. |
| `user-invocable` | No | Set `false` to hide from `/` menu. Claude can still invoke. |
| `context` | No | Set `fork` to run in an isolated subagent context. Skill content becomes the subagent prompt. |
| `agent` | No | Subagent type when `context: fork` is set (e.g., `Explore`, `Plan`). Defaults to `general-purpose`. |
| `model` | No | Switch model when skill is active. |
| `argument-hint` | No | Hint shown during autocomplete (e.g., `[issue-number]`). |
| `hooks` | No | Lifecycle-scoped hooks for this skill. |

**Invocation control:**

| Setting | User can invoke | Claude can invoke | Description in context |
|---------|----------------|-------------------|----------------------|
| (default) | Yes | Yes | Yes |
| `disable-model-invocation: true` | Yes | No | No |
| `user-invocable: false` | No | Yes | Yes |

---

## String Substitutions

Skill content supports dynamic values at invocation time. **CAUTION:** The skill loader processes these substitutions before Claude sees the file — even inside code fences and inline code blocks. Do not use the raw syntax in documentation or example text. Variables silently resolve to empty strings, and shell preprocessing attempts execution, causing load errors.

There are three substitution types:

1. **Argument variables** — A dollar sign followed by ARGUMENTS for all args, or a dollar sign followed by ARGUMENTS[N] or just a dollar sign followed by N for positional args (0-based index, where N is shorthand for ARGUMENTS[N]). If no placeholder exists in the content, arguments are appended as an `ARGUMENTS:` line.

2. **Session variable** — A dollar sign followed by {CLAUDE_SESSION_ID} (with curly braces) resolves to the current session ID.

3. **Shell preprocessing** — An exclamation mark immediately followed by a command enclosed in backticks. For example, to inject the output of `git status`, place an exclamation mark before the backtick-enclosed command. The command runs before Claude sees the content; its output replaces the placeholder.

**Design implications:**
- Use argument variables when the skill accepts free-form input (file paths, issue numbers)
- Use positional args when the skill expects structured input (e.g., `/migrate-component SearchBar React Vue`)
- Use shell preprocessing to inject live context (git status, PR diff) — pairs well with `context: fork`

**When documenting these patterns in a skill:** Describe the syntax textually (as this file does) rather than using the raw patterns. Code fences and inline code do NOT prevent substitution — the loader processes the raw file content before any Markdown parsing.

---

## Tool Inventory

| Tool | Purpose | Use for |
|------|---------|---------|
| **Read** | Read file contents | Examining specific files by path |
| **Glob** | Find files by pattern | Discovering files (`**/*.py`, `**/SKILL.md`) |
| **Grep** | Search file contents | Finding patterns across files |
| **Write** | Create/overwrite files | Generating output files |
| **Edit** | Modify existing files | Targeted changes to existing files |
| **Bash** | Execute shell commands | Running tools, scripts, git operations |
| **AskUserQuestion** | Get user input | Disambiguation, confirmation, preferences |
| **Task** | Spawn subagents | Delegating complex subtasks |
| **TaskCreate/TaskUpdate/TaskList** | Track progress | Multi-step workflows with dependencies |
| **TodoRead/TodoWrite** | Track progress via todo list | Most skills and agents — enables progress tracking during execution |
| **WebFetch** | Fetch URL content | Reading web pages |
| **WebSearch** | Search the web | Finding current information |

---

## Tool Selection Matrix

Map the operation you need to the correct tool:

| Operation | Correct Tool | NOT this |
|-----------|-------------|----------|
| Find files by name/pattern | **Glob** | `find` via Bash |
| Search file contents | **Grep** | `grep`/`rg` via Bash |
| Read a file | **Read** | `cat`/`head`/`tail` via Bash |
| Write a new file | **Write** | `echo`/`cat <<EOF` via Bash |
| Edit an existing file | **Edit** | `sed`/`awk` via Bash |
| Run a shell command | **Bash** | — |
| Run a Python script | **Bash** (`uv run`) | — |
| Get user confirmation | **AskUserQuestion** | Printing and hoping |
| Delegate analysis | **Task** (subagent) | Doing everything inline |

**Rule:** If a dedicated tool exists for the operation, use it. Only use Bash for operations that genuinely require shell execution (running programs, git commands, build tools).

---

## Assigning Tools to Components

### Read-Only Analysis Skills

Skills that examine code without modifying it:

```yaml
allowed-tools:
  - Read
  - Glob
  - Grep
  - TodoRead
  - TodoWrite
```

### Interactive Analysis Skills

Skills that need user input during execution:

```yaml
allowed-tools:
  - Read
  - Glob
  - Grep
  - AskUserQuestion
  - TodoRead
  - TodoWrite
```

### Code Generation Skills

Skills that produce output files:

```yaml
allowed-tools:
  - Read
  - Glob
  - Grep
  - Write
  - Bash
  - TodoRead
  - TodoWrite
```

### Pipeline Skills (Multi-Step)

Skills that orchestrate complex workflows:

```yaml
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
  - AskUserQuestion
  - Task
  - TaskCreate
  - TaskList
  - TaskUpdate
  - TodoRead
  - TodoWrite
```

### Agents

Agents declare tools in frontmatter with `tools:` (not `allowed-tools:`):

```yaml
---
name: my-agent
description: "What it does"
tools: Read, Grep, Glob, TodoRead, TodoWrite
---
```

**Agent tool principle:** Agents should have the minimum tools needed for their specific task. A read-only analysis agent should not have Write or Bash. Most agents should include `TodoRead` and `TodoWrite` for progress tracking.

---

## Subagent Context Passing

When spawning a subagent via the Task tool, include:

1. **What to analyze** — specific file paths, function names, or patterns
2. **What to look for** — explicit criteria, not vague "analyze this"
3. **What format to return** — markdown structure, JSON schema, or checklist
4. **What tools to use** — specify the subagent_type so it has appropriate tools

**Good prompt:**
```
Read all files in plugins/my-skill/skills/my-skill/. Check that:
1. SKILL.md has valid YAML frontmatter with name and description
2. All file paths referenced in SKILL.md exist
3. SKILL.md is under 500 lines
4. No hardcoded paths (/Users/, /home/)
Return a pass/fail checklist with details for each failure.
```

**Bad prompt:**
```
Review the skill and tell me if it's good.
```

### Skills with `context: fork`

A skill with `context: fork` runs its content as a subagent prompt in isolation (no conversation history). This differs from spawning subagents via the Task tool:

| Approach | System prompt | Task prompt | Use when |
|----------|--------------|-------------|----------|
| Skill + `context: fork` | From `agent` field type | SKILL.md content | Self-contained actions needing isolation (deploy, research, review) |
| Task tool subagent | Subagent's definition | Parent's delegation message | Dynamic delegation within a workflow |

**Design rule:** If the skill represents one action the user triggers directly, use `context: fork`. If a workflow needs to delegate variable subtasks at runtime, use the Task tool.

---

## Common Tool Assignment Mistakes

| Mistake | Problem | Fix |
|---------|---------|-----|
| Listing `Bash` for file operations | Fragile, verbose, permission issues | Use Read/Write/Glob/Grep |
| Listing `Write` on a read-only skill | Principle of least privilege violation | Remove Write if skill never creates files |
| Listing `Task` without using subagents | Unused tools clutter the permission model | Only list tools you actually use |
| Agent with `Bash` for `grep` | Dedicated Grep tool is more reliable | Use Grep tool instead |
| No `AskUserQuestion` on interactive skill | Skill can't get user confirmation | Add AskUserQuestion if any gate/confirmation exists |
| Missing `TaskCreate`/`TaskUpdate` on pipeline | Can't track multi-step progress | Add task tools for pipeline patterns |
| Grep per-file per-pattern | N×M tool calls, agent shortcuts and misses results | Combine patterns into single regex, grep once |
| One subagent per file | Context exhaustion, agent refuses or degrades | Batch into groups of 10-20 per subagent |

---

## Scaling Tool Calls

Instructions must produce tool-calling patterns that stay efficient regardless of codebase size. Apply the **10,000-file test**: mentally run the workflow against a 10,000-file repo. If the number of tool calls grows with input size, redesign.

### Combine-Then-Filter for Searches

When a workflow searches for multiple patterns across multiple files, combine all patterns into a single regex and grep the entire codebase once.

**Wrong:** "For each of these 10 patterns, grep all `.sol` files." (10 patterns × N files = 10N calls)

**Right:** "Grep the codebase for `pattern1|pattern2|...|pattern10`. Filter results to exclude test paths." (1 call)

The agent can then Read specific files of interest from the grep results, but the discovery step is a single call.

### Batching for Subagent Work

When a workflow needs to process many items (files, functions, findings), batch them into fixed-size groups instead of spawning one subagent per item.

**Wrong:** "Spawn a subagent for each discovered file." (N files = N subagents)

**Right:** "Batch files into groups of 10-20. Spawn one subagent per batch." (N/15 subagents, capped)

Always specify the batch size explicitly. Without a number, the agent picks its own grouping (or doesn't batch at all).

### The 10,000-File Test

Before finalizing any workflow, ask: "What happens if this runs against a 10,000-file repo?"

- **Grep calls** should be O(1) or O(patterns), not O(files) or O(files × patterns)
- **Subagent count** should be O(1) or O(batches), not O(files) or O(functions)
- **Read calls** should target specific files from search results, not enumerate all files

---

## Reference: Workflow Patterns

# Workflow Patterns

Five patterns for structuring workflow-based skills. Choose based on your skill's decision structure, not its domain.

---

## 1. Routing Pattern

**When to use:** The skill handles multiple independent tasks that share common setup but diverge into separate paths.

**Key characteristics:**
- Intake form collects context upfront
- Router maps user intent to a specific workflow file
- Each workflow is self-contained and independent
- Adding a new capability means adding a new workflow file, not modifying existing ones

**Structural skeleton:**

```markdown
<intake>
Step 1: What data do you have?
- Option A -> Proceed
- Option B -> Extract first, then proceed
- No data -> Ask user to provide it

Step 2: What would you like to do?
1. Task One - brief description
2. Task Two - brief description
3. Task Three - brief description
</intake>

<routing>
| Response | Workflow |
|----------|----------|
| 1, "keyword", "phrase" | `workflows/task-one.md` |
| 2, "keyword", "phrase" | `workflows/task-two.md` |
| 3, "keyword", "phrase" | `workflows/task-three.md` |

**After reading the workflow, follow it exactly.**
</routing>
```

**Key design decisions:**
- Intake MUST validate prerequisites before routing (e.g., "do you have the required data?")
- Routing table uses both numeric options AND keyword synonyms for fuzzy matching
- Each workflow file stands alone — no cross-workflow dependencies
- The routing instruction "follow it exactly" prevents the LLM from improvising

**Common mistakes:**
- Routing based on vague keywords that overlap between workflows
- Forgetting to handle the "none of the above" case
- Putting workflow logic in SKILL.md instead of separate files
- Missing the "follow it exactly" instruction, causing the LLM to paraphrase instead of execute

---

## 2. Sequential Pipeline Pattern

**When to use:** The skill executes a series of dependent steps where each step's output feeds the next. Skipping steps produces bad results.

**Key characteristics:**
- Steps must execute in order
- Each step has entry criteria (what must be true) and exit criteria (what it produces)
- Auto-detection logic determines which step to start from
- Task tracking (TaskCreate/TaskUpdate) coordinates multi-step execution

**Structural skeleton:**

```markdown
## Quick Start

For the common case ("do the standard thing"):
1. Verify prerequisites are installed
2. Check for existing artifacts from prior runs

Then execute the full pipeline: step1 -> step2 -> step3

## Workflow Selection

| Workflow | Purpose |
|----------|---------|
| [step-one](workflows/step-one.md) | First phase description |
| [step-two](workflows/step-two.md) | Second phase description |
| [step-three](workflows/step-three.md) | Third phase description |

### Auto-Detection Logic

| Condition | Action |
|-----------|--------|
| No artifacts exist | Execute full pipeline (step1 -> step2 -> step3) |
| Step 1 complete | Execute step2 -> step3 |
| Steps 1-2 complete | Ask user: run step3 on existing, or restart? |
```

**Key design decisions:**
- Auto-detection prevents redundant work when partial results exist
- Each workflow file documents its own entry/exit criteria
- The decision prompt asks the user only when the correct action is ambiguous
- Pipeline dependencies are explicit — "step2 requires output from step1"

**Common mistakes:**
- No auto-detection, forcing users to always start from scratch
- Steps that silently fail without checking their own prerequisites
- Missing the "ask user" case when existing artifacts may be stale
- Workflow files that assume prior steps ran without checking

---

## 3. Linear Progression Pattern

**When to use:** A single start-to-finish process with no branching. Every execution follows the same numbered phases.

**Key characteristics:**
- One path, no routing decisions
- Phases are strictly numbered and sequential
- Each phase has clear completion criteria
- The user follows the entire flow every time

**Structural skeleton:**

```markdown
## Workflow

### Phase 1: Setup
**Entry:** User has provided [input]
**Actions:**
1. Validate input
2. Check prerequisites
**Exit:** [Specific artifact] exists and is valid

### Phase 2: Analysis
**Entry:** Phase 1 exit criteria met
**Actions:**
1. Perform analysis step A
2. Perform analysis step B
**Exit:** [Analysis result] is complete

### Phase 3: Output
**Entry:** Phase 2 exit criteria met
**Actions:**
1. Generate output
2. Validate output
**Exit:** [Final deliverable] ready for user
```

**Key design decisions:**
- Entry/exit criteria on every phase prevent skipping
- Actions within phases are numbered for unambiguous ordering
- No conditional branching — if you need branches, use Routing or Sequential Pipeline
- Verification at the end catches errors from any phase

**Common mistakes:**
- Phases without exit criteria ("do analysis" — how do you know it's done?)
- Mixing phases that should be separate (analysis + output in one phase)
- No verification step at the end
- Using this pattern when the skill actually needs routing (forcing a linear flow on branching logic)

---

## 4. Safety Gate Pattern

**When to use:** The skill performs destructive or irreversible actions. User confirmation is required before any such action.

**Key characteristics:**
- Analysis phase gathers all information before any action
- Explicit confirmation gates (usually two: review + execute)
- Exact commands shown to user before execution
- Individual action execution (so partial failures don't block remaining work)

**Structural skeleton:**

```markdown
## Core Principle: SAFETY FIRST

**Never [perform action] without explicit user confirmation.**

## Workflow

### Phase 1: Comprehensive Analysis
Gather ALL information upfront before any action.
[Data gathering commands]

### Phase 2: Categorize
[Decision tree for categorizing items]
| Category | Meaning | Action |
|----------|---------|--------|
| SAFE | Verified safe | Standard action |
| RISKY | Needs review | User decides |
| KEEP | Active/needed | No action |

### GATE 1: Present Complete Analysis
Present everything in ONE comprehensive view.
[Formatted summary with categories]
Use AskUserQuestion with clear options.
**Do not proceed until user responds.**

### GATE 2: Final Confirmation with Exact Commands
Show the EXACT commands that will run.
**Confirm? (yes/no)**

### Phase 3: Execute
Run each action as a **separate command**.
Report result of each. Continue on individual failure.

### Phase 4: Report
[Summary of what was done and what remains]
```

**Key design decisions:**
- Two gates, not one: first to review the plan, second to approve exact commands
- Analysis MUST complete before any gate — no incremental "analyze then ask"
- Individual execution means one failure doesn't block the rest
- Report phase shows both what changed and what was left untouched

**Common mistakes:**
- Only one confirmation gate (user approves without seeing exact commands)
- Interleaving analysis and confirmation (asking after each item instead of all at once)
- Batch execution where one failure aborts everything
- Missing the report phase, leaving the user unsure what happened

---

## 5. Task-Driven Pattern

**When to use:** Complex multi-step workflows where steps have dependencies, can partially fail, and need progress tracking.

**Key characteristics:**
- TaskCreate/TaskUpdate/TaskList for state management
- Explicit dependency declarations (blockedBy/blocks)
- Each task is independently completable
- Progress is visible and resumable

**Structural skeleton:**

```markdown
## Workflow

### Phase 1: Plan
Analyze inputs and create task list:

- TaskCreate: "Step A" (no dependencies)
- TaskCreate: "Step B" (blockedBy: Step A)
- TaskCreate: "Step C" (blockedBy: Step A)
- TaskCreate: "Step D" (blockedBy: Step B, Step C)

### Phase 2: Execute
For each unblocked task:
1. TaskUpdate: set to in_progress
2. Execute the task
3. TaskUpdate: set to completed
4. TaskList: check for newly unblocked tasks

### Phase 3: Report
TaskList to show final status.
Report completed vs failed tasks.
```

**Key design decisions:**
- Dependencies are declared upfront, not discovered during execution
- Tasks that don't depend on each other can execute in parallel
- Failed tasks block dependents but don't abort unrelated tasks
- TaskList provides natural progress reporting

**Common mistakes:**
- Creating tasks without dependency declarations, then executing in wrong order
- Not checking TaskList after completing a task (missing newly unblocked work)
- Marking tasks complete before verifying they actually succeeded
- Using task tracking for linear workflows where it adds overhead without value

---

## Cross-Pattern Guidance: Feedback Loops

Any pattern can incorporate a validation loop — not just a final check.

**When to use:** The workflow modifies state iteratively and intermediate results can be validated.

**Structure:**
```
Execute step → Validate → Pass? → Next step
                       → Fail? → Fix → Re-validate
```

**Examples:**
- TDD: write test → run → fail → write code → run → pass → refactor → run → pass
- PR iteration: push → CI checks → fix failures → push → re-check
- Form filling: map fields → validate mapping → fix errors → re-validate → fill

**Key design decisions:**
- Define a maximum loop count (e.g., "if 3+ attempts fail, stop and ask for help")
- Each loop iteration must make the validation command explicit ("Run: `python validate.py`")
- Distinguish between "fix and retry" loops (automated) and "escalate" exits (human intervention)

**Common mistakes:**
- Verification only at the end, not after each mutation
- No loop bound, causing infinite retry spirals
- Loop body that doesn't re-run the same validation command
