---
title: "React Native 最佳实践"
description: "React Native 移动应用开发最佳实践，性能优化和跨平台策略"
category: "development"
source: "community"
author: "Community"
tags: ["react", "native"]
date: 2026-03-20
---

# React Native Best Practices

## Overview

Performance optimization guide for React Native applications, covering JavaScript/React, Native (iOS/Android), and bundling optimizations. Based on Callstack's "Ultimate Guide to React Native Optimization".

## Skill Format

Each reference file follows a hybrid format for fast lookup and deep understanding:

- **Quick Pattern**: Incorrect/Correct code snippets for immediate pattern matching
- **Quick Command**: Shell commands for process/measurement skills
- **Quick Config**: Configuration snippets for setup-focused skills
- **Quick Reference**: Summary tables for conceptual skills
- **Deep Dive**: Full context with When to Use, Prerequisites, Step-by-Step, Common Pitfalls

**Impact ratings**: CRITICAL (fix immediately), HIGH (significant improvement), MEDIUM (worthwhile optimization)

## When to Apply

Reference these guidelines when:
- Debugging slow/janky UI or animations
- Investigating memory leaks (JS or native)
- Optimizing app startup time (TTI)
- Reducing bundle or app size
- Writing native modules (Turbo Modules)
- Profiling React Native performance
- Reviewing React Native code for performance

## Security Notes

- Treat shell commands in these references as local developer operations. Review them before running, prefer version-pinned tooling, and avoid piping remote scripts directly to a shell.
- Treat third-party libraries and plugins as dependencies that still require normal supply-chain controls: pin versions, verify provenance, and update through your standard review process.
- Treat Re.Pack code splitting as first-party artifact delivery only. Remote chunks must come from trusted HTTPS origins you control and be pinned to the current app release.

## Priority-Ordered Guidelines

| Priority | Category | Impact | Prefix |
|----------|----------|--------|--------|
| 1 | FPS & Re-renders | CRITICAL | `js-*` |
| 2 | Bundle Size | CRITICAL | `bundle-*` |
| 3 | TTI Optimization | HIGH | `native-*`, `bundle-*` |
| 4 | Native Performance | HIGH | `native-*` |
| 5 | Memory Management | MEDIUM-HIGH | `js-*`, `native-*` |
| 6 | Animations | MEDIUM | `js-*` |

## Quick Reference

### Optimization Workflow

Follow this cycle for any performance issue: **Measure → Optimize → Re-measure → Validate**

1. **Measure**: Capture baseline metrics (FPS, TTI, bundle size) before changes
2. **Optimize**: Apply the targeted fix from the relevant reference
3. **Re-measure**: Run the same measurement to get updated metrics
4. **Validate**: Confirm improvement (e.g., FPS 45→60, TTI 3.2s→1.8s, bundle 2.1MB→1.6MB)

If metrics did not improve, revert and try the next suggested fix.

### Critical: FPS & Re-renders

**Profile first:**
```bash
# Open React Native DevTools
# Press 'j' in Metro, or shake device → "Open DevTools"
```

**Common fixes:**
- Replace ScrollView with FlatList/FlashList for lists
- Use React Compiler for automatic memoization
- Use atomic state (Jotai/Zustand) to reduce re-renders
- Use `useDeferredValue` for expensive computations

### Critical: Bundle Size

**Analyze bundle:**
```bash
npx react-native bundle \
  --entry-file index.js \
  --bundle-output output.js \
  --platform ios \
  --sourcemap-output output.js.map \
  --dev false --minify true

npx source-map-explorer output.js --no-border-checks
```

**Verify improvement after optimization:**
```bash
# Record baseline size before changes
ls -lh output.js  # e.g., Before: 2.1 MB

# After applying fixes, re-bundle and compare
npx react-native bundle --entry-file index.js --bundle-output output.js \
  --platform ios --dev false --minify true
ls -lh output.js  # e.g., After: 1.6 MB  (24% reduction)
```

**Common fixes:**
- Avoid barrel imports (import directly from source)
- Remove unnecessary Intl polyfills (Hermes has native support)
- Enable tree shaking (Expo SDK 52+ or Re.Pack)
- Enable R8 for Android native code shrinking

### High: TTI Optimization

**Measure TTI:**
- Use `react-native-performance` for markers
- Only measure cold starts (exclude warm/hot/prewarm)

**Common fixes:**
- Disable JS bundle compression on Android (enables Hermes mmap)
- Use native navigation (react-native-screens)
- Preload commonly-used expensive screens before navigating to them

### High: Native Performance

**Profile native:**
- iOS: Xcode Instruments → Time Profiler
- Android: Android Studio → CPU Profiler

**Common fixes:**
- Use background threads for heavy native work
- Prefer async over sync Turbo Module methods
- Use C++ for cross-platform performance-critical code

## References

Full documentation with code examples in [references/][references]:

### JavaScript/React (`js-*`)

| File | Impact | Description |
|------|--------|-------------|
| [js-lists-flatlist-flashlist.md][js-lists-flatlist-flashlist] | CRITICAL | Replace ScrollView with virtualized lists |
| [js-profile-react.md][js-profile-react] | MEDIUM | React DevTools profiling |
| [js-measure-fps.md][js-measure-fps] | HIGH | FPS monitoring and measurement |
| [js-memory-leaks.md][js-memory-leaks] | MEDIUM | JS memory leak hunting |
| [js-atomic-state.md][js-atomic-state] | HIGH | Jotai/Zustand patterns |
| [js-concurrent-react.md][js-concurrent-react] | HIGH | useDeferredValue, useTransition |
| [js-react-compiler.md][js-react-compiler] | HIGH | Automatic memoization |
| [js-animations-reanimated.md][js-animations-reanimated] | MEDIUM | Reanimated worklets |
| [js-uncontrolled-components.md][js-uncontrolled-components] | HIGH | TextInput optimization |

### Native (`native-*`)

| File | Impact | Description |
|------|--------|-------------|
| [native-turbo-modules.md][native-turbo-modules] | HIGH | Building fast native modules |
| [native-sdks-over-polyfills.md][native-sdks-over-polyfills] | HIGH | Native vs JS libraries |
| [native-measure-tti.md][native-measure-tti] | HIGH | TTI measurement setup |
| [native-threading-model.md][native-threading-model] | HIGH | Turbo Module threads |
| [native-profiling.md][native-profiling] | MEDIUM | Xcode/Android Studio profiling |
| [native-platform-setup.md][native-platform-setup] | MEDIUM | iOS/Android tooling guide |
| [native-view-flattening.md][native-view-flattening] | MEDIUM | View hierarchy debugging |
| [native-memory-patterns.md][native-memory-patterns] | MEDIUM | C++/Swift/Kotlin memory |
| [native-memory-leaks.md][native-memory-leaks] | MEDIUM | Native memory leak hunting |
| [native-android-16kb-alignment.md][native-android-16kb-alignment] | CRITICAL | Third-party library alignment for Google Play |

### Bundling (`bundle-*`)

| File | Impact | Description |
|------|--------|-------------|
| [bundle-barrel-exports.md][bundle-barrel-exports] | CRITICAL | Avoid barrel imports |
| [bundle-analyze-js.md][bundle-analyze-js] | CRITICAL | JS bundle visualization |
| [bundle-tree-shaking.md][bundle-tree-shaking] | HIGH | Dead code elimination |
| [bundle-analyze-app.md][bundle-analyze-app] | HIGH | App size analysis |
| [bundle-r8-android.md][bundle-r8-android] | HIGH | Android code shrinking |
| [bundle-hermes-mmap.md][bundle-hermes-mmap] | HIGH | Disable bundle compression |
| [bundle-native-assets.md][bundle-native-assets] | HIGH | Asset catalog setup |
| [bundle-library-size.md][bundle-library-size] | MEDIUM | Evaluate dependencies |
| [bundle-code-splitting.md][bundle-code-splitting] | MEDIUM | Re.Pack code splitting |


## Searching References

```bash
# Find patterns by keyword
grep -l "reanimated" references/
grep -l "flatlist" references/
grep -l "memory" references/
grep -l "profil" references/
grep -l "tti" references/
grep -l "bundle" references/
```

## Problem → Skill Mapping

| Problem | Start With |
|---------|------------|
| App feels slow/janky | [js-measure-fps.md][js-measure-fps] → [js-profile-react.md][js-profile-react] |
| Too many re-renders | [js-profile-react.md][js-profile-react] → [js-react-compiler.md][js-react-compiler] |
| Slow startup (TTI) | [native-measure-tti.md][native-measure-tti] → [bundle-analyze-js.md][bundle-analyze-js] |
| Large app size | [bundle-analyze-app.md][bundle-analyze-app] → [bundle-r8-android.md][bundle-r8-android] |
| Memory growing | [js-memory-leaks.md][js-memory-leaks] or [native-memory-leaks.md][native-memory-leaks] |
| Animation drops frames | [js-animations-reanimated.md][js-animations-reanimated] |
| List scroll jank | [js-lists-flatlist-flashlist.md][js-lists-flatlist-flashlist] |
| TextInput lag | [js-uncontrolled-components.md][js-uncontrolled-components] |
| Native module slow | [native-turbo-modules.md][native-turbo-modules] → [native-threading-model.md][native-threading-model] |
| Native library alignment issue | [native-android-16kb-alignment.md][native-android-16kb-alignment] |

[references]: references/
[js-lists-flatlist-flashlist]: references/js-lists-flatlist-flashlist.md
[js-profile-react]: references/js-profile-react.md
[js-measure-fps]: references/js-measure-fps.md
[js-memory-leaks]: references/js-memory-leaks.md
[js-atomic-state]: references/js-atomic-state.md
[js-concurrent-react]: references/js-concurrent-react.md
[js-react-compiler]: references/js-react-compiler.md
[js-animations-reanimated]: references/js-animations-reanimated.md
[js-uncontrolled-components]: references/js-uncontrolled-components.md
[native-turbo-modules]: references/native-turbo-modules.md
[native-sdks-over-polyfills]: references/native-sdks-over-polyfills.md
[native-measure-tti]: references/native-measure-tti.md
[native-threading-model]: references/native-threading-model.md
[native-profiling]: references/native-profiling.md
[native-platform-setup]: references/native-platform-setup.md
[native-view-flattening]: references/native-view-flattening.md
[native-memory-patterns]: references/native-memory-patterns.md
[native-memory-leaks]: references/native-memory-leaks.md
[native-android-16kb-alignment]: references/native-android-16kb-alignment.md
[bundle-barrel-exports]: references/bundle-barrel-exports.md
[bundle-analyze-js]: references/bundle-analyze-js.md
[bundle-tree-shaking]: references/bundle-tree-shaking.md
[bundle-analyze-app]: references/bundle-analyze-app.md
[bundle-r8-android]: references/bundle-r8-android.md
[bundle-hermes-mmap]: references/bundle-hermes-mmap.md
[bundle-native-assets]: references/bundle-native-assets.md
[bundle-library-size]: references/bundle-library-size.md
[bundle-code-splitting]: references/bundle-code-splitting.md

## Attribution

Based on "The Ultimate Guide to React Native Optimization" by Callstack.

---

## Reference: Bundle Analyze App

# Skill: Analyze App Bundle Size

Measure iOS and Android app download/install sizes using Ruler, App Store Connect, and Emerge Tools.

## Quick Command

```bash
# Android (Ruler)
cd android && ./gradlew analyzeReleaseBundle

# iOS (Xcode export with thinning)
cd ios && xcodebuild -exportArchive \
  -archivePath MyApp.xcarchive \
  -exportPath ./export \
  -exportOptionsPlist ExportOptions.plist
# Check: App Thinning Size Report.txt
```

## When to Use

- App download size is too large
- Users complain about storage usage
- App approaching store limits
- Comparing releases for size regression

> **Note**: This skill involves interpreting visual size reports (Ruler, Emerge Tools X-Ray). AI agents cannot yet process screenshots autonomously. Use this as a guide while reviewing the reports manually, or await MCP-based visual feedback integration (see roadmap).

## Key Metrics

| Metric | Description | User Impact |
|--------|-------------|-------------|
| Download Size | Compressed, transferred over network | Download time, data usage |
| Install Size | Uncompressed, on device storage | Storage space |

**Google finding**: Every 6 MB increase reduces installs by 1%.

## Android: Ruler (Spotify)

### Setup

Add to `android/build.gradle`:

```groovy
buildscript {
    dependencies {
        classpath("com.spotify.ruler:ruler-gradle-plugin:2.0.0-beta-3")
    }
}
```

Add to `android/app/build.gradle`:

```groovy
apply plugin: "com.spotify.ruler"

ruler {
    abi.set("arm64-v8a")  // Target architecture
    locale.set("en")
    screenDensity.set(480)
    sdkVersion.set(34)
}
```

### Analyze

```bash
cd android
./gradlew analyzeReleaseBundle
```

Opens HTML report with:
- Download size
- Install size
- Component breakdown (biggest → smallest)

### CI Size Validation

```groovy
ruler {
    verification {
        downloadSizeThreshold = 20 * 1024 * 1024  // 20 MB
        installSizeThreshold = 50 * 1024 * 1024   // 50 MB
    }
}
```

Build fails if thresholds exceeded.

## iOS: Xcode App Thinning

### Via App Store Connect (Most Accurate)

After uploading to TestFlight:
1. Open App Store Connect
2. Go to your build
3. View size table by device variant

**Note**: TestFlight builds include debug data, App Store builds slightly larger due to DRM.

### Via Xcode Export

1. Archive app: **Product → Archive**
2. In Organizer, click **Distribute App**
3. Select **Custom**
4. Choose **App Thinning: All compatible device variants**

Or in `ExportOptions.plist`:

```xml
<key>thinning</key>
<string>&lt;thin-for-all-variants&gt;</string>
```

### Output

Creates folder with:
- **Universal IPA**: All variants combined
- **Thinned IPAs**: One per device variant
- **App Thinning Size Report.txt**:

```
Variant: SampleApp-<UUID>.ipa
App + On Demand Resources size: 3.5 MB compressed, 10.6 MB uncompressed
App size: 3.5 MB compressed, 10.6 MB uncompressed
```

- Compressed = Download size
- Uncompressed = Install size

## Emerge Tools (Cross-Platform)

Third-party service with visual analysis.

### Upload

Upload IPA, APK, or AAB through their web interface or CI integration.

### Features

<!-- image: Emerge Tools X-Ray for iOS -->

- **X-Ray**: Treemap visualization (like source-map-explorer for binaries)
  - Shows Frameworks (hermes.framework), Mach-O sections (TEXT, DATA), etc.
  - Color-coded: Binaries, Localizations, Fonts, Asset Catalogs, Videos, CoreML Models
  - Visible components: `main.jsbundle` (JS code), RCT modules, DYLD sections
- **Breakdown**: Component-by-component size
- **Insights**: Automated suggestions (use with caution)

**Caution**: Some suggestions may not apply to React Native (e.g., "remove Hermes").

## Size Comparison

| Tool | Platform | Accuracy | CI Integration |
|------|----------|----------|----------------|
| Ruler | Android | High | Yes (Gradle) |
| App Store Connect | iOS | Highest | No |
| Xcode Export | iOS | High | Yes (xcodebuild) |
| Emerge Tools | Both | High | Yes (API) |

## Typical React Native App Sizes

| Component | Approximate Size |
|-----------|------------------|
| Hermes engine | ~2-3 MB |
| React Native core | ~3-5 MB |
| JavaScript bundle | 1-10 MB |
| Assets (images, etc.) | Varies |

**Baseline empty app**: ~6-10 MB download

## Optimization Impact Example

| Optimization | Size Reduction |
|--------------|----------------|
| Enable R8 (Android) | ~30% |
| Remove unused polyfills | 400+ KB |
| Asset catalog (iOS) | 10-50% of assets |
| Tree shaking | 10-15% |

## Quick Commands

```bash
# Android release bundle size
cd android && ./gradlew bundleRelease
# Check: android/app/build/outputs/bundle/release/

# iOS archive
cd ios && xcodebuild -workspace ios/MyApp.xcworkspace \
  -scheme MyApp \
  -configuration Release \
  -archivePath MyApp.xcarchive \
  archive

# Export with thinning report
cd ios && xcodebuild -exportArchive \
  -archivePath MyApp.xcarchive \
  -exportPath ./export \
  -exportOptionsPlist ExportOptions.plist
```

## Related Skills

- [bundle-r8-android.md](./bundle-r8-android.md) - Reduce Android size
- [bundle-native-assets.md](./bundle-native-assets.md) - Optimize asset delivery
- [bundle-analyze-js.md](./bundle-analyze-js.md) - JS bundle analysis

---

## Reference: Bundle Analyze Js

# Skill: Analyze JS Bundle Size

Use source-map-explorer and Expo Atlas to visualize what's in your JavaScript bundle.

## Quick Command

```bash
# React Native CLI
npx react-native bundle \
  --entry-file index.js \
  --bundle-output output.js \
  --platform ios \
  --sourcemap-output output.js.map \
  --dev false --minify true && \
npx source-map-explorer output.js --no-border-checks

# Expo
EXPO_UNSTABLE_ATLAS=true npx expo export --platform ios && npx expo-atlas
```

## When to Use

- JS bundle seems too large
- Want to identify heavy dependencies
- Investigating startup time issues
- Before/after optimization comparison

> **Note**: This skill involves interpreting visual treemap output (source-map-explorer, Expo Atlas). AI agents cannot yet process screenshots autonomously. Use this as a guide while reviewing the visualization manually, or await MCP-based visual feedback integration (see roadmap).

## Understanding Hermes Bytecode

Modern React Native (0.70+) uses Hermes bytecode, not raw JavaScript:
- Skips parsing at runtime
- Still benefits from smaller bundles
- Heavy imports still execute on startup

**Impact of bundle size:**
- Larger bytecode = longer download from store
- More imports on init path = slower TTI

## Method 1: source-map-explorer

### Generate Bundle with Source Map

**React Native CLI:**

```bash
npx react-native bundle \
  --entry-file index.js \
  --bundle-output output.js \
  --platform ios \
  --sourcemap-output output.js.map \
  --dev false \
  --minify true
```

**Expo (SDK 51+):**

```bash
npx expo export --platform ios --source-maps --output-dir dist
# Bundle at: dist/ios/_expo/static/js/ios/*.js
# Source map at: dist/ios/_expo/static/js/ios/*.map
```

### Analyze

```bash
npx source-map-explorer output.js --no-border-checks
```

**Note**: `--no-border-checks` needed due to Metro's non-standard source maps.

Opens browser with treemap visualization:

<!-- image: Bundle Treemap from source-map-explorer -->

The treemap shows:
- **Hierarchy**: `node_modules/` → `react-native/` → `Libraries/` → individual files
- **Size**: Box area proportional to file size (KB shown in labels)
- **Major components visible**: 
  - `react-native` (724.18 KB, 80.5%)
  - `Renderer` (208.44 KB) - ReactNativeRenderer-prod.js, ReactFabric-prod.js
  - `Components` (125.29 KB) - Touchable, ScrollView, etc.
  - `Animated` (79.48 KB) - Animation system
  - `virtualized-lists` (57.57 KB) - FlatList internals

Click on any section to drill down into that directory.

**Limitation**: May lose ~30% info due to mapping issues.

## Method 2: Expo Atlas

More accurate for Expo projects (or with workaround for bare RN).

### For Expo Projects

```bash
# Start with Atlas enabled
EXPO_UNSTABLE_ATLAS=true npx expo start --no-dev

# Or export
EXPO_UNSTABLE_ATLAS=true npx expo export
```

Then launch UI:

```bash
npx expo-atlas
```

<!-- image: Expo Atlas Treemap -->

Expo Atlas provides more accurate visualization for Expo projects, with similar treemap interface showing module sizes and dependencies.

### For Non-Expo Projects

Use `expo-atlas-without-expo` package.

## Method 3: Re.Pack Bundle Analysis (Webpack/Rspack)

If using Re.Pack:

### webpack-bundle-analyzer

```bash
rspack build --analyze
```

### bundle-stats / statoscope

