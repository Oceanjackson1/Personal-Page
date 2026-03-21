---
title: "Upgrading React Native"
description: "Upgrades React Native apps to newer versions by applying rn-diff-purge template diffs, updating package.json dependencies, migrating native iOS and Android configuration, resolving CocoaPods and Gradle changes, and handling breaking API updates. U..."
category: "development"
source: "community"
author: "Community"
tags: ["upgrading", "react", "native"]
date: 2026-03-20
---

# Upgrading React Native

## Overview

Covers the full React Native upgrade workflow: template diffs via Upgrade Helper, dependency updates, Expo SDK steps, and common pitfalls.

## Typical Upgrade Sequence

1. **Route**: Choose the right upgrade path via [upgrading-react-native.md][upgrading-react-native]
2. **Diff**: Fetch the canonical template diff using Upgrade Helper via [upgrade-helper-core.md][upgrade-helper-core]
3. **Dependencies**: Assess and update third-party packages via [upgrading-dependencies.md][upgrading-dependencies]
4. **React**: Align React version if upgraded via [react.md][react]
5. **Expo** (if applicable): Apply Expo SDK layer via [expo-sdk-upgrade.md][expo-sdk-upgrade]
6. **Verify**: Run post-upgrade checks via [upgrade-verification.md][upgrade-verification]

```bash
# Quick start: detect current version and fetch diff
npm pkg get dependencies.react-native --prefix "$APP_DIR"
npm view react-native dist-tags.latest

# Example: upgrading from 0.76.9 to 0.78.2
# 1. Fetch the template diff
curl -L -f -o /tmp/rn-diff.diff \
  "https://raw.githubusercontent.com/react-native-community/rn-diff-purge/diffs/diffs/0.76.9..0.78.2.diff" \
  && echo "Diff downloaded OK" || echo "ERROR: diff not found, check versions"
# 2. Review changed files
grep -n "^diff --git" /tmp/rn-diff.diff
# 3. Update package.json, apply native changes, then install + rebuild
npm install --prefix "$APP_DIR"
cd "$APP_DIR/ios" && pod install
# 4. Validate: both platforms must build successfully
npx react-native build-android --mode debug --no-packager
xcodebuild -workspace "$APP_DIR/ios/App.xcworkspace" -scheme App -sdk iphonesimulator build
```

## When to Apply

Reference these guidelines when:
- Moving a React Native app to a newer version
- Reconciling native config changes from Upgrade Helper
- Validating release notes for breaking changes

## Quick Reference

| File | Description |
|------|-------------|
| [upgrading-react-native.md][upgrading-react-native] | Router: choose the right upgrade path |
| [upgrade-helper-core.md][upgrade-helper-core] | Core Upgrade Helper workflow and reliability gates |
| [upgrading-dependencies.md][upgrading-dependencies] | Dependency compatibility checks and migration planning |
| [react.md][react] | React and React 19 upgrade alignment rules |
| [expo-sdk-upgrade.md][expo-sdk-upgrade] | Expo SDK-specific upgrade layer (conditional) |
| [upgrade-verification.md][upgrade-verification] | Manual post-upgrade verification checklist |
| [monorepo-singlerepo-targeting.md][monorepo-singlerepo-targeting] | Monorepo and single-repo app targeting and command scoping |

## Problem → Skill Mapping

| Problem | Start With |
|---------|------------|
| Need to upgrade React Native | [upgrade-helper-core.md][upgrade-helper-core] |
| Need dependency risk triage and migration options | [upgrading-dependencies.md][upgrading-dependencies] |
| Need React/React 19 package alignment | [react.md][react] |
| Need workflow routing first | [upgrading-react-native.md][upgrading-react-native] |
| Need Expo SDK-specific steps | [expo-sdk-upgrade.md][expo-sdk-upgrade] |
| Need manual regression validation | [upgrade-verification.md][upgrade-verification] |
| Need repo/app command scoping | [monorepo-singlerepo-targeting.md][monorepo-singlerepo-targeting] |

[upgrading-react-native]: references/upgrading-react-native.md
[upgrade-helper-core]: references/upgrade-helper-core.md
[upgrading-dependencies]: references/upgrading-dependencies.md
[react]: references/react.md
[expo-sdk-upgrade]: references/expo-sdk-upgrade.md
[upgrade-verification]: references/upgrade-verification.md
[monorepo-singlerepo-targeting]: references/monorepo-singlerepo-targeting.md

---

## Reference: Expo Sdk Upgrade

# Skill: Expo SDK Upgrade Layer

Expo-specific add-on to the core Upgrade Helper workflow. Use only when `expo` exists in app `package.json`.

