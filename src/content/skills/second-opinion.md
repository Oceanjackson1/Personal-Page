---
title: "Second Opinion"
description: "Runs external LLM code reviews (OpenAI Codex or Google Gemini CLI) on uncommitted changes, branch diffs, or specific commits. Use when the user asks for a second opinion, external review, codex review, gemini review, or mentions /second-opinion."
category: "research"
source: "community"
author: "Community"
tags: ["second", "opinion"]
date: 2026-03-20
---

# Second Opinion

Shell out to external LLM CLIs for an independent code review powered by
a separate model. Supports OpenAI Codex CLI and Google Gemini CLI.

## When to Use

- Getting a second opinion on code changes from a different model
- Reviewing branch diffs before opening a PR
- Checking uncommitted work for issues before committing
- Running a focused review (security, performance, error handling)
- Comparing review output from multiple models

## When NOT to Use

- Neither Codex CLI nor Gemini CLI is installed
- No API key or subscription configured for either tool
- Reviewing non-code files (documentation, config)
- You want Claude's own review (just ask Claude directly)

## Safety Note

Gemini CLI is invoked with `--yolo`, which auto-approves all
tool calls without confirmation. This is required for headless
(non-interactive) operation but means Gemini will execute any
tool actions its extensions request without prompting.

## Quick Reference

```
# Codex (headless exec with structured JSON output)
codex exec --sandbox read-only --ephemeral \
  --output-schema codex-review-schema.json \
  -o "$output_file" - < "$prompt_file"

# Gemini (code review extension)
gemini -p "/code-review" --yolo -e code-review
# Gemini (headless with diff — see references/ for full pattern)
git diff HEAD > /tmp/review-diff.txt
{ printf '%s\n\n' 'Review this diff for issues.'; cat /tmp/review-diff.txt; } \
  | gemini -p - --yolo -m gemini-3.1-pro-preview
```

## Invocation

### 1. Gather context interactively

Use `AskUserQuestion` to collect review parameters in one shot.
Adapt the questions based on what the user already provided
in their invocation (skip questions they already answered).

Combine all applicable questions into a single `AskUserQuestion`
call (max 4 questions).

**Question 1 — Tool** (skip if user already specified):

```
header: "Review tool"
question: "Which tool should run the review?"
options:
  - "Both Codex and Gemini (Recommended)" → run both in parallel
  - "Codex only"                          → codex exec
  - "Gemini only"                         → gemini CLI
```

**Question 2 — Scope** (skip if user already specified):

```
header: "Review scope"
question: "What should be reviewed?"
options:
  - "Uncommitted changes" → git diff HEAD + untracked files
  - "Branch diff vs main" → git diff <branch>...HEAD (auto-detect default branch)
  - "Specific commit"     → git diff <sha>~1..<sha> (follow up for SHA)
```

**Question 3 — Project context** (skip if neither CLAUDE.md nor AGENTS.md exists):

Check for CLAUDE.md first, then AGENTS.md in the repo root.
Only show this question if at least one exists.

```
header: "Project context"
question: "Include project conventions file so the review
  checks against your standards?"
options:
  - "Yes, include it"
  - "No, standard review"
```

**Question 4 — Review focus** (always ask):

```
header: "Review focus"
question: "Any specific focus areas for the review?"
options:
  - "General review"    → no custom prompt
  - "Security & auth"   → security-focused prompt
  - "Performance"       → performance-focused prompt
  - "Error handling"    → error handling-focused prompt
```

### 2. Run the tool directly

Do not pre-check tool availability. Run the selected tool
immediately. If the command fails with "command not found" or
an extension is missing, report the install command from the
Error Handling table below and skip that tool (if "Both" was
selected, run only the available one).

## Diff Preview

After collecting answers, show the diff stats:

```bash
# For uncommitted (tracked + untracked):
git diff --stat HEAD
git ls-files --others --exclude-standard

# For branch diff:
git diff --stat <branch>...HEAD

# For specific commit:
git diff --stat <sha>~1..<sha>
```

If the diff is empty, stop and tell the user.

If the diff is very large (>2000 lines changed), warn the user
and ask whether to proceed or narrow the scope.

## Skipping Inapplicable Checks

After determining the diff scope, skip checks that don't apply
to the files actually changed.

### Dependency Scanning

Only run `/security:scan-deps` when the diff touches dependency
manifest files. Check with:

```bash
git diff --name-only <scope> \
  | grep -qiE '(package\.json|package-lock|yarn\.lock|pnpm-lock|Gemfile|\.gemspec|requirements\.txt|setup\.py|setup\.cfg|pyproject\.toml|poetry\.lock|uv\.lock|Cargo\.toml|Cargo\.lock|go\.mod|go\.sum|composer\.json|composer\.lock|Pipfile)'
```

