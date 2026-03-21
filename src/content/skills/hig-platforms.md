---
title: "Hig Platforms"
description: "Apple Human Interface Guidelines for platform-specific design."
category: "other"
source: "community"
author: "Community"
tags: ["hig", "platforms"]
date: 2026-03-20
---

# Apple HIG: Platform Design

Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered.

## Key Principles

1. **Each platform has a distinct identity.** Do not port designs between platforms. Respect each platform's conventions, interaction models, and user expectations.

2. **iOS: touch-first.** Direct manipulation on a handheld screen. Optimize for one-handed use. Navigation uses tab bars and push/pop stacks.

3. **iPadOS: expanded canvas.** Support Split View, Slide Over, and Stage Manager. Use sidebars and multi-column layouts. Support pointer and keyboard alongside touch.

4. **macOS: pointer and keyboard.** Dense information display is acceptable. Use menu bars, toolbars, and keyboard shortcuts extensively. Windows are resizable with precise control.

5. **tvOS: remote and focus.** Viewed from a distance. Design for the Siri Remote with focus-based navigation. Large text, simple layouts, linear navigation.

6. **visionOS: spatial interaction.** 3D environment using windows, volumes, and spaces. Eye tracking for targeting, indirect gestures for interaction. Respect ergonomic comfort zones.

7. **watchOS: glanceable and brief.** Information consumable at a glance. Brief interactions. Digital Crown, haptics, and complications for timely content.

8. **Games: own paradigm.** Free to define in-game interaction models, but still respect platform conventions for system interactions (notifications, accessibility, controllers).

## Reference Index

| Reference | Topic | Key content |
|---|---|---|
| [designing-for-ios.md](references/designing-for-ios.md) | iOS | Touch, tab bars, navigation stacks, gestures, screen sizes, safe areas |
| [designing-for-ipados.md](references/designing-for-ipados.md) | iPadOS | Multitasking, sidebars, pointer, keyboard, Apple Pencil, Stage Manager |
| [designing-for-macos.md](references/designing-for-macos.md) | macOS | Menu bars, toolbars, window management, keyboard shortcuts, dense layouts, Dock |
| [designing-for-tvos.md](references/designing-for-tvos.md) | tvOS | Focus engine, Siri Remote, lean-back experience, content-forward, parallax |
| [designing-for-visionos.md](references/designing-for-visionos.md) | visionOS | Spatial computing, windows/volumes/spaces, eye tracking, hand gestures, depth |
| [designing-for-watchos.md](references/designing-for-watchos.md) | watchOS | Glanceable UI, Digital Crown, complications, notifications, haptics |
| [designing-for-games.md](references/designing-for-games.md) | Games | Controllers, immersive experiences, platform-specific conventions, accessibility |

## Decision Framework

1. **Identify the primary use context.** On the go (iOS/watchOS), at a desk (macOS), on the couch (tvOS), spatial environment (visionOS)?

2. **Match input to interaction.** Touch for direct manipulation, pointer for precision, gaze+gesture for spatial, Digital Crown for quick scrolling, remote for focus navigation.

3. **Adapt, don't replicate.** A macOS sidebar becomes a tab bar on iPhone. A visionOS volume has no equivalent on watchOS. Translate intent, not implementation.

4. **Leverage platform strengths.** Live Activities on iOS, Desktop Widgets on macOS, complications on watchOS, immersive spaces on visionOS.

5. **Maintain brand consistency** while respecting each platform's visual language and interaction patterns.

## Output Format

1. **Platform-specific recommendations** citing relevant HIG sections.
2. **Platform differences table** comparing navigation, input, layout, and conventions.
3. **Implementation notes** per platform including recommended APIs and adaptation strategies.

## Questions to Ask

1. Which platforms are you targeting?
2. New app or adapting an existing one? If existing, which platform is the base?
3. SwiftUI or UIKit/AppKit?
4. Need to support older OS versions?
5. Primary use context? (On the go, desk, couch, spatial, glanceable?)

## Related Skills

- **hig-foundations** -- Shared principles (color, typography, accessibility, layout) across platforms
- **hig-patterns** -- Interaction patterns that manifest differently per platform
- **hig-components-layout** -- Navigation structures (tab bars, sidebars, split views) that vary by platform
- **hig-components-content** -- Content display that adapts across platforms

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Designing For Games

