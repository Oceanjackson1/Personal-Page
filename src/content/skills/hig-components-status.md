---
title: "Hig Components Status"
description: "Apple HIG guidance for status and progress UI components including progress indicators, status bars, and activity rings."
category: "development"
source: "community"
author: "Community"
tags: ["hig", "components", "status"]
date: 2026-03-20
---

# Apple HIG: Status Components

Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered.

## Key Principles

### Progress Indicators

1. **Show progress for operations longer than a second or two.**

2. **Determinate when duration/percentage is known.** A filling progress bar gives users a clear sense of remaining work. Use for downloads, uploads, or any measurable process.

3. **Indeterminate when duration is unknown.** A spinner communicates work is happening without promising a timeframe. Use for unpredictable network requests.

4. **Prefer progress bars over spinners.** Determinate progress feels faster and more trustworthy.

5. **Place indicators where content will appear.** Inline progress near the content area, not modal or distant.

6. **Don't stack multiple indicators.** Aggregate simultaneous operations into one representation or show the most relevant.

### Status Bars

7. **Don't hide the status bar without good reason.** Reserve hiding for immersive experiences (full-screen media, games, AR).

8. **Match status bar style to your content.** Light or dark for adequate contrast.

9. **Respect safe areas.** No interactive content behind the status bar.

10. **Restore promptly** when exiting immersive contexts.

### Activity Rings

11. **Activity rings are for Move, Exercise, and Stand goals.** Don't repurpose the ring metaphor for unrelated data.

12. **Respect ring color conventions.** Red (Move), green (Exercise), blue (Stand) are strongly associated with Apple Fitness.

13. **Use HealthKit APIs** for activity data rather than manual tracking.

14. **Celebrate completions** with animation and haptics when rings close.

## Reference Index

| Reference | Topic | Key content |
|---|---|---|
| [progress-indicators.md](references/progress-indicators.md) | Progress bars and spinners | Determinate, indeterminate, inline placement, duration |
| [status-bars.md](references/status-bars.md) | iOS/iPadOS status bar | System info, visibility, style, safe areas |
| [activity-rings.md](references/activity-rings.md) | watchOS activity rings | Move/Exercise/Stand, HealthKit, fitness tracking, color |

## Output Format

1. **Indicator type recommendation** with rationale (determinate vs indeterminate).
2. **Timing and animation guidance** -- duration thresholds, animation style, transitions.
3. **Accessibility** -- VoiceOver progress announcements, live region updates.
4. **Platform-specific behavior** across targeted platforms.

## Questions to Ask

1. Is the duration known or unknown?
2. Which platforms?
3. How long does the operation typically take?
4. System-level or in-app indicator?

## Related Skills

- **hig-components-system** -- Widgets and complications displaying progress or status
- **hig-inputs** -- Gestures triggering progress states (pull-to-refresh)
- **hig-technologies** -- HealthKit for activity ring data; VoiceOver for progress announcements

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Activity Rings

|---|---  
<!-- image: R-250,G-17,B-79 -->| <!-- image: R-166,G-255,B-0 -->| <!-- image: R-0,G-255,B-246 -->  
  
**Maintain Activity ring margins.** An Activity ring element must include a minimum outer margin of no less than the distance between rings. Never allow other elements to crop, obstruct, or encroach upon this margin or the rings themselves.

**Differentiate other ring-like elements from Activity rings.** Mixing different ring styles can lead to a visually confusing interface. If you must include other rings, use padding, lines, or labels to separate them from Activity rings. Color and scale can also help provide visual separation.

**Don’t send notifications that repeat the same information the Activity app sends.** The system already delivers Move, Exercise, and Stand progress updates, so it’s confusing for people to receive redundant information from your app. Also, don’t show an Activity ring element in your app’s notifications. It’s fine to reference Activity progress in a notification, but do so in a way that’s unique to your app and doesn’t replicate the same information the system provides.

**Don’t use Activity rings for decoration.** Activity rings provide information to people; they don’t just embellish your app’s design. Never display Activity rings in labels or background graphics.

**Don’t use Activity rings for branding.** Use Activity rings strictly to display Activity progress in your app. Never use Activity rings in your app’s icon or marketing materials.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Platform-considerations)

 _No additional considerations for iPadOS or watchOS. Not supported in macOS, tvOS, or visionOS._

### [iOS](https://developer.apple.com/design/human-interface-guidelines/activity-rings#iOS)