```bash
# Generate stats
npx react-native bundle \
  --platform android \
  --entry-file index.js \
  --dev false \
  --minify true \
  --json stats.json

# Analyze
npx bundle-stats --html --json stats.json
```

### Rsdoctor

```javascript
// rspack.config.js
const { RsdoctorRspackPlugin } = require('@rsdoctor/rspack-plugin');

module.exports = {
  plugins: [
    process.env.RSDOCTOR && new RsdoctorRspackPlugin(),
  ].filter(Boolean),
};
```

Run with:

```bash
RSDOCTOR=true npx react-native start
```

## What to Look For

### Red Flags

| Finding | Problem | Solution |
|---------|---------|----------|
| Entire library imported | Barrel exports | Use direct imports |
| Duplicate packages | Multiple versions | Dedupe in package.json |
| Dev dependencies in bundle | Incorrect imports | Check conditional imports |
| Large polyfills | Unnecessary for Hermes | Remove (see native-sdks-over-polyfills.md) |
| Moment.js with locales | Bloated date library | Switch to date-fns or dayjs |

### Common Offenders

- **Lodash full import**: Use `lodash-es` or specific imports
- **Moment.js**: Replace with `date-fns` or `dayjs`
- **Intl polyfills**: Check Hermes support
- **AWS SDK**: Import specific services only

## Code Examples

### Identify Barrel Import Impact

```tsx
// BAD: Imports entire library through barrel
import { format } from 'date-fns';

// In bundle: All of date-fns loaded

// GOOD: Direct import
import format from 'date-fns/format';

// In bundle: Only format function
```

## Comparing Bundles

### source-map-explorer

```bash
# Generate baseline
npx react-native bundle ... --bundle-output baseline.js --sourcemap-output baseline.js.map

# Make changes, generate new bundle
npx react-native bundle ... --bundle-output current.js --sourcemap-output current.js.map

# Compare manually in browser
```

### Re.Pack (automated)

```bash
npx bundle-stats compare baseline-stats.json current-stats.json
```

## Quick Commands

**React Native CLI:**

```bash
# iOS bundle analysis
npx react-native bundle \
  --entry-file index.js \
  --bundle-output ios-bundle.js \
  --platform ios \
  --sourcemap-output ios-bundle.js.map \
  --dev false \
  --minify true && \
npx source-map-explorer ios-bundle.js --no-border-checks

# Android bundle analysis  
npx react-native bundle \
  --entry-file index.js \
  --bundle-output android-bundle.js \
  --platform android \
  --sourcemap-output android-bundle.js.map \
  --dev false \
  --minify true && \
npx source-map-explorer android-bundle.js --no-border-checks
```

**Expo:**

```bash
# Use Expo Atlas (recommended for Expo projects)
EXPO_UNSTABLE_ATLAS=true npx expo export --platform ios
npx expo-atlas
```

## Related Skills

- [bundle-barrel-exports.md](./bundle-barrel-exports.md) - Fix barrel import issues
- [bundle-tree-shaking.md](./bundle-tree-shaking.md) - Enable dead code elimination
- [bundle-library-size.md](./bundle-library-size.md) - Check library sizes before adding

---

## Reference: Bundle Barrel Exports

# Skill: Avoid Barrel Exports

Refactor barrel imports (index files) to reduce bundle size and improve startup time.

## Quick Pattern

**Incorrect:**

```tsx
import { Button } from './components';
// Loads ALL exports from components/index.ts
```

**Correct:**

```tsx
import Button from './components/Button';
// Loads only Button
```

## When to Use

- Bundle contains unused code from libraries
- Circular dependency warnings in Metro
- Hot Module Replacement (HMR) breaks frequently
- TTI is slow due to module evaluation

## What Are Barrel Exports?

```tsx
// components/index.ts (barrel file)
export { Button } from './Button';
export { Card } from './Card';
export { Modal } from './Modal';
export { Sidebar } from './Sidebar';

// Usage (barrel import)
import { Button } from './components';
```

## Problems with Barrel Imports

### 1. Bundle Size Overhead

Metro includes **all exports** even if you use one:

```tsx
// Only need Button, but entire barrel is bundled
import { Button } from './components';
// Card, Modal, Sidebar also included!
```

### 2. Runtime Overhead

All modules evaluate before returning your import:

```tsx
import { Button } from './components';
// JavaScript must evaluate:
// - Button.tsx
// - Card.tsx
// - Modal.tsx  
// - Sidebar.tsx
// Even though you only use Button
```

### 3. Circular Dependencies

Barrel files make cycles easier to create accidentally:

```
Warning: Require cycle:
  components/index.ts -> Button.tsx -> utils/index.ts -> components/index.ts
```

Breaks HMR, causes unpredictable behavior.

## Solution 1: Direct Imports

Replace barrel imports with direct paths:

```tsx
// BEFORE: Barrel import
import { Button, Card } from './components';

// AFTER: Direct imports
import Button from './components/Button';
import Card from './components/Card';
```

### Enforce with ESLint

```bash
npm install -D eslint-plugin-no-barrel-files
```

```javascript
// eslint.config.js
import noBarrelFiles from 'eslint-plugin-no-barrel-files';

export default [
  {
    plugins: { 'no-barrel-files': noBarrelFiles },
    rules: {
      'no-barrel-files/no-barrel-files': 'error',
    },
  },
];
```

## Solution 2: Tree Shaking (Automatic)

Enable tree shaking to automatically remove unused barrel exports.

### Expo SDK 52+

```tsx
// metro.config.js
const { getDefaultConfig } = require('expo/metro-config');
const config = getDefaultConfig(__dirname);

config.transformer.getTransformOptions = async () => ({
  transform: {
    experimentalImportSupport: true,
  },
});

module.exports = config;
```

```bash
# .env
EXPO_UNSTABLE_METRO_OPTIMIZE_GRAPH=1
EXPO_UNSTABLE_TREE_SHAKING=1
```

### metro-serializer-esbuild

```bash
npm install @rnx-kit/metro-serializer-esbuild
```

### Re.Pack (Webpack/Rspack)

Tree shaking built-in.

## Real-World Example: date-fns

```tsx
// BAD: Imports entire library
import { format, addDays, isToday } from 'date-fns';

// GOOD: Direct imports
import format from 'date-fns/format';
import addDays from 'date-fns/addDays';
import isToday from 'date-fns/isToday';
```

## Library-Specific Solutions

Some libraries provide Babel plugins:

### React Native Paper

```javascript
// babel.config.js
module.exports = {
  plugins: [
    'react-native-paper/babel',  // Auto-transforms imports
  ],
};
```

Transforms:
```tsx
import { Button } from 'react-native-paper';
// Into:
import Button from 'react-native-paper/lib/module/components/Button';
```

## Refactoring Strategy

### Step 1: Identify Barrel Files

Look for `index.ts` files with multiple exports:

```bash
grep -r "export \* from" src/
grep -r "export { .* } from" src/
```

### Step 2: Update Imports

```tsx
// Find all usages
// VS Code: Cmd+Shift+F for "from './components'"

// Replace each with direct import
import Button from './components/Button';
```

### Step 3: (Optional) Keep Barrel for External API

If your package is consumed by others:

```tsx
// Keep index.ts for package API
// components/index.ts
export { Button } from './Button';

// Internal code uses direct imports
// src/screens/Home.tsx
import Button from '../components/Button';
```

## Migration Script Example

```bash
# Use codemod or search-replace
# Find: import { (\w+) } from '\.\/components';
# Replace: import $1 from './components/$1';
```

## Verification

After refactoring:

1. Run bundle analysis (see [bundle-analyze-js.md](./bundle-analyze-js.md))
2. Compare sizes before/after
3. Check for circular dependency warnings

## Common Pitfalls

- **Breaking external consumers**: If publishing a library, keep barrel for public API
- **IDE auto-imports**: Configure IDE to prefer direct imports
- **Inconsistent patterns**: Enforce with ESLint across team

## Related Skills

- [bundle-analyze-js.md](./bundle-analyze-js.md) - Verify impact
- [bundle-tree-shaking.md](./bundle-tree-shaking.md) - Automatic solution
- [bundle-library-size.md](./bundle-library-size.md) - Check library patterns

---

## Reference: Bundle Code Splitting

# Skill: Remote Code Loading

Set up code splitting with Re.Pack for on-demand bundle loading from trusted, first-party assets.

## Quick Pattern

**Before (static import):**

```jsx
import SettingsScreen from './screens/SettingsScreen';
```

**After (lazy loaded chunk):**

```jsx
const SettingsScreen = React.lazy(() =>
  import(/* webpackChunkName: "settings" */ './screens/SettingsScreen')
);

<Suspense fallback={<Loading />}>
  <SettingsScreen />
</Suspense>
```

## When to Use

Consider code splitting when:
- **Not using Hermes** (JSC/V8 benefits more)
- App size exceeds 200 MB (Play Store limit)
- Building micro-frontend architecture
- Loading features based on user permissions
- Other optimizations exhausted

**Note**: Hermes already uses memory mapping for efficient bundle reading. Benefits of code splitting are minimal with Hermes or even counterproductive in some cases.

## Security Model

Remote chunks are executable application code. Only load chunks that you build and publish yourself.

Keep these guardrails in place:
- Serve chunks only from a first-party, HTTPS-only origin you control
- Resolve `scriptId` through a fixed allowlist or release manifest
- Fail closed if a chunk is missing or unexpected
- Do not load chunks from user-controlled input, query params, or third-party domains

## Prerequisites

- Re.Pack installed (replaces Metro)

```bash
npx @callstack/repack-init
```

## Step-by-Step Instructions

### 1. Initialize Re.Pack

```bash
npx @callstack/repack-init
```

