---
title: "Winui App"
description: "Bootstrap, develop, and design modern WinUI 3 desktop applications with C# and the Windows App SDK using official Microsoft guidance, WinUI Gallery patterns, Windows App SDK samples, and CommunityToolkit components. Use when creating a brand new a..."
category: "development"
source: "community"
author: "Community"
tags: ["winui", "app"]
date: 2026-03-20
---

# WinUI App

Use this skill for WinUI 3 and Windows App SDK work that needs grounded setup guidance, app bootstrap, modern Windows UX decisions, or concrete implementation patterns.

## Required Flow

1. Classify the task as environment/setup, new-app bootstrap, design, implementation, review, or troubleshooting.
2. If the task is about preparing a machine for WinUI, auditing readiness, or creating a brand new app, start with the bundled setup-and-scaffold flow in this skill before broader design, implementation, or troubleshooting work:
   - Pick the app name when the request is for a new app.
   - Use the exact name the user gave when it is already a safe folder name.
   - If the user did not give a name, derive a short PascalCase name from the request and state what you chose.
   - Create the project in the user's current workspace unless they asked for another location.
   - Do not use `--force` unless the user explicitly asked to overwrite existing files.
   - Run the bundled WinGet configuration from the skill directory so the relative path stays exactly `config.yaml`:

```powershell
winget configure -f config.yaml --accept-configuration-agreements --disable-interactivity
```

   - Treat the configuration as intended to enable Developer Mode, install or update Visual Studio Community 2026, and install the Managed Desktop, Universal, and Windows App SDK C# components needed for WinUI development.
   - Assess the configuration result before continuing. Continue on success. If it fails, inspect the output instead of guessing. If the `winui` template is already available and the toolchain is usable, note the partial failure and continue. If prerequisites are still missing, stop and report the blocker clearly.
   - Verify the template is available before scaffolding:

```powershell
dotnet new list winui
```

   - For diagnostics-only environment requests, explain that the bundled bootstrap may change the machine and get confirmation before running it. If the user declines changes, use the manual verification guidance in `references/foundation-environment-audit-and-remediation.md` and summarize readiness under `present`, `missing`, `uncertain`, and `recommended optional tools`.
   - For a brand new app, scaffold with `dotnet new winui -o <name>`. Add template options only when the user asked for them. Supported options: `-f|--framework net10.0|net9.0|net8.0`, `-slnx|--use-slnx`, `-cpm|--central-pkg-mgmt`, `-mvvm|--use-mvvm`, `-imt|--include-mvvm-toolkit`, `-un|--unpackaged`, `-nsf|--no-solution-file`, `--force`. Do not invent unsupported flags. If the user asks for packaged behavior, pass `--unpackaged false`. Otherwise keep the template default.
   - Verify a new scaffold by confirming the expected project file exists and running `dotnet build` against the generated `.csproj`.
   - Launch a newly scaffolded app through the correct path for its actual packaging model and confirm there is a real top-level window instead of relying only on the launcher process exit code.
3. Read `references/_sections.md`, then load only the reference files that match the task.
4. Make the packaging model explicit before creating or refactoring the app. Default to packaged for Store-like product workflows and Visual Studio deploy/F5 flows. Default to unpackaged when the user expects repeatable CLI build-and-run loops or direct `.exe` launches after each change.
5. When the task is an opaque XAML compiler failure such as `MSB3073` or `XamlCompiler.exe`, read `references/foundation-template-first-recovery.md` and simplify back toward the current `dotnet new winui` scaffold for the chosen packaging model before inventing custom recovery structure.
6. For any work that creates or changes a WinUI app, make a complete but minimal edit set, then build the app and run it before responding to the user. Do this by default even when the user did not explicitly ask for verification. If a running app instance locks the output while more work remains, stop it, rebuild, relaunch, and continue verification. When the work is complete and launch verification succeeds, leave the final verified app instance running for the user unless they explicitly asked you not to.
7. Treat launch verification as incomplete until the app shows objective success signals such as a responsive top-level window, expected window title, or other clear startup behavior. A spawned process by itself is not enough.
8. Prefer Microsoft Learn for requirements, API expectations, and platform guidance.
9. Prefer WinUI Gallery for concrete control usage, shell composition, and design details.
10. Prefer WindowsAppSDK-Samples for scenario-level APIs such as windowing, lifecycle, notifications, deployment, and custom controls.
11. Build toward WinUI and Fluent guidance first. Treat native WinUI shells, controls, interactions, and control chrome as the default implementation path.
12. For grouped command surfaces such as document actions, editor formatting, view toggles, or page-level toolbars, favor a native `CommandBar` or other stock WinUI command surface before building a custom row with `Grid`, `StackPanel`, `Border`, or ad hoc button groupings.
13. Do not invent app-specific controls, bespoke component libraries, or custom chrome to replace stock WinUI behavior unless the user explicitly asks for that customization, the existing product design system already requires it, or a verified platform gap leaves no clean native option.
14. When customization is needed, first compose, template, or restyle built-in WinUI controls and system resources before adding CommunityToolkit dependencies or authoring a new custom control.
15. Use CommunityToolkit only when built-in WinUI controls or helpers do not cover the need cleanly.
16. Support both light and dark mode by default. Treat single-theme output as an exception that requires an explicit user request or an existing product constraint.
17. Use theme-aware resources, system brushes, and WinUI styling hooks instead of hard-coded light-only or dark-only colors when building or revising UI.
18. Make scroll ownership explicit for collection layouts. When a page already scrolls vertically, do not assume a nested `GridView` or other scroll-owning collection will still render a horizontal poster rail correctly.
19. Do not add extra `Border` wrappers around sections, lists, or cards unless the border is doing distinct work that the contained control or parent surface does not already provide. Avoid "double-card" compositions where a section `Border` wraps child items that already render as cards.
20. Treat responsiveness as a shell-plus-page problem, not only a control-resize problem. Plan explicit wide, medium, and phone-width behavior for navigation, padding, content density, and footer/tool regions, and simplify or hide nonessential UI as width shrinks.

## Common Routes

