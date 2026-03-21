---
title: "Hig Components Dialogs"
description: "Apple HIG guidance for presentation components including alerts, action sheets, popovers, sheets, and digit entry views."
category: "writing"
source: "community"
author: "Community"
tags: ["hig", "components", "dialogs"]
date: 2026-03-20
---

# Apple HIG: Presentation Components

Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered.

## Key Principles

1. **Alerts: sparingly, for critical situations.** Errors needing attention, destructive action confirmations, or information requiring acknowledgment. They interrupt flow and demand a response.

2. **Sheets: focused tasks that maintain context.** Slides in from the edge (or attaches to a window on macOS). Use for creating items, editing settings, multi-step forms.

3. **Popovers: non-modal on iPad and Mac.** Appear next to the trigger element, dismissed by tapping outside. For additional information, options, or controls without taking over the screen.

4. **Action sheets: choosing among actions.** Present when picking from multiple actions, especially if one is destructive. iPhone: slide up from bottom. iPad: appear as popovers.

5. **Minimize interruptions.** Before reaching for a modal, consider inline presentation or making the action undoable instead.

6. **Concise, actionable alert text.** Short descriptive title. Brief message body if needed. Button labels should be specific verbs ("Delete", "Save"), not "OK".

7. **Mark destructive actions clearly.** Destructive button style (red text). Place destructive buttons where users are less likely to tap reflexively.

8. **Provide a cancel option** for alerts and action sheets with multiple actions. On action sheets, cancel appears at the bottom, separated.

9. **Digit entry: focused and accessible.** Appropriately sized input fields, automatic advancement between digits, support for paste and autofill.

10. **Adapt presentation to platform.** The same interaction may use different components on iPhone, iPad, Mac, and visionOS.

## Reference Index

| Reference | Topic | Key content |
|---|---|---|
| [alerts.md](references/alerts.md) | Alerts | Button ordering, title/message text, confirmation, destructive actions |
| [action-sheets.md](references/action-sheets.md) | Action sheets | Multiple actions, cancel option, destructive handling |
| [popovers.md](references/popovers.md) | Popovers | Non-modal, dismiss on tap outside, iPad/Mac |
| [sheets.md](references/sheets.md) | Sheets | Modal task, context preservation |
| [digit-entry-views.md](references/digit-entry-views.md) | Digit entry | PIN input, autofill, auto-advance |

## Output Format

1. **Recommended presentation type with rationale** and why alternatives are less suitable.
2. **Content guidelines** -- title, message, button labels per Apple's tone and brevity rules.
3. **Dismiss behavior** -- how the user dismisses and what happens (save, discard, cancel).
4. **Alternatives** -- when the scenario might not need a modal at all (inline feedback, undo, progressive disclosure).

## Questions to Ask

1. What information or action does the presentation need?
2. Blocking or non-blocking?
3. Which platforms?
4. How often does this appear?

## Related Skills

- **hig-components-menus** -- Buttons and toolbar items triggering presentations
- **hig-components-controls** -- Input controls within sheets and popovers
- **hig-components-search** -- Search and navigation within presented views
- **hig-patterns** -- Modality, interruptions, user flow management
- **hig-foundations** -- Color, typography, layout for presentation components

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Action Sheets

|---  
Default| The button has no special meaning.  
Destructive| The button destroys user data or performs a destructive action in the app.  
Cancel| The button dismisses the view without taking any action.  
  
**Avoid displaying more than four buttons in an action sheet, including the Cancel button.** When there are fewer buttons onscreen, it’s easier for people to view all their options at once. Because the Cancel button is required, aim to provide no more than three additional choices.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/action-sheets#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/action-sheets#Related)