Follow prompts to migrate from Metro. Check [migration guide](https://re-pack.dev/docs/getting-started/quick-start).

### 2. Create Split Point with React.lazy

```tsx
// BEFORE: Static import
import SettingsScreen from './screens/SettingsScreen';

// AFTER: Dynamic import (creates split point)
const SettingsScreen = React.lazy(() =>
  import(/* webpackChunkName: "settings" */ './screens/SettingsScreen')
);
```

### 3. Wrap with Suspense

```tsx
import React, { Suspense } from 'react';

const App = () => {
  return (
    <Suspense fallback={<LoadingSpinner />}>
      <SettingsScreen />
    </Suspense>
  );
};
```

### 4. Configure Chunk Loading

```jsx
// index.js (before AppRegistry)
import { ScriptManager, Script } from '@callstack/repack/client';

const CHUNK_URLS = {
  settings: 'https://assets.example.com/app/v42/settings.chunk.bundle',
};

ScriptManager.shared.addResolver((scriptId) => ({
  url: __DEV__ ? Script.getDevServerURL(scriptId) : getChunkUrl(scriptId),
}));

function getChunkUrl(scriptId) {
  const url = CHUNK_URLS[scriptId];

  if (!url) {
    throw new Error(`Unknown chunk: ${scriptId}`);
  }

  return url;
}

AppRegistry.registerComponent(appName, () => App);
```

### 5. Build and Deploy Chunks

Build generates:
- `index.bundle` - Main bundle
- `settings.chunk.bundle` - Lazy-loaded chunk

Deploy chunks to a first-party CDN with versioned paths, and keep the allowlist or manifest in sync with the app release.

## Complete Example

```tsx
// App.tsx
import React, { Suspense, useState } from 'react';
import { Button, View, ActivityIndicator } from 'react-native';

// Lazy load heavy feature
const HeavyFeature = React.lazy(() =>
  import(/* webpackChunkName: "heavy-feature" */ './HeavyFeature')
);

const App = () => {
  const [showFeature, setShowFeature] = useState(false);
  
  return (
    <View>
      <Button 
        title="Load Feature" 
        onPress={() => setShowFeature(true)} 
      />
      
      {showFeature && (
        <Suspense fallback={<ActivityIndicator />}>
          <HeavyFeature />
        </Suspense>
      )}
    </View>
  );
};
```

## Module Federation (Advanced)

For micro-frontend architecture:

```tsx
// Host app loads remote module
const RemoteModule = React.lazy(() =>
  import('remote-app/Module')
);
```

Enables:
- Independent team deployments
- Shared dependencies
- Runtime composition

**Complexity warning**: Only use when organizational benefits outweigh overhead. Federation increases the trust boundary, so keep the same first-party origin and allowlist rules as above.

### Version Management

Consider [Zephyr Cloud](https://zephyr-cloud.io/) for:
- Sub-second deployments
- Version management
- Re.Pack integration

## Caching Strategy

```tsx
ScriptManager.shared.addResolver((scriptId) => ({
  url: getChunkUrl(scriptId),
  cache: {
    // Enable caching
    enabled: true,
    // Cache location
    path: `${FileSystem.cacheDirectory}/chunks/`,
  },
}));
```

## When NOT to Use

| Scenario | Why Not |
|----------|---------|
| Using Hermes | mmap already efficient |
| Small app | Overhead not worth it |
| Simple navigation | Native navigation better |
| Quick iteration needed | Added complexity |

## Hermes Memory Mapping

Hermes reads bytecode lazily via mmap:
- Only loads executed code into memory
- No parse step needed
- Code splitting provides marginal benefit

## Verification

```tsx
// Check if chunk loaded correctly
ScriptManager.shared.on('loading', (scriptId) => {
  console.log(`Loading: ${scriptId}`);
});

ScriptManager.shared.on('loaded', (scriptId) => {
  console.log(`Loaded: ${scriptId}`);
});

ScriptManager.shared.on('error', (scriptId, error) => {
  console.error(`Failed: ${scriptId}`, error);
});
```

## Common Pitfalls

- **Forgetting Suspense**: Lazy components need fallback
- **Wrong CDN path**: Chunks 404 in production
- **No caching**: Re-downloads on every load
- **Too many chunks**: Network overhead exceeds savings
- **Untrusted chunk source**: Remote JS from third-party or user-controlled origins is equivalent to remote code execution

## Related Skills

- [bundle-tree-shaking.md](./bundle-tree-shaking.md) - Re.Pack tree shaking
- [bundle-analyze-js.md](./bundle-analyze-js.md) - Measure chunk sizes
- [native-measure-tti.md](./native-measure-tti.md) - Verify TTI impact

---

## Reference: Bundle Hermes Mmap

# Skill: Disable JS Bundle Compression

Disable Android JS bundle compression to enable Hermes memory mapping for faster startup.

## Quick Config

```groovy
// android/app/build.gradle
android {
    androidResources {
        noCompress += ["bundle"]
    }
}
```

**Note**: Default in React Native 0.79+. Only needed for 0.78 and earlier.

## When to Use

- Android app using Hermes
- Want faster TTI (Time to Interactive)
- Willing to trade install size for startup speed
- React Native version is 0.78 or earlier, skip otherwise (see applicability)

## Background

Android compresses most files in APK/AAB by default, including `index.android.bundle`.

**Problem**: Compressed files can't be memory-mapped (mmap).

**Impact**: Hermes must decompress before reading, losing one of its key optimizations.

## How Hermes Memory Mapping Works

Without compression:
1. Hermes opens bytecode file
2. OS memory-maps directly to disk
3. Only pages actually accessed are loaded
4. **Result**: Fast startup, low memory

With compression:
1. Android decompresses entire bundle
2. Loaded into memory
3. Then Hermes processes
4. **Result**: Slower startup, higher memory

## Step-by-Step Implementation

### Edit build.gradle

In `android/app/build.gradle`:

```groovy
android {
    androidResources {
        noCompress += ["bundle"]
    }
}
```

### Full Context

```groovy
android {
    namespace "com.myapp"
    defaultConfig {
        applicationId "com.myapp"
        // ...
    }
    
    androidResources {
        noCompress += ["bundle"]
    }
    
    buildTypes {
        release {
            minifyEnabled true
            // ...
        }
    }
}
```

### Rebuild

```bash
cd android
./gradlew clean
./gradlew bundleRelease
# or
./gradlew assembleRelease
```

## Trade-offs

| Metric | Without Change | With Change |
|--------|----------------|-------------|
| Download size | Same | Same |
| Install size | Smaller | **+8% larger** |
| TTI | Slower | **-16% faster** |

**Real example**: 75.9 MB install → 82 MB install, but 450ms faster startup.

## Applicability

**React Native 0.78 and earlier**: Apply this optimization manually.

**React Native 0.79+**: Skip this—bundle compression is disabled by default.

## Verification

### Check APK Contents

```bash
# Unzip APK
unzip app-release.apk -d apk-contents

# Check if bundle is compressed
file apk-contents/assets/index.android.bundle
# Should show: "data" (not "gzip compressed")
```

### Measure TTI Impact

Use performance markers (see [native-measure-tti.md](./native-measure-tti.md)) to compare before/after.

## Multiple File Types

If you have other files that benefit from mmap:

```groovy
androidResources {
    noCompress += ["bundle", "hbc", "data"]
}
```

## Common Pitfalls

- **Not rebuilding**: Change requires clean build
- **Wrong config location**: Must be in `android` block
- **Ignoring size increase**: Monitor user feedback on install size
- **Already default**: Check if React Native version includes this

## Expo Notes

For Expo projects, run `npx expo prebuild` first to generate `android/` folder, then apply the `build.gradle` changes. Add `android/` to version control or use a [config plugin](https://docs.expo.dev/config-plugins/introduction/) for persistent changes.

## Should You Enable This?

| Scenario | Recommendation |
|----------|---------------|
| Startup-critical app | ✅ Enable |
| Storage-sensitive users | ⚠️ Test impact |
| Already fast TTI | Maybe not worth it |
| Large JS bundle | ✅ Bigger benefit |

## Related Skills

- [native-measure-tti.md](./native-measure-tti.md) - Measure TTI improvement
- [bundle-analyze-app.md](./bundle-analyze-app.md) - Check size impact
- [bundle-r8-android.md](./bundle-r8-android.md) - Offset size increase

---

## Reference: Bundle Library Size

# Skill: Determine Library Size

Evaluate third-party library size impact before adding to your project.

## Quick Command

```bash
# Check size before installing
# Visit: https://bundlephobia.com/package/[package-name]

# Or use CLI
npx bundle-phobia-cli <package-name>
```

## When to Use

- Evaluating new dependencies
- Comparing alternative libraries
- Auditing existing dependencies
- Investigating bundle bloat

## Tools Overview

| Tool | Type | Best For |
|------|------|----------|
| bundlephobia.com | Web | Quick size check |
| pkg-size.dev | Web | Backup/alternative |
| Import Cost (VS Code) | IDE extension | Real-time feedback |

## bundlephobia.com

### Usage

Visit [bundlephobia.com](https://bundlephobia.com) and enter package name.

### Shows

- **Minified size**: Raw JS size
- **Minified + Gzipped**: Network transfer size
- **Download time**: Estimated on various connections
- **Dependencies**: What else gets pulled in
- **Composition**: Breakdown by dependency

### Example Analysis

```
react-native-paper
├── Minified: 312 kB
├── Gzipped: 78 kB
└── Dependencies: 12 packages
    ├── @callstack/react-theme-provider
    ├── color
    └── ...
```

## pkg-size.dev

Backup when bundlephobia fails.

Visit [pkg-size.dev](https://pkg-size.dev) with package name.

**Difference**: Actually installs package in web container, may be more accurate for edge cases.

## Import Cost (VS Code Extension)

### Install

Search "Import Cost" in VS Code extensions or:

```bash
code --install-extension wix.vscode-import-cost
```

### Usage

Shows inline size next to imports:

```tsx
import React from 'react';           // 6.5K (gzipped)
import { View, Text } from 'react-native';  // 0B (native)
import lodash from 'lodash';         // 71.5K (gzipped: 24.7K)
import get from 'lodash/get';        // 8K (gzipped: 2.9K)
```

### Limitations

- Uses Webpack internally (not Metro)
- May fail on React Native-specific packages
- Doesn't account for tree shaking

## Comparison Workflow

### Before Adding Dependency

1. Check on bundlephobia:
   ```
   https://bundlephobia.com/package/[package-name]
   ```

2. Compare alternatives:
   ```
   moment (289 kB) vs date-fns (75 kB) vs dayjs (6 kB)
   ```

3. Check what you actually need:
   - Full library import vs specific functions
   - Native alternative available?

### After Adding

1. Analyze bundle (see [bundle-analyze-js.md](./bundle-analyze-js.md))
2. Verify actual impact matches expected
3. Check for duplicate dependencies

## Size Guidelines

| Size (gzipped) | Assessment | Action |
|----------------|------------|--------|
| < 5 KB | Small | Generally fine |
| 5-20 KB | Medium | Evaluate necessity |
| 20-50 KB | Large | Look for alternatives |
| > 50 KB | Very large | Strong justification needed |

## Common Large Dependencies

| Library | Size (gzipped) | Alternative |
|---------|----------------|-------------|
| moment | ~70 KB | dayjs (~3 KB) |
| lodash (full) | ~25 KB | lodash-es + direct imports |
| aws-sdk (full) | 200+ KB | @aws-sdk/client-* |
| crypto-js | ~15 KB | react-native-quick-crypto |

## Quick Size Check Script

```bash
# Check size before installing
npx bundle-phobia-cli <package-name>

# Or use npm directly (less accurate)
npm pack <package-name> --dry-run 2>&1 | grep "total files"
```

## Decision Matrix

| Factor | Keep JS Library | Use Native Alternative |
|--------|-----------------|------------------------|
| Size | > 50 KB | < 50 KB |
| Platform coverage | Both platforms | Single platform OK |
| Performance | Not critical | Critical path |
| Functionality | Simple | Complex computation |

## Code Example: Optimizing Imports

```tsx
// BAD: Full library (71.5 KB)
import _ from 'lodash';
_.get(obj, 'path.to.value');

// BETTER: Specific import (8 KB)
import get from 'lodash/get';
get(obj, 'path.to.value');

// BEST: Native JS (0 KB)
obj?.path?.to?.value;
```

## Related Skills

- [bundle-analyze-js.md](./bundle-analyze-js.md) - Verify actual bundle impact
- [bundle-barrel-exports.md](./bundle-barrel-exports.md) - Optimize how you import
- [native-sdks-over-polyfills.md](./native-sdks-over-polyfills.md) - Native alternatives to JS libs

---

## Reference: Bundle Native Assets

# Skill: Native Assets

Configure platform-specific asset delivery to reduce app download size.

## Quick Config

**iOS Asset Catalog (Build Phase):**

```bash
# Add to "Bundle React Native code and images" build phase
export EXTRA_PACKAGER_ARGS="--asset-catalog-dest ./"
```

**Android**: Automatic via AAB — Play Store delivers correct density per device.

## When to Use

- Images bloating app size
- Different device densities need different assets
- Want to leverage App Store/Play Store optimization
- Using high-resolution images

## Concept: Size Suffixes

React Native convention for multiple resolutions:

```
assets/
├── image.jpg       # 1x resolution (base)
├── image@2x.jpg    # 2x resolution
└── image@3x.jpg    # 3x resolution
```

```tsx
// React Native selects best one for device
<Image source={require('./assets/image.jpg')} />
```

## Android: Automatic Optimization

Android handles this automatically.

### How It Works

1. Build AAB:
   ```bash
   cd android && ./gradlew bundleRelease
   ```

2. Metro places images in density folders:
   ```
   android/app/build/outputs/bundle/release/
   └── base/
       └── res/
           ├── drawable-mdpi-v4/     # 1x
           ├── drawable-hdpi-v4/     # 1.5x
           ├── drawable-xhdpi-v4/    # 2x
           ├── drawable-xxhdpi-v4/   # 3x
           └── drawable-xxxhdpi-v4/  # 4x
   ```

3. Play Store delivers only needed density per device.

**No configuration required** for Android.

## iOS: Asset Catalog Setup

iOS requires explicit configuration.

### Step 1: Create Asset Catalog

Create folder in `ios/`:

```
ios/RNAssets.xcassets/
```

**Important**: Must be named exactly `RNAssets.xcassets` (hardcoded in React Native).

### Step 2: Configure Build Phase

In Xcode:
1. Open project settings
2. Go to **Build Phases**
3. Find **"Bundle React Native code and images"**
4. Add before line 8:

```bash
export EXTRA_PACKAGER_ARGS="--asset-catalog-dest ./"
```

### Step 3: Build

Run build to populate asset catalog:

```bash
npx react-native run-ios --mode Release
```

Or manually:

```bash
npx react-native bundle \
  --entry-file index.js \
  --bundle-output ios-bundle.js \
  --platform ios \
  --dev false \
  --asset-catalog-dest ios \
  --assets-dest ios/assets
```

### Step 4: Verify

After build, `RNAssets.xcassets` contains:

```
ios/RNAssets.xcassets/
└── assets_image_image.imageset/
    ├── Contents.json
    ├── image.jpg
    ├── image@2x.jpg
    └── image@3x.jpg
```

App Store then delivers only needed resolution.

## Before/After Comparison

### Without Asset Catalog (All Variants)

```
App bundle contains:
├── image.jpg       (100 KB)
├── image@2x.jpg    (300 KB)
└── image@3x.jpg    (600 KB)
Total: 1 MB
```

### With Asset Catalog (Device-Specific)

```
iPhone 15 Pro receives:
└── image@3x.jpg    (600 KB)
Total: 600 KB  (40% smaller)
```

## Asset Optimization Tips

### 1. Compress Images

Use tools before adding to project:

```bash
# ImageOptim (macOS)
# TinyPNG (web)
# sharp (programmatic)

npx sharp-cli input.jpg -o output.jpg --quality 80
```

### 2. Use Appropriate Formats

| Format | Best For |
|--------|----------|
| JPEG | Photos |
| PNG | Icons, transparency |
| WebP | Both (smaller) |
| SVG | Vector icons |

### 3. Consider react-native-fast-image

Caching and better image handling:

```bash
npm install react-native-fast-image
```

## Verification

### iOS App Thinning Report

After export, check `App Thinning Size Report.txt`:

```
Variant: MyApp-<UUID>.ipa
Supported variant descriptors: iPhone15,2 ...
App size: 3.5 MB compressed, 10.6 MB uncompressed
```

### Use Emerge Tools

Upload IPA to see asset breakdown.

## Common Pitfalls

- **Wrong folder name**: Must be `RNAssets.xcassets` exactly
- **Missing build phase config**: Assets not processed
- **Not using size suffixes**: All variants included anyway
- **Forgetting to rebuild**: Changes need fresh build

## Future Note

As of January 2025, Asset Catalog is not default. May become default in future React Native versions.

## Related Skills

- [bundle-analyze-app.md](./bundle-analyze-app.md) - Verify asset impact
- [bundle-r8-android.md](./bundle-r8-android.md) - Android code optimization

---

## Reference: Bundle R8 Android

# Skill: R8 Code Shrinking

Enable R8 for Android to shrink, optimize, and obfuscate native code.

## Quick Config

```groovy
// android/app/build.gradle
def enableProguardInReleaseBuilds = true

android {
    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true
        }
    }
}
```

## When to Use

- Android app size too large
- Want to obfuscate code for security
- Building release APK/AAB

## What is R8?

R8 replaces ProGuard in Android:
- **Shrinks**: Removes unused code
- **Optimizes**: Improves bytecode
- **Obfuscates**: Renames classes/methods

**Compatibility**: Uses ProGuard configuration format.

## Step-by-Step Instructions

### 1. Enable R8

Edit `android/app/build.gradle`:

```groovy
def enableProguardInReleaseBuilds = true
```

This sets `minifyEnabled = true` for release builds.

### 2. Enable Resource Shrinking (Optional)

Further reduces size by removing unused resources:

```groovy
android {
    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true  // Requires minifyEnabled
            
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

### 3. Configure ProGuard Rules (If Needed)

Edit `android/app/proguard-rules.pro`. React Native defaults are usually sufficient—only add rules when specific libraries break after enabling R8.

**Only add if using Firebase (`@react-native-firebase/*`):**

```proguard
-keep class io.invertase.firebase.** { *; }
-dontwarn io.invertase.firebase.**
```

**Only add if using Retrofit:**

```proguard
-keepattributes Signature
-keepattributes *Annotation*
-keep class retrofit2.** { *; }
-dontwarn retrofit2.**
```

See [Common Library Rules](#common-library-rules) and [Troubleshooting](#troubleshooting) for more examples.

### 4. Build and Test

```bash
cd android
./gradlew assembleRelease
# or
./gradlew bundleRelease
```

**Critical**: Test thoroughly! R8 can remove code it thinks is unused.

## ProGuard Rules Reference

| Rule | Effect |
|------|--------|
| `-keep class X` | Don't remove class X |
| `-keepclassmembers` | Keep members but allow rename |
| `-keepnames` | Keep names but allow removal if unused |
| `-dontwarn X` | Suppress warnings for X |
| `-dontobfuscate` | Disable obfuscation |

### Keep Entire Package

```proguard
-keep class com.mypackage.** { *; }
```

### Keep Classes with Annotation

```proguard
-keep @interface com.facebook.proguard.annotations.DoNotStrip
-keep @com.facebook.proguard.annotations.DoNotStrip class *
-keepclassmembers class * {
    @com.facebook.proguard.annotations.DoNotStrip *;
}
```

## Disable Obfuscation (If Needed)

```proguard
# proguard-rules.pro
-dontobfuscate
```

Use when:
- Debugging crashes (stack traces more readable)
- Library requires class names

## Size Impact

Example from guide:
- **Without R8**: 9.5 MB
- **With R8**: 6.3 MB
- **Savings**: 33%

Larger apps may see 20-30% reduction.

## Troubleshooting

### App Crashes After R8

Usually means needed class was removed.

**Debug steps**:

1. Check crash log for class name
2. Add keep rule:
   ```proguard
   -keep class com.example.CrashedClass { *; }
   ```
3. Rebuild and test

### Library Specific Rules

Many libraries provide ProGuard rules. Check:
- Library README
- Library's `consumer-proguard-rules.pro`
- Stack Overflow for library + proguard

### Common Library Rules

```proguard
# Hermes (usually auto-included)
-keep class com.facebook.hermes.unicode.** { *; }

# React Native
-keep class com.facebook.react.** { *; }

# Gson
-keepattributes Signature
-keep class com.google.gson.** { *; }

# OkHttp
-dontwarn okhttp3.**
-dontwarn okio.**
```

## Verification

### Check APK Size

```bash
# Build
./gradlew assembleRelease

# Check size
ls -la android/app/build/outputs/apk/release/
```

### Use Ruler for Detailed Analysis

See [bundle-analyze-app.md](./bundle-analyze-app.md).

### Verify Obfuscation

Decompile APK to check class names are obfuscated:

```bash
# Using jadx or similar
jadx android/app/build/outputs/apk/release/app-release.apk
```

## Common Pitfalls

- **Not testing release build**: Always QA with R8 enabled
- **Missing library rules**: Check library docs
- **Over-keeping**: Too many keep rules negates benefits
- **Reflection**: Code using reflection may break

## Related Skills

- [bundle-analyze-app.md](./bundle-analyze-app.md) - Measure size impact
- [bundle-native-assets.md](./bundle-native-assets.md) - Further size reduction

---

## Reference: Bundle Tree Shaking

# Skill: Tree Shaking

Enable dead code elimination to remove unused exports from your JavaScript bundle.

## Quick Config

```bash
# .env (Expo SDK 52+)
EXPO_UNSTABLE_METRO_OPTIMIZE_GRAPH=1
EXPO_UNSTABLE_TREE_SHAKING=1
```

```javascript
// metro.config.js
config.transformer.getTransformOptions = async () => ({
  transform: { experimentalImportSupport: true },
});
```

```javascript
// babel.config.js (non-Expo projects must set `disableImportExportTransform`)
module.exports = {
  presets: [
    [
      'module:@react-native/babel-preset',
      { disableImportExportTransform: true },
    ],
  ],
};
```

## When to Use

- Bundle includes unused library code
- Want automatic barrel export optimization
- Using Expo SDK 52+ (recommended approach)
- Project already uses Re.Pack (`@callstack/repack`)

## Platform Support

| Bundler        | Tree Shaking    | Notes                        |
| -------------- | --------------- | ---------------------------- |
| Metro          | ❌ No           | Use metro-serializer-esbuild |
| Expo (SDK 52+) | ✅ Experimental | Requires config              |
| Re.Pack        | ✅ Yes          | Built-in via Webpack/Rspack  |

## Setup: Expo SDK 52+

### 1. Enable Import Support

```javascript
// metro.config.js
const { getDefaultConfig } = require('expo/metro-config');

const config = getDefaultConfig(__dirname);

config.transformer.getTransformOptions = async () => ({
  transform: {
    experimentalImportSupport: true,
  },
});

module.exports = config;
```

### 2. Enable Tree Shaking

Create/edit `.env`:

```bash
EXPO_UNSTABLE_METRO_OPTIMIZE_GRAPH=1
EXPO_UNSTABLE_TREE_SHAKING=1
```

**Note**: Only applies in production builds.

## Setup: Metro with ESBuild

```bash
npm install @rnx-kit/metro-serializer-esbuild
```

Configure in metro.config.js.

## Setup: Re.Pack (Only If Already Installed)

> **Important**: Re.Pack (`@callstack/repack`) is a custom bundler using Rspack/Webpack. Only apply these instructions if the project already has Re.Pack configured. Do not suggest migrating a codebase to Re.Pack—it's rarely necessary and requires significant setup.

**If project has `@callstack/repack` in dependencies:**

Tree shaking is enabled by default with Rspack. Verify in config:

```javascript
// rspack.config.js or webpack.config.js
module.exports = {
  optimization: {
    usedExports: true, // Mark unused exports
    minimize: true, // Remove during minification
  },
};
```

## Platform Shaking

Code inside `Platform.OS` and `Platform.select` checks is removed for other platforms:

```tsx
// IMPORTANT: import Platform directly from 'react-native'
import { Platform } from 'react-native';

if (Platform.OS === 'ios') {
  // Removed from Android bundle
}

if (Platform.select({ ios: true, android: false }) === 'ios') {
  // Removed from Android bundle
}
```

**Critical**: Must use direct import. This does NOT work:

```tsx
import * as RN from 'react-native';
if (RN.Platform.OS === 'ios') {
  // NOT removed - optimization fails
}
```

For non-Expo projects, requires both `experimentalImportSupport: true` in Metro config and `disableImportExportTransform: true` in Babel config.

Impact: Savings from enabling platform shaking on a bare React Native Community CLI project are:
- 5% smaller Hermes bytecode (2.79 MB → 2.64 MB)
- 15% smaller minified JS bundle (1 MB → 0.85 MB)

## Requirements for Tree Shaking

### ESM Imports Required

```tsx
// ✅ ESM - Tree shakeable
import { foo } from './module';

// ❌ CommonJS - Not tree shakeable
const { foo } = require('./module');
```

### Side Effects Declaration

Libraries must declare side-effect-free in `package.json`:

```json
{
  "sideEffects": false
}
```

Or specify files with side effects:

```json
{
  "sideEffects": ["*.css", "./src/polyfills.js"]
}
```

## Size Impact

| Bundle Type       | Metro (MB) | Re.Pack (MB) | Change   |
| ----------------- | ---------- | ------------ | -------- |
| Production        | 35.63      | 38.48        | +8%      |
| Prod Minified     | 15.54      | 13.36        | **-14%** |
| Prod HBC          | 21.79      | 19.35        | **-11%** |
| Prod Minified HBC | 21.62      | 19.05        | **-12%** |

**Expected improvement**: 10-15% bundle size reduction.

## Verification

1. Build production bundle (see [bundle-analyze-js.md](./bundle-analyze-js.md))
2. Analyze with source-map-explorer (see [bundle-analyze-js.md](./bundle-analyze-js.md))
3. Search for functions you know are unused
4. If found → tree shaking not working

### Test Example

```tsx
// test-treeshake.js
export const usedFunction = () => 'used';
export const unusedFunction = () => 'unused'; // Should be removed

// app.js
import { usedFunction } from './test-treeshake';
```

After building, search bundle for `unusedFunction`. Should not exist.

## Common Pitfalls

- **Not using production build**: Tree shaking only in prod
- **CommonJS modules**: Need ESM for full effectiveness
- **Side effects not declared**: Library may not be shakeable
- **Dynamic imports**: `require(variable)` prevents analysis
- **Babel/Metro config mismatch**: `disableImportExportTransform` must match `experimentalImportSupport`

## Related Skills

- [bundle-analyze-js.md](./bundle-analyze-js.md) - Verify tree shaking effect
- [bundle-barrel-exports.md](./bundle-barrel-exports.md) - Manual alternative
- [bundle-code-splitting.md](./bundle-code-splitting.md) - Re.Pack code splitting

---

## Reference: Js Animations Reanimated

# Skill: High-Performance Animations

Use React Native Reanimated for smooth 60+ FPS animations.

## Quick Pattern

**Incorrect (JS thread - blocks on heavy work):**

```jsx
const opacity = useRef(new Animated.Value(0)).current;
Animated.timing(opacity, { toValue: 1 }).start();
```

**Correct (UI thread - smooth even during JS work):**

```jsx
const opacity = useSharedValue(0);
const style = useAnimatedStyle(() => ({ opacity: opacity.value }));
opacity.value = withTiming(1);
```

## When to Use

- Animations drop frames or feel janky
- UI freezes during animations
- Need gesture-driven animations
- Want animations to run during heavy JS work

## Prerequisites

- `react-native-reanimated` (v4+) and `react-native-worklets` installed

```bash
npm install react-native-reanimated react-native-worklets
```

Add to `babel.config.js`:

```javascript
module.exports = {
  plugins: ['react-native-worklets/plugin'],  // Must be last
};
```

> **Note**: Reanimated 4 requires React Native's **New Architecture** (Fabric + TurboModules). The Legacy Architecture is no longer supported. If upgrading from v3, see the migration notes at the end of this document.

## Key Concepts

### Main Thread vs JS Thread

- **Main/UI Thread**: Handles native rendering (60+ FPS target)
- **JS Thread**: Runs React and your JavaScript

**Problem**: Heavy JS work blocks animations running on JS thread.

**Solution**: Run animations on UI thread with Reanimated worklets.

## Step-by-Step Instructions

### 1. Basic Animated Style (UI Thread)

```jsx
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming
} from 'react-native-reanimated';

const FadeInView = () => {
  const opacity = useSharedValue(0);

  // This runs on UI thread - won't be blocked by JS
  const animatedStyle = useAnimatedStyle(() => {
    return { opacity: opacity.value };
  });

  useEffect(() => {
    opacity.value = withTiming(1, { duration: 500 });
  }, []);

  return <Animated.View style={[styles.box, animatedStyle]} />;
};
```

### 2. Run Code on UI Thread with `scheduleOnUI`

```jsx
import { scheduleOnUI } from 'react-native-worklets';

const triggerAnimation = () => {
  scheduleOnUI(() => {
    'worklet';
    console.log('Running on UI thread');
    // Direct UI manipulations here
  });
};
```

### 3. Call JS from UI Thread with `scheduleOnRN`

```jsx
import { scheduleOnRN } from 'react-native-worklets';

// Regular JS function
const trackAnalytics = (value) => {
  analytics.track('animation_complete', { value });
};

const AnimatedComponent = () => {
  const progress = useSharedValue(0);

  const animatedStyle = useAnimatedStyle(() => {
    // When animation completes, call JS function
    if (progress.value === 1) {
      scheduleOnRN(trackAnalytics, progress.value);
    }
    return { opacity: progress.value };
  });

  return <Animated.View style={animatedStyle} />;
};
```

### 4. Animation with Callback

```jsx
import { scheduleOnRN } from 'react-native-worklets';

const AnimatedButton = () => {
  const scale = useSharedValue(1);

  const onComplete = () => {
    console.log('Animation finished!');
  };

  const handlePress = () => {
    scale.value = withTiming(
      1.2,
      { duration: 200 },
      (finished) => {
        if (finished) {
          scheduleOnRN(onComplete);
        }
      }
    );
  };

  const animatedStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scale.value }],
  }));

  return (
    <Pressable onPress={handlePress}>
      <Animated.View style={[styles.button, animatedStyle]}>
        <Text>Press Me</Text>
      </Animated.View>
    </Pressable>
  );
};
```

## When to Use What

| Thread | Best For |
|--------|----------|
| **UI Thread** (worklets) | Visual animations, transforms, gestures |
| **JS Thread** | State updates, data processing, API calls |

| Hook/API | Use Case |
|----------|----------|
| `useAnimatedStyle` | Animated styles (auto UI thread) |
| `scheduleOnUI` | Manual UI thread execution (from `react-native-worklets`) |
| `scheduleOnRN` | Call JS functions from worklets (from `react-native-worklets`) |
| `useTransition` | Alternative for React state-driven delays |

## Common Pitfalls

- **Accessing React state in worklets**: Use `useSharedValue` instead of `useState` for animated values
- **Not using Animated components**: Must use `Animated.View`, `Animated.Text`, etc.
- **Heavy computation in useAnimatedStyle**: Keep worklets fast
- **Forgetting 'worklet' directive**: Required for inline worklet functions

```jsx
// BAD: Regular function in useAnimatedStyle
const style = useAnimatedStyle(() => {
  heavyComputation();  // Blocks UI thread!
  return { opacity: 1 };
});

// GOOD: Keep worklets fast
const style = useAnimatedStyle(() => {
  return { opacity: opacity.value };  // Just read value
});
```

## Migrating from Reanimated 3.x to 4.x

If you're upgrading from Reanimated 3.x, here are the key changes.

> **Can't upgrade to v4?** If your project is blocked from migrating to New Architecture (e.g., incompatible native libraries, complex native code, or timeline constraints), keep using existing APIs and leverage native drivers where applicable. Avoid introducing legacy Reanimated 3.x or older to reduce future migration complexity.

### Breaking Changes

| Old API (v3) | New API (v4) | Package |
|--------------|--------------|---------|
| `runOnUI(() => {...})()` | `scheduleOnUI(() => {...})` | `react-native-worklets` |
| `runOnJS(fn)(args)` | `scheduleOnRN(fn, args)` | `react-native-worklets` |
| `executeOnUIRuntimeSync` | `runOnUISync` | `react-native-worklets` |
| `runOnRuntime` | `scheduleOnRuntime` | `react-native-worklets` |
| `useScrollViewOffset` | `useScrollOffset` | `react-native-reanimated` |
| `useWorkletCallback` | Use `useCallback` with `'worklet';` directive | React |

### Removed APIs

- `useAnimatedGestureHandler` - Migrate to the Gesture API from `react-native-gesture-handler` v2+
- `addWhitelistedNativeProps` / `addWhitelistedUIProps` - No longer needed
- `combineTransition` - Use `EntryExitTransition.entering(...).exiting(...)` instead

### withSpring Changes

```jsx
// Before (v3)
withSpring(value, {
  restDisplacementThreshold: 0.01,
  restSpeedThreshold: 0.01,
  duration: 300,
});

// After (v4)
withSpring(value, {
  energyThreshold: 0.01,  // Replaces both threshold parameters
  duration: 200,          // Duration is now "perceptual" (~1.5x actual time)
});
```

### Migration Checklist

1. **Enable New Architecture** - Reanimated 4 only supports Fabric + TurboModules
2. **Install `react-native-worklets`** - Required new dependency
3. **Update Babel plugin** - Change `'react-native-reanimated/plugin'` to `'react-native-worklets/plugin'`
4. **Update imports** - Move worklet functions to `react-native-worklets`
5. **Update API calls** - New functions take callback + args directly (not curried)
6. **Rebuild native apps** - Required after adding `react-native-worklets`

## Related Skills

- [js-measure-fps.md](./js-measure-fps.md) - Verify animation frame rate
- [js-concurrent-react.md](./js-concurrent-react.md) - React-level deferral with useTransition

---

## Reference: Js Atomic State

# Skill: Atomic State Management

Use atomic state libraries (Jotai, Zustand) to reduce unnecessary re-renders without manual memoization.

## Quick Pattern

**Before (Context - all consumers re-render):**

```jsx
const { filter, todos } = useContext(TodoContext);
// Re-renders when ANY state changes
```

**After (Zustand - only subscribed state):**

```jsx
const filter = useTodoStore((s) => s.filter);
// Only re-renders when filter changes
```

## When to Use

- Global state changes cause widespread re-renders
- Using React Context for app state
- Components re-render even when their data hasn't changed
- Want to avoid manual `useMemo`/`useCallback` everywhere
- Not ready to adopt React Compiler

## Prerequisites

- State management library: `jotai` or `zustand`

```bash
npm install jotai
# or
npm install zustand
```

## Problem Description

With traditional React state or Context:

```jsx
// When filter OR todos change, EVERYTHING re-renders
const App = () => {
  const [filter, setFilter] = useState('all');
  const [todos, setTodos] = useState([]);
  
  return (
    <>
      <FilterMenu filter={filter} setFilter={setFilter} />
      <TodoList todos={todos} filter={filter} setTodos={setTodos} />
    </>
  );
};
```

Changing a todo re-renders FilterMenu even though it doesn't use todos.

## Step-by-Step Instructions

### Using Jotai

#### 1. Define Atoms

```jsx
import { atom } from 'jotai';

// Each atom is an independent piece of state
const filterAtom = atom('all');
const todosAtom = atom([]);

// Derived atom (computed value)
const filteredTodosAtom = atom((get) => {
  const filter = get(filterAtom);
  const todos = get(todosAtom);
  
  if (filter === 'active') return todos.filter(t => !t.completed);
  if (filter === 'completed') return todos.filter(t => t.completed);
  return todos;
});
```

#### 2. Use Atoms in Components

```jsx
import { useAtom, useAtomValue, useSetAtom } from 'jotai';

// Only re-renders when filterAtom changes
const FilterMenu = () => {
  const [filter, setFilter] = useAtom(filterAtom);
  
  return (
    <View>
      {['all', 'active', 'completed'].map((f) => (
        <Pressable key={f} onPress={() => setFilter(f)}>
          <Text style={filter === f ? styles.active : null}>{f}</Text>
        </Pressable>
      ))}
    </View>
  );
};

// Only re-renders when todosAtom changes
const TodoItem = ({ id }) => {
  const setTodos = useSetAtom(todosAtom);  // Only setter, no re-render on read
  
  const toggleTodo = () => {
    setTodos((prev) => 
      prev.map((t) => t.id === id ? { ...t, completed: !t.completed } : t)
    );
  };
  
  return <Pressable onPress={toggleTodo}>...</Pressable>;
};
```

### Using Zustand

#### 1. Create Store

```jsx
import { create } from 'zustand';

const useTodoStore = create((set, get) => ({
  filter: 'all',
  todos: [],
  
  setFilter: (filter) => set({ filter }),
  
  toggleTodo: (id) => set((state) => ({
    todos: state.todos.map((t) =>
      t.id === id ? { ...t, completed: !t.completed } : t
    ),
  })),
  
  // Selector for derived state
  getFilteredTodos: () => {
    const { filter, todos } = get();
    if (filter === 'active') return todos.filter(t => !t.completed);
    if (filter === 'completed') return todos.filter(t => t.completed);
    return todos;
  },
}));
```

#### 2. Use Selectors

```jsx
// Only re-renders when filter changes
const FilterMenu = () => {
  const filter = useTodoStore((state) => state.filter);
  const setFilter = useTodoStore((state) => state.setFilter);
  
  return (
    <View>
      {['all', 'active', 'completed'].map((f) => (
        <Pressable key={f} onPress={() => setFilter(f)}>
          <Text>{f}</Text>
        </Pressable>
      ))}
    </View>
  );
};

// Only re-renders when todos change
const TodoList = () => {
  const todos = useTodoStore((state) => state.todos);
  return todos.map((todo) => <TodoItem key={todo.id} {...todo} />);
};
```

## Code Examples

### Before: Context-Based (Many Re-renders)

```jsx
const TodoContext = createContext();

const TodoProvider = ({ children }) => {
  const [state, setState] = useState({ filter: 'all', todos: [] });
  return (
    <TodoContext.Provider value={{ state, setState }}>
      {children}
    </TodoContext.Provider>
  );
};

// Every component using this context re-renders on ANY state change
const FilterMenu = () => {
  const { state, setState } = useContext(TodoContext);
  // Re-renders when todos change too!
};
```

### After: Atomic (Targeted Re-renders)

```jsx
// Jotai version - only affected components re-render
const filterAtom = atom('all');
const todosAtom = atom([]);

const FilterMenu = () => {
  const [filter, setFilter] = useAtom(filterAtom);
  // Only re-renders when filter changes
};

const TodoList = () => {
  const todos = useAtomValue(todosAtom);
  // Only re-renders when todos change
};
```

## Comparison

| Feature | Context | Jotai | Zustand |
|---------|---------|-------|---------|
| Re-render scope | All consumers | Atom subscribers | Selector subscribers |
| Derived state | Manual | Built-in atoms | Selectors |
| DevTools | React DevTools | Jotai DevTools | Zustand DevTools |
| Bundle size | 0 KB | ~3 KB | ~2 KB |
| Learning curve | Low | Medium | Low |

## When to Use Which

- **Jotai**: Fine-grained state, many small atoms, derived/async atoms
- **Zustand**: Simpler mental model, single store, familiar Redux-like pattern
- **React Compiler**: If available, may eliminate need for these libraries

## Common Pitfalls

- **Over-atomizing**: Don't create an atom for every variable. Group related state.
- **Missing selectors in Zustand**: Always use selectors to prevent unnecessary re-renders.
- **Derived state without memoization**: Use derived atoms (Jotai) or memoized selectors.

## Related Skills

- [js-react-compiler.md](./js-react-compiler.md) - Automatic memoization alternative
- [js-profile-react.md](./js-profile-react.md) - Verify re-render reduction

---

## Reference: Js Concurrent React

# Skill: Concurrent React

Use `useDeferredValue` and `useTransition` to improve perceived performance by prioritizing critical updates.

## Quick Pattern

**Incorrect (blocks input on every keystroke):**

```jsx
const [query, setQuery] = useState('');
<TextInput value={query} onChangeText={setQuery} />
<ExpensiveList query={query} />  // Blocks typing
```

**Correct (input stays responsive):**

```jsx
const [query, setQuery] = useState('');
const deferredQuery = useDeferredValue(query);
<TextInput value={query} onChangeText={setQuery} />
<ExpensiveList query={deferredQuery} />  // Deferred update
```

## When to Use

- Search/filter inputs feel laggy with large result sets
- Expensive computations block UI interactions
- Loading states appear too frequently
- Want to show stale content while loading new content
- Need to prioritize user input over background updates

## Prerequisites

- React Native with New Architecture enabled (default in RN 0.76+)
- React 18+ features (`useDeferredValue`, `useTransition`, `Suspense`)

## Concept Overview

**Concurrent React** allows updates to be:
- **Paused**: Low-priority work can wait
- **Interrupted**: User input takes priority
- **Abandoned**: Outdated updates can be skipped

## Step-by-Step Instructions

### Pattern 1: Defer Expensive Rendering with `useDeferredValue`

Use when a value drives expensive computation but you want input to stay responsive.

```jsx
import { useState, useDeferredValue } from 'react';

const SearchScreen = () => {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  
  // query updates immediately (input stays responsive)
  // deferredQuery updates when React has time
  
  return (
    <View>
      <TextInput
        value={query}
        onChangeText={setQuery}
        placeholder="Search..."
      />
      {/* ExpensiveList receives deferred value */}
      <ExpensiveList query={deferredQuery} />
    </View>
  );
};
```

### Pattern 2: Show Stale Content While Loading

```jsx
const SearchWithStaleIndicator = () => {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  const isStale = query !== deferredQuery;
  
  return (
    <View>
      <TextInput value={query} onChangeText={setQuery} />
      <View style={isStale && { opacity: 0.7 }}>
        <SearchResults query={deferredQuery} />
      </View>
      {isStale && <ActivityIndicator />}
    </View>
  );
};
```

### Pattern 3: Transition Non-Critical Updates with `useTransition`

Use when you have multiple state updates and want to mark some as low-priority.

```jsx
import { useState, useTransition } from 'react';

const TransitionExample = () => {
  const [count, setCount] = useState(0);
  const [heavyData, setHeavyData] = useState(null);
  const [isPending, startTransition] = useTransition();
  
  const handleIncrement = () => {
    // High priority - updates immediately
    setCount(c => c + 1);
    
    // Low priority - can be interrupted
    startTransition(() => {
      setHeavyData(computeExpensiveData());
    });
  };
  
  return (
    <View>
      <Text>Count: {count}</Text>
      {isPending ? <ActivityIndicator /> : <HeavyComponent data={heavyData} />}
      <Button onPress={handleIncrement} title="Increment" />
    </View>
  );
};
```

### Pattern 4: Suspense for Data Fetching

```jsx
import { Suspense, useDeferredValue } from 'react';

const DataScreen = () => {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  
  return (
    <View>
      <TextInput value={query} onChangeText={setQuery} />
      <Suspense fallback={<LoadingSpinner />}>
        <SearchResults query={deferredQuery} />
      </Suspense>
    </View>
  );
};
```

## Code Examples

### Slow Component Optimization

```jsx
// Without Concurrent React - UI freezes
const SlowSearch = () => {
  const [query, setQuery] = useState('');
  
  return (
    <>
      <TextInput value={query} onChangeText={setQuery} />
      <SlowComponent query={query} /> {/* Blocks every keystroke */}
    </>
  );
};

// With Concurrent React - UI stays responsive  
const FastSearch = () => {
  const [query, setQuery] = useState('');
  const deferredQuery = useDeferredValue(query);
  
  return (
    <>
      <TextInput value={query} onChangeText={setQuery} />
      <SlowComponent query={deferredQuery} />
    </>
  );
};

// Important: Wrap SlowComponent in memo to prevent re-renders from parent
const SlowComponent = memo(({ query }) => {
  // Expensive computation here
});
```

### Automatic Batching (React 18+)

React 18 automatically batches state updates:

```jsx
// Before React 18 - 2 re-renders
setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
  // Rendered twice
}, 1000);

