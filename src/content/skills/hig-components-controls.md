---
title: "Hig Components Controls"
description: "Apple HIG guidance for selection and input controls including pickers, toggles, sliders, steppers, segmented controls, combo boxes, text fields, text views, labels, token fields, virtual..."
category: "development"
source: "community"
author: "Community"
tags: ["hig", "components", "controls"]
date: 2026-03-20
---

# Apple HIG: Selection and Input Controls

Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered.

## Key Principles

1. **Clear current state.** Users must always see what is selected. Toggles show on/off, segmented controls highlight the active segment, pickers display the current selection.

2. **Prefer standard system controls.** Built-in controls provide consistency and accessibility. Custom controls introduce a learning curve and may break assistive features.

3. **Toggles for binary states.** On or off. In Settings-style screens, changes take effect immediately. In modal forms, changes commit on confirmation.

4. **Segmented controls for mutually exclusive options.** 2-5 items, roughly equal importance, short labels.

5. **Sliders for continuous values.** When precise numeric input is not critical. Provide min/max labels or icons for range endpoints.

6. **Pickers for long option lists.** Too many options for a segmented control. Works well for dates, times, structured data.

7. **Steppers for small, precise adjustments.** Increment/decrement in fixed steps. Display current value next to the stepper with reasonable min/max bounds.

8. **Text fields for short, single-line input.** Text views for multi-line. Configure keyboard type to match expected input (email, URL, number).

9. **Combo boxes: text input + selection list.** macOS. Type a value or choose from a predefined list when custom values are valid.

10. **Token fields: discrete values as visual tokens.** macOS. For email recipients, tags, or collections of discrete items.

11. **Gauges and rating indicators display values.** Gauges show a value within a range. Rating indicators show ratings (often stars). Display-only; use interactive variants for input.

## Reference Index

| Reference | Topic | Key content |
|---|---|---|
| [controls.md](references/controls.md) | General controls | States, affordance, system controls |
| [toggles.md](references/toggles.md) | Toggles | On/off, immediate effect |
| [segmented-controls.md](references/segmented-controls.md) | Segmented controls | 2-5 options, equal weight |
| [sliders.md](references/sliders.md) | Sliders | Continuous range, min/max labels |
| [steppers.md](references/steppers.md) | Steppers | Fixed steps, bounded values |
| [pickers.md](references/pickers.md) | Pickers | Dates, times, long option sets |
| [combo-boxes.md](references/combo-boxes.md) | Combo boxes | macOS, type or select, custom values |
| [text-fields.md](references/text-fields.md) | Text fields | Short input, keyboard types, validation |
| [text-views.md](references/text-views.md) | Text views | Multi-line, comments, descriptions |
| [labels.md](references/labels.md) | Labels | Placement, VoiceOver support |
| [token-fields.md](references/token-fields.md) | Token fields | macOS, chips, tags, recipients |
| [virtual-keyboards.md](references/virtual-keyboards.md) | Virtual keyboards | Email, URL, number keyboard types |
| [rating-indicators.md](references/rating-indicators.md) | Rating indicators | Star ratings, display-only |
| [gauges.md](references/gauges.md) | Gauges | Level indicators, range display |

## Output Format

1. **Control recommendation with rationale** and why alternatives are less suitable.
2. **State management** -- how the control communicates current state and whether changes apply immediately or on confirmation.
3. **Validation approach** -- when to show errors and how to communicate rules.
4. **Accessibility** -- labels, traits, hints for VoiceOver.

## Questions to Ask

1. What type of data? (Boolean, choice from fixed set, numeric, free-form text?)
2. How many options?
3. Which platforms? (Combo boxes and token fields are macOS-only)
4. Settings screen or inline form?

## Related Skills

- **hig-components-menus** -- Buttons and pop-up buttons complementing selection controls
- **hig-components-dialogs** -- Sheets and popovers containing forms
- **hig-components-search** -- Search fields sharing text input patterns
- **hig-inputs** -- Keyboard, pointer, gesture interactions with controls
- **hig-foundations** -- Typography, color, layout for control styling

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Combo Boxes

---
title: "Combo boxes | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/combo-boxes

# Combo boxes

A combo box combines a text field with a pull-down button in a single control.

<!-- image: A stylized representation of a combo box control displaying a list of cities. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

People can enter a custom value into the field or click the button to choose from a list of predefined values. When people enter a custom value, it’s not added to the list of choices.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/combo-boxes#Best-practices)

**Populate the field with a meaningful default value from the list.** Although the field can be empty by default, it’s best when the default value refers to the hidden choices. The default value doesn’t have to be the first item in the list.

