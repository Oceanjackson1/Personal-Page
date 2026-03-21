---
title: "Github"
description: "GitHub patterns using gh CLI for pull requests, stacked PRs, code review, branching strategies, and repository automation. Use when working with GitHub PRs, merging strategies, or repository management tasks."
category: "workflow"
source: "community"
author: "Community"
tags: ["github"]
date: 2026-03-20
---

# GitHub Patterns

## Tools

Use `gh` CLI for all GitHub operations. Prefer CLI over GitHub MCP servers for lower context usage.

## Quick Commands

```bash
# Create a PR from the current branch
gh pr create --title "feat: add feature" --body "Description"

# Squash-merge a PR
gh pr merge <PR_NUMBER> --squash --title "feat: add feature (#<PR_NUMBER>)"

# View PR status and checks
gh pr status
gh pr checks <PR_NUMBER>
```

## Stacked PR Workflow Summary

When merging a chain of stacked PRs (each targeting the previous branch):

1. **Merge the first PR** into main via squash merge
2. **For each subsequent PR**: rebase onto main, update base to main, then squash merge
3. **On conflicts**: stop and ask the user to resolve manually

```bash
# Rebase next PR's branch onto main, excluding already-merged commits
git rebase --onto origin/main <old-base-branch> <next-branch>
git push --force-with-lease origin <next-branch>
gh pr edit <N> --base main
gh pr merge <N> --squash --title "<PR title> (#N)"
```

See [stacked-pr-workflow.md][stacked-pr-workflow] for full step-by-step details.

## Quick Reference

| File | Description |
| --- | --- |
| [stacked-pr-workflow.md][stacked-pr-workflow] | Merge stacked PRs into main as individual squash commits |

## Problem -> Skill Mapping

| Problem | Start With |
| --- | --- |
| Merge stacked PRs cleanly | [stacked-pr-workflow.md][stacked-pr-workflow] |

[stacked-pr-workflow]: references/stacked-pr-workflow.md

---

## Reference: Stacked Pr Workflow

# Skill: Merge PR Chain

Merge a chain of stacked GitHub PRs into main as individual squash commits. Use when user has multiple PRs where each targets the previous one's branch (e.g., PR #2 → PR #1's branch → main) and wants to squash merge them all to main while preserving separate commits per PR.

## Workflow

### 1. Identify the chain

Fetch PR details to map the chain structure:
```
main
  └── #1 (base: main, branch: feat-a)
        └── #2 (base: feat-a, branch: feat-b)
              └── #3 (base: feat-b, branch: feat-c)
```

### 2. Merge and rebase sequentially

**First PR** (targets main):
```bash
# Squash merge via GitHub CLI
gh pr merge <N> --squash --title "<PR title> (#N)"
git pull origin main
```

**Subsequent PRs** — rebase onto main, update base, then merge:
```bash
# 1. Checkout the branch for the next PR
git checkout <next-branch>

# 2. Rebase onto main, excluding commits from the old base branch
#    This replays only this PR's commits onto main
git rebase --onto origin/main <old-base-branch> <next-branch>

# 3. Force push the rebased branch
git push --force-with-lease origin <next-branch>

# 4. Update the PR's base branch to main via GitHub CLI
gh pr edit <N> --base main

# 5. Squash merge the PR
gh pr merge <N> --squash --title "<PR title> (#N)"

# 6. Update local main
git fetch origin main
git checkout main
git pull origin main
```

Repeat step 2 for each subsequent PR in the chain.

## Key details

- **Always use PR title as commit title** — GitHub may default to branch name or first commit otherwise. Pass `--title` explicitly.
- **Use `--force-with-lease`** — Safer than `--force`, fails if remote has unexpected changes.
- **Update PR base before merging** — After rebasing, change the PR's base branch to `main` so it merges correctly and shows "merged into main" in GitHub UI.

## Handling conflicts

When `git rebase --onto` encounters conflicts:

1. Git will pause and show which files have conflicts
2. **Stop and ask the user** to resolve conflicts manually
3. After user resolves: `git add <resolved-files> && git rebase --continue`
4. If user wants to abort: `git rebase --abort`

**Never auto-resolve conflicts** — always ask the user to review and resolve manually.

## Why this works

`git rebase --onto <new-base> <old-base> <branch>` takes commits that are in `<branch>` but not in `<old-base>` and replays them onto `<new-base>`. This effectively strips the already-merged commits and moves only the PR's unique changes onto main.

## Benefits over cherry-pick

- PRs show as "merged into main" in GitHub UI
- Clean linear history on main
- No duplicate commits or confusing merge states
- Each PR's diff remains reviewable until merged