// React 18+ - 1 re-render (automatic batching)
setTimeout(() => {
  setCount(c => c + 1);
  setFlag(f => !f);
  // Rendered once!
}, 1000);
```

## When to Use Which

| Scenario | Solution |
|----------|----------|
| Single value drives expensive render | `useDeferredValue` |
| Multiple state updates, some non-critical | `useTransition` |
| Need loading indicator for transition | `useTransition` (has `isPending`) |
| Data fetching with loading states | `Suspense` + `useDeferredValue` |
| Simple parent-to-child value deferral | `useDeferredValue` |

## Important Considerations

1. **Wrap expensive components in `memo()`**: Without memoization, the component re-renders from parent anyway.

2. **Use with New Architecture**: Concurrent features require New Architecture in React Native.

3. **Don't overuse**: Only defer truly expensive work. Adding complexity for fast components is counterproductive.

## Common Pitfalls

- **Forgetting memo()**: `useDeferredValue` is useless if child re-renders from parent
- **Using for simple state**: Overhead isn't worth it for cheap updates
- **Expecting faster computation**: These hooks don't make code faster, they prioritize what runs when

## Related Skills

- [js-profile-react.md](./js-profile-react.md) - Identify slow components
- [js-react-compiler.md](./js-react-compiler.md) - Automatic memoization
- [js-lists-flatlist-flashlist.md](./js-lists-flatlist-flashlist.md) - For list-specific optimizations

---

## Reference: Js Lists Flatlist Flashlist

# Skill: Higher-Order Lists

Replace ScrollView with FlatList or FlashList for performant large list rendering.

## Quick Pattern

**Incorrect:**

```jsx
<ScrollView>
  {items.map((item) => <Item key={item.id} {...item} />)}
</ScrollView>
```

**Correct:**

```jsx
<FlashList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <Item {...item} />}
  estimatedItemSize={50}
/>
```

## When to Use

- Rendering more than 10-20 items in a list
- List scrolling is choppy or laggy
- App freezes when loading list data
- Memory usage spikes with long lists

## Prerequisites

- `@shopify/flash-list` for FlashList (recommended)
- Understanding of list virtualization

## Step-by-Step Instructions

### 1. Identify the Problem

<!-- image: FPS Drop Graph -->

The FPS graph shows a severe performance problem during list rendering:
- FPS starts at ~60 (smooth)
- Drops to ~3 FPS during heavy list operation
- Recovers after rendering completes

```jsx
// BAD: ScrollView renders ALL items at once
const BadList = ({ items }) => (
  <ScrollView>
    {items.map((item, index) => (
      <View key={index}>
        <Text>{item}</Text>
      </View>
    ))}
  </ScrollView>
);
```

With 5000 items, this creates 5000 views immediately, causing:
- Multi-second freeze
- FPS drop to 0
- High memory usage

### 2. Replace with FlatList

```jsx
import { FlatList } from 'react-native';

const BetterList = ({ items }) => {
  const renderItem = ({ item }) => (
    <View>
      <Text>{item}</Text>
    </View>
  );
  
  return (
    <FlatList
      data={items}
      renderItem={renderItem}
      keyExtractor={(item, index) => index.toString()}
    />
  );
};
```

FlatList only renders visible items + buffer (windowing).

### 3. Optimize FlatList with getItemLayout

For fixed-height items, skip layout measurement:

```jsx
const ITEM_HEIGHT = 50;

const OptimizedList = ({ items }) => {
  const renderItem = ({ item }) => (
    <View style={{ height: ITEM_HEIGHT }}>
      <Text>{item}</Text>
    </View>
  );
  
  const getItemLayout = (_, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  });
  
  return (
    <FlatList
      data={items}
      renderItem={renderItem}
      keyExtractor={(item, index) => index.toString()}
      getItemLayout={getItemLayout}
    />
  );
};
```

### 4. Upgrade to FlashList (Best Performance)

```bash
npm install @shopify/flash-list
```

```jsx
import { FlashList } from '@shopify/flash-list';

const BestList = ({ items }) => {
  const renderItem = ({ item }) => (
    <View style={{ height: 50 }}>
      <Text>{item}</Text>
    </View>
  );
  
  return (
    <FlashList
      data={items}
      renderItem={renderItem}
      estimatedItemSize={50}  // Required for FlashList
    />
  );
};
```

**FlashList advantages:**
- Recycles views instead of creating new ones
- 78/100 vs 25/100 performance score in benchmarks
- Smoother scrolling at ~54 FPS vs lower for FlatList

## Code Examples

### Variable Height Items

```jsx
// Calculate average for estimatedItemSize
// Items are 50px, 100px, 150px
// Average: (50 + 100 + 150) / 3 = 100px

<FlashList
  data={items}
  renderItem={renderItem}
  estimatedItemSize={100}
/>
```

### Mixed Item Types

```jsx
<FlashList
  data={items}
  renderItem={({ item }) => {
    if (item.type === 'header') return <Header {...item} />;
    if (item.type === 'product') return <Product {...item} />;
    return <DefaultItem {...item} />;
  }}
  getItemType={(item) => item.type}  // Helps recycling
  estimatedItemSize={80}
/>
```

### FlatList Optimizations (if not using FlashList)

```jsx
<FlatList
  data={items}
  renderItem={renderItem}
  // Performance props
  removeClippedSubviews={true}
  maxToRenderPerBatch={10}
  updateCellsBatchingPeriod={50}
  initialNumToRender={10}
  windowSize={5}
  // Avoid re-renders
  keyExtractor={(item) => item.id}
  extraData={selectedId}  // Only when selection changes
/>
```

## Performance Comparison

| Component | 5000 Items Load | Scroll FPS | Memory |
|-----------|-----------------|------------|--------|
| ScrollView | 1-3 seconds freeze | < 30 | High |
| FlatList | ~100ms | ~45 | Medium |
| FlashList | ~50ms | ~54 | Low |

## Decision Matrix

| Scenario | Recommendation |
|----------|---------------|
| < 20 static items | ScrollView OK |
| 20-100 items | FlatList minimum |
| > 100 items | FlashList |
| Complex item layouts | FlashList with `getItemType` |
| Fixed height items | Add `getItemLayout` or `estimatedItemSize` |

## Common Pitfalls

- **Inline renderItem functions**: Causes re-renders. Define outside or use `useCallback`.
- **Missing keyExtractor**: Use unique IDs, not array index when possible.
- **Ignoring estimatedItemSize warning**: FlashList warns if not set. Always provide it.
- **Heavy item components**: Keep list items light. Move side effects out.

## Related Skills

- [js-profile-react.md](./js-profile-react.md) - Profile list rendering
- [js-measure-fps.md](./js-measure-fps.md) - Measure scroll performance

---

## Reference: Js Measure Fps

# Skill: Measure JS FPS

Monitor and measure JavaScript frame rate to quantify app smoothness and identify performance regressions.

## Quick Command

```bash
# Method 1: Built-in Perf Monitor
# Shake device → Dev Menu → "Perf Monitor"