**Use an introductory label to let people know what types of items to expect.** Generally, use title-style capitalization for labels and end them with a colon. For related guidance, see [Labels](https://developer.apple.com/design/human-interface-guidelines/labels).

**Provide relevant choices.** People appreciate the ability to enter a custom value, as well as the convenience of choosing from a list of the most likely choices.

**Make sure list items aren’t wider than the text field.** If an item is too wide, the text field might truncate it, which is hard for people to read.

For guidance, see [Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields) and [Pull-down buttons](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/combo-boxes#Platform-considerations)

 _Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/combo-boxes#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/combo-boxes#Related)

[Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)

[Pull-down buttons](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/combo-boxes#Developer-documentation)

[`NSComboBox`](https://developer.apple.com/documentation/AppKit/NSComboBox) — AppKit

---

## Reference: Controls

|---  
June 10, 2024| New page.

---

## Reference: Gauges

|---  
September 23, 2022| New page.

---

## Reference: Labels

|---|---|---  
Label| Primary information| [`label`](https://developer.apple.com/documentation/UIKit/UIColor/label)| [`labelColor`](https://developer.apple.com/documentation/AppKit/NSColor/labelColor)  
Secondary label| A subheading or supplemental text| [`secondaryLabel`](https://developer.apple.com/documentation/UIKit/UIColor/secondaryLabel)| [`secondaryLabelColor`](https://developer.apple.com/documentation/AppKit/NSColor/secondaryLabelColor)  
Tertiary label| Text that describes an unavailable item or behavior| [`tertiaryLabel`](https://developer.apple.com/documentation/UIKit/UIColor/tertiaryLabel)| [`tertiaryLabelColor`](https://developer.apple.com/documentation/AppKit/NSColor/tertiaryLabelColor)  
Quaternary label| Watermark text| [`quaternaryLabel`](https://developer.apple.com/documentation/UIKit/UIColor/quaternaryLabel)| [`quaternaryLabelColor`](https://developer.apple.com/documentation/AppKit/NSColor/quaternaryLabelColor)  
  
**Make useful label text selectable.** If a label contains useful information — like an error message, a location, or an IP address — consider letting people select and copy it for pasting elsewhere.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/labels#Platform-considerations)

 _No additional considerations for iOS, iPadOS, tvOS, or visionOS._

### [macOS](https://developer.apple.com/design/human-interface-guidelines/labels#macOS)

Developer note

To display uneditable text in a label, use the [`isEditable`](https://developer.apple.com/documentation/AppKit/NSTextField/isEditable) property of [`NSTextField`](https://developer.apple.com/documentation/AppKit/NSTextField).

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/labels#watchOS)

Date and time text components (shown below on the left) display the current date, the current time, or a combination of both. You can configure a date text component to use a variety of formats, calendars, and time zones. A countdown timer text component (shown below on the right) displays a precise countdown or count-up timer. You can configure a timer text component to display its count value in a variety of formats.

<!-- image: An illustration of date and time text components on Apple Watch, with the date aligned to the leading edge and the time aligned to the trailing edge. -->Date and time labels

<!-- image: An illustration of a countdown timer text component on Apple Watch, with the time value at the center. -->Timer label

When you use the system-provided date and timer text components, watchOS automatically adjusts the label’s presentation to fit the available space. The system also updates the content without further input from your app.

Consider using date and timer components in complications. For design guidance, see [Complications](https://developer.apple.com/design/human-interface-guidelines/components/system-experiences/complications); for developer guidance, see [`Text`](https://developer.apple.com/documentation/SwiftUI/Text).

## [Resources](https://developer.apple.com/design/human-interface-guidelines/labels#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/labels#Related)

[Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)

[Text views](https://developer.apple.com/design/human-interface-guidelines/text-views)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/labels#Developer-documentation)

[`Label`](https://developer.apple.com/documentation/SwiftUI/Label) — SwiftUI

[`Text`](https://developer.apple.com/documentation/SwiftUI/Text) — SwiftUI

[`UILabel`](https://developer.apple.com/documentation/UIKit/UILabel) — UIKit

[`NSTextField`](https://developer.apple.com/documentation/AppKit/NSTextField) — AppKit

## [Change log](https://developer.apple.com/design/human-interface-guidelines/labels#Change-log)

Date| Changes  
---|---  
June 5, 2023| Updated guidance to reflect changes in watchOS 10.

---

## Reference: Pickers

|---  
June 5, 2023| Updated guidance for using pickers in watchOS.

---

## Reference: Rating Indicators

|---  
September 23, 2022| New page.

---

## Reference: Segmented Controls

|---  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Sliders

|---  
June 21, 2023| Updated to include guidance for visionOS.

---

## Reference: Steppers

---
title: "Steppers | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/steppers

# Steppers

A stepper is a two-segment control that people use to increase or decrease an incremental value.

<!-- image: A stylized representation of a stepper control. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

A stepper sits next to a field that displays its current value, because the stepper itself doesn’t display a value.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/steppers#Best-practices)

**Make the value that a stepper affects obvious.** A stepper itself doesn’t display any values, so make sure people know which value they’re changing when they use a stepper.

**Consider pairing a stepper with a text field when large value changes are likely.** Steppers work well by themselves for making small changes that require a few taps or clicks. By contrast, people appreciate the option to use a field to enter specific values, especially when the values they use can vary widely. On a printing screen, for example, it can help to have both a stepper and a text field to set the number of copies.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/steppers#Platform-considerations)

 _No additional considerations for iOS, iPadOS, or visionOS. Not supported in watchOS or tvOS._

### [macOS](https://developer.apple.com/design/human-interface-guidelines/steppers#macOS)

**For large value ranges, consider supporting Shift-click to change the value quickly.** If your app benefits from larger changes in a stepper’s value, it can be useful to let people Shift-click the stepper to change the value by more than the default increment (by 10 times the default, for example).

## [Resources](https://developer.apple.com/design/human-interface-guidelines/steppers#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/steppers#Related)

[Pickers](https://developer.apple.com/design/human-interface-guidelines/pickers)

[Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/steppers#Developer-documentation)

[`UIStepper`](https://developer.apple.com/documentation/UIKit/UIStepper) — UIKit

[`NSStepper`](https://developer.apple.com/documentation/AppKit/NSStepper) — AppKit

---

## Reference: Text Fields

|---  
June 5, 2023| Updated guidance to reflect changes in watchOS 10.

---

## Reference: Text Views

|---  
June 5, 2023| Updated guidance to reflect changes in watchOS 10.

---

## Reference: Toggles

|---  
March 29, 2024| Enhanced guidance for using switches in macOS apps, clarified when a checkbox has a title, and added artwork for radio buttons.  
September 12, 2023| Updated artwork.

---

## Reference: Token Fields

---
title: "Token fields | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/token-fields

# Token fields

A token field is a type of text field that can convert text into _tokens_ that are easy to select and manipulate.

<!-- image: A stylized representation of a text field containing a person's name formatted as a token. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

For example, Mail uses token fields for the address fields in the compose window. As people enter recipients, Mail converts the text that represents each recipient’s name into a token. People can select these recipient tokens and drag to reorder them or move them into a different field.

You can configure a token field to present people with a list of suggestions as they enter text into the field. For example, Mail suggests recipients as people type in an address field. When people select a suggested recipient, Mail inserts the recipient into the field as a token.

<!-- image: A partial screenshot of a Mail compose window in which tokens represent some recipients. -->

An individual token can also include a contextual menu that offers information about the token or editing options. For example, a recipient token in Mail includes a contextual menu with commands for editing the recipient name, marking the recipient as a VIP, and viewing the recipient’s contact card, among others.

<!-- image: A partial screenshot of a Mail compose window in which one recipient token reveals a menu of commands. -->

Tokens can also represent search terms in some situations; for guidance, see [Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields).

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/token-fields#Best-practices)

**Add value with a context menu.** People often benefit from a [context menu](https://developer.apple.com/design/human-interface-guidelines/context-menus) with additional options or information about a token.

**Consider providing additional ways to convert text into tokens.** By default, text people enter turns into a token whenever they type a comma. You can specify additional shortcuts, such as pressing Return, that also invoke this action.

**Consider customizing the delay the system uses before showing suggested tokens.** By default, suggestions appear immediately. However, suggestions that appear too quickly may distract people while they’re typing. If your app suggests tokens, consider adjusting the delay to a comfortable level.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/token-fields#Platform-considerations)

 _Not supported in iOS, iPadOS, tvOS, visionOS, and watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/token-fields#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/token-fields#Related)

[Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields)

[Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields)

[Context menus](https://developer.apple.com/design/human-interface-guidelines/context-menus)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/token-fields#Developer-documentation)

[`NSTokenField`](https://developer.apple.com/documentation/AppKit/NSTokenField) — AppKit

---

## Reference: Virtual Keyboards

|---  
June 9, 2025| Added guidance for displaying custom controls above the keyboard, and updated to reflect virtual keyboard availability in watchOS.  
February 2, 2024| Clarified the virtual keyboard’s support for direct and indirect gestures in visionOS.  
December 5, 2023| Added artwork for visionOS.  
June 21, 2023| Changed page title from Onscreen keyboards and updated to include guidance for visionOS.