[Modality](https://developer.apple.com/design/human-interface-guidelines/modality)

[Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)

[Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/action-sheets#Developer-documentation)

[`confirmationDialog(_:isPresented:titleVisibility:actions:)`](https://developer.apple.com/documentation/SwiftUI/View/confirmationDialog\(_:isPresented:titleVisibility:actions:\)-46zbb) — SwiftUI

[`UIAlertController.Style.actionSheet`](https://developer.apple.com/documentation/UIKit/UIAlertController/Style/actionSheet) — UIKit

---

## Reference: Alerts

|---  
Exit to the Home Screen| iOS, iPadOS  
Pressing Escape (Esc) or Command-Period (.) on an attached keyboard| iOS, iPadOS, macOS, visionOS  
Pressing Menu on the remote| tvOS  
  
## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/alerts#Platform-considerations)

 _No additional considerations for tvOS or watchOS._

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/alerts#iOS-iPadOS)

**Use an action sheet — not an alert — to offer choices related to an intentional action.** For example, when people cancel the Mail message they’re editing, an action sheet provides three choices: delete the edits (or the entire draft), save the draft, or return to editing. Although an alert can also help people confirm or cancel an action that has destructive consequences, it doesn’t provide additional choices related to the action. For guidance, see [Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets).

**When possible, avoid displaying an alert that scrolls.** Although an alert might scroll if the text size is large enough, be sure to minimize the potential for scrolling by keeping alert titles short and including a brief message only when necessary.

### [macOS](https://developer.apple.com/design/human-interface-guidelines/alerts#macOS)

macOS automatically displays your app icon in an alert, but you can supply an alternative icon or symbol. In addition, macOS lets you:

  * Configure repeating alerts to let people suppress subsequent occurrences of the same alert.

  * Append a custom view if it’s necessary to provide additional information (for developer guidance, see [`accessoryView`](https://developer.apple.com/documentation/AppKit/NSAlert/accessoryView)).

  * Include a Help button that opens your help documentation (see [Help buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Help-buttons)).




**Use a caution symbol sparingly.** Using a caution symbol like `exclamationmark.triangle` too frequently in your alerts diminishes its significance. Use the symbol only when extra attention is really needed, as when confirming an action that might result in unexpected loss of data. Don’t use the symbol for tasks whose only purpose is to overwrite or remove data, such as a save or empty trash.

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/alerts#visionOS)

When your app is running in the Shared Space, visionOS displays an alert in front of the app’s window, slightly forward along the z-axis.

Video with custom controls. 

Content description: A video of an alert in the Freeform app running in the Shared Space in visionOS. When the video plays, someone chooses to permanently delete a recently deleted Freeform board. An alert then appears in front of the Freeform window to ask for confirmation. 

Play 

If someone moves a window without dismissing its alert, the alert remains anchored to the window. If your app is running in a Full Space, the system displays the alert centered in the wearer’s [field of view](https://developer.apple.com/design/human-interface-guidelines/spatial-layout#Field-of-view).

Video with custom controls. 

Content description: A video of an alert in the Freeform app running in the Shared Space in visionOS. When the video plays, someone chooses to permanently delete a recently deleted Freeform board. An alert then appears in front of the Freeform window to ask for confirmation. The alert is not dismissed and remains anchored to the Freeform window as it’s moved around the Shared Space. 

Play 

If you need to display an accessory view in a visionOS alert, create a view that has a maximum height of 154 pt and a 16-pt corner radius.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/alerts#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/alerts#Related)

[Modality](https://developer.apple.com/design/human-interface-guidelines/modality)

[Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets)

[Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/alerts#Developer-documentation)

[`alert(_:isPresented:actions:)`](https://developer.apple.com/documentation/SwiftUI/View/alert\(_:isPresented:actions:\)-1bkka) — SwiftUI

[`UIAlertController`](https://developer.apple.com/documentation/UIKit/UIAlertController) — UIKit

[`NSAlert`](https://developer.apple.com/documentation/AppKit/NSAlert) — AppKit

## [Change log](https://developer.apple.com/design/human-interface-guidelines/alerts#Change-log)

Date| Changes  
---|---  
February 2, 2024| Enhanced guidance for using default and Cancel buttons.  
September 12, 2023| Added anatomy artwork for visionOS.  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Digit Entry Views

---
title: "Digit entry views | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/digit-entry-views

# Digit entry views

A digit entry view fills the entire screen and prompts people to enter a series of digits, like a PIN, using a digit-specific keyboard.

<!-- image: A stylized representation of an Apple TV five-digit passcode entry screen. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

You can add an optional title and prompt above the line of digits.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/digit-entry-views#Best-practices)

**Use secure digit fields.** Secure digit fields display asterisks instead of the entered digit onscreen. Always use a secure digit field when your app asks for sensitive data.

**Clearly state the purpose of the digit entry view.** Use a title and prompt that explains why someone needs to enter digits.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/digit-entry-views#Platform-considerations)

 _Not supported in iOS, iPadOS, macOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/digit-entry-views#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/digit-entry-views#Related)

[Virtual keyboards](https://developer.apple.com/design/human-interface-guidelines/virtual-keyboards)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/digit-entry-views#Developer-documentation)

[`TVDigitEntryViewController`](https://developer.apple.com/documentation/TVUIKit/TVDigitEntryViewController) — TVUIKit

---

## Reference: Popovers

---
title: "Popovers | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/popovers

# Popovers

A popover is a transient view that appears above other content when people click or tap a control or interactive area.

<!-- image: A stylized representation of a popover view. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/popovers#Best-practices)

**Use a popover to expose a small amount of information or functionality.** Because a popover disappears after people interact with it, limit the amount of functionality in the popover to a few related tasks. For example, a calendar event popover makes it easy for people to change the date or time of an event, or to move it to another calendar. The popover disappears after the change, letting people continue reviewing the events on their calendar.

**Consider using popovers when you want more room for content.** Views like sidebars and panels take up a lot of space. If you need content only temporarily, displaying it in a popover can help streamline your interface.

**Position popovers appropriately.** Make sure a popover’s arrow points as directly as possible to the element that revealed it. Ideally, a popover doesn’t cover the element that revealed it or any essential content people may need to see while using it.

**Use a Close button for confirmation and guidance only.** A Close button, including Cancel or Done, is worth including if it provides clarity, like exiting with or without saving changes. Otherwise, a popover generally closes when people click or tap outside its bounds or select an item in the popover. If multiple selections are possible, make sure the popover remains open until people explicitly dismiss it or they click or tap outside its bounds.

**Always save work when automatically closing a nonmodal popover.** People can unintentionally dismiss a nonmodal popover by clicking or tapping outside its bounds. Discard people’s work only when they click or tap an explicit Cancel button.

**Show one popover at a time.** Displaying multiple popovers clutters the interface and causes confusion. Never show a cascade or hierarchy of popovers, in which one emerges from another. If you need to show a new popover, close the open one first.

**Don’t show another view over a popover.** Make sure nothing displays on top of a popover, except for an alert.

**When possible, let people close one popover and open another with a single click or tap.** Avoiding extra gestures is especially desirable when several different bar buttons each open a popover.

**Avoid making a popover too big.** Make a popover only big enough to display its contents and point to the place it came from. If necessary, the system can adjust the size of a popover to ensure it fits well in the interface.

**Provide a smooth transition when changing the size of a popover.** Some popovers provide both condensed and expanded views of the same information. If you adjust the size of a popover, animate the change to avoid giving the impression that a new popover replaced the old one.

**Avoid using the word _popover_ in help documentation.** Instead, refer to a specific task or selection. For example, instead of “Select the Show button at the bottom of the popover,” you might write “Select the Show button.”

**Avoid using a popover to show a warning.** People can miss a popover or accidentally close it. If you need to warn people, use an [alert](https://developer.apple.com/design/human-interface-guidelines/alerts) instead.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/popovers#Platform-considerations)

 _No additional considerations for visionOS. Not supported in tvOS or watchOS._

### [iOS, iPadOS](https://developer.apple.com/design/human-interface-guidelines/popovers#iOS-iPadOS)

**Avoid displaying popovers in compact views.** Make your app or game dynamically adjust its layout based on the size class of the content area. Reserve popovers for wide views; for compact views, use all available screen space by presenting information in a full-screen modal view like a sheet instead. For related guidance, see [Modality](https://developer.apple.com/design/human-interface-guidelines/modality).

### [macOS](https://developer.apple.com/design/human-interface-guidelines/popovers#macOS)

You can make a popover detachable in macOS, which becomes a separate panel when people drag it. The panel remains visible onscreen while people interact with other content.

  * Attached popover 
  * Detached popover 



<!-- image: An illustration of an event in Calendar with the attached version of the event's popover next to and pointing to it. -->

<!-- image: An illustration of an event in Calendar with the detached version of the event's popover next to it. -->

**Consider letting people detach a popover.** People might appreciate being able to convert a popover into a panel if they want to view other information while the popover remains visible.

**Make minimal appearance changes to a detached popover.** A panel that looks similar to the original popover helps people maintain context.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/popovers#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/popovers#Related)

[Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets)

[Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets)

[Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts)

[Modality](https://developer.apple.com/design/human-interface-guidelines/modality)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/popovers#Developer-documentation)

[`popover(isPresented:attachmentAnchor:arrowEdge:content:)`](https://developer.apple.com/documentation/SwiftUI/View/popover\(isPresented:attachmentAnchor:arrowEdge:content:\)) — SwiftUI

[`UIPopoverPresentationController`](https://developer.apple.com/documentation/UIKit/UIPopoverPresentationController) — UIKit

[`NSPopover`](https://developer.apple.com/documentation/AppKit/NSPopover) — AppKit

---

## Reference: Sheets

|---  
March 29, 2024| Added guidance to use form or page sheet styles in iPadOS apps.  
December 5, 2023| Recommended using a split view to offer supplementary items in a visionOS app.  
June 21, 2023| Updated to include guidance for visionOS.  
June 5, 2023| Updated guidance for using sheets in watchOS.