# Method 2: Flashlight (Android, detailed reports)
# Install Flashlight from an official, verified release channel first.
flashlight measure
```

## When to Use

- Animations feel choppy or janky
- Scrolling is not smooth
- Need baseline FPS metrics before/after optimization
- Want to compare performance across builds

## Prerequisites

- React Native app running on device/simulator
- For Flashlight: Android device (iOS not supported)

> **Note**: This skill involves interpreting visual output (FPS graphs, performance overlays). AI agents cannot yet process screenshots autonomously. Use this as a guide while reviewing metrics manually, or await MCP-based visual feedback integration (see roadmap).

## Step-by-Step Instructions

### Method 1: React Perf Monitor (Quick Check)

1. Open Dev Menu:
   - iOS Simulator: `Ctrl + Cmd + Z` or Device > Shake
   - Android Emulator: `Cmd + M` (Mac) / `Ctrl + M` (Windows)

2. Select **"Perf Monitor"**

3. Observe the overlay showing:
   - **UI (Main) thread FPS** - Native rendering
   - **JS thread FPS** - JavaScript execution
   - **RAM usage**

4. Hide with "Hide Perf Monitor" from Dev Menu

**Interpretation:**
- **60 FPS** = Smooth (16.6ms per frame)
- **< 60 FPS** = Dropping frames
- **120 FPS** target for high refresh rate devices (8.3ms per frame)

### Method 2: Flashlight (Automated Benchmarking)

> Android only. Provides detailed reports and JSON export.

<!-- image: Flashlight FlatList vs FlashList Comparison -->

Flashlight shows comparative performance data:
- **Score** (0-100): Overall performance rating (higher is better)
- **Average FPS**: Target 60 FPS for smooth scrolling
- **FPS Graph**: Real-time frame rate over test duration
- **CPU/RAM metrics**: Resource consumption

The image shows FlatList (score: 3) vs FlashList (score: 67) - a dramatic difference visible in both the score and FPS graph.

**Installation:**

Install Flashlight from the vendor's official release channel before using it. Prefer a package manager or a version-pinned binary with checksum/signature verification. Do not pipe a remote install script directly into a shell.

**Usage:**

```bash
# Start measuring (app must be running on Android)
flashlight measure
```

**Features:**
- Real-time FPS graph
- Average FPS calculation
- CPU and RAM metrics
- Overall performance score
- JSON export for CI comparison

### Important: Disable Dev Mode

**Always disable development mode for accurate measurements:**

**Android:**
1. Open Dev Menu
2. Settings > JS Dev Mode → **OFF**

**iOS (React Native CLI):**
```bash
# Run Metro in production mode
npx react-native start --reset-cache
# Then build release variant
```

**Expo:**
```bash
# Start Metro without dev mode
npx expo start --no-dev --minify
# For accurate measurements, use EAS Build for release testing
```

## Code Examples

### Identify FPS Drop Source

If **UI FPS drops but JS FPS is fine:**
- Native rendering issue
- Too many views/complex layouts
- Heavy native animations

If **JS FPS drops but UI FPS is fine:**
- JavaScript computation blocking
- Expensive React re-renders
- Look for `longRunningFunction` patterns

If **Both drop:**
- Mixed issue, start with JS profiling

### Target Frame Budgets

```javascript
// 60 FPS = 16.6ms per frame
const FRAME_BUDGET_60 = 16.6;

// 120 FPS = 8.3ms per frame  
const FRAME_BUDGET_120 = 8.3;

// If your function takes longer, it will drop frames
const longRunningFunction = () => {
  let i = 0;
  while (i < 1000000000) { // This blocks for seconds!
    i++;
  }
};
```

## Interpreting Results

| FPS Range | User Perception | Action |
|-----------|-----------------|--------|
| 55-60 | Smooth | Acceptable |
| 45-55 | Slight stutter | Investigate |
| 30-45 | Noticeable jank | Optimize required |
| < 30 | Very choppy | Critical fix needed |

## Flashlight CI Integration

```bash
# Export measurements to JSON
flashlight measure --output results.json

# Compare builds
flashlight compare baseline.json current.json
```

## Common Pitfalls

- **Measuring in dev mode**: Results will be artificially slow
- **Not using real device**: Simulators don't reflect real performance
- **Ignoring UI thread**: React Native has two threads - JS issues don't always show on UI thread
- **Single measurement**: Run multiple times, FPS varies

## Related Skills

- [js-profile-react.md](./js-profile-react.md) - Find what's causing FPS drops
- [js-animations-reanimated.md](./js-animations-reanimated.md) - Fix animation-related drops
- [js-lists-flatlist-flashlist.md](./js-lists-flatlist-flashlist.md) - Fix scroll-related drops

---

## Reference: Js Memory Leaks

# Skill: Hunt JS Memory Leaks

Find and fix JavaScript memory leaks using React Native DevTools memory profiling.

## Quick Pattern

**Incorrect (listener not cleaned up):**

```jsx
useEffect(() => {
  const sub = EventEmitter.addListener('event', handler);
  // Missing cleanup!
}, []);
```

**Correct (proper cleanup):**

```jsx
useEffect(() => {
  const sub = EventEmitter.addListener('event', handler);
  return () => sub.remove();
}, []);
```

## When to Use

- App memory usage grows over time
- App crashes after extended use
- Navigating between screens increases memory
- Suspecting event listeners or timers not cleaned up

## Prerequisites

- React Native DevTools accessible
- App running in development mode

## Step-by-Step Instructions

### 1. Open Memory Profiler

1. Launch React Native DevTools (press `j` in Metro)
2. Go to **Memory** tab
3. Select **"Allocation instrumentation on timeline"**

### 2. Record Memory Allocations

1. Click **"Start"** at the bottom
2. Perform actions that might leak (navigate, trigger events, etc.)
3. Wait 10-30 seconds
4. Click **"Stop"**

### 3. Analyze the Timeline

**Key indicators:**
- **Blue bars** = Memory allocated
- **Gray bars** = Memory freed (garbage collected)
- **Blue bars that stay blue** = Potential leak!

### 4. Investigate Leaking Objects

<!-- image: Memory Heap Snapshot -->

The Memory tab shows:
- **Timeline** (top): Blue bars = allocations, select time range to filter
- **Summary view** (bottom): Lists constructors with allocation counts

**Key columns:**
- **Constructor**: Object type (e.g., `JSObject`, `Function`, `(string)`)
- **Count**: Number of instances (×85000 = 85,000 objects)
- **Shallow Size**: Memory of the object itself
- **Retained Size**: Memory freed if object is deleted (including references)

**Red flag**: Large retained size % with small shallow size % = closures or references holding large objects.

**To investigate:**
1. Click on a blue spike in the timeline
2. Look at the Constructor list below
3. Check **Shallow size** vs **Retained size**
4. Expand constructors to see individual allocations
5. Click to see the exact source location

### 5. Verify the Fix

After fixing, re-profile. All bars should turn gray (except the most recent).

## Code Examples

### Common Leak Patterns

**1. Listeners Not Cleaned Up:**

```jsx
// BAD: Memory leak
const BadEventComponent = () => {
  useEffect(() => {
    const subscription = EventEmitter.addListener('myEvent', handleEvent);
    // Missing cleanup!
  }, []);
  
  return <Text>Listening...</Text>;
};

// GOOD: Proper cleanup
const GoodEventComponent = () => {
  useEffect(() => {
    const subscription = EventEmitter.addListener('myEvent', handleEvent);
    return () => subscription.remove(); // Cleanup!
  }, []);
  
  return <Text>Listening...</Text>;
};
```

**2. Timers Not Cleared:**

```jsx
// BAD: Memory leak
const BadTimerComponent = () => {
  useEffect(() => {
    const timer = setInterval(() => {
      setCount(prev => prev + 1);
    }, 1000);
    // Missing cleanup!
  }, []);
};

// GOOD: Proper cleanup
const GoodTimerComponent = () => {
  useEffect(() => {
    const timer = setInterval(() => {
      setCount(prev => prev + 1);
    }, 1000);
    return () => clearInterval(timer); // Cleanup!
  }, []);
};
```

**3. Closures Capturing Large Objects:**

```jsx
// BAD: Closure captures entire array
class BadClosureExample {
  private largeData = new Array(1000000).fill('data');
  
  createLeakyFunction() {
    return () => this.largeData.length; // Captures this.largeData
  }
}

// GOOD: Only capture what's needed
class GoodClosureExample {
  private largeData = new Array(1000000).fill('data');
  
  createEfficientFunction() {
    const length = this.largeData.length; // Extract value
    return () => length; // Only captures primitive
  }
}
```

**4. Global Arrays Growing:**

```jsx
// BAD: Global array never cleared
let leakyClosures = [];

const createLeak = () => {
  const data = generateLargeData();
  leakyClosures.push(() => data); // Keeps growing!
};

// GOOD: Clear when done or use WeakRef
const createNoLeak = () => {
  const data = generateLargeData();
  const closure = () => data;
  // Use it and let it be garbage collected
  return closure;
};
```

## Memory Profiler Metrics

| Metric | Meaning |
|--------|---------|
| **Shallow size** | Memory held by the object itself |
| **Retained size** | Memory freed if object is deleted (includes references) |

**Large retained size with small shallow size** = Object holding references to other large objects (common in closures).

## Common Pitfalls

- **Not forcing GC**: GC runs periodically. Allocate something else to trigger collection before concluding there's a leak.
- **Ignoring gray bars**: Gray = properly collected. Only blue bars that persist are leaks.
- **Missing useEffect cleanup**: Most common React Native leak source.

## Related Skills

- [native-memory-leaks.md](./native-memory-leaks.md) - Native-side memory leaks
- [js-profile-react.md](./js-profile-react.md) - General profiling

---

## Reference: Js Profile React

# Skill: Profile React Performance

Identify unnecessary re-renders and performance bottlenecks in React Native apps using React Native DevTools.

## Quick Command

```bash
# Open React Native DevTools (press 'j' in Metro terminal)
# Or shake device → "Open DevTools"
# Go to Profiler tab → Start profiling → Perform actions → Stop
```

## When to Use

- App feels sluggish or janky during interactions
- Need to identify which components re-render unnecessarily
- Investigating slow list scrolling or form inputs
- Before applying memoization or state management changes

## Prerequisites

- React Native DevTools accessible (press `j` in Metro or use Dev Menu)
- App running in development mode
- React DevTools version 6.0.1+ for React Compiler support

> **Note**: This skill involves interpreting visual profiler output (flame graphs, component highlighting). AI agents cannot yet process screenshots autonomously. Use this as a guide while reviewing the profiler UI manually, or await MCP-based visual feedback integration (see roadmap).

## Step-by-Step Instructions

### 1. Open React Native DevTools

```bash
# Option A: Press 'j' in Metro terminal (works with both RN CLI and Expo)
# Option B: Shake device / Cmd+D (iOS) / Cmd+M (Android) → "Open DevTools"
# Expo: Also accessible via Expo DevTools in browser
```

### 2. Configure Profiler Settings

1. Go to **Profiler** tab
2. Click gear icon (⚙️) for settings
3. Enable:
   - "Highlight updates when components render"
   - "Record why each component rendered while profiling"

### 3. Record a Profiling Session

```
1. Click "Start profiling" (blue circle) or "Reload and start profiling"
2. Perform the interaction you want to analyze
3. Click "Stop profiling"
```

**Use "Reload and start profiling"** for startup performance analysis.

### 4. Analyze the Flame Graph

<!-- image: React DevTools Flamegraph -->

The flame graph shows component render hierarchy with timing:

**Color indicators:**
- **Yellow components**: Most time spent rendering (focus here)
- **Green components**: Fast/memoized
- **Gray components**: Did not render

**Right panel shows "Why did this render?":**
- Props changed (shows which prop, e.g., `children`, `onPress`)
- Rendered at timestamps with duration (e.g., "3.7s for 0.9ms")

**Click on a component to see:**
- Why it rendered (hook change, props change, parent re-render)
- Render duration
- Child components affected

### 5. Use Ranked View for Bottom-Up Analysis

Click "Ranked" tab to see components sorted by render time (slowest first).

### 6. Profile JavaScript CPU

For non-React performance issues:

1. Go to **JavaScript Profiler** tab (enable in settings if hidden)
2. Click "Start" to record
3. Perform actions
4. Click "Stop"
5. Use **Heavy (Bottom Up)** view to find slowest functions

## Code Examples

### Before: Unnecessary Re-renders

```jsx
const App = () => {
  const [count, setCount] = useState(0);
  
  return (
    <View>
      <Text>{count}</Text>
      {/* Button re-renders on every count change */}
      <Button onPress={() => setCount(count + 1)} title="Press" />
    </View>
  );
};

const Button = ({onPress, title}) => (
  <Pressable onPress={onPress}>
    <Text>{title}</Text>
  </Pressable>
);
```

### After: Memoized

```jsx
const App = () => {
  const [count, setCount] = useState(0);
  const onPressHandler = useCallback(() => setCount(c => c + 1), []);
  
  return (
    <View>
      <Text>{count}</Text>
      <Button onPress={onPressHandler} title="Press" />
    </View>
  );
};

const Button = memo(({onPress, title}) => (
  <Pressable onPress={onPress}>
    <Text>{title}</Text>
  </Pressable>
));
```

## Interpreting Results

| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| Many yellow components | Cascading re-renders | Add memoization or use React Compiler |
| "Props changed" on callbacks | Inline functions recreated | Use `useCallback` |
| "Parent component rendered" | State too high in tree | Move state down or use atomic state |
| Long JS thread block | Heavy computation | Move to background or use `useDeferredValue` |

## Common Pitfalls

- **Profiling in dev mode**: Always disable JS Dev Mode for accurate measurements (Settings > JS Dev Mode on Android)
- **Not using production builds**: Some issues only appear with minified code
- **Ignoring "Why did this render?"**: This tells you exactly what to fix

## Related Skills

- [js-react-compiler.md](./js-react-compiler.md) - Automatic memoization
- [js-atomic-state.md](./js-atomic-state.md) - Reduce re-renders with Jotai/Zustand
- [js-measure-fps.md](./js-measure-fps.md) - Quantify frame rate impact

---

## Reference: Js React Compiler

# Skill: React Compiler

Set up React Compiler to automatically memoize components and eliminate unnecessary re-renders.

## Quick Pattern

**Before (manual memoization):**

```jsx
const MemoizedButton = memo(({ onPress }) => <Pressable onPress={onPress} />);
const handler = useCallback(() => doSomething(), []);
```

**After (automatic with React Compiler):**

```jsx
// No memo/useCallback needed - compiler handles it
const Button = ({ onPress }) => <Pressable onPress={onPress} />;
const handler = () => doSomething();
```

## When to Use

- Want automatic performance optimization without manual `memo`/`useMemo`/`useCallback`
- Codebase follows Rules of React
- React Native 0.76+ or Expo SDK 52+
- Ready to remove boilerplate memoization code

## Prerequisites

- React 17+ (React 19 recommended for best compatibility)
- Babel-based build system
- Code follows [Rules of React](https://react.dev/reference/rules)

## Step-by-Step Instructions

### Step 1: Check Compatibility

Before enabling the compiler, verify your project is compatible:

```bash
npx react-compiler-healthcheck@latest
```

This checks if your app follows the Rules of React and identifies potential issues.

### Step 2: Install React Compiler

#### Expo Projects

**SDK 54 and later** (simplified setup):

```bash
npx expo install babel-plugin-react-compiler
```

**SDK 52-53**:

```bash
npx expo install babel-plugin-react-compiler@beta react-compiler-runtime@beta
```

Then enable in your app config:

```json
// app.json
{
  "expo": {
    "experiments": {
      "reactCompiler": true
    }
  }
}
```

#### React Native (without Expo)

```bash
npm install -D babel-plugin-react-compiler@latest
```

For React Native < 0.78 (React < 19), also install the runtime:

```bash
npm install react-compiler-runtime@beta
```

### Step 3: Configure Babel (React Native without Expo)

For non-Expo React Native projects, configure Babel manually:

```javascript
// babel.config.js
const ReactCompilerConfig = {
  target: '19', // Use '18' for React Native < 0.78
};

module.exports = function (api) {
  api.cache(true);
  return {
    presets: ['module:@react-native/babel-preset'],
    plugins: [
      ['babel-plugin-react-compiler', ReactCompilerConfig], // Must run first!
      // ... other plugins
    ],
  };
};
```

> **Important**: React Compiler must run **first** in your Babel plugin pipeline. The compiler needs the original source information for proper analysis.

### Step 4: Set Up ESLint (Recommended)

The ESLint plugin helps identify code that can't be optimized and enforces the Rules of React.

#### Expo Projects

```bash
npx expo lint  # Ensures ESLint is set up
npx expo install eslint-plugin-react-compiler -- -D
```

Configure ESLint:

```javascript
// .eslintrc.js
const { defineConfig } = require('eslint/config');
const expoConfig = require('eslint-config-expo/flat');
const reactCompiler = require('eslint-plugin-react-compiler');

module.exports = defineConfig([
  expoConfig,
  reactCompiler.configs.recommended,
  {
    ignores: ['dist/*'],
  },
]);
```

#### React Native (without Expo)

```bash
npm install -D eslint-plugin-react-hooks@latest
```

The compiler rules are available in the `recommended-latest` preset. Follow the [eslint-plugin-react-hooks installation instructions](https://github.com/facebook/react/tree/main/packages/eslint-plugin-react-hooks).

### Step 5: Verify Optimizations

Open React DevTools. Optimized components show a `Memo ✨` badge.

You can also verify by checking build output—compiled code includes automatic memoization:

```javascript
import { c as _c } from 'react/compiler-runtime';

export default function MyApp() {
  const $ = _c(1);
  let t0;
  if ($[0] === Symbol.for('react.memo_cache_sentinel')) {
    t0 = <div>Hello World</div>;
    $[0] = t0;
  } else {
    t0 = $[0];
  }
  return t0;
}
```

**Note**: React Native 0.76+ includes DevTools with Memo badge support by default. For older versions or third-party debuggers with version mismatches, you may need to override `react-devtools-core` in `package.json`.

## Incremental Adoption

You can incrementally adopt React Compiler using two strategies:

### Strategy 1: Limit to Specific Directories

Configure the Babel plugin to only run on specific files, e.g. `src/path/to/dir` in the following examples:

**Expo** (create `babel.config.js` with `npx expo customize babel.config.js`):

```javascript
// babel.config.js
module.exports = function (api) {
  api.cache(true);
  return {
    presets: [
      [
        'babel-preset-expo',
        {
          'react-compiler': {
            sources: (filename) => {
              return filename.includes('src/path/to/dir');
            },
          },
        },
      ],
    ],
  };
};
```

**React Native (without Expo)**:

```javascript
// babel.config.js
const ReactCompilerConfig = {
  target: '19',
  sources: (filename) => {
    return filename.includes('src/path/to/dir');
  },
};

module.exports = function (api) {
  api.cache(true);
  return {
    presets: ['module:@react-native/babel-preset'],
    plugins: [['babel-plugin-react-compiler', ReactCompilerConfig]],
  };
};
```

After changing `babel.config.js`, restart Metro with cache cleared:

```bash
# Expo
npx expo start --clear