## Quick Commands

```bash
npm pkg get dependencies.expo devDependencies.expo --prefix "$APP_DIR"
cd "$APP_DIR" && npx expo install --fix
cd "$APP_DIR" && npx expo-doctor
```

## When to Apply

- `expo` or `expo-updates` is present in the target app package
- RN upgrade is paired with Expo SDK upgrade

## Official Expo Reference

- Follow Expo's official upgrade skill as a primary guide:
  - [Expo Upgrading Expo Skill][expo-upgrading-expo-skill]
- Important for this workflow: skip `app.json` changes, because this is not an Expo Managed project.

## Pre-Upgrade Audit (Required)

- Confirm SDK version and target path.
- Inventory dependencies and native modules.
- Review config plugins and prebuild behavior.
- Review native build setup (Gradle, iOS settings, CI/EAS config).
- Identify critical app flows for regression testing before changes.

## Workflow Additions

1. Run Expo compatibility alignment.
   - `npx expo install --fix` (source of truth for SDK-compatible versions).
   - Treat `expo-modules` package versions as SDK-coupled; align them with Expo recommendations.
2. Run health checks.
   - `npx expo-doctor`; resolve blocking issues first.
3. If native folders are part of workflow, reconcile prebuild output.
   - `npx expo prebuild --clean` (when applicable).
4. Handle React 19 pairing.
   - Run [react.md](react.md).
5. Run [upgrade-verification.md](upgrade-verification.md) for manual regression checks and release gates.

## Notes

- Use `npx expo ...`; do not require global `expo-cli`.
- Some package bumps may be optional if not SDK-bound; validate before deferring.
- Read Expo and React Native release notes deeply before editing code, then map each breaking change to a concrete code/task item.

## Related Skills

- [upgrading-react-native.md](upgrading-react-native.md) - Routing and mode selection
- [upgrade-helper-core.md](upgrade-helper-core.md) - Base upgrade workflow
- [react.md](react.md) - React and React 19 alignment
- [upgrade-verification.md](upgrade-verification.md) - Manual post-upgrade validation
- [monorepo-singlerepo-targeting.md](monorepo-singlerepo-targeting.md) - Repo/app selection and command scoping

[expo-upgrading-expo-skill]: https://github.com/expo/skills/blob/main/plugins/upgrading-expo/skills/upgrading-expo/SKILL.md

---

## Reference: Monorepo Singlerepo Targeting

# Skill: Monorepo vs Single-App Targeting

Small instruction set for selecting the correct app package and running upgrade commands in the right scope.

## Quick Commands

```bash
APP_DIR=apps/mobile
npm pkg get dependencies.react-native devDependencies.react-native --prefix "$APP_DIR"
```

## Rules

1. Pick one target app package before any upgrade command.
2. Run all app-specific commands with `--prefix "$APP_DIR"` or from `cd "$APP_DIR"`.
3. Use `APP_DIR=.` for single-package repos.
4. Never apply diffs to workspace root when RN app lives in a subpackage.

## Verification

- `react-native` is present in `APP_DIR/package.json`.
- `ios/` and `android/` paths used for build/pods are under `APP_DIR`.

## Related Skills

- [upgrading-react-native.md](upgrading-react-native.md) - Routing and mode selection
- [upgrade-helper-core.md](upgrade-helper-core.md) - Base upgrade workflow
- [expo-sdk-upgrade.md](expo-sdk-upgrade.md) - Expo-specific steps

---

## Reference: React

# Skill: React Upgrade Layer

React-specific upgrade rules to run when `react` changes during a React Native or Expo upgrade.

## When to Apply

- `react` version changes (major, minor, or patch).
- React Native target implies a newer React pairing.
- Tests/types break after React upgrade.

## React Pairing Rules

1. Keep companion packages aligned with installed React version:
   - `react-test-renderer`
   - `@types/react`
   - `react-dom` (if used by the app)
2. Prefer matching React major and minor exactly; patch should also match when available.
3. Do not leave these packages on older `x.y` after upgrading `react`.

## React 19 Rules

1. Upgrade `@testing-library/react-native` to `v13+`.
2. Follow:
   - [Expo React 19 Reference][expo-react-19-reference]
   - [RNTL LLM Docs][rntl-llm-docs]
3. Expect type-level breakages from deprecated API removals; fix code and mocks accordingly.

## Related Skills

- [upgrade-helper-core.md](upgrade-helper-core.md) - Core RN upgrade workflow
- [upgrading-dependencies.md](upgrading-dependencies.md) - Dependency compatibility triage
- [expo-sdk-upgrade.md](expo-sdk-upgrade.md) - Expo-specific upgrade layer
- [upgrade-verification.md](upgrade-verification.md) - Post-upgrade manual validation

