---
title: "Hig Components Menus"
description: "Apple HIG guidance for menu and button components including menus, context menus, dock menus, edit menus, the menu bar, toolbars, action buttons, pop-up buttons, pull-down buttons, disclosure..."
category: "development"
source: "community"
author: "Community"
tags: ["hig", "components", "menus"]
date: 2026-03-20
---

# Apple HIG: Menus and Buttons

Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered.

## Key Principles

1. **Menus should be contextual and predictable.** Standard items in standard locations. Follow platform conventions for ordering and grouping.

2. **Use standard button styles.** System-defined styles communicate affordance and maintain visual consistency. Prefer them over custom designs.

3. **Toolbars for frequent actions.** Most commonly used commands in the toolbar. Rarely used actions belong in menus.

4. **Menu bar is the primary command interface on macOS.** Every command reachable from the menu bar. Toolbars and context menus supplement, not replace.

5. **Context menus for secondary actions.** Right-click or long-press, relevant to the item under the pointer. Never put a command only in a context menu.

6. **Pop-up buttons for mutually exclusive choices.** Select exactly one option from a set.

7. **Pull-down buttons for action lists.** No current selection; they offer a set of commands.

8. **Action buttons consolidate related actions** behind a single icon in toolbars or title bars.

9. **Disclosure controls for progressive disclosure.** Show or hide additional content.

10. **Dock menus: short and focused** on the most useful actions when the app is running.

## Reference Index

| Reference | Topic | Key content |
|---|---|---|
| [menus.md](references/menus.md) | General menu design | Item ordering, grouping, shortcuts |
| [context-menus.md](references/context-menus.md) | Context menus | Right-click, long press, secondary actions |
| [dock-menus.md](references/dock-menus.md) | Dock menus | macOS app-level actions, running state |
| [edit-menus.md](references/edit-menus.md) | Edit menus | Undo, copy, paste, standard items |
| [the-menu-bar.md](references/the-menu-bar.md) | Menu bar | macOS primary command interface, structure |
| [toolbars.md](references/toolbars.md) | Toolbars | Frequent actions, customization, placement |
| [buttons.md](references/buttons.md) | Buttons | System styles, sizing, affordance |
| [action-button.md](references/action-button.md) | Action button | Grouped secondary actions, toolbar use |
| [pop-up-buttons.md](references/pop-up-buttons.md) | Pop-up buttons | Mutually exclusive choice selection |
| [pull-down-buttons.md](references/pull-down-buttons.md) | Pull-down buttons | Action lists, no current selection |
| [disclosure-controls.md](references/disclosure-controls.md) | Disclosure controls | Progressive disclosure, show/hide |

## Output Format

1. **Component recommendation** -- which menu or button type and why.
2. **Visual hierarchy** -- placement, sizing, grouping within the interface.
3. **Platform-specific behavior** across iOS, iPadOS, macOS, visionOS.
4. **Keyboard shortcuts** (macOS) -- standard and custom shortcuts for menu items and toolbar actions.

## Questions to Ask

1. Which platforms?
2. Primary or secondary action?
3. How many actions need to be available?
4. macOS menu bar app?

## Related Skills

- **hig-components-search** -- Search fields, page controls alongside toolbars and menus
- **hig-components-controls** -- Toggles, pickers, segmented controls complementing buttons
- **hig-components-dialogs** -- Alerts, sheets, popovers triggered by menu items or buttons
- **hig-inputs** -- Keyboard shortcuts and pointer interactions with menus and toolbars

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Action Button

|---  
September 12, 2023| Updated to include guidance for iOS.  
September 14, 2022| New page.

---

## Reference: Buttons

|---  
Dialog with dismissal buttons (like OK and Cancel)| Lower corner, opposite to the dismissal buttons and vertically aligned with them  
Dialog without dismissal buttons| Lower-left or lower-right corner  
Settings window or pane| Lower-left or lower-right corner  
  
**Use a help button within a view, not in the window frame.** For example, avoid placing a help button in a toolbar or status bar.

**Avoid displaying text that introduces a help button.** People know what a help button does, so they don’t need additional descriptive text.

#### [Image buttons](https://developer.apple.com/design/human-interface-guidelines/buttons#Image-buttons)

An _image button_ appears in a view and displays an image, symbol, or icon. You can configure an image button to behave like a push button, toggle, or pop-up button.

**Use an image button in a view, not in the window frame.** For example, avoid placing an image button in a toolbar or status bar. If you need to use an image as a button in a toolbar, use a toolbar item. See [Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars).

