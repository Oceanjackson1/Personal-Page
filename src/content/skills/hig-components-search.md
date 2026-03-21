---
title: "Hig Components Search"
description: "Apple HIG guidance for navigation-related components including search fields, page controls, and path controls."
category: "development"
source: "community"
author: "Community"
tags: ["hig", "components", "search"]
date: 2026-03-20
---

# Apple HIG: Navigation Components

Check for `.claude/apple-design-context.md` before asking questions. Use existing context and only ask for information not already covered.

## Key Principles

1. **Search: discoverable with instant feedback.** Place search fields where users expect them (top of list, toolbar/navigation bar). Show results as the user types.

2. **Page controls: position in a flat page sequence.** For discrete, equally weighted pages (onboarding, photo gallery). Show current page and total count.

3. **Path controls: file hierarchy navigation.** macOS path controls display location within a directory structure and allow jumping to any ancestor.

4. **Search scopes narrow large result sets.** Provide scope buttons so users can filter without complex queries.

5. **Clear empty states for search.** Helpful message suggesting corrections or alternatives, not a blank screen.

6. **Page controls are not for hierarchical navigation.** Flat, linear sequences only. Use navigation controllers, tab bars, or sidebars for hierarchy.

7. **Keep path controls concise.** Show meaningful segments only. Users can click any segment to navigate directly.

8. **Support keyboard for search.** Command-F and system search shortcuts should activate search.

## Reference Index

| Reference | Topic | Key content |
|---|---|---|
| [search-fields.md](references/search-fields.md) | Search fields | Scopes, tokens, instant results, placement |
| [page-controls.md](references/page-controls.md) | Page controls | Dot indicators, flat page sequences |
| [path-controls.md](references/path-controls.md) | Path controls | Breadcrumbs, ancestor navigation |

## Output Format

1. **Component recommendation** -- search field, page control, or path control, and why.
2. **Behavior specification** -- interaction model (search-as-you-type, swipe for pages, click-to-navigate for paths).
3. **Platform differences** across iOS, iPadOS, macOS, visionOS.

## Questions to Ask

1. What type of content is being searched or navigated?
2. Which platforms?
3. How large is the dataset?
4. Is search the primary interaction?

## Related Skills

- **hig-components-menus** -- Toolbars and menu bars hosting search and navigation controls
- **hig-components-controls** -- Text fields, pickers, segmented controls in search interfaces
- **hig-components-dialogs** -- Popovers and sheets for expanded search or filtering
- **hig-patterns** -- Navigation patterns and information architecture
- **hig-foundations** -- Typography and layout for navigation components

---

*Built by [Raintree Technology](https://raintree.technology) · [More developer tools](https://raintree.technology)*

## When to Use
This skill is applicable to execute the workflow or actions described in the overview.

---

## Reference: Page Controls

|---  
June 21, 2023| Updated to include guidance for visionOS.  
June 5, 2023| Updated guidance for using page controls in watchOS.

---

## Reference: Path Controls

---
title: "Path controls | Apple Developer Documentation"
source: https://developer.apple.com/design/human-interface-guidelines/path-controls

# Path controls

A path control shows the file system path of a selected file or folder.

<!-- image: A stylized representation of a path control for a HIG Design document showing its root disk, parent folder, and selected item. The image is tinted red to subtly reflect the red in the original six-color Apple logo. -->

For example, choosing View > Show Path Bar in the Finder displays a path bar at the bottom of the window. It shows the path of the selected item, or the path of the window’s folder if nothing is selected.

There are two styles of path control.

<!-- image: A screenshot of a Finder path bar that displays a hierarchy of four locations. -->

**Standard.** A linear list that includes the root disk, parent folders, and selected item. Each item appears with an icon and a name. If the list is too long to fit within the control, it hides names between the first and last items. If you make the control editable, people can drag an item onto the control to select the item and display its path in the control.

<!-- image: A screenshot of a path control showing a folder icon and a pop-up control. -->

**Pop up.** A control similar to a [pop-up button](https://developer.apple.com/design/human-interface-guidelines/pop-up-buttons) that shows the icon and name of the selected item. People can click the item to open a menu containing the root disk, parent folders, and selected item. If you make the control editable, the menu contains an additional Choose command that people can use to select an item and display it in the control. They can also drag an item onto the control to select it and display its path.

## [Best practices](https://developer.apple.com/design/human-interface-guidelines/path-controls#Best-practices)

**Use a path control in the window body, not the window frame.** Path controls aren’t intended for use in toolbars or status bars. Note that the path control in the Finder appears at the bottom of the window body, not in the status bar.

## [Platform considerations](https://developer.apple.com/design/human-interface-guidelines/path-controls#Platform-considerations)

 _Not supported in iOS, iPadOS, tvOS, visionOS, or watchOS._

## [Resources](https://developer.apple.com/design/human-interface-guidelines/path-controls#Resources)

#### [Related](https://developer.apple.com/design/human-interface-guidelines/path-controls#Related)

[File management](https://developer.apple.com/design/human-interface-guidelines/file-management)

#### [Developer documentation](https://developer.apple.com/design/human-interface-guidelines/path-controls#Developer-documentation)

[`NSPathControl`](https://developer.apple.com/documentation/AppKit/NSPathControl) — AppKit

---

## Reference: Search Fields

|---  
June 9, 2025| Updated guidance for search placement in iOS, consolidated iPadOS and macOS platform considerations, and added guidance for tokens.  
September 12, 2023| Combined guidance common to all platforms.  
June 5, 2023| Added guidance for using search fields in watchOS.
