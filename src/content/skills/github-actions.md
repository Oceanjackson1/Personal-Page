---
title: "Github Actions"
description: "GitHub Actions workflow patterns for React Native iOS simulator and Android emulator cloud builds with downloadable artifacts. Use when setting up CI build pipelines or downloading GitHub Actions artifacts via gh CLI and GitHub API."
category: "devops"
source: "community"
author: "Community"
tags: ["github", "actions"]
date: 2026-03-20
---

# GitHub Actions Build Artifacts

## Overview

Reusable GitHub Actions patterns to build React Native apps for iOS simulators and Android emulators in the cloud, then publish artifacts retrievable via `gh` CLI or GitHub API.

## When to Apply

Use this skill when:
- Creating CI workflows that build React Native simulator/emulator artifacts.
- Uploading iOS simulator and Android emulator installables from PRs or manual dispatch runs.
- Replacing local-only mobile builds with downloadable CI artifacts.
- Needing stable artifact IDs/names for scripted retrieval with `gh` or REST API.

## Quick Reference

1. Add composite actions from [gha-ios-composite-action.md][gha-ios-composite-action] and [gha-android-composite-action.md][gha-android-composite-action].
2. Wire them into `.github/workflows/mobile-build.yml` from [gha-workflow-and-downloads.md][gha-workflow-and-downloads].
3. Upload with `actions/upload-artifact@v4` and capture `artifact-id` output.
4. Download with `gh run download` or `GET /repos/{owner}/{repo}/actions/artifacts/{artifact_id}/{archive_format}`.

## References

| File | Description |
|------|-------------|
| [gha-ios-composite-action.md][gha-ios-composite-action] | Composite `action.yml` for iOS simulator `.app.tar.gz` builds and artifact upload |
| [gha-android-composite-action.md][gha-android-composite-action] | Composite `action.yml` for Android emulator `.apk` builds and artifact upload |
| [gha-workflow-and-downloads.md][gha-workflow-and-downloads] | End-to-end workflow wiring plus `gh` and REST download commands |

## Problem -> Skill Mapping

| Problem | Start With |
|---------|------------|
| Need CI iOS simulator `.app.tar.gz` artifact | [gha-ios-composite-action.md][gha-ios-composite-action] |
| Need CI Android emulator `.apk` artifact | [gha-android-composite-action.md][gha-android-composite-action] |
| Need one workflow to trigger both platform jobs | [gha-workflow-and-downloads.md][gha-workflow-and-downloads] |
| Need scripted artifact download | [gha-workflow-and-downloads.md][gha-workflow-and-downloads] |

## Source Inspiration

