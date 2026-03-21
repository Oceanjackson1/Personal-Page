---
title: "Hig Inputs"
description: "Apple HIG guidance for input methods and interaction patterns: gestures, Apple Pencil, keyboards, game controllers, pointers, Digital Crown, eye tracking, focus system, remotes, spatial..."
category: "development"
source: "community"
author: "Community"
tags: ["hig", "inputs"]
date: 2026-03-20
---

# Apple HIG: Inputs

Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered.

## Key Principles

### General

1. **Support multiple input methods.** Touch, pointer, keyboard, pencil, voice, eyes, hands, controllers. Design for the inputs available on each platform. On iPadOS, support both touch and pointer; on macOS, both pointer and keyboard.

2. **Consistent feedback for every input action.** Visible, audible, or haptic response.

### Gestures

3. **Standard gestures must behave consistently.** Tap to activate, swipe to scroll/navigate, pinch to zoom, long press for context menus, drag to move. Don't override system gestures (edge swipes for back, Home, notifications).

4. **Use standard recognizers; keep custom gestures discoverable.** Apple's built-in recognizers handle edge cases and accessibility. If you add non-standard gestures, provide hints or coaching to teach them.

### Apple Pencil

5. **Precision drawing, markup, and selection.** Support pressure, tilt, and hover. Distinguish finger from Pencil when appropriate (finger pans, Pencil draws).

6. **Support Scribble in text fields.** Users expect to write with Pencil in any text input.

### Keyboards

7. **Keyboard shortcuts and full navigation.** Standard shortcuts (Cmd+C/V/Z) plus custom ones visible in the iPadOS Command key overlay. Logical tab order.

8. **Respect the software keyboard.** Adjust layout when keyboard appears. Use keyboard-avoidance APIs.

### Game Controllers

9. **MFi controllers with on-screen fallbacks.** Map to extended gamepad profile, sensible defaults, remappable. Always offer touch or keyboard alternatives.

### Pointer and Trackpad

10. **Native feel.** Hover effects, pointer shape adaptation, standard cursor behaviors. Two-finger scroll, pinch to zoom, swipe to navigate.

### Digital Crown

11. **Primary scrolling and value-adjustment input on watchOS.** Scrolling lists, adjusting values, navigating views. Haptic feedback at detents.

### Eyes and Spatial (visionOS)

12. **Look and pinch.** Generous hit targets (eye tracking is less precise than touch). Avoid sustained gaze for activation. Direct hand manipulation in immersive experiences.

### Focus System

13. **Critical for tvOS and visionOS.** Predictable focus movement. Every interactive element focusable. Clear visual indicators (scale, highlight, elevation). Logical focus groups.

### Remotes

14. **Siri Remote: limited surface.** Touch area for swiping, clickpad for selection, few physical buttons. Keep interactions simple.

### Motion and Nearby

15. **Gyroscope, accelerometer, UWB: use judiciously.** Suits gaming, fitness, AR. Not for essential tasks. Provide calibration and reset. For UWB, communicate distance and direction with visual or haptic cues.

## Reference Index

| Reference | Topic | Key content |
|---|---|---|
| [gestures.md](references/gestures.md) | Touch gestures | Tap, swipe, pinch, long press, drag, system gestures |
| [apple-pencil-and-scribble.md](references/apple-pencil-and-scribble.md) | Apple Pencil | Precision, pressure, tilt, hover, handwriting |
| [keyboards.md](references/keyboards.md) | Keyboards | Shortcuts, navigation, software keyboard, Command key |
| [game-controls.md](references/game-controls.md) | Game controllers | MFi, extended gamepad, remapping, fallbacks |
| [pointing-devices.md](references/pointing-devices.md) | Pointer/trackpad | Hover, cursor morphing, trackpad gestures |
| [digital-crown.md](references/digital-crown.md) | Digital Crown | Scrolling, value adjustment, haptic detents |
| [eyes.md](references/eyes.md) | Eye tracking | Look and tap, gaze targeting, hit target sizing |
| [spatial-interactions.md](references/spatial-interactions.md) | Spatial input | Hand gestures, direct manipulation, immersive input |
| [focus-and-selection.md](references/focus-and-selection.md) | Focus system | tvOS/visionOS navigation, focus indicators, groups |
| [remotes.md](references/remotes.md) | Remotes | Touch surface, clickpad, simple interactions |
| [gyro-and-accelerometer.md](references/gyro-and-accelerometer.md) | Motion sensors | Gyroscope, accelerometer, calibration, gaming |
| [nearby-interactions.md](references/nearby-interactions.md) | Nearby interactions | U1 chip, directional finding, proximity triggers |
| [camera-control.md](references/camera-control.md) | Camera Control | iPhone camera hardware button, quick launch |

## Output Format

1. **Input method recommendations by platform** and how they interact.
2. **Gesture specification table** -- standard and custom gestures with expected behaviors.
3. **Keyboard shortcut recommendations** following system conventions.
4. **Accessibility input alternatives** for VoiceOver, Switch Control, etc.

## Questions to Ask

1. Which platforms and input devices?
2. Productivity or casual app?
3. Custom gestures in the design?
4. Game controller support needed?

## Related Skills

- **hig-components-status** -- Progress indicators responding to input (pull-to-refresh)
- **hig-components-system** -- System experiences with unique input constraints
- **hig-technologies** -- VoiceOver, Siri voice input, ARKit spatial gesture context

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Apple Pencil And Scribble

|---  
May 7, 2024| Added guidance for handling squeeze and barrel roll on Apple Pencil Pro.  
September 12, 2023| Updated artwork.  
November 3, 2022| Added guidelines for using hover to enhance your app.

---

## Reference: Camera Control

|---  
September 9, 2024| New page.

---

## Reference: Digital Crown

|---  
December 5, 2023| Added artwork for Apple Vision Pro and Apple Watch, and clarified that visionOS apps don’t receive direct information from the Digital Crown.  
June 21, 2023| Updated to include guidance for visionOS.  
June 5, 2023| Added guidelines emphasizing the central role of the Digital Crown for navigation.

---

## Reference: Eyes

|---  
June 10, 2024| Added guidance for custom hover effects.  
March 29, 2024| Added artwork showing the visionOS hover effect.  
October 24, 2023| Clarified the difference between focus effects and the visionOS hover effect.  
June 21, 2023| New page.

---

## Reference: Focus And Selection

