---
title: "React Native Brownfield Migration"
description: "Provides an incremental adoption strategy to migrate native iOS or Android apps to React Native or Expo using @callstack/react-native-brownfield for initial setup. Use when planning migration steps, packaging XCFramework/AAR artifacts, and integra..."
category: "development"
source: "community"
author: "Community"
tags: ["react", "native", "brownfield", "migration"]
date: 2026-03-20
---

# Migrating to React Native

## Overview

Prescriptive workflow for incremental adoption of React Native in existing native apps using `@callstack/react-native-brownfield`, from initial setup through phased host integration.

- Expo track
- Bare React Native track

Use one track per task unless the user explicitly asks for migration or comparison.

## Migration Strategy

Use this strategy for brownfield migration planning and execution:

1. Assess app state and select Expo or bare path.
2. Perform initial setup with `@callstack/react-native-brownfield`.
3. Package RN artifacts (`XCFramework`/`AAR`) from the RN source app.
4. Integrate one RN surface into the host app and validate startup/runtime.
5. Repeat integration by feature/screen for incremental rollout.

## Agent Guardrails (Global)

Apply these rules across all reference files:

1. Select one path first (Expo or bare) and do not mix steps.
2. Use placeholders from the docs (`<framework_target_name>`, `<android_module_name>`, `<registered_module_name>`) and resolve from project files.
3. Validate each packaging command before moving to host integration.
4. Prefer official docs for long platform snippets and CLI option details.
5. Keep host apps isolated from direct React Native APIs when possible (facade approach).

## Canonical Docs