- [callstackincubator/ios/action.yml](https://github.com/callstackincubator/ios/blob/main/action.yml)
- [callstackincubator/android/action.yml](https://github.com/callstackincubator/android/blob/main/action.yml)

[gha-ios-composite-action]: references/gha-ios-composite-action.md
[gha-android-composite-action]: references/gha-android-composite-action.md
[gha-workflow-and-downloads]: references/gha-workflow-and-downloads.md

---

## Reference: Gha Android Composite Action

# Skill: Android Emulator Composite Action (RN CLI)

Composite action template for building React Native Android emulator APKs in GitHub Actions and uploading the resulting artifact.

## Quick Config

1. Create `.github/actions/github-actions/android-build/action.yml`.
2. Copy the template below.
3. Set `variant` (for emulator flows, use `Debug` by default).
4. Use action outputs (`artifact-name`, `artifact-id`, `artifact-url`) in downstream jobs.

## When to Use

- Need cloud Android emulator build artifacts for testing.
- Need configurable debug-style builds from one action.
- Need reliable artifact retrieval through `gh` and REST API.

## Prerequisites

- Linux runner with JDK 17.
- React Native dependencies installed.
- Android SDK and Gradle wrapper available in the repository.

## Template (`.github/actions/github-actions/android-build/action.yml`)

```yaml
name: React Native Android Emulator Build
description: Build React Native Android emulator APK in GitHub Actions and upload artifact

inputs:
  working-directory:
    description: Project root
    required: false
    default: "."
  variant:
    description: Build variant (Debug by default for emulator flows)
    required: false
    default: Debug
  artifact-prefix:
    description: Prefix for artifact naming
    required: false
    default: rn-android-emulator
  custom-identifier:
    description: Optional stable identifier (PR number, channel, etc.)
    required: false
  artifact-retention-days:
    description: GitHub artifact retention
    required: false
    default: "7"

outputs:
  artifact-name:
    description: Uploaded artifact name
    value: ${{ steps.names.outputs.artifact_name }}
  artifact-id:
    description: Uploaded artifact id
    value: ${{ steps.upload.outputs.artifact-id }}
  artifact-url:
    description: Uploaded artifact URL
    value: ${{ steps.upload.outputs.artifact-url }}

runs:
  using: composite
  steps:
    - name: Resolve Android project settings
      id: resolve
      shell: bash
      working-directory: ${{ inputs.working-directory }}
      run: |
        set -euo pipefail

        CONFIG_JSON="$(npx react-native config)"
        ANDROID_SOURCE_DIR="$(printf '%s' "$CONFIG_JSON" | node -e "const fs=require('fs');const j=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(j.project?.android?.sourceDir || 'android')")"
        APP_NAME="$(printf '%s' "$CONFIG_JSON" | node -e "const fs=require('fs');const j=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(j.project?.android?.appName || 'app')")"

        IDENTIFIER="${{ inputs.custom-identifier }}"
        if [[ -z "$IDENTIFIER" ]]; then
          if [[ "${{ github.event_name }}" == "pull_request" ]]; then
            IDENTIFIER="pr-${{ github.event.pull_request.number }}"
          else
            IDENTIFIER="${GITHUB_SHA::7}"
          fi
        fi

        echo "android_source_dir=$ANDROID_SOURCE_DIR" >> "$GITHUB_OUTPUT"
        echo "app_name=$APP_NAME" >> "$GITHUB_OUTPUT"
        echo "identifier=$IDENTIFIER" >> "$GITHUB_OUTPUT"

    - name: Build Android APK
      id: build
      shell: bash
      working-directory: ${{ inputs.working-directory }}
      run: |
        set -euo pipefail

        VARIANT="${{ inputs.variant }}"
        VARIANT_LOWER="$(echo "$VARIANT" | tr '[:upper:]' '[:lower:]')"
        GRADLE_TASK="assemble${VARIANT}"

        (
          cd "${{ steps.resolve.outputs.android_source_dir }}"
          ./gradlew ":${{ steps.resolve.outputs.app_name }}:${GRADLE_TASK}"
        )

        OUTPUT_ROOT="${{ steps.resolve.outputs.android_source_dir }}/${{ steps.resolve.outputs.app_name }}/build/outputs/apk"
        SEARCH_DIR="$OUTPUT_ROOT"
        if [[ -d "$OUTPUT_ROOT/$VARIANT_LOWER" ]]; then
          SEARCH_DIR="$OUTPUT_ROOT/$VARIANT_LOWER"
        fi

        APK_PATH="$(find "$SEARCH_DIR" -type f -name '*.apk' ! -name '*androidTest*' | sort | head -n1 || true)"
        if [[ -z "$APK_PATH" ]]; then
          APK_PATH="$(find "$OUTPUT_ROOT" -type f -name '*.apk' ! -name '*androidTest*' | sort | head -n1 || true)"
        fi

        if [[ -z "$APK_PATH" ]]; then
          echo "No Android APK found"
          exit 1
        fi

        echo "apk_path=$APK_PATH" >> "$GITHUB_OUTPUT"

    - name: Build artifact name
      id: names
      shell: bash
      run: |
        set -euo pipefail

        VARIANT="$(echo "${{ inputs.variant }}" | tr '[:upper:]' '[:lower:]')"
        NAME="${{ inputs.artifact-prefix }}-${VARIANT}-${{ steps.resolve.outputs.identifier }}"
        echo "artifact_name=$NAME" >> "$GITHUB_OUTPUT"

    - name: Upload artifact
      id: upload
      uses: actions/upload-artifact@v4
      with:
        name: ${{ steps.names.outputs.artifact_name }}
        path: ${{ steps.build.outputs.apk_path }}
        if-no-files-found: error
        retention-days: ${{ inputs.artifact-retention-days }}
```

## Common Pitfalls

- Lowercase `variant` values causing wrong Gradle task names.
- Missing JDK setup in caller workflow.
- Hardcoding module name to `app` when `react-native config` reports a custom `appName`.

## Related Skills

- [gha-ios-composite-action.md](gha-ios-composite-action.md)
- [gha-workflow-and-downloads.md](gha-workflow-and-downloads.md)

---

## Reference: Gha Ios Composite Action

# Skill: iOS Simulator Composite Action (RN CLI)

Composite action template for building React Native iOS simulator apps in GitHub Actions and uploading `.app.tar.gz` artifacts.

## Quick Config

1. Create `.github/actions/github-actions/ios-build/action.yml`.
2. Copy the template below.
3. Set your app `scheme` and optional `configuration`.
4. Use `actions/upload-artifact@v4` outputs (`artifact-id`, `artifact-url`).
5. Download later by ID (REST) or by run/name (`gh run download`).

## When to Use

- Need cloud iOS simulator build artifacts for QA or PR validation.
- Need deterministic artifact naming and machine-readable IDs.
- Need RN CLI project discovery without Rock (`npx react-native config`).

## Prerequisites

- macOS runner (`macos-latest` recommended).
- Xcode scheme is known and buildable in CI.
- JS dependencies installed before invoking the action.

## Template (`.github/actions/github-actions/ios-build/action.yml`)

```yaml
name: React Native iOS Simulator Build
description: Build React Native iOS simulator app in GitHub Actions and upload artifact

inputs:
  working-directory:
    description: Project root
    required: false
    default: "."
  scheme:
    description: Xcode scheme
    required: true
  configuration:
    description: Xcode configuration
    required: false
    default: Debug
  workspace-path:
    description: Optional path to .xcworkspace
    required: false
  project-path:
    description: Optional path to .xcodeproj
    required: false
  derived-data-path:
    description: DerivedData path relative to working-directory
    required: false
    default: build/ios/DerivedData
  artifact-prefix:
    description: Prefix for artifact naming
    required: false
    default: rn-ios-simulator
  custom-identifier:
    description: Optional stable identifier (PR number, channel, etc.)
    required: false
  artifact-retention-days:
    description: GitHub artifact retention
    required: false
    default: "7"

outputs:
  artifact-name:
    description: Uploaded artifact name
    value: ${{ steps.names.outputs.artifact_name }}
  artifact-id:
    description: Uploaded artifact id
    value: ${{ steps.upload.outputs.artifact-id }}
  artifact-url:
    description: Uploaded artifact URL
    value: ${{ steps.upload.outputs.artifact-url }}

runs:
  using: composite
  steps:
    - name: Validate inputs
      shell: bash
      run: |
        set -euo pipefail

        if [[ -n "${{ inputs.workspace-path }}" && -n "${{ inputs.project-path }}" ]]; then
          echo "Use workspace-path or project-path, not both"
          exit 1
        fi

    - name: Resolve iOS project settings
      id: resolve
      shell: bash
      working-directory: ${{ inputs.working-directory }}
      run: |
        set -euo pipefail

        CONFIG_JSON="$(npx react-native config)"
        IOS_SOURCE_DIR="$(printf '%s' "$CONFIG_JSON" | node -e "const fs=require('fs');const j=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(j.project?.ios?.sourceDir || 'ios')")"

        WORKSPACE="${{ inputs.workspace-path }}"
        PROJECT="${{ inputs.project-path }}"

        if [[ -z "$WORKSPACE" && -z "$PROJECT" ]]; then
          WORKSPACE="$(find "$IOS_SOURCE_DIR" -maxdepth 2 -name '*.xcworkspace' | head -n1 || true)"
          PROJECT="$(find "$IOS_SOURCE_DIR" -maxdepth 2 -name '*.xcodeproj' | head -n1 || true)"
        fi

        if [[ -n "$WORKSPACE" ]]; then
          CONTAINER_KIND="workspace"
          CONTAINER_PATH="$WORKSPACE"
        elif [[ -n "$PROJECT" ]]; then
          CONTAINER_KIND="project"
          CONTAINER_PATH="$PROJECT"
        else
          echo "Could not find .xcworkspace or .xcodeproj"
          exit 1
        fi

        IDENTIFIER="${{ inputs.custom-identifier }}"
        if [[ -z "$IDENTIFIER" ]]; then
          if [[ "${{ github.event_name }}" == "pull_request" ]]; then
            IDENTIFIER="pr-${{ github.event.pull_request.number }}"
          else
            IDENTIFIER="${GITHUB_SHA::7}"
          fi
        fi

        echo "container_kind=$CONTAINER_KIND" >> "$GITHUB_OUTPUT"
        echo "container_path=$CONTAINER_PATH" >> "$GITHUB_OUTPUT"
        echo "identifier=$IDENTIFIER" >> "$GITHUB_OUTPUT"

    - name: Build iOS simulator
      shell: bash
      working-directory: ${{ inputs.working-directory }}
      run: |
        set -euo pipefail

        if [[ "${{ steps.resolve.outputs.container_kind }}" == "workspace" ]]; then
          XCODE_CONTAINER=( -workspace "${{ steps.resolve.outputs.container_path }}" )
        else
          XCODE_CONTAINER=( -project "${{ steps.resolve.outputs.container_path }}" )
        fi

        xcodebuild \
          "${XCODE_CONTAINER[@]}" \
          -scheme "${{ inputs.scheme }}" \
          -configuration "${{ inputs.configuration }}" \
          -sdk iphonesimulator \
          -destination "generic/platform=iOS Simulator" \
          -derivedDataPath "${{ inputs.derived-data-path }}" \
          CODE_SIGNING_ALLOWED=NO \
          build

    - name: Package simulator app
      id: simulator
      shell: bash
      working-directory: ${{ inputs.working-directory }}
      run: |
        set -euo pipefail

        PRODUCTS_DIR="${{ inputs.derived-data-path }}/Build/Products"
        CONFIG_PRODUCTS_DIR="$PRODUCTS_DIR/${{ inputs.configuration }}-iphonesimulator"
        SEARCH_DIR="$PRODUCTS_DIR"
        if [[ -d "$CONFIG_PRODUCTS_DIR" ]]; then
          SEARCH_DIR="$CONFIG_PRODUCTS_DIR"
        fi

        # Prefer the app matching the scheme, then deterministic non-test fallbacks.
        APP_PATH="$(find "$SEARCH_DIR" -type d -name "${{ inputs.scheme }}.app" | sort | head -n1 || true)"
        if [[ -z "$APP_PATH" ]]; then
          APP_PATH="$(find "$SEARCH_DIR" -type d -name '*.app' \
            ! -name '*Tests*.app' \
            ! -name '*UITests*.app' \
            ! -name '*-Runner.app' \
            | sort | head -n1 || true)"
        fi
        if [[ -z "$APP_PATH" ]]; then
          APP_PATH="$(find "$SEARCH_DIR" -type d -name '*.app' | sort | head -n1 || true)"
        fi

        if [[ -z "$APP_PATH" ]]; then
          echo "No .app found in $SEARCH_DIR"
          exit 1
        fi

        mkdir -p build/ios
        APP_DIR="$(dirname "$APP_PATH")"
        APP_NAME="$(basename "$APP_PATH")"
        TARBALL="build/ios/${APP_NAME%.app}.app.tar.gz"
        tar -C "$APP_DIR" -czf "$TARBALL" "$APP_NAME"

        echo "artifact_path=$TARBALL" >> "$GITHUB_OUTPUT"

    - name: Build artifact name
      id: names
      shell: bash
      run: |
        set -euo pipefail

        CONFIG="$(echo "${{ inputs.configuration }}" | tr '[:upper:]' '[:lower:]')"
        NAME="${{ inputs.artifact-prefix }}-${CONFIG}-${{ steps.resolve.outputs.identifier }}"
        echo "artifact_name=$NAME" >> "$GITHUB_OUTPUT"

    - name: Upload artifact
      id: upload
      uses: actions/upload-artifact@v4
      with:
        name: ${{ steps.names.outputs.artifact_name }}
        path: ${{ steps.simulator.outputs.artifact_path }}
        if-no-files-found: error
        retention-days: ${{ inputs.artifact-retention-days }}
```

## Common Pitfalls

- Passing both `workspace-path` and `project-path`.
- Uploading `.app` directly instead of `tar.gz` (permission loss risk).
- Using non-macOS runner for iOS jobs.

## Related Skills

- [gha-android-composite-action.md](gha-android-composite-action.md)
- [gha-workflow-and-downloads.md](gha-workflow-and-downloads.md)

---

## Reference: Gha Workflow And Downloads

# Skill: Workflow Wiring and Artifact Downloads

Use this workflow to run iOS simulator and Android emulator builds in cloud CI and expose artifact metadata for scripted retrieval.

## Minimum Required Inputs

Set these before first run:
- iOS scheme: exact Xcode scheme name (for example `YourApp`).
- Android variant: Gradle variant for emulator artifacts (usually `Debug`).
- Branch strategy: branches for `push` and `pull_request` triggers (default below uses `main`).
- Retention days: artifact retention period passed to upload steps (for example `7`).

## Repo-Compat Checklist (Before First Run)

- Confirm the iOS scheme exists and builds locally.
- Confirm `pod install` works in CI context from iOS source dir.
- Confirm `android/gradlew` is executable (`chmod +x android/gradlew` if needed).
- Confirm `npx react-native config` resolves valid `project.ios.sourceDir` and `project.android.sourceDir`.

## Quick Config

1. Create `.github/workflows/mobile-build.yml`.
2. Call local composite actions from this skill (`github-actions/ios-build`, `github-actions/android-build`).
3. Keep `actions/upload-artifact@v4` output IDs.
4. Retrieve with `gh run download` or `gh api`.

## When to Use

- Need one pipeline for simulator/emulator artifacts.
- Need PR, push, and manual dispatch triggers.
- Need deterministic artifact retrieval in CI/CD or external tooling.

## Workflow Template (`.github/workflows/mobile-build.yml`)

```yaml
name: RN Cloud Build

on:
  # Baseline trigger strategy: validate incoming changes and direct branch updates.
  push:
    branches: [main]
  pull_request:
    branches: [main]
  workflow_dispatch:
    inputs:
      ios_scheme:
        description: iOS scheme name
        required: true
        default: YourApp
        type: string
      ios_configuration:
        description: iOS configuration
        required: true
        default: Debug
        type: string
      android_variant:
        description: Android Gradle variant
        required: true
        default: Debug
        type: string
      artifact_retention_days:
        description: Artifact retention days
        required: true
        default: '7'
        type: string

permissions:
  contents: read
  actions: read

env:
  IOS_SCHEME: YourApp
  IOS_CONFIGURATION: Debug
  ANDROID_VARIANT: Debug
  ARTIFACT_RETENTION_DAYS: '7'

jobs:
  ios:
    name: iOS simulator build
    runs-on: macos-latest
    outputs:
      artifact_name: ${{ steps.build.outputs.artifact-name }}
      artifact_id: ${{ steps.build.outputs.artifact-id }}
      artifact_url: ${{ steps.build.outputs.artifact-url }}
    steps:
      - uses: actions/checkout@v4

      - name: Resolve Node version from package.json engines
        id: node-version
        run: |
          set -euo pipefail
          NODE_SPEC="$(python3 - <<'PY'
import json
from pathlib import Path
pkg = Path('package.json')
if not pkg.exists():
    print('22')
else:
    data = json.loads(pkg.read_text())
    print((data.get('engines', {}).get('node') or '22').strip())
PY
          )"
          echo "value=$NODE_SPEC" >> "$GITHUB_OUTPUT"

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ steps.node-version.outputs.value }}
          cache: npm

      - name: Install JS dependencies
        run: npm ci

      - name: Install CocoaPods dependencies
        run: |
          set -euo pipefail
          IOS_SOURCE_DIR="$(npx react-native config | node -e "const fs=require('fs');const j=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(j.project?.ios?.sourceDir || 'ios')")"
          cd "$IOS_SOURCE_DIR"
          pod install --repo-update

      # Optional: only add ruby/setup-ruby when this repo enforces Ruby tooling
      # (for example via .ruby-version and Bundler workflow).
      # - uses: ruby/setup-ruby@v1
      #   with:
      #     bundler-cache: true

      - name: Resolve iOS inputs
        id: ios-inputs
        run: |
          if [[ "${{ github.event_name }}" == "workflow_dispatch" ]]; then
            echo "scheme=${{ inputs.ios_scheme }}" >> "$GITHUB_OUTPUT"
            echo "config=${{ inputs.ios_configuration }}" >> "$GITHUB_OUTPUT"
            echo "retention=${{ inputs.artifact_retention_days }}" >> "$GITHUB_OUTPUT"
          else
            echo "scheme=${{ env.IOS_SCHEME }}" >> "$GITHUB_OUTPUT"
            echo "config=${{ env.IOS_CONFIGURATION }}" >> "$GITHUB_OUTPUT"
            echo "retention=${{ env.ARTIFACT_RETENTION_DAYS }}" >> "$GITHUB_OUTPUT"
          fi

      - name: Build iOS simulator
        id: build
        uses: ./.github/actions/github-actions/ios-build
        with:
          scheme: ${{ steps.ios-inputs.outputs.scheme }}
          configuration: ${{ steps.ios-inputs.outputs.config }}
          artifact-prefix: rn-ios-simulator
          artifact-retention-days: ${{ steps.ios-inputs.outputs.retention }}

  android:
    name: Android emulator build
    runs-on: ubuntu-latest
    outputs:
      artifact_name: ${{ steps.build.outputs.artifact-name }}
      artifact_id: ${{ steps.build.outputs.artifact-id }}
      artifact_url: ${{ steps.build.outputs.artifact-url }}
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'
          cache: gradle

      - name: Resolve Node version from package.json engines
        id: node-version
        run: |
          set -euo pipefail
          NODE_SPEC="$(python3 - <<'PY'
import json
from pathlib import Path
pkg = Path('package.json')
if not pkg.exists():
    print('22')
else:
    data = json.loads(pkg.read_text())
    print((data.get('engines', {}).get('node') or '22').strip())
PY
          )"
          echo "value=$NODE_SPEC" >> "$GITHUB_OUTPUT"

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ steps.node-version.outputs.value }}
          cache: npm

      - name: Install JS dependencies
        run: npm ci

      - name: Resolve Android inputs
        id: android-inputs
        run: |
          if [[ "${{ github.event_name }}" == "workflow_dispatch" ]]; then
            echo "variant=${{ inputs.android_variant }}" >> "$GITHUB_OUTPUT"
            echo "retention=${{ inputs.artifact_retention_days }}" >> "$GITHUB_OUTPUT"
          else
            echo "variant=${{ env.ANDROID_VARIANT }}" >> "$GITHUB_OUTPUT"
            echo "retention=${{ env.ARTIFACT_RETENTION_DAYS }}" >> "$GITHUB_OUTPUT"
          fi

      - name: Build Android emulator APK
        id: build
        uses: ./.github/actions/github-actions/android-build
        with:
          variant: ${{ steps.android-inputs.outputs.variant }}
          artifact-prefix: rn-android-emulator
          artifact-retention-days: ${{ steps.android-inputs.outputs.retention }}

  summary:
    name: Build summary
    runs-on: ubuntu-latest
    needs: [ios, android]
    steps:
      - name: Publish artifact metadata
        run: |
          {
            echo "## RN Cloud Build Artifacts"
            echo ""
            echo "- iOS simulator (.app.tar.gz): name=${{ needs.ios.outputs.artifact_name }}, id=${{ needs.ios.outputs.artifact_id }}"
            echo "- Android emulator (.apk): name=${{ needs.android.outputs.artifact_name }}, id=${{ needs.android.outputs.artifact_id }}"
            echo ""
            echo "Artifact URLs (auth required):"
            echo "- iOS: ${{ needs.ios.outputs.artifact_url }}"
            echo "- Android: ${{ needs.android.outputs.artifact_url }}"
          } >> "$GITHUB_STEP_SUMMARY"
```

## CocoaPods and Ruby Notes

- Run `pod install` from `ios/` or from `project.ios.sourceDir` resolved via `npx react-native config`.
- Do not assume Bundler or pinned Ruby is always required.
- `ruby/setup-ruby` is optional and should be added only when repo policy enforces Ruby tooling (for example `.ruby-version` and Bundler-managed pods).

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `ruby/setup-ruby` or Bundler fails | Repo does not require Ruby toolchain in CI | Remove Ruby setup and run plain `pod install` |
| `xcodebuild: Scheme ... not found` | Wrong iOS scheme value | Use exact shared scheme from Xcode project/workspace |
| `Task ':app:assembledebug' not found` | Wrong Android variant casing | Use Gradle-style casing (`Debug`, `Release`, `StagingDebug`) |
| `pod install --repo-update` is slow or flaky | CocoaPods spec repo updates | Retry, cache Pods, or drop `--repo-update` when lockfile + mirror are stable |

## Download Artifacts with `gh`

```bash
# 1) Find recent runs for this workflow
gh run list --workflow "RN Cloud Build" --limit 10

# 2) Download by run id + artifact name
gh run download <run-id> -n <artifact-name> -D ./artifacts

# 3) Inspect artifacts for a run (IDs + names)
gh api repos/<owner>/<repo>/actions/runs/<run-id>/artifacts \
  --jq '.artifacts[] | {id, name, size_in_bytes, expired}'
```

## Download Artifacts with Direct REST API

```bash
# List repo artifacts
curl -sS \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner>/<repo>/actions/artifacts" | jq '.artifacts[] | {id, name}'

# Download one artifact zip by ID
curl -L \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/<owner>/<repo>/actions/artifacts/<artifact-id>/zip" \
  -o artifact.zip
```

## Common Pitfalls

- Forgetting to set `permissions.actions: read` for API-driven artifact listing.
- Assuming artifact URLs are public; they require authenticated access.
- Not pinning artifact names, making `gh run download -n` brittle.

## Related Skills

- [gha-ios-composite-action.md](gha-ios-composite-action.md)
- [gha-android-composite-action.md](gha-android-composite-action.md)