|---  
<!-- image: An image of an unfocused button on top of a photograph. A small drop shadow makes it appear very close to the content behind it, with a translucent background infused by the colors of the content, and a high-contrast text color. -->| The viewer hasn’t brought focus to the item. Unfocused items appear less prominent than focused items.  
<!-- image: An image of a focused button on top of a photograph. It’s larger than an unfocused button, and a drop shadow makes it appear farther away from the content behind it, with an opaque white background and a black text label. -->| The viewer brings focus to the item. A focused item visually stands out from the other onscreen content through elevation to the foreground, illumination, and animation.  
<!-- image: An image of a highlighted button on top of a photograph. It’s the same size as an unfocused button, and a drop shadow makes it appear a little farther away from the surface of the content behind it, with an opaque white background and a black text label. -->| The viewer chooses the focused item. A focused item provides instant visual feedback when people choose it. For example, a button might briefly invert its colors and animate before it transitions to its selected appearance.  
<!-- image: An image of a selected button on top of a photograph. It’s the same size as an unfocused button, and a small drop shadow makes it appear very close to the content behind it, with an opaque white background and a black text label. -->| The viewer has chosen or activated the item in some way. For example, a heart-shaped button that people can use to favorite a photo might appear filled in the selected state and empty in the deselected state.  
<!-- image: An image of an unavailable button on top of a photograph. It’s the same size as an unfocused button. It lacks a drop shadow and appears to rest directly on the content behind it, with a translucent background tinted by the the colors of nearby content, and a low-contrast text color. -->| The viewer can’t bring focus to the item or choose it. An unavailable item appears inactive.  
  
For developer guidance, see [Adding user-focusable elements to a tvOS app](https://developer.apple.com/documentation/UIKit/adding-user-focusable-elements-to-a-tvos-app).

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#visionOS)

visionOS supports the same focus system as in iPadOS and tvOS, letting people use a connected input device like a keyboard or game controller to interact with apps and the system.

Note

When people look at a virtual object to identify it as the object they want to interact with, the system uses the _hover effect_ , not a focus effect, to provide visual feedback (for guidance, see [Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes)). The hover effect isn’t related to the focus system.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Related)

[Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes)

[Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Developer-documentation)