| Request | Read first |
| --- | --- |
| Check whether this PC can build WinUI apps | `references/foundation-environment-audit-and-remediation.md` |
| Install missing WinUI prerequisites | `references/foundation-environment-audit-and-remediation.md` |
| Start a new packaged or unpackaged app | `references/foundation-setup-and-project-selection.md` |
| Recover from opaque XAML compiler or startup failures while staying anchored to the template scaffold | `references/foundation-template-first-recovery.md` |
| Build, run, or verify that a WinUI app actually launched | `references/build-run-and-launch-verification.md` |
| Review app structure, pages, resources, and bindings | `references/foundation-winui-app-structure.md` |
| Choose shell, navigation, title bar, or multi-window patterns | `references/shell-navigation-and-windowing.md` |
| Choose controls or responsive layout patterns | `references/controls-layout-and-adaptive-ui.md` |
| Apply Mica, theming, typography, icons, or Fluent styling | `references/styling-theming-materials-and-icons.md` |
| Improve accessibility, keyboarding, or localization | `references/accessibility-input-and-localization.md` |
| Diagnose responsiveness or UI-thread performance | `references/performance-diagnostics-and-responsiveness.md` |
| Decide whether to use CommunityToolkit | `references/community-toolkit-controls-and-helpers.md` |
| Handle lifecycle, notifications, or deployment | `references/windows-app-sdk-lifecycle-notifications-and-deployment.md` |
| Run a review checklist | `references/testing-debugging-and-review-checklists.md` |

## Environment Rules

- Do not guess whether the machine is ready for WinUI development. Verify it.
- Use the bundled setup-and-scaffold flow in this skill for fresh setup, remediation, and first-project scaffolding instead of delegating to another skill.
- Treat `config.yaml` in this skill directory as the bundled bootstrap source of truth.
- Treat uncertain environment signals as uncertain, not as success.
- If the task is audit-only and the user declines machine changes, use the manual verification guidance in `references/foundation-environment-audit-and-remediation.md` and keep uncertain signals explicit instead of implying success.
- If `config.yaml` is missing, say so clearly and fall back to the official Microsoft workflow instead of pretending the bundled path exists.
- Keep environment readiness, packaging choice, and application startup verification as separate checks. Passing one does not prove the others.
- Fail closed on ambiguous launch results. If the app did not clearly open, keep debugging.
- After creating or editing a WinUI app, do not stop at a successful build. Launch the app, confirm objective startup behavior, and leave the final verified app instance running before returning control to the user unless they explicitly say not to run it.

## Reference Rules

- Keep C# as the primary path. Mention C++ or C++/WinRT only when the difference is material.
- Preserve the conventions of an existing codebase instead of forcing a generic sample structure onto it.
- Treat WinUI design guidance and native controls as the baseline. Do not drift into bespoke component systems or app-specific replacements for standard controls unless the user explicitly requests them or the existing codebase already depends on them.
- Support light and dark mode by default for app UI work unless the user explicitly asks for a single-theme result or the product already enforces one.
- Favor built-in WinUI controls and system styling hooks before adding CommunityToolkit dependencies, custom controls, or app-specific surface systems.
- Put detailed control, theming, shell, scrolling, responsiveness, packaging, and recovery guidance in the matching reference files instead of duplicating those rules here.

---

## Reference: _Sections

# Reference Sections

Use this index to choose the narrowest reference file that fits the current task.

## 1. Foundations

- `foundation-setup-and-project-selection.md`
  - Priority: CRITICAL
  - Use for first-project setup, packaged vs unpackaged decisions, and core WinUI prerequisites.
  - Authority: Microsoft Learn WinUI and Windows App SDK setup docs.

- `foundation-environment-audit-and-remediation.md`
  - Priority: CRITICAL
  - Use for machine readiness checks, missing prerequisites, and guided remediation.
  - Authority: Microsoft Learn setup and system requirements docs, plus the bundled bootstrap workflow.

- `foundation-winui-app-structure.md`
  - Priority: HIGH
  - Use for solution layout, shell composition, resources, bindings, and C#-first project structure.
  - Authority: WinUI Gallery source plus Learn XAML guidance.

- `foundation-template-first-recovery.md`
  - Priority: CRITICAL
  - Use for opaque `MSB3073`, `XamlCompiler.exe`, and startup failures that should be recovered by comparing against a fresh `dotnet new winui` scaffold instead of applying alternate baseline files.
  - Authority: Learn packaged and unpackaged deployment guidance plus recurring template-first recovery patterns.

- `build-run-and-launch-verification.md`
  - Priority: CRITICAL
  - Use for build/run workflows, actual launch verification, startup crashes, and packaged-vs-unpackaged local execution choices.
  - Authority: Learn setup and deployment guidance plus recurring WinUI troubleshooting patterns.

## 2. Shell, Navigation, and Windowing

- `shell-navigation-and-windowing.md`
  - Priority: HIGH
  - Use for `NavigationView`, page shells, title bars, `AppWindow`, and multi-window design.
  - Authority: Learn design guidance, WinUI Gallery samples, Windows App SDK Windowing samples.

## 3. Controls, Layout, and Adaptive UI

- `controls-layout-and-adaptive-ui.md`
  - Priority: HIGH
  - Use for control selection, command surfaces, responsive layout, and page composition.
  - Authority: Learn design guidance and WinUI Gallery control pages.

## 4. Styling, Theming, Materials, and Icons

- `styling-theming-materials-and-icons.md`
  - Priority: HIGH
  - Use for Fluent styling, theme resources, Mica, Acrylic, typography, and iconography.
  - Authority: Learn design/material docs, WinUI Gallery backdrop samples, Windows App SDK Mica samples.

- `motion-animations-and-polish.md`
  - Priority: MEDIUM
  - Use for transitions, connected animation, subtle polish, and animation discipline.
  - Authority: Learn motion guidance, WinUI Gallery transition samples, CommunityToolkit animations.

## 5. Accessibility, Input, and Localization

- `accessibility-input-and-localization.md`
  - Priority: HIGH
  - Use for keyboarding, Narrator, high contrast, automation properties, and localization concerns.
  - Authority: Learn accessibility and globalization guidance, WinUI Gallery automation patterns.

## 6. Performance and Diagnostics

- `performance-diagnostics-and-responsiveness.md`
  - Priority: HIGH
  - Use for UI-thread responsiveness, large item collections, rendering cost, and diagnostic tooling.
  - Authority: Learn WinUI performance docs and XAML frame analysis guidance.

## 7. Windows App SDK Scenarios

- `windows-app-sdk-lifecycle-notifications-and-deployment.md`
  - Priority: HIGH
  - Use for lifecycle, activation, notifications, packaged vs unpackaged deployment, and runtime initialization.
  - Authority: Microsoft Learn Windows App SDK docs and WindowsAppSDK-Samples.