- [Quick Start](https://oss.callstack.com/react-native-brownfield/docs/getting-started/quick-start.md)
- [Expo Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/expo.md)
- [iOS Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/ios.md)
- [Android Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/android.md)
- [Brownfield CLI](https://oss.callstack.com/react-native-brownfield/docs/cli/brownfield.md)
- [Guidelines](https://oss.callstack.com/react-native-brownfield/docs/guides/guidelines.md)
- [Troubleshooting](https://oss.callstack.com/react-native-brownfield/docs/guides/troubleshooting.md)

## Path Selection Gate (Must Run First)

Before selecting any reference file, classify the project:

1. If no React Native app exists yet, use Expo creation path:
   - [expo-create-app.md][expo-create-app] -> [expo-quick-start.md][expo-quick-start]
2. If React Native app exists, inspect `package.json` and `app.json`:
   - Expo if `expo` is present or Expo plugin workflow is requested.
   - Bare RN if native folders and direct RN CLI workflow are used without Expo path requirements.
3. If still unclear, ask one disambiguation question.
4. Continue with exactly one path.

## When to Apply

Reference this package when:

- Planning incremental migration from native-only apps to React Native or Expo
- Creating brownfield integration flows for Expo or bare React Native projects
- Performing initial setup with `@callstack/react-native-brownfield`
- Generating iOS XCFramework artifacts from a React Native app
- Generating and publishing Android AAR artifacts from a React Native app
- Integrating generated artifacts into host iOS/Android apps

## Quick Reference

| File | Description |
|------|-------------|
| [quick-start.md][quick-start] | Shared preflight and mandatory path-selection gate |
| [expo-create-app.md][expo-create-app] | Scaffold a new Expo app before Expo brownfield setup |
| [expo-quick-start.md][expo-quick-start] | Expo plugin setup and packaging readiness |
| [expo-ios-integration.md][expo-ios-integration] | Expo iOS packaging and host startup integration |
| [expo-android-integration.md][expo-android-integration] | Expo Android packaging, publish, and host integration |
| [bare-quick-start.md][bare-quick-start] | Bare React Native baseline setup |
| [bare-ios-xcframework-generation.md][bare-ios-xcframework-generation] | Bare iOS XCFramework generation |
| [bare-android-aar-generation.md][bare-android-aar-generation] | Bare Android AAR generation and publish |
| [bare-ios-native-integration.md][bare-ios-native-integration] | Bare iOS host integration |
| [bare-android-native-integration.md][bare-android-native-integration] | Bare Android host integration |

## Problem -> Skill Mapping

| Problem | Start With |
|---------|------------|
| Need path decision first | [quick-start.md][quick-start] |
| Need to create a new Expo app for brownfield | [expo-create-app.md][expo-create-app] |
| Need Expo brownfield setup and plugin wiring | [expo-quick-start.md][expo-quick-start] |
| Need Expo iOS brownfield integration | [expo-ios-integration.md][expo-ios-integration] |
| Need Expo Android brownfield integration | [expo-android-integration.md][expo-android-integration] |
| Need bare RN baseline setup | [bare-quick-start.md][bare-quick-start] |
| Need bare RN iOS XCFramework generation | [bare-ios-xcframework-generation.md][bare-ios-xcframework-generation] |
| Need bare RN Android AAR generation/publish | [bare-android-aar-generation.md][bare-android-aar-generation] |
| Need bare RN iOS host integration | [bare-ios-native-integration.md][bare-ios-native-integration] |
| Need bare RN Android host integration | [bare-android-native-integration.md][bare-android-native-integration] |

[quick-start]: references/quick-start.md
[expo-create-app]: references/expo-create-app.md
[expo-quick-start]: references/expo-quick-start.md
[expo-ios-integration]: references/expo-ios-integration.md
[expo-android-integration]: references/expo-android-integration.md
[bare-quick-start]: references/bare-quick-start.md
[bare-ios-xcframework-generation]: references/bare-ios-xcframework-generation.md
[bare-android-aar-generation]: references/bare-android-aar-generation.md
[bare-ios-native-integration]: references/bare-ios-native-integration.md
[bare-android-native-integration]: references/bare-android-native-integration.md

---

## Reference: Bare Android Aar Generation

# Skill: Bare Android AAR Generation

Package a bare React Native app into an Android AAR and publish it for native host consumption.

## Quick Command

```bash
npx brownfield package:android --variant release --module-name <android_module_name>
npx brownfield publish:android --module-name <android_module_name>
```

## When to Use

- Building Android artifact from bare RN app
- Publishing AAR for host app dependency resolution

## Prerequisites

- [bare-quick-start.md](./bare-quick-start.md) completed
- Dedicated Android library module exists (`com.android.library`)
- Brownfield Gradle plugin configured
- RN and Hermes dependency versions aligned with `package.json`

## Step-by-Step Instructions

```text
Progress checklist:
- [ ] Library module verified
- [ ] Plugin + autolinking configured
- [ ] Publishing configured
- [ ] package:android succeeds
- [ ] publish:android succeeds
- [ ] Host app resolves Maven coordinate
```

1. Verify target module is a library module and will be passed as `--module-name`.
2. Ensure module plugins include:
   - `com.android.library`
   - `org.jetbrains.kotlin.android`
   - `com.facebook.react`
   - `com.callstack.react.brownfield`
   - `maven-publish`
3. Ensure autolinking is enabled in module:

```kotlin
react {
    autolinkLibrariesWithApp()
}
```

4. Add/verify facade bootstrap class in artifact module (host app should call only this facade):

```kotlin
object ReactNativeHostManager {
    fun initialize(application: Application, onJSBundleLoaded: OnJSBundleLoaded? = null) {
        loadReactNative(application)
        val packageList = PackageList(application).packages
        ReactNativeBrownfield.initialize(application, packageList, onJSBundleLoaded)
    }
}
```

5. Package AAR:
   - `npx brownfield package:android --variant release --module-name <android_module_name>`
6. Publish to Maven local:
   - `npx brownfield publish:android --module-name <android_module_name>`
7. Validate host app resolves `groupId:artifactId:version` with `mavenLocal()` enabled.

## Stop Conditions

Proceed only if:

- package and publish commands exit with code `0`
- host app resolves published coordinate

## If Failed

- Re-check module type (`com.android.library`) and module-name flag
- Re-check plugin configuration and `maven-publish`
- Clean/rebuild Android project and retry package/publish
- Do not proceed to runtime integration until coordinate resolution passes

## Canonical Docs

- [Android Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/android.md)
- [Brownfield CLI](https://oss.callstack.com/react-native-brownfield/docs/cli/brownfield.md)
- [Guidelines](https://oss.callstack.com/react-native-brownfield/docs/guides/guidelines.md)
- [Troubleshooting](https://oss.callstack.com/react-native-brownfield/docs/guides/troubleshooting.md)

## Common Pitfalls

- Using app module instead of library module for packaging
- RN/Hermes dependency mismatch vs `package.json`
- Missing `mavenLocal()` in host dependency resolution

## Related Skills

- [bare-quick-start.md](./bare-quick-start.md) - Bare setup prerequisites
- [bare-android-native-integration.md](./bare-android-native-integration.md) - Bare Android host integration

---

## Reference: Bare Android Native Integration

# Skill: Bare Android Native Integration

Consume published bare RN AAR in host Android app and verify runtime rendering.

## Quick Command

```kotlin
// settings.gradle.kts
repositories { mavenLocal() }

// app/build.gradle.kts
dependencies { implementation("<groupId>:<artifactId>:<version>") }
```

## When to Use

- Consuming locally published AAR from bare RN artifact module
- Wiring host startup and rendering for RN-powered screens

## Prerequisites

- [bare-android-aar-generation.md](./bare-android-aar-generation.md) completed
- AAR published to local Maven
- Host app Gradle sync is healthy

## Step-by-Step Instructions

```text
Progress checklist:
- [ ] Add mavenLocal in host repositories
- [ ] Add dependency coordinate
- [ ] Initialize host runtime
- [ ] Render RN module
```

1. Add `mavenLocal()` in host `dependencyResolutionManagement` repositories.
2. Add published dependency coordinate in app module.
3. Initialize runtime before RN UI creation:

```kotlin
ReactNativeHostManager.initialize(this.application) {
    println("JS bundle loaded")
}
```

4. Render RN UI:
   - `ReactNativeFragment.createReactNativeFragment("<registered_module_name>")`
   - or `ReactNativeBrownfield.shared.createView(...)`
5. Verify host app resolves dependency and RN module renders.

## Stop Conditions

Mark complete only if:

- Gradle sync/build succeeds with published coordinate
- runtime initializes before UI creation
- RN module renders expected screen

## If Failed

- Re-check coordinate and repository order
- Re-package and re-publish if artifact is stale
- Re-check module name registration in JS

## Canonical Docs

- [Android Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/android.md)
- [Guidelines](https://oss.callstack.com/react-native-brownfield/docs/guides/guidelines.md)
- [Troubleshooting](https://oss.callstack.com/react-native-brownfield/docs/guides/troubleshooting.md)

## Common Pitfalls

- Missing `mavenLocal()`
- Dependency coordinate mismatch
- Creating RN UI before host manager initialization

## Related Skills

- [bare-android-aar-generation.md](./bare-android-aar-generation.md) - Bare Android artifact generation
- [bare-quick-start.md](./bare-quick-start.md) - Bare setup prerequisites

---

## Reference: Bare Ios Native Integration

# Skill: Bare iOS Native Integration

Integrate bare RN XCFramework artifacts into native iOS host app and verify startup/runtime behavior.

## Quick Command

```swift
ReactNativeBrownfield.shared.bundle = ReactNativeBundle
ReactNativeBrownfield.shared.startReactNative { print("React Native bundle loaded") }
```

## When to Use

- Consuming generated bare RN XCFrameworks in host iOS app
- Wiring runtime initialization for UIKit or SwiftUI entrypoints

## Prerequisites

- [bare-ios-xcframework-generation.md](./bare-ios-xcframework-generation.md) completed
- Artifacts available in package output (`ios/.brownfield/package` or `.brownfield/ios/package`)
- Host app builds in Xcode

## Step-by-Step Instructions

```text
Progress checklist:
- [ ] Link generated frameworks
- [ ] Initialize RN startup
- [ ] Render registered module
- [ ] Verify Debug and Release behavior
```

1. Link these frameworks into host app:
   - `<framework_target_name>.xcframework`
   - `ReactBrownfield.xcframework`
   - `hermesvm.xcframework` (or `hermes.xcframework` for older RN)
2. In app startup:

```swift
import <framework_target_name>

ReactNativeBrownfield.shared.bundle = ReactNativeBundle
ReactNativeBrownfield.shared.startReactNative(onBundleLoaded: {
    print("React Native bundle loaded")
}, launchOptions: launchOptions)
```

3. Render RN UI with JS-registered module name:
   - UIKit: `ReactNativeViewController(moduleName: "<registered_module_name>")`
   - SwiftUI: `ReactNativeView(moduleName: "<registered_module_name>")`
4. Validate:
   - Debug with Metro (`npx react-native start`)
   - Release without Metro

## Stop Conditions

Mark complete only if:

- host app builds in Debug and Release
- RN module renders in both configurations

## If Failed

- Re-check startup order: set bundle -> start runtime -> create RN view/controller
- Re-check `moduleName` matches `AppRegistry.registerComponent`
- Re-link all required frameworks if Release cannot load JS

## Canonical Docs

- [iOS Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/ios.md)
- [Swift API](https://oss.callstack.com/react-native-brownfield/docs/api-reference/react-native-brownfield/swift.md)
- [Troubleshooting](https://oss.callstack.com/react-native-brownfield/docs/guides/troubleshooting.md)

## Common Pitfalls

- Missing `ReactNativeBrownfield.shared.bundle = ReactNativeBundle`
- Wrong module name compared to JS registration
- Linking only app XCFramework without brownfield/hermes frameworks

## Related Skills

- [bare-ios-xcframework-generation.md](./bare-ios-xcframework-generation.md) - Bare iOS artifact generation
- [bare-quick-start.md](./bare-quick-start.md) - Bare setup prerequisites

---

## Reference: Bare Ios Xcframework Generation

# Skill: Bare iOS XCFramework Generation

Package a bare React Native app into XCFramework artifacts for native iOS host consumption.

## Quick Command

```bash
npx brownfield package:ios --scheme <framework_target_name> --configuration Release
```

## When to Use

- Building iOS artifacts from a bare RN app
- Rebuilding XCFramework after RN/native dependency updates

## Prerequisites

- [bare-quick-start.md](./bare-quick-start.md) completed
- Framework target exists in `ios/*.xcworkspace`
- Podfile includes framework target with `inherit! :complete`
- If running `pod install` directly, static linking is configured as recommended in iOS integration docs
- Framework target build settings:
  - Build Libraries for Distribution = `YES`
  - User Script Sandboxing = `NO`
  - Skip Install = `NO`
  - Enable Module Verifier = `NO`

## Step-by-Step Instructions

```text
Progress checklist:
- [ ] Framework target + Podfile ready
- [ ] Bundle script present on framework target
- [ ] Public interface file exports ReactBrownfield
- [ ] package:ios succeeds
- [ ] Artifacts validated
```

1. Create or verify framework target in Xcode workspace.
   - If target folders are folder references, convert them to groups (per iOS integration docs).
2. Ensure Podfile has nested framework target and run `pod install`.
3. Ensure framework target includes `Bundle React Native code and images` run script with expected input files (`$(SRCROOT)/.xcode.env.local`, `$(SRCROOT)/.xcode.env`).
4. Add framework interface file:

```swift
@_exported import ReactBrownfield
public let ReactNativeBundle = Bundle(for: InternalClassForBundle.self)
class InternalClassForBundle {}
```

5. Package framework:
   - `npx brownfield package:ios --scheme <framework_target_name> --configuration Release`
6. Validate output directory produced by command (commonly `ios/.brownfield/package` or `.brownfield/ios/package`):
   - `<framework_target_name>.xcframework`
   - `ReactBrownfield.xcframework`
   - `hermesvm.xcframework` (or `hermes.xcframework` for older RN)

## Stop Conditions

Proceed only if:

- package command exits with code `0`
- all required frameworks are present in package output

## If Failed

- Re-run pods and retry package command
- Re-check framework target build settings and run script phase
- Do not proceed to host integration until artifacts are complete

## Canonical Docs

- [iOS Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/ios.md)
- [Brownfield CLI](https://oss.callstack.com/react-native-brownfield/docs/cli/brownfield.md)
- [Troubleshooting](https://oss.callstack.com/react-native-brownfield/docs/guides/troubleshooting.md)

## Common Pitfalls

- Packaging app target instead of framework target
- Missing bundle run script on framework target
- Incomplete framework set linked into host app

## Related Skills

- [bare-quick-start.md](./bare-quick-start.md) - Bare setup prerequisites
- [bare-ios-native-integration.md](./bare-ios-native-integration.md) - Bare iOS host integration

---

## Reference: Bare Quick Start

# Skill: Bare React Native Quick Start

Prepare a bare React Native project for brownfield packaging and host integration.

## Quick Command

```bash
npm install @callstack/react-native-brownfield
cd ios && pod install && cd ..
```

## When to Use

- User explicitly chooses bare React Native path
- Project directly manages native iOS/Android folders

## Prerequisites

- Bare RN app with working `ios/` and `android/`
- CocoaPods and Gradle working

## Step-by-Step Instructions

```text
Progress checklist:
- [ ] Install package
- [ ] Install pods
- [ ] Continue to bare platform packaging
```

1. Install package in RN app root.
2. Run `pod install` for iOS.
3. Continue with one platform packaging file:
   - [bare-ios-xcframework-generation.md](./bare-ios-xcframework-generation.md)
   - [bare-android-aar-generation.md](./bare-android-aar-generation.md)

## Canonical Docs

- [Quick Start](https://oss.callstack.com/react-native-brownfield/docs/getting-started/quick-start.md)
- [iOS Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/ios.md)
- [Android Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/android.md)

## Common Pitfalls

- Starting packaging before `pod install`
- Mixing Expo-only startup APIs into bare flow

## Related Skills

- [quick-start.md](./quick-start.md) - Shared path-selection gate
- [bare-ios-xcframework-generation.md](./bare-ios-xcframework-generation.md) - Bare iOS artifact generation
- [bare-android-aar-generation.md](./bare-android-aar-generation.md) - Bare Android artifact generation

---

## Reference: Expo Android Integration

# Skill: Expo Android Integration

Package and publish Expo Android AAR, then initialize host runtime and mount RN UI.

## Quick Command

```bash
npx brownfield package:android --module-name <android_module_name> --variant release
npx brownfield publish:android --module-name <android_module_name>
```

## When to Use

- User requests Expo Android brownfield integration
- Host app must consume Expo-backed RN AAR

## Prerequisites

- [expo-quick-start.md](./expo-quick-start.md) completed
- Android host app builds and syncs
- Android module name resolved (`brownfieldlib` by default unless overridden in Expo plugin options)

## Step-by-Step Instructions

```text
Progress checklist:
- [ ] Package AAR
- [ ] Publish to Maven local
- [ ] Initialize host runtime
- [ ] Render RN module
```

1. Build AAR:
   - `npx brownfield package:android --module-name <android_module_name> --variant release`
2. Publish to Maven local:
   - `npx brownfield publish:android --module-name <android_module_name>`
3. Initialize runtime in `Activity` or `Application`:

```kotlin
ReactNativeHostManager.initialize(application) {
  Toast.makeText(this, "React Native has been loaded", Toast.LENGTH_LONG).show()
}
```

4. Forward configuration changes:

```kotlin
override fun onConfigurationChanged(newConfig: Configuration) {
    super.onConfigurationChanged(newConfig)
    ReactNativeHostManager.onConfigurationChanged(application, newConfig)
}
```

5. Render RN UI with JS-registered module name:
   - `ReactNativeFragment.createReactNativeFragment("<registered_module_name>")`
   - or `ReactNativeBrownfield.shared.createView(context, activity, "<registered_module_name>")`

## Stop Conditions

Mark complete only if:

- package and publish commands both exit with code `0`
- host app resolves published dependency and renders module

## Canonical Docs

- [Expo Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/expo.md)
- [Android Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/android.md)
- [Brownfield CLI](https://oss.callstack.com/react-native-brownfield/docs/cli/brownfield.md)

## Common Pitfalls

- Using `ComponentActivity` with Expo (use `AppCompatActivity`)
- Missing `ReactNativeHostManager.initialize(...)` before UI creation
- Module name mismatch with `AppRegistry.registerComponent`

## Related Skills

- [expo-quick-start.md](./expo-quick-start.md) - Expo setup and plugin wiring
- [expo-ios-integration.md](./expo-ios-integration.md) - Expo iOS equivalent

---

## Reference: Expo Create App

# Skill: Expo Create App for Brownfield

Create a new Expo app as the source project for Expo brownfield packaging and host integration.

## Quick Command

```bash
npx create-expo-app@latest my-expo-brownfield --yes
```

## When to Use

- User wants to add React Native to native apps via Expo path
- No existing Expo/RN project is available for brownfield packaging

## Prerequisites

- Node.js and `npx` available
- New project directory name selected

## Step-by-Step Instructions

```text
Progress checklist:
- [ ] Create Expo app
- [ ] Install brownfield package
- [ ] Continue on Expo-only path
```

1. Create a new Expo app in a standalone directory (not inside existing iOS/Android host repo).
2. `cd my-expo-brownfield`
3. Install brownfield package: `npm install @callstack/react-native-brownfield`
4. Continue to [expo-quick-start.md](./expo-quick-start.md).

## Stop Conditions

Proceed only if:

- create command exits with code `0`
- `app.json` exists at project root

## Canonical Docs

- [Expo Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/expo.md)
- [Quick Start](https://oss.callstack.com/react-native-brownfield/docs/getting-started/quick-start.md)

## Common Pitfalls

- Creating Expo app inside host native app project
- Jumping to iOS/Android integration before Expo plugin setup

## Related Skills

- [quick-start.md](./quick-start.md) - Path-selection gate
- [expo-quick-start.md](./expo-quick-start.md) - Expo plugin and packaging setup

---

## Reference: Expo Ios Integration

# Skill: Expo iOS Integration

Package Expo app as XCFramework artifacts, link them into host iOS app, and initialize Expo-compatible RN runtime.

## Quick Command

```bash
npx brownfield package:ios --scheme <framework_target_name> --configuration Release
```

## When to Use

- User requests Expo iOS brownfield integration
- Host app must render Expo-backed React Native UI

## Prerequisites

- [expo-quick-start.md](./expo-quick-start.md) completed
- iOS host app builds successfully
- Framework scheme name resolved (`BrownfieldLib` by default unless overridden in Expo plugin options)

## Step-by-Step Instructions

```text
Progress checklist:
- [ ] Package XCFrameworks
- [ ] Link frameworks in host app
- [ ] Configure startup
- [ ] Render RN module
```

1. Package iOS artifacts:
   - `npx brownfield package:ios --scheme <framework_target_name> --configuration Release`
2. Link artifacts from package output directory (`ios/.brownfield/package` or `.brownfield/ios/package`) into host app project:
   - `<framework_target_name>.xcframework`
   - `ReactBrownfield.xcframework`
   - `hermesvm.xcframework` (or `hermes.xcframework` for older RN)
3. Initialize runtime in app entrypoint:

```swift
ReactNativeBrownfield.shared.bundle = ReactNativeBundle
ReactNativeBrownfield.shared.startReactNative {
    print("React Native has been loaded")
}
ReactNativeBrownfield.shared.ensureExpoModulesProvider()
```

4. Forward `didFinishLaunchingWithOptions` to brownfield handler.
5. Render RN UI using the module registered in JS (`AppRegistry.registerComponent`):
   - `ReactNativeView(moduleName: "<registered_module_name>")`
   - or `ReactNativeBrownfield.shared.view(moduleName: "<registered_module_name>", initialProps: nil)`

## Stop Conditions

Mark complete only if:

- package command exits with code `0`
- host app builds in Debug and Release
- selected module renders successfully

## Canonical Docs

- [Expo Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/expo.md)
- [iOS Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/ios.md)
- [Swift API](https://oss.callstack.com/react-native-brownfield/docs/api-reference/react-native-brownfield/swift.md)

## Common Pitfalls

- Missing `ensureExpoModulesProvider()` in Expo startup flow
- Not forwarding `didFinishLaunchingWithOptions`
- Using wrong module name instead of JS-registered component name

## Related Skills

- [expo-quick-start.md](./expo-quick-start.md) - Expo setup and plugin wiring
- [expo-android-integration.md](./expo-android-integration.md) - Expo Android equivalent

---

## Reference: Expo Quick Start

# Skill: Expo Brownfield Quick Start

Configure Expo project for brownfield packaging before iOS/Android host integration.

## Quick Command

```bash
npm install @callstack/react-native-brownfield
```

## When to Use

- Expo managed or prebuild project needs brownfield packaging
- Continuing after [expo-create-app.md](./expo-create-app.md)

## Prerequisites

- Expo project with `app.json`
- Expo path selected in router

## Step-by-Step Instructions

```text
Progress checklist:
- [ ] Install package
- [ ] Configure plugin
- [ ] Continue to platform integration
```

1. Install package in the Expo project.
2. Add plugin to `app.json`:

```json
{
  "plugins": ["@callstack/react-native-brownfield"]
}
```

3. Optionally add package scripts for packaging/publish commands used by your team.
4. Continue to exactly one platform file:
   - [expo-ios-integration.md](./expo-ios-integration.md)
   - [expo-android-integration.md](./expo-android-integration.md)

## Canonical Docs

- [Expo Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/expo.md)
- [Brownfield CLI](https://oss.callstack.com/react-native-brownfield/docs/cli/brownfield.md)

## Common Pitfalls

- Missing plugin entry in `app.json`
- Mixing Expo flow with bare packaging files

## Related Skills

- [quick-start.md](./quick-start.md) - Path-selection gate
- [expo-ios-integration.md](./expo-ios-integration.md) - Expo iOS integration
- [expo-android-integration.md](./expo-android-integration.md) - Expo Android integration

---

## Reference: Quick Start

# Skill: Brownfield Quick Start

Run shared setup, select one path (Expo or bare), and route immediately to path-specific instructions.

## Quick Command

```bash
npm install @callstack/react-native-brownfield
```

## When to Use

- Starting brownfield setup and deciding between Expo and bare RN
- Preparing project prerequisites before platform-specific packaging

## Prerequisites

- React Native project root identified
- Node.js and package manager available

## Step-by-Step Instructions

```text
Progress checklist:
- [ ] Install package
- [ ] Select Expo or bare path
- [ ] Continue only on selected path
```

1. Install package in the React Native app root.
2. Classify request/project intent:
   - Expo signals: `expo`, `prebuild`, Expo plugin workflow
   - Bare signals: direct RN CLI workflow, explicit XCFramework/AAR-only path
3. Route to exactly one path:
   - Expo path: [expo-create-app.md](./expo-create-app.md) (if no RN app yet) -> [expo-quick-start.md](./expo-quick-start.md)
   - Bare path: [bare-quick-start.md](./bare-quick-start.md)
4. If unclear, ask one disambiguation question and stop.

## Stop Conditions

Proceed only if:

- package install exits with code `0`
- exactly one path is selected

## If Failed

- If install fails, retry with the active package manager and lockfile sync
- If path intent is ambiguous, stop and ask one Expo vs bare question

## Canonical Docs

- [Quick Start](https://oss.callstack.com/react-native-brownfield/docs/getting-started/quick-start.md)
- [Expo Integration](https://oss.callstack.com/react-native-brownfield/docs/getting-started/expo.md)

## Common Pitfalls

- Mixing Expo and bare steps in one flow
- Starting platform integration before path selection

## Related Skills

- [expo-create-app.md](./expo-create-app.md) - Create new Expo app for brownfield
- [expo-quick-start.md](./expo-quick-start.md) - Expo setup and plugin wiring
- [bare-quick-start.md](./bare-quick-start.md) - Bare RN baseline setup
