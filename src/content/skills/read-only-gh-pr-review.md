---
title: "Read Only Gh Pr Review"
description: "Review backend pull requests for correctness, security, performance, maintainability, and test coverage using GitHub CLI plus local repository inspection. Use when asked to review service-layer/API/database changes, audit backend branch diffs, sum..."
category: "research"
source: "community"
author: "Community"
tags: ["read", "only", "gh", "pr", "review"]
date: 2026-03-20
---

# PR Review (Backend, GitHub CLI)

## Overview

Review backend pull requests end-to-end using local code analysis and GitHub CLI API calls. Report only actionable, high-signal findings.

## Tool Constraints

- Use only: `SemanticSearch`, `WebSearch`, `Grep`, `LS`, `Glob`, `Read`, `Shell`, `GitHub CLI`.
- **Before any `gh` command**, source the read-only environment script to enable security enforcement:
  ```bash
  source "<SKILL_DIR>/scripts/activate-gh-readonly.sh"
  ```
  Replace `<SKILL_DIR>` with the absolute path to this skill directory.
- After sourcing, use `gh` commands directly—they are intercepted by the read-only wrapper.
- Verify CLI auth first with `gh auth status`. If not authenticated, ask the user to run `gh auth login`.
- Enforce strict read-only mode at all times.
- Never attempt any write operation, including comments, reviews, edits, assignments, merges, closes, reopens, or API mutations.
- If a requested command is blocked by the wrapper, do not try alternatives that can mutate state.
- The read-only wrapper blocks `command gh` and other bypass attempts.

## Workflow

1. Enable read-only environment.
   - Source the environment script: `source "<SKILL_DIR>/scripts/activate-gh-readonly.sh"`
   - All subsequent `gh` commands in this shell session are now protected.
2. Prepare review context.
   - Confirm identity and auth: `gh auth status`, `gh api user`.
   - Resolve repository owner/name from the current repo or pass `-R <OWNER>/<REPO>`.
3. Resolve the target PR.
   - Use `gh pr view <PR_NUMBER> [--json <fields>]` when PR number is known.
   - Otherwise shortlist with `gh pr list [flags]` and pick the target PR.
4. Sync local repository to the latest PR branch code.
   - Fetch the latest remote state for the PR head branch before reviewing code.
   - Example flow:
     - Get head branch name from PR metadata (`headRefName`).
     - Run `git fetch --prune origin <HEAD_BRANCH>`.
     - Review files from `FETCH_HEAD` or check out a local review branch from it.
5. Gather full PR evidence before judging.
   - Metadata: `gh pr view <PR_NUMBER> [--json <fields>]`
   - Diff: `gh pr diff <PR_NUMBER> [--patch|--name-only]`
   - Changed files: `gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/files --paginate`
   - Reviews: `gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/reviews --paginate`
   - Checks: `gh pr checks <PR_NUMBER> [--json <fields>]`
   - Comments:
     - `gh pr view <PR_NUMBER> --comments`
     - `gh api repos/<OWNER>/<REPO>/issues/<PR_NUMBER>/comments --paginate`
     - `gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments --paginate`
6. Inspect changed backend code deeply.
   - Read all high-risk touched files locally (`Read`, `Grep`) and correlate with diff hunks.
   - Prioritize request handlers/controllers, business services, authorization logic, database queries, migrations, background jobs, and queue/event handlers.
   - Verify idempotency, transaction safety, concurrency behavior, retry behavior, and backward compatibility for public API contracts.
   - Use `gh api repos/<OWNER>/<REPO>/contents/<PATH>?ref=<REF>` when exact remote content is needed (content is usually base64 in `.content`).
7. Apply review checklist with risk-first ordering.
   - Use `references/review-checklist.md`.
   - Cover security, correctness, data integrity, API compatibility, performance, and test sufficiency before style concerns.
8. Produce actionable review output.
   - Report only issues that are likely defects, regressions, or maintainability risks.
   - Include exact `file:line`, impact, and concrete fix guidance.
   - End with residual risk and missing validation/testing assumptions.
   - Return findings in chat only; do not write any comment or review back to GitHub.

## Response Format

Use this section order:

1. `Critical Issues (Must Fix)`
2. `Important Issues (Should Fix)`
3. `Suggestions (Consider)`
4. `Good Practices Noted`

For each issue, use:

```text
Issue: <brief description>
Location: <file:line>
Severity: <Critical|High|Medium|Low>
Problematic Code: <snippet or precise behavior>
Suggestion: <specific fix>
Example: <optional patch-style snippet>
```

## GitHub CLI API Equivalents

Use command mappings in `references/github-cli-map.md`.

## Review Tone

- Be constructive and specific.
- Explain impact and rationale.
- Assume positive intent.
- Prefer concise, high-confidence feedback.

---

## Reference: Github Cli Map

# GitHub CLI Mapping

Use these mappings for PR review workflows with GitHub CLI.

## Read-Only Policy