## 8. CommunityToolkit Extensions

- `community-toolkit-controls-and-helpers.md`
  - Priority: MEDIUM
  - Use when built-in WinUI controls are not enough and Toolkit packages might close the gap cleanly.
  - Authority: CommunityToolkit/Windows packages and samples.

## 9. Testing, Debugging, and Review

- `testing-debugging-and-review-checklists.md`
  - Priority: HIGH
  - Use for final review passes, debugging workflows, and validation checklists.
  - Authority: Learn tooling docs plus recurring WinUI review patterns.

- `sample-source-map.md`
  - Priority: MEDIUM
  - Use when you need to know which canonical repo or doc to inspect first for a given task.
  - Authority: Curated map across Learn, WinUI Gallery, WindowsAppSDK-Samples, and CommunityToolkit.

---

## Reference: Accessibility Input And Localization

## What This Reference Is For

Use this file for keyboard accessibility, Narrator support, automation properties, input parity, high contrast, and localization-ready UI.

## Prefer

- Accessible names, help text, and landmarks for meaningful UI elements.
- Full keyboard reachability for the main workflow.
- High-contrast-safe visuals.
- Localizable strings and layouts that tolerate growth.
- Equal support for mouse, touch, pen, and keyboard where the platform expects it.

## Avoid

- Icon-only interactions without accessible naming.
- Focus traps, hidden tab stops, or keyboard-only dead ends.
- Hard-coded strings in XAML or code-behind that block localization.
- Text layouts that collapse when strings expand.

## Guidance

- Use automation properties intentionally.
- Preserve visible focus and logical tab order.
- Verify context menus, flyouts, and dialogs by keyboard as well as mouse.
- Respect text scaling, contrast changes, and RTL where relevant.
- Keep touch targets and spacing usable on both mouse and touch hardware.

## WinUI Gallery Anchors

- Accessibility-related control samples
- Automation helper patterns in shell code
- Standard WinUI controls that already expose useful accessibility behavior

## Review Checklist

- Can a keyboard-only user complete the task?
- Does Narrator have enough information to describe the important UI?
- Does the experience stay legible in high contrast?
- Are strings and layout ready for localization and RTL growth?

---

## Reference: Build Run And Launch Verification

## What This Reference Is For

Use this file when the task involves building, running, launch failures, startup crashes, or final verification that a WinUI app actually opens on the current machine.

## Required Workflow

1. Identify the real build target:
   - solution or project file
   - configuration
   - platform
   - packaged or unpackaged model
2. Build after each meaningful code edit and again at task completion.
3. Run the app after changes when feasible. Always do it when the user asked for it or when startup, navigation, resources, or packaging changed.
4. Use the launch path that matches the deployment model:
   - packaged local dev: normally Visual Studio deploy or another package-aware flow
   - unpackaged local dev: normally the built executable the user will actually run
5. Verify real launch with objective evidence such as:
   - non-zero main window handle
   - expected window title
   - responsive process with visible shell
   - no immediate startup exception or crash
6. After completing app work, including a first scaffold or a later build-and-fix cycle, leave a successfully verified final app instance running so the user can see that it worked unless they explicitly asked you not to.
7. If launch fails or verification is ambiguous, debug the failure before saying the app is ready.

## Packaged vs Unpackaged Rules

- Choose one model intentionally before wiring startup, persistence, and launch instructions.
- Packaged apps can rely on package identity and package-backed storage.
- Unpackaged apps must not assume package identity. Guard or replace APIs that require it.
- APIs such as `Windows.Storage.ApplicationData.Current` can fail in unpackaged runs even when the build succeeds.
- Do not mix packaged-only assumptions into an unpackaged startup path.

## Build and Launch Guidance