# React Native CLI
npx react-native start --reset-cache
```

### Strategy 2: Opt Out Specific Components

Use the `"use no memo"` directive to skip optimization for specific components or files:

```jsx
function ProblematicComponent() {
  'use no memo';

  return <Text>Will not be optimized</Text>;
}
```

This is useful for temporarily opting out components that cause issues. Fix the underlying problem and remove the directive once resolved.

## How It Works

The compiler transforms your code to automatically cache values:

**Before (your code):**

```jsx
export default function MyApp() {
  const [value, setValue] = useState('');
  return (
    <TextInput onChangeText={() => setValue(value)}>Hello World</TextInput>
  );
}
```

**After (compiled output):**

```jsx
import { c as _c } from 'react/compiler-runtime';

export default function MyApp() {
  const $ = _c(2); // Cache with 2 slots
  const [value, setValue] = useState('');

  let t0;
  if ($[0] !== value) {
    t0 = (
      <TextInput onChangeText={() => setValue(value)}>Hello World</TextInput>
    );
    $[0] = value;
    $[1] = t0;
  } else {
    t0 = $[1]; // Return cached JSX
  }
  return t0;
}
```

## Code Examples

### React Compiler Playground

Test transformations at [React Playground](https://playground.react.dev/).

### What Gets Optimized

```jsx
// Components - auto-memoized
const Button = ({ onPress, label }) => (
  <Pressable onPress={onPress}>
    <Text>{label}</Text>
  </Pressable>
);

// Callbacks - auto-cached (no useCallback needed)
const handlePress = () => {
  console.log('pressed');
};

// Expensive computations - auto-cached (no useMemo needed)
const filtered = items.filter((item) => item.active);
```

### What Breaks Compilation

```jsx
// BAD: Mutating props
const BadComponent = ({ items }) => {
  items.push('new item'); // Mutation!
  return <List data={items} />;
};

// BAD: Mutating during render
const BadMutation = () => {
  const [items, setItems] = useState([]);
  items.push('new'); // Mutation during render!
  return <List data={items} />;
};

// BAD: Non-idempotent render
let counter = 0;
const BadRender = () => {
  counter++; // Side effect during render!
  return <Text>{counter}</Text>;
};
```

## Should You Remove Manual Memoization?

Improvements are primarily automatic. You can remove instances of `useCallback`, `useMemo`, and `React.memo` in favor of automatic memoization once the compiler is working correctly in your project.

**Note**: Class components will not be optimized. Migrate to function components for full benefits.

Expo's implementation only runs on application code (not node_modules), and only when bundling for the client (disabled in server rendering).

## Expected Performance Improvements

Testing on Expensify app showed:

- **4.3% improvement** in Chat Finder TTI
- Significant reduction in cascading re-renders
- Most impact on apps without existing manual optimization

Already heavily optimized apps may see marginal gains.

## Common Pitfalls

- **Not fixing ESLint errors first**: When ESLint reports an error, the compiler skips that component—this is safe but means you miss optimization
- **Expecting it to fix bad patterns**: Compiler optimizes good code, doesn't fix bad code
- **Forgetting shallow comparison**: Like `memo`, compiler uses shallow comparison for objects/arrays
- **Not running healthcheck**: Always run `npx react-compiler-healthcheck@latest` before enabling

## Related Skills

- [js-profile-react.md](./js-profile-react.md) - Verify optimization impact
- [js-atomic-state.md](./js-atomic-state.md) - Alternative for state-related re-renders

---

## Reference: Js Uncontrolled Components

# Skill: Uncontrolled Components

Fix TextInput synchronization and flickering issues by using uncontrolled component pattern.

## Quick Pattern

**Before (controlled - may flicker on legacy arch):**

```jsx
<TextInput value={text} onChangeText={setText} />
```

**After (uncontrolled - native owns state):**

```jsx
<TextInput defaultValue={text} onChangeText={setText} />
```

## When to Use

- TextInput flickers or shows wrong characters during fast typing
- Text input lags behind user input on low-end devices
- Using legacy (non-New Architecture) React Native
- Need maximum input responsiveness

## Prerequisites

- Understanding of React controlled vs uncontrolled components
- TextInput component in use

## Problem Description

<!-- image: Controlled TextInput Ping-Pong Communication -->

The diagram shows what happens when typing "TEST" with a controlled `TextInput`:

1. User types "T" → `onChangeText('T')` fires
2. React calls `setValue('T')` → native updates to "T"
3. User types "E" → `onChangeText('TE')` fires
4. React calls `setValue('TE')` → native updates to "TE"
5. ...continues for each character

**The problem**: Each character requires a round-trip between native and JavaScript. On legacy architecture, if React state update is slow, native may show intermediate states (flicker).

**New Architecture note:** This issue is largely resolved in New Architecture, but uncontrolled pattern still provides best performance.

## Step-by-Step Instructions

### 1. Identify Controlled TextInput

```jsx
// Controlled - value prop syncs state to native
const ControlledInput = () => {
  const [value, setValue] = useState('');
  
  return (
    <TextInput
      value={value}           // This causes sync issues
      onChangeText={setValue}
    />
  );
};
```

### 2. Convert to Uncontrolled

Remove the `value` prop to make it uncontrolled:

```jsx
// Uncontrolled - native owns the state
const UncontrolledInput = () => {
  const [value, setValue] = useState('');
  
  return (
    <TextInput
      defaultValue={value}     // Only sets initial value
      onChangeText={setValue}  // Still updates React state
    />
  );
};
```

### 3. Use Ref for Programmatic Control

If you need to read/set value programmatically:

```jsx
const UncontrolledWithRef = () => {
  const inputRef = useRef(null);
  
  const clearInput = () => {
    inputRef.current?.clear();
  };
  
  const getValue = () => {
    // Use onChangeText to track value, or native methods
  };
  
  return (
    <TextInput
      ref={inputRef}
      defaultValue=""
      onChangeText={(text) => console.log('Current:', text)}
    />
  );
};
```

## Code Examples

### Full Migration Example

**Before (Controlled):**

```jsx
const SearchInput = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  
  const handleChange = (text) => {
    setQuery(text);
    fetchResults(text).then(setResults);
  };
  
  return (
    <View>
      <TextInput
        value={query}              // Remove this
        onChangeText={handleChange}
        placeholder="Search..."
      />
      <ResultsList data={results} />
    </View>
  );
};
```

**After (Uncontrolled):**

```jsx
const SearchInput = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  
  const handleChange = (text) => {
    setQuery(text);
    fetchResults(text).then(setResults);
  };
  
  return (
    <View>
      <TextInput
        defaultValue=""           // Initial value only
        onChangeText={handleChange}
        placeholder="Search..."
      />
      <ResultsList data={results} />
    </View>
  );
};
```

### When You Need Value Control

For input masking or validation that modifies input:

```jsx
// Option 1: Accept the controlled behavior (may flicker)
const MaskedInput = () => {
  const [value, setValue] = useState('');
  
  const handleChange = (text) => {
    // Phone mask: (123) 456-7890
    const masked = maskPhone(text);
    setValue(masked);
  };
  
  return (
    <TextInput
      value={value}  // Necessary for masking
      onChangeText={handleChange}
    />
  );
};

// Option 2: Use a native masked input library
// react-native-masked-text handles this natively
```

## Decision Matrix

| Scenario | Recommendation |
|----------|---------------|
| Simple text input | Uncontrolled |
| Search/filter input | Uncontrolled |
| Form with validation on submit | Uncontrolled |
| Input masking (phone, credit card) | Controlled or native library |
| Character-by-character validation | Controlled |
| New Architecture app | Either works well |

## Common Pitfalls

- **Forgetting `defaultValue`**: Without it, input starts empty
- **Trying to clear with state**: Use `ref.current.clear()` instead
- **Mixing patterns**: Don't use both `value` and `defaultValue`

## Related Skills

- [js-profile-react.md](./js-profile-react.md) - Profile input performance
- [js-concurrent-react.md](./js-concurrent-react.md) - Defer expensive search operations

---

## Reference: Native Android 16Kb Alignment

# Android 16 KB page size alignment

---

## Quick Reference

| Item                   | Details                                              |
| ---------------------- | ---------------------------------------------------- |
| Google Play deadline   | November 1, 2025 for apps targeting Android 15+      |
| React Native support   | Built-in since React Native 0.79                     |
| What to check          | Third-party native libraries (`.so` files)           |
| Official documentation | [developer.android.com/guide/practices/page-sizes][] |

[developer.android.com/guide/practices/page-sizes]: https://developer.android.com/guide/practices/page-sizes

---

## Quick Command

Verify APK alignment using Android's official `zipalign` tool:

```bash
zipalign -c -P 16 -v 4 app-release.apk
```

If any 64-bit libraries (`arm64-v8a`, `x86_64`) show misalignment, they need updating.

For deeper ELF-level inspection, use Android's [check_elf_alignment.sh][] script.

[check_elf_alignment.sh]: https://cs.android.com/android/platform/superproject/main/+/main:system/extras/tools/check_elf_alignment.sh

---

## When to Check

React Native 0.79+ builds core binaries with correct alignment. However, **third-party
native libraries** may still be misaligned. Check alignment when:

* Adding or updating SDKs with native code
* Preparing a release for Google Play
* Investigating crashes on Android 15+ devices with 16 KB page size

---

## CI Integration

Add alignment check to your release pipeline to catch issues before submission, example:

```bash
zipalign -c -P 16 -v 4 app-release.apk 2>&1 | tee alignment.log
if grep -q "Verification FAILED" alignment.log; then exit 1; fi
```

## Step-by-Step

1. Build your release APK or AAB
2. Run `zipalign` verification (see Quick Command)
3. If misaligned libraries are found, trace them to source packages (see below)
4. Update, replace, or remove the affected dependencies

For runtime testing, use the [16KB Android Emulator image][] or enable
"Boot with 16KB page size" on Pixel 8/8a/9 devices.

[16KB Android Emulator image]: https://developer.android.com/guide/practices/page-sizes#set-up-the-android-emulator-with-a-16-kb-based-system-image

---

## Tracing Misaligned Libraries

When `zipalign` reports a misaligned library like `libfoo.so`, find its source package:

```bash
# Find the .so file in node_modules
find node_modules -name "libfoo.so" 2>/dev/null

# Or search gradle files for references
grep -r "foo" node_modules/*/android --include="*.gradle" 2>/dev/null
```

Once identified, update the dependency or contact the vendor for a 16KB-compatible build.

---

## Common Pitfalls

* Waiting for Play Store rejection instead of checking in CI
* Assuming a React Native upgrade rebuilds third-party native binaries
* Only checking 32-bit ABIs (`armeabi-v7a`, `x86`) — these are not affected
* Using `zipalign` without the `-P 16` flag (checks 4 KB, not 16 KB)
* Validating only debug builds

---

## Fixing Alignment Issues

Alignment issues require **rebuilding** the native library with a compatible toolchain.
Repackaging alone does not fix them.

See [official remediation steps][] for detailed guidance.

[official remediation steps]: https://developer.android.com/guide/practices/page-sizes#build-app-16kb

---

## Related Skills

* [native-profiling.md](./native-profiling.md) — Native debugging tools

---

## Reference: Native Measure Tti

# Skill: Measure TTI (Time to Interactive)

Set up performance markers to measure app startup time and track TTI improvements.

## Quick Command

```bash
npm install react-native-performance
```

```tsx
// Mark when screen is interactive
import performance from 'react-native-performance';

useEffect(() => {
  performance.mark('screenInteractive');
}, []);
```

## When to Use

- App startup feels slow
- Need baseline metrics for optimization
- Setting up performance monitoring
- Comparing TTI across releases

## Prerequisites

- `react-native-performance` library (recommended)

```bash
npm install react-native-performance
```

> **Note**: This skill involves interpreting visual timeline diagrams and profiler output. AI agents cannot yet process screenshots autonomously. Use this as a guide while reviewing metrics manually, or await MCP-based visual feedback integration (see roadmap).

## Understanding TTI

**Time to Interactive**: Time from app icon tap to displaying usable content.

### Startup Types

| Type | Description | Measure? |
|------|-------------|----------|
| Cold | App not in memory, full init | ✅ Yes |
| Warm | Process exists, activity recreated | ❌ Skip |
| Hot | App in background, resumed | ❌ Skip |
| Prewarmed (iOS) | iOS pre-initialized app | ❌ Filter out |

**Only measure cold starts** for consistent metrics.

## React Native Startup Pipeline

<!-- image: TTI Warm Start Diagram -->

The diagram shows a warm start (app was in memory):

**UI Thread:**
1. `init native process` → `init native app`
2. Gap while user is away (e.g., "5h break from using the app")
3. `JS bundle load` → `RootView render`

**JS Thread (runs in parallel):**
- `init entrypoint` → `registerComponent`

**Pipeline markers:**
```
1. Native Process Init     (nativeLaunchStart → nativeLaunchEnd)
2. Native App Init         (appCreationStart → appCreationEnd)  
3. JS Bundle Load          (runJSBundleStart → runJSBundleEnd)
4. RN Root View Render     (contentAppeared)
5. React App Interactive   (screenInteractive) ← This is TTI
```

## Step-by-Step Implementation

### 1. Detect Cold Start

**iOS (Swift):**

```swift
let isColdStart = ProcessInfo.processInfo.environment["ActivePrewarm"] != "1"
```

**Android (Kotlin):**

```kotlin
class MainApplication : Application() {
    var isColdStart = false
    
    override fun onCreate() {
        super.onCreate()
        
        var firstPostEnqueued = true
        Handler().post { firstPostEnqueued = false }
        
        registerActivityLifecycleCallbacks(object : ActivityLifecycleCallbacks {
            override fun onActivityCreated(activity: Activity, savedInstanceState: Bundle?) {
                unregisterActivityLifecycleCallbacks(this)
                if (firstPostEnqueued && savedInstanceState == null) {
                    isColdStart = true
                }
            }
            // ... other callbacks
        })
    }
}
```

### 2. Check Foreground State

Only measure when app starts in foreground.

**iOS:**

```swift
var isForegroundProcess = false

override func application(_ application: UIApplication, 
    didFinishLaunchingWithOptions launchOptions: [UIApplication.LaunchOptionsKey: Any]?) -> Bool {
    if application.applicationState == .active {
        isForegroundProcess = true
    }
    return true
}
```

**Android:**

```kotlin
private fun isForegroundProcess(): Boolean {
    val processInfo = ActivityManager.RunningAppProcessInfo()
    ActivityManager.getMyMemoryState(processInfo)
    return processInfo.importance == IMPORTANCE_FOREGROUND
}
```

### 3. Set Up Performance Markers

Using `react-native-performance`:

**Native (iOS):**

```swift
import ReactNativePerformance

RNPerformance.sharedInstance().mark("appCreationStart")
// ... app init ...
RNPerformance.sharedInstance().mark("appCreationEnd")
```

**Native (Android):**

```kotlin
import com.oblador.performance.RNPerformance

RNPerformance.getInstance().mark("appCreationStart")
// ... app init ...
RNPerformance.getInstance().mark("appCreationEnd")
```

### 4. Mark Screen Interactive (JavaScript)

```tsx
import performance from 'react-native-performance';

export default function HomeScreen() {
    useEffect(() => {
        // Mark when meaningful content is displayed
        performance.mark('screenInteractive');
    }, []);
    
    return <TabNavigator />;
}
```

### 5. Collect and Report Metrics

```tsx
import performance from 'react-native-performance';

const collectTTIMetrics = () => {
    const entries = performance.getEntriesByType('mark');
    
    // Calculate durations
    const metrics = {
        nativeInit: getMarkDuration('nativeLaunchStart', 'nativeLaunchEnd'),
        appCreation: getMarkDuration('appCreationStart', 'appCreationEnd'),
        jsBundleLoad: getMarkDuration('runJSBundleStart', 'runJSBundleEnd'),
        tti: getMarkDuration('nativeLaunchStart', 'screenInteractive'),
    };
    
    // Send to analytics
    analytics.track('app_performance', metrics);
};
```

## Built-in Markers

`react-native-performance` provides automatic markers:

| Marker | Description |
|--------|-------------|
| `nativeLaunchStart` | Process start (pre-main) |
| `nativeLaunchEnd` | Native init complete |
| `runJSBundleStart` | JS bundle loading starts |
| `runJSBundleEnd` | JS bundle loaded |
| `contentAppeared` | RN root view rendered |

## Listening to Native Events

**iOS (JS Bundle Load):**

```swift
NotificationCenter.default.addObserver(
    self,
    selector: #selector(onJSLoad),
    name: NSNotification.Name("RCTJavaScriptDidLoadNotification"),
    object: nil
)
```

**Android (JS Bundle Load):**

```kotlin
ReactMarker.addListener { name ->
    when (name) {
        RUN_JS_BUNDLE_START -> { /* mark start */ }
        RUN_JS_BUNDLE_END -> { /* mark end */ }
        CONTENT_APPEARED -> { /* mark content */ }
    }
}
```

## Target Metrics

| Metric | Good | Acceptable | Needs Work |
|--------|------|------------|------------|
| TTI | < 2s | 2-4s | > 4s |
| JS Bundle Load | < 500ms | 500ms-1s | > 1s |
| Native Init | < 500ms | 500ms-1s | > 1s |

**Note**: Targets vary by app complexity and device tier.

## Common Pitfalls

- **Including prewarmed starts**: iOS prewarming skews metrics
- **Measuring warm/hot starts**: Only cold starts are meaningful
- **Wrong screenInteractive placement**: Mark when truly interactive, not just mounted
- **Not filtering background launches**: Push notifications can start app in background

## Related Skills

- [bundle-analyze-js.md](./bundle-analyze-js.md) - Reduce JS bundle load time
- [native-profiling.md](./native-profiling.md) - Profile native init
- [bundle-hermes-mmap.md](./bundle-hermes-mmap.md) - Improve Android TTI

---

## Reference: Native Memory Leaks

# Skill: Hunt Native Memory Leaks

Find native memory leaks using Xcode Leaks and Android Studio Memory Profiler.

## Quick Command

```bash
# iOS: Profile with Leaks instrument
# Xcode → Product → Profile (Cmd+I) → Leaks template

# Android: Memory Profiler
# Android Studio → Run → Profile → Track Memory Consumption
```

## When to Use

- App memory grows despite JS profiler showing no leaks
- Native modules suspected of leaking
- Activity recreation causes memory growth (Android)
- C++/Swift/Kotlin code under investigation

## iOS: Xcode Leaks

### Quick Check: Memory Report

1. Run app via Xcode
2. Open **Debug Navigator** (side panel)
3. Click **Memory**
4. Watch graph for continuous growth

### Deep Analysis: Instruments Leaks

<!-- image: Xcode Instruments Templates -->

1. **Xcode → Product → Profile** (or Cmd+I)
2. Select **Leaks** template (highlighted with orange triangle icon in the grid)
3. Click **Choose**
4. Click **Record** (red circle)
5. Use the app, perform suspect actions
6. Stop recording

The template picker shows all available Instruments:
- **Leaks**: Memory leak detection (what we need)
- **Allocations**: All memory allocations over time
- **Time Profiler**: CPU usage profiling
- **Zombies**: Detect messages to deallocated objects

### Analyzing Results

**Red markers** = Leaked memory detected

Click on leak to see:
- **Leaked Object**: Type and size
- **Responsible Library**: Which code leaked
- **Responsible Frame**: Exact function
- **Stack Trace**: Full call path (right panel)

**Double-click function** to see source code.

### Common iOS Leak: Missing delete

```cpp
// BAD: Memory leak
void createNewStrings() {
    std::string* str = new std::string("Hello");
    // Forgot delete str;
}

// GOOD: Fixed
void createNewStrings() {
    std::string* str = new std::string("Hello");
    // ... use str ...
    delete str;
}

// BETTER: Use smart pointers
void createNewStrings() {
    auto str = std::make_unique<std::string>("Hello");
    // Automatically deleted
}
```

## Android: Memory Profiler

### Launch Profiler

1. **Run → Profile** (or click Profile in toolbar)
2. Or: **View → Tool Windows → Profiler**
3. Select **"Track Memory Consumption"**

### Recording

1. Start the app
2. Perform actions that might leak
3. Watch memory graph for growth patterns

### Analyzing Allocations

Memory profiler shows:
- **Allocations count**: Objects created
- **Deallocations count**: Objects freed
- **Live objects**: Still in memory

**If allocations >> deallocations**, you have a leak.

### Common Android Leak: Listener Not Removed

```kotlin
// BAD: Leaks MainActivity on config change
class MainActivity : AppCompatActivity(), Callback {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        EventManager.addListener(this)
        // Never removed!
    }
}