If no dependency files are in the diff, skip the scan even when
security focus is selected. The scan analyzes the entire project's
dependency tree regardless of diff scope, so it adds significant
time for zero value when dependencies weren't touched.

## Auto-detect Default Branch

For branch diff scope, detect the default branch name:

```bash
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null \
  | sed 's@^refs/remotes/origin/@@' || echo main
```

## Codex Invocation

See [references/codex-invocation.md](references/codex-invocation.md)
for full details on command syntax, prompt assembly, and the
structured output schema.

Summary:
- Uses `codex exec` (not `codex review`) for headless operation
- Model: `gpt-5.3-codex`, reasoning: `xhigh`
- Uses OpenAI's published code review prompt (fine-tuned into the model)
- Diff is generated manually and piped via stdin with the prompt
- `--output-schema` produces structured JSON findings
- `-o` captures only the final message (no thinking/exec noise)
- All three scopes (uncommitted, branch, commit) support project
  context and focus instructions (no limitations)
- Falls back to `gpt-5.2-codex` on auth errors
- Output is clean JSON — parse and present findings by priority
- Set `timeout: 600000` on the Bash call

## Gemini Invocation

See [references/gemini-invocation.md](references/gemini-invocation.md)
for full details on flags, scope mapping, and extension usage.

Summary:
- Model: `gemini-3.1-pro-preview`, flags: `--yolo`, `-e`, `-m`
- For uncommitted general review: `gemini -p "/code-review" --yolo -e code-review`
- For branch/commit diffs: pipe `git diff` into `gemini -p`
- Security extension name is `gemini-cli-security` (not `security`)
- `/security:analyze` is interactive-only — use `-p` with a
  security prompt instead
- Run `/security:scan-deps` only when security focus is selected
  AND the diff touches dependency manifest files (see Diff-Aware
  Optimizations)
- Set `timeout: 600000` on the Bash call

**Scope mapping for `git diff`** (Gemini has no built-in scope flags):

| Scope | Diff command |
|-------|-------------|
| Uncommitted | `git diff HEAD` + untracked (see codex-invocation.md) |
| Branch diff | `git diff <branch>...HEAD` |
| Specific commit | `git diff <sha>~1..<sha>` |

## Running Both

When the user picks "Both" (the default):

1. Run Codex and Gemini in parallel — issue both Bash tool
   calls in a single response. Both commands are read-only
   (they review diffs via external APIs) so there is no
   shared state or git lock contention.
2. Collect both results, then present with clear headers:

```
## Codex Review (gpt-5.3-codex)
<codex output>

## Gemini Review (gemini-3.1-pro-preview)
<gemini output>
```

Summarize where the two reviews agree and differ.

## Error Handling

| Error | Action |
|-------|--------|
| `codex: command not found` | Tell user: `npm i -g @openai/codex` |
| `gemini: command not found` | Tell user: `npm i -g @google/gemini-cli` |
| Gemini `code-review` extension missing | Tell user: `gemini extensions install https://github.com/gemini-cli-extensions/code-review` |
| Gemini `gemini-cli-security` extension missing | Tell user: `gemini extensions install https://github.com/gemini-cli-extensions/security` |
| Model auth error (Codex) | Retry with `gpt-5.2-codex` |
| Empty diff | Tell user there are no changes to review |
| Timeout | Inform user and suggest narrowing the diff scope |
| Tool partially unavailable | Run only the available tool, note the skip |

## Examples

**Both tools (default):**
```
User: /second-opinion
Claude: [asks 4 questions: tool, scope, context, focus]
User: picks "Both", "Branch diff", "Yes include CLAUDE.md", "Security"
Claude: [detects default branch = main]
Claude: [shows diff --stat: 6 files, +103 -15]
Claude: [assembles prompt with review instructions + CLAUDE.md + security focus + diff]
Claude: [runs codex exec and gemini in parallel]
Claude: [reads codex output file, parses structured findings]
Claude: [presents both reviews, highlights agreements/differences]
```

**Codex only with inline args:**
```
User: /second-opinion check uncommitted changes for bugs
Claude: [scope known: uncommitted, focus known: custom]
Claude: [asks 2 questions: tool, project context]
User: picks "Codex only", "No context"
Claude: [shows diff --stat: 3 files, +45 -10]
Claude: [writes prompt file with review instructions + diff]
Claude: [runs codex exec, reads structured JSON output]
Claude: [presents findings by priority with file:line refs]
```