[expo-react-19-reference]: https://github.com/expo/skills/blob/main/plugins/upgrading-expo/skills/upgrading-expo/references/react-19.md
[rntl-llm-docs]: https://oss.callstack.com/react-native-testing-library/llms.txt

---

## Reference: Upgrade Helper Core

# Skill: Upgrade Helper Core Workflow

Reliable, framework-agnostic workflow for React Native upgrades using Upgrade Helper and rn-diff-purge.

Run shared environment checks first in [upgrading-react-native.md](upgrading-react-native.md) under `Prerequisites (All Upgrade Paths)`.

## Quick Commands

```bash
npm pkg get dependencies.react-native devDependencies.react-native --prefix "$APP_DIR"
npm view react-native dist-tags.latest
curl -L "https://raw.githubusercontent.com/react-native-community/rn-diff-purge/master/RELEASES"
curl -L -o /tmp/rn-diff-<current_version>..<target_version>.diff "https://raw.githubusercontent.com/react-native-community/rn-diff-purge/diffs/diffs/<current_version>..<target_version>.diff"
grep -n "^diff --git" /tmp/rn-diff-<current_version>..<target_version>.diff
```

## Upgrade Helper API (Inline Reference)

- List supported versions:
  - `https://raw.githubusercontent.com/react-native-community/rn-diff-purge/master/RELEASES`
- Fetch raw unified diff:
  - `https://raw.githubusercontent.com/react-native-community/rn-diff-purge/diffs/diffs/<current_version>..<target_version>.diff`
- GitHub compare view:
  - `https://github.com/react-native-community/rn-diff-purge/compare/release/<current_version>..release/<target_version>`
- Upgrade Helper UI:
  - `https://react-native-community.github.io/upgrade-helper/?from=<current_version>&to=<target_version>`
- Path mapping note:
  - Diff paths are prefixed with `RnDiffApp/`; remap to your app paths and package names.

## Inputs

- `APP_DIR`: app package path (`.` for single-package repos)
- `current_version`: current React Native version
- `target_version`: target React Native version (latest by default)

## Reliable Workflow

1. Detect app and versions.
   - Read `react-native` from `APP_DIR/package.json`.
   - Resolve target via `npm view react-native dist-tags.latest` unless user provides one.
2. Validate `target_version` exists.
   - Check `RELEASES` from rn-diff-purge and confirm `target_version` is listed.
   - If missing, stop and ask user to choose one of available versions.
3. Collect canonical sources.
   - Upgrade Helper URL.
   - rn-diff-purge raw diff.
4. Fetch diff with fallback.
   - Try exact raw diff: `<current_version>..<target_version>`.
   - If 404, try nearest available patch versions and report what was attempted.
   - If no available pair works, stop and ask user for target adjustment.
5. Build dependency baseline from rn-diff-purge first.
   - Start with the `RnDiffApp/package.json` diff for the exact version pair.
   - Do not manually install RN packages one-by-one before this baseline is captured.
6. Publish a short execution plan before edits.
   - Include ordered phases: dependency baseline, one-pass install, native/tooling merges, verification.
   - If dependency migrations are ambiguous, ask for user confirmation before modifying package choices.
7. Run dependency risk planning.
   - Use [upgrading-dependencies.md](upgrading-dependencies.md).
   - Fold approved migrations into the same dependency update pass.
8. Apply dependency updates in one pass.
   - Update `APP_DIR/package.json` (and lockfile) from the baseline plus approved migrations.
   - Run exactly one install command with the repo's package manager (`npm install`, `yarn install`, `pnpm install`, or `bun install`).
   - Avoid piecemeal installs such as repeated `npm install <pkg>` unless explicitly requested.
9. Build a change checklist from diff.
   - Group by JS/TS, iOS, Android, tooling.
   - Skip template-only UI (`App.tsx`) unless explicitly requested.
   - Skip template-only dependencies (`@react-native/new-app-screen`) unless they exist in the app.
10. Apply diff safely.
   - Treat `RnDiffApp` as placeholder; remap app/package names.
   - Merge, do not overwrite project-specific customizations.
11. Sync native deps.
   - Run iOS pods in `APP_DIR/ios`.
12. Validate and gate completion.
   - iOS build passes.
   - Android build passes.
   - tests/typecheck/lint pass or failures are documented with next actions.
   - If `react` was upgraded, run [react.md](react.md).
   - If `target_version >= 0.81` and tests fail due to missing modules, add proper mocks.
     - Example (`BackHandler` mock removal): https://github.com/facebook/react-native/issues/52667#issuecomment-3094788618
   - Run [upgrade-verification.md](upgrade-verification.md) before closing the upgrade.