// GOOD: Remove listener
class MainActivity : AppCompatActivity(), Callback {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        EventManager.addListener(this)
    }
    
    override fun onDestroy() {
        EventManager.removeListener(this)
        super.onDestroy()
    }
}
```

### Activity Recreation Test

Android recreates activities on:
- Screen rotation
- Dark mode change
- Locale change

**Test**: Rotate device multiple times, check if old activities are freed.

React Native note: RN opts out via `android:configChanges` in manifest, but native code might not.

## Debugging Workflow

### iOS

1. Profile with Instruments Leaks
2. Trigger suspect actions repeatedly
3. Wait for red leak markers
4. Click to identify responsible frame
5. Fix and re-test

### Android

1. Profile memory consumption
2. Trigger suspect actions (rotate, navigate)
3. Check allocation/deallocation counts
4. Look for classes with 0 deallocations
5. Fix and re-test

## Code Fixes by Pattern

### Reference Cycle (Swift)

```swift
// BAD
class Parent {
    var child: Child?
}
class Child {
    var parent: Parent?  // Strong reference cycle
}

// GOOD
class Parent {
    var child: Child?
}
class Child {
    weak var parent: Parent?  // Weak breaks cycle
}
```

### Missing Cleanup (C++)

```cpp
// BAD
void process() {
    auto* data = new LargeData();
    if (error) return;  // Leak!
    delete data;
}

// GOOD: RAII with unique_ptr
void process() {
    auto data = std::make_unique<LargeData>();
    if (error) return;  // Automatically cleaned up
}
```

### Global Singleton Holding References (Kotlin)

```kotlin
// BAD: Holds strong references
object Cache {
    private val items = mutableMapOf<String, Callback>()
}

// GOOD: Use weak references
object Cache {
    private val items = mutableMapOf<String, WeakReference<Callback>>()
}
```

## Verification

After fixing:
1. Re-run profiler
2. Perform same actions
3. Verify:
   - iOS: No red leak markers
   - Android: Allocations ≈ Deallocations

## Common Pitfalls

- **Testing in debug mode**: Some leaks only appear in release
- **Not waiting for GC**: Force GC before concluding no leak
- **Ignoring small leaks**: They add up over time
- **Missing cleanup in invalidate()**: Turbo Modules need proper cleanup

## Related Skills

- [native-memory-patterns.md](./native-memory-patterns.md) - Understanding memory patterns
- [js-memory-leaks.md](./js-memory-leaks.md) - JS-side leaks
- [native-threading-model.md](./native-threading-model.md) - Module invalidation

---

## Reference: Native Memory Patterns

# Skill: Native Memory Management

Understand memory management patterns in C++, Swift, and Kotlin for React Native native modules.

## Quick Reference

| Pattern | Languages | Mechanism |
|---------|-----------|-----------|
| Reference Counting | Swift, Obj-C, C++ (smart ptrs) | Count refs, free at zero |
| Garbage Collection | Kotlin/Java, JavaScript | GC scans and frees unreachable |
| Manual | C, C++ (raw pointers) | Explicit new/delete |

**Key rule**: Use `std::unique_ptr`/`std::shared_ptr` in C++, `weak` for delegates in Swift.

## When to Use

- Writing native modules with manual memory management
- Debugging native memory leaks
- Interfacing C++ with Swift/Kotlin
- Understanding reference counting vs garbage collection

## Memory Management Patterns

| Pattern | Languages | Mechanism |
|---------|-----------|-----------|
| Reference Counting | Swift, Obj-C, C++ (smart pointers) | Count refs, free at zero |
| Garbage Collection | Kotlin/Java, JavaScript | GC scans and frees unreachable |
| Manual | C, C++ (raw pointers) | Explicit new/delete |

## C++ Smart Pointers

### `std::unique_ptr` - Single Owner

```cpp
#include <memory>

void takeOwnership(std::unique_ptr<std::string> s) {
    std::cout << *s;
    // Automatically deleted when function ends
}

int main() {
    auto str = std::make_unique<std::string>("Hello");
    
    // Can only be moved, not copied
    takeOwnership(std::move(str));
    // str is now empty
    
    return 0;
}
```

### `std::shared_ptr` - Multiple Owners

```cpp
void useShared(std::shared_ptr<std::string> s) {
    std::cout << *s;  // Reference count temporarily +1
}

void useReference(const std::shared_ptr<std::string>& s) {
    std::cout << *s;  // No ref count change (passed by reference)
}

int main() {
    auto str = std::make_shared<std::string>("Hello");
    
    useShared(str);      // Copies pointer, ref count +1
    useReference(str);   // No copy, ref count unchanged
    
    std::cout << *str;   // Still valid
    return 0;
}
```

### `std::weak_ptr` - Non-Owning Reference

```cpp
void useWeak(std::weak_ptr<std::string> weak) {
    if (auto shared = weak.lock()) {  // Check if still exists
        std::cout << *shared;
    } else {
        std::cout << "Object destroyed";
    }
}

int main() {
    auto str = std::make_shared<std::string>("Hello");
    std::weak_ptr<std::string> weak = str;  // No ref count increase
    
    useWeak(weak);  // Works
    str.reset();    // Destroys object
    useWeak(weak);  // "Object destroyed"
    
    return 0;
}
```

## Swift ARC (Automatic Reference Counting)

```swift
class Person {
    let name: String
    init(name: String) { self.name = name }
    deinit { print("Deallocated") }
}

do {
    let person1 = Person(name: "John")  // Ref count: 1
    
    do {
        let person2 = person1  // Ref count: 2
    }  // person2 out of scope, ref count: 1
    
}  // person1 out of scope, ref count: 0, "Deallocated"
```

### Breaking Reference Cycles with `weak`

```swift
// BAD: Reference cycle (memory leak)
class A {
    var b: B?
}
class B {
    var a: A?  // Strong reference creates cycle
}

// GOOD: Use weak to break cycle
class A {
    var b: B?
}
class B {
    weak var a: A?  // Weak reference, doesn't prevent deallocation
}
```

## Kotlin/Android GC

### WeakHashMap for Caches

```kotlin
val weakMap = WeakHashMap<String, String>()

run {
    weakMap[String("temp")] = "value"
    println(weakMap.size)  // 1
}

System.gc()  // Force garbage collection
Thread.sleep(100)

println(weakMap.size)  // 0 (key was collected)
```

### WeakReference for Callbacks

```kotlin
class DataManager {
    // Weak references to listeners prevent memory leaks
    private val listeners = mutableListOf<WeakReference<DataListener>>()
    
    fun addListener(listener: DataListener) {
        listeners.add(WeakReference(listener))
    }
    
    fun notifyListeners(data: String) {
        listeners.forEach { ref ->
            ref.get()?.onDataChanged(data)
        }
    }
}
```

## Common Memory Leak Sources

### 1. Forgetting to Delete (C++)

```cpp
// BAD: Memory leak
int main() {
    std::string* str = new std::string("Hello");
    // Forgot to delete!
    return 0;
}

// GOOD: Use smart pointers or stack allocation
int main() {
    auto str = std::make_unique<std::string>("Hello");
    // Automatically deleted
    return 0;
}
```

### 2. Reference Cycles (Swift/C++)

```cpp
// BAD: Cycle
class A { std::shared_ptr<B> b; };
class B { std::shared_ptr<A> a; };

// GOOD: Break with weak_ptr
class A { std::shared_ptr<B> b; };
class B { std::weak_ptr<A> a; };
```

### 3. Unremoved Listeners (Kotlin)

```kotlin
// BAD: Listener never removed
class MyClass {
    private val listener = object : Callback {
        override fun onEvent() { /* ... */ }
    }
    
    init {
        EventManager.addListener(listener)
        // Never removed!
    }
}

// GOOD: Implement cleanup
class MyClass : AutoCloseable {
    private val listener = object : Callback {
        override fun onEvent() { /* ... */ }
    }
    
    init {
        EventManager.addListener(listener)
    }
    
    override fun close() {
        EventManager.removeListener(listener)
    }
}
```

## Swift `Unmanaged` (Advanced)

For C interop, manually manage reference counts:

```swift
let obj = MyObject()                        // Ref count: 1

// Increment manually
let unmanaged = Unmanaged.passRetained(obj) // Ref count: 2

// Decrement and get object
let retrieved = unmanaged.takeRetainedValue() // Ref count: 1

// Get raw pointer for C
let pointer = unmanaged.toOpaque()
```

**Rule**: Match `passRetained` with `takeRetainedValue`, `passUnretained` with `takeUnretainedValue`.

## Best Practices Summary

| Language | Best Practice |
|----------|---------------|
| C++ | Use smart pointers (`shared_ptr`, `unique_ptr`) |
| Swift | Use `weak` for delegates, breaking cycles |
| Kotlin | Implement `AutoCloseable`, use `WeakReference` |
| All | Prefer stack over heap when possible |

## Related Skills

- [native-memory-leaks.md](./native-memory-leaks.md) - Find leaks with profilers
- [native-turbo-modules.md](./native-turbo-modules.md) - Build memory-safe modules

---

## Reference: Native Platform Setup

# Skill: Platform Differences

Navigate iOS and Android tooling, dependency management, and build systems in React Native.

## Quick Reference

| Platform | IDE | Package Manager | Build System |
|----------|-----|-----------------|--------------|
| JavaScript | VS Code | npm/yarn/pnpm/bun | Metro |
| iOS | Xcode | CocoaPods | xcodebuild |
| Android | Android Studio | Gradle | Gradle |

```bash
# Common commands
bundle install                      # Install ruby bundler
cd ios && bundle exec pod install   # Install CocoaPods deps
cd android && ./gradlew clean       # Clean Android build
xed ios/                            # Open Xcode
```

## When to Use

- Setting up native development environment
- Adding native dependencies
- Debugging platform-specific issues
- Understanding build processes

## Dependency Management

### JavaScript (npm/yarn/pnpm/bun)

Infer package manager from lockfile: `package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `bun.lockb`.

### iOS (CocoaPods)

```bash
# Install pods after npm install
bundle install
cd ios && bundle exec pod install

# Key files
ios/Podfile           # Pod dependencies
ios/Pods/             # Installed pods (gitignored)
ios/*.xcworkspace     # Open this in Xcode (not .xcodeproj)
Gemfile               # Ruby/CocoaPods version
```


### Android (Gradle)

```bash
# Sync after adding dependencies
cd android && ./gradlew clean

# Key files
android/build.gradle           # Project-level config
android/app/build.gradle       # App dependencies
android/gradle.properties      # Build flags
android/gradlew                # Gradle wrapper
```

## Common Commands

```bash
# iOS
bundle install                         # Install ruby bundler
cd ios && bundle exec pod install      # Install pods
xcrun simctl list                      # List simulators

# Android  
cd android && ./gradlew clean          # Clean build
./gradlew tasks                        # List available tasks
./gradlew assembleRelease              # Build release APK

# React Native CLI
npx react-native start                 # Start Metro
npx react-native run-ios               # Run on iOS
npx react-native run-android           # Run on Android
npx react-native build-ios             # Build for iOS
npx react-native build-android         # Build for Android

# Expo
npx expo start                         # Start Metro (Expo)
npx expo run:ios                       # Run on iOS (dev client)
npx expo run:android                   # Run on Android (dev client)
npx expo prebuild                      # Generate native projects
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Pod install fails | `cd ios && bundle exec pod install --repo-update` |
| Xcode build fails | `cd ios && xcodebuild clean` |
| Android Gradle sync fails | `./gradlew clean` then sync |
| Can't find simulator | `xcrun simctl list` to verify name |
| Metro cache issues | `npx react-native start --reset-cache` |
| React Native cache issues | `npx react-native clean` |

## Related Skills

- [native-profiling.md](./native-profiling.md) - Use IDE profilers
- [native-turbo-modules.md](./native-turbo-modules.md) - Build native modules
- [upgrading-react-native.md](../../upgrading-react-native/references/upgrading-react-native.md) - Upgrade React Native safely

---

## Reference: Native Profiling

# Skill: Profile Native Code

Use Xcode Instruments and Android Studio Profiler to identify native performance bottlenecks.

## Quick Command

```bash
# iOS: Open Instruments
# Xcode → Open Developer Tool → Instruments → Time Profiler

# Android: Open Profiler
# Android Studio → View → Tool Windows → Profiler
```

## When to Use

- App is slow but JS profiler shows no issues
- Investigating native module performance
- Startup feels slow (native init)
- Battery drain concerns
- Need CPU/memory breakdown by thread

> **Note**: This skill involves interpreting visual profiler output (Xcode Instruments, Android Studio Profiler). AI agents cannot yet process screenshots autonomously. Use this as a guide while reviewing the profiler UI manually, or await MCP-based visual feedback integration (see roadmap).

## iOS Profiling with Xcode

### Quick Check: Debug Navigator

1. Run app via Xcode
2. Open Debug Navigator (side panel)
3. View real-time: CPU, Memory, Disk, Network

**CPU percentage can exceed 100%** (multi-core usage).

### Deep Profiling: Instruments

1. Open: **Xcode → Open Developer Tool → Instruments**
2. Select **Time Profiler**
3. Choose target device and app
4. Click record (red circle)
5. Perform actions in app
6. Stop recording

### Analyzing Time Profiler Results

**Key views:**
- **Flame Graph**: Visual call stack over time
- **Call Tree**: Hierarchical function breakdown
- **Ranked**: Functions sorted by time (Bottom-Up)

**Useful filters:**
- Hide System Libraries
- Invert Call Tree (bottom-up view)
- Filter by thread (main, JS, etc.)

**Identifying problems:**
- **Microhang**: Brief UI unresponsiveness
- **Hang**: Full UI thread block (critical)
- Yellow = most time spent

### Thread Breakdown

Pin threads to compare:
- **Main thread** (SampleApp): UI rendering
- **JavaScript thread**: React/JS execution
- **Background threads**: Native modules

**Pro tip**: JS thread blocking ≠ UI block (React Native design benefit).

## Android Profiling with Android Studio

### Launch Profiler

1. **View → Tool Windows → Profiler**
2. Or: Click "Profile" in toolbar

### CPU Profiling

1. Select **"Find CPU Hotspots"**
2. Click **"Start profiler task"**
3. Interact with app
4. Stop to analyze

### Analyzing Results

**Flame Graph:**
- Zoom with scroll/pinch
- Click to expand call stacks
- Filter by keyword (e.g., "hermes")

**Views:**
- **Top Down**: From entry points down
- **Bottom Up**: From slowest functions up
- **Flame Chart**: Timeline visualization

### Reading the Call Stack

Example analysis:
```
JS Thread activity after button press:
- Event handler on main thread
- Triggers JS work via sync JSI calls
- Hermes processes React reconciliation
- ~30% time in "commit" phase (Yoga layout)
```

## Code Example: What to Look For

### 5000 Views in ScrollView (Bad)

Profiler shows:
- 240ms+ JS thread work
- Many 1ms Hermes spikes
- Exceeds 16.6ms frame budget
- Result: Dropped frames, UI jank

### Using FlatList (Better)

Profiler shows:
- Minimal JS work (windowed rendering)
- Smooth main thread
- Stays within frame budget

## Platform Tools Summary

| Tool | Platform | Use Case |
|------|----------|----------|
| Time Profiler | iOS | CPU hotspots |
| Leaks | iOS | Memory leaks |
| Hangs | iOS | UI thread blocks |
| CPU Profiler | Android | CPU hotspots |
| Memory Profiler | Android | Memory tracking |
| Perfetto | Android | Advanced trace analysis |

## Perfetto (Advanced Android)

Export traces from Android Studio and analyze at [ui.perfetto.dev](https://ui.perfetto.dev/):

- Cross-process analysis
- Custom trace events
- Additional visualizations

## Pro Tips

1. **Profile on low-end devices**: Issues appear more clearly
2. **Use release builds**: Debug builds have overhead
3. **Compare before/after**: Export traces for comparison
4. **Filter by thread**: Focus on relevant work
5. **Look for patterns**: Spikes correlating with interactions

## Expo Notes

- **Expo Go**: Cannot profile native code directly; JS profiling only
- **Dev Client / Prebuild**: Full native profiling supported via Xcode/Android Studio
- Run `npx expo prebuild` to generate native projects, then profile as bare React Native

## Common Findings

| Symptom | Likely Cause |
|---------|--------------|
| Main thread hangs | Heavy UI work, blocked operations |
| JS thread spikes | React re-renders, heavy computation |
| Background thread busy | Native module work |
| Memory climbing | Leak (see memory profiling skills) |

## Related Skills

- [native-measure-tti.md](./native-measure-tti.md) - Profile startup specifically
- [native-memory-leaks.md](./native-memory-leaks.md) - Memory profiling
- [js-profile-react.md](./js-profile-react.md) - JS/React profiling

---

## Reference: Native Sdks Over Polyfills

# Skill: Native SDKs

Replace web polyfills and JS navigators with native React Native implementations for better performance.

## Quick Pattern

**Before (JS polyfills - 430+ KB):**

```tsx
import '@formatjs/intl-datetimeformat/polyfill';
import CryptoJS from 'crypto-js';
import { createStackNavigator } from '@react-navigation/stack';
```

**After (native implementations):**

```tsx
// Hermes has native Intl.DateTimeFormat - no polyfill needed
import { createHash } from 'react-native-quick-crypto';  // 58x faster
import { createNativeStackNavigator } from '@react-navigation/native-stack';
```

## When to Use

- Large JS bundle from polyfills
- Navigation feels non-native
- Crypto operations are slow
- Internationalization bloating bundle

## Step-by-Step Instructions

### 1. Remove Unnecessary Intl Polyfills

Hermes now supports many `Intl` APIs natively. Check your imports:

```tsx
// BEFORE: All these polyfills (430+ KB)
import '@formatjs/intl-getcanonicallocales/polyfill';
import '@formatjs/intl-locale/polyfill';
import '@formatjs/intl-numberformat/polyfill';
import '@formatjs/intl-numberformat/locale-data/en';
import '@formatjs/intl-datetimeformat/polyfill';
import '@formatjs/intl-datetimeformat/locale-data/en';
import '@formatjs/intl-pluralrules/polyfill';
import '@formatjs/intl-pluralrules/locale-data/en';
import '@formatjs/intl-relativetimeformat/polyfill';
import '@formatjs/intl-relativetimeformat/locale-data/en';
import '@formatjs/intl-displaynames/polyfill';
```

**Hermes Support (as of 2025):**

| API | Hermes | Keep Polyfill? |
|-----|--------|----------------|
| `Intl.Collator` | ✅ | No |
| `Intl.DateTimeFormat` | ✅ | No |
| `Intl.NumberFormat` | ✅ | No |
| `Intl.getCanonicalLocales()` | ✅ | No |
| `Intl.supportedValuesOf()` | ✅ | No |
| `Intl.Locale` | ❌ | Yes |
| `Intl.PluralRules` | ❌ | Yes |
| `Intl.RelativeTimeFormat` | ❌ | Yes |
| `Intl.DisplayNames` | ❌ | Yes |
| `Intl.ListFormat` | ❌ | Yes |
| `Intl.Segmenter` | ❌ | Yes |

```tsx
// AFTER: Only needed polyfills
import '@formatjs/intl-locale/polyfill';
import '@formatjs/intl-pluralrules/polyfill';
import '@formatjs/intl-pluralrules/locale-data/en';
import '@formatjs/intl-relativetimeformat/polyfill';
import '@formatjs/intl-relativetimeformat/locale-data/en';
import '@formatjs/intl-displaynames/polyfill';
```

### 2. Use Native Crypto

Replace JS crypto with native C++ implementation:

```bash
npm install react-native-quick-crypto
```

**Performance**: Up to 58x faster than `crypto-js`.

```tsx
// BEFORE: Slow JS implementation
import CryptoJS from 'crypto-js';