- Treat this workflow as read-only.
- Use only read/list/view/search/diff/check operations.
- Enable the read-only shell environment first: `source "<SKILL_DIR>/scripts/activate-gh-readonly.sh"`.
- After sourcing, call `gh` normally; it is intercepted by the read-only wrapper.
- Do not run mutating operations (`edit`, `comment`, `review`, `merge`, or `gh api` with `POST/PATCH/PUT/DELETE`).

## Prerequisites

- Confirm auth: `gh auth status`
- Resolve repository context:
  - Preferred: run inside the repository root.
  - Alternative: add `-R <owner>/<repo>` to commands.

## Backend Review Operation Mapping

| Allowed operation | GitHub CLI equivalent |
| --- | --- |
| `search_code` | `gh search code "<query>"` |
| `get_commit` | `gh api repos/<OWNER>/<REPO>/commits/<SHA>` |
| `get_file_contents` | `gh api repos/<OWNER>/<REPO>/contents/<PATH>?ref=<REF>` (content is usually base64 in `.content`) |
| `get_issue` | `gh issue view <ISSUE_NUMBER> [--comments] [--json <fields>]` |
| `get_me` | `gh api user` |
| `get_pull_request` | `gh pr view <PR_NUMBER> [--json <fields>]` |
| `get_pull_request_comments` | PR conversation comments: `gh pr view <PR_NUMBER> --comments`; issue comments API: `gh api repos/<OWNER>/<REPO>/issues/<PR_NUMBER>/comments --paginate`; inline review comments: `gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/comments --paginate` |
| `get_pull_request_diff` | `gh pr diff <PR_NUMBER> [--patch|--name-only]` |
| `get_pull_request_files` | `gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/files --paginate` |
| `get_pull_request_reviews` | `gh api repos/<OWNER>/<REPO>/pulls/<PR_NUMBER>/reviews --paginate` |
| `get_pull_request_status` | `gh pr checks <PR_NUMBER> [--json <fields>]` |
| `list_commits` | `gh api repos/<OWNER>/<REPO>/commits --paginate` |
| `list_pull_requests` | `gh pr list [flags]` |
| `search_issues` | `gh search issues "<query>"` |

## Notes

- Prefer `gh pr view --json ...` and `gh pr checks --json ...` when structured output is needed.
- Prefer `gh api` when no first-class subcommand exists.
- Use `--paginate` for list endpoints when full history matters.
- Keep requests scoped to required fields to reduce noise.
- If asked to post review comments or change PR state, refuse and keep the process read-only.

---

## Reference: Review Checklist

# PR Review Checklist

Use only relevant sections for the current pull request. Prefer depth over breadth.

## 1. Backend Code Quality and Structure

- Confirm naming follows project conventions.
- Confirm style and formatting align with repository standards.
- Flag duplicated logic that should be consolidated.
- Check separation of concerns across handlers/controllers, services, repositories, and domain logic.
- Flag complex functions or deeply nested branching that are hard to reason about or test.
- Flag unexplained magic numbers and hidden constants.
- Verify comments explain non-obvious logic and remove noise comments.

## 2. Security, Authentication, and Authorization

- Validate and sanitize all untrusted input.
- Verify SQL/database calls are parameterized.
- Verify authentication checks on protected backend operations.
- Verify authorization and role checks are complete on every sensitive code path.
- Flag hardcoded secrets, tokens, or credentials.
- Verify secure transport assumptions for sensitive backend operations.
- Flag dependency or package-level vulnerability concerns when visible.

## 3. Error Handling, Logging, and Observability

- Ensure expected failures are handled and surfaced safely.
- Ensure errors do not leak sensitive internals.
- Verify log level choices are appropriate.
- Verify cleanup paths for files, transactions, locks, and connections.
- Verify important operational signals are observable (metrics, traces, or structured logs where applicable).

## 4. Data Access and Migrations

- Check for N+1 queries and avoidable repeated database access.
- Validate indexes, query shape, and pagination for large datasets.
- Ensure schema changes include migrations.
- Ensure rollback or safe recovery path exists.
- Validate constraints and data integrity rules.
- Estimate migration impact on large datasets and runtime risk.

## 5. Performance and Scalability

- Check heavy computations and synchronous blocking work in request paths.
- Evaluate algorithmic complexity in hot paths.
- Verify async/concurrency usage avoids unnecessary blocking and race conditions.
- Check retry/backoff behavior for external dependencies.
- Identify useful caching opportunities when repeated reads dominate.

## 6. API Contracts and Backward Compatibility

- Validate API changes against existing contracts.
- Check backward compatibility and versioning impact.
- Ensure request/response and error formats stay consistent.
- Verify API behavior/documentation updates where needed.
- Consider rate limiting and abuse controls for exposed endpoints.

## 7. Testing Strategy

- Ensure new behavior has tests.
- Ensure tests cover boundary, failure, and concurrency cases.
- Ensure tests assert external behavior (not only implementation details).
- Ensure critical integration paths are exercised when changed.
- Verify mocks isolate external dependencies correctly.

## 8. Business Rules and Invariants

- Verify behavior matches requirements and acceptance criteria.
- Validate business-rule enforcement and edge cases.
- Verify auditability for high-risk backend operations.
- Flag flows that can violate invariants under concurrency.