**Include about 10 pixels of padding between the edges of the image and the button edges.** An image button’s edges define its clickable area even when they aren’t visible. Including padding ensures that a click registers correctly even if it’s not precisely within the image. In general, avoid including a system-provided border in an image button; for developer guidance, see [`isBordered`](https://developer.apple.com/documentation/AppKit/NSButton/isBordered).

**If you need to include a label, position it below the image button.** For related guidance, see [Labels](https://developer.apple.com/design/human-interface-guidelines/labels).

### [visionOS](https://developer.apple.com/design/human-interface-guidelines/buttons#visionOS)

A visionOS button typically includes a visible background that can help people see it, and the button plays sound to provide feedback when people interact with it.

Video with custom controls. 

Content description: A recording showing the top portion of a window in visionOS. The window contains several buttons, including a 'More' button, which receives the hover effect. The button is selected and a menu containing additional options appears. 

Play 

There are three standard button shapes in visionOS. Typically, an icon-only button uses a [`circle`](https://developer.apple.com/documentation/SwiftUI/ButtonBorderShape/circle) shape, a text-only button uses a [`roundedRectangle`](https://developer.apple.com/documentation/SwiftUI/ButtonBorderShape/roundedRectangle) or [`capsule`](https://developer.apple.com/documentation/SwiftUI/ButtonBorderShape/capsule) shape, and a button that includes both an icon and text uses the capsule shape.

visionOS buttons use different visual styles to communicate four different interaction states.

<!-- image: An image of a circular button that contains an icon of an outlined square with rounded corners. The button background is dark and the dashed outline is white. -->Idle

<!-- image: An image of a circular button that contains an icon of an outlined square with rounded corners. The button background is medium dark and the outline is white. -->Hover

<!-- image: An image of a circular button that contains an icon of an outlined square with rounded corners. The button background is white and the outline is black. -->Selected

<!-- image: An image of a circular button that contains an icon of an outlined square with rounded corners. The button background is very dark and the outline is light. -->Unavailable

Note

In visionOS, buttons don’t support custom hover effects.

In addition to the four states shown above, a button can also reveal a tooltip when people look at it for a brief time. In general, buttons that contain text don’t need to display a tooltip because the button’s descriptive label communicates what it does.

Video with custom controls. 

Content description: An animation showing a tooltip appearing beneath a visionOS button. 

Play 

In visionOS, buttons can have the following sizes.

Shape| Mini (28 pt)| Small (32 pt)| Regular (44 pt)| Large (52 pt)| Extra large (64 pt)  
---|---|---|---|---|---  
Circular| <!-- image: A checkmark denoting availability. -->| <!-- image: A checkmark denoting availability. -->| <!-- image: A checkmark denoting availability. -->| <!-- image: A checkmark denoting availability. -->| <!-- image: A checkmark denoting availability. -->  
Capsule (text only)| | <!-- image: A checkmark denoting availability. -->| <!-- image: A checkmark denoting availability. -->| <!-- image: A checkmark denoting availability. -->|   
Capsule (text and icon)| | | <!-- image: A checkmark denoting availability. -->| <!-- image: A checkmark denoting availability. -->|   
Rounded rectangle| | <!-- image: A checkmark denoting availability. -->| <!-- image: A checkmark denoting availability. -->| <!-- image: A checkmark denoting availability. -->|   
  
**Prefer buttons that have a discernible background shape and fill.** It tends to be easier for people to see a button when it’s enclosed in a shape that uses a contrasting background fill. The exception is a button in a toolbar, context menu, alert, or [ornament](https://developer.apple.com/design/human-interface-guidelines/ornaments) where the shape and material of the larger component make the button comfortably visible. The following guidelines can help you ensure that a button looks good in different contexts:

  * When a button appears on top of a glass [window](https://developer.apple.com/design/human-interface-guidelines/windows#visionOS), use the [`thin`](https://developer.apple.com/documentation/SwiftUI/Material/thin) material as the button’s background.

  * When a button appears floating in space, use the [glass material](https://developer.apple.com/design/human-interface-guidelines/materials#visionOS) for its background.




**Avoid creating a custom button that uses a white background fill and black text or icons.** The system reserves this visual style to convey the toggled state.

**In general, prefer circular or capsule-shape buttons.** People’s eyes tend to be drawn toward the corners in a shape, making it difficult to keep looking at the shape’s center. The more rounded a button’s shape, the easier it is for people to look steadily at it. When you need to display a button by itself, prefer a capsule-shape button.

**Provide enough space around a button to make it easy for people to look at it.** Aim to place buttons so their centers are always at least 60 pts apart. If your buttons measure 60 pts or larger, add 4 pts of padding around them to keep the hover effect from overlapping. Also, it’s usually best to avoid displaying small or mini buttons in a vertical stack or horizontal row.

**Choose the right shape if you need to display text-labeled buttons in a stack or row.** Specifically, prefer the rounded-rectangle shape in a vertical stack of buttons and prefer the capsule shape in a horizontal row of buttons.

**Use standard controls to take advantage of the audible feedback sounds people already know.** Audible feedback is especially important in visionOS, because the system doesn’t play haptics.

### [watchOS](https://developer.apple.com/design/human-interface-guidelines/buttons#watchOS)

watchOS displays all inline buttons using the [`capsule`](https://developer.apple.com/documentation/SwiftUI/ButtonBorderShape/capsule) button shape. When you place a button inline with content, it gains a material effect that contrasts with the background to ensure legibility.

<!-- image: An illustration that represents a screen on Apple Watch, which includes capsule-shaped Primary and Secondary buttons. -->

**Use a toolbar to place buttons in the corners.** The system automatically moves the time and title to accommodate toolbar buttons. The system also applies the [Liquid Glass](https://developer.apple.com/design/human-interface-guidelines/materials#Liquid-Glass) appearance to toolbar buttons, providing a clear visual distinction from the content beneath them.

<!-- image: An illustration showing toolbar buttons in the top leading and trailing corners, as well as three toolbar buttons across the bottom of the screen. -->

**Prefer buttons that span the width of the screen for primary actions in your app.** Full-width buttons look better and are easier for people to tap. If two buttons must share the same horizontal space, use the same height for both, and use images or short text titles for each button’s content.

**Use toolbar buttons to provide either navigation to related areas or contextual actions for the view’s content.** These buttons provide access to additional information or secondary actions for the view’s content.

**Use the same height for vertical stacks of one- and two-line text buttons.** As much as possible, use identical button heights for visual consistency.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/buttons#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/buttons#Related)

[Pop-up buttons](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons)

[Pull-down buttons](https://developer.apple.com/design/human-interface-guidelines/pull-down-buttons)

[Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles)

[Segmented controls](https://developer.apple.com/design/human-interface-guidelines/segmented-controls)

[Location button](https://developer.apple.com/design/human-interface-guidelines/privacy#Location-button)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/buttons#Developer-documentation)

[`Button`](https://developer.apple.com/documentation/SwiftUI/Button) — SwiftUI

[`UIButton`](https://developer.apple.com/documentation/UIKit/UIButton) — UIKit

[`NSButton`](https://developer.apple.com/documentation/AppKit/NSButton) — AppKit

## [Change log](https://developer.apple.com/design/human-interface-guidelines/buttons#Change-log)

Date| Changes  
---|---  
December 16, 2025| Updated guidance for Liquid Glass.  
June 9, 2025| Updated guidance for button styles and content.  
February 2, 2024| Noted that visionOS buttons don’t support custom hover effects.  
December 5, 2023| Clarified some terminology and guidance for buttons in visionOS.  
June 21, 2023| Updated to include guidance for visionOS.  
June 5, 2023| Updated guidance for using buttons in watchOS.

---

## Reference: Context Menus

|---  
December 5, 2023| Added guidance on hiding unavailable menu items.  
June 21, 2023| Updated to include guidance for visionOS.  
September 14, 2022| Refined guidance on including a submenu and added a guideline on using a context menu to support object creation in an iPadOS app.

---

## Reference: Disclosure Controls

---
title: "Disclosure controls | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/disclosure-controls

# Disclosure controls

Disclosure controls reveal and hide information and functionality related to specific controls or views.

<!-- image: A stylized representation of collapsed and expanded disclosure buttons. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Best-practices)

**Use a disclosure control to hide details until they’re relevant.** Place controls that people are most likely to use at the top of the disclosure hierarchy so they’re always visible, with more advanced functionality hidden by default. This organization helps people quickly find the most essential information without overwhelming them with too many detailed options.

## [Disclosure triangles](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Disclosure-triangles)

A disclosure triangle shows and hides information and functionality associated with a view or a list of items. For example, Keynote uses a disclosure triangle to show advanced options when exporting a presentation, and the Finder uses disclosure triangles to progressively reveal hierarchy when navigating a folder structure in list view.

  * Collapsed 
  * Expanded 



<!-- image: An illustration of three folders in a Finder list view. The folders are collapsed, with disclosure triangles on their leading edges pointing inward to indicate that they can be expanded to reveal their contents. -->

<!-- image: An illustration of three folders in a Finder list view. The first and third folders are collapsed, with disclosure triangles on their leading edges pointing inward to indicate that they can be expanded to reveal their contents. The second folder is expanded, with its disclosure triangle pointing down, revealing three subfolders inside. -->

A disclosure triangle points inward from the leading edge when its content is hidden and down when its content is visible. Clicking or tapping the disclosure triangle switches between these two states, and the view expands or collapses accordingly to accommodate the content.

**Provide a descriptive label when using a disclosure triangle.** Make sure your labels indicate what is disclosed or hidden, like “Advanced Options.”

For developer guidance, see [`NSButton.BezelStyle.disclosure`](https://developer.apple.com/documentation/AppKit/NSButton/BezelStyle-swift.enum/disclosure).

## [Disclosure buttons](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Disclosure-buttons)

A disclosure button shows and hides functionality associated with a specific control. For example, the macOS Save sheet shows a disclosure button next to the Save As text field. When people click or tap this button, the Save dialog expands to give advanced navigation options for selecting an output location for their document.

A disclosure button points down when its content is hidden and up when its content is visible. Clicking or tapping the disclosure button switches between these two states, and the view expands or collapses accordingly to accommodate the content.

  * Collapsed 
  * Expanded 



<!-- image: A screenshot of a collapsed save dialog in macOS. The dialog includes a closed disclosure button that expands the dialog to reveal additional options. -->

<!-- image: A screenshot of an expanded save dialog in macOS. The dialog includes an open disclosure button that collapses the dialog to hide some options. -->

**Place a disclosure button near the content that it shows and hides.** Establish a clear relationship between the control and the expanded choices that appear when a person clicks or taps a button.

**Use no more than one disclosure button in a single view.** Multiple disclosure buttons add complexity and can be confusing.

For developer guidance, see [`NSButton.BezelStyle.pushDisclosure`](https://developer.apple.com/documentation/AppKit/NSButton/BezelStyle-swift.enum/pushDisclosure).

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Platform-considerations)

 _No additional considerations for macOS. Not supported in tvOS or watchOS._

### [iOS, iPadOS, visionOS](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#iOS-iPadOS-visionOS)

Disclosure controls are available in iOS, iPadOS, and visionOS with the SwiftUI [`DisclosureGroup`](https://developer.apple.com/documentation/SwiftUI/DisclosureGroup) view.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Related)

[Outline views](https://developer.apple.com/design/human-interface-guidelines/outline-views)

[Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables)

[Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Developer-documentation)

[`DisclosureGroup`](https://developer.apple.com/documentation/SwiftUI/DisclosureGroup) — SwiftUI

[`NSButton.BezelStyle.disclosure`](https://developer.apple.com/documentation/AppKit/NSButton/BezelStyle-swift.enum/disclosure) — AppKit

[`NSButton.BezelStyle.pushDisclosure`](https://developer.apple.com/documentation/AppKit/NSButton/BezelStyle-swift.enum/pushDisclosure) — AppKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/disclosure-controls#Videos)

[<!-- image:  --> Stacks, Grids, and Outlines in SwiftUI ](https://developer.apple.com/videos/play/wwdc2020/10031)

---

## Reference: Dock Menus

---
title: "Dock menus | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/dock-menus

# Dock menus

On a Mac, people can secondary click an app’s or game’s icon in the Dock to reveal a Dock menu, which presents both system-provided and custom items.

<!-- image: A stylized representation of a menu extending from an icon in the Dock. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

The system-provided Dock menu items can vary depending on whether the app is open. For example, the Dock menu for Safari includes menu items for actions like viewing a current window or creating a new window.

Note

Although iOS and iPadOS don’t support a Dock menu, people can reveal a similar menu of system-provided and custom items — called Home Screen quick actions — when they long press an app icon on the Home Screen or in the Dock. For guidance, see [Home Screen quick actions](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions).

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/dock-menus#Best-practices)

As with all menus, you need to label Dock menu items succinctly and organize them logically. For guidance, see [Menus](https://developer.apple.com/design/human-interface-guidelines/menus).

**Make custom Dock menu items available in other places, too.** Not everyone uses a Dock menu, so it’s important to offer the same commands elsewhere, like in your menu bar menus or within your interface.

**Prefer high-value custom items for your Dock menu.** For example, a Dock menu can list all currently or recently open windows, making it a convenient way to jump to the window people want. Also consider listing a few of the actions that are most likely to be useful when your app isn’t frontmost or when there are no open windows. For example, Mail includes items for getting new mail and composing a new message in addition to listing all open windows.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/dock-menus#Platform-considerations)

 _Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/dock-menus#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/dock-menus#Related)

[Menus](https://developer.apple.com/design/human-interface-guidelines/menus)

[Home Screen quick actions](https://developer.apple.com/design/human-interface-guidelines/home-screen-quick-actions)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/dock-menus#Developer-documentation)

[`applicationDockMenu(_:)`](https://developer.apple.com/documentation/AppKit/NSApplicationDelegate/applicationDockMenu\(_:\)) — AppKit

---

## Reference: Edit Menus

|---  
June 21, 2023| Updated to include guidance for visionOS.  
September 14, 2022| Added guidance on supporting both edit-menu styles in iPadOS.

---

## Reference: Menus

|---  
December 16, 2025| Added guidance for presenting menus with breakthrough effects in visionOS.  
July 28, 2025| Added guidance for representing menu items with icons.  
June 10, 2024| Added guidance for in-game menus and included game-specific examples.  
June 21, 2023| Updated to include guidance for visionOS.  
September 14, 2022| Added guidelines for using the small, medium, and large menu layouts in iPadOS.

---

## Reference: Pop Up Buttons

|---  
October 24, 2023| Added artwork.  
September 14, 2022| Added a guideline on using a pop-up button in a popover or modal view in iPadOS.

---

## Reference: Pull Down Buttons

|---  
September 14, 2022| Refined guidance on designing a useful menu length.

---

## Reference: The Menu Bar

|---|---  
About _YourAppName_|  Displays the About window for your app, which includes copyright and version information.| Prefer a short name of 16 characters or fewer. Don’t include a version number.  
Settings…| Opens your [settings](https://developer.apple.com/design/human-interface-guidelines/settings) window, or your app’s page in iPadOS Settings.| Use only for app-level settings. If you also offer document-specific settings, put them in the File menu.  
Optional app-specific items| Performs custom app-level setting or configuration actions.| List custom app-configuration items after the Settings item and within the same group.  
Services (macOS only)| Displays a submenu of services from the system and other apps that apply to the current context.|   
Hide _YourAppName_ (macOS only)| Hides your app and all of its windows, and then activates the most recently used app.| Use the same short app name you supply for the About item.  
Hide Others (macOS only)| Hides all other open apps and their windows.|   
Show All (macOS only)| Shows all other open apps and their windows behind your app’s windows.|   
Quit _YourAppName_|  Quits your app. Pressing Option changes Quit _YourAppName_ to Quit and Keep Windows.| Use the same short app name you supply for the About item.  
  
**Display the About menu item first.** Include a separator after the About menu item so that it appears by itself in a group.

## [File menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#File-menu)

The File menu contains commands that help people manage the files or documents an app supports. If your app doesn’t handle any types of files, you can rename or eliminate this menu.

The File menu typically contains the following menu items listed in the following order.

Menu item| Action| Guidance  
---|---|---  
New _Item_|  Creates a new document, file, or window.| For _Item_ , use a term that names the type of item your app creates. For example, Calendar uses _Event_ and _Calendar_.  
Open| Can open the selected item or present an interface in which people select an item to open.| If people need to select an item in a separate interface, an ellipsis follows the command to indicate that more input is required.  
Open Recent| Displays a submenu that lists recently opened documents and files that people can select, and typically includes a _Clear Menu_ item.| List document and filenames that people recognize in the submenu; don’t display file paths. List the documents in the order people last opened them, with the most recently opened document first.  
Close| Closes the current window or document. Pressing Option changes Close to Close All. For a tab-based window, Close Tab replaces Close.| In a tab-based window, consider adding a Close Window item to let people close the entire window with one click or tap.  
Close Tab| Closes the current tab in a tab-based window. Pressing Option changes Close Tab to Close Other Tabs.|   
Close File| Closes the current file and all its associated windows.| Consider supporting this menu item if your app can open multiple views of the same file.  
Save| Saves the current document or file.| Automatically save changes periodically as people work so they don’t need to keep choosing File > Save. For a new document, prompt people for a name and location. If you need to let people save a file in multiple formats, prefer a pop-up menu that lets people choose a format in the Save sheet.  
Save All| Saves all open documents.|   
Duplicate| Duplicates the current document, leaving both documents open. Pressing Option changes Duplicate to Save As.| Prefer Duplicate to menu items like Save As, Export, Copy To, and Save To because these items don’t clarify the relationship between the original file and the new one.  
Rename…| Lets people change the name of the current document.|   
Move To…| Prompts people to choose a new location for the document.|   
Export As…| Prompts people for a name, output location, and export file format. After exporting the file, the current document remains open; the exported file doesn’t open.| Reserve the Export As item for when you need to let people export content in a format your app doesn’t typically handle.  
Revert To| When people turn on autosaving, displays a submenu that lists recent document versions and an option to display the version browser. After people choose a version to restore, it replaces the current document.|   
Page Setup…| Opens a panel for specifying printing parameters like paper size and printing orientation. A document can save the printing parameters that people specify.| Include the Page Setup item if you need to support printing parameters that apply to a specific document. Parameters that are global in nature, like a printer’s name, or that people change frequently, like the number of copies to print, belong in the Print panel.  
Print…| Opens the standard Print panel, which lets people print to a printer, send a fax, or save as a PDF.|   
  
## [Edit menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Edit-menu)

The Edit menu lets people make changes to content in the current document or text container, and provides commands for interacting with the Clipboard. Because many editing commands apply to any editable content, the Edit menu is useful even in apps that aren’t document-based.

**Determine whether Find menu items belong in the Edit menu.** For example, if your app lets people search for files or other types of objects, Find menu items might be more appropriate in the File menu.

The Edit menu typically contains the following top-level menu items, listed in the following order.

Menu item| Action| Guidance  
---|---|---  
Undo| Reverses the effect of the previous user operation.| Clarify the target of the undo. For example, if people just selected a menu item, you can append the item’s title, such as Undo Paste and Match Style. For a text entry operation, you might append the word _Typing_ to give Undo Typing.  
Redo| Reverses the effect of the previous Undo operation.| Clarify the target of the redo. For example, if people just reversed a menu item selection, you can append the item’s title, such as Redo Paste and Match Style. For a text entry operation, you might append the word _Typing_ to give Redo Typing.  
Cut| Removes the selected data and stores it on the Clipboard, replacing the previous contents of the Clipboard.|   
Copy| Duplicates the selected data and stores it on the Clipboard.|   
Paste| Inserts the contents of the Clipboard at the current insertion point. The Clipboard contents remain unchanged, permitting people to choose Paste multiple times.|   
Paste and Match Style| Inserts the contents of the Clipboard at the current insertion point, matching the style of the inserted text to the surrounding text.|   
Delete| Removes the selected data, but doesn’t place it on the Clipboard.| Provide a Delete menu item instead of an Erase or Clear menu item. Choosing Delete is the equivalent of pressing the Delete key, so it’s important for the naming to be consistent.  
Select All| Highlights all selectable content in the current document or text container.|   
Find| Displays a submenu containing menu items for performing search operations in the current document or text container. Standard submenus include: Find, Find and Replace, Find Next, Find Previous, Use Selection for Find, and Jump to Selection.|   
Spelling and Grammar| Displays a submenu containing menu items for checking for and correcting spelling and grammar in the current document or text container. Standard submenus include: Show Spelling and Grammar, Check Document Now, Check Spelling While Typing, Check Grammar With Spelling, and Correct Spelling Automatically.|   
Substitutions| Displays a submenu containing items that let people toggle automatic substitutions while they type in a document or text container. Standard submenus include: Show Substitutions, Smart Copy/Paste, Smart Quotes, Smart Dashes, Smart Links, Data Detectors, and Text Replacement.|   
Transformations| Displays a submenu containing items that transform selected text. Standard submenus include: Make Uppercase, Make Lowercase, and Capitalize.|   
Speech| Displays a submenu containing Start Speaking and Stop Speaking items, which control when the system audibly reads selected text.|   
Start Dictation| Opens the dictation window and converts spoken words into text that’s added at the current insertion point. The system automatically adds the Start Dictation menu item at the bottom of the Edit menu.|   
Emoji & Symbols| Displays a Character Viewer, which includes emoji, symbols, and other characters people can insert at the current insertion point. The system automatically adds the Emoji & Symbols menu item at the bottom of the Edit menu.|   
  
## [Format menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Format-menu)

The Format menu lets people adjust text formatting attributes in the current document or text container. You can exclude this menu if your app doesn’t support formatted text editing.

The Format menu typically contains the following top-level menu items, listed in the following order.

Menu item| Action  
---|---  
Font| Displays a submenu containing items for adjusting font attributes of the selected text. Standard submenus include: Show Fonts, Bold, Italic, Underline, Bigger, Smaller, Show Colors, Copy Style, and Paste Style.  
Text| Displays a submenu containing items for adjusting text attributes of the selected text. Standard submenus include: Align Left, Align Center, Justify, Align Right, Writing Direction, Show Ruler, Copy Ruler, and Paste Ruler.  
  
## [View menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#View-menu)

The View menu lets people customize the appearance of all an app’s windows, regardless of type.

Important

The View menu doesn’t include items for navigating between or managing specific windows; the [Window menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Window-menu) provides these commands.

**Provide a View menu even if your app supports only a subset of the standard view functions.** For example, if your app doesn’t include a tab bar, toolbar, or sidebar, but does support full-screen mode, provide a View menu that includes only the Enter/Exit Full Screen menu item.

**Ensure that each show/hide item title reflects the current state of the corresponding view.** For example, when the toolbar is hidden, provide a Show Toolbar menu item; when the toolbar is visible, provide a Hide Toolbar menu item.

The View menu typically contains the following top-level menu items, listed in the following order.

Menu item| Action  
---|---  
Show/Hide Tab Bar| Toggles the visibility of the [tab bar](https://developer.apple.com/design/human-interface-guidelines/tab-bars) above the body area in a tab-based window  
Show All Tabs/Exit Tab Overview| Enters and exits a view (similar to Mission Control) that provides an overview of all open tabs in a tab-based window  
Show/Hide Toolbar| In a window that includes a [toolbar](https://developer.apple.com/design/human-interface-guidelines/toolbars), toggles the toolbar’s visibility  
Customize Toolbar| In a window that includes a toolbar, opens a view that lets people customize toolbar items  
Show/Hide Sidebar| In a window that includes a [sidebar](https://developer.apple.com/design/human-interface-guidelines/sidebars), toggles the sidebar’s visibility  
Enter/Exit Full Screen| In an app that supports a [full-screen experience](https://developer.apple.com/design/human-interface-guidelines/going-full-screen), opens the window at full-screen size in a new space  
  
## [App-specific menus](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#App-specific-menus)

Your app’s custom menus appear in the menu bar between the View menu and the Window menu. For example, Safari’s menu bar includes app-specific History and Bookmarks menus.

**Provide app-specific menus for custom commands.** People look in the menu bar when searching for app-specific commands, especially when using an app for the first time. Even when commands are available elsewhere in your app, it’s important to list them in the menu bar. Putting commands in the menu bar makes them easier for people to find, lets you assign keyboard shortcuts to them, and makes them more accessible to people using Full Keyboard Access. Excluding commands from the menu bar — even infrequently used or advanced commands — risks making them difficult for everyone to find.

**As much as possible, reflect your app’s hierarchy in app-specific menus.** For example, Mail lists the Mailbox, Message, and Format menus in an order that mirrors the relationships of these items: mailboxes contain messages, and messages contain formatting.

**Aim to list app-specific menus in order from most to least general or commonly used.** People tend to expect menus in the leading end of a list to be more specialized than menus in the trailing end.

## [Window menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Window-menu)

The Window menu lets people navigate, organize, and manage an app’s windows.

Important

The Window menu doesn’t help people customize the appearance of windows or close them. To customize a window, people use commands in the [View menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#View-menu); to close a window, people choose Close in the [File menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#File-menu).

**Provide a Window menu even if your app has only one window.** Include the Minimize and Zoom menu items so people using Full Keyboard Access can use the keyboard to invoke these functions.

**Consider including menu items for showing and hiding panels.** A [panel](https://developer.apple.com/design/human-interface-guidelines/panels) provides information, configuration options, or tools for interacting with content in a primary window, and typically appears only when people need it. There’s no need to provide access to the font panel or text color panel because the Format menu lists these panels.

The Window menu typically contains the following top-level menu items, listed in the following order.

Menu item| Action| Guidance  
---|---|---  
Minimize| Minimizes the active window to the Dock. Pressing the Option key changes this item to Minimize All.|   
Zoom| Toggles between a predefined size appropriate to the window’s content and the window size people set. Pressing the Option key changes this item to Zoom All.| Avoid using Zoom to enter or exit full-screen mode. The [View menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#View-menu) supports these functions.  
Show Previous Tab| Shows the tab before the current tab in a tab-based window.|   
Show Next Tab| Shows the tab after the current tab in a tab-based window.|   
Move Tab to New Window| Opens the current tab in a new window.|   
Merge All Windows| Combines all open windows into a single tabbed window.|   
Enter/Exit Full Screen| In an app that supports a [full-screen experience](https://developer.apple.com/design/human-interface-guidelines/going-full-screen), opens the window at full-screen size in a new space.| Include this item in the Window menu only if your app doesn’t have a View menu. In this scenario, continue to provide separate Minimize and Zoom menu items.  
Bring All to Front| Brings all an app’s open windows to the front, maintaining their onscreen location, size, and layering order. (Clicking the app icon in the Dock has the same effect.) Pressing the Option key changes this item to Arrange in Front, which brings an app’s windows to the front in a neatly tiled arrangement.|   
_Name of an open app-specific window_|  Brings the selected window to the front.| List the currently open windows in alphabetical order for easy scanning. Avoid listing panels or other modal views.  
  
## [Help menu](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Help-menu)

The Help menu — located at the trailing end of the menu bar — provides access to an app’s help documentation. When you use the Help Book format for this documentation, macOS automatically includes a search field at the top of the Help menu.

Menu item| Action| Guidance  
---|---|---  
Send _YourAppName_ Feedback to Apple| Opens the Feedback Assistant, in which people can provide feedback.|   
_YourAppName_ Help| When the content uses the Help Book format, opens the content in the built-in Help Viewer.|   
_Additional Item_| |  Use a separator between your primary help documentation and additional items, which might include registration information or release notes. Keep the total the number of items you list in the Help menu small to avoid overwhelming people with too many choices when they need help. Alternatively, consider linking to additional items from within your help documentation.  
  
For guidance, see [Offering help](https://developer.apple.com/design/human-interface-guidelines/offering-help); for developer guidance, see [`NSHelpManager`](https://developer.apple.com/documentation/AppKit/NSHelpManager).

## [Dynamic menu items](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Dynamic-menu-items)

In rare cases, it can make sense to present a _dynamic menu item_ , which is a menu item that changes its behavior when people choose it while pressing a modifier key (Control, Option, Shift, or Command). For example, the _Minimize_ item in the Window menu changes to _Minimize All_ when people press the Option key.

**Avoid making a dynamic menu item the only way to accomplish a task.** Dynamic menu items are hidden by default, so they’re best suited to offer shortcuts to advanced actions that people can accomplish in other ways. For example, if someone hasn’t discovered the _Minimize All_ dynamic menu item in the Window menu, they can still minimize each open window.

**Use dynamic menu items primarily in menu bar menus.** Adding a dynamic menu item to contextual or Dock menus can make the item even harder for people to discover.

**Require only a single modifier key to reveal a dynamic menu item.** It can be physically awkward to press more than one key while simultaneously opening a menu and choosing a menu item, in addition to reducing the discoverability of the dynamic behavior. For developer guidance, see [`isAlternate`](https://developer.apple.com/documentation/AppKit/NSMenuItem/isAlternate).

Tip

macOS automatically sets the width of a menu to hold the widest item, including dynamic menu items.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Platform-considerations)

 _Not supported in iOS, tvOS, visionOS, or watchOS._

### [iPadOS](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#iPadOS)

The menu bar displays the top-level menus for your app or game, including both system-provided menus and any custom ones you choose to add. People reveal the menu bar by moving the pointer to the top edge of the screen, or swiping down from it. When visible, the menu bar occupies the same vertical space as the [status bar](https://developer.apple.com/design/human-interface-guidelines/status-bars) at the top edge of the screen.

As with the macOS menu bar, the iPadOS menu bar provides a familiar way for people to learn what an app does, find the commands they need, and discover keyboard shortcuts. While they are similar in most respects, there are a few key differences between the menu bars on each platform.

| iPadOS| macOS  
---|---|---  
Menu bar visibility| Hidden until revealed| Visible by default  
Horizontal alignment| Centered| Leading side  
Menu bar extras| Not available| System default and custom  
Window controls| In the menu bar when the app is full screen| Never in the menu bar  
Apple menu| Not available| Always available  
App menu| About, Services, and app visibility-related items not available| Always available  
  
**Because the menu bar is often hidden when running an app full screen, ensure that people can access all of your app’s functions through its UI.** In particular, always offer other ways to accomplish tasks assigned to dynamic menu items, since these are only available when a hardware keyboard is connected. Avoid using the menu bar as a catch-all location for functionality that doesn’t fit in elsewhere.

**Reserve the YourAppName > Settings menu item for opening your app’s page in iPadOS Settings.** If your app includes its own internal preferences area, link to it with a separate menu item beneath Settings in the same group. Place any other custom app-wide configuration options in this section as well.

**For apps with tab-style navigation, consider adding each tab as a menu item in the View menu.** Since each tab is a different view of the app, the View menu is a natural place to offer an additional way to navigate between tabs. If you do this, consider assigning key bindings to each tab to make navigation even more convenient.

**Consider grouping menu items into submenus to conserve vertical space.** Menu item rows on iPad use more space than on Mac to make them easier to tap. Because of this, and the smaller screen sizes of some iPads, it can be helpful to group related items into submenus more frequently than in the menu bar on Mac.

### [macOS](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#macOS)

The menu bar in macOS includes the Apple menu, which is always the first item on the leading side of the menu bar. The Apple menu includes system-defined menu items that are always available, and you can’t modify or remove it. Space permitting, the system can also display menu bar extras in the trailing end of the menu bar. For guidance, see [Menu bar extras](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Menu-bar-extras).

When menu bar space is constrained, the system prioritizes the display of menus and essential menu bar extras. To ensure that menus remain readable, the system may decrease the space between the titles, truncating them if necessary.

When people enter full-screen mode, the menu bar typically hides until they reveal it by moving the pointer to the top of the screen. For guidance, see [Going full screen](https://developer.apple.com/design/human-interface-guidelines/going-full-screen).

#### [Menu bar extras](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Menu-bar-extras)

A menu bar extra exposes app-specific functionality using an icon that appears in the menu bar when your app is running, even when it’s not the frontmost app. Menu bar extras are on the opposite side of the menu bar from your app’s menus. For developer guidance, see [`MenuBarExtra`](https://developer.apple.com/documentation/SwiftUI/MenuBarExtra).

When necessary, the system hides menu bar extras to make room for app menus. Similarly, if there are too many menu bar extras, the system may hide some to avoid crowding app menus.

<!-- image: A screenshot of the Input menu bar extra and its menu. -->

**Consider using a symbol to represent your menu bar extra.** You can create an [icon](https://developer.apple.com/design/human-interface-guidelines/icons) or you can choose one of the [SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols), using it as-is or customizing it to suit your needs. Both interface icons and symbols use black and clear colors to define their shapes; the system can apply other colors to the black areas in each image so it looks good on both dark and light menu bars, and when your menu bar extra is selected. The menu bar’s height is 24 pt.

**Display a menu — not a popover — when people click your menu bar extra.** Unless the app functionality you want to expose is too complex for a menu, avoid presenting it in a [popover](https://developer.apple.com/design/human-interface-guidelines/popovers).

**Let people — not your app — decide whether to put your menu bar extra in the menu bar.** Typically, people add a menu bar extra to the menu bar by changing a setting in an app’s settings window. To ensure discoverability, however, consider giving people the option of doing so during setup.

**Avoid relying on the presence of menu bar extras.** The system hides and shows menu bar extras regularly, and you can’t be sure which other menu bar extras people have chosen to display or predict the location of your menu bar extra.

**Consider exposing app-specific functionality in other ways, too.** For example, you can provide a [Dock menu](https://developer.apple.com/design/human-interface-guidelines/dock-menus) that appears when people Control-click your app’s Dock icon. People can hide or choose not to use your menu bar extra, but a Dock menu is aways available when your app is running.

## [Resources](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Related)

[Menus](https://developer.apple.com/design/human-interface-guidelines/menus)

[Dock menus](https://developer.apple.com/design/human-interface-guidelines/dock-menus)

[Standard keyboard shortcuts](https://developer.apple.com/design/human-interface-guidelines/keyboards#Standard-keyboard-shortcuts)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Developer-documentation)

[`CommandMenu`](https://developer.apple.com/documentation/SwiftUI/CommandMenu) — SwiftUI

[Adding menus and shortcuts to the menu bar and user interface](https://developer.apple.com/documentation/UIKit/adding-menus-and-shortcuts-to-the-menu-bar-and-user-interface) — UIKit

[`NSStatusBar`](https://developer.apple.com/documentation/AppKit/NSStatusBar) — AppKit

#### [Videos](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Videos)

[<!-- image:  --> Elevate the design of your iPad app ](https://developer.apple.com/videos/play/wwdc2025/208)

## [Change log](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar#Change-log)

Date| Changes  
---|---  
June 9, 2025| Added guidance for the menu bar in iPadOS.

---

## Reference: Toolbars

|---  
December 16, 2025| Updated guidance for Liquid Glass.  
June 9, 2025| Added guidance for grouping bar items, updated guidance for using symbols, and incorporated navigation bar guidance.  
June 21, 2023| Updated to include guidance for visionOS.  
June 5, 2023| Updated guidance for using toolbars in watchOS.