## Stop Conditions

- Missing `react-native` dependency in target package.
- Diff source unavailable and no fallback available.
- Unresolved native merge conflicts in iOS/Android entry files.

## Reliability Rules

- Keep operations version-pair scoped (`current_version -> target_version`).
- Prefer official sources over ad-hoc guides.
- Record every manual deviation from Upgrade Helper.
- Do not run Expo-specific commands here.

## Common Pitfalls

- Upgrading an Expo project with only RN CLI steps: apply the Expo layer ([expo-sdk-upgrade.md](expo-sdk-upgrade.md)).
- Skipping the Upgrade Helper: leads to missed native config changes.
- Treating `RnDiffApp` paths as literal project paths.
- Copying the entire template wholesale: use the diff as a guide and merge only needed changes.
- Using the wrong changelog: `0.7x` changes live in `CHANGELOG-0.7x.md`.
- Running the wrong package manager: always match the repo lockfile.
- Forgetting CocoaPods: iOS builds will fail without `pod install`.
- Not updating Android Gradle wrapper binary: update `android/gradle/wrapper/gradle-wrapper.jar` for the target RN version. Source template:
  - `https://raw.githubusercontent.com/react-native-community/rn-diff-purge/release/<target_version>/RnDiffApp/android/gradle/wrapper/gradle-wrapper.jar`
- Flipper artifacts lingering after removal in v0.74: remove `ReactNativeFlipper.kt` and `FLIPPER_VERSION` when the target RN version drops Flipper.
- Skipping platform rebuilds after Pod/Gradle changes.

## Related Skills

- [upgrading-react-native.md](upgrading-react-native.md) - Routing and mode selection
- [upgrading-dependencies.md](upgrading-dependencies.md) - Dependency compatibility and migration plan
- [expo-sdk-upgrade.md](expo-sdk-upgrade.md) - Expo-only layer on top of core workflow
- [react.md](react.md) - React and React 19 alignment
- [upgrade-verification.md](upgrade-verification.md) - Manual post-upgrade validation
- [monorepo-singlerepo-targeting.md](monorepo-singlerepo-targeting.md) - Repo/app selection and command scoping

---

## Reference: Upgrade Verification

# Skill: Upgrade Verification

Manual validation checklist for human developers after React Native and/or Expo upgrades.

## Scope

- Focus on behavior and UX regressions that static diffs cannot prove.
- Keep checks small, repeatable, and tied to critical user flows.

## Manual Checks (Required)

1. App launch and core journeys work on both iOS and Android.
2. Navigation behavior is correct (forward/back stack, params, deep links, modal flows).
3. Android edge-to-edge is visually correct (status bar, nav bar, safe area insets, keyboard overlays).
4. Permissions and device APIs work (camera, location, notifications, file/media access).
5. Background/restore paths work (app resume, push open, interrupted flows).

## Build and Test Gates

1. Run unit/integration tests and fix all upgrade-related failures.
2. If `target_version >= 0.81` and tests fail due to missing modules, add proper mocks.
   - Example (`BackHandler` mock removal): https://github.com/facebook/react-native/issues/52667#issuecomment-3094788618
3. Build installable artifacts for both platforms.
4. For Expo apps, run `npx expo-doctor` from [expo-sdk-upgrade.md](expo-sdk-upgrade.md).

## Evidence to Capture

- Screen recordings/screenshots for changed flows.
- List of verified scenarios and pass/fail status.
- Follow-up fixes for any observed regressions.

## Related Skills

- [upgrading-react-native.md](upgrading-react-native.md) - Upgrade workflow router
- [upgrade-helper-core.md](upgrade-helper-core.md) - Core RN diff/merge workflow
- [expo-sdk-upgrade.md](expo-sdk-upgrade.md) - Expo-specific checks and commands
- [react.md](react.md) - React-specific upgrade rules

---

## Reference: Upgrading Dependencies

# Skill: Upgrading Dependencies

Common dependency issues and mitigations when upgrading React Native.

## Quick Checks

```bash
npm ls --depth=0
```

## Dependency Risk and Migration Plan