**Gemini only:**
```
User: /second-opinion
Claude: [asks 4 questions]
User: picks "Gemini only", "Uncommitted", "No", "General"
Claude: [shows diff --stat: 2 files, +20 -5]
Claude: [runs gemini -p "/code-review" --yolo -e code-review]
Claude: [presents review]
```

**Large diff warning:**
```
User: /second-opinion
Claude: [asks questions] → user picks "Both", "Uncommitted", "General"
Claude: [shows diff --stat: 45 files, +3200 -890]
Claude: "Large diff (3200+ lines). Proceed, or narrow the scope?"
User: "proceed"
Claude: [runs both reviews]
```

---

## Reference: Codex Invocation

# Codex CLI Invocation

## Default Configuration

- Model: `gpt-5.3-codex`
- Reasoning effort: `xhigh`

## Approach

Use `codex exec` in headless mode with the published code review
prompt, structured JSON output, and `-o` (`--output-last-message`)
to capture only the final review. This avoids the verbose
`[thinking]` and `[exec]` blocks that `codex review` dumps to
stdout.

## Review Prompt

Use this prompt verbatim — it is from OpenAI's [Build Code Review
with the Codex SDK](https://developers.openai.com/cookbook/examples/codex/build_code_review_with_codex_sdk)
cookbook, and GPT-5.2-codex and later received specific training
on it:

```
You are acting as a reviewer for a proposed code change made by another engineer.
Focus on issues that impact correctness, performance, security, maintainability, or developer experience.
Flag only actionable issues introduced by the pull request.
When you flag an issue, provide a short, direct explanation and cite the affected file and line range.
Prioritize severe issues and avoid nit-level comments unless they block understanding of the diff.
After listing findings, produce an overall correctness verdict ("patch is correct" or "patch is incorrect") with a concise justification and a confidence score between 0 and 1.
Ensure that file citations and line numbers are exactly correct using the tools available; if they are incorrect your comments will be rejected.
```

## Prompt Assembly

Create temp files for the prompt and output:

```bash
prompt_file="$(mktemp)"
output_file="$(mktemp)"
stderr_log="$(mktemp)"
```

Write the prompt file with these sections in order:

```
<review prompt from above>

<If project context was requested>
Project conventions and standards:
---
<full contents of CLAUDE.md or AGENTS.md>
---

<If focus area was selected or custom text provided>
Focus: <focus area instructions>

Diff to review:
---
<git diff output for the selected scope>
---
```

### Generating the diff

| Scope | Command |
|-------|---------|
| Uncommitted (tracked) | `git diff HEAD` |
| Uncommitted (untracked) | `git ls-files --others --exclude-standard` — for each file, append `git diff --no-index /dev/null <file>` |
| Branch diff | `git diff <branch>...HEAD` |
| Specific commit | `git diff <sha>~1..<sha>` |

**Uncommitted scope must include untracked files.** `git diff HEAD`
alone only shows changes to tracked files. New files that haven't
been staged would be silently excluded. Generate the full diff:

```bash
{
  git diff HEAD
  git ls-files --others --exclude-standard | while IFS= read -r f; do
    git diff --no-index /dev/null "$f" 2>/dev/null || true
  done
}
```

## Base Command

```bash
codex exec \
  -c model='"gpt-5.3-codex"' \
  -c model_reasoning_effort='"xhigh"' \
  --sandbox read-only \
  --ephemeral \
  --output-schema {baseDir}/references/codex-review-schema.json \
  -o "$output_file" \
  - < "$prompt_file" \
  > /dev/null 2>"$stderr_log"
```

Then read `$output_file` with the Read tool. If empty or missing,
read `$stderr_log` to diagnose the failure.

## Output Format

The output is structured JSON matching `codex-review-schema.json`:

```json
{
  "findings": [
    {
      "title": "Short description (max 80 chars)",
      "body": "Detailed explanation",
      "confidence_score": 0.95,
      "priority": 1,
      "code_location": {
        "file_path": "src/main.rs",
        "line_range": { "start": 42, "end": 48 }
      }
    }
  ],
  "overall_correctness": "patch is correct",
  "overall_explanation": "Summary of the review",
  "overall_confidence_score": 0.9
}
```

Priority levels: 0 = informational, 1 = low, 2 = medium, 3 = high.

### Presenting Results

Parse the JSON and present findings grouped by priority (highest
first). For each finding, show:

- **Title** with file:line reference
- **Body** explanation
- **Confidence** as a percentage

End with the overall verdict and confidence.

If the output file is empty or missing, read `$stderr_log` to
diagnose the failure.

## Model Fallback

If `gpt-5.3-codex` fails with an auth error (e.g., "not supported
when using Codex with a ChatGPT account"), retry with
`gpt-5.2-codex`. Log the fallback for the user.

## Error Handling

| Error | Action |
|-------|--------|
| `codex: command not found` | Tell user: `npm i -g @openai/codex` |
| Model auth error | Retry with `gpt-5.2-codex` |
| Timeout | Suggest narrowing the diff scope |
| `EPERM` / sandbox errors | Expected — `codex exec` runs sandboxed. Ignore these. |
| Empty/missing output file | Read `$stderr_log` to diagnose the failure |

---

## Reference: Gemini Invocation

# Gemini CLI Invocation

## Default Configuration

- Model: `gemini-3.1-pro-preview`
- Extensions: `code-review`, `gemini-cli-security`

## Key Flags

| Flag | Purpose |
|------|---------|
| `-p <prompt>` | Non-interactive (headless) mode |
| `--yolo` / `-y` | Auto-approve all tool calls |
| `-m <model>` | Model selection |
| `-e <ext>` | Load specific extension(s) |

## Scope-to-Diff Mapping

Gemini does not have built-in scope flags like Codex. Map the
user's scope choice to the correct `git diff` command:

| Scope | Diff command |
|-------|-------------|
| Uncommitted | `git diff HEAD` (captures both staged and unstaged) |
| Branch diff | `git diff <branch>...HEAD` |
| Specific commit | `git diff <sha>~1..<sha>` |

**Important:** For uncommitted scope, use `git diff HEAD` not
bare `git diff`. Bare `git diff` misses staged changes.

## Code Review (General, Performance, Error Handling)

For uncommitted changes, the `/code-review` extension
automatically picks up the working tree diff:

```bash
gemini -p "/code-review" \
  --yolo \
  -e code-review \
  -m gemini-3.1-pro-preview
```

For branch diffs or specific commits, pipe the diff with a
prompt header (avoids heredocs — diffs contain `$` and backticks
that break shell expansion):

```bash
git diff <branch>...HEAD > /tmp/review-diff.txt
{ printf '%s\n\n' 'Review this diff for code quality issues. <focus prompt>'; \
  cat /tmp/review-diff.txt; } \
  | gemini -p - -m gemini-3.1-pro-preview --yolo
```

## Security Review

The `/security:analyze` extension is interactive-only, so use
headless mode with a security-focused prompt instead:

```bash
git diff HEAD > /tmp/review-diff.txt
{ printf '%s\n\n' 'Analyze this diff for security vulnerabilities, including injection, auth bypass, data exposure, and input validation issues. Report each finding with severity, location, and remediation.'; \
  cat /tmp/review-diff.txt; } \
  | gemini -p - -e gemini-cli-security -m gemini-3.1-pro-preview --yolo
```

When security focus is selected, only run the supply chain scan
if the diff touches dependency manifest files:

```bash
# Check whether dependency files changed before scanning
git diff --name-only <scope> \
  | grep -qiE '(package\.json|package-lock|yarn\.lock|pnpm-lock|Gemfile|\.gemspec|requirements\.txt|setup\.py|setup\.cfg|pyproject\.toml|poetry\.lock|uv\.lock|Cargo\.toml|Cargo\.lock|go\.mod|go\.sum|composer\.json|composer\.lock|Pipfile)' \
  && gemini -p "/security:scan-deps" \
       --yolo \
       -e gemini-cli-security \
       -m gemini-3.1-pro-preview
```

Skip the scan when only non-dependency files changed. The scan
analyzes the entire project's dependency tree regardless of diff
scope, so it adds significant time for no value when dependencies
weren't touched.

## Adding Project Context

If project context was requested, prepend it to the prompt:

```bash
git diff HEAD > /tmp/review-diff.txt
{ printf 'Project conventions:\n---\n'; \
  cat CLAUDE.md; \
  printf '\n---\n\n%s\n\n' '<review instructions and focus>'; \
  cat /tmp/review-diff.txt; } \
  | gemini -p - -m gemini-3.1-pro-preview --yolo
```

## Error Handling

| Error | Action |
|-------|--------|
| `gemini: command not found` | Tell user: `npm i -g @google/gemini-cli` |
| Extension missing | Tell user: `gemini extensions install <github-url>` |
| `-e security` silently ignored | Use `-e gemini-cli-security` (the actual installed name) |
| Timeout | Inform user, suggest scoping down the diff |

## Extension Install Commands

```bash
gemini extensions install https://github.com/gemini-cli-extensions/code-review
gemini extensions install https://github.com/gemini-cli-extensions/security
```

Note: The security extension installs as `gemini-cli-security`
(not `security`). Always use `-e gemini-cli-security` when
loading it.