|---|---  
iOS, iPadOS| 17 pt| 11 pt  
macOS| 13 pt| 10 pt  
tvOS| 29 pt| 23 pt  
visionOS| 17 pt| 12 pt  
watchOS| 16 pt| 12 pt  
  
**Make sure buttons are always easy to use.** Buttons that are too small or too close together can frustrate players and make gameplay less fun. Each platform defines a recommended minimum button size based on its default interaction method. For example, buttons in iOS must be at least 44x44 pt to accommodate touch interaction. For guidance, see [Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons).

Platform| Default button size| Minimum button size  
---|---|---  
iOS, iPadOS| 44x44 pt| 28x28 pt  
macOS| 28x28 pt| 20x20 pt  
tvOS| 66x66 pt| 56x56 pt  
visionOS| 60x60 pt| 28x28 pt  
watchOS| 44x44 pt| 28x28 pt  
  
**Prefer resolution-independent textures and graphics.** If creating resolution-independent assets isn’t possible, match the resolution of your game to the resolution of the device. In visionOS, prefer vector-based art that can continue to look good when the system dynamically scales it as people view it from different distances and angles. For guidance, see [Images](https://developer.apple.com/design/human-interface-guidelines/images).

**Integrate device features into your layout.** For example, a device may have rounded corners or a camera housing that can affect parts of your interface. To help your game look at home on each device, accommodate such features during layout, relying on platform-provided safe areas when possible (for developer guidance, see [Positioning content relative to the safe area](https://developer.apple.com/documentation/UIKit/positioning-content-relative-to-the-safe-area)). For guidance, see [Layout](https://developer.apple.com/design/human-interface-guidelines/layout); for templates that include safe-area guides, see [Apple Design Resources](https://developer.apple.com/design/resources/).

**Make sure in-game menus adapt to different aspect ratios.** Games need to look good and behave well at various aspect ratios, such as 16:10, 19.5:9, and 4:3. In particular, in-game menus need to remain legible and easy to use on every device — and, if you support them, in both orientations on iPhone and iPad — without obscuring other content. To help ensure your in-game menus render correctly, consider using dynamic layouts that rely on relative constraints to adjust to different contexts. Avoid fixed layouts as much as possible, and aim to create a custom, device-specific layout only when necessary. For guidance, see [In-game menus](https://developer.apple.com/design/human-interface-guidelines/menus#In-game-menus).

**Design for the full-screen experience.** People often enjoy playing a game in a distraction-free, full-screen context. In macOS, iOS, and iPadOS, full-screen mode lets people hide other apps and parts of the system UI; in visionOS, a game running in a Full Space can completely surround people, transporting them somewhere else. For guidance, see [Going full screen](https://developer.apple.com/design/human-interface-guidelines/going-full-screen).

[<!-- image: A sketch of a small rectangle in the upper-left quadrant of a larger rectangle, suggesting the position of a user interface element within a window. The image is overlaid with rectangular and circular grid lines and is tinted yellow to subtly reflect the yellow in the original six-color Apple logo. --> Layout ](https://developer.apple.com/design/human-interface-guidelines/layout)

[<!-- image: A sketch of a small letter A to the left of a large letter A, suggesting the use of typography to convey hierarchical information. The image is tinted yellow to subtly reflect the yellow in the original six-color Apple logo. --> Typography ](https://developer.apple.com/design/human-interface-guidelines/typography)

[<!-- image: A sketch of two outward-pointing arrows arranged in a vertical line extending from the upper-left to the bottom-right, suggesting expansion. The image is tinted orange to subtly reflect the orange in the original six-color Apple logo. --> Going full screen ](https://developer.apple.com/design/human-interface-guidelines/going-full-screen)

## [Enable intuitive interactions](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Enable-intuitive-interactions)

**Support each platform’s default interaction method.** For example, people generally use touch to play games on iPhone; on a Mac, players tend to expect keyboard and mouse or trackpad support; and in a visionOS game, people expect to use their eyes and hands while making indirect and direct gestures. As you work to ensure that your game supports each platform’s default interaction method, pay special attention to control sizing and menu behavior, especially when bringing your game from a pointer-based context to a touch-based one.

Platform| Default interaction methods| Additional interaction methods  
---|---|---  
iOS| Touch| Game controller  
iPadOS| Touch| Game controller, keyboard, mouse, trackpad, Apple Pencil  
macOS| Keyboard, mouse, trackpad| Game controller  
tvOS| Remote| Game controller, keyboard, mouse, trackpad  
visionOS| Touch| Game controller, keyboard, mouse, trackpad, spatial game controller  
watchOS| Touch| –  
  
**Support physical game controllers, while also giving people alternatives.** Every platform except watchOS supports physical game controllers. Although the presence of a game controller makes it straightforward to port controls from an existing game and handle complex control mappings, recognize that not every player can use a physical game controller. To make your game available to as many players as possible, also offer alternative ways to interact with your game. For guidance, see [Physical controllers](https://developer.apple.com/design/human-interface-guidelines/game-controls#Physical-controllers).

**Offer touch-based game controls that embrace the touchscreen experience on iPhone and iPad.** In iOS and iPadOS, your game can allow players to interact directly with game elements, and to control the game using virtual controls that appear on top of your game content. For design guidance, see [Touch controls](https://developer.apple.com/design/human-interface-guidelines/game-controls#Touch-controls).

[<!-- image: A sketch of a D-pad control from a game controller, suggesting gameplay. The image is tinted purple to subtly reflect the purple in the original six-color Apple logo. --> Game controls ](https://developer.apple.com/design/human-interface-guidelines/game-controls)

[<!-- image: A sketch of a pointing hand swiping in a curved motion toward the right, suggesting touch interaction with a device. The image is tinted purple to subtly reflect the purple in the original six-color Apple logo. --> Gestures ](https://developer.apple.com/design/human-interface-guidelines/gestures)

[<!-- image: A sketch of an arrow-shaped pointer, suggesting use of a mouse or trackpad. The image is tinted purple to subtly reflect the purple in the original six-color Apple logo. --> Pointing devices ](https://developer.apple.com/design/human-interface-guidelines/pointing-devices)

## [Welcome everyone](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Welcome-everyone)

**Prioritize perceivability.** Make sure people can perceive your game’s content whether they use sight, hearing, or touch. For example, avoid relying solely on color to convey an important detail, or providing a cutscene that doesn’t include descriptive subtitles or offer other ways to read the content. For specific guidance, see:

  * Text sizes

  * Color and effects

  * Motion

  * Interactions

  * Buttons




**Help players personalize their experience.** Players have a variety of preferences and abilities that influence their interactions with your game. Because there’s no universal configuration that suits everyone, give players the ability to customize parameters like type size, game control mapping, motion intensity, and sound balance. You can take advantage of built-in [Apple accessibility technologies](https://developer.apple.com/accessibility/) to support accessibility personalizations, whether you’re using system frameworks or [Unity plug-ins](https://github.com/Apple/UnityPlugins).

**Give players the tools they need to represent themselves.** If your game encourages players to create avatars or supply names or descriptions, support the spectrum of self-identity and provide options that represent as many human characteristics as possible.

**Avoid stereotypes in your stories and characters.** Ask yourself whether you’re depicting game characters and scenarios in a way that perpetuates real-life stereotypes. For example, does your game depict enemies as having a certain race, gender, or cultural heritage? Review your game to uncover and remove biases and stereotypes and — if references to real-life cultures and languages are necessary — be sure they’re respectful.

[<!-- image: A sketch of the Accessibility icon. The image is tinted yellow to subtly reflect the yellow in the original six-color Apple logo. --> Accessibility ](https://developer.apple.com/design/human-interface-guidelines/accessibility)

[<!-- image: A sketch of two people, suggesting inclusion. The image is tinted yellow to subtly reflect the yellow in the original six-color Apple logo. --> Inclusion ](https://developer.apple.com/design/human-interface-guidelines/inclusion)

## [Adopt Apple technologies](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Adopt-Apple-technologies)

**Integrate Game Center to help players discover your game across their devices and connect with their friends.** [Game Center](https://developer.apple.com/game-center/) is Apple’s social gaming network, available on all platforms. Game Center lets players keep track of their progress and achievements and allows you to set up leaderboards, challenges, and multiplayer activities in your game. For design guidance, see [Game Center](https://developer.apple.com/design/human-interface-guidelines/game-center); for developer guidance, see [GameKit](https://developer.apple.com/documentation/GameKit).

**Let players pick up their game on any of their devices.** People often have a single iCloud account that they use across multiple Apple devices. When you support [GameSave](https://developer.apple.com/documentation/GameSave), you can help people save their game state and start back up exactly where they left off on a different device.

**Support haptics to help players feel the action.** When you adopt Core Haptics, you can compose and play custom haptic patterns, optionally combined with custom audio content. Core Haptics is available in iOS, iPadOS, tvOS, and visionOS, and supported on many game controllers. For guidance, see [Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics); for developer guidance, see [Core Haptics](https://developer.apple.com/documentation/CoreHaptics) and [Playing Haptics on Game Controllers](https://developer.apple.com/documentation/CoreHaptics/playing-haptics-on-game-controllers).

**Use Spatial Audio to immerse players in your game’s soundscape.** Providing multichannel audio can help your game’s audio adapt automatically to the current device, enabling an immersive Spatial Audio experience where supported. For guidance, see [Playing audio > visionOS](https://developer.apple.com/design/human-interface-guidelines/playing-audio#visionOS); for developer guidance, see [Explore Spatial Audio](https://developer.apple.com/news/?id=fakg1z5b).

**Take advantage of Apple technologies to enable unique gameplay mechanics.** For example, you can integrate technologies like augmented reality, machine learning, and [HealthKit](https://developer.apple.com/documentation/HealthKit), and request access to location data and functionality like camera and microphone. For a full list of Apple technologies, features, and services, see [Technologies](https://developer.apple.com/design/human-interface-guidelines/technologies).

[<!-- image: A sketch of the Game Center icon. The image is tinted blue to subtly reflect the blue in the original six-color Apple logo. --> Game Center ](https://developer.apple.com/design/human-interface-guidelines/game-center)

[<!-- image: A sketch of the iCloud icon. The image is tinted blue to subtly reflect the blue in the original six-color Apple logo. --> iCloud ](https://developer.apple.com/design/human-interface-guidelines/icloud)

[<!-- image: A sketch of an add button, suggesting the purchase of additional digital assets within an app. The image is tinted blue to subtly reflect the blue in the original six-color Apple logo. --> In-app purchase ](https://developer.apple.com/design/human-interface-guidelines/in-app-purchase)

## [Resources](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Related)

[Game Center](https://developer.apple.com/design/human-interface-guidelines/game-center)

[Game controls](https://developer.apple.com/design/human-interface-guidelines/game-controls)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Developer-documentation)

[Games Pathway](https://developer.apple.com/games/get-started/)

[Create games for Apple platforms](https://developer.apple.com/games/)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Videos)

[<!-- image:  --> Level up your games ](https://developer.apple.com/videos/play/wwdc2025/209)

[<!-- image:  --> Design advanced games for Apple platforms ](https://developer.apple.com/videos/play/wwdc2024/10085)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/designing-for-games#Change-log)

Date| Changes  
---|---  
June 9, 2025| Updated guidance for touch-based controls and Game Center.  
June 10, 2024| New page.

---

## Reference: Designing For Ios

---
title: "Designing for iOS | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/designing-for-ios

# Designing for iOS

People depend on their iPhone to help them stay connected, play games, view media, accomplish tasks, and track personal data in any location and while on the go.

<!-- image: A stylized representation of an iPhone frame shown on top of a grid. The image is overlaid with rectangular and circular grid lines and is tinted green to subtly reflect the green in the original six-color Apple logo. -->

As you begin designing your app or game for iOS, start by understanding the following fundamental device characteristics and patterns that distinguish the iOS experience. Using these characteristics and patterns to inform your design decisions can help you provide an app or game that iPhone users appreciate.

**Display.** iPhone has a medium-size, high-resolution display.

**Ergonomics.** People generally hold their iPhone in one or both hands as they interact with it, switching between landscape and portrait orientations as needed. While people are interacting with the device, their viewing distance tends to be no more than a foot or two.

**Inputs.** Multi-Touch [gestures](https://developer.apple.com/design/human-interface-guidelines/gestures), [virtual keyboards](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards), and [voice](https://developer.apple.com/design/human-interface-guidelines/siri) control let people perform actions and accomplish meaningful tasks while they’re on the go. In addition, people often want apps to use their [personal data](https://developer.apple.com/design/human-interface-guidelines/privacy) and input from the device’s [gyroscope and accelerometer](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer), and they may also want to participate in [spatial interactions](https://developer.apple.com/design/human-interface-guidelines/spatial-interactions).

**App interactions.** Sometimes, people spend just a minute or two checking on event or social media updates, tracking data, or sending messages. At other times, people can spend an hour or more browsing the web, playing games, or enjoying media. People typically have multiple apps open at the same time, and they appreciate switching frequently among them.

**System features.** iOS provides several features that help people interact with the system and their apps in familiar, consistent ways.

  * [Widgets](https://developer.apple.com/design/human-interface-guidelines/widgets)

  * [Home Screen quick actions](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions)

  * [Spotlight](https://developer.apple.com/design/human-interface-guidelines/searching)

  * [Shortcuts](https://developer.apple.com/design/human-interface-guidelines/siri#Shortcuts-and-suggestions)

  * [Activity views](https://developer.apple.com/design/human-interface-guidelines/activity-views)




## [Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Best-practices)

Great iPhone experiences integrate the platform and device capabilities that people value most. To help your design feel at home in iOS, prioritize the following ways to incorporate these features and capabilities.

  * Help people concentrate on primary tasks and content by limiting the number of onscreen controls while making secondary details and actions discoverable with minimal interaction.

  * Adapt seamlessly to appearance changes — like device orientation, Dark Mode, and Dynamic Type — letting people choose the configurations that work best for them.

  * Support interactions that accommodate the way people usually hold their device. For example, it tends to be easier and more comfortable for people to reach a control when it’s located in the middle or bottom area of the display, so it’s especially important let people swipe to navigate back or initiate actions in a list row.

  * With people’s permission, integrate information available through platform capabilities in ways that enhance the experience without asking people to enter data. For example, you might accept payments, provide security through biometric authentication, or offer features that use the device’s location.




## [Resources](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Related)

[Apple Design Resources](https://developer.apple.com/design/resources/#ios-apps)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Developer-documentation)

[iOS Pathway](https://developer.apple.com/ios/get-started/)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios#Videos)

[<!-- image:  --> Meet Liquid Glass ](https://developer.apple.com/videos/play/wwdc2025/219)

[<!-- image:  --> Get to know the new design system ](https://developer.apple.com/videos/play/wwdc2025/356)

---

## Reference: Designing For Ipados

---
title: "Designing for iPadOS | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados

# Designing for iPadOS

People value the power, mobility, and flexibility of iPad as they enjoy media, play games, perform detailed productivity tasks, and bring their creations to life.

<!-- image: A stylized representation of an iPad frame shown on top of a grid. The image is overlaid with rectangular and circular grid lines and is tinted green to subtly reflect the green in the original six-color Apple logo. -->

As you begin designing your app or game for iPad, start by understanding the following fundamental device characteristics and patterns that distinguish the iPadOS experience. Using these characteristics and patterns to inform your design decisions can help you provide an app or game that iPad users appreciate.

**Display.** iPad has a large, high-resolution display.

**Ergonomics.** People often hold their iPad while using it, but they might also set it on a surface or place it on a stand. Positioning the device in different ways can change the viewing distance, although people are typically within about 3 feet of the device as they interact with it.

**Inputs.** People can interact with iPad using Multi-Touch [gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) and [virtual keyboards](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards), an attached [keyboard](https://developer.apple.com/design/human-interface-guidelines/keyboards) or [pointing device](https://developer.apple.com/design/human-interface-guidelines/pointing-devices), [Apple Pencil](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble), or [voice](https://developer.apple.com/design/human-interface-guidelines/siri), and they often combine multiple input modes.

**App interactions.** Sometimes, people perform a few quick actions on their iPad. At other times, they spend hours immersed in games, media, content creation, or productivity tasks. People frequently have multiple apps open at the same time, and they appreciate viewing more than one app onscreen at once and taking advantage of inter-app capabilities like drag and drop.

**System features.** iPadOS provides several features that help people interact with the system and their apps in familiar, consistent ways.

  * [Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking)

  * [Widgets](https://developer.apple.com/design/human-interface-guidelines/widgets)

  * [Drag and drop](https://developer.apple.com/design/human-interface-guidelines/drag-and-drop)




## [Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Best-practices)

Great iPad experiences integrate the platform and device capabilities that people value most. To help your experience feel at home in iPadOS, prioritize the following ways to incorporate these features and capabilities.

  * Take advantage of the large display to elevate the content people care about, minimizing modal interfaces and full-screen transitions, and positioning onscreen controls where they’re easy to reach, but not in the way.

  * Use viewing distance and input mode to help you determine the size and density of the onscreen content you display.

  * Let people use Multi-Touch gestures, a physical keyboard or trackpad, or Apple Pencil, and consider supporting unique interactions that combine multiple input modes.

  * Adapt seamlessly to appearance changes — like device orientation, multitasking modes, Dark Mode, and Dynamic Type — and transition effortlessly to running in macOS, letting people choose the configurations that work best for them.




## [Resources](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Related)

[Apple Design Resources](https://developer.apple.com/design/resources/#ios-apps)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Developer-documentation)

[iPadOS Pathway](https://developer.apple.com/ipados/get-started/)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados#Videos)

[<!-- image:  --> Elevate the design of your iPad app ](https://developer.apple.com/videos/play/wwdc2025/208)

[<!-- image:  --> Meet Liquid Glass ](https://developer.apple.com/videos/play/wwdc2025/219)

[<!-- image:  --> Get to know the new design system ](https://developer.apple.com/videos/play/wwdc2025/356)

---

## Reference: Designing For Macos

---
title: "Designing for macOS | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/designing-for-macos

# Designing for macOS

People rely on the power, spaciousness, and flexibility of a Mac as they perform in-depth productivity tasks, view media or content, and play games, often using several apps at once.

<!-- image: A stylized representation of a Mac shown on top of a grid. The image is overlaid with rectangular and circular grid lines and is tinted green to subtly reflect the green in the original six-color Apple logo. -->

As you begin designing your app or game for macOS, start by understanding the fundamental device characteristics and patterns that distinguish the macOS experience. Using these characteristics and patterns to inform your design decisions can help you provide an app or game that Mac users appreciate.

**Display.** A Mac typically has a large, high-resolution display, and people can extend their workspace by connecting additional displays, including their iPad.

**Ergonomics.** People generally use a Mac while they’re stationary, often placing the device on a desk or table. In the typical use case, the viewing distance can range from about 1 to 3 feet.

**Inputs.** People expect to enter data and control the interface using any combination of input modes, such as physical [Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards), [Pointing devices](https://developer.apple.com/design/human-interface-guidelines/pointing-devices), [Game controls](https://developer.apple.com/design/human-interface-guidelines/game-controls), and [Siri](https://developer.apple.com/design/human-interface-guidelines/siri).

**App interactions.** Interactions can last anywhere from a few minutes of performing some quick tasks to several hours of deep concentration. People frequently have multiple apps open at the same time, and they expect smooth transitions between active and inactive states as they switch from one app to another.

**System features.** macOS provides several features that help people interact with the system and their apps in familiar, consistent ways.

  * [The menu bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar)

  * [File management](https://developer.apple.com/design/human-interface-guidelines/file-management)

  * [Going full screen](https://developer.apple.com/design/human-interface-guidelines/going-full-screen)

  * [Dock menus](https://developer.apple.com/design/human-interface-guidelines/dock-menus)




## [Best practices](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Best-practices)

Great Mac experiences integrate the platform and device capabilities that people value most. To help your design feel at home in macOS, prioritize the following ways to incorporate these features and capabilities.

  * Leverage large displays to present more content in fewer nested levels and with less need for modality, while maintaining a comfortable information density that doesn’t make people strain to view the content they want.

  * Let people resize, hide, show, and move your windows to fit their work style and device configuration, and support full-screen mode to offer a distraction-free context.

  * Use the menu bar to give people easy access to all the commands they need to do things in your app.

  * Help people take advantage of high-precision input modes to perform pixel-perfect selections and edits.

  * Handle keyboard shortcuts to help people accelerate actions and use keyboard-only work styles.

  * Support personalization, letting people customize toolbars, configure windows to display the views they use most, and choose the colors and fonts they want to see in the interface.




## [Resources](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Related)

[Apple Design Resources](https://developer.apple.com/design/resources/#macos-apps)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Developer-documentation)

[macOS Pathway](https://developer.apple.com/macos/get-started/)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/designing-for-macos#Videos)

[<!-- image:  --> Meet Liquid Glass ](https://developer.apple.com/videos/play/wwdc2025/219)

[<!-- image:  --> Get to know the new design system ](https://developer.apple.com/videos/play/wwdc2025/356)

[<!-- image:  --> Build an AppKit app with the new design ](https://developer.apple.com/videos/play/wwdc2025/310)

---

## Reference: Designing For Tvos

|---  
September 14, 2022| Refined best practices for multiuser support.

---

## Reference: Designing For Visionos

|---  
February 2, 2024| Included a link to Apple Vision Pro User Guide.  
September 12, 2023| Updated intro artwork.  
June 21, 2023| New page.

---

## Reference: Designing For Watchos

|---  
June 5, 2023| Enhanced guidance for providing a glanceable, focused app experience, and emphasized the importance of the Digital Crown in navigation.