[Focus Attributes](https://developer.apple.com/documentation/TVML/focus-attributes) — TVML

[Focus-based navigation](https://developer.apple.com/documentation/UIKit/focus-based-navigation) — UIKit

[About focus interactions for Apple TV](https://developer.apple.com/documentation/UIKit/about-focus-interactions-for-apple-tv) — UIKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Videos)

[<!-- image:  --> Design for spatial input ](https://developer.apple.com/videos/play/wwdc2023/10073)

[<!-- image:  --> Design for spatial user interfaces ](https://developer.apple.com/videos/play/wwdc2023/10076)

[<!-- image:  --> Design for the iPadOS pointer ](https://developer.apple.com/videos/play/wwdc2020/10640)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection#Change-log)

Date| Changes  
---|---  
October 24, 2023| Clarified the difference between focus effects and the visionOS hover effect.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Game Controls

|---  
A| Activates a control  
B| Cancels an action or returns to previous screen  
X| —  
Y| —  
Left shoulder| Navigates left to a different screen or section  
Right shoulder| Navigates right to a different screen or section  
Left trigger| —  
Right trigger| —  
Left/right thumbstick| Moves selection  
Directional pad| Moves selection  
Home/logo| Reserved for system controls  
Menu| Opens game settings or pauses gameplay  
  
**Support multiple connected controllers.** If there are multiple controllers connected, use labels and glyphs that match the one that the player is actively using. If your game supports multiplayer, use the appropriate labels and symbols when referring to a specific player’s controller. If you need to refer to buttons on multiple controllers, consider listing them together.

**Prefer using symbols, not text, to refer to game controller elements.** The Game Controller framework makes [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) available for most elements, including the buttons on various brands of game controllers. Using symbols instead of text descriptions can be especially helpful for players who aren’t experienced with controllers because it doesn’t require them to hunt for a specific button label during gameplay.

<!-- image: A screenshot of the SF Symbols app showing symbols in the Gaming category. -->

## [Keyboards](https://developer.apple.com/design/human-interface-guidelines/game-controls#Keyboards)

Keyboard players appreciate using keyboard bindings to speed up their interactions with apps and games.

**Prioritize single-key commands.** Single-key commands are generally easier and faster for players to perform, especially while they’re simultaneously using a mouse or trackpad. For example, you might use the first letter of a menu item as a shortcut, such as I for Inventory or M for Map; you might also map the game’s main action to the Space bar, taking advantage of the key’s relatively large size.

**Test key binding comfort game using an Apple keyboard.** For example, if a key binding uses the Control key (^) on a non-Apple keyboard, consider remapping it to the Command key (⌘) on an Apple keyboard. On Apple keyboards, the Command key is conveniently located next to the Space bar, making it especially easy to reach when players are using the W, A, S, and D keys.

**Take the proximity of keys into account.** For example, if players navigate using the W, A, S, and D keys, consider using nearby keys to define other high-value commands. Similarly, if there’s a group of closely related actions, it can work well to map their bindings to keys that are physically close together, such as using the number keys for inventory categories.

**Let players customize key bindings.** Although players tend to expect a reasonable set of defaults, many people need to customize a game’s key bindings for personal comfort and play style.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/game-controls#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, or tvOS. Not supported in watchOS._

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/game-controls#visionOS)

**Match spatial game controller behavior to hand input.** In addition to supporting a wide array of wireless game controllers, your visionOS game can also support spatial game controllers such as PlayStation VR2 Sense controller. Allow players to interact with your game in a similar manner to how they interact using their hands. Specifically, support looking at an object and pressing the controller’s left or right trigger button to indirectly interact, or reaching out and pressing the left or right trigger button to directly interact. For more information, see [visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS).

## [Resources](https://developer.apple.com/design/human-interface-guidelines/game-controls#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/game-controls#Related)

[Designing for games](https://developer.apple.com/design/human-interface-guidelines/designing-for-games)

[Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures)

[Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards)

[Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/game-controls#Developer-documentation)

[Create games for Apple platforms](https://developer.apple.com/games/)

[Touch Controller](https://developer.apple.com/documentation/TouchController)

[Game Controller](https://developer.apple.com/documentation/GameController)

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/game-controls#Videos)

[<!-- image:  --> Design advanced games for Apple platforms ](https://developer.apple.com/videos/play/wwdc2024/10085)

[<!-- image:  --> Tap into virtual and physical game controllers ](https://developer.apple.com/videos/play/wwdc2021/10081)

[<!-- image:  --> Explore game input in visionOS ](https://developer.apple.com/videos/play/wwdc2024/10094)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/game-controls#Change-log)

Date| Changes  
---|---  
June 9, 2025| Updated touch control best practices, updated game controller mapping for UI, and added guidance for spatial game controller support in visionOS.  
June 10, 2024| Added guidance for supporting touch controls and changed title from Game controllers.

---

## Reference: Gestures

|---  
Three-finger swipe| Initiate undo (left swipe); initiate redo (right swipe).  
Three-finger pinch| Copy selected text (pinch in); paste copied text (pinch out).  
Four-finger swipe (iPadOS only)| Switch between apps.  
Shake| Initiate undo; initiate redo.  
  
**Consider allowing simultaneous recognition of multiple gestures if it enhances the experience.** Although simultaneous gestures are unlikely to be useful in nongame apps, a game might include multiple onscreen controls — such as a joystick and firing buttons — that people can operate at the same time. For guidance on integrating touchscreen input with Apple Pencil input in your iPadOS app, see [Apple Pencil and Scribble](https://developer.apple.com/design/human-interface-guidelines/apple-pencil-and-scribble).

### [macOS](https://developer.apple.com/design/human-interface-guidelines/gestures#macOS)

People primarily interact with macOS using a [keyboard](https://developer.apple.com/design/human-interface-guidelines/keyboards) and mouse. In addition, they can make [standard gestures](https://developer.apple.com/design/human-interface-guidelines/gestures#Standard-gestures) on a Magic Trackpad, Magic Mouse, or a [game controller](https://developer.apple.com/design/human-interface-guidelines/game-controls) that includes a touch surface.

### [tvOS](https://developer.apple.com/design/human-interface-guidelines/gestures#tvOS)

People expect to use [standard gestures](https://developer.apple.com/design/human-interface-guidelines/gestures#Standard-gestures) to navigate tvOS apps and games with a compatible remote, Siri Remote, or [game controller](https://developer.apple.com/design/human-interface-guidelines/game-controls) that includes a touch surface. For guidance, see [Remotes](https://developer.apple.com/design/human-interface-guidelines/remotes).

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#visionOS)

visionOS supports two categories of gestures: indirect and direct.

People use an _indirect_ gesture by looking at an object to target it, and then manipulating that object from a distance — indirectly — with their hands. For example, a person can look at a button to focus it and select it by quickly tapping their finger and thumb together. Indirect gestures are comfortable to perform at any distance, and let people quickly change focus between different objects and select items with minimal movement.

Video with custom controls. 

Content description: A recording showing a closeup view of the top portion of a window in visionOS. A button in the window becomes highlighted. A picture-in-picture window is visible in the bottom-right corner of the recording. It shows a person's hand performing the indirect tap gesture. In response to the gesture, the highlighted button in the window activates. 

Play 

People use a _direct_ gesture to physically touch an interactive object. For example, people can directly type on the visionOS keyboard by tapping the virtual keys. Direct gestures work best when they are within reach. Because people may find it tiring to keep their arms raised for extended periods, direct gestures are best for infrequent use. visionOS also supports direct versions of all standard gestures, allowing people the choice to interact directly or indirectly with any standard component.

Video with custom controls. 

Content description: A recording showing a table with a vertical stack of three virtual cubic blocks on it in visionOS. A person moves their hand toward the blocks from right to left, and their extended fingers touch and push aside the center block. The center block falls to the side, and the other block also tumbles onto the tabletop. 

Play 

Here are the standard direct gestures people use in visionOS; see [Specifications](https://developer.apple.com/design/human-interface-guidelines/gestures#Specifications) for a list of standard indirect gestures.

Direct gesture| Common use  
---|---  
Touch| Directly select or activate an object.  
Touch and hold| Open a contextual menu.  
Touch and drag| Move an object to a new location.  
Double touch| Preview an object or file; select a word in an editing context.  
Swipe| Reveal actions and controls; dismiss views; scroll.  
With two hands, pinch and drag together or apart| Zoom in or out.  
With two hands, pinch and drag in a circular motion| Rotate an object.  
  
**Support standard gestures everywhere you can.** For example, as soon as someone looks at an object in your app or game, tap is the first gesture they’re likely to make when they want to select or activate it. Even if you also support custom gestures, supporting standard gestures such as tap helps people get comfortable with your app or game quickly.

**Offer both indirect and direct interactions when possible.** Prefer indirect gestures for UI and common components like buttons. Reserve direct gestures and custom gestures for objects that invite close-up interaction or specific motions in a game or interactive experience.

**Avoid requiring specific body movements or positions for input.** Not all people can perform specific body movements or position themselves in certain ways at all times, whether due to disability, spatial constraints, or other environmental factors. If your experience requires movement, consider supporting alternative inputs to let people choose the interaction method that works best for them.

#### [Designing custom gestures in visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#Designing-custom-gestures-in-visionOS)

If you want to offer a specific interaction for your experience that people can’t perform using an existing system gesture, consider designing a custom gesture. To offer this type of interaction, your app needs to be running in a Full Space, and you must request people’s permission to access information about their hands. For developer guidance, see [Setting up access to ARKit data](https://developer.apple.com/documentation/visionOS/setting-up-access-to-arkit-data).

<!-- image: A screenshot of a person's hands performing a custom gesture, placing the two hands together to form a heart, while playing a visionOS game. -->

**Prioritize comfort.** Continually test ergonomics of all interactions that require custom gestures. A custom interaction that requires people to keep their arms raised for even a little while can be physically tiring, and repeating very similar movements many times in succession can stress people’s muscles and joints.

**Carefully consider complex custom gestures that involve multiple fingers or both hands.** People may not always have both hands available when using your app or game. If you require a more complex gesture for your experience, consider also offering an alternative that requires less movement.

**Avoid custom gestures that require using a specific hand.** It can increase someone’s cognitive load if they need to remember which hand to use to trigger a custom gesture. It may also make your experience less welcoming to people with strong hand-dominance or limb differences.

#### [Working with system overlays in visionOS](https://developer.apple.com/design/human-interface-guidelines/gestures#Working-with-system-overlays-in-visionOS)

In visionOS 2 and later, people can look at the palm of one hand and use gestures to quickly access system overlays for Home and Control Center. These interactions are available systemwide, and are reserved solely for accessing system overlays.

Note

The system overlay is the default method of accessing Control Center in visionOS 2 and later. The visionOS 1 behavior (looking upward) remains available as an accessibility setting.

When designing apps and games that use custom gestures or anchor content to a person’s hands, it’s important to take interactions with the system overlays into consideration.

**Reserve the area around a person’s hand for system overlays and their related gestures.** If possible, don’t anchor content to a person’s hands or wrists. If you’re designing a game that involves hand-anchored content, place it outside of the immediate area of someone’s hand to avoid colliding with the Home indicator.

<!-- image: An illustration of a person's open hand with the palm facing upward. A dashed circular line above the hand indicates the area reserved for system overlays. -->The area reserved for interacting with system overlays.

<!-- image: An illustration of a person's open hand with the palm facing upward. A button with a circle icon representing the Home indicator appears above the palm. -->A person looks at their palm to reveal the Home indicator.

<!-- image: An illustration of a person's open hand with the palm facing downward. An overlay with the status bar appears above the hand. -->A person turns their hand to reveal the status bar, and can tap to open Control Center.

**Consider deferring the system overlay behavior when designing an immersive app or game.** In certain circumstances, you may not want the Home indicator to appear when someone looks at the palm of their hand. For example, a game that uses virtual hands or gloves may want to keep someone within the world of the story, even if they happen to look at their hands from different angles. In such cases, when your app is running in a Full Space, you can choose to require a tap to reveal the Home indicator instead. For developer guidance, see [`persistentSystemOverlays(_:)`](https://developer.apple.com/documentation/SwiftUI/View/persistentSystemOverlays\(_:\)).

<!-- image: An image of a person's open hand with the palm facing upward, shown from the person's perspective. A button with a circle icon representing the Home indicator appears above the palm. The image background shows the room that's the person's surroundings. -->Default behavior in the Shared Space

<!-- image: An image of a person's open hand with the palm facing upward, shown from the person's perspective. A button with a circle icon representing the Home indicator appears above the palm. The image background shows a forest in a fully immersive space. -->Default behavior in a Full Space

<!-- image: An image of a person's open hand wearing a bulky space suit glove, shown from the person's perspective. The palm faces upward, and no button appears above it. The image background shows a starry sky in a fully immersive space. -->Deferred behavior in a Full Space

Note

Apps and games that you built for visionOS 1 defer the system overlay behavior by default. When a person looks at their palm with your app running in a Full Space, the Home indicator won’t appear unless they tap first.

**Use caution when designing custom gestures that involve a rolling motion of the hand, wrist, and forearm.** This specific motion is reserved for revealing system overlays. Since system overlays always display on top of app content and your app isn’t aware of when they’re visible, it’s important to test any custom gestures or content that might conflict.

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/gestures#watchOS)

#### [Double tap](https://developer.apple.com/design/human-interface-guidelines/gestures#Double-tap)

In watchOS 11 and later, people can use the double-tap gesture to scroll through lists and scroll views, and to advance between vertical tab views. Additionally, you can specify a toggle or button as the primary action in your app, or in your widget or Live Activity when the system displays it in the Smart Stack. Double-tapping in a view with a primary action highlights the control and then performs the action. The system also supports double tap for custom actions that you offer in [notifications](https://developer.apple.com/design/human-interface-guidelines/notifications), where it acts on the first nondestructive action in the notification.

**Avoid setting a primary action in views with lists, scroll views, or vertical tabs.** This conflicts with the default navigation behaviors that people expect when they double-tap.

**Choose the button that people use most commonly as the primary action in a view.** Double tap is helpful in a nonscrolling view when it performs the action that people use the most. For example, in a media controls view, you could assign the primary action to the play/pause button. For developer guidance, see [`handGestureShortcut(_:isEnabled:)`](https://developer.apple.com/documentation/SwiftUI/View/handGestureShortcut\(_:isEnabled:\)) and [`primaryAction`](https://developer.apple.com/documentation/SwiftUI/HandGestureShortcut/primaryAction).

## [Specifications](https://developer.apple.com/design/human-interface-guidelines/gestures#Specifications)

### [Standard gestures](https://developer.apple.com/design/human-interface-guidelines/gestures#Standard-gestures)

The system provides APIs that support the familiar gestures people use with their devices, whether they use a touchscreen, an indirect gesture in visionOS, or an input device like a trackpad, mouse, remote, or game controller. For developer guidance, see [Gestures](https://developer.apple.com/documentation/SwiftUI/Gestures).

Gesture| Supported in| Common action  
---|---|---  
Tap| iOS, iPadOS, macOS, tvOS, visionOS, watchOS| Activate a control; select an item.  
Swipe| iOS, iPadOS, macOS, tvOS, visionOS, watchOS| Reveal actions and controls; dismiss views; scroll.  
Drag| iOS, iPadOS, macOS, tvOS, visionOS, watchOS| Move a UI element.  
Touch (or pinch) and hold| iOS, iPadOS, tvOS, visionOS, watchOS| Reveal additional controls or functionality.  
Double tap| iOS, iPadOS, macOS, tvOS, visionOS, watchOS| Zoom in; zoom out if already zoomed in; perform a primary action on Apple Watch Series 9 and Apple Watch Ultra 2.  
Zoom| iOS, iPadOS, macOS, tvOS, visionOS| Zoom a view; magnify content.  
Rotate| iOS, iPadOS, macOS, tvOS, visionOS| Rotate a selected item.  
  
For guidance on supporting additional gestures and button presses on specific input devices, see [Pointing devices](https://developer.apple.com/design/human-interface-guidelines/pointing-devices), [Remotes](https://developer.apple.com/design/human-interface-guidelines/remotes), and [Game controls](https://developer.apple.com/design/human-interface-guidelines/game-controls).

## [Resources](https://developer.apple.com/design/human-interface-guidelines/gestures#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/gestures#Related)

[Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)

[Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes)

[Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/gestures#Developer-documentation)

[Gestures](https://developer.apple.com/documentation/SwiftUI/Gestures) — SwiftUI

[`UITouch`](https://developer.apple.com/documentation/UIKit/UITouch) — UIKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/gestures#Videos)

[<!-- image:  --> Enhance your UI animations and transitions ](https://developer.apple.com/videos/play/wwdc2024/10145)

[<!-- image:  --> Design for spatial input ](https://developer.apple.com/videos/play/wwdc2023/10073)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/gestures#Change-log)

Date| Changes  
---|---  
September 9, 2024| Added guidance for working with system overlays in visionOS and made organizational updates.  
September 15, 2023| Updated specifications to include double tap in watchOS.  
June 21, 2023| Changed page title from Touchscreen gestures and updated to include guidance for visionOS.

---

## Reference: Gyro And Accelerometer

---
title: "Gyroscope and accelerometer | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer

# Gyroscope and accelerometer

On-device gyroscopes and accelerometers can supply data about a device’s movement in the physical world.

<!-- image: A sketch of a gyroscope, suggesting movement. The image is overlaid with rectangular and circular grid lines and is tinted purple to subtly reflect the purple in the original six-color Apple logo. -->

You can use accelerometer and gyroscope data to provide experiences based on real-time, motion-based information in apps and games that run in iOS, iPadOS, and watchOS. tvOS apps can use gyroscope data from the Siri Remote. For developer guidance, see [Core Motion](https://developer.apple.com/documentation/CoreMotion).

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Best-practices)

**Use motion data only to offer a tangible benefit to people.** For example, a fitness app might use the data to provide feedback about people’s activity and general health, and a game might use the data to enhance gameplay. Avoid gathering data simply to have the data.

Important

If your experience needs to access motion data from a device, you must provide copy that explains why. The first time your app or game tries to access this type of data, the system includes your copy in a permission request, where people can grant or deny access.

**Outside of active gameplay, avoid using accelerometers or gyroscopes for the direct manipulation of your interface.** Some motion-based gestures may be difficult to replicate precisely, may be physically challenging for some people to perform, and may affect battery usage.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Related)

[Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Developer-documentation)

[Getting processed device-motion data](https://developer.apple.com/documentation/CoreMotion/getting-processed-device-motion-data) — Core Motion

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/gyro-and-accelerometer#Videos)

[<!-- image:  --> Measure health with motion ](https://developer.apple.com/videos/play/wwdc2021/10287)

---

## Reference: Keyboards

|---|---  
Space| Command-Space| Show or hide the Spotlight search field.  
| Shift-Command-Space| Varies.  
| Option-Command-Space| Show the Spotlight search results window.  
| Control-Command-Space| Show the Special Characters window.  
Tab| Shift-Tab| Navigate through controls in a reverse direction.  
| Command-Tab| Move forward to the next most recently used app in a list of open apps.  
| Shift-Command-Tab| Move backward through a list of open apps (sorted by recent use).  
| Control-Tab| Move focus to the next group of controls in a dialog or the next table (when Tab moves to the next cell).  
| Control-Shift-Tab| Move focus to the previous group of controls.  
Esc| Esc| Cancel the current action or process.  
Esc| Option-Command-Esc| Open the Force Quit dialog.  
Eject| Control-Command-Eject| Quit all apps (after changes have been saved to open documents) and restart the computer.  
| Control-Option-Command-Eject| Quit all apps (after changes have been saved to open documents) and shut the computer down.  
F1| Control-F1| Toggle full keyboard access on or off.  
F2| Control-F2| Move focus to the menu bar.  
F3| Control- F3| Move focus to the Dock.  
F4| Control-F4| Move focus to the active (or next) window.  
| Control-Shift-F4| Move focus to the previously active window.  
F5| Control-F5| Move focus to the toolbar.  
| Command-F5| Turn VoiceOver on or off.  
F6| Control-F6| Move focus to the first (or next) panel.  
| Control-Shift-F6| Move focus to the previous panel.  
F7| Control-F7| Temporarily override the current keyboard access mode in windows and dialogs.  
F8| | Varies.  
F9| | Varies.  
F10| | Varies.  
F11| | Show desktop.  
F12| | Hide or display Dashboard.  
Grave accent (`)| Command-Grave accent| Activate the next open window in the frontmost app.  
| Shift-Command-Grave accent| Activate the previous open window in the frontmost app.  
| Option-Command-Grave accent| Move focus to the window drawer.  
Hyphen (-)| Command-Hyphen| Decrease the size of the selection.  
| Option-Command-Hyphen| Zoom out when screen zooming is on.  
Left bracket ({)| Command-Left bracket| Left-align a selection.  
Right bracket (})| Command-Right bracket| Right-align a selection.  
Pipe (|)| Command-Pipe| Center-align a selection.  
Colon (:)| Command-Colon| Display the Spelling window.  
Semicolon (;)| Command-Semicolon| Find misspelled words in the document.  
Comma (,)| Command-Comma| Open the app’s settings window.  
| Control-Option-Command-Comma| Decrease screen contrast.  
Period (.)| Command-Period| Cancel an operation.  
| Control-Option-Command-Period| Increase screen contrast.  
Question mark (?)| Command-Question mark| Open the app’s Help menu.  
Forward slash (/)| Option-Command-Forward slash| Turn font smoothing on or off.  
Equal sign (=)| Shift-Command-Equal sign| Increase the size of the selection.  
| Option-Command-Equal sign| Zoom in when screen zooming is on.  
3| Shift-Command-3| Capture the screen to a file.  
| Control-Shift-Command-3| Capture the screen to the Clipboard.  
4| Shift-Command-4| Capture a selection to a file.  
| Control-Shift-Command-4| Capture a selection to the Clipboard.  
8| Option-Command-8| Turn screen zooming on or off.  
| Control-Option-Command-8| Invert the screen colors.  
A| Command-A| Select every item in a document or window, or all characters in a text field.  
| Shift-Command-A| Deselect all selections or characters.  
B| Command-B| Boldface the selected text or toggle boldfaced text on and off.  
C| Command-C| Copy the selection to the Clipboard.  
| Shift-Command-C| Display the Colors window.  
| Option-Command-C| Copy the style of the selected text.  
| Control-Command-C| Copy the formatting settings of the selection and store on the Clipboard.  
D| Option-Command-D| Show or hide the Dock.  
| Control-Command-D| Display the definition of the selected word in the Dictionary app.  
E| Command-E| Use the selection for a find operation.  
F| Command-F| Open a Find window.  
| Option-Command-F| Jump to the search field control.  
| Control-Command-F| Enter full screen.  
G| Command-G| Find the next occurrence of the selection.  
| Shift-Command-G| Find the previous occurrence of the selection.  
H| Command-H| Hide the windows of the currently running app.  
| Option-Command-H| Hide the windows of all other running apps.  
I| Command-I| Italicize the selected text or toggle italic text on or off.  
| Command-I| Display an Info window.  
| Option-Command-I| Display an inspector window.  
J| Command-J| Scroll to a selection.  
M| Command-M| Minimize the active window to the Dock.  
| Option-Command-M| Minimize all windows of the active app to the Dock.  
N| Command-N| Open a new document.  
O| Command-O| Display a dialog for choosing a document to open.  
P| Command-P| Display the Print dialog.  
| Shift-Command-P| Display the Page Setup dialog.  
Q| Command-Q| Quit the app.  
| Shift-Command-Q| Log out the person currently logged in.  
| Option-Shift-Command-Q| Log out the person currently logged in without confirmation.  
S| Command-S| Save a new document or save a version of a document.  
| Shift-Command-S| Duplicate the active document or initiate a Save As.  
T| Command-T| Display the Fonts window.  
| Option-Command-T| Show or hide a toolbar.  
U| Command-U| Underline the selected text or turn underlining on or off.  
V| Command-V| Paste the Clipboard contents at the insertion point.  
| Shift-Command-V| Paste as (Paste as Quotation, for example).  
| Option-Command-V| Apply the style of one object to the selection.  
| Option-Shift-Command-V| Paste the Clipboard contents at the insertion point and apply the style of the surrounding text to the inserted object.  
| Control-Command-V| Apply formatting settings to the selection.  
W| Command-W| Close the active window.  
| Shift-Command-W| Close a file and its associated windows.  
| Option-Command-W| Close all windows in the app.  
X| Command-X| Remove the selection and store on the Clipboard.  
Z| Command-Z| Undo the previous operation.  
| Shift-Command-Z| Redo (when Undo and Redo are separate commands rather than toggled using Command-Z).  
Right arrow| Command-Right arrow| Change the keyboard layout to current layout of Roman script.  
| Shift-Command-Right arrow| Extend selection to the next semantic unit, typically the end of the current line.  
| Shift-Right arrow| Extend selection one character to the right.  
| Option-Shift-Right arrow| Extend selection to the end of the current word, then to the end of the next word.  
| Control-Right arrow| Move focus to another value or cell within a view, such as a table.  
Left arrow| Command-Left arrow| Change the keyboard layout to current layout of system script.  
| Shift-Command-Left arrow| Extend selection to the previous semantic unit, typically the beginning of the current line.  
| Shift-Left arrow| Extend selection one character to the left.  
| Option-Shift-Left arrow| Extend selection to the beginning of the current word, then to the beginning of the previous word.  
| Control-Left arrow| Move focus to another value or cell within a view, such as a table.  
Up arrow| Shift-Command-Up arrow| Extend selection upward in the next semantic unit, typically the beginning of the document.  
| Shift-Up arrow| Extend selection to the line above, to the nearest character boundary at the same horizontal location.  
| Option-Shift-Up arrow| Extend selection to the beginning of the current paragraph, then to the beginning of the next paragraph.  
| Control-Up arrow| Move focus to another value or cell within a view, such as a table.  
Down arrow| Shift-Command-Down arrow| Extend selection downward in the next semantic unit, typically the end of the document.  
| Shift-Down arrow| Extend selection to the line below, to the nearest character boundary at the same horizontal location.  
| Option-Shift-Down arrow| Extend selection to the end of the current paragraph, then to the end of the next paragraph (include the paragraph terminator, such as Return, in cut, copy, and paste operations).  
| Control-Down arrow| Move focus to another value or cell within a view, such as a table.  
  
The system also defines several keyboard shortcuts for use with localized versions of the system, localized keyboards, keyboard layouts, and input methods. These shortcuts don’t correspond directly to menu commands.

Keyboard shortcut| Action  
---|---  
Control-Space| Toggle between the current and last input source.  
Control-Option-Space| Switch to the next input source in the list.  
[Modifier key]-Command-Space| Varies.  
Command-Right arrow| Change keyboard layout to current layout of Roman script.  
Command-Left arrow| Change keyboard layout to current layout of system script.  
  
## [Custom keyboard shortcuts](https://developer.apple.com/design/human-interface-guidelines/keyboards#Custom-keyboard-shortcuts)

**Define custom keyboard shortcuts for only the most frequently used app-specific commands.** People appreciate using keyboard shortcuts for actions they perform frequently, but defining too many new shortcuts can make your app seem difficult to learn.

**Use modifier keys in ways that people expect.** For example, pressing Command while dragging moves items as a group, and pressing Shift while drag-resizing constrains resizing to the item’s aspect ratio. In addition, holding an arrow key moves the selected item by the smallest app-defined unit of distance until people release the key.

Here are the modifier keys and the symbols that represent them.

Modifier key| Symbol| Recommended usage  
---|---|---  
Command| <!-- image: Outline of a stylized clover shape. -->| Prefer the Command key as the main modifier key in a custom keyboard shortcut.  
Shift| <!-- image: Outline of an upward-pointing arrow. -->| Prefer the Shift key as a secondary modifier that complements a related shortcut.  
Option| <!-- image: Line segments that suggest a horizontally transformed Z shape combined with a short horizontal segment aligned with the top of the Z. -->| Use the Option modifier sparingly for less-common commands or power features.  
Control| <!-- image: A shallow, upside-down V shape. -->| Avoid using the Control key as a modifier. The system uses Control in many systemwide features and shortcuts, like moving focus or capturing screenshots.  
  
Tip

Some languages require modifier keys to generate certain characters. For example, on a French keyboard, Option-5 generates the “{“ character. It’s usually safe to use the Command key as a modifier, but avoid using an additional modifier with characters that aren’t available on all keyboards. If you must use a modifier other than Command, prefer using it only with the alphabetic characters.

**List modifier keys in the correct order.** If you use more than one modifier key in a custom shortcut, always list them in this order: Control, Option, Shift, Command.

**Avoid adding Shift to a shortcut that uses the upper character of a two-character key.** People already understand that they must hold the Shift key to type the upper character of a two-character key, so it’s clearer to simply list the upper character in the shortcut. For example, the keyboard shortcut for Hide Status Bar is Command-Slash, whereas the keyboard shortcut for Help is Command-Question mark, not Shift-Command-Slash.

**Let the system localize and mirror your keyboard shortcuts as needed.** The system automatically localizes a shortcut’s primary and modifier keys to support the currently connected keyboard; if your app or game switches to a right-to-left layout, the system automatically mirrors the shortcut. For guidance, see [Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left).

**Avoid creating a new shortcut by adding a modifier to an existing shortcut for an unrelated command.** For example, because people are accustomed to using Command-Z for undoing an action, it would be confusing to use Shift-Command-Z as the shortcut for a command that’s unrelated to undo and redo.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/keyboards#Platform-considerations)

 _No additional considerations for iOS, iPadOS, macOS, or tvOS. Not supported in watchOS._

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/keyboards#visionOS)

In visionOS, an app’s keyboard shortcuts appear in the shortcut interface that displays when people hold the Command key on a connected keyboard. Similar in organization to an app’s [menu bar menus](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar) on iPad or Mac, the shortcut interface on Apple Vision Pro displays app commands in familiar system-defined menu categories such as File, Edit, and View. Unlike menu bar menus, the shortcut interface displays all relevant categories in one view, listing within each category only available commands that also have shortcuts.

**Write descriptive shortcut titles.** Because the shortcut interface displays a flat list of all items in each category, submenu titles aren’t available to provide context for their child items. Make sure each shortcut title is descriptive enough to convey its action without the additional context a submenu title might provide. For developer guidance, see [`discoverabilityTitle`](https://developer.apple.com/documentation/UIKit/UIKeyCommand/discoverabilityTitle).

**Recognize that people see an overlay when they use a physical keyboard with your visionOS app or game.** When people connect a physical keyboard while using your visionOS app or game, the system displays a virtual keyboard overlay that provides typing completion and other controls.

Video with custom controls. 

Content description: A recording that shows two hands typing on a physical keyboard while the person runs an app in visionOS. A virtual window is visible above the physical keyboard, and displays the entered text and suggestions. 

Play 

## [Resources](https://developer.apple.com/design/human-interface-guidelines/keyboards#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/keyboards#Related)

[Virtual keyboards](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards)

[Entering data](https://developer.apple.com/design/human-interface-guidelines/entering-data)

[Pointing devices](https://developer.apple.com/design/human-interface-guidelines/pointing-devices)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/keyboards#Developer-documentation)

[`KeyboardShortcut`](https://developer.apple.com/documentation/SwiftUI/KeyboardShortcut) — SwiftUI

[Input events](https://developer.apple.com/documentation/SwiftUI/Input-events) — SwiftUI

[Handling key presses made on a physical keyboard](https://developer.apple.com/documentation/UIKit/handling-key-presses-made-on-a-physical-keyboard) — UIKit

[Mouse, Keyboard, and Trackpad](https://developer.apple.com/documentation/AppKit/mouse-keyboard-and-trackpad) — AppKit

## [Change log](https://developer.apple.com/design/human-interface-guidelines/keyboards#Change-log)

Date| Changes  
---|---  
June 9, 2025| Moved game-specific key bindings guidance to the Game controls page.  
June 10, 2024| Added game-specific guidance and made organizational updates.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Nearby Interactions

|---  
June 21, 2023| Changed page title from Spatial interactions.

---

## Reference: Pointing Devices

|---|---|---  
Primary click| Select or activate an item, such as a file or button.| ●| ●  
Secondary click| Reveal contextual menus.| ●| ●  
Scrolling| Move content up, down, left, or right within a view.| ●| ●  
Smart zoom| Zoom in or out on content, such as a web page or PDF.| ●| ●  
Swipe between pages| Navigate forward or backward between individually displayed pages.| ●| ●  
Swipe between full-screen apps| Navigate forward or backward between full-screen apps and spaces.| ●| ●  
Mission Control (double-tap the mouse with two fingers or swipe up on the trackpad with three or four fingers)| Activate Mission Control.| ●| ●  
Lookup and data detectors (force click with one finger or tap with three fingers)| Display a lookup window above selected content.| | ●  
Tap to click| Perform the primary click action using a tap rather than a click.| | ●  
Force click| Click then press firmly to display a Quick Look window or lookup window above selected content. Apply a variable amount of pressure to affect pressure-sensitive controls, such as variable speed media controls.| | ●  
Zoom in or out (pinch with two fingers)| Zoom in or out.| | ●  
Rotate (move two fingers in a circular motion)| Rotate content, such as an image.| | ●  
Notification Center (swipe from the edge of the trackpad)| Display Notification Center.| | ●  
App Exposé (swipe down with three or four fingers)| Display the current app’s windows in Exposé.| | ●  
Launchpad (pinch with thumb and three fingers)| Display the Launchpad.| | ●  
Show Desktop (spread with thumb and three fingers)| Slide all windows out of the way to reveal the desktop.| | ●  
  
#### [Pointers](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Pointers)

macOS offers a variety of standard pointer styles, which your app can use to communicate the interactive state of an interface element or the result of a drag operation.

Pointer| Name| Meaning| AppKit API  
---|---|---|---  
<!-- image: A pointer that resembles a diagonal arrow pointing up and to the left. -->| Arrow| Standard pointer for selecting and interacting with content and interface elements.| [`arrow`](https://developer.apple.com/documentation/AppKit/NSCursor/arrow)  
<!-- image: A closed, gloved hand. -->| Closed hand| Dragging to reposition the display of content within a view—for example, dragging a map around in Maps.| [`closedHand`](https://developer.apple.com/documentation/AppKit/NSCursor/closedHand)  
<!-- image: A pointer arrow with a small menu-like square to the right of the arrow. -->| Contextual menu| A contextual menu is available for the content below the pointer. This pointer is generally shown only when the Control key is pressed.| [`contextualMenu`](https://developer.apple.com/documentation/AppKit/NSCursor/contextualMenu)  
<!-- image: A plus symbol. -->| Crosshair| Precise rectangular selection is possible, such as when viewing an image in Preview.| [`crosshair`](https://developer.apple.com/documentation/AppKit/NSCursor/crosshair)  
<!-- image: A small pointer arrowhead with a circle underneath; the circle contains an Ex. -->| Disappearing item| A dragged item will disappear when dropped. If the item references an original item, the original is unaffected. For example, when dragging a mailbox out of the favorites bar in Mail, the original mailbox isn’t removed.| [`disappearingItem`](https://developer.apple.com/documentation/AppKit/NSCursor/disappearingItem)  
<!-- image: A small pointer arrowhead with a circle underneath; the circle contains a plus symbol. -->| Drag copy| Duplicates a dragged—not moved—item when dropped into the destination. Appears when pressing the Option key during a drag operation.| [`dragCopy`](https://developer.apple.com/documentation/AppKit/NSCursor/dragCopy)  
<!-- image: A curved arrow, pointing up and to the right. -->| Drag link| During a drag and drop operation, creates an alias of the selected file when dropped. The alias points to the original file, which remains unmoved. Appears when pressing the Option and Command keys during a drag operation.| [`dragLink`](https://developer.apple.com/documentation/AppKit/NSCursor/dragLink)  
<!-- image: Opposing veritcal braces, used to form an insertion marker. -->| Horizontal I beam| Selection and insertion of text is possible in a horizontal layout, such as a TextEdit or Pages document.| [`iBeam`](https://developer.apple.com/documentation/AppKit/NSCursor/iBeam)  
<!-- image: An open, gloved hand. -->| Open hand| Dragging to reposition content within a view is possible.| [`openHand`](https://developer.apple.com/documentation/AppKit/NSCursor/openHand)  
<!-- image: A small pointer arrowhead with a do not enter symbol underneath. -->| Operation not allowed| A dragged item can’t be dropped in the current location.| [`operationNotAllowed`](https://developer.apple.com/documentation/AppKit/NSCursor/operationNotAllowed)  
<!-- image: A gloved hand, with the index finger extended. -->| Pointing hand| The content beneath the pointer is a URL link to a webpage, document, or other item.| [`pointingHand`](https://developer.apple.com/documentation/AppKit/NSCursor/pointingHand)  
<!-- image: A horizontal bar with a downward-pointing arrow at its midpoint. -->| Resize down| Resize or move a window, view, or element downward.| [`resizeDown`](https://developer.apple.com/documentation/AppKit/NSCursor/resizeDown)  
<!-- image: A vertical bar with a left-pointing arrow at its midpoint. -->| Resize left| Resize or move a window, view, or element to the left.| [`resizeLeft`](https://developer.apple.com/documentation/AppKit/NSCursor/resizeLeft)  
<!-- image: A vertical bar with left- and right-pointing arrows extending from its midpoint. -->| Resize left/right| Resize or move a window, view, or element to the left or right.| [`resizeLeftRight`](https://developer.apple.com/documentation/AppKit/NSCursor/resizeLeftRight)  
<!-- image: A vertical bar with a right-pointing arrow at its midpoint. -->| Resize right| Resize or move a window, view, or element to the right.| [`resizeRight`](https://developer.apple.com/documentation/AppKit/NSCursor/resizeRight)  
<!-- image: A horizontal bar with an up-pointing arrow at its midpoint. -->| Resize up| Resize or move a window, view, or element upward.| [`resizeUp`](https://developer.apple.com/documentation/AppKit/NSCursor/resizeUp)  
<!-- image: A horizontal bar with up- and down-pointing arrows extending from its midpoint. -->| Resize up/down| Resize or move a window, view, or element upward or downward.| [`resizeUpDown`](https://developer.apple.com/documentation/AppKit/NSCursor/resizeUpDown)  
<!-- image: Opposing horizontal braces, used to form an insertion marker. -->| Vertical I beam| Selection and insertion of text is possible in a vertical layout.| [`iBeamCursorForVerticalLayout`](https://developer.apple.com/documentation/AppKit/NSCursor/iBeamCursorForVerticalLayout)  
  
### [visionOS](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#visionOS)

In visionOS, people can attach an external pointing device or keyboard, and use both devices while they continue to use their eyes and hands. If people look at an element and then move the pointer, the system brings focus to the element under the pointer. Your app doesn’t have to do anything to support this behavior.

When a pointing device is attached, the area people are looking at determines the pointer’s context. For example, when people shift their eyes from one window to another, the pointer’s context seamlessly transitions to the new window.

Video with custom controls. 

Content description: A recording that shows a pointer moving around, highlighting items, and scrolling content within a Safari window in visionOS. A picture-in-picture window is visible in the bottom left corner of the recording. It shows a person's hand operating a trackpad next to a keyboard outside the field of view. The person's gestures on the trackpad correspond to the pointer movements. 

Play 

When people use an attached pointing device that supports gestures, like a trackpad or mouse, the pointer hides while people are gesturing, minimizing visual distraction. In this scenario, the pointer remains hidden until people move it, when it reappears in the location they’re looking at.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Related)

[Entering data](https://developer.apple.com/design/human-interface-guidelines/entering-data)

[Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Developer-documentation)

[Input events](https://developer.apple.com/documentation/SwiftUI/Input-events) — SwiftUI

[Pointer interactions](https://developer.apple.com/documentation/UIKit/pointer-interactions) — UIKit

[Mouse, Keyboard, and Trackpad](https://developer.apple.com/documentation/AppKit/mouse-keyboard-and-trackpad) — AppKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Videos)

[<!-- image:  --> Design for the iPadOS pointer ](https://developer.apple.com/videos/play/wwdc2020/10640)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/pointing-devices#Change-log)

Date| Changes  
---|---  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Remotes

|---|---  
Touch surface (swipe)| Navigates. Changes focus.| Performs directional pad behavior.  
Touch surface (press)| Activates a control or an item. Navigates deeper.| Performs primary button behavior.  
Back| Returns to previous screen. Exits to Apple TV Home Screen.| Pauses/resumes gameplay. Returns to previous screen, exits to main game menu, or exits to Apple TV Home Screen.  
Play/Pause| Activates media playback. Pauses/resumes media playback.| Performs secondary button behavior. Skips intro video.  
  
## [Compatible remotes](https://developer.apple.com/design/human-interface-guidelines/remotes#Compatible-remotes)

Some remotes that are compatible with Apple TV include buttons for browsing live TV or other channel-based content. For example, a remote might include a button people can use to open an electronic program guide (EPG) and other buttons they can use to browse the guide or change channels. For developer guidance, see [Providing Channel Navigation](https://developer.apple.com/documentation/TVServices/providing-channel-navigation); for design guidance, see [EPG experience](https://developer.apple.com/design/human-interface-guidelines/live-viewing-apps#EPG-experience).

**If your live-viewing app provides an EPG, respond to a remote’s EPG-browsing buttons in ways people expect.** When people press a “guide” or “browse” button, they expect your EPG to open. While they’re viewing your EPG, people expect to navigate through it by pressing a “page up” or “page down” button. Avoid responding to these buttons in other ways while people are browsing the EPG. On the Siri Remote and compatible remotes, people can also tap on the upper or lower area of the Touch surface to browse the EPG. If your app doesn’t support an EPG experience, the system routes these button presses to the default guide app on the viewer’s device.

**While your content plays, respond to a compatible remote’s “page up” or “page down” button by changing the channel.** People expect these buttons to behave differently when they switch between viewing content and browsing an EPG.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/remotes#Platform-considerations)

 _Not supported in iOS, iPadOS, macOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/remotes#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/remotes#Related)

[Use your Siri Remote or Apple TV Remote with Apple TV](https://support.apple.com/en-us/HT205305)

---

## Reference: Spatial Interactions

|---  
June 21, 2023| Changed page title from Spatial interactions.
