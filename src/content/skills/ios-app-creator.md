---
title: "Ios App Creator"
description: "Orchestrate iOS/macOS app scaffolding and optional skill adoption for existing projects. Use when users want a guided wizard that can scaffold with XcodeGen and optionally install xcode-makefiles and simple-tasks."
category: "development"
source: "community"
author: "Community"
tags: ["ios", "app", "creator"]
date: 2026-03-20
---

# App Creator

## Overview

Paul Solt
Paul@SuperEasyApps.com
Version: 0.9.8

`app-creator` is now an orchestrator skill.

Responsibilities:
1. Scaffold new projects with XcodeGen templates.
2. Adopt existing projects non-destructively.
3. Optionally install subskills:
   - `xcode-makefiles`
   - `simple-tasks`

## Workflow

1. Collect inputs.
2. Run doctor checks.
3. Choose mode: `new` or `adopt`.
4. In `new` mode, scaffold app templates and run XcodeGen.
5. Install selected subskills (default: both).
6. Optionally initialize git and create a baseline commit.
7. Print exact next commands.

## Modes

### New Project

Run:

```bash
skills/app-creator/scripts/init.sh --project-mode new
```

Required fields in new mode:
- App name
- Bundle id
- Platform (`ios` or `macos`)
- UI framework (`swiftui`, `uikit`, `appkit`)
- Output directory

### Adopt Existing Project

Run:

```bash
skills/app-creator/scripts/init.sh --project-mode adopt
```

Behavior:
- No scaffolding/regeneration.
- Only installs selected subskills into the existing project.

## Subskill install defaults

Wizard defaults to installing both:
- `xcode-makefiles`
- `simple-tasks`

You can opt out with:
- `--skip-xcode-makefiles`
- `--skip-simple-tasks`

## Dry run

Use `--dry-run` to preview actions without mutating files.

## Git onboarding

`init.sh`/`scaffold_app.sh` support:
- `--git-init auto|never`
- `--git-commit prompt|always|never`

Defaults:
- `--git-init auto`
- `--git-commit prompt`

Safety behavior:
- If the target repo is already dirty before app-creator runs, auto-commit is skipped.
- If there are no staged/unstaged changes after install/scaffold, no commit is created.

## Resources

Use these files when you need details beyond the workflow:
- `references/workflow.md`
- `references/placeholders.md`

---

## Reference: Placeholders

# Template placeholders

These placeholders are replaced by `scripts/render_template.py` during scaffolding.

- __APP_NAME__
  - App and scheme name.
- __BUNDLE_ID__
  - Full bundle identifier (e.g., com.example.MyApp).
- __DEPLOYMENT_TARGET__
  - Deployment target (iOS 18.0 or macOS 15.4 by default).
- __PLATFORM__
  - ios or macos.
- __SIM_NAME__
  - iOS Simulator name (defaults to "auto" to pick the newest available iPhone).
- __SCRIPTS_DIR__
  - Toolkit scripts directory (defaults to `./scripts` or `./scripts/<namespace>`).
- __TARGET_PREFIX__
  - Optional Makefile target prefix when the toolkit is namespaced (e.g., `demo-`).
- __APP_GENERATOR__
  - Generator used for project generation: `xcodegen`.

---

## Reference: Workflow

# App Creator workflow

1. Run doctor to verify Xcode, XcodeGen, and CLI tools.
2. Choose mode:
   - `new`: scaffold app + install selected subskills
   - `adopt`: install selected subskills into existing project
3. Default selected subskills:
   - `xcode-makefiles`
   - `simple-tasks`
4. Apply git onboarding policy:
   - `--git-init auto|never`
   - `--git-commit prompt|always|never`
5. Print next commands (`make diagnose/build/test`, `scripts/task.sh summary --last-24h`).

Defaults
- Project mode: `new`
- Platform: `ios`
- UI: `swiftui`
- iOS deployment target: `18.0`
- macOS deployment target: `15.4`
- iOS simulator: `auto`
- Subskill installs: both enabled
- Git init: `auto`
- Baseline commit: `prompt`

Required dependency
- XcodeGen is required by default for new scaffolding: `brew install xcodegen`

Optional onboarding
- Run `skills/app-creator/scripts/init.sh` for interactive prompts.
- Use `--no-prompt` with explicit flags for non-interactive flows.

Adopt mode constraints
- Existing-project mode is non-destructive and does not regenerate app sources.
- In adopt mode, provide `--platform` when installing `xcode-makefiles`.

Tooling behavior
- App creator delegates build and task tooling to subskills.
- This skill no longer owns makefile/task implementation details directly.
- Auto-commit is skipped for pre-existing dirty repos to avoid sweeping unrelated edits.