Activity rings are available in iOS with [`HKActivityRingView`](https://developer.apple.com/documentation/HealthKitUI/HKActivityRingView). The appearance of the Activity ring element changes automatically depending on whether an Apple Watch is paired:

  * With an Apple Watch paired, iOS shows all three Activity rings.

  * Without an Apple Watch paired, iOS shows the Move ring only, which represents an approximation of a person’s activity based on their steps and workout information from other apps.




<!-- image: A screenshot of the Activity summary in the iOS Fitness app with Apple Watch paired. All three Activity rings are displayed. -->

Apple Watch paired

<!-- image: A screenshot of the Activity summary in the iOS Fitness app with no Apple Watch paired. Only the Move ring is displayed. -->

No Apple Watch paired

Because iOS shows Activity rings whether or not an Apple Watch is paired, activity history can include a combination of both styles. For example, Activity rings in Fitness have three rings when a person exercises with their Apple Watch paired, and only the Move ring when they exercise without their Apple Watch.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Related)

[Workouts](https://developer.apple.com/design/human-interface-guidelines/workouts)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Developer-documentation)

[`HKActivityRingView`](https://developer.apple.com/documentation/HealthKitUI/HKActivityRingView) — HealthKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Videos)

[<!-- image:  --> Track workouts with HealthKit on iOS and iPadOS ](https://developer.apple.com/videos/play/wwdc2025/322)

[<!-- image:  --> Build a workout app for Apple Watch ](https://developer.apple.com/videos/play/wwdc2021/10009)

[<!-- image:  --> Build custom workouts with WorkoutKit ](https://developer.apple.com/videos/play/wwdc2023/10016)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/activity-rings#Change-log)

Date| Changes  
---|---  
March 29, 2024| Enhanced guidance for displaying Activity rings and listed specific colors for displaying related content.  
December 5, 2023| Added artwork representing Activity rings in iOS.

---

## Reference: Progress Indicators

|---  
September 12, 2023| Combined guidance common to all platforms.  
June 5, 2023| Updated guidance to reflect changes in watchOS 10.

---

## Reference: Status Bars

---
title: "Status bars | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/status-bars

# Status bars

A status bar appears along the upper edge of the screen and displays information about the device’s current state, like the time, cellular carrier, and battery level.

<!-- image: A stylized representation of an iPhone status bar with labels showing the time and cellular, Wi-Fi, and battery levels. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/status-bars#Best-practices)

**Obscure content under the status bar.** By default, the background of the status bar is transparent, allowing content beneath to show through. This transparency can make it difficult to see information presented in the status bar. If controls are visible behind the status bar, people may attempt to interact with them and be unable to do so. Be sure to keep the status bar readable, and don’t imply that content behind it is interactive. Prefer using a scroll edge effect to place a blurred view behind the status bar. For developer guidance, see [`ScrollEdgeEffectStyle`](https://developer.apple.com/documentation/SwiftUI/ScrollEdgeEffectStyle) and [`UIScrollEdgeEffect`](https://developer.apple.com/documentation/UIKit/UIScrollEdgeEffect).

**Consider temporarily hiding the status bar when displaying full-screen media.** A status bar can be distracting when people are paying attention to media. Temporarily hide these elements to provide a more immersive experience. The Photos app, for example, hides the status bar and other interface elements when people browse full-screen photos.

<!-- image: A screenshot of the top half of the Photos app on iPhone, showing a photo filling the screen. The status bar is visible at the top of the screen. -->

The Photos app with the status bar visible

<!-- image: A screenshot of the top half of the Photos app on iPhone, showing a photo filling the screen. The status bar is hidden, and only the photo is visible. -->

The Photos app with the status bar hidden

**Avoid permanently hiding the status bar.** Without a status bar, people have to leave your app to check the time or see if they have a Wi-Fi connection. Let people redisplay a hidden status bar with a simple, discoverable gesture. For example, when browsing full-screen photos in the Photos app, a single tap shows the status bar again.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/status-bars#Platform-considerations)

 _No additional considerations for iOS or iPadOS. Not supported in macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/status-bars#Resources)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/status-bars#Developer-documentation)

[`UIStatusBarStyle`](https://developer.apple.com/documentation/UIKit/UIStatusBarStyle) — UIKit

[`preferredStatusBarStyle`](https://developer.apple.com/documentation/UIKit/UIViewController/preferredStatusBarStyle) — UIKit