1. Review compatibility signals:
   - [RN nightly tests](https://react-native-community.github.io/nightly-tests/)
   - [React Native Directory](https://reactnative.directory/packages?newArchitecture=false)
2. If `react` is upgraded, run [react.md](react.md) for companion package alignment and React 19 rules.
3. Handle known risky packages:
   - `react-native-fast-image` -> prefer `@d11/react-native-fast-image` or `expo-image` (confirm with user)
   - `@react-native-cookies/cookies` -> prefer `@preeternal/react-native-cookie-manager` (confirm with user)
   - `react-native-code-push` -> treat as incompatible; disable for upgrade and consider `@appzung/react-native-code-push`, `@bravemobile/react-native-code-push`, or `expo-updates`
   - `react-native-image-crop-picker` -> upgrade to `>=0.51.1`; if unstable, plan migration to `expo-image-picker` (confirm with user)
   - `react-native-network-logger` - lists `react` and `react-native` in peer deps as `*` which can be misleading. Upgrade to v2 if `target_version >= 0.79`.
   - `react-native-permissions` - upgrade to v5 if possible (requires RN 0.74+)
4. Apply additional cleanup rules:
   - If `@rnx-kit/metro-resolver-symlinks` is present, remove it from deps and `metro.config.js` (Metro supports symlinks since 0.72)
   - If app uses `react-native-localize` timezone APIs and `@callstack/timezone-hermes-fix` is missing, ask whether to add it
5. If no safe alternative is found for a critical dependency, ask for explicit user confirmation before continuing.
6. Read only breaking/manual steps from RN blog posts between `current_version` and `target_version`.

## Related Skills

- [upgrade-helper-core.md](upgrade-helper-core.md) - Core upgrade workflow
- [react.md](react.md) - React and React 19 alignment
- [expo-sdk-upgrade.md](expo-sdk-upgrade.md) - Expo-specific dependency alignment
- [upgrading-react-native.md](upgrading-react-native.md) - Routing and mode selection

---

## Reference: Upgrading React Native

# Skill: Upgrading React Native

Router for React Native upgrade workflows. Start with core Upgrade Helper instructions, then apply focused add-ons by project shape.

## Prerequisites (All Upgrade Paths)

- Ensure the repo is clean or on a dedicated upgrade branch.
- Know which package manager the repo uses (`npm`, `yarn`, `pnpm`, `bun`).
- Use Node.js `20.19.4+`, Java `17`, and Xcode `16.4+` (with Command Line Tools), following https://reactnative.dev/docs/set-up-your-environment.
  - Optional: use [Xcodes](https://github.com/XcodesOrg/XcodesApp) to manage Xcode versions.
- Verify active versions before upgrading: `node -v`, `java -version`.
- Verify Android Studio is installed.
- For iOS, verify Xcode CLI toolchain is in sync (common pitfall after Xcode upgrades):
  - Check:
    - `xcode-select --print-path`
    - `xcodebuild -version`
    - `xcrun --sdk iphoneos --show-sdk-version`
  - If mismatch is suspected, re-point and initialize:
    - `sudo xcode-select -s /Applications/Xcode.app/Contents/Developer`
    - `sudo xcodebuild -runFirstLaunch`

## Quick Start

0. Run the [Prerequisites (All Upgrade Paths)](#prerequisites-all-upgrade-paths) checklist.
1. Set `APP_DIR` to the app folder (`.` for single-app repos).
2. Use [monorepo-singlerepo-targeting.md](monorepo-singlerepo-targeting.md) if you need help choosing `APP_DIR`.
3. Run [upgrade-helper-core.md](upgrade-helper-core.md) first to anchor changes to rn-diff-purge.
4. Publish a short plan (ordered phases) before making versioned edits.
5. Run [upgrading-dependencies.md](upgrading-dependencies.md) to assess risky packages and migrations.
6. Apply dependency updates in one pass and run a single install with the repo package manager.
7. Run [react.md](react.md) when `react` is upgraded.
8. Add [expo-sdk-upgrade.md](expo-sdk-upgrade.md) only if `expo` is present in `APP_DIR/package.json`.
9. Finish with [upgrade-verification.md](upgrade-verification.md).

## Decision Map

- Need canonical RN diff/merge workflow: [upgrade-helper-core.md](upgrade-helper-core.md)
- Need to ensure dependencies are compatible: [upgrading-dependencies.md](upgrading-dependencies.md)
- Need React and React 19 alignment: [react.md](react.md)
- Project contains Expo SDK deps: [expo-sdk-upgrade.md](expo-sdk-upgrade.md)
- Need manual post-upgrade validation: [upgrade-verification.md](upgrade-verification.md)

## Related Skills

- [native-platform-setup.md](../../react-native-best-practices/references/native-platform-setup.md) - Tooling and native dependency basics
- [native-android-16kb-alignment.md](../../react-native-best-practices/references/native-android-16kb-alignment.md) - Third-party library alignment for Google Play