// AFTER: Native C++ implementation
import { createHash } from 'react-native-quick-crypto';
```

Essential for:
- Web3 wallet seed generation
- CSPRNG (Cryptographically Secure Random Numbers)
- Any heavy cryptographic operations

### 3. Use Native Stack Navigator

```bash
npm install @react-navigation/native-stack react-native-screens
```

```tsx
// BEFORE: JS-based stack (more flexible, less native)
import { createStackNavigator } from '@react-navigation/stack';
const Stack = createStackNavigator();

// AFTER: Native stack (native feel, better performance)
import { createNativeStackNavigator } from '@react-navigation/native-stack';
const Stack = createNativeStackNavigator();

// Usage is nearly identical
<Stack.Navigator>
  <Stack.Screen name="Home" component={HomeScreen} />
  <Stack.Screen name="Details" component={DetailsScreen} />
</Stack.Navigator>
```

**Benefits:**
- Native navigation animations
- Platform-specific headers (large titles on iOS)
- Lower memory usage
- Offloads work from JS thread

### 4. Use Native Bottom Tabs

```bash
npm install @bottom-tabs/react-navigation react-native-bottom-tabs
```

```tsx
// BEFORE: JS tabs
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
const Tabs = createBottomTabNavigator();

// AFTER: Native tabs
import { createNativeBottomTabNavigator } from '@bottom-tabs/react-navigation';
const Tabs = createNativeBottomTabNavigator();

<Tabs.Navigator>
  <Tabs.Screen name="Home" component={HomeScreen} />
  <Tabs.Screen name="Profile" component={ProfileScreen} />
</Tabs.Navigator>
```

## Recommended Native Libraries

| Category | Library | Description |
|----------|---------|-------------|
| Navigation | `react-native-screens` | Native screen containers |
| Menus | `zeego` | Native menus (Radix-like API) |
| Slider | `@react-native-community/slider` | Native slider |
| Date Picker | `react-native-date-picker` | Native date/time picker |
| Image | `react-native-fast-image` | Native image caching |

## Decision Matrix

| Scenario | Use Native? | Tradeoff |
|----------|-------------|----------|
| Standard navigation | ✅ Yes | Slight API differences |
| Custom transition animations | ⚠️ Maybe | Native is more limited |
| Platform-consistent UI | ✅ Yes | Less customization |
| Unique/branded design | ⚠️ Consider JS | Native may not support |

## Common Pitfalls

- **Assuming all polyfills needed**: Check Hermes compatibility first
- **Ignoring migration effort**: Native navigators have slightly different APIs
- **Over-customizing native components**: If design requires heavy customization, JS might be better

## Related Skills

- [bundle-analyze-js.md](./bundle-analyze-js.md) - Measure polyfill impact
- [bundle-library-size.md](./bundle-library-size.md) - Compare library sizes

---

## Reference: Native Threading Model

# Skill: Threading Model

Understand which threads Turbo Modules and Fabric use for initialization, method calls, and view updates.

## Quick Reference

| Action | iOS Thread | Android Thread |
|--------|------------|----------------|
| Module init | Main | JS (lazy) / Native (eager) |
| Sync method | JS | JS |
| Async method | Native modules | Native modules |
| View init/props | Main | Main |
| Yoga layout | JS | JS |

**Key rule**: Sync methods block JS thread. Keep under 16ms or make async.

## When to Use

- Building native modules
- Debugging threading issues
- Accessing UI from native code
- Understanding async vs sync method behavior

## Available Threads

| Thread | Name in Debugger | Purpose |
|--------|------------------|---------|
| Main/UI | Main thread | UI rendering, UIKit/Android Views |
| JavaScript | `mqt_v_js` | JS execution, React |
| Native Modules | `mqt_v_native` | Async Turbo Module calls |
| Custom | Various | Your background threads |

## Turbo Modules Threading

### Initialization

| Platform | Thread | Notes |
|----------|--------|-------|
| iOS | Main thread | Assumes UIKit access needed |
| Android (lazy) | JS thread | Default behavior |
| Android (eager) | Native modules thread | When `needsEagerInit = true` |

**iOS**: React Native runs `init` on main thread assuming UIKit access.

**Android Eager Loading:**

```kotlin
// ReactModuleInfo constructor params:
// canOverrideExistingModule, needsEagerInit, isCxxModule, isTurboModule
ReactModuleInfo(
    AwesomeModule.NAME,
    AwesomeModule.NAME,
    false,
    true,   // needsEagerInit = true → runs on native modules thread
    false,
    true
)
```

### Synchronous Method Calls

**Always run on JS thread** - blocks until return.

```swift
// iOS - runs on JS thread
@objc func multiply(_ a: Double, b: Double) -> NSNumber {
    // This blocks JS for entire duration!
    return a * b as NSNumber
}
```

**Danger**: Long sync operations freeze the app:

```swift
// BAD: Blocks JS for 20 seconds
@objc func multiply(_ a: Double, b: Double) -> NSNumber {
    Thread.sleep(forTimeInterval: 20)  // App frozen!
    return a * b as NSNumber
}
```

### Asynchronous Method Calls

**Run on Native Modules thread** - doesn't block JS.

```swift
// iOS - runs on mqt_v_native thread
@objc func asyncOperation(
    _ a: Double,
    resolve: @escaping RCTPromiseResolveBlock,
    reject: RCTPromiseRejectBlock
) {
    // Already on background thread
    resolve(a * 2)
}
```

```kotlin
// Android - runs on native modules thread
override fun asyncOperation(a: Double, promise: Promise?) {
    // Already on background thread
    promise?.resolve(a * 2)
}
```

### Module Invalidation

Called when React Native instance is torn down (e.g., Metro reload):

| Platform | Thread |
|----------|--------|
| iOS | Native modules thread |
| Android | ReactHost thread pool |

**iOS**: Implement `RCTInvalidating` protocol.

## Fabric (Native Views) Threading

### View Lifecycle

| Operation | Thread |
|-----------|--------|
| View init | Main thread |
| Prop updates | Main thread |
| Layout (Yoga) | JS thread |

Views always manipulate UI on main thread (UIKit/Android requirement).

### Yoga Layout

Layout calculations happen on JS thread:

```
JS Thread: Calculate Yoga tree → Shadow tree
Main Thread: Apply layout to native views
```

## Moving Work to Background

### iOS: DispatchQueue

```swift
@objc func heavyWork(
    resolve: @escaping RCTPromiseResolveBlock,
    reject: RCTPromiseRejectBlock
) {
    DispatchQueue.global().async {
        // Heavy computation here
        let result = self.compute()
        resolve(result)
    }
}
```

### Android: Coroutines

```kotlin
class MyModule(reactContext: ReactApplicationContext) :
    NativeMyModuleSpec(reactContext) {
    
    private val moduleScope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    
    override fun heavyWork(promise: Promise?) {
        moduleScope.launch {
            // Heavy computation here
            val result = compute()
            promise?.resolve(result)
        }
    }
    
    override fun invalidate() {
        super.invalidate()
        moduleScope.cancel()  // Important: cancel to prevent leaks
    }
}
```

## Thread Safety Checklist

| Scenario | Safe? | Solution |
|----------|-------|----------|
| Sync method accessing shared state | ⚠️ | Use locks/synchronized |
| Async method accessing UI | ❌ | Dispatch to main thread |
| Multiple async calls to same resource | ⚠️ | Queue or mutex |
| Accessing JS from background | ❌ | Use CallInvoker |

### Accessing UI from Background (iOS)

```swift
DispatchQueue.global().async {
    let result = self.heavyComputation()
    
    DispatchQueue.main.async {
        // Safe to update UI here
        self.updateUI(with: result)
    }
}
```

### Accessing UI from Background (Android)

```kotlin
moduleScope.launch(Dispatchers.Default) {
    val result = heavyComputation()
    
    withContext(Dispatchers.Main) {
        // Safe to update UI here
        updateUI(result)
    }
}
```

## Summary Table

| Action | iOS Thread | Android Thread |
|--------|------------|----------------|
| Module init | Main | JS (lazy) / Native (eager) |
| Sync method | JS | JS |
| Async method | Native modules | Native modules |
| View init | Main | Main |
| Prop update | Main | Main |
| Yoga layout | JS | JS |
| Invalidate | Native modules | ReactHost pool |

## Related Skills

- [native-turbo-modules.md](./native-turbo-modules.md) - Implement background threads
- [native-profiling.md](./native-profiling.md) - Debug thread issues

---

## Reference: Native Turbo Modules

# Skill: Fast Native Modules

Build performant Turbo Modules using modern languages and background threading.

## Quick Pattern

**Incorrect (sync method blocks JS thread):**

```swift
@objc func heavyWork() -> NSNumber {
    Thread.sleep(forTimeInterval: 2)  // Blocks JS for 2s!
    return 42
}
```

**Correct (async on background thread):**

```swift
@objc func heavyWork(
    resolve: @escaping RCTPromiseResolveBlock,
    reject: RCTPromiseRejectBlock
) {
    DispatchQueue.global().async {
        let result = self.compute()
        resolve(result)
    }
}
```

## When to Use

- Creating new native modules
- Optimizing existing module performance
- Heavy computation needs to run off JS thread
- Cross-platform C++ code needed

## Prerequisites

- React Native Builder Bob for scaffolding

```bash
npx create-react-native-library@latest my-library
```

## Step-by-Step Instructions

### 1. Scaffold with Builder Bob

```bash
npx create-react-native-library@latest awesome-library
# Follow prompts: choose Turbo Module, select languages
```

Creates ready-to-publish library with:
- iOS (Obj-C/Swift) support
- Android (Kotlin) support
- TypeScript definitions
- Codegen setup

For local modules:

```bash
npx create-react-native-library@latest awesome-library --local
```

### 2. Enable Swift in iOS Module

Update `awesome-library.podspec`:

```diff
- s.source_files = "ios/**/*.{h,m,mm,cpp}"
+ s.source_files = "ios/**/*.{h,m,mm,cpp,swift}"
```

Create Swift file in Xcode (accept bridging header prompt).

Update header file for Swift compatibility:

```objc
// AwesomeLibrary.h
#import <Foundation/Foundation.h>

#if __cplusplus
#import "ReactCodegen/RNAwesomeLibrarySpec/RNAwesomeLibrarySpec.h"
#endif

@interface AwesomeLibrary : NSObject
#if __cplusplus
<NativeAwesomeLibrarySpec>
#endif
@end
```

Import header in bridging header:

```objc
// AwesomeLibrary-Bridging-Header.h
#import "AwesomeLibrary.h"
```

Implement in Swift:

```swift
// AwesomeLibrary.swift
import Foundation

extension AwesomeLibrary {
    @objc func multiply(_ a: Double, b: Double) -> NSNumber {
        return (a * b) as NSNumber
    }
}
```

Bridge in Obj-C++:

```objc
// AwesomeLibrary.mm
#import "AwesomeLibrary.h"

#if __has_include("awesome_library/awesome_library-Swift.h")
#import "awesome_library/awesome_library-Swift.h"
#else
#import "awesome_library-Swift.h"
#endif

@implementation AwesomeLibrary
RCT_EXPORT_MODULE()
RCT_EXTERN_METHOD(multiply:(double)a b:(double)b);
@end
```

### 3. Run on Background Thread (iOS)

```swift
@objc func heavyOperation(
    _ input: Double,
    resolve: @escaping RCTPromiseResolveBlock,
    reject: RCTPromiseRejectBlock
) {
    DispatchQueue.global().async {
        // Heavy work on background thread
        let result = self.expensiveComputation(input)
        resolve(result)
    }
}
```

### 4. Run on Background Thread (Android)

```kotlin
class AwesomeLibraryModule(reactContext: ReactApplicationContext) :
    NativeAwesomeLibrarySpec(reactContext) {
    
    private val moduleScope = CoroutineScope(Dispatchers.Default + SupervisorJob())
    
    override fun heavyOperation(input: Double, promise: Promise?) {
        moduleScope.launch {
            // Heavy work on coroutine
            val result = expensiveComputation(input)
            promise?.resolve(result)
        }
    }
    
    override fun invalidate() {
        super.invalidate()
        moduleScope.cancel()  // Prevent memory leaks!
    }
}
```

### 5. Use C++ for Cross-Platform Code

Create C++ Turbo Module for shared logic:

```cpp
// MyCppModule.h
#pragma once

#include <ReactCommon/TurboModule.h>

namespace facebook::react {

class MyCppModule : public TurboModule {
public:
    MyCppModule(std::shared_ptr<CallInvoker> jsInvoker);
    
    double multiply(double a, double b);
};

} // namespace facebook::react
```

Register for iOS auto-linking:

```objc
// MyCppModuleRegistration.mm
#include <ReactCommon/CxxTurboModuleUtils.h>

@implementation MyCppModuleRegistration

+ (void)load {
    facebook::react::registerCxxModuleToGlobalModuleMap(
        std::string(facebook::react::MyCppModule::kModuleName),
        [&](std::shared_ptr<facebook::react::CallInvoker> jsInvoker) {
            return std::make_shared<facebook::react::MyCppModule>(jsInvoker);
        }
    );
}

@end
```

## Threading Summary

| Method Type | Default Thread | Best Practice |
|-------------|----------------|---------------|
| Sync | JS thread | Keep fast (<16ms) |
| Async | Native modules thread | OK for moderate work |
| Heavy async | Custom background | Use DispatchQueue/Coroutines |

## Language Interop Costs

| Interface | Overhead | Notes |
|-----------|----------|-------|
| Obj-C ↔ C++ | ~0 | Compile-time |
| Swift ↔ C++ | ~0 | Swift 5.9+ interop |
| Kotlin ↔ C++ (JNI) | Medium | Per-call lookup |
| C++ Turbo Module | Low | JSI direct access |

**Tip**: C++ Turbo Modules skip JNI at runtime since JS holds direct C++ function references via JSI.

## Code Example: Complete Async Operation

```typescript
// TypeScript interface
export interface Spec extends TurboModule {
    multiply(a: number, b: number): number;  // Sync
    heavyOperation(input: number): Promise<number>;  // Async
}
```

```kotlin
// Android implementation
override fun heavyOperation(input: Double, promise: Promise?) {
    moduleScope.launch {
        try {
            val result = withContext(Dispatchers.Default) {
                // Simulate heavy work
                delay(1000)
                input * 2
            }
            promise?.resolve(result)
        } catch (e: Exception) {
            promise?.reject("ERROR", e.message)
        }
    }
}
```

```swift
// iOS implementation
@objc func heavyOperation(
    _ input: Double,
    resolve: @escaping RCTPromiseResolveBlock,
    reject: @escaping RCTPromiseRejectBlock
) {
    DispatchQueue.global(qos: .userInitiated).async {
        // Simulate heavy work
        Thread.sleep(forTimeInterval: 1.0)
        let result = input * 2
        resolve(result)
    }
}
```

## Common Pitfalls

- **Sync methods that block**: Keep under 16ms or make async
- **Forgetting to cancel coroutine scope**: Causes memory leaks
- **Not handling errors in async**: Always try/catch with reject
- **Accessing UI from background**: Dispatch to main thread

## Related Skills

- [native-threading-model.md](./native-threading-model.md) - Thread details
- [native-memory-patterns.md](./native-memory-patterns.md) - Memory in native code

---

## Reference: Native View Flattening

# Skill: View Flattening

Understand and debug React Native's view flattening optimization.

## Quick Pattern

**Problem (children get flattened unexpectedly):**

```jsx
<NativeTabBar>
  <Tab1 />  // May be flattened, breaking native component
  <Tab2 />
</NativeTabBar>
```

**Solution (prevent flattening):**

```jsx
<NativeTabBar>
  <Tab1 collapsable={false} />
  <Tab2 collapsable={false} />
</NativeTabBar>
```

## When to Use

- Native component receives unexpected number of children
- Layout debugging with native components
- Building native components that accept children
- Understanding React Native rendering

> **Note**: This skill involves interpreting visual view hierarchy tools (Xcode Debug View Hierarchy, Android Layout Inspector). AI agents cannot yet process screenshots autonomously. Use this as a guide while reviewing the hierarchy manually, or await MCP-based visual feedback integration (see roadmap).

## What is View Flattening?

React Native's renderer automatically removes "layout-only" views that:
- Only affect layout (no visual rendering)
- Don't need to exist in native view hierarchy

**Benefits**: Reduced memory, faster rendering, shallower view tree.

## The Problem with Native Components

```tsx
// You expect 3 children
<MyNativeComponent>
  <Child1 />
  <Child2 />
  <Child3 />
</MyNativeComponent>
```

If `Child1` is flattened, its internal views become direct children:

```tsx
// Native side receives 5 views instead of 3!
<MyNativeComponent>
  <View />   // Was inside Child1
  <View />   // Was inside Child1  
  <View />   // Was inside Child1
  <Child2 />
  <Child3 />
</MyNativeComponent>
```

## Preventing Flattening with `collapsable`

```tsx
<MyNativeComponent>
  <Child1 collapsable={false} />
  <Child2 collapsable={false} />
  <Child3 collapsable={false} />
</MyNativeComponent>
```

Now native side always receives exactly 3 children.

## Debugging View Hierarchy

<!-- image: View Hierarchy Flattening -->

Use native debugging tools to see the actual view hierarchy:

### Xcode (iOS)

1. Run app via Xcode
2. Click **"Debug View Hierarchy"** in debug toolbar (shown in image)
3. Inspect 3D view of native hierarchy

**React Native components map to:**
- `<View />` → `RCTViewComponentView`
- `<Text />` → `RCTTextView`

### Android Studio

1. Run app via Android Studio
2. **View → Tool Windows → Layout Inspector**
3. Select running process

**React Native components map to:**
- `<View />` → `ReactViewGroup`
- `<Text />` → `ReactTextView`

## Code Examples

### When Flattening Breaks Your Component

```tsx
// Your native component expects exactly 2 tabs
const NativeTabBar = requireNativeComponent('RCTTabBar');

// BAD: TabContent might get flattened
const MyTabs = () => (
  <NativeTabBar>
    <TabContent title="Home">
      <View><Text>Home content</Text></View>
    </TabContent>
    <TabContent title="Profile">
      <View><Text>Profile content</Text></View>
    </TabContent>
  </NativeTabBar>
);

// GOOD: Prevent flattening
const MyTabs = () => (
  <NativeTabBar>
    <TabContent title="Home" collapsable={false}>
      <View><Text>Home content</Text></View>
    </TabContent>
    <TabContent title="Profile" collapsable={false}>
      <View><Text>Profile content</Text></View>
    </TabContent>
  </NativeTabBar>
);
```

### Wrapper Component with collapsable

```tsx
// Wrapper that prevents flattening
const NativeChildWrapper = ({ children, ...props }) => (
  <View collapsable={false} {...props}>
    {children}
  </View>
);

// Usage
<NativeComponent>
  <NativeChildWrapper>
    <ComplexChild />
  </NativeChildWrapper>
</NativeComponent>
```

## When Views Get Flattened

Views are considered "layout-only" when they:
- Have no `backgroundColor`
- Have no `borderWidth`, `borderColor`
- Have no `shadowColor`, `elevation`
- Don't handle events (no `onPress`, etc.)
- Don't use `opacity` < 1
- Don't have `overflow: 'hidden'`

## Forcing a View to Stay

Besides `collapsable={false}`, these also prevent flattening:

```tsx
// Any of these prevent flattening
<View style={{ backgroundColor: 'transparent' }} />
<View style={{ borderWidth: 0.01 }} />
<View style={{ opacity: 0.99 }} />
<View onLayout={() => {}} />
```

But `collapsable={false}` is the cleanest solution.

## Debugging Checklist

1. **Check native child count**: Log received children in native code
2. **Use Layout Inspector**: Visual hierarchy debugging
3. **Add collapsable={false}**: Test if flattening is the issue
4. **Check wrapper components**: Intermediate views may be flattened

## Common Pitfalls

- **Assuming JS children = native children**: Flattening changes this
- **Not documenting native component requirements**: If your native component expects specific child count, document it
- **Over-using collapsable={false}**: Only use when necessary (loses optimization benefits)

## Related Skills

- [native-platform-setup.md](./native-platform-setup.md) - IDE setup for debugging
- [native-profiling.md](./native-profiling.md) - Performance impact analysis