- Prefer explicit platform targets when WinUI output is sensitive to architecture defaults. If `AnyCPU` creates ambiguity, use `x64` for local verification.
- For unpackaged verification, prefer launching the built `.exe` from `bin\Debug\...\win-x64\` or the project-specific output path.
- After a successful final launch verification, do not immediately tear the app down just because verification succeeded; keep it open for the user unless it blocks the next required action.
- If `dotnet run` throws bootstrapper, deployment, or COM activation errors, treat that as a signal that the chosen launch path or packaging setup is wrong for the current app.
- Stop old app instances before rebuilding if they can lock output files.

## Debugging Startup Failures

- Separate environment problems from app-code startup crashes.
- If the app exits before showing a window, inspect the startup path first:
  - `App.xaml`
  - merged resource dictionaries
  - converters
  - `MainWindow`
  - services used during startup
- For startup or manifest issues, compare the current app against a fresh `dotnet new winui` scaffold for the same packaging model before broader surgery.
- For opaque `MSB3073` and `XamlCompiler.exe` failures, simplify back toward the template-generated startup and shared-resource shape before making further structural changes.
- Restore complex startup pieces incrementally when the failure point is unclear. A minimal `App.xaml` plus minimal `MainWindow` is a valid isolation step.
- If the diagnostics look stale or inconsistent with the current files, run a clean build once before deeper surgery.
- Prefer restoring the last known-good template-based shared-resource state over moving styles inline as the long-term fix.
- When using unpackaged startup, review persistence, notifications, storage, and activation code for hidden package-identity assumptions.

## Exit Criteria

- Build succeeds from the intended local workflow.
- The app launches from the intended local workflow.
- A real top-level window or equivalent expected UI is confirmed.
- No unresolved startup exception remains.

---

## Reference: Community Toolkit Controls And Helpers

## What This Reference Is For

Use this file when deciding whether the Windows Community Toolkit should be added to a WinUI 3 app.

## Prefer

- Platform controls first.
- Targeted Toolkit package additions for clear gaps such as richer settings surfaces, segmented controls, or focused animation helpers.
- The smallest package set that solves the problem.

## Avoid

- Adding Toolkit packages because they look convenient without checking whether WinUI already covers the need.
- Pulling in multiple Toolkit packages for a minor visual difference.
- Hiding fundamental UX problems behind a new dependency.

## Good Candidate Areas

- `SettingsControls`
  - useful for settings surfaces and cards
- `Segmented`
  - useful when segmented selection is clearer than a tab or radio cluster
- `HeaderedControls`
  - useful for labeled control groupings
- `Animations`
  - useful when built-in transitions are not enough
- helpers and extensions
  - useful when they reduce repetitive WinUI plumbing cleanly

## Package Guidance

- Prefer WinUI 3 compatible Toolkit packages.
- Add only what the app will actually use.
- Document why a Toolkit dependency was added and what built-in alternative was rejected.

## Sample and Source Anchors

- CommunityToolkit `components/SettingsControls`
- CommunityToolkit `components/Segmented`
- CommunityToolkit `components/HeaderedControls`
- Toolkit animations and helper packages

## Review Checklist

- Does built-in WinUI already solve the problem?
- Is the dependency narrowly scoped and justified?
- Does the new control match the rest of the app’s design language?
- Will the package meaningfully reduce custom code or improve UX?

---

## Reference: Controls Layout And Adaptive Ui

## What This Reference Is For

Use this file when choosing controls, composing pages, or making a WinUI layout adapt well to different window sizes and input modes.

## Prefer

- Built-in WinUI controls first.
- Native command surfaces such as `CommandBar` when the UI is grouping actions, toggles, and lightweight tool controls.
- Standard controls for common tasks: `TextBox`, `NumberBox`, `ComboBox`, `ListView`, `GridView`, `ContentDialog`, `InfoBar`, `TeachingTip`, `TabView`, `NavigationView`.
- Explicit scroll ownership for collection layouts. If the page already scrolls vertically, prefer giving a media shelf its own horizontal `ScrollViewer` and a simple horizontal panel.
- Responsive techniques such as reposition, resize, reflow, and show/hide.
- Layouts that remain usable when the window becomes narrow.
- A real phone-width plan when the app may be resized that far: fewer columns, reduced padding, simplified controls, and stacked content instead of compressed desktop rails.

## Avoid

- Replacing standard WinUI controls with custom controls just to change appearance.
- Building custom toolbar rows out of generic layout panels when a stock `CommandBar` would cover the grouping cleanly.
- Hard-coded sizes that only look correct at one window width.
- Dense desktop-only layouts that break touch or keyboard workflows.
- Adding extra controls for local filtering or sorting when live updates and a simpler layout would better match the workflow.
- Nesting a scroll-owning `GridView` inside an outer page `ScrollViewer` without deciding which control owns scrolling; this often produces a single vertical column or awkward scroll conflicts instead of a horizontal media shelf.
- Wrapping list sections or card groups in an extra `Border` when the section header, spacing, and child surfaces already establish grouping.

## Control Selection Guidance

- Forms and settings:
  - Prefer native controls first; add Toolkit settings controls only if the experience clearly benefits.
- Command surfaces:
  - Prefer `CommandBar` for grouped document, formatting, view, and page-level actions before composing a custom bar from `Grid`, `StackPanel`, `Border`, and loose buttons.
  - Prefer the `CommandBar` overflow model for secondary actions before splitting the command surface into multiple custom rows.
  - Fall back to a custom command layout only when a verified `CommandBar` limitation, an explicit product design requirement, or unusual content composition makes the native surface a poor fit.
- Large collections:
  - Prefer controls with virtualization-friendly behavior.
  - Use `GridView` when it owns the collection surface and its scrolling behavior is part of the intended experience.
  - For poster rails or other horizontal shelves inside a vertically scrolling page, prefer a horizontal `ScrollViewer` containing an `ItemsControl` or `ItemsRepeater` with a horizontal panel instead of a nested `GridView`.
  - Consider `ItemsRepeater` when the layout is custom and performance matters.
- Search and filtering:
  - Prefer a single search field with live updates for local or otherwise inexpensive filtering.
  - Add explicit apply, refresh, or mode-selection controls only when the underlying operation is expensive, remote, asynchronous, or semantically different.
- Dialogs and transient guidance:
  - Use `ContentDialog` for modal decisions.
  - Use `InfoBar` for persistent status.
  - Use `TeachingTip` for contextual onboarding.

## Adaptive Layout Guidance

- Design with effective pixels, not fixed device assumptions.
- Make the smallest supported layout fully usable.
- Add density or multi-column views only when width allows.
- Use visual states, adaptive triggers, or layout state changes intentionally.
- Keep commands and primary content reachable after resize.
- Verify collection orientation and scrolling behavior at runtime. A shelf that looks horizontal in XAML can still render as a vertical stack once nested scroll regions are involved.
- When simplifying a dense section, remove redundant outer surfaces before adding more adaptive layout rules; fewer layers usually adapt more cleanly across breakpoints.
- Define breakpoint intent explicitly. Typical questions: when does a shelf become a stacked list, when does a footer drop nonessential controls, and when does the page stop behaving like a desktop canvas and become a single-column phone layout?
- Simplify as width shrinks. Prefer dropping secondary controls or moving them behind shell affordances over preserving every control at every breakpoint.
- When a page contains desktop-oriented horizontal shelves, add a phone-width alternative that stacks items vertically instead of relying on clipped rails and horizontal scrolling everywhere.

## WinUI Gallery Anchors

- Control pages for built-in WinUI control usage
- Gallery home and shell pages for adaptive layout ideas
- Sample pages for title bar and system backdrop interactions with content layout

## Review Checklist

- Did you choose the simplest built-in control that fits?
- Are search and filter controls no more complex than the data flow requires?
- Does the page remain usable when narrow?
- Can keyboard, mouse, and touch all reach the same core actions?
- Are spacing and hierarchy consistent across breakpoints?
- If the page mixes page scrolling with collection scrolling, is it obvious which control owns vertical scrolling and which one, if any, owns horizontal shelf scrolling?
- Are section containers doing real layout or surface work, or are some outer borders now redundant?
- At phone width, does the page read as a coherent single-column flow instead of a squeezed desktop layout?

---

## Reference: Foundation Environment Audit And Remediation

## What This Reference Is For

Use this file for machine-readiness checks, build failures caused by missing tools, and any request to install WinUI prerequisites.

## Required Workflow

1. Use the setup-and-scaffold flow in [../SKILL.md](../SKILL.md) for environment readiness, remediation, and initial verification.
2. If the user asked only for an audit and not for setup, explain that the bundled bootstrap may change the machine and get confirmation before running it.
3. If the user declines machine changes, run a manual non-mutating audit instead and summarize the result under four headings:
   - present
   - missing
   - uncertain
   - recommended optional tools
4. Manual non-mutating audit coverage should focus on:
   - OS version and build floor
   - Developer Mode state when relevant to the task
   - `dotnet --list-sdks`
   - `dotnet new list winui`
   - Visual Studio presence and edition
   - Windows SDK presence
   - MSBuild availability for XAML compilation
5. If prerequisites are still missing after the bundled setup flow, stop and report the blocker clearly instead of inventing alternate install recipes.

## Required vs Optional

Required for normal C# WinUI 3 development:

- Supported Windows build
- Visual Studio with WinUI C# support
- Windows SDK 10.0.19041.0 or later
- MSBuild available for XAML compilation
- .NET SDK 6 or later

Usually optional, but often recommended:

- Developer Mode for local deploy and debug
- WinGet for one-command remediation
- Visual Studio debugging features such as Hot Reload and Live Visual Tree

## Prefer

- The setup-and-scaffold flow in `SKILL.md` over ad hoc manual checks or duplicated setup instructions in this reference.
- A short manual audit only when the user wants a non-mutating readiness check.

## Avoid

- Rewriting or paraphrasing the bundled setup workflow here when `SKILL.md` already covers the user's goal.
- Marking workload detection as present when the bootstrap or manual audit leaves uncertainty.
- Branching into custom per-component install steps unless the user explicitly asks for them.
- Treating Developer Mode as a hard requirement for every task.

## Remediation Strategy

- Missing any required WinUI prerequisite:
  - Use the setup-and-scaffold flow in `SKILL.md` after confirmation when the request is audit-only.
- The bundled setup flow reports a partial failure but the toolchain appears usable:
  - Note the partial failure and continue when the user's task can proceed.
- The bundled setup flow fails and prerequisites still appear to be missing:
  - Use the manual audit checks above for detail if needed, then stop and report the blocker clearly.
- Windows build unsupported:
  - Upgrade Windows first. The WinUI bootstrap command does not replace the OS requirement.
- Developer Mode disabled:
  - Explain whether the current task needs it.
  - If it does, prefer the bundled setup flow or let the user enable it manually.

## Review Checklist

- Was the setup-and-scaffold flow in `SKILL.md` used before advice was given?
- Are missing items clearly separated from uncertain signals?
- Is the remediation plan the minimum needed for the user's goal?
- Was post-install verification handled by the bundled setup flow or by a clearly justified fallback?

---

## Reference: Foundation Setup And Project Selection

## What This Reference Is For

Use this file when the user is starting from scratch, choosing a project template, or asking what a WinUI machine needs before code work begins.

## Prefer

- The setup-and-scaffold flow in [../SKILL.md](../SKILL.md) for prerequisite setup, template verification, and the first scaffold.
- A C# WinUI 3 desktop app on the Windows App SDK unless the user has a clear reason to prefer C++ or an existing non-WinUI stack.
- Official project templates and default packaging choices first.
- The current supported LTS .NET SDK for new C# work instead of only meeting the bare minimum.
- A packaged app by default for the smoothest first-project, deployment, and Store-compatible path.
- An unpackaged app when the user explicitly needs repeatable CLI build-and-run verification or direct executable launches as the normal local workflow.

## Avoid

- Starting project setup before the setup-and-scaffold flow in this skill has finished.
- Starting with unpackaged deployment unless the user needs repeatable CLI launch, an installer, existing desktop app integration, or a deliberate runtime strategy.
- Giving machine-readiness advice without verification.
- Treating old Windows builds, missing SDKs, or partial Visual Studio installs as "probably fine."
- Deferring the packaging choice until after startup, storage, and launch code are already written.

## Setup Baseline

- Use the setup-and-scaffold flow in [../SKILL.md](../SKILL.md) for prerequisite setup, template verification, and the first scaffold.
- Treat [../config.yaml](../config.yaml) as the bundled WinGet bootstrap source for setup and remediation.
- Return to this reference only after that workflow completes or when the task moves beyond initial project creation.
- Windows 10 version 1809 (build 17763) or later is the floor.
- Windows SDK 10.0.19041.0 or later is the practical baseline.
- Visual Studio with the WinUI application development workload is the supported primary IDE path.
- For C# apps, a supported .NET SDK must be installed.
- Developer Mode matters for common local deploy and debug flows.

## Project Selection Guidance

- Choose packaged when the user wants the default WinUI 3 path, easy local F5 workflows, or Store-friendly deployment. Keep the scaffold at its default unless the user explicitly asks for unpackaged behavior.
- Choose packaged when the app needs package identity or package-backed APIs during normal operation.
- Choose unpackaged when the user expects direct `.exe` launches, agent-driven local verification after each change, or integration with an existing installer or external location. Request that option through the setup flow instead of converting the initial project afterward.
- For either packaging model, scaffold first through the setup flow in `SKILL.md` and continue from the generated project instead of copying in prebuilt baseline files.
- If startup or shared resources later become suspect, create a fresh comparison app with the same packaging model and diff against that `dotnet new winui` output before broader restructuring.
- Once the model is chosen, keep startup and service code consistent with that model.
- Choose the standard blank app template first, then layer in navigation, title bar, or windowing patterns as the app matures.

## Sample and Source Anchors

- Learn `start-here.md` for the current official setup path.
- Learn `winui/winui3/index.md` for the framework position and platform benefits.
- Learn `windows-app-sdk/index.md` for the Windows App SDK feature surface.
- Learn `system-requirements.md` for tool and OS baselines.

## Review Checklist

- Is the machine baseline actually verified through the setup-and-scaffold flow in `SKILL.md`?
- Is the chosen packaging model intentional?
- Does the launch workflow match the chosen packaging model?
- Is the app still rooted in the standard WinUI template unless there is a real reason not to?
- Is the recommendation aligned with a C#-first WinUI 3 workflow?

---

## Reference: Foundation Template First Recovery

## What This Reference Is For

Use this file when a new app should stay close to the `dotnet new winui` scaffold, or when opaque `MSB3073`, `XamlCompiler.exe`, and startup failures make it unclear whether the problem is in app code, shared resources, or the surrounding project structure.

## Prefer

- Scaffold with the standard `dotnet new winui` template first and keep the generated project file, manifests, assets, and startup shape unless the task explicitly requires broader changes.
- Match any comparison scaffold to the app's actual packaging model.
- Keep `App.xaml` minimal while isolating startup problems.
- Prefer explicit `new Window()` and avoid `Window.Current` when customizing WinUI 3 startup.
- Reintroduce shell, resources, bindings, and services incrementally after a clean build and launch.

## Avoid

- Swapping in alternate baseline files or helper scripts as the first recovery move.
- Replacing the template-generated `.csproj` or manifests during initial isolation.
- Flattening all styles into page-local markup as the permanent fix for opaque compiler failures.
- Treating `MSB3073` as proof that the most recently edited XAML line is the only fault.

## Template-First Recovery Loop

1. Confirm the intended packaging model and launch path.
2. If the current startup shape is unclear, scaffold a temporary comparison app with the same packaging choice. Example:
   - `dotnet new winui -n RecoveryReference -o RecoveryReference --use-slnx false --no-solution-file false`
   - Add `--unpackaged true` when the target app is unpackaged.
3. Diff only the startup and shared-resource areas against that comparison scaffold:
   - `App.xaml`
   - `App.xaml.cs`
   - `MainWindow.xaml` / `MainWindow.xaml.cs` or the app's actual shell entry point
   - merged resource dictionaries
   - startup-related project properties
4. Revert the suspect area toward the template-generated shape until the app builds cleanly again.
5. Build explicitly for a concrete architecture. Example:
   - `dotnet build MyApp.sln -c Debug -p:Platform=x64`
6. Launch using the correct packaged or unpackaged path and confirm objective startup signals.
7. Reapply custom changes in small slices, building and running after each meaningful edit.

## Common Recovery Checks

- Confirm `Window.Current` is not used in WinUI 3 startup code.
- Confirm `x:Class`, namespaces, and code-behind names still match.
- Confirm merged resource dictionaries load cleanly before adding more layers.
- Confirm project content items still match any local data or asset files the app expects at runtime.
- Run one clean build if diagnostics appear stale.

## Exit Criteria

- The current app is still rooted in the generated `dotnet new winui` scaffold rather than an alternate baseline shell.
- Build succeeds from the intended local workflow.
- The app launches from the intended local workflow.
- A real top-level window or equivalent expected UI is confirmed.

---

## Reference: Foundation Winui App Structure

## What This Reference Is For

Use this file when structuring a WinUI 3 app, reviewing project layout, or deciding where shell, pages, controls, resources, and view models should live.

## Prefer

- A clear C#-first folder split such as `Pages`, `Controls`, `ViewModels`, `Services`, `Styles`, and `Assets`.
- `App.xaml` and shared resource dictionaries for app-wide theme resources and styles.
- A single main shell window that owns navigation and common chrome.
- Native command surfaces such as `CommandBar` for grouped window or page actions before inventing a custom toolbar composition.
- Strongly typed `x:Bind` where it improves compile-time safety and performance.

## Avoid

- Putting shell logic, page logic, and resource definitions into one large window file.
- Scattering theme brushes and styles across many page-local dictionaries.
- Introducing MVVM ceremony that the project will not actually maintain.

## Recommended Shape

- `App.xaml` / `App.xaml.cs`
  - global resources, startup, window creation, app-level exceptions
- `MainWindow.xaml` / `MainWindow.xaml.cs`
  - shell, title bar, top-level navigation host
- `Pages/`
  - page views and page-specific logic
- `Controls/`
  - reusable WinUI user controls
- `ViewModels/`
  - state and commands when the app benefits from separation
- `Styles/`
  - resource dictionaries, theme tokens, shared control styles
- `Helpers/` or `Services/`
  - windowing, navigation, persistence, OS integration helpers

## Binding Guidance

- Prefer `x:Bind` for page-local properties, event handlers, and strongly typed view model access.
- Use `Binding` where the data context is dynamic or a template must stay flexible.
- Avoid binding patterns that depend on unclear page lifetime or implicit data contexts.

## WinUI Gallery Anchors

- `App.xaml.cs` shows app-level startup and integration points.
- `MainWindow.xaml` shows shell composition, title bar usage, and search integration.
- `Pages/` and `Samples/` show how Microsoft organizes pages, helpers, and styles in a real WinUI companion app.

## Review Checklist

- Are app resources centralized?
- Is shell logic separated from content pages?
- Are bindings explicit and maintainable?
- Is the structure consistent with the scale of the app?

---

## Reference: Motion Animations And Polish

## What This Reference Is For

Use this file when adding polish to a WinUI app through motion, transitions, and subtle animated state changes.

## Prefer

- Motion that clarifies hierarchy, continuity, and state changes.
- Theme transitions, connected animations, and built-in platform behaviors before custom animation systems.
- Short, purposeful animations that support the task.

## Avoid

- Decorative animation that delays interaction.
- Multiple overlapping animations for the same state change.
- Animation that hides focus, selection, or accessibility state.

## Guidance

- Use transitions to explain where content came from and where it went.
- Keep entrance and exit motion subtle.
- Use connected animation when there is a real source-to-destination relationship.
- Reach for CommunityToolkit animation helpers only when built-in transitions are not enough.

## Sample and Source Anchors

- WinUI Gallery animation, transition, and implicit animation pages
- Learn motion guidance
- CommunityToolkit animations package and samples

## Review Checklist

- Does the motion improve clarity?
- Is the app still responsive while the animation runs?
- Can the transition be simplified to a built-in WinUI behavior?
- Does the motion preserve accessibility and input clarity?

---

## Reference: Performance Diagnostics And Responsiveness

## What This Reference Is For

Use this file when the user reports sluggish WinUI behavior, dropped frames, long startup, or laggy scrolling and layout.

## Prefer

- Keeping the UI thread free for layout, rendering, and input.
- Simpler visual trees and lighter templates.
- Virtualization-friendly controls and item layouts.
- Measurement before optimization when the issue is not obvious.

## Avoid

- Doing expensive I/O or CPU work directly on the UI thread.
- Deeply nested XAML trees without a concrete benefit.
- Re-templating controls in ways that dramatically increase layout work.
- Guessing at performance causes without profiling.

## Guidance

- Favor platform controls and layouts that virtualize well for long lists.
- Defer or background heavy work when it does not need to block interaction.
- Reduce unnecessary layout invalidation and repeated measure/arrange churn.
- Use WPR and WPA with the XAML Frame Analysis plugin for frame-level investigations.
- Treat slow-frame findings as a clue to UI-thread overload, not as a reason to micro-optimize blindly.

## Sample and Source Anchors

- Learn `winui-perf.md`
- WinUI Gallery pages that demonstrate adaptive UI and complex controls without excessive custom infrastructure

## Review Checklist

- Is heavy work running off the UI thread where possible?
- Are large collections using an appropriate items control?
- Is the visual tree no more complex than it needs to be?
- Has profiling been used before claiming a fix?

---

## Reference: Sample Source Map

## What This Reference Is For

Use this file when you know the task but need to identify the best canonical source to inspect first.

| Task | First source | Backup source |
| --- | --- | --- |
| Check whether a PC can build WinUI apps | `../SKILL.md` | `foundation-environment-audit-and-remediation.md` |
| Install missing prerequisites | `../SKILL.md` | `foundation-environment-audit-and-remediation.md` |
| Start a new packaged or unpackaged app | `../SKILL.md` | `foundation-setup-and-project-selection.md` |
| Choose packaged vs unpackaged | Learn Windows App SDK deployment docs | WindowsAppSDK-Samples `Samples/Unpackaged` |
| Build a shell with navigation | WinUI Gallery navigation pages | Learn navigation basics |
| Design a custom title bar | Learn title bar guidance | WinUI Gallery title bar samples |
| Add Mica or system backdrops | Learn Mica guidance | WindowsAppSDK-Samples `Samples/Mica` |
| Design a settings page | WinUI Gallery control pages | CommunityToolkit `SettingsControls` |
| Pick a control for a list or collection | WinUI Gallery control pages | Learn responsive/layout guidance |
| Improve accessibility | Learn accessibility docs | WinUI Gallery standard control behavior |
| Diagnose responsiveness | Learn `winui-perf.md` | WPR/WPA guidance in `testing-debugging-and-review-checklists.md` |
| Add notifications or activation flows | WindowsAppSDK-Samples | Learn Windows App SDK lifecycle docs |
| Decide whether to add CommunityToolkit | `community-toolkit-controls-and-helpers.md` | Toolkit component directories |

## Source Preferences

- Learn first for requirements and behavioral guidance.
- WinUI Gallery first for concrete control usage and shell composition.
- WindowsAppSDK-Samples first for scenario APIs and platform integration.
- CommunityToolkit only when the task clearly requires Toolkit-specific functionality.

---

## Reference: Shell Navigation And Windowing

## What This Reference Is For

Use this file for top-level app shells, page navigation models, custom title bars, and multi-window decisions.

## Prefer

- `NavigationView` for standard desktop shells with clear top-level destinations.
- A small, stable set of primary destinations.
- Built-in back navigation behavior that matches user expectations.
- `AppWindow` and Windows App SDK windowing APIs for modern window management.

## Avoid

- Overloading the nav surface with every command and secondary action.
- Turning the `NavigationView` pane into a branded hero area when the user did not ask for custom shell treatment.
- Custom title bar layouts that break drag regions or caption button clarity.
- Multi-window designs unless the workflow clearly benefits from them.

## Navigation Guidance

- Use left navigation when the app has several stable, high-level destinations.
- Use top navigation when there are few peer destinations and width is available.
- Use a single-page or document-first layout when navigation is shallow and the user mostly stays in one workflow.
- Keep naming and iconography stable across pages.
- Treat `NavigationView` as functional shell chrome first. Keep pane headers, footer content, and decorative branding minimal unless the product requirements clearly call for them.
- Prefer the platform's normal pane structure before adding custom logo blocks, taglines, or non-navigation content that changes the shell's native feel.
- For narrow or phone-like widths, stop reserving permanent pane width for desktop navigation. Prefer a minimal or overlay navigation mode, show the pane toggle when needed, close the pane by default after navigation, and give content the width back.
- When a shell enters a phone-width mode, reduce content padding and decorative chrome so the page reads as one primary column instead of a desktop shell with a squeezed content strip.

## Title Bar Guidance

- Treat the title bar as functional chrome first, branding surface second.
- Keep empty non-interactive areas draggable.
- Blend title bar visuals with the rest of the app when possible.
- Respect light, dark, and high-contrast states.

## Windowing Guidance

- Start with one main window.
- Add secondary windows only for workflows such as document detachment, inspection panes, or tool windows.
- Use Windows App SDK samples for resizing, placement, and window-specific behaviors instead of inventing custom platform abstractions.

## Sample and Source Anchors

- WinUI Gallery `NavigationView`, `TitleBar`, `AppWindow`, and windowing sample pages
- WindowsAppSDK-Samples `Samples/Windowing`
- Learn navigation and title bar guidance

## Review Checklist

- Is the navigation model simple and intentional?
- Does the shell still look and behave like a normal WinUI `NavigationView` unless there is an explicit reason to diverge?
- Does the title bar still behave like a Windows title bar?
- Are back, search, and pane behaviors consistent?
- Is multi-window use justified by the workflow?
- Does the shell intentionally switch behavior at narrow or phone widths instead of leaving a full desktop pane open?

---

## Reference: Styling Theming Materials And Icons

## What This Reference Is For

Use this file for Fluent styling choices, theme resources, Mica or Acrylic usage, custom title bar visuals, typography, and iconography.

## Prefer

- Theme resources and system brushes over hard-coded colors.
- Standard WinUI surface resources and default control chrome before custom panel systems.
- Mica on long-lived surfaces such as the main window background or title bar region.
- Acrylic on transient or light-dismiss surfaces.
- Segoe UI Variable or platform-default typography choices.
- Fluent iconography that matches the platform language.
- When metadata needs a visual container, prefer small rounded rectangles or subtle badges over bright oval pills.

## Avoid

- Hard-coded light-theme colors that break dark or high-contrast themes.
- Wrapping every region in a custom `Border` with a bespoke corner radius, stroke, and fill when standard WinUI surfaces would do the job.
- Adding an outer section `Border` around content that is already visually grouped by card controls, spacing, or headers; this often creates a redundant "card around cards" effect.
- Using Acrylic where Mica or a simple theme-aware surface would be cheaper and clearer.
- Mixing unrelated icon styles.
- Filling lists or cards with rows of decorative oval chips for routine metadata. Use tag treatments sparingly, and default to rounded rectangles when they are justified.

## Theming Guidance

- Support light, dark, and high-contrast by default.
- Centralize brushes, typography, and corner/spacing decisions in shared resource dictionaries.
- Let built-in controls keep their platform behavior unless there is a strong design reason to customize them.
- When a grouped surface is needed, prefer system resources such as `CardBackgroundFillColorDefaultBrush`, `CardStrokeColorDefaultBrush`, and `LayerFillColorDefaultBrush` instead of inventing a parallel surface language.
- If child content already uses card-like surfaces, prefer removing the outer section border and relying on layout spacing and typography for grouping unless the section needs its own distinct background, inset, or stroke.

## Materials Guidance

- Use Mica for long-lived base layers.
- Use Acrylic for transient surfaces such as flyouts and menus.
- Verify fallback behavior on older Windows versions or unsupported scenarios.

## Icon and Typography Guidance

- Use standard Windows iconography and keep visual weight consistent.
- Use typography to create hierarchy instead of adding extra borders or decoration.
- Keep title bar text and document titles aligned with Windows guidance.

## Sample and Source Anchors

- Learn material, typography, and iconography guidance
- WinUI Gallery system backdrop and styling pages
- WindowsAppSDK-Samples `Samples/Mica`

## Review Checklist

- Are colors and brushes theme-aware?
- Does the app look correct in light, dark, and high contrast?
- Is the selected material appropriate for the surface lifetime?
- Are icon and typography choices consistent with Fluent design?
- Are standard WinUI surfaces doing most of the visual work, with custom borders limited to clearly justified cases?
- Are there any redundant outer borders that could be removed without losing hierarchy or usability?
- Are tag or chip treatments sparse, visually quiet, and not rendered as default oval pills unless the product explicitly calls for that style?

---

## Reference: Testing Debugging And Review Checklists

## What This Reference Is For

Use this file for final review passes, debugging sessions, and "what should I verify before I call this done?" prompts.

## Required Verification Loop

- Build after each meaningful edit, not only at the end.
- Run the app after changes when the user asked for it or when startup-sensitive files changed.
- Verify actual launch instead of assuming success from a spawned process.
- If the app fails before showing a window, debug the startup path before continuing feature work.

## Design Review Checklist

- Shell and navigation are simple and predictable.
- `NavigationView` still reads like standard WinUI shell chrome unless the product explicitly calls for branded pane content or custom shell composition.
- Layout stays usable when the window is narrow.
- Layout has been checked at more than one breakpoint, including a genuinely phone-like width when the app can be resized that far.
- Collection pages with mixed scroll regions have been checked at runtime so shelves still render in the intended direction and do not collapse into a single vertical column.
- Theme, contrast, hierarchy, and interactive state visibility hold up in both light and dark mode, and typography and iconography still feel native to Windows.
- Command placement and hierarchy are clear.
- Default WinUI surfaces and control templates carry most of the layout instead of a custom border/card system.
- Search and filter workflows avoid redundant controls when live local filtering would be clearer.
- At narrow and phone widths, nonessential controls are simplified, hidden, or moved behind shell affordances instead of merely compressed.

## Code Review Checklist

- App structure is coherent and scalable.
- Resource dictionaries and styles are centralized where they should be.
- Platform controls are preferred over unnecessary custom control work.
- New dependencies are justified.
- The packaging model matches the startup, storage, and launch code.
- The app builds cleanly from the workflow the user will actually use.

## Accessibility Checklist

- Keyboard-only flow works end to end.
- Focus states are visible and sensible.
- Automation properties are present where needed.
- High contrast and text scaling do not break the UI.

## Performance Checklist

- No obvious UI-thread blocking work in interactive paths.
- Large collections use an appropriate control and layout.
- Scroll ownership is intentional for collection-heavy pages; nested `GridView` plus outer `ScrollViewer` combinations have been justified or replaced.
- Expensive styling or template choices are justified.
- Profiling data exists for non-obvious performance claims.

## Debugging Tools

- Use Hot Reload for fast visual iteration.
- Use Live Visual Tree and Live Property Explorer for layout and property debugging.
- Use WPR and WPA when diagnosing frame or responsiveness issues.
- Reproduce resize, theme, and input-mode changes before concluding the issue is fixed.
- When resize behavior is part of the task, verify wide, medium, and phone-width states against the running app rather than trusting the XAML structure alone.
- When a collection page looks wrong, inspect the live tree for nested `ScrollViewer` ownership before rewriting the item template; the bug may be layout ownership rather than card markup.
- Use startup exception details, debugger output, or Event Viewer when the process dies before any window appears.

## Exit Criteria

- The build succeeds from the intended local workflow.
- The feature works on the intended machine configuration.
- The app launches and shows the expected shell or window.
- The app remains usable in light, dark, and high contrast.
- Primary flows are keyboard-accessible.
- Resize behavior, startup, and interactive responsiveness have been checked.
- If the window can become phone-width, the shell and content have been verified there too.

---

## Reference: Windows App Sdk Lifecycle Notifications And Deployment

## What This Reference Is For

Use this file when the user needs lifecycle, activation, notification, packaged vs unpackaged, or runtime initialization guidance that goes beyond plain XAML UI work.

## Prefer

- Learning the scenario from the matching WindowsAppSDK sample before designing an abstraction.
- Packaged deployment when it fits the product constraints.
- Explicit unpackaged guidance when the user has an installer, external-location requirement, or expects repeatable direct executable launches during development.

## Avoid

- Mixing packaged and unpackaged guidance in one answer without stating which path applies.
- Treating deployment requirements as optional details.
- Re-implementing lifecycle behavior already covered by Windows App SDK APIs.
- Using package-identity-dependent APIs in unpackaged startup code without an explicit guard or replacement path.

## Guidance

- Use AppLifecycle guidance and samples for activation, instancing, restart, and state notifications.
- Use notifications samples for push or app notifications rather than inventing custom delivery logic.
- For packaged apps, account for framework-dependent deployment and runtime package requirements.
- For unpackaged apps, account for bootstrapper and runtime initialization requirements.
- For unpackaged apps, treat package identity as absent unless the app deliberately establishes it through the chosen deployment model.
- Keep storage, settings, and startup services aligned with the deployment model. If a service assumes packaged storage or activation, redesign it before local unpackaged verification.
- Explain the deployment model before giving build or publish steps.

## Sample and Source Anchors

- WindowsAppSDK-Samples `Samples/AppLifecycle`
- WindowsAppSDK-Samples `Samples/Notifications`
- WindowsAppSDK-Samples `Samples/Unpackaged`
- WindowsAppSDK-Samples `Samples/CustomControls`
- Learn packaged and unpackaged deployment guides

## Review Checklist

- Is the app’s deployment model explicit?
- Are lifecycle and activation behaviors using platform APIs rather than ad hoc workarounds?
- Are notification requirements matched to the correct sample and runtime guidance?
- Does the recommendation match packaged or unpackaged constraints?
